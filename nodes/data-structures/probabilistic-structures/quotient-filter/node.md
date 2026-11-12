---
tag: 44MVA2
kind: data-structure
slug: quotient-filter
name: Quotient filter
area: data-structures/probabilistic-structures
level: advanced
summary: Compact approximate set storing quotient and remainder bits in a cache-friendly table.
model: word-ram
complexity:
  vars: {n: the number of stored keys, q: the quotient bits, r: the remainder bits, C: the length of the cluster of the key}
  time: {worst: Θ(C)}
  space: {extra: Θ(2^q (r + 3))}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [approximate-membership, linear-probing, fingerprinting, false-positive-rate]
see_also: [cuckoo-filter, bloom-filter, counting-bloom-filter, robin-hood-hashing, log-structured-merge-tree, compressed-data-structure]
sources:
  - paper: doi:10.14778/2350229.2350275
    title: Michael A. Bender, Martin Farach-Colton, Rob Johnson, Russell Kraner, Bradley C. Kuszmaul, Dzejla Medjedovic, Pablo Montes, Pradeep Shetty, Richard P. Spillane and Erez Zadok, Don't thrash, how to cache your hash on flash, PVLDB 5(11), 2012
    locator: pages 1627 to 1637, Section 3 (the quotient filter, the three metadata bits, lookup, insert and delete, merging and resizing)
  - paper: doi:10.1109/tc.1984.1676499
    title: John G. Cleary, Compact hash tables using bidirectional linear probing, IEEE Transactions on Computers C-33(9), 1984
    locator: pages 828 to 834 (storing only the remainder of a key, with its quotient given by the position and a few extra bits)
  - paper: doi:10.1145/3035918.3035963
    title: Prashant Pandey, Michael A. Bender, Rob Johnson and Rob Patro, A general-purpose counting filter, making every bit count, SIGMOD 2017
    locator: pages 775 to 787 (the counting quotient filter with rank and select metadata)
---

A quotient filter stores a fingerprint of $q + r$ bits for each key in a table of $2^q$ slots. The top $q$ bits, the *quotient*, choose the slot where the fingerprint belongs, and only the other $r$ bits, the *remainder*, are stored. Fingerprints with the same quotient form a sorted *run*, and runs that collide are shifted to the right as in [linear probing](/linear-probing/). Three metadata bits per slot are enough to find the run of any quotient, so each slot costs $r + 3$ bits, and the false positive rate is at most $\alpha 2^{-r}$ at load $\alpha$. Unlike a [Bloom filter](/bloom-filter/), it supports deletes, it can be resized and merged without the original keys, and its accesses go to consecutive memory. The idea of storing only the remainder is due to Cleary (1984); Bender et al. (2012) made it a filter.

## In plain words

Each key is turned into a number with, say, 16 bits. The first 10 bits say which of 1024 boxes the number belongs in, so they need not be written down: the box itself records them. Only the last 6 bits are written in the box.

Two numbers can want the same box. Then the second one goes to the next box, and others move to make room, as when people sit along a bench. The numbers that want the same box stay together and in order.

Each box keeps three small flags: whether some number wants this box, whether this box continues the group to its left, and whether its number was pushed from its own box. With these flags a lookup walks a short way along the bench to find the group that the key's number belongs to, and checks it.

## The abstract type

The filter solves the dynamic version of the [approximate membership problem](/approximate-membership/) for a multiset $S$ of keys. INSERT$(x)$ adds a copy of $x$, or reports that the table is full. DELETE$(x)$ removes a copy of $x$, and is allowed only when $x$ has a copy in $S$. QUERY$(x)$ returns true for each $x$ in $S$, and returns true for an $x$ not in $S$ with probability at most $n/2^{q+r}$.

## Representation

The table has $m = 2^q$ slots, numbered modulo $m$, so slot $m - 1$ is followed by slot 0. A hash function gives each key a fingerprint $F(x)$ of $q + r$ bits, with quotient $f_q = \lfloor F/2^r \rfloor$ and remainder $f_r = F \bmod 2^r$. Each slot $p$ has a remainder field of $r$ bits and three bits:

- `occupied[p]`: some stored fingerprint has quotient $p$. This bit belongs to the slot as a canonical position, not to what the slot holds.
- `continuation[p]`: the slot holds a remainder that is not the first of its run.
- `shifted[p]`: the slot holds a remainder whose quotient is not $p$.

A slot is empty exactly when its three bits are 0.

**Invariant (Q).** The stored fingerprints form the multiset of fingerprints of $S$, and:
1. For each quotient $Q$ with `occupied[Q]` = 1, its remainders fill a *run* of consecutive slots in sorted order, the first with `continuation` = 0 and the others with `continuation` = 1.
2. A *cluster* is a maximal sequence of non-empty slots. Its first slot $c$ holds the start of the run of quotient $c$. In a cluster the runs follow each other in the order of their quotients, and each run starts at a slot at or after its quotient.
3. `shifted[p]` = 1 exactly when slot $p$ holds a remainder whose quotient is not $p$.
4. At least one slot is empty.

So the layout is the one that linear probing gives when the fingerprints are inserted in sorted order, and it depends only on the multiset.

## Operations

```pseudo id=main
QUERY(x)
L1  (f_q, f_r) ← F(x); if occupied[f_q] = 0 then return false
L2  b ← f_q; while shifted[b] do b ← b − 1              ▷ back to an unshifted slot
L3  s ← b                                              ▷ s: the start of the run of b
L4  while b ≠ f_q do                                   ▷ one run for each occupied quotient
L5      repeat s ← s + 1 until continuation[s] = 0     ▷ next run start
L6      repeat b ← b + 1 until occupied[b] = 1         ▷ next occupied quotient
L7  repeat                                             ▷ s is the start of the run of f_q
L8      if remainder[s] = f_r then return true
L9      s ← s + 1
L10 until continuation[s] = 0; return false

INSERT(x)
L11 b ← f_q; while shifted[b] do b ← b − 1
L12 E ← the fingerprints stored from slot b to the next empty slot
L13 add (f_q, f_r) to E
L14 write E back from slot b in sorted order, each run at max(its quotient, end of the previous run + 1)

DELETE(x)                                              ▷ precondition: x is in S
L15 b, E as in lines L11 and L12
L16 remove one copy of (f_q, f_r) from E
L17 write E back from slot b as in line L14, and clear the slots left over
```

All indices are modulo $m$.

**Query.** Line L2 walks left to a slot $b$ whose remainder is not shifted. That slot is the start of the run of quotient $b$, and nothing to its left affects the runs to its right. Lines L4 to L6 then walk right in step: $b$ moves over the occupied quotients and $s$ over the run starts. When $b$ reaches $f_q$, $s$ is the start of the run of $f_q$, and lines L7 to L10 scan that run.

**Insert and delete.** Lines L11 to L17 rewrite the part of the cluster from the unshifted slot $b$ to the next empty slot. The fingerprints there are the runs of the occupied quotients in that part, in order, so they can be read back, changed, and written again. An insert can fill the empty slot at the end and join two clusters. A delete can leave a gap and split a cluster. The Python code does exactly this; an optimized code moves the remainders one slot in place and updates the bits, with the same result.

## Example

Take $q = 3$ and $r = 3$, so 8 slots, and these fingerprints, written as (quotient, remainder).

| key | a | b | c | d | e | f | g | x |
|---|---|---|---|---|---|---|---|---|
| $F$ | (1, 5) | (1, 2) | (2, 7) | (4, 3) | (3, 1) | (7, 6) | (7, 4) | (2, 1) |

Insert a, b, c, d, e. Quotient 1 has the run 2, 5 at slots 1 and 2. The run of quotient 2 must start after it, at slot 3, and so must the runs of 3 and 4, at slots 4 and 5. Then insert f and g: the run 4, 6 of quotient 7 fills slot 7 and wraps to slot 0. The bits are (occupied, continuation, shifted).

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| remainder | 6 | 2 | 5 | 7 | 1 | 3 | | 4 |
| bits | 011 | 100 | 111 | 101 | 101 | 001 | 000 | 100 |

Slot 2 holds the second remainder of quotient 1, so it is shifted and a continuation, but its occupied bit is 1 because quotient 2 has a run, which lives in slot 3.

- QUERY(d), with quotient 4: `occupied[4]` = 1. Slots 4, 3 and 2 are shifted, slot 1 is not, so $b = s = 1$. Then $s$ moves over the run starts 3, 4, 5 while $b$ moves over the occupied quotients 2, 3, 4. At $s = 5$ the remainder is 3, so the answer is true.
- QUERY(x), with quotient 2: the walk stops at $s = 3$, the run of quotient 2. Its only remainder is 7, not 1, and slot 4 starts a new run, so the answer is false.
- DELETE(b): the part from slot 1 is read back as (1, 5), (2, 7), (3, 1), (4, 3) and written again. Now each run starts at its own quotient, slots 1 to 4 have bits 100, and slot 5 becomes empty.

## Correctness

The query relies on two facts from invariant (Q). First, an unshifted non-empty slot $b$ holds the start of the run of $b$, and every run that starts at or after $b$ in its cluster belongs to an occupied quotient at or after $b$; so counting occupied quotients from $b$ to $f_q$ and counting run starts from $b$ meet at the run of $f_q$. Second, insert and delete rewrite a part of a cluster that begins at such a slot and ends at an empty slot, and the layout of that part depends only on the fingerprints in it. So the invariant holds after each operation, and the query returns true exactly when $(f_q, f_r)$ is stored, which includes each key of $S$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory |
|---|---|---|
| query | $O(C)$ | consecutive slots |
| insert, delete | $O(C)$ | consecutive slots |
| space | | $2^q (r + 3)$ bits |

Here $C$ is the length of the cluster of the key. The set of non-empty slots is the same as in [linear probing](/linear-probing/) with the quotients as hash values, so with ideal hashing and load $\alpha = n/2^q < 1$ the expected length of a cluster is $O(1/(1 - \alpha)^2)$, a constant for a fixed $\alpha$. All accesses are to consecutive slots, so a query usually costs one or two cache misses.

**False positive rate.** A query for $x \notin S$ returns true exactly when $F(x)$ equals a stored fingerprint. With ideal hashing $F(x)$ is uniform on $2^{q+r}$ values, so by the [union bound](/union-bound/) the rate is at most $n/2^{q+r} = \alpha 2^{-r}$. The proof is in [the complexity proof](proofs/complexity.md).

**Space per key.** At load $\alpha$, the space is $(r + 3)/\alpha$ bits per key. For a rate $\varepsilon$ take $r = \lceil \log_2(\alpha/\varepsilon) \rceil$. At $\alpha = 0.75$ and $\varepsilon = 2^{-8}$ this is $r = 8$ and 14.7 bits per key, against 11.5 for a Bloom filter. Since $1/\alpha < 1.44$ for $\alpha > 0.69$, the quotient filter needs less space than a Bloom filter only for small rates. If the rounding of $r$ is ignored, this holds at 90 percent load for rates below about $2^{-10}$, and at 75 percent load only below about $2^{-31}$; the rounding moves both limits lower. Its advantages are locality, deletes, merging and resizing.

## Variants

- **Counting quotient filter.** Pandey, Bender, Johnson and Patro (2017) replace the three bits by rank and select structures on two bit vectors, about 2.125 bits per slot, and encode repeated remainders as counters, so the filter also counts multiplicities in little space.
- **Merging.** The fingerprints can be read in sorted order of $F$, so two filters with the same $q$, $r$ and hash function merge in linear time, as in [merge sort](/merge-sort/). This makes the quotient filter fit a [log-structured merge tree](/log-structured-merge-tree/) on flash, which is the use that Bender et al. (2012) had in mind, with the buffered and cascade filters built from it.
- **Resizing.** To double the table, move the top bit of each remainder into the quotient: $q$ grows by 1 and $r$ falls by 1. The keys are not needed, and the false positive rate doubles.
- **Robin Hood layout.** The sorted runs are the layout of [Robin Hood hashing](/robin-hood-hashing/) with ties broken by remainder, which bounds the variance of the distance from each fingerprint to its slot.
- **Cuckoo filter.** The [cuckoo filter](/cuckoo-filter/) reaches higher loads, about 95 percent, with two bucket reads per query, but cannot be merged or resized without the keys.

## When to use it

Use a quotient filter when the filter lives on disk or flash, or when it must be merged, resized or scanned in order, as in storage engines with sorted runs of data. It also suits concurrent and external memory settings, because each operation touches one contiguous area. For a filter in RAM that only needs deletes at the lowest space, a cuckoo filter is often smaller. Keep the load below about 90 percent: the clusters grow like those of linear probing.

## Pitfalls

- **The occupied bit is about the slot, not its content.** `occupied[p]` says that quotient $p$ has a run somewhere, which may start far to the right of $p$. Reading it as "slot $p$ holds a fingerprint of quotient $p$" breaks the walk of lines L4 to L6.
- **A full table.** With all slots used there is no empty slot, the cluster is the whole table, and the scans of lines L12 and L2 can loop for ever. The code accepts at most $2^q - 1$ fingerprints.
- **High load.** Cluster lengths grow like $1/(1 - \alpha)^2$. At 95 percent load an insert can move hundreds of slots.
- **Deleting an absent key.** If QUERY$(x)$ is a false positive, DELETE$(x)$ removes the fingerprint of another key, which then gives a false negative. The code deletes only a fingerprint that is present, but it cannot tell whose it is.
- **Wrap-around.** Indices must be taken modulo $m$, including in the backward walk of line L2, as the example shows at slots 7 and 0.

## Implementations

The Python class follows the main block for QUERY. INSERT and DELETE decode the part of the cluster from the nearest unshifted slot, change the list of fingerprints, and write it back, which is simpler than moving slots in place and gives the same table.

## History

Cleary (1984) showed how a hash table can store only the remainder of each key, with the quotient given by the position and a few extra bits, under linear probing in both directions. Bender, Farach-Colton, Johnson and others (2012) turned this into the quotient filter, with the three metadata bits, and used it for filters that are merged on flash storage. Pandey, Bender, Johnson and Patro (2017) gave the counting quotient filter with rank and select metadata.

## References
