---
tag: PS9P4P
kind: algorithm
slug: schnorr-signature
name: Schnorr signature
aliases:
- Schnorr identification-based signature
- BIP 340 signature
area: cryptography/signatures
level: advanced
summary: "Sign with R = g^k and s = k + e x, where e hashes R and the message. EUF-CMA in the random oracle model under discrete log, with a loose reduction. BIP 340 is the Bitcoin form."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [Claus-Peter Schnorr]
  note: Presented at CRYPTO 1989 and published in the Journal of Cryptology in 1991. US patent 4,995,082 expired in 2008. BIP 340 put the scheme on secp256k1 for Bitcoin in 2020.
prereqs: [schnorr-identification-protocol, discrete-logarithm-problem, random-oracle-model, digital-signature]
see_also: [fiat-shamir-heuristic, forking-lemma, existential-unforgeability, ecdsa, ed25519, musig, batch-verification, adaptor-signature]
sources:
  - paper: "Claus-Peter Schnorr, Efficient identification and signatures for smart cards, CRYPTO 1989, LNCS 435, Springer, 1990, pages 239 to 252"
    locator: the identification protocol, its signature form and the preprocessing of the commitments
  - paper: doi:10.1007/BF00196725
    title: Claus-Peter Schnorr, Efficient signature generation by smart cards, Journal of Cryptology 4(3), 1991, pages 161 to 174
    locator: the identification scheme, the signature (e, y) with e = h(x, m) and y = r + s e mod q, and the parameter choices
  - paper: doi:10.1007/s001450010003
    title: David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, pages 361 to 396
    locator: the forking lemma and its application to the Schnorr signature in the random oracle model
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr Signatures for secp256k1, 2020
    locator: sections Design, Default Signing, Verification, and the file test-vectors.csv (rows 0, 1, 2, 4, 5 and 6 are copied in the tests)
  - paper: "Mihir Bellare and Gregory Neven, Multi-signatures in the plain public-key model and a general forking lemma, ACM CCS 2006, pages 390 to 399"
    locator: the general forking lemma (the bound frk >= acc (acc/q - 1/h))
  - paper: "Yannick Seurin, On the exact security of Schnorr-type signatures in the random oracle model, EUROCRYPT 2012, LNCS 7237, Springer, 2012, pages 554 to 571"
    locator: the result that the loss of the forking reduction cannot be avoided by an algebraic reduction, under the one-more discrete log assumption
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 13 (digital signature schemes), the Fiat-Shamir transform and the Schnorr identification and signature schemes
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 19 (identification and signatures from sigma protocols), the Schnorr identification protocol and the Schnorr signature with its security proof
---

The Schnorr signature signs a message with one exponentiation: pick a fresh nonce $k$, publish $R = g^k$, hash $R$ with the message to get a challenge $e$, and reply $s = k + e x$, where $x$ is the secret key. It is the [Schnorr identification protocol](/schnorr-identification-protocol/) made non-interactive by the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/). It is [existentially unforgeable](/existential-unforgeability/) under chosen message attack (EUF-CMA) in the [random oracle model](/random-oracle-model/) if the [discrete logarithm problem](/discrete-logarithm-problem/) is hard, by the [forking lemma](/forking-lemma/), with a reduction that loses a factor of about the number of hash queries. Its linear form is the reason for [batch verification](/batch-verification/), [MuSig](/musig/), [FROST](/threshold-signature/) and [adaptor signatures](/adaptor-signature/), and BIP 340 put it into Bitcoin in 2020.

**Notation.** $G$ is a cyclic group of prime order $q$ with generator $g$, written multiplicatively ($g^k$); on an elliptic curve the same steps are written additively ($kG$). $x \in [1, q-1]$ is the secret key and $y = g^x$ the public key. $H$ maps a group element and a message to $\mathbb{Z}_q$. $\lambda$ is the security parameter, $q_h$ and $q_s$ are the numbers of hash and signing queries of an adversary $A$, and $t$ is its running time.

## In plain words

The signer has a secret number and publishes a lock made from it. To sign, the signer picks a new random number for this one signature and publishes its lock too. A hash of that lock and the message gives a challenge number. The signer answers with the random number plus the challenge times the secret.

Anyone can check the answer against the two locks without learning the secret, because the locks combine in the same way as the numbers. The random number hides the secret in the answer, like a one-time pad. The hash plays the role of an honest examiner who picks the challenge only after the lock is fixed, so a forger cannot pick the lock to fit a challenge it already knows.

The random number must be new and secret each time. Two answers with the same random number give away the secret with one division.

## The problem

The scheme solves the [digital signature](/digital-signature/) problem: a [signature scheme](/signature-scheme/) with key generation, signing and verification, such that each honest signature verifies and no efficient adversary that sees signatures on messages of its choice can produce a valid signature on a new message (EUF-CMA, the game of the [chosen message attack](/chosen-message-attack/) page).

## The algorithm

### The identification protocol

Schnorr first built an interactive proof that the prover knows $x = \log_g y$. It is a [sigma protocol](/sigma-protocol/) with three moves.

1. The prover picks $k$ uniform in $\mathbb{Z}_q$ and sends the commitment $R = g^k$.
2. The verifier sends a uniform challenge $e \in \mathbb{Z}_q$ (Schnorr used a short challenge of $t$ binary digits, with $2^t \le q$).
3. The prover sends $s = k + e x \bmod q$. The verifier accepts if $g^s = R \cdot y^e$.

The protocol has special soundness: two accepting answers $(R, e, s)$ and $(R, e', s')$ with $e \ne e'$ give $x = (s - s')/(e - e') \bmod q$. It is honest-verifier zero knowledge: pick $e$ and $s$ first and set $R = g^s y^{-e}$, and the triple has the same distribution as a real one. The full treatment is on the [identification protocol](/schnorr-identification-protocol/) page.

### The signature

The Fiat-Shamir step replaces the verifier by a hash of the commitment and the message.

```pseudo id=main
KEYGEN()
L0  x ← uniform in [1, q − 1];  y ← g^x;  return (x, y)

SIGN(x, m)
L1  k ← uniform in [1, q − 1]              ▷ fresh and secret for each signature
L2  R ← g^k
L3  e ← H(R ‖ m) mod q
L4  s ← (k + e·x) mod q
L5  return σ = (R, s)                      ▷ or σ = (e, s), see below

VERIFY(y, m, σ = (R, s))
L6  if R ∉ G or s ∉ [0, q − 1] then return false
L7  e ← H(R ‖ m) mod q
L8  return g^s = R · y^e
```

**The two forms.** A signature can carry $R$ or $e$.

- **$(e, s)$**, the form of Schnorr's papers. The verifier recomputes $R' = g^s y^{-e}$ and checks $e = H(R' \| m)$. The value $e$ can be shorter than a group element: it needs only about $\lambda$ or $2\lambda$ binary digits, so the signature can be shorter. A wrong signature fails at the hash, so there is no linear equation to combine across signatures.
- **$(R, s)$**, the form of BIP 340 and of [Ed25519](/ed25519/). The check of line L8 is a linear equation in the group, so many signatures can be checked together with random weights ([batch verification](/batch-verification/)), and several signers can add their $R$ and $s$ values ([MuSig](/musig/)). The signature is one group element and one scalar.

The two forms carry the same information. From $(R, s)$, compute $e$ by line L7. From $(e, s)$, compute $R = g^s y^{-e}$. So a forgery in one form gives a forgery in the other, and the same security proof covers both.

Schnorr's paper writes the public key as $v = \alpha^{-s}$ and the answer as $y = r + s e$, with the roles of the letters swapped from the modern form here. The verification $\bar{x} = \alpha^{y} v^{e}$ then needs no inverse. The difference is only a sign convention.

### BIP 340 on secp256k1

BIP 340 fixes the group to the curve secp256k1, $y^2 = x^3 + 7$ over $\mathbb{F}_p$ with $p = 2^{256} - 2^{32} - 977$ and a prime order $n$, and makes four choices.

- **x-only keys.** A public key is the 32-byte $x$ coordinate of $P = d' G$. The point with that $x$ and an even $y$ is the key. The signer uses $d = d'$ if $P$ has even $y$ and $d = n - d'$ otherwise, so $d G$ always has even $y$.
- **x-only nonces.** $R$ is sent as its $x$ coordinate. The signer negates $k$ when $R = k G$ has an odd $y$, and the verifier rejects an $R$ with odd $y$. A signature is 64 bytes: $x(R)$ and $s$.
- **Tagged hashes.** $\mathrm{hash}_{tag}(z) = \mathrm{SHA256}(\mathrm{SHA256}(tag) \| \mathrm{SHA256}(tag) \| z)$, with the tags BIP0340/aux, BIP0340/nonce and BIP0340/challenge. Different tags make the three hashes independent, and a hash in one protocol cannot be replayed in another.
- **Key prefixing and a synthetic nonce.** The challenge is $e = \mathrm{hash}_{\text{challenge}}(x(R) \| x(P) \| m) \bmod n$, so it covers the public key. The nonce is $k = \mathrm{hash}_{\text{nonce}}(t \| x(P) \| m) \bmod n$ with $t = d \oplus \mathrm{hash}_{\text{aux}}(a)$ for 32 bytes $a$ of fresh randomness. It stays safe when $a$ is all zero, and it gives some protection against faults when $a$ is random (see [deterministic nonce generation](/deterministic-nonce-generation/)).

Verification lifts $x(P)$ to the point with even $y$, rejects $r \ge p$ and $s \ge n$, computes $R = sG - eP$ and accepts if $R$ is not the point at infinity, has even $y$ and has $x(R) = r$.

## Example

Take the toy group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ (here $2039 = 2 \cdot 1019 + 1$) with $g = 4$, and let $H(R \| m)$ be SHA-256 of the 2-byte $R$ followed by $m$, reduced mod $q$. This group is far too small to be secure.

| step | value |
|---|---|
| secret key $x$ | 123 |
| public key $y = 4^{123} \bmod 2039$ | 572 |
| nonce $k$ | 456 |
| $R = 4^{456} \bmod 2039$ | 1777 |
| $e = H(1777 \| \text{"hi"}) \bmod 1019$ | 1010 |
| $s = 456 + 1010 \cdot 123 \bmod 1019$ | 368 |

The signature is $(R, s) = (1777, 368)$, or $(e, s) = (1010, 368)$ in the other form. Verification computes $4^{368} \bmod 2039 = 418$ and $1777 \cdot 572^{1010} \bmod 2039 = 418$, so it accepts. In the $(e, s)$ form it computes $4^{368} \cdot 572^{-1010} \bmod 2039 = 1777$, hashes it with the message and gets 1010 again.

For a real example, BIP 340 test vector 0 has the secret key 3, the public key `F9308A01...BCE036F9` (the $x$ coordinate of $3G$), the message of 32 zero bytes, $a$ of 32 zero bytes, and the signature `E907831F...DCA82151` followed by `25F66A4A...310536C0`. The code on this page reproduces vectors 0, 1 and 2 byte for byte.

## Correctness

An honest signature verifies: $g^s = g^{k + e x} = g^k (g^x)^e = R \cdot y^e$, because $g$ has order $q$ and $s \equiv k + ex \pmod q$. For BIP 340 the same identity holds with $d$ and $k$ after the two negations, because $d G = P$ and $k G = R$ for the even-$y$ points $P$ and $R$ that the verifier rebuilds. The full proof, with the $(e, s)$ form and the BIP 340 negations, is below.

## Complexity

Let $n$ be the number of binary digits of the group order ($n = 256$ for secp256k1).

- **Signing**: one fixed-base exponentiation $g^k$ (about $n$ squarings and $n/2$ multiplications by double and add, fewer with precomputed tables because $g$ is fixed), one hash and one multiplication mod $q$. BIP 340 adds one more fixed-base multiplication to compute $P$ when the key is not cached.
- **Verification**: two exponentiations, or one double exponentiation $g^s y^{-e}$ by Shamir's trick, which shares the squarings of the two exponentiations.
- **Sizes**: a public key of one group element (32 bytes in BIP 340), a signature of one group element and one scalar (64 bytes), or $e$ and $s$ in the other form.
- **Time**: with schoolbook field arithmetic each group operation costs $\Theta(n^2)$ word operations, so both signing and verification take $\Theta(n^3)$. Space is $\Theta(n)$.

## Properties

- **EUF-CMA in the random oracle model under discrete log.** Let $A$ forge with probability $\varepsilon$ after $q_h$ hash and $q_s$ signing queries. The reduction answers signing queries with the zero knowledge simulator and programs $H$, and fails with probability at most $q_s(q_h + q_s)/q$. Then the [general forking lemma](/forking-lemma/) with $Q = q_h + 1$ oracle answers from a set of size $q$ gives a discrete log solver that runs $A$ twice and succeeds with probability $\varepsilon_{DL} \ge \varepsilon'(\varepsilon'/Q - 1/q)$, where $\varepsilon' = \varepsilon - q_s(q_h + q_s)/q$. Solved for the forger: $\varepsilon \le \sqrt{Q \cdot \varepsilon_{DL}} + Q/q + q_s(q_h+q_s)/q$. Pointcheval and Stern (1996, 2000) gave the first proof, and Bellare and Neven (2006) gave the clean general form used here.
- **The reduction is loose.** The square root and the factor $Q$ cost a lot: with $Q = 2^{60}$ and $\varepsilon_{DL} \le 2^{-128}$, the bound only gives $\varepsilon \le 2^{-34}$, and the solver runs the forger twice. Seurin (2012) showed that no algebraic reduction from discrete log can avoid a loss of about $q_h$, if the one-more discrete log problem is hard. Proofs in the [generic group model](/generic-group-model/) or the algebraic group model are tight, but they rest on stronger idealizations.
- **Strongly unforgeable.** For a fixed $R$ and $m$, the value $e$ and so $s$ is unique mod $q$, and BIP 340 rejects $s \ge n$. So a valid signature cannot be changed into another valid signature on the same message ([strong unforgeability](/strong-unforgeability/)), unlike [ECDSA](/ecdsa/) with its $(r, -s)$ twin.
- **Linear.** The check $g^s = R y^e$ is linear in $(k, x, s)$. Sums of nonces and keys give signatures under sums of keys, which [MuSig](/musig/) and [FROST](/threshold-signature/) use, and a pre-signature shifted by a secret gives an [adaptor signature](/adaptor-signature/).
- **Randomized.** The textbook scheme needs a fresh uniform $k$. BIP 340 and Ed25519 derive $k$ from the key and the message, which removes the need for a good random source at signing time.

## Variants and improvements

- **BIP 340**, described above, with 32-byte keys, 64-byte signatures and batch verification. Bitcoin uses it in Taproot (BIP 341).
- **EdDSA and [Ed25519](/ed25519/)** are Schnorr signatures on a twisted Edwards curve with a hash-derived nonce and the challenge $H(R \| A \| m)$.
- **Key prefixing.** Hashing the public key into $e$ (as BIP 340 and EdDSA do) stops related-key attacks: without it, a signature $(R, s)$ under $y$ is also valid under $y g^{\delta}$ after the change $s \mapsto s + e \delta$. The [Fiat-Shamir](/fiat-shamir-heuristic/) page shows this in code.
- **Preprocessing.** Schnorr's paper computes the pairs $(k, g^k)$ before the message arrives, so a smart card signs with one hash and one multiplication mod $q$.
- **Multi and threshold signatures.** [MuSig](/musig/) and [MuSig2](/musig/) for $n$ of $n$, [FROST](/threshold-signature/) for $t$ of $n$, both with a final signature that a plain verifier accepts.

## When to use it

Use a Schnorr-type signature when you want short signatures with a clean proof, batch verification, or multi-party signing. On Bitcoin, use BIP 340 through libsecp256k1. Elsewhere, [Ed25519](/ed25519/) through libsodium or a FIPS 186-5 implementation is the common choice of the same family. If a standard requires FIPS 186-5 and an elliptic curve over a NIST prime, [ECDSA](/ecdsa/) or EdDSA are the approved options; FIPS 186-5 does not list BIP 340.

## Pitfalls

- **A repeated or biased nonce.** Two signatures with the same $k$ and different $e$ give $x = (s_1 - s_2)/(e_1 - e_2) \bmod q$. A few known binary digits of each nonce over many signatures give $x$ by a lattice attack. See the [nonce reuse attack](/nonce-reuse-attack/) page and use [deterministic nonce generation](/deterministic-nonce-generation/).
- **No key in the hash.** Without key prefixing, signatures move between related keys, which breaks key derivation schemes such as BIP 32 with public derivation.
- **Not checking the ranges.** Line L6 must reject $s \ge q$ and an $R$ outside the group. BIP 340 test vectors 5 and 6 check a key not on the curve and an $R$ with odd $y$.
- **Mixing the two forms.** A verifier for $(e, s)$ that also accepts $(R, s)$ with a different hash input can be fooled into checking the wrong equation. Fix one encoding.
- **Naive sums of keys.** Adding public keys of several signers without the MuSig coefficients lets one signer choose a rogue key that cancels the others. See the [multisignature problem](/multisignature-problem/).
- **Side channels.** The exponentiation in line L2 and the multiplication in line L4 must not leak timing, or the nonces become partly known and a lattice attack follows.

## Implementations

The Python code on this page implements the toy scheme in both forms and BIP 340 with its own secp256k1 arithmetic, and the tests check BIP 340 test vectors 0, 1, 2, 4, 5 and 6, copied by hand from test-vectors.csv. The code is for study only. It is not constant time, it branches on secret values, and it must not be used to protect real data. Use libsecp256k1 for BIP 340, and libsodium or a FIPS 140 validated module for other signatures.

## History

Claus-Peter Schnorr presented the identification protocol and its signature form at CRYPTO 1989, aimed at smart cards that could not afford RSA, and the journal version "Efficient signature generation by smart cards" appeared in 1991. He held US patent 4,995,082, which covered the scheme until it expired in 2008. While the patent was in force, the standard discrete log signatures were the ElGamal-like [DSA](/dsa/) and later [ECDSA](/ecdsa/).

Pointcheval and Stern proved the scheme secure in the random oracle model with the forking lemma at Eurocrypt 1996, in the journal version of 2000. Bellare and Neven gave the general forking lemma in 2006, and Seurin showed in 2012 that the loss in this proof is needed for algebraic reductions. After the patent expired, Bernstein and others built Ed25519 (2011) on the same idea, and Wuille, Nick and Ruffing wrote BIP 340 (2020), which made Schnorr signatures part of Bitcoin with Taproot.

## References
