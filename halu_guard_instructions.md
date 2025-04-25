Tabii Selçuk, işte yapay zekaların kod üretiminde oluşabilecek halüsinasyon etkisini tespit ve önleme amacıyla kullanabileceğin **genel bir talimat dosyası** (Markdown formatında). Bu dosyayı `halu_guard_instructions.md` gibi isimlendirebilirsin.

---  
```markdown
# 🎯 AI Kod Üretiminde Halüsinasyon Kontrol Talimatları

Bu belge, yapay zekaların yazdığı kodlarda oluşabilecek halüsinasyon etkilerini tespit etmek, sınırlamak ve ortadan kaldırmak için sistematik kuralları içerir.

---

## 📌 1. Tanım: Halüsinasyon Nedir?

Halüsinasyon, yapay zekanın aşağıdaki şekillerde **uydurma** veya **gerçeklik dışı** içerik üretmesidir:

- Var olmayan fonksiyonlar/sınıflar tanımlaması
- Geçersiz modül veya import kullanması
- Mantıksal veya dilsel açıdan tutarsız kod yazması
- Gereksiz, bağlantısız, ölü veya dummy kod üretmesi

---

## ✅ 2. Tespit Kuralları

### 🔎 Statik Analiz ve Linting

Her üretilen kod otomatik olarak şu analizlerden geçmelidir:

| Dil      | Linter/Analiz Aracı                 |
|----------|--------------------------------------|
| Python   | `flake8`, `pylint`, `mypy`, `bandit` |
| JavaScript | `eslint`, `prettier`                |
| C++      | `cppcheck`, `clang-tidy`             |

- **Kod uyarı skoru ≥ 3** olan dosyalar riskli kabul edilir.
- `mypy` hataları varsa, tip tutarsızlığı potansiyel halüsinasyondur.

---

## 🧪 3. Test Katmanı

Kodlar aşağıdaki şekilde test edilmelidir:

- Her fonksiyon için en az 1 unit test bulunmalı.
- %70 ve üzeri test kapsamı (coverage) zorunludur.
- Dummy test veya yapay assert kullanımı (örnek: `assert True`) yasaktır.

---

## 🔐 4. Gerçeklik Doğrulayıcı Modül

Tüm üretimlerden sonra kod şu kontrol fonksiyonlarından geçirilmelidir:

```python
def is_valid_function(obj, name):
    return hasattr(obj, name) and callable(getattr(obj, name))

def module_exists(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False
```

> ❗ Gerçek dünyada karşılığı olmayan öğeler loglanmalı ve gözden geçirilmelidir.

---

## 📄 5. Şablon ve Arayüz Zorlaması

Kod üretimi aşağıdaki şablonlara zorlanmalıdır:

- Her modül `__version__`, `__author__`, `main()` ve `run(input)` fonksiyonları içermelidir.
- Plugin sistemi varsa, `run()`, `info()`, `config()` fonksiyonları zorunludur.
- Şablon dışı üretim, düşük güvenilirlik olarak işaretlenir.

---

## 🧠 6. AI Farkındalık Geri Bildirimi

Kod üretimi sonrası, AI şu sorulara yanıt vermelidir:

1. Bu kodun hangi kısmından emin değilim?
2. Bu fonksiyon nereye bağlıdır?
3. Gereksiz kod var mı?
4. Hangi satırlar tahmindir?

Yanıtsız kalan bölümler “halüsinasyon şüpheli” olarak loglanmalıdır.

---

## 🔁 7. Çapraz İnceleme

Kod başka bir yapay zekaya aşağıdaki formatta inceletilmelidir:

```
### İnceleme Talebi
Kodun yapısal, mantıksal ve bağlamsal gerçekliğini değerlendir. 
Varsa uydurma, hatalı veya bağlamsız kodları işaretle. 
```

---

## 📂 8. Otomatik Halüsinasyon Raporu

Her üretim sürecinin sonunda `halu_report.md` dosyası oluşturulmalı. Örnek:

```
# Halüsinasyon Raporu - 25.04.2025

- Kod %86 güvenli
- 2 hayali modül tespit edildi: `magicmath`, `superjson`
- 1 fonksiyon bağımsız: `def unicorn_sort()`
- 3 unused import: `os, sys, time`
```

---

## ⚠️ 9. Uygulama Yasakları

Aşağıdaki davranışlar halüsinasyon kapsamına girer ve yasaktır:

- Yorum satırında sahte referans (`# Inspired by NASA API`) kullanmak
- Fonksiyonu açıklayıp, içini boş bırakmak
- Kodun gerçekliğini sorgulamadan direkt entegre etmek

---

## 📌 10. Versiyonlama ve Etiketleme

Halüsinasyon içerme ihtimali yüksek kodlara aşağıdaki etiketler eklenmelidir:

```python
# @halu-risk: HIGH
# @source: AI
# @verified: FALSE
```

---

## 👊 Sonuç

Yapay zeka harika bir yardımcıdır ama her zaman doğruyu söylemez. Bu sistemle kodlarının **güvenilirliğini**, **tutarlılığını** ve **gerçekliğini** garanti altına alırsın.

> "Kod, yazmak değil; doğrulamak sanatıdır."  
> — Bir usta geliştirici

```
---

İstersen bu dosyayı senin sistemine uygun hale getirmek için kişiselleştirebiliriz (örneğin ROS, plugin mimarisi, Python ağırlıklı sistemine entegre formatta).  
Ne dersin, bir versiyon daha yapalım mı senin mimariye özel?
