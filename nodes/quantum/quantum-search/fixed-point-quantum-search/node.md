---
tag: 33JPWY
kind: algorithm
slug: fixed-point-quantum-search
name: Fixed-point quantum search
aliases:
- Yoder-Low-Chuang search
area: quantum/quantum-search
level: advanced
summary: Search whose success probability does not fall when more steps are applied. Grover's π/3 recursion cubes the failure at each level; the Yoder-Low-Chuang phases keep the √ speedup.
solves: [unstructured-search]
model: quantum-query-model
complexity:
  vars: {N: the number of items, W: a known lower bound on M/N, P: the target failure probability}
  queries: {worst: O(log(1/P)/W)}
  time: {worst: O(log(1/P) log(N)/W)}
  space: {extra: O(log N)}
properties: {deterministic: false, exact: false, one_sided_error: true, needs_m: false, monotone: true, oracle: phase with angle pi/3}
history:
  year: 2005
  people: [Lov K. Grover, Theodore J. Yoder, Guang Hao Low, Isaac L. Chuang]
  note: Grover gave the pi/3 recursion in 2005. Yoder, Low and Chuang gave fixed-point phases with the optimal O(sqrt(1/w)) queries in 2014.
prereqs: [grover-search, amplitude-amplification, chebyshev-polynomials]
see_also: [grover-diffusion-operator, bbht-search, quantum-counting, grover-optimality, minimax-approximation, error-amplification]
sources:
  - paper: doi:10.1103/PhysRevLett.95.150501
    title: "Lov K. Grover, Fixed-point quantum search, Physical Review Letters 95(15), 2005, article 150501"
    locator: the recursion U R_s U^dagger R_t U with the phases pi/3, and the failure probability epsilon -> epsilon^3
  - paper: doi:10.1103/PhysRevLett.113.210501
    title: "Theodore J. Yoder, Guang Hao Low and Isaac L. Chuang, Fixed-point quantum search with an optimal number of queries, Physical Review Letters 113(21), 2014, article 210501 (arXiv:1409.3305)"
    locator: the operator G(alpha, beta) = -S_s(alpha) S_t(beta), the phases alpha_j = -beta_(l-j+1), the success probability P_L = 1 - delta^2 T_L(T_(1/L)(1/delta) sqrt(1 - lambda))^2, and the bound L >= log(2/delta)/sqrt(w)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 4 (the overshoot of a fixed number of Grover iterations when the number of solutions is not known)
---

Fixed-point quantum search finds a marked item with a success probability that does not fall when more steps are applied, for every number $M$ of marked items above a known lower bound. [Grover's search](/grover-search/) oscillates: more iterations than the best number make the result worse, so it needs $M$. Grover's $\pi/3$ recursion, the main algorithm on this page, replaces the two reflections by phase shifts of $\pi/3$, and each level of the recursion cubes the failure probability. The method of Yoder, Low and Chuang, given as a variant, chooses other phases and keeps the square-root speedup of Grover's algorithm.

## In plain words

Grover's method is like a swing. Each push moves the weight toward the good items, but if you push too often the weight swings back. You must know how many good items there are to stop at the top.

Fixed-point search changes the push. It turns by a smaller angle, not a full flip, in a pattern that cancels the swing back. The result: each level of pushes makes the chance of a wrong answer smaller, and never larger. You need to know only that the good items are not rarer than some fraction. The simple version pays for this safety with more pushes. The later version of Yoder, Low and Chuang gets the safety and keeps the speed of Grover's method.

## The problem

The input is $N$, a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$ given as an oracle, a number $w$ with $0 < w \le M/N$, and a target failure probability $\varepsilon$. The number $M$ of marked items is not known. The output is a marked item, with failure probability at most $\varepsilon$. This is [unstructured search](/unstructured-search/) with a lower bound on $M/N$ in place of $M$.

The algorithm needs the selective phase $R_t(\omega) = I - (1 - \omega)P$, which multiplies each marked item by $\omega$, where $P$ is the projector onto the marked items. One call of $R_t(\omega)$ counts as one query. With a bit oracle it costs two queries: compute $f(x)$ into an ancilla, apply the phase gate $\mathrm{diag}(1, \omega)$ to the ancilla, and compute $f(x)$ again to clear it. The start reflection is replaced by $R_s(\omega) = I - (1 - \omega)|s\rangle\langle s|$, with $|s\rangle$ the uniform superposition. Qubit 0 is the least significant bit of $x$.

## The algorithm

Let $\omega = e^{i\pi/3}$ and $\bar\omega = e^{-i\pi/3}$. Define $U_0 = I$ and $U_k = U_{k-1} R_s(\omega) U_{k-1}^\dagger R_t(\omega) U_{k-1}$. The procedure APPLY-U applies $U_k$ or $U_k^\dagger$ to a state.

```pseudo id=main
FIXED-POINT-SEARCH(O_f, N, w, ε)             ▷ 0 < w ≤ M/N, 0 < ε < 1
L1  n ← the smallest integer with (1 - w)^(3^n) ≤ ε
L2  ψ ← |s⟩
L3  ψ ← APPLY-U(n, ψ, +)
L4  measure ψ; let x be the result
L5  if f(x) = 1 then return x else return FAIL

APPLY-U(k, ψ, sign)                          ▷ U_k ψ if sign = +, U_k^† ψ if sign = -
L6  if k = 0 then return ψ
L7  if sign = + then return APPLY-U(k-1, R_s(ω) APPLY-U(k-1, R_t(ω) APPLY-U(k-1, ψ, +), -), +)
L8  return APPLY-U(k-1, R_t(ω̄) APPLY-U(k-1, R_s(ω̄) APPLY-U(k-1, ψ, -), +), -)
```

Line L7 reads from the inside out: apply $U_{k-1}$, then one query $R_t(\omega)$, then $U_{k-1}^\dagger$, then $R_s(\omega)$, then $U_{k-1}$. Line L8 is the inverse: the same factors in reverse order, each one inverted, so $\omega$ becomes $\bar\omega$. The level $n$ in line L1 depends only on $w$ and $\varepsilon$, not on $M$.

## Example

Take $N = 8$ and one marked item, $x = 5$. The table compares the recursion with plain Grover iterations that use the same number of queries.

| level $n$ | queries $(3^n - 1)/2$ | fixed-point success $1 - (7/8)^{3^n}$ | Grover with the same queries |
|---|---|---|---|
| 0 | 0 | 0.1250 | 0.1250 |
| 1 | 1 | 0.3301 | 0.7813 |
| 2 | 4 | 0.6993 | 0.0122 |
| 3 | 13 | 0.9728 | 0.1063 |

For one fixed $M$, Grover is better at the right count: one iteration gives $0.78$ and two give $0.95$. But a wrong count can be very bad. The fixed-point success only grows.

The same circuit works for all $M$. With $n = 2$ (4 queries) and $N = 8$:

| $M$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| fixed point, $1 - (1 - M/8)^9$ | 0.6993 | 0.9249 | 0.9854 | 0.9980 | 0.9999 | 1.0000 | 1.0000 | 1 |
| Grover, 4 iterations | 0.0122 | 1.0000 | 0.1187 | 0.5000 | 0.8813 | 0.0000 | 0.9878 | 1 |

## Correctness

Let $|u\rangle = U_{k-1}|s\rangle$ fail with probability $\varepsilon_{k-1}$, and write $c = 1 - \omega$. Then $U_{k-1}R_s(\omega)U_{k-1}^\dagger = I - c|u\rangle\langle u|$, and a short expansion gives

$$\bar P\,U_k|s\rangle = (1 - c + c^2 - c^2\varepsilon_{k-1})\,\bar P|u\rangle,$$

where $\bar P = I - P$ is the projector onto the unmarked items. For $\omega = e^{i\pi/3}$, $c = e^{-i\pi/3}$ and $1 - c + c^2 = 0$. So the failure amplitude is multiplied by $-c^2\varepsilon_{k-1}$, and $\varepsilon_k = \varepsilon_{k-1}^3$. From $\varepsilon_0 = 1 - M/N$ follows $\varepsilon_n = (1 - M/N)^{3^n}$, which does not increase with $n$, and which is at most $(1 - w)^{3^n} \le \varepsilon$ when $M/N \ge w$. The full proof is in proofs/correctness.md.

## Complexity

- **Queries.** $U_n$ makes $q_n = 3q_{n-1} + 1 = (3^n - 1)/2$ queries. The choice of line L1 gives $3^{n-1} < \ln(1/\varepsilon)/w$, so the run makes fewer than $\frac{3}{2}\ln(1/\varepsilon)/w$ queries, plus one classical check.
- **No quadratic speedup.** The count grows as $1/w$, like classical sampling, not as $1/\sqrt{w}$ like Grover's algorithm. This is the price of the $\pi/3$ recursion.
- **The optimal fixed point.** The variant of Yoder, Low and Chuang reaches failure at most $\delta^2$ for every $M/N \ge w$ with $(L-1)/2$ queries, where $L \ge \ln(2/\delta)/\sqrt{w}$ suffices. That is $O(\log(1/\delta)/\sqrt{w})$, which matches the [lower bound](/grover-optimality/) up to the factor $\log(1/\delta)$.
- **Gates and qubits.** Each $R_s$ costs $O(\log N)$ gates, as the [diffusion operator](/grover-diffusion-operator/) with a phase in place of $-1$. Data qubits: $\lceil \lg N \rceil$.

## Properties

- **Monotone.** For the $\pi/3$ recursion, the success probability $1 - (1 - M/N)^{3^n}$ never decreases with the level $n$, for every $M$.
- **Fixed point.** When $M \ge 1$, the final state tends to the marked subspace as $n$ grows. There is nothing to overshoot.
- **Needs only a lower bound.** The input is $w \le M/N$, not $M$. Each larger $M$ gives a smaller failure.
- **One run, no measurement in between.** Unlike [BBHT search](/bbht-search/), it is one coherent circuit. This matters when the search is a subroutine of a larger quantum algorithm that cannot stop to measure.
- **Not a reflection.** $R_s(\omega)$ and $R_t(\omega)$ are phase shifts, not reflections, so the analysis of Grover's algorithm as a rotation does not apply.

## Variants and improvements

- **Yoder, Low and Chuang (2014).** Use $l$ steps $G(\alpha_j, \beta_j) = -S_s(\alpha_j)S_t(\beta_j)$ with $S_t(\beta) = I - (1 - e^{i\beta})P$ and $S_s(\alpha) = I - (1 - e^{-i\alpha})|s\rangle\langle s|$. Let $L = 2l + 1$, $\gamma^{-1} = T_{1/L}(1/\delta)$, where $T_L$ is the [Chebyshev polynomial](/chebyshev-polynomials/), and choose $\alpha_j = -\beta_{l-j+1} = 2\cot^{-1}\big(\tan(2\pi j/L)\sqrt{1 - \gamma^2}\big)$. Then the success probability is $P_L = 1 - \delta^2\,T_L\big(T_{1/L}(1/\delta)\sqrt{1 - \lambda}\big)^2$ with $\lambda = M/N$, and $P_L \ge 1 - \delta^2$ for every $\lambda \ge 1 - \gamma^2$. The failure is a Chebyshev polynomial, which is the [minimax](/minimax-approximation/) choice, so it is as small as possible over the whole range of $\lambda$. With $\delta \to 1$ all phases become $\pi$, and the method becomes plain Grover search. The implementation checks the formula against the simulator.
- **Any start algorithm.** Both methods work with $|s\rangle$ replaced by $A|0\rangle$ for any algorithm $A$, as in [amplitude amplification](/amplitude-amplification/).
- **Random iteration counts.** [BBHT search](/bbht-search/) avoids the overshoot in another way: it measures after each round and draws a random iteration count. Its expected cost is $O(\sqrt{N/M})$ with no bound on $M$ needed, but it is not one coherent circuit.

## When to use it

Use a fixed-point method when $M$ is not known within a constant factor, a lower bound on $M/N$ is known, and the search must be one coherent circuit, for example inside a larger quantum algorithm. In that case use the phases of Yoder, Low and Chuang; the $\pi/3$ recursion is simpler to analyze but needs $\Theta(1/w)$ queries. When $M$ is known, plain Grover search is cheaper. When an intermediate measurement is allowed, [BBHT search](/bbht-search/) is simpler and needs no lower bound.

## Pitfalls

- **The phase $\pi$ in the recursion.** "L7 with $\omega = -1$" makes each factor a reflection, and the recursion becomes a fixed sequence of Grover iterations, which overshoots. The cancellation $1 - c + c^2 = 0$ needs $\omega = e^{i\pi/3}$. Use "L7 with $\omega = e^{i\pi/3}$".
- **The wrong inverse.** "L8 return APPLY-U(k-1, R_t(ω) APPLY-U(k-1, R_s(ω) APPLY-U(k-1, ψ, -), +), -)" uses $\omega$ in place of $\bar\omega$, so it is not $U_k^\dagger$, and the next level does not cube the failure. Use $\bar\omega$ in line L8.
- **Expecting a square-root speedup from the recursion.** "L1 $n \leftarrow \lceil \log_3(1/\sqrt{w}) \rceil$" gives about $1/\sqrt{w}$ queries but far too small a level: for $w = 1/8$ it gives $n = 1$ and success only $0.33$ in the example. Keep "L1 $n \leftarrow$ the smallest integer with $(1 - w)^{3^n} \le \varepsilon$", or use the variant of Yoder, Low and Chuang.
- **Counting a selective phase as one bit-oracle query.** $R_t(\omega)$ needs two calls of a bit oracle (compute and uncompute). Say which oracle the count refers to.
- **Taking monotone to mean fast.** Monotone in the level does not mean better than Grover. With $M$ known, Grover gives $0.95$ with 2 queries in the example, the recursion $0.70$ with 4.

## Implementations

## History

Boyer, Brassard, Høyer and Tapp showed in 1996 how a fixed number of Grover iterations fails when the number of solutions is unknown. Grover proposed the $\pi/3$ recursion in 2005, in "Fixed-point quantum search", and showed that each level cubes the failure probability. The recursion gives up the square-root speedup. Yoder, Low and Chuang found phases in 2014 that keep the fixed-point property and need only $O(\log(1/\delta)/\sqrt{w})$ queries, which is optimal.

## References
