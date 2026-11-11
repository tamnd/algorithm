---
tag: T1TB5Q
kind: definition
slug: sigma-protocol
name: Sigma protocol
aliases:
- three-move protocol
- Σ-protocol
area: cryptography/protocols
level: advanced
summary: A three-move public-coin protocol (commit, challenge, respond) for proving knowledge of a relation witness.
prereqs: [zero-knowledge-proof, proof-of-knowledge]
see_also: [schnorr-identification-protocol, fiat-shamir-heuristic, schnorr-signature, feige-fiat-shamir-identification, pedersen-commitment, decisional-diffie-hellman, ring-signature, shamir-secret-sharing]
sources:
  - paper: "Ronald Cramer, Modular design of secure yet practical cryptographic protocols, PhD thesis, CWI and University of Amsterdam, 1996"
    title: Ronald Cramer, Modular design of secure yet practical cryptographic protocols
    locator: the definition of Σ-protocols with special soundness and special honest-verifier zero knowledge, and their composition
  - url: https://www.cs.au.dk/~ivan/Sigma.pdf
    title: Ivan Damgård, On Σ-protocols, lecture notes, Aarhus University, 2010
    locator: the definition, the proof that special soundness gives knowledge error 2^-t, the OR construction, and zero knowledge by a committed challenge
  - paper: "Ronald Cramer, Ivan Damgård and Berry Schoenmakers, Proofs of partial knowledge and simplified design of witness hiding protocols, CRYPTO 1994, LNCS 839, 174-187"
    title: Ronald Cramer, Ivan Damgård and Berry Schoenmakers, Proofs of partial knowledge and simplified design of witness hiding protocols
    locator: proofs of knowledge of a witness for some of several statements, by splitting the challenge with a secret sharing scheme, and their witness indistinguishability
  - paper: "David Chaum and Torben Pryds Pedersen, Wallet databases with observers, CRYPTO 1992, LNCS 740, 89-105"
    title: David Chaum and Torben Pryds Pedersen, Wallet databases with observers
    locator: the protocol for equality of two discrete logarithms
  - paper: doi:10.1007/BF00196725
    title: Claus-Peter Schnorr, Efficient signature generation by smart cards, Journal of Cryptology 4(3), 1991, 161-174
    locator: the identification protocol for knowledge of a discrete logarithm, the basic example
  - book: isbn:9783642143021
    title: Carmit Hazay and Yehuda Lindell, Efficient Secure Two-Party Protocols, Techniques and Constructions, Springer, 2010
    locator: Chapter 6, Sigma Protocols and Efficient Zero-Knowledge (definitions, AND and OR, zero knowledge from Σ-protocols)
  - url: https://toc.cryptobook.us/
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: the chapter on identification and signatures from sigma protocols, and the chapter on proving properties in zero-knowledge
  - paper: "David Bernhard, Olivier Pereira and Bogdan Warinschi, How not to prove yourself, pitfalls of the Fiat-Shamir heuristic and applications to Helios, ASIACRYPT 2012, LNCS 7658, 626-643"
    title: David Bernhard, Olivier Pereira and Bogdan Warinschi, How not to prove yourself
    locator: the weak Fiat-Shamir transform, which does not hash the statement, and the attacks it allows
---

A sigma protocol is a three-move protocol between a prover and a verifier: the prover sends a first message $a$, the verifier answers with a random challenge $c$, and the prover sends a response $z$. Two properties make it useful. Two accepting answers to different challenges for the same $a$ give a witness (special soundness), so the protocol is a [proof of knowledge](/proof-of-knowledge/). For each challenge there is a simulator that makes accepting transcripts without the witness (special honest-verifier zero knowledge). The [Schnorr identification protocol](/schnorr-identification-protocol/) is the standard example. The name, from Cramer's 1996 thesis, comes from the zigzag shape of the three flows.

## Definition

**Notation.** $R$ is a binary relation that can be checked in polynomial time; $x$ is the statement and $w$ a witness, $(x, w) \in R$. $C$ is a finite challenge set, for example $\mathbb{Z}_q$ or $\{0, 1\}^t$. The verifier's decision is a fixed function $\varphi(x, a, c, z) \in \{0, 1\}$; $(a, c, z)$ is accepting if $\varphi = 1$.

**Sigma protocol.** A protocol $\Pi$ for $R$ is a sigma protocol with challenge set $C$ if it has this form:

1. $P(x, w)$ sends a first message $a$ (the commitment).
2. $V$ sends $c$, uniform in $C$ and independent of $a$ (a public coin).
3. $P$ sends $z$ (the response), and $V$ outputs $\varphi(x, a, c, z)$.

and it has the three properties:

- **Completeness.** If $(x, w) \in R$, the honest run is accepting.
- **Special soundness.** There is an efficient algorithm $E$ that, given $x$ and two accepting transcripts $(a, c, z)$, $(a, c', z')$ with $c \ne c'$, outputs $w$ with $(x, w) \in R$.
- **Special honest-verifier zero knowledge (SHVZK).** There is an efficient simulator $S$ that, given $x$ and any $c \in C$, outputs $(a, z)$ such that $(a, c, z)$ has the same distribution as a real transcript with challenge $c$, for each $(x, w) \in R$.

"Special" in the last property means the simulator gets the challenge as input. It is stronger than plain honest-verifier zero knowledge, and the OR construction needs this form.

### Basic facts

1. **Proof of knowledge.** A sigma protocol is a [proof of knowledge](/proof-of-knowledge/) with knowledge error $1/|C|$ (Damgård's notes).
2. **Honest-verifier zero knowledge only, for large $C$.** SHVZK gives a simulator for the honest verifier. For a polynomial size $C$ the rewinding simulator works against any verifier. For an exponential size $C$, no simulator for a malicious verifier is known in general. A standard fix is that the verifier first commits to $c$ with a trapdoor commitment.
3. **Witness indistinguishability.** Each sigma protocol is witness indistinguishable, and this property survives parallel composition (Cramer, Damgård and Schoenmakers 1994).
4. **Challenge length.** Parallel repetition keeps the three-move form: $k$ copies with a challenge in $C^k$ give a sigma protocol with challenge set $C^k$. The GI protocol with $|C| = 2$ becomes one with error $2^{-k}$.
5. **Non-interactive form.** With $c = H(x, a)$ for a hash function $H$, the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) gives a non-interactive proof in the random oracle model, and with the message in the hash, a signature such as the [Schnorr signature](/schnorr-signature/). The hash must include the statement $x$; the weak form without $x$ allows attacks (Bernhard, Pereira and Warinschi 2012).
6. **The extractor is an attack on reuse.** Special soundness means that a prover who answers two challenges with the same $a$ gives away $w$. A real prover who reuses its first-move randomness leaks its secret key.

## Examples and non-examples

**Generic interface.** In the Python file `sigma_protocol.py` each protocol has the five functions of the definition, with the random coins passed in so that the tests can enumerate them:

```pseudo id=main
SCHNORR-SIGMA over a group of prime order q with generator g;  statement y = g^x
L1  COMMIT(y, x):  k ← uniform in Z_q;  return a = g^k
L2  CHALLENGE:     c ← uniform in Z_q
L3  RESPOND:       return z = k + c·x mod q
L4  VERIFY:        accept iff g^z = a · y^c
L5  EXTRACT(a, c1, z1, c2, z2):  return x = (z1 - z2) · (c1 - c2)^(-1) mod q
L6  SIMULATE(y, c):  z ← uniform in Z_q
L7                   return (a, z) with a = g^z · y^(-c)
```

**Schnorr, knowledge of a discrete logarithm.** In the subgroup of order $q = 11$ of $\mathbb{Z}_{23}^*$ with $g = 4$, take $x = 7$, so $y = 4^7 \bmod 23 = 8$. With $k = 5$ the prover sends $a = 4^5 \bmod 23 = 12$.

| step | value |
| --- | --- |
| answer to $c = 2$ | $z = 5 + 2 \cdot 7 \bmod 11 = 8$; check $4^8 = 9 = 12 \cdot 8^2 \bmod 23$ |
| answer to $c = 9$ | $z' = 5 + 9 \cdot 7 \bmod 11 = 2$ |
| extraction | $(8 - 2) \cdot (2 - 9)^{-1} = 6 \cdot 3 = 18 \equiv 7 \pmod{11}$ |
| simulation for $c = 2$, $z = 4$ | $a = 4^4 \cdot 8^{-2} \bmod 23 = 4$ |

The simulator picks $z$ first and solves for $a$. For a fixed $c$, both $z$ in the real run ($z = k + cx$ with uniform $k$) and $z$ in the simulation are uniform, and $a$ is the unique value that makes the check hold. So the two distributions are equal.

**Chaum-Pedersen, equality of discrete logarithms.** The statement is $(u, v)$ with $u = g^x$ and $v = h^x$ for a second generator $h$. The prover sends $(g^k, h^k)$, gets $c$, answers $z = k + cx$; the verifier checks $g^z = a_1 u^c$ and $h^z = a_2 v^c$. This proves that $(g, h, u, v)$ is a Diffie-Hellman tuple, which is how a party proves correct ElGamal decryption or the output of some verifiable random functions. With $h = 9$, $x = 7$: $u = 8$, $v = 4$, and with $k = 5$ the first message is $(12, 8)$.

**AND.** For statements $x_1, x_2$, run both protocols with one shared challenge. Special soundness and SHVZK follow branch by branch.

**OR (Cramer, Damgård and Schoenmakers).** The prover knows a witness for $x_i$ only. It runs the simulator for the other branch with a challenge $c_{1-i}$ that it picks itself, and runs the real protocol on branch $i$. When the verifier sends $c$, the prover sets $c_i = c - c_{1-i} \bmod q$, answers branch $i$ honestly, and sends $(c_0, z_0, z_1)$. The verifier sets $c_1 = c - c_0$ and checks both transcripts. Two answers to $c \ne c'$ have $c_0 \ne c_0'$ or $c_1 \ne c_1'$, so special soundness of that branch gives a witness for one of the two statements. With $x_0 = 7$, $y_1 = 4^3 = 18$, prover coins $k = 5$, $c_1 = 6$, simulated $z_1 = 8$ and challenge $c = 2$, the prover sends $a = (12, 4)$ and then $(c_0, z_0, z_1) = (7, 10, 8)$. For $k$ out of $n$ statements, the challenges of the branches are shares of $c$ in [Shamir's secret sharing](/shamir-secret-sharing/).

**What the tests check.** There are no official test vectors for sigma protocols. In the group of order 11 the tests enumerate all prover coins and all simulator coins and check that the real and simulated transcripts are the same multiset, for each instance (Schnorr, Chaum-Pedersen, AND, OR with both branches, OR of Schnorr and Chaum-Pedersen) and several challenges. They also check:

- extraction from two transcripts in the group of order 1019, for every instance, and that the OR extractor returns the branch the prover really knows;
- witness indistinguishability of OR: the transcripts made with the witness for branch 0 and for branch 1 have the same distribution;
- soundness of Chaum-Pedersen: for a tuple with $\log_g u \ne \log_h v$, each first message has at most one challenge that can be answered.

The code is for study only, is not constant time and must not be used for real keys. Real systems use reviewed libraries such as libsodium or a FIPS 140 validated module for the group operations.

**Non-examples.**

- *The 3-coloring protocol.* It has three moves, but two accepted answers for different edges reveal only four vertex colors, not a coloring. It has no special soundness, so it is not a sigma protocol.
- *A private-coin challenge.* If the verifier's challenge depends on a secret of the verifier, the protocol is not public coin, and the Fiat-Shamir transform does not apply.
- *Answering before the challenge.* If the prover can choose $c$, the simulator becomes a cheating prover: pick $z$, set $a = g^z y^{-c}$. The verifier's fresh random challenge is what makes the protocol sound.

## Related definitions

- **[Proof of knowledge](/proof-of-knowledge/).** Special soundness implies it with knowledge error $1/|C|$.
- **[Zero-knowledge proof](/zero-knowledge-proof/).** SHVZK is the honest-verifier form of the simulator definition.
- **[Schnorr identification protocol](/schnorr-identification-protocol/) and [Feige-Fiat-Shamir identification](/feige-fiat-shamir-identification/).** Sigma protocols used for identification.
- **[Fiat-Shamir heuristic](/fiat-shamir-heuristic/).** Turns a sigma protocol into a non-interactive proof or a signature.
- **[Pedersen commitment](/pedersen-commitment/).** Has a sigma protocol for knowledge of an opening $(m, r)$, the two-base form of the Schnorr protocol above. Maurer's 2009 framework gives one protocol for every statement "I know a preimage of $y$ under a group homomorphism".
- **[Ring signature](/ring-signature/).** The Fiat-Shamir form of an OR proof over many public keys.

## References
