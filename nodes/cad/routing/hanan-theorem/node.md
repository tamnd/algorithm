---
tag: 1GZ7DZ
kind: theorem
slug: hanan-theorem
name: Hanan's theorem
aliases:
- Hanan grid
area: cad/routing
level: core
summary: Some rectilinear Steiner minimal tree of a finite point set has all its Steiner points at crossings of the horizontal and vertical lines drawn through the points.
prereqs: [rectilinear-steiner-tree-problem]
see_also: [rectilinear-steiner-tree-problem, hwang-rectilinear-steiner-ratio, iterated-one-steiner, flute, steiner-tree-problem, rectilinear-minimum-spanning-tree, half-perimeter-wirelength, np-complete]
sources:
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the theorem that a minimal tree can be found on the grid of lines through the given points, and the exact solutions for small numbers of points
  - paper: doi:10.1137/0132071
    title: M. R. Garey and D. S. Johnson, The rectilinear Steiner tree problem is NP-complete, SIAM Journal on Applied Mathematics 32(4), 1977
    locator: the NP-completeness of the decision problem
  - paper: "Frank K. Hwang, Dana S. Richards and Pawel Winter, The Steiner Tree Problem, Annals of Discrete Mathematics 53, North-Holland, 1992"
    locator: Part III, the rectilinear Steiner problem (general locator)
---

Hanan's theorem says that a shortest network of horizontal and vertical wires that joins a finite set of points can always be found on the grid of lines through the points. For a set $P$ of points, draw a vertical line through every point and a horizontal line through every point. The crossings of these lines form the *Hanan grid*, which has at most $n^2$ points for $n$ points of $P$. M. Hanan proved in 1966 that some rectilinear Steiner minimal tree of $P$ has all its Steiner points, and in fact all its bends, at these crossings, and runs only along these lines. This turns the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/), which allows Steiner points anywhere in the plane, into a [Steiner tree problem](/steiner-tree-problem/) on a finite graph. In electronic design automation (EDA) it is the reason why Steiner tree methods such as [iterated 1-Steiner](/iterated-one-steiner/) and [FLUTE](/flute/) only consider grid points.

## Statement

Let $P$ be a finite set of $n \ge 1$ points in the plane, with the set $X$ of their $x$ coordinates and the set $Y$ of their $y$ coordinates. A *rectilinear Steiner tree* of $P$ is a finite union of horizontal and vertical segments that is connected and contains $P$. Its length is the total length of the segments. The *grid graph* $\Gamma(P)$ has the vertex set $X \times Y$, and an edge between two vertices that are next to each other on a horizontal or a vertical line, with its L1 length.

**Theorem (Hanan 1966).** For every rectilinear Steiner tree $T$ of $P$ there is a tree in $\Gamma(P)$ that contains $P$ and is no longer than $T$. Hence a rectilinear Steiner minimal tree of $P$ exists, and some rectilinear Steiner minimal tree is a subtree of $\Gamma(P)$: all its Steiner points and bends are in $X \times Y$ and all its segments lie on the lines $x = a$ for $a \in X$ and $y = b$ for $b \in Y$.

The theorem says "some", not "every". Other optimal trees off the grid can exist, as the section on tightness shows.

## In plain words

You must join some pins with wire that runs only left, right, up and down. You may add branch points anywhere. Where should they go?

Hanan's answer: draw a vertical line and a horizontal line through every pin. You never need a branch point or a bend that is not on a crossing of these lines.

The reason is a sliding argument. Take a vertical piece of wire that is not on one of the lines. Push it a little to the left or to the right. The horizontal wires that end on it get longer on one side and shorter on the other. Push it toward the side with more of them, and the total does not grow. Keep pushing until it lands on another vertical piece, which brings it closer to the lines. Do the same for the horizontal pieces.

## Proof

*Step 0: a tree as a graph.* Split the segments of $T$ at every endpoint, bend, crossing and point of $P$. This gives a finite connected graph $G$ drawn in the plane, whose edges are horizontal or vertical segments, and whose total edge length is the length of $T$. A spanning tree of $G$ still connects $P$ and is no longer. From now on we work with an abstract tree $G$ and a position $\mathrm{pos}(u)$ for each vertex $u$, with three invariants:

1. every edge joins two vertices with the same $x$ or the same $y$, so it is horizontal or vertical;
2. the vertices that are points of $P$ keep their positions;
3. the *length* $\ell(G) = \sum_{uv} \mathrm{dist}(\mathrm{pos}(u), \mathrm{pos}(v))$ over the edges never grows.

Edges may overlap in the plane. The drawn union of the edges is connected, contains $P$ and has length at most $\ell(G)$.

*Step 1: one slide.* Let $c \notin X$ be the $x$ coordinate of some vertex. Let $U$ be the set of vertices with $x = c$. None of them is a point of $P$. Let $A$ be the number of horizontal edges with one end in $U$ and the other end at $x < c$, and $B$ the number with the other end at $x > c$. Every other edge at a vertex of $U$ has both ends in $U$, since it joins two points with $x = c$, and a move of all of $U$ keeps its length. Because $G$ is connected and contains a point of $P$, which is not in $U$, we have $A + B \ge 1$.

Move every vertex of $U$ to $x = c + \delta$ and keep its $y$. The edges inside $U$ keep their length, the $A$ edges to the left change by $+\delta$ and the $B$ edges to the right change by $-\delta$, as long as no vertex is passed. So $\ell(G)$ changes by $(A - B)\,\delta$. If $A \le B$, then $B \ge 1$, and we take $\delta > 0$ up to the nearest $x$ coordinate $c' > c$ of a vertex outside $U$, which exists because the $B$ edges have their other ends there. If $A > B$, we take $\delta < 0$ up to the nearest $c' < c$ of a vertex outside $U$, which exists because $A \ge 1$. In both cases $(A - B)\,\delta \le 0$, and no edge reaches negative length on the way, since no vertex outside $U$ has its $x$ strictly between $c$ and $c'$. All three invariants hold. After the move, the set of $x$ coordinates of the vertices has lost $c$ and gained nothing.

*Step 2: all slides.* Repeat Step 1 while some vertex has an $x$ coordinate not in $X$. Each slide removes one value from the finite set of $x$ coordinates of vertices and adds none, so after finitely many slides every vertex has $x \in X$. Now do the same with the roles of $x$ and $y$ exchanged. A vertical slide changes only $y$ coordinates, so the $x$ coordinates stay in $X$. At the end every vertex is in $X \times Y$.

*Step 3: back to the grid.* Each edge now joins two points of $X \times Y$ on the same horizontal or vertical line, so it is a path of grid edges of $\Gamma(P)$ with the same length. The union $H$ of these grid paths is a connected subgraph of $\Gamma(P)$ that contains $P$, and its length is at most $\ell(G) \le |T|$, with equality when no two paths share a grid edge. A spanning tree of $H$ is a tree in $\Gamma(P)$ that contains $P$ and is no longer than $T$.

*Step 4: existence and the conclusion.* $\Gamma(P)$ is finite, so among its trees that contain $P$ there is a shortest one, $T^*$. Every grid tree is a rectilinear Steiner tree, and by Step 3 every rectilinear Steiner tree is at least as long as some grid tree, so at least as long as $T^*$. Hence $T^*$ is a rectilinear Steiner minimal tree, and all its vertices, Steiner points and bends included, are in $X \times Y$. $\square$

*Example.* Take $P = \{(0, 0), (0, 4), (3, 2)\}$ and the tree with a trunk on $x = 1$ from $(1, 0)$ to $(1, 4)$ and the arms $(0, 0)$ to $(1, 0)$, $(0, 4)$ to $(1, 4)$ and $(1, 2)$ to $(3, 2)$. Its length is $4 + 1 + 1 + 2 = 8$, and $1 \notin X = \{0, 3\}$. On the line $x = 1$ there are $A = 2$ arms to the left and $B = 1$ to the right, so the slide goes left with change $(2 - 1)\delta$ for $\delta < 0$. At $x = 0$ the trunk meets the pins, and the length is $8 - 1 = 7$. This is the half perimeter $3 + 4$ of the bounding box, which no tree can beat, so the grid tree is optimal.

## Consequences

- **A finite problem.** The rectilinear Steiner tree problem is the Steiner tree problem in the graph $\Gamma(P)$ with at most $n^2$ vertices. Exact methods search this graph, and the brute force of trying every set of at most $n - 2$ grid points with a [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) on each is correct.
- **In NP.** The decision form, "is there a tree of length at most $L$", has a certificate of polynomial size: a subtree of $\Gamma(P)$. Garey and Johnson (1977) showed that it is NP-complete.
- **Candidate points.** Heuristics need only try the at most $n^2$ grid points as Steiner points, as in [iterated 1-Steiner](/iterated-one-steiner/).
- **Lengths are linear in the gaps.** The length of a grid tree is a sum of gaps between neighboring $x$ values and neighboring $y$ values, with integer coefficients. For a fixed order of the points in $x$ and in $y$, the optimum is the least of finitely many such linear forms. [FLUTE](/flute/) stores these forms in tables.
- **Three points.** For $n \le 3$ the optimum is the [half-perimeter wirelength](/half-perimeter-wirelength/) of the bounding box, reached by a star from the grid point with the median $x$ and the median $y$.

## Tightness

- **Not every optimal tree is on the grid.** For the four corners $(0, 0)$, $(3, 0)$, $(0, 4)$ and $(3, 4)$ of a 3 by 4 rectangle, the two horizontal sides and one vertical bridge between them give length $3 + 3 + 4 = 10$, which is optimal. The bridge can be at any $x$ in $[0, 3]$, for example at $x = 1$, where its two Steiner points $(1, 0)$ and $(1, 4)$ are not on the grid. Here $A = B = 1$ on the line of the bridge, and the slide keeps the length the same.
- **Steiner points that are not pins are needed.** For the plus shape $(1, 0)$, $(0, 1)$, $(2, 1)$, $(1, 2)$, the optimum 4 uses the grid point $(1, 1)$, which is not one of the points. Every tree with no Steiner points has length at least 6.
- **The grid does not shrink in general.** The theorem gives a set of $n^2$ candidates, and a minimal tree uses at most $n - 2$ of them, but which ones depends on the gaps between the coordinates, as the example on the [FLUTE](/flute/) page shows for one order of four points.
- **Other metrics.** In the Euclidean plane the Steiner points of a minimal tree are at 120 degree junctions and are not on any fixed finite grid, so the theorem has no direct Euclidean form.

## History

M. Hanan studied the Steiner problem with rectilinear distance in 1966 and proved that a minimal tree can be found on the grid of lines through the given points. He also gave exact solutions for small numbers of points. F. K. Hwang studied the shape of full rectilinear Steiner trees in 1976 and proved the bound 3/2 on the ratio of the minimum spanning tree to the minimal tree, see [Hwang's theorem](/hwang-rectilinear-steiner-ratio/). Garey and Johnson showed in 1977 that the problem is NP-complete, and the grid shows that its decision form is in NP. The grid is now the standard search space of rectilinear Steiner tree methods in VLSI routing.

## References
