---
tag: NBWGAF
kind: algorithm
slug: projective-dynamics
name: Projective dynamics
aliases:
- projective implicit dynamics
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Solve implicit Euler by alternating local projections of elements onto constraint sets and a global linear solve with a constant prefactored matrix.
model: real-ram
complexity:
  vars: {n: "the number of free vertices", T: "the number of elements", K: "the number of local and global iterations per step", z: "the number of nonzeros of the Cholesky factor"}
  time: {setup: "O(n^3)", iteration: "Θ(T + z)", step: "O(K (T + z))"}
  space: {step: "O(n + T + z)"}
properties: {deterministic: true, exact: false, monotone_objective: true, constant_system_matrix: true, linear_momentum_conserving: true}
history:
  year: 2014
  people: [Sofien Bouaziz, Sebastian Martin, Tiantian Liu, Ladislav Kavan, Mark Pauly]
  note: Bouaziz, Martin, Liu, Kavan and Pauly presented projective dynamics at SIGGRAPH 2014. It generalized the local and global solver of fast mass-spring simulation (Liu, Bargteil, O'Brien and Kavan, 2013) to many kinds of constraints.
prereqs: [backward-euler-method, cholesky-decomposition, deformation-gradient]
see_also: [fast-mass-spring, extended-position-based-dynamics, vertex-block-descent, optimization-time-integration, as-rigid-as-possible-deformation, corotational-fem, admm, chebyshev-iteration]
sources:
  - paper: doi:10.1145/2601097.2601116
    title: "Sofien Bouaziz, Sebastian Martin, Tiantian Liu, Ladislav Kavan and Mark Pauly, Projective dynamics: fusing constraint projections for fast simulation, ACM Transactions on Graphics 33(4), article 154, 2014 (SIGGRAPH 2014)"
    locator: "the whole paper (the variational implicit Euler step, the projective energies, the local and global solver and the constraint types)"
---

Projective dynamics (PD) takes a [backward Euler](/backward-euler-method/) step of a deformable body by minimizing the inertia term plus a sum of energies of a special form: the squared distance of each element from a constraint set, such as the set of rotations. Bouaziz, Martin, Liu, Kavan and Pauly (2014) solve this minimization by alternating two steps. The local step projects every element onto its set, independently and in parallel. The global step solves a linear system whose matrix never changes, so it is factored once by [Cholesky decomposition](/cholesky-decomposition/). Each pair of steps never increases the objective, which makes the method robust at large time steps, but it converges only linearly.

## In plain words

Think of a sheet made of small triangles. Each triangle wants to be a turned copy of its rest shape. First let the sheet fly freely for one frame. Then repeat two moves. In the first move, look at each triangle alone and find the turned copy of its rest shape that is closest to it; this is quick and every triangle can do it at the same time. In the second move, find the positions of all corners that best agree with all these copies at once and with where the free flight wanted them. This is one linear system, and it is the same system in every frame, so you prepare it once and then each solve is cheap. Each round makes the total mismatch smaller or keeps it the same.

## The problem

The input is a mesh with lumped vertex masses $M$, rest shape, positions $\mathbf x^n$, velocities $\mathbf v^n$, a step $\Delta t$ and a set of elements, each with a weight $w_t$ and a constraint set $\mathcal C_t$. The output is the next state of the backward Euler step in variational form,

$$\mathbf x^{n+1} = \arg\min_{\mathbf x}\ \frac{1}{2\Delta t^2}(\mathbf x - \mathbf y)^T M (\mathbf x - \mathbf y) + \sum_t \frac{w_t}{2}\, \min_{\mathbf p_t \in \mathcal C_t} |A_t S_t \mathbf x - B_t \mathbf p_t|^2, \qquad \mathbf y = \mathbf x^n + \Delta t\mathbf v^n + \Delta t^2 \mathbf g,$$

the same form that this site uses for [XPBD](/extended-position-based-dynamics/), [optimization time integration](/optimization-time-integration/), [vertex block descent](/vertex-block-descent/), [incremental potential contact](/incremental-potential-contact/) and [affine body dynamics](/affine-body-dynamics/). $S_t$ selects the vertices of element $t$, and $A_t$, $B_t$ are constant matrices. For the strain energy used here, $A_t S_t \mathbf x$ is the [deformation gradient](/deformation-gradient/) $F_t$, $B_t$ is the identity and $\mathcal C_t$ is the set of rotations, so the element energy is $\frac{w_t}{2}\operatorname{dist}(F_t, SO(2))^2$ with $w_t = k \cdot \text{area}_t$. This is the energy of [as-rigid-as-possible](/as-rigid-as-possible-deformation/) deformation. The page uses 2D triangles, $y$ up and $\mathbf g = (0, -9.81)$ m/s²; the paper works with 3D meshes and many constraint types, and the code is a 2D version.

## The algorithm

```pseudo id=main
PD-STEP(x, v, Δt, K)
L1  (once) L <- M/Δt² + Σ_t w_t S_tᵀ A_tᵀ A_t S_t;  factor L = C Cᵀ
L2  y <- x + Δt v + Δt² g                           ▷ pinned vertices stay
L3  z <- y
L4  repeat K times:
L5      for each element t: p_t <- projection of A_t S_t z onto C_t      ▷ local, parallel
L6      solve L z = M y/Δt² + Σ_t w_t S_tᵀ A_tᵀ B_t p_t with the factor C  ▷ global
L7  v <- (z - x)/Δt;  x <- z
```

**Local step (L5).** For the strain energy, the projection of $F_t$ onto the rotations is the rotation factor of its polar decomposition. In 2D it is the rotation by $\theta = \operatorname{atan2}(f_{10} - f_{01}, f_{00} + f_{11})$, which the shared `polar` helper computes. It is always a rotation, also for an inverted triangle. Other constraint sets have other projections: an interval of lengths for springs, an interval of areas or volumes, or a plane for a collision.

**Global step (L6).** With the projections fixed, the objective is a quadratic in $\mathbf x$ whose Hessian $L$ is the matrix of L1. $L$ does not depend on $\mathbf x$ or on the projections, and in 2D or 3D it is the same for each coordinate, so a step solves two (or three) systems with one factor. Pinned vertices are removed from the unknowns, and their terms move to the right side. The paper uses a sparse Cholesky factor; the code uses a dense one, which is fine for the small meshes of the tests.

**Why it descends.** Write the objective as $g(\mathbf x) = \min_{\mathbf p} h(\mathbf x, \mathbf p)$. The local step minimizes $h$ over $\mathbf p$ and the global step minimizes it over $\mathbf x$, so each step can only lower $h$, and $g(\mathbf x_{k+1}) \le h(\mathbf x_{k+1}, \mathbf p_k) \le h(\mathbf x_k, \mathbf p_k) = g(\mathbf x_k)$. This is block coordinate descent on the pair $(\mathbf x, \mathbf p)$.

## Example

**One triangle by hand.** The rest triangle is $(0, 0)$, $(1, 0)$, $(0, 1)$ with the first two corners pinned. With density 6 the free corner has mass $m = 1$, and with $k = 200$ the weight is $w = 200 \cdot 0.5 = 100$. Take $\Delta t = 0.1$, no gravity, and the free corner at rest at $(0, 1.5)$. The deformation gradient is $F = \operatorname{diag}(1, 1.5)$, so the local step gives $R = I$. The global step for the free corner is $(m/\Delta t^2 + w)\mathbf x = (m/\Delta t^2)\mathbf y + w(0, 1)$, that is $200\,\mathbf x = 100\,(0, 1.5) + 100\,(0, 1)$, so $\mathbf x = (0, 1.25)$ with the velocity $(0, -2.5)$. Now $F = \operatorname{diag}(1, 1.25)$ and $R = I$ again, so further iterations change nothing. Backward Euler for the energy $\frac{w}{2}(s - 1)^2$ of the height $s$ gives $100(s - 1.5) + 100(s - 1) = 0$, the same $s = 1.25$.

**Convergence on a cantilever (measured).** A plate of $6 \times 3$ vertices with spacing 0.1 m and density 1 is pinned at its left column and falls under gravity with $\Delta t = 1/30$ s. After 5 steps, one step is solved with 2000 iterations to get the reference value $g^*$, and the gap $g(\mathbf x_K) - g^*$ after $K$ iterations is

| stiffness $k$ | $K = 1$ | 2 | 5 | 10 | 20 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|---|
| 10 | $3.6 \times 10^{-4}$ | $9.6 \times 10^{-5}$ | $3.7 \times 10^{-6}$ | $2.9 \times 10^{-8}$ | $2.1 \times 10^{-12}$ | 0 | 0 | 0 |
| 100 | $1.5 \times 10^{-3}$ | $3.7 \times 10^{-4}$ | $1.6 \times 10^{-5}$ | $2.4 \times 10^{-6}$ | $1.5 \times 10^{-7}$ | $3.2 \times 10^{-11}$ | $4 \times 10^{-17}$ | $2 \times 10^{-17}$ |
| 1000 | $1.5 \times 10^{-2}$ | $4.7 \times 10^{-3}$ | $4.5 \times 10^{-4}$ | $1.2 \times 10^{-4}$ | $4.1 \times 10^{-5}$ | $1.9 \times 10^{-6}$ | $1.2 \times 10^{-8}$ | $4.6 \times 10^{-13}$ |

The gap falls at every iteration, as the descent argument requires. It falls more slowly for the stiffer plate, where the elastic part dominates $M/\Delta t^2$ in $L$. After 2000 iterations the largest entry of the gradient is below $2 \times 10^{-13}$ in all three rows.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Exact subproblems (proved).** The local step gives the best rotation of each element, and the global step gives the unique minimizer for fixed rotations, because $L$ is symmetric positive definite.
2. **Constant matrix (proved).** $L$ depends only on the masses, $\Delta t$, the weights and the rest shape, and it is the same for every coordinate.
3. **Monotone descent (proved).** Each iteration lowers the objective by at least $\frac12|\mathbf x_k - \mathbf x_{k+1}|_L^2$. The test checks that the objective never increases over 30 iterations for a soft and a stiff plate.
4. **Limit points are backward Euler steps (proved).** The steps go to zero, and every limit point where all best rotations are unique has zero gradient, so it satisfies the backward Euler equation. The test reaches a gradient below $10^{-10}$ after 300 iterations, and it checks the gradient formula against central differences.
5. **Linear momentum (proved).** With no pins and no gravity, every global step keeps $\sum m_v \mathbf x_v = \sum m_v \mathbf y_v$, so a step keeps the linear momentum for any number of iterations.
6. **Rigid motions (proved).** The energy is zero on rotated and moved copies of the rest shape, and an unstressed body falls by symplectic Euler, $-5.3955$ m after 10 steps of $0.1$ s.

The test also checks the Cholesky solver against an LU solve. The rate of convergence is not proved; the table measures it.

## Complexity

The setup assembles $L$ in $O(T)$ and factors it once. With a sparse factor that has $z$ nonzeros, an iteration costs $\Theta(T)$ for the local step, which is parallel over the elements, and $\Theta(T + z)$ for the right side and the triangular solves. A step with $K$ iterations costs $O(K(T + z))$. The factor must be recomputed when $\Delta t$, a weight or the set of pinned vertices changes. The dense factor of the code costs $O(n^3)$ once and $O(n^2)$ per solve.

## Properties

- **Robust.** The objective never increases, so a step cannot blow up, at any $\Delta t$. With few iterations the answer is a partial minimization, which adds damping; it is stable, not accurate.
- **Linear convergence.** The method is a fixed point iteration that converges slowly for stiff materials, as the table shows. It is often stopped after a fixed number of iterations.
- **Restricted energies.** Only energies that are squared distances to constraint sets fit the form. General hyperelastic materials such as [neo-Hookean](/neo-hookean-model/) need other methods.
- **Constant matrix.** Changing contacts, pins or stiffness need a new factorization, or must be handled in the local step.
- **Momentum.** Linear momentum is kept for every iteration count without pins and external forces.

## Variants and improvements

- **Fast mass-spring.** [Fast mass-spring](/fast-mass-spring/) is the special case of springs, where the local step projects each spring onto its rest length.
- **Chebyshev acceleration.** Wang (2015) accelerated the iterations with a [Chebyshev](/chebyshev-iteration/) semi-iterative method, which also works for position based solvers.
- **Quasi-Newton.** Liu, Bouaziz and Kavan (2017) viewed the global matrix as an approximate Hessian and used it as the starting matrix of a quasi-Newton method, which allows general hyperelastic materials.
- **ADMM.** Overby, Brown, Li and Narain (2017) wrote the same split as [ADMM](/admm/), which also allows general materials and hard constraints.
- **Vertex block descent.** [Vertex block descent](/vertex-block-descent/) minimizes the same objective by Newton steps on single vertices, with no global solve.
- **Shape matching.** The local step is the same best rotation as in [meshless shape matching](/meshless-shape-matching/) and [corotational FEM](/corotational-fem/).

## When to use it

Use projective dynamics for interactive simulation of cloth, soft bodies and rods with as-rigid-as-possible type energies, when the mesh and the pins do not change often and robustness at large steps matters more than an exact solution. It is a good fit when a sparse Cholesky factor can be reused for many steps.

Do not use it for general nonlinear materials or for very stiff objects where many iterations would be needed; use Newton based [optimization time integration](/optimization-time-integration/) then. Contact that changes every step does not fit the constant matrix well.

## Pitfalls

- **Few iterations look soft.** With a fixed small iteration count, stiff materials look softer and more damped than the material law says.
- **Changing the step size.** $L$ contains $M/\Delta t^2$, so a new $\Delta t$ needs a new factor.
- **Pins in the matrix.** Remove pinned vertices from the unknowns, or add stiff attachment constraints; both change $L$ and need a new factor when the pins change.
- **Degenerate elements.** A triangle with zero rest area has no deformation gradient. A deformation gradient with $f_{00} + f_{11} = f_{10} - f_{01} = 0$ has no unique best rotation.
- **Stopping test.** Monotone descent does not bound the error after a given number of iterations. Use the gradient norm if accuracy matters.

## Implementations

## History

Liu, Bargteil, O'Brien and Kavan (2013) showed that the implicit Euler step of a mass-spring system can be solved by alternating spring projections and a solve with a constant matrix. Bouaziz, Martin, Liu, Kavan and Pauly (2014) generalized this to projective dynamics with many constraint types. Wang (2015) added Chebyshev acceleration, and Liu, Bouaziz and Kavan (2017) and Overby, Brown, Li and Narain (2017) extended the method to general materials with quasi-Newton and ADMM views.

## References
