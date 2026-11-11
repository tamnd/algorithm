---
tag: 2JJVZ2
kind: definition
slug: proof-of-knowledge
name: Proof of knowledge
aliases:
- argument of knowledge
area: cryptography/protocols
level: advanced
summary: An interactive proof whose accepting provers must know a witness, shown by an extractor that computes the witness from any prover that succeeds often enough.
prereqs: [zero-knowledge-proof, discrete-logarithm-problem]
see_also: [sigma-protocol, schnorr-identification-protocol, feige-fiat-shamir-identification, fiat-shamir-heuristic, forking-lemma, zk-snark, interactive-proofs, graph-isomorphism-problem]
sources:
  - paper: "Mihir Bellare and Oded Goldreich, On defining proofs of knowledge, CRYPTO 1992, LNCS 740, 390-420"
    title: Mihir Bellare and Oded Goldreich, On defining proofs of knowledge
    locator: the definition with a knowledge error, the oracle extractor with expected time inversely proportional to the success probability minus the knowledge error, and the reduction of the error by sequential repetition
  - paper: doi:10.1007/BF02351717
    title: Uriel Feige, Amos Fiat and Adi Shamir, Zero-knowledge proofs of identity, Journal of Cryptology 1(2), 1988, 77-94
    locator: the first formal definition of a proof of knowledge, used for identification
  - paper: doi:10.1109/SFCS.1987.49
    title: Martin Tompa and Heather Woll, Random self-reducibility and zero knowledge interactive proofs of possession of information, FOCS 1987, 472-482
    locator: proofs of possession of information for random self-reducible problems such as the discrete logarithm
  - paper: doi:10.1137/0218012
    title: Shafi Goldwasser, Silvio Micali and Charles Rackoff, The knowledge complexity of interactive proof systems, SIAM Journal on Computing 18(1), 1989, 186-208
    locator: the informal notion of a prover that knows a witness
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 4.7, Proofs of Knowledge (definition, reducing the knowledge error, zero-knowledge proofs of knowledge for NP)
  - url: https://www.cs.au.dk/~ivan/Sigma.pdf
    title: Ivan Damgård, On Σ-protocols, lecture notes, Aarhus University, 2010
    locator: the theorem that a Σ-protocol with special soundness is a proof of knowledge with knowledge error 2^-t for t-bit challenges
  - book: isbn:9783642143021
    title: Carmit Hazay and Yehuda Lindell, Efficient Secure Two-Party Protocols, Techniques and Constructions, Springer, 2010
    locator: Chapter 6, Sigma Protocols and Efficient Zero-Knowledge (proofs of knowledge and the extractor for special soundness)
  - paper: "David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, 361-396"
    title: David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures
    locator: the forking lemma, the rewinding argument that extracts a witness from a prover in the random oracle model
---

A proof of knowledge is an interactive proof in which the verifier is convinced of more than the truth of a statement: it is convinced that the prover knows a witness for it. "Knows" is defined by an algorithm called an extractor. If a prover is accepted with high enough probability, the extractor, with black-box access to that prover and the power to rewind it, computes a witness. Feige, Fiat and Shamir gave the first formal definition in 1988, and Bellare and Goldreich gave the standard form, with a knowledge error, in 1992.

## Definition

**Notation.** $R$ is a relation that can be checked in polynomial time, with $x$ the statement and $w$ a witness. $V$ is the verifier. $P^*$ is any prover, viewed as a deterministic program once its random tape is fixed. $p(x)$ is the probability that $V$ accepts when it talks to $P^*$ on input $x$. $\kappa : \mathbb{N} \to [0, 1]$ is the knowledge error. An oracle machine $K^{P^*}$ can run $P^*$ on a chosen tape, send it chosen messages, and rewind it to an earlier state.

**Proof of knowledge (Bellare and Goldreich).** $(P, V)$ is a proof of knowledge for $R$ with knowledge error $\kappa$ if:

1. **Completeness.** If $(x, w) \in R$, then $V$ accepts the honest $P(w)$ with probability 1.
2. **Validity.** There is an oracle machine $K$, the knowledge extractor, and a polynomial $q$ such that for each prover $P^*$ and each $x$ with $p(x) > \kappa(|x|)$, $K^{P^*}(x)$ outputs a $w$ with $(x, w) \in R$ in expected time at most
$$\frac{q(|x|)}{p(x) - \kappa(|x|)}.$$

The extractor uses $P^*$ only as a black box. If validity holds only for efficient provers $P^*$, the protocol is an **argument of knowledge**.

**Why soundness is not enough.** Soundness only says that a false statement is rejected. For the statement "$y$ has a discrete logarithm base $g$" in a [cyclic group](/cyclic-group/) of prime order, every $y$ is a true statement, so a sound protocol can say nothing. What an identification scheme needs is that the prover knows $x = \log_g y$. That is what validity gives.

### Basic facts

1. **Special soundness gives knowledge error $1/|C|$.** If a three-move protocol $(a, c, z)$ with challenge set $C$ has special soundness (two accepting transcripts $(a, c, z)$ and $(a, c', z')$ with $c \ne c'$ give a witness), it is a proof of knowledge with knowledge error $1/|C|$. This is the main use of [sigma protocols](/sigma-protocol/).
2. **The error is tight for guessing.** A prover that guesses the challenge $c^*$ in advance can prepare an accepting transcript for $c^*$ only. It is accepted with probability exactly $1/|C|$, and the extractor cannot get two transcripts with the same first message.
3. **Repetition.** Sequential repetition $k$ times reduces the knowledge error from $\kappa$ to $\kappa^k$.
4. **Zero knowledge is separate.** A protocol can be a proof of knowledge without being zero knowledge (the prover sends $w$), and zero knowledge without being a proof of knowledge for a given relation.
5. **Extraction in the random oracle model.** For a non-interactive proof made by the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/), the extractor rewinds the prover to the point of the hash query and answers it differently. This is the [forking lemma](/forking-lemma/) of Pointcheval and Stern. It loses a factor in tightness that interactive extraction does not.
6. **Non-black-box extraction.** The knowledge soundness of pairing-based [zk-SNARKs](/zk-snark/) uses knowledge assumptions, in which the extractor reads the code of the prover, not just its answers.

## Examples and non-examples

**The extractor for Schnorr's protocol.** In the [Schnorr identification protocol](/schnorr-identification-protocol/) the prover knows $x$ with $y = g^x$. It sends $a = g^k$, gets a challenge $c \in C = \mathbb{Z}_q$, and answers $z = k + cx \bmod q$. The verifier checks $g^z = a y^c$. The extractor:

```pseudo id=main
EXTRACT(P*, y)
    repeat
L1      ρ ← a fresh random tape for P*
L2      c1 ← uniform in C;  run P*(ρ) on c1, get (a, z1)
L3      if the run is not accepted then continue
L4      for up to 2|C| tries
L5          c2 ← uniform in C \ {c1};  rewind P* to ρ, run it on c2, get z2
L6          if g^z2 = a · y^c2 then
L7              return x ← (z1 - z2) · (c1 - c2)^(-1) mod q
```

Line 5 is the rewind: the prover runs again on the same tape, so it sends the same $a$. Two accepting answers then give $g^{z_1 - z_2} = y^{c_1 - c_2}$, so $x = (z_1 - z_2)(c_1 - c_2)^{-1} \bmod q$.

A worked example in the subgroup of squares mod $p = 2039$, with $q = 1019$ and $g = 4$. The secret is $x = 777$, so $y = 4^{777} \bmod 2039 = 1590$. With nonce $k = 100$, $a = 4^{100} \bmod 2039 = 1153$.

| challenge | answer $z = k + cx \bmod q$ | check $g^z = a y^c$ |
| --- | --- | --- |
| $c_1 = 3$ | $z_1 = 393$ | $4^{393} = 713 = 1153 \cdot 1590^3 \bmod 2039$ |
| $c_2 = 10$ | $z_2 = 737$ | holds in the same way |

The extractor computes $z_1 - z_2 \equiv 675$ and $(c_1 - c_2)^{-1} = (-7)^{-1} \equiv 291 \pmod{1019}$, so $x = 675 \cdot 291 \bmod 1019 = 777$.

**Graph isomorphism.** In the [zero-knowledge](/zero-knowledge-proof/) graph isomorphism protocol, two answers for one $H$, $\tau_1$ with $\tau_1(G_1) = H$ and $\tau_0$ with $\tau_0(G_0) = H$, give the isomorphism $\tau_1^{-1} \circ \tau_0$ from $G_0$ to $G_1$. The protocol is a proof of knowledge of an isomorphism with knowledge error $1/2$.

**Code.** The Python file `proof_of_knowledge.py` models a prover as a deterministic function of (tape, challenge), as a program on a fixed random tape is, and runs the extractor against it in the toy group above. The tests check:

- A prover that knows $x$ but answers only 30 or 5 percent of the challenges still gives up $x$. The mean number of prover runs is near $2/p$ (between half and twice that value over 60 extractions for $p = 0.5$ and $p = 0.1$).
- With $|C| = 8$, a guessing prover has exactly one accepting challenge per tape and success exactly $1/8$. The extractor fails within its budget of 3000 runs.
- A prover that knows $x$ and answers 2 of the 8 challenges on each tape has success $1/4 > 1/8$, and the extractor finds $x$.

There are no official test vectors for proofs of knowledge. The code is for study only, is not constant time and must not be used for real keys. Real systems use reviewed libraries such as libsodium or a FIPS 140 validated module for the group operations.

**Non-examples.**

- *A one-element challenge set.* With $C = \{0\}$, the prover sends $a = g^z$ and answers $z$. Each prover is accepted and nothing can be extracted: the knowledge error is 1.
- *The guessing prover.* It succeeds with probability $1/|C|$ without $x$. This shows that no extractor can work at success probability $1/|C|$, so the knowledge error of Schnorr's protocol cannot be below $1/|C|$.
- *Checking group membership.* A protocol in which the verifier checks $y^q = 1$ is a sound proof that $y$ has a logarithm, but it proves no knowledge of the logarithm.

## Related definitions

- **[Zero-knowledge proof](/zero-knowledge-proof/).** Says what the verifier does not learn; a proof of knowledge says what the prover must know. Most useful protocols are zero-knowledge proofs of knowledge.
- **[Sigma protocol](/sigma-protocol/).** The three-move form whose special soundness gives the extractor above.
- **[Forking lemma](/forking-lemma/).** The rewinding argument for signatures made by the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/).
- **Knowledge soundness.** The name used for SNARKs, where the extractor may be non-black-box.
- **Witness hiding.** The view does not help the verifier compute a witness. It is weaker than zero knowledge and holds under parallel composition for some protocols.
- **[Interactive proofs](/interactive-proofs/).** The model with plain soundness.

## References
