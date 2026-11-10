---
tag: 1HBVC8
kind: algorithm
slug: streaming-triangle-counting
name: Streaming triangle counting algorithm
aliases:
- wedge sampling triangle counting
area: online-and-streaming/streaming-sketches
level: advanced
summary: Neighborhood sampling keeps a random edge and a random wedge on it with two reservoirs. Its estimate is unbiased for the triangle count T, with variance at most m·C·T for one estimator.
solves: [streaming-triangle-counting-problem]
model: word-ram
complexity:
  vars: {m: the number of edges, T: the number of triangles, C: the largest number of later edges that touch an edge, s: the number of estimators, ε: the relative error, δ: the failure probability}
  time: {worst: O(m s)}
  space: {extra: O(s), for_eps_delta: O(m C/(ε² δ T))}
properties: {online: true, deterministic: false, one_pass: true, unbiased: true}
history:
  year: 2013
  people: [A. Pavan, Kanat Tangwongsan, Srikanta Tirthapura, Kun-Lung Wu]
  note: Pavan, Tangwongsan, Tirthapura and Wu gave neighborhood sampling in PVLDB 2013. It follows Bar-Yossef, Kumar and Sivakumar (2002), Jowhari and Ghodsi (2005) and Buriol et al. (2006), and is close to the wedge sampling of Jha, Seshadhri and Pinar (2013).
prereqs: [reservoir-sampling, triangle-counting, variance, chebyshev-inequality, streaming-model]
see_also: [streaming-triangle-counting-problem, clustering-coefficient, median-trick, triangle-listing-by-degree, greedy-streaming-matching, agm-graph-sketch, epsilon-delta-guarantee, ams-sketch]
sources:
  - url: https://www.vldb.org/pvldb/vol6/p1870-tirthapura.pdf
    title: A. Pavan, Kanat Tangwongsan, Srikanta Tirthapura and Kun-Lung Wu, Counting and sampling triangles from a graph stream, PVLDB 6(14), 2013
    locator: pp. 1870 to 1881; the section on neighborhood sampling (the estimator, its expectation and variance, and the bound on the number of estimators)
  - paper: doi:10.1145/1142351.1142388
    title: Luciana S. Buriol, Gereon Frahling, Stefano Leonardi, Alberto Marchetti-Spaccamela and Christian Sohler, Counting triangles in data streams, PODS 2006
    locator: the one-pass sampling algorithm for the incidence and adjacency stream models
  - url: https://arxiv.org/abs/1212.2264
    title: Madhav Jha, C. Seshadhri and Ali Pinar, A space efficient streaming algorithm for triangle counting using the birthday paradox, KDD 2013
    locator: the streaming algorithm with an edge reservoir and a wedge reservoir, and its analysis
  - url: https://arxiv.org/abs/1304.1458
    title: Vladimir Braverman, Rafail Ostrovsky and Dan Vilenchik, How hard is counting triangles in the streaming model, ICALP 2013
    locator: Section 1 (the survey of earlier algorithms and their parameters), Theorems 1 and 2 (lower bounds)
---

This page describes neighborhood sampling, a one-pass algorithm of Pavan, Tangwongsan, Tirthapura and Wu (2013) that estimates the number $T$ of triangles of a graph whose edges arrive as a stream. One estimator keeps a uniformly random edge $r_1$, a uniformly random later edge $r_2$ that touches $r_1$, and a count $c$ of such edges, all with [reservoir sampling](/reservoir-sampling/), and it checks whether the edge that closes the wedge $r_1 r_2$ comes later. The estimate $m \cdot c$ when the triangle closes, and 0 otherwise, has expectation exactly $T$. The mean of $s$ independent estimators gives a $(1 \pm \varepsilon)$ estimate when $s$ is of order $mC/(\varepsilon^2 \delta T)$, where $C$ is at most twice the largest degree. On this page $m$ is the number of edges, the edges $e_1, \ldots, e_m$ arrive in this order, and each edge arrives once.

## In plain words

Pick one road on a map at random, as the roads are announced one by one. Then, among the roads announced after it that share a town with it, pick one at random, and count how many there were. The two roads form a corner with three towns. If the third road that closes this corner into a triangle is announced later, you have found a triangle. Each triangle has a fixed chance of being found this way, and you multiply by the inverse of that chance, so on average you get the true number of triangles. One try is very noisy, so you run many tries side by side and take the mean.

## The problem

The input is a stream of the $m$ edges of a simple graph $G$, in any order. The output is an estimate $\hat T$ of the number $T$ of triangles, with $\Pr[|\hat T - T| > \varepsilon T] \le \delta$, in one pass and little memory. The [triangle counting in streams problem](/streaming-triangle-counting-problem/) page gives the lower bounds: in one pass, the space must depend on $m/T$ or more, so every algorithm has a bound in terms of graph parameters.

## The algorithm

For an edge $e_j$, let its *neighborhood* $N(e_j)$ be the set of later edges $e_k$, $k > j$, that share an endpoint with $e_j$, and let $c(e_j) = |N(e_j)|$. For a triangle $\tau$, write its edges in stream order as $f_1(\tau), f_2(\tau), f_3(\tau)$. Both $f_2$ and $f_3$ lie in $N(f_1)$.

```pseudo id=main
PROCESS(e)                  ▷ one estimator; state i, r1, r2, c, found
L1  i ← i + 1
L2  with probability 1/i: r1 ← e; r2 ← none; c ← 0; found ← false; return
L3  if e shares an endpoint with r1 then
L4      if r2 ≠ none and e closes the wedge r1, r2 into a triangle then found ← true
L5      c ← c + 1
L6      with probability 1/c: r2 ← e; found ← false

ESTIMATE()
L7  return i · c if found, else 0

ESTIMATE-MEAN(stream, s)
L8  run s independent estimators on the stream and return the mean of their estimates
```

Line L2 is a reservoir of size one over all edges, so at the end $r_1$ is uniform. After $r_1$ is fixed, lines L5 and L6 are a reservoir of size one over $N(r_1)$, so $r_2$ is uniform over $N(r_1)$ and $c = c(r_1)$. Line L4 checks the closing edge before line L6 may replace $r_2$, because the closing edge of a wedge on $r_1$ is itself in $N(r_1)$.

## Example

Take the stream $\{1,2\}$, $\{2,3\}$, $\{1,3\}$, $\{3,4\}$, $\{2,4\}$, $\{4,5\}$. Here $m = 6$, and there are $T = 2$ triangles, $\{1,2,3\}$ and $\{2,3,4\}$.

| $j$ | $e_j$ | later edges that touch $e_j$ | $c(e_j)$ |
|---|---|---|---|
| 1 | $\{1,2\}$ | $\{2,3\}$, $\{1,3\}$, $\{2,4\}$ | 3 |
| 2 | $\{2,3\}$ | $\{1,3\}$, $\{3,4\}$, $\{2,4\}$ | 3 |
| 3 | $\{1,3\}$ | $\{3,4\}$ | 1 |
| 4 | $\{3,4\}$ | $\{2,4\}$, $\{4,5\}$ | 2 |
| 5 | $\{2,4\}$ | $\{4,5\}$ | 1 |
| 6 | $\{4,5\}$ | none | 0 |

The triangle $\{1,2,3\}$ arrives as $\{1,2\}$, $\{2,3\}$, $\{1,3\}$. It is found exactly when $r_1 = \{1,2\}$ (probability $1/6$) and $r_2 = \{2,3\}$ (probability $1/3$ given $r_1$); then the closing edge $\{1,3\}$ arrives after $r_2$, and the estimate is $6 \cdot 3 = 18$. The triangle $\{2,3,4\}$ arrives as $\{2,3\}$, $\{3,4\}$, $\{2,4\}$, and is found when $r_1 = \{2,3\}$ and $r_2 = \{3,4\}$, also with probability $1/18$ and estimate 18. In every other case the estimate is 0. So one estimator returns 18 with probability $1/9$ and 0 with probability $8/9$. Its mean is $2 = T$, its second moment is 36, and its variance is $36 - 4 = 32$. The tests compute this distribution exactly, over all coin flips, with fractions.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **The reservoirs.** By induction over the stream, $\Pr[r_1 = e_j] = 1/m$ for every $j$, and given $r_1 = e_j$, $c = c(e_j)$ and $r_2$ is uniform over $N(e_j)$ when $c(e_j) > 0$.
2. **When found is true.** At the end, found is true exactly when $r_1 = f_1(\tau)$ and $r_2 = f_2(\tau)$ for some triangle $\tau$. Each such pair belongs to only one triangle, because two edges that share a vertex determine the third.
3. **Unbiased.** Hence $\mathbb{E}[X] = \sum_\tau \frac{1}{m} \cdot \frac{1}{c(f_1(\tau))} \cdot m\,c(f_1(\tau)) = T$.
4. **Variance.** In the same way $\mathbb{E}[X^2] = \sum_\tau m\,c(f_1(\tau)) \le mCT$, where $C = \max_j c(e_j) \le 2(\Delta - 1)$ and $\Delta$ is the largest degree. So $\mathrm{Var}[X] \le mCT$.
5. **The mean of s estimators.** It is unbiased with variance at most $mCT/s$. By [Chebyshev's inequality](/chebyshev-inequality/), $s \ge mC/(\varepsilon^2 \delta T)$ gives $\Pr[|\hat T - T| > \varepsilon T] \le \delta$. With the [median trick](/median-trick/), $O(\log(1/\delta))$ groups of $O(mC/(\varepsilon^2 T))$ estimators suffice.

## Complexity

**Space.** One estimator keeps two edges, two counters and a bit, $O(1)$ words. The mean of $s$ estimators needs $O(s)$ words, and for an $(\varepsilon, \delta)$ estimate $s = O(mC/(\varepsilon^2 \delta T))$, or $O((mC/(\varepsilon^2 T))\log(1/\delta))$ with the median trick. The algorithm needs an upper bound on $mC/T$ to choose $s$; Pavan et al. state the bound with the largest degree $\Delta$ in place of $C$.

**Time.** Each edge costs $O(1)$ per estimator, so $O(ms)$ in all. Pavan et al. also show how to process a batch of edges for all estimators together, which is much faster than running each estimator on its own when $s$ is large.

## Properties

- **Unbiased** for every graph and every stream order.
- **One pass, insertion only.** It does not handle deletions.
- **Order-dependent variance.** The value $c(f_1(\tau))$, and so the variance, depends on the order of the stream. The bound $mCT$ holds for every order.
- **Sampling triangles.** The triangle found by an estimator is a random triangle, with probability $1/(m\,c(f_1(\tau)))$. Pavan et al. correct this bias with an extra step to sample triangles uniformly.
- **No knowledge of T in the estimator.** Only the choice of $s$ needs a bound on $m C/T$.

## Variants and improvements

- **Bar-Yossef, Kumar and Sivakumar (2002)** reduced triangle counting to estimating [frequency moments](/frequency-moment-problem/) of a derived stream of vertex triples, with space polynomial in $(T_1 + T_2)/T$, where $T_i$ is the number of vertex triples with exactly $i$ edges.
- **Jowhari and Ghodsi (2005)** used [AMS-style sketches](/ams-sketch/) with space depending on $m$, $T$ and the numbers of 4-cycles and 6-cycles.
- **Buriol et al. (2006)** sample an edge and a third vertex, and check whether the two closing edges arrive later. The space depends on $mn/T$.
- **Jha, Seshadhri and Pinar (2013)** keep a reservoir of edges and a reservoir of the wedges they form, estimate the fraction of closed wedges, and use the birthday paradox to show that $O(\sqrt{n})$ edges suffice for many real graphs. This is the wedge sampling method of the alias.
- **TRIEST (De Stefani, Epasto, Riondato and Upfal, 2016)** keeps a reservoir of a fixed number of edges, counts the triangles in the sample, and scales each by the inverse of its probability to be kept. Its fully dynamic version handles deletions.
- **Several passes.** With two or more passes, space bounds such as $O(m/T^{1/3})$ for distinguishing $T = 0$ from $T \ge T_0$ are possible (Braverman, Ostrovsky and Vilenchik 2013).

## When to use it

Use neighborhood sampling when the edges of a large graph arrive once, the graph does not fit in memory, and the graph has many triangles compared with $mC$, as in social and web graphs. It is simple, unbiased, and easy to run as many independent estimators in parallel. If the graph fits in memory, count exactly with [triangle listing by degree](/triangle-listing-by-degree/) in $O(m^{3/2})$ time. If the stream has deletions, use TRIEST or a sketch-based method. If $T$ may be tiny or zero, no small-space one-pass method can work, by the lower bounds on the problem page.

## Pitfalls

- **Order of lines L4 and L6.** The closing edge of the wedge $r_1 r_2$ also touches $r_1$. If the code first replaces $r_2$ and then checks closure, it misses triangles and the estimate is biased.
- **Resetting found.** When $r_2$ changes, found must be reset; when $r_1$ changes, everything must be reset.
- **Too few estimators.** The variance can be as large as $mCT$, so with $T$ small compared with $mC$ one needs many estimators. In the test of this page, a random graph with $m = 102$ and $T = 100$ has a variance of about $124000$ per estimator, so 1500 estimators still have a standard error of about 9.
- **Repeated edges.** The analysis assumes each edge arrives once. Duplicate edges change $c$ and can create false triangles; remove them first or use a model that allows them.
- **Independence.** The $s$ estimators must use independent random choices.

## Implementations

## History

Bar-Yossef, Kumar and Sivakumar (SODA 2002) started the study of triangle counting in streams, with the reduction to frequency moments and the first one-pass lower bound. Jowhari and Ghodsi (COCOON 2005) and Buriol et al. (PODS 2006) gave sampling algorithms with better space in terms of graph parameters. Pavan, Tangwongsan, Tirthapura and Wu (PVLDB 2013) introduced neighborhood sampling with the bound in terms of $m\Delta/T$, and in the same year Jha, Seshadhri and Pinar (KDD 2013) gave wedge sampling with the birthday paradox, and Braverman, Ostrovsky and Vilenchik (ICALP 2013) proved the $\Omega(m)$ one-pass lower bound. TRIEST (KDD 2016) made fixed-memory sampling practical for dynamic streams.

## References
