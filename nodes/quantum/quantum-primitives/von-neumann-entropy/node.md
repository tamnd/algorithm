---
tag: AFM9DC
kind: definition
slug: von-neumann-entropy
name: Von Neumann entropy
aliases:
- quantum entropy
area: quantum/quantum-primitives
level: advanced
summary: "S(rho) = -Tr(rho log2 rho), the Shannon entropy of the eigenvalues of a density matrix. It is 0 for pure states, log2 d for I/d, and is strongly subadditive."
prereqs: [density-matrix, shannon-entropy]
see_also: [entanglement-entropy, partial-trace, mixed-state, binary-entropy-function, conditional-entropy, entanglement, gibbs-state-preparation, convex-function]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 11.3 (von Neumann entropy, with 11.3.1 to 11.3.6 on relative entropy, subadditivity and concavity) and Section 11.4 (strong subadditivity)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 5.2 (quantum entropy)
  - url: http://eudml.org/doc/59231
    title: "John von Neumann, Thermodynamik quantenmechanischer Gesamtheiten, Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse, 1927"
    locator: pp. 273 to 291
  - paper: doi:10.1007/BF01646092
    title: Huzihiro Araki and Elliott H. Lieb, Entropy inequalities, Communications in Mathematical Physics 18(2), 1970
    locator: pp. 160 to 170
  - paper: doi:10.1063/1.1666274
    title: Elliott H. Lieb and Mary Beth Ruskai, Proof of the strong subadditivity of quantum-mechanical entropy, Journal of Mathematical Physics 14(12), 1973
    locator: pp. 1938 to 1941
---

The von Neumann entropy of a [density matrix](/density-matrix/) $\rho$ is $S(\rho) = -\operatorname{Tr}(\rho\log_2\rho)$. If $\rho$ has eigenvalues $\lambda_1, \ldots, \lambda_d$, then $S(\rho) = -\sum_i \lambda_i\log_2\lambda_i$, the [Shannon entropy](/shannon-entropy/) of the eigenvalue distribution. It measures how [mixed](/mixed-state/) a state is: it is 0 exactly for pure states and $\log_2 d$ for the maximally mixed state $I/d$. For the parts of a composite system, its inequalities (subadditivity, the Araki-Lieb inequality and strong subadditivity) are the base of quantum information theory. This page uses base 2, so entropy is in bits.

## Definition

Let $\rho$ be a density matrix on $\mathbb{C}^d$ with spectral decomposition $\rho = \sum_i \lambda_i|e_i\rangle\langle e_i|$. The **von Neumann entropy** of $\rho$ is

$$S(\rho) = -\operatorname{Tr}(\rho\log_2\rho) = -\sum_{i=1}^{d}\lambda_i\log_2\lambda_i = H(\lambda_1, \ldots, \lambda_d),$$

with the convention $0\log 0 = 0$. Here $\log_2\rho = \sum_i \log_2\lambda_i\,|e_i\rangle\langle e_i|$ on the support of $\rho$, and $H$ is the Shannon entropy. With the natural logarithm, the entropy is in nats, and $S_{\text{nats}} = S_{\text{bits}}\ln 2$. Physics texts often use the natural logarithm, and quantum information texts base 2.

For subsystems, write $S(A) = S(\rho_A)$, $S(AB) = S(\rho_{AB})$ and so on, where $\rho_A = \operatorname{Tr}_B\rho_{AB}$ is the [partial trace](/partial-trace/). The **conditional entropy** is $S(A|B) = S(AB) - S(B)$, and the **mutual information** is $I(A:B) = S(A) + S(B) - S(AB)$, as in the classical [conditional entropy](/conditional-entropy/).

The **relative entropy** of $\rho$ to $\sigma$ is $S(\rho\|\sigma) = \operatorname{Tr}(\rho\log_2\rho) - \operatorname{Tr}(\rho\log_2\sigma)$ when the support of $\rho$ lies in that of $\sigma$, and $+\infty$ otherwise. **Klein's inequality** says $S(\rho\|\sigma) \ge 0$, with equality exactly when $\rho = \sigma$.

### Properties of one state

- **Range.** $0 \le S(\rho) \le \log_2 d$. The eigenvalues form a probability distribution on $d$ outcomes, and the Shannon entropy of such a distribution lies in $[0, \log_2 d]$. The lower bound is reached exactly when one eigenvalue is 1, so $S(\rho) = 0$ exactly when $\rho$ is pure. The upper bound is reached exactly for the uniform distribution, that is, $\rho = I/d$. In terms of relative entropy, $S(\rho\|I/d) = \log_2 d - S(\rho) \ge 0$.
- **Unitary invariance.** $S(U\rho U^\dagger) = S(\rho)$, because the eigenvalues do not change.
- **One qubit.** A qubit state with Bloch vector $\vec r$ has eigenvalues $(1 \pm |\vec r|)/2$, so $S(\rho) = h\bigl((1 + |\vec r|)/2\bigr)$ with $h$ the [binary entropy function](/binary-entropy-function/). It depends only on the distance from the centre of the Bloch ball.
- **Measurement in a basis.** For the diagonal $p_i = \langle i|\rho|i\rangle$ in any basis, $H(p) \ge S(\rho)$, with equality when the basis diagonalizes $\rho$. A measurement that forgets its result can only increase entropy.
- **Concavity and its limit.** For a mixture $\rho = \sum_j p_j\rho_j$, $\sum_j p_j S(\rho_j) \le S(\rho) \le \sum_j p_j S(\rho_j) + H(p)$. The right side is an equality when the $\rho_j$ have orthogonal supports. For an ensemble of pure states this reads $S(\rho) \le H(p)$: the entropy of the ensemble weights bounds the entropy of the state, and the two differ when the states are not orthogonal.

### Inequalities for composite systems

- **Additivity.** $S(\rho \otimes \sigma) = S(\rho) + S(\sigma)$, because the eigenvalues of $\rho\otimes\sigma$ are the products $\lambda_i\mu_j$.
- **Pure joint states.** If $\rho_{AB}$ is pure, then $S(A) = S(B)$. The two reduced states have the same nonzero eigenvalues, the squares of the Schmidt coefficients (see the partial trace page). This common value is the [entanglement entropy](/entanglement-entropy/) of the state.
- **Subadditivity.** $S(AB) \le S(A) + S(B)$, with equality exactly for $\rho_{AB} = \rho_A \otimes \rho_B$. *Proof.* $\log_2(\rho_A \otimes \rho_B) = \log_2\rho_A \otimes I + I \otimes \log_2\rho_B$, so $S(\rho_{AB}\|\rho_A\otimes\rho_B) = -S(AB) + S(A) + S(B)$, which is $\ge 0$ by Klein's inequality. $\square$ So $I(A:B) \ge 0$.
- **Araki-Lieb (triangle) inequality.** $S(AB) \ge |S(A) - S(B)|$. *Proof.* Take a purification $|\psi\rangle_{ABR}$ of $\rho_{AB}$. Then $S(R) = S(AB)$ and $S(A) = S(BR)$, both by the rule for pure joint states. Subadditivity gives $S(A) = S(BR) \le S(B) + S(R) = S(B) + S(AB)$. Exchange $A$ and $B$ for the other sign. $\square$
- **Strong subadditivity (Lieb and Ruskai 1973).** For every state on $A \otimes B \otimes C$, $S(ABC) + S(B) \le S(AB) + S(BC)$. Equivalently, $I(A : BC) \ge I(A : B)$: discarding $C$ does not increase the mutual information. Its proof is much harder than that of subadditivity, and it rests on Lieb's concavity theorem.
- **Negative conditional entropy.** Classical conditional entropy is never negative, but $S(A|B)$ can be. For a [Bell state](/bell-states/), $S(AB) = 0$ and $S(B) = 1$, so $S(A|B) = -1$. A negative value shows [entanglement](/entanglement/), since $S(A|B) \ge 0$ for every separable state.

## Examples and non-examples

**A worked example.** The density matrix $\rho = \begin{pmatrix}3/4 & 1/4\\ 1/4 & 1/4\end{pmatrix}$, the equal mixture of $|0\rangle$ and $|+\rangle$, has eigenvalues $(2 \pm \sqrt2)/4 \approx 0.8536$ and $0.1464$. So

$$S(\rho) = -0.8536\log_2 0.8536 - 0.1464\log_2 0.1464 \approx 0.1950 + 0.4058 = 0.6009 \text{ bits}.$$

Its Bloch vector $(1/2, 0, 1/2)$ has length $1/\sqrt2$, and $h((1 + 1/\sqrt2)/2) = h(0.8536)$ gives the same value. The ensemble weights $(1/2, 1/2)$ have Shannon entropy 1 bit, more than $S(\rho)$, because $|0\rangle$ and $|+\rangle$ are not orthogonal.

**Other values.**

| state | eigenvalues | $S$ in bits |
|---|---|---|
| any pure state, such as $\lvert+\rangle$ | $1, 0$ | $0$ |
| $\operatorname{diag}(3/4, 1/4)$ | $3/4, 1/4$ | $h(3/4) \approx 0.8113$ |
| $I/2$ | $1/2, 1/2$ | $1$ |
| $I/d$ | $1/d$ each | $\log_2 d$ |
| one half of a Bell state | $1/2, 1/2$ | $1$ |
| the whole Bell state | $1, 0, 0, 0$ | $0$ |

The last two rows show that a part can have more entropy than the whole, which never happens for classical distributions.

**Non-examples.**

- **The Shannon entropy of the diagonal.** For $|+\rangle$, the diagonal $(1/2, 1/2)$ in the computational basis has entropy 1, but $S = 0$. The diagonal depends on the basis; the eigenvalues do not.
- **The entropy of the ensemble weights.** It depends on the ensemble, and many ensembles give one $\rho$. It is at least $S(\rho)$, with equality only for ensembles of orthogonal states.
- **The logarithm of the entries.** $-\sum_{ij}\rho_{ij}\log\rho_{ij}$ is not $S(\rho)$, and it is not even defined for negative or complex entries. The logarithm is a matrix function, taken through the eigenvalues.
- **The linear entropy** $1 - \operatorname{Tr}\rho^2$ is also 0 exactly for pure states, but it is a different function. It is not additive over tensor products.

### Common errors

- **The base of the logarithm.** A value of $0.6931$ for $I/2$ is in nats; in bits it is 1.
- **Eigenvalues near zero.** In floating point, a pure state can have eigenvalues like $-10^{-17}$. Set eigenvalues below a small cutoff to 0 before taking logarithms.
- **Conditional entropy is not an entanglement test in one direction.** $S(A|B) < 0$ implies entanglement, but many entangled states have $S(A|B) \ge 0$.

### Implementation

The Python code with this page computes $S$ from the eigenvalues of the Jacobi method in the shared helper, the qubit formula, the relative entropy, the conditional entropy and the mutual information. Its tests check the eigenvalues through the power sums $\sum_i\lambda_i^k = \operatorname{Tr}\rho^k$, compare $S$ with $-\operatorname{Tr}(\rho\log_2\rho)$ through the matrix logarithm, and check the diagonal and qubit cases, the bounds, the equal entropies of the parts of random pure states, subadditivity and Araki-Lieb, strong subadditivity on random three-qubit states, concavity with its upper bound, and Klein's inequality.

## Related definitions

- [Shannon entropy](/shannon-entropy/): the classical entropy, equal to $S$ for diagonal density matrices.
- [Entanglement entropy](/entanglement-entropy/): $S(\rho_A)$ for a pure joint state, a measure of entanglement.
- [Mixed state](/mixed-state/): the states with $S > 0$.
- [Partial trace](/partial-trace/): gives the reduced states whose entropies the inequalities compare.
- [Binary entropy function](/binary-entropy-function/): the entropy of a qubit as a function of the length of its Bloch vector.
- [Gibbs state preparation](/gibbs-state-preparation/): the Gibbs state $e^{-\beta H}/Z$ has the largest entropy among the states with a given mean energy.

### History

Von Neumann defined the entropy of a statistical operator in his 1927 paper on the thermodynamics of quantum ensembles, from a thermodynamic argument. Araki and Lieb proved the triangle inequality in 1970, and Lieb and Ruskai proved strong subadditivity in 1973, after it had been conjectured by Lanford and Robinson.

## References
