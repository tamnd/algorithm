---
tag: 9898W4
kind: definition
slug: c-approximate-nearest-neighbor
name: c-approximate nearest neighbor
aliases:
- (c,r)-ANN
- c-ANN
area: searching/similarity-search
level: core
summary: Given radius r, return a point within distance c·r of the query whenever one lies within distance r.
prereqs: [k-nearest-neighbor-search, metric-space]
see_also: [approximate-nearest-neighbor-search, locality-sensitive-hashing, locality-sensitive-hash-family, fixed-radius-near-neighbors, nearest-neighbor-search, curse-of-dimensionality]
sources:
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: pages 321 to 350; Section 2 (the definitions of the c-approximate nearest neighbor and of the randomized c-approximate r-near neighbor problems, and the reduction from the first to the second)
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (the ε-NN and (r, ε)-point location in equal balls problems)
  - paper: doi:10.1145/293347.293348
    title: Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998
    locator: pages 891 to 923 (the (1+ε)-approximate nearest neighbor in fixed dimension with the BBD tree)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the definitions of the c-approximate and randomized c-approximate R-near neighbor problems)
---

A c-approximate nearest neighbor of a query is a stored point whose distance to the query is at most $c$ times the distance of the true [nearest neighbor](/k-nearest-neighbor-search/), for a fixed factor $c > 1$. Its fixed-radius form, the $(c, r)$-near neighbor problem, asks only for a point within $c \cdot r$ when some point lies within $r$. These two definitions are the contracts of [approximate nearest neighbor search](/approximate-nearest-neighbor-search/), and [locality-sensitive hashing](/locality-sensitive-hashing/) solves the second one with a query time sublinear in the number of points.

## Definition

Let $(M, \delta)$ be a [metric space](/metric-space/), $P \subseteq M$ a finite nonempty set of $n$ points, $q \in M$ a query, and $c > 1$ a real number. Let $\delta^*(q) = \min_{p \in P} \delta(q, p)$.

**c-approximate nearest neighbor (c-ANN).** A point $p \in P$ is a *c-approximate nearest neighbor* of $q$ if

$$\delta(q, p) \le c \cdot \delta^*(q).$$

The c-ANN problem asks for such a point. With $c = 1 + \varepsilon$ it is also called the $\varepsilon$-approximate or $(1+\varepsilon)$-approximate nearest neighbor problem.

**$(c, r)$-approximate near neighbor, or $(c, r)$-NN.** Fix also a radius $r > 0$. The problem asks for an output $A(q)$ with these rules:

- if $\delta^*(q) \le r$, then $A(q)$ is a point $p \in P$ with $\delta(q, p) \le c r$;
- if $\delta^*(q) > c r$, then $A(q)$ is "none";
- if $r < \delta^*(q) \le c r$, then $A(q)$ is "none" or a point within $c r$.

So a returned point is always within $c r$, and "none" proves that no point is within $r$. The gap between $r$ and $c r$ is what makes the problem easier than the exact one.

**Randomized versions.** A data structure for $P$ solves the *randomized* c-ANN or $(c, r)$-NN problem with failure probability $f$ if, for each fixed query $q$, its answer is correct with probability at least $1 - f$ over the random choices of its preprocessing (and of its query). The bound is for each query, not for all queries at once. A structure with constant failure probability $f < 1$ becomes one with failure probability $f^t$ by $t$ independent copies: return the best answer, and "none" only if all copies say "none".

**k nearest.** A list $p_1, \ldots, p_k$ of distinct points of $P$ is a *c-approximate k nearest neighbor* answer if $\delta(q, p_i) \le c \cdot r_i(q)$ for each $i$, where $r_i(q)$ is the $i$-th smallest distance from $q$ to $P$.

### From the radius form to the factor form

**Proposition.** Let all distances from queries to points lie in $[a, b]$ with $0 < a \le b$, and let $\varepsilon > 0$. Let $r_i = a(1 + \varepsilon)^i$ for $i = 0, 1, \ldots, m$, with $m = \lceil \log_{1+\varepsilon}(b/a) \rceil$. Given $(c, r_i)$-NN structures $D_0, \ldots, D_m$, a c$(1+\varepsilon)$-approximate nearest neighbor can be found with $O(\log m)$ queries to them.

*Proof.* Write $D_i(q) = $ yes if $D_i$ returns a point. A "no" at $i$ means $\delta^*(q) > r_i$, by the first rule. A "yes" at $i$ returns a point within $c r_i$. Since $r_m \ge b \ge \delta^*(q)$, $D_m$ says yes. If $D_0$ says yes, its point is within $c\, r_0 = c a \le c\, \delta^*(q)$, and we are done. Else binary search on the indices keeps an interval $[lo, hi]$ with "no" at $lo$ and "yes" at $hi$: query the middle index and keep the half whose ends still differ. This needs no monotonicity, and after $O(\log m)$ queries $hi = lo + 1$. Then $\delta^*(q) > r_{lo} = r_{hi} / (1 + \varepsilon)$, and the point of $D_{hi}$ is within $c\, r_{hi} < c (1 + \varepsilon)\, \delta^*(q)$. $\square$

With randomized structures of failure probability $f$, the answer is correct with probability at least $1 - O(\log m) f$ by the [union bound](/union-bound/) over the queries made. Har-Peled, Indyk and Motwani give a reduction whose number of structures does not depend on $b/a$.

## Examples and non-examples

**On a line.** Let $P = \{0, 3, 10\} \subset \mathbb{R}$ with $\delta(x, y) = |x - y|$, and $q = 1$. The distances are 1, 2 and 9, so $\delta^*(q) = 1$.

| problem | correct outputs |
|---|---|
| exact nearest neighbor | 0 |
| c-ANN with $c = 2$ | 0 or 3 (since $2 \le 2 \cdot 1$) |
| c-ANN with $c = 1.5$ | 0 |
| $(2, 1)$-NN | 0 or 3 (a point within 1 exists, so a point within 2 is required) |
| $(2, 0.5)$-NN | "none" or 0 (no point within 0.5, but 0 is within $c r = 1$) |
| $(2, 0.25)$-NN | "none" (no point within $c r = 0.5$) |

**Non-example: a far point.** For $q = 1$ and $c = 2$, the answer 10 is wrong in each version: $9 > 2$.

**Non-example: recall is not a factor.** Systems often report *recall at k*, the fraction of the true $k$ nearest neighbors in the output. A list with recall 0 can still be a $1.01$-approximate answer when many points have almost the same distance, and a list with recall $0.9$ can hold one point at a huge distance. The two measures say different things.

**Non-example: an additive error.** "Return a point within $\delta^*(q) + \varepsilon$" is an absolute guarantee. It is not the same as a factor $c$: for a query on a stored point, $\delta^*(q) = 0$, and c-ANN must then return a point at distance 0, but the additive version may return any point within $\varepsilon$.

## Related definitions

- **[Approximate nearest neighbor search](/approximate-nearest-neighbor-search/)**: the problem page, with the known algorithms and bounds for these contracts.
- **[Locality-sensitive hash family](/locality-sensitive-hash-family/)**: an $(r, cr, p_1, p_2)$-sensitive family is defined with the same two radii $r$ and $c r$, and it gives a $(c, r)$-NN structure.
- **[Fixed-radius near neighbors](/fixed-radius-near-neighbors/)**: the exact problem of reporting all points within $r$. The $(c, r)$-NN problem asks for only one point, and accepts any point up to $c r$.
- **[Nearest neighbor search](/nearest-neighbor-search/)**: the exact problem, which is c-ANN with $c = 1$.
- **[Curse of dimensionality](/curse-of-dimensionality/)**: the reason to accept $c > 1$. In $\mathbb{R}^d$ with large $d$, exact methods with polynomial space need a query time near $n$, while $(c, r)$-NN has methods with query time $n^{\rho}$ for some $\rho < 1$ that depends on $c$.

## References
