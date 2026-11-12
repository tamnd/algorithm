---
tag: B0Q47Q
kind: concept
slug: ray-coherence
name: Ray coherence
aliases:
- spatial coherence of rays
area: graphics-and-signals/ray-tracing
level: core
summary: Rays with nearby origins and directions tend to visit the same nodes, test the same primitives and hit the same surfaces, so work and memory traffic can be shared among them.
prereqs: [ray-casting, bvh-traversal]
see_also: [ray-packet-tracing, visibility-coherence, amanatides-woo-traversal, beam-tracing, locality-of-reference, warp-divergence, z-order-curve, path-tracing]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the discussion of coherence, the general idea of which ray coherence is the ray tracing case
  - paper: doi:10.1145/37401.37409
    title: James Arvo and David Kirk, Fast ray tracing by ray classification, Computer Graphics 21(4) (SIGGRAPH 87), 1987
    locator: rays as points of a five-dimensional space of origins and directions, and the grouping of rays into beams that share candidate objects
  - paper: doi:10.1145/258734.258791
    title: Matt Pharr, Craig Kolb, Reid Gershbein and Pat Hanrahan, Rendering complex scenes with memory-coherent ray tracing, SIGGRAPH 97, 1997
    locator: the scheduling of ray computations by the region of the scene that they need, to reduce memory traffic
  - paper: doi:10.1111/1467-8659.00508
    title: Ingo Wald, Philipp Slusallek, Carsten Benthin and Markus Wagner, Interactive rendering with coherent ray tracing, Computer Graphics Forum 20(3) (Eurographics 2001), 2001, pages 153 to 165
    locator: the tracing of coherent rays in packets with SIMD instructions, and the memory layout that this makes possible
  - paper: doi:10.1145/1572769.1572792
    title: Timo Aila and Samuli Laine, Understanding the efficiency of ray traversal on GPUs, High Performance Graphics 2009, pages 145 to 149
    locator: the measurements of traversal speed for ray types of different coherence, from primary to diffuse rays
  - paper: doi:10.1145/1268517.1268547
    title: Solomon Boulos, Dave Edwards, J. Dylan Lacewell, Joe Kniss, Jan Kautz, Peter Shirley and Ingo Wald, Packet-based Whitted and distribution ray tracing, Graphics Interface 2007
    locator: the coherence of secondary rays and the behavior of packets for reflection, refraction and distribution ray tracing
---

Ray coherence is the tendency of rays with nearby origins and nearby directions to take similar paths through a scene: they visit the same nodes of an acceleration structure or the same cells of a grid, test the same primitives, and often hit the same surface. It is the ray tracing case of [visibility coherence](/visibility-coherence/). Primary rays through neighboring pixels of a pinhole camera are coherent, and so are shadow rays from neighboring points toward one point light. Rays after a diffuse bounce or a reflection from a bumpy surface have scattered directions and are incoherent. Coherence is a property of a set of rays and of the scene, not a guarantee: two rays through neighboring pixels can still split at the edge of a small object. Packet tracing, beam and cone tracing, ray classification and the reordering of rays all exploit it, and the gains that they get from it are measured on scenes, not proved.

## In plain words

Two people who stand side by side and look in almost the same direction see almost the same things. If you have to work out what each person sees, most of the work for the first person can be reused for the second.

Rays are the same. Rays from the camera through two neighboring pixels pass through the same parts of the scene and usually hit the same surface. A ray tracer can handle such rays as a group: check a box once for the whole group, or load a part of the scene into memory once for all of them.

After light bounces off a rough wall, the rays go in random directions. Then the group falls apart, each ray needs its own work, and the tracer is slower.

## The idea

**Rays as points.** A ray is a point of a five-dimensional space, three numbers for the origin and two for the direction, as Arvo and Kirk (1987) used. For a fixed scene and acceleration structure, the sequence of nodes or cells that a ray visits, and the primitive that it hits, are functions of this point. They are piecewise constant: they change only where the ray crosses a boundary of the structure, such as the face of a grid cell or of a bounding box, or the edge of a primitive. Two rays are coherent to the extent that no such boundary separates them over most of their length.

**Footprint against feature size.** Two rays from one eye at an angle $\delta$ are about $t \delta$ apart at distance $t$. They share a cell while this distance is small against the cell, and they hit the same primitive while it is small against the primitive. So coherence depends on the ratio of the spacing of the rays to the size of the features of the scene. A camera at a higher resolution has more coherent rays, while a scene with more, smaller triangles has less coherent ones.

**Measures.** Three numbers are common, and they measure different costs:

- the number of ray-node visits per distinct node visited by a group, which is the work that a group can share;
- the fraction of the rays of a group that are active at a node visit, which is the SIMD or [warp](/warp-divergence/) utilization;
- the number of distinct blocks of memory touched per ray, which is the cache behavior in the sense of [locality of reference](/locality-of-reference/).

**Where coherence comes from.** A common origin (the camera, a point light), similar directions (a pinhole view, a flat mirror, a distant light), and time (the same pixel in the next frame). **Where it goes.** Diffuse and glossy bounces, curved or bumpy mirrors and lenses, the random directions of [path tracing](/path-tracing/) after the first bounce, and rays of one group that stop at different depths.

**Getting it back.** When the rays are not coherent by their origin, a tracer can sort them so that similar rays are processed together: classify them by origin and direction (Arvo and Kirk), queue them by the region of the scene that they need next (Pharr et al. 1997), or sort them by a key on a [z-order curve](/z-order-curve/) of origin and direction. Sorting costs time, and pays off only when the rays share enough work afterward.

## Examples

**A grid.** The measurements below use the [Amanatides-Woo traversal](/amanatides-woo-traversal/) in an empty grid of $32 \times 32 \times 32$ unit cells, so that every ray runs until it leaves the grid. A camera at $(16, 16, -20)$ with a $60°$ view and $256 \times 256$ pixels shoots primary rays. Each row averages 40 groups.

| group of rays | rays | cell visits | distinct cells | visits per distinct cell |
|---|---|---|---|---|
| one pixel | 1 | 32.0 | 32.0 | 1.0 |
| $2 \times 2$ neighboring pixels | 4 | 121.8 | 39.0 | 3.1 |
| $4 \times 4$ neighboring pixels | 16 | 505.0 | 59.1 | 8.5 |
| $8 \times 8$ neighboring pixels | 64 | 2133.5 | 119.6 | 17.8 |
| $16 \times 16$ neighboring pixels | 256 | 8805.4 | 296.9 | 29.7 |
| 16 random pixels | 16 | 485.4 | 480.8 | 1.01 |
| 16 diffuse rays from one cell | 16 | 409.6 | 370.1 | 1.11 |
| 16 random rays | 16 | 339.6 | 338.0 | 1.005 |

A $4 \times 4$ tile of neighboring pixels needs only 59 distinct cells for 505 visits, so each cell that the group loads serves 8.5 rays on average. The same 16 rays at random pixels share almost nothing. Rays that start in one cell but go in random directions, as after a diffuse bounce, share only the first few cells. Larger tiles share more in total but less per ray, because the rays at the edges of a large tile diverge.

**A BVH.** The page on [ray packet tracing](/ray-packet-tracing/) measures the same effect in a BVH over a height field: $4 \times 4$ tiles of primary rays need 446 node visits where single rays need 4114, while 16 random rays per packet need 1414.

**Shadow rays.** Shadow rays from the hit points of neighboring pixels toward a point light have nearby origins and converge to one point, so they are coherent where the hit points are on one surface, and they lose coherence at the silhouettes where neighboring hits are far apart.

## Where it is used

- **Packet tracing.** [Ray packet tracing](/ray-packet-tracing/) traces groups of coherent rays together, so that one node fetch and one SIMD instruction serve several rays (Wald et al. 2001).
- **Beams and cones.** [Beam tracing](/beam-tracing/) and [cone tracing](/cone-tracing/) replace a set of coherent rays by one volume and compute its visibility once.
- **Ray classification.** Arvo and Kirk (1987) partition the five-dimensional space of rays and keep, for each part, the objects that its rays can hit.
- **Scenes larger than memory.** Pharr et al. (1997) reorder the work of many rays so that rays that need the same part of the scene are processed while that part is in memory.
- **GPU traversal.** Rays of one warp that take different paths cause [warp divergence](/warp-divergence/) and scattered memory accesses. Aila and Laine (2009) measured traversal speed separately for ray types of different coherence and found incoherent rays much slower.
- **Secondary rays.** Boulos et al. (2007) studied how much coherence the reflection, refraction and distribution rays of a packet keep, and when packets still pay off for them.

## References
