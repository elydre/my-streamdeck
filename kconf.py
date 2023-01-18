def exit_function(deck):
    print("Exiting...")
    deck.reset()
    deck.close()

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
        "action": lambda deck: exit_function(deck)
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
        "action": lambda deck: print("test")
    },
}
