---
tag: ZST7G3
kind: definition
slug: quantum-channel
name: Quantum channel
aliases:
- quantum operation
- CPTP map
area: quantum/quantum-primitives
level: advanced
summary: "A linear map on density matrices that is completely positive and trace preserving. It is the most general physical change of a quantum state, noise included."
prereqs: [density-matrix, tensor-product]
see_also: [kraus-operators, partial-trace, trace-distance, fidelity, binary-symmetric-channel, channel-capacity, quantum-error-correction, open-quantum-system-simulation]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 8.2 (quantum operations, with 8.2.3 the operator-sum representation and 8.2.4 the axiomatic approach) and Section 8.3 (examples of quantum noise)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 2.2 (quantum channels), with 2.2.2 (representations and characterizations) and 2.2.3 (examples)
  - paper: doi:10.1016/0024-3795(75)90075-0
    title: Man-Duen Choi, Completely positive linear maps on complex matrices, Linear Algebra and its Applications 10(3), 1975
    locator: pp. 285 to 290
  - paper: doi:10.1016/0034-4877(72)90011-0
    title: Andrzej Jamiołkowski, Linear transformations which preserve trace and positive semidefiniteness of operators, Reports on Mathematical Physics 3(4), 1972
    locator: pp. 275 to 278
  - paper: doi:10.1090/S0002-9939-1955-0069403-4
    title: W. Forrest Stinespring, Positive functions on C*-algebras, Proceedings of the American Mathematical Society 6(2), 1955
    locator: pp. 211 to 216
  - paper: doi:10.1070/RM1997v052n06ABEH002155
    title: "A. Yu. Kitaev, Quantum computations: algorithms and error correction, Russian Mathematical Surveys 52(6), 1997"
    locator: pp. 1191 to 1249 (the norm on superoperators now called the diamond norm)
  - paper: doi:10.1007/BF01608499
    title: Göran Lindblad, On the generators of quantum dynamical semigroups, Communications in Mathematical Physics 48(2), 1976
    locator: pp. 119 to 130
---

A quantum channel is a linear map $\Phi$ that takes [density matrices](/density-matrix/) of one system to density matrices of another, in a way that stays valid when the system is part of a larger one. Formally, $\Phi$ is completely positive and trace preserving (CPTP). Unitary evolution, adding or discarding a system, measurement whose result is forgotten, and every kind of noise are channels. A closed system evolves by a unitary; an open system, one that interacts with an environment we do not track, evolves by a channel. The [Kraus operators](/kraus-operators/) page gives the main way to write a channel down.

## Definition

Write $L(\mathbb{C}^d)$ for the $d \times d$ complex matrices. A linear map $\Phi : L(\mathbb{C}^{d_{in}}) \to L(\mathbb{C}^{d_{out}})$ is

1. **positive** if $\Phi(P) \ge 0$ for every positive semidefinite $P$;
2. **completely positive** if $\Phi \otimes \mathrm{id}_m$ is positive for every $m \ge 1$, where $\mathrm{id}_m$ is the identity map on $L(\mathbb{C}^m)$;
3. **trace preserving** if $\operatorname{Tr}\Phi(X) = \operatorname{Tr} X$ for every $X$.

A **quantum channel** is a linear map that is completely positive and trace preserving. It maps density matrices to density matrices, and so does $\Phi \otimes \mathrm{id}_m$ for every $m$.

Linearity comes from ensembles: if a system is in state $\rho_i$ with probability $p_i$, the output must be $\Phi(\rho_i)$ with probability $p_i$, so $\Phi(\sum_i p_i\rho_i) = \sum_i p_i \Phi(\rho_i)$. Complete positivity is needed because the system can be entangled with a second system $R$ that the channel does not touch. The joint state then changes by $\Phi \otimes \mathrm{id}$, and that output must also be a state. Positivity alone does not ensure this; the transpose map below is the standard example.

**Quantum operation.** Nielsen and Chuang use the term *quantum operation* for the larger class of completely positive maps with $\operatorname{Tr}\Phi(\rho) \le \operatorname{Tr}\rho$. Such a map describes one outcome of a process, and $\operatorname{Tr}\Phi(\rho)$ is the probability of that outcome. A channel is a quantum operation that preserves the trace.

### Choi's theorem

The **Choi matrix** of a linear map $\Phi$ is the $d_{out} d_{in} \times d_{out} d_{in}$ matrix

$$J(\Phi) = \sum_{i,j=1}^{d_{in}} \Phi\bigl(|i\rangle\langle j|\bigr) \otimes |i\rangle\langle j| = (\Phi \otimes \mathrm{id})\bigl(|\Omega\rangle\langle\Omega|\bigr), \qquad |\Omega\rangle = \sum_{i} |i\rangle|i\rangle.$$

The map is recovered from it by $\Phi(X) = \operatorname{Tr}_{in}\bigl(J(\Phi)\,(I \otimes X^{T})\bigr)$, because $\operatorname{Tr}(|i\rangle\langle j|\,X^{T}) = X_{ij}$ and $\Phi(X) = \sum_{i,j} X_{ij}\, \Phi(|i\rangle\langle j|)$. So $\Phi \mapsto J(\Phi)$ is a linear bijection between maps and matrices; this is the Choi-Jamiołkowski correspondence.

**Theorem (Choi 1975).** A linear map $\Phi$ is completely positive if and only if $J(\Phi) \ge 0$. It is trace preserving if and only if $\operatorname{Tr}_{out} J(\Phi) = I_{in}$.

**Proof.** If $\Phi$ is completely positive, then $J = (\Phi \otimes \mathrm{id}_{d_{in}})(|\Omega\rangle\langle\Omega|) \ge 0$, because $|\Omega\rangle\langle\Omega| \ge 0$. Conversely, if $J \ge 0$, the spectral decomposition of $J$ gives Kraus operators $K_k$ with $\Phi(X) = \sum_k K_k X K_k^\dagger$, as proved on the [Kraus operators](/kraus-operators/) page, and a map of that form is completely positive. For the trace, $\operatorname{Tr}_{out} J = \sum_{i,j} \operatorname{Tr}\Phi(|i\rangle\langle j|)\, |i\rangle\langle j|$, and this is $\sum_{i,j} \delta_{ij}|i\rangle\langle j| = I$ exactly when $\operatorname{Tr}\Phi(|i\rangle\langle j|) = \operatorname{Tr}|i\rangle\langle j|$ for all $i, j$, that is, when $\Phi$ preserves the trace. $\square$

A consequence: to test complete positivity it is enough to test $\Phi \otimes \mathrm{id}_m$ with $m = d_{in}$, on the one input $|\Omega\rangle\langle\Omega|$.

### Three equivalent forms

For a linear map $\Phi$, these are equivalent:

1. $\Phi$ is a channel.
2. **Kraus form.** $\Phi(\rho) = \sum_{k=1}^{r} K_k\rho K_k^\dagger$ with $\sum_k K_k^\dagger K_k = I$, and $r \le d_{in} d_{out}$ terms suffice.
3. **Stinespring form.** $\Phi(\rho) = \operatorname{Tr}_E(V\rho V^\dagger)$ for an isometry $V : \mathbb{C}^{d_{in}} \to \mathbb{C}^{d_{out}} \otimes \mathbb{C}^{r}$. When $d_{in} = d_{out}$, this is a unitary on the system and an environment that starts in $|0\rangle$, followed by the [partial trace](/partial-trace/) over the environment.

Choi's theorem gives 1 to 2, and the Kraus operators page proves 2 to 3 and back. So every channel is a unitary on a larger system, seen from a part of it.

### Properties

- **Convex and closed under composition.** Mixtures $p\Phi + (1-p)\Psi$, compositions $\Psi \circ \Phi$ and tensor products $\Phi \otimes \Psi$ of channels are channels. The Kraus operators of $\Psi \circ \Phi$ are the products $B_l A_k$.
- **Distances shrink.** For every channel, the [trace distance](/trace-distance/) satisfies $D(\Phi(\rho), \Phi(\sigma)) \le D(\rho, \sigma)$, and the [fidelity](/fidelity/) satisfies $F(\Phi(\rho), \Phi(\sigma)) \ge F(\rho, \sigma)$. Processing cannot make two states easier to tell apart.
- **The dual map.** The adjoint $\Phi^\dagger(Y) = \sum_k K_k^\dagger Y K_k$ acts on observables (the Heisenberg picture): $\operatorname{Tr}(Y\Phi(\rho)) = \operatorname{Tr}(\Phi^\dagger(Y)\rho)$. Trace preservation of $\Phi$ is the same as $\Phi^\dagger(I) = I$.
- **Unital channels.** $\Phi$ is unital if $\Phi(I) = I$, that is, $\sum_k K_k K_k^\dagger = I$. Unitary, Pauli and depolarizing channels are unital; amplitude damping is not.
- **Continuous time.** A family $\Phi_t = e^{t\mathcal{L}}$ of channels with $\Phi_{s+t} = \Phi_s \circ \Phi_t$ has a generator $\mathcal{L}$ of the Lindblad form $\mathcal{L}(\rho) = -i[H, \rho] + \sum_k \bigl(L_k \rho L_k^\dagger - \frac12\{L_k^\dagger L_k, \rho\}\bigr)$ (Lindblad 1976). The [open quantum system simulation](/open-quantum-system-simulation/) problem asks to apply such a $\Phi_t$.

### Distance between channels

The distance between two channels is measured by the **diamond norm** of their difference,

$$\|\Phi - \Psi\|_\diamond = \max_{\rho} \bigl\| \bigl((\Phi - \Psi) \otimes \mathrm{id}_{d_{in}}\bigr)(\rho) \bigr\|_1,$$

with the maximum over density matrices $\rho$ on $\mathbb{C}^{d_{in}} \otimes \mathbb{C}^{d_{in}}$. A reference system is needed: without it, the maximum can be smaller, and it then misses what an experiment that uses entanglement can detect. Half the diamond norm is the largest advantage in telling the two channels apart from one use, just as half the [trace norm](/matrix-norms/) is for states. Kitaev introduced this norm in 1997, and it is the error measure for noisy gates in fault tolerance.

## Examples and non-examples

**Channels.**

- **Unitary channel.** $\rho \mapsto U\rho U^\dagger$, with the single Kraus operator $U$.
- **Depolarizing channel.** $\rho \mapsto (1-p)\rho + p\,\operatorname{Tr}(\rho)\, I/d$. On a qubit it shrinks the Bloch ball by the factor $1-p$. With $p = 1/2$, $|0\rangle\langle0| \mapsto \operatorname{diag}(0.75, 0.25)$. The states $|0\rangle$ and $|1\rangle$, at trace distance 1, go to states at trace distance $1 - p$.
- **Measurement that forgets the result.** $\rho \mapsto \sum_m \langle m|\rho|m\rangle\, |m\rangle\langle m|$, with Kraus operators $|m\rangle\langle m|$. It keeps the diagonal and removes all coherences.
- **Classical channels.** A classical channel with transition probabilities $P(y \mid x)$ is the quantum channel with Kraus operators $\sqrt{P(y \mid x)}\,|y\rangle\langle x|$. On diagonal states it acts as the classical channel. The [binary symmetric channel](/binary-symmetric-channel/) comes from the quantum bit flip channel in this way, and quantum channels have capacities that extend the classical [channel capacity](/channel-capacity/).
- **Partial trace, adding a system, replacement.** $\rho \mapsto \operatorname{Tr}_B\rho$; $\rho \mapsto \rho \otimes \tau$ for a fixed state $\tau$; $\rho \mapsto \operatorname{Tr}(\rho)\,\tau$.

**Non-examples.**

- **The transpose.** $T(\rho) = \rho^{T}$ is positive and trace preserving, because $\rho^{T}$ has the same eigenvalues as $\rho$. But on the [Bell state](/bell-states/) $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt2$ it gives $(T \otimes \mathrm{id})(|\Phi^+\rangle\langle\Phi^+|) = \frac12 \sum_{i,j} |j\rangle\langle i| \otimes |i\rangle\langle j| = \frac12\,\mathrm{SWAP}$, which has the eigenvalue $-1/2$ on the antisymmetric vector $(|01\rangle - |10\rangle)/\sqrt2$. So $T$ is not completely positive and is not a channel. This test, applied to mixed states, is the partial transpose criterion for [entanglement](/entanglement/).
- **One measurement outcome.** $\rho \mapsto |0\rangle\langle0|\rho|0\rangle\langle0|$ is completely positive but loses trace. It is a quantum operation in the sense of Nielsen and Chuang, not a channel.
- **Nonlinear maps.** $\rho \mapsto \rho \otimes \rho$ and $\rho \mapsto \rho^2/\operatorname{Tr}\rho^2$ are not linear, so they are not channels. A channel that copied every state would contradict the [no-cloning theorem](/no-cloning-theorem/).

### Common errors

- **Positive is not enough.** A map that sends states to states can still fail on half of an entangled pair. Test $J(\Phi) \ge 0$, not only $\Phi(\rho) \ge 0$ for single states.
- **Trace preserving versus unital.** $\sum_k K_k^\dagger K_k = I$ and $\sum_k K_k K_k^\dagger = I$ are different conditions. Every channel satisfies the first; only unital channels satisfy the second.
- **Two meanings of "quantum operation".** In Nielsen and Chuang the term includes maps that lose trace. Check which class a source means.
- **Diamond norm versus operator norm.** The largest $\|(\Phi - \Psi)(\rho)\|_1$ over states of the system alone can be smaller than the diamond norm. Gate errors are usually stated in the diamond norm.

## Related definitions

- [Kraus operators](/kraus-operators/): the operator-sum form of a channel, its Stinespring isometry and its Choi matrix.
- [Density matrix](/density-matrix/): the states that channels act on.
- [Partial trace](/partial-trace/): the channel that discards a system, and the last step of every Stinespring form.
- [Trace distance](/trace-distance/) and [fidelity](/fidelity/): distances between states that channels do not increase.
- [Quantum error correction](/quantum-error-correction/): undoing a channel on the states of a code.
- [Unitary operator](/unitary-operator/): the channels that can be undone.

### History

Stinespring proved in 1955 that a completely positive map on a C*-algebra is an isometry followed by a restriction. Jamiołkowski (1972) and Choi (1975) related linear maps to matrices, and Choi proved that complete positivity is the positivity of $J(\Phi)$. Lindblad gave the generators of semigroups of channels in 1976. Kraus collected the operator-sum theory of quantum operations in his 1983 lecture notes, and Kitaev introduced the diamond norm in 1997.

## References
