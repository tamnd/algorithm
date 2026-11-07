---
tag: Z717HS
kind: definition
slug: bfloat16
name: bfloat16
aliases:
- brain floating point
- BF16
- bfloat16 format
area: numerical/floating-point
level: intro
summary: 16-bit binary format with the exponent range of float32 and a short significand.
prereqs: [floating-point-arithmetic, ieee-754]
see_also: [floating-point-model, block-floating-point, stochastic-rounding, double-rounding, round-to-nearest-even, subnormal-numbers, posit-format, fused-multiply-add]
sources:
  - url: https://arxiv.org/abs/1905.12322
    title: Dhiraj Kalamkar et al., A study of BFLOAT16 for deep learning training, arXiv 1905.12322 (2019)
    locator: the description of the BFLOAT16 format, its relation to FP32, and the conversion from FP32 with round to nearest even
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 3.3 (the parameters that define a format) and Clause 3.6 (the interchange formats; bfloat16 is not one of them)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.1, Floating-Point Numbers (the parameters of a format); Section 3.4.6, Binary16 (half-precision) support
  - paper: doi:10.1017/S0962492922000022
    title: Nicholas J. Higham and Theo Mary, Mixed precision algorithms in numerical linear algebra, Acta Numerica 31 (2022), 347-414
    locator: the table of the parameters of the formats fp16, bfloat16, fp32 and fp64 (unit roundoff, range)
---

bfloat16 is a 16-bit binary [floating-point](/floating-point-arithmetic/) format with 1 sign bit, 8 exponent bits and 7 stored fraction bits, so it has the same exponent range as binary32 but only 8 bits of precision. A bfloat16 value is exactly the upper half of a binary32 value, so a conversion between the two is a shift, plus a rounding step in one direction. The format was introduced by Google Brain for the training of neural networks, where the range matters more than the precision, and is now supported by TPUs and by many CPUs and GPUs. It is not one of the interchange formats of [IEEE 754](/ieee-754/)-2019.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; $u = \tfrac12\beta^{1-p}$ is the unit roundoff for rounding to nearest, and $\mathrm{fl}(\cdot)$ is the rounded value (see [floating-point arithmetic](/floating-point-arithmetic/)).

**bfloat16** is the system with $\beta = 2$, $p = 8$, $e_{\min} = -126$, $e_{\max} = 127$, encoded in 16 bits as follows. A word $b_{15} b_{14} \cdots b_0$ has sign $s = b_{15}$, biased exponent $E = (b_{14} \cdots b_7)_2 \in [0, 255]$ and fraction $T = (b_6 \cdots b_0)_2 \in [0, 127]$. Its value is

$$v = \begin{cases} (-1)^{s} \, 2^{E - 127} \, (1 + T/2^{7}) & 1 \le E \le 254 \quad \text{(normal)}, \\ (-1)^{s} \, 2^{-126} \, (T/2^{7}) & E = 0 \quad \text{(zero or subnormal)}, \\ (-1)^{s} \infty & E = 255, \ T = 0, \\ \text{NaN} & E = 255, \ T \ne 0. \end{cases}$$

This is the encoding of binary32 with the 16 low fraction bits removed. So if $h$ is a bfloat16 word, the binary32 word $h \cdot 2^{16}$ (the 16-bit pattern followed by 16 zero bits) has exactly the same value.

The derived constants follow from $p$, $e_{\min}$ and $e_{\max}$.

| quantity | bfloat16 | binary16 | binary32 |
|---|---|---|---|
| bits (sign, exponent, fraction) | 1, 8, 7 | 1, 5, 10 | 1, 8, 23 |
| precision $p$ | 8 | 11 | 24 |
| unit roundoff $u$ | $2^{-8} \approx 3.91 \times 10^{-3}$ | $2^{-11} \approx 4.88 \times 10^{-4}$ | $2^{-24} \approx 5.96 \times 10^{-8}$ |
| largest finite | $(2 - 2^{-7}) 2^{127} \approx 3.39 \times 10^{38}$ | 65504 | $(2 - 2^{-23}) 2^{127} \approx 3.40 \times 10^{38}$ |
| smallest normal | $2^{-126} \approx 1.18 \times 10^{-38}$ | $2^{-14} \approx 6.10 \times 10^{-5}$ | $2^{-126}$ |
| smallest subnormal | $2^{-133} \approx 9.18 \times 10^{-41}$ | $2^{-24} \approx 5.96 \times 10^{-8}$ | $2^{-149}$ |

**Conversion from binary32.** Let $b$ be the 32-bit pattern of a finite binary32 value. Rounding to nearest, ties to even, gives the bfloat16 pattern

$$h = \left\lfloor \frac{b + \texttt{0x7FFF} + \left(\lfloor b / 2^{16} \rfloor \bmod 2\right)}{2^{16}} \right\rfloor.$$

*Why it works.* Write $b = 2^{16} H + L$ with $0 \le L < 2^{16}$. The candidates are $H$ and $H + 1$ (a carry from the fraction into the exponent field gives the next binade, or infinity from the largest binade, which is the correct overflow result). If $L < 2^{15}$, the sum is below $2^{16}(H + 1)$ and $h = H$. If $L > 2^{15}$, then $L + \texttt{0x7FFF} \ge 2^{16}$ and $h = H + 1$. If $L = 2^{15}$ (a tie), $h = H + 1$ exactly when $H$ is odd. Because the binary32 encoding is monotone in the magnitude, "nearer pattern" is "nearer value". A NaN needs a separate test, because the formula can turn a NaN with only low fraction bits into infinity. Truncation, $h = \lfloor b/2^{16} \rfloor$, is rounding toward zero.

A binary64 value that is first rounded to binary32 and then to bfloat16 is rounded twice, which can differ from one rounding to bfloat16: see [double rounding](/double-rounding/).

## Examples and non-examples

The table rounds binary32 values to bfloat16 with ties to even.

| real | binary32 pattern | bfloat16 pattern | bfloat16 value |
|---|---|---|---|
| $1$ | 0x3F800000 | 0x3F80 | $1$ |
| $\pi$ | 0x40490FDB | 0x4049 | $3.140625$ |
| $0.1$ | 0x3DCCCCCD | 0x3DCD | $0.10009765625$ |
| $1 + 2^{-8}$ | 0x3F808000 | 0x3F80 | $1$ (a tie, to even) |
| $257$ | 0x43808000 | 0x4380 | $256$ (a tie, to even) |
| $3 \times 10^{38}$ | 0x7F61B1E6 | 0x7F62 | $3.00405527047391 \times 10^{38}$ |
| $3.4 \times 10^{38}$ | 0x7F7FC99E | 0x7F80 | $+\infty$ (overflow) |
| $65504$ | 0x477FE000 | 0x4780 | $65536$ |

- **Few digits.** $\pi$ becomes $3.140625$, so bfloat16 keeps between 2 and 3 significant decimal digits ($\log_{10} 2^{8} \approx 2.4$). The integers are exact only up to $2^{8} = 256$: $257$ rounds to $256$.
- **Large range.** $3 \times 10^{38}$ is finite in bfloat16 and overflows in binary16, whose largest value is $65504$. This is the reason for the format: gradients and activations in training span a wide range, and binary16 needs loss scaling to keep them in range.
- **Accumulation stalls.** If each partial sum of $1 + 1 + \cdots + 1$ is rounded to bfloat16, the sum reaches $256$ and stays there: $256 + 1 = 257$ is a tie that rounds back to $256$. A sum of 1000 ones gives $256$. So hardware that multiplies bfloat16 values accumulates in binary32; the products of two bfloat16 significands (8 bits each) are exact in binary32 (24 bits).
- **Non-example: binary16.** The IEEE 754 half-precision format also has 16 bits, but with 5 exponent bits and 10 fraction bits. It has three more bits of precision and a much smaller range. The two formats are not interchangeable.
- **Non-example: truncated binary32 as storage only.** Some code stores the upper 16 bits of a binary32 value and computes in binary32. The stored values are bfloat16 values, but the arithmetic is binary32 arithmetic; the error analysis then has a storage error $u = 2^{-8}$ (or $2^{-7}$ with truncation) and a computation error $2^{-24}$.

## Related definitions

- [Floating-point arithmetic](/floating-point-arithmetic/) and the [standard model](/floating-point-model/): bfloat16 arithmetic satisfies the standard model with $u = 2^{-8}$ when it rounds correctly to nearest.
- [IEEE 754](/ieee-754/): defines binary16, binary32 and binary64, but not bfloat16.
- [Subnormal numbers](/subnormal-numbers/): many bfloat16 units flush subnormal inputs and results to zero; the formula above still decodes them.
- [Block floating point](/block-floating-point/) and the microscaling formats: other low-precision formats for machine learning, which share one exponent among many values.
- [Stochastic rounding](/stochastic-rounding/): often used with bfloat16 so that long sums of small updates do not stall.
- [Fused multiply-add](/fused-multiply-add/): the bfloat16 dot-product instructions of current CPUs multiply bfloat16 pairs and add them into binary32.

## References
