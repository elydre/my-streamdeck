from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
import os

# classic render

def get_render(render):
    render_table = {
        "classic": update_key_image,
        "active": active_update_key_image
    }
    if render in render_table:
        return render_table[render]
    print(f"Render {render} not found, using default")
    return render_table["classic"]

def gen_args(deck, key, info):
    return {
        "deck": deck,
        "key": key,
        "info": info
    }

def render_key_image(deck, icon_filename, font_filename, label_text):
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)

def update_key_image(deck, key, state, key_config, info):
    if key in key_config:
        render_info = key_config[key]["render"]
        key_style = {
            "icon": os.path.join(info["assets_path"], render_info["icon"]["pressed" if state else "default"]),
            "font": os.path.join(info["assets_path"], info["font"]),
            "label": render_info["label"]["pressed" if state else "default"]
        }
        if callable(key_style["label"]):
            key_style["label"] = key_style["label"](gen_args(deck, key, info))
        elif not isinstance(key_style["label"], str):
            print(f"Label {key_style['label']} is not a string or callable")
            return
    else:
        print(f"Key {key} not configured")
        return
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    with deck:
        deck.set_key_image(key, image)

# active render

def active_render_key_image(deck, font_filename, label_text, info):
    image = Image.new("RGB", info["resolution"], "black")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height / 2), text=label_text, font=font, anchor="mm", fill="white")


    return PILHelper.to_native_format(deck, image)

def active_update_key_image(deck, key, state, key_config, info):
    if key in key_config:
        render_info = key_config[key]["render"]
        key_style = {
            "font": os.path.join(info["assets_path"], info["font"]),
            "label": render_info["label"]
        }
        if callable(key_style["label"]):
            key_style["label"] = key_style["label"](gen_args(deck, key, info))
        elif not isinstance(key_style["label"], str):
            print(f"Label {key_style['label']} is not a string or callable")
            return
    else:
        print(f"Key {key} not configured")
        return
    image = active_render_key_image(deck, key_style["font"], key_style["label"], info)

    with deck:
        deck.set_key_image(key, image)
