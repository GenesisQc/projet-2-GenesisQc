import pygame
import random
from game_object import GameObject
from constants import *

class Portal(GameObject):
    
    def __init__(self, layout, color, CELL_WIDTH, CELL_HEIGHT):
        self.layout = layout
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.color = color

        rows = len(layout)
        cols = len(layout[0])
    
        
        while True:
            cx = random.randint(0, cols - 1)
            cy = random.randint(0, rows - 1)
            if layout[cy][cx] == 0:
                break

        x = cx * CELL_WIDTH
        y = cy * CELL_HEIGHT

        super().__init__(x, y, CELL_WIDTH, CELL_HEIGHT, color)
    
    def update(self):
        pass


    def draw(self,screen):

        if self.color == "orange":
            path_image = (f"imgs/orange_portal.png")
        else:                
            path_image = (f"imgs/blue_portal.png")
        image_load = pygame.image.load(path_image)

        image_scale = pygame.transform.scale(image_load, (self.width, self.height))

        screen.blit(image_scale, (self.x, self.y))

            
