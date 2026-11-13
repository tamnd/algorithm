---
tag: RT7ET6
kind: problem
slug: phase-estimation-problem
name: Phase estimation problem
aliases:
- eigenvalue estimation
area: quantum/quantum-primitives
level: core
summary: "Given a controlled unitary U and an eigenvector with eigenvalue e^(2 pi i phi), estimate phi to within epsilon. The optimal cost is Theta((1/epsilon) log(1/delta)) uses of U."
prereqs: [unitary-operator, quantum-oracle, quantum-measurement]
see_also: [quantum-phase-estimation, eigenvalue-problem, order-finding, quantum-counting, ground-state-energy-estimation, hamiltonian-simulation, hadamard-test, median-trick]
sources:
  - url: https://arxiv.org/abs/quant-ph/9511026
    title: "A. Yu. Kitaev, Quantum measurements and the Abelian Stabilizer Problem, arXiv:quant-ph/9511026, 1995"
    locator: the problem of measuring an eigenvalue of a unitary operator, and its use for the abelian stabilizer problem
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: phase estimation as the common pattern of the known quantum algorithms, and order finding as an instance
  - paper: doi:10.1103/PhysRevA.71.042313
    title: "Arvid J. Bessen, Lower bound for quantum phase estimation, Physical Review A 71(4):042313, 2005"
    locator: the lower bound of order log(1/ε) queries when the oracle gives controlled powers of U
  - url: https://arxiv.org/abs/2305.04908
    title: "Nikhil S. Mande and Ronald de Wolf, Tight bounds for quantum phase estimation and related problems, ESA 2023 and Quantum 10:2140, 2026, arXiv:2305.04908"
    locator: the lower bound Ω((1/ε) log(1/δ)) for precision ε and error probability δ, which matches the upper bound
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.2 (phase estimation) and Section 5.3.1 (order finding as phase estimation)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 4.6 (application of the Fourier transform to phase estimation)
---

The phase estimation problem asks for the eigenvalue of a unitary operator $U$ on a given eigenvector $|u\rangle$. A unitary has eigenvalues of modulus $1$, so the eigenvalue is $e^{2\pi i \varphi}$ for a phase $\varphi \in [0, 1)$, and the task is to output $\varphi$ to within $\varepsilon$ with probability at least $1 - \delta$. The operator is a circuit on $b$ qubits, given as a black box, and the cost is the number of uses of the controlled form of $U$. The optimal cost is $\Theta((1/\varepsilon) \log(1/\delta))$ uses. If the controlled powers $U^{2^j}$ are given at unit cost, $\Theta(\log(1/\varepsilon))$ queries are enough for a constant $\delta$. Order finding in [Shor's algorithm](/shor-algorithm/), [quantum counting](/quantum-counting/) and energy estimation in [Hamiltonian simulation](/hamiltonian-simulation/) are all instances. The standard method is [quantum phase estimation](/quantum-phase-estimation/).

## In plain words

A quantum operation acts on one special state by turning it through a hidden angle and changing nothing else. You cannot see the turn by looking at the state alone, because a turn of the whole state has no effect on any measurement. You can see it only when the operation is applied or not applied depending on a helper qubit, so that the two cases can interfere.

The task is to find the angle to a given number of digits, with a small chance of failure. Each use of the operation costs one unit. A small change in the angle changes the result of one use by a very small amount, so you must use the operation many times to see it. Each extra digit about doubles the number of uses.

## Definition

**Input.** An integer $b \ge 1$, oracle access to the controlled unitary $\mathrm{c}U = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U$ for a unitary $U$ on $b$ qubits, one copy of a $b$-qubit state $|u\rangle$, a precision $\varepsilon \in (0, 1/2)$ and an error bound $\delta \in (0, 1)$.

**Promise.** $U|u\rangle = e^{2\pi i \varphi} |u\rangle$ for some $\varphi \in [0, 1)$.

**Output.** A number $\tilde\varphi \in [0, 1)$ with $d_\circ(\tilde\varphi, \varphi) \le \varepsilon$, with probability at least $1 - \delta$. Here $d_\circ(a, c) = \min_{z \in \mathbb{Z}} |a - c - z|$ is the distance on the circle of length $1$, because the phases $0.001$ and $0.999$ are close.

**Cost.** The number of applications of $\mathrm{c}U$ and of its inverse, in the [quantum query model](/quantum-query-model/) with $U$ as the [quantum oracle](/quantum-oracle/). Other gates are free in this count. The state $|u\rangle$ is part of the input, and an algorithm that does not destroy it can use it again.

**Why the control.** If an algorithm may apply only $U$ itself, it cannot tell $U$ from $e^{i\alpha} U$: each use multiplies the whole state by $e^{i\alpha}$, which is a global phase with no effect on any measurement. So $\varphi$ is defined only relative to a reference, and the controlled form gives the reference: on $(|0\rangle + |1\rangle)|u\rangle/\sqrt{2}$, the gate $\mathrm{c}U$ gives $(|0\rangle + e^{2\pi i\varphi}|1\rangle)|u\rangle/\sqrt{2}$. The phase is now a relative phase of the control qubit, by [phase kickback](/phase-kickback/), and a measurement can see it.

Qubit order on these pages follows [quantum state](/quantum-state/): qubit $0$ is the least significant bit.

## Variants

- **Controlled powers.** The oracle gives $\mathrm{c}U^{2^j}$ for each $j$ at the cost of one query. This is the case of order finding, where $U^{2^j}$ is a multiplication by $a^{2^j} \bmod N$, and $a^{2^j} \bmod N$ is computed classically by repeated squaring.
- **Hamiltonian form.** $U = e^{-iH\tau}$ for a Hermitian $H$, and the task is to estimate an eigenvalue $E$ of $H$. Then $\varphi = -E\tau/(2\pi) \bmod 1$, and the cost is the total time of evolution. If $\|H\|\tau < \pi$, the phase determines $E$ without wraparound. Precision $\varepsilon$ in $E$ needs total time of order $1/\varepsilon$.
- **Exact phase.** The promise is that $\varphi = a/2^t$ for an integer $a$, and the output must be $a$ exactly, with probability $1$.
- **Superposition input.** The input is $|\psi\rangle = \sum_j c_j |u_j\rangle$ in the eigenbasis of $U$, and the output is a sample: an estimate of $\varphi_j$ with probability about $|c_j|^2$. This is *eigenvalue sampling*. [Ground-state energy estimation](/ground-state-energy-estimation/) asks for the smallest eigenvalue of a Hamiltonian, with the promise that the input state has overlap at least $\gamma$ with its eigenvector.
- **Decision form.** Decide whether $d_\circ(\varphi, a) \le \varepsilon$ or $d_\circ(\varphi, a) \ge 2\varepsilon$ for a given $a$. The lower bound below is proved for this form, so it holds for the estimation form too.

## Examples

- **A phase gate.** $U = R_\theta = \mathrm{diag}(1, e^{i\theta})$ on one qubit and $|u\rangle = |1\rangle$, so $\varphi = \theta/(2\pi)$. For $\theta = 0.6\pi$ the phase is $0.3$, and with $\varepsilon = 1/16$ both $4/16 = 0.25$ and $5/16 = 0.3125$ are correct outputs.
- **Order finding.** For $\gcd(a, N) = 1$, let $U_a |y\rangle = |ay \bmod N\rangle$ for $0 \le y < N$ (and $U_a |y\rangle = |y\rangle$ for $y \ge N$). If $r$ is the [order](/order-finding/) of $a$, the states $|u_s\rangle = r^{-1/2} \sum_{k=0}^{r-1} e^{-2\pi i sk/r} |a^k \bmod N\rangle$ satisfy $U_a |u_s\rangle = e^{2\pi i s/r} |u_s\rangle$, and $r^{-1/2} \sum_{s=0}^{r-1} |u_s\rangle = |1\rangle$. So the input $|1\rangle$ gives a sample $s/r$ with a uniform $s$, without knowledge of the eigenvectors.
- **Counting.** On the plane of the marked and unmarked states, the Grover iterate is a rotation by $2\theta$ with $\sin^2\theta = M/N$, where $M$ is the number of marked items among $N$. Its eigenvalues are $e^{\pm 2i\theta}$, so an estimate of the phase gives an estimate of $M$ (see [quantum counting](/quantum-counting/)).
- **One spin.** $U = e^{-iZ\tau}$ with $|u\rangle = |0\rangle$ has $E = 1$ and $\varphi = -\tau/(2\pi) \bmod 1$.

## Known algorithms

| algorithm | uses of $\mathrm{c}U$ | precision and error |
|---|---|---|
| [quantum phase estimation](/quantum-phase-estimation/), $t$ qubits | $2^t - 1$ ($t$ queries to controlled powers) | $d_\circ < 2^{-t}$ with probability at least $8/\pi^2$ |
| the same with $t = n + \lceil \log_2(2 + 1/(2\delta)) \rceil$ | $O(2^n/\delta)$ | $d_\circ < 2^{-n}$ with probability at least $1 - \delta$ |
| the same with $t = n + 2$, $O(\log(1/\delta))$ runs and the [median](/median-trick/) | $O(2^n \log(1/\delta))$ | $d_\circ < 2^{-n}$ with probability at least $1 - \delta$ |
| [Hadamard test](/hadamard-test/), repeated | $O(1/\varepsilon^2)$ for a constant $\delta$ | estimates $\cos 2\pi\varphi$ and $\sin 2\pi\varphi$ to within $O(\varepsilon)$ |

Kitaev's original method (1995) uses a Hadamard test on each $\mathrm{c}U^{2^j}$, repeats each test a few times, and finds the bits of $\varphi$ one at a time with classical rounding. It needs no Fourier transform. *Iterative phase estimation* uses one control qubit, measures it after each controlled power, and corrects the next measurement with a phase that depends on the earlier outcomes.

A classical computer that has $U$ as an explicit $2^b \times 2^b$ matrix and $|u\rangle$ as a vector solves the problem with one product $U|u\rangle$, in $O(4^b)$ operations: $e^{2\pi i\varphi} = \langle u | U | u \rangle$. The general [eigenvalue problem](/eigenvalue-problem/) for such a matrix takes time polynomial in $2^b$. The quantum problem is of interest only because $U$ is a circuit on $b$ qubits and $2^b$ is too large to write down.

## Bounds

| access | cost | source of the lower bound |
|---|---|---|
| uses of $\mathrm{c}U$, constant $\delta$ | $\Theta(1/\varepsilon)$ | the hybrid argument below |
| uses of $\mathrm{c}U$, error $\delta$ | $\Theta((1/\varepsilon) \log(1/\delta))$ | Mande and de Wolf (2023) |
| queries to $\mathrm{c}U^{2^j}$, constant $\delta$ | $\Theta(\log(1/\varepsilon))$ | Bessen (2005) |

The upper bounds come from quantum phase estimation and the median trick, as in the table of known algorithms.

**The lower bound $\Omega(1/\varepsilon)$.** Let $\varepsilon < 1/5$ and $\delta = 1/3$. Take any $U$ and $|u\rangle$ with phase $\varphi$, and let $U' = e^{2\pi i \cdot 3\varepsilon} U$. Then $|u\rangle$ is an eigenvector of $U'$ with phase $\varphi + 3\varepsilon \bmod 1$, and the two sets of correct answers, the arcs of radius $\varepsilon$ around $\varphi$ and around $\varphi + 3\varepsilon$, are disjoint. Also $\|\mathrm{c}U - \mathrm{c}U'\| = |1 - e^{2\pi i \cdot 3\varepsilon}| = 2\sin(3\pi\varepsilon) \le 6\pi\varepsilon$. Run an algorithm with $T$ uses on both oracles from the same start state. Replace the uses one at a time: each change moves the final state by at most $6\pi\varepsilon$ in norm, because all other gates are unitary. So the two final states $\psi$ and $\psi'$ have $\|\psi - \psi'\| \le 6\pi\varepsilon T$. The algorithm is right with probability at least $2/3$ on both, with disjoint sets of correct answers, so the two output distributions differ by at least $1/3$ in total variation distance. For unit vectors that distance is at most $\|\psi - \psi'\|$. So $6\pi\varepsilon T \ge 1/3$, that is $T \ge 1/(18\pi\varepsilon)$.

The same argument counts a query to $\mathrm{c}U^{k}$ as $k$ uses, since $\|\mathrm{c}U^k - \mathrm{c}U'^k\| \le 6\pi\varepsilon k$. So with controlled powers the sum of the powers must still be $\Omega(1/\varepsilon)$. The number of queries can be much smaller, and Bessen proved that $\Omega(\log(1/\varepsilon))$ queries are needed.

The bound $\Omega(1/\varepsilon)$ is the *Heisenberg limit* of quantum metrology. Independent repetitions of a test that uses $\mathrm{c}U$ once, such as the Hadamard test, reach only precision $1/\sqrt{T}$ after $T$ uses. Phase estimation reaches $1/T$ because the uses are applied in sequence to the same state.

## Reductions

- **Order finding to phase estimation.** With the oracle $U_a$ above, controlled powers by repeated squaring, and the input $|1\rangle$, phase estimation with $t \approx 2\log_2 N$ qubits gives an approximation of $s/r$ close enough for [continued fractions](/continued-fraction/) to recover $r$ with good probability. This is the quantum part of [Shor's algorithm](/shor-algorithm/).
- **Counting to phase estimation.** Phase estimation on the Grover iterate estimates the number of marked items.
- **Energy to phase estimation.** Estimating an eigenvalue of $H$ reduces to phase estimation of $e^{-iH\tau}$, where each use costs a [Hamiltonian simulation](/hamiltonian-simulation/) for time $\tau$.
- **Small error from constant error.** If an algorithm has error $1/4$ and leaves $|u\rangle$ intact, $O(\log(1/\delta))$ runs and the median of the estimates on the circle give error $\delta$, by the [Chernoff bound](/chernoff-bound/).
- **Bits from Hadamard tests.** The phase of $\mathrm{c}U^{2^j}$ is $2^j\varphi \bmod 1$, whose leading bit is bit $j + 1$ of $\varphi$ after the binary point. So estimates of $2^j\varphi$ to a constant precision for $j = 0, \ldots, t-1$ give $\varphi$ to precision about $2^{-t}$.

## Applications

- **Factoring and discrete logarithms.** Order finding, and the two-dimensional phase estimation of the [discrete logarithm problem](/discrete-logarithm-problem/), in [Shor's algorithm](/shor-algorithm/).
- **Counting and amplitude estimation.** [Quantum counting](/quantum-counting/), and the estimate of a success probability from the phase of a Grover-type iterate.
- **Quantum chemistry and physics.** Energies of molecules and materials by phase estimation of a time evolution, as in [ground-state energy estimation](/ground-state-energy-estimation/).
- **Linear algebra.** Quantum algorithms for linear systems use phase estimation to write the eigenvalues of a matrix into a register and then act on them.
- **Metrology.** Estimating a physical phase, such as a frequency in a clock, at the Heisenberg limit.

## References
