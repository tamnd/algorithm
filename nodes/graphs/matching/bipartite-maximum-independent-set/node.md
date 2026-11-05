---
tag: RDW7Z3
kind: problem
slug: bipartite-maximum-independent-set
name: Maximum independent set in a bipartite graph
aliases:
- Maximum independent set in bipartite graph
area: graphs/matching
level: core
summary: Problem of finding the largest set of vertices with no edge between them in a bipartite graph, derived from a maximum matching via König's theorem.
prereqs: [bipartite-matching, independent-set, konig-theorem]
see_also: [maximum-independent-set, vertex-cover, gallai-identity, hopcroft-karp, min-cut-problem, edge-cover, dilworth-theorem, perfect-graph]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 16.5, Finding a minimum-size vertex cover, Section 17.4, Finding a minimum-size w-vertex cover, and Chapter 19, Bipartite edge cover and stable set
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Kőnig's theorem, Gallai's theorem, and independence in bipartite graphs)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 1, Matchings in bipartite graphs (Kőnig's minimax theorem and its consequences)
---

The maximum independent set problem in a [bipartite graph](/bipartite-graph/) asks for a largest set of vertices with no edge between any two of them. In general graphs this is the [NP-hard](/np-complete/) [maximum independent set](/maximum-independent-set/) problem, but in bipartite graphs it has an exact polynomial-time solution: a maximum independent set is the complement of a minimum [vertex cover](/vertex-cover/), and by [Kőnig's theorem](/konig-theorem/) a minimum vertex cover comes from a maximum matching. So its size is $n - \nu(G)$, and it can be found in $O(m\sqrt n)$ time. The graph is bipartite; the unweighted case uses matching, and the vertex-weighted case uses a minimum cut.

## In plain words

You have two groups of people, and some pairs across the groups do not get along. You want to invite as many people as possible to a party so that no two guests dislike each other. In a general network of dislikes this is a very hard puzzle. With two groups it is easy.

First pair up as many disliking pairs as you can, so that nobody is in two pairs. Each pair can send at most one guest, so the number of guests is at most the number of people minus the number of pairs. A short search from the people left without a pair then shows which person of each pair to invite, and this reaches that number exactly.

## Definition

**Input.** A finite bipartite graph $G = (X \cup Y, E)$, every edge joining $X$ to $Y$, with $n = |X| + |Y|$ and $m = |E|$.

**Output.** A set $I \subseteq X \cup Y$ such that no edge has both ends in $I$, of the largest size $\alpha(G)$.

**The formula.** For every bipartite graph,

$$\alpha(G) = n - \tau(G) = n - \nu(G),$$

where $\tau(G)$ is the least size of a vertex cover and $\nu(G)$ the largest size of a matching. The first equality holds in every graph, because the complement of an independent set is a vertex cover and conversely ([Gallai's identity](/gallai-identity/), part 1). The second is [Kőnig's theorem](/konig-theorem/). If $G$ has no isolated vertex, [Gallai's identity](/gallai-identity/) also gives $\alpha(G) = \rho(G)$, the size of a minimum [edge cover](/edge-cover/).

**Kőnig's construction.** Let $M$ be a maximum matching. Let $Z$ be the set of vertices that are ends of [$M$-alternating paths](/alternating-path/) starting at a free vertex of $X$, the free vertices of $X$ included. Then

$$C = (X \setminus Z) \cup (Y \cap Z), \qquad I = (X \cap Z) \cup (Y \setminus Z)$$

are a minimum vertex cover and a maximum independent set. *Proof.* (a) *$I$ is independent.* Suppose $xy \in E$ with $x \in X \cap Z$ and $y \in Y \setminus Z$. If $xy \in M$, then $x$ is not free, so it is reached by an alternating path whose last edge is matched, and that edge is $xy$; so $y \in Z$, a contradiction. If $xy \notin M$, take an alternating path $P$ from a free vertex of $X$ to $x$; it ends with a matched edge or has no edge, and $y \notin P$ because $y \notin Z$, so $P$ followed by $xy$ is alternating and $y \in Z$, a contradiction. (b) *$|C| = |M|$.* Each $y \in Y \cap Z$ is matched, since otherwise an alternating path to $y$ would be augmenting, against [Berge's lemma](/berge-lemma/); its partner is in $X \cap Z$, reached by the matched edge. Each $x \in X \setminus Z$ is matched, since every free vertex of $X$ is in $Z$; its partner $y$ is not in $Z$, since otherwise $x$ would be reached through $y$. So every vertex of $C$ is matched, and no edge of $M$ has both ends in $C$. Thus $|C| \le |M|$, and as $C = (X \cup Y) \setminus I$ is a vertex cover by (a), $|C| \ge \tau(G) \ge \nu(G) = |M|$. So $|C| = \tau(G)$, and $I$ has $n - \tau(G) = \alpha(G)$ vertices. $\square$

## Variants

- **Vertex weights.** Each vertex $v$ has a weight $w(v) \ge 0$; find an independent set of largest total weight. It is the complement of a minimum-weight vertex cover, which is a [minimum cut](/min-cut-problem/): add a source $s$ with an arc of capacity $w(x)$ to each $x \in X$, a sink $t$ with an arc of capacity $w(y)$ from each $y \in Y$, and arcs of infinite capacity from $x$ to $y$ for each edge $xy$. A finite cut $(S, \bar S)$ cuts exactly the arcs of the vertices in $(X \setminus S) \cup (Y \cap S)$, which is a vertex cover, and each vertex cover arises in this way. So a [maximum flow](/max-flow-problem/) solves the weighted problem.
- **Decision.** Is $\alpha(G) \ge k$? Equivalent to $\nu(G) \le n - k$.
- **Minimum vertex cover.** The complementary problem, solved by the same construction.
- **General graphs.** [Maximum independent set](/maximum-independent-set/) in a general graph is NP-hard, and hard to approximate. The bipartite case is easy because of Kőnig's theorem $\nu = \tau$. Bipartite graphs are also [perfect graphs](/perfect-graph/), a wider class in which a maximum independent set can still be found in polynomial time, but by much heavier methods.

## Examples

**Five people and five tasks.** Let $X = \{A, B, C, D, E\}$ and $Y = \{1, 2, 3, 4, 5\}$, with $A$, $B$, $C$ each adjacent to 1 and 2, $D$ adjacent to 3 and 4, and $E$ adjacent to 4 and 5. Here $n = 10$.

| step | result |
|---|---|
| maximum matching $M$ | $\{A1, B2, D3, E4\}$, $\nu = 4$ |
| free vertices | $C$ in $X$, and 5 in $Y$ |
| alternating search from $C$ | $C \to 1 \Rightarrow A$, $C \to 2 \Rightarrow B$; from $A$ and $B$ only 1 and 2 again |
| $Z$ | $\{C, 1, 2, A, B\}$ |
| $C = (X \setminus Z) \cup (Y \cap Z)$ | $\{D, E, 1, 2\}$, a minimum vertex cover of size 4 |
| $I = (X \cap Z) \cup (Y \setminus Z)$ | $\{A, B, C, 3, 4, 5\}$, independent, of size $6 = 10 - 4$ |

**Small graphs.**

| graph | $n$ | $\nu$ | $\alpha$ | a maximum independent set |
|---|---|---|---|---|
| no edges, 4 vertices | 4 | 0 | 4 | all vertices |
| empty graph, no vertices | 0 | 0 | 0 | $\emptyset$ |
| path $P_5$ | 5 | 2 | 3 | $v_1, v_3, v_5$ |
| even cycle $C_6$ | 6 | 3 | 3 | one side |
| $K_{3,5}$ | 8 | 3 | 5 | the side of size 5 |
| star $K_{1,4}$ | 5 | 1 | 4 | the four leaves |

**Not bipartite.** In the 5-cycle, $\nu = 2$ but $\alpha = 2 \ne 5 - 2$. The formula needs bipartiteness: here $\tau = 3 > \nu$.

## Known algorithms

- Compute a maximum matching by [Hopcroft-Karp](/hopcroft-karp/) in $O(m\sqrt n)$ time, or by [Kuhn's algorithm](/kuhn-algorithm/) in $O(nm)$ time, then run one alternating search from all free vertices of $X$ in $O(n + m)$ time and output $I$. The search is a [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) that follows unmatched edges from $X$ to $Y$ and matched edges from $Y$ to $X$.
- For vertex weights, a maximum flow on the network of the Variants section, by any [max flow](/max-flow-problem/) algorithm, followed by the minimum cut.
- Any algorithm for [bipartite matching](/bipartite-matching/) transfers its bound to this problem, with $O(n + m)$ extra time.

## Bounds

- **Upper bound.** The same as for bipartite matching plus $O(n + m)$: $O(m\sqrt n)$ by a combinatorial algorithm, and $m^{1 + o(1)}$ through [almost-linear max flow](/almost-linear-max-flow/).
- **Lower bound.** $\Omega(n + m)$ in the adjacency-list model, to read the graph.
- **Equivalence.** The size $\alpha(G)$ and the size $\nu(G)$ determine each other by $\alpha = n - \nu$, so computing one is as hard as computing the other, up to $O(n)$ time. Finding the set from a maximum matching costs $O(n + m)$.

## Reductions

- **To bipartite matching.** As above, through Kőnig's construction, with $O(n + m)$ extra time.
- **From bipartite matching (the size).** $\nu(G) = n - \alpha(G)$.
- **Maximum antichain in a partial order.** Split each element $p$ into $p^{\text{out}} \in X$ and $p^{\text{in}} \in Y$, and join $p^{\text{out}}$ to $q^{\text{in}}$ when $p < q$. The elements $p$ with both copies in the independent set $I$ form a maximum antichain, and the minimum chain cover has $N - \nu$ chains for $N$ elements. This is the constructive proof of [Dilworth's theorem](/dilworth-theorem/).

## Applications

- Placing as many non-attacking pieces as possible on a board with holes, when the attack graph is bipartite, as for knights or for rooks on a board split into row and column segments.
- Selecting a largest set of mutually compatible items when conflicts only occur between two classes of items, never inside a class.
- Computing the width of a partial order, through the antichain reduction.
- Image segmentation and project selection, through the weighted version and the minimum cut.

## References
