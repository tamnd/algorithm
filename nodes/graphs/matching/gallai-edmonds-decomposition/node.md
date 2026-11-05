---
tag: FEXZXY
kind: theorem
slug: gallai-edmonds-decomposition
name: Gallai-Edmonds decomposition
aliases:
- Gallai-Edmonds structure theorem
area: graphs/matching
level: advanced
summary: Partitions the vertices of a general graph by how maximum matchings cover them.
prereqs: [berge-lemma, blossom]
see_also: [tutte-berge-formula, tutte-theorem, edmonds-blossom, dulmage-mendelsohn-decomposition, maximum-matching, perfect-matching, konig-theorem, micali-vazirani-algorithm]
sources:
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449 to 467 (1965)
    locator: the whole paper (the labels of the final alternating forest, from which the decomposition is read)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 3, Size and structure of maximum matchings (the Gallai-Edmonds structure theorem and factor-critical graphs)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (the Gallai-Edmonds structure theorem, proved through Edmonds' algorithm)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 10, Maximum Matchings (the Berge-Tutte formula and the Gallai-Edmonds structure theorem)
---

The Gallai-Edmonds decomposition splits the vertices of any [graph](/graph/) into three sets: $D$, the vertices that some [maximum matching](/maximum-matching/) leaves uncovered; $A$, the neighbours of $D$ outside $D$; and $C$, the rest. The structure theorem says that every maximum matching has the same shape with respect to this split: it matches $C$ perfectly, matches each vertex of $A$ into a different component of $D$, and covers each component of $D$ except for at most one vertex. The theorem holds for general graphs, [bipartite](/bipartite-graph/) or not, and is about matchings without weights. It refines the [Tutte-Berge formula](/tutte-berge-formula/): $S = A$ is a canonical set that attains its minimum.

## Statement

Let $G = (V, E)$ be a finite undirected graph without weights, $n = |V|$, and $\nu(G)$ the size of a maximum matching. Define

- $D = \{ v \in V : \text{some maximum matching misses } v \}$,
- $A = \{ v \in V \setminus D : v \text{ has a neighbour in } D \}$,
- $C = V \setminus (D \cup A)$.

A graph $H$ is *factor-critical* if $H - x$ has a [perfect matching](/perfect-matching/) for every vertex $x$ of $H$. A matching of $H$ is *near-perfect* if it misses exactly one vertex.

**Theorem (Gallai, Edmonds).** Let $c(D)$ be the number of connected components of $G[D]$.

1. Every component of $G[D]$ is factor-critical.
2. $G[C]$ has a perfect matching.
3. Every maximum matching $M$ of $G$ consists of a near-perfect matching of each component of $G[D]$, a perfect matching of $G[C]$, and $|A|$ edges that match each vertex of $A$ to a vertex of $D$, in distinct components of $G[D]$.
4. $\nu(G) = \frac12 \bigl(n - c(D) + |A|\bigr)$, and $S = A$ attains the minimum in the Tutte-Berge formula.

**Example with all three parts.** Take a hub $h$ with a triangle $xyz$ attached by the edge $hx$, a leaf $\ell$ with the edge $h\ell$, and an edge $pq$ attached by $hp$; seven vertices and seven edges. Here $\nu = 3$.

| set | vertices | why |
|---|---|---|
| $D$ | $x, y, z, \ell$ | $\{pq, hx, yz\}$ misses $\ell$; $\{pq, h\ell, yz\}$ misses $x$, and likewise for $y$ and $z$ |
| $A$ | $h$ | the only vertex outside $D$ next to $D$ |
| $C$ | $p, q$ | always matched to each other |

$G[D]$ has two components, the triangle and the single vertex $\ell$, both factor-critical, so $\nu = \frac12 (7 - 2 + 1) = 3$. Every maximum matching contains $pq$, matches $h$ to $x$ or to $\ell$, and covers the triangle except one vertex. The edge $hp$ is between $A$ and $C$, so it is in no maximum matching.

**Three triangles and a hub.** Three disjoint triangles and a vertex $h$ adjacent to one vertex of each: $D$ is the nine triangle vertices, $A = \{h\}$, $C = \emptyset$, and $\nu = \frac12 (10 - 3 + 1) = 4$. Every maximum matching matches $h$ into one triangle and leaves one vertex of each of the other two uncovered.

**Odd cycle.** In $C_5$ every vertex is missed by some maximum matching, so $D = V$, $c(D) = 1$, $A = \emptyset$ and $\nu = \frac12 (5 - 1) = 2$.

**Bipartite.** In $K_{2,3}$ with sides $\{a_1, a_2\}$ and $\{b_1, b_2, b_3\}$, $D = \{b_1, b_2, b_3\}$, $A = \{a_1, a_2\}$, $C = \emptyset$, and $\nu = \frac12 (5 - 3 + 2) = 2$, with each component of $D$ a single vertex.

## In plain words

Look at all the largest ways of pairing up the vertices of a network. Some vertices are always paired, whichever largest pairing you choose; others are left out by at least one of them. Call the second kind "sometimes left out".

The theorem says these vertices form islands, and each island is so well connected that, after taking away any one of its vertices, the rest of the island pairs up perfectly. The always-paired vertices that touch an island act as gatekeepers: in every largest pairing, each gatekeeper is paired into a different island. All other vertices pair up among themselves. So the number of islands, minus the number of gatekeepers, is exactly how many vertices every largest pairing must leave out.

## Proof

The proof reads the three sets off the last phase of [Edmonds' blossom algorithm](/edmonds-blossom/). Fix a maximum matching $M$ and grow the alternating forest of the forest version of the algorithm, with every $M$-free vertex as a root. Since $M$ is maximum, by [Berge's lemma](/berge-lemma/) the phase finds no augmenting path and stops when no step applies. Write $G'$ for the graph at that moment, in which every [blossom](/blossom/) found has been contracted to a pseudo-vertex, possibly nested. Each vertex of $G$ is in exactly one of three classes: *outer* if it lies in an outer pseudo-vertex of $G'$, *inner* if it is an inner vertex of $G'$ (inner vertices are never contracted), and *unlabelled* otherwise. Call these sets $O$, $I$ and $U$.

**Claim 1 (edge condition).** In $G'$ every edge at an outer pseudo-vertex goes to an inner vertex. So in $G$, an edge between two outer vertices lies inside one outer pseudo-vertex, and no edge joins $O$ to $U$.

*Proof.* An edge from an outer pseudo-vertex to an unlabelled vertex would let the forest grow; an edge between two outer pseudo-vertices of the same tree would form a blossom, and one between two trees would give an augmenting path. The phase stopped, so none of these exists. $\square$

**Claim 2.** The mate of an unlabelled vertex is unlabelled, and $M$ matches $U$ perfectly. The mate of an inner vertex is outer.

*Proof.* Every root is outer, so every vertex of $U$ is matched. An inner vertex enters the forest together with its mate, which becomes outer; an outer vertex other than a root is matched to an inner vertex or to a vertex of its own blossom. So the mate of a labelled vertex is labelled, and the mate of an unlabelled vertex is unlabelled. $\square$

**Claim 3.** Each outer pseudo-vertex of $G'$, expanded in $G$, induces a factor-critical subgraph, and these subgraphs are the components of $G[O]$.

*Proof.* By induction on the nesting. A single vertex is factor-critical. A blossom is an odd cycle $\beta_0 \beta_1 \cdots \beta_{2k}$ whose nodes are vertices or smaller pseudo-vertices $H_0, \ldots, H_{2k}$, each factor-critical by induction. Take $x \in H_i$. The cycle minus $\beta_i$ is a path on $2k$ nodes with a perfect matching; each of its edges joins some $y \in H_j$ to some $z \in H_l$, and then $H_j - y$ and $H_l - z$ have perfect matchings, as does $H_i - x$. Together these form a perfect matching of the blossom minus $x$. Each expanded pseudo-vertex is connected, and by Claim 1 two different outer pseudo-vertices are not adjacent in $G$, so they are the components of $G[O]$. $\square$

**Claim 4.** $\nu(G) = \frac12 (n - q + |I|)$, where $q$ is the number of outer pseudo-vertices, and every maximum matching $N$ covers $I \cup U$, matches each vertex of $I$ to an outer vertex, with distinct vertices of $I$ going to distinct outer pseudo-vertices, and matches $U$ within $U$.

*Proof.* By Claim 1 the components of $G - I$ are the $q$ outer pseudo-vertices, which are odd since factor-critical graphs have an odd number of vertices, and the components of $G[U]$, which are even by Claim 2. Each tree of the forest has one more outer pseudo-vertex than inner vertices, since the root is outer and each inner vertex brings one outer mate, and contracting a blossom removes as many inner vertices as outer pseudo-vertices. With $f = n - 2|M|$ trees, $q = |I| + f$, so $|M| = \frac12 (n - q + |I|)$.

Now let $N$ be any matching. Each odd component of $G - I$ that has no vertex matched by $N$ to $I$ has a vertex missed by $N$ or matched outside it; the only edges leaving a component of $G - I$ go to $I$, so it has a vertex missed by $N$. At most $|I|$ components are matched to $I$, so $N$ misses at least $q - |I| = f$ vertices, and $|N| \le |M|$. Equality forces every inequality to be tight: $N$ matches each vertex of $I$ into a different odd component, that is, to an outer vertex in a different pseudo-vertex; it misses exactly one vertex in each of the other $q - |I|$ outer components and none in the matched ones; and it misses no vertex of $U$. Since $I$ is already used by the outer components, $N$ matches $U$ within $U$. $\square$

**Claim 5.** $D = O$, $A = I$ and $C = U$.

*Proof.* ($O \subseteq D$.) Let $x$ be outer, in the tree with root $r$. By fact 2 of the [blossom](/blossom/) page, applied through every level of nesting, $G$ has an even [alternating path](/alternating-path/) $P$ from $r$ to $x$ that starts at the free vertex $r$ and ends at $x$ with an edge of $M$, or is empty if $x = r$. Then $M \triangle E(P)$ is a maximum matching that misses $x$.

($D \subseteq O$.) By Claim 4 every maximum matching covers $I \cup U$.

($A = I$.) By Claim 1 a neighbour of $O$ outside $O$ is inner, so $A \subseteq I$. Each inner vertex is adjacent in the forest to an outer vertex, its parent, so $I \subseteq A$. Then $C = V \setminus (O \cup I) = U$. $\square$

Now the theorem follows. Part 1 is Claim 3 with $D = O$. Part 2 holds since $M$ matches $U = C$ within itself by Claim 2. For part 3, Claim 4 says a maximum matching $N$ matches $A = I$ into distinct components of $G[D]$ and $C$ within $C$; the remaining edges of $N$ lie inside $G[D]$. In each component of $G[D]$, exactly one vertex is either missed by $N$ or matched to $A$, so $N$ restricted to the component is near-perfect. Part 4 is Claim 4 with $c(D) = q$. Finally $q(G - A) \ge c(D)$, so $\frac12 (n + |A| - q(G - A)) \le \nu(G)$, and the easy direction of the Tutte-Berge formula gives equality. $\blacksquare$

The sets $D$, $A$, $C$ are defined without reference to $M$ or to the algorithm, so the proof also shows that the labels of the final forest do not depend on the maximum matching or on the order of the search.

## Consequences

- **Tutte-Berge formula.** Part 4 gives a set attaining the minimum, which proves the hard direction of the [Tutte-Berge formula](/tutte-berge-formula/), and with it [Tutte's theorem](/tutte-theorem/): $G$ has a perfect matching if and only if $D = \emptyset$.
- **Computation.** One run of Edmonds' algorithm, plus one more search from all free vertices of the final matching, yields $D$, $A$, $C$ in $O(n^3)$ time; with a faster maximum matching, such as the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/), the decomposition costs one blossom search on top of it.
- **Factor-critical graphs.** A connected graph is factor-critical if and only if $D = V$. Gallai's lemma follows: if $G$ is connected and no vertex is covered by every maximum matching, then $G$ is factor-critical, and $\nu(G) = (n - 1)/2$.
- **Stability.** For $a \in A$, the graph $G - a$ has the same sets $D$ and $C$, and $A \setminus \{a\}$; removing a vertex of $A$ lowers $\nu$ by one.
- **Allowed edges.** An edge lies in some maximum matching only if it is inside $G[D]$, inside $G[C]$, or between $A$ and $D$. Edges inside $G[A]$ and between $A$ and $C$ lie in no maximum matching.
- **Bipartite graphs.** A factor-critical bipartite graph is a single vertex, so in a bipartite graph $D$ is an independent set and the theorem reduces to the coarse part of the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/), which refines $C$ further.

## Tightness

- **Each set can be the whole graph.** In an odd cycle $C_{2k+1}$, or in $K_{2k+1}$, $D = V$ and $A = C = \emptyset$. In a graph with a perfect matching, such as the path $P_4$, $C = V$. In a graph with no edges, $D = V$ and $\nu = 0$, and each isolated vertex is a component; the empty graph with $n = 0$ has all three sets empty and $\nu = 0$.
- **Components of $D$ need not be cycles.** Factor-critical graphs include $K_5$, the bowtie of two triangles sharing a vertex, and any odd cycle with chords, so part 1 cannot be sharpened to "odd cycles".
- **$A$ is needed.** In the star $K_{1,3}$, $D$ is the three leaves, $A$ is the centre and $\nu = \frac12 (4 - 3 + 1) = 1$. Without the term $|A|$ the formula would give $\frac12 (4 - 3)$, which is not even an integer.
- **Not every minimizer.** Other sets $S$ may attain the Tutte-Berge minimum. In the path $P_5 = v_1 v_2 v_3 v_4 v_5$, $D = \{ v_1, v_3, v_5 \}$ and $A = \{ v_2, v_4 \}$, and $S = \{ v_2 \}$ also attains $\nu = 2$. The theorem singles out one canonical minimizer, the one in which $G - S$ has only factor-critical odd components and components with perfect matchings.
- **Not every vertex of $D$ is missed by one matching.** In $P_5$ each maximum matching misses exactly one of $v_1, v_3, v_5$; the definition of $D$ uses all maximum matchings together.

## History

Tibor Gallai proved the structure theorem in two papers of 1963 and 1964, as part of a new proof of Tutte's theorem and a study of the maximal systems of independent edges. Jack Edmonds, in his 1965 paper on the blossom algorithm, obtained the same partition as the labels of the final alternating forest, and showed that it is computable in polynomial time. Lovász and Plummer's book of 1986 made the theorem a central tool of matching theory.

## References
