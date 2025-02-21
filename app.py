import streamlit as st

st.set_page_config(
    page_title="Document Converter",
    page_icon="📄",
    layout="centered"
)

st.title("Document Converter")
st.markdown("### Welcome to the Document Converter App!")

st.write("""
This application allows you to:
- Convert PDF files to Word documents
- Convert Word documents to PDF files

Please use the sidebar to navigate to the converter you need.
""")

# Add some information about supported formats
with st.expander("Supported Formats"):
    st.write("""
    - **PDF to Word**: Converts PDF (.pdf) files to Word (.docx) format
    - **Word to PDF**: Converts Word (.docx) files to PDF (.pdf) format
    """)

# Add usage instructions
with st.expander("How to Use"):
    st.write("""
    1. Select the desired converter from the sidebar
    2. Upload your file in the supported format
    3. Wait for the conversion to complete
    4. Download your converted file
    """)

# Add a footer
st.markdown("---")
st.markdown("Created by ❤️ Shiraz Ali")
