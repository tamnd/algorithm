---
tag: PP7XPG
kind: algorithm
slug: randomized-quicksort
name: Randomized quicksort
aliases:
- random-pivot quicksort
- randomized Hoare sort
area: sorting/comparison-sorts
level: core
summary: Quicksort with uniformly random pivots, giving expected O(n log n) on every input.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), expected: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: false, comparison: true, recursive: true}
prereqs: [quicksort, indicator-random-variable, linearity-of-expectation]
see_also: [quicksort-expected-running-time, lomuto-partition, three-way-quicksort, pivot-selection, quicksort-stack-depth, las-vegas-algorithm, quickselect, introsort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 7.3, A randomized version of quicksort, and Section 7.4.2, Expected running time
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the algorithm RandQS and the bound on its expected number of comparisons)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.5, Application, the expected run-time of quicksort
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the mean and the variance of the number of comparisons of quicksort)
---

Randomized quicksort is [quicksort](/quicksort/) with a pivot that is chosen uniformly at random from the range at each step. On each input of $n$ distinct keys, its expected number of comparisons is $2(n+1)H_n - 4n \approx 1.39\, n \lg n$, so its expected time is $\Theta(n \log n)$. No input is bad for it: the bad cases depend only on the random choices, and they are very rare. It is always correct, and only its time is random, so it is a [Las Vegas algorithm](/las-vegas-algorithm/). It sorts in place and is not stable.

## In plain words

Plain quicksort picks a fixed card as the pivot, for example the last one. Then some orders of the cards, such as a row that is already in order, make it very slow, and anyone who knows the rule can build such a row.

Randomized quicksort picks the pivot card at random. Now no row is bad on purpose. A slow run needs bad luck at many steps in a row, and that almost never happens. On average, the random pivot lands near the middle often enough that the work grows only a little faster than the number of cards. This is the same average that plain quicksort has on a row in random order, but now it holds for each row.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm has access to a source of uniform random numbers.

## The algorithm

The call RANDOMIZED-QUICKSORT$(A, 0, n)$ sorts the full array. PARTITION is the [Lomuto partition](/lomuto-partition/) of [quicksort](/quicksort/): it puts the pivot $A[hi-1]$ at its final index $p$, the items at most the pivot before it, and the larger items after it.

```pseudo id=main
RANDOMIZED-QUICKSORT(A, lo, hi)            ▷ sort A[lo .. hi − 1]
L1  if hi − lo ≤ 1 then return
L2  r ← a uniform random integer with lo ≤ r < hi
L3  swap A[r] and A[hi − 1]                ▷ the random item becomes the pivot
L4  p ← PARTITION(A, lo, hi)
L5  RANDOMIZED-QUICKSORT(A, lo, p)
L6  RANDOMIZED-QUICKSORT(A, p + 1, hi)
```

Lines L2 and L3 are the only change to quicksort. After them, the pivot is a uniform random item of the range, whatever the order of the input. Each call makes new random choices, independent of the earlier ones.

An equivalent form shuffles the array once with the [Fisher-Yates shuffle](/fisher-yates-shuffle/) and then runs plain quicksort. Both forms have the same distribution of the comparison count.

## Example

Sort the sorted array $A = [1, 2, 3, 4, 5, 6, 7, 8]$. Plain quicksort with the last item as pivot makes $28$ comparisons here, its worst case. Suppose the random pivots are 5, then 2 and 3 on the left side, then 7 on the right side.

| range | pivot | range after line L3 | range after PARTITION | comparisons |
|---|---|---|---|---|
| $A[0 \ldots 7]$ | 5 | 1 2 3 4 8 6 7 5 | 1 2 3 4 **5** 6 7 8 | 7 |
| $A[0 \ldots 3]$ | 2 | 1 4 3 2 | 1 **2** 3 4 | 3 |
| $A[2 \ldots 3]$ | 3 | 4 3 | **3** 4 | 1 |
| $A[5 \ldots 7]$ | 7 | 6 8 7 | 6 **7** 8 | 2 |

The ranges of one item end at line L1. The run makes $13$ comparisons. The expected count for $n = 8$ is $2 \cdot 9 \cdot H_8 - 32 = 2369/140 \approx 16.9$, on this input and on each other input of 8 distinct keys.

## Correctness

The random choice changes only which item is the pivot. After line L3, the range holds the same items, and PARTITION works for each choice of the pivot. So the proof of correctness of quicksort applies to each run, whatever the random numbers are: by strong induction on $hi - lo$, each call sorts its range and changes nothing outside it. The recursion stops on each run, because each call is on a range that is smaller by at least one item. The full proof is below.

## Complexity

**The expected number of comparisons.** Assume that the keys are distinct, and let $z_1 < z_2 < \cdots < z_n$ be the items in sorted order. All comparisons are made by PARTITION, between the pivot and another item of the range. So two items are compared at most once: after the comparison, the pivot is in no later call. Let $X_{ij}$ be the [indicator random variable](/indicator-random-variable/) of the event that $z_i$ and $z_j$ are compared, for $i < j$.

Consider the set $Z_{ij} = \{z_i, z_{i+1}, \ldots, z_j\}$. While no item of $Z_{ij}$ is a pivot, all of $Z_{ij}$ stays in one range, because a pivot outside $Z_{ij}$ is smaller or larger than all of it. The first pivot from $Z_{ij}$ is uniform over its $j - i + 1$ items. If it is $z_i$ or $z_j$, the two items are compared. If it is an item between them, they go to different sides and are never compared. So $\Pr[X_{ij} = 1] = 2/(j - i + 1)$. By [linearity of expectation](/linearity-of-expectation/), with $k = j - i + 1$,

$$\mathbb{E}[X] = \sum_{i < j} \frac{2}{j - i + 1} = \sum_{k=2}^{n} \frac{2(n - k + 1)}{k} = 2(n+1)H_n - 4n,$$

where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). Since $H_n = \ln n + O(1)$, this is $2n \ln n + O(n) \approx 1.386\, n \lg n$. For $n = 1000$ the mean is about $10{,}986$, against $499{,}500$ in the worst case. The count has no dependence on the input. The page [expected running time of randomized quicksort](/quicksort-expected-running-time/) gives this proof in full.

**The expected time.** Each call does $O(1)$ work besides its comparisons, and there are at most $2n + 1$ calls. So the expected time is $\Theta(n \log n)$. It is also $\Omega(n \log n)$ on each run, by the [comparison sort lower bound](/comparison-sort-lower-bound/).

**The spread.** Knuth gives the variance of the comparison count. Its leading term is $(7 - 2\pi^2/3)\, n^2 \approx 0.42\, n^2$, so the standard deviation is about $0.65\, n$, which is small next to the mean of about $2 n \ln n$.

**A bound with high probability.** Follow one item through the calls. At each call that contains it, the pivot has a rank in the middle half of the range with probability at least $1/2$, and then the range of the item shrinks to at most $3/4$ of its size. After $\log_{4/3} n$ such calls, the range has one item. A Chernoff bound shows that $c \ln n$ calls, for a large enough constant $c$, contain that many good calls with probability at least $1 - n^{-2}$. By a union bound over the $n$ items, with probability at least $1 - 1/n$ each item is in $O(\log n)$ calls, and each item is compared at most once in each call. So the run makes $O(n \log n)$ comparisons with probability at least $1 - 1/n$.

**The worst case.** A run is quadratic only when the pivots are near the ends of the ranges again and again. With distinct keys, all $n(n-1)/2$ comparisons happen only when each pivot is the least or the largest item of its range. For a range of $k \ge 2$ items this has probability $2/k$, so the probability is $\prod_{k=2}^{n} 2/k = 2^{n-1}/n!$. For $n = 8$ this is about $0.0032$, and for $n = 30$ it is less than $10^{-23}$.

**Space.** The recursion is $O(\log n)$ deep with high probability, by the bound above, but $n - 1$ deep in the worst case. Recursing on the smaller side first and looping on the larger side makes the stack $O(\log n)$ on each run. See [quicksort stack depth](/quicksort-stack-depth/).

| claim | model and case | bound |
|---|---|---|
| comparisons | comparison model, expected on each input of distinct keys | $2(n+1)H_n - 4n$ |
| time | expected on each input | $\Theta(n \log n)$ |
| time | with probability at least $1 - 1/n$ | $O(n \log n)$ |
| time | worst case over the random choices | $\Theta(n^2)$ |
| extra space | expected, for the stack | $O(\log n)$ |

## Properties

- **Las Vegas.** The output is always sorted. Only the time depends on the random choices.
- **No bad input.** For distinct keys, the distribution of the comparison count is the same for each input order. An adversary who knows the algorithm but not the random numbers cannot force a slow run.
- **In place.** It uses only the stack of the recursion and $O(1)$ more space.
- **Not stable.** The swap of line L3 and the swaps of PARTITION move items past equal items.
- **Not adaptive.** A sorted input costs as much as any other on average.

## Variants and improvements

- **Shuffle first.** Shuffle the array once, then run deterministic quicksort. This is the form of Sedgewick and Wayne. It uses $n - 1$ random numbers, and the analysis is the same.
- **Hoare partition.** Use the random pivot with the [Hoare partition](/hoare-partition/). It makes fewer swaps, and it splits a range of equal items near the middle.
- **Three-way partition.** Lomuto with many equal keys is quadratic even with random pivots. [Three-way quicksort](/three-way-quicksort/) puts the items equal to the pivot in a middle part, and its expected time is $O(n \log n)$ for any multiset of keys.
- **Median of three random items.** Take the median of three random items as the pivot. The expected count falls to about $1.19\, n \lg n$ comparisons. See [median-of-three pivot](/median-of-three-pivot/) and [pivot selection](/pivot-selection/).
- **Randomized selection.** The same random pivot with recursion on one side only gives [quickselect](/quickselect/), with expected linear time.
- **Introsort.** [Introsort](/introsort/) bounds the worst case by a switch to heapsort when the depth is too large. This gives $O(n \log n)$ in the worst case without random numbers.

## When to use it

Use randomized quicksort when the input can come from a user or an adversary, so that a fixed pivot rule could be attacked, and when an expected $O(n \log n)$ bound is enough. It is also the simplest version of quicksort with a proof of an $O(n \log n)$ bound that holds for each input. When the worst case must be $O(n \log n)$, use [introsort](/introsort/), [heapsort](/heapsort/) or [merge sort](/merge-sort/). When the run must be repeatable, use a seeded generator.

## Pitfalls

- **Many equal keys.** With the Lomuto partition, each item equal to the pivot goes to the left side. On an array of $n$ equal items each call removes one item, and the time is $\Theta(n^2)$ whatever the pivots are. Use a three-way or Hoare partition.
- **A biased random index.** The index must be uniform in $[lo, hi)$. The expression `lo + rand() % (hi - lo)` is biased when the range of `rand` is not a multiple of $hi - lo$, and the bias is large when $hi - lo$ is close to that range.
- **A fixed seed.** A generator that is seeded with a known constant makes the pivots predictable again, and an adversary can then build a bad input.
- **The off-by-one in the index.** The index $r$ must include $hi - 1$. With $lo \le r < hi - 1$, the last item is never the pivot, and a range of two items is never split around its last item.
- **Deep recursion.** The rare bad runs and inputs of equal keys can make the stack $n$ calls deep. Recurse on the smaller side first when the stack is small.

## Implementations

## History

Hoare's paper of 1962 already proposed a random choice of the pivot, to protect against inputs in an unlucky order. The analysis by indicator variables over the pairs $z_i, z_j$ is the one of Motwani and Raghavan and of CLRS. The exact mean $2(n+1)H_n - 4n$ is the mean of quicksort on a random permutation, which Hoare and later Knuth derived from the recurrence of the average case.

## References
