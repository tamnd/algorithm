---
tag: 74TKQQ
kind: data-structure
slug: region-quadtree
name: Region quadtree
aliases:
- image quadtree
- regional quadtree
area: data-structures/spatial-structures
level: core
summary: Quadtree that recursively subdivides a binary image or region into homogeneous quadrants.
model: word-ram
complexity:
  vars: {N: the side of the image in pixels (a power of 2), D: the number of halvings from the image to a pixel so that N = 2^D, n: the number of nodes of the tree, p: the perimeter of the black region in pixel edges}
  time: {build: O(N^2), get: O(D), set: O(D), union: O(n), black_area: O(n)}
  space: {total: O(n), nodes_for_a_region: O(p + D)}
history:
  year: 1971
  people: [Allen Klinger, Gregory M. Hunter, Kenneth Steiglitz]
  note: Klinger proposed in 1971 to divide a picture into quadrants until each part is uniform; Hunter and Steiglitz in 1979 gave the operations on images stored this way and the bound on the number of nodes by the perimeter.
prereqs: [quadtree, tree]
see_also: [linear-quadtree, octree, pr-quadtree, mx-cif-quadtree, z-order-curve, run-length-encoding, connected-component-labeling, image-segmentation]
sources:
  - paper: doi:10.1145/356924.356930
    title: Hanan Samet, The quadtree and related hierarchical data structures, ACM Computing Surveys 16(2), 1984, pp. 187 to 260
    locator: the section on region data (the region quadtree, its history from Klinger, the node count theorem, and set operations)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on the region quadtree and region octree
  - paper: doi:10.1109/TPAMI.1979.4766900
    title: Gregory M. Hunter and Kenneth Steiglitz, Operations on images using quad trees, IEEE Transactions on Pattern Analysis and Machine Intelligence 1(2), 1979, pp. 145 to 153
    locator: the union and intersection of quadtrees, and the bound on the number of nodes of a polygon by its perimeter
  - paper: "Allen Klinger, Patterns and search statistics, in Optimizing Methods in Statistics, J. S. Rustagi (editor), Academic Press, 1971, pp. 303 to 337"
    title: Allen Klinger, Patterns and search statistics, 1971
    locator: the recursive division of a picture into quadrants until each part is uniform
---

A region quadtree stores a $2^D \times 2^D$ binary image as a tree in which each node is a square block of pixels: a block of one color is a leaf, and a block of mixed colors is an internal node with four children, its quadrants. Large areas of one color become a single leaf, so the tree is small when the image has large uniform regions, and its size depends on the length of the region boundaries, not on their area. Get and set of one pixel cost $O(D)$, and the union, the intersection and the area of images come from one walk over the trees. Allen Klinger proposed the idea in 1971, and Hunter and Steiglitz gave the main operations in 1979.

## In plain words

Look at a black and white picture. If it is all black or all white, write down one color and stop. If not, cut it into four equal squares and do the same for each square. Keep cutting until every square has one color, or is one pixel.

The cuts make a tree. The top is the whole picture, each cut gives four children, and each uncut square is a leaf with its color. A picture with a big black shape needs few leaves inside the shape and many leaves along its edge.

To read one pixel, go down from the top, into the square that holds it, until you reach a leaf. To combine two pictures, walk down both trees together, and stop where either one has a leaf.

## The abstract type

The region quadtree stores a map from the pixels $\{0, \ldots, N-1\}^2$ of a square image to the colors $\{0, 1\}$, white and black, with $N = 2^D$. The operations are `build(image)`, `get(x, y)`, `set(x, y, c)`, `black_area()`, and the set operations `union(A, B)` and `intersection(A, B)` of two images of the same size. It is a representation of a region, the set of black pixels, not an index of separate objects, so it does not implement a [spatial index](/spatial-index/) by itself. The [PR quadtree](/pr-quadtree/) and the [MX-CIF quadtree](/mx-cif-quadtree/) apply the same cuts to points and rectangles.

## Representation

A *block* is a square $[x_0, x_0 + s) \times [y_0, y_0 + s)$ of pixels, where $s$ is a power of 2 and $x_0, y_0$ are multiples of $s$. The root is the block of the whole image, $x_0 = y_0 = 0$ and $s = N$. A block of side $s \ge 2$ has four quadrants of side $s/2$, numbered NW = 0, NE = 1, SW = 2 and SE = 3, with row 0 at the top. Pixel $(x, y)$ lies in quadrant
$$q = 2\,[y \ge y_0 + s/2] + [x \ge x_0 + s/2],$$
where $[\cdot]$ is 1 if the test holds and 0 if not. In binary, the bits of $q$ on the way down are the bits of $y$ and $x$ from the top bit, so the path to a pixel spells its [Morton code](/morton-encoding/).

A node is a *leaf* with a color, or an *internal node* with four children in quadrant order. A node of side $s$ stands for its block.

**Invariant (Q).** (1) The leaves partition the image, and each pixel has the color of the leaf whose block holds it. (2) The tree is *maximal*: no internal node has four leaf children of one color.

Part 2 makes the tree unique: for each image there is exactly one tree that satisfies (Q), because a block is a leaf exactly when it has one color. The proof is in the proofs folder. Two images are equal exactly when their trees are equal, and a program can compare them in time linear in the size of the trees.

The *linear quadtree* drops the pointers and keeps only the black leaves as a sorted list of locational codes. See the [linear quadtree](/linear-quadtree/).

## Operations

```pseudo id=main
BUILD(image)                                ▷ bottom up, one level of blocks at a time
L1  make a leaf for each pixel, with its color; s ← 1
L2  while s < N:
L3      for each block of side 2s, take the nodes of its four quadrants, in the order NW, NE, SW, SE
L4      if the four are leaves of one color c then the block is a leaf of color c
L5      else the block is an internal node with the four as its children; s ← 2s

GET(x, y)
L6  u ← the root; while u is internal:
L7      go into the child of quadrant q = 2 [y ≥ y0 + s/2] + [x ≥ x0 + s/2]
L8  return the color of u

SET(x, y, c)
L9  if GET(x, y) = c then return
L10 u ← the root; while the side of u is more than 1: record u on the path, go into the quadrant of (x, y)
L11     when that child is a leaf of side at least 2, first replace it by an internal node with four leaves of its color
L12 make the pixel a leaf of color c
L13 go back up the path: at each node, if its four children are leaves of one color, replace it by one leaf of that color
```

BUILD merges four equal leaves at once, so every node it makes keeps part 2 of (Q). SET first goes down to the pixel and splits each leaf on the way into four leaves of the same color, which does not change the image. It then sets the pixel and merges upward, which restores part 2. Merges can only happen on the path, since no other node changed, and they stop at the first node that does not merge. In the code, a merge test at a node that did not change is harmless, so it can run up to the root.

```pseudo id=union
UNION(A, B)                                  ▷ A and B are nodes for the same block
L14 if A or B is a black leaf then return a black leaf
L15 if A is a white leaf then return B; if B is a white leaf then return A
L16 children ← UNION of the four pairs of children; merge them as in L4 and L5 and return the result
INTERSECTION(A, B) is the same with the colors swapped:
L17 a white leaf wins, a black leaf returns the other side, and the merge step is the same
```

UNION goes down the two trees together and stops at the first leaf on either side, so it visits at most $n_A + n_B$ nodes. The merge step in line L16 is needed: the union of two quadrants that are both mixed may be all black.

## Example

Take $N = 8$, so $D = 3$, and the image below, with row 0 at the top and $x$ from left to right. A 1 is black.

```text
y=0  0 0 0 0 0 0 0 0
y=1  0 0 0 0 0 0 0 0
y=2  0 0 0 0 1 1 1 1
y=3  0 0 0 0 1 1 1 1
y=4  0 0 0 1 1 1 1 1
y=5  0 0 1 1 1 1 1 1
y=6  0 0 1 1 1 1 0 0
y=7  0 0 1 1 1 1 0 0
```

BUILD gives this tree, with W for a white leaf and B for a black leaf, and children in the order NW, NE, SW, SE:

| block | side | node |
|---|---|---|
| root | 8 | internal: [NW, NE, SW, SE] |
| NW, $x, y \in [0, 4)$ | 4 | W |
| NE, $x \in [4, 8)$, $y \in [0, 4)$ | 4 | internal: [W, W, B, B] |
| SW, $x \in [0, 4)$, $y \in [4, 8)$ | 4 | internal: [W, internal: [W, B, B, B], W, B] |
| SE, $x, y \in [4, 8)$ | 4 | internal: [B, B, B, W] |

The tree has 21 nodes, of which 16 are leaves, while the image has 64 pixels. The black area is $4 + 4 + 1 + 1 + 1 + 4 + 4 + 4 + 4 = 27$ pixels, read off the black leaves by their sides.

- GET(5, 3) goes into the root's quadrant $2 \cdot 0 + 1 = 1$ (NE), then into quadrant $2 \cdot 1 + 0 = 2$ (SW of NE), a black leaf: the answer is 1.
- SET(2, 4, 1) makes the leaf at pixel (2, 4) black. Its parent, the block $[2, 4) \times [4, 6)$, now has four black leaves and merges into one black leaf. The SW block is then [W, B, W, B], which is mixed, so the merging stops. The tree has 17 nodes and 13 leaves, and the black area is 28.
- SET(0, 0, 1) on the first image must split the white NW leaf of side 4 into four leaves, and then the white leaf of side 2 at its NW corner into four pixels. The tree grows by 8 nodes, to 29 nodes and 22 leaves. Setting the pixel back to 0 merges both levels again, and gives back the tree of the first image.

## Correctness

BUILD is correct by induction on $s$: after the round for side $s$, each block of side $s$ has the unique maximal tree of its pixels, because a block is one leaf exactly when its four quadrants are leaves of one color. GET follows the quadrant rule, which picks the child whose block holds the pixel, until a leaf, and part 1 of (Q) gives its color. SET splits leaves without changing the image, changes one pixel, and merges along the path, which is the only place where part 2 can fail. UNION and INTERSECTION are correct by induction on the side of the blocks, since the union with a black block is black and the union with a white block is the other block. The full proof is in the proofs folder.

## Complexity

The model is the word RAM. Let $N = 2^D$ be the side of the image and $n$ the number of nodes of the tree.

- **Build.** The bottom-up build makes $N^2/s^2$ blocks of side $s$, for a total of $N^2 (1 + 1/4 + 1/16 + \cdots) < \frac{4}{3} N^2$ steps, so $O(N^2)$ time, linear in the number of pixels.
- **Get and set.** The path from the root to a pixel has $D + 1$ nodes, so GET is $O(D)$. SET splits and merges at most one node per level, each at $O(1)$ cost, so it is $O(D)$, and it adds at most $4D$ nodes.
- **Union, intersection and area.** UNION visits each node of the two trees at most once, so $O(n_A + n_B)$. The area adds $s^2$ over the black leaves, $O(n)$.
- **Size.** Each internal node has 4 children, so a tree with $L$ leaves has $(L - 1)/3$ internal nodes and $n = (4L - 1)/3$. In the worst case, a checkerboard, every pixel is a leaf, and $n = (4N^2 - 1)/3$.
- **Size of a region.** The *quadtree complexity theorem* of Hunter and Steiglitz bounds the number of nodes of a region with perimeter $p$, measured in pixel edges, by $O(p + D)$: a block of side $s$ is internal only if the boundary passes through it or very near it, and the boundary meets $O(p/s + 1)$ blocks of side $s$. Adding over the $D + 1$ sizes gives $O(p + D)$. The size grows with the boundary, not with the area.

| operation | time | case |
|---|---|---|
| build | $O(N^2)$ | worst |
| get | $O(D)$ | worst |
| set | $O(D)$ | worst |
| union, intersection | $O(n_A + n_B)$ | worst |
| black area | $O(n)$ | worst |
| space | $O(n)$, and $O(p + D)$ for a region of perimeter $p$ | worst |

## Variants

- **Linear quadtree.** Keeps only the black leaves as sorted locational codes, with no pointers. See the [linear quadtree](/linear-quadtree/).
- **Region octree.** The same in three dimensions, with eight octants per node, for voxel data. See the [octree](/octree/).
- **Gray images and labels.** A leaf can hold any value instead of a color, with the rule that a block is a leaf when all its pixels have the same value. With labels, the tree supports [connected component labeling](/connected-component-labeling/) and [image segmentation](/image-segmentation/) by split and merge.
- **Point and rectangle quadtrees.** The same cuts, with a different stop rule: the [PR quadtree](/pr-quadtree/) stops when a block has at most one point, and the [MX-CIF quadtree](/mx-cif-quadtree/) stores each rectangle at the smallest block that holds it.
- **Bintree.** Cuts a block in two, along $x$ and $y$ in turn, so each node has two children. It has at most as many leaves as the quadtree of the same image.
- **Run-length codes.** For images with long runs along rows, [run-length encoding](/run-length-encoding/) is a simpler alternative that does not see vertical structure.

## When to use it

Use a region quadtree for a binary or labeled raster with large uniform regions, such as maps of land use, masks in image processing, or occupancy grids in robotics, when you need set operations, area, or a coarse view at several resolutions. The tree is small when the boundary is short, and union and intersection run in time linear in the trees. Use a plain bit array when the image is small or full of detail, because the tree then has more nodes than pixels. Use the [linear quadtree](/linear-quadtree/) for images on disk.

## Pitfalls

- **Forgetting to merge.** If SET skips line L13, the tree still gives correct colors, but it is no longer maximal, it grows, and equal images no longer have equal trees.
- **Not splitting first.** SET must split a large leaf down to the pixel before it changes the color. Changing the leaf itself changes a whole block.
- **Union without a merge.** The union of two mixed blocks can be all black. Without the merge in line L16, the result is correct but not maximal.
- **Image sizes that are not powers of 2.** Pad the image with white to the next power of 2. The padding costs at most $O(D)$ more nodes per side, but the coordinates of blocks must use the padded size.
- **Quadrant order.** The order NW, NE, SW, SE must be the same in every operation and in both trees of a union. With $y$ up instead of down, the names of the quadrants change but the bit rule does not.
- **Recursion depth.** The tree has depth $D$, so recursion is safe for images, but code that recurses over the leaves of a large tree should use an explicit stack.

## Implementations

## History

Allen Klinger described in 1971 the division of a picture into quadrants until each part is uniform, as a way to search images. Gregory Hunter, in his Princeton thesis of 1978, and Hunter and Steiglitz in 1979 gave the operations on images stored as quadtrees, among them union and intersection, and proved the bound on the number of nodes of a polygon by its perimeter. Charles Dyer, Azriel Rosenfeld and Hanan Samet then studied conversions between quadtrees, rasters and boundary codes, and Samet's survey of 1984 named the structure the region quadtree. Irene Gargantini removed the pointers in 1982, with the linear quadtree.

## References
