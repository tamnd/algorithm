---
tag: SNS1K9
kind: algorithm
slug: lp-rounding-vertex-cover
name: LP-rounding 2-approximation for vertex cover
aliases:
- LP-based vertex cover
- Hochbaum vertex cover rounding
- threshold 1/2 rounding for vertex cover
area: approximation/lp-rounding
level: core
summary: Solve the LP relaxation of weighted vertex cover and take every vertex whose LP value is at least 1/2; the cover has weight at most twice the LP value, so at most twice the optimum.
solves: [weighted-vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: poly(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [Dorit S. Hochbaum]
  note: Hochbaum (1982) rounded the LP of weighted set cover and vertex cover at the threshold 1/f, which is 1/2 for vertex cover.
prereqs: [weighted-vertex-cover, lp-relaxation, linear-programming-rounding]
see_also: [half-integrality, threshold-rounding, frequency-rounding-set-cover, primal-dual-weighted-vertex-cover, bar-yehuda-even-vertex-cover, vertex-cover-2-approximation, integrality-gap, vertex-cover-inapproximability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.4 (approximating weighted vertex cover by linear programming)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.3 (a deterministic rounding algorithm for set cover, with vertex cover as the case f = 2)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 14, Sections 14.1 and 14.3 (simple rounding and half-integrality of vertex cover)
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349
---

LP rounding for [weighted vertex cover](/weighted-vertex-cover/) solves the [LP relaxation](/lp-relaxation/) of the problem and puts each vertex with LP value at least $1/2$ into the cover. The cover has weight at most $2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}$ in the worst case, and the algorithm runs in polynomial time. It is the simplest example of [LP rounding](/linear-programming-rounding/) and of [threshold rounding](/threshold-rounding/), and the ratio 2 is the best known for the problem: under the [Unique Games Conjecture](/unique-games-conjecture/), no polynomial-time algorithm has ratio $2 - \varepsilon$.

## In plain words

Each point of a network has a price, and you must buy points so that each link touches a bought point. First solve an easier problem: you may buy a fraction of a point, and each link must be covered by fractions that add up to at least one whole. A computer finds the cheapest fractional answer fast.

Now look at each link. Its two fractions add up to at least one, so at least one of them is at least one half. Buy every point whose fraction is at least one half. Each link is then covered. Each bought point costs at most twice its fractional price, so the total is at most twice the fractional cost, and the fractional cost is never more than the best real cost.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges, no self-loops, and weights $w(v) \ge 0$. The output is a vertex cover $C \subseteq V$, a set with at least one endpoint of each edge. The goal is a small weight $w(C) = \sum_{v \in C} w(v)$. The algorithm uses the LP relaxation of the integer program:

$$\text{LP}^* = \min \sum_{v \in V} w(v)\, x_v \quad \text{subject to} \quad x_u + x_v \ge 1 \text{ for each } \{u, v\} \in E, \qquad x_v \ge 0 \text{ for each } v.$$

Each cover $C$ gives the feasible point $x = \mathbf{1}_C$ with value $w(C)$, so $\text{LP}^* \le \text{OPT}$. This is the lower bound that the analysis compares with. The ratio convention is ALG $\le \rho \cdot$ OPT with $\rho \ge 1$.

## The algorithm

```pseudo id=main
LP-ROUND-VC(G = (V, E), w)
L1  x ← an optimal solution of the vertex cover LP     ▷ by the ellipsoid or an interior point method
L2  C ← ∅
L3  for each v in V do
L4      if x_v ≥ 1/2 then C ← C ∪ {v}
L5  return C
```

Line L1 is the only costly step. The LP has $n$ variables and $m + n$ constraints, so it has a polynomial size, and it is solved in polynomial time; no separation oracle is needed. Lines L2 to L4 are [threshold rounding](/threshold-rounding/) at the threshold $1/2$. The algorithm does not need a vertex solution of the LP; any optimal solution, or even any feasible solution $x$, gives a cover of weight at most $2 \sum_v w(v) x_v$.

## Example

The graph has 6 vertices and 7 edges: 1-3, 1-4, 2-4, 2-5, 3-4, 4-6 and 5-6. The vertices 1, 3 and 4 form a triangle.

| vertex | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| weight $w(v)$ | 4 | 1 | 6 | 6 | 8 | 3 |
| LP value $x_v$ | 1/2 | 1 | 1/2 | 1/2 | 0 | 1 |
| $x_v \ge 1/2$? | yes | yes | yes | yes | no | yes |

The simplex method returns this optimal vertex of the LP. Its value is $4 \cdot \tfrac12 + 1 + 6 \cdot \tfrac12 + 6 \cdot \tfrac12 + 0 + 3 = 12$. The dual solution $y_{13} = 2$, $y_{14} = 2$, $y_{25} = 1$, $y_{34} = 4$, $y_{56} = 3$ and $y_e = 0$ on the edges 2-4 and 4-6 packs each vertex within its weight and has the value 12 too, so LP* $= 12$ by [weak duality](/weak-duality/).

The rounding takes $C = \{1, 2, 3, 4, 6\}$ with weight $4 + 1 + 6 + 6 + 3 = 20 \le 2 \cdot 12 = 24$. The optimum is $\{1, 2, 3, 6\}$ with weight 14, so the ratio of this run is $20/14 \approx 1.43$. The loss comes from the triangle: the LP pays one half for each of its three vertices, and the rounding buys all three, but a cover needs only two.

## Correctness

**Theorem (Hochbaum 1982).** For each feasible solution $x$ of the vertex cover LP, the set $C = \{v : x_v \ge 1/2\}$ is a vertex cover with $w(C) \le 2 \sum_v w(v) x_v$. If $x$ is optimal, then $w(C) \le 2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}$.

For an edge $\{u, v\}$, the constraint $x_u + x_v \ge 1$ gives $\max(x_u, x_v) \ge 1/2$, so an endpoint is in $C$. For each $v \in C$, $1 \le 2 x_v$, and $w(v) \ge 0$, so $w(v) \le 2 w(v) x_v$; the sum over $C$ is at most the sum over $V$. The full proof is in the proof file below.

**Tight examples.** The bound 2 is tight for the algorithm, even with a vertex solution. On the odd cycle $C_{2k+1}$ with unit weights, adding the $2k + 1$ edge constraints gives $2 \sum_v x_v \ge 2k + 1$, with equality only if every constraint is tight, and tight constraints around an odd cycle force $x_v = 1/2$ for all $v$. So the LP has the unique optimum $x = (1/2, \ldots, 1/2)$, the rounding takes all $2k + 1$ vertices, and OPT $= k + 1$. The ratio $(2k+1)/(k+1)$ tends to 2. The analysis also cannot improve, because the [integrality gap](/integrality-gap/) of the LP is 2: on the complete graph $K_n$ with unit weights, LP* $= n/2$ and OPT $= n - 1$, and the ratio $2 - 2/n$ tends to 2.

**Hardness.** Vertex cover is NP-hard to approximate within 1.3606 (Dinur and Safra 2005) and within $\sqrt{2} - \varepsilon$ (Khot, Minzer and Safra 2018), and within $2 - \varepsilon$ under the Unique Games Conjecture (Khot and Regev 2008). See [vertex cover inapproximability](/vertex-cover-inapproximability/).

## Complexity

- **Time.** The LP has $n$ variables, $m + n$ constraints and coefficients 0 and 1. The [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) solves it in time polynomial in $n + m$ and the bit size of the weights, in the worst case; see [linear programming is in P](/lp-in-p/). The rounding of lines L2 to L4 takes $\Theta(n)$ time. The total is poly$(n + m)$ for weights of polynomial bit size. A faster exact method uses a minimum cut, see the variants.
- **Space.** The LP data and the solution take $\Theta(n + m)$ space, besides the work space of the LP solver.

## Properties

- **Deterministic.** The output depends only on the LP solution that line L1 returns.
- **A certificate.** The value LP* is a lower bound on OPT, so each run reports its own ratio $w(C)/\text{LP}^*$, which is at most 2.
- **Half-integral input.** If $x$ is a vertex of the LP, then $x_v \in \{0, 1/2, 1\}$ for each $v$, by [half-integrality](/half-integrality/). The cover is then $\{v : x_v > 0\}$, and the vertices with $x_v = 1$ belong to some optimal cover.
- **Not minimal.** The cover may hold redundant vertices. A pass that drops each vertex whose neighbours are all in the cover keeps the bound and often lowers the weight.

## Variants and improvements

- **Rounding by a minimum cut.** The LP optimum is half the weight of a minimum vertex cover of the bipartite double cover of $G$, which a minimum cut finds. This gives a half-integral optimal $x$ with no LP solver; see [half-integrality](/half-integrality/).
- **Set cover.** The same rounding at the threshold $1/f$ gives ratio $f$ for set cover, where $f$ is the largest [element frequency](/element-frequency/); see [frequency rounding for set cover](/frequency-rounding-set-cover/).
- **No LP at all.** The [primal-dual algorithm](/primal-dual-weighted-vertex-cover/) and the [Bar-Yehuda and Even algorithm](/bar-yehuda-even-vertex-cover/) reach ratio 2 in linear time, by a feasible dual in place of the LP optimum. For unit weights, the [maximal matching algorithm](/vertex-cover-2-approximation/) gives 2.
- **Better ratios on special graphs.** For graphs with no odd cycle the LP is integral, so the rounding is exact. With extra steps that remove short odd cycles, the ratio improves to $2 - \Theta(\log \log n / \log n)$ (Bar-Yehuda and Even 1985; Monien and Speckenmeyer 1985).

## When to use it

Use LP rounding when an LP solver is at hand and you also want the bound LP* to judge the result, or when the vertex cover constraints are part of a larger LP. When speed matters, the primal-dual algorithm gives the same ratio in linear time without an LP. When the graph is bipartite, solve the problem exactly by a minimum cut or by [König's theorem](/konig-theorem/). When the cover must be optimal, use the half-integral solution to fix vertices first, then search; see [half-integrality](/half-integrality/).

## Pitfalls

- **Rounding with $>$ in place of $\ge$.** The test $x_v > 1/2$ in line L4 is wrong: on the triangle with $x = (1/2, 1/2, 1/2)$ it returns the empty set, which covers no edge. Use $x_v \ge 1/2$. The odd cycle test case catches this.
- **Floating-point LP values.** A solver may return $0.4999999$ for a value that is $1/2$. Then $x_v \ge 1/2$ fails, and an edge may stay uncovered. Use exact arithmetic, or compare with a tolerance, $x_v \ge 1/2 - \varepsilon$, and then check the cover.
- **The upper bounds $x_v \le 1$.** They are not needed. With weights $w \ge 0$, a solution with $x_v > 1$ can be cut down to 1 without loss, and the rounding takes $v$ in both cases.
- **Negative weights.** With $w(v) < 0$, the step $w(v) \le 2 w(v) x_v$ fails. A vertex of negative weight should always be taken, so add it first and delete its edges.

## Implementations

The Python code solves the LP with a small exact simplex method in rational arithmetic, which is for small graphs only.

## History

Hochbaum (1982) gave the rounding of the set cover LP at the threshold $1/f$, which is the threshold $1/2$ for vertex cover, together with the use of the dual to get the same bound. Nemhauser and Trotter (1975) had already shown that the vertex cover LP has half-integral vertex solutions, and that the vertices of value 1 can be fixed in an optimal cover. Bar-Yehuda and Even (1981) gave a linear-time algorithm with the same ratio. The hardness of $2 - \varepsilon$ under the Unique Games Conjecture is due to Khot and Regev (2008).

## References
