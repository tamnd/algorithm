---
tag: V7TB1S
kind: theorem
slug: eulers-theorem-eulerian-graphs
name: Euler's theorem on Eulerian graphs
aliases:
- Euler's characterization of Eulerian circuits
area: graphs/paths-and-cycles
level: intro
summary: A graph whose edges lie in one component has an Eulerian circuit iff all degrees are even, and an Eulerian path iff it has zero or two odd vertices.
prereqs: [eulerian-circuit, eulerian-path, degree, handshake-lemma, connected-components]
see_also: [eulerian-graph, eulerian-path-problem, hierholzer-algorithm, fleury-algorithm, chinese-postman-problem, de-bruijn-existence-theorem, in-degree-and-out-degree]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.8, Euler tours, Theorem 1.8.1 (Euler 1736) and its proof by a longest trail
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3, Connected graphs, Section 3.3, Euler tours (the theorem for graphs with loops and parallel edges, and Euler trails)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-3, Euler tour (the directed form)
  - paper: "Leonhard Euler, Solutio problematis ad geometriam situs pertinentis, Commentarii academiae scientiarum Petropolitanae 8, 128 to 140 (written 1736, printed 1741)"
    locator: the whole paper (the bridges of Königsberg; the necessity of the degree condition)
  - paper: "Carl Hierholzer, Über die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren, Mathematische Annalen 6, 30 to 32 (1873)"
    locator: the whole paper (the first published proof that the condition suffices)
  - book: "Norman L. Biggs, E. Keith Lloyd and Robin J. Wilson, Graph Theory 1736-1936, Clarendon Press, Oxford, 1976"
    locator: Chapter 1, Paths (translations of Euler's and Hierholzer's papers, with commentary)
---

Euler's theorem says that a finite graph whose edges all lie in one [connected component](/connected-components/) has an [Eulerian circuit](/eulerian-circuit/) if and only if each vertex has even [degree](/degree/), and an [Eulerian path](/eulerian-path/) if and only if it has zero or two vertices of odd degree. For a directed graph, the condition is that in-degree equals out-degree at each vertex, with one surplus of one at each end for an open path. The theorem holds for [multigraphs](/multigraph/) with parallel edges and [self-loops](/self-loop/). Euler proved the necessity in 1736 for the bridges of Königsberg; Hierholzer published the first proof of the sufficiency in 1873, and his proof is the linear-time [Hierholzer's algorithm](/hierholzer-algorithm/).

## Statement

Let $G = (V, E)$ be a finite graph that may have parallel edges and self-loops. In an undirected graph, $d(v)$ counts the edge ends at $v$, so a self-loop adds 2. In a directed graph, $d^+(v)$ and $d^-(v)$ count the edges out of and into $v$, and a self-loop adds 1 to each. Say that the edges of $G$ are *in one component* if some component of $G$ (of the underlying undirected graph, when $G$ is directed) contains every edge. Isolated vertices are allowed anywhere.

**Theorem (undirected).** Let the edges of $G$ be in one component.

1. $G$ has an Eulerian circuit if and only if $d(v)$ is even for each $v \in V$.
2. For $s \ne t$, $G$ has an Eulerian path from $s$ to $t$ if and only if $s$ and $t$ are exactly the vertices of odd degree.

If the edges of $G$ are not in one component, $G$ has no Eulerian path at all. So $G$ has an Eulerian path if and only if its edges are in one component and it has 0 or 2 odd vertices. By the [handshake lemma](/handshake-lemma/), it never has exactly 1.

**Theorem (directed).** Let the edges of $G$ be in one component.

1. $G$ has a directed Eulerian circuit if and only if $d^+(v) = d^-(v)$ for each $v \in V$.
2. For $s \ne t$, $G$ has a directed Eulerian path from $s$ to $t$ if and only if $d^+(s) - d^-(s) = 1$, $d^-(t) - d^+(t) = 1$, and $d^+(v) = d^-(v)$ for each other $v$.

## In plain words

Each time a pen passes through a point on a drawing, it uses one line to come in and one line to go out. So, if you draw a figure in one stroke and never trace a line twice, each point where you only pass through has its lines in pairs. Only the first and the last point can have an odd number of lines. If the stroke ends where it began, every point has an even number.

The surprise is that this test is also enough. If the drawing is in one piece and the counts are even, you can always finish: start anywhere, walk until you are stuck, which can only happen back at the start, and then splice in loops through the lines you missed.

## Proof

Write a trail as $W = (v_0, e_1, v_1, \ldots, e_k, v_k)$. For a vertex $v$, the *ends of $W$ at $v$* are the edge ends at $v$ that $W$ uses. Each index $i$ with $0 < i < k$ and $v_i = v$ uses two ends at $v$: the end of $e_i$ and the end of $e_{i+1}$. This also holds when $e_i$ or $e_{i+1}$ is a self-loop, whose two ends are both at $v$. The index $0$ uses one end (of $e_1$) and the index $k$ uses one end (of $e_k$). So the number of ends of $W$ at $v$ is even, except that it is odd at $v_0$ and at $v_k$ when $v_0 \ne v_k$.

**Necessity, undirected.** An Eulerian path uses every edge end exactly once, so the number of its ends at $v$ is $d(v)$. If the path is closed, every $d(v)$ is even. If it is open from $s$ to $t$, exactly $s$ and $t$ have odd degree. All edges of a trail lie in one component, because consecutive edges share a vertex.

**Necessity, directed.** In a directed trail, each index $0 < i < k$ with $v_i = v$ uses one edge into $v$ and one edge out of $v$. The index 0 uses an edge out of $v_0$ and the index $k$ uses an edge into $v_k$. An Eulerian path uses each edge once, so $d^+(v) = d^-(v)$ for each $v$ when it is closed, and when it is open from $s$ to $t$, the surplus is $+1$ out of $s$, $+1$ into $t$, and 0 elsewhere.

**Sufficiency of 1, undirected.** If $E = \emptyset$, the trail $(v)$ of length 0 is an Eulerian circuit. Else let $W = (v_0, e_1, \ldots, e_k, v_k)$ be a trail of $G$ with the largest number $k$ of edges; it exists because a trail has at most $|E|$ edges, and $k \ge 1$.

*Step 1: $W$ is closed.* Assume that $v_0 \ne v_k$. The number of ends of $W$ at $v_k$ is odd, and $d(v_k)$ is even, so some edge end at $v_k$ is not used by $W$. Its edge $e$ is not in $W$: an edge in $W$ has both its ends used, a self-loop included. Then $W$ followed by $e$ is a trail with $k + 1$ edges, which contradicts the choice of $W$.

*Step 2: $W$ uses every edge.* Assume that some edge $e$ is not in $W$. Let $U$ be the set of vertices on $W$. Because all edges are in one component, there is a path $P$ in $G$ from an end $x$ of $e$ to $v_0$. If $x \in U$, put $f = e$. Else let $y$ be the first vertex of $P$ in $U$, and let $f$ be the edge of $P$ that enters $y$; its other end is not in $U$, so $f$ is not in $W$. In both cases, $f$ is an edge not in $W$ with an end $v_i \in U$. Since $W$ is closed, the rotation $(v_i, e_{i+1}, \ldots, e_k, v_k = v_0, e_1, \ldots, e_i, v_i)$ is a trail with the same edges, and appending $f$ gives a trail with $k + 1$ edges. This contradicts the choice of $W$. So $W$ is an Eulerian circuit.

**Sufficiency of 2, undirected.** Let $s \ne t$ be the only odd vertices. Add a new edge $f$ with ends $s$ and $t$ (it may be parallel to an existing edge). In $G + f$ every degree is even, and the edges are in one component, because $s$ has odd degree, so it has an edge in the component of all edges, and $f$ joins $s$ to $t$. By part 1, $G + f$ has an Eulerian circuit. Rotate it so that $f$ is its last edge, and reverse it if needed so that it starts at $s$: it reads $(s, e_1, \ldots, e_m, t, f, s)$. Removing the last step gives an Eulerian path of $G$ from $s$ to $t$.

**Sufficiency, directed.** The same proof works with three changes. In Step 1, if $v_0 \ne v_k$, then $W$ uses one more edge into $v_k$ than out of $v_k$, and $d^+(v_k) = d^-(v_k)$, so some edge out of $v_k$ is unused. In Step 2, the path $P$ is a path of the underlying undirected graph, and the edge $f$ may point into $v_i$. But $W$ is closed, so it uses as many edges into $v_i$ as out of $v_i$, and the unused edges are balanced at $v_i$ too. Since one unused edge enters $v_i$, an unused edge leaves $v_i$, and we append that one. For part 2, add the new edge $t \to s$. $\blacksquare$

## Consequences

- **Algorithms.** The proof of Step 2 is [Hierholzer's algorithm](/hierholzer-algorithm/): walk until stuck, then splice in a closed trail at a vertex with unused edges. With adjacency lists and a pointer to the next unused edge at each vertex, it runs in $O(|V| + |E|)$ time. [Fleury's algorithm](/fleury-algorithm/) uses the same theorem with a different rule. The test itself is linear: count degrees and run one [graph search](/connected-components/). This solves the [Eulerian path problem](/eulerian-path-problem/).
- **Cycle decomposition (Veblen).** An undirected graph is even if and only if its edge set is a disjoint union of cycles. The "if" part holds because each cycle adds 2 to the degree of each of its vertices. For "only if", use induction on $|E|$. If $E \ne \emptyset$, the graph has a cycle: a self-loop or two parallel edges is a cycle, and otherwise the first vertex $v_0$ of a longest simple path $v_0, \ldots, v_k$ with $k \ge 1$ has even degree $\ge 2$, so it has a neighbour other than $v_1$, which lies on the path by maximality and closes a cycle. Removing the edges of that cycle keeps every degree even, and the induction hypothesis splits the rest. The same holds for balanced directed graphs and directed cycles.
- **Covering by trails.** If a connected graph has $2k > 0$ odd vertices, its edges split into exactly $k$ trails and no fewer. At least $k$ are needed, because each odd vertex is an end of some trail, and a trail has two ends. To get $k$, add $k$ new edges that pair up the odd vertices, take an Eulerian circuit of the result, and delete the $k$ new edges. This is the drawing count for the "how many strokes" puzzles.
- **The Chinese postman.** If $G$ is not even, a closed walk through every edge must repeat a set of edges that makes all degrees even. The [Chinese postman problem](/chinese-postman-problem/) finds the cheapest such set.
- **De Bruijn sequences.** The de Bruijn graph is balanced and strongly connected, so by the directed theorem it has an Eulerian circuit, which spells a [de Bruijn sequence](/de-bruijn-sequence/). See the [de Bruijn existence theorem](/de-bruijn-existence-theorem/).

## Tightness

**Both conditions are needed.** Two disjoint triangles are even, but have no Eulerian path: the component condition fails. The [complete graph](/complete-graph/) $K_4$ is connected, but has four odd vertices and no Eulerian path. The transitive triangle $0 \to 1$, $1 \to 2$, $0 \to 2$ has an even underlying graph, but vertex 0 has a surplus of $+2$ out and vertex 2 a surplus of $+2$ in. So it has no directed Eulerian circuit and no directed Eulerian path, although its underlying undirected graph has an Eulerian circuit.

**The isolated vertex case.** The condition is "the edges are in one component", not "$G$ is connected". A triangle plus an isolated vertex has an Eulerian circuit. If the theorem is stated with "connected", it is still true but it says less.

**Finiteness is needed.** The two-way infinite path $\ldots, -1, 0, 1, \ldots$ is connected and every degree is 2, but it has no Eulerian circuit, because a circuit is a finite sequence. In the proof, the longest trail exists only because $E$ is finite.

## History

Euler presented his solution of the problem of the seven bridges of Königsberg to the Saint Petersburg Academy in 1736, and it was printed in 1741. He showed that a route that crosses each bridge once needs at most two land areas with an odd number of bridges, and he stated the converse without a proof. Carl Hierholzer gave the first published proof of the converse. His paper appeared in 1873, after his death in 1871. Biggs, Lloyd and Wilson reprint both papers in translation, with commentary. The directed form and the use of the theorem in linear-time algorithms are standard in textbooks such as CLRS.

## References
