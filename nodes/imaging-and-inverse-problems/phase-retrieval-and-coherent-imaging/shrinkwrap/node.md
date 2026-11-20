---
tag: J58G2A
kind: algorithm
slug: shrinkwrap
name: Shrinkwrap
aliases:
- shrinkwrap support update
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: "Phase retrieval without a known support. Start from the thresholded autocorrelation, run HIO, and every few steps set the support to a threshold of a blurred copy of the estimate."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations, T: the steps between support updates}
  time: {worst: O(K N log N + (K / T) N^2)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2003
  people: [Stefano Marchesini, Henry N. Chapman, John C. H. Spence]
  note: Marchesini and coworkers reconstructed an x-ray image from a diffraction pattern alone, with the support found during the run from the current estimate.
prereqs: [hybrid-input-output, phase-retrieval]
see_also: [coherent-diffraction-imaging, autocorrelation, patterson-function, gaussian-filter, image-thresholding, raar, difference-map, ptychography]
sources:
  - paper: doi:10.1103/PhysRevB.68.140101
    title: S. Marchesini, H. He, H. N. Chapman, S. P. Hau-Riege, A. Noy, M. R. Howells, U. Weierstall and J. C. H. Spence, X-ray image reconstruction from a diffraction pattern alone, Physical Review B 68, 2003, 140101(R)
    locator: the description of the algorithm, with the start from the autocorrelation at the 4 percent level, HIO with beta = 0.9, the update every 20 iterations with a Gaussian of width sigma from 3 pixels down by 1 percent per update to 1.5 pixels, and the threshold at 20 percent (preprint arXiv physics/0306174)
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the hybrid input-output algorithm used for the steps between updates
---

Shrinkwrap is a method for [phase retrieval](/phase-retrieval/) when the support of the object is not known. Marchesini and coworkers (2003) proposed it for x-ray diffraction. It starts with a loose support from the autocorrelation, which the data give directly. It runs [hybrid input-output](/hybrid-input-output/) with that support. Every few steps it blurs the current estimate with a Gaussian and takes the pixels above a fraction of the maximum as the new support. As the estimate improves, the support shrinks around the object.

## In plain words

To find the lost phases you need to know where the object is, but you do not know that before you have the object. Shrinkwrap solves both at once.

The measured pattern gives one free clue: a blurry map of all the distances inside the object. That map is larger than the object, so it is a safe first box. You run the usual repair method in that box for a while. Then you blur the current picture and keep only its bright part as the new box. The box fits the object a little better each time, and a better box gives a better picture.

## The problem

The input is the Fourier magnitude $A = |\mathrm{DFT2}(f)|$ of an unknown nonnegative image $f$ with $N$ pixels. No support is given. The output is a nonnegative image with Fourier magnitude $A$ and a small support. A shift of $f$, and the twin $f(-r)$, have the same data, so the answer is $f$ only up to these changes.

## The algorithm

```pseudo id=main
SHRINKWRAP(A, g₀, K, β, T, σ₀, σ_min, d, τ, τ₀)
L1  S ← {r : |IDFT2(A²)(r)| ≥ τ₀ · max}
L2  g ← g₀;  σ ← σ₀
L3  for k ← 1 to K do
L4      (g, g′) ← HIO-STEP(g, A, S, β)
L5      if k mod T = 0 then
L6          S ← {r : (G_σ ∗ |P_S g′|)(r) ≥ τ · max}
L7          σ ← max(d · σ, σ_min)
L8  return P_S(g′), S
```

- Line L1 is the start. $\mathrm{IDFT2}(A^2)$ is the autocorrelation of $f$, also called the [Patterson function](/patterson-function/) in crystallography. For $f \ge 0$ its support holds a shifted copy of the support of $f$.
- Line L4 is one HIO step with nonnegativity for the current support. $g'$ is the image after the magnitude step.
- Line L6 is the update. $P_S g'$ is the current estimate, $G_\sigma$ is a periodic [Gaussian](/gaussian-filter/) of width $\sigma$ with sum 1, and the new support is the set of pixels where the blur is at least $\tau$ times its maximum.
- Line L7 makes the blur narrower, down to $\sigma_{\min}$.

Marchesini and coworkers used $\tau_0 = 0.04$, $\beta = 0.9$, $T = 20$, $\tau = 0.2$, $\sigma_0 = 3$ pixels, $d = 0.99$ and $\sigma_{\min} = 1.5$ pixels for their images. These values are tuned. The blur must fit the size of the object, as the example shows.

## Example

Take a $16 \times 16$ frame with the nonnegative $5 \times 5$ object

$$\begin{pmatrix} 0 & 1 & 2 & 1 & 0 \\ 1 & 3 & 4 & 2 & 0 \\ 2 & 4 & 5 & 3 & 1 \\ 0 & 2 & 3 & 2 & 2 \\ 0 & 0 & 1 & 2 & 3 \end{pmatrix}$$

at rows 3 to 7 and columns 4 to 8. Its support has 19 pixels. Only $A$ is given. The thresholded autocorrelation (line L1) has 49 pixels, a $7 \times 7$ block around the origin. Run with $\sigma_0 = 1$, $\sigma_{\min} = 0.5$, and the other values as above, from the random start of seed 1. The object error $E_0 = \|g' - P_S g'\|$ at step $k$, and the size of the support after the update at step $k$ (measurements of the implementation):

| step $k$ | 1 | 20 | 40 | 60 | 100 | 200 | 300 | 400 |
|---|---|---|---|---|---|---|---|---|
| $E_0$ | 9.31 | 1.2 | 1.05 | 0.26 | 0.0175 | 6.7e-4 | 4.8e-6 | 4.1e-8 |
| support size | 49 | 24 | 25 | 22 | 22 | 22 | 22 | 21 |

After 400 steps the estimate is the object shifted by 10 rows and 11 columns (with wrap around), to within $4.7 \times 10^{-9}$. The final support has 21 pixels and holds the 19 pixels of the shifted object. The starts of seeds 2 and 3 give the object or its twin, up to a shift, to within $2.7 \times 10^{-7}$ and $1.1 \times 10^{-10}$.

For comparison, HIO with the fixed 49 pixel start support gets to within $0.010$, $0.0094$ and $0.0012$ after 400 steps from the same starts. With Marchesini's widths $\sigma_0 = 3$ and $\sigma_{\min} = 1.5$, which suit images much larger than this one, the support stays at 71 to 80 pixels, and seeds 1 and 3 do not find the object.

## Correctness

The proof page shows four facts. There is no theorem that shrinkwrap finds the object.

- **The start uses only the data.** $\mathrm{IDFT2}(A^2)$ is the autocorrelation $c(t) = \sum_r f(r + t) \overline{f(r)}$.
- **The start is safe before the threshold.** For $f \ge 0$, $c > 0$ on a shifted copy of the support of $f$. The threshold of line L1 is a tuned choice and can cut this.
- **Solutions are fixed points.** If $g = z$ is a nonnegative image with magnitude $A$ and the support holds the support of $z$, the HIO step keeps $z$.
- **The update keeps a solution in some cases.** If $k(0) \min_{z > 0} z \ge \tau \max z$, where $k(0)$ is the center value of the Gaussian, the new support holds the support of $z$.

## Complexity

Each HIO step costs $O(N \log N)$ with a [fast Fourier transform](/fast-fourier-transform/). Each update is one blur. The implementation blurs by direct periodic convolution, $O(N^2)$ per update; a blur through the FFT costs $O(N \log N)$. The start is one inverse FFT. With $K$ steps and an update every $T$ steps, the total is $O(K N \log N + (K/T) N^2)$, or $O(K N \log N)$ with FFT blurs. The extra space is $O(N)$.

## Properties

- **Needs no support.** Only the Fourier magnitude and nonnegativity, or another object constraint.
- **Heuristic.** No convergence proof; the parameters are tuned.
- **Gives the object up to a shift and the twin,** because the data do not fix them.
- **Works with any iteration.** HIO can be replaced by RAAR or the difference map in line L4.

## Variants and improvements

- **Other iterations.** [RAAR](/raar/) or the [difference map](/difference-map/) in place of HIO.
- **Complex objects.** Marchesini and coworkers also report complex objects; then line L4 uses the support constraint without nonnegativity, and line L6 blurs the modulus.
- **Missing data.** Pixels of the pattern behind a beam stop can be left free in the magnitude step, as in the original paper.
- **Final polish.** A few steps of [error reduction](/error-reduction-algorithm/) with the final support reduce the error further.
- **[Ptychography](/ptychography/).** Many overlapping patterns make the support constraint less important.

## When to use it

Use shrinkwrap for [coherent diffraction imaging](/coherent-diffraction-imaging/) of an isolated object when the support is not known well. Choose the blur width from the size of the object in pixels, and try several starts.

## Pitfalls

- **A blur that is too wide.** The support then stays too large, as in the example with $\sigma = 3$ on a small object.
- **A threshold that is too high.** Weak parts of the object fall out of the support and are lost.
- **Comparing with the truth.** The answer can be shifted, and it can be the twin. Compare up to shifts and the twin.
- **Noise.** Marchesini and coworkers expect the method to fail when the noise in the estimate becomes larger than the update threshold, because the noise then shapes the support.

## Implementations

## History

The support of the autocorrelation as a bound for the object comes from the vector space methods of crystallography, which the paper cites through Buerger (1959). Marchesini and coworkers (2003) made the support update part of the iteration, with the blur and threshold step. They reconstructed an image of a test object made of gold balls from an x-ray diffraction pattern at a wavelength of 2.1 nm alone. They also compared HIO with fixed supports of known accuracy under Poisson noise, and found that HIO needs a support known at about the resolution of the reconstruction.

## References
