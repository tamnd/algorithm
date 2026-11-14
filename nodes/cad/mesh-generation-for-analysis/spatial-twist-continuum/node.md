---
tag: H9HJ7J
kind: concept
slug: spatial-twist-continuum
name: Spatial twist continuum
aliases:
- dual of a hexahedral mesh
- hex mesh sheets
area: cad/mesh-generation-for-analysis
level: advanced
summary: The dual of a hex mesh, an arrangement of surfaces called sheets whose triple crossings are the hexes, used to reason about and edit hexahedral meshes.
prereqs: [hexahedral-mesh-generation]
see_also: [whisker-weaving, hexahedral-mesh-existence-theorem, plastering, polycube-hex-meshing, hexahedral-sweeping, paving, euler-formula, disjoint-set]
sources:
  - paper: "Peter Murdoch, Steven Benzley, Ted Blacker and Scott A. Mitchell, The spatial twist continuum: a connectivity based method for representing all-hexahedral finite element meshes, Finite Elements in Analysis and Design 28(2), 1997, 137 to 149"
    locator: the definition of the twist planes and the chords as the dual of a hex mesh (general locator)
  - paper: doi:10.1007/3-540-60922-9_38
    title: Scott A. Mitchell, A characterization of the quadrilateral meshes of a surface which admit a compatible hexahedral mesh of the enclosed volume, STACS 96, Lecture Notes in Computer Science 1046, Springer, 1996
    locator: the conditions under which an arrangement of surfaces is the dual of a hex mesh (general locator)
  - paper: "Timothy J. Tautges and Sarah E. Knoop, Topology modification of hexahedral meshes using atomic dual-based operations, Proceedings of the 12th International Meshing Roundtable, 2003"
    locator: the dual complex as an arrangement of pseudo-hyperplanes, and the atomic operations (general locator)
  - paper: "Michael J. Borden, Steven E. Benzley and Jason F. Shepherd, Hexahedral sheet extraction, Proceedings of the 11th International Meshing Roundtable, 2002, 147 to 152"
    locator: the removal of a sheet to coarsen a hex mesh (general locator)
  - paper: "Katerina Jurkova, Franck Ledoux, Raphael Kuate, Thomas Rickmeyer, Timothy J. Tautges and Hamdi Zorgati, Local topological modifications of hexahedral meshes, part II, combinatorics and relation to Boy surface, ESAIM Proceedings 24, 2008, 34 to 45"
    locator: the change of parity of the number of hexes by a Boy surface in the dual (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: Section 2.2 on the dual mesh, sheets and chords, and Section 5 on sheet, flipping and atomic operators and padding
---

The spatial twist continuum is the dual of a hex mesh, looked at as a set of surfaces. Put a point at the center of each hex. Two hexes that share a face are joined through that face. When you follow a hex across one face and then across the opposite face of the next hex, and so on, you move along a column of hexes. When you take all the hexes that are crossed by one layer, you get a surface, a sheet. The sheets cross each other, and each hex is a point where three sheets cross. Murdoch, Benzley, Blacker and Mitchell gave this view its name in 1997. It is the language in which most theory of [hexahedral mesh generation](/hexahedral-mesh-generation/) is written, and the base of [whisker weaving](/whisker-weaving/) and of many editing operations.

## In plain words

Cut a cube into $3 \times 3 \times 3$ small cubes. It has three families of slabs, normal to $x$, $y$ and $z$. Draw one surface through the middle of each slab. Each small cube is where three of these nine surfaces cross.

An unstructured hex mesh has the same structure, but the layers bend, close up and can cross themselves. To find a layer, start at an edge and, in each quad, jump to the opposite edge. The surface through the layer you reach is a sheet. Two sheets meet along a column of hexes, a chord. Three sheets meet at a hex. On the boundary, each sheet leaves a closed curve through the quads, a loop. So the boundary quads fix the loops, and a hex mesh fills in surfaces that end at these loops.

## The idea

**The dual complex.** The dual of a hex mesh has a vertex for each hex, an edge for each inner face, a face for each inner edge and a cell for each inner vertex. Because each hex has 6 faces and each face has 4 edges, the dual is regular: each inner dual vertex has 6 dual edges, and each inner dual edge is on 4 dual faces. This regularity is what the sheet view uses. In the primal mesh, edges can have any number of hexes around them, but in the dual the local structure is always that of a cube grid.

**Sheets.** On a quad, the edges $ab$ and $cd$ are opposite, and so are $bc$ and $da$. Join each edge of the mesh to the edges opposite to it on each of its faces, and take the classes of the equivalence relation that this generates. A class is a sheet. Seen in the dual, a sheet is a 2-manifold surface made of dual faces, possibly with a boundary and possibly with self-crossings. Murdoch and others called the sheets twist planes, and Tautges and Knoop called them pseudo-hyperplanes.

**Chords.** In the same way, a hex has three pairs of opposite faces. Join each face to the opposite face in each hex that has it. A class is a chord, a column of hexes. A chord is the curve where two sheets cross, or where one sheet crosses itself. It is either a closed ring or a curve whose two ends are boundary quads.

**Hexes are triple points.** A hex has three classes of four parallel edges, and each class lies in one sheet. So each hex is where three sheets meet, or two sheets if one of them passes the hex twice, or one sheet three times. The arrangement of surfaces cuts the solid into cells, and these cells are dual to the vertices of the mesh.

**What is proved, and where.** The claims that each class of parallel edges of a hex lies in one sheet, that a sheet is a layer of hexes glued across their shared faces, and that the boundary of a sheet is a union of boundary loops, are proved in full in the correctness proof on the [whisker weaving](/whisker-weaving/) page, parts 1 to 3 and 5. The same proof shows $6H = 2I + B$ for $H$ hexes, $I$ inner faces and $B$ boundary quads. The chords give a second view of this count. Each boundary quad is the end of exactly one chord, and an open chord has two ends, so $B$ is twice the number of open chords. The [hexahedral mesh existence theorem](/hexahedral-mesh-existence-theorem/) uses the converse direction: when an arrangement of surfaces with the right boundary loops is dual to a valid mesh. Mitchell gives conditions for this, which rule out, for example, cells that touch themselves and configurations that are not manifolds.

**The boundary does not fix the sheets.** The loops are fixed by the boundary quads, but a sheet can have any genus and any number of loops as its boundary, and there can be closed sheets with no boundary at all. This is the difference from the 2D case. The dual of a quad mesh is an arrangement of curves, and each curve is either closed or runs from boundary to boundary. In 3D, the choice of the surfaces that fill in the loops is free, and that freedom is both the power and the difficulty of the dual view.

## Examples

**Structured grids.** A grid of $n \times m \times p$ hexes has $n + m + p$ sheets, all planar disks: $n$ slabs normal to $x$, $m$ normal to $y$ and $p$ normal to $z$. Two sheets of different families meet in a chord, so there are $nm + mp + pn$ chords, all open. Three sheets of three families meet in a hex, so there are $nmp$ hexes. The boundary has $2(nm + mp + pn)$ quads, two ends for each chord, and $n + m + p$ loops. For $2 \times 2 \times 2$ this gives 6 sheets, 12 chords, 8 hexes and 24 boundary quads. Each loop goes around the cube through 8 quads, and $6 \times 8 = 48 = 2 \times 24$, because each boundary quad is a crossing of two loops.

**Small unstructured cases.** The whisker weaving page computes the sheets of two meshes with code and checks them in its tests.

| mesh | hexes | boundary quads | sheets | loops | Euler characteristic of the sheets |
|---|---|---|---|---|---|
| two cubes side by side | 2 | 10 | 4 | 4 | 1, 1, 1, 1 |
| pillowed cube | 7 | 6 | 4 | 3 | 1, 1, 1, 2 |

For the two cubes, the chords are the 5 pairs of crossing sheets, and $10 = 2 \times 5$. The pillowed cube is a cube cut into an inner cube and six hexes that join each inner face to an outer face. Its boundary is the same 6 quads as one cube, with 3 loops. Three sheets are disks through the inner cube. The fourth sheet goes around the inner cube through the six outer hexes and is a closed sphere, with Euler characteristic 2 and no loop. So two meshes with the same boundary, one hex and seven hexes, have different sheets, and a sheet can be closed.

**Doublets.** If two hexes share two faces, the mesh has a doublet. In the dual, two dual vertices are then joined by two dual edges, and no placement of the vertices gives both hexes a good shape: one of the faces always has an angle of at least $\pi$. The standard fix is to insert a new closed sheet around a set of hexes, which is called pillowing or padding, as in the pillowed cube above.

## Where it is used

- **Whisker weaving** builds the dual first. It starts from the boundary loops, fills them in with sheets one crossing at a time, and only at the end makes the hexes. The theory says when such a weave is a valid mesh, but the process has no general guarantee to finish.
- **Existence proofs.** Thurston and Mitchell prove that a ball with an even number of boundary quads has a hex mesh by building an arrangement of surfaces with the given loops.
- **Sheet and chord operations.** Removing a sheet takes away a layer of hexes, which coarsens a mesh, as in the sheet extraction of Borden, Benzley and Shepherd. Inserting a sheet adds a layer, which refines a mesh or pads a boundary. Collapsing a chord removes a column. These operations keep the mesh all hex, because they change whole dual surfaces and curves.
- **Padding.** Many methods, such as [polycube hex meshing](/polycube-hex-meshing/), add a layer of hexes along the boundary to remove bad corners. In the dual this is one new sheet parallel to the boundary.
- **Local operators.** Tautges and Knoop describe small dual operations that can be combined into flips and sheet operations. The survey of Pietroni and others notes that the completeness of this set is not proved. These operations keep the parity of the number of hexes. Jurkova and others add a Boy surface, a closed surface with one triple point, to the dual to change the parity.
- **Reading a mesh.** The sheets and chords show the global structure of a mesh. For example, a mesh made by [hexahedral sweeping](/hexahedral-sweeping/) has one sheet for each layer of the sweep, and a closed sheet shows where a layer was padded.

## References
