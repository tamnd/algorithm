---
tag: SE99CH
kind: data-structure
slug: generalized-search-tree
name: Generalized search tree (GiST)
aliases:
- GiST
area: databases/storage-and-indexing
level: advanced
summary: "A balanced tree template whose keys are predicates. Six key methods (Consistent, Union, Compress, Decompress, Penalty, PickSplit) turn it into a B+ tree, an R-tree or other indexes."
model: external-memory-model
complexity:
  vars: {n: the number of records, M: the largest number of entries in a node, m: the smallest number of entries in a node other than the root, h: the height of the tree}
  time: {worst: "O(n)", average: "O(h M)", best: "O(h M)"}
  space: {extra: "O(n)"}
  io:
    worst: "O(n / m)"
    average: "O(log_m n)"
    best: "O(log_m n)"
properties: {deterministic: true, exact: true, external: true, online: true, in_place: false, recursive: true}
history:
  year: 1995
  people: [Joseph M. Hellerstein, Jeffrey F. Naughton, Avi Pfeffer]
  note: "Hellerstein, Naughton and Pfeffer defined the GiST at VLDB 1995 as one tree whose search and update code is shared by B+ trees, R-trees and other indexes. Kornacker, Mohan and Hellerstein added concurrency and recovery in 1997."
prereqs: [b-plus-tree, r-tree]
see_also: [blink-tree, spatial-join, nearest-neighbor-search, interval-tree, kd-tree, bloom-filter, prefix-b-tree, partial-index]
sources:
  - url: http://www.vldb.org/conf/1995/P562.PDF
    title: "Joseph M. Hellerstein, Jeffrey F. Naughton and Avi Pfeffer, Generalized search trees for database systems, Proceedings of the 21st International Conference on Very Large Data Bases (VLDB 1995)"
    locator: pp. 562 to 573, the tree properties, the six key methods, the tree methods Search, Insert (with ChooseSubtree, Split and AdjustKeys) and Delete, the methods for linearly ordered domains, and the B+ tree, R-tree and RD-tree instances
  - paper: doi:10.1145/253262.253272
    title: "Marcel Kornacker, C. Mohan and Joseph M. Hellerstein, Concurrency and recovery in generalized search trees, Proceedings of ACM SIGMOD 1997 (SIGMOD Record 26(2))"
    locator: pp. 62 to 72, right links and node sequence numbers to detect concurrent splits, and logging of GiST operations
  - paper: doi:10.1145/602259.602266
    title: "Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984"
    locator: pp. 47 to 57, the least-enlargement rule for ChooseLeaf and the quadratic split, used here as Penalty and PickSplit of the R-tree instance
---

A generalized search tree (GiST) is a balanced tree of pages in which every key is a predicate: an index entry $(p, ptr)$ says that $p$ holds for every record below $ptr$. The tree code for search, insert and delete is written once. An index designer supplies six *key methods* that say what a predicate is, when it can match a query, how predicates combine, and how to split a full node. With interval predicates the tree behaves like a [B+ tree](/b-plus-tree/), and with bounding boxes it behaves like an [R-tree](/r-tree/); the GiST is the template that both are instances of.

## In plain words

Picture a set of boxes inside boxes. Each box has a label that is true of everything inside it, such as "numbers from 30 to 50" or "points inside this rectangle". To find things, you open only the boxes whose label could match your question. To put a thing away, you choose the box whose label has to change the least, and when a box gets too full, you split its contents into two boxes and write a new label on each.

A B+ tree and an R-tree both work like this. They differ only in what a label is, how two labels combine, how to measure "change the least", and how to split. A GiST lets you write just those four things, plus two more that pack a label into less space, and it does the rest.

## The abstract type

A GiST holds a set of records, each with a key from a domain chosen by the extension, and answers *queries* that are predicates over that domain.

- `search(T, q)`: every record whose key is consistent with $q$.
- `insert(T, key, rid)`: add a record.
- `delete(T, rid)`: remove a record.

The kinds of query depend on the extension: an overlap with a range for the B+ tree instance, an intersection with a rectangle for the R-tree instance, and containment of elements for the RD-tree instance of the paper, which indexes sets.

The six key methods, as in the paper, with $E = (p, ptr)$ an entry and $P$ a set of entries:

| method | what it does |
|---|---|
| Consistent$(E, q)$ | false only if $p \wedge q$ cannot hold; true otherwise, so false positives are allowed |
| Union$(P)$ | a predicate that holds for every record below any entry of $P$ |
| Compress$(E)$ | an entry with a shorter representation $p'$, where $p$ implies $p'$ |
| Decompress$(E)$ | the inverse of Compress, again possibly a weaker predicate |
| Penalty$(E_1, E_2)$ | the cost of putting $E_2$ below $E_1$, used to choose the subtree |
| PickSplit$(P)$ | split $M + 1$ entries into two sets of at least $m$ entries each |

## Representation

The tree has these properties, which are the tree properties of the paper:

1. Every node other than the root has between $m$ and $M$ entries, with $2 \le m \le (M + 1) / 2$. The root has at least two entries unless it is a leaf.
2. A leaf entry is $(p, rid)$, where $p$ holds for the key of the record $rid$ (exactly, or as a weaker predicate if Compress is lossy).
3. An index entry is $(p, ptr)$, where $p$ holds for every record reachable from $ptr$. The predicates of two entries in one node may overlap.
4. All leaves are at the same level.

Property 3 is weaker than the separator rule of a B+ tree: a key does not tell a search where a record is, only where it may be. This is what makes the template general, and it is also why a search may have to follow more than one path.

## Operations

```pseudo id=main
SEARCH(R, q)                        ▷ R is a node, q a query predicate
L1  if R is not a leaf then
L2      for each entry (p, ptr) of R do
L3          if CONSISTENT(DECOMPRESS(p), q) then SEARCH(ptr, q)
L4  else for each entry (p, rid) of R do
L5          if CONSISTENT(DECOMPRESS(p), q) then output rid

INSERT(T, E)                        ▷ E = (key, rid)
L6  L ← CHOOSE-SUBTREE(root of T, E)
L7  add (COMPRESS(key), rid) to L
L8  if L has more than M entries then SPLIT(L)
L9  ADJUST-KEYS from L up to the root

CHOOSE-SUBTREE(R, E)
L10 if R is a leaf then return R
L11 F ← the entry of R with the least PENALTY(F, E)
L12 return CHOOSE-SUBTREE(F.ptr, E)

SPLIT(N)                            ▷ N has M + 1 entries
L13 (P1, P2) ← PICKSPLIT(the entries of N)
L14 N keeps P1; a new node N' gets P2
L15 add (COMPRESS(UNION(P2)), N') to the parent of N; split the parent if it is now full
L16 set the key of N in its parent to COMPRESS(UNION(P1))

DELETE(T, rid)
L17 find the leaf that holds rid by a search with the key of rid; remove the entry
L18 for each node on the path with fewer than m entries: remove it and keep its records to reinsert
L19 ADJUST-KEYS on the path, then reinsert the kept records with INSERT
```

ADJUST-KEYS sets the key of each node on the path to COMPRESS(UNION) of the keys of its entries, which keeps property 3 and keeps the keys tight. If the root splits, a new root with two entries is made. If the root of an inner tree ends with one entry, its child becomes the root.

**Instances.** The code on this page has two extensions:

- *Intervals* (like a B+ tree): a key is an integer interval $[lo, hi]$, and a point $x$ is $[x, x]$. Consistent is "overlaps the query range", Union is the smallest covering interval, Penalty is the growth in length, and PickSplit sorts by $lo$ and cuts in half. Compress is the identity.
- *Rectangles* (like an R-tree): Consistent is "intersects", Union is the bounding box, Penalty is the growth in area with the area as a tie break (Guttman's rule), and PickSplit is Guttman's quadratic split. Compress can round each rectangle outward to a grid, which needs fewer bits and gives a weaker predicate.

For linearly ordered keys, the paper adds methods so that a range search can find the first match and then walk the leaves in order, as a B+ tree does, instead of calling Consistent on every node.

## Example

**Intervals.** Insert the points 50, 20, 80, 10, 30, 60, 90, 40, 70 with $M = 4$ and $m = 2$.

1. The first four fill the root leaf. The point 30 makes 5 entries, so PickSplit sorts them (10, 20, 30, 50, 80) and splits them into {10, 20} and {30, 50, 80}. The new root has the keys $[10, 20]$ and $[30, 80]$.
2. For 60, the penalties are $60 - 10 - 10 = 40$ for $[10, 20]$ and 0 for $[30, 80]$, so 60 goes right. For 90, the penalties are 70 and 10, and 90 also goes right. That leaf now has 30, 50, 60, 80, 90, and it splits into {30, 50} and {60, 80, 90}.
3. 40 goes into $[30, 50]$ with penalty 0, and 70 into $[60, 90]$.

The final root has the keys $[10, 20]$, $[30, 50]$ and $[60, 90]$, over the leaves {10, 20}, {30, 40, 50} and {60, 70, 80, 90}. The query "overlaps $[25, 45]$" calls Consistent on the three root keys, and only $[30, 50]$ passes. The search reads 2 nodes and returns 30 and 40.

**Rectangles.** Insert $a = (0,0,2,2)$, $b = (1,6,3,8)$, $c = (7,1,9,3)$, $d = (6,7,8,9)$, $e = (2,2,4,4)$ and $f = (8,8,9,9)$, written as $(x_1, y_1, x_2, y_2)$, with $M = 4$ and $m = 2$. The quadratic split of the first five takes the pair with the most wasted area as seeds, and the tree ends with the root keys $(0,0,4,8)$ over $a, b, e$ and $(6,1,9,9)$ over $c, d, f$. The query rectangle $(3,3,7,7)$ meets both root keys, which overlap it, so the search reads all 3 nodes and returns $b, c, d, e$. This is the price of property 3: overlapping keys can send a search down several paths.

**Lossy keys.** With rectangles rounded outward to multiples of 8, a test with 100 random rectangles and 40 small queries (seed 9) gives leaf matches that are not real matches. The search then checks each candidate against the stored record, as PostgreSQL does with its "recheck" step.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). The main points:

- **Search finds every match.** If a record $r$ matches $q$, then by property 3 every key on the path from the root to $r$ holds for $r$, so its conjunction with $q$ can hold and Consistent cannot return false. SEARCH follows that path. With a lossy Compress the leaf test can pass for records that do not match, so the result is a superset that a recheck makes exact.
- **Insert and delete keep the properties.** ADJUST-KEYS makes each key the Union of its child, which implies every key below it. PickSplit returns two sets of at least $m$ entries. Splits and reinsertion keep all leaves at one level, because a split adds a node at the same level and only a root split adds a level.
- **Termination.** Every call descends one level, and the height is finite.

## Complexity

Costs are in the page I/O model: one node is one page. In the [external memory model](/external-memory-model/), the memory holds M/B blocks; this page counts page reads only and does not use a buffer size. On this page, M and m count the entries in a node.

- **Height.** Every node other than the root has at least $m$ entries, so the height $h$ is at most $1 + \lceil \log_m (n / m) \rceil$, and $h = O(\log_m n)$.
- **Search.** If at most one entry per node is consistent with $q$, as with disjoint intervals and a point query, a search reads $h$ pages and makes $O(h M)$ Consistent calls. In the worst case every key overlaps $q$ and the search reads every node, $O(n / m)$ pages. How close a GiST gets to the good case depends on Penalty and PickSplit; this is a property of the extension, not a guarantee of the template.
- **Insert** reads $h$ pages to choose a leaf, with $M$ Penalty calls per level, and writes up to $h + 1$ pages for the splits and the key changes. The quadratic PickSplit costs $O(M^2)$ area computations per split.
- **Delete** costs one search, which can visit several paths, plus the reinsertion of the records of the removed nodes.

## Variants

- **Concurrency and recovery.** Kornacker, Mohan and Hellerstein (1997) add a right link to each node and a node sequence number, as in the [B-link tree](/blink-tree/), so that a search that reads a node during a split can detect the split and follow the right link. The keys of a GiST are not ordered, so the B-link rule of comparing with a high key does not work, and the sequence number replaces it.
- **RD-tree.** The paper's third instance indexes sets: a key is a set that contains all sets below it, and Compress can store it in a lossy form such as a signature.
- **Nearest neighbor search.** Later work runs a best-first search on the same tree with a distance bound per key, which gives [nearest neighbor](/nearest-neighbor-search/) queries for any extension that can bound a distance.
- **Space-partitioning trees.** A GiST keeps balance and lets keys overlap. SP-GiST, a related template, covers trees that split space without overlap, such as the [kd-tree](/kd-tree/) and the [quadtree](/quadtree/).

## When to use it

Use a GiST when a database must index a new kind of data (geometric shapes, ranges, sets, text signatures, network addresses) and the designer wants the system's existing page handling, concurrency and logging, not a new access method. PostgreSQL ships a GiST framework, and its range, geometric and full-text operator classes are GiST extensions. For plain ordered keys, a native B+ tree is simpler and faster, because it can use separators and in-order leaf scans.

## Pitfalls

- **A Consistent that is too strict.** Consistent may return true when the answer is "maybe", but never false when a match is possible. An exact-looking test on a lossy compressed key loses records.
- **A Union that is not a cover.** If Union does not imply the keys of all its entries, property 3 fails and searches miss records. This also holds after Decompress: Union must cover the decompressed keys.
- **No recheck with a lossy Compress.** The leaf test on a compressed key is only a filter. Without a recheck, the result has false positives.
- **A PickSplit that ignores the minimum fill.** Every split must leave at least $m$ entries on each side, or the height bound fails and deletes underflow at once.
- **A Penalty that ignores overlap.** If Penalty lets keys of one node overlap a lot, every search follows many paths and the tree degrades to a scan.

## Implementations

## History

Joseph Hellerstein, Jeffrey Naughton and Avi Pfeffer presented the GiST at VLDB 1995, based on the observation that the B+ tree, the R-tree and many other balanced trees of the time shared their search and update code. They gave the six key methods, the tree methods and three instances. Marcel Kornacker, C. Mohan and Hellerstein added concurrency control and recovery at SIGMOD 1997. The design was built into Postgres, and PostgreSQL still uses it for many of its non-B-tree indexes.

## References
