---
tag: K15JXV
kind: problem
slug: visibility-culling
name: Visibility culling
aliases:
- visibility determination for rendering
area: graphics-and-signals/visibility
level: core
summary: Discard scene objects that cannot contribute to the rendered image before rasterization.
prereqs: [hidden-surface-removal, bounding-volume, graphics-pipeline]
see_also: [back-face-culling, frustum-culling, occlusion-culling, portal-culling, potentially-visible-set, visibility-coherence, hierarchical-z-buffer, occlusion-query]
sources:
  - paper: doi:10.1109/TVCG.2003.1207447
    title: Daniel Cohen-Or, Yiorgos L. Chrysanthou, Cláudio T. Silva and Frédo Durand, A survey of visibility for walkthrough applications, IEEE Transactions on Visualization and Computer Graphics 9(3), 2003
    locator: the statement of the problem, the conservative, aggressive, approximate and exact classes, and the from-point and from-region methods
  - paper: doi:10.1145/360349.360354
    title: James H. Clark, Hierarchical geometric models for visible surface algorithms, Communications of the ACM 19(10), 1976, pages 547 to 554
    locator: the hierarchy of bounding volumes and the culling of whole subtrees against the view volume
  - paper: doi:10.1145/91385.91416
    title: John M. Airey, John H. Rohlf and Frederick P. Brooks Jr., Towards image realism with interactive update rates in complex virtual building environments, Proceedings of the 1990 Symposium on Interactive 3D Graphics, Computer Graphics 24(2), pages 41 to 50
    locator: the precomputed potentially visible sets of the cells of a building
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19, Section 19.2 (Culling Techniques), page 830, and Sections 19.3 to 19.7
---

Visibility culling is the problem of finding, before the expensive part of rendering, a small set of scene objects that includes each object that can appear in the image. The renderer then draws only that set, and a [z-buffer](/z-buffer/) or another [hidden surface removal](/hidden-surface-removal/) method decides the final visibility. The answer does not have to be exact. A *conservative* answer may keep some hidden objects but never drops a visible one. The goal is a cost that depends on the number of visible objects, not on the size of the scene. Clark in 1976 gave the base of most methods: a hierarchy of bounding volumes, so that one test can remove a whole group of objects.

## In plain words

A game level can have millions of triangles, but from any one place you see only a small part of them. Most are behind you, outside the edges of the screen, behind a wall, or on the far side of an object. Drawing them all costs time, and none of them change the picture.

Visibility culling is the job of finding the things that are surely not in the picture, quickly, and skipping them. It is acceptable to draw a few things that end up hidden, because the depth buffer hides them later. It is not acceptable to skip something that you can see, because then it disappears from the picture.

## Definition

**Input.** A scene of $n$ objects, each with a [bounding volume](/bounding-volume/). A view: an eye point, a view frustum and the resolution of the image. In some variants, also a region $R$ of eye points, or the depth buffer of the objects that are already drawn.

**Visible objects.** An object $o$ is *visible* when at least one sample of the image sees it: the ray from the eye through the sample center is inside the frustum, meets $o$, and meets no other object nearer to the eye. Let $V$ be the set of visible objects. For a region $R$, $V(R)$ is the union of the sets $V$ for all eye points in $R$.

**Output.** A set $K$ of objects to draw. The answer is

- *exact* when $K = V$;
- *conservative* when $K \supseteq V$;
- *aggressive* when $K \subseteq V$, so that no hidden object is drawn but some visible objects can be missed;
- *approximate* when $K$ can differ from $V$ in both directions, usually by objects that cover few pixels.

**The cost.** The cost of a frame is the cost to compute $K$ plus the cost to draw $K$. The set $K = $ all objects is conservative and costs nothing to compute, so the problem is not to find a conservative set but to find a good one fast. A method is *output sensitive* when its time is a function of $|V|$, or of $|K|$, more than of $n$.

## Variants

- **By the reason that an object is hidden.** It faces away from the eye: [back-face culling](/back-face-culling/). It is outside the view volume: [frustum culling](/frustum-culling/). Other objects hide it: [occlusion culling](/occlusion-culling/). The walls of a building hide it, and only the openings let the view through: [portal culling](/portal-culling/). It covers less than a pixel: detail culling, which is approximate.
- **From a point or from a region.** From-point methods run for each frame at the current eye. From-region methods run once, before run time, for each cell of the space, and store a [potentially visible set](/potentially-visible-set/) for each cell.
- **Object precision or image precision.** A method can test bounding volumes against planes and other geometry, or it can test them against a depth buffer, for example with a [hierarchical z-buffer](/hierarchical-z-buffer/) or [occlusion queries](/occlusion-query/).
- **Static or dynamic scenes.** A precomputed set is valid only while the occluders do not move. Per-frame methods handle moving objects.
- **Occluder fusion.** Two objects can together hide an object that neither of them hides alone. Methods that test one occluder at a time miss this, and they keep more objects.
- **From the light.** For shadow maps and shadow volumes, the set of objects that can cast a shadow into the visible part of the scene is a culling problem from the light.

## Examples

**A small scene in the plane.** The eye is at the origin and looks along $+z$. The frustum is the wedge $|x| \le z$, so the image is the range $-1 \le x/z \le 1$ of directions. The objects are boxes $[x_1, x_2] \times [z_1, z_2]$:

| object | box | directions $x/z$ | status |
|---|---|---|---|
| $A$ | $[-1, 1] \times [2, 3]$ | $[-\tfrac12, \tfrac12]$ | visible |
| $B$ | $[-\tfrac12, \tfrac12] \times [6, 7]$ | $[-\tfrac1{12}, \tfrac1{12}]$ | hidden behind $A$ |
| $C$ | $[10, 11] \times [2, 3]$ | $[\tfrac{10}{3}, \tfrac{11}{2}]$ | outside the frustum |
| $D$ | $[4, 5] \times [5, 6]$ | $[\tfrac23, 1]$ | visible |
| $E$ | $[-4, -3] \times [3, 4]$ | $[-\tfrac43, -\tfrac34]$ | visible in $[-1, -\tfrac34]$ |

Each ray toward $B$ has $|x/z| \le \tfrac1{12}$. It meets the front side $z = 2$ of $A$ at $|x| \le \tfrac16 < 1$, so it hits $A$ first. So $V = \{A, D, E\}$.

- Frustum culling of the boxes gives $K = \{A, B, D, E\}$. This is conservative.
- Occlusion culling with $A$ as the occluder then removes $B$ and gives $K = V$, which is exact.
- A method that sends one ray to the center of each of 8 equal parts of the image samples the directions $\pm\tfrac18, \pm\tfrac38, \pm\tfrac58, \pm\tfrac78$. It finds $E$ at $-\tfrac78$ and $D$ at $\tfrac78$. With only 4 parts, the directions are $\pm\tfrac14$ and $\pm\tfrac34$. The direction $-\tfrac34$ is at the edge of $E$, so a strict test misses $E$, and the result $\{A, D\}$ is aggressive, which is wrong.

**A building.** In a model of an office floor with 100 rooms, from a room you can see the room itself, the corridor, and a few rooms whose doors line up. Portal culling or a potentially visible set draws a few rooms out of 100, and the frame cost goes down by about the same factor.

**A city at street level.** Most buildings are hidden by the street fronts near the eye. There are no portals, so occlusion culling with large nearby occluders does the work.

## Known algorithms

| method | year | kind | idea |
|---|---|---|---|
| [Back-face culling](/back-face-culling/) | 1963 | per face, exact for convex solids | one sign test against the face normal |
| [Frustum culling](/frustum-culling/) | 1976 | per object, conservative | test the bounding volumes of a hierarchy against the frustum planes |
| [Potentially visible set](/potentially-visible-set/) | 1990 | from region, precomputed | a stored set for each cell of a subdivision |
| [Hierarchical z-buffer](/hierarchical-z-buffer/) | 1993 | image precision, conservative | a depth pyramid and an octree of the scene |
| [Portal culling](/portal-culling/) | 1995 | per frame, conservative | walk the cells and portals and shrink the view through each portal |
| [Occlusion culling](/occlusion-culling/) | 1990s | per frame, conservative | test the bounding volumes against the depth of the drawn occluders, for example with [occlusion queries](/occlusion-query/) |

Teller and Séquin in 1991 computed exact potentially visible sets at the level of cells. Luebke and Georges in 1995 did portal culling at run time with screen rectangles. Bittner and others in 2004 made hardware occlusion queries practical with coherent hierarchical culling, which uses [visibility coherence](/visibility-coherence/) between frames.

## Bounds

- **Lower bound.** Each method must output each visible object, so its time is $\Omega(|V|)$ for each frame.
- **Hierarchical culling.** With a [bounding volume hierarchy](/bounding-volume-hierarchy/), frustum culling costs $O(1)$ for each node whose box straddles a frustum plane, $O(1)$ for each child of such a node, and $O(|K|)$ for the subtrees that are wholly inside. When few boxes straddle the planes, this is close to $O(|K|)$. In the worst case, many boxes straddle the planes, and the cost is $\Theta(n)$.
- **Exact visibility is the full problem.** An exact answer at image precision gives the set of objects that appear in the hidden surface removal output. So exact culling is at least as hard as reporting which objects the visibility map contains. This is why practical methods are conservative.
- **Space for from-region sets.** A table with one bit for each pair of $c$ cells takes $c^2$ bits before compression.

## Reductions

- **To hidden surface removal.** Run a z-buffer that writes the object number at each pixel (an *item buffer*), and read the set of numbers that it contains. The result is exact at image precision, but the cost is that of drawing all objects, so it is useful only as a reference or with coarse proxies.
- **To range searching.** Frustum culling is a range query with a convex polytope over the bounding volumes of a [bounding volume hierarchy](/bounding-volume-hierarchy/), and the traversal is a [BVH traversal](/bvh-traversal/).
- **To line stabbing.** From-region visibility between cells through a chain of portals asks for a line that passes through each portal. In the plane, this is a linear feasibility problem in two variables.
- **To depth tests.** Occlusion culling against a depth buffer asks, for each box, whether the depth at each covered pixel is nearer than the nearest point of the box. This is an [early depth test](/early-depth-test/) for a whole object.

## Applications

Visibility culling is part of each real-time renderer of large scenes: games, flight and driving simulators, walkthroughs of buildings and city models, and CAD viewers for large assemblies. The same sets decide what to load or stream from disk or a network near the viewer, and, in networked games, which objects a client must be told about. Shadow rendering uses culling from the light to limit the shadow casters. Offline renderers use the same bounding volume hierarchies to skip work, but in the form of ray queries.

## References
