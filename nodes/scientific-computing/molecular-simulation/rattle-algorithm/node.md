---
tag: VJX93A
kind: algorithm
slug: rattle-algorithm
name: RATTLE algorithm
aliases:
- RATTLE
area: scientific-computing/molecular-simulation
level: core
summary: Extends SHAKE to velocity Verlet by also projecting velocities onto the tangent space of the constraints, giving a symplectic constrained integrator.
model: real-ram
complexity:
  vars: {N: the number of atoms, C: the number of constraints, s: the number of sweeps}
  time: {worst: O(N + s C)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, symplectic: true, time_reversible: true}
history:
  year: 1983
  people: [Hans C. Andersen]
  note: Andersen gave RATTLE in 1983 as a velocity version of SHAKE, and Leimkuhler and Skeel proved in 1994 that it is symplectic.
prereqs: [shake-constraint-algorithm]
see_also: [verlet-integration, lincs-algorithm, position-based-dynamics, baumgarte-stabilization, symplectic-integrators, hamiltonian-systems, lagrange-multiplier, shadow-hamiltonian]
sources:
  - paper: doi:10.1016/0021-9991(83)90014-1
    title: Hans C. Andersen, Rattle, A "velocity" version of the Shake algorithm for molecular dynamics calculations, Journal of Computational Physics 52(1), 1983, 24-34
    locator: the two constraint stages for positions and velocities
  - paper: doi:10.1006/jcph.1994.1085
    title: Benedict J. Leimkuhler and Robert D. Skeel, Symplectic numerical integrators in constrained Hamiltonian systems, Journal of Computational Physics 112(1), 1994, 117-125
    locator: the proof that RATTLE is symplectic and its relation to SHAKE
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: the treatment of constrained mechanical systems and the RATTLE method
---

RATTLE integrates the motion of particles with fixed distances between some pairs, using velocity Verlet. A fixed distance is a constraint, such as a rigid bond in a molecule or a rigid link in a mechanism, and it asks two things: that the distance has the right value, and that the two particles have no relative velocity along the line between them. The position stage is the [SHAKE](/shake-constraint-algorithm/) iteration: after a half kick and a drift, it corrects the positions and the half-step velocities along the old bond directions until every distance holds. The velocity stage, which SHAKE does not have, corrects the new velocities along the new bond directions until each one is tangent to the constraints. Both stages iterate to a tolerance. The result is symplectic and time reversible on the set of allowed states, so the energy stays in a band over long runs. Graphics methods such as [position-based dynamics](/position-based-dynamics/) project positions and then take velocities from the change of position; RATTLE instead keeps the momenta as variables and treats both constraints exactly.

## In plain words

Imagine a pendulum with a rigid rod. The bob must stay at the same distance from the pivot, and it must never move toward or away from the pivot. Its velocity must always point along the circle.

RATTLE moves the bob one step as if the rod were not there. Then it pulls the bob back to the right distance, as SHAKE does, and fixes the velocity it used so that it matches that move. After the new forces act, the velocity has a small part that points along the rod. RATTLE removes that part. When there are many rods that share atoms, fixing one upsets the next, so both corrections go over all the rods again and again until each one is right to the requested accuracy.

## The problem

There are $N$ atoms with positions $x_i$, velocities $v_i$, inverse masses $w_i = 1/m_i$ (zero for a fixed atom), a force $f(x)$, and $C$ constraints $c = (i, j, d_c)$ with $\sigma_c(x) = |x_i - x_j|^2 - d_c^2$. Let $G(x)$ be the matrix with rows $\frac12 \nabla \sigma_c(x)$, so the velocity constraint is $G(x) v = 0$. Given $(x^0, v^0)$ with $\sigma(x^0) = 0$ and $G(x^0) v^0 = 0$, and the step $h$, find
$$v^{1/2} = v^0 + \tfrac{h}{2} W f(x^0) - W G(x^0)^{\mathsf T} \gamma, \qquad x^1 = x^0 + h v^{1/2}, \qquad \sigma(x^1) = 0,$$
$$v^1 = v^{1/2} + \tfrac{h}{2} W f(x^1) - W G(x^1)^{\mathsf T} \delta, \qquad G(x^1) v^1 = 0,$$
where $W$ is the diagonal matrix of the $w_i$ and $\gamma, \delta$ are multipliers.

## The algorithm

```pseudo id=main
RATTLE-STEP(x, v, f, w, force, h, bonds, τ)
L1  v' ← v + (h/2) W f                         ▷ half kick
L2  x' ← x + h v'                              ▷ drift
L3  repeat sweeps over the constraints c = (i, j, d), until each has |d² - |x'_i - x'_j|²| ≤ 2τd²
L4      g ← (d² - |s|²) / (2 (w_i + w_j) s · r);  shift x'_i, x'_j by ±w g r and v'_i, v'_j by ±w g r / h
L5  f' ← force(x')
L6  v'' ← v' + (h/2) W f'                       ▷ second half kick
L7  repeat sweeps over the constraints, until each has |r' · (v''_i - v''_j)| ≤ τ d²
L8      k ← -r' · (v''_i - v''_j) / ((w_i + w_j) d²);  v''_i ← v''_i + w_i k r';  v''_j ← v''_j - w_j k r'
L9  return (x', v'', f')
```

Here $s = x'_i - x'_j$, $r = x_i - x_j$ is the old bond, and $r' = x'_i - x'_j$ is the new bond. The velocity equations are linear in $\delta$, so the loop of line L7 is a Gauss-Seidel solve of a linear system. Each loop stops with an error if it does not converge in a set number of sweeps.

## Example

Take a pendulum of length 1 and mass 1 under gravity $g = 1$, as an anchor with $w = 0$ and a bob joined by one constraint. Released at rest from the angle $\theta_0 = 1$, its exact period is $2\pi / \mathrm{agm}(1, \cos(\theta_0/2)) = 6.699975664$. The period from RATTLE, measured from the crossings of the vertical:

| step $h$ | period error |
|---|---|
| 0.04 | $9.83 \times 10^{-4}$ |
| 0.02 | $2.47 \times 10^{-4}$ |
| 0.01 | $6.16 \times 10^{-5}$ |

Each halving of the step divides the error by 4.0, the second order of velocity Verlet. In every step, the rod length and the radial velocity are zero to $10^{-12}$.

Released from $\theta_0 = 1.5$, close to horizontal, and run to the time 200, about 25 periods, the energy error is at most $8.50 \times 10^{-4}$ with $h = 0.05$ and $2.13 \times 10^{-4}$ with $h = 0.025$. The largest error after the time 20 is the same as before it, to three digits: the energy moves in a band and does not drift.

## Correctness

The proof below shows these claims:

1. **The position stage** returns $x^1 = x^0 + h v^{1/2}$, with the velocity corrections along the rows of $G(x^0)$, and every bond within the tolerance.
2. **The velocity stage** returns $v^1$ with corrections along the rows of $G(x^1)$, and every velocity constraint within the tolerance.
3. **Time reversal.** One step from $(x^1, -v^1)$ returns to $(x^0, -v^0)$, when the equations have locally unique solutions.
4. **The positions are those of SHAKE.** Three successive positions satisfy the constrained Verlet equations, so RATTLE and SHAKE give the same positions from the same start.
5. **Order and symplecticity.** RATTLE has order 2 and is a symplectic map on the states that satisfy both constraints. These are theorems of Leimkuhler and Skeel (1994), cited and not proved again.

The tests check the period of the pendulum against the exact value, both constraints on every step of a chain, reversibility to $10^{-9}$, the preserved area of the pendulum map, the energy band, and agreement with the SHAKE positions to $10^{-10}$.

## Complexity

The kicks and the drift cost $\Theta(N)$ plus one force evaluation. Each sweep of either loop costs $\Theta(C)$. The position loop needs a number of sweeps that grows like $\log(1/\tau)$ over the log of the convergence factor, as in SHAKE. The velocity loop solves a linear system with the same coupling, so its number of sweeps behaves in the same way. Extra memory is $\Theta(N)$.

## Properties

- **Symplectic.** On the manifold of states that satisfy both constraints, the step preserves the symplectic form, a theorem of Leimkuhler and Skeel (1994). The energy error therefore stays bounded over long runs, as explained by the [shadow Hamiltonian](/shadow-hamiltonian/) theory.
- **Time reversible,** when both loops are solved to a tight tolerance.
- **Order two,** like velocity Verlet.
- **Consistent velocities.** The velocities satisfy the velocity constraints, so the kinetic energy and the temperature come out right.
- **One force evaluation per step,** the same as velocity Verlet without constraints.

## Variants and improvements

- **SHAKE.** [SHAKE](/shake-constraint-algorithm/) is the position form, with the same positions and no velocity stage.
- **LINCS.** [LINCS](/lincs-algorithm/) replaces the position loop by a matrix series, and a projection of the same kind gives the velocities.
- **SETTLE.** For rigid water, both stages have closed-form solutions.
- **Newton solves.** For large rigid molecules, solve all the multipliers of each stage at once with a sparse linear solver.
- **Other splittings.** The same two projections can go into the [RESPA](/respa-multiple-time-step/) integrator or a Langevin splitting, after each position update and each velocity update.

## When to use it

Use RATTLE with velocity Verlet whenever a simulation holds bonds or rigid groups fixed, and you need good velocities, for example to compute a temperature, a pressure, or a time correlation function. It is a standard choice for constrained molecular dynamics and for mechanical systems with rigid links. For very large systems in parallel, LINCS is faster. For a fixed small number of passes and visual results, position-based dynamics is cheaper.

## Pitfalls

- **A loose tolerance** breaks reversibility and symplecticity, and the energy then drifts. Use $10^{-8}$ or tighter in double precision.
- **Skipping the velocity stage** leaves a radial velocity of order $h$ in each bond. The positions are still those of SHAKE, but kinetic energies are wrong.
- **The wrong bond vectors.** The position stage corrects along the old bonds and the velocity stage along the new bonds. Mixing them up loses symplecticity.
- **Fixed atoms.** An atom with $w = 0$ must not be in a constraint with another fixed atom, because then $w_i + w_j = 0$.
- **Degrees of freedom.** Each constraint removes one degree of freedom from the count used for the temperature.

## Implementations

## History

Andersen (1983) gave RATTLE as a velocity version of SHAKE, the method of Ryckaert, Ciccotti and Berendsen (1977), for velocity Verlet. Leimkuhler and Skeel (1994) proved that RATTLE is symplectic, and showed that SHAKE gives the same positions. Hairer, Lubich and Wanner give RATTLE for general constrained mechanical systems in their book on geometric integration.

## References
