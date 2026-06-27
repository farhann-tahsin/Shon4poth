# Fourier Epicycles Portrait of Lionel Messi

A visualization of Lionel Messi's portrait drawn using Fourier Transform epicycles (rotating circles).

## How it works

1. A set of 14,460 coordinate points (outline of the portrait) is loaded from `complex_points.json`
2. A Discrete Fourier Transform (DFT) is applied to convert the points into frequency components
3. Each frequency component becomes a rotating circle (epicycle)
4. Together, all 14,460 epicycles trace out Messi's portrait

## ⚠️ Performance Warning

- 14,460 epicycles is a lot. Each frame redraws all circles and spokes
- Expected run time on an average PC: 5–15 minutes to complete the full animation
- The script may feel frozen or unresponsive at first, but it is still running
- Do not close the window unless you want to cancel

## Tips to Speed it Up

- Increase the step in `range(0, NUM_FRAMES, 150)` currently skips 150 frames at a time, increase to `300` or `500` for faster but rougher animation

## Requirements

numpy, matplotlib

## Author
Md. Farhan Tahsin Rifty
