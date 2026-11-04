---
tag: FZSDPB
kind: data-structure
slug: radix-heap
name: Radix heap
aliases:
- monotone radix heap
area: data-structures/heaps
level: advanced
summary: Monotone priority queue for integer keys using buckets indexed by the highest differing bit.
implements: [priority-queue]
model: word-ram
complexity:
  vars: {n: the number of items, U: the largest key, C: the largest key minus the last extracted key}
  time: {amortized: O(log U)}
  space: {extra: Θ(n + log U)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [priority-queue, bucket-queue, word-ram, bitwise-operations, aggregate-method]
see_also: [bucket-queue, dial-algorithm, dijkstra, single-source-shortest-paths, leading-zero-count, integer-sorting, fusion-tree, fibonacci-heap]
sources:
  - paper: Ravindra K. Ahuja, Kurt Mehlhorn, James B. Orlin and Robert E. Tarjan, Faster algorithms for the shortest path problem, Journal of the ACM 37(2), 1990
    locator: pages 213 to 223 (the one-level radix heap with O(m + n log C) for Dijkstra's algorithm, and the two-level form with Fibonacci heaps, O(m + n sqrt(log C)))
  - paper: Boris V. Cherkassky, Andrew V. Goldberg and Craig Silverstein, Buckets, heaps, lists, and monotone priority queues, SIAM Journal on Computing 28(4), 1999
    locator: the definition of monotone priority queues and the comparison of multilevel bucket structures
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 7 (Shortest paths), Dijkstra's algorithm and its heap operations
---

A radix heap is a *monotone* priority queue for nonnegative integer keys: the keys it returns never decrease, and every key inserted must be at least the last key returned. It keeps the items in about $\lg U$ buckets, indexed by the position of the highest bit in which a key differs from the last returned key. An item only moves to a lower bucket, so it moves at most $\lceil \lg U \rceil$ times in its life, which gives $O(\log U)$ amortized time per insert and $O(1)$ amortized time per extract-min. Dijkstra's algorithm with nonnegative integer weights produces exactly this monotone pattern, and Ahuja, Mehlhorn, Orlin and Tarjan introduced radix heaps for it in 1990.

## In plain words

Think of sorting mail by how far away it must go. Letters for your own street go in the first box, letters for your district in the next, for your city in the next, and so on, with each box covering a range twice as wide as the one before. You always take mail from the first box.

When the first box is empty, you open the smallest nonempty box, move to the nearest address in it, and sort that box again into the smaller boxes, because now you are closer to all of them. A letter can only move to a smaller box, never to a larger one, and there are only a few boxes. So each letter is sorted only a few times in total.

## The abstract type

A radix heap implements a monotone [priority queue](/priority-queue/) on items with nonnegative integer keys below $U$:

- `insert(x)` with $\mathrm{key}(x) \ge last$,
- `extract-min()`, which returns an item of smallest key and sets $last$ to its key,
- `find-min()`, `is-empty()`, `size()`.

Here $last$ starts at $0$. A key smaller than $last$ is not allowed. This is the case in [Dijkstra's algorithm](/dijkstra/) with nonnegative weights: every new tentative distance $d(u) + w(u, v)$ is at least $d(u)$, which was just extracted. Decrease-key is possible with handles, as long as the new key is still at least $last$.

## Representation

Let $b(k)$ be the *bucket index* of a key $k$:
$$b(k) = \begin{cases} 0 & \text{if } k = last, \\ 1 + \lfloor \lg(k \oplus last) \rfloor & \text{otherwise,} \end{cases}$$
where $\oplus$ is the bitwise exclusive or. So $b(k) = i \ge 1$ means that $k$ and $last$ agree on all bits above bit $i - 1$ and differ in bit $i - 1$. On a word RAM this is one XOR and one [leading-zero count](/leading-zero-count/). For keys below $U = 2^w$, the indices are $0$ to $w$.

The heap holds the value $last$, buckets $B[0], \dots, B[w]$, each an unordered list of items, and a count $n$.

**Invariant.**

- **(R1) Monotone.** Every key in the heap is at least $last$.
- **(R2) Buckets.** Every item with key $k$ is in the bucket $B[b(k)]$.

By (R1) and (R2), every key in $B[0]$ equals $last$. If $k$ is in $B[i]$ with $i \ge 1$, then $k > last$, so bit $i - 1$ is 1 in $k$ and 0 in $last$. So all keys of $B[i]$ are smaller than all keys of $B[j]$ for $1 \le i < j$: they agree with $last$ on bit $j - 1$, which is 0, and those of $B[j]$ have a 1 there, and both agree with $last$ above.

## Operations

```pseudo id=main
INSERT(x)
L1  require key(x) ≥ last
L2  add x to B[b(key(x))]

EXTRACT-MIN()                           ▷ the heap is not empty
L3  if B[0] is empty then
L4      i ← the smallest index with B[i] not empty
L5      last ← the smallest key in B[i]
L6      S ← B[i]; B[i] ← the empty list
L7      for each item y of S do add y to B[b(key(y))]         ▷ with the new last
L8  remove any item from B[0] and return it
```

**Insert** (lines L1 and L2) computes one bucket index and appends the item, in $O(1)$ time.

**Extract-min** (lines L3 to L8) returns an item of $B[0]$ if there is one. Otherwise, the smallest keys are in the lowest nonempty bucket $B[i]$, by the order of buckets shown above. It finds the minimum of $B[i]$, makes it the new $last$, and redistributes the items of $B[i]$. The items in buckets above $i$ do not move. The new $last$ is in $B[i]$, so it agrees with the old $last$ on all bits above bit $i - 1$. A key in $B[j]$ with $j > i$ first differs from the old $last$ in bit $j - 1 > i - 1$, so it first differs from the new $last$ in the same bit.

**Find-min** does the same refill, if needed, and returns $last$.

## Example

Start with $last = 0$ and insert 5, 1, 7, 6, 13. In binary, these are 101, 1, 111, 110 and 1101, so the buckets are $B[1] = \{1\}$, $B[3] = \{5, 6, 7\}$ and $B[4] = \{13\}$.

| step | operation | $last$ | refill | buckets after | returns |
|---|---|---|---|---|---|
| 1 | extract-min | 1 | $B[1] = \{1\}$: 1 goes to $B[0]$ | $B[3] = \{5, 6, 7\}$, $B[4] = \{13\}$ | 1 |
| 2 | extract-min | 5 | $B[3]$: 5 to $B[0]$; $6 \oplus 5 = 3$ and $7 \oplus 5 = 2$, both to $B[2]$ | $B[2] = \{6, 7\}$, $B[4] = \{13\}$ | 5 |
| 3 | insert 8 | 5 | $8 \oplus 5 = 1101_2$, so $B[4]$ | $B[2] = \{6, 7\}$, $B[4] = \{8, 13\}$ | |
| 4 | extract-min | 6 | $B[2]$: 6 to $B[0]$; $7 \oplus 6 = 1$, to $B[1]$ | $B[1] = \{7\}$, $B[4] = \{8, 13\}$ | 6 |
| 5 | extract-min | 7 | $B[1]$: 7 to $B[0]$ | $B[4] = \{8, 13\}$ | 7 |
| 6 | extract-min | 8 | $B[4]$: 8 to $B[0]$; $13 \oplus 8 = 101_2$, to $B[3]$ | $B[3] = \{13\}$ | 8 |
| 7 | extract-min | 13 | $B[3]$: 13 to $B[0]$ | empty | 13 |

In step 1, 13 stays in $B[4]$: $13 \oplus 1 = 1100_2$ still has its highest bit at position 3. The six items were moved 10 times in total by the refills, and no item moved more than 3 times. The key 13 went from $B[4]$ to $B[3]$ to $B[0]$.

## Correctness

Insert keeps (R1) because of its precondition and (R2) by construction. In extract-min, the keys of the lowest nonempty bucket are the smallest keys in the heap, so the new $last$ is the minimum of the heap. After the refill, every item of the old $B[i]$ goes to the bucket for the new $last$, and the items of higher buckets are already there. The key returned equals $last$, which is a smallest key. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| insert | $O(1)$ actual, $O(\log U)$ amortized to pay for its later moves |
| extract-min, find-min | $O(\log U)$ actual to find the bucket, plus the moves; $O(1)$ amortized with a word of flags |
| space | $\Theta(n + \log U)$ |

**Each item moves at most $\lceil \lg U \rceil$ times.** When an item of $B[i]$ moves in a refill, it goes to a bucket of index less than $i$, because the new $last$ agrees with it on bit $i - 1$ and above. An item in a bucket above $i$ does not move. So the bucket index of an item only goes down, and it starts at most at $w = \lceil \lg U \rceil$. By the [aggregate method](/aggregate-method/), the total cost of all refills over a sequence with $n$ inserts is $O(n \log U)$, plus $O(\log U)$ per extract-min to find the lowest nonempty bucket. A bit mask of the nonempty buckets and a lowest-set-bit instruction find it in $O(1)$.

**Dijkstra's algorithm.** With $n$ vertices, $m$ edges and integer weights at most $C$, all keys are at most $nC$. With the bucket index of this page, Dijkstra's algorithm runs in $O(m + n \log(nC))$ time, and in $O(m + n \log C)$ with the interval form of Ahuja et al. below, which depends only on $C$. Ahuja et al. also combine radix heaps with Fibonacci heaps inside the buckets to get $O(m + n\sqrt{\log C})$. For comparison, a [Fibonacci heap](/fibonacci-heap/) gives $O(m + n \log n)$ in the comparison model, and the [bucket queue](/bucket-queue/) of [Dial's algorithm](/dial-algorithm/) gives $O(m + nC)$.

## Variants

- **Interval form.** Ahuja et al. define the buckets by ranges of keys: $B[0]$ holds $last$, and at the start $B[i]$ for $i \ge 1$ holds the keys from $last + 2^{i-1}$ to $last + 2^i - 1$, so that $\lceil \lg(C + 1) \rceil + 1$ buckets cover all keys up to $last + C$. A refill finds the minimum $d$ of the lowest nonempty bucket and splits that bucket's range among the lower buckets, starting from $d$. Each item again only moves down, and the number of buckets depends only on $C$. The form of this page, with exclusive or, has the same moves argument and is shorter to code, but its number of buckets depends on the size of the keys.
- **Two-level radix heap.** Using a larger base, with $K$ buckets per level and a heap inside the buckets, Ahuja et al. get $O(m + n \log C / \log \log C)$ and, with Fibonacci heaps, $O(m + n\sqrt{\log C})$ for Dijkstra's algorithm.
- **Bucket queue.** The [bucket queue](/bucket-queue/) uses one bucket per key value. It is simpler, but needs $C + 1$ buckets and its scan costs $O(C)$ per extract-min in the worst case.
- **Monotone heaps in general.** Cherkassky, Goldberg and Silverstein study multilevel bucket structures for monotone priority queues, with a heap on top for the nonempty buckets, and compare them in experiments on shortest paths.

## When to use it

Use a radix heap for [single-source shortest paths](/single-source-shortest-paths/) with nonnegative integer weights, for event simulation with integer times, and for any other monotone sequence of integer keys. It does no key comparisons in the usual sense, has no pointers in the items, and moves each item only a few times, so it is often faster than a [binary heap](/binary-heap/) in practice. Do not use it when keys can go below the last extracted key, when keys are not integers, or when you need extract-max as well. For floating-point keys, the bit pattern of a nonnegative IEEE number preserves order, so the same idea works on those bits.

## Pitfalls

- **Non-monotone inserts.** A key below $last$ has no correct bucket. Without the check of line L1, it goes to some bucket and is returned too late, which breaks Dijkstra's algorithm without an error.
- **Refilling from the live bucket.** Lines L6 and L7 take the list $S$ out of $B[i]$ before they redistribute it. A program that loops over $B[i]$ while it appends to the buckets works only because no item goes back to $B[i]$; a later change, such as a decrease-key that can reach $B[i]$, then breaks it. Take the list out first.
- **Using the difference instead of the exclusive or.** The bucket of $k$ is fixed by $k \oplus last$, not by $k - last$. With the difference, keys in higher buckets would have to move after every change of $last$, and the moves bound fails.
- **Number of buckets.** With 64-bit keys there are 65 buckets, $B[0]$ to $B[64]$. An array of 64 buckets misses the keys whose top bit differs from $last$.
- **Ties.** Many items can have the key $last$. They all stay in $B[0]$ and are returned in any order, which is correct for a priority queue but not stable.

## Implementations

The Python version stores (key, value) pairs in lists and grows the list of buckets when a larger key arrives, so it works for keys of any size. It counts the moves of the refills, and the tests check this count against the bound of one move per bit.

## History

Ravindra Ahuja, Kurt Mehlhorn, James Orlin and Robert Tarjan introduced radix heaps in their 1990 paper on faster shortest path algorithms, in the interval form, as a way to beat the $O(m + n \log n)$ of Fibonacci heaps when the weights are small integers. The form with the exclusive or of this page is a later simplification with the same moves argument. Cherkassky, Goldberg and Silverstein studied multilevel bucket structures for the same monotone setting in 1999, and Thorup later gave deterministic integer priority queues that make Dijkstra's algorithm run in linear time for undirected graphs.

## References
