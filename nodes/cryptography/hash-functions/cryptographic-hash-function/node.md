---
tag: HVMPK2
kind: definition
slug: cryptographic-hash-function
name: Cryptographic hash function
aliases:
- secure hash function
area: cryptography/hash-functions
level: intro
summary: An efficient function from inputs of any length to an n-bit digest for which preimages, second preimages and collisions are hard to find. SHA-256 and SHA-3 are standard examples.
prereqs: [hash-function]
see_also: [collision-resistance, preimage-resistance, second-preimage-resistance, random-oracle-model, merkle-damgard-construction, sponge-construction, hmac, password-hashing]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: Chapter 6 (hash functions as keyed families, collision resistance, the Merkle-Damgard transform, HMAC, and applications)
  - paper: "Phillip Rogaway and Thomas Shrimpton, Cryptographic hash-function basics: definitions, implications, and separations for preimage resistance, second-preimage resistance, and collision resistance, FSE 2004, LNCS 3017, pages 371 to 388"
    locator: Section 3 (the seven notions) and Figure 1 (the implications and separations among them)
  - paper: "Phillip Rogaway, Formalizing human ignorance: collision-resistant hashing without the keys, VIETCRYPT 2006, LNCS 4341, pages 211 to 228"
    locator: Section 1 (why a fixed hash cannot be collision resistant in the usual sense) and the explicit-reduction approach
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST FIPS 180-4, Secure Hash Standard (SHS), 2015
    locator: Sections 1 and 6 (SHA-1 and the SHA-2 family)
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST FIPS 202, SHA-3 Standard, 2015
    locator: Sections 4 to 6 (the sponge, Keccak and the SHA-3 and SHAKE functions)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9 (hash functions and data integrity), Section 9.2 (classification and properties)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography
    locator: Chapter 8 (message integrity from collision resistant hashing)
---

A cryptographic hash function maps an input of any length to a short digest of fixed length $n$, such as 256 bits, so that it is easy to compute but hard to attack. The three classic security properties are [preimage resistance](/preimage-resistance/) (a digest cannot be inverted), [second-preimage resistance](/second-preimage-resistance/) (a given message cannot be matched by another) and [collision resistance](/collision-resistance/) (no two messages with one digest can be found). For a random function, their generic costs are $2^n$, $2^n$ and $2^{n/2}$. A plain [hash function](/hash-function/) for hash tables needs only to spread keys well; a cryptographic one must hold up against an adversary who knows the function. SHA-256, SHA-512, SHA-3 and BLAKE2 are in use today. MD5 and SHA-1 are broken for collisions. Hashes are used in signatures, commitments, message authentication codes, key derivation, password storage and Merkle trees.

## Definition

**Syntax.** A hash function is a deterministic, efficiently computable map $H : \{0,1\}^{\le N} \to \{0,1\}^n$, where $N$ is a large maximum length (for SHA-256, $2^{64} - 1$ bits). It compresses: its inputs are far more numerous than its outputs, so collisions exist.

**Security.** For messages of $m > n$ bits, $H$ should satisfy:

| Property | The adversary gets | It must find | Generic cost |
|---|---|---|---|
| preimage resistance | $H(M)$ for a random $M$ | any $M'$ with $H(M') = H(M)$ | $2^n$ |
| second-preimage resistance | a random $M$ | $M' \ne M$ with $H(M') = H(M)$ | $2^n$, less for long $M$ in Merkle-Damgard hashes |
| collision resistance | nothing | $M \ne M'$ with $H(M) = H(M')$ | $2^{n/2}$, by the [birthday attack](/birthday-attack/) |

**The hierarchy.** Collision resistance implies second-preimage resistance, and second-preimage resistance implies preimage resistance when $H$ compresses enough, with a loss of $2^{n-m}$ (Rogaway and Shrimpton 2004). None of the reverse directions hold. So collision resistance is the strongest of the three, and the hardest to achieve: SHA-1 still has no practical preimage attack, but it has practical collisions.

**Keyed families and unkeyed functions.** Katz and Lindell define a hash function as a keyed family: a key generation algorithm outputs a public key $s$, and the function is $H^s$. The key is not secret. It only picks a function from the family after the adversary is fixed, so that no adversary has a collision built in. Real hashes such as SHA-256 have no key, and for any fixed function an adversary that prints a known collision exists, even if nobody knows it. Rogaway (2006) resolves this with explicit reductions: a proof shows how to turn any attack on a scheme into a collision of $H$, so the scheme is secure as long as nobody can find such a collision. This is the "human ignorance" approach, and it lets proofs speak about SHA-256 itself.

**Secret-key objects are different.** A message authentication code such as [HMAC](/hmac/) or KMAC uses a hash with a secret key, and its goal is unforgeability or pseudorandomness. That key plays another role than the public key of a keyed hash family.

**Beyond the three properties.** Many uses need more: that $H$ behave like a random function ([random oracle model](/random-oracle-model/)), that it resist [length extension](/length-extension-attack/), that it be a pseudorandom function when keyed, or that small input changes spread to the whole output ([avalanche effect](/avalanche-effect/)). The indifferentiability framework defines when a construction behaves like a random oracle.

## Examples and non-examples

- **SHA-2.** SHA-256 and SHA-512 (FIPS 180-4) are [Merkle-Damgard](/merkle-damgard-construction/) hashes with Davies-Meyer compression functions. No attack on the full functions is known, but plain SHA-256 allows length extension.
- **SHA-3.** SHA3-256 and SHAKE (FIPS 202) are [sponges](/sponge-construction/) on the Keccak permutation. They resist length extension.
- **BLAKE2 and BLAKE3.** Fast hashes with a finalization flag, widely used in software.
- **MD5 and SHA-1.** Once standard, now broken for collisions: MD5 in seconds, SHA-1 at about $2^{63}$ calls, including [chosen-prefix collisions](/chosen-prefix-collision/). Do not use them where an attacker may choose input.
- **CRC-32 and other checksums.** Linear and short. They detect accidental errors but resist no attack.
- **Hash table functions.** MurmurHash, FNV and similar functions spread keys well and are fast, but they are not cryptographic. Keyed functions such as SipHash defend tables against crafted inputs, but they are PRFs with a secret key, not public hash functions.
- **A plain hash for passwords.** SHA-256 of a password is a cryptographic hash used wrongly: it is too fast, and with no salt it falls to precomputed tables. [Password hashing](/password-hashing/) needs salted, slow, memory-hard functions such as Argon2.

## Related definitions

**Uses, and the property each needs.**

| Use | What it needs |
|---|---|
| hash-then-sign signatures | collision resistance, or second-preimage resistance with randomized hashing |
| commitments $H(r \,\|\, m)$ | collision resistance for binding, and a random oracle style property for hiding |
| message authentication (HMAC, KMAC) | a pseudorandom compression function or permutation |
| key derivation (HKDF, the SHAKE functions) | pseudorandomness, often argued in the random oracle model |
| password storage | preimage resistance plus slowness and salts |
| Merkle trees and content addressing | collision resistance, with domain separation of leaves and inner nodes |
| proof of work | partial preimages being uniformly hard |

**A map of the pages on attacks and models.**

- The properties: [collision resistance](/collision-resistance/), [second-preimage resistance](/second-preimage-resistance/), [preimage resistance](/preimage-resistance/).
- The problems of breaking them: [collision finding](/collision-finding/), [second-preimage finding](/second-preimage-finding/), [preimage finding](/preimage-finding/).
- Generic collision attacks: the [birthday attack](/birthday-attack/), [Pollard rho collision search](/pollard-rho-collision-search/), the [generalized birthday problem](/generalized-birthday-problem/) and [Wagner's algorithm](/wagners-algorithm/).
- Attacks on iterated hashes: [multicollisions](/multicollision-attack/), [length extension](/length-extension-attack/), [chosen-prefix collisions](/chosen-prefix-collision/).
- Inverting a fixed function many times: the [time-memory tradeoff](/time-memory-tradeoff/), [Hellman's tables](/hellman-time-memory-tradeoff/) and [rainbow tables](/rainbow-table/).
- Models and heuristics: the [random oracle model](/random-oracle-model/) and the [avalanche effect](/avalanche-effect/).
- Constructions: [Merkle-Damgard](/merkle-damgard-construction/), [sponge](/sponge-construction/), [HMAC](/hmac/), and the standards [SHA-2](/sha-2/), [SHA-3](/sha-3/) and [BLAKE2](/blake2/).

## References
