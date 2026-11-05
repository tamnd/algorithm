---
tag: NM23TV
kind: problem
slug: dynamic-reachability
name: Dynamic reachability
aliases:
- dynamic s-t reachability
area: graphs/dynamic-graphs
level: advanced
summary: Maintain whether a target vertex is reachable from a source under edge updates.
prereqs: [dynamic-graph, reachability, directed-graph, strongly-connected-components]
see_also: [dynamic-transitive-closure, dynamic-connectivity, even-shiloach-tree, decremental-sssp, italiano-dynamic-transitive-closure, omv-conjecture]
sources:
  - paper: doi:10.1145/322234.322235
    title: Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)
    locator: the whole paper (the search tree with levels that only grow, which also works for directed graphs)
  - paper: doi:10.1145/3313276.3316335
    title: Aaron Bernstein, Maximilian Probst Gutenberg and Christian Wulff-Nilsen, Decremental strongly-connected components and single-source reachability in near-linear time, Proceedings of STOC 2019, 365 to 376
    locator: the main theorem (O(m log^4 n) expected total update time, Las Vegas)
  - paper: doi:10.1109/FOCS.2004.25
    title: Piotr Sankowski, Dynamic transitive closure via dynamic matrix inverse, Proceedings of FOCS 2004, 509 to 517
    locator: the results for fully dynamic single-pair reachability (subquadratic worst-case update time)
  - paper: doi:10.1109/FOCS.2019.00036
    title: Jan van den Brand, Danupon Nanongkai and Thatchaphol Saranurak, Dynamic matrix inverse, improved algorithms and matching conditional lower bounds, Proceedings of FOCS 2019, 456 to 480
    locator: the results for s-t reachability (O(n^1.407) worst-case update time) and the matching conditional lower bounds
  - paper: doi:10.1109/FOCS.2014.53
    title: Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, Proceedings of FOCS 2014, 434 to 443
    locator: the conditional lower bounds for dynamic reachability problems
---

Dynamic reachability is the problem of answering "is there a directed path from $s$ to $t$?" in a [directed](/directed-graph/) [dynamic graph](/dynamic-graph/) under edge insertions and deletions. It has a single-pair form, with $s$ and $t$ fixed, and a single-source form, which keeps the set of vertices reachable from a fixed $s$. Insertions alone are easy, since reachable sets only grow. Deletions alone are harder, but near-linear total time is possible. With both, the problem has polynomial conditional lower bounds, unlike the undirected [dynamic connectivity](/dynamic-connectivity/) problem.

## In plain words

Picture one-way streets in a city. Streets open and close, and you want to know whether you can still drive from your home to the station.

When a street opens, the places you can reach can only grow, so you only explore from the new street. When a street closes, you may lose places, but often another route still exists. The trouble in one-way networks is that a route back is not the same as a route there. Tricks that work for two-way streets, such as a single tree that spans each group, fail here, and the known methods for streets that both open and close are much slower than those for two-way streets.

## Definition

**Input.** A directed graph $G = (V, E)$ on $n$ vertices, a source $s \in V$ (and in the single-pair form a target $t$), and an online sequence of updates $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ of directed edges, mixed with queries.

**Queries.**

- **Single pair:** $\mathrm{reach}()$ returns true if and only if $G$ has a directed path from $s$ to $t$.
- **Single source:** $\mathrm{reach}(v)$ returns true if and only if $G$ has a directed path from $s$ to $v$.

**Output.** The answer to each query before the next operation is read.

The all-pairs form, where both ends are arguments of the query, is [dynamic transitive closure](/dynamic-transitive-closure/). Each bound is worst case, [amortized](/amortized-update-time/) or expected, and a randomized algorithm may be correct only with high probability.

## Variants

- **Incremental single source.** Keep a marked set $R$ of vertices reachable from $s$. After inserting $(u, v)$ with $u \in R$ and $v \notin R$, search from $v$ and mark every newly reached vertex. Each vertex is marked once, and each edge is scanned only after its tail is marked, so the total time over all insertions is $O(n + m)$, deterministic, and each query takes $O(1)$ time.
- **Decremental single source.** The [Even-Shiloach tree](/even-shiloach-tree/), run on the directed graph, keeps breadth-first levels from $s$ in $O(mn)$ total time. Much faster algorithms exist (see below).
- **Decremental strongly connected components.** Keep the [strongly connected components](/strongly-connected-components/) under deletions. Reachability from $s$ is easy to keep once the components are known, because inside a component every vertex reaches every other.
- **Fully dynamic single pair or single source.** Both insertions and deletions.
- **Undirected graphs.** Reachability is connectivity; see [dynamic connectivity](/dynamic-connectivity/).

## Examples

Take $V = \{0, \ldots, 5\}$ with source $0$ and target $4$. The table gives the set reachable from 0 after each update.

| update | reachable from 0 | 4 reachable |
|---|---|---|
| insert 0→1 | 0, 1 | no |
| insert 1→2 | 0, 1, 2 | no |
| insert 3→4 | 0, 1, 2 | no |
| insert 2→3 | 0, 1, 2, 3, 4 | yes |
| insert 4→1 | 0, 1, 2, 3, 4 | yes |
| delete 1→2 | 0, 1 | no |
| insert 0→5 | 0, 1, 5 | no |
| insert 5→3 | 0, 1, 3, 4, 5 | yes |
| delete 0→1 | 0, 1, 3, 4, 5 | yes |

The insertion of $3 \to 4$ adds nothing at once, because 3 is not yet reachable. The insertion of $2 \to 3$ then makes both 3 and 4 reachable. The edge $4 \to 1$ closes the cycle $1, 2, 3, 4$, which is a strongly connected component until $1 \to 2$ is deleted. The deletion of $1 \to 2$ removes three vertices at once. The last row shows that a deletion of an edge out of $s$ need not remove its head: 1 is still reached through $0, 5, 3, 4, 1$.

## Known algorithms

| setting | algorithm | update time | query | case |
|---|---|---|---|---|
| incremental, single source | search from new vertices | $O(n + m)$ total | $O(1)$ | worst, deterministic |
| decremental, single source | [Even-Shiloach tree](/even-shiloach-tree/) | $O(mn)$ total | $O(1)$ | worst, deterministic |
| decremental, single source and SCC | Bernstein, Probst Gutenberg and Wulff-Nilsen (2019) | $O(m \log^4 n)$ total | $O(1)$ | expected, Las Vegas |
| fully dynamic, single pair | Sankowski (2004), dynamic matrix inverse | subquadratic, $O(n^{1.575})$ | $O(n^{0.575})$ | worst, Monte Carlo |
| fully dynamic, single pair | van den Brand, Nanongkai and Saranurak (2019) | $O(n^{1.407})$ | $O(1)$ after the update | worst, Monte Carlo |
| fully dynamic, all pairs | see [dynamic transitive closure](/dynamic-transitive-closure/) | | | |

The algebraic algorithms work with the adjacency matrix $A$ over a finite field, with random values in place of the ones. The entry $(s, t)$ of $(I - A)^{-1}$, or of a related matrix, is nonzero with high probability exactly when $t$ is reachable from $s$. An edge update is a rank-one change of $A$, and the inverse can be kept up to date under rank-one changes. Fast matrix multiplication then gives subquadratic update times. The exponents depend on the current bounds for fast matrix multiplication.

## Bounds

**Upper bounds.** As in the table. In the decremental setting, near-linear total time is possible; in the incremental setting, linear total time.

**Conditional lower bounds.** For the fully dynamic problem, polylogarithmic bounds are not expected. Abboud and Vassilevska Williams (2014) derive polynomial lower bounds for dynamic reachability problems from conjectures such as the hardness of combinatorial Boolean matrix multiplication, and Henzinger, Krinninger, Nanongkai and Saranurak (2015) derive bounds of the same kind from the [OMv conjecture](/omv-conjecture/). Van den Brand, Nanongkai and Saranurak (2019) show that their algebraic upper bounds match conditional lower bounds for the approach. These results contrast with undirected connectivity, which has polylogarithmic amortized algorithms.

## Reductions

- **Reachability to transitive closure.** A transitive closure structure answers any single-pair query.
- **Single source to strongly connected components.** Contract each strongly connected component; the reachable set from $s$ is a union of components, and within the acyclic condensation the problem is simpler. The 2019 algorithm uses this view.
- **To shortest paths.** $t$ is reachable from $s$ exactly when the distance from $s$ to $t$ is finite, so [dynamic single-source shortest paths](/dynamic-single-source-shortest-paths/) and [decremental SSSP](/decremental-sssp/) solve reachability.

## Applications

- **Program analysis.** Pointer and data-flow analyses ask whether one program point can reach another in a graph that changes as the analysis adds facts.
- **Garbage collection.** An object is live when it is reachable from a root; reference updates insert and delete edges of the object graph.
- **Databases and access control.** Queries over relations such as "who can access this file through some chain of groups" are reachability questions on a changing graph.
- **Model checking and deadlock detection.** Whether a bad state is reachable, or whether a wait-for graph has a cycle, under changes.

## References
