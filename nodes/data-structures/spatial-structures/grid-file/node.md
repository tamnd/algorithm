---
tag: 0WX5ZW
kind: data-structure
slug: grid-file
name: Grid file
aliases:
- adaptive grid file
area: data-structures/spatial-structures
level: advanced
summary: Disk-oriented adaptive grid whose directory maps cells to buckets with at most two disk accesses per lookup.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of points, B: the bucket capacity, X: the number of columns, Y: the number of rows, c: the number of directory cells that a query box meets}
  time: {lookup: O(log X + log Y), insert: O(X Y + B), delete: O(n / B + B), range_search: O(c + c B)}
  space: {total: O(X Y + n)}
history:
  year: 1984
  people: [Jürg Nievergelt, Hans Hinterberger, Kenneth C. Sevcik]
  note: Nievergelt, Hinterberger and Sevcik proposed the grid file in ACM Transactions on Database Systems in 1984, as a symmetric multikey file whose exact match queries take two disk accesses.
prereqs: [uniform-grid, external-memory-model]
see_also: [extendible-hashing, kd-b-tree, orthogonal-range-searching, r-tree, linear-hashing, b-tree, bulk-loading, object-partitioning]
sources:
  - paper: doi:10.1145/348.318586
    title: Jürg Nievergelt, Hans Hinterberger and Kenneth C. Sevcik, The grid file, an adaptable, symmetric multikey file structure, ACM Transactions on Database Systems 9(1), 1984
    locator: the whole paper (linear scales, the grid directory, buckets with box-shaped regions, splitting and merging, the two-disk-access principle)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the section on bucket methods with grid directories (the grid file and its relatives)
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998
    locator: the section on point access methods, the part on the grid file and the growth of its directory
---

A grid file stores points of two or more keys on disk. It cuts the plane into a grid by a sorted list of split values on each axis, the *linear scales*, which are small and stay in memory. A *directory*, a two-dimensional array with one entry per grid cell, names the disk bucket of each cell. Several cells may share one bucket, as long as their union is a box. To find a point, a program does a binary search on each scale, reads one directory entry, and reads one bucket: two disk accesses, whatever the data. When a bucket overflows, it is split along a grid line, and when it spans only one cell, a new split value is added to a scale, which adds a whole row or column to the directory. Nievergelt, Hinterberger and Sevcik proposed it in 1984; it is the multidimensional counterpart of [extendible hashing](/extendible-hashing/).

## In plain words

Think of a city map with lines drawn across it, some north to south and some east to west, at places you choose. The lines make a grid of blocks. A small table says, for each block, which drawer holds the addresses in that block. Next to each other, blocks with few addresses can share one drawer.

To find an address, look up its block on the two lists of lines, read the table, and open one drawer. That is always two steps, wherever the address is.

When a drawer gets too full, split it. If it covers several blocks, split along a line that is already there. If not, draw a new line across the whole map.

## The abstract type

The grid file is a [spatial index](/spatial-index/) for points with two or more keys. It supports `insert(p)`, `delete(p)`, exact match `p in G`, and `range_search(lo, hi)`, which reports the points in a box; partial match queries, with some keys free, are range searches with an infinite range on those keys. It is used as a file organization in the [external memory model](/external-memory-model/), with the buckets as disk pages.

## Representation

In two dimensions:

- **Scales.** Two sorted lists $xs$ and $ys$ of split values. A point $(x, y)$ is in column $c = |\{v \in xs : v \le x\}|$ and row $r = |\{v \in ys : v \le y\}|$, so the grid has $X = |xs| + 1$ columns and $Y = |ys| + 1$ rows.
- **Directory.** An $X \times Y$ array $G$, with $G[c][r]$ the bucket of cell $(c, r)$. On disk it is stored in pages, and it is the large part of the structure.
- **Buckets.** Each bucket holds at most $B$ points and has a *region*: the columns $c_0$ to $c_1 - 1$ and the rows $r_0$ to $r_1 - 1$, a box of cells.

**Invariant (G).** (1) The regions of the buckets are boxes of cells that partition the grid, and $G$ names, for each cell, the bucket whose region holds it. (2) Each point is in a bucket whose region holds its cell. (3) Each bucket holds at most $B$ points.

The scales are what make the grid adaptive: the lines are placed where the data is, not at fixed places as in a [uniform grid](/uniform-grid/). Box-shaped regions are needed so that a bucket can be split along a grid line and still leave two boxes, and so that a range query can tell from the region whether a bucket meets the query box.

## Operations

```pseudo id=main
LOOKUP(p)                                  ▷ the bucket of p
L1  c ← the column of p, by binary search on xs
L2  r ← the row of p, by binary search on ys
L3  return G[c][r]

INSERT(p)
L4  b ← LOOKUP(p); if p is in b then return false
L5  add p to b
L6  while b holds more than B points:
L7      if the region of b spans two or more columns or rows then
L8          choose the axis on which it spans more cells, and the grid line in the middle of its span
L9      else add a new split value to the scale of one axis, between the points of b, and copy the column or row of b in G
L10     split b at the chosen line into two buckets; set G for the new one; b ← the half with more points
L11 return true
```

Line L9 is the only step that makes the directory grow. Adding a value $v$ to $xs$ splits one column into two, and the whole directory column is copied, so every bucket whose region crossed that column now spans one column more; only $b$ is split, and the others now share their bucket between two cells. The value is chosen between two distinct coordinates of the points of $b$, so both halves of $b$ get a point, and the loop ends: each pass either shrinks the region of $b$ or splits its points into two nonempty parts.

```pseudo id=delete
DELETE(p)
L12 b ← LOOKUP(p); if p is not in b then return false
L13 remove p from b
L14 if a bucket u next to b has the same rows and adjacent columns, or the same columns and adjacent rows, and the two together hold at most B points, then merge u into b and set G for its cells
    return true

RANGE-SEARCH(lo, hi)
L15 find the columns c(lo_x) to c(hi_x) and the rows c(lo_y) to c(hi_y) by binary search
L16 for each directory cell in that block, read its bucket once
L17     report the points of the bucket that lie in [lo, hi]
```

## Example

Take $B = 2$ and insert seven points.

| insert | what happens | xs | ys | buckets, as (columns, rows): points |
|---|---|---|---|---|
| (10,10), (60,20) | one bucket, one cell | | | $[0,1) \times [0,1)$: (10,10), (60,20) |
| (30,70) | overflow in one cell; $xs$ has no more lines than $ys$, so split on $x$ at the median 30 of the distinct $x$ values 10, 30, 60 | 30 | | col 0: (10,10); col 1: (30,70), (60,20) |
| (80,80) | the bucket of column 1 overflows; now split on $y$ at 70; the directory gets a second row, and the bucket of column 0 spans both rows | 30 | 70 | col 0, rows 0 to 1: (10,10); (1,0): (60,20); (1,1): (30,70), (80,80) |
| (40,40) | goes to cell (1, 0), which has room | 30 | 70 | (1,0): (40,40), (60,20) |
| (70,60) | cell (1, 0) overflows; split on $x$ at 60; the column is copied, so the bucket of (30,70) and (80,80) now spans columns 1 to 2 | 30, 60 | 70 | (1,0): (40,40); (2,0): (60,20), (70,60); cols 1 to 2, row 1: (30,70), (80,80) |
| (20,30) | goes to column 0, which has room | 30, 60 | 70 | col 0, rows 0 to 1: (10,10), (20,30) |

The final directory has $3 \times 2 = 6$ cells and 4 buckets. Columns hold $x < 30$, $30 \le x < 60$ and $x \ge 60$; rows hold $y < 70$ and $y \ge 70$.

- **Lookup** $(90, 90)$: column 2, row 1, the bucket of (30,70) and (80,80), which is also the bucket of $(40, 75)$.
- **Range** $[25, 65] \times [25, 65]$: columns 0 to 2 and row 0, so 3 cells and 3 buckets; the only point in the box is (40,40).
- **Delete** (80,80): its bucket keeps (30,70) and has no neighbor with the same rows or columns, so nothing merges. **Delete** (70,60): the bucket of cell (2, 0) keeps (60,20), and its neighbor (1, 0) has the same row and holds one point, so they merge into one bucket for columns 1 to 2 of row 0. The scales stay as they are.

## Correctness

INSERT puts $p$ in the bucket of its cell, so part 2 holds. A split at a grid line cuts a box of cells into two boxes and sends each point to the half that holds its cell; adding a split value copies a column or row of the directory, so each region grows by that column or row and stays a box. So part 1 holds after each pass, and the loop ends with every bucket within capacity. DELETE merges only two buckets whose union is a box. LOOKUP returns the right bucket by part 1, and RANGE-SEARCH reads every bucket whose region meets the box. The full proof is in the proofs folder.

## Complexity

In the external memory model, the scales are in memory and each directory page and bucket is one disk access.

- **Lookup.** Two binary searches in memory, one directory access and one bucket access: the *two-disk-access principle* of the grid file, which holds for any data.
- **Insert.** Usually one bucket write, or two buckets and a few directory entries for a split along an existing line. A new split value copies a whole row or column of the directory, $O(X)$ or $O(Y)$ entries, and in the worst case the directory must be rewritten, $O(XY)$.
- **Directory size.** This is the weak point. Each split value cuts across the whole grid, so the directory has $XY$ cells, which can be far more than the number of buckets. For $n$ points on the diagonal, $(i, i)$, with $B = 1$, the code here makes 64 buckets and 32 and 31 split values for $n = 64$, a directory of $33 \times 32 = 1056$ cells: quadratic in $n$. For points spread evenly, it grows faster than linearly but much more slowly; in one run of the code with 4000 random points and $B = 4$, there were 1566 buckets and 5625 cells.
- **Bucket fill.** Splits make buckets about half full, and in the random run above the buckets were about 64% full.
- **Range search.** It reads the $c$ directory cells in the box and each bucket once. Since a bucket's region is a box of cells, the buckets read are exactly those whose regions meet the block of cells.

| operation | time | case |
|---|---|---|
| lookup | $O(\log X + \log Y)$ in memory, 2 disk accesses | worst |
| insert | $O(XY + B)$ | worst, when the directory grows |
| delete | $O(n/B + B)$ | worst, with a scan for a neighbor |
| range_search | $O(c + cB)$ | worst |
| space | $O(XY + n)$ | total |

## Variants

- **Merging policies.** Nievergelt and others proposed the *buddy* system, which merges a bucket only with the one it was split from, and the *neighbor* system used here, which merges with any adjacent bucket whose union is a box. Removing a split value that no bucket boundary uses shrinks the directory.
- **Two-level directory.** Hinrichs and others kept a small root directory on top of a paged directory, to control the size of the directory on skewed data.
- **Split policies.** Splitting the axes in turn, or the axis of the largest spread, or by the expected queries, changes the shape of the grid.
- **Higher dimensions.** The same structure in $d$ dimensions has $d$ scales and a $d$-dimensional directory, which can grow as fast as $n^d$ on bad data.
- **Hierarchical alternatives.** The [k-d-B tree](/kd-b-tree/) and later the BANG file and the hB-tree replaced the flat directory with a tree, which grows linearly with the number of buckets.
- **Extended objects.** Rectangles can be stored as points in four dimensions, by their corners or their centers and extents, as with other point structures.

## When to use it

Use a grid file for points with a few keys on disk, when exact match queries must be fast for any data and the keys are not strongly correlated, and when the range and partial match queries are about all keys alike, which is the *symmetric* use the authors aimed at. For correlated or clustered data, such as points along a road or a diagonal, the directory grows too much: use a [k-d-B tree](/kd-b-tree/), an [R-tree](/r-tree/) or a B-tree on a space-filling curve key. Use a [B-tree](/b-tree/) on one key if almost all queries use the same key.

## Pitfalls

- **Correlated keys.** Keys that move together, such as the price and the cost of an item, put the points on a line, and the directory then grows quadratically, as in the diagonal example.
- **Duplicate coordinates.** If more than $B$ points share both coordinates, no split can separate them. Store the points as a set, or let such buckets overflow into a chain.
- **Regions that are not boxes.** A merge must keep each region a box; merging two buckets whose union is an L shape breaks range queries and later splits.
- **Splitting at an existing line that separates nothing.** A split along an existing line can put all points on one side. The loop must go on with the full half, as line L10 does, and not assume that one split is enough.

## Implementations

## History

Nievergelt, Hinterberger and Sevcik published the grid file in 1984, at about the time of extendible hashing, which uses a similar directory for one key. Hinrichs studied its implementation in the mid 1980s, and others analyzed the growth of its directory, which led to the hierarchical structures that followed, such as the BANG file of Freeston. The survey of Gaede and Günther of 1998 places it among the point access methods.

## References
