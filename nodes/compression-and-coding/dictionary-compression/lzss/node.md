---
tag: M0JP2V
kind: algorithm
slug: lzss
name: LZSS
aliases:
- Lempel-Ziv-Storer-Szymanski
area: compression-and-coding/dictionary-compression
level: intro
summary: LZ77 variant that writes a flag bit and then a literal or a (distance, length) pair, and uses a pair only when it is shorter than the literals.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the input, w: the window size}
  time: {worst: O(n·w)}
  space: {aux: O(w)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1982
  people: [James A. Storer, Thomas G. Szymanski]
  note: Storer and Szymanski studied data compression by pointers to earlier text in the Journal of the ACM in 1982.
prereqs: [lz77]
see_also: [lz77, back-reference, match-finding, lazy-matching, optimal-lz-parsing, deflate, lz4, greedy-parsing]
sources:
  - paper: doi:10.1145/322344.322346
    title: James A. Storer and Thomas G. Szymanski, Data compression via textual substitution, Journal of the ACM 29(4), 1982
    locator: pages 928 to 951 (compression by pointers to earlier text mixed with plain symbols, and the cost of pointers against the text they replace)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Section 6.4, LZSS, page 339
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapter on dictionary techniques (LZSS among the LZ77 variants)
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: P. Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996
    locator: Section 3.2.5 (literal and length codes in one alphabet, with a separate distance code)
---

LZSS is a variant of [LZ77](/lz77/) in which each token is either one literal symbol or one [back-reference](/back-reference/) $(d, \ell)$, with a flag bit in front that says which. It drops the literal that LZ77 adds to every copy, and it uses a copy only when the copy takes fewer bits than the literals it replaces. It solves [lossless compression](/lossless-compression/), and its token stream, with an entropy coder on top, is the plan of DEFLATE and most later LZ coders. The idea goes back to the study of textual substitution by Storer and Szymanski (1982).

## In plain words

The coder reads the text from left to right. At each place it searches the recent text for the longest piece that matches what comes next. If the piece is long enough, it writes a "copy" mark, how far back the piece is, and how long it is. If the piece is short or missing, it writes a "letter" mark and one letter.

A copy costs more bits than one letter. So a copy of one or two letters can cost more than the letters themselves. The coder knows the cost of each, and it uses a copy only when the copy is cheaper.

The reader reads one mark at a time. A letter mark gives a letter. A copy mark gives a place and a length, and the reader copies letter by letter from there.

## The problem

The input is a string $T = T[1..n]$ of bytes. The output is a bit string that the decoder turns back into $T$. In the fixed-width format of this page, a literal costs $1 + 8 = 9$ bits and a pair costs $1 + b_d + b_\ell$ bits, where $b_d$ bits hold $d - 1$ (so the window has $W = 2^{b_d}$ positions) and $b_\ell$ bits hold $\ell - m$. A pair of length $\ell$ replaces $\ell$ literals, so it is worth it when $1 + b_d + b_\ell < 9\ell$. The smallest such length is the *minimum match length*

$$m = \left\lfloor \frac{1 + b_d + b_\ell}{9} \right\rfloor + 1,$$

and the largest length is $L_{\max} = m + 2^{b_\ell} - 1$. With $b_d = 12$ and $b_\ell = 4$, a pair costs 17 bits, $m = 2$, $W = 4096$ and $L_{\max} = 17$.

## The algorithm

```pseudo id=main
LZSS-ENCODE(T, W, Lmax, m)                 ▷ T[1 .. n]
L1  i ← 1
L2  while i ≤ n do
L3      (d, ℓ) ← the longest prefix of T[i .. n] of length at most Lmax that starts at some j in [i − W, i − 1], nearest j on a tie
L4      if ℓ ≥ m then
L5          output flag 1, then d − 1 and ℓ − m
L6          i ← i + ℓ
L7      else
L8          output flag 0, then T[i]
L9          i ← i + 1

LZSS-DECODE(bits)
L10 S ← the empty string
L11 while the bits that remain hold a whole token do
L12     read a flag bit
L13     if flag = 1 then read d and ℓ; repeat ℓ times: append S[|S| − d + 1] to S
L14     else read a byte c and append c to S
L15 return S
```

Line L3 is the same search as in [LZ77](/lz77/): the copy may run past $i$ (overlap), and an exhaustive scan of the window takes $O(W)$ candidates. Unlike LZ77, the length may reach $n - i + 1$, the end of the input, because no literal must follow. The encoder pads the last byte with 0 bits. The padding has fewer than 8 bits, and its first bit reads as a literal flag that asks for 8 more bits, so line L11 stops the decoder before the padding.

## Example

With $b_d = 12$, $b_\ell = 4$, $m = 2$:

| Input | Tokens | Bits |
|---|---|---|
| abracadabra | a, b, r, a, c, a, d, $(7, 4)$ | $7 \cdot 9 + 17 = 80$, so 10 bytes |
| aaaaaaaa | a, $(1, 7)$ | $9 + 17 = 26$, so 4 bytes |
| abababab | a, b, $(2, 6)$ | $2 \cdot 9 + 17 = 35$, so 5 bytes |

On $abracadabra$ the copy $abra$ at position 8 now has length 4, one more than in LZ77, since no literal must follow it. The single copies of $a$ at positions 4 and 6 would have length 1, less than $m$, so they stay literals.

**The bits for aaaaaaaa.** The literal is flag 0 and $a = 01100001$. The pair is flag 1, then $d - 1 = 0$ in 12 bits, then $\ell - m = 5$ in 4 bits. The 26 bits $0\,01100001\,1\,000000000000\,0101$, padded with six 0 bits, give the bytes 30 C0 01 40 in hexadecimal.

## Correctness

The decoder keeps the invariant that after it has read $t$ tokens, $S$ equals the prefix of $T$ covered by the first $t$ tokens of the encoder. A literal token appends the right symbol. A pair made at position $i$ satisfies $T[i - d + k] = T[i + k]$ for $0 \le k < \ell$, and the decoder copies one symbol at a time, so each symbol it reads is already written, as in LZ77. The bit stream can be read without ambiguity: the flag says which kind of token follows, the fields have fixed widths, and the padding is too short to be a token. The full proof is below.

## Complexity

**Time.** The search of line L3 costs $O(W(\ell + 1))$ at a position where the token covers $\max(\ell, 1)$ symbols, so the encoder takes $O(nW)$ time with an exhaustive search; real coders use [match finding](/match-finding/) with hash chains or trees. The decoder takes $O(n)$ time.

**Space.** The encoder and the decoder need the last $W$ symbols, $O(W)$.

**Output size.** A pair is used only when it is shorter than its literals, so the output never has more than $9n$ bits, plus fewer than 8 bits of padding: at most 1 bit per byte more than the input. LZ77 triples on a string with no repeats cost about $\log_2 W + \log_2 (L_{\max} + 1)$ more bits for every symbol.

## Properties

- **Lossless and deterministic.** The output is a function of $T$ and the field widths.
- **Streaming.** Both sides keep only the window and a short lookahead.
- **Prefix-free tokens.** A flag bit and fixed-width fields make each token readable on its own.
- **Greedy, not optimal.** Taking the longest match is not always cheapest: a shorter copy here can allow a much longer copy at the next position. [Lazy matching](/lazy-matching/) and [optimal LZ parsing](/optimal-lz-parsing/) do better.
- **No standard codec.** There is no single LZSS format; programs that use the name differ in field widths, flag layout and the order of bits. No standard library has an LZSS codec and there are no official test vectors, so the reference implementation is tested by round trips and by streams worked out by hand.

## Variants and improvements

- **Flags in groups.** Many programs gather 8 flag bits into one byte in front of the 8 tokens that they describe, so that literals stay byte-aligned.
- **Entropy-coded tokens.** [DEFLATE](/deflate/) puts literals and lengths into one Huffman alphabet, so the flag is not a separate bit, and codes distances with a second Huffman code. [LZMA](/lzma/), [Zstandard](/zstandard/) and [Brotli](/brotli/) follow the same plan with other entropy coders.
- **Byte-aligned tokens.** [LZ4](/lz4/) and [Snappy](/snappy/) write literal runs and copies in whole bytes, which is fast to decode.
- **Better parses.** [Lazy matching](/lazy-matching/), and [optimal LZ parsing](/optimal-lz-parsing/) as a shortest path over the positions, with the real token costs.
- **Hash-chain search.** Hash the next $m$ or 3 symbols and walk a chain of earlier positions with the same hash, with a limit on the chain length.

## When to use it

Use LZSS when you need a simple LZ coder with a small, fast decoder and a guaranteed small worst-case growth: firmware images, game data, embedded systems and the like. When the ratio matters, use a format that adds an entropy coder, such as [DEFLATE](/deflate/) or [Zstandard](/zstandard/).

## Pitfalls

- **The minimum match.** Using pairs of length 1 or 2 when they cost more than the literals makes the output larger. Compute $m$ from the field widths, and store $\ell - m$ so that no code is wasted on lengths that are never used.
- **Distance off by one.** Store $d - 1$, since $d = 0$ is never a valid distance; mixing up $d$ and $d - 1$ between encoder and decoder breaks every copy.
- **Overlapping copies.** The decoder must copy one symbol at a time when $\ell > d$.
- **Padding and short pairs.** The decoder must stop when the remaining bits cannot hold a whole token. A fixed test such as "at least 9 bits remain" is wrong when a pair has fewer than 9 bits ($m = 1$): it drops a final pair that ends on a byte boundary.
- **Bad input.** Reject $d > |S|$.

## Implementations

## History

Storer and Szymanski (1982) studied compression by textual substitution: a text is written as a mix of plain symbols and pointers to other copies of the same text. They proved that finding the best such scheme is NP-hard for many of its forms. The coder named after them applies to the LZ77 window the rule that a pointer is used only when it is shorter than the text it replaces, with a flag bit per token. In the late 1980s it spread in simple public programs, and DEFLATE (RFC 1951, 1996) is LZSS with Huffman-coded tokens.

## References
