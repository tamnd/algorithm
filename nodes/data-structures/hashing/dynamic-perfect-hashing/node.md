---
tag: F7B69T
kind: algorithm
slug: dynamic-perfect-hashing
name: Dynamic perfect hashing
aliases:
- Dietzfelbinger dynamic dictionary
- Dietzfelbinger dynamic perfect hashing
- dynamic FKS
area: data-structures/hashing
level: research
summary: Extends FKS to support updates with worst-case O(1) lookups.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys}
  time: {amortized: O(1) expected}
  space: {extra: O(n)}
properties: {deterministic: false}
prereqs: [fks-perfect-hashing, universal-hash-family, hash-table]
see_also: [cuckoo-hashing, perfect-hashing, global-rebuilding, amortized-cost, rehashing, universal-hashing]
sources:
  - paper: doi:10.1137/S0097539791194094
    title: Martin Dietzfelbinger, Anna Karlin, Kurt Mehlhorn, Friedhelm Meyer auf der Heide, Hans Rohnert and Robert E. Tarjan, Dynamic perfect hashing, upper and lower bounds, SIAM Journal on Computing 23(4), 1994
    locator: pages 738 to 761 (the dynamic scheme and its expected amortized analysis)
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, János Komlós and Endre Szemerédi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3), 1984
    locator: pages 538 to 544 (the static two-level scheme)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 11.5 (Perfect hashing), the static scheme that this page makes dynamic
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (the universal family used at both levels)
---

Dynamic perfect hashing keeps a changing set of $n$ keys so that a search reads one slot and takes $O(1)$ time in the worst case, while an insert or a delete takes $O(1)$ expected amortized time, and the space is $O(n)$ words. It is the two-level scheme of [FKS perfect hashing](/fks-perfect-hashing/), with three rules for change: rebuild a bucket when a new key collides in it, double the table of a bucket when the bucket grows, and rebuild the whole structure after a fixed number of updates. It solves the [dictionary problem](/dictionary-problem/), and Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert and Tarjan published it in 1994.

## In plain words

The static FKS method sorts the keys into groups with a first hash function, and gives each group a small table, with room for about the square of the group size, and a second function that puts each key of the group in its own slot. A search looks at one slot.

To allow changes, keep spare room. A new key goes to its group, and into its slot if that slot is free. If two keys of the group now want the same slot, choose a new function for that group only, which is cheap because the group is small. If a group gets too big for its table, give it a table twice as wide. After enough changes, build everything again with fresh functions and sizes that fit the new number of keys. The rare large rebuilds are paid for by the many cheap changes between them.

## The problem

The input is a sequence of operations insert$(x)$, delete$(x)$ and search$(x)$ on keys of $U = \{0, \ldots, p - 1\}$, with $p$ prime. The structure keeps a set $S \subseteq U$, and search$(x)$ must return whether $x \in S$. This is the [dictionary problem](/dictionary-problem/) for keys without values; a value can be stored next to each key. The sequence is fixed in advance and does not depend on the random choices of the algorithm (an oblivious adversary).

Both levels use the universal family of Carter and Wegman,

$$h_{a,b,m}(x) = ((a x + b) \bmod p) \bmod m, \qquad a \in \{1, \ldots, p - 1\}, \ b \in \{0, \ldots, p - 1\},$$

for which two distinct keys collide with probability at most $1/m$.

## The algorithm

The fields are the set $S$; the number $M$ of buckets and the first-level function $h = h_{a,b,M}$; the update counter $u$; and, for each bucket $j$, the set $S_j = \{x \in S : h(x) = j\}$, a limit $L_j$, a counter $c_j$, a table $T_j$ of $2 L_j^2$ slots and a function $h_j$ into these slots. The constants 64 and 512 are the choice of this page; the paper uses other constants.

```pseudo id=main
DPH-INSERT(x)
L1  if DPH-SEARCH(x) then return
L2  u ← u + 1
L3  if u > ⌈M/2⌉ then REHASH-ALL(S ∪ {x}); return
L4  j ← h(x); S_j ← S_j ∪ {x}; c_j ← c_j + 1
L5  if c_j ≤ L_j and T_j[h_j(x)] = NIL then T_j[h_j(x)] ← x; return
L6  if c_j > L_j and |S_j| > L_j / 2 then
L7      L_j ← 2 L_j
L8      if Σ_i 2 L_i² > 512 M then REHASH-ALL(S); return
L9  REBUILD-BUCKET(j)

DPH-DELETE(x)
L10 if not DPH-SEARCH(x) then return
L11 u ← u + 1
L12 if u > ⌈M/2⌉ then REHASH-ALL(S ∖ {x}); return
L13 j ← h(x); T_j[h_j(x)] ← NIL; S_j ← S_j ∖ {x}

DPH-SEARCH(x)
L14 j ← h(x)
L15 return T_j[h_j(x)] = x

REBUILD-BUCKET(j)
L16 if T_j has 2 L_j² slots then T_j[h_j(y)] ← NIL for each y ∈ S_j, else T_j ← an array of 2 L_j² slots
L17 repeat pick (a_j, b_j) at random; h_j ← h_{a_j,b_j,2L_j²}
L18 until h_j(x) ≠ h_j(y) for all x ≠ y in S_j
L19 T_j[h_j(x)] ← x for each x ∈ S_j; c_j ← |S_j|

REHASH-ALL(S′)
L20 S ← S′; M ← max(|S|, 1); u ← 0
L21 repeat pick (a, b) at random; h ← h_{a,b,M}; S_j ← {x ∈ S : h(x) = j} for each j
L22 until Σ_j 8 · max(|S_j|, 1)² ≤ 64 M
L23 for j ← 0 to M − 1 do L_j ← 2 · max(|S_j|, 1); REBUILD-BUCKET(j)
```

**Search** (lines L14 and L15) is the FKS search: one first-level hash, one second-level hash, one comparison. Each table has at least 8 slots, so an empty bucket needs no special case.

**Insert.** Line L1 makes an insert of a present key do nothing. Lines L2 and L3 count the update and start a new phase with REHASH-ALL when the phase has had more than $\lceil M/2 \rceil$ updates. Line L4 adds $x$ to its bucket. In the common case, line L5 finds the slot of $x$ free and writes it there. Otherwise the bucket is rebuilt by line L9, either because $x$ collides, or because more keys came into the bucket since its last rebuild than the limit $L_j$ allows. If the bucket is also more than half full, lines L6 and L7 double its limit first, which makes its table four times larger. Line L8 keeps the total size of the second level at most $512M$; if a doubling breaks this, everything is rebuilt. The sum of line L8 is kept in a counter and updated at each doubling, so the test takes $O(1)$ time.

**Delete** (lines L10 to L13) counts the update, starts a new phase if needed, and clears the slot of $x$. It does not change $c_j$, so $c_j$ counts all the keys placed in the bucket since its last rebuild, including the deleted ones. This makes a bucket with many deletions and insertions be rebuilt from time to time, which the analysis needs.

**REBUILD-BUCKET** draws second-level functions until one has no collision on $S_j$. **REHASH-ALL** sets $M$ to the number of keys, draws a first-level function until the second level is not too large, and rebuilds each bucket.

## Example

Let $p = 101$, start from the empty set, and insert 10, 22, 37, 40, 52, 60 and 70, then delete 37. The random choices are those of the Python version with `random.Random(5)`. The table shows the state after each operation: $M$, $u$, the buckets $S_0, S_1, \ldots$, the limits $L_j$ and the total number of second-level slots $\sum_j 2L_j^2$.

| operation | what happens | $M$ | $u$ | buckets | limits $L_j$ | slots |
|---|---|---|---|---|---|---|
| start | REHASH-ALL$(\emptyset)$ | 1 | 0 | [] | 2 | 8 |
| insert 10 | line L5 writes the key | 1 | 1 | [10] | 2 | 8 |
| insert 22 | $u = 2 > \lceil 1/2 \rceil$: REHASH-ALL | 2 | 0 | [22] [10] | 2 2 | 16 |
| insert 37 | line L5 writes the key | 2 | 1 | [22 37] [10] | 2 2 | 16 |
| insert 40 | $u = 2 > 1$: REHASH-ALL | 4 | 0 | [40] [10 22] [] [37] | 2 4 2 2 | 56 |
| insert 52 | line L5 writes the key | 4 | 1 | [40 52] [10 22] [] [37] | 2 4 2 2 | 56 |
| insert 60 | $c_0 = 3 > L_0 = 2$, $\lvert S_0 \rvert = 3 > 1$: double $L_0$, rebuild bucket 0 | 4 | 2 | [40 52 60] [10 22] [] [37] | 4 4 2 2 | 80 |
| insert 70 | $u = 3 > 2$: REHASH-ALL on 7 keys | 7 | 0 | [37] [10 22] [] [] [70] [] [40 52 60] | 2 4 2 2 2 2 6 | 144 |
| delete 37 | line L13 clears the slot | 7 | 1 | [] [10 22] [] [] [70] [] [40 52 60] | 2 4 2 2 2 2 6 | 144 |

After the last step, a search for 22 reads one slot of $T_1$ and finds 22, and a search for 37 reads one slot of $T_0$, which is NIL. The example shows that the constants of the space bound are large: 144 slots for 6 keys.

## Correctness

The structure keeps these invariants after each operation:

- **(D1)** $S$ is the disjoint union of the sets $S_j$, and $S_j = \{x \in S : h(x) = j\}$.
- **(D2)** $T_j$ has $2L_j^2$ slots, $h_j$ is one-to-one on $S_j$, and the slots of $T_j$ that are not NIL hold exactly the keys of $S_j$, each $x$ in slot $h_j(x)$.
- **(D3)** $|S_j| \le c_j \le L_j$.
- **(D4)** $\sum_j 2L_j^2 \le 512M$.
- **(D5)** $u \le \lceil M/2 \rceil$, and $M = \max(n_0, 1)$, where $n_0$ is the size of $S$ at the last REHASH-ALL.

By (D1) and (D2), a key $x \in S$ is in slot $h_j(x)$ of $T_{h(x)}$, and a key $x \notin S$ is not in any table, so line L15 answers correctly. The key step for insert is line L5: by (D3), the bucket still has $c_j \le L_j$, and writing $x$ to a free slot keeps (D2). Each other path ends in REBUILD-BUCKET or REHASH-ALL, which restore all invariants from scratch. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with $p < 2^w$. The details are in [the complexity proof](proofs/complexity.md).

**Search: $O(1)$ worst case.** Lines L14 and L15 do two hash evaluations and one comparison, in every state.

**Space: $O(n)$ words in every state.** By (D4), the second level has at most $512M$ slots. By (D5), at most $\lceil M/2 \rceil$ updates happened since the last REHASH-ALL, so $n \ge n_0 - \lceil n_0/2 \rceil$ and $M \le 2n + 1$. The first level has $O(M)$ words. So the space is at most a constant times $n + 1$.

**A rebuild of a bucket.** The table of bucket $j$ has $2L_j^2$ slots and at most $L_j$ keys, so a random $h_j$ has an expected number of colliding pairs of at most $\binom{L_j}{2}/(2L_j^2) < 1/4$, and line L18 accepts it with probability more than $3/4$. A trial costs $O(|S_j|)$, so a rebuild costs $O(|S_j| + 1)$ expected time, plus $O(L_j^2)$ when line L16 allocates a new table. Line L16 clears an old table in $O(|S_j|)$ time, because by (D2) only the slots of the keys of $S_j$ can be in use; clearing all $2L_j^2$ slots would make the rebuilds after collisions too costly.

**Collisions are rare.** A new key collides in line L5 with one of the at most $L_j$ keys placed since the last rebuild with probability at most $\frac{4}{3} \cdot L_j / (2L_j^2) = \frac{2}{3 L_j}$, even when we condition on the fact that $h_j$ survived the earlier inserts. So the expected cost of the rebuilds by collision is $O(1)$ for each insert.

**Doubling and phases.** A bucket doubles only when it is more than half full, so its limit is at most 4 times the number of distinct keys that fall into it during the phase, and the tables that it allocates have a total size of at most $\frac{4}{3}$ times the last one. A phase has $\lceil M/2 \rceil$ updates when it ends at line L3 or L12, and costs $O(M)$ expected time for REHASH-ALL and the doublings. A phase ends at line L8 with probability less than $0.64$, whatever happened before it, because the total table size is bounded by the sum of the squares of the bucket sizes of a fixed set of at most $2M$ keys. So the expected sum of $M$ over all phases is at most a constant times the number of updates, and a sequence of $N$ operations from the empty set takes $O(N + 1)$ expected time. This is $O(1)$ expected amortized time for each operation. The constants are those of this page; the paper proves the same bounds with its own constants and a different accounting.

| operation | bound | case |
|---|---|---|
| search | $O(1)$ | worst case |
| insert, delete | $O(1)$ | expected amortized |
| space | $O(n)$ words | worst case |

## Properties

- **Las Vegas.** The answers are always right; only the running time is random.
- **Two probes for a search.** A search reads the first-level entry of the bucket and one slot of its table, as in FKS.
- **Oblivious adversary.** The expected bounds hold when the sequence of operations does not depend on the random functions. An adversary who learns $h$ can force many keys into one bucket and many rebuilds.
- **Large constants.** The space is linear but with a large constant factor, as the example shows.

## Variants and improvements

- **Real-time dynamic hashing.** Dietzfelbinger and Meyer auf der Heide gave a scheme with $O(1)$ worst-case time for each operation with high probability, with a new class of hash functions.
- **[Cuckoo hashing](/cuckoo-hashing/).** Two tables and two functions, a search reads two slots, and inserts take $O(1)$ expected amortized time. It uses about $2n$ to $3n$ slots and is much simpler. It replaced dynamic perfect hashing in most uses.
- **Deamortized versions.** The global rebuild can be done in the background, a few keys at each update, as in [global rebuilding](/global-rebuilding/), to bound the cost of each single update.

## When to use it

Dynamic perfect hashing is mainly of theoretical interest: it was the first dictionary with worst-case $O(1)$ search, linear space and expected amortized $O(1)$ updates. In practice, [cuckoo hashing](/cuckoo-hashing/) gives the same guarantees with less space and less code, and an ordinary [hash table](/hash-table/) with [linear probing](/linear-probing/) is faster on average. If the set does not change, use [FKS perfect hashing](/fks-perfect-hashing/).

## Pitfalls

- **Counting only present keys.** If line L13 also decreases $c_j$, a bucket where one key is deleted and inserted again many times is never rebuilt, and the bound on the collision probability for a new key no longer holds, because $h_j$ has survived many trials. Count each key placed since the last rebuild, as line L4 does.
- **Doubling a sparse bucket.** If lines L6 and L7 double $L_j$ whenever $c_j > L_j$, without the test $|S_j| > L_j/2$, repeated delete and insert of the same key doubles the table of one bucket many times, and line L8 forces a rebuild of everything each time.
- **No phase limit.** Without lines L3 and L12, $M$ stays fixed while $n$ grows, the buckets get large, and the sum of their squares grows faster than $n$. The space bound and the expected cost both fail.
- **Duplicate inserts.** Without line L1, a second insert of a present key counts as an update, makes $c_j$ count the key twice, and finds its own slot in use, so it forces a needless rebuild of the bucket.

## Implementations

The Python version takes a `random.Random` object, so that a test can fix the random choices. Its constants 64 and 512 are those of the pseudocode.

## History

Fredman, Komlós and Szemerédi gave the static two-level scheme in 1984. Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert and Tarjan presented the dynamic version at the IEEE Symposium on Foundations of Computer Science in 1988 and published it in the SIAM Journal on Computing in 1994, with $O(1)$ worst-case search, $O(1)$ expected amortized updates and linear space. The same paper proves lower bounds for deterministic dynamic schemes of a restricted kind. Pagh and Rodler's cuckoo hashing of 2001 gave the same bounds with a simpler structure.

## References
