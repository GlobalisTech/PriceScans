import streamlit as st
import pandas as pd
import os
import requests
import gdown
from datetime import datetime, timedelta

# Google Drive File ID
GOOGLE_DRIVE_FILE_ID = "13lT8UO4HKq_3lY7MVxZptUvO8X3vTrQQw_yPZk-FPW8"
FILE_NAME = "GoogleSummary1.xlsm"


# Apply CSS Styling
st.markdown(
    """
    <style>
    /* Custom Styling for Dashboard */
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: black;
    }

    /* Italicize Table Headers */
    table thead th {
        font-style: italic;
        font-size: 16px;
        color: black;
        font-weight: bold;
    }

    /* Bold Table Data */
    table tbody td {
        font-weight: bold;
        font-size: 14px;
    }

    /* Align numbers to the right */
    .dataframe td {
        text-align: right;
    }

    /* Color positive & negative values */
    .dataframe td:nth-child(n+3) {
        color: black;
    }
    
    .dataframe td:nth-child(n+3):contains("-") {
        color: red;
    }
    
    .dataframe td:nth-child(n+3):not(:contains("-")) {
        color: green;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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
        
def ensure_latest_file(file_id, filename):
    if os.path.exists(filename):
        os.remove(filename)
    return download_from_drive(file_id, filename)


# def download_from_drive(file_id, filename):
#     url = f"https://drive.google.com/uc?export=download&id={file_id}"
#     response = requests.get(url)
#     with open(filename, "wb") as file:
#         file.write(response.content)
#     return filename

# Download file
SUMMARY_FILE_PATH = ensure_latest_file(GOOGLE_DRIVE_FILE_ID, FILE_NAME)

# Define allowed symbols for different portfolios
MD_ALLOWED_SYMBOLS = [
    "TARIL", "AIIL", "NETWEB", "GRAVITA", "SKYGOLD", "WEALTH", "WEBELSOLAR", "AWFIS",
    "KAYNES", "POKARNA", "NIBE", "VOLTAMP", "AWHCL", "SHILCTECH", "ANANTRAJ", "POCL",
    "GOLDIAM", "REFEX", "RIR", "TECHNOE", "ECORECO", "CEINSYSTECH", "E2E", "MINID",
    "QUICKHEAL", "SHAKTIPUMP", "WOCKPHARMA", "NEULANDLAB", "SENCO", "VEEFIN", "INA",
    "OLATECH", "ORIANA"
]

GOINVESTX_ALLOWED_SYMBOLS = [
    "RIR", "MINID", "VUENOW", "KAYNES", "AVANTIFEED", "CYIENT", "DIXON", "E2E",
    "REFEX", "TARIL", "CEINSYSTECH", "SHAKTIPUMP", "BEL", "BDL", "OLECTRA", "HAL",
    "INA", "SAGILITY", "POWERINDIA", "GILLETTE"
]

NEW_AGE_STOCKS = [
    "AIIL", "ALPHALOGIC", "ANANTRAJ", "AURIONPRO", "AWFIS", "AWHCL", "CEINSYSTECH", 
    "E2E", "ECORECO", "GOLDIAM", "INA", "KAYNES", "MINID", "NETWEB", "NEULANDLAB", 
    "NIBE", "OLATECH", "ORIANA", "POCL", "POKARNA", "QUICKHEAL", "REFEX", "RIR", 
    "SENCO", "SHAKTIPUMP", "SKYGOLD", "TARIL", "TECHNOE", "WEALTH", "WOCKPHARMA"
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
    "RIR": 3625.68, "MINID": 190.67, "VUENOW": 191.36, "KAYNES": 6662.37, "AVANTIFEED": 681.04, "CYIENT": 1426.32,
    "DIXON": 15642.97, "E2E": 3317.01, "REFEX": 473.48, "TARIL": 932.29, "CEINSYSTECH": 1678.61, "SHAKTIPUMP": 990.10,
    "BEL": 290.69, "BDL": 1324.02, "OLECTRA": 1447.79, "HAL": 3926.65, "INA": 306.86, "SAGILITY": 48.97, "POWERINDIA": 11380.35,
    "GILLETTE": 8892.50
}


NEWAGE_BUY_RATES = {}

NEWAGE_BUY_RATES = {
    "AIIL": 1653.67,"ALPHALOGIC": 165.36, "ANANTRAJ": 673.15, "AURIONPRO": 1885.5, "AWFIS": 732.24,
    "AWHCL": 717.16, "CEINSYSTECH": 1487.43, "E2E": 3043.68, "ECORECO": 970.64, "GOLDIAM": 346.78,
    "INA": 419.48, "KAYNES": 5304.66, "MINID": 195.81, "NETWEB": 2660.83, "NEULANDLAB": 13373.00,
    "NIBE": 1900.08, "OLATECH": 488.00, "ORIANA": 2267.68, "POCL": 983.78, "POKARNA": 1147.92,
    "QUICKHEAL": 656.82, "REFEX": 486.66, "RIR": 3667.91, "SENCO": 619.83, "SHAKTIPUMP": 728.05,
    "SKYGOLD": 271.77, "TARIL": 733.83, "TECHNOE": 1549.07, "WEALTH": 1331.86, "WOCKPHARMA": 1109.2
}


def main():
    st.set_page_config(page_title="Stock Portfolio Dashboard", layout="wide")
    st.title("Stock Portfolio Dashboard")

    # # File Upload Option (Newly Added)
    # uploaded_file = st.file_uploader("Upload your file (.csv)", type=["csv"])

    # if uploaded_file:
    #     st.success("Uploaded file will be used.")
    #     SUMMARY_FILE_PATH = uploaded_file  # Directly use the uploaded file
    # else:
    #     st.info("No file uploaded. Fetching from Google Drive...")
    #     SUMMARY_FILE_PATH = ensure_latest_file(GOOGLE_DRIVE_FILE_ID, FILE_NAME)

     # Portfolio selection
    portfolio_option = st.selectbox(
        "Select Portfolio",
        options=["MD Portfolio", "GOINVESTX Portfolio", "NEW AGE Portfolio"],
        index=0,
    )

    # Assign symbols and buy rates dynamically
    if portfolio_option == "MD Portfolio":
        ALLOWED_SYMBOLS = MD_ALLOWED_SYMBOLS
        BUY_RATES = MD_BUY_RATES
    elif portfolio_option == "GOINVESTX Portfolio":
        ALLOWED_SYMBOLS = GOINVESTX_ALLOWED_SYMBOLS
        BUY_RATES = GOINVESTX_BUY_RATES
    else:
        ALLOWED_SYMBOLS = NEW_AGE_STOCKS
        BUY_RATES = NEWAGE_BUY_RATES

    # ALLOWED_SYMBOLS = MD_ALLOWED_SYMBOLS if portfolio_option == "MD Portfolio" else GOINVESTX_ALLOWED_SYMBOLS

    try:
        summary_data = pd.read_excel(SUMMARY_FILE_PATH, sheet_name="Summary")
        # summary_data = pd.read_csv(SUMMARY_FILE_PATH)
        summary_data.columns = summary_data.columns.astype(str)

        if "DATE1" in summary_data.columns:
            summary_data.drop(columns=["DATE1"], inplace=True)

        dynamic_columns = [col for col in summary_data.columns if "-" in col and col[:4].isdigit()]
        date_mapping = {col: pd.to_datetime(col, errors='coerce').date() for col in dynamic_columns}
        sorted_dynamic_columns = sorted(date_mapping, key=date_mapping.get)

        renamed_columns = {col: date_mapping[col].strftime('%d %b').upper() for col in sorted_dynamic_columns}

        for col in summary_data.columns:
            if col not in ["SYMBOL", "CLOSE", "BUY RATE"]:
                renamed_columns[col] = f"{renamed_columns.get(col, col)} (in %)"

        summary_data.rename(columns=renamed_columns, inplace=True)

        # Ensure all numeric columns are rounded to two decimal places
        numeric_cols = summary_data.select_dtypes(include=['number']).columns
        summary_data[numeric_cols] = summary_data[numeric_cols].round(2)

        if "SYMBOL" not in summary_data.columns or "CLOSE" not in summary_data.columns:
            st.error("The required column SYMBOL or CLOSE is missing in the summary file.")
            return

        summary_data["SYMBOL"] = summary_data["SYMBOL"].fillna("UNKNOWN").astype(str)
        filtered_data = summary_data[summary_data["SYMBOL"].isin(ALLOWED_SYMBOLS)]
        filtered_data.reset_index(drop=True, inplace=True)
        filtered_data.index = filtered_data.index + 1

        filtered_data["BUY RATE"] = filtered_data["SYMBOL"].map(BUY_RATES)
        filtered_data["ROI (in %)"] = ((filtered_data["CLOSE"] - filtered_data["BUY RATE"]) / filtered_data["BUY RATE"]) * 100

        # Ensure ROI is rounded properly
        filtered_data["ROI (in %)"] = filtered_data["ROI (in %)"].round(2)

        column_order = ["SYMBOL", "BUY RATE", "ROI (in %)", "CLOSE"] + \
                       [col for col in filtered_data.columns if col not in ["SYMBOL", "BUY RATE", "ROI (in %)", "CLOSE"]]
        filtered_data = filtered_data[column_order]

        # Apply color formatting to percentage columns
        def color_text(val):
            """Applies color formatting based on the value."""
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

        # Exclude SYMBOL, BUY RATE, and CLOSE from coloring
        color_columns = [col for col in filtered_data.columns if col not in ["SYMBOL", "BUY RATE", "CLOSE"]]

        # Ensure rounding before display
        filtered_data[color_columns] = filtered_data[color_columns].round(2)

        # Apply styles to all percentage columns
        styled_table = filtered_data.style.applymap(color_text, subset=color_columns)

        # Ensure right alignment
        styled_table = styled_table.set_properties(
            subset=[col for col in filtered_data.columns if col not in ["SYMBOL"]],
            **{"text-align": "right"}
        )

        # Display table using st.dataframe()
        st.subheader(f"{portfolio_option} Summary Table")
        st.dataframe(filtered_data.style.format(precision=2), use_container_width=True, height=500)

        # Provide CSV download option
        csv_data = filtered_data.round(2).to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name=f"{portfolio_option.lower().replace(' ', '_')}_summary.csv",
            mime="text/csv",
        )

    except FileNotFoundError:
        st.error(f"Summary file not found at {SUMMARY_FILE_PATH}. Please upload it to the correct location.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
