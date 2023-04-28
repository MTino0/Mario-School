import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite): # Object
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def update(self,shift):
        self.rect.x += shift
        
class StaticTile(Tile): # Solid Object
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface
        
class AnimatedTile(Tile): # Animated Object
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self): # Animation Frames
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def change_image(self, new_image_path): # Animation
        self.image = pygame.image.load(new_image_path).convert_alpha()
        
    def update(self,shift):
        self.animate()
        self.rect.x += shift