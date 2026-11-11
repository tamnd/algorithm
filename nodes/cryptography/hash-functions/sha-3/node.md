---
tag: J553RH
kind: algorithm
slug: sha-3
name: SHA-3
aliases:
- Secure Hash Algorithm 3
- SHA3-256
area: cryptography/hash-functions
level: core
summary: The FIPS 202 hash functions SHA3-224, SHA3-256, SHA3-384 and SHA3-512, each the Keccak sponge with capacity c = 2d, the suffix 01 and one Keccak-f[1600] call per block of 1600 - 2d bits.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche]
  note: Keccak won the NIST SHA-3 competition in October 2012, and NIST published it with the domain suffix 01 and capacity 2d as FIPS 202 in August 2015.
prereqs: [keccak, sponge-construction]
see_also: [shake, sha-2, extendable-output-function, kmac, length-extension-attack, blake2, cryptographic-hash-function, hmac]
sources:
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 5 (pad10*1 and Keccak[c]), Section 6.1 (the four SHA-3 functions), Appendix A.1 (Table 4, security strengths) and Appendix B.2 (the byte forms of the padding)
  - url: "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values"
    title: NIST, Cryptographic standards and guidelines, example values for SHA-3
    locator: SHA3-224, SHA3-256, SHA3-384 and SHA3-512, for the empty message and for the 1600-bit message of bytes A3
  - url: "https://www.di-mgt.com.au/sha_testvectors.html"
    title: David Ireland, Test vectors for SHA-1, SHA-2 and SHA-3
    locator: the SHA-3 digests of "abc", a secondary source used in the tests
  - paper: doi:10.6028/NIST.IR.7896
    title: Shu-jen Chang, Ray Perlner, William E. Burr, Meltem Sönmez Turan, John M. Kelsey, Souradyuti Paul and Lawrence E. Bassham, Third-Round Report of the SHA-3 Cryptographic Hash Algorithm Competition, NISTIR 7896, November 2012
    locator: the selection of Keccak and the reasons NIST gave for it
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: the generic bound for a sponge with capacity c, the reason for c = 2d
---

SHA-3 is the hash standard FIPS 202, published by NIST in August 2015 as the result of a public competition that [Keccak](/keccak/) won in 2012. It defines four fixed-length hash functions, SHA3-224, SHA3-256, SHA3-384 and SHA3-512, with the digest lengths $d$ in their names. Each one is the [sponge construction](/sponge-construction/) over the permutation Keccak-f[1600] with capacity $c = 2d$ bits: SHA3-$d(M) = \mathrm{KECCAK}[2d](M \| 01, d)$. The two suffix bits 01 separate SHA-3 from the extendable-output functions [SHAKE](/shake/), which use 1111 in the same place. SHA-3 is not a replacement for [SHA-2](/sha-2/), which is still secure, but an alternative with a different internal structure and no length extension.

**Notation.** $d \in \{224, 256, 384, 512\}$ is the digest length in bits, $c = 2d$ the capacity, and $r = 200 - d/4$ the rate in bytes, that is $1600 - 2d$ bits. KECCAK-F is Keccak-f[1600] on 25 lanes of 64 bits, as on the [Keccak](/keccak/) page. Bytes go into lanes in little-endian order (FIPS 202 Appendix B.1). $n$ is the message length in bytes, and "abc" is the 3-byte message 61 62 63.

## In plain words

SHA-3 keeps a state of 200 bytes, all zero at the start. It reads the message in blocks of $r$ bytes. It XORs each block into the first $r$ bytes of the state and then mixes the whole state with Keccak-f. The last $200 - r$ bytes, the capacity, are never touched by the message directly and never output, so an attacker cannot control or see them. After the last block, the digest is simply the first $d/8$ bytes of the state. Before it starts, SHA-3 adds the bits 01 and the padding to the message, so that SHA-3 and SHAKE never compute the same thing.

## The problem

The input is a message $M$ of $n$ bytes and a digest length $d$. The output is the $d$-bit digest SHA3-$d(M)$. It must behave like a random function: a collision should cost about $2^{d/2}$ work and a preimage or second preimage about $2^d$ (FIPS 202 Table 4). The four functions have these parameters:

| Function | $d$ | $c$ | Rate $r$ (bytes) | Collision | Preimage | Second preimage |
|---|---|---|---|---|---|---|
| SHA3-224 | 224 | 448 | 144 | 112 | 224 | 224 |
| SHA3-256 | 256 | 512 | 136 | 128 | 256 | 256 |
| SHA3-384 | 384 | 768 | 104 | 192 | 384 | 384 |
| SHA3-512 | 512 | 1024 | 72 | 256 | 512 | 512 |

## The algorithm

```pseudo id=main
SHA3(M, d)                                ▷ d ∈ {224, 256, 384, 512}
L1  r ← 200 − 2d/8                        ▷ rate in bytes; capacity c = 2d bits
L2  P ← M ‖ 06                            ▷ suffix 01, then the first 1 of pad10*1
L3  append zero bytes to P until r divides |P|
L4  set the top bit of the last byte of P      ▷ the final 1 of pad10*1
L5  A ← 0                                 ▷ 25 lanes of 64 bits
L6  for each r-byte block B of P do
L7      XOR B into the first r/8 lanes of A, little-endian
L8      A ← KECCAK-F(A)
L9  Z ← the 200 bytes of A
L10 return the first d/8 bytes of Z
```

Lines L2 to L4 are FIPS 202's $M \| 01 \| \mathrm{pad10^*1}$ written on bytes. In the bit order of Appendix B.1, the bits 0, 1, 1 (suffix 01 and the first padding bit) are bits 1 and 2 of a byte, which gives $\texttt{06}$. When $n \equiv r - 1 \pmod r$, the suffix and both padding bits share one byte, $\texttt{86}$. Lines L9 and L10 squeeze only once, because $d/8 \le r$ for all four functions.

## Example

**SHA3-256("abc").** The rate is 136 bytes, so the padded message is one block: $\texttt{61 62 63 06}$, then 131 zero bytes, then $\texttt{80}$. As lanes, $A[0, 0] = \texttt{0000000006636261}$ and lane 16, $A[1, 3]$, is $\texttt{8000000000000000}$; the other 15 rate lanes and the 8 capacity lanes are 0. One call of Keccak-f[1600] gives $A[0, 0] = \texttt{b225e24fa75d983a}$, $A[1, 0] = \texttt{bd90d36b2d175c04}$, $A[2, 0] = \texttt{5b529d3e6e085f85}$ and $A[3, 0] = \texttt{3215431145e2bf46}$. Their 32 bytes in little-endian order are the digest:

$$\text{SHA3-256}(\text{abc}) = \texttt{3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532}.$$

**The four functions.** The digests of "" are NIST example values; those of "abc" are from a secondary source and agree with `hashlib`:

| Function | "" | "abc" |
|---|---|---|
| SHA3-224 | `6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7` | `e642824c3f8cf24ad09234ee7d3c766fc9a3a5168d0c94ad73b46fdf` |
| SHA3-256 | `a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a` | `3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532` |
| SHA3-384 | `0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004` | `ec01498288516fc926459f58e2c6ad8df9b473cb0fc08c2596da7cf0e49be4b298d88cea927ac7f539f1edf228376d25` |
| SHA3-512 | `a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26` | `b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0` |

**The 1600-bit example.** NIST also gives the digests of 200 bytes of $\texttt{A3}$. With the padding, this is 2 blocks for SHA3-224, SHA3-256 and SHA3-384 and 3 blocks for SHA3-512, whose rate is 72 bytes. SHA3-256 of it is $\texttt{79f38adec5c20307a98ef76e8324afbfd46cfd81b22e3973c65fa1bd9de31787}$. The tests check all eight NIST values and messages of lengths around each rate against `hashlib`.

## Correctness

Lines L2 to L4 are injective and give a whole number of blocks, by the padding lemma of the [Keccak](/keccak/) page with $d = \texttt{06}$. Lines L5 to L8 are the absorbing phase of FIPS 202 Algorithm 8. Because $d/8 \le 200 - d/4$ for $d \le 512$, the first $r$ bytes of the state already hold the $d/8$ output bytes, so the squeezing phase ends after one read, which is lines L9 and L10. So the code computes $\mathrm{KECCAK}[2d](M \| 01, d)$, the definition of SHA3-$d$ in FIPS 202 Section 6.1. The proof file gives the details. The NIST example values check the code, not the proof.

## Complexity

The padded message has $\lfloor n/r \rfloor + 1$ blocks, and each takes one call of Keccak-f[1600], which is $\Theta(1)$ work. So the time is $\Theta(n)$, and the extra space is the 200-byte state and one block, $\Theta(1)$. The cost per byte grows with $d$: SHA3-512 absorbs 72 bytes per call against 136 for SHA3-256, so it is almost twice as slow. In software without special instructions, SHA3-256 is slower than SHA-256 and much slower than [BLAKE2](/blake2/); in hardware it is small and fast.

## Properties

- Each SHA3-$d$ is a sponge, so it is indifferentiable from a random oracle up to about $2^{c/2} = 2^d$ queries of the permutation, if Keccak-f[1600] behaves like a random permutation.
- No length extension: the digest is part of the state, and the 1600 - d other bits are never output. So $H(K \| M)$ is a usable MAC, unlike with SHA-2; see [length-extension attack](/length-extension-attack/). [KMAC](/kmac/) is the standard form.
- Domain separation: SHA-3 adds 01, SHAKE 1111, and cSHAKE 00, so the functions never share an input to Keccak[$c$].
- The same digest lengths as SHA-2, so SHA-3 can replace SHA-2 in a protocol without changes to field sizes.

## Variants and improvements

- **SHAKE128 and SHAKE256** (FIPS 202 Section 6.2) are the extendable-output functions of the same standard. See [SHAKE](/shake/) and [extendable-output function](/extendable-output-function/).
- **cSHAKE, KMAC, TupleHash and ParallelHash** (SP 800-185, 2016) add customization strings, keys, tuples and parallel hashing on the same sponge.
- **Keccak-256** is the sponge without the suffix 01, as submitted to the competition, and is what Ethereum calls "keccak256". It gives different digests; see [Keccak](/keccak/).
- **KangarooTwelve and TurboSHAKE** use 12 rounds instead of 24 for about twice the speed, with the security margin that the Keccak team argues is still large.
- **HMAC-SHA3** is defined, with the rate as the HMAC block size, but it is not needed for security; KMAC is cheaper.

## When to use it

Use SHA3-256 or SHA3-512 from a vetted library when a standard asks for SHA-3, when you want a hash that does not share its design with SHA-2 as a hedge, or when you want $H(K \| M)$ to be safe without HMAC. Use SHAKE when you need a non-standard output length. Use SHA-256 when speed in software matters and processor support for SHA-2 exists, or [BLAKE2](/blake2/) or BLAKE3 for speed with no standard required.

## Pitfalls

- **Keccak-256 is not SHA3-256.** Some libraries and all of Ethereum use the pre-standard padding. The digest of "" tells them apart: `a7ffc6f8…` for SHA3-256, `c5d24601…` for Keccak-256.
- **Truncating SHA3-512 is not SHA3-256.** The capacity and the rate differ, so the first 32 bytes of SHA3-512$(M)$ have nothing to do with SHA3-256$(M)$.
- **Bit-level messages.** FIPS 202 allows messages of any number of bits, and the bit order inside a byte is from the least significant bit. Byte-oriented code such as this page cannot hash a message of 7 bits.
- **Rate boundaries.** A message of $r - 1$ bytes ends in the single byte $\texttt{86}$, and one of $r$ bytes needs a whole extra block. Bugs show up at exactly these lengths, so test them.
- **For study only.** The code on this page is slow and not constant time. Use `hashlib.sha3_256`, OpenSSL or a validated module.

## Implementations

## History

NIST announced a public competition for a new hash standard in November 2007, after the attacks of 2004 and 2005 on MD5 and SHA-1 raised doubts about the design that SHA-2 shares with them. It received 64 submissions, of which 51 entered the first round. Fourteen went to the second round in 2009, and five finalists were named in December 2010: BLAKE, [Grøstl](/groestl/), [JH](/jh-hash/), Keccak and [Skein](/skein/). On October 2, 2012, NIST chose Keccak, citing its large security margin, its efficiency in hardware and its design, which is very different from SHA-2. In 2013 NIST proposed to reduce the capacity to $c = 256$ or $512$ for speed; after public objections it kept $c = 2d$, which gives preimage resistance of $d$ bits under the generic sponge bound. FIPS 202 was published in August 2015 and added the suffix bits that separate SHA-3 from SHAKE.

## References
