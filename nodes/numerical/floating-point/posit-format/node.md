---
tag: 0CXRC5
kind: definition
slug: posit-format
name: Posit number format
aliases:
- posits
- unum type III
- posit arithmetic
area: numerical/floating-point
level: research
summary: A tapered-precision alternative to IEEE floats with variable-length regime field.
prereqs: [floating-point-arithmetic, ieee-754, relative-error]
see_also: [bfloat16, logarithmic-number-system, kulisch-accumulator, floating-point-model, special-floating-point-values, subnormal-numbers, round-to-nearest-even, block-floating-point]
sources:
  - url: https://posithub.org/docs/posit_standard-2.pdf
    title: Posit Working Group, Standard for Posit Arithmetic (2022)
    locator: the definition of posit<n, 2> with es = 2 for every n, the decoding of the regime, exponent and fraction fields, NaR, the rounding rule that never rounds to 0 or NaR, and the quire of 16n bits
  - paper: doi:10.14529/jsfi170206
    title: John L. Gustafson and Isaac Yonemoto, Beating floating point at its own game, posit arithmetic, Supercomputing Frontiers and Innovations 4(2) (2017), 71-86
    locator: the original definition of posits with the parameter es, useed = 2^(2^es), and the comparison with IEEE 754 formats
  - book: isbn:9781482239867
    title: John L. Gustafson, The End of Error, Unum Computing, CRC Press, 2015
    locator: the unum type I format that posits replace
  - paper: doi:10.1145/3316279.3316285
    title: Florent de Dinechin, Luc Forget, Jean-Michel Muller and Yohann Uguen, Posits, the good, the bad and the ugly, Conference for Next Generation Arithmetic (CoNGA 2019)
    locator: the loss of precision far from 1, the failure of Sterbenz's lemma and of exact error terms for TwoSum and TwoProduct, and the cost of hardware decoding
---

## Definition

Fix a width $n \ge 3$ and an exponent size $\mathrm{es} \ge 0$. The 2022 Posit Standard fixes $\mathrm{es} = 2$ for every $n$, and that is the default here. Let $\mathrm{useed} = 2^{2^{\mathrm{es}}}$, which is 16 for $\mathrm{es} = 2$. A **posit**$\langle n, \mathrm{es} \rangle$ is an $n$-bit string $b$ that is decoded as follows.

1. **Special patterns.** All zeros is the real number $0$. A 1 followed by $n - 1$ zeros is **NaR**, "not a real". There is one zero and one NaR, with no signed zero, no infinities and no payloads.
2. **Sign.** If the leading bit is 1, decode the two's complement $-b \bmod 2^{n}$ instead and negate the result. Negation is integer negation of the bit string.
3. **Regime.** After the sign bit, read the run of identical bits $r r \ldots r$ of length $m$. The run ends at the first opposite bit or at the end of the string. The regime value is $k = m - 1$ if $r = 1$ and $k = -m$ if $r = 0$. The terminating opposite bit, if present, is skipped.
4. **Exponent.** The next $\mathrm{es}$ bits are an unsigned integer $e$. Bits cut off by the end of the string count as 0.
5. **Fraction.** The remaining $\ell \ge 0$ bits are a fraction $f = F / 2^{\ell}$ with $0 \le F < 2^{\ell}$.

The value of a posit with sign bit 0 is
$$
x = \mathrm{useed}^{k} \cdot 2^{e} \cdot (1 + f) = 2^{\,k 2^{\mathrm{es}} + e}\,(1 + f).
$$

**Rounding.** A real $y$ is rounded to the posit nearest to it, with ties going to the posit whose bit string ends in 0. There are two exceptions: a nonzero $y$ never rounds to 0, and a finite $y$ never rounds to NaR. So values above the largest posit $\mathrm{maxpos} = \mathrm{useed}^{\,n-2}$ round to $\mathrm{maxpos}$, and nonzero values below $\mathrm{minpos} = \mathrm{useed}^{-(n-2)}$ in magnitude round to $\pm\mathrm{minpos}$. The standard requires $+, -, \times, \div$, $\sqrt{\cdot}$ and fused operations to be correctly rounded in this sense. Operations with no real result, such as $0/0$, $1/0$ and $\sqrt{-1}$, return NaR.

**Tapered precision.** The regime is a unary code for the scale. Numbers near 1 have a short regime and leave the most bits to the fraction. Numbers near $\mathrm{maxpos}$ or $\mathrm{minpos}$ have a long regime and few or no fraction bits. For $|x| \in [\mathrm{useed}^{k}, \mathrm{useed}^{k+1})$ the fraction has
$$
\ell = \max\bigl(0,\ n - 1 - m - 1 - \mathrm{es}\bigr) \quad\text{bits, with } m = k + 1 \text{ for } k \ge 0 \text{ and } m = -k \text{ for } k < 0,
$$
so the relative spacing $2^{-\ell}$ varies with the size of $x$. In IEEE 754 formats the relative spacing is the same in every binade of normal numbers.

**Quire.** The standard also defines the quire, a fixed-point register of $16n$ bits, which accumulates sums of products of posits exactly. It is the posit form of the [Kulisch accumulator](/kulisch-accumulator/).

## Examples and non-examples

**Examples, posit$\langle 8, 2 \rangle$.** Here $\mathrm{useed} = 16$.

| bits | regime | $e$ | $f$ | value |
|---|---|---|---|---|
| `0 1 0 00 000` | $m = 1$, $k = 0$ | 0 | 0 | $1$ |
| `0 1 0 00 001` | $k = 0$ | 0 | $1/8$ | $9/8$ |
| `0 0 1 11 111` | $m = 1$, $k = -1$ | 3 | $7/8$ | $15/16$ |
| `0 1 1 0 10 11` | $m = 2$, $k = 1$ | 2 | $3/4$ | $16 \cdot 4 \cdot 1.75 = 112$ |
| `1 0 0 1 0 1 0 1` | two's complement of the row above | | | $-112$ |
| `0 1 1 1 1 1 1 1` | $m = 7$, $k = 6$ | cut off, 0 | none | $16^{6} = 2^{24} = \mathrm{maxpos}$ |
| `0 0 0 0 0 0 0 1` | $m = 6$, $k = -6$ | 0 | none | $2^{-24} = \mathrm{minpos}$ |

The 255 real posit$\langle 8, 2 \rangle$ values, ordered as reals, are in the same order as their bit strings read as signed 8-bit integers. This holds for every $n$, with NaR as the smallest integer. So posit comparison is integer comparison.

**Precision near 1 and far from it.** posit$\langle 32, 2 \rangle$ has 27 fraction bits for $|x| \in [1, 16)$, four more than binary32. Its range is $[2^{-120}, 2^{120}]$. posit$\langle 16, 2 \rangle$ has 11 fraction bits near 1, one more than binary16, so the neighbours of $1$ are $1 + 2^{-11}$ and $1 - 2^{-12}$. At $10^{6}$ its relative spacing is about $4 \times 10^{-3}$, and at $10^{-6}$ about $7 \times 10^{-3}$. Binary16 reaches $10^{-6}$ only as a subnormal, with a relative spacing of about $6 \times 10^{-2}$, and it overflows above 65504. Its largest value is $2^{56} \approx 7.2 \times 10^{16}$.

**Non-examples.**

- $1/3$ is not a posit$\langle 16, 2 \rangle$. Its neighbours are $0.333251953125$ and $0.3333740234375$, and it rounds to the second one.
- $+\infty$ is not a posit. $2^{200}$ rounded to posit$\langle 32, 2 \rangle$ is $\mathrm{maxpos} = 2^{120}$, not an overflow. This saturation is a design choice of the standard, and it means that $\mathrm{maxpos} \times 2 = \mathrm{maxpos}$.
- $-0$ and quiet or signalling NaNs are not posits. There is no analogue of [IEEE special values](/special-floating-point-values/) apart from NaR.
- There are no [subnormal numbers](/subnormal-numbers/). The tapering of the regime plays their role at both ends of the range.
- Unum type I (variable width with an exact-or-open bit) and unum type II (a lookup-table format on the projective reals) are earlier designs by Gustafson. They are not posits.

## Related definitions

- **IEEE 754 binary formats.** [IEEE 754](/ieee-754/) fixes the exponent width per format and so has uniform relative precision $u$ over its normal range. The [standard model](/floating-point-model/) with one $u$ applies to it. For posits it applies only with a $u$ that depends on the magnitude of the result, which makes classical error bounds weaker far from 1.
- **Exact error properties.** For IEEE arithmetic, $x - y$ is exact when $y/2 \le x \le 2y$ ([Sterbenz's lemma](/sterbenz-lemma/)), and the rounding errors of $+$ and $\times$ are floats. De Dinechin et al. (2019) show that both facts can fail for posits, because the error term may need more fraction bits than a posit of its smaller magnitude has.
- **[bfloat16](/bfloat16/).** This is another format aimed at machine learning, with 8 bits of precision and the range of binary32. Posits instead trade range for precision near 1.
- **[Logarithmic number system](/logarithmic-number-system/).** It has uniform relative precision over a fixed range. Posits taper, and LNS does not.
- **Rounding.** Posit rounding is [round to nearest even](/round-to-nearest-even/) on the bit string, with saturation instead of overflow and underflow.

## References
