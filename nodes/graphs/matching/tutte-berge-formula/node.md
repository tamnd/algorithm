---
tag: 13ETDE
kind: theorem
slug: tutte-berge-formula
name: Tutte-Berge formula
aliases:
- Tutte-Berge theorem
area: graphs/matching
level: advanced
summary: Gives the maximum matching size as a min-max over vertex subsets.
prereqs: [tutte-theorem, maximum-matching]
see_also: [konig-theorem, gallai-edmonds-decomposition, edmonds-blossom, micali-vazirani-algorithm, perfect-matching, minimum-edge-cover, matching-polytope, strong-duality]
sources:
  - paper: "Claude Berge, Sur le couplage maximum d'un graphe, Comptes Rendus de l'Académie des Sciences Paris 247, 258 to 259 (1958)"
    locator: the whole note (the formula for the deficiency)
  - paper: doi:10.1112/jlms/s1-22.2.107
    title: William T. Tutte, The factorization of linear graphs, Journal of the London Mathematical Society 22(2), 107 to 111 (1947)
    locator: the whole paper (the case of perfect matchings)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (the Berge-Tutte formula, derived from Tutte's theorem)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 24, Cardinality nonbipartite matching (the Tutte-Berge formula)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 10, Maximum Matchings (the Berge-Tutte formula and the Gallai-Edmonds structure theorem)
---

The Tutte-Berge formula gives the size $\nu(G)$ of a [maximum matching](/maximum-matching/) of any graph as a minimum over sets of vertices:
$$\nu(G) = \min_{S \subseteq V} \tfrac12 \bigl(|V| + |S| - q(G - S)\bigr),$$
where $q(G - S)$ is the number of odd components of $G - S$. It extends [Tutte's theorem](/tutte-theorem/), which is the case $\nu(G) = |V|/2$, and it plays for general graphs the part that [Kőnig's theorem](/konig-theorem/) plays for bipartite graphs. A set $S$ that attains the minimum proves that a matching of that size is maximum.

## Statement

Let $G = (V, E)$ be a finite undirected graph, general and without weights, with $n = |V|$. For $S \subseteq V$, let $q(G - S)$ be the number of connected components of $G - S$ with an odd number of vertices. The *deficiency* of $G$ is $\operatorname{def}(G) = n - 2\nu(G)$, the number of vertices that a maximum matching leaves exposed.

**Theorem (Tutte-Berge).**
$$\operatorname{def}(G) = \max_{S \subseteq V} \bigl(q(G - S) - |S|\bigr), \qquad \text{equivalently} \qquad \nu(G) = \min_{S \subseteq V} \tfrac12 \bigl(n + |S| - q(G - S)\bigr).$$

The maximum is at least 0, by $S = \emptyset$ when $n$ is even, and at least 1 when $n$ is odd. For every $S$, $q(G - S) - |S| \equiv n \pmod 2$, since the even components, the odd components and $S$ together have $n$ vertices.

## In plain words

Delete a set of vertices. The graph falls apart into pieces, and some pieces have an odd number of vertices. Each odd piece must leave one of its vertices unpaired, unless that vertex is paired with one of the deleted vertices. Each deleted vertex can rescue at most one odd piece. So the number of unpaired vertices is at least the number of odd pieces minus the number of deleted vertices.

The formula says that the best such count is exactly right: for the right choice of deleted vertices, the largest matching leaves exactly that many vertices unpaired.

## Proof

Write $d = \max_{S} \bigl(q(G - S) - |S|\bigr)$.

**$\operatorname{def}(G) \ge d$.** Let $M$ be a matching and $S \subseteq V$. In each odd component $K$ of $G - S$, the edges of $M$ inside $K$ cover an even number of vertices, so a vertex of $K$ is exposed or matched to a vertex outside $K$, which must be in $S$. At most $|S|$ odd components have a vertex matched into $S$, so at least $q(G - S) - |S|$ vertices are exposed. So $n - 2|M| \ge q(G - S) - |S|$ for every $M$ and $S$.

**$\operatorname{def}(G) \le d$.** By the parity remark, $n + d$ is even. Let $G^*$ be $G$ together with a set $D$ of $d$ new vertices, each joined to every other vertex of $G^*$, old or new. Then $|V(G^*)| = n + d$ is even. We check condition (T) of Tutte's theorem for $G^*$. Let $S^* \subseteq V(G^*)$.

- If $S^* = \emptyset$: when $d \ge 1$, $G^*$ is connected with an even number of vertices, so $q(G^*) = 0$. When $d = 0$, $G^* = G$ and $q(G) \le 0$ by the definition of $d$ with $S = \emptyset$.
- If $S^* \ne \emptyset$ and some vertex of $D$ is not in $S^*$: that vertex is adjacent to all others, so $G^* - S^*$ is connected and $q(G^* - S^*) \le 1 \le |S^*|$.
- If $D \subseteq S^*$: let $S = S^* \setminus D$. Then $G^* - S^* = G - S$, and $q(G - S) \le |S| + d = |S^*|$ by the definition of $d$.

So by [Tutte's theorem](/tutte-theorem/), $G^*$ has a perfect matching $M^*$, with $(n + d)/2$ edges. At most $d$ of its edges have an end in $D$. Deleting them leaves a matching of $G$ with at least $(n + d)/2 - d = (n - d)/2$ edges, so $\operatorname{def}(G) \le d$. $\blacksquare$

**Example: odd cycles.** For the cycle $C_{2k+1}$, $S = \emptyset$ gives one odd component, so $\nu \le \frac12 (2k + 1 - 1) = k$, and a matching with $k$ edges exists. So $\nu = k$.

**Example: a triangle with pendants.** Let $G$ be the triangle $abc$ with the extra edges $ad$ and $ce$, so $n = 5$. For $S = \{a\}$, $G - S$ has the components $\{d\}$ and $\{b, c, e\}$, both odd, so $\nu \le \frac12 (5 + 1 - 2) = 2$. The matching $\{ad, ce\}$ has 2 edges, so $\nu = 2$. Here $S = \emptyset$ gives only $\nu \le 2$ as well, and $S = \{a, c\}$ gives three odd components $\{b\}$, $\{d\}$, $\{e\}$ and the same bound $\frac12 (5 + 2 - 3) = 2$. Several sets can attain the minimum.

**Example: the empty graph.** With no vertices, $S = \emptyset$ gives $\nu = 0$. With $n$ isolated vertices, $S = \emptyset$ gives $q = n$ and $\nu = 0$.

## Consequences

- **[Tutte's theorem](/tutte-theorem/)** is the case $\operatorname{def}(G) = 0$.
- **Certificates of optimality.** A matching $M$ and a set $S$ with $|M| = \frac12 (n + |S| - q(G - S))$ prove each other optimal. [Edmonds' blossom algorithm](/edmonds-blossom/) returns such a pair, so maximum matching has a good characterization in the sense of Edmonds.
- **The [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/).** Let $D(G)$ be the vertices exposed by some maximum matching, $A(G)$ their neighbours outside $D(G)$, and $C(G)$ the rest. Then $S = A(G)$ attains the minimum for every graph, and the components of $G - A(G)$ inside $D(G)$ are factor-critical.
- **Gallai's identity.** With $\rho(G) = n - \nu(G)$ for graphs without isolated vertices, the formula also gives a min-max description of the [minimum edge cover](/minimum-edge-cover/).
- **Linear programming.** The formula is a form of [strong duality](/strong-duality/) for the [matching polytope](/matching-polytope/): Edmonds' odd-set constraints and the Cunningham-Marsh theorem give a dual solution of the same value that is built from $S$ and the odd components.

## Tightness

The two sides are equal for every graph, so the formula cannot be improved. What fails is the bipartite min-max: replacing the right side by the smallest [vertex cover](/vertex-cover/) gives only $\nu \le \tau \le 2\nu$, and the triangle has $\nu = 1 < 2 = \tau$. Restricting $S$ to small sets also fails. For the graph $G_k$ made of $K_k$ and $k + 2$ further vertices joined to all of $K_k$, the minimum is attained only by sets $S$ with $|S| \ge k$: it gives $\nu = \frac12 (2k + 2 + k - (k + 2)) = k$, while every $S$ with $|S| < k$ gives a bound of at least $k + 1$.

## History

William Tutte proved the perfect matching case in 1947. Claude Berge stated and proved the formula for the deficiency in a 1958 note in the Comptes Rendus. Gallai in 1963 and 1964 and Edmonds in 1965 described the canonical minimizer, now called the Gallai-Edmonds decomposition, and Edmonds' algorithm made the formula constructive.

## References
