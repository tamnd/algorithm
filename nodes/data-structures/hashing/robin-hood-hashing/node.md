---
tag: CR9J17
kind: algorithm
slug: robin-hood-hashing
name: Robin Hood hashing
aliases:
- Robin Hood linear probing
- Robin Hood open addressing
area: data-structures/hashing
level: advanced
summary: Linear probing that swaps keys so probe lengths are evened out.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {m: the number of slots, n: the number of keys}
  time: {worst: Θ(m), expected: O(1), best: Θ(1)}
  space: {extra: Θ(m)}
properties: {deterministic: true, comparison: false, recursive: false, in_place: true}
history:
  year: 1985
  people: [Pedro Celis, Per-Åke Larson, J. Ian Munro]
  note: Celis, Larson and Munro presented Robin Hood hashing at FOCS 1985. Celis's PhD thesis at Waterloo (1986) has the full version.
prereqs: [linear-probing, open-addressing]
see_also: [quadratic-probing, swiss-table, lazy-deletion, linear-probing-analysis, hopscotch-hashing, cuckoo-hashing, primary-clustering, load-factor]
sources:
  - paper: doi:10.1109/SFCS.1985.48
    title: Pedro Celis, Per-Åke Larson and J. Ian Munro, Robin Hood Hashing (Preliminary Report), 26th Annual Symposium on Foundations of Computer Science (FOCS 1985)
    locator: pages 281 to 288
  - paper: doi:10.1137/S0097539702403372
    title: Luc Devroye, Pat Morin and Alfredo Viola, On Worst-Case Robin Hood Hashing, SIAM Journal on Computing 33(4), 2004
    locator: pages 923 to 936
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), Algorithm L (linear probing) and its analysis
  - url: https://blog.rust-lang.org/2019/07/04/Rust-1.36.0/
    title: The Rust Release Team, Announcing Rust 1.36.0 (2019)
    note: the standard HashMap moves to the hashbrown (Swiss table) design
---

Robin Hood hashing is a rule for [linear probing](/linear-probing/) in which an inserted key takes the slot of a key that is closer to its home slot, and that key moves on instead. It keeps, for each run of full slots, the keys in order of their home slots. So a search for a missing key can stop early, the total number of probes is the same as in plain linear probing, and the spread of the probe lengths is the smallest possible for the occupied slots. Deletion moves the next keys back by one slot, so the table needs no [tombstones](/tombstone/). It solves the [dictionary problem](/dictionary-problem/) in expected $O(1)$ time per operation at a fixed [load factor](/load-factor/) below 1.

## In plain words

Each key has a home slot. When the home slot is taken, the key walks right, one slot at a time, and its number of steps is its distance. In plain linear probing, the first key to reach a slot keeps it, so some keys walk a long way and others do not walk at all.

Robin Hood hashing takes from the rich and gives to the poor. When a walking key meets a key that walked less, it takes that slot, and the other key walks on. The total walking stays the same, but no key walks much more than the others.

Because the walks are fair, the keys near each home are kept in order. A search can stop when it meets a key that walked less than the search has. A deletion pulls the next keys one slot back, so there are no holes in a run.

## The problem

Keep a set of keys, each with a value, under insert, search and delete: the [dictionary problem](/dictionary-problem/). The table has slots $0, \ldots, m-1$. Slot $j$ is EMPTY or holds a key $T[j]$ and its distance $D[j] = (j - h(T[j])) \bmod m$, the number of slots between the home slot $h(T[j])$ of the key and slot $j$. All index arithmetic is modulo $m$. The table must keep at least one EMPTY slot, so $n < m$.

## The algorithm

```pseudo id=main
RH-SEARCH(T, k)                       ▷ return the slot of k, or NIL
L1  j ← h(k), d ← 0
L2  loop
L3      if T[j] = EMPTY or D[j] < d then return NIL
L4      if T[j] = k then return j
L5      j ← (j + 1) mod m, d ← d + 1

RH-INSERT(T, k)                       ▷ k is not in T, and n < m − 1 before the call
L6  x ← k, j ← h(k), d ← 0
L7  loop
L8      if T[j] = EMPTY then T[j] ← x, D[j] ← d, return
L9      if D[j] < d then swap (x, d) with (T[j], D[j])    ▷ the poorer key takes the slot
L10     j ← (j + 1) mod m, d ← d + 1

RH-DELETE(T, k)                       ▷ backward shift, no tombstones
L11 j ← RH-SEARCH(T, k)
L12 if j = NIL then return
L13 i ← (j + 1) mod m
L14 while T[i] ≠ EMPTY and D[i] > 0 do
L15     T[j] ← T[i], D[j] ← D[i] − 1
L16     j ← i, i ← (i + 1) mod m
L17 T[j] ← EMPTY
```

RH-INSERT walks right from the home slot of $k$ with the key $x$ that is "in the hand" and its distance $d$. When it meets a key that is closer to its home ($D[j] < d$), it puts $x$ there and takes the old key in the hand (line L9). The walk ends at the first EMPTY slot, so the set of full slots grows exactly as in plain linear probing. RH-SEARCH stops at line L3 when it meets an EMPTY slot or a key whose distance is less than the distance $d$ that $k$ would have here: if $k$ were further right, the insertion of $k$ would have taken this slot. RH-DELETE removes $k$ and shifts each following key with a positive distance one slot to the left, until it meets an EMPTY slot or a key in its home slot.

The table stores the distances. They can also be computed as $(j - h(T[j])) \bmod m$ from a stored hash value; many implementations store a short distance or the hash to avoid calling the hash function on old keys.

## Example

Take $m = 8$ and $h(k) = k \bmod 8$. A full slot is written key/distance, and "·" is EMPTY.

| step | what happens | $T[0 \ldots 7]$ |
|---|---|---|
| insert 8 | home 0 is EMPTY | 8/0 · · · · · · · |
| insert 1 | home 1 is EMPTY | 8/0 1/0 · · · · · · |
| insert 16 | at slot 1, 16 has distance 1 and 1 has 0: swap; 1 goes on to slot 2 | 8/0 16/1 1/1 · · · · · |
| insert 2 | home 2 is full with 1/1 (not less than 0); slot 3 is EMPTY | 8/0 16/1 1/1 2/1 · · · · |
| insert 24 | at slot 2, 24 (distance 2) takes the slot of 1/1; at slot 3, 1 (distance 2) takes the slot of 2/1; 2 lands in slot 4 | 8/0 16/1 24/2 1/2 2/2 · · · |
| insert 9 | at slot 4, 9 (distance 3) takes the slot of 2/2; 2 lands in slot 5 | 8/0 16/1 24/2 1/2 9/3 2/3 · · |
| search 9 | probes 1, 2, 3, 4: found at 4 | |
| search 17 | probes 1 to 5; at slot 5, $D = 3 < 4$: NIL | |
| search 32 | probes 0 to 3; at slot 3, $D = 2 < 3$: NIL | |
| delete 16 | slot 1 is freed; 24, 1, 9 and 2 each move one slot left; slot 5 becomes EMPTY | 8/0 24/1 1/1 9/2 2/2 · · · |

After the six insertions, the keys of the run are in order of their home slots: 8, 16, 24 (home 0), 1, 9 (home 1), 2 (home 2). Plain linear probing puts the same keys at the same six slots, in the order 8, 1, 16, 2, 24, 9. Its distances are $0, 0, 2, 1, 4, 4$, with sum 11, largest value 4 and sum of squares 37. Robin Hood gives distances $0, 1, 2, 2, 3, 3$, with the same sum 11, largest value 3 and sum of squares 27. The search for 32 stops after 4 probes; plain linear probing needs 7 probes, slots 0 to 6, to reach an EMPTY slot.

## Correctness

The key invariant is a statement about neighbours:

> **(R)** If slot $j$ holds a key with $D[j] > 0$, then slot $j - 1$ holds a key and $D[j-1] \ge D[j] - 1$.

Equivalently, along each run of full slots the home slots never decrease. From (R), all slots from the home of a key to its slot are full, so the table is a valid linear probing table. (R) also justifies the early stop: if $k$ were at slot $h(k) + t$ with $t > d$, then (R), applied $t - d$ times backward from that slot, gives a full slot at $h(k) + d$ with distance at least $d$, so line L3 does not stop there. Insertion keeps (R) because the key in the hand, at slot $j$, always has a distance at most one more than the key in slot $j - 1$, so it may be put at slot $j$. The backward shift keeps (R) because it lowers the distances of a block by 1 and stops before a key with distance 0. The full proof, with the result on the sum of squares below, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Worst case.** An insertion walks at most to the first EMPTY slot, a search at most until the distance test fails, and a deletion over one run. Each is $\Theta(m)$ in the worst case, for example when all keys have one home slot.

**Expected cost.** Insertion fills the first EMPTY slot at or after the home slot, as in plain linear probing, so the set of full slots after any sequence of insertions is the same as for plain linear probing. The total distance of all keys depends only on the home slots and the set of full slots (the proof file shows this), so it is the same too. With a random hash function and load factor $\alpha = n/m$, Knuth's analysis of [linear probing](/linear-probing-analysis/) gives an expected successful search of about $\frac{1}{2}(1 + \frac{1}{1-\alpha})$ probes, and an expected insertion of about $\frac{1}{2}(1 + \frac{1}{(1-\alpha)^2})$ probes, for a fixed $\alpha < 1$. Both are $O(1)$. The swaps of line L9 add $O(1)$ work per probe. An unsuccessful search stops at the latest at the first EMPTY slot, so it costs at most as much as in plain linear probing, and often less.

**Spread.** For a fixed set of full slots, the Robin Hood layout has the least sum of squared distances of all linear probing layouts. As the mean is fixed, its variance of the successful search cost is the least possible among all insertion rules that fill the first EMPTY slot.

**Space.** $m$ slots, plus a distance per slot. A distance fits in one byte in practice, because long distances are very rare at the load factors used.

## Properties

- **Ordered runs.** Within a run, keys are in order of home slot. Keys with the same home slot are next to each other.
- **The layout is fixed by the full slots.** For a given set of full slots, the keys of each run are sorted by home slot, so the distance of each slot is fixed. Only keys with the same home slot can be in a different order.
- **No tombstones.** Backward shift deletion leaves the table as if the key had never been inserted, up to the order of keys with equal home slots. Searches do not slow down after many deletions.
- **Same total work as linear probing.** Robin Hood does not lower the mean successful search cost. It lowers the variance and the maximum, and it speeds up unsuccessful searches.

## Variants and improvements

- **Robin Hood with other probe sequences.** The original paper of Celis, Larson and Munro uses the rule with general open addressing, where the "distance" is the number of the probe in the key's own sequence. For random probing, Devroye, Morin and Viola proved that the longest search is $\log_2 \log n \pm O(1)$ with probability $1 - o(1)$, for a fixed load factor below 1. Backward shift does not work there; deletion uses tombstones.
- **Early stop by home slot.** Instead of the distance, store the home slot or part of the hash; the test of line L3 then compares home slots.
- **Limited distance.** Store the distance in a few bits and grow the table when a distance overflows. This bounds the worst search at the cost of an early resize.
- **Hopscotch and Swiss tables.** [Hopscotch hashing](/hopscotch-hashing/) keeps each key within a fixed window of its home. The [Swiss table](/swiss-table/) uses metadata bytes and vector instructions instead of reordering.

## When to use it

Use Robin Hood hashing when you want linear probing at a high load factor, 0.8 to 0.9, with a short worst search and with many deletions. The backward shift deletion avoids the slow growth of tombstones of plain [lazy deletion](/lazy-deletion/). It costs extra writes on insertion and deletion, because keys move. If keys must not move, for example because the program keeps pointers to entries, use [separate chaining](/separate-chaining/) or a scheme without reordering. Before 2019, Rust's standard `HashMap` used Robin Hood linear probing with backward shift; Rust 1.36 replaced it with a [Swiss table](/swiss-table/).

## Pitfalls

- **Stopping only at EMPTY.** If line L3 tests only $T[j] = $ EMPTY, the search is still correct, but it loses the early stop, and unsuccessful searches cost as much as in plain linear probing.
- **Emptying the slot without a shift.** If RH-DELETE writes EMPTY at the slot of $k$ and stops after line L12, a key to the right with a positive distance is cut off from its home, and line L3 returns NIL for it. In the example, deleting 16 this way makes 24, 1 and 9 impossible to find. Use the backward shift of lines L13 to L17.
- **Shifting keys in their home slot.** If line L14 omits the test $D[i] > 0$, the shift moves a key left of its home slot, and its distance becomes $-1$, which is $m - 1$ modulo $m$; that key is then lost. Stop the shift at a key with distance 0.
- **Comparing with $\le$ in line L9.** Swapping when $D[j] = d$ is also correct for (R), but it moves keys for no gain and changes the order of keys with equal homes on each insertion. Use the strict $<$.
- **A full table.** RH-INSERT needs an EMPTY slot, and the loop of line L7 does not end without one. Grow the table before $n$ reaches $m - 1$.
- **Forgetting to move the value.** Line L9 swaps the key and the distance; in a map, the value must move with them.

## Implementations

## History

Pedro Celis, Per-Åke Larson and J. Ian Munro presented Robin Hood hashing at FOCS 1985, with a new insertion rule that cuts the variance of the search cost, and a way to delete keys. Celis's PhD thesis (University of Waterloo, 1986) gives the full analysis. Devroye, Morin and Viola (2004) proved the $\log_2 \log n \pm O(1)$ bound on the longest search for random probing. The linear probing form with backward shift deletion became popular in practice; Rust's standard hash map used it until 2019.

## References
