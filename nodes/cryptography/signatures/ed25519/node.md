---
tag: 2THJ4W
kind: algorithm
slug: ed25519
name: Ed25519 (EdDSA)
aliases:
- EdDSA
- Edwards-curve Digital Signature Algorithm
area: cryptography/signatures
level: intro
summary: "A deterministic Schnorr signature on the twisted Edwards curve edwards25519 with SHA-512: 32-byte keys, 64-byte signatures, no random nonce. RFC 8032 and FIPS 186-5."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2011
  people: [Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, Bo-Yin Yang]
  note: Presented at CHES 2011. Standardized in RFC 8032 (2017) and in FIPS 186-5 (2023). Ed448 is the larger member of the same family.
prereqs: [schnorr-signature, elliptic-curve-cryptography, sha-2]
see_also: [ecdsa, deterministic-nonce-generation, batch-verification, signature-malleability, strong-unforgeability, nonce-reuse-attack, fiat-shamir-heuristic, elliptic-curve-discrete-logarithm-problem]
sources:
  - paper: doi:10.1007/s13389-012-0027-1
    title: Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe and Bo-Yin Yang, High-speed high-security signatures, Journal of Cryptographic Engineering 2(2), 2012, pages 77 to 89 (first at CHES 2011, LNCS 6917, pages 124 to 142)
    locator: the definition of EdDSA and Ed25519, the hash-derived nonce, the encoding and the batch verification
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), 2017
    locator: Section 5.1 (Ed25519, with 5.1.2 encoding, 5.1.3 decoding, 5.1.5 key generation, 5.1.6 signing and 5.1.7 verification), Section 5.2 (Ed448), and Section 7.1, TEST 1 to TEST 3, copied in the tests
  - url: "https://doi.org/10.6028/NIST.FIPS.186-5"
    title: NIST, FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: Section 7 (the Edwards-Curve Digital Signature Algorithm)
  - paper: "Konstantinos Chalkias, Francois Garillot and Valeria Nikolaenko, Taming the many EdDSAs, Security Standardisation Research (SSR) 2020, LNCS 12529, Springer, 2020"
    locator: the table of the validation rules of many Ed25519 libraries, the test cases that split them, and the strict rules that the paper proposes
  - url: "https://zips.z.cash/zip-0215"
    title: Henry de Valence, ZIP 215, Explicitly Defining and Modifying Ed25519 Validation Rules, 2020
    locator: the rules (non-canonical point encodings accepted, S below the group order, the cofactored equation) that make single and batch verification agree
  - paper: "Jacqueline Brendel, Cas Cremers, Dennis Jackson and Mang Zhao, The provable security of Ed25519, theory and practice, IEEE Symposium on Security and Privacy 2021"
    locator: the proofs of existential and strong unforgeability of Ed25519 in the random oracle model, and the effect of the different validation rules
  - paper: "Mike Hamburg, Ed448-Goldilocks, a new elliptic curve, IACR ePrint 2015/625"
    locator: the curve edwards448 that Ed448 uses
---

Ed25519 is a [Schnorr signature](/schnorr-signature/) on the twisted Edwards curve edwards25519, the Edwards form of Curve25519, with SHA-512 as the hash. Its nonce is a hash of a secret prefix and the message, so signing needs no random numbers and the same message always gets the same signature. Keys are 32 bytes and signatures 64 bytes. Bernstein, Duif, Lange, Schwabe and Yang designed it in 2011 for speed and for safe implementations: complete addition formulas, no secret branches, and no nonce to get wrong. RFC 8032 specifies it, and FIPS 186-5 approved it in 2023. OpenSSH, Tor onion services and many blockchains use it.

**Notation.** $p = 2^{255} - 19$. The curve is $-x^2 + y^2 = 1 + d x^2 y^2$ over $\mathbb{F}_p$ with $d = -121665/121666$. $B$ is the base point with $y = 4/5$ and an even $x$, of prime order $L = 2^{252} + 27742317777372353535851937790883648493$. The curve has $8L$ points, so the cofactor is 8. $\mathrm{ENC}(P)$ is the 32-byte encoding of a point. Scalars are encoded as 32 bytes in little endian, and SHA-512 outputs are read as little endian integers.

## In plain words

Ed25519 is the Schnorr idea with every choice fixed. The secret key is 32 random bytes. Hashing them gives two halves: one half becomes the secret number, the other half is a secret salt.

To sign, the signer hashes the salt with the message to get the one-time random number, so it never needs fresh randomness and can never repeat a number for two different messages. It publishes the point of that number, hashes the point, the public key and the message into a challenge, and answers with the one-time number plus the challenge times the secret.

The verifier checks one equation between points. The curve has a small extra part of size 8. Verifiers that ignore it and verifiers that multiply it away agree on honest signatures but can disagree on crafted ones.

## The problem

Ed25519 solves the [digital signature](/digital-signature/) problem with existential and [strong unforgeability](/strong-unforgeability/) under chosen message attack. Its design goals were also practical: fast signing and verification, small keys and signatures, no random numbers at signing time, and code that is easy to make constant time.

## The algorithm

```pseudo id=main
KEYGEN()
L1  sk ← 32 uniform bytes;  h ← SHA-512(sk)
L2  a ← h[0..31] read as an integer, with its 3 low binary digits and its top digit cleared and digit 254 set
L3  A ← a·B;  prefix ← h[32..63];  return (sk, ENC(A))

SIGN(sk, M)
L4  r ← SHA-512(prefix ‖ M) mod L               ▷ the deterministic nonce
L5  R ← r·B
L6  k ← SHA-512(ENC(R) ‖ ENC(A) ‖ M) mod L      ▷ the challenge
L7  S ← (r + k·a) mod L
L8  return ENC(R) ‖ S as 32 bytes

VERIFY(ENC(A), M, (ENC(R), S))
L9  decode A and R; if one fails or S ≥ L then return false
L10 k ← SHA-512(ENC(R) ‖ ENC(A) ‖ M) mod L
L11 return [8][S]B = [8]R + [8][k]A               ▷ cofactorless: [S]B = R + [k]A
```

The letters follow RFC 8032: $a$ is the secret scalar (RFC 8032 calls it $s$), $k$ is the challenge, not a nonce.

**The twisted Edwards curve.** The curve $-x^2 + y^2 = 1 + d x^2 y^2$ with $d$ not a square in $\mathbb{F}_p$ has a complete addition law: one formula adds any two points, including a point to itself and the neutral element $(0, 1)$, with no special cases. That removes the branches that leak timing in Weierstrass code. The code uses extended coordinates $(X : Y : Z : T)$ with $x = X/Z$, $y = Y/Z$, $xy = T/Z$, where one addition costs about 8 field multiplications.

**The clamping.** Line L2 makes $a$ a multiple of 8, so $a \cdot P$ kills any component of order dividing 8, and it fixes the top binary digit so that a scalar multiplication always runs the same number of steps. Clamping comes from Curve25519 key exchange. For signatures, the multiple of 8 does not matter for honest keys.

**The SHA-512 nonce.** The nonce $r$ hashes a secret prefix with the message. Two different messages get independent nonces (if SHA-512 behaves like a random function), and the same message gets the same nonce and so the same signature, which is harmless. This removes the nonce failures of [ECDSA](/ecdsa/), such as the PlayStation 3 key recovery (see [nonce reuse attack](/nonce-reuse-attack/) and [deterministic nonce generation](/deterministic-nonce-generation/)).

**The encoding.** A point is encoded as its $y$ coordinate in 255 binary digits, little endian, with the low binary digit of $x$ in the top digit of the last byte. Decoding computes $x^2 = (y^2 - 1)/(d y^2 + 1)$ and one square root mod $p$ (with $p \equiv 5 \bmod 8$, a power and maybe a multiplication by $\sqrt{-1}$), and it fails if no root exists. RFC 8032 rejects $y \ge p$ and the encoding of $x = 0$ with the sign digit set.

**Key prefixing.** The challenge in line L6 hashes $\mathrm{ENC}(A)$, so a signature is bound to one public key, and the attack of moving a signature to a related key fails (see the [Fiat-Shamir](/fiat-shamir-heuristic/) page).

### Cofactored and cofactorless verification

Because the cofactor is 8, a point can have a small order component that $L$ does not kill. RFC 8032 Section 5.1.7 says to check the cofactored equation $[8][S]B = [8]R + [8][k]A$, and that it is sufficient, but not required, to check the cofactorless $[S]B = R + [k]A$. Both accept every honest signature. They differ on crafted inputs: let $T$ be a point of order 8 and let the public key be $A' = aB + T$. A signer that knows $a$ signs as usual. Then $[S]B - [k]A' = R - [k]T$. The cofactored check multiplies by 8 and passes for every message. The cofactorless check passes only when $8$ divides $k$, so about 1 message in 8.

Chalkias, Garillot and Nikolaenko (2020) tested many Ed25519 libraries and found that they disagree on such cases: the equation, the check $S < L$, non-canonical encodings of $A$ and $R$, and small order $A$ or $R$. In a consensus system, two nodes that disagree on one signature split the chain. ZIP 215 (Zcash, 2020) fixed one rule set: accept non-canonical point encodings, require $S < L$, and use the cofactored equation, so that single and [batch verification](/batch-verification/) agree. The batch equation is a random combination of cofactored checks, so only the cofactored single check matches it.

## Example

RFC 8032 Section 7.1 TEST 1 has the secret key `9d61b19d...1cae7f60` and the empty message.

| step | value |
|---|---|
| $a$ after clamping | `0x4fe94d90...86837c30` (big endian) |
| prefix | `9b4f0afe...87e01f8f` |
| $\mathrm{ENC}(A)$ | `d75a9801...f707511a` |
| $r = \mathrm{SHA\text{-}512}(\text{prefix}) \bmod L$ | `0x0474a058...300789f3` |
| $\mathrm{ENC}(R)$, first half of the signature | `e5564300...22490155` |
| $k = \mathrm{SHA\text{-}512}(\mathrm{ENC}(R) \| \mathrm{ENC}(A)) \bmod L$ | `0x0454522e...8ebcea86` |
| $S = r + k a \bmod L$, little endian | `5fb88215...8e7a100b` |

The 64 bytes $\mathrm{ENC}(R) \| S$ are the signature of TEST 1. The code reproduces TEST 1 to TEST 3 byte for byte. For the small order example, the point $T$ with encoding `c7176a70...92ac037a` has order 8, and the tests show the two verifiers splitting on about 7 messages in 8 under the key $A' = aB + T$.

## Correctness

From line L7, $S \equiv r + k a \pmod L$, and $B$ has order $L$, so $[S]B = [r]B + [k][a]B = R + [k]A$. This is the cofactorless equation, and multiplying both sides by 8 gives the cofactored one. Line L9 does not reject: $\mathrm{ENC}$ outputs canonical encodings of curve points, which decode back to the same points, and $S < L$. Line L10 hashes the same bytes as line L6. The full proof is below.

## Complexity

Let $n$ be the number of binary digits of $L$ (here $n = 253$).

- **Key generation and signing**: one SHA-512 and one fixed-base scalar multiplication each. Signing hashes the message two times, so it cannot stream the message in one pass (Ed25519ph exists for that).
- **Verification**: one decompression (a square root), one SHA-512, and one double scalar multiplication. Batch verification of many signatures costs much less per signature.
- **Sizes**: public key 32 bytes, signature 64 bytes, secret key 32 bytes.
- **Time**: $\Theta(n)$ group operations of $\Theta(n^2)$ word operations each, so $\Theta(n^3)$ with schoolbook arithmetic, and $\Theta(n)$ space.

## Properties

- **Unforgeable in the random oracle model.** As a Schnorr signature with a hash-derived nonce, Ed25519 is EUF-CMA if the discrete log problem in the group of order $L$ is hard and SHA-512 is modeled as a random oracle; the proof uses the [forking lemma](/forking-lemma/) with its loss. Brendel, Cremers, Jackson and Zhao (2021) gave the proofs for Ed25519 as standardized, and showed that the check $S < L$ is what makes it strongly unforgeable.
- **Strongly unforgeable with $S < L$.** Without that check, $S + L$ is a second valid encoding (some early implementations checked only the top three binary digits of $S$, which lets $S + L$ through). See [signature malleability](/signature-malleability/).
- **Deterministic.** The same key and message give the same signature. This removes the need for a random source, but a fault during signing can then leak the key: two runs on the same message where one challenge is faulty give $a$ by one division. See [deterministic nonce generation](/deterministic-nonce-generation/).
- **About 128 binary digits of security.** The best known attack is Pollard rho in a group of order about $2^{252}$, which takes about $2^{126}$ steps.

## Variants and improvements

- **Ed25519ctx and Ed25519ph** (RFC 8032): a domain separation prefix $\mathrm{dom2}$ with a context string, and a prehashed form that signs $\mathrm{SHA\text{-}512}(M)$ instead of $M$.
- **Ed448.** RFC 8032 Section 5.2 defines Ed448 on edwards448, the untwisted Edwards curve $x^2 + y^2 = 1 - 39081 x^2 y^2$ over $p = 2^{448} - 2^{224} - 1$ from Hamburg's Goldilocks curve. It uses SHAKE256 with 114 bytes of output and always hashes a $\mathrm{dom4}$ prefix with a flag and a context. Keys are 57 bytes, signatures 114 bytes, the cofactor is 4, and the security level is about 224 binary digits. The steps are the same as those of Ed25519. FIPS 186-5 approves both.
- **Hedged EdDSA**: add fresh randomness to the nonce hash to resist fault attacks; see [deterministic nonce generation](/deterministic-nonce-generation/).
- **Strict validation rules**: ZIP 215, and the rules of Chalkias, Garillot and Nikolaenko.
- **Ristretto255** builds a prime order group from the same curve, which removes the cofactor issues for new protocols.

## When to use it

Use Ed25519 for new designs that need a fast, small, deterministic signature: SSH keys, software signing, protocol messages and many blockchains. Use a reviewed library such as libsodium, and fix the validation rules (ZIP 215 or a strict set) when several parties must agree on validity. Use [ECDSA](/ecdsa/) instead where a standard or hardware requires a NIST curve, and [BLS](/bls-signature/) or Schnorr multisignatures when signatures must aggregate.

## Pitfalls

- **Different validation rules.** Two libraries can disagree on the same signature. In a replicated system, fix one rule set and test it with the cases of Chalkias, Garillot and Nikolaenko.
- **Not checking $S < L$.** This makes signatures malleable.
- **Signing with a mismatched public key.** An API that takes the public key as a separate argument from the secret key, and signs with a wrong one, leaks the secret: two signatures on one message with the same nonce $r$ but different $A$ give different challenges, and $a = (S_1 - S_2)/(k_1 - k_2) \bmod L$. Always derive $A$ from the secret key.
- **Faults.** A glitch in the computation of $k$ or $S$ on a device leaks $a$ from one faulty and one correct signature of the same message.
- **Treating the clamped scalar as uniform.** Protocols that derive child keys (such as hierarchical wallets) or that add keys must handle clamping and the cofactor with care.

## Implementations

The Python code on this page implements Ed25519 with its own field and curve arithmetic in extended coordinates and SHA-512 from hashlib, with a choice of the cofactored or cofactorless verification. The tests reproduce RFC 8032 Section 7.1 TEST 1, TEST 2 and TEST 3, copied by hand, check that $S + L$ is rejected, and build the order 8 key that splits the two verifiers. The code is for study only. It is not constant time, it branches on secret values, and it must not be used to protect real data.

## History

Edwards (2007) gave the normal form of the curves, and Bernstein and Lange made them practical for cryptography. Bernstein, Birkner, Joye, Lange and Peters (2008) introduced twisted Edwards curves, and Hisil, Wong, Carter and Dawson (2008) the extended coordinates. Curve25519 (Bernstein, 2006) was the key exchange curve. Bernstein, Duif, Lange, Schwabe and Yang presented Ed25519 at CHES 2011 and in the Journal of Cryptographic Engineering in 2012.

The CFRG work led to RFC 8032 by Josefsson and Liusvaara in 2017, with Ed448 on Hamburg's curve. NIST added EdDSA to FIPS 186-5 in 2023, with the curves in SP 800-186. The study of validation rules by Chalkias, Garillot and Nikolaenko and Zcash's ZIP 215 came in 2020, to make the set of valid signatures well defined for consensus.

## References
