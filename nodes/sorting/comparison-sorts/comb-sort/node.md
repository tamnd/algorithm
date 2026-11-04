---
tag: SYZVMD
kind: algorithm
slug: comb-sort
name: Comb sort
area: sorting/comparison-sorts
level: intro
summary: Bubble sort generalized to compare elements a shrinking gap apart, removing small values near the end quickly.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(n²), best: Θ(n log n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1980
  people: [Włodzimierz Dobosiewicz, Stephen Lacey, Richard Box]
  note: Dobosiewicz described bubble sort passes with a shrinking gap in 1980. Lacey and Box found it again, named it comb sort, and proposed the shrink factor 1.3 in Byte in 1991.
prereqs: [bubble-sort, inversion]
see_also: [shell-sort, cocktail-shaker-sort, insertion-sort, h-sorting, heapsort, comparison-cost-model]
sources:
  - paper: "Włodzimierz Dobosiewicz, An efficient variation of bubble sort, Information Processing Letters 11(1) (1980)"
    locator: pp. 5 to 6
  - paper: "Stephen Lacey and Richard Box, A fast, easy sort, Byte 16(4) (April 1991)"
    locator: the article (the name comb sort, the shrink factor 1.3 and the rule that replaces the gaps 9 and 10 by 11)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (bubble sort and the count of inversions that adjacent exchanges must remove)
---

Comb sort is [bubble sort](/bubble-sort/) with a gap. A pass compares each item with the item $gap$ places to its right, and exchanges them when they are out of order. The gap starts near $n$ and shrinks by a factor of about 1.3 after each pass. When it reaches 1, the passes are bubble sort passes, and they go on until one makes no exchange. The early passes move small items from the right end to the left in long jumps, which is the slow case of bubble sort. On random input comb sort makes about $2.3\, n \lg n$ comparisons for $n$ from $10^3$ to $10^4$, which is much faster than bubble sort, but there is no proof of an $O(n \log n)$ bound, and it is not stable.

## In plain words

Bubble sort only swaps neighbours. An item that must travel far, such as a small item at the right end, moves only one place in each pass, so bubble sort is slow.

Comb sort first compares items that are far apart, like the teeth at the two ends of a wide comb. A swap of two items far apart can fix many wrong pairs at once. After each pass, the comb gets finer: the distance between the compared items shrinks. At the end the distance is one, and the last passes are bubble sort passes. By then most items are near their place, so these passes have little left to do.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

This is the form of Lacey and Box, with the shrink factor $1.3$ in integer arithmetic: the new gap is $\lfloor 10 \cdot gap / 13 \rfloor$.

```pseudo id=main
COMB-SORT(A)
L1  gap ← n
L2  done ← false
L3  while not done do
L4      gap ← max(1, ⌊10 · gap / 13⌋)
L5      done ← (gap = 1)                  ▷ only a pass with gap 1 can end the sort
L6      for i ← 0 to n − 1 − gap do
L7          if A[i] > A[i + gap] then
L8              exchange A[i] and A[i + gap]
L9              done ← false
```

Lines L6 to L9 are one pass with the current gap. Line L4 shrinks the gap before each pass, and keeps it at 1 once it is there. Line L5 lets the loop end only after a pass with gap 1 and no exchange. Such a pass checks every pair of neighbours, so the array is then sorted.

## Example

Sort $A = [8, 4, 1, 5, 9, 2, 6, 3, 7, 0]$, with $n = 10$. The input has 26 [inversions](/inversion/), so bubble sort would make 26 exchanges.

| pass | gap | the array after the pass | comparisons | exchanges |
|---|---|---|---|---|
| start | | 8 4 1 5 9 2 6 3 7 0 | | |
| 1 | 7 | 3 4 0 5 9 2 6 8 7 1 | 3 | 2 |
| 2 | 5 | 2 4 0 5 1 3 6 8 7 9 | 5 | 2 |
| 3 | 3 | 2 1 0 5 4 3 6 8 7 9 | 7 | 1 |
| 4 | 2 | 0 1 2 3 4 5 6 8 7 9 | 8 | 2 |
| 5 | 1 | 0 1 2 3 4 5 6 7 8 9 | 9 | 1 |
| 6 | 1 | 0 1 2 3 4 5 6 7 8 9 | 9 | 0 |

In pass 1, the item 0 jumps from index 9 to index 2, and 8 jumps from index 0 to index 7. The run makes 41 comparisons and 8 exchanges. Pass 6 makes no exchange and ends the sort. Bubble sort makes 26 exchanges and 45 comparisons on this input.

## Correctness

The loop can stop only after a pass with gap 1 that made no exchange, because line L5 sets $done$ to true only when the gap is 1 and line L9 sets it back to false at each exchange. That pass found each pair of neighbours in order, so the array is sorted. Each change is an exchange, so the output is a permutation of the input.

The loop stops because the gap reaches 1 after at most $\lceil \log_{1.3} n \rceil + 1$ passes, and each later pass either makes no exchange or lowers the number of inversions. An exchange of two items that are out of order, at any distance, lowers the number of inversions by at least 1. The full proof is below.

## Complexity

**Passes with a gap above 1.** The gaps are $\lfloor 10n/13 \rfloor$, then about $n/1.3^2$, and so on, so there are about $\log_{1.3} n \approx 2.64 \lg n$ such passes. The pass with gap $g$ makes $n - g$ comparisons. Together they make $\Theta(n \log n)$ comparisons on each input of size $n$.

**Passes with gap 1.** Each of them makes $n - 1$ comparisons. Their number is at least 1, and at most $d + 1$, where $d$ is the number of inversions left after the passes with a larger gap.

**Worst case.** Each pass with gap 1 is a bubble sort pass without the bound of the last exchange, so they take $O(n^2)$ comparisons in total. With the passes before, the worst case is $O(n^2)$. No bound of $O(n \log n)$ on the worst case is known.

**Best case.** A sorted array makes all the passes with a gap above 1 and one pass with gap 1, with no exchange. This is $\Theta(n \log n)$ comparisons: for $n = 1000$ it is 22 passes and 18,713 comparisons. Bubble sort and insertion sort need only 999.

**Random input.** In a measurement on random permutations of distinct keys, the mean cost was:

| $n$ | comparisons | exchanges | passes | comparisons / $(n \lg n)$ |
|---|---|---|---|---|
| 1000 | 22,759 | 4,471 | 26.1 | 2.28 |
| 10,000 | 328,734 | 63,474 | 36.2 | 2.47 |

The mean number of passes with gap 1 is small, about 5 for $n = 1000$, but the measurement does not show whether the ratio in the last column stays bounded. For comparison, [heapsort](/heapsort/) makes about $2 n \lg n$ comparisons, and bubble sort about $n^2/2$, which is 499,500 for $n = 1000$.

**Space.** $\Theta(1)$ extra.

## Properties

- **Not stable.** An exchange over a gap of more than 1 can jump over an equal item. For example, with gap 2 on $[2_a, 2_b, 1]$, the pass exchanges $2_a$ and $1$, and gives $[1, 2_b, 2_a]$.
- **In place.** It uses a fixed number of variables.
- **Not adaptive.** It makes all the passes with a gap above 1 on each input, even a sorted one.
- **Not online.** It needs the whole array, and the first gap depends on $n$.

## Variants and improvements

- **Combsort11.** Lacey and Box replace a gap of 9 or 10 by 11. In the measurement above, for $n = 1000$, this cut the mean number of comparisons from 22,759 to 21,654.
- **Other shrink factors.** The factor matters a lot. In the same measurement for $n = 1000$, the factor 2 gave 447,366 comparisons, because the gaps 4, 2, 1 leave many items far from their place, and the factor 1.1 gave 44,280, because it makes more passes. Lacey and Box chose 1.3 from experiments.
- **Ending with insertion sort.** Replace the passes with gap 1 by one run of [insertion sort](/insertion-sort/). When few inversions are left, it takes $O(n + d)$ time.
- **[Shell sort](/shell-sort/).** With each gap, Shell sort makes the array fully [h-sorted](/h-sorting/) by insertion, while comb sort makes only one bubble pass. Shell sort with good gaps has proved bounds, such as $O(n^{3/2})$ and $O(n \log^2 n)$.
- **[Cocktail shaker sort](/cocktail-shaker-sort/).** Another fix for the slow small items of bubble sort, by passes in both directions. It is much weaker than comb sort.

## When to use it

Use comb sort when the code must be very short and in place, and the input is random and of moderate size. In most other cases, a library sort, [heapsort](/heapsort/) or [Shell sort](/shell-sort/) is a better choice: they have proved bounds, and heapsort has a worst case of $O(n \log n)$. Do not use comb sort when the sort must be stable.

## Pitfalls

- **Ending when the gap reaches 1.** The sort is not done after the first pass with gap 1. It must go on until a pass with gap 1 makes no exchange. Line L5 does this.
- **A gap of 0.** For $n \le 1$, or with float arithmetic that rounds down, $\lfloor 10 \cdot gap / 13 \rfloor$ can be 0. A pass with gap 0 compares each item with itself, and the loop never ends. The $\max(1, \ldots)$ in line L4 prevents it.
- **Claiming $O(n \log n)$.** The measured cost on random input is close to $n \lg n$ times a small constant, but this is not a proved bound, and the worst case is only known to be $O(n^2)$.

## Implementations

## History

Dobosiewicz (1980) described a variation of bubble sort that compares items at a gap that shrinks after each pass, and showed by experiment that it is much faster than bubble sort. Lacey and Box (1991) found the method again, gave it the name comb sort, and proposed the shrink factor 1.3 and the rule for the gap 11, both from experiments.

## References
