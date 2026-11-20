---
tag: PQJARX
kind: algorithm
slug: car-parrinello-molecular-dynamics
name: Car-Parrinello molecular dynamics
aliases:
- CPMD
area: scientific-computing/molecular-simulation
level: advanced
summary: "Propagates electronic orbitals as fictitious classical variables together with the nuclei, so ab initio forces need no full electronic minimization each step."
model: real-ram
complexity:
  vars: {T: the number of time steps, C: the cost of one energy and force evaluation}
  time: {worst: O(T C)}
  space: {extra: O(C)}
properties: {deterministic: true, randomized: false, iterative: false}
history:
  year: 1985
  people: [Roberto Car, Michele Parrinello]
  note: Car and Parrinello wrote one Lagrangian for the nuclei and the Kohn-Sham orbitals, with a fictitious mass for the orbitals, and so made ab initio molecular dynamics with density functional theory practical.
prereqs: [born-oppenheimer-molecular-dynamics, verlet-integration, rattle-algorithm, lagrange-multiplier]
see_also: [shake-constraint-algorithm, qm-mm-method, hamiltonian-systems, symplectic-integrators, molecular-dynamics, nose-hoover-thermostat, behler-parrinello-potential, interatomic-potential]
sources:
  - paper: doi:10.1103/PhysRevLett.55.2471
    title: Roberto Car and Michele Parrinello, Unified approach for molecular dynamics and density-functional theory, Physical Review Letters 55, 2471-2474, 1985
    locator: the extended Lagrangian with fictitious orbital dynamics and the orthonormality constraints
  - paper: doi:10.1103/PhysRevA.44.6334
    title: Giorgio Pastore, Enrico Smargiassi and Francesco Buda, Theory of ab initio molecular-dynamics calculations, Physical Review A 44(10), 1991, 6334-6347
    locator: the analysis of adiabatic separation between the fictitious electron dynamics and the nuclei, and the role of the gap and the fictitious mass
  - book: isbn:9780521898638
    title: Dominik Marx and Jürg Hutter, Ab Initio Molecular Dynamics, Basic Theory and Advanced Methods, Cambridge University Press, 2009
    locator: the chapter on the theory of ab initio molecular dynamics, the sections on Car-Parrinello molecular dynamics, the fictitious mass and adiabaticity
---

Car-Parrinello molecular dynamics (CPMD) is ab initio molecular dynamics in which the electronic orbitals are not solved at each step but move with the nuclei as classical variables. Car and Parrinello (1985) wrote one Lagrangian with the nuclear kinetic energy, a fictitious kinetic energy $\frac{\mu}{2} |\dot c|^2$ of the orbitals with a small fictitious mass $\mu$, the electronic energy $E(X, c)$, and Lagrange multipliers that keep the orbitals orthonormal. Started at the electronic ground state, the orbitals then oscillate fast and with small amplitude around the instantaneous ground state, and the nuclei move almost on the Born-Oppenheimer surface. Each step costs one energy and force evaluation, with no self-consistent field (SCF) loop, but the time step must resolve the fast orbital motion. The method has a conserved energy and no SCF drift, and its error is controlled by $\mu$. Compare [Born-Oppenheimer molecular dynamics](/born-oppenheimer-molecular-dynamics/), which solves the SCF at each step. The code on this page uses the same toy electronic model as the BOMD page, not a real quantum chemistry method.

## In plain words

In ordinary ab initio dynamics, the electrons are solved from scratch at every step, which costs many inner iterations.

Car and Parrinello let the electrons move along with the nuclei instead. The electronic state gets a small artificial mass and is pushed by the same energy that holds the nuclei together. Because this mass is small, the electronic state follows the nuclei closely, like a light dog on a short leash that stays near its owner.

Each step is then cheap, but the steps must be short, since the light electronic state moves fast. The answer is slightly off from the exact ground state, by an amount that shrinks with the artificial mass.

## The problem

The input is the nuclear positions $X$, velocities $V$ and masses $M$, an initial electronic state $c$ (usually the ground state for $X$) with velocity $\dot c = 0$, the fictitious mass $\mu$, and the time step $h$. For one orbital with the constraint $|c| = 1$, the Car-Parrinello Lagrangian is
$$\mathcal L = \sum_k \frac{M_k}{2} \dot x_k^2 + \frac{\mu}{2} |\dot c|^2 - E(X, c) + \Lambda (|c|^2 - 1),$$
and its equations of motion are
$$M_k \ddot x_k = -\frac{\partial E}{\partial x_k}, \qquad \mu \ddot c = -\nabla_c E + 2 \Lambda c,$$
with $\Lambda$ chosen so that $|c| = 1$ at all times. The conserved energy is $E_{\text{cons}} = \sum_k \frac{M_k}{2} \dot x_k^2 + \frac{\mu}{2} |\dot c|^2 + E(X, c)$ (Claim 1 of the proof). The toy model is the one of the BOMD page: one orbital per atom on a line, $E(X, c) = 2 c^T H_0(X) c + U \sum_i c_i^4 + \Phi(X)$.

## The algorithm

```pseudo id=main
CPMD(X, V, M, c, cdot, mu, h, steps)
L1  F_X ← -dE/dX at (X, c); F_c ← -grad_c E at (X, c)
L2  for n ← 1 to steps do
L3      V ← V + (h / 2) F_X / M; X ← X + h V
L4      cdot ← cdot + (h / 2) F_c / mu
L5      c ← c + h cdot + lambda c_old, with lambda chosen so |c| = 1; cdot ← cdot + lambda c_old / h   ▷ SHAKE
L6      F_X ← -dE/dX at (X, c); F_c ← -grad_c E at (X, c)
L7      V ← V + (h / 2) F_X / M; cdot ← cdot + (h / 2) F_c / mu
L8      cdot ← cdot - (c . cdot) c                               ▷ RATTLE
L9  return the trajectory and E_cons
```

This is velocity Verlet for the nuclei and the orbital together, with the constraint $|c| = 1$ kept by SHAKE on the positions and RATTLE on the velocities, as in the [RATTLE algorithm](/rattle-algorithm/). Line L5 solves the quadratic $|d + \lambda c_{\text{old}}|^2 = 1$ with $d = c_{\text{old}} + h \dot c$, whose root of smaller size is $\lambda = -d \cdot c_{\text{old}} + \sqrt{(d \cdot c_{\text{old}})^2 - |d|^2 + 1}$. Line L8 removes the part of $\dot c$ along $c$, so that $\frac{d}{dt}|c|^2 = 2 c \cdot \dot c = 0$. For many orbitals the same steps keep the orbitals orthonormal with a matrix of multipliers. The nuclear force in line L6 is the partial derivative at the current $c$, which is not exactly the Born-Oppenheimer force, because $c$ is not exactly the ground state.

## Example

**Orbital frequency.** For the dimer with $U = 0$ at fixed distance $r = 1$, the two orbital energies are $\mp 1$, a gap $\Delta = 2$. Near the ground state the orbital oscillates with angular frequency $\omega = 2\sqrt{\Delta / \mu}$ (Claim 3). With $h = 0.002$, the measured $\omega$ was 28.268 against $2\sqrt{2/0.01} = 28.284$ for $\mu = 0.01$, and 14.134 against 14.142 for $\mu = 0.04$.

**The chain.** Four atoms with $U = 1$, $X = (0, 1.1, 2.0, 3.2)$, $V = (0.3, -0.2, 0.1, -0.2)$ and unit masses, started at the self-consistent ground state with $\dot c = 0$, run for a time of 10 and compared with BOMD with a tight SCF at the same time step:

| $\mu$ | $h$ | spread of $E_{\text{cons}}$ | largest fictitious kinetic energy | largest $\lvert x_{\text{CP}} - x_{\text{BO}} \rvert$ | largest $E$ above the BO surface |
|---|---|---|---|---|---|
| 0.002 | 0.002 | $6.1 \times 10^{-7}$ | $5.4 \times 10^{-5}$ | $8.6 \times 10^{-4}$ | $1.2 \times 10^{-5}$ |
| 0.01 | 0.004 | $2.4 \times 10^{-6}$ | $2.5 \times 10^{-4}$ | $4.3 \times 10^{-3}$ | $5.6 \times 10^{-5}$ |
| 0.05 | 0.01 | $1.5 \times 10^{-5}$ | $1.2 \times 10^{-3}$ | 0.022 | $2.3 \times 10^{-4}$ |
| 0.2 | 0.01 | $1.4 \times 10^{-5}$ | $3.9 \times 10^{-3}$ | 0.099 | $2.0 \times 10^{-3}$ |

The mean nuclear kinetic energy was about 0.212, so the fictitious kinetic energy stays a small fraction of it, which is the adiabatic regime. The deviation of the trajectory from BOMD grows about linearly in $\mu$. The norm $|c|$ stayed 1 to $10^{-15}$. The self-consistent orbital energies of the chain at the start are $-1.641, 0.086, 0.923, 1.632$, a gap of 1.73, so the slowest orbital frequency for $\mu = 0.2$ is about $2\sqrt{1.73/0.2} \approx 5.9$, not far above the nuclear frequencies: this is where the error becomes large.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The conserved energy.** The exact Car-Parrinello equations with the constraint conserve $E_{\text{cons}}$.
2. **The constraint steps.** The SHAKE step of line L5 has a real root exactly when $h |\dot c_\perp| \le 1$, where $\dot c_\perp$ is the part of $\dot c$ orthogonal to $c_{\text{old}}$, and then $|c| = 1$ after the step; the RATTLE step of line L8 makes $c \cdot \dot c = 0$ with the smallest change of $\dot c$.
3. **The orbital frequency.** For $U = 0$ and fixed nuclei, the motion of $c$ stays in the plane of the ground state and any other eigenvector, and small oscillations about the ground state have angular frequency $2\sqrt{\Delta / \mu}$, where $\Delta$ is the eigenvalue gap.

The claim that the nuclei follow the BO surface with an error that vanishes as $\mu \to 0$ is the adiabatic argument of Car and Parrinello and of Pastore, Smargiassi and Buda (1991). It is not proved here; the table above measures it.

## Complexity

Each step costs one evaluation of $E$, $\nabla_c E$ and $\partial E / \partial X$, of cost $C$, plus the orthonormality constraint. For plane-wave DFT with many orbitals, the orthonormalization costs $O(N^3)$ per step, the same order as one SCF iteration. Over $T$ steps the time is $O(T C)$, with no SCF loop. The time step must resolve the fastest orbital frequency $\omega_{\max} \sim \sqrt{E_{\text{cut}} / \mu}$ for a plane-wave cutoff $E_{\text{cut}}$, so it is typically 5 to 10 times smaller than for BOMD. Whether CPMD or BOMD is faster depends on the system: CPMD saves the SCF iterations but needs more steps.

## Properties

- **No SCF at each step**, and so no SCF tolerance and no drift from an incomplete SCF.
- **A conserved energy**, $E_{\text{cons}}$, for the extended system; velocity Verlet with RATTLE is symplectic and time reversible for it.
- **Close to the BO surface, not on it.** The orbitals lag the ground state and add an error that grows with $\mu$; the nuclei also feel a drag, as if their mass were larger.
- **Needs a gap.** The adiabatic separation needs the lowest orbital frequency $2\sqrt{\Delta / \mu}$ to stay well above the nuclear frequencies; in metals, with no gap, the orbitals heat up.
- **Small time steps**, set by $\mu$ and the plane-wave cutoff.

## Variants and improvements

- **Thermostats on the orbitals.** A [Nosé-Hoover thermostat](/nose-hoover-thermostat/) on the orbital degrees of freedom keeps the fictitious kinetic energy low, which is needed for metals and small gaps.
- **Mass preconditioning.** Different fictitious masses for different plane waves reduce the highest frequency and allow larger steps.
- **Extended Lagrangian BOMD** (Niklasson 2008) borrows the idea of an auxiliary electronic variable but uses it as the initial guess of an SCF.
- **Car-Parrinello QM/MM.** Only a small region is treated by CPMD; see the [QM/MM method](/qm-mm-method/).

## When to use it

Use CPMD for insulators and semiconductors with a clear gap, large systems where one SCF solve per step is expensive, and simulations where strict energy conservation matters. For metals, for systems with small gaps, or when large time steps are wanted, BOMD with a good initial guess is usually simpler. Check adiabaticity by monitoring the fictitious kinetic energy: it should stay small and not grow.

## Pitfalls

- **Fictitious mass too large.** The orbitals lag the nuclei, the forces are wrong, and energy flows from the nuclei into the orbitals; the nuclear temperature drops.
- **Not starting at the ground state.** The orbitals must be minimized before the run, or they carry a large fictitious kinetic energy from the start.
- **Small gaps and metals.** The orbital and nuclear frequencies overlap and adiabaticity is lost.
- **Time step too large** for the orbital frequency; the run becomes unstable.
- **Mass renormalization.** The nuclei behave as if slightly heavier, which changes vibrational frequencies by an amount that grows with $\mu$.
- **Toy model.** The code here is a toy with one orbital; it shows the structure of CPMD, not real chemistry.

## Implementations

## History

Car and Parrinello (1985) introduced the method, which made ab initio molecular dynamics with density functional theory practical for condensed matter and started a large field. Pastore, Smargiassi and Buda (1991) analysed why the fictitious electron dynamics stays close to the ground state, in terms of the gap and the fictitious mass. Later, better SCF methods made Born-Oppenheimer dynamics competitive again, and Marx and Hutter (2009) treat both methods in one book.

## References
