---
tag: 7XC042
kind: data-structure
slug: binary-search-symbol-table
name: Binary search symbol table
area: data-structures/linear-structures
level: core
summary: Ordered symbol table kept in sorted parallel arrays, using binary search to find keys and rank.
implements: [ordered-symbol-table, dictionary]
prereqs: [binary-search, ordered-symbol-table, array]
see_also: [sequential-search-symbol-table, binary-search-tree, dynamic-array, interpolation-search, eytzinger-layout, b-tree, gap-buffer, order-statistic-tree]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), Algorithm 3.2 (BinarySearchST), the trace of the keys S E A R C H E X A M P L E, Proposition B (at most lg N + 1 compares for a search) and Proposition C (insertion uses about 2N array accesses in the worst case)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1 (Searching an ordered table), Algorithm B (binary search) and its history
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Exercise 2.3-6 (binary search) and Section 17.1, the rank and select operations
---

A binary search symbol table stores the key-value pairs of an [ordered symbol table](/ordered-symbol-table/) in two parallel [arrays](/array/), `keys` and `vals`, with the keys in increasing order. All operations rest on `rank(k)`, the number of keys less than $k$, which [binary search](/binary-search/) computes with at most $\lfloor \lg n \rfloor + 1$ comparisons. So a search costs $O(\log n)$ time, and the order-based operations min, max, floor, ceiling, select and range count are as fast or faster. An insert or delete of a key must shift the larger keys by one place, which costs $\Theta(n)$ in the worst case. It is the right table when searches far outnumber updates, and the static case is the base of many search structures.

## In plain words

Think of a printed dictionary. The words are in alphabetical order, so you find a word by opening the book in the middle, deciding whether your word comes before or after, and repeating on the half that is left. Even in a very large book, this takes only a few dozen steps.

The table works the same way: one array holds the keys in sorted order and a second array holds, at the same index, the value of each key. Finding a key is fast. Adding a new key is slow, because every larger key must move one place to make room, as a new word in a printed dictionary would push all later words down.

## The abstract type

The structure implements the [ordered symbol table](/ordered-symbol-table/) type for keys with a total order: `put(k, v)` (insert, or replace the value of an existing key), `get(k)`, `delete(k)`, `contains(k)`, `size`, and the order-based operations `min`, `max`, `floor(k)` (the largest key $\le k$), `ceiling(k)` (the smallest key $\ge k$), `rank(k)`, `select(i)` (the key of rank $i$), and `size(lo, hi)` and `keys(lo, hi)` for a range. Each key occurs at most once.

## Representation

Two arrays, $keys[0..cap-1]$ and $vals[0..cap-1]$, and a count $n$. The arrays grow and shrink as [dynamic arrays](/dynamic-array/).

**Invariant.** $keys[0] < keys[1] < \cdots < keys[n-1]$, and the table holds exactly the pairs $(keys[i], vals[i])$ for $0 \le i < n$.

Since the keys are strictly increasing, the index of a key is its rank: $keys[i]$ has exactly $i$ smaller keys.

## Operations

```pseudo id=main
RANK(T, k)                                 ▷ number of keys < k
L1  lo ← 0, hi ← T.n − 1
L2  while lo ≤ hi
L3      mid ← lo + ⌊(hi − lo) / 2⌋
L4      if k < keys[mid] then hi ← mid − 1
L5      else if k > keys[mid] then lo ← mid + 1
L6      else return mid
L7  return lo
GET(T, k)
L8  i ← RANK(T, k); if i < T.n and keys[i] = k then return vals[i] else return NIL
PUT(T, k, v)
L9  i ← RANK(T, k)
L10 if i < T.n and keys[i] = k then vals[i] ← v, return
L11 for j ← T.n down to i + 1: keys[j] ← keys[j − 1], vals[j] ← vals[j − 1]
L12 keys[i] ← k, vals[i] ← v, T.n ← T.n + 1
DELETE(T, k)
L13 i ← RANK(T, k); if i = T.n or keys[i] ≠ k then return
L14 for j ← i to T.n − 2: keys[j] ← keys[j + 1], vals[j] ← vals[j + 1]
L15 T.n ← T.n − 1
```

RANK is binary search that returns, on a miss, the place where $k$ would go. Both cases give the number of keys less than $k$. PUT on a new key shifts $keys[i..n-1]$ one place to the right, from the right end, so no key is overwritten before it is copied. DELETE shifts the keys after $i$ one place to the left. Before line L11, the array grows if it is full, and after line L15 it may shrink, as in a dynamic array.

The order-based operations need at most one RANK:

- `min` is $keys[0]$, `max` is $keys[n-1]$, and `select(i)` is $keys[i]$, each in $O(1)$.
- `ceiling(k)` is $keys[\text{RANK}(k)]$ if $\text{RANK}(k) < n$.
- `floor(k)` is $keys[i]$ if $keys[i] = k$ for $i = \text{RANK}(k)$, and $keys[i - 1]$ otherwise, if $i > 0$.
- `size(lo, hi)` is $\text{RANK}(hi) - \text{RANK}(lo)$, plus 1 if $hi$ is in the table.
- `keys(lo, hi)` returns $keys[\text{RANK}(lo)]$ up to the last key $\le hi$, in $O(\log n + r)$ for $r$ keys.

## Example

Put the keys S E A R C H E X A M P L E, with the value of each key equal to its position $0, 1, \ldots, 12$ in this list. This is the trace of Sedgewick and Wayne. "Moves" counts the shifts of line L11.

| put | value | keys after it | moves |
|---|---|---|---|
| S | 0 | S | 0 |
| E | 1 | E S | 1 |
| A | 2 | A E S | 2 |
| R | 3 | A E R S | 1 |
| C | 4 | A C E R S | 3 |
| H | 5 | A C E H R S | 2 |
| E | 6 | A C E H R S | 0, value replaced |
| X | 7 | A C E H R S X | 0 |
| A | 8 | A C E H R S X | 0, value replaced |
| M | 9 | A C E H M R S X | 3 |
| P | 10 | A C E H M P R S X | 3 |
| L | 11 | A C E H L M P R S X | 5 |
| E | 12 | A C E H L M P R S X | 0, value replaced |

The final arrays are $keys = $ A C E H L M P R S X and $vals = $ 8 4 12 5 11 9 10 3 0 7. The 13 puts made 20 moves. On this table:

- get(E) returns 12, and get(F) returns NIL.
- rank(F) is 3, so ceiling(F) is $keys[3] = $ H and floor(F) is $keys[2] = $ E.
- select(5) is M.
- size(F, Q) is rank(Q) − rank(F) = 7 − 3 = 4: the keys H, L, M, P.
- delete(H) finds $i = 3$ and shifts the 6 keys L M P R S X to the left.

RANK(F) on the 10 keys probes $keys[4] = $ L, then $keys[1] = $ C, then $keys[2] = $ E, then $keys[3] = $ H, and returns $lo = 3$ after 4 probes, which is $\lfloor \lg 10 \rfloor + 1$.

## Correctness

RANK keeps the invariant that every key in $keys[0..lo-1]$ is less than $k$ and every key in $keys[hi+1..n-1]$ is greater than $k$. Lines L4 and L5 keep it because the keys are sorted, and each pass makes $hi - lo$ smaller. If line L6 returns, $keys[mid] = k$, and by the order $mid$ keys are less than $k$. If the loop ends, $lo = hi + 1$, so the two parts cover the whole array and exactly $lo$ keys are less than $k$. PUT and DELETE then insert or remove at index RANK$(k)$, which keeps the keys strictly increasing. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | key comparisons |
|---|---|---|
| get, contains, rank, floor, ceiling | $O(\log n)$ | at most $\lfloor \lg n \rfloor + 1$ three-way compares |
| put of an existing key | $O(\log n)$ | |
| put of a new key, delete | $\Theta(n)$ | plus about $2(n - i)$ array writes for shifts |
| min, max, select | $O(1)$ | 0 |
| size(lo, hi), keys(lo, hi) | $O(\log n)$, $O(\log n + r)$ | |
| space | $2n$ to $8n$ cells with resizing | |

Building a table by $n$ puts in random order costs $\Theta(n^2)$ time, since each new key shifts about half of the others. Puts of keys in increasing order shift nothing and cost $O(n \log n)$ in total; and a table can be built from $n$ unsorted pairs in $O(n \log n)$ time by sorting them, then dropping repeated keys.

## Variants

- **Static table.** Build once by sorting, then only search. This is the common use: a read-only dictionary, a sorted index in a file, a sorted array of IP ranges.
- **Linear or interpolation search inside.** For small $n$, a linear scan beats binary search because of branch prediction. For keys spread evenly, [interpolation search](/interpolation-search/) uses $O(\log \log n)$ expected probes.
- **Cache-friendly layouts.** The [Eytzinger layout](/eytzinger-layout/) stores the sorted keys in the order of a breadth-first walk of the implicit search tree, so the first probes share cache lines. The [van Emde Boas layout](/van-emde-boas-layout/) does the same at every scale.
- **Insert buffer.** Keep new keys in a small unsorted or sorted buffer, and merge it into the main array when it reaches $\sqrt{n}$ keys. Searches look in both. This trades a slower search for $O(\sqrt{n})$ amortized updates, and with $\log n$ levels of doubling sizes it becomes the logarithmic method of Bentley and Saxe.
- **Gap at the edit point.** A [gap buffer](/gap-buffer/) makes a run of inserts near the same place cheap, which helps for keys that arrive nearly sorted.
- **Balanced search trees.** A [binary search tree](/binary-search-tree/) that stays balanced, or a [B-tree](/b-tree/), gives $O(\log n)$ for put and delete too, at the cost of pointers and of slower searches in practice.

## When to use it

Use a binary search symbol table when the set of keys changes rarely compared with the number of searches, or when it is built once: a symbol table read from a file, the keywords of a language, a lookup table in a sorted file on disk. It is compact, two arrays and no pointers, and its searches touch few cache lines. It also gives the order-based operations, rank and select, which a hash table does not. For a table with many inserts in random order, use a balanced tree or, without order operations, a [hash table](/hash-table/).

## Pitfalls

- **Overflow in the midpoint.** With fixed-width integers, $\lfloor (lo + hi)/2 \rfloor$ can overflow when $lo + hi$ exceeds the largest integer. Line L3 uses $lo + \lfloor (hi - lo)/2 \rfloor$.
- **Off by one in RANK.** Returning $hi$ instead of $lo$ on a miss, or a loop condition $lo < hi$ with $hi = n - 1$, misses the last key or puts a new key in the wrong place. The invariant above fixes the right bounds.
- **Shifting in the wrong direction.** In PUT, copying from left to right, $keys[i+1] \leftarrow keys[i]$ first, writes one key over all the others. Shift from the right end, as line L11 does.
- **Forgetting the replace case.** Line L10 must test for an existing key. Without it, a repeated put adds a second copy, and the keys are no longer strictly increasing.
- **Keys with an inconsistent order.** Binary search assumes a total order. Floating-point NaN keys, or a comparison that is not transitive, make RANK return wrong places, and the invariant breaks silently.

## Implementations

## History

Binary search in a sorted table is old: Knuth (Volume 3, Section 6.2.1) traces it to John Mauchly's 1946 lectures at the Moore School, and notes that the first version correct for every $n$ was published only in 1960. The pairing of a sorted array of keys with a parallel array of values, and the use of rank as the core operation of an ordered symbol table, is the presentation of Sedgewick and Wayne's BinarySearchST.

## References
