# YUI

A very simple to-do list.

![](/yui_demo.png)

## Installation

Clone this repository, `cd` into the project directory, and install the package with:

``` {shell}
pip install .
```

## Quickstart

`YUI` persists to-do list tasks so you can keep track of what you do and how long it took you.

Start using `YUI` by creating a `yui.json` file with:

``` {shell}
yui init
```

Then, open the `YUI` CLI:

``` {shell}
yui start
```

Add your first task by typing in the command line and pressing `enter`.

## Usage

`YUI` implements an intentionally limited to-do list interface made up of "tasks". The goal of the library is speed and ease of navigation while keeping tasks small.

Tasks are divided in two categories: "All tasks" and "Sprint tasks". A "sprint" is a collection of tasks that will be completed in a single "effort" (for example, in a day). The concept of a "sprint" has been stolen from agile software development, where a "sprint" typically lasts longer.

Tasks can be "sprinted", "unsprinted", "completed", or "deleted".

### Navigation

`up` and `down` arrows - Navigate the task list.  
`ctrl + S` - "sprinting" a task labels it as a part of the current sprint.  
`ctrl + S` - "unsprinting" a task removes it from the current sprint.  
`ctrl + X` - "completing" a task removes it from the task list and marks it as completed.  
`ctrl + O` - "deleting" a task deletes it from the task list.  

### Other commands

`ctrl + A` - toggles "All tasks" and "Sprint tasks".  
`ctrl + 1` - advances a task to the top of the task list.  

*Tasks that have been completed or deleted cannot be restored.*

## Recommended use

This library is a rapid, persistent to-do list.

`YUI` will NOT work well with:

* Long to-do descriptions
* Very many to-do items (25+)

`YUI` is good for:

* Quickly updating your todo list
* Tracking short-term project goals
* Recording when you added, prioritised, and completed tasks.

## Contributions

This is a small library with limited scope. Contributions are welcome. If you see a problem with the library, please [open an issue](https://github.com/hamishgibbs/yui/issues/new).
