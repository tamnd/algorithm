---
tag: 34ZTAK
kind: algorithm
slug: lzo
name: LZO
aliases:
- Lempel-Ziv-Oberhumer
- LZO1X
- LZO-RLE
area: compression-and-coding/dictionary-compression
level: advanced
summary: "Oberhumer's byte-oriented LZ77 formats, built for very fast decompression with no extra memory. This page covers the LZO1X stream and its LZO-RLE version."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1996
  people: [Markus F. X. J. Oberhumer]
  note: Oberhumer posted LZO1 and LZO1A in March 1996, the first public release of the library (0.10) is dated 20 May 1996, and LZO1X came in version 0.20 of 11 August 1996. Linux added the LZO-RLE version in 2018.
prereqs: [lz77, back-reference]
see_also: [lz4, snappy, deflate, lzss, match-finding, greedy-parsing, optimal-parsing, run-length-encoding]
sources:
  - url: https://www.oberhumer.com/opensource/lzo/
    title: Markus F. X. J. Oberhumer, LZO real-time data compression library, version 2.10 (01 Mar 2017)
    locator: doc/LZO.TXT, sections Introduction, Design criteria, Performance, Short documentation and The algorithms; doc/NEWS, the entries for 0.10 (20 May 1996) and 0.20 (11 Aug 1996); doc/LZO.FAQ, the list of LZO1X decompressors
  - url: https://github.com/torvalds/linux/blob/master/Documentation/staging/lzo.rst
    title: Willy Tarreau and Dave Rodgman, LZO stream format as understood by Linux's LZO decompressor
    locator: sections Description, Versions and Byte sequences (first byte encoding and instruction encoding)
  - url: https://github.com/torvalds/linux/blob/master/lib/lzo/lzo1x_decompress_safe.c
    title: Linux kernel, lib/lzo/lzo1x_decompress_safe.c
    locator: the function lzo1x_decompress_safe, in particular the version test, the zero run case and the label eof_found
  - url: https://github.com/torvalds/linux/blob/master/lib/lzo/lzo1x_compress.c
    title: Linux kernel, lib/lzo/lzo1x_compress.c
    locator: the functions lzo1x_1_do_compress (the encodings of the matches, the zero runs and the length cap 261 to 264) and lzogeneric1x_1_compress (the first literal run and the end marker)
  - url: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Oberhumer
    title: Wikipedia, Lempel-Ziv-Oberhumer
    locator: sections Design and Implementations (the programs and Linux subsystems that use LZO)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

LZO is a family of compressed data formats and a library by Markus Oberhumer that code an [LZ77](/lz77/) parse with whole bytes and no entropy coder. The library has many algorithms (LZO1, LZO1A, LZO1B, LZO1C, LZO1F, LZO1X, LZO1Y, LZO1Z and LZO2A); its own notes say that LZO1X "is often the best choice of all", and LZO1X is the one that Linux and most programs use. An LZO1X stream is a list of instructions. Each copy instruction holds a length, a distance (a [back-reference](/back-reference/)) and a count of 0 to 3 literal bytes that come after it. The decoder needs no memory except the input and the output. This page covers the LZO1X stream, in the original version 0 and the LZO-RLE version 1 of Linux. It does not cover the other LZO algorithms or the lzop file format.

## In plain words

The decoder reads one instruction byte at a time. Most instructions say "go back this far in what you already wrote, copy this many bytes, then copy up to three new bytes from the input". The high bits of the byte choose the kind of copy: short copies from near, or long copies from far. Some kinds need one more byte for the distance, others need two.

Long lengths are written as a run of zero bytes, each worth 255, then one more byte. Literal runs of four bytes or more have their own instruction. Because a short literal run hides in two spare bits of the copy before it, the meaning of a small instruction byte depends on what came just before it. A special copy from a far distance marks the end of the stream.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case, with no probability model. There is no public specification of LZO1X. The Linux document lzo.rst says: "This is not a specification." The format is what the decoders of the LZO library and of Linux accept. Oberhumer writes that he first wrote each decompressor, "thereby defining the compressed data format". So this page describes the stream that lzo1x_decompress_safe accepts. It checks the description against both decoders.

### Lengths

Several fields hold a length in the low $b$ bits of the instruction byte. We write LEN$(t, b)$ for the value of such a field. If $v = t \bmod 2^b$ is not 0, the value is $v$. If $v = 0$, then $z \ge 0$ zero bytes and one byte $c \ne 0$ follow, and the value is $2^b - 1 + 255 z + c$. So a zero byte adds 255 to the length.

### The instructions

The decoder keeps a *state*: 0 if the last instruction copied no literals, 1 to 3 if it copied that many, and 4 after a literal run of 4 bytes or more. $S$ is the literal count of a copy, and LE16 is a 16-bit little-endian word that follows the instruction byte.

| byte $t$ | state | meaning | bytes after $t$ | length $\ell$ | distance $d$ | $S$ |
|---|---|---|---|---|---|---|
| 0000LLLL | 0 | literal run | LEN extension, then $\ell$ bytes | 3 + LEN$(t, 4)$ | none | 0, state 4 |
| 0000DDSS | 1 to 3 | short copy | byte $H$ | 2 | $4H + D + 1$, up to 1024 | SS |
| 0000DDSS | 4 | short far copy | byte $H$ | 3 | $4H + D + 2049$, 2049 to 3072 | SS |
| 01LDDDSS, 1LLDDDSS | any | M2 copy | byte $H$ | $\lfloor t/32 \rfloor + 1$, 3 to 8 | $8H + D + 1$, up to 2048 | SS |
| 001LLLLL | any | M3 copy | LEN extension, LE16 $w$ | 2 + LEN$(t, 5)$ | $\lfloor w/4 \rfloor + 1$, up to 16384 | $w \bmod 4$ |
| 0001HLLL | any | M4 copy | LEN extension, LE16 $w$ | 2 + LEN$(t, 3)$ | $16384 + 16384 H + \lfloor w/4 \rfloor$, 16385 to 49151 | $w \bmod 4$ |

After each copy, the decoder copies $S$ literal bytes and sets the state to $S$. An M4 copy with $H = 0$ and $\lfloor w/4 \rfloor = 0$ would have distance 16384. That value ends the stream; the decoder then requires length 3, so the end marker is the bytes 11 00 00.

### The first byte

There is no output before the first instruction, so the first byte has its own rule. A value of 18 to 255 copies $t - 17$ literal bytes and sets the state to $t - 17$ if that is below 4, else to 4. A value of 0 to 15 is a normal literal run with state 0.

### Version 1: LZO-RLE

Linux added a version for data with many zero bytes, which lzo.rst calls "a common case for zram". If a stream of 5 bytes or more starts with 17, the next byte is the version. Version 0 never starts that way, except the empty stream 11 00 00, which has only 3 bytes. In version 1, an M4 byte 00011LLL whose LE16 has all 14 distance bits set (distance 49151) is a zero run. A fourth byte $X$ follows, and the run length is $8X + \mathrm{LLL} + 4$, 4 to 2051. So a version 1 encoder must not write the distance 49151. It must also not write a long M4 copy that the decoder would read as a zero run (see Pitfalls).

## The algorithm

The decoder:

```pseudo id=main
LZO1X-DECODE(s)
L1  if |s| ≥ 5 and s[0] = 17 then v ← s[1] and skip 2 bytes, else v ← 0; then apply the first byte rule
L2  loop
L3      t ← the next byte
L4      if t < 16 and state = 0 then
L5          append the next 3 + LEN(t, 4) bytes to out; state ← 4; go to L2
L6      else if t < 16 and state < 4 then ℓ ← 2; d ← 1 + ⌊t/4⌋ + 4·(next byte); S ← t mod 4
L7      else if t < 16 then ℓ ← 3; d ← 2049 + ⌊t/4⌋ + 4·(next byte); S ← t mod 4
L8      else if t ≥ 64 then ℓ ← ⌊t/32⌋ + 1; d ← 1 + (⌊t/4⌋ mod 8) + 8·(next byte); S ← t mod 4
L9      else if t ≥ 32 then ℓ ← 2 + LEN(t, 5); w ← next LE16; d ← 1 + ⌊w/4⌋; S ← w mod 4
L10     else if v ≠ 0 and ⌊t/8⌋ = 3 and the next LE16 w has ⌊w/4⌋ = 16383 then append 8·(byte after w) + (t mod 8) + 4 zero bytes; S ← w mod 4; go to L14
L11     else ℓ ← 2 + LEN(t, 3); w ← next LE16; d ← 2048·(t AND 8) + ⌊w/4⌋; S ← w mod 4
L12         if d = 0 then return out if ℓ = 3 and s is used up, else fail; d ← d + 16384
L13     if d > |out| then fail; repeat ℓ times: append out[|out| − d]
L14     append the next S bytes to out; state ← S
```

Each read fails if the input ends. Line L10 looks at the two bytes after $t$ before it reads the LEN extension, as the Linux decoder does. Line L13 copies byte by byte, so a copy with $d < \ell$ repeats the last $d$ bytes.

The encoder is free. Ours is a [greedy parse](/greedy-parsing/) in the style of the LZO1X-1 compressor of Linux:

1. Keep a table from each 4-byte string to the last position where it started. At position $p$, look up $x[p \ldots p+3]$. If the table has a position $c$ with $p - c$ at most 49151 (49150 in version 1), extend the match as far as it goes and write it. Else store $p$ and move to $p + 1$.
2. Write a match with the smallest kind that holds it: M2 if $\ell \le 8$ and $d \le 2048$, else M3 if $d \le 16384$, else M4. All our matches have $\ell \ge 4$, so every copy byte is 16 or more and its meaning does not depend on the state. We never write the two state-dependent short copies.
3. Before a match, write the pending literals. The first run uses the first byte rule (18 to 255) if it has at most 238 bytes. Later, a run of 1 to 3 bytes goes into the two $S$ bits of the copy before it, and a longer run gets its own instruction.
4. In version 1, at a position $p > 0$ with 4 zero bytes, write a zero run of up to 2051 bytes. Cut an M4 copy to length 260 when it would be read as a zero run.
5. At the end, write the last literals and 11 00 00.

## Example

Compress $x$ = `hello hello hello hello` followed by a newline (24 bytes). Our encoder writes 14 bytes, the same bytes as lzo1x_999_compress of LZO 2.10:

| bytes | instruction | output so far |
|---|---|---|
| 17, then `hello ` | first byte 23: 23 − 17 = 6 literals, state 4 | `hello ` |
| 2F 15 00 | M3: 2F = 001 01111, $\ell = 2 + 15 = 17$; $w$ = 0015, $d = 5 + 1 = 6$, $S = 1$ | `hello hello hello hello` |
| 0A | the $S = 1$ literal | `hello hello hello hello` and a newline |
| 11 00 00 | 0001 0 001: $\ell = 3$, $d$ field 0: end | |

The M3 copy reads from 6 bytes back and writes 17 bytes, so it reads bytes that it wrote itself. For 64 bytes `a`, lzo1x_999_compress writes 12 61 20 1E 00 00 11 00 00: one literal, then an M3 copy whose length field is 0, so a LEN extension of one byte follows (1E = 30, length 2 + 31 + 30 = 63), at distance 1.

In version 1, our encoder writes ten zero bytes as 11 01 12 00 1D FC FF 00 11 00 00: the version, one literal 00, a zero run (1D = 00011 101, $w$ = FFFC, $X = 0$, so $8 \cdot 0 + 5 + 4 = 9$ zero bytes) and the end marker. The literal comes first because a zero run cannot be the first instruction: the first byte rule would read 1D as a run of 12 literals.

## Correctness

The decoder of lines L1 to L14 inverts the encoder above. Each encoder field has a fixed place and width, and the table above maps it back to the length and distance. An extension of $z$ zero bytes and a byte $c$ gives back $255 z + c$. The encoder writes a short literal run into the $S$ bits only after a copy, so the state that the decoder keeps is the state that the encoder assumed, and the encoder writes a byte below 16 only for a literal run in state 0. In version 1, the distance limit and the length cap make sure that line L10 sees no copy that the encoder wrote. A copy is written only when the bytes match, and then by induction the byte copy of line L13 gives the right bytes, also when they overlap. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each instruction reads at least one byte and costs $O(1)$ plus the bytes it reads and writes. So the time is $\Theta(n + m)$. The decoder needs no tables and no memory beyond the output: LZO.TXT says that decompression "requires no memory".
- **Encoding.** Each position needs at most one lookup in the [hash table](/hash-table/), $O(1)$ expected time, and a match of length $\ell$ costs $O(\ell)$ to extend. So the time is $O(n)$ expected. Our table has one entry per distinct 4-byte string. LZO.TXT gives 64 KiB of memory for the fast compressors, and 8 KiB for the level LZO1X-1(11).
- **Size.** On data with no match, our version 0 encoder writes one literal run, and the output has at most $n + \lceil n/255 \rceil + 4$ bytes. LZO.TXT says that its own compressors expand data with no match by at most 64 bytes per 1024 bytes.

## Properties

- **Byte aligned.** Each instruction starts at a byte, so the decoder needs no bit buffer.
- **No entropy coding.** A literal byte costs 8 bits. On text, LZO1X is larger than [DEFLATE](/deflate/).
- **Window.** The farthest copy is 49151 bytes back (49150 in version 1).
- **No header.** The stream does not store $n$ or a checksum. The caller gives the size of the output buffer, and the lzop program adds a header and checksums.
- **Asymmetric levels.** The levels of the library change only the encoder. LZO1X-999 searches almost optimally and is slow, and its output uses the same decoder.

## Variants and improvements

- **The other LZO algorithms.** LZO1, LZO1A, LZO1B, LZO1C, LZO1F, LZO1Y, LZO1Z and LZO2A are different formats in the same library. LZO.TXT says that LZO1Y and LZO1Z "are almost identical to LZO1X".
- **Compression levels.** LZO1X-1 is a greedy parse with one candidate per hash slot, like ours. LZO1X-999 is close to an [optimal parse](/optimal-parsing/). Both give streams for the same decoder.
- **LZO-RLE.** Version 1 adds the zero runs above. Linux offers it as the separate compressor name lzo-rle.
- **Related formats.** [LZ4](/lz4/) and [Snappy](/snappy/) have the same aim: no entropy coder and a fast byte decoder.

## When to use it

Use LZO when decompression speed and a small decoder matter more than size. Examples are boot images, swap pages in memory, and file systems. LZO.TXT gives figures for the Calgary Corpus in blocks of 256 KiB, measured "on an ancient Intel Pentium 133". There, LZO1X-1 leaves 49.4% of the input, compresses at about 4992 and decompresses at about 15585 thousand bytes per second. LZO1X-999 leaves 38.0%, at 136 and 16548 thousand bytes per second. These are old numbers on an old machine, so use them only to compare the levels. Wikipedia lists uses in the Linux kernel (btrfs, SquashFS, initramfs, zram and zswap), the lzop program and OpenVPN. For new designs, [LZ4](/lz4/) or [Zstandard](/zstandard/) at a low level are the usual choices.

## Pitfalls

- **State-dependent bytes.** A byte below 16 means a literal run, a short copy or a short far copy, depending on the state. A decoder that forgets to update the state after a literal run reads the wrong instruction.
- **Version 1 ambiguity.** In version 1, an M4 copy at distance 49151 reads as a zero run. A long M4 copy with $H = 1$ also does, if its one extension byte is 252 to 255 (length 261 to 264), the low 6 bits of its distance field are all 1 and $S = 3$. The Linux encoder limits the distance to 49150 and cuts such a copy to 260 bytes. Our encoder does the same, and a test shows that the uncut stream decodes wrongly.
- **Version 0 decoders.** The library LZO 2.10 does not know version 1. It reads 11 01 as an M4 copy and fails. So send LZO-RLE data only to a decoder that knows it.
- **Long extensions.** Each zero byte adds 255 to a length. In C the sum can overflow; the Linux decoder limits the count of zero bytes (MAX_255_COUNT) for this reason.
- **The unchecked decoder.** The library's lzo1x_decompress does no checks and, in the words of LZO.FAQ, "will probably crash your application" on corrupt data. Use lzo1x_decompress_safe on data you do not trust, and a checksum to detect changes.
- **End of stream.** Line L12 must require $\ell = 3$ and the end of the input. The Linux decoder returns a separate error when bytes are left over.

## Implementations

## History

Markus Oberhumer posted LZO1 and LZO1A to the newsgroups comp.compression and comp.compression.research in March 1996. The first public release of the library, 0.10 of 20 May 1996, had LZO1 to LZO1C. Version 0.20 of 11 August 1996 added LZO1X with the levels LZO1X-1 and LZO1X-999. The current version, 2.10, is dated 1 March 2017. The Linux kernel has its own copy of the LZO1X code. Willy Tarreau wrote down its stream format in 2014 during an analysis of the decoder, and Dave Rodgman added the LZO-RLE version in 2018. The parse is the sliding window method of Ziv and Lempel (1977).

## References
