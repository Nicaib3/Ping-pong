from pygame import *
from random import randint

# Inicializar Pygame
init()

# Clases
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y, None)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y *= -1

# Configuración de la ventana
back = (128, 0, 128)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")

# Estado del juego
game = True
finish = False
clock = time.Clock()
FPS = 60

# Creación de los objetos
P1 = Player('racket.png', 10, 200, 150, 100, 5)
P2 = Player('racket.png', win_width -150, 200, 150, 100, 5)
ball = Ball('ball.png', 300, 250, 50, 50, 3, 3)

# Textos para el juego
font.init()
font = font.Font(None, 35)
loseP1 = font.render('Player 1 loses!!', True, (180, 0, 0))
loseP2 = font.render('Player 2 loses!!', True, (180, 0, 0))

# Bucle del juego
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)

        P1.update_l()
        P2.update_r()
        ball.update()

        # Colisiones con las paletas
        if sprite.collide_rect(P1, ball):
            ball.speed_x = abs(ball.speed_x)
        if sprite.collide_rect(P2, ball):
            ball.speed_x = -abs(ball.speed_x)

        # Comprobar si un jugador pierde
        if ball.rect.x < 0:
            finish = True
            window.blit(loseP1, (200, 200))

        if ball.rect.x > win_width:
            finish = True
            window.blit(loseP2, (200, 200))

        P1.reset()
        P2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
