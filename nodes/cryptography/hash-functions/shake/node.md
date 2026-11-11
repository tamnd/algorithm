---
tag: WR6HQ2
kind: algorithm
slug: shake
name: SHAKE
aliases:
- SHAKE128
- SHAKE256
area: cryptography/hash-functions
level: advanced
summary: The FIPS 202 extendable-output functions SHAKE128 and SHAKE256, the Keccak sponge with capacity 256 or 512 and the suffix 1111. Collision security is min(d/2, c/2) for d output bits.
model: word-ram
complexity:
  vars: {n: the message length in bytes, ℓ: the output length in bytes}
  time: {worst: Θ(n + ℓ), average: Θ(n + ℓ), best: Θ(n + ℓ)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche]
  note: NIST standardized SHAKE128 and SHAKE256 in FIPS 202 (August 2015) as the first standard extendable-output functions, next to the four SHA-3 hash functions.
prereqs: [sha-3, extendable-output-function]
see_also: [keccak, sponge-construction, kmac, hkdf, pseudorandom-generator, random-oracle-model, blake3, sha-2]
sources:
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 6.2 (SHAKE128 and SHAKE256), Section 6.3 (the suffix 1111 and RawSHAKE), Appendix A.1 (Table 4, security strengths), Appendix A.2 (related outputs) and Appendix B.2 (the padding byte 1F)
  - url: "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values"
    title: NIST, Cryptographic standards and guidelines, example values for SHA-3
    locator: SHAKE128 and SHAKE256 with 4096 output bits, for the empty message and for the 1600-bit message of bytes A3
  - paper: doi:10.6028/NIST.SP.800-185
    title: NIST, SP 800-185, SHA-3 Derived Functions, cSHAKE, KMAC, TupleHash and ParallelHash, December 2016
    locator: Section 3 (cSHAKE, with the suffix 00, built on Keccak[256] and Keccak[512])
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: the sponge is indifferentiable from a random oracle with an infinite output up to about 2^(c/2) queries
  - paper: doi:10.17487/RFC8032
    title: Simon Josefsson and Ilari Liusvaara, Edwards-Curve Digital Signature Algorithm (EdDSA), RFC 8032, 2017
    locator: Section 5.2, Ed448 uses SHAKE256 with 114 bytes of output
---

SHAKE128 and SHAKE256 are the two extendable-output functions of FIPS 202, the SHA-3 standard. Each takes a message and an output length $d$ and returns $d$ bits, and a shorter output is always a prefix of a longer one. Each is the [sponge](/sponge-construction/) over Keccak-f[1600], like [SHA-3](/sha-3/), but with the suffix bits 1111 in place of 01 and a capacity that depends on the security level, not on the output length: $\mathrm{SHAKE128}(M, d) = \mathrm{KECCAK}[256](M \| 1111, d)$ and $\mathrm{SHAKE256}(M, d) = \mathrm{KECCAK}[512](M \| 1111, d)$. The number in the name is the security strength $c/2$. For $d$ output bits, collisions cost about $2^{\min(d/2,\, c/2)}$ (FIPS 202 Table 4). SHAKE is used for seed expansion in the post-quantum standards, for Ed448 and as the base of cSHAKE and [KMAC](/kmac/).

**Notation.** $c$ is the capacity in bits, 256 for SHAKE128 and 512 for SHAKE256. $r = 200 - c/8$ is the rate in bytes, 168 and 136. $n$ is the message length and $\ell = d/8$ the output length, both in bytes. KECCAK-F is Keccak-f[1600] on 25 lanes of 64 bits, as on the [Keccak](/keccak/) page, with bytes in lanes in little-endian order.

## In plain words

SHAKE is SHA-3 with an output tap that you can leave open. It absorbs the message into a 200-byte state block by block, as SHA-3 does. Then it reads out the first $r$ bytes of the state. If you want more, it scrambles the state again with Keccak-f and reads $r$ more bytes, and so on, for as long as you like. You can read in pieces of any size. Because each byte of output depends only on the message and its position, asking for 16 bytes gives exactly the first 16 bytes of what you would get if you asked for 1000. The number 128 or 256 is the security you get, as long as you ask for enough output.

## The problem

The input is a message $M$ of $n$ bytes and an output length $\ell$. The output is the first $\ell$ bytes of one infinite string that depends only on $M$. It should behave like a random oracle with infinite output up to the strength $c/2$. FIPS 202 Table 4 gives, for $d = 8\ell$ output bits:

| Function | $c$ | Rate $r$ (bytes) | Collision | Preimage | Second preimage |
|---|---|---|---|---|---|
| SHAKE128 | 256 | 168 | $\min(d/2, 128)$ | $\ge \min(d, 128)$ | $\min(d, 128)$ |
| SHAKE256 | 512 | 136 | $\min(d/2, 256)$ | $\ge \min(d, 256)$ | $\min(d, 256)$ |

So the collision strength is $\min(d/2, c/2)$. A short output is limited as any $d$-bit function is; a long output cannot give more than $c/2$ bits. For example, with $d = 224$ both give 112 bits against collisions, but SHAKE128 gives 128 bits against preimages and SHAKE256 gives 224.

## The algorithm

```pseudo id=main
SHAKE(M, s, ℓ)                            ▷ s = 128 or 256; returns ℓ bytes
L1  r ← 200 − s/4                         ▷ rate in bytes; capacity c = 2s bits
L2  P ← M ‖ 1F                            ▷ suffix 1111, then the first 1 of pad10*1
L3  append zero bytes to P until r divides |P|
L4  set the top bit of the last byte of P      ▷ the final 1 of pad10*1
L5  A ← 0; for each r-byte block B of P do
L6      A ← KECCAK-F(A ⊕ (B ‖ 0^(200 − r)));  buf ← the first r bytes of A
L7  out ← empty; while |out| < ℓ do
L8      if buf is empty then A ← KECCAK-F(A); buf ← the first r bytes of A
L9      move the first min(ℓ − |out|, |buf|) bytes of buf to the end of out
L10 return out
```

The byte $\texttt{1F}$ is the bit string 1, 1, 1, 1, 1, 0, 0, 0 in the bit order of FIPS 202 Appendix B.1: four suffix bits and the first padding bit. When $n \equiv r - 1 \pmod r$, the suffix and both padding bits share the byte $\texttt{9F}$. The code keeps $A$ and $buf$ in an object, so a caller can call lines L7 to L10 many times and read the output in pieces.

## Example

**SHAKE128 of the empty message.** The padded message is one block of 168 bytes: $\texttt{1F}$, 166 zero bytes, $\texttt{80}$. After one call of Keccak-f[1600], $A[0, 0] = \texttt{7d828fe8a42b9c7f}$ and $A[1, 0] = \texttt{3e85057650456061}$, so the output starts with the bytes of these lanes in little-endian order:

$$\mathrm{SHAKE128}(\text{""}, 256) = \texttt{7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26}.$$

The NIST example asks for 4096 bits, 512 bytes. The first read gives bytes 0 to 167; lines L8 then call Keccak-f three more times for bytes 168 to 335, 336 to 503 and 504 to 671, of which the first 8 are used. The last 32 bytes are $\texttt{43e41b45a653f2a5c4492c1add544512dda2529833462b71a41a45be97290b6f}$, as in NIST's file.

**The prefix property.** $\mathrm{SHAKE128}(\text{abc}, 128) = \texttt{5881092dd818bf5cf8a3ddb793fbcba7}$, and the 256-bit output is the same 16 bytes followed by $\texttt{4097d5c526a6d35f97b83351940f2cc8}$. For SHAKE256, the 32-byte output of "abc" is $\texttt{483366601360a8771c6863080cc4114d8db44530f8f1e1ee4f94ea37e78b5739}$, and the 64-byte output starts with it.

**SHAKE256 is not SHA3-256.** Both have rate 136, but the suffix differs: $\mathrm{SHAKE256}(\text{""}, 256) = \texttt{46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762f}$, while SHA3-256("") is $\texttt{a7ffc6f8}\ldots$. The tests check the four NIST examples (the first and last 32 of 512 bytes), the prefix property at the rate boundaries, reads in pieces of 1, 7, 136 and 137 bytes, and agreement with `hashlib`.

## Correctness

Lines L2 to L4 are injective and give whole blocks, by the padding lemma of the [Keccak](/keccak/) page with $d = \texttt{1F}$. Lines L5 and L6 are the absorbing phase of FIPS 202 Algorithm 8. The loop of lines L7 to L9 keeps this invariant: out followed by buf is a prefix of the infinite squeezed string $\mathrm{Trunc}_r(S_0) \| \mathrm{Trunc}_r(S_1) \| \cdots$, with $S_{i+1} = f(S_i)$. So the output is the first $\ell$ bytes of $\mathrm{KECCAK}[c](M \| 1111)$, whatever the sizes of the pieces. The proof file gives the details.

## Complexity

Absorbing takes $\lfloor n/r \rfloor + 1$ calls of Keccak-f[1600] and squeezing $\lceil \ell/r \rceil - 1$ more, each $\Theta(1)$. So the time is $\Theta(n + \ell)$ and the extra space is the 200-byte state and the buffer, $\Theta(1)$. SHAKE128 has the largest rate of the FIPS 202 functions, 168 bytes, so it is the fastest of them; SHAKE256 runs at the speed of SHA3-256.

## Properties

- **Prefix property.** $\mathrm{SHAKE}(M, d) = \mathrm{Trunc}_d(\mathrm{SHAKE}(M, d'))$ for $d \le d'$ (FIPS 202 Appendix A.2). So outputs of different lengths from the same message are related.
- **Security set by the capacity.** The strength is $c/2$ bits for long outputs, by the sponge bound; a larger $d$ does not help beyond that.
- **Domain separation.** SHAKE adds 1111, SHA-3 01 and cSHAKE 00, so the three families never share an input to Keccak[$c$]. RawSHAKE (FIPS 202 Section 6.3) uses 11 and leaves the last two bits to tree-hashing modes such as Sakura.
- **No length extension**, for the same reason as SHA-3: the capacity bits are never output.

## Variants and improvements

- **cSHAKE128 and cSHAKE256** (SP 800-185) add a function name and a customization string; with both empty they are SHAKE. See [extendable-output function](/extendable-output-function/).
- **KMACXOF128 and KMACXOF256** are keyed XOFs built on cSHAKE. See [KMAC](/kmac/).
- **TurboSHAKE and KangarooTwelve** use 12 rounds of Keccak-p[1600] instead of 24 for about twice the speed, and KangarooTwelve adds a tree mode for long inputs.
- **Uses in standards.** ML-KEM (FIPS 203) and ML-DSA (FIPS 204) expand seeds into matrices with SHAKE128 and SHAKE256, SLH-DSA (FIPS 205) has SHAKE instances, and Ed448 (RFC 8032) hashes with SHAKE256 to 114 bytes.

## When to use it

Use SHAKE256, or SHAKE128 at the 128-bit level, from a vetted library when you need an output length that the fixed hashes do not offer: a key stream from a seed, a mask, a long random-looking string for a lattice scheme, or a hash of a non-standard size. Ask for at least $2s$ bits when you need collision resistance at strength $s$. When the output must also depend on its length or on a label, use cSHAKE or KMAC instead, or put the length into the input. For key derivation with a secret key, [HKDF](/hkdf/) or KMAC is the usual choice.

## Pitfalls

- **Too short an output.** SHAKE256 with 128 bits of output has only 64-bit collision resistance. The name gives the ceiling, not the actual strength.
- **Related outputs.** SHAKE128$(M, 16)$ is the first half of SHAKE128$(M, 32)$. A protocol that derives a short key and a long key from the same input gets one key inside the other.
- **SHAKE128 is not SHA3-128.** There is no SHA3-128. SHAKE128 with 256 output bits still has only 128-bit security against preimages.
- **Single-shot APIs.** `hashlib.shake_128(M).digest(n)` recomputes from the start on each call; to read a stream, use an object that keeps the state, as the code here does.
- **For study only.** The code on this page is slow and not constant time. Use `hashlib.shake_128` and `hashlib.shake_256`, OpenSSL or a validated module.

## Implementations

## History

The sponge construction always had an output of any length, and Keccak's competition submission of 2008 was already defined with an output of arbitrary length. After Keccak won in 2012, NIST added the domain suffixes and two functions with fixed capacities, and FIPS 202 (August 2015) published them as SHAKE128 and SHAKE256, the first standard XOFs; the name joins "Secure Hash Algorithm" and "Keccak". SP 800-185 (2016) built cSHAKE and KMAC on them, and the post-quantum standards FIPS 203, 204 and 205 (2024) made SHAKE a core component.

## References
