---
tag: E023N7
kind: algorithm
slug: coalesced-hashing
name: Coalesced hashing
aliases:
- coalesced chaining
area: data-structures/hashing
level: advanced
summary: Hybrid of chaining and open addressing in which chains share the table space.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys in the table, m: the number of slots, α: the load factor n/m}
  time: {expected: O(1), worst: Θ(n)}
  space: {extra: Θ(m)}
prereqs: [separate-chaining, open-addressing, hash-function, collision-resolution]
see_also: [hash-table, linear-probing, double-hashing, load-factor, hash-collision, linked-list, uniform-hashing-assumption]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), Algorithm C (chained hash table search and insertion) and its analysis
  - paper: doi:10.1145/358728.358745
    title: Jeffrey Scott Vitter, Implementations for coalesced hashing, Communications of the ACM 25(12), 1982
    locator: pages 911 to 926
  - paper: doi:10.1145/322374.322375
    title: Jeffrey Scott Vitter, Analysis of the search performance of coalesced hashing, Journal of the ACM 30(2), 1983
    locator: pages 231 to 258
  - paper: doi:10.1145/368336.368352
    title: F. A. Williams, Handling identifiers as internal symbols in language processors, Communications of the ACM 2(6), 1959
    locator: pages 21 to 24
---

Coalesced hashing is a method of [collision resolution](/collision-resolution/) that keeps the chains of [separate chaining](/separate-chaining/) inside the table itself, as in [open addressing](/open-addressing/). Each slot holds a key and a link to the next slot of its chain. A key that collides goes into a free slot of the table and is linked to the end of the chain of its home slot. Chains of different home slots can merge, or *coalesce*, but they stay short: with a random [hash function](/hash-function/), a search takes at most about 2.1 probes in expectation even when the table is full. The method needs no memory outside the table and no tombstones for the insert and search operations.

## In plain words

All keys live in one array, and each slot also has room for an arrow to another slot. A key first tries its home slot. If the home slot is taken, the key follows the arrows from there to the end of the chain, takes the highest free slot of the array, and the last slot of the chain gets an arrow to it.

A search starts at the home slot and follows the arrows. It never looks at slots outside the chain, so it is fast even when the table is almost full.

Sometimes a key has to start its chain at a slot that a key from another chain already took. Then the two chains join into one, and a search for either kind of key walks through both. This joining is the "coalescing". It makes the chains a little longer, but the effect is small.

## The problem

The algorithm keeps a [dictionary](/dictionary/) of distinct keys with values under insert and search, which is the [dictionary problem](/dictionary-problem/) without deletions. The table has $m$ slots $0, \ldots, m - 1$. Slot $i$ has the fields $\mathit{key}[i]$ (a key or EMPTY), $\mathit{val}[i]$ and $\mathit{next}[i]$ (a slot index or NIL). A hash function $h$ maps each key to a home slot in $\{0, \ldots, m - 1\}$. A pointer $r$ starts at $m$ and only moves down; it marks the part of the table that is known to be full.

## The algorithm

```pseudo id=main
COALESCED-INSERT(T, k, v)
L1  i ← h(k)
L2  if T.key[i] = EMPTY then T.key[i] ← k; T.val[i] ← v; T.next[i] ← NIL; return
L3  loop
L4      if T.key[i] = k then T.val[i] ← v; return
L5      if T.next[i] = NIL then exit the loop
L6      i ← T.next[i]
L7  repeat T.r ← T.r − 1 until T.r < 0 or T.key[T.r] = EMPTY
L8  if T.r < 0 then error "the table is full"
L9  T.next[i] ← T.r; i ← T.r
L10 T.key[i] ← k; T.val[i] ← v; T.next[i] ← NIL

COALESCED-SEARCH(T, k)
L11 i ← h(k)
L12 if T.key[i] = EMPTY then return NIL
L13 while i ≠ NIL do
L14     if T.key[i] = k then return T.val[i]
L15     i ← T.next[i]
L16 return NIL
```

**Insert.** If the home slot is free, line L2 stores the key there. Otherwise lines L3 to L6 walk the chain from the home slot to its last slot, and line L4 replaces the value if the key is already present. Line L7 moves $r$ down to the highest EMPTY slot below its old value. Line L9 links the last slot of the chain to slot $r$, and line L10 stores the key there.

**Search.** Lines L11 to L16 start at the home slot and follow the links. If the home slot is EMPTY, no key with this home exists, because an insert always fills its home slot first or finds it already full.

This is the late-insertion form, Knuth's Algorithm C: the new key goes at the end of the chain. The free slots are taken from the top of the table down, so the slots near the top fill first and act as an overflow area.

## Example

Let $m = 11$ and $h(k) = k \bmod 11$. Insert 27, 18, 29, 28, 39, 13, 16, 38 and 21. A dot is an EMPTY slot, and $x{\to}j$ means key $x$ with a link to slot $j$.

| key | home | slots visited | $r$ after | table, slots 0 to 10 |
|---|---|---|---|---|
| 27 | 5 | 5 | 11 | . . . . . 27 . . . . . |
| 18 | 7 | 7 | 11 | . . . . . 27 . 18 . . . |
| 29 | 7 | 7, then 10 | 10 | . . . . . 27 . 18→10 . . 29 |
| 28 | 6 | 6 | 10 | . . . . . 27 28 18→10 . . 29 |
| 39 | 6 | 6, then 9 | 9 | . . . . . 27 28→9 18→10 . 39 29 |
| 13 | 2 | 2 | 9 | . . 13 . . 27 28→9 18→10 . 39 29 |
| 16 | 5 | 5, then 8 | 8 | . . 13 . . 27→8 28→9 18→10 16 39 29 |
| 38 | 5 | 5, 8, then 4 | 4 | . . 13 . 38 27→8 28→9 18→10 16→4 39 29 |
| 21 | 10 | 10, then 3 | 3 | . . 13 21 38 27→8 28→9 18→10 16→4 39 29→3 |

For 38, line L7 moves $r$ from 8 down past the occupied slots 7, 6 and 5 to slot 4. Key 21 has home slot 10, but key 29, whose home is 7, already took it. So 21 joins the chain $7 \to 10$ and makes it $7 \to 10 \to 3$: the chains of homes 7 and 10 have coalesced. A search for 21 visits slots 10 and 3. A search for the absent key 40, with home 7, visits 7, 10 and 3, one probe more than it would need without the coalescing. A search for 33 finds its home slot 0 EMPTY and stops after one probe.

## Correctness

The algorithm keeps this invariant:

- **(C1)** For each stored key $k$, the home slot $h(k)$ is occupied, and the slot of $k$ is reached from $h(k)$ by following links.
- **(C2)** Each link goes from an occupied slot to an occupied slot, each slot has at most one incoming link, and the links form no cycle.
- **(C3)** No key is stored twice.
- **(C4)** Each slot with index at least $r$ is occupied.

By (C1), a search that follows the links from $h(k)$ meets $k$ if it is present, and by (C2) the walk ends at a NIL link after at most $n$ steps. Insert adds a new key only after the walk shows that it is absent, so (C3) holds. The new slot was EMPTY, so it had no incoming link and no outgoing link, and linking it after the last slot of a chain makes no cycle. By (C4), line L8 reports a full table only when all $m$ slots are occupied. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Worst case.** If all keys have the same home slot, they form one chain, and the $j$-th insert walks $j - 1$ slots. Line L7 moves $r$ down by at most $m$ in total over all inserts, because $r$ never moves up. So a search or an insert takes $\Theta(n)$ time in the worst case, and $n$ inserts take $O(n^2 + m)$ time in total.

**Expected case.** Assume that each key is hashed independently and uniformly to one of the $m$ slots, and count a probe for each slot whose key is examined (one probe for an EMPTY home slot). Knuth derives the expected number of probes of Algorithm C, for $n$ keys and $\alpha = n/m$, as $m \to \infty$:

$$C'(\alpha) \approx 1 + \tfrac{1}{4}\big(e^{2\alpha} - 1 - 2\alpha\big) \quad \text{(search that fails)},$$

$$C(\alpha) \approx 1 + \tfrac{1}{8\alpha}\big(e^{2\alpha} - 1 - 2\alpha\big) + \tfrac{\alpha}{4} \quad \text{(search that succeeds)}.$$

Both are increasing in $\alpha$ and finite at $\alpha = 1$: $C'(1) \approx 2.10$ and $C(1) \approx 1.80$. So for each $\alpha \le 1$ the expected cost of a search, and of an insert, which costs a search that fails plus the move of $r$, is $O(1)$. For $\alpha = 0.5$ the values are about 1.18 and 1.30, and for $\alpha = 0.9$ about 1.81 and 1.68. The derivation counts the expected number of chains of each length; it is in Knuth Section 6.4, and Vitter (1983) extends it to the variants with a cellar. The [complexity notes](proofs/complexity.md) give the worst-case proof and the outline of the expected-case one.

**Space.** The table uses $m$ slots, each with a key, a value and a link, so $\Theta(m)$ space, and no memory outside the table.

| operation | worst case | expected, random hashing |
|---|---|---|
| search, key absent | $\Theta(n)$ | about $1 + \frac{1}{4}(e^{2\alpha} - 1 - 2\alpha)$ probes, at most about 2.10 |
| search, key present | $\Theta(n)$ | about $1 + \frac{1}{8\alpha}(e^{2\alpha} - 1 - 2\alpha) + \frac{\alpha}{4}$ probes, at most about 1.80 |
| insert | $\Theta(n)$ plus the move of $r$ | $O(1)$ |
| space | $\Theta(m)$ | |

## Properties

- **Works up to a full table.** Unlike [linear probing](/linear-probing/), the cost stays bounded as $\alpha \to 1$, because a search follows only its chain.
- **No outside memory.** Unlike separate chaining, no nodes are allocated, and the links are small integers.
- **Deletion is hard.** Removing a key from a chain can cut off keys of other chains that coalesced into it. A tombstone works, or the affected chain can be rebuilt. Knuth (Section 6.4) and Vitter (1982) discuss deletion algorithms for the method.
- **The free-slot pointer only moves down.** This makes the total cost of line L7 over all inserts $O(m)$, but slots freed by a deletion above $r$ are not found again without extra work.

## Variants and improvements

- **Coalesced hashing with a cellar.** Hash only into the first $m'$ slots, the address region, and keep the other $m - m'$ slots as a cellar for collisions. Line L7 then takes free slots from the cellar first. A cellar of the right size makes coalescing rare. Vitter showed that an address factor $m'/m$ of about 0.86 gives close to the best search cost over a wide range of load factors.
- **Early insertion.** Put the new key right after the home slot in its chain, not at the end. This shortens successful searches when the home slot is the start of the chain.
- **Varied insertion.** A mix of late and early insertion that inserts after the last key of the chain that lies in the cellar; it was studied in later work of Chen and Vitter.
- **Separate chaining.** [Separate chaining](/separate-chaining/) keeps each chain apart in allocated nodes, so chains never coalesce, at the cost of a pointer and an allocation for each key.

## When to use it

Use coalesced hashing when the table lives in a fixed block of memory, such as a file or an embedded system, must fill to a high load factor, and sees few deletions. Its search cost at $\alpha = 1$ is about 2 probes, while linear probing at $\alpha = 0.9$ already needs about 50 probes for a search that fails. Prefer separate chaining when deletions are frequent or memory can be allocated freely, and prefer [linear probing](/linear-probing/) or [double hashing](/double-hashing/) at moderate load, where their simpler slots and better cache use win.

## Pitfalls

- **Searching from the end of the table.** A search must start at the home slot $h(k)$ (line L11), not at slot $r$ or at the start of some chain. Starting elsewhere misses keys whose chain begins at the home slot.
- **Deleting by clearing the slot.** Writing EMPTY into the slot of a deleted key cuts the chain: in the example, deleting 29 that way makes slot 10 EMPTY, and the search for 21 then stops at its EMPTY home slot and fails. Use a tombstone, or rebuild the chain.
- **Resetting $r$ without care.** If a deletion frees a slot above $r$ and code later resets $r$ to $m$, line L7 is still correct but loses its $O(m)$ total bound. If code instead lets $r$ skip a free slot, invariant (C4) breaks and line L8 can report a full table that is not full.
- **Linking from the home slot instead of the chain end.** Line L9 must link from the last slot of the chain that the walk of lines L3 to L6 reached. Linking from the home slot overwrites the old link and loses the rest of the chain.

## Implementations

The Python version follows lines L1 to L16. It adds a delete that rebuilds the whole table without the key, in $O(m)$ time plus the reinserts, which keeps the invariant simple.

## History

Williams described in 1959 a table in which overflow records are linked into the free slots of the table, the idea of coalesced chaining. Knuth gives the method as Algorithm C in Section 6.4, with the analysis of its expected cost. Vitter, in papers from 1980 to 1983, studied the choice of the cellar size and analysed the search cost of the variants.

## References
