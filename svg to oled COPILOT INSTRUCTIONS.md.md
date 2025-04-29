Harika, şimdi senin için bu SVG tabanlı, yapay zeka destekli **"duygu → yüz ifadesi üretimi"** sistemini GitHub Copilot ile verimli geliştirebilmek adına bir **markdown formatında talimat dosyası** hazırlayacağım.

---

## 📘 `COPILOT_INSTRUCTIONS.md`

```markdown
# 🤖 Copilot AI Komutları: Duygu Tabanlı SVG Yüz Sistemi

Bu proje, yapay zekâ ile öğrenebilen ve SVG katmanlarıyla yüz ifadeleri üretebilen bir sistemdir.  
Amaç: Duygulara göre göz, ağız ve kaş bileşenlerini seçip vektörel bir yüz oluşturmak, bu yüzü webde göstermek ve küçük OLED ekrana uyarlamaktır.

---

## 🚦 Copilot Kullanım Talimatları

### 💡 Kurallar:
1. **Kodları fonksiyonlara böl.** Her fonksiyon tek görevli olsun.
2. **SVG katmanlarını isimle çağır.** (`eye_01.svg`, `mouth_smile.svg`)
3. **Cache sistemi kullan.** Aynı duygu → aynı yüz olmalı.
4. **Duygu eşlemesini öğrenebilir yap.** İlk başta sabit, sonra Q-Learning.
5. **SVG render sonrasında hem `data:image` hem PNG üret.**

---

## 🧱 Ana Fonksiyon Listesi

| Fonksiyon Adı | Açıklama |
|---------------|----------|
| `get_emotion_components(emotion: str) -> dict` | Göz, ağız, kaş bileşenlerini döndürür. |
| `compose_svg(parts: dict) -> str` | SVG katmanlarını birleştirir. |
| `render_svg_to_png(svg_data: str) -> bytes` | SVG'yi bitmap'e çevirir (OLED için). |
| `cache_lookup(emotion: str) -> Optional[str]` | Cache'te aynı duygu için SVG varsa getirir. |
| `save_to_cache(emotion: str, svg: str)` | Oluşturulan yüz SVG'sini cache'e ekler. |
| `learn_emotion_feedback(emotion: str, result: str)` | Q-learning ile öğrenme tablosunu günceller. |
| `serve_svg_webpanel(svg_data: str)` | Web arayüzde SVG’yi yayınlar. |

---

## 🧠 Öğrenme Sistemi

Başlangıçta `emotion_to_svg.json` dosyası kullanılacaktır.  
Zamanla `q_table.json` oluşur.  
Her duygu girişinde başarı değerlendirmesi alınarak `learn_emotion_feedback()` fonksiyonu ile AI gelişir.

---

## 🖼️ SVG Katman Yapısı

SVG klasörleri:

```
/svg_parts/
  eyes/
    eye_01.svg, eye_02.svg
  mouths/
    smile_01.svg, frown_01.svg
  brows/
    angry_01.svg, sad_01.svg
```

SVG birleştirme mantığı:
```xml
<svg>
  <use href="eyes/eye_03.svg"/>
  <use href="mouths/smile_01.svg"/>
  <use href="brows/angry_01.svg"/>
</svg>
```

---

## 🧪 Test Senaryoları

| Test | Açıklama |
|------|----------|
| `test_angry_face()` | "sinirli" ifadesi → kaş + göz değişmeli |
| `test_smile_reuse()` | Aynı "mutlu" ifadesi cache'ten gelmeli |
| `test_learning()` | Duygu eşleşmesi geri bildirimle iyileşmeli |

---

## 🛠️ Gereken Python Kütüphaneleri

```bash
pip install svgwrite cairosvg pillow flask
```

---

## 🌐 Web Panel Kısmı

SVG çıktısı doğrudan HTML içine gömülür:
```html
<img src="data:image/svg+xml;base64,..." />
```

Canlı WebSocket paneli için Flask tabanlı küçük bir sunucu çalışır.

---

## 💾 OLED İçin Render

SVG'den `128x64 monochrome` bitmap oluşturmak için:
```python
cairosvg.svg2png(url="face.svg", write_to="oled_face.png", output_width=128, output_height=64)
```

`PIL.Image.convert("1")` ile tek renkli hale getirilip luma.oled ile gösterilebilir.

---

## 👨‍🏫 Geliştirici Notları

- Katmanlar birleşmeden önce `scale` ve `position` bilgisi eklenebilir.
- SVG'ler optimize edilmeli (`svgo`, `nano`).
- Gelişmiş öğrenme için `emotion → vector → GAN-SVG` tarzı evrimsel sistem kurulabilir.

---

İstersen bu markdown dosyasını `.md` olarak dışa aktarabilirim.  
Ayrıca bu yapıya uygun bir **starter Python kod paketi** de hazırlamamı ister misin?
