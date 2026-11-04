---
tag: 8ZEXDP
kind: problem
slug: range-distinct-count-query
name: Range distinct count query
aliases:
- count distinct in range
- range distinct elements
area: data-structures/range-query-structures
level: advanced
summary: Count the distinct values in a subarray.
prereqs: [range-query-problem, fenwick-tree, segment-tree]
see_also: [persistent-segment-tree, mo-algorithm, dominance-counting, merge-sort-tree, wavelet-tree, sliding-window-distinct-count, element-distinctness, mo-algorithm-with-updates]
sources:
  - url: https://www.spoj.com/problems/DQUERY/
    title: SPOJ, DQUERY - D-query
    locator: the problem statement, distinct counts of subarrays for n up to 30000 and 200000 queries
  - url: https://cp-algorithms.com/data_structures/sqrt_decomposition.html
    title: cp-algorithms, Sqrt Decomposition
    locator: section Mo's algorithm
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Preserving the history of its values (Persistent Segment Tree)
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983)"
    locator: the Omega(n log n) lower bound for element distinctness
---

The range distinct count query asks for the number of different values among $A[l], \ldots, A[r]$, for many ranges $[l, r]$ of an array. The count of a range is not a function of the counts of two halves, because a value can occur in both, so the methods of the [range query problem](/range-query-problem/) for a [monoid](/monoid/) do not apply directly. The key step is a change of view: an index $i$ adds one to the count of $[l, r]$ exactly when the previous occurrence of $A[i]$ lies before $l$. This turns the problem into [dominance counting](/dominance-counting/), which a [Fenwick tree](/fenwick-tree/) solves offline and a [persistent segment tree](/persistent-segment-tree/) online, in $O(\log n)$ time per query.

## In plain words

You have the list of all visitors of a shop, in the order they came in, and a visitor who comes back appears again. A question names a stretch of the list and asks how many different people it holds.

Counting the names of a stretch and then removing the repeats is slow. The trick is to count each person only at the first time they appear inside the stretch. A visit is a first time inside the stretch exactly when the same person's visit before it lies outside the stretch, to its left. So for each visit, write down where the same person came last. The answer is the number of visits in the stretch whose earlier visit lies before the start of the stretch.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of values from a set with an equality test. Then queries $(l, r)$ with $0 \le l \le r \le n - 1$.

**Output.** For each query,

$$D(l, r) = \bigl|\{A[i] : l \le i \le r\}\bigr|.$$

**The previous occurrence.** Let $\mathrm{prev}[i]$ be the largest $j < i$ with $A[j] = A[i]$, or $-1$ if there is none. Then

$$D(l, r) = \bigl|\{\, i : l \le i \le r,\ \mathrm{prev}[i] < l \,\}\bigr|. \tag{1}$$

*Proof.* Map each value $v$ that occurs in $A[l \ldots r]$ to its first index $i$ in that range. Then $A[i] = v$ and $\mathrm{prev}[i] < l$, since an earlier occurrence in $[l, i)$ would contradict the choice of $i$. Conversely, an index $i \in [l, r]$ with $\mathrm{prev}[i] < l$ has no earlier occurrence of $A[i]$ in $[l, i)$, so it is the first index of its value. So the map is a bijection between the distinct values and the counted indices. $\square$

The array $\mathrm{prev}$ takes $O(n)$ expected time with a hash table, or $O(n \log n)$ time with sorting.

## Variants

- **Static, offline.** All queries are known first. This is the classic setting of the SPOJ problem DQUERY.
- **Static, online.** Each query must be answered before the next one is read.
- **Point updates.** $A[i] \leftarrow x$ changes $\mathrm{prev}$ at up to three indices: $i$, the next occurrence of the old value, and the next occurrence of $x$. With ordered sets of the positions of each value, the problem becomes dominance counting with point insertions and deletions.
- **Sliding windows.** The ranges are $[i, i + w - 1]$; a hash map of counts moved along the array answers all of them in $O(n)$ expected time; see [sliding window distinct count](/sliding-window-distinct-count/).
- **Distinct values in a subtree.** On a rooted tree, an [Euler tour](/euler-tour-technique/) turns each subtree into a range of the tour.
- **Approximate counts.** With little space, sketches estimate the count; see the [distinct elements problem](/distinct-elements-problem/) for streams.

## Examples

Let $A = [1, 2, 1, 3, 2, 2, 4, 1]$. Then $\mathrm{prev} = [-1, -1, 0, -1, 1, 4, -1, 2]$.

| query $(l, r)$ | the range | distinct values | indices $i$ with $\mathrm{prev}[i] < l$ |
|---|---|---|---|
| $(1, 5)$ | 2, 1, 3, 2, 2 | $\{1, 2, 3\}$, so 3 | 1, 2, 3 |
| $(0, 7)$ | the whole array | $\{1, 2, 3, 4\}$, so 4 | 0, 1, 3, 6 |
| $(4, 7)$ | 2, 2, 4, 1 | $\{1, 2, 4\}$, so 3 | 4, 6, 7 |
| $(2, 2)$ | 1 | 1 | 2 |

**The offline sweep.** Sort the queries by their right end $r$. Scan the array from left to right, and keep a 0-1 array $M$ with $M[j] = 1$ exactly when $j$ is the last occurrence of $A[j]$ in $A[0 \ldots r]$. At step $r$, set $M[\mathrm{prev}[r]] \leftarrow 0$ if $\mathrm{prev}[r] \ge 0$, and $M[r] \leftarrow 1$. Then $D(l, r) = \sum_{j = l}^{r} M[j]$ for each query with this right end. After step 5 of the example, $M = [0, 0, 1, 1, 0, 1, 0, 0]$, and the query $(1, 5)$ reads $0 + 1 + 1 + 0 + 1 = 3$. With $M$ in a Fenwick tree, the total time is $O((n + q) \log n)$.

## Known algorithms

| method | preprocessing | query | space | mode |
|---|---|---|---|---|
| scan with a hash set | none | $O(r - l + 1)$ expected | $O(n)$ | online |
| offline sweep with a [Fenwick tree](/fenwick-tree/) | sort the queries | $O(\log n)$ | $O(n + q)$ | offline |
| [Mo's algorithm](/mo-algorithm/) | sort the queries | $O(n \sqrt q + q)$ in total | $O(n + q)$ | offline |
| [persistent segment tree](/persistent-segment-tree/) | $O(n \log n)$ | $O(\log n)$ | $O(n \log n)$ | online |
| [merge sort tree](/merge-sort-tree/) on $\mathrm{prev}$ | $O(n \log n)$ | $O(\log^2 n)$ | $O(n \log n)$ | online |
| [wavelet tree](/wavelet-tree/) on $\mathrm{prev}$ | $O(n \log n)$ | $O(\log n)$ | $O(n \log n)$ bits | online |
| [Mo's algorithm with updates](/mo-algorithm-with-updates/) | sort the operations | $O(n^{5/3})$ in total for $q = \Theta(n)$ | $O(n + q)$ | offline, point updates |

**Persistent version.** The online method keeps the version $M_r$ of the sweep for every $r$ as a persistent segment tree. Step $r$ changes at most two leaves, so it creates $O(\log n)$ new nodes, and the query $(l, r)$ is a range sum on the version $M_r$.

**Tree of $\mathrm{prev}$ values.** By (1), the query counts the points $(i, \mathrm{prev}[i])$ in the rectangle $[l, r] \times [-1, l - 1]$. A [merge sort tree](/merge-sort-tree/) over the indices with sorted $\mathrm{prev}$ lists answers it with a binary search in each of $O(\log n)$ nodes, and a wavelet tree answers it with one root-to-leaf walk.

**Mo's algorithm.** Keep a count of each value in the current window and the number of nonzero counts. Moving an end of the window by one changes one count in $O(1)$ time, so the total cost is $O(n \sqrt q + q)$ window moves with blocks of size $n / \sqrt q$.

## Bounds

**Lower bound in the comparison setting.** In the [algebraic decision tree](/algebraic-decision-tree/) model, deciding [element distinctness](/element-distinctness/) for $n$ real numbers needs $\Omega(n \log n)$ steps, by Ben-Or. One query $D(0, n - 1)$ decides it, since the items are distinct exactly when the answer is $n$. So preprocessing and one query together need $\Omega(n \log n)$ steps in this model. For integer values below $n$, a table replaces the hash set, and $\mathrm{prev}$ takes $O(n)$ time on the word RAM.

**Upper bound.** $O(n \log n)$ preprocessing and $O(\log n)$ query time online, and $O((n + q) \log n)$ total time offline.

## Reductions

- **Distinct count to dominance counting.** By (1), each query is a count of points in a 3-sided rectangle of the point set $\{(i, \mathrm{prev}[i])\}$. Since $\mathrm{prev}[i] < i$, every $i < l$ has $\mathrm{prev}[i] < l$, so $D(l, r) = |\{ i \le r : \mathrm{prev}[i] < l \}| - l$, a dominance count, and every method for [orthogonal range counting](/orthogonal-range-counting/) applies.
- **Element distinctness to distinct count.** One full-range query decides element distinctness, as in the bound above.
- **Subtree distinct count to range distinct count.** By the Euler tour order of the nodes.

## Applications

- The number of distinct users, words or products in a window of a log, a text or a sales record.
- The number of distinct colors in a subtree of a tree, with an Euler tour.
- Diversity measures of a segment of a genome or of a sequence of events.
- Subproblems of string algorithms, such as the number of distinct letters in a substring.

## References
