---
tag: WFNCHK
kind: algorithm
slug: beam-tracing
name: Beam tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Trace whole pyramids of rays through a polygonal scene. Clip each beam against the polygons in front-to-back order, and spawn reflected beams from the mirror image of the apex.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: "the number of polygons or segments", b: "the number of beams in the beam tree"}
  time: {worst: O(b n^2), best: Θ(n)}
  space: {extra: O(b n)}
properties: {deterministic: true, exact: true, recursive: true, object-space: true}
history:
  year: 1984
  people: [Paul S. Heckbert, Pat Hanrahan]
  note: Heckbert and Hanrahan replaced the rays of a ray tracer by beams with polygonal cross-sections, built a beam tree of the visible polygon fragments and their reflections, and drew the tree with a polygon renderer.
prereqs: [hidden-surface-removal, polygon-clipping]
see_also: [weiler-atherton-algorithm, whitted-ray-tracing, cone-tracing, ray-differentials, ray-coherence, ray-packet-tracing, bsp-tree, warnock-algorithm]
sources:
  - paper: doi:10.1145/800031.808588
    title: Paul S. Heckbert and Pat Hanrahan, Beam tracing polygonal objects, Computer Graphics 18(3) (SIGGRAPH 84), 1984, pages 119 to 127
    locator: the whole paper (beams with polygonal cross-sections, the intersection of a beam with the polygons in depth order, reflection by a virtual eye point, the linear approximation of refraction, and the beam tree)
  - paper: doi:10.1145/323233.323241
    title: Norm Dadoun, David G. Kirkpatrick and John P. Walsh, The geometry of beam tracing, Symposium on Computational Geometry 1985, pages 55 to 61
    locator: the analysis of beam tracing with hierarchical space subdivision, from the point of view of computational geometry
  - paper: doi:10.1145/280814.280818
    title: Thomas Funkhouser, Ingrid Carlbom, Gary Elko, Gopal Pingali, Mohan Sondhi and Jim West, A beam tracing approach to acoustic modeling for interactive virtual environments, SIGGRAPH 98, 1998, pages 21 to 32
    locator: beam tracing through a cell decomposition of a building to find the reflection paths of sound
---

Beam tracing replaces the single rays of a ray tracer by *beams*: pyramids of rays with a common apex and a polygonal cross-section. A beam from the eye covers a whole view at once. It is clipped against the polygons of the scene in front-to-back order. Each polygon takes the part of the beam that it covers and that no nearer polygon has taken, and that part is a visible fragment. A visible fragment on a mirror spawns a reflected beam, whose apex is the mirror image of the old apex in the mirror's plane, and which is traced in the same way. The fragments and their reflections form a *beam tree*, which a polygon renderer can draw directly, with exact reflections and no per-pixel rays. Heckbert and Hanrahan introduced the method in 1984. It works for polygonal scenes and planar mirrors. Curved surfaces do not reflect a pyramid into a pyramid, and refraction is not linear, so the method approximates it.

## In plain words

A ray tracer asks, for one pixel at a time, "what does this thin line of sight hit first?". Neighboring pixels nearly always get the same answer from the same surface. Beam tracing asks the question once for a whole fan of sight lines.

Shine a flashlight with a square lens into a room. Each object takes the part of the light that reaches it first and leaves a shadow behind it. The lit parts are what the eye sees. When light falls on a flat mirror, it bounces as if it came from a second flashlight behind the mirror, at the mirror image of the first. So you start a new fan from that point, through the lit part of the mirror, and repeat.

## The problem

Given a scene of polygons (in the plane, line segments), some of them planar mirrors, an eye point and a view region, list for the view the visible fragments of each polygon, and the same for the views seen in mirrors, up to a given number of reflections. A fragment is a maximal part of a polygon that is visible in the beam, together with the part of the beam that sees it. This is [hidden-surface removal](/hidden-surface-removal/) in object space, extended by reflections.

The implementation on this page solves the problem in the plane with exact rational arithmetic. A beam is a wedge narrower than a half turn, with directions $v(s) = d_l + s(d_r - d_l)$ for $s \in [0, 1]$. The segments are disjoint, so that a front-to-back order exists.

## The algorithm

```pseudo id=main
TRACE-BEAM(beam with apex A, window W, depth)
L1  for each polygon P of the scene, except the one that holds W:
L2      piece[P] ← P clipped to the beam (and to the far side of W)
L3  remaining ← the whole cross-section of the beam
L4  for each piece in front-to-back order from A:
L5      visible ← piece ∩ remaining;  remaining ← remaining − piece
L6      for each visible fragment F: add F to the beam tree
L7          if P is a mirror and depth < maximum depth then
L8              A' ← the mirror image of A in the plane of P
L9              child[F] ← TRACE-BEAM(beam from A' through F, window F, depth + 1)
L10 return the beam with its fragments and children
```

In 3D, line L2 is the clipping of a polygon to a pyramid, line L5 is a polygon intersection and difference, as done by the [Weiler-Atherton algorithm](/weiler-atherton-algorithm/), and the cross-section is a set of polygons. In the plane, the cross-section is a set of intervals of $s$, and line L5 is interval arithmetic on them. The front-to-back order in line L4 comes from a [BSP tree](/bsp-tree/), a depth sort, or, as in the implementation, from comparing every pair of pieces whose intervals overlap and sorting the resulting graph.

The window $W$ of a reflected beam matters. The child beam starts at $A'$, behind the mirror, but only the points on the far side of the mirror's line, which is the side of the original apex, belong to it. Without this, the beam would "see" polygons behind the mirror.

## Example

The apex is $A = (0, 0)$ and the beam is the wedge from $d_l = (2, -1)$ to $d_r = (2, 1)$, so direction $s$ is $(2, -1 + 2s)$. The scene has three segments:

- $P_0$ from $(3, -1)$ to $(3, 0.5)$, opaque;
- $P_1$ from $(5, -3)$ to $(5, 3)$, a mirror;
- $P_2$ from $(1, -4)$ to $(1, -6)$, opaque, outside the first beam.

| step | piece or fragment | $s$ interval | remaining after |
|---|---|---|---|
| L2 | $P_0$ clipped | $[1/6, 2/3]$ | |
| L2 | $P_1$ clipped | $[0, 1]$ | |
| L4, L5 | $P_0$ visible, from $(3, -1)$ to $(3, 0.5)$ | $[1/6, 2/3]$ | $[0, 1/6] \cup [2/3, 1]$ |
| L4, L5 | $P_1$ visible, from $(5, -2.5)$ to $(5, -5/3)$ | $[0, 1/6]$ | $[2/3, 1]$ |
| L4, L5 | $P_1$ visible, from $(5, 5/6)$ to $(5, 2.5)$ | $[2/3, 1]$ | empty |

$P_0$ is nearer than $P_1$ wherever both are in the beam, so the order puts $P_0$ first. Each of the two fragments of the mirror spawns a child with the apex $A' = (10, 0)$, the image of $A$ in the line $x = 5$. The lower child, through the fragment from $(5, -5/3)$ to $(5, -2.5)$, reaches $x = 1$ with $y$ between $-3$ and $-4.5$, and finds the fragment of $P_2$ from $(1, -4)$ to $(1, -4.5)$. The upper child meets nothing and leaves the scene. The tests check this tree exactly and compare random scenes with ten segments and up to three reflections against single rays traced with exact fractions: every ray of a beam, away from the fragment boundaries, follows the same chain of segments to the same hit points.

## Correctness

Fix a direction $s$ that is not an endpoint of any piece. Two pieces that both contain $s$ in their interval are disjoint segments, so along their common interval the difference of their distances from the apex never changes sign. A front-to-back order therefore puts the nearer piece first, and such an order exists for disjoint segments. Line L5 gives $s$ to the first piece in the order that contains it, which is the nearest one, and so the fragment containing $s$ is the first hit of the ray in direction $s$ within the beam. For a reflected beam, the points of the reflected ray from a hit point $h$ are exactly the points of the line from $A'$ through $h$ beyond $h$, which is the child beam beyond its window, and distances along both grow together. Induction on the depth gives the theorem: the path of every ray through the beam tree equals the path of that ray traced alone. The full proof, including the existence of the order, is in [the correctness proof](proofs/correctness.md).

## Complexity

In the plane, one beam clips $n$ segments in $O(n)$ time and orders the pieces by comparing pairs in $O(n^2)$ time; the interval updates of line L5 take $O(n)$ per piece, because $n$ disjoint segments seen from one point give at most $2n - 1$ fragments. So one beam costs $O(n^2)$, and the tree costs $O(b n^2)$ for $b$ beams. With an order given in advance by a BSP tree and no reflections, the cost is $\Theta(n)$ for the clipping. The extra space is $O(n)$ per beam for its fragments, $O(b n)$ in total.

The number of beams $b$ is the problem. Each mirror fragment of a beam spawns a beam, so $b$ can grow by a factor of up to the number of visible mirror fragments at each level: exponentially in the depth. In 3D, the beams also get more complex cross-sections after each clip, and the polygon operations of line L5 cost more than a constant per piece. A ray tracer pays per pixel instead; beam tracing wins when there are few polygons and many pixels.

## Properties

- **Exact for planar mirrors.** Reflection in a plane maps a pyramid with polygonal cross-section to another, so the reflected beams are exact. A single beam replaces all rays through a view region, with no sampling.
- **Object space.** The output is a set of polygons in the scene, independent of the image resolution. A renderer can draw it at any resolution, and it can be reused while the view moves inside the same visible set.
- **No aliasing from sampling the geometry.** Edges come out as exact polygon edges, so the aliasing of point sampling is replaced by the antialiasing of the polygon renderer.
- **Polygonal scenes only.** A curved surface reflects a pyramid into a curved, not polygonal, beam.
- **Refraction is approximate.** Snell's law is not linear, so a refracted pyramid is not a pyramid. Heckbert and Hanrahan approximate it by a linear map.
- **Depth-limited.** The tree must be cut at a maximum depth, or at fragments below a size, because the number of beams grows exponentially.

## Variants and improvements

- **Acoustics.** Funkhouser et al. (1998) traced beams through a cell decomposition of a building to find all specular reflection paths of sound from a source to listeners. Sound needs few reflections per path but every path, which suits beams.
- **Cell and portal traversal.** In architectural scenes the beams pass through portals between cells, and the beam is clipped to each portal. This is the same clipping of line L2 with the portal as window.
- **Cone tracing.** [Cone tracing](/cone-tracing/) uses circular cones instead of pyramids, handles curved surfaces approximately, and computes partial coverage for antialiasing instead of exact fragments.
- **Ray differentials.** [Ray differentials](/ray-differentials/) keep only the first-order size of a beam around a single ray, which works on any smooth surface at the price of exactness.
- **Packets.** [Ray packet tracing](/ray-packet-tracing/) groups rays into a frustum but still intersects them one by one. The frustum test of a packet is the beam idea used only for culling.
- **Computational geometry.** Dadoun, Kirkpatrick and Walsh (1985) analyzed beam tracing with a hierarchical subdivision of space.

## When to use it

Use beam tracing when the scene is made of polygons and planar mirrors, the number of reflections is small, and an exact, resolution-independent answer is needed: acoustic simulation, the computation of visible sets, exact shadows from a point light (a beam from the light is a shadow volume), and the analysis of mirror rooms. Prefer [Whitted ray tracing](/whitted-ray-tracing/) for curved surfaces, many bounces, or scenes with millions of polygons, where the beams break into fragments that are smaller than pixels and the polygon operations cost more than the rays they replace.

## Pitfalls

- **Forgetting the window.** A reflected beam that does not clip to the far side of the mirror sees objects behind the mirror, between the mirror and the virtual apex.
- **Testing the mirror against its own reflection.** Exclude the polygon of the window from its child beam, or the beam finds the mirror at distance zero.
- **Cyclic overlap in 3D.** Polygons in space can overlap cyclically, so no front-to-back order exists. Split polygons first, as a BSP tree does. In the plane, disjoint segments always have an order; the implementation raises an error if the input breaks this.
- **Fragment explosion.** Each clip can split a beam into many pieces. Merge fragments of the same polygon that touch, and stop at a minimum fragment size.
- **Floating-point clipping.** Repeated polygon clipping in floating point creates slivers and cracks between fragments. Exact or carefully rounded arithmetic, as with rational numbers in the implementation, avoids this at a cost.
- **Wide beams.** A beam must be narrower than a half turn for the cross-section to be a simple polygon in one image plane. Split a wide beam, such as the view of a full panorama, into several beams.

## Implementations

## History

Whitted's ray tracer of 1980 traced one ray per pixel and spent most of its time in intersection tests. Heckbert and Hanrahan (1984) observed that neighboring rays usually hit the same polygons and proposed tracing beams instead. Their beam tracer clipped beams against polygons in depth order, built a beam tree, reflected beams from a virtual eye point, approximated refraction by a linear transformation, and rendered the tree with a polygon renderer. The same year Amanatides published [cone tracing](/cone-tracing/), which uses cones with circular cross-sections. Dadoun, Kirkpatrick and Walsh (1985) studied the geometry of beam tracing. Later work applied beams to the computation of potentially visible sets and, from 1998 on, to acoustic modeling.

## References
