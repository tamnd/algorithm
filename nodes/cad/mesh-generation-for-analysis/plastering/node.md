---
tag: ZETKKR
kind: algorithm
slug: plastering
name: Plastering
aliases:
- plastering hex meshing
area: cad/mesh-generation-for-analysis
level: advanced
summary: The 3D analogue of paving that advances layers of hexahedra inward from a quadrilateral boundary mesh, hard to close where the fronts meet.
solves: [hexahedral-mesh-generation]
model: real-ram
complexity:
  vars: {V: the number of front vertices, Q: the number of front quads}
  time: {worst: O(V + Q)}
  space: {extra: O(V + Q)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1993
  people: [Ted D. Blacker, R. J. Meyers]
  note: Blacker and Meyers described plastering, with its seams and wedges, in 1993. Staten, Owen, Blacker and others gave unconstrained plastering, which starts from the geometry and not from a fixed boundary quad mesh, from 2005 to 2010.
prereqs: [paving, hexahedral-mesh-generation, scaled-jacobian]
see_also: [advancing-front-mesh-generation, whisker-weaving, hexahedral-sweeping, hexahedral-mesh-existence-theorem, spatial-twist-continuum, mesh-untangling, boundary-layer-mesh-generation, octree-mesh-generation]
sources:
  - paper: "T. D. Blacker and R. J. Meyers, Seams and wedges in plastering, a 3D hexahedral mesh generation algorithm, Engineering with Computers 9(2), 1993, 83 to 93"
    locator: the advancing front of quads, the projection of hexes inward, and the seam and wedge operations where fronts meet (general locator)
  - paper: "Matthew L. Staten, Steven J. Owen and Ted D. Blacker, Unconstrained paving and plastering, a new idea for all hexahedral mesh generation, Proceedings of the 14th International Meshing Roundtable, 2005, 399 to 416"
    locator: layers that start from the geometry and leave the boundary mesh unconstrained (general locator)
  - paper: "Matthew L. Staten, Robert A. Kerr, Steven J. Owen, Ted D. Blacker, Marco Stupazzini and Kenji Shimada, Unconstrained plastering, hexahedral mesh generation via advancing-front geometry decomposition, International Journal for Numerical Methods in Engineering 81, 2010, 135 to 171"
    locator: the full unconstrained plastering method and the meshing of the remaining voids (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the section on advancing front methods, which states that there is no guarantee of a full hex mesh and that a void with an odd quad count needs backtracking
---

Plastering is the 3D form of [paving](/paving/). It starts from a closed quad mesh of the boundary, called the front, and builds hexahedra inward one layer at a time. Each new hex stands on a front quad, and its inner face becomes part of the new front. Where two parts of the front come close or meet at a sharp angle, plastering joins them with seams and wedges. The method ends when the front closes up, but this last step is the hard part: the void that remains often cannot be filled with good hexes, and sometimes not with hexes at all. This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it is a front method with no guarantee to close, while that page states the general problem and its limits. The code on this page implements one exact core step, one layer on a convex box.

## In plain words

Think of a plasterer who covers the inside walls of a room with a layer of plaster of even thickness. Each tile on a wall gets a brick of plaster behind it. In a corner, the bricks of two walls must meet along a slanted joint, so they fit without a gap.

When the first layer is done, the room is a bit smaller, and its new walls are the inner faces of the bricks. The plasterer can do the same again and again.

For a plain box room this works well. For a room with odd shapes, the layers from different walls run into each other at strange angles, and at the end a small hole is left in the middle. Often there is no good way to fill that hole with bricks, and the method fails.

## The problem

The input of plastering is a solid and a closed quad mesh of its boundary. The output is an all-hex mesh of the solid whose boundary quads are the given ones. A hex is valid if its trilinear map has $\det J > 0$ everywhere, as on the [scaled Jacobian](/scaled-jacobian/) page.

The code solves the core step for a convex axis-aligned box $\mathcal{B} = \prod_t [l_t, u_t]$ with a grid of breakpoints on each axis. The front is the boundary grid, with each quad counterclockwise seen from outside, and the step adds one layer of thickness $h$. The safe thickness is

$$g = \min_t \min\Big(\text{first spacing on axis } t,\ \text{last spacing on axis } t,\ \tfrac12 (u_t - l_t)\Big).$$

## The algorithm

Each front vertex $v$ moves inward by $h$ along each box face that contains it: $n_v$ is the sum of the outward unit normals of those faces. A vertex inside a face moves along one normal, a vertex on a box edge along two, and a box corner along three, which makes the slanted joints at the edges and corners.

```pseudo id=main
PLASTER-LAYER(P, Q, n, h)
L1  for each front vertex v do
L2      n_v ← the sum of the outward unit normals of the box faces that contain v
L3      v' ← v − h n_v
L4  H ← empty list
L5  for each front quad (a, b, c, d), counterclockwise seen from outside do
L6      append the hex (a', b', c', d', a, b, c, d) to H
L7  ok ← every hex of H has 8 positive corner Jacobians
L8  return H, the new front (the quads (a', b', c', d')), ok
```

Lines L1 to L3 place the new front. Lines L4 to L6 make one hex per front quad. The bottom of the hex is the offset quad and its top is the front quad, so the hex grows inward and its top face is counterclockwise seen from above, as the standard vertex order needs. Line L7 is the usual check of the corner Jacobians.

**The full method.** For a general solid, plastering repeats a loop of this kind, in words:

1. Choose front quads to advance, usually a whole row or layer at once, and compute inward directions at their vertices from the angles of the front.
2. Make new hexes on them, and project the new nodes so that the hexes have good shape.
3. Where the front makes a sharp angle, close it with a seam, which joins two front faces into one inner face of a hex. Where it makes a wide angle, add a wedge.
4. Find places where fronts come too close or cross, and join or trim them. A mixed mesh of the unmeshed region helps to find such contacts.
5. When the void that remains is small, fill it with a known pattern of a few hexes. If no pattern fits, back up and try again, or give up.

## Example

Take the box $[0, 4]^3$ with the breakpoints $0, 1, 3, 4$ on each axis, so each face has $3 \times 3$ quads. The front has $56$ vertices and $54$ quads, and $g = 1$. Take $h = 1/2$. The corner $(0, 0, 0)$ moves to $(1/2, 1/2, 1/2)$, the edge vertex $(1, 0, 0)$ to $(1, 1/2, 1/2)$, and the face vertex $(1, 1, 0)$ to $(1, 1, 1/2)$.

| hexes | how many | front quad | offset quad | corner Jacobians | volume |
|---|---|---|---|---|---|
| on a face center | 6 | $2 \times 2$ | $2 \times 2$ | all $2$ | $2$ |
| along a box edge | 24 | $1 \times 2$ | $1/2 \times 2$ | $1/2$ and $1$ | $3/4$ |
| at a box corner | 24 | $1 \times 1$ | $1/2 \times 1/2$ | $1/8$ and $1/2$ | $7/24$ |

The volumes add up to $12 + 18 + 7 = 37 = 4^3 - 3^3$, the volume of the shell between the box and the inner box $[1/2, 7/2]^3$. The new front is the boundary grid of the inner box with the breakpoints $1/2, 1, 3, 7/2$. A second layer with $h = 1/2$ leaves the box $[1, 3]^3$ with the breakpoints $1, 3$, which is one cell.

**A layer that passes the corner check but folds.** Take the one-cell box $[0, 4] \times [0, 2] \times [0, 6]$, where $g = 1$, and $h = 7/2$. Every offset width is negative: $4 - 7$, $2 - 7$ and $6 - 7$. The corner Jacobians are $h$ times a product of two widths, so all of them are positive and L7 returns true. But the inner box is turned inside out in all three directions, and the hexes overlap. With $h = 3/2$ only the width in $y$ is negative, and L7 returns false.

## Correctness

The proof below covers the core step. The offset of a vertex is a map $\mu$ that acts on each coordinate on its own. For a hex on a face with normal axis $a$ and in-plane axes $b$ and $c$, the trilinear map splits by coordinate, and

$$\det J(u, v, w) = h\,\big((1 - w)\Delta'_b + w\,\Delta_b\big)\big((1 - w)\Delta'_c + w\,\Delta_c\big),$$

where $\Delta$ are the side lengths of the front quad and $\Delta'$ those of the offset quad. So if $0 < h < g$, every hex is valid at every point, and the layer is a conforming mesh of the shell. If $h \ge g$, some offset width is at most zero and the layer is not a valid mesh of a shell, even when, as in the example, every corner Jacobian is positive.

What is proved and what is measured are different here. The proof covers only the box. For a general solid, plastering has no guarantee to close the last void, and the survey of Pietroni and others states that a void with an odd number of quads cannot be filled at all and needs backtracking. Plastering often fails to close the last void, and practical codes fall back to tetrahedra or pyramids there. The tests compare the corner check with a direct formula on 500 random boxes and thicknesses, and check conformity by face counts. On a sample of these boxes they also check that all Bernstein coefficients of $\det J$ are positive and that the volumes add up to the volume of the shell.

## Complexity

One layer visits each front vertex and each front quad once, so it takes $O(V + Q)$ time and space. For the grid box, $Q = 2(n_0 n_1 + n_1 n_2 + n_2 n_0)$. Each new layer of a box has the same quad count, and $k$ layers of thickness $h$ are valid exactly when $k h < g$, because each layer lowers $g$ by $h$. For a general solid, the cost of front contact tests and of backtracking dominates, and there is no useful bound on the number of tries.

## Properties

- **Good boundary hexes.** The first layers follow the boundary closely, with faces parallel to it. This is the main reason for plastering, as for boundary layers in flow problems.
- **Fixed boundary mesh.** The given boundary quads are kept, so a plastered volume can meet a neighbour volume with a matching mesh.
- **Same front size.** On a convex box, each layer leaves a front with the same number of quads, so the front does not shrink in count, only in size.
- **No closure guarantee.** The front may meet itself in a way that no hex pattern can close. The last void is often impossible to fill well.
- **Parity.** A void with an odd number of quads has no hex mesh at all, by the parity of the [hexahedral mesh existence theorem](/hexahedral-mesh-existence-theorem/).

## Variants and improvements

- **Seams and wedges.** Blacker and Meyers close sharp front angles by seams and fill wide angles by wedges.
- **Unconstrained plastering.** Staten and others start from the geometry, not from a boundary quad mesh. They advance whole layers until they meet, and only then fix the boundary mesh. The remaining voids are easier to fill, but the process can still fail.
- **Hybrid meshes.** Owen and Saigal keep a tetrahedral mesh of the unmeshed region during the advance, so front contacts are easy to find. The last void can stay as tetrahedra and pyramids, which gives a hex-dominant mesh.
- **Receding front.** Ruiz-Gironés, Roca and Sarrate grow a seed mesh outward and the boundary front inward, guided by distance fields, so the meeting surface is known in advance.

## When to use it

Use plastering, or one of its unconstrained or hybrid forms, when good hexes near the boundary matter most and a few non-hex elements in the middle are acceptable. For a solid with a sweep direction, [sweeping](/hexahedral-sweeping/) is simpler and safer. For a strict all-hex mesh of a general solid, [polycube](/polycube-hex-meshing/) and [frame field](/frame-field-hex-meshing/) methods are the research choices, and none of them is guaranteed either.

## Pitfalls

- **Closing the last void.** This is the main failure. Check the parity of the void first, and plan a fallback, such as a few tetrahedra or a pillow layer.
- **Corner checks are not enough.** The example shows a layer with all corner Jacobians positive that overlaps itself. Check the new front against the old one, not only each hex.
- **Front collisions.** Two parts of the front that grow toward each other can cross. Test for contacts after each layer.
- **Thickness too large.** On a box, a layer thicker than the safe value $g$ folds. On a general solid, the safe thickness changes along the front and must be found locally.

## Implementations

## History

Paving, the 2D method of Blacker and Stephenson, appeared in 1991. Plastering, its 3D form, was described by Blacker and Meyers in 1993, with seams and wedges to close the front. It showed that the 3D closure problem is much harder than in 2D, and Mitchell's work on the [existence theorem](/hexahedral-mesh-existence-theorem/) explained part of the reason: a void can be closed by hexes only if its quad count is even, and even then the hexes may have to be bad. From 2005 to 2010 Staten, Owen, Blacker and others gave unconstrained plastering, which defers the boundary mesh until the layers meet.

## References
