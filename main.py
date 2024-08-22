'''
main.py
This file is to run the main loop for python program
version 1.0 on 1/1/2022
a. defined the basic functions.
version 1.1 on 10/24/2022
a. add debugUI function
version 1.2 on 11/22/2022
a. at the first iteration of stage, clean the old transition verify to zero to avoid trigger from last cycle.
version 1.3 on 3/31/2023
a. define screenWidth and screenHeight based on the system setting
version 1.4 on 10/12/2023
a. add hd_ratio to read from Zconfigure.txt
'''

import iCreatorData
import handgesture
import sys
from datetime import datetime
from time import time
from time import sleep
import mmap
import ctypes
from random import randint
import logging
import os
import random
import threading
import debugUI as debug


def addCommnets(content):
    # add # as comments before separation line ##**##
    paragraph1 = content.split('##**##')
    lines = paragraph1[0].splitlines()
    newlines = ""
    for line1 in lines:
        newlines = newlines+"# "+line1+"\n"
    newlines = newlines+"# above is all comments"
    if len(paragraph1) > 1:
        newlines = newlines+paragraph1[1]
    return newlines

def read_hd_ratio():
    conf_path = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "Integem",
        "IntegemCam",
        "Zconfigure.txt",
    )
    if not os.path.exists(conf_path):
        return 1
    with open(conf_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("HDratio="):
                return int(line.split("=")[1].strip())

    return 1

MAX_INFO_ENTITIES = 8
# PAST_VERSION_NO=iCreatorData.PAST_VERSION_NO
CURRENT_VERSION_NO = iCreatorData.CURRENT_VERSION_NO

BODYNUMBER = 6

dirName = os.path.dirname(os.path.abspath(__file__))
folder = dirName.split("\\")
logfolder = os.path.join("C:\\integem\\pythonLogs\\"+folder[-1])
if not os.path.isdir(logfolder):
    os.mkdir(logfolder)
printFilename = logfolder+"\\print.log"

scriptDir = os.path.join(dirName, 'script')
scripts = os.listdir(scriptDir)
# scriptCodes = [open(os.path.join(scriptDir, file),"r").read() for file in scripts]
# scriptCodeFileNames = [file.split(".")[0].split("_")[1] for file in scripts]
scriptCodes = {}
for file in scripts:
    if (len(file.split(".")) > 1 and file.split(".")[1] == 'py'):
        # scriptCodes[file.split(".")[0]] = open(os.path.join(scriptDir, file),"r").read().split('##**##')[1]
        scriptCodes[file.split(".")[0]] = addCommnets(
            open(os.path.join(scriptDir, file), "r").read())
initial_setup_code = scriptCodes.get('initial_setup')
initial_stage_code = scriptCodes.get('initial_stage')

# userfile = os.path.join(dirName, "user.py")
# usercode = open(userfile,"r").read().split('##**##')
# usercode0 = usercode[0]
# usercode0len = len(usercode[0])
# usercode1 = usercode[1]
# usercode1len = len(usercode[1])
userUtilsfile = os.path.join(dirName, "userUtils.py")
# usercode = open(userUtilsfile,"r").read().split('##**##')[1]
usercode = addCommnets(open(userUtilsfile, "r").read())

exec(usercode)
del usercode                # delete variable


# debug ui setup
try:
    t = threading.Thread(target=debug.run)
    t.start()
except Exception as e:
    filename = logfolder+"\\logError.log"
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.exception(str(e))
    loginfoprint(printFilename,1,"For plotting, please install matplotlib -- https://matplotlib.org/stable/users/installing/index.html")


try:

    # region ############ Must declare related variable.
    FGInfoIni = iCreatorData.strFGInfoInputAry()
    FGCIni = iCreatorData.strFGCInputAry()
    BGInfoIni = iCreatorData.strBGInfoInputAry()
    BGCIni = iCreatorData.strBGCInputAry()
    CUSInfoIni = iCreatorData.strCUSInfoInputAry()
    CUSCIni = iCreatorData.strCUSCInputAry()
    OBJInfoIni = iCreatorData.strOBJInfoInputAry()
    OBJCIni = iCreatorData.strOBJCInputAry()
    InfoInputNo = iCreatorData.strInfoInputNo()
    InfoInputNo.VersionNo = CURRENT_VERSION_NO
    InfoInputNo2 = iCreatorData.strInfoInputNo2()
    GoodyIni = iCreatorData.strGoodyAry()
    infoOut = iCreatorData.readInfoOut()
    BodyPosIni = iCreatorData.strBodyPosAry()
    ScriptIni = iCreatorData.strScriptConditionAry()
    HandIni = iCreatorData.strHandAry()
    HandIniLast = iCreatorData.strHandAry()
    HandTrans = iCreatorData.strHandAry()
    LogDirIni = str("")
    endSignal = 0
    firstTimeIni = 0
    firstTime = 0
    previousStage = 0
    currentStagePre = 0
    counter = 0
    time_interval = 0.015
    init_time = time()
    goodyNumList = [0, 0, 0, 0, 0, 0, 0, 0]
    modifyByUser = [0, 0, 0, 0, 0, 0, 0, 0]

    FGInfoBuffer = iCreatorData.strFGInfoInputAryBuffer()
    BGInfoBuffer = iCreatorData.strBGInfoInputAryBuffer()
    CUSInfoBuffer = iCreatorData.strCUSInfoInputAryBuffer()
    OBJInfoBuffer = iCreatorData.strOBJInfoInputAryBuffer()
    FGCBuffer = iCreatorData.strFGCInputAryBuffer()
    BGCBuffer = iCreatorData.strBGCInputAryBuffer()
    CUSCBuffer = iCreatorData.strCUSCInputAryBuffer()
    OBJCBuffer = iCreatorData.strOBJCInputAryBuffer()
    GoodyBuffer = iCreatorData.strGoodyAryBuffer()
    BodyPosBuffer = iCreatorData.strBodyPosAryBuffer()
    ScriptBuffer = iCreatorData.strScriptConditionAryBuffer()

    BufferIdx = 0

    BufferSize = 3

    # added new parameter
    hd_ratio = read_hd_ratio()
    screenWidth=1920 / hd_ratio
    screenHeight=1080 / hd_ratio
    # endregion ########### end of Must declare related variable.

    # region ------------------------- initialize user related values

    stageNoforChange = 22           # this will be changed by user in user.py file
#     exec(usercode0)
    elements = Elements()
    if (initial_stage_code != None):
        exec(initial_stage_code)
    if (initial_setup_code != None):
        exec(initial_setup_code)
    # endregion ------------------------- end of initialize user related values

    # region ################# Must setup initial communication.
    initialList = iCreatorData.SetupInitial()

    # endregion ################# end of Must setup initial communication.

    while (endSignal == 0):
        # run every time_interval
        if init_time + time_interval <= time():
            init_time = time()

            # region ########## Must get initial vaules from main program.
            infoOut, PersonExist, FGInfoIni, FGCIni, BGInfoIni, BGCIni, CUSInfoIni, CUSCIni, OBJInfoIni, OBJCIni, GoodyIni, BodyPosIni, LogDirIni, ScriptIni, firstTimeIni, previousStage = iCreatorData.ReadStageInitial(
                stageNoforChange, FGInfoIni, FGCIni, BGInfoIni, BGCIni, CUSInfoIni, CUSCIni, OBJInfoIni, OBJCIni, GoodyIni, BodyPosIni, LogDirIni, ScriptIni, firstTimeIni, previousStage, InfoInputNo)
            #loginfoprint(printFilename,1,str(firstTimeIni)+",d, , ,"+str(FGInfoIni.FGInfo[0].xstart)+","+str(FGInfoIni.FGInfo[0].ystart)+","+str(FGInfoIni.verified[0]))

            endSignal = infoOut.endSignal
            currentStage = infoOut.stageNo
            if currentStage != currentStagePre:
                stageEnterTime = time()
                stageInitime = 0
                currentStagePre = currentStage
                SetElementNumber(elements, currentStage)
                # read goody numbers
                GetGoodyNumList(goodyNumList, modifyByUser)
            # endregion ########## End of Must get initial vaules from main program.

            if (firstTimeIni == 1):

                # region ########### Must clear all the numbers to zero.
                iCreatorData.clearInfoInputNo(InfoInputNo)
                if InfoInputNo.VersionNo >= iCreatorData.PAST_VERSION_NO2:
                    iCreatorData.clearInfoInputNo2(InfoInputNo2)

                # endregion ########### End of Must clear all the numbers to zero.

                # region -----------------this is the start of user input to get the needed initial value
                # from user.py
                SetGoodyNum(goodyNumList, modifyByUser)
                SetElementNumber(elements, currentStage)

                # get the screensize
                screenWidth=BodyPosIni.ScreenWidth
                screenHeight=BodyPosIni.ScreenHeight

                #at the first iteration of stage, clean the old transition verify to zero to avoid trigger from last cycle.
                if InfoInputNo.VersionNo >= CURRENT_VERSION_NO:
                    for i in range(BufferSize):
                        clearScriptTransition(ScriptBuffer.InfoBuffer[i])
                # print("**************** user program start *******************")

                # print("********************** run second part *************************")

                # endregion -----------------end of user input to get the needed initial value

            # firstTimeIni will increase accordingly in the related stage.
            if (firstTimeIni >= 1):

                # region-----------------this is the start of user input to change things during the desired stage
                thisCode = scriptCodes.get('stage_' + str(currentStage))
                if (thisCode != None):
                    exec(thisCode)

                # debug ui pack payload
                if debug.win is not None and debug.FLAG == debug.DEBUG_PLOT_INTERFACE_FLAG:
                    payload = {
                        "FGInfoIni": FGInfoIni,
                        "BGInfoIni": BGInfoIni,
                        "CUSInfoIni": CUSInfoIni,
                        "OBJInfoIni": OBJInfoIni,
                        "GoodyInfoIni": GoodyIni,
                        "timestamp": time()
                    }
                    debug.win.pack_payload(payload)
                # print("********************** run third part *************************")

                # endregion-----------------End of user input to change things during the desired stage
                SetGoodyNum(goodyNumList, modifyByUser)

                # region ############### must output the changes to the main program

                if InfoInputNo.VersionNo >= CURRENT_VERSION_NO:
                    # write InfoIni into a 3-element buffer
                    BuffIdx1 = BufferIdx % BufferSize
                    FGInfoBuffer.currentIdx = BuffIdx1
                    FGInfoBuffer.InfoBuffer[BuffIdx1] = FGInfoIni
                    BGInfoBuffer.currentIdx = BuffIdx1
                    BGInfoBuffer.InfoBuffer[BuffIdx1] = BGInfoIni
                    CUSInfoBuffer.currentIdx = BuffIdx1
                    CUSInfoBuffer.InfoBuffer[BuffIdx1] = CUSInfoIni
                    OBJInfoBuffer.currentIdx = BuffIdx1
                    OBJInfoBuffer.InfoBuffer[BuffIdx1] = OBJInfoIni

                    FGCBuffer.currentIdx = BuffIdx1
                    FGCBuffer.InfoBuffer[BuffIdx1] = FGCIni
                    BGCBuffer.currentIdx = BuffIdx1
                    BGCBuffer.InfoBuffer[BuffIdx1] = BGCIni
                    CUSCBuffer.currentIdx = BuffIdx1
                    CUSCBuffer.InfoBuffer[BuffIdx1] = CUSCIni
                    OBJCBuffer.currentIdx = BuffIdx1
                    OBJCBuffer.InfoBuffer[BuffIdx1] = OBJCIni

                    GoodyBuffer.currentIdx = BuffIdx1
                    GoodyBuffer.InfoBuffer[BuffIdx1] = GoodyIni
                    BodyPosBuffer.currentIdx = BuffIdx1
                    BodyPosBuffer.InfoBuffer[BuffIdx1] = BodyPosIni
                    ScriptBuffer.currentIdx = BuffIdx1
                    ScriptBuffer.InfoBuffer[BuffIdx1] = ScriptIni

                    BufferIdx += 1

                # do a copy operation
                # ctypes.pointer(FGInfoBuffer.FGInfoBuffer[FGBuffIdx1])[0]=FGInfoIni
                # do a simple copy
                # FGInfoBuffer.FGInfoBuffer[FGBuffIdx1].FGInfo[0].xstart= FGInfoIni.FGInfo[0].xstart
                # FGInfoBuffer.FGInfoBuffer[FGBuffIdx1].FGInfo[0].ystart= FGInfoIni.FGInfo[0].ystart
                # FGInfoBuffer.FGInfoBuffer[FGBuffIdx1].verified[0] =FGInfoIni.verified[0]

                if InfoInputNo.VersionNo >= CURRENT_VERSION_NO:  # additional due to version change
                    # iCreatorData.OutputStageChanges2(GoodyIni,BodyPosIni,ScriptIni,InfoInputNo2)
                    iCreatorData.OutputStageChanges2Ary(
                        GoodyBuffer, BodyPosBuffer, ScriptBuffer, InfoInputNo2)
                    #loginfoprint(printFilename,1,str(firstTimeIni)+",b,"+str(BuffIdx1)+", ,"+str(GoodyIni.GoodyInfo[0].initNum))
                elif InfoInputNo.VersionNo>=iCreatorData.PAST_VERSION_NO2:
                     iCreatorData.OutputStageChanges2(GoodyIni,BodyPosIni,ScriptIni,InfoInputNo2)

                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(0)+", ,"+str(GoodyBuffer.InfoBuffer[0].GoodyInfo[0].initNum)+","+str(GoodyBuffer.InfoBuffer[0].verified[0]))
                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(1)+", ,"+str(GoodyBuffer.InfoBuffer[1].GoodyInfo[0].initNum)+","+str(GoodyBuffer.InfoBuffer[1].verified[0]))
                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(2)+", ,"+str(GoodyBuffer.InfoBuffer[2].GoodyInfo[0].initNum)+","+str(GoodyBuffer.InfoBuffer[2].verified[0]))

                # loginfoprint(printFilename,1,str(firstTimeIni)+",b,"+str(BuffIdx1)+", ,"+str(FGInfoIni.FGInfo[0].xstart)+","+str(FGInfoIni.FGInfo[0].ystart)+","+str(FGInfoIni.verified[0]))
                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(0)+", ,"+str(FGInfoBuffer.InfoBuffer[0].FGInfo[0].xstart)+","+str(FGInfoBuffer.InfoBuffer[0].FGInfo[0].ystart)+","+str(FGInfoBuffer.InfoBuffer[0].verified[0]))
                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(1)+", ,"+str(FGInfoBuffer.InfoBuffer[1].FGInfo[0].xstart)+","+str(FGInfoBuffer.InfoBuffer[1].FGInfo[0].ystart)+","+str(FGInfoBuffer.InfoBuffer[1].verified[0]))
                # loginfoprint(printFilename,1,str(firstTimeIni)+",c,"+str(2)+", ,"+str(FGInfoBuffer.InfoBuffer[2].FGInfo[0].xstart)+","+str(FGInfoBuffer.InfoBuffer[2].FGInfo[0].ystart)+","+str(FGInfoBuffer.InfoBuffer[2].verified[0]))
                # iCreatorData.OutputStageChangesAry(FGInfoBuffer,FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,InfoInputNo)
                if InfoInputNo.VersionNo >= CURRENT_VERSION_NO:
                    iCreatorData.OutputStageChangesAry(
                        FGInfoBuffer, FGCBuffer, BGInfoBuffer, BGCBuffer, CUSInfoBuffer, CUSCBuffer, OBJInfoBuffer, OBJCBuffer, InfoInputNo)
                elif InfoInputNo.VersionNo>=iCreatorData.PAST_VERSION_NO2:
                     iCreatorData.OutputStageChanges(FGInfoIni,FGCIni,BGInfoIni,BGCIni,CUSInfoIni,CUSCIni,OBJInfoIni,OBJCIni,InfoInputNo)
                # endregion ############### must output the changes to the main program
        else:
            sleep(0.001)
# region create error log for user to debug
except Exception as e:

    # dirName=logfolder
    filename = logfolder+"\\logError.log"
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.exception(str(e))
# endregion
