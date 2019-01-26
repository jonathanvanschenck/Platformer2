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
    sword = initialize.initSword()
    player = initialize.initPlayer(sword)
    
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
    scrollingSprites = classes.RenderUpdatesSneaky([lava]+[player,sword]+mobs+platforms+[goal])
    physicsSprites = pg.sprite.Group([player]+mobs)
    mobSprites = pg.sprite.Group(mobs)
    
    # Blit everything to the screen
    screen.blit(background, (0,0))
    pg.display.update()
    
    # Initalize killcounter
    global killcounter
    killcounter = 0
    
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
                if event.key == K_SPACE:
                    player.setAttack(True)
            if event.type == KEYUP:
                if event.key == K_a:
                    player.setAccel(left=0.0)
                if event.key == K_d:
                    player.setAccel(right=0.0)
                if event.key == K_w:
                    player.jumpActive = True
                #if event.key == K_SPACE:
                #    player.setAttack(False)

        # Erase Player and platform location    
        scrollingSprites.clear(screen,background)
        # Step physics
        engine.stepPhysics(physicsSprites)
        engine.stepMobAI(playerSprite,mobSprites)
        engine.stepPlayer(playerSprite)
        for sprite in physicsSprites.sprites():
            sprite.moveFromV()
            engine.collisionPlatform(sprite,platformSprites)
        # Kill mobs in the lava
        pg.sprite.spritecollide(lava, mobSprites,1)
        # Kill mobs hit by sword
        if sword.visible:
            killcounter += len(pg.sprite.spritecollide(sword, mobSprites, 1))
        # Check for collisions with mobs
        dead, kc = engine.collisionMob(player,mobSprites)
        killcounter += kc
        # Scroll Screen
        charx = player.rect.centerx
        if charx < 0.39*varbs.screenW or charx > 0.41*varbs.screenW:
            dx = 0.4*varbs.screenW - charx
            for sprite in scrollingSprites.sprites():
                sprite.rect.move_ip(dx,0)
        if len(mobSprites.sprites()) < 2:
            newMob = classes.Mob(x = 1.3*varbs.screenW)
            mobSprites.add(newMob)
            physicsSprites.add(newMob)
            scrollingSprites.add(newMob)
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
        print("Purifications: ",killcounter)


if __name__ == "__main__":
    main()
