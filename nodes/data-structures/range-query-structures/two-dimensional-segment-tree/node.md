---
tag: QYYQT1
kind: data-structure
slug: two-dimensional-segment-tree
name: Two-dimensional segment tree
aliases:
- Segment Tree 2D
- 2D segment tree
area: data-structures/range-query-structures
level: advanced
summary: A segment tree of segment trees that answers and updates rectangle queries over a matrix in logarithmic squared time.
implements: [range-query-structure]
prereqs: [segment-tree, two-dimensional-range-sum-query, monoid]
see_also: [two-dimensional-fenwick-tree, range-tree, quadtree, kd-tree, merge-sort-tree, dynamic-segment-tree, coordinate-compression, orthogonal-range-counting]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Generalization to higher dimensions, subsections Simple 2D Segment Tree and Compression of 2D Segment Tree
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 5 (Orthogonal Range Searching), Section 5.3 (Range Trees), the two-level structure with an associated structure at each node
  - paper: "Jon L. Bentley, Solutions to Klee's rectangle problems, unpublished manuscript, Department of Computer Science, Carnegie-Mellon University, 1977"
    locator: the segment tree over the elementary intervals
---

A two-dimensional segment tree stores an $n \times m$ matrix $M$ and answers the aggregate of any axis-aligned rectangle under a commutative [monoid](/monoid/), such as the sum, the minimum or the gcd, with point updates. It is a [segment tree](/segment-tree/) over the rows in which each node holds a second segment tree over the columns, for the rows of that node. A query splits its rows into $O(\log n)$ nodes of the outer tree and asks each of their inner trees for its columns, so it costs $O(\log n \log m)$, and an update rebuilds one root-to-leaf path of inner nodes in each of the $O(\log n)$ outer nodes on one path. Unlike the [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/), it needs no inverse, so it answers rectangle minimums and maximums.

## In plain words

Think of a table of numbers, for example the height of the ground at each point of a map, and requests such as "what is the lowest point inside this rectangle?". Some points of the map also change now and then.

A normal segment tree splits a list in halves, then in quarters, and stores an answer for each piece. Here we do this twice. First, split the rows of the table into halves, quarters and so on. Then, for each such band of rows, build a normal segment tree over the columns of that band. A rectangle is a few bands of rows, and inside each band it is a few pieces of columns, so its answer combines a few stored values. A change of one point touches a few bands, and a few pieces in each of them.

## The abstract type

The tree implements the [range query structure](/range-query-structure/) on a grid: `build(M)`, `query(r1, c1, r2, c2)` for the product of the rectangle, and `set(r, c, x)` for $M[r][c] \leftarrow x$. The operation $\oplus$ must be associative and commutative, with an identity $e$. Commutativity is needed because a rectangle has no single order of its cells: the tree combines the cells row band by row band, and the build combines them in other groupings.

## Representation

Both trees use the node numbering of a [binary heap](/binary-heap/), as in the [segment tree](/segment-tree/). The outer node $v_x$ covers a range of rows $[l_x, r_x]$, with the root $1$ for $[0, n - 1]$ and the children $2 v_x$ and $2 v_x + 1$ for the two halves. The inner node $v_y$ covers a range of columns $[l_y, r_y]$ in the same way. The values sit in one table $t[v_x][v_y]$ of $4n \times 4m$ cells.

**Invariant (T).** For each outer node $v_x$ with rows $[l_x, r_x]$ and each inner node $v_y$ with columns $[l_y, r_y]$,

$$t[v_x][v_y] = \bigoplus_{l_x \le i \le r_x} \ \bigoplus_{l_y \le j \le r_y} M[i][j].$$

The outer tree has $2n - 1$ nodes and each inner tree has $2m - 1$ nodes, so $(2n - 1)(2m - 1)$ cells are used. There are two ways to compute a cell from other cells: from the two inner children, $t[v_x][2v_y] \oplus t[v_x][2v_y + 1]$, or, when $v_x$ is not a leaf, from the two outer children, $t[2v_x][v_y] \oplus t[2v_x + 1][v_y]$. Both give the same value by (T) and commutativity.

## Operations

```pseudo id=main
BUILD-Y(vx, lx, rx, vy, ly, ry)               ▷ the inner tree of vx; call with vy = 1, [0, m − 1]
L1  if ly = ry then
L2    if lx = rx then t[vx][vy] ← M[lx][ly] else t[vx][vy] ← t[2vx][vy] ⊕ t[2vx + 1][vy]
L3    return
L4  my ← ⌊(ly + ry)/2⌋; BUILD-Y(vx, lx, rx, 2vy, ly, my); BUILD-Y(vx, lx, rx, 2vy + 1, my + 1, ry)
L5  t[vx][vy] ← t[vx][2vy] ⊕ t[vx][2vy + 1]

BUILD-X(vx, lx, rx)                           ▷ call BUILD-X(1, 0, n − 1)
L6  if lx ≠ rx then mx ← ⌊(lx + rx)/2⌋; BUILD-X(2vx, lx, mx); BUILD-X(2vx + 1, mx + 1, rx)
L7  BUILD-Y(vx, lx, rx, 1, 0, m − 1)

QUERY-Y(vx, vy, ly, ry, c1, c2)
L8  if c2 < ly or ry < c1 then return e
L9  if c1 ≤ ly and ry ≤ c2 then return t[vx][vy]
L10 my ← ⌊(ly + ry)/2⌋; return QUERY-Y(vx, 2vy, ly, my, c1, c2) ⊕ QUERY-Y(vx, 2vy + 1, my + 1, ry, c1, c2)

QUERY-X(vx, lx, rx, r1, r2, c1, c2)           ▷ call QUERY-X(1, 0, n − 1, r1, r2, c1, c2)
L11 if r2 < lx or rx < r1 then return e
L12 if r1 ≤ lx and rx ≤ r2 then return QUERY-Y(vx, 1, 0, m − 1, c1, c2)
L13 mx ← ⌊(lx + rx)/2⌋; return QUERY-X(2vx, lx, mx, r1, r2, c1, c2) ⊕ QUERY-X(2vx + 1, mx + 1, rx, r1, r2, c1, c2)

UPDATE-Y(vx, lx, rx, vy, ly, ry, c)           ▷ M[r][c] is already set
L14 if ly = ry then
L15   if lx = rx then t[vx][vy] ← M[lx][ly] else t[vx][vy] ← t[2vx][vy] ⊕ t[2vx + 1][vy]
L16   return
L17 my ← ⌊(ly + ry)/2⌋; if c ≤ my then UPDATE-Y(vx, lx, rx, 2vy, ly, my, c) else UPDATE-Y(vx, lx, rx, 2vy + 1, my + 1, ry, c)
L18 t[vx][vy] ← t[vx][2vy] ⊕ t[vx][2vy + 1]

UPDATE-X(vx, lx, rx, r, c)                    ▷ set M[r][c] ← x, then call UPDATE-X(1, 0, n − 1, r, c)
L19 if lx ≠ rx then mx ← ⌊(lx + rx)/2⌋; if r ≤ mx then UPDATE-X(2vx, lx, mx, r, c) else UPDATE-X(2vx + 1, mx + 1, rx, r, c)
L20 UPDATE-Y(vx, lx, rx, 1, 0, m − 1, c)
```

**Build** (lines L1 to L7) builds the outer children first, in post order, so that line L2 can take the leaves of an inner tree from the two outer children. Inside one inner tree, line L5 combines inner children as in a normal segment tree. Each cell is computed once with at most one $\oplus$.

**Query** (lines L8 to L13) is a segment tree query over the rows whose "stored value" at a fully covered outer node is an inner query over the columns (line L12).

**Update** (lines L14 to L20) first updates the outer child that holds row $r$, then walks the inner tree of $v_x$ from the root to the column $c$. The inner leaf is recomputed from the matrix (an outer leaf) or from the two outer children (an inner node of the outer tree), and the inner nodes on the way back up from their inner children. So the cells of $v_x$ on the column path are correct as soon as the cells of the outer child are.

## Example

Let $\oplus = \min$ and $e = +\infty$, on

$$M = \begin{pmatrix} 2 & 1 & 4 & 3 \\ 0 & 5 & 2 & 1 \\ 3 & 1 & 6 & 2 \\ 1 & 4 & 0 & 5 \end{pmatrix}.$$

For $n = m = 4$, the outer node 5 is the row 1 alone and node 6 the row 2 alone; the inner node 5 is the column 1 alone and node 3 the columns 2 and 3. The cell $t[1][1]$ is the minimum of the whole matrix, 0.

| step | operation | cells used | result |
|---|---|---|---|
| 1 | QUERY$(1, 1, 2, 3)$ | the rows split into the outer nodes 5 and 6, the columns into the inner nodes 5 and 3: $t[5][5] = 5$, $t[5][3] = \min(2, 1) = 1$, $t[6][5] = 1$, $t[6][3] = \min(6, 2) = 2$ | 1 |
| 2 | set $M[2][1] \leftarrow 7$ | the outer path 1, 3, 6 and in each the inner path 1, 2, 5: 9 cells, with $t[6][5] = 7$ and $t[3][5] = \min(7, 4) = 4$ | |
| 3 | QUERY$(1, 1, 2, 3)$ | the same four cells: $5, 1, 7, 2$ | 1 |
| 4 | set $M[1][3] \leftarrow 9$ | the outer path 1, 2, 5 and in each the inner path 1, 3, 7: now $t[5][3] = \min(2, 9) = 2$ | |
| 5 | QUERY$(1, 1, 2, 3)$ | the same four cells: $5, 2, 7, 2$ | 2 |

The rectangle of the query is $5, 2, 1$ in row 1 and $1, 6, 2$ in row 2 at the start, so 1 is right. After both updates it is $5, 2, 9$ and $7, 6, 2$, with the minimum 2.

## Correctness

BUILD establishes (T) cell by cell: an inner leaf of an outer leaf is a matrix entry; an inner leaf of an inner outer node is the product of the same column over the two halves of its rows; and an inner node is the product of its two inner children. By commutativity and associativity each of these equals the product over its rectangle. UPDATE keeps (T), because the cells whose rectangle holds $(r, c)$ are exactly the pairs of an outer node on the path to row $r$ and an inner node on the path to column $c$, and it recomputes them from the bottom up in both trees. QUERY-Y returns the product over the columns $[l_y, r_y] \cap [c_1, c_2]$ of the rows of $v_x$, by the argument of the one-dimensional segment tree, and QUERY-X then returns the product over the rows $[l_x, r_x] \cap [r_1, r_2]$ by the same argument with QUERY-Y as the stored value. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The outer query visits at most 4 nodes on each level of the outer tree, and at most 2 of them per level are fully covered, so it calls QUERY-Y at most $2 \lceil \lg n \rceil$ times, or once when the rectangle has all the rows. Each inner query visits at most $4 \lceil \lg m \rceil + 1$ nodes. An update recomputes $\lceil \lg n \rceil + 1$ outer nodes times $\lceil \lg m \rceil + 1$ inner nodes, at most, each with one $\oplus$.

| operation | time | applications of $\oplus$ |
|---|---|---|
| build | $\Theta(nm)$ | fewer than $4nm$ |
| query | $O(\log n \log m)$ worst case | $O(\log n \log m)$ |
| set one cell | $\Theta(\log n \log m)$ worst case | at most $(\lceil \lg n \rceil + 1)(\lceil \lg m \rceil + 1)$ |
| space | $(2n - 1)(2m - 1)$ cells used in a table of $16nm$ | |

The times count one $\oplus$ as $O(1)$. For $n = m = 1024$, an update recomputes at most $11 \cdot 11 = 121$ cells, as in the Fenwick tree, but the table has $16 \cdot 2^{20}$ cells against $2^{20}$ for the Fenwick tree.

## Variants

- **Compressed tree for points.** For $N$ points with large coordinates and queries known in advance, keep in each outer node only the columns of the points of its rows, in a sorted list with its own segment tree or Fenwick tree. The space becomes $O(N \log N)$ and each operation costs $O(\log^2 N)$; this is the [range tree](/range-tree/) with a dynamic associated structure.
- **Dynamic inner trees.** Create the nodes of the inner trees only when an update reaches them, as in a [dynamic segment tree](/dynamic-segment-tree/). After $q$ updates on an empty grid the tree has $O(q \log n \log m)$ nodes.
- **Sorted lists in the nodes.** An outer tree whose nodes hold sorted lists of the column values, the [merge sort tree](/merge-sort-tree/), counts points in rectangles of a static set in $O(\log^2 N)$.
- **Rectangle updates.** Lazy propagation does not move tags between outer nodes in general. For range add with sums, and for "raise each cell of the rectangle to at least $x$" with maximum queries, each outer node can keep a second inner tree of permanent tags that are never pushed down, and a query reads the tags of the outer nodes it passes.
- **Higher dimensions.** Nesting $d$ trees gives $O(\log^d n)$ per operation and $O(4^d n^d)$ space for a full grid.
- **Quadtree.** A [quadtree](/quadtree/) splits both axes at once; it uses less space for sparse data, but a rectangle query can take $\Theta(n)$ time on an $n \times n$ grid.

## When to use it

Use it for rectangle queries with an operation that has no inverse, such as $\min$, $\max$ or $\gcd$, on a grid with point updates. For sums, prefer the [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/), which is shorter and uses $16$ times less memory. For a static grid and an idempotent operation, a two-dimensional sparse table answers in $O(1)$ with $O(nm \log n \log m)$ space. For sparse points in a large plane, use the compressed variant, a [range tree](/range-tree/) or a [k-d tree](/kd-tree/).

## Pitfalls

- **Memory.** The table has $16nm$ cells. For $n = m = 2000$ this is $6.4 \cdot 10^7$ cells, which is too much for many judges in some languages. Use the bottom-up layout with $2n \times 2m$ cells, or a Fenwick tree for sums.
- **Leaves of inner trees in outer nodes that are not leaves.** Line L2 and line L15 must combine the two outer children. Taking a matrix entry there, or skipping the case, leaves wrong values in all non-leaf outer nodes.
- **Updating only the leaf row.** UPDATE-X must call UPDATE-Y for every outer node on the path, not only for the outer leaf. Line L20 runs after the recursive call for this reason.
- **The order of the recursion.** In BUILD-X and UPDATE-X, the outer children must be done before the inner tree of $v_x$, because line L2 and line L15 read them.
- **An operation that is not commutative.** The tree combines cells in different orders in different places, so the product of matrices, for example, gives wrong answers.

## Implementations

The Python class `SegmentTree2D` follows the main block, with the operation and its identity as arguments, so the same class gives sums, minimums, maximums and gcds. It keeps a copy of the matrix for the leaves of line L15, and its `check_invariant` method compares each used cell with a direct fold of its rectangle.

## History

The segment tree goes back to Bentley's 1977 manuscript on Klee's rectangle problems. Trees whose nodes hold a second structure for the next coordinate are the multi-level structures of computational geometry, such as the range trees of Chapter 5 of de Berg and coauthors. The form over a dense matrix with a monoid in each cell, as on this page, is the usual one in programming texts such as cp-algorithms.

## References
