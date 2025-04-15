from machine import Pin, I2C, Timer
import time
import math
import framebuf
import random

# SSD1306 Kütüphanesi (Başlangıç)
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            SET_MEM_ADDR, 0x00, # horizontal
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xff,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)

    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)

    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)
        
    def ellipse(self, x0, y0, a, b, col, fill=False):
        """Elips çizme fonksiyonu"""
        x1 = 0
        y1 = b
        
        # Başlangıç değerleri
        a2 = a * a
        b2 = b * b
        
        # İlk bölge için karar parametresi
        p1 = b2 - (a2 * b) + (0.25 * a2)
        dx = 2 * b2 * x1
        dy = 2 * a2 * y1
        
        # İlk bölge için çizim
        while dx < dy:
            if fill:
                self.hline(x0 - x1, y0 - y1, 2 * x1 + 1, col)
                self.hline(x0 - x1, y0 + y1, 2 * x1 + 1, col)
            else:
                self.pixel(x0 + x1, y0 + y1, col)
                self.pixel(x0 - x1, y0 + y1, col)
                self.pixel(x0 + x1, y0 - y1, col)
                self.pixel(x0 - x1, y0 - y1, col)
            
            # Bir sonraki nokta
            if p1 < 0:
                x1 += 1
                dx += 2 * b2
                p1 += dx + b2
            else:
                x1 += 1
                y1 -= 1
                dx += 2 * b2
                dy -= 2 * a2
                p1 += dx - dy + b2
        
        # İkinci bölge için karar parametresi
        p2 = (b2 * (x1 + 0.5) * (x1 + 0.5)) + (a2 * (y1 - 1) * (y1 - 1)) - (a2 * b2)
        
        # İkinci bölge için çizim
        while y1 >= 0:
            if fill:
                self.hline(x0 - x1, y0 - y1, 2 * x1 + 1, col)
                self.hline(x0 - x1, y0 + y1, 2 * x1 + 1, col)
            else:
                self.pixel(x0 + x1, y0 + y1, col)
                self.pixel(x0 - x1, y0 + y1, col)
                self.pixel(x0 + x1, y0 - y1, col)
                self.pixel(x0 - x1, y0 - y1, col)
            
            # Bir sonraki nokta
            if p2 > 0:
                y1 -= 1
                dy -= 2 * a2
                p2 += a2 - dy
            else:
                y1 -= 1
                x1 += 1
                dx += 2 * b2
                dy -= 2 * a2
                p2 += dx - dy + a2

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass
# SSD1306 Kütüphanesi (Son)

class RobotFace:
    """Robot yüzü sınıfı - OLED ekranlar için yüz ifadelerini yönetir"""
    
    # İfade türleri
    EXPRESSIONS = [
        'normal', 'happy', 'angry', 'sad', 'surprised', 
        'sleepy', 'confused', 'excited', 'wink', 'thinking'
    ]
    
    def __init__(self, i2c_pins=(22, 21)):
        """Robot yüzünü başlat"""
        self.i2c = I2C(0, scl=Pin(i2c_pins[0]), sda=Pin(i2c_pins[1]))
        self.oleds = []
        self.initialize_displays()
        
        # İfade durumu
        self.current_expression = 'normal'
        self.blinking = False
        self.blink_timer = Timer(-1)
        self.animation_timer = Timer(-1)
        
        # Rastgele davranış için durum değişkenleri
        self.last_random_action = time.time()
        self.random_action_interval = random.uniform(3, 8)
        
        # Göz pozisyonları
        self.left_eye_pos = [0, 0]  # [x_offset, y_offset]
        self.right_eye_pos = [0, 0]
        
        # Başlangıç durumu
        self.set_expression('normal')
        self.setup_random_behavior()
    
    def initialize_displays(self):
        """OLED ekranları başlat"""
        # I2C adreslerini tara
        devices = self.i2c.scan()
        print("Bulunan I2C adresleri:", [hex(addr) for addr in devices])
        
        if len(devices) < 3:
            raise RuntimeError("En az 3 OLED bağlı olmalıdır! Bulunan: {}".format(len(devices)))
        
        # İlk 3 cihazı kullan
        oled_addresses = devices[:3]
        
        # OLED'leri başlat
        for i, addr in enumerate(oled_addresses):
            try:
                oled = SSD1306_I2C(128, 64, self.i2c, addr)
                oled.fill(0)
                oled.text("OLED {}".format(i+1), 0, 0, 1)
                oled.show()
                self.oleds.append(oled)
                print(f"OLED başlatıldı (Adres: 0x{addr:02X})")
                time.sleep(0.5)
            except Exception as e:
                print(f"Adres 0x{addr:02X} için OLED başlatılamadı: {e}")
        
        if len(self.oleds) < 3:
            raise RuntimeError("Tüm OLED'ler başlatılamadı!")
        
        time.sleep(1)
        for oled in self.oleds:
            oled.fill(0)
            oled.show()
    
    def draw_eye(self, oled, state, is_left=True, x_offset=0, y_offset=0):
        """Göz çizimi"""
        oled.fill(0)
        base_offset = -10 if is_left else 10
        
        # x_offset ve y_offset göz hareketini kontrol eder
        x_offset = max(-10, min(10, x_offset))
        y_offset = max(-10, min(10, y_offset))
        
        if state == 'normal':
            oled.fill_rect(30 + x_offset, 20 + y_offset, 40, 30, 1)
            oled.fill_rect(45 + base_offset + x_offset, 30 + y_offset, 10, 10, 0)
        elif state == 'happy':
            oled.fill_rect(35 + base_offset + x_offset, 25 + y_offset, 30, 20, 1)
            oled.fill_rect(35 + base_offset + x_offset, 30 + y_offset, 30, 5, 0)
        elif state == 'angry':
            oled.hline(30 + x_offset, 20 + y_offset, 40, 1)
            oled.fill_rect(30 + x_offset, 30 + y_offset, 40, 10, 1)
            # Kaş çizimi
            oled.line(30 + x_offset, 15 + y_offset, 45 + x_offset, 5 + y_offset, 1)
            oled.line(70 + x_offset, 15 + y_offset, 55 + x_offset, 5 + y_offset, 1)
        elif state == 'sad':
            oled.fill_rect(30 + x_offset, 25 + y_offset, 40, 20, 1)
            oled.fill_rect(45 + base_offset + x_offset, 30 + y_offset, 10, 10, 0)
            # Üzgün kaş çizimi
            oled.line(30 + x_offset, 5 + y_offset, 45 + x_offset, 15 + y_offset, 1)
            oled.line(70 + x_offset, 5 + y_offset, 55 + x_offset, 15 + y_offset, 1)
        elif state == 'surprised':
            oled.ellipse(50 + x_offset, 30 + y_offset, 20, 20, 1, True)
            oled.ellipse(50 + x_offset, 30 + y_offset, 12, 12, 0, True)
        elif state == 'sleepy':
            oled.fill_rect(30 + x_offset, 30 + y_offset, 40, 15, 1)
            oled.hline(30 + x_offset, 30 + y_offset, 40, 1)
        elif state == 'confused':
            oled.fill_rect(30 + x_offset, 20 + y_offset, 40, 30, 1)
            oled.fill_rect(45 + base_offset + x_offset, 30 + y_offset, 10, 10, 0)
            # Şaşkın kaş çizimi (tek taraf)
            if is_left:
                oled.line(30 + x_offset, 10 + y_offset, 45 + x_offset, 15 + y_offset, 1)
            else:
                oled.line(70 + x_offset, 10 + y_offset, 55 + x_offset, 15 + y_offset, 1)
        elif state == 'excited':
            oled.ellipse(50 + x_offset, 30 + y_offset, 25, 25, 1, True)
            oled.ellipse(50 + x_offset, 30 + y_offset, 15, 15, 0, True)
            # Parlama efekti
            for i in range(8):
                angle = math.pi * i / 4
                r = 30
                ex = int(50 + r * math.cos(angle)) + x_offset
                ey = int(30 + r * math.sin(angle)) + y_offset
                oled.line(50 + x_offset, 30 + y_offset, ex, ey, 1)
        elif state == 'wink':
            if is_left:
                oled.fill_rect(30 + x_offset, 20 + y_offset, 40, 30, 1)
                oled.fill_rect(45 + base_offset + x_offset, 30 + y_offset, 10, 10, 0)
            else:
                # Göz kırpma sadece sağ göz için
                oled.hline(35 + x_offset, 30 + y_offset, 30, 1)
                oled.fill_rect(35 + x_offset, 31 + y_offset, 30, 5, 1)
        elif state == 'thinking':
            oled.fill_rect(30 + x_offset, 20 + y_offset, 40, 30, 1)
            # Yukarı bakış
            oled.fill_rect(45 + base_offset + x_offset, 25 + y_offset, 10, 10, 0)
        elif state == 'blink':
            oled.hline(35 + x_offset, 30 + y_offset, 30, 1)
            oled.fill_rect(35 + x_offset, 31 + y_offset, 30, 3, 1)
            
        oled.show()

    def draw_mouth(self, oled, state, talking=False):
        """Ağız çizimi"""
        oled.fill(0)
        
        if talking:
            # Konuşma efekti - ağız durumunu değiştir
            talk_state = int(time.time() * 5) % 3
            if talk_state == 0:
                self.draw_mouth_shape(oled, state, talk_offset=5)
            elif talk_state == 1:
                self.draw_mouth_shape(oled, state, talk_offset=10)
            else:
                self.draw_mouth_shape(oled, state, talk_offset=0)
        else:
            self.draw_mouth_shape(oled, state)
    
    def draw_mouth_shape(self, oled, state, talk_offset=0):
        """Ağız şeklini çiz"""
        if state == 'normal':
            oled.hline(30, 40, 70, 1)
            if talk_offset:
                oled.hline(40, 40 + talk_offset, 50, 1)
        elif state == 'happy':
            for x in range(30, 100):
                y = 40 - int(10 * math.sin((x-30) * math.pi / 70))
                oled.pixel(x, y, 1)
            if talk_offset:
                for x in range(40, 90):
                    y = 40 - int(10 * math.sin((x-40) * math.pi / 50)) + talk_offset
                    oled.pixel(x, y, 1)
        elif state == 'angry':
            for x in range(30, 100):
                y = 40 + int(10 * math.sin((x-30) * math.pi / 70))
                oled.pixel(x, y, 1)
            if talk_offset:
                for x in range(40, 90):
                    y = 40 + int(10 * math.sin((x-40) * math.pi / 50)) + talk_offset
                    oled.pixel(x, y, 1)
        elif state == 'sad':
            for x in range(30, 100):
                y = 40 + int(15 * math.sin((x-30) * math.pi / 70))
                oled.pixel(x, y, 1)
            if talk_offset:
                for x in range(40, 90):
                    y = 40 + int(15 * math.sin((x-40) * math.pi / 50)) + talk_offset
                    oled.pixel(x, y, 1)
        elif state == 'surprised' or state == 'excited':
            oled.ellipse(65, 40, 20 + talk_offset, 15 + talk_offset, 1, False)
        elif state == 'sleepy':
            oled.hline(40, 40, 50, 1)
            if talk_offset:
                oled.fill_rect(45, 41, 40, talk_offset, 1)
        elif state == 'confused':
            # Dalgalı ağız
            for x in range(30, 100, 2):
                y = 40 + int(3 * math.sin((x-30) * math.pi / 10))
                oled.pixel(x, y, 1)
            if talk_offset:
                for x in range(40, 90, 2):
                    y = 40 + int(3 * math.sin((x-40) * math.pi / 10)) + talk_offset
                    oled.pixel(x, y, 1)
        elif state == 'wink':
            # Hafif gülümseme
            for x in range(30, 100):
                y = 40 - int(5 * math.sin((x-30) * math.pi / 70))
                oled.pixel(x, y, 1)
            if talk_offset:
                for x in range(40, 90):
                    y = 40 - int(5 * math.sin((x-40) * math.pi / 50)) + talk_offset
                    oled.pixel(x, y, 1)
        elif state == 'thinking':
            # Düşünceli ağız
            oled.hline(40, 42, 50, 1)
            oled.fill_rect(60, 30, 20, 20, 1)  # Düşünce baloncuğu
            oled.fill_rect(62, 32, 16, 16, 0)
            oled.text("?", 67, 35, 1)
        
        oled.show()
    
    def set_expression(self, expression, talking=False, duration=2.0):
        """İfadeyi ayarla"""
        if expression not in self.EXPRESSIONS:
            print(f"Bilinmeyen ifade: {expression}")
            expression = 'normal'
        
        self.current_expression = expression
        
        # Göz pozisyonlarını sıfırla
        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [0, 0]
        
        # İfadeyi çiz
        self.draw_eyes()
        self.draw_mouth(self.oleds[2], expression, talking)
        
        # Göz kırpma zamanlayıcısını ayarla
        self.set_blinking(True)
        
        return duration
    
    def draw_eyes(self):
        """Gözleri çiz"""
        self.draw_eye(self.oleds[0], self.current_expression, True, 
                     self.left_eye_pos[0], self.left_eye_pos[1])
        self.draw_eye(self.oleds[1], self.current_expression, False, 
                     self.right_eye_pos[0], self.right_eye_pos[1])
    
    def set_blinking(self, enable=True):
        """Göz kırpma özelliğini aç/kapat"""
        if enable:
            # Rastgele göz kırpma zamanlayıcısı
            blink_interval = random.uniform(2, 6) * 1000  # ms
            self.blink_timer.init(period=int(blink_interval), mode=Timer.ONE_SHOT, callback=self.blink)
        else:
            self.blink_timer.deinit()
    
    def blink(self, timer):
        """Göz kırpma fonksiyonu"""
        # Gözleri kapat
        self.draw_eye(self.oleds[0], 'blink', True, self.left_eye_pos[0], self.left_eye_pos[1])
        self.draw_eye(self.oleds[1], 'blink', False, self.right_eye_pos[0], self.right_eye_pos[1])
        
        # 200ms sonra gözleri aç
        time.sleep(0.2)
        
        # Gözleri tekrar aç
        self.draw_eyes()
        
        # Yeni göz kırpma zamanlayıcısı ayarla
        blink_interval = random.uniform(2, 6) * 1000  # ms
        self.blink_timer.init(period=int(blink_interval), mode=Timer.ONE_SHOT, callback=self.blink)
    
    def setup_random_behavior(self):
        """Rastgele davranışları ayarla"""
        # Her 1 saniyede bir kontrol et
        self.animation_timer.init(period=1000, mode=Timer.PERIODIC, callback=self.random_action_check)
    
    def random_action_check(self, timer):
        """Rastgele davranış kontrolü"""
        now = time.time()
        if now - self.last_random_action > self.random_action_interval:
            # Rastgele bir davranış seç
            action = random.choice([
                self.random_eye_movement,
                self.random_expression,
                self.quick_emotion,
                lambda: None  # Bazen hiçbir şey yapma
            ])
            
            action()
            
            # Sonraki rastgele davranış için zaman ayarla
            self.last_random_action = now
            self.random_action_interval = random.uniform(3, 8)
    
    def random_eye_movement(self):
        """Gözleri rastgele hareket ettir"""
        # Rastgele göz pozisyonları
        self.left_eye_pos = [random.randint(-8, 8), random.randint(-5, 5)]
        self.right_eye_pos = [random.randint(-8, 8), random.randint(-5, 5)]
        
        # Gözleri çiz
        self.draw_eyes()
        
        # 1-2 saniye sonra gözleri normal pozisyona getir
        time.sleep(random.uniform(1, 2))
        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [0, 0]
        self.draw_eyes()
    
    def random_expression(self):
        """Rastgele bir ifade göster"""
        # Mevcut ifadeden farklı bir ifade seç
        expressions = [e for e in self.EXPRESSIONS if e != self.current_expression]
        new_expression = random.choice(expressions)
        
        # İfadeyi ayarla
        duration = self.set_expression(new_expression)
        
        # Bir süre sonra normal ifadeye dön
        time.sleep(duration)
        self.set_expression('normal')
    
    def quick_emotion(self):
        """Hızlı bir duygu ifadesi göster"""
        # Hızlı ifadeler
        quick_expressions = ['surprised', 'wink', 'confused']
        expression = random.choice(quick_expressions)
        
        # İfadeyi ayarla
        self.set_expression(expression)
        
        # Kısa bir süre sonra normal ifadeye dön
        time.sleep(1.0)
        self.set_expression('normal')
    
    def animate_expression_sequence(self, expressions, durations=None, talking=False):
        """İfade dizisi animasyonu"""
        if durations is None:
            durations = [2.0] * len(expressions)
        
        for i, expression in enumerate(expressions):
            self.set_expression(expression, talking)
            time.sleep(durations[i])
    
    def show_emotion(self, emotion):
        """Belirli bir duygu göster"""
        if emotion == 'happy':
            self.animate_expression_sequence(['happy', 'excited', 'happy'], [1.0, 0.5, 2.0])
        elif emotion == 'sad':
            self.animate_expression_sequence(['sad', 'sad'], [3.0, 1.0])
        elif emotion == 'angry':
            self.animate_expression_sequence(['angry', 'angry', 'normal'], [1.0, 2.0, 1.0])
        elif emotion == 'confused':
            self.animate_expression_sequence(['confused', 'thinking', 'confused'], [1.0, 2.0, 1.0])
        elif emotion == 'surprised':
            self.animate_expression_sequence(['surprise