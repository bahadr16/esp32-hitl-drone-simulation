#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
unsigned long timer = 0;

void setup() {
  // Haberleşme hızını yüksek tutuyoruz ki gecikme (latency) olmasın
  Serial.begin(115200); 
  
  // ESP32 için varsayılan I2C pinlerini (SDA:21, SCL:22) başlatır
  Wire.begin(); 

  byte status = mpu.begin();
  Serial.print(F("MPU6050 Durumu: "));
  Serial.println(status);
  
  // Eğer bağlantıda hata varsa (kablo temassızlığı vb.) kodu burada durdur
  while(status != 0){ 
      Serial.println(F("Sensör bulunamadı, kabloları kontrol edin!"));
      delay(1000);
  } 

  Serial.println(F("Kalibrasyon yapılıyor, lütfen sensörü MASADA SABİT TUTUN..."));
  delay(1000);
  
  // Bu fonksiyon sensörün o anki konumunu "0 derece (düz)" olarak kabul eder
  mpu.calcOffsets(); 
  Serial.println(F("Kalibrasyon tamamlandı!\n"));
}

void loop() {
  // Tamamlayıcı filtreyi çalıştırıp açıları hesaplar
  mpu.update(); 

  // ROS 2'ye saniyede 20 defa (50 milisaniyede bir) veri gönderiyoruz
  if((millis() - timer) > 50){ 
    
    // Veriyi virgülle ayrılmış "X_Acisi,Y_Acisi" formatında gönderiyoruz
    // Örnek çıktı: 12.45,-4.32
    Serial.print(mpu.getAngleX());
    Serial.print(",");
    Serial.println(mpu.getAngleY());
    
    timer = millis();
  }
}