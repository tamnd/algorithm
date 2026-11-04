---
tag: A555C0
kind: data-structure
slug: packed-memory-array
name: Packed memory array
aliases:
- PMA
- cache-oblivious sorted array
- dynamic array with gaps
area: data-structures/external-memory-structures
level: research
summary: Sorted array with evenly spaced gaps that supports updates in O(log^2 N) amortized moves while staying scan-friendly.
implements: [ordered-set]
model: cache-oblivious-model
prereqs: [cache-oblivious-model, amortized-cost, binary-search]
see_also: [cache-oblivious-b-tree, van-emde-boas-layout, library-sort, dynamic-array, b-tree, potential-method, external-searching]
sources:
  - paper: "Alon Itai, Alan G. Konheim and Michael Rodeh, A sparse table implementation of priority queues, International Colloquium on Automata, Languages and Programming (ICALP 1981), Lecture Notes in Computer Science 115"
    locator: pp. 417 to 431 (the sparse table with density thresholds and O(log^2 N) amortized moves per insert)
  - paper: "Michael A. Bender, Erik D. Demaine and Martin Farach-Colton, Cache-oblivious B-trees, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS 2000)"
    locator: pp. 399 to 409, the section on the packed memory structure (thresholds per level of an implicit tree, the O(log^2 N) bound, and O(1 + (log^2 N)/B) memory transfers)
  - paper: "Michael A. Bender and Haodong Hu, An adaptive packed-memory array, ACM Transactions on Database Systems 32(4) (2007)"
    locator: Sections 2 and 3 (the standard PMA with its density thresholds, and an adaptive version for common insert patterns)
---

A packed memory array, or PMA, keeps $N$ keys in sorted order in an array of $\Theta(N)$ cells, with gaps spread among the keys. A new key goes into a gap near its place, so most inserts move only a few keys. When a part of the array gets too full, the PMA spreads the keys of a larger part evenly, choosing the smallest part, among nested windows of sizes $\Theta(\log N) \cdot 2^i$, that is not too full for its level. With density limits that get tighter toward larger windows, an insert or a delete moves $O(\log^2 N)$ keys amortized, and since every window is contiguous, it costs $O\big(1 + \frac{\log^2 N}{B}\big)$ amortized block transfers in the [cache-oblivious model](/cache-oblivious-model/), for every $B$. Because the gaps take only a constant fraction, a scan of $K$ consecutive keys costs $O(1 + K/B)$ transfers, like a plain sorted array. The idea goes back to the sparse tables of Itai, Konheim and Rodeh in 1981, and Bender, Demaine and Farach-Colton used it in 2000 as the base layer of the [cache-oblivious B-tree](/cache-oblivious-b-tree/).

## In plain words

Picture a bookshelf where you leave some space between the books. A new book fits into a nearby gap, so you only shift a few books. If one shelf gets crowded, you spread out the books of that shelf and its neighbor. If that pair is crowded too, you spread out a larger group of shelves.

The rule for "crowded" is stricter for larger groups. So big spreads are rare, and most inserts touch only a small region. Since the books stay in order with small gaps, reading a run of them is as fast as reading a packed shelf.

## The abstract type

An [ordered set](/ordered-set/) of distinct keys, stored in sorted order in one array:

- `insert(k)` and `delete(k)`.
- `predecessor(k)` returns the largest key at most $k$; `contains(k)` follows from it.
- `range(a, b)` lists the keys between $a$ and $b$ by one scan.

Unlike a search tree, the PMA guarantees that the keys sit in order in a region of $O(N)$ cells, which is what scans and the cache-oblivious B-tree need.

## Representation

- An array `slots` of capacity $c = 2^r$, holding the keys in increasing order and *gaps* (empty cells) elsewhere.
- *Segments* of $S$ cells, where $S$ is a power of two near $\lg c$, so there are $c/S$ segments. Let $H = \lg(c/S)$.
- The *windows* at height $i$, for $0 \le i \le H$, are the aligned runs of $2^i$ segments. They are the nodes of an implicit complete binary tree whose leaves are the segments and whose root is the whole array. Nothing of this tree is stored.
- *Density thresholds.* The density of a window is its number of keys divided by its size. At height $i$, the upper threshold $\tau_i$ goes linearly from $\tau_0 = 1$ at the segments to $\tau_H = 1/2$ at the root, and the lower threshold $\rho_i$ from $\rho_0 = 1/16$ to $\rho_H = 1/8$. So $\rho_0 < \rho_H < \tau_H < \tau_0$, and larger windows have tighter limits. These are the constants of the code of this page; any constants in the same order work.

**Invariants.**

- **(A1)** The keys in `slots`, read from left to right and skipping gaps, are strictly increasing.
- **(A2)** The capacity is a power of two, and $S$ divides it.
- **(A3)** After a rebalance of a window $W$ at height $i$, the keys of $W$ are spread evenly, so every window inside $W$ has density at most about the density of $W$, which is at most $\tau_i$.

## Operations

```pseudo id=main
INSERT(A, k)
L1  p ← the position of the predecessor of k, by binary search that skips gaps (segment 0 if none)
L2  for i ← 0 to H do
L3      W ← the window at height i that holds position p
L4      if (keys(W) + 1) / |W| ≤ τ_i then
L5          REBALANCE(W, with k added); return
L6  RESIZE(A, with k added)                ▷ the whole array is too dense

DELETE(A, k)
L7  p ← the position of k; if k is absent then return; make p a gap
L8  for i ← 0 to H do
L9      W ← the window at height i that holds position p
L10     if keys(W) / |W| ≥ ρ_i then REBALANCE(W) if i > 0; return
L11 RESIZE(A)                              ▷ the whole array is too sparse

REBALANCE(W, extra)
L12 collect the keys of W in order, insert extra at its place if given, and write them back evenly spaced over W

RESIZE(A, extra)
L13 collect all keys, add extra if given; choose the capacity 2^r with density between 0.177 and 0.354, recompute S and H, and spread the keys evenly
```

**Searching.** A binary search over the array treats a probe that hits a gap by moving right to the next key in the current range. It costs $O(\log N)$ probes and $O(\log (N/B))$ block transfers, as on a sorted array. For $O(\log_B N)$ transfers, put a static search tree in the [van Emde Boas layout](/van-emde-boas-layout/) over the segments; this is the [cache-oblivious B-tree](/cache-oblivious-b-tree/).

**Why the new key fits.** In line L5, the window has at most $\tau_i |W| \le |W|$ keys after the insert, so it has room. And all keys before $W$ are at most the predecessor of $k$ and all keys after $W$ are larger than $k$, so placing $k$ in order inside $W$ keeps (A1).

## Example

The array starts with capacity 8, $S = 2$ and $H = 2$, so the thresholds are $\tau_0 = 1$, $\tau_1 = 3/4$, $\tau_2 = 1/2$. A gap is written $\_$.

1. Insert 50, 20, 80. The third insert finds its segment full ($3/2 > 1$) and spreads the first window of height 1: $20\ 50\ 80\ \_\ \ \_\ \_\ \_\ \_$.
2. Insert 10. Its segment ($3/2 > 1$) and its window of height 1 ($4/4 > 3/4$) would be too dense, but the whole array would have $4/8 = 1/2 \le \tau_2$, so the root is spread: $10\ \_\ 20\ \_\ 50\ \_\ 80\ \_$.
3. Insert 60 and 30: each fits in its own segment: $10\ \_\ 20\ 30\ 50\ 60\ 80\ \_$.
4. Insert 70. Its segment, its pair of segments ($4/4$) and the root ($7/8$) are all too dense, so RESIZE builds an array of 32 cells with $S = 4$ and $H = 3$, and spreads the 7 keys: $10$ at cell 0, $20$ at 4, $30$ at 9, $50$ at 13, $60$ at 18, $70$ at 22 and $80$ at 27.
5. Insert 40: its segment (cells 8 to 11) holds only 30, so the segment is spread: 30 at cell 8 and 40 at cell 10.

The 8 inserts made 19 moves in the count of the code. A scan of the range 15 to 60 reads cells 4 to 18 and returns 20, 30, 40, 50, 60.

## Correctness

Each update changes the keys only inside one window $W$ or the whole array, and writes them back in order. The keys outside $W$ are not moved, and by the choice of $p$ they are all smaller or all larger than the keys inside, so the whole array stays sorted. A rebalanced window always has room, because its density after the update is at most $\tau_i \le 1$. A resize picks a capacity that holds all keys. The search finds the predecessor because a gap does not change the order of the keys around it. The proof is below.

## Complexity

**Moves per update.** Consider a window $W$ at height $i \ge 1$ that is rebalanced in an insert. It was too dense for one of its two children: that child had density above $\tau_{i-1}$. Right after the last rebalance of $W$ or of an ancestor, all windows inside $W$ had density at most $\tau_i$, up to rounding. So since then, at least $(\tau_{i-1} - \tau_i) \cdot |W|/2$ keys were inserted into that child. The gap $\tau_{i-1} - \tau_i = (\tau_0 - \tau_H)/H$ is $\Theta(1/\log N)$, so this is $\Omega(|W|/\log N)$ inserts. The rebalance costs $O(|W|)$ moves, so each of these inserts pays $O(\log N)$ for this window. An insert is charged at most once per height, and there are $O(\log N)$ heights, which gives $O(\log^2 N)$ amortized moves. Deletes are the same with the lower thresholds. A resize costs $O(N)$, and it happens only after $\Omega(N)$ updates since the last resize, because a resize leaves the density at a constant factor from both root thresholds.

| measure | cost |
|---|---|
| insert, delete: moves | $O(\log^2 N)$ amortized |
| insert, delete: block transfers | $O\big(1 + \frac{\log^2 N}{B}\big)$ amortized, plus the search |
| search with binary search | $O(\log N)$ time, $O(\log (N/B))$ transfers |
| scan of $K$ keys | $O(1 + K/B)$ transfers |
| space | $\Theta(N)$ cells |

**Lower bound.** Keeping $N$ keys in order in an array of size $O(N)$ is the *online list labeling* problem. Bulánek, Koucký and Saks proved in 2012 that $\Omega(\log^2 N)$ amortized moves are needed in the worst case for arrays of linear size, so the PMA is optimal for its space. With an array of size $N^{1+\Omega(1)}$, $O(\log N)$ moves suffice.

## Variants

- **Worst-case bounds.** Willard gave a sparse table with $O(\log^2 N)$ moves per update in the worst case, at the price of a much more complex structure.
- **Adaptive PMA.** Bender and Hu's adaptive packed memory array leaves more gaps where inserts are frequent, which gives $O(\log N)$ amortized moves for common patterns such as inserts at the end or at a few hot spots, while keeping the general bound.
- **Randomized labeling.** Bender and others (FOCS 2022) beat $\log^2 N$ in expectation with randomization, which shows that the lower bound holds only for deterministic algorithms.
- **Library sort.** [Library sort](/library-sort/) is insertion sort into an array with gaps, the same idea used for sorting.
- **Graphs and sparse matrices.** PMAs store the edge lists of dynamic graphs in one array, so that scans of neighbors stay fast while edges are added.

## When to use it

Use a PMA when data must stay in sorted order in one contiguous array, for fast scans and for cache-friendly behavior at all levels of memory, and yet must take inserts and deletes: as the base of a [cache-oblivious B-tree](/cache-oblivious-b-tree/), for dynamic graph storage, and for sorted indexes that are scanned often. If only searches and updates matter, a [B-tree](/b-tree/) has better update cost; if the set is static, a sorted array or the [van Emde Boas layout](/van-emde-boas-layout/) is simpler.

## Pitfalls

- **One threshold for all levels.** With the same density limit for all window sizes, one crowded spot can cause rebalances of large windows over and over, and the cost becomes linear per insert. The limits must get tighter for larger windows.
- **Thresholds that leave no gap at the root.** The density after a resize must be well inside $(\rho_H, \tau_H)$; otherwise a few updates cause another resize, and the cost of resizing is not amortized.
- **Uneven spreading.** A rebalance must spread the keys evenly, so that every sub-window ends below its own limit. Packing the keys to the left leaves full segments that overflow at once.
- **Binary search on gaps.** A probe that lands on a gap must look for the next key in the current range, not stop.
- **Segments that are too small.** With segments of $O(1)$ cells, the number of heights is $\lg N$ and the gaps between thresholds become too small; segments of $\Theta(\log N)$ cells keep the analysis and the constants reasonable.

## Implementations

## History

Itai, Konheim and Rodeh (ICALP 1981) introduced sparse tables with density thresholds and the $O(\log^2 N)$ amortized bound, to implement priority queues. Willard (1982, journal version 1992) made the bound worst-case. Bender, Demaine and Farach-Colton (FOCS 2000) gave the name packed memory structure and analyzed it in the cache-oblivious model, as a part of the cache-oblivious B-tree. Bender and Hu (2007) made it adaptive. Bulánek, Koucký and Saks (STOC 2012) proved the matching lower bound for deterministic algorithms with linear space.

## References
