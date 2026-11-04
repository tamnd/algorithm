---
tag: W6T3BN
kind: data-structure
slug: hopscotch-hashing
name: Hopscotch hashing
aliases:
- hopscotch hash table
area: data-structures/hashing
level: advanced
summary: Open addressing that bounds each key's distance from its home slot with a neighbourhood bitmap.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the number of slots, H: the neighbourhood size, α: the load factor n/m}
  time: {search: O(H), delete: O(H), insert: O(m · H), expected: O(H/(1 − α)^2 + 1)}
  space: {extra: Θ(m)}
prereqs: [hash-table, open-addressing, load-factor]
see_also: [linear-probing, robin-hood-hashing, cuckoo-hashing, swiss-table, linear-probing-analysis, primary-clustering, rehashing, concurrent-hash-table]
sources:
  - paper: doi:10.1007/978-3-540-87779-0_24
    title: Maurice Herlihy, Nir Shavit and Moran Tzafrir, Hopscotch hashing, Distributed Computing (DISC 2008), Lecture Notes in Computer Science 5218
    locator: pages 350 to 364 (the neighbourhood, the hop bitmap, the displacement step of insert, and the concurrent version)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of linear probing (Algorithm L)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing)
---

Hopscotch hashing is an [open addressing](/open-addressing/) [hash table](/hash-table/), due to Herlihy, Shavit and Tzafrir (2008), in which each key is stored at most $H - 1$ slots after its home slot $h(k) \bmod m$. These $H$ slots are the **neighbourhood** of the home slot, and each slot keeps a bitmap of $H$ bits that marks which slots of its neighbourhood hold its own keys. A search or a delete looks only at one neighbourhood, so it takes $O(H)$ time in the worst case, and $O(1)$ when $H$ is a constant such as 32, the size of a machine word. An insert finds the nearest empty slot by [linear probing](/linear-probing/) and, while that slot is too far from the home slot, moves a key forward into it, so that the empty slot hops back towards home. If no key can move, the table grows.

## In plain words

Picture a long row of lockers. Each person has a favourite locker, and must keep their things in it or in one of the next few lockers. Each locker has a card that lists which of the next few lockers hold things of the people who like it best.

To find someone's things, read the card of their favourite locker and open only the lockers it lists. That takes a few looks, however full the row is.

To store new things, walk along the row to the first empty locker. If it is too far, look at the lockers just before it, find someone whose things can move into the empty one and still be near their own favourite, and move them. Now the empty locker is closer. Repeat until it is close enough. If nobody can move, build a longer row.

## The abstract type

Hopscotch hashing implements the [dictionary](/dictionary/) abstract type. It keeps a finite map $D$ from keys to values, with distinct keys, and supports:

- `insert(T, k, v)`: set $D(k) = v$. If $k$ is already a key, its value is replaced.
- `search(T, k)`: return $D(k)$, or NIL if $k$ is not a key.
- `delete(T, k)`: remove $k$ and its value, if $k$ is a key.
- `size(T)`: return the number $n$ of keys.

Like each hash table, it needs only an equality test and a [hash function](/hash-function/) on the keys, and it does not support ordered queries.

## Representation

The table has $m$ slots, numbered $0, \ldots, m-1$, and a fixed neighbourhood size $H$ with $1 \le H \le m$. Slot $s$ holds either nothing (it is empty) or one pair $(k, v)$. The **home** of a key is $\mathrm{home}(k) = h(k) \bmod m$, and the **distance** of slot $s$ from slot $i$ is $(s - i) \bmod m$, so the array wraps around. The neighbourhood of slot $i$ is the set of the $H$ slots at distance $0, 1, \ldots, H - 1$ from $i$. Each slot $i$ also has a bitmap $\mathrm{hop}[i]$ of $H$ bits. The count $n$ is the number of pairs.

**Invariant.**

- **(P1) Neighbourhood.** Each key in slot $s$ has $(s - \mathrm{home}(k)) \bmod m < H$.
- **(P2) Bitmap.** For each slot $i$ and each $d < H$, bit $d$ of $\mathrm{hop}[i]$ is 1 exactly when slot $(i + d) \bmod m$ holds a key whose home is $i$.
- **(P3) Distinct keys and count.** No key is in two slots, and $n$ is the number of full slots.

The map of the table is the set $D$ of the pairs in full slots. By (P3) it is a function. By (P1) and (P2), the keys with home $i$ are exactly the keys in the slots that the set bits of $\mathrm{hop}[i]$ point to.

## Operations

Search and delete read one bitmap. Insert first checks whether the key is there, then calls HOP-PLACE, which can fail; then the table grows and tries again.

```pseudo id=main
HOP-INSERT(T, k, v)
L1  i ← h(k) mod T.m
L2  for d ← 0 to H − 1 do
L3      if bit d of T.hop[i] = 1 and slot (i + d) mod T.m holds k then set its value to v; return
L4  while HOP-PLACE(T, k, v) = FAIL do RESIZE(T, 2 · T.m)
L5  T.n ← T.n + 1

HOP-PLACE(T, k, v)
L6  i ← h(k) mod T.m
L7  e ← 0; while e < T.m and slot (i + e) mod T.m is full do e ← e + 1
L8  if e = T.m then return FAIL
L9  while e ≥ H do
L10     j ← (i + e) mod T.m
L11     find the largest t in 1 … H − 1, and for it the smallest d < t, with bit d of T.hop[(j − t) mod T.m] = 1
L12     if there is no such pair (t, d) then return FAIL
L13     b ← (j − t) mod T.m; s ← (b + d) mod T.m
L14     move the pair in slot s to slot j; in T.hop[b] clear bit d and set bit t
L15     e ← e − (t − d)
L16 put (k, v) in slot (i + e) mod T.m; set bit e of T.hop[i]; return OK

HOP-SEARCH(T, k)
L17 i ← h(k) mod T.m
L18 for d ← 0 to H − 1 do
L19     if bit d of T.hop[i] = 1 and slot (i + d) mod T.m holds k then return its value
L20 return NIL

HOP-DELETE(T, k)
L21 i ← h(k) mod T.m
L22 for d ← 0 to H − 1 do
L23     if bit d of T.hop[i] = 1 and slot (i + d) mod T.m holds k then
L24         make the slot empty; clear bit d of T.hop[i]; T.n ← T.n − 1; return

RESIZE(T, m′)
L25 P ← the list of the pairs of T
L26 repeat
L27     make T an empty table of m′ slots, with all bitmaps 0
L28     ok ← true; for each (k, v) in P do if HOP-PLACE(T, k, v) = FAIL then ok ← false and stop the loop
L29     m′ ← 2m′
L30 until ok
```

**Search.** Line L17 finds the home slot. Lines L18 and L19 compare $k$ only with the keys at the set bits of $\mathrm{hop}[i]$, at most $H$ of them. By (P1) and (P2), these are all the keys with home $i$, so if $k$ is not among them, line L20 is right.

**Delete.** Lines L21 to L24 find $k$ the same way, empty its slot and clear its bit. No other key moves. Unlike linear probing, a delete needs no [tombstone](/tombstone/), because a search does not stop at empty slots: it reads the bitmap.

**Place.** Line L7 is a linear probe from the home slot to the first empty slot, at distance $e$. If the whole table is full, line L8 fails. If $e < H$, the empty slot is in the neighbourhood and line L16 uses it. Otherwise the loop of lines L9 to L15 brings the empty slot $j$ closer. It looks at the $H - 1$ slots just before $j$, the farthest one first, for a slot $b$ that has a key with home $b$ placed before $j$, at distance $d < t$ from $b$, where $t$ is the distance from $b$ to $j$. Moving that key to $j$ keeps it in its neighbourhood, because $t < H$. Its old slot $s$ is now empty, and it is $t - d \ge 1$ slots closer to $i$. If no key before $j$ can move, line L12 fails, and the keys moved so far stay where they are, which keeps the invariant.

**Insert.** Lines L1 to L3 replace the value if $k$ is a key. Otherwise line L4 calls HOP-PLACE, and while it fails, RESIZE doubles the number of slots and puts all pairs in again. RESIZE itself repeats with a larger size if one of its placements fails.

## Example

Take $m = 10$, $H = 3$ and $h(k) = k$, so the home slot is $k \bmod 10$. A bitmap is written with bit 0 first, so $\mathrm{hop}[2] = 011$ means that slots 3 and 4 hold keys with home 2. Insert 20, 31, 41, 13, 22, 15, 52 and 62.

| step | home | first empty slot, distance $e$ | moves | slots $0, 1, \ldots, 9$ |
|---|---|---|---|---|
| insert 20 | 0 | 0, $e = 0$ | | 20 . . . . . . . . . |
| insert 31 | 1 | 1, $e = 0$ | | 20 31 . . . . . . . . |
| insert 41 | 1 | 2, $e = 1$ | | 20 31 41 . . . . . . . |
| insert 13 | 3 | 3, $e = 0$ | | 20 31 41 13 . . . . . . |
| insert 22 | 2 | 4, $e = 2$ | | 20 31 41 13 22 . . . . . |
| insert 15 | 5 | 5, $e = 0$ | | 20 31 41 13 22 15 . . . . |
| insert 52 | 2 | 6, $e = 4$ | 15 from 5 to 6, then 13 from 3 to 5 | 20 31 41 52 22 13 15 . . . |
| insert 62 | 2 | 7, $e = 5$ | 15 from 6 to 7, then fail | grow to $m = 20$ |

The insert of 52 shows the hops. Slot 6 is at distance 4 from home slot 2, and $4 \ge H$. Before slot 6, slot 4 has no key of its own ($\mathrm{hop}[4] = 000$), but slot 5 holds 15, whose home is 5, at distance 0. So 15 moves to slot 6, and slot 5 is empty, at distance 3. Before slot 5, slot 3 holds 13 at distance 0 from its home 3, so 13 moves to slot 5, which is at distance $2 < H$ from 3. Now slot 3 is empty, at distance 1 from home 2, and 52 goes there. The bitmaps are now $\mathrm{hop}[2] = 011$ (slots 3 and 4, keys 52 and 22), $\mathrm{hop}[3] = 001$ (slot 5, key 13) and $\mathrm{hop}[5] = 010$ (slot 6, key 15).

The insert of 62 fails in the table of 10 slots, although 4 slots are empty. Slot 7 is at distance 5. First 15 moves from slot 6 to slot 7, so slot 6 is empty, at distance 4. The slots before it are 4, which has no key of its own, and 5, which has no key of its own either: slot 5 holds 13, whose home is 3, and slot 6 is at distance 3 from slot 3, outside its neighbourhood. So line L12 fails, and RESIZE builds a table of 20 slots. With homes $k \bmod 20$, the pairs go to slots 0 (20), 1 (41), 2 (22), 11 (31), 12 (52), 13 (13) and 15 (15), and then 62, with home 2, goes to slot 3, at distance 1.

Then search for 13: $\mathrm{hop}[13] = 100$, so the search looks at slot 13 only and finds it. A search for 42 reads $\mathrm{hop}[2] = 110$, compares with 22 and 62 in slots 2 and 3, and returns NIL. A delete of 41 empties slot 1 and clears bit 0 of $\mathrm{hop}[1]$.

## Correctness

The key facts are (P1) and (P2): together they say that the keys with home $i$ are exactly the keys at the set bits of $\mathrm{hop}[i]$, so search and delete need to look at one neighbourhood only. A displacement moves a key with home $b$ from distance $d$ to distance $t < H$ of $b$, and moves its bit from $d$ to $t$, so it keeps (P1) and (P2), and it does not change the map. Each displacement brings the empty slot at least one slot closer, so HOP-PLACE ends. When the empty slot is at distance $e < H$, the new key goes there, with bit $e$ of its home. Insert adds a key only after the search of lines L2 and L3 shows that it is absent, which keeps (P3). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Worst case.** Search and delete test at most $H$ bits and compare $k$ with at most $H$ keys, so they take $O(H)$ time. With $H$ at most the word size $w$, the set bits of a bitmap can be found with word operations, and $H = 32$ is the usual choice. In HOP-PLACE, line L7 probes at most $m$ slots, and each pass of the loop L9 to L15 lowers $e$ by at least 1, so there are at most $m$ passes. Each pass looks at $H - 1$ bitmaps; with word operations, the test of line L11 for one bitmap is a mask and a test for a nonzero word, so a pass takes $O(H)$ time. So HOP-PLACE takes $O(mH)$ time in the worst case, and a resize takes $O(m'H)$ for each attempt, plus the cost of the failed attempts.

**Expected case.** With no deletes and no failed placements, a hopscotch table and a linear-probing table that receive the same keys in the same order have the same set of full slots: line L7 finds the same first empty slot, and the moves only shuffle keys among full slots, so the net effect of an insert is to fill that slot. So the distance $e$ is the length of an unsuccessful search of linear probing, minus 1. By Knuth's analysis of linear probing, with home slots that are independent and uniform, an unsuccessful search makes about $\frac{1}{2}(1 + 1/(1 - \alpha)^2)$ probes in expectation: 2.5 at $\alpha = 0.5$, 8.5 at $\alpha = 0.75$, and 50.5 at $\alpha = 0.9$. See the [analysis of linear probing](/linear-probing-analysis/). So HOP-PLACE takes $O(1 + H/(1 - \alpha)^2)$ expected time, for a fixed $\alpha < 1$. This does not count the resizes; how often an insert fails depends on $H$ and $\alpha$, and the paper studies it by experiment. The argument is in [the complexity proof](proofs/complexity.md).

| operation | worst case | expected (random homes, $\alpha < 1$ fixed) |
|---|---|---|
| search | $O(H)$ | $O(H)$, and $O(1)$ for constant $H$ |
| delete | $O(H)$ | $O(H)$ |
| insert, without resize | $O(mH)$ | $O(1 + H/(1 - \alpha)^2)$ |
| resize to $m'$ slots | $O(m'H)$ for each attempt | |
| space | $m$ slots and $m$ bitmaps of $H$ bits | |

These bounds hold on the [word RAM](/word-ram/) when the hash value and one key comparison cost $O(1)$ and $H \le w$.

## Variants

- **Concurrent hopscotch hashing.** Herlihy, Shavit and Tzafrir designed the table for multicore machines. Their concurrent version splits the table into segments with a lock each, and lets a search run without taking a lock; a search that may have missed a key because of a concurrent move detects this and retries. See [concurrent hash table](/concurrent-hash-table/).
- **The choice of $H$.** With $H = 32$ or 64, each bitmap is one machine word, and a neighbourhood of small keys fits in one or two cache lines, so a search touches very little memory. A larger $H$ makes failed inserts rarer, at the cost of longer searches.
- **Neighbours of other methods.** [Robin Hood hashing](/robin-hood-hashing/) also bounds how far keys are from home in practice, by reordering runs of linear probing, but it has no hard bound. [Cuckoo hashing](/cuckoo-hashing/) gives each key two possible slots and moves keys between them. The [Swiss table](/swiss-table/) keeps a byte of metadata for each slot and probes groups of slots with SIMD instructions.

## When to use it

Use hopscotch hashing when searches are much more common than inserts, the table should run at a high [load factor](/load-factor/), and you want each search to touch a fixed, small region of memory. It keeps the cache behaviour of [linear probing](/linear-probing/) while removing the long searches caused by [primary clustering](/primary-clustering/). Use plain linear probing, or Robin Hood hashing, when inserts are common and the extra bitmap and the moves do not pay off. Use [cuckoo hashing](/cuckoo-hashing/) when you want at most two memory accesses per search and can afford a lower load factor. Use [separate chaining](/separate-chaining/) when the records are large or the load factor can exceed 1.

## Pitfalls

- **Searching past the neighbourhood.** A search that probes until an empty slot, as in linear probing, is wrong after deletes and wasteful before them. The search must read the bitmap of the home slot and stop after $H$ slots.
- **Moving a key out of its neighbourhood.** In line L11, the key must be at distance $d < t$ from its home $b$, that is, before the empty slot $j$, and $j$ must be at distance $t < H$ from $b$. Picking any key in the $H - 1$ slots before $j$ breaks (P1): in the example, moving 13 from slot 5 to slot 6 would put it at distance 3 from its home.
- **Forgetting the bitmap of the moved key.** Each move changes two bits of $\mathrm{hop}[b]$, the bitmap of the moved key's home, not the bitmap of the key being inserted.
- **Growth that never succeeds.** If more than $H$ keys have the same hash value $h(k)$, they have the same home in every table size, and no size can hold them. Even fewer keys with nearby hash values can make RESIZE fail at every size. A practical table then changes its hash function, for example with a new random seed; the Python version gives up with an error.
- **Wrap-around.** Distances are taken mod $m$. The neighbourhood of a slot near the end of the array goes on at slot 0, and the bit for slot $s$ in $\mathrm{hop}[i]$ is bit $(s - i) \bmod m$.

## Implementations

The Python version stores the bitmaps as integers and takes the hash function as a parameter, with the built-in `hash` as the default, so for a small non-negative `int` the home slot is $k \bmod m$ and the tests can follow the example. It scans the bits one at a time, which costs $O(H^2)$ for each pass of the loop instead of $O(H)$ with word operations. Insert raises `OverflowError` when more than $H$ keys share one hash value, or when the table would pass $2^{20}$ slots.

## History

Maurice Herlihy, Nir Shavit and Moran Tzafrir introduced hopscotch hashing at the DISC conference in 2008. The name refers to the children's game. Their aim was a resizable hash table for multicore machines that keeps the cache benefits of linear probing at high load factors, and the paper gives both a sequential and a concurrent version, with experiments on multicore machines. The analysis of the linear probe that HOP-PLACE starts with is Knuth's analysis of linear probing, given in Section 6.4 of his Volume 3.

## References
