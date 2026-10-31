from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Project folders
BASE = Path(__file__).parent
DATA = BASE / "Data" / "demo_sequence"
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

print("OrbitLab — Noise Filtering")
print("--------------------------")

# Load two images from the demonstration sequence
for needed in (DATA / "ah-demo-1.fits", DATA / "ah-demo-2.fits"):
    if not needed.is_file():
        raise SystemExit(
            f"File not found: {needed}\n"
            "This file is not included with OrbitLab. See the README."
        )

with fits.open(DATA / "ah-demo-1.fits") as hdul:
    image1 = hdul[0].data.astype(np.float32)

with fits.open(DATA / "ah-demo-2.fits") as hdul:
    image2 = hdul[0].data.astype(np.float32)

if image1.shape != image2.shape:
    raise ValueError("Images have different dimensions.")

# Replace invalid pixels with each image's median
for image in (image1, image2):
    valid = np.isfinite(image)
    if not valid.any():
        raise ValueError("Image contains no valid pixels.")
    image[~valid] = np.median(image[valid])

# Remove the overall background level
image1 -= np.median(image1)
image2 -= np.median(image2)

# Calculate differences
difference = image2 - image1

# Estimate background noise using median absolute deviation
median_diff = np.median(difference)
mad = np.median(np.abs(difference - median_diff))
noise_sigma = 1.4826 * mad

print(f"Estimated difference noise: {noise_sigma:.2f}")

if noise_sigma <= 0:
    raise ValueError("Cannot estimate a positive noise level.")

# Highlight changes greater than 5 times the estimated noise
threshold = 5 * noise_sigma

positive_changes = (difference > threshold).astype(np.uint8) * 255
negative_changes = (difference < -threshold).astype(np.uint8) * 255

# Remove isolated single-pixel noise
kernel = np.ones((2, 2), np.uint8)

positive_filtered = cv2.morphologyEx(
    positive_changes, cv2.MORPH_OPEN, kernel
)

negative_filtered = cv2.morphologyEx(
    negative_changes, cv2.MORPH_OPEN, kernel
)

print(f"Detection threshold: {threshold:.2f}")
print(f"Positive-change pixels: {np.count_nonzero(positive_filtered)}")
print(f"Negative-change pixels: {np.count_nonzero(negative_filtered)}")

# Display results
fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), constrained_layout=True)

limit = max(np.percentile(np.abs(difference), 99.5), 1)

axes[0].imshow(
    difference,
    cmap="seismic",
    origin="lower",
    vmin=-limit,
    vmax=limit
)
axes[0].set_title("Original Difference")

axes[1].imshow(
    positive_filtered,
    cmap="gray",
    origin="lower",
    vmin=0,
    vmax=255
)
axes[1].set_title("Positive Changes")

axes[2].imshow(
    negative_filtered,
    cmap="gray",
    origin="lower",
    vmin=0,
    vmax=255
)
axes[2].set_title("Negative Changes")

for ax in axes:
    ax.set_xlabel("X Pixels")
    ax.set_ylabel("Y Pixels")

fig.suptitle("OrbitLab — Significant Image Changes (candidates, not confirmed objects)")

output = RESULTS / "filtered_differences.png"
plt.savefig(output, dpi=150, bbox_inches="tight")

print(f"Result saved: {output}")

plt.show()