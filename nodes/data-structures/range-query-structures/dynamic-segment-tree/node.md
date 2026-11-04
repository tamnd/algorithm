---
tag: 6P1XHV
kind: data-structure
slug: dynamic-segment-tree
name: Dynamic (sparse) segment tree
aliases:
- Dynamic (sparse) Segment Tree
- sparse segment tree
- implicit segment tree
area: data-structures/range-query-structures
level: core
summary: A segment tree that creates nodes only when needed, supporting queries over huge index ranges with memory proportional to the updates.
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {U: the size of the index range, m: the number of updates}
  time: {worst: O(log U)}
  space: {extra: "O(min(m log U, U))"}
prereqs: [segment-tree, monoid]
see_also: [persistent-segment-tree, lazy-propagation, coordinate-compression, fenwick-tree, li-chao-tree, point-update-range-sum-query, trie, range-update-range-query]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 28, Segment trees revisited, Section 28.2 Dynamic trees (dynamic structure, sparse segment tree, persistent segment tree)
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the section Dynamic segment tree, the last section before Practice Problems
  - url: https://usaco.guide/plat/sparse-segtree
    title: USACO Guide, Platinum, Sparse Segment Trees
    locator: the whole module (dynamic creation of nodes, and the comparison with coordinate compression)
---

A dynamic segment tree is a [segment tree](/segment-tree/) over a large index range $[0, U)$ that stores a node only after an update has touched its range. A node that does not exist stands for a range of identity values, such as zeros for sums. Each update and each range query takes $O(\log U)$ time, and after $m$ updates the tree has at most $m \lceil \lg U \rceil + 1$ nodes, so $U$ can be $10^9$ or $2^{63}$ while the memory follows the number of updates. It is the online answer to the problem that [coordinate compression](/coordinate-compression/) solves offline.

## In plain words

An ordinary segment tree over a billion positions needs about two billion boxes before it starts. Most of them would hold zero forever, because only a few positions ever change.

A dynamic segment tree builds the boxes only when it needs them. It starts with one box for the whole range. When a change arrives at a position, it walks down from the top towards that position and makes each missing box on the way. A box that was never made counts as zero. A question about a range walks down the same way, but it never makes boxes; it stops at a missing box and uses zero for it.

## The abstract type

The structure keeps an array $A[0 \ldots U-1]$ over a [monoid](/monoid/) $(M, \oplus, e)$, with all items equal to $e$ at the start. The operations are:

- $\textsc{update}(i, x)$: set $A[i] \leftarrow A[i] \oplus x$, for $0 \le i < U$; with a commutative monoid such as integer addition this is the point add of the [point update range sum query](/point-update-range-sum-query/);
- $\textsc{query}(l, r)$: return $A[l] \oplus A[l+1] \oplus \cdots \oplus A[r-1]$ for $0 \le l \le r \le U$, or $e$ when $l = r$.

The point assignment $A[i] \leftarrow x$ works the same way, with the leaf set to $x$ and the inner nodes recomputed on the way up.

## Representation

The nodes are records in three growing arrays: $\mathit{val}[v]$, $\mathit{left}[v]$ and $\mathit{right}[v]$, where a child of 0 means "absent" and node 1 is the root. A node $v$ that covers the range $[lo, hi)$ with $hi - lo \ge 2$ has its children over $[lo, mid)$ and $[mid, hi)$ with $mid = \lfloor (lo + hi) / 2 \rfloor$. The ranges are not stored; they are computed on the way down from $[0, U)$. The invariant is:

> **(D)** For each node $v$ over $[lo, hi)$, $\mathit{val}[v] = A[lo] \oplus \cdots \oplus A[hi - 1]$, and for each range $[lo, hi)$ of the full segment tree whose node is absent, $A[lo] = \cdots = A[hi-1] = e$.

## Operations

```pseudo id=main
UPDATE(i, x)                               ▷ A[i] ← A[i] ⊕ x, for 0 ≤ i < U
L1  v ← 1, lo ← 0, hi ← U
L2  loop
L3      val[v] ← val[v] ⊕ x                 ▷ for a commutative ⊕; else recompute on the way up
L4      if hi − lo = 1 then return
L5      mid ← ⌊(lo + hi) / 2⌋
L6      if i < mid then
L7          if left[v] = 0 then left[v] ← NEWNODE()
L8          v ← left[v], hi ← mid
L9      else
L10         if right[v] = 0 then right[v] ← NEWNODE()
L11         v ← right[v], lo ← mid
```

NEWNODE appends a record with $\mathit{val} = e$ and no children, and returns its index. The query is the query of the plain segment tree, with one more case for an absent node:

```pseudo id=query
QUERY(v, lo, hi, l, r)                     ▷ the call is QUERY(1, 0, U, l, r)
L12 if v = 0 or r ≤ lo or hi ≤ l then return e      ▷ absent node, or no overlap
L13 if l ≤ lo and hi ≤ r then return val[v]
L14 mid ← ⌊(lo + hi) / 2⌋
L15 return QUERY(left[v], lo, mid, l, r) ⊕ QUERY(right[v], mid, hi, l, r)
```

A query never creates nodes, so a read-only workload does not grow the tree. The recursion depth is $\lceil \lg U \rceil + 1$, which is 65 for $U = 2^{64}$, so a recursive query is safe, and an explicit stack works as well.

## Example

Take $U = 16$, integer addition, and the updates $\textsc{update}(3, 5)$, $\textsc{update}(10, 2)$ and $\textsc{update}(11, 4)$.

| operation | new nodes (by range) | nodes in total |
|---|---|---|
| start | the root $[0, 16)$ | 1 |
| $\textsc{update}(3, 5)$ | $[0, 8)$, $[0, 4)$, $[2, 4)$, $[3, 4)$ | 5 |
| $\textsc{update}(10, 2)$ | $[8, 16)$, $[8, 12)$, $[10, 12)$, $[10, 11)$ | 9 |
| $\textsc{update}(11, 4)$ | $[11, 12)$ | 10 |

The stored values are $\mathit{val} = 11$ at the root, 5 on the path to position 3, $6$ at $[8, 16)$, $[8, 12)$ and $[10, 12)$, 2 at $[10, 11)$ and 4 at $[11, 12)$. The full tree would have 31 nodes.

$\textsc{query}(2, 12)$ visits the root, then $[0, 8)$: its left child $[0, 4)$ splits into $[0, 2)$, which is absent and gives 0, and $[2, 4)$, which lies inside the query and gives 5; its right child $[4, 8)$ is absent and gives 0. On the right side, $[8, 16)$ splits into $[8, 12)$, which lies inside and gives 6, and $[12, 16)$, which is absent. The answer is $5 + 6 = 11$. $\textsc{query}(0, 8) = 5$, and $\textsc{query}(4, 10) = 0$, which ends at absent nodes and at the absent left child $[8, 10)$ of $[8, 12)$.

## Correctness

UPDATE keeps (D). It walks the path from the root to the leaf $[i, i+1)$, creating each missing node on it. A new node covers a range that was absent, so by (D) all its items were $e$ and $\mathit{val} = e$ is right. Line L3 adds $x$ to every node whose range contains $i$, and these are exactly the nodes of the path; with a commutative $\oplus$, $(a_1 \oplus \cdots \oplus a_k) \oplus x$ equals the product with $a_i \oplus x$ in place of $a_i$. Nodes off the path are unchanged and so are their ranges. Absent ranges off the path still hold only $e$.

QUERY returns $A[\max(l, lo)] \oplus \cdots \oplus A[\min(r, hi) - 1]$ for the node over $[lo, hi)$, by induction on $hi - lo$: an absent node gives $e$, which is right by (D); a node inside the query gives $\mathit{val}[v]$, which is right by (D); and otherwise the two halves give the two parts of the overlap, in order, by the induction hypothesis. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

UPDATE makes one pass of the loop per level, and the tree over $[0, U)$ has $\lceil \lg U \rceil + 1$ levels, so it takes $O(\log U)$ time and creates at most $\lceil \lg U \rceil$ nodes. QUERY visits at most four nodes per level, as in the plain segment tree: at each level, at most two visited nodes are partly covered by the query, and only those have visited children. So it takes $O(\log U)$ time. After $m$ updates the tree has at most $\min(1 + m \lceil \lg U \rceil, 2U - 1)$ nodes. For $U = 10^9$ and $m = 10^5$, that is at most $3 \cdot 10^6 + 1$ nodes, against $2 \cdot 10^9$ for the full tree.

The cost per node is three words instead of one in an array segment tree, and the walk follows pointers rather than index arithmetic, which is slower in practice by a constant factor.

## Variants

- **With lazy propagation.** Range updates with [lazy propagation](/lazy-propagation/) work the same way: PUSH creates both children of a node before it moves the tag down. A range update creates $O(\log U)$ nodes.
- **Persistent.** Copy each node on the update path instead of changing it, and keep the old roots; this is the [persistent segment tree](/persistent-segment-tree/), and it has the same shape.
- **Li Chao tree on a huge range.** A [Li Chao tree](/li-chao-tree/) over integer abscissas up to $10^9$ is often built as a dynamic segment tree.
- **Binary trie.** A dynamic segment tree over $[0, 2^w)$ with the midpoint split is a binary [trie](/trie/) of the $w$-bit keys, with an aggregate at each node.
- **Merging.** Two dynamic segment trees over the same range can be merged by walking both at once and keeping one node when the other is absent. A sequence of merges of trees with $m$ leaves in total takes $O(m \log U)$ time, because each step of the merge removes a node.
- **Preallocation.** When an upper bound on $m$ is known, the three arrays are allocated once with $1 + m \lceil \lg U \rceil$ records, which avoids growing them.

## When to use it

Use a dynamic segment tree when the index range is too large for an array and the positions are not known in advance, for example when they arrive online or depend on earlier answers. When all positions are known first, [coordinate compression](/coordinate-compression/) followed by a plain segment tree or a [Fenwick tree](/fenwick-tree/) is faster and uses less memory. When the range is small, say $U \le 10^7$, an array segment tree is simpler. For range sums with point updates on keys that only need an order, a [balanced search tree](/balanced-binary-search-tree/) with subtree sums is another option.

## Pitfalls

- **Creating nodes in queries.** A QUERY that creates the children it visits turns every query into $O(\log U)$ new nodes, and the memory grows with the queries.
- **Overflow of the midpoint.** In languages with fixed-size integers, $(lo + hi) / 2$ can overflow for $U$ near the largest value; use $lo + (hi - lo) / 2$.
- **The size of the pool.** The bound is $m \lceil \lg U \rceil + 1$ nodes, not $2m$ or $4m$. With range updates and lazy tags it is about four times that.
- **Negative indices.** The range must be $[0, U)$, or the midpoint must round down, also for negative numbers. Shift the indices by a constant if they can be negative.
- **Non-commutative monoids.** Line L3 updates the nodes on the way down, which needs $(\cdots) \oplus x$ to commute with the order of the items. For a non-commutative monoid, or for assignment, record the path and recompute $\mathit{val}[v] = \mathit{val}[\mathit{left}[v]] \oplus \mathit{val}[\mathit{right}[v]]$ on the way up.

## Implementations

## History

Segment trees over a fixed set of endpoints are due to Bentley in the 1970s. Building the nodes on demand is a standard idea of pointer-based trees, and it appears without a named inventor in the teaching material of competitive programming, such as Laaksonen's handbook and the cp-algorithms page, under the names dynamic, sparse or implicit segment tree.

## References
