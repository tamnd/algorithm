---
tag: S172EG
kind: algorithm
slug: introsort
name: Introsort
aliases:
- introspective sort
area: sorting/comparison-sorts
level: advanced
summary: Quicksort that switches to heapsort at depth limit and to insertion sort on small ranges; O(n log n) worst case.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: O(log n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1997
  people: [David R. Musser]
  note: Musser named the method and the idea of an algorithm that watches its own recursion depth and changes method when the depth shows a bad case; it became the usual form of std::sort in C++ libraries.
prereqs: [quicksort, heapsort, insertion-sort, hoare-partition, median-of-three-pivot]
see_also: [quicksort-stack-depth, randomized-quicksort, introselect, adversary-argument, three-way-quicksort, java-system-sort, timsort, comparison-sort-lower-bound]
sources:
  - paper: "David R. Musser, Introspective sorting and selection algorithms, Software: Practice and Experience 27(8), 1997"
    locator: pp. 983 to 993 (introsort with the depth limit 2⌊lg n⌋, the median-of-3 killer inputs, and introselect)
  - paper: "M. Douglas McIlroy, A killer adversary for quicksort, Software: Practice and Experience 29(4), 1999"
    locator: pp. 341 to 344 (an adversary that drives any quicksort of a certain kind to quadratic time)
  - paper: "Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software: Practice and Experience 23(11), 1993"
    locator: pp. 1249 to 1265 (the median-of-3 quicksort with an insertion sort cut-off on which introsort is built)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6 (heapsort), Chapter 7 (quicksort and its problem on Hoare partitioning), Section 2.1 (insertion sort)
---

Introsort is [quicksort](/quicksort/) with a safety net. It partitions around a median-of-three pivot as usual, but it counts the depth of its recursion. When a range is still not sorted after $2 \lfloor \lg n \rfloor$ levels of partitioning, the pivots have been bad for too long, and introsort sorts that range with [heapsort](/heapsort/) instead. Ranges of at most 16 items go to [insertion sort](/insertion-sort/). So it is as fast as quicksort on almost all inputs, it never takes more than $O(n \log n)$ time, and it works in place with $O(\log n)$ stack. Musser introduced it in 1997, and it became the usual way to write C++ `std::sort`.

## In plain words

Quicksort is fast because each pivot usually splits the items into two parts of similar size. Then about $\lg n$ rounds of splitting are enough. But on some inputs the pivot is always near one end, the parts shrink by only a few items each time, and the work grows like $n^2$.

Introsort watches for this. It gives itself a budget of about twice $\lg n$ levels of splitting. A part that is still big when the budget runs out is sorted by heapsort, which is slower on average but never takes more than $n \lg n$ steps times a constant.

Very small parts are sorted by insertion sort, which is the fastest method for a handful of items. Most inputs never use up the budget, so introsort behaves like quicksort.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, which the algorithm can only compare with $<$. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/). The aim is the speed of quicksort with a worst case of $O(n \log n)$ comparisons, in place, and with no random numbers.

## The algorithm

```pseudo id=main
INTROSORT(A)
L1  if n > 1 then INTRO(A, 0, n, 2⌊lg n⌋)

INTRO(A, lo, hi, d)                                 ▷ sorts A[lo … hi−1]
L2  while hi − lo > 16 do
L3      if d = 0 then HEAPSORT(A, lo, hi); return  ▷ the depth budget is used up
L4      d ← d − 1
L5      m ← the index of the median of A[lo], A[⌊(lo + hi)/2⌋], A[hi − 1]
L6      exchange A[lo] and A[m]
L7      j ← HOARE-PARTITION(A, lo, hi − 1)
L8      if j + 1 − lo < hi − j − 1 then INTRO(A, lo, j + 1, d); lo ← j + 1
L9      else INTRO(A, j + 1, hi, d); hi ← j + 1
L10 INSERTION-SORT(A, lo, hi)

HOARE-PARTITION(A, p, r)                            ▷ splits A[p … r] around x = A[p]
L11 x ← A[p]; i ← p − 1; j ← r + 1
L12 loop
L13     repeat j ← j − 1 until not x < A[j]
L14     repeat i ← i + 1 until not A[i] < x
L15     if i < j then exchange A[i] and A[j] else return j
```

[HOARE-PARTITION](/hoare-partition/) returns an index $j$ with $p \le j < r$ such that each item of $A[p \ldots j]$ is at most $x$ and each item of $A[j+1 \ldots r]$ is at least $x$. Both parts are non-empty, so each step makes progress. Lines L8 and L9 recurse on the smaller part and loop on the larger one, which keeps the stack at $O(\log n)$ frames on any input. HEAPSORT$(A, lo, hi)$ is ordinary heapsort on the range $A[lo \ldots hi-1]$, and INSERTION-SORT$(A, lo, hi)$ is ordinary insertion sort on the same kind of range.

## Example

Sort these 20 items:

$$A = [13, 2, 19, 7, 5, 17, 11, 3, 20, 1, 15, 9, 6, 18, 4, 12, 16, 8, 14, 10].$$

Here $n = 20$, so the budget is $d = 2 \lfloor \lg 20 \rfloor = 8$.

| step | range | action | result |
|---|---|---|---|
| 1 | $A[0 \ldots 19]$, 20 items | median of $A[0] = 13$, $A[10] = 15$, $A[19] = 10$ is 13, already at $A[0]$ | pivot $x = 13$ |
| 2 | $A[0 \ldots 19]$ | HOARE-PARTITION: 5 exchanges, $(13, 10)$, $(19, 8)$, $(17, 12)$, $(20, 4)$, $(15, 6)$; returns $j = 11$ | $[10, 2, 8, 7, 5, 12, 11, 3, 4, 1, 6, 9 \mid 15, 18, 20, 17, 16, 19, 14, 13]$ |
| 3 | right part $A[12 \ldots 19]$, 8 items, smaller | recursive call with $d = 7$: at most 16 items, so insertion sort | $[13, 14, \ldots, 20]$ |
| 4 | left part $A[0 \ldots 11]$, 12 items | the loop goes on with this range: at most 16 items, so insertion sort | $[1, 2, \ldots, 12]$ |

The pivot 13 ends up in the right part. Hoare partitioning does not put the pivot at its final place; it only separates the small items from the large ones. The depth budget is not touched in this example. On a bad input it matters a lot, as the next table shows.

## Correctness

Each pass of the loop in INTRO splits the range into two non-empty parts, such that every item of the left part is at most every item of the right part. So sorting the two parts on their own sorts the range. The call on the smaller part sorts it by induction on the length, and the loop goes on with the larger part, which is shorter than the range it came from. When the loop ends, either heapsort or insertion sort sorts what is left, and both are correct on any range. The depth budget only chooses which correct method finishes a range, so it does not affect correctness. The full proof is below.

## Complexity

**Worst case: $O(n \log n)$.** Look at the recursion as a tree of partitioning steps. At each depth, the ranges are disjoint, and partitioning a range of $m$ items costs $O(m)$, so each depth costs $O(n)$. There are at most $2 \lfloor \lg n \rfloor$ depths with partitioning, which costs $O(n \log n)$ in total. The ranges that reach heapsort are disjoint, and heapsort on $m$ items costs $O(m \log m)$, so all of them cost $O(n \log n)$. The ranges that reach insertion sort are disjoint and each has at most 16 items, so they cost $O(16 n)$. The [comparison sort lower bound](/comparison-sort-lower-bound/) shows that $\Omega(n \log n)$ is needed, so the worst case is $\Theta(n \log n)$.

**Average case.** On random inputs the budget is almost never used, and introsort makes about as many comparisons as median-of-3 quicksort, whose leading term is $\frac{12}{7} n \ln n \approx 1.188\, n \lg n$. Measured comparisons:

| input, $n$ | comparisons | per $n \lg n$ | items sent to heapsort |
|---|---|---|---|
| random, $10^3$ | 11,790 | 1.18 | 0 |
| random, $10^4$ | 167,493 | 1.26 | 0 |
| random, $10^5$ | 2,078,269 | 1.25 | 0 |
| sorted, $10^5$ | 1,424,572 | 0.86 | 0 |
| reversed, $10^5$ | 1,474,599 | 0.89 | 0 |
| all equal, $10^5$ | 1,420,156 | 0.86 | 0 |
| 10 distinct values, $10^5$ | 1,492,282 | 0.90 | 0 |

The counts include the partitioning, the median-of-3 tests and the insertion sorts. On sorted input the median of three is the true median of the first range, and later splits stay close to even. On equal keys, Hoare partitioning stops on every item and exchanges it, which also splits evenly.

**The bad case.** McIlroy's adversary builds, for any deterministic quicksort, an input that makes almost every pivot the smallest item still in its range. The table uses inputs built against the quicksort above with no depth limit:

| $n$ | quicksort with no depth limit | introsort | items sent to heapsort | depth budget |
|---|---|---|---|---|
| 1,000 | 253,911 | 33,638 | 966 | 18 |
| 2,000 | 1,007,911 | 75,994 | 1,962 | 20 |
| 4,000 | 4,015,911 | 168,289 | 3,958 | 22 |

The plain quicksort makes about $n^2/4$ comparisons. Introsort spends its budget on splits that remove only a few items each, then hands almost all the items to heapsort, and stays within a small factor of $n \lg n$.

**Space.** Recursing on the smaller part keeps the stack at most $\lg n$ frames. The depth budget also bounds it by $2 \lfloor \lg n \rfloor$. Heapsort and insertion sort use $O(1)$ extra words. See [quicksort stack depth](/quicksort-stack-depth/).

## Properties

- **Not stable.** Partitioning moves items over long distances. For example, with the cut-off set to 0, the array $[1_a, 1_b, 0]$ gives $[0, 1_b, 1_a]$: the first exchange puts $0$ first and $1_a$ last. With the cut-off of 16, an array of 17 keys from $\{0, 1\}$ already shows the effect.
- **In place.** It uses $O(\log n)$ words of stack and no buffer. See [in-place algorithm](/in-place-algorithm/).
- **Deterministic.** It needs no random numbers, so the same input always takes the same path. The price is that an adversary who knows the code can build inputs that use up the budget, as above. They cost only a constant factor, not a change from $n \log n$ to $n^2$.
- **Not adaptive.** It makes $\Theta(n \log n)$ comparisons on sorted input, unlike [Timsort](/timsort/).

## Variants and improvements

- **One final insertion sort.** Musser's paper and the SGI STL do not sort the small ranges as they appear. INTRO stops when a range has at most 16 items, and one pass of insertion sort over the whole array finishes the work at the end. Each item then moves at most 16 places, so the pass is linear. libstdc++ `std::sort` works this way.
- **Other depth limits.** Any limit $c \lg n$ with a constant $c$ gives the same bounds. A smaller $c$ switches to heapsort sooner on bad inputs and more often on good ones.
- **Introselect.** The same idea applied to [quickselect](/quickselect/) falls back to a linear-time selection, such as [median of medians](/median-of-medians/), when the ranges shrink too slowly. See [introselect](/introselect/).
- **Pattern-defeating quicksort.** Peters' pdqsort keeps the depth limit and the fall-back to heapsort, and adds a check for bad splits that shuffles some items, a fast path for runs that are already sorted, and a [three-way](/three-way-quicksort/) split for many equal keys. Go's `sort.Sort` and Rust's `sort_unstable` have used it or its descendants.
- **Random pivots.** [Randomized quicksort](/randomized-quicksort/) has an expected $O(n \log n)$ time on every input but no worst-case bound. Introsort gives the worst-case bound without randomness, and the two ideas can be combined.

## When to use it

Use it as a general sort for arrays in memory when stability is not needed. It is fast on random data, needs only $O(\log n)$ extra space, and has an $O(n \log n)$ guarantee, which also protects a server against inputs that an attacker builds to slow down a quicksort. If equal items must keep their order, use merge sort or [Timsort](/timsort/). If the input often has long sorted runs, Timsort or pdqsort uses them and introsort does not.

## Pitfalls

- **A cut-off with an off-by-one.** Hoare partitioning needs at least 2 items, and the median of three needs 3 distinct positions. Both hold because the loop runs only when the range has more than 16 items.
- **An unguarded final pass.** The one-pass variant often uses an insertion sort whose inner loop has no test for the left end. That is safe only from position 16 on, because the smallest item lies in the leftmost range of at most 16 items. libstdc++ runs the guarded loop on the first 16 items and the unguarded loop on the rest. Using the unguarded loop from position 1 can read before the array.
- **A Lomuto partition with many equal keys.** A partition that puts all keys equal to the pivot on one side makes every split uneven when all keys are equal. Introsort then still runs in $O(n \log n)$, but only because heapsort takes over, which is slow. Hoare partitioning, as above, splits equal keys evenly.

## Implementations

## History

Hoare's quicksort (1961) has a quadratic worst case. Median-of-3 pivots, from Singleton (1969), and the engineering of Bentley and McIlroy (1993) made it fast in practice, but Musser showed simple input families, the median-of-3 killers, on which such sorts still take quadratic time. In his 1997 paper Musser proposed introspection: the algorithm counts its recursion depth, and when the depth passes $2 \lfloor \lg n \rfloor$ it switches to heapsort. He also gave introselect. The SGI STL, and then libstdc++ and other C++ libraries, adopted introsort for `std::sort`, and C++11 made a worst-case $O(n \log n)$ comparison bound part of the standard for `std::sort`. McIlroy (1999) gave an adversary that drives any such quicksort into its worst case, which shows why the fall-back matters.

## References
