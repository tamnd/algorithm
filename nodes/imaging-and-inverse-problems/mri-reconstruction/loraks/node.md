---
tag: HJ4N14
kind: algorithm
slug: loraks
name: LORAKS
aliases:
- low-rank modeling of local k-space neighborhoods
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: Reconstruct undersampled MRI by asking that matrices built from local k-space neighborhoods have low rank, which follows from limited support or smooth phase.
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: the number of k-space grid points, w: the number of offsets in one neighborhood, r: the target rank, K: the number of iterations}
  time: {worst: O(K (n w^2 + w^3))}
  space: {extra: O(n w)}
properties: {deterministic: true, iterative: true, convex: false, monotone: true, online: false, in_place: false}
history:
  year: 2014
  people: [Justin P. Haldar]
  note: Haldar showed that matrices of local k-space neighborhoods have low rank when the image has limited support or a smooth phase, and reconstructed k-space by a low rank fit.
prereqs: [k-space, singular-value-decomposition, partial-fourier-reconstruction]
see_also: [spirit, espirit, low-rank-plus-sparse-mri, compressed-sensing-mri, matrix-completion, prony-method, homodyne-reconstruction, robust-pca]
sources:
  - paper: doi:10.1109/TMI.2013.2293974
    title: Justin P. Haldar, Low-rank modeling of local k-space neighborhoods (LORAKS) for constrained MRI, IEEE Transactions on Medical Imaging 33(3), 2014, 668 to 681
    locator: the C, G and S matrices, the rank arguments from limited support and smooth phase, and the penalized reconstruction (general locator)
  - paper: "Justin P. Haldar, Low-rank modeling of local k-space neighborhoods (LORAKS): implementation and examples for reproducible research, USC-SIPI Technical Report 414, University of Southern California, April 2014"
    locator: equation (4) for the penalized objective, equation (5) for the tail sum of squared singular values, and the majorize-minimize algorithm
  - paper: doi:10.1002/mrm.25717
    title: Justin P. Haldar and Jingwei Zhuo, P-LORAKS, low-rank modeling of local k-space neighborhoods with parallel imaging data, Magnetic Resonance in Medicine 75(4), 2016, 1499 to 1514
    locator: the extension to multichannel data and calibrationless parallel imaging (general locator)
  - paper: doi:10.1109/msp.2019.2949570
    title: Justin P. Haldar and Kawin Setsompop, Linear predictability in magnetic resonance imaging reconstruction, IEEE Signal Processing Magazine 37(1), 2020, 69 to 82 (arXiv:1903.03141)
    locator: the linear predictability of k-space from limited support, smooth phase and multichannel data, and the note that exact annihilation needs a support of measure zero (general locator)
  - paper: doi:10.1109/MSP.2019.2950432
    title: Mathews Jacob, Merry P. Mani and Jong Chul Ye, Structured low-rank algorithms, IEEE Signal Processing Magazine 37(1), 2020, 54 to 68
    locator: the survey of structured low rank methods for MRI and their relation to annihilating filters (general locator)
---

LORAKS (low-rank modeling of local k-space neighborhoods) reconstructs an MR image from undersampled [k-space](/k-space/) by a low rank fit in k-space itself. It builds a matrix whose rows are small neighborhoods of k-space samples. When the image is zero outside a region, or when its phase is smooth, this matrix has low rank, or nearly so. LORAKS fills the missing samples so that the matrix is close to rank $r$ and the measured samples agree with the data. It uses no sparsifying transform, which sets it apart from [compressed sensing MRI](/compressed-sensing-mri/). It also differs from [low-rank plus sparse MRI](/low-rank-plus-sparse-mri/) and the [partial separability model](/partial-separability-model/): those methods ask for low rank in a space-time matrix of a dynamic series, while LORAKS asks for low rank in a structured matrix of one k-space.

## In plain words

Look at a small window of k-space, a few neighboring samples. Slide the window over all of k-space and write each window as one row of a big table. If the image is empty outside some region, the rows are not independent: some fixed mix of the samples in a window gives zero in every window. So the table has fewer independent rows than columns. The same is true, with a different table, when the image phase changes slowly.

Now some samples are missing. LORAKS guesses them, builds the table, and replaces it by the nearest table with only $r$ independent rows. Then it reads the samples back out of that table, puts the measured samples back, and starts again. Each pass makes the table closer to low rank.

## The problem

The input is a grid of k-space samples $d$ with a 0/1 mask $M$ of the measured points, a neighborhood of $w$ integer offsets, a target rank $r$, a weight $\lambda > 0$ or the choice of exact data, and an iteration count $K$. The grid is in centered order: point $q$ holds the signed frequency $\kappa(q)$. The data come from the model $d = M F_u x + \text{noise}$ of the [MRI reconstruction problem](/mri-reconstruction-problem/), with the unitary DFT $F_u$ ($F_u^H F_u = I$) and one coil.

The operator $P$ maps a grid $k$ to the matrix $P(k)$ with one row for each center $c$ whose whole neighborhood lies in the grid, and one column for each offset $o_j$: $P(k)_{c, j} = k(c + o_j)$. This is the C matrix of Haldar. In 1D it is a Hankel-like matrix with one window per row; in 2D the neighborhood is the set of offsets in a disk. The adjoint $P^H$ adds each entry back onto its grid point, and $P^H P$ is the diagonal of the counts $D(q)$, the number of rows that hold $q$.

The output is a full grid $k$ that minimizes, as far as the method can,

$$J(k) = \|M k - d\|^2 + \lambda \sum_{j > r} \sigma_j\big(P(k)\big)^2,$$

or, with exact data, the tail sum alone over the grids with $k = d$ on the mask. The penalty is the squared distance from $P(k)$ to the set of matrices of rank at most $r$ (equation (5) of the USC-SIPI report). The image is $F_u^H k$.

## The algorithm

The method is majorize-minimize. At the current $k$, the distance to rank $r$ is at most $\|P(k) - L\|_F^2$ for the best rank $r$ matrix $L$ of the current iterate. The new $k$ minimizes this upper bound plus the data term. Because $P^H P$ is diagonal, the minimizer is one division per grid point.

```pseudo id=main
LORAKS(d, M, offsets, r, lambda, K)   ▷ lambda = none keeps the data exactly
L1  k <- M d                          ▷ zero filled start
L2  repeat K times
L3      C <- P(k)                     ▷ one row per neighborhood
L4      L <- best rank r approximation of C (truncated SVD)
L5      z <- P^H(L)                   ▷ add the entries back onto the grid
L6      for each grid point q do
L7          if lambda = none: k(q) <- d(q) if M(q) = 1, else z(q) / D(q)
L8          else: k(q) <- (M(q) d(q) + lambda z(q)) / (M(q) + lambda D(q))
L9  return k
```

Line L4 is the truncated SVD of $C$. The code works with the $w \times w$ Gram matrix $C^H C$, because $w$ is small and the number of rows is large. A point with $D(q) = 0$ and $M(q) = 0$ lies in no neighborhood and has no sample; the code sets it to 0.

## Example

Take a 1D line of $n = 32$ pixels with three nonzero pixels: $x_5 = 1$, $x_6 = 0.7 - 0.3i$ and $x_{20} = -0.5 + 0.2i$. Its k-space $F_u x$ has 32 samples at the frequencies $-16, \ldots, 15$. With the neighborhood of radius 4 ($w = 9$ offsets), $P(F_u x)$ is a $24 \times 9$ matrix. Its singular values are

| $\sigma_1$ | $\sigma_2$ | $\sigma_3$ | $\sigma_4, \ldots, \sigma_9$ |
|---|---|---|---|
| 3.58 | 1.408 | 0.6427 | below $5 \times 10^{-8}$ |

The squares of the last six are at the rounding level $10^{-15}$, so the rank is 3, the number of nonzero pixels, as the rank bound below says.

Now keep 16 of the 32 samples ($R = 2$): the frequencies $-16, -13, -8, -7, -3, -2, -1, 0, 1, 2, 5, 8, 9, 12, 13, 15$. Zero filling has a relative error of 0.688. LORAKS with $r = 3$ and exact data gives these values (measured with the code below):

| iterations $i$ | $J(k_{i-1})$ | relative error of $k_i$ |
|---|---|---|
| 1 | 2.672 | 0.517 |
| 2 | 1.411 | 0.340 |
| 5 | 0.0798 | 0.128 |
| 10 | 0.00395 | 0.0421 |
| 20 | $7.2 \times 10^{-5}$ | 0.00598 |
| 50 | $7.8 \times 10^{-10}$ | $2.0 \times 10^{-5}$ |
| 100 | 0 (rounding) | $1.4 \times 10^{-9}$ |
| 150 | 0 (rounding) | $1.0 \times 10^{-13}$ |

$J$ falls at every step, as the proof says. Here the iterates also reach the true k-space, but that is a measurement on this example, not a theorem. With $r = 2$ the error stops at 0.21, and with $r = 4$ it is 0.0029 after 150 iterations. With only 11 samples (another random mask), the error stays between 0.6 and 0.9 for the radii 3, 4 and 5, close to the zero filled error of 0.80.

## Correctness

Two results hold, and both are proved in full below.

- **Rank bound.** If the image has $s$ nonzero pixels, then $\operatorname{rank} P(F_u x) \le \min(s, w)$. More exactly, $P(F_u x) = A \operatorname{diag}(x_S) B^T$, where $B$ is the $w \times s$ matrix of the neighborhood exponentials on the support. Every filter $h$ on the neighborhood whose image-domain function vanishes on the support is in the null space. This is the annihilating filter of [Prony's method](/prony-method/) in a new form.
- **Monotone objective.** With $\lambda > 0$, $J(k_{i+1}) \le J(k_i)$ at every pass. With exact data, the tail sum does not increase. The proof uses the Eckart-Young theorem: the best rank $r$ matrix gives a surrogate that touches $J$ at $k_i$ and lies above it elsewhere, and line L8 minimizes the surrogate exactly.

The rank penalty is not convex. So the theorems give a non-increasing sequence $J(k_i)$, not a global minimizer and not recovery of the true k-space. For a real image whose support has positive area, the rank deficiency is only approximate (Haldar and Setsompop 2020), which is why the method penalizes the tail and does not force an exact rank.

## Complexity

Let $n$ be the number of grid points, $w$ the size of the neighborhood and $N \le n$ the number of rows of $P(k)$. One pass costs:

- $O(N w)$ to build $P(k)$ (line L3) and to scatter $L$ back (line L5).
- $O(N w^2)$ to form the Gram matrix $C^H C$ and the product $C V_r V_r^H$ (line L4).
- $O(w^3)$ for the eigendecomposition of the Gram matrix with a dense solver. The code uses the cyclic Jacobi method on a $2w \times 2w$ real matrix, with $O(w^3)$ work per sweep and a number of sweeps that is small in practice but not bounded here.
- $O(n)$ for the update (lines L6 to L8).

So $K$ passes take $O(K (n w^2 + w^3))$ in the [real RAM](/real-ram/), and the space is $O(n w)$ for $P(k)$. No bound on $K$ in terms of the accuracy is known for this non-convex method; the number of passes is a measured quantity. Real implementations use larger neighborhoods (in 2D, a disk of radius 3 has 29 offsets), several coils and FFT-based products with $P$ and $P^H$.

## Properties

- **Calibrationless.** LORAKS needs no fully sampled k-space center and no coil maps. The structure comes from the image support and phase.
- **No sparsifying transform.** The prior is a rank condition on k-space, not a sparse representation of the image.
- **Monotone but non-convex.** The objective does not increase, but the limit depends on the start and on $r$.
- **Local in k-space.** The neighborhood is small, so the method can fill gaps that are a few samples wide, but not a large missing block far from any measured sample.

## Variants and improvements

- **G and S matrices.** Haldar also builds matrices from each neighborhood together with its mirror neighborhood at the negative frequencies. If the image is $\rho e^{i \varphi}$ with a real $\rho$ and a smooth phase $\varphi$, then $\bar x = x e^{-2 i \varphi}$, so the conjugate mirrored k-space is the k-space convolved with a short kernel. This gives linear relations between a neighborhood and its mirror, and so low rank. The S matrix uses the real and imaginary parts of these pairs. Smooth phase is the same prior that [homodyne reconstruction](/homodyne-reconstruction/) and [partial Fourier reconstruction](/partial-fourier-reconstruction/) use, and LORAKS can use it with partial Fourier sampling.
- **P-LORAKS.** With several coils, the neighborhoods of all coils go into one row. Coil sensitivities add more linear relations, as in [SPIRiT](/spirit/) and [ESPIRiT](/espirit/), but no calibration region is needed (Haldar and Zhuo 2016).
- **Other structured low rank methods.** Methods such as SAKE and ALOHA use the same idea with block Hankel matrices and other priors; Jacob, Mani and Ye (2020) survey them. The common root is the annihilating filter and linear prediction (see [linear prediction](/linear-prediction/)).
- **Convex relaxations.** One can replace the tail penalty by the nuclear norm of $P(k)$ and solve a convex problem with singular value thresholding, as in [matrix completion](/matrix-completion/). The tail penalty fits the rank better but gives up convexity.

## When to use it

Use LORAKS when the data lack a fully sampled calibration region, when the sampling is unusual (partial Fourier, random, or with gaps), or when the image support is small compared to the field of view. Use it with a sparsity prior when the image is also compressible. For standard Cartesian scans with a good calibration region, [GRAPPA](/grappa/) or [SENSE](/sense/) is faster and simpler.

## Pitfalls

- **The rank $r$ is a choice.** In the example, $r = 2$ fails and $r = 4$ converges slowly. For real data the singular values decay without a clear gap, and $r$ and $\lambda$ are tuned.
- **The neighborhood size.** A larger neighborhood has more annihilating filters but fewer rows and a higher cost. The rank bound is useful only when $r$ is well below $w$.
- **Too few samples.** Recovery is measured, not proved. In the example, 11 of 32 samples fail for every neighborhood tried.
- **Edges of the grid.** Points near the edge lie in few rows, so $D(q)$ is small there and the update is weak. A point in no row and with no sample stays at 0.
- **Complex SVD.** A real SVD of the real and imaginary parts as separate columns is not the complex SVD. The code embeds the complex Gram matrix as a real symmetric matrix of twice the size, where each eigenvalue appears twice.
- **Slow convergence with a penalty.** With $\lambda > 0$ the data term pulls each sample only part of the way. On the example above with $\lambda = 1$, the relative error is still 0.42 after 150 passes, while exact data give $10^{-13}$.

## Implementations

## History

Justin Haldar introduced LORAKS in 2014 in IEEE Transactions on Medical Imaging, with a technical report and code for reproducible research. The idea joins two older lines. One is the annihilating filter and linear prediction of signals with few components, which goes back to Prony. The other is the use of support and smooth phase constraints in MRI, as in partial Fourier methods. In 2016 Haldar and Zhuo extended the method to multichannel data as P-LORAKS. Haldar and Setsompop (2020) and Jacob, Mani and Ye (2020) later placed LORAKS among the structured low rank methods for MRI.

## References
