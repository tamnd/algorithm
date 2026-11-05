---
tag: QC6EWV
kind: definition
slug: strongly-connected-graph
name: Strongly connected graph
area: graphs/connectivity
level: intro
summary: A directed graph in which every vertex can reach every other vertex.
prereqs: [directed-graph, simple-path, connected-graph]
see_also: [strongly-connected-components, weakly-connected-graph, condensation-graph, graph-transpose, kosaraju-sharir, tarjan-scc, strong-orientation, reachability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4, Graphs (strongly connected directed graphs), and Section 20.5, Strongly connected components
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.4, Directed graphs (strongly connected digraphs and strong components)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (strong connectivity and strong components)
---

A strongly connected graph is a [directed graph](/directed-graph/) in which, for each ordered pair of vertices $(u, v)$, there is a directed path from $u$ to $v$. It is the directed form of a [connected graph](/connected-graph/), and it is the stronger of the two such forms: the weaker one, a [weakly connected graph](/weakly-connected-graph/), forgets the directions. Every directed graph splits into maximal strongly connected parts, its [strongly connected components](/strongly-connected-components/), and two graph searches from one vertex decide in linear time whether the whole graph is one such part.

## Definition

Let $G = (V, E)$ be a directed graph. [Parallel arcs](/multigraph/) and [self-loops](/self-loop/) are allowed. They do not change any statement on this page, because a directed path never needs a loop or a second copy of an arc.

A *directed $u$-$v$ path* is a sequence of distinct vertices $u = x_0, x_1, \ldots, x_k = v$ with an arc $(x_{i-1}, x_i) \in E$ for each $i$. For each $u$, the sequence $u$ alone is a path of length 0. Write $u \leadsto v$ when a directed $u$-$v$ path exists. A directed [walk](/walk/) from $u$ to $v$ exists exactly when a directed path exists, because a walk that visits a vertex twice gets shorter when the part between the two visits is cut out.

$$G \text{ is strongly connected} \iff V \neq \emptyset \ \text{ and } \ \forall u, v \in V : u \leadsto v.$$

We follow the convention of the [connected graph](/connected-graph/) page: the graph with no vertex is not strongly connected, and the graph with one vertex is.

**Root form.** Fix any vertex $r$. Then $G$ is strongly connected if and only if $r \leadsto v$ and $v \leadsto r$ for each $v \in V$.

*Proof.* The direction "only if" is the definition with $u = r$ or $v = r$. For "if", take any $u, v$. A walk from $u$ to $r$ followed by a walk from $r$ to $v$ is a walk from $u$ to $v$, so $u \leadsto v$. $\square$

The condition $v \leadsto r$ for all $v$ is the same as $r \leadsto v$ for all $v$ in the [transpose graph](/graph-transpose/) $G^{\mathsf T}$, which has the arc $(y, x)$ for each arc $(x, y)$ of $G$. So one [graph search](/graph-reachability/) from $r$ in $G$ and one in $G^{\mathsf T}$ decide strong connectivity in $\Theta(n + m)$ time, with $n = |V|$ and $m = |E|$.

**Cut form.** Write $E^{+}(S)$ for the set of arcs $(x, y)$ with $x \in S$ and $y \notin S$. A directed graph with $V \neq \emptyset$ is strongly connected if and only if

$$\forall S \text{ with } \emptyset \neq S \subsetneq V : \ E^{+}(S) \neq \emptyset.$$

*Proof.* Suppose $G$ is strongly connected and $\emptyset \neq S \subsetneq V$. Pick $u \in S$, $v \notin S$, and a directed path $x_0 = u, \ldots, x_k = v$. Let $i$ be the least index with $x_i \notin S$. Then $i \ge 1$, and $(x_{i-1}, x_i) \in E^{+}(S)$. Conversely, suppose that $G$ is not strongly connected, so $u \not\leadsto v$ for some $u, v$. Let $S = \{x : u \leadsto x\}$. Then $u \in S$ and $v \notin S$. An arc $(x, y)$ with $x \in S$ and $y \notin S$ would give $u \leadsto y$, so $E^{+}(S) = \emptyset$. $\square$

**Cycle form.** $G$ is strongly connected if and only if it is weakly connected and each arc lies on a directed cycle.

*Proof.* Suppose $G$ is strongly connected. A directed path is also a path of the underlying undirected graph, so $G$ is weakly connected. For an arc $(u, v)$ with $u \ne v$, take a directed $v$-$u$ path. It does not use the arc $(u, v)$, because it ends at its first visit to $u$, and with this arc it closes a directed cycle. A loop is a cycle of length 1. Conversely, suppose that $G$ is weakly connected and each arc lies on a directed cycle. For an arc $(x, y)$, the rest of its cycle is a walk from $y$ to $x$, so $x \leadsto y$ and $y \leadsto x$. Two vertices $u$ and $v$ are joined by a path of the underlying graph, and each of its steps uses an arc in one direction or the other. In both cases the two ends of the step reach each other. The relation $\leadsto$ is transitive, so $u \leadsto v$. $\square$

**Fewest arcs.** A strongly connected graph on $n \ge 2$ vertices has at least $n$ arcs, and the directed cycle on $n$ vertices has exactly $n$. *Proof.* Each vertex $v$ reaches some other vertex, so it has an outgoing arc to a vertex other than $v$. These $n$ arcs are distinct, because their tails are distinct. $\square$ So, unlike a [tree](/tree/) in the undirected case, the sparsest strongly connected graphs have $n$ arcs, not $n - 1$.

## Examples and non-examples

| graph | strongly connected? | why |
|---|---|---|
| one vertex, with or without a loop | yes | the only pair is $(u, u)$ |
| the directed cycle $0 \to 1 \to 2 \to 3 \to 0$ | yes | from each vertex, follow the cycle |
| two vertices with the arcs $0 \to 1$ (twice) and $1 \to 0$ | yes | parallel arcs do not matter |
| the complete directed graph on $n$ vertices | yes | each pair is joined by an arc in each direction |
| the directed path $0 \to 1 \to 2$ | no | $2 \not\leadsto 0$; the cut $S = \{2\}$ has no arc leaving it |
| any [directed acyclic graph](/directed-acyclic-graph/) with $n \ge 2$ | no | a sink has no outgoing arc, so $S = \{\text{sink}\}$ fails the cut form |
| the arcs $0 \to 1$, $1 \to 0$, $1 \to 2$, $2 \to 3$, $3 \to 2$ | no | weakly connected, but the arc $1 \to 2$ lies on no cycle |
| the graph with no vertex | no | by the convention $V \neq \emptyset$ |

The table counts the strongly connected graphs on the vertex set $\{1, \ldots, n\}$ without loops and parallel arcs, among all $2^{n(n-1)}$ such graphs.

| $n$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| all directed graphs | 1 | 4 | 64 | 4096 |
| strongly connected | 1 | 1 | 18 | 1606 |

For $n = 2$ the only strongly connected graph is the pair of opposite arcs. For $n = 3$ there are 18. By the number of arcs: 2 graphs with 3 arcs (the two directed triangles), 9 with 4 arcs (a triangle plus one arc, in 6 ways, or two opposite pairs that share a vertex, in 3 ways), 6 with 5 arcs (the complete graph minus one arc) and the complete graph with 6 arcs.

**Undirected graphs.** An undirected graph is the directed graph with both arcs $(u, v)$ and $(v, u)$ for each edge. In this view it is strongly connected exactly when it is connected, so the notion adds nothing there. The question becomes interesting when the edges must get one direction each: this is the [strong orientation](/strong-orientation/) problem.

## Related definitions

- [Strongly connected components](/strongly-connected-components/): the classes of the relation "$u \leadsto v$ and $v \leadsto u$". A graph is strongly connected exactly when it has one class. [Kosaraju-Sharir](/kosaraju-sharir/) and [Tarjan's algorithm](/tarjan-scc/) find all classes in linear time.
- [Condensation graph](/condensation-graph/): contract each strong component to a vertex. The result is always acyclic, and it has one vertex exactly when the graph is strongly connected.
- [Weakly connected graph](/weakly-connected-graph/): the underlying undirected graph is connected. Strong implies weak, and the directed path $0 \to 1$ shows that the converse fails.
- [Connected graph](/connected-graph/): the undirected notion.
- [Strong orientation](/strong-orientation/): an undirected graph has a strongly connected orientation exactly when it is connected and has no [bridge](/bridge/).
- [Reachability](/reachability/) and [transitive closure](/transitive-closure/): $G$ is strongly connected exactly when its transitive closure contains every ordered pair.

## References
