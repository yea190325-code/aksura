import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime

# --- Arayüz Ayarları ---
st.set_page_config(page_title="Hızlı Teklif Sistemi", layout="centered")

st.title("🛡️ Zafer Aksu Sigorta - Premium Teklif Şablonu")
st.write("Ekran görüntüsünü yükleyin, yüksek çözünürlüklü ve logolu teklifiniz hazırlansın.")

uploaded_file = st.file_uploader("Ekran Görüntüsünü Yükle (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen Görüntü", use_container_width=True)
    
    if st.button("🚀 Teklif Görselini Üret"):
        with st.spinner("Premium görsel çiziliyor..."):
            
            # --- Örnek Veriler (Yapay zeka bağlandığında buradan dolacak) ---
            ornek_veriler = [
                {"sirket": "RAY SİGORTA", "fiyat": "8.254,55 ₺", "logo_isim": "ray"},
                {"sirket": "ZURICH SİGORTA", "fiyat": "8.449,75 ₺", "logo_isim": "zurich"},
                {"sirket": "NEOVA SİGORTA", "fiyat": "8.471,71 ₺", "logo_isim": "neova"},
                {"sirket": "DOĞA SİGORTA", "fiyat": "8.689,00 ₺", "logo_isim": "doga"},
                {"sirket": "KORU SİGORTA", "fiyat": "9.123,44 ₺", "logo_isim": "koru"}
            ]
            
            # --- Yüksek Çözünürlüklü Çizim (1200x1200) ---
            genislik = 1200
            yukseklik = 1200
            arkaplan = Image.new('RGB', (genislik, yukseklik), color="#F4F6F9")
            cizim = ImageDraw.Draw(arkaplan)
            
            # --- Font Yükleme (arial.ttf GitHub'da Yüklü Olmalı!) ---
            try:
                font_baslik = ImageFont.truetype("arial.ttf", 55)
                font_alt_baslik = ImageFont.truetype("arial.ttf", 35)
                font_metin = ImageFont.truetype("arial.ttf", 40)
                font_kucuk = ImageFont.truetype("arial.ttf", 25)
            except IOError:
                st.error("⚠️ DİKKAT: 'arial.ttf' dosyası bulunamadı! Harfler bozuk çıkabilir. Lütfen arial.ttf dosyasını GitHub'a yükleyin.")
                font_baslik = font_alt_baslik = font_metin = font_kucuk = ImageFont.load_default()

            # --- Üst Kırmızı Bant ---
            cizim.rectangle([(0, 0), (genislik, 200)], fill="#D90429") 
            cizim.text((genislik/2, 70), "ZAFER AKSU SİGORTA", fill="#FFFFFF", font=font_baslik, anchor="mm")
            cizim.text((genislik/2, 140), "KARŞILAŞTIRMALI TRAFİK SİGORTASI TEKLİFLERİ", fill="#EDF2F4", font=font_alt_baslik, anchor="mm")
            
            # --- Beyaz Bilgi Kutusu ---
            cizim.rounded_rectangle([(60, 240), (genislik-60, 360)], radius=20, fill="#FFFFFF", outline="#CED4DA", width=3)
            tarih = datetime.now().strftime("%d.%m.%Y")
            
            cizim.text((90, 270), f"Tarih: {tarih}", fill="#2B2D42", font=font_metin)
            cizim.text((90, 315), "Plaka: 25 ABR 911", fill="#2B2D42", font=font_metin)
            cizim.text((genislik-400, 270), "TC/VKN: 3724*****", fill="#2B2D42", font=font_metin)

            # --- Sütun Başlıkları ---
            cizim.text((220, 420), "SİGORTA ŞİRKETİ", fill="#8D99AE", font=font_alt_baslik)
            cizim.text((genislik-350, 420), "TEKLİF TUTARI", fill="#8D99AE", font=font_alt_baslik)
            cizim.line([(60, 480), (genislik-60, 480)], fill="#CED4DA", width=3)

            # --- Dinamik Logo ve Fiyat Listesi Çizimi ---
            y_koordinati = 520
            for item in ornek_veriler:
                # 1. Logo Ekleme İşlemi
                logo_yolu = f"logolar/{item['logo_isim']}.png"
                if os.path.exists(logo_yolu):
                    try:
                        # Logoyu aç, boyutlandır ve yapıştır
                        logo = Image.open(logo_yolu).convert("RGBA")
                        logo = logo.resize((100, 100)) # Logonun boyutu
                        arkaplan.paste(logo, (90, y_koordinati - 25), logo)
                    except Exception as e:
                        pass # Logo bozuksa atla
                else:
                    # Logo yoksa yuvarlak bir madde işareti koy
                    cizim.ellipse([(130, y_koordinati+10), (145, y_koordinati+25)], fill="#D90429")

                # 2. Şirket Adı (Logonun yanına)
                cizim.text((220, y_koordinati), item['sirket'], fill="#2B2D42", font=font_metin)
                
                # 3. Fiyat (Sağ tarafa)
                cizim.text((genislik-350, y_koordinati), item['fiyat'], fill="#D90429", font=font_metin)
                
                # Çizgi ve boşluk
                y_koordinati += 70
                cizim.line([(60, y_koordinati), (genislik-60, y_koordinati)], fill="#E9ECEF", width=2)
                y_koordinati += 40

            # --- Alt Lacivert Bant ---
            cizim.rectangle([(0, yukseklik-150), (genislik, yukseklik)], fill="#2B2D42")
            cizim.text((genislik/2, yukseklik-100), "www.zaferaksusigorta.com.tr", fill="#FFFFFF", font=font_alt_baslik, anchor="mm")
            cizim.text((genislik/2, yukseklik-45), "Hazırlayan: Yuşa Enes Aksu  |  Erzurum", fill="#8D99AE", font=font_kucuk, anchor="mm")

            # --- Resmi Dışa Aktarma ---
            buf = io.BytesIO()
            arkaplan.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.success("✨ Premium Tasarım Başarıyla Oluşturuldu!")
            st.image(byte_im, caption="WhatsApp'tan Göndermeye Hazır Yüksek Kalite Görsel", use_container_width=True)
            
            st.download_button(
                label="📥 Görseli İndir",
                data=byte_im,
                file_name="zafer_aksu_premium_teklif.png",
                mime="image/png"
            )
