---
tag: 9ZG9VC
kind: concept
slug: back-reference
name: Back-reference
aliases:
- copy reference
- pointer to earlier text
- distance-length pair
area: compression-and-coding/dictionary-compression
level: intro
summary: A (distance, length) token that tells the decoder to copy symbols from earlier in its own output, the basic token of LZ77-style coders.
prereqs: [dictionary-based-compression]
see_also: [lz77, lzss, lempel-ziv-factor, match-finding, run-length-encoding, deflate, adaptive-dictionary-compression, string-compression-by-period]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: P. Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996
    locator: Section 3.2.5 (lengths 3 to 258, distances 1 to 32,768) and Section 3.2.3 (a copy may overlap the bytes it produces)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the pointer into the sliding window, with a reproduction that may extend into the new text)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Section 6.3, LZ77 (Sliding Window), page 334
  - url: https://www.rfc-editor.org/rfc/rfc8878
    title: Y. Collet and M. Kucherawy, RFC 8878, Zstandard Compression and the 'application/zstd' Media Type, February 2021
    locator: Section 3.1.1.5, Repeat Offsets
---

A back-reference is a token $(d, \ell)$ that tells the decoder to copy $\ell$ symbols, starting $d$ positions back in the output it has already produced. It is the way an [LZ77](/lz77/)-style coder writes a repeat: in place of a phrase that occurred before, it writes where the earlier copy is and how long it is. The copy may run into the symbols it is producing ($\ell > d$), and then one token writes a periodic string of any length.

## In plain words

When you see a word that you saw a moment ago, you can say "same as the word five words back" in place of the word. A back-reference does this for any piece of text. It says how far back to look and how many letters to take.

The reader follows the instruction one letter at a time. It looks back, takes one letter, writes it at the end, and does this again. Because it writes each letter before it reads the next one, the copy can reach into the part that it is writing now. "Go back two letters and copy six" after "ab" gives "ababab": each new letter repeats the letter two places before it.

## The idea

Let $S$ be the output so far, with $|S| = p$. The token $(d, \ell)$, with $1 \le d \le p$ and $\ell \ge 1$, appends $\ell$ symbols by the rule

$$S[p + k] = S[p + k - d] \qquad \text{for } k = 1, 2, \ldots, \ell,$$

where each symbol is written before the next one is read. When $\ell \le d$ the token copies the existing substring $S[p-d+1 .. p-d+\ell]$. When $\ell > d$ the source and the target overlap, and the new text is the first $\ell$ symbols of the infinite repetition of $S[p-d+1 .. p]$: a string with period $d$. In the LZ77 dictionary view, the token points to an entry of the window, and the overlap makes the dictionary include strings that end after the current position.

**Cost of a token.** With a window of $W$ symbols and lengths up to $L_{\max}$, a fixed-width token needs $\lceil \log_2 W \rceil + \lceil \log_2 L_{\max} \rceil$ bits, while a literal symbol needs about $\log_2 \sigma$ bits. A back-reference saves space only when $\ell$ is at least a *minimum match length* $m$, so formats set a smallest allowed length: 3 in DEFLATE, and a value computed from the field widths in [LZSS](/lzss/). Formats with an entropy coder (DEFLATE, Zstandard, LZMA) code the lengths and distances with variable-length codes, so short distances and common lengths cost less.

**Where the token comes from.** The encoder must find, at each position, an earlier occurrence of the text that follows; that is [match finding](/match-finding/). Taking the longest match at each step gives [greedy parsing](/greedy-parsing/); waiting one step for a longer match is [lazy matching](/lazy-matching/); choosing tokens to minimize the total bit cost is [optimal LZ parsing](/optimal-lz-parsing/). Each phrase of the [Lempel-Ziv factorization](/lempel-ziv-factorization/) is one back-reference or one new symbol (see [Lempel-Ziv factor](/lempel-ziv-factor/)).

**Decoding.** The decoder runs the rule above. A fast decoder copies blocks with a memory copy routine when $d \ge \ell$ (no overlap). When $d < \ell$ it must not use a routine that reads all the source before it writes, such as `memmove`, because that does not repeat the pattern; it copies one symbol at a time, or it copies the $d$-symbol pattern and doubles it. A decoder must check that $d \le p$; a distance that points before the start of the output is an error in the input, and a decoder that does not check it reads memory it does not own.

**Repeat offsets.** Many structured inputs (tables, records, images) repeat with the same distance many times. Zstandard keeps the last three distances (RFC 8878, Section 3.1.1.5) and LZMA keeps the last four, and a token can name one of them with a short code in place of the full distance.

## Examples

**Overlap gives a period.** After $S = ab$, the token $(2, 6)$ appends $ababab$, so $S = abababab$. This is the LZ77 triple $(2, 5, b)$ of [LZ77](/lz77/) on $abababab$ in another form: five copied symbols and one literal.

**A run.** After $S = a$, the token $(1, 7)$ gives $aaaaaaaa$. A back-reference with $d = 1$ is [run-length encoding](/run-length-encoding/) of the last symbol, so an LZ77 coder needs no separate run mode.

**No overlap.** After $S = abracad$ ($p = 7$), the token $(7, 4)$ copies $S[1..4] = abra$ and gives $abracadabra$.

**DEFLATE.** In DEFLATE (RFC 1951, Section 3.2.5) a length is 3 to 258 and a distance is 1 to 32,768. Section 3.2.3 says that the referenced string may overlap the current position: if the last two bytes are $X, Y$, the pair (length 5, distance 2) adds $X, Y, X, Y, X$. The length and distance codes are then Huffman coded.

**Byte-by-byte decoder.**

```text
copy(S, d, l):
    if d < 1 or d > |S|: fail
    start = |S| - d
    for k = 0 .. l - 1:
        append S[start + k] to S
```

## Where it is used

- **Every LZ77-type format.** [DEFLATE](/deflate/), [LZ4](/lz4/), [Snappy](/snappy/), [LZO](/lzo/), [Zstandard](/zstandard/), [Brotli](/brotli/), [LZMA](/lzma/) and [LZX](/lzx/) write repeats as back-references and differ in how they code $d$ and $\ell$.
- **Delta and patch formats.** A patch tool can write a new file as back-references into an old file plus literals, which is a back-reference into a [static dictionary](/static-dictionary-compression/).
- **String algorithms.** The phrases of the [Lempel-Ziv factorization](/lempel-ziv-factorization/) are back-references to earlier text, and the [LZ-index](/lz-index/) and other [compressed indexes](/compressed-indexing/) store them.

A back-reference with $\ell > d$ writes a string with period $d$; [string compression by period](/string-compression-by-period/) asks for the shortest such period of a whole string.

## References
