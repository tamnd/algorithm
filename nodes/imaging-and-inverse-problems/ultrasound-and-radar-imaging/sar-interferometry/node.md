---
tag: W4DWFB
kind: technique
slug: sar-interferometry
name: SAR interferometry
aliases:
- InSAR
- interferometric SAR
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: Measure height or ground motion from the phase difference of two SAR images taken from close orbits or at different times.
history:
  year: 1974
  people: [L. C. Graham]
  note: "Graham (1974) proposed a radar interferometer for topographic mapping. Zebker and Goldstein (1986) made topographic maps from airborne interferometric SAR data, and Goldstein, Zebker and Werner (1988) unwrapped satellite interferograms."
prereqs: [synthetic-aperture-radar, phase-unwrapping]
see_also: [sar-image-formation, goldstein-branch-cut, least-squares-phase-unwrapping, image-registration, speckle, range-doppler-algorithm, phase-gradient-autofocus, min-cost-flow-problem]
sources:
  - paper: doi:10.1109/PROC.1974.9516
    title: "L. C. Graham, Synthetic interferometer radar for topographic mapping, Proceedings of the IEEE 62(6), 1974, 763"
    locator: "the idea of measuring height from the phase difference of two radar antennas (general locator)"
  - paper: doi:10.1029/JB091iB05p04993
    title: "Howard A. Zebker and Richard M. Goldstein, Topographic mapping from interferometric synthetic aperture radar observations, Journal of Geophysical Research 91(B5), 1986, 4993"
    locator: "topographic maps from airborne interferometric SAR (general locator)"
  - paper: doi:10.1029/RS023i004p00713
    title: "Richard M. Goldstein, Howard A. Zebker and Charles L. Werner, Satellite radar interferometry: two-dimensional phase unwrapping, Radio Science 23(4), 1988, 713"
    locator: "satellite interferograms, residues and branch cut unwrapping (general locator)"
  - paper: doi:10.1088/0266-5611/14/4/001
    title: "Richard Bamler and Philipp Hartl, Synthetic aperture radar interferometry, Inverse Problems 14(4), 1998, R1"
    locator: "review of the interferogram, coherence, flat earth removal, height sensitivity and unwrapping (general locator)"
  - paper: doi:10.1109/5.838084
    title: "Paul A. Rosen, Scott Hensley, Ian R. Joughin, Fuk K. Li, Soren N. Madsen, Ernesto Rodriguez and Richard M. Goldstein, Synthetic aperture radar interferometry, Proceedings of the IEEE 88(3), 2000, 333"
    locator: "the interferometric phase with the factor p = 1 for single-pass and p = 2 for repeat-pass systems (general locator)"
---

SAR interferometry (InSAR) measures the height of the ground, or its motion, from the phase difference of two complex [synthetic aperture radar](/synthetic-aperture-radar/) images of the same scene. The two images come from two antennas on one platform (single-pass) or from two passes of one antenna (repeat-pass). After the two images are aligned, the product $s_1 \overline{s_2}$ of each pixel pair cancels the random phase of the scatterers and keeps the phase of the path difference. A path difference of one wavelength, a few centimetres, gives one or two full turns of phase, so the method is very sensitive. The phase is wrapped, so InSAR is the main application of [phase unwrapping](/phase-unwrapping/). The quality of each pixel is measured by the coherence of the two images.

## In plain words

A radar image stores, at every pixel, a strength and a phase. The phase of one image looks random, because each pixel holds many small reflectors. But if the same ground is seen twice from almost the same place, the random part is the same both times. Multiply the first image by the mirror of the second, and the random part cancels. What is left is the difference of the two distances to the ground, measured in fractions of a wavelength.

That difference changes with the height of the ground, because the two antennas see it from slightly different angles. It also changes if the ground moved between two passes. Count the turns of phase (unwrap), scale them, and you get a height map or a map of movement in millimetres.

## When it applies

- Two complex SAR images (single look complex) of the same area, with the same wavelength and a similar viewing geometry.
- **The baseline is short enough.** The component of the baseline across the line of sight, $B_\perp$, must be well below the critical baseline, where the two images decorrelate completely.
- **The scene stays similar.** Vegetation, water, snow and long time gaps lower the coherence. Where it is low the phase is noise.
- **The geometry is known.** The orbits, the range $R$ and the look angle $\theta$ are needed to remove the flat earth phase and to scale the phase to height.

## The template

```pseudo id=main
INSAR(s1, s2, orbits)
L1  register s2 to s1 to a small fraction of a pixel          ▷ hole: registration method
L2  I(x) ← s1(x) · conj(s2(x))                                 ▷ the interferogram
L3  I(x) ← I(x) · exp(-i φ_flat(x))                            ▷ remove the flat earth phase
L4  Ī(x) ← average of I over a window W(x)                      ▷ multilook
L5  γ(x) ← |Σ_W s1 conj(s2)| / sqrt(Σ_W |s1|² · Σ_W |s2|²)      ▷ coherence
L6  ψ(x) ← arg Ī(x)                                             ▷ wrapped phase
L7  φ ← UNWRAP(ψ, weights from γ)                               ▷ hole: unwrapping method
L8  h ← φ λ R sin θ / (2π p B_perp)                             ▷ p = 2 repeat-pass, p = 1 single-pass
L9  return h and γ, mapped to ground coordinates
```

Line L1 aligns the speckle of the two images. A shift of a small fraction of a resolution cell already lowers the coherence, so registration is done on the image amplitudes or on the coherence itself. Line L3 subtracts the phase that a smooth reference surface (a flat earth or an ellipsoid) would give, so that what is left is the phase of the topography. Line L4 trades resolution for lower phase noise. Line L5 is the sample coherence, between 0 and 1. Line L7 is any unwrapping method: [Goldstein branch cuts](/goldstein-branch-cut/), weighted [least squares](/least-squares-phase-unwrapping/) or a [minimum cost flow](/min-cost-flow-problem/).

**The factor p.** For two antennas at the slant ranges $R$ and $R + \Delta R$, the phase difference is $\varphi = 2\pi p\, \Delta R / \lambda$. In a repeat-pass system, and in a system where both antennas transmit and receive on their own, each image has a two-way path, and $p = 2$. In a single-pass system with one antenna that transmits and two that receive, the transmit path is common, only the receive paths differ, and $p = 1$ (Rosen and others 2000 write the phase with this factor $p$). For a height $h$ above the reference surface, $\Delta R$ changes by $B_\perp h / (R \sin\theta)$, which gives line L8:

$$h = \frac{\varphi\, \lambda R \sin\theta}{2\pi p\, B_\perp}, \qquad \text{for repeat-pass} \quad h = \frac{\varphi\, \lambda R \sin\theta}{4\pi B_\perp}.$$

The height of one full turn of phase is the height of ambiguity, $h_{2\pi} = \lambda R \sin\theta / (p B_\perp)$.

## Classic examples

**Topography from a satellite pair.** A C-band system with $\lambda = 5.66$ cm, $R = 850$ km, $\theta = 23$ degrees and $B_\perp = 100$ m in repeat-pass mode has $h_{2\pi} = 0.0566 \cdot 850000 \cdot \sin 23° / (2 \cdot 100) = 94.0$ m. A residual phase of 0.8 rad after the flat earth removal means a height of $0.8 / (2\pi) \cdot 94.0 = 12.0$ m. With the same geometry in single-pass mode ($p = 1$), the height of ambiguity is 188 m. So a single-pass system needs twice the baseline for the same sensitivity.

**One pixel pair.** Let $s_1 = 2 e^{i \cdot 1.0}$ and $s_2 = 3 e^{i \cdot 0.2}$. Then $s_1 \overline{s_2} = 6 e^{i \cdot 0.8}$: the amplitudes multiply and the phases subtract. The random phase of the scatterers, common to both, cancels.

**Differential InSAR.** Two passes with no baseline but a time gap see only the motion $d$ of the ground along the line of sight: $\varphi = 4\pi d / \lambda$. One fringe is $\lambda / 2 = 2.83$ cm at C band, and phase noise of a few degrees means millimetres. With a nonzero baseline, the topographic phase is removed first with a known height model or with a third image.

**Single-pass topography.** Two antennas on one aircraft or one spacecraft pair record at the same time, so the scene does not change between the images. This is how Zebker and Goldstein (1986) made their airborne topographic maps.

**Persistent scatterers and stacks.** Long series of images use only the pixels that stay coherent, such as buildings and rocks, and fit height and a velocity of motion at each.

## Variations

- **Along-track interferometry.** Two antennas separated along the flight path see moving targets, such as ocean currents, through the phase of their radial velocity.
- **Multi-baseline and multi-frequency InSAR.** Several baselines or wavelengths resolve the turns pixel by pixel, which reduces the need for spatial unwrapping.
- **Phase filtering.** Adaptive filters of the interferogram, before unwrapping, lower the noise and the number of residues.
- **Range spectral filtering.** The two images see slightly different parts of the ground spectrum. Filtering both to the common band raises the coherence.
- **Coherence as a product.** The coherence map itself is used to classify land cover and to detect change.

## Pitfalls

- **Wrong factor p.** Using $4\pi$ for a single-pass system with one transmitter, or $2\pi$ for repeat-pass data, gives heights wrong by a factor of 2.
- **Flat earth phase left in.** Without line L3, the interferogram is covered by dense fringes from the geometry alone, and the unwrapping sees steep slopes and many residues.
- **Low coherence.** As a rule of thumb (a heuristic, not a theorem), the phase is mostly noise below a coherence of a few tenths. Mask those pixels or give them low weights in the unwrapping.
- **Atmosphere.** Water vapour delays the signal differently on the two passes. The result is a phase screen of the size of kilometres that looks like topography or motion.
- **Layover and shadow.** On steep slopes facing the radar, several ground points map to one pixel, and the phase there is meaningless.
- **Registration errors.** A shift of a fraction of a pixel between the images destroys the coherence. Register before forming the interferogram, not after.
- **Unwrapping errors are whole turns.** An error of $2\pi$ in one region gives a height error of $h_{2\pi}$ there. Check the unwrapped phase against control points.

## Exercises

1. Derive $\Delta R \approx B_\perp h / (R \sin\theta)$ for a target at height $h$ seen by two antennas with the perpendicular baseline $B_\perp$, for $B_\perp \ll R$.
2. For the C-band example, what baseline gives a height of ambiguity of 30 m? Why is a very long baseline not better?
3. Show that if $s_1 = a\, e^{i\alpha} n$ and $s_2 = b\, e^{i\beta} n$ with the same complex speckle factor $n$, the phase of $s_1 \overline{s_2}$ is $\alpha - \beta$.
4. Two images with a coherence of 1 are each corrupted by independent complex Gaussian noise of the same power as the signal. What is the coherence of the noisy pair?
5. A single-pass system and a repeat-pass system have the same $\lambda$, $R$, $\theta$ and $B_\perp$. Which one is more sensitive to height, and by what factor?

## References
