---
tag: MMDM7B
kind: data-structure
slug: s2-cell-hierarchy
name: S2 cell hierarchy
aliases:
- S2 geometry
- S2 library
area: data-structures/spatial-structures
level: research
summary: Hierarchical decomposition of the sphere into quadrilateral cells indexed along a Hilbert curve.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {L: the number of levels (30 in S2), k: the level of a cell}
  time: {encode: O(L), parent: O(1), children: O(1), contains: O(1)}
  space: {cell: O(1)}
history:
  year: 2011
  people: [Eric Veach]
  note: Eric Veach designed the S2 library at Google; the code was released as open source, and the C++ version with its documentation appeared at s2geometry.io in 2017.
prereqs: [quadtree, hilbert-curve, space-filling-curve]
see_also: [geohash, discrete-global-grid-system, hilbert-curve, z-order-curve, linear-quadtree, morton-encoding, region-quadtree, spatial-index]
sources:
  - url: https://s2geometry.io/devguide/s2cell_hierarchy
    title: S2 Geometry, the S2 cell hierarchy (developer guide)
    locator: the cube faces, the quadtree of 30 levels, the Hilbert curve order, the 64-bit cell id with its face bits, position bits and trailing 1 bit, the quadratic projection, and the cell statistics
  - url: https://github.com/google/s2geometry
    title: S2 Geometry library, C++ source code (s2cell_id.h, s2coords.h and s2coords.cc)
    locator: the functions XYZtoFaceUV, UVtoST, STtoIJ and FromFaceIJ, and the Hilbert tables kIJtoPos, kPosToIJ and kPosToOrientation
  - book: isbn:9780387942650
    title: Hans Sagan, Space-Filling Curves, Springer, 1994
    locator: Chapter 2, the Hilbert curve and its construction by rotated and reflected quarters
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, the region quadtree, the linear quadtree with locational codes, and space-filling orderings of the cells
---

The S2 cell hierarchy divides the surface of the sphere into cells, each cell into four, and so on for 30 levels, and gives each cell a 64-bit number, its *cell id*. The sphere is first projected onto the six faces of a cube; each face is a [quadtree](/quadtree/) of square cells, and the cells of a level are numbered in the order of a [Hilbert curve](/hilbert-curve/) that runs over all six faces. With this numbering, the parent of a cell, its children, and the test "cell $a$ contains cell $b$" take a few bit operations, and the cells of a region fall into a few ranges of ids, which an ordinary sorted index, such as a [B-tree](/b-tree/), can store and search. The S2 library of Google, designed by Eric Veach, uses it for geographic indexing.

## In plain words

Put the Earth inside a box. Each point of the Earth seen from the center lands on one of the six sides of the box. Each side is a square, so you can cut it into four squares, cut each of those into four, and so on, like a map grid that gets finer at each step. After 30 steps the squares on the ground are about a centimeter wide.

Now walk through the squares of one step in a fixed path that never jumps: each square is next to the one before it. Write down where each square comes in that path. Squares that are near each other on the path are near each other on the Earth. A big square is a run of numbers on the path of a finer step, so to ask "is this small square inside that big one", you only compare two numbers.

## The abstract type

A cell hierarchy is a set of cells on the sphere with a level function, such that the cells of each level cover the sphere without overlap, and each cell of level $k < 30$ is the union of four cells of level $k + 1$, its children. The operations are: the leaf cell (level 30) that contains a point; the ancestor of a cell at a level; the four children; the test of containment; and the order of cells along the curve, which turns a region into a list of id ranges. As a [spatial index](/spatial-index/), a set of points is stored as a sorted list of their leaf ids, and a region query becomes a few range scans of that list.

## Representation

**From a point to a face.** A point is a unit vector $p = (x, y, z)$; from latitude and longitude, $x = \cos\phi \cos\lambda$, $y = \cos\phi \sin\lambda$ and $z = \sin\phi$. The *face* is the axis of the coordinate of largest absolute value: 0, 1, 2 for $x, y, z$ when it is positive, and 3, 4, 5 when it is negative. Dividing by that coordinate gives the point $(u, v)$ in $[-1, 1]^2$ where the ray from the center meets the face. Each face has its own axes for $u$ and $v$, chosen by S2 so that the curve is continuous from face to face; for face 0, $u = y/x$ and $v = z/x$.

**The quadratic projection.** The cells of a uniform grid in $(u, v)$ are larger at the center of a face than at its corners, after projection to the sphere. S2 maps each coordinate by $s = \frac{1}{2}\sqrt{1 + 3u}$ for $u \ge 0$ and $s = 1 - \frac{1}{2}\sqrt{1 - 3u}$ for $u < 0$, into $[0, 1]$, which makes the areas of cells of one level closer to each other. Then $i = \lfloor 2^{30} s \rfloor$ and $j = \lfloor 2^{30} t \rfloor$, clamped to $[0, 2^{30} - 1]$, are the integer coordinates of the leaf cell on the face.

**The Hilbert order.** At each level, the four children of a cell are numbered 0 to 3 in the order of a Hilbert curve, whose shape in each cell depends on an *orientation*: two bits, *swap* (exchange $i$ and $j$) and *invert* (reverse both). For the canonical orientation, the children with bits $(i, j)$ = (0, 0), (0, 1), (1, 1), (1, 0) come at positions 0, 1, 2, 3. The child at position 0 has its orientation swapped, the one at position 3 swapped and inverted, and the two in the middle keep it. Face $f$ starts with the orientation swap if $f$ is odd, which joins the curves of the six faces into one closed curve.

**The cell id.** A cell of level $k$ has the 64-bit id

$$\text{id} = f \cdot 2^{61} + \sum_{l=1}^{k} p_l \cdot 2^{61 - 2l} + 2^{60 - 2k},$$

where $f$ is the face and $p_1, \ldots, p_k$ are the positions of the cell and its ancestors among their siblings. So the id is 3 bits of face, then 2 bits for each level, then a 1 bit, then zeros. The lowest 1 bit marks the level: it is at bit $60 - 2k$. A face is $f \cdot 2^{61} + 2^{60}$. The *token* of a cell is its id in hex with the trailing zeros removed.

**Invariant.** For each cell $c$ of level $k$, the leaf ids of the leaf cells inside $c$ are exactly the odd numbers in $[\text{id}(c) - 2^{60 - 2k} + 1, \ \text{id}(c) + 2^{60 - 2k} - 1]$. In particular, the ids of a level, in increasing order, are the cells in Hilbert order.

## Operations

```pseudo id=main
FROM-POINT(p)
L1  face ← axis of the largest |coordinate| of p, plus 3 if that coordinate is negative; (u, v) ← projection on the face
L2  s ← QUADRATIC(u); t ← QUADRATIC(v)
L3  i ← clamp(⌊2^30 s⌋); j ← clamp(⌊2^30 t⌋)
L4  orientation ← face mod 2 (swap for odd faces); pos ← 0
L5  for level bits b = 29 down to 0:
L6      q ← IJ-TO-POS[orientation][(bit b of i, bit b of j)]; pos ← 4 pos + q
L7      orientation ← orientation XOR POS-TO-ORIENTATION[q]
L8  return face · 2^61 + pos · 2 + 1
PARENT(id, k)
L9  b ← 2^(60 − 2k)                         ▷ the lowest set bit of a cell of level k
L10 return (id with all bits below b cleared) + b
CHILDREN(id)
L11 b ← lowest set bit of id; c ← b / 4
L12 return id − b + c + 2 c · q, for q = 0, 1, 2, 3
CONTAINS(a, b)
L13 return range_min(a) ≤ b ≤ range_max(a), where range_min(a) = a − (lsb(a) − 1) and range_max(a) = a + (lsb(a) − 1)
```

**Levels and parents.** The level of an id is $(60 - z)/2$, where $z$ is the number of trailing zeros. PARENT clears the low bits and sets the new marker bit, which keeps the first $k$ positions. CHILDREN moves the marker two bits down and writes each of the four positions in front of it.

**Containment by ranges.** The leaves of cell $c$ are a block of consecutive positions, so cell $a$ contains cell $b$ if and only if $b$ lies in the range of $a$. Comparing ranges also tells if two cells are disjoint, since two cells either nest or are disjoint.

**Coverings.** A region, such as a disk or a polygon, is approximated by a *covering*, a small set of cells of mixed levels whose union contains the region; S2 finds one with a best-first descent from the faces, under a limit on the number of cells. Each cell is a range of leaf ids, so a query "points in the region" becomes a few range scans of the sorted leaf ids, followed by an exact test.

## Example

Take New York, at latitude $40.7128$ and longitude $-74.0060$. The unit vector is about $(0.209, -0.729, 0.652)$. The largest coordinate in absolute value is $y$, and it is negative, so the face is $1 + 3 = 4$. The projection of face 4 gives $u = z/y \approx -0.895$ and $v = -x/y \approx 0.287$, the quadratic map gives $s \approx 0.0401$ and $t \approx 0.6819$, and so $i = 43\,071\,499$ and $j = 732\,173\,869$.

Face 4 is even, so the orientation starts canonical. The first levels:

| level | bit of $i$ | bit of $j$ | orientation | position | id so far (binary) | token |
|---|---|---|---|---|---|---|
| 0 | | | canonical | | 100 1 | 9 |
| 1 | 0 | 1 | canonical | 1 | 100 01 1 | 8c |
| 2 | 0 | 0 | canonical | 0 | 100 01 00 1 | 89 |
| 3 | 0 | 1 | swap | 3 | 100 01 00 11 1 | 89c |

At level 1, $j \ge 2^{29}$ and $i < 2^{29}$, so the bits are $(0, 1)$, at position 1, which keeps the orientation. At level 2, both bits are 0: position 0, which swaps the orientation. At level 3, the bits $(0, 1)$ with the swap come at position 3, which swaps and inverts. Going on to level 30 gives the leaf id `0x89c25a220cf80969`, whose token starts with `89c25`, the prefix of the S2 cells over Manhattan.

The level 0 cell, face 4, is `0x9000000000000000`; its children, in Hilbert order, have the tokens `84`, `8c`, `94` and `9c`. CONTAINS(`8c`, leaf) holds, since the leaf lies in the range from `0x8800000000000001` to `0x8fffffffffffffff`, and CONTAINS(`84`, leaf) does not. PARENT(leaf, 4) is `0x89d0000000000000`, token `89d`: the level 4 cell sets its marker bit at bit 52, which shows that a token is not always a prefix of the token of a descendant.

## Correctness

The invariant follows from the layout of the id. The positions of the first $k$ levels are the high bits below the face bits, so the leaves below a cell of level $k$ are the ids with the same face and the same first $k$ positions, followed by any $30 - k$ positions and the marker bit 1. These are the odd numbers in a block of length $2^{61 - 2k}$ centered at the id of the cell, which gives CONTAINS. PARENT keeps the first $k$ positions and sets the marker, and CHILDREN writes the four values of position $k + 1$, so both follow the definition. FROM-POINT computes the position at each level from the bits of $i$ and $j$ and the current orientation; since the tables are a bijection from bit pairs to positions for each orientation, and the orientation of a child depends only on its position and the orientation of its parent, the id names the unique cell at each level that contains $(i, j)$. The full proof is in the proofs folder.

## Complexity

The model is the [word RAM](/word-ram/) with 64-bit words.

- **From a point.** The projection costs $O(1)$, and the Hilbert encoding costs $O(L)$, one step per level. The library processes 4 levels per step with a table of 256 entries, which gives $L/4 = 8$ steps.
- **Parent, children, level, containment.** $O(1)$ each, a few bit operations on the id; the level needs a count of trailing zeros, one instruction on most processors.
- **Neighbors.** The cells next to a cell across an edge take $O(L)$, by going to $(i, j)$ coordinates and back, with care at the edge of a face.
- **Space.** One 64-bit word per cell. A covering of a region with at most $c$ cells takes $c$ words, and a query with it takes $c$ range scans.
- **Cell sizes.** There are $6 \cdot 4^k$ cells of level $k$. Their average area is $4\pi r^2 / (6 \cdot 4^k)$: about $85$ million km$^2$ at level 0 and about $0.74$ cm$^2$ at level 30. The quadratic projection keeps the ratio between the largest and smallest cell of a level small, about 2.

| operation | time | case |
|---|---|---|
| point to leaf cell | $O(L)$ | worst |
| parent at level $k$ | $O(1)$ | worst |
| children | $O(1)$ | worst |
| contains | $O(1)$ | worst |
| space per cell | $O(1)$ | total |

## Variants

- **Other projections.** S2 also defines a linear map ($s = (u + 1)/2$) and a tangent map ($s$ from $\tan(\pi u / 4)$), which trade the speed of the projection against how equal the cell areas are.
- **Z-order on the cube.** Using a [Z-order curve](/z-order-curve/) in place of the Hilbert curve gives a simpler code, as in [geohash](/geohash/) on the plane of longitude and latitude, but the curve jumps, so a region needs more ranges.
- **Hexagonal grids.** H3 of Uber divides an icosahedron into hexagons, with the same idea of a hierarchy of cells with 64-bit ids, but the children of a hexagon do not cover it exactly. Such grids are [discrete global grid systems](/discrete-global-grid-system/).
- **HEALPix.** In astronomy, HEALPix divides the sphere into 12 base cells of equal area, each a quadtree, with a nested numbering of the same kind.

## When to use it

Use S2 cells to index points and shapes on the whole Earth, when the data crosses the poles or the date line, where grids on latitude and longitude break, and when the store is a sorted key value store or a B-tree, which can scan id ranges but has no spatial index. Use [geohash](/geohash/) when a short text key on latitude and longitude is enough, and a projected planar index such as an [R-tree](/r-tree/) when the data covers a small area and the shapes are complex.

## Pitfalls

- **Tokens are not prefixes.** The marker bit makes the token of a parent not always a prefix of the token of a child, as in the example. Compare ranges of ids, not strings.
- **Faces have their own axes.** The $(u, v)$ axes of each face and the starting orientations are chosen so that the curve is continuous; copying the formula of face 0 to all faces gives a curve that jumps between faces.
- **Neighbors across faces.** The neighbors of a cell at the edge of a face are on another face, with other axes. Do not compute them by adding 1 to $i$ or $j$.
- **Cell edges are geodesics.** The edges of a cell are arcs of great circles, not lines of constant latitude, so a cell is not a rectangle on a map of latitude and longitude.
- **Precision.** The point to cell map uses floating point; points on the edge of a cell may land on either side. Treat the boundary as belonging to one cell by the rule of the library, not by a second computation.

## Implementations

## History

Hierarchical grids on the sphere were studied in cartography and astronomy before S2, among them the quadrilateralized spherical cube used for sky maps and HEALPix. Eric Veach designed the S2 library at Google, where it was used for geographic data in products such as Google Maps; a Java version was released as open source around 2011, and the C++ library, with the documentation of the cell hierarchy, was published at s2geometry.io in 2017. The 2dsphere index of MongoDB is built on S2, and many other systems use its cell ids as keys.

## References
