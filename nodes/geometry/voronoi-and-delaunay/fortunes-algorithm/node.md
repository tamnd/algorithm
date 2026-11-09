---
tag: A89AWB
kind: algorithm
slug: fortunes-algorithm
name: Fortune's algorithm
aliases:
- Fortune's sweep line algorithm
- sweepline Voronoi algorithm
- Fortune's sweep
area: geometry/voronoi-and-delaunay
level: advanced
summary: Sweep-line algorithm constructing the Voronoi diagram in O(n log n) time.
solves: [voronoi-diagram-construction]
model: real-ram
complexity:
  vars: {n: the number of sites}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Steven Fortune]
  note: Fortune presented the sweep at the Symposium on Computational Geometry in 1986 and published it in Algorithmica in 1987.
prereqs: [voronoi-diagram, beach-line, sweep-line-technique, priority-queue, balanced-binary-search-tree]
see_also: [voronoi-complexity-theorem, voronoi-construction-lower-bound, guibas-stolfi-algorithm, bowyer-watson-algorithm, voronoi-delaunay-duality, bentley-ottmann-algorithm, weighted-voronoi-diagram, circumcenter]
sources:
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987
    locator: the whole paper (the sweep over a transformed diagram, site and circle events, the O(n log n) time and O(n) space bounds, and the extension to weighted points and segments)
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 7.2 (the beach-line form of the sweep, its event handling and its O(n log n) analysis)
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Tóth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 27, Voronoi diagrams and Delaunay triangulations, by S. Fortune (the sweep construction)
---

Fortune's algorithm builds the [Voronoi diagram](/voronoi-diagram/) of $n$ point sites in the plane in $O(n \log n)$ worst-case time and $O(n)$ space. A horizontal line sweeps down over the plane. Above it, the part of the diagram that no lower site can change is bounded by the [beach line](/beach-line/), a chain of parabolic arcs. The breakpoints between neighbouring arcs trace the Voronoi edges. The beach line changes only at two kinds of events: a *site event*, when the sweep line reaches a site and a new arc appears, and a *circle event*, when an arc shrinks to a point, which is a Voronoi vertex.

## In plain words

A wall moves down over the page. Every site above the wall claims the points that are nearer to it than to the wall. The edge of all the claimed land is a chain of bowl-shaped pieces, one piece or more for each site. Where two pieces meet, the point is equally far from two sites, so it is on a border between their regions.

When the wall reaches a new site, a thin new piece starts at that site and grows. When two pieces squeeze the piece between them to a point, three regions meet there, and the algorithm records a corner of the diagram.

The algorithm keeps the pieces in order and keeps a list of the next places where something happens. It moves from one such place to the next and never goes back.

## The problem

The input is a finite list $P$ of sites $p = (x, y)$ with integer coordinates; repeats are allowed. The output is the Voronoi diagram of the distinct sites: the list of Voronoi vertices, as exact rational points, and for each pair of sites whose cells share an edge of positive length, the two ends of that edge, where an end can be at infinity.

Notation: $n$ is the number of distinct sites and $h$ the number of vertices of their convex hull. The sweep line is $y = \ell$ and moves down. For a site $p$ above it, $\beta_p(x) = ((x - p_x)^2 + p_y^2 - \ell^2) / (2 (p_y - \ell))$ is its parabola, and the beach line is the lower envelope of these parabolas, as on the [beach-line page](/beach-line/). $\mathrm{orient}(a, b, c)$ is the sign of $(b - a) \times (c - a)$: positive for a counterclockwise turn, negative for a clockwise turn, zero on a line. For counterclockwise $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside their circle; the sweep does not call it, because the circle events do its work.

General position: the proof assumes no two sites with the same $y$, no four sites on one circle, and distinct event heights. The code also accepts sites on one row, cocircular sites and equal event heights; these cases are checked against a brute-force diagram but are not covered by the proof.

## The algorithm

```pseudo id=main
FORTUNE(P)
L1  S ← the distinct sites of P sorted by (-y, x)
L2  Q ← a priority queue with a site event for each site but the first, highest first
    the beach line ← one arc of the first site
L3  while Q is not empty do
        pop the highest event e from Q; skip it if it is marked invalid
L4      if e is a site event for site s then
L5          find the arc of the beach line above s, say of site p
L6          mark the circle event of that arc invalid
L7          replace the arc by three arcs p, s, p, and start two traces at the point above s
L8          check the two new triples whose middle arc is p, and push their circle events
L9      else e is a circle event of the arc b between arcs a and c
L10         record the center v of the circle as a vertex, and end the traces of a|b and b|c at v
L11         start a trace for the new breakpoint a|c at v
L12         remove b, and mark the circle events of a and c invalid
L13         check the new triples whose middle arc is a or c, and push their circle events
L14 join the twin traces and return the vertices and the edges
```

- **Line L1.** The order is the order of the sweep: higher sites first, and on one row from left to right.
- **Line L2.** The queue is a [priority queue](/priority-queue/), for example a [binary heap](/binary-heap/). A site event has height $s_y$; a circle event has the height $v_y - r$ of the lowest point of its circle, with center $v$ and radius $r$. The code compares the heights $v_y - r$ exactly: $v_y$ and $r^2$ are rational, and the sign of $u + r'^{1/2} - r^{1/2}$ is found by squaring with sign checks.
- **Line L5.** The arcs are kept in left-to-right order in a [balanced binary search tree](/balanced-binary-search-tree/), such as a [red-black tree](/red-black-tree/), keyed by the breakpoints. The search compares $s_x$ with the breakpoint of two neighbouring arcs at height $s_y$. That breakpoint is a root of a quadratic with integer coefficients, so the comparison is an exact sign test. The code on this page walks a linked list instead.
- **Line L6.** The arc of $p$ is split, so the triple that had it in the middle is gone. Its circle event is a *false alarm*; it stays in the queue, marked, and is skipped when popped.
- **Line L7.** The new arc of $s$ has width zero at first. Both new breakpoints start at the point of the beach line above $s$, which is on the Voronoi edge of $p$ and $s$. They move apart, so the edge is traced from that point in two directions by two *twin* traces.
- **Lines L8 and L13.** A triple of consecutive arcs $a, b, c$ gets a circle event only when $a$ and $c$ are arcs of different sites and $\mathrm{orient}(a, b, c) < 0$, that is, when the sites turn clockwise from left to right. Only then do the two breakpoints of $b$ move toward each other.
- **Line L10.** The center of the circle through three sites is computed exactly with rationals, as on the [circumcenter page](/circumcenter/).
- **Line L14.** Each Voronoi edge is the union of the traces of its pair of sites. Twin traces start at one point and give the two ends; a trace that starts at a vertex gives that vertex and its own end. An end that is never closed is at infinity.

## Example

Take the six sites $(2,8)$, $(6,7)$, $(0,4)$, $(4,5)$, $(8,3)$ and $(3,0)$. The beach line is written as the list of the sites of its arcs, from left to right.

1. Start: $(2,8)$ is the highest site, and the beach line is its one arc.
2. Site $(6,7)$ falls under the arc of $(2,8)$. The beach line is $(2,8), (6,7), (2,8)$. The only triple has the same site at both ends and gets no event.
3. Site $(4,5)$ falls under the arc of $(6,7)$: $(2,8), (6,7), (4,5), (6,7), (2,8)$. The triple $(2,8), (6,7), (4,5)$ turns clockwise, so its circle event is pushed: center $(39/10, 71/10)$, $r^2 = 221/50$, height about $4.998$. The triple $(4,5), (6,7), (2,8)$ turns counterclockwise and gets no event.
4. Circle event at about $4.998$: the vertex $(39/10, 71/10)$ is recorded and the left arc of $(6,7)$ is removed: $(2,8), (4,5), (6,7), (2,8)$. A trace of the pair $(2,8), (4,5)$ starts at the vertex.
5. Site $(0,4)$ falls under the leftmost arc: $(2,8), (0,4), (2,8), (4,5), (6,7), (2,8)$. The triple $(0,4), (2,8), (4,5)$ gets the event with center $(12/7, 79/14)$, $r^2 = 1105/196$, height about $3.268$.
6. Circle event at about $3.268$: vertex $(12/7, 79/14)$, and the beach line is $(2,8), (0,4), (4,5), (6,7), (2,8)$. No new triple turns clockwise.
7. Site $(8,3)$ falls under the arc of $(6,7)$: $(2,8), (0,4), (4,5), (6,7), (8,3), (6,7), (2,8)$. The triple $(4,5), (6,7), (8,3)$ gets the event with center $(19/3, 14/3)$, $r^2 = 50/9$, height about $2.310$.
8. Circle event at about $2.310$: vertex $(19/3, 14/3)$, and the beach line is $(2,8), (0,4), (4,5), (8,3), (6,7), (2,8)$. The new triple $(0,4), (4,5), (8,3)$ turns clockwise, so it gets an event at height about $-7.36$.
9. Site $(3,0)$ falls under the arc of $(4,5)$, so the event at $-7.36$ becomes a false alarm. The beach line is $(2,8), (0,4), (4,5), (3,0), (4,5), (8,3), (6,7), (2,8)$. Two events are pushed: $(0,4), (4,5), (3,0)$ with center $(93/38, 103/38)$ at height about $-0.056$, and $(3,0), (4,5), (8,3)$ with center $(56/11, 24/11)$ at height about $-0.840$.
10. The two circle events record the vertices $(93/38, 103/38)$ and $(56/11, 24/11)$. The beach line ends as $(2,8), (0,4), (3,0), (8,3), (6,7), (2,8)$, with no clockwise triple, and the false alarm is skipped.

The output has $5$ vertices and $10$ edges. The hull has $h = 5$ vertices and $(4,5)$ is inside it, so the [Voronoi complexity theorem](/voronoi-complexity-theorem/) gives $2n - 2 - h = 5$ vertices and $3n - 3 - h = 10$ edges, as found. The $5$ unbounded edges belong to the hull pairs, for example the edge of $(2,8)$ and $(6,7)$, which runs from $(39/10, 71/10)$ to infinity.

## Correctness

**Theorem.** If no two sites have the same $y$, no four sites lie on one circle, and the event heights are pairwise distinct, then FORTUNE terminates, returns exactly the Voronoi vertices, and returns each Voronoi edge of positive length once with its two ends.

The proof rests on one fact about the beach line: a point on it is the center of a disc that touches the sweep line and holds no site, so the breakpoints lie on Voronoi edges and above the beach line the diagram is final. Between two events the order of the arcs does not change, because a change needs three sites on one empty circle with its lowest point on the sweep line, and that is a circle event. A clockwise triple of consecutive arcs has its circle bottom below the sweep line, and if it stays consecutive until then, its circle is empty and its middle arc vanishes at the circle center, which is a Voronoi vertex. Every Voronoi vertex is found, because just above the bottom of its empty circle its three sites are consecutive arcs in clockwise order. The full proof, with the trace argument for the edges, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Worst case.** At most $2n - 1$ arcs exist at one time, at most $2n - 5$ circle events are processed for $n \ge 3$, and fewer than $7n$ events are pushed. With a binary heap and a balanced search tree, each event costs $O(\log n)$, so the time is $O(n \log n)$ in the worst case and the space is $O(n)$. This is proved in [the complexity proof](proofs/complexity/).
- **Lower bound.** In the algebraic decision tree model, building the Voronoi diagram needs $\Omega(n \log n)$ time, so the sweep is optimal; see the [lower bound](/voronoi-construction-lower-bound/).
- **This code.** The code walks a linked list in line L5, which costs $O(n)$ per site, so its worst case is $O(n^2)$ time. All other steps meet the bounds above.

## Properties

- **Exact.** All predicates are signs of integer or rational expressions; event heights with square roots are compared exactly.
- **Deterministic.** No random choices; ties in the queue are broken by $x$ and then by the kind of event.
- **Linear size.** The diagram has $O(n)$ size by [Euler's formula](/euler-formula/), and the beach line and the queue are also $O(n)$.
- **Not online.** All sites must be known before the sweep starts.

## Variants and improvements

- **Fortune's transformation.** Fortune's paper sweeps a transformed diagram, where a point $q$ is moved up by its distance to the nearest site. The beach-line form of textbooks such as de Berg et al. is the same algorithm described in the untransformed plane.
- **Weighted sites and segments.** Fortune's paper extends the sweep to [additively weighted sites](/weighted-voronoi-diagram/) and to line segments, with the same $O(n \log n)$ bound.
- **Delaunay output.** Each circle event gives a Delaunay triangle $a, b, c$, so the same sweep builds the [Delaunay triangulation](/delaunay-triangulation/) by [duality](/voronoi-delaunay-duality/).
- **Bounding box.** Many programs clip the unbounded edges to a box at the end; this code keeps ends at infinity.

## When to use it

Use it to compute the Voronoi diagram directly, with its edges, in deterministic $O(n \log n)$ time. To get the Delaunay triangulation, an incremental method such as [Bowyer-Watson](/bowyer-watson-algorithm/) or divide and conquer by the [Guibas-Stolfi algorithm](/guibas-stolfi-algorithm/) is often simpler to make robust. Fortune's sweep needs the beach-line search tree, the breakpoint formula and the false alarms right; a quadratic list walk, as in this code, is fine for small inputs.

## Pitfalls

- **Pushing events for counterclockwise triples in lines L8 and L13.** Then the breakpoints move apart and the circle event is wrong. Push only when $\mathrm{orient}(a, b, c) < 0$ and $a$, $c$ are different sites.
- **Forgetting false alarms in lines L6 and L12.** An event whose triple was broken must be skipped when popped, or a wrong vertex is recorded.
- **Floating breakpoints in line L5.** A rounded breakpoint can send a new site into the wrong arc when it falls near a breakpoint. Compare $s_x$ with the root of the quadratic exactly.
- **Rounded event heights in line L2.** The height $v_y - r$ has a square root. Two events at nearly the same height can be popped in the wrong order unless the comparison is exact.
- **Sites on the top row in line L2.** With several highest sites at one $y$, the first arc of each is not under any other arc. Start the beach line with all of them, side by side, separated by vertical edges from infinity.
- **Cocircular sites in line L14.** Four or more sites on one empty circle give several circle events at one point and edges of length zero. Record the vertex once and drop the zero-length edges.

## Implementations

## History

Steven Fortune presented the sweep at the second Symposium on Computational Geometry in 1986, and the journal version appeared in Algorithmica in 1987, in the same volume as Dwyer's algorithm. Before it, the $O(n \log n)$ algorithms for the Voronoi diagram were divide and conquer, by Shamos and Hoey in 1975 and by Lee and Schachter and Guibas and Stolfi for the Delaunay dual. A plane sweep looked hard, because a site below the sweep line can own points above it. Fortune solved this by sweeping a transformed diagram in which every region starts at its own site. Later textbooks describe the same sweep with the beach line of parabolas.

## References
