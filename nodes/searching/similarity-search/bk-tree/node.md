---
tag: WM7ED9
kind: data-structure
slug: bk-tree
name: BK-tree
aliases:
- Burkhard-Keller tree
area: searching/similarity-search
level: core
summary: A tree over a discrete metric such as edit distance, where children are keyed by their distance to the parent.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of stored items, h: the height of the tree, D: the largest distance between two items, E: the time of one distance evaluation}
  time: {insert: O(h E), range: O(n E), nearest: O(n E)}
  space: {total: O(n)}
history:
  year: 1973
  people: [Walter A. Burkhard, Robert M. Keller]
  note: Burkhard and Keller described trees keyed by the integer distance to a pivot for best-match file searching in Communications of the ACM in 1973.
prereqs: [metric-space, edit-distance, triangle-inequality]
see_also: [vantage-point-tree, gnat, ball-tree, metric-space-indexing, pivot-based-indexing, similarity-range-query, hamming-distance, cover-tree]
sources:
  - paper: doi:10.1145/362003.362025
    title: Walter A. Burkhard and Robert M. Keller, Some approaches to best-match file searching, Communications of the ACM 16(4), 1973
    locator: pages 230 to 236 (the tree whose subtrees are keyed by the discrete distance to a key element, and its search by the triangle inequality)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 5, the Burkhard-Keller tree and the fixed-queries trees among the indexes for discrete distance functions)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, Section 4.5 (distance-based indexing methods, including pivot-based trees for discrete distances)
---

A BK-tree (Burkhard-Keller tree) is a tree for a [metric space](/metric-space/) whose distance takes nonnegative integer values, such as the [edit distance](/edit-distance/) between words or the [Hamming distance](/hamming-distance/). Each node holds one item, and the child with key $i$ holds the items at distance exactly $i$ from it. A range query with radius $r$ visits only the children with keys from $d - r$ to $d + r$, where $d$ is the distance from the query to the node, because the [triangle inequality](/triangle-inequality/) rules out the others. The tree is small and simple and is the usual index for spelling correction, but its worst-case query time is a full scan of $n$ items. Burkhard and Keller described it in 1973.

## In plain words

Pick one word and make it the root. For each other word, measure how far it is from the root, and put it under a branch labeled with that number. Inside each branch, do the same again with the first word that arrived there.

To find all words within a small distance of a query word, measure the query against the root. A word under the branch labeled 5 is exactly 5 from the root. If the query is 2 from the root, a word under branch 5 is at least 3 from the query, so with a limit of 1 you can skip that whole branch. You keep only the branches whose labels are close to the query's own distance from the root.

## The abstract type

A BK-tree implements a [similarity index](/similarity-index/) over a set $S$ of items from a metric space $(M, \delta)$ with $\delta: M \times M \to \{0, 1, 2, \dots\}$: `insert(x)`, `range(q, r)`, which returns $\{x \in S : \delta(q, x) \le r\}$, and `nearest(q)`, which returns an item of $S$ at the least distance from $q$. The index only calls $\delta$; it never looks inside the items. Its cost is counted in distance evaluations, since one edit distance costs far more than the rest of the work.

## Representation

Each node $t$ holds an item $t.item$ and a map $t.child$ from integer keys to nodes. The tree stores each item of $S$ in exactly one node. Items at distance 0 from a stored item are equal to it in a metric, so they are not stored twice.

**Invariant (B).** For each node $t$ and each key $i$ of $t.child$, every item $x$ in the subtree of $t.child[i]$ has $\delta(x, t.item) = i$.

The keys of one node are distinct integers from 1 to $D$, the largest distance, so a node has at most $D$ children. For words of length at most $\ell$ under the edit distance, $D \le \ell$. Store $t.child$ as a small array or a [hash table](/hash-table/).

## Operations

```pseudo id=main
INSERT(T, x)
L1  if T.root = nil then T.root ← a new node with item x; return
L2  t ← T.root
L3  repeat: k ← δ(x, t.item)
L4      if k = 0 then return                      ▷ x is already stored
L5      if k is a key of t.child then t ← t.child[k] else (t.child[k] ← a new node with item x; return)

RANGE(t, q, r)                                    ▷ report each item x in the subtree of t with δ(q, x) ≤ r
L6  if t = nil then return
L7  k ← δ(q, t.item); if k ≤ r then report t.item
L8  for each key i of t.child with k − r ≤ i ≤ k + r do RANGE(t.child[i], q, r)
```

INSERT walks down from the root. At each node it computes the distance $k$ and moves into the child with key $k$, so the new item meets (B) at every node of its path; when the child does not exist, the item becomes a new leaf there. RANGE tests the item of each visited node and goes into the children whose keys lie in $[k - r, k + r]$.

**Nearest neighbor** search runs RANGE with a radius $\tau$ that shrinks to the best distance found so far. A stack entry carries a lower bound on the distance from $q$ to every item of its subtree.

```pseudo id=nearest
NEAREST(T, q)
L9  best ← nil; τ ← ∞; push (0, T.root) on a stack S
L10 while S is not empty: pop (b, t); if b ≥ τ then continue
L11     k ← δ(q, t.item); if k < τ then (best ← t.item; τ ← k)
L12     for each key i of t.child with |i − k| < τ do push (|i − k|, t.child[i])
L13 return (τ, best)
```

For the $k$ nearest items, keep the $k$ best in a max-heap and let $\tau$ be the largest distance in the heap once it has $k$ items. Deletion is not supported directly: an inner node fixes the keys of its whole subtree. The usual fix is to mark the item as deleted, skip it in reports, and rebuild when too many items are marked.

## Example

Insert the words book, books, cake, boo, boon, cook, cape and cart in this order, with the [edit distance](/edit-distance/). The root is book. books is at distance 1 from book and becomes child 1; cake is at distance 4 and becomes child 4. boo is at distance 1 from book, so it goes to books, where it is at distance 2 and becomes child 2 of books. boon goes book → books → boo and becomes child 1 of boo. cook goes the same way and becomes child 2 of boo. cape and cart go under cake with keys 1 and 2.

```
book
├─1─ books
│    └─2─ boo
│         ├─1─ boon
│         └─2─ cook
└─4─ cake
     ├─1─ cape
     └─2─ cart
```

Query: all words within $r = 1$ of bool.

| node | $\delta(\text{bool}, \cdot)$ | reported | keys visited |
|---|---|---|---|
| book | 1 | yes | $[0, 2]$: key 1; key 4 is skipped |
| books | 2 | no | $[1, 3]$: key 2 |
| boo | 1 | yes | $[0, 2]$: keys 1 and 2 |
| boon | 1 | yes | none |
| cook | 2 | no | none |

The answer is {book, boo, boon} after 5 distance evaluations, against 8 for a scan. The skip at the root is safe: each word under key 4 is at distance 4 from book, so at distance at least $4 - 1 = 3$ from bool. NEAREST for the query cast returns cart at distance 1.

## Correctness

**INSERT keeps (B).** The new item $x$ is placed in the subtree of $t.child[k]$ only when $k = \delta(x, t.item)$, at each node $t$ on its path. No other subtree changes.

**RANGE is exact.** Each reported item passed the test of line L7. Conversely let $x$ be in the subtree of $t.child[i]$ with $\delta(q, x) \le r$. By (B), $\delta(x, t.item) = i$. By the triangle inequality, $|\delta(q, t.item) - \delta(x, t.item)| \le \delta(q, x) \le r$, that is, $k - r \le i \le k + r$. So line L8 enters the subtree, and by induction on the depth the call reaches $x$ and reports it.

**NEAREST is exact.** By the same inequality, every item in the subtree of $t.child[i]$ is at distance at least $|i - k|$ from $q$, and these bounds only grow along a path, so the bound $b$ on a stack entry is a lower bound for its whole subtree. An entry is dropped only when $b \ge \tau$, so none of its items is closer than the current best. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/) with a distance oracle of cost $E$; for the edit distance on words of length at most $\ell$, $E = O(\ell^2)$.

- **Insert.** One distance per node on the path: $O(h E)$, where $h$ is the height, plus $O(1)$ expected per child lookup.
- **Height.** The height depends on the insertion order and on the metric. With the discrete metric, where all distances are 1, every item goes to child 1 of the previous one, and $h = n$. For words, $h$ is often small, since the keys spread over $1, \dots, D$.
- **Range and nearest.** At most one distance per node: $O(n E)$ in the worst case. This bound is reached: with the discrete metric and $r \ge 1$, every key is in $[k - r, k + r]$. In practice, for small $r$ relative to the spread of distances, a query visits a small fraction of the nodes, and the fraction grows fast with $r$.
- **Space.** One node and one map entry per item: $O(n)$.

| operation | distance evaluations | case |
|---|---|---|
| insert | $O(h)$ | worst; $h \le n$ |
| range$(q, r)$ | $O(n)$ | worst, reached by the discrete metric |
| nearest | $O(n)$ | worst |
| space | $O(n)$ nodes | total |

## Variants

- **Fixed-queries tree.** All nodes at one depth use the same pivot, so a query computes one distance per level and not per node. This trades extra space for far fewer distance evaluations.
- **Buckets.** A leaf may hold up to $b$ items that are scanned directly, which cuts the number of nodes and the work for small subtrees.
- **Continuous distances.** For real-valued distances, keys are intervals of distances; this leads to the [vantage-point tree](/vantage-point-tree/) with one split value, and to [GNAT](/gnat/) with several pivots per node.

## When to use it

Use a BK-tree for spelling suggestions, fuzzy lookup of names, and near-duplicate fingerprints under the Hamming distance, when the radius is small (1 or 2 edits) and the set fits in memory. It needs only a metric with integer values, it is short to write, and inserts are cheap. For large radii or high intrinsic dimension it degrades to a scan; then use [LSH](/locality-sensitive-hashing/) for Hamming codes, or an index for strings such as a trie with a bounded edit search. For vectors, use the [k-d tree](/kd-tree/) or a [ball tree](/ball-tree/).

## Pitfalls

- **Not a metric.** The pruning of line L8 needs the triangle inequality. Weighted edit distances with asymmetric costs, or $1 - $ cosine similarity, break it, and the tree then misses answers without warning.
- **Real-valued distances.** Keys must be exact. Rounding real distances to integers breaks (B); use a tree for real distances instead.
- **Large radius.** The range $[k - r, k + r]$ covers most keys when $r$ is close to the typical distance, and the query visits almost every node.
- **Sorted insertion order.** Inserting items in an order that makes each item far from all earlier ones, or all at one distance, gives a tall tree. Shuffle the items first.

## Implementations

## History

Burkhard and Keller presented three methods for best-match file searching in Communications of the ACM in 1973; the first is the tree that now bears their names, for distance functions with discrete values. Chávez, Navarro, Baeza-Yates and Marroquín placed it among the pivot-based metric indexes in their survey of 2001, together with the fixed-queries trees derived from it.

## References
