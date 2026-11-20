---
tag: PHV9XM
kind: algorithm
slug: fast-gauss-transform
name: Fast Gauss transform
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Evaluates sums of N Gaussians at M targets in O(N + M) time by Hermite and Taylor expansions on a grid of boxes.
model: real-ram
complexity:
  vars: {N: the number of sources, M: the number of targets, p: the number of terms in each coordinate, n: the range in boxes, b: the number of nonempty boxes}
  time: {best: "Θ((N + M) p^2)", average: "Θ((N + M) p^2 + b n^2 p^3)", worst: "O((N + M) p^2 + b n^2 p^3)"}
  space: {extra: "Θ(N + M + b p^2)"}
properties: {deterministic: true}
history:
  year: 1991
  people: [Leslie Greengard, John Strain]
  note: Greengard and Strain published the fast Gauss transform in the SIAM Journal on Scientific and Statistical Computing in 1991.
prereqs: [fast-multipole-method, orthogonal-polynomials]
see_also: [kernel-density-estimation, gaussian-process, heat-equation, gaussian-filter, mean-shift, radial-basis-function-interpolation, black-box-fast-multipole-method, kd-tree]
sources:
  - paper: doi:10.1137/0912004
    title: "Leslie Greengard and John Strain, The fast Gauss transform, SIAM Journal on Scientific and Statistical Computing 12(1), 1991, 79-94"
    locator: "Section 2, the Hermite and Taylor expansions and Cramér's inequality; Section 3, the boxes of side r√(2δ), the range of (2n + 1)^d boxes and the four ways with the cutoffs N_F and M_L; Section 4, the formal algorithm; Section 5, the 2D experiments"
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: Section 3, the fast Gauss transform for the heat kernel, with boxes of side √T and Hermite expansions
  - paper: doi:10.1137/S1064827501396920
    title: "Brad J. C. Baxter and George Roussos, A new error estimate of the fast Gauss transform, SIAM Journal on Scientific Computing, 2002"
    locator: the correction of the error estimate of Lemma 2.1 of Greengard and Strain
  - paper: doi:10.1109/ICCV.2003.1238383
    title: "Changjiang Yang, Ramani Duraiswami, Nail A. Gumerov and Larry Davis, Improved fast Gauss transform and efficient kernel density estimation, Proceedings of the Ninth IEEE International Conference on Computer Vision, 2003, 664-671"
    locator: the improved fast Gauss transform for higher dimensions
---

The fast Gauss transform (FGT) evaluates the discrete Gauss transform

$$G(t_i) = \sum_{j=1}^{N} q_j \, e^{-|t_i - s_j|^2 / \delta}, \qquad i = 1, \ldots, M,$$

in work proportional to $N + M$, with a constant that depends only on the dimension and the precision. Direct evaluation costs $NM$ kernel evaluations. The method puts the points in a grid of boxes of side proportional to $\sqrt{\delta}$. Because the Gaussian decays fast, only boxes within a fixed range interact. For those, the Gaussians of a source box are collected into one Hermite expansion, and the field in a target box is collected into one Taylor expansion. Greengard and Strain (1991) gave the method for sums that come from the heat equation, vortex methods and statistics, and the same sums appear in [kernel density estimation](/kernel-density-estimation/) and [Gaussian processes](/gaussian-process/).

## In plain words

Each source spreads a bump around it. The bump is wide about the square root of the given width, and it is almost zero farther away. You want the total height of all bumps at many targets.

Cut the square into small boxes. A box only feels boxes a few steps away, so far boxes are skipped. For a near box with many sources, replace all its bumps by one short sum of fixed shapes centred at the box. For a target box with many targets, collect everything it receives into one short polynomial about its centre, and then read each target from that polynomial. Boxes with few points simply add bump by bump.

Every step then costs a fixed amount per point and per pair of boxes, so the total grows like the number of points.

## The problem

The input is $N$ sources $s_j$ with weights $q_j$, $M$ targets $t_i$, all in the unit square, a width $\delta > 0$, a number $p$ of terms in each coordinate and a range $n$. The output is an approximation of every $G(t_i)$, with an error at most a fixed small multiple of $Q = \sum_j |q_j|$.

## The algorithm

Scale every coordinate by $1 / \sqrt{\delta}$, so the kernel is $e^{-|x - y|^2}$. Let $h_k(x) = (-1)^k \frac{d^k}{dx^k} e^{-x^2}$ be the Hermite functions, computed by $h_{k+1} = 2x h_k - 2k h_{k-1}$, and use the multi-index notation $\alpha = (\alpha_1, \alpha_2)$, $\alpha! = \alpha_1! \, \alpha_2!$ and $h_\alpha(x) = h_{\alpha_1}(x_1) h_{\alpha_2}(x_2)$. For a source $y$ near a center $c$ and a target $x$ near a center $c'$, the Hermite and Taylor expansions are

$$e^{-|x - y|^2} = \sum_{\alpha} \frac{(y - c)^\alpha}{\alpha!} h_\alpha(x - c) = \sum_{\beta} \frac{(x - c')^\beta}{\beta!} h_\beta(y - c').$$

Cut the square into boxes of side $\sqrt{\delta} / 2$. A source box $B$ is big if it has more than $N_F$ sources, and a target box $C$ is big if it has more than $M_L$ targets. Each target box looks at the source boxes at most $n$ boxes away in each coordinate.

```pseudo id=main
FGT(q, s, t, δ, p, n)
L1  for each big source box B: A_B(α) ← Σ_{j in B} q_j (s_j - c_B)^α / α!, for α_1, α_2 < p
    for each target box C and each source box B at most n boxes away do
L2      if B and C are small: G(t_i) += Σ_{j in B} q_j e^{-|t_i - s_j|^2} for each t_i in C
L3      if B is small and C is big: T_C(β) += Σ_{j in B} q_j h_β(s_j - c_C) / β!
L4      if B is big and C is small: G(t_i) += Σ_α A_B(α) h_α(t_i - c_B) for each t_i in C
L5      if B and C are big: T_C(β) += ((-1)^{|β|} / β!) Σ_α A_B(α) h_{α+β}(c_C - c_B)
L6  for each big target box C and t_i in C: G(t_i) += Σ_β T_C(β) (t_i - c_C)^β
L7  return G
```

Line L5 converts a Hermite expansion into a Taylor expansion. Since $h_{\alpha + \beta}(w) = h_{\alpha_1 + \beta_1}(w_1) \, h_{\alpha_2 + \beta_2}(w_2)$, it is done one coordinate at a time in $O(p^3)$ operations instead of $O(p^4)$. Greengard and Strain take $N_F$ and $M_L$ of order $p^{d-1}$ in dimension $d$, which balances the four kinds of work; the code takes $N_F = M_L = p$. Their boxes have side $r \sqrt{2\delta}$ with $r \le \frac12$; this page uses $r = 1 / (2\sqrt{2})$, the side $\sqrt{T}$ of the short course of Beatson and Greengard for the heat kernel $e^{-|x|^2 / 4T}$.

## Example

Take $N = M = 300$ sources and targets uniform in the unit square, weights uniform in $[0, 1]$ (seed 11), and $\delta = 0.16$. The boxes have side $0.2$, so there are 25 boxes and, with $n = 8$, all 625 pairs interact. Forcing one of the three expansion methods for all pairs gives the largest error divided by $Q$:

| $p$ | sources to Taylor (L3) | Hermite to targets (L4) | Hermite to Taylor (L5) | bound of the proof |
|---|---|---|---|---|
| 2 | $1.2 \times 10^{-2}$ | $6.6 \times 10^{-3}$ | $1.9 \times 10^{-2}$ | $2.7$ |
| 4 | $1.5 \times 10^{-4}$ | $7.8 \times 10^{-5}$ | $2.1 \times 10^{-4}$ | $1.3 \times 10^{-1}$ |
| 6 | $3.0 \times 10^{-6}$ | $1.3 \times 10^{-6}$ | $3.4 \times 10^{-6}$ | $5.4 \times 10^{-3}$ |
| 8 | $4.9 \times 10^{-8}$ | $1.8 \times 10^{-8}$ | $5.2 \times 10^{-8}$ | $1.8 \times 10^{-4}$ |
| 10 | $5.7 \times 10^{-10}$ | $2.1 \times 10^{-10}$ | $5.8 \times 10^{-10}$ | $4.7 \times 10^{-6}$ |
| 12 | $5.3 \times 10^{-12}$ | $2.1 \times 10^{-12}$ | $5.3 \times 10^{-12}$ | $2.1 \times 10^{-7}$ |

These are measurements, and the last column is the bound $2\varepsilon_p + \varepsilon_p^2$ of the proof. Each two more terms give about two more digits. With the cutoffs $N_F = M_L = 8$ and $p = 8$, the code uses all four ways: 6 pairs direct, 44 sources to Taylor, 69 Hermite to targets and 506 Hermite to Taylor, with the error $5.2 \times 10^{-8} Q$.

The range matters when the boxes are small. With $\delta = 0.01$ there are $20 \times 20$ boxes, and with all pairs direct, the error divided by $Q$ for the ranges $n = 1, \ldots, 6$ is $2.4 \times 10^{-2}$, $8.9 \times 10^{-3}$, $1.8 \times 10^{-3}$, $2.4 \times 10^{-4}$, $2.9 \times 10^{-5}$ and $1.2 \times 10^{-6}$, below the bounds $e^{-n^2/4}$, which are $0.78$, $0.37$, $0.11$, $1.8 \times 10^{-2}$, $1.9 \times 10^{-3}$ and $1.2 \times 10^{-4}$.

## Correctness

The proof file proves the bound $|\tilde G(t_i) - G(t_i)| \le Q (2\varepsilon_p + \varepsilon_p^2 + e^{-n^2/4})$. In each coordinate, the Gaussian for one source and one target is a double series in the offset of the source from its center and the offset of the target from its center, and the four ways compute partial sums of it: all terms, the Hermite part ($m < p$), the Taylor part ($n < p$) or both. Cramér's inequality $|H_k(z)| \le K 2^{k/2} \sqrt{k!} \, e^{z^2/2}$, with $K < 1.09$, and $(m + n)! \le 2^{m+n} m! \, n!$ bound the omitted terms by $\varepsilon_p = 2 K C_0 \sum_{k \ge p} 2^{-k} / \sqrt{k!}$, because the offsets are at most $\frac14$. A product of two such factors has the error at most $2\varepsilon_p + \varepsilon_p^2$. Sources in skipped boxes are at least $n / 2$ away in the scaled coordinates, so they contribute at most $e^{-n^2/4}$ each. The original error estimate of Greengard and Strain for Hermite expansions was later corrected by Baxter and Roussos; the bound here is derived directly and does not use it.

## Complexity

The model is the [real RAM](/real-ram/), with $e^x$ counted as one operation.

- **Linear work (theorem).** Line L1 costs $O(p^2)$ per source and line L6 $O(p^2)$ per target. With $N_F = M_L = p$, every pair of boxes costs $O(p^3)$: a direct pair has at most $p^2$ kernel evaluations, the pairs of lines L3 and L4 at most $p \cdot p^2$, and line L5 is $O(p^3)$ by the product form. There are at most $b (2n + 1)^2$ pairs, so the total is $O((N + M) p^2 + b n^2 p^3)$, and $b$ is at most $N + M$ and at most the number of boxes, $\lceil 2 / \sqrt{\delta} \rceil^2$.
- **Constant set by the precision.** For a fixed error, $p$ and $n$ are fixed, so the work is $O(N + M)$. Greengard and Strain report, for their 2D Fortran code with $p^2 = 8^2$ terms and $\delta = 1$, a time of 205 seconds for $N = M = 102400$ uniform points, against an estimated 622780 seconds for direct evaluation, and more than 3000 times faster than direct evaluation for 102400 points on a circle with $\delta = 0.01$.
- **Dimension.** In $d$ dimensions the expansions have $p^d$ terms and the range has $(2n + 1)^d$ boxes, so the constant grows exponentially with $d$; this is the limit that the improved FGT addresses.
- **Space.** $\Theta(N + M)$ for the points and $\Theta(b p^2)$ for the expansions.

## Properties

- **No tree.** The boxes form one flat grid, because the Gaussian has a fixed width; unlike the [fast multipole method](/fast-multipole-method/), there is no hierarchy.
- **Error relative to the total weight.** The bound is a multiple of $Q$, not of $|G(t_i)|$. Where the field is small compared with $Q$, the relative error can be large.
- **Independent of the distribution.** The error bound does not depend on the positions. The work is smallest when the points are clustered into few boxes.
- **Linear in the weights.** The output is a linear function of $q$, so the method is a fast product with the matrix $[e^{-|t_i - s_j|^2 / \delta}]$.
- **Deterministic.** The result does not depend on the order of the points, up to rounding.

## Variants and improvements

- **Improved FGT.** Yang, Duraiswami, Gumerov and Davis (2003) use a multivariate Taylor expansion with terms of total degree below $p$, about $\binom{p + d - 1}{d}$ instead of $p^d$, and cluster the sources with farthest point clustering instead of a grid, which makes the method usable in more dimensions.
- **New versions of the FGT.** Later versions of Greengard and coworkers replace the Hermite expansions by plane wave (Fourier) expansions, which diagonalize the translations, and add adaptive trees for sources spread over many scales.
- **Variable widths.** Strain extended the method to Gaussians whose width changes from source to source.
- **Heat equation solvers.** The FGT evaluates heat potentials in integral equation methods for the [heat equation](/heat-equation/).
- **Tree codes for Gaussians.** For high dimensions and small widths, dual tree methods on a [k-d tree](/kd-tree/) prune far pairs with error bounds.

## When to use it

Use the FGT for sums of Gaussians with one width in two or three dimensions, with many sources and targets: [kernel density estimation](/kernel-density-estimation/), [mean shift](/mean-shift/) clustering, Gaussian [radial basis functions](/radial-basis-function-interpolation/), Gaussian process regression with a squared exponential kernel, and heat potentials. If the width is so small that each target sees only a few sources, a grid of cells with direct sums is enough. If the width is so large that the Gaussian is nearly constant, a few Taylor terms over one box are enough. In more than three or four dimensions, use the improved FGT or a tree method.

## Pitfalls

- **Wrong scaling.** The expansions use the offsets divided by $\sqrt{\delta}$. Forgetting the scaling, or using boxes much larger than $\sqrt{\delta}$, makes the offsets large and the series converge slowly or not at all in floating point.
- **Error relative to Q.** If the weights have mixed signs and cancel, the error bound in terms of $Q = \sum |q_j|$ can be much larger than the result.
- **Range too small.** The cutoff error is about $e^{-n^2/4}$ in the scaled units of this page. For the same precision, smaller boxes need a larger $n$.
- **Too many terms in many dimensions.** In $d$ dimensions the tensor expansions have $p^d$ terms; for $d \ge 4$ the method can be slower than direct evaluation.
- **Old error formula.** The error estimate in Lemma 2.1 of the 1991 paper was shown to be wrong by Baxter and Roussos. Use a corrected bound, such as the one in the proof file, when you choose $p$.

## Implementations

## History

Greengard and Strain (1991) gave the fast Gauss transform: Hermite and Taylor expansions in $d$ dimensions, a grid of boxes of side proportional to $\sqrt{\delta}$, four ways for a pair of boxes chosen by the cutoffs $N_F$ and $M_L$, and 2D experiments with up to about 100000 sources and targets. Beatson and Greengard (1997) presented it for the heat kernel in their short course on fast multipole methods. Baxter and Roussos (2002) showed that the error estimate of Lemma 2.1 of the original paper is wrong and gave a new one. Yang, Duraiswami, Gumerov and Davis (2003) gave the improved FGT for kernel density estimation in higher dimensions.

## References
