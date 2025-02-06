import random

font_name = "pressstart2p-regular"
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
        #self.health = 100

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
        
class Missile(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)
        
    def move(self):
        if self.y > -20:
            self.y -= 10  # Düşmanı aşağı hareket ettir
        else:
            return False
        return True


explosions = []

class Explosion(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.frames = [
                            "fragmentation_frame_1",
                            "fragmentation_frame_2",
                            "fragmentation_frame_3",
                            "fragmentation_frame_4",
                            "fragmentation_frame_5",
                            "fragmentation_frame_6",
                        ]
        self.frame = 0
        self.animation_speed = 0.2
        
    def update(self):
        self.frame += self.animation_speed
        if self.frame >= len(self.frames):
            explosions.remove(self)
            return
        self.image = self.frames[int(self.frame)]

# Oyuncu gemisini oluşturuyoruz
ship = Ship("playership2_orange", (640, 360))

ship1 = Actor("playership1_orange", center=(WIDTH / 4, HEIGHT / 3 * 2))
ship2 = Actor("playership2_orange", center=(WIDTH / 4 * 2, HEIGHT / 3 * 2))
ship3 = Actor("playership3_orange", center=(WIDTH / 4 * 3, HEIGHT / 3 * 2))

ship_prices = {
    "playership1_orange": 50,
    "playership2_orange": 75,
    "playership3_orange": 100,
}

# Düşmanlar ve füzeler için boş listeler oluşturuyoruz
enemies = []
missiles = []


# Oyun modu ve can sayısını tanımlıyoruz
mode = "menu"
lives = 3
score = 100
money = 150

menu_options = ["Start Game", "Shop", "Instructions", "Exit"]
selected_option = 0

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
    global mode, lives, score, money

    # Gemi düşmanlarla çarpışıyor mu kontrol et
    enemy_hit = ship.collidelist(enemies)
    if enemy_hit != -1:
        lives -= 1  # Canı bir azalt
        enemies.pop(enemy_hit)  # Çarpışan düşmanı listeden çıkar
        create_enemies(1)  # Yeni bir düşman ekle
        if lives <= 0:
            mode = "gameover"  # Can bitince oyun bitiyor
            
    for enemy in enemies:
        for missile in missiles:
            if enemy.colliderect(missile):
                score += 1 
                chance = random.randint(1,4)
                if chance == 1:
                    money += random.randint(50,100)
                explosion = Explosion("fragmentation_frame_0",enemy.pos)
                explosions.append(explosion)
                enemies.remove(enemy)
                missiles.remove(missile)
                create_enemies(1)
    

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

    if mode == "menu":
        for index, option in enumerate(menu_options):
            color = "yellow" if index == selected_option else "white"
            screen.draw.text(option,center=(WIDTH // 2, HEIGHT // 2 + index * 50), fontsize=40, color=color, fontname="pressstart2p-regular")
            
    elif mode == "shop":
        screen.draw.text(
            "Select Your Ship",
            center=(WIDTH // 2, HEIGHT // 4),
            fontsize=50,
            color="white",
            fontname=font_name,
        )

        ship1.draw()
        screen.draw.text(
            f"{ship_prices['playership1_orange']}",
            center=(WIDTH // 4, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        ship2.draw()
        screen.draw.text(
            f"{ship_prices['playership2_orange']}",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        ship3.draw()
        screen.draw.text(
            f"{ship_prices['playership3_orange']}",
            center=(WIDTH // 4 * 3, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        screen.draw.text(
            f"Money: {money}",
            center=(WIDTH // 2, HEIGHT // 4 + 100),
            fontsize=30,
            color="white",
            fontname=font_name,
        )
        screen.draw.text(
            "Press 'Enter' to return to menu.",
            center=(WIDTH // 2, HEIGHT - 50),
            fontsize=24,
            color="white",
            fontname=font_name,
        )
        
        
    elif mode == "game":
        ship.draw()  # Oyuncu gemisini çiz
        screen.draw.text(str(score), topright=(1250, 30), fontsize=24, fontname="pressstart2p-regular")
        
        screen.draw.text(str(money), center=(600, 30), fontsize=24, fontname="pressstart2p-regular")

        # Düşmanları ekrana çiz
        for enemy in enemies:
            enemy.draw()
            
        for missile in missiles:
            missile.draw()
            
        for explosion in explosions:
            explosion.draw()

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
    global mode, enemies, lives, selected_option
    # key: hangi tuşa basıldığını temsil eder
    
    if mode == "gameover" and keyboard.r :
        mode = "menu"  # Oyunu yeniden başlat
        enemies = []  # Düşman listesini temizle
        create_enemies(5)  # Yeni düşmanlar oluştur
        lives = 3  # Canları sıfırla
        score = 0 
    
    elif mode== "menu" :
        if keyboard.UP:
            selected_option = (selected_option - 1 ) % len(menu_options)
        if keyboard.DOWN:
            selected_option = (selected_option + 1 ) % len(menu_options)
        if keyboard.RETURN:
            if selected_option == 0:
                mode = "game"
            if selected_option == 1:
                mode = "shop"
                
    elif mode== "shop" :
        if keyboard.RETURN:
            mode = "menu"

# Fare hareket ettiğinde çağrılan fonksiyon (pgzero'ya ait)
def on_mouse_move(pos):
    # pos: (x, y) koordinatlarını içeren bir tuple, fare imlecinin konumunu temsil eder
    ship.move(pos)  # Gemi fare ile hareket ettirilir

# Fareye tıklanınca füze ateşlemek için kullanılan fonksiyon (pgzero'ya ait)
def on_mouse_down(button, pos):
    global money
    
    # button: Hangi fare düğmesine basıldığını temsil eder (mouse.left, mouse.right vb.)
    # pos: (x, y) koordinatlarını içeren bir tuple, fare tıklamasının konumunu belirtir
    if mode == "game" and button == mouse.LEFT:
        missile = Missile("laserred01", ship.pos)
        missiles.append(missile)
        
    elif mode == "shop":
        if ship1.collidepoint(pos) and money >= ship_prices["playership1_orange"]:
            money -= ship_prices["playership1_orange"]
            ship.image = "playership1_orange"
        if ship2.collidepoint(pos) and money >= ship_prices["playership2_orange"]:
            money -= ship_prices["playership2_orange"]
            ship.image = "playership2_orange2"
        if ship3.collidepoint(pos) and money >= ship_prices["playership3_orange"]:
            money -= ship_prices["playership3_orange"]
            ship.image = "playership3_orange"
            
            

# Oyun içindeki güncellemeleri gerçekleştiren fonksiyon (pgzero'ya ait)
def update(dt):
    # dt: Delta time, iki güncelleme arasındaki süreyi temsil eder
    if mode == "game":
        for enemy in enemies:
            enemy.move()  # Düşmanları hareket ettir
    
        for missile in missiles:
            if not missile.move():
                missiles.remove(missile)
                
        for explosion in explosions:
            explosion.update()
        
        handle_collision()  # Çarpışmaları kontrol et

# İlk başta 5 düşman oluşturuyoruz
create_enemies(5)
