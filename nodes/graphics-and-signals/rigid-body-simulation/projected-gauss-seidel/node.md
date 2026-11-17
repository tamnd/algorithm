---
tag: MA63NH
kind: algorithm
slug: projected-gauss-seidel
name: Projected Gauss-Seidel
aliases:
- PGS
- sequential impulses
- projected Gauss-Seidel solver
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Solve a contact problem by sweeping over constraints, solving each for its impulse alone and clamping it to its bounds, for a fixed number of sweeps.
solves: [rigid-body-simulation-problem]
model: real-ram
complexity:
  vars: {n: the number of constraint rows, K: the number of sweeps, z: the number of nonzero entries of A, m: the number of bodies}
  time: {matrix: O(K z), matrix_free_pairwise: O(K n)}
  space: {matrix: O(n + z), matrix_free: O(n + m)}
properties: {deterministic: true, online: false, recursive: false, in_place: true}
history:
  year: 2005
  people: [Erin Catto]
  note: Projected iterative methods for symmetric linear complementarity problems come from mathematical programming. Catto (2005) used projected Gauss-Seidel with cached impulses as the contact solver of a game engine and later reframed it as sequential impulses.
prereqs: [gauss-seidel-method, collision-impulse, coulomb-friction-law, positive-definite-matrix, kkt-conditions]
see_also: [baraff-contact-force-algorithm, shock-propagation, baumgarte-stabilization, linear-complementarity-problem, successive-over-relaxation, coordinate-descent, impulse-based-simulation, stewart-trinkle-time-stepping]
sources:
  - url: https://box2d.org/files/ErinCatto_IterativeDynamics_GDC2005.pdf
    title: "Erin Catto, Iterative Dynamics with Temporal Coherence, Game Developers Conference, 2005"
    locator: "Section 3.5 (bounds on each multiplier), Section 4.3 (friction bounded by a constant), Section 7 (Algorithms 3 and 4, the mixed LCP in 7.3), Section 8 (contact caching) and Section 9 (box stacking and mass ratios)"
  - url: https://box2d.org/posts/2024/02/solver2d/
    title: "Erin Catto, Solver2D, Box2D blog, February 2024"
    locator: "the section on PGS, which reframes it as sequential impulses and clamps the accumulated impulse"
  - book: isbn:9780898716863
    title: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, SIAM Classics in Applied Mathematics, 2009 (first edition Academic Press, 1992)"
    locator: the chapter on iterative methods for the LCP
  - paper: doi:10.1145/1243980.1243986
    title: "Kenny Erleben, Velocity-based shock propagation for multibody dynamics animation, ACM Transactions on Graphics 26(2), article 12, 2007"
    locator: the iterative complementarity solver for velocity-based multibody dynamics
---

Projected Gauss-Seidel (PGS) computes contact and joint impulses for one time step of a [rigid body simulation](/rigid-body-simulation-problem/). It visits the constraint rows one at a time. For each row, it solves for the impulse that would make that row exactly satisfied if the other impulses stayed fixed, and then it clamps the impulse to its bounds: a normal impulse must not pull, and a friction impulse must stay inside its limit. It repeats these sweeps a fixed number of times. When it applies each change to the body velocities at once, it is called sequential impulses, and it is the usual contact solver of game physics engines.

## In plain words

Several boxes touch each other and the floor. Each touching point needs a push that stops the boxes from moving into each other. The pushes depend on each other: a push at one point changes the motion at the points nearby.

The method takes the touching points one at a time. At each point, it asks what push would stop the boxes at that point, if all other pushes stayed as they are. If that push would pull instead of push, it uses no push. A friction push is limited in the same way. Then it goes to the next point. One pass over all points does not make every point correct, because later pushes change the earlier points. So it makes several passes. Each pass makes the answer better. A game stops after a fixed number of passes, so the cost of each frame is known.

## The problem

There are $n$ constraint rows. Row $i$ has a Jacobian row $J_i$, so that $J_i v$ is the relative velocity along that row for the body velocities $v$; for a contact normal $n$ from $B$ to $A$, $J_i v = n \cdot (v_A(p) - v_B(p))$, which is positive when the bodies separate. An impulse $\lambda_i$ on row $i$ changes the velocities by $M^{-1} J_i^T \lambda_i$. With the velocities $v^0$ before the solve,

$$w = A \lambda + b, \qquad A = J M^{-1} J^T, \qquad b = J v^0 + \text{bias},$$

is the vector of row velocities after the impulses. The bias carries restitution or position correction, for example [Baumgarte stabilization](/baumgarte-stabilization/). Each row has bounds $lo_i \le \lambda_i \le hi_i$: $[0, \infty)$ for a contact normal, $(-\infty, \infty)$ for a joint, and $[-\mu \lambda_n, \mu \lambda_n]$ for a friction row in the box model of [Coulomb friction](/coulomb-friction-law/). The task is to find $\lambda$ with

$$lo \le \lambda \le hi, \quad w_i = 0 \text{ if } lo_i < \lambda_i < hi_i, \quad w_i \ge 0 \text{ if } \lambda_i = lo_i, \quad w_i \le 0 \text{ if } \lambda_i = hi_i.$$

This is a box-constrained (mixed) [linear complementarity problem](/linear-complementarity-problem/) (Catto, Section 7.3). For contact normals alone it is the LCP $\lambda \ge 0$, $w \ge 0$, $\lambda^T w = 0$ at the velocity level. $A$ is symmetric and positive semidefinite; it is singular when there are redundant contacts, such as four corners of a box on the floor.

## The algorithm

```pseudo id=main
PGS(A, b, bounds, λ0, K)
L1  λ ← λ0                                ▷ zero, or the impulses of the last step
L2  for k ← 1 to K
L3    for i ← 1 to n
L4      r ← b_i + Σ_j A_ij λ_j             ▷ the current velocity of row i
L5      (lo, hi) ← BOUNDS(i, λ)            ▷ fixed, or ±μ λ_normal for friction
L6      λ_i ← clamp(λ_i - r / A_ii, lo, hi)  ▷ clamp the total, not the change
L7  return λ
```

Line L6 is one Gauss-Seidel step for row $i$ of $A \lambda = -b$, followed by a projection onto the bounds of that row. It is the exact minimizer of $q(\lambda) = \tfrac12 \lambda^T A \lambda + b^T \lambda$ over $\lambda_i$ alone, so PGS is [coordinate descent](/coordinate-descent/) on $q$ over the box.

**Sequential impulses.** The matrix $A$ is never formed. Keep the body velocities $v$, which always equal $v^0 + M^{-1} J^T \lambda$. Then line L4 is $r = J_i v + \text{bias}_i$, $A_{ii} = J_i M^{-1} J_i^T$ is the effective mass of the row, and after line L6 the change $(\lambda_i^{new} - \lambda_i^{old}) J_i^T$ is applied to the two bodies of the row as an impulse. Each row touches two bodies, so one update costs $O(1)$. This is Catto's Algorithm 4, which keeps $a = M^{-1} J^T \lambda$ and applies only "the actual increment" after the clamp; in exact arithmetic it gives the same iterates as the matrix version.

## Example

A 2D box of mass 1 with sides 2 and 1 ($I = 5/12$) falls flat onto the ground at $1$ m/s and lands on its two bottom corners, at $x = -1$ and $x = 1$. With $e = 0$ and no friction, $b = (-1, -1)$ and

$$A = \begin{pmatrix} 17/5 & -7/5 \\ -7/5 & 17/5 \end{pmatrix}.$$

The exact answer is $\lambda = (1/2, 1/2)$: the box stops, without spin. A push at one corner turns the box and drives the other corner down ($A_{12} < 0$).

| sweep | $\lambda_1$ | $\lambda_2$ | error of $\lambda_2$ |
|---|---|---|---|
| 1 | $5/17$ | $120/289$ | $-49/578$ |
| 2 | $2285/4913$ | $40560/83521$ | $-49/578 \cdot 49/289$ |
| $k$ | | | $-49/578 \cdot (49/289)^{k-1}$ |

After one sweep, the box still moves down at $84/289$ m/s and turns at $84/289$ rad/s, the order effect shown on the [collision impulse](/collision-impulse/) page. Each further sweep multiplies the error of both impulses by exactly $(A_{12}/A_{11})^2 = 49/289 \approx 0.17$, so about 8 sweeps reduce it below $10^{-6}$.

**Tall stacks converge slowly.** A column of $N$ boxes of mass 1 rests on the ground. After the gravity step all boxes move down at $g \Delta t$ with $\Delta t = 1/60$, so only the ground row has $b \ne 0$, and the exact impulses are $(N - k) g \Delta t$ for the row under box $k$. Starting from zero, the number of sweeps until every impulse is within 1% of its exact value is a measurement:

| boxes $N$ | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| rows from the bottom up | 1 | 7 | 47 | 192 | 776 |
| rows from the top down | 1 | 8 | 51 | 201 | 795 |

The count grows about as $2N^2$ in this test, and the row order matters little. So with a budget of 10 sweeps from a cold start, the impulses of a tall stack stay too small, and the stack sinks. Warm starting and [shock propagation](/shock-propagation/) are the usual remedies.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows:

- **Termination.** The loops run $K n$ updates, whatever the input.
- **Each update is exact for its row.** Line L6 minimizes $q$ over $\lambda_i$ within its bounds, and the new $\lambda_i$ satisfies the box condition of row $i$. The [KKT conditions](/kkt-conditions/) of $\min q$ over the box are exactly the box conditions of all rows.
- **Sufficient decrease.** Each update lowers $q$ by at least $\tfrac12 A_{ii} \delta^2$, where $\delta$ is the change of $\lambda_i$.
- **Convergence.** For a symmetric [positive definite](/positive-definite-matrix/) $A$ and fixed bounds, the iterates converge to the unique solution. Catto (Section 7.2) cites Cottle, Pang and Stone for this fact.
- **Sequential impulses compute the same iterates** as the matrix version, by the invariant $v = v^0 + M^{-1} J^T \lambda$.
- **Redundant contacts.** For a positive semidefinite $A$, all solutions have the same row velocities $w$, although the impulses are not unique.

Not proved: convergence for a singular $A$, convergence with friction bounds $\pm\mu\lambda_n$ (the bounds move with $\lambda_n$, so the argument of the proof does not apply), and any rate of convergence beyond the exact two-contact example.

## Complexity

One update reads row $i$ of $A$, so a sweep costs $O(z)$ for $z$ nonzero entries of $A$, and $K$ sweeps cost $O(K z)$. In the matrix-free form, each row touches at most two bodies, so an update is $O(1)$ and a sweep is $O(n)$, with $O(n + m)$ memory for $n$ rows and $m$ bodies; Catto gives $O(s)$ time per iteration and $O(s + n)$ storage for $s$ constraints and $n$ bodies. The number of sweeps needed for a given accuracy depends on the matrix: it is small for loosely coupled contacts and grows with stack height and mass ratios, as the table above shows. In practice $K$ is fixed (Catto uses 10 iterations in his stacking test), so the cost per frame is predictable and the accuracy is not.

## Properties

- Simple: a few lines per constraint type, and joints, contacts, motors and limits all fit the same bounds scheme (Catto, Section 3.5).
- Matrix-free and cache friendly in the sequential impulse form.
- The result depends on the order of the rows after a finite number of sweeps.
- Never pulls at a contact, at every iterate, because every update clamps.
- Not exact after $K$ sweeps: the remaining error shows up as slow sinking or jitter.
- Handles redundant contacts without special code; a pivoting method needs care there.

## Variants and improvements

- **Warm starting.** Start from the impulses of the previous step, matched by contact ids (Catto, Section 8). This is a heuristic: it helps when the contacts change little between frames. In Catto's tests, a stack of three boxes fell without caching, and a stack of ten boxes was stable with it (Section 9.1).
- **Friction models.** Catto 2005 bounds the friction impulse by a constant, $\mu m_c g$ per contact (Section 4.3), which keeps the bounds fixed. Later engines use $\pm \mu \lambda_n$ with the current normal impulse, which follows Coulomb's law more closely but loses the convergence proof.
- **Relaxation.** Multiply the step of line L6 by a factor $\omega \in (0, 2)$, as in [successive over-relaxation](/successive-over-relaxation/).
- **Projected Jacobi.** Update all rows from the same old $\lambda$. It is parallel, but it converges under stronger conditions on $A$ than Gauss-Seidel, and it is often damped (see the [Jacobi method](/jacobi-method/)).
- **Graph coloring.** Rows that share no body do not affect each other's update, so a color class can be updated in parallel. The result is that of a sweep in the order of the colors.
- **Exact methods.** [Baraff's pivoting algorithm](/baraff-contact-force-algorithm/) solves the frictionless problem exactly, at a higher cost per step.
- **Stacking.** [Shock propagation](/shock-propagation/) solves the levels of a stack from the ground up and freezes the lower levels.

## When to use it

Use it for interactive simulations with many contacts and a fixed time budget per frame: games, virtual reality, and robotics simulators that value speed. It accepts joints and contacts in one loop, and warm starting makes it strong for scenes that change little between frames. Do not use it when you need accurate forces, very stiff chains, or large mass ratios: in Catto's test of two stacked boxes, the stack was stable until the density of the lower box was lowered to 3% of the upper one, and below that the top box bounced and slid off (Section 9.2). A direct or pivoting solver, or a reduced coordinate method for chains, is better there.

## Pitfalls

- **Clamp the total, not the increment.** A 2D box of mass 1 and sides 2 and 1 falls at $10$ m/s and spins clockwise at $36$ rad/s onto three contacts at $x = -1, 0, 1$, so $b = (26, -10, -46)$. Correct PGS gives $(0, 10, 180/17)$ after one sweep and the exact $(0, 0, 230/17)$ after the second: the middle impulse must fall back to zero. A solver that clamps each change at zero can never lower an impulse. It stops at $(0, 10, 180/17)$, where the middle contact pushes with $10$ while it separates at $180/17$ m/s.
- **Read the effective mass from the right rows.** $A_{ii} = J_i M^{-1} J_i^T$ must include the angular terms of both bodies. A wrong $A_{ii}$ changes the fixed point.
- **Few sweeps means soft contacts.** With a fixed $K$, tall stacks sink slowly and heavy bodies on light ones push through. Check the residual $w$ if accuracy matters.
- **Bias adds energy.** A position bias in $b$ makes the contacts push bodies apart faster than they met. See [Baumgarte stabilization](/baumgarte-stabilization/) for split impulses.
- **Restitution in the bias.** Compute the restitution target from the velocity before the solve, not from the current iterate, or the bounce changes with $K$.
- **Robotics conventions.** Pages on [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/) use $z$ up; this page uses $y$ up.

## Implementations

## History

Projected iterative methods such as projected Gauss-Seidel and projected SOR for symmetric linear complementarity problems are classical in mathematical programming; Cottle, Pang and Stone (1992) treat them. Catto (2005) used projected Gauss-Seidel with contact caching as the solver of a velocity-level time stepping scheme for games, and later reframed the same loop as sequential impulses, which apply one row impulse at a time to the bodies. Erleben (2007) studied velocity-based iterative complementarity solvers for stacking, together with shock propagation.

## References
