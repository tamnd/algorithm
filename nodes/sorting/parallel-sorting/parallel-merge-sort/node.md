---
tag: J1JZCG
kind: algorithm
slug: parallel-merge-sort
name: Parallel merge sort
aliases:
- multithreaded merge sort
- parallel mergesort
area: sorting/parallel-sorting
level: core
summary: Merge sort in which the two recursive calls and the merge run in parallel.
solves: [parallel-sorting-problem]
model: work-span-model
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  depth: {worst: O(log³ n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [merge-sort, parallel-merging-problem, work-span-model, binary-search]
see_also: [merge-sort, parallel-merging-problem, merge-path, cole-merge-sort, sample-sort, parallel-quicksort, brent-theorem, fork-join-model]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.3, Parallel merge sort (P-MERGE with work Theta(n) and span Theta(log^2 n), and P-MERGE-SORT with span Theta(log^3 n))
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.3, Multithreaded merge sort
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting (merging by ranking, and merge sort on the PRAM)
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: the pipelined merge sort with time O(log n) on n processors
---

Parallel merge sort is [merge sort](/merge-sort/) in which the two recursive calls run at the same time and the merge itself is parallel. The merge picks the middle item of the longer input, finds its place in the other input by [binary search](/binary-search/), writes it, and then merges the two sides in parallel. In the [work-span model](/work-span-model/) the sort has work $\Theta(n \log n)$, the same as the sequential sort, and span $O(\log^3 n)$. It is stable and deterministic, and it is the standard example of a [fork-join](/fork-join-model/) sort.

## In plain words

To sort a large stack of cards, split it into two halves and give each half to a helper. The helpers sort their halves at the same time, in the same way, with more helpers.

Then the two sorted halves must become one. A single person would do this card by card, which is slow. Instead, take the middle card of the larger half and find where it belongs in the other half. That card now has its final place, and it cuts both halves into a left part and a right part. The two left parts and the two right parts can be merged by two different helpers at the same time, in the same way.

Each cut leaves at most three quarters of the cards on either side, so the cuts soon reach single cards.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys from a total order. The output is the same array in non-decreasing order, and equal keys keep their input order. This is the [parallel sorting problem](/parallel-sorting-problem/) in the [work-span model](/work-span-model/): the cost of the algorithm is its work $T_1$, the total number of steps, and its span $T_\infty$, the length of the longest chain of steps that must run one after the other. The inner step is the [parallel merging problem](/parallel-merging-problem/).

## The algorithm

P-MERGE-SORT sorts $A[lo \ldots hi-1]$ with a temporary array $T$ of length $n$. P-MERGE merges the sorted ranges $X[a_1 \ldots a_2 - 1]$ and $Y[b_1 \ldots b_2 - 1]$ into $Z[c \ldots]$. A `spawn` lets the called procedure run in parallel with the next line, and `sync` waits for all spawned calls of the procedure.

```pseudo id=main
P-MERGE-SORT(A, lo, hi)                    ▷ sort A[lo .. hi − 1]
L1  if hi − lo ≤ 1 then return
L2  mid ← ⌊(lo + hi) / 2⌋
L3  spawn P-MERGE-SORT(A, lo, mid)
L4  P-MERGE-SORT(A, mid, hi)
L5  sync
L6  parallel for i ← lo to hi − 1 do T[i] ← A[i]
L7  P-MERGE(T, lo, mid, T, mid, hi, A, lo)

P-MERGE(X, a₁, a₂, Y, b₁, b₂, Z, c)
L8  n_a ← a₂ − a₁;  n_b ← b₂ − b₁
L9  if n_a + n_b = 0 then return
L10 if n_a ≥ n_b then                      ▷ split on the middle item of X
L11     q ← a₁ + ⌊n_a / 2⌋
L12     r ← least index in [b₁, b₂] with r = b₂ or Y[r] ≥ X[q]
L13     t ← c + (q − a₁) + (r − b₁)
L14     Z[t] ← X[q]
L15     spawn P-MERGE(X, a₁, q, Y, b₁, r, Z, c)
L16     P-MERGE(X, q + 1, a₂, Y, r, b₂, Z, t + 1)
L17     sync
L18 else                                   ▷ split on the middle item of Y
L19     q ← b₁ + ⌊n_b / 2⌋
L20     r ← least index in [a₁, a₂] with r = a₂ or X[r] > Y[q]
L21     t ← c + (r − a₁) + (q − b₁)
L22     Z[t] ← Y[q]
L23     spawn P-MERGE(X, a₁, r, Y, b₁, q, Z, c)
L24     P-MERGE(X, r, a₂, Y, q + 1, b₂, Z, t + 1)
L25     sync
```

Lines L12 and L20 are binary searches. They use different tests on purpose. When the split item comes from $X$, the items of $Y$ equal to it go to its right. When the split item comes from $Y$, the items of $X$ equal to it go to its left. So in both cases each item of $X$ comes before each equal item of $Y$, and the sort is stable. The two calls on lines L15 and L16, and on lines L23 and L24, write to disjoint parts of $Z$, so they do not interfere.

## Example

Sort $A = [38, 27, 43, 3, 9, 82, 10]$. The recursion sorts $[38, 27, 43, 3]$ into $[3, 27, 38, 43]$ and $[9, 82, 10]$ into $[9, 10, 82]$ in parallel. The last merge then runs as follows, with $X = [3, 27, 38, 43]$, $Y = [9, 10, 82]$ and output positions $0$ to $6$.

| call | inputs | split item | rank in the other input | written at |
| --- | --- | --- | --- | --- |
| 1 | $[3, 27, 38, 43]$, $[9, 10, 82]$ | $38$ from $X$ | $2$ | $0 + 2 + 2 = 4$ |
| 2 | $[3, 27]$, $[9, 10]$ | $27$ from $X$ | $2$ | $0 + 1 + 2 = 3$ |
| 3 | $[43]$, $[82]$ | $43$ from $X$ | $0$ | $5 + 0 + 0 = 5$ |
| 4 | $[3]$, $[9, 10]$ | $10$ from $Y$ | $1$ | $0 + 1 + 1 = 2$ |
| 5 | $[\,]$, $[82]$ | $82$ from $Y$ | $0$ | $6 + 0 + 0 = 6$ |
| 6 | $[3]$, $[9]$ | $3$ from $X$ | $0$ | $0 + 0 + 0 = 0$ |
| 7 | $[\,]$, $[9]$ | $9$ from $Y$ | $0$ | $1 + 0 + 0 = 1$ |

Calls 2 and 3 are the two halves of call 1 and run at the same time. Call 4 is the left half of call 2, call 5 is the right half of call 3, and calls 6 and 7 are the halves of call 4. The output is $[3, 9, 10, 27, 38, 43, 82]$. The longest chain of calls is $1, 2, 4, 6$, of length 4, while the sequential merge would take 6 comparisons one after the other.

## Correctness

Each call of P-MERGE writes its split item to the position that the [cross-rank formula](/parallel-merging-problem/) gives for the stable merge: the items before it are the items of its own input to its left, plus the items of the other input that come before it in the stable order, which the binary search counts. The two recursive calls get exactly the items before and after the split item, so by induction on the number of items each item is written once, to its correct position. P-MERGE-SORT is then correct by induction on $hi - lo$, as for sequential merge sort. The full proof, with the stability argument, is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are in the [work-span model](/work-span-model/), with unit cost for each comparison, each read or write and each spawn.

**Split sizes.** Let a call of P-MERGE have $N = n_a + n_b$ items. Each recursive call gets at most $3N/4$ items. In the case $n_a \ge n_b$, we have $n_b \le N/2$, and the left call gets at most $n_a/2 + n_b = N/2 + n_b/2 \le 3N/4$ items. The right call gets fewer. The other case is the same with the roles swapped.

**P-MERGE.** The binary search costs $O(\log N)$, and the split sizes give the span recurrence $S(N) \le S(3N/4) + O(\log N)$, so the span is $O(\log^2 N)$. The work satisfies $W(N) = W(N_1) + W(N_2) + O(\log N)$ with $N_1 + N_2 = N - 1$ and both parts at least $N/4 - 1$, and this solves to $W(N) = \Theta(N)$. The proof is in [the proof of correctness](proofs/correctness.md).

**P-MERGE-SORT.** The copy on line L6 is a [parallel loop](/parallel-for/) with work $\Theta(n)$ and span $O(\log n)$. So the work is $W(n) = 2W(n/2) + \Theta(n) = \Theta(n \log n)$, and the span is $S(n) = S(n/2) + O(\log^2 n) = O(\log^3 n)$.

**Parallelism.** The [parallelism](/parallelism/) is $T_1/T_\infty = \Omega(n / \log^2 n)$. By [Brent's theorem](/brent-theorem/), a greedy scheduler on $p$ processors finishes in time $O(n \log n / p + \log^3 n)$, which is $O(n \log n / p)$ for $p = O(n / \log^2 n)$.

**Space.** The array $T$ takes $n$ cells. Each recursive call uses $O(1)$ local space, and the stack of one chain of calls has depth $O(\log^2 n)$.

## Properties

- **Stable.** The tie rules on lines L12 and L20 keep equal keys in input order.
- **Work-efficient.** The work matches the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/), so the algorithm is [work-efficient](/work-efficiency/).
- **Deterministic.** The calls, and so the work and span, depend only on the input.
- **Not in place.** It uses an extra array of $n$ cells.
- **Comparison-based.** It accesses keys only through comparisons.
- **Race-free.** Parallel calls read shared input but write disjoint output ranges, so the result does not depend on the schedule.

## Variants and improvements

- **A faster merge.** A merge with work $O(N)$ and span $O(\log N)$ gives a sort with span $O(\log^2 n)$ and the same work. The [merge path](/merge-path/) method does this: it cuts the output into $N / \log N$ pieces by binary search on diagonals and merges each piece sequentially.
- **Pipelined merges.** [Cole's merge sort](/cole-merge-sort/) overlaps the merges of all levels and sorts in time $O(\log n)$ with $n$ processors on the CREW and EREW PRAM.
- **Coarsening.** Below a grain size of a few thousand keys, both the sort and the merge switch to the sequential versions. This removes most of the cost of spawns and does not change the bounds.
- **Ping-pong buffers.** Alternating the roles of $A$ and $T$ between levels removes the copy on line L6.
- **Multiway merge.** Splitting into $p$ parts and merging them in one pass is the idea behind [sample sort](/sample-sort/) and [parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/), which move each key fewer times.

## When to use it

Use parallel merge sort on a shared-memory machine when the sort must be stable and deterministic, or when worst-case bounds matter. When stability does not matter, [parallel quicksort](/parallel-quicksort/) and sample sort often run faster because they need no extra array and move keys fewer times. For integer keys, [parallel radix sort](/parallel-radix-sort/) is often faster.

## Pitfalls

- **Sequential merge.** With a sequential merge, the span is $S(n) = S(n/2) + \Theta(n) = \Theta(n)$, and the parallelism is only $\Theta(\log n)$.
- **Wrong tie rule.** If both binary searches use the same test, equal keys from the two inputs can change order, and the sort is no longer stable.
- **Split on the shorter input.** If the split item comes from the shorter input, one side can keep almost all of the longer input, and the span bound fails.
- **Overlapping buffers.** The merge reads $T$ and writes $A$. Merging in place inside one array overwrites keys that other calls still read.
- **Too fine a grain.** Spawning a task for each key costs much more than the comparison it does. Without coarsening, the parallel sort is often slower than the sequential one.

## Implementations

## History

Merging by ranks is a basic PRAM method, and the textbook of JaJa uses it for merge sort on the PRAM. Cole published the pipelined version with time $O(\log n)$ in 1988. The fork-join form on this page, with the split on the longer input and the bounds of work $\Theta(n \log n)$ and span $\Theta(\log^3 n)$, is the one in the chapter on multithreaded algorithms that Cormen, Leiserson, Rivest and Stein added in the third edition of their textbook in 2009.

## References
