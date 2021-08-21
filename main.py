# yui cli todo list
import json
from datetime import datetime
import os
import click


def filter_active(tasks):

    return [x for x in tasks
            if "xtime" not in x.keys()
            and "otime" not in x.keys()]


def filter_inactive(tasks):

    return [x for x in tasks
            if "xtime" in x.keys()
            and "otime" in x.keys()]


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


def add_task(yui, task):

    yui["tasks"].append({
        "task": task,
        "ctime": datetime.timestamp(datetime.now())
    })


def sprint_task(task):

    task.update({"stime": datetime.timestamp(datetime.now())})


def unsprint_task(task):

    task.update({"stime_" + str(task["stime"]): task["stime"]})
    task.update({
        "ustime_" + str(task["stime"]): datetime.timestamp(datetime.now())
        })
    task.pop("stime")


def complete_task(task):

    task.update({"xtime": datetime.timestamp(datetime.now())})


def delete_task(task):

    task.update({"otime": datetime.timestamp(datetime.now())})


def rearrange_tasks(tasks, new_position, orig_position):

    tasks.insert(new_position, tasks[orig_position])
    tasks.pop(orig_position + 1)


@click.group()
def cli():
    pass


@click.command()
def init():
    write_yui()


from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()


@kb.add('s')
def exit_(event):
    event.app.exit()


@click.command()
def start():
    app = Application(key_bindings=kb, full_screen=True)

    print(app)
    app.run()


cli.add_command(start)
cli.add_command(init)




# decorator to complete task operations
# open file
# get correct task
# write file

# cycle is open, do single thing, close, repeat
# optimize later

def main():

    yui = read_yui()
    #add_task(yui, "test")
    #add_task(yui, "test1")
    #add_task(yui, "test2")
    #add_task(yui, "test3")
    #add_task(yui, "test4")
    #sprint_task(yui["tasks"][0])
    #sprint_task(yui["tasks"][1])
    #sprint_task(yui["tasks"][2])
    #sprint_task(yui["tasks"][3])
    #sprint_task(yui["tasks"][4])
    #unsprint_task(yui["tasks"][0])
    #delete_task(yui["tasks"][0])

    # Changing order of tasks
    #rearrange_tasks(yui["tasks"], 0, 4)

    #print(yui["tasks"])

    # print only sprinted tasks
    #print([x for x in filter_active(yui["tasks"]) if "stime" in x.keys()])

    # print all tasks
    #print(filter_active(yui["tasks"]))

    write_yui(yui)


cli()
#main()
