---
tag: B4ES2D
kind: theorem
slug: graph-minor-theorem
name: Robertson-Seymour graph minor theorem
aliases:
- Graph minor theorem
- Robertson-Seymour theorem
- Wagner's conjecture
area: graphs/planar-graphs
level: research
summary: Every infinite family of graphs contains a pair where one is a minor of the other; minor-closed families have finite obstruction sets.
prereqs: [graph-minor, kuratowski-theorem, wagner-theorem, treewidth, ramsey-theorem]
see_also: [minor-testing, graph-genus, graph-genus-computation, tree-decomposition, hadwiger-conjecture, fixed-parameter-tractable, courcelle-theorem, planar-graph]
sources:
  - paper: doi:10.1016/j.jctb.2004.08.001
    title: Neil Robertson and Paul D. Seymour, Graph minors XX, Wagner's conjecture, Journal of Combinatorial Theory, Series B 92(2), 325 to 357 (2004)
    locator: the main theorem, that finite graphs are well-quasi-ordered by the minor relation
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 12, Minors, trees and WQO; Section 12.1 (well-quasi-ordering and the Ramsey argument), Section 12.2 (the graph minor theorem for trees) and the statement of the graph minor theorem with its corollaries
  - paper: "C. St. J. A. Nash-Williams, On well-quasi-ordering finite trees, Proceedings of the Cambridge Philosophical Society 59, 833 to 835 (1963)"
    locator: the minimal bad sequence argument used in the proof file for trees
  - paper: "Joseph B. Kruskal, Well-quasi-ordering, the tree theorem, and Vázsonyi's conjecture, Transactions of the American Mathematical Society 95, 210 to 225 (1960)"
    locator: the tree theorem, the first case of the graph minor theorem
  - paper: "Neil Robertson and Paul D. Seymour, Graph minors XIII, The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65 to 110 (1995)"
    locator: the cubic-time test for a fixed minor
  - paper: "Michael R. Fellows and Michael A. Langston, Nonconstructive tools for proving polynomial-time decidability, Journal of the ACM 35(3), 727 to 739 (1988)"
    locator: the use of the theorem to prove that problems are in polynomial time without giving the algorithm
---

The graph minor theorem of Neil Robertson and Paul Seymour says that in every infinite sequence of finite graphs $G_1, G_2, \ldots$ there are indices $i < j$ such that $G_i$ is a [minor](/graph-minor/) of $G_j$. Equivalently, every class of graphs that is closed under taking minors is described by a finite list of forbidden minors. [Wagner's theorem](/wagner-theorem/), with the list $K_5, K_{3,3}$ for planar graphs, is the first example. The proof fills twenty-three papers that appeared from 1983 to 2004, and the theorem is one of the deepest results in graph theory. It has a strong algorithmic side: together with the cubic-time test for a fixed minor, it shows that membership in any minor-closed class can be decided in polynomial time, even when nobody knows the list. **How the embedding is given:** no embedding is involved; the theorem is about abstract finite graphs, and the minor relation does not depend on any drawing.

## Statement

A graph $H$ is a **minor** of $G$, written $H \preceq G$, if $H$ can be obtained from a subgraph of $G$ by contracting edges; equivalently, $G$ has a model of $H$: disjoint connected vertex sets $V_h$ ($h \in V(H)$), the branch sets, with an edge of $G$ between $V_h$ and $V_{h'}$ for each edge $hh'$ of $H$. Graphs are finite, and isomorphic graphs are not distinguished. The relation $\preceq$ is reflexive and transitive.

A quasi-order is a **well-quasi-order** if every infinite sequence $x_1, x_2, \ldots$ has indices $i < j$ with $x_i \le x_j$. Such a pair makes the sequence *good*; a sequence with no such pair is *bad*.

**Theorem (Robertson and Seymour, 2004).** The finite graphs are well-quasi-ordered by the minor relation.

**Corollary (finite obstruction sets).** Let $\mathcal{C}$ be a class of graphs that is closed under minors: if $G \in \mathcal{C}$ and $H \preceq G$ then $H \in \mathcal{C}$. Let $\mathrm{Obs}(\mathcal{C})$ be the set of graphs that are not in $\mathcal{C}$ but all of whose proper minors are in $\mathcal{C}$. Then $\mathrm{Obs}(\mathcal{C})$ is finite, and a graph $G$ is in $\mathcal{C}$ if and only if no graph of $\mathrm{Obs}(\mathcal{C})$ is a minor of $G$.

The theorem and the corollary are equivalent; the [proof file](proofs/main.md) shows this.

## In plain words

Take any endless list of networks. The theorem says that, somewhere in the list, an earlier network can be found inside a later one, after deleting some parts and squeezing some links to points. You cannot build an endless list in which no network hides in a later one.

The useful form is about properties that survive deleting and squeezing, such as "can be drawn on a doughnut without crossings". For every such property, there is a finite list of small bad networks, and a network has the property exactly when none of them hides inside it. For "drawable on paper" the list has two networks. For the doughnut it has many thousands, and nobody knows the full list, but the theorem says it is finite.

## Proof

The full proof is far beyond the scope of one page: it runs through Graph Minors I to XX and uses most of the structure theory built there. The [proof file](proofs/main.md) has the status of a sketch. It proves in full:

1. **The Ramsey lemma.** A quasi-order is a well-quasi-order if and only if every infinite sequence has an infinite increasing subsequence, and if and only if it is well-founded and has no infinite antichain. The proof uses the infinite [Ramsey theorem](/ramsey-theorem/) on pairs.
2. **The equivalence with the corollary.** The minor relation is well-founded, because a proper minor has fewer vertices plus edges. The obstruction set of a minor-closed class is an antichain. So the theorem gives finite obstruction sets; conversely, if every minor-closed class has a finite obstruction set, then an infinite antichain $A$ would give the class of graphs with no minor in $A$, whose obstruction set is $A$ itself.
3. **The case of trees.** Finite trees are well-quasi-ordered by the minor relation. This is a form of Kruskal's tree theorem, proved by the minimal bad sequence argument of Nash-Williams.

For general graphs the file gives the outline of Robertson and Seymour.

- **Bounded tree-width.** The tree case extends to graphs of bounded [treewidth](/treewidth/), because a graph of tree-width less than $k$ has a [tree decomposition](/tree-decomposition/) whose bags have at most $k$ vertices, and the minimal bad sequence argument runs on the trees of these decompositions, with labels on the nodes (Graph Minors IV).
- **Excluding a grid.** Take a bad sequence $G_1, G_2, \ldots$. Every later $G_j$ excludes $G_1$ as a minor. A planar graph $H$ is a minor of every large enough grid, and every graph of large tree-width has a large grid minor (Graph Minors V). So if $G_1$ is planar, all $G_j$ have bounded tree-width, and the previous case applies.
- **The structure theorem.** If $G_1$ is not planar, the graphs $G_j$ exclude a fixed non-planar graph. Graph Minors XVI shows that such graphs are built by clique-sums, in a tree-like way, from pieces that nearly embed in a surface of bounded genus, up to a bounded number of apex vertices and vortices of bounded depth.
- **Graphs on a surface.** Well-quasi-ordering is proved for graphs nearly embedded in a fixed surface, by induction on the surface (Graph Minors VIII, XVIII to XX), and then lifted through the tree-like clique-sums with the tree argument. This last step is where most of the length lies.

## Consequences

- **Finite obstruction sets.** Every minor-closed class has a finite list of forbidden minors. Examples: planar graphs ($K_5$, $K_{3,3}$); forests ($K_3$); [outerplanar graphs](/outerplanar-graph/) ($K_4$, $K_{2,3}$); graphs of tree-width at most 2 ($K_4$); graphs with a linkless embedding in space (the 7 graphs of the Petersen family, by Robertson, Seymour and Thomas); graphs that embed in a fixed surface (see [graph genus](/graph-genus/)).
- **Polynomial membership tests.** For each fixed $H$, [minor testing](/minor-testing/) decides $H \preceq G$ in $O(n^3)$ time (Graph Minors XIII), later $O(n^2)$ and then almost linear time. With a finite obstruction set, every minor-closed class has a polynomial membership test. So, for example, for each fixed $k$, deciding whether a graph has genus at most $k$, or a feedback vertex set of size at most $k$, or tree-width at most $k$, takes polynomial time.
- **Non-constructive algorithms.** The theorem proves that the obstruction set exists but does not give it. So these tests are proofs that an algorithm exists, not algorithms one can write down, as Fellows and Langston pointed out. In general there is no procedure that computes the obstruction set of a class from a membership test for it.
- **Fixed-parameter tractability.** Many problems with a parameter $k$ whose yes-instances form a minor-closed class are [fixed-parameter tractable](/fixed-parameter-tractable/) by this route, with an $f(k) \, n^3$ bound in which $f$ is not known.
- **Immersions.** Robertson and Seymour also proved, in Graph Minors XXIII, that finite graphs are well-quasi-ordered by immersion.

## Tightness

- **Minors cannot be replaced by subgraphs.** The cycles $C_3, C_4, C_5, \ldots$ form an infinite antichain for the subgraph relation, since the only cycle that is a subgraph of $C_l$ is $C_l$ itself. In the minor relation, every cycle is a minor of every longer cycle, by contracting edges.
- **Topological minors.** The topological minor relation is a well-quasi-order on trees, by Kruskal's theorem, but not on all graphs: there are infinite antichains (Diestel, Chapter 12). So the theorem needs contraction, not only subdivision.
- **Infinite graphs.** The theorem fails for uncountable graphs (Thomas found a counterexample), and it is open for countable graphs.
- **The obstruction sets are large.** For the projective plane there are 35 minor-minimal obstructions. For the torus, computer searches have found more than 17000, and the full list is not known.
- **Proof strength.** Friedman, Robertson and Seymour showed that the tree case already cannot be proved in some weak systems of arithmetic in which most of mathematics can be done, so a short elementary proof of the general case is not expected.

## History

Joseph Kruskal proved in 1960 that finite trees are well-quasi-ordered by topological embedding, a conjecture of Vázsonyi, and Crispin Nash-Williams gave the short minimal bad sequence proof in 1963. Klaus Wagner, whose 1937 characterization of planar graphs by $K_5$ and $K_{3,3}$ minors is the model for the corollary, is credited with the general conjecture, although he did not publish it. Neil Robertson and Paul Seymour began the Graph Minors series in 1983, proved the bounded tree-width case and the grid theorem in the 1980s, and finished the proof in Graph Minors XX, published in 2004. Michael Fellows and Michael Langston showed in 1988 how the theorem, with the cubic-time minor test, gives polynomial algorithms for many problems.

## References
