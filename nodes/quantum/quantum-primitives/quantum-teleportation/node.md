---
tag: WR96G8
kind: algorithm
slug: quantum-teleportation
name: Quantum teleportation
aliases:
- teleportation protocol
area: quantum/quantum-primitives
level: intro
summary: "Alice sends an unknown qubit to Bob with one shared Bell pair and two classical bits: a Bell measurement on her side, then a Pauli correction on his."
model: quantum-circuit-model
complexity:
  vars: {n: the number of qubits sent}
  time: {gates: Θ(n), classical_bits: 2n}
  space: {bell_pairs: n, qubits: 3n}
properties: {deterministic: false, exact: true, quantum: true}
history:
  year: 1993
  people: [Charles H. Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres, William K. Wootters]
  note: Bennett, Brassard, Crépeau, Jozsa, Peres and Wootters gave the protocol in Physical Review Letters in 1993; the first photon experiments followed in 1997 and 1998.
prereqs: [bell-states, quantum-measurement]
see_also: [superdense-coding, no-cloning-theorem, no-communication-theorem, entanglement, pauli-gates, cnot-gate]
sources:
  - paper: doi:10.1103/PhysRevLett.70.1895
    title: Charles H. Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres and William K. Wootters, Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels, Physical Review Letters 70, 1993, pages 1895 to 1899
    locator: the whole paper
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.3.7 (Example, quantum teleportation) and Section 2.4.3 (quantum teleportation and the reduced density operator)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 1.5 (example, quantum teleportation)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 6.3.1 (teleportation and dense coding)
  - paper: doi:10.1038/37539
    title: Dik Bouwmeester, Jian-Wei Pan, Klaus Mattle, Manfred Eibl, Harald Weinfurter and Anton Zeilinger, Experimental quantum teleportation, Nature 390, 1997, pages 575 to 579
    locator: the first photon experiment
  - paper: doi:10.1103/PhysRevLett.71.4287
    title: M. Żukowski, A. Zeilinger, M. A. Horne and A. K. Ekert, Event-ready-detectors Bell experiment via entanglement swapping, Physical Review Letters 71, 1993, pages 4287 to 4290
    locator: entanglement swapping
  - paper: doi:10.1038/46503
    title: Daniel Gottesman and Isaac L. Chuang, Demonstrating the viability of universal quantum computation using teleportation and single-qubit operations, Nature 402, 1999, pages 390 to 393
    locator: gate teleportation
  - paper: doi:10.1103/PhysRevA.60.1888
    title: Michał Horodecki, Paweł Horodecki and Ryszard Horodecki, General teleportation channel, singlet fraction, and quasidistillation, Physical Review A 60, 1999, pages 1888 to 1898
    locator: the fidelity (2f + 1)/3 with a noisy pair
  - paper: doi:10.1103/PhysRevLett.81.5932
    title: H.-J. Briegel, W. Dür, J. I. Cirac and P. Zoller, Quantum repeaters, the role of imperfect local operations in quantum communication, Physical Review Letters 81, 1998, pages 5932 to 5935
    locator: repeaters built on entanglement swapping
  - paper: doi:10.1038/nature23675
    title: Ji-Gang Ren and others, Ground-to-satellite quantum teleportation, Nature 549, 2017, pages 70 to 73
    locator: teleportation over a ground-to-satellite link
---

Quantum teleportation moves an unknown qubit state from Alice to Bob without sending the qubit itself. Alice and Bob share one [Bell pair](/bell-states/) in advance; Alice makes a Bell measurement on the input qubit and her half of the pair, sends the two result bits to Bob, and Bob applies one of four [Pauli corrections](/pauli-gates/) to his half, which then holds the input state exactly. Each of the four outcomes has probability $\tfrac{1}{4}$ whatever the input, so the bits say nothing about the state, and Alice's original is destroyed, as the [no-cloning theorem](/no-cloning-theorem/) requires. It uses up one shared pair and two classical bits per qubit, and both amounts are necessary.

## In plain words

Alice has a qubit in a state she does not know, and she wants Bob to have it. She cannot measure it and send the result, because a measurement gives only one bit and destroys the rest of the state. Earlier, Alice and Bob made an entangled pair of qubits and each kept one. Now Alice does a joint operation on her unknown qubit and her half of the pair, and measures both. She gets two random bits and phones them to Bob. Bob's qubit is now one of four scrambled versions of the state, and the two bits tell him which one. He applies the matching fix, and his qubit is in the original state. Alice's qubit is left in a plain zero or one, so there is still only one copy. Nothing travels faster than the phone call.

## The problem

Alice holds a qubit in an unknown pure state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$, or more generally a qubit that is part of a larger entangled system. Alice and Bob share the Bell state $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$, and they can send classical bits from Alice to Bob, but no quantum system. The goal is that at the end a qubit of Bob is in the state $|\psi\rangle$, with all correlations of the input with other systems kept, for every input and with certainty.

## The algorithm

Qubits are numbered as on the [quantum state](/quantum-state/) page, with kets written $|q_2 q_1 q_0\rangle$. Qubit $2$ is the input, qubit $1$ is Alice's half of the pair and qubit $0$ is Bob's half.

```pseudo id=main
TELEPORT(qubit 2 in |ψ⟩)                 ▷ Alice holds qubits 2 and 1, Bob holds qubit 0
L1  qubits 1 and 0 start in |Φ+⟩ = (|00⟩ + |11⟩)/√2      ▷ shared in advance
L2  apply CNOT with control qubit 2 and target qubit 1    ▷ Alice
L3  apply H to qubit 2                                     ▷ Alice
L4  measure qubit 2 to get m_z and qubit 1 to get m_x     ▷ Alice
L5  send the bits m_z and m_x to Bob                       ▷ classical channel
L6  if m_x = 1 then apply X to qubit 0                     ▷ Bob
L7  if m_z = 1 then apply Z to qubit 0                     ▷ Bob
    return qubit 0                                         ▷ now in |ψ⟩
```

Lines L2 to L4 are a Bell measurement of qubits $2$ and $1$: the CNOT and the Hadamard are the reverse of the Bell circuit of the [Bell states](/bell-states/) page, so the outcome $(m_z, m_x)$ is the label of the Bell state found. After line L4, Bob's qubit is in $X^{m_x} Z^{m_z}|\psi\rangle$, and lines L6 and L7 undo the two Paulis.

## Example

Take $|\psi\rangle = 0.6\,|0\rangle + 0.8\,|1\rangle$. After line L3 the state is

$$\tfrac{1}{2}\Big(|00\rangle(0.6|0\rangle + 0.8|1\rangle) + |01\rangle(0.8|0\rangle + 0.6|1\rangle) + |10\rangle(0.6|0\rangle - 0.8|1\rangle) + |11\rangle(-0.8|0\rangle + 0.6|1\rangle)\Big).$$

| $(m_z, m_x)$ | probability | Bob's qubit after L4 | after L6 | after L7 |
|---|---|---|---|---|
| $(0, 0)$ | $\tfrac{1}{4}$ | $(0.6, 0.8)$ | $(0.6, 0.8)$ | $(0.6, 0.8)$ |
| $(0, 1)$ | $\tfrac{1}{4}$ | $(0.8, 0.6)$ | $(0.6, 0.8)$ | $(0.6, 0.8)$ |
| $(1, 0)$ | $\tfrac{1}{4}$ | $(0.6, -0.8)$ | $(0.6, -0.8)$ | $(0.6, 0.8)$ |
| $(1, 1)$ | $\tfrac{1}{4}$ | $(-0.8, 0.6)$ | $(0.6, -0.8)$ | $(0.6, 0.8)$ |

The pairs are the amplitudes of $|0\rangle$ and $|1\rangle$. All four rows end in $(0.6, 0.8)$, and the probabilities do not depend on $0.6$ and $0.8$. If Bob skips the correction, his qubit has the fidelity $1, 0.9216, 0.0784, 0$ with $|\psi\rangle$ in the four rows, which averages to $\tfrac{1}{2}$.

## Correctness

The proof in `proofs/correctness.md` expands the state after line L3 as $\tfrac{1}{2}\sum_{m_z, m_x} |m_z m_x\rangle \otimes X^{m_x} Z^{m_z}|\psi\rangle$, as in the example. The Born rule then gives each outcome the probability $\tfrac{1}{4}$ and leaves Bob with $X^{m_x} Z^{m_z}|\psi\rangle$, and $Z^{m_z}X^{m_x} X^{m_x}Z^{m_z} = I$ because $X^2 = Z^2 = I$. The same proof works when qubit $2$ is entangled with a reference system, because Bob's correction in each branch is the same operator for every component of the input. Before the bits arrive, Bob's qubit is the average of the four branches, which is $I/2$ for every input, so Bob learns nothing until line L5.

## Complexity

For one qubit, Alice applies one CNOT and one Hadamard and measures two qubits, Bob applies at most two one-qubit gates, and the protocol uses up one Bell pair and sends two classical bits. For $n$ qubits, run $n$ copies in parallel: $\Theta(n)$ gates, $n$ Bell pairs and $2n$ classical bits, in constant depth.

Both resources are optimal.

- **Two bits are needed.** Suppose a protocol sent one qubit with one Bell pair and fewer than two classical bits on average. Combine it with [superdense coding](/superdense-coding/): Alice encodes two classical bits into her half of a second Bell pair and teleports that qubit. Bob would then receive two bits of information from fewer than two bits of classical communication and shared entanglement, which the [no-communication theorem](/no-communication-theorem/) with the Holevo bound rules out.
- **One Bell pair is needed.** Teleport one half of a Bell pair held by Alice. Afterwards Alice and Bob share a Bell pair, so the protocol created one unit of entanglement by local operations and classical communication from what it used up. Those operations cannot increase entanglement ([entanglement](/entanglement/)), so it used at least one pair.

## Properties

- **Exact.** For every input and every outcome, Bob's qubit ends in exactly $|\psi\rangle$. The outcomes are random, but the result is not, so the protocol never fails and never needs a repeat.
- **Input-independent outcomes.** Each outcome has probability $\tfrac{1}{4}$ for every $|\psi\rangle$, so the classical bits are uniformly random and carry no information about the state. An eavesdropper on the classical channel learns nothing.
- **The original is destroyed.** After line L4, qubits $2$ and $1$ are in the basis state $|m_z m_x\rangle$. At no time do two copies of $|\psi\rangle$ exist.
- **No faster than light.** Before line L5 Bob's reduced state is $I/2$.
- **Linear and transparent to entanglement.** Teleportation acts as the identity channel from qubit $2$ to qubit $0$, so it keeps the entanglement of the input with any other system.

## Variants and improvements

- **Entanglement swapping.** Teleport one half of a Bell pair. The two qubits that never met end up in a Bell state (Żukowski, Zeilinger, Horne and Ekert 1993). Chains of swaps over short links are the basis of quantum repeaters (Briegel, Dür, Cirac and Zoller 1998).
- **Qudits.** For a $d$-level system, share $\sum_j |jj\rangle/\sqrt{d}$, measure in the basis of generalized Bell states, send $2\log_2 d$ bits and correct with one of the $d^2$ generalized Paulis $X^a Z^b$. The 1993 paper gives this form.
- **Gate teleportation.** To apply a gate $U$, teleport through the state $(I \otimes U)|\Phi^+\rangle$; the correction becomes $U P U^\dagger$ for a Pauli $P$. For $U$ in the [Clifford group](/clifford-group/) this is again a Pauli, and for a gate such as $T$ it is a Clifford gate. Gottesman and Chuang (1999) used this to make hard gates from prepared states, the idea behind magic state injection in fault-tolerant computing.
- **Deferred measurement.** Replace the measurement and the classical control by a CNOT from qubit $1$ to qubit $0$ and a controlled-$Z$ from qubit $2$ to qubit $0$. The circuit then has no measurement, which is useful in simulation, but it is no longer a protocol between distant parties.
- **Noisy pairs.** If the shared state has fully entangled fraction $f = \max \langle\Phi|\rho|\Phi\rangle$ over maximally entangled $|\Phi\rangle$, the best average fidelity of teleportation is $(2f + 1)/3$ (Horodecki, Horodecki and Horodecki 1999). It beats the value $2/3$ of the best measure-and-prepare scheme exactly when $f > \tfrac{1}{2}$.
- **Measurement-based computation.** A one-way quantum computer runs a circuit by a sequence of single-qubit measurements on an entangled cluster state, a form of repeated gate teleportation.

## When to use it

Use teleportation to move a qubit between two places that share entanglement but have no reliable quantum channel at the moment of transfer, for example two modules of a distributed quantum computer or two nodes of a quantum network. The pairs can be made, checked and purified in advance, and the transfer itself then needs only classical communication. Use it inside a fault-tolerant computer to apply gates by teleportation. Do not use it when a direct and good quantum channel is available, since it costs one Bell pair and two bits per qubit, and do not use it to copy a state: the input is consumed.

## Pitfalls

- **The correction order.** Bob holds $X^{m_x} Z^{m_z}|\psi\rangle$, so he must apply $X^{m_x}$ first and $Z^{m_z}$ second. The other order gives $-|\psi\rangle$ for the outcome $(1, 1)$, a global phase that is harmless even if the code also tracks a reference system, but a relative phase in a coherent version where the corrections are controlled gates whose control branches later interfere.
- **The qubit order.** Which measured bit controls $X$ and which controls $Z$ depends on the qubit roles. Here $m_x$ comes from Alice's half of the pair (qubit $1$) and $m_z$ from the input qubit (qubit $2$). A swap of the two bits gives a wrong state in half of the cases.
- **A different shared pair.** With $|\Psi^-\rangle$ or another Bell state as the resource, the four corrections are permuted. Bob's correction must match the shared pair.
- **Missing classical bits.** If the bits are lost, Bob's qubit is $I/2$, with fidelity $\tfrac{1}{2}$ on average with the input. Teleportation is only as reliable as its classical channel.
- **Reading it as transport of matter.** Only the state moves. Bob needs a qubit of the right kind, and Alice's qubit stays where it was, in a basis state.

## Implementations

## History

Bennett, Brassard, Crépeau, Jozsa, Peres and Wootters (1993) found the protocol and its $d$-level form, and named it teleportation. Żukowski, Zeilinger, Horne and Ekert proposed entanglement swapping the same year. Bouwmeester and others (1997) teleported the polarization of a photon, and other groups teleported photon and light-mode states in 1998. Gottesman and Chuang (1999) turned it into a method for computing. In 2017 a Chinese team teleported photon states from the ground to the Micius satellite, more than 1000 km away.

## References
