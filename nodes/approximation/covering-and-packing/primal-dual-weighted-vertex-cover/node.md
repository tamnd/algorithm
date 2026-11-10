---
tag: 7D7Y44
kind: algorithm
slug: primal-dual-weighted-vertex-cover
name: Primal-dual 2-approximation for weighted vertex cover
aliases:
- Bar-Yehuda and Even algorithm
- local ratio vertex cover
- pricing method for vertex cover
area: approximation/covering-and-packing
level: advanced
summary: Scan the edges and raise the dual of each uncovered edge until an endpoint becomes tight; the tight vertices form a cover of weight at most twice the optimum, in linear time.
solves: [weighted-vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1981
  people: [Reuven Bar-Yehuda, Shimon Even]
  note: Bar-Yehuda and Even (1981) gave this linear-time 2-approximation; Kleinberg and Tardos present it as the pricing method.
prereqs: [weighted-vertex-cover, dual-linear-program, weak-duality, complementary-slackness]
see_also: [bar-yehuda-even-vertex-cover, set-cover-primal-dual, vertex-cover-2-approximation, lp-rounding-vertex-cover, local-ratio-technique, primal-dual-approximation, vertex-cover-inapproximability]
sources:
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 11, Section 11.4 (the pricing method, vertex cover)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.5 (the primal-dual algorithm for set cover, with vertex cover as the case f = 2), and Chapter 7 (the primal-dual method)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 15 (the primal-dual schema; weighted vertex cover as the case f = 2 of set cover)
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349
---

The primal-dual algorithm for [weighted vertex cover](/weighted-vertex-cover/) scans the edges once. When an edge has no endpoint in the cover yet, it raises the dual variable of the edge until one endpoint is paid for in full, and it puts each fully paid endpoint into the cover. The cover has weight at most $2 \cdot$ OPT, and the algorithm runs in linear time without solving an LP. It is the case $f = 2$ of the [primal-dual set cover algorithm](/set-cover-primal-dual/), and also the [local ratio](/local-ratio-technique/) algorithm of Bar-Yehuda and Even. The ratio 2 is tight for the algorithm, and under the [Unique Games Conjecture](/unique-games-conjecture/) no polynomial-time algorithm has ratio $2 - \varepsilon$.

## In plain words

Each point of a network has a price, and you must buy points so that each link touches a bought point. Each link can pay money toward its two ends. Take the links one by one. When a link touches no bought point, it pays the same amount to both of its ends, as much as it can until one end is paid in full. Buy each point that is paid in full.

Each bought point is paid only by its own links, and each link pays to at most two bought points. The total paid by the links is at most the price of the best choice, because the best choice must touch each link. So the bought points cost at most twice the best price.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges, no self-loops, and weights $w(v) \ge 0$. The output is a vertex cover $C$, a set with an endpoint of each edge. The goal is a small weight $w(C) = \sum_{v \in C} w(v)$. The algorithm uses the [dual](/dual-linear-program/) of the [LP relaxation](/lp-relaxation/):

$$\max \sum_{e \in E} y_e \quad \text{subject to} \quad \sum_{e \ni v} y_e \le w(v) \text{ for each } v, \qquad y \ge 0.$$

A vertex is *tight* when its constraint holds with equality. OPT is the least weight of a cover, LP* is the LP optimum, and the ratio convention is ALG $\le \rho \cdot$ OPT.

## The algorithm

```pseudo id=main
PRIMAL-DUAL-WVC(G = (V, E), w)
L1  r[v] ← w(v) for each v, C ← ∅            ▷ r[v] is the residual w(v) − Σ_{e ∋ v} y_e
L2  for each edge e = {u, v} in E, in any order do
L3      if u ∈ C or v ∈ C then y_e ← 0, continue
L4      δ ← min(r[u], r[v])
L5      y_e ← δ, r[u] ← r[u] − δ, r[v] ← r[v] − δ
L6      add to C each endpoint x of e with r[x] = 0
L7  return C, y
```

Line L4 computes the largest raise of $y_e$ that keeps the dual feasible. After line L5, at least one endpoint has residual 0, so line L6 covers the edge. If both residuals were equal, both endpoints enter $C$. The edge order in line L2 can be any order; it changes the output but not the bound.

## Example

The graph is the one of the [maximal matching algorithm](/vertex-cover-2-approximation/) page, now with weights.

| vertex | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 5 | 2 | 6 | 3 | 2 |

The table shows the residuals after each edge that raises its dual. The edges 2-3, 2-4, 4-6 and 5-7 are skipped by line L3, because an endpoint is in $C$ when they are visited.

| edge | $\delta$ | $r_1$ | $r_2$ | $r_3$ | $r_4$ | $r_5$ | $r_6$ | $r_7$ | added to $C$ |
|---|---|---|---|---|---|---|---|---|---|
| start | | 4 | 3 | 5 | 2 | 6 | 3 | 2 | |
| 1-2 | 3 | 1 | 0 | 5 | 2 | 6 | 3 | 2 | 2 |
| 1-3 | 1 | 0 | 0 | 4 | 2 | 6 | 3 | 2 | 1 |
| 3-5 | 4 | 0 | 0 | 0 | 2 | 2 | 3 | 2 | 3 |
| 4-5 | 2 | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 4, 5 |
| 6-7 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 |

The cover is $C = \{1, 2, 3, 4, 5, 7\}$ with weight $4 + 3 + 5 + 2 + 6 + 2 = 22$. The dual value is $3 + 1 + 4 + 2 + 2 = 12$, so the bound is $2 \cdot 12 = 24$. The optimum is $\{2, 3, 4, 7\}$ with weight 12, and LP* $= 12$, so the dual is optimal on this instance and the ratio of this run is $22/12 \approx 1.83$. The cover is not minimal: the vertices 1 and 5 are redundant. A reverse delete pass that visits $C$ in the reverse order of addition (7, 5, 4, 3, 1, 2) drops 5 and then 1, and leaves the optimum $\{2, 3, 4, 7\}$.

## Correctness

The algorithm keeps two invariants: $y$ is dual feasible, because line L4 raises $y_e$ by the smaller residual of its two endpoints, and each vertex of $C$ is tight, because line L6 adds only tight vertices and a later raise never touches a vertex of $C$. Each edge is covered after its visit.

**Theorem (Bar-Yehuda and Even 1981).** PRIMAL-DUAL-WVC returns a vertex cover of weight at most $2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}$, in the worst case.

Each vertex of $C$ is tight, so its weight is the sum of the duals of its edges, and each edge is counted at most twice:

$$w(C) = \sum_{v \in C} \sum_{e \ni v} y_e = \sum_{e} y_e \, |e \cap C| \le 2 \sum_{e} y_e \le 2 \cdot \text{LP}^*.$$

The last step is [weak duality](/weak-duality/). The full proof is in the proof file below.

**The lower bound used.** ALG is compared with the value of the dual $y$, a fractional packing of edges into the vertex weights. This is at most LP* $\le$ OPT.

**Tight examples.** The ratio 2 is tight. With unit weights, on the complete bipartite graph $K_{k,k}$, each raise makes both endpoints tight, the raised edges form a perfect matching, and the cover has all $2k$ vertices, while OPT $= k$. The LP lower bound itself limits any such analysis: on the complete graph $K_n$ with unit weights, LP* $= n/2$ and OPT $= n - 1$.

**Hardness.** Weighted vertex cover is as hard as the unit case: 1.3606 and $\sqrt{2} - \varepsilon$ are NP-hard, and $2 - \varepsilon$ is hard under the Unique Games Conjecture. See [vertex cover inapproximability](/vertex-cover-inapproximability/).

## Complexity

- **Time.** Each edge needs $O(1)$ work: two membership tests, a minimum and two subtractions. The residual array costs $\Theta(n)$ to set up. The total is $\Theta(n + m)$ in the worst case, in the [word RAM](/word-ram/) with weights that fit in a word.
- **Space.** The residuals and the flags for $C$ take $\Theta(n)$ extra space. The duals $y$ take $\Theta(m)$ more if they are kept.

## Properties

- **Deterministic.** For a fixed edge order, the output depends only on the input.
- **Online.** Each edge is read once and its dual is fixed at once, so the algorithm works on an edge stream.
- **A certificate.** The value $\sum_e y_e$ is a lower bound on OPT, and it comes with each run.
- **Unit weights.** With unit weights, each raise has $\delta = 1$ and makes both endpoints tight, so the algorithm is the [maximal matching algorithm](/vertex-cover-2-approximation/).
- **Zero weights.** A vertex of weight 0 enters $C$, at no cost, at the first uncovered edge that it touches.

## Variants and improvements

- **Local ratio.** Subtract $\delta$ from the weights of both endpoints in place of raising $y_e$. The steps are the same, and the proof uses the local ratio theorem in place of LP duality; see [Bar-Yehuda and Even vertex cover](/bar-yehuda-even-vertex-cover/) and the [local ratio technique](/local-ratio-technique/).
- **Reverse delete.** Drop redundant vertices after the scan, in the reverse order of addition. The result is a minimal cover, often much lighter, and the bound 2 still holds.
- **LP rounding.** Solve the LP and take each $v$ with $x_v \ge 1/2$. This is [LP rounding for vertex cover](/lp-rounding-vertex-cover/), with the same ratio 2 and an LP solve. The LP has an optimal solution with values in $\{0, 1/2, 1\}$; see [half-integrality](/half-integrality/).
- **Set cover.** The same steps on a set system give ratio $f$, the largest [element frequency](/element-frequency/); see [primal-dual set cover](/set-cover-primal-dual/).
- **The general method.** The [primal-dual method](/primal-dual-approximation/) and the [primal-dual schema](/primal-dual-schema/) extend the idea to network design and facility location.

## When to use it

Use the primal-dual algorithm for weighted vertex cover when you need a fast answer with a guarantee. It is linear time, uses no LP solver, works on an edge stream, and reports a lower bound. Add the reverse delete pass. When the graph is bipartite, solve the problem exactly by a minimum cut. When the cover must be optimal and OPT is small or the graph is small, use an exact method and start it with this cover.

## Pitfalls

- **Taking both endpoints.** With weights, taking both endpoints of an uncovered edge, as in the unit case, has no bounded ratio: one endpoint may be very heavy. Take only the tight endpoints.
- **Raising a covered edge.** An edge with an endpoint in $C$ must get $y_e = 0$. Raising it adds load to a tight vertex and breaks dual feasibility, and the proof fails.
- **Floating-point residuals.** The test $r[x] = 0$ needs exact arithmetic. Use integer or rational weights, or a tolerance followed by a check of the cover.
- **Negative weights.** A vertex with $w(v) < 0$ should always be taken; the algorithm assumes $w \ge 0$, and the implementation rejects negative weights.

## Implementations

## History

Bar-Yehuda and Even (1981) gave this algorithm as a linear-time 2-approximation for weighted vertex cover, with the ratio $f$ for weighted set cover. Hochbaum (1982) found the ratio 2 by rounding the LP at about the same time. Bar-Yehuda and Even (1985) stated the local ratio theorem, which explains the same algorithm without LP. Kleinberg and Tardos call it the pricing method, and the books of Vazirani and of Williamson and Shmoys use it to introduce the primal-dual method.

## References
