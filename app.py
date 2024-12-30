import streamlit as st
import tempfile
import analyzer
import preprocessor

st.title("Welcome to WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Upload your WhatsApp chat", type="txt")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name  # Get the path of the saved file

    df = preprocessor.preprocess(file_path, '12hr')

    if 'username' in df.columns and not df.empty:

        top_users = df['username'].value_counts().head(10).index
        user_list = top_users.tolist()
        user_list.insert(0, "All")
        selected_user = st.selectbox("Show analysis of", user_list)

        data = analyzer.data_generate(df, top_users)

        if selected_user == "All":
            st.header("📊 WhatsApp Chat Analysis: All Users")
            fig, table1 = analyzer.analyze_all(df, top_users, data)

            for pic in fig:
                pic.set_size_inches(13, 8)
                st.pyplot(pic)
            st.write("Most Used Emoji")
            st.dataframe(table1, use_container_width=True, hide_index=True)

        else:
            st.header(f"📊 WhatsApp Chat Analysis: {selected_user}")

            fig, table1 = analyzer.analyze_user(df, top_users, data, selected_user)
            
            for pic in fig:
                pic.set_size_inches(10, 6)  # Adjust the size (width, height) in inches
                st.pyplot(pic)
            st.write("Most Used Emoji")
            st.dataframe(table1, use_container_width=True, hide_index=True)

            
    else:
        st.write("❌ The uploaded chat data does not contain valid user information.")
