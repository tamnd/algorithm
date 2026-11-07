---
tag: 9EAYV8
kind: problem
slug: floating-point-division
name: Floating-point division
aliases:
- correctly rounded division
- IEEE division
- floating-point quotient
area: numerical/floating-point
level: advanced
summary: Compute the correctly rounded quotient of two floating-point numbers in hardware.
prereqs: [floating-point-arithmetic, rounding-modes, floating-point-exceptions]
see_also: [srt-division, goldschmidt-division, newton-raphson-division, fused-multiply-add, floating-point-product-error, long-division, correctly-rounded-functions, special-floating-point-values]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.4.1, Arithmetic operations (division, correctly rounded); Clause 7.2, Invalid operation (0/0 and infinity/infinity); Clause 7.3, Division by zero
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.5, Computation of residuals of division and square root with an FMA; Section 4.7, Newton-Raphson-based division with an FMA; Chapter 8, Hardware Implementation of Floating-Point Arithmetic (digit-recurrence division)
  - paper: "Stuart F. Oberman and Michael J. Flynn, Division algorithms and implementations, IEEE Transactions on Computers 46(8) (1997), 833-854"
    title: Stuart F. Oberman and Michael J. Flynn, Division algorithms and implementations (1997)
    locator: the survey of digit recurrence, functional iteration (Newton-Raphson and Goldschmidt), very high radix and table-based methods, with their latencies
  - book: "Milos D. Ercegovac and Tomas Lang, Division and Square Root, Digit-Recurrence Algorithms and Implementations, Kluwer, 1994"
    title: Milos D. Ercegovac and Tomas Lang, Division and Square Root, Digit-Recurrence Algorithms and Implementations (1994)
    locator: SRT division with redundant digit sets and quotient digit selection tables
  - paper: "Peter W. Markstein, Computation of elementary functions on the IBM RISC System/6000 processor, IBM Journal of Research and Development 34(1) (1990), 111-119"
    title: Peter W. Markstein, Computation of elementary functions on the IBM RISC System/6000 processor (1990)
    locator: correctly rounded division and square root by Newton iterations with the fused multiply-add
  - paper: "Alan Edelman, The mathematics of the Pentium division bug, SIAM Review 39(1) (1997), 54-67"
    title: Alan Edelman, The mathematics of the Pentium division bug (1997)
    locator: the missing entries of the SRT quotient digit table and the inputs that expose them
---

Floating-point division asks for the quotient $a/b$ of two floats rounded once to the format, $\circ(a/b)$, together with the special cases fixed by IEEE 754: division of a nonzero number by zero gives a signed infinity and raises the divide-by-zero flag, and $0/0$ and $\infty/\infty$ give NaN and raise invalid. Unlike multiplication, the exact quotient usually has an infinite expansion, so the hardware must compute enough of it to decide the rounding. Three families of methods do this: digit recurrences such as [SRT division](/srt-division/), which produce a few quotient bits per cycle; multiplicative iterations, [Newton-Raphson](/newton-raphson-division/) and [Goldschmidt](/goldschmidt-division/), which double the number of correct bits per step; and table-based approximations. All of them end with a rounding step that relies on an exact remainder.

## In plain words

Dividing two numbers usually gives an answer whose digits never stop, such as one third. The computer must stop somewhere and keep the stored number nearest to the true answer.

The difficulty is that it cannot see the true answer, only an approximation of it. It must compute enough digits to be sure which stored number is nearest. The usual ways are to produce the answer a few digits at a time, like long division at school, or to start from a rough guess and improve it, doubling the number of correct digits at each step. Either way, the last step checks the remainder to choose between the two closest candidates.

## Definition

**Notation.** A binary floating-point system with precision $p$ (binary64: $p = 53$), $\circ$ the rounding function of the current mode (round to nearest, ties to even, by default), $u = 2^{-p}$, and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/).

**Input.** Floats $a$ and $b$, including zeros, infinities and NaNs.

**Output.** The float $q = \circ(a/b)$ when $a$ and $b$ are finite and $b \ne 0$, with the inexact, underflow and overflow flags as for any operation; otherwise the IEEE 754 result (Clauses 5.4.1, 7.2 and 7.3):

- $a/0$ for finite $a \ne 0$: $\pm\infty$ with the sign of $a$ times the sign of the zero, flag divide-by-zero;
- $0/0$ and $\pm\infty/\pm\infty$: NaN, flag invalid;
- $a/\pm\infty$ for finite $a$: a signed zero; $\pm\infty/b$ for finite $b$: a signed infinity;
- any NaN operand: a quiet NaN.

In the [standard model](/floating-point-model/) the finite case satisfies $q = (a/b)(1 + \delta)$ with $|\delta| \le u$ when no underflow or overflow occurs.

## Variants

- **Reciprocal.** $\circ(1/b)$; computing $\circ(a \cdot \circ(1/b))$ is faster but is not a correctly rounded quotient.
- **Faithful or approximate division.** GPU intrinsics such as CUDA's `__fdividef` and compiler options for fast math return a quotient within a few ulps.
- **Remainder and fused operations.** IEEE 754's `remainder(a, b)` is exact; the exact residual $a - qb$ is the related problem of the [exact product error](/floating-point-product-error/) family.
- **Square root.** It is computed by the same hardware or the same iterations, with the residual $a - s^2$.
- **Decimal division.** [Decimal floating-point](/decimal-floating-point/) formats require the same correct rounding, plus a preferred exponent for the result.
- **Integer division.** Hardware dividers often share the datapath for integer quotients; see [integer division](/integer-division/).

## Examples

Each line was run in Python 3.14 with binary64 and checked with `fractions.Fraction`.

- $1/3 = $ 0x1.5555555555555p-2 and $1/10 = $ 0x1.999999999999ap-4; the residuals `math.fma(-q, b, a)` are $2^{-54}$ and $-2^{-54}$, exactly $a - qb$.
- $5/10 = 0.5$ exactly, with residual $0$ and no inexact flag.
- **The reciprocal shortcut is wrong.** $3 \cdot \mathrm{fl}(1/5) = 0.6000000000000001$ but $\mathrm{fl}(3/5) = 0.6$. For $100000$ random pairs in $[1, 2)$, $\mathrm{fl}(a \cdot \mathrm{fl}(1/b))$ differed from $\mathrm{fl}(a/b)$ in $27.2\%$ of cases.
- **The Pentium bug.** $4195835/3145727 = 1.333820449136241$ in binary64. The flawed Pentium (1994) returned $1.333739068902038$, wrong from the fifth significant digit, because five entries of its radix-4 SRT digit selection table were missing (Edelman, 1997).
- **Exceptions in Python.** Python raises `ZeroDivisionError` for `1.0 / 0.0` instead of returning $\infty$; IEEE behavior is available through other routes, for example `math.inf` arithmetic or NumPy.

## Known algorithms

- **Digit recurrence.** Restoring and nonrestoring division generate one quotient bit per step from the remainder recurrence $r_{j+1} = 2r_j - q_{j+1} b$. [SRT division](/srt-division/) (Sweeney, Robertson, Tocher) uses a redundant digit set, so each digit can be chosen from a few leading bits of the remainder with a small table; radix 4 gives 2 bits per step, radix 16 is often built as two overlapped radix-4 stages. Cost: about $p/k$ steps for radix $2^{k}$, each with an addition. The final remainder gives the rounding directly. Many x86 and ARM processors divide this way.
- **[Newton-Raphson iteration](/newton-raphson-division/).** Iterate $y \leftarrow y(2 - by)$ for $1/b$ from a table guess; the error squares at each step, so an 8-bit seed reaches $53$ bits in three iterations. With an FMA the exact residual $r = \mathrm{fma}(-q, b, a)$ and a final correction $q + ry$ give the correctly rounded quotient (Markstein, 1990). IA-64 and many GPUs divide this way in software.
- **[Goldschmidt division](/goldschmidt-division/).** Multiply numerator and denominator by $2 - d_i$ until the denominator approaches $1$; the same quadratic convergence as Newton's method, but the two multiplications per step are independent, so a pipelined multiplier runs them in parallel. Used in some AMD processors and the IBM System/360 Model 91.
- **Table-based and polynomial methods.** A large table and a short polynomial give a near-full-precision reciprocal in a few cycles, followed by a correction.

## Bounds

- **A quotient is never a midpoint (proved).** In binary, if $a/b$ is not a float, it is not the midpoint of two consecutive floats either. If $a/b = M \cdot 2^{e}$ with $M$ an odd integer of $p + 1$ bits, then $a = M \cdot b \cdot 2^{e}$, and the odd part of the integer significand of $a$ would be a multiple of $M > 2^{p}$, which is impossible for a $p$-bit significand. So round to nearest never meets an exact tie, and ties-to-even and ties-away give the same quotient.
- **Exact residuals (proved).** If $q = \mathrm{RN}(a/b)$ and no underflow occurs, $a - qb$ is a float (Muller et al., Section 4.5); with an FMA it is computed exactly, which is what allows the final rounding decision of iterative methods.
- **Latency.** Digit recurrence needs about $p/k$ cycles; multiplicative methods need $O(\log p)$ multiplications. On current processors a binary64 division takes several times the latency of a multiplication and is usually not fully pipelined (observed, varies by processor).

## Reductions

- **Division to multiplication.** Newton and Goldschmidt iterations reduce division to a few multiplications, an initial table lookup, and a correction step using an exact residual.
- **Correct rounding to a sign test.** Given an approximation $\tilde{q}$ within one ulp, the correctly rounded quotient is decided by the sign of the residual $a - mb$ at a midpoint $m$; this reduces rounding to an [exact product error](/floating-point-product-error/) computation.
- **To integer division.** With integer significands, $\circ(a/b)$ is $\lfloor 2^{k} M_a / M_b \rfloor$ for a suitable $k$, plus a rounding decided by the remainder; this is [long division](/long-division/) on $p$-bit integers.

## Applications

Division appears in solving linear systems (the pivots of Gaussian elimination), normalization of vectors, computing ratios and averages, Newton iterations of all kinds, and graphics (perspective division). Because it is slower than multiplication, compilers replace division by a constant with multiplication by its reciprocal only under fast-math options, since the results can differ, as in the $3/5$ example.

## References
