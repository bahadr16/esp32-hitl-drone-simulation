#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from mavros_msgs.srv import SetMode  # MAVROS'un uçuş modu değiştirme servisi

class LandingController(Node):
    def __init__(self):
        super().__init__('landing_controller')
        
        # 1. SUBSCRIBER: ESP32'den gelen verileri dinliyoruz
        self.subscription = self.create_subscription(
            Vector3,
            '/platform_tilt',
            self.tilt_callback,
            10)
            
        # 2. SERVICE CLIENT: ArduPilot'a "Modu Değiştir" emri göndereceğimiz köprü
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        
        # Güvenlik Değişkenleri
        self.landing_triggered = False # Komutu arka arkaya spam'lememek için
        self.stable_counter = 0        # Platformun ne kadar süre dengede kaldığını sayar

        self.get_logger().info("Landing Controller aktif! ESP32 verisi ve uygun açı bekleniyor...")

    def tilt_callback(self, msg):
        # Eğer zaten iniş emri verildiyse verileri dinlemeye devam et ama işlem yapma
        if self.landing_triggered:
            return 

        pitch = msg.x
        roll = msg.y
        
        # ŞART: X(Pitch) ve Y(Roll) açıları -5 ile +5 derece arasında mı?
        if -5.0 <= pitch <= 5.0 and -5.0 <= roll <= 5.0:
            self.stable_counter += 1
            
            # Saniyede 20 veri geliyor. 20 kez üst üste (yaklaşık 1 saniye) dengedeyse:
            if self.stable_counter >= 20:
                self.trigger_landing()
        else:
            # Ufak bir sarsıntıda bile sayaç sıfırlanır, güvenlik her şeydir!
            if self.stable_counter > 0:
                self.get_logger().warning(f"Platform sarsıldı! Açı bozuldu (X:{pitch:.1f}, Y:{roll:.1f}). İniş iptal, sayaç sıfırlandı.")
            self.stable_counter = 0

    def trigger_landing(self):
        self.get_logger().info("GÜVENLİ İNİŞ KOŞULLARI SAĞLANDI! İNİŞ BAŞLATILIYOR (LAND MODU)...")
        self.landing_triggered = True
        
        # MAVROS servisi müsait olana kadar bekle
        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('MAVROS set_mode servisi bekleniyor...')
            
        # İniş talebini (LAND) oluştur ve gönder
        req = SetMode.Request()
        req.custom_mode = "LAND" 
        
        self.future = self.set_mode_client.call_async(req)
        self.future.add_done_callback(self.mode_change_callback)

    def mode_change_callback(self, future):
        try:
            response = future.result()
            if response.mode_sent:
                self.get_logger().info("BAŞARILI: ArduPilot LAND moduna geçti! Drone iniyor...")
            else:
                self.get_logger().error("HATA: ArduPilot iniş modunu reddetti!")
        except Exception as e:
            self.get_logger().error(f"Servis çağrısı başarısız oldu: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = LandingController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()