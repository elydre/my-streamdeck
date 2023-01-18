import contextlib
import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

import kconf as kc

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

############################
# CLASSIC RENDER FUNCTIONS #
############################

def render_key_image(deck, icon_filename, font_filename, label_text):
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, state):
    if key in kc.key_config:
        render_info = kc.key_config[key]["render"]
        key_style = {
            "icon": os.path.join(ASSETS_PATH, render_info["icon"]["pressed" if state else "default"]),
            "font": os.path.join(ASSETS_PATH, DEFAULT_FONT),
            "label": render_info["label"]["pressed" if state else "default"]
        }
    else:
        print(f"Key {key} not configured")
        return
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])


    with deck:
        deck.set_key_image(key, image)

##################
# CORE FUNCTIONS #
##################

def key_change_callback(deck, key, state):
    print(f"Deck {deck.id()} Key {key} = {state}", flush=True)

    if key not in kc.key_config:
        print(f"Key {key} not configured")
        return

    get_render(kc.key_config[key]["render"]["name"])(deck, key, state)
    if state: kc.key_config[key]["action"](deck)

def get_render(render):
    render_table = {
        "classic": update_key_image
    }
    if render in render_table:
        return render_table[render]
    print(f"Render {render} not found, using default")
    return render_table["classic"]


DEFAULT_INDEX = 0
DEFAULT_FONT = "Roboto-Regular.ttf"

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    count = len(streamdecks)
    print(f"Found {count} Stream Deck...")
    if DEFAULT_INDEX >= count: exit(1)

    deck = streamdecks[DEFAULT_INDEX]

    deck.open()
    deck.reset()

    print(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}', fw: '{deck.get_firmware_version()}')")

    # Set initial screen brightness to 30%.
    deck.set_brightness(30)

    # Set initial key images.
    for id in kc.key_config:
        get_render(kc.key_config[id]["render"]["name"])(deck, id, False)

    # Register callback function for when a key state changes.
    deck.set_key_callback(key_change_callback)

    # Wait until all application threads have terminated (for this example,
    # this is when all deck handles are closed).
    for t in threading.enumerate():
        with contextlib.suppress(RuntimeError):
            t.join()
