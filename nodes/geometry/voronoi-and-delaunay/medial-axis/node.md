---
tag: K4ZRGN
kind: concept
slug: medial-axis
name: Medial axis
aliases:
- Blum medial axis
- skeleton of a shape
- medial axis transform
- Voronoi diagram of line segments
area: geometry/voronoi-and-delaunay
level: advanced
summary: Set of centers of maximal disks inside a shape, computed as a Voronoi diagram restricted to the shape.
prereqs: [voronoi-diagram, simple-polygon]
see_also: [straight-skeleton, fortunes-algorithm, weighted-voronoi-diagram, largest-empty-circle, voronoi-cell, alpha-shape, distance-transform, offset-curve]
sources:
  - paper: "H. Blum, A transformation for extracting new descriptors of shape, in Models for the Perception of Speech and Visual Form, MIT Press, 1967, 362-380"
    locator: the medial axis as the set of centers of maximal discs, with the radius function
  - paper: "D. T. Lee, Medial axis transformation of a planar shape, IEEE Transactions on Pattern Analysis and Machine Intelligence 4(4), 1982, 363-369"
    locator: the medial axis of a simple polygon as part of the Voronoi diagram of its edges and vertices, built in O(n log n) time
  - paper: "F. Chin, J. Snoeyink and C. A. Wang, Finding the medial axis of a simple polygon in linear time, Discrete and Computational Geometry 21(3), 1999, 405-420"
    locator: the O(n) algorithm for simple polygons
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987
    locator: the extension of the sweep to sites that are line segments, with parabolic arcs in the diagram
---

The medial axis of a shape in the plane is the set of points inside it that have two or more nearest points on the boundary. Equivalently, up to its limit points, it is the set of centers of the maximal discs that fit inside the shape. With the radius of the disc at each point, it describes the shape completely, and it is a thin, branching curve that follows the middle of the shape: a skeleton. For a polygon it is part of the Voronoi diagram whose sites are the polygon's edges and vertices, so it is built with the tools for the [Voronoi diagram](/voronoi-diagram/), extended from points to line segments. It is made of straight segments and parabolic arcs.

## In plain words

Set fire to the edge of a dry field all around at the same time. The fire moves inward at the same speed everywhere. The places where two fire fronts meet and go out form a thin, branching line in the middle of the field. That line is the medial axis.

Another way to see it: push the largest coin you can into each part of the shape. If a coin cannot grow in any direction without leaving the shape, its center is on the medial axis. The coin touches the edge in two or more places, or it sits in a tight round end.

The line shows the shape's structure, like the bones of a body, and the coin sizes along it tell how thick the shape is at each place.

## The idea

Notation: $P$ is the set of $n$ vertices of a simple polygon $\Omega$, given in counterclockwise order, with $h$ of them on the boundary of its convex hull; a point is $p = (x, y)$; $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, so a vertex $b$ with neighbours $a$ and $c$ is **reflex** when $\mathrm{orient}(a, b, c) < 0$; $\mathrm{incircle}$ is the [in-circle test](/in-circle-test/). For a set $S$, $d(x, S)$ is the distance from $x$ to the nearest point of $S$. No general position is assumed.

**Definition.** Let $\Omega$ be a closed bounded set in the plane, the closure of its interior, with boundary $\partial \Omega$. The **medial axis** $M(\Omega)$ is the set of points $x$ in the interior of $\Omega$ with at least two points $y \in \partial \Omega$ at distance $d(x, \partial \Omega)$. A closed disc in $\Omega$ is **maximal** when no other closed disc in $\Omega$ contains it. The **medial axis transform** is the pair of $M(\Omega)$ and the radius function $r(x) = d(x, \partial \Omega)$; for a polygon, the union of the closed discs of radius $r(x)$ around the points $x$ of the closure of $M(\Omega)$ is $\Omega$.

**Lemma.** Every point of $M(\Omega)$ is the center of a maximal disc.

*Proof.* Let $x \in M(\Omega)$, $r = d(x, \partial \Omega)$, and let $y_1 \ne y_2$ be two nearest boundary points. The closed disc $D$ of radius $r$ around $x$ is in $\Omega$. Let $D' \supseteq D$ be a closed disc in $\Omega$. The interior of $D'$ is an open set in $\Omega$, so it holds no boundary point, and $y_1$, $y_2$ are on the circle of $D'$. They are also on the circle of $D$. Two different circles, one inside the other, meet in at most one point, so $D' = D$. $\square$

The converse fails only at limit points: the center of a maximal disc that touches the boundary along one arc of its own radius, such as the center of curvature at the end of an ellipse, has one nearest point. Blum's original definition, by maximal discs, adds these points; it lies between $M(\Omega)$ and its closure.

**Polygons and the Voronoi diagram of segments.** Let $\Omega$ be a simple polygon. Take as sites its $n$ vertices and its $n$ open edges. The distance from $x$ to a site is the distance to the nearest point of that site, and the Voronoi diagram of these $2n$ sites splits the plane by nearest site. Inside $\Omega$:

- Assign each point $x$ of the interior to the sites that contain one of its nearest boundary points. This splits the interior into regions. The region of a convex vertex is empty, and the region of a reflex vertex is the wedge between the two normals to its edges at that vertex.
- The boundaries between the regions are the bisector pieces of two sites, and also the two normal segments at each reflex vertex, which separate the region of the vertex from the regions of its two edges. A point is in $M(\Omega)$ exactly when it has two or more nearest boundary points, so $M(\Omega)$ is the set of these boundaries without the normal segments: on a normal segment, the reflex vertex is the only nearest point.
- The Voronoi edges between two sites are pieces of their bisector. Between two vertices it is a line. Between two edges it is a line, a piece of an angle bisector of their supporting lines. Between a vertex $v$ and an edge $e$ not through $v$ it is a piece of the parabola with focus $v$ and directrix the line of $e$.
- So $M(\Omega)$ is made of $O(n)$ line segments and parabolic arcs, and since $\Omega$ is simply connected it is known to be a tree. Parabolic arcs appear only at reflex vertices; a convex polygon has no parabolic arc, and there its medial axis is the same as its [straight skeleton](/straight-skeleton/).

**Algorithms.**

- **Segment Voronoi diagrams.** For $n$ sites that are points and line segments with disjoint interiors, the Voronoi diagram has $O(n)$ size and is built in $O(n \log n)$ worst-case time, for example by [Fortune's sweep](/fortunes-algorithm/) extended to segments, or by divide and conquer (Yap, 1987).
- **Simple polygons.** Lee (1982) gave an $O(n \log n)$ algorithm for the medial axis of a simple polygon. Chin, Snoeyink and Wang (1999) gave an $O(n)$ algorithm. These are cited bounds, not proved here.
- **Sampling.** For a curved shape, sample the boundary densely and compute the ordinary Voronoi diagram of the samples. In the plane, the Voronoi vertices inside the shape approach the medial axis as the sampling gets denser; in space only special Voronoi vertices, the poles, do.
- **Pixels.** On images, the [distance transform](/distance-transform/) and thinning methods give a discrete skeleton.

**Exact arithmetic.** The Voronoi vertices of segments are not rational in general: they are equidistant from lines and points, which gives equations with square roots. Exact programs use algebraic numbers or carefully bounded floating point; the example below shows an irrational vertex for a polygon with integer corners.

**Instability.** A tiny bump on the boundary adds a long branch to the medial axis, so the medial axis is not a continuous function of the shape. Applications prune branches whose discs add little to the shape.

## Examples

**A rectangle.** For $\Omega = [0, 4] \times [0, 2]$, the medial axis is the segment from $(1, 1)$ to $(3, 1)$, where the top and the bottom edge are nearest, and four segments on the angle bisectors, from each corner to the nearer of $(1, 1)$ and $(3, 1)$; the corners themselves are only limit points. The largest disc has center $(2, 1)$ and radius $1$. All pieces are straight, because the rectangle is convex.

**An L-shape.** Let $\Omega$ have corners $(0,0)$, $(4,0)$, $(4,2)$, $(2,2)$, $(2,4)$, $(0,4)$; the corner $(2,2)$ is reflex. On the diagonal $y = x$ from $(0,0)$, the point $(t, t)$ is at distance $t$ from the edges $x = 0$ and $y = 0$, and at distance $\sqrt{2} (2 - t)$ from $(2,2)$. These are equal at $t = 4 - 2\sqrt{2} \approx 1.17$, an irrational Voronoi vertex, where the disc touches both edges and the reflex corner. From there, the points at equal distance from $(2,2)$ and the edge $y = 0$ form the parabola

$$y = \frac{(x - 2)^2 + 4}{4},$$

which passes through $(4 - 2\sqrt{2}, 4 - 2\sqrt{2})$ and reaches $(2, 1)$, where the edge $y = 2$ also becomes nearest. Then the axis runs along $y = 1$ to $(3, 1)$ and splits to the corners $(4, 0)$ and $(4, 2)$. The upper arm is the mirror image in $y = x$, with the parabola $x = ((y - 2)^2 + 4)/4$.

**A point and a segment.** For the sites $(0, 2)$ and the segment from $(-3, 0)$ to $(3, 0)$, the bisector is the parabola $y = (x^2 + 4)/4$ for $|x| \le 3$, where the nearest point of the segment is straight below. For $x > 3$ the nearest point of the segment is the end $(3, 0)$, and the bisector is the line $6x - 4y = 5$, which meets the parabola at $(3, \frac{13}{4})$; the case $x < -3$ is the mirror image.

## Where it is used

- **Shape analysis and recognition.** The skeleton gives a graph that describes the parts of a shape and how they connect, used in computer vision and in character recognition.
- **Path planning.** A robot that follows the medial axis of the free space keeps as far from obstacles as possible.
- **Machining and offsets.** The offset curves of a polygon at distance $t$, used for pocket machining, are read off the medial axis transform ([offset curve](/offset-curve/)).
- **Mesh generation.** The medial axis splits a domain into simple parts and gives a local size for the mesh.
- **Largest inscribed disc.** Along each straight or parabolic piece of the medial axis of a polygon, the radius is an affine or convex function of the position, so it has no strict maximum inside the piece, and the largest disc inside a polygon has its center at a vertex of the medial axis. The [largest empty circle](/largest-empty-circle/) is the same question for point sites.

## References
