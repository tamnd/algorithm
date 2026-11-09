---
tag: FK22GB
kind: problem
slug: planar-point-location
name: Planar point location in O(log n)
aliases:
- Point location in O(log n)
- planar point location
- point location problem
- point location in a planar subdivision
area: geometry/point-location
level: core
summary: Problem of finding which region of a planar subdivision contains a query point, solved in logarithmic time with a sweep and persistent or ordered structures.
prereqs: [planar-subdivision, orientation-test, binary-search]
see_also: [vertical-ray-shooting, slab-method-point-location, sarnak-tarjan-point-location, kirkpatrick-point-location, seidel-point-location, chazelle-monotone-point-location, triangle-walk-point-location, post-office-problem]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Point Location (Section 6.1 the slab method, Sections 6.2 to 6.4 the trapezoidal map, its randomized construction, degenerate cases and the tail estimate), and the notes and comments of Chapter 6
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2 (point location, the slab method, the chain method, Kirkpatrick's method and the lower bound), to be checked
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink (planar methods, lower bounds, expected-case and dynamic variants)
  - paper: doi:10.1137/0205015
    title: David Dobkin and Richard J. Lipton, Multidimensional searching problems, SIAM Journal on Computing 5(2), 1976
    locator: the slab method (DOI to be checked)
  - paper: doi:10.1137/0206043
    title: D. T. Lee and Franco P. Preparata, Location of a point in a planar subdivision and its applications, SIAM Journal on Computing 6(3), 1977
    locator: the chain method (DOI to be checked)
  - paper: doi:10.1137/0212002
    title: David Kirkpatrick, Optimal search in planar subdivisions, SIAM Journal on Computing 12(1), 1983
    locator: the hierarchy of triangulations (DOI to be checked)
  - paper: doi:10.1137/0215023
    title: Herbert Edelsbrunner, Leonidas J. Guibas and Jorge Stolfi, Optimal point location in a monotone subdivision, SIAM Journal on Computing 15(2), 1986
    locator: the chain tree with fractional cascading (DOI to be checked)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: the persistent slab method (DOI to be checked)
  - paper: doi:10.1016/0925-7721(91)90012-4
    title: Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry 1(1), 1991
    locator: the randomized trapezoidal map and its search structure (DOI to be checked)
  - paper: doi:10.1137/07068669X
    title: Timothy M. Chan and Mihai Pătraşcu, Transdichotomous results in computational geometry, I, Point location in sublogarithmic time, SIAM Journal on Computing 39(2), 2009
    locator: the word RAM bounds for integer coordinates (DOI to be checked)
---

Planar point location asks for a data structure that stores a [planar subdivision](/planar-subdivision/) with $n$ edges and, for a query point $q$, reports the vertex, edge or face that contains $q$. A single query takes $\Theta(n)$ time by a scan of the edges. With preprocessing, several methods answer each query in $O(\log n)$ time with $O(n)$ space. In the algebraic decision tree model with ternary branching, $\lceil \log_3 N \rceil$ tests are needed for a subdivision with $N$ vertices, edges and faces, so $O(\log n)$ is optimal.

## In plain words

You have a map with many countries and borders, and many people ask "which country am I in?". You may study the map once, as long as you like, and build an index. After that, each question must be answered fast.

Looking at every border for each question is slow when the map is large. The good methods cut the map into simple pieces, such as strips or triangles, and arrange those pieces so that each question cuts the remaining candidates about in half. Then a map with a million borders needs only a few dozen small tests for each question. No method can do much better, because each test has only a few possible results, and the question has as many possible answers as the map has pieces.

## Definition

**Notation.** $P$ is the set of vertices of the subdivision, $n$ the number of edges, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. The output size of a query is $h = 1$. The predicate $\mathrm{incircle}$ is not used. Costs are on the [real RAM](/real-ram/): each arithmetic operation and each comparison of reals takes unit time, and memory cells hold reals or pointers.

**Input.** A planar straight-line graph with vertex set $P$ and $n$ segments that meet only at common end points (a [planar subdivision](/planar-subdivision/)), usually given as a [doubly connected edge list](/doubly-connected-edge-list/). By Euler's formula, there are $O(n)$ vertices and faces when there are no isolated vertices.

**Query.** A point $q \in \mathbb{R}^2$. The answer is the vertex $q$ if $q \in P$; otherwise the edge whose relative interior contains $q$, if one exists; otherwise the face that contains $q$.

**Costs.** A solution is measured by three numbers: the preprocessing time $T(n)$ to build the structure, the space $S(n)$ it uses, and the query time $Q(n)$. Each is a worst-case bound unless marked expected (for randomized structures, over the random choices only, for every input and every fixed query point) or amortized.

**Degenerate input.** Vertical edges, several vertices on one vertical line, and query points on edges, at vertices or on a vertical line through a vertex are all allowed. The implementations on these pages use the symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ of de Berg et al., Section 6.3: points are compared in lexicographic order, which removes all equal $x$-coordinates and all vertical edges, and above or below a segment is decided by an exact $\mathrm{orient}$ test on integer coordinates. No floating-point tolerance is used.

## Variants

- **Vertical ray shooting.** Report the edges directly above and below $q$. This is the form most structures compute; the face follows from the DCEL as the face below the edge above $q$ (or the face above the edge below, or the unbounded face if both rays escape). See [vertical ray shooting](/vertical-ray-shooting/).
- **Special subdivisions.** For a single [convex polygon](/convex-polygon-point-location/), a binary search on the vertices answers in $O(\log n)$ with no extra space. For a [monotone subdivision](/monotone-subdivision/), the chain method applies. For a triangulation, Kirkpatrick's hierarchy and walking apply.
- **One-shot queries.** One point and one polygon: [point in polygon](/point-in-polygon/) by ray crossing in $\Theta(n)$ time, with no preprocessing.
- **Dynamic point location.** Edges are inserted and deleted between queries. The known structures trade query time against update time within small powers of $\log n$; the Handbook, Chapter 38, surveys them.
- **Distribution-sensitive point location.** Queries come from a known distribution, and the goal is expected query time close to the entropy of the face probabilities, as for optimal binary search trees.
- **Higher dimensions.** Point location in subdivisions of $\mathbb{R}^d$ for $d \ge 3$, for example in [Delaunay tetrahedralizations](/higher-dimensional-delaunay/), where walking is the method used in practice.
- **Integer coordinates on the word RAM.** With coordinates that are $w$-bit integers and a word RAM, the $\Omega(\log n)$ bound of the algebraic model does not apply, and Chan and Pătraşcu give $O(\log n / \log \log n)$ query time with linear space.

## Examples

**A small subdivision.** Take the segments $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$. They form a triangle with vertices $(0,0), (8,2), (4,6)$ (face 1) and a free segment $s_3$; everything else is the unbounded face 0. These answers come from the [slab method](/slab-method-point-location/) and agree with a linear scan:

| query $q$ | edge above | edge below | answer |
|---|---|---|---|
| $(5, 3)$ | $s_1$ | $s_0$ | face 1, the inside of the triangle |
| $(4, 7)$ | $s_3$ | $s_1$ | face 0 |
| $(1, 5)$ | none | $s_2$ | face 0 |
| $(9, 4)$ | $s_3$ | none | face 0 |
| $(6, 7)$ | | | edge $s_3$ |
| $(8, 2)$ | | | vertex $(8, 2)$ |

For $(5, 3)$: $\mathrm{orient}((4,6), (8,2), (5,3)) = (8-4)(3-6) - (2-6)(5-4) = -8 < 0$, so $q$ is below $s_1$, and $\mathrm{orient}((0,0), (8,2), (5,3)) = 8 \cdot 3 - 2 \cdot 5 = 14 > 0$, so $q$ is above $s_0$. The face below $s_1$ is the face of its half-edge from $(8,2)$ to $(4,6)$, which is face 1. The point $(4, 7)$ has the same $x$ as the vertex $(4, 6)$; under the shear it lies to the right of $(4,6)$, so it falls in the slab between $(4,6)$ and $(8,2)$, where $s_1$ is the segment below it.

**The lower bound for a fan.** A convex polygon with $m$ vertices, triangulated by the diagonals from one vertex, has $m$ vertices, $2m - 3$ edges, $m - 2$ triangles and the unbounded face: $N = 4m - 4$ possible answers. For $m = 8$, $N = 28$, and every ternary decision tree that answers point location for it has depth at least $\lceil \log_3 28 \rceil = 4$; the $F = 7$ faces alone force depth at least $\lceil \log_2 7 \rceil = 3$ (see Bounds).

## Known algorithms

The table gives preprocessing time, space and query time for a subdivision with $n$ edges. W means worst case and E means expected over the random choices of the algorithm, for every input and every fixed query point.

| method | preprocessing | space | query |
|---|---|---|---|
| linear scan of the edges | none | $O(n)$ W | $O(n)$ W |
| [slab method](/slab-method-point-location/) (Dobkin and Lipton 1976) | $O(n^2)$ W | $\Theta(n^2)$ W | $O(\log n)$ W |
| [chain method](/chazelle-monotone-point-location/) (Lee and Preparata 1977) | $O(n \log n)$ W | $O(n)$ W | $O(\log^2 n)$ W |
| chain method with [fractional cascading](/multiple-list-search/) (Edelsbrunner, Guibas and Stolfi 1986) | $O(n \log n)$ W, $O(n)$ for a regular monotone subdivision | $O(n)$ W | $O(\log n)$ W |
| [Kirkpatrick's hierarchy](/kirkpatrick-point-location/) (1983) | $O(n \log n)$ W, $O(n)$ for a triangulation | $O(n)$ W | $O(\log n)$ W |
| [persistent slabs](/sarnak-tarjan-point-location/) (Sarnak and Tarjan 1986) | $O(n \log n)$ W | $O(n)$ W | $O(\log n)$ W |
| [trapezoidal map](/seidel-point-location/) by randomized incremental construction (Mulmuley 1990, Seidel 1991) | $O(n \log n)$ E | $O(n)$ E | $O(\log n)$ E, and $O(\log n)$ W after rebuilding while the DAG is deep |
| [triangle walk](/triangle-walk-point-location/) in a triangulation | none | $O(n)$ W | $O(n)$ W |
| [convex polygon](/convex-polygon-point-location/), one face | none | $O(n)$ W | $O(\log n)$ W |

The $O(n \log n)$ preprocessing of the chain method and of Kirkpatrick's method includes making the subdivision monotone or triangulating it, which takes $O(n \log n)$ by a plane sweep. The first method with $O(\log n)$ query and $O(n)$ space was by Lipton and Tarjan (1980), from the [planar separator theorem](/planar-separator-theorem/); it is of theoretical interest only. The trapezoidal map structure is also the [data structure page](/trapezoidal-map/) that the randomized method builds.

## Bounds

**Theorem (query lower bound).** Fix a subdivision with $N$ pieces (vertices, edges and faces), $F$ of them faces. Let $\mathcal{T}$ be an [algebraic decision tree](/algebraic-decision-tree/) that answers point location for it: each inner node tests the sign of a nonzero polynomial $f(q_x, q_y)$ of degree at most a fixed $k$ whose coefficients may depend on the subdivision, it has three children for $f < 0$, $f = 0$ and $f > 0$, and each leaf outputs one piece. If $\mathcal{T}$ is correct for every $q \in \mathbb{R}^2$, its depth $t$ satisfies $t \ge \lceil \log_3 N \rceil$ and $t \ge \lceil \log_2 F \rceil$.

*Proof.* Every piece $\sigma$ is the answer for the points of $\sigma$, so some leaf outputs $\sigma$, and different pieces need different leaves. A ternary tree of depth $t$ has at most $3^t$ leaves, so $3^t \ge N$. For the second bound, the set of points that reach a node by a path with at least one $f = 0$ branch lies in the zero set of a nonzero polynomial, which has area zero, and there are finitely many such sets. A face is open and nonempty, so it has positive area, and some point of it reaches a leaf along a path of strict branches only. Those leaves are at most $2^t$, so $2^t \ge F$. $\blacksquare$

The bound needs no restriction on the preprocessing or on the space. A triangulated convex polygon with $m$ vertices has $F = m - 1$, so every algebraic decision tree for it has depth at least $\log_2(m - 1)$, and $Q(n) = \Omega(\log n)$ for all of the methods above. The query algorithms above are decision trees of degree $1$ (for a fixed edge, the $\mathrm{orient}$ test is a polynomial of degree $1$ in $q$, and so is the comparison of $q$ with a vertex), so the theorem applies to them. The same counting holds in the algebraic computation tree model, where the query may also compute with the coordinates of $q$, since its branch nodes are also ternary.

**Constant factors.** The depth of the best tree is $\log_2 n + O(\sqrt{\log n})$ in the model of above or below tests against lines: Seidel and Adamy (2000) found the second-order term and a matching lower bound (exact form to be checked against their paper). The constant factors of the practical methods differ: the proof for the trapezoidal map gives at most $12 H_n \approx 12 \ln n$ expected tests, and fewer are observed; Kirkpatrick's method has a large constant from the degree bound and the fraction of removed vertices.

**Preprocessing and space.** $\Omega(n)$ space is needed to store the subdivision. When the subdivision is given as an unordered list of segments, building its DCEL takes $\Omega(n \log n)$ time in the [algebraic computation tree](/algebraic-computation-tree/) model: for the star of segments from $(0,0)$ to $(x_i, 1)$, the $\mathrm{next}$ pointers give the angular order of the end points, which is the sorted order of the $x_i$, and sorting has that lower bound. For a triangulation given as a DCEL, Kirkpatrick's method builds in $O(n)$.

## Reductions

**Point location to vertical ray shooting.** Given the edge $e$ directly above $q$, the face of $q$ is the face below $e$, which the DCEL stores on one half-edge of $e$. If no edge is above $q$, use the edge below, or report the unbounded face. So every vertical ray shooting structure answers point location with $O(1)$ extra time. The converse also holds for the methods based on trapezoids or slabs, which return both edges.

**Nearest neighbor to point location.** The [post office problem](/post-office-problem/) asks for the nearest of $n$ sites to a query point. The nearest site is the site of the [Voronoi cell](/voronoi-diagram/) that contains $q$, so a point location structure on the Voronoi diagram, of size $O(n)$, answers each query in $O(\log n)$. Other locus problems reduce in the same way, for example to point location in an arrangement of lines.

**Sorted search to point location.** Searching a sorted list $y_1 < \cdots < y_n$ is point location in a ladder: the $n$ horizontal segments $[0, 1] \times \{y_i\}$ and the vertical segments that join $(0, y_i)$ to $(0, y_{i+1})$ and $(1, y_i)$ to $(1, y_{i+1})$. A query $(1/2, y)$ falls in the rectangle between the two list entries around $y$, on a rung, or in the unbounded face. So point location is at least as hard as [searching a sorted list](/sorted-search-lower-bound/).

## Applications

- Geographic information systems: find the region, parcel or zone of a coordinate.
- Locus approaches to proximity: nearest neighbor through the Voronoi diagram, and the $k$ nearest neighbors through higher order Voronoi diagrams.
- Mesh codes: find the element of a finite element mesh that contains a point, usually by a walk from a nearby element.
- Computer graphics and user interfaces: find the shape under the mouse pointer in a planar scene.
- Robot motion planning: locate the start and the goal in a free-space decomposition.
- Overlay and Boolean operations of maps, which need to find the face of one map that contains a vertex of the other.

## References
