---
tag: MDJVBV
kind: algorithm
slug: keccak
name: Keccak
aliases:
- Keccak-f permutation
- Keccak-256
area: cryptography/hash-functions
level: advanced
summary: The sponge family over the permutation Keccak-f[1600] (24 rounds of theta, rho, pi, chi, iota) that won the SHA-3 competition. Its original padding is still used as Keccak-256 in Ethereum.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche]
  note: Submitted to the NIST SHA-3 competition in October 2008, raised to 24 rounds in 2009, selected as the winner in October 2012, and standardized with new domain bits as SHA-3 in FIPS 202 (2015).
prereqs: [sponge-construction]
see_also: [sha-3, shake, extendable-output-function, kmac, blake2, sha-2, s-box, indifferentiability-framework]
sources:
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 3.1 (the state and its byte order), Section 3.2 (Algorithms 1 to 6, the step mappings and rc), Section 3.3 (Keccak-p and Algorithm 7), Section 5 (pad10*1 and Keccak[c]) and Appendix B.1 (bytes and bits)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, The Keccak reference, version 3.0, January 2011"
    locator: the definition of Keccak-f[b] and of the step mappings, the design rationale for each step, and the number of rounds 12 + 2l
  - url: "https://github.com/XKCP/XKCP/blob/master/tests/TestVectors/KeccakF-1600-IntermediateValues.txt"
    title: The Keccak team, XKCP, Keccak-f[1600] intermediate values
    locator: the example with the all-zero input, the round constants and the rotation offsets, used in the tests
  - url: "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values"
    title: NIST, Cryptographic standards and guidelines, example values for SHA-3
    locator: SHA3-256_Msg0.pdf, the state after each step of round 0 and the digest of the empty message
  - url: "https://github.com/ethereum/go-ethereum/blob/master/core/types/hashes.go"
    title: go-ethereum, core/types/hashes.go
    locator: EmptyCodeHash (Keccak-256 of the empty string) and EmptyRootHash (Keccak-256 of the byte 80)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: the generic security of a sponge over a random permutation, the basis of the Keccak security claim
---

Keccak is the family of [sponge](/sponge-construction/) functions that Bertoni, Daemen, Peeters and Van Assche submitted to the NIST SHA-3 competition in 2008 and that NIST chose as the winner in 2012. Its core is the permutation Keccak-f[1600] on a state of 1600 bits, arranged as a $5 \times 5$ array of 64-bit lanes. One call applies 24 rounds, and each round has five steps: $\theta$ mixes columns, $\rho$ rotates lanes, $\pi$ moves lanes, $\chi$ is the only nonlinear step, and $\iota$ adds a round constant. Keccak[$c$] is the sponge over this permutation with capacity $c$ and the multi-rate padding pad10*1. This page is about the permutation and the original Keccak sponge. [SHA-3](/sha-3/) and [SHAKE](/shake/) are the same sponge with two or four extra domain bits before the padding, so the original Keccak-256, which Ethereum uses, gives different digests from SHA3-256.

**Notation.** The state $A$ has 25 lanes $A[x, y]$ of $w = 64$ bits, $0 \le x, y < 5$; index $x$ and $y$ modulo 5. The code stores lane $(x, y)$ at index $x + 5y$, and byte $i$ of the 200-byte state is byte $i \bmod 8$ of lane $\lfloor i/8 \rfloor$, little-endian (FIPS 202 Section 3.1 and Appendix B.1). $\oplus$, $\wedge$ and $\neg$ act on lanes bit by bit, and $\mathrm{rot}(v, s)$ rotates a lane left by $s$ positions toward higher bit indices. $r$ is the rate in bytes, $c$ the capacity in bits, $r = 200 - c/8$. $n$ is the message length in bytes.

## In plain words

Picture the state as 25 boxes of 64 bits in a $5 \times 5$ grid. A round does five simple things. Every bit gets the parity of two nearby columns added to it, so a change in one bit spreads to 11 bits. Each box is rotated by its own fixed amount, and the boxes swap places, so bits that were neighbors move far apart. Each row of 5 bits goes through a small nonlinear function: a bit is flipped if its right neighbor is 0 and the next one is 1. Last, a constant goes into one box so that the rounds are not all the same. To hash, Keccak XORs each message block into the first $r$ bytes of the state and calls the permutation, then reads the digest from the first bytes.

## The problem

The input is a message $M$ of $n$ bytes, a capacity $c$ and an output length $\ell$. The output is $\ell$ bytes of Keccak[$c$]$(M)$. The design goal is that the permutation has no structure that an attacker can use, so that the sponge bound applies: collisions and preimages cost about $2^{c/2}$ for long outputs, and the digest behaves like a random oracle otherwise. Keccak-256 is Keccak[512] with $\ell = 32$ bytes and rate $r = 136$ bytes.

## The algorithm

The steps of round $i_r$ (FIPS 202 Algorithms 1 to 6):

- $\theta$: $C[x] = A[x, 0] \oplus A[x, 1] \oplus A[x, 2] \oplus A[x, 3] \oplus A[x, 4]$, $D[x] = C[x - 1] \oplus \mathrm{rot}(C[x + 1], 1)$, and $A[x, y] \leftarrow A[x, y] \oplus D[x]$.
- $\rho$: $A[x, y] \leftarrow \mathrm{rot}(A[x, y], r[x, y])$. Start at $(x, y) = (1, 0)$; for $t = 0, \ldots, 23$ set $r[x, y] = (t + 1)(t + 2)/2 \bmod 64$ and step $(x, y) \leftarrow (y, 2x + 3y)$. Lane $(0, 0)$ is not rotated.
- $\pi$: $A'[x, y] = A[(x + 3y) \bmod 5, x]$.
- $\chi$: $A'[x, y] = A[x, y] \oplus (\neg A[x + 1, y] \wedge A[x + 2, y])$.
- $\iota$: $A[0, 0] \leftarrow A[0, 0] \oplus RC[i_r]$, where bit $2^j - 1$ of $RC[i_r]$ is $\mathrm{rc}(j + 7 i_r)$ for $j = 0, \ldots, 6$, and $\mathrm{rc}(t)$ is the output of the LFSR with polynomial $x^8 + x^6 + x^5 + x^4 + 1$.

The code derives $RC$ and $r[x, y]$ from these rules, and the tests compare them with the tables of XKCP: $RC[0] = \texttt{0000000000000001}$, $RC[1] = \texttt{0000000000008082}$, $RC[23] = \texttt{8000000080008008}$, and $r$ row by row $(0, 1, 62, 28, 27), (36, 44, 6, 55, 20), (3, 10, 43, 25, 39), (41, 45, 15, 21, 8), (18, 2, 61, 56, 14)$.

```pseudo id=main
KECCAK-F(A)                               ▷ Keccak-f[1600] on 25 lanes of 64 bits
L1  for i ← 0 to 23 do
L2      A ← θ(A)                          ▷ add the parity of two nearby columns
L3      A ← ρ(A)                          ▷ rotate each lane by r[x, y]
L4      A ← π(A)                          ▷ A'[x, y] = A[x + 3y, x]
L5      A ← χ(A)                          ▷ nonlinear, row by row
L6      A ← ι(A, i)                       ▷ A[0, 0] ⊕= RC[i]
L7  return A

KECCAK[c](M, ℓ, d)                        ▷ r = 200 − c/8 bytes; d = 01 (Keccak), 06 (SHA-3), 1F (SHAKE)
L8  P ← M ‖ d
L9  append zero bytes to P until r divides |P|
L10 set the top bit of the last byte of P      ▷ the final 1 of pad10*1
L11 A ← 0
L12 for each r-byte block B of P do
L13     A ← KECCAK-F(A ⊕ (B ‖ 0^(200 − r)))
L14 Z ← empty; repeat
L15     Z ← Z ‖ the first r bytes of A
L16     if |Z| ≥ ℓ then return the first ℓ bytes of Z
L17     A ← KECCAK-F(A)
```

The byte $d$ holds the domain bits followed by the first 1 of pad10*1, in the bit order of FIPS 202 Appendix B.1: for Keccak there are no domain bits, so $d = \texttt{01}$; SHA-3 appends the bits 01, so $d = \texttt{06}$; SHAKE appends 1111, so $d = \texttt{1F}$. If $|M| \equiv r - 1 \pmod r$, lines L8 to L10 give one byte $d \mid \texttt{80}$.

## Example

**The permutation on the zero state.** Keccak-f[1600] maps the all-zero state to a state whose lane $(0, 0)$ is $\texttt{F1258F7940E1DDE7}$; the test checks all 25 lanes against XKCP.

**SHA3-256 of the empty message, round 0.** The absorbed state is the padding alone: byte 0 is $\texttt{06}$ and byte 135 is $\texttt{80}$, so lane $(0, 0)$ is $\texttt{6}$ and lane $(1, 3)$, at index 16, is $\texttt{8000000000000000}$. $\theta$ spreads these two lanes to 20 nonzero lanes; for example $A[1, 3]$ becomes $\texttt{8000000000000006}$. The table follows row $y = 0$, the five lanes $A[0, 0], \ldots, A[4, 0]$, through round 0 (as 64-bit numbers, 0 where a lane is zero):

| Step | $A[0,0]$ | $A[1,0]$ | $A[2,0]$ | $A[3,0]$ | $A[4,0]$ |
|---|---|---|---|---|---|
| input | 6 | 0 | 0 | 0 | 0 |
| after $\theta$ | 7 | 6 | 8000000000000000 | 0 | c |
| after $\rho$ | 7 | c | 2000000000000000 | 0 | 60000000 |
| after $\pi$ | 7 | 600000000000 | 40000000000 | 0 | 30000 |
| after $\chi$ | 40000000007 | 600000000000 | 40000030000 | 7 | 600000030000 |
| after $\iota$ | 40000000006 | 600000000000 | 40000030000 | 7 | 600000030000 |

For example, $\chi$ gives $A[3, 0] = 0 \oplus (\neg \texttt{30000} \wedge \texttt{7}) = \texttt{7}$, and $\iota$ adds $RC[0] = 1$ to $A[0, 0]$. The test compares the full 200-byte states after $\theta$ and after $\iota$ with NIST's example file. After 24 rounds, $A[0, 0] = \texttt{66D71EBFF8C6FFA7}$, whose little-endian bytes $\texttt{a7ffc6f8bf1ed766}$ start the digest.

**Keccak-256 against SHA3-256.** The two differ only in the byte $d$:

| Input | Keccak-256 ($d = \texttt{01}$) | SHA3-256 ($d = \texttt{06}$) |
|---|---|---|
| "" | `c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470` | `a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a` |
| "abc" | `4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45` | `3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532` |

The Keccak-256 value of "" is the `EmptyCodeHash` of go-ethereum, and Keccak-256 of the byte $\texttt{80}$ (the RLP encoding of an empty list) is its `EmptyRootHash`, $\texttt{56e81f17}\ldots\texttt{e363b421}$; the tests check both. The SHA3-256 values are the NIST example values and agree with `hashlib.sha3_256`.

## Correctness

Each of the five steps is a bijection of the state: $\rho$ and $\pi$ only move bits, $\iota$ adds a constant, $\chi$ is a bijection on each 5-bit row, and $\theta$ is linear with an invertible effect on the column parities. So Keccak-f[1600] is a permutation, which the sponge security argument needs. The padding of lines L8 to L10 is injective for a fixed $d$, and lines L11 to L17 are FIPS 202 Algorithm 8. The proof is in the proof file. That the code computes the standard function is checked by the XKCP and NIST test values, not proved.

## Complexity

One call of Keccak-f[1600] does 24 rounds of a fixed number of lane operations: about 50 XORs and 5 rotations for $\theta$, 24 rotations for $\rho$, 25 each of NOT, AND and XOR for $\chi$, and one XOR for $\iota$, so $\Theta(1)$ per call. A message of $n$ bytes takes $\lfloor n/r \rfloor + 1$ calls to absorb and $\lceil \ell/r \rceil - 1$ more to squeeze, so the time is $\Theta(n)$ and the extra space is the 200-byte state, $\Theta(1)$. A larger capacity means a smaller rate and so a slower hash: Keccak-512 absorbs 72 bytes per call, Keccak-256 136 and SHAKE128 168. $\chi$ has degree 2 and uses only AND, NOT and XOR, so Keccak is cheap in hardware and in bitsliced or masked software.

## Properties

- A permutation of 1600 bits, with an inverse that the hash never uses. $\chi^{-1}$ has degree 3 and $\theta^{-1}$ is dense.
- The steps are the same on every lane position up to rotation, which gives Keccak symmetries that $\iota$ breaks.
- Sponge security: with $c = 512$, generic collisions cost $2^{128}$ for a 256-bit output and preimages $2^{256}$.
- No length extension, unlike [SHA-2](/sha-2/): the capacity part of the state is never output.
- Cryptanalysis: the published collision attacks reach only a few of the 24 rounds (practical collisions for 5-round SHA3-224 and SHA3-256 were found in 2019), and distinguishers on the full permutation do not give attacks on the hash.

## Variants and improvements

- **Keccak-f[b]** for $b = 25 \cdot 2^l$, $l = 0, \ldots, 6$, with lanes of $2^l$ bits and $12 + 2l$ rounds. Keccak-f[200], [400] and [800] serve small devices.
- **Keccak-p[b, n_r]** (FIPS 202 Section 3.3) keeps only the last $n_r$ rounds. KangarooTwelve and TurboSHAKE use Keccak-p[1600, 12].
- **SHA-3 and SHAKE** (FIPS 202) are Keccak[$c$] with domain bits; see [SHA-3](/sha-3/) and [SHAKE](/shake/).
- **cSHAKE, KMAC, TupleHash and ParallelHash** (SP 800-185) are built on Keccak[256] and Keccak[512]. See [KMAC](/kmac/).
- **Duplex modes** such as Keyak and Ketje use reduced-round Keccak-p for authenticated encryption.

## When to use it

Use Keccak through SHA3-256, SHA3-512, SHAKE or KMAC from a vetted library when you want a hash that is not built like SHA-2, has no length extension, or needs extendable output. Use the original Keccak-256 only for compatibility with Ethereum and the systems built on it. For pure speed in software, [BLAKE2](/blake2/), BLAKE3 or SHA-256 with processor support are faster.

## Pitfalls

- **Keccak-256 is not SHA3-256.** Many libraries named "sha3" before 2015 implement the original Keccak. Ethereum's `keccak256` and the Solidity function of that name use $d = \texttt{01}$. Check the digest of the empty string: `c5d24601…` is Keccak-256, `a7ffc6f8…` is SHA3-256.
- **Bit order.** FIPS 202 numbers bits within a byte from the least significant bit. Getting this wrong flips the domain bits ($\texttt{06}$ against $\texttt{60}$) and the padding byte.
- **The single padding byte.** When one byte is free in the last block, the domain bits and both padding 1s share it: $\texttt{81}$ for Keccak, $\texttt{86}$ for SHA-3, $\texttt{9F}$ for SHAKE.
- **$\pi$ direction.** $A'[x, y] = A[x + 3y, x]$; the map $A'[y, 2x + 3y] = A[x, y]$ is the same step written the other way. Mixing the two gives a wrong permutation that still looks random.
- **For study only.** The code on this page is a direct transcription, slow and not constant time. Use `hashlib.sha3_256`, OpenSSL or XKCP.

## Implementations

## History

Bertoni, Daemen, Peeters and Van Assche introduced the sponge construction in 2007 and submitted Keccak to the SHA-3 competition in October 2008. In 2009, for the second round, they set the number of rounds to $12 + 2l$, 24 for Keccak-f[1600] instead of the earlier 18. NIST chose Keccak as SHA-3 on October 2, 2012, citing its large security margin, its hardware efficiency and its design, which is different from SHA-2. In 2013 NIST proposed lower capacities for the standard, then returned to $c = 2d$ after public comments. FIPS 202 (August 2015) added the domain bits that separate SHA-3 from SHAKE. Ethereum had already fixed on the original padding, so Keccak-256 lives on there.

## References
