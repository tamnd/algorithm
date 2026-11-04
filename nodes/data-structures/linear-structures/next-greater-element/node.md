---
tag: ZTYAAJ
kind: problem
slug: next-greater-element
name: Next greater element
aliases:
- nearest greater to the right
area: data-structures/linear-structures
level: intro
summary: For each position, find the first later element that is strictly larger.
prereqs: [array, stack]
see_also: [monotonic-stack, histogram-stack-algorithm, largest-rectangle-in-histogram, cartesian-tree, trapping-rain-water, sliding-window-maximum, monotonic-deque]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 8, Amortized analysis, the section Nearest smaller elements
  - paper: doi:10.1006/jagm.1993.1018
    title: Omer Berkman, Baruch Schieber and Uzi Vishkin, Optimal doubly logarithmic parallel algorithms based on finding all nearest smaller values, Journal of Algorithms 14(3) (1993)
    locator: pp. 344 to 370
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1, Stacks, queues, and deques (the exercises on sorting and permuting with a stack)
---

The next greater element problem asks, for each position $i$ of an [array](/array/) $A$, for the first position $j > i$ with $A[j] > A[i]$, or for a mark that no such position exists. The [monotonic stack](/monotonic-stack/) solves it for all $n$ positions in $\Theta(n)$ time with at most $2n$ [stack](/stack/) operations, and $\Omega(n)$ is a lower bound because each item must be read. It is one of four mirror forms (greater or smaller, to the right or to the left) of the all nearest smaller values problem, and it is a step of many array algorithms, for example the [largest rectangle in a histogram](/largest-rectangle-in-histogram/) and the [Cartesian tree](/cartesian-tree/).

## In plain words

People stand in a row and look to the right. Each person wants to know who is the first person to the right who is taller. A short person next to a tall person finds the answer at once. A tall person may have to look far, or may find nobody.

The naive way lets each person look until they find someone taller, and this can take a long time for a row that gets shorter and shorter. A faster way walks along the row once and keeps a list of the people who still wait for an answer. When a new person arrives, every waiting person who is shorter has found the answer, and leaves the list. The new person then joins the list. Each person joins once and leaves at most once, so the total work grows only in proportion to the length of the row.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of $n \ge 0$ items from a totally ordered set.

**Output.** An array $N[0 \ldots n-1]$ where, for each $i$ with $0 \le i < n$,

$$N[i] = \min\{\, j : i < j < n \text{ and } A[j] > A[i] \,\},$$

and $N[i] = \bot$ when this set is empty. Implementations often write $-1$ or $n$ for $\bot$.

**Value version.** Output $A[N[i]]$ instead of $N[i]$, with $\bot$ kept. The index version gives the value version in $O(n)$ time, but the value version does not give the index version when items repeat.

The comparison is strict. Equal items are not "greater", so in $[1, 1, 1]$ each answer is $\bot$.

## Variants

- **Four directions.** Next smaller element ($A[j] < A[i]$), previous greater element (the largest $j < i$ with $A[j] > A[i]$) and previous smaller element are the same problem after a reversal of the array, a reversal of the order, or both. The previous smaller form is the all nearest smaller values problem of Berkman, Schieber and Vishkin.
- **Non-strict.** Ask for $A[j] \ge A[i]$. The stack algorithm changes one comparison from $<$ to $\le$.
- **Circular array.** Position $n - 1$ is followed by position $0$. The answer is the first greater item in the order $i + 1, \ldots, n - 1, 0, \ldots, i - 1$. A scan over the indices $0, \ldots, 2n - 1$ taken modulo $n$ solves it in $\Theta(n)$ time.
- **Queries on a subset.** Given a second array $B$ whose items all occur in $A$, report the next greater element of each item of $B$ in $A$. Solve the full problem on $A$ once, store the answers in a [hash table](/hash-table/) keyed by value (the items of $A$ are distinct in the usual statement), and answer each query in $O(1)$ expected time.
- **Both neighbours.** Many uses need the previous smaller and the next smaller element of each position at once: then $A[i]$ is the minimum of exactly the subarrays that start after the first and end before the second.
- **Distance only.** The stock span problem asks for $i - P[i]$, where $P[i]$ is the previous greater element. It is the same computation.

## Examples

| $A$ | $N$ (index) | value version |
|---|---|---|
| $[2, 7, 3, 5, 4, 6, 8]$ | $[1, 6, 3, 5, 5, 6, \bot]$ | $[7, 8, 5, 6, 6, 8, \bot]$ |
| $[4, 5, 2, 25]$ | $[1, 3, 3, \bot]$ | $[5, 25, 25, \bot]$ |
| $[13, 7, 6, 12]$ | $[\bot, 3, 3, \bot]$ | $[\bot, 12, 12, \bot]$ |
| $[5, 4, 3, 2, 1]$ | $[\bot, \bot, \bot, \bot, \bot]$ | all $\bot$ |
| $[1, 1, 1]$ | $[\bot, \bot, \bot]$ | all $\bot$ |
| $[\,]$ | $[\,]$ | $[\,]$ |

In the first row, the item 7 at position 1 waits until the 8 at position 6, because 3, 5, 4 and 6 are all smaller than 7. The decreasing array is the worst case for the naive scan: position $i$ looks at all $n - 1 - i$ later items, $n(n-1)/2$ comparisons in total. For the circular variant, $[1, 2, 1]$ has the value answers $[2, \bot, 2]$: the last 1 wraps around and finds the 2.

## Known algorithms

| method | time | extra space |
|---|---|---|
| for each $i$, scan $j = i + 1, i + 2, \ldots$ | $\Theta(n^2)$ worst case, $\Theta(n)$ best case | $O(1)$ |
| [monotonic stack](/monotonic-stack/), left to right, pop the smaller items | $\Theta(n)$, at most $2n$ stack operations | $O(n)$ |
| monotonic stack, right to left, keep the candidates | $\Theta(n)$ | $O(n)$ |
| jump along answers: to find $N[i]$, try $j = i + 1$, then $N[j]$, $N[N[j]]$, and so on, from right to left | $\Theta(n)$ | $O(1)$ beyond the output |
| Berkman, Schieber and Vishkin, CRCW PRAM | $O(\log \log n)$ time, $O(n)$ work | $O(n)$ |

The left-to-right stack keeps the positions that still have no answer. Their items are non-increasing from the bottom to the top. When $A[i]$ arrives, it pops each position $k$ on top with $A[k] < A[i]$ and sets $N[k] = i$. Then it pushes $i$. Each position is pushed once and popped at most once, so the loop does at most $2n - 1$ stack operations and at most $2n - 2$ comparisons, for $n \ge 1$. The positions left on the stack at the end get $\bot$. The full method, with its invariant and proof, is on the [monotonic stack](/monotonic-stack/) page.

The jumping method works because if $A[j] \le A[i]$ for $j = i + 1$, then no position between $j$ and $N[j]$ can be the answer of $i$: those items are at most $A[j] \le A[i]$.

## Bounds

**Upper bound.** $\Theta(n)$ time on the [word RAM](/word-ram/) and $O(n)$ comparisons in the [comparison model](/comparison-model/), by the stack method.

**Lower bound.** Each correct algorithm reads all $n$ items, for $n \ge 2$, so it needs $\Omega(n)$ time in any model where an algorithm learns the input only by reading items. Proof: let the algorithm run on the all-zero array, and suppose it never reads position $k$. If $k \ge 1$, the output on the all-zero array has $N[k-1] = \bot$, but the array with $A[k] = 1$ and all other items 0 has $N[k-1] = k$. If $k = 0$, the array with $A[0] = -1$ and all other items 0 has $N[0] = 1$, not $\bot$. The algorithm reads the same items with the same values on both arrays, so it gives the same output on both, and one of the outputs is wrong. The output also has $n$ entries, which takes $n$ writes.

So the stack method is optimal up to a constant factor. In the parallel CRCW PRAM model, Berkman, Schieber and Vishkin find all nearest smaller values in $O(\log \log n)$ time with linear total work.

## Reductions

- **Between the four directions.** Previous greater on $A$ is next greater on the reversed array, with each index $j$ mapped to $n - 1 - j$. Next smaller on $A$ is next greater on $-A$ for numbers, or with the order reversed for other items. Each map costs $O(n)$.
- **To a Cartesian tree.** For distinct items, the parent of position $i$ in the max-[Cartesian tree](/cartesian-tree/) of $A$ is the one of its previous greater and next greater elements whose item is smaller. So the previous and next greater elements give the Cartesian tree in $O(n)$ time.
- **From range minimum queries.** With a [range minimum query](/range-minimum-query/) structure, $N[i]$ can also be found by a binary search for the first $j > i$ with $\max A[i+1 \ldots j] > A[i]$, in $O(\log n)$ queries for each $i$. This is slower than the stack, but it answers one position without the others.

## Applications

- **Largest rectangle in a histogram.** The rectangle of full height $h_i$ at bar $i$ extends to the previous and the next smaller bar. See [largest rectangle in a histogram](/largest-rectangle-in-histogram/) and the [histogram stack algorithm](/histogram-stack-algorithm/).
- **Sum of subarray minimums.** $A[i]$ is the minimum of $(i - P[i]) \cdot (S[i] - i)$ subarrays, where $P$ and $S$ are the previous and next smaller positions, with ties broken on one side only.
- **Trapping rain water** and daily temperature questions ("how many days until a warmer day") are next greater element queries. See [trapping rain water](/trapping-rain-water/).
- **Cartesian trees** in linear time, and through them [range minimum queries](/range-minimum-query/) and suffix tree construction.
- **Parallel algorithms.** Berkman, Schieber and Vishkin use all nearest smaller values as a subroutine for other parallel algorithms, for example the matching of parentheses and the merge of two sorted lists.

## References
