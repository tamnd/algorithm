---
tag: 9QJVC1
kind: problem
slug: pocket-machining
name: Pocket machining
aliases:
- pocketing
area: cad/cam-and-additive-manufacturing
level: core
summary: Remove all material inside a planar region, possibly with islands, down to a depth with an end mill, by a toolpath that covers the region.
prereqs: [toolpath-planning, polygon-with-holes, minkowski-sum]
see_also: [contour-parallel-toolpath, direction-parallel-toolpath, voronoi-pocket-machining, morphological-opening, coverage-path-planning, medial-axis, infill-pattern, traveling-salesman-problem]
sources:
  - book: isbn:978-3-540-54103-5
    title: Martin Held, On the Computational Geometry of Pocket Machining, Lecture Notes in Computer Science 500, Springer, 1991
    locator: the introduction and the chapters that define pockets, islands and the two kinds of pocketing paths
  - paper: doi:10.1016/S0925-7721(00)00015-8
    title: Esther M. Arkin, Sándor P. Fekete and Joseph S. B. Mitchell, Approximation algorithms for lawn mowing and milling, Computational Geometry 17(1-2), 25-50, 2000
    locator: the milling problem, where the cutter must stay inside the region, its NP-hardness for regions with holes, and its approximation algorithms
  - paper: doi:10.1007/s004539910010
    title: Esther M. Arkin, Martin Held and Christopher L. Smith, Optimization problems related to zigzag pocket machining, Algorithmica 26(2), 197-236, 2000
    locator: the NP-hardness of minimizing retractions for zigzag paths in pockets with holes
---

Pocket machining asks for a toolpath that removes all the material inside a closed planar region, the pocket, down to a fixed depth, with a rotating end mill that must stay inside the region. The region can have islands, parts that must stay standing. Most of the material of a typical machined part is removed this way, level by level, so pocketing is the most common operation of milling. This is a problem of mechanical manufacturing: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit. This page is about the problem, what any path can and cannot do, and how hard the best path is to find. The methods are on the pages of the [contour-parallel](/contour-parallel-toolpath/), [direction-parallel](/direction-parallel-toolpath/) and [Voronoi](/voronoi-pocket-machining/) paths.

## In plain words

Think of cutting a shallow tray out of a block of wood with a router. The tray has a shape drawn on the top of the block, perhaps with a few posts in the middle that must stay. The router bit is round. You must move it around inside the shape so that it takes out all the wood, without cutting into the walls or the posts.

Three things make this hard. The bit is round, so it cannot get into a sharp inside corner, and a little wood always stays there. The path must cover every part of the tray it can, with no strips left between passes. And the path should be short and smooth, with few times where the bit has to lift and move to another place, because lifts and sharp turns cost time.

## Definition

**Input.** A pocket $P$, a closed bounded region of the plane, usually a [polygon with holes](/polygon-with-holes/) or a region bounded by segments and circular arcs. The holes are the islands. A tool radius $r > 0$, and the depth of the pocket, which plays no role in the planar problem.

**Tool and cut.** The tool is a disk $D_r$ of radius $r$. A path is a curve $\Gamma$ of tool center positions, possibly in several pieces, with a retraction between pieces. The path is *valid* if the tool stays in the pocket: $c + D_r \subseteq P$ for every $c \in \Gamma$, which holds if and only if $\Gamma$ lies in the inward offset $P_r = \{c : \operatorname{dist}(c, \mathbb{R}^2 \setminus P) \ge r\}$. The tool removes the [Minkowski sum](/minkowski-sum/) $\Gamma \oplus D_r$.

**Goal.** A valid path that removes the whole *machinable region* $O_r(P) = P_r \oplus D_r$, the [morphological opening](/morphological-opening/) of $P$ by the disk. No valid path removes more, because every tool position lies in $P_r$. Among such paths, minimize a cost: the length, the machining time, the number of retractions, or a mix that also counts sharp turns and the load on the tool.

## Variants

- **Islands or not.** A pocket without islands is simply connected. Islands make the offsets split and merge, and they make several hard problems NP-hard.
- **Roughing and finishing.** Roughing removes the bulk with a large tool and a large step-over and leaves a thin layer. Finishing passes along the walls and the floor remove that layer.
- **Rest machining.** A smaller tool clears only the material that the last tool could not reach, which is $O_{r_1}(P) \setminus O_{r_0}(P)$ for radii $r_1 < r_0$.
- **Open pockets.** Part of the boundary is open to the air, so the tool may leave the region there, and the entry moves are easy.
- **Engagement limits.** High-speed machining bounds the angle over which the tool is in contact with the material, so the path must avoid full-width cuts and sharp turns. Trochoidal and spiral paths serve this.
- **Many levels.** A 2.5D part is cut level by level, with one pocket problem per level.
- **Coverage in other fields.** The same problem with a mower or a cleaning robot is [coverage path planning](/coverage-path-planning/). The same problem with a nozzle is the infill of a layer in additive manufacturing, see [infill pattern](/infill-pattern/).

## Examples

**A right triangle.** Take the triangle with vertices $(0, 0)$, $(12, 0)$ and $(0, 9)$ and a tool with $r = 1$. The inward offset $P_1$ is the triangle $(1, 1)$, $(9, 1)$, $(1, 7)$, with area 24 and perimeter 24. The machinable region has area
$$
\operatorname{area}(P_1) + r \cdot \operatorname{perimeter}(P_1) + \pi r^2 = 24 + 24 + \pi \approx 51.14,
$$
and the triangle has area 54, so $6 - \pi \approx 2.86$ stays in the three corners whatever path is used.

**A rectangle.** In a rectangle, each corner keeps the region between the corner and the arc of the tool, of area $(1 - \pi/4)r^2$, so $(4 - \pi)r^2$ stays in total.

**A narrow neck.** If the pocket is two wide rooms joined by a corridor narrower than $2r$, then $P_r$ falls into two parts. The tool cannot pass from one room to the other inside the pocket, so a path needs a retraction, and the corridor stays uncut. A smaller tool is needed for it.

## Known algorithms

- **[Contour-parallel toolpath](/contour-parallel-toolpath/).** Nested inward offsets of the boundary, from the wall to the middle. With step-over at most $r$ it removes the whole machinable region, and the tool cuts in one direction.
- **[Direction-parallel toolpath](/direction-parallel-toolpath/).** Parallel straight passes joined in a zigzag, plus a pass along the boundary. With step-over at most $2r$ it removes the whole machinable region.
- **[Voronoi pocket machining](/voronoi-pocket-machining/).** All the offsets of a pocket with islands and arcs from one Voronoi diagram of the boundary, with the splits and the order of the loops.
- **Spiral paths.** Offsets joined into one spiral, or the [connected Fermat spirals](/fermat-spiral-toolpath/) of additive manufacturing, to avoid retractions and sharp turns.
- **Approximation algorithms.** Arkin, Fekete and Mitchell give constant-factor approximations for the length of a milling path, and Arkin, Held and Smith bound the retractions of a zigzag path.

## Bounds

**Uncut corners.** For a convex polygon with interior angles $\alpha_1, \dots, \alpha_n$ and $r$ at most its inradius, the area that no path can remove is
$$
\operatorname{area}(P) - \operatorname{area}(O_r(P)) = r^2\Big(\sum_{i=1}^{n} \cot\frac{\alpha_i}{2} - \pi\Big).
$$
At a corner with angle $\alpha$, the region between the two walls and the tool, with the tool touching both walls, has area $r^2(\cot(\alpha/2) - (\pi - \alpha)/2)$, and the exterior angles $\pi - \alpha_i$ of a convex polygon add up to $2\pi$. For the triangle above, the cotangents of the half angles are 1, 3 and 2, which gives $6 - \pi$. For a rectangle it gives $(4 - \pi)r^2$.

**Length.** A path of length $L$ removes at most $2rL + \pi r^2$ of area, because the Minkowski sum of a curve of length $L$ with a disk of radius $r$ has at most that area. So every path that removes the machinable region $O$ has length
$$
L \ge \frac{\operatorname{area}(O) - \pi r^2}{2r}.
$$
For the triangle above this gives $L \ge 24$. The contour-parallel path with step-over 1 has length $36 + 2\sqrt2 \approx 38.83$, because its strips overlap.

**Hardness.** Minimizing the length of a milling path, where the cutter must stay in the region, is NP-hard for regions with holes (Arkin, Fekete and Mitchell, 2000). Minimizing the number of retractions of a zigzag path is NP-hard for pockets with holes (Arkin, Held and Smith, 2000). For a fixed pocket, the order of the pieces of a path and the moves between them form a [traveling salesman problem](/traveling-salesman-problem/).

## Reductions

- **To offsetting.** The set of valid tool positions is the inward offset $P_r$, and the machinable region is the opening $O_r(P)$. So every pocketing method starts with a polygon offset, see [solid offsetting](/solid-offsetting/) for the 3D form.
- **To coverage.** With the offset known, pocketing is the coverage of $P_r$ by a path whose $r$-neighbourhood covers $O_r(P)$. Robot [coverage path planning](/coverage-path-planning/) solves the same problem.
- **To the medial axis.** The clearance of each point of $P$ and the places where offsets split are read from the [medial axis](/medial-axis/), which reduces the order of the loops to a tree walk.

## Applications

- **Milling of 2.5D parts.** Housings, plates, molds and dies are cut as a stack of pockets, one per level.
- **Roughing of free-form parts.** Before finishing, a free-form part is roughed out by pockets at many heights.
- **Engraving and printed circuit board milling.** Clearing the area between traces on a board is a pocket problem with many islands.
- **Additive manufacturing.** The infill of each layer of a print is a pocket problem for a nozzle, with the same coverage and path questions.

## References
