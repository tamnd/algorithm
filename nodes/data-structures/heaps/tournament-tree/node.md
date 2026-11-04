---
tag: A58YZQ
kind: data-structure
slug: tournament-tree
name: Tournament tree
aliases:
- winner tree
- loser tree
- tournament
area: data-structures/heaps
level: core
summary: Complete binary tree of pairwise comparisons whose root holds the current minimum.
implements: [priority-queue]
model: comparison-model
complexity:
  vars: {k: the number of players (leaves)}
  time: {worst: O(log k)}
  space: {extra: Θ(k)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [complete-binary-tree, binary-tree, priority-queue, induction]
see_also: [tournament-sort, k-way-merge, replacement-selection, external-merge-sort, tournament-minimum, binary-heap, segment-tree, heap-select]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1 (Multiway merging and replacement selection), trees of winners and trees of losers; Section 5.2.3 (Sorting by selection), tree selection; Section 5.3.3 (Minimum-comparison selection), the second largest of n
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9 (Medians and Order Statistics), Exercise 9.1-1 on the second smallest element with n + ⌈lg n⌉ − 2 comparisons
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), multiway merge with an index priority queue
---

A tournament tree holds $k$ *players*, each with a key, at the leaves of a complete binary tree, and each internal node records the result of a match between the winners of its two subtrees. The root records the overall winner, the player with the smallest key. When the key of one player changes, only the $\lceil \lg k \rceil$ or so matches on its path to the root are played again. The *winner tree* stores the winner at each node; the *loser tree* stores the loser and needs only one comparison per level. Loser trees are the standard tool for the [k-way merge](/k-way-merge/) of [external merge sort](/external-merge-sort/) and for [replacement selection](/replacement-selection/).

## In plain words

Think of a knockout sports tournament. Players meet in pairs, the winners meet in pairs again, and one champion is left at the end. Each match is recorded on a board shaped like a tree.

Now suppose the champion leaves and a new player takes that place. You do not need to replay the whole tournament. Only the matches that the old champion played are affected, one per round. Replay those, from the bottom up, and you have the new champion. With a thousand players, that is about ten matches instead of a thousand.

A loser board records, for each match, the player who lost. The newcomer then only has to beat the recorded losers on the path, which saves looking up the other side of each match.

## The abstract type

A tournament tree is a priority queue over a fixed set of $k$ slots, numbered $0$ to $k - 1$. Each slot holds a key, or $+\infty$ when it is empty.

- `build(key[0..k-1])` plays all matches.
- `winner()` returns the slot with the smallest key; ties go to the smaller slot number.
- `update(i, x)` sets the key of slot $i$ to $x$, which may be $+\infty$.

A priority queue of at most $k$ items is the special case in which delete-min is `update(winner(), +∞)` and insert writes into an empty slot. In the loser tree, `update` is allowed only for the current winner, which is the case in a merge and in sorting.

## Representation

Both trees use an array of $2k$ cells, in the layout of a [binary heap](/binary-heap/) with 1-based indices. The leaves are the cells $k$ to $2k - 1$, with leaf $k + i$ for slot $i$. The internal nodes are $1$ to $k - 1$, the children of $j$ are $2j$ and $2j + 1$, and the parent of $j$ is $\lfloor j/2 \rfloor$. This tree has $2k - 1$ nodes, and every internal node has two children, for any $k \ge 1$, not only for powers of 2. The depth of leaf $k + i$ is $\lfloor \lg(k + i) \rfloor$, which is $\lfloor \lg k \rfloor$ or $\lceil \lg k \rceil$.

Say that slot $a$ *beats* slot $b$ if $key[a] < key[b]$, or the keys are equal and $a < b$. This is a total order on slots, so every set of slots has one winner.

**Invariant of the winner tree (W).** $t[k + i] = i$ for each slot, and for each internal node $j$, $t[j]$ is the slot of the two $t[2j]$ and $t[2j + 1]$ that beats the other. By induction from the leaves, $t[j]$ is the winner among the slots below $j$, and $t[1]$ is the overall winner.

**Invariant of the loser tree (L).** Let $w(j)$ be the winner among the slots below node $j$. For each internal node $j$, $l[j]$ is the slot of $w(2j)$ and $w(2j + 1)$ that loses, and $l[0] = w(1)$. The winners $w(j)$ are not stored.

## Operations

```pseudo id=main
BUILD(key[0..k-1])                      ▷ winner tree
L1  for i ← 0 to k − 1 do t[k + i] ← i
L2  for j ← k − 1 downto 1 do
L3      t[j] ← the one of t[2j], t[2j + 1] that beats the other

UPDATE(i, x)                            ▷ winner tree: key[i] ← x first
L4  j ← ⌊(k + i)/2⌋
L5  while j ≥ 1 do
L6      t[j] ← the one of t[2j], t[2j + 1] that beats the other
L7      j ← ⌊j/2⌋

WINNER()
L8  return t[1]                         ▷ slot 0 if k = 1
```

```pseudo id=loser
LOSER-UPDATE(i, x)                      ▷ i is the current winner l[0]; key[i] ← x first
L9  w ← i; j ← ⌊(k + i)/2⌋
L10 while j ≥ 1 do
L11     if l[j] beats w then swap w and l[j]   ▷ the loser stays at j, the winner goes up
L12     j ← ⌊j/2⌋
L13 l[0] ← w
```

**Build** (lines L1 to L3) plays the $k - 1$ matches bottom up, one per internal node, so it does $k - 1$ comparisons. A loser tree is built the same way, with a temporary array of winners, and stores the loser of each match.

**Update in a winner tree** (lines L4 to L7) replays the matches on the path from the leaf of slot $i$ to the root. Each replay reads both children, so it must know the winner of the other side, which is in the sibling node.

**Update in a loser tree** (lines L9 to L13) carries a candidate winner $w$ up the path. At each node it meets the stored loser. Because slot $i$ was the winner, it won every match on its path, so the stored loser at each node on the path is exactly the winner of the other side. The new key plays against it, the loser of the new match stays, and the winner goes on. This is one comparison per level and reads only the nodes on the path.

**Winner** (line L8) is $t[1]$ or $l[0]$.

## Example

Take $k = 8$ players with the keys 31, 4, 15, 92, 65, 35, 89, 7 in slots 0 to 7.

**Build of the winner tree.** The first round plays slots (0, 1), (2, 3), (4, 5), (6, 7) at nodes 4 to 7. The winners are slot 1 (key 4), slot 2 (15), slot 5 (35) and slot 7 (7). The second round, at nodes 2 and 3, gives slot 1 (4) and slot 7 (7). The final at node 1 gives slot 1. So $t[1..7]$ = [1, 1, 7, 1, 2, 5, 7], after 7 comparisons.

**Remove the winner.** Set the key of slot 1 to $+\infty$ and replay its path, nodes 4, 2, 1. Node 4: slot 0 (31) beats slot 1. Node 2: slot 2 (15) beats slot 0 (31). Node 1: slot 7 (7) beats slot 2 (15). Now $t[1..7]$ = [7, 2, 7, 0, 2, 5, 7], and the winner is slot 7, with key 7.

**The loser tree for the same keys.** Each internal node keeps the loser of its match: node 4 keeps slot 0 (31 lost to 4), node 5 slot 3, node 6 slot 4, node 7 slot 6, node 2 slot 2 (15 lost to 4), node 3 slot 5 (35 lost to 7), and node 1 slot 7 (7 lost to 4). With $l[0] = 1$, the array is $l[0..7]$ = [1, 7, 2, 5, 0, 3, 4, 6].

**Replay in the loser tree.** Set the key of the winner, slot 1, to 50, as when a run in a merge gives its next key.

| node | stored loser | candidate | match | stays at node | goes up |
|---|---|---|---|---|---|
| 4 | slot 0 (31) | slot 1 (50) | 31 < 50 | slot 1 | slot 0 |
| 2 | slot 2 (15) | slot 0 (31) | 15 < 31 | slot 0 | slot 2 |
| 1 | slot 7 (7) | slot 2 (15) | 7 < 15 | slot 2 | slot 7 |

The new winner is slot 7, and $l$ = [7, 2, 0, 5, 1, 3, 4, 6], after 3 comparisons, one per level.

**A 4-way merge.** With the runs [2, 9, 15], [5, 6], [1, 7, 20] and [3, 4, 30], a loser tree on the four heads outputs 1, 2, 3, 4, 5, 6, 7, 9, 15, 20, 30. After each output, the next key of the same run, or $+\infty$ at its end, replays the path with 2 comparisons.

## Correctness

For the winner tree, (W) says each internal node holds the winner of its two children, and so, by induction on the height, the winner of all slots below it. A change of slot $i$ changes the winners only at the ancestors of its leaf, and UPDATE recomputes those from the bottom up, each after its children are correct. For the loser tree, the key fact is that the overall winner won every match on its path, so the losers stored on the path are the winners of the sibling subtrees; replaying against them is the same as replaying the true matches. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | comparisons | time |
|---|---|---|
| build | $k - 1$ | $\Theta(k)$ |
| winner | 0 | $O(1)$ |
| update, winner tree | $\lfloor \lg(k + i) \rfloor \le \lceil \lg k \rceil$ | $O(\log k)$ |
| update of the winner, loser tree | $\lfloor \lg(k + i) \rfloor \le \lceil \lg k \rceil$ | $O(\log k)$ |
| space | | $2k$ cells for the tree and $k$ for the keys |

A replay goes through one node per level, from depth $\lfloor \lg(k + i) \rfloor$ to the root, with one comparison per node. In a winner tree, each step also reads the sibling and its key; in a loser tree it reads only the path. This halves the memory reads, which matters when the tree is large or the keys are far away in memory.

**Merging and sorting.** A $k$-way merge of $N$ keys does $k - 1$ comparisons to build and at most $\lceil \lg k \rceil$ per output, so at most $k - 1 + N \lceil \lg k \rceil$ comparisons in total. [Tournament sort](/tournament-sort/) of $n$ keys builds a tree on all of them and removes the winner $n$ times, for $n - 1 + (n - 1) \lceil \lg n \rceil$ comparisons at most. Both are within a lower-order term of the bounds for the [comparison model](/comparison-sort-lower-bound/), but they use $\Theta(n)$ extra space, unlike [heapsort](/heapsort/).

**The second smallest key.** After the build, the second smallest key has lost only to the winner, so it is one of the $\lceil \lg k \rceil$ players that met the winner on its path. A minimum over those costs at most $\lceil \lg k \rceil - 1$ more comparisons, for a total of $k + \lceil \lg k \rceil - 2$. Knuth shows in Section 5.3.3 that this number is optimal.

## Variants

- **Winner tree and loser tree.** The winner tree allows the update of any slot, so it can serve as an indexed priority queue for a fixed set of slots. The loser tree allows only the update of the winner, but it is faster for that case.
- **Replacement selection.** In [replacement selection](/replacement-selection/), each key is tagged with a run number and the tree orders by (run number, key). A key that is smaller than the last output is put in the next run, which gives runs of about twice the memory size on random data. Knuth presents it with a tree of losers in Section 5.4.1.
- **Tournament for the minimum.** The [tournament method](/tournament-method/) and the [tournament minimum](/tournament-minimum/) use the same match structure to find the smallest key, or the two smallest keys, with few comparisons.
- **Segment tree.** A [segment tree](/segment-tree/) with the minimum as the operation is a winner tree that also answers range queries.

## When to use it

Use a loser tree for the inner loop of a $k$-way merge, as in external sorting, where each output is followed by exactly one replacement of the winner. It does one comparison per level, against about two per level for the delete-min and sift-down of a [binary heap](/binary-heap/). Use a winner tree when the set of slots is fixed and any slot may change, as in event simulation with one pending event per source. Use a binary heap when the number of items changes and there is no fixed set of slots, or when memory is short, since a tournament tree needs about twice as many cells.

## Pitfalls

- **Updating a non-winner in a loser tree.** LOSER-UPDATE assumes that the changed slot won every match on its path. For any other slot, the stored losers on its path are not the winners of the sibling subtrees, and the result is wrong without an error. Use a winner tree for that case.
- **End of a run.** When a run in a merge ends, its slot must get $+\infty$, which loses to every real key. Using a fixed large number as $+\infty$ breaks when real keys can be as large.
- **Ties.** Without a fixed rule for equal keys, a merge is not stable. Breaking ties by slot number, as here, keeps a merge of runs stable when the runs are given in their original order.
- **Number of players not a power of 2.** With the layout of this page, any $k$ works, but some leaves are one level deeper than others. A program that pads to the next power of 2 must fill the extra slots with $+\infty$.
- **The case $k = 1$.** There are no internal nodes, and the winner is slot 0. Code that reads $t[1]$ without a check reads a leaf or a cell that does not exist.

## Implementations

The Python version has a `WinnerTree`, a `LoserTree`, a `k_way_merge` of sorted iterables with a loser tree, and a `tournament_sort`. A key of `None` is $+\infty$. The loser tree counts its comparisons, and the tests check that a replay costs one comparison per level.

## History

Knockout tournaments to find the best of $n$ are old; their analysis for finding the second best goes back to Lewis Carroll's 1883 remarks on lawn-tennis tournaments, which Knuth discusses in Section 5.3.3. Knuth traces the history of tree selection, of the tree of losers and of replacement selection, which came from the early work on sorting with magnetic tapes, in Sections 5.2.3 and 5.4.1. Tournament trees are still the usual merge structure in external sorting programs.

## References
