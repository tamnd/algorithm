---
tag: YBFHVG
kind: algorithm
slug: fritsch-carlson-monotone-interpolation
name: Fritsch-Carlson monotone interpolation
aliases:
- Monotone cubic interpolation
- PCHIP
- monotone piecewise cubic Hermite interpolation
- shape-preserving cubic interpolation
area: numerical/interpolation-and-approximation
level: advanced
summary: Piecewise cubic Hermite interpolation whose node slopes are limited so that each piece is monotone wherever the data are. No overshoot, no spurious extrema, C1, O(n) setup.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {n: "the number of intervals, with n + 1 data points"}
  time: {setup: Θ(n), per_point: Θ(log n)}
  space: {extra: Θ(n)}
  flops: {setup: "20n", per_point: "22"}
properties: {deterministic: true, recursive: false, smoothness: C1, shape_preserving: monotone}
history:
  year: 1980
  people: [Frederick N. Fritsch, Ralph E. Carlson, Judy Butland, Carl de Boor, Blair Swartz]
  note: Fritsch and Carlson (1980) found the exact region of slopes for which a cubic Hermite piece is monotone and gave the slope limiting algorithm; Fritsch put it in the PCHIP package (1982), and Fritsch and Butland (1984) added the harmonic mean slopes used by MATLAB and SciPy.
prereqs: [cubic-hermite-spline]
see_also: [cubic-spline-interpolation, piecewise-linear-interpolation, hermite-interpolation, catmull-rom-spline, smoothing-spline, spline, binary-search, interpolation-problem]
sources:
  - paper: doi:10.1137/0717021
    title: "F. N. Fritsch and R. E. Carlson, Monotone piecewise cubic interpolation, SIAM Journal on Numerical Analysis 17(2) (1980) 238-246"
    locator: the necessary and sufficient conditions for a monotone cubic Hermite piece, the figure of the region, and the slope limiting algorithm
  - paper: doi:10.1137/0905021
    title: "F. N. Fritsch and J. Butland, A method for constructing local monotone piecewise cubic interpolants, SIAM Journal on Scientific and Statistical Computing 5(2) (1984) 300-304"
    locator: the weighted harmonic mean slope formula
  - paper: "Carl de Boor and Blair Swartz, Piecewise monotone interpolation, Journal of Approximation Theory 21 (1977) 411-416"
    locator: the sufficient condition 0 <= d/delta <= 3 and its consequences for accuracy
  - book: isbn:9780898715606
    title: Cleve B. Moler, Numerical Computing with MATLAB, SIAM, 2004
    locator: Chapter 3, Interpolation (Section 3.4, the shape-preserving piecewise cubic pchip and its end slopes)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IV, Piecewise cubic interpolation (cubic Hermite pieces, slope choices and shape preservation)
  - paper: "James M. Hyman, Accurate monotonicity preserving cubic interpolation, SIAM Journal on Scientific and Statistical Computing 4(4) (1983) 645-654"
    locator: limiting higher-order slope estimates to keep monotonicity
---

Fritsch-Carlson monotone interpolation fits a piecewise cubic Hermite interpolant through data $(x_k, y_k)$ and chooses the node slopes so that the curve rises wherever the data rise, falls wherever they fall and is flat wherever they are flat. Ordinary cubic splines overshoot near steep steps and can produce negative concentrations or decreasing cumulative distributions from monotone data. Fritsch and Carlson found the exact condition on the two end slopes for a cubic piece to be monotone. The algorithm starts from ordinary three-point slopes and scales any pair that falls outside a disk of radius 3 (in units of the secant slope). The result is $C^1$, local, built in $O(n)$ operations and free of spurious extrema. It is the method behind the PCHIP family of routines.

## In plain words

You have points that only go up, like a cumulative total, and you want a smooth curve through them. A standard smooth curve fit can dip down between two points before a big jump, or shoot above the last point, which is wrong for data that are known never to decrease. This method draws each piece between two neighboring points as a cubic, and chooses how steep the curve is at every point with care. It first takes a natural guess for the steepness. If the guess is so steep that the piece would bend back, it scales the steepness down until the piece is monotone. Where the data have a peak or a valley, the curve is made flat at that point, so it never invents a new peak.

## The problem

The input is data $(x_k, y_k)$, $k = 0, \ldots, n$, with distinct abscissas (the implementation sorts them). The output is a function $s$ on $[x_0, x_n]$ with:

- $s(x_k) = y_k$, and $s$ is a cubic polynomial on each $[x_k, x_{k+1}]$, with $s \in C^1$;
- *shape preservation*: on every interval where $y_{k+1} > y_k$, $s$ is nondecreasing; where $y_{k+1} < y_k$, nonincreasing; where $y_{k+1} = y_k$, constant. So $s$ is monotone on any run of monotone data, and $s$ stays between $y_k$ and $y_{k+1}$ on each interval.

Notation: $h_k = x_{k+1} - x_k$, the secant slope $\delta_k = (y_{k+1} - y_k)/h_k$ (a first [divided difference](/divided-differences/)), node slopes $d_k = s'(x_k)$, and for an interval with $\delta_k \ne 0$ the ratios $\alpha_k = d_k/\delta_k$ and $\beta_k = d_{k+1}/\delta_k$. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

```pseudo id=main
MONOTONE-CUBIC(x[0..n], y[0..n])                ▷ x sorted and distinct, n ≥ 1
L1  for k ← 0 to n − 1: h[k] ← x[k+1] − x[k];  δ[k] ← (y[k+1] − y[k])/h[k]
L2  d[k] ← three-point slope (h[k]δ[k−1] + h[k−1]δ[k])/(h[k−1] + h[k]) if δ[k−1]δ[k] > 0, else 0
        for 0 < k < n; end slopes by the one-sided three-point formula, set to 0 if their
        sign differs from the adjacent secant (n = 1: d[0] = d[1] = δ[0])
L3  for k ← 0 to n − 1: if δ[k] = 0: d[k] ← 0; d[k+1] ← 0; continue
L4      r ← hypot(d[k], d[k+1]);  if r > 3|δ[k]|: τ ← 3|δ[k]|/r;  d[k] ← τ·d[k];  d[k+1] ← τ·d[k+1]
EVAL(t)
L5  k ← the interval with x[k] ≤ t ≤ x[k+1] (binary search);  u ← (t − x[k])/h[k];  v ← 1 − u
L6  return y[k]v²(1 + 2u) + y[k+1]u²(1 + 2v) + h[k](d[k]uv² − d[k+1]u²v)
```

Line L4 is Fritsch and Carlson's step: if the point $(\alpha_k, \beta_k)$ lies outside the disk of radius 3, it is pulled back radially onto the circle. It is written with $d_k$ and $\delta_k$ instead of $\alpha_k$ and $\beta_k$ so that a tiny secant cannot overflow the ratios. Because the scaling only shrinks slopes, a slope reduced while processing interval $k$ cannot push interval $k - 1$ back out of the disk, so one left-to-right pass suffices. The end slopes in L2 follow Moler's `pchip`: also set to $3\delta$ when the one-sided formula exceeds three times the secant next to a change of direction.

## Example

Data with a step: $x = 0, 1, 2, 3, 4, 5$ and $y = 0, 0.1, 0.2, 2, 2.1, 2.2$. The secants are $0.1, 0.1, 1.8, 0.1, 0.1$.

- **Line L2.** The three-point slopes at $x_1, \ldots, x_4$ are $0.1, 0.95, 0.95, 0.1$, and the end slopes are $0.1$.
- **Line L4.** On $[1, 2]$, $(\alpha, \beta) = (1, 9.5)$, far outside the disk. Scaling by $\tau = 3/\sqrt{1 + 90.25} = 0.314$ gives $d_1 = 0.0314$, $d_2 = 0.2984$. On $[3, 4]$ the same happens by symmetry. The final slopes are $0.1, 0.0314, 0.2984, 0.2984, 0.0314, 0.1$.
- **Values.** $s(0.5) = 0.0586$, $s(1.5) = 0.1166$, $s(2.5) = 1.1$, $s(3.5) = 2.0834$, $s(4.5) = 2.1414$. The curve is nondecreasing with range exactly $[0, 2.2]$.

The natural [cubic spline](/cubic-spline-interpolation/) through the same data dips to $-0.0268$, is negative at $x = 1.5$ ($-0.0239$), decreases on parts of $[0.74, 4.26]$ and rises to $2.2268$ above the last data value. Without the scaling in L4, the cubic Hermite piece on $[1, 2]$ with slopes $0.1$ and $0.95$ would also dip, to $0.0376$, below $y_1 = 0.1$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key facts:

1. *Interpolation and smoothness.* On each interval L6 is the cubic Hermite form with values $y_k, y_{k+1}$ and slopes $d_k, d_{k+1}$, so $s(x_k) = y_k$ and $s'$ is continuous because neighboring pieces share each $d_k$ ([cubic Hermite spline](/cubic-hermite-spline/)).
2. *The derivative of a piece.* With $u = (t - x_k)/h_k$, $s'(t) = \delta_k\,g(u)$, where $g(u) = 6u(1 - u) + \alpha(1 - 4u + 3u^2) + \beta(3u^2 - 2u)$.
3. *Sufficient condition (proved).* If $0 \le \alpha \le 3$ and $0 \le \beta \le 3$, then $g \ge 0$ on $[0, 1]$: $g$ is linear in $(\alpha, \beta)$ and its values at the four corners of the square are $6u(1 - u)$, $3(1 - u)^2$, $3u^2$ and $3(2u - 1)^2$, all nonnegative. The disk of radius 3 in the first quadrant lies in this square.
4. *The algorithm lands in the disk.* L2 gives $d_k$ the sign of the adjacent secants or $0$, so $\alpha, \beta \ge 0$; L4 forces $\alpha^2 + \beta^2 \le 9$ and later steps only shrink slopes.
5. *Flat intervals and extrema.* If $\delta_k = 0$, L3 makes the piece constant. At a data extremum, $\delta_{k-1}\delta_k \le 0$ and $d_k = 0$, so $s$ has its extremum at the node and nowhere else.

**The exact region (Fritsch and Carlson, 1980, proved).** For $\delta_k \ne 0$, the piece is monotone if and only if $\alpha, \beta \ge 0$ and either $\alpha + \beta \le 2$, or $2\alpha + \beta \le 3$, or $\alpha + 2\beta \le 3$, or $\alpha - \frac{(2\alpha + \beta - 3)^2}{3(\alpha + \beta - 2)} \ge 0$. The disk of radius 3 and the square $[0, 3]^2$ are convenient subsets; any rule that maps $(\alpha, \beta)$ into the region works.

**Accuracy.** Shape preservation costs accuracy only where slopes are changed.

- *Proved.* On an interval where L3 and L4 change nothing, the error is that of cubic Hermite interpolation with approximate slopes: for $f \in C^4$, $|f - s| \le \frac{h^4}{384}\|f^{(4)}\| + \frac{h}{4}\max(|f'(x_k) - d_k|, |f'(x_{k+1}) - d_{k+1}|)$, and the three-point slopes have errors $O(h^2)$, so the error is $O(h^3)$.
- *Proved.* Where a slope is set to 0 at a data extremum or scaled, the local error is $O(h^2)$ in general (de Boor and Swartz 1977 analyse the limits of accuracy of monotone piecewise cubics).
- *Observed.* For $e^x$ on $[0, 1]$ and $\arctan 5x$ on $[-1, 1]$ with uniform nodes, the maximum error falls by a factor of about 8 per halving of $h$: $1.60 \times 10^{-4}$, $2.08 \times 10^{-5}$, $2.66 \times 10^{-6}$, $3.36 \times 10^{-7}$ for $e^x$ with $n = 10, 20, 40, 80$. For $\sin x$ on $[0, 2\pi]$, which has interior extrema, the observed rate was also about 3 for $n$ from 20 to 160 ($1.90 \times 10^{-3}$, $2.46 \times 10^{-4}$, $3.09 \times 10^{-5}$, $3.87 \times 10^{-6}$), since the zeroed slopes occur only at the one or two nodes next to each extremum.

## Complexity

- **Setup.** Line L1 costs $3n$ operations, L2 about $7$ per interior node, and L3 and L4 at most about $10$ per interval (one `hypot` counted as a few operations): about $20n$ in total, all in one pass. Space $O(n)$ for $h$, $\delta$ and $d$.
- **Evaluation.** Locating the interval costs $\lceil\log_2 n\rceil$ comparisons by [binary search](/binary-search/), or $O(1)$ for a uniform grid or when points are evaluated in sorted order. The Hermite form of L6 costs about 22 operations.
- **Locality.** The initial slopes are local, but the left-to-right scaling pass can carry a reduced slope from one interval into the test on the next, so in the worst case a change propagates further. In practice the effect dies out within one or two intervals. The Fritsch-Butland slopes below are strictly local: each $d_k$ depends only on $y_{k-1}, y_k, y_{k+1}$.

**Rounding.** Every step is a short, well-conditioned expression. The secants $\delta_k$ suffer cancellation when $y_{k+1} \approx y_k$, but $s$ uses $h_k\delta_k$ only through the Hermite form, so absolute errors stay of order $u\max|y|$. Exact monotonicity in floating point is not guaranteed by the theory: rounding in L6 can produce a decrease of a few units in the last place between two very close evaluation points. The tests allow a relative tolerance of $10^{-12}$ for this.

## Properties

- **Shape preserving.** Monotone on monotone data, constant on flat data, extrema only at data extrema, and values between neighboring data on every interval, so the range of $s$ equals the range of the data.
- **$C^1$, not $C^2$.** The second derivative jumps at the nodes; curvature plots show the joins.
- **Nearly local.** No linear system is solved; changing one data point changes the initial slopes at three nodes only, and the scaling pass rarely carries the change further.
- **Exact for linear data.** All $\alpha = \beta = 1$, nothing is scaled and $s$ is the line.
- **Not exact for quadratics.** The three-point slopes reproduce quadratics, but scaling or zeroing near extrema does not.
- **Nonlinear.** The interpolant of a sum of data is not the sum of interpolants.

## Variants and improvements

- **Fritsch-Butland harmonic mean.** $d_k = \dfrac{3(h_{k-1} + h_k)}{(2h_k + h_{k-1})/\delta_{k-1} + (h_k + 2h_{k-1})/\delta_k}$ when $\delta_{k-1}\delta_k > 0$, else 0. This weighted harmonic mean is never more than 3 times either secant, so no scaling pass is needed. MATLAB's `pchip` and SciPy's `PchipInterpolator` use it.
- **Box limiting (de Boor and Swartz).** Clip $d_k$ to $[0, 3\delta]$ on each side, the condition $0 \le \alpha, \beta \le 3$ of step 3 above.
- **Hyman filter (1983).** Limits three-point or higher-order slopes by $3\min(|\delta_{k-1}|, |\delta_k|)$, and keeps the higher order of those slopes away from extrema.
- **Akima interpolation (1970).** A different local slope rule, chosen to avoid wiggles rather than to guarantee monotonicity.
- **Convexity preserving** and **positivity preserving** splines, and monotone splines of higher continuity ($C^2$ monotone interpolation needs quintic pieces or extra knots).
- **Monotone smoothing.** For noisy monotone data, isotonic regression followed by monotone interpolation, or monotone smoothing splines.

## When to use it

Use it for data that are known to be monotone or nonnegative and where overshoot would be wrong or harmful: cumulative distribution functions, yield curves and discount factors, thermodynamic tables, dose-response data, lookup tables in control systems, and color and tone curves in graphics. Prefer a [cubic spline](/cubic-spline-interpolation/) when the data are smooth and accuracy or $C^2$ continuity matters more than shape. Prefer [piecewise linear interpolation](/piecewise-linear-interpolation/) when even $C^1$ is not needed.

## Pitfalls

- **Expecting fourth-order accuracy.** With three-point slopes the method is third order at best, and second order where slopes are limited.
- **Forgetting that monotone is not smooth enough for derivatives.** $s''$ jumps at every node, so differentiating $s$ twice gives a step function.
- **Testing $\alpha^2 + \beta^2 > 9$ with ratios.** If $\delta_k$ is tiny, $d_k/\delta_k$ overflows; compare $\sqrt{d_k^2 + d_{k+1}^2}$ with $3|\delta_k|$ as in L4.
- **Changing slopes in a second pass that grows them.** Any later adjustment that increases a slope can break monotonicity of an interval already processed.
- **Unsorted or repeated abscissas.** Sort the data with their values; repeated abscissas have no secant and must be merged or rejected.
- **Extrapolation.** Outside $[x_0, x_n]$ the end cubic is not monotone in general; clamp or extend linearly.
- **Calling this PCHIP in every library.** SLATEC's PCHIP family and MATLAB's `pchip` share the name but use different slope formulas and end conditions, so results differ slightly.

## Implementations

## History

Shape-preserving interpolation became a practical concern in the 1970s with interpolation of physical tables, where splines produced negative densities and nonmonotone equations of state. De Boor and Swartz (1977) studied monotone piecewise cubics and gave the condition $0 \le \alpha, \beta \le 3$. Fritsch and Carlson (1980) at Lawrence Livermore found the exact monotonicity region of a cubic Hermite piece and the two-pass algorithm with the disk of radius 3. Fritsch's PCHIP package (1982), later part of SLATEC, made the method widely available. Fritsch and Butland (1984) gave the harmonic mean slopes, which became MATLAB's `pchip`, with end conditions from Moler's textbook. Hyman (1983) extended the limiting idea to higher-order slopes.

## References
