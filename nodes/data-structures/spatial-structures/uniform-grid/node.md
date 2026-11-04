---
tag: F5M3BP
kind: data-structure
slug: uniform-grid
name: Uniform grid bucketing
aliases:
- Uniform grid
- bucket grid
- cell grid
- regular grid
- spatial hash grid
- uniform grid acceleration
area: data-structures/spatial-structures
level: intro
summary: Partition space into equal cells and store each point in its cell; the basis of fixed-radius and grid-based closest pair.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of points, h: the cell side, r: the query radius, b: the size of the bucket of the point, c: the number of cells, m: the number of points in the cells that a query scans, K: the number of pairs at distance at most h}
  time: {insert: O(1), delete: O(1 + b), radius_query: O((2⌈r/h⌉ + 1)^2 + m), close_pairs: O(c + n + K)}
  space: {total: O(c + n)}
prereqs: [array, floor-division]
see_also: [spatial-hashing, fixed-radius-near-neighbors, randomized-closest-pair, quadtree, kd-tree, collision-detection, bucket-sort, space-partitioning]
sources:
  - paper: "Jon L. Bentley, Donald F. Stanat and E. Hollins Williams, The complexity of finding fixed-radius near neighbors, Information Processing Letters 6(6), 1977"
    locator: the cell method (cells of side r, each query point checks its own and the adjacent cells) and its analysis
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning, Section 7.1 Uniform Grids (cell size, grids as arrays of linked lists, and testing an object against the neighbor cells)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 13.7, Finding the Closest Pair of Points, a Randomized Approach (the grid of subsquares of side δ/2 and the dictionary of nonempty subsquares)
  - paper: doi:10.1006/inco.1995.1049
    title: Samir Khuller and Yossi Matias, A simple randomized sieve algorithm for the closest-pair problem, Information and Computation 118(1), 1995
    locator: the grid of cells of side equal to the current distance estimate and the final grid pass
---

Uniform grid bucketing cuts a box of the plane (or of $\mathbb{R}^d$) into equal square cells of side $h$ and keeps, for each cell, a bucket of the points that lie in it. A point finds its cell with two divisions and a [floor](/floor-division/), so insertion takes $O(1)$ time, and a query for the points near $q$ scans only the few cells near $q$. With $h$ equal to a search radius $r$, all pairs of points at distance at most $r$ are found in $O(n + K)$ time plus the number of cells, where $K$ is the number of such pairs. It is the simplest [spatial index](/spatial-index/), and the basis of the cell method for [fixed-radius near neighbors](/fixed-radius-near-neighbors/), of the [randomized closest pair](/randomized-closest-pair/) algorithm, and of the broad phase of [collision detection](/collision-detection/).

## In plain words

Draw a square grid on a map, like the lines on graph paper. Give each square a box, and put each place of the map into the box of the square it is in. To find the square of a place, divide its position by the size of a square and drop the fraction.

To find all places near a spot, you do not look at every place. You look only in the box of the square of the spot and in the boxes of the squares around it. If the squares are as big as the distance you care about, then two places that are that close are always in the same square or in squares next to each other.

The grid works well when the places are spread out evenly. If all places fall into one square, the grid helps nothing.

## The abstract type

The grid implements a [spatial index](/spatial-index/) for a multiset of points in a box: `insert(p)`, `delete(p)`, `radius_query(q, r)`, which reports the stored points $p$ with $\lVert p - q \rVert \le r$, and `close_pairs()`, which reports all pairs of stored points at distance at most $h$. A window query works as the radius query does, with the cells that meet the window. This page uses the plane and the Euclidean distance; the method is the same in each fixed dimension.

## Representation

The grid has an origin $(x_0, y_0)$, a cell side $h > 0$ and $n_x \times n_y$ cells, so it covers the box $[x_0, x_0 + n_x h) \times [y_0, y_0 + n_y h)$. Cell $(i, j)$, for $0 \le i < n_x$ and $0 \le j < n_y$, is the half-open square

$$Z_{ij} = [x_0 + i h,\ x_0 + (i+1) h) \times [y_0 + j h,\ y_0 + (j+1) h).$$

The buckets are an [array](/array/) of $c = n_x n_y$ lists, with the bucket of cell $(i, j)$ at index $j n_x + i$. The cell of a point $p$ in the box is

$$\operatorname{cell}(p) = \left(\left\lfloor \frac{p_x - x_0}{h} \right\rfloor,\ \left\lfloor \frac{p_y - y_0}{h} \right\rfloor\right).$$

**Invariant (G).** Each stored copy of a point $p$ is in the bucket of $\operatorname{cell}(p)$, exactly once, and in no other bucket.

The cells are half-open and tile the box, so each point of the box is in exactly one cell, and (G) gives each point one place.

## Operations

```pseudo id=main
RADIUS-QUERY(G, q, r)                      ▷ report the stored p with |p − q| ≤ r
L1  i0 ← max(0, ⌊(qx − r − x0)/h⌋), i1 ← min(nx − 1, ⌊(qx + r − x0)/h⌋), and j0, j1 the same for y
L2  out ← empty list
L3  for j ← j0 to j1, for i ← i0 to i1 do
L4      for each p in the bucket of cell (i, j) do
L5          if (px − qx)² + (py − qy)² ≤ r² then append p to out
L6  return out
```

Lines L1 to L3 visit each cell that meets the square $[q_x - r, q_x + r] \times [q_y - r, q_y + r]$, which contains the disk of radius $r$ around $q$. The point $q$ itself may lie outside the grid; the bounds are clamped to the grid. Line L5 compares squared distances, so no square root is needed.

```pseudo id=insert
INSERT(G, p)                               ▷ p in the box of the grid
L9  (i, j) ← cell(p)
L10 append p to the bucket of cell (i, j)

DELETE(G, p)
L11 (i, j) ← cell(p)
L12 if p is not in the bucket of cell (i, j) then return false
L13 remove one copy of p from that bucket; return true
```

```pseudo id=pairs
CLOSE-PAIRS(G)                             ▷ all pairs at distance ≤ h
L14 for each cell (i, j) do
L15     test each pair of points in the bucket of (i, j)
L16     for each neighbor (i + 1, j), (i + 1, j + 1), (i, j + 1), (i − 1, j + 1) inside the grid do
L17         test each point of (i, j) against each point of the neighbor
```

A test reports the pair when the distance is at most $h$. Two points at distance at most $h$ are in the same cell or in two cells that touch, by a side or by a corner. Each cell has eight such neighbors, and line L16 takes the four of them that come later in the order of the rows, so each pair of touching cells is examined once.

## Example

Take $(x_0, y_0) = (0, 0)$, $h = 2$, $n_x = 4$ and $n_y = 3$: the box $[0, 8) \times [0, 6)$ in twelve cells. Insert eight points.

| point | cell | point | cell |
|---|---|---|---|
| (1, 1) | (0, 0) | (6.8, 1.6) | (3, 0) |
| (2.5, 1.5) | (1, 0) | (4.1, 5) | (2, 2) |
| (3.5, 3.2) | (1, 1) | (0.4, 4.4) | (0, 2) |
| (6.2, 0.5) | (3, 0) | (5.6, 5.9) | (2, 2) |

| operation | what happens | result |
|---|---|---|
| radius_query((3, 2), 2) | line L1 gives $i$ from 0 to 2 and $j$ from 0 to 2: nine cells. They hold six points; (1, 1) is at distance 2.236 and fails line L5 | (2.5, 1.5) at 0.707, (3.5, 3.2) at 1.3 |
| close_pairs() | 8 distance tests, against the 28 tests of all pairs | (1, 1) and (2.5, 1.5) at 1.581; (2.5, 1.5) and (3.5, 3.2) at 1.972; (3.5, 3.2) and (4.1, 5) at 1.897; (4.1, 5) and (5.6, 5.9) at 1.749; (6.2, 0.5) and (6.8, 1.6) at 1.253 |
| delete((2.5, 1.5)) | removed from the bucket of cell (1, 0) | true |
| radius_query((3, 2), 2) | the same nine cells | (3.5, 3.2) |

The pair (3.5, 3.2) and (4.1, 5) is in cells (1, 1) and (2, 2), which touch only at a corner. A method that looks only at the four cells that share a side would miss it.

## Correctness

INSERT and DELETE keep (G): they change only the bucket of $\operatorname{cell}(p)$, and the formula for the cell does not depend on the other points. RADIUS-QUERY is correct because each point $p$ with $\lVert p - q \rVert \le r$ has $|p_x - q_x| \le r$ and $|p_y - q_y| \le r$, so its cell index lies between the bounds of line L1, and by (G) the loop meets $p$ once and line L5 keeps it. CLOSE-PAIRS is correct because two points at distance at most $h$ differ by less than one cell in each index, so their cells are equal or touch, and each pair of touching cells is examined exactly once. The full proof is in the proofs folder.

## Complexity

The model is the [word RAM](/word-ram/) with real arithmetic and a floor operation in $O(1)$ time.

- **Insert.** $O(1)$: one cell computation and one append.
- **Delete.** $O(1 + b)$ where $b$ is the size of the bucket of $p$; with an index from each point to its place in the bucket, it is $O(1)$.
- **Radius query.** The square of side $2r$ meets at most $\lceil 2r/h \rceil + 1$ cells along each axis, which is at most $2\lceil r/h \rceil + 1$. So the cost is $O((2\lceil r/h \rceil + 1)^2 + m)$, where $m$ is the number of points in those cells. For $r \le h$ this is at most 9 cells, and $O(1 + m)$.
- **Close pairs.** $O(c + n + K)$, where $K$ is the number of pairs at distance at most $h$. The proof is a packing argument. Cut each cell into four subcells of side $h/2$. Two points in one subcell are at distance at most $h/\sqrt 2 < h$, so if subcell $s$ holds $m_s$ points, then $\sum_s \binom{m_s}{2} \le K$. A cell with $n_a$ points has $n_a = \sum_{s \in a} m_s$, and by the Cauchy-Schwarz inequality $n_a^2 \le 4 \sum_{s \in a} m_s^2$. Lines L15 and L17 make at most $\binom{n_a}{2} + \sum_b n_a n_b \le n_a^2 + \tfrac12 \sum_b (n_a^2 + n_b^2)$ tests at cell $a$, over its four forward neighbors $b$. Each cell is a forward neighbor of at most four cells, so the total is at most $5 \sum_a n_a^2 \le 20 \sum_s m_s^2 = 20 \sum_s (2\binom{m_s}{2} + m_s) \le 40K + 20n$.
- **Space.** $O(c + n)$: one list per cell and one entry per point.
- **Worst case.** If all $n$ points fall into one cell, a radius query costs $\Theta(n)$ even when it reports nothing, because the bucket is scanned. The grid gives no bound in terms of $n$ alone; it relies on points that are spread out at the scale $h$.

| operation | time | case |
|---|---|---|
| insert | $O(1)$ | worst |
| delete | $O(1 + b)$ | worst |
| radius_query | $O((2\lceil r/h \rceil + 1)^2 + m)$ | worst |
| close_pairs | $O(c + n + K)$ | worst |
| space | $O(c + n)$ | total |

## Variants

- **Spatial hashing.** Keep only the nonempty cells, in a [hash table](/hash-table/) keyed by $(i, j)$. The space becomes $O(n)$ for an unbounded plane, and each cell lookup takes $O(1)$ expected time. See [spatial hashing](/spatial-hashing/).
- **Compact grid by counting sort.** For a static set, compute the cell of each point, then sort the points by cell index with [counting sort](/counting-sort/). Each bucket is then a range of one array, given by an array of $c + 1$ offsets. This saves the list pointers and keeps each bucket together in memory.
- **Randomized closest pair.** Rabin's idea, made simple by Khuller and Matias and by Kleinberg and Tardos: insert the points in random order into a grid of side $\delta/2$, where $\delta$ is the closest distance so far, and rebuild the grid when $\delta$ drops. Each point checks the 25 cells around it, and the expected time is $O(n)$ with hashing. See [randomized closest pair](/randomized-closest-pair/).
- **Objects with extent.** Store a box in each cell it meets, and remove the duplicate answers of a query. Or store it only in the cell of its lower corner, and widen the query by the largest object size. Ericson treats both.
- **Hierarchical grids.** Several grids with sides $h, 2h, 4h, \ldots$, and each object in the grid whose cells fit its size. This handles objects of very different sizes; the [quadtree](/quadtree/) is the adaptive form of the same idea.
- **Higher dimensions.** In $d$ dimensions a query with $r \le h$ scans $3^d$ cells, which is too many for large $d$.

## When to use it

Use a uniform grid when the points lie in a known box, are spread out fairly evenly, and the queries have one typical radius, so that $h$ can be set to that radius. This is the case for particles in a simulation, for agents in a game and for the cutoff radius of molecular dynamics. Inserts and deletes are $O(1)$, so a grid can be rebuilt in each frame. Use a [quadtree](/quadtree/) or a [k-d tree](/kd-tree/) when the density changes a lot over the box, and use [spatial hashing](/spatial-hashing/) when the box is not known in advance or most cells would be empty.

## Pitfalls

- **Wrong cell size.** With $h$ much smaller than the query radius, a query scans many empty cells; with $h$ much larger, each bucket holds many points that fail line L5. The cost bound of close pairs needs $h$ equal to the radius.
- **Only four neighbors.** Two close points can be in cells that touch only at a corner, as in the example. Line L16 must include the diagonal neighbors.
- **Truncation instead of floor.** In many languages, casting a negative number to an integer rounds toward zero, so $-0.5$ goes to cell 0 instead of cell $-1$. Use a real floor, or shift the origin so that all coordinates are positive.
- **The top edge of the box.** With half-open cells, a point with $p_x = x_0 + n_x h$ has no cell. Make the box a little larger than the data, or clamp the index to $n_x - 1$.
- **Duplicate pairs.** If each cell is tested against all eight neighbors, each pair of points in two cells is found twice. Test only the four forward neighbors, as in line L16, or keep only pairs with the first point smaller.

## Implementations

## History

Bentley, Stanat and Williams analyzed the cell method for fixed-radius near neighbors in 1977: with cells of side $r$, each point needs to look only at its own cell and the cells around it. Rabin used a grid in his 1976 randomized closest pair algorithm, and Khuller and Matias gave a simple linear-time randomized sieve on grids in 1995. In graphics and games, uniform grids have been a standard broad phase for collision detection; Ericson's book of 2005 treats their design in detail.

## References
