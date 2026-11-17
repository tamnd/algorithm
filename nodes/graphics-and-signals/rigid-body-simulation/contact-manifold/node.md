---
tag: Y5AHWB
kind: definition
slug: contact-manifold
name: Contact manifold
aliases:
- contact point set
- persistent contact manifold
area: graphics-and-signals/rigid-body-simulation
level: core
summary: The set of contact points with a shared normal and penetration depths between two touching bodies, kept across frames for stable stacking.
prereqs: [collision-detection, penetration-depth, sutherland-hodgman]
see_also: [collision-impulse, projected-gauss-seidel, separating-axis-theorem, gjk-algorithm, expanding-polytope-algorithm, polygon-clipping, shock-propagation, baraff-contact-force-algorithm]
sources:
  - url: https://box2d.org/files/ErinCatto_IterativeDynamics_GDC2005.pdf
    title: "Erin Catto, Iterative Dynamics with Temporal Coherence, Game Developers Conference, 2005"
    locator: "Section 8.1 (contact caching and warm starting), Section 8.2 (contact identifiers from the clipping of the incident face against the reference face) and Section 9.1 (box stacking; contact reduction credited to Moravanszky and Terdiman)"
  - url: https://www.cs.cmu.edu/~baraff/sigcourse/notesd2.pdf
    title: "David Baraff, Rigid Body Dynamics II, motion with constraints, in Andrew Witkin and David Baraff, Physically Based Modeling: Principles and Practice, SIGGRAPH 97 course notes"
    locator: the vertex/face and edge/edge contact points between polyhedra, with their normals (general locator)
---

A contact manifold is what the narrow phase of [collision detection](/collision-detection/) hands to the contact solver for one pair of touching bodies. It is a short list of contact points that share one normal, each with its depth of penetration, and each with an id that names the features of the two shapes that made it. One point is not enough for a box on a table: a solver that sees only the deepest corner pushes that corner up, the box rocks, and the next frame finds a different corner. A manifold with the corners of the touching face lets the solver hold the box flat. The ids let the solver match points between frames and start from last frame's impulses, which is what makes stacks stable with few iterations. How the points are chosen and how many are kept is a set of heuristics, not a law.

## Definition

Let bodies $A$ and $B$ touch or nearly touch. A contact manifold for the pair is

$$\mathcal M = (n, \{(p_i, d_i, \text{id}_i)\}_{i=1}^{k}),$$

where:

- $n$ is one unit normal, from $B$ to $A$ ($y$ up, as in the rest of this area), shared by all points;
- $p_i$ is a contact point (or a pair of points, one on each surface);
- $d_i$ is the separation along $n$, negative for penetration (some engines store the depth $-d_i$ instead), and points are kept while $d_i$ is below a small margin;
- $\text{id}_i$ is a feature key, for example the pair of edges or the vertex and face that produced the point.

The solver gives each point a normal row and friction rows. The relative normal velocity at $p_i$ is $v_{rel,i} = n \cdot (v_A(p_i) - v_B(p_i))$, which is negative when the bodies approach there.

A **persistent** manifold is kept from frame to frame. Points whose id appears again keep their cached normal and friction impulses for warm starting (Catto 2005, Section 8.1); points that disappear are dropped. This is a heuristic: the cached impulse is a good start only when the contact changes little between frames.

**Feature ids (Catto 2005, Section 8.2).** For two boxes, the narrow phase picks a reference face on one box and an incident face on the other, clips the incident face against the side planes of the reference face (as in [Sutherland-Hodgman](/sutherland-hodgman/) clipping), and keeps the clipped points below the reference face. The id of a point records which edges were clipped to make it, so the same corner gets the same id in the next frame even if it moved a little.

**Reduction.** A face against a face can produce many points, for example eight from clipping two boxes in 3D. Engines keep at most four per pair, chosen to keep the deepest point and to span a large area. This is a heuristic. Catto (2005, Section 9.1) notes that boxes are often supported by four points and credits contact reduction to Moravanszky and Terdiman (2004); the paper itself does not state a four-point rule.

## Examples and non-examples

**A box on the ground (2D).** A box with sides 2 and 1 rests flat on the ground with an overlap of $0.01$ m. The manifold is $n = (0, 1)$ with two points at $x = -1$ and $x = 1$, both with $d = -0.01$, and ids naming the two bottom corners. The two normal rows of this manifold are the example of [projected Gauss-Seidel](/projected-gauss-seidel/).

**A tilted box (computed).** The same box is turned by $0.01$ rad and its center sits at height $0.495$. Its bottom corners are at $(-0.994950, -0.014975)$ and $(1.004950, 0.005025)$. The left corner penetrates by $0.014975$ m. The right corner is $0.005025$ m above the ground. With a margin of $0.01$ m, the manifold keeps both points, with separations $-0.014975$ and $+0.005025$. A solver that accepts a gap, with the target $v_{rel} \ge -d / \Delta t$ for a separation $d > 0$, applies no impulse at the right corner unless that corner would reach the ground within the step; the row is ready when it does. With a margin of zero, the manifold has only the left corner, and the right corner enters the solve only after it has penetrated.

**Polyhedra.** Baraff's course notes describe the contacts between polyhedra by vertex/face and edge/edge contact points, each with its own normal; a face resting on a face is described by the corners of the touching region. In the sense of this page, the points of one face/face contact share the face normal and form one manifold.

**Not a manifold: one deepest point.** [GJK](/gjk-algorithm/) with [EPA](/expanding-polytope-algorithm/) returns one normal and one pair of closest or deepest points. That is a single point of the manifold. Engines that build manifolds from it add one point per frame and keep a few of them, which is again a heuristic.

**Not one manifold: different normals.** A box in a corner touches the floor and a wall. These are two manifolds with two normals, not one manifold with mixed normals; the solver gives each its own rows.

## Related definitions

- The [penetration depth](/penetration-depth/) is the size of the smallest translation that separates two bodies; the depths $d_i$ of a manifold are measured along its one normal and may differ from point to point.
- The [separating axis theorem](/separating-axis-theorem/) gives the normal for boxes and convex polyhedra: the axis of least overlap.
- The [collision impulse](/collision-impulse/) is computed for one point of a manifold; with several points, the order of the points matters, and [projected Gauss-Seidel](/projected-gauss-seidel/) iterates over them.
- [Baraff's contact force algorithm](/baraff-contact-force-algorithm/) takes all points of all manifolds as one linear complementarity problem.
- [Shock propagation](/shock-propagation/) groups the manifolds of a stack by the level of the bodies in a contact graph.

## References
