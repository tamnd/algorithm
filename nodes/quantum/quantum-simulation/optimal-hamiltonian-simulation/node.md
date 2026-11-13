---
tag: WBXH9G
kind: algorithm
slug: optimal-hamiltonian-simulation
name: Optimal Hamiltonian simulation by quantum signal processing
aliases:
- Low-Chuang optimal simulation
- QSP-based Hamiltonian simulation
area: quantum/quantum-simulation
level: research
summary: "Apply the Jacobi-Anger series of cos(tH) and sin(tH) to a block encoding of H by quantum signal processing, then amplify: O(a t + log(1/e)) queries, the optimal cost."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {a: the normalization of the block encoding, t: the evolution time, e: the error, m: the number of ancilla qubits of the block encoding}
  time: {worst: O(a t + log(1/e))}
  space: {extra: O(m)}
properties: {deterministic: false, exact: false, ancilla_free: false, error_norm: spectral, success_probability: close to 1}
history:
  year: 2017
  people: [Guang Hao Low, Isaac L. Chuang]
  note: The method appeared on arXiv in June 2016 and in Physical Review Letters in 2017. Low and Chuang gave the block encoding form in the qubitization paper, and Gilyen, Su, Low and Wiebe restated it as an eigenvalue transformation in 2019.
prereqs: [quantum-signal-processing, qubitization, sparse-hamiltonian-simulation]
see_also: [quantum-eigenvalue-transformation, block-encoding, linear-combination-of-unitaries, truncated-taylor-series-simulation, interaction-picture-simulation, no-fast-forwarding-theorem, chebyshev-series, amplitude-amplification]
sources:
  - paper: doi:10.1103/PhysRevLett.118.010501
    title: "Guang Hao Low and Isaac L. Chuang, Optimal Hamiltonian simulation by quantum signal processing, Physical Review Letters 118(1), 2017, article 010501 (arXiv:1606.02685)"
    locator: "the main result (the query cost O(t d max|H| + log(1/e)/log log(1/e)) for d-sparse Hamiltonians through the quantum walk)"
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "Theorem 1 (O(t + log(1/e)) queries for a Hamiltonian in standard form, with ceil(log2 N) + ceil(log2 d) + 2 qubits)"
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM STOC, 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1: Lemma 57 (the Jacobi-Anger polynomials), Theorem 58 (block-Hamiltonian simulation), Lemma 59 (bounds on the degree), Corollary 60 (the tight query count and the note on the Low-Chuang form), Lemma 61 and Corollary 62 (robust simulation)"
  - paper: arxiv:1501.01715
    title: "Dominic W. Berry, Andrew M. Childs and Robin Kothari, Hamiltonian simulation with nearly optimal dependence on all parameters, Proceedings of the 56th IEEE FOCS, 2015, pages 792 to 809"
    locator: "Theorem 2 (the lower bound in tau and e)"
---

*Optimal Hamiltonian simulation by quantum signal processing* is an algorithm for [Hamiltonian simulation](/hamiltonian-simulation/) by Low and Chuang (2017). The input is a [block encoding](/block-encoding/) $U$ of $H/\alpha$, for example from a [linear combination of unitaries](/linear-combination-of-unitaries/) of Pauli strings or from the oracles of a [sparse Hamiltonian](/sparse-hamiltonian-simulation/). The algorithm writes $\cos(\alpha tx)$ and $\sin(\alpha tx)$ as truncated [Chebyshev series](/chebyshev-series/) with Bessel coefficients (the Jacobi-Anger expansion). It applies the two polynomials to $H/\alpha$ with [quantum signal processing](/quantum-signal-processing/) on the [qubitized](/qubitization/) walk, combines them into $e^{-iHt}$ with one more qubit, and removes the leftover factor with oblivious amplitude amplification. The cost is $O(\alpha t + \log(1/\epsilon))$ calls to $U$, with only two ancilla qubits beyond those of $U$. A sum of the time term and the error term matches the lower bound, so no algorithm in this query model can do better than a constant factor.

## In plain words

Earlier methods paid for time and accuracy together: each step of time had to be accurate, so the costs multiplied. This method does not cut time into steps. A smooth wave can be written as a short sum of simple polynomials, and the needed length grows with the time plus a small amount for each extra digit of accuracy. Quantum signal processing can apply any such polynomial to the energies of a quantum system, with a short sequence of calls and turns of one extra qubit. The method builds the polynomials for the cosine and the sine waves, adds them, and gets the full evolution at a reduced strength. Two rounds of amplitude amplification then restore the full strength. The costs add instead of multiply, and a known lower bound shows that this sum cannot be improved.

## The problem

Given a time $t > 0$, an error $\epsilon > 0$ and a unitary $U$ on $m + n$ qubits with $(\langle 0^m| \otimes I)U(|0^m\rangle \otimes I) = H/\alpha$ for a Hermitian $H$ on $n$ qubits, build a unitary $G$ on more qubits whose top-left $2^n \times 2^n$ block is within $\epsilon$ of $e^{-iHt}$ in the spectral norm. Here, as on the [qubitization](/qubitization/) page, $U$ is also Hermitian, so $U^2 = I$; any block encoding can be made Hermitian with one more qubit. The ancillas are the high qubits, and qubit 0 is the least significant bit. The cost is the number of calls to $U$ and to controlled $U$. A run applies $G$ to $|0\rangle|\psi\rangle$ and measures the ancillas; outcome 0 leaves the system within about $\epsilon$ of $e^{-iHt}|\psi\rangle$.

## The algorithm

Let $\kappa = 2\sin(\pi/10) \approx 0.618$, let $\Pi$ project on the states with all ancillas 0, and let $R = 2\Pi - I$. QET$(U, p)$ is the circuit of the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) that has the block $p(H/\alpha)$ for a real polynomial $p$ of definite parity with $|p| \le 1$ on $[-1, 1]$. It uses $\deg p$ calls to $U$ and one more qubit.

```pseudo id=main
OPT-HS(U, α, t, R)
L1  τ ← α t
L2  c_0 ← J_0(τ);  c_2k ← 2 (-1)^k J_2k(τ) for 1 ≤ k ≤ R;  s_2k+1 ← 2 (-1)^k J_2k+1(τ) for 0 ≤ k ≤ R
L3  p_c(x) ← κ Σ_k c_2k T_2k(x);  p_s(x) ← κ Σ_k s_2k+1 T_2k+1(x)      ▷ degrees 2R and 2R + 1
L4  Q_c ← QET(U, p_c);  Q_s ← QET(U, p_s)
L5  V ← (Had ⊗ I)(|0><0| ⊗ Q_c + |1><1| ⊗ (-i Q_s))(Had ⊗ I)    ▷ block (p_c - i p_s)(H/α)/2
L6  G ← V;  repeat 2 times: G ← -V R V^† R G
L7  return G
```

Line L2 lists the Jacobi-Anger coefficients, where $J_k$ is the Bessel function of the first kind and $T_k$ is the Chebyshev polynomial of the first kind: $\cos(\tau x) = J_0(\tau) + 2\sum_{k \ge 1}(-1)^kJ_{2k}(\tau)T_{2k}(x)$ and $\sin(\tau x) = 2\sum_{k \ge 0}(-1)^kJ_{2k+1}(\tau)T_{2k+1}(x)$. The block of $V$ is close to $\sin(\pi/10)\,e^{-iHt}$. One round of line L6 multiplies the angle $\pi/10$ by 3 and the second by $5/3$ more, so the block becomes close to $\sin(\pi/2)\,e^{-iHt} = e^{-iHt}$. The factor $\kappa$ leaves a margin so that $|p_c|, |p_s| \le 1$ even after the truncation. To meet an error $\epsilon$, take the least $R$ whose bound in the correctness section is at most $\epsilon$.

## Example

Take $H = 0.6X + 0.3Z + 0.1Y$ on one qubit and $t = 3$. The block encoding is PREP SELECT PREP with a Householder PREP on $m = 2$ ancillas, so $U = U^\dagger$ and $\alpha = 1$. With the QET qubit and the qubit of line L5, $G$ acts on 5 qubits, a $32 \times 32$ unitary. Here $\tau = 3$. The distance of the top-left $2 \times 2$ block of $G$ from $e^{-3iH}$, computed by eigendecomposition, against the bound of the correctness section, is:

| $R$ | degree $2R + 1$ | error | bound |
|---|---|---|---|
| 2 | 5 | 0.0059537 | 1.09 |
| 3 | 7 | 0.00087866 | 0.045 |
| 4 | 9 | 0.0000101547 | 0.0014 |
| 5 | 11 | 0.00000037013 | 0.000029 |
| 6 | 13 | 0.000000002955 | 0.00000042 |

Each step of $R$ adds two to the degree, and the error falls faster than geometrically once $2R$ is larger than $\tau$. At $t = 1$, $R = 2$ already gives $4.1 \cdot 10^{-6}$ and $R = 4$ gives $1.1 \cdot 10^{-10}$. The tests in `impl/python` check these numbers, check the truncation of the Jacobi-Anger series on a grid, check that the block of $V$ is $(p_c - ip_s)(H/\alpha)/2$, check the block of $G$ against the polynomial of the correctness section, and run random 2-qubit Hamiltonians.

## Correctness

Let $c_R$ and $s_R$ be the truncated series, so $p_c = \kappa c_R$ and $p_s = \kappa s_R$. Since $|T_k| \le 1$ on $[-1, 1]$, both $\|c_R - \cos(\tau\,\cdot)\|_\infty$ and $\|s_R - \sin(\tau\,\cdot)\|_\infty$ are at most $\eta = 2\sum_{k > 2R}|J_k(\tau)|$. The block of $V$ is $Z = (p_c - ip_s)(H/\alpha)/2$, so with $s = \sin(\pi/10) = \kappa/2$,
$$\|Z - s\,e^{-iHt}\| \le \delta = \kappa\eta.$$
In each 2-dimensional subspace of the singular value decomposition of the block, line L6 is a Grover rotation, as in [amplitude amplification](/amplitude-amplification/). After two rounds, the block of $G$ is $f(Z) = 5Z - 20ZZ^\dagger Z + 16ZZ^\dagger ZZ^\dagger Z$, which is $\sin 5\theta = 5\sin\theta - 20\sin^3\theta + 16\sin^5\theta$ on each singular value $\sin\theta$. Then $f(s\,e^{-iHt}) = \sin(\pi/2)\,e^{-iHt}$, and $f$ is Lipschitz on the ball of radius $\rho = s + \delta$, so
$$\|\Pi G\Pi - e^{-iHt}\| \le \delta\,(5 + 60\rho^2 + 80\rho^4).$$
The full proof is in `proofs/correctness.md`.

## Complexity

- **Degree.** The bound $|J_k(\tau)| \le (\tau/2)^k/k!$ makes $\eta$ fall faster than geometrically once $2R > e\tau/2$. Gilyén, Su, Low and Wiebe (Lemmas 57 and 59) show that degree $r = \Theta(\tau + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/\tau))$ suffices for $\epsilon$-approximations of $\cos(\tau x)$ and $\sin(\tau x)$. The least degree $2R + 1$ with $\eta \le \epsilon$ is:

  | $\tau$ | $\epsilon = 10^{-3}$ | $10^{-6}$ | $10^{-9}$ |
  |---|---|---|---|
  | 1 | 5 | 9 | 11 |
  | 2 | 7 | 11 | 13 |
  | 4 | 11 | 15 | 17 |
  | 8 | 15 | 21 | 25 |

  Doubling $\tau$ adds a fixed amount, and each factor 1000 in $1/\epsilon$ adds a few degrees, which shows the sum $\tau + \log(1/\epsilon)$.
- **Calls.** $Q_c$ and $Q_s$ use $U$ $2R$ and $2R + 1$ times. In the simple circuit of line L5, each use is controlled, so $V$ costs $4R + 1$ calls, and $G$ uses $V$ or $V^\dagger$ 5 times. The total is $5(4R + 1) = O(\alpha t + \log(1/\epsilon))$ calls. Gilyén, Su, Low and Wiebe (Theorem 58) merge the two sequences so that only 3 calls are controlled, and use the factor $\tfrac{1}{2}$ with one round of robust amplification, for $3r$ calls with $r$ the degree.
- **Tight form.** Their Corollary 60 gives the exact order of the query count, $\Theta(\alpha t + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/(\alpha t)))$, for all $t$.
- **Ancillas.** $m + 2$ qubits: those of $U$, one for QET and one for line L5. Qubitization gives the same count, $\lceil\log_2 N\rceil + \lceil\log_2 d\rceil + 2$ qubits in all (Low and Chuang, qubitization, Theorem 1).
- **Gates.** $O(m)$ gates for each reflection, so $O(mR)$ gates beyond the calls. The phases are computed once, classically, from $\tau$ and $R$.
- **Sparse input.** For a $d$-sparse $H$ with oracle access, the sparse-access construction on the [block encoding](/block-encoding/) page has $\alpha = d\|H\|_{\max}$, and the cost is $O(\tau + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/\tau))$ queries with $\tau = d\|H\|_{\max}t$.

## Properties

- **Optimal.** Berry, Childs and Kothari (2015, Theorem 2) prove that $\Omega(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$ queries are necessary for sparse Hamiltonians, and the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/) gives the linear term. This algorithm meets the bound, with the correction of the next paragraph.
- **A correction to the stated cost.** Low and Chuang stated the cost as $O(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$. Gilyén, Su, Low and Wiebe (Corollary 60) note that this form does not match the true cost in every range: for $\tau = \log\log(1/\epsilon)$ the cost is $\Theta(\log(1/\epsilon)/\log\log\log(1/\epsilon))$. The form with $\log(e + \log(1/\epsilon)/\tau)$ is correct for all $\tau$, including $\tau < 1$.
- **Additive.** The time and the error enter as a sum. [Truncated Taylor series simulation](/truncated-taylor-series-simulation/) has the product $\tau\log(\tau/\epsilon)/\log\log(\tau/\epsilon)$.
- **Few ancillas.** Two qubits beyond the block encoding, against $O(\log(1/\epsilon))$ index qubits for the Taylor series.
- **Robust.** If $U$ encodes $H'$ with $\|H - H'\| \le \beta$, the output is within $\epsilon + t\beta$ of $e^{-iHt}$, since $\|e^{-iHt} - e^{-iH't}\| \le t\|H - H'\|$ (Gilyén, Su, Low and Wiebe, Lemma 61 and Corollary 62).
- **Nearly deterministic.** The ancillas return 0 with probability at least $(1 - \epsilon)^2$.

## Variants and improvements

- **The original form.** Low and Chuang (2017) applied quantum signal processing to the quantum walk of Childs for a $d$-sparse $H$, with the phases of the Jacobi-Anger polynomials. The qubitization paper (2019) replaced the walk by any block encoding.
- **Halving instead of $\kappa$.** Gilyén, Su, Low and Wiebe (Theorem 58) build polynomials within $\epsilon/6$ of $\cos$ and $\sin$ with $|p| \le 1$, combine them with the block $e^{-iHt}/2$, and use one round of robust oblivious amplitude amplification. The factor $\kappa$ of this page trades two more uses of $V$ for a margin that needs no rescaling of the polynomials.
- **Phases.** For large degrees, the phases come from stable numerical methods, as on the [quantum signal processing](/quantum-signal-processing/) page. The test code solves for them directly at small degrees.
- **Interaction picture.** If $H = A + B$ with a large $A$ that is easy to simulate, [interaction picture simulation](/interaction-picture-simulation/) gives a cost that scales with $\|B\|$ instead of $\|A\| + \|B\|$.
- **Time-dependent Hamiltonians.** A single polynomial does not work, because $e^{-iHt}$ is then a time-ordered exponential. See [time-dependent Hamiltonian simulation](/time-dependent-hamiltonian-simulation/).

## When to use it

Use it on a fault-tolerant computer when the error must be small and $H$ has a block encoding with a small $\alpha$, such as a short sum of Pauli strings or a sparse matrix with oracles. It has the best asymptotic query count and uses few ancillas. For estimates of energies, [qubitization](/qubitization/) with [quantum phase estimation](/quantum-phase-estimation/) on the walk itself avoids the polynomial. For short times and large errors, or with many terms that nearly commute, [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) can be cheaper in gates.

## Pitfalls

- **The factor $\alpha$.** The cost scales with $\alpha t$, not $\|H\|t$. A poor block encoding with large $\alpha$ makes the simulation slow even if $\|H\|$ is small.
- **The bounded polynomial condition.** QET needs $|p| \le 1$ on all of $[-1, 1]$. The truncated cosine can exceed 1 by up to $\eta$. Scale the polynomials, as $\kappa$ does here.
- **Parity.** QET applies real polynomials of definite parity. The cosine part is even and the sine part is odd, and each needs its own sequence before line L5 combines them.
- **The sign of the exponent.** The block of $V$ is built for $e^{-iHt}$. With the other sign of $p_s$, the result is $e^{+iHt}$.
- **Rounds and amplitude.** The number of rounds must match the starting amplitude: two rounds need $\sin(\pi/10)$, and one round needs $\sin(\pi/6) = \tfrac{1}{2}$. Otherwise the amplitude overshoots.
- **Phase precision.** At large degrees, the phases must be computed with care; naive root finding becomes unstable.

## Implementations

## History

Childs (2010) and Berry and Childs (2012) simulated sparse Hamiltonians with a quantum walk, at a cost linear in $\tau$ but polynomial in $1/\epsilon$. Berry, Childs, Cleve, Kothari and Somma (2014 and 2015) reached $O(\tau\log(\tau/\epsilon)/\log\log(\tau/\epsilon))$ with fractional queries and the [truncated Taylor series](/truncated-taylor-series-simulation/), and Berry, Childs and Kothari (2015) combined the walk with a linear combination of unitaries and proved the lower bound $\Omega(\tau + \log(1/\epsilon)/\log\log(1/\epsilon))$. Low and Chuang (arXiv 2016, Physical Review Letters 2017) used quantum signal processing on the walk to reach the sum of the two terms. In the qubitization paper, also from 2016 and published in Quantum in 2019, they extended the result to any block encoding. Gilyén, Su, Low and Wiebe (2019) restated it as an eigenvalue transformation, gave the tight form of the cost, and proved robustness.

## References
