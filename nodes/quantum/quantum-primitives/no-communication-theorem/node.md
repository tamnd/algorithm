---
tag: AMHNNQ
kind: theorem
slug: no-communication-theorem
name: No-communication theorem
aliases:
- no-signalling theorem
area: quantum/quantum-primitives
level: core
summary: "A quantum channel or measurement on system B does not change the reduced state of A, so no local action on one half of a shared state sends a message to the other half."
prereqs: [entanglement, partial-trace, density-matrix, quantum-channel]
see_also: [no-cloning-theorem, bell-theorem, chsh-inequality, quantum-teleportation, superdense-coding, kraus-operators]
sources:
  - paper: doi:10.1007/BF02817189
    title: G. C. Ghirardi, A. Rimini and T. Weber, A general argument against superluminal transmission through the quantum mechanical measurement process, Lettere al Nuovo Cimento 27(10), 1980, pages 293 to 298
    locator: the whole paper
  - paper: doi:10.1007/BF02728628
    title: Phillippe H. Eberhard, Bell's theorem and the different concepts of locality, Il Nuovo Cimento B 46, 1978, pages 392 to 419
    locator: the argument that quantum correlations cannot carry a signal
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.4.3 (the reduced density operator, with the remark that teleportation does not send information faster than light) and Section 8.2 (quantum operations)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 6.3.2 (non-classical correlations)
  - paper: doi:10.1103/RevModPhys.76.93
    title: Asher Peres and Daniel R. Terno, Quantum information and relativity theory, Reviews of Modern Physics 76, 2004, pages 93 to 123
    locator: the discussion of no-signalling and relativity
  - paper: doi:10.1007/BF02058098
    title: Sandu Popescu and Daniel Rohrlich, Quantum nonlocality as an axiom, Foundations of Physics 24, 1994, pages 379 to 385
    locator: no-signalling correlations beyond the quantum ones
---

The *no-communication theorem* says that nothing one party does to their own part of a shared quantum state changes the reduced state of the other party's part. If Alice holds system $A$ and Bob holds system $B$ of a state $\rho_{AB}$, then any [quantum channel](/quantum-channel/) or measurement on $B$ leaves $\rho_A = \mathrm{Tr}_B\, \rho_{AB}$ the same, so no measurement by Alice can detect what Bob did. Shared [entanglement](/entanglement/) gives correlations that no classical model explains, but it cannot carry a message on its own; a message always needs a physical system that travels from Bob to Alice. The theorem is also called the *no-signalling theorem*.

## Statement

Let $\mathcal{H}_A$, $\mathcal{H}_B$ and $\mathcal{H}_{B'}$ be finite-dimensional Hilbert spaces and let $\rho$ be a [density matrix](/density-matrix/) on $\mathcal{H}_A \otimes \mathcal{H}_B$.

**Theorem (no-communication).** Let $\Phi$ be a quantum channel from $B$ to $B'$, with [Kraus operators](/kraus-operators/) $K_1, \dots, K_m : \mathcal{H}_B \to \mathcal{H}_{B'}$ and $\sum_k K_k^\dagger K_k = I_B$. Then

$$\mathrm{Tr}_{B'}\big[(\mathrm{id}_A \otimes \Phi)(\rho)\big] = \mathrm{Tr}_B\, \rho.$$

**Corollary 1 (no signal).** Suppose Bob picks one of several channels $\Phi_c$ on $B$, by a choice $c$ that Alice does not see, and Alice then measures $A$ with a POVM $\{M_a\}$ ([quantum measurement](/quantum-measurement/)). Then the probability of each outcome is

$$\Pr[a \mid c] = \mathrm{Tr}\big[(M_a \otimes I_{B'})\,(\mathrm{id}_A \otimes \Phi_c)(\rho)\big] = \mathrm{Tr}[M_a\, \rho_A],$$

which does not depend on $c$. So Alice's outcome is independent of Bob's choice, and the mutual information between them is $0$.

**Corollary 2 (measurements with outcomes).** Let Bob make a measurement with outcome $b$ and Kraus operators $K_b$, so that outcome $b$ has probability $p_b = \mathrm{Tr}[(I \otimes K_b)\rho(I \otimes K_b^\dagger)]$ and Alice's state given $b$ is $\rho_A^{(b)} = \mathrm{Tr}_B[(I \otimes K_b)\rho(I \otimes K_b^\dagger)] / p_b$. Then $\sum_b p_b\, \rho_A^{(b)} = \rho_A$.

**What the theorem forbids.** It forbids sending information from Bob to Alice by any local operation of Bob, unitary or not, with or without his own ancillas and measurements, when no system goes from Bob to Alice afterwards. Alice's statistics are not only close to the old ones: they are exactly the same. The theorem does not forbid:

- correlations between the two sides that no shared classical randomness gives, as in [Bell's theorem](/bell-theorem/);
- changes of Alice's *conditional* state given Bob's outcome $b$ (Corollary 2): the states $\rho_A^{(b)}$ can differ from $\rho_A$, but Alice cannot know $b$ without a message;
- communication once a message is sent: [teleportation](/quantum-teleportation/) sends two classical bits and [superdense coding](/superdense-coding/) sends one qubit;
- an interaction across the cut, such as a two-qubit gate between a qubit of $A$ and a qubit of $B$. Such a gate is not an operation on $B$ alone.

## In plain words

Alice and Bob share a pair of entangled qubits and go far apart. Bob wants to send Alice a yes or a no. He could measure his qubit in one way for yes and in another way for no. When Alice measures her qubit, she sees random results. The theorem says that her results have the same chances in both cases, so she learns nothing about Bob's choice. Bob's measurement does change the pair, but only in a way that shows up when Alice and Bob later compare their results, and to compare them one of them must send the other a message. That message travels no faster than light. So entanglement is a shared resource that makes some tasks easier, but it is not a phone line.

## Proof

**A lemma on partial traces.** For operators $X$ on $\mathcal{H}_A \otimes \mathcal{H}_B$ and $K, L : \mathcal{H}_B \to \mathcal{H}_{B'}$,

$$\mathrm{Tr}_{B'}\big[(I \otimes K)\, X\, (I \otimes L^\dagger)\big] = \mathrm{Tr}_B\big[X\, (I \otimes L^\dagger K)\big].$$

Both sides are linear in $X$, so it suffices to check it for $X = Y \otimes Z$ with $Y$ on $A$ and $Z$ on $B$, because such products span all operators on $\mathcal{H}_A \otimes \mathcal{H}_B$. The left side is $Y \cdot \mathrm{Tr}[K Z L^\dagger]$ and the right side is $Y \cdot \mathrm{Tr}[Z L^\dagger K]$ ([partial trace](/partial-trace/)). They are equal by the cyclic property of the trace, $\mathrm{Tr}[K (Z L^\dagger)] = \mathrm{Tr}[(Z L^\dagger) K]$.

**The theorem.** By the lemma with $K = L = K_k$, and then the completeness relation,

$$\mathrm{Tr}_{B'}\Big[\sum_k (I \otimes K_k)\, \rho\, (I \otimes K_k^\dagger)\Big] = \sum_k \mathrm{Tr}_B\big[\rho\, (I \otimes K_k^\dagger K_k)\big] = \mathrm{Tr}_B\Big[\rho\, \Big(I \otimes \sum_k K_k^\dagger K_k\Big)\Big] = \mathrm{Tr}_B\, \rho.$$

Every quantum channel has a Kraus form ([Kraus operators](/kraus-operators/)), so this covers every operation of Bob: a unitary on $B$ ($m = 1$, $K_1 = U$), the addition of an ancilla in a fixed state ($K_1 = I \otimes |0\rangle$), a measurement whose result is forgotten, or the discarding of part of $B$.

**Corollary 1.** For an operator $M$ on $A$, $\mathrm{Tr}[(M \otimes I)\,\sigma] = \mathrm{Tr}[M\, \mathrm{Tr}_{B'} \sigma]$ for every $\sigma$ on $A \otimes B'$; this is the defining property of the partial trace. With $\sigma = (\mathrm{id} \otimes \Phi_c)(\rho)$ and the theorem, $\Pr[a \mid c] = \mathrm{Tr}[M_a \rho_A]$. As this does not depend on $c$, the joint distribution of $(a, c)$ is a product for every distribution of $c$, and the mutual information is $0$.

**Corollary 2.** The map $\rho \mapsto \sum_b (I \otimes K_b)\rho(I \otimes K_b^\dagger)$ is a channel on $B$, since $\sum_b K_b^\dagger K_b = I$. By the theorem, $\sum_b p_b \rho_A^{(b)} = \sum_b \mathrm{Tr}_B[(I \otimes K_b)\rho(I \otimes K_b^\dagger)] = \rho_A$. $\square$

## Consequences

**Teleportation needs its classical bits.** In [quantum teleportation](/quantum-teleportation/), Alice's Bell measurement leaves Bob's qubit in one of four states, each with probability $\tfrac{1}{4}$. Before her two bits arrive, Bob's reduced state is the average of the four, which is $I/2$ for every input state, as the theorem requires. The unknown state reaches Bob only when the bits do, so teleportation is no faster than light.

**Bell correlations are no-signalling correlations.** In a [CHSH](/chsh-inequality/) test the distribution $p(a, b \mid x, y)$ of outcomes given settings has marginals $p(a \mid x, y) = p(a \mid x)$ that do not depend on the other party's setting $y$, and the same for $b$. Popescu and Rohrlich (1994) showed that no-signalling alone allows the CHSH value $4$, while quantum mechanics reaches only $2\sqrt{2}$ (Tsirelson's bound). So no-signalling is a property of quantum correlations, but it does not explain their exact limit.

**No cloning, or signalling would follow.** Herbert's 1982 proposal for a faster-than-light signal used a cloner on Bob's side. With the [no-cloning theorem](/no-cloning-theorem/), the two theorems are consistent: if Bob could make many copies of his half, he could tell the two ensembles of Alice apart, against the theorem.

**Entanglement does not raise the rate of a one-way bit channel.** By the theorem and the Holevo bound, Alice and Bob with any amount of shared entanglement still need $n$ classical bits sent to share $n$ bits of information. Superdense coding sends two bits in one *qubit*, not in one bit.

**Security without trust in the devices.** Device-independent protocols for key distribution and randomness assume only that the two devices cannot signal to each other. The theorem is what makes that assumption hold for quantum devices that are separated.

## Tightness

**An operation across the cut does change $\rho_A$.** Let $A$ be qubit $2$ and $B$ be qubits $1$ and $0$, and start in $|0\rangle_A|01\rangle_B$, so $\rho_A = |0\rangle\langle 0|$. A [CNOT](/cnot-gate/) with control qubit $0$ (in $B$) and target qubit $2$ (in $A$) gives $|1\rangle_A|01\rangle_B$, so now $\rho_A = |1\rangle\langle 1|$. The gate acts on both sides, so it is a physical interaction, not a local operation; the theorem needs the tensor product form $\mathrm{id}_A \otimes \Phi$.

**Trace preservation is needed.** Let Alice and Bob share $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$, so $\rho_A = I/2$. The map with the single Kraus operator $|0\rangle\langle 0|$ on Bob's side is completely positive but not trace preserving. After it and a renormalization, Alice's state is $|0\rangle\langle 0|$. This is the conditional state of Corollary 2 for the outcome $0$ of a measurement; it is not something Bob can force, because the outcome $1$ also occurs and Bob cannot stop it. A theory in which Bob could choose the outcome, or postselect without telling Alice, would allow signals.

**The conditional states do change.** For the same $|\Phi^+\rangle$, if Bob measures in the computational basis, Alice's conditional state is $|0\rangle\langle 0|$ or $|1\rangle\langle 1|$; if he measures in the basis $|\pm\rangle$, it is $|{+}\rangle\langle{+}|$ or $|{-}\rangle\langle{-}|$. Each pair averages to $I/2$. So the theorem is a statement about the averages, and the averages are all that Alice can see.

### Implementation

The folder `impl/python` checks the theorem on random pure states of three qubits, with $A$ as qubit $2$ and $B$ as qubits $1$ and $0$. For random two-qubit unitaries on $B$, random projective measurements on $B$ and amplitude damping on qubit $0$, the reduced state of $A$ stays the same to within $10^{-12}$. It also checks that the conditional states of a measurement differ from $\rho_A$ while their average does not, that the CNOT across the cut above changes $\rho_A$, and that in $20\,000$ sampled rounds on $|\Phi^+\rangle$ one party's frequency of the outcome $1$ is within $0.015$ of $\tfrac{1}{2}$ whether the other party measures in the $Z$ or the $X$ basis. By the [Hoeffding inequality](/hoeffding-inequality/), a correct simulation leaves that band with probability below $3 \cdot 10^{-4}$ for each basis.

## History

Eberhard (1978) argued that the correlations of quantum mechanics cannot be used for a signal, and Ghirardi, Rimini and Weber (1980) gave a general proof for measurements on one subsystem. Herbert's FLASH proposal of 1982 led to the [no-cloning theorem](/no-cloning-theorem/). In quantum information the statement is usually given in the form above, as a direct consequence of the partial trace and the Kraus form of channels.

## References
