import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io

# Scrubber function to categorize responses
def categorize_response(response):
    if isinstance(response, str):
        if "support" in response or "beneficial" in response:
            return "Support"
        elif "oppose" in response or "detrimental" in response:
            return "Oppose"
        elif "neutral" in response or "fine" in response:
            return "Neutral"
    return "No Response"

# Main function for the app
def main():
    st.title("Feedback Cleaning and Summarization App")
    
    # Step 1: File Upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.write("Original Data", df.head())

        # Step 2: Data Cleaning and Scrubbing
        df_cleaned = df.dropna(how='all').applymap(lambda x: x.lower() if isinstance(x, str) else x)

        # Adjust the feedback columns filter
        feedback_columns = [col for col in df.columns if 'Do you support' in col or 'Section' in col]

        # Apply the scrubber across all relevant feedback columns
        for col in feedback_columns:
            df_cleaned[col + " (Categorized)"] = df_cleaned[col].apply(categorize_response)

        st.write("Cleaned Data", df_cleaned.head())

        # Step 3: Generate Summary
        summary = {}
        for col in df_cleaned.columns:
            if 'Categorized' in col:
                summary[col] = df_cleaned[col].value_counts()

        summary_df = pd.DataFrame(summary).T
        st.write("Summary", summary_df)

        # Step 4: Visuals
        for col in summary_df.index:
            st.write(f"Summary of {col}")
            fig, ax = plt.subplots()
            summary_df.loc[col].plot(kind='bar', ax=ax, color=['gray', 'yellow', 'red', 'green'])
            ax.set_ylabel('Number of Responses')
            st.pyplot(fig)

        # Step 5: Download Cleaned File (In-Memory Buffer)
        cleaned_csv = io.StringIO()
        df_cleaned.to_csv(cleaned_csv, index=False)
        cleaned_csv.seek(0)  # Reset the pointer to the beginning of the file

        st.download_button(
            label="Download Cleaned Data",
            data=cleaned_csv.getvalue(),
            file_name="cleaned_feedback_report.csv",
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
