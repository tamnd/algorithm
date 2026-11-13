---
tag: 6JAGW4
kind: algorithm
slug: quantum-phase-estimation
name: Quantum phase estimation
aliases:
- QPE
area: quantum/quantum-primitives
level: core
summary: "Estimates the phase phi of an eigenvalue e^(2 pi i phi) of U with t qubits, 2^t - 1 uses of controlled U and an inverse QFT. The result is within 2^-t of phi with probability at least 8/pi^2."
solves: [phase-estimation-problem]
model: quantum-query-model
complexity:
  vars: {t: the number of qubits of the phase register, b: the number of qubits that U acts on}
  queries: {worst: 2^t - 1}
  gates: {worst: Θ(t^2)}
  qubits: {worst: t + b}
  time: {worst: O(2^t + t^2)}
properties: {exact: false, randomized: true, recursive: false}
history:
  year: 1995
  people: [Alexei Kitaev, Richard Cleve, Artur Ekert, Chiara Macchiavello, Michele Mosca]
  note: Kitaev gave the first phase estimation method in 1995. Cleve, Ekert, Macchiavello and Mosca gave the form with controlled powers and the inverse QFT in 1998.
prereqs: [phase-estimation-problem, quantum-fourier-transform, phase-kickback, hadamard-gate, quantum-measurement]
see_also: [order-finding, shor-algorithm, quantum-counting, ground-state-energy-estimation, hamiltonian-simulation, hadamard-test, median-trick, fourier-sampling]
sources:
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the circuit with the controlled powers U^(2^j) and the inverse Fourier transform, and known algorithms as instances of it
  - url: https://arxiv.org/abs/quant-ph/9511026
    title: "A. Yu. Kitaev, Quantum measurements and the Abelian Stabilizer Problem, arXiv:quant-ph/9511026, 1995"
    locator: the first procedure for measuring an eigenvalue of a unitary operator
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.2 (the procedure, the analysis of the error, and the number of qubits for n bits with probability 1 - ε)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 4.6 (phase estimation with the quantum Fourier transform)
  - paper: doi:10.1103/PhysRevLett.76.3228
    title: "Robert B. Griffiths and Chi-Sheng Niu, Semiclassical Fourier transform for quantum computation, Physical Review Letters 76(17):3228-3231, 1996"
    locator: the measured Fourier transform with classical control, which gives phase estimation with one control qubit
  - url: https://arxiv.org/abs/2305.04908
    title: "Nikhil S. Mande and Ronald de Wolf, Tight bounds for quantum phase estimation and related problems, ESA 2023 and Quantum 10:2140, 2026, arXiv:2305.04908"
    locator: the lower bound Ω((1/ε) log(1/δ)) that the median of independent runs matches
---

Quantum phase estimation (QPE) solves the [phase estimation problem](/phase-estimation-problem/): given the controlled form of a unitary $U$ and an eigenvector $|u\rangle$ with $U|u\rangle = e^{2\pi i\varphi}|u\rangle$, it outputs an estimate $m/2^t$ of $\varphi \in [0, 1)$. It uses a register of $t$ qubits, the controlled powers $U^{2^j}$ for $j = 0, \ldots, t-1$, which are $2^t - 1$ uses of controlled $U$ in all, and an inverse [quantum Fourier transform](/quantum-fourier-transform/) on the $t$ qubits. If $2^t\varphi$ is an integer, the output is exact. Otherwise the nearest $t$-bit value comes out with probability at least $4/\pi^2 \approx 0.405$, and one of the two nearest values with probability at least $8/\pi^2 \approx 0.811$. With $t = n + \lceil \log_2(2 + 1/(2\delta)) \rceil$ the estimate is within $2^{-n}$ of $\varphi$ with probability at least $1 - \delta$. QPE is the quantum step of [order finding](/order-finding/) in [Shor's algorithm](/shor-algorithm/), of [quantum counting](/quantum-counting/) and of energy estimation for a Hamiltonian.

## In plain words

A quantum operation turns one special state through a hidden angle. Phase estimation reads that angle. It uses a row of helper qubits. The first helper controls the operation once, the next controls it twice, the next four times, and so on. Each helper then spins by the angle, and each one spins twice as fast as the one before it.

This pattern of spins is exactly what the quantum Fourier transform makes from a number. So the transform run backward turns the spinning helpers into the binary digits of the angle, and a measurement reads them. If the angle has more digits than there are helpers, the result is the nearest value most of the time, and a few extra helpers make a wrong result rare.

## The problem

The input is a number $t \ge 1$ of phase qubits, an oracle that applies the controlled power $\mathrm{c}U^{2^j}$ for each $j < t$, and a $b$-qubit state $|u\rangle$ with $U|u\rangle = e^{2\pi i\varphi}|u\rangle$. The output is an integer $m$ with $0 \le m < T$, where $T = 2^t$, and the estimate $\tilde\varphi = m/T$. Distances between phases are taken on the circle: $d_\circ(a, c) = \min_{z \in \mathbb{Z}} |a - c - z|$.

Register A is qubits $0$ to $t - 1$ and register B is qubits $t$ to $t + b - 1$. We use the qubit order of [quantum state](/quantum-state/): qubit $j$ of A is bit $j$ of $m$, and qubit $0$ is the least significant bit. Write $e(x) = e^{2\pi i x}$.

## The algorithm

```pseudo id=main
PHASE-ESTIMATION(t, CU, |u⟩)             ▷ CU(j) is controlled U^(2^j)
L1  prepare |0...0⟩ on register A (qubits 0 .. t-1) and |u⟩ on register B
L2  apply H to each qubit of A
L3  for j ← 0 to t-1: apply CU(j) with control qubit j of A and target B
L4  apply the inverse QFT to register A
L5  measure register A and let m be the outcome
L6  return m / 2^t
```

After line L2, register A is in $T^{-1/2} \sum_x |x\rangle$. On $|x\rangle|u\rangle$, the gates of line L3 apply $U^{2^j}$ exactly when bit $x_j$ is $1$, so they apply $U^x$ in all, and $U^x|u\rangle = e(x\varphi)|u\rangle$. The phase moves to register A by [phase kickback](/phase-kickback/), and register B stays in $|u\rangle$. Register A is now

$$\frac{1}{\sqrt{T}} \sum_{x=0}^{T-1} e(x\varphi) |x\rangle = \bigotimes_{j=t-1}^{0} \frac{|0\rangle + e(2^j\varphi)|1\rangle}{\sqrt{2}}.$$

If $\varphi = a/T$, this is the QFT of $|a\rangle$, so line L4 gives $|a\rangle$ exactly. In general, line L4 gives the amplitude

$$\alpha_m = \frac{1}{T} \sum_{x=0}^{T-1} e\big(x(\varphi - m/T)\big), \qquad |\alpha_m|^2 = \frac{\sin^2(\pi T \Delta)}{T^2 \sin^2(\pi \Delta)}, \quad \Delta = \varphi - \frac{m}{T},$$

with $|\alpha_m|^2 = 1$ when $\Delta$ is an integer. This is the Fejér kernel. It has a peak of width about $1/T$ at the values $m/T$ next to $\varphi$, and its tail falls as $1/(T\Delta)^2$.

The inverse QFT on $t$ qubits is the QFT circuit run backward: $\lfloor t/2 \rfloor$ swaps, then for $q = 0, \ldots, t-1$ the rotations $\mathrm{CR}_{q-p+1}^\dagger$ from each qubit $p < q$ and $H$ on qubit $q$.

## Example

**An exact phase.** Take $t = 3$ and $\varphi = 5/8$. After line L3, qubit $0$ of A holds the phase $5/8$, qubit $1$ holds $10/8 \bmod 1 = 1/4$, and qubit $2$ holds $20/8 \bmod 1 = 1/2$. This is the state $F_8|5\rangle$ of the example on the [QFT](/quantum-fourier-transform/) page, so line L4 gives $|5\rangle = |101\rangle$, and line L6 returns $5/8$ with probability $1$.

**A phase that needs more bits.** Take the phase gate $U = \mathrm{diag}(1, e(0.3))$ with $|u\rangle = |1\rangle$, so $\varphi = 0.3$ and $b = 1$. With $t = 4$, $T\varphi = 4.8$, and the simulator in the implementation gives this distribution of $m$:

| $m$ | $3$ | $4$ | $5$ | $6$ | $7$ | all others |
|---|---|---|---|---|---|---|
| $m/16$ | $0.1875$ | $0.25$ | $0.3125$ | $0.375$ | $0.4375$ | |
| probability | $0.0113$ | $0.0551$ | $0.8756$ | $0.0248$ | $0.0077$ | $0.0255$ |

The nearest value $5/16$ has probability $0.8756$, and the two nearest values $4/16$ and $5/16$ together have $0.9307$. With $t = 3$ instead, $T\varphi = 2.4$, and $m = 2$ has probability $0.5775$ and $m = 3$ has $0.2593$.

## Correctness

The proof below derives $|\alpha_m|^2$ and proves three bounds on it. The nearest value has probability at least $4/\pi^2$, because $|\sin(\pi T\Delta)| \ge 2T|\Delta|$ and $|\sin(\pi\Delta)| \le \pi|\Delta|$ when $T|\Delta| \le 1/2$. The two nearest values have probability at least $8/\pi^2$, from the product formula for the cosine. The tail beyond $e$ steps from $\lfloor T\varphi \rfloor$ has probability at most $1/(2(e-1))$, which gives the rule for $t$: with $e = 2^{t-n} - 1$, the failure probability is at most $1/(2(2^{t-n} - 2))$, and this is at most $\delta$ when $2^{t-n} \ge 2 + 1/(2\delta)$.

## Complexity

The exact costs, for use by other algorithms:

- **Uses of $U$.** Line L3 makes $t$ queries, one to each $\mathrm{c}U^{2^j}$. If each power is built from controlled $U$, this is $\sum_{j<t} 2^j = 2^t - 1$ uses. If $U^{2^j}$ is as cheap as $U$, as for modular multiplication, it is $t$ queries.
- **Other gates.** $t$ Hadamard gates in line L2, and the inverse QFT on $t$ qubits: $t$ Hadamard gates, $t(t-1)/2$ controlled phase gates and $\lfloor t/2 \rfloor$ swaps. So $2t + t(t-1)/2 + \lfloor t/2 \rfloor$ gates besides the oracle, which is $16$ for $t = 4$. The approximate QFT with rotations up to $\mathrm{CR}_k$, $k \le \log_2(t/\varepsilon) + 3$, cuts this to $O(t \log(t/\varepsilon))$ at an extra error at most $\varepsilon$.
- **Qubits.** $t + b$, and the oracle may need its own ancillas.
- **Precision and success.** For each $t$:
  - if $T\varphi$ is an integer, $m = T\varphi$ with probability $1$;
  - $m = \mathrm{round}(T\varphi) \bmod T$ with probability at least $4/\pi^2 \approx 0.405$;
  - $d_\circ(m/T, \varphi) < 1/T$ with probability at least $8/\pi^2 \approx 0.811$;
  - $d_\circ(m/T, \varphi) < 2^{-n}$ with probability at least $1 - \delta$ if $t = n + \lceil \log_2(2 + 1/(2\delta)) \rceil$.
- **Low error.** Run QPE $k$ times with $t = n + 2$, so that each run is within $2^{-n}$ with probability at least $3/4$, and take the median on the circle. The median is wrong only if at least half of the runs are wrong, so by the [Chernoff bound](/chernoff-bound/) in the form of Hoeffding the error is at most $e^{-k/8}$, so $k = O(\log(1/\delta))$ runs and $O(2^n \log(1/\delta))$ uses of $U$ give error $\delta$. One run with the extra qubits instead costs $2^t > 2^n/(2\delta)$ uses. Register B stays in $|u\rangle$, so one copy of $|u\rangle$ serves all runs. The cost $O((1/\varepsilon) \log(1/\delta))$ with $\varepsilon = 2^{-n}$ is optimal, by the bound of Mande and de Wolf on the [problem](/phase-estimation-problem/) page.

The extra qubits $t - n$ that the rule asks for, and the smallest probability of success within $2^{-n}$ over $2000$ phases on a grid, for $n = 3$:

| $\delta$ | $0.5$ | $0.25$ | $0.1$ | $0.05$ | $0.01$ | $0.001$ |
|---|---|---|---|---|---|---|
| $t - n$ | 2 | 2 | 3 | 4 | 6 | 9 |

| $t - n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| rule's bound $1 - 1/(2(2^{t-n} - 2))$ | none | 0.75 | 0.9167 | 0.9643 | 0.9833 |
| smallest success on the grid | 0.9059 | 0.9522 | 0.976 | 0.988 | 0.994 |

The bound is loose by a factor of $3$ to $5$ in the failure probability, so the rule is safe but spends one or two qubits more than needed.

## Properties

- **Exact on $t$-bit phases.** If $\varphi = a/2^t$, the output is $a/2^t$ with probability $1$.
- **The eigenvector survives.** Register B ends in $|u\rangle$, not entangled with register A.
- **Superposition input.** For the input $\sum_k c_k |u_k\rangle$ with eigenvectors $|u_k\rangle$ and phases $\varphi_k$, the outcome distribution is $\sum_k |c_k|^2 P_{\varphi_k}(m)$, the mixture of the distributions for the single eigenvectors. After the outcome $m$, register B is in $\sum_k c_k \alpha_m(\varphi_k) |u_k\rangle$ up to normalization, which gives the most weight to the eigenvectors with phase near $m/T$. Order finding uses this with the input $|1\rangle$.
- **Shift of the phase.** The distribution depends only on $\varphi - m/T$, so replacing $U$ by $e(c/T)U$ shifts the outcomes by $c \bmod T$.
- **Non-adaptive.** No query depends on an earlier outcome, and the controlled powers commute, so their order in line L3 does not matter.

## Variants and improvements

- **Iterative phase estimation.** With the semiclassical QFT of Griffiths and Niu, one control qubit is enough. Run the controlled $U^{2^{t-1}}$ first and measure the least significant bit of $m$, then use each outcome to choose a phase correction on the control qubit before the next, smaller power. The qubit count drops to $1 + b$ and the uses stay $2^t - 1$.
- **Kitaev's method.** Run a [Hadamard test](/hadamard-test/) on each $\mathrm{c}U^{2^j}$ several times to estimate $2^j\varphi \bmod 1$ to a constant precision, and combine the estimates from the largest power down into the bits of $\varphi$. This uses no QFT and only one control qubit at a time.
- **Hamiltonians.** For $U = e^{-iH\tau}$, the phase is $\varphi = -E\tau/(2\pi) \bmod 1$, and the cost is $(2^t - 1)\tau$ of total time of evolution. With $\|H\|\tau < \pi$ there is no wraparound, and the energy resolution is $2\pi/(T\tau)$. Each use is a [Hamiltonian simulation](/hamiltonian-simulation/) with its own error, which adds to the error of QPE.
- **Approximate QFT.** Drop the rotations below about $\varepsilon/t$, as on the [QFT](/quantum-fourier-transform/) page. The change in the outcome distribution is at most $\varepsilon$ in total variation distance.
- **Counting.** QPE on the Grover iterate is [quantum counting](/quantum-counting/).

## When to use it

Use QPE when an algorithm needs an eigenvalue of a unitary that it can apply, to many bits, and it can prepare the eigenvector or a state with large overlap with it. This is the case in order finding and discrete logarithms, where the controlled powers are cheap, and in quantum chemistry, where each use is a time evolution. On hardware with noise, the depth of $2^t - 1$ uses in sequence is the main limit. Then iterative phase estimation with one control qubit, or Kitaev's method with repeated short circuits, is often the better choice. If $U$ fits in classical memory as a matrix, compute $\langle u | U | u\rangle$ classically instead.

## Pitfalls

- **Order of the powers.** Qubit $j$ must control $U^{2^j}$. If qubit $0$ controls the largest power, the bits of $m$ come out reversed, unless the swaps of the inverse QFT are dropped to match.
- **The sign of the QFT.** Line L4 needs the inverse QFT, with $e^{-2\pi i/T}$. The forward QFT returns an estimate of $1 - \varphi$.
- **Uses, not queries.** The count $t$ holds only when $U^{2^j}$ costs as much as $U$. For a time evolution or a generic circuit, $\mathrm{c}U^{2^j}$ costs $2^j$ uses, and the total is $2^t - 1$.
- **The global phase of $U$.** Two circuits for $U$ that differ by a global phase give different controlled gates, and QPE measures the phase of the exact matrix that is controlled. When a controlled gate is built from a circuit, keep track of its phase.
- **Too few qubits.** With $t = n$, the result is within $2^{-n}$ only with probability at least $8/\pi^2$, not $1 - \delta$. Add the extra qubits or use the median.
- **The median on a line.** A phase near $0$ gives estimates near $0$ and near $1$. Take the median on the circle, for example after a rotation that moves the cluster of estimates away from $0$.
- **An approximate eigenvector.** If the input has overlap $|c|^2$ with $|u\rangle$, the right phase comes out with probability scaled by $|c|^2$, and the other outcomes are phases of other eigenvectors.

## Implementations

## History

Alexei Kitaev described the first phase estimation method in 1995. It measured an eigenvalue of a unitary bit by bit with repeated one-qubit tests, and Kitaev used it to solve the abelian stabilizer problem, which contains factoring and discrete logarithms. In 1996 Griffiths and Niu showed that the Fourier transform before a measurement needs only one-qubit gates and classical control. In 1998 Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca gave the form with controlled powers and the inverse QFT. They showed that Deutsch's problem, Shor's order finding and other known quantum algorithms are instances of this pattern. The textbook of Nielsen and Chuang gives the rule for the number of qubits. Bessen in 2005 and Mande and de Wolf in 2023 proved lower bounds that match its cost.

## References
