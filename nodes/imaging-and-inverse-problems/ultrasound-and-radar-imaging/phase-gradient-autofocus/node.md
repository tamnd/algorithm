---
tag: Y2C9T3
kind: algorithm
slug: phase-gradient-autofocus
name: Phase gradient autofocus
aliases:
- PGA
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Estimate and remove a phase error common to all range bins of a SAR image from the phase derivatives of circularly shifted bright scatterers."
model: real-ram
complexity:
  vars: {M: the number of range bins, N: the number of azimuth samples, I: the number of iterations}
  time: {worst: O(I M N log N)}
  space: {extra: O(M N), data: O(M N)}
properties: {deterministic: true, linear_in_data: false, recursive: false, exact: false}
history:
  year: 1989
  people: [Paul H. Eichel, Dennis C. Ghiglia, Charles V. Jakowatz Jr.]
  note: "Eichel, Ghiglia and Jakowatz proposed the method in 1989; Wahl, Eichel, Ghiglia and Jakowatz described the full algorithm and its robustness in 1994."
prereqs: [sar-image-formation, fast-fourier-transform]
see_also: [polar-format-algorithm, sar-backprojection, synthetic-aperture-radar, phase-unwrapping, point-spread-function, maximum-likelihood-estimation, cramer-rao-bound, window-functions]
sources:
  - paper: doi:10.1109/7.303752
    title: "Daniel E. Wahl, Paul H. Eichel, Dennis C. Ghiglia and Charles V. Jakowatz Jr., Phase gradient autofocus: a robust tool for high resolution SAR phase correction, IEEE Transactions on Aerospace and Electronic Systems 30(3), 1994, 827 to 835"
    locator: "the four steps (center shift, windowing, phase gradient estimation, iterative correction) and the measured results (general locator)"
  - paper: doi:10.1364/OL.14.000001
    title: "Paul H. Eichel, Dennis C. Ghiglia and Charles V. Jakowatz Jr., Speckle processing method for synthetic-aperture-radar phase correction, Optics Letters 14(1), 1989"
    locator: "the first description of the method (general locator)"
  - book: isbn:9780792396772
    title: "Charles V. Jakowatz Jr., Daniel E. Wahl, Paul H. Eichel, Dennis C. Ghiglia and Paul A. Thompson, Spotlight-Mode Synthetic Aperture Radar: A Signal Processing Approach, Kluwer, 1996"
    locator: "the chapter Phase Errors and Autofocus in SAR Imagery"
---

Phase gradient autofocus (PGA) removes the blur that an unknown phase error causes in a [synthetic aperture radar](/synthetic-aperture-radar/) image. If the path of the antenna is not known to a small part of the wavelength, or the atmosphere adds a delay, the azimuth phase history of every range bin is multiplied by the same unknown factor $e^{i\phi(k)}$, and every target is smeared in azimuth by the same [point spread function](/point-spread-function/). PGA estimates $\phi$ from the image itself. In each range bin it shifts the brightest pixel to the center, cuts a window around it to keep the blurred response of that scatterer and drop most others, and takes the azimuth DFT. The phase differences of neighboring samples, summed over all range bins, estimate the derivative of $\phi$; integrating gives $\phi$, which is removed. The steps are repeated, with a smaller window as the image gets sharper. A constant and a linear part of $\phi$ only shift the image, so PGA estimates $\phi$ up to $a + b k$. PGA is a heuristic with strong measured results; one exact statement holds for isolated scatterers.

## In plain words

A blurred radar picture is often blurred in the same way everywhere, because the same error in the flight path affects every echo. Bright single reflectors show this blur clearly. Move the brightest point of each row to the middle, so that all the blurred copies line up. Cut away the rest of each row. Now every row shows the same blur, plus a little noise. Turning each row back into the frequency form shows the error as a twist in its phase, and averaging over many rows gives a good estimate of the twist. Untwist the picture and repeat a few times.

## The problem

The input is a complex image $g_m[j]$ with $M$ range bins $m$ and $N$ azimuth pixels $j$. Its azimuth phase histories are $G_m = \text{DFT}(g_m)$. The model is $G_m(k) = F_m(k)\, e^{i\phi(k)}$, where $F_m$ is the phase history of the focused image and $\phi$ is an unknown phase error, the same for every range bin. The output is an estimate $\hat\phi$ and the corrected image $\text{IDFT}(G_m e^{-i\hat\phi})$. Because $e^{i(a + b k)}$ with $b = 2\pi s/N$ only multiplies the image by a constant and shifts it by $s$ pixels, $\phi$ can only be found up to $a + b k$. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT. Autofocus does not solve [SAR image formation](/sar-image-formation/) by itself; it corrects the output of an image formation algorithm.

## The algorithm

```pseudo id=main
PGA(g, iterations, tol)    ▷ g[m][j]: complex image, range bin m, azimuth pixel j; c = N/2
L1  for every row m: s_m[j] ← g_m[(j + j_m - c) mod N] with j_m the index of the largest |g_m[j]|   ▷ center shift
L2  w_m[j] ← s_m[j] for |j - c| within the window, 0 elsewhere               ▷ window from the -10 dB width
L3  h_m ← DFT(w_m) for every row m
L4  Δ(k) ← arg Σ_m h_m[k] conj(h_m[k - 1]) for k = 1, ..., N - 1          ▷ phase gradient, summed over rows
L5  ψ ← arg Σ_k e^{iΔ(k)};  φ̂(k) ← Σ_{l ≤ k} wrap(Δ(l) - ψ);  remove the line a + b k from φ̂
L6  g_m ← IDFT(DFT(g_m) · e^{-iφ̂}) for every row m; add φ̂ to the total estimate
L7  if rms(φ̂) < tol or the iterations are done: return g and the total estimate; else go to L1
```

Line L1 moves the brightest pixel of each row to the center $c$, which removes the different positions of the scatterers: each row then holds a copy of the blur that peaks at $c$. Line L2 keeps a window around the center. Its width is 1.5 times the width of the region where the summed intensity $\sum_m |s_m[j]|^2$ stays above 10% of its center value, but at least 16 pixels; this follows the blur and drops clutter outside it. Line L3 returns to the phase history. Line L4 is the estimate of the gradient: in each row, $h_m[k]\, \overline{h_m[k - 1]}$ has the phase $\phi(k) - \phi(k - 1)$ plus noise, and the sum over rows weights each row by its energy. Line L5 integrates; removing the circular mean $\psi$ first keeps the integration away from jumps of $2\pi$, and the linear part is removed at the end. Line L6 applies the correction, and L7 stops when the correction is small. The default is at most 8 iterations and a tolerance of 0.01 rad.

## Example

The tests use $M = 24$ range bins of $N = 64$ azimuth pixels. Each row has one bright scatterer, of amplitude 3, 4 or 5 at a random place, in complex Gaussian clutter of standard deviation 0.3 per part. The phase error is $\phi(k) = 8 t^2 + 3 t^3$ with $t = (k - 32)/32$, whose rms after removing its best line is 2.385 rad. The rms of the remaining error, also after removing the best line, is:

| seed | 1 iteration | 2 | 4 | 8 |
|---|---|---|---|---|
| 1 | 0.53 | 0.188 | 0.153 | 0.178 |
| 2 | 0.385 | 0.222 | 0.197 | 0.194 |
| 3 | 0.488 | 0.174 | 0.158 | 0.161 |
| 4 | 0.40 | 0.172 | 0.131 | 0.113 |

Most of the gain comes in the first two iterations; the rest of the error is set by the clutter. For a quadratic error $6 t^2$, a brute-force search over 41 quadratic coefficients that maximizes $\sum |g|^4$ finds 6.0, and PGA gives 6.38. With one scatterer per row, no clutter and the full window, one iteration finds $\phi$ up to $a + b k$ within $10^{-15}$. All values are measurements on these simulations, except the last, which the theorem of the next section predicts.

## Correctness

PGA is a heuristic: there is no general guarantee that its iterations converge to the true phase error. One exact statement holds. If every row holds a single scatterer, the blur $|\text{IDFT}(e^{i\phi})|$ has a unique largest value, the window keeps whole rows, and the differences $\phi(k) - \phi(k - 1)$ all lie in an open interval of length $\pi$, then one iteration returns $\phi$ exactly up to $a + b k$. With clutter, the estimate of L4 is a sum over rows of the true gradient with independent noise, and the sum lowers the noise as the number of rows with a strong scatterer grows; this is the reason PGA works well on real scenes, and the window improves the ratio of the scatterer energy to the clutter energy in each row. The proof of the exact case is in proofs/correctness.md.

## Complexity

Each iteration does $M$ shifts and windows in $O(M N)$, $M$ DFTs and $M$ inverse DFTs in $O(M N \log N)$ with an FFT, and the gradient sum and integration in $O(M N)$. With $I$ iterations the total is $O(I M N \log N)$ in the real-RAM model, with $O(M N)$ extra space.

## Properties

- Not linear in the data: the shift, the window and the phase are all chosen from the data.
- Estimates a phase error of any shape, not only a polynomial of low order.
- Blind to a constant and to a linear phase, which only shift the image.
- Needs a phase error that is the same for every range bin, and scatterers that stand out from the clutter in many rows.
- Works on the complex image, so it can be applied after any image formation algorithm.

## Variants and improvements

- **Other gradient estimators.** The derivative can be estimated as $\sum_m \text{Im}(\overline{h_m} h_m') / \sum_m |h_m|^2$ from a derivative of each history, or, as here, from the phase of summed products of neighbors, which needs no derivative of the data.
- **Row selection.** Using only the range bins whose brightest pixel stands out most from the rest of the row improves the estimate in scenes with weak scatterers.
- **Range-dependent errors.** For errors that change with range, as in wide scenes or in stripmap mode, PGA is applied to blocks of range bins or extended with a model of how $\phi$ varies.
- **Model-based autofocus.** Map drift fits a quadratic phase from the shift between images of two subapertures, and contrast or sharpness methods search over the coefficients of a polynomial phase, as in the brute-force test.

## When to use it

Use PGA after forming a SAR image, for spotlight images formed by the [polar format algorithm](/polar-format-algorithm/) or [backprojection](/sar-backprojection/) when the motion measurement is not accurate enough, and when the phase error may have a complex shape. For a smooth error with a few known terms, a model-based method is cheaper and more robust. Scenes without bright scatterers, such as calm water or uniform fields, give PGA little to work with.

## Pitfalls

- **A window that is too narrow at the start.** The first window must hold the whole blur, or the estimate keeps only part of the error. Start wide and let it shrink.
- **Wrapping.** Integrating gradients that are wrapped to $(-\pi, \pi]$ can add jumps of $2\pi$ when the gradient has a large linear part; remove the circular mean first, as in L5.
- **Errors that depend on range.** PGA assumes one $\phi$ for all range bins. If the error changes over the scene, the estimate is an average and focuses only part of it.
- **Too few iterations or too strict a stop.** Most of the gain comes in the first iterations, and the rest is limited by the clutter; a very small tolerance only runs more iterations.
- **Wrong axis.** PGA works on the azimuth phase history; the image must be in range bins by azimuth pixels.

## Implementations

## History

Eichel, Ghiglia and Jakowatz (1989) proposed estimating the SAR phase error from the image itself, in a paper on speckle processing for phase correction. Wahl, Eichel, Ghiglia and Jakowatz (1994) described the full algorithm, with the four steps of center shift, windowing, phase gradient estimation and iterative correction, and presented it as a robust tool for phase errors of high order. The book of Jakowatz and colleagues (1996) treats it in its chapter on phase errors and autofocus, and PGA has since become a standard autofocus method for spotlight SAR.

## References
