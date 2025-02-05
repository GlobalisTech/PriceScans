import streamlit as st
import pandas as pd
import os
import requests
import gdown
from datetime import datetime, timedelta

# Google Drive File ID
GOOGLE_DRIVE_FILE_ID = "13lT8UO4HKq_3lY7MVxZptUvO8X3vTrQQw_yPZk-FPW8"
FILE_NAME = "GoogleSummary.xlsm"

# Function to download file from Google Drive
def download_from_drive(file_id, filename="GoogleSummary.xlsm"):
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        gdown.download(url, filename, quiet=False)
        print(f"Downloaded: {filename}")
        return filename
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")
        return None

# Download file
SUMMARY_FILE_PATH = download_from_drive(GOOGLE_DRIVE_FILE_ID)

# Portfolio Symbols
MD_ALLOWED_SYMBOLS = ["TARIL", "AIIL", "NETWEB", "GRAVITA", "SKYGOLD", "WEALTH", "WEBELSOLAR", "AWFIS"]
GOINVESTX_ALLOWED_SYMBOLS = ["RIR", "MINID", "VUENOW", "KAYNES", "AVANTIFEED", "CYIENT", "DIXON", "E2E"]
NEW_AGE_STOCKS = ["AIIL", "ALPHALOGIC", "ANANTRAJ", "AURIONPRO", "AWFIS", "AWHCL", "CEINSYSTECH", "E2E"]

# Buy Rates
MD_BUY_RATES = {"TARIL": 733.83, "AIIL": 1590.00, "NETWEB": 2779.63, "GRAVITA": 2346.30}
GOINVESTX_BUY_RATES = {"RIR": 3625.68, "MINID": 190.67, "VUENOW": 191.36, "KAYNES": 6662.37}
NEWAGE_BUY_RATES = {"AIIL": 1653.67, "ALPHALOGIC": 165.36, "ANANTRAJ": 673.15, "AURIONPRO": 1885.5}

def main():
    st.set_page_config(page_title="Stock Portfolio Dashboard", layout="wide")
    st.title("Stock Portfolio Dashboard")

    # Portfolio selection
    portfolio_option = st.selectbox(
        "Select Portfolio",
        options=["MD Portfolio", "GOINVESTX Portfolio", "NEW AGE Portfolio"],
        index=0,
    )

    # Assign symbols and buy rates dynamically
    if portfolio_option == "MD Portfolio":
        ALLOWED_SYMBOLS, BUY_RATES = MD_ALLOWED_SYMBOLS, MD_BUY_RATES
    elif portfolio_option == "GOINVESTX Portfolio":
        ALLOWED_SYMBOLS, BUY_RATES = GOINVESTX_ALLOWED_SYMBOLS, GOINVESTX_BUY_RATES
    else:
        ALLOWED_SYMBOLS, BUY_RATES = NEW_AGE_STOCKS, NEWAGE_BUY_RATES

    try:
        if not os.path.exists(SUMMARY_FILE_PATH):
            st.error(f"File {SUMMARY_FILE_PATH} not found.")
            return

        # Load the Summary sheet
        sheets = pd.read_excel(SUMMARY_FILE_PATH, sheet_name=None)
        if "Summary" not in sheets:
            st.error("Sheet 'Summary' not found in the Excel file.")
            return

        summary_data = sheets["Summary"]
        summary_data.columns = summary_data.columns.astype(str)

        # Validate Required Columns
        required_cols = ["SYMBOL", "CLOSE"]
        for col in required_cols:
            if col not in summary_data.columns:
                st.error(f"Missing required column: {col}")
                return

        # Process Date Columns
        dynamic_columns = [col for col in summary_data.columns if "-" in col and col[:4].isdigit()]
        date_mapping = {col: pd.to_datetime(col, errors='coerce').date() for col in dynamic_columns}
        sorted_dynamic_columns = sorted(date_mapping, key=date_mapping.get)
        renamed_columns = {col: date_mapping[col].strftime('%d %b').upper() for col in sorted_dynamic_columns}

        for col in summary_data.columns:
            if col not in required_cols:
                renamed_columns[col] = f"{renamed_columns.get(col, col)} (in %)"

        summary_data.rename(columns=renamed_columns, inplace=True)

        # Round numeric columns
        numeric_cols = summary_data.select_dtypes(include=['number']).columns
        summary_data[numeric_cols] = summary_data[numeric_cols].round(2)

        # Filter by Portfolio
        summary_data["SYMBOL"] = summary_data["SYMBOL"].fillna("UNKNOWN").astype(str)
        filtered_data = summary_data[summary_data["SYMBOL"].isin(ALLOWED_SYMBOLS)]
        filtered_data.reset_index(drop=True, inplace=True)
        filtered_data.index = filtered_data.index + 1

        # Calculate ROI
        filtered_data["BUY RATE"] = filtered_data["SYMBOL"].map(BUY_RATES)
        filtered_data["ROI (in %)"] = ((filtered_data["CLOSE"] - filtered_data["BUY RATE"]) / filtered_data["BUY RATE"]) * 100
        filtered_data["ROI (in %)"] = filtered_data["ROI (in %)"].round(2)

        # Column Order
        column_order = ["SYMBOL", "BUY RATE", "ROI (in %)", "CLOSE"] + \
                       [col for col in filtered_data.columns if col not in ["SYMBOL", "BUY RATE", "ROI (in %)", "CLOSE"]]
        filtered_data = filtered_data[column_order]

        # Apply Color Formatting
        def color_text(val):
            try:
                num_val = float(val)
                if num_val > 5:
                    return "color: blue; font-weight: bold;"
                elif 0 < num_val <= 5:
                    return "color: green; font-weight: bold;"
                elif num_val < 0:
                    return "color: red; font-weight: bold;"
                return ""
            except:
                return ""

        color_columns = [col for col in filtered_data.columns if col not in ["SYMBOL", "BUY RATE", "CLOSE"]]
        filtered_data[color_columns] = filtered_data[color_columns].round(2)

        styled_table = filtered_data.style.applymap(color_text, subset=color_columns)
        styled_table = styled_table.set_properties(
            subset=[col for col in filtered_data.columns if col not in ["SYMBOL"]],
            **{"text-align": "right"}
        )

        # Display Data
        st.subheader(f"{portfolio_option} Summary Table")
        st.data_editor(filtered_data.style.format(precision=2), use_container_width=True, height=500)

        # Provide CSV download option
        csv_data = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name=f"{portfolio_option.lower().replace(' ', '_')}_summary.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
