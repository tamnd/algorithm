---
tag: M8ZTQT
kind: problem
slug: merging-sorted-lists
name: Merging sorted lists
aliases:
- two-way merge
- merge problem
area: sorting/comparison-sorts
level: core
summary: Combine two sorted sequences into one sorted sequence, in n+m-1 comparisons in the worst case.
model: comparison-model
complexity:
  vars: {m: the length of the first list, n: the length of the second list}
  time: {worst: Θ(m + n)}
prereqs: [sorting-problem]
see_also: [merge-sort, k-way-merge, merging-lower-bound, in-place-merge-sort, timsort, parallel-merge, median-of-two-sorted-arrays, optimal-merge-pattern]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by merging (Algorithm M, two-way merge), and Section 5.3.2, Minimum-comparison merging (the function M(m, n), the bound M(n, n) = 2n - 1, and binary merging)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3.1, The divide-and-conquer method (the procedure MERGE and its loop invariant)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (the abstract in-place merge)
  - paper: "F. K. Hwang and S. Lin, A simple algorithm for merging two disjoint linearly ordered sets, SIAM Journal on Computing 1(1), 1972"
    locator: the binary merging algorithm
---

The merging problem asks to combine two sorted lists of $m$ and $n$ items into one sorted list of all $m + n$ items. The standard two-way merge solves it in $\Theta(m + n)$ time with at most $m + n - 1$ comparisons, and for $m = n$ no algorithm in the [comparison model](/comparison-model/) does better in the worst case. When one list is much shorter, binary and [exponential search](/exponential-search/) need only $O(m \log(n/m + 1))$ comparisons. Merging is the step of [merge sort](/merge-sort/), of [Timsort](/timsort/) and of external sorts.

## In plain words

Two piles of cards are each in order, with the smallest card on top. You want one pile in order. You look at the two top cards, take the smaller one, and put it on the new pile. Then you look at the two top cards again. When one pile is empty, you put the rest of the other pile on the new pile.

Each look at two cards places one card, so the work grows with the total number of cards. This is far less work than to sort all the cards from the start, because the order inside each pile is already known.

## Definition

**Input.** Two sequences $A = a_1, \ldots, a_m$ and $B = b_1, \ldots, b_n$ of items with a [total order](/total-order/) on their keys, with $a_1 \le \cdots \le a_m$ and $b_1 \le \cdots \le b_n$.

**Output.** A sequence $C = c_1, \ldots, c_{m+n}$ with $c_1 \le \cdots \le c_{m+n}$ whose items are the items of $A$ and $B$, each used once. So $C$ is a [permutation](/permutation/) of the concatenation of $A$ and $B$, and it is sorted.

**Stable merge.** A merge is *stable* when the items of $A$ keep their order, the items of $B$ keep theirs, and on equal keys each item of $A$ comes before each item of $B$. A [stable sort](/stable-sort/) such as merge sort needs a stable merge.

**The interleavings.** If all keys are distinct, the output is fixed by the set of the positions in $C$ that hold items of $A$. There are $\binom{m+n}{m}$ such sets, and each one is a possible answer. This count gives the lower bound below.

## Variants

- **Merging $k$ lists.** Merge $k$ sorted lists of $N$ items in total. This is the [k-way merge](/k-way-merge/). A heap of the $k$ heads takes $O(N \log k)$ time.
- **In place.** Merge two adjacent sorted parts $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$ of one array with $O(1)$ extra space. Linear-time methods exist but are complex. See [in-place merge sort](/in-place-merge-sort/).
- **Linked lists.** Merge two sorted linked lists by relinking the nodes. It needs no extra space and is stable. This is the step of [linked-list merge sort](/linked-list-merge-sort/).
- **Very different sizes.** When $m \ll n$, the cost in comparisons is $\Theta(m \log(n/m + 1))$, much less than $m + n$. The output still has $m + n$ items, but in a linked list or a balanced tree the long list does not have to be copied.
- **Set operations.** The union, the intersection and the difference of two sorted sets use the same scan, and output only some of the items.
- **Parallel merge.** Split the output into equal blocks by binary search, and merge the blocks at the same time. See [parallel merge](/parallel-merge/) and [merge path](/merge-path/).

## Examples

**A short merge.** Merge $A = [1, 4, 7]$ and $B = [2, 3, 9, 10]$. The merge compares $1$ with $2$, $4$ with $2$, $4$ with $3$, $4$ with $9$ and $7$ with $9$, and it outputs $1, 2, 3, 4, 7$. Now $A$ is empty, so it copies $9, 10$ without a comparison. The output is $[1, 2, 3, 4, 7, 9, 10]$, after 5 comparisons, one less than $m + n - 1 = 6$.

**The worst case.** Merge $A = [1, 3, 5]$ and $B = [2, 4, 6]$. Each comparison outputs one item, and the last item, $6$, is the only one left when the other list is empty. So the merge makes $5 = m + n - 1$ comparisons.

**The best case.** If $a_m \le b_1$, the merge compares each $a_i$ with $b_1$ and then copies $B$. That is $m$ comparisons. With the test $a_m \le b_1$ first, one comparison is enough. Merge sort and Timsort use this test to skip a merge.

**Equal keys.** Merge $A = [(2, a), (5, b)]$ and $B = [(2, c), (3, d)]$ by the first field. A stable merge takes the item of $A$ on a tie, so it outputs $(2, a), (2, c), (3, d), (5, b)$.

**Not a merge.** The output $[1, 2, 3, 4, 7, 9]$ for the first example is sorted but loses the item $10$, so it is not a correct merge.

## Known algorithms

- **Two-way merge.** Compare the two heads and output the smaller, until one list is empty, then copy the rest. It takes $\Theta(m + n)$ time and at most $m + n - 1$ comparisons. It is Algorithm M of Knuth, Section 5.2.4, and the procedure MERGE of CLRS, Section 2.3.1. To be stable, take the item of $A$ on a tie.
- **Binary insertion.** For $m = 1$, find the place of $a_1$ in $B$ by [binary search](/binary-search/), in $\lceil \lg(n+1) \rceil$ comparisons. For small $m$, insert each $a_i$ in turn, in about $m \lg n$ comparisons.
- **Binary merging.** Hwang and Lin (1972) mix the two ideas. With $m \le n$, the algorithm compares $a_m$ with the item about $n/m$ places from the end of $B$. If $a_m$ is smaller, it outputs that whole block of $B$ at once, and else it places $a_m$ in the block by binary search. It uses $O(m \log(n/m + 1))$ comparisons, which is the order of the lower bound. Knuth gives it in Section 5.3.2.
- **Galloping.** For each head, find how many items of the other list are smaller by [exponential search](/exponential-search/), and copy them as a block. This takes $O(m \log(n/m + 1))$ comparisons and needs no knowledge of $m$ and $n$ in advance. [Timsort](/timsort/) switches to it when one list wins many times in a row.
- **$k$-way merge with a heap.** Keep the heads of the $k$ lists in a [priority queue](/priority-queue/). Each output costs $O(\log k)$. See [k-way merge](/k-way-merge/).
- **In-place merges.** Rotations and block swaps give $O(1)$ extra space. A simple recursive form takes $O((m + n) \log(m + n))$ time, and more complex forms take linear time.

## Bounds

**The output bound.** Each algorithm must write the $m + n$ items, so the time is $\Omega(m + n)$ when the output is an array. The two-way merge reaches it.

**The decision-tree bound.** In the [decision tree model](/decision-tree-model/), each of the $\binom{m+n}{m}$ interleavings needs its own leaf. A binary tree of height $h$ has at most $2^h$ leaves, so the worst case needs at least $\lceil \lg \binom{m+n}{m} \rceil$ comparisons. For $m \le n$, this is $\Theta(m \log(n/m + 1))$. For $m = 1$ it is $\lceil \lg(n+1) \rceil$, and binary search reaches it. See [the merging lower bound](/merging-lower-bound/).

**The case $m = n$.** Write $M(m, n)$ for the least worst-case number of comparisons. Then $M(n, n) = 2n - 1$, so the two-way merge is optimal. The proof is an [adversary argument](/adversary-argument/): the adversary answers so that the output is $a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n$. Each of the $2n - 1$ pairs of neighbours in this list must be compared, because if one pair is not compared, the order with only those two items in the other order is also consistent with all answers. The decision-tree bound is weaker here, as the table shows.

| $n$ | $\binom{2n}{n}$ | $\lceil \lg \binom{2n}{n} \rceil$ | $M(n, n) = 2n - 1$ |
|---|---|---|---|
| 1 | 2 | 1 | 1 |
| 2 | 6 | 3 | 3 |
| 3 | 20 | 5 | 5 |
| 4 | 70 | 7 | 7 |
| 5 | 252 | 8 | 9 |
| 10 | 184,756 | 18 | 19 |
| 100 | about $9.05 \times 10^{58}$ | 196 | 199 |

**Unequal sizes.** For $m = 10$ and $n = 1000$, the decision-tree bound is 78 comparisons, against 1009 for the two-way merge. Binary merging and galloping need $O(m \log(n/m + 1))$ comparisons, so they are within a constant factor of the bound.

**$k$ lists.** For $k$ lists of $N/k$ items each, the number of interleavings is $N! / ((N/k)!)^k$, whose logarithm is about $N \lg k$. So a heap of the heads is optimal up to a constant factor.

## Reductions

- **Merge sort reduces sorting to merging.** Split, sort each half, and merge. With a linear-time merge, the time is $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$ by the [master theorem](/master-theorem/).
- **Merging reduces to sorting.** Concatenate the two lists and sort them. This gives no better bound, but shows that merging is no harder than sorting.
- **Merging gives the [median of two sorted arrays](/median-of-two-sorted-arrays/)** by a partial merge in $O(m + n)$ time, though binary search does it in $O(\log \min(m, n))$.
- **Set union and intersection** of sorted lists reduce to one merge scan.

## Applications

- **Sorting.** [Merge sort](/merge-sort/), [natural merge sort](/natural-merge-sort/) and [Timsort](/timsort/) consist of merges.
- **External sorting.** An [external merge sort](/external-merge-sort/) sorts runs that fit in memory, then merges them in passes, because a merge reads each list in order.
- **Databases.** The [sort-merge join](/sort-merge-join/) merges two tables that are sorted on the join key.
- **Search engines.** The posting lists of words are sorted by document number, and a query intersects them with a merge or with galloping.
- **Logs.** Two logs that are sorted by time are combined into one with a merge.

## References
