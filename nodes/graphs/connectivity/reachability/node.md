---
tag: BDXNZA
kind: problem
slug: reachability
name: Reachability
aliases:
- Directed reachability
- s-t connectivity
area: graphs/connectivity
level: intro
summary: Decide whether a target vertex can be reached from a source vertex.
prereqs: [graph-reachability, directed-graph, walk]
see_also: [graph-reachability, transitive-closure, strongly-connected-components, strongly-connected-graph, dynamic-reachability, parenthesis-theorem, nondeterministic-logspace, cfl-reachability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search, Section 20.3, Depth-first search (the parenthesis theorem), and Section 23.2 (transitive closure of a directed graph)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Space complexity (the language PATH, Savitch's theorem, and Section 8.5, NL-completeness of PATH)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic graph algorithms (reachability and whatever-first search), and Chapter 6, Depth-first search
---

Reachability is the decision problem that asks, for a [directed graph](/directed-graph/) and two vertices $s$ and $t$, whether some directed path leads from $s$ to $t$. It is the s-t form of [graph reachability](/graph-reachability/), which asks for all vertices reachable from $s$, and the one-entry form of the [transitive closure](/transitive-closure/), which asks for all pairs. One graph search answers a single question in $O(n + m)$ time. When many questions come for the same graph, the problem becomes a data structure question: how much to precompute, how much memory to keep, and how fast to answer each query.

## In plain words

You have a map of one-way roads and two places, a start and a goal. Can you drive from the start to the goal?

To answer once, explore from the start and mark every place you reach. Stop when you mark the goal, or when there is nothing new to mark. To answer many such questions about the same map, it pays to prepare: you can write down every answer in a big table, or keep small labels on each place that let you combine two labels into an answer. The art is to keep the preparation and the memory small and the answers fast.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ arcs, in [adjacency lists](/adjacency-list/), and two vertices $s, t \in V$. Parallel arcs and [self-loops](/self-loop/) are allowed and do not change the answer. An undirected graph is the directed graph with both arcs of each edge.

**Output.** Yes if there is a directed [walk](/walk/) $s = x_0, x_1, \ldots, x_k = t$ with $(x_{i-1}, x_i) \in E$ for each $i$, else no. Write $s \leadsto t$ for "yes". A walk exists exactly when a path with distinct vertices exists, and $s \leadsto s$ by the walk with $k = 0$.

**The relation.** The relation $\leadsto$ is the reflexive and transitive closure of the arc relation $E$: it is the smallest relation that contains $E$, is reflexive and is transitive. So it is a preorder on $V$. It is symmetric for undirected graphs, where its classes are the [connected components](/connected-components/). In general, $u \leadsto v$ and $v \leadsto u$ together define the [strongly connected components](/strongly-connected-components/), and on these classes $\leadsto$ is a partial order.

**Certificates.** A yes answer has a short proof: a path with at most $n - 1$ arcs. A no answer also has one: a set $S \subseteq V$ with $s \in S$, $t \notin S$ and no arc from $S$ to $V \setminus S$. If such an $S$ exists, a walk from $s$ to $t$ would need an arc that leaves $S$, so $s \not\leadsto t$. If $s \not\leadsto t$, the set $S = \{v : s \leadsto v\}$ is such a set.

## Variants

- **One query.** The basic form above.
- **Many queries, same graph.** Preprocess $G$ into a *reachability oracle*, then answer each query $(u, v)$. The cost has three parts: preprocessing time, memory, and query time.
- **Undirected s-t connectivity.** The relation is symmetric. With arc insertions only, [union-find](/union-find-connectivity/) answers queries online in almost constant amortized time.
- **Dynamic.** Arcs are inserted and deleted between queries. See [dynamic reachability](/dynamic-reachability/).
- **Bounded length.** Is there a path with at most $k$ arcs? A [breadth-first search](/breadth-first-search/) answers it.
- **Constrained paths.** The labels on the path must form a word of a given language. For a regular language this is reachability in a product graph. For a context-free language it is [CFL-reachability](/cfl-reachability/).
- **Implicit graphs.** The graph is a state space given by rules, as in [model checking](/reachability-problem/).

## Examples

Take the directed graph with vertices 0 to 7 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $4 \to 1$, $5 \to 2$, $5 \to 6$, $6 \to 7$, $7 \to 5$.

| query | answer | certificate |
|---|---|---|
| $0 \leadsto 4$? | yes | the path $0 \to 1 \to 3 \to 4$ |
| $4 \leadsto 0$? | no | $S = \{1, 3, 4\}$: no arc leaves it |
| $7 \leadsto 3$? | yes | the path $7 \to 5 \to 2 \to 3$ |
| $0 \leadsto 6$? | no | $S = \{0, 1, 2, 3, 4\}$ |
| $2 \leadsto 1$? | yes | the path $2 \to 3 \to 4 \to 1$ |
| $3 \leadsto 2$? | no | $S = \{1, 3, 4\}$ |

The strongly connected components are $\{1, 3, 4\}$, $\{5, 6, 7\}$, $\{0\}$ and $\{2\}$. The vertices 5, 6 and 7 reach every vertex except 0, and 1, 3 and 4 reach only their own class.

## Known algorithms

**One query.**

- **A search from $s$.** [Breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/) or any [whatever-first search](/whatever-first-search/) from $s$, stopped when $t$ is marked. Time $O(n + m)$, and less when $t$ is close.
- **Bidirectional search.** Search forward from $s$ in $G$ and backward from $t$ in the [transpose](/graph-transpose/), one step of each in turn. Answer yes when a vertex is marked by both searches, and no when one search runs out of vertices without such a meeting. This is correct: a vertex marked by both has a walk from $s$ and a walk to $t$. If the forward search runs out, it has marked all of $\{v : s \leadsto v\}$, and $t$ is marked by the backward search from the start, so $s \leadsto t$ would have caused a meeting. The case of the backward search is symmetric. The worst case is still $O(n + m)$, but on graphs that grow fast with distance, the two balls of half the radius are much smaller than one ball of the full radius.

**Many queries.** Let $q$ be the number of queries.

| method | preprocessing | memory | query |
|---|---|---|---|
| a new search for each query | none | $O(n + m)$ | $O(n + m)$ |
| full [transitive closure](/transitive-closure/) | $O(n(n + m))$, or $\Theta(n^3)$ by [Warshall](/warshall-algorithm/) | $n^2$ bits | $O(1)$ |
| closure of the [condensation](/condensation-graph/) | $O(n + m)$ plus the closure of $k$ classes | $k^2$ bits plus $n$ labels | $O(1)$ |
| rooted tree, arcs from parent to child | $O(n)$ | $O(n)$ | $O(1)$ |
| hub labels (2-hop labels) | depends on the graph | the total label size | $O(\text{label size})$ |

For a rooted tree, one DFS gives each vertex its [discovery and finish times](/discovery-and-finish-times/). By the [parenthesis theorem](/parenthesis-theorem/), $u \leadsto v$ exactly when $d[u] \le d[v]$ and $f[v] \le f[u]$, so a query compares four numbers.

Hub labels store for each vertex $v$ two sets of vertices, $L_{\mathrm{out}}(v)$ and $L_{\mathrm{in}}(v)$, such that for each pair, $u \leadsto v$ if and only if $L_{\mathrm{out}}(u) \cap L_{\mathrm{in}}(v) \neq \emptyset$. The trivial choice is $L_{\mathrm{out}}(u) = \{v : u \leadsto v\}$ and $L_{\mathrm{in}}(v) = \{v\}$. Good labelings choose a few central vertices as hubs, so that each reachable pair has a hub on some path between them.

## Bounds

**One query, adjacency lists.** Every correct algorithm reads $\Omega(m)$ entries in the worst case. Take a graph in which $t$ has no incoming arc and all other vertices are reachable from $s$. The answer is no. If the algorithm does not read some entry of the list of a vertex $u \ne t$, change that entry to $t$. The algorithm reads the same values and still answers no, but now $s \leadsto u \to t$. So it reads all entries outside the list of $t$, and the list of $t$ can be empty.

**Oracles.** The full closure uses $n^2$ bits, and this is necessary in the worst case for any structure that stores the answers exactly: the [directed acyclic graphs](/directed-acyclic-graph/) with all arcs from $\{0, \ldots, n/2 - 1\}$ to $\{n/2, \ldots, n - 1\}$ have $2^{n^2/4}$ different reachability relations, so some of them need $n^2/4$ bits. Sparse classes do better: trees need $O(n)$ words, as above.

**Space.** With a read-only input and a small work space, directed reachability is complete for [NL](/nondeterministic-logspace/), and the undirected case is in [L](/logspace/). The [graph reachability](/graph-reachability/) page gives these results with Savitch's theorem and the Immerman-Szelepcsényi theorem.

## Reductions

- **To acyclic graphs.** Reachability in $G$ equals reachability between the classes in the [condensation](/condensation-graph/), which is acyclic. This costs $O(n + m)$ time.
- **Acyclic graphs are as hard, for small space.** Build the layered graph with the vertices $(v, i)$ for $v \in V$ and $0 \le i \le n - 1$, and the arcs $(u, i) \to (v, i + 1)$ for each arc $(u, v)$ and $(v, i) \to (v, i + 1)$ for each $v$. It is acyclic, because each arc raises $i$ by 1. Then $s \leadsto t$ in $G$ if and only if $(s, 0) \leadsto (t, n - 1)$: a path with $k \le n - 1$ arcs moves up $k$ layers and then waits at $t$ for $n - 1 - k$ layers, and a path in the layered graph projects to a walk in $G$ when the waiting arcs are dropped. The construction needs only logarithmic work space.
- **Strong connectivity.** $u$ and $v$ are in the same [strongly connected component](/strongly-connected-components/) exactly when $u \leadsto v$ and $v \leadsto u$.
- **Cycle through an arc.** The arc $(u, v)$ lies on a directed cycle exactly when $v \leadsto u$.

## Applications

- **Ancestry in version control.** "Is commit $a$ an ancestor of commit $b$?" is a reachability query in the acyclic graph of commits, with arcs from each commit to its parents.
- **Type hierarchies.** "Is class $A$ a subtype of class $B$?" is a query in the inheritance graph. With single inheritance the graph is a tree, and the interval test of the parenthesis theorem answers each query in constant time.
- **Program analysis.** Many analyses ask whether a value can flow from one point to another, which is reachability in a graph of program points, often with the CFL constraint that calls and returns match.
- **Access control and dependencies.** Whether a user gets a permission through a chain of roles, or whether one package depends on another through a chain of dependencies.

## References
