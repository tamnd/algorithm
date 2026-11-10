---
tag: V1VWVP
kind: algorithm
slug: bar-yehuda-even-vertex-cover
name: Bar-Yehuda-Even vertex cover
aliases:
- local ratio vertex cover
- Bar-Yehuda-Even algorithm
- weight subtraction for vertex cover
area: approximation/lp-rounding
level: core
summary: A linear-time local-ratio 2-approximation for weighted vertex cover that subtracts the smaller end weight at each edge and takes the vertices whose weight reaches zero.
solves: [weighted-vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1981
  people: [Reuven Bar-Yehuda, Shimon Even]
  note: Bar-Yehuda and Even (1981) gave the linear-time 2-approximation; their 1985 paper stated the local ratio theorem behind it.
prereqs: [weighted-vertex-cover, local-ratio-technique, lp-duality]
see_also: [primal-dual-weighted-vertex-cover, lp-rounding-vertex-cover, half-integrality, set-cover-primal-dual, frequency-rounding-set-cover, vertex-cover-inapproximability, unique-games-conjecture, weak-duality]
sources:
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - title: Reuven Bar-Yehuda and Shimon Even, A local-ratio theorem for approximating the weighted vertex cover problem, Annals of Discrete Mathematics 25, 1985
    locator: pages 27 to 45 (the local ratio theorem and the ratio 2 − log log n / (2 log n))
  - title: Reuven Bar-Yehuda, Keren Bendel, Ari Freund and Dror Rawitz, Local ratio, a unified framework for approximation algorithms, ACM Computing Surveys 36(4), 2004
    locator: Section 2 (vertex cover as the first example)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 7, Section 7.1 (the primal-dual method for set cover)
---

The Bar-Yehuda-Even algorithm is a 2-approximation for [weighted vertex cover](/weighted-vertex-cover/) that runs in linear time and solves no LP. It scans the edges once. At each edge it subtracts the smaller of the two current end weights from both ends, so at least one end drops to weight 0, and it returns the vertices whose weight reached 0. The cover has weight at most $2 \cdot \text{OPT}$ in the worst case. The proof is the first use of the [local ratio technique](/local-ratio-technique/); read with dual variables, the same steps are the [primal-dual algorithm](/primal-dual-weighted-vertex-cover/). The ratio 2 is tight for the algorithm, and under the [Unique Games Conjecture](/unique-games-conjecture/) no polynomial-time algorithm has ratio $2 - \varepsilon$.

## In plain words

Each vertex has a price, and each edge needs one of its two ends in the cover. Go through the edges one at a time. At an edge, look at the cheaper of its two ends, and lower both prices by that amount. Now one end is free. When all edges are done, take every free vertex.

Each edge has a free end, so the free vertices cover all edges. Each amount you took off could be charged to any cover once, since each cover must hold an end of that edge. Your cover pays it at most twice, once at each end. So your cover costs at most twice what the best cover costs.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges, without self-loops, and weights $w(v) \ge 0$. The output is a vertex cover $C \subseteq V$, which is a set that contains an end of each edge. The goal is a small weight $w(C) = \sum_{v \in C} w(v)$. The ratio convention is ALG $\le \rho \cdot$ OPT with $\rho \ge 1$. The lower bound of the analysis is the sum of the amounts taken off, which is the value of a feasible solution of the dual of the vertex cover LP.

## The algorithm

```pseudo id=main
BAR-YEHUDA-EVEN(G, w)
L1  for each v ∈ V do r(v) ← w(v)              ▷ residual weights
L2  for each edge uv ∈ E, in any order do
L3      ε ← min(r(u), r(v))
L4      r(u) ← r(u) − ε;  r(v) ← r(v) − ε
L5  C ← {v ∈ V : r(v) = 0}
L6  return C
```

Line L3 is the largest amount that keeps both residual weights nonnegative. After line L4, one end of $uv$ has residual weight 0, and residual weights never go up, so this end is still in $C$ at line L5. In local ratio terms, line L4 splits the weight function as $w = \delta_{uv} + w'$, where $\delta_{uv}$ puts $\varepsilon$ on $u$ and on $v$ and 0 elsewhere. Each cover pays between $\varepsilon$ and $2\varepsilon$ for $\delta_{uv}$, so each cover is a 2-approximation for $\delta_{uv}$.

## Example

The graph has the vertices 1 to 5 with weights $w = (3, 5, 2, 4, 6)$ and the edges below, scanned in this order.

| edge | $\varepsilon$ | $r$ after the step |
|---|---|---|
| start | | (3, 5, 2, 4, 6) |
| 1-2 | 3 | (0, 2, 2, 4, 6) |
| 1-3 | 0 | (0, 2, 2, 4, 6) |
| 2-3 | 2 | (0, 0, 0, 4, 6) |
| 2-4 | 0 | (0, 0, 0, 4, 6) |
| 3-5 | 0 | (0, 0, 0, 4, 6) |
| 4-5 | 4 | (0, 0, 0, 0, 2) |

The algorithm returns $C = \{1, 2, 3, 4\}$ with weight $3 + 5 + 2 + 4 = 14$. The amounts add up to $3 + 2 + 4 = 9$, so each cover weighs at least 9 and $w(C) \le 18$. Here the bound 9 is exact: $\{1, 3, 4\}$ is a cover of weight 9, so OPT $= 9$ and the run has ratio $14/9 \approx 1.56$. Vertex 2 is redundant in $C$, since its edges 1-2, 2-3 and 2-4 have their other ends in $C$; removing it gives the optimum in this case.

## Correctness

**Theorem (Bar-Yehuda and Even 1981).** BAR-YEHUDA-EVEN returns a vertex cover $C$ with $w(C) \le 2 \sum_{e} \varepsilon_e \le 2 \cdot \text{OPT}$, where $\varepsilon_e$ is the amount of line L3 at edge $e$.

The weight splits as $w = \sum_e \varepsilon_e (\mathbf{1}_u + \mathbf{1}_v) + r$ with $r \ge 0$ at the end. Each cover $S$ has $w(S) \ge \sum_e \varepsilon_e$, since $S$ holds an end of each edge. The returned cover has $r(C) = 0$ and pays each $\varepsilon_e$ at most twice, so $w(C) \le 2 \sum_e \varepsilon_e$. The full proof is in the proof file below.

**The dual view.** The amounts $y_e = \varepsilon_e$ satisfy $\sum_{e \ni v} y_e = w(v) - r(v) \le w(v)$, so they are a feasible solution of the dual LP $\max \sum_e y_e$ subject to $\sum_{e \ni v} y_e \le w(v)$ and $y \ge 0$. By [weak duality](/weak-duality/), $\sum_e \varepsilon_e \le \text{LP}^* \le \text{OPT}$. The vertices of $C$ are the vertices whose dual constraint is tight, as in the [primal-dual algorithm](/primal-dual-weighted-vertex-cover/).

**Tight examples.** A single edge with weights $(1, 1)$ gives $\varepsilon = 1$, $C$ with both ends, weight 2, and OPT $= 1$. With weights, take a star with centre 0 of weight 5, one leaf 1 of weight 5 and three leaves of weight 1, with the edge 0-1 first. The first step takes 5 off both, so $C = \{0, 1\}$ with weight 10, while the centre alone is a cover of weight 5. So the ratio 2 of the algorithm is tight. The lower bound $\sum_e \varepsilon_e$ is at most $\text{LP}^*$, and the [integrality gap](/integrality-gap/) of $K_n$ is $2 - 2/n$, so no analysis against this bound gives less than 2 in general.

**Hardness.** Vertex cover is NP-hard to approximate within $1.3606$ (Dinur and Safra 2005) and within $\sqrt{2} - \varepsilon$ (Khot, Minzer and Safra 2018), and within $2 - \varepsilon$ under the Unique Games Conjecture (Khot and Regev 2008); see [vertex cover inapproximability](/vertex-cover-inapproximability/).

## Complexity

- **Time.** Line L1 takes $\Theta(n)$ time and the loop of lines L2 to L4 does $O(1)$ work per edge, so the time is $\Theta(n + m)$ in the worst case on the word RAM, with each weight in one word. No LP is solved, and no separation oracle is needed.
- **Space.** The graph takes $\Theta(n + m)$ space and the residual weights $\Theta(n)$ more.

## Properties

- **Deterministic.** The output depends on the order of the edges, but the bound holds for each order.
- **One pass.** Each edge is read once, in any order, so the algorithm also works in a stream of edges with $\Theta(n)$ memory for the residual weights.
- **A certificate.** The sum $\sum_e \varepsilon_e$ is a lower bound on OPT, so each run reports its own ratio $w(C) / \sum_e \varepsilon_e \le 2$.
- **Unit weights.** With all weights 1, each step with $\varepsilon = 1$ puts both ends of an edge into $C$, and these edges form a maximal matching. The algorithm is then the classic maximal matching 2-approximation for [vertex cover](/vertex-cover/).

## Variants and improvements

- **Remove redundant vertices.** After line L5, drop vertices of $C$ whose edges are all covered by other vertices of $C$, in the reverse order of the step that made them free. The ratio stays 2 in the worst case, but the cover is minimal, and in practice it is often lighter, as in the example.
- **Small odd cycles first.** Bar-Yehuda and Even (1985) first take local ratio steps on short odd cycles, where each cover pays at least half the cycle weight, and got the ratio $2 - \frac{\log \log n}{2 \log n}$. Karakostas (2009) reached $2 - \Theta(1 / \sqrt{\log n})$ with a stronger LP.
- **Set cover.** The same steps on the sets of each element give ratio $f$ for [set cover](/set-cover/) with largest frequency $f$; this is the [primal-dual set cover algorithm](/set-cover-primal-dual/). The [frequency rounding](/frequency-rounding-set-cover/) gives the same ratio with an LP solve.
- **LP rounding.** [LP rounding for vertex cover](/lp-rounding-vertex-cover/) also gives ratio 2, against the stronger lower bound $\text{LP}^*$, but needs an LP solver or a max flow.

## When to use it

Use it when you need a fast cover with a proved ratio 2 for weighted vertex cover, for large graphs or for edges that arrive in a stream. It needs no LP solver and no sorting. When the graph fits in memory and a few percent matter, run it as a first step, then remove redundant vertices, or solve the LP and use [half-integrality](/half-integrality/) to fix part of an optimal cover.

## Pitfalls

- **Taking the wrong vertices.** $C$ is the set of vertices with residual weight 0, not the set of vertices touched by a step with $\varepsilon > 0$. In the example, the step at edge 4-5 touches vertex 5, but its residual weight stays 2; adding it would cost 6 more.
- **Zero weights.** A vertex of weight 0 has residual weight 0 from the start and is in $C$ even if it is isolated. This costs nothing, but code that counts the size of the cover must expect it.
- **Floating-point weights.** With floats, $r(u) - \varepsilon$ can end at a tiny positive number, and then neither end of an edge tests as 0. Use integers or exact fractions, or test the end that gave the minimum in line L3, not the value.
- **Self-loops.** An edge $vv$ needs $v$ in each cover; the step of line L4 would subtract $\varepsilon$ twice from the same vertex. Put such vertices into $C$ first, or reject the input.

## Implementations

The Python code keeps the residual weights in a list and returns the cover together with the amounts $\varepsilon_e$ and the residual weights, so a caller can read off the lower bound $\sum_e \varepsilon_e$.

## History

Bar-Yehuda and Even (1981) gave this algorithm as the first linear-time 2-approximation for weighted vertex cover, a year before Hochbaum's LP rounding. In 1985 they stated the local ratio theorem, which explains the algorithm as a sum of weight functions on which every cover is a 2-approximation, and used it for the ratio $2 - \frac{\log \log n}{2 \log n}$. Bar-Yehuda, Bendel, Freund and Rawitz (2004) surveyed the local ratio technique, and Bar-Yehuda and Rawitz (2005) showed that it is equivalent to the primal-dual method.

## References
