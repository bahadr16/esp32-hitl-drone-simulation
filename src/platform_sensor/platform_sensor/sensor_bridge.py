#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
from geometry_msgs.msg import Vector3

class SensorBridgeNode(Node):
    def __init__(self):
        super().__init__('sensor_bridge')
        
        # ROS 2 Topic'i oluşturuyoruz. Adı: '/platform_tilt'
        # Vector3 mesaj tipini kullanıyoruz çünkü x(pitch) ve y(roll) açılarını tutmak için mükemmel.
        self.publisher_ = self.create_publisher(Vector3, '/platform_tilt', 10)
        
        # Seri port ayarları (ESP32'nin bağlı olduğu port ve hız)
        self.serial_port = '/dev/ttyUSB0'
        self.baud_rate = 115200
        
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.get_logger().info(f"{self.serial_port} portuna başarıyla bağlanıldı!")
        except Exception as e:
            self.get_logger().error(f"Seri porta bağlanılamadı: {e}")
            return
            
        # Saniyede 20 kez (0.05 saniye) veriyi okuyup ROS 2'ye yayınlayan bir timer (zamanlayıcı) kuruyoruz.
        self.timer = self.create_timer(0.05, self.publish_sensor_data)

    def publish_sensor_data(self):
        if self.ser.in_waiting > 0:
            try:
                # ESP32'den gelen veriyi oku, gereksiz boşlukları sil
                line = self.ser.readline().decode('utf-8').strip()
                
                # Veriyi virgülden ikiye böl ("12.45,-4.32" -> "12.45" ve "-4.32")
                angles = line.split(',')
                
                if len(angles) == 2:
                    msg = Vector3()
                    msg.x = float(angles[0]) # X ekseni (Pitch)
                    msg.y = float(angles[1]) # Y ekseni (Roll)
                    msg.z = 0.0              # Z eksenini (Yaw) kullanmıyoruz
                    
                    self.publisher_.publish(msg)
                    # Konsola yazdır (İsteğe bağlı, verinin geldiğini görmek için)
                    # self.get_logger().info(f'Yayınlanan: Pitch(X): {msg.x}, Roll(Y): {msg.y}')
            except Exception as e:
                self.get_logger().warning(f"Veri okuma/dönüştürme hatası: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SensorBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()