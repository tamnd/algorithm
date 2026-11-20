---
tag: 3Z17AM
kind: concept
slug: range-cell-migration
name: Range cell migration
aliases:
- range migration
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "The change of range to a target over the synthetic aperture, which spreads its echo over several range cells and must be corrected before azimuth focusing."
prereqs: [synthetic-aperture-radar]
see_also: [range-doppler-algorithm, chirp-scaling-algorithm, omega-k-algorithm, sar-backprojection, sar-image-formation, stolt-migration, sinc-interpolation, linear-frequency-modulation-pulse]
sources:
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapter 5, SAR Signal Properties (the range equation and the migration in the range-Doppler domain), and Chapter 6, The Range Doppler Algorithm (its correction)"
  - paper: doi:10.1109/MGRS.2013.2248301
    title: "Alberto Moreira, Pau Prats-Iraola, Marwan Younis, Gerhard Krieger, Irena Hajnsek and Konstantinos P. Papathanassiou, A tutorial on synthetic aperture radar, IEEE Geoscience and Remote Sensing Magazine 1(1), 2013, 6 to 43"
    locator: "the part on SAR focusing and range cell migration (general locator)"
---

Range cell migration (RCM) is the change of the range from a [synthetic aperture radar](/synthetic-aperture-radar/) to a point target while the target is in the beam, measured in range cells. The range of a target is smallest when the radar passes it and grows on both sides along a hyperbola, so after range compression its echo does not stay in one range cell: it follows a curve through several cells. Azimuth focusing sums the echo along the track, so it must follow that curve. Range cell migration correction (RCMC) straightens the curves before the sum, or a focusing method takes them into account directly. The alias "range migration" names this effect; the "range migration algorithm" is a different thing, another name of the [omega-k algorithm](/omega-k-algorithm/).

## In plain words

As a plane flies past a house, the distance to the house first gets shorter, then longer again. The radar sorts its echoes by distance into narrow bins. If the distance changes by more than one bin while the house is in view, its echo slides from bin to bin over the recordings. To add up the echo of the house you must follow that slide. If you only add up one bin, you miss most of the echo and the house looks dim and smeared. Correcting the slide means moving each piece of the echo back into the bin of the shortest distance.

## The idea

**The range history.** For a straight track at the speed $V$ and a target at the closest range $R_0$ passed at the slow time $\eta = 0$,

$$R(\eta) = \sqrt{R_0^2 + V^2 \eta^2} = R_0 + \frac{V^2 \eta^2}{2 R_0} + O\!\left(\frac{V^4 \eta^4}{R_0^3}\right).$$

The migration is $R(\eta) - R_0$. At the edge of a beam with the half angle $\theta$, it is $R_0 (1/\cos\theta - 1)$. When the beam is squinted, the curve also has a linear part, the range walk, on top of the quadratic part, the range curvature. In units of the range cell $c/(2 f_s)$, a migration of less than a fraction of a cell can be ignored. The size of that fraction is a matter of image quality, not a theorem.

**In the range-Doppler domain.** Take the DFT along the track of the range-compressed data. The azimuth phase of the target is $-4\pi R(\eta)/\lambda$, and the principle of stationary phase links each Doppler frequency $f_\eta$ to the slow time where the instantaneous frequency $-(2/\lambda)\, dR/d\eta$ equals $f_\eta$. At that time,

$$R_{rd}(f_\eta) = \frac{R_0}{D(f_\eta)}, \qquad D(f_\eta) = \sqrt{1 - \left(\frac{\lambda f_\eta}{2V}\right)^2},$$

and $R_{rd} - R_0 \approx \lambda^2 R_0 f_\eta^2 / (8 V^2)$ for small $f_\eta$. Two facts make this domain useful. First, the curve does not depend on the along-track position of the target, only on $R_0$, so all targets at one range share one curve and are corrected together. Second, the curve depends on $R_0$, so the shift at a given Doppler frequency changes along the range axis. That is why RCMC is a range-varying shift. The [range-Doppler algorithm](/range-doppler-algorithm/) applies it by [sinc interpolation](/sinc-interpolation/) along each Doppler line. The [chirp scaling algorithm](/chirp-scaling-algorithm/) makes it a range-invariant shift by scaling the range chirp before the range FFT, so a phase multiply can do it. The [omega-k algorithm](/omega-k-algorithm/) removes it with a change of variables in the 2D frequency domain. [Backprojection](/sar-backprojection/) reads each pulse at the exact range of each pixel, so the migration needs no special step.

**The coupling of range and azimuth.** Migration also bends the range chirp. In the range-Doppler domain the range FM rate changes from $K_r$ to

$$K_m = \frac{K_r}{1 - K_r \dfrac{c R_0 f_\eta^2}{2 V^2 f_0^3 D^3}},$$

so a range matched filter designed for $K_r$ alone defocuses at large Doppler frequencies. Secondary range compression (SRC) applies the change; the chirp scaling algorithm uses $K_m$ in its scaling function.

## Examples

**A narrow beam.** With $\lambda = 1$ m, a half beam angle whose sine is 0.125 and $R_0 = 400$ m, the migration at the edge of the beam is $400\,(1/\sqrt{1 - 0.125^2} - 1) = 3.16$ m, that is 2.5 range cells of 1.25 m. On these data, the range-Doppler algorithm gives a peak of 0.90 of the brute-force matched filter with RCMC and 0.47 without it; these are measurements on that simulation.

**A wide beam at short range.** With a half beam angle whose sine is 0.35, the migration at the edge of the beam is $96\,(1/\sqrt{1 - 0.35^2} - 1) = 6.48$ m at $R_0 = 96$ m and 8.10 m at $R_0 = 120$ m. The difference, 1.62 m, is more than one cell, so a correction that is right at 120 m is wrong at 96 m. In the chirp scaling tests, the bulk shift of 120 m alone leaves a peak of 0.73 of the ideal value at 96 m and moves it by one cell, and the full chirp scaling gives 1.05 at the right cell (measurements).

**A satellite.** For a C-band radar ($\lambda = 5.6$ cm) with a 10 m antenna, the half beam angle is about $\lambda/(2L) = 0.0028$ rad, and at $R_0 = 850$ km the migration at the edge of the beam is about $850000 \cdot 0.0028^2 / 2 \approx 3.3$ m. That is several range cells for a fine range resolution, so spaceborne processors correct it.

## Where it is used

- **Stripmap focusing.** The [range-Doppler algorithm](/range-doppler-algorithm/), the [chirp scaling algorithm](/chirp-scaling-algorithm/) and the [omega-k algorithm](/omega-k-algorithm/) differ mainly in how they correct it.
- **Spotlight focusing.** In the [polar format algorithm](/polar-format-algorithm/), the polar to Cartesian interpolation also removes the migration of the targets near the scene center.
- **Time domain.** [Backprojection](/sar-backprojection/) and [fast factorized backprojection](/fast-factorized-backprojection/) follow the exact range of each pixel.
- **Seismic imaging.** The diffraction hyperbola of a point in a zero-offset section is the same curve, and [Stolt migration](/stolt-migration/) and [Kirchhoff migration](/kirchhoff-migration/) collapse it.
- **The image formation problem.** [SAR image formation](/sar-image-formation/) states the full model in which the migration appears.

## References
