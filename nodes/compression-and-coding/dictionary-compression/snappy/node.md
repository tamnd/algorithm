---
tag: A8ZRG6
kind: algorithm
slug: snappy
name: Snappy
aliases:
- Google Snappy
- Zippy compression
area: compression-and-coding/dictionary-compression
level: advanced
summary: "Google's byte-oriented LZ77 format: a varint length, then literal and copy elements whose tag byte gives the kind. No entropy coder, so it trades size for speed."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2011
  note: Google published the Snappy library and its format description in 2011; the format description is last revised 2011-10-05 and says it is based on text by Zeev Tarantov.
prereqs: [lz77, back-reference]
see_also: [lz4, lzo, deflate, lzss, match-finding, greedy-parsing, variable-byte-encoding, crc32c]
sources:
  - url: https://github.com/google/snappy/blob/main/format_description.txt
    title: Google, Snappy compressed format description, last revised 2011-10-05
    locator: Section 1 (the varint preamble), Section 2.1 (literals) and Sections 2.2.1 to 2.2.3 (the three copy elements)
  - url: https://github.com/google/snappy/blob/main/framing_format.txt
    title: Google, Snappy framing format description, last revised 2013-10-25
    locator: Section 3 (masked CRC-32C) and Section 4 (chunk types 0x00, 0x01, 0xfe, 0xff and the reserved ranges)
  - url: https://github.com/google/snappy/blob/main/README.md
    title: Google, Snappy README
    locator: Introduction and Performance (the speed figures and the earlier name Zippy)
  - url: https://github.com/golang/snappy/blob/master/snappy_test.go
    title: The Go Authors, golang/snappy, snappy_test.go
    locator: the function TestDecode (hand-made valid and corrupt streams)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

Snappy is a compressed data format and library of Google that codes an [LZ77](/lz77/) parse with whole bytes and no entropy coder. A raw Snappy stream is the uncompressed length as a varint, followed by *elements*: a literal run, or a copy of earlier output given by an offset and a length (a [back-reference](/back-reference/)). The low two bits of each element's tag byte say which of four element kinds follows. Because each field is a whole number of bytes, the decoder is a short loop of table-free byte operations; the price is a larger output than an entropy-coded format such as [DEFLATE](/deflate/).

## In plain words

The output begins with the length of the original data. Then the decoder reads one instruction at a time. Each instruction starts with one byte. Its two lowest bits say what kind of instruction it is: "copy the next few bytes as they are", or "go back some distance in what you already wrote and copy some bytes from there". The other six bits of that byte, and one to four bytes after it, give the count and the distance.

The encoder looks for a 4-byte string that it saw a short time ago, with a hash table. If it finds one, it extends the match and writes a copy instruction. If not, it moves on, and it moves faster and faster through data where it finds nothing. There is no Huffman coding step, so both directions are fast and simple.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$, with $n < 2^{32}$. The analysis is worst case, with no probability model. The format description of Google is the contract; it says that it "is not a formal specification". It fixes the decoder and leaves the encoder free.

### The preamble

The stream starts with $n$ as a little-endian base-128 varint: each byte holds 7 bits of the value, and its high bit is 1 when more bytes follow ([variable-byte encoding](/variable-byte-encoding/)). The value 64 is the byte 40, and 2097150 is FE FF 7F. At most 5 bytes are needed.

### The elements

| tag bits 1 and 0 | element | the rest of the tag | bytes after the tag | length | offset |
|---|---|---|---|---|---|
| 00 | literal | bits 7 to 2 hold $len - 1$ if it is below 60; the values 60, 61, 62, 63 say that $len - 1$ follows in 1, 2, 3 or 4 little-endian bytes | the length bytes, then $len$ raw bytes | 1 to $2^{32}$ | none |
| 01 | copy, 1-byte offset | bits 4 to 2 hold $len - 4$; bits 7 to 5 hold bits 10 to 8 of the offset | 1 byte: bits 7 to 0 of the offset | 4 to 11 | 0 to 2047 |
| 10 | copy, 2-byte offset | bits 7 to 2 hold $len - 1$ | 2 bytes, little endian | 1 to 64 | 0 to 65535 |
| 11 | copy, 4-byte offset | bits 7 to 2 hold $len - 1$ | 4 bytes, little endian | 1 to 64 | 0 to $2^{32} - 1$ |

An offset of 0 can be written but is not legal, and so is an offset larger than the output written so far. The length may be larger than the offset; then the copy repeats the last offset bytes, which codes a run. The stream has no end marker: it ends when the elements have produced exactly $n$ bytes.

### The framing format

The raw format holds one buffer. The separate, optional framing format cuts a stream into chunks of a 1-byte type and a 3-byte little-endian length. Type FF is the stream identifier `sNaPpY` and must come first, so a framed stream begins with FF 06 00 00 73 4E 61 50 70 59. Type 00 is a raw Snappy stream and type 01 is uncompressed data; both hold at most 65536 uncompressed bytes and start with a masked [CRC-32C](/crc32c/) of the uncompressed bytes: the CRC rotated right by 15 bits plus A282EAD8 modulo $2^{32}$. Type FE is padding, types 02 to 7F are reserved and must stop the decoder, and types 80 to FD are reserved and must be skipped.

## The algorithm

The decoder:

```pseudo id=main
SNAPPY-DECODE(s)
L1  (n, pos) ← READ-VARINT(s, 0)
L2  out ← empty byte string
L3  while pos < |s| do
L4      tag ← s[pos]; pos ← pos + 1
L5      if tag mod 4 = 0 then                          ▷ literal
L6          ℓ ← ⌊tag / 4⌋
L7          if ℓ ≥ 60 then ℓ ← the next ℓ − 59 bytes, little endian
L8          ℓ ← ℓ + 1
L9          append the next ℓ bytes of s to out
L10     else if tag mod 4 = 1 then ℓ ← 4 + (⌊tag / 4⌋ mod 8); off ← 256 ⌊tag / 32⌋ + the next byte
L11     else ℓ ← 1 + ⌊tag / 4⌋; off ← the next 2 or 4 bytes, little endian
L12     if off = 0 or off > |out| then fail
L13     if the element was a copy: repeat ℓ times: append out[|out| − off] to out
L14 if |out| ≠ n then fail
L15 return out
```

Each step also fails when the input ends inside an element or when out would grow past $n$. Line L13 copies byte by byte, which handles $off < \ell$.

The encoder is free. Ours follows the plan of the reference compressor:

1. Cut the input into blocks of 64 KiB, and match only inside a block, so each offset fits in 2 bytes.
2. In each block, keep a [hash table](/hash-table/) from each 4-byte string to its last position. At position $p$, look up $x[p \ldots p+3]$. If the table has a position $c$, extend the match as far as the block allows, write the pending literals, write the copy, put the positions inside the match into the table, and jump to the end of the match. This is a [greedy parse](/greedy-parsing/) with one candidate per position.
3. If the lookup fails, move ahead by $step = \lfloor skip / 32 \rfloor$ bytes and add $step$ to $skip$, which starts at 32. So $skip - 32$ is the number of bytes passed since the last match: after 32 bytes with no match the step is 2 bytes, after 32 more it is 3, and so on. A match sets $skip$ back to 32. Each stretch of 32 bytes at step $j$ costs about $32/j$ lookups, so a stretch of $B$ bytes with no match costs about $32 \ln(B/32) + O(32)$ lookups, $O(\log B)$: 131 lookups pass 1024 bytes, and 266 lookups pass a full block of 65536 bytes.
4. Write a copy of length up to 64 as one element: 01 when $4 \le \ell \le 11$ and $off < 2048$, else 10. Cut a longer copy into pieces of 64, and use a piece of 60 when the rest would be below 4, so each piece has at least 4 bytes.

## Example

Compress $x$ = `the cat and the hat and the bat` (31 bytes). Our encoder writes 24 bytes:

| bytes | element | output so far |
|---|---|---|
| 1F | varint: $n = 31$ | |
| 2C, then 12 bytes | literal, $\lfloor 44/4 \rfloor = 11$, so $\ell = 12$ | `the cat and ` |
| 01 0C | copy-1: $\ell = 4 + 0 = 4$, $off = 12$ | `the cat and the ` |
| 00 68 | literal, $\ell = 1$: `h` | `the cat and the h` |
| 1D 0C | copy-1: tag 1D = 000 111 01, $\ell = 4 + 7 = 11$, $off = 12$ | `the cat and the hat and the ` |
| 08 62 61 74 | literal, $\ell = 3$: `bat` | `the cat and the hat and the bat` |

The first copy finds `the ` at distance 12. The second finds `at and the ` at distance 12 too, 11 bytes, the longest a copy-1 element can hold. A match of 12 bytes or more needs element 10: for $x$ = `abcdabcdabcdabcd` the encoder writes 10 0C `abcd` 2E 04 00, where 2E = 001011 10 is a copy-2 of length 12 at offset 4, a copy that overlaps itself. A run of 100 bytes `a` becomes 64 00 61 FE 01 00 8A 01 00: one literal, then copies of 64 and 35 at offset 1.

The format description's own example writes `xababab` as the literal `xab` and a copy with offset 2 and length 4. Our encoder writes exactly that: 07 08 78 61 62 01 02.

## Correctness

The decoder of lines L1 to L15 inverts the encoder. The encoder's elements describe $x$: a literal holds the next bytes of $x$, and a copy at position $p$ with offset $off$ and length $\ell$ is only written when $x[p + i] = x[p - off + i]$ for $0 \le i < \ell$. By induction on $i$, the byte copy of line L13 then appends $x[p + i]$, also when $off < \ell$, because each byte it reads is either before $p$ or was written earlier in the same copy. Each field of an element has a fixed width given by the tag, so the decoder reads the elements in the order and with the values that the encoder wrote, and the encoder writes $n$ in the preamble. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each element costs $O(1)$ plus the bytes it reads and writes, and each element reads at least one input byte. So the time is $\Theta(n + m)$. The decoder needs no tables and no extra space beyond the output.
- **Encoding.** Each lookup costs $O(1)$ expected time in the hash table, and a match of length $\ell$ costs $O(\ell)$ to extend and to insert. Positions skipped by line 3 of the plan cost nothing. So the time is $O(n)$ expected. The table has at most one entry per position of a block, at most 65536 entries.
- **Size.** A literal of $\ell \le 60$ bytes costs $\ell + 1$ bytes, and a longer one at most $\ell + 5$. A copy of $\ell \ge 4$ bytes costs at most 3 bytes per piece of at least 4 bytes, so it never costs more than the bytes it replaces. On data with no match, our encoder writes one literal per 64 KiB block, so the output has at most $n + 4 \lceil n / 65536 \rceil + 5$ bytes. The reference library sizes its output buffer with the looser bound $32 + n + \lfloor n/6 \rfloor$ (the function MaxCompressedLength in snappy.cc), which also covers its own choice of short literals.

## Properties

- **Byte aligned.** Each element starts at a byte, so the decoder needs no bit buffer. This is the source of its speed.
- **No entropy coding.** A literal byte costs 8 bits, whatever its frequency. On text the format is larger than DEFLATE.
- **Small window in practice.** The offset field allows $2^{32} - 1$, but an encoder that matches inside 64 KiB blocks never writes element 11. The description says the encoder of its time works in 32 kB blocks and that a decoder must not rely on that.
- **Not streaming in the raw form.** The preamble holds the full length, so the raw format suits one buffer. The framing format adds streams and checksums.

## Variants and improvements

- **Framing.** The framing format above, used for files with the extension `.sz`.
- **LZ4.** [LZ4](/lz4/) has a similar design: a token byte with two 4-bit length fields, and a 2-byte offset. [LZO](/lzo/) is an older format with the same aim.
- **Better parsing.** A lazy or optimal parse, as in [lazy matching](/lazy-matching/), gives a smaller stream in the same format; each decoder reads it.

## When to use it

Use Snappy when the speed of compression and decompression matters more than the size, for example for data that moves between machines in a data center, or for blocks in a database or a column store. The README of the library gives, on a single core of an Intel Core i7 in 64-bit mode, about 250 MB/s or more for compression and about 500 MB/s or more for decompression, for the slowest inputs of its benchmark. For smaller output with a similar decode speed, LZ4 at a high level or [Zstandard](/zstandard/) at a low level are the usual choices.

## Pitfalls

- **Zero or far offsets.** Line L12 must reject $off = 0$ and $off > |out|$. Without the first test, a copy of offset 0 loops or reads one byte past the output; the corruption tests of the library check exactly this.
- **Overflow in the literal length.** With 4 length bytes, $\ell - 1$ can be $2^{32} - 1$, so $\ell = 2^{32}$. In 32-bit arithmetic $\ell$ wraps to 0 and the decoder skips the literal. Compute $\ell$ with 64 bits, or test $\ell - 1$ against the bytes left.
- **Trust in the preamble.** The preamble is a claim, not a fact. Line L14 checks it, and each element must check that out stays at most $n$.
- **Copy-1 range.** Element 01 holds lengths 4 to 11 only. An encoder that writes a copy of length 12 as element 01 writes length 4 with the wrong offset bits.
- **Raw and framed.** A framed stream starts with FF 06 00 00 `sNaPpY`; a raw decoder reads it as a corrupt stream. The masked CRC is of the uncompressed data.

## Implementations

## History

Snappy was used inside Google, where it was earlier called Zippy, before the library and its format description were published in 2011. The format description says that it is based on text by Zeev Tarantov. The framing format was added later and has the revision date 2013-10-25. The parse is the sliding window method of Ziv and Lempel (1977).

## References
