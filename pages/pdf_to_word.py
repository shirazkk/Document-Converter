import streamlit as st
import tempfile
import os
from pdf2docx import Converter

st.title("PDF to Word Converter")

# Create a file uploader that accepts DOCX files
uploaded_file = st.file_uploader("Upload a PDF file (.pdf)", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.getbuffer())
        tmp_pdf_path = tmp_pdf.name

    # Define a temporary output path for the PDF
    output_pdf_path = tmp_pdf_path.replace(".pdf", ".docx")
    
    try:
        # Convert PDF to Word using pdf2docx
        cv = Converter(tmp_pdf_path)
        cv.convert(output_pdf_path)
        cv.close()
        
        # Read the resulting Word file
        with open(output_pdf_path, "rb") as docx_file:
            docx_bytes = docx_file.read()
        
        # Provide a download button for the Word file
        st.download_button(
            label="Download Converted Word",
            data=docx_bytes,
            file_name=f"{uploaded_file.name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Conversion failed: {e}")
    finally:
        # Clean up temporary files
        os.remove(tmp_pdf_path)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
