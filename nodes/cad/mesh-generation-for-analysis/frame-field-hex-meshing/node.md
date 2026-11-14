---
tag: WR7B7E
kind: algorithm
slug: frame-field-hex-meshing
name: Frame-field hex meshing
aliases:
- CubeCover
area: cad/mesh-generation-for-analysis
level: research
summary: Computes a smooth 3D frame field in a solid and an integer-grid map aligned to it, as Nieser, Reitebuch and Polthier did, whose integer isosurfaces form the hexes.
solves: [hexahedral-mesh-generation]
model: real-ram
complexity:
  vars: {F: the number of free cells (one sweep)}
  time: {worst: O(F)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2011
  people: [Matthias Nieser, Ulrich Reitebuch, Konrad Polthier]
  note: In 2011 Nieser, Reitebuch and Polthier computed an integer grid map from a given frame field, and Huang, Tong, Wei and Bao computed boundary-aligned smooth frame fields. Later work improved the field, the treatment of singularities and the extraction of the hexes.
prereqs: [hexahedral-mesh-generation, cross-field, mixed-integer-quadrangulation]
see_also: [polycube-hex-meshing, whisker-weaving, spatial-twist-continuum, hexahedral-sweeping, wahba-problem, davenport-q-method, jacobi-eigenvalue-algorithm, gauss-seidel-method]
sources:
  - paper: "M. Nieser, U. Reitebuch and K. Polthier, CubeCover, parameterization of 3D volumes, Computer Graphics Forum 30(5), 2011, 1397 to 1406"
    locator: the integer grid map that follows a frame field, with integer transitions and singularities on grid lines (general locator)
  - paper: "Jin Huang, Yiying Tong, Hongyu Wei and Hujun Bao, Boundary aligned smooth 3D cross-frame field, ACM Transactions on Graphics 30(6), 2011"
    locator: frames as rotations of the polynomial x^4 + y^4 + z^4 in the spherical harmonics basis, and the smoothness energy (general locator)
  - paper: "Nicolas Ray, Dmitry Sokolov and Bruno Lévy, Practical 3D frame field generation, ACM Transactions on Graphics 35(6), 2016, article 233"
    locator: frames at vertices, boundary constraints and a faster projection onto frames (general locator)
  - paper: "Max Lyon, David Bommes and Leif Kobbelt, HexEx, robust hexahedral mesh extraction, ACM Transactions on Graphics 35(4), 2016, article 123"
    locator: the extraction of the hexes from the integer level sets of the map (general locator)
  - paper: "Berthold K. P. Horn, Closed-form solution of absolute orientation using unit quaternions, Journal of the Optical Society of America A 4(4), 1987, 629 to 642"
    locator: the best rotation as the eigenvector of the largest eigenvalue of a symmetric 4 x 4 matrix, used in L6 (general locator)
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: the section on frame fields, its three steps, the octahedral symmetry, and the singularities that no hex mesh can have
---

A frame field method makes a hex mesh of a solid in three steps. First it computes a frame field: at each point of the solid, a small cube orientation, aligned with the boundary and as smooth as possible. Then it computes an integer grid map, a map from the solid into space whose gradient follows the frames and which sends the singular curves of the field to integer grid lines. Last it extracts the hexes as the preimages of the cells of the integer grid. This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it guides the hexes by a field that can follow any shape, while that page states the general problem and its limits. The code on this page implements one simple step of the first stage, a local smoothing sweep of a frame field on a grid of cells, and it is not the published field solvers.

## In plain words

Fill a solid with many tiny dice. Each die can turn, but the dice next to a wall must lie flat against it. Now turn each inner die a little so that it looks like its neighbours. After many such turns the dice change their direction smoothly through the solid.

Some places cannot be made smooth, and there the dice turn around a line in a way that never fits. These lines become the edges of the mesh where more or fewer than four hexes meet.

Next, draw a 3D grid that follows the dice everywhere, with grid lines through the bad lines. The cells of this grid are the hexes. A die looks the same after a quarter turn, so turning by 90 degrees between two dice costs nothing.

## The problem

A frame is a rotation $R \in SO(3)$, whose columns and their negatives give the six directions of a cube. Two rotations $R$ and $Rg$ with $g$ in the octahedral group $O$, the 24 signed permutation matrices with determinant $+1$, give the same frame. The core step works on a grid of cells, each with a frame. Boundary cells are fixed, and the free cells must be chosen to make the smoothness energy small:

$$E = \sum_{\{i, j\} \text{ adjacent}} \min_{g \in O} \lVert R_i - R_j g \rVert_F^2 = \sum_{\{i, j\}} \Big(6 - 2 \max_{g \in O} \operatorname{tr}(R_i^{\mathsf T} R_j g)\Big).$$

## The algorithm

One sweep visits the free cells in a fixed order. At each cell it turns every neighbour frame by the best element of $O$, adds the results, and replaces the frame by the nearest rotation to this sum. Line L6 finds that rotation by Horn's quaternion method: it is the eigenvector of the largest eigenvalue of a symmetric $4 \times 4$ matrix built from the sum, found here by the cyclic [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).

```pseudo id=main
FRAME-SWEEP(R, free)
L1  for each free cell i, in a fixed order do
L2      M ← the 3 × 3 zero matrix
L3      for each neighbour j of i do
L4          G ← R_j g for the g in O that maximizes tr(R_iᵀ R_j g)
L5          M ← M + G
L6      R_i ← the rotation R that maximizes tr(Rᵀ M), by Horn's quaternion method
L7  return R
```

This is a block [Gauss-Seidel](/gauss-seidel-method/) step on the energy, one cell at a time. The best rotation for a sum of matrices is the same problem as [Wahba's problem](/wahba-problem/), which the [Davenport q-method](/davenport-q-method/) also solves by a $4 \times 4$ eigenvector.

**The full method.** A frame field pipeline goes on from the field, in words:

1. Compute a smooth frame field on a tetrahedral mesh, aligned with the boundary. Published methods use a representation that has the cube symmetry built in, such as the rotations of the polynomial $x^4 + y^4 + z^4$ in a basis of spherical harmonics, and minimize a Dirichlet energy.
2. Find the singular curves of the field and repair those that no hex mesh can have.
3. Cut the solid to a ball and compute a map $f$ whose gradient follows the frames. Across each cut, the two sides of $f$ must differ by an element of $O$ and an integer shift, and the singular curves must map to integer grid lines. This is a mixed integer problem, often solved by rounding the integers one at a time.
4. Extract the hexes as the preimages under $f$ of the cells of the integer grid.

## Example

Take the $3 \times 3 \times 3$ grid of cells with all frames equal to the identity, except the center cell, which is turned by an angle $\theta$ about the $z$ axis. The center has 6 neighbours, so before the sweep $E = 6\,(4 - 4\cos\theta')$, where $\theta'$ is the distance from $\theta$ to the nearest multiple of $90^\circ$.

| $\theta$ | $E$ before | best $g$ in L4 | new center frame | $E$ after |
|---|---|---|---|---|
| $30^\circ$ | $24 - 12\sqrt3 \approx 3.215$ | identity | identity | $0$ |
| $45^\circ$ | $24 - 12\sqrt2 \approx 7.029$ | identity (a tie with the quarter turn) | identity | $0$ |
| $60^\circ$ | $24 - 12\sqrt3 \approx 3.215$ | the quarter turn | the quarter turn | $0$ |

The turns by $30^\circ$ and $60^\circ$ have the same energy, because a quarter turn changes nothing. At $60^\circ$ the sweep moves the frame to the quarter turn, which is the same frame as the identity.

On a $4 \times 4 \times 4$ grid with fixed identity frames on the boundary and 8 random inner frames (seed 0 in the tests), three sweeps give the measured energies $41.43$, $14.23$, $0.84$ and $0.03$.

## Correctness

The full proof is below. The energy does not change when a frame is replaced by an equal frame $Rg$, so it measures frames, not matrices. At a cell, with the matches of L4 fixed, the energy of its edges is $6d - 2\operatorname{tr}(R_i^{\mathsf T} M)$. Line L6 maximizes the trace over all rotations, so the energy does not rise, and choosing the best matches again can only lower it. So one sweep never increases $E$, and repeated sweeps converge to some value.

What is proved is only this monotone decrease, in exact arithmetic. The code works in floating point, and the tests check each claim to $10^{-9}$. They compare the edge energy with a brute force over the 24 matrices of $O$, check Horn's rotation against random rotations and small turns on 500 random matrices, and check on 12 random grids that every local step does not raise the energy and that each sweep lowers it. A sweep can stop at a local minimum with singular curves inside, so the limit need not be the least energy. For the whole pipeline there is no general guarantee: the field can have singular curves that no hex mesh can have, the integer grid map can fold, and the survey of Pietroni and others lists these as open problems. The quality of the meshes in the published papers is measured on test models, not proved.

## Complexity

A free cell has at most 6 neighbours, L4 tries 24 matrices for each, and L6 works on a fixed $4 \times 4$ matrix. So one sweep takes $O(F)$ time for $F$ free cells and $O(1)$ extra space. The number of sweeps needed is not bounded in general. In a full method, the integer grid map, a mixed integer problem, is the costly step.

## Properties

- **Symmetry built into the energy.** The best match over $O$ makes the energy depend only on the frames, so a quarter turn between two cells costs nothing.
- **Monotone.** Each local update lowers the energy or keeps it, but it can stop in a local minimum.
- **Not exact.** The rotation of L6 comes from an iterative eigen solver in floating point.
- **General output.** A frame field can describe the singular structure of any hex mesh, so the method is not limited to a class of shapes, unlike [sweeping](/hexahedral-sweeping/) or [polycubes](/polycube-hex-meshing/).
- **Over-general.** A smooth field can also have singularities that no hex mesh has, such as a curve where 3 and 5 hexes meet on its two sides.

## Variants and improvements

- **Spherical harmonics.** Huang, Tong, Wei and Bao write a frame as a vector of 9 coefficients, solve a relaxed smooth problem, and project back onto frames.
- **Frames at vertices.** Ray, Sokolov and Lévy put the frames on the vertices of the tetrahedral mesh and make the projection fast.
- **Fixed singularities.** Some methods let the user fix the singular curves first and then compute a field with exactly these singularities.
- **Robust extraction.** Lyon, Bommes and Kobbelt extract the hexes from a map that is only mostly valid.
- **Hex-dominant output.** When the map folds in a few places, some methods keep a hex-dominant mesh with a few other cells there.

## When to use it

Use a frame field method when the hexes must follow curved boundaries or inner features at many angles and some failures are acceptable, as in research codes and for smooth shapes. For a solid with a sweep direction, [sweeping](/hexahedral-sweeping/) is safer. For box-like shapes, a [polycube](/polycube-hex-meshing/) gives a simpler structure. The local sweep on this page is a teaching step and a cheap smoother, not a full field solver.

## Pitfalls

- **Local minima.** Random initial frames can lead to a field with extra singular curves. Start from a good guess, such as the boundary frames spread inward.
- **Non-meshable singularities.** Check the singular curves of the field before the map, and repair them.
- **Ties in L4.** At an angle of $45^\circ$ two matches are equally good. A fixed rule, such as the first in a fixed order, keeps the sweep deterministic.
- **Floating point.** Stop the Jacobi solver with a relative test. An absolute test such as $10^{-15}$ on the squared off-diagonal left eigenvector errors near $10^{-8}$ in the tests.
- **No guarantee of hexes.** Even a good field can give a map that folds, and then the extraction gives no valid hex mesh.

## Implementations

## History

Frame fields grew out of 2D cross fields for quad meshing. In 2011 Huang, Tong, Wei and Bao computed boundary-aligned smooth 3D frame fields with spherical harmonics, and Nieser, Reitebuch and Polthier showed how to turn a frame field into an integer grid map whose level sets give a hex mesh. Li and others repaired singularities in 2012. Ray, Sokolov and Lévy made the field practical in 2016, and Lyon, Bommes and Kobbelt made the extraction robust in the same year. Horn's quaternion method of 1987 for the best rotation is a much older result from photogrammetry.

## References
