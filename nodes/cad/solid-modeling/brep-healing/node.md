---
tag: BGTJDA
kind: problem
slug: brep-healing
name: B-rep healing
aliases:
- B-rep repair
- model sewing
- CAD model healing
area: cad/solid-modeling
level: core
summary: Turn a B-rep with gaps, overlaps, missing faces and tolerance errors, often from data exchange, into a valid closed solid by sewing faces and merging edges.
prereqs: [boundary-representation, manifold-solid, trimmed-surface]
see_also: [tolerant-modeling, mesh-repair-problem, vertex-welding, hole-filling, geometric-robustness-problem, single-linkage-clustering, optimal-polygon-triangulation, hausdorff-distance]
sources:
  - paper: "Gill Barequet and Micha Sharir, Filling gaps in the boundary of a polyhedron, Computer Aided Geometric Design 12(2), 207 to 229, 1995"
    locator: the matching of boundary curve pieces across gaps by geometric hashing, and the filling of the remaining holes by triangulation
  - paper: "Gill Barequet and Subodh Kumar, Repairing CAD models, Proceedings of IEEE Visualization 1997, 363 to 370"
    locator: stitching cracks between the faces of tessellated CAD models and filling holes
  - paper: "Jan Helge Bøhn and Michael J. Wozny, Automatic CAD-model repair: shell-closure, Proceedings of the Solid Freeform Fabrication Symposium, Austin, Texas, 1992, 86 to 94"
    locator: closing gaps in faceted models for layered manufacturing by adding facets along unmatched boundary edges
  - paper: doi:10.1145/218013.218067
    title: David J. Jackson, Boundary representation modelling with local tolerances, Proceedings of the Third ACM Symposium on Solid Modeling and Applications, 247 to 254, 1995
    locator: the alternative to healing, keeping the gaps and storing a tolerance on each edge and vertex
  - paper: doi:10.1016/S0925-7721(98)00005-4
    title: Gill Barequet, Matthew Dickerson and David Eppstein, On triangulating three-dimensional polygons, Computational Geometry 10(3), 155 to 170, 1998
    locator: the proof that deciding whether a polygon in space has a triangulation without self-intersections is NP-complete
  - paper: doi:10.1145/1015706.1015815
    title: Tao Ju, Robust repair of polygonal models, ACM Transactions on Graphics 23(3), 888 to 895, 2004
    locator: volumetric repair on an octree, with an output surface that is closed by construction
  - paper: doi:10.1145/1095878.1095883
    title: Stephan Bischoff, Darko Pavic and Leif Kobbelt, Automatic restoration of polygon models, ACM Transactions on Graphics 24(4), 2005
    locator: volumetric repair with an adaptive octree, and the reconstruction of sharp features
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), 2013
    locator: the survey of defects, of local and volumetric repair methods, and of what each one guarantees
---

B-rep healing takes a [boundary representation](/boundary-representation/) that is not a valid solid and repairs it. The faces may not meet along shared edges, leaving gaps or overlaps. Faces may be missing, duplicated or wrongly oriented. Edges may be tiny, faces may be slivers, and the stated tolerances may not match the geometry. The usual cause is data exchange. A model is built in one system with one precision, written to a neutral format such as STEP or IGES as separate [trimmed surfaces](/trimmed-surface/), and read into another system with a different precision. A model that was closed in the first system arrives as a set of faces that almost meet. Healing must sew them into a closed, oriented, [manifold](/manifold-solid/) shell without changing the shape by more than a tolerance. There is no standard formal statement of the problem, because the correct repair is the solid the designer meant, and the data does not contain it. This page gives the most precise version in use, the known approaches, and the few results that are proved.

## In plain words

A box is sent from one CAD program to another. The second program does not receive a box. It receives six separate panels whose edges almost touch, with gaps a hundredth of a millimetre wide. To the second program it is not a solid, so it cannot compute the volume, cut it, or mesh it.

Healing glues the panels back into a box. It finds edges that are close enough to be the same edge and makes them one. Where a panel is missing, it adds a patch. Where two panels overlap, it trims them. Where a panel faces the wrong way, it flips it.

The hard part is the word "close enough". If the threshold is too small, gaps stay open. If it is too large, real details such as thin slots get glued shut.

## Definition

No standard formal statement exists. Papers and kernels state the goal as validity of the result, with the shape changed as little as possible, and each makes "as little as possible" precise in its own way. The version below collects the conditions they share.

**Input.**

- A finite set of faces. Each face is a surface patch, given as a surface and boundary loops of curves, or as a set of triangles.
- A tolerance $\varepsilon > 0$, usually taken from the precision of the source system or chosen by the user.

**Output.** A B-rep, that is, vertices, edges, loops and faces with their incidences, and a curve or point for each edge and vertex, such that:

- *Topological validity.* Every edge has exactly two face uses, with opposite orientations, and the faces around each vertex form one disc. So the boundary is a closed, oriented 2-manifold, and the [Euler-Poincaré formula](/euler-poincare-formula/) holds.
- *Geometric consistency within $\varepsilon$.* Each edge curve lies within $\varepsilon$ of the boundaries of both its faces. Each vertex lies within $\varepsilon$ of the ends of all its edges.
- *No self-intersection.* Faces that share no edge or vertex are more than $\varepsilon$ apart.
- *Fidelity.* The new faces are within $\varepsilon$, in [Hausdorff distance](/hausdorff-distance/), of the input faces they come from. The added faces fill only the gaps that no sewing within $\varepsilon$ can close, and they are as small as possible in some measure, such as area.

**The gap.** These conditions may have no solution, for example when a gap is wider than $\varepsilon$ and has no surface that fills it without intersections. They may also have many solutions, which differ in which edges are joined. The choice among them is the designer's intent. Two faces 0.8ε apart may be one surface split by a crack, or the two walls of a thin slot. No rule computed from the geometry alone can always tell these apart.

**Size.** The number of faces and of boundary curve pieces, $n$, and the number of triangles for faceted input.

**Model.** Floating-point geometry with tolerance $\varepsilon$. The topological conditions are exact and the geometric ones hold up to $\varepsilon$.

## Variants

- **Sewing only.** The faces are all present and nearly meet, so the task is to identify the boundary edges and vertices that should be shared. Kernels call this *sewing* or *stitching*.
- **Gap and hole filling.** Some faces are missing, so new surface must be made to close the shell. For faceted models this is [hole filling](/hole-filling/).
- **Faceted repair.** The input is a triangle soup, as in STL files for 3D printing. The defects are cracks, holes, wrong normals, non-manifold edges and self-intersections. The local methods sew and fill. The volumetric methods convert to a volume and back.
- **Healing the tolerances.** The topology is right, but the stored tolerances are smaller than the actual gaps. The repair raises the tolerances, as in [tolerant modeling](/tolerant-modeling/), or recomputes the edge curves so that the gaps shrink.
- **Small-feature removal.** Short edges, sliver faces and tiny steps that come from rounding are merged into their neighbours. This is a separate step from closing the shell.
- **Orientation.** All faces are made to point outward, by propagating the orientation across shared edges and then testing one face, for example with a ray or a [generalized winding number](/generalized-winding-number/).

## Examples

- **A box with cracks.** Six planar faces of the unit cube, each with its edges moved by up to $0.01$ mm. With $\varepsilon = 0.02$ mm, every boundary edge has exactly one partner within $\varepsilon$. Sewing merges the 24 face edges into 12 edges and the 24 face corners into 8 vertices, and the result has $V - E + F = 8 - 12 + 6 = 2$.
- **Chaining.** Points $p_i = (0.6\, i\, \varepsilon, 0, 0)$ for $i = 0, \dots, 5$ lie on the boundaries of different faces. Each consecutive pair is within $\varepsilon$, so merging every pair within $\varepsilon$ joins all six points into one vertex. But $p_0$ and $p_5$ are $3\varepsilon$ apart. A rule that merges only pairs within $\varepsilon$ must then choose which pairs to merge, and different choices give different topologies.
- **A missing face.** The same box with its top face lost in translation. Sewing closes the other 20 edges and leaves a hole bounded by 4 edges. These 4 edges lie in a plane, so a planar face fills the hole exactly. A hole whose boundary is not planar needs a surface chosen by some rule, for example a minimum-area triangulation of the boundary.
- **A T-junction.** One face has a single edge along a line where its neighbour has two edges, meeting at a vertex in the middle. No pairing of whole edges works. The long edge must be split at the point nearest the middle vertex, and then each half is paired.
- **A thin slot.** A slot of width $0.8\varepsilon$ is cut into a block. Sewing with tolerance $\varepsilon$ joins its two walls, and the slot disappears. Here the tolerance is wrong for the model, and only a smaller tolerance or the user can save the slot.

## Known algorithms

No algorithm solves the problem as stated, because the fidelity condition refers to intent. The approaches are:

- **Proximity sewing.** Find candidate pairs of boundary edges that are close, with a [k-d tree](/kd-tree/) or [spatial hashing](/spatial-hashing/). Merge vertices that are within $\varepsilon$, often with a [disjoint-set forest](/disjoint-set-forest/), which is [single-linkage clustering](/single-linkage-clustering/) at threshold $\varepsilon$ and the same step as [vertex welding](/vertex-welding/) of a mesh. Pair edges whose ends merged and whose curves stay within $\varepsilon$, and split edges at T-junctions. This is the common scheme in commercial kernels, and it is described in their documentation, not in a single paper.
- **Matching boundary curves.** Barequet and Sharir match pieces of boundary curves across gaps with geometric hashing, so that whole runs of edges are paired at once. Then they fill the holes that remain by triangulating each hole. Barequet and Kumar applied this kind of stitching and hole filling to tessellated CAD models.
- **Shell closure for faceted models.** Bøhn and Wozny closed the gaps of faceted models for layered manufacturing by finding the unmatched boundary edges and adding facets along them.
- **Volumetric repair.** Convert the faces to a volume, for example by marking the cells of an octree as inside or outside, and extract a new surface from it, for example by [dual contouring](/dual-contouring/). Ju's method and that of Bischoff, Pavic and Kobbelt work this way. The output is closed by construction, but details smaller than the cells are lost or changed, and the result is a mesh, not the original surfaces. For faceted models this is the setting of [mesh repair](/mesh-repair-problem/).
- **Keeping the gaps.** [Tolerant modeling](/tolerant-modeling/) stores a tolerance on each edge and vertex, as Jackson described, so that the faces that nearly meet count as meeting, without moving any geometry.

Attene, Campen and Kobbelt survey the faceted case and list which defects each method repairs and what it guarantees.

## Bounds

**What is proved.**

- *Closeness is not transitive.* Let $R_\varepsilon$ be the relation "within distance $\varepsilon$". It is not an equivalence relation, by the chaining example: its transitive closure joins $p_0$ and $p_5$ at distance $3\varepsilon$. Merging by the closure, as a disjoint-set forest does, can join points that are arbitrarily far apart, since a chain of $k$ steps of length $0.6\varepsilon$ spans $0.6 (k - 1) \varepsilon$. Any merge rule that avoids this must drop some pairs within $\varepsilon$. So, under the definition above, no rule depends only on pairwise distances and satisfies both "every pair within $\varepsilon$ is joined" and "no joined pair is more than $\varepsilon$ apart".
- *Hole filling can be hard.* Barequet, Dickerson and Eppstein proved that deciding whether a polygon in space has a triangulation without self-intersections, using its own vertices, is NP-complete. So filling a non-planar hole without self-intersections has no known polynomial algorithm in general. If self-intersection is ignored, a triangulation of one hole with $m$ boundary vertices that minimizes the total weight, such as area, is found in $O(m^3)$ time by the dynamic program of [optimal polygon triangulation](/optimal-polygon-triangulation/).
- *Validity is easy to check.* Given a candidate output, the topological conditions take linear time to check: count the uses of each edge, walk the faces around each vertex, and compute $V - E + F$ for each shell. The geometric conditions take distance computations between curves and surfaces.
- *Volumetric output is closed.* The volumetric methods produce a surface that bounds a set of cells, so it is closed and separates inside from outside by construction. The cost is fidelity: no bound on the change of shape below the cell size can be given.

**What is only measured.** The success of healing tools is reported as the fraction of models in a test set that become valid solids. These test sets are chosen by vendors and authors, and their results cannot be compared. There is no agreed benchmark with agreed correct answers, and the survey of Attene, Campen and Kobbelt says the same for faceted repair.

## Reductions

- **From data exchange.** Every translation of a B-rep between systems with different precisions can create the defects, so every importer runs some form of healing.
- **To clustering.** Merging vertices within $\varepsilon$ is clustering at threshold $\varepsilon$. The disjoint-set approach is single-linkage clustering, with its chaining.
- **To matching.** Pairing boundary edges is a matching between edge pieces, weighted by distance, with the T-junction case as a split of one piece.
- **To triangulation.** Filling a hole bounded by a polygon in space is triangulating that polygon. With self-intersections forbidden it is NP-complete, and with them allowed it is a dynamic program.
- **To the robustness problem.** The defects come from rounded arithmetic in the source system. Healing repairs after the fact what the [geometric robustness problem](/geometric-robustness-problem/) describes, and [tolerant modeling](/tolerant-modeling/) avoids it in another way.

## Applications

- **Import of STEP and IGES files.** Every CAD system heals imported models before it can run Booleans, offsets or mass properties on them.
- **Meshing for analysis.** A finite element mesher needs a closed, consistent shell. Gaps make it leak, and slivers make it produce bad elements.
- **3D printing.** STL files must describe closed solids before slicing, and shell closure was studied early on for this use.
- **Manufacturing.** Toolpath planning and casting analysis need a closed solid to classify points as material or air.
- **Legacy data.** Models from old systems, or rebuilt from drawings, are healed before they are used in new ones.

## References
