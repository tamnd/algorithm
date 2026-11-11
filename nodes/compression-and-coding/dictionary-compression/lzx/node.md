---
tag: Y9A12Q
kind: algorithm
slug: lzx
name: LZX
aliases:
- LZX compression
area: compression-and-coding/dictionary-compression
level: advanced
summary: "The LZ77 format of Microsoft cabinet files: Huffman-coded literals and matches in blocks, three repeated offsets, position slots, 32 KiB frames and an optional x86 call filter."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes, w: the window size in bytes}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(w)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1995
  people: [Jonathan Forbes, Tomi Poutanen]
  note: Forbes and Poutanen made LZX for an Amiga archiver, released in 1995. Microsoft adapted the method for its cabinet (CAB) files after Forbes joined Microsoft in 1996.
prereqs: [lz77, canonical-huffman-code]
see_also: [deflate, lzma, brotli, zstandard, huffman-coding, match-finding, greedy-parsing, package-merge]
sources:
  - url: https://officeprotocoldoc.z19.web.core.windows.net/files/MS-PATCH/%5BMS-PATCH%5D.pdf
    title: "Microsoft, [MS-PATCH]: LZX DELTA Compression and Decompression, release of 19 August 2025"
    locator: "Section 2.1 (bit stream, repeated offsets, match lengths, position slots), Section 2.2.2 (E8 call translation), Section 2.3 (block header and block types), Section 2.5 (tree lengths and pretree), Sections 2.6 and 2.7 (match encoding and decoding), Section 3 (the example stream for abc)"
  - url: https://github.com/kyz/libmspack/blob/master/libmspack/mspack/lzxd.c
    title: Stuart Caie, libmspack, mspack/lzxd.c (the LZX decoder of cabextract)
    locator: "the opening comment (the creators, and where the CAB format differs from the old LZX document and from LZX DELTA), lzxd_init (window sizes), lzxd_read_lens, lzxd_decompress (frames, block headers, E8 reversal)"
  - url: https://github.com/kyz/libmspack/blob/master/libmspack/test/test_files/cabd/mszip_lzx_qtm.cab
    title: libmspack, test/test_files/cabd/mszip_lzx_qtm.cab
    locator: "folder 1 (CFFOLDER at offset 0x2C, typeCompress 0x1203), its CFDATA block at offset 0xC9: 114 bytes that decode to the 187 bytes of lzx.txt"
  - url: https://en.wikipedia.org/wiki/LZX
    title: LZX, Wikipedia
    locator: the history part (the Amiga release in 1995, Forbes at Microsoft from 1996, use in CAB, CHM and WIM)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

LZX is the [LZ77](/lz77/) format of Microsoft cabinet (CAB) files. It codes literals and matches with [canonical Huffman codes](/canonical-huffman-code/) in one large main tree, whose match symbols join a *position slot* (the size class of the offset) with a short length. It keeps the last three match offsets, so a repeated offset costs only a main symbol. The output is cut into frames of 32 KiB, and an optional filter makes x86 call addresses easier to compress. This page describes the CAB form with windows of $2^{15}$ to $2^{21}$ bytes. LZX DELTA, the later form in [MS-PATCH], adds larger windows, longer matches and reference data.

## In plain words

The compressor reads the input and finds repeated pieces. Each new byte becomes a literal. Each repeat becomes a match: "copy this many bytes from this far back".

One Huffman tree codes both literals and matches. A match symbol holds the rough size of the distance and the length, if the length is short. Extra raw bits then give the exact distance, and a second tree gives long lengths. The last three distances are remembered, and a match can say "use one of those" with no extra bits.

The data comes in blocks. Each block sends its own trees, as changes to the trees of the block before. A block can also hold raw bytes. Every 32 KiB of output, the bit stream jumps to the next 16-bit word, so a reader can start a frame at a known place.

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case. The stream stores neither $n$ nor the window size $w = 2^b$, $15 \le b \le 21$. A CAB file keeps $b$ in the compression type of its folder (`0x1203` is LZX with $b = 18$) and $n$ in its data blocks.

### Bits

The stream is a sequence of 16-bit little-endian words. Bits are read from the high bit of each word down. A number of $k$ bits is read high bit first, and so is a Huffman code. The raw bytes of an uncompressed block are the only byte-wise part.

### The stream

| part | content |
|---|---|
| E8 header | 1 bit; if it is 1, a 32-bit translation size follows (high 16 bits first) |
| blocks | block type (3 bits), block size (24 bits, the number of output bytes), then the block body |

Blocks and frames are independent. A frame is 32,768 output bytes (the last frame can be shorter). When the output reaches the end of a frame, the reader drops the rest of the current word. A block can span frames, and a frame can hold many blocks, but no match crosses the end of a frame or of a block.

### Block types

| type | body |
|---|---|
| 1, verbatim | the main tree (in two parts: symbols 0 to 255, then the match symbols), the length tree (249 symbols), then the tokens |
| 2, aligned offset | as verbatim, but an aligned offset tree of 8 symbols comes first, as 8 lengths of 3 bits |
| 3, uncompressed | 1 to 16 zero bits up to the next word, then R0, R1, R2 as 32-bit little-endian numbers, the raw bytes, and one zero byte if the size is odd |

The main tree has $256 + 8s$ symbols, where $s$ is the number of position slots: 30, 32, 34, 36, 38, 42 or 50 for $b = 15, \ldots, 21$.

### Tree lengths

A tree is sent as its code lengths (0 to 16), each as a difference to the length that the same symbol had in the previous block (0 at the start). A *pretree* of 20 symbols, sent as 20 lengths of 4 bits, codes the differences. A pretree symbol $z \le 16$ sets the length to $(\mathit{old} - z) \bmod 17$. Symbol 17 sets $4 + $ (4 bits) lengths to 0, symbol 18 sets $20 + $ (5 bits) lengths to 0, and symbol 19 reads 1 bit and one more pretree symbol $z$, and sets $4 + $ (1 bit) lengths to $(\mathit{old} - z) \bmod 17$, where $\mathit{old}$ is the old length of the first of them. The main tree uses one pretree per part, and the length tree has its own. A tree must be complete, except that the length tree may be empty if no match has a length above 8.

### Matches

A match has a length $\ell \in [2, 257]$ and an offset $d \ge 1$. Its *formatted offset* is 0, 1 or 2 if $d$ is R0, R1 or R2, and $d + 2$ otherwise. The formatted offset falls in one position slot $p$ with base $B_p$ and $e_p$ footer bits:

| slot $p$ | 0 to 3 | 4, 5 | 6, 7 | ... | 34, 35 | 36 and up |
|---|---|---|---|---|---|---|
| footer bits $e_p$ | 0 | 1 | 2 | $\lfloor p / 2 \rfloor - 1$ | 16 | 17 |

and $B_0 = 0$, $B_{p+1} = B_p + 2^{e_p}$. The main symbol is $256 + 8p + \min(\ell - 2, 7)$. If $\ell \ge 9$, the length tree codes $\ell - 9$. Then come the footer bits. In an aligned offset block with $e_p \ge 3$, the top $e_p - 3$ footer bits are raw and the low 3 come from the aligned offset tree. All three offsets start as 1. Offset R1 or R2 swaps with R0; a new offset $d$ pushes: $(R0, R1, R2) \leftarrow (d, R0, R1)$.

## The algorithm

The decoder of the tokens of a verbatim or aligned offset block. It runs until the block has no bytes left or the frame ends; $R$ is the list (R0, R1, R2):

```pseudo id=main
LZX-TOKENS(r, out, left, end, R)        ▷ left: bytes left in the block; end: the end of the frame
L1  while left > 0 and |out| < end
L2      s ← DECODE(r, MAIN)
L3      if s < 256 then append s to out; ℓ ← 1
L4      else
L5          h ← (s − 256) mod 8; p ← ⌊(s − 256) / 8⌋
L6          ℓ ← h + 2; if h = 7 then ℓ ← ℓ + DECODE(r, LENGTH)
L7          if p < 3 then d ← R[p]; swap R[0] and R[p]
L8          else
L9              e ← EXTRA[p]
L10             if the block is aligned and e ≥ 3 then v ← 8 · READ(r, e − 3) + DECODE(r, ALIGNED)
L11             else v ← READ(r, e)
L12             d ← BASE[p] + v − 2; R ← (d, R[0], R[1])
L13         if d < 1 or d > |out| or ℓ > left or |out| + ℓ > end then fail
L14         repeat ℓ times: append out[|out| − d] to out
L15     left ← left − ℓ
L16 return left
```

The stream decoder reads the E8 header, then loops until $|out| = n$. When $left = 0$ it reads a block header, the trees or the raw header, and sets $left$. It calls LZX-TOKENS, or copies raw bytes up to the end of the block or frame. Each time $|out|$ reaches the end of a frame, it drops the rest of the current word. At the end, if the translation size $t$ is not 0, it undoes the E8 translation in each frame below 1 GiB with more than 10 bytes:

```pseudo id=e8
E8-REVERSE(frame, start, t)
E1  i ← 0
E2  while i < |frame| − 10
E3      if frame[i] ≠ E8 then i ← i + 1; continue
E4      c ← start + i; v ← the signed 32-bit number in frame[i + 1 .. i + 4]
E5      if −c ≤ v < t then write (v − c if v ≥ 0, else v + t) back to frame[i + 1 .. i + 4]
E6      i ← i + 5
```

The encoder is free. Ours writes a valid subset of the format:

1. The window is the smallest CAB window that holds the input (or the one the caller gives). If the caller gives a translation size $t$, the encoder applies the forward E8 translation per frame: a relative value $v$ with $-c \le v < t - c$ becomes $v + c$, and one with $t - c \le v < t$ becomes $v - t$.
2. One block per frame. A greedy parse tries R0, R1 and R2 first (length 2 and up), then a [hash chain](/match-finding/) over 3-byte strings, 32 candidates deep and at most $w - 3$ back (length 3 and up). It takes a new offset only if it is strictly longer than the best repeated one.
3. It builds the trees as optimal [length-limited](/package-merge/) codes (16 bits for the main and length trees, 15 for the pretrees, 7 for the aligned offset tree). A tree with one used symbol gets a second symbol, so that its codes are 0 and 1.
4. It writes the block as verbatim or aligned offset, whichever is smaller. If raw bytes are smaller, it writes an uncompressed block with the offsets from before the frame, and restores its own R0, R1, R2 to those values.

## Example

Take $x$ = `abcabcabcabcabcabc` (18 bytes, window $2^{15}$). The parse is `a`, `b`, `c`, then a match of length 15 at offset 3. The offset is new, so its formatted offset is 5, which is slot 4 ($B_4 = 4$, 1 footer bit, footer 1). The length gives header 7 and length symbol $15 - 9 = 6$. The main symbol is $256 + 8 \cdot 4 + 7 = 295$.

| token | main symbol | main code | length code | footer | bits |
|---|---|---|---|---|---|
| `a` | 97 | `00` | | | 2 |
| `b` | 98 | `01` | | | 2 |
| `c` | 99 | `10` | | | 2 |
| match 15 at 3 | 295 | `11` | `1` (symbol 6) | `1` | 4 |

The main tree has four used symbols of length 2. The length tree has one used symbol, so it gets symbol 0 as a partner: 0 is `0` and 6 is `1`. In a verbatim block the tokens take 10 bits. The three pretrees take 240 bits and the coded lengths 113 more. With the E8 bit and the block header (1 + 27 bits), the stream has 391 bits, which the frame end pads to 50 bytes:

`00 10 22 01 00 00 00 00 00 00 20 00 07 01 FD DA DF F7 00 A8 ...`

The first word is `0x1000`: the E8 bit 0, block type `001`, then the start of the block size 18. An uncompressed block takes $1 + 27 + 4 + 96 + 8 \cdot 18 = 272$ bits (the 4 bits are padding), which is 34 bytes. So our encoder picks an uncompressed block for this input. For `abc` it writes `00 30 30 00 01 00 00 00 01 00 00 00 01 00 00 00 61 62 63 00`, which is the example of [MS-PATCH] Section 3 without its 2-byte chunk size.

## Correctness

The decoder inverts the encoder. Four facts carry the proof. First, the pretree tokens rebuild each tree's lengths: each token sets its run to the right value, because $(\mathit{old} - z) \bmod 17$ inverts $z = (\mathit{old} - \mathit{new}) \bmod 17$, and both sides keep the same old lengths. Second, the slot and footer of a formatted offset $f$ give $f$ back, because the slots split $[0, 2^b)$ into intervals $[B_p, B_p + 2^{e_p})$, and in an aligned block $B_p$ is a multiple of 8. Third, the lists R0, R1, R2 of the encoder and the decoder start equal and change by the same rule. Fourth, every copy points inside the output and inside its frame, so line L14 copies, as in any LZ77 decoder, also when $d < \ell$. The E8 translation is a bijection on the 4-byte values in the range $[-c, t)$, and both sides scan the same positions. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** Each token costs one main symbol of at most 16 bits, at most one length symbol, at most 17 footer bits and one aligned symbol, and each output byte is written once. The header of a verbatim or aligned offset block reads at most $656 + 249$ lengths and three pretrees, but it also takes at least 267 bits of input. An uncompressed block header takes at least 124 bits and costs $O(1)$. The E8 pass reads each output byte once. So the time is $\Theta(n + m)$. A streaming decoder keeps $w$ bytes of output, so the extra space is $\Theta(w)$. Our code keeps the whole output.
- **Encoding.** Our encoder checks at most 32 chain candidates and 3 repeated offsets at a searched position, each in $O(257)$ time, and inserts but does not search the positions inside a match. So the parse costs $O(n)$ expected time (the hash table is expected $O(1)$ per access). The trees cost a constant per frame, because the alphabets have at most 656 symbols. The chains use $\Theta(n)$ space.
- **Size.** A frame costs at most $27 + 16 + 96 + 8(L + 1)$ bits for $L$ bytes, plus at most 15 bits of padding, and the header is at most 33 bits. So the output is at most $n + 21 \lceil n / 32768 \rceil + 5$ bytes.

## Properties

- **One tree for literals and matches.** The main symbol joins the offset class with a short length, so frequent pairs of slot and length get short codes.
- **Cheap repeated offsets.** A match at R0, R1 or R2 costs only its main symbol and its length. Structured data with fixed record sizes uses them often.
- **Aligned offset blocks.** When the low 3 bits of large offsets are skewed, for example in tables of 4-byte or 8-byte entries, a Huffman code for those bits beats raw bits.
- **Frames.** Each 32 KiB of output starts on a word boundary of the input, so a reader can map frames to CAB data blocks.
- **No framing data.** The stream has no length, no window size and no checksum. The container gives the first two; a CAB data block has an optional checksum.

## Variants and improvements

- **LZX DELTA.** The form of [MS-PATCH] adds a 16-bit chunk size before each frame, windows up to $2^{25}$ bytes, matches up to 33,024 bytes after a length of 257, and reference data that offsets can reach before the output.
- **CHM and LIT files.** These reset the LZX state at fixed intervals, so a reader can start at a reset point.
- **WIM.** The Windows imaging format uses a variant of LZX as one of its compression methods.
- **Better encoders.** The format allows any parse. An [optimal parse](/optimal-parsing/) priced with the trees, many blocks of chosen sizes, and lazy matching all give smaller output with the same decoder.
- **Related formats.** [DEFLATE](/deflate/) has separate literal/length and distance trees and no repeated offsets. [LZMA](/lzma/) also keeps repeated offsets but codes every bit with an adaptive range coder. [Zstandard](/zstandard/) and [Brotli](/brotli/) keep repeated offsets too.

## When to use it

Use LZX when you must read or write CAB, CHM or similar Microsoft files. It was made for program files: the E8 filter helps x86 code, the window can be 64 times larger than the 32 KiB of DEFLATE, and decoding stays one Huffman lookup per token. For a new format, [Zstandard](/zstandard/) or [LZMA](/lzma/) is a more common choice.

## Pitfalls

- **The stream has no length.** A decoder must get $n$ from the container. The last frame is shorter than 32 KiB.
- **Bit order.** Words are little-endian, but bits come from the high end of each word. A reader that takes bits from the low end of each byte, as in DEFLATE, fails.
- **Padding before raw bytes.** An uncompressed block skips 1 to 16 bits, not 0 to 15: at a word boundary it skips a full word.
- **The odd byte.** After an uncompressed block of odd size there is one pad byte, and the next block header starts after it.
- **Frame ends.** At every multiple of 32,768 output bytes the reader drops the rest of the word, also in the middle of a block. A match must not cross that point.
- **Tree lengths are differences.** The old lengths come from the last verbatim or aligned block, not from zero, and an uncompressed block does not reset them.
- **Code 19.** The difference of a code 19 run uses the old length of the first element of the run for all of them.
- **E8 range.** The scan stops 10 bytes before the end of each frame, skips the 4 bytes after each E8 byte, and stops after the first $2^{30}$ bytes.
- **The old LZX document.** libmspack lists several errors in it: the number of slots for 1 MiB and 2 MiB windows, the place of the aligned offset tree, and 3 footer bits in aligned blocks. Follow the CAB implementation or [MS-PATCH].

## Implementations

## History

Jonathan Forbes and Tomi Poutanen made LZX for an Amiga archiver of the same name, released in 1995. Forbes joined Microsoft in 1996, and Microsoft adapted the method for its cabinet files. CHM help files and the WIM image format use it too. The first public document of the CAB format had errors that libmspack lists. The [MS-PATCH] specification of LZX DELTA, published later, corrects them. The parse is the sliding window method of Ziv and Lempel (1977).

## References
