---
tag: GT7NZ8
kind: algorithm
slug: kasteleyn-method
name: Kasteleyn's method
aliases:
- FKT algorithm
- Fisher-Kasteleyn-Temperley method
- Kasteleyn's Pfaffian method
area: combinatorics/counting-algorithms
level: research
summary: Counts perfect matchings of planar graphs in polynomial time via a Pfaffian.
solves: [counting-perfect-matchings]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1961
  people: [Pieter W. Kasteleyn, H. N. V. Temperley, Michael E. Fisher]
  note: Kasteleyn, and independently Temperley and Fisher, counted the domino tilings of a rectangle in 1961. Kasteleyn proved in 1963 that every planar graph has an orientation for which the Pfaffian counts the perfect matchings.
prereqs: [perfect-matching, planar-graph, planar-dual-graph, determinant-computation]
see_also: [counting-perfect-matchings, domino-tiling-problem, permanent-computation, tutte-matrix, bareiss-algorithm, planar-face-finding, euler-formula, ryser-formula]
sources:
  - paper: doi:10.1016/0031-8914(61)90063-5
    title: P. W. Kasteleyn, The statistics of dimers on a lattice I. The number of dimer arrangements on a quadratic lattice, Physica 27(12), 1209 to 1225, 1961
    locator: the whole paper (the Pfaffian for the square lattice and the product formula)
  - paper: doi:10.1080/14786436108243366
    title: H. N. V. Temperley and Michael E. Fisher, Dimer problem in statistical mechanics, an exact result, Philosophical Magazine 6(68), 1061 to 1063, 1961
    locator: the whole note (the same count for the square lattice)
  - paper: doi:10.1063/1.1703953
    title: P. W. Kasteleyn, Dimer statistics and phase transitions, Journal of Mathematical Physics 4(2), 287 to 293, 1963
    locator: the section on planar graphs (every planar graph has a Pfaffian orientation)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing, 2009
    locator: Chapter 8 (determinants, Pfaffians and Pfaffian orientations of planar graphs)
  - paper: doi:10.1016/0890-5401(89)90017-5
    title: Vijay V. Vazirani, NC algorithms for computing the number of perfect matchings in K3,3-free graphs and related problems, Information and Computation 80(2), 152 to 164, 1989
    locator: the introduction and the section on planar graphs (the orientation in NC)
---

Kasteleyn's method counts the [perfect matchings](/perfect-matching/) of a [planar graph](/planar-graph/) $G$ with $n$ vertices in polynomial time. It orients the edges of $G$ so that every bounded face has an odd number of edges oriented clockwise along its boundary. Such an orientation is called a Pfaffian orientation. Let $K$ be the skew-symmetric matrix with $K_{uv} = 1$ and $K_{vu} = -1$ for each oriented edge $u \to v$, and 0 elsewhere. Then every perfect matching contributes the same sign to the Pfaffian of $K$, so

$$\#\text{perfect matchings of } G = |\operatorname{Pf}(K)| = \sqrt{\det K}.$$

The orientation takes $O(n \log n)$ time from a plane drawing, and the [determinant](/determinant-computation/) takes $O(n^3)$ arithmetic operations. For general graphs the same count is #P-complete, so planarity is what makes the problem easy. The method counts the domino tilings of a region, the dimer coverings of a planar lattice, and the matchings of any planar graph.

## In plain words

A perfect matching pairs up all the points of a network, using only the links of the network. Counting perfect matchings is very hard for most networks. For networks drawn on paper with no crossing links, there is a fast way.

Give each link a direction. Choose the directions so that, around each small region of the drawing, an odd number of links point clockwise. Then write the directions into a table of numbers and compute one standard quantity of the table, which a computer does quickly. In general this quantity adds up the matchings with mixed plus and minus signs, so it does not count them. With directions chosen this way, all matchings get the same sign, and the quantity becomes the square of the number of matchings.

## The problem

Input: a planar graph $G = (V, E)$ with $n$ vertices, given with a plane drawing (here, integer coordinates for the vertices, with straight edges that do not cross). Output: the number of perfect matchings of $G$, that is, the number of sets of $n/2$ edges that cover each vertex once. This is the problem [counting perfect matchings](/counting-perfect-matchings/), restricted to planar graphs. A disconnected graph is handled one component at a time, and the counts multiply.

## The algorithm

Let $G$ be connected. Trace the faces with each face on the left of its boundary walk, so the bounded faces are traced counterclockwise. An edge $u \to v$ is clockwise on a face $f$ if the walk of $f$ uses it as $v \to u$.

```pseudo id=main
KASTELEYN(G)                        ▷ G connected, drawn in the plane, n vertices
L1  if n is odd then return 0
L2  T ← a spanning tree of G; orient each edge of T arbitrarily
L3  trace the faces of G; f_out ← the outer face
L4  D ← the tree on the faces with one edge for each edge of G not in T,
        joining the two faces on its sides; root D at f_out
L5  for each face f ≠ f_out, children before parents in D do
L6      e ← the edge of G that joins f to its parent in D
L7      orient e so that the number of clockwise edges on f is odd
L8  K[u][v] ← 1 and K[v][u] ← −1 for each oriented edge u → v; other entries 0
L9  return √det(K)
```

The graph $D$ in line L4 is a tree: the edges not in a spanning tree of a plane graph are dual to a spanning tree of the [dual graph](/planar-dual-graph/). When line L7 handles $f$, all edges of $f$ except $e$ are already oriented: tree edges in line L2, and the edges to the children of $f$ in earlier passes. In the implementation, line L3 sorts the neighbours of each vertex by angle and follows each dart to the next edge clockwise, as in [planar face finding](/planar-face-finding/). The outer face is the face whose boundary walk has negative signed area.

## Example

Take the $2 \times 3$ grid: vertices 0, 1, 2 at $(0,0), (1,0), (2,0)$ and 3, 4, 5 at $(0,1), (1,1), (2,1)$, with the edges of the grid. It has 3 perfect matchings. Line L2 uses the depth-first tree from vertex 0, which is the path 0, 1, 2, 5, 4, 3, and points each tree edge from the smaller to the larger label.

| step | action | state after the step |
|---|---|---|
| L1 | $n = 6$ is even | continue |
| L2 | tree $0 - 1 - 2 - 5 - 4 - 3$ | $0 \to 1$, $1 \to 2$, $2 \to 5$, $4 \to 5$, $3 \to 4$ |
| L3 | trace the faces | $A = (0, 1, 4, 3)$, $B = (1, 2, 5, 4)$, outer face $O$ |
| L4 | non-tree edges $0 - 3$ (between $A$ and $O$) and $1 - 4$ (between $A$ and $B$) | $D$ is the path $O - A - B$, root $O$ |
| L5 to L7, face $B$ | walk $1 \to 2 \to 5 \to 4 \to 1$; only $4 \to 5$ is clockwise, so 1 so far | orient $4 \to 1$ (with the walk); $B$ has 1 clockwise edge |
| L5 to L7, face $A$ | walk $0 \to 1 \to 4 \to 3 \to 0$; $4 \to 1$ and $3 \to 4$ are clockwise, so 2 so far | orient $0 \to 3$ (against the walk); $A$ has 3 clockwise edges |
| L8 | build $K$ from the 7 oriented edges | $6 \times 6$ skew-symmetric matrix |
| L9 | $\det K = 9$ | return 3 |

The three matchings $\{01, 25, 34\}$, $\{03, 12, 45\}$ and $\{03, 14, 25\}$ each contribute $+1$ to $\operatorname{Pf}(K)$, so $\operatorname{Pf}(K) = 3$ and $\det K = 9$.

## Correctness

The full proof is in `proofs/correctness.md`. It has four steps.

- **The Pfaffian.** For a skew-symmetric matrix $K$ of even order, $\operatorname{Pf}(K)$ is a signed sum with one term for each perfect matching of the complete graph on the indices, and $\operatorname{Pf}(K)^2 = \det K$. Only perfect matchings of $G$ give nonzero terms, and each such term is $\pm 1$.
- **Two matchings.** If $M$ and $M'$ are perfect matchings, their union is a set of shared edges and disjoint even cycles. The terms of $M$ and $M'$ have the same sign if and only if each of these cycles has an odd number of clockwise edges.
- **Cycles in a planar graph.** If every bounded face has an odd number of clockwise edges, then a cycle $C$ has an odd number of clockwise edges if and only if it encloses an even number of vertices. This follows from [Euler's formula](/euler-formula/) applied to $C$ and everything inside it. A cycle of $M \cup M'$ encloses an even number of vertices, because $M$ matches them among themselves.
- **The orientation.** Lines L5 to L7 make each bounded face odd, and later passes do not touch the edges of a face already handled.

So all terms of $\operatorname{Pf}(K)$ are equal, $|\operatorname{Pf}(K)|$ is the number of perfect matchings, and line L9 returns it.

## Complexity

- **Time.** A planar graph has at most $3n - 6$ edges. Sorting the neighbours by angle takes $O(n \log n)$ time; the tree, the faces, the dual tree and the loop of lines L5 to L7 take $O(n)$ time, since each face walk is read once. Line L9 dominates: Gaussian elimination on the $n \times n$ matrix takes $O(n^3)$ arithmetic operations.
- **Bit cost.** Each row of $K$ has $\deg(v)$ entries $\pm 1$, so by Hadamard's bound every minor of $K$ has absolute value at most $\prod_v \sqrt{\deg(v)} \le 6^{n/2}$. With the fraction-free [Bareiss algorithm](/bareiss-algorithm/), all intermediate numbers are minors and have $O(n)$ bits.
- **Space.** The matrix takes $\Theta(n^2)$ words.

## Properties

- **Exact.** The algorithm returns the exact count, using only integer arithmetic.
- **Deterministic.** The orientation depends on the spanning tree, but every Pfaffian orientation gives the same $|\operatorname{Pf}(K)|$.
- **Weighted version.** With $K_{uv} = w(uv)$ and $K_{vu} = -w(uv)$ for edge weights $w$, $\operatorname{Pf}(K)$ is $\pm$ the sum over perfect matchings of the product of the weights.
- **The outer face.** Each edge is clockwise on exactly one of its two sides, so the clockwise counts of all faces add up to the number of edges. With Euler's formula, this shows that if $n$ is even and every bounded face is odd, the outer face is odd too. So the root of $D$ can be any face.
- **Parallel.** The orientation and the determinant can both be computed in NC, so counting perfect matchings of planar graphs is in NC.

## Variants and improvements

- **Lattices and tilings.** For the $m \times n$ grid, a fixed orientation (horizontal edges one way, vertical edges alternating by column) is Pfaffian, and the eigenvalues of $K$ give a closed product formula for the number of [domino tilings](/domino-tiling-problem/). The $8 \times 8$ board has 12988816 tilings.
- **Bipartite planar graphs.** If $G$ is bipartite, $K$ is a block matrix built from a signed biadjacency matrix $B$, and the count is $|\det B|$, a determinant of order $n/2$.
- **Separators.** Elimination orders based on planar separators (nested dissection) reduce the number of arithmetic operations below $n^3$.
- **$K_{3,3}$-free graphs.** Little showed that graphs with no $K_{3,3}$ minor have Pfaffian orientations, and Vazirani computed them in NC. Straub, Thierauf and Wagner gave a polynomial algorithm for graphs with no $K_5$ minor, which combines Pfaffians with a decomposition.
- **Bounded genus.** On a surface of genus $g$, the count is a signed sum of $4^g$ Pfaffians, so it is polynomial for fixed $g$.

## When to use it

Use Kasteleyn's method to count perfect matchings, dimer coverings or domino tilings of a planar graph exactly, for graphs with thousands of vertices. For general graphs, exact counting is #P-complete: use [Ryser's formula](/ryser-formula/) on the biadjacency matrix of a small bipartite graph, or an approximation scheme for large bipartite graphs. If only the parity is needed, the determinant modulo 2 of the adjacency matrix gives it for any graph, since the permanent and the determinant agree modulo 2.

## Pitfalls

- **The parity.** Line L7 must make the number of clockwise edges odd. If all edges of the example are simply pointed from the smaller to the larger label, both faces have 2 clockwise edges, the terms of the Pfaffian are $+1, +1, -1$, $\det K = 1$, and line L9 returns 1 instead of 3.
- **The order of the loop.** Line L5 must handle children before parents. In the opposite order, the edge to a child face is still unoriented when the parent is handled, and the parity of line L7 is not defined.
- **Disconnected graphs.** Lines L2 to L4 assume that $G$ is connected. For a disconnected graph there is no spanning tree, and $D$ is not a tree. Run the algorithm on each component, and return 0 if one component has an odd number of vertices.
- **The square root.** Line L9 returns the square root of $\det K$, not $\det K$ itself. The symmetric adjacency matrix, without the orientation, does not give the count.
- **The drawing.** Lines L3 and L4 need a true plane drawing. If two edges cross, the traced faces are wrong, and $\det K$ can be a non-square or a wrong square.

## Implementations

## History

The dimer problem asks for the number of ways to cover a lattice with dimers, which are molecules that fill two adjacent sites. In 1961 Kasteleyn, and independently Temperley and Fisher, solved it for the square lattice by writing the count as a Pfaffian and finding its eigenvalues. In 1963 Kasteleyn proved that every planar graph has an orientation for which the Pfaffian counts the perfect matchings, which gives a polynomial algorithm for planar graphs. Valiant's 1979 proof that counting perfect matchings is #P-complete showed that the general problem is hard. Little extended the method to $K_{3,3}$-free graphs in 1974, Vazirani made it parallel in 1989, and later work extended it to graphs of bounded genus and to $K_5$-free graphs.

## References
