---
tag: SH6M7B
kind: algorithm
slug: knox-thompson-method
name: Knox-Thompson method
aliases:
- cross-spectrum method
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Recover object Fourier phases from the average cross spectrum of speckle images at neighboring frequencies, summed along paths."
model: real-ram
complexity:
  vars: {F: the number of frames, N: the number of pixels in a frame}
  time: {worst: Θ(F N log N), average: Θ(F N log N), best: Θ(F N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, iterative: false, linear: false, shift_invariant: false, needs_reference_star_for_modulus: true}
history:
  year: 1974
  people: [Keith T. Knox, Brian J. Thompson]
  note: "Knox and Thompson (1974) showed that the average cross spectrum of short exposures at two close frequencies keeps the difference of the object phases, which the power spectrum of speckle interferometry loses."
prereqs: [speckle-interferometry, cross-correlation, discrete-fourier-transform]
see_also: [speckle-masking, lucky-imaging, phase-retrieval, power-spectral-density, optical-transfer-function, phase-unwrapping, aperture-synthesis]
sources:
  - paper: doi:10.1086/181627
    title: "K. T. Knox and B. J. Thompson, Recovery of images from atmospherically degraded short-exposure photographs, The Astrophysical Journal 193, 1974"
    locator: "pp. L45 to L48 (the cross spectrum of the frames, its transfer function and the recursion for the phase)"
  - paper: doi:10.1364/JOSAA.5.000963
    title: "G. R. Ayers, M. J. Northcott and J. C. Dainty, Knox-Thompson and triple-correlation imaging through atmospheric turbulence, Journal of the Optical Society of America A 5(7), 1988"
    locator: "the article from page 963 (a comparison of the cross spectrum and the bispectrum on simulated and real data)"
  - book: isbn:9781119009450
    title: "Joseph W. Goodman, Statistical Optics, second edition, Wiley, 2015"
    locator: "the chapter on imaging through randomly inhomogeneous media (short exposures, speckle interferometry and the recovery of the phase)"
---

The Knox-Thompson method recovers the Fourier phase of an object from many short exposures taken through atmospheric turbulence. It averages the cross spectrum $I(u)\, \overline{I(u + \Delta)}$ of the frames at two close frequencies, whose phase is the difference of the object phases, and it adds these differences along paths from the origin of the frequency plane. [Speckle interferometry](/speckle-interferometry/) gives only the Fourier modulus of the object. [Speckle masking](/speckle-masking/) gets the phase from the bispectrum, which is free of image motion; the cross spectrum is not, but it is a two-frequency quantity and cheaper to store.

## In plain words

A telescope on the ground sees a star through moving air. A very short exposure freezes the air, and the image breaks into many small bright spots, called speckles. Each spot still holds fine detail, but the pattern changes from frame to frame. Speckle interferometry keeps the strength of each fine detail and loses its position. The Knox-Thompson method keeps the positions too. For each frame it compares every detail with its close neighbor detail. The air changes both in almost the same way, so the comparison, averaged over many frames, shows how the object moves from one detail to the next. Starting from the coarsest detail, the method walks outward and adds up these small steps. With the strengths from speckle interferometry, this gives an image at the full resolution of the telescope.

## The problem

The object $o$ is a real nonnegative image on an $n \times n$ periodic grid, with $N = n^2$ and the [DFT](/discrete-fourier-transform/) $O(u) = |O(u)|\, e^{i\varphi(u)}$ at the signed frequencies $u = (u_1, u_2)$. A short exposure $f$ is $i_f = o \ast s_f$, where $s_f$ is the instantaneous [point spread function](/point-spread-function/): the squared modulus of the Fourier transform of the pupil field $P\, e^{i\psi_f}$, with the pupil $P$ and the random phase screen $\psi_f$ of the air. In the frequency plane,

$$I_f(u) = O(u)\, T_f(u),$$

where $T_f$ is the [optical transfer function](/optical-transfer-function/) of frame $f$, scaled to $T_f(0) = 1$. The transfer function is random and has random phases, so the average $\langle I_f \rangle$ keeps only the low frequencies (the long exposure), and the average power spectrum $\langle |I_f|^2 \rangle = |O|^2 \langle |T|^2 \rangle$ keeps the modulus but not the phase.

The input is $F$ frame spectra and a radius $R$ inside the cutoff of the telescope. The output is an estimate of $\varphi(u)$ for $|u| \le R$. With $|O|$ from speckle interferometry, the inverse DFT of $|O|\, e^{i\varphi}$ is the image.

## The algorithm

For an offset $\Delta$, the average cross spectrum factors as

$$C(u, \Delta) = \big\langle I_f(u)\, \overline{I_f(u + \Delta)} \big\rangle = O(u)\, \overline{O(u + \Delta)}\; H(u, \Delta), \qquad H(u, \Delta) = \big\langle T_f(u)\, \overline{T_f(u + \Delta)} \big\rangle .$$

If the screen statistics do not change when $\psi$ is replaced by $-\psi$, as for a Gaussian screen, then $H$ is real. Where $H > 0$, the phase of $C$ is $\varphi(u) - \varphi(u + \Delta)$. The method uses the two unit offsets $e_1 = (1, 0)$ and $e_2 = (0, 1)$, sets $\varphi(0) = 0$ because $O(0)$ is the total flux, and walks outward in the order of $|u_1| + |u_2|$.

```pseudo id=main
KNOX-THOMPSON(I_1, ..., I_F, R)
L1  C_e(u) ← (1/F) Σ_f I_f(u) · conj(I_f(u + e)) for e ∈ {e1, e2} and every u
L2  φ(0) ← 0
L3  for each u ≠ 0 with |u| ≤ R, in the order of |u1| + |u2| do
L4      z ← 0
L5      for each known neighbor p = u ∓ e with |p1| + |p2| = |u1| + |u2| - 1 do
L6          z ← z + e^{iφ(p)} · conj(C_e(p)) if u = p + e, or e^{iφ(p)} · C_e(u) if u = p - e
L7      φ(u) ← arg z
L8  return φ

RECONSTRUCT(M, φ, R)                      ▷ M is the modulus from speckle interferometry
L9  return Re IDFT(M(u) e^{iφ(u)} for |u| ≤ R, 0 elsewhere)
```

Line L6 adds a phasor and not an angle, so there is no wrapping of phases, and a neighbor with a larger $|C_e|$ has more weight. A frequency off the axes has two neighbors closer to the origin, and line L7 combines both paths. The modulus $M$ comes from the same frames: $M^2 = \langle |I_f|^2 \rangle / \langle |T|^2 \rangle$, where $\langle |T|^2 \rangle$ is the power spectrum of frames of a point source, the reference star.

## Example

Take $n = 16$, a disk pupil of diameter $d = 6$ cells, and an object of three points: flux 1 at the offset $(0, 0)$, 0.6 at $(2, 1)$ and 0.35 at $(-1, 3)$. Each phase screen is filtered white noise with the power spectrum $|f|^{-11/3}$ of Kolmogorov turbulence and an expected rms phase of 3 radians, from `random.Random(seed)`. The transfer function of a frame is zero at $|u_1| \ge 6$ or $|u_2| \ge 6$.

Along the $u_1$ axis, the transfer function without turbulence is 1, 0.8125, 0.625, 0.4375, 0.25 and 0.125 at $u_1 = 0, \dots, 5$. The long exposure keeps $|\langle T \rangle| = 0.281$ at $u_1 = 1$ and 0.030 at $u_1 = 2$, so it loses everything beyond the first ring. The speckle transfer function $\langle |T|^2 \rangle$ is 1, 0.155, 0.040, 0.020, 0.011 and 0.005, and $H(u, e_1)$ is 0.300, 0.044, 0.017, 0.009 and 0.004 at $u_1 = 0, \dots, 4$: small, but positive up to the cutoff.

The method recovers the 49 phases with $|u| \le 4$. The table gives the largest and the rms phase error, in radians, with independent screens (seed 1) and with antithetic pairs, where each screen $\psi$ is also used as $-\psi$.

| frames | largest error | rms error |
|---|---|---|
| 1 | 2.903 | 1.495 |
| 10 | 0.466 | 0.223 |
| 30 | 1.210 | 0.677 |
| 100 | 0.788 | 0.402 |
| 300 | 0.197 | 0.101 |
| 1 antithetic pair | 3.142 | 2.105 |
| 50 antithetic pairs | 0 to rounding | 0 to rounding |

One frame gives no useful phase. The error falls with the number of frames, but not at every step, because a few unlucky frames can dominate a small sample. An antithetic pair makes every averaged $H$ exactly real, so each phase is exact or off by $\pi$; with one pair $H$ is negative at some frequencies, and with 50 pairs it is positive at all 49 and the phases are exact. With the modulus from 50 antithetic pairs of a reference star (seed 2), the image differs from the object, cut to $|u| \le 4$, by at most 0.0075, against its peak of 0.193, and the brightest pixel is at the true position.

## Correctness

The factorization of $C$ is the linearity of the average, because $O$ does not change from frame to frame. If the law of $\psi$ is the same as the law of $-\psi$, then $T$ and $\overline{T}$ have the same law, because the PSF of $-\psi$ is the PSF of $\psi$ turned by 180 degrees. So $H(u, \Delta)$ equals its own conjugate and is real. Where $H > 0$ along every step that line L6 uses, each term added to $z$ is $e^{i\varphi(u)}$ times a positive number, by induction on $|u_1| + |u_2|$, so line L7 returns $\varphi(u)$ exactly. The sample average converges to the expected value as $F \to \infty$ by the [law of large numbers](/law-of-large-numbers/), so the computed phases converge to $\varphi$ wherever the expected $H$ is positive. That $H > 0$ for unit offsets is an assumption about the turbulence: it holds when the offset is small against the size of a seeing cell in the frequency plane, and it held at every frequency of the example. The full proof is below.

## Complexity

Each frame needs one FFT, $\Theta(N \log N)$, and two products per frequency, $\Theta(N)$, so $F$ frames cost $\Theta(F N \log N)$. The recursion visits each frequency once with at most four neighbors, $\Theta(N)$. The extra space is $\Theta(N)$ for the two cross spectra and the power spectrum, which are accumulated frame by frame. The real cost is the number of frames: the noise of $C$ falls as $1/\sqrt F$, and $H$ is small at high frequencies, so thousands of frames are usual.

## Properties

- **It keeps the position of the object.** $\varphi(e_1)$ and $\varphi(e_2)$ come from the data, so the image is placed where the object is, in the average over the frames.
- **It is not invariant to frame motion.** A shift $t$ of frame $f$ multiplies its term in $C$ by $e^{2\pi i\, \Delta \cdot t / n}$. Random motion lowers $|H|$, and only its symmetry keeps $H$ real.
- **It needs only two frequencies at a time.** The stored cross spectra have $2N$ values, against the much larger bispectrum of speckle masking.
- **Errors add along paths.** A wrong step at one frequency goes into every frequency after it on the path, so the error grows with $|u|$.
- **Phase only.** The method gives no modulus; the modulus comes from speckle interferometry and a reference star.

## Variants and improvements

- **More offsets and least squares.** Use more offsets $\Delta$ and solve for all phases at once by least squares on the phase differences, in the same way as least squares [phase unwrapping](/phase-unwrapping/). This spreads the error over many paths.
- **Speckle masking.** The bispectrum $\langle I(u)\, I(v)\, \overline{I(u + v)} \rangle$ is free of frame motion. See [speckle masking](/speckle-masking/). Ayers, Northcott and Dainty (1988) compare the two methods.
- **Frame selection.** Keep the best frames first, as in [lucky imaging](/lucky-imaging/), then apply the method to them.

## When to use it

Use the Knox-Thompson method on short exposures of a bright object through turbulence, when a diffraction-limited image is needed and there is no adaptive optics. It needs many frames, each shorter than the time in which the air changes, and a reference star for the modulus. For faint objects, or when frame motion is large, speckle masking is more robust. For bright and compact objects, lucky imaging is simpler.

## Pitfalls

- **Too large an offset.** $H(u, \Delta)$ falls fast when $\Delta$ is larger than a seeing cell in the frequency plane. Use unit offsets on a grid that samples the cutoff well.
- **Too few frames.** The phases at high frequencies have a small $|H|$, and their noise needs many frames to average down.
- **Adding angles instead of phasors.** Sums of angles wrap at $\pm\pi$, and the mean of two angles near $\pm\pi$ is wrong; line L6 adds phasors to avoid this.
- **A changed atmosphere for the reference star.** The modulus uses $\langle |T|^2 \rangle$ from another star at another time. If the seeing changed, the modulus is wrong, while the phase is not affected.
- **Photon noise.** In photon-counting data the power spectrum has a bias from the photon count, and it must be removed before the modulus is formed.

## Implementations

## History

Labeyrie (1970) showed that the average power spectrum of short exposures keeps the diffraction-limited modulus of the object, but not its phase. Knox and Thompson (1974) found that the cross spectrum at two close frequencies keeps the phase differences, and that a recursion gives the phase. Weigelt (1977) introduced speckle masking with triple correlations, and Lohmann, Weigelt and Wirnitzer (1983) wrote it with the bispectrum. Ayers, Northcott and Dainty (1988) compared the two phase methods.

## References
