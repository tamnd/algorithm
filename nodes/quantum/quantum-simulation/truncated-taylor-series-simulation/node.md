---
tag: 6TQGRV
kind: algorithm
slug: truncated-taylor-series-simulation
name: Truncated Taylor series simulation
aliases:
- Taylor series Hamiltonian simulation
- Berry-Childs-Cleve-Kothari-Somma simulation
area: quantum/quantum-simulation
level: advanced
summary: "Cut e^(-iHt) into r = ceil(lambda t/ln 2) segments, write each as a truncated Taylor series of Pauli products, and apply it by LCU with one round of oblivious amplitude amplification."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {l: the coefficient sum of the Pauli terms, t: the evolution time, e: the error, L: the number of terms, n: the number of system qubits}
  time: {worst: O(L (n + log L) l t log(l t/e)/log log(l t/e))}
  space: {extra: O(log(L) log(l t/e)/log log(l t/e))}
properties: {deterministic: false, exact: false, ancilla_free: false, error_norm: spectral, success_probability: close to 1}
history:
  year: 2015
  people: [Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, Rolando D. Somma]
  note: The method appeared on arXiv in December 2014 and in Physical Review Letters in 2015. It was the first simple simulation method with a cost polylogarithmic in 1/e.
prereqs: [hamiltonian-simulation, linear-combination-of-unitaries]
see_also: [taylor-series-method, interaction-picture-simulation, optimal-hamiltonian-simulation, trotter-suzuki-product-formulas, qdrift, pauli-string-decomposition, sparse-hamiltonian-simulation, amplitude-amplification]
sources:
  - paper: doi:10.1103/PhysRevLett.114.090502
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Simulating Hamiltonian dynamics with a truncated Taylor series, Physical Review Letters 114(9), 2015, article 090502 (arXiv:1412.4687)"
    locator: "eqs. (3) and (4) (segments and the order K), eqs. (13) to (16) (oblivious amplitude amplification for a nonunitary sum), eqs. (17) to (21) (the index set, s = 2 and r = ceil(T/ln 2)), and eqs. (22) to (25) (qubit and gate counts)"
  - paper: doi:10.1145/2591796.2591854
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the 46th ACM STOC, 2014, pages 283 to 292 (arXiv:1312.1414)"
    locator: "Lemmas 3.6 and 3.7 (oblivious amplitude amplification) and Theorem 1.2 (the lower bound in the error)"
  - paper: arxiv:1501.01715
    title: "Dominic W. Berry, Andrew M. Childs and Robin Kothari, Hamiltonian simulation with nearly optimal dependence on all parameters, Proceedings of the 56th IEEE FOCS, 2015, pages 792 to 809"
    locator: "Lemma 6 (robust oblivious amplitude amplification), Theorem 1 (the sparse upper bound) and Theorem 2 (the lower bound in tau and e)"
  - paper: arxiv:1202.5822
    title: "Andrew M. Childs and Nathan Wiebe, Hamiltonian simulation using linear combinations of unitary operations, Quantum Information and Computation 12(11-12), 2012, pages 901 to 924"
    locator: "Section IV (linear combinations of product formulas) and Lemma 2 (the success amplitude of a linear combination)"
---

*Truncated Taylor series simulation* is an algorithm for [Hamiltonian simulation](/hamiltonian-simulation/) by Berry, Childs, Cleve, Kothari and Somma (2015). The Hamiltonian is a sum $H = \sum_{l=1}^L c_lP_l$ of Pauli strings, for example from a [Pauli string decomposition](/pauli-string-decomposition/), with $\lambda = \sum_l |c_l|$. The algorithm cuts the time $t$ into $r = \lceil\lambda t/\ln 2\rceil$ segments of length $\tau = t/r$. In each segment, it expands $e^{-iH\tau}$ as the [Taylor series](/taylor-series-method/) $\sum_{k \le K}(-iH\tau)^k/k!$, writes every power of $H$ as a sum of products of Pauli strings, and applies the sum with a [linear combination of unitaries](/linear-combination-of-unitaries/). The 1-norm of the weights is at most $e^{\lambda\tau} \le 2$, so one round of oblivious amplitude amplification makes each segment succeed with probability close to 1. The order $K = O(\log(\lambda t/\epsilon)/\log\log(\lambda t/\epsilon))$ gives error $\epsilon$, so the cost is $O(\lambda t\log(\lambda t/\epsilon)/\log\log(\lambda t/\epsilon))$ calls to the controlled terms. Product formulas need a number of steps that grows as a power of $1/\epsilon$. Here the growth in $1/\epsilon$ is only logarithmic.

## In plain words

A product formula splits a time step into small steps for each term and pays for the error of the split. This method does not split. It uses the textbook series for the exponential: one, plus the step, plus half its square, and so on. It stops after a few terms, because the terms soon become very small. Each term is a product of simple operations, so the whole series is a weighted sum of simple operations. A quantum circuit can apply a weighted sum with the help of extra qubits, but it succeeds only part of the time. If the time step is short enough, one round of amplitude amplification makes it succeed almost always. Then the circuit repeats the step until it reaches the full time. More accuracy costs only a few more terms in each step.

## The problem

Given real $c_l$, Pauli strings $P_l$ on $n$ qubits, a time $t > 0$ and an error $\epsilon > 0$, apply to any $n$-qubit state $|\psi\rangle$ an operation that gives $e^{-iHt}|\psi\rangle$ within $\epsilon$, with $H = \sum_l c_lP_l$. Write $\sigma_l = \mathrm{sign}(c_l)$, so $c_lP_l = |c_l|\,\sigma_lP_l$ with the unitary $\sigma_lP_l$. The circuit may use ancilla qubits and controlled versions of the $P_l$. The costs are the number of segments times the order $K$, which counts uses of the controlled terms, and the number of ancilla qubits.

## The algorithm

The index register holds the label $j = (k, l_1, \ldots, l_k)$ of a term of the series. As on the [linear combination of unitaries](/linear-combination-of-unitaries/) page, $B$ prepares the weights, SELECT applies the term with label $j$, and $R = 2|0\rangle\langle 0| \otimes I - I$ reflects about the zero index.

```pseudo id=main
TAYLOR-SIM((c_1, P_1), ..., (c_L, P_L), t, K, |ψ>)
L1  λ ← |c_1| + ... + |c_L|
L2  r ← ceil(λ t / ln 2);  τ ← t / r          ▷ λ τ ≤ ln 2
L3  for 0 ≤ k ≤ K and 1 ≤ l_1..l_k ≤ L: β_j ← (τ^k / k!) |c_l1| ... |c_lk|,  V_j ← (-i)^k σ_l1 P_l1 ... σ_lk P_lk;  then add (c, I) and (c, -I) with 2c = 2 - Σ_j β_j
L4  B ← a unitary on the index register with B|0> = 2^(-1/2) Σ_j sqrt(β_j) |j>
L5  repeat r times
L6      apply A = -W R W^† R W to |0>|ψ>, with W = (B^† ⊗ I) SELECT (B ⊗ I)
L7      measure the index register; on outcome 0, the system holds the new |ψ>; reset the index to |0>
L8  return |ψ>
```

Line L3 lists $1 + L + \cdots + L^K$ terms. Their weights add up to $s_K = \sum_{k \le K}(\lambda\tau)^k/k! \le e^{\lambda\tau} \le 2$. The two padding terms $+cI$ and $-cI$ cancel in the sum, but they raise the 1-norm to exactly 2. A circuit stores $k$ in unary in $K$ qubits and each $l_i$ in $\lceil\log_2 L\rceil$ qubits, so SELECT is $K$ controlled selections of one term each. To meet an error $\epsilon$, take the least $K$ with $(1 + e)^r - 1 \le \epsilon$, where $e$ is the bound of the correctness section.

## Example

Take $H = 0.6X - 0.8Z$ on one qubit and $t = 2$. Then $\lambda = 1.4$, $\lambda t/\ln 2 = 4.04$, so $r = 5$, $\tau = 0.4$ and $\lambda\tau = 0.56$. Since $H^2 = I$, the exact evolution is $\cos(2)I - i\sin(2)H$. For $K = 3$, line L3 lists $1 + 2 + 4 + 8 = 15$ terms with $s_3 = 1.7461$, and the padding adds $c = 0.1270$ twice. Each segment applies $W$ three times and succeeds with probability above $0.99999$. From $|0\rangle$, the distance from the exact state, against the bound of the correctness section, is:

| $K$ | terms | error | bound |
|---|---|---|---|
| 1 | 3 | 0.1052 | 2.036 |
| 2 | 7 | 0.0506 | 0.191 |
| 3 | 15 | 0.00168 | 0.0234 |
| 4 | 31 | 0.000403 | 0.00253 |
| 5 | 63 | 0.0000096 | 0.000233 |

Each new order divides the error by about 10, and the bound follows the same trend. The tests in `impl/python` check these numbers, check that the weighted sum is the truncated series exactly, check the segment formula below, and run random 2-qubit Hamiltonians.

## Correctness

Let $\tilde V = \sum_j \beta_jV_j$, the sum of line L3. Expanding the products shows $\tilde V = \sum_{k \le K}(-i\tau H)^k/k!$, the padding terms cancel, and $\|\tilde V - e^{-iH\tau}\| \le \delta = \sum_{k > K}(\lambda\tau)^k/k!$ because $\|H\| \le \lambda$. With $\Pi = |0\rangle\langle 0| \otimes I$ and $\Pi W\Pi = |0\rangle\langle 0| \otimes \tilde V/2$, expanding $R = 2\Pi - I$ gives
$$\Pi A\Pi = |0\rangle\langle 0| \otimes \Big(\tfrac{3}{2}\tilde V - \tfrac{1}{2}\tilde V\tilde V^\dagger\tilde V\Big),$$
which is eq. (14) of the paper for $s = 2$. If $\tilde V$ were unitary, this would be $\tilde V$ exactly, which is oblivious amplitude amplification. With $\tilde V = U + E$, $U = e^{-iH\tau}$ and $\|E\| \le \delta$, the terms of first order in $E$ give $\tfrac{1}{2}(E - UE^\dagger U)$, so the segment operator $A_0$ satisfies $\|A_0 - U\| \le e = \delta + \tfrac{3}{2}\delta^2 + \tfrac{1}{2}\delta^3$. A telescoping sum over the $r$ segments gives $\|A_0^r - e^{-iHt}\| \le (1 + e)^r - 1$. The outcome 0 in every segment has probability $\|A_0^r\psi\|^2$, and the normalized output is within twice that distance of $e^{-iHt}|\psi\rangle$. The full proof is in `proofs/correctness.md`.

## Complexity

- **Segments and order.** $r = \lceil\lambda t/\ln 2\rceil$ segments. Since $\delta \le 2(\ln 2)^{K+1}/(K+1)!$, the order $K$ with $\delta \le \epsilon/(4r)$ is $O(\log(\lambda t/\epsilon)/\log\log(\lambda t/\epsilon))$. In the example with $\epsilon = 10^{-3}$, the least $K$ is 5, 6, 7 and 8 for $t = 2$, 10, 100 and 1000.
- **Calls.** Each segment uses SELECT twice and SELECT$^\dagger$ once, so $3r$ calls in all. Each SELECT applies up to $K$ controlled terms. The total is $O(\lambda t\log(\lambda t/\epsilon)/\log\log(\lambda t/\epsilon))$ controlled Pauli strings.
- **Gates.** One controlled selection of a term costs $O(L(n + \log L))$ gates, which gives the bound in the front matter. $B$ and $B^\dagger$ cost $O(LK)$ gates each.
- **Ancillas.** $K + K\lceil\log_2 L\rceil$ qubits for the index, plus one for the padding.
- **Sparse input.** For a $d$-sparse $H$ given by oracles, the paper splits $H$ into equal 1-sparse parts and gets $O(\tau\log(\tau/\epsilon)/\log\log(\tau/\epsilon))$ queries with $\tau = d^2\|H\|_{\max}t$. Berry, Childs and Kothari (2015, Theorem 1) lower $\tau$ to $d\|H\|_{\max}t$.

## Properties

- **Polylogarithmic in $1/\epsilon$.** The $\epsilon$-dependence is $\log(1/\epsilon)/\log\log(1/\epsilon)$ per unit of $\lambda t$. The lower bound $\Omega(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$ (Berry, Childs and Kothari 2015, Theorem 2) shows that this factor is necessary, but the bound has a sum where the algorithm has a product.
- **Priced by $\lambda$.** The cost depends on the 1-norm $\lambda$ and not on commutators. Terms that commute give no saving, unlike the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/).
- **Nearly deterministic.** Each segment fails with probability $O(\delta)$. A failure is detected by the measurement, and the run starts again.
- **Ancilla cost.** The index register grows with $K\log L$, while a product formula needs no ancillas.

## Variants and improvements

- **Rescaling time.** If $\lambda t/\ln 2$ is not an integer, the paper keeps $r - 1$ full segments and pads only the last one. Here every segment is shortened and padded, which gives the same circuit for all segments.
- **Interaction picture.** [Interaction picture simulation](/interaction-picture-simulation/) applies the same series to a time-ordered (Dyson) exponential, so the cost depends on the size of the small part of $H$.
- **Qubitization.** [Optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) by quantum signal processing reaches $O(\lambda t + \log(1/\epsilon))$ calls with only a few ancillas, the sum of the two terms of the lower bound.
- **Multi-product formulas.** [Multi-product formulas](/multi-product-formulas/) use the same LCU machinery with product formulas as the unitaries, and need fewer ancillas.
- **Fractional queries.** The earlier method of Berry, Childs, Cleve, Kothari and Somma (2014) had the same cost through a simulation of fractional queries. The Taylor series method gives it with a simpler circuit.

## When to use it

Use it when the error must be small, the Hamiltonian is a sum of a moderate number of Pauli strings or is sparse with an oracle, and ancilla qubits are available. It is a clear and analyzable baseline for fault-tolerant simulation. For short times with large errors, or on hardware with few qubits, product formulas or [qDRIFT](/qdrift/) are cheaper. For the best asymptotic cost with few ancillas, use qubitization with quantum signal processing.

## Pitfalls

- **$s$ must not exceed 2.** If $\lambda\tau > \ln 2$, the weights add up to more than 2 for large $K$, and one round of amplification overshoots. Line L2 rounds $r$ up for this reason.
- **The Taylor series alone is not unitary.** The segment operator is $\tfrac{3}{2}\tilde V - \tfrac{1}{2}\tilde V\tilde V^\dagger\tilde V$, not $\tilde V$. Its error is of order $\delta$ only because $\tilde V$ is within $\delta$ of a unitary.
- **Errors add over segments.** The per-segment error must be about $\epsilon/r$, not $\epsilon$. The bound $(1 + e)^r - 1$ is about $re$.
- **Signs and phases.** The weights must be positive. Put $\mathrm{sign}(c_l)$ and the factor $(-i)^k$ into the unitaries $V_j$, as line L3 does.
- **Number of terms.** The full index set has $L^K$ entries at order $K$. A circuit never lists them; it prepares $B$ as a product over $K + 1$ registers.
- **Identity terms.** A multiple of $I$ in $H$ adds to $\lambda$ but only gives a global phase. Drop it first.

## Implementations

## History

Childs and Wiebe (2012) introduced the linear combination of unitaries for simulation, with product formulas as the unitaries. Berry, Childs, Cleve, Kothari and Somma (STOC 2014) reached a cost polylogarithmic in $1/\epsilon$ through fractional queries and introduced oblivious amplitude amplification. In December 2014 the same authors showed that a truncated Taylor series gives the same cost directly, with a robust version of oblivious amplitude amplification for a sum that is only close to unitary. The paper appeared in Physical Review Letters in 2015. Berry, Childs and Kothari (2015) then improved the dependence on the sparsity and proved the lower bound. Low and Chuang (2017) closed the gap with quantum signal processing.

## References
