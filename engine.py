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
        
def collisionPlatform(sprite,platformSprites):
    contact = False
    for platform in pg.sprite.spritecollide(sprite, platformSprites, 0):
        dx = collisionEdgeCorrection(sprite.rectO,sprite.rect,platform.rect)
        if platform.openBottom and dx[1] < 0.0:
            sprite.rect = sprite.rect.move(dx[0],dx[1])
            contact = True
            sprite.v[1] = 0.0
        elif not platform.openBottom:
            sprite.rect = sprite.rect.move(dx[0],dx[1])
            if dx[0] != 0.0:
                sprite.v[0] = 0.0
            if dx[1] != 0.0:
                sprite.v[1] = 0.0
            if dx[1] < 0.0:
                contact = True
    sprite.contact = contact
    sprite.doubleJumpReset(contact)
    
            

def collisionEdgeCorrection2(oM1,oM2,oS):
    cM1 = np.array([[oM1.left,oM1.top],[oM1.right,oM1.top],[oM1.right,oM1.bottom],[oM1.left,oM1.bottom]])
    print(cM1)
    cM2 = np.array([[oM2.left,oM2.top],[oM2.right,oM2.top],[oM2.right,oM2.bottom],[oM2.left,oM2.bottom]])
    print(cM2)
    cS =  np.array([[ oS.left, oS.top],[ oS.right, oS.top],[ oS.right, oS.bottom],[ oS.left, oS.bottom]])
    print(cS)
    cornerIn = [bool(oS.collidepoint(cM2[i][0],cM2[i][1])) for i in range(4)]
    print(cornerIn)
    res = np.array([0,0])
    maxsum = sum(res)
    for i in np.arange(4)[cornerIn]:
        p1 = cM1[i]
        p2 = cM2[i]
        print(i)
        res1 = edgeReaction(p1,p2,cS)
        print(res1)
        if np.sum(np.abs(res1)) > maxsum:
            maxsum = 1*np.sum(np.abs(res1))
            res = 1*res1
    return res

reaction = np.array([[0,-1],[1,0],[0,1],[-1,0]])
def edgeReaction2(p1,p2,corners):
    dc = [[c[0]-p2[0],c[1]-p2[1]] for c in corners]
    #dc = list(map(lambda c: [c[0]-p2[0],c[1]-p2[1]],corners))
    thc = list(map(lambda c: np.arctan2(-c[1],c[0]),dc))
    thx = np.arctan2(p2[1]-p1[1],p1[0]-p2[0])
    print(thx)
    print(thc)
    print(dc)
    if thx > thc[0]:
        return reaction[3]*np.dot(reaction[3],dc[3])
    for i in range(1,4):
        if thx > thc[i]:
            return reaction[i-1]*np.dot(reaction[i-1],dc[i])
    else:
        return reaction[3]*np.dot(reaction[3],dc[3])
        
def edgeReaction3(p1,p2,corners):
    dc = [[c[0]-p2[0],c[1]-p2[1]] for c in corners]
    thc = np.array([np.arctan2(-c[1],c[0]) for c in dc])
    thx = (np.arctan2(p2[1]-p1[1],p1[0]-p2[0])-thc[0]+1.9999*np.pi)%(2*np.pi)
    thc = (thc-thc[0]+1.9999*np.pi)%(2*np.pi)
    print(thx)
    print(thc)
    print(dc)
    for i in range(1,4):
        if thx > thc[i]:
            return reaction[i-1]*np.dot(reaction[i-1],dc[i])
    else:
        return reaction[3]*np.dot(reaction[3],dc[3])    
        
def collisionEdgeCorrection3(oM1,oM2,oS):
    p1 = np.array([oM1.centerx,oM1.centery])
    print(p1)
    p2 = np.array([oM2.centerx,oM2.centery])
    print(p2)
    cS =  np.array([[ oS.left, oS.top],[ oS.right, oS.top],[ oS.right, oS.bottom],[ oS.left, oS.bottom]])
    print(cS)
    return edgeReaction(p1,p2,cS)
    
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
