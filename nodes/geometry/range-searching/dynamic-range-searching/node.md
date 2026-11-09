---
tag: TSGFGA
kind: problem
slug: dynamic-range-searching
name: Dynamic range searching
aliases:
- dynamic orthogonal range searching
- fully dynamic range searching
- range searching with updates
area: geometry/range-searching
level: research
summary: Range searching in which points are inserted and deleted between queries.
prereqs: [orthogonal-range-searching, range-tree, decomposable-searching-problem]
see_also: [decomposable-searching-problem, range-tree, global-rebuilding, two-dimensional-fenwick-tree, weight-balanced-tree, dynamic-partial-sums-lower-bound, range-searching-lower-bound, offline-query-processing]
sources:
  - paper: doi:10.1016/0196-6774(80)90015-2
    title: Jon Louis Bentley and James B. Saxe, Decomposable searching problems I. Static-to-dynamic transformation, Journal of Algorithms 1(4), 1980, pages 301 to 358
    locator: the logarithmic method for decomposable problems, with insertions only
  - book: isbn:9783540123309
    title: Mark H. Overmars, The Design of Dynamic Data Structures, Lecture Notes in Computer Science 156, Springer, 1983
    locator: Chapters 5 and 6 (weak deletions, global rebuilding, worst case dynamization) and Chapter 7 (dynamic range trees)
  - paper: doi:10.1145/322276.322281
    title: Michael L. Fredman, A lower bound on the complexity of orthogonal range queries, Journal of the ACM 28(4), 1981, pages 696 to 705
    locator: Omega(n log^d n) semigroup operations for a sequence of n insertions, deletions and queries (DOI to be checked)
  - paper: doi:10.1007/BF01840386
    title: Kurt Mehlhorn and Stefan Näher, Dynamic fractional cascading, Algorithmica 5, 1990, pages 215 to 241
    locator: dynamic range trees in the plane with O(log n log log n + k) query and O(log n log log n) amortized update (DOI to be checked)
  - book: isbn:9783540136422
    title: Kurt Mehlhorn, Data Structures and Algorithms 3, Multi-dimensional Searching and Computational Geometry, Springer, 1984
    locator: Chapter VII, Sections 1 (dynamization of decomposable problems) and 2 (range trees with BB[alpha] trees)
---

Dynamic range searching keeps a set $P$ of points under insertions and deletions while answering range queries, such as counting or reporting the points in a box, a halfspace or a simplex. Static structures like the [range tree](/range-tree/) or the [partition tree](/partition-tree/) are built once and do not allow cheap changes, so dynamic versions pay a factor in the query or update time. Every range searching problem is [decomposable](/decomposable-searching-problem/), so the logarithmic method of Bentley and Saxe turns any static structure into one that supports insertions, at a $\log n$ factor, and [global rebuilding](/global-rebuilding/) adds deletions. For orthogonal ranges, range trees on [weight-balanced trees](/weight-balanced-tree/) give $O(\log^d n + k)$ queries with $O(\log^d n)$ amortized updates, and Fredman's lower bound shows that $\Omega(\log^d n)$ amortized semigroup operations per operation cannot be avoided.

## In plain words

A set of points changes over time: new points arrive and old points leave. In between, questions come in, such as how many points lie inside a given rectangle, or which ones.

A structure built for a fixed set can answer quickly, but rebuilding it after every change would be slow. Dynamic structures avoid this. One general trick keeps several static structures of sizes one, two, four, eight and so on, like the digits of a binary number, and merges them when a new point arrives; a question is asked of each one and the answers are added up. Another trick lets deleted points stay in place, marked, and rebuilds everything once enough of them have piled up.

## Definition

**Notation.** $P$ is the current set of points in $\mathbb{R}^d$, $n = |P|$, and $k$ the output size of a reporting query. A range family $\mathcal{R}$ is fixed in advance: boxes, halfspaces, simplices or disks. $\mathrm{orient}$ and $\mathrm{incircle}$ are the predicates of the static problems for the non-orthogonal families.

**Input.** A sequence of operations, starting from $P = \emptyset$ or from a given set: INSERT$(p)$, DELETE$(p)$ and QUERY$(R)$ for $R \in \mathcal{R}$.

**Output.** For each QUERY, the answer for the current $P$: the points of $P \cap R$ (**reporting**), $|P \cap R|$ or a semigroup sum of weights (**counting**), or whether $P \cap R = \emptyset$ (**emptiness**).

**Degenerate input.** Ranges are closed. $P$ is a multiset: inserting a point already present adds a second copy, and DELETE removes one copy. Deleting a point that is not present is an error the structure may reject.

## Variants

- **Semi-dynamic.** Insertions only, or deletions only. The logarithmic method handles insertions alone with no extra assumptions.
- **Amortized or worst case.** Bounds may hold per operation or on average over a sequence; Overmars and van Leeuwen turned many amortized bounds into worst case ones.
- **Offline.** The whole sequence is known in advance; then time becomes one more coordinate and the problem is a static one in $d + 1$ dimensions, see Reductions and [offline query processing](/offline-query-processing/).
- **Grid coordinates.** Points come from a fixed $U \times U$ grid; a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) counts in $O(\log^2 U)$ time.
- **Range families.** Orthogonal ranges have polylogarithmic dynamic bounds; halfspace, simplex and disk ranges have dynamic partition trees and dynamic halfspace reporting structures with polynomial query time.

## Examples

Start from $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ and query the closed box $Q = [3, 7] \times [2, 6]$ after each update.

| operation | points of $P \cap Q$ after it | count |
|---|---|---|
| QUERY$(Q)$ | $(5,4), (6,6), (7,2)$ | 3 |
| INSERT$(3, 2)$, a corner of $Q$ | $(3,2), (5,4), (6,6), (7,2)$ | 4 |
| DELETE$(6, 6)$ | $(3,2), (5,4), (7,2)$ | 3 |
| INSERT$(5, 4)$, a second copy | $(3,2), (5,4), (5,4), (7,2)$ | 4 |
| INSERT$(8, 4)$, outside $Q$ | unchanged | 4 |

With the logarithmic method, after the $8$ initial points and the $3$ insertions the structure stores $11 = 1011_2$ points, held in static structures of sizes $8$, $2$ and $1$, and each query is answered by the three of them, with the deleted point $(6,6)$ marked in the structure of size $8$.

## Known algorithms

| structure | space | query | update | model and case | reference |
|---|---|---|---|---|---|
| unsorted array | $O(n)$ | $O(n)$ | $O(1)$ | real RAM, worst case | |
| logarithmic method on a static structure with build $P(n)$, query $Q(n)$ | $O(S(n))$ | $O(Q(n) \log n)$ | insertion $O((P(n)/n) \log n)$ | real RAM, amortized | Bentley and Saxe (1980) |
| range tree on BB[$\alpha$] trees, boxes in $\mathbb{R}^d$ | $O(n \log^{d-1} n)$ | $O(\log^d n + k)$ | $O(\log^d n)$ | real RAM, amortized | Lueker (1978), Willard and Lueker (1985) |
| range tree with dynamic fractional cascading, $d = 2$ | $O(n \log n)$ | $O(\log n \log \log n + k)$ | $O(\log n \log \log n)$ | real RAM, amortized | Mehlhorn and Näher (1990) |
| [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/), counting on a $U \times U$ grid | $O(U^2)$ | $O(\log^2 U)$ | $O(\log^2 U)$ | word RAM, worst case | |
| [kd-tree](/kd-tree/) with the logarithmic method and weak deletions, $d = 2$ | $O(n)$ | $O(\sqrt{n} + k)$ | $O(\log^2 n)$ | real RAM, amortized | Overmars (1983) |
| dynamic [partition tree](/partition-tree/), simplex counting | $O(n)$ | $O(n^{1 - 1/d} \log^{O(1)} n)$ | $O(\log^{O(1)} n)$ | real RAM, amortized | Matoušek (1992) |

For the range tree, a BB[$\alpha$] tree keeps every subtree within a constant factor of balance; an update that unbalances a node of subtree size $s$ rebuilds that subtree and its secondary structures in $O(s \log^{d-1} s)$ time, and since this happens only after $\Omega(s)$ updates below the node, the amortized cost per update is $O(\log^{d} n)$.

## Bounds

- **Semigroup arithmetic model, orthogonal ranges (Fredman 1981).** Weights come from a commutative semigroup; the structure keeps variables that hold sums of weights, an insertion or deletion may recompute them, and a query adds stored sums. Only semigroup additions are counted, and the structure cannot subtract. Fredman proved that some sequence of $n$ insertions, deletions and queries for $d$-dimensional boxes needs $\Omega(n \log^d n)$ additions, so $\Omega(\log^d n)$ per operation, amortized. Dynamic range trees meet this bound.
- **Cell probe model, counting.** Already for $d = 1$, dynamic prefix sums need $\Omega(\log n)$ cell probes per operation on words of $\Theta(\log n)$ bits; see [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). For $d = 2$, Larsen (2012) proved that a query time $t_q$ and update time $t_u$ must satisfy $t_q = \Omega((\log n / \log(w t_u))^2)$, where $w$ is the word size.
- **Insertions only.** The logarithmic method costs a factor $\log n$ in query time for problems whose query time is polylogarithmic, and only a constant factor when $Q(n) = n^{\varepsilon}$ for a fixed $\varepsilon > 0$, since the sizes form a geometric series.

## Reductions

- **Decomposability.** For every range $R$, the answer on $A \cup B$ with $A \cap B = \emptyset$ is the union or the sum of the answers on $A$ and $B$. This is what the [logarithmic method](/decomposable-searching-problem/) needs.
- **Deletions for group weights.** If weights form a group, as counts do, a deletion is the insertion of the negated weight, and only an insertion-only structure is needed.
- **Offline to static.** If all operations are known, a point present from time $t_1$ to time $t_2$ becomes, for counting, a point $(p, t_1)$ with weight $+1$ and a point $(p, t_2)$ with weight $-1$; a query $R$ at time $t$ counts the weights in $R \times (-\infty, t)$. This is a static problem with one more dimension.
- **Static as a special case.** Any lower bound for the static problem in a model applies to the dynamic one, with the preprocessing counted as $n$ insertions.

## Applications

- **Databases** with indexes on several attributes that change between queries.
- **Sweep-line algorithms** maintain a dynamic one-dimensional range structure along the sweep, for example in [rectangle intersection reporting](/rectangle-intersection-reporting/).
- **Moving objects and simulations**: positions change over time and region queries are asked in between.
- **Streaming geometric data**: windows of recent points with insertions at one end and deletions at the other.

## References
