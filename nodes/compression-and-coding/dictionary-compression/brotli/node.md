---
tag: EH674F
kind: algorithm
slug: brotli
name: Brotli
aliases:
- Brotli compression
- RFC 7932
- Brotli Compressed Data Format
area: compression-and-coding/dictionary-compression
level: advanced
summary: "The LZ77 format of RFC 7932: prefix-coded commands, literal trees chosen by the last two bytes, a ring of four recent distances and a static dictionary of English words with 121 transforms."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes, w: the window size in bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(w)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2015
  people: [Jyrki Alakuijala, Zoltán Szabadka]
  note: Google announced Brotli on 22 September 2015 as a successor to Zopfli for web content. RFC 7932 (July 2016) fixed the format.
prereqs: [lz77, canonical-huffman-code, context-modeling]
see_also: [deflate, zstandard, lzma, static-dictionary-compression, move-to-front-transform, package-merge, match-finding, optimal-parsing]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc7932
    title: Jyrki Alakuijala and Zoltan Szabadka, RFC 7932, Brotli Compressed Data Format, July 2016
    locator: "Section 3 (prefix codes), Section 4 (distances), Section 5 (insert-and-copy codes), Section 6 (block types), Section 7 (context modeling), Section 8 (static dictionary), Section 9 (stream format), Section 10 (decoding algorithm), Appendix B (transforms)"
  - url: https://github.com/google/brotli/tree/master/tests/testdata
    title: google/brotli, tests/testdata
    locator: "the files empty.compressed, empty.compressed.05, empty.compressed.16, x.compressed, x.compressed.01, x.compressed.03, xyzzy.compressed, 10x10y.compressed, 64x.compressed, quickfox.compressed, ukkonooa.compressed"
  - url: https://opensource.googleblog.com/2015/09/introducing-brotli-new-compression.html
    title: Zoltan Szabadka, Introducing Brotli, a new compression algorithm for the internet, Google Open Source Blog, 22 September 2015
    locator: the whole post (the release, the name, and the relation to Zopfli)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

Brotli is a compressed data format that codes an [LZ77](/lz77/) parse with [canonical prefix codes](/canonical-huffman-code/) and adds three tools. First, the tree that codes a literal can depend on the two bytes before it, through a *context map* ([context modeling](/context-modeling/)). Second, a distance can name one of the last four distances with a short code. Third, a distance that points before the start of the output names a word of a built-in [static dictionary](/static-dictionary-compression/) of 13,504 words, changed by one of 121 *transforms*. RFC 7932 fixes the decoder and leaves the encoder free.

## In plain words

The compressor turns the input into a list of commands. Each command says: "write these new bytes, then copy this many bytes from this far back". The command, its new bytes and its distance each go through their own Huffman-style codes.

Brotli adds three ideas. The code for a new byte can depend on the two bytes before it, so the byte after a space and the byte after a digit can use different codes. The last four distances are kept, and a command can say "use the last one" or "the second-to-last, plus one" with a tiny code. A distance that points before the start of the output means a word of a fixed English dictionary that every decoder has. The word can come with a capital letter or with a space or "the" around it.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case.

### Bits

All fields are packed from the least significant bit of each byte. A number of $k$ bits is stored low bit first. A prefix code is stored from its first bit, so a decoder reads it one bit at a time, or reverses it in a table. A stream has no magic number and no checksum.

### The stream

| part | content |
|---|---|
| WBITS | 1, 4 or 7 bits: `0` means 16; else 3 bits $a \ne 0$ give $17 + a$; else 3 bits $b \ge 2$ give $8 + b$, and $b = 0$ gives 17. The window is $w = 2^{\mathrm{WBITS}} - 16$ |
| meta-blocks | each has a header and a body; the last one has ISLAST = 1 |

A meta-block header has ISLAST (1 bit), ISLASTEMPTY (1 bit, only if ISLAST; if set, the stream ends), MNIBBLES (2 bits: 4, 5 or 6 nibbles, or 0 for a metadata block), MLEN − 1 in that many nibbles (the top nibble must not be 0 if there are more than 4), and ISUNCOMPRESSED (1 bit, only if not ISLAST). An uncompressed meta-block skips to a byte boundary and holds MLEN raw bytes. A metadata block holds bytes that the decoder skips.

### The compressed meta-block header

| field | content |
|---|---|
| NBLTYPESL, NBLTYPESI, NBLTYPESD | the number of block types (1 to 256) for literals, commands and distances; if 2 or more: a prefix code for block type codes, a prefix code for block count codes, and the first block count |
| NPOSTFIX, NDIRECT | 2 bits and 4 bits; NDIRECT is the 4-bit value shifted left by NPOSTFIX |
| CMODE | 2 bits per literal block type: LSB6, MSB6, UTF8 or Signed |
| NTREESL, CMAPL | the number of literal trees and a context map of $64 \cdot$ NBLTYPESL entries |
| NTREESD, CMAPD | the number of distance trees and a context map of $4 \cdot$ NBLTYPESD entries |
| trees | NTREESL literal trees (256 symbols), NBLTYPESI command trees (704 symbols), NTREESD distance trees ($16 + \mathrm{NDIRECT} + 48 \cdot 2^{\mathrm{NPOSTFIX}}$ symbols) |

A *simple* prefix code lists 1 to 4 symbols, and the code lengths follow from their number (1; 1, 1; 1, 2, 2; 2, 2, 2, 2 or 1, 2, 3, 3). A *complex* prefix code sends the code lengths, compressed with a second prefix code. In that second code, symbol 16 repeats the last nonzero length 3 to 6 times and symbol 17 repeats a zero 3 to 10 times. A run of 16s (or of 17s) multiplies: the next count is $4(c - 2) + (3 \ldots 6)$, or $8(c - 2) + (3 \ldots 10)$. All codes are complete, except that a code with one symbol uses 0 bits.

### Commands

A *command* is (insert length, copy length, distance). One symbol of the 704-symbol command alphabet gives an insert length code (24 codes), a copy length code (24 codes, lengths from 2) and a flag. The 64 symbols in each cell share one insert code range and one copy code range. Symbols 0 to 127 also mean "the distance is the last distance", and then no distance is sent. Extra bits follow the symbol: first for the insert length, then for the copy length.

Distance codes 0 to 15 use the ring of the last four distances: 0 to 3 are the last to fourth-to-last distance, 4 to 9 are the last distance $-1, +1, -2, +2, -3, +3$, and 10 to 15 do the same for the second-to-last. The ring starts as 16, 15, 11, 4 (4 is the last), and every distance except code 0 and dictionary words goes into it. The codes after them give $1 \ldots \mathrm{NDIRECT}$, then the rest carry 1 to 24 extra bits.

### Context and block types

The literal tree is CMAPL$[64t + c]$, where $t$ is the current literal block type and $c \in [0, 64)$ is a function of the last two output bytes $p_1$ and $p_2$. The function is chosen by CMODE$[t]$: $p_1 \bmod 64$, $\lfloor p_1 / 4 \rfloor$, LUT0$[p_1]$ ∣ LUT1$[p_2]$, or $8 \cdot$ LUT2$[p_1]$ + LUT2$[p_2]$, with three tables of RFC Section 7.1. The distance tree is CMAPD$[4t + c]$, with $c = \min(\ell, 5) - 2$ for copy length $\ell$. Each category has a current block type and a count. When the count reaches 0, a block type code (0: the previous type, 1: the current type plus 1, $k \ge 2$: type $k - 2$) and a new count are read.

## The algorithm

The decoder of the commands of one compressed meta-block, after its header. Here $out$ is the output so far, $rb$ is the ring of distances, and READ uses the tree that the text names:

```pseudo id=main
BROTLI-DECODE-COMMANDS(MLEN, out, rb, w)
L1  end ← |out| + MLEN
L2  while |out| < end
L3      t ← next command block type; s ← READ(command tree of t)
L4      split s into insert code, copy code; λ ← insert length, ℓ ← copy length
L5      repeat λ times
L6          t ← next literal block type
L7          append READ(CMAPL[64t + CONTEXT(CMODE[t], p_1, p_2)]) to out
L8      if |out| = end then break                  ▷ the copy is ignored
L9      if s < 128 then d ← the last distance in rb
L10     else t ← next distance block type; k ← READ(CMAPD[4t + min(ℓ, 5) − 2]); d ← DISTANCE(k, rb)
L11     if d ≤ min(w, |out|) then push d to rb if s ≥ 128 and k ≠ 0; copy ℓ bytes, each from d back
L12     else append the dictionary word for (ℓ, d − min(w, |out|) − 1)
```

"Next block type" decrements the count of its category and, if the count was 0, first reads a block type code and a new count. The distance of a general code (NPOSTFIX $= p$, NDIRECT $= D$):

```pseudo id=dist
DISTANCE(k, rb)
D1  if k < 16 then return the short code value of k; it must be positive
D2  if k < 16 + D then return k − 15
D3  c ← k − D − 16; b ← 1 + ⌊c / 2^(p+1)⌋; h ← ⌊c / 2^p⌋
D4  return ((((2 + (h mod 2)) · 2^b − 4) + READ(b bits)) · 2^p) + (c mod 2^p) + D + 1
```

A dictionary word for length $\ell \in [4, 24]$ and word id $j$: let $b = $ NDBITS$[\ell]$, take base word $j \bmod 2^b$ of length $\ell$, and apply transform $\lfloor j / 2^b \rfloor$ (at most 120). A transform is a prefix, one of 21 elementary changes (none, capitalize the first letter, capitalize all, drop the first or last 1 to 9 bytes) and a suffix.

The encoder is free. Ours writes a valid subset of the format:

1. WBITS is the smallest value from 16 to 24 whose window holds the input. Meta-blocks have at most $2^{18}$ bytes and are never last; an empty last meta-block (bits 1, 1) ends the stream.
2. A greedy [hash chain](/match-finding/) search over 4-byte strings, 16 candidates deep and at most $w$ back, splits each meta-block into commands. A last command may have only literals.
3. One block type per category, NTREESL = NTREESD = 1, NPOSTFIX = NDIRECT = 0, context mode LSB6. So there is one literal tree, one command tree and one distance tree.
4. A distance equal to the last distance uses a command symbol below 128 if the codes fit, else distance code 0. A distance equal to another entry of the ring uses code 1, 2 or 3. Others use a general code. The encoder updates its own ring as the decoder will.
5. The trees are optimal [length-limited](/package-merge/) codes (at most 15 bits). A tree with at most 4 symbols is sent as a simple code, else as a complex code with runs of zeros (17) and of a repeated length (16).
6. If the compressed body is not smaller than the raw bytes, the meta-block is sent uncompressed and the ring is restored.

## Example

Compress $x$ = `abcabcabcabcabcabc` (18 bytes). The parse is one command: insert `abc`, then copy 15 bytes from distance 3. Our encoder writes 12 bytes, `10 01 00 00 E4 58 98 58 68 13 51 CD`, which are 96 bits:

| bits | field | value |
|---|---|---|
| 1 | WBITS | 0: 16, so $w = 65520$ |
| 1 + 2 + 16 + 1 | ISLAST, MNIBBLES, MLEN − 1, ISUNCOMPRESSED | 0, 4 nibbles, 17, 0 |
| 3 + 2 + 4 + 2 + 2 | NBLTYPES ×3, NPOSTFIX, NDIRECT, CMODE, NTREES ×2 | all one type, one tree, 0, 0, LSB6 |
| 28 | literal tree | simple, 3 symbols: `c` (1 bit), `a`, `b` (2 bits) |
| 14 | command tree | simple, 1 symbol: 218 |
| 10 | distance tree | simple, 1 symbol: 17 |
| 0 + 2 | command 218, copy extra bits | cell 3, insert code 3, copy code 10: $\lambda = 3$, $\ell = 14 + 1 = 15$ |
| 2 + 2 + 1 | literals | `a` = 10, `b` = 11, `c` = 0 |
| 0 + 1 | distance code 17, extra bit | $c = 1$, $b = 1$, $h = 1$: $(3 \cdot 2 - 4) + 0 + 1 = 3$ |
| 2 | ISLAST, ISLASTEMPTY | 1, 1 |

The trees with one symbol cost no bits per use. The decoder appends `abc`, then copies 15 bytes, each from 3 back, which gives $x$. A full encoder could send distance 3 as short code 4 ("last distance − 1"), because the ring starts with last distance 4. Ours uses only short codes 0 to 3.

## Correctness

The decoder inverts the encoder. Four facts carry the proof. First, the decoder rebuilds the same code lengths that the encoder used: a simple code lists its symbols in order of length, and the run codes 16 and 17 that the encoder writes add up, under the multiplying rule, to the exact run length. Since both sides build canonical codes from the same lengths, every symbol comes back. Second, each length and distance code with its extra bits covers its value exactly, because each base plus $2^{\text{extra}}$ is the next base. Third, both rings of distances start equal and change by the same rule. Fourth, each copy points inside the output, so line L11 copies, as in any LZ77 decoder, also when $d < \ell$. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each command, literal and distance costs $O(1)$ symbol reads of at most 15 bits plus at most 24 extra bits, and each output byte is written once. A meta-block header has at most 256 trees of each kind, of at most 704 symbols, and context maps of at most $64 \cdot 256$ entries. These are constants of the format, and every meta-block with a header adds at least one byte to $m$. So the time is $\Theta(n + m)$. A streaming decoder keeps $w$ bytes of output and the tables, so the extra space is $\Theta(w)$. Our code keeps the whole output.
- **Encoding.** Our encoder checks at most 16 candidates at a searched position, and inserts but does not search the positions inside a match. So the parse costs $O(n)$ expected time (the hash table is expected $O(1)$ per access). The trees cost a constant per meta-block. The chains use $\Theta(n)$ space.
- **Size.** Each meta-block adds at most 31 bits plus 8 bits per byte, and the start and end add at most 9 bits. So the output is at most $n + 4 \lceil n / 2^{18} \rceil + 2$ bytes.

## Properties

- **Context modeling at low cost.** The context of a literal picks a tree, not a probability, so decoding stays one table lookup per symbol.
- **Static dictionary.** Short text gains most, because the dictionary gives matches before any history exists. The dictionary is 122,784 bytes, and every decoder must hold it.
- **No framing.** No magic number, no checksum and no content size. The HTTP content coding name is `br` (RFC 7932 Section 13).
- **Window.** From $2^{10} - 16$ to $2^{24} - 16$ bytes. Copies may cross meta-block boundaries.
- **Same decoder for all levels.** The qualities 0 to 11 of the reference encoder differ only in their search, parse and choice of block types and trees.

## Variants and improvements

- **Better encoders.** The reference encoder at high quality uses an [optimal parse](/optimal-parsing/) priced with the prefix codes, many block types, context maps chosen by clustering, and the dictionary. The format is the same.
- **Context map coding.** A context map is sent with run-length codes for zeros and an optional inverse [move-to-front transform](/move-to-front-transform/), so maps with many repeated trees stay small.
- **Large window.** A later extension of the reference code allows windows up to $2^{30}$ bytes, but its streams do not follow RFC 7932.
- **Related formats.** [DEFLATE](/deflate/) has one literal tree, a 32 KiB window and no dictionary. [Zstandard](/zstandard/) uses FSE for the command parts and repeat offsets without a dictionary. [LZMA](/lzma/) uses adaptive binary range coding with contexts for every bit.

## When to use it

Use Brotli for content that is compressed once and sent many times: web pages, scripts, style sheets and fonts (WOFF 2.0 uses it). The static dictionary makes small text files smaller than DEFLATE can. Decoding stays fast because every symbol is one prefix code lookup. For general-purpose files where the compression time matters too, [Zstandard](/zstandard/) is a common choice.

## Pitfalls

- **Two bit orders.** Numbers are stored low bit first, but prefix codes are stored from their first bit. The fixed code for the code length code lengths (RFC Section 3.5) is printed so that it reads from right to left.
- **Which distances go into the ring.** Code 0 and the implicit distance of symbols below 128 do not push. Dictionary words do not push. Codes 1 to 15 push, even though the value was already in the ring.
- **The distance limit grows.** The largest copy distance is $\min(w, |out|)$, so the same distance is a copy late in the stream and a dictionary word early in it. A decoder must not treat it as corrupt.
- **The last command.** If the inserted literals fill the meta-block, the copy length is ignored and no distance follows. In every other case a copy or word that passes MLEN is an error.
- **Repeat code chains.** A 16 after a 16 changes the count of the first one; it does not start a new run. The same holds for 17 after 17, but not for a 16 after a 17.
- **Context across meta-blocks.** $p_1$ and $p_2$ are the last output bytes of the stream, also from earlier or uncompressed meta-blocks, and 0 at the start.
- **No uncompressed last meta-block.** ISUNCOMPRESSED is absent when ISLAST is set, so an encoder that ends with raw bytes must add an empty last meta-block.
- **Padding.** Unused bits at the end of the stream, and before an uncompressed or metadata body, must be 0.

## Implementations

## History

Jyrki Alakuijala and Zoltán Szabadka designed Brotli at Google. Zoltán Szabadka announced it on the Google Open Source Blog on 22 September 2015 as a new format after Zopfli, which is an encoder for DEFLATE. The post says that the name means "small bread" in Swiss German, after Zopfli, another Swiss bakery product. RFC 7932 (July 2016) defined the format and registered the HTTP content coding `br`. The parse is the sliding window method of Ziv and Lempel (1977).

## References
