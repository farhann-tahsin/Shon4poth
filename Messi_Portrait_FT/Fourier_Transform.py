"""
Lionel Messi Portrait using the Fourier Transform 

"""

import json
import numpy as np
#import cupy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Loading complex points

with open("complex_points.json", "r") as f:
    raw = json.load(f)

points = np.array([complex(p[0], p[1]) for p in raw])
N = len(points)

# Computing DFT coefficients

F = np.fft.fft(points) / N
freqs = np.fft.fftfreq(N, d=1.0 / N).astype(int)

coefficients = []
for freq, coeff in zip(freqs, F):
    coefficients.append({"freq": int(freq), "amp": abs(coeff), "coeff": coeff})

coefficients.sort(key=lambda d: d["amp"], reverse=True)

# Pre-computing the full traced path

NUM_FRAMES  = N
time_values = np.linspace(0, 1, NUM_FRAMES, endpoint=False)

path_x = np.zeros(NUM_FRAMES)
path_y = np.zeros(NUM_FRAMES)

for i, t in enumerate(time_values):
    pos = complex(0, 0)
    for d in coefficients:
        pos += d["coeff"] * np.exp(1j * 2 * np.pi * d["freq"] * t)
    path_x[i] = pos.real
    path_y[i] = pos.imag

# Figure

fig, ax = plt.subplots(figsize=(9, 9))
ax.set_facecolor("black")
fig.patch.set_facecolor("black")
ax.set_aspect("equal")
ax.axis("off")

margin = 1.15
x_min, x_max = path_x.min(), path_x.max()
y_min, y_max = path_y.min(), path_y.max()
cx = (x_min + x_max) / 2
cy = (y_min + y_max) / 2
half_range = max(x_max - x_min, y_max - y_min) / 2 * margin
ax.set_xlim(cx - half_range, cx + half_range)
ax.set_ylim(cy - half_range, cy + half_range)

circle_artists = []
spoke_artists  = []
for _ in coefficients:
    circ = Circle((0, 0), radius=0, fill=False,
                  color="cyan", linewidth=0.3, alpha=0.4)
    ax.add_patch(circ)
    circle_artists.append(circ)

    ln, = ax.plot([], [], color="white", linewidth=0.5, alpha=0.7)
    spoke_artists.append(ln)

trace, = ax.plot([], [], color="gold", linewidth=1.0, zorder=5)
dot,   = ax.plot([], [], "o", color="red", markersize=3, zorder=6)

all_artists = circle_artists + spoke_artists + [trace, dot]

# Animation

def init():
    for c in circle_artists:
        c.set_radius(0)
        c.center = (0, 0)
    for ln in spoke_artists:
        ln.set_data([], [])
    trace.set_data([], [])
    dot.set_data([], [])
    return all_artists


def update(frame):
    t   = time_values[frame]
    pos = complex(0, 0)

    for d, circ, ln in zip(coefficients, circle_artists, spoke_artists):
        center = pos
        pos    = pos + d["coeff"] * np.exp(1j * 2 * np.pi * d["freq"] * t)
        r      = abs(pos - center)
        circ.center = (center.real, center.imag)
        circ.set_radius(r)
        ln.set_data([center.real, pos.real], [center.imag, pos.imag])

    trace.set_data(path_x[:frame + 1], path_y[:frame + 1])
    dot.set_data([pos.real], [pos.imag])

    return all_artists


ani = animation.FuncAnimation(
    fig,
    update,
    frames=range(0, NUM_FRAMES, 150),
    init_func=init,
    interval=1,
    blit=True,
    repeat=False, 
)

# Show

plt.tight_layout()
plt.show()

