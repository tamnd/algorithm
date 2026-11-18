---
tag: DS250H
kind: data-structure
slug: alex-learned-index
name: ALEX updatable learned index
aliases:
- ALEX
area: databases/storage-and-indexing
level: research
summary: "A learned index that supports inserts by gapped arrays at its leaves and by splitting and retraining nodes when they fill."
model: word-ram
complexity:
  vars: {n: the number of keys, h: the depth of the tree, C: the largest number of slots in a data node, e: the distance from the predicted slot to the true slot}
  time: {worst: "O(h + C)", average: "O(h + log e)", best: "O(h)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, external: false, online: true, in_place: false, recursive: false}
history:
  year: 2020
  people: [Jialin Ding, Umar Farooq Minhas, Jia Yu, Chi Wang, Jaeyoung Do, Yinan Li, Hantian Zhang, Badrish Chandramouli, Johannes Gehrke, Donald Kossmann, David Lomet, Tim Kraska]
  note: "Jialin Ding and eleven coauthors presented ALEX at SIGMOD 2020. It made the learned index of Kraska et al. (2018) support inserts, by gapped arrays and by a tree whose shape adapts to the data and the workload."
prereqs: [learned-index, exponential-search]
see_also: [pgm-index, b-plus-tree, packed-memory-array, library-sort, linear-regression, interpolation-search, adaptive-radix-tree, ordinary-least-squares]
sources:
  - paper: doi:10.1145/3318464.3389711
    title: "Jialin Ding, Umar Farooq Minhas, Jia Yu, Chi Wang, Jaeyoung Do, Yinan Li, Hantian Zhang, Badrish Chandramouli, Johannes Gehrke, Donald Kossmann, David Lomet and Tim Kraska, ALEX: an updatable adaptive learned index, Proceedings of ACM SIGMOD 2020"
    locator: pp. 969 to 984, the node layouts (gapped array and packed memory array), model-based inserts, exponential search, node expansion and splits, the cost models, bulk loading, and the experiments
  - paper: doi:10.1145/3183713.3196909
    title: "Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean and Neoklis Polyzotis, The case for learned index structures, SIGMOD 2018"
    locator: pp. 489 to 504, the recursive model index that ALEX starts from
---

ALEX is a [learned index](/learned-index/) that accepts inserts and deletes. Its leaves, the *data nodes*, are sorted arrays with gaps, and each has a linear model that predicts the slot of a key. An insert puts the key in the slot that the model predicts when that keeps the order, so later lookups find it at or near the prediction, and an [exponential search](/exponential-search/) from the prediction finishes the lookup. Its inner nodes also hold linear models, which choose a child, and the tree grows by expanding and splitting nodes when they fill. ALEX is exact: the models only guide the search. Its reported speed and size are measurements, not bounds.

## In plain words

Think of a shelf of books in order, with some free spaces left on purpose. A good guess tells you that a book with a title starting with "M" should be about halfway along the shelf. When you buy a new book, you put it where the guess says, if that space is free and the order stays right. If the space is not free, you push a few neighbours one place to the nearest free space. Because books sit where the guess says, finding a book later takes only a short look around the guessed place.

When a shelf gets too full, you either get a longer shelf and spread the books out again, or you split the shelf into two. A small guide above the shelves, also a guess, tells you which shelf to go to.

## The abstract type

An ordered set of distinct keys (numbers):

- `contains(k)`: is $k$ in the set.
- `insert(k)` and `delete(k)`.
- `range(lo, hi)`: the keys in $[lo, hi]$, in order.

These are the operations of a [B+ tree](/b-plus-tree/), and ALEX is meant to replace one in main memory.

## Representation

- **Inner node.** A linear model $a k + b$ and an array of child pointers of size $F$, a power of 2. The slot of $k$ is $\lfloor a k + b \rfloor$, clamped to $[0, F-1]$. A child can fill several adjacent slots.
- **Data node.** A *gapped array* of $C$ slots, a bitmap of the occupied slots, and a linear model that maps a key to a slot. The keys are in increasing order across the occupied slots. Each gap holds a copy of the next key to its right (or $\infty$), so the whole array is sorted and a plain search works on it. The data nodes are linked in key order for range scans.
- **Density limits.** The paper uses a lower limit $d_l = 0.6$ and an upper limit $d_u = 0.8$ for the fraction of occupied slots. A new or rebuilt node has density $d_l$; a node that would go above $d_u$ expands or splits.

The paper also gives a second layout for data nodes, the [packed memory array](/packed-memory-array/), which keeps the gaps spread evenly and so bounds the cost of a shift.

## Operations

```pseudo id=main
LOOKUP(k)
L1  v ← root
L2  while v is an inner node do v ← v.child[clamp(⌊v.model(k)⌋, 0, v.fanout - 1)]
L3  p ← clamp(round(v.model(k)), 0, v.capacity - 1)
L4  i ← EXPONENTIAL-SEARCH from p for the first slot with a value ≥ k
L5  return true if the first occupied slot at or after i holds k

INSERT(k)
L6  v ← the data node of k, as in L1 to L2
L7  if v.n + 1 > d_u · v.capacity then
L8      if ⌈(v.n + 1) / d_l⌉ ≤ C then EXPAND: rebuild v with that many slots, a new model, and model-based placement
L9      else SPLIT v (sideways if it fills two or more slots of its parent, after doubling the parent if needed; else down), and go to L6
L10 p ← the predicted slot; i ← the first slot with a value ≥ k; q ← the first occupied slot at or after i
L11 if i < q then put k in the gap of [i, q - 1] that is closest to p
L12 else shift the keys between q (or i - 1) and the nearest gap one place toward the gap, and put k in the freed slot
L13 copy k into the gaps just before it; set its bit
```

- **Model-based placement.** When a node is built or expanded, each key in order goes to its predicted slot, moved right if that slot is not after the previous key, and moved left if the keys after it would not fit.
- **Sideways split.** The data node is cut by the parent's slots: if it fills the slots $[s, e)$, the keys routed to $[s, mid)$ and to $[mid, e)$ form two new nodes. If it fills only one slot, the parent first doubles its child array (slot $j$ becomes $2j$ and $2j + 1$, and its model is multiplied by 2), when it is still under the fanout limit.
- **Split down.** If the parent cannot grow, a new inner node with two slots replaces the data node, and its keys go to two new data nodes.
- **Delete** clears the slot and its bit, and copies the next key into the new gap and the gaps before it. The paper also contracts a node that gets too sparse; the code on this page does not.

The paper chooses between expanding and splitting, and builds the tree at bulk load, with cost models that predict the search and shift cost of a node from its statistics. The code on this page uses fixed limits instead (a largest capacity $C$ and a largest fanout), and the bulk load is one root over one data node per slot.

## Example

A data node with $C = 10$ slots gets the keys 10, 20, 30, 40, 50 and 60. The least-squares line through (key, rank), scaled to 10 slots, is $(k - 10)/6$, so the keys go to the slots 0, 2, 3, 5, 7 and 8 (the rounded values of 0, 1.67, 3.33, 5, 6.67 and 8.33). The array is

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| value | 10 | 20 | 20 | 30 | 40 | 40 | 50 | 50 | 60 | ∞ |
| occupied | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 0 |

1. **insert(35).** The model predicts $25/6 \approx 4.17$, slot 4. The first slot with a value $\ge 35$ is slot 4 (a gap with the copy 40), and the first occupied slot from there is 5. Slot 4 is in the gap run $[4, 4]$, so 35 goes to slot 4, exactly where the model says.
2. **insert(15).** Predicted slot 1, a gap between 10 and 20. 15 goes to slot 1.
3. **insert(33).** Predicted slot 4, which now holds 35. The first slot with a value $\ge 33$ is 4, and it is occupied, so there is no gap between 30 and 35. The nearest gap is slot 6 on the right (slots 0 to 3 are all full on the left). The keys 35 and 40 move to the slots 5 and 6, and 33 goes to slot 4.
4. **lookup(40).** The model predicts $30/6 = 5$; slot 5 holds 35 now. The exponential search goes right and finds 40 in slot 6, one slot away.

Inside an index with $d_u = 0.8$, the insert of 33 would be the ninth key in 10 slots, above $0.8 \cdot 10 = 8$, so the node would first expand to $\lceil 9 / 0.6 \rceil = 15$ slots and place all keys again by the new model.

**Measurement.** With 5,000 random keys from $[0, 10^6)$ (seed 11), a largest capacity of 256 slots and a largest fanout of 64, the bulk load gives one root and 64 data nodes, and a lookup of a stored key reads 3.2 slots on average in the exponential search. After 5,000 more random inserts, the tree has depth 3, 11 inner nodes and 74 data nodes, after 113 expansions and 10 splits, and a lookup reads 3.1 slots on average.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). The main points:

- **Routing.** All models have a slope of at least 0 (a least-squares line through sorted points cannot fall), so the routing is monotone: a smaller key never goes to a later leaf. A split partitions the keys of a node by the routing function that will route them, so every key stays in the leaf that its route reaches.
- **Gapped array.** The occupied values are strictly increasing, and every gap holds the next key to its right. So the array is sorted, the exponential search finds the first slot with a value $\ge k$, and $k$ is present if and only if the first occupied slot from there holds $k$.
- **Insert.** The slot that the code chooses is between the last key below $k$ and the first key above it, and a shift moves a run of keys by one place without changing their order. Only the gaps just before a changed slot need a new copy.
- **Termination.** An expansion makes room at once. Each split halves the slots of a node in its parent or splits down into two nonempty nodes, so the loop at L9 ends.

The models affect only the speed. A bad model gives long searches and long shifts, but never a wrong answer.

## Complexity

- **Lookup.** $h$ model evaluations to reach a data node, then an exponential search that costs $O(\log e)$ comparisons when the key is $e$ slots from the prediction. Finding the next occupied slot uses the bitmap. In the worst case, with a long run of gaps or a bad model, this is $O(C)$ on a word RAM, or $O(C / w)$ with word operations on the bitmap.
- **Insert.** A lookup plus a shift. With a gapped array the shift can cost $O(C)$ in the worst case; the packed memory array of the paper bounds the amortized cost of a shift by $O(\log^2 C)$. An expansion or a split rebuilds a node in $O(C)$ time, amortized over the inserts that filled it.
- **Space.** The keys and the gaps, at least $n / d_u$ slots in all, plus one model and a bitmap per data node and one model and one pointer array per inner node. The models are small, which is why the index part of ALEX is much smaller than the inner nodes of a B+ tree.

These are bounds for the code; the paper's claims are measurements. It reports, on a machine with an Intel Core i9-9900K and 64 GB of memory, throughput up to 4.1 times that of a B+ tree and an index up to 2000 times smaller, on its datasets and workloads.

## Variants

- **Packed memory array nodes.** The second layout of the paper keeps gaps evenly spread with density bounds per window, so the shift cost is bounded, at some cost in lookups.
- **Cost models.** The paper's ALEX estimates the cost of a node from the expected number of exponential search steps and shifts, and uses these estimates to choose between expanding, retraining and splitting.
- **[PGM-index](/pgm-index/).** A learned index with a proved error bound per segment, made dynamic by rebuilding static parts. ALEX has no such bound and adapts to the data instead.

## When to use it

ALEX fits an in-memory ordered index on numeric keys with a mix of lookups, short range scans and inserts, when the key distribution is smooth enough for linear models to predict positions. It is a research design: it does not handle strings directly, the paper does not cover concurrent access, and its speed depends on the data. Where predictable worst-case behaviour matters, a B+ tree or an [adaptive radix tree](/adaptive-radix-tree/) is the safer choice.

## Pitfalls

- **Fixed limits instead of cost models.** In the code on this page, 1,000 inserts in increasing order past the last key of an index of 100 keys, with a capacity of 32 and a fanout of 4, give a tree of depth 64 with 66 inner nodes (a measurement). Every new key goes to the rightmost node, which splits down again and again. The cost models of the paper, or a larger fanout, are needed for such patterns.
- **Gap values.** A search on the slot array is only correct if every gap holds the next key to its right. Forgetting to update the gaps before a new key, or after a delete, gives wrong lookups.
- **Floating-point models.** Rounding can change which slot a key routes to. This is not a problem if lookup and insert use the same code for the routing, but it is if two code paths compute the slot in different ways.
- **Negative slopes.** If a model could fall, the routing would no longer be monotone, and range scans along the leaves would miss keys. Least squares on sorted keys cannot give a negative slope, but a hand-made model can.
- **Duplicates.** The design assumes distinct keys. Store a list per key, or make keys unique, before indexing.

## Implementations

## History

Tim Kraska and coauthors proposed learned indexes in 2018, with a recursive model index over a static sorted array. Jialin Ding, Umar Farooq Minhas and ten coauthors, with Tim Kraska as the last author, made the idea updatable with ALEX, at SIGMOD 2020. It brought in gapped arrays with model-based inserts, exponential search, and a tree whose nodes expand and split by cost models.

## References
