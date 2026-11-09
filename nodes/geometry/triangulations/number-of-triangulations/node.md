---
tag: A7KD6Y
kind: problem
slug: number-of-triangulations
name: Counting triangulations of point sets
aliases:
- Triangulation counting problem
- number of triangulations
- counting triangulations
area: geometry/triangulations
level: research
summary: Count or bound the number of triangulations of a planar point set; hard in general.
model: real-ram
prereqs: [triangulation-of-point-set, catalan-triangulation-theorem, polygon-triangulation-dp]
see_also: [flip-graph, catalan-numbers, triangulation-counting-theorem, min-weight-triangulation, flip-distance, interval-dp, polygon-triangulation, flip-graph-diameter-theorem]
sources:
  - paper: "Victor Alvarez and Raimund Seidel, A simple aggregative algorithm for counting triangulations of planar point sets and related problems, Proceedings of the 29th Symposium on Computational Geometry, 1 to 8 (2013)"
    locator: the O(n^2 2^n) algorithm by sweeping monotone paths
  - paper: "Micha Sharir and Adam Sheffer, Counting triangulations of planar point sets, Electronic Journal of Combinatorics 18(1), paper 70 (2011)"
    locator: every set of n points has O(30^n) triangulations
  - paper: "Adrian Dumitrescu, André Schulz, Adam Sheffer and Csaba D. Tóth, Bounds on the maximum multiplicity of some common geometric graphs, SIAM Journal on Discrete Mathematics 27(2), 802 to 826 (2013)"
    locator: point sets with Ω(8.65^n) triangulations
  - paper: "Alfredo García, Marc Noy and Javier Tejel, Lower bounds on the number of crossing-free subgraphs of K_N, Computational Geometry 16(4), 211 to 221 (2000)"
    locator: the double chain with Θ(8^n) triangulations up to polynomial factors
  - paper: "Oswin Aichholzer, Victor Alvarez, Thomas Hackl, Alexander Pilz, Bettina Speckmann and Birgit Vogtenhuber, An improved lower bound on the minimum number of triangulations, Proceedings of the 32nd Symposium on Computational Geometry, article 7 (2016)"
    locator: every set of n points in general position has Ω(2.631^n) triangulations
  - paper: "Victor Alvarez, Karl Bringmann, Radu Curticapean and Saurabh Ray, Counting triangulations and other crossing-free structures via onion layers, Discrete and Computational Geometry 53(4), 675 to 690 (2015)"
    locator: a subexponential algorithm for points with few convex layers (venue and title to be checked)
  - paper: "Dániel Marx and Tillmann Miltzow, Peeling and nibbling the cactus, subexponential-time algorithms for counting triangulations and related problems, Proceedings of the 32nd Symposium on Computational Geometry, article 52 (2016)"
    locator: an n^O(√n) algorithm for counting triangulations
---

Counting triangulations asks how many [triangulations](/triangulation-of-point-set/) a given set of $n$ points in the plane has, and how large or small that number can be over all sets of $n$ points. For points in convex position the answer is the Catalan number $C_{n-2}$, and for the vertices of a simple polygon an $O(n^3)$ [dynamic program](/polygon-triangulation-dp/) counts the triangulations exactly. For general point sets the number depends on the order type and ranges between about $2.63^n$ and $30^n$; the best exact algorithm takes $O(n^2 2^n)$ time, or $n^{O(\sqrt{n})}$ time in theory, and whether the problem is #P-hard is open.

## In plain words

Put some dots on paper. In how many different ways can you connect them into triangles, with no crossings and using every dot? Around a circle the answer follows a known sequence: 2 ways for 4 dots, 5 for 5, 14 for 6, and so on. For dots placed in other patterns the answer changes a lot, and the hard question is how to count the ways without listing them one by one.

There are always very many: at least about $2.63$ to the power of the number of dots, and at most about $30$ to that power.

## Definition

**Input.** A set $S$ of $n$ points in the plane, not all on one line.

**Output.** The number $\mathrm{tr}(S)$ of triangulations of $S$, triangulations that use every point as a vertex and cover the convex hull.

**Extremal questions.** Let $\mathrm{tr}_{\max}(n)$ and $\mathrm{tr}_{\min}(n)$ be the largest and smallest values of $\mathrm{tr}(S)$ over sets of $n$ points in general position. Determine their growth rates.

All triangulations of $S$ have the same numbers of edges, $3n - h - 3$, and of triangles, $2n - h - 2$, where $h$ is the number of hull points; see the [triangulation counting theorem](/triangulation-counting-theorem/). So $\mathrm{tr}(S)$ counts different structures of the same size.

## Variants

- **Simple polygons.** Count the triangulations of a polygon by diagonals: $O(n^3)$ by the interval DP, $t(i, j) = \sum_k t(i, k) \, t(k, j)$ over valid triangles $v_i v_k v_j$.
- **Convex position.** $\mathrm{tr} = C_{n-2} = \frac{1}{n-1}\binom{2n-4}{n-2}$, by the [Catalan triangulation theorem](/catalan-triangulation-theorem/).
- **Other crossing-free structures.** Count all plane graphs, spanning trees, perfect matchings or spanning cycles on $S$; the same sweep algorithms apply.
- **Approximate counting.** Estimate $\mathrm{tr}(S)$ within a factor $1 \pm \varepsilon$; random walks on the [flip graph](/flip-graph/) mix fast for convex polygons, but no fast sampler is known for general point sets.
- **Sampling.** Draw a uniformly random triangulation. For convex polygons this is easy through bijections with binary trees.

## Examples

The following counts come from enumerating all triangulations by computer with exact predicates.

| point set | $n$ | $h$ | $\mathrm{tr}$ |
|---|---|---|---|
| triangle $(0,0)$, $(6,0)$, $(0,6)$ with $(1,1)$ inside | 4 | 3 | 1 |
| square $(0,0)$, $(4,0)$, $(4,4)$, $(0,4)$ with $(1,2)$ inside | 5 | 4 | 3 |
| triangle $(0,0)$, $(12,0)$, $(0,12)$ with $(2,3)$ and $(5,2)$ inside | 5 | 3 | 2 |
| convex hexagon | 6 | 6 | 14 |
| triangle $(0,0)$, $(20,0)$, $(10,17)$ with $(10,1)$, $(15,8)$, $(5,8)$ near the side midpoints | 6 | 3 | 4 |
| double chain $(0,0)$, $(3,1)$, $(6,0)$ and $(0,8)$, $(3,7)$, $(6,8)$ | 6 | 4 | 6 |
| square $(0,0)$, $(10,0)$, $(10,10)$, $(0,10)$ with $(5,1)$, $(9,5)$, $(5,9)$, $(1,5)$ | 8 | 4 | 30 |
| convex octagon | 8 | 8 | 132 |
| double chain $(0,0)$, $(3,1)$, $(6,1)$, $(9,0)$ and $(0,20)$, $(3,19)$, $(6,19)$, $(9,20)$ | 8 | 4 | 80 |

Convex position is not the maximum: for $n = 8$, the double chain has fewer triangulations than the octagon, but for large $n$ the double chain has about $8^n$, far more than $C_{n-2} \approx 4^n$. The configurations with points just inside the hull edges, the **double circles**, have few triangulations.

## Known algorithms

| method | time | note |
|---|---|---|
| enumeration through the flip graph | $O(\mathrm{tr}(S) \cdot \mathrm{poly}(n))$ | lists every triangulation |
| polygon DP | $O(n^3)$ | simple polygons and convex position only |
| Alvarez and Seidel | $O(n^2 2^n)$ | dynamic programming over monotone paths |
| Alvarez, Bringmann, Curticapean and Ray | subexponential for few onion layers | separators on convex layers |
| Marx and Miltzow | $n^{O(\sqrt{n})}$ | planar separators of the triangulation |

**The Alvarez and Seidel algorithm.** Sort the points by $x$. Every triangulation can be built triangle by triangle so that the boundary of the part built so far is always an $x$-monotone path from the leftmost to the rightmost point, and with a canonical rule for which triangle to add next, each triangulation corresponds to exactly one sequence of such paths. A monotone path is a subset of the points ordered by $x$, so there are at most $2^n$ of them. Counting paths in this directed acyclic graph by dynamic programming gives $\mathrm{tr}(S)$ in $O(n^2 2^n)$ time. The same scheme counts other crossing-free structures.

## Bounds

- **Maximum.** $\mathrm{tr}_{\max}(n) = O(30^n)$ (Sharir and Sheffer), through charging schemes and the cross-graph method; $\mathrm{tr}_{\max}(n) = \Omega(8.65^n)$ (Dumitrescu, Schulz, Sheffer and Tóth), by the Koch chain. The double chain gives $\Theta^*(8^n)$ (García, Noy and Tejel), where $\Theta^*$ hides polynomial factors.
- **Minimum.** $\mathrm{tr}_{\min}(n) = \Omega(2.631^n)$ (Aichholzer, Alvarez, Hackl, Pilz, Speckmann and Vogtenhuber). The double circle has $\Theta^*(\sqrt{12}^{\,n})$, about $3.46^n$, triangulations and is conjectured to be the minimum.
- **Convex position.** $C_{n-2} = \Theta(4^n n^{-3/2})$.
- **Complexity.** Counting is in #P, since a triangulation can be checked in polynomial time, but no #P-hardness proof is known for point sets, and no polynomial algorithm is known either.

## Reductions

- **To counting paths in a DAG.** The Alvarez and Seidel algorithm reduces counting to paths over the monotone path graph.
- **From triangulations to other structures.** Every crossing-free graph on $S$ is a subgraph of some triangulation, and every triangulation has at most $2^{3n - h - 3}$ subgraphs, so bounds on $\mathrm{tr}_{\max}$ give bounds for plane graphs, spanning trees and matchings.
- **To the polygon DP.** Points in convex position, or a polygon given with its vertices, reduce to the interval DP, which counts with the same recurrence as [optimal polygon triangulation](/polygon-triangulation-dp/) with sum and product in place of min and plus.

## Applications

- **Extremal combinatorics.** Bounds on $\mathrm{tr}_{\max}$ give the best bounds on the numbers of crossing-free graphs, spanning trees and matchings on $n$ points.
- **Enumeration and testing.** Counting gives exact checks for enumeration code and the size of a search space, for example for the [minimum weight triangulation](/min-weight-triangulation/) of small sets.
- **Random triangulations.** Uniform sampling, which depends on counting, provides test inputs for geometric algorithms.

## References
