---
tag: HV6EG1
kind: algorithm
slug: quadratic-probing
name: Quadratic probing
aliases:
- quadratic open addressing
- quadratic probing hash table
area: data-structures/hashing
level: intro
summary: Open addressing with probe offsets that grow quadratically, which reduces primary clustering.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {m: the number of slots, a power of two, n: the number of keys}
  time: {worst: Θ(m), expected: O(1), best: Θ(1)}
  space: {extra: Θ(m)}
properties: {deterministic: true, comparison: false, recursive: false, in_place: true}
history:
  year: 1968
  people: [Ward Douglas Maurer]
  note: Maurer proposed quadratic probing in 1968. Hopgood and Davenport studied the version for tables whose size is a power of two in 1972.
prereqs: [open-addressing, probe-sequence, lazy-deletion]
see_also: [linear-probing, double-hashing, primary-clustering, secondary-clustering, swiss-table, uniform-hashing-assumption, load-factor, tombstone]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing), the part on quadratic probing
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of open addressing with secondary clustering
  - book: isbn:9780132847377
    title: Mark Allen Weiss, Data Structures and Algorithm Analysis in C++, fourth edition
    locator: Chapter 5 (Hashing), Section 5.4.2 (Quadratic Probing)
  - paper: doi:10.4230/LIPIcs.ICALP.2024.103
    title: William Kuszmaul and Zoe Xi, Towards an Analysis of Quadratic Probing, ICALP 2024
    locator: LIPIcs volume 297, paper 103
  - paper: doi:10.1145/362851.362880
    title: W. D. Maurer, An improved hash code for scatter storage, Communications of the ACM 11(1), 1968
    locator: pages 35 to 38
---

Quadratic probing is a form of [open addressing](/open-addressing/) in which the $i$-th probe for a key $k$ goes to slot $(h(k) + c(i)) \bmod m$, where the offset $c(i)$ grows as a quadratic function of $i$. The usual choice is $c(i) = i(i+1)/2$ with a table size $m$ that is a power of two: then the [probe sequence](/probe-sequence/) visits each slot exactly once in its first $m$ probes. The jumps break up the long runs of full slots that [linear probing](/linear-probing/) builds ([primary clustering](/primary-clustering/)), but two keys with the same home slot still follow the same path ([secondary clustering](/secondary-clustering/)). It solves the [dictionary problem](/dictionary-problem/) in expected $O(1)$ probes per operation at a load factor that is bounded away from 1.

## In plain words

You park in a long street with numbered places, and your ticket gives you a home place. If it is taken, linear probing tells you to try the next place, then the next. When many drivers do that, the cars bunch together in long rows, and each new driver walks along the whole row.

Quadratic probing makes the jumps larger each time: one place on, then two more, then three more, and so on. Two drivers who start at different places soon go different ways, so long rows form less often. Two drivers with the same ticket still take the same path.

To find a car, you follow the same jumps from the home place. When you reach a free place that was never used, the car is not in the street.

## The problem

Keep a set of keys, each with a value, under insert, search and delete. This is the [dictionary problem](/dictionary-problem/). The table is an array $T[0 \ldots m-1]$ of slots, with $m = 2^p$ for some $p \ge 0$. Each slot is EMPTY, DELETED (a [tombstone](/tombstone/)) or holds one key. A [hash function](/hash-function/) $h$ maps each key to a home slot $h(k) \in \{0, \ldots, m-1\}$. The $i$-th probe for $k$, for $i = 0, 1, 2, \ldots$, is

$$p_i(k) = \left(h(k) + \tfrac{i(i+1)}{2}\right) \bmod m.$$

In CLRS terms this is $h(k, i) = (h(k) + c_1 i + c_2 i^2) \bmod m$ with $c_1 = c_2 = 1/2$.

## The algorithm

The offset grows by $i + 1$ from probe $i$ to probe $i + 1$, so the code adds a counter and needs no multiplication.

```pseudo id=main
QP-SEARCH(T, k)                       ▷ return the slot of k, or NIL
L1  j ← h(k)
L2  for i ← 0 to m − 1 do
L3      if T[j] = EMPTY then return NIL
L4      if T[j] = k then return j
L5      j ← (j + i + 1) mod m             ▷ now j = h(k) + (i + 1)(i + 2)/2 mod m
L6  return NIL

QP-INSERT(T, k)                       ▷ k is not in T
L7  j ← h(k)
L8  for i ← 0 to m − 1 do
L9      if T[j] = EMPTY or T[j] = DELETED then T[j] ← k, return j
L10     j ← (j + i + 1) mod m
L11 error "the table is full"

QP-DELETE(T, k)
L12 j ← QP-SEARCH(T, k)
L13 if j ≠ NIL then T[j] ← DELETED
```

QP-SEARCH follows the probe sequence of $k$. It stops at the first EMPTY slot, because an insertion of $k$ would have used that slot. It does not stop at a DELETED slot, because $k$ can lie beyond a slot whose key was deleted later. QP-INSERT puts $k$ into the first slot that holds no key, EMPTY or DELETED. It needs the precondition that $k$ is not in $T$: a caller that wants "insert or update" runs QP-SEARCH first. QP-DELETE writes a tombstone, which is [lazy deletion](/lazy-deletion/). Writing EMPTY there would cut the probe path of each key that was inserted past this slot.

A table must not run full. In practice the table is rebuilt in a table twice as large, by [rehashing](/rehashing/), when the number of keys plus tombstones passes a fixed fraction of $m$, often $1/2$. A rebuild also removes all tombstones.

## Example

Take $m = 8$ and $h(k) = k \bmod 8$. The sequence of offsets $i(i+1)/2 \bmod 8$ for $i = 0, \ldots, 7$ is $0, 1, 3, 6, 2, 7, 5, 4$, a permutation of $0, \ldots, 7$. So the keys with home slot 2 probe $2, 3, 5, 0, 4, 1, 7, 6$, and the keys with home slot 7 probe $7, 0, 2, 5, 1, 6, 4, 3$.

| step | probes | result | $T[0 \ldots 7]$ |
|---|---|---|---|
| insert 10 | 2 | slot 2 | · · 10 · · · · · |
| insert 18 | 2, 3 | slot 3 | · · 10 18 · · · · |
| insert 26 | 2, 3, 5 | slot 5 | · · 10 18 · 26 · · |
| insert 34 | 2, 3, 5, 0 | slot 0 | 34 · 10 18 · 26 · · |
| insert 7 | 7 | slot 7 | 34 · 10 18 · 26 · 7 |
| insert 15 | 7, 0, 2, 5, 1 | slot 1 | 34 15 10 18 · 26 · 7 |
| delete 18 | 2, 3 | slot 3 becomes D | 34 15 10 D · 26 · 7 |
| search 26 | 2, 3, 5 | found at 5 | 34 15 10 D · 26 · 7 |
| search 42 | 2, 3, 5, 0, 4 | NIL (EMPTY at 4) | 34 15 10 D · 26 · 7 |
| insert 42 | 2, 3 | slot 3 | 34 15 10 42 · 26 · 7 |

Here "·" is EMPTY and "D" is DELETED. The search for 26 passes the tombstone at slot 3 and finds 26 at slot 5. If delete had written EMPTY at slot 3, that search would stop at slot 3 and fail. The four keys 10, 18, 26 and 34 share home slot 2, so they share one path, and the fourth one needs four probes: this is secondary clustering. Key 15 has another home slot, but its path still meets slots 0, 2 and 5 of the first group.

## Correctness

The proof rests on two facts. The first is arithmetic: for $m = 2^p$, the offsets $i(i+1)/2 \bmod m$ for $i = 0, \ldots, m-1$ are all different, so the first $m$ probes of each key visit every slot once. The second is an invariant of the table: for each key $k$ that sits at probe $t$ of its sequence, none of the slots $p_0(k), \ldots, p_{t-1}(k)$ is EMPTY. Insert keeps it because it only turns EMPTY or DELETED slots into full ones, and it places $k$ after full slots only. Delete keeps it because it never writes EMPTY. With the invariant, QP-SEARCH cannot stop before it reaches $k$, and by the first fact QP-INSERT finds a free slot whenever one exists. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each operation runs at most $m$ iterations of $O(1)$ work, so the worst case is $\Theta(m)$ time per operation. The worst case happens: if all keys share one home slot, the $n$-th insertion makes $n$ probes.

No exact formula for the expected cost of quadratic probing is known. Knuth analyses an idealized model of secondary clustering, in which the probe sequence depends only on the home slot, and the sequences of different home slots behave like independent random permutations. With the load factor $\alpha = n/m$, the expected number of probes in that model is about

$$C_n \approx 1 - \ln(1 - \alpha) - \frac{\alpha}{2} \quad \text{(successful search)}, \qquad C'_n \approx \frac{1}{1-\alpha} - \alpha - \ln(1-\alpha) \quad \text{(unsuccessful search)}.$$

These numbers predict quadratic probing with random home slots well. For a table of $2^{16}$ slots, filled with random home slots, the measured averages and the model are:

| $\alpha$ | successful, measured | successful, model | unsuccessful, measured | unsuccessful, model | linear probing, unsuccessful |
|---|---|---|---|---|---|
| 0.5 | 1.438 | 1.443 | 2.161 | 2.193 | 2.5 |
| 0.75 | 2.001 | 2.011 | 4.647 | 4.636 | 8.5 |
| 0.9 | 2.892 | 2.853 | 12.022 | 11.403 | 50.5 |

The last column is Knuth's formula $\frac{1}{2}(1 + 1/(1-\alpha)^2)$ for [linear probing](/linear-probing/); the gap shows what the removal of primary clustering gains. The [uniform hashing](/uniform-hashing-assumption/) bound $1/(1-\alpha)$ is $2$, $4$ and $10$ at the same load factors, so the remaining secondary clustering costs little. As a theorem about quadratic probing itself, Kuszmaul and Xi proved in 2024 that there is a positive constant load factor at which quadratic probing has $O(1)$ expected time per operation; before that, no constant bound at any load factor was proved. Their result assumes a fully random hash function, and the constant load factor it gives is small. So the expected $O(1)$ cost is a theorem for load factors below that constant, and for larger fixed load factors below 1 it is the prediction of the model and of experiments, not a theorem.

The table uses $m$ slots. Tombstones count as full slots for the cost of a search, so a table with many deletions must be rebuilt from time to time.

## Properties

- **No primary clustering.** Two keys with different home slots can meet in one slot, but their next probes differ, because they reach that slot at different probe numbers and so take steps of different length.
- **Secondary clustering.** Keys with the same home slot have the same probe sequence. [Double hashing](/double-hashing/) removes this too.
- **Cache behaviour.** The first few probes are close to the home slot, offsets 1, 3 and 6, so they often fall in the same cache line or the next one. Later probes jump far.
- **Full coverage needs the right $m$.** With $m = 2^p$ and triangular offsets, every slot is reached. With other choices of $m$ and $c(i)$ the sequence can reach only part of the table (see Pitfalls).

## Variants and improvements

- **Prime table size and $c(i) = i^2$.** If $m$ is an odd prime, the offsets $i^2 \bmod m$ for $0 \le i \le (m-1)/2$ are all different: from $i^2 \equiv j^2$ follows $m \mid (j - i)(j + i)$, which is not possible for $0 \le i < j \le (m-1)/2$. So the first $(m+1)/2$ probes are different slots, and an insertion always succeeds when fewer than $(m+1)/2$ slots hold a key, which holds when $\alpha < 1/2$. This is Theorem 5.1 in Weiss. Later probes repeat these slots, so the other half of the table is never reached.
- **Alternating signs.** The offsets $0, +1, -1, +4, -4, +9, -9, \ldots$ reach every slot when $m$ is a prime with $m \equiv 3 \pmod 4$.
- **Probing groups of slots.** The [Swiss table](/swiss-table/) uses the triangular sequence over groups of 16 slots, and tests one group at a time with vector instructions.
- **Double hashing.** Make the step depend on the key through a second hash, so that keys with the same home slot follow different paths. See [double hashing](/double-hashing/).

## When to use it

Use quadratic probing when you want the low memory and good cache use of open addressing, but linear probing clusters too much at the load factors you need, or the hash function is weak, so that keys land in runs of nearby slots. It needs only one hash value per key, unlike double hashing. If the hash function is good and the load factor is at most about $1/2$, linear probing is often faster in practice, because each probe after the first is in the next cache line. If keys are deleted often, consider [Robin Hood hashing](/robin-hood-hashing/) with backward shift, which leaves no tombstones, or [separate chaining](/separate-chaining/).

## Pitfalls

- **Offsets $i^2$ with $m$ a power of two.** If line L5 is written as $j \leftarrow (h(k) + (i+1)^2) \bmod m$ with $m = 8$, the offsets mod 8 are only $0, 1, 4$: the sequence reaches 3 slots of 8, and an insertion can fail in a table that is mostly empty. Keep the triangular step $j \leftarrow j + i + 1$ of line L5 with $m = 2^p$, or use $i^2$ only with a prime $m$ and $\alpha < 1/2$.
- **Writing EMPTY on delete.** If line L13 sets $T[j] \leftarrow$ EMPTY, a later search for a key past slot $j$ stops at line L3 and returns NIL by mistake. In the example, deleting 18 this way makes 26 impossible to find. Write DELETED, or rebuild the table.
- **Inserting without a search first.** QP-INSERT stops at the first tombstone (line L9). If the key is already in the table further along the path, the table now holds it twice, and a later delete removes only one copy. Search first, as the precondition of line L7 states.
- **Counting only the keys.** If the rebuild test counts only keys and not tombstones, a table with many deletions fills with DELETED slots, and unsuccessful searches scan the whole table at line L2. Count keys plus tombstones.
- **A table size that is not a power of two.** Line L5 reaches all slots only for $m = 2^p$. For $m = 6$, for example, the triangular offsets mod 6 are $0, 1, 3, 0, 4, 3$, so slots at offsets 2 and 5 are never probed.

## Implementations

## History

Maurer proposed quadratic probing in 1968 in Communications of the ACM, as a way to avoid the clustering of linear probing. Hopgood and Davenport (1972) studied the form with triangular offsets for a table whose size is a power of two. Knuth's Section 6.4 analyses the model of secondary clustering that predicts its average cost. For decades no bound was proved for quadratic probing itself; Kuszmaul and Xi (2024) gave the first one, a constant expected time at some positive constant load factor.

## References
