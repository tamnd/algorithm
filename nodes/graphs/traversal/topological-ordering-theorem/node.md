---
tag: S18084
kind: theorem
slug: topological-ordering-theorem
name: Topological ordering theorem
aliases:
- DAG characterization theorem
area: graphs/traversal
level: core
summary: A directed graph has a topological ordering exactly when it is acyclic.
prereqs: [topological-ordering, directed-acyclic-graph]
see_also: [topological-sort, kahns-algorithm, edge-classification, white-path-theorem, cycle-detection, depth-first-orders, condensation-graph]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.6, Directed acyclic graphs and topological ordering (a graph with a topological ordering is a DAG, every DAG has a node with no incoming edges, every DAG has a topological ordering)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4, Topological sort (the lemma that a directed graph is acyclic if and only if a depth-first search yields no back edges)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3.2, Directed acyclic graphs (a directed graph has a cycle if and only if its DFS reveals a back edge; every DAG has at least one source and one sink)
  - paper: "Edward Szpilrajn, Sur l'extension de l'ordre partiel, Fundamenta Mathematicae 16, 386 to 389 (1930)"
    locator: the extension theorem for partial orders
---

The topological ordering theorem says that a finite [directed graph](/directed-graph/) has a [topological ordering](/topological-ordering/), a list of its vertices in which each edge goes forward, if and only if it has no directed cycle. One direction is a one-line argument: a cycle would need its first vertex to come before itself. The other direction rests on the fact that each finite [directed acyclic graph](/directed-acyclic-graph/) has a vertex with no incoming edge. A third equivalent condition is that a [depth-first search](/depth-first-search/) finds no back edge. The two proofs of the hard direction become the two classical algorithms, [Kahn's algorithm](/kahns-algorithm/) and the [DFS topological sort](/topological-sort/).

## Statement

Let $G = (V, E)$ be a directed graph with a finite set of $n$ vertices. A *directed cycle* is a sequence of vertices $u_1, \ldots, u_k$ with $k \ge 1$ such that $(u_i, u_{i+1}) \in E$ for $1 \le i < k$ and $(u_k, u_1) \in E$; a self-loop is a cycle with $k = 1$. A *source* is a vertex with in-degree zero.

**Theorem.** The following are equivalent.

1. $G$ has a topological ordering.
2. $G$ has no directed cycle.
3. Some run of DFS$(G)$ finds no back edge.
4. Every run of DFS$(G)$ finds no back edge.

**Lemma (sources).** If $G$ is finite, has at least one vertex and has no directed cycle, then $G$ has a source.

## In plain words

If you can put the jobs in a line so that every rule points forward, then the rules cannot go round in a loop: a loop would have to come back to where it started, and that means going backwards at some point.

The other way is the real content. If there is no loop, you can always start: some job has no rule pointing at it, because otherwise you could walk backwards along rules forever, and with finitely many jobs you would come back to a job you have seen, which is a loop. Do that job first, forget it, and repeat. The leftover jobs still have no loop, so the same reason works each time.

Depth-first search gives a test: it finds a loop exactly when it reaches a vertex that it is still in the middle of exploring.

## Proof

**Proof of the lemma.** Assume that each vertex has an incoming edge. Start at any vertex $w_0$ and choose $w_1$ with $(w_1, w_0) \in E$, then $w_2$ with $(w_2, w_1) \in E$, and so on. The sequence $w_0, w_1, \ldots, w_n$ has $n + 1$ entries from a set of $n$ vertices, so some vertex repeats: $w_i = w_j$ with $i < j$. Then $w_j, w_{j-1}, \ldots, w_{i+1}$ is a directed cycle, because each $(w_{t+1}, w_t)$ is an edge and $(w_{i+1}, w_i) = (w_{i+1}, w_j)$ closes it. This contradicts the assumption that $G$ has no cycle. $\square$

**1 implies 2.** Let $\sigma$ be a topological ordering and assume that $u_1, \ldots, u_k$ is a directed cycle. Each edge of the cycle goes forward, so $\sigma(u_1) < \sigma(u_2) < \cdots < \sigma(u_k) < \sigma(u_1)$, which is false. For $k = 1$ this reads $\sigma(u_1) < \sigma(u_1)$.

**2 implies 1.** By induction on $n$. For $n = 0$ the empty list is a topological ordering. Let $n \ge 1$ and let $G$ have no cycle. By the lemma, $G$ has a source $s$. The graph $G - s$, with $s$ and its outgoing edges removed, has $n - 1$ vertices and no cycle, because each cycle of $G - s$ is a cycle of $G$. By the induction hypothesis it has a topological ordering $v_2, \ldots, v_n$. The list $s, v_2, \ldots, v_n$ is a topological ordering of $G$: an edge between two of the $v_i$ goes forward by the choice of the ordering of $G - s$, and an edge that touches $s$ goes out of $s$, because $s$ has no incoming edge, so it goes forward from the first place.

**4 implies 3.** DFS$(G)$ has at least one run.

**3 implies 2.** Fix a run with no back edge. By [edge classification](/edge-classification/), each edge $(u, v)$ is then a tree, forward or cross edge, and each of those has $f[v] < f[u]$. If $u_1, \ldots, u_k$ were a cycle, then $f[u_1] > f[u_2] > \cdots > f[u_k] > f[u_1]$, which is false. (In other words, the vertices in decreasing order of $f$ form a topological ordering, so 3 implies 1 directly.)

**2 implies 4.** Fix any run and assume that it finds a back edge $(u, v)$. Then $v$ is an ancestor of $u$ in the [depth-first forest](/dfs-forest/). If $u = v$, the edge is a self-loop, which is a cycle. Else let $v = w_0, w_1, \ldots, w_j = u$ be the tree path from $v$ to $u$. Each $(w_{i-1}, w_i)$ is a tree edge, so $w_0, \ldots, w_j$ with the edge $(u, v)$ is a directed cycle. This contradicts 2.

The chain $1 \Rightarrow 2 \Rightarrow 4 \Rightarrow 3 \Rightarrow 2 \Rightarrow 1$ proves that the four statements are equivalent. $\blacksquare$

## Consequences

- **Two algorithms.** The proof of "2 implies 1" is [Kahn's algorithm](/kahns-algorithm/): output a source, remove it, repeat. The proof of "3 implies 2" is the [DFS topological sort](/topological-sort/): list the vertices in decreasing order of finish time.
- **Cycle detection in linear time.** A directed graph has a cycle exactly when one DFS finds a back edge, and the back edge with its tree path is a cycle. This is the method of [DFS cycle detection](/dfs-cycle-detection/) for [cycle detection](/cycle-detection/).
- **Sinks.** Applied to the graph with all edges reversed, the lemma shows that each finite nonempty DAG also has a sink, a vertex with out-degree zero. The last vertex of any topological ordering is a sink, and the first is a source.
- **Uniqueness.** A DAG has exactly one topological ordering if and only if it has a directed path through all its vertices. If such a path $v_1, \ldots, v_n$ exists, each ordering must put $v_i$ before $v_{i+1}$ for each $i$, so it is the path. Conversely, if an ordering $v_1, \ldots, v_n$ has two neighbours $v_i, v_{i+1}$ with no edge $(v_i, v_{i+1})$, then exchanging them gives a second ordering: the only pair whose order changes is $(v_i, v_{i+1})$, and no edge joins them in either direction, since $(v_{i+1}, v_i)$ would go backwards in the first ordering.
- **Condensation.** The graph of [strong components](/strongly-connected-components/), the [condensation graph](/condensation-graph/), has no cycle, so it has a topological ordering.

## Tightness

**Finiteness is needed for the lemma.** Take the vertices $0, 1, 2, \ldots$ with the edges $(i + 1, i)$ for each $i$. This graph has no cycle, but each vertex has an incoming edge, so it has no source. It also has no topological ordering in the form of a list $v_1, v_2, \ldots$ indexed by the positive integers: the first vertex $v_1$ would need to be a source. The ordering by decreasing numbers is a linear order in which each edge goes forward, but it has no first element. Szpilrajn's extension theorem shows that each partial order, also an infinite one, extends to a linear order, so statement 2 still implies the existence of a linear order in which all edges go forward, but not of a list that starts with a first vertex.

**The DFS condition is about back edges only.** A DFS of an acyclic graph can have forward and cross edges. In the graph with the edges $0 \to 1$, $1 \to 2$ and $0 \to 2$, DFS from 0 with the list $0: 1, 2$ makes $0 \to 2$ a forward edge, and the graph is still acyclic.

**One cycle is enough to block every ordering, and the cycle can be long.** On a cycle of $n$ vertices, each vertex has in-degree one, so the lemma fails at the first step. Removing any one edge makes the graph a path with exactly one topological ordering.

## History

Kahn described the method of removing vertices with no predecessors in 1962, in a paper on the topological sorting of large networks, and Knuth presents it as Algorithm T in the first volume of The Art of Computer Programming. Cormen, Leiserson, Rivest and Stein prove the DFS form, with the lemma that a directed graph is acyclic if and only if a DFS finds no back edge. Kleinberg and Tardos state the theorem in the form "a graph is a DAG if and only if it has a topological ordering", with the lemma on sources as the main step. For infinite partial orders, the existence of a linear extension is Szpilrajn's theorem of 1930.

## References
