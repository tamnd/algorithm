---
tag: NXPR8R
kind: technique
slug: speckle-interferometry
name: Speckle interferometry
aliases:
- Labeyrie speckle interferometry
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: Recover the diffraction limited power spectrum of a star field by averaging the power spectra of many short exposures through turbulence.
history:
  year: 1970
  people: [Antoine Labeyrie]
  note: "Labeyrie (1970) showed that the average power spectrum of short exposures of a star keeps information up to the diffraction limit of the telescope, which a long exposure loses."
prereqs: [speckle, power-spectral-density, optical-transfer-function]
see_also: [knox-thompson-method, speckle-masking, lucky-imaging, autocorrelation, cross-correlation, wiener-khinchin-theorem, phase-retrieval, van-cittert-zernike-theorem]
sources:
  - paper: "A. Labeyrie, Attainment of diffraction limited resolution in large telescopes by Fourier analysing speckle patterns in star images, Astronomy and Astrophysics 6, 1970"
    locator: "pp. 85 to 87 (the average power spectrum of short exposures and its use to measure objects at the diffraction limit)"
  - paper: doi:10.1364/JOSA.63.000971
    title: "D. Korff, Analysis of a method for obtaining near-diffraction-limited information in the presence of atmospheric turbulence, Journal of the Optical Society of America 63, 1973"
    locator: "the article from page 971 (the speckle transfer function for Kolmogorov turbulence)"
  - paper: doi:10.1364/JOSA.56.001372
    title: "D. L. Fried, Optical resolution through a randomly inhomogeneous medium for very long and very short exposures, Journal of the Optical Society of America 56, 1966"
    locator: "the article from page 1372 (the coherence length r0 and the transfer functions of long and short exposures)"
  - book: isbn:9780974707792
    title: "Joseph W. Goodman, Speckle Phenomena in Optics, Theory and Applications, Roberts and Company, 2007"
    locator: "the chapter on speckle in imaging through the atmosphere (speckle interferometry and the speckle transfer function)"
---

Speckle interferometry measures the Fourier modulus of an astronomical object at the full resolution of a telescope, through atmospheric turbulence that blurs a long exposure to a much larger size. It takes many short exposures, each of which freezes the air into a pattern of [speckle](/speckle/), and averages the squared modulus of their Fourier transforms, their [power spectrum](/power-spectral-density/). Dividing by the same average for a point star gives $|O(u)|^2$, the power spectrum of the object, or by the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) its [autocorrelation](/autocorrelation/). The phase is lost; the [Knox-Thompson method](/knox-thompson-method/) and [speckle masking](/speckle-masking/) recover it from the same frames, and [lucky imaging](/lucky-imaging/) gets an image by keeping only the best frames.

## In plain words

Through moving air, a long photograph of a star is a soft blob many times larger than the telescope can resolve. A very short exposure looks different: the blob breaks into many tiny bright grains. Each grain is as small as the telescope's finest detail, but the grains move every few milliseconds. For a double star, every grain comes twice, once from each star, at the same small offset. A simple average of the frames washes this out. Speckle interferometry instead measures, for each frame, how strongly each fine stripe pattern is present, without asking where it is. These strengths survive averaging. Comparing them with the same measurement on a single star removes the effect of the air. The result tells the separation and brightness ratio of a double star, or the size of a star, but not which star is on which side.

## When it applies

**Notation.** The object $o$ and the frames are images on an $n \times n$ grid, with the DFT $O(u)$ and $I_f(u)$ at the signed frequencies $u$. A short exposure is $i_f = o * s_f$, where the instantaneous PSF $s_f$ is the squared modulus of the Fourier transform of the pupil field $P\, e^{i\psi_f}$, so $I_f(u) = O(u)\, T_f(u)$ with the random [optical transfer function](/optical-transfer-function/) $T_f$, $T_f(0) = 1$. The telescope has diameter $D$, and $r_0$ is the Fried coherence length of the air.

The method rests on one identity. Since $O$ is the same in every frame,

$$\big\langle |I_f(u)|^2 \big\rangle = |O(u)|^2\, \big\langle |T_f(u)|^2 \big\rangle .$$

The long exposure has the transfer function $\langle T_f(u) \rangle$, which falls to almost zero beyond spatial frequencies of about $r_0/\lambda$. The speckle transfer function $\langle |T_f(u)|^2 \rangle$ is small but not zero up to the diffraction cutoff $D/\lambda$ (Korff, 1973). So the power spectrum of short exposures keeps the object's modulus up to the diffraction limit, while the long exposure keeps it only to the seeing limit.

Use it when these conditions hold:

- **Short exposures.** Each exposure is shorter than the time the air needs to change, typically milliseconds, so that $s_f$ is one frozen pattern.
- **A small object.** The whole object lies in one isoplanatic patch, so every point of it sees the same $s_f$.
- **A narrow band.** The speckle pattern scales with the wavelength, so a wide filter smears the grains at large distances from the center.
- **A reference.** A point star near the object in the sky and in time gives $\langle |T|^2 \rangle$ under the same seeing.
- **Enough light and frames.** $\langle |T|^2 \rangle$ is small at high frequencies, so many frames are needed to average the noise down there.

## The template

```pseudo id=main
SPECKLE-INTERFEROMETRY(object frames i_1..i_F, reference frames r_1..r_G)
L1  P ← 0, R ← 0
L2  for each object frame i_f do P ← P + |DFT(i_f)|^2 / F
L3  for each reference frame r_g do R ← R + |DFT(r_g)|^2 / G
L4  subtract the noise bias from P and R                       ▷ hole: the bias of photon counting or read noise
L5  Q(u) ← P(u) / R(u) where R(u) is large enough, else 0       ▷ hole: the cut or a Wiener-type division
L6  A ← IDFT(Q)                                                ▷ the autocorrelation of the object
L7  fit a model to Q or to A                                   ▷ hole: a binary, a disk, or the input of a phase method
L8  return Q, A and the fitted model
```

Line L2 gives the identity above with a finite average, and lines L3 and L5 divide out $\langle |T|^2 \rangle$. The holes are the noise bias (L4), the cut at frequencies where $R$ is noise (L5) and the model (L7). For a binary star with fluxes 1 and $F$ at separation $s$, $|O(u)|^2 = 1 + F^2 + 2F \cos(2\pi\, u \cdot s / n)$: the power spectrum has straight fringes, whose period and direction give $s$ up to its sign, and whose depth gives $F$. The autocorrelation has a peak $1 + F^2$ at 0 and two peaks $F$ at $\pm s$; this is the [cross-correlation](/cross-correlation/) of the object with itself.

## Classic examples

**A binary star in simulation.** A grid of $64 \times 64$ cells holds a disk pupil of diameter 16 cells, so the diffraction limit $\lambda/D$ is 4 pixels and the transfer function is zero beyond 16 cells from the origin. Phase screens are filtered white noise with the Kolmogorov phase spectrum $0.023\, r_0^{-5/3} f^{-11/3}$ and $D/r_0 = 6$, on a periodic grid, so they have no scales larger than the grid. The binary has fluxes 1 at $(0, 0)$ and 0.5 at $(6, 2)$, a separation of 6.3 pixels. There are 300 object frames (seed 1) and 300 reference frames of a point star (seed 2). The long exposure of the point star is 17 pixels wide at half maximum along a row. Along the $u_1$ axis the two transfer functions of the reference are:

| $u_1$ | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---|---|---|---|---|---|---|---|
| long exposure $\lvert \langle T \rangle \rvert$ | 1 | 0.228 | 0.028 | 0.0066 | 0.0049 | 0.0036 | 0.0033 | 0.0018 |
| speckle $\langle \lvert T \rvert^2 \rangle$ | 1 | 0.112 | 0.025 | 0.013 | 0.0081 | 0.0053 | 0.0026 | 0.00075 |

The long exposure is near zero beyond $u_1 = 4$, where the fringes of the binary are. The estimate $Q = P/R$ on the 657 frequencies with $|u| \le 14.4$ has a mean absolute error of 0.071 and a largest error of 0.47 against the true $|O|^2$, which runs from 0.25 to 2.25. At $u = (8, 0)$ it gives 1.323 against 1.25, while the long exposure gives $|O|^2\, |\langle T \rangle|^2 \approx 3 \times 10^{-5}$. The inverse DFT of $Q$ has local maxima 0.2081 at $(0, 0)$ and 0.0877 at $(6, 2)$ and at $(-6, -2)$; the same computation with the true $|O|^2$ gives 0.2089 and 0.0888. The ratio of the peaks is 0.4215, against 0.4251 for the true band-limited spectrum and $F/(1 + F^2) = 0.4$ without the cut. The separation is found exactly, but the method cannot say whether the fainter star is at $(6, 2)$ or at $(-6, -2)$.

**Binary stars.** Separations and brightness ratios of close binaries, below the seeing limit, are a main use of the method. The orbits give stellar masses.

**Diameters of stars.** For a star that is a uniform disk, $|O|$ is the Airy pattern $|2 J_1(x)/x|$ in the scaled frequency $x$, and its first zero gives the diameter.

## Variations

- **Recovering the phase.** The [Knox-Thompson method](/knox-thompson-method/) uses the cross spectrum $\langle I(u)\, \overline{I(u + \Delta)} \rangle$, and [speckle masking](/speckle-masking/) uses the bispectrum. Both work on the same frames and give a true image, not only its autocorrelation.
- **Fitting instead of inverting.** For a binary, fit the three parameters directly to $Q$, which avoids the division at frequencies where $R$ is small.
- **Speckle holography.** If a point star lies in the same isoplanatic patch as the object, the cross terms between the star and the object in the autocorrelation give an image of the object.
- **Shift-and-add and lucky imaging.** Registering each frame on its brightest grain and adding gives an image with a diffraction-limited core; keeping only the best frames is [lucky imaging](/lucky-imaging/).
- **Phase retrieval.** Since $Q$ is a Fourier modulus, [phase retrieval](/phase-retrieval/) with a positivity and support constraint can in principle give the image, with the ambiguities of that problem.

## Pitfalls

- **A changed seeing between object and reference.** $\langle |T|^2 \rangle$ depends strongly on $r_0$ at high frequencies. If the seeing changed, $Q$ is wrong by a smooth factor, which biases the brightness ratio and the size of a star.
- **Dividing by noise.** Near the cutoff, $R$ is tiny, and $P/R$ is mostly noise. Cut the frequencies or use a Wiener-type division.
- **The noise bias.** In photon-counting data, $\langle |I|^2 \rangle$ has an added constant from the photon count. Subtract it before the division.
- **The 180 degree ambiguity.** The autocorrelation is symmetric, so the position angle of a binary is known only up to 180 degrees. A phase method or a long exposure must decide it.
- **Exposures too long or band too wide.** Both lower the contrast of the speckle and the value of $\langle |T|^2 \rangle$ at high frequencies, and the method loses its gain.
- **An object larger than the isoplanatic patch.** Different parts of the object see different speckle patterns, and the identity no longer holds.

## Exercises

1. Prove $\langle |I_f|^2 \rangle = |O|^2 \langle |T_f|^2 \rangle$ and show that $\langle |T_f(u)|^2 \rangle \ge |\langle T_f(u) \rangle|^2$. When is it equal?
2. Compute $|O(u)|^2$ for a binary with fluxes 1 and $F$ at offset $s$, and its inverse DFT. Show that the peak ratio is $F/(1 + F^2)$, and that $F$ and $1/F$ give the same ratio, so the ratio fixes $F$ once $F \le 1$ is chosen.
3. Show that the objects $o(x)$ and $o(-x)$ have the same power spectrum. What does this mean for a triple star?
4. For a uniform disk of angular diameter $\theta$, find the frequency of the first zero of $|O|$ in terms of $\theta$ and $\lambda$.
5. Reproduce the binary simulation with $D/r_0 = 3$ and with $D/r_0 = 10$, and compare the errors of $Q$ at $u_1 = 12$.

## References
