---
tag: ZPH211
kind: theorem
slug: hadwiger-conjecture
name: Hadwiger's conjecture
aliases:
- Hadwiger conjecture on clique minors
area: graphs/coloring-and-cliques
level: research
summary: Conjecture that every graph with chromatic number k has a K(k) minor.
prereqs: [graph-minor, chromatic-number, four-color-theorem]
see_also: [four-color-theorem, graph-minor, wagner-theorem, chromatic-number, five-color-theorem, deletion-contraction, mycielski-graph, graph-minor-theorem]
sources:
  - paper: "H. Hadwiger, Über eine Klassifikation der Streckenkomplexe, Vierteljahrsschrift der Naturforschenden Gesellschaft in Zürich 88, 133 to 142 (1943)"
    locator: the conjecture, and its proof for k at most 4
  - paper: doi:10.1112/jlms/s1-27.1.85
    title: G. A. Dirac, A property of 4-chromatic graphs and some remarks on critical graphs, Journal of the London Mathematical Society 27(1), 85 to 92 (1952)
    locator: the whole paper (every 4-chromatic graph contains a subdivision of K4)
  - paper: doi:10.1007/BF01594196
    title: K. Wagner, Über eine Eigenschaft der ebenen Komplexe, Mathematische Annalen 114, 570 to 590 (1937)
    locator: the structure of graphs with no K5 minor, which makes the case k = 5 equivalent to the four color theorem
  - paper: doi:10.1007/BF01202354
    title: Neil Robertson, Paul Seymour and Robin Thomas, Hadwiger's conjecture for K6-free graphs, Combinatorica 13(3), 279 to 361 (1993)
    locator: the main theorem (the case k = 6, by reduction to the four color theorem)
  - paper: doi:10.1017/S0305004100061521
    title: Andrew Thomason, An extremal function for contractions of graphs, Mathematical Proceedings of the Cambridge Philosophical Society 95(2), 261 to 265 (1984)
    locator: the main theorem (average degree O(t sqrt(log t)) forces a K(t) minor)
  - paper: doi:10.1090/jams/1047
    title: Michelle Delcourt and Luke Postle, Reducing linear Hadwiger's conjecture to coloring small graphs, Journal of the American Mathematical Society 38(2), 481 to 507 (2025)
    locator: the main theorem (every graph with no K(t) minor is O(t log log t)-colorable)
  - paper: doi:10.1016/0095-8956(79)90062-5
    title: P. A. Catlin, Hajós' graph-coloring conjecture, variations and counterexamples, Journal of Combinatorial Theory, Series B 26(3), 268 to 274 (1979)
    locator: the whole paper (counterexamples to the subdivision version for k at least 7)
  - paper: doi:10.1007/978-3-319-32162-2_13
    title: Paul Seymour, Hadwiger's conjecture, in Open Problems in Mathematics, Springer, 2016, 417 to 437
    locator: the whole survey (known cases, the bounds, and related conjectures)
---

Hadwiger's conjecture says that every graph with [chromatic number](/chromatic-number/) at least $k$ has the complete graph $K_k$ as a [minor](/graph-minor/). Equivalently, every graph with no $K_k$ minor can be colored with $k - 1$ colors. Hadwiger stated it in 1943 and proved it for $k \le 4$. The case $k = 5$ is equivalent to the [four color theorem](/four-color-theorem/), and the case $k = 6$ was proved in 1993 by reduction to it; for every $k \ge 7$ the conjecture is open. It is one of the central open problems of graph theory.

## Statement

A graph $H$ is a *minor* of $G$ if $H$ can be obtained from a subgraph of $G$ by contracting edges. Equivalently, $G$ has a $K_k$ minor if there are $k$ disjoint connected vertex sets $B_1, \ldots, B_k$, the *branch sets*, with an edge between $B_i$ and $B_j$ for every $i \ne j$.

**Conjecture (Hadwiger 1943).** For every integer $k \ge 1$, every graph $G$ with $\chi(G) \ge k$ has a $K_k$ minor. Equivalently, if $G$ has no $K_{k}$ minor, then $\chi(G) \le k - 1$.

**Known cases.**

- For $k \le 4$ it is a theorem (Hadwiger 1943; Dirac 1952 proved the stronger form with a subdivision of $K_4$). The proof is below.
- For $k = 5$ it is equivalent to the four color theorem (Wagner 1937), so it holds.
- For $k = 6$ it holds (Robertson, Seymour and Thomas 1993), by showing that a minimal counterexample is a planar graph plus one vertex, and then using the four color theorem.
- For $k \ge 7$ it is open.

## In plain words

Take a network that needs many colors. The conjecture says the reason is always a hidden complete network. You can find $k$ separate connected pieces, each pair of pieces joined by at least one line, whenever $k$ colors are needed.

Squeeze each piece into a single point and you get $k$ points all joined to each other, which plainly needs $k$ colors. The conjecture says this is the only way to need many colors, up to squeezing and erasing.

## Proof

We prove the cases $k \le 4$.

**$k = 1, 2, 3$.** $K_1$ is a minor of every nonempty graph. A graph with $\chi \ge 2$ has an edge, which is a $K_2$. A graph with $\chi \ge 3$ is not bipartite, so it contains an [odd cycle](/bipartite-odd-cycle-theorem/), and contracting all but three edges of that cycle gives $K_3$.

**$k = 4$.** We show that every graph with no $K_4$ minor is 3-colorable. Every subgraph and every minor of such a graph again has no $K_4$ minor. Suppose the claim is false, and let $G$ be a counterexample with the fewest vertices. Then $\chi(G) \ge 4$, so $n \ge 4$.

*$G$ is connected and has no cut vertex.* Otherwise $G = G_1 \cup G_2$, where the two parts are smaller and share at most one vertex $v$. Each part is 3-colorable by minimality. Rename the colors in $G_2$ so that $v$ gets the same color in both, and the two colorings together color $G$, a contradiction.

*$G$ has no separating set of two vertices.* Suppose $G - \{u, v\}$ is disconnected, let $D$ be one of its components and $D'$ another. Every component of $G - \{u, v\}$ has a neighbor at $u$ and at $v$: otherwise one vertex of $\{u, v\}$ would separate it from the rest, and $G$ has no cut vertex. Let $G_1 = G[D \cup \{u, v\}]$ and $G_2 = G - D$, both with fewer vertices than $G$. Add the edge $uv$ to both if it is missing. $G_1 + uv$ is a minor of $G$: contract a path from $u$ to $v$ through $D'$ onto an edge. Likewise $G_2 + uv$ is a minor of $G$, using a path through $D$. So both have no $K_4$ minor, and by minimality both are 3-colorable, with $u$ and $v$ of different colors. Rename the colors of the second coloring so that it agrees with the first on $u$ and $v$. Since $G_1 \cap G_2 = \{u, v\}$, together they color $G$, a contradiction.

So $G$ is 3-connected with $n \ge 4$, and in particular every vertex has degree at least 3, so $G$ has a cycle. Let $C$ be a cycle of $G$.

*Case 1: some vertex is not on $C$.* Let $D$ be a component of $G - V(C)$. The neighbors of $D$ on $C$ separate $D$ from the rest of $C$ unless they are all of $C$, so by 3-connectivity $D$ has at least 3 neighbors $a, b, c$ on $C$, in this cyclic order. Cut $C$ into three paths: from $a$ up to the vertex before $b$, from $b$ up to the vertex before $c$, and from $c$ up to the vertex before $a$. Take these three paths and $D$ as branch sets. They are connected and disjoint, any two of the paths are joined by an edge of $C$, and $D$ is joined to each path, through $a$, $b$ and $c$. That is a $K_4$ minor.

*Case 2: $C$ contains every vertex.* Since $n \ge 4$ and every vertex has degree at least 3, $C$ has a chord $xy$. It splits $C$ into two paths with nonempty interiors $A$ and $B$. As $\{x, y\}$ does not separate $G$, some path joins $A$ to $B$ in $G - \{x, y\}$; all vertices lie on $C$, so this path has an edge $ab$ with $a \in A$ and $b \in B$. In the cyclic order of $C$ the four vertices come as $x, a, y, b$. Cut $C$ into four paths: from $x$ up to the vertex before $a$, from $a$ up to the vertex before $y$, from $y$ up to the vertex before $b$, and from $b$ up to the vertex before $x$. Consecutive paths are joined by edges of $C$, the chord $xy$ joins the first and the third, and the chord $ab$ joins the second and the fourth. That is a $K_4$ minor.

Both cases contradict the choice of $G$, so every graph with no $K_4$ minor is 3-colorable, and every graph with $\chi \ge 4$ has a $K_4$ minor. $\blacksquare$

**$k = 5$ and the four color theorem.** Planar graphs have no $K_5$ minor, so the case $k = 5$ implies the four color theorem. Conversely, Wagner (1937) showed that every graph with no $K_5$ minor is built from planar graphs and copies of an 8-vertex graph $V_8$ by gluing along cliques of at most 3 vertices; such gluing keeps 4-colorability, so the four color theorem implies the case $k = 5$.

## Consequences

- **Graphs without $K_4$ minors.** These are the series-parallel graphs, and the proof above shows they are 3-colorable. By Dirac's theorem, a graph with minimum degree at least 3 contains a subdivision of $K_4$, so every graph with no $K_4$ minor has a vertex of degree at most 2; these graphs are 2-degenerate, and greedy coloring in a degeneracy order 3-colors them in linear time.
- **Bounds for every $k$.** Thomason (1984), and independently Kostochka, showed that a graph with average degree at least $c\, t \sqrt{\log t}$ has a $K_t$ minor, for a constant $c$. Graphs with no $K_t$ minor are then $O(t \sqrt{\log t})$-[degenerate](/degeneracy/), and greedy coloring uses $O(t \sqrt{\log t})$ colors. Delcourt and Postle (2025) improved this to $O(t \log \log t)$ colors.
- **Minor-closed classes.** In any class closed under minors that misses some $K_t$, such as graphs embeddable on a fixed surface, the chromatic number is bounded by a function of $t$. Hadwiger's conjecture would make the function $t - 1$.
- **Induction over minors.** The proof shows the standard method: a minimal counterexample is highly connected, because separations of small order allow induction on minors obtained by [deletion and contraction](/deletion-contraction/).

## Tightness

- **$K_{k-1}$.** The complete graph $K_{k-1}$ has no $K_k$ minor and needs $k - 1$ colors, so $k - 1$ in the statement cannot be lowered.
- **Minors cannot be replaced by subgraphs.** Graphs with no triangle can have any chromatic number, as the [Mycielski graphs](/mycielski-graph/) show. So a large chromatic number does not force a large complete subgraph, only, conjecturally, a large complete minor.
- **Minors cannot be replaced by subdivisions.** Hajós conjectured that $\chi \ge k$ forces a subdivision of $K_k$. This is true for $k \le 4$ by Dirac's theorem, but false for every $k \ge 7$ (Catlin 1979).

## History

Hugo Hadwiger stated the conjecture in 1943 in a paper on a classification of graphs, and proved the cases $k \le 4$. Wagner had shown in 1937 that the case $k = 5$ is equivalent to the four color problem, then still open, and Dirac proved in 1952 that a 4-chromatic graph even contains a subdivision of $K_4$. After the four color theorem was proved by Appel and Haken in 1976, Robertson, Seymour and Thomas settled the case $k = 6$ in 1993, again relying on it. Lower bounds on the average degree that force a $K_t$ minor, by Kostochka and by Thomason in 1984, gave $O(t \sqrt{\log t})$ colors, improved in a series of papers to the $O(t \log \log t)$ bound of Delcourt and Postle. Seymour's 2016 survey describes the state of the problem.

## References
