---
tag: 3GVCEG
kind: algorithm
slug: range-coding
name: Range coding
aliases:
- range encoder
area: compression-and-coding/entropy-coding
level: advanced
summary: An interval coder that keeps a low end and a width in integer registers and writes whole bytes; a cached byte takes the carry. This page gives the binary range coder of LZMA.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of coded binary decisions, k: the number of probability counters}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(k)}
properties: {deterministic: true, online: true, recursive: false, comparison: false}
history:
  year: 1979
  people: [G. Nigel N. Martin]
  note: Martin described range encoding at a conference in Southampton in 1979; the LZMA compressor of Igor Pavlov made its binary byte-wise form common.
prereqs: [arithmetic-coding]
see_also: [asymmetric-numeral-systems, rans-coding, cabac, lzma, adaptive-modeling, context-modeling]
sources:
  - paper: "G. N. N. Martin, Range encoding: an algorithm for removing redundancy from a digitised message, Video and Data Recording Conference, Southampton, UK, July 1979"
    title: Range encoding, an algorithm for removing redundancy from a digitised message
    locator: the whole paper (a range of integers in place of a real interval, with digits written one at a time)
  - url: https://www.7-zip.org/sdk.html
    title: Igor Pavlov, LZMA specification, file DOC/lzma-specification.txt of the LZMA SDK, 2015
    locator: sections Range Decoder and The Bit Decoding with Probability Model; the encoder is RangeEnc_ShiftLow and RangeEnc_EncodeBit in C/LzmaEnc.c
  - paper: doi:10.1145/290159.290162
    title: Alistair Moffat, Radford M. Neal and Ian H. Witten, Arithmetic coding revisited, ACM Transactions on Information Systems 16(3), 1998
    locator: pp. 256 to 294 (the low and range form of the coder and the handling of a carry into the written output)
---

Range coding is an entropy coder for [lossless compression](/lossless-compression/) that keeps the current interval as an integer low end $low$ and an integer width $range$, and writes the output one byte at a time. It belongs to the same family as [arithmetic coding](/arithmetic-coding/): each coded decision with probability $p$ makes the interval about $p$ times as wide. It differs in the register layout and in how it treats a carry. The arithmetic coder of Witten, Neal and Cleary keeps $low$ and $high$, writes single bits, and defers a bit it cannot decide yet. A range coder adds to $low$ and lets a carry run into the bytes it has not written yet. This page gives the binary range coder of LZMA, with 11-bit adaptive probabilities, a shift of 5 for the update, and one cached byte that takes the carry.

## In plain words

The coder holds a stretch of whole numbers, described by where it starts and how long it is. For each yes or no decision, it cuts the stretch into two pieces in proportion to how likely each answer is, and keeps the piece of the answer that came. When the stretch gets short, the coder sends out the top byte of the start and makes the stretch 256 times longer.

Sometimes adding to the start makes a carry, like 199 plus 1 makes 200. The carry can change bytes that the coder already wanted to send. So the coder keeps the last such byte, and any run of 255 bytes behind it, in a waiting area. It sends them only when it knows that no carry can reach them.

After each decision, the guess for that kind of decision moves a little toward the answer that came.

## The problem

The input is a sequence of binary decisions $b_1 \ldots b_n$. Each decision has a context $c_j$ from a fixed set of $k$ contexts, and each context owns an adaptive probability $prob[c]$, the chance of a 0 times $2^{11}$. The output is a byte string from which the decoder, which sees the same contexts, gets the decisions back. Larger alphabets are coded as a path of binary decisions in a bit tree, as in the order-0 byte coder of the implementation, where each byte is 8 decisions over 255 counters. The bound of this page is for each input, with no source model: it compares the output to the sum of $\lg(1/p_j)$, where $p_j$ is the probability that the model gave to the decision that came.

## The algorithm

The encoder keeps $low$ (33 bits are enough), $range$ (32 bits), the cached byte $cache$ and the count $cs$ of bytes that wait: the cached byte and $cs - 1$ bytes 0xFF behind it. The decoder keeps $range$ and $code$, 32 bits each.

```pseudo id=main
INIT-ENCODER
L1  low ← 0, range ← 2^32 − 1, cache ← 0, cs ← 1

ENCODE-BIT(prob, bit)
L2  bound ← ⌊range / 2^11⌋ · prob
L3  if bit = 0 then range ← bound
L4      prob ← prob + ⌊(2^11 − prob) / 2^5⌋
L5  else low ← low + bound, range ← range − bound
L6      prob ← prob − ⌊prob / 2^5⌋
L7  while range < 2^24 do range ← 2^8 · range, SHIFT-LOW

FLUSH
L8  call SHIFT-LOW five times

ENCODE(b[1..n], c[1..n])
L9  for j ← 1 to n do ENCODE-BIT(prob[c[j]], b[j]); then FLUSH

ENCODE-BYTE(y)                                   ▷ bit tree of 255 counters
L10 node ← 1; for i ← 7 down to 0 do ENCODE-BIT(prob[node], bit i of y)
L11     node ← 2 · node + (bit i of y)

SHIFT-LOW
L12 if low < 0xFF000000 or low ≥ 2^32 then
L13     write (cache + ⌊low / 2^32⌋) mod 256, then cs − 1 bytes (0xFF + ⌊low / 2^32⌋) mod 256; cs ← 0
L14     cache ← ⌊low / 2^24⌋ mod 256
L15 cs ← cs + 1
L16 low ← (low mod 2^24) · 2^8

INIT-DECODER(input)
L17 range ← 2^32 − 1; read one byte, which must be 0; code ← the next 4 bytes (0 past the end)

DECODE-BIT(prob)
L18 bound ← ⌊range / 2^11⌋ · prob
L19 if code < bound then range ← bound, update prob as in line L4, bit ← 0
L20 else code ← code − bound, range ← range − bound, update prob as in line L6, bit ← 1
L21 if range < 2^24 then range ← 2^8 · range, code ← 2^8 · code + the next byte
    return bit

DECODE(input, c[1..n])
L22 for j ← 1 to n do output DECODE-BIT(prob[c[j]])

DECODE-BYTE
L23 node ← 1; while node < 256 do node ← 2 · node + DECODE-BIT(prob[node])
L24 output node − 256
```

Line L2 splits the range: the 0 bit gets the lower part of width $bound$, about $range \cdot prob / 2^{11}$, and the 1 bit gets the rest. The division by $2^{11}$ comes first, so the product fits in 32 bits. Lines L4 and L6 move the probability $1/32$ of the way toward the bit that came. This is an exponential moving average, and it keeps $prob$ in $[31, 2017]$, so no bit ever gets a zero width.

Line L5 can make $low$ reach $2^{32}$. SHIFT-LOW handles this. If the top byte of $low$ is less than 0xFF, no later carry can pass it, so line L13 writes the waiting bytes. If $low \ge 2^{32}$, the carry goes into the waiting bytes as they are written: the cached byte gets 1 and each 0xFF becomes 0x00. If the top byte is 0xFF and there is no carry, line L15 only adds the byte to the waiting run. The decoder does not need any of this, because it reads the finished number.

The probability of a 0 is at least $31/2048$, and $range \ge 2^{24}$ before each bit, so after one bit $range > 2^{16}$, and one shift by 8 bits brings it back above $2^{24}$. That is why the decoder at line L21 uses `if` where the encoder at line L7 uses `while`: the loop runs at most once in both. The implementation also has the direct bits of LZMA, with probability $\tfrac12$ and no counter, and a decoder for the literals of a raw LZMA1 stream.

## Example

Code the bits 0, 0, 1, 0, all with one counter that starts at 1024. The table gives the registers after each bit. No shift happens, because $range$ stays at least $2^{24}$.

| bit | $prob$ before | $bound$ | $low$ after | $range$ after | $prob$ after |
|---|---|---|---|---|---|
| 0 | 1024 | 0x7FFFFC00 | 0x00000000 | 0x7FFFFC00 | 1056 |
| 0 | 1056 | 0x41FFFBE0 | 0x00000000 | 0x41FFFBE0 | 1087 |
| 1 | 1087 | 0x2307BBC1 | 0x2307BBC1 | 0x1EF8401F | 1054 |
| 0 | 1054 | 0x0FF042F0 | 0x2307BBC1 | 0x0FF042F0 | 1085 |

FLUSH makes five shifts. The first writes the initial cached byte 00 and caches 0x23. The next ones write 23, 07, BB and C1. The output is the five bytes `00 23 07 BB C1`. The decoder reads $code$ = 0x2307BBC1. It is below the first two bounds, so the first two bits are 0. At the third bit $code$ equals $bound$, which is not below it, so the bit is 1 and $code$ becomes 0, which is below the last bound. At the end $code = 0$, the check that LZMA uses to detect a damaged stream.

The four bits have a model cost of $\lg(2048/1024) + \lg(2048/1056) + \lg(2048/961) + \lg(2048/1054) \approx 4.01$ bits. The final width $\text{0x0FF042F0} / (2^{32} - 1) \approx 2^{-4.01}$ agrees. The other 36 bits are the fixed cost of the zero byte and the flush.

## Correctness

The proof keeps track of the value $V = (W \cdot 256^{cs} + P) \cdot 2^{32} + low$, where $W$ is the integer of the written bytes and $P$ is the integer of the waiting bytes. Lines L2 to L6 change $V$ exactly as an exact interval coder changes the lower end. SHIFT-LOW does not change $V$: it writes bytes only when no carry can reach them, and when $low \ge 2^{32}$ the cached byte is never 0xFF, so the carry stops inside the waiting block. The written bytes, read as one big number, are the lower end of the final interval, so they lie in every interval of the coding. The decoder's $code$ is the distance from the lower end to that number, so $code < bound$ holds exactly when the bit is 0. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/) with 32-bit words, plus one bit for the carry of $low$.

- **Time.** Each decision costs a constant number of word operations and at most one shift. SHIFT-LOW writes each output byte once, and there are at most $n + 5$ of them. So the time is $\Theta(n)$ for $n$ decisions. The order-0 byte coder makes 8 decisions per byte.
- **Space.** $\Theta(k)$ for the counters, and $O(1)$ words for the coder. The byte coder has 255 counters.
- **Code length.** Let $p_j$ be the model probability of the decision that came. For a 1 bit the new width is at least $p_j$ times the old one. For a 0 bit the truncation of $range / 2^{11}$ loses a factor of at most $1 - 2^{11}/2^{24}$. The output has $8$ bits per shift plus 40 bits for the five bytes of FLUSH and the zero byte, so it has at most
$$\sum_{j=1}^{n} \lg \frac{1}{p_j} + n \lg \frac{1}{1 - 2^{-13}} + 40$$
bits. The middle term is less than $1.8 \times 10^{-4}$ bits per decision. On 4000 bytes of a skewed two-letter source, the implementation measured a model cost of 2728.9 bits and an output of 2768 bits.

## Properties

- **Deterministic and online.** The encoder writes a byte as soon as no carry can reach it. A long run of 0xFF bytes can wait in the cache, but the count $cs$ takes $O(1)$ space.
- **Binary and adaptive.** The LZMA coder codes only binary decisions. Each counter is its own adaptive model with a fixed rate of $1/32$, which follows changes in the data fast but does not converge to the true probability.
- **No division.** With a binary model the coder needs only shifts, one multiplication and additions. A multi-symbol range coder needs a division by the total of the counts.

## Variants and improvements

- **Multi-symbol range coders.** Martin's coder and later byte-wise coders cut the range among all symbols with cumulative counts, $range \leftarrow \lfloor range / T \rfloor \cdot f(s)$, in the same way as [arithmetic coding](/arithmetic-coding/).
- **Carryless coders.** The carryless range coder of Dmitry Subbotin never makes a carry. When the top byte of $low$ and of $low + range$ differ and $range$ is small, it shrinks $range$ so that the interval stops below the next byte boundary. This costs a little compression but needs no cache.
- **Larger probability scales.** Other binary coders use 12-bit or 16-bit probabilities, two rates of adaptation mixed together, or probabilities from a [context mixing](/context-mixing/) model.
- **ANS.** [rANS](/rans-coding/) uses the same byte-wise renormalization with a single state, and it decodes with fewer operations, but it decodes in reverse order. See [asymmetric numeral systems](/asymmetric-numeral-systems/).
- **CABAC.** The M coder of [CABAC](/cabac/) is also a binary interval coder, with a 9-bit range and a table in place of the multiplication.

## When to use it

Use a range coder when the model gives a new probability for each binary decision, as in [LZMA](/lzma/) and in context mixing compressors, and when byte output is more convenient than bit output. It is a good default for adaptive models. For a static model with many symbols, [rANS](/rans-coding/) or [tANS](/tabled-asymmetric-numeral-systems/) decode faster.

## Pitfalls

- **Forgetting the carry.** A coder that writes the top byte of $low$ at once gives a wrong output when a later addition carries into that byte. Either keep the cache and the count of 0xFF bytes, or use a carryless coder.
- **Too few flush bytes.** The LZMA encoder needs five calls of SHIFT-LOW: one for the cached byte and four for the bytes of $low$. With fewer, the decoder reads zeros in place of the last bytes of $low$, and the last bits come out wrong.
- **The order of the multiplication.** $range \cdot prob / 2^{11}$ overflows 32 bits. Divide first, as in line L2, and use the same order in the encoder and the decoder.
- **A 32-bit low.** $low$ needs one more bit than $range$ for the carry. In C, use a 64-bit type for $low$.
- **A probability that reaches 0 or 2048.** An update rule that lets $prob$ reach an end gives a zero width to one bit. With $2^{11}$ and a shift of 5, the bounds 31 and 2017 hold. With other constants, check them.

## Implementations

## History

Martin presented range encoding at the Video and Data Recording Conference in Southampton in July 1979. He described the coder as arithmetic on a range of integers that writes one digit at a time. The method stayed in the background while arithmetic coding grew at IBM, and in the 1990s it drew interest as a byte-wise coder that was thought to be free of the IBM patents. Several range coders appeared in compression programs in the late 1990s, among them the carryless coder of Subbotin. Igor Pavlov used the binary form with 11-bit counters and the cached byte in LZMA, the method of 7-Zip and of the xz format. The LZMA specification cites Martin's paper as the source of its range coder.

## References
