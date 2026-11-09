---
tag: DRSQ2X
kind: problem
slug: euclidean-steiner-tree-problem
name: Euclidean Steiner tree problem
aliases:
- Steiner minimal tree in the plane
- Steiner tree problem in the plane
- Euclidean Steiner minimal tree
area: geometry/geometric-optimization
level: core
summary: Find the shortest network that connects n points in the plane, with extra junction points allowed. It is NP-hard, junctions meet at 120 degrees, and it has a PTAS.
prereqs: [euclidean-minimum-spanning-tree, fermat-point, steiner-tree-problem]
see_also: [steiner-ratio, rectilinear-steiner-tree-problem, fermat-point, euclidean-minimum-spanning-tree, steiner-tree-problem, arora-euclidean-tsp-ptas, ptas, geometric-median]
sources:
  - paper: "E. N. Gilbert and H. O. Pollak, Steiner minimal trees, SIAM Journal on Applied Mathematics 16(1), 1968, 1 to 29"
    locator: the degree and 120 degree angle conditions, the bound of n − 2 Steiner points, and the Steiner ratio conjecture
  - paper: doi:10.1137/0132072
    title: M. R. Garey, R. L. Graham and D. S. Johnson, The complexity of computing Steiner minimal trees, SIAM Journal on Applied Mathematics 32(4), 1977
    locator: NP-hardness of the Euclidean Steiner tree problem
  - paper: "Z. A. Melzak, On the problem of Steiner, Canadian Mathematical Bulletin 4(2), 1961, 143 to 148"
    locator: the finite construction of a full Steiner tree for a given topology by equilateral triangles
  - paper: doi:10.1145/290179.290180
    title: Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998
    locator: the polynomial-time approximation scheme for the Euclidean Steiner tree problem in fixed dimension
  - paper: "Frank K. Hwang, Dana S. Richards and Pawel Winter, The Steiner Tree Problem, Annals of Discrete Mathematics 53, North-Holland, 1992"
    locator: Part I, the Euclidean Steiner problem (properties of Steiner minimal trees, full topologies, exact algorithms)
  - paper: "David M. Warme, Pawel Winter and Martin Zachariasen, Exact algorithms for plane Steiner tree problems, a computational study, in Advances in Steiner Trees, Kluwer, 2000"
    locator: the GeoSteiner method of full Steiner tree generation and concatenation
---

The Euclidean Steiner tree problem asks for the shortest network that connects $n$ given points, the terminals, in the plane, where the network may use extra junction points, called Steiner points. The answer, a Steiner minimal tree, is a tree whose Steiner points have three edges meeting at 120 degrees; for three points it is the [Fermat point](/fermat-point/) construction. The problem is NP-hard (Garey, Graham and Johnson 1977), and Arora (1998) gave a [polynomial-time approximation scheme](/ptas/). The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), which uses no extra points, is at most about 21 percent longer; the conjectured worst case of $2/\sqrt{3}$, the [Steiner ratio](/steiner-ratio/), is still open.

## In plain words

You must connect some towns with roads, and you want the least total road length. You may build crossroads anywhere, not only at the towns.

Without crossroads, the best you can do is to join towns directly, town to town. With crossroads you can do better. For three towns in a triangle, one crossroad in the middle can serve all three, and the roads leave it at equal angles of a third of a full turn.

In the best network every crossroad has exactly three roads at equal angles. Finding the best network for many towns is very hard, because there are too many ways to choose which roads meet where. Fast methods find a network that is only a little longer than the best.

## Definition

Notation: $T = \{t_1, \ldots, t_n\} \subset \mathbb{R}^2$ is the set of terminals, $|uv|$ the Euclidean length of a segment, and the length of a tree is the sum of the lengths of its edges. A Steiner tree for $T$ is a tree in the plane, drawn with straight edges, whose vertex set contains $T$; its other vertices are Steiner points. $\mathrm{SMT}(T)$ is the smallest length of a Steiner tree, and $\mathrm{MST}(T)$ is the length of the minimum spanning tree on $T$.

**Input.** The terminals $T$.

**Output.** A Steiner tree of length $\mathrm{SMT}(T)$, given by its Steiner points and its edges.

**Structure of a Steiner minimal tree** (Gilbert and Pollak 1968).

1. Two edges at a common vertex meet at an angle of at least 120 degrees.
2. Every Steiner point has degree exactly 3, and its three edges meet at 120 degrees. Every terminal has degree at most 3.
3. There are at most $n - 2$ Steiner points, and they lie in the convex hull of $T$.
4. The tree splits at the terminals of degree 2 or 3 into full components. In a full Steiner tree every terminal is a leaf, and there are exactly $k - 2$ Steiner points for $k$ terminals.

*Proof sketch.* If two edges at a vertex $v$ meet at less than 120 degrees, the [Fermat point](/fermat-point/) of $v$ and two points near $v$ on these edges is a new junction that shortens the tree, so (1) holds. A Steiner point of degree 1 or 2 can be removed or straightened, and degree 4 or more forces two edges within 90 degrees; with (1) this gives (2). Counting edges with (2) gives (3): a tree with $n$ terminals and $s$ Steiner points has $n + s - 1$ edges, and the degree sum is at least $3s + n$, so $s \le n - 2$. $\square$

The topology of a Steiner tree is its graph without the positions. Each full topology for $k$ terminals is an unrooted binary tree with $k$ labeled leaves, and there are $(2k - 5)!! = 1 \cdot 3 \cdot 5 \cdots (2k - 5)$ of them. For a fixed full topology the length is a convex function of the Steiner point positions, so every local minimum is a global one, and Melzak's construction finds it exactly. The difficulty is the number of topologies.

Degeneracies: the 120 degree rule can force Steiner points to coincide with terminals, which then means that the full topology is not realizable and a different topology is optimal. Collinear terminals have $\mathrm{SMT} = \mathrm{MST}$. Model: real RAM; the lengths involve square roots, so the decision version ("is there a tree of length at most $L$?") is not known to be in NP.

## Variants

- **Rectilinear.** Lengths in the $L_1$ metric with horizontal and vertical edges: the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/), which has a grid of candidate Steiner points by Hanan's theorem.
- **Graph Steiner tree.** Terminals are vertices of a weighted graph and Steiner points are other vertices: the [Steiner tree problem](/steiner-tree-problem/) in graphs.
- **Higher dimensions.** The same angle conditions hold in $\mathbb{R}^d$; Smith (1992) gave an exact branch and bound method for $\mathbb{R}^d$.
- **Other metrics.** $\lambda$-geometry Steiner trees allow $\lambda$ uniformly spaced edge directions; the rectilinear case is $\lambda = 2$.
- **With obstacles.** The tree must avoid polygonal obstacles, and the edges bend at obstacle corners as in [shortest paths](/euclidean-shortest-path/).
- **Bottleneck and bounded Steiner points.** Minimize the longest edge, or use at most $k$ Steiner points.

## Examples

**An equilateral triangle** with side 1. The Steiner point is the center, the three edges have length $1/\sqrt{3}$, and $\mathrm{SMT} = \sqrt{3} \approx 1.7321$, while $\mathrm{MST} = 2$. The ratio $\sqrt{3}/2 \approx 0.8660$ is the conjectured worst case.

**A triangle with an angle of at least 120 degrees.** For $(0, 0), (4, 0), (-1, 1)$ the angle at $(0, 0)$ is 135 degrees. No Steiner point helps: the tree is the two edges at that corner, of length $4 + \sqrt{2}$, as for the [Fermat point](/fermat-point/).

**The unit square** $(0, 0), (1, 0), (1, 1), (0, 1)$. The minimal tree has two Steiner points, $(\sqrt{3}/6, 1/2)$ and $(1 - \sqrt{3}/6, 1/2)$. The first joins $(0, 0)$ and $(0, 1)$, the second joins $(1, 0)$ and $(1, 1)$, and an edge joins the two. Each of the four outer edges has length $1/\sqrt{3}$, and the middle edge has length $1 - \sqrt{3}/3$, so $\mathrm{SMT} = 4/\sqrt{3} + 1 - \sqrt{3}/3 = 1 + \sqrt{3} \approx 2.7321$. At each Steiner point the edges point in directions 120 degrees apart, for example $120°$, $240°$ and $0°$ at the first. The topology that pairs $(0, 0)$ with $(1, 0)$ gives the same length by symmetry, and $\mathrm{MST} = 3$.

**Points on a line.** For collinear terminals the path through them in order is optimal, and no Steiner point is used.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| Melzak (1961): all topologies, each by equilateral-triangle constructions | exact | exponential |
| fixed full topology (Hwang 1986) | exact for that topology | $O(k)$ for $k$ terminals |
| GeoSteiner (Warme, Winter and Zachariasen): generate the full Steiner trees that pass pruning tests, then join them by integer programming | exact | exponential in the worst case; thousands of terminals in practice |
| [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) | factor $1/\rho$, where $\rho \ge 0.824$ is the Steiner ratio | $O(n \log n)$ |
| Arora (1998), randomized; also Mitchell (1999) by guillotine subdivisions | factor $1 + \varepsilon$ | $n (\log n)^{O(1/\varepsilon)}$ in the plane for Arora's scheme |
| greedy insertion of Steiner points into the MST, and other heuristics | no worst-case bound beyond the MST | $O(n \log n)$ to $O(n^2)$ |

**Melzak's construction for a full topology.** Pick two terminals $a, b$ that are joined to the same Steiner point $s$. Replace them by the apex $c$ of the equilateral triangle on $ab$, on the side away from $s$. Solve the smaller problem, in which $c$ is joined to some vertex $s'$. Then $s$ is the point where the segment $cs'$ meets the arc $ab$ of the circle through $a$, $b$ and $c$, and $|as| + |bs| = |cs|$, so the two trees have the same length. This is the same 60 degree rotation that proves the [Fermat point](/fermat-point/) formula.

## Bounds

- **NP-hard.** Garey, Graham and Johnson (1977) show that the Euclidean Steiner tree problem is NP-hard. Because of the square roots, its decision version is not known to be in NP. The rectilinear version is NP-complete (Garey and Johnson 1977).
- **Steiner ratio.** Let $\rho = \inf_T \mathrm{SMT}(T)/\mathrm{MST}(T)$. Gilbert and Pollak (1968) conjectured $\rho = \sqrt{3}/2$, the value for an equilateral triangle. Du and Hwang announced a proof in 1990, but a gap in it was later identified, and the conjecture is regarded as open. It is proved for $n \le 6$ terminals, and the best general lower bound is $\rho \ge 0.824$ (Chung and Graham 1985). See [Steiner ratio](/steiner-ratio/).
- **Approximation.** Arora's scheme shows that the plane problem is not hard to approximate: for every fixed $\varepsilon > 0$ there is a polynomial-time $(1 + \varepsilon)$-approximation. This contrasts with the graph version, which is [APX-hard](/steiner-tree-inapproximability/).
- **Number of topologies.** Already the full topologies number $(2n - 5)!!$, which grows faster than $2^n$, so plain enumeration works only for small $n$.

## Reductions

- **From the Fermat point.** For $n = 3$ the problem is exactly the [Fermat point](/fermat-point/) problem: the sum of distances from one junction is the length of the star.
- **To full components.** A Steiner minimal tree is a union of full Steiner trees joined at terminals, so an exact method can generate candidate full trees and choose a minimum spanning union of them, a minimum spanning tree problem in a hypergraph.
- **To the graph problem.** Restricting Steiner points to a fine grid gives a graph Steiner instance whose answer converges to $\mathrm{SMT}$; in the rectilinear case the Hanan grid makes this exact.

## Applications

- **Network design.** Leased telephone lines, pipelines, roads and power grids, where the cost grows with the length and junctions can be placed freely.
- **Chip design.** Wiring nets in VLSI uses the rectilinear version, and Steiner tree length estimates the wire length in placement.
- **Phylogenetics.** Trees of minimum total change among sequences or feature vectors are Steiner trees in other metrics.
- **Soap films.** The 120 degree junctions are the junctions that soap films form between pins held by two plates, which gives a physical analogue computer for small instances.

## References
