---
tag: FQMV6V
kind: algorithm
slug: counting-sort
name: Counting sort
aliases:
- Key-indexed counting
- Distribution counting
area: sorting/distribution-sorts
level: intro
summary: Sorts n integers in [0,k) in O(n+k) time by counting keys and prefix-summing the counts.
solves: [integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of items, k: the number of possible key values}
  time: {worst: Θ(n + k), average: Θ(n + k), best: Θ(n + k)}
  space: {extra: Θ(n + k)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1954
  people: [Harold H. Seward]
  note: Knuth credits distribution counting to H. H. Seward, who described it in 1954 for use with radix sorting.
prereqs: [sorting-problem, prefix-sums, asymptotic-notation]
see_also: [radix-sort, pigeonhole-sort, bucket-sort, integer-sorting, stable-sort, comparison-sort-lower-bound, distribution-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.2, Counting sort
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 5, Section 5.1, String Sorts, subsection Key-indexed counting
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2, Algorithm D (distribution counting), and the history in the same section
---

Counting sort sorts $n$ items whose keys are integers in $\{0, 1, \ldots, k-1\}$: it counts how many items have each key, turns the counts into start positions with a [prefix sum](/prefix-sums/), and then copies each item to its final position. It runs in $\Theta(n + k)$ time and uses $\Theta(n + k)$ extra space. It makes no comparisons between keys, so the $\Omega(n \log n)$ [lower bound for comparison sorts](/comparison-sort-lower-bound/) does not apply to it, and for $k = O(n)$ it sorts in linear time. It is [stable](/stable-sort/), which makes it the standard digit sort inside [LSD radix sort](/radix-sort/).

## In plain words

A teacher has a pile of exam papers, each with a grade from 0 to 5, and wants them in order of grade. First she counts the papers of each grade: two papers with grade 0, none with grade 1, two with grade 2, and so on. From the counts she knows where each grade starts in the final pile: the grade 0 papers take the first two places, so the grade 2 papers start at place three. Then she goes through the pile one time from the top and puts each paper in the next free place for its grade.

She never compares two papers with each other. She only looks at each grade one time to count it and one time to place the paper. Papers with the same grade stay in the order that they had in the original pile.

## The problem

The input is an array $A[0 \ldots n-1]$ of items and a function $\mathrm{key}$ that maps each item to an integer in $\{0, \ldots, k-1\}$. The output is an array $B[0 \ldots n-1]$ that holds the same items, ordered so that $\mathrm{key}(B[0]) \le \mathrm{key}(B[1]) \le \cdots \le \mathrm{key}(B[n-1])$. Items with equal keys must keep their input order. This is the [integer sorting](/integer-sorting/) problem with a universe of size $k$, plus stability.

## The algorithm

```pseudo id=main
COUNTING-SORT(A, n, k, key)                ▷ keys are in 0 .. k − 1
L1  C ← an array of k zeros
L2  for i ← 0 to n − 1 do                  ▷ pass 1: count
L3      C[key(A[i])] ← C[key(A[i])] + 1
L4  s ← 0
L5  for v ← 0 to k − 1 do                  ▷ pass 2: exclusive prefix sums
L6      t ← C[v], C[v] ← s, s ← s + t
L7  B ← a new array of n slots
L8  for i ← 0 to n − 1 do                  ▷ pass 3: place, from left to right
L9      B[C[key(A[i])]] ← A[i]
L10     C[key(A[i])] ← C[key(A[i])] + 1
L11 return B
```

Pass 1 makes $C[v]$ the number of items with key $v$. Pass 2 replaces each count by the sum of the counts before it. After line L6 has run for all $v$, $C[v]$ is the number of items with a key less than $v$, which is the index in $B$ where the block of key $v$ starts. Pass 3 reads $A$ from left to right. It writes each item at the next free slot of its block and moves that slot one place to the right. Because the pass goes from left to right, items with the same key fill their block in input order.

CLRS uses a different but equivalent form: inclusive prefix sums, so that $C[v]$ is the end of the block of $v$, and a placing pass from right to left that decrements before or after each write. Both forms are stable. The mix of the two (end positions with a left to right pass) is not, see the pitfalls.

## Example

Sort $A = [2, 5, 3, 0, 2, 3, 0, 3]$ with $k = 6$ and $\mathrm{key}(x) = x$.

After pass 1, the counts are $C = [2, 0, 2, 3, 0, 1]$ for the keys 0 to 5. After pass 2, the start positions are $C = [0, 2, 2, 4, 7, 7]$: the two 0s take slots 0 and 1, no 1s, the two 2s take slots 2 and 3, the three 3s take slots 4 to 6, and the 5 takes slot 7. Pass 3 then does this:

| $i$ | $A[i]$ | written to $B[\,\cdot\,]$ | $C$ after line L10 |
|---|---|---|---|
| 0 | 2 | 2 | [0, 2, 3, 4, 7, 7] |
| 1 | 5 | 7 | [0, 2, 3, 4, 7, 8] |
| 2 | 3 | 4 | [0, 2, 3, 5, 7, 8] |
| 3 | 0 | 0 | [1, 2, 3, 5, 7, 8] |
| 4 | 2 | 3 | [1, 2, 4, 5, 7, 8] |
| 5 | 3 | 5 | [1, 2, 4, 6, 7, 8] |
| 6 | 0 | 1 | [2, 2, 4, 6, 7, 8] |
| 7 | 3 | 6 | [2, 2, 4, 7, 7, 8] |

The result is $B = [0, 0, 2, 2, 3, 3, 3, 5]$. At the end, each $C[v]$ is the start of the block of $v + 1$, which is the end of the block of $v$. The first 3 of the input (at $i = 2$) went to slot 4, ahead of the other two 3s, so the order of equal keys is kept.

## Correctness

After pass 2, $C[v] = |\{j : \mathrm{key}(A[j]) < v\}|$ for each $v$. Pass 3 keeps this [loop invariant](/loop-invariant/) at the test of line L8: for each key $v$, $C[v]$ equals the start of block $v$ plus the number of items with key $v$ among $A[0 \ldots i-1]$, and those items are in the first slots of block $v$, in input order. At the end, block $v$ holds all items with key $v$ in input order, and the blocks are in order of $v$. So $B$ is sorted and the sort is stable. The full proof is below.

## Complexity

Lines L1 and L5 to L6 take $\Theta(k)$ time. Lines L2 to L3 and L8 to L10 take $\Theta(n)$ time. Line L7 takes $\Theta(n)$ time to allocate. Each step is an array access at a computed index or an addition, which costs $O(1)$ in the [word RAM](/word-ram/) when $k$ and $n$ fit in a word. So:

- The time is $\Theta(n + k)$ in the best, the average and the worst case. No input is faster or slower than another of the same $n$ and $k$.
- The extra space is $\Theta(k)$ for $C$ and $\Theta(n)$ for $B$.
- The time is $\Theta(n)$ when $k = O(n)$. It is worse than a $\Theta(n \log n)$ comparison sort when $k$ grows faster than $n \log n$, for example for 64-bit keys with $k = 2^{64}$.

The $\Omega(n \log n)$ bound of the [comparison model](/comparison-model/) does not apply, because line L9 uses the key as an array index. That is an operation that a comparison sort cannot do.

## Properties

- **Stable.** Pass 3 goes from left to right and fills each block from its start.
- **Not in place.** It writes to a second array $B$. An in-place version that permutes along cycles exists, but it is not stable; see [American flag sort](/american-flag-sort/).
- **Not adaptive.** A sorted input costs the same as any other input.
- **Not a comparison sort.** It never compares two keys. It needs keys that are small integers, or that map to small integers by an order-preserving function.

## Variants and improvements

- **Counting only.** If the items are the keys themselves, pass 3 is not necessary: write $C[v]$ copies of $v$ for each $v$. This is not stable, but stability has no meaning for bare integers. [Pigeonhole sort](/pigeonhole-sort/) is a close variant that puts items in lists, one list for each key.
- **Keys in a range $[lo, hi]$.** Use $\mathrm{key}(x) - lo$ and $k = hi - lo + 1$. This handles negative keys.
- **Digit sort for radix sort.** Use the $d$-th digit of the key as $\mathrm{key}$. Because counting sort is stable, [LSD radix sort](/radix-sort/) can apply it digit by digit, which handles a large $k$ with many passes over a small range.
- **Parallel counting.** Each processor counts one part of the input, and a prefix sum over all the count arrays gives each processor its own write positions. This is the base of [parallel radix sort](/parallel-radix-sort/).

## When to use it

Use counting sort when the keys are integers in a range that is not much larger than the number of items, for example bytes, ages, grades or small codes. It is also the right digit sort inside radix sort. Do not use it when $k$ is much larger than $n$: the count array costs time and memory for each possible key, used or not. For such keys use [radix sort](/radix-sort/), or a comparison sort such as [merge sort](/merge-sort/).

## Pitfalls

- **End positions with a forward pass.** If pass 2 makes inclusive sums ($C[v]$ is the end of block $v$) and pass 3 still goes from left to right with $C[v] \leftarrow C[v] - 1$ and then $B[C[v]] \leftarrow A[i]$, the result is sorted but equal keys come out in reverse order. With inclusive sums, the loop of line L8 must go from $n - 1$ down to 0, as in CLRS.
- **Off by one in line L6.** The start of block $v$ is the sum of the counts of the keys *less than* $v$. Line L6 saves $s$ before it adds $C[v]$. Adding first gives the end of the block, and the first item of key $k - 1$ is written at index $n$.
- **A key outside the range.** A key that is negative or at least $k$ writes outside $C$. Check the range or shift by the minimum key first.
- **A large range.** Sorting 1000 items with keys up to $10^9$ allocates $10^9$ counters. Measure $k$ against $n$ before you choose counting sort.

## Implementations

## History

Knuth (Section 5.2) credits the idea of distribution counting to H. H. Seward, who described it in 1954 in his master's thesis at MIT, for use with radix sorting. Sedgewick and Wayne call the method key-indexed counting, and CLRS presents it as counting sort in Chapter 8, where it is the first sort that beats the comparison lower bound.

## References
