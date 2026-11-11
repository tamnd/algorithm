---
tag: CGBNHK
kind: algorithm
slug: sha-2
name: SHA-2
aliases:
- SHA-256
- SHA-512
- Secure Hash Algorithm 2
area: cryptography/hash-functions
level: core
summary: The NIST hash family of FIPS 180-4, SHA-224 to SHA-512/256, on 32-bit or 64-bit words with 64 or 80 rounds. No attack on the full functions; it is the default hash today.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2001
  people: [National Security Agency, NIST]
  note: NIST published the draft of SHA-256, SHA-384 and SHA-512 in 2001 and FIPS 180-2 in 2002. SHA-224 came in 2004, and SHA-512/224 and SHA-512/256 in FIPS 180-4 (2012).
prereqs: [merkle-damgard-construction, davies-meyer-construction]
see_also: [sha-1, sha-3, hmac, length-extension-attack, collision-resistance, preimage-resistance, merkle-tree, proof-of-work]
sources:
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST, FIPS 180-4, Secure Hash Standard (SHS), August 2015
    locator: Sections 4.1.2 and 4.1.3 (the functions), 4.2.2 and 4.2.3 (the constants), 5.1 (padding), 5.3 (initial hash values, with 5.3.6 for SHA-512/t) and 6.2 to 6.7 (the hash computations)
  - url: "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values"
    title: NIST, Cryptographic Standards and Guidelines, Examples with Intermediate Values
    locator: SHA224.pdf, SHA256.pdf, SHA384.pdf, SHA512.pdf, SHA512_224.pdf and SHA512_256.pdf, the one-block and two-block messages
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, August 2015
    locator: Appendix A.1, Table 4 (security strengths of SHA-1, SHA-2 and SHA-3)
  - paper: "Florian Mendel, Tomislav Nad and Martin Schläffer, Improving local collisions: new attacks on reduced SHA-256, Advances in Cryptology, EUROCRYPT 2013, LNCS 7881, Springer, 2013"
    locator: a collision attack on 31 steps and a semi-free-start collision on 38 steps of SHA-256
  - url: "https://eprint.iacr.org/2024/349"
    title: Yingxin Li, Fukang Liu and Gaoli Wang, New records in collision attacks on SHA-2, EUROCRYPT 2024
    locator: the first practical semi-free-start collision of 39-step SHA-256, a practical free-start collision of 40-step SHA-224, and collision attacks on 28-step and 31-step SHA-512
---

SHA-2 is the family of [cryptographic hash functions](/cryptographic-hash-function/) in NIST FIPS 180-4: SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256. There are two cores. SHA-256 works on 32-bit words with 64 rounds and a 512-bit block. SHA-512 works on 64-bit words with 80 rounds and a 1024-bit block. The other four functions are one of the two cores with another initial value and a truncated output. Each is a [Merkle-Damgard](/merkle-damgard-construction/) hash over a [Davies-Meyer](/davies-meyer-construction/) compression function, like [SHA-1](/sha-1/), but with a non-linear message schedule and eight registers. No attack is known on any full SHA-2 function: the best collision attacks reach 31 of 64 steps of SHA-256 and 31 of 80 steps of SHA-512. SHA-256 is the default hash of TLS, code signing, Bitcoin and much more.

**Notation.** $w$ is the word size, 32 or 64. $+$ is addition modulo $2^w$, $\mathrm{ROTR}^s$ is right rotation and $\mathrm{SHR}^s$ right shift by $s$ bits. $(H_0, \ldots, H_7)$ is the chaining value and $a, \ldots, h$ the working registers. $W_t$ is the expanded block. $n$ is the message length in bytes.

## In plain words

SHA-2 follows the plan of SHA-1 with more care. The message is padded to whole blocks, with its length at the end. The state is eight numbers. For each block, the 16 words of the block are stretched to 64 or 80 words, and this time the stretch mixes the bits with rotations and shifts, not only XOR. Then each of 64 or 80 rounds builds two new values from the registers, a constant and one word, and puts them into two of the eight registers while the others move down one place. After the rounds, the old state is added back. The constants are not chosen by hand: they are the fractional parts of square roots and cube roots of the first prime numbers, so that nobody can hide a trap in them.

## The problem

The input is a message of $8n$ bits, with $8n < 2^{64}$ for SHA-224 and SHA-256 and $8n < 2^{128}$ for the others. The output has $d$ bits, $d \in \{224, 256, 384, 512\}$. The security goals are [collision resistance](/collision-resistance/) at $2^{d/2}$ and [preimage resistance](/preimage-resistance/) at $2^d$. FIPS 202, Table 4 lists the security strengths in bits:

| function | collision | preimage | second preimage |
|---|---|---|---|
| SHA-224 | 112 | 224 | min(224, 256 − L(M)) |
| SHA-512/224 | 112 | 224 | 224 |
| SHA-256 | 128 | 256 | 256 − L(M) |
| SHA-512/256 | 128 | 256 | 256 |
| SHA-384 | 192 | 384 | 384 |
| SHA-512 | 256 | 512 | 512 − L(M) |

Here $L(M) = \lceil \log_2(\text{the number of blocks of } M) \rceil$. The loss of $L(M)$ bits in the second preimage column is the long-message attack of Kelsey and Schneier on each Merkle-Damgard hash.

## The algorithm

The functions are $\mathrm{Ch}(x, y, z) = (x \wedge y) \oplus (\neg x \wedge z)$ and $\mathrm{Maj}(x, y, z) = (x \wedge y) \oplus (x \wedge z) \oplus (y \wedge z)$, and for $w = 32$:

- $\Sigma_0(x) = \mathrm{ROTR}^2(x) \oplus \mathrm{ROTR}^{13}(x) \oplus \mathrm{ROTR}^{22}(x)$, $\Sigma_1(x) = \mathrm{ROTR}^6(x) \oplus \mathrm{ROTR}^{11}(x) \oplus \mathrm{ROTR}^{25}(x)$,
- $\sigma_0(x) = \mathrm{ROTR}^7(x) \oplus \mathrm{ROTR}^{18}(x) \oplus \mathrm{SHR}^3(x)$, $\sigma_1(x) = \mathrm{ROTR}^{17}(x) \oplus \mathrm{ROTR}^{19}(x) \oplus \mathrm{SHR}^{10}(x)$.

For $w = 64$ the amounts are $(28, 34, 39)$, $(14, 18, 41)$, $(1, 8, 7)$ and $(19, 61, 6)$. The round constants $K_t$ are the first $w$ bits of the fractional parts of the cube roots of the first 64 primes ($w = 32$) or 80 primes ($w = 64$). The IV of SHA-256 is the first 32 bits of the fractional parts of the square roots of the first 8 primes, and the IV of SHA-512 is the first 64 bits of the same. SHA-384 uses the primes 23 to 53 (the 9th to 16th), and SHA-224 uses the second 32 bits of those 64-bit values. SHA-512/$t$ hashes the string "SHA-512/$t$" with the SHA-512 IV XOR `a5a5...a5` and uses the result as its IV (FIPS 180-4, Section 5.3.6).

```pseudo id=main
SHA-2(M, w, IV, d)                          ▷ w = 32: 64 rounds; w = 64: 80 rounds
L1  P ← M ‖ 1 ‖ 0^k ‖ [8n]_(2w)              ▷ |P| ≡ 0 mod 16w; length big-endian
L2  H ← IV
L3  for each 16w-bit block Y of P, in order, do
L4      H ← COMPRESS(H, Y)
L14 return the first d bits of H0 ‖ H1 ‖ … ‖ H7   ▷ big-endian words

COMPRESS(H, Y)
L5  W[0..15] ← the 16 big-endian words of Y
L6  for t ← 16 to R − 1 do                   ▷ R = 64 or 80
L7      W[t] ← σ1(W[t−2]) + W[t−7] + σ0(W[t−15]) + W[t−16]
L8  (a, b, c, d, e, f, g, h) ← (H0, …, H7)
L9  for t ← 0 to R − 1 do
L10     T1 ← h + Σ1(e) + Ch(e, f, g) + K[t] + W[t]
L11     T2 ← Σ0(a) + Maj(a, b, c)
L12     (a, b, c, d, e, f, g, h) ← (T1 + T2, a, b, c, d + T1, e, f, g)
L13 return (H0 + a, H1 + b, …, H7 + h)
```

The six functions differ only in $w$, $IV$ and $d$: SHA-256 is $(32, IV_{256}, 256)$, SHA-224 is $(32, IV_{224}, 224)$, SHA-512 is $(64, IV_{512}, 512)$, SHA-384 is $(64, IV_{384}, 384)$, and SHA-512/$t$ is $(64, IV_{512/t}, t)$. The code derives each constant and IV from the primes with integer roots and checks them against the values printed in FIPS 180-4.

## Example

Hash `abc` with SHA-256. The block has $W_0 = \texttt{61626380}$, $W_{15} = \texttt{00000018}$ and zeros between. The first constant is $K_0 = \lfloor 2^{32} \cdot \mathrm{frac}(2^{1/3}) \rfloor = \texttt{428A2F98}$, and the first IV word is $\lfloor 2^{32} \cdot \mathrm{frac}(2^{1/2}) \rfloor = \texttt{6A09E667}$. The registers after some rounds are:

| after $t$ | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | $h$ |
|---|---|---|---|---|---|---|---|---|
| 0 | `5d6aebcd` | `6a09e667` | `bb67ae85` | `3c6ef372` | `fa2a4622` | `510e527f` | `9b05688c` | `1f83d9ab` |
| 1 | `5a6ad9ad` | `5d6aebcd` | `6a09e667` | `bb67ae85` | `78ce7989` | `fa2a4622` | `510e527f` | `9b05688c` |
| 63 | `506e3058` | `d39a2165` | `04d24d6c` | `b85e2ce9` | `5ef50f24` | `fb121210` | `948d25b6` | `961f4894` |

The feed-forward gives the digest `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`. The NIST example SHA256.pdf lists the same rows. The other members give, for "abc":

| function | digest of "abc" |
|---|---|
| SHA-224 | `23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7` |
| SHA-384 | `cb00753f45a35e8bb5a03d699ac65007272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7` |
| SHA-512 | `ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f` |
| SHA-512/224 | `4634270f707b6a54daae7530460842e20e37ed265ceee9a43e8924aa` |
| SHA-512/256 | `53048e2681941ef99b2e29b76b4c7dabe4c2d0c634fc6d46e0e2f13107e7af23` |

The tests check these values and the two-block examples against the NIST example files, and check all six functions against `hashlib` at the lengths 55, 56, 111, 112 and 128 bytes, where the padding changes shape.

## Correctness

The padding is injective and gives whole blocks; the loop computes the Merkle-Damgard iteration; and each round of lines L10 to L12 is a bijection of the eight registers for fixed $W[t]$, since from the new state one reads $a, b, c, e, f, g$, then $T_2$, then $T_1 = a_{\text{new}} - T_2$, $d = e_{\text{new}} - T_1$ and $h$. So COMPRESS is $E_Y(H) + H$, the Davies-Meyer form (the cipher $E$ of SHA-256 is SHACAL-2). The truncated functions output a function of the final chaining value, so a collision of the truncated output is a collision of a $d$-bit function, and the generic bound is $2^{d/2}$. The full proof is below.

## Complexity

SHA-256 does 48 schedule words and 64 rounds per 64-byte block; SHA-512 does 64 schedule words and 80 rounds per 128-byte block. Each round costs about 7 additions and 2 $\Sigma$ functions of 3 rotations. The time is $\Theta(n)$ and the extra space $\Theta(1)$ (a 16-word ring for the schedule). On 64-bit processors without SHA instructions, SHA-512 is faster per byte than SHA-256, because each round handles twice the bits. With the SHA instructions of x86 and ARM, SHA-256 is fast.

## Properties

- Output: 224, 256, 384 or 512 bits. Block: 512 bits (SHA-224, SHA-256) or 1024 bits (the others).
- [Length extension](/length-extension-attack/) works on SHA-256 and SHA-512, whose output is the full chaining value. It fails on SHA-384 and SHA-512/256, which hide 128 or 256 bits of the state. SHA-224 hides only 32 bits, so an extension costs about $2^{32}$ guesses. SHA-512/224 hides 288 bits.
- Best published attacks (reduced rounds only): a collision of 31-step SHA-256 and a semi-free-start collision of 38-step SHA-256 (Mendel, Nad and Schläffer 2013); a practical semi-free-start collision of 39-step SHA-256 and collision attacks on 28-step and 31-step SHA-512 (Li, Liu and Wang 2024).
- [HMAC](/hmac/)-SHA-256 is a standard [message authentication code](/message-authentication-code/), and the length extension does not apply to it.

## Variants and improvements

- SHA-512/256 is the best SHA-2 choice for new designs on 64-bit machines: it is fast there and it resists length extension.
- [SHA-3](/sha-3/) is a different design, a [sponge](/sponge-construction/), standardized as a backup in case SHA-2 fails.
- Double SHA-256, $\text{SHA-256}(\text{SHA-256}(M))$, is the hash of Bitcoin; it also blocks length extension at the cost of a second call.
- [BLAKE2](/blake2/) and [BLAKE3](/blake3/) are faster in software with similar security claims.

## When to use it

Use SHA-256 or SHA-512/256 when a standard, a FIPS 140 module or a protocol asks for a hash, and use [HMAC](/hmac/) for a keyed hash. Do not use a plain $H(K \| M)$ as a MAC with SHA-256 or SHA-512. For a password, use a [password hashing](/password-hashing/) function, not SHA-2 alone.

## Pitfalls

- SHA-224 is not just SHA-256 cut to 224 bits: it has its own IV. The same holds for SHA-384 and SHA-512/$t$.
- The SHA-512 length field has 128 bits, not 64. Messages of 112 to 127 bytes need a second block.
- $\Sigma$ uses three rotations; $\sigma$ uses two rotations and a shift. A rotation in place of the shift gives a different function that passes no vector.
- The code on this page is for study only. It is not constant time, and it must not protect real data. Use `hashlib.sha256` or a FIPS 140 validated module.

## Implementations

## History

The NSA designed SHA-2. NIST published a draft with SHA-256, SHA-384 and SHA-512 in 2001 and FIPS 180-2 in August 2002. A change notice of 2004 added SHA-224, to match the 112-bit security of three-key Triple DES. FIPS 180-4 (March 2012) added SHA-512/224 and SHA-512/256, and its August 2015 revision changed the rules for where the padding may be computed. After the attacks on SHA-1 in 2005, NIST ran the SHA-3 competition from 2007 to 2012 to get a backup with a different structure. The attacks on SHA-2 have reached only reduced rounds.

## References
