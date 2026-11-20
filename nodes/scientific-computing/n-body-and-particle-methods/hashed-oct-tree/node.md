---
tag: 4795RQ
kind: data-structure
slug: hashed-oct-tree
name: Hashed oct-tree
aliases:
- Warren-Salmon tree
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: An octree whose cells sit in a hash table keyed by Morton codes, so a parallel tree code can find any cell and share cells across processors.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {N: the number of bodies, L: the depth of the keys, B: the leaf capacity}
  time: {build: "O(N log N + N L)", lookup: "O(1) expected", parent: "O(1)", find_leaf: "O(L) expected"}
  space: {total: "O(N L)"}
history:
  year: 1993
  people: [Michael S. Warren, John K. Salmon]
  note: Warren and Salmon described the hashed oct-tree for parallel N-body codes at Supercomputing 1993, with key-based addresses for cells and a domain decomposition along the key order.
prereqs: [octree, z-order-curve, hash-table]
see_also: [barnes-hut-algorithm, linear-quadtree, space-filling-curve, hilbert-curve, spatial-hashing, radix-sort, multipole-acceptance-criterion, fast-multipole-method]
sources:
  - paper: doi:10.1145/169627.169640
    title: "Michael S. Warren and John K. Salmon, A parallel hashed oct-tree N-body algorithm, Proceedings of Supercomputing 1993, 12-21"
    locator: the keys of cells, the hash table from keys to cells and the parallel decomposition
  - paper: doi:10.1006/jcph.1994.1050
    title: "John K. Salmon and Michael S. Warren, Skeletons from the treecode closet, Journal of Computational Physics 111(1), 1994, 136-155"
    locator: the error-bound acceptance criteria used with the tree
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data (linear quadtrees and locational codes)
---

A hashed oct-tree is an [octree](/octree/) without pointers. Each cell is named by an integer key, built from the bits of its integer coordinates in the [Z-order](/z-order-curve/), with a leading 1 bit that marks its level. A [hash table](/hash-table/) maps each key to the data of the cell. The parent and the children of a cell are found by shifting its key, and any cell is found by one table lookup, from its key alone. Warren and Salmon designed it for parallel tree codes: a processor can ask for a cell of another processor by its key, the bodies are divided among processors along the key order, and each processor stores only the cells it needs. It is close to a [linear quadtree](/linear-quadtree/), which stores the leaf keys in sorted order; the hashed oct-tree stores all cells and uses hashing instead of search.

## In plain words

An ordinary tree keeps, for each box, links to its smaller boxes. Here each box gets a number instead. The number of the big box is one. To get the number of a smaller box, write the number of its parent and add one digit from zero to seven that says which of the eight parts it is.

So from the number of a box you can find its parent and its children by simple steps, without any links. All boxes are kept in a table that finds a box from its number very fast. This is useful when many computers share one tree: a computer can ask another one for a box just by sending its number. Sorting bodies by the number of their smallest box also puts nearby bodies next to each other.

## The abstract type

A hashed oct-tree stores a set of $N$ points in a cube and supports:

- **lookup(key):** the cell with this key, or a report that it does not exist.
- **parent(key)** and **children(key):** the keys of the neighbors in the tree.
- **bounds(key):** the cube of a key.
- **find-leaf(p):** the deepest stored cell whose cube holds the point $p$.
- **build(points):** the tree in which a cell is split while it holds more than $B$ points and is above level $L$.

In a tree code each cell also stores the mass, the center of mass and the higher moments of its bodies, as for the [Barnes-Hut algorithm](/barnes-hut-algorithm/).

## Representation

Fix the root cube of side $S$ and a depth $L$ (at most 21 in 3D, so that keys fit in 64 bits). A cell at level $l$ has integer coordinates $0 \le i, j, k < 2^l$. Its key is the bit 1 followed by $l$ octal digits; the digit of level $b$ is $4 k_b + 2 j_b + i_b$, from the highest bits of the coordinates to the lowest. So:

- the root has the key $1$;
- the children of the key $K$ are $8K + c$ for $c = 0, \ldots, 7$, and the parent is $\lfloor K / 8 \rfloor$;
- the level of $K$ is $(\lfloor \log_2 K \rfloor) / 3$;
- the keys of one level, in increasing order, follow the [Z-order curve](/z-order-curve/).

The leading 1 bit makes keys of different levels different: without it, the root and its child 0 would both have the key 0. The bodies are sorted by their keys at level $L$, and each stored cell holds the range of the sorted bodies that lie in it, or its moments.

## Operations

```pseudo id=main
KEY(p)                                       ▷ key of the level-L cell that holds p
L1  (i, j, k) ← ⌊2^L (p - lo) / S⌋, coordinate by coordinate
L2  K ← 1
L3  for b ← L - 1 downto 0 do K ← 8K + 4 k_b + 2 j_b + i_b
L4  return K

BUILD(points)
L5  sort the points by KEY
L6  push (1, all points) on a stack
    while the stack is not empty do pop (K, R)
L7      T[K] ← R                              ▷ T is the hash table
L8      if |R| > B and level(K) < L then
            split R into runs by the next octal digit of the keys; push (8K + c, run c) for each run

LOOKUP(K)
L9  return T[K]
PARENT(K)
L10 return K >> 3
```

Line L5 is what makes the split of line L8 easy: in the sorted order, the bodies of each cell are one run of consecutive positions. Find-leaf computes the level-$L$ key of the point and tests its prefixes $K \gg 3(L - l)$ for $l = 1, 2, \ldots$ until one is missing from the table. A binary search over $l$ also works, because the stored prefixes of a point form an initial segment of the levels.

## Example

Take the unit cube, $L = 3$, $B = 1$ and four bodies.

| body | position | level-3 coordinates | key (octal) |
|---|---|---|---|
| B | (0.1, 0.1, 0.1) | (0, 0, 0) | 1000 |
| A | (0.6, 0.3, 0.8) | (4, 2, 6) | 1560 |
| D | (0.65, 0.35, 0.85) | (5, 2, 6) | 1561 |
| C | (0.9, 0.9, 0.9) | (7, 7, 7) | 1777 |

For A, the coordinates in binary are $i = 100$, $j = 010$, $k = 110$, so the digits are $4 \cdot 1 + 2 \cdot 0 + 1 = 5$, then $4 \cdot 1 + 2 \cdot 1 + 0 = 6$, then $0$. Sorted by key, the order is B, A, D, C. The root (key 1) holds four bodies and splits into the cells 10 (B), 15 (A, D) and 17 (C). Cell 15 holds two bodies and splits; both are in its child 156, which splits again into 1560 (A) and 1561 (D). The table holds the seven keys 1, 10, 15, 17, 156, 1560 and 1561 (octal). The parent of 1561 is 156, its level is 3, and the lookup of 157 reports that the cell does not exist.

## Correctness

Each key names one cell, because the bit length gives the level and the remaining bits give the coordinates (Lemma 1 of the proof file). Removing the last octal digit gives the key of the parent, because it removes the last bit of each coordinate (Lemma 2). So the key of the level-$l$ cell that holds a point is a prefix of the point's level-$L$ key (Lemma 3), and in the sorted order the bodies of each cell are consecutive (Lemma 4). The build keeps the invariant that each stack entry holds exactly the bodies of its cube; splitting by the next digit gives the runs of the children. So the table holds the cells of the octree with leaf capacity $B$, each with its bodies.

## Complexity

In the [word RAM](/word-ram/) model with keys of $3L + 1 \le w$ bits:

- **Build:** sorting $N$ keys costs $O(N \log N)$, or $O(N L)$ with a [radix sort](/radix-sort/) by octal digits; the splits touch each body once per level, $O(N L)$.
- **Lookup:** one hash access, $O(1)$ expected time. **Parent and children:** a shift, and 8 lookups for the children.
- **Find-leaf:** $O(L)$ expected time by testing prefixes from the root, or $O(\log L)$ lookups by binary search over the levels.
- **Space:** at most $N(L + 1)$ cells; $O(N)$ for well-spread bodies.

## Variants

- **Hilbert keys.** Keys from the [Hilbert curve](/hilbert-curve/) keep neighboring cells closer in the order, which gives better domains for the processors; the key arithmetic is more complex.
- **Linear octree.** Store only the leaf keys in a sorted array and search it by binary search ([linear quadtree](/linear-quadtree/)).
- **Bodies in key order.** The bodies themselves are stored in key order, so each cell is a range of an array, and the moments of a cell are sums over a range.
- **Parallel decomposition.** Split the sorted keys into $P$ ranges of equal work, one per processor. Each processor builds the cells of its range and asks others for the cells that the [acceptance criterion](/multipole-acceptance-criterion/) needs; replies are cached in the local table.
- **Two dimensions.** With 2 bits per level, the same scheme gives a hashed quadtree.

## When to use it

Use a hashed oct-tree in parallel tree codes and [fast multipole methods](/fast-multipole-method/) on distributed memory, where pointers can not cross processors. Use it when cells must be found from their position, for example to find the neighbors of a cell by computing their keys. On a single processor with a tree that is built once and walked from the root, a pointer octree is simpler and about as fast.

## Pitfalls

- **Forgetting the leading 1 bit.** Without it, keys of different levels collide.
- **Too deep a key.** In 3D with 64-bit keys, $L \le 21$. Bodies closer than $S 2^{-21}$ get the same key and must share a leaf.
- **Points on the far face.** A point with $p = lo + S$ gives the coordinate $2^L$, which is out of range. Clamp it, or make the root cube slightly larger.
- **Bad hash functions.** Keys of one region share their high bits. A hash that uses only the high bits, or a table size that is a power of 2 with the low bits of a key, can cluster; mix the bits.
- **Z-order is not distance.** Most bodies with close keys are near each other, but two near bodies can have keys far apart when a boundary of a large cell lies between them.

## Implementations

## History

Morton described the interleaving of bits for a geographic database in 1966, and the linear quadtrees of the 1980s used such locational codes for image data. Warren and Salmon (1993) added the leading bit, put all cells in a hash table and used the key order to divide the bodies among the processors of a parallel computer. Their codes ran cosmological simulations with millions of bodies on parallel machines of the early 1990s.

## References
