import pandas as pd
import streamlit as st
import re
from difflib import SequenceMatcher
import PyPDF2

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

# PDF'den metin okuma fonksiyonu
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"PDF dosyası okunurken hata oluştu: {str(e)}")
        st.stop()
    return text

# Sabit bir PDF dosyası üzerinden arama yapılacak
PDF_FILE = "egitim_listesi.pdf"  # Dosya adını buraya ekleyin

try:
    pdf_text = extract_text_from_pdf(PDF_FILE)
    st.success("Eğitim verileri yüklendi!")
except FileNotFoundError:
    st.error("PDF dosyası bulunamadı! Lütfen 'egitim_listesi.pdf' dosyasının mevcut olduğundan emin olun.")
    st.stop()
except Exception as e:
    st.error(f"PDF dosyası yüklenirken hata oluştu: {str(e)}")
    st.stop()

search_term = st.text_input("Aramak istediğiniz eğitimi girin:")

if st.button("Kontrol Et"):
    found_results = []
    search_term_normalized = normalize_text(search_term)  # Kullanıcının girdisini normalize et
    pdf_text_normalized = normalize_text(pdf_text)
    
    # Kullanıcının girdisini içeren tüm sonuçları getir
    if search_term_normalized in pdf_text_normalized:
        found_results.append(search_term)
    
    if found_results:
        st.success(f'"{search_term}" eğitimi PDF dosyanızda bulundu! ✅')
    else:
        st.error(f'"{search_term}" eğitimi PDF dosyanızda bulunmuyor! ❌')
