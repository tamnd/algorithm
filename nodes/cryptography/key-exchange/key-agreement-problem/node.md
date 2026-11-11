---
tag: 670PGX
kind: problem
slug: key-agreement-problem
name: Key agreement problem
aliases:
- key exchange problem
area: cryptography/key-exchange
level: intro
summary: Two parties with no shared secret talk over a public channel and must end with the same secret key, where both contribute and neither can choose the key alone.
prereqs: [session-key]
see_also: [diffie-hellman, key-transport-problem, key-distribution-problem, authenticated-key-exchange, merkle-puzzles, man-in-the-middle-attack, ecdh, hybrid-key-exchange]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.2.1 (Definition 12.2 key establishment, Definition 12.3 key transport, Definition 12.4 key agreement) and Section 12.6.1 (Protocol 12.47, basic Diffie-Hellman)
  - paper: doi:10.6028/NIST.SP.800-56Ar3
    title: Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev and Richard Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018
    locator: Section 3.1 (definitions of key agreement and key establishment) and Section 6 (the key-agreement schemes)
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976
    locator: Section III (public key distribution systems)
  - paper: doi:10.1145/73007.73012
    title: Russell Impagliazzo and Steven Rudich, Limits on the provable consequences of one-way permutations, STOC 1989
    locator: the result that no black-box reduction builds key agreement from a random permutation (a random oracle)
  - paper: doi:10.1007/978-3-642-03356-8_22
    title: Boaz Barak and Mohammad Mahmoody-Ghidary, Merkle puzzles are optimal, an O(n^2)-query attack on any key exchange from a random oracle, CRYPTO 2009, LNCS 5677, pages 374 to 390
    locator: the main theorem, an attack with O(n^2) oracle queries on any protocol in which the parties make n queries
  - book: isbn:9783662581452
    title: Colin Boyd, Anish Mathuria and Douglas Stebila, Protocols for Authentication and Key Establishment, second edition, Springer, 2020
    locator: Chapter 1 (the classification of key establishment) and Chapter 5 (Key Agreement Protocols)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the chapter Key Management and the Public-Key Revolution, the section on key exchange and the Diffie-Hellman protocol (the experiment for a passive eavesdropper)
---

The key agreement problem asks two parties who share no secret to end with the same secret key after they exchange messages over a channel that an adversary can read. Both parties contribute to the key, and neither can fix its value alone; this separates it from [key transport](/key-transport-problem/), where one party picks the key and sends it. The first solutions were [Merkle's puzzles](/merkle-puzzles/) and [Diffie-Hellman key exchange](/diffie-hellman/) (1976). Against an adversary who can also change messages, a solution needs [authentication](/authenticated-key-exchange/), else a [man in the middle](/man-in-the-middle-attack/) breaks it.

**Notation.** $\lambda$ is the security parameter. $A$ and $B$ are the two parties, with independent random coins $r_A$ and $r_B$. $T$ is the transcript, the list of all messages. $k_A$ and $k_B$ are the keys that the parties output, strings of $n$ binary digits. $\mathcal{A}$ is an adversary, $\mathrm{Adv}$ its advantage, and $\varepsilon$ a small error probability. $G = \langle g \rangle$ is a cyclic group of prime order $q$.

## In plain words

Two people want to share a secret password, but every word they say can be heard by a spy. They have never met, so they have no secret yet. Can they still agree on a password that the spy does not know?

It seems impossible, but it is not. Each person keeps a private random number and sends a value computed from it. Each one then combines the other's value with its own private number. The two results are the same, but the spy, who sees only the sent values, cannot compute the result in a reasonable time.

Both people help to make the password, and neither can choose it alone. If the spy can also change the messages, the problem is harder: the two people must also check who they are talking to.

## Definition

A key agreement protocol is a pair of efficient probabilistic interactive algorithms $(A, B)$. On input $1^\lambda$, they exchange messages that form $T$, and each outputs a key: $k_A = k_A(r_A, T)$ and $k_B = k_B(r_B, T)$.

**Correctness.** $\Pr[k_A = k_B] \ge 1 - \varepsilon(\lambda)$, with $\varepsilon$ negligible (often $\varepsilon = 0$).

**Security against a passive adversary.** Run the protocol, let $k = k_A$, pick a uniform bit $b$, and give $\mathcal{A}$ the transcript $T$ and the string $k_b$, where $k_1 = k$ and $k_0$ is uniform in $\{0,1\}^n$. The protocol is secure if for every efficient $\mathcal{A}$

$$\mathrm{Adv}(\mathcal{A}) = \bigl|\Pr[\mathcal{A}(T, k_b) = b] - \tfrac{1}{2}\bigr|$$

is negligible in $\lambda$. This is the eavesdropping experiment of Katz and Lindell. The weaker goal, that $\mathcal{A}$ cannot compute $k$ from $T$, is not enough for use as a key, because part of $k$ may still leak.

**Contributory.** HAC (Definition 12.4) and NIST SP 800-56A Rev. 3 (Section 3.1) define key agreement as key establishment in which the key is a function of information contributed by both parties, so that (ideally) neither party can predetermine it. In key transport (HAC, Definition 12.3) one party creates the key and sends it to the other.

**Security against an active adversary.** When $\mathcal{A}$ controls the network, it can run the protocol with each party on its own. Then the goal is [authenticated key exchange](/authenticated-key-exchange/): each party must also know who holds the key. The models of Bellare and Rogaway (1993) and Canetti and Krawczyk (2001) define it; see [session key](/session-key/). This needs some prior trusted data, such as a public key in a certificate, a password, or a check over a second channel.

## Variants

- **Passive or active adversary**, as above.
- **Group key agreement.** Three or more parties agree on one key ([group Diffie-Hellman](/group-diffie-hellman/)).
- **Password-based.** The parties share only a low-entropy password, and the protocol must resist offline guessing ([PAKE](/password-authenticated-key-exchange/)).
- **Non-interactive.** Each party publishes one public key, and each pair derives its key with no further message (static Diffie-Hellman). With a trusted center that loads secrets in advance, this becomes the [key predistribution problem](/key-predistribution-problem/).
- **With forward secrecy.** The key stays secret even if long-term keys leak later ([perfect forward secrecy](/perfect-forward-secrecy/)).
- **Post-quantum and hybrid.** The adversary may have a quantum computer later, so the key must not rest only on discrete logarithms ([hybrid key exchange](/hybrid-key-exchange/)).

## Examples

**Diffie-Hellman with toy numbers.** Take $p = 23$ and $g = 2$, which has order $q = 11$ modulo 23. Alice picks $a = 6$ and sends $A = 2^6 \bmod 23 = 18$. Bob picks $b = 9$ and sends $B = 2^9 \bmod 23 = 6$. Alice computes $B^a = 6^6 \bmod 23 = 12$, and Bob computes $A^b = 18^9 \bmod 23 = 12$. Both hold 12. An eavesdropper sees 18 and 6; with numbers this small she finds $a = 6$ by trying the 11 powers of 2, but with a 2048-bit prime this search is out of reach. Both parties contribute: the key depends on $a$ and on $b$.

**Merkle's puzzles.** Alice sends $N$ puzzles; Bob solves one and sends back its public label. The honest parties do about $N$ units of work, and an eavesdropper about $N^2/4$ ([Merkle's puzzles](/merkle-puzzles/)). This is key agreement with a gap that is only quadratic.

**Non-example: RSA key transport.** In TLS 1.2 with RSA key exchange, the client picks the 48-byte premaster secret and encrypts it under the server's RSA key. The server contributes nothing to that secret, so this is [key transport](/key-transport-problem/), not key agreement.

**Non-example: a fixed contribution.** If Bob always sends $B = 1$ (or another element of small order), the key $B^a$ is 1 whatever Alice picks. A protocol must reject such values; see [small subgroup attack](/small-subgroup-attack/).

## Known algorithms

- **[Diffie-Hellman](/diffie-hellman/)** in a prime-order subgroup of $\mathbb{Z}_p^*$, secure against passive adversaries under the [DDH assumption](/decisional-diffie-hellman/).
- **[ECDH](/ecdh/)** on NIST curves, and **[X25519](/x25519/)** and **[X448](/x448/)** on Montgomery curves (RFC 7748).
- **[Merkle's puzzles](/merkle-puzzles/)**: a quadratic gap from any one-way function modelled as a random oracle.
- **Authenticated protocols**: [station-to-station](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/), [MQV](/mqv/) and [HMQV](/hmqv/), the [Noise protocol framework](/noise-protocol-framework/), and [X3DH](/x3dh/).
- **KEM-based key exchange.** One side sends a [KEM](/key-encapsulation-mechanism/) public key and the other side encapsulates to it, as with [ML-KEM](/crystals-kyber/). The key is fixed by the encapsulating side's random choice and the public key, so this sits between agreement and transport. [Hybrid key exchange](/hybrid-key-exchange/) combines it with X25519.

## Bounds

**No key agreement against an unbounded eavesdropper.** With only a public noiseless channel and private random coins, every protocol with error $\varepsilon$ lets an adversary with unlimited computing time output $k_B$ with probability at least $1 - \varepsilon$.

*Proof.* Fix a transcript $t$ of positive probability. The messages of $A$ are functions of $r_A$ and of the earlier messages, and the same holds for $B$ with $r_B$. By induction on the number of messages, the set of coin pairs that give $t$ is a product $R_A(t) \times R_B(t)$: each new message of $A$ restricts only $r_A$, and each new message of $B$ restricts only $r_B$. Since $r_A$ and $r_B$ are independent and uniform, given $T = t$ they are still independent, uniform on $R_A(t)$ and on $R_B(t)$. The adversary samples $r'_A$ uniformly from $R_A(t)$ and outputs $k_A(r'_A, t)$. Given $t$, the pair $(r'_A, r_B)$ has the same distribution as $(r_A, r_B)$, so $\Pr[k_A(r'_A, t) = k_B] = \Pr[k_A = k_B] \ge 1 - \varepsilon$. $\blacksquare$

So every solution rests on a computational assumption (or on extra resources such as noisy channels or quantum channels).

**Black-box limits.** Impagliazzo and Rudich (STOC 1989) showed that no black-box reduction builds key agreement from a one-way permutation: relative to a random permutation oracle, no protocol is secure. Barak and Mahmoody-Ghidary (CRYPTO 2009) showed that in the [random oracle model](/random-oracle-model/), if the parties make $n$ oracle queries, an eavesdropper finds the key with $O(n^2)$ queries. Merkle's puzzles reach this bound, so the quadratic gap is the best possible from a random oracle alone. Practical key agreement therefore uses structured assumptions: [CDH](/computational-diffie-hellman/) and DDH, or lattice problems such as [Module-LWE](/module-learning-with-errors/).

**Cost of the round trip.** Two messages are enough (Diffie-Hellman), and one message is enough when one party has a static public key that the other already knows.

## Reductions

- **To and from public-key encryption.** A two-message key agreement in which the first message does not depend on the second party gives [public-key encryption](/public-key-encryption/): the first message is the public key, and the sender runs the second side, gets the key, and uses it as a one-time pad. Diffie-Hellman gives [ElGamal encryption](/elgamal-encryption/) in this way. In the other direction, a public-key encryption scheme gives key transport, and a CPA-secure scheme gives a two-message protocol that is secure against eavesdroppers.
- **Diffie-Hellman security.** Computing the Diffie-Hellman key from the transcript is the [CDH problem](/computational-diffie-hellman/). Telling the key from a random group element is the [DDH problem](/decisional-diffie-hellman/). With a key derivation function modelled as a random oracle, CDH is enough for the derived key.
- **Discrete logarithm.** An algorithm for the [discrete logarithm problem](/discrete-logarithm-problem/) breaks Diffie-Hellman. Whether the converse holds in every group is open.

## Applications

- TLS 1.3 uses only (EC)DHE key agreement, or hybrid post-quantum key exchange, for new keys; it removed static RSA key transport (RFC 8446, Section 1.2).
- SSH, IPsec IKEv2, WireGuard and the Signal protocol all start with Diffie-Hellman key agreement on X25519 or on a NIST curve.
- Messaging apps run key agreement many times per conversation in the [double ratchet](/double-ratchet/), to recover secrecy after a key leak.

## References
