---
tag: 4WMP39
kind: algorithm
slug: lamport-signature
name: Lamport one-time signature
aliases:
- Lamport signature
- Lamport signatures
- Lamport-Diffie
- Lamport-Diffie one-time signature
- LD-OTS
area: cryptography/signatures
level: intro
summary: "One-time signature from a one-way function. The secret key is 2n random values and a signature reveals one value per digest bit. Two signatures with one key allow forgeries."
model: word-ram
complexity:
  vars: {n: the digest length and the hash length}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
history:
  year: 1979
  people: [Leslie Lamport]
  note: SRI International technical report CSL-98, Constructing digital signatures from a one-way function, October 1979.
prereqs: [hash-based-signatures, one-way-function, signature-scheme]
see_also: [winternitz-one-time-signature, merkle-signature-scheme, hash-chain, preimage-resistance, collision-resistance, existential-unforgeability, xmss, sphincs-plus]
sources:
  - paper: "Leslie Lamport, Constructing digital signatures from a one-way function, Technical Report CSL-98, SRI International, October 1979"
    locator: the scheme with two secret values for each bit, one of them revealed by the signature
  - paper: "Ralph C. Merkle, A certified digital signature, CRYPTO 1989, LNCS 435, Springer, 1990, pages 218 to 238"
    locator: the improvements of one-time signatures (the hashed public key, the count of zero bits, and the method that Merkle credits to Winternitz)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: chapter Hash-based Digital Signature Schemes by Johannes Buchmann, Erik Dahmen and Michael Szydlo, section on the Lamport-Diffie one-time signature scheme (LD-OTS)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 13 (digital signature schemes), the section on signatures from hash functions, Lamport's one-time signature and its proof from a one-way function
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 14 (fast hash-based signatures), Lamport signatures and one-time security
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.6 (one-time digital signatures)
---

The Lamport one-time signature signs a message with nothing but a [one-way function](/one-way-function/), such as a hash function. The secret key is $2n$ random values, two for each bit of an $n$-bit message digest, and the public key is their hashes. To sign, the signer reveals one value of each pair, chosen by the digest bit. One key pair may sign only one message: two signatures with the same key reveal both values at many positions, and an attacker can then sign other messages. The scheme is the base of all [hash-based signatures](/hash-based-signatures/), which stay secure against quantum computers.

**Notation.** $H$ is the hash function (SHA-256 in the code), $n$ is the digest length in bits, and $\ell$ is the length of a secret value and of a hash value ($n = \ell = 256$ in practice, about $\lambda$ for security parameter $\lambda$). $D(m) = d_1 \ldots d_n$ is the digest of the message $m$. The secret key is $x_{i,b}$ and the public key is $y_{i,b} = H(x_{i,b})$, for $i \in [n]$ and $b \in \{0, 1\}$. The security notion is one-time existential unforgeability under chosen message attack (EUF-1-CMA): the adversary $A$ may see one signature on a message of its choice. The proof is in the standard model.

## In plain words

Make a table with two rows and 256 columns. Fill each cell with a random secret number. Hash each cell, and publish the table of hashes. That is the public key.

To sign, hash the message to get 256 bits. For each column, if the bit is 0, show the secret from the top row, and if it is 1, show the secret from the bottom row. Anyone can hash what you show and compare it with the published table.

A forger who wants to sign another message needs a secret that you did not show, in at least one column. To get it, the forger must undo a hash, which is not possible.

If you sign a second message, you show many cells from both rows. A forger can then mix the two signatures and sign a third message. So each key signs only once.

## The problem

The scheme is a [signature scheme](/signature-scheme/) in the narrow sense of a one-time signature: it has key generation, signing and verification, an honest signature verifies, and no efficient adversary that sees *one* signature on a message of its choice can make a valid signature on another message. It uses only a one-way function $H$ for the key values, and a [collision resistant](/collision-resistance/) hash for the message digest. It is not a signature scheme for many messages. To sign many messages, a [Merkle signature scheme](/merkle-signature-scheme/) puts many one-time keys under one public key.

## The algorithm

```pseudo id=main
KEYGEN(n)
L1  for i ← 1 to n, for b ∈ {0, 1}: x[i][b] ← random value of ℓ bits
L2  for i ← 1 to n, for b ∈ {0, 1}: y[i][b] ← H(x[i][b])
L3  return sk = x, pk = y

SIGN(x, m)
L4  d ← D(m)                                     ▷ n digest bits d[1..n]
L5  return σ = (x[1][d[1]], x[2][d[2]], …, x[n][d[n]])

VERIFY(y, m, σ)
L6  if σ does not have n values of ℓ bits then return false
L7  d ← D(m)
L8  for i ← 1 to n do
L9      if H(σ[i]) ≠ y[i][d[i]] then return false
L10 return true
```

Lines L1 and L2 make $n$ pairs of secret values and their images. Line L4 hashes the message, and line L5 picks, for each position $i$, the value of the pair that the bit $d_i$ selects. The signer computes no hash beyond the digest. The verifier recomputes the digest in line L7 and hashes each revealed value in line L9. It accepts only if each hash equals the public value for that bit.

The code takes $D(m)$ as the first $n$ bits of SHA-256$(m)$, so $n = 256$ in normal use, and a smaller $n$ gives a toy version for the attack below.

## Example

Take a toy digest of $n = 4$ bits, the first 4 bits of SHA-256, and keys made with a fixed seed. The values are shown by their first 4 bytes.

| $i$ | $x_{i,0}$ | $x_{i,1}$ | $y_{i,0} = H(x_{i,0})$ | $y_{i,1} = H(x_{i,1})$ |
|---|---|---|---|---|
| 1 | `f5b16522` | `7bd5d47e` | `42e6ba1d` | `a2b7b75d` |
| 2 | `8c2e0718` | `85c924c3` | `6a793ae1` | `cf8e9ad0` |
| 3 | `3129903a` | `b99e8306` | `eee397d9` | `abe21bc9` |
| 4 | `df0e7337` | `a0661970` | `707e0e21` | `7f6908aa` |

SHA-256 of the message "hi" starts with the hex digit `8`, so $D(\text{hi}) = 1000$. The signature is $(x_{1,1}, x_{2,0}, x_{3,0}, x_{4,0}) = $ (`7bd5d47e`, `8c2e0718`, `3129903a`, `df0e7337`). The verifier hashes the first value and compares it with $y_{1,1}$ = `a2b7b75d`, and so on for each position.

Now the signer makes a mistake and also signs "yo", with $D(\text{yo}) = 1110$. The signature reveals $x_{1,1}, x_{2,1}, x_{3,1}, x_{4,0}$. After the two signatures, the attacker knows both values at positions 2 and 3, and only $x_{1,1}$ and $x_{4,0}$ at positions 1 and 4. The two digests agree at $e = 2$ positions, so the attacker can sign each message whose digest has the form $1{*}{*}0$: 4 of the 16 digests, a fraction $2^{-e} = 1/4$. The message "so" has $D(\text{so}) = 1010$, so the attacker signs it with $(x_{1,1}, x_{2,0}, x_{3,1}, x_{4,0})$, and the verifier accepts.

## Correctness

**Correctness.** An honest signature verifies, because line L9 compares $H(x_{i,d_i})$ with $y_{i,d_i} = H(x_{i,d_i})$ for each $i$.

**One-time security.** Let $A$ run in time $t$ and win the EUF-1-CMA game with chance $\varepsilon$. Then there is an inverter of $H$ on the key values, and a collision finder for $D$, both of running time about $t$, with

$$\varepsilon \le 2n \cdot \mathrm{Adv}^{\mathrm{OW}}_H + \mathrm{Adv}^{\mathrm{CR}}_D.$$

The inverter plants its challenge $Y$ at a random one of the $2n$ public positions. A forgery on a new digest uses at least one value that the one signature did not reveal, and that value is at the planted position with chance at least $1/(2n)$. So the reduction loses a factor $2n$, independent of $t$. Both proofs are below.

### Why one key signs one message

After signatures on $m_1$ and $m_2$, the attacker knows both values at each position where $D(m_1)$ and $D(m_2)$ differ. Let $e$ be the number of positions where they agree. A random message $m^*$ is forgeable exactly when $D(m^*)$ agrees with them at those $e$ positions, which has chance $2^{-e}$. For random digests, $e$ is binomial with mean $n/2$, and the average chance is $(3/4)^n$. More generally, after $k$ signatures with one key, a random message is forgeable with chance $(1 - 2^{-k})^n$ on average.

| digest length $n$ | signatures $k$ | chance that a random message is forgeable |
|---|---|---|
| 16 | 2 | $(3/4)^{16} \approx 1.0 \cdot 10^{-2}$ |
| 256 | 2 | $(3/4)^{256} \approx 2^{-106.2}$ |
| 256 | 5 | $(31/32)^{256} \approx 2^{-11.7}$ |
| 256 | 8 | $(255/256)^{256} \approx 0.37$ |

With two signatures and $n = 256$, a forgery by random search is still out of reach, but the proof no longer holds, and an attacker who can choose the messages does better. With a handful of signatures, forgeries are cheap. The test file builds the attack on a toy digest of 16 bits:

```python
rev = [{} for _ in range(n)]           # revealed halves per position
for msg, sig in signed:                 # two signatures with one key
    d = digest_bits(msg, n)
    for i in range(n):
        rev[i][d[i]] = sig[i]
for i in range(1 << 16):                # search for a covered digest
    d = digest_bits(b"pay Eve %d" % i, n)
    if all(d[j] in rev[j] for j in range(n)):
        forged = [rev[j][d[j]] for j in range(n)]
        break
```

## Complexity

Count calls of $H$ on inputs of $\ell$ bits, plus the one hash of the message.

- KEYGEN makes $2n$ random values and $2n$ calls of $H$.
- SIGN makes one call of $D$ and no other hash. It copies $n$ values.
- VERIFY makes one call of $D$ and $n$ calls of $H$.

So the time of each operation is $\Theta(n)$ hash calls. The sizes are:

| object | size | for $n = \ell = 256$ |
|---|---|---|
| secret key | $2n\ell$ bits | 16 KiB (or a 32-byte seed) |
| public key | $2n\ell$ bits | 16 KiB |
| signature | $n\ell$ bits | 8 KiB |

So keys and signatures are about $n^2$ bits. Two standard changes shrink them. The secret values can come from one short seed through a pseudorandom function, so the secret key is one seed. The public key can be one hash of all $2n$ values $y_{i,b}$ (Merkle 1989); then a signature must also carry the $n$ values $y_{i, 1 - d_i}$ that the verifier cannot compute, so it grows to $2n\ell$ bits, and the public key is $\ell$ bits.

## Properties

- **One-time.** A key may sign one message. The security proof uses exactly one signing query.
- **Deterministic signing.** The signature depends only on the key and the message.
- **Minimal assumption.** Security needs only a one-way function for the key values and a collision resistant (or, with a random prefix, a weaker) hash for the digest. No number theory is used, so Shor's algorithm does not apply. Grover's algorithm speeds up the search for a preimage, so the hash length must be about twice the classical security level.
- **Fast signing.** Signing is a table lookup. Verification is $n$ hashes.

## Variants and improvements

- **Hashed public key.** Publish $H$ of all $2n$ public values (Merkle 1989). The public key becomes one hash value, and the signature carries the $n$ missing public values.
- **Merkle's count of zeros.** Reveal a secret value only for the bits that are 1, and sign the count of the zero bits in the same way. A forger can hide a revealed value and so turn a 1 into a 0, but then the count of zeros grows, and the signed count can only shrink. This needs about $n + \lg n$ secret values instead of $2n$.
- **[Winternitz one-time signature](/winternitz-one-time-signature/).** Sign $w$ bits at a time with a [hash chain](/hash-chain/) of length $2^w$, and add a checksum. The signature shrinks by a factor of about $w$, and the hash work grows by a factor of about $2^w / w$.
- **Few-time signatures.** HORS and the FORS of [SPHINCS+](/sphincs-plus/) reveal a few values out of a large set, so a key can sign a small number of messages with a slowly falling security.
- **Many messages.** A [Merkle signature scheme](/merkle-signature-scheme/) authenticates $2^h$ one-time public keys with one Merkle tree root.

## When to use it

Use the Lamport scheme to learn how hash-based signatures work, or inside a larger scheme where each key is used once by construction. In practice the Winternitz form replaces it, because its signatures are several times shorter. For a real system, use a standard: [LMS](/leighton-micali-signature/) or [XMSS](/xmss/) (NIST SP 800-208) when the signer can keep a reliable state, or SLH-DSA ([SPHINCS+](/sphincs-plus/), FIPS 205) when it cannot.

## Pitfalls

- **Two messages with one key.** This is the main failure. The signer must record that a key is used before it releases the signature, and must never sign again with it, also after a crash or a restore from a backup. The code has a `OneTimeSigner` that forgets the key after the first signature.
- **Signing the message bits, not a digest.** Line L4 must hash the message. Signing the raw bits of a long message needs a key as long as the message, and a short message padded with zeros lets an attacker sign related messages.
- **No length check in line L6.** A verifier that accepts a shorter signature, or that loops over the signature instead of over the public key, may accept a forgery with fewer values.
- **Weak randomness in line L1.** If the secret values come from a weak generator, an attacker can guess them. Derive them from a uniform seed with a pseudorandom function.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. For real use, take LMS or XMSS (NIST SP 800-208) or SLH-DSA (FIPS 205) from a FIPS 140 validated module or a reviewed library. The page is about the signature and not about the hash, so the code takes SHA-256 from `hashlib`. No standard defines the Lamport scheme, so there are no official test vectors; the tests check the round trip, the rejection of changed messages and signatures, the sizes, and the key reuse attack on a toy digest of 16 bits.

## History

Leslie Lamport described the scheme in an SRI International technical report in October 1979. Ralph Merkle studied one-time signatures in his 1979 thesis and in his 1989 paper "A certified digital signature", where he reduced the key size with the hashed public key and the count of zeros, gave the hash chain method that he credits to Robert Winternitz, and put many one-time keys under a tree. The scheme is called the Lamport-Diffie one-time signature (LD-OTS) in the post-quantum literature. Its descendants, LMS and XMSS (standardized in RFC 8554, RFC 8391 and NIST SP 800-208) and SLH-DSA (FIPS 205, 2024), are in use today.

## References
