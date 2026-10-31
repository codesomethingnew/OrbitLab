from pathlib import Path

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ImageNormalize, ZScaleInterval

BASE = Path(__file__).parent

image_path = (
    BASE / "Data" / "horsehead" / "HorseHead.fits"
)

results_folder = BASE / "results"
results_folder.mkdir(exist_ok=True)

if not image_path.is_file():
    raise SystemExit(
        f"Image file not found: {image_path}\n"
        "This file is not included with OrbitLab. See the README."
    )

# Open the astronomical image
with fits.open(image_path) as hdul:
    image = hdul[0].data

if image is None:
    raise SystemExit("No image data found.")

# Adjust brightness and contrast for visualization
norm = ImageNormalize(image, interval=ZScaleInterval())

plt.figure(figsize=(10, 8), constrained_layout=True)

plt.imshow(
    image,
    cmap="gray",
    origin="lower",
    norm=norm
)

plt.title("OrbitLab — Horsehead Nebula (astronomical image)")
plt.xlabel("X Pixels")
plt.ylabel("Y Pixels")
plt.colorbar(label="Pixel intensity")

output = results_folder / "horsehead_visualization.png"

plt.savefig(output, dpi=150, bbox_inches="tight")

print("Astronomical image loaded successfully!")
print(f"Visualization saved: {output}")

plt.show()