---
tag: GT011W
kind: algorithm
slug: backus-gilbert-method
name: Backus-Gilbert method
aliases:
- method of optimally localized averages
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Estimate local averages of the unknown with averaging kernels that are as narrow as possible under a bound on the noise amplification.
solves: [fredholm-integral-equation-first-kind]
model: real-ram
complexity:
  vars: {m: "the number of data values", q: "the number of quadrature nodes", r: "the number of estimation points"}
  time: {per_point: "O(m^2 q + m^3)", total: "O(r (m^2 q + m^3))"}
  space: {extra: "O(m^2)"}
properties: {deterministic: true, iterative: false, linear_in_data: true, weights_depend_on_point: true, trade_off_parameter: "mu (spread against noise variance)", output: "an estimate and its averaging kernel at each point"}
history:
  year: 1967
  people: [G. Backus, F. Gilbert]
  note: Backus and Gilbert developed the method in a series of papers from 1967 to 1970 to find out what gross Earth data can resolve about the interior of the Earth.
prereqs: [fredholm-integral-equation-first-kind, regularization-method, resolution-matrix]
see_also: [approximate-inverse, tikhonov-regularization, truncated-svd, point-spread-function, bias-variance-tradeoff, quadratic-programming, morozov-discrepancy-principle, singular-value-expansion]
sources:
  - paper: "G. Backus and F. Gilbert, Numerical applications of a formalism for geophysical inverse problems, Geophysical Journal of the Royal Astronomical Society 13, 1967, 247 to 276"
    locator: the formalism of averaging kernels for finite data (general locator)
  - paper: "G. Backus and F. Gilbert, The resolving power of gross Earth data, Geophysical Journal of the Royal Astronomical Society 16, 1968, 169 to 205"
    locator: the spread criterion and optimally localized averaging kernels (general locator)
  - paper: "G. Backus and F. Gilbert, Uniqueness in the inversion of inaccurate gross Earth data, Philosophical Transactions of the Royal Society of London A 266, 1970, 123 to 192"
    locator: the trade-off between resolution and error for noisy data (general locator)
---

The Backus-Gilbert method estimates local averages of an unknown function $x(t)$ from finitely many noisy linear data
$$d_i = \int G_i(t)\,x(t)\,dt + n_i, \qquad i = 1, \dots, m,$$
with noise covariance $C$. For each point $p$ it looks for weights $a = a(p)$ and reports $\hat x(p) = \sum_i a_i d_i$. For exact data this estimate is $\int K_p(t)\,x(t)\,dt$, an average of $x$ with the averaging kernel $K_p = \sum_i a_i G_i$. The method chooses $a$ so that $K_p$ has unit area and is as concentrated near $p$ as the data allow, while the noise variance $a^\top C a$ of the estimate stays small. With the spread $s(a) = 12\int (t - p)^2 K_p(t)^2\,dt$, which is a quadratic form $a^\top S(p)\, a$, it solves
$$\min_a \ a^\top \big(S(p) + \mu C\big)\, a \quad \text{subject to} \quad c^\top a = 1, \qquad c_i = \int G_i ,$$
and a Lagrange multiplier gives $a = W^{-1} c / (c^\top W^{-1} c)$ with $W = S(p) + \mu C$. The parameter $\mu \ge 0$ trades resolution (a small spread) against stability (a small variance). Unlike most regularization methods, it reports with each estimate the averaging kernel that the estimate really is, so the user sees the resolution at every point.

## In plain words

With a finite number of noisy measurements you cannot know the unknown function at a point. You can only know weighted averages of it. The Backus-Gilbert method asks, for each point, which combination of the measurements gives an average that is concentrated as closely as possible around that point. A very sharp average needs large weights of both signs, and these amplify the noise. So the method finds the sharpest average whose noise is still acceptable. It returns both the value and the shape of the average, so you know how much detail the value really contains.

## The problem

Given data kernels $G_1, \dots, G_m$ on an interval (in the code, sampled at quadrature nodes $t_k$ with weights $w_k$), data $d \in \mathbb{R}^m$, a symmetric positive semidefinite noise covariance $C$, a parameter $\mu \ge 0$, and points $p_1, \dots, p_r$, compute for each $p$ the weights $a(p)$ that minimize $a^\top (S(p) + \mu C)\, a$ under $\sum_i a_i \int G_i = 1$, and the estimate $\hat x(p) = a(p)^\top d$.

## The algorithm

```pseudo id=main
BACKUS-GILBERT(G₁…G_m, d, C, points P, μ)         ▷ μ ≥ 0, cᵢ = ∫ Gᵢ
L1  for each point p in P do
L2      S_ij ← 12 ∫ (t - p)² Gᵢ(t) Gⱼ(t) dt      for i, j = 1, …, m
L3      W ← S + μ C
L4      solve W z = c
L5      a ← z / (cᵀ z)
L6      x̂(p) ← aᵀ d
L7  return (x̂(p) for p in P)
```

Line L1 treats each point on its own; the weights depend on $p$ through the spread matrix. Line L2 computes the spread matrix by the quadrature rule. The factor 12 is chosen so that a box of width $w$ centered at $p$ (height $1/w$) has spread exactly $w$, so the spread reads as a width. Line L3 adds the weighted noise covariance. Lines L4 and L5 solve the constrained problem in closed form: $a$ is proportional to $W^{-1} c$, scaled to unit area. Line L6 applies the weights to the data, and line L7 returns all estimates. The averaging kernel $K_p = \sum_i a_i G_i$ and the variance $a^\top C a$ come with no extra solve and should be reported too.

## Example

**Ten data kernels.** Take $m = 10$ Gaussian kernels $G_i(t) = \exp(-\tfrac12((t - t_i)/0.08)^2)/(0.08\sqrt{2\pi})$ on $[0, 1]$ with centers $t_i = (i - 0.5)/10$, white noise ($C = I$), and the midpoint rule with $400$ nodes. One kernel alone, used at its own center, has spread $3 \cdot 0.08/\sqrt\pi = 0.1354$. At $p = 0.5$, halfway between two centers, with $\mu = 10^{-2}$, the method gives the weights
$$a = (0.030, -0.054, 0.153, -0.272, 0.648, 0.648, -0.272, 0.153, -0.054, 0.030)$$
and spread $0.1300$. The weights alternate in sign: the negative sidelobes of the neighbors make the kernel narrower than one data kernel, at the price of a noise factor $\sqrt{a^\top a} = 1.02$.

**The trade-off.** Now take $m = 20$ such kernels (centers $(i - 0.5)/20$, the same width), so neighbors overlap strongly and the problem is ill-conditioned. Let $x(t) = \sin(\pi t) + 0.5t$, with $x(0.5) = 1.25$, add white noise with standard deviation $\sigma = 0.001$ (`random.Random(7)`), keep $C = I$, and estimate at $p = 0.5$. The noise column is the standard deviation $\sigma\sqrt{a^\top a}$ of the estimate.

| $\mu$ | spread | noise std of $\hat x$ | $\hat x$, exact data | $\hat x$, noisy data | error |
|---|---|---|---|---|---|
| $10^{-12}$ | 0.0655 | 0.380 | 1.2249 | 0.6995 | 0.5505 |
| $10^{-8}$ | 0.0657 | 0.326 | 1.2244 | 0.7705 | 0.4795 |
| $10^{-6}$ | 0.0733 | 0.0472 | 1.2209 | 1.1653 | 0.0847 |
| $10^{-4}$ | 0.0859 | 0.0067 | 1.2153 | 1.2161 | 0.0339 |
| $10^{-2}$ | 0.1108 | 0.0011 | 1.2028 | 1.2038 | 0.0462 |
| $1$ | 0.2055 | 0.00037 | 1.1402 | 1.1404 | 0.1096 |

As $\mu$ grows the spread grows and the noise falls, at every step. With exact data the estimate is exactly the average $\int K_p x$; it differs from $x(0.5) = 1.25$ because $x$ is curved on the scale of the spread. The best total error here is near $\mu = 10^{-4}$, where the kernel is $0.086$ wide and the noise is $0.0067$. Twenty kernels resolve $0.066$ at best, compared with $0.129$ for ten; more data buy resolution, but only with more noise amplification.

## Correctness

The proofs are in proofs/correctness.md, in exact arithmetic and with the same quadrature rule for every integral.

- **Optimal weights (theorem).** If $W = S(p) + \mu C$ is positive definite and $c \ne 0$, lines L4 and L5 give the unique minimizer of $a^\top W a$ under $c^\top a = 1$.
- **Unit area and exact averages (theorem).** The averaging kernel has $\int K_p = 1$, and for exact data $\hat x(p) = \int K_p\, x$. So constants are reproduced exactly.
- **Spread identity (lemma).** $a^\top S(p)\,a = 12 \int (t - p)^2 K_p(t)^2\,dt$.
- **Monotone trade-off (theorem).** As $\mu$ increases, the spread $a^\top S a$ does not decrease and the variance $a^\top C a$ does not increase.
- **Termination.** One linear solve per point; no data-dependent loop.

## Complexity

- **Per point.** Line L2 costs $O(m^2 q)$ with $q$ quadrature nodes, and the solve at line L4 costs $O(m^3)$. Lines L5 and L6 cost $O(m)$.
- **Total.** $O(r (m^2 q + m^3))$ for $r$ points, and $O(m^2)$ extra space. The products $G_i G_j$ can be computed once, so that each new $p$ needs only a weighted sum.
- **Comparison.** Tikhonov regularization solves one system for all points; Backus-Gilbert solves one per point. This is why it is used for problems with a modest number of data, as in geophysics and helioseismology, and why faster variants exist.

## Properties

- **Linear in the data.** For fixed $p$ and $\mu$, $\hat x(p) = a(p)^\top d$.
- **Self-describing resolution.** The output includes the averaging kernel $K_p$ and its spread, which are the rows of the [resolution matrix](/resolution-matrix/) in the continuous setting.
- **Unbiased for the average.** $E\,\hat x(p) = \int K_p\, x$ for zero-mean noise, whatever $x$ is. The bias with respect to $x(p)$ depends on how much $x$ varies over the width of $K_p$.
- **No prior on $x$.** The method uses no smoothness assumption on $x$ to compute the weights; it only describes what the data can resolve.
- **Trade-off curve.** Plotting spread against variance for all $\mu$ gives a monotone curve, the standard picture of the conflict between resolution and stability.

## Variants and improvements

- **Other spread functions.** Use $(t - p)^2$ in higher dimensions as $\|t - p\|^2$, or another weight that grows away from $p$; the algorithm is unchanged.
- **Subtractive optimally localized averages (SOLA).** Fit $K_p$ to a chosen target kernel (for example a Gaussian of a given width) in least squares, instead of minimizing the spread. The matrix of the system then does not depend on $p$, so it is factored once. Pijpers and Thompson introduced it for helioseismology.
- **Choice of $\mu$.** Pick $\mu$ so that the noise standard deviation reaches a target, or use the [discrepancy principle](/morozov-discrepancy-principle/) on the misfit of a model built from the estimates.
- **Fixed averaging kernels.** If the averaging kernel is chosen in advance and the weights are computed for it, the method becomes the [approximate inverse](/approximate-inverse/).

## When to use it

Use the Backus-Gilbert method when there are tens to a few hundred data, when the question is what the data can say about the unknown at each point, and when each estimate needs its own resolution and error bar. This is the typical situation in seismology, in helioseismic rotation inversions, and in other problems with sparse, integral data. When you need a full reconstruction on a fine grid from many data, [Tikhonov regularization](/tikhonov-regularization/) or [truncated SVD](/truncated-svd/) is much cheaper, and you can compute their averaging kernels afterwards from the resolution matrix.

## Pitfalls

- **$\mu = 0$ with close data kernels.** $S(p)$ is then nearly singular, the weights are huge with alternating signs, and the noise standard deviation reaches $0.380$ in the table, about fifteen times the smoothing error $0.025$. Always use $\mu > 0$ with noisy data.
- **Reading $\hat x(p)$ as a point value.** It is an average over a width of about the spread. Report the spread with the estimate.
- **Wrong noise covariance.** The trade-off uses $C$; a wrong scale of $C$ only rescales $\mu$, but a wrong correlation structure gives wrong error bars.
- **Points near the edge of the data coverage.** The averaging kernel cannot be centered there; it is lopsided and wider. Check $K_p$, not only the spread number.
- **Quadrature too coarse.** Line L2 needs a quadrature that resolves the products $G_i G_j$; otherwise the spread and the unit area are wrong.

## Implementations

## History

George Backus and Freeman Gilbert developed the method between 1967 and 1970 to find out what gross Earth data, such as the frequencies of free oscillations and the mass and moment of inertia of the Earth, can resolve about the density and elastic properties of the interior. Their papers introduced averaging kernels, the spread criterion and the trade-off curve between resolution and error. The method became a standard tool in seismology and helioseismology, and it influenced the later view of regularization in terms of resolution. The approximate inverse of Louis and Maass (1990) reverses the roles: the averaging kernel is fixed in advance and the weights follow from it.

## References
