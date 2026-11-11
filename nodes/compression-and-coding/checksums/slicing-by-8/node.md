---
tag: K8JNYQ
kind: algorithm
slug: slicing-by-8
name: Slicing-by-8 CRC
aliases:
- slicing-by-8 CRC
- slicing-by-n CRC
area: compression-and-coding/checksums
level: advanced
summary: Processes eight bytes per step with eight tables to speed up table-driven CRC.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 2005
  people: [Michael E. Kounavis, Frank L. Berry]
  note: Kounavis and Berry of Intel published slicing-by-4 and slicing-by-8 at the IEEE Symposium on Computers and Communications in 2005.
prereqs: [table-driven-crc]
see_also: [cyclic-redundancy-check, clmul-crc-folding, crc32c, gf2-polynomial-arithmetic, word-ram]
sources:
  - paper: "Michael E. Kounavis and Frank L. Berry, A systematic approach to building high performance software-based CRC generators, Proceedings of the 10th IEEE Symposium on Computers and Communications (ISCC 2005), Cartagena, Spain"
    locator: pp. 855 to 862 (slicing-by-4 and slicing-by-8, the tables for a byte followed by zero bytes, and the lookup counts)
  - paper: "Michael E. Kounavis and Frank L. Berry, Novel table lookup-based algorithms for high-performance CRC generation, IEEE Transactions on Computers 57(11), 2008"
    locator: pp. 1550 to 1560 (the journal version, with slicing-by-N for general N)
  - paper: doi:10.1145/63030.63037
    title: Dilip V. Sarwate, Computation of cyclic redundancy checks via table look-up, Communications of the ACM 31(8), 1988
    locator: pp. 1008 to 1013 (the byte-wise table method that slicing extends)
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Check values of CRC-32/ISO-HDLC (0xCBF43926) and CRC-32/ISCSI (0xE3069283)
---

Slicing-by-8 computes a 32-bit [cyclic redundancy check](/cyclic-redundancy-check/) eight bytes at a time with eight tables of 256 entries. The eight lookups of one step do not depend on each other, so a CPU can do them at the same time. It does the same number of lookups as the [table-driven CRC](/table-driven-crc/), but the chain of dependent steps is eight times shorter. Michael Kounavis and Frank Berry of Intel published slicing-by-4 and slicing-by-8 in 2005.

## In plain words

The byte-at-a-time CRC uses one table. Each step must wait for the step before, because the next lookup needs the new register. A modern CPU could do several lookups at once, but this chain stops it.

Slicing-by-8 takes 8 bytes at once. For each of the 8 bytes it asks a different question: what does this byte do to the register if 7, 6, 5, and so on down to 0 more bytes come after it? There is one table for each of these questions. The 8 answers are independent, so the CPU looks them all up at the same time and adds them together. Only one step in eight waits for the step before.

## The problem

The input is a byte string of $n$ bytes. The output is its CRC for a 32-bit CRC in the reflected form (refin and refout true), with init and xorout all ones. CRC-32/ISO-HDLC (the CRC-32 of zip and Ethernet) and [CRC-32C](/crc32c/) have this form. The model is the [word RAM](/word-ram/) with words of at least 32 bits.

## The algorithm

Table $T_k$ holds the effect of a byte followed by $k$ zero bytes. $T_0$ is the table of the table-driven CRC. Each next table is one more byte step with input 0.

```pseudo id=main
MAKE-TABLES(poly)
L1  T₀ ← the reflected byte table of poly          ▷ as in the table-driven CRC
L2  for k ← 1 to 7 do
L3      for v ← 0 to 255 do T_k[v] ← (T_{k−1}[v] >> 8) XOR T₀[T_{k−1}[v] AND 255]

SLICING-BY-8(data)
L4  reg ← 0xFFFFFFFF
L5  for each block of 8 bytes d₀ … d₇ of data do
L6      c ← reg XOR (d₀ + 2⁸ d₁ + 2¹⁶ d₂ + 2²⁴ d₃)      ▷ a 32-bit little-endian load
L7      let c₀ … c₃ be the bytes of c, low byte first
L8      reg ← T₇[c₀] ⊕ T₆[c₁] ⊕ T₅[c₂] ⊕ T₄[c₃] ⊕ T₃[d₄] ⊕ T₂[d₅] ⊕ T₁[d₆] ⊕ T₀[d₇]
L9  process the last n mod 8 bytes with the byte-wise step and T₀
L10 return reg XOR 0xFFFFFFFF
```

The first 4 bytes of a block are XORed into the register, because they meet the register bits directly. The last 4 bytes meet nothing yet, so they go into their tables as they are. Byte $d_0$ is followed by 7 more bytes in the block, so it uses $T_7$, and so on.

Slicing-by-4 is the same with blocks of 4 bytes: `c ← reg XOR (4 bytes)`, then `reg ← T₃[c₀] ⊕ T₂[c₁] ⊕ T₁[c₂] ⊕ T₀[c₃]`. It uses 4 tables.

## Example

CRC-32/ISO-HDLC of the first block `12345678`. The register is 0xFFFFFFFF. The little-endian load of `1234` is 0x34333231, so $c$ = 0xCBCCCDCE, with bytes $c_0, \ldots, c_3$ = 0xCE, 0xCD, 0xCC, 0xCB. The other bytes are $d_4, \ldots, d_7$ = 0x35, 0x36, 0x37, 0x38.

| lookup | value |
|---|---|
| $T_7$[0xCE] | 0x6F2C5505 |
| $T_6$[0xCD] | 0xADCAFE4B |
| $T_5$[0xCC] | 0x662ADECF |
| $T_4$[0xCB] | 0x9EC5D9CA |
| $T_3$[0x35] | 0xC7F50893 |
| $T_2$[0x36] | 0x20E69922 |
| $T_1$[0x37] | 0x9007A034 |
| $T_0$[0x38] | 0x2802B89E |
| XOR of all | 0x651F2550 |

This is the same register as after the eighth byte in the trace of the [table-driven CRC](/table-driven-crc/). The ninth byte `9` goes through line L9: the register becomes 0x340BC6D9, and the CRC is 0x340BC6D9 XOR 0xFFFFFFFF = 0xCBF43926, the check value.

## Correctness

In the normal domain the register after a block $D$ of 64 bits is $(R x^{64} + D x^{32}) \bmod G$. The first 4 bytes of $D$ and the register both are multiplied by $x^{64}$, so they are XORed first. Then each byte $c_j$ of the sum is a term $c_j x^{32 + 8(7-j)}$, and each of the last 4 bytes is a term $d_j x^{32 + 8(7-j)}$. The table $T_k$ holds $v\, x^{32 + 8k} \bmod G$, and the remainder of a sum is the sum of the remainders. The reflected form is the same computation with each word reversed. The full proof is below.

## Complexity

The count of operations does not change, but their order does. The implementation counts table lookups and dependent register updates. For 1003 bytes:

| method | tables | table size | lookups | dependent updates |
|---|---|---|---|---|
| byte-wise (Sarwate) | 1 | 1 KiB | 1003 | 1003 |
| slicing-by-4 | 4 | 4 KiB | 1003 | 253 |
| slicing-by-8 | 8 | 8 KiB | 1003 | 128 |

- **Time.** $\Theta(n)$ in each case, with exactly $n$ lookups.
- **Dependency chain.** $\lfloor n/8 \rfloor + (n \bmod 8)$ register updates, each of which waits for the one before. In the byte-wise method there are $n$. On a CPU that can issue several loads in one cycle, this is the reason for the speed gain.
- **Space.** 8 tables of 256 entries of 4 bytes, 8 KiB in total. This does not grow with $n$, but it must stay in the L1 cache to be fast.

This page reports operation counts and not timings, because timings in Python do not show the effect of the chain.

## Properties

- **Same CRC** as the bit loop and the byte-wise table, for each length.
- **Tables are fixed** for a generator. They do not depend on the data.
- **Little-endian load.** The 4-byte load of line L6 matches the reflected register directly. A big-endian CPU needs a byte swap or tables in the other byte order.
- **Streaming.** The register is the only state, so data can come in parts, with any part length.

## Variants and improvements

- **Slicing-by-N.** The journal version of Kounavis and Berry (2008) gives the method for other $N$. Slicing-by-16 uses 16 KiB of tables.
- **Normal form.** For CRCs that are not reflected, use a big-endian load and the normal tables.
- **Braiding.** zlib since version 1.2.12 computes several CRCs on interleaved words and combines them, with a different table layout.
- **Hardware.** On x86 with SSE4.2, [CRC-32C](/crc32c/) has its own instruction. With a carry-less multiply, [CRC folding](/clmul-crc-folding/) is faster than any table method for long messages.

## When to use it

Use slicing-by-8 for long messages on a CPU with no CRC instruction and no carry-less multiply. For short messages the table-driven CRC is as fast and uses less cache. In a program that also needs the cache for other work, 8 KiB of tables can slow the rest of the program.

## Pitfalls

- **Wrong table order.** Byte $d_0$ is the furthest from the end of the block, so it uses $T_7$. A reversed table order gives a wrong CRC.
- **Byte order of the load.** Line L6 needs a little-endian load. On a big-endian CPU the same code gives a wrong result.
- **Alignment.** Real code processes the first bytes one at a time until the pointer is aligned to 8 bytes. The tail of fewer than 8 bytes goes through line L9.
- **Benchmarks.** A small benchmark keeps the tables in the cache. In a real program the tables can be cold, and the gain is smaller.

## Implementations

## History

Dilip Sarwate published the one-table method in 1988. Michael Kounavis and Frank Berry of Intel published slicing-by-4 and slicing-by-8 at ISCC in 2005, and a journal version with general $N$ in IEEE Transactions on Computers in 2008. Many libraries took over slicing-by-8 for CRC-32 and CRC-32C before carry-less multiply and CRC instructions became common.

## References
