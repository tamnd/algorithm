---
tag: JD10F7
kind: algorithm
slug: three-way-quicksort
name: Three-way quicksort
aliases:
- Dijkstra's three-way partitioning quicksort
- fat-partition quicksort
area: sorting/comparison-sorts
level: core
summary: Quicksort splitting into less-than, equal and greater-than parts; efficient for many duplicate keys.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of distinct keys}
  time: {worst: Θ(n²), average: Θ(n log k), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [quicksort, dutch-national-flag]
see_also: [bentley-mcilroy-partitioning, lomuto-partition, hoare-partition, randomized-quicksort, multikey-quicksort, dual-pivot-quicksort, shannon-entropy, pivot-selection]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (Entropy-optimal sorting, Quick3way with Dijkstra's three-way partition, and the bound in terms of the Shannon entropy)
  - paper: "Edsger W. Dijkstra, A Discipline of Programming, Prentice-Hall, 1976"
    locator: the chapter The problem of the Dutch national flag
  - paper: "Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software: Practice and Experience 23(11), 1993"
    locator: the split-end partition that keeps the equal items at the two ends and swaps them to the middle
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (quicksort with equal keys)
---

Three-way quicksort is [quicksort](/quicksort/) with a partition into three parts: the items less than the pivot $v$, the items equal to $v$, and the items larger than $v$. Only the first and the last part are sorted again, so all copies of $v$ are done after one partition. On an array of equal keys it takes linear time, where the [Lomuto partition](/lomuto-partition/) takes quadratic time. With random pivots and $k$ distinct keys, its expected cost is $O(n \log k)$, and in terms of the [Shannon entropy](/shannon-entropy/) of the keys it is within a constant factor of the best possible. This page uses Dijkstra's [Dutch national flag](/dutch-national-flag/) partition, as in Sedgewick and Wayne.

## In plain words

Quicksort picks a pivot card and splits the other cards into the smaller ones and the larger ones. If many cards have the same value as the pivot, a two-way split puts them all on one side, and they are split again and again for no gain.

Three-way quicksort makes three piles: smaller than the pivot, equal to the pivot, and larger. The middle pile is done at once, because all its cards are equal. Only the other two piles need more work. When there are only a few different values, the piles of equal cards are large, and the sort finishes fast.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, and possibly many equal keys. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm sorts in place.

## The algorithm

The call THREE-WAY-QUICKSORT$(A, 0, n)$ sorts the full array. The range $[lo, hi)$ is half-open. The pivot is the middle item of the range; a random item is the safer choice, as in [randomized quicksort](/randomized-quicksort/).

```pseudo id=main
THREE-WAY-QUICKSORT(A, lo, hi)             ▷ sort A[lo .. hi − 1]
L1  if hi − lo ≤ 1 then return
L2  v ← A[lo + ⌊(hi − lo)/2⌋]
L3  lt ← lo;  i ← lo;  gt ← hi
L4  while i < gt do
L5      if A[i] < v then
L6          swap A[lt] and A[i];  lt ← lt + 1;  i ← i + 1
L7      else if v < A[i] then
L8          gt ← gt − 1;  swap A[i] and A[gt]
L9      else i ← i + 1
L10 THREE-WAY-QUICKSORT(A, lo, lt)
L11 THREE-WAY-QUICKSORT(A, gt, hi)
```

During the loop the range has four parts:

- $A[lo \ldots lt-1]$ holds the items less than $v$,
- $A[lt \ldots i-1]$ holds the items equal to $v$,
- $A[i \ldots gt-1]$ is not yet seen,
- $A[gt \ldots hi-1]$ holds the items larger than $v$.

A small item at $i$ is swapped with the first equal item, so both of these parts move one place right. A large item at $i$ is swapped with the last unseen item, and the large part grows to the left; the new item at $i$ is not yet seen, so $i$ stays. An equal item extends the equal part. The pivot itself is one of the equal items, so the equal part is never empty at the end. Lines L10 and L11 sort the small and the large parts.

## Example

Sort $A = [3, 1, 3, 2, 2, 1, 2, 3]$. The pivot is $v = A[4] = 2$. The table shows the partition of lines L3 to L9. The comparisons are the calls of `<`: one for a small item, and two for an equal or large item.

| $A[i]$ | case | the array after the step | $lt$ | $i$ | $gt$ |
|---|---|---|---|---|---|
| 3 | large: swap $A[0], A[7]$ | 3 1 3 2 2 1 2 3 | 0 | 0 | 7 |
| 3 | large: swap $A[0], A[6]$ | 2 1 3 2 2 1 3 3 | 0 | 0 | 6 |
| 2 | equal | 2 1 3 2 2 1 3 3 | 0 | 1 | 6 |
| 1 | small: swap $A[0], A[1]$ | 1 2 3 2 2 1 3 3 | 1 | 2 | 6 |
| 3 | large: swap $A[2], A[5]$ | 1 2 1 2 2 3 3 3 | 1 | 2 | 5 |
| 1 | small: swap $A[1], A[2]$ | 1 1 2 2 2 3 3 3 | 2 | 3 | 5 |
| 2 | equal | 1 1 2 2 2 3 3 3 | 2 | 4 | 5 |
| 2 | equal | 1 1 2 2 2 3 3 3 | 2 | 5 | 5 |

The loop stops with $lt = 2$ and $gt = 5$, after 14 comparisons. The three items equal to 2 are at indices 2 to 4 and are done. The calls on $[1, 1]$ and $[3, 3, 3]$ each finish after one partition, with 4 and 6 comparisons, because each of these parts is all equal. The total is 24 comparisons.

## Correctness

The invariant of the loop of line L4 is:

> $lo \le lt \le i \le gt \le hi$, each item of $A[lo \ldots lt-1]$ is less than $v$, each item of $A[lt \ldots i-1]$ is equal to $v$, each item of $A[gt \ldots hi-1]$ is larger than $v$, and the range holds the same items as at the start.

It holds at the start, when the three known parts are empty. Each case of lines L5 to L9 keeps it, as the description above shows, and each step makes $gt - i$ smaller by one, so the loop stops after $hi - lo$ steps with $i = gt$. Then the range is the small part, the equal part, and the large part. The equal part holds the pivot, so each recursive call is on fewer items than the range. By strong induction on $hi - lo$, the calls sort the two outer parts, and then the whole range is sorted. The full proof is below.

## Complexity

**The partition.** The loop of lines L4 to L9 runs $m = hi - lo$ times. A small item costs one comparison, and an equal or large item costs two. So a partition takes $\Theta(m)$ time with between $m$ and $2m$ comparisons. With a three-way comparison, such as `compareTo` in Java, each item costs one call.

**Equal keys.** If all $n$ keys are equal, the first partition puts all items in the equal part, and lines L10 and L11 are calls on empty ranges. So the time is $\Theta(n)$, with $2n$ comparisons. This is the best case. The Lomuto partition takes $\Theta(n^2)$ on the same input.

**Few distinct keys.** Each partition puts all copies of its pivot in their final place. Consider the tree of pivots, one node for each distinct key that is a pivot. The keys are at most $k$, and so is the number of levels. Each level of the recursion does $O(n)$ work in all. With random pivots the expected depth of the tree is $O(\log k)$, so the expected time is $O(n \log k)$.

**The entropy bound.** Let the $k$ distinct keys occur $n_1, \ldots, n_k$ times, with $p_i = n_i / n$, and let $H = -\sum_i p_i \lg p_i$ be the Shannon entropy, so $H \le \lg k$. The number of different sorted outputs of a sort is $n!/(n_1! \cdots n_k!)$, so a [decision tree](/decision-tree-model/) with three-way comparisons needs about $nH - O(n)$ comparisons in the worst case. Sedgewick and Wayne state that three-way quicksort with random pivots uses about $(2 \ln 2)\, n H \approx 1.39\, nH$ three-way comparisons on average. So it is within a constant factor of the lower bound for each distribution of the keys. For distinct keys, $H = \lg n$, and the bound is the usual $1.39\, n \lg n$.

**Measured counts.** For $n = 100{,}000$ random keys from $k$ values, the code below makes these numbers of `<` comparisons:

| $k$ | 2 | 10 | 100 | $10^6$ |
|---|---|---|---|---|
| comparisons | 250,022 | 499,410 | 1,184,329 | 3,164,343 |

The count grows with $\log k$, not with $\log n$. For nearly distinct keys, the two tests per item make it about $1.5$ times the count of a two-way quicksort.

**The worst case.** With a fixed pivot rule and distinct keys, some inputs make each pivot the least or the largest item of its range, and the time is $\Theta(n^2)$, as for plain quicksort. With random pivots this is very unlikely.

**Space.** The recursion is as deep as the pivot tree, which is $O(\log n)$ on average and $n$ in the worst case. Recursing on the smaller part first bounds it by $\lfloor \lg n \rfloor$; see [quicksort stack depth](/quicksort-stack-depth/).

| claim | model and case | bound |
|---|---|---|
| time | worst case, distinct keys | $\Theta(n^2)$ |
| time | expected, random pivots, $k$ distinct keys | $O(n \log k)$ |
| comparisons | expected, random pivots, three-way comparisons | about $(2 \ln 2)\, nH$ |
| time | all keys equal | $\Theta(n)$ |
| extra space | worst case, as written | $\Theta(n)$ |

## Properties

- **Not stable.** The swaps of lines L6 and L8 move items past equal items. On $(2, a), (2, b), (1, c)$ with $v = (2, b)$, the first step finds $(2, a)$ equal, the next finds $(2, b)$ equal, and then $(1, c)$ is swapped with $(2, a)$; the output is $(1, c), (2, b), (2, a)$.
- **In place.** It uses $O(1)$ extra space besides the stack.
- **Adapts to equal keys.** The more equal keys, the less work. It is not adaptive to order: a sorted input costs as much as other inputs.
- **More swaps than Hoare.** On distinct keys, Dijkstra's partition makes more swaps than the [Hoare partition](/hoare-partition/), because each large item is swapped and each small item is swapped with the first equal item.

## Variants and improvements

- **[Bentley-McIlroy partitioning](/bentley-mcilroy-partitioning/).** Scan from both ends as in the Hoare partition, put the items equal to $v$ at the two ends of the range, and swap them to the middle at the end. It makes as few swaps as the Hoare partition on distinct keys and still groups the equal keys.
- **Random pivot.** Pick $v$ at random. Then the expected bounds hold on every input.
- **[Dual-pivot quicksort](/dual-pivot-quicksort/).** Split around two pivots $p \le q$ into the parts less than $p$, between $p$ and $q$, and larger than $q$. It also has three parts, but the middle part is not done.
- **[Multikey quicksort](/multikey-quicksort/).** For strings, compare one character at a time and partition three ways on it. The equal part goes on with the next character.
- **Cut-off to insertion sort.** Sort ranges of fewer than about 10 items by insertion sort.

## When to use it

Use three-way quicksort when the keys have many duplicates, for example sorting records by a field with few values, such as a country, a status or a grade. It is also a safe default for a general quicksort, because the cost of the equal part is small when keys are distinct, and the gain is large when they are not. When the keys are known to be distinct and swaps are costly, a two-way Hoare partition is faster. When stability matters, use [merge sort](/merge-sort/) or [Timsort](/timsort/).

## Pitfalls

- **Advancing $i$ after a large item.** After the swap of line L8, the item at $i$ comes from the unseen part. If the code also does $i \leftarrow i + 1$, it skips that item, and the partition is wrong.
- **Comparing with a moving pivot.** The pivot value $v$ must be saved at line L2. If the code compares with $A[\text{mid}]$ instead, the item at that index can change during the loop.
- **Recursing on the equal part.** The calls must be on $[lo, lt)$ and $[gt, hi)$. A call that includes the equal part repeats work and can loop forever on equal keys.
- **A fixed pivot on hostile input.** The middle item is good on sorted input, but some inputs are still quadratic. Use a random pivot where the input can be chosen by an attacker.
- **Two comparisons per item.** With only `<`, an item that is not small costs two comparisons. When comparisons are costly, as for long strings, use a three-way comparison that returns less, equal or greater in one call.

## Implementations

## History

Dijkstra posed the problem of the Dutch national flag, the sort of an array of three colours in one pass, in A Discipline of Programming in 1976, and his partition is the one of this page. Bentley and McIlroy published a faster three-way partition for the C library sort in 1993. Sedgewick and Wayne present the method as entropy-optimal sorting, with the bound in terms of the Shannon entropy.

## References
