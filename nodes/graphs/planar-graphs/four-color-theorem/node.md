---
tag: V9X3E0
kind: theorem
slug: four-color-theorem
name: Four color theorem
aliases:
- Appel-Haken theorem
- four colour theorem
- four-colour theorem
area: graphs/planar-graphs
level: core
summary: Every planar graph is 4-colorable.
prereqs: [planar-graph, graph-coloring, five-color-theorem, kempe-chain, euler-formula]
see_also: [five-color-algorithm, chromatic-number, hadwiger-conjecture, planar-dual-graph, maximal-planar-graph, graph-genus, jordan-curve-theorem, np-complete]
sources:
  - paper: doi:10.1215/ijm/1256049011
    title: Kenneth Appel and Wolfgang Haken, Every planar map is four colorable. Part I. Discharging, Illinois Journal of Mathematics 21(3), 429 to 490 (1977)
    locator: the discharging procedure and the unavoidable set (Part II, with John Koch, is the reducibility part in the same issue)
  - paper: doi:10.1006/jctb.1997.1750
    title: Neil Robertson, Daniel P. Sanders, Paul Seymour and Robin Thomas, The four-colour theorem, Journal of Combinatorial Theory, Series B 70(1), 2 to 44 (1997)
    locator: the proof with 633 reducible configurations and 32 discharging rules, and the quadratic-time 4-coloring algorithm
  - paper: "Georges Gonthier, Formal proof, the four-color theorem, Notices of the American Mathematical Society 55(11), 1382 to 1393 (2008)"
    locator: the proof checked in the Coq proof assistant
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 5, Colouring, Section 5.1, Colouring maps and planar graphs (statement of the four colour theorem and the proof of the five colour theorem)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 7.3, Planarity, coloring, and cycles (the four color problem, Kempe chains, discharging and Tait's theorem)
  - paper: doi:10.2307/2369235
    title: A. B. Kempe, On the geographical problem of the four colours, American Journal of Mathematics 2(3), 193 to 200 (1879)
    locator: the chain interchange argument and the false proof
  - paper: "Percy J. Heawood, Map-colour theorem, Quarterly Journal of Pure and Applied Mathematics 24, 332 to 338 (1890)"
    locator: the counterexample to Kempe's argument
  - book: "Robin Wilson, Four Colors Suffice, How the Map Problem Was Solved, Princeton University Press, 2002"
    locator: the history from Guthrie and De Morgan to Appel and Haken
---

The four color theorem says that every [planar graph](/planar-graph/) without loops has a proper vertex [coloring](/graph-coloring/) with 4 colors: adjacent vertices get different colors. In the language of maps, the regions of every map in the plane can be colored with 4 colors so that regions with a common border of positive length differ. Appel and Haken proved it in 1976 with a large computer check; Robertson, Sanders, Seymour and Thomas gave a simpler computer proof in 1996, and Gonthier checked a full proof in the Coq proof assistant in 2005. No proof without a computer is known.

## Statement

**Theorem (Appel and Haken).** For every planar graph $G$ without loops, the [chromatic number](/chromatic-number/) satisfies $\chi(G) \le 4$.

The theorem is about graphs, so it does not depend on an embedding: if some plane drawing of $G$ exists, $G$ is 4-colorable. The proof works with a plane embedding, given as a drawing or as a [rotation system](/rotation-system/), because it uses the faces around each vertex. Parallel edges do not change colorability, so it suffices to prove the theorem for simple graphs.

**Map form.** A map is a connected plane graph without bridges; its regions are its faces. Two faces are neighbours when they share an edge. Coloring the faces of a plane graph $M$ is coloring the vertices of its [planar dual](/planar-dual-graph/) $M^*$, which is planar and has no loop exactly when $M$ has no bridge. So the map form and the graph form are equivalent.

## In plain words

Take any map of countries on a flat sheet, where each country is one piece. You can color the countries with only four colors so that two countries with a common border always get different colors. Countries that touch only at a corner may get the same color.

Three colors are not always enough: four countries can each touch the other three. The surprise is that four always suffice, however large and twisted the map is.

The proof shows that a smallest map that needs five colors cannot exist. Every map contains at least one of a long, fixed list of small patterns, and each pattern can be removed, the rest colored, and the pattern put back. A computer checks both facts for the list of patterns.

## Proof

The full proof does not fit on a page: its two finite parts are checked by computer. We prove its first steps, which are elementary, and then give the structure of the rest with locators.

**Step 1: a minimal counterexample is a triangulation.** Suppose the theorem is false, and let $G$ be a simple planar graph that is not 4-colorable with the least number $n$ of vertices. Then $n \ge 5$, since a graph with at most 4 vertices is colored by giving each vertex its own color. Add edges to a plane drawing of $G$ until it is [maximal planar](/maximal-planar-graph/). The new graph has the same $n$ vertices and is not 4-colorable, since a coloring of it would color $G$. So we may assume that $G$ is a triangulation: every face is a triangle, and $G$ has $3n - 6$ edges.

**Step 2: minimum degree 5.** Let $v$ be a vertex of $G$. By the choice of $n$, $G - v$ has a proper 4-coloring $c$. If the neighbours of $v$ use at most 3 colors, give $v$ the fourth, and $G$ is 4-colorable, a contradiction. So $v$ has at least 4 neighbours. Suppose $\deg(v) = 4$, with neighbours $x_1, x_2, x_3, x_4$ in the cyclic order of the edges at $v$, of four different colors $c_1, \ldots, c_4$. Consider the [Kempe chain](/kempe-chain/) of $x_1$ in the colors $c_1, c_3$, the component of $x_1$ in the subgraph of $G - v$ induced by those two colors. Swapping $c_1$ and $c_3$ on a Kempe chain keeps the coloring proper. If the chain does not contain $x_3$, the swap makes $x_1$ color $c_3$, and $c_1$ is free for $v$. Otherwise a path of colors $c_1, c_3$ from $x_1$ to $x_3$ and the edges $v x_1$, $v x_3$ form a cycle $C$. By the [Jordan curve theorem](/jordan-curve-theorem/), $x_2$ and $x_4$ lie on different sides of $C$, since the edges $v x_2$ and $v x_4$ leave $v$ on different sides of the two edges of $C$ at $v$. A path of colors $c_2, c_4$ has no vertex on $C$, so it cannot cross $C$, and the chain of $x_2$ in colors $c_2, c_4$ does not contain $x_4$. Swapping on that chain frees $c_2$ for $v$. Either way $G$ is 4-colorable, a contradiction. So every vertex of $G$ has degree at least 5.

**Step 3: the charge.** Give each vertex $v$ the charge $6 - \deg(v)$. The degrees sum to $2(3n - 6)$, so

$$\sum_{v} (6 - \deg(v)) = 6n - 2(3n - 6) = 12.$$

So the total charge is positive, and by Step 2 the positive charge sits on vertices of degree 5. In particular $G$ has a vertex of degree 5.

**Why Kempe's argument stops here.** For a vertex of degree 5 with four colors on its neighbours, one color appears twice. Kempe made two chain interchanges, one for each copy of that color. Heawood (1890) gave a coloring where the first interchange changes the chains that the second one uses, so that the argument fails. The [five color theorem](/five-color-theorem/) survives because with five colors a vertex of degree 5 needs only one interchange.

**Step 4: reducible configurations.** A *configuration* is a part of a triangulation near a vertex: a set of vertices with the degrees that they have in $G$, and the triangles among them. A configuration $K$ is *reducible* if no minimal counterexample can contain it: every 4-coloring of the rest of the graph, after a fixed modification, extends to $K$, possibly after Kempe interchanges. Step 2 shows that a vertex of degree at most 4 is reducible. Birkhoff (1913) found the first reducible configurations of larger size. Reducibility of a given configuration is a finite check over the colorings of the ring of vertices around it.

**Step 5: an unavoidable set by discharging.** A set $\mathcal{U}$ of configurations is *unavoidable* if every triangulation of minimum degree 5 contains one of them. The proof of unavoidability moves charge from Step 3 between nearby vertices by fixed rules, keeping the total at 12, and shows that every vertex that ends with positive charge has a configuration of $\mathcal{U}$ near it. Since the total is positive, some vertex has positive charge.

**Conclusion.** Robertson, Sanders, Seymour and Thomas give a set $\mathcal{U}$ of 633 configurations, check by computer that each is reducible, and prove with 32 discharging rules that $\mathcal{U}$ is unavoidable; this proof, too, is checked by computer. So a minimal counterexample contains a configuration that it cannot contain, and no counterexample exists. Appel and Haken's original proof used the same two steps with a larger set. Gonthier checked the whole argument, including the graph theory and the topology, in Coq. $\blacksquare$

## Consequences

- **Algorithms.** The proof gives an algorithm: find a configuration of $\mathcal{U}$, reduce, color the smaller graph, and extend. Robertson, Sanders, Seymour and Thomas give a 4-coloring algorithm that runs in $O(n^2)$ time. A 5-coloring takes linear time by the [five-color algorithm](/five-color-algorithm/), which is far simpler.
- **The decision problem.** Deciding whether a planar graph is 4-colorable is trivial: the answer is yes. Deciding whether it is 3-colorable is [NP-complete](/np-complete/), even for planar graphs of maximum degree 4. So the chromatic number of a planar graph is easy to bound and hard to compute.
- **Tait's form.** A planar cubic graph without bridges has an edge coloring with 3 colors. Tait showed in 1880 that this statement is equivalent to the four color theorem (West, Section 7.3).
- **Hadwiger's conjecture for $k = 5$.** Every graph without a $K_5$ [minor](/graph-minor/) is 4-colorable. Wagner's structure theorem for graphs without a $K_5$ minor reduces this case to planar graphs and one more graph, so it is equivalent to the four color theorem. See [Hadwiger's conjecture](/hadwiger-conjecture/).
- **Independent sets.** Each color class is independent, so every planar graph with $n$ vertices has an independent set of at least $n/4$ vertices. No proof of this without the four color theorem is known.

## Tightness

The bound 4 is attained, and no smaller number works in general.

| planar graph | $n$ | $\chi$ | reason |
|---|---|---|---|
| a single vertex | 1 | 1 | no edge |
| a tree with an edge | at least 2 | 2 | bipartite |
| an odd cycle | odd, at least 3 | 3 | an odd cycle is not bipartite |
| octahedron $K_{2,2,2}$ | 6 | 3 | the three pairs of opposite vertices are the color classes |
| $K_4$ | 4 | 4 | all four vertices are pairwise adjacent |
| icosahedron | 12 | 4 | its independent sets have at most 3 vertices, and $12/3 = 4$ |
| $K_5$, $K_{3,3}$ | 5, 6 | 5, 2 | not planar; $K_5$ shows that 4 fails beyond planar graphs |

- **Loops.** A graph with a loop has no proper coloring at all, so the theorem excludes loops.
- **Lists.** The analogue for list coloring fails: Voigt (1993) gave a planar graph that is not 4-choosable, while Thomassen proved that every planar graph is 5-choosable (see [five color theorem](/five-color-theorem/)).
- **Other surfaces.** On the torus, $K_7$ embeds, so 7 colors are needed there. Heawood bounded the number of colors for each surface of genus $g \ge 1$; see [graph genus](/graph-genus/).
- **Triangle-free planar graphs** need only 3 colors (Grötzsch's theorem), so the extremal examples contain triangles.

## History

Francis Guthrie posed the question in 1852, and it reached the mathematical public through Augustus De Morgan and, in 1878, Arthur Cayley. Kempe published a proof in 1879 with the chain interchange, and Tait gave the edge-coloring form in 1880. Heawood found the error in Kempe's proof in 1890 and proved the five color theorem. Birkhoff introduced reducibility in 1913, and Heesch developed discharging in the 1960s. Appel and Haken, with Koch, completed the proof in 1976 and published it in 1977. Robertson, Sanders, Seymour and Thomas gave a new proof in 1996 (published 1997) with a smaller unavoidable set and checkable programs. Gonthier, with Benjamin Werner, completed the formal proof in Coq in 2005.

## References
