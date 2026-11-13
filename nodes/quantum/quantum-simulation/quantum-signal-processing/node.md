---
tag: 9B38VZ
kind: technique
slug: quantum-signal-processing
name: Quantum signal processing
aliases:
- QSP
area: quantum/quantum-simulation
level: research
summary: "Interleave d copies of a one-qubit signal rotation W(x) with d + 1 Z rotations. The top-left entry becomes a degree-d polynomial in x, and every bounded polynomial of the right parity is reachable."
prereqs: [chebyshev-polynomials, unitary-operator]
see_also: [qubitization, quantum-eigenvalue-transformation, block-encoding, optimal-hamiltonian-simulation, chebyshev-series, minimax-approximation, polynomial-method, fixed-point-quantum-search]
sources:
  - paper: doi:10.1103/PhysRevX.6.041067
    title: "Guang Hao Low, Theodore J. Yoder and Isaac L. Chuang, Methodology of resonant equiangular composite quantum gates, Physical Review X 6(4), 2016, article 041067 (arXiv:1603.03996)"
    locator: "the characterization of the single-qubit polynomials that a sequence of phased rotations can make"
  - paper: doi:10.1103/PhysRevLett.118.010501
    title: "Guang Hao Low and Isaac L. Chuang, Optimal Hamiltonian simulation by quantum signal processing, Physical Review Letters 118(1), 2017, article 010501 (arXiv:1606.02685)"
    locator: "the name quantum signal processing and its use for Hamiltonian simulation"
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM STOC, 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1, Section 3: Theorem 3 (the characterization), Theorem 4 (one polynomial alone), Theorem 5 (real parts), Corollary 8 (the reflection convention), Lemma 9 (Chebyshev phases) and Corollary 10 (real quantum signal processing)"
  - paper: doi:10.1103/PhysRevA.103.042419
    title: "Yulong Dong, Xiang Meng, K. Birgitta Whaley and Lin Lin, Efficient phase-factor evaluation in quantum signal processing, Physical Review A 103(4), 2021, article 042419 (arXiv:2002.11649)"
    locator: "Theorem 2 (symmetric phase factors), the Chebyshev nodes of the objective function, and the initial guess of equation (27)"
  - paper: doi:10.1103/PRXQuantum.2.040203
    title: "John M. Martyn, Zane M. Rossi, Andrew K. Tan and Isaac L. Chuang, Grand unification of quantum algorithms, PRX Quantum 2(4), 2021, article 040203 (arXiv:2105.02859)"
    locator: "the tutorial on the conventions of quantum signal processing and its use for search, simulation and linear systems"
---

*Quantum signal processing* (QSP) is a statement about one qubit. Take the *signal rotation*
$$W(x) = \begin{pmatrix} x & i\sqrt{1-x^2} \\ i\sqrt{1-x^2} & x \end{pmatrix} = e^{i \arccos(x) X}, \qquad x \in [-1, 1],$$
and interleave $d$ copies of it with $d + 1$ rotations about $Z$:
$$U_\Phi(x) = e^{i\phi_0 Z}\, W(x)\, e^{i\phi_1 Z}\, W(x) \cdots W(x)\, e^{i\phi_d Z}.$$
The entry $P(x) = \langle 0|U_\Phi(x)|0\rangle$ is a polynomial of degree at most $d$ in $x$. Low, Yoder and Chuang (2016) showed which polynomials occur, and Gilyén, Su, Low and Wiebe (2019, Theorem 3) gave a short proof: every complex $P$ of parity $d \bmod 2$ with a partner $Q$ such that $|P|^2 + (1-x^2)|Q|^2 = 1$. For the real part the condition is only $|\mathrm{Re}\,P| \le 1$ on $[-1, 1]$. The phases $\Phi$ do not depend on $x$, so the same circuit computes $P(x)$ for every signal value at once. This page is the one-qubit core. A [block encoding](/block-encoding/) gives a matrix in place of $x$, [qubitization](/qubitization/) turns its walk operator into many copies of $W(x)$, one for each eigenvalue, and the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) is the result: $p(H/\alpha)$ with $d$ queries.

## In plain words

A single qubit can be turned by a fixed but unknown amount, and we cannot look at that amount directly. Between the unknown turns we insert turns of our own about a different axis, chosen in advance. The final state of the qubit then depends on the unknown amount in a way that we design. With a few unknown turns, the chance to find the qubit in its start state can follow almost any smooth curve we want, within simple limits: the curve must be even or odd, stay between minus one and one, and bend no more often than the number of turns allows. The work of choosing our own turns is done once, on a classical computer. The same sequence then works for every value of the unknown amount, which is what makes it useful for matrices with many eigenvalues.

## When it applies

- The input is a one-qubit unitary that depends on an unknown $x$ in the form $W(x)$, or a larger operator that splits into such two-dimensional blocks, as the walk operator of [qubitization](/qubitization/) does.
- The target is a function $f$ on $[-1, 1]$ that a polynomial of degree $d$ approximates well, with $|f| \le 1$ and a definite parity. If $f$ has no parity, split it into its even and odd parts and add them with a [linear combination of unitaries](/linear-combination-of-unitaries/).
- The cost of interest is the number $d$ of signal calls. It equals the degree of the polynomial, so the query count is the approximation degree of $f$, which [Chebyshev series](/chebyshev-series/) and [minimax approximation](/minimax-approximation/) estimate.

## The template

**The characterization** (Gilyén, Su, Low and Wiebe, Theorem 3). There are phases $\Phi \in \mathbb{R}^{d+1}$ with
$$U_\Phi(x) = \begin{pmatrix} P(x) & iQ(x)\sqrt{1-x^2} \\ iQ^*(x)\sqrt{1-x^2} & P^*(x) \end{pmatrix} \quad \text{for all } x \in [-1, 1]$$
if and only if the polynomials $P, Q \in \mathbb{C}[x]$ satisfy
1. $\deg P \le d$ and $\deg Q \le d - 1$,
2. $P$ has parity $d \bmod 2$ and $Q$ has parity $(d-1) \bmod 2$,
3. $|P(x)|^2 + (1 - x^2)|Q(x)|^2 = 1$ for all $x \in [-1, 1]$.

The forward direction is an induction on $d$: multiplying by $W(x)e^{i\phi Z}$ raises each degree by one and flips each parity, and unitarity gives property 3. For the converse, if $\deg P = d$, the leading coefficients of $P$ and $Q$ fix a phase $\phi_d$ such that $U_\Phi\,(W(x)e^{i\phi_d Z})^{-1}$ has degrees $d - 1$ and $d - 2$, so one rotation can be peeled off at a time.

**Real targets** (Theorem 5 and Corollary 10). For a real polynomial $f$ of degree at most $d$ and parity $d \bmod 2$, there are phases with $\mathrm{Re}\,P = f$ if and only if $|f(x)| \le 1$ on $[-1, 1]$. The imaginary part of $P$ and the polynomial $Q$ are then free, and need not be computed. With the pair of sequences $\Phi$ and $-\Phi$ the real part is easy to use, because $\langle 0|U_{-\Phi}(x)|0\rangle = P^*(x)$, so their average has $\mathrm{Re}\,P$ in the corner.

**Finding the phases.** The phases come from a classical computation. The method below follows Dong, Meng, Whaley and Lin (2021): it looks only for *symmetric* phases, $\phi_j = \phi_{d-j}$, and starts from $\Phi = (\pi/4, 0, \ldots, 0, \pi/4)$, where $P = iT_d$ and so $\mathrm{Re}\,P = 0$. A symmetric $\Phi$ has $m = \lfloor d/2\rfloor + 1$ free values, and $\mathrm{Re}\,P$ has exactly $m$ coefficients of the right parity, so $m$ sample points give a square system. Dong and coauthors minimize the error with a quasi-Newton method; the code here uses Newton's method with a step that halves until the error falls.

```pseudo id=main
QSP-PHASES(f, d)
L1  m ← ⌊d/2⌋ + 1;  x_k ← cos((2k - 1)π/(4m)) for k = 1..m    ▷ positive Chebyshev nodes
L2  ψ ← (0, ..., 0) ∈ R^m
L3  Φ(ψ) ← (ψ_0 + π/4, ψ_1, ψ_2, ..., ψ_2, ψ_1, ψ_0 + π/4) ∈ R^(d+1)    ▷ symmetric
L4  repeat:  r_k ← Re <0|U_Φ(ψ)(x_k)|0> - f(x_k)  for k = 1..m
L5      if max_k |r_k| ≤ tol: go to L7
L6      ψ ← ψ - t J(ψ)^(-1) r,  J_kj = ∂r_k/∂ψ_j,  t ∈ {1, 1/2, 1/4, ...} so that max|r| falls
L7  return Φ(ψ)    ▷ the circuit is e^(iφ_0 Z) W(x) e^(iφ_1 Z) ... W(x) e^(iφ_d Z)
```

**Why the samples suffice.** $\mathrm{Re}\,P$ and $f$ are both polynomials of degree at most $d$ and parity $d \bmod 2$. Such a polynomial is fixed by its values at $m$ distinct positive points, so if $r_k = 0$ for all $k$, then $\mathrm{Re}\,P = f$ on the whole interval. The derivatives in $J$ come from prefix and suffix products of the sequence: $\partial U_\Phi/\partial\phi_j$ inserts $iZ$ after the $j$-th rotation. Each Newton step costs $O(d^2)$ arithmetic operations on $2 \times 2$ matrices, plus solving the $m \times m$ system.

**Cost on the quantum side.** One run uses $d$ calls to the signal and $d + 1$ rotations. The degree is all that matters: to approximate $f$ to error $\epsilon$ in the [Chebyshev](/chebyshev-polynomials/) sense one needs the least $d$ with $\min_{\deg p \le d}\max_x|f - p| \le \epsilon$, which the [Jackson theorem](/jackson-theorem/) bounds for smooth $f$.

**Example: degree 1 by hand.** For $f(x) = x/2$, the symmetric phases are $\Phi = (\phi, \phi)$, and $P(x) = e^{i\phi}\,x\,e^{i\phi} = e^{2i\phi}x$. So $\mathrm{Re}\,P = x\cos 2\phi = x/2$ gives $\phi = \pi/6$, and $P(x) = e^{i\pi/3}x$. The solver finds exactly $(\pi/6, \pi/6) = (0.5236, 0.5236)$.

**Example: degree 3.** For $f(x) = (x^3 + x)/4$, which has $\max|f| = 1/2$, the solver returns $\Phi = (0.7524, -0.2288, -0.2288, 0.7524)$. At $x = 0.7$, $\mathrm{Re}\,P = 0.26075 = f(0.7)$ while $\mathrm{Im}\,P = -0.7454$. The tests in `impl/python` check these phases, check random targets of degree 2, 3, 5, 8 and 11 on a grid of 201 points, and check the three properties of the characterization for random phases.

## Classic examples

- **Chebyshev polynomials.** With all phases zero, $W(x)^d = e^{id\arccos(x)X}$, so $P = T_d(x)$ and $Q = U_{d-1}(x)$, the [Chebyshev polynomials](/chebyshev-polynomials/) of the first and second kind. In the reflection convention below, Lemma 9 gives $\phi_1 = (1-d)\pi/2$ and $\phi_j = \pi/2$ for $j \ge 2$.
- **Amplitude amplification.** With $x = \sin\theta$ the good amplitude, $\ell$ rounds of [amplitude amplification](/amplitude-amplification/) give $\sin((2\ell+1)\theta) = (-1)^\ell T_{2\ell+1}(\sin\theta)$. Other phases give polynomials that stay near 1 for every $\theta$ above a threshold, which is [fixed-point quantum search](/fixed-point-quantum-search/).
- **Hamiltonian simulation.** The Jacobi-Anger expansion writes $\cos(\tau x)$ and $\sin(\tau x)$ as Chebyshev series with Bessel function coefficients. Truncating at a degree of order $\tau + \log(1/\epsilon)$ and running QSP on each eigenvalue of $H/\alpha$, through qubitization, gives $e^{-iHt}$ with $\tau = \alpha t$. See [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/).
- **Matrix inversion and thresholds.** An odd polynomial close to $1/(\kappa x)$ away from 0 gives linear systems, and a polynomial close to the sign function gives eigenvalue thresholds. See the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/).

## Variations

- **The reflection convention** (Corollary 8). With $R(x) = \begin{pmatrix} x & \sqrt{1-x^2} \\ \sqrt{1-x^2} & -x\end{pmatrix}$, which is the form a [block encoding](/block-encoding/) takes on a two-dimensional subspace, the sequence $e^{i\psi_0 Z}\prod_j R(x)e^{i\psi_j Z}$ equals $(-i)^d U_\Phi(x)$ when $\psi_0 = \phi_0 - \pi/4$, $\psi_d = \phi_d - \pi/4$ and $\psi_j = \phi_j - \pi/2$ in between, because $R(x) = -i\,e^{i\pi Z/4}W(x)e^{i\pi Z/4}$. Other papers swap the roles of $X$ and $Z$. All conventions differ by fixed one-qubit gates, but phases from one convention are wrong in another.
- **One polynomial alone** (Theorem 4). A complex $P$ has a partner $Q$ if and only if $|P| \le 1$ on $[-1, 1]$, $|P| \ge 1$ outside it, and, for even $d$, $P(ix)P^*(ix) \ge 1$ on the real line. Finding $Q$ needs the roots of $1 - |P|^2$, which is the original route to the phases. It needs high precision for large $d$, and optimization avoids it.
- **Other phase solvers.** Besides root finding and optimization, there are methods by layer stripping, and by fast Fourier transforms on the unit circle. They differ in numerical stability for degrees in the thousands.
- **Matrices.** If $x$ is replaced by a Hermitian $A$ with $\|A\| \le 1$, the same polynomial acts on each eigenvalue. This is the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/). For a non-square or non-Hermitian $A$ it acts on singular values, which is the singular value transformation of Gilyén, Su, Low and Wiebe.

## Pitfalls

- **Parity.** A single QSP sequence gives only polynomials of parity $d \bmod 2$. A target such as $e^{-i\tau x}$ has no parity and must be split into $\cos(\tau x)$ and $-i\sin(\tau x)$.
- **The bound $|f| \le 1$.** If $f$ reaches $\pm 1$, Newton's method becomes ill conditioned near those points. Scale the target to $\max|f| \le 1 - \delta$ and pay for it with a factor in the success probability, or use amplitude amplification afterwards.
- **Conventions.** The order of the phases, the axis of the signal ($X$ or $Z$), $W$ against $R$ and the extra $\pi/4$ at the ends all change the phases. Test a phase list in the exact circuit that will use it, for example on $f = T_d$.
- **The real part, not the entry.** The method controls $\mathrm{Re}\,P$. The entry $P$ itself has an imaginary part that is not small. A circuit that uses $P$ without the $\pm\Phi$ average, or without a measurement that picks the real part, gets the wrong function.
- **Degree is the cost.** A high-degree polynomial with large coefficients in the monomial basis may still be fine for QSP, but an approximation that does not converge in the Chebyshev sense, such as a Taylor series far from its center, needs a much larger degree.

## Exercises

1. Show by induction that $\langle 0|W(x)^d|0\rangle = T_d(x)$ and that the top-right entry is $i\sqrt{1-x^2}\,U_{d-1}(x)$.
2. Find all phase pairs $(\phi_0, \phi_1)$ with $\mathrm{Re}\,P(x) = x/2$. Which of them are symmetric?
3. Prove that for $\Phi = (\pi/4, 0, \ldots, 0, \pi/4)$ the polynomials are $P = iT_d$ and $Q = U_{d-1}$, so $\mathrm{Re}\,P = 0$.
4. Show that $\langle 0|U_{-\Phi}(x)|0\rangle = P^*(x)$. Hint: complex conjugation maps $e^{i\phi Z}$ to $e^{-i\phi Z}$ and $W(x)$ to $W(x)^{-1} = ZW(x)Z$, and $Z$ commutes with every $e^{i\phi Z}$.
5. Check the identity $R(x) = -i\,e^{i\pi Z/4}W(x)e^{i\pi Z/4}$, and use it to convert $\Phi = (\pi/6, \pi/6)$ to the reflection convention.

## References
