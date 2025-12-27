import argparse
import os
import sys

from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

from palettes import THEMES
from utils import color_distance, hex_to_rgb, is_vibrant, lab_distance, rgb_to_lab


class AlgorithmConfig:
    def __init__(self, vibrant_weight=2.0, dull_weight=0.5,
                 saturation_threshold=0.15, brightness_low=40, brightness_high=230):
        self.vibrant_weight = vibrant_weight
        self.dull_weight = dull_weight
        self.saturation_threshold = saturation_threshold
        self.brightness_low = brightness_low
        self.brightness_high = brightness_high

EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
)  # yeah, it prolly may slow down tool a bit, but it is still better then trying to guess the txt theme


def main():
    parser = argparse.ArgumentParser(description="Sort wallpapers by color themes.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the images directory.")
    parser.add_argument("-u", "--untag", action="store_true", help="Remove theme tags from filenames.")
    parser.add_argument("--algorithm", choices=["kmeans", "quantize"], default="kmeans",
                        help="Color extraction algorithm to use: kmeans (default) or quantize")
    parser.add_argument("--clusters", type=int, default=5,
                        help="Number of clusters for K-means algorithm (default: 5)")
    parser.add_argument("--vibrant-weight", type=float, default=2.0,
                        help="Weight for vibrant colors (default: 2.0)")
    parser.add_argument("--dull-weight", type=float, default=0.5,
                        help="Weight for dull colors (default: 0.5)")
    parser.add_argument("--saturation-threshold", type=float, default=0.15,
                        help="Saturation threshold for vibrant color detection (default: 0.15)")
    parser.add_argument("--brightness-low", type=float, default=40,
                        help="Lower brightness threshold (default: 40)")
    parser.add_argument("--brightness-high", type=float, default=230,
                        help="Higher brightness threshold (default: 230)")
    parser.add_argument("--log", type=str, help="Path to save analysis log file")
    parser.add_argument("--color-space", choices=["lab", "rgb"], default="lab",
                        help="Color space for distance calculation: lab (default) or rgb")
    parser.add_argument("--kmeans-iterations", type=int, default=10,
                        help="Number of iterations for K-means algorithm (default: 10)")

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory.")
        return

    if args.untag:
        remove_tags(args.path)
    else:
        process_directory(args.path, args.algorithm, args.clusters, args.vibrant_weight, args.dull_weight,
                         args.saturation_threshold, args.brightness_low, args.brightness_high, args.log,
                         args.color_space, args.kmeans_iterations)
    print("Done!")


def get_dominant_color(image_path: str) -> tuple:
    """
    Opens an image and finds the main color using K-means
    """

    try:
        # Use the K-means function to get dominant colors with counts
        palette_with_counts = get_dominant_colors_kmeans(image_path, n_colors=1)
        if not palette_with_counts:
            return None
        # Return the most dominant color
        return palette_with_counts[0][0]  # Get the RGB tuple of the most dominant color

    except Exception as e:
        print(f"error processing {image_path}: {e}")
        return None



def get_dominant_colors_kmeans(image_path: str, n_colors=5, n_init=10) -> list:
    """
    Extracts dominant colors from the image using K-means clustering.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((150, 150))

            img_array = np.array(img)
            height, width, channels = img_array.shape
            reshaped_img = img_array.reshape((height * width, channels))

            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=n_init)
            kmeans.fit(reshaped_img)

            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_

            unique, counts = np.unique(labels, return_counts=True)

            color_count_pairs = [(tuple(color), count) for color, count in zip(colors, counts)]
            color_count_pairs.sort(key=lambda x: x[1], reverse=True)

            return color_count_pairs
    except Exception as e:
        print(f"Error extracting palette with K-means: {e}")
        return []


def get_palette(image_path: str, count=5) -> list:
    """
    Extracts a palette of dominant colors from the image.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((150, 150))

            paletted = img.quantize(colors=count).convert("RGB")
            colors = paletted.getcolors()

            return [c[1] for c in colors]
    except Exception as e:
        print(f"Error extracting palette: {e}")
        return []


def match_theme(image_palette: list, config: 'AlgorithmConfig', color_space="lab") -> str:
    """
    Advanced scoring system to find the best theme match using K-means results.
    """
    scores = {theme: 0 for theme in THEMES}

    total_pixels = sum([count for _, count in image_palette]) if image_palette else 1

    for color_rgb, pixel_count in image_palette:
        vibrant_weight = config.vibrant_weight if is_vibrant(color_rgb,
            config.saturation_threshold, config.brightness_low, config.brightness_high) else config.dull_weight
        pixel_percentage = pixel_count / total_pixels
        weight = vibrant_weight * pixel_percentage

        best_theme = None
        min_dist = float("inf")

        for theme_name, hex_colors in THEMES.items():
            for hex_color in hex_colors:
                theme_rgb = hex_to_rgb(hex_color)

                if color_space == "lab":
                    color_lab = rgb_to_lab(color_rgb)
                    theme_lab = rgb_to_lab(theme_rgb)
                    dist = lab_distance(color_lab, theme_lab)
                else:  # rgb
                    dist = color_distance(color_rgb, theme_rgb)

                if dist < min_dist:
                    min_dist = dist
                    best_theme = theme_name

        if best_theme:
            scores[best_theme] += weight

    return max(scores, key=scores.get)


def process_directory(directory_path: str, algorithm="kmeans", clusters=5, vibrant_weight=2.0, dull_weight=0.5,
                     saturation_threshold=0.15, brightness_low=40, brightness_high=230, log_path=None, color_space="lab",
                     kmeans_iterations=10):
    """
    Scans the directory and renames images using weighted palette analysis.
    """
    print(f"Analyzing images in: {directory_path} using {algorithm} algorithm")

    config = AlgorithmConfig(vibrant_weight, dull_weight, saturation_threshold, brightness_low, brightness_high)

    files = [f for f in os.listdir(directory_path) if f.lower().endswith(EXTENSIONS)]

    if not files:
        print("No supported images found.")
        return

    log_content = []
    for filename in files:
        if any(filename.startswith(f"{theme}_") for theme in THEMES):
            continue

        file_path = os.path.join(directory_path, filename)

        try:
            if algorithm == "kmeans":
                palette_with_counts = get_dominant_colors_kmeans(file_path, n_colors=clusters, n_init=kmeans_iterations)
                theme = match_theme(palette_with_counts, config, color_space)
            else:  # quantize
                palette = get_palette(file_path, count=clusters)
                if not palette:
                    print(f"Skipping {filename}: Could not extract colors.")
                    continue
                theme = match_theme([(color, 1) for color in palette], config, color_space)  # Simple counts for quantize

            new_name = f"{theme}_{filename}"
            new_path = os.path.join(directory_path, new_name)

            os.rename(file_path, new_path)
            message = f"Tagged: [{theme.upper()}] -> {filename}"
            print(message)

            # Store for log
            log_content.append(message)

        except Exception as e:
            message = f"Failed to process {filename}: {e}"
            print(message)
            log_content.append(message)

    # Write log if path provided
    if log_path:
        with open(log_path, 'w') as log_file:
            log_file.write("\n".join(log_content))
        print(f"Log saved to: {log_path}")

    print("\nProcessing complete!")

def remove_tags(directory_path: str):
    """Removes theme prefixes from filenames."""
    print("Untagging files")
    for filename in os.listdir(directory_path):
        for theme in THEMES:
            prefix = f"{theme}_"
            if filename.startswith(prefix):
                new_name = filename[len(prefix) :]
                old_path = os.path.join(directory_path, filename)
                new_path = os.path.join(directory_path, new_name)
                os.rename(old_path, new_path)
                print(f"Restored: {filename} -> {new_name}")
                break


if __name__ == "__main__":
    main()
