"""
module holds game variables
"""
screenH = 500
screenW = 1000

margin = 10

stageH = screenH - 2*margin
stageW = 2*screenW - 2*margin

framerate = 20

g = 5.0
playerAccel = 5.0
playerFric = 3.0
playervmax = [30.0,50.0]
playerJump = 40.0
playerJumpOn = 25.0
attackFrameLength = 5
stepFrameLength = 3

mobvmax = [30.0,50.0]
mobVision = stageW
mobSpeed = 10.0
