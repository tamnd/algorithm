---
tag: 8CJ9C7
kind: algorithm
slug: natural-merge-sort
name: Natural merge sort
aliases:
- runs merge sort
area: sorting/comparison-sorts
level: core
summary: Merge sort that first detects existing ascending runs and merges them; adaptive to presorted input.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, r: the number of maximal non-decreasing runs}
  time: {worst: Θ(n log n), runs: O(n log r + n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [merge-sort, sorted-run]
see_also: [timsort, merge-sort, adaptive-sorting, merging-sorted-lists, computing-runs, strand-sort, external-merge-sort, linked-list-merge-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by merging (Algorithm N, natural two-way merge sort, and Algorithm S, straight two-way merge sort)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (bottom-up mergesort, and the exercise on natural mergesort)
  - paper: "Heikki Mannila, Measures of presortedness and optimal sorting algorithms, IEEE Transactions on Computers C-34(4), 1985"
    locator: the measure Runs and the optimality of natural merge sort for it
  - paper: "Vladimir Estivill-Castro and Derick Wood, A survey of adaptive sorting algorithms, ACM Computing Surveys 24(4), 1992"
    locator: the measures of presortedness, including the number of runs
---

Natural merge sort is a [merge sort](/merge-sort/) that starts from the [sorted runs](/sorted-run/) that the input already has, instead of from single items. One scan finds the $r$ maximal non-decreasing runs, and then passes of [merging](/merging-sorted-lists/) combine neighbouring runs in pairs until one run is left. It makes at most $n - 1 + n \lceil \lg r \rceil$ comparisons, so it takes $\Theta(n)$ time on a sorted input and $O(n \log r)$ time in general, and it is never worse than $O(n \log n)$. It is stable and needs $\Theta(n)$ extra space. It is the base of [Timsort](/timsort/), which adds better rules for the order of the merges.

## In plain words

Plain merge sort cuts the cards into single cards and then merges them back in pairs, pairs of pairs, and so on. It does the same amount of work when the cards are already almost in order.

Natural merge sort first looks along the row and finds the stretches that are already in order. Each stretch is a pile that is already sorted. Then it merges the first two piles, the next two piles, and so on, and repeats this until one pile is left. If the row is in order, there is one pile and nothing to merge. If the row has only a few stretches, there are only a few rounds of merging.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array in non-decreasing order, with equal items in their input order. This is the [sorting problem](/sorting-problem/) with a [stable](/stable-sort/) output.

## The algorithm

A run is a maximal part $A[b \ldots e-1]$ with $A[b] \le A[b+1] \le \cdots \le A[e-1]$. The runs split the array, and we keep their bounds in a list $B = [b_0, b_1, \ldots, b_r]$ with $b_0 = 0$ and $b_r = n$, so that run $t$ is $A[b_{t-1} \ldots b_t - 1]$.

```pseudo id=main
NATURAL-MERGE-SORT(A)
L1  B ← [0, b₁, …, b_r]                    ▷ the bounds of the maximal runs; b_r = n
L2  while |B| > 2 do                        ▷ more than one run
L3      C ← [0]
L4      for t ← 2 to |B| − 1 step 2 do      ▷ B is indexed from 0
L5          MERGE(A, B[t − 2], B[t − 1], B[t])
L6          append B[t] to C
L7      if |B| is even then append B[|B| − 1] to C    ▷ an odd number of runs: the last waits
L8      B ← C
```

Line L1 scans the array once: a run ends before index $i$ exactly when $A[i] < A[i-1]$, which costs $n - 1$ comparisons. Each pass of lines L3 to L8 merges run 1 with run 2, run 3 with run 4, and so on. MERGE$(A, lo, mid, hi)$ is the stable merge of [merge sort](/merge-sort/): it copies $A[lo \ldots mid-1]$ to a buffer and merges it with $A[mid \ldots hi-1]$, and on a tie it takes the item from the left. If the number of runs is odd, the last run is copied to the next pass as it is. Each pass halves the number of runs, rounded up.

## Example

Sort $A = [3, 8, 9, 2, 5, 1, 4, 6, 7, 0]$. The scan finds the runs $[3, 8, 9]$, $[2, 5]$, $[1, 4, 6, 7]$ and $[0]$, so $B = [0, 3, 5, 9, 10]$, after 9 comparisons.

| pass | merges | the array after the pass | $B$ | comparisons |
|---|---|---|---|---|
| scan | | 3 8 9 \| 2 5 \| 1 4 6 7 \| 0 | [0, 3, 5, 9, 10] | 9 |
| 1 | $[3, 8, 9] + [2, 5]$, $[1, 4, 6, 7] + [0]$ | 2 3 5 8 9 \| 0 1 4 6 7 | [0, 5, 10] | 3 + 1 |
| 2 | $[2, 3, 5, 8, 9] + [0, 1, 4, 6, 7]$ | 0 1 2 3 4 5 6 7 8 9 | [0, 10] | 8 |

The total is 21 comparisons. A merge stops comparing when one side is empty, so the merge of $[1, 4, 6, 7]$ with $[0]$ takes one comparison. Plain top-down [merge sort](/merge-sort/) makes 23 comparisons on the same input, so on random-looking data the scan costs more than it saves.

## Correctness

The proof uses an invariant of the loop of line L2:

> $B = [b_0, \ldots, b_s]$ with $0 = b_0 < b_1 < \cdots < b_s = n$, each part $A[b_{t-1} \ldots b_t - 1]$ is sorted, and $A$ holds the input items, with equal items in input order within each part and in the order of the parts.

After line L1 it holds, because each run is sorted, and the runs are the input in order. A pass merges neighbouring parts, and the merge of two sorted parts is sorted and keeps the left items first on ties. A part that waits does not change. So the invariant holds for $C$. Each pass with $s \ge 2$ parts leaves $\lceil s/2 \rceil < s$ parts, so the loop stops with $B = [0, n]$, and then $A$ is one sorted part. For $n = 0$, $B = [0]$, and the loop does not run. The full proof is below.

## Complexity

**Comparisons.** The scan of line L1 makes $n - 1$ comparisons. A pass merges each item at most once, and a merge of $p + q$ items makes at most $p + q - 1$ comparisons, so a pass makes at most $n$ comparisons. With $r$ runs, there are $\lceil \lg r \rceil$ passes. So the total is at most

$$C(n, r) \le n - 1 + n \lceil \lg r \rceil.$$

On a sorted input, $r = 1$, and the sort makes exactly $n - 1$ comparisons and no merges. On a random permutation, the mean number of runs is $(n + 1)/2$, so the count is about $n \lg n$, as for plain merge sort. On a reversed input, $r = n$.

**Time.** Each comparison and each move costs $O(1)$, and a pass moves at most $2n$ items. So the time is $O(n + n \log r)$, which is $\Theta(n)$ for a constant number of runs and $O(n \log n)$ in each case.

**Optimal for the number of runs.** Consider the inputs made of $r$ sorted blocks of $n/r$ items each, with any items in the blocks. There are $n!/((n/r)!)^r$ such inputs that need different outputs, so in the [decision tree model](/decision-tree-model/) a sort needs at least $\lg(n!/((n/r)!)^r) = n \lg r - O(n)$ comparisons on some of them. So $O(n + n \log r)$ is optimal up to a constant factor, which Mannila calls optimal with respect to the measure Runs.

**Measured counts.** For $n = 100{,}000$ items made of $r$ sorted blocks with random items, the code below makes these numbers of comparisons:

| $r$ | 1 | 2 | 10 | 100 | 1000 | random input |
|---|---|---|---|---|---|---|
| comparisons | 99,999 | 199,996 | 459,978 | 787,811 | 1,096,423 | 1,617,879 |

**Space.** The merge uses a buffer of at most $n$ items, and $B$ has at most $n + 1$ entries. So the extra space is $\Theta(n)$. The bounds can be found again in each pass instead of stored, at the cost of more comparisons.

| claim | model and case | bound |
|---|---|---|
| comparisons | comparison model, $r$ runs | at most $n - 1 + n \lceil \lg r \rceil$ |
| time | worst case | $\Theta(n \log n)$ |
| time | input with $r$ runs | $O(n + n \log r)$ |
| time | sorted input | $\Theta(n)$ |
| extra space | | $\Theta(n)$ |

## Properties

- **Stable.** Runs are maximal non-decreasing parts, so equal items in input order stay in one run or in runs in input order, and the merge takes the left item on a tie.
- **Adaptive.** The cost depends on the number of runs. A sorted input takes linear time, and an input made of a few sorted parts takes little more.
- **Not in place.** It needs a buffer for the merge.
- **No recursion.** The passes are loops, so the stack is $O(1)$.
- **Good for sequential data.** It reads and writes each run in order, so it suits linked lists, tapes and files. This is how Knuth presents it.

## Variants and improvements

- **Descending runs.** Also take maximal strictly decreasing parts, and reverse them in place before the merges. A reversed input is then one run, and the sort is linear on it. The run must be strictly decreasing, or the reversal breaks stability. [Timsort](/timsort/) does this.
- **Minimum run length.** Extend short runs to a minimum length by [insertion sort](/insertion-sort/). This avoids many merges of tiny runs on random input. Timsort chooses the minimum between 32 and 64.
- **The order of the merges.** Merging runs of very different lengths in pairs wastes work. A rule that merges runs of similar size, as in Timsort, or the best order by the [optimal merge pattern](/optimal-merge-pattern/), gives a cost of about $n H$, where $H$ is the entropy of the run lengths.
- **Linked lists.** On a [linked list](/linked-list-merge-sort/), the merges relink nodes and need no buffer.
- **Strand sort.** [Strand sort](/strand-sort/) also uses existing order, but it extracts increasing subsequences rather than consecutive runs.
- **External sorting.** An [external merge sort](/external-merge-sort/) on a file of natural runs needs fewer passes. [Replacement selection](/replacement-selection/) makes the runs longer before the merges.

## When to use it

Use natural merge sort when the data is often sorted or made of a few sorted parts, for example a sorted list with some new items appended, or the concatenation of sorted files, and when a stable sort is needed. For general use, [Timsort](/timsort/) is the refined form of the same idea and is the library sort of Python and of Java for objects. If the input is random, plain [merge sort](/merge-sort/) is as good and simpler.

## Pitfalls

- **Strict and non-strict runs.** Ascending runs must allow equal items ($A[i-1] \le A[i]$), or equal items split runs for no reason. Descending runs must be strict, or the reversal changes the order of equal items.
- **The last run of an odd pass.** When the number of runs is odd, the last run must be carried to the next pass. Code that drops it, or merges it with an empty run past the end, loses items or reads out of range.
- **Many short runs.** On random input the runs have length about 2, and the first passes do many short merges. Without a minimum run length, the sort is slower than plain merge sort because of the scan and the bookkeeping.
- **An unstable merge.** The merge must take the left item on a tie. With $A[j] \le A[i]$ as the test for the right item, the result is still sorted but not stable.
- **Finding the runs again.** If the code does not store the bounds but scans for runs in each pass, a merge of two runs can create a part that joins with the next part, and the run structure changes. This is still correct, but the pass count is then not $\lceil \lg r \rceil$.

## Implementations

## History

Natural merging comes from the sorting of tapes, where the data on a tape already has runs. Knuth gives Algorithm N, natural two-way merge sort, in Section 5.2.4, together with the straight merge sort that starts from runs of length 1. Mannila (1985) and later surveys on adaptive sorting showed that natural merge sort is optimal for the number of runs. Tim Peters built Timsort on the same idea in 2002.

## References
