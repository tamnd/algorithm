---
tag: 8Q7YB1
kind: technique
slug: qubitization
name: Qubitization
aliases:
- quantum walk qubitization
- Low-Chuang qubitization
area: quantum/quantum-simulation
level: research
summary: "From a block encoding U of H/alpha with U^2 = I, form the walk W = (2 Pi - I) U. It splits into one 2 x 2 rotation for each eigenvalue lambda, with eigenvalues e^(+-i arccos(lambda/alpha))."
prereqs: [block-encoding, quantum-signal-processing, chebyshev-polynomials]
see_also: [quantum-eigenvalue-transformation, optimal-hamiltonian-simulation, linear-combination-of-unitaries, sparse-hamiltonian-simulation, quantum-phase-estimation, ground-state-energy-estimation, quantum-walk-search, amplitude-amplification]
sources:
  - paper: doi:10.22331/q-2019-07-12-163
    title: "Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3, 2019, article 163 (arXiv:1610.06546)"
    locator: "Definition 1 (standard form), Theorem 1 (simulation by qubitization), Theorem 2 (qubitization), Lemma 8 (conditions on qubitization), Corollary 9 (qubitization of reflections), Lemma 10 (existence of qubitization), Lemma 11 (the phased iterate), Corollaries 15 to 17"
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM STOC, 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1: Section 3 (the invariant subspaces of a projected unitary, Definitions 11 and 12) and Corollary 60 (the query complexity of block-Hamiltonian simulation)"
  - paper: arxiv:0810.0312
    title: "Andrew M. Childs, On the relationship between continuous- and discrete-time quantum walk, Communications in Mathematical Physics 294(2), 2010, pages 581 to 603"
    locator: "the discrete-time walk of a Hamiltonian and its eigenvalues, the forerunner of the walk operator"
  - paper: arxiv:0910.4157
    title: "Dominic W. Berry and Andrew M. Childs, Black-box Hamiltonian simulation and unitary implementation, Quantum Information and Computation 12(1-2), 2012, pages 29 to 62"
    locator: "Hamiltonian simulation by phase estimation on the quantum walk"
---

*Qubitization* turns a [block encoding](/block-encoding/) of a Hermitian matrix into a unitary whose eigenvalues carry the eigenvalues of the matrix. Let $U$ act on $a$ ancilla qubits and $n$ system qubits with
$$(\langle 0^a| \otimes I)\, U\, (|0^a\rangle \otimes I) = H/\alpha, \qquad U^2 = I,$$
and let $\Pi = |0^a\rangle\langle 0^a| \otimes I$. The *walk operator* (Low and Chuang call it the iterate) is
$$W = (2\Pi - I)\, U.$$
For every eigenvalue $\lambda$ of $H$, $W$ keeps a plane that contains $|0^a\rangle|\lambda\rangle$, and on it $W$ is a rotation with eigenvalues $e^{\pm i\arccos(\lambda/\alpha)}$. So the whole space splits into small blocks, each a copy of the one-qubit signal of [quantum signal processing](/quantum-signal-processing/) with $x = \lambda/\alpha$. Low and Chuang (2016, published 2019) named the method and used it for [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/). In the chain of methods it comes after the block encoding and QSP: it is what lets a one-qubit polynomial act on all eigenvalues at once, and the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) is the result. Any block encoding can be qubitized with one more qubit (Lemma 10).

## In plain words

A block encoding hides a matrix in one corner of a larger reversible operation. Using it once gives a scaled copy of the matrix, with some chance of failure. Qubitization adds one simple step: after each use, flip the sign of everything that is outside the corner. The combination of the two steps behaves, for each eigenvalue of the matrix separately, like a turn of one qubit by an angle that the eigenvalue fixes. The many eigenvalues do not mix. This lets us treat a large matrix as a bundle of independent one-qubit problems. Repeating the combined step gives the Chebyshev polynomials of the matrix. Adding a few phase turns gives any bounded polynomial. Measuring the angle of the turn with phase estimation gives the eigenvalue itself.

## When it applies

- There is a block encoding $U$ of a Hermitian $H$ with normalization $\alpha$, for example the PREPARE, SELECT, PREPARE$^\dagger$ circuit of a [linear combination of unitaries](/linear-combination-of-unitaries/) or the sparse construction for [sparse Hamiltonian simulation](/sparse-hamiltonian-simulation/).
- $U^2 = I$, which holds when $U$ is Hermitian. A SELECT of Pauli strings with a Householder PREPARE, as in the code, has this property. Otherwise first apply Lemma 10 below, at the cost of one qubit and a controlled $U$ and $U^\dagger$.
- The goal is a function of $H/\alpha$ (simulation, filtering, inversion) or the eigenvalues of $H$ (energy estimation), and the cost is counted in calls to $U$.

## The template

The ancillas are the high qubits, so $\Pi$ is the projector onto the first $2^n$ basis states, and $H/\alpha$ is the top-left block of $U$.

```pseudo id=main
QUBITIZE(U, a, n)    ▷ U = U^†, U^2 = I, top-left block H/α
L1  W ← (2Π - I) · U,  Π = |0^a><0^a| ⊗ I
L2  for each eigenpair (λ, |λ>) of H, with x = λ/α:
L3      |G_λ> ← |0^a>|λ>
L4      |G_λ^⊥> ← (U|G_λ> - x|G_λ>) / sqrt(1 - x^2)
L5      θ_λ ← arccos(x):  W = [[x, sqrt(1-x^2)], [-sqrt(1-x^2), x]] in the basis (|G_λ>, |G_λ^⊥>)
L6  return W    ▷ eigenvalues e^(±iθ_λ), and ±1 on the rest of the space
```

The circuit only needs L1: one call to $U$ and one reflection about $|0^a\rangle$ on the ancillas. Lines L2 to L5 describe the spectrum and are not run.

**Why the plane is invariant.** Since $\Pi\,U|G_\lambda\rangle = |0^a\rangle (H/\alpha)|\lambda\rangle = x|G_\lambda\rangle$, the vector $U|G_\lambda\rangle - x|G_\lambda\rangle$ has no part in the range of $\Pi$, so $|G_\lambda^\perp\rangle$ is a unit vector with $\Pi|G_\lambda^\perp\rangle = 0$. Then $U|G_\lambda\rangle = x|G_\lambda\rangle + s|G_\lambda^\perp\rangle$ with $s = \sqrt{1-x^2}$. Because $U$ is Hermitian and $U^2 = I$, $U|G_\lambda^\perp\rangle = (|G_\lambda\rangle - xU|G_\lambda\rangle)/s = s|G_\lambda\rangle - x|G_\lambda^\perp\rangle$. So on the plane $U$ is the reflection $R(x) = \begin{pmatrix} x & s \\ s & -x\end{pmatrix}$, and $2\Pi - I$ is $Z$. The product is
$$W = Z\,R(x) = \begin{pmatrix} x & s \\ -s & x \end{pmatrix}, \qquad W\,\frac{|G_\lambda\rangle \pm i|G_\lambda^\perp\rangle}{\sqrt2} = e^{\pm i\arccos(x)}\,\frac{|G_\lambda\rangle \pm i|G_\lambda^\perp\rangle}{\sqrt2}.$$
Planes for different eigenvectors are orthogonal. Their sum contains the whole range of $\Pi$. On the orthogonal complement, $\Pi = 0$, so $W = -U$, whose eigenvalues are $\pm 1$.

**Chebyshev polynomials for free.** On each plane, $W^k = \begin{pmatrix} T_k(x) & sU_{k-1}(x) \\ -sU_{k-1}(x) & T_k(x)\end{pmatrix}$. So
$$(\langle 0^a| \otimes I)\, W^k\, (|0^a\rangle \otimes I) = T_k(H/\alpha):$$
$k$ calls to $U$ give a block encoding of the $k$-th [Chebyshev polynomial](/chebyshev-polynomials/) of $H/\alpha$.

**Phases give every QSP polynomial.** Replace the plain reflection $2\Pi - I$ by $e^{i\phi(2\Pi - I)}$ (Lemma 11 of Low and Chuang writes the phased iterate as $Z_{\phi+\pi/2} W Z_{-\phi-\pi/2}$). On each plane this is $e^{i\phi Z}$, so a sequence of phased reflections and calls to $U$ is the QSP sequence in the reflection convention, with $x = \lambda/\alpha$ on each plane. With one extra qubit it gives $\mathrm{Re}\,P(H/\alpha)$ for every real polynomial $P$ of definite parity bounded by 1. The [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/) writes this out.

**Cost.** One step of $W$ is one call to $U$ and one reflection about $|0^a\rangle$, a multi-controlled $Z$ with $O(a)$ gates. The step uses no new ancillas. Simulation by qubitization (Theorem 1 of Low and Chuang) uses $\Theta(Q)$ queries with $Q = O(\alpha t + \log(1/\epsilon))$, at most $\lceil\log_2 N\rceil + \lceil\log_2 d\rceil + 2$ qubits in total, where $N$ is the system dimension and $d$ the ancilla dimension, and $O(Q\log d)$ extra gates. The sharper count $\Theta(\alpha t + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/(\alpha t)))$ is Corollary 60 of Gilyén, Su, Low and Wiebe.

**Example: $H = X + Z$.** The block encoding from the [block encoding](/block-encoding/) page has $a = 1$, $\alpha = 2$ and $U^2 = I$. The eigenvalues of $H$ are $\pm\sqrt2$, so $x = \pm 0.7071$ and $\theta = \pi/4$ and $3\pi/4$. The four eigenvalues of the $4 \times 4$ walk $W$ are $e^{\pm i\pi/4}$ and $e^{\pm 3i\pi/4}$. The two planes fill the space, so there is no $\pm 1$ part. Phase estimation on $W$ that returns $\theta = \pi/4$ gives back $\lambda = \alpha\cos\theta = \sqrt2$. The tests in `impl/python` check this spectrum, check the invariant planes and the eigenvalues $e^{\pm i\arccos(\lambda/\alpha)}$ for random Pauli sums on 2 and 4 qubits with the rest of the spectrum at $\pm 1$, and check $W^k$ against $T_k(H/\alpha)$ for $k \le 6$.

## Classic examples

- **Optimal Hamiltonian simulation.** With phases that make $\cos(\alpha t x)$ and $\sin(\alpha t x)$, qubitization gives $e^{-iHt}$ with $O(\alpha t + \log(1/\epsilon))$ queries. For a $d$-sparse $H$ this is $O(dt\|H\|_{\max} + \log(1/\epsilon))$ queries (Corollary 15), for a [linear combination of unitaries](/linear-combination-of-unitaries/) $O(\alpha t + \log(1/\epsilon))$ (Corollary 16), and for a density matrix given by a purification $O(t + \log(1/\epsilon))$ (Corollary 17). See [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/).
- **Energy estimation.** [Quantum phase estimation](/quantum-phase-estimation/) on $W$ in place of $e^{-iHt}$ returns $\theta_\lambda$, and $\lambda = \alpha\cos\theta_\lambda$. Each step is one call to $U$, with no Trotter error. This is the usual form of [ground state energy estimation](/ground-state-energy-estimation/) in [quantum chemistry](/quantum-chemistry-simulation/).
- **Quantum walks.** For a sparse $H$ the walk operator is a Szegedy-type quantum walk on the graph of the nonzero entries. Childs (2010) used such a walk, with eigenvalues determined by those of $H$, and Berry and Childs (2012) simulated $e^{-iHt}$ by phase estimation on it. The walk view also underlies [quantum walk search](/quantum-walk-search/).
- **Amplitude amplification.** With $H$ a $1 \times 1$ matrix (a number $x$, the good amplitude), $W^k$ gives $T_k(x)$, which is the polynomial behind [amplitude amplification](/amplitude-amplification/).

## Variations

- **Making a block encoding Hermitian** (Lemma 10). If $U$ encodes a Hermitian $H/\alpha$ but $U$ is not Hermitian, add a flag qubit and use $U' = |0\rangle\langle 0| \otimes U + |1\rangle\langle 1| \otimes U^\dagger$ with the flag in $|+\rangle$, and a swap of the flag values in the reflection. The code puts the swap into the encoding: with $\mathrm{Had}$ the Hadamard gate on the flag, $(\mathrm{Had} \otimes I)\,(|0\rangle\langle 1| \otimes U + |1\rangle\langle 0| \otimes U^\dagger)\,(\mathrm{Had} \otimes I)$ is Hermitian, squares to $I$, and has the same top-left block. It costs one controlled $U$ and one controlled $U^\dagger$.
- **General conditions** (Lemma 8). A walk $W = (2\Pi - I)\,S U$ with $S$ on the ancillas works exactly when $\langle G|SU|G\rangle = H$ and $\langle G|SUSU|G\rangle = I$. Corollary 9 is the case $S = I$ with $U^2 = I$.
- **Normal and non-Hermitian matrices.** For a normal matrix there is a similar construction (Appendix A of Low and Chuang). For a general matrix, the same plane decomposition works with singular values in place of eigenvalues, using two projectors; this is the singular value transformation of Gilyén, Su, Low and Wiebe.
- **Other ancilla states.** The block can be defined with any state $|G\rangle = G|0^a\rangle$ in place of $|0^a\rangle$, and then the reflection is $2|G\rangle\langle G| - I$. This is the standard form of Definition 1.

## Pitfalls

- **$U^2 = I$ is needed.** For a block encoding that is not Hermitian, $(2\Pi - I)U$ is still unitary, but the planes are not invariant, and $W^k$ does not give $T_k(H/\alpha)$. The tests show this on a small example. Apply Lemma 10 first.
- **The reflection must be about the same state as the block.** If the block is $\langle G|U|G\rangle$ with $|G\rangle \ne |0^a\rangle$, reflect about $|G\rangle$, not about $|0^a\rangle$.
- **Arccos, not the eigenvalue.** The eigenphase of $W$ is $\arccos(\lambda/\alpha)$, not $\lambda t$. Phase estimation on $W$ gives $\cos\theta$ to error about $\sin\theta\,\delta\theta$, so the energy error is $\alpha\sin\theta\,\delta\theta$. A large $\alpha$ costs precision in proportion.
- **The sign of $\theta$.** Each $\lambda$ gives both $e^{i\theta}$ and $e^{-i\theta}$. A start state $|0^a\rangle|\lambda\rangle$ is an equal mix of the two eigenvectors, so phase estimation returns $+\theta$ or $-\theta$ at random. Both give the same $\cos\theta$.
- **Normalization.** All costs scale with $\alpha$, not with $\|H\|$. Qubitization does not reduce $\alpha$; it only removes the waste of post-selection.

## Exercises

1. For a single qubit block encoding of $H = x$ (a $1 \times 1$ matrix) with $U = R(x)$, write $W$ and its powers, and identify $T_k(x)$ in the corner.
2. Prove that $U|G_\lambda^\perp\rangle = s|G_\lambda\rangle - x|G_\lambda^\perp\rangle$ uses both $U = U^\dagger$ and $U^2 = I$. Which part of the proof fails if only $U$ is unitary?
3. Show that the dimension of the $\pm 1$ part of the spectrum of $W$ is $2^{a+n} - 2 \cdot 2^n$ when no eigenvalue of $H$ equals $\pm\alpha$. What happens when $\lambda = \alpha$?
4. Let $U$ have top-left block $A/\alpha$. Check that $(\mathrm{Had} \otimes I)(|0\rangle\langle 1| \otimes U + |1\rangle\langle 0| \otimes U^\dagger)(\mathrm{Had} \otimes I)$ has top-left block $(A + A^\dagger)/(2\alpha)$.
5. For $H = X + Z$, compute the eigenvectors of $W$ and the outcome distribution of perfect phase estimation started from $|0\rangle|\lambda\rangle$.

## References
