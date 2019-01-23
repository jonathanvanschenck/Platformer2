"""
Main gui for game.
"""

import pygame as pg
from pygame.locals import *
import varbs
import classes
import engine

def main():
    # Initalize the Screen
    pg.init()
    screen = pg.display.set_mode((varbs.screenW,varbs.screenH))
    pg.display.set_caption("The Judges")
    
    # Initalized a background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))
    
    # Populate background
    font = pg.font.Font(None, 36)
    text = font.render("Hello!", 1, (10,10,10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)
    
    # Initialize player
    global player
    player = classes.Player()
    
    # Initialize platform
    global platform
    platform = classes.Platform()
    platform2 = classes.Platform(dx=200,dy=-300,openBottom=True)
    
    # Initialize sprite groups
    playerSprite = pg.sprite.Group(player)
    platformSprites = pg.sprite.Group((platform,platform2))
    scrollingSprites = pg.sprite.RenderPlain((player,platform,platform2))
    physicsSprites = pg.sprite.RenderPlain(player)
    
    # Blit everything to the screen
    screen.blit(background, (0,0))
    pg.display.update()
    
    # Initialize the clock
    clock = pg.time.Clock()
    
    while 1:
        clock.tick(varbs.framerate)
        for event in pg.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_a:
                    player.setAccel(left=-1.0)
                if event.key == K_d:
                    player.setAccel(right=1.0)
                if event.key == K_w:
                    player.jumpAttempt()
                    player.jumpActive = False
            if event.type == KEYUP:
                if event.key == K_a:
                    player.setAccel(left=0.0)
                if event.key == K_d:
                    player.setAccel(right=0.0)
                if event.key == K_w:
                    player.jumpActive = True

        # Erase Player and platform location    
        screen.blit(background, platform.rect, platform.rect)
        screen.blit(background, player.rect, player.rect)
        # Step physics
        engine.stepPhysics(physicsSprites)
        engine.stepPlayer(playerSprite)
        for sprite in physicsSprites.sprites():
            sprite.moveFromV()
            engine.collisionPlatform(sprite,platformSprites)
        # Scroll Screen
        charx = player.rect.centerx
        if charx < 0.2*varbs.screenW or charx > 0.8*varbs.screenW:
            dx = screen.get_rect().centerx - charx
            for sprite in scrollingSprites.sprites():
                sprite.rect.move_ip(dx,0)
        # Update all sprites
        scrollingSprites.update()
        # Draw all sprites (via groups)
        scrollingSprites.draw(screen)
        # Update display with new screen
        pg.display.flip()


if __name__ == "__main__":
    main()
