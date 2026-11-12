---
tag: 5ASM9T
kind: technique
slug: bvh-refitting
name: BVH refitting
aliases: [bounding volume refit]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Recompute the boxes of a BVH after its primitives move and keep the shape of the tree, in one bottom-up pass of unions in O(n) time, while the quality of the tree decays until a rebuild.
prereqs: [bounding-volume-hierarchy, axis-aligned-bounding-box]
see_also: [bvh-construction, lbvh-construction, surface-area-heuristic, bvh-traversal, collision-detection, object-instancing, kd-tree-traversal, loose-octree]
sources:
  - paper: doi:10.1145/1189762.1206075
    title: Ingo Wald, Solomon Boulos and Peter Shirley, Ray tracing deformable scenes using dynamic bounding volume hierarchies, ACM Transactions on Graphics 26(1), 2007, article 6
    locator: the refit of the BVH of a deformable scene in each frame, and the loss of quality when the motion is not coherent
  - paper: doi:10.1080/10867651.1997.10487480
    title: Gino van den Bergen, Efficient collision detection of complex deformable models using AABB trees, Journal of Graphics Tools 2(4), 1997, 1 to 13
    locator: the bottom-up refit of an AABB tree after a deformation, much faster than a rebuild, and its use for collision detection
  - paper: doi:10.1145/2159616.2159649
    title: Daniel Kopta, Thiago Ize, Josef Spjut, Erik Brunvand, Al Davis and Andrew Kensler, Fast, effective BVH updates for animated scenes, ACM Symposium on Interactive 3D Graphics and Games 2012, 197 to 204
    locator: refitting with local tree rotations that lower the SAH cost, to slow the decay of the tree
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 6, on bounding volume hierarchies, including the update of a hierarchy of a deforming object
---

**BVH refitting** updates a [bounding volume hierarchy](/bounding-volume-hierarchy/) after its primitives move. It keeps the shape of the tree and the primitives in each leaf, and only recomputes the boxes: each leaf gets the box of its primitives at their new positions, and each internal node gets the union of the boxes of its two children, in an order with the children first. This is one pass over the nodes, $O(n)$ for $n$ primitives, and much faster than a [new build](/bvh-construction/). The result is a correct BVH: every box contains everything below it, so [BVH traversal](/bvh-traversal/) gives the right answers. But the tree was chosen for the old positions, so when primitives that were close move apart, the boxes grow and overlap, and the [SAH cost](/surface-area-heuristic/) rises. A renderer or a physics engine therefore refits for small changes and rebuilds when the cost has grown too much.

## In plain words

Think of a set of nested bags. Each small bag holds a few objects, and each bigger bag holds two smaller bags. When the objects move, you do not repack the bags. You make each small bag just large enough for its objects at their new places, and then each bigger bag just large enough for its two smaller bags.

This is fast, and the bags still hold everything. But if two objects in the same bag move to opposite ends of the room, that bag becomes as large as the room. After much motion of this kind, many bags are large, and a search must open most of them. Then it is better to pack the bags again from the start.

## When it applies

- The structure is a hierarchy of bounding volumes in which the volume of a node can be computed from the volumes of its children, as the union of [axis-aligned boxes](/axis-aligned-bounding-box/) can.
- The primitives move or deform, but no primitive is added or removed. A change in the set of primitives needs an insert or a delete, or a rebuild.
- The motion is coherent: primitives that are close at one time are mostly close at the next, as in a character that bends or a cloth that folds. Then the old grouping stays good.
- The time per frame is short, and a rebuild costs more than the extra time that the worse tree adds to the queries. If many rays are traced per frame, a rebuild can pay for itself.

## The template

The holes are BOUND, the box of one primitive at its new position; MERGE, the volume that bounds two volumes; an order of the nodes in which each child comes before its parent; COST, a measure of the quality of the tree; and the threshold $\rho \ge 1$.

```pseudo id=main
REFIT(T, P)                                   ▷ T: a BVH of fixed shape, P: the primitives at their new positions
L1  for each primitive p: b(p) ← BOUND(p)
L2  for each node v of T, in an order with the children before the parents, do
L3      if v is a leaf then B(v) ← MERGE of b(p) over the primitives p of v
L4      else B(v) ← MERGE(B(left(v)), B(right(v)))
L5  if COST(T) > ρ · the cost of T after its last build then rebuild T
```

If the nodes are stored with each parent before its children, as a top-down builder makes them, line L2 is the loop over the array in reverse order. A tree from an [LBVH build](/lbvh-construction/) has no such order; there, line L2 is the walk up from every leaf with a counter per node, as in the last line of that build. For boxes, MERGE is the union, and the refitted box of each node is then the tight box of all the primitives below it, by induction from the leaves: the union of the tight boxes of two sets is the tight box of their union. So the boxes are the same as those that a new build with the same shape would give, and only the shape is old.

The cost of lines L1 to L4 is $O(n)$, since a tree with $n$ primitives and nonempty leaves has at most $2n - 1$ nodes. Line L5 with the SAH costs $O(n)$ more, the sum over the nodes of the area times the cost of the node.

The implementation stores the nodes of a binned SAH build in one array, refits on random scenes after random motion, and checks that the shape is kept, that each box is the tight box of the triangles below it, that the root equals the root of a new build, that a refit of only the moved paths gives the same boxes as the full refit, and that closest-hit and any-hit answers equal a brute force over all triangles. It also checks that a refit without motion gives back the boxes of the build.

**Example.** Four triangles have the unit boxes $[c, c + 1] \times [0, 1] \times [0, 1]$, each of area 6, for $c = 0, 1, 10, 11$. The SAH build with leaves of one triangle puts the first two into one child and the last two into the other. Then triangles 1 and 2 change places: triangle 1 moves to $c = 10$ and triangle 2 to $c = 1$. The SAH cost uses $c_t = c_i = 1$, and the root box $[0, 12] \times [0, 1] \times [0, 1]$ has area 50 in all three trees.

| tree | left child box | right child box | SAH cost |
|---|---|---|---|
| the build, before the motion | $[0, 2]$ in $x$, area 10 | $[10, 12]$ in $x$, area 10 | $(50 + 10 + 10 + 4 \cdot 6)/50 = 1.88$ |
| the refit, after the motion | $[0, 11]$ in $x$, area 46 | $[1, 12]$ in $x$, area 46 | $(50 + 46 + 46 + 4 \cdot 6)/50 = 3.32$ |
| a new build, after the motion | $[0, 2]$ in $x$, area 10 | $[10, 12]$ in $x$, area 10 | $1.88$ |

After the refit, each child covers almost the whole scene, so a ray that enters the root nearly always enters both children. With $\rho = 3/2$, line L5 asks for a rebuild, since $3.32 > 1.5 \cdot 1.88$. The tests also follow 60 small triangles through 12 steps of random motion with the seed 3: the ratio of the refitted cost to the cost of a new build goes from about 1.08 after one step to about 1.53 after 12.

## Classic examples

- **Ray tracing deformable scenes.** Wald, Boulos and Shirley (2007) refit the BVH of an animated mesh in each frame and trace packets of rays through it with [BVH traversal](/bvh-traversal/), since the shape of a character changes far less than the positions of its triangles.
- **Collision detection of deformable models.** Van den Bergen (1997) showed that an AABB tree of a deforming mesh can be refit much faster than rebuilt, which made AABB trees the usual choice for deformable models in [collision detection](/collision-detection/).
- **Two-level scenes.** With [object instancing](/object-instancing/), a renderer keeps one BVH per object and a top BVH over the instances. Objects that move rigidly need only new transforms, objects that deform get a refit, and the small top BVH is rebuilt in each frame.
- **The box pass of LBVH.** The last line of the [LBVH build](/lbvh-construction/) is a refit of a tree whose shape came from the Morton order.
- **Not for kd-trees.** A kd-tree for [kd-tree traversal](/kd-tree-traversal/) stores planes and puts a primitive into every cell it meets, so a motion changes which cells hold it, and there is no refit that keeps the structure. This is one reason why BVHs replaced kd-trees for dynamic scenes.

## Variations

- **Refitting only the moved paths.** If only $k$ primitives move, walk up from the leaf of each one and stop at a node whose box does not change. The cost is $O(k h)$ for a tree of height $h$. This is correct only when all boxes were tight before; the tests compare it with the full refit.
- **Tree rotations.** Kopta et al. (2012) combine the refit with local changes of the shape: at a node, a grandchild is swapped with its uncle if that lowers the SAH cost. This slows the decay at a small extra cost.
- **Rebuild triggers.** Line L5 can also rebuild after a fixed number of frames, or when the sum of the areas of the boxes has grown by a factor. A rebuild can also run in the background while the refitted tree is in use.
- **Partial rebuilds.** Rebuild only the subtrees whose cost grew most, and refit the rest.
- **Boxes over an interval of time.** For motion blur, a leaf box is the union of the boxes at the start and at the end of the frame. If each vertex moves on a line, its position at every time between is in that union, so the tree is valid for the whole frame.
- **Other bounding volumes.** The union of two boxes is tight, but the smallest sphere around two spheres is larger than the smallest sphere around their primitives, so a refitted sphere tree is valid but not tight.

## Pitfalls

- **Parents before children in line L2.** A parent computed before a child uses the old box of that child, and the parent box can miss a moved primitive. Traversal then skips a hit.
- **Old primitive boxes in line L1.** The boxes must come from the new positions of the vertices. Using a cached box from the last frame, or the box of only the moved vertices, gives boxes that miss parts of the primitives.
- **Growing the old box in line L4.** Setting $B(v) \leftarrow B(v) \cup B(\mathrm{left}) \cup B(\mathrm{right})$ keeps the boxes valid but never lets them shrink, so the cost can only go up. Compute $B(v)$ from the children alone.
- **The early stop without tight boxes.** The walk of the variation that refits only the moved paths may stop at an unchanged box only if every box was tight before. After a build with boxes rounded outward, or after a growing update, the stop can leave an ancestor box larger than the tight box of its primitives, so the result differs from the full refit.
- **No rebuild in line L5.** The decay has no bound. In the example, two swaps make both children cover the scene; with $n$ primitives, a motion can make almost every internal box cover the scene, and the cost of the refitted tree is then about $n$ times the root area, while a new build costs $O(\log n)$ for the same scene.
- **Adding and removing primitives.** A refit keeps the set of primitives. A primitive that appears needs a leaf, and one that disappears leaves an empty leaf whose box is undefined in line L3; both need an insert, a delete, or a rebuild.

## Exercises

1. Put $n = 2^m$ unit cubes on a line at $x = 0, 1, \ldots, n - 1$ and build a balanced tree with one cube per leaf. Show that its SAH cost is $O(\log n)$. Then find a permutation of the positions such that after a refit every internal node at depth $k$ spans at least $n - 2^k$ in $x$, and show that the cost of the refitted tree is $\Theta(n)$, so the ratio to a new build is $\Theta(n / \log n)$.
2. Show that a refit with the union as MERGE gives every node the tight box of the primitives below it, and that the walk that refits only the moved paths and stops at an unchanged box gives the same boxes as the full refit when all boxes were tight before the motion.

## References
