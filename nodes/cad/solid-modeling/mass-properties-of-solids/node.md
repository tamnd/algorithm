---
tag: S1B0KK
kind: problem
slug: mass-properties-of-solids
name: Mass properties of solids
aliases:
- solid mass properties
- volume and moments of a solid
area: cad/solid-modeling
level: core
summary: Compute the volume, centre of mass and inertia tensor of a solid given as a B-rep, a CSG tree or a cell model, exactly or to a stated accuracy.
prereqs: [r-set, boundary-representation, constructive-solid-geometry]
see_also: [mirtich-polyhedral-mass-properties, csg-ray-casting, klee-measure-problem, boundary-evaluation, solid-boolean-operations, set-membership-classification, spatial-occupancy-enumeration, generalized-winding-number]
sources:
  - paper: doi:10.1145/358628.358643
    title: Yong Tsui Lee and Aristides A. G. Requicha, Algorithms for computing the volume and other integral properties of solids, I, Known methods and open issues, Communications of the ACM 25(9), 635 to 641, 1982
    locator: the whole paper (the statement of the problem for each representation, and the survey of integration methods)
  - paper: doi:10.1145/358628.358648
    title: Yong Tsui Lee and Aristides A. G. Requicha, Algorithms for computing the volume and other integral properties of solids, II, A family of algorithms based on representation conversions and cellular approximations, Communications of the ACM 25(9), 642 to 650, 1982
    locator: the whole paper (integration over cell decompositions obtained from CSG, and the accuracy of the approximation)
  - paper: doi:10.1080/10867651.1996.10487458
    title: Brian Mirtich, Fast and accurate computation of polyhedral mass properties, Journal of Graphics Tools 1(2), 31 to 50, 1996
    locator: the whole paper (exact volume, first and second moments of a polyhedron from its faces)
  - paper: doi:10.1016/0146-664X(82)90169-1
    title: Scott D. Roth, Ray casting for modeling solids, Computer Graphics and Image Processing 18(2), 109 to 144, 1982
    locator: the use of ray casting on a CSG tree to estimate volumes
  - paper: doi:10.1109/FOCS.2013.51
    title: Timothy M. Chan, Klee's measure problem made easy, FOCS 2013
    locator: the O(n^(d/2)) algorithm for the volume of a union of n boxes, the case of CSG unions of boxes
---

The mass property problem asks for the volume, the mass, the centre of mass and the inertia tensor of a solid, given in one of the representations of a solid modeler. All of them are integrals over the solid of the monomials $1$, $x$, $y$, $z$, $x^2$, $y^2$, $z^2$, $xy$, $yz$, $zx$, times the density. For a polyhedron with rational vertices and constant density the values are rational numbers and can be computed exactly in linear time. For a CSG tree, or a solid with curved faces, the problem is harder: either the boundary must be computed first, or the integrals are approximated, and then the answer comes with an error.

## In plain words

An engineer needs to know how heavy a part is, where its balance point is, and how hard it is to spin it about each axis. These numbers are its mass properties.

For a part made of one material, they all come from adding up small pieces of the part: how much space each piece takes, and where it is. The question is how to do that sum when the part is stored only as its outer faces, or as a recipe of blocks and cylinders joined and cut.

For flat faces the sum can be done exactly. For a recipe, or for curved faces, the usual ways either first work out the outer faces, or they fill the part with many small cells and add them up, which gives an answer that is close but not exact.

## Definition

**Input.** A solid $S \subset E^3$, an [r-set](/r-set/), given as a valid [boundary representation](/boundary-representation/), as a [CSG](/constructive-solid-geometry/) tree, or as a set of cells, and a density $\rho$. Usually $\rho$ is a constant, and then the mass is $\rho$ times the volume.

**Output.** The integrals
$$M = \int_S \rho \, dV, \qquad \mathbf{c} = \frac{1}{M} \int_S \rho \, \mathbf{x} \, dV, \qquad \mathbf{J} = \int_S \rho \, \big( |\mathbf{x} - \mathbf{c}|^2 \, \mathbf{I} - (\mathbf{x} - \mathbf{c})(\mathbf{x} - \mathbf{c})^{\mathsf{T}} \big) \, dV,$$
the mass, the centre of mass and the inertia tensor about the centre of mass. With constant $\rho$ these follow from the ten integrals $\int_S x^a y^b z^c \, dV$ with $a + b + c \le 2$.

**Objective.** In the exact form, return the values exactly, as rationals or in a symbolic form such as $\tfrac{4}{3}\pi$. In the approximate form, return values within a stated absolute or relative error $\varepsilon$, with the error either proved or bounded with a stated probability.

**Constraints.** The integrals are over the regularized solid, so faces, edges and points of zero volume do not matter. The answer must not depend on how the solid is represented: two B-reps of the same set, or a B-rep and a CSG tree of the same set, give the same values.

**Size.** For a B-rep, $n$ is the total number of vertices over all faces. For a CSG tree, $n$ is the number of primitives.

## Variants

- **Polyhedra.** All faces are planar polygons. The exact values are rational when the vertices are.
- **Curved B-reps.** Faces on quadrics or on spline surfaces. The values are integrals over curved patches, usually computed by numerical quadrature.
- **CSG trees.** The integral over a combination is linear in the indicator function, so $\int_{A \cup^* B} = \int_A + \int_B - \int_{A \cap^* B}$ and $\int_{A -^* B} = \int_A - \int_{A \cap^* B}$, but the intersection terms are again solids that must be integrated.
- **Unions of boxes.** The volume of the union of $n$ axis-parallel boxes is [Klee's measure problem](/klee-measure-problem/).
- **Cell models.** The solid is a set of grid cells or an octree, as in [spatial occupancy enumeration](/spatial-occupancy-enumeration/). The sum over the cells is exact for the cell model and approximate for the solid that the cells approximate.
- **Meshes that are not closed.** For a triangle mesh with holes or self-intersections, the inside can be defined by the [generalized winding number](/generalized-winding-number/), and the integrals are over that set or are weighted by the winding number.
- **Surface area.** The area of $\partial S$ is a mass property of a different kind, a boundary integral instead of a volume integral.

## Examples

**A notched cube.** Let $S = [0, 2]^3 -^* [1, 2]^3$, the difference of the overlapping cubes on the [Boolean operations](/solid-boolean-operations/) page, with $\rho = 1$. By the linearity above, each integral is the one over $[0, 2]^3$ minus the one over $[1, 2]^3$.

| quantity | $[0, 2]^3$ | $[1, 2]^3$ | $S$ |
|---|---|---|---|
| $\int 1 \, dV$ | $8$ | $1$ | $7$ |
| $\int x \, dV$ | $8$ | $3/2$ | $13/2$ |
| $\int (y^2 + z^2) \, dV$ | $64/3$ | $14/3$ | $50/3$ |
| $\int x y \, dV$ | $8$ | $9/4$ | $23/4$ |

So $M = 7$ and $\mathbf{c} = (13/14, 13/14, 13/14)$. About the origin the diagonal entries of the inertia tensor are $50/3$, and the off-diagonal entries are $-23/4$. Moving to the centre of mass subtracts $M (|\mathbf{c}|^2 \mathbf{I} - \mathbf{c} \mathbf{c}^{\mathsf{T}})$, which gives the diagonal entries $J_{xx} = J_{yy} = J_{zz} = 193/42$ and the off-diagonal entries $J_{xy} = J_{yz} = J_{zx} = 2/7$. These values were checked with exact rational arithmetic.

**A ball.** The unit ball has volume $\tfrac{4}{3}\pi$, centre $\mathbf{0}$ and $J = \tfrac{8}{15}\pi \, \mathbf{I}$. The values are not rational, so an exact answer needs a symbolic form, and a polyhedral or cell approximation of the ball gives only an approximation.

**Representation does not matter.** The notched cube as a B-rep with $9$ faces, as the CSG tree $[0, 2]^3 -^* [1, 2]^3$, and as the $7$ unit cells of $\{0, 1\}^3$ other than $[1, 2]^3$ have the same values. A $40 \times 40 \times 40$ grid of cells of side $1/20$, one cell kept when its centre is in $S$, also gives the volume $7$ exactly here, because the faces of $S$ lie on cell boundaries. For a solid whose faces cut the cells, the cell sum has an error.

## Known algorithms

- **[Mirtich's method](/mirtich-polyhedral-mass-properties/).** For a polyhedral B-rep, the divergence theorem turns each volume integral into a sum of face integrals, and each face integral is turned into a sum over its edges. It returns the exact values with rational input, in $\Theta(n)$ time and $O(1)$ extra space. The page also covers the sum of signed tetrahedra of Lien and Kajiya.
- **[CSG ray casting](/csg-ray-casting/).** Cast a grid of parallel rays through a CSG tree and sum the lengths of the in intervals times the grid cell area. No boundary is computed. The result is a numerical quadrature of the cross-section function, so its error depends on the grid spacing and on the shape. Roth used it for volumes.
- **[Boundary evaluation](/boundary-evaluation/) then a B-rep method.** Convert the CSG tree to a B-rep, then integrate it exactly. Exact for polyhedral primitives, at the cost of the conversion.
- **Cell decomposition** (Lee and Requicha). Split space into cells, classify each cell against the CSG tree with [set membership classification](/set-membership-classification/), integrate the cells inside exactly, and refine the cells on the boundary. The error is bounded by the volume of the boundary cells.
- **Monte Carlo.** Classify $N$ random points of a bounding box. The fraction inside times the box volume estimates the volume, with a standard error of order $1/\sqrt{N}$.
- **Unions of boxes.** The [Klee's measure problem](/klee-measure-problem/) algorithms compute the volume exactly, in $O(n^{3/2})$ time for $n$ boxes in three dimensions by Chan's method.

## Bounds

- **Polyhedral B-reps.** $\Theta(n)$ time. The upper bound is Mirtich's method. The lower bound holds because the volume depends on every vertex: moving one vertex of a face along the normal of the face changes the volume, so an algorithm that does not read a vertex is wrong on some input.
- **CSG unions of boxes.** The volume of a CSG union of $n$ boxes needs $\Omega(n \log n)$ time in the algebraic decision tree model, by the lower bound for Klee's measure problem, and the best known upper bound in three dimensions is $O(n^{3/2})$. So computing mass properties from CSG is harder in the worst case than from a B-rep of the same solid.
- **Through the boundary.** A B-rep of a CSG solid can have size $\Theta(n^2)$ for two primitives of size $n$ (see the Boolean operations page), so the route through boundary evaluation can be far more costly than the size of the tree.
- **Approximation.** For a grid of rays or cells of spacing $h$, the error for a polyhedron is at most the volume of the cells that meet the boundary, which is $O(h \cdot \operatorname{area}(\partial S))$. The Monte Carlo error is a probability statement, not a bound. The accuracy of practical quadrature on curved B-reps is measured, not proved, unless the method gives an error bound.

## Reductions

- **To ten integrals.** Mass, centre and inertia about any point follow from $\int_S x^a y^b z^c \, dV$ with $a + b + c \le 2$, by the parallel axis rule $\mathbf{J}_{\mathbf{0}} = \mathbf{J} + M (|\mathbf{c}|^2 \mathbf{I} - \mathbf{c} \mathbf{c}^{\mathsf{T}})$.
- **To Boolean operations.** The integral over a combination is the signed sum of integrals over intersections of primitives, so CSG mass properties reduce to mass properties of [Boolean](/solid-boolean-operations/) results.
- **From Klee's measure problem.** The volume of the union of $n$ boxes is the volume of a CSG tree that is a union of $n$ box primitives, so its lower bound applies.
- **To point classification.** Cell and Monte Carlo methods need only an in or out answer per point or cell.

## Applications

- **Mechanical design.** The weight, balance and inertia of a part or an assembly, and checks that a design meets a weight limit.
- **Dynamics and simulation.** Rigid body simulators need the mass, the centre of mass and the inertia tensor of each body.
- **Manufacturing.** The volume of material removed by a machining step, and the material cost of a part.
- **Validation of models.** A volume that changes after an exchange between systems, or a negative volume, shows that a B-rep is broken or inverted.

## References
