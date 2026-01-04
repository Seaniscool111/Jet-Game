import os
import pygame

#====== LOADING FUNCTIONS ======#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_image(filename):
    return pygame.image.load(
        os.path.join(ASSETS_DIR, "images", filename)
    ).convert()

def load_sound(filename):
    return pygame.mixer.Sound(
        os.path.join(ASSETS_DIR, "sounds", filename)
    )

def load_music(filename):
    pygame.mixer.music.load(
        os.path.join(ASSETS_DIR, "music", filename)
    )

def load_font(filename, size):
    return pygame.font.Font(
        os.path.join(ASSETS_DIR, "fonts", filename), size
    )

def get_data_file(filename):
    return os.path.join(BASE_DIR, filename)
