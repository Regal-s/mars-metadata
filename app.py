import streamlit as st
from metadata_generator import process_file
import os

# App title
st.set_page_config(page_title="Metadata Extractor", layout="centered")
st.title("📄 PDF Metadata Extractor")

# Upload section
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# File handling
if uploaded_file is not None:
    with st.spinner("Processing..."):
        # Save uploaded file temporarily
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Process file using metadata generator
        try:
            metadata = process_file(file_path)
            if isinstance(metadata, dict):
                st.success("Metadata successfully extracted!")

                # Display results
                st.subheader("📌 Title")
                st.write(metadata.get("title", "N/A"))

                st.subheader("📝 Summary")
                st.write(metadata.get("summary", "N/A"))

                st.subheader("🔑 Keywords")
                st.write(", ".join(metadata.get("keywords", [])))

                st.subheader("🧠 Named Entities")
                st.write(", ".join(metadata.get("topics", [])))

                st.subheader("🔢 Word Count")
                st.write(metadata.get("word_count", 0))
            else:
                st.error("Metadata extraction failed. Unexpected output format.")
        except Exception as e:
            st.error(f"Error processing file: {e}")

        # Clean up temp file
        os.remove(file_path)





