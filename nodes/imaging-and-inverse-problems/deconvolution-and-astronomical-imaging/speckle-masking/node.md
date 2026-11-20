---
tag: A53FCA
kind: algorithm
slug: speckle-masking
name: Speckle masking
aliases:
- bispectrum imaging
- triple correlation imaging
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Recover the Fourier phase of an object from short exposure speckle images by averaging their bispectrum, whose phase is free of turbulence."
model: real-ram
complexity:
  vars: {F: the number of frames, N: the number of pixels in a frame, V: the number of offsets v kept in the bispectrum}
  time: {worst: Θ(F N (log N + V)), average: Θ(F N (log N + V)), best: Θ(F N (log N + V))}
  space: {extra: Θ(V N)}
properties: {deterministic: true, iterative: false, linear: false, shift_invariant: true, needs_reference_star_for_modulus: true}
history:
  year: 1977
  people: [Gerd Weigelt]
  note: "Weigelt (1977) proposed speckle masking with triple correlations of short exposures; Lohmann, Weigelt and Wirnitzer (1983) gave the theory in terms of the bispectrum."
prereqs: [speckle-interferometry, discrete-fourier-transform]
see_also: [knox-thompson-method, lucky-imaging, phase-retrieval, power-spectral-density, cross-correlation, optical-transfer-function, aperture-synthesis]
sources:
  - paper: doi:10.1016/0030-4018(77)90077-3
    title: "G. P. Weigelt, Modified astronomical speckle interferometry 'speckle masking', Optics Communications 21(1), 1977"
    locator: "pp. 55 to 59 (the triple correlation of the frames and the reconstruction of the object)"
  - paper: doi:10.1364/AO.22.004028
    title: "A. W. Lohmann, G. Weigelt and B. Wirnitzer, Speckle masking in astronomy, triple correlation theory and applications, Applied Optics 22(24), 1983"
    locator: "pp. 4028 to 4037 (the bispectrum, the speckle masking transfer function and the recursion for the phase)"
  - paper: doi:10.1364/AO.23.003121
    title: "H. Bartelt, A. W. Lohmann and B. Wirnitzer, Phase and amplitude recovery from bispectra, Applied Optics 23(18), 1984"
    locator: "the article from page 3121 (recursive recovery of the Fourier phase from the bispectrum)"
  - paper: doi:10.1364/JOSAA.5.000963
    title: "G. R. Ayers, M. J. Northcott and J. C. Dainty, Knox-Thompson and triple-correlation imaging through atmospheric turbulence, Journal of the Optical Society of America A 5(7), 1988"
    locator: "the article from page 963 (a comparison of the bispectrum and the cross spectrum on simulated and real data)"
---

Speckle masking recovers the Fourier phase of an object from many short exposures taken through atmospheric turbulence. It averages the bispectrum $I(u)\, I(v)\, \overline{I(u + v)}$ of the frames, whose phase is the closure phase $\varphi(u) + \varphi(v) - \varphi(u + v)$ of the object, and it recovers $\varphi$ by a recursion over the frequency plane. [Speckle interferometry](/speckle-interferometry/) gives only the Fourier modulus. The [Knox-Thompson method](/knox-thompson-method/) gets the phase from a cross spectrum, which image motion disturbs; the bispectrum does not change when a frame moves, but in return it loses the position of the object.

## In plain words

A short exposure through moving air breaks the image of a star into many small spots, called speckles. Each frame still holds the fine detail, but the air mixes up where it is. Speckle masking takes three details at a time, chosen so that the third one is the sum of the first two. The air changes the three positions in a way that cancels in a fixed combination, and so does any motion of the whole frame. Averaged over many frames, this combination gives a sum of three object positions that the air does not hide. From these sums the method builds the position of each detail, step by step, out from the coarsest one. Only one thing stays unknown: where the whole object is in the frame. With the strengths of the details from speckle interferometry, this gives an image at the full resolution of the telescope.

## The problem

The object $o$ is a real nonnegative image on an $n \times n$ periodic grid, with $N = n^2$ and the [DFT](/discrete-fourier-transform/) $O(u) = |O(u)|\, e^{i\varphi(u)}$ at the signed frequencies $u = (u_1, u_2)$. A short exposure is $i_f = o \ast s_f$, where the instantaneous PSF $s_f$ is the squared modulus of the Fourier transform of the pupil field $P\, e^{i\psi_f}$ for a random phase screen $\psi_f$. In the frequency plane $I_f(u) = O(u)\, T_f(u)$, with the random [optical transfer function](/optical-transfer-function/) $T_f$ and $T_f(0) = 1$.

The input is $F$ frame spectra, a set of offsets $v$ and a radius $R$ inside the cutoff of the telescope. The output is an estimate of $\varphi(u)$ for $|u| \le R$, up to a term $a \cdot u$ that is linear in $u$. With $|O|$ from speckle interferometry, the inverse DFT of $|O|\, e^{i\varphi}$ is the image, up to a shift.

## The algorithm

The average bispectrum factors as

$$B(u, v) = \big\langle I_f(u)\, I_f(v)\, \overline{I_f(u + v)} \big\rangle = O(u)\, O(v)\, \overline{O(u + v)}\; S(u, v), \qquad S(u, v) = \big\langle T_f(u)\, T_f(v)\, \overline{T_f(u + v)} \big\rangle .$$

If the screen statistics do not change when $\psi$ is replaced by $-\psi$, the speckle masking transfer function $S$ is real. Where $S > 0$, the phase of $B$ is the closure phase $\beta(u, v) = \varphi(u) + \varphi(v) - \varphi(u + v)$, and so

$$\varphi(u + v) = \varphi(u) + \varphi(v) - \beta(u, v).$$

A shift $t$ of a frame multiplies $I_f(u)$ by $e^{-2\pi i\, u \cdot t/n}$, and the three factors cancel in $B$. The same cancellation means that $\varphi$ and $\varphi + 2\pi\, a \cdot u$ have the same closure phases for every vector $a$, so $\varphi(e_1)$ and $\varphi(e_2)$ are free. The recursion sets them to given values, by default 0, and walks outward with the two offsets $v \in \{e_1, e_2\}$.

```pseudo id=main
SPECKLE-MASKING(I_1, ..., I_F, R, τ1, τ2)     ▷ τ1, τ2 fix the free linear term
L1  B_e(u) ← (1/F) Σ_f I_f(u) · I_f(e) · conj(I_f(u + e)) for e ∈ {e1, e2} and every u
L2  φ(0) ← 0, φ(e1) ← τ1, φ(e2) ← τ2
L3  for each other u with |u| ≤ R, in the order of |u1| + |u2| do
L4      z ← 0
L5      for each known neighbor p = u ∓ e with |p1| + |p2| = |u1| + |u2| - 1 do
L6          z ← z + e^{i(φ(p) + φ(e))} · conj(B_e(p)) if u = p + e, or e^{i(φ(p) - φ(e))} · B_e(u) if u = p - e
L7      φ(u) ← arg z
L8  return φ

RECONSTRUCT(M, φ, R)                          ▷ M is the modulus from speckle interferometry
L9  return Re IDFT(M(u) e^{iφ(u)} for |u| ≤ R, 0 elsewhere)
```

The full bispectrum of an $n \times n$ image has a value for every pair $(u, v)$, which is $N^2$ values. The recursion needs only small offsets $v$, so implementations keep a few planes of $v$ near the origin; this page keeps the two unit offsets, which is $2N$ values. Line L6 adds phasors weighted by $|B|$, so there is no wrapping of angles, and a frequency off the axes combines two paths.

## Example

The setup is the same as on the Knox-Thompson page: $n = 16$, a disk pupil of diameter 6 cells, phase screens with the Kolmogorov power spectrum $|f|^{-11/3}$ and an expected rms phase of 3 radians, and an object of three points with flux 1 at $(0, 0)$, 0.6 at $(2, 1)$ and 0.35 at $(-1, 3)$. The object has $\varphi(e_1) = -0.1646$ and $\varphi(e_2) = -0.3165$, which the bispectrum cannot see. Along the $u_1$ axis, the transfer function $S(u, e_1)$, measured on a point source with 50 antithetic pairs of screens (seed 2), is 0.155, 0.0269, 0.0094, 0.0042 and 0.0021 at $u_1 = 0, \dots, 4$. At $u = 0$ it is $\langle |T(e_1)|^2 \rangle$, the value that speckle interferometry uses.

The method recovers the 49 phases with $|u| \le 4$. The table gives the phase error in radians after the free linear term is removed, with independent screens (seed 1). The last column is the rms error of the Knox-Thompson method on the same frames.

| frames | largest error | rms error | rms error of Knox-Thompson |
|---|---|---|---|
| 1 | 3.048 | 1.860 | 1.495 |
| 10 | 0.621 | 0.190 | 0.223 |
| 30 | 0.203 | 0.105 | 0.677 |
| 100 | 0.112 | 0.051 | 0.402 |
| 300 | 0.052 | 0.028 | 0.101 |

With 50 antithetic pairs, where each screen $\psi$ is also used as $-\psi$, the averaged $S$ is exactly real and positive at all 49 frequencies, and the phases are exact to rounding. They stay exact when every frame is moved by a random shift of up to 2 pixels in each direction, because the bispectrum does not change. With one antithetic pair, $S$ is negative at some frequencies and the largest error is $\pi$. With the modulus from 50 antithetic pairs of a reference star (seed 2), the image differs from the object, cut to $|u| \le 4$ and moved by the free linear term, by at most 0.0075, against its peak of 0.193.

## Correctness

The factorization of $B$ holds because $O$ is the same in every frame. If the law of $\psi$ equals the law of $-\psi$, then $T$ and $\overline T$ have the same law, because the PSF of $-\psi$ is the PSF of $\psi$ turned by 180 degrees; so $S(u, v)$ equals its own conjugate and is real. A frame shift multiplies the three factors by $e^{-2\pi i\, u \cdot t/n}$, $e^{-2\pi i\, v \cdot t/n}$ and $e^{2\pi i\, (u + v) \cdot t/n}$, whose product is 1. Where $S > 0$ on every step of the recursion, each term of line L6 is $e^{i\varphi'(u)}$ times a positive number, where $\varphi'$ is the object phase with the linear term set by $\tau_1, \tau_2$; by induction on $|u_1| + |u_2|$, line L7 returns $\varphi'(u)$. As $F \to \infty$, the sample bispectrum converges to $B$ by the law of large numbers, so the returned phases converge to $\varphi'$. That $S > 0$ on the steps is an assumption about the turbulence; it held at every frequency of the example. The full proof is below.

## Complexity

Each frame needs one FFT, $\Theta(N \log N)$, and one triple product per frequency and offset, $\Theta(V N)$, so $F$ frames cost $\Theta(F N (\log N + V))$. The recursion is $\Theta(V N)$. The extra space is $\Theta(V N)$ for the kept planes of the bispectrum; the full bispectrum would need $\Theta(N^2)$. As for every speckle method, the real cost is the number of frames.

## Properties

- **Free of image motion.** A shift of a frame does not change its bispectrum, so random tip and tilt of the air do not lower $|S|$.
- **The position is lost.** The closure phases do not fix $\varphi(e_1)$ and $\varphi(e_2)$, so the image comes out at an arbitrary place. A long exposure or a known feature fixes the shift.
- **The phase of a point-symmetric object is trivial.** Then $\varphi$ is 0 or $\pi$ after centering, and the bispectrum adds little to the power spectrum.
- **Errors add along paths.** A wrong closure phase goes into every frequency after it on the path.
- **Phase only.** The modulus comes from speckle interferometry with a reference star.

## Variants and improvements

- **More offsets and least squares.** Keep more planes of $v$ and solve for all phases at once by weighted least squares on the closure phases, which spreads the error over many paths.
- **Full triple correlation.** Weigelt (1977) worked with the triple correlation of the frames in the image domain, whose Fourier transform is the bispectrum.
- **Photon-noise bias correction.** In photon-counting data the bispectrum has bias terms from the photon count, which must be removed before the phase is formed.
- **Closure phases in radio and optical interferometry.** The bispectrum phase of three antennas or apertures is free of the phase errors of each antenna, the same cancellation as here. See [aperture synthesis](/aperture-synthesis/).

## When to use it

Use speckle masking on short exposures of an object through turbulence when a diffraction-limited image is needed without adaptive optics, and in particular when image motion is large or the object is faint, where the [Knox-Thompson method](/knox-thompson-method/) is weaker. If the position of the object matters, fix it from a long exposure. For bright, compact objects, [lucky imaging](/lucky-imaging/) is simpler.

## Pitfalls

- **Too few frames.** $|S|$ is small at high frequencies, and the noise of the bispectrum needs many frames to average down.
- **Forgetting the free linear term.** Comparing the result with the truth without removing $a \cdot u$ gives a large apparent error, and the image is shifted.
- **Adding angles instead of phasors.** Sums of angles wrap at $\pm\pi$; line L6 adds phasors.
- **Memory.** The full bispectrum of a 2D image is 4D. Keep only the planes of small $v$ that the recursion uses.
- **A changed atmosphere for the reference star.** The modulus uses $\langle |T|^2 \rangle$ from another star at another time. If the seeing changed, the modulus is wrong, while the phase is not affected.

## Implementations

## History

Labeyrie (1970) showed that the average power spectrum of short exposures keeps the diffraction-limited modulus, and Knox and Thompson (1974) recovered the phase from cross spectra. Weigelt (1977) introduced speckle masking with triple correlations, and Lohmann, Weigelt and Wirnitzer (1983) gave its theory in terms of the bispectrum and its transfer function. Bartelt, Lohmann and Wirnitzer (1984) studied the recursive recovery of the phase and the modulus from bispectra, and Ayers, Northcott and Dainty (1988) compared speckle masking with the Knox-Thompson method.

## References
