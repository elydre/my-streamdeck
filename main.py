import contextlib
import os
import threading
import time

from StreamDeck.DeviceManager import DeviceManager

import mod.kconf as kc
import mod.render as rdr

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


##################
# CORE FUNCTIONS #
##################

def key_change_callback(deck, key, state):
    if key not in kc.key_config:
        print(f"Key {key} not configured")
        return

    if state and callable(kc.key_config[key]["action"]):
        kc.key_config[key]["action"](rdr.gen_args(deck, key, current_info))

    rdr.get_render(kc.key_config[key]["render"]["name"])(deck, key, state, kc.key_config, current_info)

DEFAULT_INDEX = 0
DEFAULT_FONT = "Roboto-Regular.ttf"
DEFAULT_BRIGHTNESS = 30
MAX_LOOP_SEC = 25

current_info = {
    "l_usage": [0], # stack of last usage values
    "brightness": DEFAULT_BRIGHTNESS,
    "resolution": (72, 72),
    "assets_path": ASSETS_PATH,
    "font": DEFAULT_FONT,
    "mid_lps": 0,
}

def thread_loop(deck):
    key_to_update = [[e, 0] for e in kc.key_config if kc.key_config[e]["render"]["name"] in ["graph", "active"]] # TODO: auto detect the actives renders modes
    ideal = 1 / MAX_LOOP_SEC
    init_time = time.time()
    loop_count = 0
    while deck.is_open():
        start_time = time.time()
        for key in key_to_update:
            if time.time() - key[1] > kc.key_config[key[0]]["render"]["refresh_after"]:
                key[1] = time.time()
                rdr.get_render(kc.key_config[key[0]]["render"]["name"])(deck, key[0], False, kc.key_config, current_info)
        if len(current_info["l_usage"]) > MAX_LOOP_SEC * 10:
            current_info["l_usage"].pop(0)
        taked_time = time.time() - start_time
        current_info["l_usage"].append((taked_time / ideal) * 100)
        loop_count += 1
        current_info["mid_lps"] = loop_count / (time.time() - init_time)
        time.sleep(max(0, ideal - taked_time))

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    count = len(streamdecks)
    print(f"Found {count} Stream Deck...")
    if DEFAULT_INDEX >= count: exit(1)

    deck = streamdecks[DEFAULT_INDEX]

    deck.open()
    deck.reset()

    print(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}', fw: '{deck.get_firmware_version()}')")
    current_info["resolution"] = deck.key_image_format()["size"]

    # Set initial screen brightness to 30%.
    deck.set_brightness(current_info["brightness"])

    # Set initial key images.
    for id in kc.key_config:
        rdr.get_render(kc.key_config[id]["render"]["name"])(deck, id, False, kc.key_config, current_info)

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
