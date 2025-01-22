import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configure Google Sheets API credentials
def connect_to_google_sheets(sheet_name):
    # Load credentials from Streamlit secrets
    credentials_dict = st.secrets["google_sheets"]
    credentials = Credentials.from_service_account_info(credentials_dict)
    client = gspread.authorize(credentials)
    return client.open(sheet_name).sheet1  # Access the first sheet

# Streamlit App
def main(worksheet):
    st.title("Production Data Entry")

    # Instructions for supervisors
    st.info("""
    **Instructions for Supervisors:**  
    - This form must be completed once the production of a product has been completed.  
    - Ensure all fields are filled out accurately, including the product being run and any issues encountered during production.  
    - **Production Quantity must be entered in pallets.**
    """)

    # Product list
    products = [
        "64oz Family Dollar Lemon Ammonia",
        "64oz True Living Lemon Ammonia RP2555",
        "64oz True Living Cleaning Vinegar RP2555",
        "33oz True Living Lavender MPC",
        "24oz True Living Pine MPC RP2106",
        "56oz Terriffic! Pine",
        "56oz Terriffic! Lavender",
        "40oz Sun-Pine Window Spray Bonus RP2520",
        "40oz Sun-Pine Cleaner with Bleach/Peroxide Bonus",
        "56oz Sun-Pine Lavender Floor Cleaner RP2290",
        "32oz CVS Drain Opener",
        "32oz Mr. Plumber Drain Opener",
        "32oz Red Cleaning Vinegar RP2325",
        "32oz Red Value Window Cleaner",
        "32oz Solutions Pink AllPurpose",
        "56oz Red Cleaning Vinegar Original",
        "32oz Tile Plus 4 in 1",
        "64oz Maxx Bubbles",
        "128oz Maxx Bubbles"
    ]

    # Input form
    with st.form("data_entry_form"):
        # Dropdown for product selection
        product = st.selectbox("Select Product", products)
        
        # Other fields
        date = st.date_input("Date")
        production_line = st.selectbox("Production Line", ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5", "Line 6", "Line 7", "Line 8", "Line 9"])
        production_quantity = st.number_input("Production Quantity (in pallets)", min_value=0, step=1)
        issues = st.text_area("Issues (if any)")
        
        # Submit button
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Save data to Google Sheets
            data = [str(date), production_line, product, production_quantity, issues]
            try:
                worksheet.append_row(data)
                st.success("Data submitted successfully!")
            except Exception as e:
                st.error(f"Failed to submit data: {e}")
    
    # Display data preview
    if st.checkbox("Show Existing Data"):
        try:
            data = worksheet.get_all_values()
            df = pd.DataFrame(data[1:], columns=data[0])  # Assuming the first row has headers
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to load data: {e}")

if __name__ == "__main__":
    # Replace 'Your Actual Sheet Name' with the name of your Google Sheet
    sheet_name = "Production"
    worksheet = connect_to_google_sheets(sheet_name)
    main(worksheet)
