---
tag: XYCABA
kind: concept
slug: beach-line
name: Beach line
aliases:
- wavefront
- parabolic front
area: geometry/voronoi-and-delaunay
level: advanced
summary: Sweep-line frontier of parabolic arcs, used by Fortune's algorithm to build the Voronoi diagram.
prereqs: [voronoi-diagram, sweep-line-technique]
see_also: [fortunes-algorithm, sweep-status-structure, event-queue, lower-envelope-of-segments, circumcircle, voronoi-diagram-construction, balanced-binary-search-tree]
sources:
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987
    locator: the whole paper (the sweep over a transformed Voronoi diagram, with site and circle events and an O(n log n) bound)
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 7.2 (the beach line, its breakpoints, site events and circle events, and the bound on the number of arcs)
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Tóth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 27, Voronoi diagrams and Delaunay triangulations, by S. Fortune (the sweep construction)
---

The beach line is the moving frontier of a sweep over a set of point sites in the plane. While a horizontal sweep line moves down, every site above it defines a parabola: the points that are as far from the site as from the sweep line. The beach line is the lower envelope of these parabolas. Above it, the nearest site of every point is already fixed and cannot change, so the part of the [Voronoi diagram](/voronoi-diagram/) above the beach line is final. The breakpoints between consecutive arcs move along the Voronoi edges, and [Fortune's algorithm](/fortunes-algorithm/) keeps the beach line as its sweep status.

## In plain words

Think of the sweep line as a wall that moves down over the page. A point above the wall is settled when some site above the wall is nearer to it than the wall is. No site below the wall can then be nearer, because such a site is farther than the wall.

For one site, the edge of its settled region is a bowl-shaped curve, a parabola. For many sites, it is a chain of bowl pieces, the beach line. Where two pieces meet, the point is equally far from two sites, so it is on a Voronoi edge. As the wall moves down, these meeting points slide along the Voronoi edges and draw them.

A new piece appears only when the wall reaches a new site. A piece disappears when its two neighbours squeeze it to a point, and that point is a Voronoi vertex.

## The idea

**Setting.** Let $P$ be a finite set of $n$ sites $p = (p_x, p_y)$ and let the sweep line be $y = \ell$. For a site with $p_y > \ell$, the points equidistant from $p$ and the line form the parabola

$$\beta_p(x) = \frac{(x - p_x)^2 + p_y^2 - \ell^2}{2 (p_y - \ell)},$$

which opens upward and has $p$ as its focus. A point $z$ above the sweep line is nearer to $p$ than to the line exactly when $z$ is above $\beta_p$. The beach line is $\beta(x) = \min_p \beta_p(x)$ over the sites above the line, a curve that meets every vertical line once.

**Why the part above is final.** Let $z$ be above the beach line, so some site $p$ above the sweep line has $|z - p| < z_y - \ell$. Every site $q$ below the sweep line has $|z - q| \ge z_y - q_y > z_y - \ell$. So the nearest site of $z$ is a site already passed, and later sites cannot change it.

**Breakpoints.** A breakpoint between the arc of $p$ and the arc of $q$ is at the same distance from $p$, $q$ and the sweep line, and no site is nearer. So it is a point of the Voronoi edge of $p$ and $q$. As $\ell$ decreases, each breakpoint moves along one Voronoi edge, and the edges are traced out.

**Events.** The beach line changes its sequence of arcs only at two kinds of events.

- **Site event.** When the sweep line reaches a site $s$, $\beta_s$ is a vertical ray up to the beach line, and it then opens into a narrow arc. It splits the arc above $s$ into two, so the sequence $\ldots a \ldots$ becomes $\ldots a\, s\, a \ldots$. Two new breakpoints start at the point of the old arc above $s$ and trace the same new Voronoi edge in two directions.
- **Circle event.** An arc of $q$ between arcs of $p$ and $r$ shrinks to a point when the sweep line reaches the lowest point of the circle through $p$, $q$ and $r$. At that moment the center of the circle is at the same distance from $p$, $q$, $r$ and the sweep line, so the circle is empty of sites, and the center is a Voronoi vertex. The arc of $q$ goes away, and one new breakpoint starts on the edge of $p$ and $r$.

An arc can appear only at a site event, never at a circle event. So the beach line has at most $2n - 1$ arcs: each site event adds two arcs, and the first site makes one. Another argument gives the same bound: two parabolas cross at most twice, so the sequence of sites along the beach line has no subsequence $a \ldots b \ldots a \ldots b$, a Davenport-Schinzel sequence of order 2, and such a sequence on $n$ symbols has length at most $2n - 1$.

**Data structure.** The arcs are stored in left-to-right order in a [balanced binary search tree](/balanced-binary-search-tree/), the [sweep status structure](/sweep-status-structure/). The keys are not stored: the position of a breakpoint is a function of $\ell$ and is computed when needed, which is enough for a search because the order of the arcs changes only at events. Each triple of consecutive arcs whose breakpoints move toward each other has a circle event in the [event queue](/event-queue/).

## Examples

**Two sites.** Let $p = (0, 10)$, $q = (2, 4)$ and the sweep line $y = 0$. Then $\beta_p(x) = (x^2 + 100)/20$ and $\beta_q(x) = ((x - 2)^2 + 16)/8$. They are equal when $3x^2 - 20x - 100 = 0$, at $x = -10/3$ and $x = 10$. The beach line has three arcs, of $p$, $q$ and $p$ from left to right, with breakpoints $(-10/3, 50/9)$ and $(10, 10)$. The point $(10, 10)$ is at distance $10$ from $p$, from $q$ and from the sweep line, so it is on the bisector of $p$ and $q$, the Voronoi edge of these two sites.

**A circle event.** Let the sites be $p = (0, 5)$, $q = (3, 4)$ and $r = (-4, 3)$, all on the circle of radius $5$ around the origin. The sweep meets them in this order. The site event of $q$ splits the arc of $p$, giving $p\, q\, p$. The site event of $r$ splits the left arc of $p$, giving $p\, r\, p\, q\, p$. The middle arc of $p$ lies between the arcs of $r$ and $q$, and $\mathrm{orient}(r, p, q) < 0$, so its two breakpoints move toward each other. Its circle event is at the lowest point $(0, -5)$ of the circle through $r$, $p$ and $q$. When the sweep line reaches $y = -5$, that arc vanishes, the beach line becomes $p\, r\, q\, p$, and the center $(0, 0)$ is the one Voronoi vertex, at distance $5$ from the three sites.

**Collinear sites.** For sites on one horizontal line, the first sweep position touches all of them at once, the arcs are vertical rays side by side, and all Voronoi edges are vertical lines. Implementations handle this top row before the sweep, as the code of [Fortune's algorithm](/fortunes-algorithm/) does.

## Where it is used

- [Fortune's algorithm](/fortunes-algorithm/) for the Voronoi diagram in $O(n \log n)$ time, and so for the [Delaunay triangulation](/delaunay-triangulation/) as its dual.
- Sweep algorithms for related diagrams: the Voronoi diagram of segments, the [additively weighted Voronoi diagram](/weighted-voronoi-diagram/) and the [power diagram](/power-diagram/), where the arcs are pieces of other conics.
- As a teaching example of a sweep whose status structure has keys that move continuously, unlike the [sweep line technique](/sweep-line-technique/) for segment intersection, where the order changes only at crossings.

## References
