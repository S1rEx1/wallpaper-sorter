import os
from palettes import THEMES
from PIL import Image
from utils import hex_to_rgb


def main():
    print("---- IUSEARCHBTW theme sorter ----")
    print("loading,,,,,,,,,,,,,,,")  # why does everyone use '.'? comma is funnier,,,
    for theme, colors in THEMES.items():
        rgb_colors = [hex_to_rgb(c) for c in colors]
        print(f'themme "{theme}" loaded with {len(rgb_colors)} reference colors')

    # TODO: scanning loop (zalup)


def get_dominant_color(image_path: str) -> tuple:
    """
    Opens an image and finds the main color

    Args:
        image_path (str): Path to the image file

    Returns:
        tuple: (R, G, B) of the main color or None
    """

    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")

            # not to fuck your hardware we gonna make the image smaller(who are 'we'?)
            img = img.resize((150, 150))
            colors = img.getcolors(maxcolors=150 * 150)
            most_frequent = sorted(colors, key=lambda x: x[0], reverse=True)[0]
            return most_frequent[1]  # -> tuple (R, G, B)

    except Exception as e:
        print(f"erore processing {image_path}: {e}")
        return None


if __name__ == "__main__":
    main()
