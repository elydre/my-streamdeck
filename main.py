import contextlib
import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import time

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
        if isinstance(key_style["label"], str):
            pass
        elif callable(key_style["label"]):
            key_style["label"] = key_style["label"](gen_args(deck, key))
        else:
            print(f"Label {key_style['label']} is not a string or callable")
            return
    else:
        print(f"Key {key} not configured")
        return
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])


    with deck:
        deck.set_key_image(key, image)

###########################
# ACTIVE RENDER FUNCTIONS #
###########################

def active_render_key_image(deck, font_filename, label_text):
    image = Image.new("RGB", resolution, "black")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)

def active_update_key_image(deck, key, state):
    if key in kc.key_config:
        render_info = kc.key_config[key]["render"]
        key_style = {
            "font": os.path.join(ASSETS_PATH, DEFAULT_FONT),
            "label": render_info["label"]["pressed" if state else "default"]
        }
        if isinstance(key_style["label"], str):
            pass
        elif callable(key_style["label"]):
            key_style["label"] = key_style["label"](gen_args(deck, key))
        else:
            print(f"Label {key_style['label']} is not a string or callable")
            return
    else:
        print(f"Key {key} not configured")
        return
    image = active_render_key_image(deck, key_style["font"], key_style["label"])

    with deck:
        deck.set_key_image(key, image)


##################
# CORE FUNCTIONS #
##################

def key_change_callback(deck, key, state):
    if key not in kc.key_config:
        print(f"Key {key} not configured")
        return

    if state: kc.key_config[key]["action"](gen_args(deck, key))
    get_render(kc.key_config[key]["render"]["name"])(deck, key, state)

def get_render(render):
    render_table = {
        "classic": update_key_image,
        "active": active_update_key_image
    }
    if render in render_table:
        return render_table[render]
    print(f"Render {render} not found, using default")
    return render_table["classic"]

def gen_args(deck, key):
    return {
        "deck": deck,
        "key": key,
        "info": current_info
    }

DEFAULT_INDEX = 0
DEFAULT_FONT = "Roboto-Regular.ttf"
DEFAULT_BRIGHTNESS = 30
MAX_FPM = 70 # Max frames per minute

resolution = (0, 0)
current_info = {
    "usage": 0,
    "brightness": DEFAULT_BRIGHTNESS
}

def thread_loop(deck):
    key_to_update = [e for e in kc.key_config if kc.key_config[e]["render"]["name"] == "active"]
    ideal = 1 / (MAX_FPM / 60)
    while deck.is_open():
        start_time = time.time()
        for key in key_to_update:
            active_update_key_image(deck, key, False)
        time_to_sleep = max(0, ideal - (time.time() - start_time))
        current_info["usage"] = (1 - time_to_sleep / ideal) * 100
        time.sleep(time_to_sleep)

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    count = len(streamdecks)
    print(f"Found {count} Stream Deck...")
    if DEFAULT_INDEX >= count: exit(1)

    deck = streamdecks[DEFAULT_INDEX]

    deck.open()
    deck.reset()

    print(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}', fw: '{deck.get_firmware_version()}')")
    resolution = deck.key_image_format()["size"]

    # Set initial screen brightness to 30%.
    deck.set_brightness(current_info["brightness"])

    # Set initial key images.
    for id in kc.key_config:
        get_render(kc.key_config[id]["render"]["name"])(deck, id, False)

    # Register callback function for when a key state changes.
    deck.set_key_callback(key_change_callback)

    # Start thread for active render
    active_t = threading.Thread(target=thread_loop, args=(deck,))
    active_t.start()

    # Wait until all application threads have terminated (for this example,
    # this is when all deck handles are closed).
    for t in threading.enumerate():
        with contextlib.suppress(RuntimeError):
            t.join()
