---
tag: YJVCAJ
kind: definition
slug: directed-acyclic-graph
name: Directed acyclic graph
area: graphs/graph-representation
level: intro
summary: Directed graph with no cycles, the structure that admits topological ordering and underlies dependency scheduling and dynamic programming.
prereqs: [directed-graph, acyclic-graph]
see_also: [topological-sort, dag-source-lemma, topological-ordering-theorem, kahns-algorithm, dag-shortest-paths, dag-longest-path, condensation-graph, transitive-reduction]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4 (Topological sort), the definition of a dag and the lemma that a directed graph is acyclic if and only if depth-first search yields no back edges; Section 22.2 (Single-source shortest paths in directed acyclic graphs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3, Section 3.6 (Directed acyclic graphs and topological ordering), the statements that a DAG has a node with no incoming edges and that G has a topological ordering if and only if it is a DAG
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.3.2 (Directed acyclic graphs), and Section 6.1 (Shortest paths in dags, revisited), where dynamic programming is described as a walk on a dag
  - paper: "Robert W. Robinson, Counting labeled acyclic digraphs, in New Directions in the Theory of Graphs, F. Harary (editor), Academic Press, 1973"
    locator: pages 239 to 273, the recurrence for the number of labelled DAGs
---

A directed acyclic graph, or DAG, is a [directed graph](/directed-graph/) with no directed cycle. Its vertices can be put in a [topological order](/topological-sort/), an order in which each edge goes forward, and a finite directed graph has such an order exactly when it is a DAG. DAGs model dependencies: tasks that must run before other tasks, cells of a spreadsheet, the commits of a version history and the subproblems of a dynamic program. Many problems that are hard on general graphs, such as the [longest path](/dag-longest-path/), take linear time on a DAG.

## Definition

A **directed acyclic graph** is a finite directed graph $G = (V, E)$, $E \subseteq V \times V$, that has no directed cycle. Here a directed cycle is a sequence $v_0, \ldots, v_{k-1}$ of $k \ge 1$ distinct vertices with $(v_i, v_{i+1}) \in E$ for $0 \le i \le k - 2$ and $(v_{k-1}, v_0) \in E$. So a DAG has no self-loop ($k = 1$) and no pair of edges $(u, v), (v, u)$ ($k = 2$).

A *source* is a vertex with in-degree 0 and a *sink* is a vertex with out-degree 0. A **topological order** of $G$ is a bijection $\tau : V \to \{1, \ldots, n\}$ with $\tau(u) < \tau(v)$ for each $(u, v) \in E$.

**Theorem.** A finite directed graph has a topological order if and only if it is a DAG.

*Proof.* If $\tau$ is a topological order and $v_0, \ldots, v_{k-1}$ were a directed cycle, then $\tau(v_0) < \tau(v_1) < \cdots < \tau(v_{k-1}) < \tau(v_0)$, which is impossible. So a graph with a topological order is a DAG.

For the converse, we first show that each DAG with $n \ge 1$ vertices has a source. Start at any vertex $u_0$. While the current vertex $u_i$ has an in-edge $(u_{i+1}, u_i)$, step to $u_{i+1}$. If the walk made $n$ steps, it would visit $n + 1$ vertices, so some vertex twice, say $u_i = u_j$ with $i < j$; then $u_j, u_{j-1}, \ldots, u_i$ follows edges forward and contains a directed cycle. So the walk stops after fewer than $n$ steps, at a vertex with no in-edge. This is the [DAG source lemma](/dag-source-lemma/).

Now induct on $n$. For $n = 0$ the empty map is a topological order. For $n \ge 1$, let $s$ be a source and set $\tau(s) = 1$. The graph $G - s$ is a DAG, because a cycle in it would be a cycle in $G$. By induction it has a topological order $\tau'$ onto $\{1, \ldots, n-1\}$; set $\tau(v) = \tau'(v) + 1$ for $v \ne s$. An edge $(u, v)$ with $u, v \ne s$ goes forward by $\tau'$. An edge $(s, v)$ goes forward because $\tau(s) = 1$. No edge enters $s$. $\blacksquare$

The proof is [Kahn's algorithm](/kahns-algorithm/): remove a source, repeat. CLRS gives a second proof by [depth-first search](/depth-first-search/): a directed graph is acyclic if and only if a DFS finds no back edge, and the vertices in decreasing order of finish time are a topological order.

**The reachability order.** For a DAG, write $u \preceq v$ when $v$ is reachable from $u$. This relation is reflexive and transitive, and it is antisymmetric because $u \preceq v \preceq u$ with $u \ne v$ gives a closed walk and so a cycle. So it is a partial order on $V$, and each topological order is a linear extension of it. Conversely each finite partial order is the reachability order of some DAG, for example of its [transitive reduction](/transitive-reduction/), the Hasse diagram.

**Size.** A DAG on $n$ vertices has at most $\binom{n}{2}$ edges. By a topological order, each edge $(u, v)$ has $\tau(u) < \tau(v)$, so $\{\tau(u), \tau(v)\}$ is a 2-element subset of $\{1, \ldots, n\}$, and different edges give different subsets, since $(u, v)$ and $(v, u)$ cannot both be edges. The graph with all edges $(i, j)$ for $i < j$ has exactly $\binom{n}{2}$ edges, so the bound is tight.

## Examples and non-examples

**A worked example.** A build has the tasks $a$ (fetch), $b$ (configure), $c$ (compile), $d$ (test), $e$ (docs), $f$ (package), with the edges

$$(a, b), (b, c), (c, d), (b, e), (d, f), (e, f).$$

| vertex | in-degree | out-degree |
|---|---|---|
| $a$ | 0 | 1 |
| $b$ | 1 | 2 |
| $c$ | 1 | 1 |
| $d$ | 1 | 1 |
| $e$ | 1 | 1 |
| $f$ | 2 | 0 |

The source is $a$ and the sink is $f$. Removing sources in turn, and taking the first one in alphabetical order each time, gives the topological order $a, b, c, d, e, f$. The graph has exactly three topological orders: $a, b, c, d, e, f$, then $a, b, c, e, d, f$, then $a, b, e, c, d, f$. The tasks $a$, $b$ must come first and $f$ last, and $e$ may go before $c$, between $c$ and $d$, or after $d$.

**The number of DAGs.** The number of labelled DAGs on the vertex set $\{1, \ldots, n\}$ satisfies Robinson's recurrence

$$a_n = \sum_{k=1}^{n} (-1)^{k+1} \binom{n}{k} 2^{k(n-k)} a_{n-k}, \qquad a_0 = 1.$$

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| labelled DAGs $a_n$ | 1 | 3 | 25 | 543 | 29281 | 3781503 |
| directed graphs without loops, $2^{n(n-1)}$ | 1 | 4 | 64 | 4096 | 1048576 | 1073741824 |

For $n = 2$ the three DAGs are the empty graph, $(1, 2)$ and $(2, 1)$; the fourth loopless graph, with both edges, is a cycle.

**More examples.**

- A [rooted tree](/rooted-tree/) with edges from parent to child.
- The [condensation graph](/condensation-graph/) of each directed graph: contract each [strongly connected component](/strongly-connected-components/) to one vertex. The result is always a DAG.
- The subproblem graph of a dynamic program, with an edge from each subproblem to each subproblem whose answer it uses. The program is correct only if this graph is a DAG, and it solves the subproblems in a topological order.
- A [Bayesian network](/bayesian-network/), whose edges point from causes to effects.

**Non-examples.**

- The edges $(0, 1), (1, 2), (2, 0)$ form a directed cycle, so the graph is not a DAG and has no topological order.
- A graph with a self-loop $(v, v)$.
- An undirected tree is not a DAG, since it is not directed. Each orientation of it is a DAG.
- A DAG need not be a tree: the edges $(0, 1), (0, 2), (1, 3), (2, 3)$ form a DAG in which vertex 3 has two parents.

**Costs.** On an [adjacency list](/adjacency-list/), testing acyclicity and computing a topological order take $\Theta(n + m)$ time by DFS or by Kahn's algorithm. On an [adjacency matrix](/adjacency-matrix/), the same algorithms take $\Theta(n^2)$ time. After the order is known, [shortest paths](/dag-shortest-paths/) and [longest paths](/dag-longest-path/) from one source take $\Theta(n + m)$ time with any real weights, by relaxing the edges in topological order.

## Related definitions

- [Acyclic graph](/acyclic-graph/): the general notion, with forests as the undirected case.
- [Topological sort](/topological-sort/) and the [topological ordering theorem](/topological-ordering-theorem/).
- [DAG source lemma](/dag-source-lemma/): each finite DAG has a source.
- [Condensation graph](/condensation-graph/): the DAG of the strongly connected components.
- [Transitive closure](/transitive-closure/) and [transitive reduction](/transitive-reduction/).
- [Critical path](/critical-path/) and [precedence-constrained scheduling](/precedence-constrained-scheduling/): scheduling on a DAG.

## References
