---
tag: QDZSDB
kind: algorithm
slug: gerchberg-saxton-algorithm
name: Gerchberg-Saxton algorithm
aliases:
- GS algorithm
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "Find a phase that fits known magnitudes in two planes linked by a Fourier transform, by putting each magnitude on in turn and keeping the phase. The error never grows."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {n: the number of samples in each plane, K: the number of iterations}
  time: {worst: O(K n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1972
  people: [Ralph W. Gerchberg, W. Owen Saxton]
  note: Gerchberg and Saxton found the phase of an electron microscope image from the image and diffraction plane intensities.
prereqs: [phase-retrieval, discrete-fourier-transform]
see_also: [error-reduction-algorithm, hybrid-input-output, griffin-lim-algorithm, transport-of-intensity-equation, phase-diversity, fast-fourier-transform, projected-gradient-descent, phase-retrieval-ambiguities]
sources:
  - paper: "R. W. Gerchberg and W. O. Saxton, A practical algorithm for the determination of phase from image and diffraction plane pictures, Optik 35(2), 1972, pages 237 to 246"
    locator: the iteration between the image plane and the diffraction plane
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the Gerchberg-Saxton algorithm as the parent of error reduction, and the proof that the error does not increase
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: the section on alternating projection algorithms
---

The Gerchberg-Saxton algorithm is one of the first iterative methods for [phase retrieval](/phase-retrieval/). The magnitude of a complex field is known in two planes, an image plane and a diffraction plane, that a Fourier transform links. The phase is not known in either plane. The algorithm starts with any phase. It goes back and forth between the planes, and in each plane it puts on the known magnitude and keeps the current phase. Each step is a nearest point projection, so the error never grows (Fienup 1982). It can still stop before it finds a solution.

## In plain words

You know how bright a light field is at two places: right at an object, and far away, where the light has spread out. You do not know how the waves line up at either place. The far field is the Fourier transform of the near field.

Guess the alignment at the object. Use the known brightness there, compute the far field, and look at it. Its brightness is wrong. Replace the brightness with the measured one and keep the alignment. Go back to the object, and do the same there. Repeat.

Each round fixes one place and spoils the other a little. The disagreement never grows. Often it falls to zero and the alignment is found. Sometimes it gets stuck.

## The problem

The input is two arrays of magnitudes of length $n$: $a_j = |f_j|$ in the object plane and $A_u = |F_u|$ in the Fourier plane, where $F$ is the DFT of an unknown complex signal $f$. The DFT is unnormalized forward with $1/n$ on the inverse. The output is a signal $g$ with $|g_j| = a_j$ and $|G_u| = A_u$ for all $j$ and $u$. The same steps work in 2D, with the 2D DFT. At best, $g$ equals $f$ up to a constant phase factor $e^{i\phi}$, which no magnitude can see.

## The algorithm

```pseudo id=main
GERCHBERG-SAXTON(a, A, φ, K)
L1  g_j ← a_j · e^{iφ_j} for each j
L2  for k ← 1 to K do
L3      G ← DFT(g)
L4      G′_u ← A_u · G_u / |G_u| for each u        ▷ A_u when G_u = 0
L5      g′ ← IDFT(G′)
L6      g_j ← a_j · g′_j / |g′_j| for each j        ▷ a_j when g′_j = 0
L7  return g
```

Lines L3 to L5 replace the Fourier magnitude and keep the phase. Line L6 does the same in the object plane. The error is measured with the unitary DFT, so that it is a distance between signals:

$$E_F(g)^2 = \frac{1}{n}\sum_u \bigl(|G_u| - A_u\bigr)^2, \qquad E_0(g')^2 = \sum_j \bigl(|g'_j| - a_j\bigr)^2 .$$

## Example

Take $f = (1, i, -1, 2, 0, 0, 0, 0)$, a signal of length 8 whose last four samples are zero. So $a = (1, 1, 1, 2, 0, 0, 0, 0)$. Its DFT magnitudes are

$$A = \bigl(\sqrt5,\ \sqrt2 - 1,\ \sqrt{13},\ 3 + \sqrt2,\ \sqrt5,\ 1 + \sqrt2,\ \sqrt5,\ 3 - \sqrt2\bigr) \approx (2.236, 0.414, 3.606, 4.414, 2.236, 2.414, 2.236, 1.586).$$

For example $F_0 = 1 + i - 1 + 2 = 2 + i$, so $A_0 = \sqrt5$. The start phases $\phi$ are random. These are measurements of the implementation with seed 1:

| iteration $k$ | 0 | 1 | 2 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|---|---|
| $E_F(g_k)$ | 1.16 | 0.816 | 0.642 | 0.368 | 0.0611 | 4.6e-4 | 2.9e-10 | 8e-17 |

The result is $g = c f$ with $c \approx 0.143 - 0.990i$, so $|c| = 1$: the signal is found up to a global phase, which is the best possible. Seeds 2 to 5 also reach errors near $10^{-16}$ within 200 iterations. The zeros in $a$ help: they act like a support constraint, as in the [error reduction algorithm](/error-reduction-algorithm/). With no zeros in $a$, the same code from random starts often stops at an error near $10^{-2}$.

## Correctness

Line L4 gives the nearest point to $G$ among the spectra with magnitude $A$, one frequency at a time: for $|w| = a$, $|z - w| \ge \bigl||z| - a\bigr|$, with equality at $w = a z / |z|$. By Parseval's identity for the unitary DFT, lines L3 to L5 are the nearest signal with Fourier magnitude $A$. Line L6 is the nearest signal with object magnitude $a$. With $g'_k$ the signal of line L5,

$$E_F(g_{k+1}) \le \|g_{k+1} - g'_k\| = E_0(g'_k) \le \|g'_k - g_k\| = E_F(g_k).$$

So the error does not increase, and a run that reaches error zero has found a signal that fits both magnitudes. This is a theorem. Neither set is convex, so there is no theorem that the error reaches zero. The full proof is below.

## Complexity

Each iteration does one DFT and one inverse DFT and $O(n)$ other work. With a [fast Fourier transform](/fast-fourier-transform/) the cost is $O(n \log n)$ per iteration and $O(K n \log n)$ in total, and $O(n^2)$ per iteration with the direct sum. The extra space is $O(n)$. On an image of $n = n_1 n_2$ pixels, the 2D FFT also costs $O(n \log n)$.

## Properties

- **Monotone.** The error $E_F$ does not increase (a theorem).
- **Fixed points.** Every signal that fits both magnitudes is a fixed point. Stagnation points are fixed points too.
- **Global phase.** If $g$ is a solution, so is $e^{i\phi} g$. The output depends on the start through this factor.
- **Local.** The result depends on the start.

## Variants and improvements

- **[Error reduction](/error-reduction-algorithm/).** Fienup replaced the object magnitude by a support and nonnegativity, for the case of one intensity measurement.
- **[Hybrid input-output](/hybrid-input-output/).** A feedback step that escapes most stagnation points.
- **[Griffin-Lim algorithm](/griffin-lim-algorithm/).** The same alternation for the magnitudes of a short-time Fourier transform, used for audio.
- **Weighted and phase-only holograms.** To design a phase plate or a phase-only light modulator that makes a wanted far field, one runs GS with a uniform object magnitude. Weighted versions change the target magnitude between iterations to make the far field more uniform. This is a heuristic with no error guarantee.
- **Other propagators.** Replace the DFT with a Fresnel propagator for two planes at a finite distance, or use more than two planes. This is close to [phase diversity](/phase-diversity/).
- **Transport of intensity.** For two planes that are very close, the [transport-of-intensity equation](/transport-of-intensity-equation/) gives the phase directly: it is a [Poisson equation](/poisson-equation/) for the phase, and a fast Poisson solver replaces the iteration.

## When to use it

Use GS when you have a reliable magnitude in two planes and a Fourier (or Fresnel) model links them, for example to find the phase of a wavefront from an in-focus and a far-field image, or to design a phase-only hologram. If you have only one magnitude and a support, use error reduction, hybrid input-output or one of the newer projection methods. If the data are noisy, the error will not reach zero; stop when it reaches the noise level.

## Pitfalls

- **The centered transform.** Optical data usually have the zero frequency in the middle. Shift the data with fftshift before you compare them with an unshifted DFT, or the two planes do not match.
- **Intensity and magnitude.** Detectors measure the intensity $|F_u|^2$. Take the square root first.
- **The scale of the DFT.** With the unnormalized DFT, $\sum_u |F_u|^2 = n \sum_j |f_j|^2$. Data that break this energy balance are inconsistent, and the error cannot reach zero.
- **Zeros.** Where $G_u = 0$, the phase is not defined. Any fixed choice keeps the proof valid; line L4 uses phase zero.
- **Stagnation.** A flat error that is not zero is a stagnation point, not a solution. Restart from other phases.

## Implementations

## History

Gerchberg and Saxton published the algorithm in 1972. They wanted the phase of the electron wave in an electron microscope, from one picture in the image plane and one in the diffraction plane. Fienup (1978, 1982) changed it for the case of one intensity measurement and constraints in the object domain, which gave the error reduction and hybrid input-output algorithms, and proved that the error of the alternation does not increase.

## References
