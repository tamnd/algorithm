---
tag: F2JK2W
kind: data-structure
slug: spatial-occupancy-enumeration
name: Spatial occupancy enumeration
aliases:
- voxel representation
- exhaustive enumeration of solids
area: cad/solid-modeling
level: intro
summary: Represents a solid by the set of cells of a regular 3D grid that it fills. Booleans on cells are exact, but the shape is only approximated and the memory grows as n³.
model: word-ram
complexity:
  vars:
    n: the number of cells along each side of the grid
    m: the number of filled cells
    D: the depth of the octree, log₂ n
  time:
    classify: O(1)
    boolean: O(m)
    area: O(m)
    to_octree: O(m D)
  space:
    cell_set: Θ(m)
    bit_array: Θ(n^3)
prereqs: [r-set, regularized-set-operations]
see_also: [octree, region-quadtree, constructive-solid-geometry, boundary-representation, marching-cubes, mass-properties-of-solids, uniform-grid, signed-distance-function]
sources:
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the section on representation schemes, where spatial occupancy enumeration and cell decomposition are two of the schemes, with their domain, validity, unambiguity and uniqueness
  - paper: doi:10.1016/0146-664X(82)90104-6
    title: Donald Meagher, Geometric modeling using octree encoding, Computer Graphics and Image Processing 19(2), 129 to 147, 1982
    locator: the octree encoding of solids, its size, and the Boolean operations, motions and display on it
  - paper: "Chris L. Jackins and Steven L. Tanimoto, Oct-trees and their use in representing three-dimensional objects, Computer Graphics and Image Processing 14(3), 1980"
    locator: the oct-tree as the three-dimensional form of the region quadtree, and its construction from a voxel array
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: the chapter on decomposition models, with exhaustive enumeration, octrees and cell decompositions
  - paper: "Gregory M. Hunter and Kenneth Steiglitz, Operations on images using quad trees, IEEE Transactions on Pattern Analysis and Machine Intelligence 1(2), 1979, pp. 145 to 153"
    locator: the bound on the number of nodes of a quadtree by the perimeter of the region
---

Spatial occupancy enumeration stores a solid as a list of cells. Cut space into a regular grid of equal cubes, the *voxels*, and keep the cubes that the solid fills. The stored solid is the union of these closed cubes. This union is always a valid solid, an [r-set](/r-set/), and the Boolean operations become set operations on the lists of cells: a cell is in the union, intersection or difference exactly when the operation says so for the two lists. This is the [regularized](/regularized-set-operations/) operation, with no extra step. Point tests, volume and surface area are as simple. The price is that most solids are not unions of grid cubes, so the cells only approximate them, and the memory grows with the cube of the resolution. Requicha named the scheme in his survey of 1980, and Meagher's octree encoding of 1982 made it smaller.

## In plain words

Build the shape from small equal cubes, like a toy made of building blocks of one size on a fixed grid. To store it, list the grid places that hold a block.

To join two shapes, keep each place that holds a block in either list. To find their common part, keep only the places in both lists. To cut one shape out of another, remove from the first list each place that the second list also has. These rules never make a thin skin or a loose line, because every result is again a set of whole blocks.

The problem is the grid. A sphere or a sloped face becomes a staircase. To make the steps smaller, you need more blocks, and halving the size of the block makes eight times as many. A tree that groups large empty and full regions, the octree, saves much of this memory.

## The abstract type

Fix the grid of unit cubes $c(i, j, k) = [i, i + 1] \times [j, j + 1] \times [k, k + 1]$ for integers $i, j, k$; another grid step $h$ is a scaling of this one. A voxel set $V$ is a finite set of integer triples, and it stands for the solid $[V] = \bigcup_{c \in V} c(c)$.

- $\mathrm{SAMPLE}(S, box)$: the set of cells of $box$ whose centres lie in the solid $S$. This is one common way to make $V$ from a CAD model, a scan or a medical image.
- $\mathrm{UNION}(V, W)$, $\mathrm{INTERSECTION}(V, W)$ and $\mathrm{DIFFERENCE}(V, W)$: the voxel sets of $[V] \cup^* [W]$, $[V] \cap^* [W]$ and $[V] -^* [W]$.
- $\mathrm{CLASSIFY}(V, p)$: IN, ON or OUT, as $p$ is in the interior of $[V]$, on its boundary or outside it.
- $\mathrm{VOLUME}(V)$ and $\mathrm{AREA}(V)$: the volume and the boundary area of $[V]$.
- $\mathrm{OCTREE}(V)$ and its inverse: the octree of $V$ inside a cube of side $2^D$, and back.

## Representation

Three forms are common, and they store the same set.

| form | storage | membership test | good for |
|---|---|---|---|
| bit array | $n^3$ bits for the box of $n \times n \times n$ cells | one index computation | dense data in a fixed box, as from a scanner |
| set of cells | one integer triple per filled cell, in a hash table | one hash look up, expected $O(1)$ | sparse sets and unbounded space |
| octree | one node per block of the tree, each leaf EMPTY or FULL | a walk of $O(D)$ steps | solids with large uniform regions |

The code of this page uses the set of cells, so all costs on it are expected costs under hashing. The point $p$ and the corners of the cells are exact rationals and integers, so every test is exact.

## Operations

```pseudo id=main
CLASSIFY(V, p)                         ▷ IN, ON or OUT for the closed union [V]
L1  for j ← 1 to 3: R_j ← {⌊p_j⌋ − 1, ⌊p_j⌋} if p_j is an integer, else {⌊p_j⌋}
L2  k ← the number of cells c ∈ R₁ × R₂ × R₃ with c ∈ V
L3  if k = 0 then return OUT
L4  if k = |R₁ × R₂ × R₃| then return IN
L5  return ON

BOOLEAN(V, W, op)                      ▷ op is or, and, or and-not
L6  return {c ∈ V ∪ W : op(c ∈ V, c ∈ W)}

OCTREE(C, corner, s)                   ▷ C: the cells of V in the cube of side s at corner
L7  if C = ∅ then return EMPTY
L8  if |C| = s³ then return FULL
L9  split C among the 8 cubes of side s/2 and return a node with their 8 OCTREE results
```

Line L1 finds the cells that contain $p$. On an axis where $p_j$ is not an integer, only the cell $\lfloor p_j \rfloor$ covers it; where $p_j$ is an integer, $p$ lies on a grid plane and both neighbour cells touch it. So $p$ is in 1, 2, 4 or 8 closed cells, as it is inside a cell, on a face, on an edge or at a corner. If none of them is in $V$, the point is outside; if all of them are, a small ball around $p$ is filled and $p$ is inside; otherwise it is on the boundary.

Line L6 is the whole Boolean operation. UNION takes or, INTERSECTION takes and, and DIFFERENCE takes "in $V$ and not in $W$".

The volume of $[V]$ is the number of cells. The area is the number of pairs of a cell in $V$ and one of its six face neighbours not in $V$: each such pair is one unit square of the boundary.

To combine two octrees of the same cube, walk them together. Where both nodes are leaves, apply op to their two values. Where one is a leaf, treat it as eight equal children. If all eight results are EMPTY, or all are FULL, return one leaf. This walk visits each node of each input tree at most once.

## Example

Take two boxes, one cell thick in $z$. $A$ fills the cells with $0 \le i \le 2$ and $0 \le j \le 1$, so $[A] = [0, 3] \times [0, 2] \times [0, 1]$, and $B$ fills those with $2 \le i \le 3$ and $0 \le j \le 1$, so $[B] = [2, 4] \times [0, 2] \times [0, 1]$. They overlap in the column $i = 2$.

| result | cells | volume | area |
|---|---|---|---|
| $A$ | 6 | 6 | 22 |
| $B$ | 4 | 4 | 16 |
| $A \cup^* B$ | 8 | 8 | 28 |
| $A \cap^* B$ | the 2 cells with $i = 2$ | 2 | 10 |
| $A -^* B$ | the 4 cells with $i \le 1$ | 4 | 16 |

The check $\mathrm{vol}(A \cup^* B) + \mathrm{vol}(A \cap^* B) = 8 + 2 = 6 + 4$ holds. Now classify some points against $A -^* B = [0, 2] \times [0, 2] \times [0, 1]$.

| point $p$ | cells around $p$ (L1) | cells in $A -^* B$ | class |
|---|---|---|---|
| $(1, 1, \tfrac12)$ | 4 cells with $i, j \in \{0, 1\}$ | 4 | IN |
| $(2, 1, \tfrac12)$ | 4 cells with $i \in \{1, 2\}$, $j \in \{0, 1\}$ | 2 | ON |
| $(\tfrac52, 1, \tfrac12)$ | 2 cells with $i = 2$ | 0 | OUT |
| $(0, 0, 0)$ | 8 cells around the corner | 1 | ON |

The point $(2, 1, \tfrac12)$ is the reason for regularization. It lies in the closed box $[B]$, so the ordinary difference $[A] \setminus [B]$ does not contain it, and that set has no face at $x = 2$. It is not closed. The cell rule keeps the face, and CLASSIFY reports ON.

The octree of $A \cup^* B$ in the cube $[0, 4)^3$ has depth 2. The root has 8 children of side 2. The two children at $z \in [0, 2)$ and $y \in [0, 2)$ hold 4 of their 8 cells each, so they are split into 8 unit leaves, 4 FULL and 4 EMPTY. The other 6 children are EMPTY leaves. So the tree has $1 + 8 + 16 = 25$ nodes for 8 cells: for a solid this thin, the tree is larger than the list.

## Correctness

The proof page shows four facts. First, for any finite $V$ the set $[V]$ is closed and regular, so it is an r-set. Second, the set operations on cells give exactly the regularized operations: off the grid planes a point is in one open cell, and the regularized result is the closure of its interior, which these points decide. Third, CLASSIFY is exact, because the cells found in L1 cover a ball around $p$ and the open part of each one comes as close to $p$ as we like. Fourth, the area count is the area of the boundary, because a point inside a grid square is on the boundary exactly when one of the two cells beside it is in $V$.

The proof page also proves the error of SAMPLE: a cell that does not meet the boundary of $S$ is kept exactly when it lies in $S$. So $S$ and $[\mathrm{SAMPLE}(S)]$ differ only inside cells that the boundary of $S$ crosses, and with grid step $h$ every point of the difference is within $\sqrt3\,h$ of the boundary of $S$.

The tests compare the operations with a brute force built only on ordinary point membership in the operands, by a scan over their cells. For random voxel sets, every point of the half-integer grid is classified both by CLASSIFY on the result and by the operation applied to the operands at the eight points $p + s/4$, $s \in \{-1, +1\}^3$, which lie inside cells. Points with denominator 7 are on no grid plane, and there CLASSIFY must agree with the ordinary formula. The tests also check the area against a count of ON square centres, the volume identity above, the sampling error on a ball, and the octree round trip and octree Booleans against the cell sets.

## Complexity

With a hash table, CLASSIFY makes at most 8 look ups, so it takes expected $O(1)$ time. BOOLEAN looks at each cell of $V$ and $W$ once, so it takes expected $O(m)$ time for $m = |V| + |W|$. VOLUME is $O(1)$ if the count is stored, and AREA is $O(m)$, six look ups per cell. The set of cells takes $\Theta(m)$ space. The bit array takes $\Theta(n^3)$ bits whatever the solid, and its Booleans take $O(n^3 / w)$ word operations on a machine with words of $w$ bits.

OCTREE splits the cells once per level, so it takes $O(m D)$ time, and each level has at most $m$ nonempty nodes, so the tree has $O(m D)$ nodes. The joint walk of two octrees takes time linear in the sum of their sizes, because each call pairs a node position that is present in at least one of the two trees.

The real cost is the resolution. A part of 1 m at a cell of 1 mm needs $10^9$ cells, 125 MB as bits, and a cell of 0.5 mm needs 8 times more. The octree helps because its size follows the boundary, not the volume. For a region quadtree, Hunter and Steiglitz proved a bound of $O(p + D)$ nodes for a region of perimeter $p$; for a ball the octree size here grows by about 4 when the radius doubles, while the box of cells grows by 8. These ball figures are measured, not proved:

| radius $r$ | cells in the sample | octree nodes | cells in the cube $(2r)^3$ | AREA | $4 \pi r^2$ |
|---|---|---|---|---|---|
| 4 | 280 | 457 | 512 | 312 | 201 |
| 8 | 2176 | 1737 | 4096 | 1248 | 804 |
| 16 | 17256 | 6985 | 32768 | 4872 | 3217 |
| 32 | 137376 | 29065 | 262144 | 19368 | 12868 |

## Variants

- **Octree.** [Meagher's octree encoding](/octree/) groups each uniform block of $2^k \times 2^k \times 2^k$ cells into one leaf. Booleans walk the two trees together, and a rotation by a multiple of $90°$ about an axis permutes the children.
- **Linear octree.** Store only the FULL leaves, each as its [Morton code](/morton-encoding/) and its level, in sorted order, as Gargantini did for the [linear quadtree](/linear-quadtree/).
- **Run lengths.** Store each grid line as the list of runs of filled cells, as in [run-length encoding](/run-length-encoding/). The Boolean operations merge the runs line by line.
- **Cell decomposition.** Requicha's more general scheme glues cells of different shapes, such as tetrahedra or curved bricks, that meet only on their faces. Finite element meshes are decompositions of this kind.
- **Values in the cells.** Store a density, a material or a [signed distance](/signed-distance-function/) per cell instead of one bit. [Marching cubes](/marching-cubes/) then makes a smooth surface between the samples, and [TSDF fusion](/tsdf-fusion/) builds such grids from depth images.
- **Two dimensions.** The same scheme on pixels gives the binary image and the [region quadtree](/region-quadtree/).

## When to use it

Use a voxel set when the data comes as samples on a grid, as from CT and MRI scans, when the shape is noisy or very complex and its exact faces do not matter, or when an algorithm needs many fast point tests and Booleans of the same size, as in the simulation of machining, the slicing for 3D printing or the planning of paths. A [B-rep](/boundary-representation/) or a [CSG tree](/constructive-solid-geometry/) is better for a precise CAD part with flat and curved faces: it is exact, it is small, and it can be moved by any rigid motion. A voxel set is exact only for solids that are unions of grid cubes.

## Pitfalls

- **Resolution.** Halving the cell multiplies the memory of a dense grid by 8. Choose the cell from the smallest feature that must survive, and prefer an octree or a sparse set when most cells are empty or full.
- **Thin features vanish.** SAMPLE keeps a cell by its centre, so a wall or a rod thinner than one cell can disappear or break into parts. Sampling by "the cell meets $S$" keeps them, but the result is larger than $S$.
- **The area is wrong in the limit.** AREA counts the steps of the staircase, and on a slope the steps do not get flatter when the cells get smaller. For a convex solid each grid line that meets the sample gives exactly 2 boundary squares, so the area tends to the sum of the areas of the shadows in the three axis directions, counted twice. For a ball of radius $r$ this is $6 \pi r^2$, 1.5 times the true $4 \pi r^2$, as the table shows. Use the cells for volume, and fit a surface, for example by marching cubes, for area.
- **Motions.** Only translations by whole cells and the 24 rotations of the cube are exact. Any other motion must sample the moved solid again, and the errors grow with each step.
- **Different grids.** Booleans are exact only when both operands use the same grid. Two grids with different steps or origins must be sampled onto one first.
- **Non-manifold results.** Two cells that meet only along an edge or at a corner give a valid r-set whose boundary is not a manifold. A [manifold](/manifold-solid/) B-rep made from the cells must treat these edges and vertices with care.

## Implementations

## History

Arrays of volume samples came from medical imaging and image processing in the 1970s. In 1980 Requicha's survey put solids on a formal basis and listed spatial occupancy enumeration among the representation schemes, as an unambiguous and unique scheme whose domain is limited to unions of grid cells; he also named the more general cell decompositions. In the same year Jackins and Tanimoto described oct-trees for three-dimensional objects, after the quadtrees of images, and Meagher's report of 1980 and paper of 1982 developed octree encoding for solid modeling, with Booleans, motions and display that work on the tree. Mäntylä's book of 1988 treats exhaustive enumeration and octrees together as decomposition models.

## References
