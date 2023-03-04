import time

import psutil

DEBUG = False

psutil_history = {
    "cpu": [],
    "mem": [],
}

def exit_function(args):
    deck = args["deck"]
    print("Exiting...")
    deck.reset()
    deck.close()

def more_brightness(args):
    deck = args["deck"]
    info = args["info"]
    info["brightness"] = min(100, info["brightness"] + 10)
    deck.set_brightness(info["brightness"])

def less_brightness(args):
    deck = args["deck"]
    info = args["info"]
    info["brightness"] = max(0, info["brightness"] - 10)
    deck.set_brightness(info["brightness"])

def to_graph(args, in_list, in_max=None, in_min=0):
    max_len = args["info"]["resolution"][0]
    max_val = args["info"]["resolution"][1]

    out_list = in_list.copy()

    # remove values
    while len(out_list) > max_len:
        out_list.pop(0)

    # scale values
    if in_max is None: in_max = max(out_list) + max(out_list) / 10 + 1
    out_list = [int((i - in_min) * (max_val - 0) / (in_max - in_min)) for i in out_list]

    # add values
    while len(out_list) < max_len:
        out_list.insert(0, 0)

    return out_list

def graph_psutil(args, thing):
    max_len = args["info"]["resolution"][0]

    if len(psutil_history[thing]) > max_len:
        psutil_history[thing].pop(0)
    
    if thing == "cpu":
        psutil_history[thing].append(psutil.cpu_percent())
    elif thing == "mem":
        psutil_history[thing].append(psutil.virtual_memory().percent)

    return to_graph(args, psutil_history[thing], 100)

def get_linux_version():
    # return linux kernel version
    with open("/proc/version", "r") as f:
        return f.read().split(" ")[2].split("-")[0]

key_config = {
    0: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "linux.png",
                "pressed": "linux.png"
            },
            "label": {
                "default": lambda args: get_linux_version(),
                "pressed": "refresh"
            }
        },
        "action": None
    },
    2: {
        "render": {
            "name": "active",
            "refresh_after": 0.9,
            "label": lambda args: f"{time.strftime('%H:%M:%S')}\n{time.strftime('%H:%M:%S', time.gmtime())}",
            "size": 18,
        },
        "action": None
    },
    4: {
        "render": {
            "name": "big",
            "label": {
                "default": "+",
                "pressed": lambda args: f"{args['info']['brightness']}"
            }
        },
        "action": lambda args: more_brightness(args)
    },
    5: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"{sum(args['info']['l_usage']) / len(args['info']['l_usage']):.3f}%\n{max(args['info']['l_usage']):.2f}%\n{args['info']['crsp']:.3f}%\n{args['info']['mid_lps']:.4f}",
            "size": 15,
        },
        "action": lambda args: exit_function(args) if DEBUG else None
    },
    6: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"RAM\n{psutil.virtual_memory().percent}%\n{psutil.virtual_memory().used / 1024 ** 3:.2f}Go",
            "size": 15,
        },
        "action": None
    },
    7: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"CPU\n{psutil.cpu_percent()}%\n{psutil.cpu_freq().current / 1000:.1f}GHz",
            "size": 15,
        },
        "action": None
    },
    9: {
        "render": {
            "name": "big",
            "label": {
                "default": "-",
                "pressed": lambda args: f"{args['info']['brightness']}"
            }
        },
        "action": lambda args: less_brightness(args)
    },
    10: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: to_graph(args, args["info"]["l_usage"]),
            "color": 0x66FF66,
        },
        "action": None
    },
    11: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: graph_psutil(args, "mem"),
            "color": 0x66FFFF,
        },
        "action": None
    },
    12: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: graph_psutil(args, "cpu"),
            "color": 0xFFFF00,
        },
        "action": None
    },
}
