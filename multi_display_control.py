"""
===========================================================
# Proje: Çoklu OLED Ekranlı Göz ve Ağız Kontrolü
# Dosya: multi_display_control.py
# Açıklama: 3 OLED ekranlı yüz animasyonlarını kontrol etmek için Python arayüzü
# Bağımlılıklar: pyserial
 
# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] İlk versiyon oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-27
===========================================================
"""

import serial
import time
import argparse

class FaceController:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        """
        Arduino'ya bağlanarak yüz animasyonlarını kontrol eden sınıf
        
        Args:
            port (str): Seri port adı
            baudrate (int): Baud hızı
        """
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Arduino'nun başlaması için bekle
            print(f"Bağlandı: {port}")
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            self.arduino = None
    
    def is_connected(self):
        """Arduino bağlantısının durumunu kontrol et"""
        return self.arduino is not None and self.arduino.isOpen()
    
    def send_animation(self, index):
        """
        Belirtilen animasyon indeksini Arduino'ya gönder
        
        Args:
            index (int): Animasyon indeksi (0-7)
        """
        if not self.is_connected():
            print("Arduino bağlı değil!")
            return False
            
        cmd = f'A{int(index)}'
        cmd_byte = bytes(cmd, 'utf-8')
        print(f"Gönderiliyor: {cmd}")
        self.arduino.write(cmd_byte)
        time.sleep(0.1)
        
        # Geri dönüş yanıtını oku (isteğe bağlı)
        response = self.arduino.readline().decode('utf-8').strip()
        if response:
            print(f"Yanıt: {response}")
        
        return True
    
    def start_demo_mode(self):
        """Demo modunu başlat"""
        if not self.is_connected():
            print("Arduino bağlı değil!")
            return False
            
        cmd = 'D'
        cmd_byte = bytes(cmd, 'utf-8')
        print("Demo modu başlatılıyor")
        self.arduino.write(cmd_byte)
        return True
    
    def run_sequence(self, sequence=None, delay=2.0):
        """
        Belirtilen animasyon sırasını çalıştır
        
        Args:
            sequence (list): Çalıştırılacak animasyon indekslerinin listesi
            delay (float): Animasyonlar arasındaki bekleme süresi
        """
        if sequence is None:
            sequence = [0, 1, 2, 4, 5, 6, 7, 3]  # Varsayılan sıralama
            
        for anim_index in sequence:
            self.send_animation(anim_index)
            time.sleep(delay)
    
    def close(self):
        """Seri bağlantıyı kapat"""
        if self.arduino and self.arduino.isOpen():
            self.arduino.close()
            print("Bağlantı kapatıldı")

def main():
    # Komut satırı argümanlarını ayarla
    parser = argparse.ArgumentParser(description='OLED Yüz Kontrolü')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Arduino seri port')
    parser.add_argument('--baudrate', type=int, default=115200, help='Seri port hızı')
    parser.add_argument('--demo', action='store_true', help='Demo modunu başlat')
    parser.add_argument('--anim', type=int, help='Tek bir animasyon çalıştır (0-7)')
    parser.add_argument('--sequence', action='store_true', help='Tüm animasyonları sırayla çalıştır')
    
    args = parser.parse_args()
    
    # Yüz kontrolcüsünü başlat
    face = FaceController(args.port, args.baudrate)
    
    try:
        if args.demo:
            face.start_demo_mode()
            print("Demo modu aktif. Çıkmak için Ctrl+C")
            while True:
                time.sleep(1)
        
        elif args.anim is not None:
            face.send_animation(args.anim)
            time.sleep(3)  # Animasyonun tamamlanması için bekle
            
        elif args.sequence:
            face.run_sequence()
            
        else:
            print("Animasyon rehberi:")
            print("0: Uyanma")
            print("1: Normal bakış")
            print("2: Göz kırpma")
            print("3: Uyuma")
            print("4: Mutlu ifade")
            print("5: Konuşma")
            print("6: Sağa bakış")
            print("7: Sola bakış")
            print("\nKullanım: python multi_display_control.py --anim 0")
            
    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        face.close()

if __name__ == "__main__":
    main()
