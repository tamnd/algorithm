---
tag: CPQSNC
kind: algorithm
slug: molecular-dynamics
name: Molecular dynamics simulation
aliases:
- MD simulation
area: biology/structure-prediction
level: advanced
summary: Simulates the motion of atoms by integrating Newton's equations under a force field, with the velocity Verlet method and one force evaluation per time step of about 1 to 2 fs.
solves: [ab-initio-protein-folding]
model: real-ram
complexity:
  vars: {N: the number of atoms, S: the number of time steps}
  time: {worst: O(S N^2)}
  space: {extra: O(N)}
properties: {deterministic: true, iterative: true, symplectic: true, symmetric: true}
history:
  year: 1957
  people: [Berni J. Alder, Thomas E. Wainwright, Aneesur Rahman, Loup Verlet, J. Andrew McCammon, Bruce R. Gelin, Martin Karplus]
  note: Alder and Wainwright simulated hard spheres in 1957, Rahman simulated liquid argon in 1964, Verlet gave the integrator in 1967, and McCammon, Gelin and Karplus simulated the first protein in 1977.
prereqs: [energy-function, verlet-integration]
see_also: [hamiltonian-systems, symplectic-integrators, hamiltonian-monte-carlo, parallel-tempering, energy-landscape, ab-initio-protein-folding, rosetta, partition-function]
sources:
  - paper: doi:10.1103/PhysRev.159.98
    title: Loup Verlet, Computer "experiments" on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1), 1967, 98-103
    locator: the integrator and the simulation of a Lennard-Jones fluid
  - paper: doi:10.1063/1.442716
    title: William C. Swope, Hans C. Andersen, Peter H. Berens and Kent R. Wilson, A computer simulation method for the calculation of equilibrium constants for the formation of physical clusters of molecules, application to small water clusters, Journal of Chemical Physics 76(1), 1982, 637-649
    locator: the velocity form of the Verlet integrator
  - paper: doi:10.1063/1.1743957
    title: Berni J. Alder and Thomas E. Wainwright, Phase transition for a hard sphere system, Journal of Chemical Physics 27(5), 1957, 1208-1209
    locator: the first molecular dynamics simulation
  - paper: doi:10.1103/PhysRev.136.A405
    title: Aneesur Rahman, Correlations in the motion of atoms in liquid argon, Physical Review 136(2A), 1964, A405-A411
    locator: the first simulation with a continuous potential
  - paper: doi:10.1038/267585a0
    title: J. Andrew McCammon, Bruce R. Gelin and Martin Karplus, Dynamics of folded proteins, Nature 267(5612), 1977, 585-590
    locator: the first molecular dynamics simulation of a protein
  - paper: doi:10.1126/science.282.5389.740
    title: Yong Duan and Peter A. Kollman, Pathways to a protein folding intermediate observed in a 1-microsecond simulation in aqueous solution, Science 282(5389), 1998, 740-744
    locator: a microsecond simulation of the villin headpiece in explicit water
  - paper: doi:10.1126/science.1187409
    title: David E. Shaw et al., Atomic-level characterization of the structural dynamics of proteins, Science 330(6002), 2010, 341-346
    locator: millisecond simulations on the special-purpose machine Anton
  - paper: doi:10.1126/science.1208351
    title: Kresten Lindorff-Larsen, Stefano Piana, Ron O. Dror and David E. Shaw, How fast-folding proteins fold, Science 334(6055), 2011, 517-520
    locator: the folding of 12 small proteins in equilibrium simulations
  - book: doi:10.1016/B978-0-12-267351-1.X5000-7
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the chapter on molecular dynamics simulations
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: the chapters on molecular dynamics and on periodic boundary conditions
---

Molecular dynamics simulates the motion of the atoms of a molecule, often with the water around it, by integrating Newton's equations of motion $m_i \ddot{x}_i = -\nabla_i U(x)$, where $U$ is a force field, a physical [energy function](/energy-function/). The standard integrator is the velocity form of [Verlet integration](/verlet-integration/): each time step does a half kick of the velocities, a drift of the positions, one evaluation of the forces and a second half kick. The method is time-reversible and symplectic, so the total energy has no drift over long runs, and the total momentum is conserved. For proteins, the time step is about 1 to 2 fs, and the force evaluation dominates the cost. Molecular dynamics is the physics-based approach to [ab initio protein folding](/ab-initio-protein-folding/), and it is a main tool for studying how proteins move.

## In plain words

Each atom is a small ball with a mass. The force field says how hard each ball is pushed by every other ball: bonds act like springs, atoms that come too close push apart, and charges attract or repel. Molecular dynamics moves all the balls forward in time in very small steps.

At each step it computes all the pushes, changes the speed of each ball a little, and moves each ball a little. Repeat this many millions of times and you have a film of the molecule. The steps must be shorter than the fastest motion in the molecule, the vibration of light hydrogen atoms, or the film becomes nonsense. So even a long run covers only a short real time. This is why a computer needs a very long time to watch a protein fold.

## The problem

The input is the positions $x_i \in \mathbb{R}^3$, the velocities $v_i$ and the masses $m_i > 0$ of $N$ atoms, a force field that returns the potential energy $U(x)$ and the forces $f_i = -\nabla_i U(x)$, a time step $h > 0$ and a number of steps $S$. The output is an approximation of the trajectory of the system
$$\dot{x}_i = v_i, \qquad m_i \dot{v}_i = f_i(x),$$
at the times $h, 2h, \ldots, S h$. The system is Hamiltonian, with total energy $H = \sum_i \frac12 m_i |v_i|^2 + U(x)$, which the exact flow conserves. A periodic box of side $L$ is often used to model a bulk solution: then each atom interacts with the nearest image of every other atom, the minimum image convention, and atoms that leave the box enter it again on the opposite side.

The implementation includes two force fields: independent springs $U = \frac{k}{2} \sum_i |x_i|^2$, for tests with exact solutions, and the Lennard-Jones pair potential $U(r) = 4\epsilon\bigl((\sigma/r)^{12} - (\sigma/r)^6\bigr)$, optionally cut at a distance $r_c \le L/2$ and shifted so that $U(r_c) = 0$.

## The algorithm

```pseudo id=main
MOLECULAR-DYNAMICS(x, v, m, FORCES, h, S)
L1  (U, f) ← FORCES(x);  record K(v) + U
L2  for step ← 1 to S do
L3      v_i ← v_i + (h / 2) f_i / m_i for each atom i          ▷ half kick
L4      x_i ← x_i + h v_i for each atom i, wrapped into the box  ▷ drift
L5      (U, f) ← FORCES(x)                                     ▷ the one force evaluation
L6      v_i ← v_i + (h / 2) f_i / m_i for each atom i          ▷ half kick
L7      record K(v) + U
L8  return (x, v, the recorded energies)
```

Here $K(v) = \sum_i \frac12 m_i |v_i|^2$ is the kinetic energy. The forces of line L5 are kept for line L3 of the next step, so each step costs one force evaluation. Lines L3 and L6 together are a full kick of $h f_i / m_i$ between two drifts, which is the leapfrog form of the same method. The Lennard-Jones forces are $f_i = \sum_{j \ne i} 24\epsilon \bigl(2 (\sigma/r_{ij})^{12} - (\sigma/r_{ij})^6\bigr) r_{ij} / |r_{ij}|^2$ with $r_{ij}$ the minimum image of $x_i - x_j$, computed once for each pair and added to $i$ and subtracted from $j$.

## Example

**A spring with an exact solution.** One atom with $m = 1$ on a spring with $k = 1$, starting at $x = 1$ and $v = 0$. The exact motion is $x(t) = \cos t$, and the energy is $\frac12$. With $h = 0.1$:

| step | $t$ | $x$ | $\cos t$ | $v$ | $-\sin t$ | $K + U$ |
|---|---|---|---|---|---|---|
| 1 | 0.1 | 0.995000 | 0.995004 | $-0.099750$ | $-0.099833$ | 0.4999875 |
| 2 | 0.2 | 0.980050 | 0.980067 | $-0.198503$ | $-0.198669$ | 0.4999506 |
| 3 | 0.3 | 0.955300 | 0.955336 | $-0.295270$ | $-0.295520$ | 0.4998907 |

In step 1, line L3 gives $v = 0 - 0.05 \cdot 1 = -0.05$, line L4 gives $x = 1 - 0.1 \cdot 0.05 = 0.995$, line L5 gives $f = -0.995$, and line L6 gives $v = -0.05 - 0.05 \cdot 0.995 = -0.09975$. At $t = 10$:

| $h$ | steps | $\lvert x - \cos 10 \rvert$ | largest $\lvert H - \frac12 \rvert$ |
|---|---|---|---|
| 0.1 | 100 | $2.277 \times 10^{-3}$ | $1.250 \times 10^{-3}$ |
| 0.05 | 200 | $5.673 \times 10^{-4}$ | $3.125 \times 10^{-4}$ |
| 0.025 | 400 | $1.417 \times 10^{-4}$ | $7.812 \times 10^{-5}$ |

Halving $h$ divides both errors by 4, which shows order 2. The energy error does not grow with time. For this system the method conserves $v^2 + (1 - h^2/4) x^2$ exactly (see [Verlet integration](/verlet-integration/)), so $H - \frac12 = \frac{h^2}{8}(x^2 - 1)$, whose largest size is $h^2 / 8$, the values in the last column.

**A Lennard-Jones cluster.** Put 8 atoms with $\epsilon = \sigma = m = 1$ at the corners of a cube of side $2^{1/6}$, where each edge pair is at the minimum of the pair potential. The potential energy is $-15.1033$. Give the atoms random velocities (seed 1, normal with standard deviation 0.5, with the mean removed), so that $K = 2.5706$ and $H = -12.5327$. Run without a box to $t = 2.5$:

| $h$ | steps | largest $\lvert H - H_0 \rvert$ | largest $\lvert \sum_i m_i v_i \rvert$ component |
|---|---|---|---|
| 0.01 | 250 | $1.127 \times 10^{-2}$ | $2.2 \times 10^{-15}$ |
| 0.005 | 500 | $2.928 \times 10^{-3}$ | $3.4 \times 10^{-15}$ |
| 0.0025 | 1000 | $7.354 \times 10^{-4}$ | $3.3 \times 10^{-15}$ |

The energy error falls by a factor of 3.85 and then 3.98 when $h$ is halved, so it is $O(h^2)$. The momentum is zero up to rounding, because the pair forces cancel.

**The time step of a protein.** The fastest motion in a protein is the stretch of a bond to a hydrogen atom, with a period of about 11 fs for a C-H bond. For a harmonic motion of angular frequency $\omega$, Verlet is stable only for $h \omega < 2$, that is, for $h < T / \pi \approx 3.5$ fs with the period $T$. For accuracy, simulations use $h = 1$ fs, or 2 fs when the lengths of the bonds to hydrogen are held fixed by constraints. One microsecond then takes $5 \times 10^8$ steps.

## Correctness

The algorithm computes the velocity Verlet map exactly, up to rounding, and the properties of that map are proved on the [Verlet integration](/verlet-integration/) page: it is a method of order 2, it is symplectic, and its energy error stays bounded over exponentially long times for a small enough $h$ by backward error analysis. On this page the proof below shows the claims that depend on the force field and on the box:

1. **The loop is velocity Verlet.** Lines L3 to L6 apply a half kick, a drift and a half kick, with the forces at the start and at the end of the step.
2. **Momentum.** For a force field made of pair forces, such as Lennard-Jones with or without a periodic box, $\sum_i m_i v_i$ does not change.
3. **Time reversal.** If the run from $(x, v)$ for $S$ steps ends at $(x', v')$, then the run from $(x', -v')$ for $S$ steps ends at $(x, -v)$, up to a shift by a multiple of the box.
4. **The recorded energy is exact.** The $s$-th recorded value is $H$ at the state after step $s$.

Energy is not conserved exactly. The recorded $H$ oscillates with an amplitude of $O(h^2)$, as the examples show. A drift of $H$ over a long run is a sign of a bug, a step that is too large, or a force field that is not smooth, such as a cutoff without a shift.

## Complexity

Each step does $O(N)$ work in lines L3, L4 and L6 and one force evaluation in line L5. The all-pairs force loop of the implementation costs $\Theta(N^2)$ time, so $S$ steps cost $O(S N^2)$ time and $O(N)$ extra space.

Production programs make the force evaluation faster:

- **Cutoff with cell or neighbour lists.** Short-range forces only need the pairs within $r_c$. A grid of cells of side $r_c$, or a list of neighbours that is rebuilt every few steps, finds them in $O(N)$ time at a fixed density.
- **Particle mesh Ewald.** The long-range Coulomb sum in a periodic box is split into a short-range part and a smooth part on a grid, which the [fast Fourier transform](/fast-fourier-transform/) computes in $O(N \log N)$ time.
- **Parallel hardware.** Spatial decomposition over many processors, graphics processors, and special-purpose machines such as Anton (Shaw et al. 2010).

The number of steps is the real limit. A protein in water has tens of thousands of atoms or more, and a folding event of 1 ms needs about $5 \times 10^{11}$ steps at 2 fs.

## Properties

- **Deterministic.** The same input gives the same trajectory. Chaos makes two runs that differ by rounding diverge after a short time, but their statistics agree.
- **Symplectic and time-reversible.** These properties are the reason for the good energy behaviour. See [symplectic integrators](/symplectic-integrators/).
- **Conservation laws.** Total momentum is conserved for pair forces. Angular momentum is conserved without a box. Energy is conserved only approximately.
- **Ensemble.** Without a thermostat, the method samples the microcanonical ensemble, at a fixed number of atoms, volume and energy, if the dynamics is ergodic.
- **One force evaluation per step.** The same cost as the Euler method, with much better long-time behaviour.

## Variants and improvements

- **Thermostats and barostats.** Langevin dynamics adds friction and random forces, and the Nosé-Hoover method adds an extra variable, so that the system samples the canonical ensemble at a temperature $T$ with the Boltzmann distribution $e^{-H/k_B T}$. Barostats keep the pressure fixed.
- **Constraints.** Holding the bond lengths to hydrogen fixed, with the SHAKE or LINCS algorithms, removes the fastest motion and allows $h = 2$ fs.
- **Multiple time steps.** Slowly varying forces, such as the long-range part, are computed less often than the fast ones (RESPA).
- **Enhanced sampling.** Replica exchange over temperatures ([parallel tempering](/parallel-tempering/)), umbrella sampling and metadynamics help the system cross the barriers of its [energy landscape](/energy-landscape/).
- **Coarse-grained models.** Several atoms are grouped into one bead, which allows larger steps and fewer particles.
- **Sampling.** [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) uses the same leapfrog trajectories as proposals for a Metropolis test, so that it samples a distribution exactly.

## When to use it

Use molecular dynamics to study how a molecule moves: the flexibility of a protein, the binding of a ligand, the effect of a mutation, or the folding of a small fast-folding protein. It needs a force field and a starting structure. For prediction of a fold, it is useful as a refinement of a model, or for small proteins that fold in microseconds. For most proteins, [fragment assembly](/fragment-assembly/), [Rosetta](/rosetta/) or [AlphaFold](/alphafold/) predicts a fold far faster. To sample an equilibrium distribution and not the dynamics, Monte Carlo methods can be faster, because their moves need not follow a physical path.

## Pitfalls

- **A time step that is too large.** The energy grows quickly, and the simulation fails. Check the energy in a test run without a thermostat.
- **A cutoff without a shift.** The potential jumps at $r_c$, and the energy is not conserved. Shift or smooth the potential.
- **A cutoff longer than half the box.** The minimum image convention then misses pairs. The implementation raises an error in this case.
- **A thermostat that hides errors.** A thermostat removes the energy that a bad integrator adds, so the run looks stable but samples the wrong distribution. Test the integrator without it.
- **Too short a run.** A simulation that is shorter than the time scale of the event gives no information about the event. A protein that folds in 1 ms is not seen to fold in 1 µs.
- **The force field decides the answer.** A perfect integration of a wrong force field gives a wrong structure.

## Implementations

## History

Alder and Wainwright (1957) simulated a system of hard spheres, the first molecular dynamics simulation. Rahman (1964) simulated liquid argon with a Lennard-Jones potential. Verlet (1967) used the integrator for a Lennard-Jones fluid, together with a list of neighbours for each atom, and Swope, Andersen, Berens and Wilson (1982) gave its velocity form. McCammon, Gelin and Karplus (1977) simulated a small protein, the bovine pancreatic trypsin inhibitor, for a few picoseconds. Duan and Kollman (1998) simulated the villin headpiece for 1 µs in water. Shaw and others (2010) reached 1 ms on Anton, and Lindorff-Larsen, Piana, Dror and Shaw (2011) folded 12 small proteins in long equilibrium simulations. Karplus, Levitt and Warshel shared the 2013 Nobel Prize in Chemistry for multiscale models of complex chemical systems.

## References
