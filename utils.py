# why hex is hex? should've been hehehehe instead of hex(sorry)


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
