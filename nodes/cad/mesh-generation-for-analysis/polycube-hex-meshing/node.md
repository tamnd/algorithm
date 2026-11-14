---
tag: ZACEGX
kind: algorithm
slug: polycube-hex-meshing
name: Polycube-based hex meshing
aliases:
- polycube map
- PolyCut
area: cad/mesh-generation-for-analysis
level: research
summary: Deforms a solid into a polycube, an axis-aligned union of cubes, by a volumetric map, meshes the polycube with a grid and maps the hexes back.
solves: [hexahedral-mesh-generation]
model: real-ram
complexity:
  vars: {C: the number of voxels of the polycube, s: the number of grid cells per voxel edge}
  time: {worst: O(C s^3)}
  space: {extra: O(C s^3)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2011
  people: [James Gregson, Alla Sheffer, Eugene Zhang]
  note: Tarini, Hormann, Cignoni and Montani introduced polycube maps in 2004 for texture mapping. Gregson, Sheffer and Zhang used a volumetric polycube deformation to make all-hex meshes in 2011, and later work improved the choice of the polycube and the injectivity of the map.
prereqs: [hexahedral-mesh-generation, mesh-parameterization, scaled-jacobian]
see_also: [frame-field-hex-meshing, hexahedral-sweeping, plastering, octree-mesh-generation, mesh-untangling, volumetric-spline-parameterization, as-rigid-as-possible-deformation, bernstein-polynomials]
sources:
  - paper: "Marco Tarini, Kai Hormann, Paolo Cignoni and Claudio Montani, PolyCube-Maps, ACM Transactions on Graphics 23(3), 2004"
    locator: the definition of a polycube and of a polycube map (general locator)
  - paper: "James Gregson, Alla Sheffer and Eugene Zhang, All-hex mesh generation via volumetric PolyCube deformation, Computer Graphics Forum 30(5), 2011, 1407 to 1416"
    locator: the deformation that turns surface normals to the axes, the grid of the polycube, the inverse map and the padding layer (general locator)
  - paper: "Marco Livesu, Nicholas Vining, Alla Sheffer, James Gregson and Riccardo Scateni, PolyCut, monotone graph-cuts for PolyCube base-complex construction, ACM Transactions on Graphics 32(6), 2013, article 171"
    locator: the labeling of the boundary by axes under topological conditions for a valid polycube (general locator)
  - paper: "Xiao-Ming Fu, Chong-Yang Bai and Yang Liu, Efficient volumetric PolyCube-map construction, Computer Graphics Forum 35(7), 2016, 97 to 106"
    locator: a deformation energy that grows without bound for inverted tetrahedra (general locator)
  - paper: "David Eppstein and Elena Mumford, Steinitz theorems for orthogonal polyhedra, Proceedings of the Symposium on Computational Geometry, 2010, 429 to 438"
    locator: the graph conditions for an orthogonal polyhedron (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the section on polycube maps, which states that neither the labeling nor the flip-free map is guaranteed
---

A polycube method makes a hex mesh of a solid in three steps. First it finds a polycube, a solid made of axis-aligned unit cubes, with the same shape in a rough sense. Then it computes a volumetric map between the solid and the polycube. Last it meshes the polycube with a regular grid and maps the grid back into the solid. This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it gets a full hex mesh from a map to a polycube, while that page states the general problem and its limits. The code on this page implements one exact core step: the grid of a given polycube under a given map, with a test that proves every hex valid.

## In plain words

Imagine the solid is made of soft clay. You press the clay until every face of it is flat and points along one of the three axes, so the clay looks like a stack of toy blocks. Blocks are easy to cut into small equal cubes.

Now draw these small cubes on the clay and let the clay spring back to its first shape. The small cubes bend with the clay, and they become the hexes of the mesh.

The hard parts are to choose a good stack of blocks for the shape, and to press the clay so that no part of it folds over another part. If the clay folds, some hexes turn inside out.

## The problem

The input is a polycube $P$, a finite set $C$ of unit voxels with integer corners, and a map $g$ from $P$ into space, given by the images of the integer voxel corners and trilinear on each voxel. In a full method, $g$ is the inverse of the map from the solid to the polycube. The output is the hex mesh of resolution $s$: the images under $g$ of the cells of the grid of spacing $1/s$ in $P$. A hex is valid if $\det J > 0$ at every point of it, as on the [scaled Jacobian](/scaled-jacobian/) page.

## The algorithm

The core step first proves that $g$ has a positive Jacobian on every voxel, then builds the grid. The test uses the 27 [Bernstein](/bernstein-polynomials/) coefficients of $\det Dg$ on each voxel, which is a polynomial of degree 2 in each variable.

```pseudo id=main
POLYCUBE-GRID(C, G, s)
L1  for each voxel c of C do
L2      if some Bernstein coefficient of det Dg on c is at most 0 then return failure
L3  K ← the grid points k / s, with k integer, that lie in some voxel of C
L4  for each grid point p of K do
L5      x_p ← g(p), by the trilinear map of a voxel that contains p
L6  H ← empty list
L7  for each voxel c of C and each cell q of side 1/s in c do
L8      append the hex of the 8 points x_p at the corners of q to H
L9  return H
```

Lines L1 and L2 are the certificate. Lines L3 to L5 map the grid, and lines L6 to L8 make one hex per grid cell. The code names a grid point by its integer key $k$, so two cells that share a face use the same four points.

**The full method.** A polycube pipeline wraps this step, in words:

1. Tetrahedralize the solid.
2. Label each boundary triangle with one of the six directions $\pm x$, $\pm y$, $\pm z$, often the one closest to its normal, and then fix the labels so that they describe a real polycube.
3. Deform the tetrahedral mesh so that each boundary patch becomes flat and normal to its label. This gives a map $f$ from the solid to a polycube.
4. Scale the polycube, sample it with an integer grid, and place each grid point in the solid by $f^{-1}$, found by point location in the deformed tetrahedra.
5. Add a padding layer of hexes on the boundary, and improve the mesh by untangling and smoothing.

## Example

Take the L-shaped polycube with the voxels $(0, 0, 0)$, $(1, 0, 0)$ and $(0, 1, 0)$. Let $g$ be the identity, except at the two corners $(1, 1, 0)$ and $(1, 1, 1)$ on the inner edge of the L, which move to $(\frac54, \frac54, 0)$ and $(\frac54, \frac54, 1)$. This rounds the inner corner a little.

| voxel | least Bernstein coefficient | largest | volume of its image |
|---|---|---|---|
| $(0, 0, 0)$ | $1$ | $\frac32$ | $\frac54$ |
| $(1, 0, 0)$ | $\frac34$ | $\frac54$ | $1$ |
| $(0, 1, 0)$ | $\frac34$ | $\frac54$ | $1$ |

All coefficients are positive, so L2 accepts. With $s = 2$ the grid has $63$ points and $24$ hexes, and $56$ boundary quads, $4$ for each of the $14$ unit faces of the L. The grid point $(\frac12, \frac12, 0)$ goes to $(\frac{9}{16}, \frac{9}{16}, 0)$. The least corner Jacobian of a hex is $\frac{3}{32} = \frac34 \cdot 2^{-3}$, and the hex volumes add up to $\frac{13}{4}$, the sum of the voxel volumes.

## Correctness

The full proof is below. A trilinear map restricted to a grid cell is again trilinear, so each hex is $g$ on its cell, and $\det J$ of the hex is $s^{-3}$ times $\det Dg$. The Bernstein basis is at least $0$ and adds up to $1$, so positive coefficients give $\det Dg > 0$ on the whole voxel. Thus, when L2 accepts, every hex at every resolution $s$ is valid at every point, not only at its corners. The hexes are conforming because the maps of two voxels agree on their shared face. If $g$ is also one to one on $P$, the hexes tile the image $g(P)$.

The conditions are exactly these: $g$ is trilinear on each voxel and given by its corner images, every voxel passes the Bernstein test, and, for a mesh of the solid, $g$ is one to one. The proof does not cover the steps that make $g$. The survey of Pietroni and others notes that no current method guarantees a valid polycube labeling, nor a volumetric map without flipped tetrahedra. What is measured is the quality that published methods report on their test models. The tests compare the step with brute force on 500 random polycubes and maps: the set of grid points, face counts for conformity, positive corner Jacobians when the map is accepted, the volume sum, and the Bernstein form against direct values of $\det J$.

## Complexity

The test of L1 and L2 costs a constant per voxel. The grid has $O(|C| s^3)$ points and exactly $|C| s^3$ hexes, so the step takes $O(|C| s^3)$ time and space. In a full method the deformation of the tetrahedral mesh dominates. It is an iterative nonlinear optimization with no general bound on its number of steps.

## Properties

- **Regular inside.** Every inner vertex of the grid has 6 edges, except along the edges and corners of the polycube, where the irregular vertices sit.
- **Coarse structure.** The polycube is a coarse block structure of the mesh. Its blocks can be meshed with different numbers of cells along each axis, as long as the counts match across blocks.
- **Sensitive to the polycube.** Too few cubes give bad hexes near features. Too many give a complex structure with many irregular vertices.
- **No closure problem.** Unlike [plastering](/plastering/), there is no void to close, since the whole polycube is a grid.

## Variants and improvements

- **Labeling first.** Gregson and others label the boundary by the nearest axis and then fix it. Livesu and others search the labelings for one that meets the conditions for a valid polycube, based on the work of Eppstein and Mumford.
- **Deformation first.** Some methods deform the solid freely until a polycube appears, and then read off the labels.
- **Flip-free energies.** Fu, Bai and Liu use an energy that grows without bound when a tetrahedron flips, so the map stays locally one to one.
- **Generalized polycubes.** Some methods allow a polycube that is not embedded in space, which allows fewer cubes for some shapes.
- **Spline output.** The polycube map also gives a volumetric spline parameterization of the solid, for [isogeometric analysis](/volumetric-spline-parameterization/).

## When to use it

Use a polycube method for a solid that looks roughly like a union of boxes, such as a part with flat faces at right angles, or a smooth organic shape where a few hundred irregular vertices are fine. For a solid with a sweep direction, [sweeping](/hexahedral-sweeping/) is simpler. When the shape has features at many angles, [frame field](/frame-field-hex-meshing/) methods align hexes better, at the cost of less robust singularity structures.

## Pitfalls

- **Positive corners are not enough.** A voxel can have corner Jacobians $4$ and $12$ while $\det Dg = 4(1 - 2w)(1 - 4w)$ is negative for $\frac14 < w < \frac12$. Without the Bernstein test, its grid of resolution 3 has hexes with corner Jacobian $-\frac{4}{243}$.
- **The test is conservative.** A positive $\det Dg$ can still have a coefficient at most $0$. Then the code rejects the map, although subdividing the voxel might prove it valid.
- **Invalid labelings.** A labeling that does not describe a polycube makes the deformation fail. Check it before the deformation.
- **Flipped tetrahedra.** A deformation with flips gives a map that is not one to one, and then grid points land in the wrong place. Use a flip-free energy, or untangle the hex mesh afterwards.
- **Boundary hexes.** At a polycube edge the hexes of two faces meet at a right angle in the polycube but may meet at a flat angle on the solid. Add a padding layer.

## Implementations

## History

Tarini, Hormann, Cignoni and Montani defined polycube maps in 2004 to store textures on surfaces without seams. Gregson, Sheffer and Zhang used a volumetric polycube deformation for all-hex meshing in 2011, with a padding layer to fix the boundary hexes. In 2013 Livesu, Vining, Sheffer, Gregson and Scateni turned the choice of the labeling into a search under the graph conditions of Eppstein and Mumford. Later methods added flip-free energies and generalized polycubes.

## References
