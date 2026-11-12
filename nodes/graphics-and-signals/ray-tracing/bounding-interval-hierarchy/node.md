---
tag: P0KNZR
kind: data-structure
slug: bounding-interval-hierarchy
name: Bounding interval hierarchy
aliases: [BIH]
area: graphics-and-signals/ray-tracing
level: advanced
summary: A binary tree over objects whose inner nodes store one axis and two clip planes, the end of the objects of the left child and the start of those of the right child, so the boxes are implicit.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of objects, h: the depth of the build (with the halvings that leave one side empty)}
  time: {build: O(n h), closest_hit: O(n), any_hit: O(n)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2006
  people: [Carsten Wächter, Alexander Keller]
  note: Wächter and Keller introduced the BIH for ray tracing scenes that are built again in each frame, with two clip planes per node, global candidate planes from halving the scene box, and an in-place build in bounded memory.
prereqs: [bounding-volume-hierarchy, slab-method]
see_also: [kd-tree-traversal, kd-tree, bvh-construction, bvh-traversal, spatial-splits, surface-area-heuristic, axis-aligned-bounding-box, spatial-index]
sources:
  - paper: doi:10.2312/EGWR/EGSR06/139-149
    title: Carsten Wächter and Alexander Keller, Instant ray tracing, the bounding interval hierarchy, Rendering Techniques 2006 (Eurographics Symposium on Rendering), 139 to 149
    locator: Section 3.1 (the node layout with two clip planes), Section 3.2 (the traversal with interval clipping), Section 3.3 (the classification of objects by the center of their boxes), Section 3.3.1 (global candidate planes from halving the scene box) and Section 3.3.2 (the O(n log n) average build)
  - paper: doi:10.1109/RT.2006.280216
    title: Ingo Wald and Vlastimil Havran, On building fast kd-trees for ray tracing, and on doing that in O(N log N), IEEE Symposium on Interactive Ray Tracing 2006, 61 to 69
    locator: the SAH kd-tree, which puts an object into every cell it overlaps, for comparison with the BIH, which puts it into one leaf
---

A **bounding interval hierarchy** (BIH) is a binary tree over a set of objects, such as the triangles of a scene, in which each object is in exactly one leaf, as in a [bounding volume hierarchy](/bounding-volume-hierarchy/). But an inner node does not store a box. It stores one axis $a$ and two numbers: $\lambda$, the largest coordinate on $a$ of the objects of the left child, and $\rho$, the least coordinate on $a$ of the objects of the right child. The left child lies in the slab $x_a \le \lambda$ and the right child in the slab $x_a \ge \rho$; the two slabs can overlap or leave a gap. The box of a node is the scene box cut by all the slabs on its path, and a ray finds it by clipping its interval at each node, as in [kd-tree traversal](/kd-tree-traversal/). Wächter and Keller (2006) built the planes by halving the scene box, which is fast enough to build the tree again in each frame.

## In plain words

A kd-tree cuts space with one wall per node, and an object that crosses the wall must go to both sides. A BIH sorts each object to one side by the position of its center, and then puts two walls: one at the right end of everything on the left side, and one at the left end of everything on the right side. Everything on the left is behind the first wall, and everything on the right is behind the second wall.

So each object is stored once, as in a BVH, but each node needs only two numbers, as a kd-tree needs one. A ray passes through the walls and keeps track of the part of the ray that is inside each side.

## The abstract type

A BIH is a static [spatial index](/spatial-index/) over $n$ objects with boxes. It supports:

- **build**$(P)$: make the tree for a set of objects.
- **closest hit**$(o, d)$: the object that the ray $o + t d$ meets at the least $t \ge 0$, or none.
- **any hit**$(o, d, t_{max})$: whether the ray meets an object with $0 \le t \le t_{max}$.

It has no insert or delete: a scene that changes is built again.

## Representation

- The scene box $S$, stored once.
- An inner node: the axis $a$ (2 bits), the clip planes $\lambda$ and $\rho$, and the index of the first child, with the two children next to each other.
- A leaf: a range of an array of object indices. Each object is in one leaf, so the array has $n$ entries.

The tree has at most $2n - 1$ nodes, and an inner node has two numbers in place of the six of a box. The box of a node is implicit: $I(\mathrm{root}) = S$, $I(\mathrm{left}) = I(v) \cap \{x_a \le \lambda\}$ and $I(\mathrm{right}) = I(v) \cap \{x_a \ge \rho\}$. The implicit box is a bound, but often not the tight box of the objects below the node, since only one axis is cut at each node.

## Operations

The build uses global candidate planes: each node has a candidate box $V$, which is $S$ at the root, and the plane is the middle of the longest side of $V$. The plane is not fitted to the objects of the node; $V$ is only used to choose planes. Each object goes left when the center $c_r$ of its box is less than the plane. $l_r$ and $h_r$ are the corners of the box of object $r$, and $L$ is the largest number of objects in a leaf.

```pseudo id=main
BIH-BUILD(P)
L1  refs ← all objects; S ← the scene box
L2  stack ← [(refs, V = S)]; while the stack is not empty do pop (R, V); make a node v for R
L3      if |R| ≤ L or the box centers in R are all equal then v is a leaf; continue
L4      a ← the longest axis of V; p ← the middle of V on axis a
L5      R_L ← {r ∈ R : c_{r,a} < p}; R_R ← R minus R_L
L6      if R_L or R_R is empty then V ← the half of V on the side of p that holds the centers; go to L4
L7      v ← an inner node with axis a, λ ← the largest h_{r,a} over R_L, ρ ← the least l_{r,a} over R_R
L8      push (R_R, the upper half of V), then (R_L, the lower half of V), as the children of v
```

Line L6 does not make a node: it shrinks the candidate box until the plane separates the objects. Line L3 makes a leaf when all centers are equal, since then no plane separates them. Lines L5 and L7 can be done in place with one pass that swaps objects, as in the partition of quicksort, so the build needs no memory beyond the tree.

The closest-hit query walks the tree with the interval of the ray inside the implicit box of each node.

```pseudo id=closest
BIH-CLOSEST(T, o, d)
L9  [t_n, t_f] ← the ray against S on [0, ∞) by the slab method; if it is empty, return none
L10 best ← none; stack ← [(root, t_n, t_f)]
L11 while the stack is not empty do pop (v, t_n, t_f); if best ≠ none then (if t_n > t(best) then continue; t_f ← min(t_f, t(best)))
L12     if v is a leaf then for each object r of v: if the ray meets r at t ≥ 0 with t < t(best) then best ← (t, r); continue
L13     a ← axis(v); I_L ← [t_n, t_f] ∩ {t : o_a + t d_a ≤ λ}; I_R ← [t_n, t_f] ∩ {t : o_a + t d_a ≥ ρ}
L14     push the far child with its interval if it is not empty, then the near child (the left child is near when d_a ≥ 0)
L15 return best
```

Line L13 is one division per clip plane, and one comparison when $d_a = 0$. The walk does not stop at the first leaf with a hit, since the slabs of the two children can overlap; line L11 skips a node whose interval starts after the best hit. The any-hit query is the same walk with $t_f$ starting at $t_{max}$, in any order, and it returns true at the first hit with $t \le t_{max}$.

## Example

Four triangles lie in $0 \le y, z \le 1$ with these extents in $x$: A $[0, 3]$, B $[2, 7]$, C $[6, 9]$ and D $[12, 16]$. Their box centers in $x$ are 1.5, 4.5, 7.5 and 14. The scene box is $[0, 16] \times [0, 1] \times [0, 1]$, so $x$ is the longest axis at every node; $L = 1$.

| node | candidate box in $x$ | plane $p$ | left | right | $\lambda$ | $\rho$ |
|---|---|---|---|---|---|---|
| root | $[0, 16]$ | 8 | A, B, C | D | 9 | 12 |
| N1 (left of root) | $[0, 8]$ | 4 | A | B, C | 3 | 2 |
| N2 (right of N1) | $[4, 8]$ | 6 | B | C | 7 | 6 |

At the root the slabs leave the gap $9 < x < 12$, so a ray there is cut off at once. At N1 they overlap in $[2, 3]$.

Take the ray $o = (-1, 9/10, 1/20)$, $d = (1, 0, 0)$. Triangle A is $(0, 0, 0)$, $(3, 1, 0)$, $(0, 0, 1)$, which the ray meets at $x = 2.7$, so $t = 3.7$. Triangle B is $(7, 0, 0)$, $(2, 1, 0)$, $(7, 0, 1)$, which it meets at $x = 2.5$, so $t = 3.5$. C and D are met at $t = 9.7$ and $t = 16.6$.

| step | node | interval | action |
|---|---|---|---|
| 1 | root | $[1, 17]$ | left: $x \le 9$ gives $[1, 10]$; right: $x \ge 12$ gives $[13, 17]$; push the right, then the left |
| 2 | N1 | $[1, 10]$ | left: $x \le 3$ gives $[1, 4]$; right: $x \ge 2$ gives $[3, 10]$ |
| 3 | leaf A | $[1, 4]$ | hit at $t = 3.7$; best = A |
| 4 | N2 | $[3, 10]$ cut to $[3, 3.7]$ | left: $x \le 7$ gives $[3, 3.7]$; right: $x \ge 6$ gives $t \ge 7$, empty |
| 5 | leaf B | $[3, 3.7]$ | hit at $t = 3.5$; best = B |
| 6 | leaf D | $[13, 17]$ | $13 > 3.5$, skipped |

The near leaf A gives a hit first, but the nearer hit is in B, in the far child of N1. A walk that stopped at the first leaf with a hit would return A. The tests check this example.

## Correctness

Three facts make the BIH correct; [proofs/correctness.md](proofs/correctness.md) has the full proofs.

- **The build ends, and each object is in one leaf.** Line L6 keeps all centers of the range in $V$, and since two centers differ on some axis by some $\epsilon > 0$, the halvings of line L6 end with a split. Each split makes two nonempty parts, so the leaves partition the objects.
- **The implicit boxes contain their objects.** By line L7, every object of the left child ends at or before $\lambda$ on axis $a$, and every object of the right child starts at or after $\rho$. By induction from $S$, the box of each object lies in the implicit box of every node above it.
- **The walk finds the closest hit.** The interval of a node is the part of the ray in its implicit box, up to the best hit so far. The point of the closest hit lies in the implicit box of every node on the path to its leaf, so none of them is skipped in line L11.

The implementation builds random scenes with exact rational coordinates, including copies of triangles and centers that differ by $1/64$. It checks that each triangle is in exactly one leaf, that there are at most $2n - 1$ nodes, that each implicit box contains every triangle below it, that the clip planes are tight, and that closest-hit and any-hit answers equal a brute force over all triangles.

## Complexity

| operation | time | note |
|---|---|---|
| build | $O(n h)$ | $O(\vert R \vert)$ for each pass of lines L4 to L7 at a node; $O(n \log n)$ for well spread input |
| closest hit | $O(n)$ per ray in the worst case | a ray can meet every implicit box; logarithmic in practice for scenes of small objects |
| any hit | $O(n)$ per ray in the worst case | the same walk, which can stop at any hit |
| space | $\Theta(n)$ | at most $2n - 1$ nodes of two numbers and one index, and $n$ object indices |

Here $h$ counts the halvings of line L6. In exact arithmetic it is bounded by the number of times the scene box must be halved to separate the closest pair of distinct centers; with floating point numbers the halvings stop at the precision, and an implementation then makes a leaf or limits the depth. The $O(n \log n)$ build of Wächter and Keller is for objects that are spread evenly, where the depth is $O(\log n)$. The logarithmic query time is an observation and not a bound: a ray can pass through the implicit boxes of all the leaves, as in a scene of long thin triangles that the ray grazes.

## Variants

- **Adaptive planes.** Choose the plane from the box of the objects of the node, or from their centers, in place of the global candidate box. This gives a better tree for clustered scenes at the same cost.
- **SAH planes.** Choose the plane with the least cost by the [surface area heuristic](/surface-area-heuristic/), as for a [BVH build](/bvh-construction/). The build is slower and the tree is close to an SAH BVH.
- **Empty space nodes.** When a halving leaves one side empty, a node with one child and one clip plane can cut away the empty part of the box, so a ray that misses it stops sooner.
- **Related structures.** Trees with two planes per node were also used before for spatial databases and for collision detection, and in the same year as the BIH, for ray tracing on hardware. They differ in how they choose the planes.
- **Lazy building.** Build only the nodes that rays reach, which suits scenes that are traced with few rays per frame.

## When to use it

Use a BIH when a scene changes every frame and is built again each time, when the memory is limited and known in advance, or when a [kd-tree](/kd-tree-traversal/) would duplicate too many objects. Its nodes are small and its build is a few passes of partitioning. For a static scene, an SAH [BVH](/bvh-construction/) or an SBVH with [spatial splits](/spatial-splits/) traces faster. For small changes to a scene, [refitting](/bvh-refitting/) a BVH is cheaper than any build.

## Pitfalls

- **Stopping at the first hit in line L12.** The slabs of the two children overlap when $\lambda > \rho$, so a hit in the near child need not be the closest; the example shows it. Only the test of line L11 may skip a node.
- **The candidate box as the node box.** In line L4, $V$ is only a source of planes. Objects stick out of $V$, so a traversal that tests the ray against $V$ misses hits; the box of a node is the implicit box from the clip planes.
- **Clip planes from the centers in line L7.** $\lambda$ and $\rho$ must come from the ends of the boxes of the objects, not from their centers or from $p$, or parts of the objects lie outside the slab of their child.
- **The wrong half in line L6.** If line L6 keeps the half without the centers, the plane never separates them and the build does not end. The half must be the one on the side of $p$ that holds all the centers.
- **No leaf for equal centers in line L3.** Copies of one triangle have equal centers. Without the test, lines L4 to L6 halve $V$ forever.
- **$d_a = 0$ in line L13.** The interval is then all or nothing by the sign of $\lambda - o_a$. A division gives $\pm \infty$, or a NaN when $o_a = \lambda$; the [slab method](/slab-method/) explains how to make that case safe with [IEEE 754](/ieee-754/) numbers.

## Implementations

## History

Wächter and Keller (2006) introduced the bounding interval hierarchy for instant ray tracing, in which the acceleration structure is built again for each frame. They took the planes from the halving of the scene box, so that the build is a few passes of an in-place partition, and the traversal is that of a kd-tree with a second clip plane at each node and no early stop. Similar trees with two planes per node had appeared earlier in spatial databases and in collision detection, and in the same year in hardware ray tracing.

## References
