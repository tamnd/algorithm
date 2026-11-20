---
tag: A5VK4X
kind: algorithm
slug: parrinello-rahman-barostat
name: Parrinello-Rahman barostat
aliases:
- Parrinello-Rahman method
area: scientific-computing/molecular-simulation
level: advanced
summary: Lets the shape and size of the periodic box evolve as dynamical variables driven by the pressure tensor. Alone it samples NPH; with a thermostat added it samples NPT.
model: real-ram
complexity:
  vars: {N: the number of particles, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, symplectic: true, symmetric: true}
history:
  year: 1980
  people: [Michele Parrinello, Aneesur Rahman]
  note: Parrinello and Rahman made the matrix of the cell vectors a dynamical variable with a kinetic energy, so that the box changes shape under the stress, and used it to see a crystal change its structure in a simulation.
prereqs: [molecular-dynamics, periodic-boundary-conditions]
see_also: [nose-hoover-chains, stochastic-velocity-rescaling, nose-hoover-thermostat, langevin-dynamics, canonical-ensemble, lennard-jones-potential, symplectic-integrators, verlet-integration]
sources:
  - paper: doi:10.1103/PhysRevLett.45.1196
    title: M. Parrinello and A. Rahman, Crystal structure and pair potentials, A molecular-dynamics study, Physical Review Letters 45(14), 1980, 1196-1199
    locator: the Lagrangian with the cell matrix as a variable and the first simulation of a structural transition
  - paper: doi:10.1063/1.328693
    title: M. Parrinello and A. Rahman, Polymorphic transitions in single crystals, A new molecular dynamics method, Journal of Applied Physics 52(12), 1981, 7182-7190
    locator: the full equations of motion for the particles and the cell under an external stress, and the conserved quantity
  - paper: doi:10.1080/00268979600100761
    title: Glenn J. Martyna, Mark E. Tuckerman, Douglas J. Tobias and Michael L. Klein, Explicit reversible integrators for extended systems dynamics, Molecular Physics 87(5), 1996, 1117-1157
    locator: reversible splitting integrators for constant pressure dynamics with a flexible cell and thermostat chains
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: Chapter 5, the isobaric ensembles, including anisotropic cell fluctuations
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the chapter on molecular dynamics in various ensembles, constant pressure
---

The Parrinello-Rahman barostat controls the pressure in [molecular dynamics](/molecular-dynamics/) with [periodic boundary conditions](/periodic-boundary-conditions/). It makes the matrix $H$ of the cell vectors a dynamical variable with a mass $W$. The cell feels a force equal to the difference between the internal pressure tensor and the external pressure, so it can change both its volume and its shape. That makes it the standard method for solids, where a crystal may need a box of a new shape to change its structure. The equations alone conserve an enthalpy, so they sample the isoenthalpic-isobaric (NPH) ensemble if they are ergodic. For the isothermal-isobaric (NPT) ensemble a thermostat must act as well, for example a [Nose-Hoover chain](/nose-hoover-chains/) or [stochastic velocity rescaling](/stochastic-velocity-rescaling/).

## In plain words

In a normal simulation the box has a fixed size and shape. In a lab, a sample is pushed by the air around it at a fixed pressure, and it can grow, shrink or shear.

This method gives the walls of the box a mass and lets them move. If the atoms push outward harder than the outside pressure, the box grows; if they push less, it shrinks. If they push harder in one direction, the box stretches that way, and a shear stress tilts it. The box overshoots and swings like a heavy spring, so the mass of the walls sets how fast it swings.

The total of the energy of the atoms, the work against the outside pressure and the energy of the moving walls stays fixed. To also keep the temperature fixed, a thermostat must be added.

## The problem

The input is $N$ particles in $d$ dimensions with positions $r_i$, velocities $v_i$ and masses $m_i$, a periodic cell with the matrix $H$ whose columns are the cell vectors (volume $V = \det H$), a cell velocity $\dot H$, a pair potential, a time step $h$, a number of steps $S$, the external pressure $P$ and the cell mass $W > 0$. The particles use scaled coordinates $s_i = H^{-1} r_i \in [0, 1)^d$. With $G = H^{\mathsf T} H$, the Lagrangian of Parrinello and Rahman gives the Hamiltonian
$$E = \sum_i \frac{\pi_i^{\mathsf T} G^{-1} \pi_i}{2 m_i} + U(H s) + \frac{\operatorname{tr}(P_H^{\mathsf T} P_H)}{2W} + P \det H,$$
with the momenta $\pi_i = m_i G \dot s_i$ and $P_H = W \dot H$. The first term is the kinetic energy $K$ of the particles in Cartesian velocities $v_i = H \dot s_i$. Its equations give the cell equation
$$W \ddot H = V\,(\Pi - P I)\,H^{-\mathsf T}, \qquad \Pi = \frac{1}{V}\Bigl(\sum_i m_i v_i v_i^{\mathsf T} + \sum_{i < j} f_{ij} r_{ij}^{\mathsf T}\Bigr),$$
with the internal pressure tensor $\Pi$. The output is the trajectory and, after each step, $E$, $\det H$ and $\Pi$. The implementation works in $d = 2$ with a force-shifted [Lennard-Jones potential](/lennard-jones-potential/). For the kinetic temperature, $N_f = dN - d$, since the flow keeps $\sum_i \pi_i$, and with it the total momentum, at 0.

## The algorithm

```pseudo id=main
PARRINELLO-RAHMAN(s, pi, H, P_H, m, h, S, P, W)
L1  (U, f, F) ← FORCES(s, H)              ▷ F = Σ_pairs f_ij s_ij^T, with minimum images
L2  for step ← 1 to S do
L3      pi_i ← pi_i + (h/2) H^T f_i; P_H ← P_H + (h/2)(F - P det(H) H^-T)        ▷ V: potential and P V
L4      for each i: v_i ← H^-T pi_i / m_i; s_i ← s_i + (h/2) H^-1 v_i; P_H ← P_H + (h/2) m_i v_i (H^-1 v_i)^T   ▷ T
L5      H ← H + h P_H / W                                                       ▷ C: cell drift
L6      repeat line L4 with the new H                                           ▷ T
L7      (U, f, F) ← FORCES(s, H)
L8      repeat line L3                                                          ▷ V
L9      record E, det(H) and the pressure tensor Pi
L10 return (H s, the velocities, H, P_H / W, the records)
```

The energy is split into three parts: $U + P\det H$, the particle kinetic energy $K$, and the cell kinetic energy. Each part has an exact flow. In the $K$ part the Cartesian velocities stay fixed while the scaled positions move, so line L4 is exact. The step V T C T V is a palindrome, so it is symplectic, time-reversible and of order 2, with one force evaluation per step. With $W \to \infty$ the cell stays fixed and the step is velocity Verlet.

## Example

**The test system.** 24 particles with $m = 1$ on a $4 \times 6$ triangular lattice with spacing 1.12, in reduced Lennard-Jones units, with the cutoff $r_c = 1.8$, so the cell is $4.48 \times 5.81969$ and $V_0 = 26.0722$. The velocities are normal with standard deviation 0.3 (seed 3), less their mean. Then $K = 1.886$, $N_f = 46$, $k_B T = 2K/N_f = 0.0820$ and $U = -45.704$. The internal pressure is $\Pi \approx 0.865 I$, with off-diagonal entries of $-0.0074$.

**Second order energy error.** With $P = 1$, $W = 5$ and the cell at rest, run to $t = 0.5$:

| $h$ | 0.01 | 0.005 | 0.0025 |
|---|---|---|---|
| spread of $E$ | $6.152 \times 10^{-3}$ | $1.579 \times 10^{-3}$ | $3.979 \times 10^{-4}$ |

The spread falls by a factor of 4 when $h$ is halved. A run of 150 steps forward and 150 back with the velocities flipped recovers the start to $10^{-9}$. With $W = 10^{14}$ the positions agree with velocity Verlet in the fixed cell to $10^{-7}$.

**The pressure follows the external pressure.** With $W = 2$, $h = 0.01$ and 400 steps:

| $P$ | mean of $\frac12 \operatorname{tr} \Pi$ | range of $V$ |
|---|---|---|
| 0.5 | 0.4917 | 26.07 to 26.78 |
| 1.5 | 1.4987 | 25.73 to 26.09 |

At $P = 0.5$, less than the initial internal pressure, the cell grows. At $P = 1.5$ it shrinks. These are measurements. The time average of $\Pi$ tends to $P$ because $\dot H$ stays bounded in the cell equation.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The three flows are exact**, so the step is symplectic.
2. **Time reversal.** The step is a palindrome of flows that the flip of all momenta reverses.
3. **The cell equation** of the flow is $W\ddot H = V(\Pi - P I)H^{-\mathsf T}$.
4. **Conserved momenta.** The flow and the step keep $\sum_i \pi_i$ and the antisymmetric part of $P_H H^{\mathsf T}$. So a cell that starts without rotation does not start to rotate.
5. **Large cell mass.** As $W \to \infty$ the step tends to velocity Verlet in a fixed cell.
6. **Minimum image.** If $2 r_c$ is less than the smallest width of the cell, each pair has at most one image within $r_c$, the one that the code uses.
7. **The ensemble.** The flow keeps $E$, the enthalpy $K + U + PV$ plus the cell kinetic energy, so if it is ergodic it samples NPH. With a thermostat on all variables at $k_B T$, the stationary density is $e^{-\beta(K + U + PV)}\,dr\,dp\,dH$, with the Lebesgue measure on the $d^2$ entries of $H$.

The measure on $V$ is the question for NPT. Since $dH$ gives the weight $V^{d-1}\,dV$, not $dV$, the method with a thermostat samples an NPT distribution in which the volume has the extra weight $V^{d-1}$. The configurational integral already has the factor $V^N$, so this changes volume averages by a relative amount of order $(d-1)/N$. Later constant pressure equations, such as those in the work of Martyna, Tuckerman, Tobias and Klein, are built to give the weight of the standard NPT ensemble.

## Complexity

Each step does one force evaluation with the minimum image of each pair, $O(N)$ work for the particle flows and $O(d^3)$ work for the cell. With all pairs, $S$ steps take $O(S N^2)$ time; with neighbor lists, $O(S N)$. The extra space is $O(N)$ for the scaled coordinates and momenta.

## Properties

- **Ensemble.** NPH if the flow is ergodic. NPT only with a thermostat added, and then with the volume weight $V^{d-1}$ of the measure $dH$.
- **Flexible cell.** Both volume and shape change, driven by the full pressure tensor, so stress-driven phase transitions in solids can occur.
- **Symplectic and time-reversible** with the splitting used here.
- **A conserved quantity to monitor.** $E$ drifts only by integration error.
- **Fictitious cell dynamics.** The mass $W$ is a choice, and the motion of the cell has no physical meaning. Static averages do not depend on $W$, but the volume oscillates with a period set by $W$, and a small $W$ disturbs the dynamics of the particles.
- **Rotation.** The cell can rotate if the antisymmetric part of $P_H H^{\mathsf T}$ is not 0 at the start.

## Variants and improvements

- **Isotropic cells.** Andersen (1980) let only the volume change, which suits liquids. The cell is then a scalar.
- **Thermostats for NPT.** Nose-Hoover chains on the particles and on the cell give a deterministic NPT method, and Martyna, Tuckerman, Tobias and Klein (1996) gave reversible integrators for it. [Langevin dynamics](/langevin-dynamics/) or [stochastic velocity rescaling](/stochastic-velocity-rescaling/) on the particles also give NPT when the cell variables are thermostatted too.
- **Stochastic barostats.** Langevin piston methods and stochastic cell rescaling add friction and noise to the cell, which damps the oscillations of the volume.
- **External stress.** Parrinello and Rahman (1981) replaced $P\det H$ by a general stress term, for simulations under uniaxial load.
- **Weak coupling.** The Berendsen barostat scales the box toward the target pressure. It equilibrates quickly but does not sample a known ensemble.

## When to use it

Use it for crystals and other solids, where the cell must change shape: phase transitions under pressure, elastic constants from the fluctuations of $H$, anisotropic materials and membranes. Combine it with a thermostat for NPT. For liquids an isotropic barostat is simpler. Use a weak coupling method for the first equilibration, since a cell far from equilibrium oscillates strongly with Parrinello-Rahman.

## Pitfalls

- **Expecting NPT from the barostat alone.** Without a thermostat the temperature drifts and the ensemble is NPH.
- **Too small a cell mass.** The cell then oscillates fast, and the time step must resolve it; check the spread of $E$.
- **Starting far from equilibrium.** A large pressure difference makes the cell oscillate with a large amplitude, and the system can become unstable. Equilibrate first.
- **A cell that becomes too thin.** If the cell shears so that $2 r_c$ exceeds a width, the minimum image is wrong. The implementation raises an error in this case.
- **A rotating cell.** Start with a symmetric $P_H H^{\mathsf T}$, for example a cell at rest, or restrict $H$ to an upper triangular form as many codes do.
- **Wrong $N_f$.** The total momentum is conserved, so subtract $d$.

## Implementations

## History

Andersen (1980) proposed a barostat in which the volume is a dynamical variable. In the same year Parrinello and Rahman generalized it to a cell matrix with its own kinetic energy, so that the shape could change, and in 1981 they gave the method in full and used it to study polymorphic transitions in crystals. Later work combined it with thermostats, and Martyna, Tuckerman, Tobias and Klein (1996) gave reversible integrators for constant pressure dynamics with a flexible cell. The method is available in most molecular dynamics codes.

## References
