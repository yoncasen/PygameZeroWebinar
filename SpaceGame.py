import random

# Oyun penceresinin genişliği ve yüksekliği belirleniyor
WIDTH = 1280
HEIGHT = 720

# Oyun başlığı belirleniyor
TITLE = "Space Game"

# Oyun kare hızını (FPS) belirliyoruz
FPS = 30

# Oyuncu gemisini temsil eden sınıf
class Ship(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)

    # Gemi fare ile hareket ettirildiğinde bu fonksiyon çağrılır
    # pos: (x, y) koordinatlarını içeren bir tuple, fare imlecinin konumunu temsil eder
    def move(self, pos):
        # Gemi ekran sınırlarını aşmasın diye konumunu kısıtlıyoruz
        self.x = max(100, min(WIDTH - 100, pos[0]))
        self.y = max(100, min(HEIGHT - 100, pos[1]))

# Düşman gemilerini temsil eden sınıf
class Enemy(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed  # Düşmanın düşme hızı

    # Düşmanları aşağı doğru hareket ettiren fonksiyon
    def move(self):
        if self.y < HEIGHT:
            self.y += self.speed  # Düşmanı aşağı hareket ettir
        else:
            self.reset_position()  # Ekrandan çıkarsa konumunu sıfırla

    # Düşmanın yeni bir rastgele konuma sıfırlanmasını sağlar
    def reset_position(self):
        self.x = random.randint(50, 1230)
        self.y = random.randint(-100, -50)
        self.speed = random.randint(5, 8)

# Oyuncu gemisini oluşturuyoruz
ship = Ship("playership2_orange", (640, 360))

# Düşmanlar ve füzeler için boş listeler oluşturuyoruz
enemies = []
missiles = []

# Oyun modu ve can sayısını tanımlıyoruz
mode = "game"
lives = 3

# Belirtilen sayıda düşman oluşturur ve listeye ekler
def create_enemies(count):
    for _ in range(count):
        x = random.randint(50, 1230)
        y = random.randint(-100, -50)
        speed = random.randint(5, 8)
        enemy = Enemy("enemyblue2", (x, y), speed)
        enemies.append(enemy)

# Gemi ile düşmanlar çarpıştığında yapılacak işlemler
def handle_collision():
    global mode, lives

    # Gemi düşmanlarla çarpışıyor mu kontrol et
    enemy_hit = ship.collidelist(enemies)
    if enemy_hit != -1:
        lives -= 1  # Canı bir azalt
        enemies.pop(enemy_hit)  # Çarpışan düşmanı listeden çıkar
        create_enemies(1)  # Yeni bir düşman ekle
        if lives <= 0:
            mode = "gameover"  # Can bitince oyun bitiyor

# Ekranı çizmek için kullanılan fonksiyon (pgzero'ya ait)
def draw():
    screen.clear()  # Ekranı temizle

    # Arka planı döşemek için tekrar tekrar çizen döngü
    for x in range(0, WIDTH, images.darkpurple.get_width()):
        for y in range(0, HEIGHT, images.darkpurple.get_height()):
            # screen.blit fonksiyonu ekrana bir görüntü çizer.
            # Parametreleri:
            # - image: Çizilecek görselin adı (string, örn: "darkpurple")
            # - pos: Görselin çizileceği konum (x, y) şeklinde bir tuple
            # - angle (isteğe bağlı): Görselin döndürülme açısı (derece cinsinden, varsayılan: 0)
            # - alpha (isteğe bağlı): Görüntünün saydamlık değeri (0-255 arası, 255 tamamen opak)
            screen.blit("darkpurple", (x, y))

    if mode == "game":
        ship.draw()  # Oyuncu gemisini çiz

        # Düşmanları ekrana çiz
        for enemy in enemies:
            enemy.draw()

        # Canları ekrana çiz (kalp simgesi olarak)
        for i in range(lives):
            heart_image_actor = Actor("playerlife2_orange", (30 + i * 40, 20))
            heart_image_actor.draw()

    elif mode == "gameover":
        # Oyun bitti ekranı
        # screen.draw.text metni ekrana yazdırır. Parametreleri:
        # - text: Yazdırılacak metin (string)
        # - center: Metnin merkez konumunu belirten (x, y) tuple'ı
        # - fontsize: Yazı tipi boyutu (int)
        # - fontname: Yazı tipi adı (string, sistemde yüklü olmalı)
        # - color (isteğe bağlı): Yazı rengi (RGB tuple veya renk adı olarak string, örn: "white")
        screen.draw.text("GAME OVER!", center=(640, 360), fontsize=36, fontname="pressstart2p-regular")
        screen.draw.text("Press R to restart", center=(640, 460), fontsize=24, fontname="pressstart2p-regular")

# Klavye girişlerini kontrol eden fonksiyon (pgzero'ya ait)
def on_key_down(key):
    global mode, enemies, lives
    # key: hangi tuşa basıldığını temsil eder
    if keyboard.r and mode == "gameover":
        mode = "game"  # Oyunu yeniden başlat
        enemies = []  # Düşman listesini temizle
        create_enemies(5)  # Yeni düşmanlar oluştur
        lives = 3  # Canları sıfırla

# Fare hareket ettiğinde çağrılan fonksiyon (pgzero'ya ait)
def on_mouse_move(pos):
    # pos: (x, y) koordinatlarını içeren bir tuple, fare imlecinin konumunu temsil eder
    ship.move(pos)  # Gemi fare ile hareket ettirilir

# Fareye tıklanınca füze ateşlemek için kullanılan fonksiyon (pgzero'ya ait)
#def on_mouse_down(button, pos):
    # button: Hangi fare düğmesine basıldığını temsil eder (mouse.left, mouse.right vb.)
    # pos: (x, y) koordinatlarını içeren bir tuple, fare tıklamasının konumunu belirtir
    #if mode == "game" and button == mouse.left:
    #    missile = Missile("laserred01", ship.pos)
    #    missiles.append(missile)

# Oyun içindeki güncellemeleri gerçekleştiren fonksiyon (pgzero'ya ait)
def update(dt):
    # dt: Delta time, iki güncelleme arasındaki süreyi temsil eder
    if mode == "game":
        for enemy in enemies:
            enemy.move()  # Düşmanları hareket ettir
        handle_collision()  # Çarpışmaları kontrol et

# İlk başta 5 düşman oluşturuyoruz
create_enemies(5)
