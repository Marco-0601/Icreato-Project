# initial_setup.py, write the initial setup code here

from userUtils import *
from main import *

''' sample initial setup
stageNoforChange=22
elementsIn22 = [1, 1, 1, 1, 1 ,0] # ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
elements = Elements()
elements.addStage(22, elementsIn22)
loginfoprint(printFilename,1,"start")
'''

''' sample initial setup for multiple stages
stageNoforChange=[22, 23]
elements = Elements()
elementsIn22 = [1, 1, 1, 1, 1 ,0]# ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
elements.addStage(22, elementsIn22) # to set element for stage_22 with FG change
elementsIn23 = [1, 1, 1, 1, 1 ,0] # ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
elements.addStage(23, elementsIn23) # to set element for stage_23 with FG and Cus change.
loginfoprint(printFilename,1,"start")
'''

##**##

# x=0
# y=0

# xboundary= screenWidth/2
# yboundary= screenHeight/2

# xmove_max=10

# state = 0

# cx1 = 2*xboundary/3
# cy1 = -yboundary-10
# cx2 = 0
# cy2 = -yboundary-10
# cx3 = -2*xboundary/3
# cy3 = -yboundary-10

# speed = 5

stageNoforChange=[109, 110, 111, 85, 88, 89, 90, 91, 92, 95, 97, 98]
elements = Elements()
elementsIn109 = [1, 1, 1, 1, 1, 0]
elements.addStage(109, elementsIn109)
elementsIn110 = [1, 1, 1, 1, 1, 0]
elements.addStage(110, elementsIn110)
elementsIn111 = [1, 1, 1, 1, 1, 0]
elements.addStage(111, elementsIn111)
elementsIn85 = [1, 1, 1, 1, 1, 0]
elements.addStage(85, elementsIn85)
elementsIn88 = [1, 1, 1, 1, 1, 0]
elements.addStage(88, elementsIn88)
elementsIn89 = [1, 1, 1, 1, 1, 0]
elements.addStage(89, elementsIn89)
elementsIn90 = [1, 1, 1, 1, 1, 0]
elements.addStage(90, elementsIn90)
elementsIn91 = [1, 1, 1, 1, 1, 0]
elements.addStage(91, elementsIn91)
elementsIn92 = [1, 1, 1, 1, 1, 0]
elements.addStage(92, elementsIn92)
elementsIn95 = [1, 1, 1, 1, 1, 0]
elements.addStage(95, elementsIn95)
elementsIn97 = [1, 1, 1, 1, 1, 0]
elements.addStage(97, elementsIn97)
elementsIn98 = [1, 1, 1, 1, 1, 0]
elements.addStage(98, elementsIn98)
loginfoprint(printFilename, 1, "start")

class pizza():
    xmove_max=10
    xboundary= screenWidth/2
    yboundary= screenHeight/2
    cx1 = 2*xboundary/3
    cx2 = 0
    cx3 = -2*xboundary/3
    xlocations = [cx1, cx2, cx3]

    def __init__(self, speed, xlocationIndex, arrangment):
        self.speed = speed
        self.ylocation = -self.yboundary-10
        self.xlocation = self.xlocations[xlocationIndex] #cx1/cx2/cx3
        self.arrangment = arrangment #list of 3 numbers

    def getHeadLocation(self):
        verified, headX, headY, w=GetStartLocation(currentStage,HEAD,0)
        verified, x, y =GetStartLocation(currentStage,FG, 0)
        return headX, headY, x, y

    def movePerson(self):
        '''move person+fg based on head position'''

        headX1, headY1, x1, y1 = self.getHeadLocation()

        xmove=headX1-x1
        if xmove > self.xmove_max:
            xmove=self.xmove_max
        elif xmove < -self.xmove_max:
            xmove=-self.xmove_max

        newx=max(-self.xboundary,min(x1+xmove,self.xboundary))
        setit = SetStartLocation(currentStage,FG, 0, newx, y1)
                
    def checkLocation(self):
        '''judge whether the player missed the ingredient'''
        if self.ylocation > self.yboundary+20: #different for each item
            set = setSingleScriptTransition(currentStage,2)

    def moveIngredient(self):
        '''make the ingredients change(move)'''
        self.ylocation += self.speed
        setit = SetStartLocation(currentStage,CG, self.arrangment[2], self.cx1, self.ylocation) #different for each level
        setit = SetStartLocation(currentStage,CG, self.arrangment[1], self.cx2, self.ylocation) #different for each level
        setit = SetStartLocation(currentStage,CG, self.arrangment[0], self.cx3, self.ylocation) #different for each level

    def checkGetIngredient(self):
        '''calculate distance, dis = sqrt((cx-newx)**2+(cy-y)**2)'''
        headX1, headY1, x1, y1 = self.getHeadLocation()

        distance = sqrt((self.xlocation-headX1)**2+(self.ylocation-headY1)**2) #different for each item

        '''check if got ingredient'''
        if distance < 100:
            set = setSingleScriptTransition(currentStage,1)

    def run(self):
        self.movePerson()
        self.checkLocation()
        self.moveIngredient()
        self.checkGetIngredient()

class salad():
    xmove_max=10
    xboundary= screenWidth/2
    yboundary= screenHeight/2
    cx1 = 3*xboundary/4
    cx2 = 1*xboundary/4
    cx3 = -1*xboundary/4
    cx4 = -3*xboundary/4
    xlocations = [cx1, cx2, cx3, cx4]

    def __init__(self, speed, xlocationIndex, arrangment):
        self.speed = speed
        self.ylocation = -self.yboundary-10
        self.xlocation = self.xlocations[xlocationIndex] #cx1/cx2/cx3/cx4
        self.arrangment = arrangment #list of 3 numbers

    def getHeadLocation(self):
       
        verified, headX, headY, w=GetStartLocation(currentStage,HEAD,0)
        verified, x, y =GetStartLocation(currentStage,FG, 0)
        return headX, headY, x, y

    def movePerson(self):
        '''move person+fg based on head position'''

        headX1, headY1, x1, y1 = self.getHeadLocation()

        xmove=headX1-x1
        if xmove > self.xmove_max:
            xmove=self.xmove_max
        elif xmove < -self.xmove_max:
            xmove=-self.xmove_max

        newx=max(-self.xboundary,min(x1+xmove,self.xboundary))
        setit = SetStartLocation(currentStage,FG, 0, newx, y1)
                
    def checkLocation(self):
        '''judge whether the player missed the ingredient'''
        if self.ylocation > self.yboundary+20: #different for each item
            set = setSingleScriptTransition(currentStage,2)

    def moveIngredient(self):
        '''make the ingredients change(move)'''
        self.ylocation += self.speed
        setit = SetStartLocation(currentStage,CG, self.arrangment[3], self.cx1, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[2], self.cx2, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[1], self.cx3, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[0], self.cx4, self.ylocation)

    def checkGetIngredient(self):
        '''calculate distance, dis = sqrt((cx-newx)**2+(cy-y)**2)'''
        headX1, headY1, x1, y1 = self.getHeadLocation()

        distance = sqrt((self.xlocation-headX1)**2+(self.ylocation-headY1)**2) #different for each item

        '''check if got ingredient'''
        if distance < 100:
            set = setSingleScriptTransition(currentStage,1)

    def run(self):
        self.movePerson()
        self.checkLocation()
        self.moveIngredient()
        self.checkGetIngredient()

class burger():
    xmove_max=10
    xboundary= screenWidth/2
    yboundary= screenHeight/2
    cx1 = 4*xboundary/5
    cx2 = 2*xboundary/5
    cx3 = 0
    cx4 = -2*xboundary/5
    cx5 = -4*xboundary/5
    xlocations = [cx1, cx2, cx3, cx4, cx5]

    def __init__(self, speed, xlocationIndex, arrangment):
        self.speed = speed
        self.ylocation = -self.yboundary-10
        self.xlocation = self.xlocations[xlocationIndex] #cx1/cx2/cx3/cx4
        self.arrangment = arrangment #list of 3 numbers

    def getHeadLocation(self):
        verified, headX, headY, w=GetStartLocation(currentStage,HEAD,0)
        verified, x, y =GetStartLocation(currentStage,FG, 0)
        return headX, headY, x, y

    def movePerson(self):
        '''move person+fg based on head position'''

        headX1, headY1, x1, y1 = self.getHeadLocation()

        xmove=headX1-x1
        if xmove > self.xmove_max:
            xmove=self.xmove_max
        elif xmove < -self.xmove_max:
            xmove=-self.xmove_max

        newx=max(-self.xboundary,min(x1+xmove,self.xboundary))
        setit = SetStartLocation(currentStage,FG, 0, newx, y1)
                
    def checkLocation(self):
        '''judge whether the player missed the ingredient'''
        if self.ylocation > self.yboundary+20: #different for each item
            set = setSingleScriptTransition(currentStage,2)

    def moveIngredient(self):
        '''make the ingredients change(move)'''
        self.ylocation += self.speed
        setit = SetStartLocation(currentStage,CG, self.arrangment[4], self.cx1, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[3], self.cx2, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[2], self.cx3, self.ylocation) 
        setit = SetStartLocation(currentStage,CG, self.arrangment[1], self.cx4, self.ylocation)
        setit = SetStartLocation(currentStage,CG, self.arrangment[0], self.cx5, self.ylocation)

    def checkGetIngredient(self):
        '''calculate distance, dis = sqrt((cx-newx)**2+(cy-y)**2)'''
        headX1, headY1, x1, y1 = self.getHeadLocation()

        distance = sqrt((self.xlocation-headX1)**2+(self.ylocation-headY1)**2) #different for each item

        '''check if got ingredient'''
        if distance < 100:
            set = setSingleScriptTransition(currentStage,1)

    def run(self):
        self.movePerson()
        self.checkLocation()
        self.moveIngredient()
        self.checkGetIngredient()