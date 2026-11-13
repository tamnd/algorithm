---
tag: TKS4T9
kind: algorithm
slug: quantum-imaginary-time-evolution
name: Quantum imaginary time evolution
aliases:
- imaginary-time evolution
- QITE
- quantum imaginary-time evolution algorithm
area: quantum/quantum-simulation
level: research
summary: "Motta et al. (2020): follow the normalized flow e^(-tau H)|psi> toward the ground state with unitary steps only, each one found by least squares on a few qubits around a term of H."
solves: [ground-state-preparation]
model: quantum-circuit-model
complexity:
  vars: {n: the number of qubits, M: the number of terms of H, D: the number of qubits in a domain, T: the number of steps}
  time: {pauli_expectations_per_step: O(M 4^D), rotations_per_step: O(M 4^D), classical_per_step: O(M 64^D), steps: T}
  space: {qubits: n, extra: O(1)}
properties: {deterministic: true, exact: false, ancilla_free: true, unitary_steps_only: true, needs_ground_state_overlap: true}
history:
  year: 2020
  people: [Mario Motta, Chong Sun, Adrian T. K. Tan, Matthew J. O'Rourke, Erika Ye, Austin J. Minnich, Fernando G. S. L. Brandao, Garnet Kin-Lic Chan]
  note: Motta et al. introduced QITE and the quantum Lanczos method in Nature Physics in 2020 (arXiv 2019). McArdle et al. gave a variational form of imaginary-time evolution in 2019.
prereqs: [hamiltonian-simulation, pauli-string-decomposition, ground-state-preparation, trotter-suzuki-product-formulas]
see_also: [variational-quantum-eigensolver, ground-state-energy-estimation, power-iteration, lanczos-algorithm, quantum-many-body-simulation, gibbs-state-preparation, linear-combination-of-unitaries, exponential-integrators]
sources:
  - paper: doi:10.1038/s41567-019-0704-4
    title: Mario Motta, Chong Sun, Adrian T. K. Tan, Matthew J. O'Rourke, Erika Ye, Austin J. Minnich, Fernando G. S. L. Brandao and Garnet Kin-Lic Chan, Determining eigenstates and thermal states on a quantum computer using quantum imaginary time evolution, Nature Physics 16, 2020, pages 205-210
    locator: the QITE update from the linear system for the Pauli coefficients on a domain, the argument that the domain size grows with the correlation length, and the quantum Lanczos method
  - paper: doi:10.1038/s41534-019-0187-2
    title: Sam McArdle, Tyson Jones, Suguru Endo, Ying Li, Simon C. Benjamin and Xiao Yuan, Variational ansatz-based quantum simulation of imaginary time evolution, npj Quantum Information 5, 2019, article 75
    locator: the variational form of imaginary-time evolution from McLachlan's principle
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.7 (simulation of quantum systems) for the product formula that QITE follows term by term
---

Quantum imaginary time evolution (QITE) is an algorithm for [ground state preparation](/ground-state-preparation/), introduced by Motta et al. in 2020. The normalized imaginary-time flow $|\psi(\tau)\rangle = e^{-\tau H}|\psi_0\rangle/\|e^{-\tau H}|\psi_0\rangle\|$ damps each eigenvector of $H$ by $e^{-\tau E}$, so it converges to the ground state at the rate $e^{-2\tau\Delta}$ for a spectral gap $\Delta$ whenever $|\psi_0\rangle$ has a nonzero overlap with the ground state. A quantum computer cannot apply the non-unitary $e^{-\tau H}$ directly. QITE splits $H = \sum_m h_m$ into local terms and replaces each small step $e^{-\Delta\tau h_m}$, after normalization, by a unitary $e^{-i\Delta\tau A}$, where the Hermitian $A$ is a sum of Pauli strings on a domain of $D$ qubits around the term, with coefficients from a least-squares problem built from measured Pauli expectation values. With the whole register as the domain each step is exact to first order; with small domains the method relies on a finite correlation length, which Motta et al. argue but do not prove.

## In plain words

Every physical system has a lowest energy state. Imagine a process that damps every part of a state by an amount that grows with its energy: the high energy parts fade fast, the low energy parts slowly, and after a while only the lowest energy part is left. This process is not one that a quantum computer can run as it is, because it shrinks the state. The method copies it in many small steps. For each step it measures a few numbers on a small group of neighbouring qubits, solves a small system of equations on a classical computer, and applies a rotation to those qubits that has nearly the same effect as the damping step. If the group of qubits is large enough the copy is faithful, but the cost grows very fast with the size of the group.

## The problem

The input is a Hamiltonian $H = \sum_{m=1}^{M} h_m$ on $n$ qubits, each $h_m$ a Hermitian term that acts on few qubits (on this page, a real multiple $c_mP_m$ of a Pauli string, as in a [Pauli string decomposition](/pauli-string-decomposition/)), an initial state $|\psi_0\rangle$, a step $\Delta\tau$, a number of steps $T$, and for each term a domain $D_m$ of qubits that contains its support. The output is a state close to the normalized $e^{-T\Delta\tau H}|\psi_0\rangle$, and so, for large $T\Delta\tau$, close to the ground state. The output is only as good as the overlap $\langle E_0|\psi_0\rangle$ allows: for zero overlap the flow never reaches the ground state. Qubit 0 is the least significant bit, as on [quantum state](/quantum-state/).

## The algorithm

For a set of Pauli strings $\sigma_I$ on the domain $D_m$, the step looks for a real vector $a$ such that $-i\sum_Ia_I\sigma_I|\psi\rangle$ is as close as possible to the direction $\delta$ in which the normalized step $e^{-\Delta\tau h_m}|\psi\rangle/\sqrt c$ moves $|\psi\rangle$.

```pseudo id=main
QITE(h_1 + ... + h_M, ψ_0, Δτ, T, D_1, ..., D_M)
L1  ψ ← ψ_0
L2  repeat T times
L3      for m ← 1 to M
L4          c ← ⟨ψ| e^(-2Δτ h_m) |ψ⟩
L5          δ ← (e^(-Δτ h_m)|ψ⟩ / √c - |ψ⟩) / Δτ
L6          for all Pauli strings σ_I, σ_J ≠ I on D_m: S_IJ ← Re ⟨ψ|σ_I σ_J|ψ⟩, b_I ← Im ⟨δ|σ_I|ψ⟩
L7          a ← the minimum-norm solution of S a = b              ▷ least squares
L8          ψ ← e^(-iΔτ Σ_I a_I σ_I) |ψ⟩                          ▷ a unitary on D_m
L9  return ψ
```

Line L6 is the normal equation of the least-squares problem $\min_a\|\delta + i\sum_Ia_I\sigma_I|\psi\rangle\|$ over real $a$. On a quantum computer the state $|\psi\rangle$ is never written down: for $h_m = c_mP_m$, $e^{-\Delta\tau h_m} = \cosh(\Delta\tau c_m)I - \sinh(\Delta\tau c_m)P_m$, so $c$, $S$ and $b$ are combinations of expectation values $\langle\psi|\sigma|\psi\rangle$ of Pauli strings $\sigma$ on $D_m$, which are measured as in the [variational quantum eigensolver](/variational-quantum-eigensolver/). Line L7 uses a pseudo-inverse because $S$ is often singular. Line L8 is compiled into a product of Pauli rotations, for example with the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/). If $H$ and $|\psi\rangle$ are real, only strings with an odd number of $Y$ factors get nonzero coefficients, which halves the system.

The code takes the domain of a term as the qubits within distance $r$ of its support on a line, with $r$ = None for the whole register. It solves line L7 in the equivalent form $a = G^{\mathsf T}(GG^{\mathsf T})^+\delta$, where column $I$ of $G$ is $-i\sigma_I|\psi\rangle$ written as a real vector, because $GG^{\mathsf T}$ has size $2^{n+1}$ while $S$ has size $4^D - 1$.

## Example

All numbers below are from the page's simulator with exact state vectors and exact expectation values, for the open transverse-field Ising chain $H = -\sum_q Z_qZ_{q+1} - \sum_q X_q$ and the start $|0\cdots0\rangle$. For two qubits $E_0 = -\sqrt5$ and $\Delta = \sqrt5 - 1 \approx 1.236$, and the start has ground state weight $0.362$; for three qubits $E_0 = -3.49396$, $\Delta = 0.890$ and the weight is $0.284$.

**The exact flow.** The infidelity $1 - |\langle E_0|\psi(\tau)\rangle|^2$:

| $\tau$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $n = 2$ | 0.638 | 0.105 | $9.7 \cdot 10^{-3}$ | $8.3 \cdot 10^{-4}$ | $7.0 \cdot 10^{-5}$ | $5.9 \cdot 10^{-6}$ | $5.0 \cdot 10^{-7}$ |
| $n = 3$ | 0.717 | 0.208 | $4.2 \cdot 10^{-2}$ | $7.4 \cdot 10^{-3}$ | $1.3 \cdot 10^{-3}$ | $2.1 \cdot 10^{-4}$ | $3.6 \cdot 10^{-5}$ |

From $\tau = 5$ to $\tau = 6$ the infidelity falls by $0.0844$ for $n = 2$, which is $e^{-2\Delta}$ to three digits.

**QITE with the whole register as domain.** For $n = 2$ and $\Delta\tau = 0.1$ the energy error $E(\psi) - E_0$ is $0.232$ at $\tau = 0.7$, $0.0169$ at $\tau = 2.1$ and $0.00816$ at $\tau = 5.6$, where it stops. The QITE state agrees with the normalized product $\prod_m e^{-\Delta\tau h_m}$ applied step by step to an infidelity of $2.4 \cdot 10^{-8}$: the remaining error is the bias of splitting $e^{-\Delta\tau H}$ into terms. That bias falls as $\Delta\tau^2$ in the energy:

| $\Delta\tau$ | 0.2 | 0.1 | 0.05 | 0.025 |
|---|---|---|---|---|
| energy bias, $n = 2$ | 0.0288 | 0.00810 | 0.00213 | 0.000546 |
| energy bias, $n = 3$ | 0.0593 | 0.0163 | 0.00423 | 0.00107 |
| energy bias, $n = 4$ | 0.0902 | 0.0245 | 0.00632 | 0.00160 |

**Domain size.** With $\Delta\tau = 0.1$ the energy error after the given time is:

| domain radius $r$ | $n = 3$, $\tau = 5.6$ | $n = 4$, $\tau = 4.8$ |
|---|---|---|
| 0 (the support of the term) | 1.11 | 1.86 |
| 1 | 0.00746 | 0.0379 |
| 2 | (whole register) | 0.0243 |
| whole register | 0.0164 | 0.0259 |

With $r = 0$ the energy first falls and then rises again: a rotation on the support of one term cannot build the correlations of the ground state. With $r \ge 1$ the error is near the splitting bias.

## Correctness

The full proofs are below. For the exact flow: if $w_0 > 0$ is the weight of $|\psi_0\rangle$ on the ground space, then $1 - F(\tau) \le ((1 - w_0)/w_0)e^{-2\tau\Delta}$, and the energy decreases with $dE/d\tau = -2\,\mathrm{Var}_\psi(H)$. For one QITE step with the whole register as the domain, the vectors $-iA|\psi\rangle$ for traceless Hermitian $A$ are exactly the vectors $v$ with $\mathrm{Re}\langle\psi|v\rangle = 0$, so the least-squares fit leaves only the part $\mathrm{Re}\langle\psi|\delta\rangle|\psi\rangle$, which is of order $\Delta\tau$. Each substep is then within $13c_m^2\Delta\tau^2$ of the normalized $e^{-\Delta\tau h_m}|\psi\rangle$, and after time $\tau$ the QITE state is within angle $21e^{2\lambda\tau}\tau\Delta\tau\sum_mc_m^2$ of the normalized product of the $e^{-\Delta\tau h_m}$, with $\lambda = \sum_m|c_m|$. This bound is crude in $\tau$; the measured agreement is far better.

Not proved: that a domain of fixed size $D$ suffices. Motta et al. argue that if the correlation length of the states along the flow is bounded, a domain of size growing with that length suffices, and the table above is consistent with that on small chains; there is no general theorem. The splitting into terms adds its own error, which goes to 0 as $\Delta\tau \to 0$ by the Lie product formula, at fixed $\tau$.

## Complexity

- **Measurements.** For each term the step needs the expectation values of the Pauli strings on $D_m$ and of their products with $P_m$: $O(4^D)$ values, so $O(M4^D)$ per step. Each value to precision $\epsilon$ costs $O(1/\epsilon^2)$ shots, and errors in $S$ and $b$ enter the update through the pseudo-inverse.
- **Classical work.** A dense linear system of size $4^D - 1$ per term, $O(64^D)$ time by a direct method, so $O(M64^D)$ per step.
- **Circuit.** The unitary of line L8 is a sum of $O(4^D)$ Pauli strings on $D$ qubits. Its depth grows with every step, since all earlier steps must be applied before the next measurement, so the total depth is of order $TM4^D$ rotations.
- **Domain size.** For a correlation length $C$ on a lattice of dimension $k$, Motta et al. estimate $D = O(C^k)$, so the cost is exponential in $C^k$ but not in $n$.
- **Steps.** To reach infidelity $\epsilon$ the exact flow needs $\tau = O(\Delta^{-1}\log(1/(w_0\epsilon)))$, so $T = \tau/\Delta\tau$ steps, plus a small enough $\Delta\tau$ for the splitting bias.

## Properties

- **Unitary steps, no ancilla.** Every operation is a rotation on the system qubits; there is no postselection and no failure probability, unlike methods that apply $e^{-\tau H}$ through a [linear combination of unitaries](/linear-combination-of-unitaries/).
- **Energy decrease.** The exact flow lowers the energy monotonically. QITE with a large enough domain does too, up to the splitting bias; with too small a domain the energy can rise, as in the example.
- **No optimizer.** Unlike the [variational quantum eigensolver](/variational-quantum-eigensolver/), the update is a fixed rule, so there are no local minima of a cost function. The price is a circuit that grows with every step.
- **A quantum power iteration.** The flow $e^{-\tau H}$ is the continuous form of [power iteration](/power-iteration/) for the matrix $e^{-H}$, and it shares its dependence on the gap and on the start.
- **Thermal states.** Applying $e^{-\beta H/2}$ to random product states and averaging gives Gibbs state expectation values, which Motta et al. use as a method of [Gibbs state preparation](/gibbs-state-preparation/) (the minimally entangled typical thermal states).

## Variants and improvements

- **Quantum Lanczos.** Motta et al. use the states along the QITE path as a Krylov basis and solve a small generalized eigenproblem, as in the [Lanczos algorithm](/lanczos-algorithm/); the overlaps come from the same measurements. This speeds up convergence of the energy.
- **Variational imaginary time.** McArdle et al. fix a parameterized circuit and move its parameters by McLachlan's variational principle, which gives a linear system for the parameter velocities. The circuit depth is fixed, at the price of a trial family.
- **Symmetric ordering.** Applying the terms forward and then backward in alternate steps reduces the splitting bias from $O(\Delta\tau)$ in the state to $O(\Delta\tau^2)$.
- **Non-unitary methods.** Block encodings of $e^{-\tau H}$ through [quantum signal processing](/quantum-signal-processing/) or [linear combination of unitaries](/linear-combination-of-unitaries/) apply the flow with an ancilla and postselection, with success probability equal to the squared norm of $e^{-\tau H}|\psi_0\rangle$.

## When to use it

Use QITE on small devices when a variational optimization is unreliable and the correlation length of the ground state is short, so that domains of a few qubits suffice, for example gapped spin chains. It is also a source of states for [ground state energy estimation](/ground-state-energy-estimation/) with phase estimation. Do not use it for critical or long-range correlated systems, where $D$ must grow with the system, or on hardware with short coherence times, since the circuit grows with every step. On a fault-tolerant computer, methods based on [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) give provable rates instead.

## Pitfalls

- **Domains that are too small.** With domains equal to the support of each term the method can fail completely, as with $r = 0$ in the example, where the energy rises after a first fall. Check convergence in $D$.
- **The splitting bias.** Even with exact steps, the product of the $e^{-\Delta\tau h_m}$ converges to a state that is not the ground state; its energy error falls as $\Delta\tau^2$. Extrapolate in $\Delta\tau$ or use symmetric ordering.
- **Zero overlap.** If the start has no weight on the ground state, for example because it lies in another symmetry sector, the flow converges to the lowest state of that sector. For the two-qubit chain, a start that is odd under the global flip $XX$ stays odd and ends at an energy more than 1 above $E_0$.
- **Noisy linear systems.** $S$ is often ill conditioned, and shot noise in $S$ and $b$ is amplified by the pseudo-inverse. A cutoff or a regularization is needed, and it biases the step.
- **Growing circuits.** Each step adds a unitary to the circuit, so the depth grows linearly in $T$. On noisy hardware this limits $\tau$ more than the gap does.

## Implementations

## History

Imaginary-time evolution is an old classical tool: projector quantum Monte Carlo and tensor-network methods, such as the time-evolving block decimation of Vidal, project onto ground states with $e^{-\tau H}$. On quantum computers it needs either postselection or a replacement by unitaries. McArdle et al. (2019) gave a variational form with a fixed circuit. Motta et al. (2019 on arXiv, 2020 in Nature Physics) introduced QITE with local unitary updates on domains, the quantum Lanczos method built on it, and a thermal state version, and ran small examples on Rigetti hardware.

## References
