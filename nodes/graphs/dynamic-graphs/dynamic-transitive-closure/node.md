---
tag: S1KH42
kind: problem
slug: dynamic-transitive-closure
name: Dynamic transitive closure
aliases:
- dynamic reachability matrix
- fully dynamic all-pairs reachability
area: graphs/dynamic-graphs
level: research
summary: Maintain the reachability relation of a directed graph under edge updates.
prereqs: [dynamic-graph, transitive-closure, strongly-connected-components, dynamic-reachability]
see_also: [italiano-dynamic-transitive-closure, dynamic-all-pairs-shortest-paths, decremental-sssp, even-shiloach-tree, omv-conjecture, amortized-update-time, dynamic-topological-order]
sources:
  - paper: doi:10.1016/0304-3975(86)90098-8
    title: Giuseppe F. Italiano, Amortized efficiency of a path retrieval data structure, Theoretical Computer Science 48, 273 to 281 (1986)
    locator: the whole paper (insertions only, O(n) amortized time per insertion and O(1) query time)
  - paper: doi:10.1109/SFFCS.1999.814580
    title: Valerie King, Fully dynamic algorithms for maintaining all-pairs shortest paths and transitive closure in digraphs, Proceedings of FOCS 1999, 81 to 89
    locator: the transitive closure result (O(n^2 log n) amortized time per update, O(1) query time)
  - paper: doi:10.1145/1059513.1059514
    title: Camil Demetrescu and Giuseppe F. Italiano, Trade-offs for fully dynamic transitive closure on DAGs, breaking through the O(n^2) barrier, Journal of the ACM 52(2), 147 to 156 (2005)
    locator: the main theorem (acyclic graphs, subquadratic update time with sublinear query time, randomized)
  - paper: doi:10.1145/1328911.1328917
    title: Liam Roditty, A faster and simpler fully dynamic transitive closure, ACM Transactions on Algorithms 4(1), 1 to 16 (2008)
    locator: the main theorem (O(n^2) amortized time per update, O(1) query time, deterministic)
  - paper: doi:10.1137/13093618x
    title: Liam Roditty and Uri Zwick, A fully dynamic reachability algorithm for directed graphs with an almost linear update time, SIAM Journal on Computing 45(3), 712 to 733 (2016)
    locator: the main theorem (O(m + n log n) amortized update time, O(n) query time)
  - paper: doi:10.1109/FOCS.2004.25
    title: Piotr Sankowski, Dynamic transitive closure via dynamic matrix inverse, Proceedings of FOCS 2004, 509 to 517
    locator: the main theorems (O(n^2) worst-case update time with O(1) query time, and subquadratic trade-offs, Monte Carlo)
---

Dynamic transitive closure is the problem of answering "is there a directed path from $u$ to $v$?" for every pair $u, v$ of a directed [dynamic graph](/dynamic-graph/) under edge insertions and deletions. It is the all-pairs form of [dynamic reachability](/dynamic-reachability/). One update can change $\Theta(n^2)$ pairs, so a structure that keeps the whole reachability matrix needs about $n^2$ time per update, and several algorithms reach $O(n^2)$ per update with $O(1)$ query time. Other algorithms trade a slower query for an update time close to linear in $m$.

## In plain words

In a set of one-way streets, you want to answer, for any start and any goal, whether the goal can be reached. Streets open and close.

A single new street can join two big areas, so that suddenly very many start and goal pairs become reachable. A single closed street can undo this. If you keep a full table of answers, you may have to rewrite a large part of it after each change. The alternative is to keep less, and do a little search at the time of each question.

## Definition

**Input.** A directed graph $G = (V, E)$ on $n$ vertices and an online sequence of updates $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ of directed edges, mixed with queries.

**Queries.** $\mathrm{reach}(u, v)$ returns true if and only if $G$ has a directed path from $u$ to $v$. Some structures also return such a path.

**Output.** The answer to each query before the next operation is read. The relation $\{(u, v) : \mathrm{reach}(u, v)\}$ is the [transitive closure](/transitive-closure/) of $G$.

**Cost.** Update time and query time, worst case, [amortized](/amortized-update-time/) or expected. Algebraic algorithms are randomized and Monte Carlo: their answers are correct with high probability. Updates are insertions only, deletions only, or both.

Some algorithms also support updates of all edges at one vertex in a single operation, which is natural for the matrix view.

## Variants

- **Insertions only.** Italiano (1986) keeps, for each vertex $u$, a spanning tree of the vertices reachable from $u$. When $(a, b)$ is inserted, for each $u$ that reaches $a$ but not $b$, search from $b$ and add to the tree of $u$ only the vertices not yet in it. Each pair is added once, so the total time is $O(n m + n^2)$ over $m$ insertions, or $O(n)$ amortized per insertion once $m \ge n$, with $O(1)$ query time; see [Italiano's algorithm](/italiano-dynamic-transitive-closure/).
- **Deletions only.** Roditty and Zwick (2002, 2008) and Łącki (2011, 2013) keep the closure in $O(m n)$ total time.
- **Fully dynamic.** Both, with the results below.
- **Acyclic graphs.** Some bounds hold only for DAGs; on a general graph, a structure for [strongly connected components](/strongly-connected-components/) is needed as well.
- **Single source or single pair.** See [dynamic reachability](/dynamic-reachability/).

## Examples

Take $V = \{0, \ldots, 5\}$. The table counts the ordered pairs $(u, v)$ with $u \ne v$ and $v$ reachable from $u$, and how many change.

| update | reachable pairs | added | removed |
|---|---|---|---|
| insert 0→1 | 1 | 1 | 0 |
| insert 1→2 | 3 | 2 | 0 |
| insert 3→4 | 4 | 1 | 0 |
| insert 4→5 | 6 | 2 | 0 |
| insert 2→3 | 15 | 9 | 0 |
| insert 5→0 | 30 | 15 | 0 |
| delete 2→3 | 15 | 0 | 15 |
| delete 5→0 | 6 | 0 | 9 |

The insertion of $2 \to 3$ joins two paths of 3 vertices into one path of 6, which adds $3 \cdot 3 = 9$ pairs. The insertion of $5 \to 0$ closes a cycle, and then every vertex reaches every other: all $6 \cdot 5 = 30$ pairs. One deletion then removes half of them. On $n$ vertices the same pattern changes $\Theta(n^2)$ pairs with one update, again and again if the adversary alternates the insertion and deletion of one edge. So any structure that stores the closure explicitly needs $\Omega(n^2)$ amortized time per update in the worst case.

## Known algorithms

| algorithm | update time | query | case |
|---|---|---|---|
| recompute with one search per vertex | $O(n m)$ | $O(1)$ | worst, deterministic |
| search at query time | $O(1)$ | $O(n + m)$ | worst, deterministic |
| King (1999) | $O(n^2 \log n)$ | $O(1)$ | amortized, deterministic |
| Roditty (2003, 2008) | $O(n^2)$ | $O(1)$ | amortized, deterministic |
| Sankowski (2004) | $O(n^2)$ | $O(1)$ | worst, Monte Carlo |
| Roditty and Zwick (2004, 2016) | $O(m + n \log n)$ | $O(n)$ | amortized, deterministic |
| Demetrescu and Italiano (2005), DAGs | $O(n^{1.575})$ | $O(n^{0.575})$ | worst, Monte Carlo |
| Sankowski (2004), general graphs | $O(n^{1.575})$ | $O(n^{0.575})$ | worst, Monte Carlo |

**Combinatorial methods.** King combines decremental search trees in the style of [Even and Shiloach](/even-shiloach-tree/), built around the vertex of each insertion, with $O(\log n)$ levels of path doubling, which gives the $\log n$ factor. Deletions are handled by the decremental trees, and an insertion builds new trees. Roditty (2008) simplifies this approach and removes the $\log n$ factor.

**Algebraic methods.** Give each edge a random field element and let $A$ be the resulting matrix. Then, with high probability, $v$ is reachable from $u$ exactly when the entry $(u, v)$ of $(I - A)^{-1}$ is nonzero. An edge update is a rank-one change of $A$, and the Sherman-Morrison formula updates the inverse in $O(n^2)$ field operations. Lazy updates and fast matrix multiplication give the subquadratic trade-offs; the exponents depend on the current bound for matrix multiplication.

## Bounds

**Upper bounds.** $O(n^2)$ per update with $O(1)$ query, deterministic amortized or randomized worst case; $O(m + n \log n)$ amortized per update with $O(n)$ query; and subquadratic updates with sublinear queries by algebraic methods.

**Lower bounds.** The example gives $\Omega(n^2)$ per update for an explicit matrix. For any representation, Henzinger, Krinninger, Nanongkai and Saranurak (2015) show, under the [OMv conjecture](/omv-conjecture/), that polynomial update and query times cannot both be made small; their bounds are stated as trade-offs between the two. So polylogarithmic bounds, as for undirected connectivity, are not expected.

## Reductions

- **Strongly connected components.** Contract each component; inside a component every pair is reachable, and between components the closure is that of the acyclic condensation.
- **From single pair.** A structure for the closure answers [single-pair reachability](/dynamic-reachability/), and the conditional lower bounds for the single-pair problem carry over.
- **To shortest paths.** $v$ is reachable from $u$ exactly when the distance is finite, so [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/) solves the problem, usually at a higher cost.
- **To matrix inverse.** As above, reachability is a nonzero test on the inverse of a random matrix.

## Applications

- **Databases.** Recursive queries, such as "all parts that a product contains", are closure queries over relations that change.
- **Program analysis.** Call graphs and points-to graphs change as code changes, and analyses ask which functions or objects can reach which.
- **Access control.** Who can reach a resource through chains of roles and groups.
- **Version control and build systems.** Ancestry queries in a graph of commits or targets that grows over time.

## References
