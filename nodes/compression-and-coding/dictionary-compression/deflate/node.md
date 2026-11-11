---
tag: TDJAX5
kind: algorithm
slug: deflate
name: DEFLATE
aliases:
- RFC 1951
- Deflate compressed data format
area: compression-and-coding/dictionary-compression
level: intro
summary: "The format of zlib, gzip, PNG and ZIP: LZ77 matches in a 32 KiB window, coded with canonical Huffman codes in stored, fixed or dynamic blocks (RFC 1951)."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1996
  people: [Phil Katz, L. Peter Deutsch, Jean-loup Gailly, Mark Adler]
  note: Phil Katz designed the format for PKZIP. L. Peter Deutsch wrote it down as RFC 1951 in May 1996, together with the zlib (RFC 1950) and gzip (RFC 1952) wrappers.
prereqs: [lz77, huffman-coding, canonical-huffman-code]
see_also: [lzss, lazy-matching, match-finding, length-limited-prefix-code, adler-32, zstandard, brotli, lzma]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: L. Peter Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996
    locator: Section 3.2.2 (canonical Huffman codes), Section 3.2.3 (block header), Sections 3.2.4 to 3.2.7 (stored, fixed and dynamic blocks, the length and distance tables) and Section 4 (compression with hash chains and lazy matching)
  - url: https://www.rfc-editor.org/rfc/rfc1950
    title: L. Peter Deutsch and Jean-loup Gailly, RFC 1950, ZLIB Compressed Data Format Specification version 3.3, May 1996
    locator: Section 2.2 (CMF, FLG, FCHECK, FDICT, DICTID and the ADLER32 trailer)
  - url: https://www.rfc-editor.org/rfc/rfc1952
    title: L. Peter Deutsch, RFC 1952, GZIP file format specification version 4.3, May 1996
    locator: Section 2.3 (member header, FLG bits, CRC32 and ISIZE trailer) and Section 8 (CRC sample code)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse that DEFLATE uses)
  - url: https://github.com/madler/zlib/blob/develop/contrib/puff/puff.c
    title: Mark Adler, puff.c, a small reference inflater in the zlib source distribution
    locator: the functions stored, codes, fixed and dynamic, and the comments on incomplete codes
---

DEFLATE is the compressed data format of zlib, gzip, PNG and ZIP: an [LZ77](/lz77/) parse into literals and [back-references](/back-reference/) of length 3 to 258 at distance 1 to 32768, coded with [canonical Huffman codes](/canonical-huffman-code/) in a sequence of blocks. RFC 1951 defines the format by its decoder: each block is stored, coded with fixed Huffman codes, or coded with dynamic Huffman codes whose code lengths are sent in the block header. The format does not fix the encoder, so any parse and any valid code gives a valid stream. A decoder runs in time linear in the input and the output, and needs only the last 32 KiB of output.

## In plain words

The encoder reads the input from left to right. At each position it looks back in the last 32 kilobytes for the longest earlier copy of the text that starts here. If it finds a copy of 3 bytes or more, it writes "go back this far and copy this many bytes". If not, it writes the byte itself.

Then it turns these instructions into bits. Frequent bytes and frequent copy lengths get short bit patterns, rare ones get long patterns, as in Huffman coding. The table of patterns is sent at the start of each block in a compact form, or a fixed table is used, or the block is stored as plain bytes.

The decoder reads one pattern at a time, writes bytes or copies them from what it already wrote, and stops at the end of the last block.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$ with $\Sigma = \lbrace 0, \ldots, 255 \rbrace$ ($\sigma = 256$). The analysis is worst case over all inputs; there is no probability model. The format is the contract: the encoder may write any stream that RFC 1951 allows, and the decoder must return $x$ for it.

### Bit order

A DEFLATE stream is a sequence of bits packed into bytes from the least significant bit of each byte. Every fixed-width field (BFINAL, BTYPE, HLIT, the extra bits of a length) is stored with its least significant bit first. A Huffman code is the one exception: it is stored with its most significant bit first. So a decoder that reads bit by bit from the low end of the bytes sees each Huffman code in its normal order (RFC 1951 Section 3.1.1).

### Blocks

Each block starts with a 3-bit header: BFINAL (1 bit, set on the last block) and BTYPE (2 bits).

| BTYPE | block | content |
|---|---|---|
| 00 | stored | skip to a byte boundary, then LEN and NLEN (16 bits each, NLEN is the ones' complement of LEN), then LEN raw bytes |
| 01 | fixed Huffman | literal/length and distance symbols with the fixed codes below |
| 10 | dynamic Huffman | a header with the code lengths, then the symbols |
| 11 | reserved | error |

A stored block holds at most 65535 bytes. A back-reference may reach into earlier blocks, up to 32768 bytes back, also across a stored block.

### Symbols

One alphabet holds the literals and the lengths: symbols 0 to 255 are literal bytes, 256 ends the block, and 257 to 285 are length codes. A length code is followed by a second symbol from the distance alphabet, 0 to 29. Each code adds a number of extra bits, read as an integer with its least significant bit first.

| length symbol | 257 to 264 | 265 to 268 | 269 to 272 | 273 to 276 | 277 to 280 | 281 to 284 | 285 |
|---|---|---|---|---|---|---|---|
| extra bits | 0 | 1 | 2 | 3 | 4 | 5 | 0 |
| lengths | 3 to 10 | 11 to 18 | 19 to 34 | 35 to 66 | 67 to 130 | 131 to 257 | 258 |

| distance symbols | 0 to 3 | 4, 5 | 6, 7 | 8, 9 | ... | 26, 27 | 28, 29 |
|---|---|---|---|---|---|---|---|
| extra bits | 0 | 1 | 2 | 3 | ... | 12 | 13 |
| distances | 1 to 4 | 5 to 8 | 9 to 16 | 17 to 32 | ... | 8193 to 16384 | 16385 to 32768 |

In general distance symbol $2k + 2$ and $2k + 3$ for $k \ge 1$ have $k$ extra bits, with bases $2^{k+1} + 1$ and $3 \cdot 2^{k} + 1$. Symbols 286, 287, 30 and 31 occur in the fixed code but never in valid data.

### The fixed codes

| symbols | code length | first code |
|---|---|---|
| 0 to 143 | 8 | 00110000 |
| 144 to 255 | 9 | 110010000 |
| 256 to 279 | 7 | 0000000 |
| 280 to 287 | 8 | 11000000 |

The fixed distance code gives each of the 30 distance symbols the 5-bit code equal to its number.

### The dynamic header

After BTYPE = 10, the block sends HLIT (5 bits, the number of literal/length lengths minus 257), HDIST (5 bits, the number of distance lengths minus 1) and HCLEN (4 bits, the number of code length code lengths minus 4). Then come HCLEN + 4 values of 3 bits, the lengths of the *code length code*, in the fixed order

16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15,

so that the rarely used lengths at the end can be cut off. With this code the decoder reads HLIT + 257 + HDIST + 1 code lengths as one sequence. Symbols 0 to 15 are a length. Symbol 16 repeats the previous length 3 to 6 times (2 extra bits), 17 writes 3 to 10 zeros (3 extra bits) and 18 writes 11 to 138 zeros (7 extra bits). A repeat may run from the literal/length lengths into the distance lengths. From the lengths, each code is the canonical Huffman code of RFC 1951 Section 3.2.2: shorter codes come first, and codes of the same length are in symbol order. Literal/length and distance codes have at most 15 bits; the code length code has at most 7 bits.

### The wrappers

DEFLATE has no header and no check value. Two wrappers add them.

- **zlib (RFC 1950).** A byte CMF (CM = 8 for deflate in the low 4 bits, CINFO in the high 4 bits, the window is $2^{\mathrm{CINFO} + 8}$ with CINFO at most 7), a byte FLG (FLEVEL in bits 6 and 7, FDICT in bit 5, FCHECK in bits 0 to 4 such that $256 \cdot \mathrm{CMF} + \mathrm{FLG}$ is a multiple of 31), an optional 4-byte DICTID when FDICT is set, the DEFLATE data, and the [Adler-32](/adler-32/) of the uncompressed data, big endian. With FDICT, the decoder must already hold the preset dictionary whose Adler-32 is DICTID, and the data may refer back into it.
- **gzip (RFC 1952).** The bytes 1F 8B, CM = 8, a FLG byte (FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT), a 4-byte MTIME, XFL and OS, the optional fields, the DEFLATE data, then the [CRC-32](/cyclic-redundancy-check/) of the uncompressed data and ISIZE, the length modulo $2^{32}$, both little endian. A gzip file may hold several members one after the other; the result is their concatenation.

## The algorithm

The decoder (often called *inflate*) is fixed by the format. BITS$(k)$ reads a $k$-bit field, least significant bit first. DECODE$(c)$ reads one Huffman code of the code $c$.

```pseudo id=main
INFLATE(input)
L1  out ← empty byte string
L2  repeat
L3      BFINAL ← BITS(1); BTYPE ← BITS(2)
L4      if BTYPE = 0 then
L5          skip to the next byte boundary
L6          LEN ← BITS(16); NLEN ← BITS(16)
L7          if NLEN ≠ LEN xor FFFF then fail
L8          append the next LEN input bytes to out
L9      else
L10         if BTYPE = 1 then (lit, dist) ← the fixed codes
L11         else if BTYPE = 2 then (lit, dist) ← READ-DYNAMIC-CODES()
L12         else fail                                  ▷ BTYPE = 3 is reserved
L13         loop
L14             s ← DECODE(lit)
L15             if s < 256 then append the byte s to out
L16             else if s = 256 then exit the loop      ▷ end of block
L17             else
L18                 len ← LBASE[s − 257] + BITS(LEXTRA[s − 257])
L19                 t ← DECODE(dist); d ← DBASE[t] + BITS(DEXTRA[t])
L20                 if d > |out| then fail
L21                 repeat len times: append out[|out| − d] to out
L22 until BFINAL = 1
L23 return out
```

Line L21 copies one byte at a time, so a copy with $d < len$ repeats the last $d$ bytes; this is how DEFLATE codes a run. READ-DYNAMIC-CODES reads the header of the section "The dynamic header" and builds both codes. A fast DECODE uses a table indexed by the next $L$ input bits, where $L$ is the longest code length: each symbol with a code of length $\ell$ fills $2^{L - \ell}$ entries. Because the bits arrive least significant first, the table index is the bit-reversed code.

The encoder (*deflate*) is free. The common design, also sketched in RFC 1951 Section 4, is this.

```pseudo id=encode
DEFLATE(x[0 .. n − 1])
L1  p ← 0; tokens ← empty
L2  while p < n do
L3      (ℓ, d) ← the longest match for x[p ..] found in the hash chain of x[p .. p + 2], with at most c candidates, d ≤ 32768, ℓ ≤ 258
L4      insert p into the hash chain of x[p .. p + 2]
L5      if lazy and ℓ ≥ 3 and the match at p + 1 is longer than ℓ then
L6          add the literal x[p] to tokens; p ← p + 1
L7      else if ℓ ≥ 3 then
L8          add (ℓ, d) to tokens; insert p + 1, ..., p + ℓ − 1; p ← p + ℓ
L9      else
L10         add the literal x[p] to tokens; p ← p + 1
L11 for each group of tokens do
L12     count the symbols; build length-limited codes (at most 15 bits)
L13     write the cheapest of a stored, a fixed and a dynamic block
```

The hash chains are a [hash table](/hash-table/) from each 3-byte string to its most recent position, plus a link from each position to the previous one with the same 3 bytes. This is [match finding](/match-finding/) by hash chains. Lines L5 and L6 are [lazy matching](/lazy-matching/): the encoder defers a match by one byte when the next position starts a longer one. Without them the parse is [greedy](/greedy-parsing/). Line L12 needs a [length-limited prefix code](/length-limited-prefix-code/), because a plain Huffman code may be longer than 15 bits; our code uses [package-merge](/package-merge/). Line L13 compares exact bit counts: the stored size, the fixed code size, and the dynamic code size including its header.

## Example

Compress $x$ = `abcabcabcabc` (12 bytes). The parse is three literals and one match: `a`, `b`, `c`, then (length 9, distance 3). The match overlaps its own output, so it copies `abc` three times. For one short block, the fixed code is the cheapest. The bits, in the order the decoder reads them:

| field | value | bits | width |
|---|---|---|---|
| BFINAL | 1 | 1 | 1 |
| BTYPE | 01, sent least significant bit first | 10 | 2 |
| literal `a` (97) | 00110000 + 97 | 10010001 | 8 |
| literal `b` (98) | | 10010010 | 8 |
| literal `c` (99) | | 10010011 | 8 |
| length 9 | symbol 263, no extra bits | 0000111 | 7 |
| distance 3 | symbol 2, no extra bits | 00010 | 5 |
| end of block | symbol 256 | 0000000 | 7 |

That is 46 bits. Packed from the low bit of each byte and padded with two zero bits, they give the 6 bytes `4b 4c 4a 86 23 00`. The decoder replays the trace: after the three literals out = `abc`; the match appends out$[\lvert out \rvert - 3]$ nine times, which gives `abcabcabcabc`; symbol 256 and BFINAL = 1 end the stream.

The zlib library, at level 9 with a raw stream, writes 7 bytes for the same input (`4b 4c 4a 4e 84 21 00`): its parse differs, but both streams decode to the same 12 bytes. Wrapped by zlib (`78 9c`, the data, then the Adler-32 `1d e0 04 99`), the input takes 13 bytes.

## Correctness

The full proof is below. It shows two things. First, the decoder of lines L1 to L23 is well defined: each code that it builds is a prefix code, so DECODE reads exactly the codeword that the encoder wrote. Second, the token list of DEFLATE describes $x$: the invariant of the loop of line L2 is that the tokens so far expand to $x[0 \ldots p-1]$, and a match $(\ell, d)$ at $p$ satisfies $x[p + i] = x[p - d + i]$ for $0 \le i < \ell$. Line L21 then writes $x[p + i]$ at each step, also when the copy overlaps itself. So INFLATE(DEFLATE($x$)) $= x$ for each $x$.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the uncompressed length and $m$ the compressed length. The front matter gives the decoder: time $\Theta(n + m)$, and $\Theta(1)$ extra space, a constant made of the 32 KiB window and two code tables of at most $2^{15}$ entries each.

- **Decoding.** Each pass of the loop of line L13 reads at most 15 + 5 + 15 + 13 = 48 bits and writes at least one byte, and each stored block costs $O(1)$ plus its bytes. Building a code table costs $O(2^{15})$, a constant, and each dynamic block has a header of at least 17 bits. So the time is $\Theta(n + m)$. The decoder keeps only the last 32768 output bytes, so the extra space is $O(1)$ beyond that window.
- **Encoding.** With a chain limit $c$ and the maximal match length 258, line L3 does at most $c$ comparisons of at most 258 bytes, so each position costs $O(c)$ and the time is $O(c\,n) = \Theta(n)$ for a fixed level. Package-merge on at most 286 symbols with limit 15 costs $O(15 \cdot 286)$ per block, a constant.
- **Size.** A stored block that starts on a byte boundary costs 5 bytes of overhead: 1 byte for the 3 header bits and the padding, and 4 bytes for LEN and NLEN. So the input in stored blocks alone takes $n + 5 \max(1, \lceil n / 65535 \rceil)$ bytes, and an encoder that compares each block with a stored block expands no block by more than about 5 bytes. No lossless format can compress all inputs ([the incompressibility argument](/incompressibility-argument/)).

## Properties

- **Decoder defined, encoder free.** Two good encoders give different streams for the same input. Tests must compare the decoded data, not the compressed bytes.
- **Bounded memory.** The decoder needs a 32 KiB window and at most two code tables.
- **Streaming.** Both directions work on a stream: the encoder needs to see only one block ahead, and the decoder writes output as it reads.
- **Weak on random data.** Random bytes give few matches, and a byte costs 8 or 9 bits in the fixed code. The stored block bounds the loss.
- **Sequential bits.** Huffman decoding is serial: the start of each code depends on the length of the code before it.

## Variants and improvements

- **Better parsing.** [Optimal parsing](/optimal-parsing/) chooses the tokens that minimize the coded size, not the longest match at each step. The zopfli encoder of Google does this and writes standard DEFLATE streams.
- **Deflate64.** PKWARE's "enhanced deflate" uses a 64 KiB window, two more distance codes and a longer length code. It is a different format and a standard inflater rejects it.
- **Successors.** [Brotli](/brotli/) adds context modeling and a static dictionary; [Zstandard](/zstandard/) adds a large window and finite state entropy coding; [LZMA](/lzma/) adds a range coder with adaptive binary contexts; [LZX](/lzx/) adds repeated offsets and a larger window. All of them keep the LZ77 plus entropy coder design.

## When to use it

Use DEFLATE when the reader is fixed: PNG, ZIP, gzip and HTTP content coding all require it, and a decoder exists on almost each system. For new formats, Zstandard gives better trade-offs between speed and size, Brotli is strong for small web text, LZMA and xz give smaller output with slower compression, and [LZ4](/lz4/) or [Snappy](/snappy/) decode faster with a larger output.

## Pitfalls

- **Bit order of codes.** Fixed fields go least significant bit first, Huffman codes most significant bit first. An encoder writes the bit-reversed code into an LSB-first writer. A decoder that does not reverse reads garbage after the first code.
- **Overlapping copies.** A match with $d < \ell$ must copy byte by byte, as in line L21. A block copy (memcpy or a slice) of $\ell$ bytes reads bytes that are not yet written.
- **Length 258.** The RFC table gives code 284 the lengths 227 to 257, and length 258 its own code 285 with no extra bits. An encoder must write 258 as code 285.
- **Bad code lengths.** A decoder must reject over-subscribed lengths (the Kraft sum is above 1), a repeat code 16 at the start, a run that passes HLIT + HDIST, and a missing code for symbol 256. An incomplete code is legal only in the case that RFC 1951 names: one distance code of length 1. Our decoder accepts that single-code case for the literal/length and distance codes and rejects the other incomplete codes.
- **Stored block alignment.** After the 3 header bits, the decoder drops the rest of the current byte before LEN. A decoder that keeps whole bytes in a bit buffer must drop only the partial byte.
- **Wrapper byte order.** Adler-32 in zlib is big endian; CRC-32 and ISIZE in gzip are little endian. The gzip FHCRC field is the low 16 bits of the CRC-32 of the header bytes.

## Implementations

## History

The ZIP archiver PKZIP of Phil Katz introduced the deflate method; RFC 1951 says that Katz designed the format. L. Peter Deutsch wrote RFC 1950, 1951 and 1952 in May 1996, with Jean-loup Gailly as co-author of RFC 1950; Gailly and Mark Adler wrote the zlib and gzip software that the RFCs describe. The parse is the sliding window method of Ziv and Lempel (1977), and the codes are Huffman codes (1952) in the canonical form.

## References
