"""
userUtils.py
This file is to defined the basic functions to interface with iCreatorData.py
version 1.0 on 1/1/2022
a. defined the basic functions.
version 1.1 on 1/11/2022
a. Add ObjNo and BGNo in elements definition
version 1.2 on 1/24/2022
a. change setSingleScriptTransition, make sure ScriptCondNum matches
version 1.3 on 1/28/2022
a. fix a bug in decreaseGoodyNum, goodynumlist --> goodyNumList
version 1.4 on 3/17/2022
a. add comments for return value
version 1.5 on 5/4/2022
a. change variable for GetTime() function to avoid confusion
version 1.6 on 10/24/2022
a. add plotDebug to make debug easier.
version 1.7 on 11/22/2022
a. add clearScriptTransition and SetGoodyNumByName
version 1.8 on 11/30/2022
a. add function playSound(soundSrc, status, loop, delay, volume, repeatTimes, repeatIntervalTime):
version 1.9 on 12/7/2022
a. set ScriptConditionNo and GoodyNo to maximum, when they are active
version 1.10 on 4/4/2023
a. add description for GetStartLocation for first and second person head, left hand, and right hand
version 1.11 on 10/27/2023
a. add StageElement class and  StageInfo class
version 1.12 on 01/26/2024
a. support icamera web
version 1.13 on 4/9/2024
a. fix issue related to Goody only seeing the first index, replace GoodyIni.goodyNo with MAX_INFO_ENTITIES
b. add decreaseGoodyNumWithInterval and increaseGoodyNumWithInterval to reduce the sensitivity of goody count
c. when decreaseGoody or setGoodyNumbyName, cap the minimum goody number to zero to avoid error in system
"""

from main import dirName
from main import os
from main import currentStage
from main import time
from main import ScriptIni
from main import FGInfoIni
from main import BGInfoIni
from main import CUSInfoIni
from main import BodyPosIni
from main import firstTimeIni
from main import stageInitime
from main import stageEnterTime
from main import InfoInputNo2
from main import InfoInputNo
from main import GoodyIni
from main import goodynumlist
from main import OBJInfoIni
from main import MAX_INFO_ENTITIES
from main import dirName
from main import printFilename
from main import debug

##**##

import sys
from math import *
from random import *

FG = 1
BG = 2
CG = 3
HAND = 4
HEAD = 4
OBJ = 5
OBJT = 6
goodyLastTime=0


class Logger(object):
    def __init__(self, filename="default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def loginfoprint(printFilename, firstTime, contentStr):
    contentStr = contentStr + "\n"
    if firstTime == 0:
        f = open(printFilename, "w")
        f.close()
    elif firstTime > 0:
        f = open(printFilename, "a")
        f.write(contentStr)
        f.close()


loginfoprint(printFilename, 0, "start")
loginfoprint(printFilename, 1, "start")

filename = os.path.join(dirName, "handgesture.py")

if os.path.isfile(filename):
    from handgesture import gestureOfHand

    def gestureRecognize(gestureslist):
        """
        return [verified, gestureLabel, confidenceLevel] Determine gesture based on gesture array
        gestureslist is a gesture array, contain hand gestures
        """
        labelnums = []
        for label in range(7):
            labelnums.append(gestureslist.count(label))

        Labelnummax = max(labelnums)
        # print(gestureslist)
        # print(labelnums)
        # print('max quantity is :\t', Labelnummax)
        confidenceLevel = Labelnummax / len(gestureslist)
        if Labelnummax > int(len(gestureslist) * 0.8):
            return True, labelnums.index(Labelnummax), confidenceLevel
        else:
            return False, -1, 0

    def gameJudge(hand1, hand2):  # first arg is label of first hand, return 0 as winner
        """
        return [winnerID] Judge the outcome
        USER = 0
        VITURE = 1
        NOWINNER = -1
        0 for open hand gesture
        1 for close hand gesture
        2 for scissor gesture
        """
        if (
            ((hand1 == 0) and (hand2 == 1))
            or ((hand1 == 1) and (hand2 == 2))
            or ((hand1 == 2) and (hand2 == 0))
        ):
            winner = 0
        elif (
            ((hand2 == 0) and (hand1 == 1))
            or ((hand2 == 1) and (hand1 == 2))
            or ((hand2 == 2) and (hand1 == 0))
        ):
            winner = 1
        else:
            winner = -1
        return winner

    def recognizeGesture(StageID, ObjID, handID, timePeriod):
        """
        return [verified, GestureId, confidenceLevel] recognize hand gesture in a period, for example 0.1 second.
        ObjID is person number, ex. 1- person1, 2-person2
        handID is the hand number, ex. 0-leftHand, 1-rightHand
        confidenceLevel is the percentage confidence of that gesture
        timePeriod is the time period for gesture recognition
        GestureID is the gesture type:
        0 for open hand gesture
        1 for close hand gesture
        2 for scissor gesture
        3 for Ok pose hand gesture
        4 for spiderman pose hand
        5 for gun gesture
        6 for others"""

        if currentStage != StageID:
            verified = False
            confidenceLevel = 0
            Gestured = -1
        else:
            gestures = []
            t0 = time()
            # while time() < (t0 + timePeriod) and len(gestures)<500:
            while time() < (t0 + timePeriod) or len(gestures) < 30:
                handgestureTem = gestureOfHand(ObjID, handID)
                # contentStr = "time="+str(time()-t0)[0:5]+"\t handgestureTem\t " + str(handgestureTem)
                # loginfoprint(printFilename,1,contentStr)
                if -1 < handgestureTem < 7:
                    gestures.append(handgestureTem)
            # gestures = gestures[-len(gestures)//2: -1]

            verified, Gestured, confidenceLevel = gestureRecognize(gestures)

        return verified, Gestured, confidenceLevel


# setScriptTransition(StageID, transitionNo, scriptNo)
# '''
# one script multiple transitions
# '''
#     if  currentStage != StageID:
#         pass
#     else:
#         ScriptIni.verified[scriptNo] = 1
#         ScriptIni.ScriptCondition[scriptNo] = 1


def clearScriptTransition(ScriptIni1):
    for i in range(MAX_INFO_ENTITIES):
        ScriptIni1.verified[i] = 0


def setSingleScriptTransition(StageID, scriptNo):
    """
    return [verified] set single script transition
    StageID     id of stage
    scriptNo    1,2,3
    """

    if currentStage != StageID:
        pass
        verified = False
    else:
        i = 0
        verified = False
        while (i < MAX_INFO_ENTITIES) and not verified:
            # print ("set transition, loop, i="+str(i)+ ",MAX_INFO_ENTITIES="+str(MAX_INFO_ENTITIES) )
            if ScriptIni.ScriptCondNum[i] == scriptNo:
                ScriptIni.verified[i] = 1
                ScriptIni.ScriptCondition[i] = 1
                # print ("set transition achieved, i="+str(i)+",scriptNo="+str(scriptNo))
                verified = True
            i += 1
    return verified


# def ScaleChange(StageID, ObjID, itemID, timeArray, xScaleAry, yScaleAry):
#     '''
#     Set continuous changes in scale
#     StageID     id of stage
#     ObjID
#         1 for FrontGraph
#         2 for Background Graph
#         3 for Custom Graph

#     itemID      the number of item, for example 0,1,2
#     timeArray   a list contains time, for example [0.5],[0.1, 0.2]
#     xScaleAry   a list contains xScale, corresponds to the time array
#     yScaleAry   a list contains yScale, corresponds to the time array
#     '''
#     if  currentStage != StageID:
#         pass
#         verified = False
#     else:
#         # flag, timeIndex = GetTimeIndex(StageID)
#         flag, time_in = GetTime(StageID)
#         if time_in < timeArray[0]:
#             xscale = xScaleAry[0]
#             yscale = yScaleAry[0]
#         elif time_in >= timeArray[-1]:
#             xscale = xScaleAry[-1]
#             yscale = yScaleAry[-1]
#         else:
#             for index in range(0,len(timeArray)-1):
#                 if timeArray[index]<=time_in<timeArray[index+1]:
#                     xscale = xScaleAry[index] + (xScaleAry[index+1]-xScaleAry[index]) / (timeArray[index+1]-timeArray[index]) * (time_in-timeArray[index])
#                     yscale = yScaleAry[index] + (yScaleAry[index+1]-yScaleAry[index]) / (timeArray[index+1]-timeArray[index]) * (time_in-timeArray[index])

#         if ObjID == 1:  # Front Graph
#             FGInfoIni.FGInfo[itemID].xscale = xscale
#             FGInfoIni.FGInfo[itemID].yscale = yscale
#             FGInfoIni.verified[itemID] = 1
#         elif ObjID == 2:  # Background Graph
#             BGInfoIni.BGInfo[itemID].xscale = xscale
#             BGInfoIni.BGInfo[itemID].yscale = yscale
#             BGInfoIni.verified[itemID] = 1
#         elif ObjID == 3:  # Custom Graph
#             CUSInfoIni.CUSInfo[itemID].xscale = xscale
#             CUSInfoIni.CUSInfo[itemID].yscale = yscale
#             CUSInfoIni.verified[itemID] = 1
#         # contentStr = "time="+ str(time_in)[0:5]+ "stageEnterTime="+ str(stageEnterTime)+"scale="+str(xscale)
#         # loginfoprint(printFilename,1,contentStr)
#         verified = True
#     # print('new func run \n')
#     return verified


def ScaleChange(StageID, ObjID, itemID, xScale, yScale):
    """
    return [verified] change scale of picture
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph
    xScale   scale of x
    yScale   scale of y
    """
    if currentStage != StageID:
        pass
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            FGInfoIni.FGInfo[itemID].xscale = xScale
            FGInfoIni.FGInfo[itemID].yscale = yScale
            FGInfoIni.verified[itemID] = 1
        elif ObjID == 2:  # Background Graph
            BGInfoIni.BGInfo[itemID].xscale = xScale
            BGInfoIni.BGInfo[itemID].yscale = yScale
            BGInfoIni.verified[itemID] = 1
        elif ObjID == 3:  # Custom Graph
            CUSInfoIni.CUSInfo[itemID].xscale = xScale
            CUSInfoIni.CUSInfo[itemID].yscale = yScale
            CUSInfoIni.verified[itemID] = 1
        # contentStr = "time="+ str(time_in)[0:5]+ "stageEnterTime="+ str(stageEnterTime)+"scale="+str(xscale)
        # loginfoprint(printFilename,1,contentStr)
        verified = True
    # print('new func run \n')
    return verified


# def TransparencyChange(StageID, ObjID, itemID, timeArray, transparencyAry):
#     '''
#     Set continuous changes in transparency
#     StageID     id of stage
#     ObjID
#         1 for FrontGraph
#         2 for Background Graph
#         3 for Custom Graph

#     itemID      the number of item, for example 0,1,2
#     timeArray   a list contains time, for example [0.5],[0.1, 0.2]
#     transparencyAry 1-alphaNor, for example [0.8],[0.6, 0.2]
#     '''
#     if  currentStage != StageID:
#         pass
#         verified = False
#     else:
#         # flag, timeIndex = GetTimeIndex(StageID)
#         flag, time_in = GetTime(StageID)
#         # time_second = (timeIndex-eval("timeIndex_enter"+str(StageID))) / 30
#         if time_in < timeArray[0]:
#             transparency = transparencyAry[0]
#         elif time_in >= timeArray[-1]:
#             transparency = transparencyAry[-1]
#         else:
#             for index in range(0,len(timeArray)-1):
#                 if timeArray[index]<=time_in<timeArray[index+1]:
#                     transparency = transparencyAry[index] + (transparencyAry[index+1] - transparencyAry[index] ) / (timeArray[index+1] - timeArray[index]) * (time_in - timeArray[index])
#         if ObjID == 1:  # Front Graph
#             FGInfoIni.FGInfo[itemID].alphaNor = 1-transparency
#             FGInfoIni.verified[itemID] = 1
#         elif ObjID == 2:  # Background Graph
#             BGInfoIni.BGInfo[itemID].alphaNor = 1-transparency
#             BGInfoIni.verified[itemID] = 1
#         elif ObjID == 3:  # Custom Graph
#             CUSInfoIni.CUSInfo[itemID].alphaNor = 1-transparency
#             CUSInfoIni.verified[itemID] = 1

#         verified = True
#     return verified


def TransparencyChange(StageID, ObjID, itemID, transparency):
    """
    return [verified] changes transparency of picture
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph

    itemID      the number of item, for example 0,1,2
    transparencyAry 1-alphaNor, for example 0.8, 0.2
    """
    if currentStage != StageID:
        pass
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            FGInfoIni.FGInfo[itemID].alphaNor = 1 - transparency
            FGInfoIni.verified[itemID] = 1
        elif ObjID == 2:  # Background Graph
            BGInfoIni.BGInfo[itemID].alphaNor = 1 - transparency
            BGInfoIni.verified[itemID] = 1
        elif ObjID == 3:  # Custom Graph
            CUSInfoIni.CUSInfo[itemID].alphaNor = 1 - transparency
            CUSInfoIni.verified[itemID] = 1

        verified = True
    return verified


def SetStartLocation(StageID, ObjID, itemID, xstart, ystart):
    """
    return [verified] set the position of one item
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph

    itemID      the number of item, for example 0,1,2
    xstart      the x of item
    ystart      the y of item

    """
    if currentStage != StageID:
        pass
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            FGInfoIni.FGInfo[itemID].xstart = xstart
            FGInfoIni.FGInfo[itemID].ystart = ystart
            FGInfoIni.verified[itemID] = 1
        elif ObjID == 2:  # Background Graph
            BGInfoIni.BGInfo[itemID].xstart = xstart
            BGInfoIni.BGInfo[itemID].ystart = ystart
            BGInfoIni.verified[itemID] = 1
        elif ObjID == 3:  # Custom Graph
            CUSInfoIni.CUSInfo[itemID].xstart = xstart
            CUSInfoIni.CUSInfo[itemID].ystart = ystart
            CUSInfoIni.verified[itemID] = 1
        elif ObjID == 5:  # Obj
            OBJInfoIni.OBJInfo[itemID].xstart = xstart
            OBJInfoIni.OBJInfo[itemID].ystart = ystart
            OBJInfoIni.verified[itemID] = 1
        verified = True
    return verified


def SetStartrotAngle(StageID, ObjID, itemID, rotAngle):
    """
    return [verified] Set rotate angle of picture.
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph

    itemID      the number of item, for example 0,1,2
    rotAngle    number of angle
    """
    if currentStage != StageID:
        pass
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            FGInfoIni.FGInfo[itemID].rotAngle = rotAngle
            FGInfoIni.verified[itemID] = 1
        elif ObjID == 2:  # Background Graph
            BGInfoIni.BGInfo[itemID].rotAngle = rotAngle
            BGInfoIni.verified[itemID] = 1
        elif ObjID == 3:  # Custom Graph
            CUSInfoIni.CUSInfo[itemID].rotAngle = rotAngle
            CUSInfoIni.verified[itemID] = 1
        verified = True
    return verified


# def SetStartLocationByTime(StageID, ObjID, itemID, timeArray, xAry, yAry):
#     '''
#     Set continuous changes in position
#     StageID     id of stage
#     ObjID
#         1 for FrontGraph
#         2 for Background Graph
#         3 for Custom Graph

#     itemID      the number of item, for example 0,1,2
#     timeArray   a list contains time, for example [0.5],[0.1, 0.2]
#     xAry        a list contains x of position
#     yAry        a list contains y of position

#     '''
#     x=0
#     y=0
#     if  currentStage != StageID:
#         pass
#         verified = False
#     else:
#         flag, time_in = GetTime(StageID)
#         if time_in < timeArray[0]:
#             x = xAry[0]
#             y = yAry[0]
#         elif time_in >= timeArray[-1]:
#             x = xAry[-1]
#             y = yAry[-1]
#         else:
#             for index in range(0,len(timeArray)-1):
#                 if timeArray[index]<=time_in<timeArray[index+1]:
#                     x = xAry[index] + (xAry[index+1]-xAry[index]) / (timeArray[index+1]-timeArray[index]) * (time_in-timeArray[index])
#                     y = yAry[index] + (yAry[index+1]-yAry[index]) / (timeArray[index+1]-timeArray[index]) * (time_in-timeArray[index])
#                     #print ("set location time="+str(time_in)+",x="+str(x)+",y="+str(y))
#         if ObjID == 1:  # Front Graph
#             FGInfoIni.FGInfo[itemID].xstart = x
#             FGInfoIni.FGInfo[itemID].ystart = y
#             FGInfoIni.verified[itemID] = 1
#         elif ObjID == 2:  # Background Graph
#             BGInfoIni.BGInfo[itemID].xstart = x
#             BGInfoIni.BGInfo[itemID].ystart = y
#             BGInfoIni.verified[itemID] = 1
#         elif ObjID == 3:  # Custom Graph
#             CUSInfoIni.CUSInfo[itemID].xstart = x
#             CUSInfoIni.CUSInfo[itemID].ystart = y
#             CUSInfoIni.verified[itemID] = 1
#         verified = True
#     return verified, x, y


def GetStartLocation(StageID, ObjID, itemID):
    """
    return [verified,x,y] return position of item
    return [verified,x,y,w] return position of head or hand with confidence level
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph
        4 for hand gesture from system
        FG = 1
        BG = 2
        CG = 3
        HAND = 4
        HEAD = 4
    itemID      the number of item, for example 0,1,2
    for first person head, objID=4, itemID=0
    for first person left hand, objID=4, itemID=1
    for first person right hand, objID=4, itemID=2
    for second person head, objID=4, itemID=24
    for second person left hand, objID=4, itemID=25
    for second person right hand, objID=4, itemID=26
    confidence, w=12, open hand, w=13, close hand, w=14, Lasso hand


    """
    if currentStage != StageID:
        pass
        x, y = 0, 0
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            x = FGInfoIni.FGInfo[itemID].xstart
            y = FGInfoIni.FGInfo[itemID].ystart
        elif ObjID == 2:  # Background Graph
            x = BGInfoIni.BGInfo[itemID].xstart
            y = BGInfoIni.BGInfo[itemID].ystart
        elif ObjID == 3:  # Custom Graph
            x = CUSInfoIni.CUSInfo[itemID].xstart
            y = CUSInfoIni.CUSInfo[itemID].ystart
        elif ObjID == 5:  # Obj
            x = OBJInfoIni.OBJInfo[itemID].xstart
            y = OBJInfoIni.OBJInfo[itemID].ystart
        elif ObjID == 4:  # Hand Graph
            x = BodyPosIni.BodyActPos[itemID].x  # left hand
            y = BodyPosIni.BodyActPos[itemID].y  # right hand
            w = BodyPosIni.BodyActPos[
                itemID
            ].w  # confidence, w=12, open hand, w=13, close hand, w=14, Lasso hand
            verified = True
            return verified, x, y, w
        verified = True
    return verified, x, y


def GetStartScale(StageID, ObjID, itemID):
    """
    return [verified,xscale,yscale] return scale of item
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph

    itemID      the number of item, for example 0,1,2

    """
    if currentStage != StageID:
        xscale, yscale = 0, 0
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            xscale = FGInfoIni.FGInfo[itemID].xscale
            yscale = FGInfoIni.FGInfo[itemID].yscale
        elif ObjID == 2:  # Background Graph
            xscale = BGInfoIni.BGInfo[itemID].xscale
            yscale = BGInfoIni.BGInfo[itemID].yscale
        elif ObjID == 3:  # Custom Graph
            xscale = CUSInfoIni.CUSInfo[itemID].xscale
            yscale = CUSInfoIni.CUSInfo[itemID].yscale
        verified = True
    return verified, xscale, yscale


def GetStartTransparency(StageID, ObjID, itemID):
    """
    return [verified,Transparency] of item
    StageID     id of stage
    ObjID
        1 for FrontGraph
        2 for Background Graph
        3 for Custom Graph

    itemID      the number of item, for example 0,1,2
    Transparency = 1 - alphaNor
    """
    if currentStage != StageID:
        Transparency = 1
        verified = False
    else:
        if ObjID == 1:  # Front Graph
            Transparency = 1 - FGInfoIni.FGInfo[itemID].alphaNor
        elif ObjID == 2:  # Background Graph
            Transparency = 1 - BGInfoIni.BGInfo[itemID].alphaNor
        elif ObjID == 3:  # Custom Graph
            Transparency = 1 - CUSInfoIni.CUSInfo[itemID].alphaNor
        verified = True
    return verified, Transparency


def GetTimeIndex(StageID):
    """
    return [verified, TimeIndex] in a stage
    StageID     id of stage
    """
    if currentStage != StageID:
        TimeIndex = 0
        verified = False
    else:
        TimeIndex = firstTimeIni - stageInitime
        verified = True
    return verified, TimeIndex


def GetTime(StageID):
    """
    return [verified, t] in a stage
    StageID     id of stage
    """
    if currentStage != StageID:
        Time = 0
        verified = False
    else:
        Time = time() - stageEnterTime
        verified = True
    return verified, Time


def SetElementNumber(elements, currentStage):
    """
    set element number of different stage into elements class.
    elements a dictionary contains all elements for stages being control
        value is a list, list elements are ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber
    currentStage     id of stage
    """
    ele = elements.ElementsDict

    if not (str(currentStage) in ele):
        return
    elementslist = ele[str(currentStage)]
    if elementslist[0] > 0:
        # InfoInputNo2.ScriptConditionNo=elementslist[0]
        InfoInputNo2.ScriptConditionNo = (
            4  # set maximum ScriptConditionNo as 4, when this element is selected
        )
    else:
        InfoInputNo2.ScriptConditionNo = 0

    if elementslist[1] > 0:
        # InfoInputNo2.GoodyNo=elementslist[1]
        InfoInputNo2.GoodyNo = (
            4  # set maximum GoodyNo as 4, when this element is selected
        )
    else:
        InfoInputNo2.GoodyNo = 0

    InfoInputNo.FGNo = elementslist[2]
    InfoInputNo.CUSNo = elementslist[3]
    length1 = len(elementslist)
    if length1 > 4:  # make it compatible to old version
        InfoInputNo.OBJNo = elementslist[4]
        InfoInputNo.BGNo = elementslist[5]
    InfoInputNo.stageNo = currentStage


class Elements:
    """
    a class storing element number
    """

    def __init__(self):
        self.ElementsDict = {}

    def addStage(self, stageNo, elementNoList):
        self.ElementsDict[str(stageNo)] = elementNoList


# def GetStartGoodyNum(StageID, GoodyNo):
#     '''
#     GoodyNo
#         1 or 2 mean first or second


#     '''
#     if  currentStage != StageID or GoodyNo>(GoodyIni.goodyNo):
#         GoodyNum = 0
#         verified = False
#         goody = 0
#     else:
#         # goody=[]
#         # for i in range(8):
#         #     GoodyNum = GoodyIni.GoodyInfo[i].initNum
#         #     goody.append(GoodyNum)
#         goody = GoodyIni.GoodyInfo[GoodyNo].initNum
#         verified = True
#     return verified,goody
def getString(cTypeName):
    """
    return [stringName] return a string of goody name
    """
    stringName = "".join([chr(i) for i in cTypeName]).rstrip("\x00")
    return stringName


def GetGoodyNumList(goodyNumList, modifyByUser):
    """
    return from input goodyNumList, a list contain all the goody num
    and a list represent goody modify by user, goody number modified by user
    need be set always
    goodyNumList    number of all goody
    modifyByUser    flag for every goody

    """
    if 1 in modifyByUser:  # user modified goodynum
        return
    else:
        for i in range(MAX_INFO_ENTITIES):
            goodyNum = GoodyIni.GoodyInfo[i].initNum
            goodyNumList[i] = goodyNum

        # loginfoprint(printFilename,1,"goody  is "+str(goodyNumList))


def SetGoodyNum(goodyNumList, modifyByUser):
    """
    no return, set goody number for goody changed by user

    """
    for i in range(MAX_INFO_ENTITIES):
        if modifyByUser[i] == 1:  # only set goody modified by user
            GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
            GoodyIni.verified[i] = 1


def SetGoodyNumByName(goodyString, num):
    """
    no return, set the number in the list contains all the goodynumber
    goodyString     goody name
    num    the number to increase

    """
    for i in range(MAX_INFO_ENTITIES):
        goodyCtype = GoodyIni.GoodyInfo[i].goodyString
        goodyName = getString(goodyCtype)
        if goodyString == goodyName:
            global goodyNumList
            goodyNumList[i] = max(num,0)
            global modifyByUser
            modifyByUser[i] = 1
            # GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
            # GoodyIni.verified[i] = 1
            break


def increaseGoodyNum(goodyString, num):
    """
    no return, increase the number in the list contains all the goodynumber
    goodyString     goody name
    num    the number to increase

    """
    for i in range(MAX_INFO_ENTITIES):
        goodyCtype = GoodyIni.GoodyInfo[i].goodyString
        goodyName = getString(goodyCtype)
        if goodyString == goodyName:
            global goodyNumList
            goodyNumList[i] += num
            global modifyByUser
            modifyByUser[i] = 1
            # GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
            # GoodyIni.verified[i] = 1
            break


def decreaseGoodyNum(goodyString, num):
    """
    no return, decrease the number in the list contains all the goodynumber
    goodyString     goody name
    num    the number to decrease

    """
    for i in range(MAX_INFO_ENTITIES):
        goodyCtype = GoodyIni.GoodyInfo[i].goodyString
        goodyName = getString(goodyCtype)
        if goodyString == goodyName:
            global goodyNumList
            currentNum1=goodyNumList[i]
            currentNum1-= num
            # cap to zero
            goodyNumList[i]=max(currentNum1,0)
            global modifyByUser
            modifyByUser[i] = 1
            # GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
            # GoodyIni.verified[i] = 1
            break

def increaseGoodyNumWithInterval(goodyString, num, interval=0.3):
    """
    no return, increase the number in the list contains all the goodynumber
    goodyString     goody name
    num    the number to increase
    interval (optional)  the time interval for goody to change

    """
    global goodyLastTime
    currentTime=time()
    timeDiff=abs(currentTime-goodyLastTime)
    if timeDiff > interval: 
        goodyLastTime=currentTime
        for i in range(MAX_INFO_ENTITIES):
            goodyCtype = GoodyIni.GoodyInfo[i].goodyString
            goodyName = getString(goodyCtype)
            if goodyString == goodyName:
                global goodyNumList
                goodyNumList[i] += num
                global modifyByUser
                modifyByUser[i] = 1
                # GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
                # GoodyIni.verified[i] = 1
                break

def decreaseGoodyNumWithInterval(goodyString, num, interval=0.3):
    """
    no return, decrease the number in the list contains all the goodynumber
    goodyString     goody name
    num    the number to decrease
    interval (optional)  the time interval for goody to change

    """
    global goodyLastTime
    currentTime=time()
    timeDiff=abs(currentTime-goodyLastTime)
    if timeDiff > interval: 
        goodyLastTime=currentTime
        for i in range(MAX_INFO_ENTITIES):
            goodyCtype = GoodyIni.GoodyInfo[i].goodyString
            goodyName = getString(goodyCtype)
            if goodyString == goodyName:
                global goodyNumList
                currentNum1=goodyNumList[i]
                currentNum1-= num
                # cap to zero
                goodyNumList[i]=max(currentNum1,0)
                global modifyByUser
                modifyByUser[i] = 1
                # GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
                # GoodyIni.verified[i] = 1
                break

def SetGoodyNum(goodyNumList, modifyByUser):
    """
    no return, set goody number for goody changed by user

    """
    for i in range(MAX_INFO_ENTITIES):
        if modifyByUser[i] == 1:  # only set goody modified by user
            GoodyIni.GoodyInfo[i].initNum = goodyNumList[i]
            GoodyIni.verified[i] = 1


def GetGoodyNum(goodyString):
    """
    return [goodyNum] get goody number with name
    goodyString     goody name

    """
    foundGoody = 0
    for i in range(MAX_INFO_ENTITIES):
        goodyCtype = GoodyIni.GoodyInfo[i].goodyString
        goodyName = getString(goodyCtype)
        if goodyString == goodyName:
            global goodyNumList
            global modifyByUser
            foundGoody = 1
            if modifyByUser[i] == 1:
                return goodyNumList[i]
            else:
                return GoodyIni.GoodyInfo[i].initNum

    if foundGoody == 0:
        return 0


def setObjstartLocation(StageID, PI, ObjNo, startx, starty):
    """
    return [verified] set the position of one object, player window
    StageID     id of stage
    PI
        0 for player 1
        1 for player 2

    ObjNo       the number of item, for example 0,1,2
    startx      the x of object
    starty      the y of object

    """

    if currentStage != StageID:
        pass
        verified = False
    else:
        OBJInfoIni.OBJInfo[PI * MAX_INFO_ENTITIES + ObjNo].xstart = startx
        OBJInfoIni.OBJInfo[PI * MAX_INFO_ENTITIES + ObjNo].ystart = starty
        OBJInfoIni.verified[PI * MAX_INFO_ENTITIES + ObjNo] = 1
        verified = True
    return verified


def getObjstartLocation(StageID, PI, ObjNo):
    """
    return [verified, x, y] get the position of one object, player window
    StageID     id of stage
    PI
        0 for player 1
        1 for player 2

    ObjNo       the number of item, for example 0,1,2

    """

    if currentStage != StageID:
        pass
        verified = False
    else:
        x = OBJInfoIni.OBJInfo[PI * MAX_INFO_ENTITIES + ObjNo].xstart
        y = OBJInfoIni.OBJInfo[PI * MAX_INFO_ENTITIES + ObjNo].ystart
        verified = True
    return verified, x, y


def plotDebug(StageID, **kwargs):
    """Monitor variables by debug ui

    Usage:
        single variable: plotDebug(currentStage, x=x)
        multiple variables: plotDebug(currentStage, newx=x, y=y)
    Args:
        StageID (int): id of stage
        kwargs(optional): key value pairs
    Returns:
        verified(boolean): verified
    """
    if currentStage != StageID:
        pass
        verified = False
    else:
        if debug.win is not None and debug.FLAG == debug.DEBUG_PLOT_FLAG:
            _, time_index = GetTimeIndex(StageID)
            debug.win.monitor_variables(StageID, time_index, kwargs)
        verified = True
    return verified


def playSound(soundSrc, status, loop, delay, volume, repeatTimes, repeatIntervalTime):
    """
    soundSrc The absolute address of the sound file
    status continue，pause，remove
    loop   True of False
    delay  second
    volume 0~1
    repeatTimes
    repeatIntervalTime

    Note that each parameter is a string
    """
    command = (
        "https://localhost:8443/play-music?&status=%s&loop=%s&delay=%s&volume=%s&repeatTimes=%s&repeatIntervalTime=%s"
        % (status, loop, delay, volume, repeatTimes, repeatIntervalTime)
    )
    command = (
        "curl -k --get --data-urlencode " + '"src=%s" "' % (soundSrc) + command + '"'
    )
    os.system(command)


class StageElement:
    def __init__(self, type, index):
        self.type = type
        self.index = index - 1
        self._x = 0
        self._y = 0
        self._scale_x = 1
        self._scale_y = 1
        self._transparency = 1

        verified, x, y, *rest = GetStartLocation(currentStage, type, self.index)
        if verified:
            self._x = x
            self._y = y
        verified, xscale, yscale = GetStartScale(currentStage, type, self.index)
        if verified:
            self._scale_x = xscale
            self._scale_y = yscale
        verified, transparency = GetStartTransparency(currentStage, type, self.index)
        if verified:
            self._transparency = transparency

    @property
    def x(self) -> int:
        return self.getX()

    @x.setter
    def x(self, x: int):
        self.setX(x)

    @property
    def y(self) -> int:
        return self.getY()

    @y.setter
    def y(self, y: int):
        self.setY(y)

    def getX(self) -> int:
        verified, x, y, *rest = GetStartLocation(currentStage, self.type, self.index)
        if verified:
            self._x = x
            self._y = y
        return self._x

    def getY(self) -> int:
        verified, x, y, *rest = GetStartLocation(currentStage, self.type, self.index)
        if verified:
            self._x = x
            self._y = y
        return self._y

    def setX(self, x: int):
        self._x = x
        SetStartLocation(currentStage, self.type, self.index, x, self._y)

    def setY(self, y: int):
        self._y = y
        SetStartLocation(currentStage, self.type, self.index, self._x, y)

    def getCoord(self) -> tuple:
        return (self.getX(), self.getY())

    def setCoord(self, x: int, y: int):
        self._x = x
        self._y = y
        SetStartLocation(currentStage, self.type, self.index, x, y)

    def left(self, x: int):
        self.setX(self._x - x)

    def right(self, x: int):
        self.setX(self._x + x)

    def up(self, y: int):
        self.setY(self._y - y)

    def down(self, y: int):
        self.setY(self._y + y)

    @property
    def scaleX(self) -> float:
        return self.getScaleX()

    @scaleX.setter
    def scale_x(self, xscale: float):
        self.setScaleX(xscale)

    @property
    def scaleY(self) -> float:
        return self.getScaleY()

    @scaleY.setter
    def scale_y(self, yscale: float):
        self.setScaleY(yscale)

    def getScaleX(self) -> float:
        verified, xscale, yscale = GetStartScale(currentStage, self.type, self.index)
        if verified:
            self._scale_x = xscale
            self._scale_y = yscale
        return self._scale_x

    def getScaleY(self) -> float:
        verified, xscale, yscale = GetStartScale(currentStage, self.type, self.index)
        if verified:
            self._scale_x = xscale
            self._scale_y = yscale
        return self._scale_y

    def setScaleX(self, xscale: float):
        self._scale_x = xscale
        ScaleChange(currentStage, self.type, self.index, xscale, self._scale_y)

    def setScaleY(self, yscale: float):
        self._scale_y = yscale
        ScaleChange(currentStage, self.type, self.index, self._scale_x, yscale)

    def setScale(self, xscale: float, yscale: float):
        self._scale_x = xscale
        self._scale_y = yscale
        ScaleChange(currentStage, self.type, self.index, xscale, yscale)

    @property
    def transparency(self) -> float:
        return self.getTransparency()

    @transparency.setter
    def transparency(self, transparency: float):
        self.setTransparency(transparency)

    def getTransparency(self) -> float:
        verified, transparency = GetStartTransparency(
            currentStage, self.type, self.index
        )
        if verified:
            self._transparency = transparency
        return self._transparency

    def setTransparency(self, transparency: float):
        self._transparency = transparency
        TransparencyChange(currentStage, self.type, self.index, transparency)


class ObjectElementMixin(StageElement):
    def __init__(self, type, index):
        self.type = type
        self.index = index - 1
        self._x = 0
        self._y = 0
        self._scale_x = 1
        self._scale_y = 1
        self._transparency = 1
        self.pi = 0 if self.type == OBJ else 1

        verified, x, y = getObjstartLocation(currentStage, self.pi, self.index)
        if verified:
            self._x = x
            self._y = y
        verified, xscale, yscale = GetStartScale(currentStage, type, self.index)
        if verified:
            self._scale_x = xscale
            self._scale_y = yscale
        verified, transparency = GetStartTransparency(currentStage, type, self.index)
        if verified:
            self._transparency = transparency

    def getX(self) -> int:
        verified, x, y = getObjstartLocation(currentStage, self.pi, self.index)
        if verified:
            self._x = x
            self._y = y
        return self._x

    def getY(self) -> int:
        verified, x, y = getObjstartLocation(currentStage, self.pi, self.index)
        if verified:
            self._x = x
            self._y = y
        return self._y

    def setX(self, x: int):
        self._x = x
        setObjstartLocation(currentStage, self.pi, self.index, x, self._y)

    def setY(self, y: int):
        self._y = y
        setObjstartLocation(currentStage, self.pi, self.index, self._x, y)

    def setCoord(self, x: int, y: int):
        self._x = x
        self._y = y
        setObjstartLocation(currentStage, self.pi, self.index, x, y)


class ForegroundElement(StageElement):
    def __init__(self, index=1):
        super().__init__(FG, index)


class BackgroundElement(StageElement):
    def __init__(self, index=1):
        super().__init__(BG, index)


class CustomElement(StageElement):
    def __init__(self, index=1):
        super().__init__(CG, index)


class LeftHandElement(StageElement):
    def __init__(self, index=1, copyIndex=1):
        super().__init__(HAND, (index - 1)*MAX_INFO_ENTITIES*3 + (copyIndex - 1)*3 + 2)

class RightHandElement(StageElement):
    def __init__(self, index=1, copyIndex=1):
        super().__init__(HAND, (index - 1)*MAX_INFO_ENTITIES*3 + (copyIndex - 1)*3 + 3)


class HeadElement(StageElement):
    def __init__(self, index=1, copyIndex=1):
        super().__init__(HEAD, (index - 1)*MAX_INFO_ENTITIES*3 + (copyIndex - 1)*3 + 1)


class ObjElement(ObjectElementMixin):
    def __init__(self, index=1):
        super().__init__(OBJ, index)


class ObjtElement(ObjectElementMixin):
    def __init__(self, index=1):
        super().__init__(OBJT, index)


class StageInfo:
    def __init__(self):
        self._time = 0
        self._timeIndex = 0

    @property
    def time(self):
        return self.getTime()

    @property
    def timeIndex(self):
        return self.getTimeIndex()

    def getTime(self):
        verified, t = GetTime(currentStage)
        if verified:
            self._time = t
        return self._time

    def getTimeIndex(self):
        verified, timeIndex = GetTimeIndex(currentStage)
        if verified:
            self._timeIndex = timeIndex
        return timeIndex

    def getGoodyNum(self, goodyString):
        return GetGoodyNum(goodyString)

    def setGoodyNum(self, goodyString, num):
        return SetGoodyNumByName(goodyString, num)

    def setScriptTransition(self, scriptNo):
        return setSingleScriptTransition(currentStage, scriptNo)

    def printLn(self, contentStr):
        contentStr = contentStr if contentStr.endswith("\n") else contentStr + "\n"
        with open(printFilename, "a") as f:
            f.write(contentStr)
