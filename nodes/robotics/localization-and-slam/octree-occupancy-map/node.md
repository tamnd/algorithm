---
tag: 34SSST
kind: data-structure
slug: octree-occupancy-map
name: Octree occupancy map
aliases:
- OctoMap
area: robotics/localization-and-slam
level: advanced
summary: A probabilistic 3D occupancy map stored in an octree with log odds, clamping and pruning so free and unknown space are compact.
model: word-ram
complexity:
  vars: {D: the depth of the tree, s: the side of a voxel in meters, L: the length of the longest beam in meters, R: the number of end points in a scan, K: the number of leaves}
  time: {update: O(D), search: O(D), voxels_on_segment: O(1 + L / s), insert_scan: O(R D (1 + L / s))}
  space: {total: O(1 + K D)}
history:
  year: 2013
  people: [Armin Hornung, Kai M. Wurm, Maren Bennewitz, Cyrill Stachniss, Wolfram Burgard]
  note: Hornung and coauthors combined octrees with occupancy grid mapping, clamped log odds and lossless pruning of stable nodes in the OctoMap framework, after an earlier workshop version in 2010.
prereqs: [octree, occupancy-grid-map]
see_also: [occupancy-grid-map, occupancy-grid-mapping, inverse-sensor-model, octree, quadtree, amanatides-woo-traversal, z-order-curve, frontier-based-exploration]
sources:
  - paper: doi:10.1007/s10514-012-9321-0
    title: "Armin Hornung, Kai M. Wurm, Maren Bennewitz, Cyrill Stachniss and Wolfram Burgard, OctoMap: an efficient probabilistic 3D mapping framework based on octrees, Autonomous Robots 34(3), 2013, pages 189 to 206"
    locator: "Section 3.1 to 3.4 (octrees, the log odds update, the clamping update of Eq. 4, the mean and maximum of the children in Eq. 5 and 6, pruning of stable nodes), Section 4.1 and 4.2 (node memory and the depth limit of 16), Section 5.1 (sensor model values and the update of each voxel at most once per scan)"
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 9, Section 9.2 (occupancy grid mapping in log odds form)"
  - paper: "John Amanatides and Andrew Woo, A fast voxel traversal algorithm for ray tracing, Eurographics 1987"
    locator: the traversal of the voxels that a ray crosses
---

An octree occupancy map stores a 3D [occupancy grid map](/occupancy-grid-map/) in an [octree](/octree/). Each leaf holds the log odds $l = \log(p / (1 - p))$ that its cube of space is occupied, and the update of a voxel is the same binary Bayes filter in log odds as in a 2D grid. Three choices make the tree small. Unknown space has no nodes at all. The log odds of each voxel are clamped to a range $[l_{\min}, l_{\max}]$, so that a voxel seen free many times reaches exactly $l_{\min}$. And when the eight children of a node are leaves with one equal value, they are pruned into one leaf. Large free volumes and large walls then cost few nodes. The design is that of OctoMap by Hornung, Wurm, Bennewitz, Stachniss and Burgard (2013), an open source library that is also available in ROS.

## In plain words

Think of a big cube of space that holds a building. Cut it into eight smaller cubes, cut each of those into eight, and so on, until the cubes are a few centimeters wide. A robot with a laser only writes into the small cubes that its beams touch. A small cube that a beam passes through becomes more likely to be empty; a small cube where a beam stops becomes more likely to hold something. After enough agreement, a cube is "sure" and stops changing much. When all eight parts of a cube are sure in the same way, the map forgets the parts and keeps only the big cube. Parts of space that no beam ever reached are not stored at all. To read the map at a coarse size, look at a big cube: it says "occupied" as soon as one of its parts is.

## The abstract type

The map is a partial function from the voxels of a cube of $2^D$ voxels on each side to log odds values in $[l_{\min}, l_{\max}]$. A voxel without a value is unknown. The operations are:

- `key(point)`: the integer key $(k_x, k_y, k_z)$ of the voxel that holds a point, or none outside the map.
- `update(k, l_meas)`: set the value of voxel $k$ to $\min(l_{\max}, \max(l_{\min}, l + l_{\mathrm{meas}}))$, where $l$ is its old value, or 0 (the prior probability 0.5) if it was unknown.
- `search(k, d)`: the value of the block of depth $d$ that holds $k$: the maximum of the values of its known voxels, or unknown if it has none. Depth $D$ gives the value of the voxel itself.
- `insert_scan(s, Z)`: integrate one scan from the sensor origin $s$ with the end points $Z$.

The maximum in `search` is the conservative choice of Hornung et al.: a coarse block is as occupied as its most occupied part. The mean of the children is the other choice that they describe.

## Representation

- The depth $D$, the voxel side $s$ in meters and the origin $o$ of the map. Voxel $k$ is the half-open cube with the lowest corner $o + s k$, and the map covers a cube of side $2^D s$.
- A node of depth $d$ covers a block of $2^{D - d}$ voxels on each side. Child number $c$ of a node of depth $d$ holds the voxels whose bit $D - 1 - d$ of $k_x$, $k_y$ and $k_z$ form $c$ (one bit per axis). The key of a voxel is the path from the root, so nodes store no coordinates.
- A leaf stores one log odds value. A leaf of depth $D$ is one voxel; a leaf of depth $d < D$ is a pruned block, all of whose voxels have its value.
- An inner node stores 8 child slots, each empty or a node, and the maximum of the values of its children.
- The values $l_{\mathrm{occ}}$ and $l_{\mathrm{free}}$ of the inverse sensor model, and the clamping bounds.

**Invariant (T).** (1) Inner nodes have depth below $D$, and each inner node except the root has at least one child. (2) A voxel is known if and only if the descent along its key reaches a leaf, and then its value is the value of that leaf. (3) An inner node holds the maximum of its children's values. (4) Leaf values are in $[l_{\min}, l_{\max}]$. (5) No inner node has 8 children that are leaves with one equal value.

Part 5 makes the tree canonical: for each map there is exactly one tree that satisfies (T), so the number of nodes depends only on the values, not on the order of the updates.

## Operations

```pseudo id=main
UPDATE(T, k, l_meas)                   ▷ k = (k_x, k_y, k_z), each in [0, 2^D)
L1  n ← T.root;  P ← empty stack
L2  for d ← 0 to D - 1:
L3      if n is a leaf then give n 8 leaf children with the value of n      ▷ expand a pruned block
L4      c ← bit (D-1-d) of k_x + 2 · bit (D-1-d) of k_y + 4 · bit (D-1-d) of k_z
L5      if child c of n is empty then create it: a leaf with value 0 if d = D - 1, else an inner node with no children
L6      push n on P;  n ← child c of n
L7  n.value ← min(l_max, max(l_min, n.value + l_meas))
L8  while P is not empty:
L9      q ← pop P
L10     if q has 8 children that are leaves with one equal value v then make q a leaf with value v    ▷ prune
L11     else q.value ← the maximum of the values of the children of q
```

The descent creates the missing nodes on the way to the voxel and expands a pruned block that the update must split. Line L7 is the log odds form of the binary Bayes filter with the clamping rule $L \leftarrow \max(\min(L + l_{\mathrm{meas}}, l_{\max}), l_{\min})$, which Hornung et al. take from Yguel et al. (2007). The ascent restores the maxima and prunes. A new inner node of line L5 has no children for a moment, but the next step of the descent gives it one.

```pseudo id=query
SEARCH(T, k, d_q)                      ▷ the value of the block of depth d_q that holds k, or unknown
L12 n ← T.root;  d ← 0
L13 while d < d_q and n is not a leaf:
L14     n ← child c(k, d) of n;  d ← d + 1
L15     if n is empty then return unknown
L16 return n.value                       ▷ unknown for a root with no children
```

A search that reaches a leaf above depth $d_q$ returns the value of the pruned block, which is the value of every voxel inside it.

```pseudo id=scan
INSERT-SCAN(T, s, Z)                   ▷ sensor origin s, end points Z, every beam a hit
L17 F ← empty set;  O ← empty set
L18 for each end point z in Z:
L19     V ← the voxels that the segment from s to z crosses, in order
L20     add all voxels of V except the last to F;  add the last voxel of V to O
L21 for each voxel k in F - O inside the map: UPDATE(T, k, l_free)
L22 for each voxel k in O inside the map: UPDATE(T, k, l_occ)
```

Line L19 is the 3D form of the [Amanatides-Woo traversal](/amanatides-woo-traversal/) that the [occupancy grid map](/occupancy-grid-map/) page describes in 2D, with three next-crossing parameters instead of two. Lines L21 and L22 update each voxel of the scan once, and an end voxel gets $l_{\mathrm{occ}}$ even when another beam of the same scan passes through it. Hornung et al. use this rule because a laser that sweeps over a flat surface at a shallow angle otherwise clears voxels that an earlier beam of the same sweep marked occupied, and leaves holes in the surface. The implementation sorts the two sets only to get a fixed order; the result does not depend on the order.

## Example

**Pruning and expansion.** Take $D = 2$, a cube of $4 \times 4 \times 4 = 64$ voxels, with the values of the paper: $l_{\mathrm{occ}} = 0.85$, $l_{\mathrm{free}} = -0.4$, $l_{\min} = -2$ and $l_{\max} = 3.5$. A full tree of depth 2 has $1 + 8 + 64 = 73$ nodes.

1. Update every voxel 5 times with $l_{\mathrm{free}}$. Each voxel goes $-0.4, -0.8, -1.2, -1.6, -2.0$ and reaches $l_{\min}$. During the last round, each group of 8 voxels prunes into its parent as soon as its last voxel reaches $-2$, and the last update prunes the 8 children of the root. The tree is one node: the root, a leaf with the value $-2$ (probability 0.1192) for the whole cube.
2. Update voxel $(1, 2, 3)$ once with $l_{\mathrm{occ}}$. Its child numbers are $c = 0 + 2 \cdot 1 + 4 \cdot 1 = 6$ at depth 0 (the high bits 0, 1, 1) and $c = 1 + 0 + 4 = 5$ at depth 1 (the low bits 1, 0, 1). Line L3 expands the root into 8 leaves of value $-2$, then expands child 6 into 8 voxels. The voxel gets $-2 + 0.85 = -1.15$ (probability 0.2405). The tree has $1 + 8 + 8 = 17$ nodes. SEARCH at depth 0 or at depth 1 in child 6 returns $-1.15$, the maximum; SEARCH of $(3, 0, 0)$ at depth 1 returns $-2$ from a pruned leaf.
3. Update voxel $(1, 2, 3)$ three times with $l_{\mathrm{free}}$: $-1.55$, $-1.95$, then $-2.35$, clamped to $-2$. Now the 8 children of child 6 are equal, line L10 prunes them, then the 8 children of the root are equal, and the tree is one node again.

Without clamping, the voxel of step 3 would end at $-2.35$, its 63 neighbors at $-2$, and the tree would keep 17 nodes. Clamping is what makes such blocks equal.

**One scan.** Take $D = 4$, $s = 0.1$ m and the origin at 0. The sensor is at $(0.05, 0.05, 0.05)$, in voxel $(0, 0, 0)$, and the scan has two end points on the $x$ axis: $(0.55, 0.05, 0.05)$ in voxel 5 and $(0.35, 0.05, 0.05)$ in voxel 3 (only $k_x$ is written). Then $O = \{3, 5\}$ and $F = \{0, 1, 2, 3, 4\}$, so INSERT-SCAN gives:

| $k_x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| log odds | -0.4 | -0.4 | -0.4 | 0.85 | -0.4 | 0.85 | unknown |
| probability | 0.4013 | 0.4013 | 0.4013 | 0.7006 | 0.4013 | 0.7006 | |

Voxel 3 lies on the first beam, but it holds an end point, so it gets one update with $l_{\mathrm{occ}}$. Inserting the two beams one by one would give it $-0.4 + 0.85 = 0.45$ (0.6106) and voxels 0 to 2 the value $-0.8$.

## Correctness

The abstract value of the tree is the partial map from voxels to log odds that part 2 of (T) defines. The empty tree, a root with no children, is the empty map. The descent of UPDATE changes only the representation: an expansion replaces a pruned leaf by 8 leaves with the same value over the same voxels, and a new inner node makes no voxel known. Line L7 then applies the abstract update to the leaf of $k$. The ascent goes up from depth $D - 1$, and at each node the subtrees of its children already satisfy (T), so the node either prunes into a leaf whose block is uniform or takes the maximum of its children. By induction from the leaves, the value of an inner node is the maximum over the known voxels of its block, which is what SEARCH must return; a missing child means that its whole octant is unknown. Part 5 forces a node to be a leaf exactly when its block is uniform, which makes the tree unique for each map. INSERT-SCAN calls UPDATE once per voxel, and updates of different voxels commute. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with keys of $D$ bits per axis in one word, so line L4 is a constant number of shifts and masks, and one step per operation on a floating-point log odds value.

| operation | time | case |
|---|---|---|
| key | $O(1)$ | worst |
| update | $O(D)$ | worst |
| search | $O(D)$ | worst |
| voxels_on_segment | $O(1 + L / s)$ | worst |
| insert_scan | $O(R D (1 + L / s))$ | expected, with hash sets |
| space | $O(1 + K D)$ | total |

UPDATE does constant work at each of $D$ levels on the way down and on the way up, since a node has 8 child slots. Each beam crosses $O(1 + L / s)$ voxels, and INSERT-SCAN calls UPDATE at most once per voxel. Every node is a leaf or an ancestor of a leaf, and a leaf has at most $D$ ancestors, so a tree with $K$ leaves has at most $1 + K D$ nodes; it never has more than the full tree, $(8^{D + 1} - 1) / 7$ nodes.

The fixed depth makes the per-voxel cost a constant compared with a 3D array: OctoMap uses $D = 16$, which covers $2^{16} \cdot 0.01 = 655.36$ m at 1 cm, and says the implementation can be extended to 32 levels. Hornung et al. report measurements on a 32-bit system of 40 bytes per inner node and 8 bytes per leaf, with the children of a node in one array that exists only for inner nodes; 80 to 85 percent of the nodes in their datasets were leaves, and this layout saved 60 to 65 percent of memory against eight child pointers in every node. They also report that clamping with pruning compressed their maps by up to 44 percent. These are measurements on their datasets, not bounds.

## Variants

- **Mean of the children.** Store the average of the children's log odds in inner nodes instead of the maximum. A coarse query then answers how occupied a block is on average, and a small obstacle can disappear at a coarse depth.
- **Maximum likelihood maps.** Set every voxel to $l_{\min}$ or $l_{\max}$ by a threshold and then prune. This is lossy but gives much smaller trees; Hornung et al. attribute the threshold idea to Fairfield et al. (2007).
- **Compact files.** A maximum likelihood tree can be written as a stream of 2 bits per child (unknown, occupied, free, or inner node with more data), so 16 bits per inner node, with no coordinates, since the order of the stream encodes the positions.
- **Rich voxels.** A node can store more data, such as a color or a terrain class, if there is a rule to combine measurements and children.
- **Hierarchies of maps.** A tree of submaps, each an octree with its own resolution, for example a table at fine resolution and the room around it at coarse resolution.
- **Other layouts.** Some systems store fixed-size blocks of voxels in a [hash table](/hash-table/) keyed by the block index, or order voxels on a [Z-order curve](/z-order-curve/); these keep constant time access without a fixed depth. A [quadtree](/quadtree/) is the 2D form of the same map.

## When to use it

Use an octree occupancy map for 3D maps from laser scanners or depth cameras when the robot must tell free space from unknown space, for example for collision checking of a drone or a manipulator, or for [frontier-based exploration](/frontier-based-exploration/) in 3D. It saves memory over a dense 3D [occupancy grid map](/occupancy-grid-map/) when large parts of the volume are unknown or uniform, and it supports coarse queries at no extra cost. For a ground robot in a building, a 2D grid is simpler and faster. For dense surface reconstruction, where the surface itself matters more than free space, other representations such as distance fields are common. When the map is small and fully observed, a plain 3D array is faster, because a lookup costs one index computation and not $D$ pointer steps.

## Pitfalls

- **The maximum hides free space and unknown space.** A coarse block is occupied as soon as one voxel is, and a block with known free voxels and unknown voxels returns the free value; the maximum ignores unknown voxels. A planner that needs to stay out of unknown space must check for it separately.
- **Clamping loses information.** Near the bounds, the values no longer count the evidence, and the order of the updates matters. The bounds are a trade-off between confidence and how fast the map adapts to change; the values $-2$ and $3.5$ were found to work by experiment in the paper, and they are a heuristic.
- **Pruning needs exactly equal values.** Without clamping, two voxels with the same evidence in a different order can differ in the last bit, and the tree never prunes. Compare floats exactly, as line L10 does, so that pruning stays lossless.
- **One update per scan.** Inserting the beams of a sweeping scanner one by one can clear the occupied voxels of a flat surface seen at a shallow angle. Collect a sweep into one scan and let occupied win, as INSERT-SCAN does.
- **The map has a fixed extent.** A tree of depth $D$ covers $2^D s$ per axis around a fixed origin. A point outside has no key, so check the result of `key` before an update.
- **Deep recursion and many small objects.** In a language with costly objects, millions of small nodes take far more memory than the paper's numbers. Real implementations allocate the child array only for inner nodes and keep nodes small.

## Implementations

## History

Octrees as a hierarchical subdivision of 3D space go back to the early 1980s (Hornung et al. cite Meagher, 1982), and probabilistic occupancy grids to Moravec and Elfes (1985). Hornung, Wurm, Bennewitz, Stachniss and Burgard (2013) combined the two in the OctoMap framework, after an earlier workshop version in 2010. Their paper credits the clamping update to Yguel et al. (2007), the choice between the mean and the maximum of the children to Kraetzschmar et al. (2004), and the threshold compression to Fairfield et al. (2007). The key step of their design is that clamping makes many neighboring voxels exactly equal, so lossless pruning becomes effective on probabilistic maps.

## References
