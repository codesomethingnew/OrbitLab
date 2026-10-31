from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

# OrbitLab project folders
BASE = Path(__file__).parent
DATA = BASE / "Data" / "demo_sequence"
RESULTS = BASE / "results"

RESULTS.mkdir(exist_ok=True)

print("OrbitLab — Image Sequence Explorer")
print("----------------------------------")

# Find astronomical FITS images
images = sorted(DATA.glob("*.fits"))

print(f"Found {len(images)} FITS images in {DATA}")

if len(images) < 3:
    raise SystemExit(
        "At least 3 FITS images are needed. These files are not included "
        "with OrbitLab. See the README."
    )

print("The image sequence is ready.")
print("\nReading each file...")
print("The text below is what each file says about itself.")
print("OrbitLab has not checked it.")
print("---------------------------------")

for image_path in images:
    with fits.open(image_path) as hdul:
        image_data = hdul[0].data
        header = hdul[0].header

        print(f"\nFile: {image_path.name}")
        print(f"Image shape: {image_data.shape if image_data is not None else 'No image data'}")
        print(f"Date (as written in the file): {header.get('DATE-OBS', 'Not available')}")
        print(f"Exposure time: {header.get('EXPTIME', 'Not available')}")
        print(f"Telescope (as written in the file): {header.get('TELESCOP', 'Not available')}")

print("\nShowing the images...")
fig, axes = plt.subplots(2, 2, figsize=(12, 11), constrained_layout=True)

for ax, image_path in zip(axes.flat, images):
    with fits.open(image_path) as hdul:
        image_data = hdul[0].data.astype(np.float32)

    # Improve contrast for astronomical images
    low, high = np.percentile(image_data, [1, 99.5])

    ax.imshow(
        image_data,
        cmap="gray",
        origin="lower",
        vmin=low,
        vmax=high
    )

    ax.set_title(image_path.name)
    ax.set_xlabel("X Pixels")
    ax.set_ylabel("Y Pixels")

fig.suptitle("OrbitLab — Demonstration Image Sequence", fontsize=16)

output_path = RESULTS / "image_sequence.png"
plt.savefig(output_path, dpi=150)
print(f"Visualization saved: {output_path}")

plt.show()