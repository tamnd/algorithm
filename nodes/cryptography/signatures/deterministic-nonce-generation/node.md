---
tag: DR8QGH
kind: concept
slug: deterministic-nonce-generation
name: Deterministic nonce generation
aliases:
- RFC 6979
- deterministic ECDSA
- hedged signatures
area: cryptography/signatures
level: intro
summary: "Derive the per-signature nonce from the secret key and the message hash with HMAC (RFC 6979) or a hash (EdDSA), so signing needs no random source. Faults call for hedged nonces."
prereqs: [ecdsa, hmac]
see_also: [nonce-reuse-attack, ed25519, schnorr-signature, dsa, rsa-fault-attack, timing-attack]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc6979"
    title: Thomas Pornin, RFC 6979, Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA), August 2013
    locator: Section 2.3 (bits2int, int2octets, bits2octets), Section 3.2 (the generation of k, steps a to h), and Appendix A.2.5 (the P-256 values of k for "sample" and "test", copied in the tests)
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), 2017
    locator: Section 5.1.6, step 2, the nonce r = SHA-512(prefix || M)
  - url: "https://doi.org/10.6028/NIST.FIPS.186-5"
    title: NIST, FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: Section 6.3 (the per-message secret number of ECDSA, random or deterministic)
  - paper: doi:10.1109/FDTC.2017.12
    title: Yolan Romailler and Sylvain Pelissier, Practical fault attack against the Ed25519 and EdDSA signature schemes, Workshop on Fault Diagnosis and Tolerance in Cryptography (FDTC) 2017
    locator: the single fault during signing that, with a correct signature of the same message, gives the secret scalar
  - paper: doi:10.1109/EuroSP.2018.00031
    title: Damian Poddebniak, Juraj Somorovsky, Sebastian Schinzel, Manfred Lochter and Paul Rösler, Attacking deterministic signature schemes using fault attacks, IEEE EuroS&P 2018
    locator: the fault attacks on deterministic ECDSA and EdDSA in several libraries, with Rowhammer as the fault source, and the advice to add randomness
  - url: "https://datatracker.ietf.org/doc/draft-irtf-cfrg-det-sigs-with-noise/"
    title: John Preuß Mattsson, Erik Thormarker and Sini Ruohomaa, Hedged ECDSA and EdDSA Signatures, Internet-Draft draft-irtf-cfrg-det-sigs-with-noise-05, March 2025 (a draft, not an RFC)
    locator: the hedged nonce for ECDSA and EdDSA, which mixes fresh randomness into the deterministic nonce
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr Signatures for secp256k1, 2020
    locator: section Default Signing, the synthetic nonce from the key, the message and auxiliary random data
---

A signature scheme of the Schnorr or DSA family needs a nonce $k$ for each signature that is secret, never repeated for two messages, and uniform in $[1, q-1]$. A weak random generator breaks this, and the [nonce reuse attack](/nonce-reuse-attack/) then gives the secret key. Deterministic nonce generation computes $k$ from the secret key and the message hash with a pseudorandom function, so the signer needs no randomness at signing time. RFC 6979 does this with HMAC for [DSA](/dsa/) and [ECDSA](/ecdsa/), and [Ed25519](/ed25519/) does it with SHA-512. The verifier does not change. Deterministic signing is open to fault attacks, so newer designs add fresh randomness back as a hedge.

**Notation.** $x$ is the secret key, $q$ the prime group order, $\mathrm{qlen}$ its number of binary digits and $\mathrm{rlen} = \lceil \mathrm{qlen}/8 \rceil$ bytes. $H$ is a hash with output $h_1 = H(m)$ of $\mathrm{hlen}$ binary digits, and $\mathrm{HMAC}_K(\cdot)$ is [HMAC](/hmac/) with $H$ and key $K$.

## In plain words

Each signature needs a secret one-time number. If that number repeats for two messages, or if anyone can guess part of it, the secret key falls out. Random numbers from a computer can fail, for example on a device that has just started.

The fix is to compute the one-time number from the secret key and the message with a keyed hash. Nobody without the key can predict it, and two different messages get unrelated numbers. The same message always gets the same number, and so the same signature, which is harmless.

The cost is that a glitch during signing can now be exploited: a correct and a faulty signature of the same message share the one-time number. Adding a little fresh randomness to the keyed hash closes that hole.

## The idea

### RFC 6979

RFC 6979 runs HMAC-DRBG (the deterministic random bit generator of NIST SP 800-90A) seeded with the secret key and the reduced message hash, and takes the first output in $[1, q-1]$. The helper functions are: $\mathrm{bits2int}(b)$ reads $b$ as a big endian integer and keeps its leftmost $\mathrm{qlen}$ binary digits; $\mathrm{int2octets}(x)$ writes $x$ as $\mathrm{rlen}$ bytes; $\mathrm{bits2octets}(b) = \mathrm{int2octets}(\mathrm{bits2int}(b) \bmod q)$.

```pseudo id=main
NONCE(x, m)
L1  h1 ← H(m);  V ← 0x01 0x01 … 0x01 (hlen/8 bytes);  K ← 0x00 0x00 … 0x00 (hlen/8 bytes)
L2  K ← HMAC_K(V ‖ 0x00 ‖ int2octets(x) ‖ bits2octets(h1));  V ← HMAC_K(V)
L3  K ← HMAC_K(V ‖ 0x01 ‖ int2octets(x) ‖ bits2octets(h1));  V ← HMAC_K(V)
L4  loop
L5      T ← empty;  while len(T) < qlen do V ← HMAC_K(V);  T ← T ‖ V
L6      k ← bits2int(T)
L7      if 1 ≤ k ≤ q − 1 then return k
L8      K ← HMAC_K(V ‖ 0x00);  V ← HMAC_K(V)
```

These are steps a to h of RFC 6979 Section 3.2. The loop in L4 to L8 runs again only when the candidate is out of range, which for P-256 has probability about $2^{-32}$. If HMAC is a pseudorandom function, $k$ is indistinguishable from uniform for anyone who does not know $x$, and the nonces for different messages look independent. The signature itself does not change, so a verifier cannot tell RFC 6979 signatures from randomized ones.

### The EdDSA nonce

[Ed25519](/ed25519/) hashes the secret key once, $h = \mathrm{SHA\text{-}512}(sk)$, and keeps the upper 32 bytes as a secret prefix. The nonce for message $M$ is $r = \mathrm{SHA\text{-}512}(\mathrm{prefix} \| M) \bmod L$. The prefix is independent of the signing scalar, and the 512-binary-digit hash reduced mod $L$ of about 252 binary digits has a negligible bias. BIP 340 is similar but hashes the key, the public key and the message with a tag, and mixes in 32 bytes of auxiliary randomness when they are available.

### Fault attacks

A deterministic signer computes the same $k$ every time it signs $m$. Suppose a fault during one run changes the challenge: in a Schnorr-type scheme the signer outputs $s_1 = k + e_1 x$ and, in the faulty run, $s_2 = k + e_2 x$ with $e_2 \ne e_1$. If the attacker can compute $e_2$ (for example, the fault corrupts $R$ and the faulty $R$ is in the signature), then

$$x = (s_1 - s_2)/(e_1 - e_2) \bmod q.$$

For ECDSA a fault in the hash or in $r$ gives the same kind of linear system. Romailler and Pelissier (2017) did this to Ed25519 on a microcontroller with a single voltage glitch. Poddebniak, Somorovsky, Schinzel, Lochter and Rösler (2018) attacked deterministic ECDSA and EdDSA in several libraries, including with Rowhammer bit flips from software. With a random nonce the two runs use unrelated $k$, and the attack fails.

### Hedged signatures

A hedged nonce hashes the key, the message and fresh random bytes $Z$. If $Z$ is good, the scheme is as safe as a randomized one and resists faults; if $Z$ is bad or repeated, it is still as safe as the deterministic one. The Internet-Draft draft-irtf-cfrg-det-sigs-with-noise-05 by Preuß Mattsson, Thormarker and Ruohomaa (2025, a draft, not an RFC) specifies such nonces for ECDSA and EdDSA, and BIP 340's auxiliary randomness has the same aim. The draft has expired without becoming an RFC.

## Examples

**RFC 6979 on P-256.** Appendix A.2.5 uses the key $x$ = `C9AFA9D8...120F6721` and SHA-256.

| message | $k$ |
|---|---|
| "sample" | `A6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60` |
| "test" | `D16B6AE827F17175E040871A1C7EC3500192C4C92677336EC2537ACAEE0008E0` |

Here $\mathrm{hlen} = \mathrm{qlen} = 256$, so $\mathrm{bits2octets}(h_1)$ is $h_1 \bmod q$, and one HMAC output fills $T$. The code on this page reproduces both values with the standard library `hmac` and `hashlib`.

**A fault on a toy deterministic Schnorr signer.** Take the group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with generator 4, the key $x = 345$ and the message "pay 10 coins". RFC 6979 with this $q$ gives $k = 292$. The correct signature is $(R, s) = (639, 441)$ with $e_1 = 219$. A simulated fault flips the low binary digit of $R$ after it is computed, so the signer hashes and outputs $R' = 638$, gets $e_2 = 643$ and outputs $s_2 = 1004$ with the same $k$. Then $(441 - 1004)/(219 - 643) \bmod 1019 = 345$, the key. The hedged signer in the code draws new random bytes for each run, and the same fault gives nothing. The group is far too small to be secure, and the attack runs only against a local simulated signer.

## Where it is used

- **ECDSA and DSA.** libsecp256k1 and Bitcoin Core sign ECDSA with RFC 6979 nonces. FIPS 186-5 allows deterministic ECDSA. Many hardware wallets and libraries use it after the nonce failures of the PlayStation 3 (2010) and of Android's SecureRandom (2013).
- **EdDSA.** [Ed25519](/ed25519/) and Ed448 are deterministic by definition in RFC 8032.
- **Schnorr in Bitcoin.** BIP 340 derives the nonce from the key and message and recommends fresh auxiliary randomness, a hedged design.
- **Devices exposed to faults** such as smart cards and embedded signers, where hedged nonces or a check of the signature before output are advised.

The code on this page is for study only and is not constant time.

## References
