---
tag: AMY3M8
kind: problem
slug: build-orientation
name: Build orientation optimization
aliases:
- part orientation for 3D printing
area: cad/cam-and-additive-manufacturing
level: core
summary: Choose the direction in which to print a part to trade off build time, support volume, surface error and strength.
prereqs: [slicing-for-additive-manufacturing, multi-objective-optimization]
see_also: [support-structure-generation, staircase-effect, adaptive-slicing, convex-hull-3d, rotating-calipers, pareto-front, weighted-sum-method, genetic-algorithm]
sources:
  - paper: doi:10.1007/BF00124677
    title: Dietmar Frank and Georges Fadel, Expert system-based selection of the preferred direction of build for rapid prototyping processes, Journal of Intelligent Manufacturing 6(5), 1995, 339 to 345
    locator: the criteria for the direction of build and the rules that rank candidate directions
  - paper: "W. Cheng, J. Y. H. Fuh, A. Y. C. Nee, Y. S. Wong, H. T. Loh and T. Miyazawa, Multi-objective optimization of part-building orientation in stereolithography, Rapid Prototyping Journal 1(4), 1995, 12 to 23"
    locator: the weighted objectives of part accuracy and build time over candidate orientations
  - paper: doi:10.1016/S0925-7721(99)00002-4
    title: Jayanth Majhi, Ravi Janardan, Michiel Smid and Prosenjit Gupta, On some geometric optimization problems in layered manufacturing, Computational Geometry 12(3-4), 1999, 219 to 239
    locator: the optimal build directions of convex polyhedra under single geometric criteria
  - paper: "Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988, 761 to 765"
    locator: the width of a point set in three dimensions in O(n log n + I) time, with I the number of antipodal edge pairs of the convex hull
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the discussion of part orientation in the process chain and in design for additive manufacturing (chapter not confirmed)
---

Build orientation optimization is the problem of choosing how to place a part in a printer: which direction of the part points up during the build. The choice changes almost every cost of the print. The height of the part sets the number of layers and so most of the build time. The faces that point down set the support that must be built and removed. The slope of each face sets its [staircase effect](/staircase-effect/). The layer direction sets the weak direction of the part, because layers bond less well to each other than material within a layer. These goals usually conflict, so the problem is a [multi-objective optimization](/multi-objective-optimization/) over the directions on a sphere. Frank and Fadel (1995) and Cheng and coauthors (1995) were early methods that ranked or weighted candidate directions. For convex parts some single criteria have exact polynomial algorithms. For general parts the usual methods sample the directions.

## In plain words

Before a part is printed, someone must decide which way up it goes. A rod can stand up or lie down. Standing, it takes more layers, but its sides come out smooth and nothing hangs over empty space. Lying down, it prints faster, but its lower side hangs over the plate and needs props, and its round side shows steps.

No single way up is best for everything. The problem is to find the choices that are good for the goals that matter for this part, and to pick one.

## Definition

**Input.** A closed triangle mesh $M$ with vertices $v_1, \dots, v_n$ and facets $f$ with outward normals $n_f$ and areas $A_f$, a layer thickness $t$ and a critical overhang angle $\alpha$, measured from the horizontal. Faces that are less steep than $\alpha$ and face down need support.

**Decision.** A unit vector $d \in S^2$, the build direction (the direction of the part that points up). A rotation about $d$ does not change any objective below, so the set of choices is the sphere, not the whole rotation group. The rotation about $d$ matters only for how parts fit on the plate.

**Objectives.** Each is a function of $d$. With $\cos\theta_f = n_f \cdot d / \|n_f\|$:

- *height* $h(d) = \max_i v_i \cdot d - \min_i v_i \cdot d$, and the number of layers $\lceil h(d) / t \rceil$, a proxy for the build time;
- *support area* $\sum_f A_f \,[\,\cos\theta_f < -\cos\alpha\,]$, the area of the facets that face down more steeply than the threshold allows (or the support volume, which also weights each such facet by its height above the plate);
- *surface error* $\sum_f A_f \, t\, |\cos\theta_f|$, the area weighted by the cusp height, often taken only over the faces that matter;
- other goals such as strength in a given load direction, the area in contact with supports on faces that must look good, or the area on the plate.

**Output.** A direction $d$ that minimizes a chosen combination, or the set of Pareto optimal directions, see [Pareto front](/pareto-front/). The problem as stated does not include the choice of supports or slices. Those come after the orientation, see [support structure generation](/support-structure-generation/) and [adaptive slicing](/adaptive-slicing/).

## Variants

- **Single criterion.** Minimize only the height, the support area, the support volume or the surface error.
- **Weighted sum.** Minimize $\sum_j w_j\, g_j(d)$ with fixed weights, the approach of Cheng and coauthors, see [weighted sum method](/weighted-sum-method/).
- **Pareto set.** Return all directions that no other direction beats on every objective, and let the user choose.
- **Discrete candidates.** Restrict $d$ to a finite set, such as the facet normals or the normals of the faces of the convex hull, so that the part rests on a face.
- **Rule based.** Rank candidate directions by expert rules, as Frank and Fadel (1995) did.
- **Several parts.** Choose orientations and positions of many parts on one build plate at once, which adds a packing problem.

## Examples

**A rod.** Let the part be a solid cylinder of radius 10 mm and length 40 mm, with $t = 0.2$ mm and $\alpha = 45°$.

| orientation | height | layers | support | largest cusp on the round side |
|---|---|---|---|---|
| standing on an end | 40 mm | 200 | none | 0 (the side is vertical) |
| lying on its side | 20 mm | 100 | about 515 mm³ | 0.2 mm (at the top and bottom lines) |

Standing, every face is vertical or horizontal, so there are no steps and no overhangs. Lying, the facets within $45°$ of straight down need support. They are the part of the round side with $|x| \le 10 \sin 45° \approx 7.07$ mm, and the gap under them has the area $\int_{-a}^{a} (10 - \sqrt{100 - x^2})\,dx \approx 12.88$ mm² with $a = 10/\sqrt2$, which times the length 40 mm gives about 515 mm³. The lying rod is twice as fast and needs support, the standing rod is slow and clean. Neither is better in every objective, so both are Pareto optimal for (layers, support).

**A box.** For a box of $10 \times 20 \times 40$ mm, all three resting faces give no overhang and no steps. The heights are 10, 20 and 40 mm. The flat orientation is best on these objectives. It can still be the wrong choice if the load acts across the layers.

## Known algorithms

- **Sampling.** Evaluate the objectives on a grid of directions on the sphere, or on the facet normals and the convex hull face normals, and keep the best or the Pareto set. This is the most common method in practice.
- **Rules and weights.** Frank and Fadel (1995) used an expert system. Cheng and coauthors (1995) used weighted objectives over candidate orientations.
- **Metaheuristics.** [Genetic algorithms](/genetic-algorithm/) and other searches over $S^2$, often with Pareto ranking.
- **Exact methods for convex parts.** Majhi, Janardan, Smid and Gupta (1999) give polynomial algorithms that find an optimal direction for a convex polyhedron under single geometric criteria from layered manufacturing.
- **Minimum height.** The direction of least height is the direction of the width of the [convex hull](/convex-hull-3d/). Houle and Toussaint (1988) compute the width in $O(n \log n + I)$ time, where $I$ is the number of antipodal edge pairs, which is $O(n^2)$ in the worst case. In the plane, [rotating calipers](/rotating-calipers/) do this in linear time after the hull.

## Bounds

- **The height.** $h(d)$ is the width of the convex hull of the vertices in direction $d$, so the minimum height equals the width of the hull, and only the hull vertices matter.
- **The support area has $O(n^2)$ pieces.** For a facet $f$, the condition $n_f \cdot d < -\|n_f\| \cos\alpha$ holds inside a spherical cap of $S^2$. The $n$ boundary circles of these caps cross pairwise in at most two points, so they form an arrangement with $O(n^2)$ vertices, edges and cells. Inside a cell, the set of overhang facets does not change, and the support area is constant. So an exact minimum of the support area is found by evaluating one direction per cell, which is polynomial. This is a simple counting fact, not a fast algorithm.
- **Hardness.** This page cites no NP-hardness result for the general multi-objective problem. The difficulty in practice is that the objectives are not convex on the sphere and that the true costs (time, strength, finish) are only approximated by the geometric ones.

## Reductions

- **Width.** Minimum build height is the same problem as the width of a point set in 3D.
- **To a finite search.** Because the overhang set is constant on each cell of the arrangement above, minimizing the support area reduces to a search over the $O(n^2)$ cells.
- **To support generation.** For a fixed direction, the support cost is the optimum of [support structure generation](/support-structure-generation/), so an exact support objective nests that problem inside this one. Most methods use a cheap proxy instead.

## Applications

- Every slicer for extrusion, resin and powder bed printers offers an automatic orientation step or a choice among presets.
- Batch planning in powder bed fusion, where many parts are oriented and packed into one build.
- Design for additive manufacturing, where the designer fixes the orientation early and shapes the part so that its overhangs are below the threshold.

## References
