import pygame
from tiles import StaticTile

class Block(StaticTile): # Not Working
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'C:/Pygame/SMBv4/Graphics/animation/block/0.png')
        
    def update(self, *args, **kwargs):
        pass
    
    def collide_with_player(self):
        # Handle collision with the player sprite
        if self.rect.colliderect(self.player.rect) and self.rect.bottom == self.player.rect.top:
            self.break_block()  # Call the method to break the block

    def break_block(self):
        if not self.is_broken:
            self.is_broken = True
            # Add code for the breaking animation
            if self.current_animation_frame < self.break_animation_frames:
                self.rect.y -= 3  # Move the block sprite up by 3 pixels
                self.current_animation_frame += 1
            else:
                self.kill()  # Kill the block sprite after the animation is done