---
tag: 514Y6M
kind: algorithm
slug: interaction-picture-simulation
name: Interaction picture simulation
aliases:
- Low-Wiebe interaction picture method
area: quantum/quantum-simulation
level: research
summary: "For H = A + B with e^(-iAs) easy, simulate the rotating-frame part e^(iAs) B e^(-iAs) by a truncated Dyson series with LCU, so the number of segments depends only on the size of B."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {b: the 1-norm of the coefficients of B, a: the norm of A, t: the evolution time, e: the error, m: the number of ancilla qubits of the oracle for B}
  time: {worst: O(b t log(b t/e)/log log(b t/e))}
  space: {extra: O(m + log(t (a + b)/e))}
properties: {deterministic: false, exact: false, ancilla_free: false, error_norm: spectral, success_probability: close to 1}
history:
  year: 2018
  people: [Guang Hao Low, Nathan Wiebe]
  note: The paper appeared on arXiv in May 2018. It gave a truncated Dyson series algorithm with few qubits for time-dependent Hamiltonians and applied it in the interaction picture.
prereqs: [truncated-taylor-series-simulation, linear-combination-of-unitaries]
see_also: [time-dependent-hamiltonian-simulation, optimal-hamiltonian-simulation, qubitization, trotter-suzuki-product-formulas, quantum-chemistry-simulation, midpoint-rule, amplitude-amplification, hamiltonian-simulation]
sources:
  - paper: arxiv:1805.00675
    title: "Guang Hao Low and Nathan Wiebe, Hamiltonian simulation in the interaction picture, arXiv:1805.00675 (version 2, June 2019)"
    locator: "numbering of arXiv v2: eq. (2) (the interaction picture), Theorem 3 and Corollary 4 (the truncated Dyson series in one and in many segments), Lemma 5 (truncation and discretization), Lemma 6 (query cost in the interaction picture), Theorem 7 (gate cost), Theorems 9 and 10 (sparse time-dependent and diagonally dominant Hamiltonians), Lemma 13 (the compression gadget) and Lemma 14 (robust oblivious amplitude amplification)"
  - paper: doi:10.1103/PhysRevLett.114.090502
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Simulating Hamiltonian dynamics with a truncated Taylor series, Physical Review Letters 114(9), 2015, article 090502 (arXiv:1412.4687)"
    locator: "eqs. (13) to (16) (oblivious amplitude amplification for a sum that is close to unitary) and eq. (26) (the truncated Dyson series for time-dependent Hamiltonians)"
---

*Interaction picture simulation* is an algorithm for [Hamiltonian simulation](/hamiltonian-simulation/) by Low and Wiebe (2018). The Hamiltonian is a sum $H = A + B$, where $A$ can be large but $e^{-iAs}$ is easy to apply, for example because $A$ is diagonal, and $B = \sum_l c_lP_l$ is small with $\lambda_B = \sum_l|c_l|$. In the rotating frame of $A$, the evolution is $e^{-iHt} = e^{-iAt}\,\mathcal{T}\exp(-i\int_0^tH_I(s)\,ds)$ with $H_I(s) = e^{iAs}Be^{-iAs}$, a [time-dependent Hamiltonian](/time-dependent-hamiltonian-simulation/) of norm $\|B\|$. The algorithm cuts the time into segments with $\lambda_B\tau \le \ln 2$, applies a truncated and discretized Dyson series of each segment with a [linear combination of unitaries](/linear-combination-of-unitaries/) and one round of oblivious amplitude amplification, as in [truncated Taylor series simulation](/truncated-taylor-series-simulation/), and then applies $e^{-iA\tau}$. The number of segments is $O(\lambda_Bt)$ and does not depend on $A$. The size of $A$ enters only through the number of time points, and the gate cost grows only with its logarithm.

## In plain words

Sometimes one part of a Hamiltonian is large but simple, such as the energies of separate particles, and the other part is small but hard, such as their interactions. A general method pays for the large part at every step. This method moves into a frame that turns with the simple part. In that frame only the small part acts, but it changes with time. The method writes the change over a short interval as a series of products of the small part at a few chosen times, and applies the series with extra qubits, as the Taylor series method does. After each interval it applies the simple part once, which is cheap. The number of intervals depends only on the small part. The large part costs only a few more qubits to label the times.

## The problem

Given Hermitian $A$ and $B = \sum_lc_lP_l$ on $n$ qubits, a circuit for $e^{-iAs}$ for any $s$, a time $t > 0$ and an error $\epsilon > 0$, apply to any $n$-qubit state $|\psi\rangle$ an operation that gives $e^{-i(A + B)t}|\psi\rangle$ within $\epsilon$. The circuit may use ancilla qubits, controlled $P_l$, and $e^{-iAs}$ controlled on a register that holds $s$. The costs are the number of uses of the controlled terms of $B$, the number of uses of $e^{-iAs}$, and the number of ancillas. Qubit 0 is the least significant bit.

## The algorithm

Each segment has $M$ cells of width $h = \tau/M$ with midpoints $s_q = (q + \tfrac{1}{2})h$, $0 \le q < M$. A label $j$ is a tuple of $k \le K$ pairs $(q_i, l_i)$ of a cell and a term. Its unitary is the product of the factors $e^{iAs_{q_i}}\sigma_{l_i}P_{l_i}e^{-iAs_{q_i}}$, with $\sigma_l = \mathrm{sign}(c_l)$, ordered by cell with later cells to the left, and with the pairs in one cell in the order of the tuple. As on the [linear combination of unitaries](/linear-combination-of-unitaries/) page, $B_{\mathrm{prep}}$ prepares the weights, SELECT applies the unitary of label $j$, and $R = 2|0\rangle\langle 0| \otimes I - I$ reflects about the zero index.

```pseudo id=main
IP-SIM(A, (c_1, P_1), ..., (c_L, P_L), t, M, K, |ψ>)
L1  λ_B ← |c_1| + ... + |c_L|
L2  r ← ceil(λ_B t / ln 2);  τ ← t / r          ▷ λ_B τ ≤ ln 2
L3  for each label j = ((q_1, l_1), ..., (q_k, l_k)) with k ≤ K: β_j ← h^k |c_l1| ... |c_lk| / k!,  V_j ← (-i)^k (the ordered product);  then add (c, I) and (c, -I) with 2c = 2 - Σ_j β_j
L4  B_prep ← a unitary on the index register with B_prep|0> = 2^(-1/2) Σ_j sqrt(β_j) |j>
L5  repeat r times
L6      apply -W R W^† R W to |0>|ψ>, with W = (B_prep^† ⊗ I) SELECT (B_prep ⊗ I); measure the index; on outcome 0 keep the system
L7      |ψ> ← e^(-iAτ) |ψ>
L8  return |ψ>
```

The weights of line L3 at order $k$ add up to $(\lambda_B\tau)^k/k!$, so the sum over $k \le K$ is at most $e^{\lambda_B\tau} \le 2$, and the padding raises it to exactly 2. The labels with repeated cells are kept. With them, the sum $D_{K,M} = \sum_j\beta_jV_j$ is exactly the part of degree at most $K$ in $h$ of the product $\prod_q e^{-ihH_I(s_q)}$, a [midpoint rule](/midpoint-rule/) for the time-ordered exponential with error $O(h^2)$ per unit of time. A circuit holds the $k$ cell labels in $K$ registers of $\lceil\log_2M\rceil$ qubits and puts them in order with a [sorting network](/sorting-network/), as Low and Wiebe do.

## Example

Take $A = 2\,ZI + IZ$ with $\|A\| = 3$, $B = 0.3\,XX + 0.2\,IX$ with $\lambda_B = 0.5$, and $t = 2$. Then $r = \lceil 1/\ln 2\rceil = 2$ and $\tau = 1$. The [truncated Taylor series](/truncated-taylor-series-simulation/) on all of $H$ would have $\lambda = 3.5$ and $r = 11$ segments. Here $\|[A, B]\| = 1.865$ and $\|[A, [A, B]]\| = 10.87$. The distance of the midpoint product, the limit $K \to \infty$, from the exact segment $e^{iA\tau}e^{-iH\tau}$, computed by eigendecomposition, against the bound of the correctness section, is:

| $M$ | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|
| error | 0.2921 | 0.02138 | 0.004939 | 0.001215 | 0.0003026 | 0.00007557 | 0.00001889 |
| bound | 0.903 | 0.199 | 0.0463 | 0.0111 | 0.00273 | 0.000676 | 0.000168 |

From $M = 4$ on, each doubling of $M$ divides the error by 4.0, the order 2 of the midpoint rule. The full circuit from $|\psi\rangle = \tfrac{1}{2}(|00\rangle + i|01\rangle - |10\rangle + |11\rangle)$ gives, for the distance of the output from $e^{-2iH}|\psi\rangle$:

| $M$ | $K$ | labels | error | success probability | bound |
|---|---|---|---|---|---|
| 2 | 3 | 85 | 0.02925 | 0.999997 | 0.604 |
| 4 | 1 | 9 | 0.04535 | 0.9906 | 0.577 |
| 4 | 2 | 73 | 0.01306 | 0.99988 | 0.161 |
| 4 | 3 | 585 | 0.006106 | 0.999997 | 0.108 |
| 8 | 1 | 17 | 0.04518 | 0.9909 | 0.441 |
| 8 | 2 | 273 | 0.008836 | 0.99986 | 0.0748 |

The run with $M = 4$ and $K = 3$ uses 10 index qubits and 2 system qubits. A larger $K$ removes the truncation error, and a larger $M$ removes the discretization error. The tests in `impl/python` check these numbers, check that the weighted sum of line L3 is the truncated midpoint product, check the order 2 in $M$, check the circuit against the segment formula below, and run random 2-qubit Hamiltonians.

## Correctness

Because $H$ does not depend on time, $U_I(\tau) = e^{iA\tau}e^{-iH\tau}$ solves $\tfrac{d}{d\tau}U_I = -iH_I(\tau)U_I$, so $e^{-iH\tau} = e^{-iA\tau}\,\mathcal{T}\exp(-i\int_0^\tau H_I(s)\,ds)$, and every segment uses the same $H_I$ on $[0, \tau]$. Expanding $\prod_q e^{-ihH_I(s_q)}$ and collecting the terms of the same cells shows that $D_{K,M}$ is its part of degree at most $K$, so $\|D_{K,M} - \prod_q e^{-ihH_I(s_q)}\| \le \sum_{k > K}(\lambda_B\tau)^k/k!$. A comparison of each cell with its midpoint exponential, with the variation of constants, gives
$$\Big\|\prod_q e^{-ihH_I(s_q)} - U_I(\tau)\Big\| \le d_M = \frac{\tau^3}{M^2}\Big(\frac{\|[A, [A, B]]\|}{24} + \frac{\lambda_B\|[A, B]\|}{4}\Big) + \frac{\tau^4\|[A, B]\|^2}{16M^3}.$$
So $D_{K,M}$ is within $\eta$, the sum of the two bounds, of the unitary $U_I(\tau)$. The block of $-WRW^\dagger RW$ is $\tfrac{3}{2}D - \tfrac{1}{2}DD^\dagger D$, which is within $e = \eta + \tfrac{3}{2}\eta^2 + \tfrac{1}{2}\eta^3$ of $U_I(\tau)$, as on the page of truncated Taylor series simulation. Line L7 turns it into $e^{-iH\tau}$, and over $r$ segments the error is at most $(1 + e)^r - 1$. The full proof is in `proofs/correctness.md`.

## Complexity

- **Segments.** $r = \lceil\lambda_Bt/\ln 2\rceil = O(\lambda_Bt)$ segments, each with one $e^{-iA\tau}$. The number does not depend on $A$.
- **Order.** As for the Taylor series, $K = O(\log(\lambda_Bt/\epsilon)/\log\log(\lambda_Bt/\epsilon))$ makes the truncation error at most $\epsilon/(4r)$ per segment. Each segment uses SELECT three times, and each SELECT applies up to $K$ controlled terms, so the number of calls to the terms of $B$ is $O(\lambda_Bt\log(\lambda_Bt/\epsilon)/\log\log(\lambda_Bt/\epsilon))$ (Low and Wiebe, Lemma 6).
- **Cells.** With $\|[A, B]\| \le 2\|A\|\lambda_B$ and $\|[A, [A, B]]\| \le 4\|A\|^2\lambda_B$, the bound $d_M \le \epsilon/(4r)$ holds for $M = O((\tau\|A\| + \sqrt{\tau\|A\|})\sqrt{r/\epsilon})$. Low and Wiebe use left points and labels without repeated cells, which is a rule of order 1, and need $M = O(t(\|A\| + \lambda_B)/\epsilon)$. In both cases, $M$ enters only through $\lceil\log_2M\rceil$ qubits per register and the controlled $e^{-iAs}$ on a register of that size.
- **Ancillas.** With the compression gadget of Low and Wiebe (Lemma 13), $O(m + \log(t(\|A\| + \lambda_B)/\epsilon))$ qubits, where $m$ is the number of ancillas of the oracle for $B$. The flat index of the tests is larger, $\lceil\log_2(2 + \sum_{k \le K}(ML)^k)\rceil$ qubits.
- **Gates.** If $e^{-iAs}$ costs $O(|s|\,\mathrm{polylog}(s/\epsilon))$ gates, the total gate count is $O(\lambda_Bt)$ times the cost of one call to $B$ and of one simulation of $A$ for time $O(1/\lambda_B)$, up to factors polylogarithmic in $\|A\|$, $t$ and $1/\epsilon$ (Low and Wiebe, Theorem 7).

## Properties

- **Priced by the small part.** The number of segments and calls depends on $\lambda_B$, not on $\|A\| + \lambda_B$. In the example, 2 segments replace the 11 of the Taylor series on all of $H$.
- **Logarithmic in the size of $A$.** $\|A\|$ appears only in the number of time points, and the gate count depends on its logarithm. A [Trotter-Suzuki product formula](/trotter-suzuki-product-formulas/) in the interaction picture has a cost that grows as a power of $\|[A, B]\|$.
- **Polylogarithmic in $1/\epsilon$.** As for the Taylor series, the cost per segment grows as $\log(1/\epsilon)/\log\log(1/\epsilon)$.
- **Nearly deterministic.** Each segment fails with probability $O(\eta)$, and the measurement detects a failure.
- **Not optimal in the product.** The cost has the product of $\lambda_Bt$ and the $\epsilon$ factor, not the sum that [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) reaches for time-independent $H$.

## Variants and improvements

- **Time-dependent Hamiltonians.** The truncated Dyson series alone (Low and Wiebe, Theorem 3 and Corollary 4) simulates any time-dependent $H(s)$ given by an oracle that holds $H$ at $M$ times, with a cost that scales with $\max_s\|H(s)\|$ and only logarithmically with the derivative. See [time-dependent Hamiltonian simulation](/time-dependent-hamiltonian-simulation/).
- **Sparse and diagonally dominant Hamiltonians.** For a $d$-sparse $H$ with a large diagonal $A$, Low and Wiebe (Theorem 10) get a gate cost exponentially better in the size of the diagonal. Their Theorem 9 gives a quadratic improvement in the query cost of sparse time-dependent simulation.
- **Chemistry and lattice models.** With $A$ the kinetic or the diagonal part, Low and Wiebe reduce the gate cost of plane-wave [quantum chemistry simulation](/quantum-chemistry-simulation/) from $\tilde O(N^{11/3}t)$ to $\tilde O(N^2t)$, and reduce the cost for Hubbard models with long-range interactions.
- **Choice of the rule.** This page keeps the labels with repeated cells and uses midpoints, which gives the midpoint product with error $O(1/M^2)$. Low and Wiebe use left points and labels without repeated cells, with error $O(1/M)$, which is simpler to sort but needs more cells.

## When to use it

Use it when $H$ splits into a part that is large but easy to exponentiate, such as a diagonal or a sum of commuting terms, and a part that is small with an efficient oracle. Typical cases are chemistry in a plane-wave basis and lattice models with a strong on-site term. If the two parts have similar sizes, the rotating frame gives nothing, and qubitization or the Taylor series on all of $H$ is simpler.

## Pitfalls

- **The frame needs $e^{-iAs}$ for many $s$.** SELECT applies $e^{iAs_q}$ for the cell held in a register, so $A$ must be simulated, controlled on that register, for times that are multiples of $h$. If $A$ is not easy, the method moves the cost instead of removing it.
- **Repeated cells.** If the labels with repeated cells are dropped, the discretization error is of order 1 in $h$, and a term of size $\|B\|^2\tau^2/(2M)$ remains even for constant $H_I$.
- **Order of the factors.** The product must put later times to the left. A product in the wrong order approximates the anti-time-ordered exponential.
- **The frame at the end.** Line L7 must apply $e^{-iA\tau}$ after each segment. Leaving it out returns the state in the rotating frame.
- **Signs and phases.** As for the Taylor series, the weights must be positive, so $\mathrm{sign}(c_l)$ and $(-i)^k$ go into the unitaries.

## Implementations

## History

The interaction picture comes from Dirac's perturbation theory, where Dyson's series expands the time-ordered exponential. Berry, Childs, Cleve, Kothari and Somma (2015) introduced the truncated Taylor series with oblivious amplitude amplification, and proposed a truncated Dyson series for time-dependent Hamiltonians without a full analysis. Low and Wiebe (arXiv 2018) gave a rigorous analysis and a version with few qubits, with a compression gadget and sorting of the time labels, and used it in the interaction picture to make the cost depend on the small part of $H$. They applied it to chemistry in a plane-wave basis, to Hubbard models and to sparse diagonally dominant Hamiltonians.

## References
