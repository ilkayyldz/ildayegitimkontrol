import pandas as pd
import streamlit as st
import re
from difflib import SequenceMatcher
import fitz  # PyMuPDF

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

# PDF'den metin okuma fonksiyonu (PyMuPDF ile)
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text("text") + "\n"
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
    
    # PDF içeriğini satır bazlı tarayarak kısmi eşleşmeleri bul
    lines = pdf_texts_normalized.split("\n")
    for line in lines:
        if similarity(search_term_normalized, line) > 0.6:  # %60 ve üzeri benzerlik gösterenleri al
            found_results.append(line)
    
    if found_results:
        st.success(f'"{search_term}" eğitimi PDF dosyalarınızda bulundu! ✅')
        for result in found_results:
            st.write(f"➡ {result}")
    else:
        st.error(f'"{search_term}" eğitimi PDF dosyalarınızda bulunmuyor! ❌')
