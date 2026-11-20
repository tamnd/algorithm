---
tag: KR4Y5Q
kind: algorithm
slug: born-oppenheimer-molecular-dynamics
name: Born-Oppenheimer molecular dynamics
aliases:
- ab initio molecular dynamics
area: scientific-computing/molecular-simulation
level: advanced
summary: Moves the nuclei classically on forces from an electronic structure calculation solved to self-consistency at every step.
model: real-ram
complexity:
  vars: {T: the number of time steps, I: the number of SCF iterations per step, C: the cost of one SCF iteration}
  time: {worst: O(T I C)}
  space: {extra: O(C)}
properties: {deterministic: true, randomized: false, iterative: true}
history:
  year: 1978
  people: [Claude Leforestier]
  note: Early work computed classical trajectories of a small reaction on the ab initio energy and its gradient, evaluated afresh at each step; with density functional theory and fast SCF methods the approach became a standard tool for condensed matter.
prereqs: [molecular-dynamics, verlet-integration, eigenvalue-problem, fixed-point-iteration]
see_also: [car-parrinello-molecular-dynamics, qm-mm-method, interatomic-potential, behler-parrinello-potential, jacobi-eigenvalue-algorithm, symplectic-integrators, shadow-hamiltonian, energy-landscape]
sources:
  - book: isbn:9780521898638
    title: Dominik Marx and Jürg Hutter, Ab Initio Molecular Dynamics, Basic Theory and Advanced Methods, Cambridge University Press, 2009
    locator: the chapter on the theory of ab initio molecular dynamics, the sections on Born-Oppenheimer molecular dynamics and on the Hellmann-Feynman forces
  - paper: doi:10.1103/PhysRevLett.100.123004
    title: Anders M. N. Niklasson, Extended Born-Oppenheimer molecular dynamics, Physical Review Letters 100, 123004, 2008
    locator: the loss of time reversibility and the energy drift caused by the SCF initial guess, and the extended Lagrangian that restores reversibility
  - paper: doi:10.1103/PhysRevLett.55.2471
    title: Roberto Car and Michele Parrinello, Unified approach for molecular dynamics and density-functional theory, Physical Review Letters 55, 2471-2474, 1985
    locator: the alternative to solving the electrons at every step, used for comparison
---

Born-Oppenheimer molecular dynamics (BOMD) moves the nuclei of a molecule or a solid by Newton's laws on forces computed from quantum mechanics. At each time step the electronic structure problem, usually Kohn-Sham density functional theory or Hartree-Fock, is solved by a self-consistent field (SCF) iteration for the current nuclear positions; the forces then follow from the Hellmann-Feynman theorem, and the nuclei move by [velocity Verlet](/verlet-integration/). The name comes from the Born-Oppenheimer approximation: the electrons are light and fast, so they stay in their ground state for the current nuclei, and the nuclei move on the ground-state energy surface. Compared with [molecular dynamics](/molecular-dynamics/) on an [interatomic potential](/interatomic-potential/), BOMD needs no fitted force field and can break and form bonds, at a cost thousands of times higher per step. [Car-Parrinello molecular dynamics](/car-parrinello-molecular-dynamics/) avoids the SCF at each step by moving the orbitals too. The code on this page uses a toy electronic model with one orbital per atom, not a real quantum chemistry method.

## In plain words

In a molecule, the electrons are much lighter than the nuclei and move much faster. For every arrangement of the nuclei, they settle almost at once into their lowest energy state.

BOMD uses this. At each small time step it holds the nuclei still, solves for the electrons, and computes the forces that the electrons and the other nuclei put on each nucleus. Then it moves the nuclei a little according to those forces, and repeats.

The electrons are solved by a repeated guess-and-correct loop. If that loop is stopped too early, the forces are slightly wrong, and the total energy slowly drifts.

## The problem

The input is the nuclear positions $X$, velocities $V$ and masses $M$, a time step $h$, and an electronic structure method: for given $X$, an energy $E(X, c)$ of the electronic state $c$ (orbitals or density). The Born-Oppenheimer energy is
$$E_{\text{BO}}(X) = \min_c E(X, c)$$
under the constraints on $c$, such as orthonormal orbitals. The task is to integrate
$$M_k \ddot X_k = -\frac{\partial E_{\text{BO}}}{\partial X_k}.$$
In this page's toy model, $N$ atoms sit on a line with one orbital each, the hopping $t(r) = -t_0 e^{-a(r - d_0)}$ forms the matrix $H_0(X)$, two electrons fill the lowest orbital $c$ with $|c| = 1$, and
$$E(X, c) = 2 c^T H_0(X) c + U \sum_i c_i^4 + \sum_{i < j} A e^{-b(r_{ij} - d_0)}.$$
The quartic term is a mean-field on-site repulsion, which makes the problem self-consistent: $c$ is the lowest eigenvector of $H(c) = H_0 + U\,\mathrm{diag}(c_i^2)$ (Claim 1 of the proof).

## The algorithm

```pseudo id=main
BOMD(X, V, M, h, steps)
L1  c ← SCF(X)                                   ▷ electronic ground state at the start
L2  F ← -dE/dX at fixed c                        ▷ Hellmann-Feynman forces
L3  for n ← 1 to steps do
L4      V ← V + (h / 2) F / M
L5      X ← X + h V
L6      c ← SCF(X), started from the previous density
L7      F ← -dE/dX at fixed c
L8      V ← V + (h / 2) F / M
L9  return the trajectory and the total energies E_BO(X) + (1/2) V^T M V
```

Line L6 is the costly part. The SCF loop builds $H$ from the current density, takes its lowest eigenvector (here by the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/)), mixes the new density with the old one, and repeats until the density changes by less than a tolerance. Starting from the previous step's density saves iterations. Line L7 uses the Hellmann-Feynman theorem: at a self-consistent $c$, the derivative of $E_{\text{BO}}$ is the partial derivative of $E$ at fixed $c$, so no derivative of the orbitals is needed. Lines L4, L5 and L8 are velocity Verlet.

## Example

**A dimer with $U = 0$.** With $t_0 = a = d_0 = A = 1$ and $b = 2$, the lowest orbital of two atoms has energy $-|t(r)|$, so $E_{\text{BO}}(r) = -2e^{-(r - 1)} + e^{-2(r - 1)}$, a Morse curve with minimum $-1$ at $r = 1$ and curvature $E'' = 2$. The SCF reproduces this to rounding.

**A chain of four atoms with $U = 1$.** At $X = (0, 1.1, 2.0, 3.2)$ the SCF converges in 25 iterations with mixing 0.5 to $E_{\text{BO}} = -0.589106$. The Hellmann-Feynman forces agree with centred finite differences of $E_{\text{BO}}$ to $2 \times 10^{-10}$. After one SCF iteration only, the density residual is 0.11 and the forces are visibly wrong.

**Energy conservation.** Start with $V = (0.3, -0.2, 0.1, -0.2)$, unit masses, $h = 0.05$, 1000 steps:

| SCF | total energy drift | note |
|---|---|---|
| tolerance $10^{-10}$ | $2.35 \times 10^{-6}$ | the energy oscillates with spread $5.6 \times 10^{-4}$ |
| tolerance $10^{-3}$ | $3.0 \times 10^{-3}$ | |
| one iteration per step | 0.035 | |

With the tight SCF the energy oscillates but does not drift, as expected of a symplectic integrator on an exact potential. The spread over a time of 50 was $1.38 \times 10^{-3}$ at $h = 0.1$, $5.65 \times 10^{-4}$ at $h = 0.05$ and $1.39 \times 10^{-4}$ at $h = 0.025$: it falls by about 4 when $h$ halves, so it is second order. With a loose SCF the forces are not the gradient of any energy, and the energy drifts.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows, for the toy model:

1. **SCF fixed points are stationary points.** On the sphere $|c| = 1$, $E$ is stationary in $c$ exactly when $c$ is an eigenvector of $H(c) = H_0 + U\,\mathrm{diag}(c_i^2)$.
2. **Hellmann-Feynman forces.** If $c(X)$ is a stationary point that depends smoothly on $X$, then $dE_{\text{BO}}/dX_k = \partial E / \partial X_k$ at fixed $c$, which is the formula of the code.
3. **Energy errors are second order, force errors first order.** If $c$ is off the stationary point by $\delta$, the energy is off by $O(|\delta|^2)$ but the force by $O(|\delta|)$.
4. **The dynamics.** With exact forces, $E_{\text{BO}} + \frac12 V^T M V$ is conserved by the exact flow, and velocity Verlet is a symplectic, time-reversible, second-order method for it.
5. **The dimer.** For $U = 0$ and two atoms, $E_{\text{BO}}(r) = -2 t_0 e^{-a(r - d_0)} + A e^{-b(r - d_0)}$.

## Complexity

Each step costs $I$ SCF iterations of cost $C$ each plus the forces. For the toy model one iteration is a dense eigenproblem, $C = O(N^3)$. For Kohn-Sham DFT with plane waves, $C$ is dominated by fast Fourier transforms and by orthogonalization, which grows like $O(N^3)$ in the number of electrons for large systems. The total is $O(T I C)$, and good initial guesses reduce $I$ to about 5 to 15 per step in practice. The extra space is that of one electronic structure calculation.

## Properties

- **Exact on the BO surface** in the limit of a converged SCF: no force field and no fitting.
- **Bonds can break and form**, since the energy comes from the electrons.
- **Symplectic** in the nuclei when the SCF is fully converged; then there is no long-time drift.
- **Not exactly time reversible** in practice: the SCF starts from the previous step's density, which breaks the symmetry between forward and backward steps and causes drift for loose tolerances (Niklasson 2008).
- **Large time steps.** The time step is set by the nuclear motion, about 0.5 to 1 fs, not by the electrons.
- **Ground state only.** It cannot describe processes where several electronic states mix.

## Variants and improvements

- **Extended Lagrangian BOMD** (Niklasson 2008). An auxiliary density moves with a time-reversible integrator and serves as the SCF initial guess, which removes the drift even with few SCF iterations.
- **Extrapolation of the initial guess** from several previous steps.
- **Car-Parrinello molecular dynamics.** The orbitals move as fictitious classical variables, and no SCF is solved at each step.
- **QM/MM.** Only a small region is treated by BOMD and the rest by a force field; see the [QM/MM method](/qm-mm-method/).
- **Machine-learned potentials.** BOMD data are used to fit potentials such as the [Behler-Parrinello potential](/behler-parrinello-potential/), which then run much faster.

## When to use it

Use BOMD when the chemistry matters: bond breaking, proton transfer, reactions at surfaces, liquids where polarization and charge transfer are important, or any system with no reliable force field. It is the standard method for ab initio molecular dynamics with modern codes. For long or large simulations, use it to generate training data for a machine-learned potential, or restrict it to a QM region.

## Pitfalls

- **Loose SCF.** Forces are not the gradient of the energy and the energy drifts; tighten the tolerance or use extended Lagrangian BOMD.
- **Pulay forces.** With basis functions that move with the atoms, as with Gaussian orbitals, the force has extra terms beyond Hellmann-Feynman; plane waves do not have them.
- **SCF failure.** Near level crossings or for metals, the SCF can converge slowly or to the wrong state; use smearing or better mixing.
- **Small systems and short times.** The cost limits BOMD to hundreds of atoms and tens of picoseconds; statistics are poor.
- **Toy model.** The code here is a toy with one orbital per atom; it shows the structure of BOMD, not real chemistry.

## Implementations

## History

Early ab initio trajectory studies, such as that of Leforestier (1978) on a small reaction, evaluated the quantum chemical energy and gradient at every step of a classical trajectory. Car and Parrinello (1985) showed how to avoid the full electronic minimization at each step, and for some years their method dominated condensed-matter work. With better SCF methods and initial guesses, Born-Oppenheimer dynamics with density functional theory became the more common approach. Niklasson (2008) explained the energy drift of BOMD by the broken time reversibility of the SCF initial guess and removed it with an extended Lagrangian. Marx and Hutter (2009) treat both methods in one book.

## References
