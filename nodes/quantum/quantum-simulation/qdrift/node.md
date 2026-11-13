---
tag: D4KBEW
kind: algorithm
slug: qdrift
name: qDRIFT
aliases:
- randomized Hamiltonian simulation
- random compiler
area: quantum/quantum-simulation
level: advanced
summary: "Campbell (2019): sample N terms of H = sum_j c_j P_j with probability |c_j|/lambda, each applied for time lambda t/N. The averaged channel has error O(lambda^2 t^2/N) for any number of terms."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {l: the coefficient sum of the terms, t: the evolution time, e: the error in half the diamond norm, L: the number of terms}
  time: {worst: O(l^2 t^2/e)}
  space: {extra: O(1)}
properties: {deterministic: false, exact: false, ancilla_free: true, error_norm: diamond, independent_of_term_count: true}
history:
  year: 2019
  people: [Earl Campbell]
  note: Campbell introduced qDRIFT in Physical Review Letters in 2019 (arXiv 2018). It was the first simulation method with a gate count that does not depend on the number of terms.
prereqs: [trotter-suzuki-product-formulas, quantum-channel]
see_also: [trotter-suzuki-product-formulas, commutator-scaling, pauli-string-decomposition, importance-sampling, linear-combination-of-unitaries, quantum-chemistry-simulation, hoeffding-inequality, hamiltonian-simulation]
sources:
  - paper: doi:10.1103/PhysRevLett.123.070503
    title: Earl Campbell, Random compiler for fast Hamiltonian simulation, Physical Review Letters 123(7), 2019, article 070503 (arXiv:1811.08017)
    locator: the qDRIFT protocol, the bound (2 lambda^2 t^2/N) e^(2 lambda t/N) on half the diamond norm distance and the choice N = ceil(2 lambda^2 t^2/epsilon)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 8 (quantum operations) and Chapter 9 (trace distance and distance measures for quantum channels)
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: the comparison of product formulas with randomized methods, and the first order bound used for the comparison on this page
---

qDRIFT is a randomized algorithm for [Hamiltonian simulation](/hamiltonian-simulation/), introduced by Earl Campbell in 2019. For a Hamiltonian $H = \sum_{j=1}^{L} c_j P_j$, given as a [Pauli string decomposition](/pauli-string-decomposition/), it draws $N$ terms independently at random, term $j$ with probability $|c_j|/\lambda$ where $\lambda = \sum_j |c_j|$, and applies each drawn term for the same time $\tau = \lambda t/N$. The average of the random circuits is a quantum channel within $(2\lambda^2t^2/N)e^{2\lambda t/N}$ of the exact evolution in half the diamond norm. So $N = \lceil 2\lambda^2t^2/\epsilon\rceil$ exponentials suffice, roughly, a number that does not depend on the number $L$ of terms. This makes qDRIFT useful for Hamiltonians with very many terms of very different sizes, as in quantum chemistry. Its error falls only as $1/N$ and it ignores commutators, so for local lattice models the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) with [commutator scaling](/commutator-scaling/) are usually cheaper.

## In plain words

A product formula visits every part of the Hamiltonian in every time step, even the tiny parts. qDRIFT instead throws a weighted die at each step. The die picks a part with a chance proportional to its size, and the computer applies that part for a fixed short time. Large parts are picked often and tiny parts rarely, so on average each part acts for the right total time. One run of the random circuit is not a good approximation by itself, but the average over runs is: when the measured results of many runs are averaged, they agree with the exact evolution up to an error that shrinks as the number of steps grows. The number of steps depends on the total size of all parts, not on how many parts there are.

## The problem

The input is a list of terms $(c_j, P_j)$, $j = 1, \ldots, L$, with real $c_j \ne 0$ and $n$-qubit Pauli strings $P_j$, a time $t$, and an error $\epsilon$. Let $\mathcal{U}(\rho) = e^{-iHt}\rho e^{iHt}$ be the exact evolution as a [quantum channel](/quantum-channel/). The output is a random circuit $V$ whose average channel $\mathcal{E}(\rho) = \mathbb{E}[V\rho V^\dagger]$ satisfies
$$\tfrac12 \|\mathcal{E} - \mathcal{U}\|_\diamond \le \epsilon,$$
where $\|\Phi\|_\diamond = \max_X \|(\Phi \otimes \mathrm{id})(X)\|_1/\|X\|_1$ is the diamond norm and $\|\cdot\|_1$ the trace norm. Half the diamond norm is the largest [trace distance](/trace-distance/) between the outputs of the two channels on any input, including inputs entangled with a reference system. The error is in a different norm than the spectral norm error of the product formulas, so the two are compared with care (see the pitfalls).

## The algorithm

The output is a list of pairs $(P, \theta)$, and the circuit applies $e^{-i\theta P}$ for each pair, in the order of the list.

```pseudo id=main
QDRIFT(((c_1, P_1), ..., (c_L, P_L)), t, N, rng)
L1  λ ← |c_1| + ... + |c_L|
L2  τ ← λ t / N
L3  seq ← an empty list
L4  repeat N times
L5      draw j from {1, ..., L} with probability |c_j| / λ        ▷ independent draws from rng
L6      append (P_j, sign(c_j) τ) to seq
L7  return seq
```

Line L5 draws a uniform number $u \in [0, \lambda)$ and takes the first $j$ with $|c_1| + \cdots + |c_j| > u$. Line L6 puts the sign of $c_j$ in the rotation, so each rotation is $e^{-i\tau\,\mathrm{sign}(c_j)P_j}$. To meet an error $\epsilon$, take the least $N$ with $(2\lambda^2t^2/N)e^{2\lambda t/N} \le \epsilon$; it is $\lceil 2\lambda^2t^2/\epsilon\rceil$ or a little more. Each run of the algorithm gives a fresh random list, and the error guarantee is for the average over runs, so an experiment that averages many measured results should draw a new list for each run.

## Example

Take $H = ZZ + 0.5\,XI + 0.5\,IX$ on two qubits, so $\lambda = 2$ and the probabilities are $1/2, 1/4, 1/4$. For $t = 0.5$ and $N = 4$, $\tau = 0.25$, and one draw might give $ZZ, XI, ZZ, IX$, the circuit $e^{-0.25iIX}e^{-0.25iZZ}e^{-0.25iXI}e^{-0.25iZZ}$ (the first factor on the right). On average $ZZ$ is drawn twice, for a total time $0.5$, and each $X$ term once, for $0.25 = 0.5 \cdot 0.5$: the right amounts.

**The averaged channel against the bound.** The page's simulator computes the averaged channel exactly as $\mathcal{E}_1^{N}$ with $\mathcal{E}_1(\rho) = \sum_j p_j U_j\rho U_j^\dagger$, applies it and the exact evolution to half of a maximally entangled state of the two qubits with two reference qubits (the Choi state, which gives a lower bound on half the diamond norm), and takes the trace distance of the outputs.

| $N$ | error, $t = 0.25$ | bound | error, $t = 0.5$ | bound | error, $t = 1$ | bound |
|---|---|---|---|---|---|---|
| 5 | 0.03087 | 0.1221 | 0.1161 | 0.5967 | 0.3778 | 3.561 |
| 10 | 0.01560 | 0.05526 | 0.06041 | 0.2443 | 0.2161 | 1.194 |
| 20 | 0.007844 | 0.02628 | 0.03086 | 0.1105 | 0.1165 | 0.4886 |
| 40 | 0.003933 | 0.01282 | 0.01560 | 0.05256 | 0.06058 | 0.2210 |
| 80 | 0.001970 | 0.006329 | 0.007845 | 0.02563 | 0.03091 | 0.1051 |

The error halves when $N$ doubles (ratios 1.98 to 2.00 at $t = 0.25$), the $1/N$ law, and the bound holds with a factor of about 3 to spare once $N$ is large. For $\lambda = 2$ and $t = 1$ the least $N$ from the bound is 84, 804 and 8004 for $\epsilon = 10^{-1}, 10^{-2}, 10^{-3}$, against $\lceil 2\lambda^2t^2/\epsilon\rceil = 80, 800, 8000$.

**One sequence against the average.** With $t = 0.5$, the input $|00\rangle$ and 200 random sequences (seed 7), the mean trace distance between the output of a single sequence and the exact state is 0.1917 for $N = 10$, 0.0968 for $N = 40$ and 0.0472 for $N = 160$, while the averaged channel has errors 0.0463, 0.0120 and 0.0030. A single sequence has error of order $\lambda t/\sqrt N$, which halves only when $N$ grows fourfold; the average has error of order $\lambda^2t^2/N$.

## Correctness

The average over the independent draws of the random circuit is the channel $\mathcal{E}_1$ applied $N$ times. Write $\mathcal{L}_j(\rho) = -i[\mathrm{sign}(c_j)P_j, \rho]$, so that $e^{\tau\mathcal{L}_j}$ is the rotation of line L6, and note that the exact generator per step is $(t/N)(-i[H, \cdot]) = \tau\sum_j p_j\mathcal{L}_j$. The Taylor series of $\mathcal{E}_1 = \sum_j p_je^{\tau\mathcal{L}_j}$ and of $e^{\tau\sum_j p_j\mathcal{L}_j}$ agree in the terms of degree 0 and 1, and each $\mathcal{L}_j$ has diamond norm at most 2, so one step differs by at most $2(e^{2\tau} - 1 - 2\tau) \le 4\tau^2e^{2\tau}$ in diamond norm. Channels do not increase the diamond norm, so the $N$ steps add: the total is at most $4N\tau^2e^{2\tau} = (4\lambda^2t^2/N)e^{2\lambda t/N}$, and half of it is the stated bound. The full proof is below.

## Complexity

- **Exponentials.** $N = \lceil 2\lambda^2t^2/\epsilon\rceil$ rotations, or a few more, each the exponential of one Pauli string. Each costs $2(w - 1)$ CNOT gates and one rotation for a string of weight $w$ (see [digital quantum simulation](/digital-quantum-simulation/)), and every rotation has the same angle $\tau$, which helps when rotations are synthesized from a finite gate set.
- **No dependence on $L$.** The count depends on $\lambda$, $t$ and $\epsilon$ only. A product formula of first order needs at least $L$ exponentials per step.
- **Classical cost.** Each draw takes $O(\log L)$ time with a binary search over the prefix sums, or $O(1)$ with an alias table, after $O(L)$ preprocessing.
- **Qubits.** The $n$ system qubits; no ancillas.
- **Comparison on a lattice.** For the transverse-field Ising chain $\sum_i Z_iZ_{i+1} + \sum_i X_i$ with $n = 10$ sites, $\lambda = 19$, $t = 1$ and $\epsilon = 10^{-3}$, qDRIFT needs $722\,000$ rotations. The first order product formula with its commutator bound needs $342\,000$, and for $n = 100$ the counts are $79\,202\,000$ against $39\,402\,000$. Since $\lambda^2$ grows as $n^2$ while the commutator constant grows as $n$, qDRIFT loses on lattice models.

## Properties

- **Randomized.** The output circuit is random; the guarantee is for the averaged channel. Running the algorithm once and reusing the circuit gives the much larger single-sequence error.
- **Independent of the number of terms.** Tiny terms are drawn rarely and cost almost nothing, and their sum still acts with the right weight on average.
- **Commutators are ignored.** Even if all terms commute, the averaged channel is not exact: for one term it is exact, but for two commuting terms the random order still gives a mixture of different total times for each term. The error does not vanish when the commutators do.
- **First order in $1/N$.** The error falls as $1/N$, like a first order product formula, and the plain protocol has no symmetric version that cancels the next term.
- **Unbiased drift.** The expected generator of each step equals the exact generator, $\mathbb{E}[\tau\,\mathcal{L}_j] = (t/N)(-i[H, \cdot])$, which is the sense of the name: the random walk drifts in the right direction.

## Variants and improvements

- **Hybrid methods.** Split $H$ into a part with few large terms, simulated by a product formula, and a part with many small terms, simulated by qDRIFT. This keeps the commutator savings of the large part and the $L$ independence of the small part.
- **Randomized product formulas.** Randomly ordering the terms of a product formula in each step, rather than sampling the terms, keeps all terms in each step and lowers the error constant of product formulas.
- **Concentration for one circuit.** Later work bounds the error of a single random circuit for a given input state, with high probability, using matrix concentration inequalities.
- **Other methods priced by $\lambda$.** Methods based on [linear combination of unitaries](/linear-combination-of-unitaries/) also depend on $\lambda$, but they reach a cost of order $\lambda t$ times a logarithmic factor at the price of ancilla qubits and controlled operations.

## When to use it

Use qDRIFT when the Hamiltonian has very many terms, with a few large coefficients and a long tail of small ones, and when the target error is moderate. Electronic structure Hamiltonians in [quantum chemistry simulation](/quantum-chemistry-simulation/) have of order $n^4$ terms for $n$ spin orbitals, with coefficients spread over many orders of magnitude, and Campbell reported large savings for such molecules over product formulas with norm bounds. Do not use it for local lattice models, for long times, or for small errors: its cost grows as $\lambda^2t^2/\epsilon$, while higher-order product formulas and [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) grow almost linearly in $t$.

## Pitfalls

- **Diamond norm versus spectral norm.** The bound is on the averaged channel, in half the diamond norm. Product formula bounds are on a unitary, in the spectral norm. For unitaries $U$ and $V$, half the diamond norm of the difference of the channels is at most $\|U - V\|$, so a spectral norm bound $\epsilon$ for a product formula is also a bound $\epsilon$ in half the diamond norm, but not the other way round. Compare methods in the same norm.
- **Half or full diamond norm.** Campbell's bound $(2\lambda^2t^2/N)e^{2\lambda t/N}$ is for half the diamond norm. In the full diamond norm it is twice as large, $(4\lambda^2t^2/N)e^{2\lambda t/N}$.
- **One circuit for all runs.** Reusing a single sampled circuit for all repetitions of an experiment gives the single-sequence error, of order $\lambda t/\sqrt N$, not the channel error.
- **Expected values.** For an observable $O$ with $\|O\| \le 1$, the error of $\mathrm{Tr}(O\rho(t))$ is at most twice half the diamond norm, $2\epsilon$. Then the statistical error of the average over $S$ runs adds, which the [Hoeffding inequality](/hoeffding-inequality/) bounds by $\sqrt{2\ln(2/\beta)/S}$ with probability $1 - \beta$.
- **Signs.** Negative coefficients must go into the angle, as line L6 does, not into the probability. The probabilities are $|c_j|/\lambda$.
- **Identity terms.** A multiple of the identity in $H$ adds to $\lambda$ and so to the cost, but acts as a global phase. Drop it before sampling.

## Implementations

## History

Campbell (2018 on arXiv, 2019 in Physical Review Letters) introduced qDRIFT as a randomized way to compile Hamiltonian simulation into gates, with the bound in the diamond norm and the cost $O(\lambda^2t^2/\epsilon)$ independent of the number of terms. Before it, randomization had been used in product formulas to choose the order of the terms. Later work combined qDRIFT with product formulas, proved concentration bounds for single random circuits, and used it inside phase estimation for chemistry.

## References
