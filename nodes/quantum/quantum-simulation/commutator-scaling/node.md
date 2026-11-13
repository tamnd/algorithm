---
tag: M322J4
kind: concept
slug: commutator-scaling
name: Commutator scaling
aliases:
- nested commutator bounds
area: quantum/quantum-simulation
level: advanced
summary: "The error of a p-th order product formula is O(a t^(p+1)/r^p), where a is a sum of norms of nested commutators of the terms. For local lattice models a grows like n, not like a power of the norm."
prereqs: [trotter-suzuki-product-formulas, higher-order-trotter-suzuki]
see_also: [lie-trotter-product-formula, trotter-suzuki-product-formulas, higher-order-trotter-suzuki, lieb-robinson-bound, qdrift, multi-product-formulas, quantum-many-body-simulation, universal-quantum-simulator]
sources:
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: Theorem 11 and Corollary 12 (error and step count with nested commutators), Propositions 15 and 16 (first and second order constants), and the applications to lattice Hamiltonians
  - paper: doi:10.1007/s00220-006-0150-x
    title: Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)
    locator: Lemma 1 (an error bound of order 2k with norms of the terms only)
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the gate count, and its smaller value when each term overlaps only a few other terms
---

Commutator scaling is the fact that the error of a product formula depends on the commutators of the Hamiltonian's terms, not only on their norms. If $H = H_1 + \cdots + H_L$ and the terms commute, the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) are exact. When they do not commute, the error of a formula of order $p$ with $r$ steps is at most a constant times $\tilde\alpha_{\mathrm{comm}}\, t^{p+1}/r^p$, where $\tilde\alpha_{\mathrm{comm}}$ is a sum of norms of nested commutators of depth $p + 1$. This was proved for every order by Childs, Su, Tran, Wiebe and Zhu (2021). The difference matters most for local Hamiltonians: on a lattice of $n$ sites most pairs of terms act on disjoint qubits, so $\tilde\alpha_{\mathrm{comm}}$ grows like $n$, while a bound with norms grows like $n^{p+1}$. Commutator scaling is the reason why product formulas are close to optimal for lattice models.

## In plain words

A product formula applies the parts of a Hamiltonian one after another instead of all at once. The error comes only from the parts that disturb each other, that is, from pairs that do not commute. In a large lattice of spins, each part touches a few neighboring spins, and two parts far apart do not disturb each other at all. So the error grows with the number of neighboring pairs, which is about the size of the system, and not with the square or a higher power of the size. Old error bounds counted every pair as if it disturbed every other one, and so they asked for far more steps than needed. Bounds that count only the disturbing pairs are close to the true error.

## The idea

**Where the error comes from.** For two terms, the Baker-Campbell-Hausdorff expansion gives $e^{-iA\delta}e^{-iB\delta} = e^{-i(A+B)\delta - \frac{\delta^2}{2}[A, B] + O(\delta^3)}$, and every correction term is a nested commutator of $A$ and $B$. The symmetric second order step cancels the term with one commutator, and the formulas of order $p$ cancel all terms with fewer than $p$ commutators. So the leading error of a formula of order $p$ is a combination of commutators with $p + 1$ terms.

**The bounds.** For terms $H_1, \ldots, H_L$ and a formula of order $p$, define
$$\tilde\alpha_{\mathrm{comm}} = \sum_{\gamma_1, \ldots, \gamma_{p+1} = 1}^{L} \big\| [H_{\gamma_{p+1}}, \cdots [H_{\gamma_3}, [H_{\gamma_2}, H_{\gamma_1}]] \cdots ] \big\|.$$
Theorem 11 of Childs, Su, Tran, Wiebe and Zhu (2021) bounds the error of one step of length $\delta$ by $O(\tilde\alpha_{\mathrm{comm}}\delta^{p+1})$, and their Corollary 12 gives the step count
$$r = O\!\left( \frac{\tilde\alpha_{\mathrm{comm}}^{1/p}\, t^{1+1/p}}{\epsilon^{1/p}} \right)$$
for error $\epsilon$ in the spectral norm. The constant in the $O$ depends on $p$ and on the number of stages of the formula. For the first and second order formulas the constants are explicit and small:
$$\|S_1(t/r)^r - e^{-iHt}\| \le \frac{t^2}{2r}\sum_{j=1}^{L-1}\|[H_j, T_{j+1}]\|, \qquad \|S_2(t/r)^r - e^{-iHt}\| \le \frac{t^3}{r^2}\sum_{j=1}^{L-1}\left(\frac{\|[T_{j+1}, [T_{j+1}, H_j]]\|}{12} + \frac{\|[H_j, [H_j, T_{j+1}]]\|}{24}\right),$$
with $T_{j+1} = H_{j+1} + \cdots + H_L$ (Propositions 15 and 16 of the same paper; proofs on the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) page).

**Against norm bounds.** Since $\|[A, B]\| \le 2\|A\|\|B\|$, every nested commutator of depth $p + 1$ has norm at most $2^p$ times the product of the norms, so $\tilde\alpha_{\mathrm{comm}} \le 2^p\lambda^{p+1}$ with $\lambda = \sum_j \|H_j\|$. This is the kind of bound used by Lloyd (1996) and by Berry, Ahokas, Cleve and Sanders (2007). The commutator bound is never worse up to the constant, and it is much better when many pairs commute.

**Why local Hamiltonians gain.** Let each $H_j$ act on a few neighboring sites of a lattice with $n$ sites, with $\|H_j\| \le 1$. A nested commutator $[H_{\gamma_{p+1}}, \cdots [H_{\gamma_2}, H_{\gamma_1}]]$ is zero unless each new term overlaps the support of the commutator so far. For a fixed first term $\gamma_1$ the number of such chains is a constant that depends on $p$ and on the lattice, not on $n$. So $\tilde\alpha_{\mathrm{comm}} = O(n)$, while $\lambda^{p+1} = \Theta(n^{p+1})$. Then $r = O(n^{1/p}t^{1+1/p}/\epsilon^{1/p})$ steps of $O(n)$ exponentials each give $O((nt)^{1+1/p}/\epsilon^{1/p})$ gates. For large $p$ this approaches $nt$, the size of the space-time volume, which any method needs up to small factors. With norm bounds the same formula needs $O(n^{2+1/p}t^{1+1/p}/\epsilon^{1/p})$ gates.

## Examples

**Two qubits by hand.** For $H = ZZ + 0.8\,XI + 0.8\,IX$, the only non-commuting pairs are $ZZ$ with $XI$ and $ZZ$ with $IX$. With $H_1 = ZZ$ and $T_2 = 0.8(XI + IX)$, $[H_1, T_2] = 1.6i(YZ + ZY)$ has norm 3.2, so the first order constant is 3.2; the norm bound $\sum_{j \ne k}\|H_j\|\|H_k\|$ is $2(0.8 + 0.8 + 0.64) = 4.48$. The double commutators are $[T_2, [T_2, H_1]] = 5.12(ZZ - YY)$ and $[H_1, [H_1, T_2]] = 3.2(XI + IX)$, so the second order constant is $10.24/12 + 6.4/24 = 1.12$. The exact errors are about half of these bounds (see the table on the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) page).

**The transverse-field Ising chain.** $H = \sum_{i=1}^{n-1} Z_iZ_{i+1} + \sum_{i=1}^{n} X_i$ on an open chain has $L = 2n - 1$ terms of norm 1. The terms are listed as all $ZZ$ terms, then all $X$ terms. Each $Z_iZ_{i+1}$ anticommutes with $X_i$ and $X_{i+1}$ and commutes with every other term, so there are $2(n - 1)$ anticommuting pairs and the first order constant is $\alpha_1 = 4(n - 1)$. A norm bound counts all $L(L - 1)$ ordered pairs and gives $L^2 - L$. The page's simulator computes the exact $e^{-iHt}$ by eigendecomposition and the spectral norm of the error at $t = 1$ and $r = 16$:

| $n$ | first order error | commutator bound | norm bound | $\beta_2$ | second order error | commutator bound | norm bound |
|---|---|---|---|---|---|---|---|
| 3 | 0.06926 | 0.25 | 0.625 | 3.412 | 0.003332 | 0.01333 | 0.04557 |
| 4 | 0.08652 | 0.375 | 1.3125 | 5.157 | 0.004451 | 0.02015 | 0.1322 |
| 5 | 0.1102 | 0.5 | 2.25 | 6.903 | 0.005943 | 0.02696 | 0.2891 |

The second order norm bound replaces each double commutator by $4$ times the product of the norms, with $\|T_{j+1}\| \le L - j$. The commutator constants grow linearly in $n$ ($\beta_2$ grows by 1.745 per site), the true errors grow linearly too, and the norm bounds grow quadratically (first order) and cubically (second order). For larger chains the simulator applies the circuit to a random state (seed 1) and compares with a long Taylor series of $e^{-iHt}$ applied to the same state: at $r = 16$ the first order errors for $n = 4, 6, 8, 10$ are 0.0404, 0.0750, 0.0857, 0.0936 and the second order errors are 0.00240, 0.00382, 0.00429, 0.00454, while the first order commutator bounds are 0.375, 0.625, 0.875, 1.125.

**What it buys.** For $n = 10$, $t = 1$ and $\epsilon = 10^{-3}$, the first order formula needs $r = 18\,000$ steps by the commutator bound and $r = 171\,000$ by the norm bound. A random method such as [qDRIFT](/qdrift/), whose cost depends on $\lambda^2 = 361$ and not on commutators, needs $722\,000$ exponentials for the same $\epsilon$ (in the diamond norm), against the $342\,000$ of the first order formula.

**Commuting groups.** If the terms are grouped into sets of mutually commuting strings, $H = G_1 + \cdots + G_m$, each $e^{-iG_a\delta}$ is a product of exponentials with no error, and the bounds apply to the groups. For the Ising chain, $m = 2$: $G_1$ holds all $ZZ$ terms and $G_2$ all $X$ terms. The commutator $[G_1, G_2]$ is still a sum of $2(n - 1)$ local strings, so grouping changes the circuit but not the scaling of the error.

**Order of the terms.** The first order constant $\sum_j \|[H_j, T_{j+1}]\|$ depends on the order of the terms, and so does the true error. Placing terms that do not commute next to each other in the list does not change the sum of pairwise commutators, but it can change the norms of the partial sums $T_{j+1}$.

## Where it is used

- **Resource estimates for lattice models.** Estimates of the gate count for simulating the Heisenberg, Ising and Hubbard models on early fault-tolerant machines use commutator bounds, often computed numerically for small sizes and extrapolated. They show that fourth order product formulas are competitive with methods based on a [block encoding](/block-encoding/) for these models.
- **Choice of method.** For a Hamiltonian with $L$ terms and small commutators, product formulas with commutator bounds can beat [qDRIFT](/qdrift/), whose cost is set by $\lambda = \sum_j \|H_j\|$ alone. For a Hamiltonian with very many small terms that do not commute, as in quantum chemistry, $\lambda$ can be the better measure.
- **Locality of errors.** The commutator structure is the same structure that gives [Lieb-Robinson bounds](/lieb-robinson-bound/): the error from a local term spreads only through chains of overlapping terms. Errors of local observables can therefore be bounded by sums over a light cone, which is smaller than the whole system for short times.
- **Higher orders.** The [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) formulas with commutator bounds reach $O((nt)^{1+1/p}/\epsilon^{1/p})$ gates on lattices. [Multi-product formulas](/multi-product-formulas/) also have error terms built from nested commutators.
- **Other bounds of the same kind.** Bounds that also depend on the input state, for example on its energy or on the number of particles, refine the commutator bounds further when the simulated state is known to lie in a small subspace.

## References
