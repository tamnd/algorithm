---
tag: 9YH36K
kind: technique
slug: direct-modeling
name: Direct modeling
aliases:
- history-free modeling
- explicit modeling
area: cad/solid-modeling
level: core
summary: Edits a B-rep by moving, offsetting or deleting faces and rebuilding the neighbouring faces and blends, with no feature history, by local operations and face intersection.
prereqs: [boundary-representation, surface-surface-intersection, solid-boolean-operations]
see_also: [feature-based-modeling, persistent-naming-problem, generic-naming-scheme, solid-offsetting, rolling-ball-blend, euler-operators, feature-recognition, sweep-representation]
sources:
  - paper: doi:10.1016/j.advengsoft.2018.10.003
    title: Qiang Zou and Hsi-Yung Feng, Push-pull direct modeling of solid CAD models, Advances in Engineering Software 127, 59 to 69, 2019
    locator: Section 3 (regeneration by intersecting the moved surfaces, and the two failure types, a lost connection and a new one), Section 4 (topology change points, and the update M(t_{i+1}) = M(t_i) minus the swept volume by a regularized Boolean), Section 6 (comparison with five commercial packages)
  - paper: "Jarek R. Rossignac, Issues on feature-based editing and interrogation of solid models, Computers and Graphics 14, 149 to 172, 1990"
    locator: editing a solid by moving faces, and the reading of a face translation as the extrusion of a feature
  - paper: "Markus Lipp, Peter Wonka and Pascal Müller, PushPull++, ACM Transactions on Graphics 33, 2014"
    locator: push-pull of the faces of polygonal models with planar faces, with rules for inserting and removing faces when the neighbours cannot follow
  - paper: "Vadim Shapiro and Donald L. Vossler, What is a parametric family of solids?, Proceedings of the Third ACM Symposium on Solid Modeling and Applications, 43 to 54, 1995"
    locator: why the same parameter change can give different solids in different systems, which is the ambiguity that direct edits also face
  - paper: "A. R. Grayer, Alternative approaches in geometric modelling, Computer-Aided Design 12, 189 to 192, 1980"
    locator: cited by Zou and Feng for the tweaking operations of early modelers, which moved faces without changing the topology
  - paper: "Y. Woo and S. H. Lee, Volumetric modification of solid CAD models independent of design features, Advances in Engineering Software 37, 826 to 835, 2006"
    locator: a push of faces read as a change of the volume of a feature, as cited by Zou and Feng
  - paper: "B. C. Kim and D. Mun, Stepwise volume decomposition for the modification of B-rep models, International Journal of Advanced Manufacturing Technology 75, 1393 to 1403, 2014"
    locator: modification of a B-rep through a decomposition into volumes, as cited by Zou and Feng
---

Direct modeling changes the shape of a solid by acting on its faces. The user selects faces of a [boundary representation](/boundary-representation/) and moves, rotates, offsets or deletes them. The modeler then rebuilds the edges and vertices where the moved faces meet their neighbours. Each new edge is the [intersection](/surface-surface-intersection/) of the new surfaces of its two faces, and each new vertex is the common point of its faces. The neighbouring faces are extended or trimmed to follow. No feature history is stored or replayed. The result is just a new B-rep, so a model imported from another system, with no history at all, can be edited as easily as a native one. When the move is small, regeneration keeps the topology and only recomputes geometry. When the move is large, faces appear and disappear. Then the edit must decide on a new topology, and that decision is the hard part. A sound way to make it is to treat the move as a sweep and apply a [regularized Boolean](/regularized-set-operations/) with the swept volume at each topology change, as Zou and Feng do. The commercial packages use their own rules, which are not published.

## In plain words

A block has a hole in it. You want the block shorter, so you grab its right side and drag it to the left. A direct modeler moves that side and stretches or shrinks the top and bottom to meet it. It does not ask how the block was made.

As long as the side stays clear of the hole, that is all. When the side reaches the hole, something has to give. The hole could open to the right and become a notch. It could vanish. Or the program could refuse. A reasonable rule is to cut away exactly the material that the moving side passed through, so the shape changes smoothly as you drag.

The price of having no history is that the program cannot know that the hole was meant to stay centred. It only sees faces.

## When it applies

- The model is a B-rep, often imported, whose history is missing or too tangled to edit. Direct editing needs only the faces, edges and vertices.
- The change is local: move a face, change the radius of a cylinder, offset a group of faces, delete a fillet or a small feature. Regeneration touches only the selected faces and their neighbours.
- The design intent that a history would capture, such as "this hole stays in the middle" or "this wall stays 2 mm thick", is not needed, or the user supplies it at edit time.
- It is not the right tool when a family of parts must follow from a few parameters. That is what [feature-based](/feature-based-modeling/) parametric modeling is for, and many systems now combine the two.

## The template

The edit is a motion of the selected faces $S$ along a path $T(t)$, $t \in [0, 1]$, where $T(0)$ is the identity: a translation along a normal, a rotation about an axis, or an offset by $t\,d$. A *topology change point* is a value $\tau$ where the regenerated model has one topology just before $\tau$ and another just after. At such a point an edge or a face shrinks to nothing (a lost connection), or a moved face meets a face that it did not meet before (a new connection).

```pseudo id=main
DIRECT-EDIT(M, S, T)
L1  t ← 0
L2  while t < 1 do
L3      τ ← the first topology change point in (t, 1], or 1 if there is none
L4      move the surface of each face of S to its position at τ
L5      for each edge with a face in S: its curve ← the intersection of the new surfaces of its faces
L6      for each vertex with a face in S: its point ← the common point of the new surfaces of its faces
L7      if τ < 1 then
L8          W ← the volume swept by the faces of S as t crosses τ, signed by the direction of motion
L9          M ← M − W if the faces move into the solid, M ∪ W if they move out   ▷ the new topology
L10     t ← τ
L11 rebuild the blends whose supporting faces moved
L12 return M
```

Lines L4 to L6 are the *regeneration*. They keep the topology and recompute the geometry. Lines L8 and L9 are the *resolution* at a topology change point. Line L11 deals with fillets and chamfers, which are treated as blend features and rebuilt on the new faces, for example as [rolling-ball blends](/rolling-ball-blend/), not stretched.

**Why regeneration is well defined between changes.** Take a solid with planar faces where every vertex lies on exactly three planes with independent normals, and translate one plane $\{x : n_k \cdot x = b_k\}$ by $t$ along its unit normal. A vertex on planes $i, j, k$ solves $A x = b + t\,e_k$, where the rows of $A$ are the three normals. So $x(t) = x(0) + t\,A^{-1} e_k$ moves on a straight line, along the edge where planes $i$ and $j$ meet. Vertices that are not on the moved plane stay where they are. Every vertex moves continuously in $t$. So the edge lengths and the distances between non-incident entities change continuously, and the B-rep stays valid with the same topology on an open interval around $t = 0$. That interval ends at the first $t$ where an edge length reaches zero or a vertex reaches a face that it is not on. That $t$ is the first topology change point, and line L3 finds it by solving these linear conditions. Curved faces need the same argument with the implicit function theorem, and an event search over intersections of surfaces.

**Why the Boolean resolution is continuous.** Let $W(t)$ be the volume swept by a face $F$ of area $a$ moving into the solid by distance $t$. Then $M(t) = M(0) - W(t)$ by a regularized difference, and for $t < t'$ the symmetric difference of $M(t)$ and $M(t')$ lies in $W(t') \setminus W(t)$. That set has volume at most $a\,(t' - t)$. So the volume of the result changes by at most $a\,\lvert t' - t\rvert$, through every topology change point. Deleting a face or filling a hole at a change point would make the volume jump. This continuity is the criterion that Zou and Feng use.

## Classic examples

**A worked case.** Take the cross-section of a block, $[0, 10] \times [0, 6]$, with a through hole $[3, 6] \times [2, 4]$. The right face $x = 10$ is pushed into the solid, to $x = 10 - t\,d$ with $d = 8$. Write $x_R = 10 - 8t$.

- For $x_R > 6$, which is $t < 1/2$, regeneration alone works. The top and bottom faces shrink to length $x_R$, and the hole is untouched. The section has two loops of 4 edges each, and its area is $6 x_R - 6$.
- At $x_R = 6$ the right face touches the hole's right wall. This is a new connection, so $t = 1/2$ is a topology change point. Regeneration alone would now carry the right face through the hole and leave the hole's right wall outside the material, which is not a valid solid.
- The resolution removes the swept region $[x_R, 10] \times [0, 6]$. For $3 < x_R < 6$ the section is $[0, x_R] \times [0, 6]$ minus $[3, x_R] \times [2, 4]$. It is a C shape with one loop of 8 edges, $(0,0)$, $(x_R, 0)$, $(x_R, 2)$, $(3, 2)$, $(3, 4)$, $(x_R, 4)$, $(x_R, 6)$, $(0, 6)$. The right face has split into two pieces, and the hole's right wall is gone. The area is $6 x_R - 2 (x_R - 3)$, which equals $6 x_R - 6$ at $x_R = 6$, so it does not jump.
- At $x_R = 3$, $t = 7/8$, the moving face reaches the hole's left wall. This is a second topology change point. Past it the section is the rectangle $[0, x_R] \times [0, 6]$ with area $6 x_R$, and at $x_R = 3$ both formulas give 18.

The final result at $t = 1$ is $[0, 2] \times [0, 6]$. Two other answers are geometrically possible at the first change point: drop the hole, or stop the face at the hole. Both make the area jump, so the continuity criterion rejects them.

- **Moving and offsetting faces.** Moving a planar face, changing the radius of a cylindrical face, or offsetting a set of faces by a distance are the basic edits. The new edges come from [surface intersection](/surface-surface-intersection/), and an offset of all faces is the setting of [solid offsetting](/solid-offsetting/) and the [offset surface](/offset-surface/).
- **Deleting a feature.** To delete a hole or a boss, the modeler removes its faces and extends the neighbouring faces until they close the gap. This is the reverse of a Boolean, and it needs the faces of the feature first, from the user or by [feature recognition](/feature-recognition/).
- **Moving a feature.** To move a hole, the modeler moves all its faces together by a rigid motion and regenerates their edges with the face they cut. Woo and Lee, and Kim and Mun, treat such a push as a change of the volume of a feature, which keeps the result valid.
- **Blends.** A fillet between two moved faces must change its shape. Direct modelers recognize blend faces and rebuild them as [blending surfaces](/blending-surface/) on the new faces, rather than move them.
- **Topology edits.** When a resolution changes the topology, the update can be expressed with [Euler operators](/euler-operators/): extruded, the block with a hole has $V, E, F, R, H = 16, 24, 10, 2, 1$ (vertices, edges, faces, inner loops, through holes), and the C shape has $16, 24, 10, 0, 0$. Both satisfy the [Euler-Poincaré formula](/euler-poincare-formula/) $V - E + F - R = 2(S - H)$ with $S = 1$ shell.

## Variations

- **Tweaking.** The modelers of the 1970s offered face moves that kept the topology fixed and refused any move that would change it. That is lines L4 to L6 alone, with line L3 as a guard.
- **Synchronous and hybrid modeling.** Commercial systems let the user add dimensions and constraints such as "parallel", "coaxial" or "same radius" at edit time, and solve them together with the move. Moves then carry along the faces that are related by the constraints. Some systems also turn a direct edit into a feature of a history, so the two styles can be mixed.
- **Polygonal push-pull.** For models with planar faces, such as buildings, Lipp, Wonka and Müller give rules that insert new faces or let neighbours tilt, so a push does not distort its neighbours.
- **Swept-volume resolution.** Zou and Feng split the motion at its topology change points and update the model at each one by a Boolean with the volume swept since the last one. That is lines L7 to L9, and it gives a valid solid whose volume changes continuously.
- **Moving neighbours.** If the neighbours must stay tangent to the moved face, they cannot simply be extended. Their motion is then the solution of a system of nonlinear equations, and Zou and Feng leave that case open.

## Pitfalls

- **Lost intent.** Without a history the program does not know that a hole was centred, or that two walls had the same thickness. A move of one face keeps nothing else, unless the user adds constraints or the system guesses them.
- **Different packages, different answers.** At a topology change point several valid solids are possible, and the choice is a convention. Zou and Feng tested five commercial packages on a few push-pull cases. In some cases some packages produced an invalid model, and in others they produced a valid model with an abrupt change of shape. Those are measurements on a handful of models, not a general comparison.
- **Missed change points.** If line L3 checks only the end of the move, a fast move can jump over two change points at once and pick a topology that no continuous path gives. Check events along the whole path.
- **Stretching blends.** Moving the faces next to a fillet without rebuilding the fillet leaves a blend of the wrong radius, or one that no longer touches its faces.
- **Names.** Direct edits change the topology without a history, so references from drawings, assemblies or downstream features can break. This is the [persistent naming problem](/persistent-naming-problem/) without a history to help.

## Exercises

1. In the worked case, give the area of the section as a function of $t$ for all $t \in [0, 1]$, and check that it is continuous and decreasing.
2. A cube $[0, 1]^3$ has its top face tilted: the plane $z = 1$ becomes $z = 1 + s x$. Using the formula $x(t) = x(0) + t\,A^{-1} e_k$ and its analogue for a rotation, find the new vertices. For which $s$ does the top face stay valid?
3. Give a planar polygon and a translation of one of its edges such that the first topology change point is an edge of length zero, not a new contact. Describe the topology just after it.
4. Show that if the faces of $S$ move outward and line L9 uses a union, the result contains $M$ and its area changes by at most $a\,\lvert t' - t\rvert$ for a face of area $a$.

## References
