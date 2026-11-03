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
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Part II
---

## In plain words

You have a list of things, such as numbers, names or dates. You want them in order, from the smallest to the largest. Sorting is the problem of finding this order. It is one of the most frequent steps in programs. Many other problems become easy when the data is sorted.

## Definition

**Input.** A sequence $a_1, a_2, \ldots, a_n$ of $n$ items, and a total preorder $\le$ on the items.

**Output.** A permutation $b_1, b_2, \ldots, b_n$ of the input with $b_1 \le b_2 \le \cdots \le b_n$.

A sort is **stable** when items that are equal under $\le$ keep their order from the input. A sort is **in place** when it uses $O(1)$ or $O(\log n)$ memory in addition to the input.

## Variants

- **Comparison sorting.** The algorithm can only compare two items. This is the model of most library sorts.
- **Integer sorting.** The items are integers or strings of bits, and the algorithm can use their digits. Counting sort and radix sort are in this group.
- **Partial sorting.** Find only the $k$ smallest items in order.
- **External sorting.** The items do not fit in memory.

## Examples

| input | output |
|---|---|
| 5 2 4 6 1 3 | 1 2 3 4 5 6 |
| "pear" "fig" "apple" | "apple" "fig" "pear" |
| (2, a) (1, b) (2, c) | (1, b) (2, a) (2, c) for a stable sort by the number |

## Known algorithms

## Bounds

In the [comparison model](/comparison-model/), each sort needs at least $\lceil \lg(n!) \rceil$ comparisons in the worst case. By Stirling's formula, $\lg(n!) = n \lg n - n \lg e + O(\log n)$. So the bound is $\Omega(n \log n)$.

The proof uses a decision tree. Each comparison has two outcomes, so a tree of depth $h$ has at most $2^h$ leaves. The tree must have a different leaf for each of the $n!$ orders of the input. So $2^h \ge n!$, and $h \ge \lg(n!)$. The same bound holds for the average number of comparisons on a random order.

[Merge sort](/merge-sort/) reaches this bound up to a lower-order term. Algorithms that use the digits of the items are not limited by this bound. For example, radix sort sorts $n$ integers of $w$ bits in $O(n \cdot w / \lg n)$ time.

## Reductions

- **Element distinctness reduces to sorting.** Sort the items. Then two equal items are next to each other.
- **Sorting reduces to the convex hull in the plane.** Map each number $x$ to the point $(x, x^2)$. The hull gives the points in sorted order. So a convex hull also needs $\Omega(n \log n)$ time in the comparison model.

## Applications

- Search a sorted array with [binary search](/binary-search/).
- Find duplicates, the median or the most frequent item.
- Merge and join tables in databases.
- Sweep-line algorithms in geometry process events in sorted order.

## References
