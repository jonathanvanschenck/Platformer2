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
    # Create holes
    holes = [   0,   0,
              300, 500,
              900,1200,
             1500,1900,
             varbs.stageW]
    # Create the floor
    res = [classes.Platform(x=holes[2*i+1],w=holes[2*i+2]-holes[2*i+1]) for i in range(len(holes)//2)]
    # Create left wall
    res += [classes.Wall()]
    # Create right wall
    res += [classes.Wall(x=varbs.stageW)]
    # Create platforms
    res += [classes.Platform(x=200,y=300,openBottom=True)]
    return res
    
def initLava():
    return classes.Lava(w=varbs.stageW)
    
def initGoal():
    return classes.Goal(x=varbs.stageW-50-varbs.screenW)
