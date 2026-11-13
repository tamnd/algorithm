---
tag: 6TMH0A
kind: technique
slug: quantum-eigenvalue-transformation
name: Quantum eigenvalue transformation
aliases:
- QET
- quantum eigenvalue transformation of unitary matrices
area: quantum/quantum-simulation
level: research
summary: "Given a Hermitian block encoding of H/alpha, interleave d calls with phased reflections chosen by QSP. The block becomes p(H/alpha) for any real polynomial p of parity d mod 2 with |p| <= 1."
prereqs: [quantum-signal-processing, qubitization, block-encoding]
see_also: [optimal-hamiltonian-simulation, linear-system-solving, condition-number, singular-value-decomposition, jackson-theorem, minimax-approximation, amplitude-amplification, ground-state-energy-estimation]
sources:
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM STOC, 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1: Definition 15 (alternating phase modulation), Theorem 17 (singular value transformation), Corollary 18 (real polynomials), Lemma 22 (robustness), Lemma 25 (the sign function), Theorem 27 (fixed-point amplitude amplification), Theorem 41 (pseudoinverse), Theorem 56 (eigenvalue transformation of arbitrary parity) and Corollary 69 (the polynomial for 1/x)"
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "Theorem 2 (qubitization), Lemma 10 (existence of qubitization) and Theorems 3 and 4 (ancilla-free and single-ancilla quantum signal processing on the iterate)"
  - paper: doi:10.1103/PRXQuantum.2.040203
    title: "John M. Martyn, Zane M. Rossi, Andrew K. Tan and Isaac L. Chuang, Grand unification of quantum algorithms, PRX Quantum 2(4), 2021, article 040203 (arXiv:2105.02859)"
    locator: "the eigenvalue transformation as the Hermitian case of the singular value transformation, and its use for search, simulation and linear systems"
  - paper: doi:10.1103/PRXQuantum.3.040305
    title: "Yulong Dong, Lin Lin and Yu Tong, Ground-state preparation and energy estimation on early fault-tolerant quantum computers via quantum eigenvalue transformation of unitary matrices, PRX Quantum 3(4), 2022, article 040305 (arXiv:2204.05955)"
    locator: "Theorem 1 (QET-U: an even polynomial of cos(H/2) from controlled e^(-iH) and one ancilla)"
  - paper: doi:10.1103/PhysRevLett.103.150502
    title: "Aram W. Harrow, Avinatan Hassidim and Seth Lloyd, Quantum algorithm for linear systems of equations, Physical Review Letters 103(15), 2009, article 150502 (arXiv:0811.3171)"
    locator: "the whole paper: the algorithm and its cost in the sparsity, the condition number and the error"
  - paper: doi:10.1137/16M1087072
    title: "Andrew M. Childs, Robin Kothari and Rolando D. Somma, Quantum algorithm for systems of linear equations with exponentially improved dependence on precision, SIAM Journal on Computing 46(6), 2017, pages 1920 to 1950 (arXiv:1511.02306)"
    locator: "the main results: 1/x as a linear combination of unitaries, and variable-time amplitude amplification"
  - paper: doi:10.1038/nphys3272
    title: "Scott Aaronson, Read the fine print, Nature Physics 11, 2015, pages 291 to 293"
    locator: "the whole commentary: the four caveats of the linear systems algorithm"
---

The *quantum eigenvalue transformation* (QET) applies a polynomial to the eigenvalues of a Hermitian matrix that is given as a [block encoding](/block-encoding/). Let $U$ act on $a$ ancilla qubits and $n$ system qubits, with $U = U^\dagger$ and top-left block $H/\alpha$, and let $\Pi = |0^a\rangle\langle 0^a| \otimes I$. For a sequence of phases $\psi_0, \ldots, \psi_d$,
$$U_\psi = e^{i\psi_0(2\Pi - I)}\, U\, e^{i\psi_1(2\Pi - I)}\, U \cdots U\, e^{i\psi_d(2\Pi - I)}$$
has the top-left block $P(H/\alpha)$, where $P$ is the polynomial that the same phases give in one-qubit [quantum signal processing](/quantum-signal-processing/). With one more qubit, the block becomes $p(H/\alpha)$ for every real polynomial $p$ of degree $d$ and parity $d \bmod 2$ with $|p(x)| \le 1$ on $[-1, 1]$. The cost is $d$ calls to $U$ and $d + 1$ phased reflections. This is the last step of the chain: the block encoding gives the matrix, [qubitization](/qubitization/) splits the space into one plane per eigenvalue, and QSP fixes the polynomial on every plane at once. Gilyén, Su, Low and Wiebe (2019) proved the general form for singular values, of which this is the Hermitian case, and Martyn, Rossi, Tan and Chuang (2021) use the name QET for it.

## In plain words

Many tasks need a function of a large matrix applied to a quantum state: an exponential for time evolution, an inverse for a linear system, or a step function that keeps only the low-energy part. Classically one would find the eigenvalues and change each one. Here the matrix is hidden in a corner of a reversible circuit. We call the circuit again and again, and between the calls we turn the helper qubits by angles that a classical computer chose in advance. Each eigenvalue then gets changed by the same curve, without anyone learning the eigenvalues. The curve can be any polynomial that stays between minus one and one and is either even or odd. The number of calls equals the degree of the polynomial, so a function that a low-degree polynomial approximates well is cheap.

## When it applies

- There is a block encoding $U$ of a Hermitian $H$ with normalization $\alpha$, and $U^2 = I$. If $U$ is not Hermitian, make it so with Lemma 10 of [qubitization](/qubitization/), at the cost of one qubit.
- The goal is $f(H)$ applied to a state, and a polynomial $p$ of low degree with $|p| \le 1$ approximates $f(\alpha x)$, up to a scale factor, on the part of $[-1, 1]$ that holds the spectrum. The [Jackson theorem](/jackson-theorem/), [Chebyshev series](/chebyshev-series/) and [minimax approximation](/minimax-approximation/) give the degree.
- The output may be a quantum state or a block encoding of $f(H)$ for later steps. It is not a list of numbers.

## The template

Write $k = 2^n$ for the number of rows in the range of $\Pi$. The new control qubit is the highest qubit, and $\mathrm{Had}$ is the Hadamard gate on it.

```pseudo id=main
QET-REAL(U, a, n, f, d)    ▷ U = U^†, U^2 = I, block H/α; f real, parity d mod 2, |f| < 1 on [-1, 1]
L1  Φ ← QSP-PHASES(f, d)    ▷ the W(x) convention: Re <0|U_Φ(x)|0> = f(x)
L2  V_+ ← e^(iψ_0(2Π-I)) U e^(iψ_1(2Π-I)) U ... U e^(iψ_d(2Π-I)),  ψ from Φ in the reflection convention
L3  V_- ← the same sequence with ψ from -Φ
L4  V ← (Had ⊗ I) (|0><0| ⊗ V_+ + |1><1| ⊗ V_-) (Had ⊗ I)
L5  return i^d V    ▷ top-left block f(H/α); the factor i^d is a global phase
```

The two branches V_+ and V_- call $U$ at the same places and differ only in the phases, so in a circuit $U$ is not controlled: only the $d + 1$ phased reflections depend on the control qubit. The phase conversion is $\psi_0 = \phi_0 - \pi/4$, $\psi_d = \phi_d - \pi/4$ and $\psi_j = \phi_j - \pi/2$ in between, as on the QSP page.

**Why it works.** By qubitization, for each eigenpair $(\lambda, |\lambda\rangle)$ of $H$ the plane spanned by $|G_\lambda\rangle = |0^a\rangle|\lambda\rangle$ and $|G_\lambda^\perp\rangle$ is invariant under $U$ and under $\Pi$. On it, $U$ is the reflection $R(x)$ with $x = \lambda/\alpha$, and $2\Pi - I$ is $Z$, so $e^{i\psi(2\Pi - I)}$ is $e^{i\psi Z}$. So on the plane $V_+$ is the one-qubit sequence $e^{i\psi_0 Z}R(x)\cdots R(x)e^{i\psi_d Z} = (-i)^d U_\Phi(x)$, and
$$\langle G_\lambda|V_+|G_\lambda\rangle = (-i)^d P(x).$$
The planes of different eigenvectors are orthogonal, and the $|G_\lambda\rangle$ span the range of $\Pi$, so the block of $V_+$ is $(-i)^d P(H/\alpha)$. The sequence for $-\Phi$ gives $P^*$, and the Hadamard sandwich averages the two branches, so the block of $V$ is $(-i)^d\,\mathrm{Re}\,P(H/\alpha) = (-i)^d f(H/\alpha)$. This is Corollary 18 of Gilyén, Su, Low and Wiebe, specialized to a Hermitian block.

**Arbitrary parity** (Theorem 56). If $|f| \le 1/2$ on $[-1, 1]$, split $f$ into $f_e(x) = f(x) + f(-x)$ and $f_o(x) = f(x) - f(-x)$, both bounded by 1. Run QET-REAL for each and combine the two circuits with one more control qubit and Hadamards. The block is $(f_e + f_o)/2 = f$. The code does this with $2 + a + n$ qubits.

**Cost.** $d$ calls to $U$, $d + 1$ reflections about $|0^a\rangle$ with a controlled phase, which are $O(a)$ gates each, and one extra qubit, or two for mixed parity. The phases are computed once on a classical computer. A run applies $f(H/\alpha)$ to $|\psi\rangle$ with probability $\|f(H/\alpha)\psi\|^2$, and [amplitude amplification](/amplitude-amplification/) can raise it.

**Example: a $2 \times 2$ linear system.** Take $H = 0.6X + 0.2Z + 0.1I$, so $\alpha = 0.9$, the eigenvalues are $0.1 \pm \sqrt{0.4} = 0.7325$ and $-0.5325$, and the [condition number](/condition-number/) is $\kappa = 1.376$. The values $x = \lambda/\alpha$ are $0.8138$ and $-0.5916$, both in $[1/2, 1]$ in absolute value. The odd degree-5 polynomial $p(x) = 3.02619x - 5.376791x^3 + 2.891417x^5$ fits $1/(2x)$ on $[1/2, 1]$ with error at most $0.069$, and $|p| \le 0.932$ on $[-1, 1]$. At the two eigenvalues, $p = 0.5969$ and $-0.8865$, against $1/(2x) = 0.6144$ and $-0.8451$. The circuit has $1 + 2 + 1 = 4$ qubits: the control, the two ancillas of the block encoding of three Pauli terms, and the system. On $|b\rangle = |0\rangle$, the exact solution of $Hx = b$ is $x = (10/39, 60/39)$. The circuit succeeds with probability $0.5031$, close to the value $0.4926$ of the exact $(\alpha/2)H^{-1}$, and the output state has fidelity $0.9985$ with $x/\|x\|$. The tests in `impl/python` check these numbers, check random real polynomials of degree 2 to 5 on a 2-qubit $H$, and check the mixed-parity circuit.

## Classic examples

- **Hamiltonian simulation.** $p = \cos(\alpha t x)$ and $\sin(\alpha t x)$, truncated from the Jacobi-Anger expansion, give $e^{-iHt}$ with $O(\alpha t + \log(1/\epsilon))$ calls. See [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/).
- **Eigenvalue thresholds.** An odd polynomial close to the sign function outside $(-\delta, \delta)$ has degree $O(\log(1/\epsilon)/\delta)$ (Lemma 25). Shifted by an energy $\mu$, it projects a state onto the eigenvectors below $\mu$. This is a tool for ground state preparation and [ground state energy estimation](/ground-state-energy-estimation/).
- **Amplitude amplification.** For a $1 \times 1$ block (an amplitude), the same circuit is amplitude amplification, and a polynomial close to the sign function gives fixed-point amplification (Theorem 27).
- **Linear systems.** An odd polynomial, bounded by 1, that is within $\epsilon$ of $3/(4\kappa x)$ on $[-1, -1/\kappa] \cup [1/\kappa, 1]$ has degree $O(\kappa\log(1/\epsilon))$ (Corollary 69). It gives a block encoding of a multiple of $H^{-1}$. This is the eigenvalue transformation form of the algorithm of Harrow, Hassidim and Lloyd (2009), whose original version uses phase estimation and costs $\tilde O(\log(N)s^2\kappa^2/\epsilon)$ for an $s$-sparse $N \times N$ system. Childs, Kothari and Somma (2017) reach a cost polylogarithmic in $1/\epsilon$ and almost linear in $\kappa$. For a matrix that is not Hermitian or not square, the singular value version gives the [pseudoinverse](/pseudoinverse/) (Theorem 41).

**The fine print of quantum linear systems.** Aaronson (2015) lists the conditions under which these algorithms beat classical [linear system solving](/linear-system-solving/):
- $A$ must have a block encoding with small $\alpha$, for example a [sparse matrix](/sparse-matrix/) with an efficient oracle for its nonzero entries. A dense matrix stored as a table has none in general.
- The cost grows with the condition number $\kappa$. Classical methods for [sparse linear systems](/sparse-linear-systems/), such as the [conjugate gradient method](/conjugate-gradient-method/), also run fast when $\kappa$ is small, with about $\sqrt\kappa$ iterations for positive definite $A$.
- A fast circuit must prepare the state $|b\rangle = \sum_i b_i|i\rangle/\|b\|$. Loading $N$ arbitrary numbers costs about $N$ gates, which removes the speedup.
- The output is the quantum state $|x\rangle \propto A^{-1}|b\rangle$, not the vector $x$. Reading all $N$ entries needs about $N$ repetitions. The method helps only when a few numbers, such as an expectation value $\langle x|M|x\rangle$, are enough.

## Variations

- **Singular value transformation** (Theorem 17). For any unitary $U$ and projectors $\Pi$, $\tilde\Pi$, the alternating sequence of $U$, $U^\dagger$ and phased reflections $e^{i\phi(2\Pi - I)}$, $e^{i\phi(2\tilde\Pi - I)}$ applies $P$ to the singular values of $\tilde\Pi U\Pi$, as in the [singular value decomposition](/singular-value-decomposition/). For a Hermitian block and a polynomial of definite parity, the singular value and eigenvalue forms agree.
- **Transformation of a unitary** (Dong, Lin and Tong 2022, Theorem 1). Given controlled $e^{-iH}$ in place of a block encoding, one ancilla and symmetric phases give $F(\cos(H/2))$ for every even real $F$ with $|F| \le 1$. The input is a time evolution, for example from a [product formula](/trotter-suzuki-product-formulas/), and the circuit has no multi-qubit controls. The stub alias "quantum eigenvalue transformation of unitary matrices" is the name of this variant.
- **Robustness** (Lemma 22). If $U$ is only an $\epsilon$-approximate block encoding, a degree-$d$ transformation has error at most $4d\sqrt{\epsilon/\alpha}$ in the general case, so the block encoding must be more precise than the target.
- **Complex polynomials.** Without the control qubit, the block is the complex $P(H/\alpha)$ whose real part is $f$. This is enough when $P$ itself is the target, for example $P(x) = e^{-i\tau x}$ up to the parity split, with the conditions of Theorem 3 of the QSP page.

## Pitfalls

- **Bound and parity.** $|p| \le 1$ on all of $[-1, 1]$, not only on the spectrum, and $p$ must be even or odd. A fit of $1/x$ that is good on $[1/\kappa, 1]$ can be far above 1 near 0. Check the peak of $p$ on the whole interval, as in the example.
- **The scale factor.** QET gives $p(H/\alpha)$ with $|p| \le 1$, so a target such as $H^{-1}$ comes out as $H^{-1}/(\kappa\alpha)$ or similar, and the success probability carries that factor. Count it in the cost.
- **One branch alone is complex.** Without the average over $\Phi$ and $-\Phi$, the block is $P(H/\alpha)$ with $\mathrm{Re}\,P = f$, and $\mathrm{Im}\,P$ is not small. The tests show this.
- **$U^2 = I$.** For a block encoding that is not Hermitian, the planes are not invariant, and the block is not $P(H/\alpha)$. Use the Hermitian form first, or use the singular value form with $U$ and $U^\dagger$ in turn.
- **Phase conventions.** Phases from the $W(x)$ convention must be converted before they are used with reflections, and the global factor $(-i)^d$ must be tracked when the circuit is used under control.

## Exercises

1. Show that on the plane of an eigenvalue $\lambda$, $e^{i\psi(2\Pi - I)}$ acts as $e^{i\psi Z}$, and that the sequence with all $\psi_j = -\pi/2$ for $0 < j < d$ and $\psi_0 = \psi_d = -\pi/4$ gives the block $(-i)^dT_d(H/\alpha)$.
2. Prove that the block of $V$ in QET-REAL is $(-i)^d\,\mathrm{Re}\,P(H/\alpha)$ by writing $(\mathrm{Had} \otimes I)(|0\rangle\langle 0| \otimes V_+ + |1\rangle\langle 1| \otimes V_-)(\mathrm{Had} \otimes I)$ in blocks.
3. For $H = 0.6X + 0.2Z + 0.1I$, compute $\alpha$, the two values $x = \lambda/\alpha$, and the exact $(\alpha/2)H^{-1}|0\rangle$. Compare with the success probability $0.5031$.
4. Explain why the mixed-parity construction needs $|f| \le 1/2$ and not $|f| \le 1$.
5. In a linear system with $\kappa = 100$ and $\alpha = \|A\|$, estimate the degree of the polynomial for $1/x$ and the success probability of one run on a vector $b$ whose weight lies on the smallest eigenvalues.

## References
