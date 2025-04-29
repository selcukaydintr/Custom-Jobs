#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Duygu Tabanlı SVG Yüz Sistemi
=============================
Verilen duygu ifadesine göre SVG ile yüz ifadesi oluşturan yapay zeka destekli sistem.
"""

import os
import json
import base64
import random
from typing import Dict, Optional, Tuple, List
import logging

# SVG işleme ve dönüştürme
import svgwrite
import cairosvg
from PIL import Image

# Web arayüzü için
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sabit değerler
SVG_PARTS_DIR = "svg_parts"
CACHE_DIR = "cache"
EMOTION_MAP_FILE = "emotion_to_svg.json"
Q_TABLE_FILE = "q_table.json"
OUTPUT_DIR = "output"

# Temel duygu sözlüğü - Başlangıç için bu eşleştirmeler kullanılacak
DEFAULT_EMOTION_MAP = {
    "mutlu": {"eyes": "eye_01.svg", "mouth": "smile_01.svg", "brows": "normal_01.svg"},
    "üzgün": {"eyes": "eye_02.svg", "mouth": "frown_01.svg", "brows": "sad_01.svg"},
    "sinirli": {"eyes": "eye_03.svg", "mouth": "frown_02.svg", "brows": "angry_01.svg"},
    "şaşkın": {"eyes": "eye_04.svg", "mouth": "oh_01.svg", "brows": "surprised_01.svg"},
    "normal": {"eyes": "eye_01.svg", "mouth": "neutral_01.svg", "brows": "normal_01.svg"}
}

# Q-Learning parametreleri
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 0.2  # Epsilon değeri - rastgele seçim olasılığı


class EmotionSVGSystem:
    """Duygu tabanlı SVG yüz üretim sisteminin ana sınıfı."""
    
    def __init__(self):
        """Sistem için gerekli dizinleri ve dosyaları başlat."""
        self._ensure_directories()
        self.emotion_map = self._load_emotion_map()
        self.q_table = self._load_q_table()
        self.cache = {}
        self._load_cache()
        logger.info("EmotionSVGSystem başlatıldı.")
    
    def _ensure_directories(self) -> None:
        """Gerekli dizinlerin varlığını kontrol et, yoksa oluştur."""
        for directory in [SVG_PARTS_DIR, CACHE_DIR, OUTPUT_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"{directory} dizini oluşturuldu.")
            
            # SVG parts alt dizinleri
            if directory == SVG_PARTS_DIR:
                for subdir in ['eyes', 'mouths', 'brows']:
                    subpath = os.path.join(directory, subdir)
                    if not os.path.exists(subpath):
                        os.makedirs(subpath)
                        logger.info(f"{subpath} alt dizini oluşturuldu.")
    
    def _load_emotion_map(self) -> Dict:
        """Duygu-SVG eşleştirme tablosunu yükle, yoksa varsayılanı kullan."""
        if os.path.exists(EMOTION_MAP_FILE):
            try:
                with open(EMOTION_MAP_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"{EMOTION_MAP_FILE} dosyası hatalı JSON formatında. Varsayılan değerler kullanılıyor.")
                return DEFAULT_EMOTION_MAP
        else:
            # Dosya yoksa varsayılan eşleştirmeyi kaydet ve kullan
            with open(EMOTION_MAP_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_EMOTION_MAP, f, ensure_ascii=False, indent=4)
            logger.info(f"{EMOTION_MAP_FILE} dosyası oluşturuldu.")
            return DEFAULT_EMOTION_MAP
    
    def _load_q_table(self) -> Dict:
        """Q-Learning tablosunu yükle, yoksa boş tablo oluştur."""
        if os.path.exists(Q_TABLE_FILE):
            try:
                with open(Q_TABLE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"{Q_TABLE_FILE} dosyası hatalı JSON formatında. Boş Q-table oluşturuluyor.")
                return {}
        else:
            logger.info(f"{Q_TABLE_FILE} bulunamadı. Boş Q-table oluşturuluyor.")
            return {}
    
    def _save_q_table(self) -> None:
        """Mevcut Q-Learning tablosunu dosyaya kaydet."""
        with open(Q_TABLE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.q_table, f, ensure_ascii=False, indent=4)
        logger.info(f"{Q_TABLE_FILE} dosyasına Q-table kaydedildi.")
    
    def _load_cache(self) -> None:
        """Önbelleğe alınmış SVG'leri yükle."""
        if os.path.exists(CACHE_DIR):
            for filename in os.listdir(CACHE_DIR):
                if filename.endswith('.svg'):
                    emotion = filename.split('.')[0]  # .svg uzantısını kaldır
                    filepath = os.path.join(CACHE_DIR, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.cache[emotion] = f.read()
            logger.info(f"{len(self.cache)} adet SVG önbelleğe yüklendi.")
    
    def get_emotion_components(self, emotion: str) -> Dict:
        """
        Verilen duyguya göre yüz bileşenlerini seç.
        Önce Q-Learning tablosuna bakılır, yoksa statik eşleştirme kullanılır.
        
        Args:
            emotion: Duygu adı (örn. "mutlu", "sinirli")
            
        Returns:
            Seçilen göz, ağız ve kaş bileşenlerini içeren sözlük
        """
        # Q-Learning tablosunda bu duygu için öğrenilmiş bir seçim var mı?
        if emotion in self.q_table and random.random() > EXPLORATION_RATE:
            # Keşif (exploration) yapma, en iyi bilinen seçimi kullan
            components = self._select_best_components(emotion)
            logger.info(f"Q-Learning tablosundan '{emotion}' için bileşenler seçildi.")
            return components
        elif emotion in self.emotion_map:
            # Statik eşleştirmeyi kullan
            logger.info(f"Statik eşleştirme tablosundan '{emotion}' için bileşenler seçildi.")
            return self.emotion_map[emotion]
        else:
            # Bilinmeyen duygu, varsayılan "normal" ifadeyi kullan
            logger.warning(f"Bilinmeyen duygu: '{emotion}'. 'normal' ifadesi kullanılıyor.")
            return self.emotion_map.get("normal", DEFAULT_EMOTION_MAP["normal"])
    
    def _select_best_components(self, emotion: str) -> Dict:
        """Q-Learning tablosundan en yüksek değere sahip bileşenleri seç."""
        q_values = self.q_table[emotion]
        best_components = {}
        
        # Her bileşen tipi için en yüksek puanlı olanı seç
        for component_type in ["eyes", "mouth", "brows"]:
            max_value = -float('inf')
            best_choice = None
            
            for component_name, value in q_values.get(component_type, {}).items():
                if value > max_value:
                    max_value = value
                    best_choice = component_name
            
            # Eğer Q-table'da hiçbir değer yoksa, varsayılan eşleştirmeyi kullan
            if best_choice is None:
                best_choice = DEFAULT_EMOTION_MAP.get(emotion, {}).get(component_type, 
                             DEFAULT_EMOTION_MAP["normal"][component_type])
            
            best_components[component_type] = best_choice
            
        return best_components
    
    def cache_lookup(self, emotion: str) -> Optional[str]:
        """
        Önbellekte belirtilen duygu için SVG var mı kontrol et.
        
        Args:
            emotion: Aranan duygu ifadesi
            
        Returns:
            Bulunan SVG verisi veya None
        """
        return self.cache.get(emotion)
    
    def save_to_cache(self, emotion: str, svg: str) -> None:
        """
        Oluşturulan SVG'yi önbelleğe ve dosyaya kaydet.
        
        Args:
            emotion: Duygu adı
            svg: SVG içeriği
        """
        self.cache[emotion] = svg
        
        # Dosya sistemine de kaydet
        cache_path = os.path.join(CACHE_DIR, f"{emotion}.svg")
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        logger.info(f"'{emotion}' ifadesi önbelleğe ve {cache_path} konumuna kaydedildi.")
    
    def compose_svg(self, parts: Dict) -> str:
        """
        Verilen bileşenlerden SVG oluştur.
        
        Args:
            parts: Göz, ağız ve kaş bileşenlerini içeren sözlük
            
        Returns:
            Birleştirilmiş SVG verisi
        """
        # SVG ölçüleri (face canvas)
        width, height = 240, 240
        
        # Yeni SVG oluştur
        dwg = svgwrite.Drawing(size=(width, height))
        dwg.viewbox(0, 0, width, height)
        
        # Ana yüz konteyneri grubu
        face_group = dwg.add(dwg.g(id='face'))
        
        # Bileşenlerin konum ve ölçeğini ayarla
        components_config = {
            "brows": {"x": 60, "y": 60, "width": 120, "height": 30},
            "eyes": {"x": 60, "y": 100, "width": 120, "height": 40},
            "mouth": {"x": 90, "y": 160, "width": 60, "height": 30}
        }
        
        # Her bileşeni SVG'ye ekle
        for part_type, part_file in parts.items():
            if part_type in components_config:
                config = components_config[part_type]
                
                # SVG alt dizinleri, parts içindeki dosya adlarına göre belirlenir
                # Örneğin: eyes -> svg_parts/eyes/eye_01.svg
                part_path = os.path.join(SVG_PARTS_DIR, f"{part_type}s", part_file)
                
                if os.path.exists(part_path):
                    # SVG'yi yükle
                    with open(part_path, 'r', encoding='utf-8') as f:
                        part_svg = f.read()
                    
                    # SVG element grubunu oluştur
                    part_group = dwg.g(
                        id=f"{part_type}_group",
                        transform=f"translate({config['x']}, {config['y']}) scale({config['width']/100}, {config['height']/100})"
                    )
                    
                    # SVG içeriğine kullanım (use) referansı ekle
                    part_group.add(dwg.use(href=part_path))
                    face_group.add(part_group)
                else:
                    logger.warning(f"Bileşen dosyası bulunamadı: {part_path}")
        
        # SVG string'e dönüştür
        svg_string = dwg.tostring()
        return svg_string
    
    def render_svg_to_png(self, svg_data: str, width: int = 128, height: int = 64, monochrome: bool = True) -> bytes:
        """
        SVG'yi bitmap PNG'ye dönüştür (OLED ekran için)
        
        Args:
            svg_data: SVG içeriği
            width: Çıktı genişliği (varsayılan 128)
            height: Çıktı yüksekliği (varsayılan 64)
            monochrome: Tek renk (monokrom) çıktı için True
            
        Returns:
            PNG verisi (bytes)
        """
        # Önce SVG'yi PNG'ye dönüştür
        png_data = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), 
                                   output_width=width, 
                                   output_height=height)
        
        if monochrome:
            # PNG'yi PIL ile açıp monokrom hale getir
            img = Image.open(BytesIO(png_data))
            mono_img = img.convert('1')  # '1' modu = 1-bit siyah-beyaz
            
            # Monokrom görüntüyü PNG olarak dışa aktar
            output = BytesIO()
            mono_img.save(output, format='PNG')
            png_data = output.getvalue()
        
        return png_data
    
    def learn_emotion_feedback(self, emotion: str, components: Dict, feedback: float) -> None:
        """
        Kullanıcı geri bildirimine göre Q-Learning tablosunu güncelle.
        
        Args:
            emotion: Duygu adı
            components: Kullanılan bileşenler
            feedback: -1 ile 1 arasında başarı puanı (-1: çok kötü, 1: çok iyi)
        """
        # Duygu Q tablosunda yoksa başlat
        if emotion not in self.q_table:
            self.q_table[emotion] = {}
        
        # Her bileşen türü için Q değerlerini güncelle
        for component_type, component_name in components.items():
            # Bileşen türü Q tablosunda yoksa başlat
            if component_type not in self.q_table[emotion]:
                self.q_table[emotion][component_type] = {}
            
            # Seçilen bileşenin mevcut Q değerini al veya 0 olarak başlat
            current_q = self.q_table[emotion][component_type].get(component_name, 0)
            
            # Q değerini güncelle: Q = Q + alpha * (reward - Q)
            # Burada Q-learning güncellemesini basitleştirdik
            new_q = current_q + LEARNING_RATE * (feedback - current_q)
            
            # Yeni Q değerini kaydet
            self.q_table[emotion][component_type][component_name] = new_q
        
        # Güncellenmiş Q tablosunu kaydet
        self._save_q_table()
        logger.info(f"'{emotion}' için Q-Learning tablosu güncellendi. Feedback: {feedback}")
    
    def create_face_for_emotion(self, emotion: str) -> Tuple[str, bytes]:
        """
        Verilen duygu için SVG yüz oluştur ve PNG dönüştür.
        Önbellek kontrolü yapılır.
        
        Args:
            emotion: Duygu adı
            
        Returns:
            (svg_data, png_data) tuple
        """
        # Önce önbellekte ara
        cached_svg = self.cache_lookup(emotion)
        
        if cached_svg:
            logger.info(f"'{emotion}' için önbellekte SVG bulundu.")
            svg_data = cached_svg
        else:
            # Önbellekte yoksa yeni oluştur
            components = self.get_emotion_components(emotion)
            svg_data = self.compose_svg(components)
            self.save_to_cache(emotion, svg_data)
        
        # SVG'yi PNG'ye dönüştür
        png_data = self.render_svg_to_png(svg_data)
        
        return svg_data, png_data
    
    def get_svg_data_url(self, svg_data: str) -> str:
        """
        SVG'yi base64 kodlu data URL'ye dönüştür.
        
        Args:
            svg_data: SVG içeriği
            
        Returns:
            data:image/svg+xml;base64,... formatında URL
        """
        svg_bytes = svg_data.encode('utf-8')
        base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
        return f"data:image/svg+xml;base64,{base64_svg}"


# Flask web uygulaması
app = Flask(__name__)
socketio = SocketIO(app)
svg_system = EmotionSVGSystem()

@app.route('/')
def index():
    """Ana sayfa."""
    return render_template('index.html')

@app.route('/generate_face', methods=['POST'])
def generate_face():
    """Duyguya göre yüz oluştur."""
    data = request.get_json()
    emotion = data.get('emotion', 'normal')
    
    svg_data, png_data = svg_system.create_face_for_emotion(emotion)
    data_url = svg_system.get_svg_data_url(svg_data)
    
    # Base64 PNG data da oluştur
    png_base64 = base64.b64encode(png_data).decode('utf-8')
    
    return jsonify({
        'svg': svg_data,
        'svg_data_url': data_url,
        'png_data_url': f"data:image/png;base64,{png_base64}"
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    """Kullanıcı geri bildirimi al ve öğrenme sistemini güncelle."""
    data = request.get_json()
    emotion = data.get('emotion')
    components = data.get('components')
    feedback_value = data.get('feedback', 0)  # -1 ile 1 arası
    
    if emotion and components and -1 <= feedback_value <= 1:
        svg_system.learn_emotion_feedback(emotion, components, feedback_value)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Geçersiz veri formatı'}), 400

@socketio.on('connect')
def handle_connect():
    """WebSocket bağlantısı kurulduğunda."""
    print('Client connected')

@socketio.on('generate_emotion')
def handle_emotion(data):
    """WebSocket üzerinden duygu işleme."""
    emotion = data.get('emotion', 'normal')
    svg_data, png_data = svg_system.create_face_for_emotion(emotion)
    data_url = svg_system.get_svg_data_url(svg_data)
    
    socketio.emit('face_generated', {
        'emotion': emotion,
        'svg_data_url': data_url
    })

def main():
    """Ana uygulama başlangıcı."""
    # Gerekli dizinleri kontrol et
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    # Basit web arayüzü şablonu oluştur
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Duygu → SVG Yüz Sistemi</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; }
        .face-display { border: 1px solid #ccc; margin: 20px auto; padding: 10px; width: 300px; height: 300px; }
        .controls { margin: 20px 0; }
        input, button, select { padding: 8px; margin: 5px; }
        .feedback { margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Duygu → SVG Yüz Sistemi</h1>
        
        <div class="controls">
            <input type="text" id="emotion-input" placeholder="Duygu yazın (ör: mutlu, sinirli)">
            <button id="generate-btn">Yüz Oluştur</button>
            
            <select id="preset-emotions">
                <option value="">- Hazır Duygular -</option>
                <option value="mutlu">Mutlu</option>
                <option value="üzgün">Üzgün</option>
                <option value="sinirli">Sinirli</option>
                <option value="şaşkın">Şaşkın</option>
                <option value="normal">Normal</option>
            </select>
        </div>
        
        <div class="face-display">
            <img id="face-svg" src="" alt="Duygu Yüzü" style="max-width: 100%; max-height: 100%;">
        </div>
        
        <div class="oled-preview">
            <h3>OLED Önizleme (128x64)</h3>
            <img id="face-png" src="" alt="OLED Görüntüsü" style="border: 1px solid #000; background: #000;">
        </div>
        
        <div class="feedback">
            <h3>Sonucu Değerlendir</h3>
            <button id="good-btn">👍 İyi</button>
            <button id="neutral-btn">😐 Normal</button>
            <button id="bad-btn">👎 Kötü</button>
        </div>
    </div>
    
    <script>
        // Sayfa yüklendiğinde
        document.addEventListener('DOMContentLoaded', function() {
            let currentEmotion = '';
            let currentComponents = {};
            
            // Butonlar ve inputlar
            const generateBtn = document.getElementById('generate-btn');
            const emotionInput = document.getElementById('emotion-input');
            const presetSelect = document.getElementById('preset-emotions');
            const faceSvg = document.getElementById('face-svg');
            const facePng = document.getElementById('face-png');
            const goodBtn = document.getElementById('good-btn');
            const neutralBtn = document.getElementById('neutral-btn');
            const badBtn = document.getElementById('bad-btn');
            
            // Yüz oluşturma fonksiyonu
            function generateFace(emotion) {
                if (!emotion) return;
                
                currentEmotion = emotion;
                
                fetch('/generate_face', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ emotion: emotion })
                })
                .then(response => response.json())
                .then(data => {
                    faceSvg.src = data.svg_data_url;
                    facePng.src = data.png_data_url;
                    currentComponents = data.components || {};
                })
                .catch(error => console.error('Error:', error));
            }
            
            // Geri bildirim gönderme fonksiyonu
            function sendFeedback(value) {
                if (!currentEmotion) return;
                
                fetch('/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        emotion: currentEmotion,
                        components: currentComponents,
                        feedback: value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Geri bildiriminiz için teşekkürler! Sistem öğreniyor.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
            
            // Event Listeners
            generateBtn.addEventListener('click', () => {
                generateFace(emotionInput.value.trim());
            });
            
            presetSelect.addEventListener('change', () => {
                if (presetSelect.value) {
                    emotionInput.value = presetSelect.value;
                    generateFace(presetSelect.value);
                }
            });
            
            // Geri bildirim butonları
            goodBtn.addEventListener('click', () => sendFeedback(1));
            neutralBtn.addEventListener('click', () => sendFeedback(0));
            badBtn.addEventListener('click', () => sendFeedback(-1));
            
            // Başlangıçta normal yüz oluştur
            generateFace('normal');
        });
    </script>
</body>
</html>""")
    
    # Örnek SVG'leri oluştur
    create_example_svgs()
    
    # Web sunucusunu başlat
    print("Web arayüzü http://127.0.0.1:5000 adresinde başlatılıyor...")
    socketio.run(app, host='127.0.0.1', port=5000)


def create_example_svgs():
    """Örnek SVG bileşenlerini oluştur."""
    examples = {
        "eyes": {
            "eye_01.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <circle cx="30" cy="50" r="15" fill="white" stroke="black" stroke-width="2"/>
                <circle cx="70" cy="50" r="15" fill="white" stroke="black" stroke-width="2"/>
                <circle cx="30" cy="50" r="5" fill="black"/>
                <circle cx="70" cy="50" r="5" fill="black"/>
            </svg>""",
            "eye_02.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <path d="M20,50 Q30,60 40,50" stroke="black" stroke-width="2" fill="none"/>
                <path d="M60,50 Q70,60 80,50" stroke="black" stroke-width="2" fill="none"/>
            </svg>""",
            "eye_03.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <ellipse cx="30" cy="50" rx="12" ry="8" fill="white" stroke="black" stroke-width="2"/>
                <ellipse cx="70" cy="50" rx="12" ry="8" fill="white" stroke="black" stroke-width="2"/>
                <circle cx="30" cy="50" r="4" fill="black"/>
                <circle cx="70" cy="50" r="4" fill="black"/>
            </svg>""",
            "eye_04.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <circle cx="30" cy="50" r="15" fill="white" stroke="black" stroke-width="2"/>
                <circle cx="70" cy="50" r="15" fill="white" stroke="black" stroke-width="2"/>
                <circle cx="30" cy="50" r="8" fill="black"/>
                <circle cx="70" cy="50" r="8" fill="black"/>
            </svg>"""
        },
        "mouths": {
            "smile_01.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <path d="M20,50 Q50,80 80,50" stroke="black" stroke-width="2" fill="none"/>
            </svg>""",
            "frown_01.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <path d="M20,80 Q50,50 80,80" stroke="black" stroke-width="2" fill="none"/>
            </svg>""",
            "frown_02.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <path d="M30,70 Q50,60 70,70" stroke="black" stroke-width="2" fill="none"/>
            </svg>""",
            "oh_01.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <circle cx="50" cy="60" r="15" fill="