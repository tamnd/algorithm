---
tag: K93PJS
kind: problem
slug: sorted-array-intersection
name: Intersection of sorted arrays
aliases:
- sorted list intersection
area: techniques/two-pointers-and-windows
level: intro
summary: Report the common elements of two sorted sequences by advancing the pointer at the smaller value.
prereqs: [two-pointers, merging-sorted-lists, loop-invariant]
see_also: [merging-sorted-lists, merging-lower-bound, exponential-search, binary-search, interval-list-intersection-two-pointers, remove-duplicates-from-sorted-array, hash-table, adversary-argument]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4 (merging by two pointers) and Section 5.3.2 (minimum-comparison merging, the Hwang and Lin binary merge and the lower bound from the number of interleavings)
  - paper: doi:10.1016/0020-0190(76)90071-5
    title: Jon Louis Bentley and Andrew Chi-Chih Yao, An almost optimal algorithm for unbounded searching, Information Processing Letters 5(3), 1976
    locator: pp. 82 to 87 (doubling search)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting, set operations on sorted lists)
---

The intersection problem for sorted arrays asks for the values that two sorted arrays have in common. A merge-like scan with one pointer in each array solves it with at most $m + n - 1$ comparisons, which is optimal when the two sizes are close; when one array is much shorter, doubling search gives $O(m \log(n/m))$ comparisons, which matches the lower bound $\log_2 \binom{m+n}{m}$ up to a constant factor. It is the core operation of query processing in inverted indexes, and a basic example of the [two-pointer technique](/two-pointers/).

## In plain words

Two people each have a sorted list of numbers, and they want the numbers that are on both lists. Each one puts a finger on the first number of their list. If the two numbers are equal, write it down and both move to the next number. If they differ, the person with the smaller number moves their finger down: that small number cannot be on the other list anymore, because everything left on the other list is larger. Stop when one list runs out.

Each step moves at least one finger, so the work is at most the total length of the two lists. If one list is very short, it is faster to jump ahead in the long list in growing steps instead of one step at a time.

## Definition

**Input.** Two arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ over a totally ordered set, each sorted in non-decreasing order. We may assume $m \le n$.

**Output (set version).** If each array holds distinct values, the output is the sorted array of the values in $\{A[0], \ldots, A[m-1]\} \cap \{B[0], \ldots, B[n-1]\}$.

**Output (multiset version).** With repeated values, write $c_A(x)$ and $c_B(x)$ for the number of copies of $x$ in $A$ and $B$. The output is the sorted array in which each value $x$ appears $\min(c_A(x), c_B(x))$ times.

**Model.** The algorithms compare two values with a three-way comparison ($<$, $=$ or $>$), as in the [comparison model](/comparison-model/). The cost is the number of comparisons.

## Variants

- **Decision.** Do the two arrays share a value? This is the disjointness problem.
- **Distinct output with repeated input.** Report each common value once, whatever its counts.
- **Many arrays.** Intersect $k$ sorted arrays, for example the posting lists of the $k$ words of a search query. The usual method intersects the two shortest lists first, then intersects the result with the next list.
- **Union and difference.** The same scan, with other rules for what to output, gives the sorted union, the difference $A \setminus B$ and the symmetric difference.
- **Intervals.** For two sorted lists of disjoint intervals, the [interval list intersection](/interval-list-intersection-two-pointers/) uses the same scan and moves the pointer of the interval that ends first.
- **Unsorted input.** Put the shorter array in a [hash table](/hash-table/) and look up each item of the longer one: $O(m + n)$ expected time.

## Examples

**Multiset version.** $A = [1, 2, 2, 4, 7, 9]$ and $B = [2, 2, 2, 5, 7, 10]$. The value 2 has $c_A = 2$ and $c_B = 3$, so it appears twice; 7 appears once. The output is $[2, 2, 7]$, and the set version gives $[2, 7]$. The scan does 8 comparisons:

| step | $i$ | $j$ | $A[i]$ | $B[j]$ | action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 2 | $1 < 2$, $i \leftarrow 1$ |
| 2 | 1 | 0 | 2 | 2 | output 2, both advance |
| 3 | 2 | 1 | 2 | 2 | output 2, both advance |
| 4 | 3 | 2 | 4 | 2 | $4 > 2$, $j \leftarrow 3$ |
| 5 | 3 | 3 | 4 | 5 | $4 < 5$, $i \leftarrow 4$ |
| 6 | 4 | 3 | 7 | 5 | $7 > 5$, $j \leftarrow 4$ |
| 7 | 4 | 4 | 7 | 7 | output 7, both advance |
| 8 | 5 | 5 | 9 | 10 | $9 < 10$, $i \leftarrow 6$, $A$ is used up |

**Disjoint arrays.** $A = [1, 3, 5, 7]$ and $B = [2, 4, 6, 8]$ have an empty intersection. The scan does $m + n - 1 = 7$ comparisons, and the lower bound below shows that 7 are needed for this interleaving.

**A short array against a long one.** For $m = 10$ and $n = 1000$, the scan can need up to $1009$ comparisons, while $\log_2 \binom{1010}{10} \approx 77.9$. Doubling search stays within a constant factor of the second number.

## Known algorithms

**The merge-like scan.** Keep $i$ in $A$ and $j$ in $B$, both starting at 0. While $i < m$ and $j < n$: if $A[i] < B[j]$, set $i \leftarrow i + 1$; if $A[i] > B[j]$, set $j \leftarrow j + 1$; if they are equal, output $A[i]$ and advance both. It keeps this invariant:

> **(I)** The output so far is the multiset intersection of $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$, in sorted order. Each item of $A[0 \ldots i-1]$ and of $B[0 \ldots j-1]$ is at most each of $A[i]$ and $B[j]$ (those that exist). Each item of $B[0 \ldots j-1]$ that is not matched was passed over because it was smaller than the current item of $A$ at that time, and the same holds with $A$ and $B$ swapped.

*Why no common value is skipped.* Suppose $A[i] = x < B[j]$, and the scan drops $A[i]$. All copies of $x$ in $B$ are in $B[0 \ldots j-1]$, because $B[j \ldots n-1] \ge B[j] > x$. None of them was passed over as smaller than an item of $A$: that item would be some $A[i'] > x$ with $i' \le i$, against the sorted order. So by (I) each copy of $x$ in $B$ was matched with its own copy of $x$ in $A[0 \ldots i-1]$. Then $A[i]$ has no partner left in $B$, and the count $\min(c_A(x), c_B(x))$ of the output is not changed by dropping it. The case $A[i] > B[j]$ is the mirror. In the equal case one copy on each side is matched and output, which keeps (I). When one array is used up, by the same argument no item of the other has a partner left. Each comparison advances $i$ or $j$, and the loop stops when one of them reaches its end, so there are at most $m + n - 1$ comparisons. The scan is the merge step of [merge sort](/merge-sort/), with output only on equality.

**Doubling search.** When $m \ll n$, for each $A[i]$ in order, find its position in $B$ from the current position $j$ by [exponential search](/exponential-search/): compare with $B[j], B[j+1], B[j+3], B[j+7], \ldots$ until an item at least $A[i]$ is found, then binary search in the last gap. If the gap is $g_i$ items long, this costs $2 \lceil \log_2 (g_i + 1) \rceil + O(1)$ comparisons (Bentley and Yao, 1976). The gaps add up to at most $n$, and $\log$ is concave, so by Jensen's inequality the total is at most $2 m \log_2 \frac{n + m}{m} + O(m) = O(m \log(n/m) + m)$.

**Binary merging.** Hwang and Lin's merge, described in Knuth Vol. 3 Section 5.3.2, splits $B$ into blocks of about $n/m$ items and finds each item of $A$ by one block step and one binary search. It gives the same order of comparisons with a better constant.

| algorithm | comparisons in the worst case |
| --- | --- |
| merge-like scan | $m + n - 1$ |
| binary search of each $A[i]$ in all of $B$ | $m \lceil \log_2(n+1) \rceil$ |
| doubling search from the current position | $O(m \log(n/m) + m)$ |
| hash table, unsorted input | $O(m + n)$ expected time, no comparisons of order |

## Bounds

**Lower bound by interleavings.** Restrict to inputs where $A$ and $B$ have distinct values and are disjoint, so that the right output is empty. In the merged order of such an input, call two items *adjacent* if one comes right after the other. We claim that a correct algorithm must compare directly each adjacent pair $a \in A$, $b \in B$. Suppose it stops without comparing such a pair $a < b$, with nothing between them. Change $b$ to the value of $a$. No item lies between them, so $B$ stays sorted, and each comparison that the algorithm made has the same result: the only pair whose order changes is $(a, b)$, which was not compared. So the algorithm gives the same empty output, but now $a$ is in both arrays. This is an [adversary argument](/adversary-argument/).

Two consequences follow.

- **Alternating inputs.** For $A = [1, 3, \ldots, 2m - 1]$ and $B = [2, 4, \ldots, 2m]$, all $2m - 1$ neighbors in the merged order are cross pairs, so $2m - 1 = m + n - 1$ comparisons are needed, and the scan is exactly optimal when $m = n$.
- **Counting interleavings.** The direct comparisons of all adjacent cross pairs determine the merged order. So two disjoint inputs with different interleavings must end at different leaves of the algorithm's comparison tree. On these inputs no comparison answers $=$, so the paths form a binary tree with at least $\binom{m+n}{m}$ leaves, and some input needs at least $\log_2 \binom{m+n}{m}$ comparisons. This is the [lower bound for merging](/merging-lower-bound/), and the same bound holds for intersection. Since $\binom{m+n}{m} \ge (n/m)^m$, it is at least $m \log_2(n/m)$. So doubling search is optimal up to a constant factor for all $m \le n$.

**Time.** The scan runs in $\Theta(m + n)$ time in the worst case, and doubling search in $O(m \log(n/m) + m)$ time, plus the size of the output.

## Reductions

- **From merging.** Intersection is a merge that outputs only the equal pairs. Any merge algorithm gives an intersection algorithm with the same number of comparisons, and the lower bound above shows that intersection is not easier.
- **To set operations on unsorted data.** Sort both arrays in $O(m \log m + n \log n)$ time, then intersect. For [element distinctness](/element-distinctness/)-like questions across two sets this is the standard comparison method.
- **Many lists.** The intersection of $k$ lists reduces to $k - 1$ pairwise intersections, shortest lists first; each result is no longer than its shorter input.

## Applications

- **Inverted indexes.** A search engine stores, for each word, the sorted list of documents that contain it. The documents that contain all words of a query are the intersection of these lists. Doubling search is used because the list sizes differ a lot.
- **Databases.** The merge join of two tables sorted on the join key is the multiset version of this scan, with output of all matching pairs.
- **Common items.** Common friends, common tags, common dependencies of two sorted lists.
- **Sparse vectors.** The dot product of two sparse vectors, stored as sorted lists of (index, value), multiplies the values at the common indexes, which this scan finds.

## References
