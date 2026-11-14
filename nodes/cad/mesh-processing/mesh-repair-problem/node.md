---
tag: 1RE2AF
kind: problem
slug: mesh-repair-problem
name: Mesh repair
aliases:
- mesh healing
- model repair
area: cad/mesh-processing
level: core
summary: Turn a polygon soup with holes, gaps, overlaps, flipped faces and self-intersections into a closed, oriented manifold mesh that bounds a solid.
prereqs: [manifold-mesh, indexed-face-set]
see_also: [vertex-welding, consistent-mesh-orientation, hole-filling, mesh-self-intersection, volumetric-mesh-repair, mesh-boolean-operations, generalized-winding-number, hausdorff-distance]
sources:
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the classification of defects and of the targets of repair by application, and the survey of local and global methods
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair (the types of artifacts, and surface-based and volumetric repair)
  - paper: doi:10.1145/1015706.1015815
    title: Tao Ju, Robust repair of polygonal models, ACM Transactions on Graphics 23(3), 2004, 888 to 895 (SIGGRAPH 2004)
    locator: the statement of the goal, a closed surface that divides space into inside and outside
---

Mesh repair is the problem of changing a polygon mesh with defects into a mesh that meets a stated condition of validity, while it stays close to the input. The most common condition is a *watertight solid*: a closed, consistently oriented [manifold mesh](/manifold-mesh/) without self-intersections, which bounds a region of space. The input is often a polygon soup, a list of faces with no shared vertices, from a scanner, an STL file, a CAD export, or a model made of parts. The problem is ill-posed in a strict sense: the input does not say what shape it should have been, so a repair is right only relative to a target condition and a measure of change. Attene, Campen and Kobbelt organise the field by the target, because a mesh for rendering, for 3D printing and for simulation needs different conditions. The local steps are separate pages: [vertex welding](/vertex-welding/), [consistent mesh orientation](/consistent-mesh-orientation/), [mesh hole filling](/hole-filling/) and [mesh self-intersection](/mesh-self-intersection/) detection.

## In plain words

A model from the real world is often broken. Some tiles are loose, some face the wrong way, some are missing, and some pass through others. Each of these breaks a program that needs a clean solid, such as a slicer for a 3D printer.

Repair means fixing these faults, so that the model is a closed skin with a clear inside and outside. The fix should change the model as little as possible.

The hard part is that the model does not say what it should be. A crack might be an error or a real slot. Two parts that touch might be one part or two. So each repair makes choices, and it is only right with respect to a stated goal.

## Definition

**Input.** A polygon mesh as an [indexed face set](/indexed-face-set/): points $p_0, \ldots, p_{n-1}$ in $\mathbb{R}^3$ and faces, each a list of point indices. Nothing is assumed: points can repeat, faces can be degenerate, edges can have any number of faces, and faces can cross.

**Conditions of validity.** A mesh can meet any of these conditions, each one stated without reference to a method:

| condition | meaning | check |
|---|---|---|
| C1, clean | no two points at the same position, no face with a repeated index or with zero area | by sorting or hashing the points |
| C2, manifold | each edge has one or two faces, and the link of each vertex is one cycle or one path | by a map of the edges |
| C3, closed | no edge with only one face | by the same map |
| C4, oriented | the two faces of each edge use it in opposite directions | by the same map |
| C5, embedded | no improper pair of triangles, as defined on the [self-intersection](/mesh-self-intersection/) page | a geometric test |
| C6, outward | the outward normal follows the right-hand rule for the vertex order of each face | a sign test |

A mesh that meets C1 to C6 is a *watertight solid*. Each of its components is a closed embedded surface, which divides space into an inside and an outside, and the inside is a [manifold solid](/manifold-solid/). The Euler characteristic of each component is $\chi = V - E + F = 2 - 2g$ for a surface of genus $g$, and $\chi = 2 - 2g - b$ before the $b$ holes are closed.

**Output.** A mesh $M'$ that meets the target conditions, often C1 to C6, and stays near the input $M$. *Near* has no single meaning. Common measures are the [Hausdorff distance](/hausdorff-distance/) between the two surfaces, the number of faces that change, and whether sharp edges and small features are kept. These measures are judged by sampling, for example with [Metro](/metro-mesh-comparison/).

**Degeneracies are part of the input.** Exact zero areas, vertices that lie exactly on another edge (T-junctions), coplanar faces that overlap, and parts that touch at one edge are common in CAD data. A repair must decide each case, not assume general position. The geometric conditions C5 and C6 are signs of the [orientation test](/orientation-test/) and of a sum of determinants, so their answers depend on exact arithmetic.

## Variants

- **By target.** Attene, Campen and Kobbelt classify by use. Rendering needs few conditions, and often only C4. Rapid prototyping needs C1 to C6. Simulation also needs triangles of good shape. Each target is a different problem.
- **Local or global.** A local repair changes the mesh only near each defect and keeps the rest. A global repair builds a new surface for the whole model, which removes all defects at once but changes every face.
- **Topology.** Some forms fix the genus, or ask that small handles and small components be removed, since scans often have tiny tunnels that are not in the real object.
- **Tolerance.** Some forms treat any two points within $\varepsilon$ as equal, and any pair of faces within $\varepsilon$ as touching. The result then depends on $\varepsilon$.
- **CAD models.** A boundary representation from a CAD system has gaps between trimmed surfaces. Its repair works on the curves and surfaces, before the mesh exists, and is a separate problem.

## Examples

**A cube as a soup.** An STL file of a cube has 12 triangles and 36 points, so as an indexed face set it has $V = 36$, $E = 36$, $F = 12$ and $\chi = 12$: twelve separate triangles. It meets C2 but not C1 or C3. Merging equal points gives $V = 8$, $E = 18$, $F = 12$ and $\chi = 8 - 18 + 12 = 2$, a sphere. If two triangles of one face were written in the other direction, the mesh fails C4 at the edges of those triangles, and reversing them gives C4 and C6.

**A missing face.** Remove the two triangles of one face from the welded cube. Now $F = 10$, $E = 17$ and $\chi = 1$, a disk with one border loop of 4 edges. C3 fails until the hole is filled.

**A T-junction.** Two squares side by side, where the left one is split into two triangles and the right one is split into three by a fan from a vertex at the midpoint of the shared side. The midpoint is a vertex of the right square only, so the shared side is one edge on the left and two edges on the right. All three of these edges have one face, and the mesh has a crack of zero width. Merging points does not fix it, because no two points are equal. The left triangle must be split at the midpoint.

**Two cubes that share an edge.** The cubes $[0, 1]^3$ and $[1, 2] \times [1, 2] \times [0, 1]$ touch along the segment from $(1, 1, 0)$ to $(1, 1, 1)$. After merging points, this edge has four faces, so C2 fails. One repair splits the edge into two copies, which gives two manifold cubes, but they touch with no shared vertex and so fail C5. Another repair moves the cubes apart, and a third joins them with a thin bridge. Each answer meets a different target, and the input does not say which one the user wanted.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| a pipeline of local steps: [vertex welding](/vertex-welding/), then [consistent mesh orientation](/consistent-mesh-orientation/), then [mesh hole filling](/hole-filling/) with [Liepa's method](/liepa-hole-filling/) | each step meets its own condition when its input allows it; no global guarantee, since a step can fail or create a new defect | near linear for the first two steps, $O(n^3)$ for each hole of $n$ edges |
| [volumetric mesh repair](/volumetric-mesh-repair/), Ju 2004: label the cells of an octree inside or outside, then extract the surface | the output is always closed and separates inside from outside; small features below the cell size are lost | linear in the number of cells |
| [mesh arrangements](/mesh-arrangements/) and a self-union by [mesh Boolean operations](/mesh-boolean-operations/) | exact removal of self-intersections with exact arithmetic, for inputs whose inside is defined | output sensitive, measured |
| [generalized winding number](/generalized-winding-number/) to label space, then extract a surface | a closed result for any soup; the inside is decided by a threshold | the cost of the winding numbers on a grid or a tetrahedral mesh |
| [Poisson surface reconstruction](/poisson-surface-reconstruction/) from points and normals of the input | a watertight surface; the whole model is rebuilt and moves | a sparse solve on an octree |

Which method is best for a given model is a matter of measurement, on collections of models from real use. No method meets every target on every input, and the global methods trade the guarantee of a closed result against the loss of detail and the change of every face.

## Bounds

- **Checking.** C1 to C4 can be checked in $O(c)$ expected time for $c$ corners, with a [hash table](/hash-table/) of the points and edges. Checking C5 is the [mesh self-intersection](/mesh-self-intersection/) problem, which needs $\Omega(m \log m)$ time in the algebraic decision tree model for $m$ triangles, and can have $\Theta(m^2)$ improper pairs to report.
- **No unique answer.** The examples above show inputs with several repairs that are equally valid. So there is no canonical output, and the problem has no single complexity until a target and a measure of change are fixed.
- **Hard parts.** Some strict forms are hard. Filling a hole with a patch that uses only the border vertices and does not cross itself contains the triangulability problem of Barequet, Dickerson and Eppstein, which is NP-complete, as stated on the [hole filling](/hole-filling/) page.

## Reductions

- **Contains self-intersection detection.** A repair to C5 must at least decide C5, so it is at least as hard as [mesh self-intersection](/mesh-self-intersection/) detection.
- **Contains hole filling.** A repair to C3 that keeps the input faces must close each border loop, which is the [mesh hole filling](/hole-filling/) problem.
- **To a labelling of space.** A watertight solid is the same thing as a bounded region with a surface boundary. So repair can be stated as the choice of a region of space, inside or outside for each point, that agrees with the input where the input is clear, followed by the extraction of its boundary. The global methods in the table work in this form.
- **Into Boolean operations and slicing.** Mesh Boolean operations and [slicing for additive manufacturing](/slicing-for-additive-manufacturing/) assume a watertight input, so repair is a step before them.

## Applications

- **3D printing.** Slicers need C1 to C6 to know the inside of each layer. Most models from the web fail at least one condition.
- **Simulation.** A [tetrahedralization](/tetrahedralization/) for finite element analysis needs a watertight boundary.
- **CAD data exchange.** Translation between formats leaves gaps, T-junctions and duplicate faces.
- **Scanning.** Range scans give holes, noise and small extra parts.
- **Games and film.** Models made of separate parts that pass through each other must be joined before they can be simplified or printed.

## References
