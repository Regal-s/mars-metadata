# Mars Metadata Extractor

A simple Streamlit web application that extracts **metadata** from PDF files, such as:
- Title
- Summary
- Keywords
- Named Entities (NER)
- Word count

---

## Features

- Upload any `.pdf` file
- Auto-generates metadata using NLP techniques
- Extracts keywords using RAKE
- Displays word count and named entities using spaCy
- Runs entirely in your browser via Streamlit


## Tech Stack

-  Python
-  Libraries: `PyMuPDF`, `RAKE-NLTK`, `spaCy`, `Streamlit`
-  Deployed via [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## Installation (For Local Development)

```bash
# Clone the repository
git clone https://github.com/Regal-s/mars-metadata.git
cd mars-metadata

# Create virtual environment (optional but recommended)
python -m venv mars
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
