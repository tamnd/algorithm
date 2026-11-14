---
tag: DXBDN9
kind: problem
slug: flat-pattern-development
name: Flat pattern development
aliases:
- sheet metal unfolding
- flat blank development
area: cad/manufacturing-process-planning
level: core
summary: Compute the flat blank that bends into a given sheet metal part by unfolding its faces at the bends and adding the bend allowance of each bend.
prereqs: [bend-allowance, spanning-tree]
see_also: [k-factor, developable-surface, bend-sequence-planning, nesting-problem, polygon-simplicity-test, springback-compensation, computer-aided-process-planning, manufacturability-analysis]
sources:
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Chapter 16 (sheet-metal forming), the parts on bending and on the bend allowance (general locator; the section number is not confirmed)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the O(n log n) sweep that decides whether n segments intersect, used here to test that the blank does not overlap itself
  - book: isbn:9780521857574
    title: Erik D. Demaine and Joseph O'Rourke, Geometric Folding Algorithms, Linkages, Origami, Polyhedra, Cambridge University Press, 2007
    locator: Part III, the chapters on edge unfoldings of polyhedra and the open problem of whether every convex polyhedron has a non-overlapping edge unfolding
---

Flat pattern development computes the flat blank from which a sheet metal part is made by bending. The part is a set of flat faces, the flanges, joined by cylindrical bend zones. In the [bend allowance](/bend-allowance/) model the neutral surface of the sheet keeps its lengths, so the blank is the development of that surface into the plane: each flange is moved rigidly into the plane, and each bend zone becomes a strip as wide as its bend allowance. For a part with a tree of bends this is a traversal of the faces. The work that is not routine is the choice of cuts when the faces form a cycle, and the test that the blank does not overlap itself.

## In plain words

A sheet metal part starts as a flat piece cut from a sheet, and a press brake bends it along straight lines. To cut the right piece, the planner must know its shape before the bends. The planner takes the part, opens each bend so that the two sides lie flat, and adds a small strip for the material in the curved part of the bend.

The width of that strip comes from a measured factor of the material, so the blank is only as good as that factor. When the walls of a part close on each other, as at the corners of a box, the planner must cut the part at some of them so that it can lie flat. The flat piece must also not lie on top of itself.

## Definition

**Input.** A sheet metal part of constant thickness $t$, given as a [boundary representation](/boundary-representation/) whose faces are the two sides of flat flanges and of cylindrical bend zones. Each bend $e$ has an inside radius $R_e$, a bend angle $\theta_e \in (0, \pi]$ and a [K-factor](/k-factor/) $K_e$. The *face graph* $G$ has one node per flange, one edge per bend that joins two flanges, and one edge per seam where two flanges meet without a bend, as at a welded corner.

**Model.** The neutral surface of the part is the surface at the distance $K_e t$ from the inside face in each bend, and it is the mid-surface or any one side in the flanges, since flat faces do not change their length. This surface is developable: the flanges are planar and the bend zones are cylinders with the radius $\rho_e = R_e + K_e t$. The model says that bending is an isometry of this surface.

**Output.** A region $B$ in the plane, the blank, and for each flange $f$ an isometry $T_f$ of $\mathbb{R}^3$ that takes the neutral face of $f$ into the plane $z = 0$, such that:

1. each bend zone $e$ between $f$ and $g$ maps to a rectangle of width $\mathrm{BA}_e = \theta_e \rho_e$ between the images of the bend lines of $f$ and $g$;
2. the images of the faces and bend zones have disjoint interiors, so $B$ does not overlap itself.

If $G$ has a cycle, the part is not the bent image of one flat piece in general, and the problem also asks for a set $C$ of edges (seams or bends) to cut, so that $G - C$ is a [spanning tree](/spanning-tree/) of the flanges.

**The two length formulas.** On a part whose bend lines are all parallel, a profile, the blank length across the bends is

$$L = \sum_i \ell_i + \sum_e \mathrm{BA}_e = \sum_i D_i - \sum_e \mathrm{BD}_e,$$

where the $\ell_i$ are the flat flange lengths between bend zones, the $D_i$ are the outer dimensions between mold points, and $\mathrm{BD}_e = 2(R_e + t)\tan(\theta_e/2) - \mathrm{BA}_e$ is the bend deduction. The [bend allowance](/bend-allowance/) page proves both forms for one bend. For several bends, each outer dimension $D_i$ is $\ell_i$ plus the outside setback of each bend at its ends, and the sum over the flanges counts each bend twice, once from each side.

## Variants

- **Profile parts.** All bend lines are parallel, as in a channel or a Z-section. The blank is a rectangle, and only its length needs the formula above.
- **Tree of flanges.** A tray with four walls and open corners has a face graph that is a star. Each flange has its own transform, and the blank is a cross or a more general polygon.
- **Closed corners.** A box with welded corners has a face graph with cycles. The designer chooses where to cut, and the choice decides whether the blank fits on the sheet and whether it overlaps. This is the analogue of the edge unfolding of a polyhedron, where it is open whether every convex polyhedron has a non-overlapping edge unfolding (Demaine and O'Rourke).
- **Corner reliefs and features.** Real blanks have relief cuts at the ends of bends, holes, and features such as hems and jogs. Each has its own allowance rule from the shop.
- **Stretched parts.** A drawn or stretched part is not developable, and its blank is estimated with an inverse [finite element](/finite-element-method/) analysis. This is a different problem.

## Examples

**A channel.** Steel sheet with $t = 2$ mm, $R = 3$ mm, $K = 0.33$, two bends of $90$ degrees, and outer dimensions 40, 60 and 40 mm. Each bend has $\mathrm{OSSB} = 5$ mm, $\mathrm{BA} = 5.7491$ mm and $\mathrm{BD} = 4.2509$ mm.

| flange | outer dimension $D_i$ | setbacks removed | flat length $\ell_i$ |
|---|---|---|---|
| first wall | 40 | 5 | 35 |
| web | 60 | 5 + 5 | 50 |
| second wall | 40 | 5 | 35 |
| total | 140 | | 120 |

The blank length is $120 + 2 \times 5.7491 = 131.4982$ mm from the flanges and $140 - 2 \times 4.2509 = 131.4982$ mm from the outer dimensions.

**Different angles.** Make the second bend $45$ degrees with the same outer dimensions. Its outside setback is $5 \tan(\pi/8) = 2.0711$ mm, its $\mathrm{BA}$ is $2.8746$ mm and its $\mathrm{BD}$ is $1.2676$ mm. The flat lengths are 35, 52.9289 and 37.9289 mm, and both formulas give 134.4815 mm.

A short script checks both cases without the formulas. It builds the neutral axis as a path of straight pieces and arcs of radius $R + K t$, measures the arcs as polylines with $2 \times 10^5$ pieces, offsets the path by $(1 - K)t$ to get the outer faces, and intersects the outer face lines to get the mold points. The measured outer dimensions are 40, 60 and 40 mm, and the path length agrees with both formulas to four decimal places.

**A tray.** A tray with a base of $60 \times 40$ mm outer dimensions and four walls of height 20 mm, the same sheet and $90$ degree bends, and open corners. The face graph is a star with the base at its centre. The base flat is $50 \times 30$ mm, each wall flat is 15 mm high, and each wall is placed $\mathrm{BA} = 5.7491$ mm beyond the base flat. The blank is a cross with an overall size of $91.4982 \times 71.4982$ mm. With welded corners the face graph has 5 nodes and 8 edges (4 bends and 4 seams), so it has 4 independent cycles, and 4 edges must be cut to get a spanning tree. The usual choice is the 4 seams, which gives the same cross, and the seams are welded after the bends.

## Known algorithms

**Unfolding by traversal.** Choose a base flange $r$ and set $T_r$ so that $r$ lies in $z = 0$. Traverse $G$ by [breadth-first search](/breadth-first-search/). For a bend $e$ from a placed flange $f$ to a new flange $g$, the bend line of $f$ is a segment in the plane. Rotate $g$ about the bend axis by $-\theta_e$ so that it becomes coplanar with $f$, then move it by $\mathrm{BA}_e$ across the bend line, perpendicular to it. So $T_g = T_f \circ U_e$ for a fixed rigid motion $U_e$ of each bend. Each flange is placed once, so the cost is $O(n)$ for a part with $n$ vertices in total. CAD systems that model sheet metal do this from the stored bend data. When $G$ has cycles, the traversal uses a spanning tree and leaves the other bends as cuts.

**The overlap test.** The boundary of the blank is a set of closed polygons. They have no overlap if and only if no two boundary segments cross and the polygons nest correctly. The [Shamos-Hoey](/shamos-hoey-algorithm/) sweep decides this in $O(n \log n)$ time, and for a blank with one boundary it is a [polygon simplicity test](/polygon-simplicity-test/).

**Choosing the cuts.** For a part with cycles, the planner enumerates or searches the spanning trees for one whose blank does not overlap and fits the sheet well. Systems use rules from the shop, such as "cut the corner seams and keep the bends", because the number of spanning trees grows exponentially. No method with a guarantee is known for the general case.

## Bounds

- The unfolding of a tree of flanges takes $\Theta(n)$ time, since each vertex is moved once and must be output.
- The overlap test is [segment intersection detection](/segment-intersection-detection/) on the boundary of the blank, which takes $\Theta(n \log n)$ time in the algebraic decision tree model for general segment sets. For one simple boundary a linear-time test follows in theory from [Chazelle's triangulation](/chazelle-polygon-triangulation/).
- The blank length is exact under the model, but the model has an error of the order of the error in $K$. In the channel, a change of $K$ from 0.33 to 0.5 adds $2 \times 0.5341 = 1.07$ mm to the blank. This is larger than the tolerance of many parts, so the measured $K$ matters more than the algorithm.

## Reductions

- The development of the neutral surface is a special case of the development of a [developable surface](/developable-surface/), where the pieces are planes and cylinders, so the map is known in closed form.
- The blank is the input of the [nesting problem](/nesting-problem/), which places many blanks on one sheet.
- The bent part is the output of [bend sequence planning](/bend-sequence-planning/), which starts from the blank and orders the bends.

## Applications

The blank is the base of the cutting program (laser, punch or plasma), of the material cost, and of the press brake program. In [computer-aided process planning](/computer-aided-process-planning/) for sheet metal it is the first step, and a [manufacturability analysis](/manufacturability-analysis/) uses it to find features too close to a bend and blanks that overlap. The tool bends further than the part, to allow for [springback](/springback-compensation/), but the blank length does not change, because the neutral axis keeps its length in the model.

## References
