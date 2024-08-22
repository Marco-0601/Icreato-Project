"""
localUtils.py
This file is to mock the userUtils.py file.
version 1.0 on 10/12/2023
a. initial version
version 1.1 on 10/20/2023
a. fix some position issues
version 1.2 on 10/27/2023
a. fix some bugs
version 1.3 on 01/26/2024
a. support icamera web
version 1.4 on 05/29/2024
a. updated GetGoodyNum
"""

from playStage import time
from playStage import printFilename
from playStage import currentStage
from playStage import stageEnterTime
from playStage import stageInitTime
from playStage import offsetX, offsetY, currentGesture, gestureDuration
from playStage import shared_data
from playStage import goodies
from playStage import INIT_GESTURE, REGULAR_GESTURE, MAX_INFO_ENTITIES
from playStage import send_to_stdout
from playStage import isProduction

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

NUM_OF_BODY_PARTS = 3


def sendMsgToStdout(msg):
    print(msg)
    sys.stdout.flush()


def loginfoprint(filename, firstTime, contentStr):
    contentStr = contentStr + "\n"
    if firstTime == 0:
        f = open(filename, "w")
        f.close()
    elif firstTime > 0:
        f = open(filename, "a")
        f.write(contentStr)
        f.close()


def GetObjKeyFromObjID(ObjID):
    key = ""
    if ObjID == FG:
        key = "fg"
    elif ObjID == BG:
        key = "bg"
    elif ObjID == CG:
        key = "cus"
    elif ObjID == HAND:
        key = "hand"
    elif ObjID == HEAD:
        key = "head"
    elif ObjID == OBJ:
        key = "obj"
    elif ObjID == OBJT:
        key = "objt"
    return key


def GetObjIDFromObjKey(key):
    ObjID = 0
    if key == "fg":
        ObjID = FG
    elif key == "bg":
        ObjID = BG
    elif key == "cus":
        ObjID = CG
    elif key == "hand":
        ObjID = HAND
    elif key == "head":
        ObjID = HEAD
    elif key == "obj":
        ObjID = OBJ
    elif key == "objt":
        ObjID = OBJT
    return ObjID

def calculate_player_number_from_id(itemID):
    num = int(itemID / MAX_INFO_ENTITIES / NUM_OF_BODY_PARTS)
    part = int(itemID % NUM_OF_BODY_PARTS)
    index = int(itemID / NUM_OF_BODY_PARTS) if num == 0 else int((itemID - 24) / NUM_OF_BODY_PARTS)
    
    if num == 0:
        return OBJ, index, part
    else:
        return OBJT, index, part

def GetUnit(ObjID, itemID, part=None):
    if shared_data is None:
        return None
    else:
        key = GetObjKeyFromObjID(ObjID)
        parameter = shared_data["parameter"]
        if key in parameter:
            units = parameter[key]["units"]
            unit = units[itemID]["init"] if part is None else units[itemID][str(part)]
            return unit
        else:
            return None


def GetStartLocation(StageID, ObjID, itemID):
    if isProduction:
        if ObjID == HAND:
            # confidence, w=12, open hand, w=13, close hand, w=14, Lasso hand
            key, index, part = calculate_player_number_from_id(itemID)
            unit = GetUnit(key, index, part)
            if unit is None:
                return False, 0, 0, REGULAR_GESTURE
            else:
                return True, unit["x"], unit["y"], unit["confidence"]
        elif ObjID == HEAD:
            key, index, part = calculate_player_number_from_id(itemID)
            unit = GetUnit(key, index, part)
            if unit is None:
                return False, 0, 0, REGULAR_GESTURE
            else:
                return True, unit["x"], unit["y"], unit["confidence"]
        else:
            unit = GetUnit(ObjID, itemID)
            if unit is None:
                return False, 0, 0
            else:
                return True, unit["x"], unit["y"]
    else:
        global currentGesture
        global gestureDuration
        unit = GetUnit(ObjID, itemID)
        if ObjID == HAND:
            # confidence, w=12, open hand, w=13, close hand, w=14, Lasso hand
            if gestureDuration == 0:
                currentGesture = REGULAR_GESTURE
            key, index, part = calculate_player_number_from_id(itemID)
            unit = GetUnit(key, 0)
            # distance = -10 if itemID % 2 == 1 else 10
            distance = 0
            return True, unit["x"] + offsetX + distance, unit["y"] + offsetY, currentGesture
        if ObjID == HEAD:
            key, index, part = calculate_player_number_from_id(itemID)
            unit = GetUnit(key, 0)
            distanceY = 0
            return True, unit["x"] + offsetX, unit["y"] + offsetY + distanceY, REGULAR_GESTURE
        elif unit is None:
            return False, 0, 0
        else:
            return True, unit["x"], unit["y"]


def GetStartScale(StageID, ObjID, itemID):
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False, 1, 1
    else:
        return True, unit["scaleX"], unit["scaleY"]


def GetStartTransparency(StageID, ObjID, itemID):
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False, 1
    else:
        return True, unit["opacity"]


def ScaleChange(StageID, ObjID, itemID, xScale, yScale):
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False
    else:
        unit["scaleX"] = xScale
        unit["scaleY"] = yScale
        sendMsgToStdout(
            f"<{GetObjKeyFromObjID(ObjID)}-{itemID}>:scaleX={xScale},scaleY={yScale};"
        )
        return True


def TransparencyChange(StageID, ObjID, itemID, transparency):
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False
    else:
        unit["opacity"] = transparency
        sendMsgToStdout(
            f"<{GetObjKeyFromObjID(ObjID)}-{itemID}>:opacity={transparency};"
        )
        return True


def SetStartLocation(StageID, ObjID, itemID, x, y):
    global offsetX
    global offsetY
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False
    else:
        if ObjID == OBJ or ObjID == OBJT:
            if unit["x"] != x:
                offsetX = 0
            if unit["y"] != y:
                offsetY = 0
        unit["x"] = x
        unit["y"] = y
        sendMsgToStdout(f"<{GetObjKeyFromObjID(ObjID)}-{itemID}>:x={x},y={y};")
        return True

def SetStartLocationNoRender(StageID, ObjID, itemID, x, y):
    global offsetX
    global offsetY
    unit = GetUnit(ObjID, itemID)
    if unit is None:
        return False
    else:
        if ObjID == OBJ or ObjID == OBJT:
            if unit["x"] != x:
                offsetX = 0
            if unit["y"] != y:
                offsetY = 0
        unit["x"] = x
        unit["y"] = y
        return True

def SetStartrotAngle(StageID, ObjID, itemID, rotAngle):
    pass


def getObjstartLocation(StageID, PI, ObjNo):
    obj_id = OBJT if PI == 1 else OBJ
    return GetStartLocation(StageID, obj_id, ObjNo)


def setObjstartLocation(StageID, PI, item_no, startx, starty):
    obj_id = OBJT if PI == 1 else OBJ
    return SetStartLocation(StageID, obj_id, item_no, startx, starty)


def GetTime(StageID):
    if shared_data is None:
        return False, 0
    else:
        return True, time.time() - stageEnterTime


def GetTimeIndex(StageID):
    if shared_data is None:
        return False, 0
    else:
        return True, stageInitTime


def clearScriptTransition(ScriptIni1):
    pass


def setSingleScriptTransition(StageID, scriptNo):
    sendMsgToStdout(f"[end]:scriptNo={scriptNo};")
    return True


def GetGoody(key):
    if len(goodies) == 0:
        return None
    else:
        for goody in goodies:
            if goody["name"] == key:
                return goody
        return None


def GetGoodyNumList(goodyNumList, modifyByUser):
    pass


def SetGoodyNum(goodyNumList, modifyByUser):
    pass


def SetGoodyNumByName(goodyString, num):
    goody = GetGoody(goodyString)
    if goody is None:
        return
    else:
        goody["initNum"] = num
        sendMsgToStdout(f"<goody-{goodyString}>:{num};")


def increaseGoodyNum(goodyString, num):
    goody = GetGoody(goodyString)
    if goody is None:
        return
    else:
        goody["initNum"] += num
        sendMsgToStdout(f"<goody-{goodyString}>:{goody['initNum']};")


def decreaseGoodyNum(goodyString, num):
    goody = GetGoody(goodyString)
    if goody is None:
        return
    else:
        goody["initNum"] -= num
        sendMsgToStdout(f"<goody-{goodyString}>:{goody['initNum']};")


def GetGoodyNum(goodyString):
    foundGoody = 0
    goody = GetGoody(goodyString)
    if goody is None:
        return 0, foundGoody
    else:
        foundGoody = 1
        return goody["initNum"], foundGoody


class Elements:
    """
    a class storing element number
    """

    def __init__(self):
        self.ElementsDict = {}

    def addStage(self, stageNo, elementNoList):
        self.ElementsDict[str(stageNo)] = elementNoList


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
        verified, x, y, *rest = GetStartLocation(currentStage, self.type, self.index)
        if verified:
            self._x = x
            self._y = y
        return (x, y)

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
        super().__init__(HAND, (index - 1)*MAX_INFO_ENTITIES*NUM_OF_BODY_PARTS + (copyIndex - 1)*NUM_OF_BODY_PARTS + 2)

class RightHandElement(StageElement):
    def __init__(self, index=1, copyIndex=1):
        super().__init__(HAND, (index - 1)*MAX_INFO_ENTITIES*NUM_OF_BODY_PARTS + (copyIndex - 1)*NUM_OF_BODY_PARTS + 3)


class HeadElement(StageElement):
    def __init__(self, index=1, copyIndex=1):
        super().__init__(HEAD, (index - 1)*MAX_INFO_ENTITIES*NUM_OF_BODY_PARTS + (copyIndex - 1)*NUM_OF_BODY_PARTS + 1)


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
