/**
 * ===========================================================
 * # Proje: Çoklu OLED Ekranlı Göz ve Ağız Animasyonu
 * # Dosya: multi_display_control.ino
 * # Açıklama: TCA9548A multiplexer üzerinden 3 OLED ekran kontrolü
 * # Bağımlılıklar: Wire, Adafruit_GFX, Adafruit_SSD1306
 * 
 * # Versiyon: 0.1.0
 * # Değişiklikler:
 * # - [0.1.0] İlk versiyon oluşturuldu
 * #
 * # Yazar: GitHub Copilot
 * # Tarih: 2025-04-27
 * ===========================================================
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Multiplexer I2C adresi
#define TCAADDR 0x70

// OLED ekran parametreleri
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

// Multiplexer kanalları
#define LEFT_EYE_CHANNEL 0
#define RIGHT_EYE_CHANNEL 1
#define MOUTH_CHANNEL 2

// Ekran nesnelerinin tanımlanması
Adafruit_SSD1306 leftEye(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 rightEye(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 mouth(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Göz animasyonu için değişkenler
int ref_eye_height = 40;
int ref_eye_width = 40;
int ref_corner_radius = 10;

// Sol göz değişkenleri
int left_eye_height = ref_eye_height;
int left_eye_width = ref_eye_width;
int left_eye_x = SCREEN_WIDTH / 2;
int left_eye_y = SCREEN_HEIGHT / 2;

// Sağ göz değişkenleri
int right_eye_height = ref_eye_height;
int right_eye_width = ref_eye_width;
int right_eye_x = SCREEN_WIDTH / 2;
int right_eye_y = SCREEN_HEIGHT / 2;

// Ağız değişkenleri
int mouth_width = 80;
int mouth_height = 20;
int mouth_x = SCREEN_WIDTH / 2 - mouth_width / 2;
int mouth_y = SCREEN_HEIGHT / 2 - mouth_height / 2;
int mouth_curve = 0; // Gülümseme eğrisi (-20 üzgün, 0 düz, 20 mutlu)
bool mouth_open = false;

// Animasyon indeksi
int current_animation = 0;
bool demo_mode = true;

// Multiplexer kanalını seçme fonksiyonu
void selectChannel(uint8_t channel) {
  if (channel > 7) return;
  
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

void setup() {
  Wire.begin();
  Serial.begin(115200);
  
  // Sol göz ekranını başlat
  selectChannel(LEFT_EYE_CHANNEL);
  if (!leftEye.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Sol göz ekranı başlatılamadı"));
  }
  leftEye.clearDisplay();
  leftEye.display();
  
  // Sağ göz ekranını başlat
  selectChannel(RIGHT_EYE_CHANNEL);
  if (!rightEye.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Sağ göz ekranı başlatılamadı"));
  }
  rightEye.clearDisplay();
  rightEye.display();
  
  // Ağız ekranını başlat
  selectChannel(MOUTH_CHANNEL);
  if (!mouth.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Ağız ekranı başlatılamadı"));
  }
  mouth.clearDisplay();
  mouth.display();
  
  // Başlangıç mesajları
  selectChannel(LEFT_EYE_CHANNEL);
  leftEye.clearDisplay();
  leftEye.setTextSize(1);
  leftEye.setTextColor(SSD1306_WHITE);
  leftEye.setCursor(0, 0);
  leftEye.println(F("Sol Göz"));
  leftEye.display();
  
  selectChannel(RIGHT_EYE_CHANNEL);
  rightEye.clearDisplay();
  rightEye.setTextSize(1);
  rightEye.setTextColor(SSD1306_WHITE);
  rightEye.setCursor(0, 0);
  rightEye.println(F("Sağ Göz"));
  rightEye.display();
  
  selectChannel(MOUTH_CHANNEL);
  mouth.clearDisplay();
  mouth.setTextSize(1);
  mouth.setTextColor(SSD1306_WHITE);
  mouth.setCursor(0, 0);
  mouth.println(F("Ağız"));
  mouth.display();
  
  delay(2000);
  resetFace();
}

// Gözleri çiz
void drawEyes() {
  // Sol göz
  selectChannel(LEFT_EYE_CHANNEL);
  leftEye.clearDisplay();
  int x = left_eye_x - left_eye_width / 2;
  int y = left_eye_y - left_eye_height / 2;
  leftEye.fillRoundRect(x, y, left_eye_width, left_eye_height, ref_corner_radius, SSD1306_WHITE);
  leftEye.display();
  
  // Sağ göz
  selectChannel(RIGHT_EYE_CHANNEL);
  rightEye.clearDisplay();
  x = right_eye_x - right_eye_width / 2;
  y = right_eye_y - right_eye_height / 2;
  rightEye.fillRoundRect(x, y, right_eye_width, right_eye_height, ref_corner_radius, SSD1306_WHITE);
  rightEye.display();
}

// Ağız çiz
void drawMouth() {
  selectChannel(MOUTH_CHANNEL);
  mouth.clearDisplay();
  
  if (mouth_open) {
    // Açık ağız - elips çiz
    mouth.fillRoundRect(mouth_x, mouth_y, mouth_width, mouth_height, 10, SSD1306_WHITE);
    // İç kısmını siyah yaparak ağız boşluğunu oluştur
    mouth.fillRoundRect(mouth_x + 10, mouth_y + 5, mouth_width - 20, mouth_height - 10, 5, SSD1306_BLACK);
  } else {
    // Kapalı ağız - kavisli çizgi çiz
    for (int i = 0; i < 5; i++) {
      mouth.drawLine(
        mouth_x, mouth_y + mouth_height/2 + mouth_curve,
        mouth_x + mouth_width, mouth_y + mouth_height/2 - mouth_curve,
        SSD1306_WHITE
      );
      mouth_y++; // Çizgiyi kalınlaştır
    }
  }
  
  mouth.display();
}

// Yüzü sıfırla
void resetFace() {
  // Göz parametrelerini sıfırla
  left_eye_height = ref_eye_height;
  left_eye_width = ref_eye_width;
  left_eye_x = SCREEN_WIDTH / 2;
  left_eye_y = SCREEN_HEIGHT / 2;
  
  right_eye_height = ref_eye_height;
  right_eye_width = ref_eye_width;
  right_eye_x = SCREEN_WIDTH / 2;
  right_eye_y = SCREEN_HEIGHT / 2;
  
  // Ağız parametrelerini sıfırla
  mouth_width = 80;
  mouth_height = 20;
  mouth_x = SCREEN_WIDTH / 2 - mouth_width / 2;
  mouth_y = SCREEN_HEIGHT / 2 - mouth_height / 2;
  mouth_curve = 0;
  mouth_open = false;
  
  // Ekranları güncelle
  drawEyes();
  drawMouth();
}

// Göz kırpma animasyonu
void blink(int speed = 10) {
  for (int i = 0; i < 3; i++) {
    left_eye_height -= speed;
    right_eye_height -= speed;
    drawEyes();
    delay(10);
  }
  
  for (int i = 0; i < 3; i++) {
    left_eye_height += speed;
    right_eye_height += speed;
    drawEyes();
    delay(10);
  }
}

// Uyku animasyonu
void sleep() {
  left_eye_height = 2;
  right_eye_height = 2;
  drawEyes();
  
  mouth_curve = -10;
  mouth_open = false;
  drawMouth();
}

// Uyanma animasyonu
void wakeup() {
  sleep();
  
  for (int h = 2; h <= ref_eye_height; h += 2) {
    left_eye_height = h;
    right_eye_height = h;
    drawEyes();
    delay(10);
  }
  
  mouth_curve = 0;
  drawMouth();
}

// Mutlu yüz ifadesi
void happy() {
  resetFace();
  
  // Gözleri mutlu hale getir
  for (int i = 0; i < 10; i++) {
    drawEyes();
    delay(50);
  }
  
  // Ağzı gülümset
  mouth_curve = 15;
  drawMouth();
}

// Konuşma animasyonu
void talk(int duration = 2000) {
  resetFace();
  
  int start_time = millis();
  while (millis() - start_time < duration) {
    mouth_open = !mouth_open;
    drawMouth();
    delay(100 + random(100)); // Rastgele konuşma hızı
  }
  
  mouth_open = false;
  drawMouth();
}

// Animasyon indeksi ile animasyon çalıştır
void runAnimation(int index) {
  switch (index) {
    case 0:
      wakeup();
      break;
    case 1:
      resetFace();
      break;
    case 2:
      blink(10);
      break;
    case 3:
      sleep();
      break;
    case 4:
      happy();
      break;
    case 5:
      talk(2000);
      break;
    case 6:
      // Gözleri sağa çevir
      left_eye_x += 15;
      right_eye_x += 15;
      drawEyes();
      delay(1000);
      resetFace();
      break;
    case 7:
      // Gözleri sola çevir
      left_eye_x -= 15;
      right_eye_x -= 15;
      drawEyes();
      delay(1000);
      resetFace();
      break;
  }
}

void loop() {
  // Demo modu - sırayla animasyonları göster
  if (demo_mode) {
    runAnimation(current_animation);
    current_animation = (current_animation + 1) % 8;
    delay(2000);
  }
  
  // Serial komut kontrolü
  if (Serial.available()) {
    String data = Serial.readString();
    data.trim();
    
    char cmd = data[0];
    if (cmd == 'A') {
      demo_mode = false;
      String arg = data.substring(1);
      int anim = arg.toInt();
      
      Serial.print("Animasyon çalıştırılıyor: ");
      Serial.println(anim);
      
      runAnimation(anim);
      Serial.print(cmd);
      Serial.print(arg);
    } else if (cmd == 'D') {
      demo_mode = true;
      Serial.println("Demo modu açık");
    }
  }
}
