---
tag: 42GYZ4
kind: data-structure
slug: hash-table
name: Hash table
aliases:
- hash map
- hash set
- hashed dictionary
- hashmap
area: data-structures/hashing
level: intro
summary: Array of buckets indexed by a hash function, giving expected O(1) dictionary operations.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of keys in the table, m: the number of buckets, α: the load factor n/m}
  time: {expected: O(1 + α), worst: Θ(n)}
  space: {extra: Θ(n + m)}
prereqs: [dictionary, hash-function, collision-resolution, dynamic-array]
see_also: [separate-chaining, open-addressing, load-factor, universal-hashing, rehashing, chaining-analysis, binary-search-tree, direct-address-table]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables), Sections 11.1 to 11.4
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), including the history at the end of the section
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables)
  - paper: doi:10.1145/362851.362882
    title: Robert Morris, Scatter storage techniques, Communications of the ACM 11(1), 1968
    locator: pages 38 to 44 (a survey of hashing with chaining and open addressing)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (the definition of a universal class and the bound on the expected cost of a sequence of operations)
---

A hash table stores a set of keys, each with a value, in an array of $m$ buckets, and puts each key $k$ in bucket $h(k)$, where $h$ is a [hash function](/hash-function/). It implements the [dictionary](/dictionary/) operations insert, search and delete in $O(1 + \alpha)$ expected time, where $\alpha = n/m$ is the [load factor](/load-factor/), when $h$ spreads the keys well, and in $\Theta(n)$ time in the worst case. Two keys can fall in the same bucket, so each hash table needs a method of [collision resolution](/collision-resolution/). With a table that grows to keep $\alpha$ bounded, the operations take $O(1)$ expected amortized time, which makes the hash table the default dictionary of most programming languages.

## In plain words

Think of a coat check with a row of numbered hooks. When you hand in a coat, the clerk computes a hook number from your name, with a fixed rule, and hangs the coat there. When you come back, the clerk computes the same number again and goes straight to that hook. There is no search through all the coats.

Two names can give the same hook number. Then the coats share the hook, and the clerk looks through the few coats on it. If the rule spreads the names well and there are enough hooks, each hook holds only a few coats, so each visit is fast. When the room gets too full, the clerk puts up a longer row of hooks and hangs each coat again by the same rule on the new row.

## The abstract type

A hash table implements the [dictionary](/dictionary/) abstract type. It keeps a finite map $D$ from keys to values, with distinct keys, and supports:

- `insert(T, k, v)`: set $D(k) = v$. If $k$ is already a key, its value is replaced.
- `search(T, k)`: return $D(k)$, or NIL if $k$ is not a key.
- `delete(T, k)`: remove $k$ and its value, if $k$ is a key.
- `size(T)`: return the number $n$ of keys.

A hash table needs only a test of equality on the keys and a hash function. It does not need an order on the keys, so it does not support the queries of an ordered dictionary, such as the minimum, the successor or a range.

## Representation

This page uses [separate chaining](/separate-chaining/), the method of CLRS Section 11.2. The other main method, [open addressing](/open-addressing/), has its own page.

The fields are an array $B[0 \ldots m-1]$ of buckets, where each bucket is a list of pairs $(k, v)$, the number of buckets $m \ge 1$, the number of pairs $n$, and a hash function $h$ from keys to integers. The bucket of a key $k$ is $b(k) = h(k) \bmod m$.

**Invariant.**

- **(H1) Placement.** Each pair $(k, v)$ of the table is in the list $B[b(k)]$.
- **(H2) Distinct keys.** No key occurs in two pairs of the table.
- **(H3) Count.** $n$ is the total length of the lists $B[0], \ldots, B[m-1]$.
- **(H4) Load.** $n \le m$, so the load factor $\alpha = n/m$ is at most 1.

The map that the table represents is $D = \{(k, v) : (k, v) \in B[i] \text{ for some } i\}$. By (H2), $D$ is a function.

## Operations

All three operations go to the bucket of the key and scan it. Insert can grow the table.

```pseudo id=main
HASH-INSERT(T, k, v)
L1  i ← h(k) mod T.m
L2  for each pair (k′, v′) in T.B[i] do
L3      if k′ = k then replace v′ by v; return
L4  append (k, v) to T.B[i]
L5  T.n ← T.n + 1
L6  if T.n > T.m then RESIZE(T, 2 · T.m)

HASH-SEARCH(T, k)
L7  i ← h(k) mod T.m
L8  for each pair (k′, v′) in T.B[i] do
L9      if k′ = k then return v′
L10 return NIL

HASH-DELETE(T, k)
L11 i ← h(k) mod T.m
L12 for each pair (k′, v′) in T.B[i] do
L13     if k′ = k then remove (k′, v′) from T.B[i]; T.n ← T.n − 1; return

RESIZE(T, m′)
L14 B′ ← an array of m′ empty lists
L15 for each pair (k, v) in T.B[0], T.B[1], …, T.B[T.m − 1] do
L16     append (k, v) to B′[h(k) mod m′]
L17 T.B ← B′; T.m ← m′
```

**Insert.** Line L1 finds the bucket of $k$. Lines L2 and L3 scan the bucket. If $k$ is there, its value is replaced and nothing else changes. Otherwise lines L4 and L5 add the new pair. If the table now has more pairs than buckets, line L6 doubles the number of buckets. The cost is $O(1 + \ell)$, where $\ell$ is the length of the bucket, plus the cost of a resize when one happens.

**Search.** Lines L7 to L10 scan the one bucket where $k$ can be. The cost is $O(1 + \ell)$.

**Delete.** Lines L11 to L13 scan the bucket and remove the pair with key $k$, if it is there. The cost is $O(1 + \ell)$. A delete does not shrink the table in this version.

**Resize.** Line L14 allocates the new array. Lines L15 and L16 put each pair in its bucket for the new size $m'$, because $h(k) \bmod m'$ is in general not $h(k) \bmod m$. The cost is $\Theta(n + m + m')$, that is $\Theta(n)$ when called from line L6, where $m' = 2m$ and $m < n$.

## Example

Start with $m = 4$ empty buckets, and let $h(k) = k$ for an integer key, so the bucket is $k \bmod m$. Insert the keys 10, 22, 31, 4, 15, 28 and 17, in this order. The values do not matter here, so the table shows only the keys.

| step | key | bucket | $n$ | $m$ | buckets $B[0], B[1], \ldots$ |
|---|---|---|---|---|---|
| insert 10 | 10 | 2 | 1 | 4 | [] [] [10] [] |
| insert 22 | 22 | 2 | 2 | 4 | [] [] [10 22] [] |
| insert 31 | 31 | 3 | 3 | 4 | [] [] [10 22] [31] |
| insert 4 | 4 | 0 | 4 | 4 | [4] [] [10 22] [31] |
| insert 15 | 15 | 3 | 5 | 8 | [] [] [10] [] [4] [] [22] [31 15] |
| insert 28 | 28 | 4 | 6 | 8 | [] [] [10] [] [4 28] [] [22] [31 15] |
| insert 17 | 17 | 1 | 7 | 8 | [] [17] [10] [] [4 28] [] [22] [31 15] |

Key 22 collides with key 10 in bucket 2. The insert of 15 makes $n = 5 > m = 4$, so line L6 calls RESIZE with $m' = 8$. After the resize, 10 stays in bucket 2, but 22 moves to bucket $22 \bmod 8 = 6$, and 4, 31 and 15 move as well.

Then search for 28: bucket $28 \bmod 8 = 4$ holds [4 28], so the search compares with 4, then with 28, and returns its value. A search for 12 also goes to bucket 4, compares with 4 and 28, and returns NIL. A delete of 22 removes it from bucket 6, and $n$ becomes 6.

## Correctness

Each operation keeps (H1) to (H4), and returns the answer that the dictionary asks for. The key fact is (H1): a pair with key $k$ can only be in bucket $b(k)$, so a scan of that one bucket is as good as a scan of the whole table. Insert adds a pair only to bucket $b(k)$ and only when the scan shows that $k$ is absent, which keeps (H1) and (H2). Delete removes the only pair with key $k$, if there is one. RESIZE moves each pair to its bucket for the new size and keeps all pairs, and line L6 restores (H4) because $n = m + 1 \le 2m$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost of an operation on key $k$ is $\Theta(1)$ to compute the bucket, plus one key comparison for each pair that it scans in bucket $b(k)$. So the cost depends on how $h$ spreads the keys.

**Worst case.** If all $n$ keys have the same bucket, a search scans all of them. So search, insert and delete take $\Theta(n)$ time in the worst case. An adversary who knows $h$ can force this case, which is an [algorithmic complexity attack](/algorithmic-complexity-attack/).

**Expected case.** Let $h$ be drawn at random from a [universal family](/universal-hash-family/), so that $\Pr[h(x) \bmod m = h(y) \bmod m] \le 1/m$ for each two distinct keys $x \ne y$, and let the keys be chosen without knowledge of $h$. For a key $k$, let $X_y$ be the indicator that $y$ is in the bucket of $k$. A search for $k$ scans at most $1 + \sum_{y \ne k} X_y$ pairs, and by [linearity of expectation](/linearity-of-expectation/) the expected number is at most $1 + n/m = 1 + \alpha$. So each of the three operations takes $O(1 + \alpha)$ expected time, without any assumption on the keys. The [analysis of separate chaining](/chaining-analysis/) gives the exact constants under [simple uniform hashing](/simple-uniform-hashing/).

**Resizing.** By (H4), $\alpha \le 1$ after each operation, so a single operation takes $O(1)$ expected time, without the resize. A resize from $m$ to $2m$ happens only when $n = m + 1$, and it costs $\Theta(m)$. The sizes double, so the costs of the resizes form a geometric series, and the largest one is at most a constant times the number of inserts done before it. In total, the resizes of a sequence of $s$ operations from the empty table cost less than $8s$ steps. Each operation therefore takes $O(1)$ expected amortized time. The full argument is in [the complexity proof](proofs/complexity.md).

| operation | worst case | expected (universal $h$) | expected amortized, with resize |
|---|---|---|---|
| search | $\Theta(n)$ | $O(1 + \alpha)$ | $O(1)$ |
| insert | $\Theta(n)$ | $O(1 + \alpha)$ | $O(1)$ |
| delete | $\Theta(n)$ | $O(1 + \alpha)$ | $O(1)$ |
| resize | $\Theta(n + m)$ | | |
| space | $\Theta(n + m)$ | | |

These bounds hold on the [word RAM](/word-ram/) when the hash value and one key comparison cost $O(1)$. For a string key of length $L$, each of them costs $O(L)$, and so does each operation.

## Variants

- **Collision resolution.** [Separate chaining](/separate-chaining/) keeps a list for each bucket. [Open addressing](/open-addressing/) puts the keys in the array itself and probes other slots: [linear probing](/linear-probing/), [quadratic probing](/quadratic-probing/), [double hashing](/double-hashing/), [Robin Hood hashing](/robin-hood-hashing/) and [hopscotch hashing](/hopscotch-hashing/). [Coalesced hashing](/coalesced-hashing/) keeps the chains inside the array.
- **Worst-case lookups.** [Cuckoo hashing](/cuckoo-hashing/) checks at most two slots for each search. [Perfect hashing](/perfect-hashing/) and [FKS perfect hashing](/fks-perfect-hashing/) give $O(1)$ worst-case search on a fixed set of keys.
- **Growth.** [Rehashing](/rehashing/) all keys at once, as above, gives an amortized bound. Incremental rehashing moves a few buckets at each operation, to bound the cost of each single operation. [Linear hashing](/linear-hashing/) and [extendible hashing](/extendible-hashing/) grow one bucket at a time and suit data on disk.
- **Hash set.** A table that stores only keys, without values, implements a set. It is the usual tool for [deduplication](/dedup/).
- **Cache-aware tables.** The [Swiss table](/swiss-table/) of Abseil probes groups of 16 slots with SIMD instructions on a byte of metadata for each slot.

## When to use it

Use a hash table when you need search, insert and delete by key and you do not need the keys in order. It is faster in practice than a [binary search tree](/binary-search-tree/) or a [red-black tree](/red-black-tree/), whose operations take $\Theta(\log n)$ time. Use a balanced tree instead when you need ordered queries (minimum, successor, range), a worst-case bound for each operation, or protection from keys that an adversary chooses. Use a [direct-address table](/direct-address-table/) when the keys are small integers. Use a sorted array with [binary search](/binary-search/) when the set does not change and memory is tight.

## Pitfalls

- **A bad hash function.** With $h(k) = k$ and $m$ a power of two, the bucket is the low bits of the key. Keys that are all multiples of 8 then use only one bucket in eight. Use a hash function that mixes all the bits of the key, such as the [multiplicative method](/multiplicative-hashing/), or a prime $m$ with the [division method](/division-method/).
- **Forgetting to rehash on resize.** Copying the lists to the same positions of the new array breaks (H1): later searches go to bucket $h(k) \bmod 2m$ and miss the key. Line L16 must recompute the bucket of each key with the new size $m'$.
- **Duplicate keys on insert.** If line L4 runs without the scan of lines L2 and L3, a second insert of the same key adds a second pair. Then a delete removes only one of them, and a later search still finds the old value.
- **Mutable keys.** If a key changes after the insert, its hash value changes, and the pair is in the wrong bucket. Use immutable keys, or remove the key before you change it.
- **Equality and hash must agree.** If two keys are equal, their hash values must be equal. A user-defined type that overrides equality but not the hash breaks (H1) for equal keys. See [hash codes for user-defined types](/hash-code-for-user-defined-types/).
- **Iteration order.** The order of the keys in a scan of the buckets depends on $h$ and on $m$, and it changes after a resize. Do not rely on it.

## Implementations

The Python version takes the hash function as a parameter, with the built-in `hash` as the default. For a small non-negative `int`, `hash(k)` is $k$, so the tests can follow the example exactly.

## History

Knuth, in the history at the end of Section 6.4, credits H. P. Luhn of IBM with the idea of hashing with chaining, in an internal IBM memorandum of January 1953. He reports that, at about the same time, another IBM group (G. M. Amdahl, E. M. Boehme, N. Rochester and A. L. Samuel) used open addressing with linear probing, and that the first published description of hashing appears to be by A. I. Dumey in 1956. The survey of Morris in Communications of the ACM in 1968 made the method widely known. Carter and Wegman introduced universal hashing in 1977 and 1979, which gave the expected bounds above without an assumption on the keys.

## References
