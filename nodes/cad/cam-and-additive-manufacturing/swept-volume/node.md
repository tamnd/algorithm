---
tag: K7GNZA
kind: problem
slug: swept-volume
name: Swept volume computation
aliases:
- swept volume
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Compute the region a solid occupies as it moves along a path, as in machining simulation, collision checks and the design of moving parts.
prereqs: [minkowski-sum, sweep-surface]
see_also: [nc-verification, dexel-representation, z-map-model, configuration-space, collision-detection, solid-boolean-operations, minkowski-sum-convex-polygons, offset-surface]
sources:
  - paper: "K. Abdel-Malek, J. Yang, D. Blackmore and K. Joy, Swept volumes: fundation, perspectives, and applications, International Journal of Shape Modeling 12(1), 2006, 87 to 127"
    locator: the survey of the definitions, the envelope conditions and the methods (the word fundation is spelled this way in the printed title)
  - paper: "W. P. Wang and K. K. Wang, Geometric modeling for swept volume of moving solids, IEEE Computer Graphics and Applications 6(12), 1986, 8 to 17"
    locator: the envelope of a moving solid from the condition that the velocity is tangent to its boundary, applied to NC tools
  - paper: doi:10.1016/0010-4485(78)90058-1
    title: Robert O. Anderson, Detecting and eliminating collisions in NC machining, Computer-Aided Design 10(4), 1978, 231 to 237
    locator: the region of the tool over a move, represented by heights over a grid
  - book: isbn:978-3-540-77973-5
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 13, Robot Motion Planning, Section 13.3 on Minkowski sums of convex polygons and their size
---

A solid that moves fills a region of space: the union of all the places it occupies during the motion. That region is its swept volume. Machining simulation subtracts the swept volume of the tool from the stock, collision checking asks whether the swept volume of a moving part meets an obstacle, and designers of mechanisms use swept volumes to find the space a moving arm needs. The problem is to compute a representation of this region from the solid and the motion. When the solid only translates, the swept volume is a [Minkowski sum](/minkowski-sum/), and this is the easy case. When it also rotates, the boundary of the swept volume lies on the *envelope* of the moving boundary, where the velocity of the moving point is tangent to the surface, and the computation needs that condition. This page is about the region in three dimensions, or in the plane. The [sweep surface](/sweep-surface/) page covers a different object: the surface swept by a curve.

## In plain words

Hold a box and move it through the air along some path, turning it as you go. The swept volume is all the space the box touched at any moment.

If the box only slides without turning, the swept volume is easy: for a straight slide it is the box stretched along the direction of the slide. If it turns, the outline of the swept volume is made of the parts of the box surface that were moving sideways, along the surface, at that moment. Parts of the surface that move straight out of the box or straight into it stay inside the swept volume.

In a machine shop, the moving box is a cutting tool, and the swept volume of each move is the material it removes.

## Definition

**Input.**

- A solid $X \subset \mathbb{R}^3$ (or $\mathbb{R}^2$): compact and equal to the closure of its interior, given as a boundary representation, a mesh, an implicit function, or a primitive such as a ball, a cylinder or a cutter.
- A motion: a continuous map $M : [0, 1] \to SE(3)$ of rigid motions, $M(t) x = R(t) x + d(t)$, given as a path of the reference point and of the orientation, for example a sequence of tool positions with an interpolation rule.

**Output.** A representation of
$$ \operatorname{Sw}(X, M) = \bigcup_{t \in [0, 1]} M(t) X, $$
within a given tolerance, in a stated form: a boundary representation, a mesh, an implicit function, or samples on lines or cells.

**Translations.** If $R(t) = I$ for all $t$, then
$$ \operatorname{Sw}(X, M) = X \oplus D, \qquad D = \{d(t) : t \in [0, 1]\}, $$
because $x + d(t)$ for $x \in X$ and $t \in [0, 1]$ is exactly the set of sums $x + y$ with $y \in D$. For a straight move with $d(0) = 0$, $D$ is the segment from $0$ to $d(1)$, and for a convex $X$ the swept volume is the convex hull of $X$ and $X + d(1)$. A ball of radius $r$ moved along a segment sweeps a capsule.

**The envelope condition.** Suppose $\partial X$ is smooth with outward unit normal $n$, and $M$ is differentiable. For $x \in \partial X$ write $y = M(t) x$, $n_t(x) = R(t) n(x)$ for the normal of the moved surface at $y$, and $v_t(x) = \tfrac{d}{dt} M(t) x$ for the velocity of the moving point. Then every boundary point of $\operatorname{Sw}(X, M)$ has the form $M(t) x$ with $x \in \partial X$ and

- $t = 0$ or $t = 1$, or
- $0 < t < 1$ and $n_t(x) \cdot v_t(x) = 0$.

*Sketch.* Let $y = M(t) x$ lie on the boundary of the swept volume. If $x$ were an interior point of $X$, a neighborhood of $y$ would be inside $M(t) X$, so $x \in \partial X$. Suppose $0 < t < 1$ and $n_t(x) \cdot v_t(x) > 0$: the surface point moves outward. The points just inside $M(t) X$ near $y$ are in the swept volume, and the points just outside are covered by $M(t + \delta) X$ for small $\delta > 0$, because the surface near $y$ moves past them. By continuity this holds on a whole neighborhood of $y$, which is then inside the swept volume, a contradiction. The case $n_t \cdot v_t < 0$ is the same with $t - \delta$. $\square$

The points with $n_t \cdot v_t = 0$ form, for each $t$, a curve on the moved surface, the *characteristic curve*, and these curves together form the envelope. The condition is necessary, not sufficient: parts of the envelope can lie inside the swept volume, covered by the solid at another time, and must be trimmed away.

## Variants

- **Translation only.** A Minkowski sum with the path. For polyhedra and straight moves, the swept volume of a convex polyhedron is a convex hull of two copies.
- **General rigid motion.** The envelope condition, with trimming of the inner parts. Wang and Wang (1986) used it for NC tools.
- **Tool moves.** The solid is a surface of revolution about its axis, which simplifies the envelope: for a ball, the swept volume of a straight move is a capsule, and for a cylinder moved along its axis it is a longer cylinder.
- **Sampled.** Only the trace of the swept volume on a set of lines or cells, as in the [z-map](/z-map-model/) and the [dexel](/dexel-representation/) models. It is exact on the samples for simple tools and moves.
- **Deforming solids.** The shape of $X$ changes in time. Not covered here.

## Examples

**A square translated.** $X = [0, 1]^2$ moved by $d(t) = t (2, 1)$. The swept area is $X \oplus$ the segment from $(0, 0)$ to $(2, 1)$, the hexagon with vertices $(0, 0)$, $(1, 0)$, $(3, 1)$, $(3, 2)$, $(2, 2)$, $(0, 1)$. Its area is $4$: the square has area $1$, and the segment adds its length $\sqrt 5$ times the width of the square across the direction of motion, $3/\sqrt 5$. The two new edges, from $(1, 0)$ to $(3, 1)$ and from $(0, 1)$ to $(2, 2)$, are traced by the corners $(1, 0)$ and $(0, 1)$, the points where the direction of motion is tangent to the square.

**A square turned.** $X = [0, 1]^2$ turned about the origin from $0$ to $90$ degrees. At angle $\theta$ the square covers the polar angles from $\theta$ to $\theta + 90^\circ$, and its diagonal of length $\sqrt 2$ points at $\theta + 45^\circ$. So the swept area is the first square, the last square $[-1, 0] \times [0, 1]$, and the sector of radius $\sqrt 2$ between the polar angles $45^\circ$ and $135^\circ$, which the far corner traces. The sector has area $\tfrac12 \cdot \tfrac{\pi}{2} \cdot 2 = \tfrac{\pi}{2}$, and each square adds a triangle of area $\tfrac12$ outside it, so the swept area is $1 + \tfrac{\pi}{2} \approx 2.571$. The arc is on the envelope: the velocity of the far corner is tangent to its circle. The edges of the two squares on the $x$ axis come from $t = 0$ and $t = 1$.

**A ball move.** A ball of radius $r$ whose center moves straight from $c_0$ to $c_1$ sweeps the capsule of points at distance at most $r$ from the segment $c_0 c_1$. Its envelope is the cylinder of radius $r$ about the segment, and the half spheres at the two ends come from $t = 0$ and $t = 1$.

## Known algorithms

- **Minkowski sums.** For translations, the algorithms of the [Minkowski sum](/minkowski-sum/) page: a merge of edge directions for convex polygons ([Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/)), and decomposition into convex pieces and a union for the rest.
- **Envelope methods.** Solve $n_t(x) \cdot v_t(x) = 0$ for the characteristic curves at a set of times, join them into a surface, add the start and end positions, and trim the inner parts. Exact for primitives such as tools, approximate in general. The survey of Abdel-Malek, Yang, Blackmore and Joy (2006) lists these methods, including the ones based on the rank of the Jacobian of the map $(x, t) \mapsto M(t) x$ and on a differential equation for the sweep.
- **Union of samples.** Take positions at times $t_0 < \dots < t_s$ and the union of $M(t_j) X$ with [solid Boolean operations](/solid-boolean-operations/) or on a sampled model. It misses the parts between the samples, so the error depends on the step.
- **Sampled models.** For machining, the [z-map](/z-map-model/) and [dexel](/dexel-representation/) models compute the trace of the swept tool on each line by a closed form for simple tools, with no B-rep at all.
- **Distance fields.** Represent the swept volume implicitly by $\min_t \operatorname{dist}(M(t)^{-1} y, X)$, and extract a surface with [marching cubes](/marching-cubes/). Approximate, with the error of the grid.

What is proved: the Minkowski sum identity for translations and the envelope condition. What is measured: the speed and the accuracy of the sampling and the distance field methods, which depend on the step and the grid.

## Bounds

- **Convex polygon, straight move.** For a convex polygon with $n$ vertices, the swept area is a convex polygon with at most $n + 2$ vertices, computed in $O(n)$ time from the two copies.
- **Polygon along a polyline.** For a polygon with $n$ vertices translated along a polyline with $k$ segments, the swept area is the Minkowski sum of the polygon and the polyline, with the size bounds of the [Minkowski sum](/minkowski-sum/) page.
- **Rotations.** The envelope of a polyhedron under a motion with rotation is made of ruled and curved patches whose number depends on the motion, so no bound in $n$ alone holds without a model of the motion. This page gives none.

## Reductions

- **Translation to Minkowski sum.** Shown above.
- **Motion planning.** A robot $X$ moved by $M$ collides with an obstacle $O$ if and only if $\operatorname{Sw}(X, M) \cap O \ne \emptyset$ (with interiors for touching). For translations this is the test of whether the path $D$ meets the [configuration space](/configuration-space/) obstacle $O \oplus (-X)$.
- **Machining.** [NC verification](/nc-verification/) subtracts the swept volumes of the tool from the stock.

## Applications

- Machining simulation and NC verification, with the tool as the moving solid.
- Collision and clearance checks for robots, assembly paths and the moving parts of a machine.
- Design of mechanisms, where the swept volume of a link is the space it needs.
- Modeling by sweeping: a designer moves a simple solid to create a shape, as in the sweeps of CAD systems.

## References
