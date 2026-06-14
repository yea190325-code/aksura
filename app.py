import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

# --- Arayüz Ayarları ---
st.set_page_config(page_title="Hızlı Teklif Sistemi", layout="centered")

st.title("🛡️ Zafer Aksu Sigorta - Otomatik Teklif Şablonu")
st.write("Open Hızlı Teklif ekran görüntüsünü yükleyin, kurumsal teklif görseliniz saniyeler içinde çizilsin.")

# 1. Görüntü Yükleme Alanı
uploaded_file = st.file_uploader("Ekran Görüntüsünü Yükle (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Görüntüyü ekranda göster
    st.image(uploaded_file, caption="Yüklenen Ekran Görüntüsü", use_container_width=True)
    
    if st.button("🚀 Teklif Görselini Üret"):
        with st.spinner("Kurumsal görsel çiziliyor..."):
            
            # ---------------------------------------------------------
            # 2. OCR SİMÜLASYONU (Gelecekte buraya yapay zeka bağlanacak)
            # ---------------------------------------------------------
            ornek_veriler = [
                {"sirket": "RAY SİGORTA", "fiyat": "8.254,55 ₺"},
                {"sirket": "ZURICH SİGORTA", "fiyat": "8.449,75 ₺"},
                {"sirket": "NEOVA SİGORTA", "fiyat": "8.471,71 ₺"},
                {"sirket": "DOĞA SİGORTA", "fiyat": "8.689,00 ₺"},
                {"sirket": "KORU SİGORTA", "fiyat": "9.123,44 ₺"}
            ]
            
            # ---------------------------------------------------------
            # 3. KOD İLE ŞABLON ÇİZİMİ (Sıfırdan Tasarım)
            # ---------------------------------------------------------
            genislik = 800
            yukseklik = 800
            # Açık gri/beyaz, temiz bir arka plan
            arkaplan = Image.new('RGB', (genislik, yukseklik), color="#F8F9FA")
            cizim = ImageDraw.Draw(arkaplan)
            
            # Font Ayarları 
            # (Cloud üzerinde şık durması için Arial yüklemeniz önerilir, yoksa varsayılan çalışır)
            try:
                font_baslik = ImageFont.truetype("arial.ttf", 36)
                font_alt_baslik = ImageFont.truetype("arial.ttf", 22)
                font_metin = ImageFont.truetype("arial.ttf", 26)
                font_kucuk = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                # Arial fontu bulunamazsa hata vermemesi için sistemin varsayılanı devreye girer
                font_baslik = font_alt_baslik = font_metin = font_kucuk = ImageFont.load_default()

            # --- Üst Kurumsal Bant (Kırmızı) ---
            cizim.rectangle([(0, 0), (genislik, 130)], fill="#E63946") 
            cizim.text((genislik/2, 45), "ZAFER AKSU SİGORTA", fill="#FFFFFF", font=font_baslik, anchor="mm")
            cizim.text((genislik/2, 95), "KARŞILAŞTIRMALI TRAFİK SİGORTASI TEKLİFLERİ", fill="#FFFFFF", font=font_alt_baslik, anchor="mm")
            
            # --- Müşteri ve Araç Bilgi Kutusu (Beyaz Kutu) ---
            cizim.rounded_rectangle([(40, 160), (genislik-40, 240)], radius=15, fill="#FFFFFF", outline="#DEE2E6", width=2)
            tarih = datetime.now().strftime("%d.%m.%Y")
            
            cizim.text((60, 180), f"Tarih: {tarih}", fill="#343A40", font=font_metin)
            cizim.text((60, 210), "Plaka: 25 ABR 911", fill="#343A40", font=font_metin)
            cizim.text((genislik-280, 180), "TC/VKN: 3724*****", fill="#343A40", font=font_metin)

            # --- Tablo Sütun Başlıkları ---
            cizim.text((80, 290), "SİGORTA ŞİRKETİ", fill="#6C757D", font=font_alt_baslik)
            cizim.text((genislik-250, 290), "TEKLİF TUTARI", fill="#6C757D", font=font_alt_baslik)
            cizim.line([(40, 330), (genislik-40, 330)], fill="#DEE2E6", width=2)

            # --- Dinamik Fiyat Listesi Çizimi ---
            y_koordinati = 360
            for item in ornek_veriler:
                # Şirket Adı
                cizim.text((80, y_koordinati), f"• {item['sirket']}", fill="#1D3557", font=font_metin)
                # Fiyat
                cizim.text((genislik-250, y_koordinati), item['fiyat'], fill="#E63946", font=font_metin)
                
                # Her satırın arasına çok ince ayıraç çizgisi
                y_koordinati += 45
                cizim.line([(80, y_koordinati), (genislik-80, y_koordinati)], fill="#E9ECEF", width=1)
                y_koordinati += 15

            # --- Alt Kurumsal Bant (Lacivert Footer) ---
            cizim.rectangle([(0, yukseklik-100), (genislik, yukseklik)], fill="#1D3557")
            cizim.text((genislik/2, yukseklik-70), "www.zaferaksusigorta.com.tr", fill="#FFFFFF", font=font_alt_baslik, anchor="mm")
            cizim.text((genislik/2, yukseklik-35), "Hazırlayan: Yuşa Enes Aksu  |  Erzurum", fill="#A8DADC", font=font_kucuk, anchor="mm")

            # ---------------------------------------------------------
            # 4. GÖRSELİ EKRANA BASMA VE İNDİRME
            # ---------------------------------------------------------
            buf = io.BytesIO()
            arkaplan.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.success("Tasarım Başarıyla Oluşturuldu!")
            
            # Görseli Web Sayfasında Göster
            st.image(byte_im, caption="WhatsApp'tan Göndermeye Hazır", use_container_width=True)
            
            # Müşteriye atmak için indirme butonu
            st.download_button(
                label="📥 Görseli İndir",
                data=byte_im,
                file_name="zafer_aksu_teklif.png",
                mime="image/png"
            )