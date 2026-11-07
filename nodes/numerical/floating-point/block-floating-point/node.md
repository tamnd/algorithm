---
tag: F3KJ3K
kind: concept
slug: block-floating-point
name: Block floating point
aliases:
- shared-exponent format
- block floating-point
- BFP
- block-floating arithmetic
area: numerical/floating-point
level: advanced
summary: A group of values shares one exponent, with individual significands, to save hardware.
prereqs: [floating-point-arithmetic, ulp]
see_also: [bfloat16, fast-fourier-transform, mixed-precision-training, stochastic-rounding, posit-format, logarithmic-number-system, accurate-dot-product, floating-point-model]
sources:
  - url: https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf/
    title: Open Compute Project, OCP Microscaling Formats (MX) Specification, version 1.0, 2023
    locator: Section 5, the MX formats (blocks of 32 elements in FP8, FP6, FP4 or INT8 sharing one E8M0 power-of-two scale), and Section 5.4.1 on the E8M0 scale
  - url: https://arxiv.org/abs/2310.10537
    title: Bita Darvish Rouhani et al., Microscaling data formats for deep learning, arXiv 2310.10537 (2023)
    locator: the definition of the MX formats and the experiments on training and inference with them
  - url: https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_shared_exponent.txt
    title: Khronos Group, EXT_texture_shared_exponent, OpenGL extension specification
    locator: the RGB9_E5 format (three 9-bit significands and a 5-bit shared exponent) and its encoding procedure
  - paper: "Alan V. Oppenheim and Clifford J. Weinstein, Effects of finite register length in digital filtering and the fast Fourier transform, Proceedings of the IEEE 60(8) (1972), 957-976"
    title: Oppenheim and Weinstein, Effects of finite register length in digital filtering and the fast Fourier transform (1972)
    locator: the error analysis of the FFT computed in fixed point, floating point and block floating point
  - paper: "Urs Koster et al., Flexpoint, an adaptive numerical format for efficient training of deep neural networks, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Koster et al., Flexpoint, an adaptive numerical format for efficient training of deep neural networks (2017)
    locator: tensors of 16-bit integer significands with one shared exponent per tensor, managed across iterations
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963"
    title: J. H. Wilkinson, Rounding Errors in Algebraic Processes (1963)
    locator: Chapter 1, the discussion of block-floating vectors and their error analysis
---

Block floating point stores a block of numbers as integer significands that share one exponent: $x_i \approx m_i \cdot 2^{k}$ for $i = 1, \ldots, n$, with a single $k$ for the whole block. It sits between fixed point, where $k$ is fixed for all data, and floating point, where each number carries its own exponent. The exponent adapts to the largest element of the block, so the format keeps a wide dynamic range across blocks, while the arithmetic inside a block is integer arithmetic. It is used in fixed-point signal processors for the [FFT](/fast-fourier-transform/), in shared-exponent texture formats, and in the low-precision formats of machine learning accelerators such as Microsoft's MSFP and the OCP Microscaling (MX) formats.

## In plain words

An ordinary floating-point number carries its own scale, a small exponent that says where the decimal point goes. When many numbers are about the same size, storing that scale again and again is wasteful.

Block floating point stores the scale once for a whole group, and for each number only its digits relative to that scale. The scale is chosen so that the largest number of the group fits. This saves memory and makes the hardware simpler, because adding and multiplying numbers that share a scale is just integer arithmetic. The price is that small numbers in a group with a large one keep only a few digits, or become zero.

## The idea

**Notation.** Binary arithmetic. A block is $n$ reals $x_1, \ldots, x_n$; it is stored as one integer $k$ (the shared exponent) and $n$ signed integers $m_i$ of $w$ bits each, $|m_i| \le M = 2^{w-1} - 1$; the stored values are $\hat{x}_i = m_i \cdot 2^{k}$. See [floating-point arithmetic](/floating-point-arithmetic/) for the notation of ordinary formats ($p$, $u$, $\mathrm{fl}$).

**Encoding.** Choose $k$ as the smallest integer with $\max_i |x_i| \le M \cdot 2^{k}$, and set $m_i = \mathrm{round}(x_i / 2^{k})$, rounding to nearest. Then every $|m_i| \le M$ (rounding cannot push a value above the integer $M$).

**Error bound (proved).** With $X = \max_i |x_i| > 0$ and $k$ chosen as above, for every $i$,

$$|x_i - \hat{x}_i| \le 2^{k-1} < \frac{X}{M}.$$

*Proof.* Rounding to an integer gives $|x_i/2^{k} - m_i| \le \tfrac12$. By minimality of $k$, $X > M \cdot 2^{k-1}$, so $2^{k-1} < X/M$. $\blacksquare$

This assumes exact division by $2^{k}$ (true when the inputs are binary floats and nothing underflows) and that $k$ fits in its own field. The bound is an *absolute* error relative to the largest element: the relative error of $x_i$ is about $(X/|x_i|) \cdot 2^{-(w-1)}$, which is small for the largest elements and grows as an element gets smaller, until an element below $2^{k-1}$ becomes $0$. An ordinary floating-point format with $p$ significant bits instead guarantees relative error $u = 2^{-p}$ for every normal element.

**Arithmetic inside a block.** If two blocks have exponents $k_a$ and $k_b$, their dot product is

$$\sum_i \hat{a}_i \hat{b}_i = 2^{k_a + k_b} \sum_i m_{a,i}\, m_{b,i},$$

an integer dot product followed by one scaling. With an integer accumulator of $2w + \lceil \log_2 n\rceil$ bits it is exact, so all the error comes from the encoding. This is why matrix units built on block formats are small: they are arrays of integer multipliers and adders. Addition of two blocks needs a common exponent: the block with the smaller exponent is shifted right, losing low bits.

**Choosing the block.** A small block adapts to local scale and loses less to small elements, but spends more on exponents: with $n$ elements of $w$ bits and an $e$-bit exponent, the cost is $w + e/n$ bits per element. MX formats use $n = 32$ and an 8-bit power-of-two scale, so MXFP4 costs $4 + 8/32 = 4.25$ bits per element.

**Variants.**

- *Integer elements* (the classical form; MXINT8, Flexpoint, MSFP): the elements are fixed-point fractions or integers.
- *Small floating-point elements* (MXFP8, MXFP6, MXFP4): each element has its own small exponent, for example E2M1 (2 exponent bits, 1 fraction bit) in MXFP4, and the shared scale $2^{k}$ multiplies them; this is a two-level scale.
- *Dynamic block floating point* in signal processing: the shared exponent of a whole array is updated after each stage of an algorithm, for example after each stage of an FFT the array is shifted right by one bit if any element might overflow at the next stage.

## Examples

Each example was computed in Python with `fractions.Fraction` for the exact values.

**Encoding one block.** Take $x = (3.0, -0.4, 0.07, 0.001)$ and $w = 8$, so $M = 127$. The smallest $k$ with $3.0 \le 127 \cdot 2^{k}$ is $k = -5$ ($3 \cdot 32 = 96$; for $k = -6$, $3 \cdot 64 = 192 > 127$). The significands are $m = (96, -13, 2, 0)$, and the stored values are $(3.0, -0.40625, 0.0625, 0)$. The relative errors are $0$, $1.6\%$, $10.7\%$ and $100\%$: the largest element is exact and the smallest is lost. All absolute errors are at most $2^{-6} \approx 0.0156$, within the bound $X/M = 3/127 \approx 0.0236$. For $20000$ random blocks of $16$ elements spread over $2^{\pm 20}$, the largest observed error relative to $X$ was $0.00784$, below $1/127 \approx 0.00787$.

**An exact integer dot product.** For $a = (0.5, -1.25, 2.0, 0.33)$ and $b = (1.0, 0.75, -0.1, 4.0)$ with $w = 8$: $k_a = -5$, $m_a = (16, -40, 64, 11)$, and $k_b = -4$, $m_b = (16, 12, -2, 64)$. The integer dot product is $352$, so the result is $352 \cdot 2^{-9} = 0.6875$, which equals the exact dot product of the stored vectors. The dot product of the original vectors is $0.6825$; the difference $0.005$ comes from encoding $0.33$ as $0.34375$ and $-0.1$ as $-0.125$.

**A shared-exponent texture.** OpenGL's RGB9_E5 stores a color as three 9-bit unsigned significands and a 5-bit shared exponent with bias $15$, in 32 bits, with values $m \cdot 2^{E - 15 - 9}$. Following the extension's encoding procedure, $(1.0, 0.5, 0.001)$ gets $E = 16$, so the scale is $2^{-8}$, the significands are $(256, 128, 0)$, and the blue component $0.001$ becomes $0$. The color $(100.0, 3.14159, 0.25)$ gets $E = 22$, scale $2^{-2}$, significands $(400, 13, 1)$, stored as $(100, 3.25, 0.25)$.

## Where it is used

- **Fixed-point signal processing.** FFTs and digital filters on fixed-point DSPs use a block exponent for the whole array, rescaled between stages, which keeps most of the dynamic range of floating point with integer hardware; Oppenheim and Weinstein (1972) compare the error of the three arithmetics for the FFT.
- **Graphics.** Shared-exponent formats such as RGB9_E5 store high-dynamic-range colors in 32 bits, with one exponent for the three channels.
- **Machine learning hardware.** Flexpoint (Intel Nervana, 2017) used one exponent per tensor; Microsoft's MSFP formats (Project Brainwave) use small blocks; the OCP Microscaling formats (2023) standardize blocks of $32$ elements in FP8, FP6, FP4 or INT8 with an 8-bit power-of-two scale, and are supported by recent accelerators. See [mixed-precision training](/mixed-precision-training/) and [bfloat16](/bfloat16/) for the per-element formats used alongside them.
- **Audio coding.** Broadcast and audio codecs transmit blocks of samples or transform coefficients with one scale factor per block.
- **Early computers.** Before floating-point hardware was common, numerical programs on fixed-point machines kept one exponent per vector or matrix in software; Wilkinson (1963) analyzes the rounding errors of such block-floating computations.

## References
