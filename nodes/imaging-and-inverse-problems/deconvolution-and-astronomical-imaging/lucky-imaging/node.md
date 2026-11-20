---
tag: AZ0FZD
kind: technique
slug: lucky-imaging
name: Lucky imaging
aliases:
- frame selection imaging
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: intro
summary: "Take many short exposures through turbulence, keep the few sharpest, and shift and add them into one near diffraction limited image."
history:
  year: 1978
  people: [David L. Fried]
  note: "Fried (1978) computed the probability that a short exposure through turbulence is nearly free of distortion; Law, Mackay and Baldwin (2006) showed lucky imaging in the visible with fast low-noise cameras."
prereqs: [point-spread-function, image-registration]
see_also: [speckle-interferometry, knox-thompson-method, speckle-masking, drizzle, cross-correlation, zonal-wavefront-reconstruction, phase-diversity, super-resolution]
sources:
  - paper: doi:10.1364/JOSA.68.001651
    title: "D. L. Fried, Probability of getting a lucky short-exposure image through turbulence, Journal of the Optical Society of America 68(12), 1978"
    locator: "pp. 1651 to 1658 (the probability 5.6 exp(-0.1557 (D/r0)^2) of a good exposure, for D/r0 at least 3.5)"
  - paper: doi:10.1051/0004-6361:20053695
    title: "N. M. Law, C. D. Mackay and J. E. Baldwin, Lucky imaging, high angular resolution imaging in the visible from the ground, Astronomy and Astrophysics 446(2), 2006"
    locator: "pp. 739 to 745 (frame selection, registration and adding of short exposures with a low-noise camera)"
  - paper: doi:10.1364/JOSA.66.000207
    title: "R. J. Noll, Zernike polynomials and atmospheric turbulence, Journal of the Optical Society of America 66(3), 1976"
    locator: "pp. 207 to 211 (the residual phase variance 1.0299 (D/r0)^(5/3) with the piston removed and 0.134 (D/r0)^(5/3) with the tilt also removed)"
---

Lucky imaging makes a sharp image of the sky through atmospheric turbulence by taking many short exposures, keeping only the few in which the air happened to be calm over the telescope, and adding them after aligning them. It needs no model of the turbulence and no Fourier analysis, and it gives a true image with its phase. [Speckle interferometry](/speckle-interferometry/), the [Knox-Thompson method](/knox-thompson-method/) and [speckle masking](/speckle-masking/) use every frame and recover the Fourier modulus and phase statistically; lucky imaging throws most frames away and works directly on the images.

## In plain words

The air above a telescope moves all the time, and in most short exposures it spreads a star into a cloud of small grains. But the air is random, and now and then, for a few milliseconds, it is almost flat across the telescope. A picture taken at that moment is nearly as sharp as the telescope allows. Lucky imaging takes thousands of short pictures, grades each one by how sharp a star in it looks, and keeps only the best few. Each kept picture is moved so that its star sits at the same place, and then all kept pictures are added. The sum is much sharper than a long exposure. The price is that most of the light is thrown away. The method works best for telescopes that are not much larger than the size of the calm patches of air.

## When it applies

**Notation.** The telescope has diameter $D$, and $r_0$ is the Fried coherence length of the air at the observed wavelength. A frame is a short exposure $i_f$ with the PSF $s_f$; the diffraction-limited PSF $s_0$ has peak $s_0^{\max}$. The Strehl ratio of a PSF is its peak divided by $s_0^{\max}$, for the same total light.

Use it when these conditions hold:

- **Short exposures.** Each frame is shorter than the time the air needs to change, so that a calm moment is not averaged with the rest.
- **A modest $D/r_0$.** The chance of a good frame falls fast with $D/r_0$. Fried (1978) called an exposure good when the phase error over the aperture, with the tilt removed, has a mean square of at most 1 rad$^2$, and found the probability $P \approx 5.6\, e^{-0.1557 (D/r_0)^2}$ for $D/r_0 \ge 3.5$. This is 0.46 at $D/r_0 = 4$, 0.114 at 5, 1 in 49 at 6, 1 in 367 at 7 and 1 in 3800 at 8. For larger telescopes the method needs adaptive optics first, or a smaller aperture.
- **A reference star.** The sharpness and the shift of each frame are measured on a point star in the field, close enough to the target to share its air.
- **A camera with low read noise.** Short frames hold few photons, and the noise of each readout adds up over thousands of frames.

The tilt of the wavefront moves the image but does not blur it, which is why it is removed before grading: shifting the frame undoes it. The rest of the phase error blurs the image. With Kolmogorov turbulence its mean square over the aperture is $0.134\, (D/r_0)^{5/3}$ rad$^2$ (Noll, 1976), which is 1.35 at $D/r_0 = 4$ and 3.43 at $D/r_0 = 7$.

## The template

```pseudo id=main
LUCKY-IMAGING(frames i_1..i_F, fraction p)
L1  for each frame f do q_f ← the sharpness of the reference star in i_f   ▷ hole: the peak, a Strehl estimate, or another score
L2  K ← the ⌈p F⌉ frames with the largest q_f                              ▷ hole: the fraction p, a convention
L3  for each frame f in K do t_f ← the position of the reference star   ▷ hole: the peak pixel, a centroid, or a cross-correlation
L4  S ← sum over f in K of i_f moved by -t_f                             ▷ hole: whole-pixel shifts, subpixel shifts or drizzle
L5  return S / |K|
```

The holes are the score (L1), the fraction (L2), the alignment (L3) and the resampling (L4). The fraction $p$ trades sharpness against signal: a smaller $p$ keeps sharper frames, but fewer, so the sum has more noise. There is no best value in general; it is set by the seeing, the brightness of the target and the goal. With $p = 1$ the method is plain shift-and-add, which already removes the image motion. Line L3 is [image registration](/image-registration/), often by the peak of the [cross-correlation](/cross-correlation/) with a template; line L4 with subpixel shifts can use [drizzle](/drizzle/).

## Classic examples

**A point star in simulation.** A grid of $64 \times 64$ cells holds a disk pupil of diameter 16 cells. Phase screens are filtered white noise with the Kolmogorov phase spectrum $0.023\, r_0^{-5/3} f^{-11/3}$ on the periodic grid, so they lack scales larger than the grid (seed 1, 1000 frames). The score of a frame is its peak divided by the peak of the diffraction-limited PSF, and the shift is the position of the peak. The table gives the peak of the result, also divided by the diffraction peak.

| | $D/r_0 = 4$ | $D/r_0 = 7$ |
|---|---|---|
| mean phase variance with tilt removed (rad$^2$) | 1.382 | 3.512 |
| Noll value $0.134 (D/r_0)^{5/3}$ | 1.351 | 3.432 |
| frames with variance at most 1 rad$^2$ | 0.333 | 0.001 |
| Fried probability | 0.464 | 0.0027 |
| best, median and worst frame | 0.708, 0.300, 0.069 | 0.396, 0.130, 0.044 |
| long exposure (no shifts) | 0.093 | 0.031 |
| best 1% shifted and added | 0.646 | 0.351 |
| best 10% shifted and added | 0.547 | 0.262 |
| all frames shifted and added | 0.319 | 0.143 |

The variance of the screens matches the value of Noll within a few percent. The share of good frames is of the same size as Fried's estimate, which is an approximation and assumes scales that these screens do not have. At $D/r_0 = 7$, keeping the best 1% gives a peak 11 times that of the long exposure and 2.5 times that of shift-and-add of all frames. At $D/r_0 = 4$ the gain over the long exposure is about 7.

**Visible imaging from the ground.** Law, Mackay and Baldwin (2006) used a camera with very low read noise to take fast frames in the visible and selected, aligned and added the best of them, which reached near the diffraction limit on a telescope of moderate size.

**Planetary and lunar imaging.** Video of bright planets through a small telescope, graded and stacked by software, is the same technique, and it is widely used by amateur astronomers.

## Variations

- **Shift-and-add without selection.** Keep all frames ($p = 1$). It removes the motion but keeps the blur of bad frames.
- **Selection per region.** The air differs across a wide field, so grade and align each region of the frame on its own, with a nearby star or feature.
- **Weighting instead of selection.** Give each frame a weight that grows with its score, instead of keeping or dropping it.
- **Lucky imaging with adaptive optics.** Adaptive optics lowers the effective $D/r_0$, and frame selection then works on large telescopes.
- **Lucky deconvolution.** Deconvolve the sum with a PSF measured from the reference star in the same kept frames, for example with [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/).
- **Statistical methods on the same data.** [Speckle interferometry](/speckle-interferometry/), the [Knox-Thompson method](/knox-thompson-method/) and [speckle masking](/speckle-masking/) use every frame.

## Pitfalls

- **Grading on noise.** In faint frames the brightest pixel may be a noise spike, which biases both the score and the shift toward noise. Smooth the frame or use a template.
- **The sharp core and the halo.** Even good frames have a halo of scattered light around the core, so the sum is a sharp peak on a broad base, not a clean diffraction-limited PSF.
- **Too large an aperture.** Above $D/r_0$ of about 7, good frames are so rare that the kept frames are mostly the least bad ones.
- **Long exposures.** Frames longer than the time the air changes mix good and bad moments, and selection loses its effect.
- **Far from the reference.** A frame that is good at the reference star may be poor a few arcseconds away, because the air differs across the field.
- **Calling the fraction a constant.** The best fraction depends on the seeing and the target, and published values are conventions for given instruments.

## Exercises

1. Evaluate Fried's formula for $D/r_0 = 5$ and $D/r_0 = 8$. How many frames at 100 frames per second are needed to collect 20 good ones?
2. Show that shifting a frame does not change its power spectrum. Which of the two, speckle interferometry or shift-and-add, is affected by an error in the shifts?
3. If each frame has independent noise of standard deviation $\sigma$ per pixel, what is the noise of the sum of $K$ aligned frames divided by $K$? Use this to discuss the choice of $p$.
4. Reproduce the table above with another seed, and add a row for the best 3% of frames.
5. For a telescope of 2.5 m and $r_0 = 0.1$ m, compute $D/r_0$ and the Fried probability. What aperture diameter, used as a mask, would give 1 good frame in 10?

## References
