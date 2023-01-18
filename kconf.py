import time

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
            "output": {
                "default": lambda args: time.strftime("%H:%M:%S"),
                "pressed": lambda args: time.strftime("%H:%M:%S")
            }
        },
        "action": lambda args: print("test")
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
                "pressed": "br +"
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
                "pressed": "br -"
            }
        },
        "action": lambda args: less_brightness(args)
    }
}
