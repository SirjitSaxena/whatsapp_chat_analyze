import streamlit as st
import tempfile
import analyzer
import preprocessor

# Main Title
st.title("Welcome to WhatsApp Chat Analyzer")

# File uploader at the top
uploaded_file = st.file_uploader("Upload your WhatsApp chat", type="txt")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name  # Get the path of the saved file

    # Pass the file path to your preprocessor function
    df = preprocessor.preprocess(file_path, '12hr')

    # Validate DataFrame structure
    if 'username' in df.columns and not df.empty:

        # User selection at the top
        top_users = df['username'].value_counts().head(10).index
        user_list = top_users.tolist()
        user_list.insert(0, "All")
        selected_user = st.selectbox("Show analysis of", user_list)

        # Generate data
        data = analyzer.data_generate(df, top_users)

        # Analysis section
        if selected_user == "All":
            st.header("📊 WhatsApp Chat Analysis: All Users")

            # Generate figures and emoji tables
            fig, table1 = analyzer.analyze_all(df, top_users, data)

            # Increase figure size
            for pic in fig:
                pic.set_size_inches(10, 6)  # Adjust the size (width, height) in inches
                st.pyplot(pic)

            # Display the dataframe with improved style
            st.dataframe(table1, use_container_width=True, hide_index=True)

        else:
            st.header(f"📊 WhatsApp Chat Analysis: {selected_user}")
            st.subheader(f"Insights for {selected_user}")

            # Generate figures and emoji tables for selected user
            fig, table1 = analyzer.analyze_user(df, top_users, data, selected_user)

            # Increase figure size
            for pic in fig:
                pic.set_size_inches(10, 6)  # Adjust the size (width, height) in inches
                st.pyplot(pic)

            # Display the dataframe with improved style
            st.dataframe(table1, use_container_width=True, hide_index=True)

            # Optionally add a description or summary
            st.markdown(
                f"<div style='font-size:20px;'>Here are the most frequent emojis used by {selected_user} with an enlarged view.</div>",
                unsafe_allow_html=True
            )
    else:
        st.write("❌ The uploaded chat data does not contain valid user information.")
