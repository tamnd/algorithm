---
tag: 6VVNKC
kind: algorithm
slug: elias-gamma-coding
name: Elias gamma coding
aliases:
- gamma code
- Elias gamma code
area: compression-and-coding/entropy-coding
level: intro
summary: Codes an integer x >= 1 as floor(log2 x) zeros followed by the binary digits of x, so the codeword has 2 floor(log2 x) + 1 bits. A universal code with no parameter.
model: word-ram
complexity:
  vars: {x: the integer to code}
  time: {worst: Θ(log x), average: Θ(log x), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1975
  people: [Peter Elias]
  note: Elias defined the gamma, delta and omega codeword sets in his 1975 paper on universal codes for the integers.
prereqs: [unary-coding, floor-log2]
see_also: [elias-delta-coding, elias-omega-coding, exp-golomb-coding, universal-code, fibonacci-coding, golomb-coding, kraft-inequality, prefix-code]
sources:
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 194 to 203 (the codeword sets gamma and gamma prime, and the proof that gamma is universal)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.3, Gamma and Delta, and Table 3 (arXiv:1908.10598v2)
  - url: https://www.itu.int/rec/T-REC-H.264
    title: ITU-T Recommendation H.264, Advanced video coding for generic audiovisual services (11/2007 edition)
    locator: Section 9.1, Parsing process for Exp-Golomb codes, Tables 9-1 and 9-2 (the ue(v) code is the gamma code of codeNum + 1)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 2, Entropy and Coding (variable-length codes for integers)
---

The Elias gamma code writes an integer $x \ge 1$ as $\lfloor \log_2 x \rfloor$ zero bits followed by the binary digits of $x$. The zeros tell the decoder how many digits follow, so the code is a [prefix code](/prefix-code/) that needs no parameter and no table. A codeword has $2\lfloor \log_2 x \rfloor + 1$ bits, about twice the length of $x$ in binary. Peter Elias defined it in 1975 as one of his [universal codes](/universal-code/), and it is the ue(v) code of H.264 under another name.

## In plain words

To send a number of any size, the reader must know where the number ends. The gamma code first says how many binary digits the number has, and then gives the digits.

The length goes first, written as a run of zeros: one zero for each digit after the first. The digits of the number follow. The first digit of a number in binary is always a one, so that one also marks the end of the run of zeros. The decoder counts zeros until it sees a one, and then reads that many more digits.

Small numbers get short codewords: the number one is the single bit one. A number with twenty binary digits takes thirty-nine bits.

## The problem

The input is a sequence of integers $x_1, \ldots, x_n$, each at least 1, with no known upper bound. The output is one bit string from which the decoder can recover the sequence, with no separators and no side information. Short codewords should go to small integers, because in the usual inputs (gaps in sorted lists, counts, run lengths) small values are the most frequent.

Notation: $x$ is one integer to code, $N = \lfloor \log_2 x \rfloor$, so $x$ has $N + 1$ binary digits, and $\ell(x)$ is the codeword length in bits. All logarithms are base 2. Probability statements are for a memoryless source.

## The algorithm

```pseudo id=main
GAMMA-ENCODE(x, W)                         ▷ x ≥ 1, W is a bit writer
L1  N ← ⌊log₂ x⌋                           ▷ x has N + 1 binary digits
L2  write N zero bits to W
L3  write the N + 1 binary digits of x to W, most significant first

GAMMA-DECODE(R)                            ▷ R is a bit reader
L4  N ← 0
L5  while READ-BIT(R) = 0 do N ← N + 1      ▷ the 1 that stops the loop is the top digit of x
L6  x ← 1
L7  repeat N times: x ← 2x + READ-BIT(R)
L8  return x
```

The encoder writes the length of $x$ in [unary](/unary-coding/), in the convention "zeros, then a one", and then the rest of $x$ in binary. It does not write the top digit twice: the one at the end of the unary part is the top digit of $x$. Line L1 is a [floor of the base-2 logarithm](/floor-log2/), which is the bit length of $x$ minus one; compute it with integer operations, not with floating point.

The decoder reverses the steps. Line L5 counts the zeros. The one that ends the count is the leading digit of $x$, so line L6 starts with $x = 1$, and line L7 appends the other $N$ digits.

**Zero and signed values.** The code has no codeword for 0. To code $x \ge 0$, code $x + 1$ and subtract 1 after the decode. To code any integer, first map it to a positive integer, for example $0, 1, -1, 2, -2, \ldots \mapsto 1, 2, 3, 4, 5, \ldots$, as the se(v) code of H.264 does.

## Example

The first codewords. The space separates the unary part from the low digits.

| $x$ | binary | $N$ | codeword | $\ell(x)$ |
|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 1 |
| 2 | 10 | 1 | 0 10 | 3 |
| 3 | 11 | 1 | 0 11 | 3 |
| 4 | 100 | 2 | 00 100 | 5 |
| 5 | 101 | 2 | 00 101 | 5 |
| 7 | 111 | 2 | 00 111 | 5 |
| 8 | 1000 | 3 | 000 1000 | 7 |
| 13 | 1101 | 3 | 000 1101 | 7 |
| 113 | 1110001 | 6 | 000000 1110001 | 13 |

Decode the codeword `0001101` of 13:

| step | bit read | $N$ | $x$ |
|---|---|---|---|
| L5 | 0 | 1 | |
| L5 | 0 | 2 | |
| L5 | 0 | 3 | |
| L5 | 1 (loop stops) | 3 | |
| L6 | | 3 | 1 |
| L7 | 1 | 3 | 3 |
| L7 | 0 | 3 | 6 |
| L7 | 1 | 3 | 13 |

The sequence $5, 1, 13, 2$ codes as `00101` `1` `0001101` `010`, which is 16 bits with no separators.

## Correctness

Two facts make the code correct. First, GAMMA-DECODE reads back exactly the bits that GAMMA-ENCODE wrote for $x$, and returns $x$: the loop of line L5 stops at the first one, which is the top digit of $x$, after exactly $N$ zeros, and the loop of line L7 keeps the invariant that $x$ equals the first $j + 1$ digits of the original value after $j$ rounds. Second, the codeword set is prefix-free, so a concatenation of codewords splits in only one way, and the decoder of a stream returns the sequence that was coded. The full proof is in the proof file.

## Complexity

**Length.** The codeword has $N$ zeros and $N + 1$ digits, so

$$\ell(x) = 2\lfloor \log_2 x \rfloor + 1 \le 2\log_2 x + 1.$$

There are exactly $2^N$ integers with $N + 1$ digits, and each of them has a codeword of $2N + 1$ bits.

**Time.** With one bit per step, the encoder and the decoder each take $\ell(x) = \Theta(\log x)$ steps in the worst case, and one step for $x = 1$. On a [word RAM](/word-ram/) with $w$-bit words and a count-leading-zeros instruction, the decoder finds $N$ with one instruction on a buffered word and extracts the $N$ digits with a shift and a mask, so a codeword that fits in a word takes $O(1)$ steps. The extra space is $\Theta(1)$ words.

**Kraft sum.** The $2^N$ codewords of length $2N + 1$ add $2^N \cdot 2^{-(2N+1)} = 2^{-(N+1)}$ to the [Kraft sum](/kraft-inequality/). So the codewords of $1, \ldots, 2^K - 1$ have Kraft sum $\sum_{N=0}^{K-1} 2^{-(N+1)} = 1 - 2^{-K}$, and the full sum is 1. The code is complete: no codeword can be shortened.

**Implied distribution.** The code is optimal for the distribution $P(x) = 2^{-\ell(x)}$, which is about $1/(2x^2)$. So the gamma code suits sources where the probability falls about as fast as $1/x^2$.

**Universality.** If $P$ is a non-increasing distribution on the positive integers, then $P(x) \le 1/x$, so $\log_2 x \le \log_2(1/P(x))$ and $E[\log_2 x] \le H(P)$. With the length bound above, $E[\ell] \le 2H(P) + 1$. So the gamma code is universal, but the factor 2 does not go away: it is not asymptotically optimal. The [universal code](/universal-code/) page gives the definitions and the proof.

## Properties

- **Parameter-free.** The code needs no knowledge of the source.
- **Prefix-free and complete.** The Kraft sum is exactly 1.
- **Not byte-aligned.** Codewords have odd lengths and cross byte boundaries, so a decoder needs a bit reader.
- **Fragile.** One flipped bit in the unary part changes the length of the codeword, and the decoder loses its place for the rest of the stream. [Fibonacci coding](/fibonacci-coding/) recovers from such errors.

## Variants and improvements

- **Elias delta and omega.** [Elias delta coding](/elias-delta-coding/) writes the length $N + 1$ with the gamma code instead of in unary, and [Elias omega coding](/elias-omega-coding/) repeats this step. Both are asymptotically optimal and are shorter than gamma for large $x$.
- **Exp-Golomb.** The order-0 [exp-Golomb code](/exp-golomb-coding/) is the gamma code of $x + 1$. The order-$k$ code adds $k$ fixed low digits, which suits larger values.
- **The ones-first form.** Some texts write the unary part as ones ended by a zero, for example $1 \mapsto 0$, $2 \mapsto 100$, $3 \mapsto 101$. The lengths and the properties are the same.
- **The interleaved form.** Elias's paper also gives an arrangement that interleaves the length bits with the digits of $x$. It has the same lengths and lets the decoder build $x$ in one pass without a count.
- **Golomb and Rice.** If the values follow a geometric law with a known mean, [Golomb coding](/golomb-coding/) or [Rice coding](/rice-coding/) is shorter.

## When to use it

Use the gamma code for small positive integers with an unknown upper bound and a law that falls quickly, for example gaps in dense posting lists, the lengths of short runs, or header fields. It needs no parameter, so it has no cost of model description and no pass to fit a parameter. For gaps with a known density, a [Golomb code](/golomb-coding/) is shorter. For large values, [Elias delta coding](/elias-delta-coding/) is shorter. When decode speed matters more than size, use a byte-aligned code such as [variable-byte encoding](/variable-byte-encoding/).

## Pitfalls

- **Zero has no codeword.** GAMMA-ENCODE$(0)$ must fail: line L1 has no value for $\log_2 0$. Code $x + 1$ if 0 can occur, and decode with a subtraction.
- **Floating-point logarithm in line L1.** `floor(log2(x))` in double precision is wrong for large $x$: for $x = 2^{49} - 1$ it gives 49, not 48, and the codeword gets one bit too many. Use the bit length of the integer, or a count-leading-zeros instruction.
- **An unbounded unary part.** On damaged or hostile input, line L5 may count many zeros. A decoder that stores $x$ in a 64-bit word must reject $N \ge 64$ before line L7, or $x$ overflows.
- **Two conventions in one system.** A writer that uses "zeros, then a one" and a reader that uses "ones, then a zero" agree on lengths, so short tests can pass, but every value decodes wrong. Fix the convention in the format description.

## Implementations

## History

Peter Elias defined the codeword sets gamma, delta and omega in 1975, in the paper that also defined universal codes for the integers. The same code appears in H.264 (2003) as the Exp-Golomb code ue(v) of order 0, applied to $x + 1$.

## References
