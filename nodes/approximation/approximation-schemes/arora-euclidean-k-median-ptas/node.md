---
tag: PXSWAG
kind: algorithm
slug: arora-euclidean-k-median-ptas
name: Arora-Raghavan-Rao PTAS for Euclidean k-median
aliases:
- Arora-Raghavan-Rao scheme
- ARR k-median scheme
- portal-based k-median PTAS
area: approximation/approximation-schemes
level: research
summary: Adapts Arora's portal dissection to clustering, giving a (1+ε)-approximation for k-median in fixed-dimensional Euclidean space.
solves: [euclidean-k-median]
model: real-ram
complexity:
  vars: {n: the number of points, ε: the accuracy parameter}
  time: {worst: n^O(1/ε), average: n^O(1/ε), best: n^O(1/ε)}
  space: {extra: n^O(1/ε)}
properties: {online: false, deterministic: false, recursive: true}
history:
  year: 1998
  people: [Sanjeev Arora, Prabhakar Raghavan, Satish Rao]
  note: Arora, Raghavan and Rao gave the first approximation scheme for k-median in the plane, by a dynamic program over a shifted quadtree whose states record distances at the portals.
prereqs: [euclidean-k-median, portal-based-dissection, quadtree, k-median-problem, linearity-of-expectation]
see_also: [arora-euclidean-tsp-ptas, k-median-inapproximability, facility-location-problem, coreset, k-means, geometric-median, guillotine-cut-technique, ptas]
sources:
  - paper: doi:10.1145/276698.276718
    title: S. Arora, P. Raghavan and S. Rao, Approximation schemes for Euclidean k-medians and related problems, STOC 1998, pp. 106-113
    locator: the structure theorem for k-median, the distance profiles at the portals and the dynamic program
  - paper: "S. Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998, pp. 753-782"
    title: Arora 1998
    locator: the shifted dissection and the portals
  - paper: "S. G. Kolliopoulos and S. Rao, A nearly linear-time approximation scheme for the Euclidean k-median problem, SIAM Journal on Computing 37(3), 2007, pp. 757-782"
    title: Kolliopoulos and Rao 2007
    locator: the scheme with time nearly linear in n for fixed d and ε
  - paper: "V. Arya, N. Garg, R. Khandekar, A. Meyerson, K. Munagala and V. Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 2004, pp. 544-562"
    title: Arya, Garg, Khandekar, Meyerson, Munagala and Pandit 2004
    locator: a constant factor solution by local search, usable as the first step
---

The scheme of Arora, Raghavan and Rao (1998) was the first approximation scheme for [Euclidean $k$-median](/euclidean-k-median/). For each fixed $\varepsilon > 0$ it finds, for $n$ points in the plane, $k$ centres whose cost is at most $(1 + \varepsilon)\,\mathrm{OPT}$ in expectation, in time $n^{O(1/\varepsilon)}$. It applies [portal-based dissection](/portal-based-dissection/): a randomly shifted quadtree with portals on the sides of its squares. Each point is served along a path to its centre that crosses square sides only at portals. The new idea is the state of the dynamic program: a square records how many centres it holds, and, at each portal, the rounded distance to the nearest centre inside and outside the square. These distances change by at most one unit from portal to portal, so there are few such records. The full analysis of the rounding is long, so this page gives the structure theorem and the counting in full and the dynamic program as an outline.

## In plain words

We must place a few service points so that the total distance from all homes to their nearest service point is small. Cut the map into a hierarchy of squares, dropped at a random offset, and put a few gates on each square wall. Pretend that every trip to a service point must pass walls only at gates. Such a trip is a little longer than the straight one, and on average only a little.

Now each square can be solved knowing only a short summary: how many service points it holds, and, for each gate, how far it is to the nearest service point inside and outside. Neighbouring gates are close, so their distances are nearly equal, and the number of possible summaries stays small. The computer fills a table of summaries from the smallest squares to the largest.

## The problem

The input is a set $P$ of $n$ points in the plane, an integer $k \ge 1$ and an accuracy $\varepsilon \in (0, 1)$. The output is a set $C$ of at most $k$ centres with
$$\mathrm{cost}(C) = \sum_{p \in P} \min_{c \in C} \lVert p - c \rVert \le (1 + \varepsilon)\,\mathrm{OPT}$$
in expectation over the random shift, or always if all shifts are tried. Centres can be anywhere in the plane; after the first step they are chosen among the centres of the cells of a grid.

## The algorithm

Let $D = \log_2(2L)$ be the number of levels of the dissection. A grid line of level $i$ is a side of squares of side $2L/2^i$ and carries portals at gap $2L/(2^i m)$.

```pseudo id=main
ARR-K-MEDIAN(P, k, ε)
L1  bound OPT by a constant factor solution; snap the points to a grid and split far apart groups, so that each part has an L × L grid with L = O(n²/ε), L a power of 2
L2  pick the shift a, b uniformly from {0, ..., L − 1} and build the shifted quadtree of the root square of side 2L
L3  on each side of each square put m portals, with m a power of 2 and m ≥ 2√2 D/ε
L4  a state of a square Q is (j, φ_in, φ_out): j ≤ k centres in Q, and for each portal the rounded distance to the nearest centre in Q and outside Q
L5  for each square from the leaves up, and each state, combine states of the four children whose counts add up to j and whose profiles agree through the portals
L6  store the least cost of the points of Q, each served along a portal-respecting path, by a centre in Q or through a portal at the distance φ_out
L7  return the centres of the best root state with j ≤ k and no centre outside; repeat for several shifts and keep the best
```

*Line L1.* A constant factor solution, for example by [local search](/local-search/), gives a value $A$ with $\mathrm{OPT} \le A \le c\,\mathrm{OPT}$. Two points of one optimal cluster are within $2A$ of each other, so the groups of points linked by distances at most $2A$ can be solved one by one, with $k$ divided among them by a small dynamic program. A group has diameter at most $2nA$. A grid of gap $\Theta(\varepsilon A/n)$ moves each point by $O(\varepsilon A/n)$, which changes any solution by $O(\varepsilon A) = O(\varepsilon\,\mathrm{OPT})$, and gives $L = O(n^2/\varepsilon)$.

*Line L4.* The distances are stored in whole multiples of a unit that depends on the level of the square. Consecutive portals around a square are one gap apart, so the stored values change by at most one unit from portal to portal. A profile is then fixed by one number and a sequence of steps in $\{-1, 0, 1\}$.

## Example

Take $L = 8$, so $D = 4$, the seven points $(0, 0)$, $(1, 0)$, $(1, 1)$, $(2, 1)$, $(6, 6)$, $(6, 7)$, $(7, 5)$, which stand for the centres of these cells, and $k = 2$. Among the 64 cells, the best centres are $(1, 0)$ and $(6, 6)$, with cost $1 + 0 + 1 + \sqrt 2 + 0 + 1 + \sqrt 2 = 3 + 2\sqrt 2 \approx 5.83$. The seven segments to the centres cross the grid lines $1 + 0 + 1 + 2 + 0 + 1 + 2 = 7$ times.

For the shift $(3, 5)$ and $m = 2$, the segment from $(0, 0)$ to $(1, 0)$ crosses the line $x = 1$ at height $\frac12$. That line has level 2, with portal gap $16/(4 \cdot 2) = 2$, and the nearest portal is at height $1$, so the detour is $2 \cdot \frac12 = 1$. All the detours together add 3, and the portal-respecting cost is $6 + 2\sqrt 2 \approx 8.83$. The mean over all 64 shifts, against the bound $\mathrm{OPT} + 7D/m$ of the structure theorem:

| $m$ | mean portal-respecting cost | bound |
|---|---|---|
| 1 | $14.33$ | $33.83$ |
| 2 | $9.20$ | $19.83$ |
| 4 | $7.08$ | $12.83$ |
| 8 | $6.20$ | $9.33$ |

The extra cost falls roughly in proportion to $1/m$, as the theorem predicts. With $m \ge 2\sqrt 2\, D/\varepsilon$ the mean is at most $(1 + \varepsilon/2)\,\mathrm{OPT}$.

## Correctness

1. **Structure theorem.** Take an optimal solution and serve each point along its segment to its centre, with every crossing of a grid line moved to the nearest portal. A segment of length $s$ crosses at most $\sqrt 2\, s$ grid lines. A line has level $i$ with probability at most $2^{i-1}/L$ over the shift, and then a detour costs at most one gap, $2L/(2^i m)$. So a crossing costs at most $D/m$ in expectation, and the expected total is at most $(1 + \sqrt 2\, D/m)\,\mathrm{OPT}$. No limit on the crossings per side is needed, since each path is a single segment and paths may share portals.
2. **Smooth profiles.** Consecutive portals around a square are one gap $g$ apart, so their distances to the nearest centre differ by at most $g$, and the rounded values by at most one unit. So a square has at most $\mathrm{poly}(n/\varepsilon) \cdot 3^{4m}$ profiles.
3. **The dynamic program.** The portal-respecting solution above is consistent with one state of each square, so the root value is at most its cost plus the rounding error. Every root value is the cost of a real set of at most $k$ centres plus non-negative detours. With the rounding unit chosen per level so that the errors add up to at most $(\varepsilon/2)\,\mathrm{OPT}$, the expected cost is at most $(1 + \varepsilon)\,\mathrm{OPT}$.

Parts 1 and 2 are proved in full below; part 3 is an outline of the argument of Arora, Raghavan and Rao.

## Complexity

- **Time.** There are $O(nD)$ squares. A state has $k + 1$ counts and two profiles, so a square has $(k + 1)(\mathrm{poly}(n/\varepsilon) \cdot 3^{4m})^2$ states. With $m = O(\log(n/\varepsilon)/\varepsilon)$ this is $n^{O(1/\varepsilon)}$, and combining four children costs $n^{O(1/\varepsilon)}$ per parent state. The total is $n^{O(1/\varepsilon)}$ for fixed $\varepsilon < 1$. Trying all $L^2$ shifts multiplies it by a polynomial. The model is the [real RAM](/real-ram/).
- **Space.** The table has $n^{O(1/\varepsilon)}$ entries.

## Properties

| claim | statement | status |
|---|---|---|
| structure theorem | expected portal-respecting cost at most $(1 + \sqrt 2\, D/m)\,\mathrm{OPT}$ | proved below |
| smooth profiles | rounded portal distances change by at most one unit between consecutive portals | proved below |
| guarantee | expected cost at most $(1 + \varepsilon)\,\mathrm{OPT}$ in the plane | outline below; full proof in the paper |
| time | $n^{O(1/\varepsilon)}$ in the plane | outline below |
| higher dimension | quasi-polynomial time $n^{O((\log n/\varepsilon)^{d-1})}$ for fixed $d$ | from the paper |

## Variants and improvements

- **Fixed dimension.** In $\mathbb{R}^d$ a cube has $O(m^{d-1})$ portals per facet, and the profiles have $3^{O(m^{d-1})}$ forms. Arora, Raghavan and Rao get quasi-polynomial time $n^{O((\log n/\varepsilon)^{d-1})}$.
- **Nearly linear time.** Kolliopoulos and Rao (1999, journal version 2007) use an adaptive dissection and a different structure theorem, and reach time $2^{O((\log(1/\varepsilon)/\varepsilon)^{d-1})} n \log^{d+6} n$ for fixed $d$.
- **Coresets.** For fixed $k$ and $d$, a [coreset](/coreset/) of small size can replace the input, and an exhaustive search on it gives a $(1 + \varepsilon)$ solution in time linear in $n$ (Har-Peled and Mazumdar 2004).
- **Local search.** Cohen-Addad, Klein and Mathieu showed that local search that swaps a number of centres depending on $d$ and $\varepsilon$ alone is itself an approximation scheme for $k$-median and [$k$-means](/k-means/) in fixed dimension.
- **Related problems.** The same dissection gives schemes for facility location, where each centre has an opening cost, and for the [TSP](/arora-euclidean-tsp-ptas/), where the state records the pairing of portals instead of distances.

## When to use it

The scheme settles the complexity of Euclidean $k$-median in fixed dimension: it is NP-hard, yet every ratio $1 + \varepsilon$ is reachable in polynomial time. The exponent grows like $1/\varepsilon$ and the tables are very large, so it is not a practical algorithm. For real data, local search, Lloyd-type heuristics or a coreset with exhaustive search for small $k$ are the usual choices. The design of the state, distances at portals with bounded steps, is the reusable idea; it carries over to facility location and to other problems where points connect to chosen centres.

## Pitfalls

- **No crossing bound, but a distance bound.** The TSP scheme needs few crossings per side. Here a square can be crossed by many paths, and what keeps the states few is the smoothness of the distance profiles, not a bound on crossings.
- **Rounding errors add up over levels.** Each level of the quadtree rounds the portal distances again. A fixed unit per level would lose $D$ times that unit per point, so the unit must shrink with the depth or be scaled to $\varepsilon/D$.
- **The perturbation needs care.** Unlike a tour, an optimal clustering can cost much less than the side of the bounding box, for example with two tight clusters far apart. The first step must bound $\mathrm{OPT}$ by a constant factor solution and handle distant groups separately.
- **Expected cost.** The bound holds on average over the shift. A high-probability bound needs several independent shifts, and a deterministic bound needs all $L^2$ of them.

## Implementations

## History

Arora, Raghavan and Rao presented the scheme at STOC 1998, two years after Arora's scheme for the Euclidean TSP. It gave the first $(1 + \varepsilon)$-approximation for $k$-median in the plane, a problem NP-hard by Megiddo and Supowit (1984), and a quasi-polynomial scheme in higher fixed dimension. Kolliopoulos and Rao (ESA 1999, SIAM Journal on Computing 2007) made the time nearly linear in $n$. Guruswami and Indyk (2003) showed that no such scheme exists in dimension $\Theta(\log n)$ unless P = NP.

## References
