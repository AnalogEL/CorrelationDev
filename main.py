import streamlit as st
import pandas as pd
import re

# Columns to display in the result
output_columns = ['No.', 'Device', 'Slot ID', 'Serial Number', 'Correlation Unit Device', 'Project Folder', 'Correlation Program', 'Laser Program', 'Machine Type', 'Reference ID', 'Test Status', 'BIN']

def filter_data(df, user_input):
    user_input = user_input.strip().lower()
    print(f"User entered device: {user_input}")

    # First, attempt to match the complete device name
    filtered_df = df[df["Device"].str.lower() == user_input]

    if not filtered_df.empty:
        # Select only the desired columns
        filtered_df = filtered_df[output_columns]
        return filtered_df
    else:
        # Extract numerical part from user input using regular expression
        user_number_match = re.search(r'\d+', user_input)
        user_number = user_number_match.group() if user_number_match else None

        if user_number:
            # Filter rows where the numerical part of "Device" matches the user input
            filtered_df = df[df["Device"].str.extract(r'(\d+)', expand=False).str.lower() == user_number.lower()]

            if not filtered_df.empty:
                # Select only the desired columns
                filtered_df = filtered_df[output_columns]
                return filtered_df

    return None


def main():
    st.image('analogd.png',width = 300)
    st.title('Correlation Device Indicator')

    # Allow users to upload their own CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file.")
        return

    user_input = st.text_input('Enter Device Number:')
    result = filter_data(df, user_input)

    if result is not None:
        st.table(result)
    elif user_input:
        st.warning("Sorry, data not found for the specified device.")
    elif not user_input:
        st.warning("Invalid input. Please enter a numeric value.")

if __name__ == '__main__':
    main()