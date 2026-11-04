---
tag: Y6SQW0
kind: algorithm
slug: pigeonhole-sort
name: Pigeonhole sort
area: sorting/distribution-sorts
level: intro
summary: Places each key into a hole indexed by its value, then reads the holes in order; O(n+range) time.
solves: [integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of items, k: the size of the key range (max − min + 1)}
  time: {worst: Θ(n + k), average: Θ(n + k), best: Θ(n + k)}
  space: {extra: Θ(n + k)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
prereqs: [counting-sort]
see_also: [counting-sort, bucket-sort, radix-sort, integer-sorting, distribution-sort, bucket-queue]
sources:
  - url: "https://xlinux.nist.gov/dads/HTML/pigeonholeSort.html"
    title: Paul E. Black (editor), Dictionary of Algorithms and Data Structures, NIST, entry pigeonhole sort
    locator: entry pigeonhole sort
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.2 (counting sort) and Section 8.4 (bucket sort), of which pigeonhole sort is the case with buckets of width 1
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.5, Sorting by Distribution (one pass of list distribution into piles)
---

Pigeonhole sort sorts items with integer keys in a range $[\min, \max]$ by making one list, a *hole*, for each possible key value: it appends each item to the hole of its key, then reads the holes in increasing order of key. It takes $\Theta(n + k)$ time and space for $n$ items and $k = \max - \min + 1$ possible keys. It is the same idea as [counting sort](/counting-sort/), but it stores the items in the holes instead of counting them first, and it is the case of [bucket sort](/bucket-sort/) with buckets of width one, so no hole needs a sort of its own.

## In plain words

A cloakroom has one hook for each ticket number. To give the coats back in order of ticket number, you hang each coat on the hook with its number, and then you walk along the hooks from the lowest number to the highest and take the coats off. Two coats with the same number go on the same hook, the first one in front.

You never compare two coats. Each coat is handled twice: once to hang it up and once to take it off. But you must walk past every hook, also the empty ones. So the method is fast only when the numbers do not spread over many more hooks than there are coats.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with integer keys. The output is the same items in non-decreasing order of key, with equal keys in their input order. This is the [integer sorting](/integer-sorting/) problem, with the extra condition of stability. The cost depends on the size of the range $k = \max_i \mathrm{key}(A[i]) - \min_i \mathrm{key}(A[i]) + 1$.

## The algorithm

```pseudo id=main
PIGEONHOLE-SORT(A, n)
L1  if n = 0 then return
L2  lo ← the smallest key in A, hi ← the largest key in A
L3  k ← hi − lo + 1
L4  H[0 .. k − 1] ← k empty queues                 ▷ the holes
L5  for i ← 0 to n − 1 do
L6      append A[i] to H[key(A[i]) − lo]
L7  j ← 0
L8  for h ← 0 to k − 1 do
L9      for each item x of H[h], from the front do
L10         A[j] ← x, j ← j + 1
```

Lines L2 and L3 find the range in one pass. Line L6 puts each item into the hole of its key, after the items of the same key that came before it. Lines L8 to L10 write the holes back to $A$ in order of key, and each hole from its front. The array $A$ is then sorted.

## Example

Sort $A = [8, 3, 2, 7, 4, 6, 8, 3]$. Here $lo = 2$, $hi = 8$ and $k = 7$. To show stability, the two 3s are $3_a$ and $3_b$, and the two 8s are $8_a$ and $8_b$, in input order.

| hole $h$ | key $lo + h$ | items after lines L5 and L6 |
|---|---|---|
| 0 | 2 | 2 |
| 1 | 3 | $3_a$, $3_b$ |
| 2 | 4 | 4 |
| 3 | 5 | |
| 4 | 6 | 6 |
| 5 | 7 | 7 |
| 6 | 8 | $8_a$, $8_b$ |

Lines L8 to L10 visit the 7 holes and write $A = [2, 3_a, 3_b, 4, 6, 7, 8_a, 8_b]$. The work is 8 appends, 8 writes and 7 hole visits, one of them to the empty hole 3.

## Correctness

After the loop of lines L5 and L6, hole $h$ holds exactly the items with key $lo + h$, in input order. This holds by induction on $i$, since step $i$ appends one item to the end of one hole. Each key is in $[lo, hi]$, so $0 \le \mathrm{key} - lo < k$, and each item goes into an existing hole. The loop of lines L8 to L10 writes the holes in order of $h$, so the keys in $A$ do not decrease, and it writes each item once, so $A$ holds the input items. The full proof is below.

## Complexity

- **Time.** Lines L2 and L3 take $\Theta(n)$. Line L4 takes $\Theta(k)$. The loop of lines L5 and L6 does $n$ appends of $O(1)$ each. The loop of lines L8 to L10 visits $k$ holes and writes $n$ items, so it takes $\Theta(n + k)$. The total is $\Theta(n + k)$ in each case.
- **Space.** The $k$ holes take $\Theta(k)$ space, and the $n$ entries in them take $\Theta(n)$.
- **Linear time** when $k = O(n)$. For $k$ much larger than $n$, such as 32-bit keys with $n = 1000$, the $k$ holes dominate, and [radix sort](/radix-sort/) or a comparison sort is better.

## Properties

- **Stable.** Each hole is a queue, filled and emptied in input order.
- **Not in place.** The holes hold all $n$ items.
- **Not a comparison sort.** It uses $\mathrm{key} - lo$ as an index. The search for $lo$ and $hi$ in line L2 uses $2n - 2$ comparisons or fewer, but they do not order the items.
- **Not adaptive.** The cost depends only on $n$ and $k$.

## Variants and improvements

- **[Counting sort](/counting-sort/).** Count the keys first and compute the start of each key with a prefix sum. Then the items go straight to an output array, with no lists. This is usually faster and uses one array of $n$ items instead of $n$ list nodes.
- **Bare keys.** If the items are only integers, a hole needs only a count, not a list. Then the sort writes each key as many times as its count.
- **[Bucket sort](/bucket-sort/).** Use fewer holes, each for a range of keys, and sort each hole. This trades the $\Theta(k)$ cost for a sort inside each bucket.
- **[Bucket queue](/bucket-queue/).** The same array of holes, kept as a priority queue for small integer priorities, is the bucket queue of Dial's shortest path algorithm.

## When to use it

Use pigeonhole sort when the keys are integers in a small range, about the number of items or less, and when the items carry data, so that a list per key is natural. For bare integers, or when memory for list nodes matters, [counting sort](/counting-sort/) does the same job with arrays. For a large range, use [radix sort](/radix-sort/).

## Pitfalls

- **An empty input.** Line L2 has no smallest key when $n = 0$. Line L1 must return first.
- **Holes as stacks.** If each hole is a stack and line L9 reads from the top, items with equal keys come out in reverse order, and the sort is not stable. Line L9 reads each hole from the front.
- **A huge range.** One item with key $0$ and one with key $2^{40}$ make line L4 allocate about $10^{12}$ holes. Check $k$ against $n$ before line L4.
- **Overflow of the range.** In a language with fixed-width integers, $hi - lo + 1$ in line L3 can overflow, for example for $lo = -2^{63}$ and $hi = 2^{63} - 1$. Compute it in a wider type, or reject such a range.

## Implementations

## History

The name comes from the pigeonhole principle and from the pigeonholes of a mail rack, one per address. The method is the one-pass case of distribution into piles, as done by punched-card sorters on one column (Knuth, Section 5.2.5), with one pile for each possible value. The name pigeonhole sort is the one used in the NIST Dictionary of Algorithms and Data Structures.

## References
