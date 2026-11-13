---
tag: GZQ3SX
kind: definition
slug: trace-distance
name: Trace distance
aliases:
- quantum total variation distance
area: quantum/quantum-primitives
level: advanced
summary: "D(rho, sigma) = (1/2) ||rho - sigma||_1, half the sum of the absolute eigenvalues of rho - sigma. It is the largest gap between the outcome probabilities of one measurement."
prereqs: [density-matrix, total-variation-distance]
see_also: [fidelity, state-discrimination-problem, matrix-norms, quantum-channel, quantum-measurement, bloch-sphere, quantum-state-tomography, swap-test]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 9.2.1 (trace distance) and Section 9.2.3 (relationships between distance measures)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 3.1 (quantum state discrimination, and the trace norm as the optimal bias)
  - paper: doi:10.1109/18.761271
    title: Christopher A. Fuchs and Jeroen van de Graaf, Cryptographic distinguishability measures for quantum-mechanical states, IEEE Transactions on Information Theory 45(4), 1999
    locator: pp. 1216 to 1227
---

The trace distance between two [density matrices](/density-matrix/) $\rho$ and $\sigma$ is $D(\rho, \sigma) = \frac12\|\rho - \sigma\|_1$, half the sum of the absolute values of the eigenvalues of $\rho - \sigma$. It is the quantum form of the [total variation distance](/total-variation-distance/): it equals the largest total variation distance between the outcome distributions of one measurement on $\rho$ and on $\sigma$. So it says how well one copy of a state can be told apart from another. With equal prior probabilities, the best guess is right with probability $(1 + D)/2$.

## Definition

The **trace norm** of a matrix $A$ is $\|A\|_1 = \operatorname{Tr}\sqrt{A^\dagger A}$, the sum of its singular values (see [matrix norms](/matrix-norms/)). For a Hermitian matrix with eigenvalues $\lambda_i$ it is $\sum_i |\lambda_i|$. The **trace distance** of two density matrices on $\mathbb{C}^d$ is

$$D(\rho, \sigma) = \frac12 \|\rho - \sigma\|_1 = \frac12 \sum_{i=1}^{d} |\lambda_i(\rho - \sigma)|.$$

### The variational form

**Theorem.** $D(\rho, \sigma) = \max_{P} \operatorname{Tr}\bigl(P(\rho - \sigma)\bigr)$, where the maximum is over the projectors $P$, and also over all matrices with $0 \le P \le I$. The maximum is attained by the projector $P_+$ onto the span of the eigenvectors of $\rho - \sigma$ with positive eigenvalues.

**Proof.** Write the spectral decomposition of $\rho - \sigma$ as $Q - S$, where $Q \ge 0$ collects the positive eigenvalues and $S \ge 0$ the negative ones, so $QS = 0$. Since $\operatorname{Tr}(\rho - \sigma) = 0$, $\operatorname{Tr} Q = \operatorname{Tr} S$, and so $\|\rho - \sigma\|_1 = \operatorname{Tr} Q + \operatorname{Tr} S = 2\operatorname{Tr} Q$, that is, $D = \operatorname{Tr} Q$. For $0 \le P \le I$, $\operatorname{Tr}(P(Q - S)) \le \operatorname{Tr}(PQ) \le \operatorname{Tr} Q$: the first step uses $\operatorname{Tr}(PS) \ge 0$, and the second uses $\operatorname{Tr}((I - P)Q) \ge 0$. The projector $P_+$ gives $\operatorname{Tr}(P_+ Q) = \operatorname{Tr} Q$ and $\operatorname{Tr}(P_+ S) = 0$. $\square$

**Corollary (measurements).** For every measurement with elements $E_m \ge 0$, $\sum_m E_m = I$, let $p_m = \operatorname{Tr}(E_m\rho)$ and $q_m = \operatorname{Tr}(E_m\sigma)$. Then $\frac12\sum_m |p_m - q_m| \le D(\rho, \sigma)$, with equality for the two-outcome measurement $\{P_+, I - P_+\}$. *Proof.* Let $M$ be the set of $m$ with $p_m > q_m$. The total variation distance is $\sum_{m \in M} (p_m - q_m) = \operatorname{Tr}(P(\rho - \sigma))$ with $P = \sum_{m \in M} E_m$, and $0 \le P \le I$. $\square$

### Telling two states apart

Suppose a state is $\rho$ with probability $p$ and $\sigma$ with probability $1 - p$, and we measure once to guess which. A test that answers "$\rho$" on outcome $P$ is right with probability $p\operatorname{Tr}(P\rho) + (1-p)\operatorname{Tr}((I-P)\sigma) = (1 - p) + \operatorname{Tr}\bigl(P(p\rho - (1-p)\sigma)\bigr)$. The argument of the theorem, applied to $p\rho - (1-p)\sigma$ (whose trace is $2p - 1$), gives the best value

$$P_{\text{succ}} = \frac12\Bigl(1 + \bigl\|p\rho - (1-p)\sigma\bigr\|_1\Bigr),$$

which is $(1 + D(\rho,\sigma))/2$ for $p = 1/2$. This is the Helstrom bound of the [state discrimination problem](/state-discrimination-problem/).

### Properties

- **A metric.** $D$ is symmetric, $D(\rho, \sigma) = 0$ only for $\rho = \sigma$, and the triangle inequality holds because $\|\cdot\|_1$ is a norm. Also $0 \le D \le 1$, with $D = 1$ exactly when $\rho$ and $\sigma$ have orthogonal supports.
- **Commuting states.** If $\rho = \sum_i p_i|i\rangle\langle i|$ and $\sigma = \sum_i q_i|i\rangle\langle i|$ in one basis, then $D(\rho, \sigma) = \frac12\sum_i|p_i - q_i|$, the total variation distance of the two eigenvalue distributions.
- **One qubit.** With Bloch vectors $\vec r$ and $\vec s$, $\rho - \sigma = \frac12(\vec r - \vec s)\cdot\vec\sigma$ has eigenvalues $\pm\frac12|\vec r - \vec s|$, so $D(\rho, \sigma) = \frac12|\vec r - \vec s|$: half the Euclidean distance in the [Bloch ball](/bloch-sphere/).
- **Pure states.** $D(|\psi\rangle\langle\psi|, |\phi\rangle\langle\phi|) = \sqrt{1 - |\langle\psi|\phi\rangle|^2}$. *Proof.* The difference has rank at most 2 and trace 0, so its eigenvalues are $\pm\lambda$. Then $2\lambda^2 = \operatorname{Tr}(\rho - \sigma)^2 = 2 - 2|\langle\psi|\phi\rangle|^2$. $\square$
- **Channels do not increase it.** For every [quantum channel](/quantum-channel/) $\Phi$, $D(\Phi(\rho), \Phi(\sigma)) \le D(\rho, \sigma)$. *Proof.* Let $P$ be the optimal projector for the outputs. Then $D(\Phi(\rho), \Phi(\sigma)) = \operatorname{Tr}(\Phi^\dagger(P)(\rho - \sigma))$, and the dual map $\Phi^\dagger$ is positive with $\Phi^\dagger(I) = I$, so $0 \le \Phi^\dagger(P) \le I$. The theorem then bounds the value by $D(\rho, \sigma)$. $\square$ The partial trace is a channel, so $D(\rho_A, \sigma_A) \le D(\rho_{AB}, \sigma_{AB})$. A unitary channel can be undone, so $D$ does not change under unitaries.
- **Joint convexity.** $D\bigl(\sum_i p_i\rho_i, \sum_i p_i\sigma_i\bigr) \le \sum_i p_i D(\rho_i, \sigma_i)$, from the triangle inequality of the norm.
- **Relation to fidelity.** With the [fidelity](/fidelity/) $F(\rho, \sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}$, the Fuchs-van de Graaf inequalities are $1 - F \le D \le \sqrt{1 - F^2}$. The right inequality is an equality for pure states.

## Examples and non-examples

**$|0\rangle$ and $|+\rangle$.** Here $|\langle 0|+\rangle|^2 = 1/2$, so $D = \sqrt{1/2} \approx 0.7071$. The Bloch vectors are $(0, 0, 1)$ and $(1, 0, 0)$, at Euclidean distance $\sqrt2$, which gives the same value. The difference $\rho - \sigma = \frac12\begin{pmatrix}1 & -1\\ -1 & -1\end{pmatrix}$ has eigenvalues $\pm\frac{\sqrt2}{2}$. The best single measurement guesses right with probability $(1 + 0.7071)/2 \approx 0.8536 = \cos^2(\pi/8)$, using the basis whose Bloch axis is parallel to $\vec r - \vec s = (-1, 0, 1)$.

**A mixed pair.** $\rho = \operatorname{diag}(3/4, 1/4)$ and $\sigma = I/2$ commute, so $D = \frac12(|3/4 - 1/2| + |1/4 - 1/2|) = 1/4$.

**Orthogonal states.** $D(|0\rangle\langle0|, |1\rangle\langle1|) = 1$: one measurement in the computational basis tells them apart with certainty. After the depolarizing channel $\rho \mapsto (1-p)\rho + pI/2$, their trace distance is $1 - p$.

**Non-examples.**

- **The Hilbert-Schmidt distance** $\|\rho - \sigma\|_2 = \sqrt{\operatorname{Tr}(\rho - \sigma)^2}$ is a metric, but channels can increase it. For $\rho = |0\rangle\langle0|$ and $\sigma = |1\rangle\langle1|$, the states $\rho \otimes I/2$ and $\sigma \otimes I/2$ are at Hilbert-Schmidt distance $1$, and after the partial trace $\rho$ and $\sigma$ are at distance $\sqrt2$. The trace distance is 1 in both cases.
- **Half the sum of the entries.** $\frac12\sum_{ij}|\rho_{ij} - \sigma_{ij}|$ depends on the basis and is not the trace distance. For $|0\rangle$ and $|+\rangle$ it is $\frac12(1/2 + 1/2 + 1/2 + 1/2) = 1$, while $D \approx 0.7071$.
- **$1 - |\langle\psi|\phi\rangle|$** is not the trace distance of pure states. The correct formula has the square root of $1 - |\langle\psi|\phi\rangle|^2$.

### Common errors

- **The factor $\frac12$.** Without it the distance runs from 0 to 2. Some papers use $\|\rho - \sigma\|_1$ itself; check before you compare numbers.
- **Several copies.** With $n$ copies the relevant distance is $D(\rho^{\otimes n}, \sigma^{\otimes n})$, which is not $n D(\rho, \sigma)$ and is bounded more easily through the fidelity, since $F(\rho^{\otimes n}, \sigma^{\otimes n}) = F(\rho, \sigma)^n$.
- **Absolute values of eigenvalues, not of the matrix.** The trace norm needs the eigenvalues of $\rho - \sigma$, not the difference of the eigenvalues of $\rho$ and $\sigma$. Two different states can have the same spectrum.

### Implementation

The Python code with this page computes the trace distance from the eigenvalues of $\rho - \sigma$, builds the optimal projector $P_+$, and evaluates the Helstrom success probability. Its tests check the Bloch formula, the commuting case, the metric properties, the pure-state formula, that $P_+$ attains the distance and random projectors do not exceed it, the contraction under partial traces and random channels, the non-example for the Hilbert-Schmidt distance, and the Fuchs-van de Graaf inequalities on random states.

## Related definitions

- [Total variation distance](/total-variation-distance/): the classical distance that the trace distance extends.
- [Fidelity](/fidelity/): a measure of overlap, related to $D$ by the Fuchs-van de Graaf inequalities.
- [State discrimination problem](/state-discrimination-problem/): the task whose optimal success probability is given by the trace norm.
- [Quantum channel](/quantum-channel/): the maps under which $D$ cannot grow, and the diamond norm, the distance between channels.
- [Quantum state tomography](/quantum-state-tomography/): its accuracy is usually stated in trace distance.
- [Matrix norms](/matrix-norms/): the trace norm is the Schatten 1-norm.

### History

Helstrom found the optimal measurement for two states, and the trace norm bound on its success, in his work on quantum detection theory in the 1960s and 1970s. Fuchs and van de Graaf proved in 1999 the inequalities that relate the trace distance and the fidelity, in a study of distinguishability measures for quantum cryptography.

## References
