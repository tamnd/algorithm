---
tag: 2DX733
kind: problem
slug: heilbronn-triangle-problem
name: Heilbronn triangle problem
aliases:
- Heilbronn problem
- Heilbronn's triangle problem
- Heilbronn number
area: geometry/geometric-optimization
level: research
summary: Place n points in a unit square to make the smallest triangle they span as large as possible. The answer is between log n/n^2 and n^(-8/7-1/2000) in order; the exact order is open.
prereqs: [oriented-triangle-area, probabilistic-method]
see_also: [maximum-area-inscribed-triangle, minimum-area-enclosing-triangle, 3sum-hardness, probabilistic-method, discrepancy, lattice, euclidean-steiner-tree-problem, minimum-width-annulus]
sources:
  - paper: "K. F. Roth, On a problem of Heilbronn, Journal of the London Mathematical Society 26(3), 1951"
    locator: the first upper bound O(1/(n √(log log n))), and Erdős's lower bound construction from the parabola modulo a prime
  - paper: "Wolfgang M. Schmidt, On a problem of Heilbronn, Journal of the London Mathematical Society (2) 4, 1972"
    locator: the upper bound O(1/(n √(log n)))
  - paper: "J. Komlós, J. Pintz and E. Szemerédi, On Heilbronn's triangle problem, Journal of the London Mathematical Society (2) 24, 1981"
    locator: the upper bound O(n^(-8/7+ε)) for every ε > 0
  - paper: "J. Komlós, J. Pintz and E. Szemerédi, A lower bound for Heilbronn's problem, Journal of the London Mathematical Society (2) 25, 1982"
    locator: the lower bound Ω(log n / n^2), which disproves Heilbronn's conjecture of O(1/n^2)
  - paper: "Alex Cohen, Cosmin Pohoata and Dmitrii Zakharov, A new upper bound for the Heilbronn triangle problem, arXiv preprint, 2023"
    locator: the upper bound O(n^(-8/7-1/2000)), the first improvement of the exponent 8/7 since 1981
  - paper: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry: Theory and Applications 5(3), 1995"
    locator: 3SUM-hardness of deciding if three points of a set are collinear, the degenerate case of the smallest triangle
  - paper: "Tao Jiang, Ming Li and Paul Vitányi, The average-case area of Heilbronn-type triangles, Random Structures and Algorithms 20(2), 2002"
    locator: the expected smallest triangle area of n uniform random points is of order 1/n^3
---

The Heilbronn triangle problem asks how to place $n$ points in the unit square so that the smallest triangle formed by any three of them has the largest possible area. This largest possible smallest area is $\Delta(n)$. Heilbronn conjectured around 1950 that $\Delta(n) = O(1/n^2)$. Erdős showed $\Delta(n) = \Omega(1/n^2)$ with points on a parabola modulo a prime, but Komlós, Pintz and Szemerédi (1982) disproved the conjecture with the lower bound $\Omega(\log n / n^2)$. The upper bound fell from $O(1/n)$ through Roth (1951), Schmidt (1972) and Komlós, Pintz and Szemerédi (1981) to $O(n^{-8/7-1/2000})$ by Cohen, Pohoata and Zakharov (2023). The exact order of $\Delta(n)$ is open.

## In plain words

Put some dots in a square. Any three dots make a triangle, and some of these triangles are thin or small. You want to place the dots so that even the smallest triangle is as big as you can make it. In particular, no three dots may lie on one line.

With more dots, the square gets crowded and the smallest triangle must shrink. The question is how fast it shrinks as the number of dots grows.

A grid is a bad choice, because grids have many dots on one line. Dots on a curve that bends, such as a parabola, do much better. Clever random choices do a little better still. Mathematicians have proved that the answer lies between two rates, but nobody knows the true rate.

## Definition

Notation: $Q = [0, 1]^2$ is the unit square. For a finite set $P$ of at least three points, $\delta(P)$ is the least area of a triangle with vertices in $P$; it is 0 if three points of $P$ are collinear.

**Input.** An integer $n \ge 3$.

**Output.** The value $\Delta(n) = \sup \{ \delta(P) : P \subseteq Q, |P| = n \}$, and point sets that attain or approach it.

The supremum is attained, because $\delta$ is continuous on the compact set $Q^n$. Replacing $Q$ by another compact convex region of area 1, such as a disk, changes $\Delta(n)$ only by a constant factor, so all the bounds below hold for every such region up to constants.

**General position.** A set with $\delta(P) > 0$ has no three collinear points; this is the only condition, and it is forced by optimality.

## Variants

- **Other regions.** Disks, triangles and general convex regions of area 1, with the same order of growth.
- **Higher dimensions.** The largest least volume of a simplex spanned by $k + 1$ of $n$ points in the unit cube of $\mathbb{R}^d$.
- **$k$-gons.** Maximize the least area of the convex hull of $k$ of the points.
- **Random and online versions.** The expected least area of $n$ uniform random points, and placing points one by one without knowing $n$.
- **No-three-in-line on a grid.** Choose $2m$ points of the $m \times m$ grid with no three collinear, the discrete cousin of the problem.
- **Computing $\delta(P)$.** For a given set, find its smallest triangle. This is the algorithmic subproblem of any search for good configurations.

## Examples

| configuration | $n$ | $\delta(P)$ in the unit square | $n^2 \delta(P)$ |
|---|---|---|---|
| three or four corners of the square | 3 or 4 | $1/2$ | |
| parabola modulo 5, scaled by $1/4$ | 5 | $1/32$ | $0.78$ |
| parabola modulo 7, scaled by $1/6$ | 7 | $1/72$ | $0.68$ |
| parabola modulo 13, scaled by $1/12$ | 13 | $1/288$ | $0.59$ |

**Small $n$.** Every triangle in the unit square has area at most $1/2$, and the four corners have $\delta = 1/2$. So $\Delta(3) = \Delta(4) = 1/2$.

**Erdős's parabola.** For a prime $p$, take $P_p = \{ (x, x^2 \bmod p) : 0 \le x < p \}$. For $p = 5$ this is $(0,0), (1,1), (2,4), (3,4), (4,1)$, and for $p = 7$ it is $(0,0), (1,1), (2,4), (3,2), (4,2), (5,4), (6,1)$. In both, the smallest triangle has area exactly $1/2$ in grid units, the least possible for a nondegenerate lattice triangle. Scaling the box $[0, p-1]^2$ to the unit square divides areas by $(p-1)^2$.

**Random points.** For 200 sets of $n$ uniform random points, the mean smallest area times $n^3$ was $0.94$ for $n = 8$, $0.68$ for $n = 16$ and $0.53$ for $n = 32$. Random sets are far worse than the parabola, in line with the order $1/n^3$ of Jiang, Li and Vitányi.

## Known algorithms

There is no algorithm that computes $\Delta(n)$ for general $n$. Exact values are proved only for small $n$, and good configurations for larger $n$ come from numerical search.

| task | method | time |
|---|---|---|
| compute $\delta(P)$ by brute force | all triples | $O(n^3)$ |
| compute $\delta(P)$ | dual line arrangement; for each point, the nearest line in vertical distance by topological sweep | $O(n^2)$ |
| decide $\delta(P) = 0$ | three collinear points, by the same sweep or by sorting directions around each point | $O(n^2)$ |
| search for good $P$ | local search, simulated annealing, constrained optimization | heuristic |

The $O(n^2)$ algorithms are believed to be optimal: deciding whether three of $n$ points are collinear is [3SUM-hard](/3sum-hardness/) (Gajentaan and Overmars 1995), so no $O(n^{2-c})$ algorithm for $\delta(P)$ is expected.

## Bounds

**Trivial upper bound.** Let $k = \lfloor (n-1)/2 \rfloor$. Cut $Q$ into $k$ vertical strips of width $1/k$. Some strip holds at least 3 of the $n$ points, and a triangle inside a strip of width $1/k$ and height 1 has area at most $1/(2k)$. So $\Delta(n) \le 1/(2k) = O(1/n)$.

**Erdős's lower bound.** Let $p$ be prime and $0 \le x_1 < x_2 < x_3 < p$, with $y_i = x_i^2 \bmod p$. Twice the signed area of the triangle is an integer $A = (x_2 - x_1)(y_3 - y_1) - (x_3 - x_1)(y_2 - y_1)$. Modulo $p$, $A \equiv (x_2 - x_1)(x_3 - x_1)(x_3 - x_2) \not\equiv 0$, because each factor lies strictly between 0 and $p$. So $|A| \ge 1$ and every triangle has area at least $1/2$. Scaled to $Q$, $\delta(P_p) \ge 1/(2(p-1)^2)$. For any $n \ge 3$, take a prime $p$ with $n \le p < 2n$ and any $n$ points of $P_p$: $\Delta(n) > 1/(8n^2)$.

**Best known bounds.**

$$c\, \frac{\log n}{n^2} \le \Delta(n) \le C\, n^{-8/7 - 1/2000}$$

for constants $c, C > 0$ and all large $n$. The lower bound is due to Komlós, Pintz and Szemerédi (1982), by a probabilistic construction with deletions. The upper bound is due to Cohen, Pohoata and Zakharov (2023). The gap between the exponents 2 and $8/7 + 1/2000 \approx 1.1434$ is wide, and the exact order of $\Delta(n)$ is open.

| year | authors | upper bound |
|---|---|---|
| 1951 | Roth | $O(1/(n \sqrt{\log \log n}))$ |
| 1972 | Schmidt | $O(1/(n \sqrt{\log n}))$ |
| 1972 | Roth | $O(n^{-\mu})$ with $\mu = 2 - 2/\sqrt{5} \approx 1.105$, up to $\varepsilon$ in the exponent |
| 1981 | Komlós, Pintz and Szemerédi | $O(n^{-8/7+\varepsilon})$ |
| 2023 | Cohen, Pohoata and Zakharov | $O(n^{-8/7-1/2000})$ |

**Random sets.** For $n$ independent uniform points in $Q$, the expected value of $\delta(P)$ is $\Theta(1/n^3)$ (Jiang, Li and Vitányi 2002). So random sets are far from optimal, and good sets need structure or a random construction with repairs.

## Reductions

- **From 3SUM.** Testing $\delta(P) = 0$, three collinear points, is 3SUM-hard. So computing $\delta(P)$ exactly in subquadratic time would give a subquadratic 3SUM algorithm.
- **To incidence and discrepancy questions.** The upper bounds come from counting how many points can lie in thin strips, a question of [discrepancy](/discrepancy/) and incidence geometry.
- **To independent sets in hypergraphs.** The lower bound of Komlós, Pintz and Szemerédi picks random points, forms the 3-uniform hypergraph of triples with small area, and takes a large independent set in it, a refinement of the [probabilistic method](/probabilistic-method/) with deletions.

## Applications

- **Point sets in general position.** Well spread sets with no thin triangles are useful test inputs for geometric algorithms, since they avoid near degeneracies.
- **Sampling and quasi Monte Carlo.** The problem is one of several measures of how evenly a point set covers a region, next to discrepancy and dispersion.
- **Combinatorial geometry.** Its methods, such as counting points in thin strips, feed into related problems on lines and strips.

## References
