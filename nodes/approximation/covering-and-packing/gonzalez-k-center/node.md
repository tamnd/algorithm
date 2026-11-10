---
tag: FMYANK
kind: algorithm
slug: gonzalez-k-center
name: Gonzalez's farthest-first traversal
aliases:
- Gonzalez algorithm
- Gonzalez's k-center algorithm
- farthest-first traversal
- greedy k-center
- farthest point clustering
area: approximation/covering-and-packing
level: advanced
summary: Greedily pick the point farthest from the current centers; 2-approximation for metric k-center.
solves: [k-center-problem]
model: real-ram
complexity:
  vars: {n: the number of points, k: "the number of centers (at most n)"}
  time: {worst: Θ(n k), average: Θ(n k), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1985
  people: [Teofilo F. Gonzalez]
  note: Gonzalez published the algorithm and its ratio 2 in 1985; in the same year Hochbaum and Shmoys gave a different 2-approximation by thresholds and proved that 2 is best possible with the result of Hsu and Nemhauser.
prereqs: [k-center-problem, metric-space, triangle-inequality, greedy-algorithm]
see_also: [k-center-problem, k-center-inapproximability, k-center-hardness, dominating-set, k-median-problem, k-means-problem, clustering-problem, maximal-independent-set]
sources:
  - paper: "T. F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985, pp. 293-306"
    title: Gonzalez 1985
    locator: the farthest-first algorithm and the proof of ratio 2
  - paper: "D. S. Hochbaum and D. B. Shmoys, A best possible heuristic for the k-center problem, Mathematics of Operations Research 10(2), 1985, pp. 180-184"
    title: Hochbaum and Shmoys 1985
    locator: the threshold algorithm with ratio 2 and the remark that 2 is best possible
  - paper: "M. E. Dyer and A. M. Frieze, A simple heuristic for the p-centre problem, Operations Research Letters 3(6), 1985, pp. 285-288"
    title: Dyer and Frieze 1985
    locator: a farthest-point heuristic with weights and its ratio
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 11.2 (the center selection problem)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.2 (the k-center problem)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 5 (k-center)
---

Gonzalez's farthest-first traversal is a greedy algorithm for the metric [k-center problem](/k-center-problem/). It picks any point as the first center, and then $k - 1$ times it adds the point that is farthest from the centers chosen so far. It uses $\Theta(nk)$ distance computations and returns centers whose radius is at most twice the optimum. No polynomial-time algorithm can promise a ratio below 2 unless P = NP, so in the worst case this simple rule is the best possible.

## In plain words

You must choose $k$ meeting places among a set of towns, so that the longest trip from a town to its nearest meeting place is short. Choose any town first. Then look for the town that is farthest from all meeting places so far, and make it a meeting place too. Repeat until you have $k$ of them.

Why is this good? Suppose that at the end some town is still far from every meeting place. Then the meeting places and that town are all far from each other, because each one was the farthest at its time. These are $k + 1$ towns, so in any plan with $k$ meeting places two of them share a meeting place, and that meeting place is at least half that far from one of them.

## The problem

The input is a set $V$ of $n$ points, a distance $d$ on $V$ that is a [metric](/metric-space/), and an integer $k$ with $1 \le k \le n$. For a set $C$ of centers, the radius is $r(C) = \max_{v \in V} \min_{c \in C} d(v, c)$. The goal is $|C| \le k$ with a small radius; $\mathrm{OPT}$ is the least radius. See the [k-center problem](/k-center-problem/).

*Ratio convention.* This is a minimization problem, and a ratio $\rho$ means $r(C) \le \rho\,\mathrm{OPT}$ on every input. The analysis uses this lower bound on $\mathrm{OPT}$: if $k + 1$ points have pairwise distances at least $r$, then $\mathrm{OPT} \ge r / 2$, by the pigeonhole principle and the [triangle inequality](/triangle-inequality/).

## The algorithm

```pseudo id=main
FARTHEST-FIRST(V, d, k)
L1  c ← any point of V, C ← [c]
L2  for each v ∈ V do D[v] ← d(v, c)        ▷ distance to the nearest center
L3  for i ← 2 to k do
L4      c ← a point v ∈ V with the largest D[v]
L5      if D[c] = 0 then stop the loop          ▷ every point is a center
L6      append c to C
L7      for each v ∈ V do D[v] ← min(D[v], d(v, c))
L8  return C and r = max over v of D[v]
```

The array $D$ always holds the distance from each point to its nearest center, so line L4 finds the farthest point in one scan, and line L8 gets the radius for free.

## Example

Take six points in the plane with the Manhattan distance $d(p, q) = |p_x - q_x| + |p_y - q_y|$: $a = (0, 0)$, $b = (1, 0)$, $c = (0, 1)$, $d = (6, 0)$, $e = (7, 1)$, $f = (3, 4)$, and $k = 3$. Start with $a$.

| step | new center | $D[a]$ | $D[b]$ | $D[c]$ | $D[d]$ | $D[e]$ | $D[f]$ | radius |
|---|---|---|---|---|---|---|---|---|
| L1, L2 | $a$ | 0 | 1 | 1 | 6 | 8 | 7 | 8 |
| $i = 2$ | $e$ (value 8) | 0 | 1 | 1 | 2 | 0 | 7 | 7 |
| $i = 3$ | $f$ (value 7) | 0 | 1 | 1 | 2 | 0 | 0 | 2 |

The centers $\{a, e, f\}$ have radius 2, and this is optimal: radius below 2 would need separate centers for $d$ and $e$, which are at distance 2, for $f$, and for the group $a, b, c$. With $k = 2$ the algorithm stops after the second row with radius 7, while the optimum is 6, a ratio of $\frac76$.

## Correctness

By induction, $D[v]$ is the distance from $v$ to the set of chosen centers, so the returned value $r$ is the true radius, and the centers are distinct because a center has $D$ value 0. When the algorithm returns radius $r > 0$, it has $k$ centers, and the point $f$ with $D[f] = r$ is at distance at least $r$ from each center. Each center $c_j$ was the farthest point when it was chosen, and the values in $D$ never grow, so $d(c_i, c_j) \ge r$ for $i < j$. So the $k + 1$ points $c_1, \ldots, c_k, f$ are pairwise at distance at least $r$. An optimal solution has at most $k$ centers, so two of these points, $u$ and $v$, share an optimal center $c^*$, and $r \le d(u, v) \le d(u, c^*) + d(c^*, v) \le 2\,\mathrm{OPT}$. The full proof, the prefix property and the tight example are below.

## Complexity

- **Time.** Line L2 and each pass of lines L4 and L7 scan the $n$ points once, so the time is $\Theta(nk)$ distance computations and comparisons, in the [real RAM](/real-ram/) model where one distance costs $O(1)$. If all points coincide, the loop stops in its first pass, in $\Theta(n)$ time.
- **Space.** The array $D$ and the list of centers: $\Theta(n)$ extra memory. The distance matrix is not needed; distances are computed on demand.

## Properties

| claim | statement | status |
|---|---|---|
| ratio | $r(C) \le 2\,\mathrm{OPT}$ for every first center and every tie rule | proved below |
| tight for the algorithm | points $-1, 0, 1$ with $k = 1$ and first center $-1$: radius 2 against $\mathrm{OPT} = 1$; with far points $100, \ldots, 100(k-1)$ added, the same for each $k$ | proved below |
| best possible | no polynomial-time ratio $2 - \varepsilon$ unless P = NP | [k-center inapproximability](/k-center-inapproximability/) |
| prefixes | the first $i$ centers are a 2-approximation for $i$ centers, for each $i \le k$ | proved below |
| separation | the chosen centers are pairwise at distance at least the final radius | proved below |

The prefix property makes the order of the centers useful on its own: one run with $k = n$ gives a 2-approximation for every $k$ at once.

## Variants and improvements

- **Threshold method.** Hochbaum and Shmoys (1985) guess the radius $r$ among the distances, pick a maximal set of points with pairwise distances more than $2r$, and accept the guess if it has at most $k$ points. It also has ratio 2; see the [k-center problem](/k-center-problem/).
- **k-supplier.** If the centers must come from a separate set of suppliers, the analogous rule has ratio 3, which is best possible (Hochbaum and Shmoys 1986).
- **Fast Euclidean versions.** Feder and Greene (1988) run farthest-first in $O(n \log k)$ time for points in a Euclidean space of fixed dimension.
- **Streaming.** The doubling algorithm of Charikar, Chekuri, Feder and Motwani (1997) keeps $k$ centers while points arrive and has ratio 8.
- **Hierarchical clustering.** The farthest-first order gives a hierarchy of clusterings that are good for every $k$ at the same time, up to a constant factor (Dasgupta and Long 2005).
- **Sampling.** In graphics and in machine learning, farthest point sampling uses the same order to choose well spread samples, and it is a seeding rule for [k-means](/k-means-problem/).

## When to use it

Use farthest-first when you need $k$ centers with a guarantee on the largest distance, when only distance queries are available, or when you need a good choice for every $k$ from one run. It is a good start for local search and for k-means seeding. Do not use it for the sum of distances, the [k-median problem](/k-median-problem/), where one far outlier draws a center away from the bulk of the data.

## Pitfalls

- **Outliers.** One far point always becomes a center, because it is the farthest point. If some points may be ignored, use a method for k-center with outliers.
- **No triangle inequality.** The proof needs it. For general distances no polynomial-time ratio exists unless P = NP, so the output can be arbitrarily bad.
- **Centers outside the point set.** In a Euclidean space, centers at arbitrary positions can do better than centers at input points, but by at most a factor 2; the ratio of this page is against centers chosen from $V$.
- **Stale distances.** Line L7 must take the minimum with the old value; replacing $D[v]$ by $d(v, c)$ gives wrong farthest points.
- **Duplicates.** If points repeat, the loop must stop when the largest value is 0, or it adds a point that is already covered.

## Implementations

## History

Gonzalez (1985) introduced the farthest-first algorithm for clustering to minimize the largest cluster diameter and proved the factor 2. In the same year Hochbaum and Shmoys gave the threshold method with the same factor and noted, with the reduction of Hsu and Nemhauser (1979) from dominating set, that 2 is best possible unless P = NP. Dyer and Frieze (1985) studied a similar farthest-point rule with weights. The algorithm is a standard first example of a greedy approximation algorithm in textbooks, for example in Section 11.2 of Kleinberg and Tardos.

## References
