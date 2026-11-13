---
tag: 23HY3M
kind: technique
slug: euler-operators
name: Euler operators
aliases:
- Euler-Poincare operators
- Euler ops
area: cad/solid-modeling
level: core
summary: Local steps such as make edge and vertex or kill face, make ring and hole that edit a B-rep and keep the Euler-Poincare formula and a valid topology, but not a valid geometry.
prereqs: [boundary-representation, euler-poincare-formula]
see_also: [manifold-solid, winged-edge-data-structure, radial-edge-data-structure, doubly-connected-edge-list, euler-formula, mesh-simplification, solid-boolean-operations, graph-genus]
sources:
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Chapter 9 (p. 139), with Sections 9.1.3 (p. 145), 9.2.2 (p. 148), 9.2.4 (p. 151), 9.3 (p. 152), 9.4.1 (p. 154) and 9.4.3 (p. 158); Chapter 11 (p. 175) for the low-level operators of GWB
  - paper: doi:10.1109/MCG.1982.1674396
    title: Martti Mäntylä and Reijo Sulonen, GWB, a solid modeler with Euler operators, IEEE Computer Graphics and Applications 2(7), 1982, 17 to 31
    locator: the operators of GWB and their use for sweeps and gluing
  - paper: doi:10.1016/0734-189X(84)90129-4
    title: Martti Mäntylä, A note on the modeling space of Euler operators, Computer Vision, Graphics, and Image Processing 26(1), 1984, 45 to 60
    locator: the proof that the operators reach every valid topology and only valid ones
  - paper: doi:10.1145/1499949.1500071
    title: Bruce G. Baumgart, A polyhedron representation for computer vision, AFIPS National Computer Conference 44, 1975, 589 to 596
    locator: the winged-edge structure and its Euler primitives
  - paper: "Ian C. Braid, R. C. Hillyard and Ian A. Stroud, Stepwise construction of polyhedra in geometric modelling, in K. W. Brodlie (ed.), Mathematical Methods in Computer Graphics and Design, Academic Press, 1980, 123 to 141"
    locator: the operators of the BUILD modeler, with loops and holes counted
---

Euler operators are the small steps with which a solid modeler builds and edits a [boundary representation](/boundary-representation/). Each step adds or removes a few cells together, for example one edge and one vertex (MEV), or one edge and one face (MEF), and the cells change so that the [Euler-Poincaré formula for solids](/euler-poincare-formula/) $V - E + F - (L - F) - 2(S - H) = 0$ stays true. More than that, each step changes a valid surface into a valid surface: a closed, oriented 2-manifold whose faces are disks with holes. So a modeler that changes its boundary model only through Euler operators never has a broken topology. It can still have a broken geometry, such as faces that cross, because the operators do not look at the coordinates. Baumgart introduced the idea in 1975, Braid, Hillyard and Stroud wrote the operators with rings and holes in 1980, and Mäntylä built the GWB modeler on them and proved in 1984 that they reach every valid topology.

This page is the technique. The formula itself, with its proof and the conditions it needs, is on the page of the [Euler-Poincaré formula for solids](/euler-poincare-formula/), and the planar case $V - E + F = 2$ for connected plane graphs is [Euler's formula](/euler-formula/). The formula says which counts are possible. The operators are a way to move between models with possible counts, one valid model at each step.

The counts are $V$ vertices, $E$ edges, $F$ faces, $L$ loops (the boundary cycles of the faces, so $R = L - F$ is the number of rings, the inner loops), $S$ shells and $H$ holes (the total genus). The orientation is the right-hand rule: seen from outside the solid, the outer loop of a face runs counterclockwise and its rings run clockwise.

## In plain words

Think of the surface of a solid as a map drawn on a rubber skin. You may change the map only with a few allowed moves. Draw a new line from a point to a new point. Draw a line across a country from one border to another, so that it splits into two countries. Rub out a line that has the same country on both sides, so that the country gets a hole in it. Glue two countries together through the inside of the solid, which makes a tunnel.

Each move changes the numbers of points, lines and countries in a fixed way, and the skin is never torn. Each move has an undo move. The moves do not know where the points are, so they cannot stop you from moving a point to a bad place.

## When it applies

- The model is a boundary representation of a [manifold solid](/manifold-solid/): each shell is a closed, orientable surface, and each face is a disk with holes. A half-edge structure, the [winged-edge structure](/winged-edge-data-structure/) or a [doubly connected edge list](/doubly-connected-edge-list/) with loops can store it.
- You want every program that changes the model to keep it valid by construction, instead of a full check after each change. Sweeps, gluing, Boolean operations and local edits of a B-rep modeler are made of Euler operators.
- You want a log of changes that can be undone. Each operator has an inverse with the opposite counts.
- It does not apply as it is to non-manifold models, such as two cubes that share an edge, or to faces with dangling sheets. Those need the operators of a non-manifold structure such as the [radial edge data structure](/radial-edge-data-structure/).

## The template

A model is a set of shells. A face has one outer loop and a list of rings. A loop is a cycle of half-edges, each with an origin vertex, and $next$ and $prev$ give the cycle. A loop that is a single vertex has one *lone* half-edge with no edge. An edge has two half-edges in opposite directions, and $twin(h)$ is the other half-edge of the edge of $h$. A *corner* of a vertex $v$ in a loop is a pair $(prev[h], h)$ with $origin[h] = v$. The operator takes half-edges as arguments, because a vertex can have several corners in one loop.

```pseudo id=main
MVSF(p)                              ▷ make vertex, shell and face
L1  create vertex v at p, a face f, and its outer loop (h), with h a lone half-edge at v

MEV(h, p)                            ▷ make edge and vertex, in the corner of v = origin[h] before h
L2  create vertex w at p and an edge with half-edges a: v → w and b: w → v
L3  if h is lone then the loop of h becomes (a, b) else link prev[h] → a → b → h

MEF(h1, h2)                          ▷ make edge and face; h1 and h2 are in one loop ℓ
L4  X ← (h1, next[h1], …, prev[h2]), empty if h1 = h2; Y ← the other half-edges of ℓ, from h2
L5  create an edge with a: origin[h1] → origin[h2] and b: origin[h2] → origin[h1]
L6  ℓ ← Y followed by a; create a face f′ whose outer loop is X followed by b

KEMR(a)                              ▷ kill edge, make ring; a and b = twin(a) are in one loop (a, X, b, Y)
L7  the loop becomes Y, a new ring of the same face becomes X, and the edge is deleted

KFMRH(f1, f2)                        ▷ kill face, make ring and hole; f1 ≠ f2, and f2 has one loop
L8  same ← (f1 and f2 are in one shell)
L9  the loop of f2 becomes a ring of f1, and f2 is deleted
L10 if same then H ← H + 1           ▷ otherwise two shells became one
```

In lines L3, L6 and L7, an empty sequence of half-edges means a lone half-edge at the right vertex: in line L7, an empty $X$ is a lone half-edge at $origin[b]$ and an empty $Y$ one at $origin[a]$. The inverses are KVSF, KEV, KEF, MEKR and MFKRH. KEV$(a)$ needs $next[a] = twin(a)$, so that the far vertex has no other edge, and removes $a$, $twin(a)$ and that vertex. KEF$(a)$ needs two different faces on the two sides of the edge, joins the two loops, and deletes the face of $twin(a)$, whose other loops become rings of the face of $a$. MEKR$(h_1, h_2)$ joins two loops of one face by a new edge into the loop $(a, \text{loop of } h_2, b, \text{loop of } h_1)$. MFKRH$(\ell)$ makes the ring $\ell$ the outer loop of a new face, and $H$ goes down by 1 unless this splits the shell. The changes of the counts are these:

| operator | $\Delta V$ | $\Delta E$ | $\Delta F$ | $\Delta L$ | $\Delta S$ | $\Delta H$ | inverse |
|---|---|---|---|---|---|---|---|
| MVSF | +1 | 0 | +1 | +1 | +1 | 0 | KVSF |
| MEV | +1 | +1 | 0 | 0 | 0 | 0 | KEV |
| MEF | 0 | +1 | +1 | +1 | 0 | 0 | KEF |
| KEMR | 0 | -1 | 0 | +1 | 0 | 0 | MEKR |
| KFMRH, one shell | 0 | 0 | -1 | 0 | 0 | +1 | MFKRH |
| KFMRH, two shells | 0 | 0 | -1 | 0 | -1 | 0 | MFKRH |

Put each row into $\Delta V - \Delta E + 2 \Delta F - \Delta L - 2 \Delta S + 2 \Delta H$, the change of the left side of the formula: every row gives 0. KEMR keeps $F$ and adds a loop, so it adds a ring; KFMRH removes a face and keeps its loop, so it also adds a ring. The first five rows are a basis of the integer solutions of the formula, as the theorem page shows, so any change of counts that keeps the formula is a sum of operator steps.

### Why each step gives a valid surface

Assume that the model before the step is valid: each shell is a closed, oriented surface, and the cells cut it into vertices, open arcs and faces that are open disks with holes, with the loops as boundaries. Each claim below is about the surface of one shell.

- **MVSF** makes a new shell: a sphere cut into one point and the open disk that is the rest. The disk has one loop, the vertex.
- **MEV** draws an arc inside the face $f$ of $h$, from $v$ into the face, through the corner before $h$, to a new point $w$ inside $f$. The face minus a simple arc that touches its boundary at one end is still a disk with the same number of holes. Its loop now goes out along $a$ and back along $b$.
- **MEF** draws an arc inside $f$ from the corner before $h_1$ to the corner before $h_2$, both on the loop $\ell$. A face is planar (a disk with holes), so an arc with both ends on one boundary loop cuts it into two parts. One part is bounded by $X$ and $b$, and the operator makes it the new face. The other part keeps $Y$, $a$ and the other loops. Each part is again a disk with holes. If $h_1 = h_2$, the arc is closed at $v$ and cuts off a disk bounded by the one edge $b$.
- **KEMR** removes an edge with the same loop on both sides. If $f$ has $k$ holes and its loop runs along $e$ twice, then $f \cup e$ is connected, orientable, has $k + 2$ boundary loops, and has compact Euler characteristic $(1 - k) - 1 = -k$. A surface of genus $g$ with $b$ boundary loops has $2 - 2g - b = -k$, so $g = 0$: the new face is again a disk with holes, now $k + 1$ of them.
- **KFMRH** removes the disk $f_2$ and a small disk inside $f_1$, and joins the two circles by a tube. This adds a handle if $f_1$ and $f_2$ are in one shell (the genus grows by 1), and it joins two shells into one otherwise (the connected sum). In both cases the result is a closed, oriented surface, and $f_1$ is a disk with one more hole.
- **The inverses** undo these changes, and their preconditions are exactly what makes the undo a valid surface. The checks in KEV and KEF ask that the far vertex has degree 1 and that the edge has two different faces. KEMR asks for one loop on both sides of the edge. MEKR asks for two loops of one face.

Each new edge gets two half-edges in opposite directions, and each loop that the operators build keeps the order of the old half-edges, so the orientation stays consistent. Mäntylä (1984) proved the converse: every valid topology of this kind, with any number of shells and holes, is reached from nothing by a finite sequence of these operators. The operators are therefore enough to build any manifold solid model.

### Cost

MVSF, MEV and KEV change $O(1)$ pointers. MEF, KEF, KEMR and MEKR set the loop pointer of each half-edge that changes loop, so they take $O(k)$ time for loops of $k$ half-edges in total. KFMRH and MFKRH move one loop in $O(1)$ time, plus a search of the shell in $O(n)$ time to decide whether $H$ or $S$ changes. A modeler that does not store $H$ can skip the search and get $H$ from the counts when it needs it.

## Classic examples

**A cube.** The sequence MVSF, 3 MEV, MEF, 4 MEV, 4 MEF builds the unit cube. The implementation of this page builds it like this, and the counts after each group of steps are these:

| step | the operator does | $V$ | $E$ | $F$ | $L$ | $S$ | $H$ |
|---|---|---|---|---|---|---|---|
| MVSF | vertex 0 and one face | 1 | 0 | 1 | 1 | 1 | 0 |
| 3 MEV | the path 0, 1, 2, 3 of the bottom | 4 | 3 | 1 | 1 | 1 | 0 |
| MEF | closes the bottom square with the edge from 3 to 0 | 4 | 4 | 2 | 2 | 1 | 0 |
| 4 MEV | the vertical edges up to 4, 5, 6, 7 | 8 | 8 | 2 | 2 | 1 | 0 |
| 4 MEF | the top edges, which cut off the 4 sides | 8 | 12 | 6 | 6 | 1 | 0 |

In the MEF that closes the bottom, $h_1$ is the half-edge from 3 to 2 and $h_2$ is the half-edge from 0 to 1. Then $X$ is the half-edges from 3 to 2, 2 to 1 and 1 to 0, and the new face has the loop 3, 2, 1, 0: the bottom, which runs clockwise seen from above, so its outward normal points down. The old face keeps 0, 1, 2, 3 and becomes the top later. The test checks that the 6 faces have the right corners, that each face is planar, and that the signed volume is exactly 1.

**A cube with a through-hole.** Take the box $[0, 3]^2 \times [0, 1]$ from the 13 steps above. Then:

1. MEV from the top corner $(0, 0, 1)$ to $(1, 1, 1)$, the bridge, and 3 MEV to $(2, 1, 1)$, $(2, 2, 1)$ and $(1, 2, 1)$.
2. MEF closes the inner square. This makes the inner square face, and the top loop goes around the outer square, along the bridge, around the inner square and back. Now $V = 12$, $E = 17$, $F = 7$, $L = 7$.
3. KEMR on the bridge. The inner square becomes a ring of the top face: $E = 16$, $L = 8$, so $R = 1$.
4. 4 MEV from the corners of the inner square face down to $z = 0$, and 4 MEF that cut off the 4 walls of the hole. The inner square face is now at the bottom of a well: $V = 16$, $E = 24$, $F = 11$, $L = 12$, $S = 1$, $H = 0$.
5. KFMRH with the bottom face as $f_1$ and the bottom of the well as $f_2$. They are in one shell, so the hole opens: $F = 10$, $L = 12$, $H = 1$.

The result is the square frame of the theorem page, $16 - 24 + 10 - 2 - 2(1 - 1) = 0$, with volume exactly 8 in the test. The state before the last step has the same counts as a plate with a block on top: both are spheres with one ring face, so no count can tell them apart.

**A cube with a cavity.** Build a second box with MVSF and the same 12 steps, but with an orientation that points into the cavity. This is a second shell: $V = 16$, $E = 24$, $F = 12$, $L = 12$, $S = 2$, $H = 0$, and the signed volume of $[0, 3]^3$ minus $(1, 2)^3$ is 26.

**The smallest cases.** MVSF and then MEF with $h_1 = h_2$ the lone half-edge give a sphere cut by one closed edge into two disks: $V = 1$, $E = 1$, $F = 2$, $L = 2$. MVSF twice and then KFMRH move the second vertex into the face of the first shell as a ring: $V = 2$, $E = 0$, $F = 1$, $L = 2$, $S = 1$, and $2 - 0 + 1 - 1 - 2 = 0$.

**Edits of triangle meshes.** The edge collapse of [mesh simplification](/mesh-simplification/) removes 1 vertex, 3 edges and 2 faces from a closed triangle mesh. This is KEF twice, for the two triangles of the edge, and then KEV: $(0, -1, -1, -1) + (0, -1, -1, -1) + (-1, -1, 0, 0) = (-1, -3, -2, -2)$. An edge flip is KEF followed by MEF, and it keeps all counts.

**Sweeps and gluing.** To extrude a face with $n$ edges, do MEV at each of its $n$ vertices and then $n$ MEF: the counts change by $(n, 2n, n, n, 0, 0)$. To glue two solids along two equal faces, a modeler can use KFMRH to join the two shells through the two faces, and then remove the double edges and vertices of the seam with KEF and KEV.

## Variations

- **Other operator sets.** Baumgart's Euler primitives (1975) act on the winged-edge structure. Braid, Hillyard and Stroud (1980) wrote their operators for the BUILD modeler with loops and holes in the counts. Mäntylä names the first operator MVFS, make vertex, face and solid, because a solid in GWB starts with one shell. This page writes MVSF, with S for the new shell. Any five operators whose change vectors are a basis of the solutions work as well.
- **A more general MEV.** In GWB the low-level MEV takes two half-edges at the same vertex, and it splits the vertex: the edges between the two corners move to the new vertex, and the new edge joins the two. The MEV of this page is the case in which the two half-edges are the same.
- **High-level operators.** A modeler offers sweeps, gluing, chamfers and Booleans as sequences of the basic ones. Then the result of any program stays a valid surface, and the log of basic steps makes undo simple.
- **Non-manifold operators.** For wire edges, faces that touch along an edge and solids that touch at a vertex, the counts and the operators change, and they act on a structure such as the [radial edge data structure](/radial-edge-data-structure/).

## Pitfalls

- **A valid topology is not a valid solid.** The operators keep the surface a closed, oriented 2-manifold with disk faces, but they do not look at the points. A MEV can put the new vertex outside the face, a MEF can join two points by a curve that leaves the face, and a sequence can give faces that cross. A modeler must check the geometry, or build only by steps that are geometrically safe, such as sweeps. (The stub of this page said that every result is valid; that is true only for the topology.)
- **The formula is not the check.** The formula holds after every operator, but a model can satisfy the formula without being built by valid steps. Building by operators gives validity; checking the counts does not.
- **Which side is the new face.** MEF splits the loop at two corners, and which part goes to the new face is a convention. The half-edges $h_1, \ldots, prev[h_2]$ go to the new face here. A wrong choice gives the right topology but the wrong face for later steps, for example the bottom of a cube where the top should be.
- **Outer loop and ring.** The topology does not know which loop of a face is the outer one. KEMR and MFKRH need the caller to decide this from the geometry.
- **Lone half-edges.** A loop that is a single vertex has no edge. MEV and MEF on such a loop, and KEV, KEF and KEMR that empty a loop, must make or remove the lone half-edge, or the vertex is lost.
- **KFMRH between shells.** If the two faces are in different shells, the genus does not grow; the two shells become one. Code that always adds 1 to $H$ gets wrong counts.

## Exercises

1. Give a sequence of Euler operators that builds a tetrahedron, and list the counts after each step.
2. Show that every row of the table keeps $V - E + F - (L - F) - 2(S - H)$, and check that MVSF, MEV, MEF, KEMR and KFMRH in one shell have linearly independent change vectors.
3. Write a sequence that builds a solid with two through-holes, the plate $[0, 5] \times [0, 3] \times [0, 1]$ with holes over $(1, 2) \times (1, 2)$ and $(3, 4) \times (1, 2)$. Check that it ends with $V = 24$, $E = 36$, $F = 14$, $L = 18$, $H = 2$.
4. Show that the edge flip of a triangle mesh is KEF followed by MEF, and say which half-edges the MEF takes.
5. Why is KEF not allowed for an edge that has the same face on both sides, but in two different loops of that face? What would removing the edge do to the surface?

## References
