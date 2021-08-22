import json
import os


def filter_active(tasks):

    return [x for x in tasks
            if "xtime" not in x.keys()
            and "otime" not in x.keys()]


def filter_inactive(tasks):

    return [x for x in tasks
            if "xtime" in x.keys()
            or "otime" in x.keys()]


def read_yui():

    with open("yui.json", "r") as f:
        yui = json.load(f)

    # Extract only active tasks
    yui["tasks"] = filter_active(yui["tasks"])

    return yui


def write_yui(yui={"tasks": []}):

    if os.path.isfile("yui.json"):

        # Read old tasks
        with open("yui.json", "r") as f:
            yui_old = json.load(f)

        # Append old inactive tasks
        yui["tasks"] = yui["tasks"] + filter_inactive(yui_old["tasks"])

    # write out total tasks
    with open("yui.json", "w") as f:
        json.dump(yui, f)
