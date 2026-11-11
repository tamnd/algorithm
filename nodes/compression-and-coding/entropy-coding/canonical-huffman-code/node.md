---
tag: ZVDKR0
kind: concept
slug: canonical-huffman-code
name: Canonical Huffman code
aliases:
- canonical prefix code
- canonical Huffman codes
area: compression-and-coding/entropy-coding
level: core
summary: A prefix code whose codewords follow from the code lengths alone, in order of length and then of symbol. The decoder needs only the lengths, and decodes with small tables.
prereqs: [huffman-coding, prefix-code]
see_also: [kraft-inequality, length-limited-prefix-code, package-merge, deflate, jpeg-compression, brotli, optimal-prefix-code]
sources:
  - paper: doi:10.1145/363958.363991
    title: Eugene S. Schwartz and Bruce Kallick, Generating a canonical prefix encoding, Communications of the ACM 7(3), 1964
    locator: pages 166 to 169 (codewords assigned from the lengths, in numerical order)
  - paper: doi:10.1109/26.634683
    title: Alistair Moffat and Andrew Turpin, On the implementation of minimum redundancy prefix codes, IEEE Transactions on Communications 45(10), 1997
    locator: pages 1200 to 1207 (decoding with first-code and symbol-offset tables, and the partial lookup table)
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: P. Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, 1996
    locator: Section 3.2.2 (the two rules, the algorithm in three steps, and the example ABCDEFGH) and Section 3.2.6 (the fixed literal/length code)
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Sections 2.5 (assigning codewords), 3.1 (encoding canonical codes) and 3.2 (decoding canonical codes)
  - url: https://www.rfc-editor.org/rfc/rfc7932
    title: J. Alakuijala and Z. Szabadka, RFC 7932, Brotli Compressed Data Format, 2016
    locator: Section 3.2, Use of prefix coding in the Brotli format (canonical prefix codes)
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81, Digital compression and coding of continuous-tone still images, 1992
    locator: Annex C (the lists BITS and HUFFVAL, and the code generation of Figures C.1 to C.3)
---

A canonical Huffman code is a [prefix code](/prefix-code/) whose codewords are fixed by the codeword lengths alone: the codewords are consecutive binary numbers, taken in order of length and then of symbol. Each list of lengths that satisfies the [Kraft inequality](/kraft-inequality/) has exactly one canonical code, and it has the same cost as any other code with those lengths. So an encoder that has built a [Huffman code](/huffman-coding/) sends only the lengths, and the decoder rebuilds the codewords and decodes with a few small tables instead of a tree. Schwartz and Kallick described it in 1964; DEFLATE, JPEG and Brotli use it.

## In plain words

A Huffman tree tells you how long each codeword is. It does not matter which codeword of that length a symbol gets, as long as no codeword is the start of another. So pick them by a fixed rule: give the shortest codewords first, and among codewords of the same length, give them to the symbols in alphabet order, counting up in binary.

Then the encoder does not need to send the tree. It sends only one small number for each symbol, the length, and the decoder applies the same rule to get the same codewords. The rule also makes decoding fast: the codewords of one length form one block of numbers, so the decoder can find a symbol with a subtraction and a table lookup.

## The idea

**The rule.** Let symbols $1, \ldots, n$ have lengths $l_1, \ldots, l_n \ge 1$ with $\sum_i 2^{-l_i} \le 1$. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. Sort the symbols by the key $(l_i, i)$, and let $s_1, s_2, \ldots, s_n$ be the sorted order. Define
$$ K_j = \sum_{k < j} 2^{-l_{s_k}}, \qquad 0 \le K_j < 1 .$$
The codeword of $s_j$ is the first $l_{s_j}$ bits after the binary point of $K_j$. In integer form, which is the form of RFC 1951: let $c(l)$ be the number of symbols of length $l$, and
$$ \mathrm{first}(1) = 0, \qquad \mathrm{first}(l) = 2\,\big(\mathrm{first}(l - 1) + c(l - 1)\big) \text{ for } l \ge 2 .$$
The symbols of length $l$, in the order of their numbers, get the $l$-bit integers $\mathrm{first}(l), \mathrm{first}(l) + 1, \ldots, \mathrm{first}(l) + c(l) - 1$. A length of 0 means that the symbol does not occur and gets no codeword.

**Why it is a prefix code.** All lengths before position $j$ in the sorted order are at most $l_{s_j}$, so each term of $K_j$ is a multiple of $2^{-l_{s_j}}$, and so is $K_j$. So the first $l_{s_j}$ bits of $K_j$ are its exact value: the codeword stands for the interval $I_j = [K_j, K_j + 2^{-l_{s_j}})$. The intervals $I_1, I_2, \ldots$ follow one another without overlap, and the last one ends at $\sum_i 2^{-l_i} \le 1$, so each $K_j$ fits in $l_{s_j}$ bits. A codeword $u$ is a prefix of a codeword $v$ exactly when the interval of $v$ lies inside the interval of $u$. Disjoint intervals rule this out, so no codeword is a prefix of another. The same argument shows that the integer form never runs out of $l$-bit values: $\mathrm{first}(l) + c(l) \le 2^l$ for each $l$ if and only if the Kraft inequality holds.

**Why the decoder needs only the lengths.** The rule maps each length list to one code, and both sides apply the same rule. The cost $\sum_i w_i l_i$ depends only on the lengths, so the canonical code of the Huffman lengths is still an optimal code. A length fits in 4 bits when the lengths are at most 15, against up to 15 bits for a codeword, and the list of lengths can itself be compressed, as DEFLATE does with a second Huffman code for the lengths.

**Order.** Sorted by $(l_i, i)$, the codewords increase as binary fractions. Within one length they increase with the symbol number. A shorter codeword is numerically smaller than every longer codeword read with the same number of bits, which is the first rule of RFC 1951: shorter codes come first in the lexicographic order.

**Decoding tables.** For each length $l$ the decoder keeps $c(l)$, $\mathrm{first}(l)$ and $\mathrm{offset}(l)$, the index of the first symbol of length $l$ in the sorted symbol list. These tables have one entry for each length up to the maximum $L$, plus one entry for each symbol, and no tree is needed. Moffat and Turpin (1997) give two ways to use them.

```pseudo id=decode
CANONICAL-DECODE-ONE(bits)                 ▷ c, first, offset, symbols built from the lengths
D1  code ← 0
D2  for l ← 1 to L do
D3      code ← 2 · code + NEXT-BIT(bits)
D4      k ← code − first(l)
D5      if k < c(l) then return symbols[offset(l) + k]
D6  error "not a codeword"
```

Line D5 is correct for this reason. The $l$-bit values below $\mathrm{first}(l) = 2(\mathrm{first}(l-1) + c(l-1))$ are exactly the values that start with a shorter codeword. If the loop reaches length $l$, no shorter prefix was a codeword, so $\mathrm{code} \ge \mathrm{first}(l)$ and $k \ge 0$. Then $k < c(l)$ holds exactly when the $l$ bits are a codeword of length $l$. The *left-justified* variant reads the next $L$ bits as one integer $B$, finds the smallest $l$ with $B < \mathrm{limit}(l) = (\mathrm{first}(l) + c(l)) \cdot 2^{L - l}$ by a short search, and then consumes only $l$ bits. A lookup table indexed by the first $t$ bits of $B$ gives the length directly for most codewords and narrows the search for the rest.

## Examples

**The example of RFC 1951.** The alphabet is A to H with lengths (3, 3, 3, 3, 3, 2, 4, 4). Then $c(2) = 1$, $c(3) = 5$, $c(4) = 2$, and $\mathrm{first}(2) = 0$, $\mathrm{first}(3) = 2(0 + 1) = 2$, $\mathrm{first}(4) = 2(2 + 5) = 14$.

| symbol | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| length | 3 | 3 | 3 | 3 | 3 | 2 | 4 | 4 |
| codeword | 010 | 011 | 100 | 101 | 110 | 00 | 1110 | 1111 |

These are the codes printed in Section 3.2.2 of RFC 1951. The sorted symbol list is F, A, B, C, D, E, G, H, with $\mathrm{offset}(2) = 0$, $\mathrm{offset}(3) = 1$ and $\mathrm{offset}(4) = 6$.

**A decode.** Decode 1110 00 011 with CANONICAL-DECODE-ONE.

| bits read | $l$ | code | $k = \mathrm{code} - \mathrm{first}(l)$ | $c(l)$ | result |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 0 | go on |
| 11 | 2 | 3 | 3 | 1 | go on |
| 111 | 3 | 7 | 5 | 5 | go on |
| 1110 | 4 | 14 | 0 | 2 | symbols[6] = G |
| 0 | 1 | 0 | 0 | 0 | go on |
| 00 | 2 | 0 | 0 | 1 | symbols[0] = F |
| 0 | 1 | 0 | 0 | 0 | go on |
| 01 | 2 | 1 | 1 | 1 | go on |
| 011 | 3 | 3 | 1 | 5 | symbols[2] = B |

The output is G, F, B. In the left-justified form with $L = 4$, the limits are $\mathrm{limit}(2) = 4$, $\mathrm{limit}(3) = 14$ and $\mathrm{limit}(4) = 16$. The first window 1110 is 14, which is not below 4 or 14, so $l = 4$.

**The second example of RFC 1951.** Lengths (2, 1, 3, 3) for A, B, C, D give B = 0, A = 10, C = 110 and D = 111.

**The fixed code of DEFLATE.** RFC 1951, Section 3.2.6, defines the fixed literal/length code by its lengths only: 8 bits for symbols 0 to 143, 9 for 144 to 255, 7 for 256 to 279 and 8 for 280 to 287. The canonical rule gives the codes in the RFC: 0000000 to 0010111 for 256 to 279, 00110000 to 10111111 for 0 to 143, 11000000 to 11000111 for 280 to 287, and 110010000 to 111111111 for 144 to 255.

**A non-example.** The code A 0, B 10, C 11 with lengths (1, 2, 2) is canonical. The code A 1, B 00, C 01 has the same lengths and the same cost, but it is not canonical: the shortest codeword is not the smallest number.

## Where it is used

- **DEFLATE.** RFC 1951 sends each dynamic Huffman code of a [DEFLATE](/deflate/) block as a list of lengths, at most 15 for the literal/length and distance codes, and itself compresses the list with a code over the alphabet 0 to 18. The encoder must produce lengths of at most 15 bits, so it needs a [length-limited code](/length-limited-prefix-code/).
- **JPEG.** ITU-T T.81 describes each Huffman table by BITS, the number of codes of each length from 1 to 16, and HUFFVAL, the symbols in order of increasing length. Annex C builds the codes by the same counting rule. Inside one length, the order is the order of HUFFVAL, not the symbol value, so the rule is canonical up to that order. See [JPEG](/jpeg-compression/).
- **Brotli.** [Brotli](/brotli/) uses the canonical codes of DEFLATE for its prefix codes.
- **Fast decoders.** Decoders for these formats build lookup tables from the lengths, often a first-level table indexed by the next 8 to 10 bits and small second-level tables for longer codewords. Encoders store one length and one codeword per symbol.

## References
