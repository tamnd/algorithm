---
tag: YTTWRG
kind: theorem
slug: universal-quantum-simulator
name: Universal quantum simulator
aliases:
- Lloyd universal simulation theorem
area: quantum/quantum-simulation
level: advanced
summary: "Lloyd (1996): a Hamiltonian made of L terms, each on O(1) qubits, can be simulated for time t to error epsilon by a circuit of poly(L, t, 1/epsilon) one- and two-qubit gates."
prereqs: [hamiltonian-simulation, lie-trotter-product-formula]
see_also: [digital-quantum-simulation, feynman-quantum-simulation, trotter-suzuki-product-formulas, commutator-scaling, solovay-kitaev-theorem, universal-gate-set, no-fast-forwarding-theorem, bqp]
sources:
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the main argument, the product formula for local Hamiltonians and the count of steps and gates
  - paper: doi:10.1007/BF02650179
    title: Richard P. Feynman, Simulating physics with computers, International Journal of Theoretical Physics 21(6/7), 1982, pages 467 to 488
    locator: the question whether a universal quantum simulator exists
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.5 (universality of CNOT and one-qubit gates) and Section 4.7 (simulation of quantum systems)
  - paper: doi:10.1007/s00220-006-0150-x
    title: Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)
    locator: Theorem 1 (higher order product formulas for sums of terms) and the lower bound for fast forwarding
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: Proposition 15 (first order commutator bound) and the gate counts for lattice Hamiltonians
---

The universal quantum simulator theorem, proved by Seth Lloyd in 1996, says that a quantum computer can simulate every *local* quantum system efficiently. If a Hamiltonian is a sum of $L$ terms and each term acts on a constant number of qubits, then its time evolution $e^{-iHt}$ can be approximated to any error $\epsilon$ by a circuit of one- and two-qubit gates whose size is polynomial in $L$, $t$ and $1/\epsilon$. This answered the question that Feynman left open in 1982 (see [Feynman's quantum simulation idea](/feynman-quantum-simulation/)), and it is the reason why [digital quantum simulation](/digital-quantum-simulation/) is possible. The proof is the [Lie-Trotter product formula](/lie-trotter-product-formula/) plus the fact that each small unitary is a constant number of gates. The task it solves is [Hamiltonian simulation](/hamiltonian-simulation/) in the local terms access model; the faster product formulas that refine it are on the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) page.

## Statement

**Theorem (Lloyd 1996).** Let $H = \sum_{j=1}^{L} H_j$ be a Hamiltonian on $n$ qubits in which each $H_j$ is Hermitian, acts on at most $k$ qubits, and has spectral norm $\|H_j\| \le \Lambda$. Let $t > 0$ and $\epsilon > 0$. Then there is a circuit $V$ of [CNOT](/cnot-gate/) and one-qubit gates with
$$\| V - e^{-iHt} \| \le \epsilon$$
and at most $g_k L r$ gates, where
$$r = \left\lceil \frac{L(L-1)\Lambda^2 t^2}{2\epsilon} \right\rceil$$
and $g_k = O(k^2 4^k)$ is the number of CNOT and one-qubit gates that suffice for any unitary on $k$ qubits. For constant $k$ the gate count is $O(L^3 \Lambda^2 t^2/\epsilon)$.

**Refinement.** If each $H_j$ fails to commute with at most $d$ other terms, the same holds with $r = \lceil L d \Lambda^2 t^2 / (2\epsilon) \rceil$, so the gate count is $O(L^2 d \Lambda^2 t^2 / \epsilon)$. For a lattice of $n$ sites with nearest-neighbor terms, $L = O(n)$ and $d = O(1)$, so the count is $O(n^2 \Lambda^2 t^2 / \epsilon)$.

**Finite gate sets.** With a finite [universal gate set](/universal-gate-set/) such as Clifford plus T, each one-qubit gate is approximated by the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/). The count is multiplied by a factor $O(\log^c (G/\epsilon))$, where $G$ is the exact count and $c$ is a constant (below 4).

Since a $k$-local Hamiltonian on $n$ qubits has at most $\binom{n}{k} 4^k$ terms, $L$ is polynomial in $n$, and the count is $\mathrm{poly}(n, t, 1/\epsilon)$.

## In plain words

A quantum system made of many small parts that interact a few at a time can be imitated by a quantum computer. The computer breaks the evolution into many short time steps. In each step it lets each interaction act alone for a short time, one after another. Each of these pieces touches only a few qubits, so it is a handful of gates. Doing the pieces one after another is not the same as doing them all at once, because the pieces do not commute, but the mistake in one step shrinks with the square of the step length. With enough steps, the total mistake is as small as we like, and the number of gates grows only polynomially with the size of the system, the simulated time and the inverse of the allowed error. So a single quantum computer can imitate every system of this kind.

## Proof

**Step 1: the product formula.** Let $S(\tau) = e^{-iH_1\tau} e^{-iH_2\tau} \cdots e^{-iH_L\tau}$. By the many-term corollary of the [Lie-Trotter product formula](/lie-trotter-product-formula/),
$$\| S(t/r)^r - e^{-iHt} \| \le \frac{t^2}{2r} \sum_{1 \le j < l \le L} \|[H_j, H_l]\|.$$
Each commutator has $\|[H_j, H_l]\| \le 2 \|H_j\| \|H_l\| \le 2\Lambda^2$, and it is zero when $H_j$ and $H_l$ act on disjoint qubits or commute for another reason. There are $L(L-1)/2$ pairs, so the sum is at most $L(L-1)\Lambda^2$. With the $r$ of the statement,
$$\| S(t/r)^r - e^{-iHt} \| \le \frac{L(L-1)\Lambda^2 t^2}{2r} \le \epsilon.$$
Under the refinement, at most $Ld/2$ pairs fail to commute, so the sum is at most $L d \Lambda^2$, and the smaller $r$ suffices.

**Step 2: each factor is a constant number of gates.** The factor $e^{-iH_j t/r}$ is a unitary that acts on the at most $k$ qubits of $H_j$ and as the identity on the rest. Every unitary on $k$ qubits is a product of at most $2^{k-1}(2^k - 1)$ two-level unitaries (by Givens rotations, as in a QR decomposition), and each two-level unitary on $k$ qubits is $O(k^2)$ CNOT and one-qubit gates (Nielsen and Chuang, Section 4.5). So each factor is at most $g_k = O(k^2 4^k)$ gates, exactly. For a Pauli string term $H_j = c_j P_j$ of weight $w$ much less is needed: $2(w-1)$ CNOT gates, one rotation and $2w$ basis changes (see [digital quantum simulation](/digital-quantum-simulation/)).

**Step 3: count.** The circuit $V = S(t/r)^r$ has $Lr$ factors, so at most $g_k L r$ gates, and its error is at most $\epsilon$ by Step 1. For constant $k$, $g_k$ is a constant and $Lr = O(L^3 \Lambda^2 t^2/\epsilon)$, or $O(L^2 d\Lambda^2 t^2/\epsilon)$ under the refinement.

**Step 4: finite gate sets.** Replace each of the $G = g_k L r$ gates by a product of gates from the finite set within $\epsilon/(2G)$ of it, and choose $r$ for the error $\epsilon/2$. Errors of unitaries add under products, $\|U_1 U_2 - W_1 W_2\| \le \|U_1 - W_1\| + \|U_2 - W_2\|$, so the total error is at most $\epsilon/2 + G \cdot \epsilon/(2G) = \epsilon$. The Solovay-Kitaev theorem gives each replacement in $O(\log^c(2G/\epsilon))$ gates. $\square$

## Consequences

- **Digital simulators are universal.** One gate-based machine can simulate every local system, from spin chains to molecules (after a [fermion-to-qubit mapping](/fermion-to-qubit-mapping/)) and lattice field theories (after a cutoff). This is the base of [digital quantum simulation](/digital-quantum-simulation/) and of [quantum many-body simulation](/quantum-many-body-simulation/).
- **Local dynamics is in BQP.** Estimating a local observable after the evolution under a local Hamiltonian for polynomial time, to inverse polynomial precision, is a problem in [BQP](/bqp/). The converse also holds, because a circuit can be encoded in a local Hamiltonian, so the problem is BQP-complete.
- **Analog devices can be checked against digital ones.** An [analog quantum simulator](/analog-quantum-simulation/) with a local Hamiltonian computes nothing beyond a polynomial-size circuit.
- **Energies.** The circuit $V$ can be the controlled unitary of [quantum phase estimation](/quantum-phase-estimation/), which estimates eigenvalues of $H$.
- **A bridge to better algorithms.** The theorem uses only the first order formula and crude norm bounds. Every later method improves one factor: the [higher-order Trotter-Suzuki formulas](/higher-order-trotter-suzuki/) bring $t^2$ down to $t^{1+1/(2k)}$, [commutator scaling](/commutator-scaling/) replaces $L^2\Lambda^2$ by nested commutator norms, [qDRIFT](/qdrift/) removes the dependence on $L$, and [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) brings $1/\epsilon$ down to $\log(1/\epsilon)$.

## Tightness

**The polynomial is not tight.** On the transverse-field Ising chain $H = \sum_{i=1}^{n-1} Z_i Z_{i+1} + \sum_{i=1}^{n} X_i$ (open chain, $L = 2n - 1$ terms, $\Lambda = 1$) at $t = 1$, the page's simulator computes the exact $e^{-iHt}$ by eigendecomposition and the first order product in the order of the terms (all $ZZ$ terms, then all $X$ terms). The table compares the true spectral norm error at $r = 64$ with the bounds, and the number of steps for $\epsilon = 10^{-3}$. The true error halves when $r$ doubles from 16 to 32 to 64 (ratios 2.00 to 2.01), so the "measured" column scales the error at $r = 64$ as $1/r$.

| $n$ | $L$ | error at $r = 64$ | $r$ measured | $r$ commutator bound | $r$ Lloyd bound |
|---|---|---|---|---|---|
| 3 | 5 | 0.01722 | about 1 100 | 4 000 | 10 000 |
| 4 | 7 | 0.02159 | about 1 400 | 6 000 | 21 000 |
| 5 | 9 | 0.02738 | about 1 750 | 8 000 | 36 000 |

The commutator bound is the first sum of the Lie-Trotter corollary, $\sum_j \|[H_j, T_{j+1}]\| = 4(n-1)$. The Lloyd bound is $L(L-1)\Lambda^2 t^2/(2\epsilon)$. The true count grows about linearly in $n$, the commutator bound linearly with a larger constant, and the Lloyd bound quadratically.

**What is known to be tight.**

- *Time.* A cost linear in $t$ is necessary: by the [no-fast-forwarding theorem](/no-fast-forwarding-theorem/), no method simulates all sparse Hamiltonians for time $t$ with $o(t)$ queries. The $t^2$ of the theorem is an artifact of the first order formula.
- *Error.* The $1/\epsilon$ is an artifact too. Methods built on [linear combination of unitaries](/linear-combination-of-unitaries/) and [qubitization](/qubitization/) reach a cost with an additive $\log(1/\epsilon)$ term.
- *Locality is needed.* A general Hamiltonian on $n$ qubits, with no local structure, needs an exponential number of gates for most $t$: there are not enough circuits of polynomial size to come close to all unitaries (the counting argument on the [Hamiltonian simulation](/hamiltonian-simulation/) page). So the hypothesis that each term acts on $O(1)$ qubits, or another structure such as sparsity, cannot be dropped.
- *Lattices.* For nearest-neighbor lattices the gate count of a $p$-th order formula is $O((nt)^{1+1/p}/\epsilon^{1/p})$ by the commutator bounds of Childs, Su, Tran, Wiebe and Zhu (2021). For large $p$ this is close to the $nt$ gates that any method needs to touch every site for the whole time.

## History

Feynman (1982) asked whether a universal quantum simulator exists, a quantum machine that can imitate every quantum system of a given size with resources that grow only polynomially, and conjectured that it does for systems with local interactions. Lloyd (1996) proved it for Hamiltonians that are sums of local terms, by the product formula and the universality of local gates, and observed that the count is small when each term overlaps few others. Abrams and Lloyd (1997) applied the method to systems of fermions. Aharonov and Ta-Shma (2003) moved from local to sparse Hamiltonians given by an oracle (see [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/)), and Berry, Ahokas, Cleve and Sanders (2007) gave higher order product formulas with cost close to linear in $t$, together with the lower bound that rules out fast forwarding. The modern bounds with commutators are due to Childs, Su, Tran, Wiebe and Zhu (2021).

## References
