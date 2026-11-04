---
tag: J5ZM91
kind: problem
slug: dutch-national-flag
name: Dutch national flag problem
aliases:
- sort colors
- three-way partition problem
- three-way partitioning problem
area: techniques/two-pointers-and-windows
level: intro
summary: Partition an array of three values into three contiguous blocks in one pass with O(1) extra space.
prereqs: [two-pointers, loop-invariant]
see_also: [dutch-national-flag-algorithm, three-way-quicksort, bentley-mcilroy-partitioning, partition-around-pivot, counting-sort, american-flag-sort, sorting-problem, guarded-commands]
sources:
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming, Prentice-Hall, 1976
    locator: Chapter 14, The problem of the Dutch national flag
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (3-way partitioning, entropy-optimal sorting)
  - url: https://leetcode.com/problems/sort-colors/
    title: LeetCode, problem 75, Sort Colors
    locator: problem statement
---

The Dutch national flag problem asks to rearrange a row of items of three colors, red, white and blue, so that the colors form three contiguous blocks in the order of the flag of the Netherlands. Edsger Dijkstra posed it in *A Discipline of Programming* (1976) under strict rules: the only operations are to inspect the color of one item and to swap two items, the program may use only a constant number of extra variables, and it should inspect each item once. In the general form, the three colors are "less than", "equal to" and "greater than" a pivot $p$, and the problem is the three-way partition step of [three-way quicksort](/three-way-quicksort/). [Dijkstra's three-way partition](/dutch-national-flag-algorithm/) solves it with exactly $n$ inspections and at most $n$ swaps.

## In plain words

A row of balls has three colors mixed in any order. You must put all red balls first, then all white balls, then all blue balls, like the stripes of the Dutch flag. You cannot use a second row or count the balls first: you can only look at the color of one ball and swap two balls, and you should look at each ball only once.

The same problem shows up whenever you split items into three groups: smaller than some value, equal to it and larger than it. Sorting algorithms such as quicksort need this split when many items have the same value.

## Definition

**Input.** An array $A[0 \ldots n-1]$ and a map $c$ from items to the colors $\{0, 1, 2\}$. In the pivot form, $c(x) = 0$ if $x < p$, $c(x) = 1$ if $x = p$ and $c(x) = 2$ if $x > p$.

**Output.** A permutation of $A$, made in place, and two indices $0 \le lt \le gt \le n$, such that $c(A[k]) = 0$ for $k < lt$, $c(A[k]) = 1$ for $lt \le k < gt$, and $c(A[k]) = 2$ for $k \ge gt$.

**Model (Dijkstra's rules).** The program can evaluate $c(A[k])$, which counts as one inspection, and can swap two cells. It has $O(1)$ extra variables, each holding an index or a color. It cannot copy items to other storage. The costs are the number of inspections and the number of swaps.

## Variants

- **Sort colors.** The items are the numbers 0, 1 and 2, and the output is the sorted array. LeetCode problem 75 asks for this in one pass.
- **Partition around a pivot.** The general form above. With only two classes, $x < p$ and $x \ge p$, it is the ordinary [partition around a pivot](/partition-around-pivot/).
- **$k$ colors.** Put the items in $k$ blocks in a given order. With counting allowed, [counting sort](/counting-sort/) does it in two passes. In place, [American flag sort](/american-flag-sort/) uses the counts to find the blocks and then cycles the items into place.
- **Stable version.** Keep the input order inside each color. This is not possible in one pass with $O(1)$ space and only swaps; a stable counting sort with a second array does it in $O(n)$ time.
- **Minimum swaps.** Reach the three blocks with the fewest swaps, not in one pass.

## Examples

**Sort colors.** $A = [2, 0, 2, 1, 1, 0]$ becomes $[0, 0, 1, 1, 2, 2]$, with $lt = 2$ and $gt = 4$.

**Pivot form.** $A = [1, 2, 0, 1, 2, 0, 1]$ with $p = 1$ becomes $[0, 0, 1, 1, 1, 2, 2]$ with $(lt, gt) = (2, 5)$. The [algorithm page](/dutch-national-flag-algorithm/) traces this input: 7 inspections and 4 swaps.

**Many equal keys.** $A = [5, 5, 3, 5, 9, 5]$ with $p = 5$ becomes $[3, 5, 5, 5, 5, 9]$, with a block of four items equal to $p$. A two-way partition would leave the equal items on both sides of the split, and quicksort would sort them again.

## Known algorithms

| algorithm | inspections | swaps | passes |
| --- | --- | --- | --- |
| [Dijkstra's three-way partition](/dutch-national-flag-algorithm/) | exactly $n$ | $n_0 + n_2 \le n$ | 1 |
| [Bentley-McIlroy partitioning](/bentley-mcilroy-partitioning/) | $n$ | fewer when few items have color 1 | 1, then a block move |
| two two-way partitions | up to $2n$ | up to $n$ | 2 |
| counting, then rewrite (items are only colors) | $n$ | none, $n$ writes | 2 |

Here $n_0$, $n_1$ and $n_2$ are the numbers of items of each color.

**Dijkstra's three-way partition.** Keep indices $lo \le mid \le hi + 1$, with the colors 0 left of $lo$, the colors 1 from $lo$ to $mid - 1$, the uninspected items from $mid$ to $hi$, and the colors 2 right of $hi$. Inspect $A[mid]$ and swap it to the front or the back, or step over it. The uninspected region shrinks by one item at each step, so no item is skipped and none is inspected twice. The [algorithm page](/dutch-national-flag-algorithm/) gives the pseudocode and the proof.

**Two passes of two-way partition.** First move the colors 0 to the front, then, in the rest, move the colors 1 before the colors 2. This is simple, but it can inspect an item twice, so it does not meet Dijkstra's rules.

## Bounds

**Inspections.** Every correct algorithm inspects all $n$ items on every input. Suppose that an item is never inspected. The algorithm makes the same swaps and returns the same $lt$ and $gt$ whatever the color of this item, so the item ends in the same cell. Give it a color other than the color of the block of that cell; then the output is wrong. So $n$ inspections are necessary, and Dijkstra's algorithm uses exactly $n$.

**Swaps.** Let $c_{ij}$ be the number of items of color $i$ that lie in the block of color $j$ of the output, for $i \ne j$. A swap can put two items in their blocks at once only if they are in each other's blocks. So the minimum number of swaps is
$$ \min(c_{01}, c_{10}) + \min(c_{02}, c_{20}) + \min(c_{12}, c_{21}) + 2\,|c_{01} - c_{10}|, $$
where the last term counts the items left in cycles of three blocks, each such cycle needing 2 swaps. A breadth-first search over all swap sequences confirms this formula for all inputs with $n \le 7$. On $[1, 2, 0, 1, 2, 0, 1]$ the minimum is 3, while Dijkstra's one-pass loop makes 4 swaps. The direct way to reach the minimum counts $n_0$, $n_1$ and $n_2$ first, to find the blocks, which takes a second pass.

**Time and space.** $\Theta(n)$ time and $O(1)$ extra space, by Dijkstra's algorithm. This is optimal by the inspection bound.

## Reductions

- **To sorting.** The output is a sort by color, so any [sorting](/sorting-problem/) algorithm solves the problem in $O(n \log n)$ comparisons. The point of the problem is to do better with three colors.
- **Inside quicksort.** Three-way quicksort calls the problem once per partition step. Sedgewick and Wayne show that with three-way partitioning, the number of compares of quicksort on random orders is within a constant factor of the entropy bound of the key frequencies, so inputs with few distinct keys sort in linear time.
- **From $k$ colors.** $k - 1$ two-way partitions, or $\lfloor k/2 \rfloor$ three-way partitions on nested ranges, each of which moves the smallest and the largest remaining color to the ends of the range, solve the $k$-color problem in place.

## Applications

- **Three-way quicksort and its library versions**, for arrays with many equal keys.
- **Sorting by a three-valued key** in place, such as records marked low, medium and high priority.
- **Teaching loop invariants.** Dijkstra used the problem to show how the invariant of four regions leads to the program, and it remains a standard example of programs derived from invariants with [guarded commands](/guarded-commands/).

## References
