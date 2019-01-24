"""
Main gui for game.
"""

import pygame as pg
from pygame.locals import *
import varbs
import classes
import engine
import initialize

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
    
    # Initialize player
    global player
    global sword
    player = initialize.initPlayer()
    sword = initialize.initSword(player)
    
    # Initialize mobs
    global mobs
    mobs = initialize.initMobs()
    
    # Initialize platforms
    global platforms
    platforms = initialize.initPlatforms()
    
    # Initialize Lava and Goal
    global lava
    lava = initialize.initLava()
    global goal
    goal = initialize.initGoal()
    
    # Initialize sprite groups
    playerSprite = pg.sprite.Group(player)
    itemSprites = pg.sprite.Group(sword)
    platformSprites = pg.sprite.Group(platforms)
    scrollingSprites = pg.sprite.RenderUpdates([lava]+[player,sword]+mobs+platforms+[goal])
    physicsSprites = pg.sprite.Group([player]+mobs)
    mobSprites = pg.sprite.Group(mobs)
    
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
        scrollingSprites.clear(screen,background)
        # Step physics
        engine.stepPhysics(physicsSprites)
        engine.stepMobAI(playerSprite,mobSprites)
        engine.stepPlayer(playerSprite)
        for sprite in physicsSprites.sprites():
            sprite.moveFromV()
            engine.collisionPlatform(sprite,platformSprites)
        # Check for collisions with mobs
        dead = engine.collisionMob(player,mobSprites)
        # Kill mobs in the lava
        pg.sprite.spritecollide(lava, mobSprites,1)
        # Scroll Screen
        charx = player.rect.centerx
        if charx < 0.2*varbs.screenW or charx > 0.7*varbs.screenW:
            dx = 0.4*varbs.screenW - charx
            for sprite in scrollingSprites.sprites():
                sprite.rect.move_ip(dx,0)
        # Update all sprites
        scrollingSprites.update()
        # Draw all sprites (via groups)
        dirty_rect = scrollingSprites.draw(screen)
        # Update display with new screen
        pg.display.update(dirty_rect)
        # Check for victory
        if pg.sprite.collide_rect(player,goal):
            print("YOU WIN!")
            return
        # Check for death
        if pg.sprite.collide_rect(player,lava) or dead:
            print("YOU DIED!")
            return


if __name__ == "__main__":
    main()
