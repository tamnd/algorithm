---
tag: 5VR232
kind: theorem
slug: tutte-theorem
name: Tutte's theorem
aliases:
- Tutte's perfect matching theorem
area: graphs/matching
level: advanced
summary: A graph has a perfect matching iff deleting any set S leaves at most |S| odd components.
prereqs: [perfect-matching, connected-components]
see_also: [tutte-berge-formula, petersens-theorem, hall-theorem, konig-theorem, gallai-edmonds-decomposition, tutte-matrix, edmonds-blossom, maximum-matching]
sources:
  - paper: doi:10.1112/jlms/s1-22.2.107
    title: William T. Tutte, The factorization of linear graphs, Journal of the London Mathematical Society 22(2), 107 to 111 (1947)
    locator: the whole paper (the theorem, with a proof by Pfaffians)
  - paper: "László Lovász, Three short proofs in graph theory, Journal of Combinatorial Theory, Series B 19(3), 269 to 271 (1975)"
    locator: the proof of the 1-factor theorem by an edge-maximal counterexample
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 2.2, Matching in general graphs, Theorem 2.2.1 (Tutte 1947) and its proof
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (Tutte's 1-factor theorem)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing
    locator: Chapter 3, Size and structure of maximum matchings
---

Tutte's theorem gives a necessary and sufficient condition for a general graph to have a [perfect matching](/perfect-matching/). For a set $S$ of vertices, let $q(G - S)$ be the number of [connected components](/connected-components/) of $G - S$ with an odd number of vertices. The theorem says that $G$ has a perfect matching if and only if $q(G - S) \le |S|$ for every $S$. It is the general-graph form of [Hall's theorem](/hall-theorem/), and the [Tutte-Berge formula](/tutte-berge-formula/) extends it to the size of a [maximum matching](/maximum-matching/).

## Statement

Let $G = (V, E)$ be a finite undirected graph, general (odd cycles are allowed) and without weights. Parallel edges and self-loops do not matter for matchings and may be deleted. For $S \subseteq V$, $G - S$ is the graph obtained by deleting the vertices of $S$ and their edges, and $q(G - S)$ is the number of its components with an odd number of vertices.

**Theorem (Tutte, 1947).** $G$ has a perfect matching if and only if
$$q(G - S) \le |S| \quad \text{for every } S \subseteq V. \tag{T}$$

A set $S$ with $q(G - S) > |S|$ is a *Tutte set*, or a barrier; it is a short certificate that no perfect matching exists. Condition (T) with $S = \emptyset$ says that each component of $G$ has an even number of vertices.

## In plain words

You want to split all the people at a party into pairs of friends. Pick some people and send them home for a moment. The others fall into groups that do not know each other. A group with an odd number of people cannot pair inside itself, so at least one of its members must pair with someone who was sent home. Different odd groups need different people from home. So if you can send a few people home and leave more odd groups than people at home, no full pairing exists.

The theorem says that this is the only reason. If no choice of people to send home leaves too many odd groups, then everyone can be paired.

## Proof

**Necessity.** Let $M$ be a perfect matching and $S \subseteq V$. Let $K$ be an odd component of $G - S$. The edges of $M$ inside $K$ cover an even number of its vertices, so some vertex $v \in K$ has its mate outside $K$. There is no edge from $K$ to another component of $G - S$, so the mate is in $S$. Different odd components give different vertices of $S$, since $M$ is a matching. So $q(G - S) \le |S|$.

**Sufficiency.** This is the proof of Lovász (1975). Suppose that $G$ satisfies (T) but has no perfect matching.

*Step 1. We may assume that $G$ is edge-maximal.* Adding an edge $e$ between two vertices does not increase $q(G - S)$ for any $S$: if $e$ joins two components of $G - S$, two odd components become one even component, an odd and an even component become one odd component, and two even ones become one even one; otherwise the components do not change. So adding edges keeps (T). Add edges one at a time as long as no perfect matching appears. The result is a graph $G' \supseteq G$ on $V$ that satisfies (T), has no perfect matching, and has a perfect matching after the addition of any new edge. By (T) with $S = \emptyset$, $|V|$ is even.

*Step 2. Let $S$ be the set of vertices of $G'$ that are adjacent to all other vertices. If every component of $G' - S$ is a complete graph, $G'$ has a perfect matching.* By (T), $G' - S$ has at most $|S|$ odd components. Choose one vertex in each odd component and match it to its own vertex of $S$; this is possible because each vertex of $S$ is adjacent to every vertex. The rest of each component is a complete graph with an even number of vertices, so it has a perfect matching. The vertices of $S$ not yet used are pairwise adjacent, and their number is even because $|V|$ and the number of vertices already matched are both even. So they have a perfect matching too. Together this is a perfect matching of $G'$, against the assumption. So some component of $G' - S$ is not complete.

*Step 3. A component that is not complete gives a contradiction.* Let $K$ be a component of $G' - S$ that is not complete. Two nonadjacent vertices of $K$ at the least distance are at distance 2, so there are $a, b, c \in K$ with $ab, bc \in E(G')$ and $ac \notin E(G')$. Because $b \notin S$, there is a vertex $d$ with $bd \notin E(G')$. By the maximality of $G'$, the graph $G' + ac$ has a perfect matching $M_1$, and $G' + bd$ has a perfect matching $M_2$. Then $ac \in M_1$ and $bd \in M_2$, since $G'$ itself has no perfect matching.

Let $P$ be a longest path in $G'$ that starts at $d$ with an edge of $M_1$ and whose edges are alternately in $M_1$ and in $M_2$. Let $v$ be its last vertex.

- *If the last edge of $P$ is in $M_1$*, then $v = b$. Otherwise the $M_2$-edge at $v$ is an edge of $G'$, since the only edge of $M_2$ outside $G'$ is $bd$. Its other end is not on $P$: the interior vertices of $P$ already have their $M_2$-edge on $P$, and the $M_2$-edge of $d$ is $bd$. So $P$ could be extended, which is not possible. Put $C = P + bd$.
- *If the last edge of $P$ is in $M_2$*, then $v \in \{a, c\}$. Otherwise the $M_1$-edge at $v$ is in $G'$, as the only edge of $M_1$ outside $G'$ is $ac$, and $P$ could be extended in the same way. Also $b \notin P$: the vertex $b$ cannot be interior, as its $M_2$-edge $bd$ is not in $G'$, and it is not the last vertex here. Put $C = P + vb + bd$, where $vb \in E(G')$.

In both cases $C$ is a cycle of even length whose edges alternate between $M_2$ and edges not in $M_2$, and every vertex of $C$ is covered by an edge of $M_2 \cap C$. The edges of $C \setminus M_2$ are the $M_1$-edges of $P$, plus $vb$ in the second case; all of them are in $G'$. So $M_2 \oplus C$ is a perfect matching that does not use $bd$, and all its edges are in $G'$. This contradicts the choice of $G'$. $\blacksquare$

**Example.** Let $c$ be a vertex joined by one edge to one vertex of each of three disjoint triangles. The graph is connected and has 10 vertices. For $S = \{c\}$, $G - S$ is three triangles, so $q(G - S) = 3 > 1 = |S|$, and there is no perfect matching. For the 5-cycle, $S = \emptyset$ already gives one odd component. For the 6-cycle, every $S$ satisfies (T), and indeed every other edge is a perfect matching.

## Consequences

- **The [Tutte-Berge formula](/tutte-berge-formula/).** The size of a maximum matching is $\nu(G) = \frac12 \min_{S} \bigl(|V| + |S| - q(G - S)\bigr)$. It follows by applying the theorem to $G$ joined with a complete graph on the right number of new vertices.
- **[Petersen's theorem](/petersens-theorem/).** Every bridgeless 3-regular graph has a perfect matching. The proof counts the edges between $S$ and the odd components of $G - S$.
- **Regular graphs.** More generally, every $k$-regular, $(k - 1)$-edge-connected graph with an even number of vertices has a perfect matching.
- **Hall's theorem.** For a bipartite graph with $|L| = |R|$, Hall's condition implies (T), so Tutte's theorem contains [Hall's theorem](/hall-theorem/).
- **Good characterization.** The perfect matching problem is in $\mathsf{NP} \cap \mathsf{coNP}$: a perfect matching proves "yes", and a Tutte set proves "no". [Edmonds' algorithm](/edmonds-blossom/) finds one or the other in polynomial time, and the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/) gives a canonical Tutte set.
- **Factors.** Tutte later proved a theorem of the same kind for $f$-factors, spanning subgraphs with given degrees; see the [f-factor problem](/f-factor-problem/).

## Tightness

The condition must hold for all $S$, and large sets cannot be omitted. Let $G_k$ be a complete graph $K_k$ with $k + 2$ further vertices, each joined to all vertices of the $K_k$ and to nothing else. It has $2k + 2$ vertices. For $S = V(K_k)$, $q(G - S) = k + 2 > k$, so $G_k$ has no perfect matching. But for every $S$ with $|S| < k$, $G - S$ still has a vertex of the $K_k$ adjacent to all other remaining vertices, so it is connected, and $q(G - S) \le 1 \le |S|$ when $S \ne \emptyset$, while $q(G) = 0$. So every Tutte set of $G_k$ has at least $k$ vertices.

The counting in the necessity proof is also sharp: for a graph with a perfect matching $M$ and a set $S$ with $q(G - S) = |S|$, each vertex of $S$ is matched into a different odd component, as in the star $K_{1,1}$ with $S$ one end.

## History

William Tutte proved the theorem in 1947, in the paper "The factorization of linear graphs", using Pfaffians of skew-symmetric matrices; that matrix is now called the [Tutte matrix](/tutte-matrix/). Many shorter proofs followed. Gallai and Anderson gave combinatorial proofs, and the proof above, by an edge-maximal counterexample, is due to László Lovász (1975). Claude Berge derived the formula for the size of a maximum matching in 1958. Edmonds' blossom algorithm of 1965 gave an algorithmic proof.

## References
