"""
Jet Game — Python / Pygame

2D game featuring physics-based movement, dynamic difficulty scaling,
state-driven gameplay, and persistent high-score tracking.
"""

#========= IMPORT MODULES =========#
import pygame
import random
import os

# Importing Files used
from assets_loader import (
    load_image,
    load_sound,
    load_music,
    load_font,
    get_data_file
)


# Import Keyboard movements from pygame.locals
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,  # key press event
    QUIT,
)

#========= INITIALIZATION =========#
pygame.init()  # Initialize pygame modules

#========= SCREEN SET UP =========#
SCREEN_WIDTH = 1200     # SCREEN WIDTH
SCREEN_HEIGHT = 600    # SCREEN HEIGHT
FPS = 30               # FRAMES PER SECOND
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jet Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Preview jet variables for the main menu
preview_jet_x = -100  # Start offscreen
preview_jet_speed = 2

# File path for storing high score
HIGH_SCORE_FILE = get_data_file("highscore.txt")

#================== LOAD SOUND FILES ==================#
#==== MUSIC ====#
# Sound source: https://pixabay.com/sound-effects/search/jet%20boost/
load_music("background_music.mp3")
pygame.mixer.music.play(loops=-1)


#==== SOUND EFFECTS ====#
# Flying Up
# Sound Source: https://pixabay.com/sound-effects/launching-jet-plane-332969/
move_up_sound = load_sound("Rising.mp3")

# Flying Down
# Sound Source: https://pixabay.com/sound-effects/launching-jet-plane-332969/
move_down_sound = load_sound("Falling.mp3")

# Flying Forward
# Sound Source: https://pixabay.com/sound-effects/nitro-activation-48077/
forward_sound = load_sound("Forward.mp3")

# Flying Backward
# Sound Source: https://pixabay.com/sound-effects/nitro-activation-48077/
backward_sound = load_sound("Backward.mp3")

# Collision
# Sound source: https://pixabay.com/sound-effects/search/car-crash/
collision_sound = load_sound("Collision.mp3")

# Jet Start Up (At the beginning of the game)
# Sound source: https://pixabay.com/sound-effects/jet-engine-startup-14537/
jet_startup = load_sound("Jet_EngineStartUp.mp3")

#====== FUNCTION: load_high_score() ======#
# Load high score from file
def load_high_score():
    # Read high score from file 
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

#====== FUNCTION: save_high_score(score) ======#
def save_high_score(score):
    # Saving high score to file
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

#====== FUNCTION:draw_text_center(text, size, color, surface, y) ======#
# Draws centered text
def draw_text_center(text, size, color, surface, y):
    font = load_font(custom_font_path, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    surface.blit(text_surface, text_rect)


#========= Player Sprite Class =========#
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = load_image("jet.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(100, SCREEN_HEIGHT // 2))
        
        # Physics Movements
        self.vel = pygame.math.Vector2(1, 0)
        self.acc = pygame.math.Vector2(1, 0)
        self.friction = -0.3
        self.acceleration_strength = 2.5
        self.max_speed = 7


    def update(self, pressed_keys):
        # Reset Acceleration
        self.acc = pygame.math.Vector2(0, 0)
        
        # Movement of Player with Acceleration based on input
        if pressed_keys[K_UP]: 
            self.acc.y = -self.acceleration_strength
            if not move_up_sound.get_num_channels():
                move_up_sound.play()
        if pressed_keys[K_DOWN]: 
            self.acc.y = self.acceleration_strength
            if not move_down_sound.get_num_channels():
                move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.acceleration_strength
            if not backward_sound.get_num_channels():
                backward_sound.play()
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.acceleration_strength
            if not forward_sound.get_num_channels():
                forward_sound.play()

        # Apply friction to velocity and update it
        self.acc += self.vel * self.friction
        self.vel += self.acc

        # Setting max speed limit
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Keep player within screen
        self.rect.move_ip(self.vel.x, self.vel.y)
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

#========= Enemy Sprite Class =========#
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super(Enemy, self).__init__()
        self.surf = load_image("missile.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = random.randint(5 + level * 2, 10 + level * 3)

    def update(self):
        # Move the missiles to the left, kill when it goes off screen
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#========= Cloud Sprite Class =========#
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = load_image("cloud.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT))
        )

    def update(self):
        # Move left and kill when off-screen
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#========= GAME SET UP =========#
# Custom events for spawning missiles and clouds
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2

# Initial enemy spawn timer delay
enemy_spawn_delay = 250
pygame.time.set_timer(ADDENEMY, enemy_spawn_delay)
pygame.time.set_timer(ADDCLOUD, 1000)

### Create Player and Sprite Groups  ###
player = Player()
enemies = pygame.sprite.Group()     # Enemies used for Collision Detection and Position updates
clouds = pygame.sprite.Group()      # Clouds used for position updates
all_sprites = pygame.sprite.Group() # All sprites used for rendering
all_sprites.add(player)


# Load Custom font
# Source: https://www.dafont.com/moodcake.font 
custom_font_path = "moodcake.ttf"
font = load_font(custom_font_path, 48)

# Loading High Score
high_score = load_high_score()
print("Loaded high score:", high_score)
score_font = load_font(custom_font_path, 32)
level_font = load_font(custom_font_path, 24)

#====== TRACKING ======#
# Score and Level Information
score = 0
level = 1
# Game controlling variables
running = True
game_state = "start"
enemy_timer_started = False



#====================================================#
#================== MAIN GAME LOOP ==================#
#====================================================#
while running:
    # Setting background of screen to sky blue
    screen.fill((135, 206, 250))
    # Event handling
    for event in pygame.event.get():
        
        # Adding Clouds at the starting menu of game
        if event.type == ADDCLOUD:
            cloud = Cloud()
            clouds.add(cloud)
            all_sprites.add(cloud)
            
        # Exit Game and Close
        if event.type == QUIT:
            running = False

        #===== START STATE =====#
        if game_state == "start":
            
            # Check for Key Presses
            if event.type == KEYDOWN:
                # Click ESC to Exit game
                if event.key == K_ESCAPE:
                    game_state = "exit"

                elif event.key == K_RETURN:
                    # Reset game stats
                    if jet_startup.get_num_channels() == 0:
                        jet_startup.play()
                    
                    game_state = "playing"
                    score = 0
                    player = Player()
                    enemies.empty()
                    clouds.empty()
                    all_sprites.empty()
                    all_sprites.add(player)

                    level = 1
                    enemy_spawn_delay = 250
                    enemy_timer_started = False  # Reset timer flag on restart
                    start_time = pygame.time.get_ticks()  # Track when the game starts
                    pygame.time.set_timer(ADDENEMY, 0)    # Temporarily pauses enemy spawn


        #===== PLAYING STATE =====#
        elif game_state == "playing":
            current_time = pygame.time.get_ticks()

            # Wait 2 seconds before starting enemy spawns
            if not enemy_timer_started and pygame.time.get_ticks() - start_time >= 2000:
                pygame.time.set_timer(ADDENEMY, enemy_spawn_delay)
                enemy_timer_started = True
                enemy_spawn_event_time = current_time + enemy_spawn_delay  # Pausing timer to stop enemies and clouds from spawning
            
            # Pausing Game
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_state = "paused"
                
                 # Calculate remaining time until next enemy spawn
                enemy_spawn_remaining = max(0, enemy_spawn_event_time - pygame.time.get_ticks())
                
                pygame.time.set_timer(ADDENEMY, 0)  # Stop enemy spawn timer
                pygame.time.set_timer(ADDCLOUD, 0)

            # Spawn Enemies
            elif event.type == ADDENEMY:
                enemy = Enemy(level) 
                enemies.add(enemy)
                all_sprites.add(enemy)

                enemy_spawn_event_time = current_time + enemy_spawn_delay

        #===== PAUSED STATE =====#
        elif game_state == "paused":
            # Check for Key presses
            if event.type == KEYDOWN:
                
                # Click ESC to Resume game
                if event.key == K_ESCAPE:
                    game_state = "playing"  # Resume game
                    pygame.time.set_timer(ADDENEMY, enemy_spawn_remaining)
                    enemy_spawn_event_time = pygame.time.get_ticks() + enemy_spawn_remaining
                    pygame.time.set_timer(ADDCLOUD, 1000)

                elif event.key == pygame.K_RETURN:
                    game_state = "start"  # Optionally allow restart from pause menu

        #===== GAME OVER STATE =====#
        elif game_state == "game_over":
            # Setting new high score if greater than previous one
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            if event.type == KEYDOWN:
                # Exiting game
                if event.key == K_ESCAPE:
                    game_state = "exit"
                    running = False
                # Enter key to restart game
                elif event.key == pygame.K_RETURN:
                    game_state = "start"
       
        elif event.type == pygame.KEYUP:
            if event.key == K_UP:
                move_up_sound.stop()
            elif event.key == K_DOWN:
                move_down_sound.stop()
            elif event.key == K_LEFT:
                backward_sound.stop()
            elif event.key == K_RIGHT:
                forward_sound.stop()


    # Displays for different states
    if game_state == "exit":
        running = False
        continue
    
    # Displays for Start State
    if game_state == "start":
        # Update preview jet's position
        preview_jet_x += preview_jet_speed
        if preview_jet_x > SCREEN_WIDTH + 100:
            preview_jet_x = -100  # Loop back to the left side

        # Update and draw clouds
        clouds.update()
        for cloud in clouds:
            
            screen.blit(cloud.surf, cloud.rect)

        screen.blit(player.surf, (preview_jet_x, SCREEN_HEIGHT // 2))

        # Title and Instructions
        draw_text_center("JET GAME", 64, (255, 165, 0), screen, SCREEN_HEIGHT // 3)
        draw_text_center("Press Enter To Start", 36, (255, 255, 255), screen, SCREEN_HEIGHT // 2)
        draw_text_center("Press ESC to Exit", 24, (255, 255, 0), screen, SCREEN_HEIGHT // 2 + 40)
        draw_text_center(f"High Score: {high_score}", 28, (0, 0, 0), screen, SCREEN_HEIGHT // 2 + 80)

    # Displays for Playing State
    elif game_state == "playing":
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Increasing score
        score += 20

        # Increasing Difficulty Every 5000 Points
        if score // 5000 + 1 > level:
            level += 1 # Increase level by 1

            if enemy_spawn_delay > 200: 
                enemy_spawn_delay -= 30 # Removing delay from enemy_spawn_delay
                pygame.time.set_timer(ADDENEMY, enemy_spawn_delay)

        # Update Enemies and Clouds
        enemies.update()
        clouds.update()

        # Draw Clouds
        for cloud in clouds:
            screen.blit(cloud.surf, cloud.rect)

        # Draw Enemies 
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Display for Score
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Display for Level
        level_text = level_font.render(f"Level: {level}", True, (255, 255, 0))
        screen.blit(level_text, (10, 40))

        # Display for High Score
        high_score_text = score_font.render(f"High Score: {high_score}", 28, (0, 0, 0))
        high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(high_score_text, high_score_rect)

        # Collision Detection
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()

            # Stop movement sounds to avoid overlapping
            move_up_sound.stop()
            move_down_sound.stop()
            forward_sound.stop()
            backward_sound.stop()
            collision_sound.play()

            game_state = "game_over"

    # Displays for Paused State
    elif game_state == "paused":
        draw_text_center("Game Paused", 64, (255, 255, 255), screen, SCREEN_HEIGHT // 3)
        draw_text_center("Press ESC to Resume", 36, (255, 255, 0), screen, SCREEN_HEIGHT // 2)
        draw_text_center("Press Enter to Restart", 24, (255, 255, 255), screen, SCREEN_HEIGHT // 2 + 40)

    # Displays for Game Over State
    elif game_state == "game_over":
        draw_text_center("Game Over", 64, (255, 0, 0), screen, SCREEN_HEIGHT // 3)
        draw_text_center("Press Enter To Return To Start", 36, (255, 255, 255), screen, SCREEN_HEIGHT // 2)
        draw_text_center("Press ESC to Exit", 24, (255, 255, 0), screen, SCREEN_HEIGHT // 2 + 40)
        draw_text_center(f"Final Score: {score}", 28, (255, 255, 255), screen, SCREEN_HEIGHT // 2 + 80)


    pygame.display.flip()
    clock.tick(FPS) #30 Frames Per Second

# Exit Program
pygame.quit()
