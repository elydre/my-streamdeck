import time
import psutil

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

def to_graph(args, in_list):
    max_len = args["info"]["resolution"][0]
    max_val = args["info"]["resolution"][1]

    # scale values
    in_max, in_min = max(in_list) + max(in_list) / 10 + 1, 0
    out_list = [int((i - in_min) * (max_val - 0) / (in_max - in_min)) for i in in_list]

    # remove values
    while len(out_list) > max_len:
        out_list.pop(0)

    # add values
    while len(out_list) < max_len:
        out_list.append(0)

    return out_list

key_config = {
    0: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "img.jpg",
                "pressed": "img.jpg"
            },
            "label": {
                "default": "exit",
                "pressed": "exiting"
            }
        },
        "action": lambda args: exit_function(args)
    },
    1: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "img.jpg",
                "pressed": "img.jpg"
            },
            "label": {
                "default": "test",
                "pressed": "PRESS"
            }
        },
        "action": lambda args: print("test")
    },
    2: {
        "render": {
            "name": "active",
            "refresh_after": 0.9,
            "label": lambda args: time.strftime("%H:%M:%S"),
        },
        "action": None
    },
    3: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "img.jpg",
                "pressed": "img.jpg"
            },
            "label": {
                "default": "br +",
                "pressed": lambda args: f"br: {args['info']['brightness']}"
            }
        },
        "action": lambda args: more_brightness(args)
    },
    4: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "img.jpg",
                "pressed": "img.jpg"
            },
            "label": {
                "default": "br -",
                "pressed": lambda args: f"br: {args['info']['brightness']}"
            }
        },
        "action": lambda args: less_brightness(args)
    },
    5: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"cpu: {psutil.cpu_percent():.2f}%\nmem: {psutil.virtual_memory().percent}%",
        },
        "action": None
    },
    6: {
        "render": {
            "name": "graph",
            "refresh_after": 0.05,
            "table": lambda args: to_graph(args, args["info"]["l_usage"]),
        },
        "action": None
    },
    7: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"usg: {sum(args['info']['l_usage']) / len(args['info']['l_usage']):.1f}%\nmax: {max(args['info']['l_usage']):.1f}%\nlps: {args['info']['mid_lps']:.1f}",
        },
        "action": None
    },
}
