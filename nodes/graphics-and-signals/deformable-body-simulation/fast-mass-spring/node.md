---
tag: CQQNYH
kind: algorithm
slug: fast-mass-spring
name: Fast mass-spring simulation
aliases:
- Liu fast mass-spring
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Solve implicit Euler for mass-spring systems by block coordinate descent that alternates a local spring direction step and a prefactored global solve.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of particles", m: "the number of springs", k: "the number of local and global iterations per step", b: "the half bandwidth of the matrix in the particle order"}
  time: {prefactor: "O(n b^2)", iteration: "Θ(m + n b)", step: "O(k (m + n b))"}
  space: {factor: "O(n b)"}
properties: {deterministic: true, exact: false, monotone_objective: true, momentum_conserving: true, unconditionally_stable: true}
history:
  year: 2013
  people: [Tiantian Liu, Adam W. Bargteil, James F. O'Brien, Ladislav Kavan]
  note: Liu, Bargteil, O'Brien and Kavan wrote each Hooke spring energy as a minimum over spring directions, which turns the implicit Euler step into a block coordinate descent with a constant matrix, at SIGGRAPH Asia 2013.
prereqs: [mass-spring-system, backward-euler-method, cholesky-decomposition]
see_also: [projective-dynamics, baraff-witkin-cloth, position-based-dynamics, optimization-time-integration, coordinate-descent, as-rigid-as-possible-deformation, vertex-block-descent, cloth-simulation]
sources:
  - paper: doi:10.1145/2508363.2508406
    title: "Tiantian Liu, Adam W. Bargteil, James F. O'Brien and Ladislav Kavan, Fast simulation of mass-spring systems, ACM Transactions on Graphics 32(6), 2013"
    locator: "Section 3, equations (1) to (8) (implicit Euler as a minimization), Section 4, the Lemma and equations (9) to (14) (the local and global steps), Section 4.1 (damping and collisions), Section 5, Table 1 and Figure 2 (timings and convergence)"
---

Fast mass-spring simulation solves the [backward Euler](/backward-euler-method/) step of a [mass-spring system](/mass-spring-system/) without a Newton solve. Liu, Bargteil, O'Brien and Kavan (2013) noticed that the energy of a Hooke spring is the smallest squared distance between the spring vector and any vector of the rest length. With the spring directions as extra unknowns, the step becomes a minimization that is easy in each block: the best directions for given positions are a normalization per spring, and the best positions for given directions are one linear solve with a matrix that never changes. The matrix is factored once, so each iteration is cheap. The method converges to the exact implicit Euler solution; a few iterations give a stable and plausible step.

## In plain words

An implicit step asks for the positions at the end of the step that balance the pull of the springs against the motion each particle already has. With stiff springs, finding these positions is a hard nonlinear problem.

The trick is to split each spring into two parts: a direction and a length. If the directions were known, every spring would act like a simple linear rubber band toward a known target, and the positions would come from one linear solve. If the positions were known, the best direction of each spring is just the line between its two ends.

So the method guesses the positions, then finds the directions, then solves for the positions, and repeats. Each round can only lower the quantity the step minimizes. The linear solve uses the same matrix every time, so the computer prepares it once and reuses it.

## The problem

Given positions $\mathbf x_n$, velocities $\mathbf v_n$, masses, springs $(a, b, r, k)$, external forces and a step $h$, find $\mathbf x_{n+1}$ with

$$M (\mathbf x_{n+1} - \mathbf y) = h^2 \big(\mathbf f(\mathbf x_{n+1}) + \mathbf f_{\text{ext}}\big), \qquad \mathbf y = \mathbf x_n + h \mathbf v_n,$$

and $\mathbf v_{n+1} = (\mathbf x_{n+1} - \mathbf x_n)/h$. This is backward Euler for $M \ddot{\mathbf x} = \mathbf f + \mathbf f_{\text{ext}}$. Its solutions are the stationary points of

$$g(\mathbf x) = \tfrac12 (\mathbf x - \mathbf y)^\top M (\mathbf x - \mathbf y) + h^2 \big(E(\mathbf x) - \mathbf x^\top \mathbf f_{\text{ext}}\big), \qquad E(\mathbf x) = \sum \tfrac12 k (|\mathbf x_a - \mathbf x_b| - r)^2 .$$

In [cloth simulation](/cloth-simulation/) the springs are stiff, so an explicit step would need to be tiny, and a Newton step needs a new matrix at each iteration.

## The algorithm

The key fact (Liu et al., Section 4, the Lemma) is

$$(|\mathbf p| - r)^2 = \min_{|\mathbf d| = r} |\mathbf p - \mathbf d|^2 ,$$

with the minimum at $\mathbf d = r \mathbf p / |\mathbf p|$. Put a vector $\mathbf d_i$ of length $r_i$ into each spring term. The objective becomes

$$G(\mathbf x, \mathbf d) = \tfrac12 \mathbf x^\top (M + h^2 L) \mathbf x - h^2 \mathbf x^\top J \mathbf d - \mathbf x^\top (M \mathbf y + h^2 \mathbf f_{\text{ext}}) + \text{const},$$

where $L$ is the graph Laplacian of the springs weighted by $k$, and $J \mathbf d$ puts $+k_i \mathbf d_i$ on one end of spring $i$ and $-k_i \mathbf d_i$ on the other (equations (11) to (14)). Then $g(\mathbf x) = \min_{\mathbf d} G(\mathbf x, \mathbf d)$, and the step minimizes $G$ by turns:

```pseudo id=main
FAST-MASS-SPRING-STEP(x_n, v_n, h)
L1  once: factor A = M + h^2 L by Cholesky                 ▷ A does not depend on the state
L2  y <- x_n + h alpha v_n                                 ▷ alpha = 1 means no damping
L3  x <- y
L4  repeat k times:
L5      for each spring i = (a, b, r): d_i <- r (x_a - x_b) / |x_a - x_b|      ▷ local step
L6      c <- M y + h^2 (J d + f_ext)
L7      x <- the solution of A x = c, one solve per coordinate with the factor   ▷ global step
L8  x_{n+1} <- x, v_{n+1} <- (x - x_n) / h
```

**Local step (L5).** For fixed positions, each $\mathbf d_i$ appears in one term only, and Lemma 1 gives the best one: the current spring direction scaled to the rest length. This is a normalization per spring, cheap and parallel.

**Global step (L6, L7).** For fixed $\mathbf d$, $G$ is a quadratic in $\mathbf x$ with the Hessian $A = M + h^2 L$, which is symmetric positive definite and acts on each coordinate separately. Its factor from line L1 holds while $h$, the masses, the stiffnesses, the springs and the pins stay the same, so each global step is a forward and a backward substitution.

**Pins.** A pinned particle is a constant. Its spring terms add $h^2 k \mathbf x_q$ to the right side at the free end, and its row leaves the matrix.

**Damping and collisions.** Liu et al. (Section 4.1) damp by replacing $\mathbf v_n$ with $\alpha \mathbf v_n$ in $\mathbf y$, with $\alpha$ slightly below 1, a tuning value. They handle collisions outside the solver, by moving positions with a collision method; the code of this page has no collisions.

The code builds $A$ on a 2D grid in row order, so it is banded, and uses a banded Cholesky factor. Liu et al. use a sparse Cholesky factor from a library on 3D meshes.

## Example

**One spring by hand.** One particle of $m = 1$ kg hangs on a horizontal spring of $k = 100$ N/m and rest length 1 m from a pin at the origin, with no gravity. It starts at rest at $x = 1.5$ m, a stretch $u = 0.5$ m, and $h = 0.1$ s, so $\omega h = 1$. Then $\mathbf y = (1.5, 0)$, and the local step gives $\mathbf d = (-1, 0)$ for the spring from the particle to the pin. The global step solves $(1 + 0.01 \cdot 100) x = 1.5 + 0.01 \cdot 100 \cdot 1$, so $x = 1.25$ and $v = -2.5$ m/s. The stretch went from $0.5$ to $0.25$, and the energy went from $\frac12 \cdot 100 \cdot 0.25 = 12.5$ J to $\frac12 (2.5)^2 + \frac12 \cdot 100 \cdot 0.0625 = 6.25$ J, half of it. Backward Euler multiplies the energy by $1/(1 + (\omega h)^2)$ at each step, so the spring stops swinging after a few steps. The step is stable, and stable is not accurate.

**Convergence, measured.** An 8 by 8 grid with spacing $0.1$ m, particles of $0.01$ kg, structural springs of $10^4$ N/m and shear springs of $5 \times 10^3$ N/m (210 springs) hangs from two corners with $h = 1/30$ s. For the first step from rest, the relative error $(g(\mathbf x_j) - g^\star)/(g(\mathbf x_0) - g^\star)$, with $g^\star$ from Newton's method, is

| iterations | 1 | 2 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| relative error | 0.377 | 0.208 | 0.053 | 0.0068 | 1.2e-4 | 1.1e-9 |

The decrease is linear, as Liu et al. report in their Figure 2. Here $\omega = \sqrt{k/m} = 1000$ rad/s and $\omega h \approx 33$, so symplectic Euler with the same step blows up, and the test checks that.

**Timings, measured by the authors.** Liu et al. (Table 1) simulate a curtain of 6561 vertices and 32158 springs with $h = 33$ ms and 10 iterations per frame, at 5 ms per iteration on one core of an Intel i7-3720QM, with a factorization of 113 ms done once.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **The splitting is exact (proved).** $g(\mathbf x) = \min_{\mathbf d} G(\mathbf x, \mathbf d)$, by the Lemma.
2. **Descent (proved).** Each local and global step does not increase $g$, because each block step minimizes $G$ in its block.
3. **Fixed points are solutions (proved).** A fixed point of the iteration with no spring of zero length is a stationary point of $g$, so it solves the backward Euler step. The objective is not convex, so the limit is a stationary point, not always the global minimum. The linear rate is a measurement.
4. **Momentum (proved).** Without pins, every global step keeps $\sum m_i \mathbf x_i = \sum m_i \mathbf y_i + h^2 \sum \mathbf f_{\text{ext}}$, after any number of iterations. The test checks the momentum to $10^{-10}$ relative after 1 and 3 iterations per step for 100 steps.
5. **The constant matrix (proved).** $A$ is symmetric positive definite and does not depend on the state, so one factorization serves all steps.

The tests check the Lemma against a scan of directions, the banded factor against a dense solve, the forces against central differences of the energy and zero force at rest and after a rotation, the descent at every iteration, the converged step against Newton's method to $10^{-9}$ m, the momentum, the exact energy factor of the oscillator, and the bounded run at $\omega h = 33$.

## Complexity

The factorization is done once. For a banded matrix of half bandwidth $b$ it costs $O(n b^2)$ time and $O(n b)$ space; for a 2D grid of width $w$ in row order, $b = w + 1$ with shear springs, so $b = \Theta(\sqrt n)$. One iteration costs $\Theta(m)$ for the local step and the right side, and $\Theta(n b)$ for the two substitutions per coordinate. A step with $k$ iterations costs $O(k (m + n b))$. With a fill-reducing order and a sparse factor, the solve costs the number of nonzeros of the factor. A Newton step instead needs a new matrix and a new factorization or an iterative solve at every iteration.

## Properties

- **Stable for every step size.** Every iteration lowers $g$, and the global step is a well-posed solve. Large steps lose energy, as backward Euler does.
- **Monotone.** The objective never increases, so the iteration needs no line search.
- **Constant matrix.** The system matrix changes only when $h$, a mass, a stiffness, a spring or a pin changes. Tearing or changing the step means a new factorization.
- **Linear convergence.** Early iterations make large progress; later ones are slow. Newton's method converges faster near the solution but costs much more per iteration.
- **Momentum conserving.** Without pins and with $\alpha = 1$, linear momentum changes only by the external forces.
- **Springs only.** The splitting needs an energy that is a squared distance to a set. Bending, volume and other energies need the generalization of [projective dynamics](/projective-dynamics/).

## Variants and improvements

- **Projective dynamics.** Bouaziz et al. (2014) generalized the local step to the projection onto any constraint set, which covers triangles, tetrahedra, bending and volume. See [projective dynamics](/projective-dynamics/).
- **Acceleration.** Later work speeds up the linear convergence, for example with Chebyshev or Anderson acceleration of the iterates.
- **Warm start.** Starting from $\mathbf y$ is the choice of the paper. Starting from an extrapolation of the last steps can save iterations.
- **Newton after descent.** For an exact solution, a few iterations give a good start for Newton's method on the same objective, as in [optimization time integration](/optimization-time-integration/). Liu et al. (Section 5) observed that their iterations beat damped Newton steps early on.
- **Other energies by descent.** [Vertex block descent](/vertex-block-descent/) also lowers the backward Euler objective by blocks, one vertex at a time, with no global solve.

## When to use it

Use it for stiff mass-spring cloth, hair or soft bodies with a fixed step and fixed connectivity, where a stable and plausible step at a fixed cost matters more than an exact solution: games, previews and real-time tools.

Do not use it when the connectivity changes every step, as in tearing or cutting, because every change needs a new factorization. When an accurate solution of the implicit step is needed, finish with Newton's method. For energies that are not springs, use projective dynamics or a Newton-type solver.

## Pitfalls

- **Few iterations are not the solution.** With a fixed small number of iterations the answer is not the implicit Euler solution. In practice the cloth then looks softer than its springs; the amount depends on the scene and the step, and it is an observation, not a bound.
- **Zero-length springs.** The local step divides by the spring length. A spring that collapses has no direction; the code then picks any direction of the right length, which is a minimizer too.
- **Changing the step.** Changing $h$ changes $A$. A variable step needs a new factorization, which removes the main gain.
- **Collisions in the solve.** A collision handled by forces would change the matrix. Handle contact outside the solve, as the authors do, or add it as a constraint in projective dynamics.
- **Damping by $\alpha$.** The ether drag also slows rigid motion, including free fall, because it scales the whole velocity.

## Implementations

## History

Tiantian Liu, Adam W. Bargteil, James F. O'Brien and Ladislav Kavan presented the method at SIGGRAPH Asia 2013. The local and global structure came from as-rigid-as-possible shape deformation, where Sorkine and Alexa (2007) had alternated rotations and positions. Liu et al. saw that a spring direction plays the role of a rotation, and that the implicit Euler objective fits the same scheme. One year later Bouaziz, Martin, Liu, Kavan and Pauly generalized it to projective dynamics, which became a standard solver for real-time deformable bodies.

## References
