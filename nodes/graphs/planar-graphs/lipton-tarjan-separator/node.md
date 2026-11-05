---
tag: YCV3MB
kind: algorithm
slug: lipton-tarjan-separator
name: Lipton-Tarjan separator algorithm
aliases:
- Lipton-Tarjan separator
area: graphs/planar-graphs
level: advanced
summary: Finds a planar separator in linear time using a BFS tree and fundamental cycles.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [planar-separator-theorem, breadth-first-search, planar-face-finding, fundamental-cycle]
see_also: [planar-separator-finding, r-division, nested-dissection, planar-dual-graph, maximal-planar-graph, lowest-common-ancestor, rotation-system, divide-and-conquer-paradigm]
sources:
  - paper: doi:10.1137/0136016
    title: Richard J. Lipton and Robert Endre Tarjan, A separator theorem for planar graphs, SIAM Journal on Applied Mathematics 36(2), 177 to 189 (1979)
    locator: the lemmas on breadth-first levels and on fundamental cycles, the main theorem, and the linear-time algorithm with its steps
  - paper: doi:10.1137/0209046
    title: Richard J. Lipton and Robert Endre Tarjan, Applications of a planar separator theorem, SIAM Journal on Computing 9(3), 615 to 627 (1980)
    locator: the use of the algorithm in divide-and-conquer algorithms
  - paper: doi:10.1016/0022-0000(86)90030-9
    title: Gary L. Miller, Finding small simple cycle separators for 2-connected planar graphs, Journal of Computer and System Sciences 32(3), 265 to 279 (1986)
    locator: the simple cycle separator variant
---

The Lipton-Tarjan algorithm computes a [planar separator](/planar-separator-finding/): for a planar graph with $n$ vertices, a set $S$ of at most $2\sqrt{2}\sqrt{n}$ vertices whose removal leaves two sides $A$ and $B$, each with at most $2n/3$ vertices and with no edge between them. It runs a [breadth-first search](/breadth-first-search/), cuts the graph at two thin levels, and, if the band between them is still too big, cuts the band with one short [fundamental cycle](/fundamental-cycle/) of a triangulation. The embedding is given as a [rotation system](/rotation-system/), and the whole run takes $\Theta(n)$ time. It is the algorithmic form of the [planar separator theorem](/planar-separator-theorem/).

## In plain words

Pick a start node and sort the nodes into rings by distance from it. Find the ring that holds the middle node in this order. If that ring is small, remove it: the inner rings and the outer rings each hold at most half of the nodes.

If the middle ring is too big, remove a thin ring a little further in and a thin ring a little further out. They cut the graph into an inner part, a band and an outer part. If the band is still too big, squeeze the inner rings into one point, so that every node of the band is close to it. Fill all regions with triangles and pick one closed loop made of two short paths to the point and one extra edge, so that each side of the loop keeps at most two thirds of the band. Remove its nodes too.

## The problem

**Input.** A [simple](/simple-graph/) planar graph $G = (V, E)$ with $n$ vertices and a planar rotation system $\rho$: for each vertex $v$, the list $\rho_v$ of its neighbours in counterclockwise order. A graph given by adjacency lists only gets $\rho$ from a [planar embedding](/planar-embedding/) algorithm in $O(n)$ time.

**Output.** A partition of $V$ into $A$, $B$ and $S$ with no edge between $A$ and $B$, $|A|, |B| \le 2n/3$ and $|S| \le 2\sqrt{2}\sqrt{n}$.

## The algorithm

Write $\lvert L \rvert$ for the number of vertices in a set $L$. The levels of the search are $L_0, \ldots, L_r$, and $L_i = \emptyset$ for $i < 0$ and $i > r$.

```pseudo id=main
LT-SEPARATOR(G, ρ)                          ▷ ρ: a planar rotation system
L1  K ← a largest component of G; if |K| ≤ 2n/3 then S ← ∅, go to L13
L2  run BFS in K from a vertex q: levels L_0, …, L_r, parents p(v)
    ℓ1 ← the least level with |L_0| + … + |L_ℓ1| ≥ |K|/2; k ← |L_0| + … + |L_ℓ1|
L3  if |L_ℓ1| ≤ 2√2·√|K| then S ← L_ℓ1, go to L13
L4  ℓ0 ← the largest ℓ ≤ ℓ1 with |L_ℓ| + 2(ℓ1 − ℓ) ≤ 2√k
L5  ℓ2 ← the least ℓ > ℓ1 with |L_ℓ| + 2(ℓ − ℓ1 − 1) ≤ 2√(|K| − k)
L6  S ← L_ℓ0 ∪ L_ℓ2; M ← L_(ℓ0+1) ∪ … ∪ L_(ℓ2−1); if |M| ≤ 2|K|/3 go to L13
L7  H ← the graph on M plus the levels ≤ ℓ0 contracted into one root x, with ρ
L8  in each face of H, add a new vertex joined to every corner of the face
L9  T ← the BFS tree on H, each new vertex hung from one corner; w ← 1 on M, 0 else
L10 T* ← the duals of the non-tree edges, a tree rooted at a face; subtree sums
L11 e ← a non-tree edge with w(inside C_e) + w(C_e) ≥ w(M)/3 and fewest faces inside
L12 S ← S ∪ (V(C_e) ∩ M)
L13 group the components of G − S into A and B, each with at most 2n/3 vertices
L14 return (A, B, S)
```

**Line L7, contraction.** The levels $0, \ldots, \ell_0$ are connected through the search tree, so contracting them keeps the graph planar. The rotation at $x$ is read off an Euler tour of the search tree inside the contracted part: at each vertex, scan $\rho_v$ counterclockwise from the edge to the parent, descend into each tree child, and output each edge that leaves the part. Parallel edges to $x$ are dropped, keeping the first. If $\ell_0 = -1$, nothing is contracted and the root is $q$.

**Line L8, triangulation.** A new vertex $c_f$ in face $f$, joined to the corner of $f$ after each dart $d$ of the walk of $f$, cuts $f$ into triangles $c_f, u, v$ with three distinct vertices. In the rotation at $u$, the new edge goes right after the dart $d = (u, v)$, because the face of $d$ is on its left, the counterclockwise side at $u$. The result may have parallel edges at $c_f$ when the walk of $f$ passes a vertex twice, but every face is a triangle, which is all the cycle step needs.

**Line L11, weights from subtree sums.** Root $T^*$ at a face $f_0$. A non-tree edge $e$ has a dart $d = (u, v)$ whose left face $g$ is the child of $e^*$; the faces in the subtree of $g$ are exactly the faces inside the cycle $C_e$. Give each vertex $v$ an *owner face*, the face on the left of the dart from $v$ to its parent in $T$ (for the root, the face of its first dart), and let $\Sigma(g)$ be the sum of the weights whose owner face is in the subtree of $g$. With $z$ the [lowest common ancestor](/lowest-common-ancestor/) of $u$ and $v$ and $P(v)$ the weight of the tree path from $v$ up to the root,

$$w(C_e) = P(u) + P(v) - 2P(z) + w(z), \qquad w(\text{inside } C_e) = \Sigma(g) - \big(P(v) - P(z)\big) - [\text{owner}(z) \text{ inside}] \cdot w(z).$$

The subtracted terms are the cycle vertices whose owner face is inside: walking $C_e$ along $d$ and then up from $v$, the inside is on the left, so the owners of the branch from $v$ are inside and those of the branch from $u$ are outside.

## Example

The fan with 11 vertices: a hub 0 and the path $1, 2, \ldots, 10$, all joined to the hub. Draw the path on a horizontal line above the hub. Then

$$\rho_0 = (10, 9, \ldots, 1), \quad \rho_i = (i + 1, i - 1, 0) \text{ for } 2 \le i \le 9, \quad \rho_1 = (2, 0), \quad \rho_{10} = (9, 0).$$

| line | step | value |
|---|---|---|
| L1 | the graph is connected | $\lvert K \rvert = 11 > 22/3$ |
| L2 | BFS from $q = 0$ | $L_0 = \{0\}$, $L_1 = \{1, \ldots, 10\}$, $r = 1$ |
| L2 | median level | $\ell_1 = 1$, $k = 11$ |
| L3 | is $L_1$ small? | $10^2 = 100 > 8 \cdot 11 = 88$: no |
| L4 | $\ell = 1$: $10 + 0 > 2\sqrt{11}$; $\ell = 0$: $1 + 2 \le 2\sqrt{11}$ | $\ell_0 = 0$ |
| L5 | $\ell = 2$: $0 + 0 \le 2\sqrt{0}$ | $\ell_2 = 2$ |
| L6 | $S = L_0 \cup L_2 = \{0\}$, $M = L_1$ | $\lvert M \rvert = 10 > 22/3$: continue |
| L7 | contract $L_0$ into $x$ | $H$ is again a fan: $x$ joined to the path |
| L8 | $H$ has 11 vertices, 19 edges, 10 faces | 10 new vertices; 38 triangles |
| L9 | $T$: the 10 spokes from $x$, and each new vertex hung from its first corner | $w = 1$ on $1, \ldots, 10$ |
| L11 | the cycle $x, 3, c, 10$, where $c$ is the new vertex in the outer face of $H$ | 2 vertices inside ($1, 2$), 2 on the cycle ($3, 10$) |
| L12 | add the vertices of $G$ on the cycle | $S = \{0, 3, 10\}$ |
| L13 | components of $G - S$ | $\{1, 2\}$ and $\{4, \ldots, 9\}$ |
| L14 | group them | $A = \{4, \ldots, 9\}$, $B = \{1, 2\}$, $S = \{0, 3, 10\}$ |

The candidate at line L11 has weight $2 + 2 = 4 \ge 10/3$ on and inside the cycle, and weight $2 \le 20/3$ strictly inside. The result has $\lvert A \rvert = 6 \le 22/3$, $\lvert B \rvert = 2$ and $\lvert S \rvert = 3 \le 2\sqrt{2}\sqrt{11} \approx 9.4$. The cycle uses the new vertex $c$ of the outer face: the non-tree edge from 3 to $c$ closes it, and $c$ is not a vertex of $G$, so it does not go into $S$.

**Small cases.** A single vertex gives $S = \{v\}$ at line L3, since $1 \le 2\sqrt{2}$. A tree, $K_4$ and every graph with $n \le 8$ stop at line L3, because then $|L_{\ell_1}| \le n \le 2\sqrt{2}\sqrt{n}$. $K_5$ and $K_{3,3}$ have no planar rotation system, so they are not valid inputs; the implementation checks Euler's formula $n - m + f = 2c$ on $\rho$ and rejects them.

## Correctness

Each part of $G - S$ has at most $2n/3$ vertices. If line L1 stops, every component has at most $2n/3$ vertices. If line L3 stops, the levels below $\ell_1$ hold fewer than $|K|/2$ vertices and those above hold at most $|K|/2$, and no edge skips a level. If line L6 stops, the same holds for the levels below $\ell_0$ and above $\ell_2$, and $M$ is small. Otherwise the lemma of the [planar separator theorem](/planar-separator-theorem/) applies to the triangulation of $H$ with the tree $T$ and the weights $w$: the candidate with the fewest faces inside has at most $2/3$ of the weight of $M$ strictly inside its cycle and at most $2/3$ strictly outside, and the Jordan curve theorem forbids edges between the two. The size of $S$ is bounded by the claim in that proof: $|S| \le 2\sqrt{k} + 2\sqrt{|K| - k} \le 2\sqrt{2}\sqrt{n}$. Line L13 groups the parts as in the last step of the proof. The full proof, including the formula of line L11 and the triangulation of line L8, is in the correctness proof below.

## Complexity

- **Lines L1 to L6** are one component search, one breadth-first search and scans of the level sizes: $O(n)$, since $m \le 3n - 6$.
- **Line L7** visits each dart of the contracted part a constant number of times, and line L8 adds one new vertex per face and one edge per dart of $H$: $O(n)$.
- **Lines L9 and L10** are a tree traversal of $T$, face tracing on the triangulation, and a traversal of $T^*$ with subtree sums. The triangulation has fewer than $3n$ vertices and $O(n)$ edges and faces, so this is $O(n)$.
- **Line L11** needs one lowest common ancestor per non-tree edge. With a constant-time query after linear preprocessing, it is $O(n)$. The implementation below uses [binary lifting](/binary-lifting/), which costs $O(n \log n)$; Lipton and Tarjan avoid ancestor queries by moving one cycle step by step and charging each step to the vertices it passes.
- **Lines L12 to L14** walk the cycle and find the components of $G - S$: $O(n)$.
- **Space.** $\Theta(n)$ for the levels, the triangulation and the dual tree.

## Properties

- **Deterministic.** The result depends only on $\rho$, the vertex order and the choice of $q$.
- **No recursion.** Every search is iterative, so large inputs do not exhaust the call stack.
- **The separator has a shape.** $S$ is at most two search levels and the vertices of one cycle. On many inputs line L3 already stops, and $S$ is one level.
- **Not optimal.** The guarantee is on $|S|$ in terms of $n$, not on the least separator. On the $3 \times 3$ grid from its center, the algorithm returns the 4 middle-side vertices, while 2 vertices suffice.
- **Weights.** The same steps, with weights in place of counts at lines L2 to L6, give the weighted separator theorem.

## Variants and improvements

- **Cycle separators.** Miller's algorithm finds a separator that is one simple cycle of $O(\sqrt{dn})$ vertices in a 2-connected plane graph with faces of at most $d$ vertices. Cycle separators keep the boundary of each piece on a few faces, which [r-divisions](/r-division/) and planar shortest path algorithms need.
- **Recursive use.** Applying the algorithm to the pieces gives a separator tree in $O(n \log n)$ time, or in $O(n)$ time with more care; see [finding planar separators](/planar-separator-finding/).
- **Balance $1/2$.** Separate the larger side again until both sides have at most $n/2$ vertices.
- **Smaller constants.** Better choices of the levels and of the cycle lower the constant $2\sqrt{2}$; see the [planar separator theorem](/planar-separator-theorem/).

## When to use it

Use it as the first step of [divide and conquer](/divide-and-conquer-paradigm/) on planar graphs: for [nested dissection](/nested-dissection/) of sparse linear systems, for [r-divisions](/r-division/) and fast [planar shortest paths](/planar-shortest-paths/), and for [tree decompositions](/tree-decomposition/) of width $O(\sqrt{n})$. When only good separators are needed in practice, not the guarantee, simpler heuristics such as one search level or multilevel partitioners are often used, with this algorithm as a fallback.

## Pitfalls

- **Contracting without the rotation.** Contracting the inner levels by merging adjacency lists loses the cyclic order at $x$, and the triangulation then is not planar. The Euler tour of line L7 keeps it.
- **Triangulating with chords.** Adding chords from one corner of a face can create parallel edges or edges that already exist outside the face. The new vertex per face in line L8 avoids both.
- **Counting the new vertices.** The new vertices and $x$ have weight 0 and are not vertices of $G$. They may lie on the cycle; drop them at line L12.
- **Inside and outside.** "Inside" means the side of $C_e$ without the root face of $T^*$. The root vertex $q$ may lie strictly inside some cycles; the owner test for the lowest common ancestor handles it.
- **Square roots in floating point.** Compare $c \le 2\sqrt{k}$ as $c^2 \le 4k$ in integers, to avoid rounding at the boundary.
- **Disconnected input.** Run the main part on a component with more than $2n/3$ vertices, and group all other components at line L13.

## Implementations

## History

Lipton and Tarjan proved the planar separator theorem and gave this linear-time algorithm in the paper published in 1979, and showed its use for divide and conquer, nested dissection and approximation in 1980. Miller (1986) gave the simple cycle separator, and later work on recursive decompositions builds on both.

## References
