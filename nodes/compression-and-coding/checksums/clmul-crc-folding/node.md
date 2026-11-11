---
tag: W0AB8H
kind: algorithm
slug: clmul-crc-folding
name: CRC folding with carry-less multiplication
aliases:
- CRC folding
- PCLMULQDQ CRC
area: compression-and-coding/checksums
level: advanced
summary: Computes a CRC with carry-less multiplication, folding wide blocks in parallel.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 2009
  people: [Vinodh Gopal, Erdinc Ozturk, Jim Guilford, Gil Wolrich, Wajdi Feghali, Martin Dixon, Deniz Karakoyunlu]
  note: An Intel white paper showed how to compute a CRC of any generator with the PCLMULQDQ instruction by folding and Barrett reduction.
prereqs: [table-driven-crc, barrett-reduction, gf2-polynomial-arithmetic]
see_also: [cyclic-redundancy-check, slicing-by-8, crc32c, gcm-mode, horner-rule, word-ram]
sources:
  - url: https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/fast-crc-computation-generic-polynomials-pclmulqdq-paper.pdf
    title: Vinodh Gopal, Erdinc Ozturk, Jim Guilford, Gil Wolrich, Wajdi Feghali, Martin Dixon and Deniz Karakoyunlu, Fast CRC computation for generic polynomials using PCLMULQDQ instruction, Intel white paper 323102, December 2009
    locator: Fold by 4 (p. 11), fold by 1 (p. 12), final reduction with Barrett (p. 13), the IEEE 802.3 constants (p. 16), bit reflection (p. 18), and the gzip constants (pp. 21 and 22)
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Check values of CRC-32/ISO-HDLC (0xCBF43926), CRC-32/ISCSI (0xE3069283) and CRC-32/BZIP2 (0xFC891918)
  - url: https://www.rfc-editor.org/rfc/rfc3720
    title: J. Satran et al., RFC 3720, Internet Small Computer Systems Interface (iSCSI), 2004
    locator: Appendix B.4 (CRC-32C of 32 zero bytes)
---

CRC folding computes a [cyclic redundancy check](/cyclic-redundancy-check/) with a carry-less multiply instruction such as PCLMULQDQ on x86 or PMULL on ARM. It multiplies 64-bit halves of 128-bit blocks by fixed powers of $x$ modulo the generator, so that four blocks are processed in parallel and each block takes two multiplies. At the end, a [Barrett reduction](/barrett-reduction/) over GF(2) gives the 32-bit remainder. An Intel white paper by Gopal and co-authors described the method for any generator in 2009, and it is the fastest software CRC on CPUs that have the instruction.

## In plain words

A CRC is the remainder of a division. The remainder of a long number does not change if you replace its first part by any smaller number with the same remainder. Folding does this again and again: it takes the first 128 bits, multiplies them by a fixed constant that moves them down the message, and adds them onto the next 128 bits. The message gets shorter by one block at each step, and the remainder stays the same.

A special CPU instruction does this multiply without carries in a few cycles. The method keeps four blocks moving at once so that the CPU is never idle. At the end, a short calculation with two more multiplies turns the last block into the 32-bit CRC.

## The problem

The input is a byte string of $n$ bytes and the parameters of a 32-bit CRC in the model of Ross Williams: poly, init, refin, refout and xorout. The output is the CRC value. The model is the [word RAM](/word-ram/) with an extra $O(1)$ operation `clmul(a, b)`, the carry-less product of two 64-bit words, which has 127 bits. The implementation computes `clmul` in software.

## The algorithm

Write $P = x^{32} + \text{poly}$ and $\mathrm{fold}_T(X) = H \cdot (x^{T+64} \bmod P) \oplus L \cdot (x^T \bmod P)$ for a 128-bit $X = H x^{64} + L$. Then $\mathrm{fold}_T(X) \equiv X x^T \pmod P$, and it has fewer than 96 bits. The constants are those of the white paper:

| name | value | for the IEEE CRC-32 |
|---|---|---|
| $k_1$ | $x^{4 \cdot 128 + 64} \bmod P$ | 0x8833794C |
| $k_2$ | $x^{4 \cdot 128} \bmod P$ | 0xE6228B11 |
| $k_3$ | $x^{128 + 64} \bmod P$ | 0xC5B9CD4C |
| $k_4$ | $x^{128} \bmod P$ | 0xE8A45605 |
| $k_5$ | $x^{96} \bmod P$ | 0xF200AA66 |
| $k_6$ | $x^{64} \bmod P$ | 0x490D678D |
| $\mu$ | $\lfloor x^{64} / P \rfloor$ | 0x104D101DF |

```pseudo id=main
CRC-FOLD(data, poly, init, refin, refout, xorout)     ▷ k = 8n ≥ 32 bits
L1  M ← the data (each byte bit-reversed if refin) as a polynomial; V ← M XOR init · x^(k − 32); cut V into 128-bit chunks C₀ … C_{N−1}, with zeros at the top
L2  X ← C₀; if N ≥ 4 then A₀ … A₃ ← C₀ … C₃
L3      while 4 or more chunks remain do A_j ← fold₅₁₂(A_j) XOR (next chunk j), for j = 0 … 3
L4      X ← A₀; for j ← 1 to 3 do X ← fold₁₂₈(X) XOR A_j
L5  for each remaining chunk C do X ← fold₁₂₈(X) XOR C
L6  t ← H · k₅ XOR L · x^32                          ▷ X = H x^64 + L; now t ≡ X · x^32, under 96 bits
L7  t ← (t >> 64) · k₆ XOR (t AND (2^64 − 1))         ▷ under 64 bits
L8  reg ← BARRETT(t)
L11 if refout then reverse the 32 bits of reg; return reg XOR xorout

BARRETT(t)                                           ▷ deg t < 64
L9  q ← (clmul(t >> 32, μ)) >> 32
L10 return (t XOR clmul(q, P)) AND (2^32 − 1)
```

Line L1 puts init into the first 32 bits of the message, which gives the same CRC. Messages of fewer than 4 bytes skip the folds: $I x^k + M x^{32}$ then has fewer than 64 bits, and BARRETT reduces it directly.

**Bit order.** This page and the code work in the normal domain for every CRC. For a CRC with refin, the code first reverses the bits of each byte. The white paper also gives a reflected form for CRC-32 of gzip, which works on the bytes as they are and uses reflected constants. The tests check the reflected constants of the paper, $k_1' = \text{0x154442BD4}$ to $\mu' = \text{0x1F7011641}$, as the 33-bit reversals of $x^{e} \bmod P$ for $e = 544, 480, 160, 96, 64, 32$ and of $\mu$. The code does not run the reflected form.

## Example

CRC-32/ISO-HDLC of the 32 bytes 0x00, 0x01, …, 0x1F. After the bit reversal of each byte and the XOR of init into the first 32 bits, $V$ has two chunks:

| step | value (hex) |
|---|---|
| $C_0$ | FF7FBF3F 20A060E0 109050D0 30B070F0 |
| $C_1$ | 088848C8 28A868E8 189858D8 38B878F8 |
| $\mathrm{fold}_{128}(C_0)$ | 00000000 4DFAFF0D 432F131E AD764FB0 |
| $X$ = fold XOR $C_1$ | 088848C8 655297E5 5BB74BC6 95CE3748 |
| $t$ after line L6 | 5C59E597 DB8673A9 7386B7BE |
| $t$ after line L7 | CE2D4ED1 E899E64D |
| $q$ in line L9 | CD4D4A75 |
| reg after line L10 | AE819B76 |

The bit reversal of 0xAE819B76 is 0x6ED98175, and its XOR with 0xFFFFFFFF is 0x91267E8A. This equals `binascii.crc32(bytes(range(32)))`.

## Correctness

Each fold replaces a block by a smaller value that is congruent modulo $P$ to the block times $x^T$. So the value of the whole message modulo $P$ stays the same through lines L3 to L5, by [Horner's rule](/horner-rule/) on the 128-bit chunks. Lines L6 and L7 multiply by $x^{32}$ and shorten the value to 64 bits with the same rule. Barrett reduction over GF(2) is exact for a dividend of fewer than 64 bits: with $\mu = \lfloor x^{64}/P \rfloor$, the estimate $q$ of line L9 is the true quotient, because a degree count shows that $t + qP$ has degree less than 32. Unlike Barrett over the integers, no correction step is necessary. The full proof is below.

## Complexity

- **Time.** $\Theta(n)$. Each 128-bit chunk costs 2 carry-less products and 2 XORs. The implementation counts the products: for 1024 bytes there are 64 chunks, so 15 rounds of 8 in line L3, 3 folds of 2 in line L4, 2 in lines L6 and L7, and 2 in BARRETT, which is 130 products.
- **Parallelism.** In line L3 the four accumulators are independent, so four pairs of products run at the same time. This hides the latency of the instruction, which is several cycles.
- **Space.** Seven constants and four 128-bit accumulators.

On CPUs with PCLMULQDQ, folding is much faster than [slicing-by-8](/slicing-by-8/) for long messages, because it handles 16 bytes with two products and no table loads. The exact speed depends on the CPU and on the number of accumulators.

## Properties

- **Any generator.** Only the constants depend on $P$. The same code computes CRC-32, [CRC-32C](/crc32c/) and any other 32-bit CRC; CRC-64 works the same way with 64-bit constants.
- **Same result** as the bit-by-bit CRC for each length and each parameter set.
- **Streaming.** The four accumulators are the state. A stream that ends in the middle of a chunk needs care with the tail.
- **No tables.** The method needs no lookup table, so it has no cache misses and no timing that depends on the data.

## Variants and improvements

- **Wider registers.** With VPCLMULQDQ on 256-bit or 512-bit registers, code folds more blocks in each step, with constants for a larger $T$.
- **Fold by 1 only.** Lines L2 to L4 can be left out; the result is the same but slower.
- **The reflected form.** For refin CRCs, use the reflected constants of the white paper and work on the bytes directly, with no bit reversal.
- **Combined with the CRC32 instruction.** For CRC-32C on x86, fast code mixes the SSE4.2 CRC32 instruction on three streams with carry-less folding to join them.
- **CRC combine.** The same multiply by $x^T \bmod P$ joins the CRCs of parts of a file, as in the combine step of the [table-driven CRC](/table-driven-crc/).

## When to use it

Use folding for long messages on a CPU with a carry-less multiply: x86 with PCLMULQDQ, ARMv8 with PMULL, and others. Network stacks, storage and compression libraries use it. For messages of a few bytes, the fixed cost of the final reduction is larger than the gain, so a table-driven loop or a CRC instruction is as fast.

## Pitfalls

- **Wrong constants for the domain.** The normal and the reflected forms need different constants, with exponents that differ by 32 or 64. The constants for one form give a wrong result in the other.
- **The extra factor of $x$ in the reflected form.** A carry-less product of two reflected 64-bit values is the reflection of the true product shifted by one bit. The reflected constants of the paper include this shift.
- **Short messages.** Code that loads 64 bytes at a time needs a separate path for messages shorter than one round, and for the tail.
- **Barrett with the wrong $\mu$.** $\mu$ has 33 bits, with the top bit set. A 32-bit $\mu$ gives a wrong quotient.

## Implementations

## History

Intel added the PCLMULQDQ instruction with the Westmere processors in 2010, for the GHASH function of [GCM](/gcm-mode/). In a white paper of December 2009, Vinodh Gopal and co-authors at Intel showed how to compute a CRC of any generator with it, by folding with the constants $x^{T+64} \bmod P$ and $x^T \bmod P$ and a final Barrett reduction. Paul Barrett had published his reduction method for integers in 1986. The method of the white paper is now in the Linux kernel, in zlib-ng and in many other libraries.

## References
