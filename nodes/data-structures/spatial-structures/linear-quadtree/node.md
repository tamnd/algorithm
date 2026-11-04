---
tag: HXZGKW
kind: data-structure
slug: linear-quadtree
name: Linear quadtree
aliases:
- locational-code quadtree
area: data-structures/spatial-structures
level: advanced
summary: Pointerless quadtree stored as a sorted list of locational codes, usually Morton codes.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of stored blocks, N: the number of black pixels given to the build, D: the number of halvings from the image to a pixel, k: the number of reported blocks}
  time: {build: O(N log N), locate: O(log n), insert: O(D log n), delete: O(D log n), blocks_in_cell: O(log n + k)}
  space: {total: O(n)}
history:
  year: 1982
  people: [Irene Gargantini]
  note: Gargantini proposed to keep only the black leaves of a region quadtree, each as a locational code in base 4, in a sorted list; Abel, Smith and others then stored such codes in B-trees for database use.
prereqs: [region-quadtree, morton-encoding]
see_also: [z-order-curve, pr-quadtree, quadtree, b-plus-tree, binary-search, hilbert-curve, geohash, octree]
sources:
  - paper: doi:10.1145/358728.358741
    title: Irene Gargantini, An effective way to represent quadtrees, Communications of the ACM 25(12), 1982
    locator: the whole paper (black nodes as quaternary codes in sorted order)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the sections on pointerless quadtree representations and locational codes
  - paper: doi:10.1145/356924.356930
    title: Hanan Samet, The quadtree and related hierarchical data structures, ACM Computing Surveys 16(2), 1984
    locator: the section on region data and its discussion of pointerless representations
  - paper: "G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, IBM technical report, Ottawa, 1966"
    title: G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, IBM, 1966
    locator: the interleaving of the bits of two coordinates into one key for ordering a file
---

A linear quadtree stores a [region quadtree](/region-quadtree/) without pointers. It keeps only the black leaves, and writes each one as a *locational code*: the [Morton code](/morton-encoding/) of its lower left pixel together with its level. The codes go in one sorted list, and the order is the [Z-order](/z-order-curve/) of the blocks. Because the blocks are disjoint, a pixel lies in the block with the largest code not above its own, so one [binary search](/binary-search/) finds it, and the blocks inside any quadtree cell form one run of the list. The list can live in an array, or in a [B+ tree](/b-plus-tree/) on disk, which is how spatial databases have used it.

## In plain words

Take a black and white picture with a square number of pixels, and cut it like a region quadtree: a square that is all black or all white is kept whole, and a mixed one is cut into four.

Now throw away the tree. Keep only the black squares, and give each square a number that tells where it is. The numbers come from reading the picture in a Z pattern, so squares that are close in the picture often get close numbers.

Sort the numbers into a list. To ask whether a pixel is black, find its number in the list. To change a pixel, change a few entries of the list. No pointers are needed.

## The abstract type

The linear quadtree stores the set of black pixels of a $2^D \times 2^D$ binary image. It supports `locate(p)`, which gives the black block that holds the pixel $p$, or none if $p$ is white; `insert(p)` and `delete(p)`, which make one pixel black or white; and `blocks_in_cell(c)`, which lists the black blocks inside a quadtree cell $c$. It is a [spatial index](/spatial-index/) for raster data, and the same idea gives pointerless forms of [octrees](/octree/) and of point quadtrees.

## Representation

Write $z(x, y)$ for the Morton code of the pixel $(x, y)$: bit $i$ of $x$ goes to bit $2i$ of $z$ and bit $i$ of $y$ goes to bit $2i + 1$. A *block* $(c, \ell)$ is the aligned square of side $2^\ell$ whose pixels have the codes $c, c + 1, \ldots, c + 4^\ell - 1$; this is exactly a cell of the quadtree at height $\ell$, and $c$ is a multiple of $4^\ell$. The four children of the block $(c, \ell + 1)$ are $(c + k \cdot 4^\ell, \ell)$ for $k = 0, 1, 2, 3$, in the order southwest, southeast, northwest, northeast.

The structure is a list of blocks sorted by $c$. Gargantini wrote the same blocks as base 4 strings, with a digit per level and a "don't care" digit for the levels below the block; the pair (code, level) carries the same facts.

**Invariant (L).** (1) Each block $(c, \ell)$ has $0 \le \ell \le D$ and $4^\ell \mid c$. (2) The blocks are disjoint and sorted: each block ends before the next one starts. (3) No four siblings of one level are all in the list.

Parts 1 and 2 say the list is a set of disjoint quadtree cells, so it describes a set of black pixels. Part 3 says the blocks are maximal: four black siblings would be one black parent. With (L), the list is unique for a given image: it is the list of black leaves of the region quadtree, in Z-order.

## Operations

```pseudo id=main
BUILD(P)                                   ▷ P is a set of black pixels
L1  for each code z of P, in increasing order:
L2      push (z, 0) on a stack S
L3      while S has at least four blocks:
L4          let the top four be (c, ℓ), (c', ℓ'), ...; if they are not (c + k·4^ℓ, ℓ) for k = 0..3 with 4^(ℓ+1) | c then stop
L5          pop the four blocks
L6          push the parent (c, ℓ + 1)
                                           ▷ S, from bottom to top, is the list
LOCATE(z)                                  ▷ z is the code of a pixel
L7  i ← the last index with c_i ≤ z, by binary search
L8  if i exists and z < c_i + 4^(ℓ_i) then return block i
L9  return none
```

The build reads the codes in Z-order. A block is pushed only after all blocks before it in Z-order, so four complete siblings, if they exist, are the top four of the stack at the moment the last of them is pushed, and they merge at once. The merge can go on up the levels.

```pseudo id=update
INSERT(p)
L10 z ← the code of p; if LOCATE(z) finds a block then return false
L11 add (z, 0) to the list; (c, ℓ) ← (z, 0)
L12 while ℓ < D and the four siblings of (c, ℓ) are all in the list:
L13     remove them; (c, ℓ) ← their parent; add (c, ℓ) to the list
    return true

DELETE(p)
L14 z ← the code of p; i ← LOCATE(z); if none then return false
L15 remove block i, which is (c, ℓ)
L16 for j ← ℓ − 1 down to 0:
L17     add the three blocks of level j that are children of the level j + 1 cell of z, other than the one that holds z
    return true
```

Deleting a pixel from a black block of side $2^\ell$ leaves $3\ell$ blocks, three on each level below, which is the decomposition of the block with one pixel cut out.

## Example

Take $D = 2$, a $4 \times 4$ image, and the black pixels $(0,0), (1,0), (0,1), (1,1)$, the whole southwest quadrant, then $(2,0), (3,0), (2,1)$ in the southeast quadrant, and $(1,3)$ in the northwest.

| pixel | (0,0) | (1,0) | (0,1) | (1,1) | (2,0) | (3,0) | (2,1) | (1,3) |
|---|---|---|---|---|---|---|---|---|
| code $z$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 11 |

| step | what happens | list of (code, level) |
|---|---|---|
| build | codes 0 to 3 are pushed and merge into (0, 1); then 4, 5, 6 and 11 are pushed, with no merge, since 7 is missing | (0,1), (4,0), (5,0), (6,0), (11,0) |
| locate (1,1) | $z = 3$; the last code $\le 3$ is 0, and $3 < 0 + 4$ | the block (0, 1), the square of side 2 at (0, 0) |
| locate (3,1) | $z = 7$; the last code $\le 7$ is 6, and $7 \ge 6 + 1$ | none, the pixel is white |
| blocks in the cell $(2, 0)$, side 2 | the codes 4 to 7 form one run of the list | (4,0), (5,0), (6,0) |
| insert (3,1) | add (7, 0); the siblings 4, 5, 6, 7 are all there, so they merge into (4, 1); its siblings at level 1 are 0, 4, 8, 12, and 8 is missing | (0,1), (4,1), (11,0) |
| delete (0,0) | remove (0, 1); add the three children of the cell 0 at level 0 other than 0 itself | (1,0), (2,0), (3,0), (4,1), (11,0) |

The image has 8 black pixels and the region quadtree has 5 black leaves; the linear quadtree stores exactly these 5.

## Correctness

BUILD keeps (L) on the stack: a merged block is a black parent, and since the codes come in Z-order, a group of four siblings that is complete is complete on the top of the stack, so part 3 holds at the end. LOCATE is right because the blocks are disjoint and sorted: if any block holds $z$, it is the last one that starts at or before $z$. INSERT restores part 3 along the only path where it can fail, the ancestors of the new pixel. DELETE splits the block into the maximal blocks of the block minus one pixel; none of them can merge, since each has a sibling that holds the white pixel. The full proof is in the proofs folder.

## Complexity

The model is the word RAM, with codes of $2D$ bits in one word.

- **Size.** A linear quadtree has as many entries as the region quadtree has black leaves, and no internal nodes and no pointers. Gargantini's point was this saving: a pointer quadtree also stores the white leaves and the internal nodes.
- **Build.** Sorting the $N$ codes takes $O(N \log N)$; the stack pass is $O(N)$, since each block is pushed once and popped once.
- **Locate.** One binary search, $O(\log n)$, or $O(\log_B n)$ disk reads in a B+ tree with fan-out $B$.
- **Insert and delete.** At most $D$ merges or $3D$ new blocks, each one an update of the sorted list: $O(D \log n)$ with a balanced tree or B-tree, and $O(D n)$ in the worst case with a plain array, as in the code here.
- **Blocks in a cell.** The blocks inside a cell with codes $[c, c + 4^\ell)$ form one run of the list, so two binary searches give them: $O(\log n + k)$ for $k$ blocks.

| operation | time | case |
|---|---|---|
| build | $O(N \log N)$ | worst |
| locate | $O(\log n)$ | worst |
| insert | $O(D \log n)$ with a B-tree | worst |
| delete | $O(D \log n)$ with a B-tree | worst |
| blocks_in_cell | $O(\log n + k)$ | worst |
| space | $O(n)$ | total |

## Variants

- **Base 4 strings.** Gargantini's form writes each black block as a string of $D$ base 4 digits with a marker for the levels below the block. It orders the blocks in the same way.
- **Linear point quadtrees and octrees.** The same codes index the leaves of a [PR quadtree](/pr-quadtree/) or an [octree](/octree/), with three bits per level in three dimensions. Many particle codes and GPU programs sort points by Morton code and build the tree from the sorted list.
- **Hilbert keys.** Use the index of the [Hilbert curve](/hilbert-curve/) in place of the Morton code. Runs of the list then cover the cells more compactly, but the codes cost more to compute.
- **Geographic cells.** [Geohash](/geohash/) and many global grid systems use the same idea on the surface of the Earth: a cell is a prefix of a code, and the cells of a region are ranges of a sorted index.
- **Depth-first encodings.** Other pointerless forms store the tree as a string of node types in depth-first order, which is smaller but does not allow binary search.

## When to use it

Use a linear quadtree when the data is a raster or a set of cells, when it must be kept in a database or on disk, and when the main queries are "which block holds this pixel" and "which blocks are in this cell". It needs only a sorted index, which every database has. Use a pointer quadtree when the tree changes in big pieces or when you need to walk it often from parent to child, and use a plain bitmap when the image is small or has no large uniform areas.

## Pitfalls

- **Bit order.** The code must take the top bits of $x$ and $y$ first in significance, so that the blocks of a cell form one range. Mixing the order of $x$ and $y$ between the build and the search gives wrong answers with no error.
- **Comparing codes of different levels.** Sort by the code of the lower left pixel, padded to full depth. Codes of different lengths, compared as strings with no padding, do not sort in Z-order.
- **Forgetting to merge.** If insertion does not merge four complete siblings, the list still describes the right image, but it is no longer unique, and equality tests between two images by their lists fail.
- **Array updates.** Each insert or remove in a plain array moves the tail of the array. For many updates, keep the codes in a B-tree or a balanced search tree.

## Implementations

## History

Morton described in 1966 the interleaving of the bits of coordinates into one key, for a geographic file. Gargantini, in 1982, proposed to store a quadtree as the sorted list of the base 4 codes of its black leaves. Through the 1980s, Abel, Smith, Samet and others stored such codes in B-trees for geographic databases, and Samet's books describe the method and its relatives in detail.

## References
