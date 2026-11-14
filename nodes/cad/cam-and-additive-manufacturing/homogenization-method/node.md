---
tag: MKGHFA
kind: algorithm
slug: homogenization-method
name: Homogenization method for topology optimization
aliases:
- Bendsoe-Kikuchi method
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Gives each element a periodic cell with a rectangular hole, gets its effective stiffness from the cell problem of homogenization, and optimizes the hole sizes and the cell angle.
solves: [topology-optimization]
model: real-ram
complexity:
  vars: {n: number of elements, b: half bandwidth of the stiffness matrix, N: elements across the cell, g: steps of the table in each width, k: number of iterations}
  time: {table: "O(g^2 N^6)", loop: "O(k n b^2)"}
  space: {extra: "O(n b + N^4)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1988
  people: [Martin P. Bendsøe, Noboru Kikuchi]
  note: Bendsøe and Kikuchi posed topology optimization as the distribution of a composite with rectangular holes, with the effective stiffness from homogenization theory.
prereqs: [topology-optimization, finite-element-method]
see_also: [simp-method, beso-method, density-filtering, level-set-topology-optimization, bilinear-interpolation, gauss-legendre-quadrature, banded-matrix, lagrange-multiplier]
sources:
  - paper: doi:10.1016/0045-7825(88)90086-2
    title: Martin P. Bendsøe and Noboru Kikuchi, Generating optimal topologies in structural design using a homogenization method, Computer Methods in Applied Mechanics and Engineering 71(2), 1988, 197 to 224
    locator: the cell with a rectangular hole, the effective elastic tensor from the cell problem, the rotation of the cell and the optimality criteria update of the hole sizes
  - book: isbn:978-0-387-95298-7
    title: Grégoire Allaire, Shape Optimization by the Homogenization Method, Springer, Applied Mathematical Sciences 146, 2002
    locator: the cell problem, the Wiener bounds, the laminates and the relaxation of the optimal design problem (general locator)
  - book: isbn:978-3-540-42992-0
    title: Martin P. Bendsøe and Ole Sigmund, Topology Optimization, Theory, Methods and Applications, Springer, 2003
    locator: the chapter on the minimum compliance problem and the discussion of microstructures and relaxation
---

The homogenization method was the first method of [topology optimization](/topology-optimization/) as the distribution of material. Bendsøe and Kikuchi (1988) gave every point of the design domain a fine periodic microstructure: a square cell of solid material with a rectangular hole. The two widths of the solid walls and the angle of the cell are the design variables of the point. The stiffness of such a porous material is not the stiffness of the solid times the density: it depends on the shape of the hole and on the direction of the load. Homogenization theory gives it as the solution of a small [finite element](/finite-element-method/) problem on one cell with periodic boundary conditions, the cell problem. The method computes this effective stiffness for a table of hole sizes, then iterates on the full design: solve the model, turn each cell along the flow of the load, and update the hole sizes by optimality criteria. When all composites are allowed, the relaxed design problem has a solution, which the pure 0/1 problem in general does not, and the cells with rectangular holes are a practical family inside that relaxation. The price is that the result is full of gray composite regions. This page uses the scalar form of the model (heat conduction), proves what holds for its cell problem and its steps, and measures the rest.

## In plain words

Instead of asking "is there material here or not", ask "what kind of sponge is here". Each small patch of the part is a sponge with square holes. The holes can be small, so the patch is nearly solid, or large, so it is nearly empty. They can also be long and thin, and then the patch is stiff in one direction and soft in the other, like wood along and across the grain.

First the method works out how stiff each kind of sponge is, once, by testing a single small cell. Then it repeats: load the part, turn the grain of each patch along the path of the load, and make the walls thicker where they work hard and thinner where they do not, keeping the total material fixed.

## The problem

The design domain is a grid of $n$ square elements. Element $e$ carries a cell with solid walls of width $\mu_e$ (along $y$) and $\gamma_e$ (along $x$), so the hole is $(1 - \mu_e) \times (1 - \gamma_e)$ and the density is

$$\rho_e = 1 - (1 - \mu_e)(1 - \gamma_e).$$

The cell is turned by the angle $\theta_e$. The scalar model is heat conduction: the temperature $u$ solves $-\nabla \cdot (B \nabla u) = $ source, with the conductivity tensor $B_e = R(\theta_e)\, A^H(\mu_e, \gamma_e)\, R(\theta_e)^{\mathsf T}$. The goal is to minimize the thermal compliance $c = f^{\mathsf T} u$, the analogue of the compliance of a structure, subject to $\sum_e \rho_e \le V^*$ and $0 \le \mu_e, \gamma_e \le 1$. The solid has conductivity 1 and the hole a small $a_{\text{void}} = 10^{-3}$, so every matrix is positive definite.

**The cell problem.** Let $a$ be the conductivity on the unit cell $Y$, 1 in the solid and $a_{\text{void}}$ in the hole. For each unit vector $e_j$, find a periodic $\chi_j$ with

$$\int_Y a\, (e_j + \nabla \chi_j) \cdot \nabla v = 0 \quad \text{for all periodic } v, \qquad A^H_{ij} = \frac{1}{|Y|} \int_Y a\, (e_i + \nabla \chi_i) \cdot e_j.$$

The function $\chi_j$ is the correction of the field inside the cell when the average gradient is $e_j$, and $A^H$ maps an average gradient to the average flux. The code solves this with bilinear elements on an $N \times N$ grid of the cell, with the nodes on opposite sides identified.

Bendsøe and Kikuchi solved the same problem for linear elasticity. There the unknown is a displacement vector, the effective stiffness is a fourth order tensor, and a 2D cell needs three load cases (two stretches and a shear) instead of two. The steps of the method are the same.

## The algorithm

```pseudo id=main
HOMOGENIZATION(mesh, f, V*, N, g, m, η)
L1  for μ, γ in {0, 1/g, ..., 1}: solve the cell problem on N × N elements; store A11(μ, γ), A22(μ, γ)
L2  μ_e = γ_e ← s with 1 − (1 − s)² = V*/n;  θ_e ← 0
L3  for k = 1 to maxit do
L4      B_e ← R(θ_e) diag(A11, A22)(μ_e, γ_e) R(θ_e)ᵀ        ▷ bilinear interpolation in the table
L5      solve K(B) u = f;  c_k ← fᵀu
L6      θ_e ← main direction of S_e = Σ_g ¼ q_g q_gᵀ with q_g = B_e ∇u at the Gauss points; add π/2 if A22 > A11
L7      ∂c/∂μ_e ← −u_eᵀ K_e(R ∂A/∂μ Rᵀ) u_e, and the same for γ_e
L8      μ, γ ← optimality criteria step with move limit m and power η, bisection on λ so that Σ ρ_e ≤ V*
L9      if no width changed by more than tol then stop
L10 return μ, γ, θ
```

Line L1 is done once, before the loop. The cell is symmetric, so $A^H$ is diagonal in the axes of the cell and $A_{22}(\mu, \gamma) = A_{11}(\gamma, \mu)$. In a periodic cell the place of the hole does not matter, so the code puts it in a corner. Line L4 reads the table by [bilinear interpolation](/bilinear-interpolation/), which also gives the derivatives that line L7 needs.

Line L6 is the angle step. It looks at the flux $q = B \nabla u$ at the four Gauss points of the element and turns the stiffer axis of the cell along the main direction of the flux. Line L8 is the optimality criteria update of the [SIMP page](/simp-method/), applied to both widths: $\mu_e \leftarrow \mu_e \big( -\partial c / \partial \mu_e \,/\, \lambda\, \partial \rho_e / \partial \mu_e \big)^{\eta}$, clipped to $[0, 1]$ and to the move limit, with $\partial \rho / \partial \mu = 1 - \gamma$. The multiplier $\lambda$ is found by bisection on a log scale.

## Example

**A laminate.** A cell made of layers of conductivity 1 and 10, in equal parts, has $A_{11} = 2 / (1 + 1/10) = 20/11 \approx 1.82$ across the layers, the harmonic mean, and $A_{22} = 5.5$ along them, the arithmetic mean. The finite element cell problem gives these values exactly when the layers follow the element edges, and the tests check them in exact rational arithmetic. These two means are also the bounds for every cell made of the same pieces (the Wiener bounds), so a laminate is the stiffest possible material along its layers and the softest across them.

**The table.** With $N = 10$ and $g = 5$, part of the table for $\gamma = 0.4$ is:

| $\mu$ | $\rho$ | $A_{11}$ (across the $\mu$ wall) | $A_{22}$ (along the $\mu$ wall) | arithmetic mean |
|---|---|---|---|---|
| 0 | 0.40 | 0.4006 | 0.0017 | 0.4006 |
| 0.2 | 0.52 | 0.4168 | 0.2505 | 0.5205 |
| 0.4 | 0.64 | 0.4569 | 0.4569 | 0.6404 |
| 0.6 | 0.76 | 0.5212 | 0.6562 | 0.7602 |

At $\mu = 0$ the cell is a stack of layers in $x$, and $A_{11}$ equals the arithmetic mean. With both walls present, the material is clearly softer than its density: at $\rho = 0.64$ the conductivity is 0.457 in both directions. The cell grid matters. For $\mu = \gamma = 0.6$ the value of $A_{11}$ is 0.7272 on $5 \times 5$ elements, 0.7135 on $10 \times 10$ and 0.7083 on $20 \times 20$. A finer grid can only lower it, because the coarse functions are among the fine ones.

**Checkerboards.** A $2 \times 2$ checkerboard with conductivities 1 and 10, one element per square, gives exactly $A = 5.5\, I$, the arithmetic mean, as if the squares were joined in parallel in both directions. The exact value of this checkerboard is $\sqrt{10} \approx 3.162$, a classical result of Keller (1964) and Dykhne (1970). With $2 \times 2$, $4 \times 4$ and $8 \times 8$ elements per square the cell problem gives 4.119, 3.666 and 3.444. This is the checkerboard fault of topology optimization in its simplest form: bilinear elements make a checkerboard look much stiffer than it is.

**A bar.** On a $12 \times 6$ grid, the left edge is held at $u = 0$ and the right edge carries a total load of 1, with volume fraction $0.4$. No design can do better than $F^2 L^2 / (V^*(1 - a_{\text{void}}) + n a_{\text{void}}) = 4.9925$, and a laminate along the bar reaches it. The start, square holes everywhere, has $c = 8.129$. The method stops after 7 iterations with $\mu = 0.4$, $\gamma \approx 0$ and $\theta = \pi/2$ in every element: the same laminate, built from the other wall and turned by a right angle. Its compliance is 4.9946, 0.04% above the bound.

**A heat sink.** On a $20 \times 10$ grid with a uniform heat source and a sink of three nodes in the middle of the left edge, with volume fraction 0.4, the compliance falls from 159,396 at the start to 59,223 after 10 iterations and 58,742 after 60. It fell at every iteration, which is a measurement, not a theorem. The result has 22 solid elements near the sink, 14 empty ones in the far corners, and 164 of the 200 elements are gray, with $0.05 < \rho < 0.95$. With the angle held at 0 the same run ends at 60,363, so turning the cells gains about 3% here.

## Correctness

What is proved in [the correctness proof](proofs/correctness.md), for the scalar model with exact element integrals:

- The cell problem has a solution, unique up to a constant, and $A^H$ is symmetric and equal to a minimum of energy over periodic fields.
- For every direction $\xi$, the harmonic mean $\le \xi \cdot A^H \xi \le$ the arithmetic mean. The upper bound comes from the zero correction and the lower bound from the Cauchy-Schwarz inequality, using that a periodic correction has zero mean gradient.
- A laminate whose layers follow the element edges gives the harmonic mean across and the arithmetic mean along, exactly.
- Refining the cell grid by 2 cannot raise $A^H$, and the one-element checkerboard gives the arithmetic mean.
- For fixed hole sizes, the angle step of line L6 does not raise the compliance. The proof writes the compliance as the least complementary energy over all fluxes in equilibrium, keeps the old flux, and minimizes each element's term over the angle.
- Every design has volume at most $V^*$, and the loop stops.
- For the bar, the bound above holds for every design of the model, and the laminate attains it.

What is not proved: the loop as a whole is not shown to lower the compliance or to converge, because the size step is a fixed point rule. The rectangular hole is also not an optimal microstructure. The optimal composites for compliance are laminates, of rank 1 for the scalar problem with one load and of rank 2 or 3 for elasticity, so the relaxed problem of this page is smaller than the full relaxation.

What the tests check: the laminate formulas and the Wiener bounds on random cells in exact arithmetic, the checkerboard, the symmetry, bounds and monotonicity of the table, the derivatives of line L7 against central differences, the angle step against 64 sampled angles and against the compliance, the bar against its bound, and the heat sink for feasibility.

## Complexity

The table has $(g + 1)^2$ entries, half of them by symmetry, and each is a dense solve with $N^2$ unknowns and two right-hand sides, $O(N^6)$, so it costs $O(g^2 N^6)$. That is about 0.2 s in Python for $N = 10$ and $g = 5$, and it is done once for every problem. With the nodes numbered along the short side, the stiffness matrix of the design is a [banded matrix](/banded-matrix/) with half bandwidth $b = n_y + 2$, so each solve takes $O(n b^2)$. The angle, the derivatives and the 100 steps of the bisection take $O(n)$ each. So $k$ iterations take $O(k n b^2)$. The space is $O(n b)$ for the matrix and $O(N^4)$ for the dense cell matrix. The number of iterations is not bounded by a formula: the bar stopped after 7, and the heat sink was still changing slowly at 60.

## Properties

- **Relaxed.** Allowing all composites removes the lack of optimal designs of the 0/1 problem, which is why the method was a starting point for the theory. The rectangular hole family is a subset of those composites.
- **Gray designs.** Most elements end as composites. A manufacturable part needs a penalty, a threshold, or a way to build the microstructure itself.
- **Anisotropic.** Each element has a direction, and the method uses it: the cells turn along the flow of the load.
- **Exact steps, heuristic loop.** The cell problem, the angle step and the volume are under proof; the convergence of the loop is not.
- **Deterministic.** The result depends only on the input and the parameters.

## Variants and improvements

- **Elasticity.** The original method: three cell load cases in 2D, six in 3D, and a fourth order tensor. The angle is set from the principal directions of the stress or the strain, a rule whose optimality for orthotropic materials Pedersen (1989) analysed.
- **Optimal microstructures.** Replacing the rectangular hole with laminates of rank 2 (or 3 in 3D) gives the full relaxation, where the effective tensor has a closed form and no cell table is needed. Allaire's book develops this approach.
- **Penalized densities.** Replacing the cell by the power law $\rho^p$ gives the [SIMP method](/simp-method/), which is what most codes use today: one variable per element, no table and nearly 0/1 designs.
- **De-homogenization.** Recent work keeps the composite design and turns it into a fine but manufacturable lattice, by projecting the local cell sizes and angles onto a periodic pattern. This brings the method back for parts that are made by additive manufacturing, where fine [infill patterns](/infill-pattern/) can be printed.
- **Filters.** The composite design is less prone to checkerboards than a 0/1 model, but a [density filter](/density-filtering/) is still used for a length scale.

## When to use it

Use it when the result is meant to be a graded or anisotropic material, such as a printed lattice whose cell sizes and directions vary through the part, or when a well posed relaxed problem is needed as a reference for other methods. For a solid part with clean members, [SIMP](/simp-method/), [BESO](/beso-method/) or the [level set method](/level-set-topology-optimization/) is simpler and gives a 0/1 design directly.

## Pitfalls

- **Reading density as stiffness.** A porous cell is softer than its density, often much softer, and the tensor depends on the direction. Only a laminate along its layers reaches the density.
- **Cell grid too coarse.** The finite element cell problem overestimates the stiffness, as the checkerboard and the refinement example show.
- **The angle along the gradient instead of the flux.** For a fixed field, turning the cells along the temperature gradient raises the energy of that field, which is not the same as lowering the compliance. On the heat sink with fixed random hole sizes, that rule made the compliance rise from the second step on, and inside the full loop it made the run diverge. The flux rule of line L6 never does.
- **A hole of full size.** When a wall width reaches 0 or 1, the derivative of the density in the other width can vanish. The code treats that case on its own in the update.
- **Taking the gray result as the part.** The result is a material layout, and turning it into a geometry is a separate step.

## Implementations

## History

The mathematical theory of homogenization grew in the 1970s, with the books of Bensoussan, Lions and Papanicolaou (1978) and Sanchez-Palencia (1980). In optimal design, work by Murat and Tartar, Lurie and Cherkaev, and Kohn and Strang in the late 1970s and the 1980s showed that the 0/1 problem has in general no solution and that composites, in particular laminates, give its relaxation. Bendsøe and Kikuchi (1988) turned this into a practical method for structures: a cell with a rectangular hole, the effective tensor from a cell table, rotation along the principal directions and an optimality criteria update. A year later Bendsøe (1989) proposed the simpler power law model that became the SIMP method, and the homogenization method became mostly a theoretical reference. Allaire (2002) gave a full account with laminates. Pantz and Trabelsi (2008) proposed turning a composite design into a fine geometry, and since the late 2010s this de-homogenization has brought composite designs back for lattices in additive manufacturing.

## References
