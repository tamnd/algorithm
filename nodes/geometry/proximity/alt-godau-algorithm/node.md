---
tag: BQ9SVX
kind: algorithm
slug: alt-godau-algorithm
name: Alt-Godau algorithm
aliases:
- free-space diagram algorithm
- Alt and Godau algorithm
- free-space algorithm for the Fréchet distance
area: geometry/proximity
level: advanced
summary: Decide and compute the Fréchet distance of two polygonal curves via the free-space diagram in O(mn log(mn)) time.
solves: [frechet-distance]
model: real-ram
complexity:
  vars: {m: the number of segments of the first curve, n: the number of segments of the second curve}
  time: {decision: Θ(m n), optimization: O(m n log(m n)), this page: O((m^2 n + m n^2) log(m n))}
  space: {extra: O(m n)}
properties: {online: false, deterministic: true, exact: true}
history:
  year: 1995
  people: [Helmut Alt, Michael Godau]
  note: Alt and Godau introduced the free-space diagram, decided the Fréchet distance of polygonal curves in O(mn) time, and computed it in O(mn log(mn)) time with parametric search; Godau's 1991 thesis work and conference paper preceded the journal version.
prereqs: [frechet-distance, point-to-segment-distance, binary-search]
see_also: [hausdorff-distance, parametric-search, strong-exponential-time-hypothesis, edit-distance, euclidean-distance, conditional-lower-bound]
sources:
  - paper: doi:10.1142/S0218195995000064
    title: Helmut Alt and Michael Godau, Computing the Fréchet distance between two polygonal curves, International Journal of Computational Geometry and Applications 5(1-2), 1995, 75-91
    locator: the free-space diagram, the convexity of the free space in a cell, the O(mn) decision procedure, the critical values of types a, b and c, and the O(mn log(mn)) algorithm by parametric search
  - paper: "Thomas Eiter and Heikki Mannila, Computing discrete Fréchet distance, Technical Report CD-TR 94/64, Christian Doppler Laboratory for Expert Systems, TU Vienna, 1994"
    locator: the discrete Fréchet distance, its O(mn) dynamic program, and its relation to the continuous distance
  - paper: "Karl Bringmann, Why walking the dog takes time, Fréchet distance has no strongly subquadratic algorithms unless SETH fails, Proceedings of the 55th Annual IEEE Symposium on Foundations of Computer Science, 2014, 661-670"
    locator: the conditional lower bound under the strong exponential time hypothesis, also for small approximation factors
  - paper: "Kevin Buchin, Maike Buchin, Wouter Meulemans and Wolfgang Mulzer, Four Soviets walk the dog, improved bounds for computing the Fréchet distance, Discrete and Computational Geometry 58(1), 2017, 180-216"
    locator: the first algorithm faster than O(n^2 log n) for the continuous Fréchet distance on the real RAM
---

The Alt-Godau algorithm computes the [Fréchet distance](/frechet-distance/) between two polygonal curves $P$ with $m$ segments and $Q$ with $n$ segments. It first solves the decision problem, whether $d_F(P, Q) \le \varepsilon$, in $\Theta(mn)$ time: it builds the free-space diagram, the set of parameter pairs $(s, t)$ where $P(s)$ and $Q(t)$ are within distance $\varepsilon$, and checks by dynamic programming over its $mn$ cells whether a monotone path leads from the bottom-left to the top-right corner. Then it finds the distance itself among $O(m^2 n + m n^2)$ critical values. Searching them with the decision procedure as a test gives $O((m^2 n + mn^2) \log(mn))$ time, the version implemented here; Alt and Godau (1995) reduced this to $O(mn \log(mn))$ with [parametric search](/parametric-search/). Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) no algorithm is faster by a polynomial factor, so the method is close to optimal.

## In plain words

A person walks along one path and a dog along another, joined by a leash. Both may stop or slow down but never step back. The Fréchet distance is the shortest leash that allows both to go from start to finish.

To decide whether a given leash is long enough, draw a grid: one axis is the person's progress, the other the dog's. Mark the grid positions where the two are close enough. The leash works exactly when you can cross the marked area from the bottom-left corner to the top-right corner moving only right and up. Inside each grid square the marked part is an oval piece, so the crossing can be checked square by square.

To find the shortest leash, note that the answer only changes at a few special lengths, and test those.

## The problem

**Input.** Two polygonal curves $P = (P_0, \ldots, P_m)$ and $Q = (Q_0, \ldots, Q_n)$ with $m, n \ge 1$ segments, with integer or rational coordinates; vertices may repeat. For the decision version also $\varepsilon^2 \ge 0$.

**Output.** Whether $d_F(P, Q) \le \varepsilon$, or the value $d_F(P, Q)^2$ exactly. Here
$$d_F(P, Q) = \inf_{\alpha, \beta} \max_{u \in [0, 1]} \|P(\alpha(u)) - Q(\beta(u))\|,$$
over nondecreasing surjections $\alpha : [0, 1] \to [0, m]$ and $\beta : [0, 1] \to [0, n]$, where $P(s)$ is the point at parameter $s$, linear on each segment.

**Free space.** $F_\varepsilon = \{(s, t) \in [0, m] \times [0, n] : \|P(s) - Q(t)\| \le \varepsilon\}$. Then $d_F(P, Q) \le \varepsilon$ if and only if $F_\varepsilon$ contains a path from $(0, 0)$ to $(m, n)$ that is monotone in both coordinates; the path is the pair $(\alpha, \beta)$.

## The algorithm

The cell $(i, j)$ is $[i, i+1] \times [j, j+1]$. $L[i][j] \subseteq [0, 1]$ is the free part of its left edge, the parameters on segment $Q_j Q_{j+1}$ within $\varepsilon$ of $P_i$; $B[i][j]$ is the free part of its bottom edge, the parameters on $P_i P_{i+1}$ within $\varepsilon$ of $Q_j$. $LR$ and $BR$ are their reachable parts.

```pseudo id=main
FRECHET-DECIDE(P, Q, ε)
L1  if ‖P_0 − Q_0‖ > ε or ‖P_m − Q_n‖ > ε then return false
L2  compute every free interval L[i][j] and B[i][j] by solving a quadratic inequality
L3  set LR on the line s = 0 and BR on the line t = 0: an edge is reachable while the boundary below it is free
L4  for i ← 0 to m − 1 do
L5    for j ← 0 to n − 1 do
L6      LR[i+1][j] ← L[i+1][j] if BR[i][j] ≠ ∅, else {y ∈ L[i+1][j] : y ≥ min LR[i][j]} if LR[i][j] ≠ ∅, else ∅
L7      BR[i][j+1] ← B[i][j+1] if LR[i][j] ≠ ∅, else {x ∈ B[i][j+1] : x ≥ min BR[i][j]} if BR[i][j] ≠ ∅, else ∅
L8  return 1 ∈ LR[m][n−1] or 1 ∈ BR[m−1][n]

FRECHET-DISTANCE(P, Q)
L9   C ← the critical values of types (a), (b) and (c)
L10  sort C
L11  binary search for the smallest c ∈ C with FRECHET-DECIDE(P, Q, c)
L12  return that c
```

**Free intervals (line L2).** For a point $x$ and a segment $a + t(b - a)$, the condition $\|a + t(b - a) - x\|^2 \le \varepsilon^2$ is a quadratic inequality $\alpha t^2 + 2\beta t + \gamma \le 0$ with $\alpha = \|b - a\|^2$. Its solution is the interval between the roots $(-\beta \mp \sqrt{\beta^2 - \alpha\gamma})/\alpha$, clipped to $[0, 1]$. The endpoints are numbers $A + B\sqrt{X}$ with rational $A, B, X$; the implementation compares them exactly by squaring with sign analysis, so no floating-point roots are taken.

**Propagation (lines L6 and L7).** Within one cell the free space is convex, because it is the preimage of a disk under the affine map $(s, t) \mapsto P(s) - Q(t)$. So any reachable point on the bottom edge reaches every free point of the right edge, and a reachable point on the left edge reaches the free points of the right edge at the same height or above.

**Critical values (line L9).** As $\varepsilon$ grows, the answer can only switch from false to true at one of these values: (a) $\|P_0 - Q_0\|$ or $\|P_m - Q_n\|$; (b) the distance from a vertex of one curve to a segment of the other, where a new free interval appears; (c) for a segment of one curve and two vertices $U_k, U_l$ of the other, the distance from $U_k$ to the point where the bisector of $U_k U_l$ crosses the segment, where a horizontal or vertical passage opens. All of them are exact: their squares are rational for rational input.

## Example

Let $P = ((0,0), (4,0))$ go once from left to right and $Q = ((0,0), (4,0), (0,0), (4,0))$ go right, back and right again along the same line. The two curves cover the same set of points, so their [Hausdorff distance](/hausdorff-distance/) is $0$, but $d_F(P, Q) = 2$. With $\varepsilon = 2$, the free intervals (parameters in $[0, 1]$ along $P$ or along the segment of $Q$) are:

| edge | free interval at $\varepsilon = 2$ | reachable part |
| --- | --- | --- |
| $B[0][0]$: $Q_0 = (0,0)$ on $P$ | $[0, 1/2]$ | $[0, 1/2]$ |
| $L[1][0]$: $P_1 = (4,0)$ on $Q_0 Q_1$ | $[1/2, 1]$ | $[1/2, 1]$, since $B[0][0]$ is reachable |
| $B[0][1]$: $Q_1 = (4,0)$ on $P$ | $[1/2, 1]$ | $[1/2, 1]$, since $L[0][0] = [0, 1/2]$ is reachable |
| $L[1][1]$: $P_1$ on $Q_1 Q_2$ | $[0, 1/2]$ | $[0, 1/2]$ |
| $B[0][2]$: $Q_2 = (0,0)$ on $P$ | $[0, 1/2]$ | $[1/2, 1/2]$, only at or after $1/2$, the lowest reachable point of $B[0][1]$ |
| $L[1][2]$: $P_1$ on $Q_2 Q_3$ | $[1/2, 1]$ | $[1/2, 1]$, which contains $1$: accept |

The single point $1/2$ of $BR[0][2]$ is the whole story: the person waits at $(2,0)$, the middle of $P$, while the dog runs from $(4,0)$ back to $(0,0)$, at distance at most 2 throughout. For any $\varepsilon < 2$, the interval $B[0][2]$ ends before $1/2$ and $BR[0][1]$ starts after $1/2$, so the passage closes. The value $2$ is a critical value of type (c): the bisector of $Q_1 = (4,0)$ and $Q_2 = (0,0)$ crosses $P$ at $(2,0)$. The discrete Fréchet distance of the vertex sequences is $4$, because the walk is then forced to stand on vertices.

## Correctness

The decision procedure computes, for every cell edge, exactly the set of points reachable from $(0, 0)$ by a monotone path in $F_\varepsilon$. A path that reaches the right edge of a cell entered the closed cell for the last time through its left or bottom edge; convexity of the cell's free space makes any monotone connection between free points of the same cell free. So the induction over the cells in loop order is exact, and line L8 accepts exactly when $(m, n)$ is reachable. For the optimization, each condition for a monotone path through a given sequence of cells (endpoints free, crossed edges nonempty, crossing heights in a row nondecreasing) becomes true at a threshold of type (a), (b) or (c) and stays true; so the set of accepted $\varepsilon$ is $[d_F, \infty)$ with $d_F$ a critical value, and binary search finds it. The full argument, including the exact sign tests, is in the correctness proof below.

## Complexity

| part | time | space |
| --- | --- | --- |
| decision, lines L1 to L8 | $\Theta(mn)$ | $O(mn)$, or $O(m + n)$ keeping one column |
| critical values, line L9 | $O(m^2 n + mn^2)$ | $O(m^2 n + mn^2)$ |
| sorting and binary search, lines L10 and L11 | $O((m^2 n + mn^2) \log(mn) + mn \log(mn))$ | |
| Alt and Godau with parametric search | $O(mn \log(mn))$ | $O(mn)$ |

The type (c) values are the bottleneck of the simple search. Alt and Godau avoid listing them: parametric search simulates a parallel sorting of the interval endpoints, as functions of $\varepsilon$, and calls the decision procedure only $O(\log(mn))$ times. In practice a binary search over real $\varepsilon$ to a fixed precision, with $O(mn)$ per step, is also common.

## Properties

- **Exact on rational input.** All tests are signs of expressions $a + b\sqrt{x} + c\sqrt{y}$ with rational $a, b, c, x, y$, decided by squaring; the answer $d_F^2$ is a rational number.
- **Symmetric and invariant.** Swapping $P$ and $Q$, reversing both curves, translating both, or inserting a vertex inside a segment does not change the result.
- **Monotone in $\varepsilon$.** The decision is false below $d_F$ and true from $d_F$ on.
- **Witness.** Keeping, for each reachable interval, the cell edge it came from yields a monotone path, that is, an optimal pair of reparametrizations.

## Variants and improvements

- **Discrete Fréchet distance.** Only vertices are matched; the dynamic program of Eiter and Mannila (1994) takes $O(mn)$ time and needs no square roots. Its value is at least $d_F$ and at most $d_F$ plus the longest segment.
- **Weak Fréchet distance.** The walks may go back; the decision becomes connectivity of the free space, also $O(mn)$.
- **Closed curves.** The start point on each curve is free; Alt and Godau solve this by searching over start points in the doubled free-space diagram.
- **Faster exact algorithms.** Buchin, Buchin, Meulemans and Mulzer (2017) gave the first algorithm with $o(n^2 \log n)$ time for $m = n$ on the real RAM, an improvement by a factor of roughly $\sqrt{\log n}$.
- **Approximation and realistic inputs.** For curves that are $c$-packed or otherwise well behaved, $(1 + \varepsilon)$-approximations run in near-linear time (Driemel, Har-Peled and Wenk).
- **Higher dimension and other curve types.** The same free-space argument works for polygonal curves in $\mathbb{R}^d$ with the same bounds, and extends to surfaces only in restricted cases.

## When to use it

Use it when two curves, such as GPS trajectories, handwriting strokes or protein backbones, should be compared with their order taken into account, and the [Hausdorff distance](/hausdorff-distance/) would wrongly call a path and its back-and-forth retracing equal. For up to a few thousand vertices per curve the decision procedure is fast; for the exact value, use the critical-value search on small inputs, or a binary search on $\varepsilon$ to the needed precision on large ones. If matching vertices to vertices is enough, the discrete version is simpler and avoids square roots.

## Pitfalls

- **Forgetting monotonicity.** Connectivity of the free space is not enough; a path that goes left or down corresponds to walking backwards, which gives the weak Fréchet distance.
- **Only vertex distances.** Testing only $\|P_i - Q_j\|$ computes the discrete distance, which can be much larger; in the example it is 4 instead of 2.
- **Missing type (c) values.** Searching only types (a) and (b) returns a value that is too large whenever the optimum is a passage that opens in the middle of a row, as in the example.
- **Floating-point interval ends.** Comparing endpoints computed with `sqrt` can open or close a passage that is exactly tight at the optimum. Compare exact surds, or treat the result as approximate.
- **Degenerate segments.** A repeated vertex gives a segment of length $0$; the quadratic degenerates and its free interval is all or nothing.
- **Initialization on the boundary.** The first row and column are reachable only along the boundary of the diagram, edge after edge; treating them like interior cells can create paths that do not start at $(0, 0)$.

## Implementations

## History

Maurice Fréchet introduced the distance between curves in the early twentieth century. Alt and Godau studied its computation for polygonal curves around 1991, building on Godau's thesis work, and published the free-space diagram, the $O(mn)$ decision procedure and the $O(mn \log(mn))$ algorithm in 1995. Eiter and Mannila introduced the discrete version in 1994. For two decades no faster algorithm was found, until Buchin, Buchin, Meulemans and Mulzer gained a sublogarithmic factor in 2014, and Bringmann (2014) showed that a strongly subquadratic algorithm would refute the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/).

## References
