---
tag: 3KPV28
kind: definition
slug: signature-scheme
name: Signature scheme
aliases:
- signature triple (Gen, Sign, Verify)
- digital signature scheme
area: cryptography/signatures
level: intro
summary: "A triple of efficient algorithms (KeyGen, Sign, Verify) with a message space, such that honest signatures always verify. Schemes are stateless or stateful, deterministic or randomized."
prereqs: [digital-signature, public-key-cryptography]
see_also: [existential-unforgeability, strong-unforgeability, hash-and-sign-paradigm, lamport-signature, xmss, deterministic-nonce-generation, message-authentication-code, rsa-signature]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, the definition of a signature scheme and of its correctness, and the stateful schemes built from one-time signatures
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 6, the definition of signature schemes, including memory-dependent (stateful) schemes
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, Section 11.2, signature schemes with appendix and with message recovery, randomized and deterministic schemes
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: the formal model of a signature scheme, and a scheme whose signer keeps a state
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 13, Digital signatures
---

A signature scheme is the formal object behind a [digital signature](/digital-signature/): three efficient algorithms that generate a key pair, sign a message with the private key, and verify a signature with the public key. The definition fixes the inputs and outputs of each algorithm, the set of messages that can be signed, and the correctness condition that an honest signature always verifies. It says nothing yet about security; that is the job of [existential unforgeability](/existential-unforgeability/) and [strong unforgeability](/strong-unforgeability/).

**Notation.** $\lambda$ is the security parameter, given to algorithms in unary as $1^\lambda$. "Efficient" means probabilistic polynomial time in $\lambda$. $(pk, sk)$ is a key pair, $\mathcal{M}_{pk}$ the message space, $m$ a message and $\sigma$ a signature. $\mathrm{negl}(\lambda)$ is a negligible function, one that is smaller than $1/\lambda^c$ for every constant $c$ and all large $\lambda$. $H$ is a hash function. All statements here are syntax and correctness; no security model is involved.

## Definition

**Signature scheme.** A signature scheme $\Pi = (\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ consists of three efficient algorithms.

- $\mathrm{KeyGen}(1^\lambda)$ is randomized and outputs a key pair $(pk, sk)$. The public key $pk$ fixes the message space $\mathcal{M}_{pk}$.
- $\mathrm{Sign}(sk, m)$, for $m \in \mathcal{M}_{pk}$, outputs a signature $\sigma$. It may use random coins.
- $\mathrm{Verify}(pk, m, \sigma)$ is deterministic and outputs a bit $b \in \{0, 1\}$; $b = 1$ means "valid".

**Correctness.** Except with probability $\mathrm{negl}(\lambda)$ over the key pair $(pk, sk) \leftarrow \mathrm{KeyGen}(1^\lambda)$, for every $m \in \mathcal{M}_{pk}$,

$$\Pr\bigl[\mathrm{Verify}(pk, m, \mathrm{Sign}(sk, m)) = 1\bigr] = 1,$$

where the probability is over the coins of $\mathrm{Sign}$. Katz and Lindell (Chapter 13) allow the negligible set of bad key pairs; many schemes have perfect correctness, with no bad key pairs at all.

**Message space.** $\mathcal{M}_{pk}$ can be the set $\{0,1\}^\ell$ of strings of a fixed length $\ell$ (one-time schemes such as [Lamport](/lamport-signature/) sign $\ell$-bit strings), a group or a ring fixed by $pk$ (textbook [RSA](/rsa-signature/) signs elements of $\mathbb{Z}_N$), or $\{0,1\}^*$, all finite strings. The [hash-and-sign paradigm](/hash-and-sign-paradigm/) turns a scheme for a fixed space into one for $\{0,1\}^*$ by signing $H(m)$. A scheme that signs elements of $\mathbb{Z}_N$ directly is not a scheme for byte strings until an encoding is fixed, and the encoding is part of the scheme: PKCS #1 v1.5, [FDH](/rsa-fdh/) and [PSS](/rsa-pss/) are three encodings for the same RSA permutation.

**Stateful schemes.** In a stateful scheme the signer keeps a state that changes with each signature: $\mathrm{Sign}(sk_i, m) \to (\sigma, sk_{i+1})$, and correctness holds for each signature in the sequence. The state is often a counter that selects a fresh one-time key. Merkle signatures, [XMSS](/xmss/) and [LMS](/leighton-micali-signature/) are stateful. If the signer reuses a state, for example after it restores a backup of its key, it signs two messages with one one-time key, and the security proof no longer holds. A stateless scheme has $sk_{i+1} = sk_i$ for all $i$; RSA, [ECDSA](/ecdsa/), [Ed25519](/ed25519/) and [SPHINCS+](/sphincs-plus/) are stateless. Goldreich (Chapter 6) calls stateful schemes memory-dependent.

**Deterministic and randomized signing.** $\mathrm{Sign}$ is deterministic if it uses no coins, so that one message always gets the same signature. It is randomized otherwise. A randomized scheme can be made deterministic by deriving its coins from $sk$ and $m$ with a [pseudorandom function](/pseudorandom-function/); [deterministic nonce generation](/deterministic-nonce-generation/) (RFC 6979) does this for DSA and ECDSA, and Ed25519 does it by design.

**Unique signatures.** A scheme has unique signatures if for each $pk$ and $m$ at most one $\sigma$ satisfies $\mathrm{Verify}(pk, m, \sigma) = 1$. Unique implies that honest signing is deterministic, but the converse is false: Ed25519 signs deterministically, yet a signer that picks another nonce produces a different valid signature on the same message.

**Appendix and message recovery.** In a scheme with appendix, $\mathrm{Verify}$ takes $m$ as input, as above. In a scheme with message recovery, $\mathrm{Verify}(pk, \sigma)$ returns $m$ or a symbol for "invalid", so the message need not be sent separately (HAC, Section 11.2). PSS-R and ISO/IEC 9796 are examples.

## Examples and non-examples

| scheme | message space | signing | state | public key | signature |
|---|---|---|---|---|---|
| [RSA](/rsa-signature/) PKCS #1 v1.5, 2048-bit $N$ | byte strings | deterministic | stateless | 256 bytes plus $e$ | 256 bytes |
| [RSA-PSS](/rsa-pss/), 2048-bit $N$ | byte strings | randomized (salt) | stateless | 256 bytes plus $e$ | 256 bytes |
| [DSA](/dsa/), $(L, N) = (2048, 256)$ | byte strings | randomized (nonce $k$) | stateless | 256 bytes plus the domain parameters | 64 bytes ($r$, $s$) |
| [Ed25519](/ed25519/) | byte strings | deterministic | stateless | 32 bytes | 64 bytes |
| [Lamport](/lamport-signature/), 256-bit hash values | strings of 256 bits | deterministic | one signature per key | $2 \cdot 256 \cdot 32 = 16384$ bytes | $256 \cdot 32 = 8192$ bytes |
| [XMSS](/xmss/), height 10, SHA-256 | byte strings | deterministic | stateful, $2^{10}$ signatures | 68 bytes (with a 4-byte type code) | 2500 bytes |

- **Non-example: a MAC.** A [message authentication code](/message-authentication-code/) has $\mathrm{Gen}$, $\mathrm{Mac}$ and $\mathrm{Vrfy}$, but $\mathrm{Vrfy}$ needs the secret key. It is not a signature scheme, because there is no public key.
- **Non-example: a scheme with a high error rate.** If $\mathrm{Verify}$ rejects an honest signature with probability $1/2$, the triple is not a signature scheme in the sense above, even if it is hard to forge. Some lattice schemes reach correctness by repeating the signing attempt until the result passes a test, so that the output always verifies.
- **Correct but insecure.** The triple $\mathrm{KeyGen}$ = RSA key generation, $\mathrm{Sign}(sk, m) = m^d \bmod N$, $\mathrm{Verify}(pk, m, s) = [s^e \bmod N = m]$ on $\mathcal{M}_{pk} = \mathbb{Z}_N$ is a correct signature scheme, because $(m^d)^e \equiv m \pmod N$. It is not unforgeable: see the [key-only attack](/key-only-attack/). Correctness and security are separate conditions.
- **Correct and trivially insecure.** $\mathrm{Sign}(sk, m) = 0$ and $\mathrm{Verify}$ always returns 1 is correct. It shows why the definition of a scheme needs a separate security notion.

## Related definitions

- **[Existential unforgeability](/existential-unforgeability/) (EUF-CMA).** The standard security notion: no efficient adversary with a signing oracle produces a valid signature on a message it did not query.
- **[Strong unforgeability](/strong-unforgeability/) (SUF-CMA).** The adversary also must not produce a new signature on a queried message.
- **One-time signature.** A scheme that is secure only if each key signs at most one message, such as [Lamport](/lamport-signature/) and [Winternitz](/winternitz-one-time-signature/). A [Merkle tree](/merkle-tree/) of one-time keys gives a stateful many-time scheme ([Merkle signature scheme](/merkle-signature-scheme/)).
- **[Message authentication code](/message-authentication-code/).** The symmetric-key analogue, with the same unforgeability games.
- **[Public-key encryption](/public-key-encryption/).** The other primitive of [public-key cryptography](/public-key-cryptography/). Signing is not "encryption with the private key": for RSA the two use different paddings, and for discrete logarithm schemes there is no such reading at all.

## References
