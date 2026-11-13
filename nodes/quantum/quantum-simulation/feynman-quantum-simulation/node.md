---
tag: K1581G
kind: concept
slug: feynman-quantum-simulation
name: Feynman's quantum simulation idea
aliases:
- quantum simulation motivation
area: quantum/quantum-simulation
level: intro
summary: "Feynman's 1982 proposal: a classical computer seems to need exponential resources to simulate a quantum system, so build the simulator from quantum parts instead."
prereqs: [qubit, quantum-state]
see_also: [analog-quantum-simulation, digital-quantum-simulation, hamiltonian-simulation, universal-quantum-simulator, entanglement, bqp, gottesman-knill-theorem, quantum-many-body-simulation]
sources:
  - paper: doi:10.1007/BF02650179
    title: Richard P. Feynman, Simulating physics with computers, International Journal of Theoretical Physics 21(6/7), 1982, pages 467 to 488
    locator: the sections on simulating quantum physics with a classical computer and on quantum computers as simulators
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the opening discussion of Feynman's conjecture and its proof for local Hamiltonians
  - paper: doi:10.1103/RevModPhys.86.153
    title: I. M. Georgescu, S. Ashhab and F. Nori, Quantum simulation, Reviews of Modern Physics 86(1), 2014, pages 153 to 185
    locator: the introduction and the section on the need for quantum simulation
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.7 (simulation of quantum systems)
---

Feynman's quantum simulation idea is the observation, made by Richard Feynman in a 1982 lecture, that a classical computer seems to need resources that grow exponentially with the size of a quantum system to simulate it, and the proposal to simulate quantum systems with a computer that is itself made of quantum parts. The idea is the start of the field of quantum simulation and one of the two main reasons, with factoring, to build a quantum computer. Seth Lloyd made the idea precise in 1996: the [universal quantum simulator](/universal-quantum-simulator/) theorem shows that a quantum computer can simulate local quantum systems with a polynomial number of gates. This page is about the motivation. The task itself is [Hamiltonian simulation](/hamiltonian-simulation/), and the two ways to build a simulator are [analog](/analog-quantum-simulation/) and [digital](/digital-quantum-simulation/) quantum simulation.

## In plain words

To describe one coin, you need one number: the chance of heads. A quantum system is not like a set of coins. Its description holds one number for each possible arrangement of all its parts at the same time. Each part that you add doubles the count of arrangements. So the description of fifty small parts is too large for every computer on Earth.

Feynman said that this is not a reason to stop. Nature itself runs the quantum system without trouble. So build a machine from quantum parts that you can control, and let it copy the system that you want to study. The machine holds the large description in its own state, and you never write it down. You only measure the machine at the end, as you measure the real system in an experiment.

## The idea

**The state space grows exponentially.** The state of $n$ [qubits](/qubit/) is a unit vector in $\mathbb{C}^{2^n}$, the [tensor product](/tensor-product/) of $n$ copies of $\mathbb{C}^2$ (see [quantum state](/quantum-state/)). A classical program that stores the state as a list of amplitudes needs $2^n$ complex numbers. The time evolution of a closed system for a time $t$ is the unitary $e^{-iHt}$, where the Hamiltonian $H$ is a $2^n \times 2^n$ Hermitian matrix. A direct classical method multiplies vectors of length $2^n$ by such matrices, so its cost also grows as $2^n$ or faster.

With two 64-bit floating point numbers per amplitude, the memory for the state alone is $16 \cdot 2^n$ bytes:

| qubits $n$ | amplitudes | memory |
|---|---|---|
| 10 | 1024 | 16 KiB |
| 20 | about $10^6$ | 16 MiB |
| 30 | about $10^9$ | 16 GiB |
| 40 | about $10^{12}$ | 16 TiB |
| 50 | about $10^{15}$ | 16 PiB |

**Feynman's two claims.** First, a classical computer that simulates a quantum system in a direct way needs exponential resources. Feynman did not prove that every classical method must fail. He argued that the obvious methods fail, and he gave a reason why a local classical probabilistic machine cannot even reproduce the probabilities of quantum experiments with entangled particles: the correlations break Bell-type inequalities. Second, a computer built from quantum parts, with local interactions that we can control, should be able to simulate any quantum system with a cost that grows only in proportion to the size of the system.

**What was proved later.** Lloyd proved the second claim for Hamiltonians that are sums of local terms: product formulas such as the [Lie-Trotter product formula](/lie-trotter-product-formula/) give a circuit with a polynomial number of gates in $n$, $t$ and $1/\epsilon$. The first claim is still open in its strong form. If a classical machine could simulate every quantum circuit in polynomial time, then [BQP](/bqp/) would equal BPP, and no one knows how to prove or disprove that.

**Not every quantum system is hard.** The exponential count is for a general state. Many special cases have fast classical methods:

- A state with no [entanglement](/entanglement/) is a product of $n$ one-qubit states, so it needs only $2n$ amplitudes.
- Circuits of Clifford gates on stabilizer states can be simulated in polynomial time by the [Gottesman-Knill theorem](/gottesman-knill-theorem/).
- One-dimensional systems with little entanglement are well described by tensor network methods.
- Some systems have quantum Monte Carlo methods without a sign problem, for example many models of spins with no frustration.

Feynman's idea is about the systems outside these classes: strongly correlated electrons, chemistry with many active orbitals, and dynamics far from equilibrium.

## Examples

**A product state versus an entangled state.** The two-qubit product state $(a|0\rangle + b|1\rangle) \otimes (c|0\rangle + d|1\rangle)$ is fixed by 4 numbers $a, b, c, d$, and its 4 amplitudes are $ac, ad, bc, bd$. The Bell state $(|00\rangle + |11\rangle)/\sqrt{2}$ is not of this form. If it were, then $ac = bd = 1/\sqrt{2}$ and $ad = bc = 0$. From $ad = 0$, $a = 0$ or $d = 0$, and each choice makes $ac$ or $bd$ zero. So a general state needs all $2^n$ amplitudes, and $n$ separate descriptions of the parts are not enough.

**One step of evolution.** Take one qubit with $H = X$, the Pauli $X$ matrix (see [Pauli gates](/pauli-gates/)). Then $e^{-iXt} = \cos t \, I - i \sin t \, X$, and the state $|0\rangle$ becomes $\cos t\,|0\rangle - i \sin t\,|1\rangle$. A classical program does this with 2 amplitudes. For $n$ qubits and a Hamiltonian that couples all of them, the same step acts on $2^n$ amplitudes. A quantum simulator does the step with a circuit of gates on its own $n$ qubits; the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) give such circuits.

**The output is a measurement.** The quantum simulator does not print the $2^n$ amplitudes. It prepares the evolved state, and a measurement returns one sample. To estimate an expected value such as the energy or a magnetization to an additive error $\delta$, you repeat the run about $1/\delta^2$ times, or you use [quantum phase estimation](/quantum-phase-estimation/). So the useful questions are the ones that a few measured numbers answer.

## Where it is used

- **The goal of quantum simulation.** [Analog quantum simulation](/analog-quantum-simulation/) builds a device whose own Hamiltonian copies the target. [Digital quantum simulation](/digital-quantum-simulation/) compiles $e^{-iHt}$ into gates on a [quantum circuit](/quantum-circuit-model/). Both come from Feynman's idea.
- **Chemistry and materials.** [Quantum chemistry simulation](/quantum-chemistry-simulation/) and [quantum many-body simulation](/quantum-many-body-simulation/) are the main planned uses: energies of molecules, phases of lattice models and their dynamics.
- **Complexity theory.** The idea is behind the class [BQP](/bqp/): the problems that a quantum computer solves in polynomial time with bounded error. Simulation of local Hamiltonians is a complete problem for BQP in its decision form, so it is as hard as any polynomial-time quantum computation.
- **History.** Yuri Manin made a similar remark about the exponential size of quantum states in a 1980 book in Russian. Feynman's lecture at the 1981 MIT conference on physics and computation, printed in 1982, is the usual reference. Lloyd's 1996 paper gave the first algorithm with a proof.

## References
