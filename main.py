import os
from palettes import THEMES


def main():
    print(f"{len(THEMES)} are available for analiz")
    for theme_name in THEMES:
        print(f"- {theme_name}")

    # (s/g)ooner gonna add walk through the files in current dir


if __name__ == "main":
    main()
