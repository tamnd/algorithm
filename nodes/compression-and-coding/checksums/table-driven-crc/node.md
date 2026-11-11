---
tag: KSDEEZ
kind: algorithm
slug: table-driven-crc
name: Table-driven CRC
aliases:
- byte-wise CRC
- lookup-table CRC
area: compression-and-coding/checksums
level: intro
summary: Computes a CRC one byte at a time using a precomputed 256-entry table.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1988
  people: [Dilip V. Sarwate]
  note: Sarwate published the byte-at-a-time CRC with a table of 256 entries in Communications of the ACM.
prereqs: [cyclic-redundancy-check]
see_also: [slicing-by-8, clmul-crc-folding, crc32c, crc-generator-polynomial, gf2-polynomial-arithmetic, linear-feedback-shift-register]
sources:
  - paper: doi:10.1145/63030.63037
    title: Dilip V. Sarwate, Computation of cyclic redundancy checks via table look-up, Communications of the ACM 31(8), 1988
    locator: pp. 1008 to 1013 (the table of 256 entries and the byte-wise update of the register)
  - url: http://www.ross.net/crc/download/crc_v3.txt
    title: Ross N. Williams, A painless guide to CRC error detection algorithms, version 3, 1993
    locator: Sections 10 to 12 (the table-driven implementation, the direct form without augmentation, and the reflected table)
  - url: https://github.com/madler/zlib/blob/master/crc32.c
    title: Mark Adler, zlib, crc32.c
    locator: The byte-wise loop with the reflected table, and the function crc32_combine
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Check values of CRC-8/SMBUS, CRC-16/ARC, CRC-16/IBM-3740, CRC-16/KERMIT, CRC-16/XMODEM, CRC-32/ISO-HDLC, CRC-32/ISCSI, CRC-32/BZIP2, CRC-32/MPEG-2 and CRC-64/XZ
---

A table-driven CRC computes a [cyclic redundancy check](/cyclic-redundancy-check/) one byte at a time. A table of 256 entries holds the effect of each possible byte on the register, so one lookup, one shift and one XOR replace eight bit steps. Dilip Sarwate published the method in 1988. It is the CRC-32 of zlib and of most software that has no special CPU instruction.

## In plain words

The bit-by-bit CRC does a small step for each bit: shift the register, and sometimes add the divisor. Eight such steps for one byte depend only on the top 8 bits of the register and on the byte. There are only 256 possible values for that, so you can do the eight steps in advance for all 256 values and keep the results in a table.

Then, for each byte of the message, you take the top 8 bits of the register, mix in the byte, look up the result in the table, and add it to the rest of the register. That is one lookup for each byte instead of eight steps.

## The problem

The input is a byte string of $n$ bytes and the parameters width $r$, poly, init, refin, refout and xorout of a CRC in the model of Ross Williams, with $r \ge 8$. The output is the same CRC value as the bit-by-bit [cyclic redundancy check](/cyclic-redundancy-check/). The model is the [word RAM](/word-ram/), with $r$ at most the word size.

## The algorithm

The table entry $T[v]$ is the register after the byte $v$ enters an all-zero register, which is $v(x)\, x^r \bmod G(x)$. Here $G(x) = x^r + \text{poly}$.

```pseudo id=main
MAKE-TABLE(r, poly)
L1  for v ← 0 to 255 do
L2      reg ← v · 2^(r − 8)
L3      repeat 8 times: shift reg left by 1 in r bits, XOR poly if the bit shifted out was 1
L4      T[v] ← reg

CRC-TABLE(data, r, poly, init, refin, refout, xorout)
L5  reg ← init
L6  for each byte v of data do
L7      if refin then v ← the 8 bits of v in reverse order
L8      reg ← ((reg · 2^8) AND (2^r − 1)) XOR T[(reg >> (r − 8)) XOR v]
L9  if refout then reg ← the r bits of reg in reverse order
L10 return reg XOR xorout
```

Most CRCs in use have refin and refout true. For them, software keeps the register in reversed bit order. The register then shifts right, the byte goes into the low end, and the table $T'$ is built with the reversed poly. No byte and no result is reversed.

```pseudo id=reflected
CRC-TABLE-REFLECTED(data, r, poly, init, xorout)    ▷ refin = refout = true
L11 reg ← init with its r bits reversed
L12 for each byte v of data do
L13     reg ← (reg >> 8) XOR T′[(reg XOR v) AND 255]
L14 return reg XOR xorout
```

Here $T'[w]$ is $T[\bar w]$ reversed, where $\bar w$ is $w$ reversed. For CRC-32, $T'[1] = \text{0x77073096}$, $T'[128] = \text{0xEDB88320}$ (the reversed poly) and $T'[255] = \text{0x2D02EF8D}$. These are the entries of the table in zlib.

**Init and xorout.** Init sets the start of the register. Xorout changes only the output. To continue a CRC over more data, undo xorout and the output reversal, and use the result as the new register. For CRC-32/ISO-HDLC, init and xorout are both all ones, so `binascii.crc32(b, crc32(a))` equals `crc32(a + b)`.

**Combine.** The CRC of a concatenation $AB$ follows from the two CRCs and the length of $B$, with no access to the data. With $\mathrm{reg}$ the register before refout and xorout, $b$ the number of bits of $B$, and $I$ the init,

$$\mathrm{reg}(AB) = \big((\mathrm{reg}(A) \oplus I)\, x^{b} \oplus \mathrm{reg}(B)\big) \bmod G(x).$$

The power $x^b \bmod G$ takes $O(\log b)$ products modulo $G$ by [binary exponentiation](/binary-exponentiation/). For CRC-32 this is the function `crc32_combine` of zlib. It lets threads compute the CRC of parts of a file in parallel.

## Example

CRC-32/ISO-HDLC of the 9 bytes `123456789` with the reflected form. The register starts at 0xFFFFFFFF.

| byte | index (reg XOR byte) AND 0xFF | $T'$[index] | register after line L13 |
|---|---|---|---|
| `1` (0x31) | 0xCE | 0x7CDCEFB7 | 0x7C231048 |
| `2` (0x32) | 0x7A | 0xB0D09822 | 0xB0ACBB32 |
| `3` (0x33) | 0x01 | 0x77073096 | 0x77B79C2D |
| `4` (0x34) | 0x19 | 0x646BA8C0 | 0x641C1F5C |
| `5` (0x35) | 0x69 | 0x346ED9FC | 0x340AC5E3 |
| `6` (0x36) | 0xD5 | 0xF6B9265B | 0xF68D2C9E |
| `7` (0x37) | 0xA9 | 0xAF0A1B4C | 0xAFFC9660 |
| `8` (0x38) | 0x58 | 0x65B0D9C6 | 0x651F2550 |
| `9` (0x39) | 0x69 | 0x346ED9FC | 0x340BC6D9 |

In the first row, $\text{0xFFFFFFFF} \gg 8 = \text{0x00FFFFFF}$, and its XOR with 0x7CDCEFB7 is 0x7C231048. The last register XOR 0xFFFFFFFF is 0xCBF43926, the check value of the catalogue.

## Correctness

Write the register as $R = R_{\mathrm{high}}\, x^{r-8} + R_{\mathrm{low}}$, where $R_{\mathrm{high}}$ is the top 8 bits. Eight bit steps with the byte $v$ give $(x^8 R + v x^r) \bmod G = \big((R_{\mathrm{high}} + v)\, x^r + x^8 R_{\mathrm{low}}\big) \bmod G$. The term $x^8 R_{\mathrm{low}}$ has degree less than $r$, so it stays as it is, and the remainder of $(R_{\mathrm{high}} + v) x^r$ is a table entry. This is line L8. The reflected form is the same computation with each word reversed. The combine formula follows from the register invariant $(I x^k + M x^r) \bmod G$. The full proof is below.

## Complexity

- **Time.** Line L8 is $O(1)$ word operations, so the CRC of $n$ bytes takes $\Theta(n)$ time and exactly $n$ table lookups. The table takes $256 \times 8$ bit steps, once.
- **Space.** The table has 256 words: 1 KiB for CRC-32, 2 KiB for CRC-64. This does not grow with $n$.
- **Dependency chain.** Each lookup needs the register from the step before. So the speed is limited by the latency of a load and an XOR for each byte, not by the throughput of the CPU. [Slicing-by-8](/slicing-by-8/) breaks this chain.

## Properties

- **Same result as the bit loop**, for each parameter set with $r \ge 8$.
- **Streaming.** The register is the only state, so the data can come in parts.
- **Combinable.** The CRC of $AB$ follows from the CRCs of $A$ and $B$ and the length of $B$.
- **One table for each generator.** The table does not depend on init, refout or xorout, but it depends on poly and on the bit order.

## Variants and improvements

- **Slicing-by-4 and slicing-by-8.** Use 4 or 8 tables and process 4 or 8 bytes per step. See [slicing-by-8](/slicing-by-8/).
- **Half-byte table.** A table of 16 entries and two lookups for each byte. This suits small microcontrollers.
- **Carry-less multiplication.** On CPUs with a carry-less multiply instruction, [CRC folding](/clmul-crc-folding/) is much faster.
- **Hardware instruction.** SSE4.2 has an instruction for [CRC-32C](/crc32c/) only.
- **Widths below 8.** Shift the register to the top of a byte, so that the generator is $G(x)\, x^{8 - r}$, and shift the result back at the end.

## When to use it

Use the table-driven CRC as the default software CRC when there is no carry-less multiply or CRC instruction, or when the messages are short. Use slicing-by-8 for long messages on a CPU with a good cache. Use the bit loop only when 1 KiB of table is too much memory.

## Pitfalls

- **Wrong table for the form.** The table of the left-shifting form and the table of the reflected form are different. A reflected table in a left-shifting loop gives a wrong CRC that still looks random.
- **Shift by $r - 8$.** The index is the top 8 bits of the register, `reg >> (r − 8)`, not `reg >> 24` for each width.
- **Mask.** In a language with wide integers, mask the register to $r$ bits after the shift left.
- **Combine and init.** The combine formula has the term $I$. With init 0 it disappears, and a formula for CRC-32 does not work for a CRC with another init or xorout.

## Implementations

## History

Dilip Sarwate published the method with one table of 256 entries in Communications of the ACM in 1988, and it became the standard software CRC. Ross Williams explained the table method and its reflected form in his 1993 guide. Mark Adler wrote the CRC-32 code of zlib, with `crc32_combine` for the CRC of concatenated parts.

## References
