import contextlib
import os
import threading
import time

from StreamDeck.DeviceManager import DeviceManager

import tools.render as rdr
import conf.kconf as kc

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


##################
# CORE FUNCTIONS #
##################

def key_change_callback(deck, key, state):
    if key not in kc.key_config:
        return

    if state and callable(kc.key_config[key]["action"]):
        kc.key_config[key]["action"](rdr.gen_args(deck, key, current_info))

    rdr.get_render(kc.key_config[key]["render"]["name"])(deck, key, state, kc.key_config, current_info)

DEFAULT_INDEX = 0
DEFAULT_FONT = "8.ttf"
DEFAULT_BRIGHTNESS = 40
MAX_LOOP_SEC = 30

current_info = {
    "l_usage": [0], # stack of last usage values
    "brightness": DEFAULT_BRIGHTNESS,
    "resolution": (72, 72),
    "assets_path": ASSETS_PATH,
    "font": DEFAULT_FONT,
    "mid_lps": 0,
    "max_lps": MAX_LOOP_SEC,
}

def thread_loop(deck):
    key_to_update = [[e, 0] for e in kc.key_config if kc.key_config[e]["render"]["name"] in ["graph", "active"]] # TODO: auto detect the actives renders modes

    for i in range(len(key_to_update)):
        key_to_update[i][1] = time.time() - i * 0.1

    ideal = 1 / MAX_LOOP_SEC
    last_ltimes = []
    crs = 0

    while deck.is_open():
        start_time = time.time()

        for key in key_to_update:
            if kc.key_config[key[0]]["render"]["refresh_after"] > time.time() - key[1]:
                continue
            if time.time() - start_time > ideal:
                break
            key[1] = time.time()
            rdr.get_render(kc.key_config[key[0]]["render"]["name"])(deck, key[0], False, kc.key_config, current_info)

        if len(current_info["l_usage"]) > MAX_LOOP_SEC * 10:
            current_info["l_usage"].pop(0)

        taked_time = time.time() - start_time
        mid_ltimes = sum(last_ltimes) / len(last_ltimes) if len(last_ltimes) > 0 else taked_time
        current_info["l_usage"].append((taked_time / ideal) * 100)
        current_info["mid_lps"] = 1 / mid_ltimes
        patched_time = (ideal - mid_ltimes) * 5 # time to wait to have the ideal loop time

        time.sleep(max(ideal - taked_time + patched_time, 0))

        if len(last_ltimes) > 100:
            last_ltimes.pop(0)

        last_ltimes.append(time.time() - start_time)


def main(deck):
    deck.open()
    deck.reset()

    current_info["resolution"] = deck.key_image_format()["size"]

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

if __name__ == "__main__":
    try:
        streamdecks = DeviceManager().enumerate()

        count = len(streamdecks)
        if DEFAULT_INDEX >= count: exit(1)

        deck = streamdecks[DEFAULT_INDEX]
        main(deck)

    except Exception as e:
        print("Error: ", e)
        if not deck.is_open():
            exit(1)
        print("Closing deck...")
        deck.reset()
        deck.close()
