---
tag: AB3WK9
kind: algorithm
slug: adaptive-quadrature
name: Adaptive quadrature
aliases:
- adaptive Simpson
- globally adaptive quadrature
- adaptive integration
- automatic integration
- locally adaptive quadrature
area: numerical/quadrature
level: core
summary: Keep the panels of [a, b] in a priority queue keyed by a local error estimate, and split the worst panel until the estimates add up to at most τ. The estimate is a heuristic.
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {k: "the number of panel splits", τ: "the absolute tolerance", N: "the evaluation budget"}
  time: {worst: "O(k log k)"}
  space: {extra: Θ(k)}
  evaluations: {worst: "5 + 4k"}
properties: {deterministic: true, recursive: false, error_estimate_is_heuristic: true, exact_on_polynomials_of_degree: 5}
history:
  year: 1962
  people: [J. N. Kuncir, W. M. McKeeman, J. N. Lyness, R. Piessens, Walter Gander, Walter Gautschi]
  note: Kuncir and McKeeman published recursive adaptive Simpson routines in Communications of the ACM in 1962. Lyness analysed them in 1969. QUADPACK (1983) made the globally adaptive Gauss-Kronrod scheme standard, and Gander and Gautschi revisited the termination tests in 2000.
prereqs: [composite-quadrature, simpsons-rule]
see_also: [gauss-kronrod-quadrature, composite-quadrature, simpsons-rule, richardson-extrapolation, romberg-integration, improper-integration, tanh-sinh-quadrature, binary-heap]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 6, Automatic integration (adaptive Simpson, global and local strategies, and the failure of error estimates)
  - paper: doi:10.1023/A:1022318402393
    title: "Walter Gander and Walter Gautschi, Adaptive quadrature, revisited, BIT Numerical Mathematics 40(1) (2000) 84-101"
    locator: the adaptive Simpson and adaptive Lobatto programs, and the termination test relative to a rough estimate of the integral
  - book: isbn:9783540125532
    title: Robert Piessens, Elise de Doncker-Kapenga, Christoph W. Überhuber and David K. Kahaner, QUADPACK, A Subroutine Package for Automatic Integration, Springer Series in Computational Mathematics 1, 1983
    locator: Chapter 2 (the globally adaptive strategy and its error estimates) and the descriptions of QAG and QAGS
  - paper: "J. N. Lyness, Notes on the adaptive Simpson quadrature routine, Journal of the ACM 16(3) (1969) 483-495"
    locator: the analysis of the McKeeman routine and of its tolerance per panel
  - paper: "W. M. McKeeman, Algorithm 145, Adaptive numerical integration by Simpson's rule, Communications of the ACM 5(12) (1962) 604"
    locator: the original recursive routine
  - paper: "Michael A. Malcolm and R. Bruce Simpson, Local versus global strategies for adaptive quadrature, ACM Transactions on Mathematical Software 1(2) (1975) 129-146"
    locator: the comparison of the locally adaptive (stack) strategy and the globally adaptive (priority queue) strategy
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.5, Automatic numerical integration
---

Adaptive quadrature computes $I(f) = \int_a^b f(x)\,dx$ to a requested tolerance $\tau$ by placing more nodes where $f$ is hard to integrate. It keeps a partition of $[a, b]$ into panels, each with a local rule and a local error estimate, and it splits the panel with the largest estimate until the estimates add up to at most $\tau$. This page gives the globally adaptive version with a [Simpson](/simpsons-rule/) pair on each panel and a [priority queue](/binary-heap/), which costs $5 + 4k$ function evaluations after $k$ splits. The error estimate is a heuristic: it is asymptotically right for smooth $f$, but no method that only samples $f$ can guarantee its result.

## In plain words

A fixed rule spends the same effort everywhere. Most functions are easy in some places and hard in others, for example near a sharp corner or a steep rise. Adaptive quadrature spends the effort where it is needed. It computes the area of each piece in two ways, one coarse and one fine. When the two answers agree, the piece is probably done. When they disagree, the difference is a guess of the error. The method keeps all pieces in a list sorted by their guessed error, takes the worst piece, cuts it in half, and repeats. It stops when the guessed errors add up to less than what the user asked for. The guess can be wrong: if the function hides a narrow spike between the sample points, the method never sees it.

## The problem

**Notation.** As on all quadrature pages, $I(f) = \int_a^b f(x)\,w(x)\,dx$, with $w = 1$ here; a rule is $Q(f) = \sum_i w_i f(x_i)$ with $n$ nodes; the error is $E(f) = I(f) - Q(f)$; $d$ is the [degree of precision](/degree-of-precision/); $\tau$ is the tolerance.

The input is a function $f$ that can be evaluated at any point of a finite interval $[a, b]$, a tolerance $\tau \ge 0$ on the absolute error, and a budget $N$ of function evaluations. The output is an approximation $\hat I$, an error estimate $\hat E$, the number of evaluations used, and a flag that says whether $\hat E \le \tau$. The goal is $|I(f) - \hat I| \le \tau$ with few evaluations; the algorithm can only promise $\hat E \le \tau$, and the flag reports that. For an infinite interval or an endpoint where $f$ is infinite, transform the integral first ([improper integration](/improper-integration/)).

## The algorithm

For a panel $[l, r]$ with $h = r - l$ and the values $f_0, \ldots, f_4$ of $f$ at $l, l + h/4, l + h/2, l + 3h/4, r$:

$$S_1 = \tfrac{h}{6}(f_0 + 4f_2 + f_4), \quad S_2 = \tfrac{h}{12}(f_0 + 4f_1 + 2f_2 + 4f_3 + f_4), \quad Q = S_2 + \tfrac{S_2 - S_1}{15}, \quad e = \tfrac{|S_2 - S_1|}{15}.$$

$S_1$ is Simpson's rule on the panel and $S_2$ is Simpson's rule on its two halves. The divisor 15 is $2^4 - 1$ of [Richardson extrapolation](/richardson-extrapolation/) for an error of order $h^4$ per unit length.

```pseudo id=main
ADAPTIVE(f, a, b, τ, N)                     ▷ a ≤ b finite, N ≥ 5 evaluations
L1  if a = b then return (0, 0, 0, true)
L2  evaluate f at the 5 points a + i(b − a)/4; k ← 5
L3  H ← a max-priority queue holding [a, b], keyed by its e
L4  Q_tot ← Q[a, b]; E_tot ← e[a, b]
L5  while E_tot > τ do
L6      if k + 4 > N then stop with flag false
L7      remove from H the panel [l, r] with the largest e; m ← l + (r − l)/2
L8      if l < l + (r−l)/8 < … < l + 7(r−l)/8 < r fails in floating point then put [l, r] back, stop with flag false
L9      evaluate f at l + j(r − l)/8 for j = 1, 3, 5, 7; k ← k + 4
L10     Q_tot ← Q_tot − Q[l, r] + Q[l, m] + Q[m, r]; E_tot ← E_tot − e[l, r] + e[l, m] + e[m, r]
L11     insert [l, m] and [m, r] into H
L12 return (Σ Q over H, Σ e over H, k, Σ e over H ≤ τ)   ▷ both sums compensated
```

Each panel stores its five values, so a split reuses three of them in each half and needs only four new evaluations (line L9). Line L10 keeps running totals so that the loop test of line L5 costs $O(1)$. Line L12 recomputes both sums from the panels with compensated summation (`math.fsum`), so the rounding drift of the running totals does not reach the output. Line L8 stops the loop when a panel is so narrow that its eighth points are no longer distinct floats; this happens near a jump or a singularity that the tolerance cannot resolve. The case $b < a$ is handled by $\int_a^b = -\int_b^a$.

## Example

Take $f(x) = \sqrt{x}$ on $[0, 1]$, with $I(f) = 2/3$ and $\tau = 3 \times 10^{-6}$. Here $f'$ is infinite at $0$, so the panel at the left end stays the worst one. Each row is one pass of the loop.

| pass | split panel | its $e$ | $e$ of left, right half | $\hat I = \sum Q$ | $\sum e$ | evaluations | true error $I - \hat I$ |
|---|---|---|---|---|---|---|---|
| 0 | | | | 0.65775660 | $1.230 \times 10^{-3}$ | 5 | $8.9 \times 10^{-3}$ |
| 1 | $[0, 1]$ | $1.230 \times 10^{-3}$ | $4.350 \times 10^{-4}$, $1.877 \times 10^{-6}$ | 0.66351615 | $4.369 \times 10^{-4}$ | 9 | $3.15 \times 10^{-3}$ |
| 2 | $[0, 1/2]$ | $4.350 \times 10^{-4}$ | $1.538 \times 10^{-4}$, $6.637 \times 10^{-7}$ | 0.66555245 | $1.563 \times 10^{-4}$ | 13 | $1.11 \times 10^{-3}$ |
| 3 | $[0, 1/4]$ | $1.538 \times 10^{-4}$ | $5.437 \times 10^{-5}$, $2.347 \times 10^{-7}$ | 0.66627240 | $5.715 \times 10^{-5}$ | 17 | $3.94 \times 10^{-4}$ |
| 4 | $[0, 1/8]$ | $5.437 \times 10^{-5}$ | $1.922 \times 10^{-5}$, $8.297 \times 10^{-8}$ | 0.66652694 | $2.208 \times 10^{-5}$ | 21 | $1.40 \times 10^{-4}$ |
| 5 | $[0, 1/16]$ | $1.922 \times 10^{-5}$ | $6.797 \times 10^{-6}$, $2.933 \times 10^{-8}$ | 0.66661693 | $9.685 \times 10^{-6}$ | 25 | $4.97 \times 10^{-5}$ |
| 6 | $[0, 1/32]$ | $6.797 \times 10^{-6}$ | $2.403 \times 10^{-6}$, $1.037 \times 10^{-8}$ | 0.66664875 | $5.301 \times 10^{-6}$ | 29 | $1.79 \times 10^{-5}$ |
| 7 | $[0, 1/64]$ | $2.403 \times 10^{-6}$ | $8.496 \times 10^{-7}$, $3.667 \times 10^{-9}$ | 0.66665999 | $3.752 \times 10^{-6}$ | 33 | $6.67 \times 10^{-6}$ |
| 8 | $[1/2, 1]$ | $1.877 \times 10^{-6}$ | $1.057 \times 10^{-7}$, $3.214 \times 10^{-8}$ | 0.66666032 | $2.012 \times 10^{-6}$ | 37 | $6.34 \times 10^{-6}$ |

The loop stops after pass 8 because $\sum e = 2.01 \times 10^{-6} \le \tau$. The final partition has the panels $[0, 1/128]$, $[1/128, 1/64]$, $[1/64, 1/32]$, and so on up to $[1/4, 1/2]$, $[1/2, 3/4]$, $[3/4, 1]$: they shrink geometrically toward the singular point. The estimate at the left end falls by about $2^{3/2} \approx 2.83$ per split, because the error on $[0, h]$ scales like $h^{3/2}$, not $h^5$. For the same reason the Richardson divisor 15 is wrong there, and the final true error $6.34 \times 10^{-6}$ is about three times the estimate and twice $\tau$.

## Correctness

Before each test of line L5, the panels in $H$ partition $[a, b]$, each stores the values of $f$ at its five points, and $Q_{tot}$ and $E_{tot}$ are the sums of $Q$ and $e$ over $H$. Line L11 replaces a panel by its two halves, which keeps the partition, and line L10 keeps the sums. So the output is the composite rule $\sum_H Q$ on a partition of $[a, b]$, and the flag is true exactly when $\sum_H e \le \tau$. The panel rule $Q = (16S_2 - S_1)/15$ is Boole's rule $\tfrac{h}{90}(7f_0 + 32f_1 + 12f_2 + 32f_3 + 7f_4)$, with degree of precision 5, so the output is exact for polynomials of degree at most 5, and a cubic needs no split at all. Termination holds because each pass adds 4 evaluations and line L6 caps them at $N$.

What is proved about the estimate is asymptotic: for $f \in C^6$ near the panel center $c$, $\int_l^r f - S_2 = (S_2 - S_1)/15 + O(h^7)$, while both sides are of order $h^5 f^{(4)}(c)$. So $e$ is asymptotically the error of $S_2$, which is larger than the error of the returned $Q$. There is no bound for a fixed panel. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model counts evaluations of $f$, plus the other work in floating-point operations.

- **Evaluations.** Line L2 makes 5 evaluations and each split makes 4, so $k$ splits cost $5 + 4k$ evaluations, and never more than $N$.
- **Other work.** Each split does one removal and two insertions on a binary heap of at most $k + 1$ panels, so $O(\log k)$ time, and $O(1)$ arithmetic. The total is $O(k \log k)$. The final sums of line L12 cost $O(k)$.
- **Space.** $H$ holds $k + 1$ panels with five values each, so $\Theta(k)$.
- **How $k$ depends on $\tau$.** This is not a worst-case statement, because the estimate is a heuristic. For $\int_0^1 e^x\,dx$ the evaluation counts for $\tau = 10^{-6}, 10^{-8}, 10^{-10}, 10^{-12}$ are 13, 33, 117 and 377; for $\int_0^1 \sqrt{x}\,dx$ they are 45, 137, 425 and 1333. Both grow by about $100^{1/4} \approx 3.2$ per factor 100 in $\tau$, which is the rate $\tau^{-1/4}$ of a fourth-order rule on a well-graded mesh. A fixed composite Simpson rule on $\sqrt{x}$ has rate $h^{3/2}$ and would need about $\tau^{-2/3}$ evaluations.

## Properties

- **Exact on polynomials of degree at most 5** (in exact arithmetic), through the Boole form of $Q$.
- **The error estimate is a heuristic.** It is asymptotically right where $f$ is smooth, too small near singularities, and zero for functions that vanish at all sample points.
- **Deterministic and not recursive.** The heap replaces the recursion of the classic programs, so deep refinement near a singularity does not overflow the call stack.
- **Global.** The panel with the largest estimate is always split next, so the work goes where the estimated error is, wherever that is in $[a, b]$.

## Variants and improvements

- **Locally adaptive (recursive) Simpson.** The classic programs of Kuncir and McKeeman test each panel against its share $\tau (r - l)/(b - a)$ of the tolerance and recurse on the halves that fail. It needs no heap, but it can over-refine, because a panel cannot use slack left by other panels. The implementation gives it with an explicit stack.
- **Gauss-Kronrod panels.** QUADPACK's QAG uses a [Gauss-Kronrod pair](/gauss-kronrod-quadrature/) such as G7-K15 on each panel, with the heuristic estimate of QUADPACK in place of $|S_2 - S_1|/15$. Each split costs 30 evaluations for G7-K15, but the rule has degree 23, so far fewer splits are needed for smooth $f$.
- **Extrapolation over the mesh.** QAGS adds Wynn's epsilon algorithm on the sequence of results as the mesh is refined toward an endpoint singularity, which accelerates integrands like $x^{-1/2}$ or $\log x$.
- **Gander and Gautschi.** Their programs compare the local difference with a rough estimate $\hat I_0$ of the whole integral and stop when the difference no longer changes $\hat I_0$ in floating point. This adapts the tolerance to the attainable accuracy.
- **Doubly adaptive and other schemes.** Some codes also raise the degree of the local rule, or switch to a [tanh-sinh](/tanh-sinh-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rule on a panel.

## When to use it

Use adaptive quadrature for a one-dimensional integral of a function that you can only evaluate, when the hard regions are local and their position is not known: kinks, steep layers, integrable endpoint singularities. For a smooth (analytic) $f$ on the whole interval, a single [Gauss-Legendre](/gauss-legendre-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rule of growing $n$ converges geometrically and needs far fewer evaluations. For a periodic $f$ over a period, use the [trapezoidal rule](/trapezoidal-rule/). For integrals in many dimensions, adaptive splitting becomes too costly; see [Monte Carlo integration](/monte-carlo-integration/).

## Pitfalls

- **Trusting the estimate.** On $f(x) = e^{-((x - 0.3)/0.001)^2}$ over $[0, 1]$, the five initial samples are all below $10^{-20}$, so $S_1 = S_2$, $e = 0$, and the method returns about $0$ with the flag set, while the integral is $0.001\sqrt{\pi} \approx 1.77 \times 10^{-3}$. The polynomial $f(x) = (x(x - \tfrac14)(x - \tfrac12)(x - \tfrac34)(x - 1))^2$ vanishes at all five points and fools line L2 the same way. No algorithm that samples $f$ at finitely many points can avoid this: some nonzero $f \ge 0$ vanishes at all of them. Use a starting partition that resolves the known features of $f$.
- **An absolute tolerance below the rounding floor.** If $\tau$ is below about $u \int_a^b |f|$, with $u = 2^{-53}$, line L5 never succeeds and the loop runs until the budget of line L6 is used. For a polynomial with an integral of about $3 \times 10^7$ and $\tau = 10^{-9}$, the implementation used 14833 evaluations and stopped with the flag false. Scale $\tau$ with the size of the integral, or use a test like that of Gander and Gautschi.
- **No budget and no width test.** Without lines L6 and L8 a jump or a singularity makes the loop run forever: the panel next to the bad point is split again and again, and finally its midpoint equals an endpoint.
- **Evaluating at a singular endpoint.** The panel rule uses both ends of the panel. For $f(x) = x^{-1/2}$ on $[0, 1]$, line L2 evaluates $f(0)$ and fails. Substitute $x = t^2$, which gives $\int_0^1 2\,dt$, or use a rule with interior nodes only.
- **The tolerance per panel.** A locally adaptive code must give each panel the share $\tau(r - l)/(b - a)$ of the tolerance (or $\tau/2$ for each half), not $\tau$ for each panel; otherwise the total error can grow with the number of panels.
- **Recursion depth.** A recursive program that halves the panel next to $\sqrt{x}$ or $\log x$ can reach a depth of 50 or more. Use an explicit stack or a heap as in line L3.

## Implementations

## History

J. N. Kuncir (Algorithm 103, 1962) and W. M. McKeeman (Algorithm 145, 1962) published recursive adaptive Simpson routines in Communications of the ACM. J. N. Lyness analysed McKeeman's routine in 1969. Malcolm and Simpson compared the local and the global strategies in 1975. QUADPACK, by Piessens, de Doncker-Kapenga, Überhuber and Kahaner (1983), made globally adaptive Gauss-Kronrod quadrature the standard in libraries. Gander and Gautschi (2000) revisited the termination criteria and gave adaptive Simpson and Lobatto programs.

## References
