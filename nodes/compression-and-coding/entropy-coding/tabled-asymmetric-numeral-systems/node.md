---
tag: 8ATQ56
kind: algorithm
slug: tabled-asymmetric-numeral-systems
name: Tabled asymmetric numeral systems
aliases:
- tANS
- finite-state entropy
- FSE
area: compression-and-coding/entropy-coding
level: advanced
summary: ANS with a table of L states. Each state gives a symbol, a bit count and a baseline, so decoding a symbol is one lookup plus a read of a few bits. The coder of Zstandard (FSE).
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, k: the alphabet size, L: the number of states in the table}
  time: {worst: Θ(n + k + L), average: Θ(n + k + L), best: Θ(n + k + L)}
  space: {extra: Θ(k + L)}
properties: {deterministic: true, online: false, recursive: false, comparison: false}
history:
  year: 2013
  people: [Jarek Duda, Yann Collet]
  note: Duda described the tabled variant of ANS in 2013, and Collet's Finite State Entropy library from the same year became the entropy coder of Zstandard.
prereqs: [asymmetric-numeral-systems]
see_also: [rans-coding, zstandard, huffman-coding, canonical-huffman-code, range-coding, lossless-compression]
sources:
  - url: https://arxiv.org/abs/1311.2540
    title: "Jarek Duda, Asymmetric numeral systems: entropy coding combining speed of Huffman coding with compression rate of arithmetic coding, arXiv 1311.2540, 2013"
    locator: the sections on the tabled variant (tANS), the stream in the interval [L, 2L), the symbol spread and the loss from it
  - url: https://www.rfc-editor.org/rfc/rfc8878
    title: Yann Collet and Murray Kucherawy (editors), Zstandard compression and the 'application/zstd' media type, RFC 8878, 2021
    locator: Section 4.1 (FSE), Section 4.1.1 (FSE Table Description, the spread rule and Table 21), Section 3.1.1.3.2.2 (Default Distributions) and Appendix A.1 (the decoding table of the literals length codes)
  - url: https://github.com/Cyan4973/FiniteStateEntropy
    title: Yann Collet, Finite State Entropy, the reference FSE library
    locator: fse_compress.c and fse_decompress.c (FSE_buildCTable, FSE_buildDTable, FSE_initCState2)
---

Tabled asymmetric numeral systems (tANS) is the form of [asymmetric numeral systems](/asymmetric-numeral-systems/) in which the coder has a fixed set of $L = 2^R$ states and all its arithmetic is precomputed in tables. Each state of the decoding table names a symbol, a number of bits $nb$ and a baseline: the decoder outputs the symbol and goes to the state $baseline$ plus the next $nb$ bits of the stream. So decoding a symbol costs about what a table-driven [Huffman](/huffman-coding/) decoder pays, but the coder spends a fractional number of bits per symbol, close to $\lg(L/f_s)$ for a symbol with $f_s$ of the $L$ states. Yann Collet's implementation is called Finite State Entropy (FSE), and it is the entropy coder of [Zstandard](/zstandard/) for the lengths and offsets of the LZ matches. This page follows the table construction of RFC 8878.

## In plain words

The coder has a fixed number of states, say 64, and it shares them out among the symbols in proportion to how often each symbol occurs. The states of each symbol are scattered over the whole table.

To read a symbol, the decoder looks at its current state. The table says which symbol that is, how many bits to read next, and what number to add to them. The result is the next state. A symbol that owns many states needs few bits to reach the next state, and a rare symbol needs many.

The encoder does the same steps backward, from the last symbol to the first, and writes the bits that the decoder will read. Everything is decided by the table, so the work per symbol is a lookup and a few bit operations.

## The problem

The input is a message $d_0 \ldots d_{n-1}$ over an alphabet of $k$ symbols. The model is static and memoryless: a normalized distribution gives each symbol $s$ a count $f_s \ge 1$ of states, with $\sum_s f_s = L = 2^R$. In Zstandard a count may also be $-1$, which means a probability below $1/L$: the symbol gets one state and a full reset. The output is a bit string from which the decoder, given $n$ and the same distribution, gets the message back. The length is compared to $\sum_i \lg(L/f_{d_i})$, the ideal length under the coded distribution; for counts scaled from the input, this is close to $n H_0$, the order-0 empirical [entropy](/shannon-entropy/).

## The algorithm

Lines L1 to L11 build the tables as in RFC 8878 Section 4.1.1. Write $f_s = \max(norm[s], 1)$.

```pseudo id=main
BUILD(norm[0..k−1], R)                      ▷ L = 2^R states, R ≥ 4
L1  high ← L − 1
L2  for each s with norm[s] = −1 do sym[high] ← s, high ← high − 1
L3  step ← (L >> 1) + (L >> 3) + 3, pos ← 0
L4  for each s with norm[s] > 0, repeated norm[s] times do
L5      sym[pos] ← s
L6      repeat pos ← (pos + step) mod L until pos ≤ high
L7  next[s] ← f_s for each s
L8  for u ← 0 to L − 1 do
L9      s ← sym[u], t ← next[s], next[s] ← t + 1
L10     nb[u] ← R − ⌊lg t⌋, base[u] ← t · 2^nb[u] − L
L11     append u to states[s]                  ▷ the encoding table

ENCODE(d[0..n−1])
L12 u ← states[d[n−1]][0]
L13 for i ← n − 2 down to 0 do
L14     s ← d[i], f ← f_s, x ← L + u
L15     k ← the number with f ≤ ⌊x / 2^k⌋ < 2f
L16     write the low k bits of x; u ← states[s][⌊x / 2^k⌋ − f]
L17 write u in R bits, then a 1 bit, and pad with 0 bits to a byte

DECODE(stream, n)
L18 skip the padding and the last 1 bit; read u in R bits, going backward
L19 for i ← 0 to n − 1 do
L20     d[i] ← sym[u]
L21     if i < n − 1 then u ← base[u] + (the next nb[u] bits, going backward)
L22 check that the stream is used up
```

**The spread.** Lines L3 to L6 deal the cells to the symbols with a fixed odd step, so the cells of each symbol are scattered over the table at near-even distances. For $L \ge 16$ the step is odd, so it visits every cell once before it returns to 0, and line L6 skips the cells that line L2 gave to the symbols of probability below $1/L$.

**The decoding table.** The $f_s$ cells of $s$, in increasing order, get the numbers $t = f_s, f_s + 1, \ldots, 2f_s - 1$. Line L10 gives the cell with number $t$ the range of next states $[base, base + 2^{nb})$, which in terms of $x = L + u$ is $[t \cdot 2^{nb}, (t+1) \cdot 2^{nb})$. These ranges, over the cells of $s$, cover $[L, 2L)$ exactly once. The lower cells get one bit more than the higher ones when $f_s$ is not a power of two.

**Encoding.** The encoder holds a value $x = L + u \in [L, 2L)$. To code $s$, it drops the $k$ low bits of $x$ that bring it into $[f_s, 2f_s)$, writes them, and moves to the cell with number $\lfloor x/2^k \rfloor$. This is the ANS step $x \mapsto C(s, x)$ with the renormalization done first, and the table holds $C$ for every case. Zstandard computes $k$ with one addition and a shift from a precomputed value per symbol. The encoder starts with a cell of the last symbol (line L12), which costs no bits, and the decoder skips the update after the last symbol (line L21), as in the sequence section of RFC 8878.

**The stream.** The bits are written forward and read backward, and the final 1 bit marks where the reader starts. This order follows from ANS: the decoder needs the last state of the encoder first.

## Example

Take $R = 4$, $L = 16$, and the counts $a = 8$, $b = 5$, $c = 3$. The step is $8 + 2 + 3 = 13$. Starting at 0, the positions $0, 13, 10, 7, 4, 1, 14, 11$ go to $a$, then $8, 5, 2, 15, 12$ to $b$, then $9, 6, 3$ to $c$, and the next position is 0 again. The decoding table is:

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| symbol | a | a | b | c | a | b | c | a | b | c | a | a | b | a | a | b |
| $nb$ | 1 | 1 | 2 | 3 | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| $base$ | 0 | 2 | 4 | 8 | 4 | 8 | 0 | 6 | 12 | 4 | 8 | 10 | 0 | 12 | 14 | 2 |

The cells of $c$ are 3, 6, 9 with the numbers 3, 4, 5. Cell 3 reads 3 bits into $[8, 16)$, and cells 6 and 9 read 2 bits into $[0, 4)$ and $[4, 8)$. Together they cover all 16 states.

Code the message a b a c a a. The encoder starts at cell 0, a cell of the last $a$, and works backward:

| $i$ | symbol | $x$ | $k$ | bits written | $\lfloor x/2^k \rfloor$ | new cell |
|---|---|---|---|---|---|---|
| 4 | a | 16 | 1 | 0 | 8 | 0 |
| 3 | c | 16 | 2 | 00 | 4 | 6 |
| 2 | a | 22 | 1 | 0 | 11 | 7 |
| 1 | b | 23 | 2 | 11 | 5 | 2 |
| 0 | a | 18 | 1 | 0 | 9 | 1 |

Then it writes the cell 1 in 4 bits and the end mark. The stream has $7 + 4 + 1 = 12$ bits, the bytes `B0 08`. The decoder reads the cell 1 and outputs $a$. It reads 1 bit (0) and adds the base 2, so it goes to cell 2 and outputs $b$. It reads 2 bits (11) and adds 4 to reach cell 7, and so on through the cells 6, 0 and 0. The ideal length is $4 \lg 2 + \lg(16/5) + \lg(16/3) \approx 8.09$ bits, and the steps wrote 7 bits. The other bits are the final state and the end mark, which the encoder pays once per stream.

## Correctness

The step of the spread is odd for $L \ge 16$, so it is prime to $L$, and the walk visits each cell once per cycle: every cell gets exactly one symbol, and the walk ends at 0. For a symbol $s$, every $x \in [L, 2L)$ has exactly one shift $k$ that brings it into $[f_s, 2f_s)$, so the ranges of next states of the cells of $s$ partition the table, and the cell that the encoder picks for $x$ is the one whose range holds $x - L$, at the offset given by the $k$ dropped bits. So each decoding step undoes one encoding step. The reader takes the groups of bits in the reverse order of writing, which is the order the decoder needs. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/).

- **Time.** Building the tables costs $O(L + k)$. Each symbol costs a constant number of operations to encode and to decode. So the total is $\Theta(n + k + L)$.
- **Space.** The decoding table has $L$ cells, and the encoding table $L$ entries plus $O(k)$ for the symbol data.
- **Code length.** The proof shows that the step that moves to the cell $u$ with number $t$ writes at most $\lg((L + u)/t)$ bits, up to a total of 1 bit for the whole message. If the cells of $s$ were placed exactly at $u = jL/f_s$, this would be the ideal $\lg(L/f_s)$. The spread places them close to these points, and the loss shrinks as $L$ grows; Duda (2013) gives an analysis. The stream adds $R + 1$ bits and the padding. On 20000 symbols drawn with weights 8, 4, 2, 1, 1 and $L = 2^{11}$, the implementation wrote 37824 bits (with the padding) against an ideal of about 37812 bits under the table.

## Properties

- **Fast decoding.** One table lookup, one read of $nb$ bits and one addition per symbol, with no multiplication.
- **Static model.** The table is fixed for a block. Zstandard sends a compact description of the counts, or uses a predefined distribution.
- **Reverse order.** As in all ANS coders, the encoder runs from the last symbol to the first.
- **Fractional bits.** A symbol with $f_s$ cells costs about $\lg(L/f_s)$ bits on average, not a whole number of bits as with a prefix code.

## Variants and improvements

- **Other spreads.** Duda (2013) gives a precise spread that sorts the cells by the ideal positions of the symbols and gets closer to the ideal length, and a spread from a random generator that also scrambles the data. FSE uses the fast step rule of line L3.
- **Interleaved states.** Like rANS, several tANS states can share one stream, which lets a processor decode several symbols at a time. Zstandard's Huffman decoder uses four streams for a similar reason.
- **tANS for prefix codes.** A Huffman code is the special case in which every $f_s$ is a power of two and the cells of each symbol are consecutive, and then each symbol costs a whole number of bits.
- **Range ANS.** For a large $L$ the tables no longer fit in the cache. [rANS](/rans-coding/) then computes the same kind of map with a multiplication.

## When to use it

Use tANS for a static or block-wise distribution over a small alphabet, when the table, with $L$ from about $2^5$ to $2^{12}$, fits in the first-level cache and decoding speed matters. Zstandard uses it for the literal lengths, match lengths and offset codes, and Apple's LZFSE uses it too. For a large alphabet with a large $L$, [rANS](/rans-coding/) needs less memory. For adaptive models, use [range coding](/range-coding/) or [arithmetic coding](/arithmetic-coding/).

## Pitfalls

- **A small table.** For $L = 8$, the step $4 + 1 + 3 = 8$ is not odd, and the spread puts every symbol on cell 0. RFC 8878 uses accuracy logs of at least 5.
- **Counts that do not fill the table.** The counts and the $-1$ cells must sum to $L$, or the spread does not end at 0. FSE checks this when it builds the table.
- **The order of the states.** The numbers $t = f_s, \ldots, 2f_s - 1$ go to the cells of $s$ in increasing order of the cell. Another order gives a valid coder, but not the Zstandard one.
- **The bit order.** The stream is read backward, but each group of bits is a little-endian number as written. Reversing the bits of each group breaks compatibility.

## Implementations

## History

Duda described the tabled variant in his 2013 arXiv paper, with the interval $[L, 2L)$ of states and several ways to spread the symbols. Late in 2013 Yann Collet released Finite State Entropy, a fast tANS coder with the spread rule of line L3, and it became the entropy coder of Zstandard, which Facebook released as version 1.0 in 2016. The format is specified in RFC 8478 (2018) and in RFC 8878 (2021), which replaced it. Apple's LZFSE, released in 2015, also uses tANS.

## References
