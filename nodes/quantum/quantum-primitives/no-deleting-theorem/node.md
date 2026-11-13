---
tag: 8V5BF1
kind: theorem
slug: no-deleting-theorem
name: No-deleting theorem
aliases:
- no-erasing theorem
area: quantum/quantum-primitives
level: core
summary: "Given two copies of an unknown qubit state, no unitary sets one copy to a fixed blank state while the ancilla state stays independent of it: the copy moves into the ancilla."
prereqs: [no-cloning-theorem]
see_also: [no-communication-theorem, quantum-channel, kraus-operators, unitary-operator, quantum-teleportation, entanglement]
sources:
  - paper: doi:10.1038/35004532
    title: Arun Kumar Pati and Samuel L. Braunstein, Impossibility of deleting an unknown quantum state, Nature 404, 2000, pages 164 to 165
    locator: the whole paper
  - paper: doi:10.1016/S0375-9601(03)01047-8
    title: Arun K. Pati and Samuel L. Braunstein, Quantum deleting and signalling, Physics Letters A 315, 2003, pages 208 to 212
    locator: the link between deleting and signalling
  - paper: doi:10.1147/rd.481.0079
    title: Richard Jozsa, Illustrating the concept of quantum information, IBM Journal of Research and Development 48, 2004, pages 79 to 85
    locator: the stronger forms of the no-cloning and no-deleting theorems
  - paper: doi:10.1038/299802a0
    title: W. K. Wootters and W. H. Zurek, A single quantum cannot be cloned, Nature 299, 1982, pages 802 to 803
    locator: the inner-product argument for cloning
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 1, Exercises 12 and 13 (no cloning, and no unitary deletion)
  - paper: doi:10.1147/rd.53.0183
    title: R. Landauer, Irreversibility and heat generation in the computing process, IBM Journal of Research and Development 5, 1961, pages 183 to 191
    locator: erasure moves information into the environment
---

The *no-deleting theorem* of Pati and Braunstein (2000) says that quantum information cannot be destroyed by a unitary process. If a device is given two copies $|\psi\rangle|\psi\rangle$ of an unknown qubit state and must turn the second copy into a fixed blank state $|\Sigma\rangle$, then the ancilla of the device must end up holding $|\psi\rangle$ itself: the copy is moved, not erased. So no device deletes the copy with an ancilla state that does not depend on $|\psi\rangle$. It is a counterpart of the [no-cloning theorem](/no-cloning-theorem/), and both follow from the fact that [unitary](/unitary-operator/) maps keep inner products.

## Statement

Let $\mathcal{H} = \mathbb{C}^2$, let $\mathcal{K}$ be the space of an ancilla with a fixed start state $|A\rangle$, and let $|\Sigma\rangle \in \mathcal{H}$ be a fixed unit vector, the blank state. A *deleter* is a unitary $U$ on $\mathcal{H} \otimes \mathcal{H} \otimes \mathcal{K}$ such that for every unit vector $|\psi\rangle \in \mathcal{H}$ there is a unit vector $|A_\psi\rangle \in \mathcal{K}$ with

$$U\big(|\psi\rangle|\psi\rangle|A\rangle\big) = |\psi\rangle|\Sigma\rangle|A_\psi\rangle.$$

**Theorem (Pati and Braunstein 2000).** For every deleter, $|A_0\rangle$ and $|A_1\rangle$ are orthonormal and

$$|A_\psi\rangle = \alpha\,|A_0\rangle + \beta\,|A_1\rangle \qquad \text{for } |\psi\rangle = \alpha|0\rangle + \beta|1\rangle.$$

So the map $|\psi\rangle \mapsto |A_\psi\rangle$ is a linear isometry: the ancilla holds a perfect copy of $|\psi\rangle$, written in the basis $|A_0\rangle, |A_1\rangle$.

**Corollary 1 (no deletion with a fixed ancilla).** Let $|\psi\rangle, |\phi\rangle$ be unit vectors with $0 < \lvert\langle\psi|\phi\rangle\rvert < 1$. No unitary $U$ satisfies $U(|\psi\rangle|\psi\rangle|A\rangle) = |\psi\rangle|\Sigma\rangle|A'\rangle$ and $U(|\phi\rangle|\phi\rangle|A\rangle) = |\phi\rangle|\Sigma\rangle|A''\rangle$ with $\lvert\langle A'|A''\rangle\rvert = 1$, that is, with the same final ancilla state up to a phase.

**Corollary 2 (channels).** Let $\Phi$ be a quantum channel on $\mathcal{H} \otimes \mathcal{H}$ with $\Phi(|\psi\psi\rangle\langle\psi\psi|) = |\psi\rangle\langle\psi| \otimes |\Sigma\rangle\langle\Sigma|$ and the same for $|\phi\rangle$, where $\langle\psi|\phi\rangle \ne 0$. Then in every Stinespring form $V$ of $\Phi$, with an environment $E$, the two final environment states satisfy $\lvert\langle E_\psi|E_\phi\rangle\rvert = \lvert\langle\psi|\phi\rangle\rvert$. The environment can tell the two states apart exactly as well as one input copy can.

What the theorem forbids is a reversible process that makes one of two copies blank and leaves no trace of the state anywhere else. It does not forbid resetting a qubit: the channel $\rho \mapsto \mathrm{Tr}_2(\rho) \otimes |\Sigma\rangle\langle\Sigma|$ is a valid [quantum channel](/quantum-channel/) that "deletes" the second copy, and Corollary 2 says that its environment receives the copy. It also does not forbid deleting copies of states from a known orthonormal basis.

## In plain words

Suppose a machine gets two copies of the same unknown qubit and must wipe one of them to a standard blank value. Any real process can be run backwards, so the information in the wiped copy cannot just vanish. The theorem shows that it must end up, complete, in the inner parts of the machine. A machine whose inner parts end the same way for every input cannot exist. Copying fails for the same reason: both would change how alike two inputs look, and physical processes keep that fixed.

## Proof

**The theorem.** Write $|\Phi\rangle = U\big(\tfrac{1}{\sqrt{2}}(|01\rangle + |10\rangle)|A\rangle\big)$. For $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$,

$$|\psi\rangle|\psi\rangle = \alpha^2 |00\rangle + \beta^2 |11\rangle + \sqrt{2}\,\alpha\beta \cdot \tfrac{1}{\sqrt{2}}(|01\rangle + |10\rangle).$$

Apply $U$, use linearity and the deleter equations for $|0\rangle$ and $|1\rangle$, and compare with the deleter equation for $|\psi\rangle$:

$$\alpha^2 |0\rangle|\Sigma\rangle|A_0\rangle + \beta^2 |1\rangle|\Sigma\rangle|A_1\rangle + \sqrt{2}\,\alpha\beta\,|\Phi\rangle = \alpha|0\rangle|\Sigma\rangle|A_\psi\rangle + \beta|1\rangle|\Sigma\rangle|A_\psi\rangle. \tag{1}$$

*Step 1: the form of $|\Phi\rangle$.* Take $\alpha = \beta = \tfrac{1}{\sqrt{2}}$ in (1). Then $|\Phi\rangle = |0\rangle|\Sigma\rangle|\Phi_0\rangle + |1\rangle|\Sigma\rangle|\Phi_1\rangle$ for two fixed vectors $|\Phi_0\rangle, |\Phi_1\rangle \in \mathcal{K}$, since every other term of (1) has this form.

*Step 2: the form of $|A_\psi\rangle$.* Put the form of Step 1 into (1) and compare the parts with $|0\rangle|\Sigma\rangle$ and with $|1\rangle|\Sigma\rangle$:

$$\alpha |A_\psi\rangle = \alpha^2 |A_0\rangle + \sqrt{2}\,\alpha\beta\,|\Phi_0\rangle, \qquad \beta |A_\psi\rangle = \beta^2 |A_1\rangle + \sqrt{2}\,\alpha\beta\,|\Phi_1\rangle.$$

For $\alpha\beta \neq 0$, divide by $\alpha$ and by $\beta$:

$$|A_\psi\rangle = \alpha|A_0\rangle + \sqrt{2}\,\beta\,|\Phi_0\rangle = \beta|A_1\rangle + \sqrt{2}\,\alpha\,|\Phi_1\rangle.$$

So $\alpha\,(|A_0\rangle - \sqrt{2}|\Phi_1\rangle) = \beta\,(|A_1\rangle - \sqrt{2}|\Phi_0\rangle)$ for all such $\alpha, \beta$. Take $(\alpha, \beta) = (\tfrac{1}{\sqrt{2}}, \tfrac{1}{\sqrt{2}})$ and $(\tfrac{1}{\sqrt{2}}, -\tfrac{1}{\sqrt{2}})$: the two equations give $|A_0\rangle = \sqrt{2}|\Phi_1\rangle$ and $|A_1\rangle = \sqrt{2}|\Phi_0\rangle$. Hence $|A_\psi\rangle = \alpha|A_0\rangle + \beta|A_1\rangle$ when $\alpha\beta \ne 0$, and trivially when $\alpha\beta = 0$, as then $|\psi\rangle$ is $|0\rangle$ or $|1\rangle$ up to a phase.

*Step 3: orthogonality.* $U$ keeps inner products. For two inputs $|\psi\rangle$ and $|\phi\rangle$, the inner product of $|\psi\psi\rangle|A\rangle$ and $|\phi\phi\rangle|A\rangle$ is $\langle\psi|\phi\rangle^2$, and the inner product of the outputs is $\langle\psi|\phi\rangle \langle\Sigma|\Sigma\rangle \langle A_\psi|A_\phi\rangle$. So

$$\langle\psi|\phi\rangle^2 = \langle\psi|\phi\rangle\,\langle A_\psi|A_\phi\rangle. \tag{2}$$

Take $|\psi\rangle = |0\rangle$ and $|\phi\rangle = |{+}\rangle$, with $\langle 0|{+}\rangle = \tfrac{1}{\sqrt{2}}$ and, by Step 2, $|A_+\rangle = (|A_0\rangle + |A_1\rangle)/\sqrt{2}$. Then (2) gives $\tfrac{1}{\sqrt{2}} = \langle A_0|A_+\rangle = \tfrac{1}{\sqrt{2}}(1 + \langle A_0|A_1\rangle)$, so $\langle A_0|A_1\rangle = 0$. The vectors $|A_0\rangle$ and $|A_1\rangle$ are unit vectors by definition, so they are orthonormal. $\square$

**Corollary 1.** By (2) with absolute values, $\lvert\langle\psi|\phi\rangle\rvert^2 = \lvert\langle\psi|\phi\rangle\rvert\,\lvert\langle A'|A''\rangle\rvert = \lvert\langle\psi|\phi\rangle\rvert$. So $s = \lvert\langle\psi|\phi\rangle\rvert$ satisfies $s^2 = s$, which means $s \in \{0, 1\}$, against the hypothesis. $\square$

**Corollary 2.** A Stinespring form of $\Phi$ is an isometry $V$ from $\mathcal{H} \otimes \mathcal{H}$ to $\mathcal{H} \otimes \mathcal{H} \otimes \mathcal{E}$ with $\Phi(\rho) = \mathrm{Tr}_{\mathcal{E}}(V \rho V^\dagger)$. The vector $V|\psi\psi\rangle$ is a pure state whose reduced state on $\mathcal{H} \otimes \mathcal{H}$ is the pure state $|\psi\Sigma\rangle\langle\psi\Sigma|$. A pure state of two parts with a pure reduced state is a product, so $V|\psi\psi\rangle = |\psi\rangle|\Sigma\rangle|E_\psi\rangle$ for a unit vector $|E_\psi\rangle$, and the same for $|\phi\rangle$. An isometry keeps inner products, so (2) holds with $|E_\psi\rangle$ in place of $|A_\psi\rangle$, and dividing by $\langle\psi|\phi\rangle \ne 0$ and taking absolute values gives $\lvert\langle E_\psi|E_\phi\rangle\rvert = \lvert\langle\psi|\phi\rangle\rvert$. $\square$

## Consequences

- **Information is conserved under unitary dynamics.** Together with the no-cloning theorem, the result says that a unitary process can neither make an extra copy of unknown quantum information nor remove one. A copy that seems to vanish has moved into the ancilla or the environment.
- **Erasure costs.** Resetting a qubit to $|0\rangle$ is possible, but by Corollary 2 the environment gets the state. This is the quantum side of Landauer's principle: erasure moves information into the surroundings and, in thermal settings, costs heat.
- **No deletion without signalling.** Pati and Braunstein (2003) showed that a perfect deleter applied to one half of an entangled pair would allow a signal faster than light, so the theorem is also forced by the [no-communication theorem](/no-communication-theorem/).
- **Teleportation leaves no copy.** In [quantum teleportation](/quantum-teleportation/), the input qubit ends in a basis state. This is not deletion in the sense of the theorem: the state reappears at Bob, and the record of the outcome is in the classical bits.

## Tightness

- **Orthogonal states can be deleted.** The theorem needs two non-orthogonal inputs. For $|0\rangle$ and $|1\rangle$, the CNOT with the first qubit as control maps $|00\rangle \mapsto |00\rangle$ and $|11\rangle \mapsto |10\rangle$, so it deletes the second copy to $|\Sigma\rangle = |0\rangle$ with no ancilla at all. On $|{+}{+}\rangle$ it fails: $|{+}\rangle$ is an eigenvector of $X$ with eigenvalue $1$, so $\mathrm{CNOT}\,|{+}{+}\rangle = |{+}{+}\rangle$.
- **The swap deleter exists.** The conclusion of the theorem is reached: take $\mathcal{K} = \mathbb{C}^2$, $|A\rangle = |\Sigma\rangle$ and $U$ the swap of the second qubit with the ancilla. Then $U(|\psi\rangle|\psi\rangle|\Sigma\rangle) = |\psi\rangle|\Sigma\rangle|\psi\rangle$, with $|A_\psi\rangle = |\psi\rangle$. By the theorem, on the inputs $|\psi\psi\rangle|A\rangle$ every deleter acts as this swap followed by the isometry $|0\rangle \mapsto |A_0\rangle$, $|1\rangle \mapsto |A_1\rangle$ on the ancilla.
- **Deleting one copy of one state is not the question.** De Wolf's exercise that no one-qubit unitary maps every $|\psi\rangle$ to $|0\rangle$ is a weaker fact: a unitary is injective, so it cannot map two different states to one. The no-deleting theorem is stronger because it gives the device a second copy and an ancilla, and still finds no deletion.
- **The proof uses only two states plus linearity.** Step 3 uses the pair $|0\rangle, |{+}\rangle$, and Corollary 1 needs only two non-orthogonal states with a fixed final ancilla. The full theorem, which identifies the ancilla state, uses linearity on the whole qubit.

## History

Wootters and Zurek (1982) and Dieks (1982) proved the no-cloning theorem. Pati and Braunstein (2000) asked the reverse question, whether one of two copies can be erased, and proved the theorem above in Nature. They linked it to no-signalling in 2003. Jozsa (2004) discussed stronger forms of both theorems, which say where the missing information must be.

## References
