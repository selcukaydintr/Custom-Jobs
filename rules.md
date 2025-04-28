# 4WD Robot Projesi Yol Haritası

## Proje Tanımı

4WD Robot projesi, Raspberry Pi 5 üzerinde çalışan, yapay zeka ve robot kişilik özellikleri ile donatılmış, dört tekerlekli bir robot platformu geliştirmeyi amaçlamaktadır. Robot, modüler bir yazılım mimarisi kullanır ve farklı eklentilerle genişletilebilir şekilde tasarlanmıştır.

## Temel Hedefler

1. **Otonom Hareket**: Robot çevresiyle etkileşime girerek otonom hareket edebilmeli
2. **Nesne Tanıma**: Kamera yardımıyla çevresindeki nesneleri tanıyabilmeli
3. **Engel Algılama**: Ultrasonik sensörlerle engelleri tespit edebilmeli
4. **Kişilik Özellikleri**: "Birey" gibi davranabilmeli, duruma göre kişilik özelliklerini yansıtmalı
5. **Genişletilebilirlik**: Yeni özellikler ve eklentiler kolayca eklenebilmeli

## Teknik Gereksinimler

### Donanım

- Raspberry Pi 5 anakart
- L298N motor sürücü kartı
- 4 adet DC motor ve tekerlekler
- En az 1 adet ultrasonik sensör (HC-SR04)
- Raspberry Pi Kamera veya USB kamera
- MPU6050 IMU sensörü (opsiyonel)
- Güç kaynağı (pil paketi)
- Şasi ve montaj elemanları

### Yazılım

- Python 3.9+
- TensorFlow Lite (AI modelleri için)
- OpenCV (görüntü işleme için)
- YAML (yapılandırma dosyaları için)
- SQLite (bellek sistemi için)

## Sistem Mimarisi

Sistem aşağıdaki temel bileşenlerden oluşur:

1. **Plugin Yöneticisi**: Eklentilerin keşfi ve yönetimi
2. **Model Yöneticisi**: AI modellerinin yönetimi
3. **Kişilik Motoru**: Robotun kişilik ve duygu durumu
4. **Agent Sistemi**: Farklı görevler için agent'ların koordinasyonu
5. **Donanım Arayüzü**: Fiziksel donanımla iletişim
6. **Robot Web Arayüzü**: Kullanıcı etkileşimi için web tabanlı arayüz
7. **Veri Yönetimi**: Robotun deneyimlerini ve öğrenimlerini saklama
8. **Test ve Geliştirme Araçları**: Yazılım geliştirme ve hata ayıklama için araçlar
9. **Geliştirme Ortamı**: Projenin geliştirilmesi için gerekli araçlar ve kütüphaneler
10. **Dokümantasyon**: Projenin nasıl kullanılacağına dair belgeler

## Geliştirme Aşamaları

### Aşama 1: Temel Altyapı (TAMAMLANDI)

- [x] Temel dizin yapısının oluşturulması
- [x] Temel sınıf ve arayüzlerin tanımlanması
- [x] Yapılandırma dosyalarının hazırlanması
- [x] Modüller arası ilişkilerin belirlenmesi

### Aşama 2: Donanım Katmanı

- [ ] Motor kontrolü eklentisinin geliştirilmesi
- [ ] Ultrasonik sensör eklentisinin geliştirilmesi
- [ ] Kamera eklentisinin geliştirilmesi
- [ ] IMU sensör eklentisinin geliştirilmesi
- [ ] Donanım testleri ve kalibrasyonu

### Aşama 3: AI Modelleri

- [ ] Nesne tanıma modelinin uygulanması
- [ ] Engel kaçınma algoritmasının geliştirilmesi
- [ ] Yol planlama algoritmasının geliştirilmesi
- [ ] Model doğrulaması ve performans optimizasyonu

### Aşama 4: Agent Sistemi

- [ ] Temel agent sınıflarının geliştirilmesi
- [ ] Agent yöneticisinin iyileştirilmesi
- [ ] Agent'lar arası iletişim protokolünün test edilmesi
- [ ] Farklı agent'ların uygulanması (sensör, hareket, görüntü işleme)

### Aşama 5: Kişilik Motoru

- [ ] Duygu modelinin geliştirilmesi
- [ ] Karar verme sisteminin uygulanması
- [ ] Deneyim öğrenme sisteminin uygulanması
- [ ] Kişilik özellikleri testleri

### Aşama 6: Entegrasyon ve Test

- [ ] Tüm bileşenlerin entegrasyonu
- [ ] Kapsamlı sistem testleri
- [ ] Performans optimizasyonu
- [ ] Hata giderme ve iyileştirmeler

## Eklenti Geliştirme Kuralları

1. **Yapı**: Her eklenti kendi dizininde bulunmalı ve bir `manifest.yaml` dosyası içermeli
2. **Arayüz Uyumluluğu**: Eklentiler ilgili temel sınıfları uygulamalı
3. **Bağımlılıklar**: Eklenti bağımlılıkları `manifest.yaml` dosyasında belirtilmeli
4. **Hata Yönetimi**: Eklentiler hataları zarif bir şekilde yönetmeli ve sistemi çökertmemeli
5. **Belgelendirme**: Her eklenti, nasıl kullanılacağını açıklayan belgelere sahip olmalı

## Agent Geliştirme Kuralları

1. **Temel Sınıf**: Tüm agent'lar `BaseAgent` sınıfından türetilmeli
2. **Mesajlaşma**: Agent'lar birbirleriyle doğrudan değil, mesajlar üzerinden iletişim kurmalı
3. **Durum Yönetimi**: Agent'lar kendi durumlarını yönetmeli ve raporlamalı
4. **Performans**: Agent'lar performans açısından optimize edilmeli
5. **İş Parçacığı Güvenliği**: Agent'lar çoklu iş parçacığı ortamında güvenli çalışmalı

## Gelecek Özellikler

1. **Ses Tanıma ve Sentezi**: İnsan-robot etkileşimi için konuşma özellikleri
2. **Yüz Tanıma**: Kişileri tanıma ve hatırlama yeteneği
3. **Haritalama**: SLAM algoritmaları ile çevre haritalama
4. **Web Arayüzü**: Yapılandırma ve izleme için web tabanlı arayüz
5. **Uzaktan Kontrol**: Mobil uygulama ile uzaktan kontrol olanağı

## Geliştirme Ortamı Kurulumu

### Python Sanal Ortamı (venv) Talimatları

Robot yazılımı, diğer Python uygulamalarıyla paket çakışmalarını önlemek ve bağımlılıkların izole edilmiş bir ortamda yönetilmesini sağlamak için bir sanal ortamda (virtual environment) çalıştırılmalıdır. Sanal ortam, projeye özgü Python kütüphanelerini ve bağımlılıklarını izole bir şekilde yönetmeyi sağlar.

#### Windows İçin Sanal Ortam Kurulumu

1. **Sanal Ortam Oluşturma**:
   ```cmd
   cd c:\Users\jetre\Desktop\Robot\3\4WD_Robot
   python -m venv venv
   ```

2. **Sanal Ortamı Etkinleştirme**:
   ```cmd
   venv\Scripts\activate
   ```

3. **Bağımlılıkların Yüklenmesi**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Sanal Ortamdan Çıkış**:
   ```cmd
   deactivate
   ```

#### Linux/Raspberry Pi İçin Sanal Ortam Kurulumu

1. **Sanal Ortam Oluşturma**:
   ```bash
   cd ~/4WD_Robot
   python3 -m venv venv
   ```

2. **Sanal Ortamı Etkinleştirme**:
   ```bash
   source venv/bin/activate
   ```

3. **Bağımlılıkların Yüklenmesi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Sanal Ortamdan Çıkış**:
   ```bash
   deactivate
   ```

### Coqui STT Türkçe Model Kurulumu

Robot, konuşma tanıma için Coqui STT (Speech-to-Text) sistemini kullanacaktır. Aşağıdaki adımları izleyerek Türkçe STT modelini kurun:

#### Kurulum Adımları

1. **Bağımlılıkların Yüklenmesi** (sanal ortamda olduğunuzdan emin olun):
   ```bash
   pip install stt
   ```

2. **Türkçe Model İndirme ve Yerleştirme**:
   
   Coqui STT Türkçe modelini indirmek için:
   ```bash
   # Windows
   mkdir -p 4WD_Robot/data/models/stt
   # Türkçe model dosyasını indir ve kopyala
   # Model dosyasını örnek modeller klasöründen kopyalayacağız
   ```

3. **Kullanım Örneği** (Bu kod örneği `model_manager.py` içine entegre edilmelidir):
   ```python
   import stt
   
   def load_stt_model():
       """Türkçe STT modelini yükler"""
       model_path = "data/models/stt/model.tflite"
       
       # Model yükleme
       model = stt.Model(model_path)
       
       return model
   
   def speech_to_text(audio_file_path, model):
       """Ses dosyasını metne çevirir"""
       # Ses dosyasını yükle
       audio = open(audio_file_path, 'rb')
       
       # Sesi metne çevir
       text = model.stt(audio)
       
       return text
   ```

4. **Vosk Model Alternatif Kurulumu**:
   
   Eğer Coqui STT çalışmazsa, alternatif olarak Vosk modelini kullanabilirsiniz:
   ```bash
   pip install vosk
   # Vosk Türkçe modelini örnek modeller klasöründen kopyalayalım
   mkdir -p 4WD_Robot/data/models/vosk
   cp -r "örnek modeller/vosk-model-small-tr-0.3/" 4WD_Robot/data/models/vosk/
   ```

5. **Vosk Kullanım Örneği**:
   ```python
   from vosk import Model, KaldiRecognizer
   import wave
   import json
   
   def vosk_speech_to_text(audio_file_path):
       """Vosk kullanarak sesi metne çevirir"""
       model_path = "data/models/vosk/vosk-model-small-tr-0.3"
       model = Model(model_path)
       
       wf = wave.open(audio_file_path, "rb")
       recognizer = KaldiRecognizer(model, wf.getframerate())
       
       result = ""
       while True:
           data = wf.readframes(4000)
           if len(data) == 0:
               break
           if recognizer.AcceptWaveform(data):
               result_dict = json.loads(recognizer.Result())
               result += result_dict.get("text", "") + " "
       
       final_result_dict = json.loads(recognizer.FinalResult())
       result += final_result_dict.get("text", "")
       
       return result.strip()
   ```

### TensorFlow Lite Kurulumu

Robot yazılımı, TensorFlow Lite kullanarak AI modellerini çalıştıracaktır. Aşağıdaki adımları izleyerek TensorFlow Lite'ı kurun:

1. **Bağımlılıkların Yüklenmesi** (sanal ortamda olduğunuzdan emin olun):
   ```bash
   pip install tflite-runtime
   ```

2. **Model İndirme ve Yerleştirme**:
   
   TensorFlow Lite modelini indirmek için:
   ```bash
   # Windows
   mkdir -p 4WD_Robot/data/models/tflite
   # Model dosyasını indir ve kopyala
   # Model dosyasını örnek modeller klasöründen kopyalayacağız
   ```

3. **Kullanım Örneği** (Bu kod örneği `model_manager.py` içine entegre edilmelidir):
   ```python
   import tflite_runtime.interpreter as tflite
   
   def load_tflite_model():
       """TensorFlow Lite modelini yükler"""
       model_path = "data/models/tflite/model.tflite"
       
       # Model yükleme
       interpreter = tflite.Interpreter(model_path=model_path)
       interpreter.allocate_tensors()
       
       return interpreter
   
   def run_inference(interpreter, input_data):
       """Girdi verisi ile model üzerinde çıkarım yapar"""
       input_details = interpreter.get_input_details()
       output_details = interpreter.get_output_details()
       
       # Girdi verisini ayarla
       interpreter.set_tensor(input_details[0]['index'], input_data)
       
       # Çıkarım yap
       interpreter.invoke()
       
       # Çıktı verisini al
       output_data = interpreter.get_tensor(output_details[0]['index'])
       
       return output_data
   ```

## Katkı Sağlama Rehberi

1. **Kod Standartları**: PEP 8 kod standartlarına uyulmalı
2. **Belgelendirme**: Tüm işlevler ve sınıflar belgelendirilmeli (docstrings)
3. **Testler**: Yeni özellikler için birim testleri yazılmalı
4. **Dallanma Modeli**: Git Flow dallanma modeli kullanılmalı
5. **Gözden Geçirme**: Tüm değişiklikler gözden geçirme sürecinden geçmeli

## Kaynaklar ve Referanslar

- [Raspberry Pi Resmi Dokümanları](https://www.raspberrypi.org/documentation/)
- [TensorFlow Lite Dokümanları](https://www.tensorflow.org/lite)
- [Python Robotik Kaynakları](https://robotics.stackexchange.com/questions/tagged/python)
- [Robot Operating System (ROS) Referansları](https://www.ros.org/)