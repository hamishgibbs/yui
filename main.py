# yui cli todo list
# TODO: Need unit tests for all the operations
# TODO: break task operations from prompt toolkit operations
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


# click may not be needed now?
@click.group()
def cli():
    pass


@click.command()
def init():
    write_yui()


from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit import prompt
from prompt_toolkit.application.current import get_app

state = {
    "content.text": None,
    "tasks": [],
    "active_index": 0,
    "sprinted_only": False,
}


def get_active_indices(tasks):
    if state["sprinted_only"]:
        indices = [i for i, x in enumerate(tasks) if "stime" in x.keys()]
    else:
        indices = [i for i, x in enumerate(tasks)]
    return indices


def format_text(tasks):

    tasks_formatted = []

    tasks = [tasks[i] for i in get_active_indices(tasks)]

    for i, x in enumerate(tasks):
        if "stime" in x.keys():
            tasks_formatted.append(str(i) + " S : " + x["task"])
        else:
            tasks_formatted.append(str(i) + "   : " + x["task"])

    try:
        tasks_formatted[state["active_index"]] = tasks_formatted[state["active_index"]] + " *"
    except Exception:
        state["active_index"] = 0
        tasks_formatted[state["active_index"]] = tasks_formatted[state["active_index"]] + " *"

    tasks_formatted = "\n".join(tasks_formatted)

    if state["sprinted_only"]:
        return "---Sprint Tasks---\n" + tasks_formatted
    else:
        return "---All Tasks---\n" + tasks_formatted


def accepted(buff):
    task = buff.text
    yui = read_yui()
    add_task(yui, task)
    write_yui(yui)

    tasks_formatted = [x["task"] for x in yui["tasks"]]
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


input_field = TextArea(
    height=1, prompt='>>> ', multiline=False, wrap_lines=False,
    accept_handler=accepted,
    dont_extend_height=True)

root_container = HSplit([
    Window(content=FormattedTextControl(text='')),
    input_field,
])

layout = Layout(root_container)

kb = KeyBindings()


@kb.add('c-c')
def exit_(event):
    event.app.exit()


def move_cursor(position):
    yui = read_yui()

    if state["sprinted_only"]:
        displayed_tasks = [x for x in yui["tasks"] if "stime" in x.keys()]
    else:
        displayed_tasks = [x for x in yui["tasks"]]

    state["active_index"] = (state["active_index"] + position) % len(displayed_tasks)
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


@kb.add('up')
def cursor_up(event):
    move_cursor(-1)


@kb.add('down')
def cursor_down(event):
    move_cursor(1)


@kb.add('c-x')
def complete_task_(event):
    yui = read_yui()
    active_indices = get_active_indices(yui["tasks"])
    complete_task(yui["tasks"][active_indices[state["active_index"]]])
    write_yui(yui)
    yui = read_yui()
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


@kb.add('c-o')
def delete_task_(event):
    yui = read_yui()
    active_indices = get_active_indices(yui["tasks"])
    delete_task(yui["tasks"][active_indices[state["active_index"]]])
    write_yui(yui)
    yui = read_yui()
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


@kb.add('c-s')
def sprint_task_(event):
    yui = read_yui()
    active_indices = get_active_indices(yui["tasks"])
    active_task = yui["tasks"][active_indices[state["active_index"]]]

    if "stime" in active_task.keys():
        unsprint_task(yui["tasks"][active_indices[state["active_index"]]])
    else:
        sprint_task(yui["tasks"][active_indices[state["active_index"]]])

    write_yui(yui)
    yui = read_yui()
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


@kb.add('c-a')
def toggle_sprinted(event):
    state["sprinted_only"] = not state["sprinted_only"]
    yui = read_yui()
    tasks_formatted = format_text(yui["tasks"])
    root_container.children[0].content.text = tasks_formatted


@click.command()
def start():
    app = Application(key_bindings=kb,
                      full_screen=True,
                      layout=layout)

    print(app)
    app.run()
    yui = read_yui()

    tasks_formatted = [x["task"] for x in yui["tasks"]]

    root_container.children[0].content.text = "\n".join(tasks_formatted)


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
