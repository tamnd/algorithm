---
tag: E9Q3EG
kind: algorithm
slug: zstandard
name: Zstandard
aliases:
- zstd
- Zstandard compression
- RFC 8878
- application/zstd
area: compression-and-coding/dictionary-compression
level: advanced
summary: "The LZ77 format of RFC 8878: Huffman-coded literals, sequence codes in finite state entropy (tANS) tables, three repeat offsets, 128 KiB blocks and an XXH64 checksum."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes, w: the window size in bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(w)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2015
  people: [Yann Collet]
  note: Yann Collet released zstd v0.1.0 on 25 August 2015. Version 1.0.0 (2016) fixed the format. RFC 8478 (2018) described it, and RFC 8878 (2021) replaced RFC 8478.
prereqs: [lz77, huffman-coding, tabled-asymmetric-numeral-systems]
see_also: [deflate, brotli, lz4, lzma, canonical-huffman-code, xxhash, match-finding, optimal-parsing]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc8878
    title: Yann Collet and Murray Kucherawy (editor), RFC 8878, Zstandard Compression and the 'application/zstd' Media Type, February 2021
    locator: "Section 3.1.1 (frames, blocks, literals and sequences sections), Section 3.1.1.5 (repeat offsets), Section 4.1 (FSE), Section 4.2 (Huffman coding), Appendix A (predefined decoding tables)"
  - url: https://github.com/facebook/zstd/blob/dev/doc/zstd_compression_format.md
    title: Yann Collet, Zstandard Compression Format, version 0.4.5
    locator: "Repeat offsets (the Repeated_Offsets table), Block_Content and Block_Maximum_Size"
  - url: https://github.com/facebook/zstd/tree/dev/tests/golden-decompression
    title: facebook/zstd, tests/golden-decompression and tests/golden-decompression-errors
    locator: "the files empty-block.zst, rle-first-block.zst, zeroSeq_2B.zst, off0.bin.zst, truncated_huff_state.zst, zeroSeq_extraneous.zst"
  - url: https://github.com/facebook/zstd/blob/dev/README.md
    title: facebook/zstd README
    locator: the section Benchmarks (lzbench on the Silesia corpus, Core i7-9700K)
  - url: https://github.com/facebook/zstd/blob/dev/CHANGELOG
    title: facebook/zstd CHANGELOG
    locator: "the entries v0.1.0 (Aug 25, 2015) and v1.0.0 (Sep 1, 2016)"
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

Zstandard (zstd) is a compressed data format that codes an [LZ77](/lz77/) parse with two entropy coders. A block holds a *literals section*, which is the literal bytes of all its matches, often coded with a [canonical Huffman code](/canonical-huffman-code/), and a *sequences section*. Each *sequence* is a triple (literal length, offset, match length). The three numbers become small codes plus raw extra bits, and the codes go through three [finite state entropy](/tabled-asymmetric-numeral-systems/) (FSE, a tabled ANS) coders that share one bitstream. Three *repeat offsets* make a reuse of a recent distance cheap. RFC 8878 is the contract. It fixes the decoder and leaves the encoder free.

## In plain words

The compressor first finds repeats. Each step of the result says: "copy these many new bytes, then copy these many old bytes from this far back". All new bytes of a block go into one pile, which is packed with a Huffman code. The three numbers of each step are packed with a fast table coder that gives each number close to its fair share of bits.

Steps often reuse a recent distance, so the format keeps the last three distances. A step can say "use the second-last distance" with a tiny code. The decoder reads the numbers from the end of the block toward the start, rebuilds each step, and copies the bytes. A frame of blocks ends with a checksum of the whole output.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case. All numbers are little endian. Bitstreams that are read backward have a 1 bit after their last data bit, then 0 to 7 zero bits that fill the byte.

### The frame

| part | content |
|---|---|
| magic number | 28 B5 2F FD, that is FD2FB528 |
| frame header descriptor | bits 7 and 6: content size flag; bit 5: single segment; bit 4: unused; bit 3: reserved, must be 0; bit 2: checksum flag; bits 1 and 0: dictionary ID flag |
| window descriptor | absent if single segment; else exponent $e$ (bits 7 to 3) and mantissa $a$ (bits 2 to 0), window $w = 2^{10+e} + a \cdot 2^{7+e}$ |
| dictionary ID | 0, 1, 2 or 4 bytes |
| content size | 0, 1, 2, 4 or 8 bytes; 1 byte only with single segment; the 2-byte form adds 256 |
| blocks | at least one |
| checksum | if the flag is set, the low 4 bytes of XXH64 of the content, seed 0 |

With single segment, the window is the content size. A *skippable frame* has a magic number from 184D2A50 to 184D2A5F, a 4-byte size and that many bytes to skip. Frames may follow each other, and the output is the joined content.

### Blocks

A block header has 3 bytes: bit 0 is *last block*, bits 1 and 2 are the type, and bits 3 to 23 are the size. Type 0 is a raw block of *size* bytes, type 1 is one byte repeated *size* times, type 2 is a compressed block of *size* bytes, and type 3 is not valid. The block maximum is the smaller of $w$ and 128 KiB. Both the block content and the decoded block must fit in it. A compressed block holds the literals section, then the sequences section.

### The literals section

The first byte gives the type in bits 1 and 0: 0 raw, 1 RLE, 2 Huffman with a tree description, 3 Huffman with the tree of the previous block (*treeless*). A 1 to 5 byte header holds the decoded size and, for types 2 and 3, the coded size and the number of streams (1 or 4). With 4 streams, a 6-byte *jump table* gives the sizes of the first three, and each stream decodes $\lceil r/4 \rceil$ bytes except the last.

The Huffman tree is sent as *weights*: weight $W > 0$ means a code of $b + 1 - W$ bits, where $b$ is the maximum code length (at most 11). The weights of all symbols but the last are sent, either as 4-bit fields or FSE-coded with two states. The last weight is the one that makes $\sum 2^{W-1}$ a power of two. Codes go to the smallest weights first, symbols in order within a weight. Each Huffman stream is read backward, from the end marker to the start, and must end exactly at the start.

### The sequences section

| part | content |
|---|---|
| number of sequences $N$ | 1 to 3 bytes; 0 means the block is the literals only, and the section must end there |
| modes | one byte: literal length mode (bits 7, 6), offset mode (5, 4), match length mode (3, 2), reserved (1, 0); each mode is 0 predefined, 1 RLE (one symbol byte), 2 FSE (a table description follows), or 3 repeat (the table of the previous block) |
| tables | in the order literal length, offset, match length |
| bitstream | the rest of the block, read backward |

The three codes map to values as follows:

| kind | codes | value |
|---|---|---|
| literal length | 0 to 35 | codes 0 to 15 are the length; code $c \ge 16$ has a base and 1 to 16 extra bits (RFC Table 16) |
| match length | 0 to 52 | codes 0 to 31 are the length minus 3; code $c \ge 32$ has a base and 1 to 16 extra bits (RFC Table 17) |
| offset | 0 to 31 | value $v = 2^c + $ ($c$ extra bits) |

An offset value $v > 3$ is the distance $v - 3$. A value $v \le 3$ names a *repeat offset*; see the second block of pseudocode below. At the start of a frame the repeat offsets are 1, 4, 8, and only compressed blocks change them.

### FSE tables

An FSE table with accuracy log $a$ has $2^a$ states. A *table description* gives each symbol a normalized count, and the counts add up to $2^a$; a count of $-1$ means "less than 1" and takes one cell at the end of the table. The other symbols are spread over the table with the step $2^{a-1} + 2^{a-3} + 3$. A cell of symbol $s$ gets a number of bits $k$ and a base $B$. In state $u$ the decoder outputs the symbol of cell $u$ and, to move on, reads $k$ bits $r$ and goes to state $B + r$. The *predefined* tables have $a = 6$ for both lengths and $a = 5$ for offsets, and RFC Appendix A lists them.

## The algorithm

The decoder of the sequences of one compressed block, after the literals $lits$ and the three tables $T_L$, $T_O$, $T_M$ are read. Each table maps a state to (symbol, bits, base), and READ($k$) takes the next $k$ bits from the backward stream:

```pseudo id=main
ZSTD-DECODE-SEQUENCES(lits, stream, T_L, T_O, T_M, rep, out)
L1  start reading stream at its end; skip the zero bits and the end-marker 1 bit
L2  s_L ← READ(a_L); s_O ← READ(a_O); s_M ← READ(a_M)
L3  for i ← 1 to N
L4      c ← T_O[s_O].symbol; v ← 2^c + READ(c)
L5      c ← T_M[s_M].symbol; ℓ ← MLBASE[c] + READ(MLBITS[c])
L6      c ← T_L[s_L].symbol; λ ← LLBASE[c] + READ(LLBITS[c])
L7      d ← RESOLVE-OFFSET(v, λ, rep)
L8      append the next λ bytes of lits to out
L9      if d = 0 or d > the frame output so far then fail
L10     repeat ℓ times: append out[|out| − d] to out
L11     if i < N then update s_L, then s_M, then s_O: s ← T[s].base + READ(T[s].bits)
L12 if the stream was not used up exactly then fail
L13 append the rest of lits to out
```

The repeat offsets $rep = (r_1, r_2, r_3)$, most recent first:

```pseudo id=rep
RESOLVE-OFFSET(v, λ, rep)
R1  if v > 3 then d ← v − 3; rep ← (d, r_1, r_2); return d
R2  k ← v − 1, plus 1 if λ = 0
R3  if k = 0 then return r_1                      ▷ no change
R4  d ← r_1 − 1 if k = 3, else r_(k+1)
R5  if k = 1 then rep ← (d, r_1, r_3) else rep ← (d, r_1, r_2)
R6  return d
```

Around this loop, the frame decoder reads the frame header, then each block. A raw or RLE block is copied out. A compressed block reads its literals section, the sequence count, the modes and the tables, and then runs the loop. At the end the decoder checks the content size and the XXH64 checksum.

The encoder is free. Ours writes a valid subset of the format:

1. One frame with single segment, the content size and the checksum. Blocks of at most 128 KiB.
2. A block of one repeated byte becomes an RLE block.
3. Else a greedy [hash chain](/match-finding/) search over 4-byte strings, 16 candidates deep and up to $2^{22}$ bytes back, makes a list of sequences. Matches do not cross the end of the block. Each distance becomes the repeat code that the decoder would resolve to it, or $d + 3$.
4. The literals stay raw. The three codes use the predefined tables (mode byte 0). The encoder runs the FSE coders backward: for the last sequence it takes any cell with the right symbol. For each earlier sequence it takes the one cell of the right symbol whose range $[B, B + 2^k)$ holds the next state, and writes that state minus $B$ in $k$ bits. It writes every field in the reverse of the decoder's read order, then the end marker.
5. If the compressed block is not smaller than the raw bytes, it writes a raw block and restores the repeat offsets.

## Example

Compress $x$ = `abcabcabcabcabcabc` (18 bytes). The greedy search finds one sequence: 3 literals `abc`, then a match of 15 bytes at distance 3. Distance 3 is none of the start values 1, 4, 8, so $v = 3 + 3 = 6$. Our encoder writes 22 bytes:

| bytes | field |
|---|---|
| 28 B5 2F FD | magic number |
| 24 | single segment, checksum, 1-byte content size |
| 12 | content size 18 |
| 4D 00 00 | last block, compressed, size 9 |
| 18 | raw literals, 3 bytes |
| 61 62 63 | `abc` |
| 01 00 | one sequence; all tables predefined |
| 76 6E 08 | the sequence bitstream |
| EB FE 13 27 | low 4 bytes of XXH64 of $x$ |

The bitstream is the number 086E76 (hex). Its top 1 bit is bit 19, the end marker. The 19 bits below it, read from the top, are:

| bits | field | value | meaning |
|---|---|---|---|
| 000011 | literal length state (6 bits) | 3 | $T_L$ state 3: code 3, so $\lambda = 3$ |
| 01110 | offset state (5 bits) | 14 | $T_O$ state 14: code 2 |
| 011101 | match length state (6 bits) | 29 | $T_M$ state 29: code 12, so $\ell = 12 + 3 = 15$ |
| 10 | offset extra bits (2) | 2 | $v = 2^2 + 2 = 6$, so $d = 3$ |

The length codes have no extra bits, and $N = 1$, so no state update follows. All 19 bits are used, as line L12 asks. The decoder appends `abc`, then copies 15 bytes, each from 3 back, which gives $x$.

## Correctness

The decoder inverts the encoder. Three facts carry the proof. First, for each symbol the ranges $[B, B + 2^k)$ of its cells tile the state space $[0, 2^a)$ exactly. So for each next state the encoder finds exactly one cell of the right symbol, and the decoder in that cell reads the same $k$ bits back and arrives at that state. Second, the encoder writes the fields in exactly the reverse order of the reads of lines L2 to L11, so the backward reader meets each field whole. Third, both sides run the same RESOLVE-OFFSET on the same history, so they get the same distance. Then lines L8 and L10 append $x$ as in any LZ77 decoder, also when $d < \ell$. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each sequence reads $O(1)$ fields of at most 31 bits and costs $O(1)$ plus the bytes it copies. Each Huffman symbol costs $O(1)$. Each block builds at most four tables of at most $2^{11}$ cells, a constant of the format. So the time is $\Theta(n + m)$. A streaming decoder keeps the last $w$ bytes of output and the tables, so the extra space is $\Theta(w)$. Our code keeps the whole output.
- **Encoding.** Our encoder checks at most 16 candidates at a searched position. No candidate is longer than the match it then takes, and the positions inside that match are inserted but not searched. So the search costs $O(16 n)$ in total, and the time is $O(n)$ expected (the hash table is expected $O(1)$ per access). The chains use $\Theta(n)$ space.
- **Size.** A raw block costs the input plus 3 bytes, and the frame adds at most 17 bytes, so the output is never more than $n + 3 \max(1, \lceil n / 2^{17} \rceil) + 17$ bytes.

## Properties

- **Two entropy coders.** Huffman for literals, which decodes with one table lookup per byte, and FSE for the sequence codes, which can spend a fraction of a bit on a frequent code.
- **Backward bitstreams.** An ANS coder decodes in the reverse of the order it encodes, so the encoder writes the stream backward and the decoder reads it forward in symbol order.
- **Large window.** The window can be up to $2^{41} + 7 \cdot 2^{38}$ bytes; the RFC recommends at most 8 MB for interoperability.
- **Self-checking.** The content size and the checksum catch most corruption, and the format rules (exact stream ends, reserved bits) catch more.
- **Same decoder for all levels.** The levels from fast to ultra differ only in the encoder's search and parse.

## Variants and improvements

- **Better parsing.** The reference encoder has levels from greedy and [lazy](/lazy-matching/) parsing up to an [optimal parse](/optimal-parsing/) that prices each choice with the entropy coders. The format is the same.
- **Dictionaries.** A dictionary gives history before the first byte and can carry Huffman and FSE tables and repeat offsets. A frame names it by its dictionary ID. Dictionaries help small inputs most. Our code does not support them.
- **Long distance matching.** A second search with a large window finds repeats far back, and it writes the same sequences.
- **Seekable format.** Independent frames and a skippable frame with an index allow random access.
- **Related formats.** [DEFLATE](/deflate/) has a 32 KiB window and Huffman codes only. [Brotli](/brotli/) adds context modeling and a static dictionary. [LZ4](/lz4/) drops entropy coding for speed. [LZMA](/lzma/) uses an adaptive range coder for a smaller output and slower decoding.

## When to use it

Use zstd as a general-purpose compressor when both speed and size matter: logs, packages, file systems, databases and network traffic. The README of the zstd repository reports, on the Silesia corpus with lzbench on a Core i7-9700K at 4.9 GHz (Ubuntu 24.04, gcc 14.2.0), for zstd 1.5.7 level 1: ratio 2.896, compression at 510 MB/s and decompression at 1550 MB/s. On the same table, zlib 1.3.1 level 1 gives 2.743, 105 MB/s and 390 MB/s, and lz4 1.10.0 gives 2.101, 675 MB/s and 3850 MB/s. When decoding speed matters most, use LZ4. When size matters most, use the high zstd levels or LZMA.

## Pitfalls

- **Repeat offsets when the literal length is 0.** The codes then shift by one, and code 3 means $r_1 - 1$. Encoders and decoders that get this wrong agree with each other but not with the format.
- **Which blocks update the history.** Only compressed blocks change the repeat offsets and the tables for repeat mode, and only blocks with $N > 0$ change the tables. An encoder that falls back to a raw block must undo the offsets that it chose.
- **Order of reads.** Extra bits are read offset, match length, literal length, but the states update literal length, match length, offset. The initial states are read literal length, offset, match length.
- **Exact stream ends.** A Huffman stream and the sequence bitstream must end exactly at their first bit; extra bytes after $N = 0$ are an error. The golden error files test these rules.
- **Zero offset.** Code 3 with $\lambda = 0$ and $r_1 = 1$ gives distance 0, which is corrupt (the golden file off0.bin.zst).
- **RFC Table 18.** In RFC 8878, the last two rows of the repeat offset table do not follow the text. The format document in the zstd repository (version 0.4.5) has the corrected rows.
- **Memory limits.** A frame can ask for a huge window. Decoders should reject windows above a set limit.

## Implementations

## History

Yann Collet released zstd v0.1.0 on 25 August 2015, built on his FSE coder, which is a tabled form of Jarek Duda's asymmetric numeral systems. Facebook released version 1.0.0 in 2016, which fixed the format. RFC 8478 (2018) described the format and the media type application/zstd, and RFC 8878 (February 2021), by Collet and Kucherawy, replaced it. The parse is the sliding window method of Ziv and Lempel (1977).

## References
