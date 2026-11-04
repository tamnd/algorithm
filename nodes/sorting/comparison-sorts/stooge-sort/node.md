---
tag: Y4SMX5
kind: algorithm
slug: stooge-sort
name: Stooge sort
area: sorting/comparison-sorts
level: intro
summary: Recursively sorts two-thirds of the array three times; a correct but inefficient divide-and-conquer sort, about n^2.7 time.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n^2.7095), average: Θ(n^2.7095), best: Θ(n^2.7095)}
  space: {extra: Θ(log n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [master-theorem, recursion]
see_also: [bubble-sort, insertion-sort, merge-sort, master-theorem, recurrence-relation, sorting-problem]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 7-3, Stooge sort (the procedure STOOGE-SORT, its correctness and its running time)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.5, The master method for solving recurrences (Theorem 4.1)
  - paper: "Andrei Broder and Jorge Stolfi, Pessimal algorithms and simplexity analysis, ACM SIGACT News 16(3), 1984"
    locator: the section on slowsort, a sort by multiply and surrender
---

Stooge sort is a recursive sort that is correct but very slow. It sorts the first two-thirds of the array, then the last two-thirds, then the first two-thirds again. The overlap of the two parts is large enough that the largest third of the items reaches the end in the second call. Its time obeys $T(n) = 3T(\lceil 2n/3 \rceil) + \Theta(1)$, which the [master theorem](/master-theorem/) solves as $\Theta(n^{\log_{3/2} 3}) = \Theta(n^{2.7095\ldots})$, slower than [bubble sort](/bubble-sort/) and [insertion sort](/insertion-sort/). It is a classic exercise in [recursion](/recursion/), in proofs of correctness by induction, and in solving recurrences; it is not used in practice.

## In plain words

You have a row of cards. If the first card is larger than the last card, you swap them. If the row has three or more cards, you do three steps. First you sort the first two-thirds of the row, with the same method. Then you sort the last two-thirds. Then you sort the first two-thirds again.

Why does this work? After the first step, the largest cards of the first two-thirds are at its right end, which is in the middle of the row. So after the first step, all the largest cards of the whole row are in the last two-thirds. The second step puts them at the end in order. The third step sorts what is left.

The method does a lot of repeated work, because each step calls the method again, three times, on large parts. So it is much slower than the simple sorts.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place. It is called as STOOGE-SORT$(A, 0, n - 1)$ for $n \ge 1$; the range $[lo, hi]$ includes both ends.

## The algorithm

```pseudo id=main
STOOGE-SORT(A, lo, hi)                     ▷ sorts A[lo .. hi], with lo ≤ hi
L1  if A[hi] < A[lo] then swap A[lo] and A[hi]
L2  if hi − lo + 1 ≥ 3 then
L3      k ← ⌊(hi − lo + 1) / 3⌋
L4      STOOGE-SORT(A, lo, hi − k)          ▷ the first two-thirds
L5      STOOGE-SORT(A, lo + k, hi)          ▷ the last two-thirds
L6      STOOGE-SORT(A, lo, hi − k)          ▷ the first two-thirds again
```

Let $m = hi - lo + 1$. Line L1 sorts a range of two items, and it is the only line that compares or moves items. For $m \ge 3$, the three calls work on ranges of $m - k = \lceil 2m/3 \rceil$ items. The rounding matters: each part must have at least $m - k \ge 2k$ items, so that the two parts overlap in at least $k$ items, the size of the last third.

## Example

Sort $A = [5, 1, 4, 2, 3]$. Here $m = 5$ and $k = 1$, so the parts are $A[0 \ldots 3]$ and $A[1 \ldots 4]$.

| call | the step | the array after it |
|---|---|---|
| $(0, 4)$, line L1 | $3 < 5$: swap | 3 1 4 2 5 |
| $(0, 3)$, line L4 | sorts $A[0 \ldots 3]$ | 1 2 3 4 5 |
| $(1, 4)$, line L5 | sorts $A[1 \ldots 4]$, no change | 1 2 3 4 5 |
| $(0, 3)$, line L6 | sorts $A[0 \ldots 3]$, no change | 1 2 3 4 5 |

The call on $A[0 \ldots 3]$ in line L4 swaps 3 and 2 in its line L1, then 2 and 1, then 4 and 3 in its inner calls. So the array is sorted after 4 swaps, but the algorithm still runs the calls of lines L5 and L6 in full. In total it makes 40 calls and 40 comparisons, one per call. A sort of 5 items needs at most 7 comparisons, and insertion sort makes at most 10.

## Correctness

The proof is by strong induction on $m = hi - lo + 1$. For $m = 1$ and $m = 2$, line L1 sorts the range. For $m \ge 3$, let $k = \lfloor m/3 \rfloor$, and let $L$ be the $k$ largest items of the range (with ties broken by a fixed order of the items). The key fact is:

> After line L4, all the items of $L$ are in $A[lo + k \ldots hi]$.

The items of $L$ in the last $k$ positions are not touched by line L4. The items of $L$ in the first part $A[lo \ldots hi - k]$ are now its largest items, so after line L4 they are at the right end of that part, in its last $k$ positions or fewer. The first part has $m - k \ge 2k$ items, so these positions are at index $lo + k$ or later. Then line L5 sorts $A[lo + k \ldots hi]$, which puts the items of $L$ in its last $k$ positions, in order. These are the last $k$ positions of the full range. Line L6 sorts the other items, all at most the items of $L$, into $A[lo \ldots hi - k]$. So the range is sorted. Each step is a swap, so the range keeps its items. The full proof is below.

## Complexity

**Comparisons.** Each call makes exactly one comparison, in line L1, and the number of calls does not depend on the values. Let $C(m)$ be the number of calls on a range of $m$ items. Then $C(1) = C(2) = 1$, and for $m \ge 3$,

$$C(m) = 1 + 3\,C(m - \lfloor m/3 \rfloor).$$

The first values are $C(3) = 4$, $C(4) = 13$, $C(5) = C(6) = 40$, $C(7) = C(8) = C(9) = 121$, and $C(10) = 364$: each value is $(3^{d+1} - 1)/2$, where $d$ is the depth of the recursion. For $n = 100$ the count is 265,720, for $n = 1000$ it is 64,570,081, and for $n = 2000$ it is 581,130,733.

**Time.** The time obeys $T(n) = 3T(\lceil 2n/3 \rceil) + \Theta(1)$. With $a = 3$ and $b = 3/2$, we have $n^{\log_b a} = n^{\log_{3/2} 3}$ and $\log_{3/2} 3 = \ln 3 / \ln 1.5 = 2.7095\ldots$. The extra work $\Theta(1)$ is $O(n^{\log_b a - \epsilon})$, so case 1 of the [master theorem](/master-theorem/) gives $T(n) = \Theta(n^{2.7095\ldots})$. The ceiling does not change the order. This holds in the best, the average and the worst case.

**Space.** The depth of the recursion is about $\log_{3/2} n$, and each call keeps $O(1)$ data, so the extra space is $\Theta(\log n)$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst, average and best | $\Theta(n^{\log_{3/2} 3}) = \Theta(n^{2.7095\ldots})$ |
| extra space | | $\Theta(\log n)$, the depth of the recursion |

## Properties

- **Not stable.** Line L1 swaps the two ends of a range, past the items between them. On $(1, a), (1, b), (0, c)$, it swaps $(1, a)$ and $(0, c)$, and the output is $(0, c), (1, b), (1, a)$.
- **In place.** It moves items only by swaps, with $O(\log n)$ space for the recursion.
- **Not adaptive.** The number of comparisons depends only on $n$. A sorted input costs as much as any other.
- **Oblivious.** The sequence of compare-exchange steps depends only on $n$, so the algorithm is a sorting network, with $\Theta(n^{2.71})$ comparators.

## Variants and improvements

- **The wrong rounding.** If line L3 uses $k = \lceil m/3 \rceil$, the parts have $\lfloor 2m/3 \rfloor$ items, and they may overlap in fewer than $k$ items. The sort then fails, for example on $[0, 2, 1, 3]$: with $k = 2$, the parts are $A[0 \ldots 1]$ and $A[2 \ldots 3]$, and the item 2 never meets the item 1.
- **Slowsort.** Broder and Stolfi's slowsort sorts both halves, moves the largest item to the end, and sorts the rest again. Its time grows faster than any polynomial. It is a joke on the method of divide and conquer, like stooge sort.
- **Real divide and conquer.** [Merge sort](/merge-sort/) also makes recursive calls on parts, but the parts do not overlap and the work to combine them is linear. This gives $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$.

## When to use it

Do not use stooge sort to sort data. Use it as an exercise: to prove a recursive algorithm correct by induction, to see why the sizes of the parts matter, and to solve a recurrence with the master theorem. For a real sort, use [insertion sort](/insertion-sort/) for very small arrays and [merge sort](/merge-sort/) or a library sort otherwise.

## Pitfalls

- **Rounding down the parts.** The parts must have $\lceil 2m/3 \rceil$ items. With $\lfloor 2m/3 \rfloor$, the sort is wrong already for $m = 4$.
- **Running time.** The time grows as $n^{2.71}$. An input of 2000 items needs more than 500 million calls, so tests must use small inputs.
- **The base case.** For $m = 1$, line L1 compares an item with itself, which is harmless. Do not call the algorithm on an empty range, because $hi = lo - 1$ is not a valid index.

## Implementations

## History

The name refers to the Three Stooges, the comedy act, because the algorithm makes its point three times. CLRS gives it as a problem in its chapter on quicksort (Problem 7-3 of the third edition), with the task to prove it correct and to find its running time, and with the remark that it is not worth using. Broder and Stolfi's 1984 paper on pessimal algorithms describes slowsort in the same spirit.

## References
