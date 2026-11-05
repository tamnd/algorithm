---
tag: Z66J6K
kind: problem
slug: incremental-connectivity
name: Incremental connectivity
aliases:
- union-only connectivity
- incremental connected components
area: graphs/dynamic-graphs
level: core
summary: Maintain connected components under edge insertions only.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of operations, α: the inverse Ackermann function}
  time: {amortized: Θ(α(n))}
prereqs: [incremental-graph, connected-components, disjoint-set]
see_also: [disjoint-set-forest, union-find-connectivity, dynamic-equivalence-problem, union-find-lower-bound, blum-union-find, dynamic-connectivity, decremental-connectivity, online-bridge-finding]
sources:
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 215 to 225 (1975)
    locator: the whole paper (the upper bound with the inverse Ackermann function for union by rank with path compression)
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345 to 354
    locator: Theorem 5 (the amortized lower bound for union-find) and Theorem 6 (the worst-case lower bound per operation)
  - paper: "Norbert Blum, On the single-operation worst-case time complexity of the disjoint set union problem, SIAM Journal on Computing 15(4), 1021 to 1024 (1986)"
    locator: the whole paper (O(log n / log log n) worst-case time per operation)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.1 (the procedures CONNECTED-COMPONENTS and SAME-COMPONENT) and Sections 19.3 and 19.4 (disjoint-set forests and their analysis)
---

Incremental connectivity is the problem of answering "are $u$ and $v$ in the same [connected component](/connected-components/)?" in an undirected graph that gains edges over time and never loses them. It is the [incremental](/incremental-graph/) special case of [dynamic connectivity](/dynamic-connectivity/), and it is the same problem as [union-find](/dynamic-equivalence-problem/): an edge insertion is a union of two sets and a query is a comparison of two finds. A [disjoint-set forest](/disjoint-set-forest/) with union by rank and path compression solves it in $O(\alpha(n))$ amortized time per operation, and Fredman and Saks proved that no structure can do better in the cell-probe model.

## In plain words

You have a set of points and you draw lines between them, one at a time. You never erase a line. Between drawings, someone asks: can you walk from this point to that point along the lines?

Each group of points that can reach each other is one component. A new line either joins two groups into one, or falls inside one group and changes nothing. So the whole job is to keep a list of groups that only ever merge. The classic tool for this is union-find, which keeps a leader for each group and answers each question in almost constant time.

## Definition

The vertex set $V$ has $n$ vertices, and the graph starts with no edges. The input is an online sequence of operations:

- $\mathrm{insert}(u, v)$: add the undirected edge $\{u, v\}$ to the graph,
- $\mathrm{connected}(u, v)$: return true if and only if $u$ and $v$ are in the same connected component of the current graph.

Each answer must be given before the next operation is read. Let $G_i$ be the graph after the first $i$ insertions, and let $\sim_i$ be the relation "connected in $G_i$". Then $\sim_i$ is an equivalence relation on $V$, and

$$\sim_i \;=\; \text{the smallest equivalence relation that contains } \sim_{i-1} \text{ and the pair } (u_i, v_i).$$

So an insertion either merges the two classes of $u_i$ and $v_i$ or, if they are already one class, leaves $\sim$ unchanged. The cost is the total time of the sequence, or the amortized or worst-case time per operation, in the [word RAM](/word-ram/) or the cell-probe model.

## Variants

- **Count the components.** Keep the number of classes: start at $n$ and subtract one at each insertion that merges. A query then takes $O(1)$ time.
- **Component sizes or other aggregates.** Keep a size, a sum or a minimum at each root of a disjoint-set forest, combined at each merge.
- **With isolated vertex insertions.** New vertices arrive as singletons; a disjoint-set forest handles this with make-set.
- **Spanning forest.** Report whether each inserted edge merged two components. The merging edges form a [spanning forest](/spanning-forest/) of the final graph, as in [Kruskal's algorithm](/kruskal/).
- **Incremental minimum spanning forest.** With weights, a new edge that closes a cycle replaces the heaviest edge on that cycle if it is lighter. A [link-cut tree](/link-cut-tree/) finds the heaviest edge of a tree path in $O(\log n)$ amortized time.
- **Incremental 2-edge connectivity and bridges.** Keep the [bridges](/bridge/) under insertions; see [online bridge finding](/online-bridge-finding/).
- **Directed graphs.** Incremental reachability and incremental [strongly connected components](/strongly-connected-components/) are much harder; see [dynamic reachability](/dynamic-reachability/) and [incremental topological ordering](/incremental-topological-ordering/).
- **Decremental and fully dynamic.** With deletions the problem becomes [decremental connectivity](/decremental-connectivity/) or [dynamic connectivity](/dynamic-connectivity/).

## Examples

Take $V = \{0, 1, \ldots, 6\}$. The table shows each operation, its answer and the number of components after it.

| operation | answer | components |
|---|---|---|
| insert(0, 1) | merge | 6 |
| insert(2, 3) | merge | 5 |
| connected(0, 3) | false | 5 |
| insert(1, 2) | merge | 4 |
| connected(0, 3) | true | 4 |
| insert(4, 5) | merge | 3 |
| insert(3, 0) | same component | 3 |
| connected(5, 6) | false | 3 |
| insert(5, 6) | merge | 2 |
| connected(4, 6) | true | 2 |
| insert(6, 1) | merge | 1 |
| connected(0, 4) | true | 1 |

The insertion of $\{3, 0\}$ closes the cycle $0, 1, 2, 3$ and changes no component. The six merging insertions are a spanning tree of the final graph, as they must be, since $7 - 1 = 6$.

## Known algorithms

| algorithm | insert | connected | case |
|---|---|---|---|
| graph search per query ([BFS](/breadth-first-search/) or [DFS](/depth-first-search/)) | $O(1)$ | $O(n + m)$ | worst |
| labels with relabeling of the smaller component | $O(\log n)$ | $O(1)$ | amortized, $O(n)$ worst |
| [disjoint-set forest](/disjoint-set-forest/), [union by size](/union-by-size/) only | $O(\log n)$ | $O(\log n)$ | worst |
| disjoint-set forest, union by rank and path compression | $O(\alpha(n))$ | $O(\alpha(n))$ | amortized |
| [Blum's structure](/blum-union-find/) | $O(\log n / \log\log n)$ | $O(\log n / \log\log n)$ | worst |

The relabeling method stores a label for each vertex and a member list for each component, and on a merge moves the members of the smaller component. A vertex changes its label only when its component at least doubles, so each vertex moves at most $\lfloor \lg n \rfloor$ times. The union-find analysis is on the [union-find connectivity](/union-find-connectivity/) page and in Tarjan (1975).

## Bounds

- **Upper bound.** Union by rank with path compression does $m$ operations on $n$ vertices in $O(m\,\alpha(m, n))$ time in total (Tarjan, 1975), so $O(\alpha(n))$ amortized per operation when $m \ge n$.
- **Amortized lower bound.** Fredman and Saks (1989) proved that every structure in the cell-probe model with words of $O(\log n)$ size needs $\Omega(m\,\alpha(m, n))$ time for some sequence of $n - 1$ unions and $m$ finds. Tarjan (1979) had proved the same bound earlier for a restricted class of pointer machine algorithms. So the disjoint-set forest is optimal; see the [union-find lower bound](/union-find-lower-bound/).
- **Worst case per operation.** Blum (1986) gave $O(\log n / \log\log n)$ worst-case time per operation, and Fredman and Saks proved this is optimal in the cell-probe model.
- **Linear time in special cases.** If the set of possible unions is known in advance as a tree, Gabow and Tarjan's [static tree set union](/static-tree-set-union/) runs in linear total time on the word RAM.
- **Against fully dynamic connectivity.** Fully dynamic connectivity needs $\Omega(\log n)$ amortized time per operation (Pătraşcu and Demaine, 2006), so allowing deletions makes the problem strictly harder; see the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/).

## Reductions

- **To and from union-find.** Map $\mathrm{insert}(u, v)$ to $\mathrm{union}(u, v)$ and $\mathrm{connected}(u, v)$ to $\mathrm{find}(u) = \mathrm{find}(v)$. In the other direction, map $\mathrm{union}(a, b)$ to $\mathrm{insert}(a, b)$ and a same-set query to $\mathrm{connected}$. Both maps cost $O(1)$ per operation, so the two problems have the same complexity. This is the [dynamic equivalence problem](/dynamic-equivalence-problem/).
- **Offline decremental connectivity.** If all deletions are known in advance, reverse the sequence: the deletions become insertions, and the problem becomes incremental connectivity, answered in $O(\alpha(n))$ amortized time per operation.
- **Offline fully dynamic connectivity.** With deletions known in advance, [offline dynamic connectivity](/offline-dynamic-connectivity/) uses an incremental structure that can undo its last insertions, [union-find with rollback](/union-find-with-rollback/).

## Applications

- **[Kruskal's algorithm](/kruskal/)** asks, for each edge in order of weight, whether its ends are already connected, and inserts it if not.
- **Connected component labeling** of images joins neighboring pixels of the same color, often in one pass with union-find.
- **Percolation** experiments open random sites of a grid and ask when the top and the bottom first connect.
- **Unification and type inference** merge classes of equal terms and ask whether two terms are known to be equal.
- **Network monitoring** where links are only added, for example while a network is being built.

## References
