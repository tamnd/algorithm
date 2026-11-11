---
tag: 99NZYX
kind: algorithm
slug: schnorr-identification-protocol
name: Schnorr identification protocol
aliases:
- Schnorr protocol
area: cryptography/protocols
level: advanced
summary: A sigma protocol where a prover shows knowledge of a discrete logarithm to authenticate itself.
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [Claus-Peter Schnorr]
  note: Presented at CRYPTO 1989 and published in the Journal of Cryptology in 1991, for smart cards that could not afford RSA. Bellare and Palacio proved security against active attacks in 2002.
prereqs: [sigma-protocol, discrete-logarithm-problem]
see_also: [schnorr-signature, fiat-shamir-heuristic, proof-of-knowledge, feige-fiat-shamir-identification, entity-authentication, challenge-response-authentication, safe-prime, forking-lemma]
sources:
  - paper: "Claus-Peter Schnorr, Efficient identification and signatures for smart cards, CRYPTO 1989, LNCS 435, Springer, 1990, 239-252"
    title: Claus-Peter Schnorr, Efficient identification and signatures for smart cards
    locator: the identification protocol with a short challenge and the preprocessing of commitments
  - paper: doi:10.1007/BF00196725
    title: Claus-Peter Schnorr, Efficient signature generation by smart cards, Journal of Cryptology 4(3), 1991, 161-174
    locator: the identification scheme, its security against a cheating prover, and the parameter choices for p, q and the challenge length
  - paper: doi:10.1007/3-540-45708-9_11
    title: Mihir Bellare and Adriana Palacio, GQ and Schnorr identification schemes, proofs of security against impersonation under active and concurrent attacks, CRYPTO 2002, LNCS 2442, 162-177
    locator: security against passive impersonation under the discrete logarithm assumption, and against active and concurrent impersonation under the one-more discrete logarithm assumption
  - url: https://www.rfc-editor.org/rfc/rfc3526
    title: Tero Kivinen and Mika Kojo, RFC 3526, More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE), 2003
    locator: Section 3, the 2048-bit MODP group (group 14), its formula with pi and its hexadecimal value, generator 2
  - paper: "Tatsuaki Okamoto, Provably secure and practical identification schemes and corresponding signature schemes, CRYPTO 1992, LNCS 740, 31-53"
    title: Tatsuaki Okamoto, Provably secure and practical identification schemes and corresponding signature schemes
    locator: the two-generator variant that is witness indistinguishable and secure against active attacks under the discrete logarithm assumption
  - url: https://www.cs.au.dk/~ivan/Sigma.pdf
    title: Ivan Damgård, On Σ-protocols, lecture notes, Aarhus University, 2010
    locator: the Schnorr protocol as the first example of a Σ-protocol, with special soundness and the simulator
  - url: https://toc.cryptobook.us/
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: the chapter on identification and signatures from sigma protocols (the Schnorr identification protocol, its security against eavesdropping and active attacks)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 13, identification schemes and the Schnorr identification scheme
---

The Schnorr identification protocol lets a prover show that it knows the secret key $x$ of a public key $y = g^x$, without showing $x$. The prover sends $a = g^k$ for a fresh random $k$, the verifier sends a random challenge $c$, and the prover answers $z = k + cx \bmod q$. The verifier checks $g^z = a y^c$. It is the basic [sigma protocol](/sigma-protocol/), and the [Schnorr signature](/schnorr-signature/) is this protocol with the challenge replaced by a hash. A cheating prover passes with probability $2^{-t}$ for a $t$-bit challenge, and two answers with the same $k$ give away $x$.

**Notation.** $G$ is a cyclic group of prime order $q$ with generator $g$, written multiplicatively. Here $G$ is the subgroup of squares in $\mathbb{Z}_p^*$ for a [safe prime](/safe-prime/) $p = 2q + 1$. $x \in [1, q-1]$ is the secret key and $y = g^x$ the public key. The challenge has $t$ binary digits, $c \in [0, 2^t - 1]$, with $2^t \le q$. $n$ is the number of binary digits of $q$.

## In plain words

The prover has a secret number and has published a lock made from it. To prove that it holds the secret, it makes a new random number, sends the lock of that number, and waits for a question. The question is a random number from the verifier. The prover answers with its random number plus the question times the secret.

The verifier checks the answer with the two locks only. The random number hides the secret in the answer, in the same way as a one-time pad. But the prover had to fix its first lock before it saw the question, and a prover that could answer two different questions for the same lock would know the secret. So a prover without the secret can only guess the question in advance, and it is caught unless the guess is right.

## The problem

This is the problem of [entity authentication](/entity-authentication/) with public keys: a verifier who holds $y$ wants to know that the party it talks to now holds the matching $x$. An identification scheme is secure if no adversary can make the verifier accept without $x$. In a passive attack, the adversary first sees honest runs between the prover and verifiers. In an active attack, the adversary first acts as a verifier against the real prover, with challenges of its choice, and then tries to impersonate the prover.

## The algorithm

```pseudo id=main
KEYGEN()
L1  x ← uniform in [1, q − 1];  y ← g^x;  publish y

IDENTIFY(prover with x, verifier with y)
L2  prover:   k ← uniform in Z_q;  a ← g^k;  send a
L3  verifier: c ← uniform in [0, 2^t − 1];  send c
L4  prover:   z ← (k + c·x) mod q;  send z
L5  verifier: if y ∉ G or a ∉ G or z ∉ [0, q − 1] then reject
L6  verifier: accept iff g^z = a · y^c
```

The membership test $y \in G$ for the subgroup of squares is $y^q \bmod p = 1$ with $0 < y < p$. The prover can compute the pairs $(k, g^k)$ before the session starts, so line L2 costs nothing at the time of identification and line L4 is one multiplication mod $q$. This preprocessing was the point of Schnorr's design for smart cards.

## Example

Take the toy group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$ and $t = 3$. This group is far too small to be secure.

| step | value |
| --- | --- |
| secret key $x$ | 123 |
| public key $y = 4^{123} \bmod 2039$ | 572 |
| nonce $k$, commitment $a = 4^{456} \bmod 2039$ | 456, 1777 |
| challenge $c$ | 5 |
| response $z = 456 + 5 \cdot 123 \bmod 1019$ | 52 |
| check: $4^{52} \bmod 2039$ and $1777 \cdot 572^5 \bmod 2039$ | 1252 and 1252 |

If the prover reuses $k = 456$ in a second session and gets $c' = 2$, it answers $z' = 456 + 246 = 702$. Then anyone who saw both sessions computes $x = (52 - 702) \cdot (5 - 2)^{-1} \bmod 1019 = (-650) \cdot 340 \bmod 1019 = 123$.

For a real size the code uses group 14 of RFC 3526: a 2048-bit safe prime with generator $g = 2$. Its value is $p = 2^{2048} - 2^{1984} - 1 + 2^{64}(\lfloor 2^{1918} \pi \rfloor + 124476)$. The code computes $\pi$ by Machin's formula with 64 guard bits, builds $p$, and the test checks it against the 64 hexadecimal words of RFC 3526 Section 3, from `FFFFFFFF FFFFFFFF C90FDAA2 2168C234` to `15728E5A 8AACAA68 FFFFFFFF FFFFFFFF`. Since $p \equiv 7 \pmod 8$, the number 2 is a square mod $p$, so it generates the subgroup of prime order $q = (p - 1)/2$. RFC 3526 only gives the group; there are no official test vectors for the identification protocol itself.

## Correctness

An honest run is accepted: $g^z = g^{k + cx} = g^k (g^x)^c = a y^c$, because $g$ has order $q$. Two more facts make the protocol a proof of knowledge that leaks nothing to an honest verifier. Two accepted answers to $c_1 \ne c_2$ for the same $a$ give $x = (z_1 - z_2)/(c_1 - c_2) \bmod q$, so a prover accepted with probability above $2^{-t}$ knows $x$. And for a fixed $c$, the triple $(g^z y^{-c}, c, z)$ with uniform $z$ has the same distribution as a real run. The proofs are below.

## Complexity

- **Prover**: one fixed-base exponentiation $g^k$, which can be done in advance, and one multiplication mod $q$ online.
- **Verifier**: the product $g^z \cdot y^{-c}$, which is a double exponentiation with an $n$-bit and a $t$-bit exponent, plus the membership tests. The test for $a$ costs one more exponentiation in $\mathbb{Z}_p^*$; on prime-order elliptic curves it is a cheap check that the point is on the curve.
- **Communication**: one group element, $t$ bits and one element of $\mathbb{Z}_q$.
- **Time**: with schoolbook arithmetic, each multiplication of $n$-bit numbers costs $\Theta(n^2)$ word operations and an exponentiation costs $\Theta(n^3)$. In the subgroup of $\mathbb{Z}_p^*$ the numbers have the size of $p$, about $n$ bits for a safe prime. Space is $\Theta(n)$.

## Properties

- **Soundness and knowledge error $2^{-t}$.** A prover that guesses $c$ in advance passes with probability exactly $2^{-t}$, and any prover that passes with probability $\varepsilon > 2^{-t}$ gives $x$ to a rewinding extractor in expected time about $1/(\varepsilon - 2^{-t})$. See [proof of knowledge](/proof-of-knowledge/).
- **Secure against passive attacks under discrete log.** Honest transcripts can be simulated without $x$, so an eavesdropper learns nothing that helps; an impersonator then gives $x$ by extraction.
- **Secure against active attacks under the one-more discrete log assumption.** Bellare and Palacio (2002) proved security against active and concurrent impersonation, where the adversary first plays verifier against the real prover. The proof uses the stronger one-more discrete logarithm assumption.
- **Zero knowledge depends on the challenge length.** For a fixed challenge, the simulator is exact, so the protocol is honest-verifier zero knowledge for each $t$. For a malicious verifier, the rewinding simulator needs about $2^t$ tries, so the protocol is zero knowledge only when $2^t$ is polynomial. With the long challenges used in practice, it is only known to be honest-verifier zero knowledge.
- **Witness hiding and indistinguishability.** Each $y$ has only one $x$, so witness indistinguishability says nothing here. Okamoto's two-generator variant has many witnesses per key, which gives security against active attacks under plain discrete log.

## Variants and improvements

- **[Schnorr signature](/schnorr-signature/).** Replace $c$ by $H(a \| m)$, the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/). This page does not cover the signature.
- **Okamoto identification (1992).** Public key $y = g_1^{x_1} g_2^{x_2}$, commitment $g_1^{k_1} g_2^{k_2}$, two responses. Secure against active attacks if discrete log is hard.
- **Guillou-Quisquater (1988).** The same three moves in the RSA setting: prove knowledge of an $e$-th root mod $N$.
- **[Feige-Fiat-Shamir identification](/feige-fiat-shamir-identification/).** Square roots modulo a Blum integer instead of discrete logarithms, with many short rounds.
- **Elliptic curves.** The same protocol in a prime-order elliptic curve group, with 32-byte elements at the 128-bit security level.
- **Proofs about other statements.** The same form gives proofs of equal logarithms, of an opening of a [Pedersen commitment](/pedersen-commitment/), and of OR statements; see [sigma protocol](/sigma-protocol/).

## When to use it

Use it as a building block or to study identification: it is the simplest proof of knowledge in a discrete log group, and its analysis is the template for many protocols. For a login over a network, a [challenge-response](/challenge-response-authentication/) with a signature (for example Ed25519 through libsodium) is the usual choice, because a signature can be checked later and bound to a session. Use the interactive protocol when you need deniability, since a transcript can be simulated and so does not convince a third party.

## Pitfalls

- **A repeated or predictable nonce.** Two answers with the same $k$ give $x$ by one division, as in the example. A few known binary digits of many nonces give $x$ by a lattice attack. Use a fresh $k$ from a good random source for each session.
- **No membership tests.** If $a$ or $y$ is not checked to be in the subgroup of order $q$, an element of small order can make the check pass for some challenges without $x$, or leak $x \bmod$ a small factor in related protocols.
- **Relay attacks.** The protocol proves that someone who holds $x$ answered, not that the answer came from the party in front of you. An attacker can pass messages between a real prover and a verifier (mafia fraud). Bind the run to a session or a channel.
- **A short challenge used alone.** With $t = 20$, a guessing impersonator passes once in a million tries, which can be too often for an online service. Choose $t$ for the number of attempts an attacker can make.
- **Side channels.** The exponentiation of line L2 and the multiplication of line L4 must not leak timing, or partial knowledge of $k$ follows.

## Implementations

The Python code on this page implements the protocol in the toy group and in RFC 3526 group 14, a guessing impersonator, the simulator, and the recovery of $x$ from a reused nonce. The tests check the group 14 prime against the hexadecimal text of RFC 3526, the example above, that the guessing impersonator passes exactly $1/8$ of all (guess, challenge) pairs for $t = 3$, that for each challenge exactly one response is accepted, and that the simulated transcripts for a fixed challenge are exactly the real ones. The code is for study only. It is not constant time and must not be used to protect real data. Use libsodium or a FIPS 140 validated module for real keys.

## History

Claus-Peter Schnorr presented the protocol at CRYPTO 1989, as an identification and signature scheme for smart cards. The journal version, "Efficient signature generation by smart cards", appeared in 1991. Schnorr chose a short challenge and a subgroup of prime order $q$ much smaller than $p$, so that the card did only a multiplication mod $q$ online. The protocol came after the [Feige-Fiat-Shamir](/feige-fiat-shamir-identification/) scheme of 1986 to 1988, which uses square roots and many rounds. Okamoto (1992) gave a variant with a proof against active attacks, and Bellare and Palacio (2002) proved the original protocol secure against active and concurrent attacks under the one-more discrete logarithm assumption. Cramer's thesis (1996) and later Damgård's notes made it the first example of a sigma protocol.

## References
