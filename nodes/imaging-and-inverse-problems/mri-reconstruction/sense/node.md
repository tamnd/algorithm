---
tag: 7VT2V0
kind: algorithm
slug: sense
name: SENSE
aliases:
- sensitivity encoding
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: "Unfolds an aliased image from uniformly undersampled multi-coil Cartesian data by solving a small least squares problem with the coil sensitivities at each pixel. Needs R <= c."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n image, a multiple of R", c: "the number of coils", R: "the reduction factor, R <= c"}
  time: {worst: O(c n^2 log n + c^2 n^2)}
  space: {extra: O(c n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: true}
history:
  year: 1999
  people: [Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger, Peter Boesiger]
  note: Pruessmann, Weiger, Scheidegger and Boesiger gave the unfolding with known coil sensitivities and the noise analysis with the g-factor.
prereqs: [coil-sensitivity-map, least-squares-problem]
see_also: [g-factor, cg-sense, grappa, espirit, root-sum-of-squares-coil-combination, generalized-least-squares, aliasing, normal-equations]
sources:
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S
    title: Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger and Peter Boesiger, SENSE, sensitivity encoding for fast MRI, Magnetic Resonance in Medicine 42(5), 1999, 952 to 962
    locator: the unfolding of Cartesian data with known sensitivities, the weighted least squares solution with the noise matrix, and the g-factor (general locator; section numbers not confirmed)
  - paper: doi:10.1002/mrm.1910380414
    title: Daniel K. Sodickson and Warren J. Manning, Simultaneous acquisition of spatial harmonics (SMASH), fast imaging with radiofrequency coil arrays, Magnetic Resonance in Medicine 38(4), 1997, 591 to 603
    locator: the earlier k-space method that combines coil signals to synthesize the missing spatial harmonics (general locator)
  - paper: doi:10.1002/mrm.1241
    title: Klaas P. Pruessmann, Markus Weiger, Peter Boernert and Peter Boesiger, Advances in sensitivity encoding with arbitrary k-space trajectories, Magnetic Resonance in Medicine 46(4), 2001, 638 to 651
    locator: the iterative form for any trajectory (general locator)
  - paper: doi:10.1002/mrm.20401
    title: Felix A. Breuer, Martin Blaimer, Robin M. Heidemann, Matthias F. Mueller, Mark A. Griswold and Peter M. Jakob, Controlled aliasing in parallel imaging results in higher acceleration (CAIPIRINHA) for multi-slice imaging, Magnetic Resonance in Medicine 53(3), 2005, 684 to 691
    locator: the shift of the aliased copies that lowers the g-factor (general locator)
---

SENSE (sensitivity encoding) reconstructs an MR image from a Cartesian scan that skips phase encoding lines, with an array of $c$ receive coils. If the scan keeps every $R$-th line, the image of each coil is folded: $R$ pixels, at distance $n/R$ apart, fall on the same place. Each coil sees the folded pixels with different weights, its [coil sensitivity map](/coil-sensitivity-map/). At each folded pixel the $c$ coil values give $c$ linear equations in $R$ unknowns, and SENSE solves this small [least squares problem](/least-squares-problem/). Pruessmann, Weiger, Scheidegger and Boesiger published it in 1999. Without noise and with full column rank at every pixel, the result is exact (a theorem; the [proof](proofs/correctness.md) is on this page). The noise grows by the [g-factor](/g-factor/) times $\sqrt{R}$.

## In plain words

Leave out every second line of the scan and the picture folds: the top half lands on the bottom half. One coil cannot tell which half a bright spot came from. But a coil near the top sees the top half brightly and the bottom half dimly, and a coil near the bottom sees the opposite. If we know how bright each coil sees each place, every folded pixel gives a small puzzle: two unknown values, one equation per coil. With two or more coils that see the two places differently, the puzzle has one answer. SENSE solves one such puzzle for every folded pixel.

## The problem

The input is the k-space $y_k$ of each coil $k = 1, \ldots, c$ on the rows $\kappa = 0, R, 2R, \ldots$ of the phase encoding axis of an $n \times n$ grid, the maps $s_k$, the reduction factor $R$ with $R \mid n$, and optionally the $c \times c$ noise covariance $\Psi$ between the coils. The model is $y_k = M F_u (s_k x)$ with the unitary 2D DFT $F_u = F/n$ and the row mask $M$ (see [mri-signal-equation](/mri-signal-equation/) and [k-space](/k-space/)). The output is the image $x$. This is the Cartesian case of the [MRI reconstruction problem](/mri-reconstruction-problem/) with uniform undersampling.

## The algorithm

Let $m = n/R$. The folded pixel $(i, j)$ with $0 \le i < m$ holds the image pixels $(i + pm, j)$ for $p = 0, \ldots, R - 1$.

```pseudo id=main
SENSE(y, s, R, Psi)                   ▷ y_k known on the rows kappa = 0, R, 2R, ...
L1  m <- n / R
L2  a_k <- n F^{-1}_{m x n}(kept rows of y_k) for each coil k   ▷ folded images
L3  L <- Cholesky factor of Psi (Psi = L L^H)
L4  for each folded pixel (i, j), 0 <= i < m do
L5      E[k][p] <- s_k(i + p m, j)    ▷ c x R unfolding matrix
L6      E <- L^{-1} E; b <- L^{-1} (a_1(i,j), ..., a_c(i,j))
L7      solve (E^H E) v = E^H b       ▷ R x R normal equations
L8      x(i + p m, j) <- v_p for p = 0, ..., R - 1
L9  return x
```

Line L2 is an inverse DFT of size $m \times n$ of the kept rows; by the folding lemma of the proof it gives $a_k(i, j) = \sum_p s_k(i + pm, j)\, x(i + pm, j)$. The rows that the scan skips are never read. Line L6 whitens the coils, so that line L7 solves the weighted least squares problem $\min_v (a - Ev)^H \Psi^{-1} (a - Ev)$. Without a covariance, $L = I$. The code can also add $\lambda I$ to the matrix of line L7, a [Tikhonov](/tikhonov-regularization/) step against noise; then the output is biased.

## Example

Take one image column with $n = 4$, $R = 2$, $c = 2$, the maps $s_1 = (1, 0.9, 0.5, 0.3)$ and $s_2 = (0.5, 0.6, 1, 0.9)$ along the column, the object $x = (2, 3, 1, 0)$ and $\Psi = I$. Then $m = 2$. Folded pixel 0 holds pixels 0 and 2, and folded pixel 1 holds pixels 1 and 3.

| folded pixel | $E$ (rows are coils) | $a$ | $v$ | g-factor of the two pixels |
|---|---|---|---|---|
| 0 | $\begin{pmatrix} 1 & 0.5 \\ 0.5 & 1 \end{pmatrix}$ | $(2.5, 2)$ | $(2, 1)$ | 1.6667, 1.6667 |
| 1 | $\begin{pmatrix} 0.9 & 0.3 \\ 0.6 & 0.9 \end{pmatrix}$ | $(2.7, 1.8)$ | $(3, 0)$ | 1.6288, 1.6288 |

For folded pixel 0, $a_1 = 1 \cdot 2 + 0.5 \cdot 1 = 2.5$ and $a_2 = 0.5 \cdot 2 + 1 \cdot 1 = 2$, and the $2 \times 2$ system gives $v = (2, 1)$, so line L8 writes $x_0 = 2$ and $x_2 = 1$. For folded pixel 1, $\det E = 0.63$ and $v = (3, 0)$. The output is $(2, 3, 1, 0)$, the object. The g-factor of folded pixel 0 is $\sqrt{[(E^HE)^{-1}]_{00} [E^HE]_{00}} = \sqrt{2.2222 \cdot 1.25} = 1.6667$. With $c = R$ the two pixels of a group have the same g-factor.

## Correctness

At each folded pixel the data are $a = Ev$ plus noise. If $E$ has full column rank, the normal equations of line L7 have one solution, and without noise that solution is $v$, the true pixel values. Full column rank of a $c \times R$ matrix needs $R \le c$. The noise covariance of the output at pixel $i + pm$ is $R[(E^H\Psi^{-1}E)^{-1}]_{pp}$, and the g-factor is at least 1 by the Cauchy-Schwarz inequality. The [proof](proofs/correctness.md) gives the folding lemma and both statements. These are theorems about the discrete model with known maps; they say nothing about errors in the maps.

## Complexity

In the [real RAM](/real-ram/), line L2 costs $c$ inverse FFTs of size $m \times n$, $O(c n^2 \log n)$ for $n$ a power of two (with a direct DFT it would be $O(c n^3)$ by rows and columns). Line L3 costs $O(c^3)$ once. The loop runs over $n^2/R$ folded pixels. Each one whitens $R + 1$ vectors in $O(c^2)$ each, forms the normal equations in $O(c R^2)$ and solves them in $O(R^3)$. With $R \le c$ the loop costs $O(c^2 n^2)$, and the total is $O(c n^2 \log n + c^2 n^2)$. The memory holds the $c$ folded images, $O(c n^2)$. The method is not iterative.

## Properties

- **Exact without noise.** If every unfolding matrix has full column rank, the output is the object (theorem).
- **Linear.** For fixed maps and $\Psi$, the output is a linear function of the data.
- **Noise.** The signal to noise ratio falls by $g\sqrt{R}$ against full sampling, with $g \ge 1$ at every pixel (theorem; Pruessmann et al. 1999). The test of this page checks the predicted variance on pure noise with a correlated $\Psi$ within 8 percent.
- **Coil geometry sets the g-factor.** For the four ring coils of the tests ($32 \times 32$, Gaussian coils centered at distance 1.2 at the angles 20, 110, 200 and 290 degrees), the g-factor had the mean 1.342 and the maximum 2.918 at $R = 2$, and the mean 67.3 and the maximum 393 at $R = 4$, although the noiseless $R = 4$ result was still exact to $1.2 \times 10^{-11}$ (measurement with the code of this page).
- **Local.** Each folded pixel is a separate problem, so the work runs in parallel.

## Variants and improvements

- **CG-SENSE.** For non-Cartesian or irregular sampling the problem does not split into small pixel groups. [CG-SENSE](/cg-sense/) solves the same least squares problem with the [conjugate gradient method](/conjugate-gradient-method/). For uniform Cartesian sampling both give the same answer.
- **Regularized SENSE.** Adding $\lambda I$, or a prior image, in line L7 lowers the noise where the g-factor is high, at the cost of bias.
- **CAIPIRINHA.** Shifting the sampling pattern between the two phase encoding axes in 3D, or between slices in simultaneous multi-slice imaging, moves the aliased copies apart and lowers the g-factor (Breuer et al. 2005; see [slice-GRAPPA](/slice-grappa/)).
- **Maps from the data.** [ESPIRiT](/espirit/) estimates the maps from a calibration region, so that SENSE becomes autocalibrating.
- **k-space methods.** [GRAPPA](/grappa/) and [SPIRiT](/spirit/) fill the missing k-space samples without explicit maps. SMASH (Sodickson and Manning 1997) was the first such method.

## When to use it

Use SENSE for Cartesian scans with uniform undersampling when good coil maps are known, for example from a low resolution prescan or from [ESPIRiT](/espirit/). It is fast and gives an exact answer for exact maps. Choose $R$ well below the number of coils that see each pixel group differently: the g-factor grows quickly as $R$ approaches that number. When the object is larger than the reduced field of view in a way the maps do not model, or the maps are poor, use [GRAPPA](/grappa/), which needs no maps.

## Pitfalls

- **R larger than c.** With $R > c$, the matrix of line L7 is singular, and the problem has no unique solution. The code refuses this case without regularization.
- **Wrong maps.** Errors in $s_k$ in line L5 go straight into the output as residual aliasing. Maps from a prescan can be wrong after motion.
- **Object outside the maps.** If the maps are zero, or wrong, where the object has signal, for example when the field of view of the maps is too small, line L7 places that signal in the wrong pixel.
- **High g-factor.** Where the coils see the folded pixels in almost the same way, $E$ in line L7 is ill-conditioned, and the noise is amplified even though the noiseless result is exact.
- **Forgetting the noise covariance.** Correlated coil noise with $\Psi = I$ in line L3 still gives an exact noiseless result, but not the least noise.
- **Scale of the folded image.** Line L2 needs the factor $n$; without it the output is too small by that factor.

## Implementations

## History

Sodickson and Manning showed in 1997 with SMASH that coil arrays can replace phase encoding steps. Pruessmann, Weiger, Scheidegger and Boesiger published SENSE in 1999, with the unfolding in the image domain, the use of the coil noise matrix and the g-factor. In 2001 Pruessmann, Weiger, Boernert and Boesiger extended it to any trajectory with the conjugate gradient method, the method now called [CG-SENSE](/cg-sense/). Griswold and colleagues published [GRAPPA](/grappa/), a k-space method without explicit maps, in 2002.

## References
