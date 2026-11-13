---
tag: VHKA6P
kind: concept
slug: entanglement
name: Entanglement
aliases:
- quantum entanglement
area: quantum/quantum-primitives
level: intro
summary: "A state of two or more systems is entangled when it is not a product of states of the parts (pure case) or not a mixture of such products (mixed case)."
prereqs: [quantum-state, tensor-product]
see_also: [bell-states, entanglement-entropy, bell-theorem, no-communication-theorem, partial-trace, mixed-state, quantum-teleportation, gottesman-knill-theorem]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.6 (Bell states), Section 2.5 (the Schmidt decomposition and purifications) and Section 12.5 (entanglement as a physical resource)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Chapter 6, Section 6.1 (separability, Theorem 6.9 for the Horodecki criterion) and Section 6.2.3 (partial transposition and bound entanglement)
  - paper: doi:10.1103/RevModPhys.81.865
    title: Ryszard Horodecki, Paweł Horodecki, Michał Horodecki and Karol Horodecki, Quantum entanglement, Reviews of Modern Physics 81(2), 2009, pages 865 to 942
    locator: the survey as a whole
  - paper: doi:10.1017/S0305004100013554
    title: Erwin Schrödinger, Discussion of probability relations between separated systems, Mathematical Proceedings of the Cambridge Philosophical Society 31(4), 1935, pages 555 to 563
    locator: the paper that names entanglement
  - paper: doi:10.1103/PhysRevA.40.4277
    title: Reinhard F. Werner, Quantum states with Einstein-Podolsky-Rosen correlations admitting a hidden-variable model, Physical Review A 40, 1989, pages 4277 to 4281
    locator: the definition of separable mixed states and the Werner states
  - paper: doi:10.1103/PhysRevLett.77.1413
    title: Asher Peres, Separability criterion for density matrices, Physical Review Letters 77, 1996, pages 1413 to 1415
    locator: the partial transpose test
  - paper: doi:10.1016/S0375-9601(96)00706-2
    title: Michał Horodecki, Paweł Horodecki and Ryszard Horodecki, Separability of mixed states, necessary and sufficient conditions, Physics Letters A 223, 1996, pages 1 to 8
    locator: the partial transpose test is exact for 2 x 2 and 2 x 3 systems
  - paper: doi:10.1103/PhysRevA.62.062314
    title: Wolfgang Dür, Guifré Vidal and J. Ignacio Cirac, Three qubits can be entangled in two inequivalent ways, Physical Review A 62, 2000, article 062314
    locator: the GHZ and W classes
  - paper: doi:10.1098/rspa.2002.1097
    title: Richard Jozsa and Noah Linden, On the role of entanglement in quantum-computational speed-up, Proceedings of the Royal Society A 459, 2003, pages 2011 to 2032
    locator: the classical simulation of pure-state circuits with bounded entanglement
  - paper: doi:10.1145/780542.780545
    title: Leonid Gurvits, Classical deterministic complexity of Edmonds' problem and quantum entanglement, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC), 2003, pages 10 to 19
    locator: NP-hardness of the separability problem
  - paper: doi:10.1103/PhysRevLett.83.436
    title: Michael A. Nielsen, Conditions for a class of entanglement transformations, Physical Review Letters 83, 1999, pages 436 to 439
    locator: the majorization rule for LOCC conversion of pure states
  - paper: doi:10.1103/PhysRevA.61.052306
    title: Valerie Coffman, Joydip Kundu and William K. Wootters, Distributed entanglement, Physical Review A 61, 2000, article 052306
    locator: the monogamy inequality for three qubits
---

*Entanglement* is the property of a joint state of two or more quantum systems that cannot be described by giving one state to each system. A pure state $|\psi\rangle_{AB}$ is entangled when it is not a [tensor product](/tensor-product/) $|a\rangle \otimes |b\rangle$, and a mixed state $\rho_{AB}$ is entangled when it is not a mixture of such products. Entangled systems show correlations that no shared classical randomness can give ([Bell's theorem](/bell-theorem/)), but they cannot send a message by themselves ([no-communication theorem](/no-communication-theorem/)). Teleportation, superdense coding, entanglement-based key distribution and many quantum algorithms use entanglement as a resource.

## In plain words

Two coins in two boxes each have their own state, heads or tails. You can describe the pair by describing each coin. For two qubits this is not always possible. Some joint states have no description of the form "this qubit is in this state, and that qubit is in that state". Such a pair is entangled. When you measure one qubit of an entangled pair, you learn about the other one, even if it is far away. This is also true for two sealed envelopes with copies of the same card, but entangled qubits go further: they agree in more ways than any shared card can explain. Still, the person who holds one qubit cannot use it to send a message to the other person. Entanglement is a shared resource, like a shared secret, that the two people use up in protocols.

## The idea

### Pure states

Let $A$ and $B$ be two systems with spaces $\mathcal{H}_A$ and $\mathcal{H}_B$. A pure state $|\psi\rangle \in \mathcal{H}_A \otimes \mathcal{H}_B$ is a *product state* when $|\psi\rangle = |a\rangle \otimes |b\rangle$ for unit vectors $|a\rangle \in \mathcal{H}_A$ and $|b\rangle \in \mathcal{H}_B$. Otherwise it is *entangled*.

Write $|\psi\rangle = \sum_{i,j} c_{ij} |i\rangle|j\rangle$ in product bases, and let $C = (c_{ij})$ be the $d_A \times d_B$ matrix of the coefficients. A product state has $c_{ij} = a_i b_j$, so $C = a b^{\mathsf{T}}$ has rank $1$. Conversely, a matrix of rank $1$ is an outer product $a b^{\mathsf{T}}$, and the state is then $|a\rangle|b\rangle$. So:

> $|\psi\rangle$ is a product state if and only if its coefficient matrix has rank $1$.

For two qubits with the coefficients $c_{00}, c_{01}, c_{10}, c_{11}$, the test is $c_{00}c_{11} - c_{01}c_{10} = 0$. The number $2|c_{00}c_{11} - c_{01}c_{10}|$ is the *concurrence* of the pure state, which is $0$ for products and $1$ for the [Bell states](/bell-states/).

The [singular value decomposition](/singular-value-decomposition/) $C = U \Sigma V^{\mathsf{T}}$ gives the *Schmidt decomposition*

$$|\psi\rangle = \sum_{k=1}^{r} \lambda_k |a_k\rangle|b_k\rangle, \qquad \lambda_1 \ge \cdots \ge \lambda_r > 0, \quad \sum_k \lambda_k^2 = 1,$$

with orthonormal sets $\{|a_k\rangle\}$ and $\{|b_k\rangle\}$. The *Schmidt rank* $r$ is the rank of $C$, and the state is entangled if and only if $r \ge 2$. The reduced states $\rho_A = \mathrm{Tr}_B |\psi\rangle\langle\psi|$ and $\rho_B$ (see [partial trace](/partial-trace/)) have the same nonzero eigenvalues $\lambda_k^2$. A pure state is therefore entangled if and only if its reduced state $\rho_A$ is [mixed](/mixed-state/). The [entanglement entropy](/entanglement-entropy/) $S(\rho_A) = -\sum_k \lambda_k^2 \log_2 \lambda_k^2$ measures how much entanglement a pure state has.

### Mixed states

For a [density matrix](/density-matrix/) the definition has to allow classical correlation. Werner (1989) called $\rho_{AB}$ *separable* when

$$\rho_{AB} = \sum_k p_k\, \rho_k^A \otimes \rho_k^B, \qquad p_k \ge 0, \quad \sum_k p_k = 1,$$

for density matrices $\rho_k^A$ and $\rho_k^B$. Two parties can make any separable state with local operations and shared random bits: they draw $k$ with probability $p_k$, and each prepares their factor. A state that is not separable is *entangled*. For a pure state, this agrees with the definition above.

Separability is hard to decide in general. Gurvits (2003) proved that the weak membership problem for the separable states, with an accuracy that is exponentially small in the dimension, is NP-hard. For small systems there is an exact test.

**The partial transpose test.** Let $T_B$ transpose the $B$ factor: $(|i\rangle\langle j| \otimes |k\rangle\langle l|)^{T_B} = |i\rangle\langle j| \otimes |l\rangle\langle k|$. If $\rho$ is separable, then $\rho^{T_B} = \sum_k p_k \rho_k^A \otimes (\rho_k^B)^{\mathsf{T}}$ is a sum of positive semidefinite matrices, because the transpose of a density matrix is a density matrix. So a separable state has $\rho^{T_B} \succeq 0$ (Peres 1996). For $2 \times 2$ and $2 \times 3$ systems the converse also holds (Horodecki, Horodecki and Horodecki 1996): a state of two qubits is entangled if and only if its partial transpose has a negative eigenvalue. In larger systems there are entangled states with a positive partial transpose, the *bound entangled* states.

### What local operations can do

Local unitaries $U_A \otimes U_B$ do not change the Schmidt coefficients, so they do not change any measure of entanglement. More generally, local operations and classical communication (LOCC) map separable states to separable states, so LOCC cannot create entanglement; it can only move or use up entanglement that is already shared. Nielsen (1999) found the exact rule for pure states: LOCC turns $|\psi\rangle$ into $|\phi\rangle$ if and only if the vector of squared Schmidt coefficients of $\psi$ is majorized by that of $\phi$.

### More than two systems

With three or more systems there are several kinds of entanglement. The GHZ state $(|000\rangle + |111\rangle)/\sqrt{2}$ and the W state $(|001\rangle + |010\rangle + |100\rangle)/\sqrt{3}$ cannot be turned into each other by local operations, even with a nonzero probability of failure (Dür, Vidal and Cirac 2000). Entanglement is also *monogamous*: if qubits $A$ and $B$ are maximally entangled, then neither can be entangled with a third qubit $C$.

## Examples

**A Bell state.** $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$ has $c_{00}c_{11} - c_{01}c_{10} = \tfrac{1}{2} \ne 0$, so it is entangled. Its Schmidt coefficients are $\lambda_1 = \lambda_2 = 1/\sqrt{2}$, its reduced states are $I/2$, and its entanglement entropy is $1$, the maximum for two qubits. The [Bell states](/bell-states/) page lists all four.

**A product state with all four amplitudes.** $\tfrac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle) = |+\rangle|+\rangle$ has $c_{00}c_{11} - c_{01}c_{10} = \tfrac{1}{4} - \tfrac{1}{4} = 0$. Many nonzero amplitudes do not make a state entangled.

**A hidden maximally entangled state.** $\tfrac{1}{2}(|00\rangle + |01\rangle + |10\rangle - |11\rangle)$ has $c_{00}c_{11} - c_{01}c_{10} = -\tfrac{1}{4} - \tfrac{1}{4} = -\tfrac{1}{2}$, so its concurrence is $1$. Its coefficient matrix is $H/\sqrt{2}$, where $H$ is the [Hadamard](/hadamard-gate/) matrix, with both singular values $1/\sqrt{2}$, so it is maximally entangled. It is the controlled-$Z$ gate applied to $|+\rangle|+\rangle$, and $H$ on qubit $0$ maps it to $|\Phi^+\rangle$.

**Correlated but separable.** The mixture $\tfrac{1}{2}(|00\rangle\langle 00| + |11\rangle\langle 11|)$ has perfectly correlated results in the computational basis, but it is separable by its definition. Its partial transpose is itself, with eigenvalues $\tfrac{1}{2}, \tfrac{1}{2}, 0, 0$. It differs from $|\Phi^+\rangle$ in the basis $|+\rangle, |-\rangle$: there $|\Phi^+\rangle$ is still perfectly correlated, while the mixture gives independent results.

**Werner states.** Let $\rho_p = p\,|\Psi^-\rangle\langle\Psi^-| + (1-p)\, I/4$ with $0 \le p \le 1$, where $|\Psi^-\rangle = (|01\rangle - |10\rangle)/\sqrt{2}$. The partial transpose of $|\Psi^-\rangle\langle\Psi^-|$ has the eigenvalues $\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}, -\tfrac{1}{2}$, so $\rho_p^{T_B}$ has the eigenvalue $(1+p)/4$ three times and $(1-3p)/4$ once. So $\rho_p$ is entangled if and only if $p > 1/3$. It violates the [CHSH inequality](/chsh-inequality/) if and only if $p > 1/\sqrt{2}$, and Werner gave a local hidden-variable model for all projective measurements at $p = 1/2$. So for $1/3 < p \le 1/2$ the state is entangled, but its measurement statistics have a classical model: entanglement and nonlocality are different properties.

**GHZ and W after the loss of a qubit.** Trace out qubit $2$. The GHZ state leaves $\tfrac{1}{2}(|00\rangle\langle 00| + |11\rangle\langle 11|)$, which is separable. The W state leaves $\tfrac{1}{3}|00\rangle\langle 00| + \tfrac{2}{3}|\Psi^+\rangle\langle\Psi^+|$, whose partial transpose has the negative eigenvalue $(1 - \sqrt{5})/6 \approx -0.206$, so the two remaining qubits are still entangled.

### Common errors

- Reading entanglement as a fast signal. The results of a measurement on $A$ are random, and the statistics of $B$ do not depend on what $A$ does; this is the [no-communication theorem](/no-communication-theorem/).
- Taking correlation for entanglement. Correlation in one basis is possible with a separable state, as the example above shows.
- Testing one pure state for entanglement by looking at the number of nonzero amplitudes. The rank of the coefficient matrix decides, not the number of terms in one basis.
- Using the partial transpose test as a full test beyond $2 \times 3$. A positive partial transpose in larger systems does not prove separability.

## Where it is used

- **Teleportation and dense coding.** A shared [Bell state](/bell-states/) and two classical bits move one unknown qubit ([quantum teleportation](/quantum-teleportation/)). A shared Bell state and one sent qubit carry two classical bits ([superdense coding](/superdense-coding/)). Entanglement swapping and quantum repeaters chain teleportation to spread entanglement over long distances.
- **Bell tests and cryptography.** Entangled pairs violate the [CHSH inequality](/chsh-inequality/), which no local classical model can do ([Bell's theorem](/bell-theorem/)). Ekert's 1991 protocol builds [key distribution](/key-distribution-problem/) on this, and device-independent randomness generation certifies fresh random bits from the violation.
- **Quantum algorithms and their simulation.** Jozsa and Linden (2003) proved that a pure-state circuit in which every state is a product of blocks of bounded size can be simulated classically in polynomial time, so an exponential speedup with pure states needs entanglement across an unbounded number of qubits. Entanglement is not enough: by the [Gottesman-Knill theorem](/gottesman-knill-theorem/), stabilizer circuits make highly entangled states and are still easy to simulate. Classical simulators of [many-body systems](/quantum-many-body-simulation/) are efficient when the [entanglement entropy](/entanglement-entropy/) across each cut is small.
- **Error correction.** The codewords of a [quantum error-correcting code](/quantum-error-correction/) such as the [Shor code](/shor-code/) are entangled states that spread one logical qubit over many physical qubits, so that no single qubit holds the information.
- **Communication complexity and games.** Shared entanglement lowers the classical communication needed for some tasks ([quantum communication complexity](/quantum-communication-complexity/)) and raises the winning probability of some [two-prover one-round games](/two-prover-one-round-game/), as in the CHSH game.

### History

Einstein, Podolsky and Rosen used an entangled state in 1935 to argue that quantum mechanics is incomplete. Schrödinger named the property in the same year, as "entanglement" in his English paper and "Verschränkung" in German. Bell (1964) turned the question into a testable inequality, and Werner (1989) gave the modern definition of separable mixed states. The Peres and Horodecki partial transpose test followed in 1996.

## References
