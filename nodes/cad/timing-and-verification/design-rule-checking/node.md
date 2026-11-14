---
tag: R64P5R
kind: problem
slug: design-rule-checking
name: Design rule checking
aliases:
- DRC
- layout design rule check
area: cad/timing-and-verification
level: core
summary: Check that the polygons of a layout obey the rules of the process, such as minimum width, spacing, enclosure and density, and report every violation.
prereqs: [rectilinear-polygon, polygon-union, minkowski-sum]
see_also: [rectangle-intersection-reporting, bentley-ottmann-algorithm, sweep-line-technique, segment-tree, morphological-opening, morphological-closing, corner-stitching, multiple-patterning-decomposition]
sources:
  - paper: "Henry S. Baird, Fast algorithms for LSI artwork analysis, Proceedings of the 14th Design Automation Conference, 303 to 311, 1977"
    locator: design rule checking of mask artwork as a geometric problem, with sorting and scanline methods for the checks between edges
  - paper: "Ulrich Lauther, An O(N log N) algorithm for Boolean mask operations, Proceedings of the 18th Design Automation Conference, 555 to 562, 1981"
    locator: the scanline for union, intersection and difference of mask layers, the building block of layer operations in rule checkers
  - paper: doi:10.1109/TC.1980.1675628
    title: Jon L. Bentley and Derick Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7), 1980, 571-577
    locator: the O(n log n + k) reporting of intersecting rectangles, used here for spacing checks after growing the shapes
  - paper: "M. Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (1983), doi:10.1145/800061.808735"
    locator: pages 80 to 86, the lower bound from the number of connected components of the set of yes inputs
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: the sections on design rules and physical verification (general locator)
---

Design rule checking, or DRC, is the step of chip design that checks the polygons of a layout against the geometric rules of the manufacturing process: each shape must be wide enough, two shapes must be far enough apart, one layer must enclose another by a margin, and so on. The output is the list of all violations, each with its place, so that the designer or the router can fix them. It is an EDA problem on the mask layers of a chip, a part of physical verification with [layout versus schematic](/layout-versus-schematic/). This page states the problem, its rules and what is known about its cost. The methods are on the pages that it links.

## In plain words

A chip is made by printing shapes, layer by layer, through masks. The factory can print a shape only if it is not too thin, and two shapes only if they are not too close, or they may break or touch. A wire must also stick out far enough past the hole that connects it to the layer below, or the hole may miss it.

The factory writes these limits as a list of rules. A rule checker reads the drawing of the chip and the list, and reports each place where a rule fails.

Two things make this harder than it looks. A shape on a layer is often drawn as many overlapping pieces, and only their union counts. And a chip has billions of shapes, so the checker must be fast and must not miss a case or report a false one.

## Definition

**Input.**

- A *layout*: for each layer $\ell$ (diffusion, polysilicon, metal 1, contact, and so on) a finite set of polygons with integer vertex coordinates. The *region* $R_\ell$ of the layer is the union of its polygons. Most layouts are *Manhattan*: every edge is horizontal or vertical, so each region is a union of [rectilinear polygons](/rectilinear-polygon/). Let $n$ be the total number of polygon edges.
- A *rule deck*: a list of rules, each with a layer or a pair of layers and a distance or a number.

**Rules.** For a region $R$, write $R \oplus d$ for $R$ grown by distance $d$ (the [Minkowski sum](/minkowski-sum/) with a disk or a square of radius $d$) and $R \ominus d$ for $R$ shrunk by $d$. The usual rules are:

- *Width* $w$ on $\ell$: every point of $R_\ell$ lies in a disk (or square) of diameter $w$ inside $R_\ell$. The violations are $R_\ell \setminus ((R_\ell \ominus w/2) \oplus w/2)$.
- *Spacing* $s$ on $\ell$: two points of $R_\ell$ that are not joined by a path of length less than $s$ inside $R_\ell$ have distance at least $s$. Between two different connected parts of $R_\ell$ this is the plain distance. Inside one part it forbids *notches*, narrow gaps between two edges of the same polygon.
- *Spacing* $s$ between two layers $\ell$ and $m$: $\operatorname{dist}(R_\ell, R_m) \ge s$, or the two must not overlap if $s = 0$.
- *Enclosure* $e$ of $m$ by $\ell$, for example of a contact by metal: $R_m \oplus e \subseteq R_\ell$.
- *Area* $a$: every connected part of $R_\ell$ has area at least $a$.
- *Density*: in every square window of a given size, the fraction of area covered by $R_\ell$ lies between two bounds.

Distances are Euclidean, or measured in the $L_\infty$ norm, or only between edges whose projections overlap. The rule deck says which, and the three give different answers at corners.

**Output.** Every violation, as a region or as a pair of edges with the rule it breaks. Let $k$ be the number of violations. The decision version asks whether $k = 0$, that is whether the layout is *DRC-clean*.

## Variants

- **Flat and hierarchical.** A layout is a hierarchy of cells, each placed many times. A hierarchical checker checks the inside of each cell once and then only the places where cells meet. The output is the same as for the flat layout.
- **Incremental.** After an edit, only the rules near the change are checked again. Interactive editors such as Magic do this on a [corner-stitched](/corner-stitching/) plane.
- **Conditional rules.** Modern rule decks make the spacing depend on the width and the length of the two shapes that face each other, or on the end of a line against its side. The rule is still a function of the local geometry.
- **Antenna rules.** The ratio of the area of metal connected to a gate, before the upper layers join it to a diode, must stay below a bound. These rules need connectivity, so they use [circuit extraction](/circuit-extraction/).
- **Same-mask rules for multiple patterning.** With two or more masks per layer, the spacing between shapes on the same mask is larger than between shapes on different masks. Assigning the masks is [multiple patterning decomposition](/multiple-patterning-decomposition/).

## Examples

Take one metal layer with the rules width 3, Euclidean spacing 3 and area 20, and these rectangles, written $(x_0, y_0, x_1, y_1)$:

| shape | rectangles | area | width |
| --- | --- | --- | --- |
| A | $(0, 0, 10, 4)$ | 40 | 4 |
| B | $(12, 0, 22, 2)$ | 20 | 2 |
| C | $(12, 6, 16, 10)$ | 16 | 4 |
| D | $(0, 7, 2, 13)$ and $(2, 7, 4, 13)$ | 24 | 4 |

The checker reports four violations:

- **Width of B.** B is 2 high, less than 3.
- **Spacing of A and B.** The right edge of A at $x = 10$ and the left edge of B at $x = 12$ face each other over the $y$ range $[0, 2]$, at distance 2.
- **Spacing of A and C, at a corner.** The corner $(10, 4)$ of A and the corner $(12, 6)$ of C are at distance $\sqrt{8} \approx 2.83$. A rule measured only between edges whose projections overlap does not report this pair, because the $x$ ranges $[0, 10]$ and $[12, 16]$ and the $y$ ranges $[0, 4]$ and $[6, 10]$ are disjoint.
- **Area of C.** C has area 16, less than 20.

Shape D is two rectangles of width 2 that share the edge $x = 2$. Checked one at a time, each would break the width rule. Their union is a $4 \times 6$ rectangle, so the merged layer has no width violation there. The distance from D to A is 3, which is allowed. The other pairs are far apart: B and C at distance 4, and C and D at distance 8. A scratch script checked these numbers with exact integer distances and a cell-by-cell width test.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| Layer operations by [sweep](/sweep-line-technique/) | union, intersection and difference of layers by a scanline over the edges (Lauther 1981) | $O((n + I) \log n)$ time, with $I$ the number of edge crossings, as for the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) |
| Grow and shrink | width and notch checks as shrink then grow, enclosure as grow then difference | for a rectilinear polygon, growing by a square is the union of the polygon and one rectangle per edge, so it is a [polygon union](/polygon-union/) of $O(n)$ rectangles |
| Spacing by box intersection | grow each shape by $s/2$, report the pairs of grown boxes that meet, then test each pair exactly | [rectangle intersection reporting](/rectangle-intersection-reporting/) in $\Theta(n \log n + k')$, with $k' \ge k$ candidate pairs |
| Edge-pair checks | sort the edges, and in a scanline compare each edge with the edges within the rule distance (Baird 1977) | output-sensitive, measured on layouts |
| Raster checks | draw the layers into pixels and test windows | time proportional to the area in pixels; exact only for coordinates on the pixel grid |
| Hierarchical checks | check each cell once, then the overlaps of cells | the gain depends on the reuse of cells, measured |

The grow and shrink checks are [morphological opening](/morphological-opening/) and [closing](/morphological-closing/) of the layer. In image processing these act on pixels. In DRC they act on exact polygons with integer coordinates, so no pixel grid limits the result.

## Bounds

**Lower bound (proved).** Deciding whether a layout breaks a spacing rule between two layers needs $\Omega(n \log n)$ steps in the [algebraic decision tree](/algebraic-decision-tree/) model, also for rectangles. Fix the rule distance 1, the first layer as the $n + 1$ unit squares $[6i, 6i + 1] \times [0, 1]$, and let the second layer be the $n$ unit squares $[b_j, b_j + 1] \times [0, 1]$, with the $b_j$ as the input. There is no violation if and only if each $b_j$ lies in one of the $n$ intervals $[6i + 2, 6i + 4]$, or left of $-2$, or right of $6n + 2$. So the set of clean inputs is a product of $n$ unions of $n + 2$ disjoint intervals, and it has $(n + 2)^n$ connected components. By Ben-Or's theorem every algebraic decision tree that decides it has depth $\Omega(\log((n + 2)^n) - n) = \Omega(n \log n)$. The argument is the one of the [rectangle intersection detection](/rectangle-intersection-detection/) page. The squares of the second layer may overlap and merge, but merging does not change the distance between the two layers, so the reduction holds for merged layers too.

**Upper bounds (proved).** For a layout of $n$ rectangles and an $L_\infty$ spacing rule, the violating pairs are the pairs of rectangles whose copies grown by $s/2$ on each side overlap with an open overlap, so they are reported in $O(n \log n + k)$ time. For a Euclidean rule the grown boxes give a superset of $k' \ge k$ candidate pairs, each tested exactly with integers by comparing $dx^2 + dy^2$ with $s^2$, in $O(n \log n + k')$ time. Every rule in the definition is a fixed sequence of layer operations and offsets, so for Manhattan layouts the full check of one rule runs in $O((n + I) \log n + k)$ time, where $I$ is the number of crossings of edges among the shapes the sequence builds.

**What is measured.** On real layouts $I$ and $k'$ are small compared with $n$, and hierarchical and parallel checkers run in time close to linear in the number of shapes. This is an observation from practice. The count of distinct rules in a modern deck, often in the thousands, multiplies the cost.

## Reductions

- **From bichromatic rectangle intersection.** An overlap rule between two layers ($s = 0$) asks whether some rectangle of one layer meets some rectangle of the other. This gives the lower bound above.
- **To rectangle intersection reporting.** An $L_\infty$ spacing check on rectangles is rectangle intersection reporting on the shapes grown by $s/2$.
- **To morphology on polygons.** Width, notch and enclosure checks are compositions of [dilation](/morphological-dilation/), [erosion](/morphological-erosion/) and Boolean operations of regions. On Manhattan layouts with the $L_\infty$ measure the structuring element is a square.
- **To connectivity.** Antenna rules and rules that depend on the net of a shape need the nets, from [circuit extraction](/circuit-extraction/).

## Applications

- **Sign-off.** A foundry accepts a layout only if it is DRC-clean under the foundry rule deck.
- **Routing.** [Detailed routers](/detailed-routing/) keep the wires DRC-clean as they go, and fix the remaining violations in a last pass.
- **Layout editing.** Interactive editors check the rules as the designer draws.
- **Design for manufacturing.** Density rules lead to dummy fill shapes, and recommended rules mark places that are legal but likely to print badly, which [optical proximity correction](/optical-proximity-correction/) then treats.

## References
