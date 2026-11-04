---
tag: KRJ5HP
kind: data-structure
slug: cache-oblivious-b-tree
name: Cache-oblivious B-tree
aliases:
- cache-oblivious search tree
- COB-tree
area: data-structures/external-memory-structures
level: research
summary: Dynamic search tree that matches B-tree I/O bounds without knowing B, built from a van Emde Boas layout and a packed memory array.
implements: [ordered-set]
model: cache-oblivious-model
prereqs: [packed-memory-array, van-emde-boas-layout, cache-oblivious-model]
see_also: [b-tree, b-epsilon-tree, external-searching, write-optimized-structure, locality-of-reference, binary-search-tree]
sources:
  - paper: "Michael A. Bender, Erik D. Demaine and Martin Farach-Colton, Cache-oblivious B-trees, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS 2000)"
    locator: pp. 399 to 409 (the packed memory structure, the static tree in the van Emde Boas layout over it, the post-order update, and the bound with indirection)
  - paper: "Michael A. Bender, Erik D. Demaine and Martin Farach-Colton, Cache-oblivious B-trees, SIAM Journal on Computing 35(2) (2005)"
    locator: pp. 341 to 358 (journal version, with the full proofs of the update bounds)
  - paper: "Michael A. Bender, Ziyang Duan, John Iacono and Jing Wu, A locality-preserving cache-oblivious dynamic dictionary, Proceedings of the 13th ACM-SIAM Symposium on Discrete Algorithms (SODA 2002)"
    locator: pp. 29 to 38 (a simpler structure with the same bounds, built from a PMA, a static vEB tree and one level of indirection)
  - paper: "Gerth Stolting Brodal, Rolf Fagerberg and Riko Jacob, Cache oblivious search trees via binary trees of small height, Proceedings of the 13th ACM-SIAM Symposium on Discrete Algorithms (SODA 2002)"
    locator: pp. 39 to 48 (a dynamic tree of height lg N + O(1) kept in a vEB-laid-out array, and experiments)
---

A cache-oblivious B-tree is a dynamic search tree that matches the I/O bounds of a [B-tree](/b-tree/) in the [cache-oblivious model](/cache-oblivious-model/), where the algorithm does not know the block size $B$. A search costs $O(\log_B N)$ block transfers for every $B$ at once, so the same code is efficient between cache and memory and between memory and disk. The basic form of Bender, Demaine and Farach-Colton has two layers. The keys sit in order in a [packed memory array](/packed-memory-array/) (PMA), a sorted array with gaps that takes inserts and deletes with $O(\log^2 N)$ amortized moves. Over the segments of the PMA there is a static complete binary tree stored in the [van Emde Boas layout](/van-emde-boas-layout/), whose nodes hold the smallest key below them. A search walks down this index to a segment and scans it. An update changes one window of the PMA and then fixes the index nodes above that window. This gives $O\big(\log_B N + \frac{\log^2 N}{B}\big)$ amortized transfers per update, and one more level of indirection brings it to $O(\log_B N)$. Range queries of $K$ keys cost $O(\log_B N + K/B)$, because the keys are in order in one array.

## In plain words

Think of a library where the books stand in order on long shelves with some free space, and a card index tells you which shelf to go to. To find a book, you read a few cards and then look along one short stretch of shelf.

To add a book, you put it in a nearby free space, or you spread out the books of a few shelves to make room. Then you fix the cards that point to those shelves. The cards are kept in a special order so that a lookup reads few pages of the index, whatever the page size is.

## The abstract type

An [ordered set](/ordered-set/) of distinct keys:

- `insert(k)` and `delete(k)`.
- `predecessor(k)` returns the largest key at most $k$, or none; `contains(k)` follows from it.
- `range(a, b)` lists the keys in $[a, b]$ in order.

The same operations as a [B-tree](/b-tree/), with the same I/O cost for searches, but with no parameter $B$ in the code.

## Representation

- **The PMA.** An array `slots` of capacity $c = 2^r$ with the keys in increasing order and gaps elsewhere, cut into $2^H$ segments of $S = \Theta(\log N)$ cells, with the density thresholds of the [packed memory array](/packed-memory-array/) page.
- **The index.** A complete binary tree with $H + 1$ levels, whose leaf $s$ at depth $H$ stands for segment $s$. A node $v$ stores $\min(v)$, the smallest key in the segments below it, or none if they are all empty. The nodes are stored in one array in the van Emde Boas layout: the node at depth $d$ with path $p$ is at position $\mathrm{POS}(H + 1, d, p)$, as defined on the [van Emde Boas layout](/van-emde-boas-layout/) page. The code keeps the table of positions, so a child is found in $O(1)$ time.

**Invariants.**

- **(C1)** The keys of `slots`, read from left to right and skipping gaps, are strictly increasing; this is the invariant of the PMA.
- **(C2)** For each leaf $s$, $\min(s)$ is the first key of segment $s$, or none if the segment is empty.
- **(C3)** For each internal node $v$, $\min(v) = \min(\text{left}(v))$ if that is not none, and $\min(\text{right}(v))$ otherwise.

By (C1), (C2) and (C3), $\min(v)$ is the smallest key in the segments below $v$.

## Operations

```pseudo id=main
SEARCH(T, k)                      ▷ returns the segment s and the position of the predecessor of k
L1  v ← the root
L2  while v is not a leaf do
L3      if min(right(v)) ≠ none and min(right(v)) ≤ k then v ← right(v) else v ← left(v)
L4  s ← the segment of v; scan it for the last key ≤ k; return s and its position (none if there is none)

INSERT(T, k)
L5  p ← the position from SEARCH(T, k); if k is there then return
L6  find the window W of the PMA around p for k, and rebalance it with k added, as in the PMA
L7  if no window had room then resize the PMA and build the index again; return
L8  UPDATE(the segments of W)

DELETE(T, k)
L9  p ← the position from SEARCH(T, k); if k is absent then return; make p a gap; rebalance a window W as in the PMA, or resize and build again
L10 UPDATE(the segments of W)

UPDATE(s0 .. s1)
L11 for s ← s0 to s1 do min(leaf s) ← the first key of segment s, or none
L12 for d ← H − 1 down to 0 do
L13     for each node v at depth d above s0 .. s1 do min(v) ← min(left(v)) if not none, else min(right(v))

BUILD
L14 compute POS for all nodes, then UPDATE(0 .. 2^H − 1)
```

**Why the search finds the segment.** The search keeps the rule: if any key is at most $k$, the predecessor of $k$ is below $v$ or before every key below $v$, and in the second case no key below or before $v$ is at most $k$. Going right when $\min(\text{right}(v)) \le k$ is safe because then the right subtree has a key at most $k$, and every key after it is larger than the keys in it. Going left otherwise is safe because every key in the right subtree is larger than $k$.

**Updates in the paper.** Bender, Demaine and Farach-Colton update the nodes above a window in post-order, so that the work follows the van Emde Boas layout and costs $O(\log_B N + |W|/(SB))$ transfers for the index. The code of this page updates them level by level, which computes the same values in another order; it is simpler, but its I/O cost for large windows is not the bound of the paper.

## Example

Insert $50, 20, 80, 10, 60, 30, 70, 40$, the same keys as on the [packed memory array](/packed-memory-array/) page. After the resize at the insert of 70, the PMA has 32 cells and 8 segments of 4 cells:

| segment | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| cells | $10\ \_\ \_\ \_$ | $20\ \_\ \_\ \_$ | $30\ \_\ 40\ \_$ | $\_\ 50\ \_\ \_$ | $\_\ \_\ 60\ \_$ | $\_\ \_\ 70\ \_$ | $\_\ \_\ \_\ 80$ | $\_\ \_\ \_\ \_$ |
| min | 10 | 20 | 30 | 50 | 60 | 70 | 80 | none |

The index has 4 levels and 15 nodes. In the van Emde Boas layout with a top tree of 2 levels, the array is: the root (min 10) at position 0, its children (10 and 60) at 1 and 2, then four bottom trees of 3 nodes: $(10; 10, 20)$ at 3 to 5, $(30; 30, 50)$ at 6 to 8, $(60; 60, 70)$ at 9 to 11, and $(80; 80, \text{none})$ at 12 to 14.

**Search for 45.** At the root, the right child has min 60 > 45, so go left. At the left child, the right child, at position 6, has min 30 ≤ 45, so go right. There, the right child, segment 3 at position 8, has min 50 > 45, so go left to segment 2. The index cells read are 2, 6 and 8. The scan of segment 2 finds 30 and 40, so the predecessor is 40.

**Delete 30.** Segment 2 keeps one key out of 4, which is above the lower threshold, so the PMA moves nothing. UPDATE sets the min of segment 2 to 40, and its ancestors stay right: the node at position 6 now holds 40.

## Correctness

The PMA keeps the keys in order, as proved on its page. After each change to a window of the PMA, UPDATE recomputes the leaves of the segments in the window and then, level by level from the bottom, every ancestor of those leaves; the other nodes have no changed segment below them, so they stay right. So (C2) and (C3) hold after every operation, and a resize builds all nodes again. By (C1) to (C3), SEARCH reaches the segment of the predecessor, or segment 0 when there is no predecessor, and the scan finds it. The proof is below.

## Complexity

Let $N$ be the number of keys. The index has $H + 1 = O(\log N)$ levels over $\Theta(N/\log N)$ segments.

| measure | cost |
|---|---|
| search, block transfers | $O(\log_B N)$: the index path, plus $O(1 + (\log N)/B)$ for the segment |
| range of $K$ keys | $O(\log_B N + K/B)$ |
| insert, delete | $O\big(\log_B N + \frac{\log^2 N}{B}\big)$ amortized transfers |
| with one level of indirection | $O(\log_B N)$ amortized transfers per update |
| moves of keys | $O(\log^2 N)$ amortized per update |
| space | $\Theta(N)$ cells |

The search bound comes from the van Emde Boas layout: the path of the index meets $O(\log_B N)$ blocks for every $B$, as proved on the [cache-oblivious model](/cache-oblivious-model/) page. The update bound adds the cost of the PMA, $O(1 + (\log^2 N)/B)$ amortized, and the cost of the post-order index update. The term $(\log^2 N)/B$ is at most $\log_B N$ when $B \ge \log N \log\log N$, so for large blocks the basic form already matches the B-tree. For the general case, *indirection* groups the keys into buckets of $\Theta(\log N)$ keys, stored as small arrays, and puts only one key per bucket into the PMA; a bucket changes the PMA only once per $\Omega(\log N)$ updates, which removes a factor of $\log N$.

On the machine in the code, with $N = 4096$ random keys, the worst search over 200 queries reads 12 blocks for $B = 4$, 7 for $B = 16$, and 4 for $B = 64$ and $B = 256$; a [B-tree](/b-tree/) tuned to each $B$ reads about $\log_{B} N$, that is 6, 3, 2 and 1.5 blocks, so the cost is about twice that of a tuned B-tree in this range. Bender and others proved that a cache-oblivious search structure needs at least $\lg e \approx 1.44$ times $\log_B N$ transfers for some $B$.

## Variants

- **With indirection.** Buckets of $\Theta(\log N)$ keys below the PMA give $O(\log_B N)$ amortized transfers per update, as in the B-tree.
- **Bender, Duan, Iacono and Wu (2002).** A simpler structure from the same three parts, a PMA, a static vEB tree and one level of indirection, with the same bounds and with a fast scan of nearby keys.
- **Brodal, Fagerberg and Jacob (2002).** A binary search tree of height $\lg N + O(1)$, kept balanced by rebuilding subtrees, and stored in a vEB-laid-out array with room for $2^{\text{height}}$ nodes. It is simple and fast in practice.
- **Shuttle trees and cache-oblivious lookahead arrays.** For fast inserts, the cache-oblivious analogues of the [B^ε-tree](/b-epsilon-tree/) buffer updates; see [write-optimized structures](/write-optimized-structure/).

## When to use it

Use a cache-oblivious B-tree when the same index must be fast on several levels of memory at once, or when $B$ is not known or changes, for example in code that runs on many machines. When the block size is known and fixed, a tuned [B-tree](/b-tree/) or [B+ tree](/b-plus-tree/) is simpler and has a better constant. When updates are many and searches few, a write-optimized structure is faster. For static data, the [van Emde Boas layout](/van-emde-boas-layout/) alone is enough.

## Pitfalls

- **Rebuilding the whole index after each update.** The index must be fixed only above the window that the PMA changed; a full rebuild costs $\Theta(N/\log N)$ per update.
- **Storing the max instead of the min, or the other way round, without care.** The search rule of line L3 depends on what the nodes store. With the min, empty subtrees must count as having no key, not as $-\infty$ or $+\infty$, or the search goes into an empty segment and misses the predecessor.
- **Forgetting the empty segments.** Segments can be empty after deletes. If the search reaches a leaf whose segment has no key at most $k$, the predecessor must be none, which holds only if line L3 never goes right into a subtree without such a key.
- **Index of the wrong size after a resize.** The number of segments changes when the PMA grows or shrinks, so the index and its table of positions must be built again.
- **Expecting the B-tree constant.** The vEB index costs a constant factor more than a tuned B-tree for one block size. On real hardware, B-trees with node sizes tuned to the cache line and the page are often faster.

## Implementations

## History

Bender, Demaine and Farach-Colton introduced cache-oblivious B-trees at FOCS 2000, with the packed memory structure and the static van Emde Boas tree of Prokop; the journal version appeared in SIAM Journal on Computing in 2005. In 2002, Bender, Duan, Iacono and Wu, and independently Brodal, Fagerberg and Jacob, gave simpler structures with the same bounds, and Rahman, Cole and Raman reported experiments with cache-oblivious search trees in 2001. Bender, Farach-Colton, Kuszmaul and others later built write-optimized cache-oblivious dictionaries, such as the cache-oblivious lookahead array (2007), which led to the fractal tree indexes of TokuDB.

## References
