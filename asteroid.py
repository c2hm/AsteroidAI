import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fusée dans l'espace")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Classe pour la fusée
class Rocket:
    def __init__(self):
        self.x = 50  # Position initiale à gauche de l'écran
        self.y = HEIGHT // 2
        self.vy = 0  # Vitesse verticale uniquement

    def update(self):
        self.y += self.vy
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y - 10, 20, 20))

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 10

    def update(self):
        self.x += self.vx

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y - 2, 10, 4))

class Asteroid:
    def __init__(self):
        self.reset_position()

    def reset_position(self):
        self.x = WIDTH + random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.randint(50, 150)
        self.vx = random.uniform(5, 10)

    def update(self):
        self.x -= self.vx
        if self.x < -self.radius:
            self.reset_position()

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def shrink(self):
        self.radius -= 10  
        if self.radius < 10:
            self.reset_position()

def check_rocket_collision(rocket, asteroids):
    for asteroid in asteroids:
        distance = math.hypot(rocket.x - asteroid.x, rocket.y - asteroid.y)
        if distance < asteroid.radius + 10:
            return True
    return False

def check_missile_collision(missiles, asteroids):
    for missile in missiles[:]:
        for asteroid in asteroids:
            distance = math.hypot(missile.x - asteroid.x, missile.y - asteroid.y)
            if distance < asteroid.radius:
                asteroid.shrink()
                missiles.remove(missile)
                break

# Fonction pour réinitialiser le jeu
def reset_game():
    global rocket, asteroids, missiles, score, running, game_over
    rocket = Rocket()
    asteroids = [Asteroid() for _ in range(10)]
    missiles = []
    score = 0
    game_over = False

# Initialisation du jeu
reset_game()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True

# Boucle de jeu
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                missiles.append(Missile(rocket.x + 20, rocket.y))
            elif event.key == pygame.K_r and game_over:
                reset_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        rocket.vy = -5
    elif keys[pygame.K_DOWN]:
        rocket.vy = 5
    else:
        rocket.vy = 0

    if not game_over:
        rocket.update()
        for asteroid in asteroids:
            asteroid.update()
        for missile in missiles[:]:
            missile.update()
            if missile.x > WIDTH:
                missiles.remove(missile)

        if check_rocket_collision(rocket, asteroids):
            game_over = True

        check_missile_collision(missiles, asteroids)
        score += 1

    # Affichage
    rocket.draw()
    for asteroid in asteroids:
        asteroid.draw()
    for missile in missiles:
        missile.draw()

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Affichage de l'écran de fin de jeu
    if game_over:
        game_over_text = font.render("Game Over! Press 'R' to Replay", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
