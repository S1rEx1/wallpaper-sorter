import os
from palettes import THEMES
from PIL import Image
from utils import hex_to_rgb, color_distance


def main():
    test_image = "test.jpg"
    if os.path.exists(test_image):
        dom_color = get_dominant_color(test_image)
        if dom_color:
            theme = match_theme(dom_color)
            print(f"Image: {test_image}")
            print(f"Dominant RGB: {dom_color}")
            print(f"The theme: {theme}")
    else:
        print("erore")


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

def match_theme(dominant_color: tuple) -> str:
    """
    Matches a given RGB color to the closest theme defined in THEMES
    
    Args:
        dominant_color (tuple): (R, G, B) of the image
        
    Returns:
        str: The name of the matching theme
    """
    best_match = None
    min_distance = float('inf')

    for theme_name, hex_colors in THEMES.items():
        for hex_color in hex_colors:
            theme_rgb = hex_to_rgb(hex_color)
            distance = color_distance(dominant_color, theme_rgb)
            
            if distance < min_distance:
                min_distance = distance
                best_match = theme_name
                
    return best_match

if __name__ == "__main__":
    main()
