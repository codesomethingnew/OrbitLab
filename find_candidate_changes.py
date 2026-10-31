from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

BASE = Path(__file__).parent
DATA = BASE / "Data" / "demo_sequence"
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

print("OrbitLab — Candidate Brightness Changes")
print("---------------------------------------")

files = sorted(DATA.glob("ah-demo-*.fits"))

if len(files) < 3:
    raise SystemExit(
        "At least three FITS images are needed in "
        f"{DATA}. These files are not included with OrbitLab. See the README."
    )

images = []

for file in files:
    with fits.open(file) as hdul:
        data = hdul[0].data.astype(np.float32)

    valid = np.isfinite(data)
    if not valid.any():
        raise ValueError(f"No valid image pixels: {file.name}")

    data[~valid] = np.median(data[valid])
    data -= np.median(data)
    images.append(data)

    print(f"Loaded: {file.name}")

if len({image.shape for image in images}) != 1:
    raise ValueError("Observation dimensions do not match.")

# Compare each observation with the first
reference = images[0]
detections = []

for index, image in enumerate(images[1:], start=2):
    difference = image - reference

    median = np.median(difference)
    mad = np.median(np.abs(difference - median))
    sigma = 1.4826 * mad

    if sigma <= 0:
        print(f"Observation {index}: unable to estimate noise.")
        detections.append([])
        continue

    mask = (difference > 5 * sigma).astype(np.uint8) * 255

    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )

    points = []

    for label in range(1, count):
        area = stats[label, cv2.CC_STAT_AREA]

        if 2 <= area <= 100:
            x, y = centroids[label]
            points.append((x, y))

    detections.append(points)

    print(f"Observation {index}: {len(points)} candidate regions")

# Visualize candidate regions
fig, axes = plt.subplots(2, 2, figsize=(11, 11), constrained_layout=True)

for index, (ax, image) in enumerate(zip(axes.flat, images)):
    low, high = np.percentile(image, [1, 99.5])

    ax.imshow(
        image,
        cmap="gray",
        origin="lower",
        vmin=low,
        vmax=high
    )

    ax.set_title(f"Observation {index + 1}")

    if index > 0:
        for x, y in detections[index - 1]:
            circle = plt.Circle(
                (x, y),
                radius=12,
                edgecolor="red",
                facecolor="none",
                linewidth=1.5
            )
            ax.add_patch(circle)

    ax.set_xlabel("X Pixels")
    ax.set_ylabel("Y Pixels")

fig.suptitle("OrbitLab — Candidate Brightness Changes (unconfirmed)")

output = RESULTS / "candidate_changes.png"
plt.savefig(output, dpi=150, bbox_inches="tight")

print(f"\nVisualization saved: {output}")
print("Note: Highlighted regions are unverified changes, not confirmed asteroids.")

plt.show()
