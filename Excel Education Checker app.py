import pandas as pd
import streamlit as st
import re
from difflib import SequenceMatcher

st.title("İLDAY - Eğitim Kontrol Uygulaması")

# Logo ekleme
try:
    st.image("logo.png", width=150)  # Logonuzun dosya adını veya tam yolunu ekleyin
except Exception as e:
    st.warning("Logo yüklenemedi.")

# Sabit bir Excel dosyasını yükle (Kullanıcı değiştiremeyecek)
EXCEL_FILE = "egitim_listesi.xlsx"  # Dosya adını buraya ekleyin

# Türkçe karakter dönüşümleri ve boşlukları kaldıran bir fonksiyon tanımlayalım
def normalize_text(text):
    replacements = {
        "ı": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c"
    }
    text = text.lower().strip()
    for key, value in replacements.items():
        text = text.replace(key, value)
    text = re.sub(r'\s+', '', text)  # Tüm boşlukları kaldır
    return text

# Benzerlik karşılaştırma fonksiyonu
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

try:
    xl = pd.ExcelFile(EXCEL_FILE)  # Excel dosyasını oku
    st.success("Eğitim verileri yüklendi!")
except FileNotFoundError:
    st.error("Excel dosyası bulunamadı! Lütfen 'egitim_listesi.xlsx' dosyasının mevcut olduğundan emin olun.")
    st.stop()
except Exception as e:
    st.error(f"Excel dosyası yüklenirken hata oluştu: {str(e)}")
    st.stop()

search_term = st.text_input("Aramak istediğiniz eğitimi girin:")

if st.button("Kontrol Et"):
    found_data = {}
    search_term_normalized = normalize_text(search_term)  # Kullanıcının girdisini normalize et
    
    for sheet_name in xl.sheet_names:
        try:
            df = xl.parse(sheet_name)
            df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)  # Tüm hücreleri temizle
            
            for column_name in df.columns:
                df[column_name] = df[column_name].astype(str).str.strip().apply(normalize_text)  # Tüm sütunları normalize et
                
                # Kullanıcının girdisini içeren tüm sonuçları getir
                df['Match Score'] = df[column_name].apply(lambda x: similarity(search_term_normalized, x))
                matches = df[df['Match Score'] > 0.5]  # %50 ve üzeri benzerlik gösterenleri getir
                
                if not matches.empty:
                    if sheet_name not in found_data:
                        found_data[sheet_name] = matches.drop(columns=['Match Score'])
                    else:
                        found_data[sheet_name] = pd.concat([found_data[sheet_name], matches.drop(columns=['Match Score'])])
        except Exception as e:
            st.warning(f"'{sheet_name}' sayfası işlenirken hata oluştu: {str(e)}")
    
    if found_data:
        for sheet, data in found_data.items():
            st.subheader(f'{sheet} Sayfası')
            st.dataframe(data)  # Her sayfanın sonuçlarını ayrı ayrı göster
    else:
        st.error(f'"{search_term}" eğitimi Excel dosyanızda bulunmuyor! ❌')
