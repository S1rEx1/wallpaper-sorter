


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

Specify algorithm:
```Bash
python main.py /path/to/your/wallpapers --algorithm kmeans    # Use K-means (default)
python main.py /path/to/your/wallpapers --algorithm quantize  # Use quantization (old algorithm)
```

Specify number of clusters (for K-means algorithm):
```Bash
python main.py /path/to/your/wallpapers --clusters 7  # Use 7 clusters for K-means (default: 5)
```

Configure color weights:
```Bash
python main.py /path/to/your/wallpapers --vibrant-weight 3.0 --dull-weight 0.3  # Customize color weights (defaults: 2.0 and 0.5)
```

Configure color sensitivity:
```Bash
python main.py /path/to/your/wallpapers --saturation-threshold 0.2 --brightness-low 50 --brightness-high 200  # Customize sensitivity (defaults: 0.15, 40, 230)
```

If no path is provided, it will scan the **current directory**.


## 🧠 How it works

1. **Quantization**: The image is downscaled and quantized to extract the top 5 dominant colors.
2. **LAB Conversion**: Colors are converted from RGB to **CIELAB** space, which is designed to be perceptually uniform.
3. **Vibrancy Check**: Each color is analyzed for saturation and brightness. Vibrant "accent" colors receive a **2.0x weight**, while dull or near-neutral colors receive a **0.5x weight**.
4. **Scoring**: 
   - For each extracted color, the script finds the closest match among all defined themes.
   - The theme associated with the match receives points based on the color's weight.
   - The theme with the highest total score wins.
5. **Renaming**: The winning theme name is prepended to the filename.
    
## ⚙️ Configuration

You can add your own themes or modify existing ones in `palettes.py`:
```Python
THEMES = {
    "my_theme": ["#HEXCODE1", "#HEXCODE2"],
}
```
