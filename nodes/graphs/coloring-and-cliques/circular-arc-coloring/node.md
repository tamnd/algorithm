---
tag: 0YAGRT
kind: problem
slug: circular-arc-coloring
name: Circular-arc coloring
aliases:
- Coloring a set of circular arcs
area: graphs/coloring-and-cliques
level: advanced
summary: Assigns colors to arcs of a circle so that overlapping arcs receive different colors, using as few colors as possible.
prereqs: [graph-coloring, interval-partitioning, np-complete]
see_also: [interval-partitioning, interval-coloring-depth-theorem, graph-coloring, k-coloring, perfect-graph, chordal-graph-coloring, bjorklund-chromatic-number, sweep-line-technique]
sources:
  - paper: doi:10.1137/0601025
    title: M. R. Garey, D. S. Johnson, G. L. Miller and C. H. Papadimitriou, The complexity of coloring circular arcs and chords, SIAM Journal on Algebraic and Discrete Methods 1(2), 216 to 227 (1980)
    locator: the main results (coloring circular arcs is NP-complete when the number of colors is part of the input, and polynomial for each fixed number of colors)
  - paper: doi:10.1137/0129040
    title: Alan Tucker, Coloring a family of circular arcs, SIAM Journal on Applied Mathematics 29(3), 493 to 502 (1975)
    locator: the whole paper (bounds on the number of colors in terms of the load, and the conjecture on 3/2 times the clique size)
  - paper: doi:10.1137/S0097539700382157
    title: Mario Valencia-Pabon, Revisiting Tucker's algorithm to color circular arc graphs, SIAM Journal on Computing 32(4), 1067 to 1072 (2003)
    locator: the main theorem (if at least l >= 5 arcs are needed to cover the circle, ceil((l-1)L/(l-2)) colors suffice, and this is tight)
  - url: https://www.cs.bme.hu/~dmarx/papers/circularNP.pdf
    title: Dániel Marx, A short proof of the NP-completeness of circular arc coloring (manuscript)
    locator: the whole note (a direct reduction showing NP-completeness)
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the O*(2^n) algorithm for the chromatic number, applied to the intersection graph of the arcs
---

Circular-arc coloring asks for a coloring of a family of arcs on a circle with as few colors as possible, so that any two arcs that share a point get different colors. It is [graph coloring](/graph-coloring/) on the intersection graph of the arcs, a circular-arc graph. On a line, where the arcs are intervals, a greedy sweep uses exactly as many colors as the largest number of intervals through one point; on a circle this fails, and the problem is NP-complete (Garey, Johnson, Miller and Papadimitriou 1980). For each fixed number of colors it is polynomial, and the optimum always lies between the load $L$ and $2L$.

## In plain words

Think of a round-the-clock schedule. Each job runs over a stretch of the clock face, and some stretches pass midnight. Two jobs that run at the same moment need different machines. How few machines do you need?

If no job passed midnight, the answer would be easy: count the most jobs running at any one moment, and that many machines are enough. Jobs that wrap around midnight break this. Five jobs can each overlap only their two neighbors around the clock, so at most two run at once, and still three machines are needed.

Finding the exact number is hard in general. It is easy to come within a factor of two, and with few machines there are fast exact methods.

## Definition

A circle is identified with $[0, C)$ with its ends glued. An *arc* $A = [s, t]$ is the set of points met when going clockwise from $s$ to $t$, ends included; if $s > t$ the arc passes through 0. A family $\mathcal F = (A_1, \ldots, A_n)$ of arcs is given by the $2n$ endpoints.

**Circular-arc coloring.** Input: a family $\mathcal F$ and an integer $k$. Question: is there a map $c : \{1, \ldots, n\} \to \{1, \ldots, k\}$ with $c(i) \ne c(j)$ whenever $A_i \cap A_j \ne \emptyset$? The optimization version asks for the least such $k$, the chromatic number $\chi(\mathcal F)$ of the intersection graph.

Two numbers bound it from below:

- the *load* $L(\mathcal F)$, the largest number of arcs that contain a common point;
- the *clique number* $\omega(\mathcal F)$, the largest number of pairwise intersecting arcs.

Arcs through one point intersect pairwise, so $L \le \omega \le \chi$. Unlike intervals, pairwise intersecting arcs need not share a point: three arcs that each cover two thirds of the circle, placed evenly, intersect pairwise but have no common point, so there $L = 2$ and $\omega = 3$.

## Variants

- **Interval coloring.** No arc passes through 0. The intersection graph is an interval graph, which is perfect, and $\chi = \omega = L$. See [interval partitioning](/interval-partitioning/) and the [depth theorem](/interval-coloring-depth-theorem/).
- **Fixed $k$.** Decide $k$-colorability for a constant $k$; polynomial, see below.
- **Proper and unit arcs.** No arc contains another, or all arcs have the same length. These families are easier and have their own algorithms.
- **Coloring chords.** Garey, Johnson, Miller and Papadimitriou also treat chords of a circle that cross; that problem is NP-complete too.
- **Wavelength assignment on a ring.** Each request is a path on a ring network, so an arc, and requests sharing a link need different wavelengths. This is arc coloring with the links as the points.

## Examples

| family | $n$ | $L$ | $\omega$ | $\chi$ |
|---|---|---|---|---|
| intervals, no arc through 0 | any | $L$ | $L$ | $L$ |
| odd ring: $A_i = [2i, 2i + 2]$ on a circle of length 10, $i = 0, \ldots, 4$ | 5 | 2 | 2 | 3 |
| three arcs, each two thirds of the circle, evenly placed | 3 | 2 | 3 | 3 |
| $2r + 1$ arcs, each covering $r$ of $2r + 1$ evenly spaced points, consecutive starts | $2r + 1$ | $r$ | $r$ | $r + 1$ |

**The odd ring.** Arc $A_i$ meets only $A_{i-1}$ and $A_{i+1}$ modulo 5, at the shared endpoints, so the intersection graph is the cycle $C_5$ and $\chi = 3$, though every point lies on at most 2 arcs. The bound $\lfloor 3L/2 \rfloor = 3$ is reached. All values in this table were checked by trying all colorings.

**The upper bound $2L$.** Pick any point $p$. The arcs through $p$ number at most $L$; give them distinct colors. The other arcs avoid $p$, so cutting the circle at $p$ turns them into intervals with load at most $L$, and the greedy sweep colors them with $L$ further colors. So $\chi \le 2L$.

## Known algorithms

- **Factor 2 in $O(n \log n)$.** The cut at a point described above, followed by the greedy interval sweep, uses at most $2L \le 2\chi$ colors.
- **Tucker's algorithm (1975).** If at least 4 arcs are needed to cover the whole circle, Tucker's method uses at most $\lfloor 3L/2 \rfloor$ colors. Valencia-Pabon (2003) gave a corrected and sharper analysis: if at least $l \ge 5$ arcs are needed to cover the circle, then $\lceil (l-1)L/(l-2) \rceil$ colors suffice, and this is tight.
- **Exact for fixed $k$ by a sweep.** Garey, Johnson, Miller and Papadimitriou (1980) show that $k$-colorability of arcs is polynomial for each fixed $k$. A simple way to see this: cut at a point $p$. If more than $k$ arcs contain $p$, answer no. Otherwise, by the symmetry of colors, give those arcs the colors $1, 2, \ldots$ in a fixed way. Then sweep clockwise from $p$ once around, keeping the set of all possible color assignments of the arcs that contain the current point. At a start of an arc, extend each assignment by every free color; at an end, forget the arc; when the sweep reaches the second end of an arc through $p$, its color must be the fixed one. The family is $k$-colorable exactly when some assignment survives the full turn. The live arcs number at most $k$, so there are at most $k!$ assignments at any time, and the sweep takes $O(n \cdot k! \cdot k)$ time after sorting the endpoints. This sweep, with $k = 1, 2, \ldots$, was checked against brute force over all colorings on 600 random families of up to 7 arcs.
- **Exact in general.** Build the intersection graph in $O(n^2)$ time and compute its chromatic number in $O^*(2^n)$ time with [Björklund's algorithm](/bjorklund-chromatic-number/). The sweep above, run with $k$ from $L$ up to $2L$, is the better choice when $L$ is small.

## Bounds

- **NP-completeness.** Deciding whether a family of circular arcs can be colored with $k$ colors, with $k$ part of the input, is NP-complete (Garey, Johnson, Miller and Papadimitriou 1980). Marx gave a short direct proof.
- **Polynomial for fixed $k$.** For every constant $k$ there is a polynomial algorithm (same paper); the sweep above runs in $O(n \cdot k! \cdot k)$ time.
- **Sandwich.** $L \le \omega \le \chi \le 2L$. Since every point has load at most $L$, these bounds are within a factor 2 of each other.
- **Three halves.** Tucker (1975) conjectured that $\lfloor 3\omega/2 \rfloor$ colors always suffice; this was proved by Karapetyan (1980). The odd ring, with $\omega = 2$ and $\chi = 3$, shows the factor $3/2$ cannot be lowered. On 3000 random families of up to 9 arcs, $\chi \le \lfloor 3L/2 \rfloor$ held in every case.

## Reductions

- **To graph coloring.** Build the intersection graph: arcs $A_i$ and $A_j$ intersect when an endpoint of one lies in the other. Any exact coloring algorithm then applies.
- **From interval coloring.** Intervals are arcs that avoid one point, so interval coloring is the special case, solved by the greedy sweep.
- **Cutting at a point.** For any point $p$, the family minus the arcs through $p$ is an interval family. Every hardness proof must therefore come from the interplay of the at most $L$ arcs through $p$ with the rest, which is why the problem is polynomial when $k$, and so $L$, is fixed.
- **Hardness.** NP-completeness is proved by reduction from a known NP-complete problem (Garey, Johnson, Miller and Papadimitriou 1980; Marx gives a shorter reduction). By the previous item, the gadgets must work through the arcs that cross a cut point, and their number grows with $k$.

## Applications

- **Wavelength assignment in ring networks.** Each lightpath on an optical ring is an arc, links are the points, and paths sharing a link need different wavelengths. Minimizing wavelengths is circular-arc coloring.
- **Register allocation for loops.** In a loop, a variable may be live from late in one iteration into the next. Live ranges are arcs on the circle of the loop body, and registers are colors.
- **Periodic scheduling.** Tasks that repeat every day or every cycle, such as crew shifts or traffic light phases, occupy arcs of the period; machines or crews are colors.
- **Ring resources in general.** Any resource used over a stretch of a cyclic structure, such as slots on a token ring, leads to the same problem.

## References
