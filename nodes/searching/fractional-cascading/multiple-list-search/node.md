---
tag: HAQCB7
kind: problem
slug: multiple-list-search
name: Multiple list search
aliases:
- iterated search
- catalog search problem
area: searching/fractional-cascading
level: advanced
summary: Given k sorted lists (catalogs) and a query key, find the successor of the key in every list.
model: comparison-model
complexity:
  vars: {n: the total number of items in all catalogs, k: the number of catalogs that the query visits}
  time: {worst: Θ(log n + k)}
prereqs: [binary-search, lower-bound-query, search-in-sorted-array]
see_also: [catalog-graph, fractional-cascading-bridge, dynamic-fractional-cascading, fractional-cascading-lower-bound, layered-range-tree, merge-sort-tree, hive-graph, predecessor-problem]
sources:
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162 (the iterative search problem on a catalog graph and the fractional cascading structure)
  - paper: doi:10.1007/BF01840441
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading II, Applications, Algorithmica 1 (1986)
    locator: pages 163 to 191 (applications to geometric retrieval problems)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Section 5.6 (Fractional Cascading)
---

Multiple list search, also called iterated search, is the problem of finding the successor of one query key in each of several sorted lists, called catalogs. The plain solution runs one [binary search](/binary-search/) in each list and takes $O(k \log n)$ time for $k$ lists of total size $n$. With $O(n)$ space of preprocessing, the [fractional cascading](/fractional-cascading-bridge/) structure of Chazelle and Guibas answers the query in $O(\log n + k)$ time, which is optimal in the [comparison model](/comparison-model/). The problem appears inside many geometric data structures, where a search walks down a tree and must locate the same coordinate at each node.

## In plain words

Several phone books each list names in alphabetical order. You want to know, for one name, where it would go in each book. You can open each book and search it from scratch. If the books are long, each search takes many steps, and you pay this again for every book.

A better plan works because all the searches look for the same name. Copy a few names from each book into the book before it, with a note that says where each copied name sits in the next book. After you find your place in the first book, the copied names next to it tell you almost exactly where to look in the second book. You then need only one or two more looks per book. The extra copies take only a small amount of space.

## Definition

**Input.** A totally ordered universe $U$ with a largest element $+\infty$. Catalogs $C_1, C_2, \ldots, C_k$, each a sorted list of elements of $U$, of total size $n = \sum_{i} |C_i|$. The catalogs are known in advance and can be preprocessed.

**Query.** A key $x \in U$.

**Output.** For each $i = 1, \ldots, k$, the successor
$$\operatorname{succ}(x, C_i) = \min \{\, y \in C_i \cup \{+\infty\} : y \ge x \,\},$$
given as its position in $C_i$. This is the [lower bound query](/lower-bound-query/) of $x$ in each list. The predecessor version is symmetric.

**General form.** In the form of Chazelle and Guibas, the catalogs sit at the vertices of a [catalog graph](/catalog-graph/) $G$ of bounded degree, and a query gives a key $x$ and a connected subgraph $H$ of $G$ with $k$ vertices. The output is the successor of $x$ in the catalog of each vertex of $H$. The list form above is the case where $G$ is a path and $H$ is the whole path.

**Cost.** The preprocessing builds a structure from the catalogs. Its size is measured in words, and the query time counts comparisons and pointer steps. The goal is a query time close to $O(\log n + k)$ with a structure of size close to $O(n)$.

## Variants

- **Path, tree or subgraph.** The query visits a path, a root-to-leaf path in a tree, or any connected subgraph. In a range tree the subgraph is a set of root-to-leaf paths, and the search can move down several branches.
- **Online choice of the next catalog.** In many uses the next catalog is not known in advance: it depends on the answer in the current one. A walk down a [segment tree](/segment-tree/) chooses its child by a comparison at each node. Fractional cascading allows this, because each step uses only the position in the current catalog.
- **Static or dynamic.** In the static form the catalogs never change. The dynamic form allows inserts and deletes of single items; see [dynamic fractional cascading](/dynamic-fractional-cascading/).
- **Catalogs that are planar maps.** Replace each sorted list by a planar subdivision and the successor query by [point location](/planar-point-location/). This form has no fast general solution with near-linear space; see the [Chazelle-Liu lower bound](/fractional-cascading-lower-bound/).
- **Reporting form.** Report all items of each catalog in an interval $[x, x']$. This adds the output size to the cost, since each list is scanned from the successor of $x$.

## Examples

**Three catalogs.** Let
$$C_1 = (2, 7, 13, 24, 35), \quad C_2 = (5, 9, 16, 21, 30, 42), \quad C_3 = (1, 6, 10, 19, 23, 28, 40),$$
so $n = 18$ and $k = 3$. For $x = 20$ the answer is $24$ in $C_1$ (position 3, counting from 0), $21$ in $C_2$ (position 3) and $23$ in $C_3$ (position 4). For $x = 50$ the answer is $+\infty$ in each list. For $x = 0$ the answer is the first item of each list: $2$, $5$ and $1$. The page on [bridges](/fractional-cascading-bridge/) traces the fractional cascading query for $x = 20$ on these catalogs.

**Many short lists.** With $k = 1000$ catalogs of $1000$ items each, $n = 10^6$. Separate binary searches make about $1000 \cdot \lceil \lg 1001 \rceil = 10\,000$ comparisons. Fractional cascading does one binary search in the first augmented list, which has at most $2n + k + 1 = 2\,001\,001$ items, so at most $\lceil \lg 2\,001\,002 \rceil = 21$ comparisons. Then it makes at most one comparison for each of the other 999 catalogs, so at most $1020$ comparisons in total.

**One long list.** With $k = 1$ the problem is the [search in a sorted array](/search-in-sorted-array/), and nothing is gained.

## Known algorithms

| method | query time | space | notes |
|---|---|---|---|
| $k$ separate [binary searches](/binary-search/) | $O(k \log n)$ | $O(n)$ | no preprocessing |
| merge all catalogs into one list $M$, and store for each item of $M$ its successor in each $C_i$ | $O(\log n + k)$ | $O(nk)$ | one binary search, then $k$ look-ups |
| fractional cascading on a path, sample fraction $1/2$ ([bridges](/fractional-cascading-bridge/)) | $O(\log n + k)$ | $O(n + k)$ | static |
| fractional cascading on a [catalog graph](/catalog-graph/) of degree $d$ | $O(\log n + k \log d)$ | $O(n)$ | Chazelle and Guibas, Part I |
| [dynamic fractional cascading](/dynamic-fractional-cascading/) | $O(\log n + k \log \log n)$ | $O(n)$ | updates in $O(\log \log n)$ amortized time |

The merged list is the simplest way to reach the optimal query time, but its space is too large. Fractional cascading keeps the query time and needs only linear space. On a path, each augmented list keeps every second item of the next augmented list, so the total size is at most $2n + k + 1$. A query does one binary search in the first augmented list and then at most one extra comparison for each later list.

## Bounds

**Upper bound.** $O(\log n + k)$ time and $O(n)$ space, by fractional cascading on a path or on a catalog graph of bounded degree (Chazelle and Guibas, Part I).

**Lower bound.** In the [comparison model](/comparison-model/), each algorithm needs $\Omega(\log n + k)$ steps in the worst case. *Proof.* The output has $k$ entries, so writing it takes at least $k$ steps. For the other term, assume that all $n$ items are distinct, and sort the union of the catalogs as $u_1 < u_2 < \cdots < u_n$. The answer vector for $x$ depends only on the number $r(x)$ of items that are less than $x$, and two keys with different values of $r$ get different answers: if $r(x) < r(x')$, then $u_{r(x)+1}$ lies in some catalog $C_i$, and it is the successor of $x$ in $C_i$ but it is less than $x'$. So the $n + 1$ values $r = 0, 1, \ldots, n$ give $n + 1$ distinct answers. A comparison tree with $n + 1$ different outcomes has depth at least $\lceil \lg (n+1) \rceil$, as in the [search lower bound](/search-lower-bound/). $\square$

So fractional cascading is optimal up to a constant factor among comparison-based methods. The lower bound counts the answer vectors, not the lists: the $k$ answers are not independent, because they all come from one key.

**Planar catalogs.** When the catalogs are planar subdivisions, Chazelle and Liu proved that a query time of $O(k + \operatorname{polylog} n)$ needs nearly quadratic space on a [pointer machine](/pointer-machine/). So the speed-up of fractional cascading does not extend to two dimensions.

## Reductions

- **From a tree walk.** A search that walks from the root of a balanced tree to a leaf, and needs the rank of the same key in a sorted list at each node, is a multiple list search on a path of length $O(\log n)$. With fractional cascading the walk costs $O(\log n)$ in total instead of $O(\log^2 n)$. This is the step that turns a [range tree](/range-tree/) into a [layered range tree](/layered-range-tree/), and it speeds up the [merge sort tree](/merge-sort-tree/).
- **To one search.** With $O(nk)$ space, the problem reduces to one search in the merged list, as in the table above.

## Applications

- [Layered range trees](/layered-range-tree/) for [orthogonal range reporting](/orthogonal-range-reporting/) in the plane: query time $O(\log n + t)$ instead of $O(\log^2 n + t)$, where $t$ is the output size.
- [Segment trees](/segment-tree/) that store sorted lists at their nodes, for [orthogonal segment intersection](/orthogonal-segment-intersection/) queries.
- [Planar point location](/planar-point-location/) in a [monotone subdivision](/monotone-subdivision/) by separating chains, where one query locates a point against many chains (Chazelle and Guibas, Part II).
- The [hive graph](/hive-graph/) of Chazelle, an earlier structure for orthogonal segment intersection that uses the same sampling idea.
- Range searching in databases and packet classification in routers, where one key is looked up in many sorted tables.

## References
