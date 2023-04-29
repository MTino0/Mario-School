import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, screen_height
from tiles import Tile, StaticTile, AnimatedTile
from player import Player
from block import Block

class Level:
    def __init__(self,level_data,surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        
        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # blocks setup
        blocks_layout = import_csv_layout(level_data['blocks'])
        self.blocks_sprites = self.create_tile_group(blocks_layout, 'blocks')
        
        # background
        background_layout = import_csv_layout(level_data['background'])
        self.background_sprites = self.create_tile_group(background_layout, 'background')
        
        # house
        house_layout = import_csv_layout(level_data['house'])
        self.house_sprites = self.create_tile_group(house_layout, 'house')
        
        # flag
        flag_layout = import_csv_layout(level_data['flag'])
        self.flag_sprites = self.create_tile_group(flag_layout, 'flag')
        
        # flag_pole
        flag_pole_layout = import_csv_layout(level_data['flag_pole'])
        self.flag_pole_sprites = self.create_tile_group(flag_pole_layout, 'flag_pole')
        
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'blocks':
                        question_block_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/terrain/terrain_tiles.png')
                        tile_surface = question_block_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'house':
                        house_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/house/House.png')
                        tile_surface = house_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'background':
                        background_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/background/background.png')
                        tile_surface = background_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'flag':
                        flag_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/flag/Flag.png')
                        tile_surface = flag_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    if type == 'flag_pole':
                        flag_pole_tile_list = import_cut_graphics('C:/Pygame/SMBv4/Graphics/flag/flag.png')
                        tile_surface = flag_pole_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
    
    def player_setup(self,layout): # Player image
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)
                if val == '1':
                    spawn_surface = pygame.image.load('C:/Pygame/SMBv4/Graphics/player/player.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,spawn_surface)
                    self.goal.add(sprite)
       
    def horizontal_movement_collision(self): # Collision with side of sprites
        player = self.player.sprite    
        player.rect.x += player.direction.x * player.speed
        
        collidable_sprites = self.terrain_sprites.sprites() + self.blocks_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vertical_movement_collision(self): # Collision with top and bottom of sprites
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.blocks_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0     
                    
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0             
       
    def scroll_x(self): # Camera movement
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/2) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed= 8
                    
    def check_block_collisions(self): # delete block (not working)
        block_collisions = pygame.sprite.spritecollide(self.player.sprite, self.blocks_sprites, False)

        if block_collisions:
            for block in block_collisions:
                block_centre = block.rect.centery
                block_bottom = block.rect.bottom
                player_top = self.player.sprite.rect.top

                # Check if player is colliding from below and has enough velocity to break the block
                if block_bottom < player_top < block_centre and self.player.sprite.direction.y >= 0:
                    # Perform block breaking action
                    block.break_block()  # Call the block's break_block() method
                    # Remove the block from the sprite group
                    self.blocks_sprites.remove(block)
                    # Kill the block sprite
                    block.kill()
                    
    def run(self):
        # Run the entire game / level

        # Update and draw terrain sprites
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Update and draw block sprites
        self.blocks_sprites.update(self.world_shift)
        self.blocks_sprites.draw(self.display_surface)
        
        # Update and draw background sprites
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)

        # Update and draw house sprites
        self.house_sprites.update(self.world_shift)
        self.house_sprites.draw(self.display_surface)

        # Update and draw flag_pole sprites
        self.flag_pole_sprites.update(self.world_shift)
        self.flag_pole_sprites.draw(self.display_surface)

        # Update and draw flag sprites
        self.flag_sprites.update(self.world_shift)
        self.flag_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_block_collisions()