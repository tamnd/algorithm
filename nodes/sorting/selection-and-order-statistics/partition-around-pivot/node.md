---
tag: J0QNZ6
kind: technique
slug: partition-around-pivot
name: Partition around a pivot
aliases:
- Lomuto partition
- Hoare partition
area: sorting/selection-and-order-statistics
level: intro
summary: Rearrange an array so that elements smaller than a pivot precede it and larger elements follow.
prereqs: [loop-invariant]
see_also: [lomuto-partition, hoare-partition, dutch-national-flag, bentley-mcilroy-partitioning, quicksort, quickselect, pivot-selection, three-way-quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, Section 7.1, Description of quicksort (PARTITION and its loop invariant), and the end-of-chapter problem "Hoare partition correctness"
  - paper: doi:10.1145/366622.366642
    title: C. A. R. Hoare, Algorithm 63, Partition, Communications of the ACM 4(7) (1961)
    locator: page 321 (the first published partition procedure, used by Algorithm 64, Quicksort, and Algorithm 65, Find)
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming
    locator: Chapter 14, The problem of the Dutch national flag (three-way partition with one pass and swaps)
  - paper: doi:10.1002/spe.4380231105
    title: "Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software: Practice and Experience 23(11) (1993)"
    locator: pages 1249 to 1265 (split-end three-way partition, and the failures of two-way partitions on equal keys)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (the partitioning method, and quicksort with 3-way partitioning)
---

Partitioning around a pivot rearranges an array in place so that the items less than a chosen pivot value come first and the items greater than it come last, with the items equal to it in between or spread over the two sides. It takes one pass, $n$ or fewer comparisons with the pivot, and $O(1)$ extra space. It is the step that [quicksort](/quicksort/) applies to both sides and that [quickselect](/quickselect/) applies to one side, and the different schemes, [Lomuto](/lomuto-partition/), [Hoare](/hoare-partition/) and the [Dutch national flag](/dutch-national-flag/), differ in how they keep the regions of the array apart.

## In plain words

You have a row of cards and you pick one value as a dividing line. You want all smaller cards on the left and all larger cards on the right. You do not care about the order inside each side.

You walk along the row once. You keep the cards you have already looked at in a small number of groups: smaller, equal, larger. Each new card you look at goes into its group with one swap. When no card is left unlooked at, the row is split.

The pivot is a guess at a good dividing line. A pivot near the middle splits the row into two halves, which is what the sorting and selection methods built on this step need.

## When it applies

- The items have a [total order](/total-order/), or a key with a total order, and a test that puts each item on one side of the pivot.
- The items sit in an array that may be changed in place, with swaps of two entries in $O(1)$ time.
- The order inside each side does not matter. Partitioning in place is not [stable](/stable-sort/): items with equal keys can change their relative order.
- The next step needs only the sides, not a full sort: a recursive sort, a search for one rank, or a filter of the items below a threshold.

## The template

The three-way template keeps four regions of $A[lo \ldots hi - 1]$, and each step moves one item out of the unknown region. The holes are the pivot rule, the comparison, and what the caller does with the result.

```pseudo id=main
PARTITION(A, lo, hi)                       ▷ A[lo .. hi − 1], hi − lo ≥ 1
L1  x ← CHOOSE-PIVOT(A, lo, hi)            ▷ hole: the pivot rule
L2  lt ← lo, i ← lo, gt ← hi
L3  while i < gt do                        ▷ A[i .. gt − 1] is not yet looked at
L4      if A[i] < x then                   ▷ hole: the comparison or key
L5          swap A[lt] and A[i]
L6          lt ← lt + 1, i ← i + 1
L7      else if A[i] > x then
L8          gt ← gt − 1
L9          swap A[i] and A[gt]
L10     else i ← i + 1
L11 return (lt, gt)                        ▷ hole: the caller recurses, selects or filters
```

**Invariant.** At each test of line L3:

$$ A[lo \ldots lt - 1] < x, \qquad A[lt \ldots i - 1] = x, \qquad A[i \ldots gt - 1] \text{ not looked at}, \qquad A[gt \ldots hi - 1] > x. $$

Line L2 makes the three known regions empty. Line L5 swaps a smaller item with the first equal item (or with itself, if no equal item has been seen), so both the smaller and the equal regions move one place to the right. Line L9 sends a larger item to the front of the larger region and brings an unknown item to place $i$, which is looked at in the next step; $i$ does not move. Each step shrinks $gt - i$ by one, so the loop makes exactly $hi - lo$ steps, with one or two comparisons each. When it stops, $i = gt$ and the unknown region is empty. If $x$ is an item of the range, the equal region holds at least that item.

**Two-way schemes.** If equal items need not be grouped, two regions are enough:

- [Lomuto partition](/lomuto-partition/) scans left to right with the regions "at most $x$", "greater than $x$" and "not looked at", with the pivot kept at the end and swapped into place at the end. It is short and easy to prove, and it is the form in CLRS.
- [Hoare partition](/hoare-partition/) scans from both ends towards each other and swaps a pair of items that are both on the wrong side. It makes about a third as many swaps as Lomuto on random input, and it splits equal items evenly between the two sides. It returns a split point, not the final place of the pivot.

The caller then works on the sides: [quicksort](/quicksort/) recurses on both; [quickselect](/quickselect/) compares the target rank with $lt$ and $gt$ and recurses on one side or stops; a filter keeps one side.

## Classic examples

**A trace.** Partition $A = [3, 7, 1, 3, 9, 2, 3, 8]$ around $x = 3$ with the template:

| item at $i$ | case | $A$ after the step | $lt$ | $i$ | $gt$ |
|---|---|---|---|---|---|
| 3 | equal | 3 7 1 3 9 2 3 8 | 0 | 1 | 8 |
| 7 | greater | 3 8 1 3 9 2 3 7 | 0 | 1 | 7 |
| 8 | greater | 3 3 1 3 9 2 8 7 | 0 | 1 | 6 |
| 3 | equal | 3 3 1 3 9 2 8 7 | 0 | 2 | 6 |
| 1 | less | 1 3 3 3 9 2 8 7 | 1 | 3 | 6 |
| 3 | equal | 1 3 3 3 9 2 8 7 | 1 | 4 | 6 |
| 9 | greater | 1 3 3 3 2 9 8 7 | 1 | 4 | 5 |
| 2 | less | 1 2 3 3 3 9 8 7 | 2 | 5 | 5 |

The loop makes $8 = n$ steps and returns $(2, 5)$: $A[0 \ldots 1] = [1, 2]$ is less than $3$, $A[2 \ldots 4]$ holds the three copies of $3$, and $A[5 \ldots 7] = [9, 8, 7]$ is greater. A selection of rank $k$ (counted from 1) now stops at once for $3 \le k \le 5$, recurses on the left for $k \le 2$, and on the right for $k \ge 6$.

**Uses.**

- [Quicksort](/quicksort/) and [randomized quicksort](/randomized-quicksort/): partition, then sort both sides. With [three-way quicksort](/three-way-quicksort/), the equal region is done at once, so an input with $d$ distinct keys sorts in $O(n \log d)$ expected time.
- [Quickselect](/quickselect/), [median of medians](/median-of-medians/) and [introselect](/introselect/): partition, then keep the one side that holds rank $k$.
- [Dutch national flag](/dutch-national-flag/): sort an array of three colours in one pass; this is the template with the colours as the three classes.
- [Bentley-McIlroy partitioning](/bentley-mcilroy-partitioning/): a Hoare-style scan that moves equal items to the two ends and then swaps them to the middle.
- [Top-k selection](/top-k-selection/): once the item of rank $k$ is known, one partition pass collects the $k$ smallest.

## Variations

- **By predicate.** Replace the comparison with any test $P(a)$: the items with $P$ true come first. This is `std::partition` in C++ and the filtering step of many algorithms.
- **Stable partition.** Keep the input order inside each side. With an extra array of size $n$ this is one pass; in place it takes $O(n \log n)$ time by a divide and conquer of rotations.
- **Several pivots.** Two pivots give three sides in one pass, as in [dual-pivot quicksort](/dual-pivot-quicksort/); $s$ pivots give the buckets of [sample sort](/sample-sort/).
- **Pivot rules.** First or last item, a random item, the median of three, or the median of medians ([pivot selection](/pivot-selection/)). The rule decides the balance of the sides, and so the running time of the caller, but not the correctness of the partition.

## Pitfalls

- **Many equal keys.** A two-way scheme that puts all items equal to $x$ on one side, as Lomuto does, gives sides of sizes $0$ and $n - 1$ when all keys are equal, so quicksort and quickselect take $\Theta(n^2)$ time. Use three-way partitioning or Hoare's scheme, which stops on equal items from both sides.
- **No progress.** A caller must recurse on ranges that exclude at least one item. Hoare's scheme with the first item of the range as pivot always returns a split with both sides not empty. With the last item as pivot, the split leaves one side empty when the pivot is the largest item, and the recursion does not end.
- **The pivot as an item, not an index.** The template stores the value $x$ before the loop. Code that reads $A[p]$ again after swaps may compare with a different item.
- **Off by one in bounds.** Mixing half-open ranges $[lo, hi)$ with closed ranges $[lo, hi]$ is the most common source of errors in partition code. Fix one convention and state the invariant with it.
- **A fixed pivot rule on adversarial input.** The first or last item as pivot makes quicksort quadratic on sorted input. A random pivot or a median of medians avoids this.

## Exercises

1. Prove that the template makes at most $2(hi - lo)$ comparisons and at most $hi - lo$ swaps.
2. Let all $n$ items of the range be equal. Find the sizes of the sides and the number of swaps for Lomuto's scheme and for the template, and explain the difference in the running time of quickselect on this input.

## References
