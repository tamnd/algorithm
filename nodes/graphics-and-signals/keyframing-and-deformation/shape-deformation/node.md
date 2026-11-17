---
tag: SC5AQ9
kind: problem
slug: shape-deformation
name: Shape deformation
aliases:
- mesh deformation
- space deformation
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Change the shape of a surface or volume smoothly from a few user handles, such as points, curves, a lattice or a cage.
model: real-ram
prereqs: [deformation-gradient]
see_also: [free-form-deformation, cage-based-deformation, as-rigid-as-possible-shape-manipulation, as-rigid-as-possible-deformation, laplacian-surface-editing, linear-blend-skinning, barr-global-deformations, wire-deformation]
sources:
  - paper: doi:10.1109/TVCG.2007.1054
    title: "Mario Botsch and Olga Sorkine, On linear variational surface deformation methods, IEEE Transactions on Visualization and Computer Graphics 14(1), 213-230, 2008"
    locator: the whole survey (surface-based and space deformations, linear variational methods, and their trouble with large rotations)
  - paper: doi:10.1007/978-94-007-5446-1_3
    title: "Jesús R. Nieto and Antonio Susín, Cage based deformations: a survey, in Deformation Models, Lecture Notes in Computational Vision and Biomechanics, Springer, 75-99, 2013 (online 2012)"
    locator: the whole survey (space deformations controlled by cages)
---

Shape deformation is the problem of changing the shape of an object from a few controls that a user moves: points, curves, a lattice, a cage or a skeleton.
The object is a surface mesh, a volume or a point cloud with many points, and the user moves only a few handles, so the method must decide how every other point follows.
A good answer is smooth, meets the handles, and keeps the local detail of the object, so that a bent arm looks bent and not sheared.
There are two large families.
**Space deformations** deform the space around the object with a map $f: \mathbb{R}^d \to \mathbb{R}^d$ and apply it to every point, whatever the object is made of: Barr's maps, lattices, wires and cages.
**Surface-based deformations** work on the mesh itself and minimize an energy of its triangles or vertices, such as [Laplacian surface editing](/laplacian-surface-editing/) or [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/).
The alias "space deformation" names the first family only, not the whole problem.

## In plain words

You have a detailed 3D model and you want to bend it, stretch it or pose it.
Moving its thousands of points one by one is not possible, so you grab a few of them, or a simple frame around the model, and move those.
The computer has to fill in how everything else moves.
Some methods bend the whole space around the model, like a block of jelly, and the model goes with the jelly.
Other methods look at the model's own surface and keep each small piece of it as close to its old shape as they can.
Both kinds try to make the result look like the same object, only moved and bent.

## Definition

The input is a rest shape $S$, given by the points $p_1, \dots, p_N$ (and, for surface methods, the mesh that joins them), a set of handles with rest values $h$, and new handle values $h'$.
The output is the deformed points $p'_1, \dots, p'_N$.
The requirements are:

- **Constraints.** The handles are met: handle points reach their targets, exactly or in the least squares sense.
- **Rest state.** If $h' = h$, then $p' = p$.
- **Smoothness.** The deformed shape depends smoothly on the handles and has no tears.
- **Shape preservation.** Small parts of the object change by a rotation, or a rotation and a uniform scale, as far as the handles allow.

A **space deformation** is a map $f_{h'}$ with $p'_k = f_{h'}(p_k)$ for every point, where $f_h$ is the identity.
A **surface-based deformation** is $p' = \arg\min_x E(x; p)$ over the meshes $x$ that meet the constraints, for an energy $E$ that is 0 at the rest shape, such as $\sum\|L(x) - L(p)\|^2$ with a [Laplacian](/laplacian-matrix/) $L$ or a sum of squared distances to rotated rest cells.

The cost model is the real RAM: each arithmetic operation on real numbers costs 1.
Costs are given in terms of the number of points $N$ and the number of controls $k$, and they are split into a setup cost, paid once when the handles or the cage are chosen, and a cost per pose, paid each time the handles move.

## Variants

- **2D or 3D.** 2D shape manipulation deforms drawings and images; 3D deformation deforms models and volumes.
- **Kind of handle.** Points, regions of the surface, curves ([wires](/wire-deformation/)), lattices ([FFD](/free-form-deformation/)), cages ([cage-based deformation](/cage-based-deformation/)) or skeletons ([linear blend skinning](/linear-blend-skinning/)).
- **Linear or nonlinear.** Linear methods solve one linear system or apply fixed weights; nonlinear methods also find rotations, by fitting or by iteration.
- **What is kept.** Angles (conformal maps), lengths (isometric maps), volume, or the Laplacian detail of the surface.
- **Interpolation of given shapes.** When the target shapes are given in full and only the shapes in between are wanted, the problem becomes shape interpolation, as in [as-rigid-as-possible shape interpolation](/as-rigid-as-possible-shape-interpolation/).
- **Learned or example-based.** [Pose-space deformation](/pose-space-deformation/) blends sculpted corrections over the pose of a skeleton, and [deformation transfer](/deformation-transfer/) copies the deformation of one mesh onto another.

## Examples

**A lattice.** In [free-form deformation](/free-form-deformation/) with the unit cube as a lattice of degree 2, raising the center control point by $1/2$ moves the center of the cube up by $1/16$, to $(1/2, 1/2, 9/16)$, while the corners stay.

**A cage.** With mean value coordinates of the L-shaped cage with the vertices $(0, 0)$, $(2, 0)$, $(2, 1)$, $(1, 1)$, $(1, 2)$, $(0, 2)$, sliding the top edge by $0.5$ to the right moves the point $(0.5, 1.5)$ to about $(0.8464, 1.5)$; see [cage-based deformation](/cage-based-deformation/).

**Handles on a mesh.** A bar of $5 \times 1$ squares, cut into 10 triangles, has its left end fixed and its right end raised by $1.5$. [As-rigid-as-possible shape manipulation](/as-rigid-as-possible-shape-manipulation/) bends it into an S, and the vertex that starts at $(2, 0)$ ends at about $(2.1903, 0.5898)$.

**A closed-form map.** [Barr's bend](/barr-global-deformations/) with the rate $k = 0.5$ maps the point $(0, 1, 0)$ to $(0, 2\sin 0.5, 2 - 2\cos 0.5) \approx (0, 0.9589, 0.2448)$ on a circle of radius 2.

## Known algorithms

Space deformations:

- [Barr's global deformations](/barr-global-deformations/) (1984): taper, twist and bend in closed form, with exact normals.
- [Free-form deformation](/free-form-deformation/) (Sederberg and Parry 1986): a trivariate Bezier lattice.
- [Extended free-form deformation](/extended-free-form-deformation/) (Coquillart 1990): lattices of other shapes, embedded by Newton iteration.
- [Wires](/wire-deformation/) (Singh and Fiume 1998): space curves with a radius of influence.
- [Cage-based deformation](/cage-based-deformation/) with [mean value](/floater-mean-value-coordinates/), [harmonic](/harmonic-coordinates/) or [Green](/green-coordinates/) coordinates.
- [Linear blend skinning](/linear-blend-skinning/) and [bounded biharmonic weights](/bounded-biharmonic-weights/): blends of handle transforms with weights per point.

Surface-based and mesh-based deformations:

- [As-rigid-as-possible shape manipulation](/as-rigid-as-possible-shape-manipulation/) (Igarashi, Moscovich and Hughes 2005): two linear least squares steps on a 2D triangle mesh.
- [Laplacian surface editing](/laplacian-surface-editing/): keeps the Laplacian coordinates of the surface in the least squares sense.
- [As-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) (Sorkine and Alexa 2007): alternates fitting a rotation per vertex cell and a sparse linear solve.

## Bounds

**Output cost.** Every method must at least write the $N$ moved points, so $\Omega(N)$ time per pose. Space deformations with $k$ controls and fixed weights cost $\Theta(Nk)$ per pose with dense weights; linear surface methods cost one sparse factorization when the handles are chosen and one back substitution per pose.

**Linear blends cannot keep shape under every edit (proved).** Let a method move each point by $p' = \sum_i w_i(p)h'_i$ with scalar weights that do not depend on $h'$, and let it reproduce translations and rotations of the handles. Then it reproduces every linear map $M$ of the handles, because $\sum_i w_iMh_i = M\sum_i w_ih_i$. So if the user shears the handles, every part of the object is sheared by the same amount, and no such method keeps local shapes rigid or conformal under that edit. Methods that keep shape must depend on $h'$ in a nonlinear way: [Green coordinates](/green-coordinates/) use the moved normals and edge lengths, and [ARAP](/as-rigid-as-possible-shape-manipulation/) fits rotations.

**Large rotations in linear surface methods.** Botsch and Sorkine (2008) show that linear variational methods, which solve one linear system in the positions, handle translations of the handles well but have trouble with large rotations, because the rest detail is stored in the rest orientation; nonlinear methods that estimate rotations fix this.

## Reductions

- **FFD is a cage method.** Free-form deformation is cage-based deformation with a box cage and Bernstein polynomials as the coordinates.
- **Cages are linear blends.** A cage deformation with weights $w_i$ is linear blend skinning in which each handle is a vertex with a translation only.
- **Harmonic coordinates reduce to the Laplace equation.** They are solutions of a [Poisson](/poisson-equation/)-type boundary value problem, one per cage vertex.
- **Linear surface methods reduce to sparse least squares.** [Laplacian surface editing](/laplacian-surface-editing/) and each step of ARAP manipulation are [least squares problems](/least-squares-problem/) with sparse symmetric positive definite normal matrices, solved by [Cholesky factorization](/cholesky-decomposition/).
- **Wires reduce to closest points on curves.** Each point of a wire deformation needs its closest point on the reference curve, a [point inversion](/newton-point-inversion/) problem on smooth curves.

## Applications

- **Character animation.** Skeletons with skinning, cages and pose-space corrections drive the bodies and faces of animated characters.
- **Modeling.** Lattices, wires and surface editing let artists sculpt detailed shapes from simple controls.
- **2D animation.** Shape manipulation animates drawings, photos and text by dragging points.
- **Simulation and medicine.** Embedding a detailed mesh in a coarse simulation mesh or cage, and B-spline free-form deformations in image registration, use the same idea of a coarse map that moves a fine object.

## References
