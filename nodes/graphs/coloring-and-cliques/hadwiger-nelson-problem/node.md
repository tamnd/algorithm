---
tag: DHZRR9
kind: problem
slug: hadwiger-nelson-problem
name: Hadwiger-Nelson problem
aliases:
- chromatic number of the plane
area: graphs/coloring-and-cliques
level: research
summary: Minimum number of colors needed to color the plane so that no two points at unit distance share a color; known to lie between 5 and 7.
prereqs: [graph-coloring, chromatic-number]
see_also: [sat, cdcl, k-coloring, mycielski-graph, four-color-theorem, hadwiger-conjecture, random-geometric-graph]
sources:
  - paper: "A. D. N. J. de Grey, The chromatic number of the plane is at least 5, Geombinatorics 28(1), 18 to 31 (2018)"
    locator: the 1581-vertex unit-distance graph with chromatic number 5
  - book: isbn:9780387746401
    title: Alexander Soifer, The Mathematical Coloring Book, Springer, 2009
    locator: Part II, the chromatic number of the plane (history, the bounds 4 and 7, and the measurable and axiomatic variants)
  - paper: "N. G. de Bruijn and P. Erdős, A colour problem for infinite graphs and a problem in the theory of relations, Indagationes Mathematicae 13, 369 to 373 (1951)"
    locator: the compactness theorem (an infinite graph is k-colorable if every finite subgraph is)
  - paper: "L. Moser and W. Moser, Solution to problem 10, Canadian Mathematical Bulletin 4, 187 to 189 (1961)"
    locator: the seven-vertex unit-distance graph with chromatic number 4 (the Moser spindle)
  - paper: "K. J. Falconer, The realization of distances in measurable subsets covering R^n, Journal of Combinatorial Theory, Series A 31, 184 to 189 (1981)"
    locator: the measurable chromatic number of the plane is at least 5
---

The Hadwiger-Nelson problem asks for the chromatic number of the plane: the least number of colors for the points of $\mathbb{R}^2$ such that no two points at distance exactly 1 get the same color. Since the 1950s it has been known to lie between 4 and 7. In 2018 Aubrey de Grey raised the lower bound to 5 with a finite graph of 1581 points whose 5-chromaticity was checked by computer, so the answer is 5, 6 or 7. The problem is a [graph coloring](/graph-coloring/) problem on an infinite graph, and the progress on it is a story of finite subgraphs and [SAT solvers](/sat/).

## In plain words

Paint every point of an endless flat sheet. The only rule is that two points exactly one centimeter apart must have different paints. How few paints are enough?

Seven always suffice: tile the sheet with honeycomb cells a little less than one centimeter across, and paint them in a repeating pattern of seven so that cells of the same paint are far apart. Four are not enough, because a small drawing of seven points already forces a fourth paint. Since 2018 we also know that four paints fail, using a much larger drawing checked by computer. Whether five or six suffice is still open.

## Definition

The **unit-distance graph of the plane** has vertex set $\mathbb{R}^2$, with $x$ and $y$ adjacent when $\lVert x - y \rVert = 1$. Its [chromatic number](/chromatic-number/) is

$$\chi(\mathbb{R}^2) = \min\{\, k : \exists\, c : \mathbb{R}^2 \to \{1, \ldots, k\} \text{ with } c(x) \ne c(y) \text{ whenever } \lVert x - y \rVert = 1 \,\}.$$

A **unit-distance graph** is any finite graph whose vertices are points of the plane and whose edges join some pairs at distance 1. Every unit-distance graph is a subgraph of the unit-distance graph of the plane, so its chromatic number is a lower bound for $\chi(\mathbb{R}^2)$.

**Compactness.** By the theorem of de Bruijn and Erdős (1951), assuming the axiom of choice, an infinite graph is $k$-colorable if and only if every finite subgraph is. So $\chi(\mathbb{R}^2)$ equals the largest chromatic number of a finite unit-distance graph, and lower bounds always come from finite graphs.

## Variants

- **Higher dimensions.** $\chi(\mathbb{R}^n)$ for the unit-distance graph of $\mathbb{R}^n$. It grows exponentially in $n$: Frankl and Wilson gave a lower bound of the form $(1.2 + o(1))^n$, and Larman and Rogers an upper bound $(3 + o(1))^n$.
- **Measurable chromatic number.** Require each color class to be Lebesgue measurable. Falconer (1981) proved that this version is at least 5, long before de Grey's result for the unrestricted version.
- **Other distances and norms.** Forbid a set of distances, or use another norm. In the plane, the answer does not depend on which single distance is forbidden, by scaling.
- **Restricted point sets.** Color only the rational points $\mathbb{Q}^2$, for which 2 colors suffice, or other subfields.
- **Set theory.** Shelah and Soifer showed that, for related distance graphs, the chromatic number can depend on the axioms of set theory, so a full answer may need to say which axioms are assumed.

## Examples

**The Moser spindle (lower bound 4).** Take two rhombi, each made of two equilateral triangles of side 1, sharing a vertex $A$, and rotate one about $A$ until their far tips are at distance 1. This gives 7 points and 11 unit-distance edges. In a 3-coloring, each rhombus forces its far tip to have the color of $A$, so the two tips get the same color, but they are adjacent. So the spindle needs 4 colors, and 4 suffice. An exhaustive check over all colorings agrees: it has no 3-coloring and has a 4-coloring.

**The hexagonal coloring (upper bound 7).** Tile the plane by regular hexagons of side $s$ and color them with 7 colors in the pattern where the hexagons of one color form a lattice spanned by the steps "two cells right, one cell up-right". Each hexagon has diameter $2s$, and two hexagons of the same color are at distance $\sqrt{7}\, s$. So if

$$\frac{1}{\sqrt 7} < s < \frac12,$$

then two points in the same hexagon are closer than 1 and two points in different hexagons of the same color are farther than 1. Points on the boundaries are given the color of one adjacent hexagon in a consistent way.

**Small cases.** The triangle of side 1 shows $\chi(\mathbb{R}^2) \ge 3$, and the odd cycles are not enough to go beyond 3, so a cleverer graph like the spindle is needed for 4.

## Known algorithms

There is no algorithm for the infinite problem itself. The work goes into finding finite unit-distance graphs that are not $k$-colorable and proving that they are not.

- **Building candidates.** De Grey started from graphs with many copies of the spindle and found that in some of them every 4-coloring has a monochromatic triangle of a fixed shape, then glued copies to forbid that. His graph has 1581 vertices.
- **Proving non-colorability.** Encode "$G$ is 4-colorable" in conjunctive normal form, with one variable per (vertex, color) pair, and run a [CDCL](/cdcl/) solver. An unsatisfiable answer, with a checkable proof, shows $\chi(G) \ge 5$. This is the same encoding as for [k-coloring](/k-coloring/).
- **Shrinking.** Heule used SAT solving to remove vertices while keeping the graph 5-chromatic, getting down to a few hundred vertices; a smallest 5-chromatic unit-distance graph is not known.
- **Upper bounds.** Upper bounds come from explicit periodic colorings, like the hexagons; no coloring with 6 colors is known.

## Bounds

- $5 \le \chi(\mathbb{R}^2) \le 7$. The lower bound is de Grey (2018), confirmed independently by Exoo and Ismailescu; the bound 4 is due to Moser and Moser (1961) and the bound 7 to Isbell, around 1950.
- Measurable colorings: $5 \le \chi_m(\mathbb{R}^2) \le 7$ (Falconer 1981 for the lower bound).
- If one requires each color class to be a union of nice regions (for example, regions bounded by Jordan curves), Woodall and Townsend showed that at least 6 colors are needed.

## Reductions

- **To finite graph coloring.** By de Bruijn and Erdős, $\chi(\mathbb{R}^2) \le k$ if and only if every finite unit-distance graph is $k$-colorable.
- **Finite graph coloring to SAT.** For a fixed finite graph and $k$, $k$-colorability reduces to [SAT](/sat/) with $nk$ variables, at-least-one-color clauses for each vertex, and a clause $\lnot x_{u,c} \lor \lnot x_{v,c}$ for each edge and color.
- **Not to the four color theorem.** The unit-distance graph is not planar and its edges are not region borders, so the [four color theorem](/four-color-theorem/) says nothing about it. Hadwiger's name here is unrelated to the [Hadwiger conjecture](/hadwiger-conjecture/) on minors.

## Applications

- **SAT solving as a proof tool.** The 2018 bound is one of several open problems in combinatorics settled by a mix of human construction and certified SAT proofs, and the shrinking of the graph was a benchmark for proof-producing solvers.
- **Collaborative mathematics.** The Polymath16 project, started right after de Grey's paper, worked on smaller 5-chromatic graphs and on human-checkable proofs.
- **Geometric graph theory.** Unit-distance graphs are a model for interference between transmitters at a fixed range, related to [random geometric graphs](/random-geometric-graph/).

## References
