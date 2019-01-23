"""
Module holds the custom classes and sprites for game
"""
import sys
import os
import pygame as pg
import varbs
import numpy as np

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pg.error:
        print('Cannot load image:', fullname)
        raise(SystemExit)
    return image, image.get_rect()
def flipx(image):
    return pg.surfarray.make_surface(pg.surfarray.pixels3d(image)[::-1])

    
class Player(pg.sprite.Sprite):
    """Player sprite
    Returns: Player object
    Functions: update,
    Attributes: area, v
    """
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('walk02.png')
        self.loadGraphics()
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.rectO = self.rect.copy()
        self.area = screen.get_rect()
        self.v = np.array([0.0,0.0])
        self.contact = False
        self.accel = [0.0,0.0]
        self.jump = False
        self.doubleJump = True
        self.jumpActive = True
    
    def loadGraphics(self):
        self.walkImages = [[load_png('walk0'+str(j+1)+'.png')[0] for j in range(4)]]
        self.walkImages += [[flipx(j) for j in self.walkImages[0]]]
        self.walkingI = 0
        self.facingI = 0#R=0,L=1
        self.standImage = load_png('walk02.png')[0]
        self.fallImage = load_png('walk02.png')[1]
    
    def update(self):
        """Sets current position for next loop iteration
        """
        # Check which direction the character moved, update facing dir.
        if self.rectO.left < self.rect.left:
            self.facingI = 0#Right
        elif self.rectO.left > self.rect.left:
            self.facingI = 1#Left
        # Update position
        self.rectO = self.rect.copy()
        # Default sprite state
        self.image = self.walkImages[self.facingI][1]
        if self.contact:
            # Cycle through walk animation
            if sum(self.accel) != 0.0:
                self.walkingI += 1
                self.image = self.walkImages[self.facingI][self.walkingI%4]
        # Switch to falling sprite state
        elif self.v[1]>=0.0:
            self.image = self.walkImages[self.facingI][0]
            
        
    def moveFromV(self):
        """Steps position foward according to velocity and max velocity
        """
        self.v = np.array([sign(self.v[i])*min(abs(self.v[i]),varbs.playervmax[i]) for i in [0,1]])
        #print(self.v)
        self.rect = self.rect.move(int(self.v[0]),int(self.v[1]))
        
    def setAccel(self,left=None,right=None):
        if left != None:
            self.accel[0] = left
        if right != None:
            self.accel[1] = right
            
    def getAccel(self):
        accel = varbs.playerAccel*sum(self.accel)
        if self.contact and (accel == 0.0):
            fric = -varbs.playerFric*sign(self.v[0])
            if fric*sign(self.v[0]) < 0:
                accel = -self.v[0]
            else:
                accel = -varbs.playerFric*sign(self.v[0])
        return accel
            
    def jumpAttempt(self):
        if self.contact or (self.doubleJump):# and self.jumpActive):
            self.jump = True
    def jumpReset(self):
        self.jump = False
        if not self.contact:
           self.doubleJump = False
    def doubleJumpReset(self,state):
        if state:
            self.doubleJump = True
        
class Platform(pg.sprite.Sprite):
    """Platform sprite
    Returns: Platform object
    Functions: update,
    Attributes: area,
    """
    
    def __init__(self,dx=0,dy=0,openBottom=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((500,40))
        self.image.fill((0+100*openBottom,0+100*openBottom,0+100*openBottom))
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.rect.left += dx
        self.rect.bottom = screen.get_rect().bottom+dy
        self.area = screen.get_rect()
        self.openBottom = openBottom
        
    def update(self):
        pass

def sign(x):
    if x > 0.0:
        return 1
    elif x < 0.0:
        return -1
    return 0
