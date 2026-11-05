---
tag: WCWHRH
kind: definition
slug: incremental-graph
name: Incremental graph
aliases:
- insertions-only graph
- incremental model
area: graphs/dynamic-graphs
level: intro
summary: Only edge insertions are allowed.
prereqs: [dynamic-graph]
see_also: [decremental-graph, fully-dynamic-graph, incremental-connectivity, incremental-topological-ordering, online-bridge-finding, offline-dynamic-graph, disjoint-set-forest]
sources:
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 215 to 225 (1975)
    locator: the whole paper (the inverse Ackermann bound for set union, which solves incremental connectivity)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Data Structures for Disjoint Sets (Section 19.1 uses them for the connected components of a graph that gains edges)
  - paper: "Bernhard Haeupler, Telikepalli Kavitha, Rogers Mathew, Siddhartha Sen and Robert E. Tarjan, Incremental cycle detection, topological ordering, and strong component maintenance, ACM Transactions on Algorithms 8(1), article 3 (2012)"
    locator: Section 1 (the incremental model for directed graphs and the earlier bounds)
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 (partially dynamic problems, insertions only)
---

An incremental graph is a [dynamic graph](/dynamic-graph/) in which every update inserts an [edge](/edge/) (or, in weighted problems, lowers an edge weight), and no update ever removes anything. Its properties change in one direction only: components merge, reachable sets grow and distances shrink. It is the mirror image of a [decremental graph](/decremental-graph/), and together the two form the partially dynamic setting. Many incremental problems have very fast algorithms, the best known being incremental connectivity with a [disjoint-set forest](/disjoint-set-forest/).

## Definition

An **incremental graph** is a dynamic graph $G_0, G_1, \ldots, G_t$ on a fixed vertex set $V$, with $n = |V|$, in which each update is $\mathrm{insert}(e)$ for an edge $e \notin E_{i-1}$, so that

$$E_0 \subseteq E_1 \subseteq \cdots \subseteq E_t, \qquad |E_i \setminus E_{i-1}| = 1.$$

So a simple graph has $t \le \binom{n}{2} - |E_0|$ updates, and a directed simple graph has $t \le n(n-1) - |E_0|$. Usually $G_0$ has no edges, and $m$ denotes the number of edges at the end. In a weighted graph, the incremental model often also allows an update that lowers the weight of an edge, because an insertion is the same as lowering a weight from $\infty$. Some problems also allow the insertion of a new isolated vertex.

**Monotonicity.** If $G$ is a subgraph of $H$ on the same vertices, each path of $G$ is a path of $H$. Applied to $G_{i-1} \subseteq G_i$, for all $u, v \in V$:

- $\mathrm{dist}_{G_i}(u, v) \le \mathrm{dist}_{G_{i-1}}(u, v)$,
- if $v$ is reachable from $u$ in $G_{i-1}$, it is reachable in $G_i$,
- each [connected component](/connected-components/) of $G_{i-1}$ lies inside one component of $G_i$, so the number of components never grows,
- if $G_{i-1}$ has a cycle, so has $G_i$; an acyclic graph can become cyclic but never the reverse.

A quantity that only moves one way and has few possible values can change only a few times. The number of components starts at most at $n$ and drops by one at each merge, so at most $n - 1$ insertions merge components. An unweighted distance $\mathrm{dist}(s, v)$ takes one of the values $\infty, n-1, \ldots, 1, 0$ and so drops at most $n$ times. Such counts bound the total work of incremental algorithms.

## Examples and non-examples

**Example: components merge, distances drop.** Take $V = \{0, \ldots, 5\}$, no edges at the start, and insert $01, 34, 12, 23, 45, 03, 15$ in this order. The table gives the [breadth-first search](/breadth-first-search/) distances from 0 and the number of components after each insertion.

| inserted | distances from 0 to 0, 1, 2, 3, 4, 5 | components |
|---|---|---|
| 01 | 0, 1, $\infty$, $\infty$, $\infty$, $\infty$ | 5 |
| 34 | 0, 1, $\infty$, $\infty$, $\infty$, $\infty$ | 4 |
| 12 | 0, 1, 2, $\infty$, $\infty$, $\infty$ | 3 |
| 23 | 0, 1, 2, 3, 4, $\infty$ | 2 |
| 45 | 0, 1, 2, 3, 4, 5 | 1 |
| 03 | 0, 1, 2, 1, 2, 3 | 1 |
| 15 | 0, 1, 2, 1, 2, 2 | 1 |

Each distance column only goes down, and the component count only goes down. The first five insertions each merge two components; the last two close cycles and change no component.

**Example: incremental connectivity.** Each insertion is a union and each query is a pair of finds in a [disjoint-set forest](/disjoint-set-forest/). With union by rank and path compression, $m$ operations on $n$ vertices take $O(m\,\alpha(n))$ time in total, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/) (Tarjan, 1975). This bound is amortized; see [incremental connectivity](/incremental-connectivity/). [Kruskal's algorithm](/kruskal/) runs exactly this problem on the edges sorted by weight.

**Example: incremental problems on directed graphs.** Inserting arcs into a [directed acyclic graph](/directed-acyclic-graph/) can create a cycle. The [incremental topological ordering](/incremental-topological-ordering/) problem keeps a topological order and reports the first arc that closes a cycle. Incremental [reachability](/reachability/) and transitive closure are also classic incremental problems.

**Example: incremental bridges.** Inserting an edge can only turn [bridges](/bridge/) into non-bridges, because a new edge adds cycles and removes none. [Online bridge finding](/online-bridge-finding/) keeps the bridges under insertions in nearly linear total time.

**Non-example: a weight increase.** Raising the weight of an edge can make a distance longer. A sequence with an increase is not incremental for shortest paths, even if it has no deletion.

**Non-example: insert, delete, insert.** As soon as one deletion is allowed, the sequence is [fully dynamic](/fully-dynamic-graph/), and the counting bounds above fail: a distance can go down and up again without limit.

**Non-example: a disjoint-set forest with undo.** Undoing a union in stack order is a deletion of the most recent edge. The structure that allows it, [union-find with rollback](/union-find-with-rollback/), serves the [offline](/offline-dynamic-graph/) setting and not the incremental one, and it gives up path compression to do so.

## Related definitions

- **[Decremental graph](/decremental-graph/).** Only deletions. A decremental sequence read backwards is incremental, so when the whole sequence is known in advance, a decremental problem can be solved by an incremental algorithm on the reversed sequence.
- **[Fully dynamic graph](/fully-dynamic-graph/).** Both insertions and deletions. Fully dynamic connectivity needs $\Omega(\log n)$ amortized time per operation in the cell-probe model, while incremental connectivity takes $O(\alpha(n))$, so the two classes differ in difficulty.
- **[Offline dynamic graph](/offline-dynamic-graph/).** The sequence is known in advance. The incremental model is online by default: an answer must be given before the next insertion is known.
- **[Amortized update time](/amortized-update-time/).** Incremental bounds are usually amortized or total bounds, because the monotone counts above bound the total, not each insertion.
- **[Incremental connectivity](/incremental-connectivity/)**, **[incremental topological ordering](/incremental-topological-ordering/)** and **[online bridge finding](/online-bridge-finding/)** are the main incremental problems and algorithms of this area.

## References
