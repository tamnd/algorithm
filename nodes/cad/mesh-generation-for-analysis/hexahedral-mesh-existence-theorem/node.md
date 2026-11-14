---
tag: 8E281Y
kind: theorem
slug: hexahedral-mesh-existence-theorem
name: Hexahedral mesh existence theorem
aliases:
- Mitchell-Thurston theorem
area: cad/mesh-generation-for-analysis
level: research
summary: A ball bounded by a quadrilateral mesh with an even number of quads has a compatible hexahedral mesh, as Thurston and Mitchell proved, and Eppstein gave linear size.
prereqs: [hexahedral-mesh-generation, spatial-twist-continuum]
see_also: [whisker-weaving, plastering, paving, hexahedral-sweeping, octree-mesh-generation, frame-field-hex-meshing, jordan-curve-theorem, euler-formula]
sources:
  - paper: doi:10.1007/3-540-60922-9_38
    title: Scott A. Mitchell, A characterization of the quadrilateral meshes of a surface which admit a compatible hexahedral mesh of the enclosed volume, STACS 96, Lecture Notes in Computer Science 1046, Springer, 1996
    locator: the main theorem and its proof by the extension of the dual loops of the boundary to an arrangement of surfaces (general locator)
  - paper: "W. P. Thurston, Hexahedral decomposition of polyhedra, posting to the newsgroup sci.math, 1993"
    locator: the whole posting, which gives the same result for the ball by immersed surfaces
  - paper: doi:10.1016/S0925-7721(98)00032-7
    title: David Eppstein, Linear complexity hexahedral mesh generation, Computational Geometry 12(1-2), 1999, 3 to 16
    locator: the construction with O(n) hexahedra for n boundary quads (general locator)
  - paper: "Marshall W. Bern, David Eppstein and Jeff Erickson, Flipping cubical meshes, Engineering with Computers 18(3), 2002, 173 to 187"
    locator: the flips of cubical meshes and the pseudo-shellings of simply connected domains with an even number of boundary quads (general locator)
  - paper: "Jeff Erickson, Efficiently hex-meshing things with topology, Discrete and Computational Geometry 52(3), 2014, 427 to 449"
    locator: the conditions and the construction for domains that are not balls (general locator)
  - paper: "Kilian Verhetsel, Jeanne Pellerin and Jean-François Remacle, Finding hexahedrizations for small quadrangulations of the sphere, ACM Transactions on Graphics 38(4), 2019"
    locator: the meshes of the buffer cubes, which give at most 78n hexahedra for a ball with n boundary quads (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the paragraphs on existence, linear complexity meshing and Schneiders' pyramid
---

The hexahedral mesh existence theorem answers the most basic question of [hexahedral mesh generation](/hexahedral-mesh-generation/): given a quad mesh of the boundary of a solid, is there any hex mesh of the solid with exactly these boundary quads? A simple count shows that the number of boundary quads must be even, for any solid. Thurston in 1993 and Mitchell in 1996 showed, independently, that for a ball this is also enough. Their proofs build a mesh whose hexes are only topological cubes, often badly shaped, so the theorem says that a mesh exists, not that a good one does.

This page proves the parity condition in full and sketches the converse. The [spatial twist continuum](/spatial-twist-continuum/) page describes the dual sheets that the converse uses.

## Statement

A hex mesh of a solid is conforming: two hexes meet in a whole shared face, a whole edge, a vertex, or not at all. Each quad face of the mesh is a face of one hex, then it lies on the boundary, or of two hexes, then it is inside. Let $H$ be the number of hexes, $I$ the number of inner quads and $B$ the number of boundary quads.

**Lemma (parity).** For every hex mesh of every solid, of any shape and topology,

$$6H = 2I + B,$$

so $B$ is even and $H \ge B/6$.

**Theorem (Thurston 1993, Mitchell 1996).** Let $Q$ be a quad mesh of the sphere that bounds a ball. Then there is a hex mesh of the ball whose boundary quads are exactly the quads of $Q$ if and only if the number of quads of $Q$ is even. The hexes of this mesh are topological cubes: each is a ball whose boundary is split into six quads like the faces of a cube.

**Linear size (Eppstein 1999).** If $Q$ has $n$ quads, $n$ even, such a mesh exists with $O(n)$ hexes.

## In plain words

Every hex has six faces. Count all faces of all hexes, one hex at a time. A face inside the solid is counted twice, once from each of its two hexes. A face on the outside is counted once. The total is six times the number of hexes, which is even. The inside faces add an even number, so the outside faces must be an even number too.

So if the outside of a solid is covered by an odd number of quads, no hex mesh can match it, no matter how clever. The theorem says that for a solid without holes this is the only obstacle: with an even number of quads there is always some hex mesh, but its hexes may be twisted and of very bad shape.

## Proof

**Proof of the lemma.** Count the pairs $(h, f)$ where $h$ is a hex and $f$ is one of its six faces, as quads of the mesh. Each hex gives 6 pairs, so there are $6H$ pairs. Each inner quad is a face of two hexes and each boundary quad of one hex. If a hex has two of its own faces glued to each other, that quad still gives two pairs, so it counts as an inner quad here. So the number of pairs is also $2I + B$. Then $B = 6H - 2I$ is even, and $B \le 6H$. The count uses only that the mesh is conforming, not the shape or the topology of the solid. $\square$

**The converse, a sketch.** The sketch follows Mitchell (1996, main theorem, general locator). The full proof is in that paper, and Thurston's posting gives a similar argument.

1. In each quad of $Q$, join the midpoints of the two pairs of opposite edges. These segments link up into closed curves on the sphere, the dual loops of $Q$. Each quad is a point where two loop pieces cross, so the loops have exactly $n$ crossing points.
2. In a hex mesh, the dual sheets are surfaces that meet the boundary in these loops. Two sheets, or one sheet with itself, meet along curves. A curve of this kind that reaches the boundary ends at a crossing point of the loops, and each arc has two ends. So the $n$ crossing points must pair up, which is the parity condition again, seen from the dual.
3. For a ball and even $n$, extend each loop to a surface inside the ball, in general position, so that the intersection curves join the crossing points in pairs. Then the arrangement of surfaces cuts the ball into cells, and each triple point of the surfaces is dual to a hex.
4. In general such an arrangement is not yet the dual of a valid hex mesh: it can have cells that touch themselves or faces that are not disks. Mitchell gives conditions for a valid dual and shows that adding further sheets, which do not meet the boundary, removes every bad case. The result is a topological hex mesh with boundary $Q$.

Neither proof gives good elements. The surfaces are chosen only up to topology, so the hexes need not be convex, and when they are placed in space they can be inverted or almost flat. Eppstein's construction gives the linear size by a different route: it fills the ball with a layer and a set of buffer cubes, each of which has a fixed small boundary and so a fixed hex mesh, but again with no bound on the shape. $\blacksquare$

## Consequences

- **The parity test.** Before any hex meshing method tries to close a void, it can count the quads of the void. An odd count means certain failure. This is why [plastering](/plastering/) must avoid odd voids, and why the [whisker weaving](/whisker-weaving/) loop has to be steered.
- **The 2D analogue.** The same count for quads in the plane gives $4F = 2I + B$, so a polygon with an odd number of boundary edges has no quad mesh. For a polygon, an even number is enough, and simple methods such as [paving](/paving/) show this in practice. In 3D the converse is much harder.
- **A lower bound.** Since $H \ge B/6$, a mesh needs at least one hex for each six boundary quads. A cube with its faces split into $2 \times 2$ quads has $B = 24$, and its $2 \times 2 \times 2$ grid has $H = 8$ and $I = 12$, so $48 = 24 + 24$.
- **Sizes.** Mitchell's construction can need $O(n^2)$ hexes. Eppstein's gives $O(n)$, and with the buffer cube meshes of Verhetsel, Pellerin and Remacle the bound is $78 n$ hexes, with hexes that have a geometric realization.
- **Flips.** Bern, Eppstein and Erickson showed that each simply connected domain with an even number of boundary quads has a pseudo-shelling, a hex mesh built one hex at a time so that the part left is always a ball. This gives flip operations for hex meshes, as for tetrahedral meshes.

## Tightness

**The parity condition is needed.** Take the six quads of a cube and split one face $ABCD$ into the two quads $ABCX$ and $AXCD$, where $X$ is a new point inside the face, joined to $A$ and $C$. This is a quad mesh of the sphere with $7$ quads, so by the lemma no hex mesh has this boundary.

**The ball hypothesis is needed.** For solids with holes or handles, an even number of quads is not enough in general. Mitchell's paper and Erickson's 2014 paper give extra conditions on cycles of the boundary mesh for such domains (general locator).

**Existence is not quality.** Even for small balls, a good mesh can be hard to find. Schneiders' pyramid is a square pyramid whose base is split into 4 quads and whose four triangles are each split into 3 quads, so it has $16$ quads. It was given in 1995 as a boundary for which no hex mesh was known. Meshes with $118$ hexes (2002), $88$ (2010), $36$ (2018) and $44$ (2019) were found later, by long searches, and the theorem gives no help in finding a small or well-shaped one. Whether every even quad mesh of a convex polyhedron with planar convex quads has a mesh of convex hexes with planar faces is, as far as the survey of Pietroni and others reports, still open.

## History

William Thurston described the result for the ball in a 1993 posting to the newsgroup sci.math, using immersed surfaces. Scott Mitchell proved it independently and published it at STACS in 1996, with a characterization by the dual of the mesh that also covers some surfaces of higher genus. David Eppstein gave a construction with $O(n)$ hexes in 1999. Bern, Eppstein and Erickson studied flips and shellings of cubical meshes in 2002, and Erickson treated domains with topology in 2014. Carbonera and Shepherd gave a fully explicit construction in 2010, and Verhetsel, Pellerin and Remacle found small meshes for the buffer cubes in 2019, which gives the bound of $78 n$ hexes.

## References
