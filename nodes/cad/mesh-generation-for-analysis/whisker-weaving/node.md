---
tag: 4SHZ6G
kind: algorithm
slug: whisker-weaving
name: Whisker weaving
aliases:
- Tautges-Blacker-Mitchell whisker weaving
area: cad/mesh-generation-for-analysis
level: research
summary: Tautges, Blacker and Mitchell's hex mesher that first builds the spatial twist continuum from the boundary quad mesh, then derives the hexes from it.
solves: [hexahedral-mesh-generation]
model: real-ram
complexity:
  vars: {H: the number of hexes (dual sheet step)}
  time: {worst: O(H α(H))}
  space: {extra: O(H)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [Timothy J. Tautges, Ted D. Blacker, Scott A. Mitchell]
  note: Whisker weaving was published in 1996 together with the spatial twist continuum of Murdoch and others. Folwell and Mitchell made it more reliable in 1999 by curve contraction.
prereqs: [spatial-twist-continuum, hexahedral-mesh-generation, disjoint-set]
see_also: [hexahedral-mesh-existence-theorem, plastering, paving, hexahedral-sweeping, polycube-hex-meshing, frame-field-hex-meshing, mesh-untangling, union-by-size]
sources:
  - paper: "Timothy J. Tautges, Ted Blacker and Scott A. Mitchell, The whisker weaving algorithm, a connectivity-based method for constructing all-hexahedral finite element meshes, International Journal for Numerical Methods in Engineering 39(19), 1996, 3327 to 3349"
    locator: the sheet diagrams with whiskers, the local weaving rules, and the dual step that makes the hexes (general locator)
  - paper: "Peter Murdoch, Steven Benzley, Ted Blacker and Scott A. Mitchell, The spatial twist continuum, a connectivity based method for representing all-hexahedral finite element meshes, Finite Elements in Analysis and Design 28(2), 1997, 137 to 149"
    locator: the sheets and chords of a hex mesh and their crossings (general locator)
  - paper: "N. T. Folwell and S. A. Mitchell, Reliable whisker weaving via curve contraction, Engineering with Computers 15(3), 1999, 292 to 302"
    locator: the contraction of the boundary loops that fixes the sheet arrangement before the hexes are made (general locator)
  - paper: "Franck Ledoux and Jean-Christophe Weill, An extension of the reliable whisker weaving algorithm, Proceedings of the 16th International Meshing Roundtable, 2008, 215 to 232"
    locator: further rules for the weaving (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the section on dual methods, which reports poorly shaped, inverted and degenerate elements for self-intersecting loops
---

Whisker weaving makes an all-hex mesh from a closed quad mesh of the boundary by working on the dual of the mesh, not on the hexes. The dual of a hex mesh is its [spatial twist continuum](/spatial-twist-continuum/): a set of surfaces called sheets, one for each layer of hexes, which cross three at a time inside each hex. The boundary quad mesh fixes the edges of the sheets, because each chain of opposite edges on the surface, called a loop, is where one sheet meets the boundary. Whisker weaving starts from these loops and decides, by local rules on connectivity alone, where the sheets cross. Each triple crossing becomes a hex, and the geometry is placed last. This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it works only from connectivity and has no guarantee to finish, while that page states the general problem and its limits. The code on this page implements one exact core step, the dual sheets of a given hex mesh, and not the weaving loop.

## In plain words

A brick wall has rows of bricks, and between two rows there is a layer of mortar. A block of bricks in 3D has such layers in three directions. Think of each layer as a thin sheet that cuts through one row of bricks. Every brick sits where three sheets cross.

On the outside of the block we see only the faces of the bricks. On that surface, each sheet shows up as a closed band of faces that goes around the block. Whisker weaving starts from these bands. It draws each sheet as a disk with short open threads, the whiskers, along its edge, and then ties threads of three sheets together, one brick at a time, until no thread is loose. Then it turns each knot of three sheets into a brick.

The rules are local, so the method can get stuck or tie a bad knot.

## The problem

The input of whisker weaving is a closed quad mesh $Q$ of the boundary of a solid, usually of a ball, with an even number of quads. The output is a hex mesh of the solid whose boundary quads are exactly $Q$. The method builds the combinatorial structure first: the sheets, how they cross, and so the list of hexes with their vertex ids. Vertex positions come last, by smoothing.

The code on this page solves the inverse problem, which is exact. Given a conforming hex mesh, it finds the sheets, the three sheets of each hex, the boundary quads and the loops. This is the structure that weaving must produce, and it is the test of any woven result.

## The algorithm

On a face $(a, b, c, d)$ the edges $ab$ and $cd$ are opposite, and so are $bc$ and $da$. A sheet is a class of edges under the closure of "opposite on a common face". Inside a hex this joins the four parallel edges of each direction, so a sheet cuts each of its hexes through four parallel edges. A loop is a class of boundary edges under the same closure on the boundary quads only. A union-find structure ([disjoint sets](/disjoint-set/)) finds both.

```pseudo id=main
DUAL-SHEETS(H)
L1  make a singleton set for every edge of every hex
L2  for each hex h in H do
L3      for each class c of four parallel edges of h do
L4          union the four edges of c
L5  sheets ← the sets of the union-find structure
L6  for each hex h: crossing(h) ← the sheets of the three classes of h
L7  B ← the faces that belong to exactly one hex
L8  make a singleton set for every edge of a quad in B
L9  for each quad (a, b, c, d) in B do
L10     union ab with cd, and union bc with da
L11 loops ← the sets of the second structure
L12 return sheets, crossing, B, loops
```

Lines L1 to L5 find the sheets. Line L6 records the three sheet crossings of each hex. A sheet that crosses itself appears twice in the same hex. Line L7 finds the boundary by counting faces. Lines L8 to L11 find the loops of the boundary quad mesh. Each loop is inside one sheet, and each sheet that reaches the boundary has one or more loops as its edge.

**The weaving loop.** The published method runs in the other direction. In words, it does these steps:

1. Find the loops of the boundary quad mesh $Q$. Each loop gets its own sheet, drawn as a disk. Each quad of $Q$ is a point where two loops cross, so it appears on the edge of two sheet diagrams, and from it a whisker points into each disk.
2. Pick three sheets whose loops cross each other near one corner of the surface, and whose whiskers are free there.
3. Join the matching whiskers of the three sheets in one new crossing point. This point is a new hex, and its faces toward the surface are the quads that the whiskers came from.
4. Update the free whiskers, and apply local rules that join whiskers that now face each other.
5. Repeat steps 2 to 4 until no whisker is free, or stop with failure if no rule applies.
6. Check the result: each sheet must be a surface and the cells of the arrangement must be simple. Then the dual of the woven arrangement gives the hexes, and smoothing places the inner vertices.

The checks of step 6 are the properties that DUAL-SHEETS computes for a finished mesh.

## Example

The two cubes $[0, 2] \times [0, 1] \times [0, 1]$ make the smallest mesh with an interior face.

| mesh | $H$ | $B$ | $I$ | sheets | loops | Euler characteristic of the sheets |
|---|---|---|---|---|---|---|
| two cubes | 2 | 10 | 1 | 4 | 4 | 1, 1, 1, 1 |
| pillowed cube | 7 | 6 | 18 | 4 | 3 | 1, 1, 1, 2 |

In both rows $6H = 2I + B$. For the two cubes, the sheets are the plane $x = 1/2$ through the first cube, the plane $x = 3/2$ through the second cube, and the two planes $y = 1/2$ and $z = 1/2$ through both cubes. Each is a disk, with Euler characteristic $1$, and each has one loop as its edge.

The pillowed cube is the cube $[0, 3]^3$ cut into the inner cube $[1, 2]^3$ and six hexes that join each inner face to an outer face. Its boundary is the same 6 quads as a single cube, with 3 loops. Three sheets are disks through the inner cube, bounded by the three loops. The fourth sheet goes through the six outer hexes around the inner cube. It has 8 vertices (the 8 edges from inner to outer corners), 12 edges and 6 faces, so its Euler characteristic is $2$: it is a closed sphere with no loop. The boundary loops do not fix the sheets, and a weaving that makes one sheet per loop can never make this mesh.

## Correctness

The proof below shows that DUAL-SHEETS returns the sheets and loops as defined. The key fact is that the four parallel edges of a class are linked by three faces of the hex, so the union of L4 and the relation "opposite on a common face" give the same classes. From this, each sheet cuts each of its hexes through whole classes of four parallel edges, and the sheet is a layer of quadrilateral cells, one per hex, glued across shared faces. Its free sides lie on boundary quads, so the boundary of a sheet is a union of loops. Counting the faces of all hexes gives $6H = 2I + B$, so the number of boundary quads is even for every hex mesh.

What is proved and what is measured are different here. The dual sheet step is proved exact. For the weaving loop, there is no general guarantee: it can stop with free whiskers, and when it ends it can give knotted sheets, degenerate hexes or inverted hexes. The survey of Pietroni and others reports that such elements are common when the boundary has self-intersecting loops. The tests compare DUAL-SHEETS with a breadth first search over the opposite-edge relation on 500 random voxel meshes, with random vertex labels and random vertex orders of each hex. They also check $6H = 2I + B$, that the sheet boundaries are unions of loops, and the Euler characteristic of each sheet against a direct count on its cross section.

## Complexity

DUAL-SHEETS does 9 unions per hex and one face count per face, so it runs in $O(H \alpha(H))$ time with union by size and path halving, where $\alpha$ is the inverse Ackermann function. The space is $O(H)$. The weaving loop makes one hex per step and each step is local, but a run can need many failed attempts and can stop without a mesh, so its cost is not a useful bound on its success.

## Properties

- **Connectivity first.** The weaving uses no coordinates, so it does not depend on the shape of the solid. This is its strength and its weakness: the hexes have the right connectivity but can be badly shaped.
- **Boundary conforming.** The boundary quad mesh is not changed, which is why the method was of interest for assemblies with fixed interface meshes.
- **Parity.** A woven result can only exist if the number of boundary quads is even, because $B = 6H - 2I$.
- **No general guarantee.** Termination, valid hexes and good shape are not proved for the weaving loop.
- **Exact dual step.** The sheets, crossings and loops of a given mesh are computed exactly and fast.

## Variants and improvements

- **Curve contraction.** Folwell and Mitchell first fix the arrangement of the sheets by contracting the loops on the surface, and only then make hexes. This is more reliable than the original greedy weaving.
- **More rules.** Ledoux and Weill extend the rule set of reliable whisker weaving.
- **Surface modification.** Some methods change the boundary quad mesh first to remove self-intersecting loops, which are the main source of bad elements.
- **Dual editing.** The same dual view is used to edit a finished mesh, by inserting a sheet (pillowing) or by removing one (sheet extraction). See the [spatial twist continuum](/spatial-twist-continuum/).

## When to use it

Whisker weaving is mainly of research and teaching interest. It shows how the dual view turns hex meshing into a problem about surfaces, and its checks are useful for any hex mesh. For production meshes of CAD parts, [sweeping](/hexahedral-sweeping/) of a decomposition is the common choice, and for organic shapes [polycube](/polycube-hex-meshing/) and [frame field](/frame-field-hex-meshing/) methods are used.

## Pitfalls

- **Self-intersecting loops.** A loop that crosses itself must bound a sheet that crosses itself or pairs with another loop. The local rules do not find such structures in general, and the result has degenerate or inverted hexes.
- **Odd boundary.** With an odd number of boundary quads no hex mesh exists, so the weaving must fail. Check the parity first.
- **Closed sheets.** A sheet with no loop, such as the pillow sheet of the example, is never made if each sheet comes from a loop. Meshes that need such sheets need another step, such as pillowing.
- **Geometry last.** Good connectivity does not give good shape. The hexes must be placed and smoothed, and they can still be inverted.

## Implementations

## History

Murdoch, Benzley, Blacker and Mitchell described the spatial twist continuum, the dual of a hex mesh, in the mid 1990s. Tautges, Blacker and Mitchell published whisker weaving in 1996 as a way to build the dual from the boundary and then take the hexes from it. Folwell and Mitchell gave a more reliable version by curve contraction in 1999, and Ledoux and Weill extended it in 2008. At the same time, Mitchell and Thurston proved that the parity condition is the only topological condition for a ball, which is the subject of the [hexahedral mesh existence theorem](/hexahedral-mesh-existence-theorem/).

## References
