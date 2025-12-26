# why hex is hex? should've been hehehehe instead of hex(sorry)
import math


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Converts a HEHEHE color string to an RGB tuple

    Args:
        hex_color (str): hehehe color string (e.g #ff0000)

    Returns:
        tuple: rgb tuple representing (R, G, B) (e.g. (255,0,0))
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb: tuple) -> tuple:
    """
    Converts an RGB color tuple to the LAB color space.
    This allows for more human-like color comparison.
    """
    r, g, b = [x / 255.0 for x in rgb]

    r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b / 12.92

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    def f(t):
        return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116

    l = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b_lab = 200 * (f(y) - f(z))

    return (l, a, b_lab)

def is_vibrant(rgb: tuple) -> bool:
    """
    Checks if a color is vibrant enough to be an accent.
    Filters out pure black, pure white, and dull grays.
    """
    r, g, b = rgb
    max_c = max(rgb)
    min_c = min(rgb)
    sat = (max_c - min_c) / 255.0 if max_c != 0 else 0
    
    brightness = sum(rgb) / 3
    
    # Ignore very dark (<15%), very bright (>90%), and very gray (<15% saturation)
    if brightness < 40 or brightness > 230 or sat < 0.15:
        return False
    return True

def lab_distance(lab1: tuple, lab2: tuple) -> float:
    """Calculates Euclidean distance in LAB space (Delta E)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))

def color_distance(color1: tuple, color2: tuple) -> float:
    """
    Calculates the Euclidean distance between two RGB colors

    Args:
        color1 (tuple): (R, G, B)
        color2 (tuple): (R, G, B)

    Returns:
        float: The distance value. Lower means more similar
    """
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))
