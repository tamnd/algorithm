---
tag: XPPZ2J
kind: algorithm
slug: mitchell-guillotine-ptas
name: Mitchell guillotine PTAS for Euclidean TSP
aliases:
- Mitchell's PTAS
- guillotine subdivision PTAS
- m-guillotine approximation scheme
area: approximation/approximation-schemes
level: advanced
summary: Guillotine subdivision of the plane with dynamic programming over subregions, giving a (1+ε)-approximate tour.
solves: [euclidean-tsp]
model: real-ram
complexity:
  vars: {n: the number of points, m: "the guillotine parameter (the ratio is 1 + O(1/m))"}
  time: {worst: n^O(m)}
  space: {extra: n^O(m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1996
  people: [Joseph S. B. Mitchell]
  note: Mitchell used guillotine subdivisions for a constant ratio for the k-MST in 1996, and then the m-guillotine form gave a PTAS for the Euclidean TSP, the k-MST and related network problems; the journal paper appeared in 1999.
prereqs: [guillotine-cut-technique, ptas, euclidean-tsp, eulerian-circuit]
see_also: [mitchell-euclidean-tsp-ptas, guillotine-cut-technique, arora-euclidean-tsp-ptas, portal-based-dissection, euclidean-steiner-tree-problem, rectilinear-steiner-tree-problem, euclidean-minimum-spanning-tree, christofides-algorithm]
sources:
  - paper: doi:10.1137/S0097539796309764
    title: J. S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple polynomial-time approximation scheme for geometric TSP, k-MST, and related problems, SIAM Journal on Computing 28(4), 1999, pp. 1298-1309
    locator: the m-guillotine length theorem, the dynamic program over windows, and its use for the TSP, the k-MST and related problems
  - paper: "J. S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple new method for the geometric k-MST problem, Proceedings of the 7th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1996, pp. 402-408"
    title: Mitchell 1996
    locator: guillotine subdivisions and the constant ratio for the k-MST
  - paper: doi:10.1145/290179.290180
    title: S. Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998, pp. 753-782
    locator: Section 1, the comparison with Mitchell's method
---

Mitchell's guillotine scheme is a general way to get a deterministic [PTAS](/ptas/) for network problems in the plane: the [Euclidean TSP](/euclidean-tsp/), the $k$-MST (a shortest tree that connects $k$ of $n$ given points), [Steiner trees](/euclidean-steiner-tree-problem/) and related problems. It has two parts. The *structure theorem* of the [guillotine cut technique](/guillotine-cut-technique/) says that any network of length $L$ becomes *m-guillotine* when segments of length at most $\frac{\sqrt 2}{m} L$ are added on cut lines. The *dynamic program* finds the shortest m-guillotine network with the required property, since each side of each window is described by $O(m)$ numbers. With $m = \Theta(1/\varepsilon)$ the ratio is $1 + \varepsilon$ and the time is $n^{O(1/\varepsilon)}$. This page is about the scheme as a whole and the parts that are the same for every problem; the TSP case in detail, with its own example, is on [Mitchell's TSP scheme](/mitchell-euclidean-tsp-ptas/).

## In plain words

We want a short road network that does a job, for example a round trip through all the towns, or a tree that joins some of them.

Draw a box around the towns and cut it in two with a straight line, then cut each part again, until no town is inside a part. Where a cut crosses the roads, we keep a few crossings near each end and join all the others with one new road along the cut, the bridge. Then each cut is easy to describe.

A theorem says that, if the cuts are chosen well, the bridges are short. So the best network that follows this rule is almost as short as the best network. A table over all boxes, from small to large, finds that best network.

## The problem

The input is a set $P$ of $n$ points in the plane and an integer $m \ge 1$. A *network* is a finite set of straight segments. Each problem says which networks are feasible: a closed walk through all points for the TSP, a connected network that touches $k$ points for the $k$-MST, a connected network that touches all points for the Steiner tree. The goal is a feasible network whose length ALG is at most $\rho \cdot \mathrm{OPT}$, with $\rho = 1 + O(1/m)$.

The scheme applies when the problem has two properties. *Local check*: feasibility can be decided from what each window shows on its sides, and from a small pattern of how those pieces are joined inside. *Cheap repair*: adding the bridges to an optimal solution gives a network that is feasible or can be made feasible at a cost of $O(1)$ times the bridges. For a tour the repair doubles the bridges; for a Steiner tree, extra segments keep the network connected and do not need a repair.

## The algorithm

The windows are the rectangles with sides on the lines $x = x_i$ and $y = y_i$ through the points. Points are assumed to have distinct $x$ and distinct $y$ values; a small rotation gives this.

```pseudo id=main
GUILLOTINE-PTAS(P, m)
L1  list the windows: the rectangles whose sides lie on the lines through the points, from small to large
L2  the state of a window side: the parts at most m - 1 from each end, the two parts that end the bridge, and the joining pattern
L3  for each window W and each state, value(W, state) = the least, over cuts of W and agreeing states of the two parts, of their values plus the bridge on the cut
L4  at the bounding box, keep the states that give a feasible network: for the TSP, connected with even degrees once the bridges are doubled
L5  repair the best network into a solution: for the TSP, shortcut an Euler circuit
```

A *leaf* is a window with no point strictly inside; there the network consists of straight pieces that cross the window, fixed by the states of its sides. The bridge on a cut runs from the $m$-th part to the $m$-th part from the other end, where a part is a point at which the network meets the cut line.

**What the code covers.** The code runs the table of line L3 for one fixed network, such as an optimal tour or an optimal $k$-MST found by brute force, and finds its cut tree with the least total bridge length. It computes the side states of line L2 and counts them, and it does the repair of lines L4 and L5 for tours. It does not minimize over all networks, which is what the states are for. The full table is described in the proof file and is a sketch.

## Example

Take $A(0, 6)$, $B(3, 2)$, $C(4, 1)$, $D(1, 0)$, $E(2, 4)$ and $F(5, 5)$. The optimal tour is $A\,E\,D\,C\,B\,F$, of length 20.233. The bounding box is $[0, 5] \times [0, 6]$. With $m = 1$, the cuts of the box are:

| cut | parts | 1-span length |
|---|---|---|
| $x = 1$ | $y = 5$ on $AE$, $y = 5.8$ on $FA$ | 0.8 |
| $x = 2$ | $y = 1/3$ on $DC$, $E$ at $y = 4$, $y = 5.6$ on $FA$ | 5.267 |
| $x = 3$ | $y = 2/3$ on $DC$, $B$ at $y = 2$, $y = 5.4$ on $FA$ | 4.733 |
| $x = 4$ | $C$ at $y = 1$, $y = 3.5$ on $BF$, $y = 5.2$ on $FA$ | 4.2 |
| $y = 1$ | $x = 1.25$ on $ED$, $C$ at $x = 4$ | 2.75 |
| $y = 2$ | $x = 1.5$ on $ED$, $B$ at $x = 3$ | 1.5 |
| $y = 4$ | $E$ at $x = 2$, $x = 13/3$ on $BF$ | 2.333 |
| $y = 5$ | $x = 1$ on $AE$ | 0 |

Inside the box, the cut $y = 5$ meets the tour only on $AE$, since $F$ lies on the side of the box. So its span has length 0 and the cut is free. The table finds the best cut tree, with one bridge: in the window $[1, 5] \times [0, 5]$, the cut $x = 3$ meets $DC$ at $y = 2/3$ and $B$ at $y = 2$, and the bridge between them has length $4/3$. The table has 225 windows and 290 cuts. Doubling the bridge gives a graph of length $20.233 + 8/3 = 22.899$, and shortcutting its Euler circuit gives the tour $A\,E\,D\,B\,C\,F$ of length 20.416. With $m = 2$ the table finds a cut tree with bridges of total length 0, and the tour is returned as it is.

## Correctness

**Theorem.** Let $T^*$ be an optimal solution. If $T^*$ has an m-guillotine cut tree on the grid of the points with bridges of length $B \le \frac{\sqrt 2}{m}\,\mathrm{OPT}$, then for the TSP the scheme returns a tour of length at most $(1 + \frac{2\sqrt 2}{m})\,\mathrm{OPT}$.

The proof file has four steps.

1. **The table.** For a fixed network, line L3 finds the least bridge cost over all cut trees. This is proved in full by induction over the windows and checked against a search over all cut trees.
2. **Bridges stay apart.** Each bridge lies inside its window and ends on the network, so bridges never meet and later cuts do not spoil earlier ones. Proved in full.
3. **The repair.** Doubled bridges keep the degrees even and the graph connected, and shortcutting an Euler circuit does not increase the length. Proved in full.
4. **The length bound.** Mitchell's theorem gives an m-guillotine supergraph with added length at most $\frac{\sqrt 2}{m} L$. The [technique page](/guillotine-cut-technique/) proves it in full for axis-parallel segments with factor 1; the general form, and the fact that grid cuts are enough, are a sketch here. The tests check the bound for the least cut tree on random tours and $k$-MSTs.

The table over all networks then finds a feasible network at most as long as $T^*$ plus its doubled bridges; this step is a sketch.

## Complexity

- **Windows.** $\binom{n}{2}^2 = O(n^4)$, each with at most $2n - 4$ cuts.
- **States.** A part on a side is one edge or a point with two of its edges, so $O(n^3)$ choices, and a side keeps at most $2m$ parts. With the joining pattern there are $n^{O(m)}$ states per window.
- **Time and space.** $n^{O(m)}$ for the full table. With $m = \lceil 2\sqrt 2/\varepsilon \rceil$ the ratio for the TSP is $1 + \varepsilon$.
- **The code.** $O(n^6)$ for the table of one network: $O(n^4)$ windows, $O(n)$ cuts each, and $O(n)$ edges for each span.

## Properties

- **Deterministic.** No random shift, unlike [Arora's scheme](/arora-euclidean-tsp-ptas/) with [portals](/portal-based-dissection/).
- **One theorem for many problems.** The structure theorem does not depend on the problem; only the states and the repair do.
- **Not an EPTAS.** The exponent of $n$ grows with $m$, so the time is not $f(\varepsilon) \cdot n^{O(1)}$.
- **The plane.** The length theorem uses two dimensions.

## Variants and improvements

- **TSP.** States carry the joining pattern of the tour pieces, and the bridges are doubled. See [Mitchell's TSP scheme](/mitchell-euclidean-tsp-ptas/).
- **$k$-MST.** A natural state also carries how many points the network inside the window touches, a number up to $k$. Mitchell's first use of guillotine subdivisions, in 1996, gave a constant ratio for this problem.
- **Steiner trees.** For the [Euclidean](/euclidean-steiner-tree-problem/) and [rectilinear](/rectilinear-steiner-tree-problem/) Steiner tree, extra segments only help, so no repair is needed. The Steiner points are not input points, so the windows and the parts on their sides need a finer set of positions; see the source for the details.
- **Partitions into rectangles.** The rectilinear form with factor 1 bounds the best m-guillotine partition, as on the [technique page](/guillotine-cut-technique/).
- **Portals.** Arora's scheme has time $n (\log n)^{O(1/\varepsilon)}$ and extends to fixed dimension $d$.

## When to use it

Use the scheme to show that a new network problem in the plane has a PTAS: check the local check and the cheap repair, then design the states. For real instances use heuristics such as [Lin-Kernighan](/lin-kernighan/) for tours, or a constant-factor method such as [Christofides](/christofides-algorithm/), since $n^{O(1/\varepsilon)}$ is too slow even for small $\varepsilon$.

## Pitfalls

- **Parts, not edges.** A point of the network on the cut line is one part, even if two edges meet there.
- **The repair is problem specific.** Doubling is right for tours, but a repair that is not paid for by the bridges breaks the ratio.
- **States must be closed under cuts.** The states of the two parts must agree on the cut line, including the bridge on it, or the table can build networks that do not exist.
- **Grid cuts.** The length theorem chooses cuts by an averaging argument. A table that only tries cuts on the grid needs a separate argument that grid cuts are enough.
- **Constants.** The factor $\sqrt 2/m$ is for the bridges. The final ratio depends on the repair.

## Implementations

## History

Mitchell introduced guillotine subdivisions for approximation in 1996, for a constant ratio for the $k$-MST. The m-guillotine form then gave a PTAS for the TSP and related problems, found independently of [Arora's scheme](/arora-euclidean-tsp-ptas/); the journal paper appeared in SIAM Journal on Computing in 1999. Arora and Mitchell received the Gödel Prize in 2010 for these schemes.

## References
