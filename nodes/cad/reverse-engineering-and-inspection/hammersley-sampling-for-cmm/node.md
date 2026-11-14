---
tag: 9X9MZP
kind: algorithm
slug: hammersley-sampling-for-cmm
name: Hammersley sampling for coordinate measurement
aliases:
- Woo-Liang sampling
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Places the N probe points of a measuring machine on a surface patch at the Hammersley points (i/N, radical inverse of i), which have a lower discrepancy than a grid or random points.
model: word-ram
complexity:
  vars: {N: the number of probe points}
  time: {worst: Θ(N log N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1993
  people: [T. C. Woo, R. Liang]
  note: Woo and Liang proposed the Hammersley point set of quasi-Monte Carlo integration for the placement of probe points in the dimensional measurement of surfaces.
prereqs: [halton-sequence, discrepancy]
see_also: [cmm-probe-path-planning, cad-based-inspection, form-error-evaluation, koksma-hlawka-inequality, quasi-monte-carlo-integration, stratified-sampling, latin-hypercube-sampling, sobol-sequence]
sources:
  - paper: doi:10.1016/0010-4485(93)90054-R
    title: T. C. Woo and R. Liang, Dimensional measurement of surfaces and their sampling, Computer-Aided Design 25(4), 1993, 233 to 239
    locator: the proposal of the Hammersley sequence for the probe points of surface measurement and its comparison with uniform sampling
  - paper: doi:10.1016/0278-6125(95)98871-3
    title: T. C. Woo, R. Liang, C. C. Hsieh and N. K. Lee, Efficient sampling for surface measurements, Journal of Manufacturing Systems 14(5), 1995, 345 to 354
    locator: the comparison of the Hammersley and Halton-Zaremba sequences with uniform sampling for surface measurement
  - paper: doi:10.1016/S0890-6955(96)00096-X
    title: G. Lee, J. Mou and Y. Shen, Sampling strategy design for dimensional measurement of geometric features using coordinate measuring machine, International Journal of Machine Tools and Manufacture 37(7), 1997, 917 to 934
    locator: sampling strategies for coordinate measurement that combine the Hammersley sequence with stratified sampling
  - paper: doi:10.1111/j.1749-6632.1960.tb42846.x
    title: J. M. Hammersley, Monte Carlo methods for solving multivariable problems, Annals of the New York Academy of Sciences 86(3), 1960, 844 to 874
    locator: the fixed-size point set with first coordinate i/N and radical inverses in the other coordinates
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, CBMS-NSF Regional Conference Series in Applied Mathematics 63, 1992
    locator: Chapter 2 (star discrepancy, the Koksma-Hlawka inequality), Chapter 3, Theorem 3.8 (the discrepancy bound of the Hammersley point set), Chapter 4 ((t, m, s)-nets)
---

Hammersley sampling places the probe points of a coordinate measuring machine on a surface patch. For $N$ points it takes the Hammersley set $(i/N, \varphi_2(i))$, $0 \le i < N$, where the radical inverse $\varphi_2(i)$ mirrors the binary digits of $i$ about the binary point, and maps it from the unit square onto the patch. Woo and Liang proposed it in 1993, after the use of the same set in [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/). The set has a star [discrepancy](/discrepancy/) of $O(\log N / N)$, against about $N^{-1/2}$ for a grid or random points, so averages over the patch, such as the moments of a least-squares fit, are estimated better from the same number of points. This page proves the bound $(m + 1)/N$ for $N = 2^m$ and cites the general constant. It also proves two limits: low discrepancy does not mean small holes, and a sample can only underestimate a minimum zone form error. The order in which the probe visits the points is [CMM probe path planning](/cmm-probe-path-planning/).

## In plain words

A machine checks a surface by touching it at some points, and each touch takes time. We want few points that still tell us the shape well. A square grid leaves long empty strips between its rows, and it can line up with marks left by the cutting tool. Random points leave clumps and gaps.

The Hammersley points fix this. Number the points from 0. Across the surface, the points go in equal steps. For the other direction, write the point's number in binary and read the digits backward, after a point. Point 1 goes halfway up, point 2 a quarter up, point 3 three quarters up. Each new point lands in a gap left by the earlier ones. When the number of points is a power of two, cut the surface into as many equal strips as there are points: each strip holds exactly one point.

## The problem

The input is a number $N$ of probe points and a surface patch, either a rectangle $[x_0, x_0 + w) \times [y_0, y_0 + h)$ of a planar face or a parameterized patch $S(u, v)$, $(u, v) \in [0, 1)^2$. The output is $N$ points on the patch, to be measured and then fitted by a reference feature or evaluated for [form error](/form-error-evaluation/). The aim is a point set that represents the whole patch: its star discrepancy
$$ D^*_N = \sup_{y \in [0, 1]^2} \Bigl\lvert \frac{\#\{\text{points in } [0, y_1) \times [0, y_2)\}}{N} - y_1 y_2 \Bigr\rvert $$
in the parameter square should be small. The radical inverse in base $b$ of $i = \sum_j a_j b^j$ is $\varphi_b(i) = \sum_j a_j b^{-j-1}$, as on the [Halton sequence](/halton-sequence/) page.

## The algorithm

```pseudo id=main
HAMMERSLEY-PROBES(N, patch)
L1  for i ← 0 to N − 1
L2      u ← i / N
L3      v ← φ_2(i)            ▷ reverse the binary digits of i after the point
L4      if patch is a rectangle (x0, y0, w, h) then probe at (x0 + u·w, y0 + v·h)
L5      else probe at S(u, v)
```

**Line L3, the radical inverse.** The code takes the digits of $i$ from the least significant one by repeated division and builds $\varphi_b(i)$ as an exact fraction. For $i < 2^m$, $\varphi_2(i)$ is the $m$-bit reversal of $i$ divided by $2^m$, so the first $2^m$ values are the multiples of $2^{-m}$ in a mixed order. For a dimension $k > 2$, the code puts $\varphi_{b_t}(i)$ for the first $k - 1$ primes $b_t$ in the other coordinates.

**Lines L4 and L5, the map.** A rectangle is an affine image of the square, and the mapped points keep their discrepancy relative to the rectangle. A parameterized patch keeps the points even in $(u, v)$, which is even on the surface only when the area element $\lvert S_u \times S_v \rvert$ is constant, as on a cylinder in the angle and the height. On other patches, reparameterize by area first, or the points crowd where the map shrinks area.

## Example

**Eight points on a face.** For $N = 8$ the binary reversal gives
$$ \varphi_2(0), \dots, \varphi_2(7) = 0, \tfrac12, \tfrac14, \tfrac34, \tfrac18, \tfrac58, \tfrac38, \tfrac78 , $$
so the set is $(0, 0), (\frac18, \frac12), (\frac14, \frac14), (\frac38, \frac34), (\frac12, \frac18), (\frac58, \frac58), (\frac34, \frac38), (\frac78, \frac78)$. On a face of $40 \times 16$ mm with a corner at the origin, the probe points are $(0, 0), (5, 8), (10, 4), (15, 12), (20, 2), (25, 10), (30, 6), (35, 14)$ in mm. Each of the eight columns of width $5$ mm and each of the eight rows of height $2$ mm holds one point, and so does each cell of the $2 \times 4$ and $4 \times 2$ partitions.

**Exact discrepancies.** The brute force of the tests gives, for $N = 2^m$:

| $m$ | $N$ | $D^*_N$ | $N D^*_N$ | proved bound $m + 1$ | cited bound $N \cdot (\frac{7}{2N} + \frac{\log N}{2N \log 2})$ |
|---|---|---|---|---|---|
| 2 | 4 | $1/2$ | 2 | 3 | 4.5 |
| 3 | 8 | $5/16$ | 2.5 | 4 | 5 |
| 4 | 16 | $11/64$ | 2.75 | 5 | 5.5 |
| 5 | 32 | $25/256$ | 3.125 | 6 | 6 |
| 6 | 64 | $55/1024$ | 3.4375 | 7 | 6.5 |

$N D^*_N$ grows by less than $0.5$ when $N$ doubles, the $\log N$ growth. The [discrepancy](/discrepancy/) page has a measured table that compares Hammersley points with random points, a grid and the Halton sequence.

**Holes.** On a grid of $201 \times 201$ candidate centers, the largest empty disk inside the square measured for $N = 64$ has the radius $0.097$ for the Hammersley set, and $0.088$ for the centered $8 \times 8$ grid. The Hammersley set is more even on boxes, not on disks.

## Correctness

The [correctness file](proofs/correctness.md) proves:

- **The radical inverse.** The code computes $\varphi_b(i)$, and for $i < b^m$ it is the reversal of the $m$ digits of $i$ divided by $b^m$, a bijection onto the multiples of $b^{-m}$.
- **The net property.** For $N = 2^m$, every box $[a 2^{-j}, (a+1) 2^{-j}) \times [c 2^{-(m-j)}, (c+1) 2^{-(m-j)})$ of area $1/N$ holds exactly one point.
- **The bound.** For $N = 2^m$, $D^*_N \le (m + 1)/N$: split an anchored box into strips along the binary digits of its width, and each strip makes an error of less than one point.
- **The cited constant.** Niederreiter's Theorem 3.8 gives, in dimension $k$ with the bases $b_1, \dots, b_{k-1}$,
$$ D^*_N < \frac{k}{N} + \frac{1}{N} \prod_{t=1}^{k-1} \Bigl( \frac{b_t - 1}{2 \log b_t} \log N + \frac{b_t + 1}{2} \Bigr) = O\Bigl( \frac{(\log N)^{k-1}}{N} \Bigr), $$
which for $k = 2$, $b_1 = 2$ is $\frac{7}{2N} + \frac{\log N}{2 N \log 2}$ for every $N$. The file cites it and does not prove it.
- **The brute force** over the corners formed by the point coordinates is the exact star discrepancy.
- **Holes.** An empty disk inside the square has a radius of at most $\sqrt{2 D^*_N}$.
- **Underestimation.** The minimum zone of a sample is never wider than the minimum zone of the whole surface.
- **The map** to a rectangle keeps the discrepancy.

## Complexity

The radical inverse of $i$ takes $\lfloor \log_2 i \rfloor + 1$ divisions on the [word RAM](/word-ram/), so $N$ points take $\Theta(N \log N)$ time. A bit reversal by table lookup, or an update of $\varphi_2(i+1)$ from $\varphi_2(i)$ by the carry of the increment, gives $O(1)$ amortized time per point and $\Theta(N)$ in total. The extra space is $\Theta(1)$ beyond the output. The brute-force star discrepancy used in the tests takes $O(N^3)$ time in two dimensions.

## Properties

- **Deterministic.** The same $N$ always gives the same points, which makes measurements repeatable.
- **Not extensible.** The first coordinate $i/N$ depends on $N$, so the $N$-point set is not a prefix of the $2N$-point set. To add points to a measurement already made, use the [Halton sequence](/halton-sequence/), with a discrepancy larger by a factor of order $\log N$.
- **Best order in the plane.** By Schmidt's lower bound, cited on the [discrepancy](/discrepancy/) page, every $N$-point set in the square has $D^*_N \ge c \log N / N$, so the Hammersley set has the best possible order.
- **Exact.** The code returns exact fractions.
- **Distinct coordinates.** The first coordinates are the $N$ values $i/N$, and for $N = 2^m$ the second coordinates are the same $N$ values in another order, so no two points share a row or a column.

## Variants and improvements

- **Halton-Zaremba points.** Woo, Liang, Hsieh and Lee (1995) compared the Hammersley set with the Halton-Zaremba set, a variant of the second coordinate, and with uniform sampling.
- **Stratification.** Lee, Mou and Shen (1997) combined the Hammersley sequence with stratified sampling in sampling strategies for common features.
- **Other low-discrepancy sets.** A [Sobol sequence](/sobol-sequence/) or a scrambled net gives the same order. [Latin hypercube sampling](/latin-hypercube-sampling/) and [stratified sampling](/stratified-sampling/) are randomized alternatives with one point per row or per cell.
- **Curves and higher dimensions.** On a line or a circle, the centered points $(i + \frac12)/N$ have the least star discrepancy, $\frac{1}{2N}$, and the order $\varphi_2(i)$ of the one-dimensional radical inverse is useful only to stop early with even coverage. In dimension $k$ the code uses $k - 1$ prime bases.
- **Adaptive sampling.** Measure a first Hammersley set, fit, and add points where the residuals are large. This targets the peaks that decide a minimum zone.

## When to use it

Use it to choose a fixed number of probe points on a planar face or on a patch with a near-constant area element, when the result is a least-squares fit or another average over the surface. It is simple, deterministic and better than a grid on boxes. Use a grid or a hole-minimizing set when the worst gap matters, and an adaptive scheme when the minimum zone form error must not be missed. Use the [Halton sequence](/halton-sequence/) when the number of points is not known in advance.

## Pitfalls

- **Low discrepancy is not small holes.** The measured largest hole of $64$ Hammersley points is slightly larger than that of an $8 \times 8$ grid. A narrow dent can fall between points.
- **A sample underestimates the minimum zone.** Every zone of the surface holds the sample, so the form error from the points is never larger than the true one. Report it as a lower bound of the true form error, with the number of points.
- **Distorted maps.** On a patch whose area element varies, such as a cone near its apex or a trimmed spline surface, points even in $(u, v)$ are not even on the surface.
- **Inaccessible points.** Some points may be hard to reach for the probe or may lie on trimmed-away regions. Skip them and record it, or move them by a small amount, but do not silently replace them by a grid.
- **Edge points.** The point $i = 0$ is at the corner $(0, 0)$ of the patch, on an edge where a probe can slip. Shift the set by half a step, using $(i + \frac12)/N$, or shrink the patch by the probe radius.

## Implementations

## History

Hammersley introduced the point set in 1960 in a paper on Monte Carlo methods for multivariable problems, beside Halton's sequence of the same year. Niederreiter's monograph of 1992 gives the discrepancy bounds with explicit constants and the theory of nets. Woo and Liang brought the set to dimensional metrology in 1993, for the probe points on surfaces measured by a coordinate measuring machine. Woo, Liang, Hsieh and Lee extended the comparison to the Halton-Zaremba set in 1995, and Lee, Mou and Shen combined the method with stratified sampling in 1997.

## References
