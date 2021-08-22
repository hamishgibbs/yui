def get_active_indices(tasks, state):
    if state["sprinted_only"]:
        indices = [i for i, x in enumerate(tasks) if "stime" in x.keys()]
    else:
        indices = [i for i, x in enumerate(tasks)]
    return indices


def format_text(tasks, state):

    tasks_formatted = []

    tasks = [tasks[i] for i in get_active_indices(tasks, state)]

    for i, x in enumerate(tasks):
        if "stime" in x.keys():
            tasks_formatted.append(str(i) + " S : " + x["task"])
        else:
            tasks_formatted.append(str(i) + "   : " + x["task"])

    active_index = state["active_index"]

    try:
        tasks_formatted[active_index] = tasks_formatted[active_index] + " *"
    except Exception:
        state.update({"active_index": 0})
        tasks_formatted[0] = tasks_formatted[0] + " *"

    tasks_formatted = "\n".join(tasks_formatted)

    if state["sprinted_only"]:
        return "---Sprint Tasks---\n" + tasks_formatted
    else:
        return "---All Tasks---\n" + tasks_formatted
