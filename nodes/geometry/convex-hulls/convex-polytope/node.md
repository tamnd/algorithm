---
tag: FW9MYJ
kind: definition
slug: convex-polytope
name: Convex polytope
aliases:
- polytope
- convex polyhedron
- V-polytope
- H-polytope
area: geometry/convex-hulls
level: core
summary: The convex hull of a finite point set in R^d, equivalently a bounded intersection of half-spaces.
prereqs: [convex-hull, affine-hull, supporting-hyperplane]
see_also: [minkowski-weyl-theorem, facet, convex-hull-3d, euler-formula, polyhedron, vertex-enumeration, conic-hull, beneath-beyond]
sources:
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Springer, 1995
    locator: Chapter 0 (basic examples and f-vectors), Chapter 1 (the main theorem, V- and H-polytopes), Chapter 2 (faces) and Chapter 8 (f-vectors, cyclic polytopes, Gale's evenness condition and the Upper Bound Theorem)
  - book: isbn:9780387004242
    title: Branko Grünbaum, Convex Polytopes, 2nd edition, Springer, 2003
    locator: Chapter 3 (faces and polytopes), Chapter 4 (cyclic and neighborly polytopes), Chapter 8 (Euler's relation) and Chapter 10 (the upper bound theorem)
  - paper: doi:10.1112/S0025579300002850
    title: Peter McMullen, The maximum numbers of faces of a convex polytope, Mathematika 17(2), 1970
    locator: the proof of the Upper Bound Theorem
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Chapter 5, Convex polytopes (H- and V-polytopes, faces, cyclic polytopes and the asymptotic upper bound theorem)
---

A convex polytope is the [convex hull](/convex-hull/) of finitely many points in $\mathbb{R}^d$. By the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) it is also a bounded intersection of finitely many closed half-spaces. In the plane polytopes are convex polygons, in space they are the solids such as the cube and the octahedron. Every hull algorithm turns one description into the other: the input is a list of points (the V-description), and the output lists the facets (the H-description) or the corners. The size of that output is governed by the Upper Bound Theorem: $n$ points in $\mathbb{R}^d$ can have $\Theta(n^{\lfloor d/2 \rfloor})$ facets, and the exact maximum is known.

## Definition

A *V-polytope* is $P = \mathrm{conv}(V)$ for a finite set $V \subseteq \mathbb{R}^d$. An *H-polytope* is a bounded set $P = \{ x \in \mathbb{R}^d : Ax \le b \}$ for a matrix $A \in \mathbb{R}^{m \times d}$ and $b \in \mathbb{R}^m$, that is, a bounded [polyhedron](/polyhedron/). The [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) says that the two classes are the same, so one says *polytope* for both. The *dimension* of $P$ is the dimension of its [affine hull](/affine-hull/), and a $d$-polytope is a polytope of dimension $d$.

**Faces.** A linear inequality $c \cdot x \le c_0$ is *valid* for $P$ if every point of $P$ satisfies it. A *face* of $P$ is a set $F = P \cap \{ x : c \cdot x = c_0 \}$ for a valid inequality. With $c = 0$, $c_0 = 0$ the face is $P$ itself, and with $c = 0$, $c_0 = 1$ it is $\emptyset$. Every face is itself a polytope. Faces of dimension $0$, $1$, $d - 2$ and $d - 1$ are the *vertices*, *edges*, *ridges* and [facets](/facet/). The vertices of $\mathrm{conv}(V)$ are exactly the [extreme points](/extreme-point/), and they are a subset of $V$. A face of a face is a face, and the faces ordered by inclusion form a lattice, the *face lattice*.

**Two descriptions, one polytope.** For a $d$-polytope in $\mathbb{R}^d$, the vertex set is the unique smallest V-description, and the facet inequalities, one per facet, form the unique smallest H-description (up to positive scaling of each inequality). Converting the vertex list to the facet list is the convex hull problem; the opposite direction is [vertex enumeration](/vertex-enumeration/). By polarity the two problems are the same problem.

**The f-vector.** For a $d$-polytope $P$, $f_k(P)$ is the number of $k$-dimensional faces, and $(f_0, f_1, \ldots, f_{d-1})$ is the *f-vector*. It satisfies the Euler-Poincaré relation

$$\sum_{k=0}^{d-1} (-1)^k f_k(P) = 1 - (-1)^d,$$

which for $d = 3$ is [Euler's formula](/euler-formula/) $f_0 - f_1 + f_2 = 2$.

**Simple and simplicial.** $P$ is *simplicial* if every facet is a simplex ($d$ vertices per facet), and *simple* if every vertex lies on exactly $d$ facets. Points in general position give a simplicial hull, and polarity swaps the two classes.

**Three dimensions.** For a 3-polytope with $n$ vertices, $e$ edges and $f$ facets: each facet has at least 3 edges and each edge is on 2 facets, so $2e \ge 3f$. Euler's formula $n - e + f = 2$ then gives

$$f \le 2n - 4 \qquad\text{and}\qquad e \le 3n - 6,$$

with equality exactly for simplicial polytopes. So the hull of $n$ points in space has linear size, and a 3D hull algorithm can afford to output all of it.

**The Upper Bound Theorem.** The *moment curve* is $\gamma(t) = (t, t^2, \ldots, t^d)$, and the *cyclic polytope* $C(n, d)$ is the convex hull of $n$ distinct points on it, $n \ge d + 1$. Its combinatorial type does not depend on the choice of points. Its facets are given by *Gale's evenness condition*: if the points are $\gamma(t_1), \ldots, \gamma(t_n)$ with $t_1 < \cdots < t_n$, a $d$-subset $T$ of indices spans a facet if and only if between any two indices not in $T$ there is an even number of indices of $T$. It follows that $C(n, d)$ is simplicial and *neighborly*: every set of at most $\lfloor d/2 \rfloor$ vertices spans a face.

**Theorem (Upper Bound Theorem, McMullen 1970).** Let $P$ be a $d$-polytope with $n$ vertices. Then $f_k(P) \le f_k(C(n, d))$ for every $k = 0, \ldots, d - 1$. For facets, with $m = \lfloor d/2 \rfloor$,

$$f_{d-1}(C(n, d)) = \begin{cases} \dfrac{n}{n - m} \dbinom{n - m}{m} & d = 2m \text{ even}, \\[2ex] 2 \dbinom{n - m - 1}{m} & d = 2m + 1 \text{ odd}. \end{cases}$$

So a $d$-polytope with $n$ vertices has $O(n^{\lfloor d/2 \rfloor})$ facets, and the cyclic polytope shows that this order is reached. By polarity, a $d$-polytope with $n$ facets has at most $f_{d-1}(C(n, d))$ vertices, which bounds the number of vertices of a feasible region $\{x : Ax \le b\}$ with $n$ constraints. The proof uses the $h$-vector, a shelling of the boundary and the Dehn-Sommerville equations; see Ziegler, Chapter 8.

## Examples and non-examples

- **The $d$-simplex**, the hull of $d + 1$ affinely independent points, has $f_k = \binom{d+1}{k+1}$. The tetrahedron has $f = (4, 6, 4)$, and $4 - 6 + 4 = 2$.
- **The $d$-cube** $[0, 1]^d$ has $f_k = 2^{d-k} \binom{d}{k}$. It is simple but not simplicial for $d \ge 3$. The 3-cube has $f = (8, 12, 6)$, and $8 - 12 + 6 = 2$. Its 6 facets are below the bound $2 \cdot 8 - 4 = 12$, because its facets are squares.
- **The $d$-cross-polytope** $\{x : \sum_i |x_i| \le 1\}$ has $f_k = 2^{k+1} \binom{d}{k+1}$. It is the polar of the cube, it is simplicial, and the octahedron has $f = (6, 12, 8)$, with $8 = 2 \cdot 6 - 4$ facets, so it meets the 3D bound.
- **Cyclic polytopes, counted by brute force.** The table gives the number of facets of $\mathrm{conv}\{\gamma(1), \ldots, \gamma(n)\}$, computed by checking every $d$-subset of points with an exact integer determinant (a $d$-subset is a facet when all other points are strictly on one side of its hyperplane). It agrees with the formula above in every entry, and the facet sets agree with Gale's evenness condition for $(n, d) = (6, 3), (7, 4), (8, 5), (9, 6)$.

| $d$ | $n = d+1$ | $n = d+2$ | $n = d+3$ | $n = d+4$ | $n = d+5$ | formula |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | 4 | 5 | 6 | 7 | $n$ |
| 3 | 4 | 6 | 8 | 10 | 12 | $2n - 4$ |
| 4 | 5 | 9 | 14 | 20 | 27 | $n(n-3)/2$ |
| 5 | 6 | 12 | 20 | 30 | 42 | $(n-3)(n-4)$ |
| 6 | 7 | 16 | 30 | 50 | 77 | $n(n-4)(n-5)/6$ |

In $\mathbb{R}^4$, 9 points on the moment curve have 27 facets, and every pair of the 9 vertices is an edge, which is neighborliness for $m = 2$.

- **Not a polytope: a disk or a ball.** It is convex and compact but has infinitely many extreme points, so it is not the hull of a finite set.
- **Not a polytope: an unbounded polyhedron**, such as the quadrant $\{x \ge 0, y \ge 0\}$. It is an intersection of finitely many half-planes, but not bounded. The Minkowski-Weyl theorem writes it as a polytope plus a [conic hull](/conic-hull/).
- **Not convex: a non-convex polyhedron** such as an L-shaped solid built from cubes. The word *polyhedron* in solid modeling often means any solid with flat faces; in this sub-area *polytope* always means a convex one.

## Related definitions

- A [facet](/facet/) is a face of dimension $d - 1$; a [supporting hyperplane](/supporting-hyperplane/) cuts out each face.
- The [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) proves that V-polytopes and H-polytopes are the same.
- A [polyhedron](/polyhedron/) is an intersection of finitely many half-spaces, bounded or not; the polytopes are the bounded ones. The feasible region of a [linear program](/linear-programming-problem/) is a polyhedron, and the [simplex method](/simplex-method/) walks along its edges.
- The [3D convex hull problem](/convex-hull-3d/) computes the facets of a polytope from its points, and [beneath-beyond](/beneath-beyond/) is one of its algorithms.
- [Euler's formula](/euler-formula/) for planar graphs applies to the graph of a 3-polytope, which is planar and 3-connected by Steinitz's theorem.

## References
