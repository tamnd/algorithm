---
tag: 41PNBY
kind: problem
slug: solid-offsetting
name: Solid offsetting
aliases:
- offset solid
- solid growing and shrinking
area: cad/solid-modeling
level: advanced
summary: Grow or shrink a solid by a distance r, the Minkowski sum or difference with a ball, as used for tolerances, tool clearance and thin walls.
prereqs: [r-set, minkowski-sum, offset-surface]
see_also: [rossignac-requicha-offsetting, regularized-set-operations, signed-distance-function, medial-axis, straight-skeleton, contour-parallel-toolpath, inverse-tool-offset, tolerance-stack-up]
sources:
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: the whole paper (the definition of growing and shrinking, their properties, the regularized shrink, the use for tolerances, clearance, cutter paths and rounding, and the method for CSG solids)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 11, Offset curves and surfaces, Section 11.3, Offset surfaces, and Section 11.5, General offsets
  - paper: "Takashi Maekawa, An overview of offset curves and surfaces, Computer-Aided Design 31(3), 165 to 173, 1999"
    locator: the sections on offsets of surfaces and of solids and on the removal of self-intersections
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the r-sets and the regularized operations that the offset operations must preserve
---

Solid offsetting is the problem of growing a solid $S$ by a distance $r$, the set $S \uparrow r$ of points within distance $r$ of $S$, or shrinking it by $r$, the set $S \downarrow r$ of points whose ball of radius $r$ lies in $S$. Growing is the [Minkowski sum](/minkowski-sum/) of $S$ with a ball and shrinking is the Minkowski difference. The faces of the result are trimmed [offset surfaces](/offset-surface/) of the faces of $S$, joined by pieces of cylinders around the convex edges and of spheres around the convex vertices, and finding where these pieces cut each other is the hard part. Rossignac and Requicha defined the two operations for solid modeling in 1986 and showed how tolerance zones, clearance checks, cutter paths and rounded edges all reduce to them.

## In plain words

Take a solid object and coat it with a layer of paint of constant thickness. The painted object is the solid grown by the thickness. Now do the opposite: scrape a layer of constant thickness off every face. That is the solid shrunk.

The new skin is not just each face moved out. At a sharp outer edge, the moved faces leave a gap that must be filled with a rounded strip, and at a sharp inner corner, the moved faces run into each other and must be cut back. When the layer is thick, parts can merge, holes can close, and thin walls can vanish.

Shrinking and then growing back by the same amount rounds off the outer edges. Growing and then shrinking fills in the inner corners.

## Definition

**Input.** A solid $S$, an [r-set](/r-set/) given as a [boundary representation](/boundary-representation/) or a [CSG tree](/constructive-solid-geometry/), a distance $r \ge 0$, and an operation, grow or shrink.

**Output.** A valid representation of one of the sets

$$S \uparrow r = S \oplus B_r = \{x : \operatorname{dist}(x, S) \le r\}, \qquad S \downarrow r = \{x : x + B_r \subseteq S\},$$

where $B_r$ is the closed ball of radius $r$ at the origin. The shrunk set can have parts without volume, such as the segment that remains of a slab of thickness exactly $2r$, so the output of shrinking is its regularization $\operatorname{cl}(\operatorname{int}(S \downarrow r))$, as for the [regularized set operations](/regularized-set-operations/).

**Constraints.** The output is a solid in the same scheme, or a B-rep whose faces are exact or approximate within a stated tolerance. The topology of the output must be that of the exact set: components that merge, holes that close and walls that vanish are part of the answer. Degenerate input is part of the problem, for example two faces at distance exactly $2r$, where growing makes them touch.

**Size.** The number of faces, edges and vertices of $S$, and the size of the output.

**Model.** The [real RAM](/real-ram/) with exact operations on the algebraic numbers that occur (square roots already for a disk), or floating point with a tolerance.

**What it is not.** This page states the task. The [Rossignac and Requicha method](/rossignac-requicha-offsetting/) is one algorithm for it, for CSG input, which builds the grown solid from offsets of the primitives and of their faces, edges and vertices.

## Variants

- **Grow and shrink.** In morphology, dilation and erosion by a ball. They are dual: up to regularization, $S \downarrow r$ is the closure of the complement of $(\operatorname{cl}(\mathbb{R}^3 \setminus S)) \uparrow r$.
- **Rounding and filleting.** Rossignac and Requicha define rounding as $(S \downarrow r) \uparrow r$, which rounds the convex edges with radius $r$, and filleting as $(S \uparrow r) \downarrow r$, which fills the concave edges. In morphology these are the opening and the closing.
- **Shelling.** A hollow part with walls of thickness $t$ is $S -^* (S \downarrow t)$, used for molded and printed parts.
- **General offsets.** The Minkowski sum with a convex body other than a ball, for example the shape of a flat-end cutter, or a distance that varies over the surface.
- **The plane.** Offsetting a polygon by a disk. Its mitred version, with sharp corners instead of arcs, is the [straight skeleton](/straight-skeleton/) offset, and its repeated use gives [contour-parallel tool paths](/contour-parallel-toolpath/).
- **Approximate offsets.** The level set $\{x : \operatorname{dist}(x, S) = r\}$ of a sampled [signed distance function](/signed-distance-function/), extracted as a mesh.

## Examples

- **A ball.** The ball of radius $R$ grows to the ball of radius $R + r$ and shrinks to the ball of radius $R - r$, or to the empty set when $r > R$. At $r = R$ the shrink is a single point, which regularization removes.
- **A box.** The box $[0, a] \times [0, b] \times [0, c]$ grown by $r$ is a rounded box: $6$ face rectangles moved out by $r$, $12$ quarter cylinders of radius $r$ along the edges and $8$ eighths of a sphere at the corners. Its volume is $abc + 2r(ab + bc + ca) + \pi r^2 (a + b + c) + \tfrac{4}{3}\pi r^3$, by Steiner's formula. Shrunk by $r < \min(a, b, c)/2$, it is the box $[r, a - r] \times [r, b - r] \times [r, c - r]$ with sharp edges.
- **Rounding a square.** In the plane, take the square $Q = [0, 2]^2$ and $r = 1/2$. Then $Q \downarrow r = [1/2, 3/2]^2$, and growing that by $1/2$ gives the square $[0, 2]^2$ with each corner replaced by a quarter circle of radius $1/2$. Each corner loses $r^2 - \pi r^2/4 = 1/4 - \pi/16$, so the area drops by $1 - \pi/4$. Filleting $Q$ gives $Q$ itself, since $Q$ has no concave corner.
- **Filleting an L shape.** For the L shape $[0, 2]^2 -^* [1, 2]^2$ and $r = 1/2$, growing and then shrinking fills the concave corner at $(1, 1)$ with the region between the two edges and a quarter circle of radius $1/2$ that touches both, of area $1/4 - \pi/16$. The convex corners stay sharp.
- **Merging.** Two unit cubes at distance $2r + \delta$ grow into two components for $\delta > 0$ and into one component, touching at a single segment or face, for $\delta = 0$.

## Known algorithms

- **[Rossignac and Requicha offsetting](/rossignac-requicha-offsetting/).** For CSG input. The grown solid of a union is the union of the grown operands, so growing a CSG tree reduces to growing primitives where the tree has only unions. For other nodes, the method expresses the grown solid as the union of the solid with the offsets of its faces, edges and vertices, each a simple swept primitive, and evaluates the result by point membership classification.
- **B-rep offsetting.** Offset each face to a trimmed offset surface, add cylinders or more general pipe pieces at the convex edges and spheres at the convex vertices, intersect the pieces with [surface surface intersection](/surface-surface-intersection/), and remove the parts that are closer than $r$ to the solid. This is the method of most commercial modelers, and the removal of self-intersections is its weak point.
- **Distance fields.** Sample the signed distance to $S$ on a grid or an adaptive tree and extract the $r$ level set. It is robust and simple, and its output is a mesh with a sampling error.
- **The plane.** Offsets of polygons and of regions with circular arcs from the [medial axis](/medial-axis/) or the Voronoi diagram of the edges, which give the exact offset for every $r$ at once.
- **Minkowski sums of polyhedra.** Approximate the ball by a convex polytope and compute the Minkowski sum by convex decomposition, as on the [Minkowski sum](/minkowski-sum/) page.

## Bounds

The following facts are proved, most of them in the paper of Rossignac and Requicha or by short arguments from the definitions.

- **Unions and intersections.** $(A \cup B) \uparrow r = A \uparrow r \cup B \uparrow r$ and $(A \cap B) \downarrow r = A \downarrow r \cap B \downarrow r$, exactly. But $(A \cap B) \uparrow r \subseteq A \uparrow r \cap B \uparrow r$, and the inclusion is strict in general: for two unit squares at distance $1$, the left side is empty and the right side is not when $r \ge 1/2$. So growing commutes with union only, which is why a CSG method cannot push the growth to the leaves in general.
- **Regularity.** $S \uparrow r$ is a union of closed balls of radius $r > 0$, so it is closed and regular. $S \downarrow r$ need not be regular, which is why it is regularized.
- **Rounding and filleting.** $(S \downarrow r) \uparrow r \subseteq S \subseteq (S \uparrow r) \downarrow r$, and both operations are idempotent, as in mathematical morphology.
- **Discontinuity.** The topology of $S \uparrow r$ changes when $r$ passes half the distance between two parts, as in the merging example. A decision about this is a sign of a distance minus $2r$, which needs exact or certified arithmetic near the critical value, for the same reason as the [orientation test](/orientation-test/) of polyhedral Booleans: a rounded difference of nearly equal numbers can have the wrong sign ([catastrophic cancellation](/catastrophic-cancellation/)).
- **Size in the plane.** The offset curve of a simple polygon with $n$ vertices has $O(n)$ segments and arcs. Each piece lies in one cell of the Voronoi diagram of the edges and vertices, and the distance to the sites along a Voronoi edge is unimodal, so the offset crosses each of the $O(n)$ Voronoi edges at most twice.

The running times and the failure rates of B-rep offsetting codes on industrial models are measured, not proved. No general bound on the size of the offset of a curved B-rep is stated here.

## Reductions

- **To Minkowski sums.** Growing is the Minkowski sum with $B_r$, and shrinking is the complement of growing the complement.
- **Clearance and interference.** Two solids are at distance at least $c$ exactly when $\operatorname{int}(A \uparrow c) \cap B = \emptyset$. So a clearance check is one grow and one interference test, which is a [solid Boolean operation](/solid-boolean-operations/).
- **Motion planning for a ball.** The free space of a ball robot of radius $r$ among obstacles $O$ is the complement of $O \uparrow r$, and the robot reduces to a point.
- **Cutter paths.** The center of a ball-end cutter of radius $r$ that touches but does not cut the part moves on the boundary of the part grown by $r$; see [inverse tool offset](/inverse-tool-offset/).

## Applications

- **Tolerance zones.** The set of acceptable shapes of a face within a tolerance $t$ is bounded by its grown and shrunk versions; see [tolerance stack-up](/tolerance-stack-up/).
- **Rounds and fillets.** Constant-radius rounding and filleting of whole solids by the compositions above.
- **Thin walls.** Shelling a part for injection molding, casting or 3D printing.
- **Machining and robotics.** Tool clearance, cutter location surfaces and the free space of a robot.
- **VLSI design rules.** Rossignac and Requicha name design-rule checking as an application: the shapes on a chip must keep minimum distances, which is a clearance test.

## References
