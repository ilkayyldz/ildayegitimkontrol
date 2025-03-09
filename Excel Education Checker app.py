import pandas as pd
import streamlit as st
import re
from difflib import SequenceMatcher
import pdfplumber

st.title("İLDAY - Eğitim Kontrol Uygulaması")

# Logo ekleme
try:
    st.image("logo.png", width=150)  # Logonuzun dosya adını veya tam yolunu ekleyin
except Exception as e:
    st.warning("Logo yüklenemedi.")

# Türkçe karakter dönüşümleri yapan fonksiyon
def normalize_text(text):
    replacements = {
        "ı": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c"
    }
    text = text.lower().strip()
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

# Benzerlik karşılaştırma fonksiyonu
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# PDF'den metin okuma fonksiyonu (pdfplumber ile)
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"PDF dosyası okunurken hata oluştu: {str(e)}")
        st.stop()
    return text

# Sabit 3 PDF dosyası üzerinden arama yapılacak
PDF_FILES = ["egitim_listesi1.pdf", "egitim_listesi2.pdf", "egitim_listesi3.pdf"]

pdf_texts = ""
for pdf_file in PDF_FILES:
    try:
        pdf_texts += extract_text_from_pdf(pdf_file) + "\n"
        st.success(f"{pdf_file} dosyası yüklendi!")
    except FileNotFoundError:
        st.error(f"PDF dosyası bulunamadı: {pdf_file}")
        st.stop()
    except Exception as e:
        st.error(f"PDF dosyası yüklenirken hata oluştu: {str(e)}")
        st.stop()

search_term = st.text_input("Aramak istediğiniz eğitimi girin:")

if st.button("Kontrol Et"):
    found_results = []
    search_term_normalized = normalize_text(search_term)  # Kullanıcının girdisini normalize et
    pdf_texts_normalized = normalize_text(pdf_texts)
    
    # Kullanıcının girdisini içeren tüm sonuçları getir
    if search_term_normalized in pdf_texts_normalized:
        found_results.append(search_term)
    
    if found_results:
        st.success(f'"{search_term}" eğitimi PDF dosyalarınızda bulundu! ✅')
    else:
        st.error(f'"{search_term}" eğitimi PDF dosyalarınızda bulunmuyor! ❌')
