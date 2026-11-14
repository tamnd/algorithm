---
tag: 8P0SSC
kind: algorithm
slug: pelt-algorithm
name: PELT
aliases:
- pruned exact linear time
- PELT change-point algorithm
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Finds the change points that minimize a penalized cost exactly. It runs the optimal partitioning recursion and prunes start points that can never be optimal again.
solves: [change-point-detection]
model: real-ram
complexity:
  vars: {n: "the length of the series, with each segment cost computed in O(1)"}
  time: {worst: Θ(n²)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2012
  people: [Rebecca Killick, Paul Fearnhead, Idris A. Eckley]
  note: Killick, Fearnhead and Eckley added the pruning step to the optimal partitioning recursion of Jackson et al. (2005) and proved that the expected cost is linear under conditions on the data.
prereqs: [change-point-detection, segmented-least-squares]
see_also: [binary-segmentation, cusum, bayesian-online-changepoint-detection, bayesian-information-criterion, akaike-information-criterion, maximum-likelihood-estimation, cross-validation, hidden-markov-model]
sources:
  - paper: doi:10.1080/01621459.2012.737745
    title: R. Killick, P. Fearnhead and I. A. Eckley, Optimal detection of changepoints with a linear computational cost, Journal of the American Statistical Association 107(500) (2012)
    locator: the optimal partitioning recursion, the pruning condition on the cost with the constant K, the proof that pruning keeps the optimum, and the conditions for an expected linear cost
  - paper: doi:10.1109/LSP.2001.838216
    title: Brad Jackson, Jeffrey D. Scargle and others, An algorithm for optimal partitioning of data on an interval, IEEE Signal Processing Letters 12(2) (2005)
    locator: the optimal partitioning recursion over the position of the last change point
  - paper: doi:10.1016/s0092-8240(89)80047-3
    title: I. E. Auger and C. E. Lawrence, Algorithms for the optimal identification of segment neighborhoods, Bulletin of Mathematical Biology 51(1) (1989)
    locator: the segment neighbourhood recursion for a fixed number of segments
  - paper: doi:10.1007/s11222-016-9636-3
    title: Robert Maidstone, Toby Hocking, Guillem Rigaill and Paul Fearnhead, On optimal multiple changepoint algorithms for large data, Statistics and Computing 27(2) (2017)
    locator: functional pruning (FPOP and pDPA) and its comparison with the inequality pruning of PELT
  - paper: doi:10.1080/10618600.2015.1116445
    title: Kaylea Haynes, Idris A. Eckley and Paul Fearnhead, Computationally efficient changepoint detection for a range of penalties, Journal of Computational and Graphical Statistics 26(1) (2017)
    locator: the CROPS algorithm that finds the optimal segmentations for all penalties in an interval
  - paper: doi:10.1016/j.sigpro.2019.107299
    title: Charles Truong, Laurent Oudre and Nicolas Vayatis, Selective review of offline change point detection methods, Signal Processing 167 (2020)
    locator: the sections on cost functions, penalties and exact search methods
---

PELT finds the exact minimizer of a penalized segmentation cost: the sum over segments of a cost $\mathcal C$ of each segment, plus a penalty $\beta$ for each change point. It runs the optimal partitioning recursion, a dynamic programme like the one for [segmented least squares](/segmented-least-squares/), $F(t) = \min_{s < t}[F(s) + \mathcal C(x_{s+1..t}) + \beta]$, which costs $\Theta(n^2)$ segment costs, and adds one rule: a start point $s$ is removed for good when $F(s) + \mathcal C(x_{s+1..t}) + K > F(t)$. If the cost satisfies $\mathcal C(x_{a..s}) + \mathcal C(x_{s+1..b}) + K \le \mathcal C(x_{a..b})$, a removed point can never be the best last change again, so the result is still exactly optimal. The worst case stays quadratic, but when the number of changes grows in proportion to $n$, the expected cost is linear (Killick, Fearnhead and Eckley 2012).

## In plain words

You want to cut a series into pieces so that each piece is well described by a simple model, and each cut costs a fixed fee so that you do not cut everywhere. For each position, you work out the cheapest way to cut the series up to that position, by trying every place where the last piece could start. That is exact but slow, because the list of possible starts grows. The trick is that some starts are already so bad that no future data can make them the best choice. When a clear change has happened, all starts before it become hopeless, and you cross them off. Then the list stays short and the work stays close to one pass.

## The problem

Given $x_1, \ldots, x_n$, a segment cost $\mathcal C(x_{s+1..t})$, written $C(s, t)$, and a penalty $\beta \ge 0$, find change points $0 < \tau_1 < \cdots < \tau_m < n$ that minimize
$$\sum_{j=0}^{m} C(\tau_j, \tau_{j+1}) + \beta m, \qquad \tau_0 = 0,\ \tau_{m+1} = n.$$
Here $\tau_j$ is the last index of segment $j$. A usual cost is the residual sum of squares for a change in mean, $C(s, t) = \sum_{i=s+1}^{t}(x_i - \bar x_{s+1..t})^2$, which is twice the Gaussian negative log likelihood with unit variance up to a constant per point. Usual penalties are $\beta = 2\log n$, close to the [BIC](/bayesian-information-criterion/), and $\beta = 2$ times the number of parameters added per change, the [AIC](/akaike-information-criterion/). See [change-point detection](/change-point-detection/) for the other formulations.

## The algorithm

```pseudo id=main
PELT(n, C, β, K)          ▷ C(s, t) is the cost of x_{s+1..t}; K satisfies the pruning condition
L1  F(0) ← -β; R ← {0}
L2  for t ← 1 to n do
L3      F(t) ← min over s in R of [F(s) + C(s, t) + β]
L4      last(t) ← the smallest s in R that attains the minimum
L5      R ← {s in R : F(s) + C(s, t) + K ≤ F(t)} ∪ {t}
L6  follow last from n back to 0 and return F(n) and the change points last(n), last(last(n)), ... that are positive
```

$F(t)$ is the optimal penalized cost of $x_1, \ldots, x_t$. The start value $F(0) = -\beta$ makes the first segment free of the penalty. Line L3 is the optimal partitioning recursion of Jackson et al. (2005), restricted to the set $R$ of candidate last change points. Line L5 is the pruning step. Without it, $R = \{0, \ldots, t-1\}$ at time $t$ and the method is plain optimal partitioning. For the residual sum of squares, prefix sums of $x_i$ and $x_i^2$ make each $C(s, t)$ cost $O(1)$.

## Example

Take $x = (1, 0, 1, 5, 6, 5, 6, 1, 0)$, the residual sum of squares, $\beta = 4$ and $K = 0$:

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $F(t)$ | 0 | 1/2 | 2/3 | 14/3 | 31/6 | 16/3 | 17/3 | 29/3 | 61/6 |
| last$(t)$ | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 7 | 7 |
| $\lvert R \rvert$ at line L3 | 1 | 2 | 3 | 4 | 2 | 3 | 4 | 5 | 2 |

At $t = 4$ the candidates are $s = 0, 1, 2, 3$, and the values $F(s) + C(s, 4)$ are $43/4$, $14$, $17/2$ and $2/3$. Only $s = 3$ is at most $F(4) = 14/3$, so $R$ becomes $\{3, 4\}$: the points before the first jump are gone for good. The same happens at $t = 8$, where $R$ shrinks from $\{3, \ldots, 7\}$ to $\{7, 8\}$. Back-tracking from $t = 9$ gives last$(9) = 7$ and last$(7) = 3$, so the change points are $\{3, 7\}$ with segments $(1, 0, 1)$, $(5, 6, 5, 6)$ and $(1, 0)$, and $F(9) = 13/6 + 2 \cdot 4 = 61/6$.

The penalty picks the number of changes. The smallest residual sums of squares for $m = 0, 1, 2, 3, 4$ change points are $500/9$, $71/2$, $13/6$, $5/3$ and $4/3$. Adding $4m$ gives about 55.56, 39.50, 10.17, 13.67 and 17.33, so $m = 2$ wins.

## Correctness

The proof is in full below. In outline:

1. **Optimal partitioning.** Every segmentation of $x_1, \ldots, x_t$ has a last segment $x_{s+1..t}$, and the rest is a segmentation of $x_1, \ldots, x_s$. So $F(t) = \min_{0 \le s < t}[F(s) + C(s, t) + \beta]$, and back-tracking the minimizers gives an optimal segmentation.
2. **Pruning lemma.** Suppose that $C(a, s) + C(s, b) + K \le C(a, b)$ for all $a < s < b$. If $F(s) + C(s, t) + K > F(t)$ at some $t > s$, then for every $T > t$,
$$F(s) + C(s, T) \ge F(s) + C(s, t) + K + C(t, T) > F(t) + C(t, T),$$
so $s$ is strictly worse than $t$ as the last change point before $T$, and it is never a minimizer again.
3. **Exactness.** A minimizer of the full recursion is never pruned, so the minimum over $R$ equals the minimum over all $s < t$, and the smallest minimizer is the same. PELT returns the same $F(n)$ and the same change points as optimal partitioning.

For the residual sum of squares the condition holds with $K = 0$, because cutting a segment can only lower its residual sum of squares. The same is true for any cost that is minus a maximized log likelihood. A smaller $K$ prunes less and stays exact; a larger $K$ breaks the condition and can remove the optimum.

## Complexity

Each step $t$ costs $O(\lvert R \rvert)$ segment costs. In the worst case nothing is pruned, $\lvert R \rvert = t$, and the total is $\Theta(n^2)$, the same as optimal partitioning. Series without changes come close to this case. Killick, Fearnhead and Eckley (2012) proved that the expected cost is $O(n)$ when the number of changes grows linearly with $n$ and some further conditions hold; this is cited, not proved here. Measured average and largest sizes of $R$ per step, with $\beta = 2\log n$, Gaussian noise of variance 1, and a seeded random generator:

| $n$ | changes every 100 points: mean $\lvert R \rvert$ | largest $\lvert R \rvert$ | total cost evaluations | no change: mean $\lvert R \rvert$ | largest $\lvert R \rvert$ | total cost evaluations |
|---|---|---|---|---|---|---|
| 1000 | 86.6 | 222 | 86617 | 319.3 | 703 | 319330 |
| 2000 | 82.8 | 206 | 165506 | 1000.5 | 2000 | 2001000 |
| 4000 | 91.5 | 317 | 365879 | 1751.9 | 3701 | 7007526 |
| 8000 | 90.1 | 340 | 720453 | 2940.7 | 5423 | 23525670 |

With a change every 100 points (a new mean drawn from $\{-2, -1, 0, 1, 2\}$), the mean size of $R$ stays near 90 and the total grows in proportion to $n$. Without changes the total grows by a factor between 3.4 and 6.3 each time $n$ doubles, much faster than $n$; at $n = 2000$ nothing was pruned at all. The extra space is $O(n)$ for $F$, last and $R$.

## Properties

- **Exact.** For a cost with the pruning property, the output is a global minimizer of the penalized cost, not an approximation.
- **Same tie rule as the full recursion.** Pruned points are strictly worse, so the choice of the smallest minimizer is not changed.
- **Fast when changes are frequent.** The cost is close to linear exactly in the case where binary segmentation is slowest.
- **Penalized, not constrained.** It finds the best segmentation for a given $\beta$, not for a given number of changes. For a fixed number of changes use the segment neighbourhood recursion of Auger and Lawrence (1989).
- **Any additive cost.** Mean, variance, mean and variance, Poisson rate and regression costs all work when they satisfy the condition.

## Variants and improvements

- **Optimal partitioning.** The same recursion without line L5, $\Theta(n^2)$ always (Jackson et al. 2005).
- **Segment neighbourhood.** A recursion over the number of segments that gives the best segmentation for every $m$ up to a bound, in $O(m n^2)$ (Auger and Lawrence 1989). [Segmented least squares](/segmented-least-squares/) is a close relative for line fits.
- **Functional pruning (FPOP).** Maidstone et al. (2017) keep, for each candidate, the set of segment parameters for which it is still optimal, and drop it when that set is empty. This prunes more than PELT, also when there are few changes.
- **CROPS.** Haynes, Eckley and Fearnhead (2017) find the optimal segmentations for all penalties in an interval $[\beta_{\min}, \beta_{\max}]$ with a small number of PELT runs, which helps to choose $\beta$.
- **Approximate search.** [Binary segmentation](/binary-segmentation/) is faster when there are few changes but is not exact.
- **Online methods.** For a stream, use the [CUSUM](/cusum/) or [Bayesian online changepoint detection](/bayesian-online-changepoint-detection/).

## When to use it

Use PELT when the whole series is available, the segment cost is additive and has the pruning property, and the exact penalized optimum is wanted. If there are few changes in a very long series, PELT can be close to quadratic; use FPOP or binary segmentation then.

## Pitfalls

- **Wrong $K$.** The constant $K$ must satisfy $C(a, s) + C(s, b) + K \le C(a, b)$ for every split. For the residual sum of squares $K = 0$. A positive $K$ there can prune the optimal last change, and then the result is not optimal.
- **Penalty on the wrong scale.** The residual sum of squares must be divided by the noise variance before $\beta = 2\log n$ is meaningful. With the raw sum and a large variance, PELT finds many false changes.
- **Dependent or heavy-tailed noise.** The Gaussian cost then finds too many changes. Use a robust cost, or estimate the dependence and inflate the penalty.
- **Expecting linear time always.** Without changes nothing is pruned and the cost is quadratic, as the table shows.
- **Minimum segment length.** Costs such as the variance cost are $-\infty$ on segments of length 1. Enforce a minimum length; the recursion and the pruning rule extend directly.

## Implementations

## History

Auger and Lawrence (1989) gave the segment neighbourhood dynamic programme for a fixed number of segments. Jackson et al. (2005) gave the optimal partitioning recursion for a penalized number of segments. Killick, Fearnhead and Eckley (2012) added the pruning step, proved that it keeps the exact optimum, and proved the expected linear cost under conditions on the data. Maidstone et al. (2017) compared inequality pruning with functional pruning, and Haynes, Eckley and Fearnhead (2017) gave CROPS for a range of penalties.

## References
