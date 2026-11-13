---
tag: K1PK1V
kind: definition
slug: born-rule
name: Born rule
aliases:
- Born's rule
area: quantum/quantum-primitives
level: intro
summary: "The Born rule gives the probability of outcome m of a measurement with projectors P_m on the state |psi> as <psi|P_m|psi>; in a basis it is the squared magnitude of the amplitude."
prereqs: [quantum-state, probability-distribution]
see_also: [quantum-measurement, density-matrix, quantum-interference, bloch-sphere, expected-value, hoeffding-inequality, quantum-state-tomography, state-discrimination-problem]
sources:
  - paper: doi:10.1007/BF01397477
    title: Max Born, Zur Quantenmechanik der Stoßvorgänge, Zeitschrift für Physik 37, 1926, pages 863 to 867
    locator: the footnote added in proof that gives the probability as the square of the amplitude
  - paper: doi:10.1007/BF01397184
    title: Max Born, Quantenmechanik der Stoßvorgänge, Zeitschrift für Physik 38, 1926, pages 803 to 827
    locator: the full treatment of the collision problem with the probability interpretation
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.2 (measurement of a qubit), Section 2.2.3 (the measurement postulate), Section 2.2.5 (projective measurements) and Section 2.4.1 (density matrices)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.2.2 (measurement)
---

The *Born rule* turns a quantum state into the probabilities of the outcomes of a measurement. If the measurement has the outcomes $m$ with orthogonal projectors $P_m$ that sum to the identity, the outcome $m$ on the unit vector $|\psi\rangle$ has the probability $p(m) = \langle\psi|P_m|\psi\rangle$. For a measurement in an orthonormal basis $|e_k\rangle$ this is $p(k) = |\langle e_k|\psi\rangle|^2$, the squared magnitude of the amplitude. Probabilities come from squares, so amplitudes can cancel before the square is taken, but probabilities never cancel.

## Definition

Let $|\psi\rangle$ be a unit vector of a Hilbert space $\mathcal{H}$, and let $\{P_m\}$ be a *projective measurement*: Hermitian matrices with $P_m P_{m'} = \delta_{m m'} P_m$ and $\sum_m P_m = I$ ([quantum measurement](/quantum-measurement/)). The **Born rule** says that the measurement gives outcome $m$ with probability

$$p(m) = \langle\psi|P_m|\psi\rangle = \lVert P_m|\psi\rangle \rVert^2.$$

These numbers form a [probability distribution](/probability-distribution/): each is $\ge 0$ because $\langle\psi|P_m|\psi\rangle = \lVert P_m\psi\rVert^2$, and they sum to $\langle\psi|I|\psi\rangle = 1$.

**In a basis.** For the measurement in an orthonormal basis $|e_0\rangle, \dots, |e_{d-1}\rangle$ the projectors are $P_k = |e_k\rangle\langle e_k|$, and

$$p(k) = |\langle e_k|\psi\rangle|^2.$$

In the computational basis of $n$ qubits, with $|\psi\rangle = \sum_x \alpha_x |x\rangle$, the outcome $x$ has probability $|\alpha_x|^2$.

**Part of the qubits.** Measuring only the qubits in a set $S$ in the computational basis is the projective measurement with $P_y = \sum_{x\,:\,x_S = y} |x\rangle\langle x|$, where $x_S$ is the restriction of the bit string $x$ to $S$. So the probability of $y$ is the marginal $\sum_{x\,:\,x_S = y} |\alpha_x|^2$.

**Expected values.** For a Hermitian matrix $A = \sum_m a_m P_m$ (its spectral decomposition, by the [spectral theorem](/spectral-theorem/)), the outcome $a_m$ has probability $p(m)$, and the [expected value](/expected-value/) of the outcome is $\sum_m a_m\,p(m) = \langle\psi|A|\psi\rangle$.

**Density matrices.** For a [density matrix](/density-matrix/) $\rho$ the rule is $p(m) = \operatorname{tr}(P_m \rho)$. For $\rho = |\psi\rangle\langle\psi|$ this is $\langle\psi|P_m|\psi\rangle$. For a general measurement with positive operators $E_m$ that sum to $I$ (a POVM) it is $p(m) = \operatorname{tr}(E_m\rho)$.

**Properties.**

- A global phase does not change any probability: $|\langle e_k|e^{i\gamma}\psi\rangle|^2 = |\langle e_k|\psi\rangle|^2$.
- A relative phase can. $|+\rangle$ and $|-\rangle$ give $\tfrac{1}{2}, \tfrac{1}{2}$ in the computational basis but $1, 0$ and $0, 1$ in the basis $|\pm\rangle$.
- The rule is quadratic, not linear, in the state. For $|\psi\rangle = \sum_j c_j|\phi_j\rangle$, the probability is $p(k) = \lvert \sum_j c_j \langle e_k|\phi_j\rangle \rvert^2$, which has the cross terms $2\,\mathrm{Re}(\overline{c_j\langle e_k|\phi_j\rangle}\,c_l\langle e_k|\phi_l\rangle)$. These terms can be negative. This is [quantum interference](/quantum-interference/).

## Examples and non-examples

**A worked state.** $|\psi\rangle = \tfrac{3}{5}|0\rangle + \tfrac{4i}{5}|1\rangle$.

- In the computational basis, $p(0) = \tfrac{9}{25}$ and $p(1) = \tfrac{16}{25}$.
- In the basis $|\pm\rangle = (|0\rangle \pm |1\rangle)/\sqrt{2}$, $\langle\pm|\psi\rangle = (3 \pm 4i)/(5\sqrt{2})$, so $p(+) = p(-) = \tfrac{25}{50} = \tfrac{1}{2}$.
- In the basis $|{\pm i}\rangle = (|0\rangle \pm i|1\rangle)/\sqrt{2}$, $\langle{+i}|\psi\rangle = \tfrac{1}{\sqrt 2}(\tfrac{3}{5} + \tfrac{4}{5}) = \tfrac{7}{5\sqrt 2}$ and $\langle{-i}|\psi\rangle = -\tfrac{1}{5\sqrt 2}$, so $p(+i) = \tfrac{49}{50}$ and $p(-i) = \tfrac{1}{50}$.

**A Bell state and a marginal.** For $(|00\rangle + |11\rangle)/\sqrt{2}$, a measurement of both qubits gives $00$ or $11$, each with probability $\tfrac{1}{2}$, and never $01$ or $10$. A measurement of qubit $0$ alone gives $0$ or $1$ with probability $\tfrac{1}{2}$ each: the projector $P_0 = I \otimes |0\rangle\langle 0|$ gives $\langle\psi|P_0|\psi\rangle = \tfrac{1}{2}$.

**Cancellation.** $\tfrac{1}{\sqrt 2}(|+\rangle + |-\rangle) = |0\rangle$. Each of $|+\rangle$ and $|-\rangle$ alone gives the outcome $1$ with probability $\tfrac{1}{2}$, but their superposition gives it with probability $0$, because the amplitudes $\tfrac{1}{2}$ and $-\tfrac{1}{2}$ of $|1\rangle$ cancel. A mixture of $|+\rangle$ and $|-\rangle$ with probabilities $\tfrac{1}{2}$ each still gives $1$ with probability $\tfrac{1}{2}$.

**Expected value of $Z$.** $\langle\psi|Z|\psi\rangle = |\alpha_0|^2 - |\alpha_1|^2 = p(0) - p(1)$. For the worked state it is $-\tfrac{7}{25}$, the $z$ coordinate on the [Bloch sphere](/bloch-sphere/).

**Non-example: the magnitude without the square.** $|\alpha_x|$ is not a probability. For $|+\rangle$ the magnitudes are $\tfrac{1}{\sqrt 2}$ and $\tfrac{1}{\sqrt 2}$, which sum to $\sqrt 2$. Only $|\alpha_x|^2$ sums to $1$ for every unit vector, and Gleason's theorem shows that in dimension at least $3$ the trace rule is the only way to assign probabilities to projectors that is additive on orthogonal projectors.

**Non-example: an unnormalized vector.** For $v = |0\rangle + |1\rangle$, the numbers $|\langle k|v\rangle|^2$ are $1$ and $1$. Normalize first, or use $\lVert P_m v\rVert^2 / \lVert v\rVert^2$.

### Sampling

One run of a quantum computer gives one outcome, a sample from the Born distribution. To estimate a probability $p$ to within $\varepsilon$, repeat the preparation and the measurement $N$ times and count. By the [Hoeffding inequality](/hoeffding-inequality/), the frequency is within $\varepsilon$ of $p$ except with probability at most $2e^{-2N\varepsilon^2}$. For $\varepsilon = 0.02$ and $N = 20000$ this is below $2 \cdot 10^{-6}$, so $O(1/\varepsilon^2)$ shots are needed and they are enough. The amplitudes themselves, with their phases, are not samples; estimating them needs measurements in several bases ([quantum state tomography](/quantum-state-tomography/)).

### Implementation

The file `impl/python/born_rule.py` computes $|\langle e_k|\psi\rangle|^2$ in any orthonormal basis, $\langle\psi|P|\psi\rangle$ for a projector, marginals of a subset of qubits, expected values, and exact probabilities with fractions for amplitudes with rational real and imaginary parts. The tests compare the three bases of the worked state with the exact fractions above, compare the projector form with the basis form on random states with fixed seeds, and check sampled frequencies over 20000 shots with seed 2026 against the Born probabilities with the tolerance $0.02$.

## Related definitions

- [Quantum measurement](/quantum-measurement/): the projectors, the state after the measurement, and POVMs.
- [Density matrix](/density-matrix/): the form $p(m) = \operatorname{tr}(P_m\rho)$.
- [Quantum interference](/quantum-interference/): the cross terms of the rule.
- [Expected value](/expected-value/): $\langle\psi|A|\psi\rangle$ is the mean of the outcomes of the observable $A$.
- [State discrimination](/state-discrimination-problem/): the rule limits how well a measurement can tell given states apart; nonorthogonal states cannot be told apart with certainty.

### History

Born proposed the rule in 1926 for the scattering of a particle. In the first paper the probability appears in a note added in proof, which says that the probability is proportional to the square of the amplitude; the main text only says that the amplitude determines the probability. Born received the Nobel Prize in Physics for it in 1954. Gleason proved his theorem in 1957.

## References
