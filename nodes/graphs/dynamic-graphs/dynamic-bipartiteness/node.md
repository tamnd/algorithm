---
tag: 0BY2JF
kind: problem
slug: dynamic-bipartiteness
name: Dynamic bipartiteness
aliases:
- fully dynamic bipartiteness testing
area: graphs/dynamic-graphs
level: advanced
summary: Maintain whether the graph is bipartite under edge insertions and deletions.
prereqs: [dynamic-connectivity, bipartite-graph, bipartite-odd-cycle-theorem]
see_also: [bipartiteness-testing, dsu-with-parity, offline-dynamic-connectivity, dynamic-minimum-spanning-tree, sparsification, link-cut-tree]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: the results for bipartiteness (O(n^(1/2)) worst-case time per update)
  - paper: doi:10.1145/320211.320215
    title: Monika R. Henzinger and Valerie King, Randomized fully dynamic graph algorithms with polylogarithmic time per operation, Journal of the ACM 46(4), 502 to 516 (1999)
    locator: the bipartiteness result (polylogarithmic expected amortized time)
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: Section 1 (the list of problems with an Omega(log n) bound)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 (other problems, including bipartiteness, that the techniques solve)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.4 (testing bipartiteness, and the odd cycle characterization)
---

Dynamic bipartiteness is the problem of keeping the answer to "is the graph [bipartite](/bipartite-graph/)?" for an undirected [dynamic graph](/dynamic-graph/) under edge insertions and deletions. A graph is bipartite exactly when it has no odd cycle, so the problem is to detect when an insertion closes an odd cycle and when a deletion breaks the last one. A spanning forest with parities answers the question for insertions in nearly constant time. With deletions, the known fully dynamic algorithms build on the structures for [dynamic connectivity](/dynamic-connectivity/) and minimum spanning forests, and the $\Omega(\log n)$ cell-probe lower bound of dynamic connectivity also applies.

## In plain words

Some people are in a network of quarrels, and you want to split them into two rooms so that no two people who quarrel share a room. This is possible exactly when there is no circle of quarrels of odd length. People join or end quarrels over time, and after each change you want to know whether a split into two rooms is still possible.

When a new quarrel starts between two people in different groups, the groups merge and one group swaps its rooms if needed. When it starts inside one group, it is fine if the two are in different rooms, and it breaks the split if they share a room. When a quarrel ends, an odd circle may disappear, and the program must find out whether any other odd circle is left.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, at first with no edges, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates and $\mathrm{bipartite}()$ queries.

**Output.** After each query, true if and only if there is a map $c : V \to \{0, 1\}$ with $c(u) \ne c(v)$ for each edge $\{u, v\} \in E$. By the [odd cycle theorem](/bipartite-odd-cycle-theorem/), this holds if and only if $G$ has no cycle of odd length.

**Cost.** Update time and query time, worst case, [amortized](/amortized-update-time/) or expected. A common stronger query is $\mathrm{bipartite}(v)$: is the component of $v$ bipartite? Another is $\mathrm{sameside}(u, v)$ for $u$ and $v$ in one bipartite component: do they get the same color in its 2-coloring, which is unique up to a swap?

**Self-loops.** An edge $\{v, v\}$ is a cycle of length 1, so a graph with a self-loop is not bipartite.

## Variants

- **Incremental.** Insertions only. Keep a [disjoint-set structure with parity](/dsu-with-parity/): each element stores the parity of its path to its parent, and a find returns the parity of the element relative to its representative. An insertion of $\{u, v\}$ with $u$ and $v$ in different sets merges them with the parity that makes $c(u) \ne c(v)$. With $u$ and $v$ in one set, the graph stops being bipartite if they have equal parity. This takes $O(\alpha(n))$ amortized time per operation.
- **Decremental.** Deletions only.
- **Offline.** The whole sequence is known; divide and conquer over time with a parity union-find with rollback gives $O(\log q \log n)$ time per operation for a sequence of length $q$, as in [offline dynamic connectivity](/offline-dynamic-connectivity/).
- **Fully dynamic.** Both insertions and deletions, online.
- **Odd cycle transversal.** Keep the size of a smallest set of vertices or edges whose removal makes the graph bipartite. This is NP-hard even in the static case.

## Examples

Take $V = \{0, \ldots, 5\}$. The table follows a fully dynamic sequence and gives a 2-coloring $(c(0), \ldots, c(5))$ when one exists.

| update | edges after it | bipartite | a coloring |
|---|---|---|---|
| insert(0, 1) | 01 | yes | 0, 1, 0, 0, 0, 0 |
| insert(1, 2) | 01, 12 | yes | 0, 1, 0, 0, 0, 0 |
| insert(2, 3) | 01, 12, 23 | yes | 0, 1, 0, 1, 0, 0 |
| insert(3, 0) | 01, 12, 23, 30 | yes | 0, 1, 0, 1, 0, 0 |
| insert(0, 2) | 01, 12, 23, 30, 02 | no | |
| delete(1, 2) | 01, 23, 30, 02 | no | |
| delete(0, 2) | 01, 23, 30 | yes | 0, 1, 0, 1, 0, 0 |
| insert(4, 5) | 01, 23, 30, 45 | yes | 0, 1, 0, 1, 0, 1 |
| insert(3, 4) | 01, 23, 30, 45, 34 | yes | 0, 1, 0, 1, 0, 1 |

The insertion of $02$ joins two vertices of the same color, so it closes the odd cycles $0, 1, 2$ and $0, 2, 3$. Deleting $12$ breaks the first one, but the triangle $0, 2, 3$ remains, so the graph is still not bipartite. Only the deletion of $02$ removes the last odd cycle. A structure must therefore know whether *some* odd cycle survives, not only whether the deleted edge was on one.

## Known algorithms

**A spanning forest with parity.** Keep a spanning forest $F$ of $G$, and for each vertex the parity of its depth in its tree. A non-tree edge $\{u, v\}$ is *odd* if $u$ and $v$ have the same parity, that is, if the tree path between them has even length, so that the edge closes an odd cycle. The graph is bipartite if and only if no non-tree edge is odd: if no non-tree edge is odd, the parity is a proper 2-coloring; if one is odd, it closes an odd cycle with the tree path. So a counter of odd non-tree edges answers the query. A [link-cut tree](/link-cut-tree/) or an [Euler tour tree](/euler-tour-tree/) gives the parity of a tree path in $O(\log n)$ time.

The hard update is the deletion of a tree edge. A replacement edge reconnects the tree, but it can change the parity of every vertex on one side, and so the oddness of many non-tree edges at once.

**Fully dynamic bounds.**

| algorithm | update time | case | deterministic |
|---|---|---|---|
| recompute with a search after each update | $O(n + m)$ | worst | yes |
| [sparsification](/sparsification/), Eppstein, Galil, Italiano and Nissenzweig (1997) | $O(n^{1/2})$ | worst | yes |
| Henzinger and King (1999) | polylogarithmic | expected amortized | no, Las Vegas |

Holm, de Lichtenberg and Thorup (2001) state that their techniques, through their deterministic [dynamic minimum spanning forest](/dynamic-minimum-spanning-tree/), also give a deterministic algorithm for bipartiteness with polylogarithmic amortized time per update.

## Bounds

**Upper bounds.** Polylogarithmic amortized time per update and $O(1)$ query time; $O(n^{1/2})$ in the deterministic worst case by sparsification.

**Lower bound.** In the [cell-probe model](/cell-probe-model/), the larger of the update and the query time is $\Omega(\log n)$, amortized. The reduction from dynamic connectivity below carries the bound of Pătraşcu and Demaine over.

## Reductions

- **From connectivity.** Subdivide each edge of a connectivity instance: replace $\{u, v\}$ by a path $u, w_{uv}, v$ through a new vertex. The new graph is bipartite, and every path between two original vertices has even length. So for original vertices $u \ne v$, inserting the edge $\{u, v\}$ makes the graph non-bipartite exactly when $u$ and $v$ are connected. A query $\mathrm{connected}(u, v)$ becomes insert, ask, delete: three operations. So dynamic bipartiteness is at least as hard as dynamic connectivity.
- **To connectivity in the double cover.** The bipartite double cover has two copies $v_0, v_1$ of each vertex and the edges $\{u_0, v_1\}$ and $\{u_1, v_0\}$ for each edge $\{u, v\}$. A component of $G$ is bipartite if and only if, for a vertex $v$ in it, $v_0$ and $v_1$ are in different components of the cover. Each update of $G$ is two updates of the cover. This answers the query $\mathrm{bipartite}(v)$ for one component with a connectivity structure; the global question needs a count over components.

## Applications

- **Two-coloring constraints.** Systems of constraints of the form "$x$ and $y$ differ", such as the assignment of two frequencies, two shifts or two sides, are bipartiteness instances, and a dynamic structure keeps their feasibility as constraints come and go.
- **Parity constraints.** Constraints "$x \oplus y = b$" over bits are the weighted form, solved with the same parity structures.
- **Two colors.** Keeping a proper [coloring](/dynamic-graph-coloring/) with two colors is possible exactly while the graph stays bipartite, so this problem decides when such a coloring exists.

## References
