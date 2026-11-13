---
tag: M9S5CZ
kind: algorithm
slug: multi-product-formulas
name: Multi-product formulas
aliases:
- linear combination of product formulas
area: quantum/quantum-simulation
level: research
summary: "Sum product formulas with different step numbers: M = sum_q C_q S2(t/k_q)^k_q with Lagrange weights cancels the error terms up to order 2m. A quantum circuit applies M by LCU."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {L: the number of terms, m: the number of step numbers, t: the time of one call, s: the 1-norm of the coefficients}
  time: {worst: O(L m^2)}
  space: {extra: O(log m)}
properties: {deterministic: false, exact: false, ancilla_free: false, error_order: 2m, positive_coefficients: false}
history:
  year: 2012
  people: [Andrew M. Childs, Nathan Wiebe]
  note: Multi-product formulas came from classical numerical analysis (Blanes, Casas and Ros 1999; Chin 2010). Childs and Wiebe (2012) implemented them on a quantum computer with a linear combination of unitaries.
prereqs: [trotter-suzuki-product-formulas, linear-combination-of-unitaries]
see_also: [richardson-extrapolation, sequence-extrapolation, higher-order-trotter-suzuki, symplectic-integrators, truncated-taylor-series-simulation, commutator-scaling, hamiltonian-simulation, operator-splitting]
sources:
  - paper: arxiv:1202.5822
    title: "Andrew M. Childs and Nathan Wiebe, Hamiltonian simulation using linear combinations of unitary operations, Quantum Information and Computation 12(11-12), 2012, pages 901 to 924"
    locator: "Theorem 1 (the cost), Theorem 3 (the success probability of a linear combination of nearby unitaries), Section IV, eqs. (12) to (14) (the formula, the coefficients and the Richardson example), Definition 1 and Lemmas 4 and 5 (the well-conditioned choice of steps)"
  - paper: doi:10.1023/A:1008364504014
    title: "Sergio Blanes, Fernando Casas and Joseba Ros, Extrapolation of symplectic integrators, Celestial Mechanics and Dynamical Astronomy 75(2), 1999, pages 149 to 161"
    locator: "the extrapolation of symmetric integrators and the near unitarity of the result (as cited by Childs and Wiebe)"
  - paper: arxiv:0809.0914
    title: "Siu A. Chin, Multi-product splitting and Runge-Kutta-Nystrom integrators, Celestial Mechanics and Dynamical Astronomy 106, 2010, page 391"
    locator: "the closed form of the coefficients C_q (as cited by Childs and Wiebe, eq. (13))"
  - paper: arxiv:1907.11679
    title: "Guang Hao Low, Vadym Kliuchnikov and Nathan Wiebe, Well-conditioned multiproduct Hamiltonian simulation, 2019"
    locator: "the choice of step numbers with a small 1-norm of the coefficients and the resulting simulation cost"
---

A *multi-product formula* (MPF) approximates $e^{-iHt}$ by a weighted sum of [product formulas](/trotter-suzuki-product-formulas/) with different numbers of steps. Let $S_2$ be the symmetric second-order formula and choose distinct step numbers $k_1, \ldots, k_m$. Then
$$M(t) = \sum_{q=1}^m C_q\,S_2(t/k_q)^{k_q}, \qquad C_q = \prod_{p \ne q}\frac{k_q^2}{k_q^2 - k_p^2},$$
has error $O(t^{2m+1})$, the same order as a Suzuki formula of order $2m$. The weights are the [Richardson extrapolation](/richardson-extrapolation/) weights in the variable $x = k^{-2}$: each $S_2(t/k)^k$ is $e^{-iHt}$ plus error terms in even powers of $1/k$, and the sum cancels the first $m - 1$ of them. A Suzuki formula of order $2m$ needs $5^{m-1}$ copies of $S_2$, but $M$ needs only $k_1 + \cdots + k_m$, which is $m(m+1)/2$ for $k_q = q$. The price is that $M$ is a sum, not a product, and some $C_q$ are negative. Childs and Wiebe (2012) apply it with a [linear combination of unitaries](/linear-combination-of-unitaries/), which succeeds with probability $\|M\psi\|^2/s^2$ for $s = \sum_q |C_q|$.

## In plain words

A product formula takes many small steps, and its error shrinks in a known way when the steps get smaller. If we run it with one step, with two steps and with three steps, we get three slightly wrong answers whose errors follow a pattern. A weighted average of the three answers, with some weights negative, can cancel the leading errors and leave a much better answer. This is the old trick of extrapolating to zero step size. On a quantum computer we cannot simply add the results of different circuits. A linear combination of unitaries does it with a few extra qubits, but it succeeds only part of the time, and the chance falls when the weights are large.

## The problem

Given Hermitian terms $H = \sum_{l=1}^L c_lP_l$, a time $t$ and an input state $|\psi\rangle$, prepare a state close to $e^{-iHt}|\psi\rangle$. The cost counts the exponentials $e^{-i\theta P_l}$ in the circuit, the ancilla qubits, and the expected number of repetitions. Here $S_2(\tau) = e^{-iA_1\tau/2}\cdots e^{-iA_L\tau/2}\,e^{-iA_L\tau/2}\cdots e^{-iA_1\tau/2}$ with $A_l = c_lP_l$, the Strang splitting of [operator splitting](/operator-splitting/).

## The algorithm

The index register holds $q$. As on the LCU page, $B$ prepares the weights, SELECT applies the unitary with index $q$, and the outcome 0 of the index register signals success.

```pseudo id=main
MPF((c_1, P_1), ..., (c_L, P_L), t, k_1..k_m, |ψ>)
L1  for q = 1..m: C_q ← Π_{p ≠ q} k_q^2 / (k_q^2 - k_p^2)
L2  s ← |C_1| + ... + |C_m|
L3  for q = 1..m: U_q ← sign(C_q) S_2(t / k_q)^{k_q}
L4  B ← a unitary on the index register with B|0> = s^(-1/2) Σ_q sqrt(|C_q|) |q>
L5  φ ← (B^† ⊗ I) SELECT (B ⊗ I) |0>|ψ>,  SELECT = Σ_q |q><q| ⊗ U_q
L6  measure the index register: outcome 0, with probability ‖M ψ‖^2 / s^2, leaves M|ψ> / ‖M|ψ>‖
```

For long times, cut $t$ into $r$ segments and run the formula on each, or take larger $k_q$ for the whole time. If $s \le 2$, pad the weights to $s = 2$ with $+cI$ and $-cI$ and add one round of oblivious amplitude amplification, as in [truncated Taylor series simulation](/truncated-taylor-series-simulation/). Then the segment succeeds with probability close to 1, because $M$ is close to a unitary.

## Example

The simplest case is $k = (1, 2)$, with $C = (-1/3, 4/3)$:
$$M(t) = \frac{4S_2(t/2)^2 - S_2(t)}{3} = e^{-iHt} + O(t^5).$$
For $k = (1, 2, 3)$ the weights are $C = (1/24, -16/15, 81/40)$ with $s = 3.1333$, and for $k = (1, 2, 3, 4)$, $s = 6.2127$. Take the two-qubit Hamiltonian $H = Z_1Z_0 + 0.5X_0 + 0.5X_1$ and $t = 1$. The spectral norm error of $M$ is:

| step numbers | exponentials of $S_2$ | error | error with all $k_q$ doubled |
|---|---|---|---|
| 1 | 1 | 0.3137 | 0.0711 |
| 1, 2 | 3 | 0.01594 | 0.000936 |
| 1, 2, 3 | 6 | 0.000461 | 0.00000616 |
| 1, 2, 3, 4 | 10 | 0.00000905 | 0.0000000305 |

With all $k_q$ doubled again and again, the error ratios approach $4$, $16$, $64$ and $256$, that is $2^{2m}$. For one short call, halving $t$ divides the error by about $2^{2m+1}$. On the input $|00\rangle$, one run of the LCU succeeds with probability $0.3647$ for $k = (1, 2)$ and $0.1018$ for $k = (1, 2, 3)$. With padding to $s = 2$ and one round of amplification, $k = (1, 2)$ succeeds with probability $0.9997$. The tests in `impl/python` check the weights, both error orders, these numbers, and the LCU output and success probability.

## Correctness

The symmetric formula satisfies $S_2(\tau)S_2(-\tau) = I$ and $S_2(\tau) = I - iH\tau + O(\tau^2)$, so for small $\tau$ it has a logarithm $Z(\tau)$ that is an odd function: $S_2(\tau) = e^{Z(\tau)}$ with $Z(\tau) = -iH\tau + \tau^3E_3 + \tau^5E_5 + \cdots$. Then $S_2(t/k)^k = e^{kZ(t/k)}$, and the exponent is $-iHt + \sum_{j \ge 1}k^{-2j}t^{2j+1}E_{2j+1}$. Expanding the exponential gives $S_2(t/k)^k = \sum_{J \ge 0}k^{-2J}G_J(t)$ with $G_0 = e^{-iHt}$ and $G_J(t) = O(t^{2J+1})$, where the $G_J$ do not depend on $k$. The weights are the Lagrange weights $C_q = \ell_q(0)$ for the nodes $x_q = k_q^{-2}$, so $\sum_q C_qx_q^J$ is 1 for $J = 0$ and 0 for $1 \le J \le m - 1$. Hence $M(t) = e^{-iHt} + \sum_{J \ge m}\big(\sum_q C_qk_q^{-2J}\big)G_J(t) = e^{-iHt} + O(t^{2m+1})$. Doubling every $k_q$ keeps the $C_q$ and multiplies the term $J = m$ by $2^{-2m}$. The LCU step is the block identity $(\langle 0| \otimes I)W(|0\rangle \otimes I) = M/s$. The full proof is in `proofs/correctness.md`.

## Complexity

- **Exponentials.** One $S_2$ uses $2L - 1$ exponentials after the two middle ones merge. One call to SELECT uses $\sum_q k_q$ copies of $S_2$, so $O(Lm^2)$ exponentials for $k_q = q$. A Suzuki formula of the same order uses $5^{m-1}$ copies.
- **Repetitions.** One LCU run succeeds with probability $\|M\psi\|^2/s^2 \approx 1/s^2$. For $k_q = q$, $s$ grows exponentially in $m$, so the cost grows fast with the order. Childs and Wiebe (Definition 1) take $k_1, \ldots, k_{m-1} = 1, \ldots, m-1$ and one large last step number, which makes one positive weight dominate and $s$ close to 1.
- **Cost for long times.** With $r$ segments and the order tuned to $t$ and $\epsilon$, Childs and Wiebe (Theorem 1) need $\tilde O(L^2ht\,e^{1.6\sqrt{\log(Lht/\epsilon)}})$ exponentials, where each term has norm at most $h$. The product formulas known at the time had the constant 2.54 or 2.06 in place of 1.6.
- **Ancillas.** $\lceil\log_2 m\rceil$ index qubits, plus one for the padding.

## Properties

- **Not unitary.** $M$ is a sum, so it is not exactly unitary. For a formula of order $2m$, Blanes, Casas and Ros show that $M$ is unitary to about twice that order, so it is almost unitary at small $t$.
- **Negative weights are needed.** No formula of this form with positive weights has order above 2 (a result of Sheng, cited by Childs and Wiebe). The negative weights raise $s$ above 1.
- **Polynomial length.** The number of exponentials grows as a power of the order, while Suzuki formulas grow exponentially in the order.
- **Commutator structure.** The error terms $E_{2j+1}$ are nested commutators of the terms, as for [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) formulas, so terms that commute give no error.

## Variants and improvements

- **Well-conditioned step numbers.** Low, Kliuchnikov and Wiebe (2019) choose the $k_q$ so that the 1-norm $s$ stays small as the order grows. Then one round of robust oblivious amplitude amplification makes each segment nearly deterministic.
- **Extrapolation of measured values.** Instead of a coherent sum, run each product formula alone, measure an expectation value, and combine the measured numbers with the weights $C_q$. This needs no ancillas, but the statistical noise grows with $s$.
- **Other base formulas.** Any symmetric formula $S_{2p}$ can serve as the base. Then the error has terms in $k^{-2j}$ for $j \ge p$ only, and the same weights cancel them.
- **Classical integrators.** In classical numerical analysis, the same idea gives extrapolated [symplectic integrators](/symplectic-integrators/) and multi-product splittings. See also [sequence extrapolation](/sequence-extrapolation/).

## When to use it

Use a multi-product formula when a product formula is the natural tool, for example for a local lattice Hamiltonian with small commutators, but a high order is needed and a Suzuki formula of that order is too long. It needs an ancilla register and controlled product formulas, so it suits fault-tolerant hardware. On hardware without ancillas, use the extrapolation of measured values. For the best asymptotic cost in $t$ and $\epsilon$, qubitization with quantum signal processing is better.

## Pitfalls

- **Signs into the unitaries.** The weights of $B$ are $|C_q|$, and the sign of $C_q$ goes into $U_q$, as line L3 does.
- **Large $s$.** With $k_q = q$, $s$ is 1.67, 3.13 and 6.21 for $m = 2$, 3 and 4. Each run then succeeds with probability about $1/s^2$, and for many segments the probabilities multiply. Use a well-conditioned choice of $k_q$ or amplification.
- **Not a unitary step.** Oblivious amplitude amplification is only approximate, because $M$ is not unitary. The robust version bounds the extra error by the distance of $M$ from a unitary.
- **Order is asymptotic.** The order holds for small $t\|H\|$. At $t = 1$ in the example the step-doubling ratios are 4.4, 17, 75 and 297 at first and approach $2^{2m}$ only as the steps shrink.
- **Roundoff.** The sum cancels large terms, so a classical evaluation of $M$ loses digits as $m$ grows.

## Implementations

## History

Richardson (1911) introduced extrapolation to zero step size. Blanes, Casas and Ros (1999) applied it to symmetric symplectic integrators, and Chin (2010) gave the closed form of the weights and called the result multi-product splitting. Childs and Wiebe (2012) showed how to apply such sums on a quantum computer with a linear combination of unitaries. This paper introduced the LCU method for Hamiltonian simulation and led to the truncated Taylor series method. Low, Kliuchnikov and Wiebe (2019) found step numbers with small weights. Later work combined multi-product formulas with commutator error bounds and with the extrapolation of measured expectation values.

## References
