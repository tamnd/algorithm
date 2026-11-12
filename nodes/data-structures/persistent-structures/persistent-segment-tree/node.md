---
tag: KB52KZ
kind: data-structure
slug: persistent-segment-tree
name: Persistent segment tree
aliases:
- versioned segment tree
- persistent range tree
- chairman tree
area: data-structures/persistent-structures
level: advanced
summary: A segment tree that stores each update as O(log n) new nodes, so queries on any past version run in O(log n).
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {n: the number of positions, u: the number of updates done, k: the rank asked for}
  time: {build: Θ(n), update: Θ(log n), add: Θ(log n), get: Θ(log n), query: Θ(log n), kth: Θ(log n)}
  space: {total: Θ(n + u log n)}
history:
  year: 1989
  people: [James R. Driscoll, Neil Sarnak, Daniel D. Sleator, Robert E. Tarjan]
  note: Path copying for linked structures was described in the general study of persistence; the segment-tree form with versions over prefixes became a standard tool of competitive programming for range order statistics.
prereqs: [segment-tree, path-copying, persistent-data-structure]
see_also: [range-kth-smallest-query, wavelet-tree, merge-sort-tree, dynamic-segment-tree, lazy-propagation, persistent-binary-search-tree, version-tree, structural-sharing]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the section Persistent Segment Tree, and its use to find the k-th smallest number in a range
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the path copying method for linked data structures
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures (path copying)
---

A persistent segment tree is a [segment tree](/segment-tree/) in which an update does not change any node but copies the nodes on the path from the root to the changed leaf, and makes a new root for the new version. The path has at most $\lceil \lg n \rceil + 1$ nodes, exactly $\lg n + 1$ when $n$ is a power of two, so each update takes $\Theta(\log n)$ time and space, and all other nodes are shared with the old version. Every version keeps its own root, so a range query can run on any past version in $\Theta(\log n)$ time, and any version can be updated again, which makes the structure fully persistent. Its best-known use builds one version per prefix of an array and answers [range k-th smallest queries](/range-kth-smallest-query/) by walking two versions at once.

## In plain words

A segment tree keeps an array and the sum of every block of the array, arranged as a tree: the root has the sum of everything, its two children have the sums of the two halves, and so on down to single cells.

When you change one cell, only the blocks that contain that cell change. There is one such block on each level, so only a few nodes change. Instead of changing them, make new copies with the new sums, and let each copy point to the old nodes for the parts that did not change. The new root now describes the new array, and the old root still describes the old one. Keep a list of roots, and you can ask about any past array.

## The abstract type

The structure keeps a sequence of versions of an array $a[0..n)$ of values from a monoid, here the integers with $+$. Version 0 is the array given to `build`. The operations are:

- `update(v, i, x)`: make a new version equal to version $v$ with $a[i] = x$, and return its number;
- `add(v, i, d)`: make a new version equal to version $v$ with $a[i]$ increased by $d$;
- `get(v, i)`: return $a[i]$ in version $v$;
- `query(v, l, r)`: return $a[l] + \cdots + a[r - 1]$ in version $v$;
- `kth(u, v, k)`: for count arrays with $a_v - a_u \ge 0$ at each position, return the least position $p$ with $\sum_{j \le p} (a_v[j] - a_u[j]) \ge k$.

Any version can be the argument of any operation, so this is [full persistence](/full-persistence/) of a [range query structure](/range-query-structure/).

## Representation

All nodes live in one pool, and a node is never changed after it is made. A node $t$ covers a range $[lo, hi)$ of positions and has three fields: $t.left$ and $t.right$, which cover $[lo, mid)$ and $[mid, hi)$ with $mid = \lfloor (lo + hi)/2 \rfloor$, and $t.sum$. A node with $hi - lo = 1$ is a leaf and has no children. The range of a node is not stored: it is known from the path by which the node is reached. A table $roots$ maps each version number to its root node.

**Invariant.** (I1) No field changes after a node is made. (I2) For each version $v$, the node reached from $roots[v]$ for the range $[lo, hi)$ is a leaf iff $hi - lo = 1$, and an inner node has $t.sum = t.left.sum + t.right.sum$. (I3) The children of a node were made before it. A node may be reached from many versions, and always for the same range, because a child is put only into a parent that covers the same split.

## Operations

```pseudo id=main
BUILD(a, lo, hi)                              ▷ root of a tree for a[lo..hi)
L1  if hi − lo = 1 then return NEW-NODE(nil, nil, a[lo])
L2  mid ← ⌊(lo + hi) / 2⌋
L3  l ← BUILD(a, lo, mid); r ← BUILD(a, mid, hi)
L4  return NEW-NODE(l, r, l.sum + r.sum)

UPDATE(t, lo, hi, i, x)                       ▷ root of a copy of t with a[i] = x
L5  if hi − lo = 1 then return NEW-NODE(nil, nil, x)
L6  mid ← ⌊(lo + hi) / 2⌋
L7  if i < mid then l ← UPDATE(t.left, lo, mid, i, x); r ← t.right      ▷ share t.right
L8  else l ← t.left; r ← UPDATE(t.right, mid, hi, i, x)                ▷ share t.left
L9  return NEW-NODE(l, r, l.sum + r.sum)

QUERY(t, lo, hi, l, r)                        ▷ sum of a[l..r) in the tree t
L10 if r ≤ lo or hi ≤ l then return 0
L11 if l ≤ lo and hi ≤ r then return t.sum
L12 mid ← ⌊(lo + hi) / 2⌋
L13 return QUERY(t.left, lo, mid, l, r) + QUERY(t.right, mid, hi, l, r)
```

The version table is kept outside the tree: `build` sets $roots[0] \gets \text{BUILD}(a, 0, n)$; `update(v, i, x)` appends $\text{UPDATE}(roots[v], 0, n, i, x)$ to $roots$ and returns its index; `query(v, l, r)` returns $\text{QUERY}(roots[v], 0, n, l, r)$. `add(v, i, d)` is `update(v, i, get(v, i) + d)`, and `get` walks down one path. The recursion depth of each procedure is $\lceil \lg n \rceil$.

**The k-th unit between two versions.** Let version $v$ be made from version $u$ by `add` steps with positive $d$ only. Then $a_v[j] - a_u[j] \ge 0$ for each $j$, and the difference of the sums of two nodes reached by the same path in $u$ and $v$ is the total of the difference over that range. So one walk down both trees finds the k-th unit, like a search in an [order-statistic tree](/order-statistic-tree/).

```pseudo id=kth
KTH(u, v, k)                                  ▷ u and v are roots; 1 ≤ k ≤ v.sum − u.sum
K1  if k < 1 or k > v.sum − u.sum then error "k out of range"
K2  lo ← 0; hi ← n; while hi − lo > 1 do
K3      c ← v.left.sum − u.left.sum
K4      if k ≤ c then u ← u.left; v ← v.left; hi ← mid
K5      else k ← k − c; u ← u.right; v ← v.right; lo ← mid
K6  return lo
```

**Range k-th smallest.** Given an array $b[0..m)$ of values in $[0, n)$ (after [coordinate compression](/coordinate-compression/)), build version 0 as $n$ zeros and make version $j + 1$ by `add(j, b[j], 1)`. Version $j$ then counts the values of $b[0..j)$, and the difference between version $r$ and version $l$ counts the values of $b[l..r)$. So the k-th smallest value of $b[l..r)$ is $\text{KTH}(roots[l], roots[r], k)$, and the count of values below $y$ in $b[l..r)$ is $\text{query}(r, 0, y) - \text{query}(l, 0, y)$.

## Example

Let $a = [5, 3, 7, 1]$. BUILD makes 7 nodes: four leaves, the node of $[0, 2)$ with sum 8, the node of $[2, 4)$ with sum 8, and the root with sum 16.

- `update(0, 2, 10)` makes version 1. It makes a new leaf with 10, a new node for $[2, 4)$ with sum $10 + 1 = 11$, and a new root with sum $8 + 11 = 19$: 3 new nodes. The new root points to the old node of $[0, 2)$, and the new node of $[2, 4)$ points to the old leaf with 1.
- `update(0, 0, 0)` makes version 2 from version 0, not from version 1. It makes a leaf with 0, a node of $[0, 2)$ with sum 3, and a root with sum 11. The pool now has 13 nodes.
- `query(1, 1, 3)` returns $3 + 10 = 13$, `query(0, 1, 3)` returns $3 + 7 = 10$, and `query(2, 0, 2)` returns 3. The array of version 0 is still $[5, 3, 7, 1]$.

**k-th smallest.** Let $b = [3, 1, 2, 3, 0]$ and $n = 4$. The prefix versions are 0 to 5. For the range $b[1..4) = [1, 2, 3]$, KTH on the roots of versions 1 and 4 with $k = 2$ starts at the root: the left halves count the values 0 and 1, and $c = (0 + 1) - (0 + 0) = 1$ (version 4 has seen $3, 1, 2, 3$, and version 1 has seen $3$). Since $k = 2 > 1$, the walk goes right with $k = 1$. In the node of $[2, 4)$, the left child counts the value 2, and $c = 1 - 0 = 1$, so the walk goes left and returns 2, which is the second smallest of $[1, 2, 3]$.

## Correctness

Write $\text{val}(t, lo, hi)$ for the array that the tree $t$ stores on $[lo, hi)$: the sequence of leaf sums reached for the ranges $[j, j + 1)$. By induction on $hi - lo$, BUILD returns a tree with $\text{val} = a[lo..hi)$ that meets (I2). For UPDATE, the case $hi - lo = 1$ is clear. Otherwise, if $i < mid$, the left subtree is by induction a copy of $t.left$ with $a[i] = x$, and the right subtree is $t.right$ itself, which stores $a[mid..hi)$ unchanged; the new sum is the sum of the two, so (I2) holds. The other case is the same. UPDATE only makes nodes, so by (I1) every node reachable from an old root is unchanged, and so is the array of every old version. QUERY is the usual segment tree query and returns the sum over $[lo, hi) \cap [l, r)$ by induction. For KTH, the invariant is that $k$ is at most the difference of the sums at the current pair of nodes, and the answer lies in the current range; each step keeps it. The full proof is in the proofs folder.

## Complexity

| operation | time | new nodes |
|---|---|---|
| build | $\Theta(n)$ | $2n - 1$ |
| update, add | $\Theta(\log n)$ | at most $\lceil \lg n \rceil + 1$ |
| get | $\Theta(\log n)$ | none |
| query | $\Theta(\log n)$ | none |
| kth | $\Theta(\log n)$ | none |

**Time.** UPDATE visits one node per level. QUERY visits at most four nodes per level, as in the ephemeral segment tree. All bounds are worst case and hold on every version, because no operation leaves deferred work.

**Space.** BUILD makes $2n - 1$ nodes, and each update makes one node per level of its path, so after $u$ updates the pool has at most $2n - 1 + u(\lceil \lg n \rceil + 1)$ nodes. For the range k-th smallest structure on $m$ values in $[0, n)$, that is $\Theta(n + m \log n)$. The pool can start from a single shared all-zero tree with one node per level, built in $\Theta(\log n)$, which lowers the cost of `build` for zero arrays from $\Theta(n)$ to $\Theta(\log n)$; this is a [dynamic segment tree](/dynamic-segment-tree/) made persistent.

## Variants

- **Other monoids.** Minimum, maximum, products of matrices or any associative operation work the same way; only the combine step in L4 and L9 changes.
- **Range updates.** [Lazy propagation](/lazy-propagation/) needs care, because pushing a tag down writes into children that other versions share. A persistent version must copy each child before it pushes a tag into it, which keeps $O(\log n)$ new nodes per operation; a query must also copy, or must instead add the tags on its path without pushing them (tag permanence).
- **Implicit zero tree.** Start from a single node that is its own left and right child, with sum 0. A query reaches it for any range and gets 0. This gives a tree over a huge range, such as $[0, 10^9)$, with $O(\log R)$ new nodes per update for a range of size $R$.
- **Offline alternatives.** The [wavelet tree](/wavelet-tree/) answers range k-th smallest in $O(\log \sigma)$ time with $O(m \log \sigma)$ bits, and the [merge sort tree](/merge-sort-tree/) answers the count of values below $y$ in $O(\log^2 m)$. Both are static.
- **Versions over a sweep.** Sweep the points of the plane by $x$ and insert their $y$ in order; then version $j$ holds the points with the $j$ smallest $x$, and a count in a rectangle is a difference of two queries. This answers 2D dominance counting online in $O(\log n)$ per query.

## When to use it

Use a persistent segment tree when range queries must see an old state of an array, or when a query is over the difference of two prefixes of a sequence: the k-th smallest in a subarray, the count of values in a range within a subarray, or online 2D counting. It is easy to code, since it is a segment tree with copies. If the queries are known in advance, offline methods such as sorting the queries and a [Fenwick tree](/fenwick-tree/) use $O(n)$ space instead of $O(n \log n)$. If only the newest version is needed, the ephemeral segment tree is faster and smaller.

## Pitfalls

- **Writing into a shared node.** Each update must make new nodes on its path (L5, L9). Changing $t.sum$ in place changes every version that shares $t$. Lazy tags are the usual source of this error.
- **Memory.** Each update adds up to $\lceil \lg n \rceil + 1$ nodes; $10^6$ updates on $n = 10^6$ add about $2 \times 10^7$ nodes. A pool of flat integer arrays uses much less memory than one object per node.
- **Version numbers.** `update` returns the new version; keep it. Updating the newest version when an older one was meant gives a silent wrong answer.
- **KTH on unrelated versions.** The difference of two versions is a count array only if one was made from the other by additions. For two versions on different branches of the [version tree](/version-tree/), the differences can be negative and KTH has no meaning.
- **Range bounds.** The code uses half-open ranges $[l, r)$. Mixing them with closed ranges is the most common off-by-one error.

## Implementations

## History

Driscoll, Sarnak, Sleator and Tarjan studied path copying as one of the general methods to make a linked structure persistent, in their paper of 1989, and Sarnak and Tarjan used persistent search trees for planar point location in 1986. Applying path copying to the segment tree, with one version per prefix of an array, became a standard method in programming contests in the 2000s, where it is often called the chairman tree.

## References
