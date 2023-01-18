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
            "refresh_after": 0.2,
            "label":  lambda args: f"usg: {sum(args['info']['l_usage']) / len(args['info']['l_usage']):.2f}%",
        },
        "action": None
    },
    6: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"cpu: {psutil.cpu_percent():.2f}%\nmem: {psutil.virtual_memory().percent}%",
        },
        "action": None
    },
}
