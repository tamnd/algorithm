---
tag: T6B4N4
kind: problem
slug: multiple-patterning-decomposition
name: Multiple patterning layout decomposition
aliases:
- double patterning decomposition
- triple patterning decomposition
- layout decomposition for multiple patterning lithography
area: cad/timing-and-verification
level: advanced
summary: Split the features of one layer onto two or more masks so that features closer than the minimum same-mask spacing differ in mask, a graph coloring problem.
prereqs: [graph-coloring, bipartiteness-testing, design-rule-checking]
see_also: [k-coloring, three-coloring, maximum-cut, odd-cycle-transversal, planar-graph, binary-integer-programming, semidefinite-programming, optical-proximity-correction]
sources:
  - paper: "Andrew B. Kahng, Chul-Hong Park, Xu Xu and Hailong Yao, Layout decomposition for double patterning lithography, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD) 2008, 465 to 472"
    locator: the conflict graph of a layer, the candidate stitches, and the decomposition that minimizes conflicts and stitches by integer linear programming
  - paper: doi:10.1109/TCAD.2014.2387840
    title: Bei Yu, Kun Yuan, Duo Ding and David Z. Pan, Layout decomposition for triple patterning lithography, IEEE Transactions on Computer-Aided Design 34(3), 433 to 446, 2015
    locator: the proof that triple patterning layout decomposition is NP-hard, and the decomposition by semidefinite programming and graph division (journal version of the ICCAD 2011 paper by Yu, Yuan, Zhang, Ding and Pan)
  - paper: "M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267, 1976"
    locator: the NP-completeness of 3-coloring for planar graphs with maximum degree 4
  - paper: "F. Hadlock, Finding a maximum cut of a planar graph in polynomial time, SIAM Journal on Computing 4(3), 221 to 225, 1975"
    locator: the reduction of maximum cut on planar graphs to a matching problem in the dual graph
---

Multiple patterning layout decomposition assigns each feature of one layout layer to one of $k$ masks. Lithography can print a layer only if same-mask features are far enough apart, and the features of a modern layer are closer than that. So the layer is printed in $k$ exposures, and two features that are too close must go to different masks. This is $k$-coloring of the *conflict graph*. If no valid coloring exists, a feature can be cut into parts, joined by a *stitch*, that go to different masks. This is a lithography and design-for-manufacturing problem. It is placed in timing-and-verification because it runs in the physical verification flow, next to [design rule checking](/design-rule-checking/). With $k = 2$ it is double patterning, and with $k = 3$ triple patterning.

## In plain words

The printing machine cannot draw two shapes closer than some distance in one pass. But the chip needs shapes closer than that. The fix is to print the layer in two or three passes, each with its own mask, and give each shape to one pass.

The rule is simple: two shapes that are too close must be in different passes. Draw a dot for each shape and a line between each pair that is too close. Then give each dot a color, one color per pass, so that no line joins two dots of one color. With two colors this is easy to check, and it fails exactly when the lines form a loop with an odd number of dots. Then a shape can be cut in two and printed in two passes, but each cut costs some quality.

## Definition

**Input.** A set of features (polygons) of one layer, a same-mask spacing $s$, a number of masks $k$, and optionally the candidate stitch positions of each feature with a cost $\beta$ per stitch.

**Conflict graph.** One vertex per feature, or per part of a feature when it has stitch candidates, and one *conflict edge* between two features of different polygons at distance less than $s$. The parts of one polygon are joined by *stitch edges*.

**Output.** A map from vertices to masks $\{0, \dots, k-1\}$.

- *Decision version.* Is there a map in which no conflict edge joins two vertices of one mask?
- *Optimization version.* Minimize the number of conflict edges whose ends share a mask, plus $\beta$ times the number of stitch edges whose ends differ in mask. Conflicts that remain must be fixed by changing the layout.

## Variants

- **Double patterning (litho-etch-litho-etch).** $k = 2$, the case above.
- **Triple and quadruple patterning.** $k = 3$ or $4$, for denser layers.
- **Self-aligned double patterning.** The second pattern is formed from spacers on the sides of the first one. The rules are not a plain coloring, and decomposition adds the constraints of the spacer process.
- **Balanced decomposition.** Also keep the density of the masks close to each other, for better printing.
- **Decomposition-aware layout.** Routers and placers avoid odd cycles while they build the layout, so that the decomposition step has no conflicts left.

## Examples

**An odd cycle.** Let $s = 4$, so two features conflict when the squared Euclidean distance between them is less than $16$. Take the rectangles $(x_0, y_0, x_1, y_1)$

- $w = (0, 0, 30, 2)$, a long wire,
- $p = (0, 4, 2, 6)$ and $q = (28, 4, 30, 6)$ above its two ends,
- $r_i = (5(i - 1), 9, 5(i - 1) + 2, 11)$ for $i = 1, \dots, 6$, a row of pads.

The pairs closer than $4$ are $w p$ and $w q$ (gap $2$), $p r_1$ (gap $3$), $r_i r_{i+1}$ (gap $3$ in $x$), and $q r_6$ (squared distance $1^2 + 3^2 = 10$). Other pairs, such as $p r_2$ with squared distance $3^2 + 3^2 = 18$, do not conflict. So the conflict graph is the cycle $w, p, r_1, \dots, r_6, q, w$ with $9$ vertices. It is an odd cycle, so it has no 2-coloring, and any mask assignment leaves at least one conflict. With three masks it is fine: $w \mapsto 0$, $p, q \mapsto 1$, $r_1, \dots, r_5 \mapsto 0, 1, 0, 1, 0$ and $r_6 \mapsto 2$.

**A stitch.** Cut $w$ at $x = 15$ into $w_1 = (0, 0, 15, 2)$ and $w_2 = (15, 0, 30, 2)$. Now $w_1$ conflicts only with $p$ and $w_2$ only with $q$, so the conflict edges form the path $w_1, p, r_1, \dots, r_6, q, w_2$, which is 2-colorable: $w_1 \mapsto 1$, $p \mapsto 0$, $r_1, \dots, r_6 \mapsto 1, 0, 1, 0, 1, 0$, $q \mapsto 1$, $w_2 \mapsto 0$. The path has $9$ edges from $w_1$ to $w_2$, an odd number, so every 2-coloring gives $w_1$ and $w_2$ different masks and uses the stitch. A scratch script checked the conflict edges and all colorings by brute force.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| [Bipartiteness testing](/bipartiteness-testing/) | breadth-first search on the conflict graph | decides double patterning without stitches in $O(V + E)$, and returns an odd cycle when it fails |
| Conflict graph by a sweep | report the pairs closer than $s$, as in [DRC](/design-rule-checking/) | $O(n \log n + E)$ for $n$ rectangles |
| [Integer programming](/binary-integer-programming/) | one binary variable per vertex, linear constraints for conflicts and stitches (Kahng and others 2008) | exact; exponential in the worst case; its run time is measured |
| [Semidefinite programming](/semidefinite-programming/) relaxation | vectors for the colors, rounding to $k$ masks (Yu and others for triple patterning) | polynomial; a heuristic, its quality is measured |
| Graph simplification | remove vertices of degree less than $k$, split at bridges and cut vertices, solve the parts | exact simplification; it shrinks real graphs a lot, measured |
| [Branch and bound](/branch-and-bound/) and backtracking | search over colorings with pruning | exact; exponential in the worst case |

The degree rule is exact because a vertex with fewer than $k$ neighbors can always get a free mask after the rest of the graph is colored.

## Bounds

**Double patterning without stitches is linear (proved).** A graph is 2-colorable if and only if it has no odd cycle, and breadth-first search decides this in $O(V + E)$ time.

**Fewest conflicts is NP-hard for $k = 2$ (proved).** Minimizing the conflict edges inside one mask is the same as finding a [maximum cut](/maximum-cut/) of the conflict graph, since the edges between the two masks are the cut. Maximum cut is NP-hard on general graphs. On [planar graphs](/planar-graph/) it is solvable in polynomial time (Hadlock 1975), so planar conflict graphs are easy. Conflict graphs of real layouts are not always planar, because features of different sizes can make crossing conflicts.

**Triple patterning is NP-complete (proved).** Deciding whether a planar graph of maximum degree 4 is 3-colorable is NP-complete (Garey, Johnson and Stockmeyer 1976), and Yu and others showed that triple patterning decomposition stays NP-hard for the conflict graphs of layouts. Compare this with double patterning, which is linear. Every planar graph is 4-colorable by the [four color theorem](/four-color-theorem/), but this does not make quadruple patterning easy, because conflict graphs need not be planar.

**What is measured.** On real layers the graphs split into many small parts after simplification, and integer programming solves the parts in practical time. This is an observation from experiments, not a theorem.

## Reductions

- **To graph coloring.** The decision version is [$k$-coloring](/k-coloring/) of the conflict graph.
- **From planar 3-coloring.** The hardness of triple patterning comes from [3-coloring](/three-coloring/) of planar graphs.
- **To maximum cut.** Double patterning with the fewest conflicts is maximum cut, and with stitches it is a maximum cut with weighted edges of both signs.
- **To odd cycle transversal.** Removing the fewest features so that the rest is 2-colorable is [odd cycle transversal](/odd-cycle-transversal/), which is fixed-parameter tractable in the number of features removed.

## Applications

- **Printing layers below the single-exposure limit.** Metal and contact layers of nodes from about 20 nm on use double, triple or quadruple patterning.
- **Layout checks.** Odd cycles in the conflict graph are reported as errors, in the way DRC reports spacing errors, so that the designer changes the layout.
- **Mask making.** The masks from the decomposition then go to [optical proximity correction](/optical-proximity-correction/) one by one.

## References
