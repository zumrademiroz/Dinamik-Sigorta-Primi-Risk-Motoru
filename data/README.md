# Dinamik Sigorta Primi Risk ve Maliyet Motoru 🚀

Bu proje, sigorta şirketleri için müşteri verilerini analiz ederek dinamik risk çarpanları ve net prim maliyetleri hesaplayan hibrit (**C & Python**) bir veri bilimi ve aktüerya projesidir.

## 🛠️ Teknolojiler ve Rolleri
* **C Programlama Dili (`src/prim_motoru.c`):** Büyük veri setlerini (CSV) yüksek performansla okur, yaş ve kaza geçmişi kurallarına göre aktüeryal risk çarpanlarını hesaplar ve sonuçları kaydeder.
* **Python (`src/rapor_analiz.py`):** C motorunun ürettiği verileri `pandas` ile analiz eder; `matplotlib` ve `seaborn` kullanarak yönetim raporlama grafiklerini dinamik olarak oluşturur.

## 📂 Klasör Yapısı
```text
├── data/
│   ├── musteri_verileri.csv       # Girdi (Ham Müşteri Verisi)
│   └── hesaplanmis_primler.csv    # C Motorunun Ürettiği Sonuçlar
├── src/
│   ├── prim_motoru.c              # Aktüeryal Hesaplama Motoru (C)
│   └── rapor_analiz.py            # Veri Analizi ve Görselleştirme (Python)
└── README.md                      # Proje Dokümantasyonu (Bu Dosya)