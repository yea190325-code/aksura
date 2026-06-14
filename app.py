import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime

# --- Arayüz Ayarları ---
st.set_page_config(page_title="Hızlı Teklif Sistemi", layout="centered")

st.title("🛡️ Zafer Aksu Sigorta - Premium Teklif Şablonu")
st.write("Teklif görselinizi özelleştirin ve anında oluşturun.")

# --- Tema Seçenekleri ---
tema_secimi = st.selectbox(
    "Görsel Temasını Seçiniz:",
    ["Klasik Kırmızı", "Kurumsal Mavi", "Premium Siyah", "Zarif Yeşil"]
)

# Tema Renk Sözlüğü
temalar = {
    "Klasik Kırmızı": {"ust_bant": "#D90429", "alt_bant": "#2B2D42", "arkaplan": "#F8F9FA", "metin": "#2B2D42", "fiyat": "#D90429"},
    "Kurumsal Mavi": {"ust_bant": "#1D3557", "alt_bant": "#457B9D", "arkaplan": "#F1FAEE", "metin": "#1D3557", "fiyat": "#E63946"},
    "Premium Siyah": {"ust_bant": "#212529", "alt_bant": "#343A40", "arkaplan": "#F8F9FA", "metin": "#212529", "fiyat": "#FF9F1C"},
    "Zarif Yeşil": {"ust_bant": "#2A9D8F", "alt_bant": "#264653", "arkaplan": "#FAFAFA", "metin": "#264653", "fiyat": "#E76F51"}
}
secilen_renkler = temalar[tema_secimi]

# --- Görüntü Yükleme ---
uploaded_file = st.file_uploader("Ekran Görüntüsünü Yükle (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen Görüntü", use_container_width=True)
    
    if st.button("🚀 Teklif Görselini Üret"):
        with st.spinner("Seçilen temada premium görsel çiziliyor..."):
            
            # --- Örnek Veriler (Tüm şirketleri gösterecek şekilde artırıldı) ---
            ornek_veriler = [
                {"sirket": "RAY SİGORTA", "fiyat": "8.254,55 ₺", "logo_isim": "ray"},
                {"sirket": "ZURICH SİGORTA", "fiyat": "8.449,75 ₺", "logo_isim": "zurich"},
                {"sirket": "NEOVA SİGORTA", "fiyat": "8.471,71 ₺", "logo_isim": "neova"},
                {"sirket": "DOĞA SİGORTA", "fiyat": "8.689,00 ₺", "logo_isim": "doga"},
                {"sirket": "UNICO SİGORTA", "fiyat": "8.689,00 ₺", "logo_isim": "unico"},
                {"sirket": "KORU SİGORTA", "fiyat": "9.123,44 ₺", "logo_isim": "koru"},
                {"sirket": "QUICK SİGORTA", "fiyat": "9.637,99 ₺", "logo_isim": "quick"},
                {"sirket": "CORPUS SİGORTA", "fiyat": "9.837,19 ₺", "logo_isim": "corpus"},
                {"sirket": "BEREKET SİGORTA", "fiyat": "10.690,20 ₺", "logo_isim": "bereket"},
                {"sirket": "TÜRKİYE SİGORTA", "fiyat": "11.722,54 ₺", "logo_isim": "turkiye"},
                {"sirket": "HDI SİGORTA", "fiyat": "12.599,77 ₺", "logo_isim": "hdi"}
            ]
            
            # --- Dinamik Çözünürlük ve Yükseklik Hesabı ---
            genislik = 1200
            # Her şirket için 110 piksel alan ayırıyoruz, böylece hepsi sığıyor
            liste_yuksekligi = len(ornek_veriler) * 110
            yukseklik = 650 + liste_yuksekligi 
            
            arkaplan = Image.new('RGB', (genislik, yukseklik), color=secilen_renkler["arkaplan"])
            cizim = ImageDraw.Draw(arkaplan)
            
            # --- Font Yükleme ---
            try:
                font_baslik = ImageFont.truetype("arial.ttf", 55)
                font_alt_baslik = ImageFont.truetype("arial.ttf", 35)
                font_metin = ImageFont.truetype("arial.ttf", 40)
                font_kucuk = ImageFont.truetype("arial.ttf", 25)
            except IOError:
                st.error("⚠️ 'arial.ttf' bulunamadı! Lütfen GitHub deponuza arial.ttf dosyasını yükleyin.")
                font_baslik = font_alt_baslik = font_metin = font_kucuk = ImageFont.load_default()

            # --- Üst Kurumsal Bant ---
            cizim.rectangle([(0, 0), (genislik, 200)], fill=secilen_renkler["ust_bant"]) 
            cizim.text((genislik/2, 70), "ZAFER AKSU SİGORTA", fill="#FFFFFF", font=font_baslik, anchor="mm")
            cizim.text((genislik/2, 140), "KARŞILAŞTIRMALI TRAFİK SİGORTASI TEKLİFLERİ", fill="#EDF2F4", font=font_alt_baslik, anchor="mm")
            
            # --- Müşteri Bilgi Kutusu ---
            cizim.rounded_rectangle([(60, 240), (genislik-60, 360)], radius=20, fill="#FFFFFF", outline="#CED4DA", width=3)
            tarih = datetime.now().strftime("%d.%m.%Y")
            
            cizim.text((100, 270), f"Tarih: {tarih}", fill="#2B2D42", font=font_metin)
            cizim.text((100, 315), "Plaka: 25 ABR 911", fill="#2B2D42", font=font_metin)
            cizim.text((genislik-400, 270), "TC/VKN: 3724*****", fill="#2B2D42", font=font_metin)

            # --- Tablo Başlıkları ---
            cizim.text((240, 420), "SİGORTA ŞİRKETİ", fill="#8D99AE", font=font_alt_baslik)
            cizim.text((genislik-350, 420), "TEKLİF TUTARI", fill="#8D99AE", font=font_alt_baslik)
            cizim.line([(60, 480), (genislik-60, 480)], fill="#CED4DA", width=4)

            # --- Dinamik Logo ve Fiyat Listesi Çizimi ---
            y_koordinati = 520
            for item in ornek_veriler:
                # 1. Logo Ekleme İşlemi
                logo_yolu = f"logolar/{item['logo_isim']}.png"
                if os.path.exists(logo_yolu):
                    try:
                        logo = Image.open(logo_yolu).convert("RGBA")
                        # Logoyu orantılı küçült
                        logo.thumbnail((100, 100), Image.Resampling.LANCZOS)
                        
                        # Logonun tam ortalanması için offset hesabı
                        logo_w, logo_h = logo.size
                        offset_x = 100 + (100 - logo_w) // 2
                        offset_y = y_koordinati - 20 + (100 - logo_h) // 2
                        
                        arkaplan.paste(logo, (offset_x, offset_y), logo)
                    except Exception as e:
                        pass
                else:
                    # Logo yoksa temaya uygun şık bir nokta koy
                    cizim.ellipse([(140, y_koordinati+15), (155, y_koordinati+30)], fill=secilen_renkler["ust_bant"])

                # 2. Şirket Adı
                cizim.text((240, y_koordinati + 10), item['sirket'], fill=secilen_renkler["metin"], font=font_metin)
                
                # 3. Fiyat
                cizim.text((genislik-350, y_koordinati + 10), item['fiyat'], fill=secilen_renkler["fiyat"], font=font_metin)
                
                # İnce ayıraç çizgisi
                y_koordinati += 110
                cizim.line([(60, y_koordinati-20), (genislik-60, y_koordinati-20)], fill="#E9ECEF", width=2)

            # --- Alt Kurumsal Bant ---
            footer_baslangic = yukseklik - 150
            cizim.rectangle([(0, footer_baslangic), (genislik, yukseklik)], fill=secilen_renkler["alt_bant"])
            cizim.text((genislik/2, footer_baslangic + 50), "www.zaferaksusigorta.com.tr", fill="#FFFFFF", font=font_alt_baslik, anchor="mm")
            cizim.text((genislik/2, footer_baslangic + 105), "Hazırlayan: Yuşa Enes Aksu  |  Erzurum", fill="#E0E1DD", font=font_kucuk, anchor="mm")

            # --- Resmi Dışa Aktarma ---
            buf = io.BytesIO()
            arkaplan.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.success("✨ Tasarım Başarıyla Oluşturuldu!")
            st.image(byte_im, caption=f"Seçilen Tema: {tema_secimi}", use_container_width=True)
            
            st.download_button(
                label="📥 Görseli İndir",
                data=byte_im,
                file_name=f"zafer_aksu_teklif_{tema_secimi.lower().replace(' ', '_')}.png",
                mime="image/png"
            )
