import fitz  
import docx
import pytesseract
import cv2
import spacy
from PIL import Image
import os
from transformers import pipeline
from nltk.tokenize import sent_tokenize
from keybert import KeyBERT
import spacy

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text


# Load NLP models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ----------- Advanced Metadata Generation -----------

def generate_metadata(text):
    # Title (first non-empty line)
    lines = text.strip().split('\n')
    title = next((line.strip() for line in lines if line.strip()), "Untitled Document")

    # Advanced Summary (Transformer-based)
    short_text = text[:1000]  # Truncate to avoid model overload
    try:
        summary_result = summarizer(short_text, max_length=100, min_length=30, do_sample=False)
        summary = summary_result[0]['summary_text']
    except Exception:
        summary = short_text[:300]  # Fallback if model fails

    # Better Keywords (RAKE)
    kw_model = KeyBERT()

    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)

    # Optional: Extract topics via NER (Named Entities)
    doc = nlp(text)
    topics = list(set(ent.label_ for ent in doc.ents))

    return {
        "title": title,
        "summary": summary,
        "keywords": [kw[0] for kw in keywords],
        "topics": topics,
        "word_count": len(text.split())
    }

def process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        text = extract_text_from_image(file_path)
    else:
        return "Unsupported file type"

    metadata = generate_metadata(text)
    return metadata

file_path = r"C:\Users\shash\Downloads\Assignment2.pdf" # Change to your test file
metadata = process_file(file_path)
print(metadata)
