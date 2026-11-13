---
tag: 78N3FS
kind: definition
slug: mixed-state
name: Mixed state
aliases:
- statistical mixture of states
- mixed quantum state
area: quantum/quantum-primitives
level: core
summary: "A quantum state whose density matrix has rank 2 or more. No state vector describes it, and many ensembles of pure states give the same one; they are related by a unitary."
prereqs: [density-matrix]
see_also: [quantum-state, partial-trace, entanglement, von-neumann-entropy, bloch-sphere, quantum-channel]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.4.2 (Theorem 2.6, unitary freedom in the ensemble for density matrices) and Section 2.5 (the Schmidt decomposition and purifications)
  - paper: doi:10.1016/0375-9601(93)90880-9
    title: "Lane P. Hughston, Richard Jozsa and William K. Wootters, A complete classification of quantum ensembles having a given density matrix, Physics Letters A 183(1), 1993"
    locator: pp. 14 to 18
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 2.1 (registers and states), Section 2.1.3 (reductions and purifications of quantum states)
---

A mixed state is a quantum state that is not pure: its [density matrix](/density-matrix/) $\rho$ has rank 2 or more, so it is not of the form $|\psi\rangle\langle\psi|$ for any [state vector](/quantum-state/). It arises in two ways: from classical uncertainty about which pure state was prepared, and as the state of one part of a larger system in an entangled pure state. The density matrix page defines the object and its rules; this page is about what makes a state mixed, the many ensembles of pure states that give one mixed state, and how to write each mixed state as part of a pure one.

## Definition

Let $\rho$ be a density matrix on $\mathbb{C}^d$, with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_d \ge 0$ that sum to 1. Then $\rho$ is a **mixed state** if it satisfies one, and so all, of these equivalent conditions:

1. $\operatorname{rank} \rho \ge 2$, that is, at least two eigenvalues are positive.
2. $\rho \ne |\psi\rangle\langle\psi|$ for every unit vector $|\psi\rangle$.
3. The purity is below 1: $\operatorname{Tr}(\rho^2) = \sum_k \lambda_k^2 < 1$.
4. $\rho = p\sigma + (1-p)\tau$ for some density matrices $\sigma \ne \tau$ and some $0 < p < 1$: $\rho$ is not an extreme point of the convex set of states.
5. The [von Neumann entropy](/von-neumann-entropy/) $S(\rho) = -\sum_k \lambda_k \log_2 \lambda_k$ is positive.

Conditions 1 and 2 are equivalent because a rank-one positive matrix of trace 1 is $|e_1\rangle\langle e_1|$. Conditions 2 and 3 are equivalent by the purity bound on the density matrix page, and so are 2 and 4, because the pure states are exactly the extreme points. For condition 5, $-\lambda \log_2 \lambda > 0$ for $0 < \lambda < 1$ and is 0 for $\lambda \in \{0, 1\}$, so the entropy is 0 exactly when one eigenvalue is 1.

A state is **maximally mixed** when $\rho = I/d$. It has purity $1/d$, the smallest possible value, and entropy $\log_2 d$, the largest possible value for a state on $\mathbb{C}^d$.

### Ensembles and the unitary freedom

An **ensemble** for $\rho$ is a list $\{(p_i, |\psi_i\rangle)\}_{i=1}^{m}$ with $p_i \ge 0$, $\sum_i p_i = 1$, unit vectors $|\psi_i\rangle$, and $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$. The vectors need not be orthogonal, and $m$ can be larger than $d$. A pure state has only the trivial ensembles, in which every $|\psi_i\rangle$ with $p_i > 0$ equals $|\psi\rangle$ up to a phase. A mixed state has infinitely many.

It is easier to work with the unnormalized vectors $|\tilde\psi_i\rangle = \sqrt{p_i}\,|\psi_i\rangle$, so that $\rho = \sum_i |\tilde\psi_i\rangle\langle\tilde\psi_i|$.

**Theorem (Hughston, Jozsa and Wootters 1993).** Let $\{|\tilde\psi_i\rangle\}_{i=1}^{m}$ and $\{|\tilde\phi_j\rangle\}_{j=1}^{m}$ be two lists of vectors, with zero vectors added to the shorter list so that both have length $m$. Then $\sum_i |\tilde\psi_i\rangle\langle\tilde\psi_i| = \sum_j |\tilde\phi_j\rangle\langle\tilde\phi_j|$ if and only if there is an $m \times m$ unitary matrix $u$ with

$$|\tilde\psi_i\rangle = \sum_{j=1}^{m} u_{ij} \, |\tilde\phi_j\rangle \qquad \text{for } i = 1, \ldots, m.$$

**Proof.** *If.* $\sum_i |\tilde\psi_i\rangle\langle\tilde\psi_i| = \sum_{j,k} \bigl(\sum_i u_{ij} \overline{u_{ik}}\bigr) |\tilde\phi_j\rangle\langle\tilde\phi_k|$. The inner sum is $(u^\dagger u)_{kj} = \delta_{jk}$, so the result is $\sum_j |\tilde\phi_j\rangle\langle\tilde\phi_j|$.

*Only if.* Let $\rho$ be the common sum, with spectral decomposition $\rho = \sum_{k=1}^{r} \lambda_k |e_k\rangle\langle e_k|$, $\lambda_k > 0$, $r = \operatorname{rank}\rho$. Each $|\tilde\psi_i\rangle$ lies in the span of $|e_1\rangle, \ldots, |e_r\rangle$: if $v$ is orthogonal to that span, then $0 = \langle v|\rho|v\rangle = \sum_i |\langle v|\tilde\psi_i\rangle|^2$, so $v$ is orthogonal to each $|\tilde\psi_i\rangle$. Write $|\tilde\psi_i\rangle = \sum_{k=1}^{r} c_{ik} \sqrt{\lambda_k}\,|e_k\rangle$ with $c_{ik} = \langle e_k|\tilde\psi_i\rangle / \sqrt{\lambda_k}$. Then

$$\rho = \sum_{k,l} \Bigl(\sum_i c_{ik} \overline{c_{il}}\Bigr) \sqrt{\lambda_k \lambda_l}\, |e_k\rangle\langle e_l|,$$

and a comparison with $\sum_k \lambda_k |e_k\rangle\langle e_k|$ gives $\sum_i c_{ik}\overline{c_{il}} = \delta_{kl}$. So the $m \times r$ matrix $c$ has orthonormal columns. Add $m - r$ more orthonormal columns to get an $m \times m$ unitary $C$, and set $|s_k\rangle = \sqrt{\lambda_k}|e_k\rangle$ for $k \le r$ and $|s_k\rangle = 0$ for $k > r$. Then $|\tilde\psi_i\rangle = \sum_k C_{ik} |s_k\rangle$. In the same way $|\tilde\phi_j\rangle = \sum_k D_{jk} |s_k\rangle$ for an $m \times m$ unitary $D$, so $|s_k\rangle = \sum_j \overline{D_{jk}}\, |\tilde\phi_j\rangle$. Substitute this to get $|\tilde\psi_i\rangle = \sum_j (C D^\dagger)_{ij} |\tilde\phi_j\rangle$, and $u = C D^\dagger$ is unitary. $\square$

The proof also shows that each ensemble of $\rho$ comes from the spectral ensemble $\{(\lambda_k, |e_k\rangle)\}$ by a matrix with orthonormal columns. The same theorem appears as Theorem 2.6 of Nielsen and Chuang.

### Purification

Let $\rho$ have rank $r$ and spectral decomposition $\sum_{k=1}^{r} \lambda_k |e_k\rangle\langle e_k|$. Add a reference system $R = \mathbb{C}^{r}$ with orthonormal basis $|1\rangle, \ldots, |r\rangle$. The pure state

$$|\Psi\rangle = \sum_{k=1}^{r} \sqrt{\lambda_k}\, |e_k\rangle \otimes |k\rangle$$

is a **purification** of $\rho$: its [partial trace](/partial-trace/) over $R$ is $\operatorname{Tr}_R |\Psi\rangle\langle\Psi| = \sum_{k,l} \sqrt{\lambda_k\lambda_l}\, |e_k\rangle\langle e_l| \, \langle l|k\rangle = \rho$. So every mixed state is the reduced state of a pure state on a larger system. The reference system needs dimension at least $r$, because the reduced state of $\sum_{j} |\tilde\psi_j\rangle \otimes |j\rangle$ is $\sum_j |\tilde\psi_j\rangle\langle\tilde\psi_j|$, which has rank at most the number of terms.

**Uniqueness up to a unitary on $R$.** Let $|\Psi\rangle$ and $|\Phi\rangle$ be two purifications of $\rho$ on $\mathbb{C}^d \otimes \mathbb{C}^m$. Expand them in a basis of $R$: $|\Psi\rangle = \sum_j |\tilde\psi_j\rangle|j\rangle$ and $|\Phi\rangle = \sum_j |\tilde\phi_j\rangle|j\rangle$. Both lists sum to $\rho$, so by the theorem $|\tilde\psi_i\rangle = \sum_j u_{ij}|\tilde\phi_j\rangle$. Then $|\Psi\rangle = \sum_j |\tilde\phi_j\rangle \otimes \bigl(\sum_i u_{ij}|i\rangle\bigr) = (I \otimes V)|\Phi\rangle$, where $V|j\rangle = \sum_i u_{ij}|i\rangle$ is unitary. So a local operation on the reference changes one purification into the other.

This is why a mixed state can always be seen in two ways. In a *preparation* story, a device picks $|\psi_i\rangle$ with probability $p_i$. In a *reduced state* story, the system is entangled with another system that we do not see. No measurement on the system alone can tell the two stories apart, because both give the same $\rho$.

## Examples and non-examples

**One state, three ensembles.** Take $\rho = \begin{pmatrix} 3/4 & 1/4 \\ 1/4 & 1/4 \end{pmatrix}$, the mixed state of the density matrix page.

1. $|0\rangle$ and $|+\rangle$, each with probability $1/2$. So $|\tilde\psi_1\rangle = (1/\sqrt2, 0)$ and $|\tilde\psi_2\rangle = (1/2, 1/2)$.
2. Apply $u = \frac{1}{\sqrt2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. The new vectors are $(|\tilde\psi_1\rangle + |\tilde\psi_2\rangle)/\sqrt2 = (0.8536, 0.3536)$ and $(|\tilde\psi_1\rangle - |\tilde\psi_2\rangle)/\sqrt2 = (0.1464, -0.3536)$. Their squared lengths are $(2 + \sqrt2)/4 \approx 0.8536$ and $(2 - \sqrt2)/4 \approx 0.1464$. After normalization they are $(\cos\frac{\pi}{8}, \sin\frac{\pi}{8}) = (0.9239, 0.3827)$ and $(\sin\frac{\pi}{8}, -\cos\frac{\pi}{8})$. These are the eigenvectors of $\rho$, so this second ensemble is the spectral one. Here $|0\rangle$ and $|+\rangle$ are symmetric about the angle $\pi/8$, and $u$ takes their sum and difference.
3. The four states $|0\rangle, |1\rangle, |+\rangle, |-\rangle$ with probabilities $1/2, 0, 1/2, 0$ also give $\rho$. Lists of any length $m \ge \operatorname{rank}\rho$ are possible.

**A purification of the same state.** $|\Psi\rangle = \frac{1}{\sqrt2}\bigl(|0\rangle|0\rangle + |+\rangle|1\rangle\bigr)$ on the system and a reference qubit. The reduced state is $\frac12|0\rangle\langle0| + \frac12|+\rangle\langle+| = \rho$, because the reference states $|0\rangle$ and $|1\rangle$ are orthogonal. Any ensemble gives a purification in this way.

**The maximally mixed qubit.** $I/2$ is the equal mixture of $|0\rangle, |1\rangle$, of $|+\rangle, |-\rangle$, and of any two orthogonal states. It is also the equal mixture of the three states $|0\rangle$, $\frac12|0\rangle + \frac{\sqrt3}{2}|1\rangle$ and $\frac12|0\rangle - \frac{\sqrt3}{2}|1\rangle$, whose Bloch vectors are at 120 degrees in a plane and sum to zero. Its purification $(|00\rangle + |11\rangle)/\sqrt2$ is a [Bell state](/bell-states/).

**Non-examples.**

- $|+\rangle = (|0\rangle + |1\rangle)/\sqrt2$ is a superposition, not a mixture. Its density matrix $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ has rank 1 and purity 1.
- The "ensemble" $|0\rangle$ with probability $1/2$ and $-|0\rangle$ with probability $1/2$ is the pure state $|0\rangle\langle0|$. A global phase does not make a mixture.
- A classical [probability distribution](/probability-distribution/) over bit strings is a diagonal density matrix. It is mixed, but it has no coherences, so it is a special case and not the general one.

### Common errors

- **"Mixed" means "unknown pure state".** That is one reading of a preparation. The same $\rho$ is also the reduced state of an entangled pure state, and then no pure state of the system alone exists.
- **Ensemble weights are not eigenvalues.** In example 1 the weights are $1/2, 1/2$, but the eigenvalues are $0.8536$ and $0.1464$. Only the spectral ensemble has the eigenvalues as weights. For other ensembles the eigenvalues are more spread out than the weights: here the largest eigenvalue $0.8536$ is above the largest weight $0.5$.
- **Shorter lists.** The theorem needs both lists padded to the same length with zero vectors. Without the padding, an ensemble of 2 states and one of 3 states cannot be related by a square unitary.
- **Entanglement versus mixedness.** A mixed state of two systems can be a product $\rho_A \otimes \rho_B$, with no [entanglement](/entanglement/) at all. A pure joint state can have mixed parts.

## Related definitions

- [Density matrix](/density-matrix/): the matrix that describes each state, pure or mixed.
- [Quantum state](/quantum-state/): the unit vectors, which describe the pure states only.
- [Partial trace](/partial-trace/): the reduced state of a part, the second origin of mixed states.
- [Entanglement](/entanglement/): a pure joint state is entangled exactly when its reduced states are mixed.
- [Von Neumann entropy](/von-neumann-entropy/): a measure of how mixed a state is, 0 exactly for pure states.
- [Bloch sphere](/bloch-sphere/): mixed qubit states are the points strictly inside the ball.
- [Quantum channel](/quantum-channel/): noise maps pure states to mixed states.

### History

Hughston, Jozsa and Wootters gave the classification of all ensembles of a density matrix in 1993, with the unitary relation above.

## References
