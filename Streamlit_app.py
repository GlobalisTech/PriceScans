import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime, timedelta

# Google Drive File ID
GOOGLE_DRIVE_FILE_ID = "1_R4z5DhZvZlbSVGqwcLUPQ_rlWY9r9bz"  # Replace with your actual file ID

# Function to download file from Google Drive
def download_from_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    with open("Summary.xlsm", "wb") as file:
        file.write(response.content)
    return "Summary.xlsm"

# Download the latest Summary.xlsm
SUMMARY_FILE_PATH = download_from_drive(GOOGLE_DRIVE_FILE_ID)

# Load the file into a DataFrame
summary_data = pd.read_excel(SUMMARY_FILE_PATH, sheet_name="Summary")
# Define allowed symbols for different portfolios
MD_ALLOWED_SYMBOLS = [
    "TARIL", "AIIL", "NETWEB", "GRAVITA", "SKYGOLD", "WEALTH", "WEBELSOLAR", "AWFIS",
    "KAYNES", "POKARNA", "NIBE", "VOLTAMP", "AWHCL", "SHILCTECH", "ANANTRAJ", "POCL",
    "GOLDIAM", "REFEX", "RIR", "TECHNOE", "ECORECO", "CEINSYSTECH", "E2E", "MINID",
    "QUICKHEAL", "SHAKTIPUMP", "WOCKPHARMA", "NEULANDLAB", "SENCO", "VEEFIN", "INA",
    "OLATECH", "ORIANA"
]

GOINVESTX_ALLOWED_SYMBOLS = [
    "ASIANPAINT", "AVANTEL", "NETWEB", "CEINSYSTECH", "E2E", "ELECON", "EPIGRAL", "ETHOSLTD",
    "GESHIP", "GRAUWEIL", "GRAVITA", "INA", "INDIGO", "KAYNES", "CYIENT", "MINID", "NETWEB",
    "NH", "POCL", "POKARNA", "PRECAM", "REFEX", "RIR", "SAGILITY", "SHILCTECH", "SUZLON",
    "TRENT", "VUENOW", "AVANITFEED", "TARIL", "DIXONTECH"
]

# Sample Buy Rates
BUY_RATES = {
    "TARIL": 733.83, "AIIL": 1590.00, "NETWEB": 2779.63, "GRAVITA": 2346.30, "SKYGOLD": 271.77,
    "WEALTH": 1331.86, "WEBELSOLAR": 1378.00, "AWFIS": 732.24, "KAYNES": 5304.66, "POKARNA": 1147.92,
    "NIBE": 1977.25, "VOLTAMP": 10364.00, "AWHCL": 646.53, "SHILCTECH": 6244.00, "ANANTRAJ": 788.03,
    "POCL": 983.78, "GOLDIAM": 398.33, "REFEX": 486.66, "RIR": 3667.91, "TECHNOE": 1549.07,
    "ECORECO": 890.78, "CEINSYSTECH": 1487.43, "E2E": 4069.52, "MINID": 184.48, "QUICKHEAL": 656.82,
    "SHAKTIPUMP": 980.02, "WOCKPHARMA": 1196.21, "NEULANDLAB": 13373.00, "SENCO": 1175.06,
    "VEEFIN": 645.00, "ORIANA": 2267.68, "INA": 419.48, "OLATECH": 432.00
}

def main():
    st.set_page_config(page_title="Stock Portfolio Dashboard", layout="wide")
    st.title("Stock Portfolio Dashboard")

    portfolio_option = st.selectbox(
        "Select Portfolio",
        options=["MD Portfolio", "GOINVESTX Portfolio"],
        index=0,
    )

    ALLOWED_SYMBOLS = MD_ALLOWED_SYMBOLS if portfolio_option == "MD Portfolio" else GOINVESTX_ALLOWED_SYMBOLS

    try:
        summary_data = pd.read_excel(SUMMARY_FILE_PATH, sheet_name="Summary")
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

