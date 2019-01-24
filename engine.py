"""
module holds game engine
"""
import numpy as np
import varbs
import pygame as pg


def stepPhysics(physicsSprites):
    for sprite in physicsSprites.sprites():
        sprite.v += np.array([0.0,varbs.g])
        
def stepPlayer(playerSprite):
    for sprite in playerSprite.sprites():
        vert = 0.0
        if sprite.jump:
            if not sprite.contact:
                sprite.v[1] = 0.0
            sprite.jumpReset()
            vert = -varbs.playerJump
        sprite.v += np.array([sprite.getAccel(),vert])

def stepMobAI(playerSprite,mobSprites):
    for sprite in mobSprites.sprites():
        dx = playerSprite.sprites()[0].rect.centerx - sprite.rect.centerx
        if abs(dx) < varbs.mobVision:
            sprite.v[0] = sign(dx)*varbs.mobSpeed
        else:
            sprite.v[0] = 0.0
        
def collisionPlatform(sprite,platformSprites):
    contact = False
    for platform in pg.sprite.spritecollide(sprite, platformSprites, 0):
        dx = collisionEdgeCorrection(sprite.rectO,sprite.rect,platform.rect)
        if platform.openBottom and dx[1] < 0.0:
            sprite.move(dx[0],dx[1])
            contact = True
            sprite.v[1] = 0.0
        elif not platform.openBottom:
            sprite.move(dx[0],dx[1])
            if dx[0] != 0.0:
                sprite.v[0] = 0.0
            if dx[1] != 0.0:
                sprite.v[1] = 0.0
            if dx[1] < 0.0:
                contact = True
    sprite.contact = contact
    sprite.doubleJumpReset(contact)
    
def collisionMob(sprite,mobSprites):
    for mSprite in pg.sprite.spritecollide(sprite, mobSprites, 0):
        dx = collisionEdgeCorrection(sprite.rectO,sprite.rect,mSprite.rect)
        if dx[1] < 0.0:
            sprite.move(dx[0],dx[1])
            sprite.contact = True
            sprite.v[1] = -varbs.playerJumpOn
            mSprite.kill()
        else:
            return True
        sprite.doubleJumpReset(sprite.contact)
    return False
    
def edgeReaction(p1,p2,corners):
    dc = [[c[0]-p2[0],c[1]-p2[1]] for c in corners]
    thc = np.array([np.arctan2(-c[1],c[0]) for c in dc])
    thx = (np.arctan2(p2[1]-p1[1],p1[0]-p2[0])-thc[0]+1.9999*np.pi)%(2*np.pi)
    thc = (thc-thc[0]+1.9999*np.pi)%(2*np.pi)
    for i in range(1,4):
        if thx > thc[i]:
            return i-1
    else:
        return 3  
reaction = np.array([[0,-1],[1,0],[0,1],[-1,0]])
edgePosPlat = [lambda x: x.top,lambda x: x.right,lambda x: x.bottom,lambda x: x.left]
edgePosSprit = [lambda x: x.bottom,lambda x: x.left,lambda x: x.top,lambda x: x.right]
def collisionEdgeCorrection(oM1,oM2,oS):
    p1 = np.array([oM1.centerx,oM1.centery])
    p2 = np.array([oM2.centerx,oM2.centery])
    cS =  np.array([[ oS.left, oS.top],[ oS.right, oS.top],[ oS.right, oS.bottom],[ oS.left, oS.bottom]])
    i = edgeReaction(p1,p2,cS)
    return reaction[i]*abs(edgePosPlat[i](oS)-edgePosSprit[i](oM2))
def sign(x):

    if x > 0.0:
        return 1
    elif x < 0.0:
        return -1
    return 0
