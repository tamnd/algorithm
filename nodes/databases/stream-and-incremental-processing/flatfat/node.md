---
tag: 6M9DHR
kind: data-structure
slug: flatfat
name: FlatFAT
aliases:
- flat fixed-size aggregator tree
area: databases/stream-and-incremental-processing
level: research
summary: "A complete binary tree in an array that keeps partial aggregates of a window under any associative operator, with O(log n) operator calls per single update and amortized O(1) resizing."
solves: [sliding-window-aggregation]
model: word-ram
complexity:
  vars: {n: the number of leaves of the tree (a power of two), m: the number of leaves written by one update, W: the number of values in the window}
  time: {worst: "O(n)", amortized: "O(log n)", query: "O(log n)", update: "O(m + m log(n/m))", build: "O(n)"}
  space: {extra: "O(W)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 2015
  people: [Kanat Tangwongsan, Martin Hirzel, Scott Schneider, Kun-Lung Wu]
  note: "FlatFAT is the data structure inside the Reactive Aggregator of Tangwongsan, Hirzel, Schneider and Wu, which they built in IBM InfoSphere Streams and compared with the method of Arasu and Widom."
prereqs: [associative-operator, monoid, segment-tree, sliding-window-aggregation]
see_also: [two-stacks-queue, daba-queue, panes-window-aggregation, stream-slicing, fenwick-tree, count-based-window, time-based-window, amortized-cost]
sources:
  - paper: doi:10.14778/2752939.2752940
    title: Kanat Tangwongsan, Martin Hirzel, Scott Schneider and Kun-Lung Wu, General incremental sliding-window aggregation, PVLDB 8(7), 2015, pages 702 to 713
    locator: "Section 4 (the FlatFAT layout, Theorem 4.1 with O(m + m log(n/m)) time and O(n) space, and Theorem 4.2 with the exact operator counts of new, update, prefix, suffix and aggregate), Section 5.1 (the circular buffer, the query suffix(F) and prefix(B) of an inverted buffer, and the resizing rule), Section 5.2 (windows that are not FIFO), Section 6 (the experiments)"
  - paper: doi:10.14778/3339490.3339499
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, Optimal and general out-of-order sliding-window aggregation, PVLDB 12(10), 2019, pages 1167 to 1180
    locator: the FiBA tree for out-of-order insertions and evictions, which the same authors give as the successor for windows that are not in order (general locator)
  - paper: "Arvind Arasu and Jennifer Widom, Resource sharing in continuous sliding-window aggregates, Proceedings of VLDB 2004"
    title: Resource sharing in continuous sliding-window aggregates
    locator: the earlier tree of partial aggregates that FlatFAT is compared with (general locator; the page numbers are not confirmed here)
---

FlatFAT, short for flat fixed-size aggregator, is a complete binary tree stored in an array in which each internal node holds the combination of the values below it under an associative operator $\oplus$. Tangwongsan, Hirzel, Schneider and Wu (2015) use it to answer a [sliding-window aggregation](/sliding-window-aggregation/) query: the window values are the leaves, used as a circular buffer, and a change to $m$ leaves costs $O(m + m \log(n/m))$ calls of $\oplus$. The operator needs only associativity and an identity, so it can be non-commutative and non-invertible, such as concatenation, max or a product of matrices. It is a [segment tree](/segment-tree/) with a fixed layout, and the [two-stacks queue](/two-stacks-queue/) and the [DABA queue](/daba-queue/) are faster alternatives for windows that are strictly first in, first out.

## In plain words

You must always know the largest of the last few thousand readings, and readings come and go all the time. Put the readings in a row of boxes. Above each pair of boxes, write the larger of the two. Above each pair of those notes, write the larger again, and go on up to a single note at the top, which is the answer. When a reading changes, only the notes on its path to the top can change, and there are few of them, because each level halves the number of notes. The same scheme works for any way of combining two values that does not care how you group them. It does not need the values to be numbers, and it does not need a way to undo a combination.

## The abstract type

The tree keeps an array $a_0, \dots, a_{n-1}$ of values from a set with an associative operator $\oplus$ and an identity $e$, for a fixed capacity $n$. The operations are:

- **new**($v$): set the leaves to the values $v$, padded with $e$.
- **update**($C$): for each pair $(i, x)$ in the set $C$ of changes, set $a_i \leftarrow x$.
- **aggregate**(): return $a_0 \oplus a_1 \oplus \cdots \oplus a_{n-1}$.
- **prefix**($i$): return $a_0 \oplus \cdots \oplus a_i$.
- **suffix**($j$): return $a_j \oplus \cdots \oplus a_{n-1}$.

A FIFO window on top of the tree adds **insert**($x$), which appends $x$ as the youngest value, **evict**(), which removes the oldest value, and **query**(), which returns $v_1 \oplus \cdots \oplus v_c$ for the $c$ window values $v_1, \dots, v_c$, oldest first. Order matters: for concatenation, the query of the window "c", "d", "e" must be "cde" and not "ecd".

## Representation

The capacity $n$ is a power of two, $n = 2^L$. The array $T[1..2n-1]$ holds the tree: the root is $T[1]$, the children of node $h$ are $T[2h]$ and $T[2h + 1]$, and leaf $i$ is $T[n + i]$. This page counts leaves from 0; the paper counts them from 1 and puts leaf $i$ at $n + i - 1$. No pointers are stored, and the array is filled level by level, which is why the tree is called flat. Each internal node $h$ holds $T[h] = T[2h] \oplus T[2h+1]$, which by associativity is the combination of the leaves below $h$, in order from left to right. A leaf that holds no value holds $e$.

The FIFO window uses the leaves as a circular buffer with a front $F$ (the slot of the oldest value), a back $B$ (the slot for the next value) and a count $c$. When $F < B$ the values are in one block and the root is the answer. When the buffer wraps, the paper calls it *inverted*: the oldest values are at the right end of the array and the youngest at the left, and the root then holds them in the wrong order.

## Operations

```pseudo id=main
FLATFAT(n, ⊕, e)                     ▷ n = 2^L leaves; leaf i is T[n + i]; the root is T[1]

NEW(v)
L1  T[n .. 2n - 1] ← v, padded with e
L2  for h ← n - 1 down to 1 do
L3      T[h] ← T[2h] ⊕ T[2h + 1]

UPDATE(C)                            ▷ C is a set of pairs (i, x) with distinct i
L4  for each (i, x) in C do T[n + i] ← x; add ⌊(n + i) / 2⌋ to the set D
L5  while D is not empty do          ▷ D holds the changed nodes of one level
L6      for each h in D do T[h] ← T[2h] ⊕ T[2h + 1]
L7      D ← {⌊h / 2⌋ : h in D and h > 1}

AGGREGATE()
L8  return T[1]

PREFIX(i)                            ▷ a_0 ⊕ ... ⊕ a_i
L9  h ← n + i; a ← T[h]
L10 while h > 1 do
L11     if h is odd then a ← T[h - 1] ⊕ a        ▷ the left sibling comes before i
        h ← ⌊h / 2⌋
    return a

SUFFIX(j)                            ▷ a_j ⊕ ... ⊕ a_{n-1}
L12 h ← n + j; a ← T[h]; while h > 1 do
L13     if h is even then a ← a ⊕ T[h + 1]; h ← ⌊h / 2⌋
    return a

INSERT(x)                            ▷ the FIFO window: front F, back B, count c
L14 if c = n then copy the c values, oldest first, into a new tree of 2n leaves; F ← 0; B ← c
L15 UPDATE({(B, x)}); B ← (B + 1) mod n; c ← c + 1

EVICT()
L16 UPDATE({(F, e)}); F ← (F + 1) mod n; c ← c - 1
L17 if n > 1 and c < n / 4 then copy the c values into a new tree of n / 2 leaves; F ← 0; B ← c mod (n / 2)

QUERY()
L18 if c = 0 then return e; if F < B or B = 0 then return AGGREGATE()
L19 return SUFFIX(F) ⊕ PREFIX(B - 1)      ▷ inverted: the old part, then the young part
```

The update repairs one level at a time, from the leaves up. All leaves are at the same depth, so the set $D$ always holds nodes of a single level, and a node is repaired only after both its children are correct. When two changed leaves share an ancestor, the ancestor is in $D$ once and is repaired once, which is where the batch update saves work over $m$ single updates.

PREFIX climbs from leaf $i$ to the root. Each time the current node is a right child, its left sibling covers the leaves just before the part already collected, so the sibling goes on the left. SUFFIX is the mirror image.

## Example

Take concatenation of strings, which is associative but not commutative, with $n = 8$ and the leaves a, b, c, d, e, f, g, h. NEW makes 7 calls. The two children of the root hold "abcd" and "efgh", and the root holds "abcdefgh".

An update writes "C" into leaf 2 and "F" into leaf 5. The changed leaves are $T[10]$ and $T[13]$. Line L6 repairs $T[5]$ and $T[6]$, then $T[2]$ and $T[3]$, then $T[1]$: 5 calls, and the root is "abCdeFgh". Two single updates would cost $3 + 3 = 6$ calls, because they repair the root twice.

PREFIX(5) starts at $T[13]$, which is a right child, so it computes $T[12] \oplus$ "F" = "eF". The next node, $T[6]$, is a left child, so nothing is added. The node after that, $T[3]$, is a right child, so the result is $T[2] \oplus$ "eF" = "abCdeF". That is 2 calls for 3 levels.

Now use a FIFO window that starts with one leaf. Insert a, b, c and d. The tree doubles from 1 to 2 leaves at b and from 2 to 4 at c, so the leaves are a, b, c, d with $F = 0$ and $B = 0$. Evict twice: the leaves become $e$, $e$, c, d with $F = 2$. Insert "e": it goes into slot 0, and $B = 1$. The leaves are now "e", $e$, "c", "d", and the root holds "ecd", which is the wrong order. The buffer is inverted ($F = 2 > B = 1$), so line L19 returns SUFFIX(2) $\oplus$ PREFIX(0) = "cd" $\oplus$ "e" = "cde" with 2 calls.

## Correctness

The invariant is that every internal node holds the combination, in order, of the leaves below it. NEW sets it bottom-up, and UPDATE restores it on exactly the ancestors of the changed leaves, level by level, so that each node is set from two correct children. PREFIX keeps the combination of the leaves from the leftmost leaf below the current node to leaf $i$, and it reaches the root with the leftmost leaf 0. For the window, the slots that hold no value hold $e$, so the root is the answer when the values form one block. When the buffer wraps, the window is the suffix from $F$ followed by the prefix up to $B - 1$, and associativity joins them. The full proofs are in [the correctness proof](proofs/correctness.md); every statement there is a theorem.

## Complexity

All costs count calls of $\oplus$ in the word RAM, so a call is one step when $\oplus$ takes constant time.

- **Theorem** (Tangwongsan et al., Theorem 4.2). NEW makes $n - 1$ calls. An update that writes $m$ leaves makes at most $m(1 + \lceil \log_2(n/m) \rceil)$ calls. PREFIX and SUFFIX make at most $\log_2 n$ calls each, and AGGREGATE makes none. The proof on this page gives the slightly sharper bound $m r + m - 1$ with $r = \lceil \log_2(n/m) \rceil$, which is exact for $m$ evenly spaced leaves when $m$ is a power of two.
- **Theorem** (worst case per tuple). In the FIFO window, insert and evict each make at most $\log_2 n$ calls when no resize happens, and query makes at most $2 \log_2 n + 1$. One resize to $n'$ leaves makes $n' - 1$ calls, so the worst case of a single insert is $O(n)$.
- **Theorem** (amortized resizing). From one leaf, the doubling and halving rule spends at most 4 calls per insert or evict on resizes, amortized. So insert and evict cost $O(\log n)$ amortized calls, and the window keeps $n \le 4W + 3$ leaves, which is $O(W)$ space.

The queries do not change the tree, so a window that is queried after every tuple pays $O(\log n)$ for the update and $O(\log n)$ for the query. The two-stacks queue and DABA do better for this case: $O(1)$ amortized and $O(1)$ worst case calls per operation.

## Variants

- **The paper's resize rule.** When the buffer is full, the paper compacts it in place if at most 3/4 of the slots hold values, and doubles it otherwise. After an eviction, it halves the buffer if fewer than 1/4 of the slots hold values. Resizing then costs amortized $O(1)$. Compaction matters only for windows that are not FIFO (Section 5.2), where evictions leave holes in the middle; in a FIFO window there are no holes, and the code on this page uses plain doubling.
- **Windows that are not FIFO and late data.** Because UPDATE can write any leaf, a value that arrives late but still has a slot in the buffer is written into that slot in $O(\log n)$ calls, and an eviction in the middle writes $e$. A value older than the front has no slot in the circular buffer of this page, so it must be dropped or counted as late, or the window must use a structure for out-of-order data such as the FiBA tree of Tangwongsan, Hirzel and Schneider (2019).
- **Batches.** With slicing or panes, the leaves are partial aggregates of slices instead of single tuples, as in [stream slicing](/stream-slicing/) and [pane-based aggregation](/panes-window-aggregation/), and when the buffer does not wrap, SUFFIX($j$) gives the window of the youngest values from slot $j$ on, so one tree can answer several window sizes that end at the same time.
- **Invertible operators.** When $\oplus$ has an inverse, as for a sum, a single running total with subtract-on-evict costs $O(1)$ and the tree is not needed. A [Fenwick tree](/fenwick-tree/) also needs an inverse to answer a range from two prefixes.

## When to use it

Use FlatFAT when the operator is associative but has no inverse, when the window changes in batches or out of FIFO order, or when one structure must answer many sub-ranges of the window through PREFIX and SUFFIX. For a strictly FIFO window with one change at a time, the two-stacks queue or DABA is cheaper. For an invertible operator, a running total is cheapest.

## Pitfalls

- **Order in the inverted buffer.** When the buffer wraps, the root holds the values in the wrong order. This is harmless for max or sum and wrong for concatenation, list collection or matrix products. Test with a non-commutative operator.
- **The identity.** Empty slots must hold the identity of $\oplus$, not 0 or None, unless the operator treats that value as the identity.
- **Repairing an ancestor twice.** A batch update that applies $m$ single updates one after another is correct but costs $m \log_2 n$ calls; the bound $O(m + m \log(n/m))$ needs the level-by-level repair.
- **Resizing in the worst case.** A doubling copies the whole window and rebuilds the tree, so one insert can cost $O(n)$. Systems with a latency limit per tuple need a structure with a worst-case bound, such as DABA.
- **A power of two.** The layout assumes that $n$ is a power of two. Other sizes must be rounded up and padded with the identity.

## Implementations

The paper's Reactive Aggregator, built on FlatFAT, was implemented in IBM InfoSphere Streams and measured against the method of Arasu and Widom on a two-core Xeon machine; these results are measurements, and this page does not repeat their numbers. The Python code on this page has the tree, the batch update, PREFIX, SUFFIX and the FIFO window with doubling and halving, and it counts calls of $\oplus$. Its tests check every query against recomputation of the window from scratch, with concatenation, max and sum, and they check the call counts against the bounds above.

## History

Arasu and Widom (2004) kept precomputed partial aggregates over intervals of the window to share work between sliding-window aggregates with different ranges. Tangwongsan, Hirzel, Schneider and Wu (2015) gave FlatFAT as a general structure for any associative operator, stored it in a flat array, gave exact operator counts, and added the circular buffer with resizing for windows whose size changes over time. The same group later gave DABA (2017) for FIFO windows with worst-case $O(1)$ calls, and FiBA (2019) for out-of-order windows.

## References
