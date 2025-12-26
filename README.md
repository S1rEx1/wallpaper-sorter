


# Wallpaper Theme Sorter

An automated utility that analyzes the dominant colors of your wallpapers and renames them based on popular color schemes like **Gruvbox**, **Catppuccin**, **Nord**, etc.  star plz
## 🚀 Features

- **Automated Scanning**: Scans directories for common image formats (`.jpg`, `.png`, `.webp`).
- **Color Analysis**: Uses K-Means inspired logic to find dominant colors.
- **Theme Matching**: Calculates Euclidean distance between image colors and official theme palettes.
- **Smart Renaming**: Prepends the theme name to the file (e.g., `wallpaper.jpg` -> `gruvbox_wallpaper.jpg`) and avoids double-renaming.
- **Undo Functionality**: Easily remove theme tags from your filenames using the `-u` flag.

## 🎨 Supported Themes currently

Currently, the utility recognizes:
- **Gruvbox**, **Catppuccin Mocha**, **Nord**, **Dracula**
- **Tokyo Night** (Deep blues and purples)
- **Everforest** (Soft forest greens)
- **Rose Pine** (Moody dusky colors)
- **Kanagawa** (Traditional Japanese palette)

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/S1rEx1/wallpaper-sorter
cd wallpaper-sorter
```

2. **Set up a virtual environment (recommended):**

```Bash
python -m venv venv
source venv/bin/activate 
# On Windows: venv\Scripts\activate (actually idk wether it works on windows or not, i dont gaf)
```
    
3. **Install dependencies:**

``` Bash
pip install Pillow
```
## 📖 Usage

Tagging themes:

```Bash
python main.py /path/to/your/wallpapers
```
Untagging themes:
```Bash
python main.py /path/to/wallpapers -u
```
Help:
```Bash
python main.py --help
```

If no path is provided, it will scan the **current directory**.

## 🧠 How it works

1. **Downscaling**: The image is resized to 150x150 pixels to ensure high performance without losing color context.
    
2. **Dominant Color Extraction**: The script identifies the most frequent pixel color in the image.
    
3. Distance Calculation: It measures the "distance" between the image's dominant color and the predefined HEX values in palettes.py using the Euclidean distance formula:
    
    $d = \sqrt{(r_2-r_1)^2 + (g_2-g_1)^2 + (b_2-b_1)^2}$
    
4. **Classification**: The image is assigned the theme with the smallest color distance.
    
## ⚙️ Configuration

You can add your own themes or modify existing ones in `palettes.py`:
```Python
THEMES = {
    "my_theme": ["#HEXCODE1", "#HEXCODE2"],
}
```
