---
tag: VCF4TV
kind: data-structure
slug: van-emde-boas-layout
name: van Emde Boas layout
aliases:
- vEB layout
- van Emde Boas tree layout
area: data-structures/external-memory-structures
level: advanced
summary: Recursive memory layout of a static binary search tree that gives O(log_B N) block transfers per search.
implements: [ordered-set]
model: cache-oblivious-model
prereqs: [cache-oblivious-model, binary-search-tree, complete-binary-tree]
see_also: [cache-oblivious-b-tree, packed-memory-array, eytzinger-layout, b-tree, external-searching, search-in-sorted-array, funnelsort, locality-of-reference]
sources:
  - paper: "Harald Prokop, Cache-oblivious algorithms, Master's thesis, Massachusetts Institute of Technology (1999)"
    locator: the chapter on static search trees (the recursive layout and its O(log_B N) bound)
  - paper: "Michael A. Bender, Erik D. Demaine and Martin Farach-Colton, Cache-oblivious B-trees, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS 2000)"
    locator: pp. 399 to 409, Section 2 (the van Emde Boas layout and the search bound)
  - paper: "Gerth Stolting Brodal, Rolf Fagerberg and Riko Jacob, Cache oblivious search trees via binary trees of small height, Proceedings of the 13th ACM-SIAM Symposium on Discrete Algorithms (SODA 2002)"
    locator: pp. 39 to 48 (computing the positions of the children in the layout, and experiments)
---

The van Emde Boas layout is a way to store a complete [binary search tree](/binary-search-tree/) in an array so that a search touches only $O(\log_B N)$ blocks, for every block size $B$ at once. The tree of $h$ levels is cut at its middle level into a *top tree* of $\lfloor h/2 \rfloor$ levels and $2^{\lfloor h/2 \rfloor}$ *bottom trees* of $\lceil h/2 \rceil$ levels. The array holds the layout of the top tree, then the layouts of the bottom trees from left to right, each built by the same rule. So every subtree of the recursion lies in one contiguous range. A search path crosses $O(\log_B N)$ subtrees that fit in a block, which gives the bound of a [B-tree](/b-tree/) in the [cache-oblivious model](/cache-oblivious-model/), where the algorithm does not know $B$. The proof of the bound is on the [cache-oblivious model](/cache-oblivious-model/) page. This page gives the layout as a data structure: how to build it, how to find the children of a node, and how it compares to other layouts. The name comes from the van Emde Boas tree, a structure for the [predecessor problem](/predecessor-problem/) on integers, whose recursion splits the key space at its square root in the same way.

## In plain words

A book of maps has a map of the whole country first, and then a map of each region, and each region map is followed by maps of its towns. When you go from the country to a street, you turn to a few nearby pages for each step of zoom.

The van Emde Boas layout stores a search tree like that book. The top half of the tree comes first. Then each bottom half comes, one after the other, each laid out by the same rule. A search walks down the tree and reads only a few small stretches of memory. Whatever the size of a memory block is, each stretch fits in one or two blocks.

## The abstract type

A static [ordered set](/ordered-set/) of $N$ keys, built once from a sorted list:

- `build(keys)` stores sorted distinct keys.
- `predecessor(k)` returns the largest key at most $k$, or none; see the [predecessor problem](/predecessor-problem/).
- `contains(k)` tells whether $k$ is in the set.
- `inorder()` lists the keys in order.

Updates are not supported. The [cache-oblivious B-tree](/cache-oblivious-b-tree/) adds them, with a [packed memory array](/packed-memory-array/) below the tree.

## Representation

Let $h = \lceil \lg(N+1) \rceil$ and take a complete binary search tree with $h$ levels and $2^h - 1$ nodes. The $N$ keys go into the first $N$ nodes in in-order; the other nodes hold $+\infty$. A node is named by its depth $d$, from 0 at the root, and its *path* $p$, a number of $d$ bits that gives the turns from the root, 0 for left and 1 for right. The node $(d, p)$ has in-order rank $p \cdot 2^{h-d} + 2^{h-d-1} - 1$, and its children are $(d+1, 2p)$ and $(d+1, 2p+1)$.

The array `slots` of $2^h - 1$ cells holds the node $(d, p)$ at position $\mathrm{pos}(h, d, p)$, defined below. There are no pointers.

**Invariants.**

- **(V1)** The map $(d, p) \mapsto \mathrm{pos}(h, d, p)$ is a bijection onto $\{0, \ldots, 2^h - 2\}$.
- **(V2)** For each recursive subtree, the positions of its nodes form one contiguous range.
- **(V3)** The in-order of the tree, read through the positions, is the sorted list of keys followed by the $+\infty$ cells.

## Operations

```pseudo id=main
POS(h, d, p)                  ▷ position of the node at depth d with path p, in a tree of h levels
L1  if h = 1 then return 0
L2  ht ← ⌊h/2⌋; hb ← h − ht      ▷ levels of the top tree and of each bottom tree
L3  if d < ht then return POS(ht, d, p)
L4  j ← the first ht bits of p    ▷ the bottom tree that holds the node, from the left
L5  return (2^ht − 1) + j·(2^hb − 1) + POS(hb, d − ht, the last d − ht bits of p)

BUILD(keys)
L6  h ← the least h with 2^h − 1 ≥ N; pad keys with +∞ to 2^h − 1
L7  for each node (d, p): slots[POS(h, d, p)] ← keys[p·2^(h−d) + 2^(h−d−1) − 1]

PREDECESSOR(k)
L8  d ← 0; p ← 0; best ← none
L9  while d < h do
L10     x ← slots[POS(h, d, p)]
L11     if x = k then return x
L12     if x < k then best ← x; p ← 2p + 1 else p ← 2p
L13     d ← d + 1
L14 return best
```

Line L5 is the whole layout: the top tree takes the first $2^{h_t} - 1$ cells, and the bottom tree number $j$ takes the next block of $2^{h_b} - 1$ cells after the $j$ bottom trees to its left. POS recurses on a tree of half the height, so it costs $O(\log h) = O(\log \log N)$ steps, and a search does $O(\log N \log \log N)$ work in memory. Brodal, Fagerberg and Jacob showed how to find the position of each child from that of its parent in $O(1)$ time with small tables per level, which makes a search $O(\log N)$ time. The code of this page uses the plain recursion.

**I/O cost.** A search reads one node per level. With any block size $B$ and a cache of two blocks, it touches at most $\max\{2, 8\lg(N+1)/\lg(B+1)\} = O(\log_B N)$ blocks. The proof cuts the recursion at subtrees of at most $\lg(B+1)$ levels, which fit in two blocks; see the [cache-oblivious model](/cache-oblivious-model/) for the details.

## Example

Take the keys $1, \ldots, 15$, so $h = 4$. The top tree has 2 levels (the keys 8, 4, 12), and there are 4 bottom trees of 2 levels each, under the four children of 4 and 12. The array is

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 8 | 4 | 12 | 2 | 1 | 3 | 6 | 5 | 7 | 10 | 9 | 11 | 14 | 13 | 15 |

The breadth-first order of the same tree would be $8, 4, 12, 2, 6, 10, 14, 1, 3, \ldots$; the vEB layout instead keeps each bottom tree, such as $10, 9, 11$, together.

A search for 11 reads position 0 (key 8, go right), position 2 (key 12, go left), and then enters the third bottom tree, $j = 2$ with path bits $10$: by line L5 its root is at $3 + 2 \cdot 3 + 0 = 9$ (key 10, go right), and its right child at $3 + 2 \cdot 3 + 2 = 11$ (key 11, found). The positions read are $0, 2, 9, 11$.

**A large tree.** For $N = 2^{16} - 1$ and $B = 16$, with the array aligned to a block, the worst search path meets 7 blocks; with other alignments it meets at most 8. The breadth-first layout meets 13 on its worst path, as does binary search on the sorted array. The tests of the code check these numbers.

## Correctness

Line L5 places the top tree first and the bottom trees in order after it, each in a range of its own size, and recursion places the nodes inside each part; so, by induction on $h$, POS is a bijection and every recursive subtree is contiguous. Line L7 stores at each node the key of its in-order rank, so the tree is a binary search tree in which the padding goes to the right end. PREDECESSOR is the usual search of a binary search tree: it keeps the last key smaller than $k$ on the path, and returns $k$ if it meets it. The proof is below.

## Complexity

| measure | cost |
|---|---|
| space | $2^h - 1 < 2N + 1$ cells, no pointers |
| build | $O(N \log\log N)$ time with the plain recursion, $O(N/B)$ blocks written with a recursive build |
| search, block transfers | $O(\log_B N)$ for every $B$, at most $\max\{2, 8\lg(N+1)/\lg(B+1)\}$ |
| search, time | $O(\log N)$ with the tables of Brodal, Fagerberg and Jacob |

The constant matters. A B-tree that knows $B$ uses $\log_{B+1} N$ blocks per search; the bound proved for the vEB layout is a constant factor larger: about $4\log_B N$ with a careful count, and $8\log_{B+1}(N+1)$ in the simple proof of the model page. Bender and others proved that no cache-oblivious layout can do better than $\lg e \approx 1.44$ times $\log_B N$ for all $B$, so some loss against the B-tree is necessary.

## Variants

- **Other cut points.** Cutting at another level, or with the top tree of $\lceil h/2 \rceil$ levels, gives the same bound. Brodal, Fagerberg and Jacob found in experiments that the choice of cut changes running time only a little.
- **Pointer form.** Store each node with the positions of its children. This uses more space but no arithmetic, and the same layout works for trees that are not complete.
- **B-ary leaves.** Store the bottom few levels as sorted arrays of a fixed size, which helps on real machines with known cache lines.
- **Dynamic trees.** Bender, Demaine and Farach-Colton keep a vEB-laid-out tree on top of a [packed memory array](/packed-memory-array/) to get a [cache-oblivious B-tree](/cache-oblivious-b-tree/).
- **Other recursive layouts.** The same recursion lays out the funnels of [funnelsort](/funnelsort/) and the cache-oblivious priority queues.

## When to use it

Use the vEB layout for a static search structure that must be fast on every level of a memory hierarchy at once: caches, memory pages, and disk, without tuning to each. For a known single block size, a [B-tree](/b-tree/) node layout is a little better. For data that fits in cache, the [Eytzinger layout](/eytzinger-layout/), which is breadth-first order, is often faster in practice, because its next nodes can be prefetched; see also [search in a sorted array](/search-in-sorted-array/).

## Pitfalls

- **Recomputing POS with a loop over all levels.** The plain recursion of line L5 is fine, but a version that walks the whole recursion from the top for each node can cost $O(\log N)$ per node, so $O(\log^2 N)$ per search.
- **Padding on the wrong side.** If the padding is not at the right end of the in-order, a search can go into a subtree of $+\infty$ cells and miss keys. Pad at the end of the sorted list.
- **Mixing the cut conventions.** POS and BUILD must use the same split $h_t = \lfloor h/2 \rfloor$; a mismatch scrambles the tree without any error.
- **Expecting a B-tree constant.** The vEB layout is within a constant factor of a B-tree, not equal to it. In memory, the arithmetic of POS can cost more than the cache misses it saves, for small $N$.
- **Updates.** Inserting into the array breaks the layout. Rebuild it, or use a [cache-oblivious B-tree](/cache-oblivious-b-tree/).

## Implementations

## History

Prokop described the layout in his 1999 master's thesis at MIT, in the work with Frigo, Leiserson and Ramachandran that defined cache-oblivious algorithms. He named it after the van Emde Boas tree of 1975, whose recursion on the square root of the universe it resembles. Bender, Demaine and Farach-Colton used it at FOCS 2000 as the static part of their cache-oblivious B-tree. Brodal, Fagerberg and Jacob (SODA 2002) gave fast navigation and experiments, and Bender, Brodal, Fagerberg and others (FOCS 2003) proved the lower bound of $\lg e$ on the constant for cache-oblivious searching.

## References
