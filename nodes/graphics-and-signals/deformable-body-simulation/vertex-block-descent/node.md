---
tag: B1423N
kind: algorithm
slug: vertex-block-descent
name: Vertex block descent
aliases:
- VBD
area: graphics-and-signals/deformable-body-simulation
level: research
summary: Minimize the implicit Euler energy by block coordinate descent over single vertices, each a 3x3 Newton step, in parallel over a graph coloring.
model: real-ram
complexity:
  vars: {n: "the number of free vertices", s: "the number of elements (springs here)", K: "the number of sweeps per step"}
  time: {sweep: "Θ(n + s)", step: "O(K (n + s))"}
  space: {step: "Θ(n + s)"}
properties: {deterministic: true, exact: false, monotone_objective_with_line_search: true, monotone_objective_without_line_search: false, linear_momentum_conserving: false, penetration_free: false}
history:
  year: 2024
  people: [Anka He Chen, Ziheng Liu, Yin Yang, Cem Yuksel]
  note: Chen, Liu, Yang and Yuksel presented vertex block descent at SIGGRAPH 2024 as a GPU friendly solver for the implicit Euler step of cloth and soft bodies.
prereqs: [backward-euler-method, coordinate-descent, newton-method-for-systems, graph-coloring]
see_also: [projective-dynamics, extended-position-based-dynamics, optimization-time-integration, gauss-seidel-method, greedy-coloring, mass-spring-system, chebyshev-iteration, incremental-potential-contact]
sources:
  - paper: doi:10.1145/3658179
    title: "Anka He Chen, Ziheng Liu, Yin Yang and Cem Yuksel, Vertex block descent, ACM Transactions on Graphics 43(4), 2024 (SIGGRAPH 2024)"
    locator: "Section 3 (equations (1) to (3) the objective, equations (7) and (9) the vertex Newton step), Section 3.3 (damping), Section 3.5 (collisions), Section 3.7 (initialization, equation (17)), Section 3.8 (Chebyshev acceleration), Section 3.9 (parallelization by coloring), Section 7 (limitations)"
---

Vertex block descent (VBD) solves the [backward Euler](/backward-euler-method/) step of a deformable body by updating one vertex at a time. Each update keeps all other vertices fixed and takes one Newton step on the energy terms of that vertex, a $3 \times 3$ system in 3D ($2 \times 2$ in the 2D code). Chen, Liu, Yang and Yuksel (2024) run the updates in parallel on a GPU over the classes of a [graph coloring](/graph-coloring/), because vertices of one color share no element and their updates do not interact. The method is [block coordinate descent](/coordinate-descent/) on the backward Euler objective; with a line search no update increases it, and without one, which is the default of the paper, there is no such guarantee.

## In plain words

Picture a cloth as a net of knots joined by springs. The best position of all the knots after one frame is the one that balances inertia against the springs. Finding it for all knots at once means solving one big system. Instead, pick one knot, hold all the others still, and move just this knot to the best place for it. That is a tiny problem. Do this for every knot, and repeat. Knots that share no spring do not affect each other, so you can color the net so that no spring joins two knots of the same color and then move all knots of one color at the same time. Each round brings the net closer to the balanced position.

## The problem

The input is a mesh or a [mass-spring system](/mass-spring-system/) with masses $m_i$, positions $\mathbf x^n$, velocities $\mathbf v^n$, a step $\Delta t$ and elastic energies $E_j$ on elements. The output is the next state of the backward Euler step in variational form,

$$\mathbf x^{n+1} = \arg\min_{\mathbf x} G(\mathbf x), \qquad G(\mathbf x) = \sum_i \frac{m_i}{2\Delta t^2}|\mathbf x_i - \mathbf y_i|^2 + \sum_j E_j(\mathbf x), \qquad \mathbf y = \mathbf x^n + \Delta t\mathbf v^n + \Delta t^2\mathbf g,$$

equations (1) to (3) of the paper, with its $h$ written as $\Delta t$. This is the form that this site also uses for [optimization time integration](/optimization-time-integration/), [projective dynamics](/projective-dynamics/), [incremental potential contact](/incremental-potential-contact/) and [affine body dynamics](/affine-body-dynamics/). The code uses 2D springs $E = \frac{k}{2}(|\mathbf x_a - \mathbf x_b| - r)^2$, $y$ up and $\mathbf g = (0, -9.81)$ m/s²; the paper works with 3D cloth and tetrahedral meshes, and the code is a 2D version.

## The algorithm

```pseudo id=main
VBD-STEP(x, v, colors, Δt, K)
L1  y <- x + Δt v + Δt² g                       ▷ pinned vertices stay
L2  z <- y                                      ▷ initial guess (Section 3.7 discusses others)
L3  repeat K times:
L4      for each color c:
L5          for each vertex i of color c, in parallel:
L6              f_i <- -(m_i/Δt²)(z_i - y_i) - Σ_{j ∋ i} ∂E_j/∂x_i;  H_i <- (m_i/Δt²) I + Σ_{j ∋ i} ∂²E_j/∂x_i²
L7              if |det H_i| > ε: Δx_i <- H_i⁻¹ f_i  (optional backtracking line search) else Δx_i <- 0
L8          z_i <- z_i + Δx_i for every vertex i of color c
L9  v <- (z - x)/Δt;  x <- z
```

**The vertex step (L6, L7).** The terms of $G$ that depend on $\mathbf x_i$ are its inertia term and the elements that touch it. Their gradient and Hessian with respect to $\mathbf x_i$ give the force $\mathbf f_i$ and the matrix $H_i$, and the Newton step solves $H_i\Delta\mathbf x_i = \mathbf f_i$ (equations (7) and (9)). For a spring with length $\ell$ and direction $\mathbf n$, $\partial^2 E/\partial\mathbf x_i^2 = k(\mathbf n\mathbf n^T + (1 - r/\ell)(I - \mathbf n\mathbf n^T))$, which is indefinite when the spring is compressed. The paper does not project $H_i$ to a positive definite matrix. It skips the vertex when $|\det H_i| \le \varepsilon$.

**Line search.** A full Newton step can overshoot or go uphill. The paper makes a backtracking line search on the local energy optional and reports that it costs about 40% more time. The code offers both.

**Coloring (L4, L5).** A vertex update reads only the vertices that share an element with it. A coloring in which no element joins two vertices of one color lets all vertices of a color update at once from the same state, and the result equals updating them one by one (claim 2). The code uses [greedy coloring](/greedy-coloring/). The paper reports 8 colors for a mesh of 3891 vertices (Fig. 8).

**More parts of the paper.** Section 3.3 adds damping to the vertex step (equations (10) and (11)). Section 3.5 handles collisions with penalty energies in the same vertex steps. Section 3.8 accelerates the sweeps by blending iterates with the weights of the Chebyshev semi-iterative method, $\omega_1 = 1$, $\omega_2 = 2/(2 - \rho^2)$, $\omega_n = 4/(4 - \rho^2\omega_{n-1})$, where $\rho$ is an estimated spectral radius. The code leaves these out.

## Example

**One spring by hand.** A vertex of mass 1 at $(1.5, 0)$ is joined to a pin at the origin by a spring with $r = 1$ and $k = 100$, at rest, with $\Delta t = 0.1$ and no gravity. Then $\mathbf y = (1.5, 0)$, $\mathbf f = (-100 \cdot 0.5, 0) = (-50, 0)$ and $H = \operatorname{diag}(100 + 100, 100 + 100 \cdot \frac13)$. The step is $\Delta\mathbf x = (-0.25, 0)$, so the vertex goes to $(1.25, 0)$, the backward Euler value $(1 \cdot 1.5 + 0.01 \cdot 100 \cdot 1)/(1 + 0.01 \cdot 100) = 1.25$. One update is exact here because the energy is quadratic along the spring and the vertex does not move across it.

**Convergence on a hanging cloth (measured).** A cloth of $6 \times 6$ vertices of 0.01 kg with spacing 0.1 m has structural, shear and bending springs with $k = 1000$ N/m (158 springs), and its two top corners are pinned. The greedy coloring uses 7 colors. After 10 steps of $\Delta t = 1/60$ s, the largest entry of $\nabla G$ after $K$ sweeps of one step is

| sweeps $K$ | 1 | 2 | 5 | 10 | 20 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|---|
| largest gradient entry (N) | 1.9 | 1.5 | 1.1 | 0.87 | 0.47 | 0.074 | $3.3 \times 10^{-3}$ | $6.7 \times 10^{-6}$ |

The values with and without the line search agree here, since the line search accepts every full step. The convergence is linear and slow at first.

**A crumpled start (measured).** The same cloth without pins and without gravity starts at 0.4 times its rest size with small random offsets, so most springs are compressed, with $\Delta t = 1/30$ s. The objective starts at $G = 621.4$.

| | after 1 sweep | 10 sweeps | 100 sweeps | 300 sweeps |
|---|---|---|---|---|
| no line search | $5.99 \times 10^{7}$ | $1.18 \times 10^{4}$ | 4067 | 746 |
| line search | 382.9 | 86.0 | 54.89 | 54.78 |

Without the line search the first sweep raises $G$ by a factor of about $10^5$, and $G$ rises in 4 of the 300 sweeps; with it, $G$ falls at every vertex update, as claim 3 proves.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **The local problem (proved).** $G$ equals the local energy of vertex $i$ plus terms without $\mathbf x_i$, so L6 gives the exact gradient and Hessian of $G$ in $\mathbf x_i$. The test checks both against central differences.
2. **Colors (proved).** Updates of vertices that share no element commute, so the parallel updates of a color equal the sequential ones in any order. The test checks this to the last bit. The greedy coloring is proper and uses at most one more color than the largest vertex degree.
3. **Descent with a line search (proved).** With the line search no update increases $G$; with a positive definite $H_i$ the search always finds a decrease. The test checks every color of 60 sweeps on the crumpled cloth.
4. **No guarantee without it (measured).** The crumpled start above raises $G$; the test fixes this case.
5. **Fixed points (proved).** If every $H_i$ is nonsingular, a sweep leaves $\mathbf x$ unchanged exactly when $\nabla G = 0$, the backward Euler equation. Convergence and its rate are not proved; the table measures them, and the test reaches a gradient below $10^{-6}$ after 250 sweeps.
6. **Momentum (proved for the limit, measured otherwise).** A converged step keeps the linear momentum without pins and gravity, but a finite number of sweeps does not. On a free $4 \times 4$ cloth with total mass 0.8 kg and momentum $(0.079, 0.037)$ kg m/s, the drift after 1, 10, 50 and 200 sweeps is 0.051, 0.028, $1.1 \times 10^{-3}$ and $6.4 \times 10^{-9}$ kg m/s.

The tests also check the one spring example, that a vertex with a singular $H_i$ is skipped, and free fall against the symplectic Euler value $-5.3955$ m after 10 steps of $0.1$ s.

## Complexity

A vertex update costs $O(1 + \deg i)$, so a sweep costs $\Theta(n + s)$ and a step $O(K(n + s))$, with $\Theta(n + s)$ memory for the adjacency lists and colors. There is no global matrix and no linear solve. On a GPU the time of a sweep is set by the number of colors and the size of the largest color. The number of sweeps for a given accuracy is a property of the scene.

## Properties

- **Matrix free.** Only $3 \times 3$ systems per vertex; the memory is linear and the work is local.
- **Parallel.** All vertices of a color update at once.
- **Descent only with a line search.** Without it the objective can rise (claim 4). The paper reports good results without it in its scenes; that is a measurement, not a guarantee.
- **Not momentum conserving per sweep.** The step keeps linear momentum only in the limit of many sweeps.
- **Contacts.** Penalty collisions in the paper do not guarantee a result without penetration (Section 7). [Incremental potential contact](/incremental-potential-contact/) gives that guarantee with barriers and continuous collision checks, at a higher cost.
- **Approximate when stopped early.** With few sweeps the step is a partial minimization, which adds numerical damping.

## Variants and improvements

- **Chebyshev acceleration.** Section 3.8 uses the [Chebyshev](/chebyshev-iteration/) weights above to speed up the sweeps.
- **Initialization.** Section 3.7 compares starting guesses, including an adaptive one (equation (17)); a better guess reduces the sweeps needed.
- **Damping.** Section 3.3 adds damping to the vertex step.
- **Relation to other solvers.** [Gauss-Seidel](/gauss-seidel-method/) on the Newton system updates one unknown at a time for a fixed linearization; VBD relinearizes at every vertex update. [XPBD](/extended-position-based-dynamics/) updates one constraint at a time, and [projective dynamics](/projective-dynamics/) alternates local projections with a global solve.

## When to use it

Use VBD for large cloth and soft body scenes on a GPU where a global sparse solve is too slow and the energy is a sum of element energies, such as [mass-spring systems](/mass-spring-system/) or FEM materials. It handles large steps when a line search is used.

Do not use it when a guaranteed descent is needed without the line search, when contact must be free of penetration, or when an accurate solve with few iterations is needed on a very stiff and well connected mesh; use Newton based [optimization time integration](/optimization-time-integration/) or [incremental potential contact](/incremental-potential-contact/) then.

## Pitfalls

- **Indefinite vertex Hessians.** Compressed springs and inverted elements make $H_i$ indefinite; a plain Newton step can go uphill. Use the line search, or make $H_i$ positive definite.
- **Singular vertex Hessians.** A vertex whose $H_i$ is close to singular must be skipped, as in L7, not solved.
- **Coloring errors.** Two vertices of one color that share an element give races on a GPU and a result that depends on timing.
- **Stopping early.** A fixed small number of sweeps makes the cloth softer and more damped than the material.
- **Momentum drift.** Free bodies drift a little with few sweeps (claim 6).

## Implementations

## History

Block coordinate descent and nonlinear Gauss-Seidel, which relax one block of unknowns at a time, are old methods of numerical optimization. Chen, Liu, Yang and Yuksel (2024) applied it to the variational backward Euler step with vertex blocks, a coloring for the GPU, Chebyshev acceleration and penalty collisions, and presented it at SIGGRAPH 2024.

## References
