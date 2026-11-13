---
tag: XS6DA3
kind: definition
slug: kraus-operators
name: Kraus operators
aliases:
- Kraus representation
area: quantum/quantum-primitives
level: advanced
summary: "Matrices K_k with sum K_k^dagger K_k = I that write a quantum channel as rho -> sum K_k rho K_k^dagger. Every channel has such a list, with at most d_in d_out terms."
prereqs: [quantum-channel, partial-trace]
see_also: [mixed-state, density-matrix, pauli-gates, binary-symmetric-channel, quantum-error-correction, open-quantum-system-simulation, spectral-theorem, kronecker-product]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 8.2.3 (the operator-sum representation), Section 8.2.4 (the axiomatic approach and the unitary freedom), Sections 8.3.3 to 8.3.6 (bit flip, phase flip, depolarizing, amplitude damping and phase damping)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 2.2.2 (the Choi, Kraus and Stinespring representations of channels and the characterizations of complete positivity)
  - book: doi:10.1007/3-540-12732-1
    title: "Karl Kraus, States, Effects, and Operations: Fundamental Notions of Quantum Theory, Lecture Notes in Physics 190, Springer, 1983"
    locator: the representation theorem for operations
  - paper: doi:10.1016/0024-3795(75)90075-0
    title: Man-Duen Choi, Completely positive linear maps on complex matrices, Linear Algebra and its Applications 10(3), 1975
    locator: pp. 285 to 290
  - paper: doi:10.1090/S0002-9939-1955-0069403-4
    title: W. Forrest Stinespring, Positive functions on C*-algebras, Proceedings of the American Mathematical Society 6(2), 1955
    locator: pp. 211 to 216
---

Kraus operators are a list of matrices $K_1, \ldots, K_r$ that describe a [quantum channel](/quantum-channel/) $\Phi$ by

$$\Phi(\rho) = \sum_{k=1}^{r} K_k \,\rho\, K_k^\dagger, \qquad \sum_{k=1}^{r} K_k^\dagger K_k = I.$$

This is the **Kraus representation**, or operator-sum representation. Every completely positive, trace preserving map has one, and every list that satisfies the second equation defines a channel. The list is not unique: two lists give the same channel exactly when a unitary matrix relates them. The quantum channel page gives the definition of a channel and its general properties; this page is about the lists of operators, how to find one, and how they relate to the Stinespring and Choi forms.

## Definition

Let $\mathcal{H}_{in} = \mathbb{C}^{d_{in}}$ and $\mathcal{H}_{out} = \mathbb{C}^{d_{out}}$. A **Kraus representation** of a linear map $\Phi$ from $d_{in} \times d_{in}$ matrices to $d_{out} \times d_{out}$ matrices is a list of $d_{out} \times d_{in}$ matrices $K_1, \ldots, K_r$ with $\Phi(X) = \sum_k K_k X K_k^\dagger$ for all $X$. The $K_k$ are the **Kraus operators** of $\Phi$.

- The map preserves the trace exactly when $\sum_k K_k^\dagger K_k = I_{in}$: $\operatorname{Tr}\Phi(X) = \operatorname{Tr}\bigl(\sum_k K_k^\dagger K_k\, X\bigr)$ for all $X$, and this equals $\operatorname{Tr} X$ for all $X$ only when the sum is $I$.
- A map with a Kraus form is completely positive: $(\Phi \otimes \mathrm{id}_m)(P) = \sum_k (K_k \otimes I_m) P (K_k \otimes I_m)^\dagger$ is a sum of positive semidefinite matrices when $P \ge 0$.

When $\sum_k K_k^\dagger K_k \le I$ instead, the map decreases the trace. Such maps describe one outcome of a measurement, and the probability of that outcome is $\operatorname{Tr}\Phi(\rho)$.

### The representation theorem

**Theorem (Kraus, Choi).** Every completely positive linear map $\Phi$ has a Kraus representation with $r = \operatorname{rank} J(\Phi) \le d_{in} d_{out}$ operators, where

$$J(\Phi) = \sum_{i,j=1}^{d_{in}} \Phi\bigl(|i\rangle\langle j|\bigr) \otimes |i\rangle\langle j|$$

is the **Choi matrix** of $\Phi$, a $d_{out} d_{in} \times d_{out} d_{in}$ matrix.

**Proof.** $J(\Phi) = (\Phi \otimes \mathrm{id})(|\Omega\rangle\langle\Omega|)$ with $|\Omega\rangle = \sum_i |i\rangle|i\rangle$, because $|\Omega\rangle\langle\Omega| = \sum_{i,j} |i\rangle\langle j| \otimes |i\rangle\langle j|$. Since $\Phi$ is completely positive and $|\Omega\rangle\langle\Omega| \ge 0$, $J \ge 0$. By the [spectral theorem](/spectral-theorem/), $J = \sum_{k=1}^{r} \lambda_k |v_k\rangle\langle v_k|$ with $\lambda_k > 0$ and $r = \operatorname{rank} J$. Write the entries of $v_k$ as $v_k[o, i]$, with $o$ the output index and $i$ the input index, and define the $d_{out} \times d_{in}$ matrix $(K_k)_{oi} = \sqrt{\lambda_k}\, v_k[o, i]$. Then for each pair $i, j$, the $(o, o')$ entry of $\sum_k K_k |i\rangle\langle j| K_k^\dagger$ is

$$\sum_k \lambda_k\, v_k[o, i]\, \overline{v_k[o', j]} = J_{(o,i),(o',j)} = \bigl\langle o \big| \Phi(|i\rangle\langle j|) \big| o' \bigr\rangle.$$

So $\Phi$ and $X \mapsto \sum_k K_k X K_k^\dagger$ agree on every matrix unit $|i\rangle\langle j|$, and by linearity on every matrix. The matrix $J$ has size $d_{out} d_{in}$, so $r \le d_{in} d_{out}$. $\square$

For a channel from a $d$-dimensional system to itself the bound is $d^2$, and it is reached: the completely depolarizing qubit channel $\rho \mapsto \operatorname{Tr}(\rho) I/2$ has $J = I_4/2$ of rank 4, so no list of 3 Kraus operators describes it.

### Unitary freedom

**Theorem.** Let $\{K_k\}_{k=1}^{m}$ and $\{F_j\}_{j=1}^{m}$ be two lists, with zero matrices added to the shorter one. They give the same map if and only if $F_j = \sum_k u_{jk} K_k$ for an $m \times m$ unitary $u$.

**Proof.** The proof of the representation theorem shows that $J(\Phi) = \sum_k |\kappa_k\rangle\langle\kappa_k|$, where $|\kappa_k\rangle$ is the vector of the entries of $K_k$, in the order $(o, i)$. The same holds for the $F_j$. Two lists give the same map exactly when they give the same $J$, and by the theorem of Hughston, Jozsa and Wootters on the [mixed state](/mixed-state/) page, $\sum_k |\kappa_k\rangle\langle\kappa_k| = \sum_j |\phi_j\rangle\langle\phi_j|$ exactly when the vectors are related by a unitary. $\square$

So the minimal number of Kraus operators is $\operatorname{rank} J$, and each list with this number comes from the spectral list by a unitary.

### The Stinespring form

Given Kraus operators $K_1, \ldots, K_r$ of a channel, define

$$V = \sum_{k=1}^{r} K_k \otimes |k\rangle : \mathbb{C}^{d_{in}} \to \mathbb{C}^{d_{out}} \otimes \mathbb{C}^{r}.$$

Then $V^\dagger V = \sum_{k,l} K_k^\dagger K_l \langle k|l\rangle = \sum_k K_k^\dagger K_k = I$, so $V$ is an isometry, and the [partial trace](/partial-trace/) over the second factor gives

$$\operatorname{Tr}_E\bigl(V\rho V^\dagger\bigr) = \sum_{k,l} K_k \rho K_l^\dagger\, \langle l|k\rangle = \sum_k K_k \rho K_k^\dagger = \Phi(\rho).$$

Conversely, for each isometry $V$ into $\mathcal{H}_{out} \otimes \mathbb{C}^r$, the operators $K_k = (I \otimes \langle k|)V$ are Kraus operators of $\rho \mapsto \operatorname{Tr}_E(V\rho V^\dagger)$. This is Stinespring's form: a channel is an isometry into a larger system, followed by discarding the environment $E$. When $d_{in} = d_{out} = d$, $V$ extends to a unitary $U$ on $\mathbb{C}^d \otimes \mathbb{C}^r$ with $U(|\psi\rangle|0\rangle) = V|\psi\rangle$, so $\Phi(\rho) = \operatorname{Tr}_E\bigl(U(\rho \otimes |0\rangle\langle0|)U^\dagger\bigr)$. Each Kraus operator is one way that the environment can change: if the environment were measured in the basis $|k\rangle$, result $k$ would occur with probability $\operatorname{Tr}(K_k\rho K_k^\dagger)$ and leave the state $K_k \rho K_k^\dagger$ up to normalization.

## Examples and non-examples

The standard qubit channels, with $\rho = \frac12(I + r_x X + r_y Y + r_z Z)$ and $X, Y, Z$ the [Pauli matrices](/pauli-gates/):

| channel | Kraus operators | Bloch vector after the channel |
|---|---|---|
| bit flip, probability $p$ | $\sqrt{1-p}\,I$, $\sqrt{p}\,X$ | $(r_x,\ (1-2p) r_y,\ (1-2p) r_z)$ |
| phase flip, probability $p$ | $\sqrt{1-p}\,I$, $\sqrt{p}\,Z$ | $((1-2p) r_x,\ (1-2p) r_y,\ r_z)$ |
| depolarizing, $\rho \mapsto (1-p)\rho + p I/2$ | $\sqrt{1 - 3p/4}\,I$, $\frac{\sqrt p}{2} X$, $\frac{\sqrt p}{2} Y$, $\frac{\sqrt p}{2} Z$ | $(1-p)(r_x, r_y, r_z)$ |
| amplitude damping, $\gamma$ | $\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}$, $\begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}$ | $(\sqrt{1-\gamma}\,r_x,\ \sqrt{1-\gamma}\,r_y,\ \gamma + (1-\gamma) r_z)$ |
| phase damping, $\lambda$ | $\begin{pmatrix}1&0\\0&\sqrt{1-\lambda}\end{pmatrix}$, $\begin{pmatrix}0&0\\0&\sqrt\lambda\end{pmatrix}$ | $(\sqrt{1-\lambda}\,r_x,\ \sqrt{1-\lambda}\,r_y,\ r_z)$ |

On the computational basis, the bit flip channel acts as the classical [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $p$. Phase flip and phase damping are the same channel with $1 - 2p = \sqrt{1 - \lambda}$, which shows the unitary freedom: the two lists are related by a $2 \times 2$ unitary.

**Amplitude damping, step by step.** Take $\gamma = 0.4$ and $\rho = |+\rangle\langle+| = \frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$. Then $K_1\rho K_1^\dagger = \frac12\begin{pmatrix}1 & \sqrt{0.6}\\ \sqrt{0.6} & 0.6\end{pmatrix}$ and $K_2\rho K_2^\dagger = \frac12\begin{pmatrix}0.4 & 0\\ 0 & 0\end{pmatrix}$, so

$$\Phi(\rho) = \begin{pmatrix} 0.7 & 0.3873 \\ 0.3873 & 0.3 \end{pmatrix}, \qquad r = (0.7746,\ 0,\ 0.4).$$

This agrees with the table: $\sqrt{1-\gamma} = 0.7746$ and $\gamma + (1-\gamma)\cdot 0 = 0.4$. On $|1\rangle\langle1|$ the output is $\operatorname{diag}(0.4, 0.6)$: the excited state decays with probability $\gamma$.

**Two lists for one channel.** The completely depolarizing channel $\rho \mapsto I/2$ (depolarizing with $p = 1$) has the Kraus operators $\frac12 I, \frac12 X, \frac12 Y, \frac12 Z$. The spectral list from its Choi matrix $I_4/2$ has four other operators, and a $4 \times 4$ unitary maps one list to the other.

**A unitary and the partial trace.** A unitary $U$ is a channel with the single Kraus operator $U$, and its Choi matrix has rank 1. The partial trace $\operatorname{Tr}_B$ has the $d_B$ Kraus operators $I_A \otimes \langle b|$.

**Non-examples.**

- The transpose $\rho \mapsto \rho^{T}$ maps states to states, but its Choi matrix is the swap operator, with eigenvalue $-1$. So it is not completely positive and has no Kraus form.
- One operator $K = \operatorname{diag}(1, 1/2)$ gives a completely positive map, but $K^\dagger K = \operatorname{diag}(1, 1/4) \ne I$: it loses trace and is not a channel.
- Mixing the Kraus operators with a matrix that is not unitary, such as $F_1 = K_1 + K_2$, $F_2 = K_2$, gives a different map.

### Common errors

- **$K^\dagger K$ versus $K K^\dagger$.** Trace preservation is $\sum_k K_k^\dagger K_k = I$. The condition $\sum_k K_k K_k^\dagger = I$ means that the channel maps $I/d$ to $I/d$ (a unital channel). Amplitude damping satisfies the first but not the second.
- **Probabilities outside the operators.** In $\sqrt{p}\,X$ the square root is needed, because the operator appears twice in $K\rho K^\dagger$.
- **Counting operators.** A channel has many Kraus lists of many lengths. Only the minimal length $\operatorname{rank} J$ is a property of the channel. For a channel from $d_{in}$ to $d_{out}$ dimensions the bound is $d_{in} d_{out}$, which is $d^2$ only when both are $d$.
- **The order in $J$.** Some books place the input factor first in the Choi matrix. Then the entries of $v_k$ are read in the order $(i, o)$. Either order works if it is used in the same way throughout.

### Implementation

The Python code with this page applies a channel from its Kraus list, checks trace preservation, builds the Stinespring isometry and applies the channel through it with a partial trace, builds the Choi matrix, and gets a minimal Kraus list back from the eigenvectors of the Choi matrix. Its tests compare the Kraus and Stinespring outputs on random channels and states, check the Bloch formulas of the table, check that the Choi matrices are positive semidefinite with $\operatorname{Tr}_{out} J = I$, check that a unitary mix of a list gives the same Choi matrix, and check that the transpose has a negative Choi eigenvalue.

## Related definitions

- [Quantum channel](/quantum-channel/): the completely positive, trace preserving maps that Kraus operators describe.
- [Partial trace](/partial-trace/): the last step of the Stinespring form, and itself a channel with Kraus operators $I \otimes \langle b|$.
- [Mixed state](/mixed-state/): the same unitary freedom holds for the ensembles of a density matrix.
- [Pauli gates](/pauli-gates/): the Kraus operators of the flip and depolarizing channels.
- [Quantum error correction](/quantum-error-correction/): a code corrects a channel when it corrects each of its Kraus operators, and so each linear combination of them.
- [Open quantum system simulation](/open-quantum-system-simulation/): simulating a channel or a Lindblad equation through its Kraus operators or a Stinespring dilation.

### History

Stinespring proved his dilation theorem for completely positive maps on C*-algebras in 1955. Choi characterized the completely positive maps on matrices by the positivity of the Choi matrix in 1975, and his proof gives the Kraus form with the bound on its length. Kraus developed the operator-sum description of quantum operations, collected in his 1983 lecture notes.

## References
