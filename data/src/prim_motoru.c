#include <stdio.h>
#include <stdlib.h>

// Müşteri verilerini hafızada düzenli tutmak için Struct (Yapı) kullanıyoruz
struct Musteri {
    int id;
    int yas;
    int arac_yili;
    int kaza[5]; // Son 5 yılın kaza sayılarını tutan dizi
};

int main() {
    // 1. Veri okuma ve yazma için dosyalarımızı açıyoruz
    // Not: Kodu ana dizinden çalıştıracağımız için yol "data/..." şeklinde
    FILE *girdi_dosyasi = fopen("data/musteri_verileri.csv", "r");
    FILE *cikti_dosyasi = fopen("data/hesaplanmis_primler.csv", "w");

    // Dosya okuma kontrolü (Hata yönetimi her zaman artı puandır)
    if (girdi_dosyasi == NULL) {
        printf("Hata: 'data/musteri_verileri.csv' dosyasi bulunamadi!\n");
        return 1;
    }

    // Çıktı dosyasının en üstüne başlık (header) satırını yazdırıyoruz
    fprintf(cikti_dosyasi, "ID,Yas,Toplam_Kaza,Risk_Carpani,Net_Prim\n");

    char satir[200];
    // CSV dosyasındaki ilk satırı (başlıkları) okuyup atlıyoruz ki hesaplamayı bozmasın
    fgets(satir, sizeof(satir), girdi_dosyasi);

    int islenen_musteri = 0;

    // --- DIŞ DÖNGÜ: Dosyadaki tüm müşterileri satır satır tarar ---
    while (fgets(satir, sizeof(satir), girdi_dosyasi) != NULL) {
        struct Musteri m;

        // CSV'den gelen satırı virgüllere göre parçalayıp Struct'ın içine atıyoruz
        sscanf(satir, "%d,%d,%d,%d,%d,%d,%d,%d",
               &m.id, &m.yas, &m.arac_yili,
               &m.kaza[0], &m.kaza[1], &m.kaza[2], &m.kaza[3], &m.kaza[4]);

        // Müşterinin başlangıç parametreleri
        float taban_prim = 10000.0;
        float risk_carpani = 1.0;
        int toplam_kaza = 0;

        // Kural 1: Yaş Faktörü
        if (m.yas < 25) {
            risk_carpani += 0.25; // Genç sürücüye %25 zam
        } else if (m.yas > 65) {
            risk_carpani += 0.15; // Yaşlı sürücüye %15 zam
        }

        // Kural 2: Araç Yaşı Faktörü (2026 yılına göre hesaplıyoruz)
        if ((2026 - m.arac_yili) > 15) {
            risk_carpani += 0.10; // Eski araca %10 zam
        }

        // --- İÇ DÖNGÜ: Müşterinin son 5 yıllık kaza geçmişini tarar ---
        for (int i = 0; i < 5; i++) {
            toplam_kaza += m.kaza[i];
        }

        // Çarpanlara göre ham prim hesaplanıyor
        float net_prim = taban_prim * risk_carpani;

        // Kural 3: Kaza Geçmişine Göre Ödül ve Ceza Sistemi
        if (toplam_kaza == 0) {
            net_prim *= 0.80; // Hiç kaza yapmayana %20 hasarsızlık indirimi
        } else {
            net_prim += (toplam_kaza * 1500.0); // Her 1 kaza için 1500 TL ceza eklentisi
        }

        // Hesaplanmış olan tertemiz veriyi Python'ın okuması için yeni dosyaya kaydediyoruz
        fprintf(cikti_dosyasi, "%d,%d,%d,%.2f,%.2f\n", m.id, m.yas, toplam_kaza, risk_carpani, net_prim);

        islenen_musteri++;
    }

    // Dosyaları kapatarak bellek sızıntısını (memory leak) engelliyoruz
    fclose(girdi_dosyasi);
    fclose(cikti_dosyasi);

    printf("Basariyla %d musteri islendi.\n", islenen_musteri);
    printf("Harika! Sonuclar 'data/hesaplanmis_primler.csv' dosyasina kaydedildi!\n");

    return 0;
}