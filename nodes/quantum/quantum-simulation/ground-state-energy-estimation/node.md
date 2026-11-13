---
tag: 7NPT12
kind: problem
slug: ground-state-energy-estimation
name: Ground state energy estimation
aliases:
- ground energy estimation
- local Hamiltonian problem
- guided local Hamiltonian problem
area: quantum/quantum-simulation
level: advanced
summary: "Estimate the lowest eigenvalue of a Hamiltonian to a given additive precision. QMA-hard for local Hamiltonians in general; with a guiding state of overlap gamma it costs about 1/(gamma epsilon)."
prereqs: [hamiltonian-simulation, phase-estimation-problem, eigenvalue-problem]
see_also: [ground-state-preparation, quantum-phase-estimation, variational-method, variational-quantum-eigensolver, qma, quantum-chemistry-simulation, block-encoding, lanczos-algorithm]
sources:
  - url: https://arxiv.org/abs/quant-ph/0406180
    title: "Julia Kempe, Alexei Kitaev and Oded Regev, The complexity of the local Hamiltonian problem, SIAM Journal on Computing 35(5):1070-1097, 2006, arXiv:quant-ph/0406180"
    locator: the main theorem, that the 2-local Hamiltonian problem is QMA-complete
  - book: isbn:9780821832295
    title: "A. Yu. Kitaev, A. H. Shen and M. N. Vyalyi, Classical and Quantum Computation, American Mathematical Society, 2002"
    locator: the part on the local Hamiltonian problem and the class BQNP, with Kitaev's proof that the 5-local Hamiltonian problem is complete (general locator)
  - paper: doi:10.1007/s00220-008-0710-3
    title: "Dorit Aharonov, Daniel Gottesman, Sandy Irani and Julia Kempe, The power of quantum systems on a line, Communications in Mathematical Physics 287(1):41-65, 2009"
    locator: the theorem that the local Hamiltonian problem on a line of 12-state particles is QMA-complete
  - paper: doi:10.22331/q-2020-12-14-372
    title: "Lin Lin and Yu Tong, Near-optimal ground state preparation, Quantum 4:372, 2020, arXiv:2002.12508"
    locator: the ground energy estimation algorithm with a guiding state of overlap gamma, and the matching lower bounds from unstructured search and approximate counting
  - paper: doi:10.1103/PRXQuantum.3.010318
    title: "Lin Lin and Yu Tong, Heisenberg-limited ground state energy estimation for early fault-tolerant quantum computers, PRX Quantum 3:010318, 2022"
    locator: the method with one ancilla qubit and classical post-processing of the cumulative spectral distribution, with Heisenberg-limited scaling in the precision
  - paper: doi:10.1137/22M1513721
    title: "Sevag Gharibian and Francois Le Gall, Dequantizing the quantum singular value transformation: hardness and applications to quantum chemistry and the quantum PCP conjecture, SIAM Journal on Computing 52(4):1009-1038, 2023, arXiv:2111.09079"
    locator: the guided local Hamiltonian problem, BQP-complete for inverse-polynomial precision, and the classical algorithm for constant relative precision
  - url: https://arxiv.org/abs/1712.03193
    title: "Yimin Ge, Jordi Tura and J. Ignacio Cirac, Faster ground state preparation and high-precision ground energy estimation with fewer qubits, arXiv:1712.03193, 2017"
    locator: ground energy estimation with a run time that depends on the precision exponentially better than earlier methods
  - url: https://arxiv.org/abs/1307.5143
    title: "Zeph Landau, Umesh Vazirani and Thomas Vidick, A polynomial-time algorithm for the ground state of 1D gapped local Hamiltonians, arXiv:1307.5143, 2013"
    locator: the classical polynomial-time algorithm for one-dimensional local Hamiltonians with a constant spectral gap
---

Ground state energy estimation asks for the smallest eigenvalue $E_0$ of a Hermitian operator $H$, the *Hamiltonian*, to within an additive error $\varepsilon$. On a classical computer the problem is the [eigenvalue problem](/eigenvalue-problem/) for one end of the spectrum, and it is easy when $H$ is a matrix that fits in memory. In physics and chemistry $H$ acts on $n$ qubits, so its matrix has size $2^n$, and it is given as a sum of $m$ *local* terms, each acting on at most $k$ qubits. In this form the problem is the *$k$-local Hamiltonian problem*, and it is [QMA](/qma/)-complete already for $k = 2$ (Kempe, Kitaev and Regev 2006): even a quantum computer is not expected to solve it in polynomial time in general. It becomes tractable when a *guiding state* with overlap $\gamma$ with the ground state is given: then about $1/(\gamma\varepsilon)$ uses of $H$ are enough and necessary, up to logarithmic factors. Estimating energies of molecules and materials is one of the main expected uses of a quantum computer.

## In plain words

A physical system has many possible energies, and the lowest one decides how the system behaves when it is cold: whether a molecule holds together, whether a material is a magnet. The task is to compute this lowest energy to a given number of digits. The system is described by a list of small pieces, each of which involves only a few particles, but the number of possible states grows exponentially with the number of particles, so you cannot list them. In general the problem is believed to be hard even for quantum computers. It becomes manageable if someone hands you a starting state that is partly right, that is, partly made of the lowest-energy state. A quantum computer can then read off the energy, and the cost grows as the starting state gets worse and as more digits are required.

## Definition

**Input.** An integer $n$, a $k$-local Hamiltonian $H = \sum_{j=1}^m H_j$ on $n$ qubits, where each $H_j$ is Hermitian, acts on at most $k$ qubits, is given by its $2^k \times 2^k$ matrix and has $\|H_j\| \le 1$, with $m$ polynomial in $n$, a precision $\varepsilon > 0$ and an error bound $\delta \in (0, 1)$.

**Output.** A number $\tilde E$ with $|\tilde E - E_0| \le \varepsilon$, with probability at least $1 - \delta$, where $E_0 = \min_{|\psi\rangle}\langle\psi|H|\psi\rangle$ over unit vectors.

**Decision form, the $k$-local Hamiltonian problem.** Given also numbers $a < b$ with $b - a \ge 1/p(n)$ for a polynomial $p$, decide whether $E_0 \le a$ or $E_0 \ge b$, with the promise that one of the two holds. An estimate to within $\varepsilon < (b - a)/2$ decides it, so lower bounds for the decision form hold for the estimation form.

**Guided form.** Also given is a state $|\phi\rangle$ with $|\langle\phi|\psi_0\rangle| \ge \gamma$, where $|\psi_0\rangle$ is a ground state, or the projection onto the ground space when it is degenerate. The state comes as a circuit $U_I$ with $U_I|0^n\rangle = |\phi\rangle$, or, in the classical setting, as a vector that can be sampled and queried.

**Oracle form.** $H$ is given only through a black box: a [block encoding](/block-encoding/) $U_H$ of $H/\alpha$ with $\alpha \ge \|H\|$, or the time evolution $e^{-iH\tau}$. The cost is the number of uses of $U_H$, or the total evolution time, and the number of uses of $U_I$.

The answer is a property of the spectrum only: the problem does not ask for the ground state, which is [ground state preparation](/ground-state-preparation/).

## Variants

- **Precision relative to the norm.** With $\|H\| \le m$, the precision $\varepsilon = cm$ for a small constant $c$ asks for the energy per term. Whether this version is still QMA-hard is the *quantum PCP conjecture*, which is open.
- **Geometric restrictions.** Terms on the edges of a line, a 2D lattice or a bounded-degree graph. The problem stays QMA-complete on a line of particles with 12 states each (Aharonov, Gottesman, Irani and Kempe 2009).
- **Gapped Hamiltonians.** With the promise that the gap $\Delta = E_1 - E_0$ is at least a constant, one-dimensional instances have a classical polynomial-time algorithm (Landau, Vazirani and Vidick 2013).
- **Classical Hamiltonians.** All $H_j$ diagonal in the computational basis, so that $E_0$ is the minimum of a function on bit strings. This is a constraint optimization problem.
- **Fermionic and molecular Hamiltonians.** $H$ is a molecular Hamiltonian in second quantization, mapped to qubits as on [quantum chemistry simulation](/quantum-chemistry-simulation/). The usual target precision is *chemical accuracy*, $1$ kcal/mol, about $1.6 \times 10^{-3}$ Hartree.
- **Excited states and gaps.** Estimate $E_1$, or the gap $E_1 - E_0$.

## Examples

- **One qubit.** $H = Z + X$ has eigenvalues $\pm\sqrt2$, so $E_0 = -\sqrt2 \approx -1.4142$. The basis state $|1\rangle$ is a guiding state with $|\langle 1|\psi_0\rangle|^2 = (1 + 1/\sqrt2)/2 \approx 0.854$.
- **A frustrated triangle.** $H = Z_0Z_1 + Z_1Z_2 + Z_0Z_2$ on three qubits is diagonal. Each bit string has energy $3$ if all bits agree and $-1$ otherwise, so $E_0 = -1$ with a ground space of dimension $6$. In general, for a graph with $e$ edges, $\sum_{(i,j)}Z_iZ_j$ has $E_0 = e - 2\,\mathrm{maxcut}$.
- **A transverse-field Ising chain.** On three qubits, $H = -Z_2Z_1 - Z_1Z_0 - X_2 - X_1 - X_0 - 0.3Z_2$ has $E_0 \approx -3.56025$ and $E_1 \approx -2.56899$, so the gap is about $0.991$. The product states $|{+}{+}{+}\rangle$, $|000\rangle$ and $|111\rangle$ have squared overlaps about $0.828$, $0.455$ and $0.135$ with the ground state: all three are guiding states, of very different quality. The values come from exact diagonalization.
- **The hydrogen atom.** $H = -\tfrac12\nabla^2 - 1/r$ in atomic units has $E_0 = -\tfrac12$ Hartree. This is not a qubit Hamiltonian, but it shows the problem as posed in physics; the [variational method](/variational-method/) gives upper bounds on it.

## Known algorithms

| algorithm | model | cost | guarantee |
|---|---|---|---|
| exact diagonalization | classical, explicit $2^n \times 2^n$ matrix | $O(8^n)$ time, $O(4^n)$ memory | exact up to rounding |
| [Lanczos algorithm](/lanczos-algorithm/) | classical, products $Hv$ | $O(2^n)$ memory, iterations depend on the gap | converges to $E_0$ for a start vector with nonzero overlap |
| [quantum phase estimation](/quantum-phase-estimation/) on $e^{-iH\tau}$ | guided form | total time $O(1/\varepsilon)$ per run, $O(1/\gamma^2)$ runs, or $O(1/\gamma)$ with [amplitude amplification](/amplitude-amplification/) | eigenvalue samples; the smallest one is within $\varepsilon$ of $E_0$ with high probability |
| Lin and Tong (2020) | block encoding of $H/\alpha$ | $\tilde O((\alpha/(\gamma\varepsilon))\log(1/\delta))$ uses of $U_H$, $\tilde O((1/\gamma)\log(1/\delta))$ uses of $U_I$ | precision $\varepsilon$ with probability $1 - \delta$ |
| Lin and Tong (2022) | $e^{-iH\tau}$, one ancilla qubit | Heisenberg-limited scaling $\tilde O(1/\varepsilon)$ of the maximal evolution time | from the cumulative distribution of the spectral measure of $|\phi\rangle$ |
| [variational method](/variational-method/), [VQE](/variational-quantum-eigensolver/), DMRG | any | heuristic | upper bounds on $E_0$ only, no precision guarantee |

The methods with a guarantee all need the overlap $\gamma$; the variational methods need no guiding state but give no bound on the error. A classical method with a guiding state is the topic of Gharibian and Le Gall (2023): for precision a constant fraction of $\|H\|$ and a guiding state that can be sampled and queried classically, they give a classical polynomial-time algorithm.

## Bounds

| form | model | complexity | source |
|---|---|---|---|
| decision, $k = 5$, precision $1/\mathrm{poly}(n)$ | quantum polynomial time | QMA-complete | Kitaev, in Kitaev, Shen and Vyalyi (2002) |
| decision, $k = 2$, precision $1/\mathrm{poly}(n)$ | quantum polynomial time | QMA-complete | Kempe, Kitaev and Regev (2006) |
| decision, 1D chain of 12-state particles | quantum polynomial time | QMA-complete | Aharonov, Gottesman, Irani and Kempe (2009) |
| decision, diagonal $H$, $k = 2$ | classical polynomial time | NP-complete | the MAX-CUT reduction below |
| guided, $\gamma \ge 1/\mathrm{poly}(n)$, precision $1/\mathrm{poly}(n)$ | quantum polynomial time | BQP-complete | Gharibian and Le Gall (2023) |
| oracle, constant $\gamma$ and $\delta$ | total evolution time | $\Omega(1/\varepsilon)$ | the Heisenberg limit of the [phase estimation problem](/phase-estimation-problem/) |
| oracle, constant $\varepsilon$ and $\delta$ | uses of $U_I$ | $\Omega(1/\gamma)$ | the search reduction below; Lin and Tong (2020) |

"QMA-complete" means that a polynomial-time quantum algorithm for all instances would put QMA, which contains NP, inside BQP; no such algorithm is expected. Membership in QMA holds because a ground state is a witness: the verifier measures a randomly chosen term $H_j$ on it, which accepts with a probability that is an affine function of the energy and separates $E_0 \le a$ from $E_0 \ge b$ by about $(b - a)/m$. The Lin and Tong (2020) upper bound matches both oracle lower bounds up to logarithmic factors.

## Reductions

- **Circuits to Hamiltonians.** Kitaev's circuit-to-Hamiltonian construction maps a quantum verifier circuit of $T$ gates to a local Hamiltonian whose ground energy is low exactly when an accepting witness exists. Its ground state is the *history state* $\sum_t|\psi_t\rangle|t\rangle/\sqrt{T+1}$ with a clock register, after Feynman. This gives the QMA-hardness results above.
- **MAX-CUT to diagonal 2-local Hamiltonians.** For a graph with $e$ edges, $H = \sum_{(i,j)}Z_iZ_j$ has $E_0 = e - 2\,\mathrm{maxcut}$. So deciding the energy to precision below $1$ is NP-hard even for diagonal 2-local $H$.
- **Search to guided estimation.** For an oracle that marks an unknown $w$ among $N = 2^n$ items, or no item, $H = -|w\rangle\langle w|$ has $E_0 = -1$ or $E_0 = 0$, and a block encoding of $H$ costs one oracle query. The uniform superposition is a guiding state with $\gamma = 1/\sqrt N$. The search lower bound $\Omega(\sqrt N)$ then gives $\Omega(1/\gamma)$.
- **Energy from a prepared state.** If a state close to the ground state is available, energy estimation reduces to the [phase estimation problem](/phase-estimation-problem/) in its Hamiltonian form. Conversely, Lin and Tong use an energy estimate to prepare the ground state when no bound on $E_0$ is known in advance.
- **Gibbs states.** The free energy $-\beta^{-1}\ln\mathrm{Tr}\,e^{-\beta H}$ lies within $\beta^{-1}n\ln2$ of $E_0$, so estimating it for large $\beta$ estimates $E_0$; see [Gibbs state preparation](/gibbs-state-preparation/).

## Applications

- **Quantum chemistry.** Reaction energies, binding energies and barrier heights are differences of ground energies, needed to chemical accuracy; see [quantum chemistry simulation](/quantum-chemistry-simulation/).
- **Condensed matter.** Phase diagrams of spin and electron models, from the ground energy as a function of the couplings.
- **Optimization.** For diagonal Hamiltonians, $E_0$ is the optimum of a constraint problem, as in the MAX-CUT example.
- **Complexity theory.** The local Hamiltonian problem is the basic QMA-complete problem, as satisfiability is for NP.
- **Checking variational results.** An estimate with a guarantee shows how far a variational upper bound is from $E_0$.

## References
