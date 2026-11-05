---
tag: AHD765
kind: theorem
slug: handshaking-lemma
name: Handshaking lemma
area: graphs/graph-representation
level: intro
summary: In any undirected graph the sum of all vertex degrees equals twice the number of edges, so the number of odd-degree vertices is even.
prereqs: [handshake-lemma]
see_also: [handshake-lemma, degree, eulerian-path, eulers-theorem-eulerian-graphs, christofides-algorithm, chinese-postman-problem, regular-graph, ppad]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.3 (Vertex degrees and counting), the Degree-Sum Formula and the corollary on the number of vertices of odd degree
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.2 (The degree of a vertex), the proposition that the number of vertices of odd degree is even
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1, Section 1.1, the corollary of the degree sum theorem
  - paper: "Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3), 1994"
    locator: pages 498 to 532, the class PPA and the parity argument on graphs of degree at most 2
  - paper: "Leonhard Euler, Solutio problematis ad geometriam situs pertinentis, Commentarii academiae scientiarum Petropolitanae 8, 1736 (printed 1741)"
    locator: pages 128 to 140, the count of the bridges at each land region
---

The handshaking lemma says that in each finite undirected [graph](/graph/) the number of vertices of odd [degree](/degree/) is even. It follows from the [handshake lemma](/handshake-lemma/), $\sum_v d(v) = 2m$: a sum of integers is even only if it has an even number of odd terms. The lemma is the base of many parity arguments. It shows that an [Eulerian path](/eulerian-path/) has at most two odd ends, that a perfect matching on the odd vertices exists in the [Christofides algorithm](/christofides-algorithm/), and that each graph with all degrees odd has an even number of vertices.

## Statement

**Theorem.** Let $G = (V, E)$ be a finite undirected [multigraph](/multigraph/), with loops counted twice in the degree. Let $O = \{v \in V : d(v) \text{ is odd}\}$. Then $|O|$ is even.

**Stronger form.** For each connected component $C$ of $G$, the number of odd-degree vertices in $C$ is even.

**Directed graphs.** In a directed graph the parity statement does not hold for the in-degree or for the out-degree alone. It holds for the total degree $d^+(v) + d^-(v)$, which is the degree of $v$ in the underlying undirected multigraph.

## In plain words

At any party, count the guests who shook an odd number of hands. That count is always even: zero, two, four, and so on. It can never be one or three.

The reason is the handshake count. If you add up the handshakes of all guests, you get twice the number of handshakes, which is an even number. The guests with an even count add an even number to the total. So the guests with an odd count must also add up to an even number. A sum of odd numbers is even only when there is an even number of them.

## Proof

By the [handshake lemma](/handshake-lemma/), $\sum_{v \in V} d(v) = 2|E|$, which is even. Split the sum:

$$2|E| = \sum_{v \in O} d(v) + \sum_{v \notin O} d(v).$$

Each term of the second sum is even, so the second sum is even. Hence $\sum_{v \in O} d(v) = 2|E| - \sum_{v \notin O} d(v)$ is even. Modulo 2, each term $d(v)$ with $v \in O$ is 1, so

$$0 \equiv \sum_{v \in O} d(v) \equiv \sum_{v \in O} 1 = |O| \pmod 2.$$

So $|O|$ is even.

For the stronger form, let $C$ be a component and let $G[C]$ be the subgraph on $C$ with all edges of $G$ that have both ends in $C$. Each edge at a vertex of $C$ has both ends in $C$, because its ends are joined by that edge and so lie in the same component. So $d_{G[C]}(v) = d_G(v)$ for each $v \in C$. Apply the theorem to the graph $G[C]$. $\blacksquare$

**The directed case.** The graph with the single edge $(0, 1)$ has the out-degrees $1, 0$, so exactly one vertex has odd out-degree. So no parity rule holds for $d^+$ alone, and by the same example none holds for $d^-$ alone. The total degree $d^+(v) + d^-(v)$ sums to $2|E|$ by the directed form of the handshake lemma, and the proof above applies to it.

## Consequences

- **Odd regular graphs have even order.** If $G$ is $k$-[regular](/regular-graph/) with $k$ odd, then each vertex is odd, so $n = |O|$ is even. For example, no 3-regular graph on 7 vertices exists, while the cube graph is 3-regular on 8 vertices.
- **Eulerian paths.** A connected multigraph has an Eulerian trail between two distinct vertices only if exactly those two vertices have odd degree. The handshaking lemma says that the number of odd vertices is 0, 2, 4, and so on, never 1. So a connected multigraph has an Eulerian circuit when $|O| = 0$, an Eulerian trail when $|O| = 2$, and neither when $|O| \ge 4$. See [Euler's theorem on Eulerian graphs](/eulers-theorem-eulerian-graphs/).
- **The Christofides algorithm.** The [Christofides algorithm](/christofides-algorithm/) for the metric travelling salesman problem finds a minimum perfect matching on the odd-degree vertices of a minimum spanning tree. The matching exists because their number is even and the metric gives an edge between each two of them. The [Chinese postman problem](/chinese-postman-problem/) pairs up the odd vertices in the same way.
- **Pairing in a component.** By the stronger form, the odd vertices of each component can be split into pairs within the component, and each pair is joined by a path. Adding an extra edge for each pair makes all degrees even.
- **The second end of a path.** Let $G$ have maximum degree at most 2, and let $v$ have degree 1. Then the component of $v$ is a path, and by the stronger form it holds a second vertex of degree 1, its other end. Papadimitriou (1994) defined the complexity class PPA from this argument, for graphs given implicitly by a circuit, where walking the path can take exponential time. The related class [PPAD](/ppad/) uses the directed version of the argument.

**A worked example.** In the graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$, the degrees are $2, 3, 3, 3, 2, 1$. So $O = \{1, 2, 3, 5\}$ and $|O| = 4$. The graph is connected, so all four are in one component. Adding the two edges $\{1, 2\}$ and $\{3, 5\}$ as parallel edges gives the degrees $2, 4, 4, 4, 2, 2$, all even. The resulting connected multigraph has an Eulerian circuit.

## Tightness

Each even number is possible. For each $n \ge 1$ and each even $k$ with $0 \le k \le n$, the graph on $n$ vertices with the $k/2$ disjoint edges $\{0, 1\}, \{2, 3\}, \ldots, \{k-2, k-1\}$ has exactly $k$ vertices of degree 1 and $n - k$ vertices of degree 0. So the lemma says all that parity can say about $|O|$.

The condition that the graph is finite is needed. The infinite path $0, 1, 2, \ldots$ has exactly one vertex of odd degree, the vertex 0.

## History

The parity fact goes back to Euler's 1736 paper on the bridges of Königsberg, in the form that the number of land regions with an odd number of bridges is even. The textbook form is in West (Section 1.3), in Diestel (Section 1.2) and in Bondy and Murty (Section 1.1). Some authors use the name "handshaking lemma" for the degree sum formula itself, and others for this parity corollary. This site gives the formula on the [handshake lemma](/handshake-lemma/) page and the parity statement here.

## References
