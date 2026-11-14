---
tag: VPGPRK
kind: theorem
slug: euler-poincare-formula
name: Euler-Poincare formula for solids
aliases:
- Euler-Poincare formula
area: cad/solid-modeling
level: core
summary: For a manifold solid with faces that are disks with holes, V - E + F - (L - F) - 2(S - H) = 0, where L counts loops, S shells and H holes (the total genus).
prereqs: [euler-formula, boundary-representation, graph-genus]
see_also: [euler-operators, manifold-solid, convex-polytope, polygon-mesh, winged-edge-data-structure, radial-edge-data-structure]
sources:
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Section 3.5.6, Euler characteristic (p. 43), Section 3.5.7, Surfaces with boundary (p. 46), and Section 9.4.1 (p. 154)
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapter 3 (the classification of surfaces and the Euler characteristic 2 - 2g of a cellular embedding in the orientable surface of genus g)
  - paper: "Ian C. Braid, R. C. Hillyard and Ian A. Stroud, Stepwise construction of polyhedra in geometric modelling, in K. W. Brodlie (ed.), Mathematical Methods in Computer Graphics and Design, Academic Press, 1980, 123 to 141"
    locator: the counts of a boundary model with loops, shells and holes, and the operators that keep the formula
  - paper: "Leonhard Euler, Elementa doctrinae solidorum, Novi Commentarii Academiae Scientiarum Petropolitanae 4 (1752/53), published 1758"
    locator: the relation V - E + F = 2 for polyhedra
---

The Euler-Poincaré formula for solids is a relation between the numbers of cells of the boundary of a [manifold solid](/manifold-solid/): $V - E + F - (L - F) - 2(S - H) = 0$. Here $V$, $E$ and $F$ count the vertices, edges and faces, $L$ counts the loops (the boundary cycles of the faces), $S$ counts the shells and $H$ counts the holes through the solid. It extends [Euler's formula](/euler-formula/) $V - E + F = 2$ to faces with holes, to solids with cavities and to solids with tunnels. [Boundary representations](/boundary-representation/) use it to compute the number of holes and as a quick check, and the [Euler operators](/euler-operators/) are the steps that keep it true. It is a necessary condition for a valid boundary model, not a sufficient one.

## Statement

Let $Q$ be a [manifold solid](/manifold-solid/) whose boundary $\partial Q$ is split into $V$ vertices (points), $E$ edges and $F$ faces, with these conditions:

1. Each edge is an open arc whose two ends are vertices (the two ends may be the same vertex).
2. Each face is a connected open subset of $\partial Q$ that is homeomorphic to an open disk with $k_f \ge 0$ disjoint closed disks removed. Its boundary is made of $k_f + 1$ *loops*, and each loop is a closed walk of edges, or a single vertex with no edge.
3. The vertices, the edges and the faces are disjoint, and together they make up $\partial Q$.

Let $L = \sum_f (k_f + 1)$ be the number of loops, so that $R = L - F$ is the number of *rings* (the inner loops of the faces), let $S$ be the number of connected components of $\partial Q$ (the shells), and let $H$ be the sum of the genera of the shells (the holes, or the *genus* of the solid). Then

$$V - E + F - (L - F) - 2(S - H) = 0,$$

or, in the other common form,

$$V - E + F - R = 2(S - H).$$

For a solid with one shell, no holes and faces without rings, this is $V - E + F = 2$. The orientation convention of the solid modeling pages is the right-hand rule: the outer loop of a face runs counterclockwise seen from outside. The formula does not depend on orientation, but the boundary of a solid in $E^3$ is always orientable, and the proof uses this.

## In plain words

Count the corners, the edges and the faces of a solid. For a box, a pyramid or any solid like a ball, corners minus edges plus faces is always two. Each tunnel through the solid lowers this number by two. Each empty bubble inside the solid adds a second skin, and each skin adds two. A face with a hole in it, like the top of a ring-shaped block, adds one extra boundary cycle, and the formula subtracts one for each such cycle.

So the formula does not say that the shape is a real solid. It says only that the counts agree with a skin that has the given number of parts and tunnels.

## Proof

The proof has three steps: split by shells, remove the rings, and use the Euler characteristic of a closed surface.

**Step 1: shells.** Each vertex, edge and face lies in exactly one shell, because a face and an edge are connected sets and the shells are the components of $\partial Q$. So $V$, $E$, $F$ and $L$ are sums over the shells, and $H$ is a sum by definition. It is enough to prove that a shell $\Sigma$ of genus $g$ satisfies $V - E + F - R = 2 - 2g$ for its own counts, and to add these $S$ equations.

**Step 2: rings.** Take a face $f$ with $k_f \ge 1$. The face is connected, so there is a simple arc inside $f$ from a vertex of one ring to a vertex of another loop of $f$, whose inner points lie in $f$. Add this arc as a new edge. The two loops that it joins become one loop, which goes along the first loop, across the new edge, along the second loop and back across the new edge. The face is now homeomorphic to an open disk with $k_f - 1$ closed disks removed. The count changes are $E \to E + 1$ and $L \to L - 1$, with $V$ and $F$ unchanged, so $V - E + F - (L - F)$ does not change. Repeat until no face has a ring. Then each face is an open disk, its boundary is one closed walk of edges or one vertex, and $R = 0$.

**Step 3: closed surfaces.** Now the vertices, edges and faces of $\Sigma$ form a cell decomposition: points, open arcs and open disks. A shell is a connected closed surface in $E^3$, so it is orientable, and by the classification of surfaces it is the sphere with $g$ handles for its genus $g$. The number $V - E + F$ of any cell decomposition of a surface is its Euler characteristic, which does not depend on the decomposition, and for the orientable surface of genus $g$ it is $2 - 2g$ (Mohar and Thomassen, Chapter 3; see [graph genus](/graph-genus/)). For $g = 0$ and a decomposition with at least one edge, this is Euler's formula for the plane graph that one gets by removing a point of a face. So $V - E + F = 2 - 2g$ after step 2, and $V - E + F - R = 2 - 2g$ before it.

Adding over the shells gives $V - E + F - R = 2S - 2H$, which is the statement. $\square$

**Checks.** The examples below were computed with a short script, and the first five also by the B-rep check of the [boundary representation](/boundary-representation/) page.

| solid | $V$ | $E$ | $F$ | $L$ | $S$ | $H$ | $V - E + F - (L - F) - 2(S - H)$ |
|---|---|---|---|---|---|---|---|
| cube | 8 | 12 | 6 | 6 | 1 | 0 | $8 - 12 + 6 - 0 - 2(1 - 0) = 0$ |
| square frame $[0,3]^2 \times [0,1]$ with the hole $(1,2)^2 \times [0,1]$ | 16 | 24 | 10 | 12 | 1 | 1 | $16 - 24 + 10 - 2 - 2(1 - 1) = 0$ |
| plate with two holes $[0,5] \times [0,3] \times [0,1]$ | 24 | 36 | 14 | 18 | 1 | 2 | $24 - 36 + 14 - 4 - 2(1 - 2) = 0$ |
| cube $[0,3]^3$ with the cavity $(1,2)^3$ | 16 | 24 | 12 | 12 | 2 | 0 | $16 - 24 + 12 - 0 - 2(2 - 0) = 0$ |
| plate $[0,4]^2 \times [0,1]$ with a block on top | 16 | 24 | 11 | 12 | 1 | 0 | $16 - 24 + 11 - 1 - 2(1 - 0) = 0$ |
| solid cylinder: 2 circle edges, top, bottom and side | 2 | 2 | 3 | 4 | 1 | 0 | $2 - 2 + 3 - 1 - 2(1 - 0) = 0$ |
| one vertex and one face (the first step of the Euler operators) | 1 | 0 | 1 | 1 | 1 | 0 | $1 - 0 + 1 - 0 - 2(1 - 0) = 0$ |

In the square frame, the top and bottom faces are square rings, each with one ring loop. If each of them is cut by one bridge edge, as in step 2, the counts become $V = 16$, $E = 26$, $F = 10$, $L = 10$, and $16 - 26 + 10 - 0 - 0 = 0$ again. If each is cut into four trapezoids, they become $V = 16$, $E = 32$, $F = 16$, $L = 16$, and $16 - 32 + 16 = 0$. In the cylinder, each circle edge has one vertex on it, and the side face is an annulus, a disk with one hole, so it has two loops. In the last row, the face is the sphere minus one point, an open disk, and its only loop is the vertex.

## Consequences

- **The genus from the counts.** A boundary model stores $V$, $E$, $F$, $L$ and $S$ but not $H$. The formula gives $H = S - (V - E + F - R)/2$, and the check that this is a whole number with each shell of genus at least 0 is a cheap test of the topology. The validity check of the [boundary representation](/boundary-representation/) page does this per shell.
- **Five basic changes.** The integer vectors $(V, E, F, L, S, H)$ that satisfy the formula form a lattice of rank 5 in $\mathbb{Z}^6$, because the formula is one linear equation $c \cdot x = 0$ with $c = (1, -1, 2, -1, -2, 2)$. The [Euler operators](/euler-operators/) MVSF, MEV, MEF, KEMR and KFMRH change the counts by $(1, 0, 1, 1, 1, 0)$, $(1, 1, 0, 0, 0, 0)$, $(0, 1, 1, 1, 0, 0)$, $(0, -1, 0, 1, 0, 0)$ and $(0, 0, -1, 0, 0, 1)$. Each is a solution, and the six $5 \times 5$ minors of these five rows, leaving out the columns $V$, $E$, $F$, $L$, $S$, $H$ in turn, are $\pm 1, \pm 1, \pm 2, \pm 1, \pm 2, \pm 2$, with greatest common divisor 1. So the five vectors are a basis of the lattice: every vector of counts that satisfies the formula is an integer combination of them. This is only the count side. That the operators also reach every valid topology is a separate theorem of Mäntylä (1984).
- **Convex polytopes and meshes.** For a [convex polytope](/convex-polytope/) in $E^3$, $S = 1$, $H = 0$ and $R = 0$, so $V - E + F = 2$, which is [Euler's formula](/euler-formula/) for the plane graph of the polytope. For a closed [polygon mesh](/polygon-mesh/) of genus $g$ with disk faces, $V - E + F = 2 - 2g$, and for a mesh with $b$ border loops $\chi = 2 - 2g - b$; the [graph genus](/graph-genus/) page gives the same relation for cellular embeddings of graphs.
- **The solid itself.** For a compact 3-manifold $Q$ with boundary, $\chi(\partial Q) = 2\chi(Q)$. So a decomposition of the solid into $C$ cells of dimension 3, such as the unit cubes of a [voxel set](/spatial-occupancy-enumeration/), gives $V - E + F - C = \chi(Q) = S - H$ for the counts of the whole complex. A single cube as one 3-cell has $8 - 12 + 6 - 1 = 1 = S - H$. The tests of the boundary representation page use this to check the number of holes of random voxel solids independently.
- **Cell complexes in general.** For any finite cell complex, the alternating sum of the numbers of cells of each dimension equals the alternating sum of its Betti numbers. That theorem of Poincaré is the general result, and the formula of this page is its case for the boundary surface of a solid, written with the counts that B-rep data structures store.

## Tightness

**Each hypothesis is needed.** Each example breaks one condition, and the formula fails.

- **Rings not counted.** The square frame with each square ring face counted as one loop gives $L = 10$ and $16 - 24 + 10 - 0 - 0 = 2 \ne 0$. The solid cylinder with the side face counted as one loop gives $2 - 2 + 3 - 0 - 2 = 1$.
- **A face that is not a disk with holes.** The boundary of a solid torus as one face, with one vertex as its loop, has $V = 1$, $E = 0$, $F = 1$, $L = 1$, $S = 1$, $H = 1$, and $1 - 0 + 1 - 0 - 0 = 2 \ne 0$. The face is a torus minus a point, which has genus 1, so condition 2 fails.
- **A boundary that is not a manifold.** Two cubes that share a vertex have $V = 15$, $E = 24$, $F = 12$, $L = 12$, and one connected boundary. With $S = 1$, $H = 0$ the sum is $15 - 24 + 12 - 0 - 2 = 1$, and with $S = 2$ it is $-1$; no choice of the counts gives 0. Two cubes that share an edge have $V = 14$, $E = 23$, $F = 12$ and give $14 - 23 + 12 - 2 = 1$. Non-manifold solids need a different count, which is one reason for the [radial edge data structure](/radial-edge-data-structure/).

**The converse is false.** The formula is necessary for a valid model, not sufficient.

- A cube with one extra edge from a corner to a new vertex outside the cube has $V = 9$, $E = 13$, $F = 6$, $L = 6$, $S = 1$, $H = 0$, and $9 - 13 + 6 - 0 - 2 = 0$. As counts, this is a cube with an edge drawn inside one face from a corner to a new point of that face, which is a valid model. With the new vertex outside the cube, the wire edge is not on the boundary of any solid. Only the geometry can tell the two apart.
- A tetrahedron in which one face lists its vertices in the wrong order has the counts $4 - 6 + 4 - 0 - 2 = 0$ of a valid tetrahedron, but its orientation is not consistent.
- Any vector of counts that satisfies the equation, for example $V = 10$, $E = 15$, $F = 7$, $L = 7$, $S = 1$, $H = 0$ (a pentagonal prism), passes the test, whatever faces are stored. The test does not look at the faces.

## History

Euler stated $V - E + F = 2$ for polyhedra in 1752 and published a proof in 1758. In 1813, L'Huilier pointed out polyhedra for which it fails, such as a solid with a tunnel and a solid with a face that has a hole, and gave corrections for them. Poincaré proved the general relation between the numbers of cells and the Betti numbers of a complex in his papers on analysis situs from 1895 on. In solid modeling, Baumgart used Euler's relation to define the first Euler operators in 1975, and Braid, Hillyard and Stroud wrote the formula with loops, shells and holes for the BUILD modeler in 1980. Mäntylä's book of 1988 states it in the form $V - E + F - (L - F) - 2(S - H) = 0$ that this page uses.

## References
