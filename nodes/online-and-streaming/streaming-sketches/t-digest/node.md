---
tag: ND6BPW
kind: data-structure
slug: t-digest
name: T-digest
aliases:
- Dunning t-digest
area: online-and-streaming/streaming-sketches
level: advanced
summary: Quantile summary of weighted centroids whose sizes a scale function keeps small near the tails. It is very accurate in practice, but it has no worst-case error bound.
model: word-ram
complexity:
  vars: {n: the stream length, δ: the compression parameter, b: the buffer size}
  time: {worst: O((δ + b) log(δ + b)), amortized: O(log(δ + b))}
  space: {extra: O(δ + b)}
properties: {online: true, deterministic: true, mergeable: true, comparison: false, worst_case_guarantee: false}
history:
  year: 2013
  people: [Ted Dunning, Otmar Ertl]
  note: Dunning described the t-digest in 2013 and released it as open source. Dunning and Ertl wrote the merging form and the scale functions k0 to k3 in a 2019 paper.
prereqs: [quantile-summary-problem, streaming-model, order-statistic]
see_also: [kll-sketch, greenwald-khanna-summary, q-digest, quantile-summary-problem, mergeable-summaries, munro-paterson-algorithm, dyadic-intervals, comparison-model]
sources:
  - url: https://arxiv.org/abs/1902.04023
    title: Ted Dunning and Otmar Ertl, Computing extremely accurate quantiles using t-digests, 2019
    locator: Section 2.1 (strongly and weakly ordered digests), Section 2.3 (the scale function k1 and the size bound, equations 3 to 5), Section 2.6 (Algorithm 1, the merging form), Section 2.8 (the scale functions k0 to k3), Section 2.9 (interpolation)
  - url: https://arxiv.org/abs/2102.09299
    title: Graham Cormode, Abhinav Mishra, Joseph Ross and Pavel Veselý, Theory meets practice at the median, a worst case comparison of relative error quantile algorithms, KDD 2021
    locator: Section 4 (the nested lopsided attack, Proposition 1, the asymptotic error (δ - 2)/(δ - 1) for k0), Section 4.2 (k2 and k3), Section 5 (experiments on attack streams and on i.i.d. data)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Summaries for Ordered Data
---

The t-digest is a summary of a stream of numbers that answers rank and quantile queries. It keeps a short sorted list of *centroids*, each a mean and a weight, and it uses a *scale function* that allows only small centroids near the two ends of the distribution, so that extreme quantiles such as the 99.9th percentile come out very accurate. It is small, fast and mergeable, and it is used in many monitoring and database systems. Its accuracy is an empirical fact, not a theorem: there is no worst-case bound on its error, and Cormode, Mishra, Ross and Veselý (2021) built streams on which almost all ranks are wrong. On this page $n$ is the stream length, and $\delta$ is the compression parameter of the t-digest (not a failure probability).

## In plain words

You want to know the middle value of a huge list of numbers, or the value that only one in a thousand numbers exceeds. The t-digest keeps a few groups. Each group remembers only how many numbers it holds and their average. Groups in the middle of the data may be large, but groups at the two ends must stay very small, often a single number. From time to time it sorts its groups and joins neighbors as long as the joined group is not too large for its place. To answer a question, it pretends that the numbers of each group sit evenly around the average and reads the answer from that picture. On real data this works very well. But a careful attacker can choose numbers so that the picture is badly wrong.

## The abstract type

The t-digest is a summary for the [quantile summary problem](/quantile-summary-problem/) on real numbers, with weights.

- **Insert(x, w)** adds the value $x$ with weight $w$ (usually $w = 1$).
- **Merge(T')** adds all data of another t-digest.
- **Rank(x)** returns an estimate of the number of values at most $x$.
- **Query($\phi$)** returns an estimate of the $\phi$-quantile, a value with about $\phi n$ values below it.

There is no promised bound on the error of Rank or Query. The intended behavior is a small error relative to $\min(\phi, 1 - \phi)$, that is, a small *relative* error near both tails.

## Representation

The digest stores a list of centroids $(c_1, w_1), \ldots, (c_m, w_m)$ sorted by mean, a buffer of new values, the count $n$, and the smallest and the largest value seen, $x_{\min}$ and $x_{\max}$. A centroid stands for a set of values, its *cluster*; $c_i$ is their mean and $w_i$ their number (or total weight).

Let $W_{<i} = w_1 + \cdots + w_{i-1}$. Centroid $i$ covers the quantile interval $[q_\ell, q_r] = [W_{<i}/n, (W_{<i} + w_i)/n]$. A *scale function* $k : [0, 1] \to \mathbb{R}$ is non-decreasing, and its *size bound* is
$$k(q_r) - k(q_\ell) \le 1 \quad\text{for each centroid with more than one value.}$$
The main scale functions are these (Dunning and Ertl, Section 2.8).

| name | $k(q)$ | effect |
|---|---|---|
| $k_0$ | $\delta q/2$ | every centroid holds at most $2n/\delta$ values, uniform absolute error |
| $k_1$ | $(\delta/2\pi)\arcsin(2q - 1)$ | centroids near $q = 0$ and $q = 1$ are small; the allowed share of a centroid near $q$ is about $2\pi\sqrt{q(1-q)}/\delta$ |
| $k_2$ | $\delta/(4\log(n/\delta) + 24) \cdot \log(q/(1-q))$ | still smaller centroids at the tails, relative error |
| $k_3$ | like $k_2$, with $\log 2q$ and $-\log 2(1 - q)$ | the same, split at the median |

A digest is *fully merged* if no two neighbors can be joined without breaking the size bound.

## Operations

The merging form (Algorithm 1 of Dunning and Ertl) buffers new values and then does one left-to-right pass over the sorted union of the buffer and the centroids.

```pseudo id=main
INSERT(T, x, w)
L1  append (x, w) to the buffer; n ← n + w; update x_min and x_max
L2  if the buffer is full then COMPRESS(T)

COMPRESS(T)
L3  X ← the centroids and the buffer, sorted by mean; S ← their total weight; empty the buffer
L4  q0 ← 0; q_limit ← k⁻¹(k(q0) + 1); σ ← the first element of X
L5  for each next element x of X: q ← q0 + (w(σ) + w(x))/S
L6      if q ≤ q_limit then σ ← σ ∪ x (weighted mean, weights added)
L7      else output σ; q0 ← q0 + w(σ)/S; q_limit ← k⁻¹(k(q0) + 1); σ ← x
L8  output σ; the output list is the new list of centroids

RANK(T, x)
L9  interpolate linearly through the knots (x_min, 0), (c_i, W_<i + w_i/2) for each i, and (x_max, n)

QUERY(T, φ)
L10 find the two knots whose ranks enclose φn and interpolate between their values
```

The test of line L6 is the size bound in the form $q \le k^{-1}(k(q_0) + 1)$, which needs one call to $k$ and one to $k^{-1}$ per output centroid. **Merge** adds the centroids of the other digest to the buffer as weighted values and calls COMPRESS. The interpolation in line L9 puts half of the weight of each centroid on each side of its mean. Dunning and Ertl refine it at singletons, which are known exactly, and at the two ends.

There is also a *clustering* form (their Algorithm 2), which adds each value to the nearest centroid that has room and runs COMPRESS when there are too many centroids. It is older and its result depends more on the order of the input.

## Example

Insert the 20 values $12, 3, 17, 8, 1, 15, 6, 10, 4, 14, 9, 2, 19, 7, 11, 5, 18, 13, 16, 20$ with $\delta = 10$ and a buffer of 100, then run COMPRESS once. The values are $1, \ldots, 20$, so $S = 20$.

With $k_1$, $k(0) = -2.5$, and line L4 gives $q_{\text{limit}} = k^{-1}(-1.5) = (\sin(-0.3\pi) + 1)/2 \approx 0.095$. Joining 1 and 2 would give $q = 0.1 > 0.095$, so the value 1 stays alone. The pass then makes these centroids.

| centroid | values | mean | weight | $k(q_r) - k(q_\ell)$ |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 0.718 |
| 2 | 2 to 5 | 3.5 | 4 | 0.949 |
| 3 | 6 to 11 | 8.5 | 6 | 0.993 |
| 4 | 12 to 16 | 14 | 5 | 0.865 |
| 5 | 17 to 19 | 18 | 3 | 0.758 |
| 6 | 20 | 20 | 1 | 0.718 |

The centroids are small at both ends and large in the middle. The greedy pass is not symmetric, so the left and right halves differ. Rank(10) interpolates between the knots $(8.5, 5 + 3) = (8.5, 8)$ and $(14, 11 + 2.5) = (14, 13.5)$: $8 + 5.5 \cdot 1.5/5.5 = 9.5$, while the true rank is 10. Query(0.5) looks for rank 10 on the same segment and returns $8.5 + 5.5 \cdot 2/5.5 = 10.5$.

With $k_0$ instead, every centroid may hold at most $2 \cdot 20/10 = 4$ values, and the pass makes the weights $4, 4, 3, 4, 4, 1$ with means $2.5, 6.5, 10, 13.5, 17.5, 20$: uniform sizes, no special care for the tails.

**An attack.** The tests run a small form of the attack of Cormode et al. with $k_0$ and $\delta = 20$. They start with 400 integers around 0 and attack the centroid just below 0. In each round they put a batch into the gap between the attacked mean $c$ and the next stream value above $c$: first enough values just above $c$ to fill the attacked centroid, then one value at a quarter of the gap, then many equal values at three quarters of the gap. The last two parts form a new full centroid whose mean is far below almost all of its values, and this one is attacked next. After 30 rounds the stream has 13710 values and the digest has 14 centroids. Just above the innermost mean, the estimated rank is wrong by more than 82 percent of $n$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows what can be proved about the t-digest, which is its *form*, not its accuracy.

1. **Weight and order.** COMPRESS keeps the total weight $n$, and the new means are sorted, because each output centroid is a weighted mean of a run of the sorted input.
2. **Size bound.** Each centroid formed by joining in line L6 satisfies $k(q_r) - k(q_\ell) \le 1$ at the time of the pass, since line L6 joins only while $q \le k^{-1}(k(q_0) + 1)$.
3. **Number of centroids.** After COMPRESS, two neighbors $C_i, C_{i+1}$ together always span more than 1 in $k$: the pass closed $C_i$ because adding the first element of $C_{i+1}$ broke the bound. The pairs $(C_1, C_2), (C_3, C_4), \ldots$ are disjoint, and $k$ rises by $k(1) - k(0) = \delta/2$ in all for $k_0$ and $k_1$. So $\lfloor m/2 \rfloor < \delta/2$, which gives $m \le \lceil \delta \rceil$, the bound of Dunning and Ertl.

**No accuracy guarantee.** The estimate of line L9 assumes that the values of each cluster lie evenly around its mean. Nothing in the structure enforces this. A cluster with one small value and many large ones has its mean below most of its values, so Rank just above the mean counts about half the weight of the cluster that is really above it. The attack nests such clusters, each inside the gap of the one before, so the errors add up. Cormode et al. prove (their Proposition 1) that for a scale function with derivative between two positive constants, such as $k_0$, the asymptotic error of the nested attack is at least a constant $\gamma > 0$ for all large $\delta$. For $k_0$ their equations give the error $(\delta - 2)/(\delta - 1)$, which tends to 1: a larger $\delta$ does not help. For $k_2$ their bound tends to $1/2$. The tests reproduce this effect.

Comparison-based summaries cannot be fooled this way, but the [lower bound](/quantile-summary-problem/) of Cormode and Veselý shows that they need $\Omega((1/\varepsilon)\log(\varepsilon n))$ items, so a summary of $O(\delta)$ items with error $O(1/\delta)$ is impossible in that model. The t-digest escapes the lower bound only because it averages values and interpolates, and the attack exploits exactly this.

## Complexity

**Space.** At most $\lceil \delta \rceil$ centroids after each COMPRESS, plus a buffer of $b$ values, so $O(\delta + b)$ words, and this does not grow with $n$ for $k_0$ and $k_1$. With $k_2$ and $k_3$ as normalized in the table, Dunning and Ertl note that the bound $\lceil \delta \rceil$ holds only up to about $10^{60}$ values, after which the count grows like $\log\log n$.

**Time.** INSERT is $O(1)$ until the buffer is full. COMPRESS sorts $m + b$ elements and calls $k$ and $k^{-1}$ once per output centroid, so $O((\delta + b)\log(\delta + b))$; with $b = \Theta(\delta)$ this is $O(\log \delta)$ amortized per value. Rank and Query scan or binary search the $m + 2$ knots.

**Accuracy in practice.** On data that is not adversarial, the error with $k_1$ is very small at the tails and moderate in the middle. In the tests, with $\delta = 100$ and 20000 uniform values, the rank error at the quantiles $0.001$ to $0.999$ is below $0.01n$. Cormode et al. also report large errors on i.i.d. samples from some heavy-tailed distributions, so the risk is not only for crafted streams.

## Variants

- **Merging form and clustering form.** The merging form on this page is faster and its result is easier to analyze; the clustering form of Dunning's first version adds values to centroids one at a time.
- **Scale functions.** $k_0$ gives uniform centroids; $k_1$ gives better tails; $k_2$ and $k_3$ give relative error at the tails at the cost of a slowly growing size.
- **Alternating direction.** Some implementations run the merging pass left to right and right to left in turn, which removes the asymmetry seen in the example.
- **Relative-error sketches with guarantees.** The ReqSketch of Cormode, Karnin, Liberty, Thaler and Veselý (2021) is a [KLL](/kll-sketch/)-style sketch with a proven relative error bound. It grows slowly with $n$, but its error stays bounded on every input.

## When to use it

Use the t-digest when you need tail quantiles such as the 99th and 99.9th percentile of latencies or sizes, when the data is real-valued and comes from a natural source, and when a small, fixed size and fast merges matter more than a proof. Do not use it where an adversary controls the data or where a written error bound is required; use a [KLL sketch](/kll-sketch/) or a [GK summary](/greenwald-khanna-summary/) there, or a relative-error sketch for the tails.

## Pitfalls

- **Reading its accuracy as a guarantee.** The compression $\delta$ bounds the size, not the error. No choice of $\delta$ bounds the error on all inputs.
- **Repeated values and lopsided clusters.** Many copies of one value, or clusters with a far outlier, move a mean away from the bulk of its values, and interpolation then misplaces ranks.
- **Merge order.** Results depend on the order of inserts and merges, so two digests of the same data can give different answers.
- **Floating point.** Means of large clusters and nested gaps lose precision; the published attack had to work near 0 to keep enough precision.
- **Discrete data.** For integer data with few distinct values, interpolation returns values that never occur. Rounding or an exact count of the distinct values may be better.

## Implementations

## History

Ted Dunning described the t-digest around 2013 and released it as an open-source library. Dunning and Otmar Ertl wrote the 2019 paper with the merging form, the scale functions $k_0$ to $k_3$ and the bound $\lceil\delta\rceil$ on the number of centroids. The t-digest is used in many systems for percentiles. In 2021 Cormode, Mishra, Ross and Veselý constructed inputs with almost arbitrarily large error and compared the t-digest with the ReqSketch, which has guarantees; they found that the t-digest is still more accurate on most data from practice.

## References
