---
tag: YN47TX
kind: problem
slug: state-discrimination-problem
name: State discrimination problem
aliases:
- Helstrom measurement problem
area: quantum/quantum-primitives
level: advanced
summary: Given a state drawn from a known list with known priors, find the measurement that names it with the highest success probability, or one that never errs but may abstain.
prereqs: [quantum-measurement, trace-distance, density-matrix]
see_also: [trace-distance, fidelity, semidefinite-programming, no-cloning-theorem, swap-test, quantum-state-tomography, key-distribution-problem, communication-complexity]
sources:
  - book: isbn:9780123400505
    title: Carl W. Helstrom, Quantum Detection and Estimation Theory, Mathematics in Science and Engineering 123, Academic Press, 1976
    locator: the chapters on the choice between two hypotheses and among M hypotheses (the optimal detection operators and the minimum error probability)
  - paper: doi:10.1007/BF01007479
    title: Carl W. Helstrom, Quantum detection and estimation theory, Journal of Statistical Physics 1(2), pages 231 to 252, 1969
    locator: the binary decision between two density operators and the projector on the positive part of their weighted difference
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 3.1 (discrimination of quantum states), Theorem 3.4 (the Holevo-Helstrom theorem), and the semidefinite program for several states
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.2.4 (distinguishing quantum states), Section 2.2.6 (the POVM example for |0> and |+>) and Section 9.2 (trace distance and fidelity)
  - paper: doi:10.1109/TIT.1975.1055351
    title: Horace P. Yuen, Robert S. Kennedy and Melvin Lax, Optimum testing of multiple hypotheses in quantum detection theory, IEEE Transactions on Information Theory 21(2), pages 125 to 134, 1975
    locator: the linear-programming formulation over operators and the necessary and sufficient conditions for an optimal measurement
  - paper: doi:10.1080/09500349414552221
    title: Paul Hausladen and William K. Wootters, A 'pretty good' measurement for distinguishing quantum states, Journal of Modern Optics 41(12), pages 2385 to 2390, 1994
    locator: the definition of the square-root measurement
  - paper: doi:10.1063/1.1459754
    title: Howard Barnum and Emanuel Knill, Reversing quantum dynamics with near-optimal quantum and classical fidelity, Journal of Mathematical Physics 43(5), pages 2097 to 2106, 2002
    locator: the bound that the square-root measurement succeeds with at least the square of the optimal probability
  - paper: doi:10.1016/0375-9601(87)90222-2
    title: I. D. Ivanovic, How to differentiate between non-orthogonal states, Physics Letters A 123(6), pages 257 to 259, 1987
    locator: the measurement that never errs on two non-orthogonal pure states
  - paper: doi:10.1016/0375-9601(88)90840-7
    title: D. Dieks, Overlap and distinguishability of quantum states, Physics Letters A 126(5-6), pages 303 to 306, 1988
    locator: the optimal success probability 1 - |<psi|phi>| of unambiguous discrimination
  - paper: doi:10.1016/0375-9601(88)91034-1
    title: Asher Peres, How to differentiate between non-orthogonal states, Physics Letters A 128(1-2), page 19, 1988
    locator: the proof that 1 - |<psi|phi>| is optimal
  - paper: doi:10.1103/PhysRevLett.98.160501
    title: K. M. R. Audenaert, J. Calsamiglia, R. Muñoz-Tapia, E. Bagan, Ll. Masanes, A. Acín and F. Verstraete, Discriminating states, the quantum Chernoff bound, Physical Review Letters 98, 160501, 2007
    locator: the error exponent for many copies and the inequality Tr(A^s B^(1-s)) >= Tr(A + B - |A - B|)/2
  - paper: doi:10.1109/18.761271
    title: Christopher A. Fuchs and Jeroen van de Graaf, Cryptographic distinguishability measures for quantum-mechanical states, IEEE Transactions on Information Theory 45(4), pages 1216 to 1227, 1999
    locator: the inequalities between the trace distance and the fidelity
  - paper: doi:10.1103/PhysRevLett.85.4972
    title: Jonathan Walgate, Anthony J. Short, Lucien Hardy and Vlatko Vedral, Local distinguishability of multipartite orthogonal quantum states, Physical Review Letters 85(23), pages 4972 to 4975, 2000
    locator: any two orthogonal multipartite pure states can be told apart with local operations and classical communication
  - paper: doi:10.1103/PhysRevLett.68.3121
    title: Charles H. Bennett, Quantum cryptography using any two nonorthogonal states, Physical Review Letters 68(21), pages 3121 to 3124, 1992
    locator: the B92 protocol, where the receiver uses a measurement that never errs but sometimes fails
  - paper: doi:10.1080/00107510010002599
    title: Anthony Chefles, Quantum state discrimination, Contemporary Physics 41(6), pages 401 to 424, 2000
    locator: review of minimum-error and unambiguous discrimination, including the condition of linear independence
  - paper: doi:10.1364/AOP.1.000238
    title: Stephen M. Barnett and Sarah Croke, Quantum state discrimination, Advances in Optics and Photonics 1(2), pages 238 to 278, 2009
    locator: review of the minimum-error, unambiguous and intermediate strategies, with the trine example
  - paper: doi:10.1088/1751-8113/48/8/083001
    title: Joonwoo Bae and Leong-Chuan Kwek, Quantum state discrimination and its applications, Journal of Physics A 48(8), 083001, 2015
    locator: review of the semidefinite programs and of the applications in cryptography and communication
---

In the state discrimination problem, a system is prepared in one of $N$ known states $\rho_1, \dots, \rho_N$, the state $\rho_k$ with a known prior probability $p_k$, and an observer must guess $k$ from one measurement. In the *minimum-error* version the observer wants the highest probability of a correct guess. For two states Helstrom found the answer in closed form: the best success probability is $\tfrac12\bigl(1 + \|p\rho - (1-p)\sigma\|_1\bigr)$, and a projective measurement reaches it. In the *unambiguous* version the observer must never be wrong but may say "I do not know"; for two pure states with equal priors the best success probability is $1 - |\langle\psi|\phi\rangle|$. Non-orthogonal states can never be told apart with certainty, and this fact is behind the [no-cloning theorem](/no-cloning-theorem/), quantum key distribution, and the limits of [state tomography](/quantum-state-tomography/).

**Notation.** A measurement is a POVM $\{E_k\}$: Hermitian matrices with $E_k \succeq 0$ and $\sum_k E_k = I$ ([quantum measurement](/quantum-measurement/)). For two states, $\rho$ has prior $p$ and $\sigma$ has prior $1 - p$, and $\Gamma = p\rho - (1-p)\sigma$. $\|A\|_1$ is the trace norm, the sum of the absolute values of the eigenvalues for a Hermitian $A$, and $D(\rho, \sigma) = \tfrac12\|\rho - \sigma\|_1$ is the [trace distance](/trace-distance/). $F(\rho, \sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}$ is the [fidelity](/fidelity/), so $F = |\langle\psi|\phi\rangle|$ for pure states. $s = \langle\psi|\phi\rangle$ is the overlap of two pure states.

## In plain words

Someone gives you a small quantum system and tells you that it was made in one of a few known ways, with known odds. You may look at it once, and then you must say which way it was made. If the possible states are fully different, one well-chosen look always gives the right answer. If they overlap, no look can be sure, and the question is how to look so that you are right as often as possible.

There is a second game. You must never give a wrong answer, but you are allowed to say "I do not know". Then the question is how often you can give a sure answer.

For two possible states both games have exact answers, and the answers depend only on how much the two states overlap.

## Definition

**Input.** A list of density matrices $\rho_1, \dots, \rho_N$ on $\mathbb{C}^d$ and a probability vector $(p_1, \dots, p_N)$.

**Minimum-error discrimination.** Find a POVM $\{E_1, \dots, E_N\}$ that maximizes the success probability

$$P_{\mathrm{succ}}(E) = \sum_{k=1}^{N} p_k \operatorname{Tr}(E_k \rho_k).$$

The outcome $k$ means the guess "the state was $\rho_k$". Any measurement with more outcomes, followed by any guessing rule, gives the same success as the POVM in which $E_k$ is the sum of the elements of the outcomes that lead to the guess $k$. So the maximum over $N$-outcome POVMs is the best over all strategies. The value $P_{\mathrm{opt}}$ is the optimum, and $P_{\mathrm{err}} = 1 - P_{\mathrm{opt}}$.

**Unambiguous discrimination.** Find a POVM $\{E_1, \dots, E_N, E_?\}$ with $\operatorname{Tr}(E_k \rho_j) = 0$ for all $j \ne k$, so that a guess $k$ is never wrong, that maximizes $\sum_k p_k \operatorname{Tr}(E_k \rho_k)$. The outcome $?$ is the answer "I do not know".

## Variants

- **Two states.** The case $N = 2$ has the closed-form answers of the Bounds section, for mixed states (minimum error) and for pure states (both versions).
- **Many copies.** The observer gets $\rho_k^{\otimes n}$. The error falls exponentially in $n$, and the quantum Chernoff bound gives the exact rate (see Bounds).
- **Asymmetric testing.** One type of error must stay below a fixed bound, and the other is minimized. This is the quantum form of hypothesis testing; for many copies the best exponent of the second error is the quantum relative entropy of the two states.
- **Intermediate strategies.** The rate of "I do not know" is fixed at a value between zero and the unambiguous optimum, and the error is minimized. Both main versions are end points of this family (Barnett and Croke 2009).
- **Local discrimination.** The state is shared by several parties who can only use local operations and classical communication (LOCC). Walgate, Short, Hardy and Vedral (2000) proved that any two orthogonal multipartite pure states can be told apart perfectly with LOCC. For more than two states, or for mixed states, LOCC can be strictly weaker than a joint measurement.
- **Unknown or partly known states.** In state comparison or programmable discrimination the candidate states are given as quantum systems, not as matrices. These problems are related to the [swap test](/swap-test/).

## Examples

**$|0\rangle$ or $|+\rangle$, equal priors.** The overlap is $s = 1/\sqrt2$. The Helstrom measurement is the orthonormal basis $\cos\frac{\pi}{8}|0\rangle - \sin\frac{\pi}{8}|1\rangle$ (answer $|0\rangle$) and $\sin\frac{\pi}{8}|0\rangle + \cos\frac{\pi}{8}|1\rangle$ (answer $|+\rangle$). The two basis vectors lie at the same angle, $\pi/8$, from their own state, so each state gives the right answer with probability $\cos^2\frac{\pi}{8} = \tfrac12(1 + 1/\sqrt2) \approx 0.8536$. The simple strategy "measure in the computational basis, answer $|0\rangle$ on 0 and $|+\rangle$ on 1" succeeds with probability $\tfrac12 \cdot 1 + \tfrac12 \cdot \tfrac12 = 0.75$.

**Unequal priors.** With $p = 0.8$ for $|0\rangle$, the formula $\tfrac12\bigl(1 + \sqrt{1 - 4p(1-p)|s|^2}\bigr)$ gives $\tfrac12(1 + \sqrt{0.68}) \approx 0.9123$. Always guessing $|0\rangle$ gives $0.8$, so the measurement still adds information.

**Many copies.** With $n$ copies of $|0\rangle$ or $|+\rangle$ and equal priors, the overlap is $s^n$, so $P_{\mathrm{err}} = \tfrac12\bigl(1 - \sqrt{1 - 2^{-n}}\bigr)$.

| $n$ | 1 | 2 | 5 | 10 |
|---|---|---|---|---|
| $P_{\mathrm{err}}$ | 0.1464 | 0.0670 | 0.00787 | 0.000244 |

For large $n$ this is close to $2^{-n}/4$, so each copy halves the error, as the Chernoff exponent $-\log_2 |s|^2 = 1$ bit per copy says.

**Two mixed qubit states.** Take $\rho = \operatorname{diag}(0.8, 0.2)$ (Bloch vector $(0, 0, 0.6)$) and $\sigma$ with Bloch vector $(0.3, 0, 0)$, with equal priors. For qubits $D(\rho, \sigma)$ is half the distance of the Bloch vectors, here $\tfrac12\sqrt{0.45} \approx 0.3354$, so $P_{\mathrm{opt}} \approx 0.6677$. The fidelity is $F \approx 0.9389$, and the fidelity bounds of the Bounds section give $0.5305 \le P_{\mathrm{opt}} \le 0.6721$.

**Unambiguous, $|0\rangle$ or $|+\rangle$.** The POVM $E_0 = \frac{1}{1 + 1/\sqrt2}|-\rangle\langle -|$, $E_+ = \frac{1}{1 + 1/\sqrt2}|1\rangle\langle 1|$ and $E_? = I - E_0 - E_+$ never errs, because $E_0$ is orthogonal to $|+\rangle$ and $E_+$ to $|0\rangle$. It gives a sure answer with probability $1 - 1/\sqrt2 \approx 0.2929$ and "I do not know" otherwise. This is the example of Nielsen and Chuang, Section 2.2.6.

**Three trine states.** The states $|\psi_k\rangle = \cos\frac{2\pi k}{3}|0\rangle + \sin\frac{2\pi k}{3}|1\rangle$ for $k = 0, 1, 2$, each with prior $1/3$, lie at 120 degrees on a great circle of the Bloch sphere. The POVM $E_k = \tfrac23|\psi_k\rangle\langle\psi_k|$ sums to $I$ and succeeds with probability $\tfrac23$. No measurement does better, by the bound $P_{\mathrm{opt}} \le d/N$ for $N$ equiprobable pure states in dimension $d$. The three states are linearly dependent in $\mathbb{C}^2$, so they cannot be discriminated unambiguously with a positive success probability for each state.

**Non-examples.** If $\rho$ and $\sigma$ have orthogonal supports, for example $|0\rangle$ and $|1\rangle$, the problem is classical: the projector on the support of $\rho$ succeeds with probability 1. If $\rho = \sigma$, no measurement helps, and the best strategy is to guess the more likely state, with success $\max(p, 1-p)$.

## Known algorithms

- **Helstrom measurement (two states, 1969 and 1976).** Compute the eigendecomposition of $\Gamma = p\rho - (1-p)\sigma$ and measure the projector $P_+$ on its eigenvectors with positive eigenvalues against $I - P_+$. The cost is one Hermitian [eigenvalue problem](/eigenvalue-problem/) of size $d$, $O(d^3)$ arithmetic operations.
- **Semidefinite programming (any $N$).** The minimum-error problem is a [semidefinite program](/semidefinite-programming/) in the $N$ matrix variables $E_k$, and the unambiguous problem is one too. Interior-point solvers give $P_{\mathrm{opt}}$ to any accuracy in time polynomial in $N$ and $d$. Holevo (1973) and Yuen, Kennedy and Lax (1975) gave the conditions for a POVM to be optimal: with $Y = \sum_k p_k E_k\rho_k$, the POVM is optimal if and only if $Y$ is Hermitian and $Y \succeq p_j\rho_j$ for every $j$.
- **Square-root measurement (pretty good measurement).** With $\bar\rho = \sum_k p_k\rho_k$, take $E_k = \bar\rho^{-1/2}\,p_k\rho_k\,\bar\rho^{-1/2}$ on the support of $\bar\rho$. Hausladen and Wootters (1994) named it. It is optimal for symmetric sets, such as the trine states and two pure states with equal priors, and Barnum and Knill (2002) proved that it always succeeds with probability at least $P_{\mathrm{opt}}^2$. For $|0\rangle$ and $|+\rangle$ with equal priors, $\bar\rho$ has the eigenvalues $0.1464$ and $0.8536$, and the measurement is the Helstrom basis above.
- **Ivanovic-Dieks-Peres measurement (unambiguous, two pure states, 1987 and 1988).** Take $E_\psi = \frac{1}{1 + |s|}|\phi^\perp\rangle\langle\phi^\perp|$, $E_\phi = \frac{1}{1 + |s|}|\psi^\perp\rangle\langle\psi^\perp|$ and $E_? = I - E_\psi - E_\phi$ in the span of the two states, where $|\phi^\perp\rangle$ is the unit vector of the span orthogonal to $|\phi\rangle$. It reaches $1 - |s|$ with equal priors.
- **Unambiguous discrimination of $N$ pure states.** It is possible with a positive success probability for every state if and only if the states are linearly independent; the optimal POVM comes from a semidefinite program (Chefles 2000).

The Python code with this page computes the Helstrom value from the eigenvalues of $\Gamma$, builds the measurement $P_+$, and builds the Ivanovic-Dieks-Peres POVM for two qubit states. The tests check the value $\cos^2(\pi/8)$ for $|0\rangle$ and $|+\rangle$, the identical and orthogonal cases, the pure-state formula on 100 random pairs with random priors, that $P_+$ reaches the value, and a grid search over projective measurements on 10 random pairs of mixed states: no grid point does better than the Helstrom value, and the best grid point is within $2 \cdot 10^{-3}$ of it. They also check that the unambiguous POVM is a valid POVM, never errs, and succeeds with probability $1 - |s|$ on 51 pairs, and that the trine measurement gives $\tfrac23$. The seeds are fixed.

## Bounds

**Theorem 1 (Holevo-Helstrom).** For two states with priors $p$ and $1 - p$,

$$P_{\mathrm{opt}} = \tfrac12\bigl(1 + \|p\rho - (1-p)\sigma\|_1\bigr),$$

and the measurement $\{P_+, I - P_+\}$, with $P_+$ the projector on the positive eigenspace of $\Gamma$, reaches it. For $p = \tfrac12$ the value is $\tfrac12\bigl(1 + D(\rho, \sigma)\bigr)$.

*Proof.* A two-outcome POVM is $\{E, I - E\}$ with $0 \preceq E \preceq I$, and

$$P_{\mathrm{succ}} = p\operatorname{Tr}(E\rho) + (1-p)\operatorname{Tr}\bigl((I - E)\sigma\bigr) = (1 - p) + \operatorname{Tr}(E\Gamma).$$

Write $\Gamma = \Gamma_+ - \Gamma_-$ with $\Gamma_\pm \succeq 0$ on orthogonal eigenspaces. Then $\operatorname{Tr}(E\Gamma_-) \ge 0$ because $E$ and $\Gamma_-$ are positive semidefinite, and $\operatorname{Tr}(E\Gamma_+) \le \operatorname{Tr}\Gamma_+$ because $E \preceq I$. So $\operatorname{Tr}(E\Gamma) \le \operatorname{Tr}\Gamma_+$, with equality for $E = P_+$. Since $\operatorname{Tr}\Gamma_+ - \operatorname{Tr}\Gamma_- = \operatorname{Tr}\Gamma = 2p - 1$ and $\operatorname{Tr}\Gamma_+ + \operatorname{Tr}\Gamma_- = \|\Gamma\|_1$, $\operatorname{Tr}\Gamma_+ = \tfrac12(\|\Gamma\|_1 + 2p - 1)$. Then $P_{\mathrm{opt}} = 1 - p + \tfrac12(\|\Gamma\|_1 + 2p - 1) = \tfrac12(1 + \|\Gamma\|_1)$. $\square$

**Theorem 2 (pure states).** For pure states $|\psi\rangle$ and $|\phi\rangle$ with overlap $s$,

$$P_{\mathrm{opt}} = \tfrac12\Bigl(1 + \sqrt{1 - 4p(1-p)|s|^2}\Bigr).$$

*Proof.* $\Gamma = p|\psi\rangle\langle\psi| - (1-p)|\phi\rangle\langle\phi|$ acts in the span of the two vectors and is zero outside it. Choose an orthonormal basis of the span and phases so that $|\psi\rangle = (1, 0)$ and $|\phi\rangle = (|s|, c)$ with $c = \sqrt{1 - |s|^2}$. Then

$$\Gamma = \begin{pmatrix} p - (1-p)|s|^2 & -(1-p)|s|c \\ -(1-p)|s|c & -(1-p)c^2 \end{pmatrix},$$

with trace $2p - 1$ and determinant $-(1-p)c^2\bigl(p - (1-p)|s|^2\bigr) - (1-p)^2|s|^2c^2 = -p(1-p)c^2$. The determinant is not positive, so the eigenvalues $\lambda_1 \ge 0 \ge \lambda_2$ have opposite signs or one is zero, and $\|\Gamma\|_1 = \lambda_1 - \lambda_2 = \sqrt{(\lambda_1 + \lambda_2)^2 - 4\lambda_1\lambda_2} = \sqrt{(2p-1)^2 + 4p(1-p)(1 - |s|^2)}$. Since $(2p - 1)^2 + 4p(1-p) = 1$, this is $\sqrt{1 - 4p(1-p)|s|^2}$. Theorem 1 gives the result. $\square$

**Corollary 3 (no perfect discrimination).** For $0 < p < 1$, $P_{\mathrm{opt}} = 1$ if and only if $\rho$ and $\sigma$ have orthogonal supports. In particular, two pure states can be told apart with certainty only if they are orthogonal.

*Proof.* If $P_{\mathrm{succ}}(E) = 1$, then $\operatorname{Tr}(E\rho) = 1$ and $\operatorname{Tr}(E\sigma) = 0$. Since $0 \preceq E \preceq I$, the first gives $(I - E)\rho = 0$, so the support of $\rho$ is in the eigenspace of $E$ for the eigenvalue 1, and the second gives $E\sigma = 0$, so the support of $\sigma$ is in the kernel of $E$. These two spaces are orthogonal. Conversely, the projector on the support of $\rho$ succeeds with probability 1. $\square$

**Theorem 4 (fidelity bounds).** For two states with priors $p$ and $1 - p$,

$$\tfrac12\Bigl(1 - \sqrt{1 - 4p(1-p)F(\rho, \sigma)^2}\Bigr) \le P_{\mathrm{err}} \le \sqrt{p(1-p)}\,F(\rho, \sigma).$$

The lower bound is an equality for pure states, where $F = |s|$.

*Proof of the lower bound.* By Uhlmann's theorem ([fidelity](/fidelity/)) there are purifications $|\psi\rangle$ of $\rho$ and $|\phi\rangle$ of $\sigma$ on a larger space with $|\langle\psi|\phi\rangle| = F(\rho, \sigma)$. For a Hermitian $X$, $\|X\|_1 = \max\{\operatorname{Tr}(MX) : -I \preceq M \preceq I\}$, and $\operatorname{Tr}(M \operatorname{Tr}_R X) = \operatorname{Tr}((M \otimes I)X)$, so the trace norm cannot grow under the partial trace. Hence $\|p\rho - (1-p)\sigma\|_1 \le \|p|\psi\rangle\langle\psi| - (1-p)|\phi\rangle\langle\phi|\|_1 = \sqrt{1 - 4p(1-p)F^2}$ by Theorem 2, and Theorem 1 gives the bound. In words: telling the purifications apart is at least as easy as telling the states apart. $\square$

*The upper bound* follows from the inequality $\operatorname{Tr}(A^{t}B^{1-t}) \ge \tfrac12\operatorname{Tr}(A + B - |A - B|)$ for $A, B \succeq 0$ and $0 \le t \le 1$ of Audenaert et al. (2007), with $A = p\rho$, $B = (1-p)\sigma$ and $t = \tfrac12$: the right side is $P_{\mathrm{err}}$ by Theorem 1, and $\operatorname{Tr}(\sqrt\rho\sqrt\sigma) \le \|\sqrt\rho\sqrt\sigma\|_1 = F$. For $p = \tfrac12$ the two bounds give the Fuchs-van de Graaf inequalities $1 - F \le D \le \sqrt{1 - F^2}$.

**Theorem 5 (many copies, quantum Chernoff bound).** For fixed priors $0 < p < 1$, the minimum error for $n$ copies satisfies

$$\lim_{n \to \infty} -\tfrac1n \log P_{\mathrm{err}}(\rho^{\otimes n}, \sigma^{\otimes n}) = -\log \min_{0 \le t \le 1} \operatorname{Tr}(\rho^t\sigma^{1-t}).$$

This is from Audenaert et al. (2007). For pure states $\rho^t = \rho$ and $\sigma^{1-t} = \sigma$ for $0 < t < 1$, so the exponent is $-\log|s|^2$, which agrees with Theorem 2 since $\tfrac12(1 - \sqrt{1 - x}) \approx x/4$ for small $x$.

**Theorem 6 (several states, weak duality).** For any Hermitian $Y$ with $Y \succeq p_k\rho_k$ for all $k$, $P_{\mathrm{opt}} \le \operatorname{Tr} Y$. The minimum of $\operatorname{Tr}Y$ over such $Y$ equals $P_{\mathrm{opt}}$.

*Proof of the inequality.* For any POVM, $\operatorname{Tr}\bigl(E_k(Y - p_k\rho_k)\bigr) \ge 0$ because both factors are positive semidefinite, so $\sum_k p_k\operatorname{Tr}(E_k\rho_k) \le \sum_k \operatorname{Tr}(E_kY) = \operatorname{Tr}Y$. $\square$ The equality is strong duality of the semidefinite program; it holds because the primal problem has a strictly feasible point, $E_k = I/N$. With $Y = \max_k p_k\lambda_{\max}(\rho_k) \cdot I$ the theorem gives $P_{\mathrm{opt}} \le d \max_k p_k\lambda_{\max}(\rho_k)$, which is $d/N$ for $N$ equiprobable pure states. Always guessing the most likely state gives $P_{\mathrm{opt}} \ge \max_k p_k$.

**Theorem 7 (unambiguous, Ivanovic, Dieks and Peres).** For two pure states with equal priors and overlap $s$, the best unambiguous success probability is $1 - |s|$.

*Proof.* Let $\{E_\psi, E_\phi, E_?\}$ never err, so $\langle\phi|E_\psi|\phi\rangle = 0$ and $\langle\psi|E_\phi|\psi\rangle = 0$. For a positive semidefinite $E$, $\langle v|E|v\rangle = 0$ implies $E|v\rangle = 0$, so $E_\psi|\phi\rangle = 0$ and $\langle\psi|E_\phi = 0$. Then $s = \langle\psi|(E_\psi + E_\phi + E_?)|\phi\rangle = \langle\psi|E_?|\phi\rangle$. The Cauchy-Schwarz inequality for the positive semidefinite form of $E_?$ gives $|s|^2 \le \langle\psi|E_?|\psi\rangle\langle\phi|E_?|\phi\rangle = f_\psi f_\phi$, where $f_\psi$ and $f_\phi$ are the failure probabilities. By the inequality of the arithmetic and geometric means, the average failure is $\tfrac12(f_\psi + f_\phi) \ge \sqrt{f_\psi f_\phi} \ge |s|$, so the success is at most $1 - |s|$. The measurement of the Known algorithms section reaches it: $\langle\psi|E_\psi|\psi\rangle = \frac{|\langle\phi^\perp|\psi\rangle|^2}{1 + |s|} = \frac{1 - |s|^2}{1 + |s|} = 1 - |s|$, and the same for $\phi$. $E_? \succeq 0$ because the sum of the two rank-one projectors $|\phi^\perp\rangle\langle\phi^\perp| + |\psi^\perp\rangle\langle\psi^\perp|$ has the largest eigenvalue $1 + |\langle\phi^\perp|\psi^\perp\rangle| = 1 + |s|$. $\square$

## Reductions

- **Two states to an eigenvalue problem.** By Theorem 1 the two-state problem is one Hermitian eigendecomposition of $\Gamma$ ([spectral theorem](/spectral-theorem/)).
- **Several states to a semidefinite program.** The minimum-error and unambiguous problems are semidefinite programs, and Theorem 6 is their duality ([semidefinite programming](/semidefinite-programming/)).
- **No-cloning.** A machine that copied every state of a set $\{|\psi\rangle, |\phi\rangle\}$ would give $n$ copies, and by Theorem 2 the error for $n$ copies goes to zero. So perfect cloning of non-orthogonal states would allow perfect discrimination in the limit, against Corollary 3. In the other direction, a perfect discrimination would allow cloning: measure, then prepare as many copies as needed. The [no-cloning theorem](/no-cloning-theorem/) and Corollary 3 are two sides of the same fact.
- **No-signalling.** If a local operation of Alice could change Bob's reduced state, Bob could discriminate the two reduced states and so receive a message. The [no-communication theorem](/no-communication-theorem/) says the two reduced states are equal, so by the non-examples above Bob can do no better than guess.
- **Swap test.** The [swap test](/swap-test/) on $|\psi\rangle \otimes |\phi\rangle$ accepts with probability $\tfrac12(1 + |s|^2)$. It does not need to know the states, but it is weaker than the Helstrom measurement when the states are known.

## Applications

- **Quantum key distribution.** In B92 (Bennett 1992) the sender codes a bit in one of two non-orthogonal states, and the receiver uses a measurement that never errs but sometimes fails. An eavesdropper faces the same discrimination problem, and the bounds of this page limit what she learns; see the [key distribution problem](/key-distribution-problem/).
- **Communication over quantum channels.** A receiver who decodes classical messages from quantum states solves a discrimination problem with one state for each codeword. The square-root measurement is the decoder in the standard proof of the classical capacity of a quantum channel ([channel capacity](/channel-capacity/)).
- **Communication and query complexity.** Lower bounds for quantum protocols often say that two inputs lead to final states at small trace distance, so by Theorem 1 no measurement tells them apart well ([communication complexity](/communication-complexity/), [quantum communication complexity](/quantum-communication-complexity/)).
- **Testing and learning states.** Each step of [state tomography](/quantum-state-tomography/) and of property testing must separate candidate states, and Theorem 5 gives the number of copies needed to tell two candidate states apart with a given error.
- **Optical communication.** Helstrom's original motivation was the detection of weak optical signals, such as coherent states of light, with the least error.

## References
