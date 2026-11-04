---
tag: 8SHK9M
kind: algorithm
slug: dual-pivot-quicksort
name: Dual-pivot quicksort
aliases:
- Yaroslavskiy's quicksort
area: sorting/comparison-sorts
level: advanced
summary: Quicksort partitioning around two pivots into three ranges; the default for Java primitive arrays.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: O(log n) expected}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: false, comparison: true, recursive: true}
history:
  year: 2009
  people: [Vladimir Yaroslavskiy, Jon Bentley, Joshua Bloch, Robert Sedgewick]
  note: Sedgewick studied a dual-pivot partition in his 1975 thesis and found it no better than the classic one. Yaroslavskiy proposed a different dual-pivot partition in 2009, and after tuning with Bentley and Bloch it became the sort for primitive arrays in Java 7 (2011).
prereqs: [quicksort, randomized-quicksort, hoare-partition]
see_also: [three-way-quicksort, java-system-sort, bentley-mcilroy-partitioning, quicksort-expected-running-time, introsort, multikey-quicksort, comparison-cost-model, median-of-three-pivot]
sources:
  - paper: doi:10.1007/978-3-642-33090-2_71
    title: Sebastian Wild and Markus E. Nebel, Average case analysis of Java 7's dual pivot quicksort, European Symposium on Algorithms (ESA 2012), Lecture Notes in Computer Science 7501
    locator: pp. 825 to 836 (Yaroslavskiy's partition, 1.9 n ln n − 2.46 n + O(ln n) comparisons and 0.6 n ln n + 0.08 n + O(ln n) swaps on a random permutation, and the comparison with Sedgewick's dual-pivot partition)
  - paper: doi:10.1007/978-3-642-39206-1_4
    title: Martin Aumüller and Martin Dietzfelbinger, Optimal partitioning for dual pivot quicksort, ICALP 2013, Lecture Notes in Computer Science 7965
    locator: pp. 33 to 44 (a model of all dual-pivot partitions and the least average of 1.8 n ln n + O(n) comparisons)
  - paper: "Shrinu Kushagra, Alejandro López-Ortiz, Aurick Qiao and J. Ian Munro, Multi-pivot quicksort: theory and experiments, ALENEX 2014, SIAM"
    locator: pp. 47 to 60 (cache misses of multi-pivot quicksort and a 3-pivot variant)
  - paper: "Oracle, Java Platform, Standard Edition API Specification, class java.util.Arrays"
    locator: the notes on the methods sort(int[]) and the other primitive types (a dual-pivot quicksort by Yaroslavskiy, Bentley and Bloch)
---

Dual-pivot quicksort is a [quicksort](/quicksort/) that partitions each range around two pivots $p \le q$ instead of one. One pass puts the items less than $p$ on the left, the items between $p$ and $q$ in the middle and the items greater than $q$ on the right, and the three parts are sorted recursively. The form on this page is Yaroslavskiy's partition, which Java 7 adopted for arrays of primitive types. On a random permutation it makes $1.9\, n \ln n - 2.46\, n + O(\log n)$ comparisons on average, 5% fewer than the $2 n \ln n$ of classic quicksort, but about twice as many swaps. Its speed in practice comes mostly from fewer memory accesses, not from the saved comparisons. Like quicksort, it is in place and not stable, and it takes $\Theta(n^2)$ time in the worst case.

## In plain words

Classic quicksort picks one card, the pivot, and splits the other cards into two piles: smaller and larger. Then it does the same to each pile.

Dual-pivot quicksort picks two cards, a small one and a large one. It splits the other cards into three piles: smaller than the small pivot, between the two pivots, and larger than the large pivot. Then it does the same to each of the three piles.

Three piles shrink faster than two, so there are fewer rounds. Each card now needs one or two looks to find its pile instead of one, but if the method looks at the small pivot or the large pivot first in a clever way, the total number of looks still goes down a little. The bigger gain on real machines is that the cards are read fewer times.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, compared only with $<$. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm may use random numbers to choose its pivots.

## The algorithm

```pseudo id=main
DUAL-PIVOT-QUICKSORT(A, lo, hi)
L1  if hi ≤ lo then return
L2  exchange A[lo] with A[r] for a uniform random r in [lo, hi], then A[hi] with A[r′] for a uniform random r′ in [lo + 1, hi]
L3  (l, g) ← PARTITION(A, lo, hi)
L4  DUAL-PIVOT-QUICKSORT(A, lo, l − 1)
L5  DUAL-PIVOT-QUICKSORT(A, l + 1, g − 1)
L6  DUAL-PIVOT-QUICKSORT(A, g + 1, hi)

PARTITION(A, lo, hi)                         ▷ Yaroslavskiy's partition, lo < hi
L7  if A[hi] < A[lo] then exchange A[lo] and A[hi]
L8  p ← A[lo]; q ← A[hi]                     ▷ now p ≤ q
L9  l ← lo + 1; g ← hi − 1; k ← l
L10 while k ≤ g do
L11     if A[k] < p then
L12         exchange A[k] and A[l]; l ← l + 1
L13     else if not (A[k] < q) then          ▷ A[k] ≥ q
L14         while q < A[g] and k < g do g ← g − 1
L15         exchange A[k] and A[g]; g ← g − 1
L16         if A[k] < p then
L17             exchange A[k] and A[l]; l ← l + 1
L18     k ← k + 1
L19 l ← l − 1; g ← g + 1
L20 exchange A[lo] and A[l]; exchange A[hi] and A[g]
L21 return (l, g)
```

The call DUAL-PIVOT-QUICKSORT$(A, 0, n-1)$ sorts the whole array. During the loop the range has four zones: $A[lo+1 \ldots l-1]$ holds items less than $p$, $A[l \ldots k-1]$ holds items between $p$ and $q$, $A[g+1 \ldots hi-1]$ holds items at least $q$, and $A[k \ldots g]$ is not yet seen. The index $k$ scans from the left. An item at least $q$ goes to the right end of the unseen zone, and line L14 first moves $g$ left past items that are already greater than $q$. Line L20 puts the pivots between the zones. Line L2 makes the two pivots a uniform random pair of items of the range, so no fixed input is bad for every run.

## Example

Partition $A = [3, 7, 1, 8, 5, 2, 9, 4, 6]$ with $lo = 0$ and $hi = 8$, without the random exchanges of line L2. Line L7 compares $6 < 3$, which is false, so $p = 3$ and $q = 6$.

| $k$ | $A[k]$ | action | array after the step | $l$ | $g$ | comparisons so far |
|---|---|---|---|---|---|---|
| | | start | 3 7 1 8 5 2 9 4 6 | 1 | 7 | 1 |
| 1 | 7 | $\ge q$; $A[7] = 4$ is not $> q$; exchange $A[1]$, $A[7]$; 4 is not $< p$ | 3 4 1 8 5 2 9 7 6 | 1 | 6 | 5 |
| 2 | 1 | $< p$; exchange $A[2]$, $A[1]$ | 3 1 4 8 5 2 9 7 6 | 2 | 6 | 6 |
| 3 | 8 | $\ge q$; skip $A[6] = 9 > q$; exchange $A[3]$, $A[5]$; 2 is $< p$, exchange $A[3]$, $A[2]$ | 3 1 2 4 5 8 9 7 6 | 3 | 4 | 11 |
| 4 | 5 | between $p$ and $q$ | 3 1 2 4 5 8 9 7 6 | 3 | 4 | 13 |

Now $k = 5 > g = 4$, and the loop ends. Line L19 sets $l = 2$ and $g = 5$, and line L20 moves the pivots: $[2, 1, \mathbf{3}, 4, 5, \mathbf{6}, 9, 7, 8]$. The left part $2, 1$ is less than 3, the middle part $4, 5$ lies between 3 and 6, and the right part $9, 7, 8$ is greater than 6. The partition made 13 comparisons and 6 exchanges for 9 items.

## Correctness

PARTITION keeps the four zones described above as a loop invariant. Each step of the loop puts $A[k]$ into the left zone, the middle zone or the right zone and moves $k$ or $g$, so the unseen zone shrinks by at least one item and the loop ends. At the end, the unseen zone is empty, and line L20 places $p$ at $l$ and $q$ at $g$, with smaller items to the left of $l$, items between the pivots between $l$ and $g$, and items at least $q$ to the right of $g$. The three recursive calls are on ranges that do not contain $l$ or $g$, so they are strictly shorter, and by induction they sort their parts. Each item of a part is in order with each item of the other parts and with the pivots, so the whole range is sorted. The full proof is below.

## Complexity

**Comparisons on average.** Wild and Nebel (2012) solved the recurrence for the expected number of comparisons of this algorithm on a uniformly random permutation of $n$ distinct keys:

$$C_n = \tfrac{19}{10}\, n \ln n - 2.46\, n + O(\ln n), \qquad S_n = \tfrac{6}{10}\, n \ln n + 0.08\, n + O(\ln n)$$

for the comparisons and the swaps. The comparisons are 5% fewer than the $2 n \ln n$ of classic quicksort, and the swaps are almost twice the $\tfrac{1}{3} n \ln n$ of classic quicksort with a Hoare-style partition. The gain comes from the order of the tests: an item is first compared with $p$ on the left side of the scan and with $q$ on the right side, and on average this order guesses the right pivot more often than chance.

Measured with random permutations, the averages per run were:

| $n$ | dual-pivot comparisons | $/ (n \ln n)$ | dual-pivot exchanges | classic quicksort comparisons | classic exchanges |
|---|---|---|---|---|---|
| $10^4$ (5 runs) | 147,443 | 1.601 | 55,964 | 169,843 | 31,408 |
| $10^5$ (2 runs) | 1,941,336 | 1.686 | 729,982 | 2,126,955 | 392,316 |

For $n = 10^5$ the formula gives $1.9 \cdot 10^5 \ln 10^5 - 2.46 \cdot 10^5 \approx 1{,}941{,}000$ comparisons. The exchange count here includes the exchanges of lines L7 and L20, which is why it is above $0.6\, n \ln n + 0.08\, n \approx 698{,}800$. The ratio to $n \ln n$ is still well below 1.9 because the linear term is large at these sizes.

**Worst case.** If the two pivots are the two smallest items of each range, the right part has $n - 2$ items, and the cost is $\Theta(n^2)$. With random pivots this has a very small probability. Without line L2, an already sorted input does this every time.

**Equal keys.** If all keys are equal, $p = q$, and each item goes through line L13. The scan from the left and the moves of $g$ meet in the middle, so the middle and right parts each get about half of the range, and the time is $\Theta(n \log n)$, not $\Theta(n^2)$. With $n = 10^4$ equal keys the run made 216,579 comparisons. Java's version tests for $p = q$ and then uses a three-way partition instead, which takes linear time on this input.

**Space.** The partition uses $O(1)$ extra words. The stack depth is $O(\log n)$ in expectation. Recursing on the two smaller parts and looping on the largest one bounds it by $\lg n$ in every run.

## Properties

- **Not stable.** The exchanges move items over equal items. Partitioning $[0_a, 1_b, 1_c, 0_d]$ gives $[0_a, 0_d, 1_c, 1_b]$.
- **In place.** $O(1)$ extra words for the partition, plus the stack.
- **Randomized.** The pivots are random, so the running time is random and the output is always sorted, as for [randomized quicksort](/randomized-quicksort/).
- **Not adaptive.** A sorted input costs about as much as a random one: 140,140 comparisons for $n = 10^4$ in one run.

## Variants and improvements

- **Pivot sampling.** Java 7 takes 5 items of the range, sorts them, and uses the second and the fourth as $p$ and $q$. This makes the three parts closer in size.
- **Insertion sort for short ranges.** Java 7 switches to [insertion sort](/insertion-sort/) below 47 items. The analysis of Wild, Nebel and Neininger includes this cut-off.
- **The best order of tests.** Aumüller and Dietzfelbinger (2013) studied all ways to decide whether to compare an item with $p$ or with $q$ first, and showed that the least possible average is $1.8\, n \ln n + O(n)$ comparisons. Their "Count" strategy compares with the pivot that has received more items so far, and reaches this bound.
- **Sedgewick's dual-pivot partition.** An older dual-pivot partition comes from Sedgewick's 1975 thesis. Wild and Nebel showed that it makes more comparisons than classic quicksort, which is why dual pivots were not thought useful before 2009.
- **More pivots.** Kushagra, López-Ortiz, Qiao and Munro (2014) gave a 3-pivot quicksort with fewer cache misses than the dual-pivot version, and explained the speed of multi-pivot quicksort by its cache behaviour.
- **A worst-case guard.** As in [introsort](/introsort/), a depth limit with a fall-back to [heapsort](/heapsort/) bounds the worst case by $O(n \log n)$. Later versions of the Java sort do this.

## When to use it

Use it as the main sort for arrays of keys that cannot be told apart when equal, such as integers and floating-point numbers, where stability does not matter. With pivot sampling, an insertion sort cut-off and a depth limit, it is the core of the [Java system sort](/java-system-sort/) for primitive types. For data with many equal keys, a [three-way quicksort](/three-way-quicksort/) or the [Bentley-McIlroy partition](/bentley-mcilroy-partitioning/) is safer. For records where the order of equal keys matters, use a stable sort such as [Timsort](/timsort/).

## Pitfalls

- **Fixed pivots at the ends.** Without line L2, $p = A[lo]$ and $q = A[hi]$, and a sorted array gives the parts $0$, $n - 2$ and $0$ at each level. The time is $\Theta(n^2)$ and the recursion is $n/2$ levels deep, which overflows the stack for large $n$.
- **Forgetting $k < g$ in line L14.** Without it, $g$ can move left past $k$ into the zone of middle items, and the result is not a partition.
- **Forgetting the second test of line L16.** The item that line L15 brings to position $k$ comes from the unseen zone and may be less than $p$. Without the test it stays in the middle part.
- **Comparing the work with classic quicksort by comparisons only.** The comparison count drops by only 5%, while the swaps nearly double. Timing results depend on the memory system, and the speed-up seen in Java was larger than the comparison counts predict.

## Implementations

## History

Sedgewick analysed a quicksort with two pivots in his 1975 PhD thesis and found that his version was no better than the classic one, and later texts repeated that multiple pivots do not help. In 2009 Vladimir Yaroslavskiy proposed his partition on the OpenJDK mailing list, with timings that showed it faster than the tuned quicksort of [Bentley and McIlroy](/bentley-mcilroy-partitioning/). After tuning with Jon Bentley and Joshua Bloch, it became the sort for primitive arrays in Java 7, released in 2011. Wild and Nebel (2012) gave the first exact average-case analysis and showed that it saves comparisons where Sedgewick's version did not. Aumüller and Dietzfelbinger (2013) found the best dual-pivot strategy for comparisons, and Kushagra and others (2014) related the speed to cache misses.

## References
