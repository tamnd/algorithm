---
tag: PZF188
kind: problem
slug: strongly-connected-components
name: Strongly connected components
aliases:
- SCC decomposition
area: graphs/connectivity
level: intro
summary: Partition a directed graph into maximal sets of mutually reachable vertices.
prereqs: [strongly-connected-graph, equivalence-relation, depth-first-search]
see_also: [kosaraju-sharir, tarjan-scc, gabow-path-based-scc, condensation-graph, graph-transpose, weakly-connected-graph, transitive-closure, two-sat-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.5, Strongly connected components (the component graph is acyclic, and the two-pass algorithm with the transpose)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.4, Strongly connected components (every directed graph is a DAG of its strongly connected components)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the section on strongly connected components (the first linear-time algorithm)
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified boolean formulas, Information Processing Letters 8(3), 121 to 123 (1979)
    locator: the whole paper (2-SAT by strongly connected components of the implication graph)
  - paper: doi:10.1016/0898-1221(81)90008-0
    title: Micha Sharir, A strong-connectivity algorithm and its applications in data flow analysis, Computers and Mathematics with Applications 7(1), 67 to 72 (1981)
    locator: the whole paper (the two-pass algorithm and its use in data flow analysis)
---

The strongly connected components problem asks to split the vertices of a [directed graph](/directed-graph/) into its strongly connected components: the maximal sets of vertices in which each vertex can reach each other one. The components form a partition of the vertices, and contracting each of them gives the [condensation](/condensation-graph/), which is always acyclic. So every directed graph is a [directed acyclic graph](/directed-acyclic-graph/) of [strongly connected](/strongly-connected-graph/) pieces. The problem is solved in $\Theta(n + m)$ time by [depth-first search](/depth-first-search/), with the algorithms of [Kosaraju and Sharir](/kosaraju-sharir/), of [Tarjan](/tarjan-scc/) and of [Gabow](/gabow-path-based-scc/).

## In plain words

Think of a city with one-way streets. Two crossings belong together if you can drive from the first to the second and also back again. This splits the crossings into groups. Inside a group you can get from anywhere to anywhere. Between two groups, you can go at most one way: if you could go from group A to group B and also back, they would be one group.

So if you draw each group as one dot, the one-way links between the dots never form a loop. The problem is to find these groups. A good algorithm does it with a constant number of passes over the streets.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ arcs, given by [adjacency lists](/adjacency-list/). Parallel arcs and [self-loops](/self-loop/) are allowed. They do not change the answer, because reachability ignores them.

**The relation.** Write $u \leadsto v$ when there is a directed path from $u$ to $v$ (a path of length 0 is allowed, so $u \leadsto u$). Define

$$u \sim v \iff u \leadsto v \ \text{ and } \ v \leadsto u.$$

This is an [equivalence relation](/equivalence-relation/): it is reflexive by the path of length 0, symmetric by its form, and transitive because walks can be joined. Its classes are the *strongly connected components* (SCCs) of $G$.

**Output.** A label $c(v)$ for each $v \in V$ such that $c(u) = c(v) \iff u \sim v$. Many algorithms also give the components in a [topological order](/topological-ordering/) of the condensation, or in the reverse of one.

Three facts make the classes useful.

- **Each class is strongly connected inside.** Let $u \sim v$ and let $w$ lie on a directed $u$-$v$ path. Then $u \leadsto w$, and $w \leadsto v \leadsto u$, so $w \sim u$. So each path between two vertices of a class stays in the class, and the subgraph induced by a class is strongly connected.
- **The classes are maximal.** If $S$ is any vertex set whose induced subgraph is strongly connected, then all its vertices are pairwise related by $\sim$, so $S$ lies in one class.
- **The condensation is acyclic.** Let $G^{\mathrm{SCC}}$ have one vertex for each class and an arc $(C, D)$ for $C \ne D$ when some arc of $G$ goes from $C$ to $D$. A directed cycle $C_1 \to C_2 \to \cdots \to C_k \to C_1$ with $k \ge 2$ would give walks in $G$ from each $C_i$ to each $C_j$, so all of them would be one class. This is a contradiction.

A vertex that lies on no directed cycle forms a class of size 1. Such a class is called *trivial*. A class of size 1 whose vertex has a loop is nontrivial in the sense that it holds a cycle, which matters in model checking.

## Variants

- **Decision.** Is $G$ strongly connected? Two searches from one vertex, in $G$ and in the [transpose](/graph-transpose/), answer it in $\Theta(n + m)$ time. See [strongly connected graph](/strongly-connected-graph/).
- **One component.** The class of a given vertex $s$ is the set of vertices reachable from $s$ in $G$ and in $G^{\mathsf T}$, found by two searches.
- **Condensation.** Output the [condensation graph](/condensation-graph/) as well, in topological order. The linear-time algorithms give the order at no extra cost.
- **Count only.** The number of classes, or the size of the largest one.
- **Undirected graphs.** In an undirected graph the classes are the [connected components](/connected-components/). The directed graph with both arcs of each edge has the same classes. The weaker directed notion, where directions are ignored, gives the components of a [weakly connected graph](/weakly-connected-graph/).
- **Dynamic.** Arcs are inserted or deleted between queries. See [dynamic reachability](/dynamic-reachability/).
- **Parallel.** Depth-first search is hard to run in parallel. The [forward-backward algorithm](/forward-backward-scc/) and the [colouring algorithm](/coloring-scc/) use many searches that run at the same time.

## Examples

Take the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. It is the example of the [depth-first search](/depth-first-search/) page. The sets reached from each vertex are:

| vertex | reaches |
|---|---|
| 0, 1, 2, 3 | 0, 1, 2, 3, 4 |
| 4 | 4 |
| 5, 6 | 4, 5, 6 |

The classes are $\{0, 1, 2, 3\}$, $\{4\}$ and $\{5, 6\}$. The vertices 0 and 3 are related through the cycle $0 \to 3 \to 2 \to 0$. The vertex 4 reaches only itself, so its class is trivial. The condensation has the arcs $\{0, 1, 2, 3\} \to \{4\}$ (from the arc $3 \to 4$) and $\{5, 6\} \to \{4\}$ (from the arc $5 \to 4$). It is acyclic, and one topological order is $\{5, 6\}, \{0, 1, 2, 3\}, \{4\}$.

More small cases:

| graph | classes |
|---|---|
| a directed path $0 \to 1 \to 2 \to 3$ | four trivial classes; the graph is its own condensation |
| a directed cycle on $n$ vertices | one class |
| one vertex with a loop | one class, with a cycle |
| arcs $0 \to 1$ (twice), $1 \to 0$, $1 \to 2$ | $\{0, 1\}$ and $\{2\}$ |
| any directed acyclic graph | $n$ trivial classes |

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| [Kosaraju-Sharir](/kosaraju-sharir/) | $\Theta(n + m)$ | DFS of $G$ for finish times, then DFS of $G^{\mathsf T}$ in decreasing finish time; components come out in topological order |
| [Tarjan](/tarjan-scc/) | $\Theta(n + m)$ | one DFS with a stack and [low-link values](/low-link/); components come out in reverse topological order |
| [Gabow, path-based](/gabow-path-based-scc/) | $\Theta(n + m)$ | one DFS with two stacks, no low-link values |
| one search from each vertex | $O(n(n + m))$ | compute $R(v)$ for all $v$, then compare rows |
| [Warshall's algorithm](/warshall-algorithm/) | $\Theta(n^3)$ | [transitive closure](/transitive-closure/), then $u \sim v$ when both entries are 1 |
| [forward-backward](/forward-backward-scc/) | $O(n(n + m))$ worst case | divide and conquer with a pivot; parallel |

All three linear-time algorithms rest on one fact from the [white-path theorem](/white-path-theorem/): in any DFS, the first vertex discovered in a class is an ancestor in the [DFS forest](/dfs-forest/) of all other vertices of the class. So each class is a connected piece of one DFS tree, cut out at its first vertex, and the algorithms differ only in how they find these first vertices.

## Bounds

**Upper bound.** $\Theta(n + m)$ time and $\Theta(n)$ extra words of memory on adjacency lists in the [word RAM](/word-ram/), by any of the three DFS algorithms.

**Lower bound.** Every correct algorithm needs $\Omega(n + m)$ time on adjacency lists in the worst case. It must write a label for each of the $n$ vertices. For the arcs, take a graph that contains the path $0 \to 1 \to \cdots \to n-1$ and any number of other arcs $(u, v)$ with $1 \le u < v$. It is acyclic, so all classes are trivial. Suppose an algorithm does not read some entry of the list of a vertex $u \ge 1$. Change that entry to 0. The algorithm sees the same values and gives the same output, but now $0 \leadsto u \to 0$ is a cycle, so 0 and $u$ are in one class and the output is wrong. So the algorithm reads each such entry, and there can be $\Theta(n^2)$ of them.

**Space.** Deciding whether $u \sim v$ is complete for [nondeterministic logarithmic space](/nondeterministic-logspace/), because it contains the directed [reachability](/reachability/) problem: add the arc $(t, s)$ to a graph, and then $s \sim t$ exactly when $s \leadsto t$ in the old graph.

## Reductions

- **To two reachability searches.** The class of $s$ is $R_G(s) \cap R_{G^{\mathsf T}}(s)$. Repeating this for each unlabelled vertex gives an $O(n(n + m))$ algorithm.
- **From strong connectivity of a graph.** Deciding whether $G$ is strongly connected is the special case "is there one class".
- **2-SAT.** For a 2-CNF formula, build the [implication graph](/implication-graph/), with the arcs $\lnot a \to b$ and $\lnot b \to a$ for each clause $a \lor b$. The formula is satisfiable exactly when no variable $x$ has $x$ and $\lnot x$ in the same class (Aspvall, Plass and Tarjan, 1979). An assignment follows from the topological order of the classes. See [2-SAT](/2-sat/) and the [2-SAT algorithm](/two-sat-algorithm/).
- **Transitive closure.** Vertices of one class have the same reachable set. So the [transitive closure](/transitive-closure/) of $G$ follows from the closure of the condensation, which is acyclic and often much smaller.

## Applications

- **2-SAT** and other problems with implications, as above.
- **Markov chains.** The states of a finite chain split into communicating classes, which are the classes of its transition graph. A class is recurrent exactly when no arc leaves it in the condensation.
- **Model checking.** A [Büchi automaton](/buchi-automaton/) accepts some infinite word exactly when an accepting state is reachable from the start and lies in a class with a cycle. Finding the classes decides this emptiness question.
- **Compilers.** Loops of a control flow graph and cycles of mutual recursion in a call graph are found as nontrivial classes. Sharir's 1981 paper applied the two-pass algorithm to data flow analysis.
- **Deadlock.** In a wait-for graph, a cycle means a [deadlock](/deadlock-detection/), and the nontrivial classes contain all the cycles.
- **Build systems and packages.** Dependencies that form a cycle must be built or loaded together. Each class becomes one unit, and the condensation gives a valid order.

## References
