---
tag: 16D94V
kind: definition
slug: comparison-sort
name: Comparison sort
aliases:
- comparison-based sorting
area: sorting/comparison-sorts
level: intro
summary: A sorting algorithm that uses only pairwise comparisons of elements to determine their order.
prereqs: [sorting-problem, comparison-model]
see_also: [comparison-sort-lower-bound, comparison-cost-model, decision-tree-model, stable-sort, in-place-algorithm, integer-sorting, sorting-network]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8 introduction (the term comparison sort) and Section 8.1 (the decision-tree model, Theorem 8.1)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5 introduction (sorting by comparison of keys) and Section 5.3.1 (comparison trees)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1 (the Comparable interface and the sorting cost model) and Section 2.2 (Proposition I)
---

A comparison sort is an algorithm for the [sorting problem](/sorting-problem/) that learns about the keys only by comparing two of them at a time. It is an algorithm of the [comparison model](/comparison-model/): it may move, copy and swap items, but it may not do arithmetic on a key, use a key as an index or read the bits of a key. Because of this, a comparison sort works for each type with a total order, and each comparison sort makes at least $\lceil \lg(n!) \rceil$ comparisons on some input of $n$ distinct keys.

## Definition

Let $(U, \le)$ be a set with a total order, and let the input be a sequence $a_1, \dots, a_n$ of elements of $U$. A **comparison sort** is a deterministic or randomized algorithm with these two properties.

1. **Access.** The only operation that depends on the values of the keys is a comparison of two input keys $a_i$ and $a_j$. The comparison is either the two-way test $a_i \le a_j$ (or $a_i < a_j$), or the three-way test with the answers $a_i < a_j$, $a_i = a_j$ and $a_i > a_j$.
2. **Output.** For each input it outputs a permutation $\pi$ of $\{1, \dots, n\}$ with
$$a_{\pi(1)} \le a_{\pi(2)} \le \cdots \le a_{\pi(n)},$$
or it rearranges the items in this order.

The two inputs $a$ and $b$ of length $n$ have the same **order type** when $a_i \le a_j \iff b_i \le b_j$ for all $i, j$. Property 1 has this consequence: on two inputs of the same order type, a deterministic comparison sort makes the same sequence of comparisons, gets the same answers and outputs the same $\pi$. So for each $n$ a deterministic comparison sort is a binary [decision tree](/decision-tree-model/) whose inner nodes are comparisons and whose leaves are permutations. Its worst-case number of comparisons is the height of the tree.

**The comparator.** In a program, the comparison is a function supplied by the caller, for example `compare(x, y)` or `less(x, y)`. The definition needs this function to describe a total order on the keys, or more generally a *strict weak order* $<$: it is irreflexive ($x < x$ is false), transitive, and "neither $x < y$ nor $y < x$" is an equivalence relation. Items that are equivalent are the ties, and a [stable sort](/stable-sort/) keeps their input order.

## Examples and non-examples

**Examples.** [Insertion sort](/insertion-sort/), [selection sort](/selection-sort/), [bubble sort](/bubble-sort/), [merge sort](/merge-sort/), [heapsort](/heapsort/), [quicksort](/quicksort/), [Shell sort](/shell-sort/), [Timsort](/timsort/) and [introsort](/introsort/) are comparison sorts. Each of them touches the keys only in a test such as $A[j] > key$.

**Same order type, same run.** The inputs $[30, 10, 20]$ and $[3.5, -1, 0]$ have the same order type. Insertion sort makes the same 3 comparisons on both and outputs the same permutation $\pi = (2, 3, 1)$. Over the 6 orders of 3 distinct keys, insertion sort makes 2, 3, 2, 3, 3 and 3 comparisons, so its tree has height 3 and average depth $8/3 \approx 2.667$. The lower bound for 3 keys is $\lceil \lg 6 \rceil = 3$ in the worst case and $\lg 6 \approx 2.585$ on average.

**The lower bound for small sizes.** Each comparison sort of $n$ distinct keys makes at least $\lceil \lg(n!) \rceil$ comparisons on some input. The values are 3, 5, 7 and 22 for $n = 3, 4, 5, 10$, and 525 for $n = 100$. The proof is on the [comparison sort lower bound](/comparison-sort-lower-bound/) page.

**A sorting network.** A [sorting network](/sorting-network/) is a comparison sort whose sequence of comparisons does not depend on the answers. It is an *oblivious* comparison sort.

**Non-examples.**

- [Counting sort](/counting-sort/) uses each key as an index into an array of counters. Two inputs of the same order type, such as $[1, 2]$ and $[1, 1000]$, make it touch different counters.
- [Radix sort](/radix-sort/) reads the digits of the keys. [Bucket sort](/bucket-sort/) computes a bucket number from the value of a key.
- A quicksort that uses the arithmetic mean of the keys as its pivot is not a comparison sort, because it adds keys. The usual quicksort, which picks an input key as the pivot, is one.
- Sorting by hashing, or by an [integer sorting](/integer-sorting/) method on the [word RAM](/word-ram/), is not a comparison sort. Such methods can beat the $\lg(n!)$ bound, because the bound holds only in the comparison model.

**A borderline case.** An algorithm that first checks that the keys are small integers and then runs counting sort is not a comparison sort, even if its fallback path is merge sort. The definition is about each step of the algorithm, not about its interface.

## Related definitions

- **[Comparison model](/comparison-model/).** The model of computation in which comparison sorts live. Its lower bounds hold for each comparison sort.
- **[Decision tree model](/decision-tree-model/).** The tree that a deterministic comparison sort forms for a fixed $n$.
- **[Comparison sort lower bound](/comparison-sort-lower-bound/).** At least $\lceil \lg(n!) \rceil = n \lg n - \Theta(n)$ comparisons in the worst case and $\lg(n!)$ on average.
- **[Comparison cost model](/comparison-cost-model/).** The cost model that counts comparisons and exchanges to compare comparison sorts.
- **[Stable sort](/stable-sort/).** A sort that keeps the input order of equal keys.
- **[In-place algorithm](/in-place-algorithm/).** A sort that uses $O(1)$ or $O(\log n)$ extra space besides the input.
- **[Adaptive sorting](/adaptive-sorting/).** A comparison sort whose cost goes down when the input is close to sorted.
- **[Integer sorting](/integer-sorting/).** Sorting with operations on the bits of the keys, outside the comparison model.

## References
