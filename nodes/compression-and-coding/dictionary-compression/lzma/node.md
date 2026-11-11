---
tag: KBKFC6
kind: algorithm
slug: lzma
name: LZMA
aliases:
- Lempel-Ziv-Markov chain algorithm
- LZMA1
- .lzma file format
area: compression-and-coding/dictionary-compression
level: advanced
summary: "Igor Pavlov's LZ77 coder: literals, matches and four repeated distances, coded bit by bit with an adaptive binary range coder and a 12-state context."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of uncompressed bytes, m: the number of compressed bytes, c: "lc + lp, the number of literal context and position bits"}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(2^c)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 2001
  people: [Igor Pavlov]
  note: Igor Pavlov designed LZMA for the 7z format of his 7-Zip archiver, which 7-Zip 2.30 Beta 2 (2001-08-30) added. The .xz format of 2009 wraps the later LZMA2.
prereqs: [lz77, back-reference, range-coding]
see_also: [deflate, zstandard, brotli, adaptive-modeling, context-modeling, optimal-parsing, match-finding, arithmetic-coding]
sources:
  - url: https://www.7-zip.org/sdk.html
    title: Igor Pavlov, LZMA SDK, file DOC/lzma-specification.txt, LZMA specification (draft version), 2015-06-14
    locator: "sections lzma file format, Range Decoder, The Bit Decoding with Probability Model, The Literal Decoding, The match length decoding, The match distance decoding, The main loop of decoder"
  - url: https://tukaani.org/xz/xz-file-format.txt
    title: Lasse Collin and Igor Pavlov, The .xz File Format, version 1.2.1 (2024-04-08)
    locator: Section 5.3.1 (LZMA2, filter ID 0x21, one-byte dictionary size)
  - url: https://www.7-zip.org/history.txt
    title: Igor Pavlov, 7-Zip history of changes
    locator: entry 2.30 Beta 2, 2001-08-30 (the new 7z format)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding window parse)
---

LZMA is the compression method of the 7z archive format and of `.lzma` files, and the core of the LZMA2 method in `.xz` files. It parses the input as in [LZ77](/lz77/), into literals and matches, and keeps the four most recent match distances so that a match at one of them costs few bits. It then codes every decision, bit by bit, with a binary [range coder](/range-coding/) whose probabilities adapt as it goes. The probability of each bit depends on a 12-state summary of the last few decisions, on the low bits of the position and, for literals, on the previous byte. These contexts are what the "Markov chain" in the name refers to.

## In plain words

The encoder turns the data into a list of steps: "write this byte", "copy this many bytes from that far back", or "copy from the same distance as one of the last four copies". Then it codes each step as a short list of yes-or-no answers, such as "is this a copy?" and "is it a repeat of the last distance?".

Each answer goes to a range coder. For each question, both sides keep a guess of how likely the answer is to be "no". A likely answer costs much less than one bit, and an unlikely one costs more. After each answer, both sides move the guess a little toward what happened. The guess for a question depends on what the last few steps were, so the coder learns patterns such as "after a copy, another copy is likely".

## The problem

The task is [lossless compression](/lossless-compression/) of a byte string $x \in \Sigma^n$, $\Sigma = \lbrace 0, \ldots, 255 \rbrace$. The analysis is worst case for the cost, and the model is [adaptive](/adaptive-modeling/): no probabilities are sent. The specification in the LZMA SDK fixes the decoder; the encoder is free. This page covers the LZMA method and the `.lzma` file header. It does not cover the 7z container or the LZMA2 chunks of `.xz` files.

### The .lzma file

| offset | size | field |
|---|---|---|
| 0 | 1 | properties: $(pb \cdot 5 + lp) \cdot 9 + lc$, with $lc \le 8$, $lp \le 4$, $pb \le 4$ |
| 1 | 4 | dictionary size, little endian; a decoder uses at least $2^{12}$ |
| 5 | 8 | uncompressed size, little endian; all ones means "unknown, the stream ends with an end marker" |
| 13 | | the range coder stream; its first byte is always 0 |

The default properties are $lc = 3$, $lp = 0$, $pb = 2$, which give the byte 5D.

### The binary range coder

The decoder keeps two 32-bit numbers, $range$ and $code$, and starts with $range = 2^{32} - 1$ and $code$ = the 4 bytes after the leading 0. Each adaptive bit has an 11-bit probability $p$ that the bit is 0, with start value $1024$ (one half):

```pseudo id=bit
DECODE-BIT(p)
B1  bound ← ⌊range / 2^11⌋ · p
B2  if code < bound then range ← bound; p ← p + ⌊(2048 − p) / 32⌋; b ← 0
B3  else code ← code − bound; range ← range − bound; p ← p − ⌊p / 32⌋; b ← 1
B4  if range < 2^24 then range ← 256 · range; code ← 256 · code + the next byte
B5  return b
```

So the probability moves $1/32$ of the way toward the bit it saw. *Direct bits* use a fixed probability one half: $range$ is halved and $code$ is compared with it. A number of $k$ bits is coded with a *bit tree*: $2^k - 1$ probabilities, one per prefix of the number, read from the high bit down, or from the low bit up in the *reverse* tree.

### The model

- **Literals.** A literal uses one of $2^{lc + lp}$ tables of 768 probabilities, chosen by the high $lc$ bits of the previous byte and the low $lp$ bits of the position. After a match, the decoder also uses the *match byte*, the byte at distance $rep0$: while the bits of the literal agree with the bits of the match byte, each bit uses a probability chosen by the match byte's bit too.
- **Lengths.** A match length $\ell$ from 2 to 273 is coded as $\ell - 2$: a choice bit and 3 bits for 0 to 7, two choice bits and 3 bits for 8 to 15, two choice bits and 8 bits for 16 to 271. The two 3-bit trees are chosen by the low $pb$ bits of the position. Normal matches and repeated matches have separate length coders.
- **Distances.** A distance $d + 1$ is coded as $d$: a 6-bit *slot* (the position of the top bit of $d$ and the bit below it), with one of 4 trees chosen by $\min(\ell - 2, 3)$, then the remaining low bits. For slots 4 to 13 the low bits use reverse trees; for slots 14 and up, all but the last 4 bits are direct bits and the last 4 use one shared reverse tree.
- **State and repeated distances.** The state $s \in \lbrace 0, \ldots, 11 \rbrace$ records the kinds of the last few steps: states 0 to 6 follow a literal and 7 to 11 follow a match. The decoder keeps $rep0, \ldots, rep3$, the last four distances (minus 1). The bits that choose the kind of step use probabilities chosen by $s$, and some also by the low $pb$ bits of the position.

| step | its bits | next state |
|---|---|---|
| literal | IsMatch 0 | $0$ if $s < 4$, $s - 3$ if $s < 10$, else $s - 6$ |
| match | IsMatch 1, IsRep 0, length, distance | 7 if $s < 7$, else 10 |
| short rep (1 byte at $rep0$) | IsMatch 1, IsRep 1, IsRepG0 0, IsRep0Long 0 | 9 if $s < 7$, else 11 |
| rep match at $rep_i$ | IsMatch 1, IsRep 1, then IsRepG0, IsRep0Long, IsRepG1, IsRepG2 to choose $i$, then length | 8 if $s < 7$, else 11 |

A match puts its distance in front of the four; a rep match with $i \ge 1$ moves $rep_i$ to the front. The *end marker* is a match with the distance $2^{32}$, that is $d = 2^{32} - 1$.

## The algorithm

The decoder, with the steps of the table above:

```pseudo id=main
LZMA-DECODE(s)
L1  read lc, lp, pb, the dictionary size and n from the header; start the range decoder; set every probability to 1024
L2  state ← 0; rep0, rep1, rep2, rep3 ← 0; out ← empty
L3  loop
L4      if n is known and |out| = n and code = 0 then return out
L5      if BIT(IsMatch[state, |out| mod 2^pb]) = 0 then
L6          append DECODE-LITERAL(state, rep0) to out; state ← the next state after a literal; continue
L7      if BIT(IsRep[state]) = 0 then
L8          (rep3, rep2, rep1) ← (rep2, rep1, rep0); ℓ ← LENGTH(normal length coder); state ← 7 or 10
L9          rep0 ← DISTANCE(ℓ); if rep0 = 2^32 − 1 then return out           ▷ end marker
L10     else if BIT(IsRepG0[state]) = 0 then
L11         if BIT(IsRep0Long[state, |out| mod 2^pb]) = 0 then append out[|out| − rep0 − 1]; state ← 9 or 11; continue
L12     else move rep1, rep2 or rep3 to the front, chosen by IsRepG1 and IsRepG2
L13     if this is a rep match then ℓ ← LENGTH(rep length coder); state ← 8 or 11
L14     if rep0 ≥ |out| or rep0 ≥ the dictionary size then fail
L15     repeat ℓ + 2 times: append out[|out| − rep0 − 1] to out
```

Here BIT is DECODE-BIT with the given probability, and the end-of-input checks of the specification are left out: a literal, short rep or match must not pass $n$ when $n$ is known, and the end marker must come with $code = 0$.

The encoder is free. The reference encoder searches with binary trees or hash chains and chooses among several parses by their estimated cost in bits, an [optimal parsing](/optimal-parsing/) method. Ours is a simpler greedy encoder:

1. At position $p$, measure the match length at each of $rep0, \ldots, rep3$, and find the longest match through a hash chain of 3-byte strings, with at most 24 candidates.
2. If the best repeated match has at least 2 bytes and at most one byte less than the best match, code it as a rep match. Else, if the best match has at least 3 bytes, code it as a match. Else, if $x[p] = x[p - rep0 - 1]$, code a short rep. Else code a literal.
3. After the last byte, flush the range encoder: it writes out its low end with the pending carry.

The range encoder is the mirror of DECODE-BIT: it keeps $low$ and $range$, adds $bound$ to $low$ for a 1, and on each shift writes the top byte of $low$. A carry out of $low$ can change bytes already decided, so it holds back the last byte and any run of FF bytes after it until the carry is known.

## Example

Compress $x$ = `red fish, red dish` (18 bytes) with $lc = 3$, $lp = 0$, $pb = 2$. Our encoder makes these steps:

| position | step | state before, after | bits of the step |
|---|---|---|---|
| 0 to 9 | 10 literals `red fish, ` | 0, 0 | IsMatch 0, then 8 literal bits each |
| 10 | match, distance 10, length 4 (`red `) | 0, 7 | IsMatch 1, IsRep 0, length 2 as 0 010; $d = 9$ = 1001 as slot 6 and the two low bits 01 in a reverse tree |
| 14 | literal `d`, with match byte `f` | 7, 4 | IsMatch 0, then 8 bits in the match-byte mode |
| 15 | rep match at $rep0$ = 9, length 3 (`ish`) | 4, 8 | IsMatch 1, IsRep 1, IsRepG0 0, IsRep0Long 1, length 1 as 0 001 |

The match byte of the literal at position 14 is $x[14 - 10] = $ `f` = 0110 0110. The literal `d` is 0110 0100. Its first 6 bits agree with `f`, so they use the match-byte probabilities; the 7th bit differs, and after it the last bit uses the plain probabilities. The rep match then reuses the distance 10 without coding it again.

The range coder turns these steps into 19 bytes: 00 39 19 48 AF FE 99 8B 0D BB 42 17 56 38 77 28 68 E0 00. With the 13-byte header 5D 00 00 10 00 12 00 00 00 00 00 00 00 (dictionary $2^{20}$, size 18), the file has 32 bytes, and the `lzma` module of Python (liblzma) decodes it to $x$. On so short an input the 13-byte header and the start-up of the adaptive model cost more than they save.

## Correctness

The decoder of lines L1 to L15 inverts the encoder in two layers. First, the range coder: let $A$ be the whole output read as one number. Each coded bit narrows the encoder's interval $[low, low + range)$ to the part for that bit, so $A$ lies in every interval, and the decoder's $code$ is $A - low$ at the same scale. Then $code < bound$ holds exactly when the bit was 0, so the decoder gets each bit back, as long as both sides use the same probability, and they do because both update it with the same rule. Second, the steps: the encoder only writes a match or rep match when the bytes at that distance equal the next bytes of $x$, and the decoder picks every probability from the state, the repeated distances, the position and the previous bytes, which by induction are equal on both sides. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Decoding.** A literal costs at most 9 bit decodes plus the choice bit, and a match at most about 50 (choice bits, at most 10 length bits, 6 slot bits and at most 30 distance bits), plus the bytes it copies. Each bit decode reads at most one byte, since after a bit $range \ge 2^{13} \cdot 31 \ge 2^{17}$ and one shift by 8 bits brings it back above $2^{24}$. So decoding takes $\Theta(n + m)$ time.
- **Space.** Besides the output, which serves as the window, the decoder keeps $1846 + 768 \cdot 2^{lc + lp}$ probabilities (the count in the specification), $\Theta(2^{lc + lp})$, and a few numbers.
- **Encoding.** Our greedy encoder spends $O(\ell)$ per candidate of the hash chain and a constant number of bit codings per step, so with a chain of at most 24 candidates it runs in $O(n \cdot 24 \cdot 273)$ time in the worst case and in about linear time on typical data. The reference encoder's optimal parse is slower and smaller.

## Properties

- **Adaptive.** No tables or code lengths are sent. The cost is that the model needs some input to learn, so tiny inputs do not shrink.
- **Bit-serial.** Every bit of every field goes through the range coder, and the next probability depends on the bit just decoded. This makes the decoder slower than a table-driven [DEFLATE](/deflate/) or [Zstandard](/zstandard/) decoder, and hard to run in parallel.
- **Large window.** The dictionary size can be up to $2^{32} - 1$ bytes.
- **Fine contexts.** The properties $lc$, $lp$ and $pb$ let the model fit data with a fixed record size: for example, $lp = 2$ and $pb = 2$ suit 4-byte records.
- **No checksum.** The `.lzma` format has no check of the content. The `.xz` format adds one.

## Variants and improvements

- **LZMA2.** The `.xz` format (filter ID 0x21) uses LZMA2, which in the words of the xz specification uses LZMA inside but adds flushing of the encoder, uncompressed chunks, easier stateful decoders and better support for multithreading. It keeps $lc + lp \le 4$ and codes the dictionary size in one byte.
- **Filters.** 7z and xz can put a filter before LZMA, for example one that turns relative branch targets in machine code into absolute ones, so that they repeat.
- **Better parsing.** The reference encoder uses an optimal parse over prices of the adaptive model; this is the main difference between fast and high levels.

## When to use it

Use LZMA when the output size matters more than the speed: software distribution, archives that are written once and read many times, and file systems for firmware. It decodes far slower than LZ4 or Zstandard and compresses slower still at its high levels. For new formats, LZMA2 in `.xz` or Zstandard at a high level are the usual choices.

## Pitfalls

- **Unknown size.** A size of all ones means the stream ends with an end marker; a known size may still be followed by one. A decoder must handle both, and must check $code = 0$ at the end.
- **Distances.** Line L14 must test $rep0$ against the output written so far. A repeated match at the very start, before any byte, is not valid.
- **The first byte.** The range coder stream starts with a 0 byte that carries no data. A decoder must not drop it, and an encoder must write it.
- **Carry.** An encoder that writes the top byte of $low$ at once breaks when a later addition carries into it. Hold back the last byte and the run of FF bytes after it.
- **Many states, one slip.** The 12-state rules, the order of the repeated distances and the matched-literal loop must be exact. A small mistake still decodes the first bytes and then goes wrong, so test against a reference decoder.

## Implementations

## History

Igor Pavlov designed LZMA for the 7z format of 7-Zip; the history of 7-Zip lists the new 7z format in version 2.30 Beta 2 of 2001-08-30. He published the LZMA SDK with a reference decoder and encoder; its draft specification of the format has the date 2015-06-14. Lasse Collin and Igor Pavlov designed the `.xz` format, whose first official version is dated 2009-01-14, and it uses LZMA2 instead of plain LZMA. The range coder is the method of G. N. N. Martin (1979), and the parse is that of Ziv and Lempel (1977).

## References
