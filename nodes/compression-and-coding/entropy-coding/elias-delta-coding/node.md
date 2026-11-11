---
tag: 5Y2VCC
kind: algorithm
slug: elias-delta-coding
name: Elias delta coding
aliases:
- delta code
- Elias delta code
area: compression-and-coding/entropy-coding
level: intro
summary: Codes x >= 1 as the gamma code of its bit length, then the binary digits of x without the leading 1. The length is about log2 x + 2 log2 log2 x, so the code is asymptotically optimal.
model: word-ram
complexity:
  vars: {x: the integer to code}
  time: {worst: Θ(log x), average: Θ(log x), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1975
  people: [Peter Elias]
  note: Elias defined delta in his 1975 paper on universal codes, as the first of his codes that is asymptotically optimal.
prereqs: [elias-gamma-coding, floor-log2]
see_also: [elias-omega-coding, universal-code, fibonacci-coding, exp-golomb-coding, variable-byte-encoding, kraft-inequality, unary-coding, prefix-code]
sources:
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 194 to 203 (the codeword set delta and its asymptotic optimality)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.3, Gamma and Delta, and Table 3 (arXiv:1908.10598v2)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 2, Entropy and Coding (variable-length codes for integers)
---

The Elias delta code writes an integer $x \ge 1$ as the [gamma codeword](/elias-gamma-coding/) of its bit length, followed by the binary digits of $x$ without the leading one. The gamma code spends about $2\log_2 x$ bits because it writes the length in [unary](/unary-coding/); the delta code writes the length with the gamma code, so it spends about $\log_2 x + 2\log_2\log_2 x$ bits. The ratio of this length to $\log_2 x$ tends to 1, so delta is an asymptotically optimal [universal code](/universal-code/). Peter Elias defined it in 1975.

## In plain words

A number in binary does not say where it ends, so a code for numbers of any size must first say how many digits follow. The gamma code says this with a run of zeros, one for each digit. For a large number that run is as long as the number itself.

The delta code writes the count of digits in a short form instead: it writes the count with the gamma code. Then it writes the digits of the number. The first digit of a number in binary is always a one, so the delta code leaves it out, and the decoder puts it back.

For small numbers the delta code is a little longer than the gamma code. From thirty-two up it is always shorter, and for very large numbers it is close to half the length.

## The problem

The input is a sequence of integers $x_1, \ldots, x_n$, each at least 1, with no known upper bound. The output is one bit string from which a decoder recovers the sequence, with no separators and no parameters. The codeword of $x$ should be not much longer than the $\lfloor \log_2 x \rfloor + 1$ binary digits of $x$, also for large $x$.

Notation: $x$ is one integer to code, $N = \lfloor \log_2 x \rfloor$, so $x$ has $N + 1$ binary digits, and $\ell(x)$ is the codeword length in bits. All logarithms are base 2. Probability statements are for a memoryless source.

## The algorithm

```pseudo id=main
DELTA-ENCODE(x, W)                         ▷ x ≥ 1, W is a bit writer
L1  N ← ⌊log₂ x⌋                           ▷ x has N + 1 binary digits
L2  GAMMA-ENCODE(N + 1, W)                 ▷ the bit length of x
L3  write the N low digits of x to W, most significant first   ▷ the leading 1 is left out

DELTA-DECODE(R)                            ▷ R is a bit reader
L4  N ← GAMMA-DECODE(R) − 1
L5  x ← 1                                  ▷ put back the leading 1
L6  repeat N times: x ← 2x + READ-BIT(R)
L7  return x
```

Line L1 is a [floor of the base-2 logarithm](/floor-log2/), computed as the bit length of $x$ minus one. Line L2 writes the bit length $N + 1$, which is at least 1, so the gamma code can take it. Line L3 writes $x - 2^N$ in exactly $N$ bits.

The decoder reads the gamma codeword in line L4 and gets the bit length, so it knows that $N$ more bits follow. Lines L5 and L6 rebuild $x$ from an implied leading one and the $N$ bits that follow.

To code 0, code $x + 1$. To code signed values, map them to positive integers first, for example $0, -1, 1, -2, 2, \ldots \mapsto 1, 2, 3, 4, 5, \ldots$.

## Example

Encode $x = 10$, binary `1010`. Line L1 gives $N = 3$. Line L2 writes the gamma codeword of 4, which is `00100`. Line L3 writes the low three digits `010`. The codeword is `00100` `010`, 8 bits; the gamma codeword of 10 has 7 bits.

Decode `00100010`:

| step | bits read | $N$ | $x$ |
|---|---|---|---|
| L4 | `00100` (gamma of 4) | 3 | |
| L5 | | 3 | 1 |
| L6 | `0` | 3 | 2 |
| L6 | `1` | 3 | 5 |
| L6 | `0` | 3 | 10 |

The first codewords. The space separates the gamma part from the low digits.

| $x$ | binary | $N$ | codeword | $\ell(x)$ | gamma length |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 10 | 1 | 010 0 | 4 | 3 |
| 3 | 11 | 1 | 010 1 | 4 | 3 |
| 4 | 100 | 2 | 011 00 | 5 | 5 |
| 7 | 111 | 2 | 011 11 | 5 | 5 |
| 8 | 1000 | 3 | 00100 000 | 8 | 7 |
| 16 | 10000 | 4 | 00101 0000 | 9 | 9 |
| 17 | 10001 | 4 | 00101 0001 | 9 | 9 |
| 32 | 100000 | 5 | 00110 00000 | 10 | 11 |
| 1000 | 1111101000 | 9 | 0001010 111101000 | 16 | 19 |

## Correctness

The decoder reads the gamma codeword of $N + 1$ in line L4 and gets $N$, by the correctness of the gamma decoder. After that, the loop of line L6 keeps the invariant that after $j$ rounds, $x$ equals the top $j + 1$ binary digits of the coded value. After $N$ rounds $x$ is the coded value, and the reader stands at the end of the codeword. The codeword set is prefix-free: two codewords with different bit lengths differ inside their gamma parts, which form a prefix code, and two codewords with the same bit length have the same length. So a stream of codewords splits in one way only. The full proof is in the proof file.

## Complexity

**Length.** The gamma codeword of $N + 1$ has $2\lfloor \log_2(N+1) \rfloor + 1$ bits and $N$ bits follow, so

$$\ell(x) = \lfloor \log_2 x \rfloor + 2\lfloor \log_2(\lfloor \log_2 x \rfloor + 1) \rfloor + 1 \le \log_2 x + 2\log_2(\log_2 x + 1) + 1.$$

So $\ell(x)/\log_2 x \to 1$ as $x$ grows. For $x = 2^{16}$ the codeword has 25 bits against 33 for gamma; for $x = 2^{64}$ it has 77 bits against 129.

**Crossover with gamma.** The delta codeword is longer than the gamma codeword for $x = 2, 3$ and $8 \le x \le 15$, has the same length for $x = 1$, $4 \le x \le 7$ and $16 \le x \le 31$, and is strictly shorter for each $x \ge 32$.

**Time.** With one bit per step, encoding and decoding take $\ell(x) = \Theta(\log x)$ steps, and one step for $x = 1$. On a [word RAM](/word-ram/) with a count-leading-zeros instruction, each part of a codeword that fits in a word takes $O(1)$ steps. The extra space is $\Theta(1)$ words.

**Kraft sum.** The $2^N$ integers with $N + 1$ digits all have codewords of length $N + \ell_\gamma(N+1)$, so they add $2^{-\ell_\gamma(N+1)}$ to the [Kraft sum](/kraft-inequality/). Summed over $N$ this is the Kraft sum of the gamma code, which is 1. The delta code is complete.

**Universality and asymptotic optimality.** For a non-increasing distribution $P$ with entropy $H$, $E[\log_2 x] \le H$. The function $\log_2(t + 1)$ is concave, so by Jensen's inequality

$$E[\ell] \le H + 2\log_2(H + 1) + 1.$$

So $E[\ell]/\max(1, H)$ is bounded by a constant, and it tends to 1 as $H$ grows. This is the definition of an asymptotically optimal [universal code](/universal-code/). The gamma code has a ratio that tends to 2.

## Properties

- **Parameter-free.** The code needs no knowledge of the source.
- **Prefix-free and complete.** The Kraft sum is exactly 1.
- **Asymptotically optimal.** The overhead above $\log_2 x$ grows as $2\log_2\log_2 x$.
- **Not byte-aligned and fragile.** As with the gamma code, one wrong bit in the length part makes the decoder lose its place for the rest of the stream.

## Variants and improvements

- **Elias omega.** [Elias omega coding](/elias-omega-coding/) codes the length of the length again, and so on, until the length is 1. Its overhead is a sum of iterated logarithms, so it is shorter than delta for each $x \ge 2^{511}$. For most values below $2^{127}$, delta is the shorter of the two.
- **Unary convention.** Texts that write unary as ones ended by a zero get the same lengths, for example $2 \mapsto 100\,0$ and $8 \mapsto 11000\,000$.
- **Zeta codes.** Boldi and Vigna's zeta codes for web graphs use a parameter to fit power-law gaps, where delta is not tuned to the exponent.
- **Fibonacci coding.** [Fibonacci coding](/fibonacci-coding/) is also universal and recovers after a bit error, at about $1.44\log_2 x$ bits per value.

## When to use it

Use the delta code for positive integers with an unknown range when large values occur often enough that the gamma code wastes space, for example document gaps in sparse posting lists, offsets, or lengths in a self-describing format. If most values are below 32, the gamma code is as short or shorter. If the values follow a geometric law with a known mean, a [Golomb code](/golomb-coding/) is shorter. If decode speed is the goal, use a byte-aligned code such as [variable-byte encoding](/variable-byte-encoding/).

## Pitfalls

- **The leading 1 written twice.** Line L3 must write the $N$ low digits only. An encoder that writes "the $N + 1$ digits of $x$" still decodes in its own tests if the decoder makes the same mistake, but the stream does not match any other implementation and each codeword is one bit too long.
- **The length minus one.** Line L4 must subtract 1: the gamma part holds the bit length $N + 1$, not $N$. Writing GAMMA-ENCODE$(N, W)$ in line L2 fails for $x = 1$, because the gamma code has no codeword for 0.
- **Floating-point logarithm in line L1.** `floor(log2(x))` in double precision gives 49 for $x = 2^{49} - 1$. Use the bit length of the integer.
- **An oversize length on bad input.** A damaged stream can make line L4 return a huge $N$. A decoder that stores $x$ in a 64-bit word must reject $N \ge 64$ before line L6.

## Implementations

## History

Peter Elias defined the codeword sets gamma, delta and omega in 1975 in the paper that introduced universal codes for the integers. The delta code was the first of the three that he showed to be asymptotically optimal. Inverted-index systems took up the gamma and delta codes for document gaps in the 1990s.

## References
