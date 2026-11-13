---
tag: YD9RRK
kind: problem
slug: time-dependent-hamiltonian-simulation
name: Time-dependent Hamiltonian simulation
aliases:
- time-varying Hamiltonian simulation
- time-ordered evolution simulation
area: quantum/quantum-simulation
level: advanced
summary: Simulate evolution under a Hamiltonian H(t) that changes with time, that is, implement the time-ordered exponential to error epsilon. The cost scales with the integral of the norm of H(t).
prereqs: [hamiltonian-simulation, ode-initial-value-problem, unitary-operator]
see_also: [interaction-picture-simulation, truncated-taylor-series-simulation, trotter-suzuki-product-formulas, qdrift, no-fast-forwarding-theorem, ground-state-preparation, block-encoding, commutator-scaling]
sources:
  - paper: doi:10.22331/q-2020-04-20-254
    title: "Dominic W. Berry, Andrew M. Childs, Yuan Su, Xin Wang and Nathan Wiebe, Time-dependent Hamiltonian simulation with L1-norm scaling, Quantum 4:254, 2020, arXiv:1906.07115"
    locator: the rescaled Dyson-series and continuous qDRIFT methods, whose cost scales with the integral of the norm of H(t), and their near optimality
  - paper: doi:10.1103/PhysRevA.99.042314
    title: "Maria Kieferova, Artur Scherer and Dominic W. Berry, Simulating the dynamics of time-dependent Hamiltonians with a truncated Dyson series, Physical Review A 99:042314, 2019, arXiv:1805.00582"
    locator: the truncated Dyson series with a clock register, with logarithmic dependence on the inverse precision
  - url: https://arxiv.org/abs/1805.00675
    title: "Guang Hao Low and Nathan Wiebe, Hamiltonian simulation in the interaction picture, arXiv:1805.00675, 2018"
    locator: simulation of H = A + B in the interaction picture of A, with a cost that depends on the time derivatives of the interaction-picture Hamiltonian exponentially better than earlier methods
  - paper: doi:10.1088/1751-8113/43/6/065203
    title: "Nathan Wiebe, Dominic W. Berry, Peter Hoyer and Barry C. Sanders, Higher order decompositions of ordered operator exponentials, Journal of Physics A 43:065203, 2010, arXiv:0812.0562"
    locator: Suzuki-type product formulas for time-ordered exponentials, with error bounds in terms of the time derivatives of H, and the observation that high-order scaling may fail when the derivatives are large
  - paper: doi:10.1103/PhysRevLett.106.170501
    title: "David Poulin, Angie Qarry, Rolando D. Somma and Frank Verstraete, Quantum simulation of time-dependent Hamiltonians and the convenient illusion of Hilbert space, Physical Review Letters 106:170501, 2011, arXiv:1102.1360"
    locator: the simulation of local time-dependent Hamiltonians in time polynomial in the system size, and the counting argument that most states need exponential time to reach
---

Time-dependent Hamiltonian simulation asks for a quantum circuit that implements the evolution of a quantum system whose Hamiltonian $H(t)$ changes with time, to error $\varepsilon$. The evolution operator $U(T, 0)$ is the solution of the Schrodinger equation $i\,\partial_tU(t, 0) = H(t)U(t, 0)$ with $U(0, 0) = I$. When $H(t)$ at different times do not commute, $U$ is not $e^{-i\int H}$ but a *time-ordered exponential*, given by the Dyson series. The time-independent case is [Hamiltonian simulation](/hamiltonian-simulation/); the time-dependent case covers driven systems, control pulses, adiabatic paths and the interaction picture of a time-independent $H$. The best methods have a cost that scales with $\int_0^T\|H(t)\|\,dt$, the $L^1$ norm of the Hamiltonian over time, instead of $T\max_t\|H(t)\|$, and logarithmically with $1/\varepsilon$ (Berry, Childs, Su, Wang and Wiebe 2020).

## In plain words

A quantum system changes in time according to the forces that act on it. Often those forces change too: a laser pulse switches on and off, a magnetic field rotates, or a control knob is slowly turned. The task is to reproduce on a quantum computer what the system does over a stretch of time, to a given accuracy. Because the forces at different moments can interfere with each other, the order in which they act matters, and you cannot simply add them up and apply the total. The work needed grows with the total strength of the forces over the whole stretch of time, so a force that is strong only for a short moment costs little.

## Definition

**Input.** A Hamiltonian $H(t)$ on $n$ qubits for $t \in [0, T]$, Hermitian at each time, and an error $\varepsilon > 0$. The access model is one of the following.

- *Oracle form.* A unitary $\mathrm{HAM}$ with $(\langle0|\otimes I)\,\mathrm{HAM}\,(|0\rangle\otimes I) = \sum_t|t\rangle\langle t|\otimes H(t)/\alpha$ over a grid of times $t$ in a clock register, that is, a [block encoding](/block-encoding/) of $H(t)/\alpha$ controlled by the time, with $\alpha \ge \max_t\|H(t)\|$.
- *Local form.* $H(t) = \sum_{j=1}^ma_j(t)P_j$ with Pauli strings $P_j$ and classical functions $a_j$ that can be evaluated.

**Output.** A circuit $V$ with $\|V - U(T, 0)\| \le \varepsilon$ in operator norm, where

$$U(T, 0) = \mathcal T\exp\Big(-i\int_0^TH(t)\,dt\Big) = \sum_{k=0}^\infty(-i)^k\int_{0 \le t_1 \le \cdots \le t_k \le T}H(t_k)\cdots H(t_1)\,dt_1\cdots dt_k.$$

The series is the *Dyson series*; the later times stand to the left. It converges in norm, since the $k$-th term has norm at most $(\int_0^T\|H\|)^k/k!$.

**Cost.** Uses of $\mathrm{HAM}$ in the oracle form, or gates in the local form. Each cost is stated as a function of $T$, of norms of $H$ and its time derivatives, and of $\varepsilon$.

**When the order does not matter.** If $[H(t), H(s)] = 0$ for all $t$ and $s$, the time ordering has no effect and $U(T, 0) = e^{-i\int_0^TH(t)\,dt}$, a time-independent simulation. In general the two differ, and the difference is controlled by the commutators $[H(t), H(s)]$.

## Variants

- **Piecewise-constant Hamiltonians.** $H(t) = H_j$ on intervals of lengths $\tau_j$. Then $U = \cdots e^{-iH_2\tau_2}e^{-iH_1\tau_1}$, a product of time-independent simulations. This is the model of gate sequences and of digital control.
- **Periodic driving.** $H(t + \tau) = H(t)$. By Floquet theory, $U(k\tau, 0) = U(\tau, 0)^k$, so one period suffices.
- **Slowly varying Hamiltonians.** $H(t) = \tilde H(t/T)$ for a fixed path $\tilde H(s)$ and a large $T$, the adiabatic case; see [ground state preparation](/ground-state-preparation/).
- **Interaction picture.** $H = A + B$ with a simple $A$, simulated as $e^{-iAT}$ times the evolution under $e^{iAt}Be^{-iAt}$, as in [interaction picture simulation](/interaction-picture-simulation/).
- **Open systems and non-Hermitian generators.** A time-dependent Lindbladian, as on [open quantum system simulation](/open-quantum-system-simulation/).
- **Observables only.** Estimate $\langle\psi_0|U^\dagger OU|\psi_0\rangle$ instead of implementing $U$.

## Examples

- **Commuting case.** $H(t) = f(t)Z$ on one qubit gives $U(T, 0) = e^{-iF Z}$ with $F = \int_0^Tf(t)\,dt$.
- **A rotating field.** $H(t) = \tfrac{\omega_0}2Z + \tfrac\Omega2(\cos(\omega t)X + \sin(\omega t)Y)$ is a spin in a static field along $Z$ and a field of strength $\Omega$ that rotates about $Z$ with frequency $\omega$. In the frame that rotates with the field, the Hamiltonian is constant, and

$$U(t, 0) = e^{-i\omega tZ/2}\,e^{-it[(\omega_0 - \omega)Z/2 + \Omega X/2]}.$$

At resonance, $\omega = \omega_0$, the probability of $|1\rangle$ from $|0\rangle$ is $\sin^2(\Omega t/2)$, the *Rabi oscillation*. With detuning $d = \omega_0 - \omega$, it is $\tfrac{\Omega^2}{\Omega^2 + d^2}\sin^2(\tfrac t2\sqrt{\Omega^2 + d^2})$.
- **The naive exponential fails.** For $\omega_0 = \omega = 2$, $\Omega = 0.5$ and $T = 2\pi$, the rotating terms integrate to zero, so $e^{-i\int_0^TH} = e^{-i2\pi Z}$ never flips the spin. The true evolution is a full Rabi flip, $|0\rangle \to |1\rangle$ up to a phase, since $\Omega T/2 = \pi/2$. The two operators differ by $\sqrt2$ in operator norm. The values come from the closed form above, checked against a direct numerical solution of the Schrodinger equation.
- **Interaction picture.** For $H = A + B$ with time-independent $A$ and $B$, the operator $V(t) = e^{iAt}e^{-iHt}$ solves $i\,\partial_tV = H_I(t)V$ with $H_I(t) = e^{iAt}Be^{-iAt}$. The rotating-field example is the reverse of this: the rotating frame turns a time-dependent $H$ into a constant one.

## Known algorithms

| algorithm | model | cost | source |
|---|---|---|---|
| time slicing with [product formulas](/trotter-suzuki-product-formulas/) of order $2k$ | local form, smooth $H$ | steps of order $T^{1+1/(2k)}\varepsilon^{-1/(2k)}$, with a constant that depends on $H$ and its time derivatives up to order $2k$ | Wiebe, Berry, Hoyer and Sanders (2010) |
| truncated Dyson series with a clock register | oracle form | $\tilde O(\alpha T)$ queries, logarithmic in $1/\varepsilon$; the time derivative enters only through a logarithm | Kieferova, Scherer and Berry (2019) |
| [interaction picture simulation](/interaction-picture-simulation/) | oracle access to $A$ and $B$ | dominated by $\|B\|T$ when $\|A\| \gg \|B\|$ | Low and Wiebe (2018) |
| rescaled Dyson series | oracle form | $\tilde O(\int_0^T\|H(t)\|\,dt)$ queries, logarithmic in $1/\varepsilon$ | Berry, Childs, Su, Wang and Wiebe (2020) |
| continuous [qDRIFT](/qdrift/) | local form | of order $(\int_0^T\sum_j|a_j(t)|\,dt)^2/\varepsilon$ random exponentials, as for time-independent qDRIFT | Berry, Childs, Su, Wang and Wiebe (2020) |

Time slicing with one exponential per step shows the role of the sample points. For the rotating-field example with $T = 2\pi$ and $r$ steps of length $T/r$, taking $e^{-iH(t_k)T/r}$ at the midpoint of each step gives operator-norm errors $0.106$, $0.027$, $0.0068$ and $0.0017$ for $r = 10$, $20$, $40$ and $80$, a second-order method; taking the left endpoint gives $0.625$, $0.314$, $0.157$ and $0.0785$, a first-order method. These numbers come from a classical simulation of the $2 \times 2$ products in double precision.

## Bounds

| quantity | model | bound | reason |
|---|---|---|---|
| queries, lower bound | oracle form | $\Omega(\int_0^T\|H(t)\|\,dt)$ in the worst case | a constant $H$ on a short interval has $L^1$ norm $\|H\|\tau$, and the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/) needs $\Omega(\|H\|\tau)$ |
| queries, upper bound | oracle form | $\tilde O(\int_0^T\|H(t)\|\,dt)$, logarithmic in $1/\varepsilon$ | Berry, Childs, Su, Wang and Wiebe (2020) |
| queries, lower bound in $\varepsilon$ | oracle form | the time-independent lower bound, of order $\log(1/\varepsilon)/\log\log(1/\varepsilon)$ | special case $H(t) = H$ |
| reachable states | local $H(t)$, time polynomial in $n$ | an exponentially small fraction of all states | Poulin, Qarry, Somma and Verstraete (2011) |

The $L^1$ bound is a large gain when $H(t)$ is strong only briefly: a pulse of height $\Lambda$ and width $\tau$ inside a long interval $T$ costs about $\Lambda\tau$ instead of $\Lambda T$. The costs of the slicing methods depend on the time derivatives of $H$ polynomially; those of the Dyson-series methods depend on them only logarithmically, through the number of clock points.

## Reductions

- **Time-independent simulation as a special case.** A constant $H(t) = H$ gives $U = e^{-iHT}$, so every lower bound for [Hamiltonian simulation](/hamiltonian-simulation/) holds here.
- **Interaction picture to time-dependent simulation.** The identity $e^{-iHt} = e^{-iAt}V(t)$ above reduces a time-independent simulation of $A + B$ to a simulation of $e^{-iAt}$ and of the time-dependent $H_I(t)$, whose norm is $\|B\|$.
- **Piecewise constant to time-independent.** A product of time-independent simulations, one per piece, with the errors added.
- **Time-ordered exponential to products.** If $H$ is Lipschitz with constant $L$ in operator norm, replacing $H$ on each of $r$ slices by its value at one point changes $U$ by at most $LT^2/(2r)$, since the error of each slice is at most $\int_0^{T/r}Ls\,ds$. For the rotating field, $L = \Omega\omega/2 = 0.5$ and the bound is $0.99$ at $r = 10$, above the left-endpoint error $0.625$.

## Applications

- **Quantum control.** Simulating and designing pulses that implement gates on physical qubits.
- **Adiabatic algorithms.** Adiabatic state preparation and quantum annealing are evolutions under $H(t/T)$.
- **Spectroscopy and driven systems.** Atoms and molecules in laser fields, nuclear magnetic resonance, and periodically driven lattice models.
- **Faster time-independent simulation.** Through the interaction picture, when $H$ has a large simple part $A$, as in plane-wave chemistry and lattice models.
- **Scattering.** Collisions are often described by a Hamiltonian whose coupling is switched on and off; see [quantum scattering simulation](/quantum-scattering-simulation/).

## References
