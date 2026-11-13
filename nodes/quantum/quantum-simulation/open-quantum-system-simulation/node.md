---
tag: 12TXF0
kind: problem
slug: open-quantum-system-simulation
name: Open quantum system simulation
aliases:
- Lindblad dynamics simulation
- dissipative dynamics simulation
area: quantum/quantum-simulation
level: research
summary: "Given a Hamiltonian H, jump operators L_k and a time t, implement the channel e^(tL) of the Lindblad equation to error epsilon, for a system that loses energy or coherence to its environment."
prereqs: [quantum-channel, density-matrix, hamiltonian-simulation]
see_also: [kraus-operators, ancilla-qubits, partial-trace, markov-chain, ode-initial-value-problem, stiff-ode-problem, gibbs-state-preparation, lieb-robinson-bound]
sources:
  - paper: doi:10.1007/BF01608499
    title: Göran Lindblad, On the generators of quantum dynamical semigroups, Communications in Mathematical Physics 48(2), 1976, pages 119 to 130
    locator: the main theorem, the form of the generator of a norm-continuous semigroup of completely positive maps
  - paper: doi:10.1063/1.522979
    title: Vittorio Gorini, Andrzej Kossakowski and E. C. George Sudarshan, Completely positive dynamical semigroups of N-level systems, Journal of Mathematical Physics 17(5), 1976, pages 821 to 825
    locator: the same form of the generator for a finite-dimensional system
  - paper: doi:10.1103/PhysRevLett.107.120501
    title: Martin Kliesch, Thomas Barthel, Christian Gogolin, Michael Kastoryano and Jens Eisert, Dissipative quantum Church-Turing theorem, Physical Review Letters 107(12), 2011, article 120501 (erratum in 109, 119904)
    locator: the efficient simulation of local Lindblad dynamics by quantum circuits with a product formula
  - paper: doi:10.4230/LIPIcs.ICALP.2017.17
    title: Richard Cleve and Chunhao Wang, Efficient quantum algorithms for simulating Lindblad evolution, ICALP 2017, LIPIcs 80, article 17
    locator: the algorithm with cost O(t polylog(t/ε)) for Lindbladians with sparse or local jump operators
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 8 (quantum operations, amplitude damping and phase damping, and the Lindblad form)
---

*Open quantum system simulation* is the problem of computing the evolution of a quantum system that exchanges energy or information with an environment. Under the usual Markov approximation, the [density matrix](/density-matrix/) $\rho$ of the system follows the Lindblad equation
$$\frac{d\rho}{dt} = \mathcal L(\rho) = -i[H, \rho] + \sum_k \Big(L_k\rho L_k^\dagger - \frac12\{L_k^\dagger L_k, \rho\}\Big),$$
with a Hermitian Hamiltonian $H$ and *jump operators* $L_k$. The map $e^{t\mathcal L}$ is a [quantum channel](/quantum-channel/), but not a unitary one: it can lower the purity and send every state to one fixed state. So a simulation on a quantum computer cannot apply a unitary to the system qubits alone, and needs [ancilla qubits](/ancilla-qubits/) that are reset or thrown away. Lindblad (1976) and Gorini, Kossakowski and Sudarshan (1976) proved that this form is the general generator of a Markov evolution by quantum channels. With no jump operators, the problem is [Hamiltonian simulation](/hamiltonian-simulation/).

## In plain words

A closed quantum system keeps all its information, and its evolution can always be undone. A real system leaks. An excited atom drops to its ground state and sends out a photon, and a qubit loses its phase to stray fields. The Lindblad equation adds this leak to the Schrödinger equation: each jump operator is one way the environment can act. To simulate it, the computer adds extra qubits that play the environment, lets them interact with the system, and then forgets them. The task is to do this to a given accuracy with few gates.

## Definition

**Input.**

- A system of $n$ qubits, a Hamiltonian $H$ and jump operators $L_1, \ldots, L_m$, given as local terms, as Pauli lists or by block encodings.
- A time $t > 0$ and an error $\epsilon > 0$.

**Output.** A quantum circuit on the $n$ system qubits and some ancilla qubits that start in $|0\rangle$, whose action on the system after the ancillas are discarded is a channel $\mathcal E$ with
$$\big\|\mathcal E - e^{t\mathcal L}\big\|_\diamond \le \epsilon,$$
where $\|\cdot\|_\diamond$ is the diamond norm. Then for every input, even one entangled with a reference system, the outputs of $\mathcal E$ and $e^{t\mathcal L}$ have trace distance at most $\epsilon$. A weaker form asks only for $\mathrm{Tr}(O\, e^{t\mathcal L}(\rho_0)) \pm \epsilon\|O\|$ for a given $\rho_0$ and observable $O$.

**The matrix form.** Stack the rows of $\rho$ into a vector, so that $\mathrm{vec}(A\rho B) = (A \otimes B^{T})\,\mathrm{vec}(\rho)$. Then $\mathcal L$ is the $4^n \times 4^n$ matrix
$$\hat{\mathcal L} = -i\big(H\otimes I - I\otimes H^{T}\big) + \sum_k\Big(L_k\otimes \bar L_k - \frac12 L_k^\dagger L_k\otimes I - \frac12 I\otimes (L_k^\dagger L_k)^{T}\Big),$$
and $\mathrm{vec}(\rho(t)) = e^{t\hat{\mathcal L}}\,\mathrm{vec}(\rho_0)$. Classically, the problem is a linear [ODE initial value problem](/ode-initial-value-problem/) of dimension $4^n$, often a [stiff ODE problem](/stiff-ode-problem/) when the rates differ widely.

## Variants

- **Local Lindbladians.** $H$ and each $L_k$ act on $O(1)$ neighbouring qubits of a lattice. This is the case of most noise models and of dissipative many-body physics.
- **Time-dependent and non-Markovian dynamics.** Rates that change in time, or an environment with memory, fall outside the Lindblad form with fixed operators.
- **Steady states.** Find $\rho_\infty$ with $\mathcal L(\rho_\infty) = 0$, the long-time limit. When the jump operators drive a system to its thermal state, this is a route to Gibbs states.
- **Classical rates.** With $H = 0$ and jumps $L_{ij} = \sqrt{r_{ij}}\,|i\rangle\langle j|$, the diagonal of $\rho$ follows the master equation of a continuous-time [Markov chain](/markov-chain/), $\dot p_i = \sum_j (r_{ij}p_j - r_{ji}p_i)$.

## Examples

All examples are checked against the matrix form, with $e^{t\hat{\mathcal L}}$ computed directly. The decay operator is $\sigma^- = |0\rangle\langle1|$, which sends $|1\rangle$ to $|0\rangle$.

- **Amplitude damping.** $H = \frac\omega2 Z$ and $L = \sqrt\gamma\,\sigma^-$. The excited population decays and the coherence turns and decays at half the rate:
$$\rho_{11}(t) = e^{-\gamma t}\rho_{11}(0), \qquad \rho_{01}(t) = e^{-i\omega t - \gamma t/2}\rho_{01}(0).$$
  With $\gamma = 0.8$ and $\omega = 1.3$ the closed form agrees at $t = 0, 0.5, 2, 5$ to $10^{-10}$.
- **Dephasing.** $H = 0$ and $L = \sqrt g\,Z$. The populations stay, and $\rho_{01}(t) = e^{-2gt}\rho_{01}(0)$, since $Z\rho Z - \rho$ is $-2\rho_{01}$ off the diagonal.
- **Purity is not monotone.** Under damping with $\gamma = 1$, the state $|{+}\rangle$ has purity
$$\mathrm{Tr}\,\rho(t)^2 = 1 - \tfrac12 e^{-t} + \tfrac12 e^{-2t}.$$
  It falls to $\frac78$ at $t = \ln 2$ and then rises back to 1, as the state approaches the pure state $|0\rangle$. A unitary keeps the purity fixed, so no unitary on the qubit alone gives this map.
- **Complete positivity.** Two qubits with $H = \frac12(XX + YY)$, damping with $\gamma = 0.5$ on qubit 0 and dephasing with $g = 0.2$ on qubit 1. At $t = 0.4$ and $t = 1.5$, the $16\times16$ Choi matrix of $e^{t\mathcal L}$ has no negative eigenvalue (to $10^{-10}$), and its partial trace over the output is the identity. So the map is completely positive and preserves the trace, as the Lindblad theorem says.
- **One ancilla is enough for damping.** Let $p = 1 - e^{-\gamma t}$, $c = \sqrt{1 - p}$ and $s = \sqrt p$. The two-qubit unitary that maps $|0\rangle_a|1\rangle \mapsto c\,|0\rangle_a|1\rangle + s\,|1\rangle_a|0\rangle$ and fixes $|0\rangle_a|0\rangle$ moves the excitation to the ancilla $a$ with amplitude $s$. After the [partial trace](/partial-trace/) over the ancilla, the system has undergone exactly the damping channel at time $t$, with [Kraus operators](/kraus-operators/) $|0\rangle\langle0| + c\,|1\rangle\langle1|$ and $s\,|0\rangle\langle1|$. With $\gamma = 0.9$ and $t = 0.8$ the dilation and the matrix form agree to $10^{-10}$.

## Known algorithms

The algorithms have no pages of their own here. They are described by their cost.

| method | cost | note |
|---|---|---|
| matrix exponential of $\hat{\mathcal L}$, classical | $O(4^{3n})$ time, $O(16^n)$ memory | exact; only very small systems |
| quantum trajectories, classical | $2^n$ amplitudes per sample | random pure-state paths whose average is $\rho(t)$ |
| product formula with one dilation per local term | polynomial in $n$, $t$ and $1/\epsilon$ | Kliesch, Barthel, Gogolin, Kastoryano and Eisert (2011) |
| Cleve and Wang (2017) | $O(t\,\mathrm{polylog}(t/\epsilon))$ | linear combination of the Kraus operators of a short step, with amplitude amplification |
| repeated interactions with fresh ancillas | $O(t^2/\epsilon)$ steps for a first-order scheme with bounded rates | the damping example above, repeated |

## Bounds

- **At least Hamiltonian simulation.** With $m = 0$ the problem is Hamiltonian simulation, so the cost is $\Omega(t)$ in general by the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/).
- **Ancillas are needed.** A channel that changes the purity is not a unitary on the system. By the Stinespring theorem, every channel on $n$ qubits is a unitary on the system and an environment of at most $2n$ qubits, followed by a partial trace. A simulation that runs for long times must reset or replace its ancillas, since otherwise they fill up with entropy.
- **Classical cost.** The matrix form has dimension $4^n$, and trajectories need $2^n$ amplitudes, so classical simulation is exponential in $n$ in general.
- **Locality.** For local Lindbladians, a version of the [Lieb-Robinson bound](/lieb-robinson-bound/) also holds, so effects spread at a finite speed.

## Reductions

- **To Hamiltonian simulation on a larger system.** A dilation turns each short step $e^{\delta\mathcal L}$ into a unitary on the system and ancillas, which is then a [Hamiltonian simulation](/hamiltonian-simulation/) or a circuit.
- **To a linear ODE.** The matrix form reduces the problem to $\dot v = \hat{\mathcal L}v$, an [ODE initial value problem](/ode-initial-value-problem/), solved classically by exponential integrators or by [Runge-Kutta methods](/runge-kutta-methods/).
- **Classical Markov chains as a special case.** Classical rate equations embed as Lindbladians with jumps $|i\rangle\langle j|$, so a simulator for Lindblad dynamics also simulates continuous-time Markov chains.

## Applications

- **Noise in quantum hardware.** Amplitude damping (the $T_1$ time) and dephasing (the $T_2$ time) are the standard models of qubit noise, used to predict the error of circuits and to design [quantum error correction](/quantum-error-correction/).
- **Quantum optics.** Atoms in cavities that lose photons, lasers and photon counting.
- **Chemistry and biology with an environment.** Energy transfer in light-harvesting complexes and electron transfer in solution.
- **Dissipative state preparation.** Jump operators chosen so that the steady state is a desired state, such as an entangled or a thermal state.
- **Driven many-body systems.** A [quantum many-body simulation](/quantum-many-body-simulation/) with gain and loss, for example atoms in a lattice that lose particles.

## References
