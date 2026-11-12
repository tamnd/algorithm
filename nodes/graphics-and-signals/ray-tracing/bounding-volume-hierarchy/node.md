---
tag: NZ1MVD
kind: data-structure
slug: bounding-volume-hierarchy
name: Bounding volume hierarchy
aliases: [BVH]
area: graphics-and-signals/ray-tracing
level: core
summary: A tree over primitives in which each node stores a bounding volume of all the primitives below it and each primitive is in one leaf. Rays and queries skip subtrees whose volume they miss.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of primitives, h: the height of the tree}
  time: {build: O(n log n), closest_hit: O(n), any_hit: O(n), refit: Θ(n)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1976
  people: [James H. Clark, Steven M. Rubin, Turner Whitted, Timothy L. Kay, James T. Kajiya]
  note: Clark proposed hierarchies of bounding volumes for visible surface algorithms in 1976. Rubin and Whitted (1980) and Kay and Kajiya (1986) used them to ray trace complex scenes.
prereqs: [axis-aligned-bounding-box, slab-method, binary-tree]
see_also: [bvh-construction, bvh-traversal, bvh-refitting, surface-area-heuristic, lbvh-construction, kd-tree-traversal, bounding-interval-hierarchy, r-tree]
sources:
  - paper: doi:10.1145/360349.360354
    title: James H. Clark, Hierarchical geometric models for visible surface algorithms, Communications of the ACM 19(10), 1976, 547 to 554
    locator: the hierarchy of objects with bounding volumes, and the pruning of a subtree whose volume is not visible
  - paper: doi:10.1145/965105.807479
    title: Steven M. Rubin and Turner Whitted, A 3-dimensional representation for fast rendering of complex scenes, SIGGRAPH 1980, Computer Graphics 14(3), 110 to 116
    locator: the ray tracing of a hierarchy of bounding volumes
  - paper: doi:10.1145/15886.15916
    title: Timothy L. Kay and James T. Kajiya, Ray tracing complex scenes, SIGGRAPH 1986, Computer Graphics 20(4), 269 to 278
    locator: the slab volumes, the build of the hierarchy, and the traversal in the order of entry distance
  - paper: doi:10.1109/MCG.1987.276983
    title: Jeffrey Goldsmith and John Salmon, Automatic creation of object hierarchies for ray tracing, IEEE Computer Graphics and Applications 7(5), 1987, 14 to 20
    locator: the cost estimate of a hierarchy from the surface areas of its volumes, and the build by insertion
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Primitives and Intersection Acceleration, Section 4.3 Bounding Volume Hierarchies (the build, the compact depth-first layout and the traversal)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 6, Bounding Volume Hierarchies
---

A bounding volume hierarchy (BVH) is a tree over a set of geometric primitives, for example the triangles of a scene. Each leaf holds a few primitives, each primitive is in exactly one leaf, and each node stores a [bounding volume](/bounding-volume/), usually an [axis-aligned box](/axis-aligned-bounding-box/), that contains all the primitives below it. A query that misses the box of a node skips the whole subtree. It is the standard acceleration structure for ray tracing and a common broad phase for collision detection.

## In plain words

Suppose you look for the first object that a laser beam hits in a large warehouse. You could test the beam against every object, one by one. Instead, put the objects of each shelf in a cardboard box, the shelves of each aisle in a crate, and the aisles in containers. Now test the beam against the containers first. If it misses a container, it misses every aisle, shelf and object in it, so you skip all of them with one test.

A BVH is this nesting of boxes. Each object goes in one box only, so the boxes can overlap, but nothing is counted twice. A good BVH has small boxes that do not overlap much. When objects move, you can keep the nesting and only make the boxes bigger or smaller again.

## The abstract type

A BVH implements a static [spatial index](/spatial-index/) over $n$ primitives. The operations used in rendering are:

- BUILD$(P)$: make the tree for the primitive set $P$.
- CLOSEST-HIT$(T, r)$: the primitive that the ray $r$ meets first, with its parameter $t$, which answers the [closest-hit query](/closest-hit-query/).
- ANY-HIT$(T, r, t_{max})$: whether the ray meets some primitive with $t \le t_{max}$, which answers the [any-hit query](/any-hit-query/) for shadow rays.
- REFIT$(T)$: recompute the volumes after the primitives move, with the same tree.

Collision code uses the window and overlap queries of the spatial index on the same tree. Insert and delete exist in dynamic variants, but most renderers rebuild or refit instead.

## Representation

A node has a box $[lo, hi]$. An inner node has two children. A leaf has a range $[first, first + count)$ into an array $refs$ of primitive indices. The tree is stored in one array in depth-first order: the left child of node $i$ is node $i + 1$ and the node stores only the index of its right child. This layout is the one in PBRT. It puts each node next to its left child in memory and needs no pointer to it.

The invariant has two parts.

- **(B) Bounds.** The box of each node contains each primitive in its subtree. A built tree has tight boxes, equal to the union of the children's boxes, but correctness needs only containment.
- **(P) Partition.** The leaf ranges partition $refs$, and $refs$ is a permutation of the primitive indices, so each primitive is in exactly one leaf.

A BVH partitions the objects, not the space: two sibling boxes can overlap, and a point of space can be in many leaves. A [kd-tree](/kd-tree/) or [BSP tree](/bsp-tree/) partitions space, and a primitive that crosses a plane is referenced on both sides. This difference shapes all the operations. A BVH has at most $2n - 1$ nodes and a known memory size, but its traversal cannot stop at the first hit in front to back order, because a later box can overlap an earlier one. [Spatial splits](/spatial-splits/) relax (P) to make boxes smaller.

## Operations

BUILD splits top down. The version here uses the object median on the longest axis of the box of the centroids. The [SAH build](/bvh-construction/) and the [LBVH build](/lbvh-construction/) choose better or faster splits, with the same output form.

```pseudo id=main
BUILD(P, L)                                 ▷ P: n primitives; leaves hold at most L
L1  refs ← [0, 1, ..., n − 1]
L2  stack ← [(0, n)]; while stack is not empty do pop (first, count)
L3      make node v with box = ∪ of the boxes of refs[first .. first + count − 1]
L4      if count ≤ L then v is a leaf with this range; continue
L5      a ← the longest axis of the box of the centroids of the range
L6      sort the range by the centroid coordinate a
L7      push (first + ⌊count/2⌋, count − ⌊count/2⌋) as the right child of v
L8      push (first, ⌊count/2⌋) as the left child of v
```

The left child is pushed last, so it is popped next and gets the index after its parent. If all centroids of a range are equal, no split separates them, and the range stays a leaf.

```pseudo id=closest
CLOSEST-HIT(T, o, d)                        ▷ the ray o + t d, t ≥ 0
L9  best ← none, tmax ← +∞, stack ← [root]
L10 while stack is not empty do pop v
L11     if the box of v misses the ray on [0, tmax] then continue        ▷ slab method
L12     if v is a leaf then for each primitive p of v do
L13         if p is hit at t ≤ tmax and t is less than best then best ← (t, p), tmax ← t
L14     else push the right child, then the left child
L15 return best
```

Line L11 uses the [slab method](/slab-method/) with the current $t_{max}$, so a box that lies wholly beyond the best hit so far is skipped. ANY-HIT is the same loop with a fixed $t_{max}$ that returns true at the first hit at line L13. [BVH traversal](/bvh-traversal/) adds the ordering of the children by distance and the costs.

```pseudo id=refit
REFIT(T)
L16 for i ← |T| − 1 down to 0 do                ▷ children come after parents
L17     if node i is a leaf then box(i) ← ∪ of the boxes of its primitives
L18     else box(i) ← box(left(i)) ∪ box(right(i))
```

Each node is done after its children because the depth-first order puts children at larger indices. [BVH refitting](/bvh-refitting/) discusses when refitting is enough and when to rebuild.

## Example

Four triangles lie in the plane $z = 0$. Triangle $i$ has the corners $(3i, 0, 0)$, $(3i + 2, 0, 0)$ and $(3i, 2, 0)$, so it spans $x \in [3i, 3i + 2]$. BUILD with $L = 1$ splits on x, the longest axis of the centroid box, each time.

| node | range of refs | box in x | box in y and z | kind |
|---|---|---|---|---|
| 0 | 0, 1, 2, 3 | [0, 11] | [0, 2], [0, 0] | inner, children 1 and 4 |
| 1 | 0, 1 | [0, 5] | [0, 2], [0, 0] | inner, children 2 and 3 |
| 2 | 0 | [0, 2] | [0, 2], [0, 0] | leaf |
| 3 | 1 | [3, 5] | [0, 2], [0, 0] | leaf |
| 4 | 2, 3 | [6, 11] | [0, 2], [0, 0] | inner, children 5 and 6 |
| 5 | 2 | [6, 8] | [0, 2], [0, 0] | leaf |
| 6 | 3 | [9, 11] | [0, 2], [0, 0] | leaf |

All boxes are flat in z. CLOSEST-HIT for the ray $o = (6, 1, 5)$, $d = (0, 0, -1)$:

| step | pop | box test (L11) | action | best |
|---|---|---|---|---|
| 1 | 0 | hit at $t = 5$ | push 4, 1 | none |
| 2 | 1 | miss, $x = 6 \notin [0, 5]$ | skip | none |
| 3 | 4 | hit at $t = 5$ | push 6, 5 | none |
| 4 | 5 | hit at $t = 5$ | test triangle 2: hit at $t = 5$ | (5, 2) |
| 5 | 6 | miss, $x = 6 \notin [9, 11]$ | skip | (5, 2) |

The query made five box tests and one triangle test, against four triangle tests for a linear scan. The ray from $(8, 1, 5)$ in the same direction goes into the box of node 5 but misses triangle 2, because $(8 - 6) + 1 > 2$: a box hit does not imply a primitive hit.

## Correctness

The invariant (B) and (P) is kept by each operation. BUILD writes each box as the union of the boxes of the primitives of its range, so (B) holds with tight boxes, and the two children split the range of their parent, so (P) holds by induction. REFIT recomputes each box from its children or its primitives after them, so (B) holds again for the moved primitives, and it does not change the ranges.

CLOSEST-HIT returns a primitive with the least $t$. A subtree is skipped at line L11 only if the ray on $[0, t_{max}]$ misses its box; by (B) each primitive in it has no hit with $t \le t_{max}$, so none of them can beat the current best. Every other primitive is tested at line L13, so the minimum is found. The full proof, with ANY-HIT and REFIT, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/). A box test and a primitive test cost $O(1)$ each.

- **Build.** The version above sorts each range, which costs $O(m \log m)$ at a node with $m$ primitives. The median split halves the ranges, so the height is $h = \lceil \lg n \rceil$ for $L = 1$, the ranges at one depth are disjoint, and the total is $O(n \log^2 n)$. With a linear-time median ([quickselect](/quickselect/) or a deterministic selection) it is $O(n \log n)$. The binned SAH build is $O(n \log n)$.
- **Closest hit and any hit.** In the worst case a query visits all $2n - 1$ nodes and tests all $n$ primitives, so it is $O(n)$. Take $n$ triangles in parallel planes, each with corners $(0, 0, z)$, $(10, 0, z)$ and $(10, 10, z)$. The ray along the z axis through $(1, 9)$ is inside every box and meets no triangle, so no subtree is skipped. On typical scenes with a good build the number of visits grows slowly with $n$, close to logarithmic, but that is an observation, not a bound.
- **Refit.** One pass over the nodes: $\Theta(n)$.
- **Space.** At most $2n - 1$ nodes and $n$ entries of $refs$: $\Theta(n)$. The memory size is known before the build, unlike for a kd-tree.

| operation | time | case |
|---|---|---|
| build | $O(n \log^2 n)$ | worst, median split with a sort per node |
| build | $O(n \log n)$ | worst, with linear-time median or binned SAH |
| closest_hit, any_hit | $O(n)$ | worst; close to logarithmic visits observed on typical scenes |
| refit | $\Theta(n)$ | worst |
| space | $\Theta(n)$ | total, at most $2n - 1$ nodes |

## Variants

- **The build.** Object median (above), the [surface area heuristic](/surface-area-heuristic/) with a full sweep or with bins ([BVH construction](/bvh-construction/)), the linear BVH from [Morton codes](/morton-encoding/) ([LBVH construction](/lbvh-construction/)), and bottom-up agglomerative clustering. Goldsmith and Salmon (1987) built by insertion, which is the dynamic variant.
- **Spatial splits.** The SBVH of Stich, Friedrich and Dietrich (2009) lets a primitive be in more than one leaf when that makes the boxes much smaller; see [spatial splits](/spatial-splits/).
- **The bounding volume.** Boxes are the norm. Spheres are cheaper to test but fit badly, oriented boxes fit better but cost more, and Kay and Kajiya used slab volumes with more than three normals. See [bounding volume](/bounding-volume/).
- **Wide BVH.** Nodes with 4 or 8 children, so that one SIMD instruction tests a ray against all the child boxes. They are made by collapsing a binary BVH.
- **Compressed nodes.** Child boxes stored with a few bits per coordinate relative to the parent box, rounded outward so that (B) still holds.
- **Two levels.** A top-level BVH over instances, each with a bottom-level BVH in its own frame; see [object instancing](/object-instancing/).
- **Close relatives.** The [bounding interval hierarchy](/bounding-interval-hierarchy/) stores only two planes per node. The [R-tree](/r-tree/) is a BVH with a high branching factor, balanced and built for disk pages and window queries in databases.

## When to use it

Use a BVH for ray tracing of triangle meshes, for collision detection between models, and for the culling of objects in a renderer ([frustum culling](/frustum-culling/)). Against a kd-tree, a BVH has a bounded size, a simpler build, cheap refitting for animated meshes, and an easy GPU build; a kd-tree can stop at the first hit in its front to back order and has no overlap. Against a [uniform grid](/uniform-grid/), a BVH adapts to scenes with very uneven density, the teapot in a stadium case; a grid is faster to build and to walk on uniform scenes. For points and nearest neighbor search, use a [kd-tree](/kd-tree/).

## Pitfalls

- **A box that does not contain its primitives.** Line L3 or L17 must take the union over all primitives of the range, in all three axes. A box computed only from the vertices that moved, or from the centroids, breaks (B), and rays then miss geometry near the edges of boxes.
- **Stopping at the first hit.** Line L13 must keep going and shrink $t_{max}$, not return. Sibling boxes overlap, so a primitive in a box that is popped later can still be closer.
- **The wrong $t_{max}$ in line L11.** Testing the box on $[0, +\infty)$ instead of $[0, t_{max}]$ is correct but visits all boxes behind the best hit.
- **Splitting a range whose centroids coincide.** Line L5 has no axis with extent if all centroids are equal. A build that still splits at the median makes children with equal boxes, and a build that splits at the spatial middle makes one empty child and never stops. Make a leaf.
- **Recursion depth.** A bad split can make the tree as deep as $n$. Use explicit stacks for the build and the traversal, as here, and size the traversal stack by the height of the tree.
- **Floating-point boxes.** Boxes computed in floats from transformed vertices must be rounded outward, and the box test must be the conservative version of the [slab method](/slab-method/), or the traversal can lose primitives that touch the edge of a box.

## Implementations

## History

Clark (1976) proposed hierarchies of objects with bounding volumes for visible surface algorithms, so that a renderer could reject a large part of the scene with one test. Rubin and Whitted (1980) ray traced such hierarchies, and Weghorst, Hooper and Greenberg (1984) studied the choice of volumes. Kay and Kajiya (1986) introduced slab volumes and the traversal in order of entry distance. Goldsmith and Salmon (1987) gave the first cost estimate of a hierarchy from the surface areas of its volumes, the start of the [surface area heuristic](/surface-area-heuristic/), and built hierarchies automatically. Fast SAH builds (Wald 2007), spatial splits (Stich, Friedrich and Dietrich 2009) and parallel builds from Morton codes (Lauterbach et al. 2009, Karras 2012) made the BVH the structure of choice in production and GPU ray tracing.

## References
