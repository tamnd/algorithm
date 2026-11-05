---
tag: NRXHJB
kind: theorem
slug: perfect-graph-theorem
name: Perfect graph theorem
aliases:
- Lovasz perfect graph theorem
area: graphs/coloring-and-cliques
level: advanced
summary: A graph is perfect if and only if its complement is perfect.
prereqs: [perfect-graph, complement-graph, independence-number]
see_also: [strong-perfect-graph-theorem, lovasz-theta-function, konig-theorem, dilworth-theorem, chordal-graph, clique-cover]
sources:
  - paper: doi:10.1016/0012-365X(72)90006-4
    title: L. Lovász, Normal hypergraphs and the perfect graph conjecture, Discrete Mathematics 2(3), 253 to 267 (1972)
    locator: the proof of the weak perfect graph conjecture by the replication lemma
  - paper: doi:10.1016/0095-8956(72)90045-7
    title: L. Lovász, A characterization of perfect graphs, Journal of Combinatorial Theory, Series B 13(2), 95 to 98 (1972)
    locator: the characterization by ω(H) α(H) ≥ |V(H)| for all induced subgraphs H
  - paper: "D. R. Fulkerson, Anti-blocking polyhedra, Journal of Combinatorial Theory, Series B 12, 50 to 71 (1972)"
    locator: the polyhedral approach to the perfect graph conjecture and the replication lemma
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.5, Perfect graphs (the replication lemma and the perfect graph theorem)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 3, Perfect graphs (the perfect graph theorem and the characterization by ω α ≥ n)
---

The perfect graph theorem says that a graph is [perfect](/perfect-graph/) if and only if its [complement](/complement-graph/) is perfect. In other words, if the [chromatic number](/chromatic-number/) equals the clique number in every induced subgraph, then the [independence number](/independence-number/) equals the least number of cliques needed to cover the vertices, in every induced subgraph. Berge conjectured it in 1961 and Lovász proved it in 1972; it was known as the weak perfect graph conjecture, to tell it apart from the strong one proved in 2006.

## Statement

For a graph $H$, let $\omega(H)$ be the clique number, $\chi(H)$ the chromatic number, $\alpha(H)$ the independence number, and $\theta(H)$ the **clique cover number**, the least number of cliques whose union is $V(H)$. Since cliques of $H$ are independent sets of $\overline{H}$, we have $\theta(H) = \chi(\overline{H})$ and $\alpha(H) = \omega(\overline{H})$. A graph is perfect when $\chi(G[S]) = \omega(G[S])$ for every $S \subseteq V(G)$.

**Theorem (Lovász 1972).** For every finite simple graph $G$, the following are equivalent:

1. $G$ is perfect.
2. $\overline{G}$ is perfect, that is, $\theta(G[S]) = \alpha(G[S])$ for every $S \subseteq V(G)$.
3. $\omega(G[S])\, \alpha(G[S]) \ge |S|$ for every $S \subseteq V(G)$.

The proof below shows that 1 implies 2. Applying this to $\overline{G}$ gives the converse, since $\overline{\overline{G}} = G$. The equivalence with 3 is the second 1972 paper of Lovász.

## In plain words

In a perfect graph, the number of colors you need is always just the size of the biggest group of mutually linked points, and this stays true when you delete any points.

The theorem says that the same graph then has a second, mirror property. The biggest set of points with no links between them always equals the fewest linked groups that together contain every point. Again this holds after deleting any points. Swapping "linked" and "not linked" turns one property into the other, so a graph is perfect exactly when its mirror image is.

## Proof

All graphs are finite and simple. Induced subgraphs of a perfect graph are perfect, by definition.

**Replication lemma.** Let $G$ be perfect and $x \in V(G)$. Let $G \circ x$ be $G$ with a new vertex $x'$ adjacent to $x$ and to every neighbor of $x$. Then $G \circ x$ is perfect.

*Proof of the lemma.* By induction on $|V(G)|$. A proper induced subgraph of $G \circ x$ is either an induced subgraph of $G$ (up to renaming $x'$ as $x$) or $H \circ x$ for a proper induced subgraph $H$ of $G$ containing $x$, so it is perfect by induction. It remains to show $\chi(G \circ x) \le \omega(G \circ x)$. Let $\omega = \omega(G)$.

- If $x$ lies in a clique of size $\omega$ in $G$, then $\omega(G \circ x) = \omega + 1$, and giving $x'$ a new color in an $\omega$-coloring of $G$ uses $\omega + 1$ colors.
- Otherwise $\omega(G \circ x) = \omega$. Take a coloring of $G$ with $\omega$ colors and let $A$ be the class of $x$. Every clique $K$ of size $\omega$ in $G$ meets every color class, and $x \notin K$, so $K$ meets $A \setminus \{x\}$. Hence $\omega(G - (A \setminus \{x\})) \le \omega - 1$, and since $G - (A \setminus \{x\})$ is perfect, it has a coloring with $\omega - 1$ colors. The set $(A \setminus \{x\}) \cup \{x'\}$ is independent, because $x'$ is adjacent only to $x$ and to $N(x)$, and $A$ is independent and contains $x$. Give it one more color. This colors $G \circ x$ with $\omega$ colors. $\square$

Repeating the lemma and deleting vertices, we get: if $G$ is perfect and $h : V(G) \to \{0, 1, 2, \ldots\}$, then the graph $G_h$ obtained by replacing each vertex $x$ by a clique of $h(x)$ vertices (with all edges between the cliques of two adjacent vertices) is perfect. A vertex with $h(x) = 0$ is deleted, which keeps perfection.

**Key claim.** If $G$ is perfect and has at least one vertex, then some clique of $G$ meets every maximum independent set of $G$.

*Proof of the claim.* Suppose not. Let $\mathcal{K}$ be the family of all nonempty cliques of $G$. For each $K \in \mathcal{K}$ choose a maximum independent set $A_K$ with $A_K \cap K = \emptyset$. For each vertex $x$ let $h(x)$ be the number of cliques $K \in \mathcal{K}$ with $x \in A_K$, and form $G_h$, which is perfect. Write $\alpha = \alpha(G)$ and $N = |\mathcal{K}|$.

- $|V(G_h)| = \sum_x h(x) = \sum_{K} |A_K| = N \alpha$.
- An independent set of $G_h$ takes at most one copy of each vertex, and the vertices it comes from are independent in $G$, so $\alpha(G_h) \le \alpha$.
- A clique of $G_h$ lies in the blow-up of a clique $X \in \mathcal{K}$ of $G$, so its size is at most $\sum_{x \in X} h(x) = \sum_{K} |X \cap A_K|$. Each term is at most 1, since a clique and an independent set share at most one vertex, and the term for $K = X$ is 0. So $\omega(G_h) \le N - 1$.

Every color class of $G_h$ is independent, so $\chi(G_h) \ge |V(G_h)| / \alpha(G_h) \ge N \alpha / \alpha = N > \omega(G_h)$. This contradicts the perfection of $G_h$. $\square$

**The theorem.** We show $\theta(G) = \alpha(G)$ for every perfect $G$, by induction on $|V(G)|$. The case of no vertices is trivial. The bound $\theta(G) \ge \alpha(G)$ always holds, since a clique contains at most one vertex of an independent set. For the other bound, take a clique $K$ that meets every maximum independent set. Then $\alpha(G - K) = \alpha(G) - 1$, and $G - K$ is perfect, so by induction it is covered by $\alpha(G) - 1$ cliques. Adding $K$ covers $G$ with $\alpha(G)$ cliques.

Every induced subgraph $G[S]$ is perfect, so $\theta(G[S]) = \alpha(G[S])$, that is, $\chi(\overline{G}[S]) = \omega(\overline{G}[S])$ for every $S$. So $\overline{G}$ is perfect. $\blacksquare$

## Consequences

- **Dilworth's theorem.** The comparability graph of a poset is perfect: a longest chain has as many elements as the least number of antichains that cover the poset (Mirsky). By the theorem its complement is perfect, which says that the largest antichain equals the least number of chains that cover the poset. This is [Dilworth's theorem](/dilworth-theorem/).
- **König's theorem.** Bipartite graphs are perfect, so their complements are perfect. For a bipartite graph without isolated vertices, this says that $\alpha$ equals the least number of edges and vertices that cover $V$, which is equivalent to [König's theorem](/konig-theorem/) by Gallai's identities.
- **Chordal graphs.** Chordal graphs are perfect, so a chordal graph can be covered by $\alpha$ cliques, and this cover is found greedily along a [perfect elimination ordering](/perfect-elimination-ordering/).
- **Polyhedra.** $G$ is perfect if and only if the stable set polytope of $G$ is described by the nonnegativity constraints and the inequalities $\sum_{v \in K} x_v \le 1$ for the cliques $K$ (Fulkerson; Chvátal 1975). This is the basis for optimizing over perfect graphs with the [Lovász theta function](/lovasz-theta-function/).
- **Self-complementary characterizations.** Condition 3 is symmetric in $\omega$ and $\alpha$, which explains at a glance why perfection is closed under complement.

## Tightness

The theorem needs the condition on all induced subgraphs. Let $G$ be a 5-cycle plus a disjoint triangle. Then $\chi(G) = \omega(G) = 3$. Its complement is the 5-cycle joined to an independent set of 3 vertices, with $\omega(\overline{G}) = 3$ and $\chi(\overline{G}) = 4$. So the equality $\chi = \omega$ for one graph does not pass to the complement; it is the hereditary version that does. In the same way, $\omega(G)\, \alpha(G) \ge |V(G)|$ for $G$ alone is not enough: this example has $3 \cdot 3 \ge 8$ but is not perfect.

The theorem also does not say which graphs are perfect. That is the [strong perfect graph theorem](/strong-perfect-graph-theorem/): a graph is perfect if and only if it has no odd hole and no odd antihole, which implies the perfect graph theorem at once, because the complement of an odd hole is an odd antihole.

## History

Claude Berge introduced perfect graphs in 1961 and stated two conjectures: that the complement of a perfect graph is perfect (the weak conjecture) and that the graphs with no odd hole and no odd antihole are perfect (the strong conjecture). Fulkerson developed the theory of anti-blocking polyhedra to attack the weak conjecture and reduced it to the replication lemma, but did not finish the proof. László Lovász proved the weak conjecture in 1972, and in a second paper the same year gave the characterization by $\omega \alpha \ge n$. The strong conjecture was proved by Chudnovsky, Robertson, Seymour and Thomas, announced in 2002 and published in 2006.

## References
