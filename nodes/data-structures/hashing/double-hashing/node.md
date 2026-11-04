---
tag: PMZJW6
kind: algorithm
slug: double-hashing
name: Double hashing
aliases:
- double hash probing
- double hashing open addressing
area: data-structures/hashing
level: intro
summary: Open addressing where a second hash function sets the probe step size.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys in the table, m: the number of slots, α: the load factor n/m}
  time: {expected: O(1/(1 − α)), worst: Θ(m)}
  space: {extra: Θ(m)}
prereqs: [open-addressing, probe-sequence, hash-function, uniform-hashing-assumption]
see_also: [linear-probing, quadratic-probing, load-factor, lazy-deletion, division-method, hash-table, linear-probing-analysis, cuckoo-hashing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing), double hashing and the analysis of open-address hashing
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), Algorithm D (open addressing with double hashing) and its analysis
  - paper: doi:10.1016/0022-0000(78)90046-6
    title: Leonidas J. Guibas and Endre Szemerédi, The analysis of double hashing, Journal of Computer and System Sciences 16(2), 1978
    locator: pages 226 to 274
  - paper: doi:10.1007/bf01202791
    title: George S. Lueker and Mariko Molodowitch, More analysis of double hashing, Combinatorica 13(1), 1993
    locator: pages 83 to 96
---

Double hashing is a method of [open addressing](/open-addressing/) in which a key $k$ probes the slots $(h_1(k) + i \cdot h_2(k)) \bmod m$ for $i = 0, 1, 2, \ldots$, so a second [hash function](/hash-function/) $h_2$ sets the step between probes. When $h_2(k)$ is coprime to the table size $m$, the [probe sequence](/probe-sequence/) visits every slot once. Keys that start at the same slot usually have different steps, so double hashing avoids the clusters of [linear probing](/linear-probing/) and [quadratic probing](/quadratic-probing/). Its expected number of probes is close to the ideal of the [uniform hashing assumption](/uniform-hashing-assumption/): at most $1/(1 - \alpha)$ for a search that fails, where $\alpha$ is the [load factor](/load-factor/).

## In plain words

All the keys live in one array of slots. To place a key, you compute a start slot from the key. If that slot is taken, you jump ahead by a fixed step and try again, and you keep jumping until you find a free slot. A search follows the same jumps and stops at the key or at a free slot.

In linear probing the step is always one. Then keys that land near each other pile up in long runs, and each run grows faster as it gets longer. In double hashing a second hash function computes the step from the key itself. Two keys with the same start slot most likely jump by different steps, so they follow different paths, and the runs stay short.

## The problem

The algorithm keeps a [dictionary](/dictionary/): a set of distinct keys, each with a value, under insert, search and delete. This is the [dictionary problem](/dictionary-problem/). The keys live in an array $A[0 \ldots m-1]$ with a fixed size $m$, so at most $m$ keys fit. Each slot is EMPTY, DELETED, or holds one pair $(k, v)$.

The probe sequence of $k$ is $p_k(i) = (h_1(k) + i \cdot h_2(k)) \bmod m$ for $i = 0, \ldots, m - 1$, with $0 \le h_1(k) < m$ and $1 \le h_2(k) < m$. We assume that $\gcd(h_2(k), m) = 1$ for each key. Two standard ways to meet this: choose $m$ prime, or choose $m$ a power of two and make $h_2(k)$ odd. A usual pair for integer keys is $h_1(k) = k \bmod m$ and $h_2(k) = 1 + (k \bmod m')$ with $m$ prime and $m' = m - 1$ or $m - 2$.

## The algorithm

```pseudo id=main
DH-INSERT(T, k, v)
L1  j ← NIL                                   ▷ the first free slot on the path
L2  for i ← 0 to T.m − 1 do
L3      q ← (h1(k) + i · h2(k)) mod T.m
L4      if T.A[q] = EMPTY then
L5          if j = NIL then j ← q
L6          exit the loop
L7      else if T.A[q] = DELETED then
L8          if j = NIL then j ← q
L9      else if T.A[q].key = k then
L10         T.A[q].value ← v; return
L11 if j = NIL then error "the table is full"
L12 T.A[j] ← (k, v)

DH-SEARCH(T, k)
L13 for i ← 0 to T.m − 1 do
L14     q ← (h1(k) + i · h2(k)) mod T.m
L15     if T.A[q] = EMPTY then return NIL
L16     if T.A[q] ≠ DELETED and T.A[q].key = k then return T.A[q].value
L17 return NIL

DH-DELETE(T, k)
L18 for i ← 0 to T.m − 1 do
L19     q ← (h1(k) + i · h2(k)) mod T.m
L20     if T.A[q] = EMPTY then return
L21     if T.A[q] ≠ DELETED and T.A[q].key = k then T.A[q] ← DELETED; return
```

**Insert.** The loop of lines L2 to L10 follows the probe sequence of $k$. It stops at the first EMPTY slot, because no key with this probe sequence can be stored after it. On the way, line L8 remembers the first DELETED slot, and line L10 replaces the value if $k$ is already in the table. If $k$ is absent, line L12 puts it in the first free slot of the path, which is either the first DELETED slot or the EMPTY slot that ended the loop. If all $m$ slots hold other keys, line L11 reports a full table.

**Search.** Lines L13 to L17 follow the same sequence. They skip DELETED slots and stop at the first EMPTY slot, since the key would have been placed there or before.

**Delete.** Lines L18 to L21 find the key and replace it by the marker DELETED, a tombstone, rather than by EMPTY. An EMPTY slot would cut the probe path of each key that was placed after it, and searches for those keys would stop too early. This is [lazy deletion](/lazy-deletion/).

## Example

Let $m = 13$, $h_1(k) = k \bmod 13$ and $h_2(k) = 1 + (k \bmod 11)$. Insert the keys 18, 41, 22, 44, 59, 32, 31 and 73 into an empty table. A dot is an EMPTY slot, and the slots are numbered 0 to 12.

| key | $h_1$ | $h_2$ | slots probed | table after the insert |
|---|---|---|---|---|
| 18 | 5 | 8 | 5 | . . . . . 18 . . . . . . . |
| 41 | 2 | 9 | 2 | . . 41 . . 18 . . . . . . . |
| 22 | 9 | 1 | 9 | . . 41 . . 18 . . . 22 . . . |
| 44 | 5 | 1 | 5, 6 | . . 41 . . 18 44 . . 22 . . . |
| 59 | 7 | 5 | 7 | . . 41 . . 18 44 59 . 22 . . . |
| 32 | 6 | 11 | 6, 4 | . . 41 . 32 18 44 59 . 22 . . . |
| 31 | 5 | 10 | 5, 2, 12 | . . 41 . 32 18 44 59 . 22 . . 31 |
| 73 | 8 | 8 | 8 | . . 41 . 32 18 44 59 73 22 . . 31 |

The keys 18, 44 and 31 all start at slot 5, but their steps are 8, 1 and 10, so after the first collision they go to different slots. With linear probing, 44 and 31 would both walk through slots 6 and 7.

Now delete 44. Slot 6 becomes DELETED. A search for 32 probes slot 6, sees DELETED, goes on, and finds 32 at slot $(6 + 11) \bmod 13 = 4$. If slot 6 were EMPTY, the search would stop there and miss 32. A search for 57 has $h_1 = 5$ and $h_2 = 3$. It probes slots 5, 8 and 11, finds slot 11 EMPTY and returns NIL. Last, insert 19, with $h_1 = 6$ and $h_2 = 9$. It probes slot 6 (DELETED, so $j = 6$), slot 2 (key 41) and slot 11 (EMPTY), and line L12 puts 19 in slot 6.

## Correctness

The key fact is that the probe sequence is a permutation: if $\gcd(h_2(k), m) = 1$, then $p_k(0), \ldots, p_k(m-1)$ are the $m$ slots, each once. If $p_k(i) = p_k(i')$ with $0 \le i < i' < m$, then $m$ divides $(i' - i) h_2(k)$, so $m$ divides $i' - i$, which is impossible.

The algorithm keeps this invariant:

- **(D1)** If key $k$ is in slot $p_k(t)$, then the slots $p_k(0), \ldots, p_k(t-1)$ are not EMPTY.
- **(D2)** No key is in two slots.

By (D1), a key $k$ that is in the table is met before the first EMPTY slot of its sequence, so searches and the scan of insert and delete are complete. Insert places $k$ at the first free slot of its path, so all slots before it are not EMPTY, which gives (D1) for $k$. Insert and delete never turn a slot into EMPTY, so (D1) stays true for each other key. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Worst case.** Each loop runs at most $m$ times, and each pass costs $O(1)$ on the [word RAM](/word-ram/) when $h_1$, $h_2$ and a key comparison cost $O(1)$. A set of keys that all have the same $h_1$ and the same $h_2$ forces the $j$-th of them to probe $j$ slots, so the worst case is $\Theta(m)$ for each operation, and $\Theta(n)$ for a table with $n$ keys.

**Expected case.** Let $\alpha = n/m < 1$ be the fraction of slots that are not EMPTY. Under the uniform hashing assumption, where each probe sequence is a uniformly random permutation of the slots, independent for each key:

- a search that fails probes at most $1/(1 - \alpha)$ slots in expectation;
- a search that succeeds, for a key chosen uniformly from the table and with no deletions, probes at most $\frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$ slots in expectation.

An insert costs as much as a search that fails, up to the scan for the key. The proofs are in [the complexity proof](proofs/complexity.md). For $\alpha = 0.5$, 0.75 and 0.9 the first bound is 2, 4 and 10 probes, and the second is about 1.39, 1.85 and 2.56. For comparison, linear probing needs about $\frac{1}{2}(1 + 1/(1 - \alpha)^2)$ probes for a search that fails, which is 2.5, 8.5 and 50.5.

Double hashing has only about $m^2$ distinct probe sequences (one for each pair $h_1, h_2$), not the $m!$ of uniform hashing, so the assumption is not exact. Guibas and Szemerédi proved in 1978 that double hashing has the same expected cost as uniform hashing up to a term that vanishes as $m \to \infty$, for $\alpha$ below about 0.319. Lueker and Molodowitch extended this in 1993 to each fixed $\alpha < 1$, for $h_1$ and $h_2$ that act as independent uniform random functions.

**Space.** The array has $m$ slots, so the space is $\Theta(m)$, with no pointers.

| operation | worst case | expected, uniform hashing |
|---|---|---|
| search, key absent | $\Theta(m)$ | at most $1/(1 - \alpha)$ probes |
| search, key present | $\Theta(m)$ | at most $\frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$ probes |
| insert | $\Theta(m)$ | at most $1/(1 - \alpha)$ probes |
| delete | $\Theta(m)$ | as a search |
| space | $\Theta(m)$ | |

## Properties

- **No primary or secondary clustering.** Two keys share a probe path only if they have the same $h_1$ and the same $h_2$.
- **Poor locality.** Successive probes are far apart in memory, so each probe is likely a cache miss. Linear probing is often faster in practice at low load for this reason.
- **Fixed capacity.** The table holds at most $m$ keys. A growing table rebuilds into a larger array with new $h_1$, $h_2$ and $m$, by [rehashing](/rehashing/).
- **Deletions leave tombstones.** DELETED slots count toward $\alpha$ for searches, so a table with many deletions gets slow until it is rebuilt.

## Variants and improvements

- **Brent's variation.** Before an insert, Brent's method of 1973 checks whether moving a key on the path one step along its own sequence gives a shorter total search time, and moves it if so. This lowers the cost of successful searches. Knuth describes it in Section 6.4.
- **Power-of-two tables.** With $m = 2^p$, take $h_2(k)$ odd, for example $h_2(k) = 2 \cdot g(k) + 1$, so the step is coprime to $m$ and the reduction is a mask.
- **[Linear probing](/linear-probing/) and [quadratic probing](/quadratic-probing/).** These use a step that does not depend on the key: 1, or a quadratic function of $i$. They are simpler and have better locality, at the cost of clustering.
- **[Cuckoo hashing](/cuckoo-hashing/).** Also uses two hash functions, but each key may be in only two slots, so a search costs at most two probes.

## When to use it

Use double hashing for an open-addressing table that must work well at a high load factor, such as 0.8 or 0.9, where linear probing slows down. It needs no pointers, so it uses less memory than [separate chaining](/separate-chaining/) for small keys. Prefer linear probing, or a [Robin Hood](/robin-hood-hashing/) or [Swiss table](/swiss-table/) design, when the load stays moderate and cache behaviour matters more than the number of probes. Prefer separate chaining when deletions are frequent or when the load can exceed 1.

## Pitfalls

- **A step that is not coprime to $m$.** With $m = 12$ and $h_2(k) = 4$, line L3 visits only 3 of the 12 slots, so an insert can fail while the table has free slots. Choose $m$ prime with $1 \le h_2(k) < m$, or $m$ a power of two with $h_2(k)$ odd.
- **A step of zero.** $h_2(k) = k \bmod m'$ is 0 for some keys, and then line L3 probes the same slot $m$ times. Write $h_2(k) = 1 + (k \bmod m')$.
- **Deleting by EMPTY.** Writing EMPTY instead of DELETED in line L21 breaks (D1). In the example, deleting 44 this way makes the search for 32 fail.
- **Stopping the insert at the first DELETED slot.** If line L8 also exited the loop, an insert of a key that is already present after a tombstone would store it twice, which breaks (D2). The loop must go on until EMPTY, to scan for the key.
- **Correlated $h_1$ and $h_2$.** If $h_2$ is a function of $h_1(k)$, keys with the same start slot get the same step, and the clusters come back. Compute $h_2$ from the key, for example from other bits of the hash code.

## Implementations

The Python version takes $h_1$ and $h_2$ as parameters. The default is $h_1(k) = \mathrm{hash}(k) \bmod m$ and $h_2(k) = 1 + (\mathrm{hash}(k) \bmod (m - 2))$, which for integer keys and $m = 13$ is the pair of the example.

## History

Knuth presents open addressing with double hashing as Algorithm D in Section 6.4, together with its analysis under the uniform hashing model. The first proof that double hashing matches uniform hashing asymptotically is by Guibas and Szemerédi in 1978, for load factors below about 0.319. Lueker and Molodowitch removed this limit in 1993.

## References
