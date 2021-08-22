# yui cli todo list
# TODO: Need unit tests for all the operations
# TODO: break task operations from prompt toolkit operations
import click

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea

from tasks import (add_task,
                   sprint_task,
                   unsprint_task,
                   complete_task,
                   delete_task)

from file import read_yui, write_yui


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


@click.group()
def cli():
    pass


@click.command()
def init():
    write_yui()


@click.command()
def start():
    app = Application(key_bindings=kb,
                      full_screen=True,
                      layout=layout)

    print(app)
    app.run()


cli.add_command(start)
cli.add_command(init)


cli()
