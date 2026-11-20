---
tag: 3AE47X
kind: algorithm
slug: shake-constraint-algorithm
name: SHAKE constraint algorithm
aliases:
- SHAKE
area: scientific-computing/molecular-simulation
level: core
summary: Holds bond lengths fixed during Verlet integration by adjusting positions along the bonds, one constraint at a time, until all hold to a tolerance.
model: real-ram
complexity:
  vars: {N: the number of atoms, C: the number of constraints, s: the number of sweeps}
  time: {worst: O(N + s C)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, time_reversible: true}
history:
  year: 1977
  people: [Jean-Paul Ryckaert, Giovanni Ciccotti, Herman J. C. Berendsen]
  note: Ryckaert, Ciccotti and Berendsen gave the method in 1977 for molecular dynamics of n-alkanes with rigid bonds.
prereqs: [verlet-integration, molecular-dynamics]
see_also: [rattle-algorithm, lincs-algorithm, position-based-dynamics, baumgarte-stabilization, lagrange-multiplier, gauss-seidel-method, newton-raphson-method, symplectic-integrators]
sources:
  - paper: doi:10.1016/0021-9991(77)90098-5
    title: Jean-Paul Ryckaert, Giovanni Ciccotti and Herman J. C. Berendsen, Numerical integration of the cartesian equations of motion of a system with constraints, molecular dynamics of n-alkanes, Journal of Computational Physics 23(3), 1977, 327-341
    locator: the constrained Verlet equations and their iterative solution, one constraint at a time
  - paper: doi:10.1006/jcph.1994.1085
    title: Benedict J. Leimkuhler and Robert D. Skeel, Symplectic numerical integrators in constrained Hamiltonian systems, Journal of Computational Physics 112(1), 1994, 117-125
    locator: the relation of SHAKE and RATTLE, and their symplecticity
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Chapter 3, Molecular dynamics, the section on constraint dynamics
---

SHAKE keeps chosen distances between pairs of particles fixed while a [Verlet](/verlet-integration/) integrator moves them. Each such distance is a constraint: in a molecule it is a bond length, or the distance between two hydrogens of a rigid water. The integrator first takes a free step that ignores the constraints. SHAKE then moves the particles back, each pair along its bond direction at the start of the step, with shifts weighted by the inverse masses, and goes over the constraints one at a time until all of them hold to a tolerance. [Position-based dynamics](/position-based-dynamics/) in graphics also projects positions one constraint at a time, but it usually stops after a fixed number of passes. SHAKE adds three things: the corrections are the forces of Lagrange multipliers, so the result is the constrained Verlet step of mechanics; it iterates to a set tolerance; and with the velocities from [RATTLE](/rattle-algorithm/) the method is time reversible and symplectic. [LINCS](/lincs-algorithm/) solves the same equations with a matrix series instead of a sweep.

## In plain words

Some parts of a molecule move very fast, such as a hydrogen atom that vibrates along its bond. To follow that motion, a simulation needs a tiny time step. If we hold those bonds at a fixed length, the fast motion is gone and the step can be larger.

SHAKE does this after each normal step. The step moves every atom as if the bonds were not there, so the bonds stretch or shrink a little. SHAKE looks at one bond, and pulls or pushes its two atoms along the line they had before the step until the bond has the right length. The light atom moves more than the heavy one. Fixing one bond can upset its neighbours, so SHAKE goes over all the bonds again and again until every bond is right to the requested accuracy.

## The problem

There are $N$ atoms with positions $x_i$, masses $m_i$ and inverse masses $w_i = 1/m_i$ (zero for a fixed atom), a force $f(x)$, and $C$ constraints $c = (i, j, d_c)$, each asking $\sigma_c(x) = |x_i - x_j|^2 - d_c^2 = 0$. Given $x^{n-1}$ and $x^n$ that satisfy the constraints, and the step $h$, find $x^{n+1}$ and multipliers $\lambda$ with
$$x^{n+1} = 2 x^n - x^{n-1} + h^2 W f(x^n) - h^2 W \nabla \sigma(x^n)^{\mathsf T} \lambda, \qquad \sigma(x^{n+1}) = 0,$$
where $W$ is the diagonal matrix of the $w_i$. The constraint forces act along the old bond vectors $r_c = x^n_i - x^n_j$. The equations for $\lambda$ are nonlinear, and we solve them to a relative tolerance $\tau$.

## The algorithm

```pseudo id=main
SHAKE-STEP(x_prev, x, w, f, h, bonds, τ)
L1  x̃ ← 2x - x_prev + h² W f(x)                  ▷ the free Verlet step
L2  repeat
L3      for each constraint c = (i, j, d) do
L4          s ← x̃_i - x̃_j;  if |d² - |s|²| ≤ 2τ d² then skip this constraint
L5          g ← (d² - |s|²) / (2 (w_i + w_j) s · r_c)   ▷ r_c = x_i - x_j, the old bond
L6          x̃_i ← x̃_i + w_i g r_c;  x̃_j ← x̃_j - w_j g r_c
L7  until a whole sweep skips every constraint
L8  return x̃
```

Line L5 is one Newton step for the single constraint, with all other atoms held fixed. The code stops with an error if $s \cdot r_c \le 0$, which means that a bond turned by more than a right angle in one step, and if the sweeps do not converge after a set number.

## Example

**One bond.** Atom 0 has $w_0 = 1$, atom 1 has $w_1 = 0.25$, and the old bond is $r = x_0 - x_1 = (-1, 0, 0)$ with $d = 1$. The free step puts the atoms at $(0.05, 0.1, -0.02)$ and $(1.2, -0.05, 0.03)$, so $s = (-1.15, 0.15, -0.05)$ and $|s|^2 = 1.3475$. The exact correction solves the quadratic $|s + 1.25 g r|^2 = 1$ for $g$. SHAKE takes Newton steps on this equation and reaches the smaller root to $10^{-12}$.

**Water.** A rigid water molecule has three constraints: two O-H bonds of 0.9572 Å and the H-H distance 1.5139 Å, with masses 16 and 1.008. Move each coordinate by a random amount in $[-0.02, 0.02]$ Å (seed 1), which breaks the bonds by up to $1.8\%$. The number of sweeps for three tolerances:

| tolerance $\tau$ | sweeps | largest relative bond error |
|---|---|---|
| $10^{-4}$ | 5 | $8.9 \times 10^{-5}$ |
| $10^{-8}$ | 23 | $9.2 \times 10^{-9}$ |
| $10^{-12}$ | 41 | $9.4 \times 10^{-13}$ |

Each factor of 10 in the tolerance costs about 4.5 sweeps, the sign of linear convergence. The three constraints of water form a triangle, and they are strongly coupled.

**A chain.** Four atoms of masses 1, 2, 2, 1 with three rigid bonds and soft springs between atoms that are not neighbours, run from rest for a time of 20. All bonds hold to $10^{-11}$. The total energy moves within a band of width $4.86 \times 10^{-4}$ for $h = 0.02$ and $1.21 \times 10^{-4}$ for $h = 0.01$: halving the step divides the band by 4, and the energy does not drift.

## Correctness

The proof below shows these claims:

1. **The form of the result.** At every moment of the loop, the positions are the free step plus corrections along the old bond vectors, weighted by the inverse masses. So the result has the form of the constrained Verlet step.
2. **Line L5 is a Newton step** for the single constraint as a function of its multiplier.
3. **The stopping test.** When the loop returns, every constraint holds to the relative tolerance, so the result solves the constrained Verlet equations to that tolerance.
4. **The centre of mass** does not move during the corrections.
5. **Local convergence.** For a small step and constraints that are not nearly dependent, the sweeps converge, and the error falls by a fixed factor in each sweep, the spectral radius of a Gauss-Seidel iteration matrix.

The tests check one bond against the root of the quadratic, a branched molecule against a full Newton solve of all the constraints, the centre of mass, a fixed atom, the energy band of the chain, and the error for a set of constraints that cannot all hold.

## Complexity

The free step costs $\Theta(N)$ plus the force. One sweep costs $\Theta(C)$, so the step costs $\Theta(N + sC)$ for $s$ sweeps. The number of sweeps is about $\log(1/\tau) / \log(1/\rho)$, where $\rho$ is the convergence factor of Claim 5. It is small for isolated bonds and large for rings and long chains of coupled bonds. Extra memory is $\Theta(N)$ for the old bond vectors.

## Properties

- **Time reversible.** The constrained Verlet step is symmetric in time, if the constraints are solved exactly.
- **Symplectic positions.** SHAKE gives the same positions as RATTLE, which is a symplectic method on the constraint manifold (Leimkuhler and Skeel, 1994). So the energy stays in a band and does not drift.
- **Momentum.** The corrections keep the centre of mass, and with pair forces the total momentum is kept.
- **Sequential.** Each correction uses the result of the one before, which makes the sweep hard to run in parallel.
- **Order two.** The positions have the global error $O(h^2)$ of Verlet.

## Variants and improvements

- **RATTLE.** [RATTLE](/rattle-algorithm/) puts the same idea into velocity Verlet, and adds a second loop that makes the velocities tangent to the constraints.
- **LINCS.** [LINCS](/lincs-algorithm/) replaces the sweep by a truncated matrix series, which is faster and runs in parallel, at a fixed cost per step.
- **SETTLE.** For a rigid water, the three constraints have a closed-form solution, so no iteration is needed.
- **Over-relaxation.** Multiplying the correction by a factor between 1 and 2 can cut the number of sweeps, as in successive over-relaxation.
- **Matrix SHAKE.** A Newton method on all multipliers at once, with a sparse matrix, converges in fewer iterations for large rigid systems.

## When to use it

Use SHAKE to hold bonds to hydrogen fixed in a molecular simulation, which allows a step of about 2 fs instead of about 1 fs. It is simple to code and reliable for small groups of coupled constraints. For large rigid molecules on many processors, use LINCS. For rigid water, use a closed-form method. If the integrator is velocity Verlet, use RATTLE, which contains SHAKE as its position stage.

## Pitfalls

- **A loose tolerance.** The energy then drifts, because the step is no longer exactly reversible. Use a relative tolerance of $10^{-8}$ or smaller in double precision.
- **Coupled angles.** Constraining bond angles as well as bonds makes the constraints nearly dependent, and the sweeps converge slowly or not at all. Constrain angles through a third distance, and only where the geometry stays far from flat.
- **A step that is too large.** A bond that turns by a right angle in one step has $s \cdot r_c \le 0$, and the Newton step breaks down.
- **Velocities.** Position Verlet gives velocities as differences of positions, which do not satisfy the velocity constraints. Kinetic energy and temperature then have a small error.
- **Degrees of freedom.** Each constraint removes one degree of freedom. Count them when you compute a temperature from the kinetic energy.

## Implementations

## History

Ryckaert, Ciccotti and Berendsen (1977) gave the method for molecular dynamics of n-alkanes with rigid bonds. They wrote the Verlet step with Lagrange multipliers and solved for the multipliers iteratively, one constraint at a time. Andersen (1983) gave RATTLE, the velocity version. Leimkuhler and Skeel (1994) showed that RATTLE is symplectic and that SHAKE gives the same positions. Hess, Bekker, Berendsen and Fraaije (1997) gave LINCS as a faster and more parallel replacement.

## References
