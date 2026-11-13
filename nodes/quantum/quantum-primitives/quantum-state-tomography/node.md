---
tag: JWVX4D
kind: problem
slug: quantum-state-tomography
name: Quantum state tomography
aliases:
- state tomography
area: quantum/quantum-primitives
level: advanced
summary: "Estimate an unknown density matrix from measurements on many copies. In dimension d it needs Theta(d^2/eps^2) copies for trace distance eps, so exponentially many in the qubit count."
prereqs: [density-matrix, quantum-measurement]
see_also: [trace-distance, fidelity, maximum-likelihood-estimation, hoeffding-inequality, semidefinite-programming, pauli-gates, swap-test, quantum-channel]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 8.4.2 (state tomography with Pauli measurements, then quantum process tomography)
  - paper: doi:10.1145/2897518.2897544
    title: Ryan O'Donnell and John Wright, Efficient quantum tomography, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC), 2016
    locator: pp. 899 to 912 (O(rd/eps^2) copies with entangled measurements)
  - paper: doi:10.1109/TIT.2017.2719044
    title: Jeongwan Haah, Aram W. Harrow, Zhengfeng Ji, Xiaodi Wu and Nengkun Yu, Sample-optimal tomography of quantum states, IEEE Transactions on Information Theory 63(9), 2017
    locator: pp. 5628 to 5641 (upper and lower bounds for entangled and for single-copy measurements)
  - paper: doi:10.1109/FOCS57990.2023.00029
    title: Sitan Chen, Brice Huang, Jerry Li, Allen Liu and Mark Sellke, When does adaptivity help for quantum state learning?, Proceedings of the 64th IEEE Symposium on Foundations of Computer Science (FOCS), 2023
    locator: pp. 391 to 404 (Omega(d^3/eps^2) for adaptive single-copy measurements)
  - paper: doi:10.1103/PhysRevA.55.R1561
    title: Zdeněk Hradil, Quantum-state estimation, Physical Review A 55, R1561, 1997
    locator: the R rho R iteration for the maximum likelihood estimate
  - paper: doi:10.1103/PhysRevLett.108.070502
    title: John A. Smolin, Jay M. Gambetta and Graeme Smith, Efficient method for computing the maximum-likelihood quantum state from measurements with additive Gaussian noise, Physical Review Letters 108, 070502, 2012
    locator: the projection of the eigenvalues onto the probability simplex
  - paper: doi:10.1038/s41567-020-0932-7
    title: Hsin-Yuan Huang, Richard Kueng and John Preskill, Predicting many properties of a quantum system from very few measurements, Nature Physics 16, 2020
    locator: pp. 1050 to 1057 (classical shadows)
---

Quantum state tomography is the problem of finding an unknown [density matrix](/density-matrix/) $\rho$ on $\mathbb{C}^d$ from the outcomes of [measurements](/quantum-measurement/) on many copies of it. One measurement destroys the copy and gives only one sample of a distribution, so the task is statistical: the output is an estimate $\hat\rho$ that is close to $\rho$, usually in [trace distance](/trace-distance/), with high probability. A density matrix has $d^2 - 1$ real parameters, and $\Theta(d^2/\varepsilon^2)$ copies are necessary and sufficient for trace distance $\varepsilon$ when the measurements can act on all copies together. For $n$ qubits $d = 2^n$, so the cost grows as $4^n$. Tomography is the standard way to check a small quantum device, and its cost is the reason why larger devices are checked with less complete methods.

## In plain words

You get a box that makes the same quantum state again and again, and you must say what that state is. You cannot look at the state directly. You can only measure a copy, and each measurement gives one random answer and uses up the copy. So you measure many copies in several different ways, count the answers, and work out which state gives counts like these.

For one qubit, three kinds of measurement and a few thousand copies are enough for a good answer. Each new qubit multiplies the number of unknown numbers by four. For a few dozen qubits, the copies needed are more than anyone can make.

## Definition

**Input.** Access to independent copies of an unknown state $\rho$ on $\mathbb{C}^d$, an accuracy $\varepsilon > 0$ and a failure probability $\delta$. The algorithm chooses measurements, applies them to copies, and sees the outcomes.

**Output.** A matrix $\hat\rho$ with $D(\hat\rho, \rho) = \frac12\|\hat\rho - \rho\|_1 \le \varepsilon$ with probability at least $1 - \delta$. Other error measures are the [fidelity](/fidelity/), the Frobenius norm and the error of chosen expectation values. The output is often required to be a density matrix itself.

**Cost.** The main cost is the number $N$ of copies, called the sample complexity. The other costs are the number of different measurement settings, the classical computation, and the quantum memory, which is the number of copies that one measurement acts on.

**Measurement models.**

- *Entangled (coherent) measurements.* One measurement acts on $\rho^{\otimes N}$, all the copies together.
- *Single-copy (incoherent) measurements.* Each copy is measured on its own. The measurement of a copy can be fixed in advance (nonadaptive) or can depend on earlier outcomes (adaptive).
- *Pauli measurements.* For $n$ qubits, each qubit is measured in the eigenbasis of $X$, $Y$ or $Z$ (see [Pauli gates](/pauli-gates/)). This is the model of most experiments.

**The Pauli expansion.** The $4^n$ products $P = P_{n-1} \otimes \cdots \otimes P_0$ with $P_q \in \{I, X, Y, Z\}$ satisfy $\operatorname{Tr}(PQ) = 2^n$ if $P = Q$ and $0$ otherwise. So every density matrix on $n$ qubits is

$$\rho = \frac{1}{2^n}\sum_{P} \operatorname{Tr}(P\rho)\, P,$$

and $\rho$ is fixed by the $4^n - 1$ real numbers $\langle P\rangle = \operatorname{Tr}(P\rho)$ for $P \ne I^{\otimes n}$. To find them is to find $\rho$.

## Variants

- **Pure states.** If $\rho = |\psi\rangle\langle\psi|$ is known to be pure, there are only $2d - 2$ real parameters, and the number of copies drops to order $d/\varepsilon^2$.
- **Low rank.** If $\rho$ has rank $r$, entangled measurements need order $rd/\varepsilon^2$ copies. Compressed sensing (Gross, Liu, Flammia, Becker and Eisert, 2010) recovers a state of low rank from a random subset of the Pauli expectations.
- **Fidelity error.** The goal can be a small infidelity $1 - F(\hat\rho, \rho)^2$ in place of a small trace distance. By the Fuchs-van de Graaf inequalities, infidelity at most $\varepsilon^2$ gives trace distance at most $\varepsilon$, so a scheme for infidelity also solves the trace distance problem.
- **Shadow tomography.** The goal is only the values $\operatorname{Tr}(O_i\rho)$ of $M$ given observables, each within $\varepsilon$. Aaronson (2018) showed that a number of copies polylogarithmic in $M$ and $d$ is enough with entangled measurements. Classical shadows (Huang, Kueng and Preskill, 2020) do it with single-copy measurements for many families of observables.
- **Process tomography.** The unknown object is a [quantum channel](/quantum-channel/). It reduces to state tomography of the Choi matrix of the channel, which is described with the [Kraus operators](/kraus-operators/).
- **Continuous variables.** For a mode of light, homodyne measurements give the marginals of the Wigner function, and an inverse Radon transform gives the state. This is the origin of the word "tomography", from medical imaging.

## Examples

**One qubit.** Write $\rho = \frac12(I + r_x X + r_y Y + r_z Z)$ with the Bloch vector $\vec r$ (see [Bloch sphere](/bloch-sphere/)). Measuring a copy in the $X$ basis gives $+1$ with probability $(1 + r_x)/2$ and $-1$ otherwise, and the same holds for $Y$ and $Z$. So the three averages $\hat r_x, \hat r_y, \hat r_z$ are unbiased estimates of the Bloch vector. Each is a mean of $N$ independent values in $[-1, 1]$, so by the [Hoeffding inequality](/hoeffding-inequality/) $|\hat r_k - r_k| < t$ with probability at least $1 - 2e^{-Nt^2/2}$. The trace distance between two qubit states is half the distance between their Bloch vectors, so $D(\hat\rho, \rho) \le \frac{\sqrt3}{2}t$ when all three estimates are within $t$. With $N = 20000$ copies per basis and $\delta = 10^{-3}$ shared over the three estimates, $t = \sqrt{2\ln(6000)/20000} = 0.0295$ and $D \le 0.0255$.

**An estimate that is not a state.** Let the true state be pure with $\vec r = (0.6, 0, 0.8)$, and let the counts give $\hat{\vec r} = (0.6, 0.02, 0.81)$. Then $|\hat{\vec r}| = 1.0082 > 1$, and $\hat\rho$ has the eigenvalue $(1 - 1.0082)/2 = -0.0041$, so it is not a density matrix. The closest state in Frobenius norm has the Bloch vector $\hat{\vec r}/|\hat{\vec r}| = (0.5951, 0.0198, 0.8034)$. Its trace distance to $\rho$ is $0.0104$, while that of $\hat\rho$ is $0.0112$.

**The size of the problem.** For $n$ qubits there are $4^n - 1$ Pauli expectations to estimate, $3^n$ Pauli settings that cover them (a label with $I$ on some qubits is read from any setting that agrees on the other qubits), and $2^n$ outcomes in each setting.

| $n$ | $d = 2^n$ | parameters $4^n - 1$ | settings $3^n$ |
| --- | --- | --- | --- |
| 1 | 2 | 3 | 3 |
| 2 | 4 | 15 | 9 |
| 3 | 8 | 63 | 27 |
| 5 | 32 | 1023 | 243 |
| 10 | 1024 | 1048575 | 59049 |

**Copies for linear inversion.** Suppose each of the $d^2 - 1$ Pauli estimates is within $t$. The error matrix is $\frac1d\sum_P e_P P$, so its Frobenius norm is $\sqrt{\sum_P e_P^2/d} \le t\sqrt{(d^2-1)/d}$, and $\|A\|_1 \le \sqrt d\,\|A\|_2$ gives $D(\hat\rho, \rho) \le \frac{t}{2}\sqrt{d^2 - 1}$. With a union bound over the $d^2 - 1$ estimates, $N = \frac{(d^2-1)\ln(2(d^2-1)/\delta)}{2\varepsilon^2}$ copies per setting give $D \le \varepsilon$ with probability $1 - \delta$. For $\varepsilon = 0.05$ and $\delta = 0.01$:

| $n$ | copies per setting | total copies |
| --- | --- | --- |
| 1 | 3839 | 11517 |
| 2 | 24020 | 216180 |
| 3 | 118963 | 3212001 |
| 4 | 552819 | 44778339 |

This simple analysis is far from tight, but it shows the growth: about $3^n \cdot 4^n$ copies, against the $4^n$ of the best entangled scheme.

## Known algorithms

- **Linear inversion.** Estimate each $\langle P\rangle$ by the mean of the $\pm1$ products of the outcomes, and put the estimates into the Pauli expansion. The estimate is unbiased, Hermitian and of trace 1, but noise can give it negative eigenvalues. A Pauli product has one nonzero entry in each row, so the sum of the $4^n$ terms costs $O(4^n \cdot 2^n)$ classical operations.
- **Projection onto states.** Smolin, Gambetta and Smith (2012) find the density matrix closest in Frobenius norm to a Hermitian matrix $A$ of trace 1. Keep the eigenvectors of $A$, and replace the eigenvalues by the closest probability vector: set the most negative eigenvalues to 0 one at a time and spread their sum evenly over the rest. The cost is one eigendecomposition, $O(d^3)$. The set of states is convex and contains $\rho$, so the projection is never farther from $\rho$ in Frobenius norm than $A$ was.
- **[Maximum likelihood](/maximum-likelihood-estimation/).** Choose the state that maximizes the probability of the observed counts, $\sum_j f_j \log\operatorname{Tr}(\Pi_j\rho)$, where $f_j$ is the frequency of outcome $\Pi_j$. The function is concave on the convex set of states. Hradil (1997) gave the fixed-point iteration $\rho \leftarrow R\rho R/\operatorname{Tr}(R\rho R)$ with $R = \sum_j \frac{f_j}{\operatorname{Tr}(\Pi_j\rho)}\Pi_j$. A diluted form of the step (Řeháček, Hradil, Knill and Lvovsky, 2007) always increases the likelihood. The problem can also be solved as a convex program, for example with [semidefinite programming](/semidefinite-programming/) methods.
- **Compressed sensing.** For a state of rank $r$, measure about $rd\log^2 d$ randomly chosen Pauli expectations and find the matrix of smallest trace norm that fits them. This uses far fewer settings than the full Pauli set.
- **Entangled optimal schemes.** O'Donnell and Wright (2016) measure $\rho^{\otimes N}$ with a measurement built from the representations of the symmetric and unitary groups (Schur-Weyl duality), with $O(rd/\varepsilon^2)$ copies for trace distance. Haah, Harrow, Ji, Wu and Yu (2017) give a different optimal scheme. These schemes need a quantum memory of many copies.
- **Random single-copy measurements.** Measure each copy with a random rank-one projective measurement, form a linear estimate from the outcomes, and project it onto the states. Kueng, Rauhut and Terstiege (2017) showed that $O(d^3/\varepsilon^2)$ copies suffice, which is optimal for single-copy measurements.
- **Classical shadows.** Apply a random Clifford or a random single-qubit rotation to each copy, measure in the computational basis, and keep the inverted snapshot. Huang, Kueng and Preskill (2020) showed that $O(\log(M)\, B/\varepsilon^2)$ snapshots predict $M$ expectation values, where $B$ depends on the observables; for random Pauli bases and Pauli observables on $k$ qubits, $B = 3^k$ up to a constant.

The Python code of this page simulates Pauli tomography on up to three qubits: it samples counts with a seeded generator, estimates the expectations, inverts them, projects the result onto the states, and runs Hradil's iteration. Its tests check the Hoeffding bounds of the examples above, the negative eigenvalue of a noisy pure state and its removal by the projection, and the $1/\sqrt N$ decrease of the error.

## Bounds

**Entangled measurements.** $\Theta(d^2/\varepsilon^2)$ copies are necessary and sufficient to reach trace distance $\varepsilon$ for a general state. The upper bound is $O(rd/\varepsilon^2)$ for rank $r$ (O'Donnell and Wright, 2016). Haah et al. (2017) prove the lower bound $\Omega(d^2/\varepsilon^2)$ and an upper bound $O(\frac{d^2}{\varepsilon^2}\log\frac{d}{\varepsilon})$. The lower bound counts parameters in a precise form: the algorithm must tell apart a large set of states that are pairwise far apart, and each copy carries a limited amount of information about the choice.

**Single-copy measurements.** $\Theta(d^3/\varepsilon^2)$ copies are necessary and sufficient. The upper bound is from Kueng, Rauhut and Terstiege (2017). Haah et al. (2017) proved a lower bound of this order, up to a logarithmic factor, for nonadaptive measurements, and Chen, Huang, Li, Liu and Sellke (2023) proved $\Omega(d^3/\varepsilon^2)$ even when each measurement may depend on the earlier outcomes. So a quantum memory saves a factor of $d$.

**The dependence on $\varepsilon$.** Even for one qubit with a known basis, the task contains the estimation of a coin bias to error $\varepsilon$, which needs $\Omega(1/\varepsilon^2)$ samples. So the factor $1/\varepsilon^2$ cannot be removed.

**Qubits.** With $d = 2^n$, the bounds are $\Theta(4^n/\varepsilon^2)$ with entangled measurements and $\Theta(8^n/\varepsilon^2)$ with single-copy measurements. No measurement model avoids exponential growth for general states. This is why full tomography is done only for a few qubits, and why larger devices are tested with fidelity estimates, randomized benchmarking or classical shadows.

## Reductions

- **Every property from tomography.** If $D(\hat\rho, \rho) \le \varepsilon$, then $|\operatorname{Tr}(O\hat\rho) - \operatorname{Tr}(O\rho)| \le 2\varepsilon\|O\|$ for each observable $O$, by the variational form of the trace distance. Continuity bounds then give estimates of the fidelity, the [von Neumann entropy](/von-neumann-entropy/) and other functions of the state. Tomography is the most expensive way to learn any of them.
- **Classical distribution learning.** If the eigenbasis of $\rho$ is known, measuring in that basis turns the problem into learning a distribution on $d$ outcomes in [total variation distance](/total-variation-distance/), which needs $\Theta(d/\varepsilon^2)$ samples. The unknown basis is what makes the quantum problem harder.
- **From state discrimination.** Lower bounds come from the [state discrimination problem](/state-discrimination-problem/): an algorithm that learns every state to accuracy $\varepsilon/2$ can identify a state from a set whose members are pairwise more than $\varepsilon$ apart.
- **Process tomography.** A channel $\Phi$ from $d_{\text{in}}$ to $d_{\text{out}}$ dimensions is learned by state tomography of the normalized Choi state $\frac{1}{d_{\text{in}}}(\Phi \otimes \mathrm{id})(|\Omega\rangle\langle\Omega|)$, with $|\Omega\rangle = \sum_i |i\rangle|i\rangle$.
- **Overlaps of two states.** To learn only $\operatorname{Tr}(\rho\sigma)$, tomography is not needed. The [swap test](/swap-test/) estimates it to error $\varepsilon$ with $O(1/\varepsilon^2)$ pairs of copies, for every $d$.

## Applications

- **Checking small devices.** Experiments reconstruct the state of one to a few qubits after a preparation or a gate, and compare it with the target state by fidelity or trace distance.
- **Entanglement in experiments.** The reconstructed state of two qubits gives measures of [entanglement](/entanglement/), for example the entropy of a reduced state after a [partial trace](/partial-trace/).
- **Calibration and error models.** Process tomography, which is state tomography of the Choi state, gives the Kraus operators of the noise of a gate.
- **Reduced states of large systems.** Many properties of a large system depend only on the states of a few qubits at a time. Classical shadows and local tomography estimate these reduced states without full tomography.

## References
