---
tag: N6ND1W
kind: definition
slug: fidelity
name: Fidelity (quantum)
aliases:
- quantum fidelity
- Uhlmann fidelity
area: quantum/quantum-primitives
level: advanced
summary: "F(rho, sigma) = Tr sqrt(sqrt(rho) sigma sqrt(rho)), the largest overlap of purifications of two states. It is |<psi|phi>| for pure states; some authors use its square."
prereqs: [density-matrix, mixed-state, partial-trace]
see_also: [trace-distance, swap-test, quantum-channel, quantum-state-tomography, state-discrimination-problem, singular-value-decomposition, bloch-sphere, quantum-error-correction]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 9.2.2 (fidelity, with Uhlmann's theorem) and Section 9.2.3 (relationships between distance measures)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 3.2 (the fidelity function, in the same unsquared convention)
  - paper: doi:10.1016/0034-4877(76)90060-4
    title: "A. Uhlmann, The \"transition probability\" in the state space of a *-algebra, Reports on Mathematical Physics 9(2), 1976"
    locator: pp. 273 to 279
  - paper: doi:10.1080/09500349414552171
    title: Richard Jozsa, Fidelity for mixed quantum states, Journal of Modern Optics 41(12), 1994
    locator: pp. 2315 to 2323
  - paper: doi:10.1109/18.761271
    title: Christopher A. Fuchs and Jeroen van de Graaf, Cryptographic distinguishability measures for quantum-mechanical states, IEEE Transactions on Information Theory 45(4), 1999
    locator: pp. 1216 to 1227
---

The fidelity of two [density matrices](/density-matrix/) $\rho$ and $\sigma$ measures how much they overlap. **This page uses the convention of Nielsen and Chuang and of Watrous,**

$$F(\rho, \sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\,\sqrt\rho},$$

which is $|\langle\psi|\phi\rangle|$ for pure states. Uhlmann's "transition probability" and Jozsa's fidelity are the square $F^2$, which is $|\langle\psi|\phi\rangle|^2$ for pure states. Both conventions are common, so check which one a source uses before you compare numbers. Uhlmann's theorem gives the meaning of $F$: it is the largest overlap of two pure states, one that purifies $\rho$ and one that purifies $\sigma$.

## Definition

For density matrices $\rho, \sigma$ on $\mathbb{C}^d$, with $\sqrt\rho$ the positive square root,

$$F(\rho, \sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\,\sqrt\rho} = \bigl\|\sqrt\rho\,\sqrt\sigma\bigr\|_1.$$

The two forms agree: with $M = \sqrt\rho\sqrt\sigma$, $M M^\dagger = \sqrt\rho\,\sigma\sqrt\rho$, and the trace norm $\|M\|_1$ is the sum of the [singular values](/singular-value-decomposition/) of $M$, which is $\operatorname{Tr}\sqrt{MM^\dagger}$. Since $M^\dagger M = \sqrt\sigma\,\rho\sqrt\sigma$ has the same nonzero eigenvalues, $F(\rho, \sigma) = F(\sigma, \rho)$.

**Special cases.**

- Pure states: $F(|\psi\rangle\langle\psi|, |\phi\rangle\langle\phi|) = |\langle\psi|\phi\rangle|$, because $\sqrt{|\psi\rangle\langle\psi|} = |\psi\rangle\langle\psi|$ and $|\psi\rangle\langle\psi|\phi\rangle\langle\phi|\psi\rangle\langle\psi| = |\langle\psi|\phi\rangle|^2\,|\psi\rangle\langle\psi|$.
- One pure state: $F(|\psi\rangle\langle\psi|, \sigma) = \sqrt{\langle\psi|\sigma|\psi\rangle}$, by the same computation.
- Commuting states with eigenvalues $p_i$ and $q_i$ in one basis: $F = \sum_i \sqrt{p_i q_i}$, the Bhattacharyya coefficient of the two distributions.
- One qubit: $F^2 = \operatorname{Tr}(\rho\sigma) + 2\sqrt{\det\rho\,\det\sigma}$. *Proof.* Let $A = \sqrt\rho\,\sigma\sqrt\rho$, a $2 \times 2$ positive matrix with eigenvalues $a, b$. Then $(\operatorname{Tr}\sqrt{A})^2 = a + b + 2\sqrt{ab} = \operatorname{Tr} A + 2\sqrt{\det A}$, and $\operatorname{Tr} A = \operatorname{Tr}(\rho\sigma)$, $\det A = \det\rho\det\sigma$. $\square$

### Uhlmann's theorem

Let $|\Omega\rangle = \sum_{i=1}^{d}|i\rangle|i\rangle$ on $\mathbb{C}^d \otimes \mathbb{C}^d$. Then $\langle\Omega|(A \otimes B)|\Omega\rangle = \sum_{i,j} A_{ij}B_{ij} = \operatorname{Tr}(AB^{T})$, and $|\psi_\rho\rangle = (\sqrt\rho \otimes I)|\Omega\rangle$ is a purification of $\rho$, because $\operatorname{Tr}_R |\psi_\rho\rangle\langle\psi_\rho| = \sqrt\rho\,(\sum_i |i\rangle\langle i|)\sqrt\rho = \rho$.

**Theorem (Uhlmann 1976).** $F(\rho, \sigma) = \max |\langle\psi|\phi\rangle|$, where the maximum is over all purifications $|\psi\rangle$ of $\rho$ and $|\phi\rangle$ of $\sigma$ on $\mathbb{C}^d \otimes \mathbb{C}^d$.

**Proof.** By the uniqueness of purifications on the [mixed state](/mixed-state/) page, every purification of $\rho$ on this space is $(\sqrt\rho \otimes U)|\Omega\rangle$ for a unitary $U$, and every purification of $\sigma$ is $(\sqrt\sigma \otimes V)|\Omega\rangle$. So

$$\langle\psi|\phi\rangle = \langle\Omega|\bigl(\sqrt\rho\sqrt\sigma \otimes U^\dagger V\bigr)|\Omega\rangle = \operatorname{Tr}(M W), \qquad M = \sqrt\rho\sqrt\sigma,\ W = (U^\dagger V)^{T},$$

and $W$ ranges over all unitaries. Write the singular value decomposition $M = \sum_k s_k |a_k\rangle\langle b_k|$. Then $|\operatorname{Tr}(MW)| = |\sum_k s_k\langle b_k|W|a_k\rangle| \le \sum_k s_k = \|M\|_1$, since $|\langle b_k|W|a_k\rangle| \le 1$. The unitary $W = \sum_k |b_k\rangle\langle a_k|$ gives equality. $\square$

A larger reference system gives the same maximum, because the extra dimensions only add an isometry on the reference.

### Properties

- **Range.** $0 \le F \le 1$. $F = 1$ exactly when $\rho = \sigma$, and $F = 0$ exactly when $\rho$ and $\sigma$ have orthogonal supports.
- **Channels do not decrease it.** For a [quantum channel](/quantum-channel/) $\Phi$, $F(\Phi(\rho), \Phi(\sigma)) \ge F(\rho, \sigma)$. *Proof.* Take purifications with $|\langle\psi|\phi\rangle| = F(\rho, \sigma)$, and apply the Stinespring isometry $V$ of $\Phi$ to the system part. The results $(V \otimes I)|\psi\rangle$ and $(V \otimes I)|\phi\rangle$ have the same overlap, and they purify $\Phi(\rho)$ and $\Phi(\sigma)$ with the environment added to the reference. By Uhlmann's theorem, $F(\Phi(\rho), \Phi(\sigma))$ is at least that overlap. $\square$
- **Multiplicative.** $F(\rho_1 \otimes \rho_2, \sigma_1 \otimes \sigma_2) = F(\rho_1, \sigma_1)\,F(\rho_2, \sigma_2)$, because square roots and trace norms factor over tensor products.
- **Unitary invariance.** $F(U\rho U^\dagger, U\sigma U^\dagger) = F(\rho, \sigma)$.
- **Concavity.** $F$ is jointly concave in its two arguments.

### Fidelity and trace distance

**Theorem (Fuchs and van de Graaf 1999).** With $D$ the [trace distance](/trace-distance/) and $F$ in the convention of this page,

$$1 - F(\rho, \sigma) \le D(\rho, \sigma) \le \sqrt{1 - F(\rho, \sigma)^2}.$$

**Proof of the right inequality.** Take purifications with $|\langle\psi|\phi\rangle| = F$. The trace distance of pure states is $\sqrt{1 - |\langle\psi|\phi\rangle|^2}$, and the partial trace does not increase the trace distance, so $D(\rho, \sigma) \le \sqrt{1 - F^2}$. $\square$

**The left inequality.** The fidelity is the smallest Bhattacharyya coefficient $\sum_m\sqrt{p_m q_m}$ of the outcome distributions $p_m = \operatorname{Tr}(E_m\rho)$, $q_m = \operatorname{Tr}(E_m\sigma)$ over all measurements $\{E_m\}$. For one such optimal measurement, $1 - F = \frac12\sum_m(\sqrt{p_m} - \sqrt{q_m})^2 \le \frac12\sum_m|p_m - q_m| \le D$, where the middle step uses $(\sqrt p - \sqrt q)^2 \le |\sqrt p - \sqrt q|(\sqrt p + \sqrt q) = |p - q|$ and the last step is the measurement form of $D$.

For pure states the right inequality is an equality. In the squared convention $F_J = F^2$ the inequalities read $1 - \sqrt{F_J} \le D \le \sqrt{1 - F_J}$. To use one form with the other convention is a common error.

## Examples and non-examples

**$|0\rangle$ and $|+\rangle$.** $F = |\langle 0|+\rangle| = 1/\sqrt2 \approx 0.7071$, and $F^2 = 1/2$. The trace distance is also $0.7071$, so the upper Fuchs-van de Graaf bound $\sqrt{1 - 1/2}$ is attained, and the lower bound $1 - 0.7071 = 0.2929$ is far below.

**A mixed pair.** $\rho = \operatorname{diag}(3/4, 1/4)$ and $\sigma = I/2$ commute, so $F = \sqrt{3/8} + \sqrt{1/8} \approx 0.6124 + 0.3536 = 0.9659$. The qubit formula agrees: $\operatorname{Tr}(\rho\sigma) = 1/2$, $\det\rho\det\sigma = \frac{3}{16}\cdot\frac14$, and $F^2 = \frac12 + 2\sqrt{3/64} \approx 0.9330 = 0.9659^2$. The trace distance is $1/4$, and indeed $1 - 0.9659 = 0.0341 \le 0.25 \le \sqrt{1 - 0.9330} = 0.2588$.

**Copies.** For $n$ copies, $F(\rho^{\otimes n}, \sigma^{\otimes n}) = F(\rho, \sigma)^n$. So for $|0\rangle$ and $|+\rangle$, $n = 20$ copies have fidelity $2^{-10} \approx 0.001$, and the lower bound gives a trace distance of at least $0.999$.

**Non-examples.**

- $\operatorname{Tr}(\rho\sigma)$ is not the fidelity of mixed states. For $\rho = \sigma = I/2$ it is $1/2$, but $F = 1$. It equals $F^2$ only when one of the states is pure. This quantity is what the [swap test](/swap-test/) estimates.
- $\operatorname{Tr}(\sqrt\rho\sqrt\sigma)$, the affinity, is not the fidelity. It is the trace of $M = \sqrt\rho\sqrt\sigma$, while $F$ is the trace norm of $M$, so it is at most $F$, with equality when $\rho$ and $\sigma$ commute.

### Common errors

- **Mixing conventions.** A fidelity of 0.99 in the squared convention is about 0.995 in the unsquared one. Error thresholds, Fuchs-van de Graaf bounds and gate fidelities change with the convention.
- **Infidelity.** $1 - F$ and $1 - F^2$ differ by a factor close to 2 when $F$ is near 1, since $1 - F^2 = (1 - F)(1 + F)$.
- **Numerical square roots.** For states of low rank, the eigenvalues near zero make $\sqrt\rho$ lose about half of the digits. Use a tolerance near $10^{-7}$ in double precision, or compute through the singular values of $\sqrt\rho\sqrt\sigma$.

### Implementation

The Python code with this page computes $F$ from the definition, from the trace norm of $\sqrt\rho\sqrt\sigma$, and from the formulas for pure, commuting and qubit states, and it builds two purifications of a state. Its tests check all of these against one another on random states, check Uhlmann's theorem (no purification overlap exceeds $F$, and the polar unitary of $\sqrt\rho\sqrt\sigma$ attains it), the increase under the partial trace, multiplicativity, and the Fuchs-van de Graaf inequalities on random states of random rank.

## Related definitions

- [Trace distance](/trace-distance/): the other main distance between states, bounded above and below by the fidelity.
- [Mixed state](/mixed-state/): purifications, and their uniqueness up to a unitary, which Uhlmann's theorem uses.
- [Swap test](/swap-test/): a circuit that estimates $\operatorname{Tr}(\rho\sigma)$, which is $F^2$ when one state is pure.
- [Quantum channel](/quantum-channel/): fidelity does not decrease under channels.
- [Quantum state tomography](/quantum-state-tomography/): its accuracy is often stated as an infidelity.
- [Quantum error correction](/quantum-error-correction/): code performance is often given as the fidelity of the corrected state.

### History

Uhlmann introduced the "transition probability" $(\operatorname{Tr}|\sqrt\rho\sqrt\sigma|)^2$ between states of a *-algebra in 1976 and proved that it is the largest transition probability between purifications. Jozsa named it the fidelity in 1994 and gave a list of axioms for it, in the squared convention. Nielsen and Chuang use the square root of that quantity, and Fuchs and van de Graaf related it to the trace distance in 1999.

## References
