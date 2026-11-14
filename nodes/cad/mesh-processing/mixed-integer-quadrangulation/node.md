---
tag: SKTZEV
kind: algorithm
slug: mixed-integer-quadrangulation
name: Mixed-integer quadrangulation
aliases:
- MIQ
area: cad/mesh-processing
level: research
summary: Bommes, Zimmer and Kobbelt's quad remeshing that aligns a parameterization with a smooth cross field and rounds its singularities and seams to integers.
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of integer variables}
  time: {greedy_dense: O(k n^3), greedy_nested_dissection: O(k n^(3/2))}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2009
  people: [David Bommes, Henrik Zimmer, Leif Kobbelt]
  note: Bommes, Zimmer and Kobbelt presented MIQ at SIGGRAPH 2009. Integer-grid maps by Bommes and coauthors in 2013 added constraints that prevent fold-overs.
prereqs: [mixed-integer-programming, least-squares-problem, cotangent-laplacian]
see_also: [least-squares-conformal-maps, mesh-parameterization, closest-vector-problem, gauss-seidel-method, isotropic-remeshing, spanning-tree, np-hard, mesh-segmentation]
sources:
  - paper: doi:10.1145/1531326.1531383
    title: David Bommes, Henrik Zimmer and Leif Kobbelt, Mixed-integer quadrangulation, ACM Transactions on Graphics 28(3), 2009, Article 77
    locator: the cross field with integer period jumps, the global parameterization with integer transition functions and integer singularities, and the greedy rounding solver
  - paper: doi:10.1145/2461912.2462014
    title: David Bommes, Marcel Campen, Hans-Christian Ebke, Pierre Alliez and Leif Kobbelt, Integer-grid maps for reliable quad meshing, ACM Transactions on Graphics 32(4), 2013, Article 98
    locator: the conditions under which a parameterization defines a valid quad mesh, and the constraints that prevent fold-overs
  - paper: doi:10.1111/cgf.12014
    title: David Bommes, Bruno Lévy, Nico Pietroni, Enrico Puppo, Claudio Silva, Marco Tarini and Denis Zorin, Quad-mesh generation and processing, a survey, Computer Graphics Forum 32(6), 2013, 51 to 76
    locator: the section on parameterization-based quad meshing and its integer constraints
---

Mixed-integer quadrangulation, MIQ, turns a triangle mesh into a mesh of quadrilaterals whose edges follow the principal directions and feature lines of the shape. It works in three stages. It computes a smooth *cross field*, four directions at right angles on each triangle, aligned with the curvature and the features. It computes a global parameterization $(u, v)$ whose gradients follow the cross field, with a scale $h$ for the edge length. And it reads the quads off the integer iso-lines $u \in \mathbb{Z}$ and $v \in \mathbb{Z}$. The iso-lines only close up into a quad mesh if the singular vertices of the field map to integer points and the seams of the cut mesh are crossed by integer jumps. These are integer constraints on a quadratic energy, a mixed-integer problem. MIQ solves it with *greedy rounding*: round one integer variable at a time, the one closest to an integer, and solve the rest again. This page explains the full method and gives code only for the rounding step on a toy grid, where it can be checked exactly; the cross field, the seams and the extraction are not in the code.

## In plain words

To cover a curved shape with square tiles, first draw on it at every point the two directions the tiles should follow. Then give every point two numbers, like the street and avenue numbers of a city grid, so that the numbers grow along those directions at a steady rate.

The tile edges are where a number is a whole number. For the tiles to fit, some special points must sit exactly on whole numbers, and where the grid is cut open to lie flat, the numbers on the two sides must differ by whole numbers.

Asking for whole numbers makes the problem much harder. The method first finds the best answer with any numbers. Then it fixes one number at a time to the nearest whole number, picking the one that is closest already, and improves the rest.

## The problem

The input is a triangle mesh with faces oriented so that the outward normal follows the right-hand rule, a target edge length $h$, and optionally feature curves. The output is a mesh of quadrilaterals, with a few vertices of valence other than 4, whose edges are about $h$ long and follow the principal curvature directions and the features. In the parameterization stage the task is: find $(u, v)$ on a cut of the mesh into a disk that minimizes

$$E(u, v) = \sum_T A_T \left( \lVert h \nabla u_T - \mathbf{d}_T \rVert^2 + \lVert h \nabla v_T - \mathbf{d}_T^{\perp} \rVert^2 \right),$$

where $\mathbf{d}_T$ is a direction of the cross field on $T$, subject to: the values on the two sides of a seam differ by a rotation by a multiple of $90°$ and a translation by an integer vector; each singular vertex maps to an integer point; and each feature curve lies on an integer iso-line.

## The algorithm

The full method:

1. **Cross field.** Choose on each triangle an angle $\theta_T$, with integer *period jumps* $p_{ij}$ across each edge, which say how many quarter turns the cross turns between two triangles. Minimize the smoothness energy $\sum_{ij} (\theta_i + \kappa_{ij} + \tfrac{\pi}{2} p_{ij} - \theta_j)^2$, where $\kappa_{ij}$ is the angle between the two triangle frames, with $\theta$ fixed on feature edges. Most $p_{ij}$ are set to 0 on a [spanning tree](/spanning-tree/) of the dual graph; the rest are integers found by greedy rounding.
2. **Cut graph.** Cut the mesh along a tree of edges through all singular vertices, so that it becomes a disk.
3. **Parameterization.** Minimize $E(u, v)$ with the integer constraints, again by greedy rounding. A stiffening loop raises the weight of triangles that come out distorted or flipped and solves again.
4. **Extraction.** Trace the integer iso-lines of $(u, v)$ over the triangles and across the seams, and build the quad mesh from their crossings.

The rounding solver for "minimize a convex quadratic $E(x)$ where the variables in $I$ must be integers", which steps 1 and 3 share:

```pseudo id=main
GREEDY-ROUND(E, I, pins)
L1  x ← the minimizer of E with the pins held          ▷ the relaxed problem
L2  while some variable of I is not fixed do
L3      k ← the unfixed variable of I with x_k closest to an integer
L4      fix x_k ← round(x_k)
L5      x ← the minimizer of E with all fixed variables held
L6  return x
```

The code of this page is a toy for this solver. It takes one coordinate $u$ on a grid of vertices with columns at positions $x_i$. Each edge asks for $u_b - u_a = t_{ab}$, with $t$ equal to $h$ times the step in $x$ plus a small change per edge, a guiding field that is not quite integrable. Each feature column must lie on one integer iso-line $u = k$, so the column is one integer variable. The energy is $\sum (u_b - u_a - t_{ab})^2$, a finite difference version of $E$. All arithmetic is exact. The toy has no cross field, no seam and no singularity.

**Degenerate cases.** Ties in L3 are broken by the smallest index. If the term graph is connected and at least one variable is pinned, every solve in L1 and L5 has a unique solution, see the proof; without a pin the energy is unchanged by adding a constant, and the system is singular. In the full method, a period jump or a seam translation that is rounded wrongly can force fold-overs that no later step removes.

## Example

Take a grid of 3 columns at $x = 0, 2, 7/2$ and 2 rows, with $h = 9/5$ and no change to the targets, so each horizontal edge asks for $h$ times its length: $t = 18/5$ and $27/10$. All three columns are features, and the column at $x = 0$ is pinned to $u = 0$. With $a$ and $b$ the values of the other two columns, $E(a, b) = 2(a - 18/5)^2 + 2(b - a - 27/10)^2$.

| step | value |
|---|---|
| L1 | $a = 18/5 = 3.6$, $b = 63/10 = 6.3$, $E = 0$ |
| L3 | $b$ is $3/10$ from 6, $a$ is $2/5$ from 4, so $b$ is first |
| L4 to L5 | $b = 6$, then $a = 69/20 = 3.45$ |
| L3 to L5 | $a = 3$ |
| L6 | $(a, b) = (3, 6)$, $E = 9/10$ |
| round all at once | $(4, 6)$, $E = 13/10$ |
| best integer point | $(4, 7)$, $E = 1/2$ |

Greedy rounding is better than rounding everything at once, but it misses the optimum. Fixing $b = 6$ first pulled $a$ down below $3.5$, and the choice could not be undone. On 40 random toy grids with up to 3 integer variables, greedy rounding matched the best integer point in a box around the relaxed solution in 35 cases and was better than rounding all at once in 9. These numbers are measurements on the tests of the page, not theorems.

**When the arithmetic is floating point.** The toy is exact, so the choice in L3 is exact. With floats, two variables at nearly the same distance from an integer can be ordered either way by rounding errors in the solve, and a value near $k + 1/2$ can round to either side; both change the result, not only its accuracy. The full method has a second problem: the iso-lines are traced in floating point, and whether an integer line crosses a triangle, or which side of a seam a crossing lies on, is a sign test of the kind of the [orientation test](/orientation-test/). Near a vertex of the parameterization these signs come from [catastrophic cancellation](/catastrophic-cancellation/), and extraction code has to make consistent decisions, for example with [exact predicates](/shewchuk-expansion-sum/) on the $(u, v)$ values, to avoid holes in the quad mesh. This is the [robustness problem](/geometric-robustness-problem/) of geometry.

## Correctness

On the toy, the energy with at least one fixed variable has a positive definite matrix, because the term graph is connected, so every solve has one exact solution. Each round fixes one more integer variable and never changes a fixed one, so the loop stops after as many rounds as there are integer variables, with every one of them an integer. The relaxed energy is a lower bound and every rounded solution an upper bound on the best integer energy. If the relaxed solution is already integral, greedy rounding returns it. The example shows that greedy rounding is not optimal. The full proof is below. For the full method there is no guarantee: the result can have fold-overs, which makes the extracted quad mesh invalid in those regions.

## Complexity

The relaxed problem is a sparse positive definite system with $O(n)$ unknowns. Greedy rounding solves it once per integer variable, $k$ times. With dense elimination, as in the code of this page, that is $O(k n^3)$ time; with a sparse factorization and [nested dissection](/nested-dissection/), $O(k n^{3/2})$. The integer variables are the singular vertices, the seam translations and the feature lines, so $k$ is much smaller than $n$, but $k$ global solves can still be slow on big meshes. To save time, MIQ updates the solution after a rounding by local [Gauss-Seidel](/gauss-seidel-method/) sweeps near the rounded variable and uses a full solve when the local update is not enough; the code of this page does not do this and solves the whole system each time, so the page gives no measured speed-up. Exact optimization is hopeless in general: minimizing a positive definite quadratic over integer points is the [closest vector problem](/closest-vector-problem/), which is [NP-hard](/np-hard/).

## Properties

- **Heuristic.** Greedy rounding gives a feasible integer solution but no bound on how far it is from the optimum.
- **Aligned.** The quads follow the cross field, so they follow curvature and features.
- **Global.** One parameterization covers the whole surface, with singularities where the cross field needs them.
- **Not guaranteed valid.** Fold-overs in the parameterization give degenerate or missing quads.
- **Deterministic.** The rounding order is fixed by the values and the tie rule.

## Variants and improvements

- **Rounding all at once.** Faster, but worse: in the example it gives $13/10$ against $9/10$.
- **Exact mixed-integer solvers.** Branch and bound on the integer variables gives the optimum for small problems, see [mixed-integer programming](/mixed-integer-programming/). It is too slow for meshes with hundreds of singularities.
- **Integer-grid maps (Bommes and coauthors 2013).** State the conditions under which a parameterization defines a valid quad mesh and add convex constraints that prevent fold-overs, which makes the result reliable at a higher cost.
- **QuadCover (Kälberer, Nieser and Polthier 2007).** An earlier global method for the same problem, with a cross field and integer constraints, that first makes the field integrable.
- **Field and parameterization in one.** Later methods change the cross field during rounding, or simplify the layout of singularities, so that fewer integer constraints conflict.

## When to use it

Use it to turn a scanned or triangulated model into a quad mesh for subdivision surfaces, spline fitting or animation, where edge flow along curvature and features matters. Check the result for flipped parameter triangles and repair or re-run with stiffening, or use an integer-grid map method if validity must be guaranteed. For a quick uniform triangle mesh, [isotropic remeshing](/isotropic-remeshing/) is simpler.

## Pitfalls

- **Greedy is not optimal.** The order of rounding matters, and an early choice cannot be undone. The example shows a gap of almost a factor of 2.
- **Fold-overs.** The energy does not forbid flipped triangles in $(u, v)$; then the iso-lines cross in a tangle and the extraction fails there.
- **Scale $h$ too large.** If $h$ is large compared to the distance between singularities, rounding puts two singularities on the same integer point, which collapses quads.
- **Feature conflicts.** Two feature lines that must lie on integer iso-lines at a distance that is not an integer multiple of $h$ force distortion between them.
- **Seams in floats.** Tracing iso-lines across seams needs consistent decisions on both sides, or the quad mesh gets holes.

## Implementations

## History

Felix Kälberer, Matthias Nieser and Konrad Polthier gave QuadCover in 2007, a global parameterization method for quad meshing based on a cross field. David Bommes, Henrik Zimmer and Leif Kobbelt presented mixed-integer quadrangulation at SIGGRAPH 2009. Their key step was to treat the period jumps of the cross field and the integer constraints of the parameterization as variables of one mixed-integer problem each, solved by greedy rounding, with feature alignment and an adaptive scale. In 2013 Bommes, Campen, Ebke, Alliez and Kobbelt gave integer-grid maps, which state when a parameterization gives a valid quad mesh and how to enforce it. MIQ is a standard reference method for quad remeshing.

## References
