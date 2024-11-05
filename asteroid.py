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
YELLOW = (255, 255, 0)

# Chargement des images
rocket_image = pygame.image.load("ship.png")
asteroid_base_image = pygame.image.load("asteroid.png")

# Rotation et redimensionnement de la fusée
rocket_image = pygame.transform.rotate(rocket_image, -90)  # Rotate 90 degrees to the right
rocket_image = pygame.transform.scale(rocket_image, (rocket_image.get_width() // 2.5, rocket_image.get_height() // 2.5))

# Classe pour la fusée
class Rocket:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vy = 0
        self.width = rocket_image.get_width()
        self.height = rocket_image.get_height()

    def update(self):
        self.y += self.vy
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def draw(self):
        screen.blit(rocket_image, (self.x, self.y))

        # Draw the collision boxes in red
        # for box in self.get_collision_boxes():
        #     pygame.draw.rect(screen, (255, 0, 0), box, 1)  # Red outline for each collision box

    def get_collision_boxes(self):
        # Divides the ship into 3 smaller rectangles for better collision detection
        box_width = self.width // 3
        boxes = [
            pygame.Rect(self.x, self.y, box_width, self.height),  # Left box
            pygame.Rect(self.x + box_width, self.y + self.height/2 /2, box_width, self.height/2),  # Middle box
            pygame.Rect(self.x + 2 * box_width, self.y + self.height/2.65, box_width*0.7, self.height/4),  # Right box
            pygame.Rect(self.x + 2.7 * box_width, self.y + self.height/2.265, box_width*0.3, self.height/8)  # Right box
        ]
        return boxes

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
        self.y = random.randint(0, HEIGHT)  # Spawning across the whole screen height
        self.radius = random.randint(50, 150)
        self.vx = random.uniform(5, 10)
        self.image = pygame.transform.scale(asteroid_base_image, (self.radius * 2, self.radius * 2))

    def update(self):
        self.x -= self.vx
        if self.x < -self.radius * 2:
            self.reset_position()

    def draw(self):
        screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))
        #pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 1)  # 1 is the width for outline

    def shrink(self):
        self.radius = int(self.radius * 0.75)
        if self.radius < 20:
            self.reset_position()
        else:
            self.image = pygame.transform.scale(asteroid_base_image, (self.radius * 2, self.radius * 2))

def check_rocket_collision(rocket, asteroids):
    collision_boxes = rocket.get_collision_boxes()
    for asteroid in asteroids:
        for box in collision_boxes:
            if Collision_cicle_rect((asteroid.x, asteroid.y), asteroid.radius, (box.centerx, box.centery), box.width, box.height):
                return True
    return False

import math

def Collision_cicle_rect(circle_center, circle_radius, rect_center, rect_width, rect_height):
    c_x, c_y = circle_center
    r_x, r_y = rect_center
    r_width, r_height = rect_width, rect_height

    # Calculate rectangle bounds
    r_min_x = r_x - r_width / 2
    r_max_x = r_x + r_width / 2
    r_min_y = r_y - r_height / 2
    r_max_y = r_y + r_height / 2

    # Find the closest point on the rectangle to the circle's center
    closest_x = max(r_min_x, min(c_x, r_max_x))
    closest_y = max(r_min_y, min(c_y, r_max_y))

    # Calculate distance from the circle's center to the closest point
    distance_squared = (c_x - closest_x) ** 2 + (c_y - closest_y) ** 2

    # Check for collision
    return distance_squared <= circle_radius ** 2


def check_missile_collision(missiles, asteroids):
    for missile in missiles[:]:
        for asteroid in asteroids:
            distance = math.hypot(missile.x - asteroid.x, missile.y - asteroid.y)
            if distance < asteroid.radius:
                asteroid.shrink()
                missiles.remove(missile)
                break

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
                missiles.append(Missile(rocket.x + rocket.width, rocket.y + rocket.height // 2))
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
