---
tag: YHBYC8
kind: theorem
slug: wagner-theorem
name: Wagner's theorem
aliases:
- minor characterization of planarity
area: graphs/planar-graphs
level: advanced
summary: A graph is planar if and only if it has no K5 or K3,3 minor.
prereqs: [kuratowski-theorem, graph-minor, planar-graph]
see_also: [graph-minor-theorem, hadwiger-conjecture, outerplanar-graph, planarity-testing, planar-edge-bound, four-color-theorem, complete-graph, kuratowski-theorem]
sources:
  - paper: doi:10.1007/BF01594196
    title: Klaus Wagner, Über eine Eigenschaft der ebenen Komplexe, Mathematische Annalen 114, 570 to 590 (1937)
    locator: the characterization of planar graphs by the minors K5 and K3,3, and the structure of graphs with no K5 minor
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.4, Planar graphs (Kuratowski's theorem in its minor and topological forms, and the lemma that a K5 or K3,3 minor gives a K5 or K3,3 subdivision)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.2, Characterization of planar graphs (Kuratowski's theorem and Wagner's form)
  - paper: "Kazimierz Kuratowski, Sur le problème des courbes gauches en topologie, Fundamenta Mathematicae 15, 271 to 283 (1930)"
    locator: the characterization by subdivisions of K5 and K3,3
---

Wagner's theorem says that a graph is [planar](/planar-graph/) if and only if it has neither $K_5$ nor $K_{3,3}$ as a [minor](/graph-minor/), that is, neither can be obtained from it by deleting vertices and edges and contracting edges. It is the minor form of [Kuratowski's theorem](/kuratowski-theorem/), which forbids subdivisions of the same two graphs, and the two forms are equivalent by a short argument. Wagner's form shows that planarity is a minor-closed property with exactly two minimal obstructions, the model for the [graph minor theorem](/graph-minor-theorem/).

## Statement

**Theorem (Wagner, 1937).** A graph $G$ is planar if and only if $G$ has no $K_5$ minor and no $K_{3,3}$ minor.

A graph $H$ is a *minor* of $G$ if $G$ has disjoint connected vertex sets $V_x$, one for each vertex $x$ of $H$ (the *branch sets*), such that for each edge $xy$ of $H$ some edge of $G$ joins $V_x$ and $V_y$. Equivalently, $H$ arises from a subgraph of $G$ by contracting edges. A *subdivision* of $H$ replaces the edges of $H$ by internally disjoint paths; its vertices of $H$ are the *branch vertices*.

The theorem is about abstract graphs; no embedding is given. A planar embedding, for example as a [rotation system](/rotation-system/), is a certificate for "planar", and a minor model, the list of branch sets, is a certificate for "not planar".

**Small cases.**

| graph | planar? | $K_5$ minor | $K_{3,3}$ minor |
|---|---|---|---|
| a single vertex, a tree | yes | no: fewer than 5 vertices, or a forest | no: every minor of a forest is a forest |
| $K_4$ | yes | no: 4 vertices | no |
| $K_5 - e$ | yes | no: 9 edges | no: 5 vertices |
| $K_5$ | no | itself | no: 5 vertices |
| $K_{3,3}$ | no | no: 9 edges | itself |
| the Petersen graph | no | yes: contract the 5 spokes | yes |

The Petersen graph has a $K_5$ minor but no subdivision of $K_5$, since it has maximum degree 3 and a subdivision of $K_5$ needs vertices of degree 4. This shows that the two forms of the theorem, with minors and with subdivisions, really differ in what they forbid.

## In plain words

Two small graphs cannot be drawn on paper without crossings: five points all joined to each other, and three houses each joined to three utilities. Wagner's theorem says these two are the only reasons a graph cannot be drawn without crossings.

To find them inside a large graph, you may delete points and lines, and you may shrink a line until its two ends merge into one point. If no sequence of such steps produces one of the two small graphs, the graph can be drawn without crossings. If one of them appears, it cannot.

## Proof

Write $X$ for $K_5$ or $K_{3,3}$.

**Part 1: a planar graph has no $X$ minor.** Deleting a vertex or an edge of a plane graph leaves a plane graph. Contracting an edge $uv$ of a plane graph also leaves a plane graph: draw the merged vertex at $u$ and redraw the edges of $v$ along the old arc $uv$, close to it. So every minor of a planar graph is planar. But $K_5$ and $K_{3,3}$ are not planar, by the [planar edge bound](/planar-edge-bound/): $K_5$ has $10 > 3 \cdot 5 - 6$ edges, and $K_{3,3}$ has no triangle and $9 > 2 \cdot 6 - 4$ edges.

**Part 2: a non-planar graph has an $X$ minor.** Let $G$ be non-planar. By [Kuratowski's theorem](/kuratowski-theorem/), $G$ has a subgraph $K$ that is a subdivision of $K_5$ or $K_{3,3}$. Contract, in each subdivided path of $K$, all edges but one. The result is $K_5$ or $K_{3,3}$, so it is a minor of $G$. $\square$

The rest of this section proves the converse step, from a minor to a subdivision. With it, Wagner's theorem also implies Kuratowski's theorem, so the two are equivalent.

**Lemma 1.** If $H$ has maximum degree at most 3 and $G$ has $H$ as a minor, then $G$ has a subdivision of $H$ as a subgraph.

*Proof.* Choose branch sets $V_x$ and, for each edge $xy$ of $H$, one edge $e_{xy}$ of $G$ between $V_x$ and $V_y$. In $V_x$, at most 3 vertices are ends of the chosen edges; call them the attachments of $x$. Let $T_x$ be a subtree of $G[V_x]$ that contains all attachments. If there are at most 2 attachments, any vertex of the path in $T_x$ between them serves as $c_x$ below. With 3 attachments, each edge of $T_x$ splits them into two groups; direct it toward the side with at least 2 of them. Follow directed edges from any vertex; since $T_x$ is a finite tree, this stops at a vertex $c_x$ where every edge points in. Then every component of $T_x - c_x$ holds at most one attachment, so $c_x$ is joined to all attachments by paths in $T_x$ that meet only at $c_x$. Take $c_x$ as the branch vertex of $x$, and for each edge $xy$ the path from $c_x$ through $T_x$, the edge $e_{xy}$, and $T_y$ to $c_y$. These paths are internally disjoint, because the trees $T_x$ are disjoint. $\square$

**Lemma 2.** If $G$ has a $K_5$ minor, then $G$ has a subdivision of $K_5$ or of $K_{3,3}$.

*Proof.* Choose branch sets $V_1, \ldots, V_5$, one edge between each pair, attachments and subtrees $T_i$ as in Lemma 1; now each $T_i$ has at most 4 attachments. Suppose first that no edge of any $T_i$ splits its attachments 2 and 2. Then, as in Lemma 1, direct each edge toward the side with at least 3 attachments, and find in each $T_i$ a vertex $c_i$ with disjoint paths to all attachments. The construction of Lemma 1 gives a subdivision of $K_5$.

Otherwise, say an edge of $T_1$ splits it into subtrees $U$ and $U'$, where $U$ holds the attachments toward $V_2$ and $V_3$, and $U'$ those toward $V_4$ and $V_5$. Then $U$ meets $U'$ (through the split edge), $V_2$ and $V_3$; $U'$ meets $V_4$ and $V_5$; and each of $V_4, V_5$ meets each of $V_2, V_3$. So $\{U, V_4, V_5\}$ and $\{U', V_2, V_3\}$ are the branch sets of the two sides of a $K_{3,3}$ minor. By Lemma 1, $G$ has a subdivision of $K_{3,3}$. $\square$

**Wagner implies Kuratowski.** If $G$ has a subdivision of $X$, it has an $X$ minor and is not planar by Part 1. If $G$ has no subdivision of $K_5$ or $K_{3,3}$, then by Lemma 1 (for $K_{3,3}$, of maximum degree 3) and Lemma 2 (for $K_5$) it has no $K_5$ or $K_{3,3}$ minor, and by Wagner's theorem it is planar. $\blacksquare$

## Consequences

- **Planarity is minor-closed.** Part 1 shows that the planar graphs are closed under minors, and Wagner's theorem lists their excluded minors: exactly $K_5$ and $K_{3,3}$, since neither is a minor of the other. The [graph minor theorem](/graph-minor-theorem/) of Robertson and Seymour says that every minor-closed class has a finite list of excluded minors; for planarity, Wagner found it.
- **Outerplanar graphs.** By the same method, a graph is [outerplanar](/outerplanar-graph/) if and only if it has no $K_4$ minor and no $K_{2,3}$ minor.
- **Graphs with no $K_5$ minor.** In the same 1937 paper, Wagner described the graphs with no $K_5$ minor: they are built by gluing planar graphs and one 8-vertex graph along cliques of at most 3 vertices. It follows that the [Hadwiger conjecture](/hadwiger-conjecture/) for $K_5$ minors is equivalent to the [four color theorem](/four-color-theorem/).
- **Certificates.** A [planarity test](/planarity-testing/) can return either an embedding or a minor or subdivision of $K_5$ or $K_{3,3}$, and both can be checked in linear time. Wagner's form needs only the branch sets.
- **Sparsity of minors.** Every minor of a planar graph has at most $3n - 6$ edges. Minor-closed classes in general have $O(n)$ edges, which drives many algorithms on them.

## Tightness

- **Both minors are needed.** $K_5$ has only 5 vertices, so it has no $K_{3,3}$ minor. $K_{3,3}$ has 9 edges, and deleting or contracting never adds edges, while $K_5$ has 10, so $K_{3,3}$ has no $K_5$ minor. Each graph alone is non-planar, so neither can be dropped from the list.
- **Both are minimal.** Every proper minor of $K_5$ or $K_{3,3}$ is planar. Deleting one edge gives $K_5 - e$ or $K_{3,3} - e$, both planar, and contracting one edge gives $K_4$ or a graph on 5 vertices with 8 edges, $K_{3,3}$ with two vertices merged, which is planar.
- **Minor, not subgraph.** Forbidding $K_5$ and $K_{3,3}$ only as subgraphs is not enough: a subdivision of $K_5$ with each edge split once contains neither as a subgraph but is not planar.
- **Other surfaces.** For the torus and other surfaces the list of excluded minors is finite by the graph minor theorem, but much longer.

## History

Kuratowski proved the subdivision form in 1930. Wagner proved the minor form in 1937, in a paper that also described the graphs with no $K_5$ minor and related them to the four color problem. The equivalence of the two forms, through Lemmas 1 and 2, is standard textbook material (Diestel, Section 4.4; West, Section 6.2). The minor point of view grew into the graph minor project of Robertson and Seymour.

## References
