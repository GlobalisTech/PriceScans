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
FILE_NAME = "GoogleSummary.xlsm"

# Define allowed symbols for different portfolios
MD_ALLOWED_SYMBOLS = [
    "TARIL", "AIIL", "NETWEB", "GRAVITA", "SKYGOLD", "WEALTH", "WEBELSOLAR", "AWFIS",
    "KAYNES", "POKARNA", "NIBE", "VOLTAMP", "AWHCL", "SHILCTECH", "ANANTRAJ", "POCL",
    "GOLDIAM", "REFEX", "RIR", "TECHNOE", "ECORECO", "CEINSYSTECH", "E2E", "MINID",
    "QUICKHEAL", "SHAKTIPUMP", "WOCKPHARMA", "NEULANDLAB", "SENCO", "VEEFIN", "INA",
    "OLATECH", "ORIANA"
]

GOINVESTX_ALLOWED_SYMBOLS = [
    "RIR", "MINID", "VUENOW", "KAYNES", "E2E", "REFEX", "SHAKTIPUMP", "OLECTRA", 
    "INA", "POKARNA", "EPIGRAL", "FOCUS", "PPLPHARMA", "JUBLPHARMA", "KSOLVES", 
    "V2RETAIL", "SUZLON", "EPACK", "SAGILITY",
]

NEW_AGE_STOCKS = [
    "AIIL", "ALPHALOGIC", "ANANTRAJ", "AURIONPRO", "AWHCL", "CEINSYSTECH", 
    "E2E", "ECORECO", "GOLDIAM", "INA", "KAYNES", "MINID", "NETWEB", "NEULANDLAB", 
    "NIBE", "OLATECH", "ORIANA", "POCL", "POKARNA", "QUICKHEAL", "REFEX", "RIR", 
    "SENCO", "SHAKTIPUMP", "SKYGOLD", "TARIL", "TECHNOE", "WEALTH", "WOCKPHARMA"
]

PARUL_PORTFOLIO = [
    "AIRTELPP", "BHARTIARTL", "CGPOWER", "JSWENERGY", "M&M", "NPST", "POLYMED", 
    "RELIANCE", "SUZLON", "TITAGARH", "ZOMATO"]

WATCHLIST7 = [
"ACE", "AIIL", "AKUMS", "ALPHALOGIC", "ANANTRAJ", "AVANTEL", "APARINDS",
"AURIONPRO", "AVAILFC", "AVANTIFEED", "AWFIS", "AWHCL", "AZAD", "BSE",
"CDSL", "CEIGALL", "CEINSYSTECH", "DOMS", "DYNAMATECH", "E2E", "ECORECO",
"ETHOSLTD", "EXICOM", "FABCLEAN", "GMRAIRPORT", "GOLDIAM", "GRAUWEIL",
"GRAVITA", "GRWRHITCH", "GSLSU", "HBLENGINE", "HGINFRA", "HITECHGEAR",
"IKIO", "INA", "INOXWIND", "INTLCOMBQ", "IWEL", "JITFINFRA", "JOCIL",
"JSWENERGY", "KALAMANDIR", "KAYNES", "KPEL", "KPIGREEN", "LANDMARK",
"MALLCOM", "MCX", "MICEL", "MINID", "MOSCHIP", "NETWEB", "NEULANDLAB",
"NIBE", "OLATECH", "PAYTM", "PGEL", "PIGL", "PNCINFRA", "POCL", "POKARNA",
"POWERINDIA", "PRECAM", "PTCIL", "QUICKHEAL", "REFEX", "RIR", "SAGILITY",
"SAMHI", "SENCO", "SHAKTIPUMP", "SKYGOLD", "SOLARINDS", "SPANDANA", "SWELECTES",
"SWSOLAR", "TARIL", "TATAINVEST", "TECHNOE", "TIINDIA", "TRENT", "UNITECH", "VEDL",
"VEEFIN", "VISHAL", "WAAREENER", "WAAREERTL", "WABAG", "WEBELSOLAR", "WOCKPHARMA",
"ZOMATO", "WEALTH", "POWERMECH", "GMRP&UI"
]

# Define Buy Rates
MD_BUY_RATES = {
    "TARIL": 733.83, "AIIL": 1590.00, "NETWEB": 2779.63, "GRAVITA": 2346.30, "SKYGOLD": 271.77,
    "WEALTH": 1331.86, "WEBELSOLAR": 1378.00, "AWFIS": 732.24, "KAYNES": 5304.66, "POKARNA": 1147.92,
    "NIBE": 1977.25, "VOLTAMP": 10364.00, "AWHCL": 646.53, "SHILCTECH": 6244.00, "ANANTRAJ": 788.03,
    "POCL": 983.78, "GOLDIAM": 398.33, "REFEX": 486.66, "RIR": 3667.91, "TECHNOE": 1549.07,
    "ECORECO": 890.78, "CEINSYSTECH": 1487.43, "E2E": 4069.52, "MINID": 184.48, "QUICKHEAL": 656.82,
    "SHAKTIPUMP": 980.02, "WOCKPHARMA": 1196.21, "NEULANDLAB": 13373.00, "SENCO": 1175.06,
    "VEEFIN": 645.00, "ORIANA": 2267.68, "INA": 419.48, "OLATECH": 432.00
}

GOINVESTX_BUY_RATES = {
    
    "RIR": 3625.68,
    "MINID": 190.67,
    "VUENOW": 191.36,
    "KAYNES": 5499.68,
    "E2E": 2803.94,
    "REFEX": 461.88,
    "SHAKTIPUMP": 990.10,
    "OLECTRA": 1447.79,
    "INA": 306.86,
    "POKARNA": 1271.52,
    "EPIGRAL": 1861.76,
    "FOCUS": 86.38,
    "PPLPHARMA": 193.42,
    "JUBLPHARMA": 994.37,
    "KSOLVES": 461.45,
    "V2RETAIL": 1441.47,
    "SUZLON": 55.09,
    "EPACK": 398.31,
    "SAGILITY": 45.75

}

PARUL_STOCK_BUY_RATES = {
    'AIRTELPP': 1131.15,
    'BHARTIARTL': 1575.75,
    'CGPOWER': 628.84,
    'JSWENERGY': 621.69,
    'M&M': 1257.4,
    'NPST': 3033.0,
    'POLYMED': 1871.78,
    'RELIANCE': 0.0,
    'SUZLON': 32.1,
    'TITAGARH': 1334.02,
    'ZOMATO': 239.06
}

NEWAGE_BUY_RATES = {
    "ALPHALOGIC": 165.36,
    "ANANTRAJ": 645.81,
    "AWHCL": 717.16,
    "AURIONPRO": 1885.5,
    "AIIL": 1653.67,
    "CEINSYSTECH": 1507.38,
    "E2E": 3272.59,
    "ECORECO": 970.64,
    "GRWRHITECH": 4113.8,
    "GOLDIAM": 346.78,
    "POWERINDIA": 11625.72,
    "INA": 419.48,
    "KAYNES": 5304.66,
    "MINID": 195.81,
    "NETWEB": 2645.18,
    "NEULANDLAB": 13373,
    "NIBE": 1842.78,
    "OLATECH": 488,
    "ORIANA": 2284.21,
    "POKARNA": 1147.92,
    "POCL": 983.78,
    "QUICKHEAL": 633.03,
    "REFEX": 473.95,
    "RIR": 3667.91,
    "SENCO": 164.67,
    "SHAKTIPUMP": 757.65,
    "SKYGOLD": 271.77,
    "SOLARIND": 8827.2,
    "TECHNOE": 1428.5,
    "TARIL": 383.52,
    "WEALTH": 1331.86,
    "WOCKPHARMA": 1109.2
}

WATCHLIST7_BUY_RATES = {
    "ACE": 1233.1,
    "AIIL": 1501.9,
    "AKUMS": 509.4,
    "ALPHALOGIC": 98,
    "ANANTRAJ": 544.15,
    "APARINDS": 6299.55,
    "AURIONPRO": 1339.05,
    "AVAILFC": 235,
    "AVANTEL": 120.75,
    "AVANTIFEED": 708.95,
    "AWFIS": 669.95,
    "AWHCL": 556.05,
    "AZAD": 1352.5,
    "BSE": 5931.35,
    "CDSL": 1253.4,
    "CEIGALL": 263.15,
    "CEINSYSTECH": 1642.1,
    "DOMS": 2575.15,
    "DYNAMATECH": 6477,
    "E2E": 2206.8,
    "ECORECO": 612.3,
    "ETHOSLTD": 2583.95,
    "EXICOM": 172.45,
    "FABCLEAN": 310.85,
    "GMRAIRPORT": 70.97,
    "GMRP&UI": 111.1,
    "GOLDIAM": 406.8,
    "GRAUWEIL": 91,
    "GRAVITA": 1723.8,
    "GRWRHITCH": 4039.8,
    "GSLSU": 109.17,
    "HBLENGINE": 490.9,
    "HGINFRA": 1122.75,
    "HITECHGEAR": 653.35,
    "IKIO": 178.57,
    "INA": 241.75,
    "INOXWIND": 173.96,
    "INTLCOMBQ": 806,
    "IWEL": 9370,
    "JITFINFRA": 407.8,
    "JOCIL": 162,
    "JSWENERGY": 471.4,
    "KALAMANDIR": 156.46,
    "KAYNES": 4219.55,
    "KPEL": 416.5,
    "KPIGREEN": 414.2,
    "LANDMARK": 474.75,
    "MALLCOM": 1280,
    "MCX": 5701.65,
    "MICEL": 62.64,
    "MINID": 121,
    "MOSCHIP": 172.5,
    "NETWEB": 1616.95,
    "NEULANDLAB": 11440.35,
    "NIBE": 1037.15,
    "OLATECH": 275,
    "PAYTM": 754.3,
    "PGEL": 829.5,
    "PIGL": 231.95,
    "PNCINFRA": 256.4,
    "POCL": 683.05,
    "POKARNA": 1164.2,
    "POWERINDIA": 11117.5,
    "POWERMECH": 1963.55,
    "PRECAM": 221.15,
    "PTCIL": 10583,
    "QUICKHEAL": 373.6,
    "REFEX": 407.7,
    "RIR": 1659.85,
    "SAGILITY": 46.5,
    "SAMHI": 151.87,
    "SENCO": 336.15,
    "SHAKTIPUMP": 894.65,
    "SKYGOLD": 349,
    "SOLARINDS": 8915.2,
    "SPANDANA": 292.75,
    "SWELECTES": 635.5,
    "SWSOLAR": 291.6,
    "TARIL": 405.05,
    "TATAINVEST": 6093,
    "TECHNOE": 997.2,
    "TIINDIA": 2761.6,
    "TRENT": 5112.95,
    "UNITECH": 7.33,
    "VEDL": 434.5,
    "VEEFIN": 370.15,
    "VISHAL": 27.4,
    "WAAREENER": 2312,
    "WAAREERTL": 889.45,
    "WABAG": 1399,
    "WEALTH": 941.6,
    "WEBELSOLAR": 1107,
    "WOCKPHARMA": 1384.4,
    "ZOMATO": 233.51
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
    colors = roi_data["ROI (in %)"].apply(lambda x: 'red' if x < 0 else 'green' if x <= 5 else 'darkgreen')

    fig.add_trace(go.Bar(
        x=roi_data["SYMBOL"],
        y=roi_data["ROI (in %)"],
        marker_color=colors,
        name="ROI"
    ))

    # fig.update_layout(
    #     title="Portfolio Performance by Stock",
    #     xaxis=dict(
    #         title="Stock Symbol",
    #         title_font=dict(color="black"),
    #         tickangle=270,
    #         tickfont=dict(size=14, color="black")
    #     ),
    #     yaxis_title="ROI (%)",
    #     template="plotly_dark",
    #     height=400,
    #     showlegend=False,
    # )
    fig.update_layout(
    title="Portfolio Performance by Stock",
    xaxis=dict(
        title="Stock Symbol",
        title_font=dict(color="black"),
        tickangle=270,
        tickfont=dict(size=14, color="black")  # Changed to black
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
        ["NEW AGE PORTFOLIO", "PARUL PORTFOLIO", "GOINVESTX PORTFOLIO", "MD PORTFOLIO", "WATCHLIST7"]
    )

    # Map selection to data
    if portfolio == "MD Portfolio":
        symbols = MD_ALLOWED_SYMBOLS
        rates = MD_BUY_RATES
    elif portfolio == "GOINVESTX Portfolio":
        symbols = GOINVESTX_ALLOWED_SYMBOLS
        rates = GOINVESTX_BUY_RATES
    elif portfolio == "NEW AGE Portfolio":
        symbols = NEW_AGE_STOCKS
        rates = NEWAGE_BUY_RATES
    elif portfolio == "PARUL Portfolio":
        symbols = PARUL_PORTFOLIO
        rates = PARUL_STOCK_BUY_RATES
    else:
        symbols = WATCHLIST7
        rates = WATCHLIST7_BUY_RATES

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

            # if not data.empty and "ROI (in %)" in data.columns and data["ROI (in %)"].notna().any():
            #     best_index = data["ROI (in %)"].idxmax()
            #     if pd.notna(best_index) and best_index in data.index:
            #         best = data.loc[best_index]
            #         best_symbol = best["SYMBOL"]
            #         best_roi = best["ROI (in %)"]
            #     else:
            #         best_symbol = "None"
            #         best_roi = 0
            # else:
            #     best_symbol = "None"
            #     best_roi = 0
            st.metric("Top Performer", f"{best['SYMBOL']} ({best['ROI (in %)']}%)")
            
            # st.metric("Top Performer", f"{best_symbol} ({best_roi}%)")

        # Performance chart
        st.plotly_chart(create_performance_chart(data), use_container_width=True)

        # Data table
        # st.subheader(f"{portfolio} Summary Table")
        # st.dataframe(
        #     data.style.format(precision=2)
        #     .apply(lambda x: [
        #         'color: black; font-weight: bold' if x.name in ["BUY RATE"] else
        #     ], axis = 1),
        #     .apply(lambda x: [
        #         'color: red; font-weight: bold' if isinstance(v, (int, float)) and v < 0 else
        #         'color: green; font-weight: bold' if isinstance(v, (int, float)) and 0 < v <= 5 else
        #         'color: darkgreen; font-weight: bold' if isinstance(v, (int, float)) and v > 5 else
        #         '' for v in x
        #     ], axis=1),
        #     use_container_width=True,
        #     height=500,
        # )

        st.subheader(f"{portfolio} Summary Table")
        st.dataframe(
            data.style.format(precision=2)
            .apply(lambda x: ['color: black; font-weight: bold' if x.name == "BUY RATE" else '' for _ in x], axis=0)
            .apply(lambda x: [
                'color: red; font-weight: bold' if isinstance(v, (int, float)) and v < 0 else
                'color: green; font-weight: bold' if isinstance(v, (int, float)) and 0 < v <= 5 else
                'color: darkgreen; font-weight: bold' if isinstance(v, (int, float)) and v > 5 else
                
                '' for v in x
            ], axis=1),
            use_container_width=True,
            height=500,
        )
        # st.subheader(f"{portfolio} Summary Table")
        # st.dataframe(
        #     data.style.format(precision=2)
        #     # Apply color to BUY RATE column
        #     .apply(lambda x: ['color: black; font-weight: bold' if x.name == "BUY RATE" else '' for _ in x], axis=0)
        #     # Apply color coding for numerical columns
        #     .apply(lambda x: [
        #         'color: red; font-weight: bold' if isinstance(v, (int, float)) and v < 0 else
        #         'color: green; font-weight: bold' if isinstance(v, (int, float)) and 0 < v <= 5 else
        #         'color: darkgreen; font-weight: bold' if isinstance(v, (int, float)) and v > 5 else
        #         '' for v in x
        #     ], axis=1)
        #     # Apply dark green color to "ADD" in the REMARK column
        #     .apply(lambda x: [
        #         'color: darkgreen; font-weight: bold' if v == "ADD" else '' for v in x
        #     ], axis=1, subset=['REMARK (in %)']),
        #     use_container_width=True,
        #     height=500,
        # )

        
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
