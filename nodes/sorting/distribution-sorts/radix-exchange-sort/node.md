---
tag: Y3DQBZ
kind: algorithm
slug: radix-exchange-sort
name: Radix exchange sort
aliases:
- Binary quicksort
- Binary radix sort
area: sorting/distribution-sorts
level: advanced
summary: MSD radix sort on bits, partitioning each recursion level by the current bit of the keys.
solves: [integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of keys, w: the number of bits per key}
  time: {worst: Θ(n w), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: O(w)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: true, comparison: false, recursive: true}
history: {year: 1959, people: [Paul Hildebrandt, Harold Isbitz], note: radix exchange sorting on binary computers}
prereqs: [quicksort, positional-number-system]
see_also: [msd-radix-sort, quicksort, american-flag-sort, radix-sort, trie, three-way-radix-quicksort, integer-sorting, in-place-algorithm]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by Exchanging (Algorithm R, Radix exchange sort, its analysis, and the comparison with quicksort), and Section 6.3, Digital Searching (the link with binary tries)
  - paper: Paul Hildebrandt and Harold Isbitz, Radix exchange, an internal sorting method for digital computers, Journal of the ACM 6(2), 1959, pages 156 to 163
    locator: the description of the method (partition on one bit by exchanges from both ends, then the next bit in each part)
---

Radix exchange sort is an [MSD radix sort](/msd-radix-sort/) with base 2 that works in place: it splits the keys by their most significant bit, with exchanges from both ends of the array as in [quicksort](/quicksort/), then sorts the part with bit 0 and the part with bit 1 on the next bit. Hildebrandt and Isbitz described it in 1959, and Knuth gives it as Algorithm R of Section 5.2.2. On $n$ keys of $w$ bits it takes $O(n w)$ time in the worst case, and about $n \lg n$ bit inspections on random keys, because a part stops as soon as it has at most one key. Its recursion has the shape of a binary [trie](/trie/) of the keys.

## In plain words

Write every number in binary, as a row of 0s and 1s of the same length. Look at the first digit. Put the numbers that start with 0 to the left and those that start with 1 to the right. To do this in place, walk in from both ends: from the left, find a number that starts with 1; from the right, find a number that starts with 0; swap them, and go on until the two walks meet.

Every number on the left is now smaller than every number on the right. Do the same inside each side with the second digit, then the third, and so on. A group with one number, or a group in which all digits are used up, is done.

## The problem

The input is an array $A[0 \ldots n-1]$ of non-negative integers below $2^w$. The output is the same keys in non-decreasing order. Write $\mathrm{bit}(x, b)$ for bit $b$ of $x$, where bit $w - 1$ is the most significant and bit 0 the least. Signed keys can be handled by flipping the sign bit first, see [integer sorting](/integer-sorting/).

## The algorithm

A task $(lo, hi, b)$ means that the keys of $A[lo \ldots hi-1]$ agree on the bits above $b$, and must be sorted by bits $b, b - 1, \ldots, 0$.

```pseudo id=main
RADIX-EXCHANGE-SORT(A, n, w)
L1  S ← a stack that holds the task (0, n, w − 1)
L2  while S is not empty do
L3      (lo, hi, b) ← pop S
L4      if hi − lo ≤ 1 or b < 0 then continue
L5      i ← lo; j ← hi − 1
L6      while i ≤ j do
L7          while i ≤ j and bit(A[i], b) = 0 do i ← i + 1
L8          while i ≤ j and bit(A[j], b) = 1 do j ← j − 1
L9          if i < j then swap A[i] and A[j]; i ← i + 1; j ← j − 1
L10     push (i, hi, b − 1) and (lo, i, b − 1) onto S
L11 return A
```

Lines L5 to L9 are the partition of quicksort with a test on one bit in place of a comparison with a pivot. When the loop ends, $A[lo \ldots i-1]$ have bit $b$ equal to 0 and $A[i \ldots hi-1]$ have bit $b$ equal to 1. Line L10 pushes both parts with the next lower bit. A task with $b < 0$ holds equal keys, because they agree on all $w$ bits.

## Example

Sort $A = [5, 2, 7, 1, 4, 6, 0, 3]$ with $w = 3$, in binary $101, 010, 111, 001, 100, 110, 000, 011$.

The first task $(0, 8, 2)$ splits on bit 2. From the left, $i$ stops at $5 = 101$; from the right, $j$ stops at $3 = 011$; they swap. Next $i$ stops at $7 = 111$ and $j$ at $0 = 000$; they swap. Then $i$ stops at $4 = 100$, and $j$ moves left past $6$ and $4$ until $j < i$. The split is at $i = 4$.

| Task $(lo, hi, b)$ | keys of the task after the split, in binary | split index |
|---|---|---|
| $(0, 8, 2)$ | 011 010 000 001 · 100 110 111 101 | 4 |
| $(0, 4, 1)$ | 001 000 · 010 011 | 2 |
| $(0, 2, 0)$ | 000 · 001 | 1 |
| $(2, 4, 0)$ | 010 · 011 | 3 |
| $(4, 8, 1)$ | 100 101 · 111 110 | 6 |
| $(4, 6, 0)$ | 100 · 101 | 5 |
| $(6, 8, 0)$ | 110 · 111 | 7 |

The result is $[0, 1, 2, 3, 4, 5, 6, 7]$ after 7 swaps. Each of the 7 tasks with two or more keys is one inner node of the binary trie of the 8 keys.

## Correctness

The invariant is that every task holds keys that agree on the bits above $b$, the tasks have disjoint ranges, and any two keys that are not in the same task are already in order. A split on bit $b$ keeps this: keys that agree on the bits above $b$ and differ at bit $b$ are in order of bit $b$, and both parts agree on one more bit. A task with $b < 0$ or with at most one key needs no work. The loop ends because each task lowers $b$ by one, and $b \ge -1$. The partition is correct because each swap exchanges a key with bit 1 on the left with a key with bit 0 on the right. The full proof is below.

## Complexity

- **Worst case.** Each level of tasks handles each key at most once, and there are at most $w$ levels, so the time is $O(n w)$. For $n$ copies of one key, every level splits nothing, and the cost is $\Theta(n w)$.
- **Random keys.** For $n$ keys with independent uniform bits and $w \ge \lg n$, a key stops when its prefix differs from all others, which happens after about $\lg n$ bits, so the number of bit inspections is about $n \lg n$. Knuth gives the exact analysis of the average.
- **Best case.** A key stays in tasks with two or more keys until its prefix is unique or all its bits are used. The tasks form a binary tree with the keys at the leaves, and each key costs one inspection per level above its leaf. For $n$ distinct keys this tree has $n$ leaves, so its total path length is at least $n \lg n$, and the best case is $\Theta(n \log n)$, reached for example by the keys $0, \ldots, n-1$ when $n$ is a power of 2.
- **Space.** The partition is in place. The stack holds at most two tasks per open level, so at most $2w + 1$ tasks.

## Properties

- **In place.** Only the stack is extra.
- **Not stable.** The exchanges move keys past each other, as in quicksort.
- **Adaptive.** It stops at the distinguishing prefix of each key, so short distinguishing prefixes make it fast.
- **Not a comparison sort.** It reads single bits.
- **Deterministic.** No pivot is chosen: the split value is always the bit.

## Variants and improvements

- **Larger digits.** Splitting on $r$ bits at once gives $2^r$ parts and is [American flag sort](/american-flag-sort/) on integers.
- **Cut-off.** Small tasks run faster with [insertion sort](/insertion-sort/).
- **Skip common bits.** If all keys of a task share bit $b$, the split does nothing. Computing the bitwise OR and AND of the task, and starting at the highest bit where they differ, skips such levels.
- **Strings.** On strings with an end mark, the same scheme on the bits of the characters is a binary MSD string sort.

## When to use it

Use radix exchange sort for integer keys when the sort must be in place and the keys are close to random, so that a part ends after about $\lg n$ bits. For many equal keys or keys with long common prefixes, it pays $w$ levels; then a quicksort with three-way partition, or the skip of common bits, is better. For large inputs on a modern machine, LSD [radix sort](/radix-sort/) with 8-bit to 16-bit digits is usually faster, at the cost of a buffer.

## Pitfalls

- **Signed keys.** Negative numbers in two's complement have bit $w - 1$ set and would sort after the positive keys. Flip the sign bit first, or treat the top bit with the opposite order.
- **Floating-point keys.** The bit pattern of IEEE numbers is not in numeric order for negative values. Map the keys first, see [integer sorting](/integer-sorting/).
- **Off-by-one in the scans.** Without the tests $i \le j$ in lines L7 and L8, a scan can run past the range when all keys of the task have the same bit.
- **Equal keys.** The sort does $w$ levels of work on a group of equal keys. Stop when $b < 0$, as in line L4, or detect equal keys early.

## Implementations

## History

Hildebrandt and Isbitz (1959) published radix exchange as an internal sort for binary computers, two years before Hoare published quicksort, which uses the same exchange pattern with a pivot in place of a bit. Knuth (Section 5.2.2) presents it as Algorithm R, analyses its average cost, and relates it to binary tries and to digital search in Section 6.3.

## References
