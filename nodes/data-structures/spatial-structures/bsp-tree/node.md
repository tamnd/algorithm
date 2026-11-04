---
tag: MSZB1N
kind: data-structure
slug: bsp-tree
name: Binary space partitioning tree
aliases:
- BSP tree
- binary space partition
area: data-structures/spatial-structures
level: core
summary: Tree that recursively splits space by hyperplanes, used for visibility ordering and ray tracing.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of input segments, m: the number of fragments stored, h: the height of the tree}
  time: {build: O(n m), insert: O(m), back_to_front: O(m)}
  space: {total: Θ(m)}
history:
  year: 1980
  people: [Henry Fuchs, Zvi M. Kedem, Bruce F. Naylor]
  note: Fuchs, Kedem and Naylor introduced the BSP tree for visible surface generation at SIGGRAPH 1980, building on the ordering idea of Schumacker and others from 1969.
prereqs: [binary-tree]
see_also: [bsp-tree-visibility, painters-algorithm, hidden-surface-removal, kd-tree, space-partitioning, ray-casting, octree, quadtree]
sources:
  - paper: doi:10.1145/800250.807481
    title: Henry Fuchs, Zvi M. Kedem and Bruce F. Naylor, On visible surface generation by a priori tree structures, Proceedings of SIGGRAPH 1980
    locator: the BSP tree built from the polygons of a scene and the back-to-front traversal from any viewpoint
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 12, Binary Space Partitions (the painter's algorithm, autopartitions, the random autopartition of segments with O(n log n) expected size, and BSPs in three dimensions)
  - paper: doi:10.1007/BF02187806
    title: Michael S. Paterson and F. Frances Yao, Efficient binary space partitions for hidden-surface removal and solid modeling, Discrete and Computational Geometry 5, 1990
    locator: the O(n log n) expected size of a random autopartition of n segments in the plane, and the O(n^2) bound for triangles in space
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 8, BSP Tree Hierarchies (node-storing, leaf-storing and solid-leaf BSP trees, the choice of dividing planes, and splitting polygons)
---

A binary space partitioning (BSP) tree splits space in two by a hyperplane, then splits each half again, and so on: each node holds a hyperplane, and its two children hold the parts of the scene on the two sides. In the plane the hyperplanes are lines and the scene is a set of segments; in space they are planes and the scene is a set of polygons. An object that crosses the hyperplane of a node is cut, and its two fragments go to the two sides. The tree gives, for any viewpoint, an order of the fragments from back to front, which is the order the [painter's algorithm](/painters-algorithm/) needs, and it supports point location, ray casting and set operations on solids. Fuchs, Kedem and Naylor introduced it in 1980.

## In plain words

You want to paint a picture of walls in a room, far walls first, so that near walls cover them. To know which walls are far, take one wall and think of the line through it as a cut. All the walls on the other side of the cut from you are farther than the walls on your side, in the sense that they cannot cover them.

So paint the far side first, then the wall on the cut, then your side. Do the same inside each side, with another wall as the cut. A wall that lies across a cut is cut into two pieces, one on each side.

The cuts do not depend on where you stand. You build the tree once and use it from any place.

## The abstract type

A BSP tree stores a set of objects, here segments in the plane, as a set of fragments that together cover the objects. It supports `build(S)`, `insert(s)`, and `back_to_front(v)`, which returns all fragments in an order in which no fragment hides a part of a fragment that comes later, as seen from the point $v$. The same tree answers "which cell holds the point $q$" by one walk down, and gives the cells in the order a ray from $q$ meets them.

## Representation

Each node $t$ holds a line $t.line$, given by a directed segment $(a, b)$, the list $t.on$ of the fragments that lie on that line, and two children. For a point $p$, write
$$\sigma_t(p) = (b_x - a_x)(p_y - a_y) - (b_y - a_y)(p_x - a_x).$$
The *front* half-plane of $t$ is $\{p : \sigma_t(p) > 0\}$, to the left of the directed line, and the *back* half-plane is $\{p : \sigma_t(p) < 0\}$. The subtree $t.front$ holds the fragments in the closed front half-plane, and $t.back$ those in the closed back half-plane.

**Invariant (P).** For each node $t$: each fragment of $t.on$ lies on $t.line$; each fragment in the subtree $t.front$ has $\sigma_t \ge 0$ at both ends; and each fragment in the subtree $t.back$ has $\sigma_t \le 0$ at both ends. The fragments of each input segment cover it, and they meet only at their ends.

The node regions follow from (P): the root owns the plane, and the line of a node cuts its region into the regions of its two children, which are convex polygons, possibly unbounded. This page uses an *autopartition*: the line of each node is the line through one of the input segments. This is the usual choice, and it lets each node store at least one fragment.

## Operations

```pseudo id=main
BUILD(S)                                   ▷ S a list of segments that do not cross; returns a tree
L1  if S is empty then return nil
L2  s ← the first segment of S
L3  t ← a new node with t.line the line through s and t.on = [s]
L4  F ← an empty list; K ← an empty list
L5  for each other segment r of S, in order:
L6      if r lies on t.line then append r to t.on
L7      else if r lies in the closed front half-plane then append r to F, or in the closed back half-plane then append r to K
L8      else cut r where it crosses t.line; append the front part to F and the back part to K
L9  t.front ← BUILD(F); t.back ← BUILD(K); return t

BACK-TO-FRONT(t, v)                        ▷ output the fragments, farthest first, as seen from v
L10 if t = nil then return
L11 if σt(v) > 0 then BACK-TO-FRONT(t.back, v); output t.on; BACK-TO-FRONT(t.front, v)
L12 else if σt(v) < 0 then BACK-TO-FRONT(t.front, v); output t.on; BACK-TO-FRONT(t.back, v)
L13 else BACK-TO-FRONT(t.front, v); output t.on; BACK-TO-FRONT(t.back, v)     ▷ v on the line
```

The tests of lines L6 and L7 take the signs of $\sigma_t$ at the two ends of $r$. Line L8 runs only when the signs are strictly opposite, so the cut point is inside $r$, at the parameter $\sigma_t(p) / (\sigma_t(p) - \sigma_t(q))$ from the end $p$. With rational input the cut points are rational, and the implementation computes them exactly.

In line L11 the viewer is in front of the line, so nothing in the back half-plane can hide anything in the front half-plane or on the line: draw the back first. In line L13 the viewer is on the line, and the fragments of $t.on$ are seen edge on, so any order of the two sides works.

**Insertion** filters a new segment down the tree: at each node it goes to one side, is cut in two, or lies on the line and joins $t.on$. A part that reaches an empty child becomes a new node there. Insertion keeps (P), but a tree built by many insertions may be far from the best.

## Example

Take four segments that do not touch: $a$ from $(0,0)$ to $(4,0)$, $b$ from $(2,-2)$ to $(2,2)$, $c$ from $(5,-1)$ to $(5,3)$, and $d$ from $(-1,3)$ to $(3,4)$. Build in this order. The line of $a$ points in the $+x$ direction, so its front is $y > 0$. The lines of $b$ and $c$ point in the $+y$ direction, so their fronts are $x < 2$ and $x < 5$.

| node | group | what happens | front group | back group |
|---|---|---|---|---|
| $a$ ($y = 0$) | $a, b, c, d$ | $b$ and $c$ cross $y = 0$ and are cut at $(2,0)$ and $(5,0)$; $d$ is in front | $b_1 = (2,0)$-$(2,2)$, $c_1 = (5,0)$-$(5,3)$, $d$ | $b_2 = (2,-2)$-$(2,0)$, $c_2 = (5,-1)$-$(5,0)$ |
| $b_1$ ($x = 2$) | $b_1, c_1, d$ | $c_1$ is behind; $d$ crosses $x = 2$ at $(2, 15/4)$ | $d_1 = (-1,3)$-$(2,15/4)$ | $c_1$, $d_2 = (2,15/4)$-$(3,4)$ |
| $c_1$ ($x = 5$) | $c_1, d_2$ | $d_2$ is in front | $d_2$ | none |
| $b_2$ ($x = 2$) | $b_2, c_2$ | $c_2$ is behind | none | $c_2$ |

The tree has 7 fragments for 4 segments, and height 4. From the viewpoint $v = (3, -3)$, which is behind the line of $a$, BACK-TO-FRONT draws the front subtree of $a$ first. At $b_1$, $v$ has $x = 3 > 2$, so it is behind again, and the order is $d_1$, then $b_1$, then the subtree of $c_1$; at $c_1$, $v$ has $x < 5$ and is in front, so it gives $c_1$ and then $d_2$. Then comes $a$, then the subtree of $b_2$, where $v$ is behind: $b_2$, then $c_2$. The full order is $d_1, b_1, c_1, d_2, a, b_2, c_2$, and the closest fragments, $b_2$ and $c_2$, are drawn last.

## Correctness

BUILD keeps (P): each segment of a group goes to the side its ends are on, or is cut at the line into two parts, one on each side, which together cover it and meet at the cut point. Each node puts the first segment of its group in $t.on$ and passes the others to strictly smaller groups, so the recursion stops. For BACK-TO-FRONT, take a node $t$ with the viewer $v$ strictly in front. A segment from $v$ to a point $y$ in the closed front half-plane lies in that half-plane, by convexity, so it cannot pass through the interior of a fragment that lies in the open back half-plane, and a fragment of the back subtree that lies on the line is met only at its ends or edge on. So no fragment of the back subtree hides a part of a fragment of $t.on$ or of the front subtree, and drawing the back first is safe; within each side, induction gives the order. The full proof is in the proofs folder.

## Complexity

The model is the [real RAM](/real-ram/), or exact rational arithmetic as in the implementation.

- **Size.** Each node of an autopartition stores at least one fragment, and each cut at line L8 makes one more fragment, so the tree has at most $m$ nodes and $m \ge n$. A cut line can cross each other segment once, so $m \le n + n(n-1) = O(n^2)$ for any order. Paterson and Yao showed that if the order of $S$ is a uniform random permutation, the expected size is $O(n \log n)$: a segment $r$ is cut by the line of $s$ only if $s$ comes before the $j - 1$ segments that lie between $s$ and $r$ along that line, which has probability at most $1/j$, and the sum of these over all pairs is $O(n \log n)$. Tóth later showed that some sets of $n$ segments need $\Omega(n \log n / \log \log n)$ fragments in any BSP.
- **Build.** A fragment at depth $j$ is tested at each of its $j$ ancestors, so BUILD takes $O(m h)$ time, which is $O(n m)$ because $h \le n$: each node uses up one input segment. For a random order, de Berg and others bound the expected time by $O(n^2 \log n)$.
- **Back to front.** Each node costs $O(1)$ plus its fragments: $O(m)$.
- **Insert.** A segment can be cut at many nodes; the cost is at most the number of nodes it reaches, $O(m)$.
- **Space.** $\Theta(m)$.
- **Three dimensions.** For $n$ disjoint triangles in space, Paterson and Yao gave a BSP of size $O(n^2)$, and there are sets for which every BSP has size $\Omega(n^2)$.

| operation | time | case |
|---|---|---|
| build | $O(n m)$ | worst; $m = O(n \log n)$ expected for a random order |
| insert | $O(m)$ | worst |
| back_to_front | $O(m)$ | worst |
| space | $\Theta(m)$ | total |

## Variants

- **Leaf-storing and solid BSP trees.** Store the objects only in the leaves, or, for a closed solid, use the planes of its faces and mark each leaf cell as inside or outside. A solid BSP tree answers "is this point inside" by one walk down, and Thibault and Naylor showed how to compute unions, intersections and differences of solids on such trees.
- **Choice of the splitting line.** Instead of a random segment, pick at each node a segment that cuts few others and splits the group evenly, by testing a few candidates. Engines weigh the two goals: few cuts give fewer fragments, even splits give a lower tree.
- **Free cuts.** A segment whose ends both lie on the boundary of the node's region cuts nothing more when it is used, so using it first costs nothing. This is part of the analysis of the best BSPs.
- **Axis-aligned BSP trees.** If every line is parallel to an axis, the tree is a [k-d tree](/kd-tree/) on objects, as used for ray tracing with the [surface area heuristic](/surface-area-heuristic/).
- **Visibility with BSP trees.** The [BSP tree visibility](/bsp-tree-visibility/) page treats the use of the order for [hidden surface removal](/hidden-surface-removal/), with front-to-back drawing and occlusion tests.

## When to use it

Use a BSP tree when the scene is static and is viewed from many places, so that one build pays for many queries: the back-to-front order for any viewpoint costs only a walk of the tree. This made it the choice of early 3D games, which built a BSP of the level walls before the game ran, and of flight simulators before the [z-buffer](/z-buffer/) became cheap in hardware. It is also good for solid modeling, point classification, and [ray casting](/ray-casting/) against static walls. For scenes that change, a [bounding volume hierarchy](/bounding-volume-hierarchy/) or a grid is easier to update. If only depth order per pixel is needed and memory allows, a z-buffer is simpler.

## Pitfalls

- **Rounding at the cuts.** A cut point computed in floating point does not lie exactly on the line, so later tests may put a fragment on the wrong side or call a segment both front and back. Use exact arithmetic, as here, or test with a tolerance and treat "almost on the line" as on the line.
- **Fragment blow-up.** A bad order of the segments gives $\Theta(n^2)$ fragments. Use a random order, or choose splitting lines that cut few segments.
- **Recursion depth.** The height can be $n$, for example for parallel segments taken in order. The implementation builds and walks the tree with explicit stacks.
- **Segments that cross.** The order is defined only when the objects do not cross; two crossing segments hide each other. Cut such inputs at their crossings first.
- **Wrong side for the viewer.** Line L11 draws the back first when the viewer is in front. Swapping the two cases gives the front-to-back order, which is what occlusion culling wants and what the painter's algorithm must not use.

## Implementations

## History

Schumacker, Brand, Gilliland and Sharp described in 1969 how a fixed partition of a scene by planes gives a visibility order, for flight simulators. Henry Fuchs, Zvi Kedem and Bruce Naylor turned this into the BSP tree in 1980, built automatically from the polygons of the scene, and Fuchs, Abram and Grant improved it in 1983. Thibault and Naylor used BSP trees for set operations on polyhedra in 1987. Paterson and Yao gave the first bounds on the size of BSPs in 1990. In 1993 the game Doom used a 2D BSP of its level walls to draw each frame.

## References
