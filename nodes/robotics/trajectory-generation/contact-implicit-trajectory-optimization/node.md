---
tag: YCM0CN
kind: algorithm
slug: contact-implicit-trajectory-optimization
name: Contact-implicit trajectory optimization
aliases:
- trajectory optimization through contact
area: robotics/trajectory-generation
level: research
summary: "Posa's method that adds contact forces as variables with complementarity constraints, so the optimizer chooses when contacts happen."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {N: "the number of time steps", T: "the total number of Newton steps over all stages"}
  time: {worst: O(T N^3)}
  space: {extra: O(N^2)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [trajectory-optimization, stewart-trinkle-time-stepping, barrier-method]
see_also: [rigid-contact-complementarity, painleve-paradox, manipulator-equation, friction-cone, interior-point-method, kkt-conditions, control-limited-ddp, sequential-convex-trajectory-optimization]
sources:
  - paper: doi:10.1177/0278364913506757
    title: "Michael Posa, Cecilia Cantu and Russ Tedrake, A direct method for trajectory optimization of rigid bodies through contact, The International Journal of Robotics Research 33(1), 2014, 69-81"
    locator: "the whole paper (contact forces as decision variables with complementarity constraints)"
---

Contact-implicit trajectory optimization plans motions in which contacts start and stop, such as walking, jumping and pushing, without fixing in advance when each contact happens. Posa, Cantu and Tedrake made the contact forces decision variables next to the states and controls, and wrote the physics of rigid contact as complementarity constraints: at each time step, either the distance to the ground is zero or the contact force is zero. The optimizer then chooses the contact sequence together with the motion. The resulting problem is a nonlinear program with complementarity constraints, which is hard: its constraints are not convex and violate the usual regularity conditions, so practical methods relax them or use special solvers. Like every method of [trajectory optimization](/trajectory-optimization/), it is local, and different starts can give different contact sequences.

## In plain words

Picture planning a jump. You could decide first when the feet leave the ground and then plan each phase, but the best moment to leave the ground is part of what you want to find. Instead, let the planner choose the ground force at every moment, with one rule from physics: the ground can push only while the foot touches it. Now the planner can try all contact patterns at once and settle on the cheapest one it can reach. Without that rule, the planner cheats: it lets the ground push the body up through the air, and the plan looks free but is impossible. The rule makes the problem hard, so the planner first allows a little cheating and then less and less, until the plan obeys physics.

## The problem

Input: a model with states, controls and contact forces, a time step $h$, a horizon of $N$ steps, start and goal conditions, and a cost. Output: states, controls and contact forces that satisfy the time-stepping equations of motion, with the contact conditions of [rigid contact](/rigid-contact-complementarity/): for each contact and step,

$$\phi(q_{k+1}) \ge 0, \qquad \lambda_k \ge 0, \qquad \phi(q_{k+1})\,\lambda_k = 0,$$

where $\phi$ is the distance to the contact surface and $\lambda_k$ the normal force, and with friction forces limited by the [friction cone](/friction-cone/). The equations of motion are the [manipulator equation](/manipulator-equation/) with the contact forces added, discretized as in [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/).

This page uses the smallest case that shows the idea. A unit mass moves on a vertical line at height $q \ge 0$ with thrust $u_k$, gravity $g = 9.81$ and ground force $\lambda_k$:

$$v_{k+1} = v_k + h(u_k - g + \lambda_k), \qquad q_{k+1} = q_k + h v_{k+1}, \qquad 0 \le q_{k+1} \perp \lambda_k \ge 0.$$

It starts at rest on the ground and must be at rest at height $H$ after $N$ steps, with the least energy $E = \frac h2 \sum_k u_k^2$. The velocities are eliminated: $u_k = (q_{k+1} - 2q_k + q_{k-1})/h^2 + g - \lambda_k$, with $q_{-1} = q_0 = 0$ and $q_{N-1} = q_N = H$, so the variables are the heights $q_1, \dots, q_{N-2}$ and the forces $\lambda_0, \dots, \lambda_{N-1}$, and $E$ is a convex quadratic in them.

## The algorithm

```pseudo id=main
CONTACT-IMPLICIT(problem, ε_0, μ_0, κ, ε_min)
L1  ε ← ε_0;  μ ← μ_0
L2  x ← a start with q > 0, λ > 0 and q_{k+1} λ_k < ε for every k
L3  loop
L4      repeat                                   ▷ Newton's method on φ(x) = E(x) - μ (Σ_j log x_j + Σ_k log(ε - q_{k+1} λ_k))
L5          H ← ∇²φ(x) + τI, with τ = 0 if that is positive definite, else the smallest of 10⁻⁸, 10⁻⁷, … that makes it so
L6          d ← -H⁻¹ ∇φ(x)
L7          halve s from 1 until x + s d is strictly feasible and lowers φ enough;  x ← x + s d
L8      until the Newton decrement -∇φ(x)ᵀd / 2 is below tol
L9      if ε < ε_min then return x
L10     ε ← ε/κ;  μ ← μ/κ
L11     in each pair with q_{k+1} λ_k ≥ ε, shrink the smaller factor so that the product is ε/2
```

The code uses $\varepsilon_0 = \mu_0 = 0.1$, $\kappa = 4$, $\varepsilon_{\min} = 10^{-7}$ and $tol = 10^{-10}$.

The complementarity $q_{k+1}\lambda_k = 0$ is relaxed to $q_{k+1}\lambda_k \le \varepsilon$. For $\varepsilon > 0$ the feasible set has an interior, so a [barrier method](/barrier-method/) can work in it: lines L4 to L8 minimize the energy plus $\mu$ times a logarithmic barrier for all inequalities. The products are not convex, so the Hessian of the barrier can be indefinite, and line L5 adds a multiple of the identity until it is positive definite; then $d$ is a descent direction. Line L7 keeps every iterate strictly inside.

Lines L9 to L11 are the continuation. After each stage, $\varepsilon$ and $\mu$ shrink together, and line L11 repairs the pairs whose product is now too large: in contact the height is the smaller factor and is pushed toward the ground, in flight the force is the smaller factor and is pushed toward zero. Each stage starts from the answer of the stage before, so the contact pattern found at a large $\varepsilon$ guides the later stages.

This relaxation is a standard device for problems with complementarity constraints, and it is the choice of this page; the idea of the method does not depend on how the solver treats the constraints. In every version, the solver sees one problem and never enumerates contact sequences.

## Example

The mass must reach height $H = 0.5$ at rest after $N = 10$ steps of $h = 0.1$. The table shows the stages of the continuation.

| $\varepsilon$ | energy | largest $q_{k+1}\lambda_k$ |
|---|---|---|
| $0.1$ | 31.3672 | $9.5 \cdot 10^{-2}$ |
| $0.025$ | 34.7303 | $2.4 \cdot 10^{-2}$ |
| $6.3 \cdot 10^{-3}$ | 35.6850 | $6.0 \cdot 10^{-3}$ |
| $1.6 \cdot 10^{-3}$ | 35.9310 | $1.5 \cdot 10^{-3}$ |
| $3.9 \cdot 10^{-4}$ | 35.9930 | $3.7 \cdot 10^{-4}$ |
| $2.4 \cdot 10^{-5}$ | 36.0124 | $2.3 \cdot 10^{-5}$ |
| $9.5 \cdot 10^{-8}$ | 36.0137 | $9.2 \cdot 10^{-8}$ |

At a large $\varepsilon$ the energy is lower, because the relaxed ground can still push a little while the mass is in the air. After eleven stages the motion is: the mass rests on the ground for four steps with $u = 0$ and ground force $9.81$, so the ground carries its weight for free; then it leaves the ground and rises through the heights $0.0714$, $0.1857$, $0.3143$, $0.4286$, $0.5$ and $0.5$, with thrusts $16.95$, $14.10$, $11.24$, $8.38$, $5.52$ and $2.67$. The energy is $36.0137$.

The optimizer chose the lift-off time. Fixing the number of steps on the ground and solving each case gives the energies $49.633$ (no step), $45.390$, $41.471$, $38.147$, $36.014$ (four steps), $36.559$, $44.247$, $76.935$ and $259.62$ (eight steps): waiting saves the cost of carrying the weight, and leaving too late needs a hard push. A search over all $2^8$ contact sets confirms that $36.0137$ is the global minimum. Running the thrust through a simulator with exact contact reproduces the heights within $2 \cdot 10^{-7}$.

Starting the continuation at $\varepsilon_0 = \mu_0 = 1$ instead ends with five steps on the ground and energy $36.559$: a local solution, one step late.

Without the complementarity, keeping only $q \ge 0$ and $\lambda \ge 0$, the same method returns energy $5 \cdot 10^{-11}$. The thrust is zero; the mass rises to $0.725$ and sinks back to $0.5$, and the "ground" pushes with forces between $4.6$ and $31.6$ while the mass is in the air. The same zero thrust in a simulator leaves the mass on the ground.

## Correctness

The [proof](proofs/correctness.md) shows four things. The elimination of the velocities is exact. Every point that satisfies the complementarity is the motion that a simulator with exact contact produces from its thrust, because each time step has exactly one contact force that keeps the mass above the ground and pushes only in contact; so the optimized motion is physical. Without the complementarity, the optimizer can reach zero energy by letting the ground push through the air, and with it the energy is always positive; this is why the constraint matters. The barrier continuation keeps every iterate strictly feasible, each Newton step lowers the barrier function, and the result satisfies the relaxed complementarity with $\varepsilon$ below $\varepsilon_{\min}$. The problem with complementarity is a union of $2^{N-2}$ convex pieces, one for each contact set; the method is not guaranteed to find the best piece, and the example shows a start where it does not.

## Complexity

Each Newton step forms and factors a dense matrix of size $2N - 2$, at a cost of $O(N^3)$; with $T$ Newton steps over all stages the total is $O(TN^3)$, and the memory is $O(N^2)$. The matrix is banded, because each variable interacts only with the variables of nearby steps, so a banded factorization reduces a step to $O(N)$; for a robot with $n$ coordinates and $c$ contacts the banded cost is $O(N(n + c)^3)$ per Newton step. The number of stages is about $\log_\kappa(\varepsilon_0/\varepsilon_{\min}) + 1$, eleven in the example, but there is no bound on the number of Newton steps per stage, because the problem is not convex.

The enumeration of contact sets that the test uses for checking costs $2^{N-2}$ convex solves; contact-implicit optimization exists to avoid this.

## Properties

- **No contact schedule.** The contact sequence is an output, not an input.
- **Physical in the limit.** Complementarity makes the result a motion that a time-stepping simulator would produce; any relaxation is physical only in its limit.
- **Local.** The problem is not convex, and the result depends on the start and on the continuation schedule.
- **Hard constraints.** Problems with complementarity constraints violate the usual constraint qualifications, so general solvers need relaxations or special care.
- **Deterministic.** The same start and schedule give the same result.

## Variants and improvements

- **Friction.** With friction, the tangential forces get their own complementarity conditions that encode sliding and sticking, as in the [Stewart-Trinkle](/stewart-trinkle-time-stepping/) model; the original paper plans with friction.
- **Relaxations and penalties.** Instead of $q\lambda \le \varepsilon$, the product can be added to the cost as a penalty, or replaced by a smoothed function whose zeros are the complementary pairs.
- **Smooth contact models.** A soft contact model, with forces that grow smoothly as bodies approach, removes the complementarity altogether and allows gradient methods such as [control-limited DDP](/control-limited-ddp/), at the price of some force at a distance.
- **Interior point solvers.** General [interior point](/interior-point-method/) solvers can handle the relaxed problem with many variables, using the banded structure.
- **Contact schedules fixed in advance.** When the sequence of contacts is known, a hybrid formulation with one phase per contact mode gives smooth problems that are easier to solve; contact-implicit methods are for when the sequence is not known.

## When to use it

Use contact-implicit trajectory optimization when the contact sequence is part of the answer: legged robots that may take steps, manipulation where an object may slide, roll or be pushed, and jumps and landings. Give it a reasonable start, and expect to try several. When the contact sequence is known, a formulation with fixed phases is faster and more reliable. When contacts are not part of the task, use a method for smooth problems, such as [sequential convex optimization](/sequential-convex-trajectory-optimization/). Check every result in a simulator, because a relaxed solution can still use small forces through the air, and because discretization can hide effects like the [Painlevé paradox](/painleve-paradox/).

## Pitfalls

- **Dropping the complementarity.** With only the sign conditions, the ground pushes through the air, as the example shows. Line L4 must include the product terms.
- **Infeasible restarts.** After line L10 shrinks $\varepsilon$, the old answer violates the new bound; without line L11 the logarithm of line L4 is undefined.
- **Too fast a schedule.** A large $\kappa$ in line L10 skips over contact patterns, and too large a start $\varepsilon_0$ can lead to a worse local solution; the example ends one step late from $\varepsilon_0 = 1$.
- **Indefinite Hessians.** The barrier of the products has an indefinite Hessian; without the shift of line L5, the Newton direction need not go downhill.
- **Trusting the relaxed answer.** A final $\varepsilon$ that is not small leaves forces in the air; check the largest product, and simulate the result.

## Implementations

## History

Michael Posa, Cecilia Cantu and Russ Tedrake at MIT published the method in The International Journal of Robotics Research in 2014. It built on the time-stepping models of rigid contact, which write contact and friction as complementarity conditions, and on direct transcription methods for trajectory optimization, which make states and controls decision variables of one large nonlinear program. Its point was to make the contact forces decision variables as well, so that walking and manipulation tasks could be planned without a given contact sequence. At about the same time, Igor Mordatch, Emanuel Todorov and Zoran Popović planned contact-rich motions for animated characters with contact-invariant optimization, which treats contacts with smooth auxiliary variables, and both lines of work started a large body of research on planning through contact.

## References
