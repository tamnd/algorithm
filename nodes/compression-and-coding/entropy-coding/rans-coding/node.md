---
tag: 08A5D1
kind: algorithm
slug: rans-coding
name: Range asymmetric numeral systems
aliases:
- rANS
area: compression-and-coding/entropy-coding
level: research
summary: The range form of ANS. The state x goes to floor(x/f)·M + c + (x mod f) and stays in [L, bL) by moving whole bytes. Decoding needs one multiply, and several states can interleave.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, k: the alphabet size, M: the total of the quantized frequencies}
  time: {worst: Θ(n + k log k + M), average: Θ(n + k log k + M), best: Θ(n + k log k + M)}
  space: {extra: Θ(k + M)}
properties: {deterministic: true, online: false, recursive: false, comparison: false}
history:
  year: 2013
  people: [Jarek Duda, Fabian Giesen]
  note: Duda described the range variant of ANS in 2013; Giesen published the byte-wise coder ryg_rans and the interleaving of several states in 2014.
prereqs: [asymmetric-numeral-systems]
see_also: [tabled-asymmetric-numeral-systems, range-coding, arithmetic-coding, huffman-coding, shannon-entropy, lossless-compression]
sources:
  - url: https://arxiv.org/abs/1311.2540
    title: "Jarek Duda, Asymmetric numeral systems: entropy coding combining speed of Huffman coding with compression rate of arithmetic coding, arXiv 1311.2540, 2013"
    locator: the section on the range variant (rANS) and the section on streaming with the interval [L, bL)
  - url: https://arxiv.org/abs/1402.3392
    title: Fabian Giesen, Interleaved entropy coders, arXiv 1402.3392, 2014
    locator: the whole paper (several coder states that share one stream, and their use with SIMD)
  - url: https://github.com/rygorous/ryg_rans
    title: Fabian Giesen, ryg_rans, public domain rANS coders
    locator: rans_byte.h (RansEncPut, RansEncFlush, RansDecInit, RansDecGet, RansDecAdvance with RANS_BYTE_L = 1 << 23) and the two-way interleaved example in main.cpp
---

Range asymmetric numeral systems (rANS) is the range form of [asymmetric numeral systems](/asymmetric-numeral-systems/), an entropy coder for [lossless compression](/lossless-compression/). The symbols get integer frequencies $f_s$ that sum to a power of two $M$, with prefix sums $c_s$, and coding $s$ maps the state $x$ to
$$C(s, x) = \left\lfloor \frac{x}{f_s} \right\rfloor M + c_s + (x \bmod f_s).$$
The state grows by about $\lg(M/f_s)$ bits, and the decoder undoes the step with one multiplication, a mask and a table lookup. A streaming coder keeps $x$ in an interval $[L, bL)$ and moves whole digits of base $b$ to and from the stream. This page gives the byte-wise coder of Giesen's ryg_rans, with $M = 2^{12}$, $L = 2^{23}$, $b = 256$, a static frequency table and two interleaved states.

## In plain words

The state is a number that grows as symbols go in. All numbers are cut into blocks of the same size, and each block gives every symbol a run whose length matches how often the symbol occurs. To add a symbol, the coder picks a block and a place in that symbol's run that together encode the old number. A common symbol has a long run, so the number grows slowly.

To read a symbol back, look at where the number falls inside its block. That tells the symbol, and the block and the place give the old number.

Before the number gets too large, the encoder sends its lowest byte out. The decoder takes the byte back when the number gets too small. Two such numbers can take turns on one stream, so the processor can work on both at once.

## The problem

The input is a byte string $d_0 \ldots d_{n-1}$ over an alphabet of $k \le 256$ symbols. The model is static and memoryless: the encoder counts the symbols, scales the counts to frequencies $f_s \ge 1$ with $\sum_s f_s = M$, and codes every symbol with the probability $f_s / M$. The output is a byte string from which the decoder, given $n$ and the same frequency table, gets the input back. Sending the table is a separate problem and is not counted below. The length is compared to $n H_0$, where $H_0$ is the order-0 empirical [entropy](/shannon-entropy/) of the input.

## The algorithm

```pseudo id=main
ENCODE-PUT(x, s)                        ▷ x in [L, 256 L)
L1  x_max ← (L / M) · 256 · f[s]
L2  while x ≥ x_max do write the byte x mod 256 to the front of the output, x ← ⌊x / 256⌋
L3  return ⌊x / f[s]⌋ · M + c[s] + (x mod f[s])

DECODE-GET(x)
L4  slot ← x mod M
L5  s ← sym[slot]                       ▷ the symbol with c[s] ≤ slot < c[s] + f[s]
L6  x ← f[s] · ⌊x / M⌋ + slot − c[s]
L7  while x < L do x ← 256 · x + the next byte of the input
L8  return (s, x)

ENCODE(d[0..n−1])
L9  x[0] ← L, x[1] ← L
L10 for i ← n − 1 down to 0 do x[i mod 2] ← ENCODE-PUT(x[i mod 2], d[i])
L11 write x[1], then x[0], as 4 bytes each to the front of the output

DECODE(input, n)
L12 x[0] ← the first 4 bytes, x[1] ← the next 4 bytes
L13 for i ← 0 to n − 1 do (d[i], x[i mod 2]) ← DECODE-GET(x[i mod 2])
L14 check that x[0] = x[1] = L and that the input is used up

NORMALIZE(count[0..k−1])
L15 f[s] ← max(1, round(M · count[s] / n)) for each s with count[s] > 0
L16 add the shortfall to the most frequent symbol, or take the excess 1 at a time from the largest f[s] > 1
L17 c[s] ← f[0] + … + f[s − 1]
```

Line L3 is the coding function. The quotient $\lfloor x / f_s \rfloor$ picks a block of $M$ states, and $c_s + (x \bmod f_s)$ picks a place in the run of $s$ inside the block. Lines L4 to L6 invert it: the place tells the symbol, and the block number and the offset in the run give back $x$.

Lines L1 and L2 keep the state in a word. Between symbols, $x \in [L, 256L)$. Before line L3, the loop of line L2 brings $x$ into $[2^{11} f_s, 2^{19} f_s)$, the set that line L3 maps into $[L, 256L)$. That set has the form $[a, 256a)$, so exactly one number of byte shifts reaches it from any $x \in [L, 256L)$, and the decoder's loop at line L7 reads exactly the bytes that line L2 wrote. With $L = 2^{23}$ the state fits in 32 bits, and $L/M = 2^{11}$ makes $L$ a multiple of $M$, which is what makes the set of the right form.

The encoder runs from the last symbol to the first and writes to the front, because ANS decodes in the reverse order of encoding. The decoder then reads forward. Symbol $i$ uses state $i \bmod 2$. The decoder reads the two flushed states in the order that the encoder wrote them last, and after that the operations of the two sides mirror each other exactly.

**Interleaving and SIMD.** The two states of lines L9 to L13 have no data dependence between them, so a processor can run the two chains of multiplications and divisions in parallel, although they share one byte stream. Giesen (2014) showed that this works for any number of states, as long as the decoder performs its reads in the reverse order of the encoder's writes. With 4, 8 or 32 states, the steps of the states line up in the lanes of SIMD registers or GPU threads, and the renormalization becomes a masked load.

## Example

Code $d$ = "abac". The counts 2, 1, 1 scale to $f_a = 2048$, $f_b = 1024$, $f_c = 1024$, with $c_a = 0$, $c_b = 2048$, $c_c = 3072$. Both states start at $L$ = 0x800000. The encoder works from the end. No byte leaves during the steps, because each $x$ stays below $x_{\max} = 2^{19} f_s$.

| step | $i$ | symbol | state | $x$ before | $x$ after |
|---|---|---|---|---|---|
| 1 | 3 | c | 1 | 0x00800000 | 0x02000C00 |
| 2 | 2 | a | 0 | 0x00800000 | 0x01000000 |
| 3 | 1 | b | 1 | 0x02000C00 | 0x08003800 |
| 4 | 0 | a | 0 | 0x01000000 | 0x02000000 |

The flush writes state 1 and then state 0 to the front, each with its low byte first in the stream. The output is the 8 bytes `00 00 00 02 00 38 00 08`. The decoder reads $x_0$ = 0x02000000 and $x_1$ = 0x08003800. For $i = 0$, the slot of $x_0$ is 0, which is in the run of a, and line L6 gives $2048 \cdot \text{0x2000} = \text{0x1000000}$. For $i = 1$, the slot of $x_1$ is 0x800 = 2048, so the symbol is b, and $x_1$ becomes $1024 \cdot \text{0x8003} + 2048 - 2048 = \text{0x2000C00}$. Two more steps give a and c and bring both states back to $L$.

The states grew by $\lg(\text{0x2000000}/L) = 2$ bits and $\lg(\text{0x8003800}/L) \approx 4.0$ bits, which are the 6 bits of $2 \lg 2 + 2 \lg 4$. The other 58 bits are the fixed cost of the two flushed states.

## Correctness

Between symbols each state lies in $[L, 256L)$. Before line L3 the loop brings $x$ into $[2^{11} f_s, 2^{19} f_s)$, so the quotient $\lfloor x/f_s \rfloor$ lies in $[2^{11}, 2^{19})$ and the new state lies in $[L, 256L)$ again. The slot $c_s + (x \bmod f_s)$ is less than $M$, so line L4 recovers it, line L5 recovers $s$, and line L6 recovers $x$. The decoder then reads a byte while $x < L$. Each value that the encoder had after a byte shift is less than $L$, and the value before the first shift is at least $L$, so the decoder reads exactly the shifted bytes, in reverse. The encoder's operations and the decoder's operations come in mirror order, so each one reads the bytes that its mirror wrote. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/) with 32-bit words and a 64-bit product.

- **Time.** Building the table costs $\Theta(n)$ for the counts, $O(k \log k)$ for the normalization with a heap, and $\Theta(M)$ for the slot table of line L5. Each symbol costs one division and one modulo to encode, one multiplication to decode, and at most 2 byte moves. So the total is $\Theta(n + k \log k + M)$.
- **Space.** $\Theta(k)$ for the frequencies and $\Theta(M)$ for the slot table.
- **Code length.** A byte shift lowers $\lg x$ by at least 8, and line L3 raises it by at most $\lg(M/f_s) + \lg(1 + 2^{-11})$, because $x \ge 2^{11} f_s$ there. Each state starts at $L$ and ends at least at $L$, so the output has at most
$$\sum_{i=0}^{n-1} \lg \frac{M}{f_{d_i}} + n \lg(1 + 2^{-11}) + 64$$
bits. The middle term is less than $7.1 \times 10^{-4}$ bits per symbol. The first term is $n$ times the cross entropy of the empirical distribution and the quantized one, that is $n H_0$ plus $n$ times their relative entropy. On 20000 symbols drawn with weights 8, 4, 2, 1, 1, the implementation measured an output of 37520 bits against $n H_0 \approx 37463$ bits.

## Properties

- **Static model, reverse order.** The encoder needs the whole block before it can start, and it runs backward. An adaptive model is possible only if its probabilities are computed in a forward pass first.
- **Exact integer arithmetic.** There is no rounding in the coding function, so the encoder and the decoder agree on every platform.
- **Division in the encoder only.** The decoder multiplies. The encoder divides by $f_s$, which a table of reciprocals can replace with a multiplication.
- **Many states.** Any number of states can share a stream, which suits SIMD and GPU decoders.

## Variants and improvements

- **Larger states.** rans64.h of ryg_rans keeps a 64-bit state with $L = 2^{31}$ and moves 32 bits at a time, so it renormalizes less often.
- **Reciprocal encoding.** The encoder can precompute, for each symbol, a fixed-point reciprocal of $f_s$ and a shift, and replace the division of line L3 with a multiplication.
- **Alias tables.** For a large $M$, the slot table of line L5 becomes large. An alias table of size $k$ maps a slot to a symbol in $O(1)$ time with $O(k)$ space, at the cost of a different layout of the runs.
- **Adaptive rANS.** Coders such as the order-1 rANS of the CRAM 3 format use a static table per context. A fully adaptive coder buffers the probabilities of a block and codes the block backward.
- **Binary rANS (rABS).** With two symbols, the slot lookup is one comparison, and the coder can take a new probability for each bit.
- **tANS.** For small $M$, the whole map can be precomputed in tables, which removes the multiplication. See [tabled ANS](/tabled-asymmetric-numeral-systems/).

## When to use it

Use rANS for a static or block-wise model where decoding speed matters and the alphabet is large, for example the literals and the lengths of an LZ compressor or the coefficients of an image codec. JPEG XL and the CRAM format for DNA sequence data use rANS. Prefer [tANS](/tabled-asymmetric-numeral-systems/) when a small table fits in the cache and no multiplication is wanted, and prefer [range coding](/range-coding/) or [arithmetic coding](/arithmetic-coding/) when the model adapts after each symbol.

## Pitfalls

- **A frequency of 0.** Normalization can round a rare symbol to 0. Keep $f_s \ge 1$ for every symbol that occurs, as in line L15, or the encoder divides by 0.
- **$L$ not a multiple of $M$.** If $M$ does not divide $L$, the set of states that line L3 maps into $[L, 256L)$ is not of the form $[a, 256a)$, and the decoder can read a wrong number of bytes.
- **Overflow.** $\lfloor x/f_s \rfloor \cdot M$ must fit in the state type: with $L = 2^{23}$ and $b = 256$, the states stay below $2^{31}$.
- **Mismatched interleaving.** The decoder must initialize the states in the reverse order of the encoder's flushes, and use state $i \bmod 2$ for symbol $i$ on both sides.
- **Forgetting the table.** The decoder needs the same frequencies. Sending them costs bits that the bound above does not count, which matters for short blocks.

## Implementations

## History

Duda described the range variant in his 2013 arXiv paper on asymmetric numeral systems, next to the tabled variant. Fabian Giesen wrote the public domain library ryg_rans in early 2014, with a byte-wise 32-bit coder and a 64-bit coder, and in his paper "Interleaved entropy coders" on arXiv in 2014 he showed how several states can share one stream and how to use them with SIMD. James Bonfield used rANS with order-0 and order-1 models in the CRAM 3 format for DNA sequence data, and JPEG XL uses it as its main entropy coder.

## References
