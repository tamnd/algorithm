---
tag: 4E2Q6C
kind: algorithm
slug: superdense-coding
name: Superdense coding
aliases:
- dense coding
area: quantum/quantum-primitives
level: intro
summary: Alice sends two classical bits by sending one qubit, using a Bell pair shared in advance. She applies one of four Paulis; Bob reads the bits with a Bell measurement.
model: quantum-circuit-model
complexity:
  vars: {n: the number of bit pairs sent}
  time: {gates: Θ(n)}
  space: {bell_pairs: n, qubits_sent: n}
properties: {deterministic: true, exact: true, quantum: true}
history:
  year: 1992
  people: [Charles H. Bennett, Stephen J. Wiesner]
  note: Bennett and Wiesner gave the protocol in Physical Review Letters in 1992; Mattle, Weinfurter, Kwiat and Zeilinger showed a three-message version with photons in 1996.
prereqs: [bell-states, pauli-gates]
see_also: [quantum-teleportation, no-communication-theorem, entanglement, channel-capacity, cnot-gate, hadamard-gate]
sources:
  - paper: doi:10.1103/PhysRevLett.69.2881
    title: Charles H. Bennett and Stephen J. Wiesner, Communication via one- and two-particle operators on Einstein-Podolsky-Rosen states, Physical Review Letters 69, 1992, pages 2881 to 2884
    locator: the whole paper
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.3 (superdense coding) and Chapter 12 (the Holevo bound)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 1, Exercise 14 (superdense coding)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 6.3.1 (teleportation and dense coding)
  - paper: doi:10.1103/PhysRevLett.76.4656
    title: Klaus Mattle, Harald Weinfurter, Paul G. Kwiat and Anton Zeilinger, Dense coding in experimental quantum communication, Physical Review Letters 76, 1996, pages 4656 to 4659
    locator: the photon experiment with three distinguishable messages
  - paper: doi:10.1103/PhysRevA.59.3295
    title: N. Lütkenhaus, J. Calsamiglia and K.-A. Suominen, Bell measurements for teleportation, Physical Review A 59, 1999, pages 3295 to 3300
    locator: no linear-optics Bell measurement tells all four Bell states apart
  - paper: doi:10.1109/TIT.2002.802612
    title: Charles H. Bennett, Peter W. Shor, John A. Smolin and Ashish V. Thapliyal, Entanglement-assisted capacity of a quantum channel and the reverse Shannon theorem, IEEE Transactions on Information Theory 48, 2002, pages 2637 to 2655
    locator: the entanglement-assisted classical capacity
  - paper: doi:10.1103/PhysRevLett.92.097902
    title: Aram Harrow, Coherent communication of classical messages, Physical Review Letters 92, 2004, article 097902
    locator: coherent superdense coding and the cobit resource
---

Superdense coding sends two classical bits from Alice to Bob by sending a single qubit, with the help of one [Bell pair](/bell-states/) shared in advance. Alice applies one of the four [Pauli](/pauli-gates/) operators $I, X, Z, ZX$ to her half of the pair, which turns it into one of the four Bell states, and sends her half to Bob. Bob makes a Bell measurement on the two qubits and reads both bits with certainty. Without the shared pair one qubit carries at most one bit, and with it two bits is the most possible, so the protocol is optimal.

## In plain words

Alice and Bob made a pair of entangled qubits earlier and each kept one. Alice now wants to send Bob two bits, but she can send only one qubit. She chooses one of four simple operations, one for each two-bit message, applies it to her qubit and mails the qubit to Bob. Her operation changed the joint state of the pair into one of four states that are perfectly distinguishable, even though each qubit alone looks completely random. Bob now holds both qubits, does a fixed joint operation and measures, and gets the two bits. Without the earlier pair, one qubit can carry only one bit. Anyone who steals the mailed qubit alone learns nothing.

## The problem

Alice has a message $(x, y) \in \{0, 1\}^2$. Alice and Bob share the Bell state $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$, and Alice can send one qubit to Bob. The goal is that Bob outputs $(x, y)$ with certainty, for every message.

## The algorithm

Qubits are numbered as on the [quantum state](/quantum-state/) page, with kets written $|q_1 q_0\rangle$. Qubit $1$ is Alice's half and qubit $0$ is Bob's half.

```pseudo id=main
SUPERDENSE(x, y)                            ▷ two classical bits held by Alice
L1  qubits 1 and 0 start in |Φ+⟩ = (|00⟩ + |11⟩)/√2      ▷ shared in advance
L2  if y = 1 then apply X to qubit 1                    ▷ Alice
L3  if x = 1 then apply Z to qubit 1                    ▷ Alice
L4  send qubit 1 to Bob                                  ▷ one qubit of communication
L5  apply CNOT with control qubit 1 and target qubit 0  ▷ Bob
L6  apply H to qubit 1                                   ▷ Bob
L7  measure qubit 1 to get x' and qubit 0 to get y'     ▷ Bob
    return (x', y')                                      ▷ equals (x, y)
```

Lines L2 and L3 map $|\Phi^+\rangle$ to one of the four [Bell states](/bell-states/). Lines L5 and L6 are the Bell circuit run backwards, which maps the four Bell states to the four basis states, and line L7 reads the label.

## Example

The table follows each message through the protocol.

| $(x, y)$ | Alice applies | after L3 | after L5 | after L6 | Bob reads |
|---|---|---|---|---|---|
| $(0, 0)$ | $I$ | $\tfrac{1}{\sqrt{2}}(\lvert 00\rangle + \lvert 11\rangle)$ | $\lvert{+}\rangle\lvert 0\rangle$ | $\lvert 00\rangle$ | $(0, 0)$ |
| $(0, 1)$ | $X$ | $\tfrac{1}{\sqrt{2}}(\lvert 01\rangle + \lvert 10\rangle)$ | $\lvert{+}\rangle\lvert 1\rangle$ | $\lvert 01\rangle$ | $(0, 1)$ |
| $(1, 0)$ | $Z$ | $\tfrac{1}{\sqrt{2}}(\lvert 00\rangle - \lvert 11\rangle)$ | $\lvert{-}\rangle\lvert 0\rangle$ | $\lvert 10\rangle$ | $(1, 0)$ |
| $(1, 1)$ | $ZX$ | $\tfrac{1}{\sqrt{2}}(\lvert 01\rangle - \lvert 10\rangle)$ | $\lvert{-}\rangle\lvert 1\rangle$ | $\lvert 11\rangle$ | $(1, 1)$ |

Here $|{\pm}\rangle = (|0\rangle \pm |1\rangle)/\sqrt{2}$. The four states in the column "after L3" are $|\Phi^+\rangle, |\Psi^+\rangle, |\Phi^-\rangle, |\Psi^-\rangle$, and in each row qubit $1$ alone is in the state $I/2$.

## Correctness

The proof in `proofs/correctness.md` follows the four messages as in the table. Each message ends in the basis state $|x\,y\rangle$ after line L6, so line L7 reads it with probability $1$. The same proof shows that the reduced state of either qubit is $I/2$ for every message, so neither qubit alone carries information.

## Complexity

For one message of two bits, Alice applies at most two one-qubit gates and sends one qubit, and Bob applies one CNOT and one Hadamard and measures two qubits. One Bell pair is used up. For $n$ messages, run $n$ copies: $\Theta(n)$ gates, $n$ Bell pairs and $n$ qubits sent, in constant depth.

Two bits per qubit is the most possible. If Alice sends one qubit $Q$ and Bob holds a system $B$ that is entangled with Alice in any way, the [no-communication theorem](/no-communication-theorem/) keeps the state of $B$ the same for every message. The Holevo bound with subadditivity and the Araki-Lieb inequality then limits the information Bob can get from $QB$ to $2$ bits. Without entanglement, a uniform two-bit message is decoded with probability at most $\tfrac{1}{2}$, since one qubit carries at most one bit. Both bounds are proved in `proofs/correctness.md`.

## Properties

- **Deterministic and exact.** For every message, Bob's output is correct with probability $1$.
- **Secure against a lone eavesdropper.** The qubit sent in line L4 has the reduced state $I/2$ for every message, so a party who captures it learns nothing. A party who also holds Bob's half learns everything, so the security depends on the pair being shared safely.
- **The dual of teleportation.** Teleportation spends one Bell pair and two bits to send one qubit; superdense coding spends one Bell pair and one qubit to send two bits. Each protocol shows the other's resources are optimal ([quantum teleportation](/quantum-teleportation/)).
- **The pair can be sent early.** Bob's half can be delivered before the message exists, for example when the channel is cheap, and the message then needs only one qubit.

## Variants and improvements

- **Qudits.** With a maximally entangled pair of $d$-level systems, Alice applies one of the $d^2$ generalized Paulis $X^a Z^b$ and sends one $d$-level system, which carries $2\log_2 d$ bits.
- **Partial Bell measurements.** With linear optics and no extra resources, no measurement tells all four Bell states apart (Lütkenhaus, Calsamiglia and Suominen 1999). Mattle, Weinfurter, Kwiat and Zeilinger (1996) sent three messages, $\log_2 3 \approx 1.58$ bits per photon.
- **Noisy channels.** Over a noisy quantum channel with free shared entanglement, the best rate of classical bits is the entanglement-assisted capacity, given by the largest quantum mutual information of the channel (Bennett, Shor, Smolin and Thapliyal 2002). For the noiseless qubit channel this is $2$ bits, the superdense rate. See [channel capacity](/channel-capacity/).
- **Coherent dense coding.** If Alice's bits are held in qubits and Bob's final measurement is skipped, the protocol makes "coherent bits" that can be converted back into entanglement. Harrow (2004) used this to show that teleportation and superdense coding are inverse to each other as resource conversions.

## When to use it

Use superdense coding when quantum communication is costly at the time of the message but entanglement can be shared before, for example in a network that distributes Bell pairs in quiet periods. It also gives a simple way to show that entanglement raises the classical capacity of a quantum channel. Do not use it when a classical channel is available and cheap: it needs a Bell pair per two bits and a joint measurement of two qubits on Bob's side, which is the hard part in photon experiments.

## Pitfalls

- **The order of the decoder.** Bob must apply the CNOT before the Hadamard. The other order does not map the Bell basis to the computational basis, and the messages are mixed up.
- **Which bit goes with which Pauli.** Here $y$ controls $X$ and is read from qubit $0$, and $x$ controls $Z$ and is read from qubit $1$. A swap of the two qubits in the decoder swaps $x$ and $y$.
- **A different shared pair.** If the pair is $|\Psi^-\rangle$ or another Bell state, the four encodings still give the four Bell states, but in a different order. Bob must use the matching table.
- **Counting the entanglement as free.** Two bits per qubit sent is true only when the Bell pair is not counted. Delivering the pair takes one more qubit, so the total is two qubits for two bits, the same as sending them plainly. The gain is in when and how the qubits travel.

## Implementations

## History

Bennett and Wiesner published superdense coding in 1992, a year before teleportation. Mattle, Weinfurter, Kwiat and Zeilinger showed a version with photons in 1996 that sent one of three messages per photon, as linear optics can tell apart only three classes of Bell states. Bennett, Shor, Smolin and Thapliyal (2002) found the entanglement-assisted capacity of a general quantum channel, which contains the superdense rate as the noiseless case.

## References
