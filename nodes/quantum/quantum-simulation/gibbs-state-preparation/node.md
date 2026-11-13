---
tag: 3Y9JZF
kind: problem
slug: gibbs-state-preparation
name: Gibbs state preparation
aliases:
- thermal state preparation
- quantum Gibbs sampling
area: quantum/quantum-simulation
level: advanced
summary: Prepare the thermal state proportional to e^(-beta H) at inverse temperature beta. Efficient above a constant temperature, QMA-hard at temperatures that fall polynomially with n.
prereqs: [density-matrix, partition-function, hamiltonian-simulation]
see_also: [quantum-metropolis-sampling, quantum-imaginary-time-evolution, metropolis-hastings, ground-state-preparation, hamiltonian-learning, open-quantum-system-simulation, mixing-time, von-neumann-entropy]
sources:
  - paper: doi:10.1103/PhysRevLett.103.220502
    title: "David Poulin and Pawel Wocjan, Sampling from the thermal quantum Gibbs state and evaluating partition functions with a quantum computer, Physical Review Letters 103:220502, 2009, arXiv:0905.2199"
    locator: the Gibbs sampler by phase estimation and amplitude amplification, with the upper bound D^alpha for alpha < 1/2 given by the free energy density, and the partition function estimate
  - paper: doi:10.1038/nature09770
    title: "Kristan Temme, Tobias J. Osborne, Karl G. Vollbrecht, David Poulin and Frank Verstraete, Quantum Metropolis sampling, Nature 471:87-90, 2011, arXiv:0911.3635"
    locator: the quantum Metropolis walk on the eigenvectors of H with the Gibbs state as its fixed point
  - url: https://arxiv.org/abs/2303.18224
    title: "Chi-Fang Chen, Michael J. Kastoryano, Fernando G. S. L. Brandao and Andras Gilyen, Quantum thermal state preparation, arXiv:2303.18224, 2023"
    locator: continuous-time quantum Gibbs samplers with costs that depend provably on the temperature, the accuracy and the mixing time, and a quantum walk speedup for purified Gibbs states
  - url: https://arxiv.org/abs/2311.09207
    title: "Chi-Fang Chen, Michael J. Kastoryano and Andras Gilyen, An efficient and exact noncommutative quantum Gibbs sampler, arXiv:2311.09207, 2023"
    locator: the first efficiently implementable Lindbladian with exact detailed balance for the Gibbs state, using Hamiltonian simulation for a time proportional to the mixing time
  - url: https://arxiv.org/abs/2403.16850
    title: "Ainesh Bakshi, Allen Liu, Ankur Moitra and Ewin Tang, High-temperature Gibbs states are unentangled and efficiently preparable, arXiv:2403.16850, 2024"
    locator: separability of Gibbs states of local Hamiltonians for beta < 1/(c d), and preparation by a depth-one circuit with polynomial classical overhead for beta < 1/(c d^2), where d is the degree of the interaction graph
  - url: https://arxiv.org/abs/1409.3435
    title: "Michael J. Kastoryano and Fernando G. S. L. Brandao, Quantum Gibbs samplers: the commuting case, Communications in Mathematical Physics 344(3):915-957, 2016, arXiv:1409.3435"
    locator: the gap of the Davies generators of commuting Hamiltonians, independent of system size in one dimension at every temperature and in every dimension at high enough temperature
  - url: https://arxiv.org/abs/1609.07877
    title: "Fernando G. S. L. Brandao and Michael J. Kastoryano, Finite correlation length implies efficient preparation of quantum thermal states, Communications in Mathematical Physics 365(1):1-16, 2019, arXiv:1609.07877"
    locator: preparation by a logarithmic-depth circuit of local channels under exponential decay of correlations and a uniform Markov condition, both satisfied in one dimension
---

Gibbs state preparation asks for the *thermal state* $\rho_\beta = e^{-\beta H}/Z$ of a Hamiltonian $H$ at inverse temperature $\beta \ge 0$, where $Z = \mathrm{Tr}\,e^{-\beta H}$ is the [partition function](/partition-function/). It is the state that a system in contact with a large bath at temperature $1/\beta$ reaches, and its expectation values are the thermal averages of statistical physics. At $\beta = 0$ the state is the maximally mixed state, which is trivial to prepare; as $\beta \to \infty$ it tends to the uniform mixture over the ground space, so at low temperature the problem contains [ground state preparation](/ground-state-preparation/) and is QMA-hard for local Hamiltonians. Above a constant temperature it is easy: Gibbs states of local Hamiltonians are then separable and can be prepared in polynomial time (Bakshi, Liu, Moitra and Tang 2024). Between the two, the cost is governed by the *mixing time* of a quantum Markov chain or Lindbladian with $\rho_\beta$ as its fixed point, and it is known in only a few cases.

## In plain words

A cup of coffee left on the table ends up at room temperature, whatever state it started in. In that end state the system is not in one definite state but in a random mixture, where low-energy states are more likely than high-energy ones, and the temperature sets how strongly low energies are favoured. The task is to produce such a thermal mixture on a quantum computer, for a given system and temperature. Hot systems are easy, because the mixture is close to completely random. Very cold systems are hard, because the mixture is close to the lowest-energy state, which is hard to find in general. In between, the cost depends on how fast a simulated bath brings the system to equilibrium.

## Definition

**Input.** A Hamiltonian $H = \sum_{j=1}^mH_j$ on $n$ qubits, with local terms of norm at most $1$, or a [block encoding](/block-encoding/) of $H$; an inverse temperature $\beta \ge 0$; and an error $\varepsilon \in (0, 1)$.

**Output.** A [density matrix](/density-matrix/) $\rho$ with [trace distance](/trace-distance/) $\tfrac12\|\rho - \rho_\beta\|_1 \le \varepsilon$, where

$$\rho_\beta = \frac{e^{-\beta H}}{Z} = \sum_i\frac{e^{-\beta E_i}}Z|E_i\rangle\langle E_i|,\qquad Z = \mathrm{Tr}\,e^{-\beta H} = \sum_ie^{-\beta E_i}.$$

The output may be produced with ancilla qubits that are then discarded.

**Cost.** Gates, or uses of the block encoding or of $e^{-iH\tau}$, as a function of $n$, $\beta$ and $\varepsilon$.

**Variational characterization.** Among all states, $\rho_\beta$ is the unique minimizer of the free energy $F(\rho) = \mathrm{Tr}(\rho H) - \beta^{-1}S(\rho)$, with $S$ the [von Neumann entropy](/von-neumann-entropy/), and the minimum is $F = -\beta^{-1}\ln Z$. This is the Gibbs variational principle; the free energy difference is $F(\rho) - F(\rho_\beta) = \beta^{-1}S(\rho\|\rho_\beta) \ge 0$, a relative entropy. See the [variational method](/variational-method/).

## Variants

- **Purified Gibbs states.** Prepare $\sum_i\sqrt{e^{-\beta E_i}/Z}\,|E_i\rangle|\overline{E_i}\rangle$ on two registers, where the bar is complex conjugation, also called the *thermofield double*. Tracing out the second register gives $\rho_\beta$, by the [partial trace](/partial-trace/).
- **Thermal expectation values.** Estimate $\mathrm{Tr}(O\rho_\beta)$ for given observables $O$, which needs only samples of measurements, not a copy of the state.
- **Partition function and free energy.** Estimate $Z$ to relative error, or $\ln Z$ to additive error.
- **Classical Hamiltonians.** $H$ diagonal in the computational basis, so $\rho_\beta$ is the Boltzmann distribution on bit strings, as for the [Ising model](/ising-model/). Sampling it is the classical Gibbs sampling task of [Markov chain Monte Carlo](/metropolis-hastings/).
- **Commuting Hamiltonians.** All $H_j$ commute, as in stabilizer codes and classical models; the Davies generators then have a simple local form.
- **Geometric restrictions.** Terms on a line or a lattice of fixed dimension, or a bound $d$ on the number of terms that share a qubit with a given term.

## Examples

- **One qubit.** $H = hZ$ gives $\rho_\beta = \mathrm{diag}(e^{-\beta h}, e^{\beta h})/(2\cosh\beta h)$ and $\langle Z\rangle = -\tanh(\beta h)$. A biased coin that outputs $|0\rangle$ with probability $e^{-\beta h}/(2\cosh\beta h)$ prepares it.
- **Infinite temperature.** At $\beta = 0$, $\rho_0 = I/2^n$, prepared by uniformly random bits, or by halves of $n$ Bell pairs.
- **A transverse-field Ising chain.** On three qubits, $H = -Z_2Z_1 - Z_1Z_0 - X_2 - X_1 - X_0 - 0.3Z_2$ has $E_0 \approx -3.56025$, $E_1 \approx -2.56899$ and $E_2 \approx -1.04045$. The Gibbs weights of these three levels are $0.416$, $0.253$ and $0.118$ at $\beta = 0.5$; $0.657$, $0.244$ and $0.053$ at $\beta = 1$; and $0.873$, $0.120$ and $0.006$ at $\beta = 2$. The free energy $F = -\beta^{-1}\ln Z$ is $-5.316$, $-3.980$ and $-3.628$, so $E_0 - F$ is $1.76$, $0.42$ and $0.068$, within the bound $\beta^{-1}n\ln2$, which is $4.16$, $2.08$ and $1.04$. The values come from exact diagonalization.
- **A frustrated classical triangle.** $H = Z_0Z_1 + Z_1Z_2 + Z_0Z_2$ has $6$ strings of energy $-1$ and $2$ of energy $3$. So $Z = 6e^\beta + 2e^{-3\beta}$, and as $\beta \to \infty$ the Gibbs state tends to the uniform mixture of the $6$ ground strings, which is not a pure state.

## Known algorithms

| algorithm | model | cost or guarantee | source |
|---|---|---|---|
| exact diagonalization | classical, explicit matrix | $O(8^n)$ time | |
| phase estimation with amplitude amplification | $e^{-iH\tau}$ | at most $D^\alpha$ with $D = 2^n$ and $\alpha < 1/2$ set by the free energy density | Poulin and Wocjan (2009) |
| [quantum Metropolis sampling](/quantum-metropolis-sampling/) | phase estimation and rewinding | fixed point $\rho_\beta$ in the ideal model; no general bound on the mixing time | Temme et al. (2011) |
| minimally entangled typical thermal states with [imaginary-time evolution](/quantum-imaginary-time-evolution/) | measured local terms | heuristic; gives thermal expectation values | Motta et al. (2020) |
| Lindbladian Gibbs samplers with approximate detailed balance | block encoding, $e^{-iH\tau}$ | provable dependence on $\beta$, $\varepsilon$ and the mixing time; quantum walk speedup for purified states | Chen, Kastoryano, Brandao and Gilyen (2023) |
| Lindbladian Gibbs sampler with exact detailed balance | $e^{-iH\tau}$ | Hamiltonian simulation for a time proportional to the mixing time | Chen, Kastoryano and Gilyen (2023) |
| local channels of logarithmic depth | local $H$ | efficient under exponential decay of correlations and a uniform Markov condition, both true in one dimension | Brandao and Kastoryano (2019) |
| sampling product states | local $H$, $\beta < 1/(cd^2)$ | depth-one circuit and $\mathrm{poly}(n, 1/\varepsilon)$ classical time | Bakshi, Liu, Moitra and Tang (2024) |
| [Metropolis-Hastings](/metropolis-hastings/) and other Markov chains | classical $H$ | polynomial when the chain mixes rapidly | |

The Lindbladian methods reduce the problem to bounding a [mixing time](/mixing-time/), the quantum analogue of the classical question for Markov chains. For commuting Hamiltonians, the Davies generators have a gap independent of $n$ in one dimension at every temperature and in every dimension at high enough temperature (Kastoryano and Brandao 2016).

## Bounds

| regime | model | complexity | source |
|---|---|---|---|
| $\beta < 1/(cd^2)$, local $H$ of degree $d$ | classical sampling, then a depth-one quantum circuit | $\mathrm{poly}(n, 1/\varepsilon)$ | Bakshi, Liu, Moitra and Tang (2024) |
| $\beta < 1/(cd)$ | structure | $\rho_\beta$ is separable | Bakshi, Liu, Moitra and Tang (2024) |
| one dimension, any constant $\beta$ | quantum polynomial time | efficient | Brandao and Kastoryano (2019) |
| general $H$ | uses of $e^{-iH\tau}$ | at most $D^\alpha$, $\alpha < 1/2$ | Poulin and Wocjan (2009) |
| $\beta$ polynomial in $n$, local $H$ | quantum polynomial time | QMA-hard | the reduction from ground energy below |
| $\beta \ge \ln(3 \cdot 2^n)$, oracle $H$ | queries | $\Omega(2^{n/2})$ | the search reduction below |

The constant $c$ is an absolute constant, and $d$ is the largest number of terms that overlap one term. The separability result says that at high temperature no entanglement remains, so a Gibbs state there is a mixture of product states; this is what makes a depth-one circuit possible. For classical Hamiltonians, low-temperature sampling is already NP-hard, since it finds the minimum of an Ising energy.

## Reductions

- **Ground energy from low temperature.** By the variational characterization, $E_0 - \beta^{-1}n\ln2 \le F \le E_0$, and the energy of the Gibbs state satisfies $E_0 \le \mathrm{Tr}(\rho_\beta H) \le E_0 + \beta^{-1}n\ln2$. So with $\beta = 2n\ln2/\varepsilon$, measuring the energy of copies of $\rho_\beta$ estimates $E_0$ to within $\varepsilon$, which reduces [ground state energy estimation](/ground-state-energy-estimation/) to Gibbs state preparation at a polynomial $\beta$. This gives the QMA-hardness above.
- **Search to low temperature.** For a marked item $w$ among $N = 2^n$, $H = -|w\rangle\langle w|$ has $\rho_\beta = (e^\beta|w\rangle\langle w| + (I - |w\rangle\langle w|))/(e^\beta + N - 1)$. For $e^\beta \ge 3N$, a measurement of $\rho_\beta$ outputs $w$ with probability at least $3/4$, so preparation needs $\Omega(\sqrt N)$ queries.
- **Partition function from samples.** Writing $Z(\beta)/Z(0)$ as a product of ratios $Z(\beta_{k+1})/Z(\beta_k)$ over a schedule of temperatures, each ratio is an expectation value in $\rho_{\beta_k}$. So Gibbs sampling at all intermediate temperatures gives an estimate of $Z$, as in classical annealing.
- **Purification to state.** A purified Gibbs state gives $\rho_\beta$ by discarding a register.
- **Hamiltonian learning.** The inverse problem, recovering $H$ from copies of $\rho_\beta$, is [Hamiltonian learning](/hamiltonian-learning/).

## Applications

- **Thermal physics.** Specific heats, magnetizations and correlation functions of quantum materials at finite temperature, and phase diagrams in temperature.
- **Chemistry.** Thermal averages of molecular properties and reaction free energies.
- **Optimization and learning.** Quantum algorithms for semidefinite programs and quantum Boltzmann machines use Gibbs states of matrices built from the input as a subroutine.
- **Ground states.** At low temperature, a Gibbs sampler is a route to [ground state preparation](/ground-state-preparation/), with the bath doing the cooling.
- **Learning from thermal data.** Gibbs states are the input of [Hamiltonian learning](/hamiltonian-learning/) from equilibrium measurements.

## References
