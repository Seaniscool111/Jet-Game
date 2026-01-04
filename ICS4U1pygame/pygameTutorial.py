#=============== TUTORIAL ===============#

# Import the pygame module
import pygame
import random
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN, # key press event
    QUIT,
)

# Setup for sounds.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock
clock = pygame.time.Clock()


#========= GAME SET UP =========#
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.mp3")
move_down_sound = pygame.mixer.Sound("Falling_putter.mp3")
collision_sound = pygame.mixer.Sound("Collision.mp3")


# Define the Player object by extending pygame.sprite.Sprite
# Instead of a surface, use an image for a better-looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)



# Define the enemy object by extending pygame.sprite.Sprite
# Instead of a surface, use an image for a better-looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()



# Create a surface and pass in a tuple containing its length and width
surf = pygame.Surface((50, 50))

# Give the surface a color to separate it from the background
surf.fill((0, 0, 0))
rect = surf.get_rect()

### Create groups to hold enemy sprites, cloud sprites, and all sprites ###
# Create Player Object
player = Player()

# - enemies is used for collision detection and position updates
enemies = pygame.sprite.Group()

# - clouds is used for position updates
clouds = pygame.sprite.Group()

# - all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Variable to keep the main loop running
running = True
# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player
            player.kill()

            # Stop any moving sounds and play the collision sound
            move_up_sound.stop()
            move_down_sound.stop()
            collision_sound.play()

            # Stop the loop
            running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
        
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    # Update enemy & clouds position
    enemies.update()
    clouds.update()
    
    # Refresh and tick
    pygame.display.flip()
    clock.tick(FPS)

    # Fill the screen with white
    screen.fill((135, 206, 250))

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
