---
tag: 5SRTPB
kind: problem
slug: sorting-problem
name: Sorting
aliases: [sort, the sorting problem]
area: sorting/comparison-sorts
areas: [sorting]
level: intro
summary: Put the items of a sequence in non-decreasing order by a key.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Ω(n log n)}
prereqs: [total-order, permutation]
see_also: [comparison-sort, comparison-sort-lower-bound, stable-sort, merge-sort, quicksort, heapsort, radix-sort, element-distinctness]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5 (the definition and the stability of a sort), and Section 5.3.1, Minimum-comparison sorting (the bound of lg n! and the values S(n) for small n)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Part II, Sorting and Order Statistics (the introduction gives the problem), and Section 8.1, Lower bounds for sorting
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 2, Sorting (Section 2.1 for the rules of the sort, Section 2.5 for stability and the applications)
---

The sorting problem asks to put the $n$ items of a sequence in non-decreasing order of a key. In the [comparison model](/comparison-model/), each algorithm needs at least $\lceil \lg n! \rceil = n \lg n - \Theta(n)$ comparisons in the worst case, and [merge sort](/merge-sort/) and [heapsort](/heapsort/) reach $O(n \log n)$. Sorting is one of the most frequent steps in computing, because a sorted sequence makes search, the removal of copies and the merge of data fast.

## In plain words

You have a list of things, such as numbers, names or dates. You want them in order, from the smallest to the largest. Sorting is the problem of finding this order. The things must keep their identity: the output has the same things as the input, only in a new order.

Two things can be equal in the order and still be different. For example, two people can have the same age. A sort that keeps such things in their input order is called stable.

Sorting is one of the most frequent steps in programs, and many other problems become easy when the data is sorted.

## Definition

**Input.** A sequence $a_1, a_2, \ldots, a_n$ of $n \ge 0$ items, and a total preorder $\preceq$ on the items. A total preorder is reflexive, transitive and total: for each two items $x$ and $y$, $x \preceq y$ or $y \preceq x$. Two items with $x \preceq y$ and $y \preceq x$ are *equivalent*. Usually $\preceq$ comes from a key: $x \preceq y$ if and only if $\mathrm{key}(x) \le \mathrm{key}(y)$ in a [total order](/total-order/) on the keys.

**Output.** A sequence $b_1, b_2, \ldots, b_n$ such that there is a [permutation](/permutation/) $\pi$ of $\{1, \ldots, n\}$ with $b_i = a_{\pi(i)}$ for each $i$, and $b_1 \preceq b_2 \preceq \cdots \preceq b_n$.

When $\preceq$ is a total order, the output is unique. When some items are equivalent, more than one output is correct.

**Stable.** A sort is *stable* when its output always satisfies one more condition: if $i < j$ and $a_{\pi(i)}$ and $a_{\pi(j)}$ are equivalent, then $\pi(i) < \pi(j)$. So equivalent items keep their input order. The page [stable sort](/stable-sort/) covers this property.

**In place.** A sort is [in place](/in-place-algorithm/) when it changes the input array and uses $O(\log n)$ memory in addition to it. Some authors require $O(1)$.

## Variants

- **Comparison sorting.** The algorithm learns about the items only by comparing two of them. This is the model of most library sorts. The page [comparison sort](/comparison-sort/) lists these algorithms.
- **Integer sorting.** The keys are integers or strings of bits, and the algorithm can use their digits as array indices. [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) are in this group.
- **Partial sorting.** Output only the $k$ smallest items, in order. The [selection problem](/selection-problem/) asks only for the item of rank $k$.
- **External sorting.** The items do not fit in memory. The cost is the number of block transfers. [External merge sort](/external-merge-sort/) is the usual method.
- **Sorting with a known structure.** The input is the concatenation of sorted runs, or has few [inversions](/inversion/). An [adaptive sort](/adaptive-sorting/) is fast on such input.
- **Merging.** The input is two sorted sequences. This is the problem of [merging sorted lists](/merging-sorted-lists/).

## Examples

| input | the key | a correct output |
|---|---|---|
| 5 2 4 6 1 3 | the number | 1 2 3 4 5 6 |
| "pear" "fig" "apple" | the string, in [lexicographic order](/lexicographic-order/) | "apple" "fig" "pear" |
| (2, a) (1, b) (2, c) | the number | (1, b) (2, a) (2, c), the only stable output |
| (2, a) (1, b) (2, c) | the number | (1, b) (2, c) (2, a), correct but not stable |
| empty sequence | any | empty sequence |

**Non-example.** The output 1 2 3 4 5 for the input 5 2 4 6 1 3 is in order but is not a permutation of the input, so it is not a solution. The output 1 2 4 3 5 6 is a permutation but is not in order.

**Counts for small inputs.** An input of $n$ distinct keys has $n!$ possible orders. The table gives the lower bound $\lceil \lg n! \rceil$ on the worst-case number of comparisons, against the worst case of merge sort and of the [Ford-Johnson algorithm](/ford-johnson-algorithm/).

| $n$ | $n!$ | $\lceil \lg n! \rceil$ | merge sort | Ford-Johnson |
|---|---|---|---|---|
| 4 | 24 | 5 | 5 | 5 |
| 5 | 120 | 7 | 8 | 7 |
| 8 | 40320 | 16 | 17 | 16 |
| 10 | 3628800 | 22 | 25 | 22 |
| 12 | 479001600 | 29 | 33 | 30 |
| 16 | 20922789888000 | 45 | 49 | 46 |

For $n = 10^6$, $\lg n! \approx 18{,}488{,}885$ and $n \lg n \approx 19{,}931{,}569$. So the term $-n \lg e$ in the bound is about 7 percent of the total at this size.

## Known algorithms

- **Quadratic time.** [Insertion sort](/insertion-sort/) (stable, in place, adaptive), [selection sort](/selection-sort/) (in place, $n - 1$ swaps) and [bubble sort](/bubble-sort/) take $\Theta(n^2)$ time in the worst case.
- **$O(n \log n)$ in the worst case.** [Merge sort](/merge-sort/) is stable and uses $\Theta(n)$ extra space. [Heapsort](/heapsort/) is in place but not stable.
- **$O(n \log n)$ expected.** [Quicksort](/quicksort/) with random pivots ([randomized quicksort](/randomized-quicksort/)) is in place and fast in practice, with a worst case of $\Theta(n^2)$. [Introsort](/introsort/) bounds the worst case by a switch to heapsort.
- **Adaptive.** [Natural merge sort](/natural-merge-sort/) and [Timsort](/timsort/) are linear on sorted input and $O(n \log n)$ in the worst case.
- **Between.** [Shell sort](/shell-sort/) has a time between these classes that depends on its gap sequence.
- **Not comparison based.** [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) run in $O(n + k)$ and $O(d(n + k))$ time for keys with $d$ digits in the range $0$ to $k - 1$.

## Bounds

**Lower bound in the comparison model.** Each comparison sort needs at least $\lceil \lg n! \rceil$ comparisons in the worst case on $n$ distinct keys. The proof uses the [decision tree](/decision-tree-model/) of the algorithm. Each comparison has two outcomes, so a tree of depth $h$ has at most $2^h$ leaves. Two different orders of the input need two different leaves, because one sequence of swaps cannot sort both. So the tree has at least $n!$ leaves, $2^h \ge n!$, and $h \ge \lg n!$. The page [comparison sort lower bound](/comparison-sort-lower-bound/) gives the full proof.

**The size of the bound.** By [Stirling's formula](/stirling-approximation/), $\lg n! = n \lg n - n \lg e + \tfrac12 \lg n + O(1)$, with $\lg e \approx 1.4427$. So the bound is $n \lg n - \Theta(n)$, and in particular $\Omega(n \log n)$.

**The average case.** The same bound holds for the average number of comparisons over the $n!$ orders. A binary tree with $N$ leaves has an average leaf depth of at least $\lg N$, so the average is at least $\lg n!$.

**Upper bound.** Merge sort makes at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ comparisons, which is $n \lg n - \Theta(n)$. So the lower bound is tight up to the coefficient of the linear term. Knuth (Section 5.3.1) writes $S(n)$ for the least worst-case number of comparisons that sorts $n$ items. The Ford-Johnson algorithm gives $S(n) = \lceil \lg n! \rceil$ for $n \le 11$. For $n = 12$ the lower bound is 29, and $S(12) = 30$.

**A trivial lower bound.** An algorithm that does not look at an item cannot know its place. So each sort reads all $n$ items, and even a check that the input is sorted needs $n - 1$ comparisons.

**Other models.** Algorithms that use the digits of the keys are not limited by the $\Omega(n \log n)$ bound. Radix sort sorts $n$ integers of $w$ bits in $O(n \lceil w / \lg n \rceil)$ time on the word RAM, by digits of $\lg n$ bits.

## Reductions

- **Element distinctness reduces to sorting.** Sort the items. Then two equal items are next to each other, and one scan of $n - 1$ comparisons finds them. So [element distinctness](/element-distinctness/) takes $O(n \log n)$ time.
- **Sorting reduces to the convex hull in the plane.** Map each number $x$ to the point $(x, x^2)$. All points lie on a parabola, so each one is a vertex of the hull, and the hull in counterclockwise order from the leftmost point gives the numbers in sorted order. The map and the read take $O(n)$ time. So in a model where sorting needs $\Omega(n \log n)$ time and the hull algorithm can be run, such as the algebraic decision tree model, the convex hull also needs $\Omega(n \log n)$ time.
- **Sorting reduces to a priority queue.** Insert all items into a [priority queue](/priority-queue/), then extract the minimum $n$ times. So a comparison-based priority queue cannot do both operations in $o(\log n)$ amortized time.

## Applications

- Search a sorted array with [binary search](/binary-search/) in $O(\log n)$ time.
- Find duplicates, the median or the most frequent item with one scan after the sort.
- Merge and join tables in databases with a [sort-merge join](/sort-merge-join/).
- Process events in sorted order in sweep-line algorithms of geometry.
- Sort by several fields at once with [multi-key sorting](/multi-key-sorting/).

## References
