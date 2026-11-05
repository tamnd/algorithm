---
tag: DWK2JT
kind: theorem
slug: handshake-lemma
name: Handshake lemma
aliases:
- degree sum formula
area: graphs/graph-representation
level: intro
summary: The sum of all vertex degrees equals twice the number of edges.
prereqs: [degree, double-counting]
see_also: [handshaking-lemma, degree, in-degree-and-out-degree, adjacency-list, planar-edge-bound, free-tree-properties, regular-graph, eulers-theorem-eulerian-graphs]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.3 (Vertex degrees and counting), the Degree-Sum Formula and its corollaries
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1, Section 1.1, the theorem that the degrees sum to twice the number of edges, for graphs with loops and parallel edges
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.2 (The degree of a vertex)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the sum of the lengths of all adjacency lists, and the exercises of Appendix B.4
  - paper: "Leonhard Euler, Solutio problematis ad geometriam situs pertinentis, Commentarii academiae scientiarum Petropolitanae 8, 1736 (printed 1741)"
    locator: pages 128 to 140, the count of the bridge ends at the four land regions
---

The handshake lemma, or degree sum formula, says that in each undirected [graph](/graph/) the [degrees](/degree/) of all vertices add up to twice the number of [edges](/edge/): $\sum_{v} d(v) = 2m$. The proof counts each edge once at each of its two ends. In a directed graph the same count gives $\sum_v d^+(v) = \sum_v d^-(v) = m$. The lemma fixes the size of an [adjacency list](/adjacency-list/), it gives the average degree $2m/n$, and its parity form is the [handshaking lemma](/handshaking-lemma/).

## Statement

**Theorem (degree sum formula).** Let $G = (V, E, \psi)$ be a finite undirected [multigraph](/multigraph/), where loops and parallel edges are allowed and a loop adds 2 to the degree of its vertex. Then

$$\sum_{v \in V} d(v) = 2|E|.$$

In particular this holds for each simple graph $G = (V, E)$.

**Theorem (directed form).** Let $G = (V, E)$ be a finite [directed graph](/directed-graph/), with self-loops allowed, or a finite directed multigraph. Then

$$\sum_{v \in V} d^+(v) = \sum_{v \in V} d^-(v) = |E|.$$

Here $d^+(v)$ counts the edges with tail $v$ and $d^-(v)$ counts the edges with head $v$, so a loop at $v$ adds 1 to each.

## In plain words

At a party, some pairs of guests shake hands. Ask each guest how many hands they shook, and add up all the answers. The total is always twice the number of handshakes. Each handshake has two people in it, so each handshake is counted once by each of the two people, and so it is counted exactly twice in the total.

A graph is the same: each line has two ends, and the degree of a dot counts the line ends at that dot. So the degrees add up to two times the number of lines. With arrows, each arrow has one start and one end, so the arrow starts add up to the number of arrows, and so do the arrow ends.

## Proof

*Undirected form.* Count the set $I$ of *incidences*, the pairs (vertex, end of an edge at that vertex), in two ways. Each edge $e$ has exactly two ends: two distinct vertices, or the same vertex twice for a loop. Write the ends of $e$ as the two slots $(e, 1)$ and $(e, 2)$, so that

$$I = \{(e, j) : e \in E,\ j \in \{1, 2\}\}, \qquad |I| = 2|E|.$$

Each slot $(e, j)$ belongs to exactly one vertex, the vertex in that slot. So the sets $I_v = \{(e, j) \in I : \text{slot } j \text{ of } e \text{ is } v\}$, for $v \in V$, partition $I$, and $|I| = \sum_{v} |I_v|$. A non-loop edge $e$ with ends $v \ne u$ has one slot at $v$. A loop at $v$ has both of its slots at $v$. So $|I_v|$ is the number of non-loop edges at $v$ plus twice the number of loops at $v$, which is $d(v)$ by the definition of degree in a multigraph. Hence

$$\sum_{v \in V} d(v) = \sum_{v \in V} |I_v| = |I| = 2|E|.$$

*Directed form.* The map that sends each edge to its tail is a function from $E$ to $V$. The edges with tail $v$ are the preimage of $v$, and these preimages partition $E$. So $\sum_v d^+(v) = |E|$. The same argument with the head in place of the tail gives $\sum_v d^-(v) = |E|$. $\blacksquare$

*A second proof for simple graphs, by induction on $m$.* For $m = 0$, each degree is 0 and the sum is $0 = 2 \cdot 0$. For $m \ge 1$, remove one edge $\{u, v\}$, with $u \ne v$. This lowers $d(u)$ and $d(v)$ by 1 each and changes no other degree. So the degree sum drops by exactly 2. By the hypothesis for $m - 1$ edges, the smaller graph has the sum $2(m-1)$, and $G$ has the sum $2(m - 1) + 2 = 2m$. $\square$

## Consequences

- **Average degree.** For $n \ge 1$, the average degree is $\bar d = 2m/n$. So $\delta(G) \le 2m/n \le \Delta(G)$, and $m \le n \Delta(G) / 2$.
- **The size of an adjacency list.** The adjacency list of an undirected graph holds $\sum_v d(v) = 2m$ entries, and the adjacency list of a directed graph holds $\sum_v d^+(v) = m$ entries. This is the reason that [breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/) run in $O(n + m)$ time: they scan each list once, for $O(\sum_v (1 + d(v))) = O(n + m)$ work. The same sum gives the size $n + 1 + 2m$ words of the [compressed sparse row](/compressed-sparse-row/) form of an undirected graph.
- **Parity.** The number of vertices of odd degree is even. This is the [handshaking lemma](/handshaking-lemma/), and it follows because $2m$ is even.
- **Trees.** A [tree](/tree/) with $n \ge 2$ vertices has $n - 1$ edges, so its degrees sum to $2n - 2$. Each degree is at least 1, so at least two vertices have degree 1. See [free tree properties](/free-tree-properties/).
- **Planar graphs.** The same double count on the faces of a plane graph gives $\sum_f \ell(f) = 2m$, where $\ell(f)$ is the length of the boundary walk of face $f$. With [Euler's formula](/euler-formula/) it gives $m \le 3n - 6$ for a simple planar graph with $n \ge 3$, see [planar edge bound](/planar-edge-bound/).
- **Sparse graphs.** If $G$ has $m = O(n)$ edges, then fewer than $n/2$ vertices have degree larger than $4m/n$, since those vertices alone would have a degree sum larger than $2m$. Algorithms on sparse graphs use this to treat the few high-degree vertices apart.

**A worked example.** In the graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$, the degrees are $2, 3, 3, 3, 2, 1$. Their sum is $14 = 2 \cdot 7$. Its adjacency list has 14 entries. In the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$, the out-degrees are $2, 1, 1, 2, 0$ and the in-degrees are $0, 2, 2, 1, 1$, and each list sums to $6 = m$.

## Tightness

The formula is an identity, so there is nothing to tighten in it. The bound $m \le n\Delta/2$ that follows from it holds with equality exactly when $d(v) = \Delta$ for each $v$, that is, when $G$ is [regular](/regular-graph/). The [complete graph](/complete-graph/) $K_n$ is $(n-1)$-regular and has $n(n-1)/2$ edges, which meets the bound.

The rule that a loop adds 2 to the degree is needed. If a loop added 1, the graph with one vertex and one loop would have the degree sum 1 and one edge, and the formula would fail. In the directed form a loop adds 1 to $d^+$ and 1 to $d^-$, and both sums stay equal to $m$.

## History

Euler used this counting argument in his 1736 paper on the seven bridges of Königsberg. He counted, for each land region, the bridges that end there, and he used the fact that these counts sum to twice the number of bridges, because each bridge ends at two regions. The name "handshaking lemma" comes from the party picture above. The textbooks of West (Section 1.3) and of Bondy and Murty (Section 1.1) state it in the form of this page.

## References
