---
tag: 1ZZ3YB
kind: algorithm
slug: fibonacci-coding
name: Fibonacci coding
aliases:
- Zeckendorf code
- Fibonacci code
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes x >= 1 by its Zeckendorf digits, lowest first, plus a final 1, so each codeword ends in 11 and 11 occurs nowhere else. Universal, about 1.44 log2 x bits, and self-synchronizing.
model: word-ram
complexity:
  vars: {x: the integer to code}
  time: {worst: Θ(log x), average: Θ(log x), best: Θ(1)}
  space: {extra: Θ(log x)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1987
  people: [Alberto Apostolico, Aviezri S. Fraenkel]
  note: Apostolico and Fraenkel studied codes built on Fibonacci numeration systems, including the code that ends each codeword with 11.
prereqs: [zeckendorf-theorem, prefix-code]
see_also: [fibonacci-numbers, elias-gamma-coding, elias-delta-coding, universal-code, kraft-inequality, positional-number-system, variable-byte-encoding, unary-coding]
sources:
  - paper: doi:10.1109/TIT.1987.1057284
    title: Alberto Apostolico and Aviezri S. Fraenkel, Robust transmission of unbounded strings using Fibonacci representations, IEEE Transactions on Information Theory 33(2), 1987
    locator: pp. 238 to 245 (the Fibonacci codes and their robustness to bit errors)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.8, Fibonacci, and Table 4a (arXiv:1908.10598v2)
---

The Fibonacci code writes an integer $x \ge 1$ as a sum of non-consecutive Fibonacci numbers, lists the digits of that sum from the smallest Fibonacci number up, and adds one more 1 bit. By [Zeckendorf's theorem](/zeckendorf-theorem/) the sum exists and is unique, and it never uses two Fibonacci numbers in a row, so the digit list has no two adjacent ones and ends with a one. With the extra bit, every codeword ends in `11`, and `11` appears nowhere else. The code is a [universal code](/universal-code/) of about $1.44\log_2 x$ bits, and after a bit error the decoder is back in step within a few codewords. Apostolico and Fraenkel studied it in 1987.

## In plain words

Every positive whole number can be written as a sum of Fibonacci numbers (1, 2, 3, 5, 8, 13, and so on) in which no two neighbours of the sequence both appear. To find this sum, take the largest Fibonacci number that fits, subtract it, and repeat.

The code lists, for each Fibonacci number from the smallest up to the largest one used, a one if it is in the sum and a zero if it is not. The last listed digit is always a one, and two ones never stand side by side. So the code adds one more one at the end, and the pair "one, one" marks the end of each number.

The decoder adds up the Fibonacci numbers that have a one, and stops when it sees two ones in a row. After a damaged bit, the next pair of ones puts it back in step.

## The problem

The input is a sequence of integers $x_1, \ldots, x_n$, each at least 1, with no known upper bound. The output is one bit string from which a decoder recovers the sequence, with no separators and no parameters. A single bit error in the stream should damage only a few values near it, not the rest of the stream.

Notation: $x$ is one integer to code and $\ell(x)$ is its codeword length in bits. The Fibonacci numbers are $F_1 = F_2 = 1$ and $F_i = F_{i-1} + F_{i-2}$, so $F_2, F_3, F_4, \ldots = 1, 2, 3, 5, 8, \ldots$, and $\varphi = (1 + \sqrt 5)/2$. Logarithms are base 2 unless the base is $\varphi$. Probability statements are for a memoryless source.

## The algorithm

```pseudo id=main
FIB-ENCODE(x, W)                           ▷ x ≥ 1, W is a bit writer
L1  k ← the largest index with F_k ≤ x     ▷ k ≥ 2
L2  d[2..k] ← 0
L3  for i ← k downto 2 do
L4      if F_i ≤ x then d[i] ← 1; x ← x − F_i
L5  write d[2], d[3], …, d[k] to W, then one 1 bit

FIB-DECODE(R)                              ▷ R is a bit reader
L6  x ← 0; i ← 2; prev ← 0
L7  repeat b ← READ-BIT(R)
L8      if b = 1 and prev = 1 then return x
L9      if b = 1 then x ← x + F_i
L10     prev ← b; i ← i + 1
```

Lines L3 and L4 are the greedy Zeckendorf step. When line L4 takes $F_i$, the value left is less than $F_{i-1}$, because $x < F_{i+1} = F_i + F_{i-1}$ before the step. So the next index is never taken, and no two adjacent digits are 1. The top digit $d[k]$ is 1 by the choice of $k$ in line L1. Line L5 writes the digits from the lowest Fibonacci number up, so the top digit is the next-to-last bit and the extra 1 is the last bit.

The decoder adds $F_i$ for each 1 digit. It stops at the first 1 that follows a 1: inside the digit list no two ones are adjacent, so the first such pair is the top digit and the extra bit. The extra bit is not a digit and line L8 returns before line L9 can add it.

To code 0, code $x + 1$.

## Example

Encode $x = 100$. The Fibonacci numbers up to 100 are $F_2, \ldots, F_{11} = 1, 2, 3, 5, 8, 13, 21, 34, 55, 89$, so line L1 gives $k = 11$.

| $i$ | $F_i$ | $x$ before | $d[i]$ | $x$ after |
|---|---|---|---|---|
| 11 | 89 | 100 | 1 | 11 |
| 10 | 55 | 11 | 0 | 11 |
| 9 | 34 | 11 | 0 | 11 |
| 8 | 21 | 11 | 0 | 11 |
| 7 | 13 | 11 | 0 | 11 |
| 6 | 8 | 11 | 1 | 3 |
| 5 | 5 | 3 | 0 | 3 |
| 4 | 3 | 3 | 1 | 0 |
| 3 | 2 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 |

So $100 = 89 + 8 + 3$. Line L5 writes $d[2], \ldots, d[11]$ = `0010100001` and then `1`: the codeword is `00101000011`, 11 bits. The decoder adds $F_4 + F_6 + F_{11} = 3 + 8 + 89$ and stops at the last two bits.

The first codewords:

| $x$ | sum | codeword | $\ell(x)$ |
|---|---|---|---|
| 1 | 1 | 11 | 2 |
| 2 | 2 | 011 | 3 |
| 3 | 3 | 0011 | 4 |
| 4 | 3 + 1 | 1011 | 4 |
| 5 | 5 | 00011 | 5 |
| 6 | 5 + 1 | 10011 | 5 |
| 7 | 5 + 2 | 01011 | 5 |
| 8 | 8 | 000011 | 6 |
| 12 | 8 + 3 + 1 | 101011 | 6 |

The sequence $4, 1, 2$ codes as `1011` `11` `011`. The decoder reads `1011` and stops at the second pair of ones, then reads `11`, then `011`.

## Correctness

The greedy loop of lines L3 and L4 keeps this invariant: the digits chosen so far, with the value $x$ still left, sum to the input, and $x < F_{i+1}$ before index $i$ is tested. At the end $x = 0$, so the digits sum to the input, and by the argument above no two adjacent digits are 1. So the codeword is the digit list of the Zeckendorf representation followed by a 1, and the first pair `11` in it is its last two bits. The decoder stops there and has added exactly the digit values. Since a decoder stops at the first `11`, no codeword is a prefix of another. The full proof is in the proof file.

## Complexity

**Length.** If $F_k \le x < F_{k+1}$, then $\ell(x) = k$. With $\varphi^{k-2} \le F_k$ and $F_{k+1} \le \varphi^k$,

$$\log_\varphi x < \ell(x) \le \log_\varphi x + 2, \qquad \log_\varphi x = \frac{\log_2 x}{\log_2 \varphi} \approx 1.4404\, \log_2 x.$$

Against the [gamma code](/elias-gamma-coding/), the Fibonacci code is longer only for $x = 1$ and $x = 3$, has the same length for $x = 2, 5, 6, 7, 13, 14, 15$, and is shorter for every other $x$. The [delta code](/elias-delta-coding/), with $\log_2 x + 2\log_2\log_2 x$ bits, first beats it at $x = 6765 = F_{20}$, and beats it for each large enough $x$.

**Kraft sum.** Exactly $F_{k+1} - F_k = F_{k-1}$ integers have codewords of length $k$, so the [Kraft sum](/kraft-inequality/) is $\sum_{k \ge 2} F_{k-1} 2^{-k} = 1$, by the generating function $\sum_{j \ge 1} F_j z^j = z/(1 - z - z^2)$ at $z = 1/2$. The code is complete.

**Implied distribution.** The code is optimal for $P(x) = 2^{-\ell(x)} \approx x^{-1.44}$, a power law that falls more slowly than the $x^{-2}$ of the gamma code.

**Time.** The encoder and the decoder each do $\Theta(\log x)$ steps. The encoder needs the Fibonacci numbers up to $x$, which a program keeps in a table of $\Theta(\log x)$ entries, and the digit array of line L2 has $k$ entries. Fast decoders read a byte or a word at a time with precomputed tables.

**Universality.** For a non-increasing distribution with entropy $H$, $E[\log_2 x] \le H$, so $E[\ell] \le 1.4404\,H + 2$. The code is universal but not asymptotically optimal: the ratio tends to $1/\log_2\varphi \approx 1.44$, not to 1.

## Properties

- **Self-synchronizing.** Suppose that no codeword is `11` (all values are at least 2). Then the last three bits of each codeword are `011`. After a single bit error in codeword $j$, the decoder reads codeword $j + 1$ to its true end, because the `0` before its final `11` resets the pair test, and it is in step from codeword $j + 2$ on. At most two values are lost, and one to three wrong values replace them. If values of 1 occur (codeword `11`), a run of them can be read one bit out of step, and the damage lasts until the run ends.
- **Parameter-free and complete.** The Kraft sum is 1.
- **Boundaries visible from any point.** A codeword ends in a 1, so the bit before the start of a codeword is never a 0. So each `011` in the stream ends a codeword, and a decoder can start after any `011`. This lets a program cut, search, or decode a compressed stream in parallel from any point.

## Variants and improvements

- **Higher-order Fibonacci codes.** Apostolico and Fraenkel also built codes on the numeration systems of order $m$, where each number is the sum of the $m$ before it. Each codeword ends in $m$ ones. Larger $m$ suits flatter distributions.
- **Other universal codes.** The [Elias gamma](/elias-gamma-coding/), [delta](/elias-delta-coding/) and [omega](/elias-omega-coding/) codes are shorter for large values on average, but a bit error makes them lose their place for the rest of the stream.
- **Byte-aligned codes.** When decode speed matters more than robustness, [variable-byte encoding](/variable-byte-encoding/) is faster.

## When to use it

Use the Fibonacci code when a stream of integers can suffer bit errors, or when a decoder must start at an arbitrary point, for example for random access into compressed text. It also fits sources whose probabilities fall as a power law with an exponent near 1.44. For values with a known geometric law, a [Golomb code](/golomb-coding/) is shorter. For very large values, the delta code is shorter.

## Pitfalls

- **Writing the digits from the top.** Line L5 must write $d[2]$ first and $d[k]$ last. An encoder that writes the highest digit first puts the top 1 at the start, so the pair `11` no longer marks the end and the decoder cannot find the boundaries.
- **Using $F_1$ and $F_2$ both.** The index in lines L3 and L9 starts at 2. With both $F_1 = 1$ and $F_2 = 1$ as digit places, the representation is not unique and the greedy loop can set two adjacent digits.
- **Carrying the pair test across codewords.** Line L6 sets prev ← 0 at the start of each codeword. A stream decoder that keeps prev = 1 from the end of the last codeword stops at the first 1 of the next codeword.
- **Adding the extra bit.** Line L8 must test for the end before line L9 adds $F_i$. With the tests in the other order, the decoder adds one more Fibonacci number for the extra 1 bit.

## Implementations

## History

Number systems based on Fibonacci numbers go back to Zeckendorf's theorem (published 1972) and to earlier work by Lekkerkerker. Apostolico and Fraenkel (1987) studied codes built on these representations for the transmission of strings of unknown length, and showed their robustness to bit errors. Later work used the code for compressed text that can be searched without decompression.

## References
