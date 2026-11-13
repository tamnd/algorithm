---
tag: V676X9
kind: theorem
slug: lie-trotter-product-formula
name: Lie-Trotter product formula
aliases:
- Lie product formula
- Trotter product formula
area: quantum/quantum-simulation
level: core
summary: "e^(A+B) is the limit of (e^(A/r) e^(B/r))^r as r grows. For Hermitian A and B, r steps approximate e^(-i(A+B)t) with error at most t^2 ||[A, B]|| / (2r)."
prereqs: [matrix-norms, unitary-operator]
see_also: [operator-splitting, trotter-suzuki-product-formulas, higher-order-trotter-suzuki, commutator-scaling, hamiltonian-simulation, universal-quantum-simulator, exponential-integrators, symplectic-integrators]
sources:
  - paper: doi:10.1090/S0002-9939-1959-0108732-6
    title: H. F. Trotter, On the product of semi-groups of operators, Proceedings of the American Mathematical Society 10(4), 1959, pages 545 to 551
    locator: the product formula for semigroups of operators on a Banach space
  - book: isbn:9783319134666
    title: Brian C. Hall, Lie Groups, Lie Algebras, and Representations, An Elementary Introduction, second edition, Graduate Texts in Mathematics 222, Springer, 2015
    locator: Chapter 2 (the matrix exponential), the Lie product formula and its proof
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: Proposition 15 (the first order error bound with commutators of the terms)
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the use of the product formula to simulate sums of local Hamiltonians
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.7 (simulation of quantum systems), the Trotter formula and its first and second order forms
---

The Lie-Trotter product formula says that the exponential of a sum of two matrices is the limit of products of the separate exponentials over many small steps: $e^{A+B} = \lim_{r\to\infty} (e^{A/r} e^{B/r})^r$. In quantum computing it is used in the form $e^{-i(A+B)t} \approx (e^{-iAt/r} e^{-iBt/r})^r$ for Hermitian $A$ and $B$, with an error at most $t^2 \|[A,B]\|/(2r)$ in the spectral norm. This is the reason why a quantum computer can simulate a Hamiltonian that is a sum of simple terms, which is the content of the [universal quantum simulator](/universal-quantum-simulator/) theorem. This page is the limit theorem and its first order error bound. The family of algorithms built on it is on the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) page, and the recursive construction of higher orders is on the [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) page. The numerical page [operator splitting](/operator-splitting/) uses the same idea, under the name Lie-Trotter splitting, to split the right-hand side of a differential equation; that page is about the order of accuracy of ODE integrators, and this page is about unitary evolution, errors in the operator norm and gate counts.

## Statement

Let $\|\cdot\|$ be the spectral norm, or any submultiplicative matrix norm with $\|I\| = 1$ (see [matrix norms](/matrix-norms/)). Let $[A, B] = AB - BA$.

**Theorem 1 (Lie product formula).** For all complex $d \times d$ matrices $A$ and $B$ and every integer $r \ge 1$,
$$\Big\| \big(e^{A/r} e^{B/r}\big)^r - e^{A+B} \Big\| \le \frac{s^2 e^s}{r}, \qquad s = \|A\| + \|B\|.$$
In particular $(e^{A/r} e^{B/r})^r \to e^{A+B}$ as $r \to \infty$.

**Theorem 2 (the quantum form).** Let $A$ and $B$ be Hermitian, $t \ge 0$ and $r \ge 1$. Then
$$\Big\| \big(e^{-iAt/r} e^{-iBt/r}\big)^r - e^{-i(A+B)t} \Big\| \le \frac{t^2}{2r}\, \|[A, B]\|$$
in the spectral norm. The same bound holds with the two factors in the other order.

**Corollary (many terms).** Let $H = H_1 + \cdots + H_L$ with Hermitian $H_j$, and let $T_{j+1} = H_{j+1} + \cdots + H_L$. For the product $S(\tau) = e^{-iH_1\tau} e^{-iH_2\tau} \cdots e^{-iH_L\tau}$, or the same product in the reverse order,
$$\| S(t/r)^r - e^{-iHt} \| \le \frac{t^2}{2r} \sum_{j=1}^{L-1} \|[H_j, T_{j+1}]\| \le \frac{t^2}{2r} \sum_{1 \le j < k \le L} \|[H_j, H_k]\|.$$

The bounds of Theorem 2 and the corollary are the first order case of the commutator bounds of Childs, Su, Tran, Wiebe and Zhu (2021). Theorem 1 holds for all matrices, but its constant uses only norms. Theorem 2 needs Hermitian $A$ and $B$, so that each exponential is a [unitary operator](/unitary-operator/) of norm 1, and its constant is a commutator: when $A$ and $B$ commute, the error is zero.

## In plain words

Two forces act on a system at the same time. You can only apply one at a time. So you apply the first one for a short moment, then the second one for a short moment, and you do this again and again. Each pair of moments gives almost the same change as the two forces together. The small mistake in each pair comes from the fact that the order matters: the first force changes the system before the second one acts.

If you cut the time into more and more pieces, each mistake gets much smaller, faster than the number of mistakes grows. So the total mistake goes down in proportion to the number of pieces. If the order of the two forces does not matter at all, there is no mistake, even with one piece.

## Proof

**Proof of Theorem 1.** Let $X = A/r$, $Y = B/r$ and $u = (\|A\| + \|B\|)/r = s/r$. Write $P = e^X e^Y$ and $Q = e^{X+Y}$.

*One step.* Expand both exponentials as power series. In $e^X e^Y = \sum_{a, b \ge 0} X^a Y^b/(a!\,b!)$, the terms of total degree 0 and 1 are $I + X + Y$, the same as in $e^{X+Y} = \sum_m (X+Y)^m/m!$. The terms of degree $m$ of $e^X e^Y$ have norm at most $\sum_{a+b=m} \|X\|^a \|Y\|^b/(a!\,b!) = (\|X\|+\|Y\|)^m/m! = u^m/m!$, by the binomial theorem. The term of degree $m$ of $e^{X+Y}$ has norm at most $u^m/m!$. So
$$\|P - Q\| \le 2 \sum_{m \ge 2} \frac{u^m}{m!} = u^2 \sum_{m \ge 0} \frac{2}{(m+2)!} u^m \le u^2 \sum_{m \ge 0} \frac{u^m}{m!} = u^2 e^u,$$
since $(m+2)(m+1) \ge 2$.

*Many steps.* The identity $P^r - Q^r = \sum_{k=0}^{r-1} P^k (P - Q) Q^{r-1-k}$ holds for all matrices; it telescopes. Each factor has $\|P\| \le e^{\|X\|} e^{\|Y\|} = e^u$ and $\|Q\| \le e^u$. So
$$\|P^r - Q^r\| \le r \, e^{(r-1)u} \, u^2 e^u = r \cdot \frac{s^2}{r^2} e^{s} = \frac{s^2 e^s}{r}. \qquad \square$$

**Proof of Theorem 2.** Let $H = A + B$, $U(\tau) = e^{-iH\tau}$ and $S(\tau) = e^{-iA\tau} e^{-iB\tau}$.

*One step.* Differentiate $S$:
$$S'(\tau) = -iA\, S(\tau) - i e^{-iA\tau} B e^{-iB\tau} = -iH\, S(\tau) + E(\tau), \qquad E(\tau) = -i\,[e^{-iA\tau}, B]\, e^{-iB\tau}.$$
Then $\frac{d}{d\sigma}\big( U(\tau - \sigma) S(\sigma) \big) = U(\tau - \sigma)\big(iH S(\sigma) + S'(\sigma)\big) = U(\tau-\sigma) E(\sigma)$. Integrate from $\sigma = 0$ to $\tau$:
$$S(\tau) - U(\tau) = \int_0^\tau U(\tau - \sigma)\, E(\sigma)\, d\sigma.$$
$U$ and $e^{-iB\sigma}$ are unitary, so $\|S(\tau) - U(\tau)\| \le \int_0^\tau \|[e^{-iA\sigma}, B]\|\, d\sigma$. Now $[e^{-iA\sigma}, B] = (f(\sigma) - f(0))\, e^{-iA\sigma}$ with $f(\rho) = e^{-iA\rho} B e^{iA\rho}$. Since $f'(\rho) = -i\, e^{-iA\rho} [A, B] e^{iA\rho}$ has norm $\|[A, B]\|$, we get $\|f(\sigma) - f(0)\| \le \sigma \|[A,B]\|$. So
$$\|S(\tau) - U(\tau)\| \le \int_0^\tau \sigma\, \|[A, B]\|\, d\sigma = \frac{\tau^2}{2} \|[A, B]\|.$$

*Many steps.* With $\tau = t/r$, the telescoping identity of Theorem 1 and $\|S\| = \|U\| = 1$ give $\|S(\tau)^r - U(\tau)^r\| \le r\, \|S(\tau) - U(\tau)\| \le \frac{t^2}{2r}\|[A, B]\|$, and $U(\tau)^r = e^{-iHt}$. For the other order, swap $A$ and $B$; $\|[B, A]\| = \|[A, B]\|$. $\square$

**Proof of the corollary.** By induction on $L$; the case $L = 1$ has no error. Let $S_{j}(\tau) = e^{-iH_j\tau} \cdots e^{-iH_L\tau}$. Then $S_j(\tau) = e^{-iH_j\tau} S_{j+1}(\tau)$, and
$$\|S_j(\tau) - e^{-i(H_j + T_{j+1})\tau}\| \le \|e^{-iH_j\tau}\| \, \|S_{j+1}(\tau) - e^{-iT_{j+1}\tau}\| + \|e^{-iH_j\tau} e^{-iT_{j+1}\tau} - e^{-i(H_j + T_{j+1})\tau}\|.$$
The first part is the induction hypothesis, and the second is at most $(\tau^2/2)\|[H_j, T_{j+1}]\|$ by the one-step bound. Summing gives $(\tau^2/2) \sum_j \|[H_j, T_{j+1}]\|$ for one step, and $r$ steps multiply it by $r$. The last inequality of the corollary is the triangle inequality $\|[H_j, T_{j+1}]\| \le \sum_{k > j} \|[H_j, H_k]\|$. The reverse order is the same argument with the factors in the other order. $\square$

## Consequences

- **The first order product formula.** To reach error $\epsilon$ for $H = A + B$, $r = \lceil t^2 \|[A,B]\|/(2\epsilon) \rceil$ steps are enough. With $L$ terms, each step has $L$ exponentials. This is the first order case of the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/).
- **Lloyd's theorem.** When each $H_j$ acts on $O(1)$ qubits, each exponential is a constant number of gates, and the corollary gives a circuit of $\mathrm{poly}(L, t, 1/\epsilon)$ gates. This is the [universal quantum simulator](/universal-quantum-simulator/) theorem.
- **Commuting terms are free.** If $[A, B] = 0$, then $e^{-iAt}e^{-iBt} = e^{-i(A+B)t}$ for every $t$, and one step is exact.
- **Commutators, not norms.** The constant is $\|[A, B]\|$, which can be much smaller than $2\|A\|\|B\|$. The constant from Theorem 1 uses only norms and grows as $e^s$, so it is useless for long times. The study of such bounds for higher orders is [commutator scaling](/commutator-scaling/).
- **The symmetric form.** The product $e^{-iAt/(2r)} e^{-iBt/r} e^{-iAt/(2r)}$, taken $r$ times, has error $O(t^3/r^2)$; it is the second order formula, also called the Strang splitting on the [operator splitting](/operator-splitting/) page. Its proof and constant are on the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/) page.
- **The Baker-Campbell-Hausdorff series.** For small $X$ and $Y$, $\log(e^X e^Y) = X + Y + \tfrac12 [X, Y] + \cdots$, with higher nested commutators. So the leading error of one step is $\tfrac12 [X, Y]$, which matches the constant of Theorem 2.

## Tightness

**A hand example.** Let $A = X$ and $B = Z$, the Pauli matrices (see [Pauli gates](/pauli-gates/)). Then $[X, Z] = -2iY$ and $\|[X, Z]\| = 2$, so Theorem 2 gives the bound $t^2/r$. For one step, the products can be done by hand with $ZX = iY$:
$$e^{-iZt} e^{-iXt} = \cos^2 t \; I - i \sin t \cos t \,(X + Z) - i \sin^2 t \; Y,$$
while $(X+Z)^2 = 2I$ gives
$$e^{-i(X+Z)t} = \cos(\sqrt2\, t)\, I - i \frac{\sin(\sqrt2\, t)}{\sqrt2}\,(X+Z).$$
For $t = 0.1$ the spectral norm of the difference is $9.978 \times 10^{-3}$, and the bound is $10^{-2}$. So for one short step the constant $\tfrac12\|[A,B]\|$ is tight.

**Many steps.** For $t = 1$, the exact spectral norm errors, from the page's simulator with exact $2 \times 2$ exponentials, are:

| $r$ | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| error | 0.7992 | 0.3624 | 0.1763 | 0.08751 | 0.04368 | 0.02183 |
| bound $1/r$ | 1 | 0.5 | 0.25 | 0.125 | 0.0625 | 0.03125 |
| $r \times$ error | 0.799 | 0.725 | 0.705 | 0.700 | 0.699 | 0.699 |

The error falls as $1/r$, so the order $1/r$ cannot be improved for this product. The limit of $r \times$ error is about $0.70 < 1$: over a long time the leading error is an average of the commutator as the state turns under $e^{-iHt}$, and parts of it cancel. Better orders in $r$ need other products, such as the symmetric form above.

**Norm bounds can be far off.** If $A = a X$ and $B = b Z$ with a large $a$ and a small $b$, then $\|[A, B]\| = 2ab$ while the bound of Theorem 1 grows as $(a+b)^2 e^{a+b}$. For Hermitian terms the commutator form is the right one.

## History

Sophus Lie used the formula for matrices in his theory of continuous groups in the 19th century, and it is often called the Lie product formula; Hall's book gives the matrix proof. H. F. Trotter (1959) proved it for semigroups of operators on a Banach space, which covers unbounded generators such as the Laplacian. Masuo Suzuki made it a tool of quantum statistical mechanics and built the higher-order formulas in 1990 and 1991. Seth Lloyd (1996) used it to prove that quantum computers simulate local Hamiltonians efficiently. The commutator form of the error bound with explicit constants for any number of terms is in Childs, Su, Tran, Wiebe and Zhu (2021).

## References
