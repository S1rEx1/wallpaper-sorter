import os
from palettes import THEMES
from PIL import Image
from utils import hex_to_rgb, color_distance
import sys

EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp') # yeah, it prolly may slow down tool a bit, but it is still better then trying to guess the txt theme


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    if os.path.isdir(target_dir):
        process_directory(target_dir)
        print("les go, ur welcome")
    else:
        print(f"erore: {target_dir} is not a valid directory.")


def get_dominant_color(image_path: str) -> tuple:
    """
    Opens an image and finds the main color
    """

    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")

            # not to fuck your hardware we gonna make the image smaller(who are 'we'?)
            img = img.resize((150, 150))
            colors = img.getcolors(maxcolors=150 * 150)
            if not colors:
                return None
            most_frequent = sorted(colors, key=lambda x: x[0], reverse=True)[0]
            return most_frequent[1]

    except Exception as e:
        print(f"erore processing {image_path}: {e}")
        return None

def match_theme(dominant_color: tuple) -> str:
    """
    Matches a given RGB color to the closest theme defined in THEMES
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

def process_directory(directory_path: str):
    """
    Scans the directory and renames images based on themes
    """

    print(f'dont look behing urself, scanning {directory_path}')

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if any(filename.startswith(f"{theme}_") for theme in THEMES):
            print(f"skippink {filename} (already categorized)")
            continue

        dominant_rgb = get_dominant_color(file_path)

        if dominant_rgb:
            theme = match_theme(dominant_rgb)
            new_filename = f"{theme}_{filename}"
            new_path = os.path.join(directory_path, new_filename)
            
            os.rename(file_path, new_path)
            print(f"renamed {filename} -> {new_filename}")

if __name__ == "__main__":
    main()
