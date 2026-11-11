---
tag: 2E3NAH
kind: algorithm
slug: lz4
name: LZ4
aliases:
- LZ4 compression
- LZ4 block format
- LZ4 frame format
area: compression-and-coding/dictionary-compression
level: intro
summary: "Byte-oriented LZ77 format: each sequence is a token with two 4-bit lengths, literals and a 2-byte offset. No entropy stage, so decoding is very fast."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2011
  people: [Yann Collet]
  note: Yann Collet published LZ4 in 2011. The block format and the frame format are defined in two documents of the lz4 repository; the frame format document is at version 1.6.5.
prereqs: [lz77, back-reference]
see_also: [snappy, lzo, deflate, zstandard, lzss, match-finding, greedy-parsing, xxhash]
sources:
  - url: https://github.com/lz4/lz4/blob/dev/doc/lz4_Block_format.md
    title: Yann Collet, LZ4 Block Format Description
    locator: "Compressed block format (the token, the length bytes and the offset), End of block conditions (rules 1 to 3), Implementation notes (Safe decoding)"
  - url: https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md
    title: Yann Collet, LZ4 Frame Format Description, version 1.6.5
    locator: "General Structure of LZ4 Frame format, Frame Descriptor (FLG, BD, Header Checksum), Data Blocks, Skippable Frames, Legacy frame"
  - url: https://github.com/lz4/lz4/tree/dev/tests/data/goldenSamples
    title: lz4/lz4, tests/data/goldenSamples
    locator: the files dictID.bin and skip.bin
  - url: https://github.com/lz4/lz4/blob/dev/README.md
    title: lz4/lz4 README
    locator: the section Benchmarks (lzbench on the Silesia corpus, Core i7-9700K)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

LZ4 is a compressed data format that codes an [LZ77](/lz77/) parse with whole bytes and no entropy coder. A *block* is a list of *sequences*. Each sequence is a run of literal bytes followed by a [back-reference](/back-reference/) of at least 4 bytes, given by a 2-byte offset and a length. One *token* byte holds both lengths in two 4-bit fields. The decoder is a short loop with no tables and no bit operations beyond one shift and one mask per sequence. A separate *frame format* wraps blocks with a header, block sizes and [xxHash](/xxhash/) checksums.

## In plain words

The compressed data is a list of steps. Each step says: "copy these new bytes, then go back some distance in what you wrote and copy some old bytes again". The first byte of a step holds two small numbers: how many new bytes come, and how many old bytes to copy. If a number does not fit, more bytes follow that add to it. The distance back is always two bytes. The last step has new bytes only.

The encoder looks up each group of 4 bytes in a table of places where it saw them before. When it finds one, it measures how far the match goes and writes a step. There is no Huffman stage, so the output is larger than with gzip, but both directions are very fast.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case, with no probability model. The block format document of the lz4 repository is the contract. It fixes the decoder and leaves the encoder free.

### A sequence

| field | size | meaning |
|---|---|---|
| token | 1 byte | high 4 bits: literal length $L$; low 4 bits: match length minus 4, $M$ |
| more literal length | 0 or more bytes | present only if $L = 15$: add each byte; a byte of 255 says one more byte follows |
| literals | $L$ bytes | copied to the output as they are |
| offset | 2 bytes, little endian | distance back, 1 to 65535; 0 is not valid |
| more match length | 0 or more bytes | present only if $M = 15$, coded as for $L$ |

The match length is $M + 4$, so the shortest match is 4 bytes. The offset may be smaller than the match length; then the match copies bytes that it wrote itself, one at a time, which codes a run. There is no limit on the lengths in the format; the document recommends that a decoder accept lengths up to 4 MB.

### The end of a block

The block has no length field and no end marker: the caller knows its compressed size. The last sequence ends right after its literals, with no offset. The block format adds three rules that the encoder must keep, so that fast decoders can copy in wide words without a test for each byte:

1. The last sequence has literals only.
2. The last 5 bytes of the input are literals. So the last sequence has at least 5 bytes, unless the input has fewer.
3. The last match starts at least 12 bytes before the end of the block.

So a block of fewer than 13 bytes with no history has no match. A decoder may reject a block that breaks these rules; ours accepts it.

### The frame format

A frame holds a stream that a block alone cannot, with its sizes and checks:

| part | content |
|---|---|
| magic number | 04 22 4D 18, that is 184D2204 little endian |
| FLG | bits 7 and 6: version 01; bit 5: blocks are independent; bit 4: block checksums; bit 3: content size present; bit 2: content checksum; bit 1: reserved 0; bit 0: dictionary ID present |
| BD | bits 6 to 4: maximum block size, 4 = 64 KB, 5 = 256 KB, 6 = 1 MB, 7 = 4 MB; other bits 0 |
| content size, dictionary ID | 8 and 4 bytes, little endian, if their flags are set |
| HC | bits 15 to 8 of XXH32 of the descriptor (FLG up to the dictionary ID), with seed 0 |
| data blocks | each a 4-byte little-endian size; if its high bit is 1, the block is stored, else it is an LZ4 block; then an optional XXH32 of the block bytes |
| EndMark | 4 zero bytes |
| content checksum | optional XXH32 of the whole content, seed 0 |

When the blocks are not independent, a match may reach back into the previous 64 KB of the frame. A *skippable frame* has a magic number from 184D2A50 to 184D2A5F, then a 4-byte size, then that many bytes that the decoder skips. The older *legacy frame* has the magic number 184C2102 and blocks of 8 MB; our code does not read it.

## The algorithm

The block decoder:

```pseudo id=main
LZ4-DECODE-BLOCK(s, h)                       ▷ h: earlier output that matches may use
L1  out ← h
L2  loop
L3      token ← the next byte of s
L4      L ← ⌊token / 16⌋; if L = 15 then add the more-length bytes to L
L5      append the next L bytes of s to out
L6      if s has no more bytes then exit the loop
L7      off ← the next 2 bytes of s, little endian
L8      if off = 0 or off > |out| then fail
L9      ℓ ← token mod 16; if ℓ = 15 then add the more-length bytes to ℓ
L10     ℓ ← ℓ + 4
L11     repeat ℓ times: append out[|out| − off] to out
L12 return out without its first |h| bytes
```

Each step also fails when $s$ ends inside a field. Line L11 copies one byte at a time, which handles $off < \ell$.

The encoder is free. Ours is the plain greedy method that the reference compressor also uses at its fast levels:

1. Keep a [hash table](/hash-table/) from each 4-byte string to the last position where it starts.
2. At position $p$, with $p \le n - 12$, look up $x[p \ldots p+3]$ and store $p$. If the table had a position $c$ with $p - c \le 65535$, extend the match forward, but not past $n - 5$. If the match has at least 4 bytes, write a sequence with the pending literals and this match, put the positions inside the match into the table, and jump to its end. Else move to $p + 1$. This is a [greedy parse](/greedy-parsing/) with one candidate per position.
3. At the end, write the pending literals as the last sequence.

The 4-byte table and the limits $n - 12$ and $n - 5$ make each of the three end rules true by construction. For linked blocks in a frame, the encoder puts the last 64 KB of the previous blocks in the table first.

## Example

Compress $x$ = `abcdefabcdefabcdefabcdef` (24 bytes). At $p = 6$ the table finds `abcd` at $c = 0$. The match may end at $24 - 5 = 19$, so it has 13 bytes. Our encoder writes 15 bytes:

| bytes | field | output so far |
|---|---|---|
| 69 | token: $L = 6$, $M = 9$, so $\ell = 13$ | |
| 61 62 63 64 65 66 | literals | `abcdef` |
| 06 00 | offset 6 | `abcdefabcdefabcdefa` (13 bytes copied, each 6 back) |
| 50 | token: $L = 5$, last sequence | |
| 62 63 64 65 66 | literals | `abcdefabcdefabcdefabcdef` |

The match starts at 6, which is at least 12 bytes before the end, and the last 5 bytes are literals, as the rules ask. The 12-byte input `abcabcabcabc` cannot have a match at all: the only match would start at 3, and rule 3 needs a start at $12 - 12 = 0$ or before. So it becomes C0 and the 12 bytes.

As a frame, the 57-byte text `Hello, LZ4! Hello, LZ4! Hello, LZ4! Hello, LZ4! The end.` with a newline becomes 45 bytes: 04 22 4D 18, then FLG 64 (version 01, independent blocks, content checksum), BD 40 (64 KB), HC A7, the block size 1A 00 00 00, the 26-byte block CF 48 ... 0A, the EndMark, and the content checksum 17 65 17 D1. The reference tool lz4 v1.10.0 with `-9` gives the same 45 bytes for this input.

## Correctness

The decoder of lines L1 to L12 inverts the encoder. Each sequence that the encoder writes describes the next part of $x$: its literals are the next bytes of $x$, and a match at position $p$ with offset $off$ and length $\ell$ is only written when $x[p + i] = x[p - off + i]$ for $0 \le i < \ell$. By induction on $i$, line L11 then appends $x[p + i]$, also when $off < \ell$, because each byte it reads lies before $p$ or was written earlier in the same match. The token and the length bytes store $L$ and $\ell - 4$ so that lines L4 and L9 read them back, and the last sequence is the only one whose literals reach the end of $s$, so line L6 stops at the right place. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each sequence costs $O(1)$ plus the bytes it reads and writes, and each sequence reads at least one byte. So the time is $\Theta(n + m)$, and the decoder needs no space beyond the output.
- **Encoding.** Each lookup costs $O(1)$ expected time, and a match of length $\ell$ costs $O(\ell)$ to extend and to insert. So the time is $O(n)$ expected, and the table holds at most one entry per distinct 4-byte string of the last 64 KB.
- **Size.** A literal costs 1 byte, plus 1 token byte and 1 more byte per 255 literals in a sequence. On data with no match the output is one sequence of $n + 1 + \lceil (n - 14)/255 \rceil$ bytes for $n \ge 15$. A match of $\ell$ bytes costs the 2 offset bytes, its share of the token, and, for $\ell \ge 19$, another $\lfloor (\ell - 19)/255 \rfloor + 1$ bytes. So a long match costs about 1 byte per 255 bytes, and the block format document gives about 250 as the best possible ratio.

## Properties

- **Byte aligned.** Every field starts at a byte boundary, so no bit buffer is needed. This is why the decoder is fast.
- **No entropy coding.** A literal costs 8 bits whatever its frequency. On text, the output is larger than with [DEFLATE](/deflate/).
- **64 KB window.** The offset has 16 bits, so a match reaches at most 65535 bytes back.
- **Same decoder for all levels.** A slow encoder that searches better (the HC levels, or an optimal parse) writes the same format, and the decoder speed does not change.

## Variants and improvements

- **LZ4 HC.** The high compression levels search hash chains and use a better parse. The format stays the same.
- **Dictionaries.** The two sides may agree on a dictionary of up to 64 KB that acts as history before the first block. The frame header can name it with the dictionary ID.
- **Linked blocks.** With the independence flag clear, each block may use the previous 64 KB, which helps when blocks are small.
- **Other byte formats.** [Snappy](/snappy/) and [LZO](/lzo/) are of the same kind. [Zstandard](/zstandard/) adds entropy coding and a larger window for a smaller output at a lower decode speed.

## When to use it

Use LZ4 when speed matters more than size: in-memory compression, file system blocks, network messages, or caches. The README of the lz4 repository reports, for its default level (v1.11.0) on the Silesia corpus with lzbench v2.4.1 on one core of a Core i7-9700K, a ratio of 2.112, compression at 770 MB/s and decompression at 4950 MB/s; for zlib level 1 on the same table, 2.743, 110 MB/s and 410 MB/s. When the output size matters more, use Zstandard or DEFLATE.

## Pitfalls

- **Offset 0 and far offsets.** Line L8 must reject both. The block document warns that a decoder that does not check offset 0 can leak old buffer contents.
- **Overlapping copies.** A block copy such as `memcpy` is wrong when $off < \ell$; copy byte by byte, or in steps of $off$.
- **End rules.** An encoder that writes a match into the last 5 bytes makes blocks that some fast decoders reject or read wrongly. Our encoder stops matches at $n - 5$ and starts them at $n - 12$ or before.
- **Block versus frame.** A raw block has no magic number and no size; the caller must store the compressed size and a bound on the output. Do not hand a frame to a block decoder.
- **Header checksum.** HC is the second byte of XXH32 of the descriptor, not the low byte, and the descriptor does not include the magic number.
- **Large lengths.** The length bytes have no limit in the format. A decoder with 32-bit lengths must check for overflow on very large blocks.

## Implementations

## History

Yann Collet published LZ4 in 2011. The block format and the frame format are described in two documents in the lz4 repository; the frame format has a version history, and its legacy frame is the format of the first "LZ4Demo" program. The parse is the sliding window method of Ziv and Lempel (1977), and the byte-aligned coding follows the same idea as LZO and Snappy.

## References
