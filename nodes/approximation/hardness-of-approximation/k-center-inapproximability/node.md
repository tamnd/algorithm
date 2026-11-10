---
tag: 5WNEVK
kind: theorem
slug: k-center-inapproximability
name: k-center inapproximability
aliases:
- Hsu-Nemhauser k-center hardness
- 2 - ε hardness of metric k-center
area: approximation/hardness-of-approximation
level: advanced
summary: Metric k-center cannot be approximated within 2 - ε for any ε > 0 unless P = NP, by a gap reduction from dominating set. This matches the farthest-first and threshold algorithms.
prereqs: [k-center-problem, dominating-set, gap-problem, metric-space]
see_also: [gonzalez-k-center, k-center-hardness, dominating-set-inapproximability, triangle-inequality, k-median-inapproximability, parameterized-inapproximability, bottleneck-tsp, gap-preserving-reduction]
sources:
  - paper: doi:10.1016/0166-218X(79)90044-1
    title: "W.-L. Hsu and G. L. Nemhauser, Easy and hard bottleneck location problems, Discrete Applied Mathematics 1(3), 1979"
    locator: the NP-hardness of approximating the k-center radius within a factor below 2
  - paper: doi:10.1287/moor.10.2.180
    title: "D. S. Hochbaum and D. B. Shmoys, A best possible heuristic for the k-center problem, Mathematics of Operations Research 10(2), 1985"
    locator: the threshold 2-approximation and the remark that 2 is best possible unless P = NP
  - paper: doi:10.1016/0304-3975(85)90224-5
    title: "T. F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985"
    locator: the farthest-first 2-approximation
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.2 (the k-center problem, the greedy algorithm and the hardness from dominating set)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 5 (k-center, the parametric pruning algorithm and its hardness)
  - paper: doi:10.1145/5925.5933
    title: "D. S. Hochbaum and D. B. Shmoys, A unified approach to approximation algorithms for bottleneck problems, Journal of the ACM 33(3), 1986"
    locator: the k-supplier problem, its 3-approximation and the matching hardness
  - paper: "T. Feder and D. H. Greene, Optimal algorithms for approximate clustering, Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 1988"
    locator: the hardness of k-center for points in the plane under the Euclidean and the l-infinity distance
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A1.1, problem GT2 (dominating set)
---

The k-center inapproximability theorem says that, for every $\varepsilon > 0$, no polynomial-time algorithm approximates the metric [k-center problem](/k-center-problem/) within a factor $2 - \varepsilon$, unless P = NP. Hsu and Nemhauser proved it in 1979 by a [gap reduction](/gap-problem/) from [dominating set](/dominating-set/), and the full proof is below. The factor 2 is reached by the [farthest-first algorithm](/gonzalez-k-center/) of Gonzalez and by the threshold algorithm of Hochbaum and Shmoys, so the problem has an exact approximation threshold of 2.

## Statement

An instance of metric k-center is a set $V$ of $n$ points, a distance $d : V \times V \to \mathbb{R}_{\ge 0}$ that is symmetric, zero exactly on the diagonal and satisfies the [triangle inequality](/triangle-inequality/), and an integer $k$ with $1 \le k < n$. A solution is a set $C \subseteq V$ with $|C| \le k$, and its cost is the radius $r(C) = \max_{v \in V} \min_{c \in C} d(v, c)$. $\mathrm{OPT}$ is the least radius. For this minimization problem, a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance, in the worst case.

**Theorem (Hsu and Nemhauser 1979).**

1. For each $\varepsilon \in (0, 1]$, if a polynomial-time algorithm has ratio $2 - \varepsilon$ for metric k-center, then P = NP. This holds already for instances in which every distance between distinct points is 1 or 2.
2. Without the triangle inequality, let $\alpha(n) \ge 1$ be any function with $\lceil \alpha(n) \rceil$ computable in time polynomial in $n$. If a polynomial-time algorithm has ratio $\alpha(n)$, then P = NP.

## In plain words

Picture towns joined by short roads. You want to place a few fire stations so that every town has a station in it or next to it. Deciding whether a given number of stations is enough is a hard question.

Turn it into a distance problem. Towns joined by a road are at distance one. All other pairs are at distance two. Now the farthest town from its station is at distance one exactly when the stations answer the hard question with yes. Otherwise it is at distance two. A fast method that always came within less than twice the best would have to find distance one whenever it is possible, so it would answer the hard question. The simple greedy method already reaches twice the best, so nothing better is possible.

## Proof

*The reduction.* An instance of dominating set is a graph $H = (V, E)$ with $n$ vertices and an integer $k$ with $1 \le k < n$. The question is whether some $D \subseteq V$ with $|D| \le k$ has every vertex in $D$ or adjacent to a vertex of $D$. This problem is NP-complete (Garey and Johnson, problem GT2). Define, for a number $t \ge 2$,

$$d_t(u, v) = \begin{cases} 0 & u = v, \\ 1 & \{u, v\} \in E, \\ t & \text{otherwise}. \end{cases}$$

The k-center instance is $(V, d_t, k)$. It has $\binom{n}{2}$ distances, each with $O(\log t)$ digits.

*The triangle inequality for $t = 2$.* Let $u, v, w$ be points. If two of them are equal, the inequality $d(u, w) \le d(u, v) + d(v, w)$ is an equality or reads $d(u, w) \le d(u, w) + 0$. If $u, v, w$ are distinct, then $d(u, w) \le 2 \le d(u, v) + d(v, w)$, because each distance between distinct points is at least 1. So $d_2$ is a metric.

*The key equivalence.* Let $C \subseteq V$ with $|C| \le k$. Since $k < n$, some point lies outside $C$, so $r(C) \ge 1$. Each point is at distance at most $t$ from each center, so $r(C) \le t$. Every distance is 0, 1 or $t$, so $r(C) \in \{1, t\}$. And $r(C) = 1$ exactly when each $v \notin C$ has $d(v, c) = 1$ for some $c \in C$, that is, when $C$ is a dominating set of $H$. Therefore

$$\mathrm{OPT}(V, d_t, k) = \begin{cases} 1 & \text{if } H \text{ has a dominating set of size at most } k, \\ t & \text{otherwise.} \end{cases}$$

*Part 1.* Take $t = 2$ and run the assumed $(2 - \varepsilon)$-approximation $A$. If $H$ has a dominating set of size at most $k$, then $A$ returns a radius at most $2 - \varepsilon < 2$, and the only such value is 1. If not, every solution has radius 2. So "the radius of $A$'s solution is 1" decides dominating set in polynomial time, and P = NP.

*Part 2.* Take $t = \lceil \alpha(n) \rceil + 1$. The yes case has $\mathrm{OPT} = 1$, so $A$ returns radius at most $\alpha(n) < t$, hence radius 1. The no case has radius $t$ for every solution. As before, $A$ decides dominating set. $\blacksquare$

### Example

The path $0 - 1 - 2 - 3 - 4$ has domination number 2, with $D = \{1, 3\}$. In the instance $d_2$, $\mathrm{OPT} = 1$ for $k = 2$ and $\mathrm{OPT} = 2$ for $k = 1$. The Petersen graph has 10 vertices, degree 3 and domination number 3. Each vertex covers itself and 3 neighbours, so 2 centers cover at most 8 of the 10 points: $\mathrm{OPT} = 2$ for $k = 2$, and $\mathrm{OPT} = 1$ for $k = 3$.

## Consequences

- **The threshold of k-center is exactly 2.** The [farthest-first traversal](/gonzalez-k-center/) (Gonzalez 1985) and the threshold algorithm (Hochbaum and Shmoys 1985) have ratio 2, and part 1 rules out every smaller constant. Their analyses compare with the lower bound on the [k-center problem](/k-center-problem/) page: $k + 1$ points pairwise more than $2r$ apart force $\mathrm{OPT} > r$.
- **No PTAS.** The gap is a full factor of 2, not only a small constant, so k-center has no [PTAS](/ptas/), and no algorithm improves on the known ratio by any constant.
- **Parameterized hardness.** Dominating set is W[2]-hard with parameter $k$ ([parameterized dominating set](/parameterized-dominating-set/)). The reduction keeps $k$, so even an algorithm with ratio $2 - \varepsilon$ and running time $f(k) \cdot n^{O(1)}$ would give FPT = W[2]. See [parameterized inapproximability](/parameterized-inapproximability/).
- **Related bottleneck problems.** For k-supplier, where centers must come from a given set of suppliers, the best ratio is 3, and $3 - \varepsilon$ is NP-hard (Hochbaum and Shmoys 1986). The same style of argument applies to [bottleneck TSP](/bottleneck-tsp/).
- **Geometric inputs.** The reduction uses a general metric. For points in the plane, a smaller threshold is known to hold: Feder and Greene (1988) showed hardness about $1.82$ for Euclidean distances and 2 for the $\ell_\infty$ distance. These are cited here, not proved.

## Tightness

The hard instances are as bad as possible for the problem: in $d_2$, every set of $k$ centers has radius at most 2, so every algorithm is a 2-approximation on them, and the whole question is whether one can find radius 1. So the constant 2 in part 1 cannot be raised by this reduction, and it cannot be raised by any reduction, because ratio 2 is achieved in polynomial time.

The condition $k < n$ excludes only the trivial case $k = n$, where $C = V$ has radius 0. The proof also needs integer, or at least discrete, distances: it uses that no radius lies strictly between 1 and 2.

## History

Hsu and Nemhauser (1979) proved the hardness for bottleneck location problems, including k-center. Gonzalez (1985) and Hochbaum and Shmoys (1985) gave the 2-approximations; the title of the Hochbaum and Shmoys paper, "A best possible heuristic for the k-center problem", refers to this matching bound. Hochbaum and Shmoys (1986) extended the method to k-supplier and other bottleneck problems. Williamson and Shmoys (Section 2.2) give the reduction above.

## References
