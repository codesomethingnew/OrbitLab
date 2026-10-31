from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# This script makes its own artificial star field.
# It needs no downloaded files. Everything here is a simulation.
BASE = Path(__file__).parent
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

print("OrbitLab — Simulated Object Movement")
print("------------------------------------")
print("Everything in this activity is artificial. It is NOT real sky data.")

SIZE = 200
rng = np.random.default_rng(42)  # the same seed gives the same stars each time

# Fixed random background noise and artificial stars
background = rng.normal(20, 3, (SIZE, SIZE))
yy, xx = np.mgrid[0:SIZE, 0:SIZE]


def add_dot(image, x, y, brightness, width=1.5):
    """Add one bright, soft dot to the image."""
    image += brightness * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * width**2))


for _ in range(40):
    x, y = rng.uniform(5, SIZE - 5, 2)
    add_dot(background, x, y, rng.uniform(40, 200))

# One artificial "object" moves a little in each frame
positions = [(60, 100), (100, 95), (140, 90)]
frames = []

for number, (x, y) in enumerate(positions, start=1):
    frame = background.copy()
    add_dot(frame, x, y, 255, width=2.5)
    frames.append(frame)
    print(f"Created simulated image {number}: moving dot at x={x}, y={y}")

fig, axes = plt.subplots(1, 3, figsize=(13, 5), constrained_layout=True)

for number, (ax, frame, (x, y)) in enumerate(zip(axes, frames, positions), start=1):
    ax.imshow(frame, cmap="gray", origin="lower", vmin=0, vmax=255)
    ax.plot(x, y, "o", mfc="none", mec="red", ms=18)
    ax.set_title(f"Simulated image {number}")
    ax.set_xlabel("X pixels")
    ax.set_ylabel("Y pixels")

fig.suptitle(
    "OrbitLab — Simulated Object Movement (artificial, not real data)",
    fontsize=15,
)

output = RESULTS / "simulated_motion.png"
fig.savefig(output, dpi=150)
print(f"Saved: {output}")
print("The red circle marks the artificial moving dot.")

plt.show()
