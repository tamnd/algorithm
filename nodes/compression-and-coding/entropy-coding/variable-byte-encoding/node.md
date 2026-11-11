---
tag: JRS6JT
kind: algorithm
slug: variable-byte-encoding
name: Variable-byte encoding
aliases:
- VByte
- varint
- LEB128
- base 128 varint
area: compression-and-coding/entropy-coding
level: intro
summary: Splits an integer into 7-bit groups, one per byte, and uses the eighth bit to mark whether more bytes follow. Byte-aligned and fast; LEB128 and protobuf varints are this code.
model: word-ram
complexity:
  vars: {x: the integer to code, n: the count of integers}
  time: {worst: Θ(1 + log(x + 1)), average: Θ(1 + log(x + 1)), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1972
  people: [Larry H. Thiel, H. S. Heaps]
  note: The survey of Pibiri and Venturini credits Thiel and Heaps with the first description; DWARF 2 later named the LEB128 form, and protobuf made the varint widely known.
prereqs: [bitwise-operations, twos-complement]
see_also: [elias-gamma-coding, exp-golomb-coding, pfor-delta, delta-encoding, universal-code, rice-coding, simd-within-a-register, bit-packing]
sources:
  - url: https://dwarfstd.org/doc/DWARF5.pdf
    title: DWARF Debugging Information Format, Version 5, DWARF Standards Committee, 2017
    locator: Section 7.6, Variable Length Data, with Table 7.7 (unsigned LEB128 examples) and Table 7.8 (signed LEB128 examples)
  - url: https://protobuf.dev/programming-guides/encoding/
    title: Protocol Buffers Documentation, Encoding
    locator: sections Base 128 Varints and Signed Integers (ZigZag)
  - url: https://webassembly.github.io/spec/core/binary/values.html
    title: WebAssembly Core Specification, Binary Format, Values
    locator: section Integers (LEB128, at most ceil(N/7) bytes for an N-bit integer)
  - paper: doi:10.1016/j.ipl.2017.09.011
    title: Daniel Lemire, Nathan Kurz and Christoph Rupp, Stream VByte, faster byte-oriented integer compression, Information Processing Letters 130, 2018
    locator: pp. 1 to 6, Figure 3 (control and data streams), and the review of VByte, Varint-GB, Varint-G8IU and Masked VByte (arXiv:1709.08990)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.9, Variable-Byte (arXiv:1908.10598v2)
---

Variable-byte encoding (VByte) writes a non-negative integer as a sequence of bytes. Each byte holds 7 bits of the number in its low bits and a flag in its top bit that tells whether more bytes follow. Small numbers take one byte, and a number $x$ takes $\lceil (\lfloor \log x \rfloor + 1)/7 \rceil$ bytes. Every codeword is a whole number of bytes, so the decoder needs no bit shifting across byte borders and runs fast. The little-endian form with the flag set on all but the last byte is LEB128, which DWARF, WebAssembly and the protobuf varint use. A signed value goes in as two's complement (signed LEB128) or after a ZigZag map to an unsigned value.

## In plain words

Cut the number into pieces of 7 binary digits, starting from the low end. Each piece goes into one byte, which has 8 bits, so one bit is left over. Use that bit as a flag: 1 means "another byte follows", 0 means "this is the last byte".

A number below 128 fits in one byte. A number below 16384 fits in two, and so on. The reader takes bytes one by one, keeps the 7 data bits of each, and stops at the byte whose flag is 0.

The code wastes one bit in eight, and a number never takes less than a byte. In exchange it is very simple and very fast, because a computer handles whole bytes at no extra cost.

## The problem

The input is a sequence of $n$ non-negative integers, often small: field values in a serialized record, lengths and offsets in debug data, or gaps between document numbers in a posting list. The task is a self-delimiting code that is short for small values, has no upper limit on the value, and decodes with as few operations as possible. Bit-level codes such as the [Elias gamma code](/elias-gamma-coding/) are shorter, but each codeword starts at an arbitrary bit position, which costs shifts and masks.

Notation: $x$ is the integer to code, $\ell(x)$ is its codeword length, $n$ is the count of integers, and logarithms are base 2. The byte values are in hexadecimal.

## The algorithm

```pseudo id=main
VBYTE-ENCODE(x, out)                       ▷ x ≥ 0; unsigned LEB128
L1  repeat
L2      b ← x mod 128; x ← ⌊x / 128⌋       ▷ the low 7 bits, then shift
L3      if x ≠ 0 then b ← b + 128          ▷ set the flag: more bytes follow
L4      append byte b to out
L5  until x = 0

VBYTE-DECODE(in)
L6  x ← 0; s ← 0
L7  repeat
L8      b ← the next byte of in
L9      x ← x + (b mod 128) · 2^s; s ← s + 7
L10 until b < 128                          ▷ flag clear: this was the last byte
L11 return x
```

The encoder writes the low group first. Line L3 sets the top bit on every byte except the last, so the decoder of line L10 knows where the value ends without a length field. Line L9 puts each group in its place, 7 bits above the one before.

**Two flag conventions.** The flag can mean "more bytes follow" or "this is the last byte".

- *Continuation flag* (this page): the top bit is 1 on every byte except the last. LEB128, the protobuf varint, the MIDI variable-length quantity, and the survey of Pibiri and Venturini use it. A byte below 128 is a complete small value.
- *Stop flag*: the top bit is 1 only on the last byte, and the other bytes are below 128. Some inverted index codecs use it.

The two give codes of the same length; they differ only in which bit value is tested on line L10. The group order also varies: LEB128 and protobuf put the low group first; the MIDI variable-length quantity puts the high group first.

**Signed values.**

- *Signed LEB128* (DWARF 5, Section 7.6) writes the two's complement form in 7-bit groups and stops when the rest of the number is all zeros or all ones and bit 6 of the last byte equals the sign. The decoder sign-extends from bit 6 of the last byte. So $-2$ is `7e` and $127$ is `ff 00`.
- *ZigZag* (protobuf `sint32` and `sint64`) maps $v \mapsto 2v$ for $v \ge 0$ and $v \mapsto -2v - 1$ for $v < 0$, so $0, -1, 1, -2, 2$ become $0, 1, 2, 3, 4$. In 64-bit code it is `(v << 1) ^ (v >> 63)` with an arithmetic shift. The result goes to the unsigned code. Without it, protobuf writes a negative `int64` as a 64-bit two's complement value in 10 bytes.

**Stream VByte.** A decoder of plain VByte must test one flag per byte, which leads to branch mispredictions on mixed lengths. Stream VByte (Lemire, Kurz and Rupp, 2018) codes 32-bit integers in groups of four. A control byte holds four 2-bit codes, each the byte length of one integer minus 1, with the first integer in the low bits. The integers themselves go, in little-endian order and with no flags, into a separate data stream. The decoder reads one control byte, looks up a shuffle mask in a 256-entry table, and moves the four integers into place with one SIMD shuffle.

## Example

Encode $x = 624485$, binary `10011000011101100101`:

| step | $x$ before | $b = x \bmod 128$ | $x$ after | byte written |
|---|---|---|---|---|
| 1 | 624485 | `1100101` = 65 | 4878 | 65 + 80 = `e5` |
| 2 | 4878 | `0001110` = 0e | 38 | 0e + 80 = `8e` |
| 3 | 38 | `0100110` = 26 | 0 | `26` |

The code is `e5 8e 26`. The decoder reads `e5` (flag set, $x = 65$), `8e` (flag set, $x = 65 + 0e \cdot 2^7$), and `26` (flag clear, $x = \ldots + 26 \cdot 2^{14} = 624485$).

Other values:

| value | code | source |
|---|---|---|
| 2 | `02` | DWARF 5, Table 7.7 |
| 127 | `7f` | DWARF 5, Table 7.7 |
| 128 | `80 01` | DWARF 5, Table 7.7 |
| 150 | `96 01` | protobuf encoding guide |
| 12857 | `b9 64` | DWARF 5, Table 7.7 |
| signed $-128$ | `80 7f` | DWARF 5, Table 7.8 |
| signed $-123456$ | `c0 bb 78` | |

Stream VByte on $1024, 12, 10, 2^{30}, 1, 2, 3, 1024$ (Figure 3 of the paper): the byte lengths are $2, 1, 1, 4$ and $1, 1, 1, 2$, so the control bytes are `c1` and `40`, and the data stream is the 13 bytes `00 04 0c 0a 00 00 00 40 01 02 03 00 04`.

## Correctness

Write $x = \sum_{i=0}^{m-1} g_i 2^{7i}$ with $0 \le g_i < 128$ and $g_{m-1} \ne 0$ (or $m = 1$ for $x = 0$). Round $i$ of lines L1 to L5 writes $g_i$, with the flag set exactly when $i < m - 1$, because $x$ is still nonzero after the shift exactly then. The decoder keeps the invariant that after $i$ bytes, $x = \sum_{j < i} g_j 2^{7j}$ and $s = 7i$. It stops at the first byte with a clear flag, which is byte $m$, and returns the full sum. Because the end of each codeword is marked by its own last byte, no codeword is a prefix of another, and a stream of codewords decodes in one way. The full proof is in the proof file.

## Complexity

**Length.** $\ell(x) = 8 \lceil (\lfloor \log x \rfloor + 1)/7 \rceil$ bits for $x \ge 1$, and 8 bits for $x = 0$. A 32-bit value takes 1 to 5 bytes, and a 64-bit value takes 1 to 10 bytes. For large $x$ this is about $\tfrac87 \log x$, so VByte is a [universal code](/universal-code/) but not an asymptotically optimal one.

**Time.** Encoding and decoding take $\Theta(\ell(x)/8)$ byte steps, $\Theta(1 + \log(x + 1))$. On a [word RAM](/word-ram/) with values that fit in a word this is at most $\lceil w/7 \rceil$ steps. A list of $n$ values takes $\Theta(n + \sum \log(x_i + 1))$ time.

**Space.** $\Theta(1)$ beyond the input and output. Stream VByte uses a 256-entry table of shuffle masks.

## Properties

- **Byte-aligned.** Every codeword starts on a byte border, so a decoder can skip a value by scanning for a byte below 128, and the code works with byte-level tools such as general-purpose compressors.
- **Self-synchronizing at byte level.** In the continuation form, every byte below 128 ends a codeword. A decoder that starts in the middle of a stream finds the start of the next codeword after at most $\ell(x)/8$ bytes.
- **Not unique without a rule.** The bytes `80 00` also decode to 0. LEB128 does not forbid such padded forms; WebAssembly limits the length to $\lceil N/7 \rceil$ bytes for an $N$-bit integer, and protobuf limits it to 10 bytes.
- **At least 8 bits per value.** On data where most values are 0 or 1, a bit-level code such as [Elias gamma](/elias-gamma-coding/) or [Rice](/rice-coding/) is several times shorter.

## Variants and improvements

- **Varint-GB.** Group varint, used at Google, codes four 32-bit integers with one leading byte of four 2-bit lengths, then the integers in place. Stream VByte separates the length bytes into their own stream, which lets the decoder load them ahead.
- **Varint-G8IU.** Stepanov and others (CIKM 2011) pack as many whole integers as fit into 8 data bytes, with a descriptor byte that marks the last byte of each integer. A SIMD shuffle decodes each 8-byte block.
- **Masked VByte.** Plaisance, Kurz and Lemire (2015) keep the plain VByte format and decode it with SIMD: they gather the flag bits of 16 bytes into a mask with one instruction and look the mask up in a table of shuffles. Old VByte data decodes fast with no change of format.
- **Stream VByte.** Separate control and data streams and 2-bit lengths per 32-bit integer, as above. In its authors' tests it decodes faster than the earlier byte codes.
- **Delta coding first.** Posting lists store the gaps between sorted document numbers, and [delta encoding](/delta-encoding/) before VByte keeps most gaps below 128. Stream VByte has a variant that does the delta and the prefix sum inside the codec.

## When to use it

Use VByte for small integers in byte-oriented formats: serialization (protobuf), debug information (DWARF), bytecode (WebAssembly), and posting lists where decode speed matters more than size. For posting lists with many tiny gaps, [PForDelta](/pfor-delta/) or binary packing in blocks gives smaller output at a similar speed, and [Elias-Fano encoding](/elias-fano-encoding/) gives random access. For video or audio syntax, where each bit counts, use a bit-level code such as [exp-Golomb](/exp-golomb-coding/) or [Rice](/rice-coding/).

## Pitfalls

- **Testing the flag with the wrong value.** In the continuation form, line L10 stops when $b < 128$. A decoder that stops when $b \ge 128$, the stop-flag form, reads continuation streams wrongly from the first multi-byte value. Fix the convention in the format.
- **Missing length limit.** Line L8 must stop after at most $\lceil N/7 \rceil$ bytes for an $N$-bit target (10 for 64 bits). Without the limit, a hostile stream of `80` bytes makes line L9 shift past the word size, which is undefined behavior in C and a slow bignum in other languages.
- **Signed values without ZigZag.** Passing a negative 64-bit value to line L1 as unsigned writes its two's complement form, which takes 10 bytes even for $-1$. Use signed LEB128 or ZigZag before line L1.
- **Signed LEB128 stop test.** The encoder must stop only when the rest is 0 and bit 6 of the byte is 0, or the rest is $-1$ and bit 6 is 1. Stopping when the rest is 0 alone codes 64 as `40`, which a signed decoder reads as $-64$; the right code is `c0 00`.
- **Logical shift in ZigZag.** `(v << 1) ^ (v >> 63)` needs an arithmetic right shift. With a logical shift, every negative $v$ maps to a wrong value.

## Implementations

## History

Byte-aligned codes with a continuation bit are old. The survey of Pibiri and Venturini credits the first description to Thiel and Heaps (1972), in a program design for searches on large databases. The MIDI file format codes delta times as variable-length quantities with the high group first. The DWARF 2 debugging format (1993) defined LEB128, "Little-Endian Base 128", in unsigned and signed forms, and later versions keep it. In information retrieval, Williams and Zobel (1999) and Scholer, Williams, Yiannis and Zobel (SIGIR 2002) showed that byte-aligned codes decode posting lists faster than bit-level codes at a moderate cost in size. Google's protocol buffers made the varint and ZigZag widely known. SIMD decoders followed: Varint-G8IU (Stepanov and others, 2011), Masked VByte (Plaisance, Kurz and Lemire, 2015) and Stream VByte (Lemire, Kurz and Rupp, 2018).

## References
