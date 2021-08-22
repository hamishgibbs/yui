from datetime import datetime


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


# TODO: implement
def rearrange_tasks(tasks, new_position, orig_position):

    tasks.insert(new_position, tasks[orig_position])
    tasks.pop(orig_position + 1)
