"""
playStage.py
This file is the main file for the play stage.
It is responsible for running the stage and calling the user's code.
version 1.0 on 10/12/2023
a. initial version
version 1.1 on 10/20/2023
a. add support for gesture duration
version 1.2 on 10/27/2023
a. fix some bugs
version 1.3 on 01/26/2024
a. support icamera web
version 1.4 on 04/22/2024
a. Optimize loop execution
"""

import os
import re
import threading
import time
import sys
import json
import traceback

IS_EXEC_CODE = False
TIME_INTERVAL = 0.015
# TIME_INTERVAL = 0.02
DISTANCE_UNIT = 5
INIT_GESTURE = 9
REGULAR_GESTURE = 10
MAX_INFO_ENTITIES = 8

screenWidth = 1920
screenHeight = 1080
offsetX = 0
offsetY = 0
currentGesture = INIT_GESTURE
gestureDuration = 0
isProduction = bool(0)

args = sys.argv
shared_data = None
goodies = []
project_path = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.basename(project_path)
log_folder = os.path.join(
    os.path.expanduser("~"), "Documents", "integem", "pythonLogs", project_name
)
scripts_folder = os.path.join(project_path, "script")

if os.name == "nt":
    log_folder = os.path.join("C:\\", "integem", "pythonLogs", project_name)

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

printFilename = os.path.join(log_folder, "print.log")


def send_to_stdout(type, msg):
    print(f"[{type}]:{msg};")


def replace_file_dependence(f, remove=True):
    lines = f.read().split("##**##")
    dep = lines[0]
    code = lines[1]

    if remove:
        dep_lines_count = len(dep.split("\n")) - 1
        comments = "# Placeholder comment\n" * dep_lines_count
        return comments + code
    else:
        dep = dep.replace("from userUtils import *", "from localUtils import *")
        dep = dep.replace("from main import *", "from playStage import *")
        dep = dep.replace(
            "from initial_setup import *", "from script.initial_setup import *"
        )
        return dep + code

def dict_update(raw, new):
    if raw is None:
        raw = new
    else:
        modify_dict(raw, new)
    return raw
 

def merge_arrays(arr1, arr2):
    if arr2:
        for i in range(len(arr2)):
            if i < len(arr1):
                if isinstance(arr1[i], dict) and isinstance(arr2[i], dict):
                    modify_dict(arr1[i], arr2[i])
                else:
                    arr1[i] = arr2[i]
            else:
                arr1.append(arr2[i])
    return arr1

def modify_dict(source, setting):
    for key, val in setting.items():
        if isinstance(val, dict) and isinstance(source[key], dict):
            modify_dict(source[key], val)
        elif isinstance(val, list) and isinstance(source[key], list):
            source[key] = merge_arrays(source[key], val)
        else:
            source[key] = val
    return source

def process_input():
    global goodies
    global shared_data
    global offsetX
    global offsetY
    global currentGesture
    global gestureDuration
    global IS_EXEC_CODE
    for line in sys.stdin:
        try:
            if line.find("direction") != -1:
                offsetX = int(line.split(",")[0].split("=")[1])
                offsetY = int(line.split(",")[1].split("=")[1].split(";")[0])
                currentGesture = REGULAR_GESTURE
            elif line.find("gesture") != -1:
                value = int(line.split(",")[0].split("=")[1])
                frames = int(line.split(",")[1].split("=")[1].split(";")[0])
                currentGesture = value
                gestureDuration = frames
            elif (
                line.find("<fg") != -1
                or line.find("<cus") != -1
                or line.find("<bg") != -1
                or line.find("<obj") != -1
                or line.find("<objt") != -1
            ):
                # <fg-1>:x=10,y=10;
                type = line.split(":")[0]
                layer = type.split("-")[0].replace("<", "")
                index = int(type.split("-")[1].replace(">", ""))
                props = line.split(":")[1]
                x = float(props.split(",")[0].split("=")[1])
                y = float(props.split(",")[1].split("=")[1].split(";")[0])
                is_render = line.find("!!noRender") == -1
                obj_id = GetObjIDFromObjKey(layer)
                if is_render:
                    set_it = SetStartLocation(currentStage, obj_id, index, x, y)
                else:
                    SetStartLocationNoRender(currentStage, obj_id, index, x, y)
            else:
                payload = json.loads(line)
                if isProduction:
                    IS_EXEC_CODE = True
                    shared_data = dict_update(shared_data, payload["stage"])
                else:
                    shared_data = payload["stage"]
                if "instruction" in shared_data:
                    goodies = list(
                        filter(
                            lambda x: x["type"] == "goody", shared_data["instruction"]
                        )
                    )
        except Exception as e:
            send_to_stdout("error", e)


if __name__ == "__main__":
    try:
        stage_id = args[1]
        isProduction = bool(args[2:3][0] if len(args[2:3]) > 0 else 0)
        init_time = time.time()
        currentStage = stage_id.split("_")[1]

        utils_file = os.path.join(project_path, "localUtils.py")
        with open(utils_file, "r", encoding='utf-8') as f:
            utils_code = replace_file_dependence(f)
            exec(utils_code)
            del utils_code

        process_input_thread = threading.Thread(target=process_input)
        process_input_thread.daemon = True
        process_input_thread.start()

        elements = Elements()
        initial_setup_file = os.path.join(scripts_folder, "initial_setup.py")
        with open(initial_setup_file, "r", encoding='utf-8') as f:
            initial_setup_code = replace_file_dependence(f)
            exec(initial_setup_code)
            del initial_setup_code

        stage_file = os.path.join(scripts_folder, f"{stage_id}.py")
        with open(stage_file, "r", encoding='utf-8') as f:
            stage_code = replace_file_dependence(f)

        stageEnterTime = time.time()
        stageInitTime = 0

        while True:
            if not isProduction and (init_time + TIME_INTERVAL <= time.time()):
                stageInitTime += 1
                init_time = time.time()
                exec(stage_code)
                if gestureDuration > 0:
                    gestureDuration -= 1
            elif isProduction and IS_EXEC_CODE:
                IS_EXEC_CODE = False
                stageInitTime += 1
                exec(stage_code)
            else:
                time.sleep(0.001)

    except Exception as e:
        error_message = traceback.format_exc()
        # send_to_stdout("error", e)
        print(error_message, file=sys.stderr)
    finally:
        send_to_stdout("info", "play stage finished")
