---
tag: YE7M4T
kind: problem
slug: vertex-enumeration
name: Vertex enumeration
aliases:
- enumerating polytope vertices
- vertex enumeration problem
- listing the vertices of a polyhedron
area: optimization/linear-programming
level: advanced
summary: List all vertices of a polyhedron given by linear inequalities.
prereqs: [basic-feasible-solution, polyhedron]
see_also: [convex-hull-problem, reverse-search, minkowski-weyl-theorem, fundamental-theorem-of-lp, fourier-motzkin-elimination, lp-degeneracy, nash-equilibrium, convex-polytope]
sources:
  - paper: doi:10.1007/BF02293050
    title: David Avis and Komei Fukuda, A pivoting algorithm for convex hulls and vertex enumeration of arrangements and polyhedra, Discrete and Computational Geometry 8, 295 to 313 (1992)
    locator: the reverse search method and its time and space bounds for nondegenerate inputs
  - paper: doi:10.1007/s00454-008-9050-5
    title: Leonid Khachiyan, Endre Boros, Konrad Borys, Khaled Elbassioni and Vladimir Gurvich, Generating all vertices of a polyhedron is hard, Discrete and Computational Geometry 39, 174 to 190 (2008)
    locator: the main theorem (NP-hardness of deciding whether a given list of vertices of an unbounded polyhedron is complete)
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer, 1995
    locator: Chapter 1 (the main theorem for polytopes, from inequalities to vertices) and Chapter 8 (the upper bound theorem)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.3, Polyhedra in standard form (a basic solution for each choice of basic columns), and Section 2.6, Optimality of extreme points
---

Vertex enumeration is the problem of listing all vertices of a [polyhedron](/polyhedron/) given by linear inequalities $Ax \le b$. By the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/), listing the vertices solves every linear program over the polyhedron, and by the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), the vertices (with the extreme rays) describe the polyhedron in the other way, as a convex hull. The output can be exponentially large, so algorithms are judged by their time per vertex. For bounded, nondegenerate inputs that cost is polynomial, but for unbounded polyhedra the problem is provably hard, and for general polytopes its complexity is open.

## In plain words

A region cut out by flat walls has corners. The task is to list every corner, given only the walls. A corner is a point where enough walls meet to pin it down, so one way is to try every group of walls, find where they meet, and keep the points that are inside the region. That works but is slow. Better methods walk from corner to corner along the edges, like the simplex method, and visit each corner once. A region with a few walls can still have a very large number of corners, so no method can be fast in every case; the best ones are fast for each corner they output.

## Definition

**Input.** $A \in \mathbb{Q}^{m \times n}$ with rows $a_1^\top, \ldots, a_m^\top$, and $b \in \mathbb{Q}^m$. Let $P = \{x \in \mathbb{R}^n : Ax \le b\}$.

**Output.** The set $V$ of vertices of $P$, each listed once. A point $v \in P$ is a vertex when the rows tight at $v$ have rank $n$; see [basic feasible solution](/basic-feasible-solution/) for the equal forms of this definition.

**Size.** Let $v = |V|$. Since the output has $v$ points, an algorithm is *output-polynomial* if it runs in time polynomial in $m$, $n$, the bit length $L$ and $v$, and *polynomial-delay* if the time between two outputs is polynomial in $m$, $n$ and $L$.

**Standard form.** For $P = \{x : Ax = b,\ x \ge 0\}$ with $A$ of rank $m$, the vertices are the [basic feasible solutions](/basic-feasible-solution/), each the basic solution $x_B = A_B^{-1} b$ of some basis $B$.

## Variants

- **Polytopes and polyhedra.** If $P$ is unbounded, a full description also needs the extreme rays of its recession cone. The two cases have very different complexity.
- **Facet enumeration.** Given points, list the facets of their convex hull. This is the [convex hull problem](/convex-hull-problem/); for a polytope with the origin in its interior, polarity turns one problem into the other.
- **Basis enumeration.** List all feasible bases, not all vertices. At a degenerate vertex many bases give the same point, so this list can be much longer than $V$.
- **Counting.** Count the vertices without listing them. This is #P-hard (Dyer, 1983; Linial, 1986).
- **Adjacency.** List also the edges of $P$, the graph on which the [simplex method](/simplex-method/) walks.

## Examples

**The running pentagon.** $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $-x_1 \le 0$, $-x_2 \le 0$ has $m = 5$ and $n = 2$. Of the $\binom{5}{2} = 10$ pairs of rows, one pair ($x_1 \le 3$ and $-x_1 \le 0$) is parallel, four meet outside $P$, and five give the vertices $(0, 0)$, $(3, 0)$, $(3, 1)$, $(3/2, 5/2)$ and $(0, 3)$.

**The cube.** $0 \le x_j \le 1$ for $j = 1, 2, 3$ gives $m = 6$ rows and 8 vertices. Of the $\binom{6}{3} = 20$ triples of rows, the 8 that take one row from each parallel pair give the vertices, and the other 12 are singular.

**A degenerate vertex.** The square pyramid $z \ge 0$, $\pm x + z \le 1$, $\pm y + z \le 1$ has 5 rows and 5 vertices: the corners $(\pm 1, \pm 1, 0)$ and the apex $(0, 0, 1)$. Of the 10 triples, 2 are singular, 4 give the 4 corners, and the other 4 all give the apex, which lies on 4 facets. A brute-force method must remove the repeats.

**Many vertices from few rows.** The cube $[0, 1]^n$ has $2n$ rows and $2^n$ vertices. The polar of a cyclic polytope has $m$ facets and $\Theta(m^{\lfloor n/2 \rfloor})$ vertices for fixed $n$, the most possible by the upper bound theorem of McMullen.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| Brute force over $n$-subsets of rows | $O\big(\binom{m}{n} (n^3 + mn)\big)$ | exact with rationals; simple; the reference oracle for tests |
| Brute force over bases (standard form) | $O\big(\binom{n}{m} (m^3 + mn)\big)$ | lists each basic feasible solution |
| Double description (Motzkin, Raiffa, Thompson, Thrall, 1953) | not output-polynomial in the worst case | adds one inequality at a time; good in practice for degenerate inputs |
| [Reverse search](/reverse-search/) (Avis and Fukuda, 1992) | $O(m n v)$ for nondegenerate input, $O(mn)$ space | walks a spanning tree of the simplex graph backwards from the optimal basis |
| Fourier-Motzkin and its dual | doubly exponential | computes projections, not vertices, but the double description method is its dual |

The brute-force method tries each set $J$ of $n$ rows: if $A_J$ is nonsingular, it solves $A_J x = b_J$ by [Gaussian elimination](/gaussian-elimination/), checks $Ax \le b$, and keeps the point if it is new. Exact rational arithmetic matters here: a test such as $a_i^\top x \le b_i$ at a vertex is an equality test for the tight rows, and floating point gets it wrong.

## Bounds

- **Output size.** A polyhedron with $m$ rows in $\mathbb{R}^n$ has at most $\binom{m}{n}$ vertices, and by the upper bound theorem the exact maximum is reached by the polar of a cyclic polytope, with $\Theta(m^{\lfloor n/2 \rfloor})$ vertices for fixed $n$. So any algorithm needs time exponential in $n$ in the worst case.
- **Nondegenerate polytopes.** Reverse search lists the vertices with polynomial delay and polynomial space when no point lies on more than $n$ hyperplanes.
- **Unbounded polyhedra.** Given $P$ and some of its vertices, deciding whether there is another vertex is NP-complete (Khachiyan, Boros, Borys, Elbassioni and Gurvich, 2008). So no output-polynomial algorithm exists for vertex enumeration of unbounded polyhedra unless P = NP.
- **Bounded, degenerate polytopes.** Whether an output-polynomial algorithm exists is a well-known open problem. Degenerate vertices can have exponentially many bases, so pivoting methods that visit bases are not output-polynomial.

## Reductions

- **Linear programming to vertex enumeration.** By the fundamental theorem, the best listed vertex is optimal when the program is bounded. This is a correct but slow LP solver.
- **Vertex enumeration and convex hull.** For a polytope with the origin in its interior, the vertices of $P$ are the facets of its polar, so vertex enumeration and facet enumeration are the same problem.
- **Standard form.** Converting $Ax \le b$ with free $x$ to standard form (splitting $x = u - v$, adding slacks) does not keep the vertices: the new polyhedron can have vertices that come from no vertex of $P$. For pointed $P$, keep $x$ free and use the inequality form, or add slacks only.
- **Nash equilibria.** The Nash equilibria of a bimatrix game are pairs of vertices of two best-response polytopes that are complementary, so they can be found by enumerating vertices of both polytopes; see [Nash equilibrium](/nash-equilibrium/).

## Applications

- Converting between the two descriptions of a polytope in the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), in polyhedral combinatorics and in computational geometry.
- Finding all equilibria of a two-player game.
- Checking whether a set of linear constraints admits an integral vertex, or listing all optimal vertices of an LP with several optima.
- Testing LP solvers: the brute-force enumeration is an exact oracle for small inputs, as in the tests of the [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) page.

## References
