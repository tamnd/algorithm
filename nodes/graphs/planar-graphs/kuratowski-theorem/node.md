---
tag: 9XVVA5
kind: theorem
slug: kuratowski-theorem
name: Kuratowski's theorem
aliases:
- Kuratowski's characterization
area: graphs/planar-graphs
level: core
summary: A graph is planar if and only if it contains no subdivision of K5 or K3,3.
prereqs: [planar-graph, euler-formula, graph-minor, jordan-curve-theorem, k-vertex-connected-graph]
see_also: [wagner-theorem, planarity-testing, boyer-myrvold-planarity-test, hopcroft-tarjan-planarity-test, graph-genus, graph-minor-theorem, fary-theorem, hanani-tutte-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.4, Planar graphs (Kuratowski's theorem with the proof through 3-connected graphs); Lemma 3.2.1 on contractible edges; Proposition 4.2.6 on face boundaries
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.2, Characterization of planar graphs (Kuratowski's theorem and Wagner's form)
  - paper: "Kazimierz Kuratowski, Sur le problème des courbes gauches en topologie, Fundamenta Mathematicae 15, 271 to 283 (1930)"
    locator: the original theorem
  - paper: "Carsten Thomassen, Kuratowski's theorem, Journal of Graph Theory 5(3), 225 to 241 (1981)"
    locator: the short proof through 3-connected graphs and contractible edges
  - book: "Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001"
    locator: Section 2.1 (Jordan-Schönflies theorem) and Chapter 2 (proofs of Kuratowski's theorem)
---

Kuratowski's theorem says which graphs can be drawn in the plane without crossings: exactly those that do not contain a subdivided copy of $K_5$ or of $K_{3,3}$. So two small graphs are the only obstructions to [planarity](/planar-graph/). Non-planarity, which is a statement about all possible drawings, always has a short certificate: a subgraph that is visibly a subdivided $K_5$ or $K_{3,3}$. Linear-time [planarity tests](/planarity-testing/) output either a plane embedding or such a subgraph.

## Statement

Write $TH$ for a **subdivision** of a graph $H$: a graph obtained from $H$ by replacing edges with paths whose inner vertices are new and pairwise distinct. A graph $G$ *contains* $TH$ if some subgraph of $G$ is a $TH$; equivalently, $H$ is a topological minor of $G$ (see [graph minor](/graph-minor/)).

**Theorem (Kuratowski, 1930).** A finite graph $G$ is planar if and only if $G$ contains neither $TK_5$ nor $TK_{3,3}$.

The theorem is about abstract graphs, so no embedding is given as input. In one direction the conclusion is an embedding: a drawing with coordinates, or equivalently a [rotation system](/rotation-system/) whose face count satisfies [Euler's formula](/euler-formula/). In the other direction it is a subgraph, called a **Kuratowski subgraph**. Loops and parallel edges do not affect planarity, so it suffices to treat simple graphs.

**Theorem (Wagner, 1937), the minor form.** $G$ is planar if and only if neither $K_5$ nor $K_{3,3}$ is a [minor](/graph-minor/) of $G$. The proof shows that the two conditions are equivalent (Lemma 2 there), so the two theorems are equivalent; see [Wagner's theorem](/wagner-theorem/).

## In plain words

Some networks can be drawn on paper so that no two lines cross, and some cannot. Two small networks cannot: five points all joined to each other, and three houses each joined to three utilities. Adding extra points along the lines of either one does not help, because a crossing-free drawing of the longer version would give one of the original.

The theorem says these two are the only reasons. If a network cannot be drawn without crossings, then hidden inside it is one of the two bad networks, possibly with some lines stretched into longer paths. So whenever drawing fails, you can point to a small piece of the network and say: this part alone already cannot be drawn.

## Proof

**Easy direction.** Every subgraph of a planar graph is planar, and a drawing of a $TH$ is a drawing of $H$ once each subdivided path is read as one curve. $K_5$ has $10 > 3 \cdot 5 - 6$ edges and $K_{3,3}$ is triangle-free with $9 > 2 \cdot 6 - 4$ edges, so by the edge bounds from Euler's formula neither is planar. So a planar graph contains no $TK_5$ and no $TK_{3,3}$.

**Hard direction, outline.** The full argument is in [the proof](proofs/main.md); it follows Thomassen and Diestel, Section 4.4. It has three ingredients.

1. *Minors to subdivisions.* If $G$ has a $K_{3,3}$ minor it contains $TK_{3,3}$, and if $G$ has a $K_5$ minor it contains $TK_5$ or $TK_{3,3}$. Each branch set is a tree with one attachment per neighbour; a tree with 3 attachments has a central vertex from which disjoint paths reach them, and a tree with 4 attachments either has such a vertex or splits into two halves with 2 attachments each, which turns the $K_5$ model into a $K_{3,3}$ model.
2. *A contractible edge.* Every [3-connected](/k-vertex-connected-graph/) graph other than $K_4$ has an edge whose contraction leaves it 3-connected.
3. *Induction.* Take a non-planar graph $G$ with no $TK_5$ or $TK_{3,3}$ and as few vertices plus edges as possible. Gluing plane drawings along a cut vertex or a 2-separator shows that $G$ is 3-connected. Contract a contractible edge $xy$ to one vertex $v$; the result has no $K_5$ or $K_{3,3}$ minor by step 1, so it is planar by minimality. Deleting $v$ leaves a face bounded by a cycle $C$ that contains all neighbours of $x$ and $y$. Either the neighbours of $y$ lie between two consecutive neighbours of $x$ on $C$, and $x$ and $y$ can be drawn apart, which contradicts non-planarity; or $x$ and $y$ share three neighbours on $C$, which gives a $K_5$ minor; or their neighbours alternate around $C$, which gives a $TK_{3,3}$. Each case is a contradiction. $\blacksquare$

The [Jordan curve theorem](/jordan-curve-theorem/) enters in the last step: it guarantees that each face of a 2-connected plane graph is bounded by a cycle, and that a new vertex placed in such a face can be joined to any vertices on that cycle.

## Consequences

- **Certificates of non-planarity.** A Kuratowski subgraph has at most $|E(G)|$ edges and can be checked in linear time: verify that its branch vertices have degree 3 or 4 and that the paths between them form $K_5$ or $K_{3,3}$. The [Boyer-Myrvold planarity test](/boyer-myrvold-planarity-test/) and the [Hopcroft-Tarjan test](/hopcroft-tarjan-planarity-test/), with later extensions, return such a subgraph in $O(n)$ time when the input is not planar. A plane embedding is the certificate in the other direction.
- **Wagner's theorem.** By Lemma 2 of the proof, "no $TK_5$ or $TK_{3,3}$" is the same as "no $K_5$ or $K_{3,3}$ minor". So the planar graphs form a minor-closed class with exactly two forbidden minors, the first example of the [graph minor theorem](/graph-minor-theorem/).
- **Degree 3 obstructions.** A graph of maximum degree 3 is planar if and only if it contains no $TK_{3,3}$, since $TK_5$ needs vertices of degree 4.
- **Algebraic and topological forms.** Planarity also has characterizations by drawings with even crossings ([Hanani-Tutte theorem](/hanani-tutte-theorem/)), by cycle spaces (MacLane) and by duality (Whitney). Each can be derived from Kuratowski's theorem.
- **Straight lines.** Combined with [Fáry's theorem](/fary-theorem/), a graph has a straight-line crossing-free drawing exactly when it has no Kuratowski subgraph.

## Tightness

Both obstructions are needed, and both are as small as possible.

| graph | planar? | why |
|---|---|---|
| a single vertex | yes | a point |
| a tree | yes | trees have no cycle, so they contain no subdivision of a graph with a cycle, and they draw crossing-free |
| $K_4$ | yes | a triangle with one vertex inside |
| $K_5 - e$ | yes | the triangle with two vertices on opposite sides; 9 edges $= 3 \cdot 5 - 6$ |
| $K_{3,3} - e$ | yes | 8 edges $= 2 \cdot 6 - 4$; a drawing is easy to find |
| $K_5$ | no | 10 edges $> 9$ |
| $K_{3,3}$ | no | triangle-free with 9 edges $> 8$ |
| Petersen graph | no | contains $TK_{3,3}$; it has no $TK_5$ because it is 3-regular |

- **Neither obstruction can be dropped.** $K_5$ contains no $TK_{3,3}$: it has only 5 vertices. $K_{3,3}$ contains no $TK_5$: it has no vertex of degree 4. So the list $\{K_5, K_{3,3}\}$ is minimal for subdivisions, and also for minors, since neither is a minor of the other ($K_{3,3}$ has fewer edges than $K_5$, and $K_5$ has fewer vertices than $K_{3,3}$).
- **Both are edge-minimal.** Deleting any edge of $K_5$ or of $K_{3,3}$ makes it planar (by symmetry, the rows $K_5 - e$ and $K_{3,3} - e$ cover all edges).
- **Other surfaces.** For each surface there is a finite list of forbidden minors, by the graph minor theorem, but the lists grow fast. For the projective plane there are 35 minor-minimal and 103 subdivision-minimal obstructions (Archdeacon, Glover, Huneke and Wang). For the torus, computer searches have found thousands of minor-minimal obstructions. See [graph genus](/graph-genus/).
- **Infinite graphs.** Dirac and Schuster extended the theorem to countable graphs. It fails for uncountable ones: $K_{2,\aleph_1}$ has no Kuratowski subgraph, but a drawing would need uncountably many disjoint open regions between its paths.

## History

Kazimierz Kuratowski published the theorem in 1930 in Fundamenta Mathematicae. Orrin Frink and Paul A. Smith found it independently at the same time but published only an announcement, and Lev Pontryagin is also credited with an unpublished proof, so the theorem is sometimes called the Pontryagin-Kuratowski theorem. Klaus Wagner gave the minor form in 1937, as part of his study of graphs without a $K_5$ minor. Many proofs followed; Carsten Thomassen's 1981 paper gave the short route through 3-connected graphs and contractible edges used here, and also derived from it that 3-connected planar graphs have convex drawings. The algorithmic side came later: Hopcroft and Tarjan (1974) tested planarity in linear time, and extracting a Kuratowski subgraph in linear time became standard with the tests of the 1990s and 2000s.

## References
