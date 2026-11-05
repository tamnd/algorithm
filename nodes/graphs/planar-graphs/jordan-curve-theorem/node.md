---
tag: 4EZFJ8
kind: theorem
slug: jordan-curve-theorem
name: Jordan curve theorem
area: graphs/planar-graphs
level: intro
summary: A simple closed curve in the plane separates it into exactly two regions.
prereqs: [planar-graph]
see_also: [euler-formula, planar-face, point-in-polygon, kuratowski-theorem, graph-genus, simple-polygon, planar-embedding]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.1, Topological prerequisites (the theorem for polygons with proof, and the statement for general curves)
  - book: "Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001"
    locator: Chapter 2, Planar graphs (Section 2.1, the Jordan curve theorem, with a full proof)
  - paper: "Carsten Thomassen, The Jordan-Schönflies theorem and the classification of surfaces, American Mathematical Monthly 99(2), 116 to 130 (1992)"
    locator: the graph-theoretic proof of the Jordan curve theorem from the non-planarity of K3,3
  - paper: "Thomas C. Hales, The Jordan curve theorem, formally and informally, American Mathematical Monthly 114(10), 882 to 894 (2007)"
    locator: the history of the proofs and the computer-checked proof
---

The Jordan curve theorem says that a simple closed curve $C$ in the plane splits the rest of the plane into exactly two connected regions, a bounded inside and an unbounded outside, and that $C$ is the boundary of each. It looks obvious, but a curve can be very wild, and a full proof takes real work. For graph algorithms it is the fact behind [faces](/planar-face/), [Euler's formula](/euler-formula/), the non-planarity of $K_5$ and $K_{3,3}$, and the [point in polygon](/point-in-polygon/) test. This page proves the case of polygons, which is the case that drawings with straight or polygonal edges need, and gives the locator of a proof for general curves.

## Statement

A **simple closed curve** (a Jordan curve) is a set $C \subset \mathbb{R}^2$ that is the image of a continuous one-to-one map from the circle $S^1$. A **simple arc** is the image of a continuous one-to-one map from $[0, 1]$. A **region** of an open set is one of its connected components (for open sets of the plane, connected and path-connected agree).

**Theorem (Jordan).** If $C$ is a simple closed curve in $\mathbb{R}^2$, then $\mathbb{R}^2 \setminus C$ has exactly two regions. One is bounded (the inside) and one is unbounded (the outside), and every point of $C$ lies in the closure of both.

**Companion fact (arcs).** If $A$ is a simple arc in $\mathbb{R}^2$, then $\mathbb{R}^2 \setminus A$ is connected.

In graph terms, a drawing of a graph is given by points for the vertices and curves for the edges (coordinates, or polygonal curves). A cycle of the graph is drawn as a simple closed curve, so it has an inside and an outside. A tree is drawn as a finite union of arcs that contains no closed curve, and its complement is connected.

## In plain words

Draw a closed loop on paper that never touches itself. The loop cuts the paper into two parts: the part inside the loop and the part outside. You cannot walk from a point inside to a point outside without stepping on the loop. And from every point of the loop you can step into either part.

A loop that is made of straight pieces gives a quick test. From your point, draw a straight line in some direction and count how many times it crosses the loop. An odd count means you are inside, and an even count means you are outside.

## Proof

We prove the theorem for a **polygon**, a simple closed curve $P$ that is the union of finitely many segments. This is the case of graph drawings with straight-line or polygonal edges, which by [Fáry's theorem](/fary-theorem/) is all a simple planar graph needs. The proof follows Diestel, Section 4.1.

**At most two regions.** Let $\varepsilon > 0$ be smaller than half the least distance between two segments of $P$ that do not share an end, and smaller than half the length of each segment. The points at distance less than $\varepsilon$ from $P$, minus $P$ itself, form two thin strips, one on each side of $P$: when you walk along $P$, you can keep a point on your left (or on your right) at distance about $\varepsilon/2$, and at each corner the side is well defined. Each strip is path-connected, because you can move a point along it all the way around $P$. Now let $x$ be any point not on $P$. Move from $x$ along a straight segment toward the nearest point of $P$. Just before you reach $P$ you are in one of the two strips, and the segment before that point does not meet $P$. So every point of $\mathbb{R}^2 \setminus P$ can be joined to one of two path-connected sets, and $\mathbb{R}^2 \setminus P$ has at most two regions. Also every point of $P$ is in the closure of both strips, so it is in the closure of each region that exists.

**At least two regions.** Fix a direction $d$ that is parallel to no segment of $P$. For a point $x \notin P$, let $\pi(x)$ be the parity of the number of times the ray from $x$ in direction $d$ crosses $P$, where the ray passes through a vertex $v$ of $P$ counts as a crossing exactly when the two segments at $v$ lie on different sides of the ray (and as no crossing when they lie on the same side). This rule gives the same parity as a slight turn of the ray that avoids $v$. The function $\pi$ is constant along a segment that does not meet $P$: as $x$ moves, the number of crossings changes only when the ray sweeps over a vertex of $P$, and there the count changes by 0 or 2 by the rule. So $\pi$ is constant on each region. Take a point $y$ on the interior of a segment $s$ of $P$, and two points $x_1, x_2$ very close to $y$ on the two sides of $s$, on a line parallel to $d$. Their rays agree except that one of them crosses $s$ and the other does not, so $\pi(x_1) \ne \pi(x_2)$. Hence $x_1$ and $x_2$ are in different regions, and there are at least two.

**Bounded and unbounded.** A point far from $P$ has a ray in direction $d$ that misses $P$, so $\pi = 0$ there. The points with $\pi = 0$ form the unbounded region, and the points with $\pi = 1$ form a bounded region, since they lie in a disk that contains $P$. $\square$

**The companion fact for polygonal arcs** follows in the same way: the points near a polygonal arc that are not on it form only one strip, since you can go around the end of the arc, so the complement is connected.

**General curves.** For an arbitrary simple closed curve the "at least two" part is the hard one. One approach approximates $C$ by polygons and controls the limit; another, due to Thomassen (1992), derives the theorem from the fact that $K_{3,3}$ has no plane drawing with polygonal edges. Full proofs are in Mohar and Thomassen, Section 2.1, and in Thomassen (1992). Hales checked a full proof by computer (described in his 2007 paper). $\blacksquare$

## Consequences

- **Faces and Euler's formula.** In a plane graph, the two sides of an edge on a cycle lie in different faces. This is the step of the proof of [Euler's formula](/euler-formula/) that removes a cycle edge and merges two faces.
- **Non-planarity of $K_{3,3}$ and $K_5$, directly.** Draw a 6-cycle $a_1 b_1 a_2 b_2 a_3 b_3$ of $K_{3,3}$. It has an inside and an outside. Each of the three remaining edges $a_1 b_2$, $a_2 b_3$, $a_3 b_1$ is a chord of this cycle, and every two of them have interleaved ends on the cycle, so two interleaved chords on the same side would cross. Three chords cannot be split between two sides with no two on the same side. For $K_5$, draw a 5-cycle; its five chords form a pentagram, and each chord interleaves with exactly two others, so the interleaving relation is a 5-cycle, which cannot be split into two sides without two interleaved chords on one side. See [Kuratowski's theorem](/kuratowski-theorem/).
- **Point location.** The parity argument of the proof is the ray casting test for [point in polygon](/point-in-polygon/).
- **Surfaces.** The theorem fails on the torus: a meridian circle does not separate it. This is why a cycle of a graph on the torus need not bound a face, and why [graph genus](/graph-genus/) changes the face count in Euler's formula.

## Tightness

Each hypothesis matters.

| set $C$ | regions of $\mathbb{R}^2 \setminus C$ |
|---|---|
| a simple closed curve | 2 |
| a simple arc (the drawing of a path, or of any tree) | 1 |
| a single point (the drawing of one vertex) | 1 |
| a figure eight (two loops through one point, not simple) | 3 |
| the drawing of $K_4$ as a triangle with a vertex inside | 4 |

For the L-shaped polygon with corners $(0,0), (6,0), (6,2), (2,2), (2,6), (0,6)$ and the direction $d = (1, 0)$: the point $(1, 4)$ crosses only the segment from $(2,2)$ to $(2,6)$, so its count is 1 and it is inside. The point $(4, 4)$ crosses nothing, so it is outside. The point $(4, 1)$ crosses only the segment from $(6,0)$ to $(6,2)$, so it is inside.

The stronger **Jordan-Schönflies theorem** says that the inside is homeomorphic to an open disk. Its analogue in three dimensions is false: the Alexander horned sphere is an embedded sphere whose outside is not simply connected.

## History

Camille Jordan stated and proved the theorem in his Cours d'analyse in 1887. His proof was long criticized as incomplete; Hales (2007) argues that it is essentially correct. Oswald Veblen gave a proof in 1905 that was accepted as rigorous. Thomassen's 1992 proof derives it from graph theory. Hales completed a formal proof in the HOL Light proof assistant and described it in 2007.

## References
