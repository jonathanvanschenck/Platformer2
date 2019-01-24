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
def flipxy(image):
    return pg.surfarray.make_surface(pg.surfarray.pixels3d(image)[::-1])
    
class Player(pg.sprite.Sprite):
    """Player sprite
    Returns: Player object
    Functions: update,
    Attributes: area, v
    """
    def __init__(self,sword=None):
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
        self.attacking = False
        self.sword = sword
        self.attackFrame = 0
    
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
        # Update position
        self.rectO = self.rect.copy()
        # Update sword visibility
        try:
            self.sword.visible = False
        except AttributeError:
            pass
        # Default sprite state
        self.image = self.walkImages[self.facingI][1]
        if self.contact:
            # Cycle through walk animation
            if sum(self.accel) != 0.0:
                self.walkingI += 1
                self.image = self.walkImages[self.facingI][(self.walkingI%(4*varbs.stepFrameLength))//varbs.stepFrameLength]
        # Switch to falling sprite state
        elif self.v[1]>=0.0:
            self.image = self.walkImages[self.facingI][0]
        # Force to lunge motion if attacking
        if self.attacking:
            self.image = self.walkImages[self.facingI][0]
            self.attackFrame += 1
            try:
                self.sword.visible = True
            except AttributeError:
                pass
            if self.attackFrame%varbs.attackFrameLength == 0:
                self.attackFrame = 1
                self.setAttack(False)
            
    def move(self,dx=0,dy=0):
        self.rect.move_ip(dx,dy)
        # Check which direction the character moved, update facing dir.
        if self.rectO.left < self.rect.left:
            self.facingI = 0#Right
        elif self.rectO.left > self.rect.left:
            self.facingI = 1#Left
        try:
            self.sword.image = self.sword.images[self.facingI]
            if self.facingI == 0:
                self.sword.rect.top = self.rect.top + self.sword.yoffset
                self.sword.rect.left = self.rect.left + self.sword.xoffset
            else:
                self.sword.rect.top = self.rect.top + self.sword.yoffset
                self.sword.rect.right = self.rect.right - self.sword.xoffset
        except AttributeError:
            pass
        
    def moveFromV(self):
        """Steps position foward according to velocity and max velocity
        """
        self.v = np.array([sign(self.v[i])*min(abs(self.v[i]),varbs.playervmax[i]) for i in [0,1]])
        #print(self.v)
        #self.rect = self.rect.move(int(self.v[0]),int(self.v[1]))
        self.move(int(self.v[0]),int(self.v[1]))
        
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
            
    def setAttack(self,attackBool):
        self.attacking = attackBool

class RenderUpdatesSneaky(pg.sprite.RenderUpdates):
    """Modification of .RenderUpdates which knows about sneaky sprites
    """
    def __init__(*args):
        pg.sprite.RenderUpdates.__init__(*args)
        

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            try:
                visible = s.visible
            except AttributeError:
                visible = True
            r = spritedict[s]
            if visible:
                newrect = surface_blit(s.image, s.rect)
            if r:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            else:
                dirty_append(newrect)
            spritedict[s] = newrect
        return dirty
        
class sneakySprite(pg.sprite.Sprite):
    """Sprite with 'visible' trait
    """
    def __init__(self,visible=1):
        pg.sprite.Sprite.__init__(self)
        self.__set_visible(visible)
        
    def __set_visible(self,visible):
        self.__visible = bool(visible)
        
    def __get_visible(self):
        return self.__visible
        
    visible = property(lambda self: self.__get_visible(),
                       lambda self, vis: self.__set_visible(vis),
                       doc="Sets if a sprite is visible (0/1)")
        


class PlayerItem(sneakySprite):
    """Player item sprite
    """
    
    def __init__(self,imagename,xoffset=30,yoffset=42,startVisible=False):
        sneakySprite.__init__(self)
        self.visible = startVisible
        self.image, self.rect = load_png(imagename)
        self.images = [self.image,flipx(self.image)]
        self.xoffset = xoffset
        self.yoffset = yoffset
        
    def update(self):
        pass
        
    #def move(self):
    #    self.rect.top += self.yoffset
    #    self.rect.left += self.xoffset

class Mob(pg.sprite.Sprite):
    """Mob sprite
    Returns: Player object
    Functions: update,
    Attributes: area, v
    """
    
    def __init__(self,x=100,y=100):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('walk02.png')
        self.loadGraphics()
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.rectO = self.rect.copy()
        self.area = screen.get_rect()
        self.v = np.array([0.0,0.0])
        self.contact = False
    
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
            if self.v[0] != 0.0:
                self.walkingI += 1
                self.image = self.walkImages[self.facingI][self.walkingI%4]
        # Switch to falling sprite state
        elif self.v[1]>=0.0:
            self.image = self.walkImages[self.facingI][0]
            
    def doubleJumpReset(self,arg):
        pass
    
    def move(self,dx=0,dy=0):
        self.rect.move_ip(dx,dy)
            
    def moveFromV(self):
        """Steps position foward according to velocity and max velocity
        """
        self.v = np.array([sign(self.v[i])*min(abs(self.v[i]),varbs.mobvmax[i]) for i in [0,1]])
        #print(self.v)
        #self.rect = self.rect.move(int(self.v[0]),int(self.v[1]))
        self.move(int(self.v[0]),int(self.v[1]))

            
            
class Platform(pg.sprite.Sprite):
    """Platform sprite
    Returns: Platform object
    Functions: update,
    Attributes: area,
    """
    
    def __init__(self,x=0,y=0,w=500,h=40,openBottom=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill((0+100*openBottom,0+100*openBottom,0+100*openBottom))
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.left += x
        self.rect.bottom = screen.get_rect().bottom - y
        self.area = screen.get_rect()
        self.openBottom = openBottom
        
    def update(self):
        pass
        
class Wall(pg.sprite.Sprite):
    """Platform sprite
    Returns: Platform object
    Functions: update,
    Attributes: area,
    """
    
    def __init__(self,x=0,y=0,w=40,h=1.5*varbs.screenH):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill((0,0,0))
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.left += x
        self.rect.bottom = screen.get_rect().bottom - y
        self.area = screen.get_rect()
        self.openBottom = False
        
    def update(self):
        pass
        
class Goal(pg.sprite.Sprite):
    """Platform sprite
    Returns: Platform object
    Functions: update,
    Attributes: area,
    """
    
    def __init__(self,x=0,y=40,w=20,h=0.9*varbs.screenH):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h-y))
        self.image.fill((100,100,0))
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.left += x
        self.rect.bottom = screen.get_rect().bottom - y
        self.area = screen.get_rect()
        self.openBottom = False
        
    def update(self):
        pass

class Lava(pg.sprite.Sprite):
    """Platform sprite
    Returns: Platform object
    Functions: update,
    Attributes: area,
    """
    
    def __init__(self,w=varbs.screenW):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,20))
        self.image.fill((250,0,0))
        screen = pg.display.get_surface()
        self.rect = self.image.get_rect()
        self.rect.left += screen.get_rect().left
        self.rect.bottom = screen.get_rect().bottom
        self.area = screen.get_rect()
        
    def update(self):
        pass
        
def sign(x):
    if x > 0.0:
        return 1
    elif x < 0.0:
        return -1
    return 0
