---
tag: CEQJDF
kind: definition
slug: facet
name: Facet
aliases:
- facet of a polytope
- face of a polytope
- ridge
area: geometry/convex-hulls
level: intro
summary: A face of a d-dimensional polytope of dimension d-1.
prereqs: [supporting-hyperplane, convex-hull]
see_also: [convex-polytope, convex-hull-3d, extreme-point, euler-formula, beneath-beyond, minkowski-weyl-theorem, vertex-enumeration, general-position]
sources:
  - book: isbn:9780387943657
    title: Gunter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer, 1995
    locator: Lecture 0 (cyclic polytopes and Gale's evenness condition), Lecture 2 (faces, facets and ridges of polytopes) and Lecture 8 (the Upper Bound Theorem)
  - paper: doi:10.1112/S0025579300002850
    title: Peter McMullen, The maximum numbers of faces of a convex polytope, Mathematika 17(2), 1970
    locator: the whole paper (proof of the Upper Bound Theorem)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 4, Convex Hulls in Three Dimensions (polyhedra, Euler's formula and the counts of edges and faces)
---

A facet of a $d$-dimensional convex polytope is a face of dimension $d - 1$: an edge of a convex polygon, a polygonal face of a 3D polyhedron, and in general the intersection of the polytope with a [supporting hyperplane](/supporting-hyperplane/) that has full dimension inside that hyperplane. The facets give the smallest description of a polytope by inequalities, one inequality per facet, so a $d$-dimensional hull algorithm reports its output as a list of facets. The number of facets can be much larger than the number of points: by the Upper Bound Theorem, $n$ points in $\mathbb{R}^d$ can have $\Theta(n^{\lfloor d/2 \rfloor})$ facets, and no more.

## Definition

Notation: $P$ is a finite set of $n$ points in $\mathbb{R}^d$, and $Q = \operatorname{conv} P$ is its [convex hull](/convex-hull/), a [convex polytope](/convex-polytope/). Assume $Q$ is full-dimensional, that is, $\dim Q = d$. The orientation of $d + 1$ points is the sign of the $d$ by $d$ determinant with rows $p_1 - p_0, \ldots, p_d - p_0$ (see [orientation test](/orientation-test/)).

A **face** of $Q$ is $Q$ itself, the empty set, or a set $F = Q \cap H$ where $H$ is a supporting hyperplane of $Q$. The **dimension** of a face is the dimension of its [affine hull](/affine-hull/). Faces of dimension $0$ are the **vertices** (the [extreme points](/extreme-point/) of $Q$), faces of dimension $1$ are the **edges**, faces of dimension $d - 2$ are the **ridges**, and faces of dimension $d - 1$ are the **facets**. The number of faces of dimension $k$ is written $f_k$, and $(f_0, \ldots, f_{d-1})$ is the **f-vector** of $Q$.

Facts about faces (Ziegler, Lecture 2):

- Each face of $Q$ is the convex hull of the vertices of $Q$ that it contains, so a polytope has finitely many faces.
- A face of a face of $Q$ is a face of $Q$.
- Each ridge lies in exactly two facets.
- $Q$ is the intersection of the closed half-spaces bounded by its facet hyperplanes that contain $Q$. Each such half-space is needed, so this is the smallest description of $Q$ by linear inequalities, and the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) is the general form of the step from points to inequalities.

A polytope is **simplicial** if each facet is a $(d-1)$-simplex, that is, has exactly $d$ vertices. If $P$ is in [general position](/general-position/) (no $d + 1$ points on a hyperplane), then $\operatorname{conv} P$ is simplicial.

**Facet test.** Let $S \subseteq P$ be $d$ affinely independent points, and let $H$ be the hyperplane through them. Then $Q \cap H$ is a facet if and only if the orientations of $(S, r)$ for $r \in P$ are all $\ge 0$ or all $\le 0$. Each facet arises from some such $S$.

*Proof.* If the signs agree, all of $P$, and hence all of $Q$, lies in one closed half-space of $H$, and $H$ meets $Q$, so $H$ is a supporting hyperplane. Since $Q$ is full-dimensional, $Q \not\subseteq H$, and $Q \cap H$ contains the $d$ affinely independent points of $S$, so it has dimension $d - 1$. Conversely, a facet $F$ has dimension $d - 1$ and is the hull of the points of $P$ that it contains, so it contains $d$ affinely independent points of $P$, and its supporting hyperplane leaves all of $P$ on one side. $\square$

Testing every $d$-subset against every point gives the brute-force hull in $O(n^{d+1})$ time with exact integer determinants. Subsets that give the same hyperplane give the same facet, so a facet that contains more than $d$ points of $P$ is found once for each affinely independent $d$-subset of those points, and the results must be grouped by hyperplane.

**Counts in three dimensions.** For a 3-polytope, the vertices and edges form a connected planar graph whose faces are the facets, so [Euler's formula](/euler-formula/) gives

$$f_0 - f_1 + f_2 = 2.$$

Each facet has at least 3 edges and each edge is in exactly 2 facets, so $2 f_1 \ge 3 f_2$. With Euler's formula this gives $f_1 \le 3 f_0 - 6$ and $f_2 \le 2 f_0 - 4$, with equality if and only if the polytope is simplicial. So the output of a 3D hull algorithm has size $O(n)$.

**The Upper Bound Theorem** (McMullen, 1970). Let $Q$ be a $d$-polytope with $n$ vertices. Then $f_k(Q) \le f_k(C_d(n))$ for each $k$, where $C_d(n)$ is the **cyclic polytope**, the convex hull of $n$ distinct points $(t, t^2, \ldots, t^d)$ on the moment curve. Its number of facets is

$$f_{d-1}(C_d(n)) = \binom{n - \lceil d/2 \rceil}{\lfloor d/2 \rfloor} + \binom{n - \lfloor d/2 \rfloor - 1}{\lceil d/2 \rceil - 1}.$$

The proof is long and is not given here; see McMullen's paper or Ziegler, Lecture 8. The count of facets of $C_d(n)$ follows from **Gale's evenness condition**: for $t_1 < \cdots < t_n$, a $d$-subset $S$ of the indices is a facet if and only if between any two indices not in $S$ there is an even number of indices in $S$. Special cases:

| $d$ | maximum number of facets | at $n = 10$ |
|---|---|---|
| 2 | $n$ | 10 |
| 3 | $2n - 4$ | 16 |
| 4 | $n(n-3)/2$ | 35 |
| 5 | $(n-3)(n-4)$ | 42 |
| 6 | $n(n-4)(n-5)/6$ | 50 |

So the maximum is $\Theta(n^{\lfloor d/2 \rfloor})$ for fixed $d$. This is the output size that an optimal $d$-dimensional hull algorithm must allow for in the worst case, and it is the term $n^{\lfloor d/2 \rfloor}$ in the bounds of the [beneath-beyond method](/beneath-beyond/) and the randomized algorithms of [3D and higher-dimensional hulls](/convex-hull-3d/).

## Examples and non-examples

- **Octahedron.** For the six points $(\pm 1, 0, 0)$, $(0, \pm 1, 0)$, $(0, 0, \pm 1)$ the facet test finds 8 triangles. The octahedron is simplicial, with $f_0 = 6$, $f_1 = 12 = 3 \cdot 6 - 6$ and $f_2 = 8 = 2 \cdot 6 - 4$.
- **Cube.** For the eight points $\{0, 1\}^3$, 24 triples pass the facet test, and they lie on 6 planes with 4 points each. So the cube has 6 square facets, and each is found $\binom{4}{3} = 4$ times. The cube is not simplicial: $f_0 = 8$, $f_1 = 12 < 3 \cdot 8 - 6$ and $f_2 = 6 < 2 \cdot 8 - 4$.
- **Square pyramid with an inner point.** For $(0,0,0)$, $(2,0,0)$, $(2,2,0)$, $(0,2,0)$, $(1,1,2)$ and $(1,1,1)$ there are 5 facets: the square base and 4 triangles, each through the apex $(1,1,2)$. The point $(1,1,1)$ is on no facet. Here $f_0 = 5$, $f_1 = 8$, $f_2 = 5$ and $5 - 8 + 5 = 2$.
- **Cyclic polytopes.** For the points $(t, t^2, t^3)$ with $t = 1, \ldots, 8$ the facet test finds $12 = 2 \cdot 8 - 4$ facets. For $(t, t^2, t^3, t^4)$ with $t = 1, \ldots, 8$ it finds $20 = 8 \cdot 5 / 2$ facets. For $d = 2, \ldots, 6$ and $n = d + 1, \ldots, d + 5$, the count by Gale's evenness condition equals the formula above, and for $d = 3, 4$ and $n = 5, \ldots, 8$ the brute-force facet test with exact determinants gives the same counts. With $n = 100$ points in $\mathbb{R}^4$ the cyclic polytope has $4850$ facets.
- **Non-example: an edge.** An edge of the cube is a face of dimension $1$, so it is not a facet in $\mathbb{R}^3$. It is a ridge, and it lies in exactly two square facets.
- **Non-example: a plane through vertices.** The plane $x = y$ contains four vertices of the cube, but $(1, 0, 0)$ and $(0, 1, 0)$ lie on opposite sides of it. It is not supporting, and its section of the cube is not a face.

## Related definitions

- [Convex polytope](/convex-polytope/) and [convex hull](/convex-hull/): the objects whose faces these are.
- [Supporting hyperplane](/supporting-hyperplane/) and [extreme point](/extreme-point/): faces are cut out by supporting hyperplanes, and the vertices are the extreme points.
- [Minkowski-Weyl theorem](/minkowski-weyl-theorem/): a polytope is a bounded intersection of half-spaces, and the facet half-spaces are the smallest such set.
- [Vertex enumeration](/vertex-enumeration/): the inverse problem, from facets to vertices.
- [3D convex hull](/convex-hull-3d/) and [beneath-beyond method](/beneath-beyond/): algorithms whose output is the list of facets.
- [General position](/general-position/): it makes every facet a simplex.
- [Euler's formula](/euler-formula/): the relation between the counts $f_0$, $f_1$ and $f_2$ in three dimensions.

## References
