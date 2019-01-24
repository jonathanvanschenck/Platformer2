"""
module holds game initalization methods
"""
import pygame as pg
import varbs
import classes

def initPlayer(sword = None):
    """Initalizes player
    """
    return classes.Player(sword)
    
def initSword(startVisible = False):
    """Initalizes sword
    """
    return classes.PlayerItem("sword.png",startVisible=startVisible)
    
def initMobs():
    """Initalizes player
    """
    return [classes.Mob()]
    
def initPlatforms():
    """Populates the world with plaforms and walls
    """
    # Create the floor
    res = [classes.Platform(w=varbs.screenW-200),
           classes.Platform(x=varbs.screenW,w=varbs.stageW-varbs.screenW)]
    # Create left wall
    res += [classes.Wall()]
    # Create right wall
    res += [classes.Wall(x=varbs.stageW)]
    # Create platforms
    res += [classes.Platform(x=200,y=-300,openBottom=True)]
    return res
    
def initLava():
    return classes.Lava(w=varbs.stageW)
    
def initGoal():
    return classes.Goal(x=varbs.stageW-50)
