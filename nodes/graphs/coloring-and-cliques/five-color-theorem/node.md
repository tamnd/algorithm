---
tag: T8J05P
kind: theorem
slug: five-color-theorem
name: Five color theorem
aliases:
- five-colour theorem
area: graphs/coloring-and-cliques
level: core
summary: Every planar graph is 5-colorable, with an elementary proof.
prereqs: [planar-graph, euler-formula, kempe-chain, graph-coloring]
see_also: [four-color-theorem, kempe-chain, five-color-algorithm, planar-graph-coloring, planar-edge-bound, degeneracy, chromatic-number, hadwiger-conjecture]
sources:
  - paper: "P. J. Heawood, Map-colour theorem, Quarterly Journal of Pure and Applied Mathematics 24, 332 to 338 (1890)"
    locator: the counterexample to Kempe's proof of the four color theorem, the proof of the five color theorem, and the bound for surfaces of higher genus
  - paper: doi:10.2307/2369235
    title: A. B. Kempe, On the geographical problem of the four colours, American Journal of Mathematics 2(3), 193 to 200 (1879)
    locator: the whole paper (the chain interchange argument)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2 (Euler's formula and the edge bound for plane graphs) and Section 5.1, Colouring maps and planar graphs (the five colour theorem with proof)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.3, Coloring of planar graphs (Kempe chains and the five color theorem)
  - paper: doi:10.1006/jctb.1997.1750
    title: Neil Robertson, Daniel P. Sanders, Paul Seymour and Robin Thomas, The four-colour theorem, Journal of Combinatorial Theory, Series B 70(1), 2 to 44 (1997)
    locator: the main theorem and its quadratic-time 4-coloring algorithm
  - paper: doi:10.1006/jctb.1994.1062
    title: Carsten Thomassen, Every planar graph is 5-choosable, Journal of Combinatorial Theory, Series B 62(1), 180 to 181 (1994)
    locator: the whole paper
  - paper: doi:10.1016/0012-365X(93)90579-I
    title: Margit Voigt, List colourings of planar graphs, Discrete Mathematics 120(1-3), 215 to 219 (1993)
    locator: the planar graph that is not 4-choosable
  - paper: doi:10.1215/ijm/1256049011
    title: Kenneth Appel and Wolfgang Haken, Every planar map is four colorable. Part I. Discharging, Illinois Journal of Mathematics 21(3), 429 to 490 (1977)
    locator: the whole paper (with Part II, the first proof of the four color theorem)
---

The five color theorem says that the vertices of every [planar graph](/planar-graph/) can be colored with 5 colors so that adjacent vertices get different colors. Equivalently, the regions of every map in the plane can be colored with 5 colors so that regions with a common border differ. Heawood proved it in 1890 from Kempe's flawed proof of the [four color theorem](/four-color-theorem/). The proof is short and elementary, and it gives a polynomial-time [5-coloring algorithm](/five-color-algorithm/).

## Statement

All graphs are finite and without loops.

**Theorem (Heawood 1890).** Every planar graph $G$ satisfies $\chi(G) \le 5$.

Parallel edges do not change which colorings are proper, so it is enough to prove the theorem for simple planar graphs.

The proof uses one fact about planar graphs.

**Lemma (edge bound).** A simple planar graph with $n \ge 3$ vertices has at most $3n - 6$ edges. So every simple planar graph has a vertex of [degree](/degree/) at most 5.

## In plain words

Draw a network on paper with no crossing lines. You can always give each point one of five colors so that two points joined by a line never share a color.

The proof removes one point with few neighbors, colors the rest, and puts the point back. A flat drawing always has a point with at most five neighbors. If those neighbors use fewer than five colors, a color is free. If they use all five, you swap two colors along a chain of points, which frees a color. A flat drawing cannot block both of the needed swaps at once.

## Proof

*Proof of the lemma.* Let $G$ be a simple plane graph with $n \ge 3$ vertices and $m$ edges. Adding edges keeps a graph planar as long as no crossing is made, so we may assume that $G$ is connected and that no edge can be added; then each face is bounded by a closed walk of length at least 3. Every edge borders at most 2 faces, so $2m \ge 3f$, where $f$ is the number of faces. [Euler's formula](/euler-formula/) $n - m + f = 2$ gives $m = n + f - 2 \le n + 2m/3 - 2$, so $m \le 3n - 6$. The sum of the degrees is $2m \le 6n - 12 < 6n$, so some vertex has degree at most 5. For $n \le 2$ every degree is at most 1. $\square$

*Proof of the theorem.* Induction on $n$. If $n \le 5$, give every vertex its own color. Let $n \ge 6$, and fix a drawing of $G$ in the plane without crossings. By the lemma, $G$ has a vertex $v$ with $\deg(v) \le 5$. The graph $G - v$ is planar, so by induction it has a proper coloring $c$ with colors $\{1, 2, 3, 4, 5\}$.

If the neighbors of $v$ use at most 4 colors, give $v$ a fifth one; the result is proper. Otherwise $\deg(v) = 5$ and the neighbors use all 5 colors. Name them $v_1, v_2, v_3, v_4, v_5$ in the order in which their edges leave $v$ in the drawing, going round $v$, and rename the colors so that $c(v_i) = i$.

For two colors $i \ne j$, let $H_{ij}$ be the subgraph of $G - v$ induced by the vertices of color $i$ or $j$. Swapping $i$ and $j$ on one connected component of $H_{ij}$ gives a proper coloring again: an edge inside the component keeps two different colors, and an edge from the component to a vertex $w$ outside it is fine because $w$ does not have color $i$ or $j$, or else it would be in the same component. These components are the [Kempe chains](/kempe-chain/).

*Case 1: $v_1$ and $v_3$ lie in different components of $H_{13}$.* Swap 1 and 3 on the component of $v_1$. Now $v_1$ has color 3 and $v_3$ still has color 3, so no neighbor of $v$ has color 1. Give $v$ the color 1.

*Case 2: $v_1$ and $v_3$ lie in the same component of $H_{13}$.* Then $H_{13}$ has a path $P$ from $v_1$ to $v_3$, all of whose vertices have color 1 or 3. With the edges $v v_1$ and $v_3 v$, the path $P$ forms a cycle $C$, and in the drawing $C$ is a closed curve without self-crossings. By the Jordan curve theorem, $C$ splits the rest of the plane into an inside and an outside. Round $v$, the edges to $v_1$ and $v_3$ are on $C$, the edge to $v_2$ leaves $v$ between them on one side, and the edges to $v_4$ and $v_5$ leave $v$ between them on the other side. So $v_2$ and $v_4$, which are not on $C$ since their colors are 2 and 4, lie on opposite sides of $C$, one inside and one outside.

Suppose that $H_{24}$ has a path $Q$ from $v_2$ to $v_4$. As a curve, $Q$ joins a point inside $C$ to a point outside, so it meets $C$. In a drawing without crossings two edges meet only at a common end, so $Q$ and $C$ share a vertex. But the vertices of $Q$ have colors 2 and 4, those of $C$ other than $v$ have colors 1 and 3, and $v \notin Q$ because $Q$ lies in $G - v$. This is impossible, so $v_2$ and $v_4$ lie in different components of $H_{24}$. Swap 2 and 4 on the component of $v_2$. Now no neighbor of $v$ has color 2, and $v$ gets color 2.

In all cases $G$ has a proper coloring with 5 colors. $\blacksquare$

**Worked case.** The icosahedron is planar with $n = 12$, $m = 30 = 3n - 6$, and every vertex has degree 5. So the degree 5 case of the proof is the only one available at the first step, and the proof may meet a vertex whose 5 neighbors use all 5 colors. Its chromatic number is 4, so the theorem is not tight for it.

## Consequences

- **Maps.** Every map of connected countries in the plane can be colored with 5 colors so that countries with a common border of positive length differ: the dual graph of the map is planar.
- **Algorithms.** Each step of the proof takes polynomial time: find a vertex of degree at most 5, recurse, and do at most one Kempe chain swap in $O(n)$ time. This gives an $O(n^2)$ algorithm, and more care gives $O(n)$; see the [five color algorithm](/five-color-algorithm/).
- **Degeneracy.** The lemma says that every subgraph of a planar graph has a vertex of degree at most 5, so planar graphs have [degeneracy](/degeneracy/) at most 5, and greedy coloring in a [smallest-last order](/degeneracy-ordering/) uses at most 6 colors. The five color theorem saves one color with the Kempe swap.
- **Surfaces.** Heawood used the same counting on a surface of genus $g \ge 1$ to show $\chi(G) \le \lfloor (7 + \sqrt{1 + 48 g}) / 2 \rfloor$ for every graph that can be drawn on it.

## Tightness

- **Four colors suffice.** The [four color theorem](/four-color-theorem/) (Appel and Haken 1976; a simpler proof by Robertson, Sanders, Seymour and Thomas 1997) improves the bound to 4. Its proofs use a computer to check hundreds of configurations, while the five color proof fits on one page.
- **Four colors are needed.** $K_4$ is planar and needs 4 colors, so no bound below 4 holds for all planar graphs.
- **Where 5 is the right number.** Every planar graph is 5-choosable: it can be colored from any lists of 5 colors per vertex (Thomassen 1994). Some planar graphs are not 4-choosable (Voigt 1993), so for [list coloring](/list-coloring/) of planar graphs, 5 is best possible.
- **The Kempe step for 4 colors fails.** With 4 colors and a vertex of degree 5, Kempe tried two chain swaps at once. Heawood's example shows that the first swap can undo the second.

## History

Kempe published a proof of the four color theorem in 1879 using the chain swaps now named after him. In 1890 Heawood found a map on which Kempe's argument fails, and in the same paper used Kempe's idea to prove that 5 colors always suffice. The four color theorem itself stayed open until Appel and Haken proved it with a computer in 1976. The five color theorem stays the standard textbook example of the Kempe chain method.

## References
