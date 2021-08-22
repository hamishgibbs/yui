# YUI

A simple to-do list CLI. A very simple to-do list CLI.

#### Installation

This library uses poetry for dependency management.

Clone this repository, `cd` into the project directory, and install the package with:

``` {shell}
poetry install
```

#### Quickstart

`YUI` persists to-do list tasks so you can keep track of what you do and how long it took you.

Start using `YUI` by creating a `yui.json` file with:

``` {shell}
poetry run yui init
```

Then, open the `YUI` CLI:

``` {shell}
poetry run yui start
```

Add your first tasks by typing in the command line and press `enter`.

#### Interface

`YUI` implements a flat to-do list with limited navigation commands.

The goal of the library is speed and ease of navigation.

The core concept implemented by `YUI` is the `task` which has a creation time: `ctime` and `task` string describing the task.

Tasks are divided in two categories: "All tasks" and "Sprint tasks". A "sprint" is a collection of tasks that will be completed in a single "effort" (for example, in a day). The concept of a "sprint" is stolen from agile software development, where a "sprint" typically lasts 30 days.

#### Task operations

Tasks can be "sprinted", "unsprinted", "completed", "deleted".

`ctrl + S` - "sprinting" a task labels it as a part of the current sprint.
`ctrl + S` - "unsprinting" a task removes it from the current sprint.
`ctrl + X` - "completing" a task removes it from the task list and marks it as completed.
`ctrl + O` - "deleting" a task deletes it from the task list.
`up` and `down` arrows - Navigate the task list.

`ctrl + A` - toggles "All tasks" and "Sprint tasks".

#### Recommended use

This library is a rapid, persistent to-do list.

`YUI` will NOT work well with:

* Long to-do descriptions
* Very many to-do items (25+)

`YUI` is good for:

* Quickly updating your todo list
* Tracking short-term project goals

#### Contributions

This is a small library for personal use. Contributions are welcome. If you see a problem with the library, please [open an issue](https://github.com/hamishgibbs/yui/issues/new).
