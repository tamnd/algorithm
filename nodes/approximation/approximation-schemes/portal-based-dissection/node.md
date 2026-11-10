---
tag: 4X3G6D
kind: technique
slug: portal-based-dissection
name: Portal-based dissection (Arora's technique)
aliases:
- Arora portal technique
- quadtree portals
- randomly shifted dissection
- Arora's structure theorem
area: approximation/approximation-schemes
level: research
summary: Recursively dissect the plane by a randomly shifted quadtree and allow tours or solutions to cross only at O(1/ε) portal points per cell.
prereqs: [euclidean-tsp, quadtree, ptas, expected-value, shifting-technique]
see_also: [arora-euclidean-tsp-ptas, mitchell-euclidean-tsp-ptas, guillotine-cut-technique, arora-euclidean-k-median-ptas, euclidean-k-median, steiner-tree-problem, geometric-spanner, planar-steiner-tree-ptas]
sources:
  - paper: "S. Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998, pp. 753-782"
    title: Arora 1998
    locator: the perturbation, the shifted dissection, portals, the patching lemma and the structure theorem
  - paper: "S. Arora, Approximation schemes for NP-hard geometric optimization problems: a survey, Mathematical Programming 97(1-2), 2003, pp. 43-69"
    title: Arora 2003
    locator: the technique in general form and the list of problems it solves
  - paper: "S. B. Rao and W. D. Smith, Approximating geometric graphs via spanners and banyans, STOC 1998, pp. 540-550"
    title: Rao and Smith 1998
    locator: the O(n log n) scheme for fixed ε through spanners
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 10.1 (the Euclidean traveling salesman problem)
---

Portal-based dissection is the technique of Arora (1996, journal version 1998) that gave the first approximation schemes for the [Euclidean TSP](/euclidean-tsp/), the Euclidean Steiner tree problem and many other geometric problems. Enclose the input in a square, cut it recursively into four equal squares (a [quadtree](/quadtree/)), and move the whole dissection by a random shift. On each side of each square put a few evenly spaced points, the *portals*, and allow the solution to cross a side only at a portal. The *structure theorem* says that, for a random shift, some solution of this restricted form costs at most $(1 + \varepsilon)$ times the optimum in expectation. A restricted solution has few ways to enter and leave each square, so dynamic programming over the quadtree finds the best one. The random shift is what makes the loss small: a long line of the dissection, where the portals are far apart, is hit by few edges on average.

## In plain words

Lay a square grid of streets over the map, then cut it into four blocks, each block into four, and so on. Put a few gates on each block wall and allow the route to pass a wall only through a gate. Then the route inside one block depends only on which gates it uses, and a computer can fill in the blocks from the smallest to the largest.

A gate can be far from where the best route wants to cross, so we pay a detour. The big walls have the gates farthest apart. But if we drop the whole grid at a random offset, a route rarely crosses a big wall, because there are few big walls. On average, every crossing costs a small detour, and the total detour is a small part of the route.

## When it applies

- **A geometric objective.** The input is a set of points in the plane, or in $\mathbb{R}^d$ for fixed $d$, and the cost is the total Euclidean length of a network of segments, such as a tour, a tree or a set of connections to centres.
- **Cheap local changes.** A crossing of a line can be moved along the line at a cost of twice the distance, and many crossings of one segment can be merged into a few at a cost proportional to the length of the segment (the *patching lemma*). Tours, Steiner trees and assignments to centres have this property.
- **A small interface.** Inside a square, the best partial solution depends only on the portals used on its boundary and on how they connect inside. With $O(1/\varepsilon)$ crossings per side, there are few such interfaces.
- **A lower bound in terms of the input box.** The optimum is at least a constant times the side of the bounding box, or can be split into pieces where this holds. This allows snapping the points to a grid of size $O(n/\varepsilon)$.

## The template

The squares of depth $i$ have side $2L/2^i$, and a grid line has *level* $i$ if it is a side of squares of depth $i$ but of no larger square. Its portals are the points at gap $2L/(2^i m)$ along it, starting at the corner of the root square. With $m$ a power of 2, a portal of a large square is also a portal of each smaller square on the same line.

```pseudo id=template
DISSECT(P, ε)
L1  rescale P and move each point to the centre of a unit cell of an L × L grid, L a power of 2 with L = O(n/ε)
L2  pick the shift a, b uniformly from {0, ..., L − 1}
L3  the root square has side 2L and lower left corner (−a, −b); split each square with two or more points into four
L4  on each line of level i, put portals at gap 2L/(2^i m), with m a power of 2 and m = O(log L / ε)
L5  restrict to solutions that cross each side of each square only at portals, and at most r = O(1/ε) times
L6  for each square, from the leaves up, and each interface (the portals used and how they connect inside), store the cheapest restricted solution inside the square
L7  return the cheapest solution of the root, or the best over all L² shifts for a deterministic algorithm
```

Let $D = \log_2(2L)$ be the number of levels. Points sit at centres of unit cells, so no point lies on a grid line, and a segment between two points of the grid crosses each line it meets at one point.

**Lemma 1 (levels).** For a fixed vertical line $x = c$ with $1 \le c \le L - 1$ and a shift $a$ uniform in $\{0, \ldots, L - 1\}$, $\Pr[\text{the line has level } i] \le 2^{i-1}/L$ for $1 \le i \le D$. The same holds for horizontal lines and the shift $b$.

*Proof.* The line has level $i$ when $c + a$ is an odd multiple of $2L/2^i$, so in particular a multiple of $2L/2^i$. The value $c + a$ runs over $L$ consecutive integers. For $i \ge 2$, the step $2L/2^i$ divides $L$, so exactly $L/(2L/2^i) = 2^{i-1}$ of them are multiples of it. For $i = 1$, the step is $L$ and at most one of $L$ consecutive integers is a multiple of $L$, which is $2^{0}$. $\square$

**Lemma 2 (crossings).** A tour of length $T$ through grid points crosses the grid lines at most $\sqrt 2\, T$ times.

*Proof.* An edge with horizontal extent $\Delta_x$ and vertical extent $\Delta_y$ crosses exactly $\Delta_x$ vertical and $\Delta_y$ horizontal lines, since its ends are cell centres. Its length $s$ satisfies $\Delta_x + \Delta_y \le \sqrt 2\, s$. Sum over the edges. $\square$

**Theorem (the cost of portals).** Let $\pi$ be a tour of length $T$, and let $\pi'$ be the tour that walks, at each crossing of a line, along the line to the nearest portal and back. Over the random shift,
$$\mathbb{E}\,[\mathrm{len}(\pi') - T] \le \frac{\sqrt 2\, D}{m}\, T.$$
So with $m \ge 2\sqrt 2\, D/\varepsilon$, rounded up to a power of 2, the expected extra length is at most $\varepsilon T/2$.

*Proof.* A crossing of a line of level $i$ is at most half a gap from a portal, so the detour costs at most one gap, $2L/(2^i m)$. The level of a vertical line depends only on $a$, and the bound on the detour holds for every $b$. By Lemma 1 the expected detour of one crossing is at most
$$\sum_{i=1}^{D} \frac{2^{i-1}}{L} \cdot \frac{2L}{2^i m} = \frac{D}{m}.$$
By linearity of expectation and Lemma 2, the total is at most $(D/m) \cdot \sqrt 2\, T$. $\square$

**Structure theorem (Arora).** Over the random shift, the best tour that crosses each side of each square only at portals, and at most $r = O(1/\varepsilon)$ times, has expected length at most $(1 + \varepsilon)\,\mathrm{OPT}$.

*Proof sketch.* The theorem above handles the portals. For the bound on $r$, apply the patching lemma: if a tour crosses a segment $S$ of length $s$ more than twice, adding pieces of $S$ of total length $O(s)$ turns it into a tour that crosses $S$ at most twice. Process the squares from the smallest up. Each patch on a side of a square of depth $j$ removes at least $r - 1$ crossings of a line $\ell$, so the line has at most $t(\ell)/(r - 1)$ patches over all depths, where $t(\ell)$ is its number of crossings. Let $c_j$ be the number of patches at depth $j$. They cost $O(c_j \cdot 2L/2^j)$, and they happen only if the level of $\ell$ is at most $j$, which has probability at most $\sum_{i \le j} 2^{i-1}/L < 2^j/L$. So the expected cost on $\ell$ is $O(\sum_j c_j) = O(t(\ell)/r)$, and by Lemma 2 the total is $O(\mathrm{OPT}/r)$. The patches add crossings on the perpendicular lines at the corners of squares, and Arora's full proof handles them with a second patching at the corners. $\square$

**Perturbation and the dynamic program.** Let $L_0$ be the side of the bounding box. A tour must reach both sides of the box and come back, so $\mathrm{OPT} \ge 2L_0$. Snapping each point to a grid of gap $g = \varepsilon L_0/(8n)$ moves it less than $g$, so it changes every tour by less than $2ng = \varepsilon L_0/4 \le \varepsilon\,\mathrm{OPT}/8$, and after scaling by $1/g$ the grid side is $L = O(n/\varepsilon)$. The quadtree has at most $1 + 2nD$ squares: each split square holds at least two points, the split squares of one depth are disjoint, so there are at most $n/2$ of them per depth, and each has four children. Each square has at most $(m + 2)^{4r}$ choices of portals and $r^{O(r)}$ ways to pair them, so the dynamic program runs in $n (\log n)^{O(1/\varepsilon)}$ time.

## Classic examples

**A small trace.** Take $L = 8$, so $D = 4$, and the points $(0, 1)$, $(2, 6)$, $(5, 7)$, $(6, 2)$, which stand for the centres of these cells. The optimal tour visits them in the order given and has length $\sqrt{29} + \sqrt{10} + \sqrt{26} + \sqrt{37} \approx 19.73$. It crosses the grid lines $7 + 4 + 6 + 7 = 24$ times. With the shift $a = 3$, the root square is $[-3, 13)$, and the vertical lines $x = 1, \ldots, 7$ have the levels $2, 4, 3, 4, 1, 4, 3$: the line $x = 5$ is the middle line of the root. The first edge, from $(0.5, 1.5)$ to $(2.5, 6.5)$, crosses $x = 1$ at height $\frac{11}{4}$. The table gives the detour for the shift $(3, 5)$, its mean over all 64 shifts, and the bound $D \cdot 24/m$ of the theorem.

| $m$ | detour at shift $(3, 5)$ | mean over the shifts | bound |
|---|---|---|---|
| 1 | $574/15 \approx 38.27$ | $89/3 \approx 29.67$ | 96 |
| 2 | $14$ | $147/10 = 14.7$ | 48 |
| 4 | $107/15 \approx 7.13$ | $139/20 = 6.95$ | 24 |
| 8 | $62/15 \approx 4.13$ | $97/30 \approx 3.23$ | 12 |

The mean falls like $1/m$, as the theorem says. For $m = 1$ the detour at one shift is above the mean, so a fixed shift can be worse than the average.

**Euclidean TSP.** The [Arora scheme for Euclidean TSP](/arora-euclidean-tsp-ptas/) is the template applied to tours. Inside a square, the interface is the set of portals used and the pairing of these portals by the pieces of the tour inside the square. The time is $n (\log n)^{O(1/\varepsilon)}$ in the plane.

**Euclidean Steiner tree.** The same dissection works for the [Steiner tree problem](/steiner-tree-problem/) in the plane: the interface records which portals are connected inside the square. The patching lemma holds for trees as well.

**Euclidean $k$-median.** For [Euclidean $k$-median](/euclidean-k-median/), Arora, Raghavan and Rao send each point to its centre along a path that crosses squares at portals. The interface also records how many centres lie inside the square and the distances, rounded, from the portals to the nearest centre inside and outside. See the [ARR scheme](/arora-euclidean-k-median-ptas/).

**Higher dimensions.** In $\mathbb{R}^d$ the squares become cubes with $2^d$ children, the portals form a grid on each facet, and the time becomes $n (\log n)^{(O(\sqrt d/\varepsilon))^{d-1}}$ for fixed $d$.

## Variations

- **Portals only.** Arora's first version used only portals, each crossed at most twice. A square then has $3^{O(m)} = n^{O(1/\varepsilon)}$ interfaces, and the time is $n^{O(1/\varepsilon)}$. The bound $r$ on the crossings per side brings the time down to $n (\log n)^{O(1/\varepsilon)}$.
- **Spanners and banyans.** Rao and Smith first build a [geometric spanner](/geometric-spanner/), which bounds the length of the crossings in a better way, and reach $O(n \log n)$ time for fixed $\varepsilon$ and $d$.
- **Guillotine subdivisions.** [Mitchell's guillotine technique](/guillotine-cut-technique/) reaches the same results with a deterministic recursive cutting and no random shift. It gives the [Mitchell scheme for TSP](/mitchell-euclidean-tsp-ptas/).
- **Planar graphs.** Portals on the boundaries of pieces of a planar graph play the same role in the [PTAS for planar Steiner tree](/planar-steiner-tree-ptas/), with a brick decomposition in place of the quadtree.
- **Derandomization.** There are only $L^2 = O(n^2/\varepsilon^2)$ shifts, so trying all of them gives a deterministic algorithm at a factor $O(n^2/\varepsilon^2)$ in time.

## Pitfalls

- **A fixed shift.** Without the random shift, an adversary can put the optimal tour along the middle lines of the root, where the portals are farthest apart. The theorem is a statement about the average over the shifts.
- **Too few portals.** The detour of one crossing is $D/m$ on average, and there are $D = \Theta(\log(n/\varepsilon))$ levels. A constant number of portals per side is not enough; $m$ must grow like $\log n/\varepsilon$.
- **Portals that do not nest.** If $m$ is not a power of 2, the portals of a square need not be portals of its children, and a crossing at a portal of the parent is not at a portal of the child. Choose $m$ as a power of 2.
- **Points on lines.** A point on a grid line belongs to two squares, and edges from it touch the line without crossing it. Snapping the points to cell centres, or to odd coordinates, avoids this.
- **The perturbation needs a lower bound.** Snapping to a grid of gap $\varepsilon L_0/(8n)$ is cheap only because $\mathrm{OPT} \ge 2L_0$ for a tour. For problems where the optimum can be much smaller than the box, such as $k$-median with distant clusters, the instance must first be split or the grid chosen in another way.

## Exercises

1. In the trace, compute the levels of the horizontal lines $y = 1, \ldots, 7$ for the shift $b = 5$, and check that the line $y = 3$ is the middle line of the root.
2. Show that with $m$ a power of 2, every portal on a side of a square of depth $i$ is a portal of each square of depth $j > i$ whose side lies on the same line.
3. Prove that an optimal tour that crosses sides only at portals can be changed, at no extra cost, to cross each portal at most twice.
4. Prove Lemma 1 for a cube dissection in $\mathbb{R}^3$, and find the expected detour of a crossing of a plane when each facet has a $k \times k$ grid of portals.
5. Give an instance where the best shift and the worst shift differ by a constant factor in the detour, for $m = 2$.

## References
