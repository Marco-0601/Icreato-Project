# this is a stage_89.py file

from userUtils import *
from main import *
from initial_setup import *

''' Function description

'''

# use BG, FG, CUS or Person?

##**##
'''Do not change any code above this line'''
'''pepperoni'''
# verified, headX, headY, w=GetStartLocation(currentStage,HEAD,0)
# verified, x, y =GetStartLocation(currentStage,FG, 0)
# speed = 7

# if state==0:
#     '''move person+fg based on head position'''
#     xmove=headX-x

#     if xmove > xmove_max:
#         xmove=xmove_max
#     elif xmove < -xmove_max:
#         xmove=-xmove_max

#     newx=max(-xboundary,min(x+xmove,xboundary))
#     SetStartLocation(currentStage,FG, 0, newx, y)

#     '''judge whether the player missed the ingredient'''
#     if cy1 > yboundary+20:
#         setSingleScriptTransition(currentStage,2)

#     '''make the ingredients change(move)'''
#     cy1 += speed
#     cy2 += speed
#     cy3 += speed
#     SetStartLocation(currentStage,CG, 0, cx1, cy1)
#     SetStartLocation(currentStage,CG, 1, cx2, cy2)
#     SetStartLocation(currentStage,CG, 2, cx3, cy3)

#     '''calculate distance, dis = sqrt((cx-newx)**2+(cy-y)**2)'''
#     distance = sqrt((cx1-headX)**2+(cy1-headY)**2)

#     '''check if got ingredient'''
#     if distance < 100:
#         state = 1
#         cx1 = 2*xboundary/3
#         cy1 = -yboundary-10
#         cx2 = 0
#         cy2 = -yboundary-10
#         cx3 = -2*xboundary/3
#         cy3 = -yboundary-10

# else:
#     setSingleScriptTransition(currentStage,1)

get, timeIndex=GetTimeIndex(currentStage)

if timeIndex==1:    
    bottomBun = pizza(7,0,[2,1,0])

bottomBun.run()