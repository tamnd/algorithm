---
tag: J4YHBT
kind: problem
slug: dynamic-topological-order
name: Dynamic topological order
aliases:
- incremental topological ordering
- online cycle detection
- dynamic topological sort
area: graphs/dynamic-graphs
level: advanced
summary: Maintain a topological order of a DAG under edge insertions, detecting when a cycle forms.
prereqs: [dynamic-graph, directed-acyclic-graph, topological-sort, cycle-detection]
see_also: [incremental-topological-ordering, dynamic-reachability, strongly-connected-components, dynamic-transitive-closure, incremental-graph]
sources:
  - paper: doi:10.1016/0020-0190(96)00075-0
    title: Alberto Marchetti-Spaccamela, Umberto Nanni and Hans Rohnert, Maintaining a topological order under edge insertions, Information Processing Letters 59(1), 53 to 58 (1996)
    locator: the whole paper (O(mn) total time)
  - paper: doi:10.1145/1187436.1210590
    title: David J. Pearce and Paul H. J. Kelly, A dynamic topological sort algorithm for directed acyclic graphs, ACM Journal of Experimental Algorithmics 11 (2007)
    locator: the algorithm that searches only the affected region and reorders it
  - paper: doi:10.1145/2071379.2071382
    title: Bernhard Haeupler, Telikepalli Kavitha, Rogers Mathew, Siddhartha Sen and Robert E. Tarjan, Incremental cycle detection, topological ordering, and strong component maintenance, ACM Transactions on Algorithms 8(1), 1 to 33 (2012)
    locator: the two-way search algorithm (O(m^(3/2)) total time) and the extension to strong components
  - paper: doi:10.1145/2756553
    title: Michael A. Bender, Jeremy T. Fineman, Seth Gilbert and Robert E. Tarjan, A new approach to incremental cycle detection and related problems, ACM Transactions on Algorithms 12(2), 1 to 22 (2016)
    locator: the main theorems (O(m min(m^(1/2), n^(2/3))) and O(n^2 log n) total time)
  - paper: doi:10.1137/1.9781611975031.2
    title: Aaron Bernstein and Shiri Chechik, Incremental topological sort and cycle detection in O(m n^(1/2)) expected total time, Proceedings of SODA 2018, 21 to 34
    locator: the main theorem (randomized, expected total time)
---

The dynamic topological order problem asks to keep a [topological order](/topological-sort/) of a [directed acyclic graph](/directed-acyclic-graph/) while edges are inserted, and to report the first insertion that closes a cycle. A deletion never makes a valid order invalid, so the problem is in effect incremental, and its cost is measured as the total time over a sequence of $m$ insertions. Recomputing the order after each insertion costs $O(m^2)$ in total; the best algorithms do much better by searching only the part of the order between the two ends of the new edge.

## In plain words

A list of tasks must be done in an order that respects rules of the form "do this before that". New rules arrive one at a time. If a new rule already agrees with the list, nothing changes. If it does not, some tasks must move.

The tasks that must move are only those between the two tasks of the new rule: the ones that the later task must come after, and the ones that must come after the earlier task. A good program finds these two groups, swaps their places, and leaves every other task where it is. If the two groups meet, the new rule closes a circle of rules, and no valid order exists.

## Definition

**Input.** A number $n$ of vertices and an online sequence of edge insertions $\mathrm{insert}(u, v)$ into a directed graph $G = (V, E)$ that starts with no edges.

**Output.** After each insertion that keeps $G$ acyclic, a bijection $\mathrm{ord} : V \to \{1, \ldots, n\}$ such that $\mathrm{ord}(x) < \mathrm{ord}(y)$ for every edge $(x, y) \in E$, and a query $\mathrm{before}(x, y)$ that compares $\mathrm{ord}(x)$ and $\mathrm{ord}(y)$. At the first insertion that creates a cycle, the output is "cycle", and the problem usually stops there, or the edge is rejected.

**Cost.** The total time over all insertions, as a function of $n$ and the final number of edges $m$. Some algorithms keep $\mathrm{ord}$ as explicit numbers, and others keep only an order data structure that answers $\mathrm{before}$.

**Deletions.** If $\mathrm{ord}$ is a topological order of $G$, it is also one of $G - e$ for any edge $e$. So a fully dynamic structure can ignore deletions, except that a rejected edge may become legal after a deletion.

## Variants

- **Incremental cycle detection.** Report only whether the graph has a cycle, with no order as output.
- **Strong components.** Allow cycles, and keep the [strongly connected components](/strongly-connected-components/) and a topological order of the condensation; an insertion that closes a cycle merges the components on it.
- **Explicit or implicit order.** Keep $\mathrm{ord}$ as integers, or as a list with an order-maintenance structure.
- **Offline.** All insertions known in advance; one topological sort of the final graph, if it is acyclic, is valid for every prefix.

## Examples

Take $V = \{0, \ldots, 5\}$ with the initial order $0, 1, 2, 3, 4, 5$. An insertion of $(u, v)$ with $\mathrm{ord}(u) > \mathrm{ord}(v)$ searches forward from $v$ and backward from $u$, both only within the positions from $\mathrm{ord}(v)$ to $\mathrm{ord}(u)$. Then it places the backward set before the forward set in the positions that the two sets used.

| insert | action | order after it |
|---|---|---|
| 3→4 | already in order | 0, 1, 2, 3, 4, 5 |
| 4→5 | already in order | 0, 1, 2, 3, 4, 5 |
| 5→1 | backward set 3, 4, 5, forward set 1 | 0, 3, 2, 4, 5, 1 |
| 1→2 | backward set 4, 5, 1, forward set 2 | 0, 3, 4, 5, 1, 2 |
| 2→0 | backward set 3, 4, 5, 1, 2, forward set 0 | 3, 4, 5, 1, 2, 0 |
| 0→3 | forward search from 3 reaches 0 | cycle, edge rejected |
| 4→2 | already in order | 3, 4, 5, 1, 2, 0 |
| 2→5 | forward search from 5 reaches 2 | cycle, edge rejected |

At the third insertion, vertex 2 lies between 1 and 5 in the order but is not connected to either, so it keeps its position. The insertion $0 \to 3$ would close the cycle $0, 3, 4, 5, 1, 2, 0$.

## Known algorithms

**Local search.** The step in the example is the core of most algorithms. Let $F$ be the vertices reachable from $v$ with $\mathrm{ord} \le \mathrm{ord}(u)$, and $B$ the vertices that reach $u$ with $\mathrm{ord} \ge \mathrm{ord}(v)$. If $u \in F$, the new edge closes a cycle. Otherwise $F$ and $B$ are disjoint, and moving all of $B$ before all of $F$, each in its old relative order, gives a valid order: every edge between the two sets now goes from $B$ to $F$ or did not exist, and edges to vertices outside $F \cup B$ keep their direction, because the moved vertices stay inside the window. Pearce and Kelly (2007) give a version of this that is fast in practice.

| algorithm | total time | case | deterministic |
|---|---|---|---|
| recompute after each insertion | $O(m^2)$ | worst | yes |
| Marchetti-Spaccamela, Nanni and Rohnert (1996) | $O(mn)$ | worst | yes |
| Haeupler, Kavitha, Mathew, Sen and Tarjan (2012), two-way search | $O(m^{3/2})$ | worst | yes |
| Bender, Fineman, Gilbert and Tarjan (2016), sparse | $O(m \min(m^{1/2}, n^{2/3}))$ | worst | yes |
| Bender, Fineman, Gilbert and Tarjan (2016), dense | $O(n^2 \log n)$ | worst | yes |
| Bernstein and Chechik (2018) | $\tilde O(m n^{1/2})$ | expected | no |

All bounds are totals over the whole sequence, so they are amortized per insertion; the time of a single insertion can be large. **Two-way search** runs the forward and the backward searches in turns, one edge each, and stops as soon as it has found enough of both sets to fix the order. A charging argument over pairs of related edges gives the $O(m^{3/2})$ bound. **Bender, Fineman, Gilbert and Tarjan** keep for each vertex a level that approximates the number of its ancestors, and search only within one level when possible. Later randomized algorithms improved the bound further for sparse graphs.

## Bounds

**Upper bounds.** As in the table. For sparse graphs, the deterministic bound is $O(m^{3/2})$ total.

**Lower bounds.** Each insertion must at least be read, so $\Omega(m)$ total time is necessary. Haeupler, Kavitha, Mathew, Sen and Tarjan show that a natural class of algorithms, which move vertices only in the way of the local search, must move many vertices on some sequences. No strong lower bound is known for general algorithms.

## Reductions

- **To reachability.** An insertion $(u, v)$ closes a cycle exactly when $u$ is reachable from $v$ before it, so incremental [dynamic reachability](/dynamic-reachability/) for single pairs answers cycle detection. With a [transitive closure](/dynamic-transitive-closure/) structure, each insertion costs a query.
- **Strong components.** An algorithm for topological order with cycle detection extends to strong components by contracting each new cycle into a single vertex, as Haeupler, Kavitha, Mathew, Sen and Tarjan show.

## Applications

- **Incremental compilation and build systems.** Dependencies between modules arrive as code changes; the build order must stay valid, and a dependency cycle is an error.
- **Spreadsheets.** A new formula adds dependency edges, and the evaluation order must be updated; a circular reference is a cycle.
- **Deadlock detection.** In a lock-order graph or a wait-for graph, a cycle means a possible deadlock.
- **Pointer analysis.** Constraint graphs grow during the analysis, and cycles are collapsed for speed.

## References
