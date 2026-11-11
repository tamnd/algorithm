---
tag: HK9M2T
kind: algorithm
slug: md4
name: MD4
aliases:
- Message Digest 4
area: cryptography/hash-functions
level: core
summary: Rivest's 128-bit hash of 1990 (RFC 1320). Three rounds of 16 steps on 32-bit words. Collisions are found by hand since 2005; it is broken and historic.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1990
  people: [Ronald L. Rivest]
  note: Rivest published MD4 at CRYPTO 1990 and in RFC 1186 (October 1990), then in RFC 1320 (April 1992). RFC 6150 moved it to Historic status in 2011.
prereqs: [merkle-damgard-construction, davies-meyer-construction]
see_also: [md5, sha-1, ripemd-160, collision-resistance, collision-finding, preimage-resistance, cryptographic-hash-function]
sources:
  - paper: doi:10.17487/RFC1320
    title: R. Rivest, RFC 1320, The MD4 Message-Digest Algorithm, April 1992
    locator: Section 3 (steps 1 to 5 of the algorithm), Appendix A.3 (reference code) and Appendix A.5 (test suite)
  - paper: "Ronald L. Rivest, The MD4 message digest algorithm, Advances in Cryptology, CRYPTO '90, LNCS 537, Springer, 1991"
    locator: the design goals and the first description of MD4
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.4.2, Algorithm 9.49 (MD4), Remark 9.50, Table 9.6 (test vectors) and Table 9.7 (notation)
  - paper: "Hans Dobbertin, Cryptanalysis of MD4, Fast Software Encryption, FSE 1996, LNCS 1039, Springer, 1996"
    locator: the first collision attack on the full MD4
  - paper: "Xiaoyun Wang, Xuejia Lai, Dengguo Feng, Hui Chen and Xiuyuan Yu, Cryptanalysis of the hash functions MD4 and RIPEMD, Advances in Cryptology, EUROCRYPT 2005, LNCS 3494, Springer, 2005"
    locator: MD4 collisions with fewer than 2^8 MD4 computations, which can be found by hand
  - paper: "Gaëtan Leurent, MD4 is not one-way, Fast Software Encryption, FSE 2008, LNCS 5086, Springer, 2008"
    locator: the first preimage attack on the full MD4, in about 2^102 operations
  - paper: doi:10.17487/RFC6150
    title: S. Turner and L. Chen, RFC 6150, MD4 to Historic Status, March 2011
    locator: the summary of the attacks and the move to Historic status
---

MD4 is a [cryptographic hash function](/cryptographic-hash-function/) that Ronald Rivest designed in 1990. It maps a message of any length to a 128-bit digest. It is the [Merkle-Damgard construction](/merkle-damgard-construction/) over a compression function of three rounds of 16 steps, which uses only 32-bit addition, bitwise functions and rotations. MD4 was the model for MD5, SHA-1, SHA-2 and RIPEMD-160, so it is worth study. But it is broken: Dobbertin found collisions in 1996, and since 2005 a collision takes fewer than $2^8$ MD4 computations (Wang et al.). Do not use MD4 for any security purpose.

**Notation.** All words have 32 bits. $+$ is addition modulo $2^{32}$, $\lll s$ is a left rotation by $s$ bits, $\wedge$, $\vee$, $\oplus$ and $\neg$ are the bitwise AND, OR, XOR and NOT. $(A, B, C, D)$ is the chaining value. $X[0 \ldots 15]$ are the 16 words of a 512-bit block, read in little-endian order. $n$ is the message length in bytes.

## In plain words

MD4 cuts the message into blocks of 64 bytes. It keeps four numbers of 32 bits as its state. It starts from four fixed numbers. For each block, it mixes the 16 words of the block into the state in 48 small steps. Each step changes one of the four numbers: it adds a simple function of the other three, adds one word of the block, and rotates the result. After the 48 steps, it adds the old state to the new one. When all blocks are done, the four numbers are the digest. Before it starts, MD4 adds one 1 bit, some zero bits and the length of the message, so that the length is a full number of blocks and two messages of different lengths never give the same blocks.

## The problem

The input is a message $M$ of $8n$ bits (the RFC allows any number of bits; this page and the code use whole bytes). The output is a 128-bit digest. The goal of the design was a fast hash with [collision resistance](/collision-resistance/), [preimage resistance](/preimage-resistance/) and [second preimage resistance](/second-preimage-resistance/) at the generic levels $2^{64}$, $2^{128}$ and $2^{128}$. MD4 does not meet any of these goals today.

## The algorithm

The round functions are $F(x, y, z) = (x \wedge y) \vee (\neg x \wedge z)$ (a bitwise "if $x$ then $y$ else $z$"), $G(x, y, z) = (x \wedge y) \vee (x \wedge z) \vee (y \wedge z)$ (bitwise majority) and $H(x, y, z) = x \oplus y \oplus z$. The round constants are $K_2 = \texttt{5A827999} = \lfloor 2^{30} \sqrt{2} \rfloor$ and $K_3 = \texttt{6ED9EBA1} = \lfloor 2^{30} \sqrt{3} \rfloor$. Round 1 adds no constant. The initial value is $A = \texttt{67452301}$, $B = \texttt{EFCDAB89}$, $C = \texttt{98BADCFE}$, $D = \texttt{10325476}$.

```pseudo id=main
MD4(M)
L1  P ← M ‖ 1 ‖ 0^k ‖ [8n]_64            ▷ k ≥ 0 makes |P| ≡ 0 mod 512; length little-endian
L2  (A, B, C, D) ← IV
L3  for each 512-bit block Y of P, in order, do
L4      (A, B, C, D) ← COMPRESS((A, B, C, D), Y)
L11 return A ‖ B ‖ C ‖ D                  ▷ each word in little-endian byte order

COMPRESS((A, B, C, D), Y)
L5  X[0..15] ← the 16 little-endian words of Y
L6  (a, b, c, d) ← (A, B, C, D)
L7  for i ← 0 to 15: a ← (a + F(b, c, d) + X[i]) ⋘ s1[i mod 4], then (a, b, c, d) ← (d, a, b, c)
L8  for i ← 0 to 15: a ← (a + G(b, c, d) + X[r2[i]] + K2) ⋘ s2[i mod 4], then (a, b, c, d) ← (d, a, b, c)
L9  for i ← 0 to 15: a ← (a + H(b, c, d) + X[r3[i]] + K3) ⋘ s3[i mod 4], then (a, b, c, d) ← (d, a, b, c)
L10 return (A + a, B + b, C + c, D + d)
```

The shifts are $s_1 = (3, 7, 11, 19)$, $s_2 = (3, 5, 9, 13)$ and $s_3 = (3, 9, 11, 15)$. Round 1 reads the words in order $0, 1, \ldots, 15$. Round 2 reads them by columns of a 4 by 4 grid, $r_2 = (0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15)$. Round 3 uses the bit-reversal order $r_3 = (0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15)$. The register rotation $(a, b, c, d) \leftarrow (d, a, b, c)$ is the RFC's pattern `[ABCD]`, `[DABC]`, `[CDAB]`, `[BCDA]`: the steps update the registers in the order $A, D, C, B$. Line L10 is the feed-forward. With it, COMPRESS has the [Davies-Meyer](/davies-meyer-construction/) form $E_Y(H) + H$: the 48 steps are a "cipher" $E$ keyed by the block $Y$, and the addition is word by word.

## Example

Hash the 3-byte message `abc`. The padding adds the byte `80`, 52 zero bytes and the bit length $24 = \texttt{18}$ as 8 little-endian bytes, so $P$ is one block. Its words are $X[0] = \texttt{80636261}$, $X[14] = \texttt{00000018}$, and 0 for the others.

Step 0 of round 1 updates $A$. Where $B$ has a 0 bit, $C$ and $D$ agree, so $F(B, C, D) = C = \texttt{98BADCFE}$. Then $A + F + X[0] = \texttt{67452301} + \texttt{98BADCFE} + \texttt{80636261} = \texttt{80636260}$ modulo $2^{32}$, and the rotation by 3 gives $A = \texttt{031B1304}$. The registers after each round are:

| after | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| start (IV) | `67452301` | `EFCDAB89` | `98BADCFE` | `10325476` |
| round 1 | `A299A540` | `DA717395` | `24BAADCB` | `04E19293` |
| round 2 | `7296594C` | `8E531B8F` | `3DD42422` | `4E7E1748` |
| round 3 | `12BC25A3` | `630A7626` | `4F4FE461` | `8D405204` |
| feed-forward | `7A0148A4` | `52D821AF` | `E80AC15F` | `9D72A67A` |

The digest is the four words in little-endian byte order: `a448017aaf21d8525fc10ae87aa6729d`. This is the value for "abc" in RFC 1320, Appendix A.5. A script computed the table, and the test file checks all seven vectors of A.5.

## Correctness

The padding of line L1 is injective, its length is a multiple of 512 bits, and its last 64 bits hold the length of $M$. So MD4 is the Merkle-Damgard iteration of COMPRESS with MD strengthening, and the loop of lines L3 and L4 keeps the invariant "$(A, B, C, D) = H_i$, the chaining value after $i$ blocks". Each step of lines L7 to L9 is a bijection of the state for a fixed message word, because the rotation and the addition of a value that depends only on $b$, $c$ and $d$ can be undone. So the 48 steps form a permutation, as the Davies-Meyer view needs. The full proof is below. That the code computes the RFC function is checked against the RFC test suite, not proved.

## Complexity

One call of COMPRESS does 48 steps. Each step does 2 additions (round 1) or 3 additions (rounds 2 and 3, which also add a constant), one rotation and one round function of 2 to 5 bitwise operations, so a block costs a few hundred word operations, a constant. The padded message has $\lfloor (n + 8)/64 \rfloor + 1$ blocks. So the time is $\Theta(n)$ in each case. A streaming implementation keeps the state, one partial block and a byte count, so the extra space is $\Theta(1)$. MD4 was designed to be fast on 32-bit machines: it has the fewest steps of the family (MD5 has 64, SHA-1 has 80).

## Properties

- The digest has 128 bits, the block 512 bits, the chaining value 128 bits.
- It is little-endian, like MD5 and RIPEMD-160, and unlike SHA-1 and SHA-2.
- It has the [length extension](/length-extension-attack/) property of each plain Merkle-Damgard hash: the digest of $M$ is the state after $M$ and its padding, so anyone can continue the iteration.
- It is deterministic and keyless.
- Security today: collisions in fewer than $2^8$ MD4 computations (Wang et al. 2005), and preimages in about $2^{102}$ (Leurent 2008). It has no security left for collisions, and its preimage margin is far below the 128-bit goal.

## Variants and improvements

- [MD5](/md5/) (1991) adds a fourth round, a distinct constant per step, the addition of the previous register to each step, and new shifts. It is also broken.
- [SHA-1](/sha-1/) and [SHA-2](/sha-2/) keep the MD4 structure but expand the 16 message words into 80 or 64 words, and use larger states.
- [RIPEMD-160](/ripemd-160/) runs two MD4-like lines in parallel and combines them. It is not broken.
- Extended MD4 (two parallel lines, 256-bit output) is in Rivest's 1990 paper. The first RIPEMD (1992) also ran two MD4-like lines. Wang et al. 2005 break the first RIPEMD too.

## When to use it

Do not use MD4 to protect data. The NT hash of Windows passwords is MD4 of the UTF-16LE password, with no salt. Systems that store it need other protections, and new systems must not copy it. Use MD4 only to study the design and the attacks, and to read or verify old formats that need it. For a new design, use [SHA-2](/sha-2/) or [SHA-3](/sha-3/).

## Pitfalls

- MD4 is little-endian. An implementation that reads big-endian words gives other digests, and the RFC test suite catches it.
- The length field holds the length in bits modulo $2^{64}$, not in bytes.
- A message of 56 to 63 bytes needs a second block, because the 8 length bytes do not fit after the `80` byte. Test 55, 56 and 64 bytes: they give 1, 2 and 2 blocks.
- The round 2 and round 3 word orders and shifts differ. A swap of $r_2$ and $r_3$ gives a function that passes no vector.
- The code on this page is for study only. It is not constant time and must not protect real data. Python's `hashlib.new("md4")` may fail on recent systems, because OpenSSL 3 moved MD4 to its legacy provider.

## Implementations

## History

Rivest designed MD4 in 1990 and published it at CRYPTO 1990 and as RFC 1186. RFC 1320 (April 1992) replaced RFC 1186. Den Boer and Bosselaers attacked the last two rounds in 1991. Rivest answered in 1991 with MD5, a slower and more careful design. Dobbertin found collisions of the full MD4 in 1996, at FSE 1996. In 2005, Wang, Lai, Feng, Chen and Yu gave a differential path that makes a collision with fewer than $2^8$ MD4 computations, so that a collision can be computed by hand. Leurent gave the first preimage attack, in about $2^{102}$, in 2008. RFC 6150 (2011) moved MD4 to Historic status.

## References
