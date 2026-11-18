---
tag: G5JMTR
kind: algorithm
slug: branch-and-bound-skyline
name: Branch-and-bound skyline
aliases:
- BBS skyline
area: databases/query-processing
level: advanced
summary: "Find the skyline with an R-tree: take entries from a heap in order of L1 mindist from the origin, and drop each entry whose lower corner a skyline point found so far dominates."
solves: [pareto-front-computation]
model: word-ram
complexity:
  vars: {n: the number of points, d: the number of dimensions, s: the number of skyline points, b: the node capacity of the R-tree, r: the number of R-tree nodes whose lower corner no point dominates}
  time: {worst: "O(r b (log(r b) + s d))"}
  space: {extra: "O(r b + s)"}
  io: {worst: "r"}
properties: {deterministic: true, exact: true, external: true, online: true, in_place: false, recursive: false}
history:
  year: 2003
  people: [Dimitris Papadias, Yufei Tao, Greg Fu, Bernhard Seeger]
  note: "Papadias, Tao, Fu and Seeger gave BBS at SIGMOD 2003 and a longer version in ACM TODS in 2005."
prereqs: [pareto-dominance, r-tree, best-first-search]
see_also: [bnl-skyline, sort-filter-skyline, pareto-front-computation, priority-queue, depth-first-branch-and-bound, kd-tree, top-k-query, skyline-problem]
sources:
  - paper: doi:10.1145/872757.872814
    title: "Dimitris Papadias, Yufei Tao, Greg Fu and Bernhard Seeger, An optimal and progressive algorithm for skyline queries, SIGMOD 2003, pages 467 to 478"
    locator: the BBS algorithm, its I/O optimality and its variants
  - paper: doi:10.1145/1061318.1061320
    title: "Dimitris Papadias, Yufei Tao, Greg Fu and Bernhard Seeger, Progressive skyline computation in database systems, ACM Transactions on Database Systems 30(1), 2005, pages 41 to 82"
    locator: the journal version, with the proof that BBS reads only the nodes that may contain skyline points and the variations of skyline queries
  - paper: doi:10.1109/ICDE.2001.914855
    title: "Stephan Börzsönyi, Donald Kossmann and Konrad Stocker, The skyline operator, ICDE 2001, pages 421 to 430"
    locator: the skyline operator and the block-nested-loops and divide-and-conquer algorithms
  - paper: doi:10.1016/b978-155860869-6/50032-9
    title: "Donald Kossmann, Frank Ramsak and Steffen Rost, Shooting stars in the sky: an online algorithm for skyline queries, VLDB 2002, pages 275 to 286"
    locator: the nearest-neighbor skyline algorithm with an R-tree, which BBS improves on
  - paper: doi:10.1016/s0169-023x(02)00208-2
    title: "Pin-Kwang Eng, Beng Chin Ooi and Kian-Lee Tan, Indexing for progressive skyline computation, Data and Knowledge Engineering 46(2), 2003, pages 169 to 201"
    locator: progressive skyline computation with an index
  - paper: doi:10.1109/ICDE.1997.582015
    title: "Scott T. Leutenegger, Mario A. Lopez and Jeffrey Edgington, STR: a simple and efficient algorithm for R-tree packing, ICDE 1997, pages 497 to 506"
    locator: the Sort-Tile-Recursive packing that the implementation uses to build the R-tree
---

The branch-and-bound skyline algorithm (BBS) computes the *skyline* of a set of points, the points that no other point dominates, from an [R-tree](/r-tree/) on the points. It keeps a [priority queue](/priority-queue/) of tree entries ordered by *mindist*, the L1 distance from the origin to the lower corner of the entry, and it takes the nearest entry first. An entry whose lower corner a skyline point found so far dominates is dropped with its whole subtree. [Block-nested-loop skyline](/bnl-skyline/) and [sort-filter skyline](/sort-filter-skyline/) read every point. BBS reads only the tree nodes that could hold a skyline point, and it outputs each skyline point as soon as it finds it. This database skyline is the [Pareto front](/pareto-front-computation/), not the [skyline problem](/skyline-problem/) of buildings.

## In plain words

You look for a hotel that is cheap and near the beach. A hotel is not worth a look if another one is no worse in both and better in one. The skyline is the hotels that are left.

The hotels are filed in boxes, and each box has a label that gives the lowest price and the shortest distance of the hotels in it. You open boxes in order of how good their label looks, the best label first.

A hotel that comes out first beats nothing that came before it, so it is in the skyline. When the label of a box is already beaten by a skyline hotel that you found, then every hotel in that box is beaten too, and you put the box away without opening it.

## The problem

The input is a multiset $P$ of $n$ points in $d$ dimensions, where smaller values are better in every dimension. A point $p$ *dominates* a point $q$ when $p_i \le q_i$ for every $i$ and $p_i < q_i$ for some $i$ (see [Pareto dominance](/pareto-dominance/)). The output is every point of $P$ that no point of $P$ dominates. Equal points do not dominate each other, so all copies of a skyline point are in the output. For an attribute where larger is better, negate it first.

The points are stored in an R-tree with node capacity $b$. Each node has a minimum bounding rectangle (MBR) with a lower corner $\ell$, the smallest value in each dimension of the points below it. The key of an entry is the sum of the coordinates of its lower corner, and for a point the sum of its coordinates. When all values are not negative, the key is the L1 distance from the origin.

**Cost model.** The main measure is the number of R-tree nodes read, since each node is one disk page. The second measure is the work in the [word RAM](/word-ram/), with a binary heap and a scan of the skyline found so far for each dominance test.

## The algorithm

```pseudo id=main
BBS(R)                               ▷ R: an R-tree on the points; smaller is better
L1  S ← empty list; H ← a min-heap that holds the root of R with key mindist(root)
L2  while H is not empty do
L3      e ← the entry of H with the smallest key; remove it
L4      if some point of S dominates the lower corner of e then continue
L5      if e is a node then
L6          for each child c of e do if no point of S dominates the lower corner of c then insert c in H with key mindist(c)
        else
L7          append the point e to S   ▷ output e now
L8  return S
```

Line L6 tests a child before it enters the heap, and line L4 tests it again when it leaves, because $S$ may have grown in the meantime. Both tests use the same rule: if a point dominates the lower corner of a rectangle, it dominates every point in the rectangle. This is the *bound* of branch and bound, and the heap order is the *branch* rule, as in [best-first search](/best-first-search/).

## Example

Take the 12 points $a(1, 9)$, $b(2, 10)$, $c(4, 8)$, $d(3, 6)$, $e(6, 7)$, $f(9, 10)$, $g(7, 5)$, $h(5, 4)$, $i(8, 3)$, $j(9, 1)$, $k(10, 4)$ and $l(8, 8)$, in an R-tree with capacity 3 built by Sort-Tile-Recursive packing. The root, with lower corner $(1, 1)$, has two children. $N_1$, with corner $(1, 4)$, holds the leaves $L_1 = \{d, e, h\}$ with corner $(3, 4)$, $L_2 = \{f, g, l\}$ with corner $(7, 5)$ and $L_3 = \{a, b, c\}$ with corner $(1, 8)$. $N_2$, with corner $(8, 1)$, holds the leaf $L_4 = \{i, j, k\}$ with corner $(8, 1)$. The skyline is $h, d, a, j, i$.

| step | entry taken (key) | action | skyline $S$ |
|---|---|---|---|
| 1 | root (2) | read it; insert $N_1$ (5) and $N_2$ (9) | |
| 2 | $N_1$ (5) | read it; insert $L_1$ (7), $L_3$ (9) and $L_2$ (12) | |
| 3 | $L_1$ (7) | read it; insert $h$ (9), $d$ (9) and $e$ (13) | |
| 4 | $N_2$ (9) | read it; insert $L_4$ (9) | |
| 5 | $L_3$ (9) | read it; insert $a$ (10), $c$ (12) and $b$ (12) | |
| 6 | $h$ (9) | output | $h$ |
| 7 | $d$ (9) | output | $h, d$ |
| 8 | $L_4$ (9) | read it; insert $j$ (10) and $i$ (11); $h$ dominates $k$, so $k$ does not enter | $h, d$ |
| 9 | $a$ (10), $j$ (10), $i$ (11) | output each | $h, d, a, j, i$ |
| 10 | $L_2$ (12), $c$ (12), $b$ (12), $e$ (13) | drop: $h$ dominates the corner $(7, 5)$ and $e$, $d$ dominates $c$, $a$ dominates $b$ | $h, d, a, j, i$ |

Ties in the key are taken in the order of insertion. BBS reads 6 of the 7 nodes. It never reads $L_2$, because the corner $(7, 5)$ of $L_2$ is dominated by $h$, and so every point in $L_2$ is dominated by $h$.

## Correctness

The keys of the entries taken from the heap never decrease, because a child or a point below a node has a lower corner no smaller than the corner of the node. A point that dominates another point has a smaller key. So when a point $q$ leaves the heap, every skyline point that dominates $q$ has a smaller key and is in $S$ already, and $q$ is dropped at line L4. A skyline point is never dropped, since a point that dominated the corner of one of its ancestors would dominate it too. So BBS outputs exactly the skyline, in order of key. The full proof is in [the proof page](proofs/correctness.md).

The same argument gives the node count. BBS reads a node if and only if no point of $P$ dominates its lower corner. Without the points, a node with such a corner could hold a point at that corner, which would be in the skyline. So no algorithm that uses only the rectangles of the R-tree can be sure of the skyline while it leaves such a node unread. This is the I/O optimality that Papadias et al. claim for BBS.

## Complexity

- **Node reads.** Exactly $r$, the number of nodes whose lower corner no point dominates. Each node is read at most once, because only its parent inserts it.
- **Work.** Each node read inserts at most $b$ entries, so the heap gets at most $r b + 1$ entries. Each insert and each removal costs $O(\log(r b))$, and each entry is tested against $S$ at most twice, in $O(s d)$ by a scan. The total is $O(r b (\log(r b) + s d))$ in the word RAM. A spatial index on $S$ in place of the scan makes the tests faster when the skyline is large.
- **Space.** The heap holds at most $r b + 1$ entries and $S$ holds $s$ points. In the worst case, for example when all points are in the skyline, $r$ is the number of all nodes and the heap can hold a large part of the data.
- **Building the tree.** The R-tree is a cost paid once for many queries. The implementation builds it by Sort-Tile-Recursive packing in $O(n \log n)$ time.

## Properties

- **Progressive.** Each point is final when it is output, because a point taken later has a key no smaller and cannot dominate it. The first results come after only a few node reads.
- **Output order.** The skyline comes out in order of key, the sum of the coordinates.
- **Exact.** The result does not depend on the shape of the R-tree. Only the number of node reads does.
- **Duplicates.** All copies of a skyline point are output, because equal points do not dominate each other.

## Variants and improvements

- **Constrained skyline.** To find the skyline of the points in a query rectangle, drop the entries that do not meet the rectangle, and use the corner of the part of each rectangle inside the query.
- **Top-k skyline points.** With any monotone function in place of the sum as the key, the skyline points come out in order of that function, so the first $k$ of them answer a [top-k query](/top-k-query/) that is restricted to the skyline.
- **K-skyband.** To find the points that fewer than $K$ points dominate, keep every point that is output and drop an entry only when $K$ of them dominate its corner.
- **Other indexes.** The same scheme works on any tree whose nodes give a lower corner, such as a [k-d tree](/kd-tree/) with the bounding box of each node.
- **Nearest-neighbor skyline.** Kossmann, Ramsak and Rost (2002) found skyline points by repeated nearest-neighbor searches in an R-tree, splitting the space into parts after each result. That method can read the same node in several searches. BBS reads each node at most once.

## When to use it

Use BBS when the points have an R-tree or a similar index, the skyline is asked often, and the dimensions are few, so that the skyline is small compared with the data. Then BBS reads only a small part of the tree and gives the first answers quickly. Without an index, or for a single query on data that is used once, a scan such as [sort-filter skyline](/sort-filter-skyline/) avoids the cost of the index. In many dimensions most points are in the skyline, few corners are dominated, and BBS reads nearly every node.

## Pitfalls

- **The wrong corner.** For minimization the key and the test must use the lower corner of the rectangle. The upper corner gives a key that is too large, and points come out before the points that dominate them.
- **Testing only once.** If the test of line L4 is left out, an entry inserted before its dominator was found is read anyway. The result stays correct, but the node count grows.
- **Ties in the key.** Two points with the same key cannot dominate each other, so any order of ties is correct. A key that is not strictly monotone, such as the maximum coordinate, breaks this, and a dominated point can come out first.
- **Larger is better.** Negate those attributes, or use the upper corners and the distance from the largest values. Mixing the two directions in one tree gives wrong results.
- **Heap memory.** The heap is not bounded by the size of the skyline. In anticorrelated data it can hold a large part of the tree.

## Implementations

## History

Börzsönyi, Kossmann and Stocker (2001) added the skyline operator to SQL and gave the block-nested-loops and divide-and-conquer algorithms, which read all the data. Kossmann, Ramsak and Rost (2002) gave a progressive algorithm by nearest-neighbor search in an R-tree, and Eng, Ooi and Tan (2003) studied progressive skyline computation with other indexes. Papadias, Tao, Fu and Seeger (SIGMOD 2003) replaced the repeated nearest-neighbor searches with one best-first traversal and showed that BBS reads only the nodes that may contain skyline points. The journal version of 2005 extended BBS to several variations of the skyline query.

## References
