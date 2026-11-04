---
tag: 5JQDTK
kind: problem
slug: range-minimum-query
name: Range minimum query
aliases:
- RMQ
- range minimum
- range maximum query
area: data-structures/range-query-structures
level: intro
summary: Return the minimum value of a subarray between indices l and r.
prereqs: [range-query-problem, array]
see_also: [sparse-table, segment-tree, rmq-lca-equivalence, cartesian-tree, lowest-common-ancestor, fischer-heun-rmq, bender-farach-colton-rmq, point-update-range-min-query]
sources:
  - paper: "Michael A. Bender and Martin Farach-Colton, The LCA problem revisited, LATIN 2000: Theoretical Informatics, Lecture Notes in Computer Science 1776, Springer, 2000"
    locator: the definition of RMQ, the naive and sparse table algorithms, the reduction from LCA to the plus-minus-one RMQ and the linear-time algorithm
  - paper: doi:10.1137/090779759
    title: "Johannes Fischer and Volker Heun, Space-Efficient Preprocessing Schemes for Range Minimum Queries on Static Arrays, SIAM Journal on Computing 40(2) (2011), 465-492"
    locator: the 2n + o(n) bit scheme and the matching lower bound through the number of Cartesian trees
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the linear-time preprocessing and constant-time query for nearest common ancestors
  - paper: "Harold N. Gabow, Jon L. Bentley and Robert E. Tarjan, Scaling and related techniques for geometry problems, Proceedings of the 16th Annual ACM Symposium on Theory of Computing (STOC 1984), 135-143"
    locator: the Cartesian tree and the reduction of range minimum to nearest common ancestors
---

The range minimum query (RMQ) problem asks to preprocess an [array](/array/) $A[0 \ldots n-1]$ of items from a total order so that, for any $l \le r$, the minimum of $A[l \ldots r]$, or an index where it occurs, can be returned fast. It is the [range query problem](/range-query-problem/) for the operation $\min$, which is idempotent and has no inverse. The static problem has an optimal solution, with $O(n)$ preprocessing and $O(1)$ query time on the [word RAM](/word-ram/), through its equivalence with the [lowest common ancestor](/lowest-common-ancestor/) problem. The range maximum query is the same problem with the order reversed.

## In plain words

You have a list of numbers, for example the temperature of each day of a year. Many times you ask: what was the lowest temperature between day 40 and day 75? Or: on which day was it? The list does not change, or changes only now and then.

Looking at each day of the stretch is slow when the stretches are long and the questions are many. With some work done once at the start, each answer takes only a few steps, or even a fixed number of steps no matter how long the stretch is.

The same question shows up inside other problems: the nearest common boss of two people in a company chart, and the longest common start of two pieces of a text.

## Definition

**Input.** An array $A[0 \ldots n-1]$ over a totally ordered set $(U, \le)$. Then a sequence of queries $(l, r)$ with $0 \le l \le r \le n - 1$.

**Output.** For each query, the value

$$\mathrm{RMQ}_A(l, r) = \min\{A[i] : l \le i \le r\},$$

or, in the *index version*, the position

$$\mathrm{RMQ}^{\mathrm{idx}}_A(l, r) = \min\{\, j \in [l, r] : A[j] = \mathrm{RMQ}_A(l, r) \,\},$$

the leftmost index of a minimum. Fixing the leftmost index makes the answer unique when values repeat. The index version gives the value with one more array read, and it is the version that the reductions use.

**Cost.** A solution is described as $\langle p(n), q(n) \rangle$: preprocessing time $p(n)$ and query time $q(n)$, with the space stated apart.

## Variants

- **Static or dynamic.** In the dynamic version, point updates $A[i] \leftarrow x$ come between the queries; see [point update range minimum query](/point-update-range-min-query/). With range updates such as "add $c$ to $A[l \ldots r]$", see [range update range query](/range-update-range-query/).
- **Range maximum.** Replace $\le$ by $\ge$. All bounds stay the same.
- **Plus-minus-one RMQ.** Adjacent items differ by exactly 1, as in the depth sequence of an Euler tour. This special case has a simple $\langle O(n), O(1) \rangle$ solution by tables of all short blocks; see [Bender-Farach-Colton RMQ](/bender-farach-colton-rmq/).
- **Encoding (non-systematic) version.** After preprocessing, the array is not available, and only the index version is asked. The question is then the number of bits that the structure needs.
- **Offline.** All $q$ queries are known first. Then they can be answered together in $O((n + q)\,\alpha(n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/): sort them by right end, scan the array with a [monotonic stack](/monotonic-stack/), and merge the popped positions with a union-find structure, in the manner of [Tarjan's offline LCA](/tarjan-offline-lca/); see [Arpa's offline RMQ](/arpa-offline-rmq/).
- **Sliding window minimum.** The queries are $(i, i + w - 1)$ for $i = 0, 1, \ldots$; a [monotonic deque](/monotonic-deque/) answers all of them in $O(n)$ total time.
- **Two dimensions.** The minimum over a rectangle of a matrix.

## Examples

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$, with indices 0 to 7.

| query $(l, r)$ | the range | minimum | leftmost index |
|---|---|---|---|
| $(0, 1)$ | 5, 2 | 2 | 1 |
| $(2, 6)$ | 8, 1, 9, 3, 7 | 1 | 3 |
| $(4, 7)$ | 9, 3, 7, 4 | 3 | 5 |
| $(4, 4)$ | 9 | 9 | 4 |
| $(0, 7)$ | the full array | 1 | 3 |

With repeated values, $A = [3, 1, 4, 1, 5]$ has the minimum 1 at the indices 1 and 3. The query $(0, 4)$ returns the value 1 and the index 1, and the query $(2, 4)$ returns the index 3.

## Known algorithms

| method | preprocessing | query | space |
|---|---|---|---|
| scan the range | none | $O(n)$ | none |
| table of all answers | $O(n^2)$ | $O(1)$ | $\Theta(n^2)$ words |
| [square-root decomposition](/square-root-decomposition/) | $O(n)$ | $O(\sqrt n)$ | $O(\sqrt n)$ words besides the array |
| [segment tree](/segment-tree/) | $O(n)$ | $O(\log n)$, with $O(\log n)$ updates | $O(n)$ words |
| [sparse table](/sparse-table/) | $O(n \log n)$ | $O(1)$ | $O(n \log n)$ words |
| [sqrt tree](/sqrt-tree/) | $O(n \log \log n)$ | $O(1)$ | $O(n \log \log n)$ words |
| [Cartesian tree](/cartesian-tree/) and a constant-time LCA | $O(n)$ | $O(1)$ | $O(n)$ words |
| [Bender-Farach-Colton RMQ](/bender-farach-colton-rmq/) | $O(n)$ | $O(1)$ | $O(n)$ words |
| [Fischer-Heun RMQ](/fischer-heun-rmq/) | $O(n)$ | $O(1)$ | $2n + o(n)$ bits, index version |

The times are worst case. The $O(1)$ query of the last three rows uses word operations on $\Theta(\log n)$-bit words, such as table lookups indexed by a short block.

## Bounds

**Time.** Preprocessing must read each item, so $\langle O(n), O(1) \rangle$ is optimal, and it is reached on the word RAM. Harel and Tarjan gave the first $O(n)$ preprocessing with $O(1)$ query for the lowest common ancestor, and Gabow, Bentley and Tarjan showed that RMQ reduces to it through the Cartesian tree; see the [RMQ-LCA equivalence](/rmq-lca-equivalence/).

**Space of the encoding.** For the index version, two arrays get the same answers to all queries exactly when they have the same Cartesian tree, and each binary tree shape with $n$ nodes arises from some array. So there are $C_n = \frac{1}{n+1}\binom{2n}{n}$ different answer functions, the $n$-th [Catalan number](/catalan-numbers/), and an encoding needs at least $\lceil \lg C_n \rceil = 2n - \Theta(\log n)$ bits. Fischer and Heun gave a structure with $2n + o(n)$ bits and $O(1)$ query time, so the bound is reached up to the lower-order term. For $n = 8$, $C_8 = 1430$, so 11 bits are necessary.

**Dynamic.** If a structure with point updates also returns the index of the minimum, it can sort: build on the $n$ items, then $n$ times find the minimum of the whole array and set that entry to $+\infty$. So in the [comparison model](/comparison-model/), with an $O(n)$ build, a query and an update together need $\Omega(\log n)$ comparisons; the argument is on the [range query structure](/range-query-structure/) page. The segment tree reaches $O(\log n)$ for both.

## Reductions

- **RMQ to LCA.** Build the Cartesian tree of $A$ in $O(n)$ time. The leftmost minimum of $A[l \ldots r]$ is the lowest common ancestor of the nodes $l$ and $r$. See the [RMQ-LCA equivalence](/rmq-lca-equivalence/).
- **LCA to plus-minus-one RMQ.** List the nodes of a rooted tree in an [Euler tour](/euler-tour-technique/), with their depths. The lowest common ancestor of $u$ and $v$ is the node of least depth between the first visits of $u$ and $v$. See [Euler tour LCA](/euler-tour-lca/).
- **Longest common prefix to RMQ.** In a [suffix array](/suffix-array/) with its [LCP array](/lcp-array/), the longest common prefix of the suffixes at ranks $i < j$ is the minimum of $LCP[i+1 \ldots j]$.

## Applications

- [Lowest common ancestor](/lowest-common-ancestor/) queries in trees, and with them distances in weighted trees.
- Longest common prefixes and other string queries on [suffix arrays](/suffix-array/) and [suffix trees](/suffix-tree/).
- Document retrieval and pattern matching with compressed indexes, where the encoding version keeps the index small.
- The minimum or maximum of a sliding window, in signal processing and in time series.

## References
