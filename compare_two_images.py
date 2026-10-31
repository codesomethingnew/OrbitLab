from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ImageNormalize, ZScaleInterval

# Project folders
BASE = Path(__file__).parent
DATA = BASE / "Data" / "demo_sequence"
RESULTS = BASE / "results"

RESULTS.mkdir(exist_ok=True)

print("OrbitLab — Image Comparison")
print("--------------------------------------")

# Load the first two images in the demonstration sequence
file1 = DATA / "ah-demo-1.fits"
file2 = DATA / "ah-demo-2.fits"

for needed in (file1, file2):
    if not needed.is_file():
        raise SystemExit(
            f"File not found: {needed}\n"
            "This file is not included with OrbitLab. See the README."
        )

with fits.open(file1) as hdul:
    image1 = hdul[0].data.astype(np.float32)

with fits.open(file2) as hdul:
    image2 = hdul[0].data.astype(np.float32)

# Check image dimensions
if image1.shape != image2.shape:
    raise ValueError("The images have different dimensions!")

print(f"Image dimensions: {image1.shape}")

# Replace invalid pixel values
image1 = np.nan_to_num(image1)
image2 = np.nan_to_num(image2)

# Subtract the background level from each image
image1 = image1 - np.median(image1)
image2 = image2 - np.median(image2)

# Calculate the difference between observations
difference = image2 - image1

print("Image comparison completed!")

# Display the results
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), constrained_layout=True)

norm1 = ImageNormalize(image1, interval=ZScaleInterval())
norm2 = ImageNormalize(image2, interval=ZScaleInterval())

axes[0].imshow(image1, cmap="gray", origin="lower", norm=norm1)
axes[0].set_title("Observation 1")

axes[1].imshow(image2, cmap="gray", origin="lower", norm=norm2)
axes[1].set_title("Observation 2")

# Show positive and negative changes
limit = np.percentile(np.abs(difference), 99.5)

if limit == 0:
    limit = 1

axes[2].imshow(
    difference,
    cmap="seismic",
    origin="lower",
    vmin=-limit,
    vmax=limit
)
axes[2].set_title("Difference Image")

for ax in axes:
    ax.set_xlabel("X Pixels")
    ax.set_ylabel("Y Pixels")

fig.suptitle("OrbitLab — Image Comparison (demonstration sequence)")

output = RESULTS / "image_difference.png"
plt.savefig(output, dpi=150, bbox_inches="tight")

print(f"Result saved: {output}")

plt.show()