---
tag: 2BH6WA
kind: algorithm
slug: lzw
name: Lempel-Ziv-Welch
aliases:
- LZW
area: compression-and-coding/dictionary-compression
level: intro
summary: LZ78 variant whose dictionary starts with all single symbols, so the output is only dictionary codes; used in Unix compress, GIF, TIFF and PDF.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the input, σ: the alphabet size, c: the number of codes}
  time: {worst: O(n log σ), expected: O(n)}
  space: {aux: Θ(c + σ)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1984
  people: [Terry A. Welch]
  note: Welch described the method in IEEE Computer in June 1984 as a fast variant of LZ78 for disk and tape controllers.
prereqs: [lz78]
see_also: [lz78, lz78-parsing, trie, adaptive-dictionary-compression, hash-table, lz77, deflate, lempel-ziv-parsing]
sources:
  - paper: doi:10.1109/MC.1984.1659158
    title: Terry A. Welch, A Technique for High-Performance Data Compression, IEEE Computer 17(6), 1984
    locator: pages 8 to 19 (the string table that starts with all single characters, the compression and decompression algorithms, and the exception case of a code that is not yet in the table)
  - url: https://www.w3.org/Graphics/GIF/spec-gif89a.txt
    title: CompuServe, Graphics Interchange Format, Version 89a, 1990
    locator: Section 22 (LZW Minimum Code Size) and Appendix F, Variable-Length-Code LZW Compression (clear code, end of information code, and code widths up to 12 bits)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Section 6.13, LZW, page 365
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 5, Dictionary Techniques (the LZW algorithm, with an encoding and a decoding example)
---

Lempel-Ziv-Welch (LZW) is the variant of [LZ78](/lz78/) that Terry Welch published in 1984. Its dictionary starts with every single symbol, so each phrase is the longest dictionary entry that matches, and the output is a list of dictionary codes with no literal symbols. After each phrase, the phrase plus the next symbol becomes a new entry. It solves [lossless compression](/lossless-compression/), and it is the method of Unix `compress`, of the GIF image format, and of the LZW filters of TIFF and PDF.

## In plain words

Both sides start with a list of all the single letters, each with a number. The coder reads the text and finds the longest piece that is in the list. It writes the number of that piece. It adds the piece plus the next letter to the list, under the next free number. Then it goes on from that next letter.

The reader gets numbers. For each number it writes the piece, and it adds a new entry to its own list: the piece before, plus the first letter of this piece. So it is always one entry behind the coder.

Once in a while the coder uses the entry that it has just made, which the reader does not have yet. The reader can still work it out: that entry is the piece before plus its own first letter.

## The problem

The input is a string $T = T[1..n]$ over an alphabet $\Sigma$ of $\sigma$ symbols, numbered $0, \ldots, \sigma - 1$ (for bytes, $\sigma = 256$). The encoder writes a list of codes $c_1, \ldots, c_m$, and the decoder must rebuild $T$ from it. In a bit stream, each code takes as many bits as the largest code that the decoder could see at that point, so the widths grow as the dictionary grows.

## The algorithm

$D$ maps strings to codes in the encoder and codes to strings in the decoder. In the encoder, $D$ is a [trie](/trie/) or a [hash table](/hash-table/) keyed by (code of $w$, next symbol), so that each step of line L4 is one lookup.

```pseudo id=main
LZW-ENCODE(T)                              ▷ T[1 .. n], n ≥ 1
L1  D ← the σ strings of one symbol, with codes 0 .. σ − 1; next ← σ
L2  w ← T[1]
L3  for i ← 2 to n do
L4      if w·T[i] is in D then w ← w·T[i]
L5      else
L6          output D(w)
L7          add w·T[i] to D with code next; next ← next + 1
L8          w ← T[i]
L9  output D(w)

LZW-DECODE(c_1, …, c_m)
L10 D ← the σ strings of one symbol, with codes 0 .. σ − 1; next ← σ
L11 prev ← D[c_1]; output prev
L12 for k ← 2 to m do
L13     if c_k < next then cur ← D[c_k]
L14     else if c_k = next then cur ← prev · prev[1]   ▷ the KwKwK case; any other code is an error
L15     output cur
L16     D[next] ← prev · cur[1]; next ← next + 1
L17     prev ← cur
```

**Why the decoder is one entry behind.** The encoder adds the entry $w \cdot T[i]$ in line L7 when it writes the code of $w$. The decoder learns $T[i]$ only from the next code, as the first symbol of the next phrase; so line L16 adds the same entry one step later.

**The KwKwK case.** Sometimes the next code is the entry that the encoder has just added, which the decoder does not have. This happens when the text has the form $K\omega K\omega K$, where $K$ is a symbol, $\omega$ a string, and $K\omega$ is in the dictionary but $K\omega K$ is not. The encoder writes the code of $K\omega$, adds $K\omega K$, and at once matches $K\omega K$ and writes its code. The decoder then has $prev = K\omega$, and the unknown phrase is $prev$ followed by its own first symbol, which is the first symbol of $prev$; line L14 builds it.

**Codes in a bit stream.** File formats add four things to the plain method.

- **Growing code width.** A code is written with $\lceil \log_2 (\text{largest code in use} + 1) \rceil$ bits, at least 9 for bytes. In this page's format, as in GIF and `compress`, the encoder writes each code with the bit length of $next - 1$, the largest code it has assigned, and the decoder, one entry behind, reads with the bit length of its own $next$. So the encoder starts to write 10-bit codes after it assigns code 512, and the decoder starts to read them after it assigns its own code 511: the two switch at the same code of the stream.
- **Maximum width and reset.** The table is limited to $2^b$ entries ($b = 12$ in GIF, up to 16 in `compress`). A special *clear* code tells the decoder to reset the table to the single symbols and the width to its start. The encoder of this page writes the clear code as soon as the table is full; GIF lets the encoder clear at any time, and also allows it to keep using the full table.
- **Reserved codes.** With bytes, `compress` in block mode uses 256 as the clear code and starts new entries at 257. GIF has a minimum code size $s$ (Section 22), a clear code $2^s$, an end of information code $2^s + 1$, and first free entry $2^s + 2$; codes start at $s + 1$ bits.
- **Bit order.** GIF and `compress` pack codes into bytes from the least significant bit; TIFF and PDF pack from the most significant bit.

## Example

**abababab, plain codes** ($\sigma = 256$, new entries from 256):

| step | $w$ when the match ends | output | new entry |
|---|---|---|---|
| 1 | a | 97 | 256 = ab |
| 2 | b | 98 | 257 = ba |
| 3 | ab | 256 | 258 = aba |
| 4 | aba | 258 | 259 = abab |
| 5 | b (end of input) | 98 | |

Code 258 is written one step after it is made: this is the KwKwK case with $K = a$, $\omega = b$. The decoder reads 97 ($a$), then 98 ($b$, adds 256 = ab), then 256 ($ab$, adds 257 = ba), then 258, which equals its $next$: so $cur = ab \cdot a = aba$, and it adds 258 = aba. Then 98 ($b$, adds 259 = abab). The output is $a \cdot b \cdot ab \cdot aba \cdot b = abababab$.

**abracadabra.** The codes are 97, 98, 114, 97, 99, 97, 100, 256, 258: nine codes for eleven symbols. The entries made are 256 = ab, 257 = br, 258 = ra, 259 = ac, 260 = ca, 261 = ad, 262 = da, 263 = abr.

**Packed.** In the format of the reference implementation, code 256 is the clear code and new entries start at 257, so $abababab$ gives the codes 97, 98, 257, 259, 98, all 9 bits wide. Packed from the least significant bit, they give the bytes 61 C4 04 1C 28 06 in hexadecimal.

**Width growth.** Take the 256 byte values in order and then the 44 even bytes $0, 2, \ldots, 86$. No pair of bytes repeats, so each byte is one code and 300 codes are written. Code $k$ is written when the largest assigned code is $255 + k$, so the first 256 codes take 9 bits, and after the encoder assigns code 512 the last 44 codes take 10 bits: $256 \cdot 9 + 44 \cdot 10 = 2744$ bits, or 343 bytes.

## Correctness

The encoder writes the phrases of the LZW parse: each phrase is the longest entry of $D$ that is a prefix of the rest of the text, since line L4 extends $w$ while $w \cdot T[i]$ is in $D$, and every entry of $D$ is a single symbol or an earlier entry plus one symbol, so the set is closed under prefixes. The decoder keeps the invariant that after $k$ codes its table holds the encoder's entries except the last one, and its output is the first $k$ phrases. A code is either in that table or is the one missing entry, which line L14 builds. The full proof is below.

## Complexity

**Time.** The encoder does $n - 1$ lookups of $w \cdot T[i]$ and at most $n$ insertions; with a hash table keyed by (code, symbol) this is $O(n)$ expected time, and with a balanced search tree at each trie node it is $O(n \log \sigma)$. The decoder writes each phrase once, $O(n)$ time; storing each entry as (code of prefix, last symbol) keeps it at $O(1)$ space per entry.

**Space.** $\sigma$ initial entries and one entry per code, $\Theta(c + \sigma)$; a bounded table caps this at $2^b$ entries.

**Output size.** The number of codes is at most the number of LZ78 phrases plus one, plus the clear codes; with code widths that grow as above, the code length is about $c \log_2 (c + \sigma)$ bits. Like [LZ78](/lz78/), it tends to the entropy rate of a stationary ergodic source when the table is not bounded; see the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/).

## Properties

- **Lossless and deterministic.**
- **Codes only.** No literal symbols are sent; a new symbol is always a code below $\sigma$.
- **Online.** Each code is written as soon as its phrase ends, and each phrase is decoded as soon as its code arrives.
- **Symmetric work.** Both sides build the same table; the decoder does no search.
- **Slow learning.** Each entry is one symbol longer than an earlier one, as in LZ78, so long exact repeats are coded with many codes.

## Variants and improvements

- **Table policies.** When the table is full: reset at once (this page), keep using the frozen table and reset when the compression ratio starts to fall (`compress` in block mode), or remove old entries (as in some modem standards such as V.42bis).
- **Early change.** The LZWDecode filter of PDF (ISO 32000-1, Section 7.4.4.3, EarlyChange, default 1) and LZW in TIFF increase the code width one code earlier than GIF; a decoder must use the same rule as the encoder.
- **Faster learning.** Variants add the concatenation of the last two phrases, or several prefixes, to learn repeats faster.
- **Entropy-coded codes.** The codes can be coded with an arithmetic coder over the table entries, at the cost of speed.

## When to use it

Use LZW to read and write the formats that require it: GIF, TIFF with LZW, PDF streams with the LZWDecode filter, and `.Z` files. For new formats, DEFLATE, Zstandard and other LZ77-family coders compress better at similar speed. No standard library has a general LZW codec (Python's, for example, has zlib, bz2 and lzma but no LZW), and there are no official test vectors for the plain method; the reference implementation is tested with code streams worked out by hand, the KwKwK case, width growth, resets and round trips.

## Pitfalls

- **The KwKwK case.** A decoder that looks up every code in its table fails on inputs such as $abababab$, where a code arrives one step before the decoder has made its entry. Handle $c_k = next$ as in line L14, and reject $c_k > next$.
- **The code width.** The encoder and the decoder must change width at the same code. The decoder is one entry behind, so the rule differs by one between the two sides; an off-by-one error here breaks the stream after code 511.
- **Early change.** GIF, `compress`, TIFF and PDF do not all change width at the same point; check the rule of the format.
- **Bit order.** GIF and `compress` pack from the least significant bit; TIFF and PDF from the most significant bit.
- **compress groups.** Unix `compress` writes codes in groups of eight; when the width changes or after a clear, it skips to the end of the current group. A `.Z` reader must skip the same bits.
- **The first code after a clear** must be a single symbol, and the decoder must not add a table entry for it.

## Implementations

## History

Terry Welch, at Sperry Research Center, published the method in IEEE Computer in June 1984, as a version of LZ78 simple enough for hardware in disk and tape controllers. Unix `compress` (1985) and the GIF format of CompuServe (1987, revised as GIF89a in 1990) adopted it, and it went into TIFF, PostScript and PDF. Welch's employer held a US patent on the method (US 4,558,302, later owned by Unisys), and its licence claims on GIF software in the 1990s led to the design of the PNG format, which uses DEFLATE; the US patent expired in 2003.

## References
