import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import gdown
from datetime import datetime

# Set page config at the very beginning
st.set_page_config(
    page_title="Stock Portfolio Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Google Drive File ID and filename
GOOGLE_DRIVE_FILE_ID = "13lT8UO4HKq_3lY7MVxZptUvO8X3vTrQQw_yPZk-FPW8"
FILE_NAME = "GoogleSummary1.xlsm"

# Portfolio configurations
MD_ALLOWED_SYMBOLS = [
    "TARIL", 
]

GOINVESTX_ALLOWED_SYMBOLS = [
    "RIR",  "SAGILITY", "POWERINDIA", "GILLETTE"
]

NEW_AGE_STOCKS = [
    "AIIL",  "SHAKTIPUMP", "SKYGOLD", "TARIL", "TECHNOE", "WEALTH", "WOCKPHARMA"
]

# Buy rates for each portfolio
MD_BUY_RATES = {
    "TARIL": 733.83, 
}

GOINVESTX_BUY_RATES = {
    "RIR": 3625.68, "SAGILITY": 48.97, "POWERINDIA": 11380.35, "GILLETTE": 8892.50
}

NEWAGE_BUY_RATES = {
    "AIIL": 1653.67,  "SHAKTIPUMP": 728.05, "SKYGOLD": 271.77, "TARIL": 733.83, "TECHNOE": 1549.07,
    "WEALTH": 1331.86, "WOCKPHARMA": 1109.2
}

@st.cache_data(ttl=300)
def download_from_drive(file_id, filename):
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        gdown.download(url, filename, quiet=False)
        return filename
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")
        return None

def load_local_data(filename):
    try:
        if os.path.exists(filename):
            return pd.read_excel(filename, sheet_name="Summary")
        else:
            st.error(f"File {filename} not found locally.")
            return None
    except Exception as e:
        st.error(f"Error loading local file: {str(e)}")
        return None

@st.cache_data(ttl=300)
def load_and_process_data(filename, allowed_symbols, buy_rates):
    try:
        # Try to load the actual file
        data = load_local_data(filename)
        
        if data is None:
            st.info("Using sample data for demonstration")
            data = generate_sample_data(allowed_symbols, buy_rates)

        # Process columns
        data.columns = data.columns.astype(str)
        if "DATE1" in data.columns:
            data.drop(columns=["DATE1"], inplace=True)

        # Handle date columns
        date_cols = [col for col in data.columns if "-" in col and col[:4].isdigit()]
        dates = {col: pd.to_datetime(col).strftime('%d %b').upper() for col in date_cols}

        # Rename columns
        rename_dict = {}
        for col in data.columns:
            if col in dates:
                rename_dict[col] = f"{dates[col]} (in %)"
            elif col not in ["SYMBOL", "CLOSE", "BUY RATE"]:
                rename_dict[col] = f"{col} (in %)"

        data.rename(columns=rename_dict, inplace=True)

        # Filter and process data
        data["SYMBOL"] = data["SYMBOL"].fillna("UNKNOWN")
        filtered = data[data["SYMBOL"].isin(allowed_symbols)].copy()
        filtered.reset_index(drop=True, inplace=True)
        filtered.index += 1

        # Calculate ROI
        filtered["BUY RATE"] = filtered["SYMBOL"].map(buy_rates)
        filtered["ROI (in %)"] = ((filtered["CLOSE"] - filtered["BUY RATE"]) / filtered["BUY RATE"] * 100).round(2)

        # Order columns
        cols = ["SYMBOL", "BUY RATE", "ROI (in %)", "CLOSE"]
        cols.extend([col for col in filtered.columns if col not in cols])
        filtered = filtered[cols]

        return filtered

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def create_performance_chart(data):
    roi_data = data.sort_values("ROI (in %)")

    fig = go.Figure()
    colors = roi_data["ROI (in %)"].apply(lambda x: 'red' if x < 0 else 'green' if x <= 5 else 'orange')

    fig.add_trace(go.Bar(
        x=roi_data["SYMBOL"],
        y=roi_data["ROI (in %)"],
        marker_color=colors,
        name="ROI"
    ))

    fig.update_layout(
        title="Portfolio Performance by Stock",
        xaxis=dict(
            title="Stock Symbol",
            title_font=dict(color="black"),
            tickangle=270,
            tickfont=dict(size=14, color="orange")
        ),
        yaxis_title="ROI (%)",
        template="plotly_dark",
        height=400,
        showlegend=False,
    )

    return fig

def main():
    st.title("Stock Portfolio Dashboard")

    # Portfolio selection
    portfolio = st.selectbox(
        "Select Portfolio",
        ["MD Portfolio", "GOINVESTX Portfolio", "NEW AGE Portfolio"]
    )

    # Map selection to data
    if portfolio == "MD Portfolio":
        symbols = MD_ALLOWED_SYMBOLS
        rates = MD_BUY_RATES
    elif portfolio == "GOINVESTX Portfolio":
        symbols = GOINVESTX_ALLOWED_SYMBOLS
        rates = GOINVESTX_BUY_RATES
    else:
        symbols = NEW_AGE_STOCKS
        rates = NEWAGE_BUY_RATES

    # Download the file from Google Drive
    downloaded_file = download_from_drive(GOOGLE_DRIVE_FILE_ID, FILE_NAME)
    if downloaded_file is None:
        st.error("Failed to download the file. Please check the Google Drive link and try again.")
        return

    # Load and process data
    data = load_and_process_data(FILE_NAME, symbols, rates)

    if data is not None:
        # Portfolio metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            avg_roi = data["ROI (in %)"].mean()
            st.metric("Average ROI", f"{avg_roi:.2f}%")

        with col2:
            profitable = len(data[data["ROI (in %)"] > 0])
            st.metric("Stocks in Profit", profitable)

        with col3:
            best = data.loc[data["ROI (in %)"].idxmax()]
            st.metric("Top Performer", f"{best['SYMBOL']} ({best['ROI (in %)']}%)")

        # Performance chart
        st.plotly_chart(create_performance_chart(data), use_container_width=True)

        # Data table
        st.subheader(f"{portfolio} Summary Table")
        st.dataframe(
            data.style.format(precision=2)
            .apply(lambda x: [
                'color: red; font-weight: bold' if isinstance(v, (int, float)) and v < 0 else
                'color: green; font-weight: bold' if isinstance(v, (int, float)) and 0 < v <= 5 else
                'color: blue; font-weight: bold' if isinstance(v, (int, float)) and v > 5 else
                '' for v in x
            ], axis=1),
            use_container_width=True,
            height=500,
        )

        # Download option
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Data as CSV",
            csv,
            f"{portfolio.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

if __name__ == "__main__":
    main()
