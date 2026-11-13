---
tag: P7SH7A
kind: model
slug: analog-quantum-simulation
name: Analog quantum simulation
aliases:
- analog quantum simulator
area: quantum/quantum-simulation
level: intro
summary: Simulate a quantum system with a controllable device whose own Hamiltonian copies the target. The cost is device size, run time, control precision and repetitions, not gates.
prereqs: [feynman-quantum-simulation]
see_also: [digital-quantum-simulation, hamiltonian-simulation, universal-quantum-simulator, quantum-many-body-simulation, lieb-robinson-bound, ising-model, quantum-error-correction, hoeffding-inequality]
sources:
  - paper: doi:10.1103/RevModPhys.86.153
    title: I. M. Georgescu, S. Ashhab and F. Nori, Quantum simulation, Reviews of Modern Physics 86(1), 2014, pages 153 to 185
    locator: the sections on analog quantum simulation, on the resources and limits of simulators, and the survey of physical platforms
  - paper: doi:10.1073/pnas.1804949115
    title: Toby S. Cubitt, Ashley Montanaro and Stephen Piddock, Universal quantum Hamiltonians, Proceedings of the National Academy of Sciences 115(38), 2018, pages 9497 to 9502 (arXiv:1701.05182)
    locator: the definition of Hamiltonian simulation in the analog sense and the universality results for two-qubit interactions
  - paper: doi:10.1007/BF02650179
    title: Richard P. Feynman, Simulating physics with computers, International Journal of Theoretical Physics 21(6/7), 1982, pages 467 to 488
    locator: the proposal of a quantum simulator built from controllable quantum parts
---

Analog quantum simulation is a model of computation in which a physical quantum device, whose Hamiltonian we can tune, is made to act like a target quantum system. The device is prepared in an initial state, evolves under its own Hamiltonian for a time, and is measured. No gates are applied. The model goes back to [Feynman's quantum simulation idea](/feynman-quantum-simulation/). It differs from [digital quantum simulation](/digital-quantum-simulation/), where the evolution $e^{-iHt}$ is compiled into gates of the [quantum circuit model](/quantum-circuit-model/). The analog model has no general method of error correction, so the errors of the device add up with the run time.

## The machine

An analog simulator has four parts.

1. **A register.** A set of $n$ physical sites: atoms in an optical lattice, trapped ions, Rydberg atoms in an array of optical tweezers, superconducting circuits, or electrons in quantum dots. Each site holds a qubit or a larger local system, such as the number of bosons on a lattice site.
2. **A tunable Hamiltonian.** The device has a family of Hamiltonians $H_{\mathrm{sim}}(\theta)$, where $\theta$ is a list of controls: laser intensities and frequencies, magnetic fields, voltages. Typical native forms are the Ising coupling $\sum J_{ij} Z_i Z_j$ with fields, the Bose-Hubbard model $-J \sum (a_i^\dagger a_j + a_j^\dagger a_i) + (U/2) \sum n_i(n_i - 1)$, and the XY or Heisenberg couplings.
3. **An encoding.** A map $\varphi$ from the states of the target to the states of the device, with
   $$H_{\mathrm{sim}}(\theta) = s \, \varphi \, H_{\mathrm{target}} \, \varphi^{-1}$$
   for a scale $s > 0$. Then a run for time $t/s$ on the device gives the target evolution for time $t$. In practice the equation holds only up to an error term $\delta H$.
4. **Preparation and measurement.** The device starts in a state that is easy to make, for example all atoms in one internal state, or the ground state of a simple $H_{\mathrm{sim}}$ that is then changed slowly. At the end it measures each site in a fixed basis, for example with a camera that images each atom. One run gives one sample of the outcome distribution.

A run of the machine is: set $\theta$, prepare, evolve for a time $t$ (the controls can also change in time), measure. The output of many runs is an estimate of expected values $\langle O \rangle$ of local observables $O$ at the time $t$, or of their correlations.

## What it counts

The model has no gate count. Its costs are:

- **Size.** The number $n$ of sites, and the dimension of each site.
- **Time.** The run time $t$ of the evolution. It is limited by the coherence time of the device.
- **Precision.** The error $\delta H = H_{\mathrm{sim}} - s\,\varphi H_{\mathrm{target}} \varphi^{-1}$ from imperfect controls and from couplings to the environment.
- **Repetitions.** The number $S$ of runs to estimate an expected value from samples.

**The error grows linearly in time.** For Hermitian $H$ and $H'$ and $t \ge 0$,
$$\| e^{-iHt} - e^{-iH't} \| \le t \, \| H - H' \|,$$
in the spectral norm (see [matrix norms](/matrix-norms/)). *Proof.* Let $F(s) = e^{-iH(t-s)} e^{-iH's}$. Then $F(0) = e^{-iHt}$, $F(t) = e^{-iH't}$, and $F'(s) = e^{-iH(t-s)} \, i(H - H') \, e^{-iH's}$. So $F(t) - F(0) = \int_0^t F'(s)\,ds$, and since the two exponentials are unitary, $\|F'(s)\| = \|H - H'\|$. The bound follows. $\square$

So a fixed relative miscalibration $\|\delta H\| = \eta \|H\|$ gives an error up to $\eta \|H\| t$ in the final state, and the useful run time is about $1/(\eta\|H\|)$. The bound is on the whole state. Local observables are often more robust: when the target and the error are both local, a [Lieb-Robinson bound](/lieb-robinson-bound/) limits how fast an error near one site can affect a far site.

**Hand example.** One qubit with $H = (\omega/2) Z$ and a frequency error $\delta$, so $H' = ((\omega + \delta)/2) Z$ and $\|H - H'\| = \delta/2$. The two evolutions are diagonal, and
$$\| e^{-iHt} - e^{-iH't} \| = |1 - e^{-i\delta t/2}| = 2\,|\sin(\delta t / 4)|.$$
For $\delta = 0.01$ and $t = 100$ this is $2 \sin(0.25) = 0.4948$, and the bound gives $t\,\delta/2 = 0.5$. The bound is almost tight here because the error is a constant shift of the frequency.

**Repetitions.** Each run gives one sample of an observable $O$ with values in $[-1, 1]$. By the [Hoeffding inequality](/hoeffding-inequality/), $S \ge 2 \ln(2/\beta) / \delta^2$ runs give an estimate within $\delta$ of $\langle O \rangle$ with probability at least $1 - \beta$. For $\delta = 0.01$ and $\beta = 0.05$ this is $S = 73\,778$ runs.

## Relation to other models

- **Digital quantum simulation.** A [digital simulator](/digital-quantum-simulation/) is a [quantum circuit](/quantum-circuit-model/). It can simulate any local Hamiltonian, with a gate count bound from product formulas such as the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) (the [universal quantum simulator](/universal-quantum-simulator/) theorem). It can use [quantum error correction](/quantum-error-correction/), so the error can be made small at a polynomial overhead. An analog simulator is fixed to its native Hamiltonians and cannot correct errors in general, but it has no Trotter error and can be much larger than present digital devices.
- **The circuit model can simulate an analog device.** If $H_{\mathrm{sim}}$ is a sum of local terms, then a quantum circuit simulates the analog run with polynomial overhead. So the analog model with local Hamiltonians and polynomial run time computes no more than [BQP](/bqp/).
- **Universal Hamiltonians.** Cubitt, Montanaro and Piddock (2018) define a strong analog notion of simulation: one Hamiltonian simulates another when its low-energy part reproduces the spectrum and the eigenstates of the target, up to an encoding, to any chosen precision. They show that some simple families of two-qubit interactions on a two-dimensional lattice, for example the Heisenberg interaction with chosen coupling strengths, can simulate every local Hamiltonian in this sense. The overhead is in the number of sites and in the energy scale of the couplings.
- **Classical models.** A classical simulation of the same target needs exponential memory in general (see [Feynman's quantum simulation idea](/feynman-quantum-simulation/)). For special targets, such as a classical [Ising model](/ising-model/) in thermal equilibrium, classical Markov chain methods are often enough.

## Known results in the model

- **Platforms.** The survey of Georgescu, Ashhab and Nori (2014) lists analog simulators made of neutral atoms, trapped ions, polar molecules, electrons in semiconductors, superconducting circuits, nuclear spins and photons. Ultracold atoms in optical lattices realize Bose-Hubbard and Fermi-Hubbard models. Trapped ions realize Ising and XY spin models with couplings that fall off as a power of the distance.
- **Error bound.** The bound $t\|\delta H\|$ above holds in every analog simulator. With no error correction, the reachable time is limited by the precision of the controls and by decoherence.
- **Universality.** By the result of Cubitt, Montanaro and Piddock, a device with the right family of two-qubit interactions is universal for analog simulation of local Hamiltonians, with a polynomial overhead in size and a large overhead in the energy scale.
- **Verification.** For a large device in a regime that classical methods cannot reach, no classical check of the output exists in general. Common checks compare with exact results in small or solvable cases, run the evolution forward and backward, or compare two different devices.

The access model of the task, the error norm and the cost measures of a gate-based simulator are on the [Hamiltonian simulation](/hamiltonian-simulation/) page.

## References
