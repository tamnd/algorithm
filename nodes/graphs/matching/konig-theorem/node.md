---
tag: HZG6X9
kind: theorem
slug: konig-theorem
name: Kőnig's theorem
aliases:
- Kőnig-Egerváry theorem
area: graphs/matching
level: core
summary: In a bipartite graph the maximum matching size equals the minimum vertex cover size.
prereqs: [bipartite-graph, vertex-cover, augmenting-path]
see_also: [hall-theorem, kuhn-algorithm, bipartite-matching, bipartite-maximum-independent-set, gallai-identity, menger-theorem, max-flow-min-cut-theorem, tutte-berge-formula]
sources:
  - paper: "Dénes Kőnig, Gráfok és mátrixok, Matematikai és Fizikai Lapok 38, 116 to 119 (1931)"
    locator: the whole paper (the theorem for bipartite graphs and its matrix form)
  - paper: "Jenő Egerváry, Matrixok kombinatorikus tulajdonságairól, Matematikai és Fizikai Lapok 38, 16 to 28 (1931)"
    locator: the whole paper (the weighted form)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (the Kőnig-Egerváry theorem and its proof by alternating paths)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 2.1, Matching in bipartite graphs (Kőnig's theorem, with the proof that picks one end of each matching edge)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 16, Cardinality bipartite matching and vertex cover (Kőnig's matching theorem, its proofs and history)
---

Kőnig's theorem says that in a [bipartite graph](/bipartite-graph/) the largest size of a matching equals the least size of a [vertex cover](/vertex-cover/). It is the first min-max theorem of combinatorics. The proof below is constructive: from a maximum matching, a search along [alternating paths](/alternating-path/) gives a cover of the same size in linear time, and the matching and the cover prove each other optimal. It fails for graphs with odd cycles, where the [Tutte-Berge formula](/tutte-berge-formula/) takes its place.

## Statement

Let $G = (L \cup R, E)$ be a finite [bipartite graph](/bipartite-graph/), without weights, with every edge between $L$ and $R$; parallel edges are allowed. A *matching* is a set of edges with no common end, and $\nu(G)$ is the largest size of a matching. A *vertex cover* is a set $C \subseteq L \cup R$ that contains an end of each edge, and $\tau(G)$ is the least size of a vertex cover.

**Theorem (Kőnig, 1931).** $\nu(G) = \tau(G)$.

**Matrix form.** In a 0-1 matrix, the largest number of 1 entries with no two in the same row or column equals the least number of rows and columns that together contain all the 1 entries. (Rows are $L$, columns are $R$, and a 1 entry is an edge.)

## In plain words

A matching is a set of pairs where nobody is in two pairs. A cover is a set of people that touches every possible pair. Each pair of a matching needs its own member of the cover, so a cover is never smaller than a matching. For a graph with two sides, the theorem says that the two numbers meet: the best matching and the smallest cover always have the same size.

So to prove that a matching is the largest, you show a cover of the same size, and to prove that a cover is the smallest, you show a matching of the same size. With three people who all know each other, the best matching has one pair but the smallest cover has two people. That is why the graph must have two sides.

## Proof

**The easy inequality.** Let $M$ be a matching and $C$ a vertex cover. Each edge of $M$ has an end in $C$, and the edges of $M$ have no common end, so these ends are different. So $|C| \ge |M|$, and $\tau(G) \ge \nu(G)$.

**The hard inequality.** Let $M$ be a maximum matching. An *alternating path* is a path whose edges are alternately outside and inside $M$. Let $U$ be the set of vertices of $L$ that $M$ leaves exposed. Let $Z$ be the set of vertices that are the last vertex of an alternating path that starts at a vertex of $U$ with an edge outside $M$; the paths of length 0 count, so $U \subseteq Z$. Put $S = Z \cap L$ and $T = Z \cap R$.

On such a path $P = u_0 w_1 u_1 w_2 u_2 \ldots$ with $u_0 \in U$, the vertices alternate between $L$ and $R$, because $G$ is bipartite. The first edge is outside $M$, so each step from $L$ to $R$ is outside $M$ and each step from $R$ to $L$ is in $M$.

*Claim 1. Each vertex $y \in T$ is matched, and its mate is in $S$.* Let $P$ be an alternating path from $u_0 \in U$ to $y$. Its last edge goes from $L$ to $R$, so it is outside $M$. If $y$ were exposed, $P$ would join two different exposed vertices, and $M \oplus P$ would be a matching with one more edge, against the choice of $M$. So $y$ has a mate $x$. The vertex $x$ is not on $P$: each vertex of $L$ on $P$ other than $u_0$ is entered by its own matching edge from the vertex before it, which is not $y$ because $y$ is last, and $u_0$ is exposed. So $P$ followed by the edge $yx \in M$ is an alternating path from $u_0$, and $x \in S$.

*Claim 2. Each neighbour of a vertex of $S$ is in $T$.* Let $x \in S$, with an alternating path $P$ from $u_0 \in U$ to $x$, and let $y$ be a neighbour of $x$. If $xy \in M$, then $x \ne u_0$, as $u_0$ is exposed, and $y$ is the vertex before $x$ on $P$, so $y \in T$. If $y$ is on $P$, then $y \in T$ as well. Otherwise $xy \notin M$, and $P$ followed by $xy$ is an alternating path from $u_0$: the last edge of $P$ is in $M$ when $x \ne u_0$, and $P$ has no edge when $x = u_0$. So $y \in T$.

*Claim 3. $C = (L \setminus S) \cup T$ is a vertex cover.* Let $xy$ be an edge with $x \in L$ and $y \in R$. If $x \notin S$, then $x \in C$. If $x \in S$, then $y \in T \subseteq C$ by Claim 2.

*Claim 4. $|C| \le |M|$.* Each vertex of $T$ is matched, by Claim 1. Each vertex of $L \setminus S$ is matched, because the exposed vertices of $L$ are in $U \subseteq S$. So we can map each vertex of $C$ to its matching edge. No edge $xy \in M$ has both ends in $C$: if $y \in T$, then $x \in S$ by Claim 1, so $x \notin C$. So the map is injective, and $|C| \le |M|$.

By Claims 3 and 4, $\tau(G) \le |M| = \nu(G)$. With the easy inequality, $\nu(G) = \tau(G)$. $\blacksquare$

The proof uses only that $M$ has no [augmenting path](/augmenting-path/) from $U$, so it also proves the bipartite case of [Berge's lemma](/berge-lemma/). The set $Z$ is what a [breadth-first search](/breadth-first-search/) from all of $U$ along alternating paths finds, so a minimum cover takes $O(|V| + |E|)$ time after a maximum matching is known.

**Example.** Let $L = \{1, 2, 3, 4\}$, $R = \{a, b, c, d\}$ and $E = \{1a, 1b, 2a, 3a, 4c, 4d\}$. The matching $M = \{1b, 2a, 4c\}$ has size 3, and vertex 3 is exposed, so $U = \{3\}$. From 3 the only edge goes to $a$, whose mate is 2, and 2 has no other neighbour. So $Z = \{3, a, 2\}$, $S = \{2, 3\}$ and $T = \{a\}$. The cover is $C = (L \setminus S) \cup T = \{1, 4, a\}$, of size 3: the edges $1a$ and $1b$ have the end 1, the edges $2a$ and $3a$ have the end $a$, and $4c$ and $4d$ have the end 4. So $\nu = \tau = 3$, and the graph has no perfect matching.

## Consequences

- **[Hall's theorem](/hall-theorem/).** If $|N(X)| \ge |X|$ for each $X \subseteq L$, then each cover $C$ satisfies $|C| \ge |L|$: the set $L \setminus C$ has all its neighbours in $C \cap R$, so $|C \cap R| \ge |L \setminus C|$. By Kőnig's theorem, $\nu = \tau \ge |L|$, so a matching covers $L$.
- **Independent sets and edge covers.** The complement of a vertex cover is an [independent set](/independent-set/), so $\alpha(G) = |V| - \tau(G) = |V| - \nu(G)$ for bipartite $G$; this gives the [maximum independent set of a bipartite graph](/bipartite-maximum-independent-set/) in polynomial time, while the problem is NP-hard in general. With [Gallai's identities](/gallai-identity/), the least size of an [edge cover](/minimum-edge-cover/) of a bipartite graph without isolated vertices equals $\alpha(G)$.
- **Algorithms.** Each algorithm for [bipartite matching](/bipartite-matching/), such as [Kuhn's algorithm](/kuhn-algorithm/) or [Hopcroft-Karp](/hopcroft-karp/), also returns a minimum vertex cover by the search of the proof. The [Hungarian algorithm](/hungarian-algorithm/) was built on this proof and on Egerváry's weighted form.
- **Flows.** The theorem is the case of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), or of [Menger's theorem](/menger-theorem/), for the unit network $s \to L \to R \to t$: a minimum cut gives a minimum cover.
- **Linear programming.** The edge-vertex [incidence matrix](/incidence-matrix/) of a bipartite graph is totally unimodular, so the linear programs for matching and for vertex cover have integral optima, and Kőnig's theorem is their [strong duality](/strong-duality/).

## Tightness

The theorem needs the graph to be bipartite. In an odd cycle $C_{2k+1}$, $\nu = k$, because a matching covers an even number of the $2k + 1$ vertices, and $\tau = k + 1$, because $k$ vertices cover at most $2k$ of the $2k + 1$ edges. So the triangle has $\nu = 1$ and $\tau = 2$. In the [complete graph](/complete-graph/) $K_n$, $\nu = \lfloor n/2 \rfloor$ and $\tau = n - 1$, so the gap can be close to a factor 2. For each graph $\nu \le \tau \le 2\nu$: the easy inequality gives the left side, and the ends of a [maximal matching](/maximal-matching/) form a cover. For a general graph the exact min-max formula is the [Tutte-Berge formula](/tutte-berge-formula/), with odd components in place of covers, and computing $\tau$ is NP-hard.

## History

Dénes Kőnig proved the theorem in 1931, in the matrix form, in a Hungarian paper in Matematikai és Fizikai Lapok. In the same year and journal, Jenő Egerváry proved a weighted form: for a nonnegative integer matrix, the largest total of a set of entries with no two in a line equals the least total of nonnegative integer labels on the rows and columns such that each entry is at most the label of its row plus the label of its column. Kuhn's [Hungarian algorithm](/hungarian-algorithm/) of 1955 is named after these two papers. Kőnig had earlier, in 1916, proved that the edges of a bipartite graph can be colored with as many colors as the largest degree; that is a different theorem, often also called Kőnig's theorem.

## References
