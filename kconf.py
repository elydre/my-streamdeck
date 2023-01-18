def exit_function(deck):
    print("Exiting...")
    deck.reset()
    deck.close()

key_config = {
    0: {
        "icon": {
            "default": "img.jpg",
            "pressed": "img.jpg"
        },
        "label": {
            "default": "exit",
            "pressed": "exiting",
        },
        "render": "classic",
        "action": lambda deck: exit_function(deck)
    },
    1: {
        "icon": {
            "default": "img.jpg",
            "pressed": "img.jpg"
        },
        "label": {
            "default": "test",
            "pressed": "PRESS",
        },
        "render": "classic",
        "action": lambda deck: print("test")
    },
}
