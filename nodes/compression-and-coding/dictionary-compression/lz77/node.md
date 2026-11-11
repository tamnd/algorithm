---
tag: 380S00
kind: algorithm
slug: lz77
name: LZ77
aliases:
- Ziv-Lempel 1977
- LZ77 sliding window
area: compression-and-coding/dictionary-compression
level: intro
summary: Sliding-window coder that writes the text as triples (distance, length, next symbol), each a copy of recent text plus one literal symbol.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the input, w: the window size}
  time: {worst: O(n·w)}
  space: {aux: O(w)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1977
  people: [Jacob Ziv, Abraham Lempel]
  note: Ziv and Lempel published the sliding-window method in IEEE Transactions on Information Theory in 1977.
prereqs: [back-reference, lempel-ziv-parsing]
see_also: [lzss, lz78, lempel-ziv-factorization, match-finding, lazy-matching, optimal-lz-parsing, deflate, ziv-lempel-entropy-theorem]
sources:
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the buffer of already coded and lookahead symbols, the codeword of pointer, length and last symbol, and the universality result)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Section 6.3, LZ77 (Sliding Window), page 334
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 5, Dictionary Techniques (the LZ77 approach, with a worked example of an overlapping copy)
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapter on dictionary techniques (LZ77 and its variants)
---

LZ77 is the sliding-window compressor of Ziv and Lempel (1977). It reads the text from left to right and writes it as a sequence of triples $(d, \ell, c)$: copy $\ell$ symbols from $d$ positions back in the recent text (the *window*), then add the literal symbol $c$. It solves [lossless compression](/lossless-compression/) with an [adaptive dictionary](/adaptive-dictionary-compression/) that is the window itself, so nothing but the triples is sent. It is the ancestor of DEFLATE, LZ4, Zstandard, Brotli and LZMA, which keep its [back-references](/back-reference/) and change the way they are found and coded.

## In plain words

The coder looks at the next part of the text and searches the last few thousand letters for the longest piece that matches it. It writes three things: how far back the piece starts, how long it is, and the next letter after it. Then it moves past the piece and the letter, and searches again.

If nothing matches, the coder writes "back 0, length 0" and the letter. So every step makes progress by at least one letter.

The reader keeps the same last few thousand letters. For each step it copies the piece, letter by letter, from the place the step names, and then adds the letter. The copy may reach into the letters that it is writing now, so a short pattern can be repeated many times by one step.

## The problem

The input is a string $T = T[1..n]$ over an alphabet $\Sigma$ of $\sigma$ symbols (bytes in practice). The encoder writes a sequence of triples, and the decoder must rebuild $T$ exactly from them. Two parameters fix the format: the window size $W$, so that $1 \le d \le W$, and the largest copy length $L_{\max}$, so that $0 \le \ell \le L_{\max}$. A triple with $\ell = 0$ has $d = 0$. The goal is few triples: each one costs about $\lceil \log_2 (W+1) \rceil + \lceil \log_2 (L_{\max}+1) \rceil + \lceil \log_2 \sigma \rceil$ bits in a fixed-width code.

## The algorithm

The encoder is greedy: at each position it takes the longest copy that starts in the window, the nearest one on a tie. The copy may run past position $i$ into the text that it codes. The length is at most $n - i$, so that a next symbol always exists.

```pseudo id=main
LZ77-ENCODE(T, W, Lmax)                    ▷ T[1 .. n]
L1  i ← 1
L2  while i ≤ n do
L3      (d, ℓ) ← (0, 0)
L4      for j ← i − 1 down to max(1, i − W) do
L5          k ← 0
L6          while k < Lmax and i + k < n and T[j + k] = T[i + k] do k ← k + 1
L7          if k > ℓ then (d, ℓ) ← (i − j, k)
L8      output (d, ℓ, T[i + ℓ])
L9      i ← i + ℓ + 1
L10 return

LZ77-DECODE(triples)
L11 S ← the empty string
L12 for each triple (d, ℓ, c) in order do
L13     start ← |S| − d
L14     for k ← 1 to ℓ do append S[start + k] to S
L15     append c to S
L16 return S
```

Line L4 scans the window from the nearest start, and line L7 replaces the best match only by a strictly longer one, so ties go to the smallest distance. In line L6, $T[j + k]$ can lie at or after position $i$; this is the overlapping copy. In line L14, $start$ is fixed before the loop and $S$ grows during it, so a copy with $\ell > d$ reads symbols that the same loop has just written.

## Example

**abracadabra** with $W = 4096$:

| $i$ | rest of $T$ | longest copy in the window | triple | output so far |
|---|---|---|---|---|
| 1 | abracadabra | none | $(0, 0, a)$ | a |
| 2 | bracadabra | none | $(0, 0, b)$ | ab |
| 3 | racadabra | none | $(0, 0, r)$ | abr |
| 4 | acadabra | $a$ at 1 | $(3, 1, c)$ | abrac |
| 6 | adabra | $a$ at 4 (nearest) | $(2, 1, d)$ | abracad |
| 8 | abra | $abr$ at 1 (the length is at most $n - i = 3$) | $(7, 3, a)$ | abracadabra |

Six triples code eleven symbols. With $W = 4$, the copy at $i = 8$ cannot reach position 1, and the parse needs eight triples.

**abababab**, an overlapping copy. The triples are $(0, 0, a)$, $(0, 0, b)$, $(2, 5, b)$. To decode the third, the decoder has $S = ab$ and $start = 0$; it appends $S[1], S[2], S[3], S[4], S[5] = a, b, a, b, a$, where $S[3]$ to $S[5]$ were written by the same loop, and then appends $b$. The result is $abababab$.

**aaaaaaaa.** The triples are $(0, 0, a)$, $(1, 6, a)$: one copy with distance 1 repeats the last symbol, as [run-length encoding](/run-length-encoding/) would.

## Correctness

The decoder keeps the invariant that after $t$ triples, $S$ is the prefix of $T$ that the encoder had coded after its first $t$ triples. A triple made at position $i$ satisfies $T[i + k] = T[i - d + k]$ for $0 \le k < \ell$, by line L6. When line L14 appends its $k$-th symbol, the symbol it reads, $S[start + k]$, has index at most $|S|$ because $d \ge 1$, so it is already written, and it equals $T[i - d + k - 1]$, which equals $T[i + k - 1]$. Line L15 appends $T[i + \ell]$. So the decoder outputs $T$. The encoder ends because each step advances $i$ by $\ell + 1 \ge 1$. The full proof is below.

## Complexity

**Encoder.** At a position where the triple has length $\ell$, each of the at most $W$ candidates in line L4 matches for at most $\ell$ symbols (since $\ell$ is the maximum), so the step costs $O(W(\ell + 1))$. The steps cover $n$ symbols in total, so the encoder takes $O(nW)$ time in the worst case. This search by brute force is the slow part; real coders use [match finding](/match-finding/) with hash chains, binary trees or suffix structures, and stop early.

**Decoder.** $O(n)$ time: each output symbol is one append. It needs only the last $W$ symbols of $S$, so $O(W)$ memory when the output is streamed.

**Output size.** With $t$ triples and fixed-width fields, the output has $t\,(\lceil \log_2 (W+1) \rceil + \lceil \log_2 (L_{\max}+1) \rceil + \lceil \log_2 \sigma \rceil)$ bits. On a string with no repeats, $t = n$ and the output is larger than the input. For a stationary ergodic source, the bits per symbol tend to the entropy rate as $W$ and $L_{\max}$ grow; the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/) states the result and its conditions.

## Properties

- **Lossless and deterministic.** The decoder rebuilds $T$ exactly, and the encoder output is a function of $T$, $W$ and $L_{\max}$.
- **Streaming.** The encoder needs only the window and $L_{\max}$ symbols of lookahead; the decoder needs only the window.
- **Asymmetric.** The decoder only copies, so it is much faster than the encoder, which searches.
- **Greedy.** With an unbounded window and no length limit, the copies are the [longest previous factors](/longest-previous-factor/), and the number of triples is at most the number $z$ of [Lempel-Ziv factors](/lempel-ziv-factor/) of $T$; see [Lempel-Ziv parsing](/lempel-ziv-parsing/).
- **Fixed cost per triple.** Every triple carries a literal, even when the next symbol would start another good copy, and a copy of length 0 costs a full triple.

## Variants and improvements

- **LZSS.** Write a literal or a $(d, \ell)$ pair after a flag bit, and use a pair only when it is shorter than the literals. See [LZSS](/lzss/).
- **Entropy-coded tokens.** Code the literals, lengths and distances with [Huffman coding](/huffman-coding/) or an arithmetic coder; [DEFLATE](/deflate/), [LZMA](/lzma/), [Zstandard](/zstandard/) and [Brotli](/brotli/) do this.
- **Faster match search.** Hash the next 3 or 4 symbols and follow a chain of earlier positions with the same hash, as in DEFLATE and [LZ4](/lz4/); or keep a binary tree of the window, as in LZMA.
- **Better parsing.** [Lazy matching](/lazy-matching/) delays a match by one symbol when the next position has a longer one; [optimal LZ parsing](/optimal-lz-parsing/) picks the tokens that minimize the coded size.
- **Repeat offsets.** Keep the last few distances and code a reuse of one of them with a short code.
- **No window, no literal.** With an unbounded window and no forced literal, the parse is the [Lempel-Ziv factorization](/lempel-ziv-factorization/), which string algorithms compute in $O(n)$ time.

## When to use it

Use the LZ77 scheme when the decoder must be fast and small and the data has repeats at short range: text, program code, logs, structured records. In practice use a format built on it, such as [DEFLATE](/deflate/), [Zstandard](/zstandard/) or [LZ4](/lz4/), not plain triples. Plain LZ77 triples are a teaching format: no standard library has a codec for them, and there are no official test vectors, so the reference implementation is tested by round trips and by parses worked out by hand. For data whose repeats are far apart, use a larger window or a long-range mode; for data with few exact repeats (sound, photos), use a transform or a model-based coder.

## Pitfalls

- **No next symbol.** If the copy reaches the end of $T$, the triple has no literal to write. Limit $\ell$ to $n - i$, as line L6 does, or add an end marker.
- **Block copy.** A decoder that copies the source with `memmove` or one slice breaks on $\ell > d$, because the source is not yet written. Copy one symbol at a time, or replicate the period.
- **Bad distances.** A decoder must reject $d > |S|$ (or $d > W$); otherwise a broken or hostile input makes it read outside its buffer.
- **The name.** In string algorithms "LZ77" often means the [Lempel-Ziv factorization](/lempel-ziv-factorization/) (no window, no literal). The triple parse of this page has as many or fewer phrases; give the variant when a count matters.
- **Slow search.** The brute-force search of lines L4 to L7 is $O(W)$ per position; with $W = 32768$ it is far too slow for real data.

## Implementations

## History

Abraham Lempel and Jacob Ziv defined the complexity of a sequence by copies from its own past in 1976. In 1977 Ziv and Lempel turned the idea into a practical compressor with a bounded buffer, wrote each step as a fixed-length codeword of a pointer, a length and one symbol, and proved that it is universal: asymptotically it compresses as well as codes that are designed with knowledge of the source. Storer and Szymanski removed the forced literal in [LZSS](/lzss/) (1982). The format DEFLATE, from PKZIP, combined LZSS-style tokens with Huffman coding and became RFC 1951 in 1996; most later compressors follow the same plan.

## References
