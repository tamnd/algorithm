---
tag: Z8AWR0
kind: definition
slug: partial-trace
name: Partial trace
aliases:
- reduced density matrix
area: quantum/quantum-primitives
level: advanced
summary: "The linear map Tr_B from operators on A tensor B to operators on A with Tr_B(X tensor Y) = X Tr Y. It gives the state of part A that predicts every measurement on A."
prereqs: [density-matrix, tensor-product]
see_also: [mixed-state, entanglement, entanglement-entropy, von-neumann-entropy, quantum-channel, no-communication-theorem, bell-states, kronecker-product]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.4.3 (The reduced density operator) and Section 8.3.1 (trace and partial trace as quantum operations)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 2.1.3 (reductions and purifications of quantum states)
---

The partial trace takes an operator on a composite system $A \otimes B$ to an operator on $A$ alone. Applied to a [density matrix](/density-matrix/) $\rho_{AB}$ of the whole system, it gives the **reduced density matrix** $\rho_A = \operatorname{Tr}_B \rho_{AB}$: the unique state of $A$ that gives the same probabilities as $\rho_{AB}$ for every measurement on $A$. When $\rho_{AB}$ is an entangled pure state, $\rho_A$ is a [mixed state](/mixed-state/), so the partial trace is the second source of mixed states, after classical uncertainty.

## Definition

Let $\mathcal{H}_A = \mathbb{C}^{d_A}$ and $\mathcal{H}_B = \mathbb{C}^{d_B}$, and write $L(\mathcal{H})$ for the linear operators on $\mathcal{H}$. The **partial trace over $B$** is the linear map $\operatorname{Tr}_B : L(\mathcal{H}_A \otimes \mathcal{H}_B) \to L(\mathcal{H}_A)$ with

$$\operatorname{Tr}_B (X \otimes Y) = X \cdot \operatorname{Tr} Y \qquad \text{for all } X \in L(\mathcal{H}_A),\ Y \in L(\mathcal{H}_B).$$

The products $X \otimes Y$ span $L(\mathcal{H}_A \otimes \mathcal{H}_B)$, so this fixes $\operatorname{Tr}_B$ on every operator. The partial trace over $A$, $\operatorname{Tr}_A(X \otimes Y) = \operatorname{Tr} X \cdot Y$, is the same construction with the roles changed.

**In coordinates.** Take orthonormal bases $|a\rangle$ of $\mathcal{H}_A$ and $|b\rangle$ of $\mathcal{H}_B$, and write $\rho_{(a,b),(a',b')} = \langle a, b|\rho|a', b'\rangle$. Then

$$(\operatorname{Tr}_B \rho)_{a a'} = \sum_{b=1}^{d_B} \rho_{(a,b),(a',b)}, \qquad (\operatorname{Tr}_A \rho)_{b b'} = \sum_{a=1}^{d_A} \rho_{(a,b),(a,b')}.$$

In the order with $A$ as the high-order part (index $a \cdot d_B + b$), cut $\rho$ into $d_A \times d_A$ blocks of size $d_B \times d_B$. Then entry $(a, a')$ of $\operatorname{Tr}_B \rho$ is the trace of block $(a, a')$, and $\operatorname{Tr}_A \rho$ is the sum of the $d_A$ diagonal blocks. With the operators $I_A \otimes \langle b|$, the same formula reads

$$\operatorname{Tr}_B \rho = \sum_{b=1}^{d_B} (I_A \otimes \langle b|)\, \rho\, (I_A \otimes |b\rangle).$$

For $\rho = X \otimes Y$ the sum is $X \sum_b \langle b|Y|b\rangle = X \operatorname{Tr} Y$, so the three descriptions agree. The result does not depend on the basis of $B$: if $|f_k\rangle = \sum_b U_{bk}|b\rangle$ for a unitary $U$, then $\sum_k (I \otimes \langle f_k|)\rho(I \otimes |f_k\rangle) = \sum_{b,b'} (U U^\dagger)_{b'b}\,(I \otimes \langle b|)\rho(I \otimes |b'\rangle)$, and $U U^\dagger = I$ leaves the sum over $b = b'$.

### The characterization by measurements

**Theorem.** For each $\rho \in L(\mathcal{H}_A \otimes \mathcal{H}_B)$, $\rho_A = \operatorname{Tr}_B \rho$ is the unique operator on $\mathcal{H}_A$ with

$$\operatorname{Tr}(\rho_A X) = \operatorname{Tr}\bigl(\rho\, (X \otimes I_B)\bigr) \qquad \text{for all } X \in L(\mathcal{H}_A).$$

**Proof.** *The partial trace satisfies it.* Both sides are linear in $\rho$, so it is enough to take $\rho = Y_A \otimes Y_B$. Then $\operatorname{Tr}(\rho\,(X \otimes I)) = \operatorname{Tr}(Y_A X \otimes Y_B) = \operatorname{Tr}(Y_A X)\operatorname{Tr}(Y_B) = \operatorname{Tr}\bigl((\operatorname{Tr}_B \rho) X\bigr)$.

*Uniqueness.* If $\sigma$ and $\sigma'$ both satisfy it, then $\operatorname{Tr}((\sigma - \sigma') X) = 0$ for all $X$. Take $X = |a'\rangle\langle a|$ to get $\langle a|(\sigma - \sigma')|a'\rangle = 0$ for all $a, a'$, so $\sigma = \sigma'$. $\square$

With $X$ a projector $P_m$ of a measurement on $A$, the theorem says that the [Born rule](/born-rule/) probability $\operatorname{Tr}((P_m \otimes I)\rho)$ equals $\operatorname{Tr}(P_m \rho_A)$. Expectations of observables on $A$ agree in the same way. This is why $\rho_A$ is *the* state of $A$: no other operator predicts all measurements on $A$, and any other choice, such as the top-left block of $\rho$, gives wrong probabilities for some measurement.

### Properties

- **States go to states.** $\operatorname{Tr}(\operatorname{Tr}_B \rho) = \operatorname{Tr}\rho$ (take $X = I$ above), $(\operatorname{Tr}_B\rho)^\dagger = \operatorname{Tr}_B(\rho^\dagger)$, and $\langle v|\operatorname{Tr}_B\rho|v\rangle = \sum_b \langle v, b|\rho|v, b\rangle \ge 0$ when $\rho \ge 0$. So the reduced matrix of a density matrix is a density matrix.
- **It is a quantum channel.** The sandwich formula is a Kraus form with the $d_B$ operators $K_b = I_A \otimes \langle b|$, and $\sum_b K_b^\dagger K_b = I_A \otimes I_B$. So $\operatorname{Tr}_B$ is a completely positive, trace preserving map: a [quantum channel](/quantum-channel/) with [Kraus operators](/kraus-operators/) $K_b$.
- **Operators on $A$ come out.** $\operatorname{Tr}_B\bigl((X \otimes I)\rho(Y \otimes I)\bigr) = X(\operatorname{Tr}_B\rho)Y$.
- **Operations on $B$ do not change $\rho_A$.** For operators $Y, Z$ on $B$, $\operatorname{Tr}_B\bigl((I \otimes Y)\rho(I \otimes Z)\bigr) = \operatorname{Tr}_B\bigl((I \otimes ZY)\rho\bigr)$. So for a unitary $U$ on $B$, or for any channel on $B$ with Kraus operators $\sum_k K_k^\dagger K_k = I$, the reduced state of $A$ stays the same. This is the content of the [no-communication theorem](/no-communication-theorem/).
- **Products.** $\operatorname{Tr}_B(\sigma \otimes \tau) = \sigma$ for density matrices $\sigma, \tau$.
- **In steps.** On $A \otimes B \otimes C$, $\operatorname{Tr}_{BC} = \operatorname{Tr}_B \circ \operatorname{Tr}_C$, and the order of the steps does not matter.

### Pure joint states

Let $|\psi\rangle = \sum_{a,b} M_{ab}\,|a\rangle|b\rangle$ with a $d_A \times d_B$ coefficient matrix $M$. The coordinate formula gives

$$\rho_A = \operatorname{Tr}_B |\psi\rangle\langle\psi| = M M^\dagger, \qquad \rho_B = \operatorname{Tr}_A |\psi\rangle\langle\psi| = M^{T} \overline{M} = (M^\dagger M)^{T}.$$

The matrices $M M^\dagger$ and $M^\dagger M$ have the same nonzero eigenvalues, the squares of the [singular values](/singular-value-decomposition/) of $M$. So the two parts of a pure joint state have the same nonzero spectrum and the same [von Neumann entropy](/von-neumann-entropy/), the [entanglement entropy](/entanglement-entropy/) of $|\psi\rangle$. The state is a product exactly when $M$ has rank 1, that is, when $\rho_A$ is pure.

### Qubit order

On $n$ qubits these pages number qubit 0 as the least significant bit of a basis index, so the space is (qubit $n-1$) $\otimes \cdots \otimes$ (qubit 0). To trace out qubit $q$, sum the entries $\rho_{ij}$ over the pairs of indices $i, j$ whose bit $q$ is equal, and drop bit $q$ from both. On two qubits with the index $2 q_1 + q_0$, $\operatorname{Tr}_B$ in the formulas above, with $A$ the high-order part, traces out qubit 0.

## Examples and non-examples

**A worked example.** Take $|\psi\rangle = \frac{1}{\sqrt3}\bigl(|00\rangle + |01\rangle + |10\rangle\bigr)$, with the left factor as $A$ (qubit 1) and the right factor as $B$ (qubit 0). Then $M = \frac{1}{\sqrt3}\begin{pmatrix}1 & 1\\ 1 & 0\end{pmatrix}$ and

$$\rho_A = M M^\dagger = \frac13 \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}.$$

From the coordinate formula: $(\rho_A)_{00} = \rho_{(0,0),(0,0)} + \rho_{(0,1),(0,1)} = \frac13 + \frac13$, and $(\rho_A)_{01} = \rho_{(0,0),(1,0)} + \rho_{(0,1),(1,1)} = \frac13 + 0$. The state is symmetric in $A$ and $B$, so $\rho_B$ is the same matrix. Its eigenvalues are $(3 \pm \sqrt5)/6 \approx 0.873$ and $0.127$, its purity is $(4 + 1 + 1 + 1)/9 = 7/9$, and so the state of each qubit is mixed although the joint state is pure.

**Bell states.** For $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt2$, $M = I/\sqrt2$, so $\rho_A = \rho_B = I/2$. Each part of a [Bell state](/bell-states/) is maximally mixed. The product $\rho_A \otimes \rho_B = I/4$ is not $|\Phi^+\rangle\langle\Phi^+|$: the reduced states lose the correlations.

**Three qubits.** For $(|000\rangle + |111\rangle)/\sqrt2$, tracing out one qubit gives $\frac12(|00\rangle\langle00| + |11\rangle\langle11|)$, a classical mixture with no entanglement left. For $(|001\rangle + |010\rangle + |100\rangle)/\sqrt3$, tracing out qubits 1 and 2 gives $\operatorname{diag}(2/3, 1/3)$ on qubit 0.

**Non-examples.**

- The top-left $d_A \times d_A$ block of $\rho$, or the block with $b = 0$, is not $\operatorname{Tr}_B\rho$. For $|\Phi^+\rangle$ it is $\operatorname{diag}(1/2, 0)$, of trace $1/2$.
- The partial transpose $(X \otimes Y) \mapsto X \otimes Y^{T}$ keeps the dimension and is not a partial trace. It is not even a channel.
- $\operatorname{Tr}_B$ is not multiplicative: $\operatorname{Tr}_B(\rho\sigma) \ne \operatorname{Tr}_B(\rho)\operatorname{Tr}_B(\sigma)$ in general. For $\rho = \sigma = |\Phi^+\rangle\langle\Phi^+|$ the left side is $I/2$ and the right side is $I/4$.

### Common errors

- **The wrong digit.** In the index $a \cdot d_B + b$, the $B$ digit is $b = i \bmod d_B$. Summing over the other digit gives $\operatorname{Tr}_A$. With qubits, check which qubit is the least significant bit before you trace one out.
- **Rebuilding the state from its parts.** $\rho_A \otimes \rho_B = \rho_{AB}$ holds only for product states. The reduced states describe each part alone, not the correlations.
- **Measuring $B$ changes $\rho_A$.** A measurement on $B$ whose result is not seen leaves $\rho_A$ the same. Only when the result is known does the state of $A$ change, to the conditional state for that result.

### Implementation

The Python code with this page computes the partial trace over any set of systems with the coordinate formula, in $O(D^2)$ steps for total dimension $D$, and also through the sandwich formula. Its tests check the defining property on random states, the product rule, the Bell and three-qubit examples, the qubit order, tracing out in steps, and the equal spectra of the two parts of random pure states.

## Related definitions

- [Density matrix](/density-matrix/): the input and the output of the partial trace.
- [Mixed state](/mixed-state/): the reduced state of an entangled pure state is mixed, and every mixed state arises in this way from a purification.
- [Tensor product](/tensor-product/) and [Kronecker product](/kronecker-product/): the composite space and the matrices on it.
- [Entanglement](/entanglement/) and [entanglement entropy](/entanglement-entropy/): measured through the reduced states.
- [Quantum channel](/quantum-channel/): the partial trace is a channel, and every channel is a unitary followed by a partial trace.
- [No-communication theorem](/no-communication-theorem/): operations on $B$ cannot change $\rho_A$.

### History

Landau's 1927 paper on damping in wave mechanics described a system coupled to radiation by a density matrix of the system alone, and it is often cited as the first use of a reduced state. Nielsen and Chuang give the measurement characterization above as the reason that the partial trace is the right reduced state.

## References
