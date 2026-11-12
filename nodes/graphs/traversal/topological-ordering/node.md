---
tag: V34M1Z
kind: problem
slug: topological-ordering
name: Topological ordering
aliases:
- topological sort problem
- linear ordering of a DAG
area: graphs/traversal
level: intro
summary: Order the vertices of a directed acyclic graph so that every edge goes forward.
prereqs: [directed-acyclic-graph]
see_also: [topological-ordering-theorem, topological-sort, kahns-algorithm, depth-first-orders, cycle-detection, counting-linear-extensions, dynamic-topological-order, dag-shortest-paths]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4, Topological sort
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3, Linked allocation (topological sorting, Algorithm T)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.6, Directed acyclic graphs and topological ordering
  - paper: doi:10.1145/368996.369025
    title: Arthur B. Kahn, Topological sorting of large networks, Communications of the ACM 5(11), 558 to 562 (1962)
    locator: the whole paper
  - paper: doi:10.1007/BF00383444
    title: Graham Brightwell and Peter Winkler, Counting linear extensions, Order 8(3), 225 to 242 (1991)
    locator: "the proof that counting linear extensions is #P-complete"
  - paper: doi:10.1016/0020-0190(74)90001-5
    title: Donald E. Knuth and Jayme L. Szwarcfiter, A structured program to generate all topological sorting arrangements, Information Processing Letters 2(6), 153 to 157 (1974)
    locator: the whole paper
---

The topological ordering problem takes a [directed graph](/directed-graph/) and asks for a list of all its vertices in which each edge goes from an earlier vertex to a later one, or for a proof that no such list exists. A list of this kind exists exactly when the graph is a [directed acyclic graph](/directed-acyclic-graph/), by the [topological ordering theorem](/topological-ordering-theorem/), so an algorithm for the problem also decides whether a directed graph has a cycle. Two classical algorithms solve it in $\Theta(n + m)$ time: the [DFS topological sort](/topological-sort/), which lists the vertices in decreasing order of finish time, and [Kahn's algorithm](/kahns-algorithm/), which removes vertices without incoming edges one at a time. The order is the first step of many algorithms on acyclic graphs, such as [shortest paths in a DAG](/dag-shortest-paths/) and [dynamic programming over a DAG](/dag-dynamic-programming/).

## In plain words

You have a set of jobs, and some rules of the form "this job must be done before that job". You want to put all the jobs in one line so that every rule is kept.

Sometimes this is impossible. If job A must come before B, B before C, and C before A, no line works, because the rules go round in a loop. The problem asks for a valid line, or for a loop of rules that shows that there is none.

When a valid line exists, there are usually many of them. Any one of them is a correct answer.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges, given by [adjacency lists](/adjacency-list/).

**Output.** A *topological ordering* of $G$: a list $v_1, v_2, \ldots, v_n$ of all the vertices, each one time, such that for each edge $(v_i, v_j) \in E$ we have $i < j$. Equivalently, a bijection $\sigma : V \to \{1, \ldots, n\}$ with $\sigma(u) < \sigma(v)$ for each edge $(u, v)$. If $G$ has no topological ordering, the output is a report of this fact, and a strong form of the problem asks for a directed cycle of $G$ as a certificate.

A self-loop $(u, u)$ makes the problem infeasible, because it would need $\sigma(u) < \sigma(u)$. More generally, a directed cycle $u_1, \ldots, u_k, u_1$ would need $\sigma(u_1) < \sigma(u_2) < \cdots < \sigma(u_k) < \sigma(u_1)$. The [topological ordering theorem](/topological-ordering-theorem/) proves that the converse also holds: each acyclic graph has a topological ordering.

In the language of orders, a topological ordering of an acyclic graph is a *linear extension* of the reachability relation, the partial order in which $u \le v$ when $v$ is reachable from $u$: it is a [total order](/total-order/) that agrees with each comparison of the partial order.

## Variants

- **Decision version.** Decide whether $G$ has a topological ordering. This is the problem of [cycle detection](/cycle-detection/) in directed graphs.
- **With a cycle as certificate.** Return either an ordering or a directed cycle. The DFS method gives the cycle from a back edge $(u, v)$: the tree path from $v$ to $u$ and the edge itself. Kahn's method gives it from the vertices that remain: each has an incoming edge from another remaining vertex, so following such edges backwards must repeat a vertex.
- **Lexicographically smallest ordering.** Among all orderings, find the one that is smallest when compared as sequences of vertex numbers. Kahn's algorithm with a min-[priority queue](/priority-queue/) in place of the queue does this in $O(m + n \log n)$ time: at each step, every valid ordering must take some vertex of in-degree zero next, and the smallest such vertex keeps the most options for a smaller sequence.
- **Counting.** Count the topological orderings. This is the problem of [counting linear extensions](/counting-linear-extensions/), which Brightwell and Winkler proved to be #P-complete.
- **Enumeration.** List all topological orderings. Knuth and Szwarcfiter gave a backtracking program for this.
- **Dynamic.** Keep an ordering while edges are inserted, and report the first insertion that creates a cycle. See [dynamic topological order](/dynamic-topological-order/) and [incremental topological ordering](/incremental-topological-ordering/).

## Examples

**A small DAG.** Take the vertices 0 to 6 and the edges $0 \to 1$, $0 \to 3$, $0 \to 2$, $1 \to 2$, $3 \to 2$, $3 \to 4$, $5 \to 4$ and $5 \to 6$. Some topological orderings are:

| method | ordering |
|---|---|
| DFS, roots in the order 0 to 6, lists in the order of the edges above | 5, 6, 0, 3, 4, 1, 2 |
| lexicographically smallest | 0, 1, 3, 2, 5, 4, 6 |

The list $0, 1, 2, 3, 4, 5, 6$ is not one, because the edge $3 \to 2$ goes backwards. A check by enumeration of all $7! = 5040$ lists finds exactly 91 topological orderings of this graph.

**A cycle.** On the graph with the edges $0 \to 1$, $1 \to 2$ and $2 \to 0$, there is no topological ordering. Each vertex has an incoming edge, so no vertex can be first.

**A path.** On the path $0 \to 1 \to \cdots \to n-1$, the only topological ordering is $0, 1, \ldots, n-1$. On a graph with no edges, each of the $n!$ lists is one.

## Known algorithms

| algorithm | time | extra space | idea |
|---|---|---|---|
| [DFS topological sort](/topological-sort/) | $\Theta(n + m)$ | $\Theta(n)$ | decreasing order of DFS finish times, the reverse postorder |
| [Kahn's algorithm](/kahns-algorithm/) | $\Theta(n + m)$ | $\Theta(n)$ | output a vertex of in-degree zero, remove it, repeat |
| Kahn's algorithm with a min-[binary heap](/binary-heap/) | $O(m + n \log n)$ | $\Theta(n)$ | the lexicographically smallest ordering |
| transitive closure, then sort by the number of ancestors | the cost of the closure | $\Theta(n^2)$ | if $(u, v)$ is an edge, each ancestor of $u$ is an ancestor of $v$, and $u$ is an ancestor of $v$ but not of itself |

Knuth's Algorithm T is Kahn's method with linked lists of successors and a count of predecessors for each vertex. Both linear-time methods are described on their own pages with full proofs.

## Bounds

**Lower bound.** Each algorithm that is correct on all inputs must read all $n$ adjacency lists and, in the worst case, all $m$ entries, so it needs $\Omega(n + m)$ time. Assume that on some input it outputs an ordering without reading the entry $v$ in the list of $u$. Change that entry to $u$, which makes a self-loop. The algorithm reads the same values as before, so it gives the same output, but the new graph has a cycle and no ordering. If the algorithm never looks at the list of some vertex at all, the same change to an entry of that list works when the list is not empty, and adding a self-loop there works when it is. So the linear-time algorithms are optimal.

**Space.** Both linear-time algorithms need $\Theta(n)$ words besides the input, for the marks or the in-degree counts and the output.

**Parallel.** Through the transitive closure, which can be computed with $O(\log n)$ Boolean matrix products, topological ordering is in the class NC.

## Reductions

- **From cycle detection.** Run a topological ordering algorithm. The graph is acyclic exactly when it returns an ordering. Both linear-time algorithms also give a cycle when there is one.
- **To checking.** Given a list, check in $O(n + m)$ time that it is a topological ordering: compute the position of each vertex, then test each edge. So the problem is easy to verify, and the decision version is in P.
- **Linear extensions.** A finite partial order on $n$ elements, given as a directed graph of its comparisons or of its covering pairs, has the same linear extensions as that graph has topological orderings. Counting them is the #P-complete problem of [counting linear extensions](/counting-linear-extensions/).
- **Strong components.** For a general directed graph, contract each [strongly connected component](/strongly-connected-components/) to one vertex. The result, the [condensation graph](/condensation-graph/), is acyclic and has a topological ordering. Tarjan's algorithm outputs the components in reverse topological order of the condensation.

## Applications

- **Scheduling with precedence.** Jobs with "before" rules, courses with prerequisites, and build steps of a program with dependencies are done in a topological ordering of their rule graph.
- **Shortest and longest paths in a DAG.** [DAG shortest paths](/dag-shortest-paths/) and [DAG longest paths](/dag-longest-path/) relax the edges in topological order in $\Theta(n + m)$ time, with negative weights allowed. The [critical path](/critical-path/) of a project is a longest path of this kind.
- **Dynamic programming.** A recurrence whose subproblems depend on each other without a cycle is evaluated in a topological ordering of its dependency graph, as in [DAG dynamic programming](/dag-dynamic-programming/) and [tabulation](/tabulation/).
- **Evaluation of circuits and formulas.** Each gate is computed after its inputs, which is a topological ordering of the circuit. Spreadsheets recompute cells in the same way.
- **Strong components.** The [Kosaraju-Sharir](/kosaraju-sharir/) algorithm uses the reverse postorder: if each component is placed at the position of its first vertex in that list, the components come in a topological ordering of the condensation.

## References
