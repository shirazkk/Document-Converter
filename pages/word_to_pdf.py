import streamlit as st
import tempfile
import os
from docx2pdf import convert

st.title("Word to PDF Converter")

# Create a file uploader that accepts DOCX files
uploaded_file = st.file_uploader("Upload a Word file (.docx)", type="docx")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        tmp_docx.write(uploaded_file.getbuffer())
        tmp_docx_path = tmp_docx.name

    # Define a temporary output path for the PDF
    output_pdf_path = tmp_docx_path.replace(".docx", ".pdf")
    
    try:
        # Convert the Word document to PDF using docx2pdf
        convert(tmp_docx_path, output_pdf_path)
        
        # Read the resulting PDF file
        with open(output_pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        # Provide a download button for the PDF
        st.download_button(
            label="Download Converted PDF",
            data=pdf_bytes,
            file_name=f"{uploaded_file.name}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Conversion failed: {e}")
    finally:
        # Clean up temporary files
        os.remove(tmp_docx_path)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
