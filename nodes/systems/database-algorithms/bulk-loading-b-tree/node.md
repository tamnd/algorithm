---
tag: BKKK4M
kind: algorithm
slug: bulk-loading-b-tree
name: Bulk loading a B+ tree
aliases:
- bottom-up index build
- B+ tree bulk loading
- sorted bulk load of a B-tree index
area: systems/database-algorithms
level: advanced
summary: "Build a B+ tree from a set of entries by sorting them, packing them into leaves to a chosen fill factor, and building each index level from the level below. Each node is written once."
uses: [external-merge-sort, b-plus-tree]
model: external-memory-model
complexity:
  vars: {N: the number of entries, B: the number of entries in a disk block, M: the number of entries that fit in memory, n: the number of blocks N/B, m: the number of blocks M/B}
  time: {worst: "O(N log N)"}
  space: {extra: "Θ(N)"}
  io:
    worst: "O(n log_m n)"
properties: {deterministic: true, online: false}
prereqs: [b-plus-tree, external-merge-sort]
see_also: [bulk-loading, b-tree, log-structured-merge-tree, packed-memory-array, clustered-index, buffer-tree, b-epsilon-tree]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 10, Section 10.8.2 (bulk-loading a B+ tree, p. 360), and Chapter 13 (external sorting)
  - paper: doi:10.1561/1900000028
    title: "Goetz Graefe, Modern B-tree techniques, Foundations and Trends in Databases 3(4) (2011)"
    locator: the sections on index creation by sorting and on the fill factor of new nodes
  - paper: doi:10.1007/BF00289075
    title: "Andrew Chi-Chih Yao, On random 2-3 trees, Acta Informatica 9(2) (1978)"
    locator: pp. 159 to 170, the expected storage use of B-trees under random insertions, about ln 2
  - paper: doi:10.1145/48529.48535
    title: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988)"
    locator: the sorting bound Θ((N/B) log_(M/B) (N/B)) in the two-level memory model
---

Bulk loading builds a [B+ tree](/b-plus-tree/) for a large set of entries in one go: it sorts the entries, cuts the sorted run into leaves filled to a chosen fill factor, links the leaves, and then builds each level of the index from the level below until one root remains. Each node is written exactly once, so the I/O cost is the cost of the sort plus one linear pass. The usual alternative, $N$ separate insertions, reads a root-to-leaf path for each entry, costs $\Theta(N \log_B N)$ I/Os on random keys, and leaves the nodes only about 69% full.

## In plain words

Suppose you must make the index of a thick book from a big pile of cards, one card for each entry. One way is to file the cards one at a time into a growing card box, which means a search for the right place each time, and boxes that must be split when they get full.

The fast way is to sort the whole pile first. Then you fill the boxes from the left, each to the same level, and put the boxes in a row. For each group of boxes, you write one label card that says which entries start each box. Then you do the same with the label cards, and so on, until one card at the top points to everything. You touch each box once, and you choose how full each box is.

## The problem

The input is a set $E$ of $N$ entries $(k, v)$ with distinct keys, and an order $d \ge 1$. The output is a B+ tree of order $d$ that holds exactly $E$:

- all leaves are at the same depth, and the leaves, read from left to right through their links, hold the keys in increasing order;
- an internal node with separators $s_1 < \cdots < s_j$ has children $c_0, \ldots, c_j$, and every key in $c_i$ lies in $[s_i, s_{i+1})$, with $s_0 = -\infty$ and $s_{j+1} = +\infty$;
- every node other than the root holds between $d$ and $2d$ keys (a leaf $d$ to $2d$ entries, an internal node $d$ to $2d$ separators, so $d + 1$ to $2d + 1$ children); a leaf root holds 1 to $2d$ entries, and an internal root has 2 to $2d + 1$ children.

A *fill factor* $f \in (0, 1]$ says how full the new nodes should be. A fill factor below 1 leaves room for later insertions, so that the first insertions do not split every node.

## The algorithm

```pseudo id=main
BULK-LOAD(E, d, f)
L1  sort E by key                              ▷ an external merge sort when E is large
L2  t ← ⌊f · 2d⌋ clamped to [d, 2d]            ▷ entries per leaf
L3  level ← leaves made from PACK(E, t, d, 2d), linked left to right
L4  if level is empty then return the empty tree
L5  u ← ⌊f · (2d + 1)⌋ clamped to [d + 1, 2d + 1]   ▷ children per internal node
L6  while |level| > 1 do
L7      for each group g of PACK(level, u, d + 1, 2d + 1) do
L8          make a node with children g and separators low(g[1]), ..., low(g[|g| − 1])
        level ← the new nodes, in order
L9  return the tree with root level[0]

PACK(S, t, lo, hi)                             ▷ lo ≤ t ≤ hi
L10 G ← the groups S[0..t−1], S[t..2t−1], ...; the last one may be shorter
L11 if G has at least two groups and the last has fewer than lo items then
L12     m ← the last two groups joined; remove them from G
L13     if |m| ≤ hi then append m to G
L14     else append the first ⌊|m|/2⌋ items of m and then the rest as two groups
L15 return G
```

Here $\mathrm{low}(c)$ is the smallest key in the subtree of $c$; each node stores it when it is made, so line L8 needs no search. PACK makes groups of exactly $t$ items, and repairs a short last group by joining it with the group before it, and by splitting the join into two halves if it is too big. Lines L6 to L8 repeat until one node is left, which becomes the root.

The input to line L3 is a sequential read of the sorted run, and each new node is written once and never read again during the build. Only the node being filled at each level needs to be in memory, so the build pass needs one block of memory per level.

## Example

Take the 20 keys $3, 6, 9, \ldots, 60$ in any order, with $d = 2$ (2 to 4 keys per node) and $f = 3/4$. Then $t = \lfloor 3/4 \cdot 4 \rfloor = 3$ entries per leaf and $u = \lfloor 3/4 \cdot 5 \rfloor = 3$ children per internal node.

| step | groups | result |
|---|---|---|
| L1 | | 3 6 9 12 ... 57 60 |
| L3 | PACK into groups of 3: six groups of 3 and one of 2; $2 \ge d$, so no repair | leaves [3 6 9] [12 15 18] [21 24 27] [30 33 36] [39 42 45] [48 51 54] [57 60] |
| L7 | 7 leaves in groups of 3: 3, 3, 1; the last group has $1 < d + 1 = 3$ children, so it joins the one before: $3 + 1 = 4 \le 5$ | two nodes with 3 and 4 children |
| L8 | separators are the low keys of all children but the first | [12, 21] and [39, 48, 57] |
| L7, L8 | 2 nodes, one group | root with separator [30] |

The tree has height 3 and 10 nodes. Every leaf but the last holds 3 entries, so each can take one insertion without a split.

The same 20 keys, inserted one at a time in increasing order into an empty tree of order 2, give 9 leaves: eight with 2 entries and one with 4. Each split of a full leaf leaves the left half with $d$ entries, and in sorted order no entry ever goes into a left half again. The 20 insertions touch 54 nodes in all.

**A larger run.** For 5,000 distinct random keys (`random.Random(3)`) with $d = 8$, so 16 entries per full leaf, bulk loading with $f = 1$ makes 313 leaves, 19 nodes above them and a root: 335 nodes, each written once. Inserting the same keys one by one in their random order gives 449 leaves (69.6% full), and the insertions touch 17,949 nodes. Inserting them in sorted order gives 624 leaves (50% full) and touches 19,241 nodes.

## Correctness

The leaves hold the sorted entries in order, so the leaf chain is in key order. Each level is built from the full list of nodes of the level below, so every leaf is at the same depth. The separator $\mathrm{low}(g_i)$ for child $g_i$ is a lower bound of its subtree and an upper bound (exclusive) for the subtree of $g_{i-1}$, since the subtrees cover consecutive ranges of the sorted keys. The fill bounds come from PACK: every group has between $lo$ and $hi$ items, except a single group, which then becomes the root. The full proof is below.

## Complexity

Let $L$ be the number of leaves, so $L = \lceil N / t \rceil$ or one less after the repair.

- **Nodes written.** Each internal node other than the root has at least $d + 1$ children and the root has at least 2. Every node but the root is a child of one node, so with $I$ internal nodes, $I + L - 1 \ge (d + 1)(I - 1) + 2$, which gives $I \le (L + d - 2) / d$. The build writes $L + I$ nodes, which is $L (1 + O(1/d))$, and reads the sorted run once.
- **I/O.** In the [external memory model](/external-memory-model/) with blocks of $B$ entries, a node of order $d$ fills one block, so $d = \Theta(B)$ and $L = \Theta(N / B)$. The [external merge sort](/external-merge-sort/) takes $O((N/B) \log_{M/B} (N/B))$ I/Os, and the build pass adds $O(N/B)$. So bulk loading takes $O(n \log_m n)$ I/Os with $n = N/B$ and $m = M/B$, the cost of sorting. When the entries arrive already sorted, for example from a table that is already in key order, the cost is $O(n)$.
- **Against repeated insertion.** One insertion reads the path from the root to a leaf, $\Theta(\log_B N)$ nodes, and writes at least one. With random keys and a tree much larger than memory, most of these reads are I/Os, so $N$ insertions take $\Theta(N \log_B N)$ I/Os. Sorting is cheaper by a factor of about $B \log_B N / \log_{M/B} (N/B)$, which is large for any real block size.
- **Fill.** Bulk loading fills the leaves to the chosen $f$, except the last one or two. Random insertions give an expected fill near $\ln 2 \approx 69\%$, a result of Yao (1978) for 2-3 trees that carries over to B-trees. Insertions in sorted order with plain splits give 50%.
- **CPU.** The sort takes $O(N \log N)$ comparisons, and the build $O(N)$ steps.

## Properties

- **Deterministic and offline.** It needs the whole set of entries before it starts.
- **Sequential I/O.** The input is read in order and nodes are written in order, level by level. With a layout that puts the leaves of one level in consecutive blocks, a later range scan reads the leaves sequentially too.
- **Chosen fill factor.** A full tree ($f = 1$) is the smallest and fastest to search, and suits read-only data; a lower $f$ leaves room for growth.
- **A normal B+ tree as output.** The result accepts normal inserts and deletes afterwards. Only the build is special.

## Variants and improvements

- **Rightmost path insertion.** Ramakrishnan and Gehrke build the tree from the sorted entries by always inserting into the rightmost leaf and splitting only along the rightmost path. The cost is the same order; the nodes left of the path are never touched again.
- **Merge into an existing tree.** To add a large sorted batch to a tree, merge the batch with the leaf level and rebuild the index levels, or insert the batch leaf by leaf in key order. [LSM trees](/log-structured-merge-tree/) and [buffer trees](/buffer-tree/) turn every update stream into such batch merges.
- **Bulk loading of spatial trees.** For R-trees the key has no single order. Methods such as sort-tile-recursive or Hilbert ordering first impose an order, then pack as here. See [bulk loading](/bulk-loading/) of spatial indexes; this page is the one-dimensional case, where sorting gives the order directly.
- **A plain B-tree.** In a [B-tree](/b-tree/) whose internal nodes hold entries too, the build is the same, except that one entry between two groups moves up to the parent as the separator, instead of a copy of the low key.
- **Gaps in one array.** A [packed memory array](/packed-memory-array/) keeps all entries in one sorted array with spread-out gaps and rebalances windows of it on insert. A bulk load with $f < 1$ leaves gaps too, but inside separate nodes, and the tree, not a rebalancing rule, finds the place of a key.
- **Index build in parallel.** Each processor sorts a range of keys and builds the subtree of that range; the top levels are then built from the subtree roots.

## When to use it

Use bulk loading to create an index on an existing table (`CREATE INDEX`), to load a data warehouse, to rebuild a fragmented index, or after a large batch import. Most database systems create a new B+ tree index this way. Use plain insertion for a stream of single updates, and an [LSM tree](/log-structured-merge-tree/) or a [B^ε tree](/b-epsilon-tree/) when updates arrive in a high-rate stream.

## Pitfalls

- **An underfull last node.** Cutting the run into groups of $t$ leaves a last group that can be shorter than $d$. Without the repair of lines L11 to L14 the tree breaks the fill bound, and later deletions can underflow in ways the delete code does not expect.
- **Separators from the wrong key.** Line L8 must use the smallest key of the whole subtree of each child, not the first separator of that child. For a leaf child the two are the same; for an internal child they are not.
- **Fill factor 1 on a table that will grow.** A full tree splits a node at the first insertion into it, so a burst of inserts after the load splits almost every leaf. Choose $f < 1$ when updates follow.
- **Duplicate keys.** The page assumes distinct keys. With duplicates, a separator equal to keys on both sides of a boundary sends a search to the wrong child. Make keys unique by adding the row id, or use a search that goes to the leftmost child holding the key.
- **Sorting in memory.** Calling an in-memory sort on a run that does not fit in memory thrashes the buffer. Line L1 must be an external sort for large inputs.

## Implementations

## History

Bulk loading by sorting and packing is part of the database practice described in textbooks such as Ramakrishnan and Gehrke (Section 10.8.2) and in Graefe's survey of B-tree techniques. The cost comparison rests on the sorting bound of Aggarwal and Vitter (1988) and, for the fill factor of trees built by insertion, on Yao's analysis of random 2-3 trees (1978).

## References
