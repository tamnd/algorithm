---
tag: PWQQZB
kind: technique
slug: fiat-shamir-heuristic
name: Fiat-Shamir heuristic
aliases:
- Fiat-Shamir transform
- strong Fiat-Shamir
area: cryptography/signatures
level: advanced
summary: Replace the random challenge of a public-coin proof by a hash of the statement and the commitment. This gives signatures and non-interactive proofs, sound in the random oracle model.
prereqs: [sigma-protocol, random-oracle-model, zero-knowledge-proof]
see_also: [schnorr-signature, forking-lemma, schnorr-identification-protocol, feige-fiat-shamir-identification, fiat-shamir-with-aborts, ed25519, zk-snark, proof-of-knowledge]
sources:
  - paper: doi:10.1007/3-540-47721-7_12
    title: Amos Fiat and Adi Shamir, How to prove yourself, practical solutions to identification and signature problems, CRYPTO 1986, LNCS 263, Springer, 1987, pages 186 to 194
    locator: the identification scheme based on square roots modulo N, and the signature scheme that replaces the verifier's random bits by a hash of the message and the commitments
  - paper: doi:10.1007/s001450010003
    title: David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, pages 361 to 396
    locator: the forking lemma and the security of Fiat-Shamir type signatures in the random oracle model
  - paper: "Michel Abdalla, Jee Hea An, Mihir Bellare and Chanathip Namprempre, From identification to signatures via the Fiat-Shamir transform, minimizing assumptions for security and forward-security, EUROCRYPT 2002, LNCS 2332, Springer, 2002, pages 418 to 433"
    locator: the theorem that the transformed signature is secure in the random oracle model when the identification scheme is secure against impersonation under passive attack and its commitments have high min-entropy
  - paper: "Shafi Goldwasser and Yael Tauman Kalai, On the (in)security of the Fiat-Shamir paradigm, FOCS 2003, IEEE, pages 102 to 113"
    locator: the identification scheme whose Fiat-Shamir signature is insecure for every efficient hash function family
  - paper: "David Bernhard, Olivier Pereira and Bogdan Warinschi, How not to prove yourself, pitfalls of the Fiat-Shamir heuristic and applications to Helios, ASIACRYPT 2012, LNCS 7658, Springer, 2012, pages 626 to 643"
    locator: the weak and strong Fiat-Shamir transforms, the attack on the weak form, and the consequences for the Helios voting system
  - url: "https://blog.trailofbits.com/2022/04/13/part-1-coordinated-disclosure-of-vulnerabilities-affecting-girault-bulletproofs-and-plonk/"
    title: Jim Miller (Trail of Bits), Coordinated disclosure of vulnerabilities affecting Girault, Bulletproofs, and PlonK, April 13, 2022
    locator: the Frozen Heart class of bugs (forging of zero knowledge proofs) in implementations that leave public values out of the Fiat-Shamir hash
  - paper: "Marc Fischlin, Communication-efficient non-interactive proofs of knowledge with online extractors, CRYPTO 2005, LNCS 3621, Springer, 2005"
    locator: the transform with a straight-line (online) extractor in the random oracle model
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapters 19 and 20 (sigma protocols, the Fiat-Shamir transform and non-interactive proofs in the random oracle model)
---

The Fiat-Shamir heuristic turns a public-coin interactive proof into a non-interactive one: the prover computes the verifier's random challenge itself, as a hash of the statement and of its own first message. Applied to an identification protocol, with the message added to the hash, it gives a [signature scheme](/signature-scheme/), and the [Schnorr signature](/schnorr-signature/) and [Ed25519](/ed25519/) are made this way. It is sound in the [random oracle model](/random-oracle-model/), but not for every protocol with every concrete hash, and an implementation that leaves the statement out of the hash (the *weak* form) can accept proofs of false statements.

**Notation.** A [sigma protocol](/sigma-protocol/) for a relation $\mathcal{R}$ has a statement $X$, a witness $w$ with $(X, w) \in \mathcal{R}$, a commitment $a$, a challenge $c$ from a set $\mathcal{C}$ of size $h$, and a response $z$. $H$ is a hash function with output in $\mathcal{C}$, modelled as a random oracle. In the examples, $G$ is a group of prime order $q$ with generators $g$ and $h$. $q_h$ is the number of hash queries of an adversary.

## In plain words

In an interactive proof, a prover first commits to something, then the verifier asks a random question, and the prover answers. The prover cannot cheat because it does not know the question when it commits. This needs the verifier to be online and honest.

Fiat and Shamir replace the verifier by a hash function. The prover hashes the claim and its commitment, and uses the result as the question. Nobody can predict or steer a good hash, so the question is still fixed only after the commitment. Anyone can recompute the hash later, so the proof becomes a string that many people can check. Put a message into the hash too, and the proof becomes a signature on that message.

The hash must cover everything the verifier would have seen. If the claim is left out, a cheater can fix the commitment first and then pick a claim that fits.

## When it applies

- The interactive protocol is **public coin**: the verifier's messages are only random strings, with no secret state. A sigma protocol is the main case, and multi-round public-coin protocols (Bulletproofs, PlonK, STARKs) apply the transform once for each round.
- The protocol has **special soundness** or a similar extraction property: two accepting transcripts with the same commitment and different challenges reveal a witness. This is what the [forking lemma](/forking-lemma/) needs.
- The challenge space is **large**, of size $h \ge 2^{\lambda}$, or the protocol is repeated until it is. A protocol with one-bit challenges (such as the original [Feige-Fiat-Shamir](/feige-fiat-shamir-identification/) round) must be run in parallel $\lambda$ times before the hash is applied.
- The protocol is **honest-verifier zero knowledge**, if the result must be zero knowledge or a signature. The proof of security simulates answers by programming the random oracle.
- You accept a proof in the **random oracle model**, or a direct analysis of the concrete hash. Without that, there is no general guarantee (see the counterexamples below).

## The template

```pseudo id=main
PROVE(X, w, m)                       ▷ m is a message, or empty for a plain proof
L1  (a, st) ← COMMIT(X, w)           ▷ the first move of the sigma protocol
L2  c ← H(ctx ‖ X ‖ a ‖ m)           ▷ strong form: the statement X is hashed
L3  z ← RESPOND(X, w, st, c)
    return π = (a, z)

VERIFY(X, m, π = (a, z))
L4  c ← H(ctx ‖ X ‖ a ‖ m)
L5  return CHECK(X, a, c, z)         ▷ the verification of the sigma protocol
```

The holes are COMMIT, RESPOND and CHECK, which come from the sigma protocol, the hash $H$, and the context string $ctx$ that names the protocol and its public parameters (the group, the generators, the domain). For the Schnorr protocol, COMMIT draws $k$ and returns $a = g^k$, RESPOND returns $z = k + c w \bmod q$, and CHECK tests $g^z = a \cdot X^c$.

**Strong and weak.** Bernhard, Pereira and Warinschi name two forms. The **strong** form hashes the statement with the commitment, as in line L2. The **weak** form hashes only the commitment (and the message): $c = H(a \| m)$. The weak form is still a proof of knowledge when the statement is fixed before the proof, but it is not sound when the prover can choose the statement after the hash, which is the normal case when proofs are produced by the party that also makes the statement.

**Why it works in the random oracle model.** Model $H$ as a random function that the reduction controls. A cheating prover that outputs a valid proof must have asked $H$ at the point $(X, a, m)$ of that proof, or it guessed the answer with probability $1/h$. The reduction runs the prover again from that query with a new oracle answer. By the forking lemma, with probability about $\varepsilon^2/q_h$ it gets two accepting transcripts with the same $a$ and different $c$, and special soundness gives a witness. Zero knowledge, and the signing oracle for signatures, are simulated by the honest-verifier simulator: pick $c$ and $z$, compute $a$, and set $H(X, a, m) = c$. For signatures, Pointcheval and Stern (1996, 2000) proved this for Schnorr-type schemes, and Abdalla, An, Bellare and Namprempre (2002) showed that the transform turns any identification scheme that resists impersonation under passive attack, with commitments of high min-entropy, into a signature that is EUF-CMA in the random oracle model.

**Worked example.** In the group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$, take the witness $w = 77$, so $X = 4^{77} \bmod 2039 = 360$. With the nonce $k = 500$, the commitment is $a = 4^{500} \bmod 2039 = 277$. The strong challenge $c = H(g, X, a)$, with SHA-256 and a length prefix for each item, reduced mod 1019, is 779. The response is $z = 500 + 779 \cdot 77 \bmod 1019 = 362$. The proof $(277, 362)$ verifies for $X = 360$ and fails for $X = 4^{78}$, because the hash changes with the statement. This group is far too small to be secure.

**Cost.** The transform adds one hash per proof for the prover and for the verifier, on an input of the size of the statement and the commitment. It removes all interaction, so the proof is one message.

## Classic examples

- **[Feige-Fiat-Shamir](/feige-fiat-shamir-identification/) to signatures.** The original 1986 paper made the identification scheme based on square roots modulo $N$ into a signature by hashing the message with the commitments to choose the challenge bits.
- **[Schnorr signature](/schnorr-signature/).** The [Schnorr identification protocol](/schnorr-identification-protocol/) with $c = H(R \| m)$, or $H(R \| X \| m)$ in BIP 340, is the standard example of the technique.
- **[Ed25519](/ed25519/).** A Schnorr signature on an Edwards curve, with the challenge $H(R \| A \| M)$ and a deterministic nonce.
- **[Fiat-Shamir with aborts](/fiat-shamir-with-aborts/).** Lyubashevsky's lattice version restarts the protocol when the response would leak the secret. ML-DSA (FIPS 204) is built this way.
- **Non-interactive zero knowledge.** [zk-SNARKs](/zk-snark/) such as PlonK, [zk-STARKs](/zk-stark/) and Bulletproofs apply the transform to every round of a public-coin interactive proof, with a running transcript hash.
- **Multi-party signatures.** [MuSig](/musig/) and [FROST](/threshold-signature/) run a Schnorr signature among many signers, and the hash binds the aggregate key and nonce.

## Variations

- **Key prefixing.** For signatures, hash the public key: $c = H(R \| X \| m)$. Without it, a signature under $X$ moves to a related key $X g^{\delta}$ by the change $z \mapsto z + c\delta$, because $c$ does not depend on the key. The code of this page shows the move.
- **Multi-round transcripts.** For a protocol with many rounds, the challenge of round $i$ hashes the whole transcript up to round $i$. Libraries keep a running transcript object (for example Merlin, built on Strobe) so that no public value is forgotten.
- **Domain separation.** Different protocols that share a hash must use different context strings $ctx$, or a proof from one protocol may be valid in another. BIP 340 does this with tagged hashes.
- **Fischlin's transform.** Fischlin (CRYPTO 2005) gave a transform with a straight-line extractor, which needs no rewinding, at the cost of many hash calls by the prover. It is an alternative when the forking loss is too large or when rewinding is not allowed.

**Security beyond the random oracle.** Goldwasser and Kalai (FOCS 2003) built a three-move identification scheme that is secure, but whose Fiat-Shamir signature is insecure for every efficiently computable hash function family. Their scheme is contrived: it makes the protocol sensitive to the description of the hash. So the random oracle proof is a heuristic argument for a concrete hash, not a theorem about it. No such attack is known on the transforms of the standard schemes above.

## Pitfalls

- **The weak form.** Hashing only the commitment lets a prover pick the statement after the challenge. The attack of Bernhard, Pereira and Warinschi on a proof of equal discrete logarithms (Chaum-Pedersen), the proof used in Helios ballots, goes like this. The verifier checks $g^z = a_1 u^c$ and $h^z = a_2 v^c$ with $c = H(a_1 \| a_2)$. The cheater picks $a_1 = g^{\alpha}$, $a_2 = h^{\beta}$ with $\alpha \ne \beta$ and any $z$, computes $c$, and then sets $u = g^{(z - \alpha)/c}$ and $v = h^{(z - \beta)/c}$. Both equations hold, but $\log_g u \ne \log_h v$, so the statement is false. With $\alpha = 10$, $\beta = 20$, $z = 30$ in the toy group with $h = 9$, the hash gives $c = 1014$, and the forged statement is $u = 454$, $v = 1309$, with $\log_g u = 1015$ and $\log_h v = 1017$. The strong verifier, which hashes $u$ and $v$, rejects the same proof. Helios used the weak form in its ballot and decryption proofs, and the paper shows that this breaks the verifiability that the proofs were meant to give.
- **Frozen Heart.** In 2022 Trail of Bits reported the same mistake in several implementations of Girault's proof of knowledge, of Bulletproofs and of PlonK, where some public inputs or commitments were not in the transcript hash. The result was forged proofs for random statements.
- **Missing parameters.** The group, the generators and any setup values are part of the statement. A proof that does not hash them can be valid for another setup.
- **Small challenge space.** With $h$ challenges, a cheater succeeds with probability $1/h$ per try, and it can try offline as often as it wants. Use $h \ge 2^{\lambda}$, not the short challenges that are fine in an interactive protocol where each try costs a round with the verifier.
- **Reusing randomness.** Two proofs with the same commitment and different challenges reveal the witness, which is the [nonce reuse attack](/nonce-reuse-attack/) for signatures.
- **Reading the ROM proof as tight.** The forking reduction loses a factor of about $q_h$ in success probability (see the [forking lemma](/forking-lemma/) page). Parameters chosen from the bound alone are larger than the parameters used in practice.

## Exercises

1. Take the Schnorr proof in the weak form, $c = H(a)$. Show that a cheater can output a valid proof $(a, z)$ for a statement $X$ that it chooses after the hash. Explain why this is not a break of the proof of knowledge when the statement is $y = g^x$ in a group of prime order, but is a break for the Chaum-Pedersen proof above.
2. Show that the Fiat-Shamir signature of the Schnorr protocol with one-bit challenges is insecure, and compute the work of a forger.
3. Prove that if $(a, c, z)$ and $(a, c', z')$ are accepting Schnorr transcripts with $c \ne c'$, then $w = (z - z')/(c - c') \bmod q$ is the witness.

## References
