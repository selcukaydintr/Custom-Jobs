# 3-Yönlü Ultrasonik 2D SLAM Algoritması - Bileşenler Tablosu

## 📚 Gerekli Modüller ve Kütüphaneler

| Modül/Kütüphane | Amaç | Kullanım Detayı | Kurulum |
|-----------------|------|-----------------|---------|
| `numpy` | Matematiksel işlemler, matris hesaplamaları | Harita matrisleri, koordinat dönüşümleri, lineer cebir | `pip install numpy` |
| `matplotlib.pyplot` | Harita görselleştirme, sonuç grafikleri | Occupancy grid, robot yolu, özellik haritası çizimi | `pip install matplotlib` |
| `sklearn.cluster.DBSCAN` | Özellik noktalarını kümeleme | Sensör verilerinden köşe/kenar noktalarını çıkarma | `pip install scikit-learn` |
| `sklearn.neural_network.MLPRegressor` | Sensör verisi iyileştirme | Gürültülü sensör verilerini düzeltme, harita yumuşatma | `pip install scikit-learn` |
| `tensorflow/keras` | Derin öğrenme modelleri | Loop closure tespiti için CNN modeli | `pip install tensorflow` |
| `collections.deque` | Deneyim belleği | Q-Learning için experience replay buffer | Python standart kütüphanesi |
| `random` | Rastgele sayı üretimi | Epsilon-greedy politika, Monte Carlo örnekleme | Python standart kütüphanesi |
| `math` | Temel matematik fonksiyonları | Trigonometrik hesaplamalar, açı dönüşümleri | Python standart kütüphanesi |

## 🏗️ Ana Sınıf Yapısı

### AdvancedUltrasonicSLAM Sınıfı

| Özellik | Tip | Açıklama | Başlangıç Değeri |
|---------|-----|----------|------------------|
| `__init__(map_size, cell_size)` | Constructor | Sınıfı başlatır, tüm değişkenleri initialize eder | - |

## 🗺️ Harita ve Çevre Değişkenleri

| Değişken | Tip | Boyut | Açıklama |
|----------|-----|-------|----------|
| `map_size` | tuple | (100, 100) | Harita boyutu (yükseklik, genişlik) hücre sayısı |
| `cell_size` | float | 0.1 | Her hücrenin gerçek dünyadaki boyutu (metre) |
| `occupancy_grid` | numpy.ndarray | (100, 100) | Olasılıksal occupancy grid haritası (0.0-1.0) |
| `features` | list | - | Feature-based harita: [(x, y, tip), ...] |
| `mass_functions` | numpy.ndarray | (100, 100, 3) | TBM için inanç fonksiyonları [boş, dolu, belirsiz] |

## 🤖 Robot Durum Değişkenleri

| Değişken | Tip | Boyut | Açıklama |
|----------|-----|-------|----------|
| `position` | numpy.ndarray | (2,) | Robot konumu [x, y] |
| `orientation` | float | - | Robot yönelimi (radyan) |
| `path` | list | - | Robot yolu geçmişi |
| `pose_covariance` | numpy.ndarray | (3, 3) | EKF için konum kovaryans matrisi |

## 📡 Sensör Parametreleri

| Değişken | Tip | Değer | Açıklama |
|----------|-----|-------|----------|
| `sensor_range` | int | 50 | Maksimum sensör menzili (hücre sayısı) |
| `sensor_angles` | list | [-π/4, 0, π/4] | 3 sensörün yönelimleri (sol, orta, sağ) |
| `sensor_noise` | float | 0.1 | Sensör gürültü seviyesi (metre) |

## 🎯 Monte Carlo Lokalizasyon

| Değişken | Tip | Boyut | Açıklama |
|----------|-----|-------|----------|
| `num_particles` | int | 100 | Parçacık sayısı |
| `particles` | numpy.ndarray | (100, 3) | Parçacık matrisi [x, y, theta] |

## 🧠 Q-Learning Parametreleri

| Değişken | Tip | Değer/Boyut | Açıklama |
|----------|-----|-------------|----------|
| `q_table` | dict | - | Q-tablosu: {state: {action: q_value}} |
| `learning_rate` | float | 0.1 | Öğrenme oranı |
| `discount_factor` | float | 0.9 | İndirim faktörü |
| `epsilon` | float | 0.1 | Keşif oranı (epsilon-greedy) |
| `possible_actions` | list | 4 element | ['forward', 'turn_left', 'turn_right', 'scan'] |
| `experience_buffer` | deque | maxlen=1000 | Deneyim belleği |

## 🤖 Makine Öğrenmesi Modelleri

| Model | Tip | Yapı | Amaç |
|-------|-----|------|------|
| `sensor_mlp` | MLPRegressor | (64, 32) | Sensör verisi iyileştirme |
| `loop_closure_model` | CNN | Conv2D→Dense | Loop closure tespiti |

## 📊 GraphSLAM Yapısı

| Değişken | Tip | İçerik | Açıklama |
|----------|-----|--------|----------|
| `graph_nodes` | list | [(konum, özellikler), ...] | Graf düğümleri |
| `graph_edges` | list | [(node1, node2, transform), ...] | Graf kenarları |

## 🔧 Ana Fonksiyonlar

### Başlatma ve Kurulum Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `initialize_particles()` | - | None | Monte Carlo parçacıklarını başlatır |
| `initialize_mass_functions()` | - | None | TBM inanç fonksiyonlarını başlatır |
| `build_loop_closure_model()` | - | keras.Model | CNN modelini oluşturur |

### Sensör İşleme Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `get_sensor_readings(real_env=None)` | real_env: array/None | list[float] | 3 sensörden mesafe ölçümleri alır |
| `simulate_sensor_reading(global_angle)` | global_angle: float | float | Haritaya dayalı sensör simülasyonu |

### Harita Güncelleme Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `update_map_with_measurements(measurements)` | measurements: list[float] | None | Ana harita güncelleme fonksiyonu |
| `update_tbm_with_measurements(measurements)` | measurements: list[float] | None | TBM ile harita güncelleme |
| `dempster_combination(m1, m2)` | m1, m2: array | array | Dempster kombinasyon kuralı |

### Özellik İşleme Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `extract_features(measurements)` | measurements: list[float] | list[tuple] | Köşe/kenar özelliklerini çıkarır |
| `update_feature_map(new_features)` | new_features: list[tuple] | None | Feature haritasını günceller |
| `match_features(features1, features2)` | features1,2: list[tuple] | list[tuple] | Özellik eşleştirmesi yapar |

### GraphSLAM Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `update_graph_slam()` | - | None | Graf yapılarını günceller |
| `detect_loop_closure(current_node_idx)` | current_node_idx: int | None | Loop closure tespiti yapar |
| `compute_transform_from_matches(...)` | features1,2, matches | array | Dönüşüm matrisi hesaplar |
| `optimize_graph()` | - | None | Graf optimizasyonu yapar |

### Makine Öğrenmesi Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `enhance_map_with_ml()` | - | None | ML ile harita iyileştirme |

### Q-Learning Fonksiyonları

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `q_learning_step()` | - | None | Q-Learning ile karar verme |
| `get_state()` | - | tuple | Mevcut durumu encode eder |
| `apply_action(action)` | action: str | float | Aksiyonu uygular, reward döner |

### Yardımcı Fonksiyonlar

| Fonksiyon | Parametreler | Dönüş | Açıklama |
|-----------|--------------|-------|----------|
| `get_real_sensor_reading(real_env, angle)` | real_env, angle | float | Gerçek sensör ölçümü |
| `update_particles(measurements)` | measurements: list[float] | None | Parçacık filtresi günceller |
| `resample_particles()` | - | None | Parçacık yeniden örnekleme |
| `ekf_update(measurements)` | measurements: list[float] | None | EKF konum güncelleme |

## 🎛️ Yapılandırma Parametreleri

| Kategori | Parametre | Varsayılan | Açıklama |
|----------|-----------|------------|----------|
| **Harita** | map_size | (100, 100) | Harita boyutu |
| | cell_size | 0.1 | Hücre boyutu (m) |
| **Sensör** | sensor_range | 5.0 | Maksimum menzil (m) |
| | sensor_noise | 0.1 | Gürültü seviyesi |
| **Q-Learning** | learning_rate | 0.1 | Öğrenme hızı |
| | epsilon | 0.1 | Keşif oranı |
| **ML** | hidden_layers | (64, 32) | MLP katman boyutları |
| | max_iter | 1000 | Maksimum iterasyon |
| **Monte Carlo** | num_particles | 100 | Parçacık sayısı |

## 🔄 Ana İşlem Döngüsü

| Adım | Fonksiyon | Açıklama |
|------|-----------|----------|
| 1 | `get_sensor_readings()` | Sensör verilerini al |
| 2 | `update_map_with_measurements()` | Haritaları güncelle |
| 3 | `q_learning_step()` | Sonraki aksiyonu belirle |
| 4 | `enhance_map_with_ml()` | ML ile iyileştir |
| 5 | `detect_loop_closure()` | Loop closure kontrol et |

## 📈 Performans Metrikleri

| Metrik | Hesaplama | Açıklama |
|--------|-----------|----------|
| Harita Doğruluğu | Gerçek vs tahmin | Occupancy grid doğruluğu |
| Konum Hatası | RMSE | Robot konum tahmin hatası |
| Loop Closure Başarım | Precision/Recall | Loop tespit performansı |
| Hesaplama Süresi | ms/iterasyon | Gerçek zamanlılık ölçümü |

## 🔧 Geliştirme Önerileri

| Alan | Öneriler |
|------|----------|
| **Sensör Füzyon** | IMU, enkoder, kamera verilerini entegre et |
| **Hibrit Harita** | Topological + metric harita kombinasyonu |
| **Derin Öğrenme** | Transformer tabanlı sequence modeling |
| **Optimizasyon** | GPU hızlandırma, paralel işleme |
| **Adaptif Parametreler** | Çevreye göre parametre ayarlama |

Bu tablo, 3-yönlü ultrasonik 2D SLAM projesindeki tüm bileşenleri detaylı olarak listelemektedir. Projede kullanılan:

**Ana Bileşenler:**
- 8 ana modül/kütüphane ile matematiksel ve ML işlemler
- 25+ farklı değişken ile harita, robot durumu ve algoritma parametreleri
- 15+ ana fonksiyon ile sensör işleme, harita güncelleme ve karar verme
- Hibrit yaklaşım ile 7 farklı SLAM tekniğinin entegrasyonu

**Öne Çıkan Özellikler:**
- **Multi-modal haritarama**: Grid-based + Feature-based + TBM
- **AI entegrasyonu**: Q-Learning + MLP + CNN
- **Güçlü lokalizasyon**: Monte Carlo + EKF + GraphSLAM
- **Adaptive sistem**: ML ile sürekli iyileştirme

**Geliştirme Potansiyeli:**
- Gerçek zamanlı performans optimizasyonu
- Çok sensörlü füzyon sistemi
- Derin öğrenme ile gelişmiş pattern recognition
- Cloud tabanlı collaborative SLAM

Bu kapsamlı sistem, modern robotik uygulamaları için endüstri standardında bir SLAM çözümü sunmaktadır.