---
tag: D6C9DX
kind: data-structure
slug: spatial-hashing
name: Spatial hashing
aliases:
- spatial hash grid
- hash grid
area: data-structures/spatial-structures
level: core
summary: Uniform grid stored in a hash table keyed by cell coordinates, so only occupied cells use memory.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of stored boxes, c: the number of grid cells that the given box or query meets, s: the number of entries stored in those cells, E: the total number of entries in the table, T: the number of buckets}
  time: {insert: O(c), query: O(c + s + c E / T), delete: O(c + s + c E / T)}
  space: {total: O(T + E)}
history:
  year: 2003
  people: [Matthias Teschner, Bruno Heidelberger, Matthias Müller, Danat Pomeranets, Markus Gross]
  note: Hashing grid cells into a table is older folklore of graphics and simulation; Teschner and others gave the widely copied form with a hash of three primes for collision detection of deformable objects in 2003.
prereqs: [uniform-grid, hash-table]
see_also: [uniform-grid, grid-file, geohash, collision-detection, fixed-radius-near-neighbors, loose-octree, locality-sensitive-hashing, universal-hashing]
sources:
  - paper: "Matthias Teschner, Bruno Heidelberger, Matthias Müller, Danat Pomeranets and Markus Gross, Optimized spatial hashing for collision detection of deformable objects, Proceedings of Vision, Modeling, and Visualization (VMV) 2003, pp. 47 to 54"
    title: Teschner, Heidelberger, Müller, Pomeranets and Gross, Optimized spatial hashing for collision detection of deformable objects, VMV 2003
    locator: Section 4 (the hash function of the cell coordinates with three large primes, the table size, and the cell size relative to the object size)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning, Section 7.1 on uniform grids (cell size, hashed storage of an unbounded grid, storing objects in all overlapped cells and avoiding duplicate tests)
  - paper: doi:10.1145/1141911.1141926
    title: Sylvain Lefebvre and Hugues Hoppe, Perfect spatial hashing, ACM Transactions on Graphics 25(3), Proceedings of SIGGRAPH 2006
    locator: Section 1 and Section 3 (a hash of sparse grid data with no collisions, built offline)
  - paper: "Jens-Peter Dittrich and Bernhard Seeger, Data redundancy and duplicate detection in spatial join processing, Proceedings of ICDE 2000, pp. 535 to 546"
    title: Dittrich and Seeger, Data redundancy and duplicate detection in spatial join processing, ICDE 2000
    locator: the reference point method (report a pair only in the cell that holds a fixed corner of the intersection)
---

Spatial hashing is a [uniform grid](/uniform-grid/) whose cells are kept in a [hash table](/hash-table/) instead of an array. Space is cut into square cells of side $h$, a cell is named by its integer coordinates $(\lfloor x/h \rfloor, \lfloor y/h \rfloor)$, and a hash of these two integers picks a bucket. Each box is stored in every cell it meets. Only cells that hold something take memory, so the grid has no bounds and no size fixed in advance, and insert, delete and query cost time in proportion to the number of cells touched. It is the usual broad phase of [collision detection](/collision-detection/) for many moving objects of similar size, and the usual cell list of particle simulation.

## In plain words

Draw a square grid over an infinite plane. You cannot keep an array of all its cells, but most cells are empty, so you only keep the ones that hold something. To find a cell fast, turn its two grid numbers into one number with a hash, and use that number to pick a bucket in a table.

To store an object, find the cells that its box covers and add the object to each. To ask what is near a box, find the cells that the box covers, look in their buckets, and test each object you find.

Two different cells can land in the same bucket. So each entry also keeps the numbers of its cell, and a lookup skips the entries of the other cells.

## The abstract type

Spatial hashing implements a [spatial index](/spatial-index/) for boxes: `insert(id, b)`, `delete(id, b)`, and `query(q)`, which reports each stored box that meets the box $q$ exactly once. A point query is a query with a box of size zero. For points and a radius $r$, a query with the box $[x - r, x + r] \times [y - r, y + r]$ and an exact test of distance gives a [fixed radius near neighbor](/fixed-radius-near-neighbors/) search. The operation `close_pairs()` reports all pairs of stored boxes that meet, which is the broad phase of collision detection.

## Representation

Fix the cell side $h > 0$. The cell of a point $(x, y)$ is $(\lfloor x/h \rfloor, \lfloor y/h \rfloor)$, a pair of integers that may be negative. A closed box $b = [x_1, x_2] \times [y_1, y_2]$ meets the cells $(i, j)$ with $\lfloor x_1/h \rfloor \le i \le \lfloor x_2/h \rfloor$ and $\lfloor y_1/h \rfloor \le j \le \lfloor y_2/h \rfloor$. A box of side at most $h$ meets at most 4 cells.

The table has $T$ buckets. Cell $(i, j)$ goes to bucket
$$H(i, j) = \big( (i \cdot p_1) \oplus (j \cdot p_2) \big) \bmod T,$$
where $\oplus$ is the bitwise exclusive or, and $p_1 = 73856093$ and $p_2 = 19349663$ are the primes of Teschner and others. In three dimensions a third term $k \cdot p_3$ is added in the same way. Any hash of the pair works if it spreads the cells well; a [universal hash](/universal-hashing/) gives a bound on the expected collisions for every input.

A bucket is a list of entries $(i, j, id, b)$: the cell, the identifier and the box.

**Invariant (S).** For each stored box $b$ and each cell $(i, j)$ that $b$ meets, bucket $H(i, j)$ holds the entry $(i, j, id, b)$ exactly once, and there are no other entries.

An entry keeps its cell because $H$ is not one to one: different cells can share a bucket, and a lookup of cell $(i, j)$ must skip the entries of the other cells. A [dictionary](/dictionary/) keyed by $(i, j)$, as in most languages, does the same check inside the table.

## Operations

```pseudo id=main
INSERT(id, b)
L1  for each cell (i, j) that b meets:
L2      append (i, j, id, b) to bucket H(i, j)
L3  n ← n + 1

QUERY(q)                                     ▷ report each stored box that meets q, once
L4  for each cell (i, j) that q meets:
L5      for each entry (i', j', id, b) in bucket H(i, j):
L6          if (i', j') ≠ (i, j) or b does not meet q then skip the entry
L7          if the cell of the point (max(x1 of q, x1 of b), max(y1 of q, y1 of b)) is (i, j) then report id

DELETE(id, b)
L8  for each cell (i, j) that b meets:
L9      remove the entry (i, j, id, b) from bucket H(i, j), by moving the last entry into its place
```

A box that meets several cells has an entry in each, so a query that covers several of them would find it several times. Line L7 is the *reference point* test: if $q$ and $b$ meet, their intersection is a box, and its lower left corner $(\max(q_{x1}, b_{x1}), \max(q_{y1}, b_{y1}))$ lies in exactly one cell. That cell is met by both $q$ and $b$, so the scan reaches it, and the pair is reported only there. This avoids a set of reported identifiers. The same test, with two stored boxes in place of $q$ and $b$, makes `close_pairs` report each meeting pair once: for each cell, it tests the pairs of entries of that cell.

## Example

Take $h = 10$ and $T = 8$ buckets. The four boxes are

| box | rectangle | cells | buckets |
|---|---|---|---|
| A | $[2, 8] \times [3, 7]$ | (0, 0) | 0 |
| B | $[15, 27] \times [5, 12]$ | (1, 0), (1, 1), (2, 0), (2, 1) | 5, 2, 2, 5 |
| C | $[-6, -1] \times [-4, 4]$ | (-1, -1), (-1, 0) | 2, 3 |
| D | $[31, 33] \times [31, 33]$ | (3, 3) | 2 |

The buckets need only the last 3 bits of each product, since $T = 8$: $p_1 \bmod 8 = 5$ and $p_2 \bmod 8 = 7$. For cell (1, 1) the bucket is $5 \oplus 7 = 2$, for (2, 1) it is $(10 \bmod 8) \oplus 7 = 2 \oplus 7 = 5$, and for (-1, -1) it is $3 \oplus 1 = 2$, since $-5 \equiv 3$ and $-7 \equiv 1 \pmod 8$. The table has 8 entries, and the bucket sizes are 1, 0, 4, 1, 0, 2, 0, 0. Bucket 2 holds four different cells: (1, 1), (2, 0), (-1, -1) and (3, 3).

- QUERY($[5, 16] \times [4, 9]$) meets the cells (0, 0) and (1, 0). In bucket 0, A meets the query, and the corner $(\max(5, 2), \max(4, 3)) = (5, 4)$ is in cell (0, 0): report A. In bucket 5, the entry of B for (1, 0) matches the cell and meets the query, and its corner (15, 5) is in cell (1, 0): report B. The entry of B for (2, 1) in the same bucket is skipped by its cell. The answer is A and B.
- QUERY($[-3, 12] \times [-3, 6]$) meets six cells, $i \in \{-1, 0, 1\}$ and $j \in \{-1, 0\}$. C meets the query, and the corner $(-3, -3)$ is in cell $(-1, -1)$, so C is reported there and not again in cell $(-1, 0)$. A is reported in cell (0, 0). In bucket 2, the entries for (2, 0) and (3, 3) belong to other cells and are skipped. The answer is A and C.
- QUERY($[30, 30.5] \times [30, 30.5]$) looks at cell (3, 3), finds D, and D does not meet the query: no answer.
- DELETE(B) removes its four entries, and the table has 4 entries left.

## Correctness

By (S), every entry that line L5 meets for cell $(i, j)$ and that passes the cell check of line L6 is a box that meets cell $(i, j)$. If a stored box $b$ meets $q$, let $p$ be the lower left corner of $b \cap q$ and let $(i, j)$ be its cell. Both $b$ and $q$ contain $p$, so both meet $(i, j)$: line L4 visits the cell, and by (S) the bucket holds the entry of $b$ for it. Lines L6 and L7 then report $b$. In any other cell, line L7 fails, since $p$ has one cell. So each answer is reported once, and only boxes that meet $q$ are reported. INSERT and DELETE add and remove exactly the entries that (S) asks for. The full proof is in the proofs folder.

## Complexity

The model is the word RAM, with the cost of the hash and of a floor as $O(1)$. Let $c$ be the number of cells that a box meets, $E$ the number of entries in the table, and $T$ the number of buckets.

- **Insert.** One hash and one append per cell, $O(c)$.
- **Query.** Line L4 visits $c$ cells. In each, the bucket holds the $s_{ij}$ entries of the cell and the entries of other cells that share the bucket. If the hash spreads cells like a random function, a bucket holds $E/T$ entries of other cells in expectation, so the query costs $O(c + s + cE/T)$ expected time, where $s$ is the number of entries in the $c$ cells. With $T \ge E$ this is $O(c + s)$.
- **Delete.** The same scan of the $c$ buckets, $O(c + s + cE/T)$ expected.
- **Space.** $O(T + E)$. Each box makes $c$ entries, so $E = \sum_b c_b$, which is at most $4n$ when no box is wider than $h$.
- **Close pairs.** With the reference point test, $O(E + \sum_{\text{cells}} s_{ij}^2)$. If no box is wider than $h$ and no cell holds more than a constant number of boxes, as in a simulation with a bounded density, this is $O(n)$.

The bounds are good only when $h$ fits the data. A cell much smaller than the boxes gives large $c$; a cell much larger than the boxes gives large $s$. A common rule is to make $h$ about the size of the largest box, or the interaction radius. With objects of very different sizes, no single $h$ is good, and a hierarchy of grids or a tree is better.

| operation | time | case |
|---|---|---|
| insert | $O(c)$ | worst |
| query | $O(c + s + cE/T)$ | expected |
| delete | $O(c + s + cE/T)$ | expected |
| close pairs | $O(E + \sum s_{ij}^2)$ | expected |
| space | $O(T + E)$ | worst |

## Variants

- **Points only.** If the objects are points, each has one cell, $c = 1$ for an insert, and no duplicate test is needed. A radius query looks at the $3 \times 3$ block of cells around the point when $h \ge r$, as in the [uniform grid](/uniform-grid/).
- **Dictionary keyed by cells.** Use a [dictionary](/dictionary/) from $(i, j)$ to a list. The table then grows with the number of occupied cells, at the cost of a resize now and then.
- **One reference cell.** Store each box only in the cell of its center, and have queries look one ring of cells wider, by the largest half side. This makes $c = 1$ for each insert, at the cost of larger queries. A [loose octree](/loose-octree/) does the same in a hierarchy.
- **Hierarchical grids.** Several grids, with $h$ doubling from one to the next, and each object in the grid whose cells fit its size. This handles objects of very different sizes.
- **Perfect spatial hashing.** For static data, Lefebvre and Hoppe build offline a hash with no collisions that fits in a small table, for lookups on a graphics processor.
- **Geographic cells.** A [geohash](/geohash/) names cells of latitude and longitude by strings, and a key value store plays the role of the table.
- **Locality-sensitive hashing.** [Locality-sensitive hashing](/locality-sensitive-hashing/) uses random grids, many of them, to find approximate near neighbors in high dimensions, where a fixed grid fails.

## When to use it

Use spatial hashing when many objects of similar size move every step and you need all close pairs, or all objects near a point, as in particle systems, crowds, games and molecular dynamics. It is simple, it rebuilds in linear time, and it needs no bounds of the world. Use an array [uniform grid](/uniform-grid/) when the world is bounded and dense. Use a tree, such as a [k-d tree](/kd-tree/), an [R-tree](/r-tree/) or a [bounding volume hierarchy](/bounding-volume-hierarchy/), when sizes vary a lot or the data is very clustered.

## Pitfalls

- **Rounding toward zero.** The cell must use the floor. Casting $-0.5/h$ to an integer in C or Java gives 0, not $-1$, so cells $-1$ and 0 merge into one cell of double width, and points near 0 go to the wrong cell.
- **No cell check.** Two cells can share a bucket. Without the check of line L6, a query sees entries of far away cells. With an exact test on the box this is only slow, but code that trusts the bucket as the cell gives wrong pairs.
- **Duplicates.** A box in several cells is found several times. Use the reference point test, a set of seen identifiers, or a time stamp per object.
- **Wrong cell size.** A cell much smaller or much larger than the objects makes the structure slow, not wrong. Choose $h$ from the data.
- **Overflow in the hash.** In languages with fixed width integers, $i \cdot p_1$ wraps. That is harmless for a hash if it is done the same way every time, but a signed result of the modulo can be negative in C, and it must be made non negative before it is used as an index.
- **Bad hash.** A hash such as $(i + j) \bmod T$ puts the cells of a whole diagonal in one bucket. Mix the coordinates with large odd multipliers.

## Implementations

## History

Grids of cells for near neighbor search were used in simulation and graphics from the 1960s and 1970s, and storing only the occupied cells in a hash table was common practice long before it had a name. Teschner, Heidelberger, Müller, Pomeranets and Gross published in 2003 the form that most code copies, with three large primes, a table of fixed size, and the cell size chosen near the average object size, for collision detection of deformable tetrahedral meshes. Ericson's book of 2005 gave the method in detail for games. Lefebvre and Hoppe introduced perfect spatial hashing for graphics hardware in 2006.

## References
