import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. C Motorunun Ürettiği Hesaplanmış Veriyi Okuyoruz
try:
   df= pd.read_csv(r"C:\Users\zmrde\PycharmProjects\PythonProject\.venv\data\hesaplanmis_primler.csv")
except FileNotFoundError:
    print("Hata: 'data/hesaplanmis_primler.csv' bulunamadı. Lütfen C kodunu çalıştırdığınızdan emin olun.")
    exit()

# 2. Şirket Yönetimi İçin Temel İstatistiksel Özetleri Hesaplama
print("==================================================")
print("     AKTÜERYAL RİSK VE PRİM ANALİZİ RAPORU       ")
print("==================================================")

toplam_musteri = len(df)
toplam_prim_geliri = df['Net_Prim'].sum()
ortalama_prim = df['Net_Prim'].mean()
en_yuksek_prim = df['Net_Prim'].max()
en_dusuk_prim = df['Net_Prim'].min()

print(f"► Toplam Analiz Edilen Sürücü Sayısı : {toplam_musteri}")
print(f"► Şirketin Toplam Prim Geliri Hedefi : {toplam_prim_geliri:,.2f} TL")
print(f"► Sürücü Başına Ortalama Prim Tutarı : {ortalama_prim:,.2f} TL")
print(f"► En Yüksek Riskli Poliçe Tutarı     : {en_yuksek_prim:,.2f} TL")
print(f"► En Güvenli (En Düşük) Poliçe Tutarı: {en_dusuk_prim:,.2f} TL")
print("==================================================\n")

# 3. GRAFİKSEL GÖRSELLEŞTİRME AŞAMASI
# Grafiklerin şık görünmesi için seaborn temasını aktif ediyoruz
sns.set_theme(style="whitegrid")

# İki grafiği yan yana tek bir pencerede göstermek için 1 satır 2 sütunluk alan açıyoruz
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# --- BİRİNCİ GRAFİK: Yaş Gruplarına Göre Ortalama Prim Dağılımı (Sütun Grafiği) ---
# Sürücüleri yaşlarına göre kategorize ediyoruz
df['Yas_Grubu'] = pd.cut(df['Yas'], bins=[0, 25, 65, 100], labels=['Genç Sürücü (<25)', 'Standart Sürücü (25-65)', 'Kıdemli Sürücü (>65)'])
yas_ozet = df.groupby('Yas_Grubu', observed=False)['Net_Prim'].mean().reset_index()

sns.barplot(x='Yas_Grubu', y='Net_Prim', data=yas_ozet, ax=axes[0], palette='Blues_r')
axes[0].set_title('Yaş Gruplarına Göre Ortalama Sigorta Primi', fontsize=14, fontweight='bold', pad=15)
axes[0].set_xlabel('Sürücü Yaş Kategorisi', fontsize=12)
axes[0].set_ylabel('Ortalama Prim (TL)', fontsize=12)

# Sütunların üzerine net TL değerlerini yazdırma otomasyonu
for p in axes[0].patches:
    axes[0].annotate(f"{p.get_height():,.0f} TL", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontweight='bold')

# --- İKİNCİ GRAFİK: Sürücülerin Hasarsızlık Durumu Dağılımı (Pasta Grafiği) ---
# Toplam kazası 0 olanlar "Hasarsız", diğerleri "Hasarlı/Riskli"
df['Durum'] = df['Toplam_Kaza'].apply(lambda x: 'Hasarsız Sürücü (%20 İndirimli)' if x == 0 else f'{x} Kazalı Sürücü (Cezalı)')
durum_sayilari = df['Durum'].value_counts()

axes[1].pie(durum_sayilari, labels=durum_sayilari.index, autopct='%1.1f%%', startangle=140,
        colors=['#2ecc71', '#e74c3c', '#e67e22', '#3498db'], textprops={'fontweight': 'bold'})
axes[1].set_title('Müşteri Portföyü Kaza Dağılım Oranları', fontsize=14, fontweight='bold', pad=15)

# Grafiklerin birbirine girmemesi için yerleşimi sıkıştırıyoruz
plt.tight_layout()

# Grafik penceresini ekrana basıyoruz
print("Grafikler başarıyla oluşturuldu. Ekran açılıyor...")
plt.show()