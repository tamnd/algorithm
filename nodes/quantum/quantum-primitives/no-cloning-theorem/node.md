---
tag: 0245X0
kind: theorem
slug: no-cloning-theorem
name: No-cloning theorem
aliases:
- no-cloning
area: quantum/quantum-primitives
level: intro
summary: "No unitary, isometry or quantum channel maps |ψ> to |ψ>|ψ> for two different non-orthogonal states, so no device copies an unknown quantum state."
prereqs: [quantum-state, unitary-operator]
see_also: [no-deleting-theorem, no-communication-theorem, quantum-teleportation, state-discrimination-problem, quantum-channel, key-distribution-problem, quantum-error-correction]
sources:
  - paper: doi:10.1038/299802a0
    title: William K. Wootters and Wojciech H. Zurek, A single quantum cannot be cloned, Nature 299, 1982, pages 802 to 803
    locator: the whole paper
  - paper: doi:10.1016/0375-9601(82)90084-6
    title: D. Dieks, Communication by EPR devices, Physics Letters A 92(6), 1982, pages 271 to 272
    locator: the whole paper
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.5 (qubit copying circuit?), Box 12.1 (the no-cloning theorem) and Section 12.6.3 (quantum key distribution)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 1, Exercise 12 (no-cloning) and Section 18.2 (quantum key distribution)
  - paper: doi:10.1016/j.tcs.2014.05.025
    title: Charles H. Bennett and Gilles Brassard, Quantum cryptography, public key distribution and coin tossing, Theoretical Computer Science 560, 2014, pages 7 to 11 (reprint of the 1984 Bangalore paper)
    locator: the BB84 protocol
  - paper: doi:10.1103/PhysRevA.54.1844
    title: Vladimír Bužek and Mark Hillery, Quantum copying, beyond the no-cloning theorem, Physical Review A 54, 1996, pages 1844 to 1852
    locator: the universal cloning machine with fidelity 5/6
  - paper: doi:10.1103/PhysRevLett.79.2153
    title: N. Gisin and S. Massar, Optimal quantum cloning machines, Physical Review Letters 79, 1997, pages 2153 to 2156
    locator: optimality of the fidelity 5/6
  - paper: doi:10.1103/PhysRevLett.80.4999
    title: Lu-Ming Duan and Guang-Can Guo, Probabilistic cloning and identification of linearly independent quantum states, Physical Review Letters 80, 1998, pages 4999 to 5002
    locator: probabilistic exact cloning
  - paper: doi:10.1103/PhysRevLett.76.2818
    title: Howard Barnum, Carlton M. Caves, Christopher A. Fuchs, Richard Jozsa and Benjamin Schumacher, Noncommuting mixed states cannot be broadcast, Physical Review Letters 76, 1996, pages 2818 to 2821
    locator: the no-broadcasting theorem
  - paper: doi:10.1007/BF00729622
    title: Nick Herbert, FLASH, a superluminal communicator based upon a new kind of quantum measurement, Foundations of Physics 12, 1982, pages 1171 to 1179
    locator: the signalling proposal that the theorem refutes
  - paper: doi:10.1145/1008908.1008920
    title: Stephen Wiesner, Conjugate coding, ACM SIGACT News 15(1), 1983, pages 78 to 88
    locator: quantum money from conjugate bases
---

The *no-cloning theorem* says that no physical process takes an unknown quantum state $|\psi\rangle$ and a blank system and outputs two copies $|\psi\rangle|\psi\rangle$. More exactly, a [unitary](/unitary-operator/), an isometry or a [quantum channel](/quantum-channel/) can copy two states $|\psi\rangle$ and $|\phi\rangle$ only if they are orthogonal or equal up to a phase. So a copier works on a set of states only if the set is orthogonal, as for classical bits, and no copier works on all states of a qubit. Wootters and Zurek, and independently Dieks, proved it in 1982; it underlies the security of quantum key distribution and the reason why quantum error correction cannot simply keep backup copies.

## Statement

Let $\mathcal{H}$ be a Hilbert space with $\dim \mathcal{H} \ge 2$, and let $|\psi\rangle, |\phi\rangle \in \mathcal{H}$ be unit vectors with $s = \langle\psi|\phi\rangle$.

**Theorem (no-cloning, unitary form).** Let $\mathcal{E}$ be a further system (an ancilla, or the rest of the machine). Suppose a unitary $U$ on $\mathcal{H} \otimes \mathcal{H} \otimes \mathcal{E}$ and fixed unit vectors $|b\rangle \in \mathcal{H}$ (the blank) and $|e\rangle \in \mathcal{E}$ satisfy

$$U\,|v\rangle|b\rangle|e\rangle = |v\rangle|v\rangle|e_v\rangle \quad \text{for } v \in \{\psi, \phi\},$$

for some unit vectors $|e_\psi\rangle, |e_\phi\rangle \in \mathcal{E}$. Then $s = 0$ or $|s| = 1$.

**Theorem (no-cloning, channel form).** Suppose a quantum channel $\Phi$ (a completely positive, trace-preserving map) from $\mathcal{H}$ to $\mathcal{H} \otimes \mathcal{H}$ satisfies $\Phi(|v\rangle\langle v|) = |v\rangle\langle v| \otimes |v\rangle\langle v|$ for $v \in \{\psi, \phi\}$. Then $s = 0$ or $|s| = 1$.

**Corollary.** Let $S$ be a set of pure states. A unitary with an ancilla, or a channel, that clones every state in $S$ exists if and only if any two states of $S$ are orthogonal or equal up to a phase. In particular no such device clones all pure states of $\mathcal{H}$, or even the two states $|0\rangle$ and $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$.

**What the theorem forbids.** It forbids one fixed device that, for each input from a set with two distinct non-orthogonal states, outputs two exact copies with certainty. The machine must not depend on which state comes in: that is what "unknown" means. The theorem does not forbid:

- copying a *known* state, by preparing it again from its description;
- copying states from a known orthogonal set, such as the computational basis, which is how classical information is copied;
- *approximate* copies: the best universal one-to-two qubit cloner gives each copy the fidelity $5/6$ (Bužek and Hillery 1996; optimal by Gisin and Massar 1997);
- *probabilistic* exact copies of linearly independent states, which succeed with a probability below $1$ and say when they fail (Duan and Guo 1998);
- a linear map that is not an isometry and copies two linearly independent states. Such a map is not a physical evolution; the Tightness section gives one.

## In plain words

You can copy a page of text as often as you like, and you can copy a classical bit by reading it and writing it again. A quantum state cannot be copied in this way when you do not know what it is. Any machine that copies a set of states must keep the angles between them, because physical evolutions keep angles. Two copies of two states that overlap are closer to orthogonal than the two states themselves. So the angles can stay the same only if the states are already orthogonal, or are the same state. A machine can copy zero and one, but no machine can also copy the state that is halfway between them. This rule is why a spy cannot copy the qubits of a quantum key exchange and measure the copies later.

## Proof

**Unitary form.** A unitary keeps inner products. The inner product of the two inputs is

$$\big(\langle\psi|\langle b|\langle e|\big)\big(|\phi\rangle|b\rangle|e\rangle\big) = \langle\psi|\phi\rangle\,\langle b|b\rangle\,\langle e|e\rangle = s.$$

The inner product of the two outputs is $\langle\psi|\phi\rangle^2 \langle e_\psi|e_\phi\rangle = s^2 t$ with $t = \langle e_\psi|e_\phi\rangle$. So $s = s^2 t$. If $s \ne 0$, divide by $s$ to get $1 = s\,t$, so $1 = |s|\,|t|$. By the Cauchy-Schwarz inequality $|s| \le 1$ and $|t| \le 1$, so $|s| = |t| = 1$. Hence $s = 0$ or $|s| = 1$. The same computation works for an isometry $V$ in place of $U$, because an isometry also keeps inner products: $\langle Vx|Vy\rangle = \langle x|V^\dagger V|y\rangle = \langle x|y\rangle$.

**Channel form.** Write the channel with [Kraus operators](/kraus-operators/), $\Phi(\rho) = \sum_{k=1}^{m} K_k \rho K_k^\dagger$ with $\sum_k K_k^\dagger K_k = I$. Fix $v \in \{\psi, \phi\}$ and put $|w_v\rangle = |v\rangle|v\rangle$. Each term $K_k|v\rangle\langle v|K_k^\dagger$ is positive semidefinite, and the terms add up to the rank-one projector $|w_v\rangle\langle w_v|$. A positive semidefinite matrix $A$ with $A \preceq |w\rangle\langle w|$ has its range inside the span of $|w\rangle$, because $\langle u|A|u\rangle \le |\langle u|w\rangle|^2 = 0$ for every $u \perp w$. So $K_k|v\rangle = c_k(v)\,|w_v\rangle$ for numbers $c_k(v)$, and the trace gives $\sum_k |c_k(v)|^2 = 1$. Now

$$s = \langle\psi|\phi\rangle = \sum_k \langle\psi|K_k^\dagger K_k|\phi\rangle = \sum_k \overline{c_k(\psi)}\,c_k(\phi)\,\langle w_\psi|w_\phi\rangle = s^2\,t,$$

with $t = \sum_k \overline{c_k(\psi)}\,c_k(\phi)$. The vectors $(c_k(\psi))_k$ and $(c_k(\phi))_k$ are unit vectors of $\mathbb{C}^m$, so $|t| \le 1$ by Cauchy-Schwarz, and the end of the unitary proof applies.

**Corollary.** If two states of $S$ have $0 < |s| < 1$, the theorems say no device clones both. Conversely, let $S$ be orthogonal up to phases. Choose an orthonormal basis $\{|i\rangle\}$ of $\mathcal{H}$ that contains a representative of each state of $S$, and let $U$ be any unitary with $U|i\rangle|0\rangle = |i\rangle|i\rangle$; such a $U$ exists because the vectors $|i\rangle|0\rangle$ are orthonormal and so are the vectors $|i\rangle|i\rangle$. For a state $e^{i\gamma}|i\rangle$ of $S$, $U e^{i\gamma}|i\rangle|0\rangle = e^{i\gamma}|i\rangle|i\rangle$, which is the state $|i\rangle\langle i| \otimes |i\rangle\langle i|$ as a density matrix. For a qubit, $U$ is the [CNOT gate](/cnot-gate/). Finally, $|0\rangle$ and $|+\rangle$ have $s = 1/\sqrt{2}$, and $s^2 = \tfrac{1}{2} \ne s$. $\square$

## Consequences

**No signalling through entanglement.** Herbert (1982) proposed a faster-than-light signal: Alice measures her half of an entangled pair in one of two bases, and Bob makes many copies of his half to find out which basis she used. A cloner would make this work. The no-cloning theorem was found as the reason why the scheme fails, and it is consistent with the [no-communication theorem](/no-communication-theorem/).

**Security of quantum key distribution.** In BB84, Alice sends random bits, each in the basis $Z$ (states $|0\rangle, |1\rangle$) or $X$ (states $|+\rangle, |-\rangle$), and Bob measures each qubit in a random basis. They keep the rounds where the bases agree, the *sifted key*. An eavesdropper who could clone would keep copies and measure them after the bases are announced, and Bob would see no errors. Without a cloner, an intercept-resend attacker measures in a random basis and resends what she saw. When her basis is wrong, which happens with probability $\tfrac{1}{2}$, Bob's result in the sifted key is a fair coin, so the error rate on the sifted key is exactly $\tfrac{1}{2} \cdot \tfrac{1}{2} = \tfrac{1}{4}$. Alice and Bob estimate the error rate on a sample of the key, and stop if it is too high. The protocol then uses [privacy amplification](/leftover-hash-lemma/) to remove partial information, and the final key can encrypt a message with a [one-time pad](/one-time-pad/). This solves the [key distribution problem](/key-distribution-problem/) with security that does not rest on a hard computational problem, unlike [Diffie-Hellman](/diffie-hellman/), provided the classical channel is authenticated.

**Quantum money and unforgeable tokens.** Wiesner's conjugate coding (written around 1970, published 1983) uses the same states as BB84 to make bank notes that a forger cannot copy.

**Error correction without copies.** A classical repetition code stores three copies of a bit. A [quantum error-correcting code](/quantum-error-correction/) cannot copy the unknown state, so the [Shor code](/shor-code/) and its successors spread it into an entangled state of several qubits instead, and they measure only error syndromes.

**Learning a state from one copy is impossible.** If one copy of an unknown state could be turned into many, [quantum state tomography](/quantum-state-tomography/) could identify the state from one copy, and two non-orthogonal states could be told apart with certainty. Both are false ([state discrimination](/state-discrimination-problem/)). In the other direction, telling two states apart perfectly would let one prepare copies of them, so perfect discrimination of non-orthogonal states is also forbidden.

**Teleportation must destroy the original.** In [quantum teleportation](/quantum-teleportation/) the original qubit ends in a computational basis state after Alice's measurement; otherwise the protocol would be a cloner.

**Mixed states and broadcasting.** For mixed states the right question is *broadcasting*: a channel that maps $\rho$ to a state of two systems with both reduced states equal to $\rho$. Barnum, Caves, Fuchs, Jozsa and Schumacher (1996) proved that two states can be broadcast if and only if they commute.

## Tightness

**Orthogonal states can be copied.** The corollary is sharp: CNOT copies $|0\rangle$ and $|1\rangle$. On a superposition it makes an entangled state instead of two copies: $\mathrm{CNOT}\,|{+}\rangle|0\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$, whose overlap with $|{+}{+}\rangle$ is $\langle {+}{+}|\Phi^+\rangle = 1/\sqrt{2}$, so its fidelity with two copies is $\tfrac{1}{2}$.

**Linearity alone does not forbid copying two states.** A common short statement says that "no linear map clones two non-orthogonal states". That is false. If $|\psi\rangle$ and $|\phi\rangle$ are linearly independent, then the linear map $L = [\,|\psi\psi\rangle\ \ |\phi\phi\rangle\,]\,[\,|\psi\rangle\ \ |\phi\rangle\,]^{-1}$ from $\mathbb{C}^2$ to $\mathbb{C}^4$ copies both. For $|0\rangle$ and $|{+}\rangle$, the conditions $L|0\rangle = |00\rangle$ and $L|{+}\rangle = |{+}{+}\rangle$ force

$$L|0\rangle = (1, 0, 0, 0), \qquad L|1\rangle = \sqrt{2}\,L|{+}\rangle - L|0\rangle = \Big(\tfrac{\sqrt{2}}{2} - 1,\ \tfrac{\sqrt{2}}{2},\ \tfrac{\sqrt{2}}{2},\ \tfrac{\sqrt{2}}{2}\Big).$$

This $L$ is linear and copies both states exactly, but $\lVert L|1\rangle\rVert^2 = 3 - \sqrt{2} \ne 1$ and $\langle L0|L1\rangle = \tfrac{\sqrt{2}}{2} - 1 \ne 0$, so $L$ is not an isometry and no physical process acts as $L$. What the theorem needs is that the device keeps inner products, which unitaries and isometries do, or the Kraus structure of a trace-preserving channel. A multiple of $L$ can be one Kraus operator of a channel that succeeds only with some probability; this is the probabilistic cloning of Duan and Guo.

**Linearity does forbid copying three states.** No linear map at all copies $|0\rangle$, $|1\rangle$ and $|{+}\rangle$: the first two conditions fix $L|0\rangle = |00\rangle$ and $L|1\rangle = |11\rangle$, and then $L|{+}\rangle = (|00\rangle + |11\rangle)/\sqrt{2} \ne |{+}{+}\rangle$. In the same way no linear map copies every state of a qubit.

**Approximate and probabilistic cloning.** The fidelity $5/6$ of the Bužek-Hillery machine is the best possible for a universal one-to-two cloner, so the theorem cannot be strengthened to rule out good approximate copies, nor weakened to allow better ones. For two linearly independent states with equal priors, the best average success probability of exact probabilistic cloning is $1/(1 + |s|)$ (Duan and Guo 1998), which is $1$ only for $s = 0$.

### Implementation

The folder `impl/python` checks the theorem on small cases with exact arithmetic on numbers $a + b\sqrt{2}$. It checks that $s = \langle 0|{+}\rangle$ has $s^2 \ne s$; that the linear map $L$ above copies $|0\rangle$ and $|{+}\rangle$ exactly and is not an isometry, while the copier of $|0\rangle, |1\rangle$ is one; that no linear map copies $|0\rangle$, $|1\rangle$ and $|{+}\rangle$; and that CNOT copies basis states and gives fidelity $\tfrac{1}{2}$ on $|{+}\rangle$. For BB84 it computes the intercept-resend error rate on the sifted key exactly as $\tfrac{1}{4}$, and it samples $40\,000$ rounds with a fixed seed: the sampled rate is within $0.02$ of $\tfrac{1}{4}$, a band that by the [Hoeffding inequality](/hoeffding-inequality/) a correct simulation leaves with probability below $10^{-6}$. Without an eavesdropper the sampled sifted key has no errors.

## History

Herbert's FLASH proposal of 1982 led Wootters and Zurek (Nature, 1982) and Dieks (Physics Letters A, 1982) to the theorem, both with the linearity and inner-product argument above. Bennett and Brassard published BB84 in 1984, building on Wiesner's conjugate coding. Barnum and others extended the theorem to mixed states in 1996, and the same year Bužek and Hillery turned the question to the best approximate copy.

## References
