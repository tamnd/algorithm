---
tag: 452WNT
kind: data-structure
slug: corner-stitching
name: Corner stitching
aliases:
- Ousterhout corner stitching
- corner-stitched plane
area: eda/timing-and-verification
level: core
summary: Ousterhout's layout structure that tiles the plane with solid and space rectangles, each with four pointers at two corners, for point finding and area search.
model: real-ram
complexity:
  vars: {n: the number of solid tiles, N: "the number of tiles, at most 4n + 1", k: the number of tiles that an area query reports, e: the right neighbours of the reported tiles that the enumeration examines, d: the number of neighbours of the tiles that an update splits or merges, F: the cost of one point find}
  time: {point_find_worst: O(N), area_enumeration: O(F + k + e), insert_or_delete: O(F + k + d)}
  space: {total: Θ(n)}
history:
  year: 1984
  people: [John K. Ousterhout]
  note: Ousterhout described corner stitching in IEEE TCAD in 1984 as the database of the Magic layout editor, which he and his students built at Berkeley.
prereqs: [planar-subdivision, planar-point-location]
see_also: [trapezoidal-map, doubly-connected-edge-list, triangle-walk-point-location, r-tree, quadtree, rectangle-intersection-reporting, design-rule-checking, circuit-extraction]
sources:
  - paper: doi:10.1109/TCAD.1984.1270061
    title: John K. Ousterhout, Corner stitching, a data-structuring technique for VLSI layout tools, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 3(1), 87 to 100, 1984
    locator: the tiles and the four stitches, the maximal horizontal strips, the algorithms for neighbour finding, point finding, area search, area enumeration, tile creation and tile deletion, and the measurements of memory and of point finding time
  - paper: "John K. Ousterhout, Gordon T. Hamachi, Robert N. Mayo, Walter S. Scott and George S. Taylor, Magic, a VLSI layout system, Proceedings of the 21st Design Automation Conference, 1984"
    locator: the use of corner stitched planes, one for each group of mask layers, as the database of the Magic editor (check the page range)
  - book: isbn:9781584884354
    title: Dinesh P. Mehta and Sartaj Sahni (editors), Handbook of Data Structures and Applications, Chapman and Hall/CRC, 2005
    locator: Chapter 52, Layout Data Structures, by Dinesh P. Mehta, Section 52.4 (corner stitching, point finding, tile insertion and the storage bound of 3N + 1 minus the number of violations for the space tiles) and Section 52.5 (extensions)
---

Corner stitching is a data structure for a set of disjoint rectangles in the plane that also stores the empty space between them as rectangles. The plane is cut into *tiles*: every point lies in exactly one tile, which is *solid* (part of the layout) or *space*, and space is cut into maximal horizontal strips. Each tile keeps four pointers, the *stitches*, to neighbours at its lower left and upper right corners, and the queries walk from tile to tile along them. John Ousterhout introduced it in 1984 for the Magic layout editor, where each group of mask layers is one corner stitched plane.

## In plain words

Think of a quilt. The chip area is covered with rectangular patches, some filled with material and some empty, with no gap and no overlap. Each empty patch is as wide as it can be, and is cut only where a filled patch starts or ends above or below it.

Each patch knows four neighbours: the one below it at its left end, the one to its left at its bottom end, the one above it at its right end, and the one to its right at its top end. With these four links you can walk to any patch. To find what lies under the cursor, start anywhere and walk up or down, then left or right, until you stand on the point. Empty space is stored, so the question "is this area empty?" costs a short walk along its left side, not a search.

## The abstract type

The structure stores a set $S$ of $n$ disjoint closed-open rectangles $[x_0, x_1) \times [y_0, y_1)$ with corners in a world rectangle $W$. It supports these operations.

- POINT-FIND$(p)$: the tile that contains the point $p$.
- NEIGHBOURS$(t)$: the tiles that touch one side of the tile $t$, in order along that side.
- AREA-SEARCH$(A)$: some rectangle of $S$ that meets the rectangle $A$, or nil if $A$ is empty.
- ENUMERATE$(A)$: every tile that meets $A$, solid and space, each once.
- INSERT$(R)$: add a rectangle $R$ that meets no rectangle of $S$.
- DELETE$(t)$: remove the rectangle of the solid tile $t$.

Layouts with polygons that are not rectangles are cut into rectangles first, as for any [rectilinear polygon](/rectilinear-polygon/). Magic keeps the material type in each tile and lets two solid tiles of different types touch. This page treats one type, so solid tiles can also be merged by the user, but the structure never merges them by itself.

## Representation

A tile is $t = [x_0, x_1) \times [y_0, y_1)$ with a flag solid or space. The tiles form a [planar subdivision](/planar-subdivision/) of $W$ into axis-parallel rectangles. The four stitches are defined by the point that the target tile contains, for a small $\varepsilon > 0$:

| stitch | target tile contains | meaning |
| --- | --- | --- |
| $bl(t)$ | $(x_0, y_0 - \varepsilon)$ | bottom neighbour at the left end |
| $lb(t)$ | $(x_0 - \varepsilon, y_0)$ | left neighbour at the bottom end |
| $tr(t)$ | $(x_1 - \varepsilon, y_1)$ | top neighbour at the right end |
| $rt(t)$ | $(x_1, y_1 - \varepsilon)$ | right neighbour at the top end |

A stitch that would leave $W$ is nil. Ousterhout stores only the lower left corner $(x_0, y_0)$ of a tile and reads $x_1$ from $rt(t)$ and $y_1$ from $tr(t)$, so a tile costs one flag, two coordinates and four pointers.

The space tiles are kept in a canonical form. (H) No two space tiles share a piece of a vertical edge. (V) No two space tiles with the same $x$-span share a piece of a horizontal edge. Under (H) and (V) the space tiles are the maximal horizontal strips of the free area, and they are a function of the solid tiles only. There are at most $3n + 1$ of them, so $N \le 4n + 1$ tiles in all. Both facts are proved in [proofs/correctness.md](proofs/correctness.md).

## Operations

```pseudo id=main
POINT-FIND(p = (px, py), t)            ▷ t: any start tile, for example the last tile found
L1  repeat
L2      while py < y0(t) do t ← bl(t)
L3      while py ≥ y1(t) do t ← tr(t)
L4      if px < x0(t) then t ← lb(t)
L5      else if px ≥ x1(t) then t ← rt(t)
L6      else return t

TOP-NEIGHBOURS(t)                       ▷ the other three sides are symmetric
N1  u ← tr(t)
N2  while u ≠ nil and x1(u) > x0(t) do output u;  u ← lb(u)

AREA-SEARCH(A = [ax0, ax1) × [ay0, ay1))
A1  t ← POINT-FIND((ax0, ay1 − ε))      ▷ the top tile on the left edge of A
A2  repeat  if t is solid then return t
A3      if x1(t) < ax1 then return POINT-FIND((x1(t), min(y1(t), ay1) − ε), t)    ▷ solid by (H)
A4      if y0(t) ≤ ay0 then return nil
A5      t ← POINT-FIND((ax0, y0(t) − ε), t)

ENUMERATE(A)
E1  t ← POINT-FIND((ax0, ay1 − ε))
E2  repeat  REPORT(t)
E3      if y0(t) ≤ ay0 then return
E4      t ← POINT-FIND((ax0, y0(t) − ε), t)
REPORT(u)
E5  stack ← [u];  while stack is not empty do u ← pop(stack)
E6      output u
E7      if x1(u) ≥ ax1 then continue
E8      for each right neighbour w of u, from rt(u) down, with y1(w) > max(y0(u), ay0) do
E9          if y0(w) < ay1 and max(y0(w), ay0) ≥ y0(u) then push w   ▷ u owns w

INSERT(R = [a, b) × [c, d))
I1  if AREA-SEARCH(R) ≠ nil then fail
I2  split the tile at (a, d − ε) horizontally at d
I3  split the tile at (a, c) horizontally at c
I4  C ← the space tiles on the line x = a between c and d, from the top down
I5  split each tile of C vertically at a and at b;  mark each middle part solid
I6  merge the middle parts into one solid tile R
I7  for each left and right part s do SETTLE(s)       ▷ merge s with space tiles of the same x-span above and below

DELETE(D = [a, b) × [c, d))
D1  mark D as space
D2  split each space left or right neighbour of D at c and at d
D3  H ← the top and bottom edges of these neighbours that lie strictly between c and d
D4  split D horizontally at every height of H into pieces
D5  split each space left or right neighbour of a piece at every height of H
D6  for each piece p do merge p with lb(p) and with rt(p) when they are space with the y-span of p
D7  for each row tile r made in D6 do SETTLE(r)
```

Split and merge are local. To split $t$ at a height $y$, make the upper part $u$, find $lb(u)$ by walking up the left neighbours of $t$ and the new $rt(t)$ by walking down its right neighbours, and redirect the stitches of the neighbours whose defining point now lies in $u$. A merge redirects the stitches that pointed to the tile that disappears. Each costs time linear in the number of neighbours of the two tiles.

## Example

The world is $[0, 10) \times [0, 8)$ with two solid tiles $A = [2, 5) \times [2, 5)$ and $B = [6, 9) \times [4, 7)$. The canonical space tiles are the seven maximal strips below, which reach the bound $3n + 1 = 7$.

| tile | kind | $bl$ | $lb$ | $tr$ | $rt$ |
| --- | --- | --- | --- | --- | --- |
| $s_1 = [0,10) \times [0,2)$ | space | nil | nil | $s_3$ | nil |
| $s_2 = [0,2) \times [2,5)$ | space | $s_1$ | nil | $s_5$ | $A$ |
| $A = [2,5) \times [2,5)$ | solid | $s_1$ | $s_2$ | $s_5$ | $s_4$ |
| $s_3 = [5,10) \times [2,4)$ | space | $s_1$ | $A$ | $s_6$ | nil |
| $s_4 = [5,6) \times [4,5)$ | space | $s_3$ | $A$ | $s_5$ | $B$ |
| $B = [6,9) \times [4,7)$ | solid | $s_3$ | $s_4$ | $s_7$ | $s_6$ |
| $s_6 = [9,10) \times [4,7)$ | space | $s_3$ | $B$ | $s_7$ | nil |
| $s_5 = [0,6) \times [5,7)$ | space | $s_2$ | nil | $s_7$ | $B$ |
| $s_7 = [0,10) \times [7,8)$ | space | $s_5$ | nil | nil | nil |

POINT-FIND$((1, 6))$ from $s_1$: the height 6 is not below $s_1$, so L2 does nothing, and $6 \ge 2$ sends L3 to $tr(s_1) = s_3$ and then to $tr(s_3) = s_6$, where $4 \le 6 < 7$. Now $1 < 9$, so L4 moves to $lb(s_6) = B$, then to $lb(B) = s_4$. In $s_4$ the height $6 \ge 5$, so L3 moves to $tr(s_4) = s_5$, which contains $(1, 6)$. The walk visits $s_1, s_3, s_6, B, s_4, s_5$.

AREA-SEARCH$([5, 6) \times [0, 8))$, the column between $A$ and $B$: the left edge $x = 5$ crosses $s_7$, $s_5$, $s_4$, $s_3$ and $s_1$ from the top down. Each is space and reaches $x = 6$ or more, so line A3 never fires, and the answer is nil: a wire of width 1 fits there. ENUMERATE$([1, 8) \times [1, 6))$ walks down the left edge through $s_5$, $s_2$ and $s_1$, and reports $s_5$, $s_2$, $A$, $s_3$, $s_4$, $B$, $s_1$. $B$ has two left neighbours, $s_4$ and $s_5$. It is reported from $s_4$, its owner, and not again from $s_5$, because the point just left of its lower left corner $(6, 4)$ lies in $s_4$.

DELETE$(A)$ splits $s_2$ and $s_4$ so that they lie inside the heights of $A$, cuts $A$ at height 4, joins the rows, and settles them. The result has the four space tiles $[0,10) \times [0,4)$, $[0,6) \times [4,7)$, $[9,10) \times [4,7)$ and $[0,10) \times [7,8)$, which is the canonical form for $B$ alone.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Under (H) and (V) the space tile that contains a free point is fixed by the solid tiles, and there are at most $3n + 1$ space tiles: each new free strip met by an upward sweep is charged to the top-left corner, the bottom right end or the bottom left end of one solid tile. Point find is correct because the vertical phase stops in the row of the target, and each horizontal step moves to the next tile of that row, so the walk never comes back. Area search is correct because of (H): a space tile on the left edge of the area that ends before the right edge has a solid tile as its right neighbour. Enumeration reports each tile once because every tile right of the left edge has exactly one *owner*, the left neighbour that contains the point just left of its lower left corner inside the area, and only the owner pushes it. Insertion and deletion keep (H) and (V) because they rebuild the strips only where the solid set changed and then merge every changed strip with equal strips above and below.

## Complexity

| operation | worst case |
| --- | --- |
| NEIGHBOURS$(t)$ | $O(1 + \text{number of neighbours on that side})$ |
| POINT-FIND | $O(N)$ |
| AREA-SEARCH | $O(N)$ |
| ENUMERATE | $O(F + k + e)$, where $F$ is the cost of one point find and $e$ counts the right neighbours of the reported tiles that line E8 examines |
| INSERT, DELETE | $O(F + k + d)$ |
| space | $\Theta(n)$, at most $4n + 1$ tiles |

All bounds are in the real RAM with exact comparisons of coordinates, and no arithmetic is needed. The $O(N)$ bound of point find is tight: with $n$ solid unit squares in one row and gaps of width 1, a walk from the left end to the right end of the row crosses all $2n + 1$ tiles of the row. The fast case is a measured fact, not a theorem. Ousterhout measured that on real layouts a walk from the previous tile is short and grows about as the square root of the number of tiles, and on a $k \times k$ grid of unit squares with gaps of 1 the mean walk between random points visits about $k$ tiles (36.7 tiles on average for $k = 32$, with 2080 tiles). No bound for a class of inputs is proved in the paper. Ousterhout also measured that the structure needs about three times the memory of a plain list of rectangles.

## Variants

- **Several planes.** Magic keeps one plane for each group of layers that interact, so a design rule between two layers is checked on one plane.
- **Material types.** The solid flag becomes a type field. Two solid tiles of different types may touch, and the canonical form is kept for each type with the same rules.
- **Other tile shapes.** Mehta and others describe trapezoidal, L-shaped and rectilinear tiles, which cut down the number of tiles for diagonal or L-shaped layouts.
- **Strips in the other direction.** Maximal vertical strips are the mirror image and give the same bounds.

## When to use it

Use it in an interactive layout editor, for [design rule checking](/design-rule-checking/) near a change, for [circuit extraction](/circuit-extraction/) by walking from tile to tile, and for compaction and maze routing in the free space, where the explicit empty tiles are the graph to search. A [trapezoidal map](/trapezoidal-map/) also cuts the free space into simple cells, but it handles segments in any direction and gives expected $O(\log n)$ point location with a search structure, while corner stitching handles only axis-parallel rectangles and relies on the locality of the previous query. Mechanical CAD stores parts in an [R-tree](/r-tree/) or a [quadtree](/quadtree/) of bounding boxes: those allow overlapping boxes and do not store empty space, so they answer box queries well but cannot answer "what is the nearest material to the right" with one stitch.

## Pitfalls

- The structure needs disjoint solid tiles. Overlapping rectangles from a layout file must be merged first, for example with a [polygon union](/polygon-union/).
- The canonical form must be restored after every update. A missed merge does not break point find, but it breaks area search, which uses (H), and the space bound.
- A point on an edge belongs to the tile on its right or above it, because tiles are half-open. Mixing closed and half-open tiles gives walks that never stop.
- Point find from a far start is slow. Keep the last tile found as a hint, which is what makes the measured times short.
- An area search must start on the left edge of the area and use (H). Testing only the tiles that contain the corners misses a solid tile inside the area.

## Implementations

## History

Ousterhout published corner stitching in IEEE TCAD in January 1984, and the Magic editor that used it was presented at the Design Automation Conference of the same year. The extractor, the design rule checker, the router and the compactor (plowing) of Magic all work on corner stitched planes. Mehta later gave the exact count $3n + 1 - k$ of space tiles, where $k$ counts a kind of corner alignment, and studied the L-shaped variant.

## References
