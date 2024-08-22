'''
iCreatorData.py
This file is to defined the data structure to interface with the main IntegemCam program
version 1.0 on 1/1/2022
a. defined the basic functions.
version 1.1 on 3/9/2022
a. add keyboardSpeed into  strCUSChgCtr, strBGChgCtr, strFGChgCtr, and strOBJChgCtr
version 1.2 on 9/10/2022
a. make FGInfo, BGInfo, CusInfo, OBJInfo, Goody, Script, BodyPos, transfer as a 3-element buffer
b. update CURRENT_VERSION_NO to 3 to be compatible for old projects
version 1.3 on 10/21/2022
a. fix the version compatible issue introduced in version 1.2
b. add portion to receive rawPose. use rawPoseEnbl=1 to turn on the feature
version 1.4 on 4/9/2024
a. fix issue related to Goody has empty names occassionally.
'''

import ctypes
import sys
import mmap
from datetime import datetime
import math


MAX_INFO_ENTITIES= 8
MAX_PROJECT_PEOPLE=2
MAX_COMB_ENTITIES=16
MAX_GOODY_ENTITIES=40
MAX_GOODY_IMG_STRING=440
MAX_BODY_NUM=48
LogDirStringMax=400
MAX_HAND_ENTITIES=2
MAX_HAND_POINTS=126
MAX_BUFFER_NUM=3
PAST_VERSION_NO2=2
CURRENT_VERSION_NO=3
MAX_POSE_POINTS=198
rawPoseEnbl=0


class strPoseAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int),
        ('rawPose', ctypes.c_float*MAX_POSE_POINTS)
    ]

class strInfoOut(ctypes.Structure):
    _fields_ = [
        ('stageNo', ctypes.c_int),
        ('FGNo', ctypes.c_int),
        ('mutex', ctypes.c_int),
        ('endSignal', ctypes.c_int),
        ('CUSNo', ctypes.c_int),
        ('BGNo', ctypes.c_int),
        ('PersonNo', ctypes.c_int),
        ('VersionNo', ctypes.c_int),
        ('GoodyNo', ctypes.c_int),
        ('BodyNo', ctypes.c_int),
        ('ScriptConditionNo', ctypes.c_int),
        ('EachPNo', ctypes.c_int*MAX_PROJECT_PEOPLE)
    ]


class strInfoInputNo(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('stageNo', ctypes.c_int),
        ('FGNo', ctypes.c_int),
        ('FGCNo', ctypes.c_int),
        # ('FGList', ctypes.c_int*MAX_INFO_ENTITIES),
        # ('FGCList', ctypes.c_int*MAX_INFO_ENTITIES),
        ('BGNo', ctypes.c_int),
        ('BGCNo', ctypes.c_int),
        # ('BGList', ctypes.c_int*MAX_INFO_ENTITIES),
        # ('BGCList', ctypes.c_int*MAX_INFO_ENTITIES),
        ('CUSNo', ctypes.c_int),
        ('CUSCNo', ctypes.c_int),
        # ('CUSList', ctypes.c_int*MAX_INFO_ENTITIES),
        # ('CUSCList', ctypes.c_int*MAX_INFO_ENTITIES),
        # ('PersonNo', ctypes.c_int),
        ('OBJNo', ctypes.c_int),
        ('OBJCNo', ctypes.c_int),
        ('VersionNo', ctypes.c_int)
        # ('OBJList', ctypes.c_int*MAX_INFO_ENTITIES*MAX_PROJECT_PEOPLE),
        # ('OBJCList', ctypes.c_int*MAX_INFO_ENTITIES*MAX_PROJECT_PEOPLE)
    ]

class strInfoInputNo2(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('GoodyNo', ctypes.c_int),
        ('BodyPosNo', ctypes.c_int),
        ('ScriptConditionNo', ctypes.c_int)
        #('ObjPosNo', ctypes.c_int*MAX_PROJECT_PEOPLE)

    ]

class strPythonLog(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('LogDir', ctypes.c_char*LogDirStringMax)
    ]

class strHandAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('PeopleNo', ctypes.c_int),
        ('CamWidth', ctypes.c_int),
        ('CamHeight', ctypes.c_int),
        ('LHAccNo', ctypes.c_int*MAX_HAND_ENTITIES),
        ('RHAccNo', ctypes.c_int*MAX_HAND_ENTITIES),
        ('LeftHand', ctypes.c_float*MAX_HAND_POINTS),
        ('RightHand', ctypes.c_float*MAX_HAND_POINTS)
    ]

class GoodyContent(ctypes.Structure):
    _fields_ = [
        ('img', ctypes.c_char*MAX_GOODY_IMG_STRING),
        ('goodyString', ctypes.c_char*MAX_GOODY_ENTITIES),
        ('gap', ctypes.c_int),
        ('index', ctypes.c_int),
        ('scale', ctypes.c_float),
        ('initNum', ctypes.c_int),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('height', ctypes.c_int),
        ('width', ctypes.c_int),
        ('isGif', ctypes.c_bool),
        ('show', ctypes.c_int),
        ('startStage', ctypes.c_char*MAX_GOODY_ENTITIES),
        ('endStage', ctypes.c_char*MAX_GOODY_ENTITIES)
    ]

class Vector4(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('w', ctypes.c_float)
    ]

class BounceInfo(ctypes.Structure):
    _fields_ = [
        ('v', ctypes.c_float),
        ('theta', ctypes.c_float),
        ('L', ctypes.c_bool),
        ('R', ctypes.c_bool),
        ('U', ctypes.c_bool),
        ('D', ctypes.c_bool),
        ('T', ctypes.c_float)
    ]

class strBGInfo(ctypes.Structure):
    _fields_ = [
        ('backgroundNo', ctypes.c_int),
        ('backgroundNo_BG', ctypes.c_int),
        ('foregroundX0', ctypes.c_float),
        ('foregroundY0', ctypes.c_float),
        ('foregroundWidth', ctypes.c_float),
        ('foregroundHeight', ctypes.c_float),

        ('xstart', ctypes.c_float),
        ('ystart', ctypes.c_float),
        ('xscale', ctypes.c_float),
        ('yscale', ctypes.c_float),
        ('rotAngle', ctypes.c_float),
        ('shearH', ctypes.c_float),
        ('shearV', ctypes.c_float),
        ('alphaNor', ctypes.c_float),
        ('foreGDReplaceinfo', ctypes.c_int),
        ('color', ctypes.c_int),
        ('brightness', ctypes.c_int),
        ('BFlag', ctypes.c_int),
        ('BInfo', BounceInfo),
        ('nonfollowN', ctypes.c_int)
    ]

class strFGInfo(ctypes.Structure):
    _fields_ = [
        ('foregroundNo', ctypes.c_int),
        ('foregroundNo_BG', ctypes.c_int),
        ('foregroundX0', ctypes.c_float),
        ('foregroundY0', ctypes.c_float),
        ('foregroundWidth', ctypes.c_float),
        ('foregroundHeight', ctypes.c_float),
        ('xstart', ctypes.c_float),
        ('ystart', ctypes.c_float),
        ('xscale', ctypes.c_float),
        ('yscale', ctypes.c_float),
        ('rotAngle', ctypes.c_float),
        ('shearH', ctypes.c_float),
        ('shearV', ctypes.c_float),
        ('alphaNor', ctypes.c_float),
        ('foreGDReplaceinfo', ctypes.c_int),
        ('color', ctypes.c_int),
        ('brightness', ctypes.c_int),
        ('BFlag', ctypes.c_int),
        ('BInfo', BounceInfo),
        ('nonfollowN', ctypes.c_int)
    ]

class strCUSInfo(ctypes.Structure):
    _fields_ = [
        ('foregroundX0', ctypes.c_float),
        ('foregroundY0', ctypes.c_float),
        ('foregroundWidth', ctypes.c_float),
        ('foregroundHeight', ctypes.c_float),
        ('xstart', ctypes.c_float),
        ('ystart', ctypes.c_float),
        ('xscale', ctypes.c_float),
        ('yscale', ctypes.c_float),
        ('rotAngle', ctypes.c_float),
        ('shearH', ctypes.c_float),
        ('shearV', ctypes.c_float),
        ('foreGDReplaceinfo', ctypes.c_int),
        ('alphaNor', ctypes.c_float),
        ('CustomerNo', ctypes.c_int),
        ('customerPos', ctypes.c_int),
        ('CustomerNo_BG', ctypes.c_int),
        ('color', ctypes.c_int),
        ('brightness', ctypes.c_int),
        ('BFlag', ctypes.c_int),
        ('BInfo', BounceInfo),
        ('nonfollowN', ctypes.c_int)
    ]

class strOBJInfo(ctypes.Structure):
    _fields_ = [
        ('xstart', ctypes.c_float),
        ('ystart', ctypes.c_float),
        ('xscale', ctypes.c_float),
        ('yscale', ctypes.c_float),
        ('rotAngle', ctypes.c_float),
        ('shearH', ctypes.c_float),
        ('shearV', ctypes.c_float),
        ('alphaNor', ctypes.c_float),
        ('foregroundX0', ctypes.c_float),
        ('foregroundY0', ctypes.c_float),
        ('foregroundWidth', ctypes.c_float),
        ('foregroundHeight', ctypes.c_float),
        ('foreGDReplaceinfo', ctypes.c_int),
        ('color', ctypes.c_int),
        ('brightness', ctypes.c_int),
        ('BFlag', ctypes.c_int),
        ('BInfo', BounceInfo),
        ('Showup', ctypes.c_bool),
        ('nonfollowN', ctypes.c_int)
    ]
               

class BBoundary(ctypes.Structure):
    _fields_ = [
        ('X1', ctypes.c_int),
        ('Y1', ctypes.c_int),
        ('X2', ctypes.c_int),
        ('Y2', ctypes.c_int)
    ]

class BCoef(ctypes.Structure):
    _fields_ = [
        ('LCoef', ctypes.c_float),
        ('RCoef', ctypes.c_float),
        ('UCoef', ctypes.c_float),
        ('DCoef', ctypes.c_float)
    ]   

class strBounce(ctypes.Structure):
    _fields_ = [
        ('gravity', ctypes.c_float),
        ('Bd', BBoundary),
        ('Bc', BCoef),
        ('BRotation', ctypes.c_int)
    ]

class strHoverCtr(ctypes.Structure):
    _fields_ = [
        ('HFlag', ctypes.c_int),
        ('X1', ctypes.c_float),
        ('X2', ctypes.c_float),
        ('T', ctypes.c_int)
    ]

class strFollow(ctypes.Structure):
    _fields_ = [
        ('pN', ctypes.c_int),
        ('objN', ctypes.c_int),
        ('bodyP', ctypes.c_int)
    ]

class strStick(ctypes.Structure):
    _fields_ = [
        ('stickItem', ctypes.c_int),
        ('stickNo', ctypes.c_int),
        ('valid', ctypes.c_bool),
        ('processed', ctypes.c_bool)
    ]

class strFGChgCtr(ctypes.Structure):
    _fields_ = [
        ('FGChgCtr', ctypes.c_int),
        ('FGTimeCh', ctypes.c_int),
        ('FGStepOrEnd', ctypes.c_int),
        ('FGStickItem', ctypes.c_int),
        ('FGStickValue', ctypes.c_int),
        ('FGKeyBoardSpeed', ctypes.c_int),
        ('FGBounce', strBounce),
        ('Hover', strHoverCtr),
        ('followCtr', strFollow),
        ('stickCtr', strStick)
    ]

class strBGChgCtr(ctypes.Structure):
    _fields_ = [
        ('BGChgCtr', ctypes.c_int),
        ('BGTimeCh', ctypes.c_int),
        ('BGStickItem', ctypes.c_int),
        ('BGStickValue', ctypes.c_int),
        ('BGStepOrEnd', ctypes.c_int),
        ('BGKeyBoardSpeed', ctypes.c_int),
        ('FGBounce', strBounce),
        ('Hover', strHoverCtr),
        ('followCtr', strFollow),
        ('stickCtr', strStick)
    ]

class strCUSChgCtr(ctypes.Structure):
    _fields_ = [
        ('CusChgCtr', ctypes.c_int),
        ('CusTimeCh', ctypes.c_int),
        ('CusStepOrEnd', ctypes.c_int),
        ('CusStickItem', ctypes.c_int),
        ('CusStickValue', ctypes.c_int),
        ('CusKeyBoardSpeed', ctypes.c_int),
        ('FGBounce', strBounce),
        ('Hover', strHoverCtr),
        ('followCtr', strFollow),
        ('stickCtr', strStick)
    ]

class strOBJChgCtr(ctypes.Structure):
    _fields_ = [
        ('ObjChgCtr', ctypes.c_int),
        ('ObjTimeCh', ctypes.c_int),
        ('ObjStepOrEnd', ctypes.c_int),
        ('objStickItem', ctypes.c_int),
        ('objStickValue', ctypes.c_int),
        ('objKeyBoardSpeed', ctypes.c_int),
        ('FGBounce', strBounce),
        ('Hover', strHoverCtr),
        ('followCtr', strFollow),
        ('stickCtr', strStick)
    ]
            

class strCapChange(ctypes.Structure):
    _fields_ = [
        ('cValue', ctypes.c_int),
        ('capvalue', ctypes.c_int),
        ('loop', ctypes.c_int),
        ('frequency', ctypes.c_int)
    ]

class strBasicFGC(ctypes.Structure):
    _fields_ = [
        ('DforeGDReplaceinfo', ctypes.c_int),
        ('DforegroundNo', ctypes.c_int),
        ('DforegroundX0', ctypes.c_float),
        ('DforegroundY0', ctypes.c_float),
        ('DforegroundWidth', ctypes.c_float),
        ('DforegroundHeight', ctypes.c_float),
        ('DinitialshearV', ctypes.c_float),
        ('DinitialshearH', ctypes.c_float),
        ('Dinitialx', ctypes.c_float),
        ('Dinitialy', ctypes.c_float),
        ('Dinitialscalex', ctypes.c_float),
        ('Dinitialscaley', ctypes.c_float),
        ('Dinitialalpha', ctypes.c_float),
        ('Dinitialangle', ctypes.c_float),
        ('ColorChange', strCapChange),
        ('BrightnessChange', strCapChange)
    ]

class strBasicBGC(ctypes.Structure):
    _fields_ = [
        ('DforeGDReplaceinfo', ctypes.c_int),
        ('DbackgroundNo', ctypes.c_int),
        ('DforegroundX0', ctypes.c_float),
        ('DforegroundY0', ctypes.c_float),
        ('DforegroundWidth', ctypes.c_float),
        ('DforegroundHeight', ctypes.c_float),
        ('DinitialshearV', ctypes.c_float),
        ('DinitialshearH', ctypes.c_float),
        ('Dinitialx', ctypes.c_float),
        ('Dinitialy', ctypes.c_float),
        ('Dinitialscalex', ctypes.c_float),
        ('Dinitialscaley', ctypes.c_float),
        ('Dinitialalpha', ctypes.c_float),
        ('Dinitialangle', ctypes.c_float),
        ('ColorChange', strCapChange),
        ('BrightnessChange', strCapChange)
    ]

class strBasicCUSC(ctypes.Structure):
    _fields_ = [
        ('DforeGDReplaceinfo', ctypes.c_int),
        ('DCustomerNo', ctypes.c_int),
        ('DforegroundX0', ctypes.c_float),
        ('DforegroundY0', ctypes.c_float),
        ('DforegroundWidth', ctypes.c_float),
        ('DforegroundHeight', ctypes.c_float),
        ('DinitialshearV', ctypes.c_float),
        ('DinitialshearH', ctypes.c_float),
        ('Dinitialx', ctypes.c_float),
        ('Dinitialy', ctypes.c_float),
        ('Dinitialscalex', ctypes.c_float),
        ('Dinitialscaley', ctypes.c_float),
        ('Dinitialalpha', ctypes.c_float),
        ('Dinitialangle', ctypes.c_float),
        ('DcustomerPosIni', ctypes.c_int),
        ('ColorChange', strCapChange),
        ('BrightnessChange', strCapChange)
    ]

class strBasicOBJC(ctypes.Structure):
    _fields_ = [
        ('DforeGDReplaceinfo', ctypes.c_int),
        ('DforegroundX0', ctypes.c_float),
        ('DforegroundY0', ctypes.c_float),
        ('DforegroundWidth', ctypes.c_float),
        ('DforegroundHeight', ctypes.c_float),
        ('DinitialshearV', ctypes.c_float),
        ('DinitialshearH', ctypes.c_float),
        ('Dinitialx', ctypes.c_float),
        ('Dinitialy', ctypes.c_float),
        ('Dinitialscalex', ctypes.c_float),
        ('Dinitialscaley', ctypes.c_float),
        ('Dinitialalpha', ctypes.c_float),
        ('Dinitialangle', ctypes.c_float),
        ('ColorChange', strCapChange),
        ('BrightnessChange', strCapChange)
    ]

class strFGC(ctypes.Structure):
    _fields_ = [
        ('infoFGCtr', strFGChgCtr),
        ('infoBasicFGC', strBasicFGC),
        ('infoUpFGC', strBasicFGC),
        ('infoDownFGC', strBasicFGC),
        ('infoRotateFGC', strBasicFGC),
        ('infoARotateFGC', strBasicFGC),
        ('FGContinue', ctypes.c_bool)
    ]

class strBGC(ctypes.Structure):
    _fields_ = [
        ('BGContinue', ctypes.c_bool),
        ('infoBGCtr', strBGChgCtr),
        ('infoBasicBGC', strBasicBGC),
        ('infoUpBGC', strBasicBGC),
        ('infoDownBGC', strBasicBGC),
        ('infoRotateBGC', strBasicBGC),
        ('infoARotateBGC', strBasicBGC)
    ]

class strCUSC(ctypes.Structure):
    _fields_ = [
        ('infoCUSCtr', strCUSChgCtr),
        ('infoBasicCUSC',  strBasicCUSC),
        ('infoUpCUSC', strBasicCUSC),
        ('infoDownCUSC', strBasicCUSC),
        ('infoRotateCUSC', strBasicCUSC),
        ('infoARotateCUSC', strBasicCUSC),
        ('CusContinue', ctypes.c_bool)
    ]

class strOBJC(ctypes.Structure):
    _fields_ = [
        ('infoOBJCtr', strOBJChgCtr),
        ('infoBasicOBJC', strBasicOBJC),
        ('infoUpOBJC', strBasicOBJC),
        ('infoDownOBJC', strBasicOBJC),
        ('infoRotateOBJC', strBasicOBJC),
        ('infoARotateOBJC', strBasicOBJC),
        ('ObjContinue', ctypes.c_bool)
    ]

class strFGCInput(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int),
        ('FGInfoC', strFGC)
    ]

class strFGInfoInput(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int),
        ('FGInfo', strFGInfo)
    ]

class strFGInfoInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('FGInfo', strFGInfo*MAX_INFO_ENTITIES)
    ]

class strFGInfoInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strFGInfoInputAry*MAX_BUFFER_NUM)
    ]

class strBGInfoInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('BGInfo', strBGInfo*MAX_INFO_ENTITIES)
    ]

class strBGInfoInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strBGInfoInputAry*MAX_BUFFER_NUM)
    ]

class strCUSInfoInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('CUSInfo', strCUSInfo*MAX_INFO_ENTITIES)
    ]

class strCUSInfoInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strCUSInfoInputAry*MAX_BUFFER_NUM)
    ]

class strOBJInfoInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_COMB_ENTITIES),
        ('OBJInfo', strOBJInfo*MAX_COMB_ENTITIES)
    ]

class strOBJInfoInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strOBJInfoInputAry*MAX_BUFFER_NUM)
    ]

class strFGCInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('FGInfoC', strFGC*MAX_INFO_ENTITIES)
    ]

class strFGCInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strFGCInputAry*MAX_BUFFER_NUM)
    ]

class strBGCInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('BGInfoC', strBGC*MAX_INFO_ENTITIES)
    ]

class strBGCInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strBGCInputAry*MAX_BUFFER_NUM)
    ]

class strCUSCInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('CUSInfoC', strCUSC*MAX_INFO_ENTITIES)
    ]

class strCUSCInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strCUSCInputAry*MAX_BUFFER_NUM)
    ]

class strOBJCInputAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_COMB_ENTITIES),
        ('OBJInfoC', strOBJC*MAX_COMB_ENTITIES)
    ]

class strOBJCInputAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strOBJCInputAry*MAX_BUFFER_NUM)
    ]

class strGoodyAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('goodyNo', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('GoodyInfo', GoodyContent*MAX_INFO_ENTITIES)
    ]

class strGoodyAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strGoodyAry*MAX_BUFFER_NUM)
    ]

class strBodyPosAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int),
        ('ScreenWidth', ctypes.c_int),
        ('ScreenHeight', ctypes.c_int),
        ('BodyActPos', Vector4*MAX_BODY_NUM)
    ]

class strBodyPosAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strBodyPosAry*MAX_BUFFER_NUM)
    ]

class strScriptConditionAry(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('verified', ctypes.c_int*MAX_INFO_ENTITIES),
        ('ScriptCondNum', ctypes.c_int*MAX_INFO_ENTITIES),
        ('ScriptCondition', ctypes.c_int*MAX_INFO_ENTITIES)
    ]

class strScriptConditionAryBuffer(ctypes.Structure):
    _fields_ = [
        ('mutex', ctypes.c_int),
        ('currentIdx', ctypes.c_int),
        ('InfoBuffer', strScriptConditionAry*MAX_BUFFER_NUM)
    ]


def ctypeCopy(src):
    dst = type(src)()
    ctypes.pointer(dst)[0]=src
    return dst
	
def ctypeCopy2(src, dst):
    ctypes.pointer(dst)[0]=src

# def ctypeCopy3(src, dst, idx):
#     ctypes.pointer(dst)[idx]=src

def readInfoOut():
    data5= strInfoOut()
    shmem25=mmap.mmap(-1, ctypes.sizeof(strInfoOut),"infoOut")#,access=mmap.ACCESS_READ)
    data5=strInfoOut.from_buffer(shmem25)
    return data5

#not working
def readInfoOut2():
    data5= strInfoOut()
    shmem25=mmap.mmap(-1, ctypes.sizeof(strInfoOut),"infoOut")#,access=mmap.ACCESS_READ)
    data5=strInfoOut.from_buffer(shmem25)
    data1=ctypeCopy(data5)
    # print('readInfoOut')
    # if data1.mutex>0:
    #     print('start print')
    #     print_data2(data1)
    return data1

    # data1=strInfoOut()
    # shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoOut),"infoOut")#,access=mmap.ACCESS_READ)
    # data1 = strInfoOut.from_buffer(shmem2)
    # print('readInfoOut')
    # if data1.mutex>0:
    #     print('start print')
    #     print_data2(data1)
    #     return data1



def readInfoFG(FGInfoIniList, FGnum):
    for i in range(0,FGnum):
        mName="FGInfoInit"+str(i)
        shmem = mmap.mmap(-1, ctypes.sizeof(strFGInfoInput),mName)
        data = strFGInfoInput.from_buffer(shmem)
        #print('Python Program - Getting Data')
        if data.mutex>0:
            #input("Press Enter to continue...")
            FGInfoIniList[i]=data

def readInfoFGAry():
    mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGInfoInputAry.from_buffer(shmem3)
    return data2

def readInfoFGAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGInfoInputAry.from_buffer(shmem3)
    return data2

def readInfoFGAryBufferName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strFGInfoInputAryBuffer.from_buffer(shmem3)
    return data2

def readInfoBGAryBufferName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGInfoInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strBGInfoInputAryBuffer.from_buffer(shmem3)
    return data2

def readInfoCUSAryBufferName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSInfoInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSInfoInputAryBuffer.from_buffer(shmem3)
    return data2

def readInfoOBJAryBufferName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJInfoInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJInfoInputAryBuffer.from_buffer(shmem3)
    return data2

def readGoodyAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strGoodyAry),mName)#,access=mmap.ACCESS_READ)
    data2= strGoodyAry.from_buffer(shmem3)
    return data2

def readGoodyAryBufferName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strGoodyAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strGoodyAryBuffer.from_buffer(shmem3)
    return data2

def readBodyPosAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBodyPosAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBodyPosAry.from_buffer(shmem3)
    return data2

def readRawPosAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strPoseAry),mName)#,access=mmap.ACCESS_READ)
    data2= strPoseAry.from_buffer(shmem3)
    return data2

def readBodyPosAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBodyPosAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strBodyPosAryBuffer.from_buffer(shmem3)
    return data2

def readLogDirAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strPythonLog),mName)#,access=mmap.ACCESS_READ)
    data2= strPythonLog.from_buffer(shmem3)
    return data2

def readScriptAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strScriptConditionAry),mName)#,access=mmap.ACCESS_READ)
    data2= strScriptConditionAry.from_buffer(shmem3)
    return data2

def readScriptAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strScriptConditionAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strScriptConditionAryBuffer.from_buffer(shmem3)
    return data2

def readHandAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strHandAry),mName)#,access=mmap.ACCESS_READ)
    data2= strHandAry.from_buffer(shmem3)
    return data2

def readHandIdxName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(ctypes.c_int),mName)#,access=mmap.ACCESS_READ)
    data2= ctypes.c_int.from_buffer(shmem3)
    return data2

def readInfoBGAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBGInfoInputAry.from_buffer(shmem3)
    return data2

def readInfoCUSAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSInfoInputAry.from_buffer(shmem3)
    return data2

def readInfoOBJAryName(mName):
    # mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJInfoInputAry.from_buffer(shmem3)
    return data2

def readInfoFGAry2():
    FGInfoIni=strFGInfoInputAry()
    mName="FGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGInfoInputAry.from_buffer(shmem3)
    FGInfoIni=ctypeCopy(data2)
    if FGInfoIni.mutex>0:
        # print('readInfoFGAry mutex >0')
        continueRun=True
    else:
        # print('readInfoFGAry mutex ==0')
        continueRun=False
    return FGInfoIni, continueRun

def readInfoBGAry():
    BGInfoIni=strBGInfoInputAry()
    mName="BGInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBGInfoInputAry.from_buffer(shmem3)
    BGInfoIni=ctypeCopy(data2)
    if BGInfoIni.mutex>0:
        # print('readInfoBGAry mutex >0')
        continueRun=True
    else:
        # print('readInfoBGAry mutex ==0')
        continueRun=False
    return BGInfoIni, continueRun

def readInfoCUSAry():
    CUSInfoIni=strCUSInfoInputAry()
    mName="CUSInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSInfoInputAry.from_buffer(shmem3)
    CUSInfoIni=ctypeCopy(data2)
    if CUSInfoIni.mutex>0:
        # print('readInfoCUSAry mutex >0')
        continueRun=True
    else:
        # print('readInfoCUSAry mutex ==0')
        continueRun=False
    return CUSInfoIni, continueRun

def readGoodyAry():
    GoodyIni=strGoodyAry()
    mName="GoodyInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strGoodyAry),mName)#,access=mmap.ACCESS_READ)
    data2= strGoodyAry.from_buffer(shmem3)
    GoodyIni=ctypeCopy(data2)
    if GoodyIni.mutex>0:
        # print('readGoodyAry mutex >0')
        continueRun=True
    else:
        # print('readGoodyAry mutex ==0')
        continueRun=False
    return GoodyIni, continueRun

def readLogDirAry():
    LogDirIni=strPythonLog()
    mName="PythonDirInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strPythonLog),mName)#,access=mmap.ACCESS_READ)
    data2= strPythonLog.from_buffer(shmem3)
    LogDirIni=ctypeCopy(data2)
    if LogDirIni.mutex>0:
        # print('readGoodyAry mutex >0')
        continueRun=True
    else:
        # print('readGoodyAry mutex ==0')
        continueRun=False
    return LogDirIni, continueRun

def readRawPosAry():
# def readBodyPosAry():
    RawPosIni=strPoseAry()
    mName="RawPosInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strPoseAry),mName)#,access=mmap.ACCESS_READ)
    data2= strPoseAry.from_buffer(shmem3)
    RawPosIni=ctypeCopy(data2)
    if RawPosIni.mutex>0:
        # print('readBodyPosAry mutex >0')
        continueRun=True
    else:
        # print('readBodyPosAry mutex ==0')
        continueRun=False
    return RawPosIni, continueRun

def readBodyPosAry():
# def readRawPosAry():
    BodyPosIni=strBodyPosAry()
    mName="BodyPosInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBodyPosAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBodyPosAry.from_buffer(shmem3)
    BodyPosIni=ctypeCopy(data2)
    if BodyPosIni.mutex>0:
        # print('readBodyPosAry mutex >0')
        continueRun=True
    else:
        # print('readBodyPosAry mutex ==0')
        continueRun=False
    return BodyPosIni, continueRun

# use ping-pong scheme to read Hand gesture points
def readHandAry():
    handidx=0
    mName="HandIndex"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(ctypes.c_int),mName)#,access=mmap.ACCESS_READ)
    data2= ctypes.c_int.from_buffer(shmem3)
    handidx=ctypeCopy(data2)

    HandIni=strHandAry()
    if (handidx==1):
        mName="HandInit1"
    else:
        mName="HandInit2"
    shmem4 = mmap.mmap(-1, ctypes.sizeof(strHandAry),mName)#,access=mmap.ACCESS_READ)
    data3= strHandAry.from_buffer(shmem4)
    HandIni=ctypeCopy(data3)
    if HandIni.mutex>0:
        #print('readHandAry mutex >0')
        continueRun=True
    else:
        #print('readHandAry mutex ==0')
        continueRun=False
    return HandIni, continueRun

def transFun(x0 , y0, ObjInfoIni,PI, objNum, camWidth, camHeight, xyRatio, shiftX, shiftY):
    x0=(1-x0)*camWidth*xyRatio+shiftX
    y0=y0*camHeight*xyRatio+shiftY
    x0 = (x0 - (ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].foregroundX0 + ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].foregroundWidth / 2)) * ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].xscale
    y0 = (y0 - (ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].foregroundY0 + ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].foregroundHeight / 2)) * ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].yscale
    ang = -(ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].rotAngle*math.pi / 180.0)
    newx = (x0 * math.cos(ang) + y0 * math.sin(ang))
    newy = (-x0 * math.sin(ang) + y0*math.cos(ang))
    newy = newy + math.tan(ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].shearH) * newx
    newx = newx + math.tan(ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].shearV) * newy
    newx = newx + ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].xstart
    newy = newy + ObjInfoIni.OBJInfo[PI*MAX_INFO_ENTITIES+objNum].ystart
    return newx, newy

def calculateScreenRatio(bodyPosIni, HandIni):
    ScreenWidth=bodyPosIni.ScreenWidth
    ScreenHeight=bodyPosIni.ScreenHeight
    camWidth=HandIni.CamWidth
    camHeight=HandIni.CamHeight
    xRatio=ScreenWidth / camWidth
    yRatio=ScreenHeight/ camHeight
    shiftX=0.0
    shiftY=0.0
    if (xRatio < yRatio):
        xyRatio=xRatio
    else:
        xyRatio=yRatio
    
    if (xRatio > xyRatio):
        shiftX = camWidth * (xRatio - xyRatio) / 2.0
    else:
        shiftY = camHeight * (yRatio - xyRatio) / 2.0
    
    return xyRatio, shiftX, shiftY, ScreenWidth, ScreenHeight
    

def HandTransform(HandIni, HandIniLast, HandTrans, ObjInfoIni, PI, objNum, ScreenWidth, ScreenHeight, xyRatio, shiftX, shiftY):
    HandOut=strHandAry()
    HandOut=HandTrans
    status=False
    oneHandPt=MAX_HAND_POINTS//MAX_PROJECT_PEOPLE//3
    startIdx=PI*oneHandPt # 0 person start from 0 to 20, 1 person start from 21 to 41
    stopIdx=startIdx+oneHandPt
    camWidth=HandIni.CamWidth
    camHeight=HandIni.CamHeight
    i=PI
    # for left hand
    if (HandIni.LHAccNo[i]!=HandIniLast.LHAccNo[i]):
        status=True
        HandOut.LHAccNo[i]=HandIni.LHAccNo[i]
        for i in range(startIdx,stopIdx):
            x0=HandIni.LeftHand[i*3]
            y0=HandIni.LeftHand[i*3+1]
            # assume that the camera is flipped
            newx, newy= transFun(x0 , y0, ObjInfoIni,PI, objNum, camWidth, camHeight, xyRatio, shiftX, shiftY)
            HandOut.LeftHand[i*3]=newx
            HandOut.LeftHand[i*3+1]=newy

    # for right hand
    i=PI
    if (HandIni.RHAccNo[i]!=HandIniLast.RHAccNo[i]):
        status=True
        HandOut.RHAccNo[i]=HandIni.RHAccNo[i]
        for i in range(startIdx,stopIdx):
            x0=HandIni.RightHand[i*3]
            y0=HandIni.RightHand[i*3+1]
            # assume that the camera is flipped
            newx, newy= transFun(x0 , y0, ObjInfoIni,PI, objNum, camWidth, camHeight, xyRatio, shiftX, shiftY)
            HandOut.RightHand[i*3]=newx
            HandOut.RightHand[i*3+1]=newy
    return HandOut, status

def HandinfoLog(filename, firstTime,HandIni,HandIniLast):
    if firstTime==0:
        f = open(filename, "w")
        content='time,AccNo,peopleIdx,handIdx,ptIdx,x,y,z,\n'
        f.write(content)
    elif firstTime>0:
        f = open(filename, "a")
        # content='not first time'
        # f.write(content)
        content=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        oneHandPt=21
        for i in range(0,MAX_HAND_ENTITIES):
            if (HandIni.LHAccNo[i]!=HandIniLast.LHAccNo[i]):
            #if (True):
                for j in range(0,oneHandPt):
                    if (j==0):
                        content1=content+","+str(HandIni.LHAccNo[i])+","+ str(i)+","+str(0)+","+str(j)+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+1])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
                    else:
                        content1=" , ,"+str(i)+","+str(0)+","+str(j)+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+1])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
            if (HandIni.RHAccNo[i]!=HandIniLast.RHAccNo[i]):
            #if (True):
                for j in range(0,oneHandPt):
                    if (j==0):
                        content1=content+","+str(HandIni.RHAccNo[i])+","+ str(i)+","+str(1)+","+str(j)+","+str(HandIni.RightHand[i*oneHandPt*3+j*3])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+1])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
                    else:
                        content1=" , ,"+str(i)+","+str(1)+","+str(j)+","+str(HandIni.RightHand[i*oneHandPt*3+j*3])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+1])+","+str(HandIni.LeftHand[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
    f.close()
    
def RawPoseLog(filename, firstTime,HandIni):
    if firstTime==0:
        f = open(filename, "w")
        content='time,peopleIdx,ptIdx,x,y,z,\n'
        f.write(content)
    elif firstTime>0:
        f = open(filename, "a")
        # content='not first time'
        # f.write(content)
        content=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        oneHandPt=33
        for i in range(0,2):
            #if (HandIni.LHAccNo[i]!=HandIniLast.LHAccNo[i]):
            if (True):
                for j in range(0,oneHandPt):
                    if (j==0):
                        content1=content+","+ str(i)+","+str(j)+","+str(HandIni.rawPose[i*oneHandPt*3+j*3])+","+str(HandIni.rawPose[i*oneHandPt*3+j*3+1])+","+str(HandIni.rawPose[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
                    else:
                        content1=" ,"+ str(i)+","+str(j)+","+str(HandIni.rawPose[i*oneHandPt*3+j*3])+","+str(HandIni.rawPose[i*oneHandPt*3+j*3+1])+","+str(HandIni.rawPose[i*oneHandPt*3+j*3+2])+"\n"
                        f.write(content1)
    f.close()

def readScriptAry():
    ScriptIni=strScriptConditionAry()
    mName="ScriptInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strScriptConditionAry),mName)#,access=mmap.ACCESS_READ)
    data2= strScriptConditionAry.from_buffer(shmem3)
    ScriptIni=ctypeCopy(data2)
    if ScriptIni.mutex>0:
        # print('readBodyPosAry mutex >0')
        continueRun=True
    else:
        # print('readBodyPosAry mutex ==0')
        continueRun=False
    return ScriptIni, continueRun

def readInfoOBJAry():
    OBJInfoIni=strOBJInfoInputAry()
    mName="OBJInfoInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJInfoInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJInfoInputAry.from_buffer(shmem3)
    OBJInfoIni=ctypeCopy(data2)
    if OBJInfoIni.mutex>0:
        # print('readInfoOBJAry mutex >0')
        continueRun=True
    else:
        # print('readInfoOBJAry mutex ==0')
        continueRun=False
    return OBJInfoIni, continueRun

def readFGC(FGCIniList, FGnum):
    for i in range(0,FGnum):
        mName="FGCInit"+str(i)
        shmem = mmap.mmap(-1, ctypes.sizeof(strFGCInput),mName)
        data = strFGCInput.from_buffer(shmem)
        #print('Python Program - Getting Data')
        if data.mutex>0:
            #input("Press Enter to continue...")
            FGCIniList[i]=data

def readFGCAry():
    mName="FGCInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGCInputAry.from_buffer(shmem3)
    return data2

def readFGCAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGCInputAry.from_buffer(shmem3)
    return data2

def readFGCAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strFGCInputAryBuffer.from_buffer(shmem3)
    return data2

def readBGCAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBGCInputAry.from_buffer(shmem3)
    return data2

def readBGCAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGCInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strBGCInputAryBuffer.from_buffer(shmem3)
    return data2

def readCUSCAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSCInputAry.from_buffer(shmem3)
    return data2

def readCUSCAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSCInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSCInputAryBuffer.from_buffer(shmem3)
    return data2

def readOBJCAryName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJCInputAry.from_buffer(shmem3)
    return data2

def readOBJCAryBufferName(mName):
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJCInputAryBuffer),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJCInputAryBuffer.from_buffer(shmem3)
    return data2

def readFGCAry2():
    FGCIni=strFGCInputAry()
    mName="FGCInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strFGCInputAry.from_buffer(shmem3)
    FGCIni=ctypeCopy(data2)
    if (FGCIni.mutex>0):
        # print('mutex of FGCIni >0')
        continueRun=True
    else:
        # print('FGCIni mutex ==0')
        continueRun=False
    #logfileFGC(FGCIni, filename2,init_time,firstTime)
    return FGCIni, continueRun

def readBGCAry():
    BGCIni=strBGCInputAry()
    mName="BGCInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strBGCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strBGCInputAry.from_buffer(shmem3)
    BGCIni=ctypeCopy(data2)
    if (BGCIni.mutex>0):
        # print('mutex of BGCIni >0')
        continueRun=True
    else:
        # print('BGCIni mutex ==0')
        continueRun=False
    #logfileFGC(FGCIni, filename2,init_time,firstTime)
    return BGCIni, continueRun

def readCUSCAry():
    CUSCIni=strCUSCInputAry()
    mName="CUSCInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strCUSCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strCUSCInputAry.from_buffer(shmem3)
    CUSCIni=ctypeCopy(data2)
    if (CUSCIni.mutex>0):
        # print('mutex of CUSCIni >0')
        continueRun=True
    else:
        # print('CUSCIni mutex ==0')
        continueRun=False
    #logfileFGC(FGCIni, filename2,init_time,firstTime)
    return CUSCIni, continueRun

def readOBJCAry():
    OBJCIni=strOBJCInputAry()
    mName="OBJCInit"
    shmem3 = mmap.mmap(-1, ctypes.sizeof(strOBJCInputAry),mName)#,access=mmap.ACCESS_READ)
    data2= strOBJCInputAry.from_buffer(shmem3)
    OBJCIni=ctypeCopy(data2)
    if (OBJCIni.mutex>0):
        # print('mutex of OBJCIni >0')
        continueRun=True
    else:
        # print('OBJCIni mutex ==0')
        continueRun=False
    #logfileFGC(FGCIni, filename2,init_time,firstTime)
    return OBJCIni, continueRun

def writeFGInfo(idx,FGInfoInputList):
    strName='FGInfo'+str(idx)
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInput),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGInfoInput.from_buffer(shmem2)
    data1.mutex=0
    #TransferData.fill(data)
    data1=FGInfoInputList[idx]
    data1.mutex=1

def writeFGInfo2(FGInfoIni):
    strName='FGInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGInfoInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(FGInfoIni, data1)
    data1.mutex=1

def writeFGInfo3(FGInfoBuffer):
    strName='FGInfoBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGInfoInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(FGInfoBuffer, data1)
    data1.mutex=1

def writeBGInfo(BGInfoIni):
    strName='BGInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBGInfoInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strBGInfoInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(BGInfoIni, data1)
    data1.mutex=1

def writeBGInfo3(BGInfoBuffer):
    strName='BGInfoBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBGInfoInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strBGInfoInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(BGInfoBuffer, data1)
    data1.mutex=1

def writeCUSInfo(CUSInfoIni):
    strName='CUSInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strCUSInfoInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strCUSInfoInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(CUSInfoIni, data1)
    data1.mutex=1

def writeCUSInfo3(CUSInfoBuffer):
    strName='CUSInfoBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strCUSInfoInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strCUSInfoInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(CUSInfoBuffer, data1)
    data1.mutex=1

def writeOBJInfo(OBJInfoIni):
    strName='OBJInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strOBJInfoInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strOBJInfoInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(OBJInfoIni, data1)
    data1.mutex=1

def writeOBJInfo3(OBJInfoBuffer):
    strName='OBJInfoBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strOBJInfoInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strOBJInfoInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(OBJInfoBuffer, data1)
    data1.mutex=1

def writeFGInfoAry(FGNo,FGList,FGInfoInput):
    strName='FGInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGInfoInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGInfoInputAry.from_buffer(shmem2)
    data1.mutex=0
    #TransferData.fill(data)
    for i in range(0,MAX_INFO_ENTITIES):
        for j in range(0,FGNo):
            if FGList[j] ==i:
                data1.FGInfo[i]=FGInfoInput.FGInfo[i]
                data1.verified[i]=1
    data1.mutex=1

def writeFGC(idx,FGCInputList):
    strName='FGC'+str(idx)
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGCInput),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGCInput.from_buffer(shmem2)
    data1.mutex=0
    #TransferData.fill(data)
    data1=FGCInputList[idx]
    data1.mutex=1

def writeFGC2(FGCInput):
    strName='FGC'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGCInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(FGCInput, data1)
    data1.mutex=1

def writeFGC3(FGCBuffer):
    strName='FGCBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGCInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(FGCBuffer, data1)
    data1.mutex=1

def writeBGC(BGCInput):
    strName='BGC'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBGCInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strBGCInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(BGCInput, data1)
    data1.mutex=1

def writeBGC3(BGCBuffer):
    strName='BGCBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBGCInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strBGCInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(BGCBuffer, data1)
    data1.mutex=1

def writeCUSC(CUSCInput):
    strName='CUSC'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strCUSCInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strCUSCInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(CUSCInput, data1)
    data1.mutex=1

def writeCUSC3(CUSCBuffer):
    strName='CUSCBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strCUSCInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strCUSCInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(CUSCBuffer, data1)
    data1.mutex=1

def writeOBJC(OBJCInput):
    strName='OBJC'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strOBJCInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strOBJCInputAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(OBJCInput, data1)
    data1.mutex=1

def writeOBJC3(OBJCBuffer):
    strName='OBJCBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strOBJCInputAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strOBJCInputAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(OBJCBuffer, data1)
    data1.mutex=1

def writeGoody(GoodyInput):
    strName='GoodyInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strGoodyAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strGoodyAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(GoodyInput, data1)
    data1.mutex=1

def writeGoody3(GoodyBuffer):
    strName='GoodyBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strGoodyAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strGoodyAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(GoodyBuffer, data1)
    data1.mutex=1

def writeBodyPos(GoodyInput):
    strName='BodyPosInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBodyPosAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strBodyPosAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(GoodyInput, data1)
    data1.mutex=1

def writeBodyPos3(bodyPosBuffer):
    strName='BodyPosBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strBodyPosAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strBodyPosAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(bodyPosBuffer, data1)
    data1.mutex=1

def writeScript(ScriptInput):
    strName='ScriptInfo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strScriptConditionAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strScriptConditionAry.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(ScriptInput, data1)
    data1.mutex=1

def writeScript3(ScriptBuffer):
    strName='ScriptBuffer'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strScriptConditionAryBuffer),strName)#,access=mmap.ACCESS_READ)
    data1 = strScriptConditionAryBuffer.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(ScriptBuffer, data1)
    data1.mutex=1

def writeFGCAry(FGCNo,FGCList,FGCInput):
    strName='FGC'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strFGCInputAry),strName)#,access=mmap.ACCESS_READ)
    data1 = strFGCInputAry.from_buffer(shmem2)
    data1.mutex=0
    #TransferData.fill(data)
    for i in range(0,MAX_INFO_ENTITIES):
        for j in range(0,FGCNo):
            if FGCList[j] ==i:
                data1.FGInfoC[i]=FGCInput.FGInfoC[i]
                data1.verified[i]=1
    data1.mutex=1

def writeInfoInputNum(InfoInputNo):
    strName='InfoInputNo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoInputNo),strName)#,access=mmap.ACCESS_READ)
    data1 = strInfoInputNo.from_buffer(shmem2)
    data1.mutex=0
    data1=InfoInputNo
    data1.mutex=1

def readInfoInputNum():
    strName='InfoInputNo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoInputNo),strName)#,access=mmap.ACCESS_READ)
    data1 = strInfoInputNo.from_buffer(shmem2)
    return data1

def readInfoInputNum2():
    strName='InfoInputNo2'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoInputNo2),strName)#,access=mmap.ACCESS_READ)
    data1 = strInfoInputNo2.from_buffer(shmem2)
    return data1

def writeInfoInputNum2(InfoInputNo):
    strName='InfoInputNo'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoInputNo),strName)#,access=mmap.ACCESS_READ)
    data1 = strInfoInputNo.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(InfoInputNo, data1)
    data1.mutex=1

def writeInfoInputNum2B(InfoInputNo2):
    strName='InfoInputNo2'
    shmem2 = mmap.mmap(-1, ctypes.sizeof(strInfoInputNo2),strName)#,access=mmap.ACCESS_READ)
    data1 = strInfoInputNo2.from_buffer(shmem2)
    data1.mutex=0
    ctypeCopy2(InfoInputNo2, data1)
    data1.mutex=1

# def print_data2(data):
#     print('stageNo: ' + str(data.stageNo))
#     print('FGNo: ' + str(data.FGNo))
#     print('mutex: ' + str(data.mutex))
#     print('endSignal: ' + str(data.endSignal))

# def print_data3(data):
#     print('verified: ' + str(data.verified))
#     print('mutex: ' + str(data.mutex))
#     print('FGInfo.forewidth: ' + str(data.FGInfo.foregroundWidth))
#     print('FGInfo.foreheight: ' + str(data.FGInfo.foregroundHeight))

# def print_data4(data):
#     #print('verified: ' + str(data.verified))
#     print('mutex: ' + str(data.mutex))
#     for i in range(0,4):
#         print('FGInfo.forewidth: ' + str(data.FGInfo[i].foregroundWidth))
#         print('FGInfo.foreheight: ' + str(data.FGInfo[i].foregroundHeight))


def SetupInitial():
    data2a=readInfoFGAryName("FGInfoInit")
    data2b=readInfoBGAryName("BGInfoInit")
    data2c=readInfoCUSAryName("CUSInfoInit")
    data2d=readInfoOBJAryName("OBJInfoInit")

    data4a=readInfoOut()

    data3a=readFGCAryName("FGCInit")
    data3b=readBGCAryName("BGCInit")
    data3c=readCUSCAryName("CUSCInit")
    data3d=readOBJCAryName("OBJCInit")


    data1a=readInfoFGAryName("FGInfo")
    data1b=readInfoBGAryName("BGInfo")
    data1c=readInfoCUSAryName("CUSInfo")
    data1d=readInfoOBJAryName("OBJInfo")
    data1e=readInfoFGAryBufferName("FGInfoBuffer")
    data1f=readInfoBGAryBufferName("BGInfoBuffer")
    data1g=readInfoCUSAryBufferName("CUSInfoBuffer")
    data1h=readInfoOBJAryBufferName("OBJInfoBuffer")

    data5a=readInfoInputNum()
    data5b=readInfoInputNum2()

    data6a=readFGCAryName("FGC")
    data6b=readBGCAryName("BGC")
    data6c=readCUSCAryName("CUSC")
    data6d=readOBJCAryName("OBJC")
    data6e=readFGCAryBufferName("FGCBuffer")
    data6f=readBGCAryBufferName("BGCBuffer")
    data6g=readCUSCAryBufferName("CUSCBuffer")
    data6h=readOBJCAryBufferName("OBJCBuffer")

    data7a=readGoodyAryName("GoodyInit")
    data7b=readGoodyAryName("GoodyInfo")
    data7c=readGoodyAryBufferName("GoodyBuffer")

    data8a=readBodyPosAryName("BodyPosInit")
    data8b=readBodyPosAryName("BodyPosInfo")
    data8c=readBodyPosAryBufferName("BodyPosBuffer")

    data9a=readLogDirAryName("PythonDirInit")

    data10a=readScriptAryName("ScriptInit")
    data10b=readScriptAryName("ScriptInfo")
    data10c=readScriptAryBufferName("ScriptBuffer")

    data11a=readHandAryName("HandInit1")
    data11b=readHandAryName("HandInit2")
    data11c=readHandIdxName("HandIndex")

    if (rawPoseEnbl==1):
        data12a=readRawPosAryName("RawPosInit")
    else:
        data12a=-1

    return [data12a,data7c,data8c,data10c,data6e, data6f,data6g,data6h,data1e,data1f,data1g,data1h,data2a,data4a,data3a,data1a,data5a,data5b,data6a,data2b,data3b,data1b,data6b,data2c,data3c,data1c,data6c,data2d,data3d,data1d,data6d,data7a,data7b,data8a,data8b,data9a,data10a,data10b,data11a,data11b,data11c]

def CheckStage():
    #EachPNo=[0]*MAX_PROJECT_PEOPLE
    infoOut=readInfoOut()
    infoOut1=ctypeCopy(infoOut)
    #print ('stageNO='+str(infoOut.stageNo))
    # endSignal=infoOut.endSignal
    # currentStage=infoOut.stageNo
    # FGNo=infoOut.FGNo
    # CUSNo=infoOut.CUSNo
    # BGNo=infoOut.BGNo
    # PersonNo=infoOut.PersonNo
    # for i in range(0,PersonNo):
	# 	EachPNo[i]=infoOut.EachPNo[i]
    # return endSignal,currentStage,BGNo,FGNo,CUSNo,PersonNo,EachPNo
    return infoOut1

def ReadStageInitial(stageNoforChange,FGInfoIni,FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,GoodyIni,BodyPosIni,LogDirIni,ScriptIni,firstTimeIni,previousStage,InfoInputNo):
    #only read once every stage from main program for FG,BG, and Obj,...
    # EachPNo=[0]*MAX_PROJECT_PEOPLE
    # endSignal,currentStage,BGNo,FGNo,CUSNo,PersonNo,EachPNo=CheckStage()
    #infoOut= strInfoOut()
    numStages=0

    if isinstance(stageNoforChange, list): 
        numStages=len(stageNoforChange)
        stageNoforChange1=stageNoforChange
    else:
        stageNoforChange1=[stageNoforChange]
        numStages=1

    # print (stageNoforChange1)
    # print (numStages)
    lastTimeIni=firstTimeIni
    infoOut= CheckStage()

    continueRun=False
    currentStage=infoOut.stageNo
    if (currentStage!=previousStage):
        firstTimeIni=0
    # print('inside firstTimeIni='+str(firstTimeIni))
    # print('currentStage='+str(currentStage))
    # print('prviousStage='+str(previousStage))
    previousStage=currentStage
    FGNo=infoOut.FGNo
    CUSNo=infoOut.CUSNo
    BGNo=infoOut.BGNo
    GoodyNo=infoOut.GoodyNo
    BodyNo=infoOut.BodyNo
    ScriptNo=infoOut.ScriptConditionNo
    filename1="C:\\Data_log\\rawPos_"+str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".csv"

    PersonExist=False
    for i in range(0,infoOut.PersonNo):
        if infoOut.EachPNo[i] > 0:
            PersonExist=True

    # print('person Exist'+str(PersonExist))
    InStage=False

    for i in range(0,numStages):
        stageNoforChange2=stageNoforChange1[i]
        if (currentStage==stageNoforChange2):
            if (firstTimeIni!=0):
                firstTimeIni+= 1
            else:
                firstTimeIni= 1
                # print('start to readLogDirAry')
                while (not continueRun):
                    LogDirInfo1,continueRun=readLogDirAry() # only read once every stage
                    if (ScriptNo >0 and continueRun):
                        ScriptInfo,continueRun= readScriptAry()
                    else:
                        ScriptInfo=ScriptIni
                # print('end to readLogDirAry')
                dirStr=str(LogDirInfo1.LogDir)
                x = dirStr.split("\\")
                size1=len(x)
                
                if size1>0:
                    LogDirInfo=x[size1-1]
                    LogDirInfo=LogDirInfo.strip()
                    LogDirInfo=LogDirInfo[:-1] # remove the last character
                    LogDirInfo="C:\\integem\\pythonLogs\\"+LogDirInfo
                else:
                    LogDirInfo=""
                continueRun=False
                    #LogDirInfo.replace("", "was")
            while (not continueRun):
                # print('Python in stage')
                continueRun=True
                #if (not FGReceived):
                # print('Python in readInfoFGAry')
                #print('currentStage='+str(currentStage))
                

                if (FGNo >0):
                    FGInfo,continueRun=readInfoFGAry2()
                    if (continueRun):
                        FGC,continueRun=readFGCAry2()
                else:
                    FGInfo=FGInfoIni
                    FGC=FGCIni
                if (BGNo >0 and continueRun):
                    BGInfo,continueRun=readInfoBGAry()
                    if (continueRun):
                        BGC,continueRun=readBGCAry()
                else:
                    BGInfo=BGInfoIni
                    BGC=BGCIni
                if (CUSNo >0 and continueRun):
                    CUSInfo,continueRun=readInfoCUSAry()
                    if (continueRun):
                        CUSC,continueRun=readCUSCAry()
                else:
                    CUSInfo=CUSInfoIni
                    CUSC=CUSCIni
                if (PersonExist and continueRun):
                    OBJInfo,continueRun=readInfoOBJAry()
                    #print('OBJ info xstart='+str(OBJInfo.OBJInfo[0].xstart))
                    if (continueRun):
                        OBJC,continueRun=readOBJCAry()
                else:
                    OBJInfo=OBJInfoIni
                    OBJC=OBJCIni
                # if (GoodyNo >0 and continueRun):
                #     GoodyInfo,continueRun=readGoodyAry()
                if (GoodyNo >0 and continueRun):
                    GoodyInfo1,continueRun=readGoodyAry()
                    noName=True
                    for i in range(MAX_INFO_ENTITIES):
                        len1=len(GoodyInfo1.GoodyInfo[i].goodyString)
                        if len1>0:
                            noName=False
                    if noName:
                        GoodyInfo=GoodyIni
                    else:
                        GoodyInfo=GoodyInfo1
                else:
                    GoodyInfo=GoodyIni
                if (BodyNo >0 and continueRun):
                    BodyPosInfo,continueRun=readBodyPosAry()
                else:
                    BodyPosInfo=BodyPosIni

                saveNum=firstTimeIni%5
                if (saveNum==0 and rawPoseEnbl==1):
                    RawPosInfo,continueRun=readRawPosAry()
                    RawPoseLog(filename1,firstTimeIni-1,RawPosInfo)

                # if (continueRun):
                #     print('before script: continueRun')
                # else:
                #     print('before script: not continueRun')
                
                # if (continueRun):
                #     print('continueRun')
                # else:
                #     print('not continueRun')
            InStage=True
            if (firstTimeIni==1):
                return infoOut,PersonExist,FGInfo, FGC,BGInfo, BGC, CUSInfo, CUSC,OBJInfo, OBJC,GoodyInfo,BodyPosInfo,LogDirInfo,ScriptInfo,firstTimeIni,previousStage
            else:
                return infoOut,PersonExist,FGInfo, FGC,BGInfo, BGC, CUSInfo, CUSC,OBJInfo, OBJC,GoodyInfo,BodyPosInfo,LogDirIni,ScriptIni,firstTimeIni,previousStage
            # return infoOut,PersonExist, FGInfoIni, FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,firstTimeIni,previousStage
    if (not InStage):
        firstTimeIni=0
        # reset the InfoInputNo
        if (firstTimeIni==0 and lastTimeIni>0):
            if (InfoInputNo.VersionNo>=CURRENT_VERSION_NO):
                resetInfoInputNoAry()
            elif (InfoInputNo.VersionNo>=PAST_VERSION_NO2):
                resetInfoInputNo()
        return infoOut,PersonExist, FGInfoIni, FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,GoodyIni,BodyPosIni,LogDirIni,ScriptIni,firstTimeIni,previousStage

def OutputStageChanges(FGInfoIni,FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,InfoInputNo):

    if (InfoInputNo.FGNo >0 ):
        writeFGInfo2(FGInfoIni)
        # print('xstartVal:'+str(FGInfoIni.FGInfo[0].xstart))
    
    if (InfoInputNo.FGCNo >0 ):
        writeFGC2(FGCIni)
        #print('scale:'+str(FGCIni.FGInfoC[itemNoC].infoBasicFGC.Dinitialscalex))

    if (InfoInputNo.BGNo >0 ):
        writeBGInfo(BGInfoIni)
    
    if (InfoInputNo.BGCNo >0 ):
        writeBGC(BGCIni)

    if (InfoInputNo.CUSNo >0 ):
        writeCUSInfo(CUSInfoIni)
    
    if (InfoInputNo.CUSCNo >0 ):
        writeCUSC(CUSCIni)
    
    if (InfoInputNo.OBJNo >0 ):
        writeOBJInfo(OBJInfoIni)
    
    if (InfoInputNo.OBJCNo >0 ):
        writeOBJC(OBJCIni)
               
    writeInfoInputNum2(InfoInputNo)
    print('InfoInputNo Output')

def OutputStageChangesAry(FGInfoBuffer,FGCBuffer,BGInfoBuffer,BGCBuffer,CUSInfoBuffer,CUSCBuffer,OBJInfoBuffer,OBJCBuffer,InfoInputNo):

    if (InfoInputNo.FGNo >0 ):
        writeFGInfo3(FGInfoBuffer)
        # print('xstartVal:'+str(FGInfoIni.FGInfo[0].xstart))
    
    if (InfoInputNo.FGCNo >0 ):
        writeFGC3(FGCBuffer)
        #print('scale:'+str(FGCIni.FGInfoC[itemNoC].infoBasicFGC.Dinitialscalex))

    if (InfoInputNo.BGNo >0 ):
        writeBGInfo3(BGInfoBuffer)
    
    if (InfoInputNo.BGCNo >0 ):
        writeBGC3(BGCBuffer)

    if (InfoInputNo.CUSNo >0 ):
        writeCUSInfo3(CUSInfoBuffer)
    
    if (InfoInputNo.CUSCNo >0 ):
        writeCUSC3(CUSCBuffer)
    
    if (InfoInputNo.OBJNo >0 ):
        writeOBJInfo3(OBJInfoBuffer)
    
    if (InfoInputNo.OBJCNo >0 ):
        writeOBJC3(OBJCBuffer)
               
    writeInfoInputNum2(InfoInputNo)
    print('InfoInputNo Output')

def OutputStageChanges2(GoodyIni,BodyPosIni,ScriptIni,InfoInputNo2):
    if (InfoInputNo2.GoodyNo >0 ):
        writeGoody(GoodyIni)
    
    # currently no write back for bodyPosition to IntegemCam program
    InfoInputNo2.BodyNo=0
    if (InfoInputNo2.BodyNo >0 ):
        writeBodyPos(BodyPosIni)

    if(InfoInputNo2.ScriptConditionNo>0):
        # print('write out ScriptIni')
        # print('ScriptIni.verified[0]'+str(ScriptIni.verified[0]))
        writeScript(ScriptIni)
    # print('InfoInputNo2.GoodyNo'+str(InfoInputNo2.GoodyNo))           
    writeInfoInputNum2B(InfoInputNo2)
    # print('InfoInputNo2 Output')

def OutputStageChanges2Ary(GoodyBuffer,BodyPosBuffer,ScriptBuffer,InfoInputNo2):
    if (InfoInputNo2.GoodyNo >0 ):
        writeGoody3(GoodyBuffer)
    
    # currently no write back for bodyPosition to IntegemCam program
    InfoInputNo2.BodyNo=0
    if (InfoInputNo2.BodyNo >0 ):
        writeBodyPos3(BodyPosBuffer)

    if(InfoInputNo2.ScriptConditionNo>0):
        # print('write out ScriptIni')
        # print('ScriptIni.verified[0]'+str(ScriptIni.verified[0]))
        writeScript3(ScriptBuffer)
    # print('InfoInputNo2.GoodyNo'+str(InfoInputNo2.GoodyNo))           
    writeInfoInputNum2B(InfoInputNo2)
    # print('InfoInputNo2 Output')

def clearInfoInputNo(InfoInputNo):
    InfoInputNo.FGNo=0
    InfoInputNo.FGCNo=0
    InfoInputNo.BGNo=0
    InfoInputNo.BGCNo=0
    InfoInputNo.CUSNo=0
    InfoInputNo.CUSCNo=0
    InfoInputNo.OBJNo=0
    InfoInputNo.OBJCNo=0

def clearInfoInputNo2(InfoInputNo2):
    InfoInputNo2.GoodyNo=0
    InfoInputNo2.BodyNo=0
    InfoInputNo2.ScriptConditionNo=0


def resetInfoInputNo():


    FGInfoIni=strFGInfoInputAry()
    FGCIni=strFGCInputAry()
    BGInfoIni=strBGInfoInputAry()
    BGCIni=strBGCInputAry()
    CUSInfoIni=strCUSInfoInputAry()
    CUSCIni=strCUSCInputAry()
    OBJInfoIni=strOBJInfoInputAry()
    OBJCIni=strOBJCInputAry()
    GoodyIni=strGoodyAry()
    BodyPosIni=strBodyPosAry()
    ScriptIni=strScriptConditionAry()

    for i in range(0,MAX_INFO_ENTITIES):
        FGInfoIni.verified[i]=0
        FGCIni.verified[i]=0
        BGInfoIni.verified[i]=0
        BGCIni.verified[i]=0
        CUSInfoIni.verified[i]=0
        CUSCIni.verified[i]=0
        GoodyIni.verified[i]=0
        ScriptIni.verified[i]=0
    for i in range(0,MAX_COMB_ENTITIES):
        OBJInfoIni.verified[i]=0
        OBJCIni.verified[i]=0

    BodyPosIni.verified=0

    writeFGInfo2(FGInfoIni)
    writeFGC2(FGCIni)
    writeBGInfo(BGInfoIni)
    writeBGC(BGCIni)
    writeCUSInfo(CUSInfoIni)
    writeCUSC(CUSCIni)
    writeOBJInfo(OBJInfoIni)
    writeOBJC(OBJCIni)
    writeGoody(GoodyIni)
    writeBodyPos(BodyPosIni)
    writeScript(ScriptIni)

    InfoInputNo=strInfoInputNo()
    clearInfoInputNo(InfoInputNo)
    InfoInputNo.stageNo=0
    writeInfoInputNum2(InfoInputNo)

    InfoInputNo2=strInfoInputNo2()
    clearInfoInputNo2(InfoInputNo2)
    writeInfoInputNum2B(InfoInputNo2)

def resetInfoInputNoAry():

    FGInfoIni=strFGInfoInputAry()
    FGCIni=strFGCInputAry()
    BGInfoIni=strBGInfoInputAry()
    BGCIni=strBGCInputAry()
    CUSInfoIni=strCUSInfoInputAry()
    CUSCIni=strCUSCInputAry()
    OBJInfoIni=strOBJInfoInputAry()
    OBJCIni=strOBJCInputAry()
    GoodyIni=strGoodyAry()
    BodyPosIni=strBodyPosAry()
    ScriptIni=strScriptConditionAry()

    FGInfoBuffer=strFGInfoInputAryBuffer()
    BGInfoBuffer=strBGInfoInputAryBuffer()
    CUSInfoBuffer=strCUSInfoInputAryBuffer()
    OBJInfoBuffer=strOBJInfoInputAryBuffer()
    FGCBuffer=strFGCInputAryBuffer()
    BGCBuffer=strBGCInputAryBuffer()
    CUSCBuffer=strCUSCInputAryBuffer()
    OBJCBuffer=strOBJCInputAryBuffer()
    GoodyBuffer=strGoodyAryBuffer()
    BodyPosBuffer=strBodyPosAryBuffer()
    ScriptBuffer=strScriptConditionAryBuffer()

    for i in range(0,MAX_INFO_ENTITIES):
        for j in range(0,MAX_BUFFER_NUM):
            
            FGInfoBuffer.InfoBuffer[j].verified[i]=0
            BGInfoBuffer.InfoBuffer[j].verified[i]=0
            CUSInfoBuffer.InfoBuffer[j].verified[i]=0
            FGCBuffer.InfoBuffer[j].verified[i]=0
            BGCBuffer.InfoBuffer[j].verified[i]=0
            CUSCBuffer.InfoBuffer[j].verified[i]=0
            GoodyBuffer.InfoBuffer[j].verified[i]=0
            ScriptBuffer.InfoBuffer[j].verified[i]=0

        # FGInfoIni.verified[i]=0
        # FGCIni.verified[i]=0
        # BGInfoIni.verified[i]=0
        # BGCIni.verified[i]=0
        # CUSInfoIni.verified[i]=0
        # CUSCIni.verified[i]=0
        # GoodyIni.verified[i]=0
        # ScriptIni.verified[i]=0


    for i in range(0,MAX_COMB_ENTITIES):
        for j in range(0,MAX_BUFFER_NUM):
            OBJInfoBuffer.InfoBuffer[j].verified[i]=0
            OBJCBuffer.InfoBuffer[j].verified[i]=0
        # OBJInfoIni.verified[i]=0
        # OBJCIni.verified[i]=0

    # BodyPosIni.verified=0
    for j in range(0,MAX_BUFFER_NUM):
        BodyPosBuffer.InfoBuffer[j].verified=0

    
    writeFGInfo3(FGInfoBuffer)
    writeFGC3(FGCBuffer)
    writeBGInfo3(BGInfoBuffer)
    writeBGC3(BGCBuffer)
    writeCUSInfo3(CUSInfoBuffer)
    writeCUSC3(CUSCBuffer)
    writeOBJInfo3(OBJInfoBuffer)
    writeOBJC3(OBJCBuffer)
    writeGoody3(GoodyBuffer)
    writeBodyPos3(BodyPosBuffer)
    writeScript3(ScriptBuffer)

    # writeFGInfo2(FGInfoIni)
    # writeFGC2(FGCIni)
    # writeBGInfo(BGInfoIni)
    # writeBGC(BGCIni)
    # writeCUSInfo(CUSInfoIni)
    # writeCUSC(CUSCIni)
    # writeOBJInfo(OBJInfoIni)
    # writeOBJC(OBJCIni)
    # writeGoody(GoodyIni)
    # writeBodyPos(BodyPosIni)
    # writeScript(ScriptIni)

    InfoInputNo=strInfoInputNo()
    clearInfoInputNo(InfoInputNo)
    InfoInputNo.stageNo=0
    writeInfoInputNum2(InfoInputNo)

    InfoInputNo2=strInfoInputNo2()
    clearInfoInputNo2(InfoInputNo2)
    writeInfoInputNum2B(InfoInputNo2)

# PY_OFF = 2000

# def fill(data):
#     data.exLg = PY_OFF + 1.0
#     data.other = PY_OFF + 2.0
#     data.more = PY_OFF + 3
#     data.more2 = PY_OFF + 4
#     data.next = 5
#     data.statusReady = True

#     data.status.numAvailable = PY_OFF + 7
#     data.status.numUsed = PY_OFF + 8

#     index = 9
#     for i in range(MAX_ENTITIES):
#         data.entities[i].x = PY_OFF + index
#         index += 1
#         data.entities[i].y = PY_OFF + index
#         index += 1
#         data.entities[i].z = PY_OFF + index
#         index += 1


# def print_entity(data, number):
#     e = data.entities[number]
#     print('entities[' + str(number) + ']: ' + str(e.x) + ' ' + str(e.y) +
#           ' ' + str(e.z))


# def print_data(data):
#     print('exLg: ' + str(data.exLg))
#     print('other: ' + str(data.other))
#     print('more: ' + str(data.more))
#     print('more2: ' + str(data.more2))
#     print('next: ' + str(data.next))
#     print('statusReady: ' + str(data.statusReady))
#     print('numAvailable: ' + str(data.status.numAvailable))
#     print('numUsed: ' + str(data.status.numUsed))
#     print_entity(data, 0)
#     print_entity(data, 1)
#     print_entity(data, 15)
#     print_entity(data, MAX_ENTITIES - 1)