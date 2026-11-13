---
tag: NCD5YW
kind: algorithm
slug: pancake-sort
name: Pancake sort
aliases:
- pancake flip sort
- prefix-reversal sort
area: sorting/comparison-sorts
level: core
summary: Sorts by repeatedly reversing prefixes, using at most about 2n reversals.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n²)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [selection-sort]
see_also: [pancake-sorting, burnt-pancake-problem, selection-sort, permutation, cycle-sort, bubble-sort, heapsort, inversion]
sources:
  - paper: "William H. Gates and Christos H. Papadimitriou, Bounds for sorting by prefix reversal, Discrete Mathematics 27(1), 1979"
    locator: the upper bound (5n + 5)/3 and the lower bound 17n/16 on the number of flips
  - paper: "B. Chitturi, W. Fahle, Z. Meng, L. Morales, C. O. Shields, I. H. Sudborough and W. Voit, An (18/11)n upper bound for sorting by prefix reversals, Theoretical Computer Science 410(36), 2009"
    locator: the upper bound 18n/11 + O(1)
  - paper: "Laurent Bulteau, Guillaume Fertin and Irena Rusu, Pancake flipping is hard, Journal of Computer and System Sciences 81(8), 2015"
    locator: the NP-hardness of the least number of flips
  - paper: "Mohammad H. Heydari and I. Hal Sudborough, On the diameter of the pancake network, Journal of Algorithms 25(1), 1997"
    locator: the lower bound 15n/14 on the number of flips in the worst case
---

Pancake sort sorts an array with one operation only: the *flip*, which reverses a prefix $A[0 \ldots m]$. It is a [selection sort](/selection-sort/) that moves each largest item to the end with two flips: one flip brings the item to the front, and a second flip of the unsorted prefix sends it to its final place. It uses at most $2n - 3$ flips and $n(n-1)/2$ comparisons, and $\Theta(n^2)$ time on an array. The least number of flips for a given input is the [pancake sorting](/pancake-sorting/) problem, which is NP-hard; in the worst case over the inputs of size $n$, it lies between $15n/14$ and $18n/11$, up to small terms.

## In plain words

A cook has a stack of pancakes of different sizes. The only move is to put a spatula under some pancake and turn over all the pancakes above it, which reverses the top part of the stack. The goal is a stack with the largest pancake at the bottom and the smallest on top.

Find the largest pancake. Put the spatula under it and flip, so that it comes to the top. Then flip the whole stack, so that it goes to the bottom. Now it is in place, and you never touch it again. Do the same with the rest of the stack: find its largest pancake, flip it to the top, and flip it down to its place. Each pancake costs at most two flips.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/), with the rule that the array may change only by flips. FLIP$(A, m)$ reverses $A[0 \ldots m]$. The cost is counted in comparisons and in flips. A flip of $m + 1$ items takes $\Theta(m)$ time on an array.

## The algorithm

```pseudo id=main
PANCAKE-SORT(A)                            ▷ n is the length of A
L1  for k ← n down to 2 do                 ▷ A[k .. n − 1] holds the n − k largest items, sorted
L2      m ← the index of the first largest item of A[0 .. k − 1]
L3      if m ≠ k − 1 then
L4          if m ≠ 0 then FLIP(A, m)       ▷ the largest item comes to the front
L5          FLIP(A, k − 1)                 ▷ and goes to index k − 1
```

Line L2 scans the unsorted prefix $A[0 \ldots k-1]$ with $k - 1$ comparisons, as selection sort does. If the largest item is already at index $k - 1$, nothing is done. Otherwise line L4 brings it to index 0, unless it is there already, and line L5 reverses the whole prefix, so the item goes from index 0 to index $k - 1$. The items at the indices $k$ and above are not touched.

## Example

Sort $A = [3, 6, 1, 5, 2, 4]$. Each row shows the flips for one value of $k$, with the size of each reversed prefix.

| $k$ | largest item of $A[0 \ldots k-1]$ | flips | the array after the flips |
|---|---|---|---|
| 6 | 6, at index 1 | size 2, then size 6 | 4 2 5 1 3 6 |
| 5 | 5, at index 2 | size 3, then size 5 | 3 1 4 2 5 6 |
| 4 | 4, at index 2 | size 3, then size 4 | 2 3 1 4 5 6 |
| 3 | 3, at index 1 | size 2, then size 3 | 1 2 3 4 5 6 |
| 2 | 2, at index 1 | none | 1 2 3 4 5 6 |

The run makes $5 + 4 + 3 + 2 + 1 = 15$ comparisons and 8 flips. The least number of flips for this input is 6, so the algorithm is not optimal.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) of the loop of line L1:

> Before the step for $k$, the array is a permutation of the input, $A[k \ldots n-1]$ is sorted, and each item of $A[0 \ldots k-1]$ is at most each item of $A[k \ldots n-1]$.

It holds for $k = n$, when the sorted part is empty. In the step for $k$, line L2 finds a largest item $x$ of $A[0 \ldots k-1]$ at index $m$. The flips of lines L4 and L5 only reverse prefixes of $A[0 \ldots k-1]$, so they do not change the sorted part, and they keep the items of the prefix. After line L4, $x$ is at index 0, and after line L5 it is at index $k - 1$. If $m = k - 1$ already, $x$ is in place with no flip. Now $x$ is at least each item before it and at most each item after it, so the invariant holds for $k - 1$. When the loop ends with $k = 1$, $A[1 \ldots n-1]$ is sorted and $A[0]$ is at most all of them. The full proof is below.

## Complexity

**Comparisons.** Line L2 makes $k - 1$ comparisons for each $k$ from $n$ down to $2$, so the total is $n(n-1)/2$ on each input, as for selection sort.

**Flips.** Each step makes at most 2 flips. For $k = 2$, the largest item of $A[0 \ldots 1]$ is at index 0 or 1, so the step makes at most one flip. So the total is at most $2(n - 2) + 1 = 2n - 3$ flips for $n \ge 2$. The bound is reached, for example, for $n = 3$ by $[1, 3, 2]$, which needs a flip of size 2, one of size 3, and one of size 2. On random inputs the count is close to the bound: about $2n - 21$ on average for $n = 1000$ in measurements.

**Time.** A flip of a prefix of $k$ items takes $\Theta(k)$ time on an array. So the time is $\Theta(n^2)$ on each input, from the comparisons alone. In a model where a flip costs one step, such as a real stack of pancakes, the cost is the number of flips.

**Space.** The flips are done in place with one temporary item, so the extra space is $\Theta(1)$.

**The least number of flips.** Let $P(n)$ be the largest, over the inputs of size $n$, of the least number of flips that sort them. For $n = 1, \ldots, 9$, a search over all permutations gives $P(n) = 0, 1, 3, 4, 5, 7, 8, 9, 10$. Gates and Papadimitriou proved $P(n) \le (5n + 5)/3$ in 1979, and Chitturi and others lowered the bound to $18n/11 + O(1)$ in 2009. Heydari and Sudborough proved $P(n) \ge 15n/14$. Bulteau, Fertin and Rusu proved in 2015 that finding the least number of flips for a given input is NP-hard.

| claim | model and case | bound |
|---|---|---|
| comparisons | each input | $n(n-1)/2$ |
| flips | worst case | $2n - 3$ |
| time | array, each input | $\Theta(n^2)$ |
| extra space | | $\Theta(1)$ |

## Properties

- **Not stable.** A flip reverses the order of equal items in the prefix. On $(2, a), (2, b), (1, c)$, the first largest item is $(2, a)$ at index 0, so the step for $k = 3$ flips the whole array, and the output is $(1, c), (2, b), (2, a)$.
- **In place.** It needs $O(1)$ extra space.
- **Not adaptive.** It always makes $n(n-1)/2$ comparisons. It makes no flip on a sorted input.
- **Uses one kind of move.** All changes are prefix reversals. This is its point: it is a sort for a machine or a puzzle in which only this move exists.

## Variants and improvements

- **[Burnt pancakes](/burnt-pancake-problem/).** Each pancake has a burnt side that must end facing down. A flip also turns each pancake over. The simple method needs at most 3 flips for each pancake, and Cohen and Blum showed that $2n - 2$ flips are always enough when $n \ge 10$.
- **Better flip sequences.** Gates and Papadimitriou group items that are already next to each other in the final order into blocks, and move blocks instead of single items. This gives $(5n + 5)/3$ flips.
- **Sorting by reversals.** If any part $A[i \ldots j]$ can be reversed, not only a prefix, the problem is sorting by reversals, which is studied in genome rearrangement.
- **Fewer comparisons.** The scan of line L2 can use the same tricks as selection sort, but the comparisons stay $\Theta(n^2)$ unless the prefix is kept in a better structure, which no longer fits the model of flips.

## When to use it

Use pancake sort when the only allowed operation is a prefix reversal, as in the puzzle, in some models of parallel networks (the pancake graph), and in teaching. For a normal array sort it is worse than [selection sort](/selection-sort/): it makes the same comparisons and moves many more items, because each flip moves up to $k$ items.

## Pitfalls

- **Flipping when the item is in place.** If the largest item is already at index $k - 1$, the two flips move it away and back, and also disturb the rest. Skip the step, as line L3 does.
- **An extra flip at the front.** If the largest item is at index 0, a flip of size 1 does nothing but counts as a flip. Skip it, as line L4 does.
- **Off by one in the flip size.** FLIP$(A, m)$ reverses $m + 1$ items. Mixing up the index and the size flips one item too many or too few.
- **Counting flips as the cost.** On an array, a flip of $k$ items costs $\Theta(k)$ time, so the method is quadratic even though it uses $O(n)$ flips.

## Implementations

## History

Jacob E. Goodman posed the pancake problem in 1975 under the name Harry Dweighter, in the American Mathematical Monthly. Gates and Papadimitriou published the first nontrivial bounds in 1979, the only research paper by Bill Gates. Heydari and Sudborough improved the lower bound to $15n/14$, Chitturi and others the upper bound to $18n/11$ in 2009, and Bulteau, Fertin and Rusu proved the problem of the least number of flips NP-hard in 2015.

## References
