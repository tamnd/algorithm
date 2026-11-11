---
tag: H3BHXZ
kind: problem
slug: oblivious-transfer
name: Oblivious transfer
aliases:
- 1-out-of-2 oblivious transfer
area: cryptography/protocols
level: advanced
summary: A sender holds m0 and m1, a receiver holds a bit b. The receiver learns m_b and nothing about the other message, and the sender learns nothing about b.
history:
  year: 1981
  people: [Michael O. Rabin, Shimon Even, Oded Goldreich, Abraham Lempel]
  note: Rabin defined OT in a 1981 technical report. Even, Goldreich and Lempel defined 1-out-of-2 OT in 1985, and Kilian showed in 1988 that OT is complete for secure computation.
prereqs: [trapdoor-one-way-function, decisional-diffie-hellman, semi-honest-model]
see_also: [oblivious-transfer-extension, yao-garbled-circuits, gmw-protocol, secure-multiparty-computation, private-information-retrieval, private-set-intersection, rsa-problem, random-oracle-model]
sources:
  - paper: "Michael O. Rabin, How to exchange secrets with oblivious transfer, Technical Report TR-81, Aiken Computation Laboratory, Harvard University, 1981 (typeset copy in IACR ePrint 2005/187)"
    locator: the definition of OT (the message arrives with probability 1/2) and the protocol with quadratic residues modulo a product of two primes
  - paper: doi:10.1145/3812.3818
    title: "Shimon Even, Oded Goldreich and Abraham Lempel, A randomized protocol for signing contracts, Communications of the ACM 28(6), 1985, pages 637 to 647"
    locator: the definition of 1-out-of-2 OT and its construction from public-key encryption
  - paper: doi:10.1007/3-540-48184-2_30
    title: "Claude Crepeau, Equivalence between two flavours of oblivious transfers, CRYPTO 1987, LNCS 293, pages 350 to 354"
    locator: the reduction of 1-out-of-2 OT to Rabin OT
  - paper: doi:10.1145/62212.62215
    title: "Joe Kilian, Founding cryptography on oblivious transfer, STOC 1988, pages 20 to 31"
    locator: the main theorem (any two-party function can be computed securely from OT alone)
  - paper: doi:10.1007/978-3-319-22174-8_3
    title: "Tung Chou and Claudio Orlandi, The simplest protocol for oblivious transfer, LATINCRYPT 2015, LNCS 9230, pages 40 to 58"
    locator: the protocol (one group element each way) and its claimed UC proof in the random oracle model
  - url: "https://eprint.iacr.org/2017/370"
    title: "Ziya Alper Genc, Vincenzo Iovino and Alfredo Rial, The simplest protocol for oblivious transfer revisited, IACR ePrint 2017/370"
    locator: the flaw in the UC proof for a corrupted sender
  - url: "https://eprint.iacr.org/2017/1011"
    title: "Eduard Hauck and Julian Loss, Efficient and universally composable protocols for oblivious transfer from the CDH assumption, IACR ePrint 2017/1011"
    locator: the further flaws in the proof of the simplest OT, the patched proof, and the new protocol from CDH
  - paper: "Moni Naor and Benny Pinkas, Efficient oblivious transfer protocols, SODA 2001, pages 448 to 457"
    locator: the DDH based OT protocols and their batch versions
  - paper: doi:10.1007/978-3-540-85174-5_31
    title: "Chris Peikert, Vinod Vaikuntanathan and Brent Waters, A framework for efficient and composable oblivious transfer, CRYPTO 2008, LNCS 5157, pages 554 to 571"
    locator: the dual-mode framework and the UC secure OT from DDH, quadratic residuosity and LWE
  - paper: doi:10.1145/73007.73012
    title: "Russell Impagliazzo and Steven Rudich, Limits on the provable consequences of one-way permutations, STOC 1989, pages 44 to 61"
    locator: the black-box separation of key agreement from one-way permutations
  - paper: doi:10.1007/3-540-44750-4_8
    title: "Donald Beaver, Precomputing oblivious transfer, CRYPTO 1995, LNCS 963, pages 97 to 109"
    locator: random OT computed in advance and used later with one short message each way
---

Oblivious transfer (OT) is the two-party problem where a sender holds two messages $m_0, m_1$ and a receiver holds a choice bit $b$; at the end the receiver knows $m_b$ and nothing about $m_{1-b}$, and the sender knows nothing about $b$. It looks like a narrow task, but [Kilian (1988)](https://doi.org/10.1145/62212.62215) proved that OT is *complete*: with OT as the only tool, two parties can compute any function securely. Every general two-party protocol, [Yao's garbled circuits](/yao-garbled-circuits/) and the [GMW protocol](/gmw-protocol/) among them, spends most of its public-key work on OTs. This page states the problem, shows two protocols with a full worked run, and gives the map of variants and limits.

**Notation.** $S$ is the sender and $R$ the receiver. $m_0, m_1$ are the sender's messages, $b \in \{0, 1\}$ the receiver's choice bit, and $\ell$ the message length. $\lambda$ is the security parameter. $\mathbb{G} = \langle g \rangle$ is a cyclic group of prime order $q$. For RSA, $N$ is the modulus, $e$ the public exponent and $d$ the private exponent. $H$ is a hash function modeled as a [random oracle](/random-oracle-model/).

## In plain words

A shop has two sealed envelopes. A customer may open exactly one of them. The customer does not want the shop to know which one was opened, and the shop does not want the customer to see inside the other.

With a trusted clerk this is easy: the customer whispers the choice to the clerk, the clerk hands over that envelope and burns the other. Oblivious transfer gets the same result with no clerk. The two parties exchange a few messages that use public-key cryptography. At the end, the customer has the contents of one envelope and cannot read the other, and the shop cannot tell which envelope the customer took.

This small trick is enough to build every other private computation between two parties, which is why it sits at the base of the field.

## Definition

**The 1-out-of-2 OT functionality** $\mathcal{F}_{\mathrm{OT}}$. Input of $S$: $(m_0, m_1) \in (\{0,1\}^\ell)^2$. Input of $R$: $b \in \{0,1\}$. Output of $R$: $m_b$. Output of $S$: nothing.

**Security.** A protocol $\pi$ for OT is secure if it computes $\mathcal{F}_{\mathrm{OT}}$ in the sense of [secure computation](/secure-multiparty-computation/). In the [semi-honest model](/semi-honest-model/), this means two simulators exist:

- *Receiver privacy.* A simulator $\mathcal{S}_S$ that is given only $(m_0, m_1)$ outputs a view that is indistinguishable from the sender's real view, for both values of $b$. In particular the sender's view for $b = 0$ and for $b = 1$ must be indistinguishable.
- *Sender privacy.* A simulator $\mathcal{S}_R$ that is given only $(b, m_b)$ outputs a view that is indistinguishable from the receiver's real view. So the view is indistinguishable for any two pairs that agree in position $b$.

In the [malicious model](/malicious-adversary-model/) the simulator must also *extract*: from a cheating receiver it gets an effective choice bit $b$ to send to $\mathcal{F}_{\mathrm{OT}}$, and from a cheating sender it gets an effective pair $(m_0, m_1)$. In the [UC framework](/universal-composability/) it must do this without rewinding.

**Rabin OT.** The sender has one message $m$. With probability $1/2$ the receiver gets $m$, and otherwise it gets $\bot$. The sender does not learn which case happened. This is the first form, from [Rabin (1981)](https://eprint.iacr.org/2005/187).

## Variants

- **Bit OT and string OT.** $\ell = 1$ or $\ell = \lambda$ and more. String OT of any length follows from OT of $\lambda$-bit keys: the sender sends $m_i \oplus G(k_i)$ in the clear with a [pseudorandom generator](/pseudorandom-generator/) $G$.
- **1-out-of-$n$ OT**, written $\binom{n}{1}$-OT. The receiver picks one of $n$ messages. It reduces to $\lceil \log_2 n \rceil$ 1-out-of-2 OTs of keys plus $n$ encryptions sent in the clear. GMW uses $\binom{4}{1}$-OT for each AND gate.
- **$k$-out-of-$n$ OT.** The receiver picks a set of $k$ messages.
- **Random OT.** The functionality picks $m_0, m_1$ at random and gives them to $S$, and gives $(b, m_b)$ to $R$. [Beaver (1995)](https://doi.org/10.1007/3-540-44750-4_8) showed that random OTs computed in advance turn into OTs on real inputs with one short message each way, so all the expensive work moves offline.
- **Correlated OT.** The sender fixes $\Delta$ and the pairs satisfy $m_1 = m_0 \oplus \Delta$. It is what [OT extension](/oblivious-transfer-extension/) produces for free and what free-XOR garbling needs.
- **Symmetric PIR.** $\binom{n}{1}$-OT where the communication must be smaller than the database. It is [private information retrieval](/private-information-retrieval/) with sender privacy added.

## Examples

**EGL with RSA, worked.** Take the textbook toy key $N = 61 \cdot 53 = 3233$, $e = 17$, $d = 413$. The sender's messages are $m_0 = 1000$ and $m_1 = 2000$, and the receiver's choice is $b = 1$.

| Step | Who | Value |
|---|---|---|
| 1 | $S$ sends random $x_0, x_1$ | $x_0 = 123$, $x_1 = 2500$ |
| 2 | $R$ picks $k$, sends $v = x_b + k^e \bmod N$ | $k = 42$, $k^e = 2557$, $v = 1824$ |
| 3 | $S$ computes $k_0 = (v - x_0)^d$ | $1701^{413} = 2823$ |
| 3 | $S$ computes $k_1 = (v - x_1)^d$ | $2557^{413} = 42$ |
| 4 | $S$ sends $m_0 + k_0$ and $m_1 + k_1$ | $590$ and $2042$ |
| 5 | $R$ outputs $(m_1 + k_1) - k$ | $2042 - 42 = 2000$ |

The sender sees $v = 1824$. For $b = 0$ the same $v$ arises from $k' = (v - x_0)^d = 2823$, so $v$ is uniform for either choice and hides $b$ perfectly. The receiver knows $k_1 = k$ but would need to invert RSA on $v - x_0 = 1701$ to get $k_0$.

**Simplest OT, worked.** Take the subgroup of order $q = 509$ of $\mathbb{Z}_{1019}^*$ with $g = 4$, sender key $a = 10$ and receiver key $b' = 20$ (the receiver's exponent, not the choice bit).

| Step | Who | $c = 0$ | $c = 1$ |
|---|---|---|---|
| 1 | $S$ sends $A = g^a$ | $25$ | $25$ |
| 2 | $R$ sends $B = g^{b'}$ or $A g^{b'}$ | $625$ | $340$ |
| 3 | $S$: point for $k_0$ is $B^a$ | $929$ | $596$ |
| 3 | $S$: point for $k_1$ is $(B/A)^a$ | $718$ | $929$ |
| 4 | $R$: point for $k_c$ is $A^{b'}$ | $929$ | $929$ |

The receiver always gets the point $g^{ab'} = 929$, and it is the sender's point for exactly the chosen index. The keys are $k_i = H(A, B, \text{point}_i)$ and the sender sends $m_i \oplus k_i$. $B$ is a uniform group element in both columns, so the sender learns nothing about $c$. To get the other key, the receiver would need $g^{a(b' \pm a)}$, which needs $g^{a^2}$, as hard as the [CDH problem](/computational-diffie-hellman/).

**The code.** The page's Python file implements EGL with toy RSA and the simplest OT in two toy subgroups of $\mathbb{Z}_p^*$ for safe primes $p$, with SHA-256 from hashlib as $H$. Both are semi-honest only. There are no official test vectors for OT protocols. The tests check correctness for both choice bits, run a chi-square test that the receiver's message ($v$ or $B$) has the same distribution for $b = 0$ and $b = 1$, and run the malicious receiver attack on EGL described below. The code is for study only and is not constant time.

## Known algorithms

- **Rabin (1981).** The sender publishes $N = pq$; the receiver sends $x^2 \bmod N$ for a random $x$; the sender returns a random square root. With probability $1/2$ that root is not $\pm x$, and then the receiver can factor $N$ and read the message, which was encrypted under the factors. This gives Rabin OT from factoring.
- **Even, Goldreich and Lempel (1985).** 1-out-of-2 OT from any public-key encryption with the property that the receiver can make a public key without its secret key. The RSA form in the example is its usual textbook instance. It is secure for semi-honest parties if RSA is a [trapdoor permutation](/trapdoor-one-way-function/) with a [hard-core predicate](/hard-core-predicate/) for the message bits. It is not secure against a malicious receiver: if the receiver picks a value $c$ and sends $v = (x_0 - c^e x_1)/(1 - c^e) \bmod N$, then $v - x_0 = c^e (v - x_1)$, so $k_0 = c \cdot k_1$ and the two masked messages give $m_0 - c\, m_1$, a relation between both messages.
- **Naor and Pinkas (2001).** OT from DDH with a few exponentiations per transfer, and the batch version that most libraries used before 2015.
- **Peikert, Vaikuntanathan and Waters (2008).** The dual-mode framework, with UC secure OT from [DDH](/decisional-diffie-hellman/), quadratic residuosity or [LWE](/learning-with-errors/), in the common reference string model.
- **Chou and Orlandi (2015), the "simplest OT".** One group element from each side, as in the second example, with a UC proof in the random oracle model. It is fast and widely implemented, but the proof has been found faulty (see below).
- **OT extension.** [Beaver (1996) and IKNP (2003)](/oblivious-transfer-extension/) turn $\lambda$ base OTs into millions of OTs with only symmetric-key work. In practice, a few hundred public-key OTs and then extension is how OTs are made.

**What is known about the simplest OT.** Two later papers looked at the UC proof of Chou and Orlandi, and they found real gaps.

- [Genc, Iovino and Rial (2017)](https://eprint.iacr.org/2017/370) showed that the simulator for a *corrupted sender* cannot work as written. They proved that any correct simulator of that form would solve a decisional Diffie-Hellman type problem with overwhelming probability. So the protocol cannot be proven UC secure this way in a group where that problem is hard. It may still be secure in a gap Diffie-Hellman group, where the decisional problem is easy and CDH is hard.
- [Hauck and Loss (2017)](https://eprint.iacr.org/2017/1011) found two further flaws in the proof. They gave a fixed proof for static malicious corruptions under the gap Diffie-Hellman assumption, and showed that the proof still fails for adaptive corruptions. They also gave a new protocol that is UC secure under plain CDH in the random oracle model.

None of these findings is an attack that recovers a choice bit or a second message in a semi-honest run. They say that the strong UC claim does not hold as stated. The code on this page checks the group membership of $A$ and $B$, which every implementation must do, and does not claim more than semi-honest security.

## Bounds

- **No information-theoretic OT between two parties.** OT is a two-party function with no honest majority, so by the BGW optimality results (see [secure multiparty computation](/secure-multiparty-computation/)) it has no perfectly or statistically secure protocol over plain channels. OT needs a computational assumption, or a physical one such as a noisy channel.
- **OT needs public-key strength.** OT implies key agreement: run OT with random $m_0, m_1$ and random $b$, and $m_b$ is a key that an eavesdropper does not know. [Impagliazzo and Rudich (1989)](https://doi.org/10.1145/73007.73012) proved that key agreement cannot be built from one-way permutations in a black-box way, so neither can OT. Each fresh OT costs public-key operations, and this is why OT extension matters.
- **Cost of the protocols above.** EGL with RSA costs 2 private-key operations for the sender, 1 public-key operation for the receiver, and 4 elements of $\mathbb{Z}_N$ sent. The simplest OT costs 3 exponentiations for the sender, 2 for the receiver, 2 group elements and $2\ell$ bits sent.
- **Extension is the end of the cost story.** After $\lambda$ base OTs, each further OT costs $O(\lambda)$ bits and a few hash calls, see [OT extension](/oblivious-transfer-extension/).

## Reductions

- **Rabin OT and 1-out-of-2 OT are equivalent.** One direction is easy: from 1-out-of-2 OT, the sender offers $m$ in a random position and junk in the other, and later reveals which position held $m$. [Crepeau (1987)](https://doi.org/10.1007/3-540-48184-2_30) gave the other direction: 1-out-of-2 OT from many Rabin OTs, with an error that falls exponentially in their number.
- **OT is complete for secure computation.** [Kilian (1988)](https://doi.org/10.1145/62212.62215) proved that any two-party function, and with it any [secure multiparty computation](/secure-multiparty-computation/), can be computed from an ideal OT, also against malicious parties. In the semi-honest case the GMW construction makes this concrete: one $\binom{4}{1}$-OT per AND gate.
- **OT from secure computation.** OT is itself a two-party function, so any general 2PC protocol gives OT. With Kilian's result, general 2PC and OT are equivalent.

## Applications

The input wires of [Yao's garbled circuits](/yao-garbled-circuits/) (one OT per input bit of the evaluator); the AND gates of the [GMW protocol](/gmw-protocol/); OT-based [private set intersection](/private-set-intersection/); the generation of multiplication triples for MPC with a dishonest majority; and, in the paper of Even, Goldreich and Lempel, the exchange of signatures on a contract so that neither side can stop halfway with a large advantage.

## References
