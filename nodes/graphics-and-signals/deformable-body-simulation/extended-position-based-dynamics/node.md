---
tag: 553NT7
kind: algorithm
slug: extended-position-based-dynamics
name: Extended position based dynamics
aliases:
- XPBD
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Position based dynamics with a compliance and a Lagrange multiplier per constraint, so that the converged stiffness does not depend on the time step or on the sweep count.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of particles", c: "the number of constraints, each on a bounded number of particles", k: "the number of solver sweeps per step"}
  time: {sweep: "Θ(c)", step: "O(n + k c)"}
  space: {step: "O(n + c)"}
properties: {deterministic: true, exact: false, linear_momentum_conserving: true, angular_momentum_conserving: false, backward_euler_for_linear_constraints: true}
history:
  year: 2016
  people: [Miles Macklin, Matthias Müller, Nuttapong Chentanez]
  note: Macklin, Müller and Chentanez presented XPBD at Motion in Games 2016 as a fix for the iteration dependent stiffness of position based dynamics.
prereqs: [position-based-dynamics, backward-euler-method, lagrange-multiplier]
see_also: [small-steps-physics, gauss-seidel-method, quasi-newton-method, newton-method-for-systems, projective-dynamics, vertex-block-descent, optimization-time-integration, fast-mass-spring]
sources:
  - paper: doi:10.1145/2994258.2994272
    title: "Miles Macklin, Matthias Müller and Nuttapong Chentanez, XPBD: position-based simulation of compliant constrained dynamics, Proceedings of the 9th International Conference on Motion in Games (MIG 2016), 49-54, 2016"
    locator: "equations (4) to (12) (the implicit step and its Newton system), equation (18) (the multiplier update), equation (26) (damping), Section 6 (the spring, chain, beam and cloth results)"
  - paper: doi:10.1111/cgf.14105
    title: "Matthias Müller, Miles Macklin, Nuttapong Chentanez, Stefan Jeschke and Tae-Yong Kim, Detailed rigid body simulation with extended position based dynamics, Computer Graphics Forum 39(8), 101-112, 2020"
    locator: "the whole paper (rigid bodies, joints and friction in XPBD)"
---

Extended position based dynamics (XPBD) is [position based dynamics](/position-based-dynamics/) with two additions: each constraint gets a compliance $\alpha$, the inverse of a stiffness, and a [Lagrange multiplier](/lagrange-multiplier/) $\lambda$ that collects its total correction during the step. Macklin, Müller and Chentanez (2016) derived the update as a [Gauss-Seidel](/gauss-seidel-method/) solve of a simplified Newton system of [backward Euler](/backward-euler-method/). When the sweeps converge, a spring of compliance $\alpha$ has the stiffness $1/\alpha$ for any $\Delta t$ and any sweep count, and with $\alpha = 0$ the method is PBD with hard constraints.

## In plain words

PBD fixes each stick of a rope fully, every time it visits it. So more visits make the rope stiffer, even if nothing else changes. XPBD gives each stick a softness number and a running total of how hard it has already pulled in this frame. On each visit the stick asks: given my softness and how hard I already pull, how much more should I pull? The answer gets smaller on every visit, and it settles at the same rope for any number of visits. A soft stick ends up a little longer than its rest length, by the amount its pull and its softness agree on. A stick with softness zero is a rigid stick, as in PBD.

## The problem

The input is a set of particles with positions $\mathbf x_i$, velocities $\mathbf v_i$ and inverse masses $w_i = 1/m_i$ ($w_i = 0$ for a pinned particle), constraints $C_j$ with compliances $\alpha_j \ge 0$, a step $\Delta t$ and a sweep count $k$. The elastic potential of the constraints is

$$U(\mathbf x) = \sum_j \frac{1}{2\alpha_j} C_j(\mathbf x)^2 ,$$

so a distance constraint $C = |\mathbf x_i - \mathbf x_j| - d$ is a spring of stiffness $1/\alpha$. The aim is the backward Euler step for $U$ and gravity. With $\tilde{\mathbf x} = \mathbf x^n + \Delta t \mathbf v^n + \Delta t^2 \mathbf g$ it is a stationary point of $\tfrac12 (\mathbf x - \tilde{\mathbf x})^T M (\mathbf x - \tilde{\mathbf x}) + \Delta t^2 U(\mathbf x)$, the variational form of backward Euler that this site also uses for [optimization time integration](/optimization-time-integration/), [projective dynamics](/projective-dynamics/), [vertex block descent](/vertex-block-descent/), [incremental potential contact](/incremental-potential-contact/) and [affine body dynamics](/affine-body-dynamics/). XPBD gives an approximation of it at the cost of PBD. The page uses 2D, $y$ up and $\mathbf g = (0, -9.81)$ m/s².

## The algorithm

```pseudo id=main
XPBD-STEP(x, v, w, constraints, Δt, k)
L1  for each free particle i: x~_i <- x_i + Δt v_i + Δt² g     ▷ prediction
L2  for each constraint j: λ_j <- 0
L3  p <- x~
L4  repeat k times:
L5      for each constraint C_j in a fixed order, with α~_j = α_j / Δt²:
L6          Δλ <- (-C_j(p) - α~_j λ_j) / (Σ_i w_i |∇_i C_j(p)|² + α~_j)
L7          for each particle i of C_j: p_i <- p_i + w_i ∇_i C_j(p) Δλ
L8          λ_j <- λ_j + Δλ
L9  for each particle i: v_i <- (p_i - x_i) / Δt;  x_i <- p_i
```

**Where L6 comes from.** Write $\lambda_j = -C_j(\mathbf x)/\tilde\alpha_j$. Then the backward Euler step is the pair of equations $M(\mathbf x - \tilde{\mathbf x}) - \nabla \mathbf C(\mathbf x)^T \boldsymbol\lambda = 0$ and $\mathbf C(\mathbf x) + \tilde A \boldsymbol\lambda = 0$ with $\tilde A = \operatorname{diag}(\tilde\alpha_j)$ (equations (4) to (9) of the paper). Newton's method on these equations solves a block system with the matrix $K = M - \sum_j \lambda_j \nabla^2 C_j$ (equation (12)). XPBD makes two simplifications. It replaces $K$ by $M$, which drops the geometric stiffness and gives a [quasi-Newton method](/quasi-newton-method/). It also assumes that the first equation holds at every iterate. What remains is the system $(\nabla\mathbf C\, M^{-1} \nabla\mathbf C^T + \tilde A)\Delta\boldsymbol\lambda = -\mathbf C - \tilde A\boldsymbol\lambda$, and line L6 is one Gauss-Seidel update of its row $j$, with the gradient taken at the current positions (equation (18)). For a distance constraint, $|\nabla_i C| = 1$ and the denominator is $w_i + w_j + \tilde\alpha_j$.

**The multiplier.** The term $\tilde\alpha_j \lambda_j$ in L6 is what PBD lacks. It makes repeated visits to the same constraint converge to $C_j + \tilde\alpha_j \lambda_j = 0$ instead of to $C_j = 0$, so a soft constraint is not made stiffer by more sweeps. The force of the constraint is $\nabla C_j^T \lambda_j / \Delta t^2$, a value that PBD does not give.

**Damping.** Equation (26) of the paper adds Rayleigh damping with a coefficient $\beta_j$: with $\tilde\beta_j = \Delta t^2 \beta_j$ and $\gamma_j = \tilde\alpha_j \tilde\beta_j / \Delta t$, the update becomes $\Delta\lambda = (-C_j - \tilde\alpha_j\lambda_j - \gamma_j \nabla C_j (\mathbf p - \mathbf x^n)) / ((1 + \gamma_j)\, \nabla C_j M^{-1} \nabla C_j^T + \tilde\alpha_j)$. The code leaves damping out.

## Example

**One spring by hand.** A free particle of mass 1 sits at $(1.5, 0)$ at rest, joined to a pin at the origin by a spring of rest length 1 and compliance $\alpha = 0.01$ (stiffness 100). There is no gravity and $\Delta t = 0.1$, so $\tilde\alpha = 1$ and the prediction is $(1.5, 0)$. Line L6 gives $\Delta\lambda = (-0.5 - 0)/(1 + 1) = -0.25$, and L7 moves the particle by $-0.25$ to $1.25$, with the velocity $-2.5$. A second sweep gives $\Delta\lambda = (-0.25 + 0.25)/2 = 0$. Backward Euler for this spring gives $x = (1 \cdot 1.5 + 0.01 \cdot 100 \cdot 1)/(1 + 0.01 \cdot 100) = 1.25$, the same value. PBD with the stiffness $k$ would give $1 + 0.5(1 - k)$ after one sweep, which depends on how $k$ is tuned and not on the step.

**Stretch against sweeps (measured).** A chain of 11 particles of 1 kg, joined by 10 constraints of 0.1 m, is pinned at one end and falls from a horizontal start, with $\Delta t = 1/60$ s. After 300 steps (5 s) the total length exceeds 1 m by

| compliance $\alpha$ | $k = 1$ | 2 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| 0 (PBD) | 11.4% | 5.7% | 2.9% | 1.5% | 0.64% | 0.16% |
| $10^{-5}$ | 12.5% | 6.1% | 3.3% | 1.9% | 1.13% | 0.76% |
| $10^{-4}$ | 24.6% | 7.6% | 6.0% | 5.6% | 5.53% | 5.52% |

With $\alpha = 10^{-4}$ (stiffness $10^4$ N/m per link) the stretch settles near 5.5% from about 10 sweeps on. A chain of these springs hanging at rest would stretch by $\sum_{i=1}^{10} i \cdot 9.81 / 10^4 = 0.054$ m, or 5.4%; the chain here still swings. With $\alpha = 0$ the stretch keeps falling with more sweeps, which is the PBD behavior, and the row is the same as the table on the PBD page.

**Distance from backward Euler (measured).** A chain of 6 particles with $\alpha = 10^{-4}$ swings for 6 steps, then one step is taken from the same state with 500 sweeps and compared with a Newton solve of the backward Euler equations. The largest distance between the two answers is

| $\Delta t$ | 1/30 | 1/60 | 1/120 | 1/240 | 1/480 |
|---|---|---|---|---|---|
| distance (m) | $1.6 \times 10^{-3}$ | $1.7 \times 10^{-4}$ | $1.1 \times 10^{-5}$ | $6.2 \times 10^{-7}$ | $3.6 \times 10^{-8}$ |
| motion in the step (m) | 0.045 | 0.020 | 0.0090 | 0.0043 | 0.0021 |

The gap comes from the second simplification: the gradients turn while the chain swings, so the converged answer is not exactly the backward Euler step. In this run the gap shrinks about 16 times when $\Delta t$ is halved. For a chain that only moves along its own line the gradients do not turn, and the gap is zero (claim 3 below).

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Gauss-Seidel on a simplified Newton system (proved).** Lines L6 to L8 are one Gauss-Seidel update of the Newton system of backward Euler with $K$ replaced by $M$ and the first residual set to zero.
2. **Fixed points (proved).** If the sweeps converge, the limit satisfies $C_j + \tilde\alpha_j \lambda_j = 0$ for every $j$. The other backward Euler equation holds up to a residual that is a sum of gradient changes times multiplier updates, so it is zero when the gradients do not turn.
3. **Exact for linear constraints (proved).** If every constraint is affine on the region of the iterates and every $\alpha_j > 0$, the sweeps converge for any order to the backward Euler step, because they are Gauss-Seidel for a symmetric positive definite system. The test runs a vertical chain against a Newton solve and reaches $10^{-12}$ after 200 sweeps, with the error falling at every count.
4. **One spring (proved).** For one spring on a pinned particle, one sweep gives the backward Euler step $x = (m y + \Delta t^2 k r)/(m + \Delta t^2 k)$ with $k = 1/\alpha$ for every $\Delta t$. The test checks 200 random cases across four step sizes.
5. **Zero compliance is PBD (proved).** With $\alpha_j = 0$, L6 is the PBD projection with the sweep stiffness 1.
6. **Linear momentum (proved).** With translation invariant constraints, no pins and no gravity, the step keeps $\sum m_i \mathbf v_i$. Angular momentum is not kept in general, for the same reason as in PBD.

The tests also check the gradient of the backward Euler objective against central differences, that the constraint forces sum to zero, that the swinging chain of the table is within 1% of the motion from backward Euler and closer at the smaller step, and free fall against the symplectic Euler value $-5.3955$ m after 10 steps of $0.1$ s.

## Complexity

Each update of L6 to L8 costs $O(1)$ for a constraint on a bounded number of particles, so a sweep costs $\Theta(c)$ and a step $O(n + k c)$. The extra memory over PBD is one multiplier per constraint, so the memory is $O(n + c)$. No matrix is built or factored. The number of sweeps needed for a given error is a property of the scene: Gauss-Seidel converges slowly on long chains and on stiff, well connected meshes.

## Properties

- **Stiffness is a material constant when converged.** A converged step gives the spring stiffness $1/\alpha$ independent of $\Delta t$ and $k$ (claims 3 and 4). With few sweeps the material is softer than $1/\alpha$, as the table shows.
- **Approximate backward Euler.** The method inherits the numerical damping of backward Euler, and it adds the gap of the second simplification when constraints turn.
- **Hard constraints.** $\alpha = 0$ is allowed and gives rigid constraints, as in PBD. Then the system has no compliance term; with redundant constraints its matrix is only positive semidefinite, and the convergence proof of claim 3 does not apply.
- **Order dependence.** As in PBD, the result of a finite number of sweeps depends on the constraint order.
- **Momentum.** Linear momentum is kept exactly for translation invariant constraints; angular momentum is not.

## Variants and improvements

- **Small steps.** [Small steps](/small-steps-physics/) use $k = 1$ and divide the frame into many substeps. Macklin et al. (2019) measured lower error for the same cost on chains and cloth.
- **Rigid bodies.** Müller, Macklin, Chentanez, Jeschke and Kim (2020) extended XPBD to rigid bodies with positional and angular constraints, joints and friction (Computer Graphics Forum 39(8)).
- **Jacobi and coloring.** For a GPU, constraints are updated in parallel by averaging or by [graph coloring](/graph-coloring/), as in PBD.
- **Other solvers for the same step.** [Projective dynamics](/projective-dynamics/) solves the same kind of backward Euler step by local projections and a constant global matrix, and [vertex block descent](/vertex-block-descent/) does block coordinate descent over vertices. [Optimization time integration](/optimization-time-integration/) uses Newton's method with a line search, which keeps the geometric stiffness.
- **Mass-spring view.** [Fast mass-spring](/fast-mass-spring/) solves the same backward Euler step for springs with a constant matrix.

## When to use it

Use XPBD when you want the robustness and simple code of PBD, but the stiffness must be set in physical units and must not change with the step or the sweep count, for example cloth, ropes and soft bodies in games and tools. Use $\alpha = 0$ for rigid constraints such as inextensible links and pins. It also gives constraint forces, which PBD does not.

Do not expect a converged backward Euler solution for very stiff, well connected meshes with few sweeps; use substeps or a Newton based solver then.

## Pitfalls

- **Forgetting to reset $\lambda$.** The multipliers start at zero in every step (L2). Keeping them from the last step changes the method.
- **Units.** $\alpha$ is in units of the inverse of the stiffness, for example m/N for a distance constraint. Divide by $\Delta t^2$ to get $\tilde\alpha$; using $\alpha$ directly makes the material depend on $\Delta t$ again.
- **Few sweeps on stiff materials.** With a small $\alpha$ and few sweeps the material is soft, as the table shows. More sweeps or substeps are needed.
- **Mixed compliances.** Very different compliances in one system slow Gauss-Seidel down. Small steps help here.
- **Zero gradients and pinned pairs.** Skip a constraint with a zero gradient or with only pinned particles, as in PBD.

## Implementations

## History

Position based dynamics (Müller, Heidelberger, Hennix and Ratcliff, 2007) had stiffness that changed with the sweep count and the step. Macklin, Müller and Chentanez added the compliance and the multiplier at Motion in Games 2016, and showed results for a spring, a chain, a beam and cloth. Macklin and coauthors then showed in 2019 that substeps with one sweep each reduce the error further, and Müller and coauthors extended the method to rigid bodies in 2020.

## References
