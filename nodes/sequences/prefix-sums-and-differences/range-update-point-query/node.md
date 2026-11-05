---
tag: 0HV63V
kind: problem
slug: range-update-point-query
name: Range update point query
aliases:
- offline range increment
- range add point query
area: sequences/prefix-sums-and-differences
level: intro
summary: Add a value to a contiguous range, then read single entries; the offline version is solved by difference arrays.
prereqs: [array, range-query-problem]
see_also: [difference-array, fenwick-tree, segment-tree, point-update-range-sum-query, range-update-range-query, two-dimensional-difference-array, partial-sums-problem, lazy-propagation]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.4 Additional techniques (range updates with a difference array and a binary indexed tree)
  - url: https://cp-algorithms.com/data_structures/fenwick.html
    title: cp-algorithms, Fenwick Tree
    locator: section Range Update and Point Query
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (the Omega(log n) bound for dynamic partial sums, which transfers by the reduction on this page)
---

The range update point query problem keeps an [array](/array/) $a[0 \ldots n-1]$ under two operations: add a value $c$ to every item of a range $a[l \ldots r]$, and read one item $a[i]$. When all the updates come before the reads, the [difference array](/difference-array/) solves it in $\Theta(n + m + q)$ time for $m$ updates and $q$ reads. When the two operations interleave, a [Fenwick tree](/fenwick-tree/) over the difference array does each operation in $O(\log n)$ time. The problem is the mirror image of the [point update range sum query](/point-update-range-sum-query/), and the two have the same complexity.

## In plain words

You have a row of numbers, such as the number of guests booked on each night of a season. Each booking adds guests to a run of nights. From time to time someone asks how many guests are booked on one given night.

A booking can cover many nights, so changing every night one by one is slow. The trick is to write down only where each booking starts and where it ends: plus the guests at the start, minus the guests after the end. The count on one night is then the running total of these marks up to that night. If all bookings come first, one walk computes every night. If questions arrive between bookings, a structure that keeps running totals fast, such as a Fenwick tree, answers each question in a few steps.

## Definition

**Data.** An array $a[0 \ldots n-1]$ over an abelian group $(G, +, 0)$, usually the integers. It is given at the start, or it is all zeros.

**Operations.**

- $\textsc{add}(l, r, c)$ with $0 \le l \le r \le n - 1$ and $c \in G$: set $a[i] \leftarrow a[i] + c$ for each $i$ with $l \le i \le r$.
- $\textsc{get}(i)$ with $0 \le i \le n - 1$: return the current $a[i]$.

**Forms.** In the *batch* form, all $m$ calls of $\textsc{add}$ come before all $q$ calls of $\textsc{get}$. In the *online* form, the calls come in any order and each $\textsc{get}$ is answered before the next call is read. The cost is the total time of a sequence of $m$ updates and $q$ reads, plus the preprocessing of $a$.

**The key identity.** Let $d[0] = a[0]$ and $d[i] = a[i] - a[i-1]$ for $1 \le i \le n - 1$, and $d[n] = 0$. Then $a[i] = d[0] + \cdots + d[i]$ for each $i$, and $\textsc{add}(l, r, c)$ changes exactly $d[l]$ by $+c$ and $d[r+1]$ by $-c$. So the problem is the [partial sums problem](/partial-sums-problem/) on $d$: a range add is two point adds, and a point read is one prefix sum.

## Variants

- **Batch reads of the whole array.** After all updates, output the whole array. This is the plain [difference array](/difference-array/) technique.
- **Range assignment.** $\textsc{assign}(l, r, c)$ sets the range to $c$ instead of adding. Assignments do not commute, so the difference trick fails. A segment tree with [lazy propagation](/lazy-propagation/) or an ordered map of runs, the [Chtholly tree](/chtholly-tree/), handles it.
- **Range add, range sum.** The reads ask for $\sum_{i=l}^{r} a[i]$; see the [range update range query](/range-update-range-query/).
- **Range max-update.** $a[i] \leftarrow \max(a[i], c)$ on a range, with point reads. A segment tree stores the largest pending value on each node, and a read takes the maximum over the path from the leaf to the root, in $O(\log n)$.
- **Two dimensions.** Add to a rectangle, read a cell. In the batch form, this is the [two-dimensional difference array](/two-dimensional-difference-array/); online, a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) over the two-dimensional differences.
- **Huge index ranges.** With indices up to $10^9$ and few operations, sort the update ends and read positions, then sweep; or use a [dynamic segment tree](/dynamic-segment-tree/).

## Examples

Start with $a = [4, 1, 3, 0, 2, 5]$. The ranges are inclusive.

| operation | array after | answer |
|---|---|---|
| $\textsc{add}(1, 3, +2)$ | $[4, 3, 5, 2, 2, 5]$ | |
| $\textsc{get}(2)$ | | $5$ |
| $\textsc{add}(0, 4, -1)$ | $[3, 2, 4, 1, 1, 5]$ | |
| $\textsc{get}(4)$ | | $1$ |
| $\textsc{get}(5)$ | | $5$ |
| $\textsc{add}(3, 5, +3)$ | $[3, 2, 4, 4, 4, 8]$ | |
| $\textsc{get}(3)$ | | $4$ |

On the difference array, the first update adds $2$ to $d[1]$ and $-2$ to $d[4]$; the second adds $-1$ to $d[0]$ and $+1$ to $d[5]$; the third adds $3$ to $d[3]$ and $-3$ to $d[6]$. The read $\textsc{get}(3)$ after all of them is the prefix sum $d[0] + d[1] + d[2] + d[3]$, which is $3 + (-1) + 2 + 0 = 4$.

## Known algorithms

| method | add | get | form |
|---|---|---|---|
| loop over the range | $O(r - l + 1)$ | $O(1)$ | online |
| [difference array](/difference-array/) and one prefix-sum pass | $O(1)$ | $O(1)$ after a $\Theta(n)$ pass | batch |
| difference array, with a prefix sum per read | $O(1)$ | $O(i + 1)$ | online |
| [square-root decomposition](/square-root-decomposition/) | $O(\sqrt n)$ | $O(1)$ | online |
| [Fenwick tree](/fenwick-tree/) on the differences | $O(\log n)$ | $O(\log n)$ | online |
| [segment tree](/segment-tree/), add stored on $O(\log n)$ nodes | $O(\log n)$ | $O(\log n)$ | online |

All times are worst case. The square-root method splits the array into blocks of about $\sqrt n$ items. An add changes the pending value of each block that it covers fully and the items of at most two partial blocks. A read returns the item plus the pending value of its block. The segment tree needs no lazy pushes for this problem: an add stores $c$ on the $O(\log n)$ canonical nodes of $[l, r]$, and a read sums the stored values on the path from the root to leaf $i$.

## Bounds

**Batch form.** $\Theta(n + m + q)$ time is optimal: the input has this size and must be read.

**Online form.** The reduction of the definition works in both directions. A point add $A[i] \mathrel{+}= c$ of the partial sums problem is the range add $\textsc{add}(i, n-1, c)$ on the array of prefix sums, and a prefix sum is a point read of that array. So the online problem has the same cell-probe complexity as dynamic partial sums. By the theorem of Patrascu and Demaine (2006), with word-sized values, every structure has $\max(t_{\text{add}}, t_{\text{get}}) = \Omega(\log n)$ amortized, and the Fenwick tree meets this bound. See the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) for the exact statement and the trade-off between the two costs.

## Reductions

- **To partial sums.** As in the definition: $\textsc{add}(l, r, c)$ is two point adds on $d$, and $\textsc{get}(i)$ is a prefix sum of $d$. The cost overhead is $O(1)$ per operation.
- **From partial sums.** The reverse direction is in the Bounds section.
- **From interval coverage.** "How many of these intervals contain the point $x$" is $\textsc{add}(l, r, 1)$ per interval and $\textsc{get}(x)$.
- **To two-dimensional dominance counting, offline.** A read at time $t$ of position $i$ sums the updates with time before $t$ and $l \le i \le r$. With the updates and reads sorted by time, this is a sweep over time with a Fenwick tree over positions.

## Applications

- Booking and scheduling: seats per stop of a train, rooms per night, machines busy per time slot.
- Coverage counts in genomics: the number of sequencing reads that cover each base of a reference genome is a batch of range adds of $+1$.
- Image processing and graphics: adding constant boxes to a grid, the two-dimensional form.
- A building block of [range update range query](/range-update-range-query/) with two Fenwick trees.

## References
