---
tag: R4RWDE
kind: technique
slug: small-steps-physics
name: Small steps in physics simulation
aliases:
- substepping XPBD
area: graphics-and-signals/deformable-body-simulation
level: research
summary: Split each frame into many substeps with one XPBD iteration each instead of one step with many iterations; in the paper's tests this gives a much smaller error for the same cost.
prereqs: [extended-position-based-dynamics, symplectic-euler-method, gauss-seidel-method]
see_also: [position-based-dynamics, verlet-integration, jacobi-method, cloth-simulation, position-based-fluids, rigid-body-simulation-problem, shake-constraint-algorithm, vertex-block-descent]
sources:
  - paper: doi:10.1145/3309486.3340247
    title: "Miles Macklin, Kier Storey, Michelle Lu, Pierre Terdiman, Nuttapong Chentanez, Stefan Jeschke and Matthias Müller, Small steps in physics simulation, Proceedings of the ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA 2019)"
    locator: "Algorithm 1 (the substep loop), equation (7) (the XPBD update), equation (8) (damping), Section 4.2 (collisions once per frame, equation (10), and friction, equations (11) and (12)), Section 6.1 (the chain with mass ratio 1:100000), Section 7 (limitations)"
  - paper: doi:10.1111/cgf.14105
    title: "Matthias Müller, Miles Macklin, Nuttapong Chentanez, Stefan Jeschke and Tae-Yong Kim, Detailed rigid body simulation with extended position based dynamics, Computer Graphics Forum 39(8), 2020, 101 to 112"
    locator: "the substep loop for rigid bodies with one iteration per substep (general locator)"
---

Small steps is a way to spend the work of a constraint solver. A simulation with [XPBD](/extended-position-based-dynamics/) usually takes one time step per frame and runs many [Gauss-Seidel](/gauss-seidel-method/) iterations over the constraints. Macklin, Storey, Lu, Terdiman, Chentanez, Jeschke and Müller (2019) split the frame instead into $n$ substeps of length $h = \Delta t/n$ and run one iteration in each. For the same number of constraint sweeps per frame, their measurements show a much smaller constraint error. A heuristic explanation is that a short substep starts closer to the solution, so one iteration is enough.

## In plain words

Imagine a chain that must keep the length of each link. The solver moves the beads to fix the links, one link at a time. If you take one big step and then fix the links many times, each pass fixes one link but breaks its neighbors a little, and the errors creep slowly through the chain. If you take many tiny steps instead and fix each link once per step, the beads never move far from a good state, so there is little to fix. The work is the same in both cases, but the tiny steps give a chain that stretches much less.

## When it applies

- **Constraint solvers with local iterations.** The idea is for [position based dynamics](/position-based-dynamics/) and XPBD, where one iteration is cheap and its convergence over many iterations is slow.
- **Stiff constraints and high mass ratios.** Gauss-Seidel converges slowly on long chains and with heavy bodies hanging from light ones; small steps reduce this error the most (measured below and in Section 6.1 of the paper).
- **Explicit prediction.** Each substep starts with an explicit [symplectic Euler](/symplectic-euler-method/) prediction. Smaller steps make it more accurate, so the error in time falls as well.
- **Cheap collision detection per frame.** Section 4.2 of the paper finds contact candidates once per frame and reuses them in all substeps; this keeps the cost of the substeps close to the cost of the iterations they replace.

## The template

```pseudo id=main
SMALL-STEPS-FRAME(x, v, constraints, Δt, n)
L1  h <- Δt / n
L2  repeat n times:
L3      v <- v + h f_ext / m                       ▷ for each free particle
L4      p <- x;  x <- x + h v
L5      λ <- 0                                      ▷ the multipliers restart in each substep
L6      one iteration over the constraints j:
L7          Δλ_j <- (-C_j(x) - α̃_j λ_j) / (∇C_j M⁻¹ ∇C_jᵀ + α̃_j),  α̃_j = α_j / h²
L8          x <- x + M⁻¹ ∇C_jᵀ Δλ_j;  λ_j <- λ_j + Δλ_j
L9      v <- (x - p) / h
```

L7 is equation (7) of the paper. With one iteration and $\lambda_j = 0$ the term $\tilde\alpha_j\lambda_j$ is zero, so the update is the plain XPBD projection with compliance. The code runs L6 for a given number of iterations so that it can compare both ways of spending a fixed budget. It is a 2D chain of particles with the first particle pinned.

**One constraint, one iteration (proved).** For a single distance constraint with $\alpha = 0$, one iteration of L7 and L8 sets the distance exactly to the rest length along the current direction, so more iterations change nothing; only more substeps reduce the time error. The test checks this.

**Why it works (heuristic).** In a substep of length $h$ the prediction moves each particle by $O(h)$ from a state that satisfied the constraints after the last substep, so the violation that the solver has to remove is small, and one Gauss-Seidel sweep removes most of it. With many iterations in one large step the solver must instead spread a large correction through the whole chain, which takes a number of sweeps that grows with the chain length and the mass ratio.

**Order (measured).** Section 7 of the paper notes that the velocity is first order in $h$. On the pendulum below, the position error after 1 s falls by 10 for each factor 10 in $n$.

## Classic examples

**A heavy chain (measured).** A chain of 20 particles with spacing 0.1 m hangs from its first particle, starts horizontal at rest, and falls under gravity for 60 frames of $1/60$ s, with $\alpha = 0$. The budget is 100 constraint sweeps per frame. The table gives the largest relative stretch $|\ell - r|/r$ at the end.

| last particle mass / other masses | 100 iterations, 1 substep | 10 iterations, 10 substeps | 1 iteration, 100 substeps |
|---|---|---|---|
| 1 | $3.9 \times 10^{-3}$ | $7.1 \times 10^{-4}$ | $8.2 \times 10^{-5}$ |
| 1000 | 0.77 | 0.072 | $8.0 \times 10^{-3}$ |
| 100000 | 1.89 | 1.72 | 0.80 |

With equal masses, 1 iteration in each of $n = 10$, $100$ and $1000$ substeps gives the stretch $1.0 \times 10^{-2}$, $8.2 \times 10^{-5}$ and $8.3 \times 10^{-7}$: about 100 times smaller for each factor 10. The paper reports for its chain of 20 particles with the mass ratio 1:100000 an error of 322.1 m with 100 iterations and 3.2 m with 100 substeps (Section 6.1). With the mass ratio 100000 neither choice holds the chain in the code, which shows that small steps reduce but do not remove the difficulty.

**A pendulum against a reference (measured).** A particle on a rigid rod of length 1 m starts horizontal. A classical Runge-Kutta solve of $\ddot\theta = -g\cos\theta$ with 200000 steps gives the reference position after 1 s. With 60 frames of $1/60$ s and 1 iteration, the position error is 0.23, 0.027, $2.8 \times 10^{-3}$ and $2.8 \times 10^{-4}$ m for $n = 1, 10, 100, 1000$ substeps, first order in $h$. With $n = 1$ and 1, 10, 100 or 1000 iterations the error stays 0.23 m, because one iteration already solves the single constraint.

**Rigid bodies.** Müller, Macklin, Chentanez, Jeschke and Kim (2020) use the same loop for rigid bodies with joints and contacts, with one iteration per substep.

**Cloth and fluids.** The same loop applies to [cloth simulation](/cloth-simulation/) and to [position based fluids](/position-based-fluids/), where each substep also re-evaluates the density constraints.

## Variations

- **Several iterations per substep.** Any split of a budget $N = nk$ into $n$ substeps and $k$ iterations is possible; the table shows the error between the two ends.
- **Jacobi iterations.** A [Jacobi](/jacobi-method/) update of all constraints at once is easier to run in parallel than Gauss-Seidel; with small steps the slower convergence per sweep matters less.
- **Damping.** Equation (8) of the paper adds damping per substep.
- **Collisions and friction.** Section 4.2 detects contact candidates once per frame with an enlarged bound and handles them in every substep, with a clamp for depenetration (equation (10)) and friction (equations (11) and (12)).
- **Other integrators.** The same substep loop with [Verlet integration](/verlet-integration/) prediction and a projection is used in older position based codes.

## Pitfalls

- **Floating point.** Very small $h$ gives small position changes that single precision cannot represent well; Section 7 of the paper names this limit.
- **Collision detection per substep.** Running full collision detection in every substep removes most of the gain; detect once per frame and reuse the candidates.
- **First order.** Small steps make each step cheaper and better solved, but the time integration stays first order (Section 7).
- **High mass ratios.** At a ratio of $10^5$ even 100 substeps leave a large error (the table); the remaining error needs more substeps or a direct solver.
- **Constraint energy.** With $\alpha = 0$ the constraint projection removes energy at every substep; the dissipation falls with $h$ but does not vanish.

## Exercises

1. For a single distance constraint with $\alpha = 0$, show that one iteration of L7 and L8 makes the distance equal to the rest length.
2. With one iteration and $\lambda = 0$, show that L7 is the same for XPBD and for small steps with compliance $\alpha/h^2$.
3. For a particle in free fall, compute the position after one frame of $\Delta t$ split into $n$ substeps, and show that the error against the exact value $-\frac12 g\Delta t^2$ is $-\frac{g\Delta t^2}{2n}$.
4. Measure the stretch of the heavy chain for the splits $N = nk = 100$ with $n = 1, 2, 5, 10, 20, 50, 100$ and plot it against $n$.
5. Explain why the cost of the collision detection decides whether small steps pay off, and estimate the cost of a frame with detection once per frame and once per substep.

## References
