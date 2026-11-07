---
tag: 10WFYW
kind: algorithm
slug: fast-inverse-square-root
name: Fast inverse square root
aliases:
- Quake III inverse square root
- 0x5F3759DF
- fast reciprocal square root
area: numerical/floating-point
level: intro
summary: Approximates 1/√x by reinterpreting the float bits as an integer and applying a Newton step.
model: word-ram
complexity:
  vars: {s: the number of Newton steps (1 in the classic code)}
  time: {worst: Θ(s), average: Θ(s), best: Θ(s)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1999
  note: The routine is in the source code of Quake III Arena (1999), which was released in 2005. Lomont (2003) gave the first published analysis of the constant 0x5F3759DF.
prereqs: [floating-point-arithmetic, newton-raphson-method, relative-error]
see_also: [newton-square-root, newton-raphson-division, bfloat16, ulp, floating-point-model, goldschmidt-division, fused-multiply-add, logarithmic-number-system]
sources:
  - url: http://www.lomont.org/papers/2003/InvSqrt.pdf
    title: Chris Lomont, Fast inverse square root, technical report, Purdue University, 2003
    locator: the analysis of the initial approximation for 0x5F3759DF, the search for the best constant (0x5F37642F before and 0x5F375A86 after one Newton step), and the maximal relative error 0.00175 after one step
  - url: https://arxiv.org/abs/1603.04483
    title: Leonid V. Moroz, Cezary J. Walczyk, Andriy Hrynchyshyn, Vijay Holimath and Jan L. Cieslinski, Fast calculation of inverse square root with the use of magic constant, analytical approach, Applied Mathematics and Computation 316 (2018), 245-255 (arXiv 1603.04483)
    locator: the piecewise linear form of the initial approximation and the analytic computation of its extremes
  - paper: "James F. Blinn, Floating-point tricks, IEEE Computer Graphics and Applications 17(4) (1997), 80-84"
    title: James F. Blinn, Floating-point tricks
    locator: the bit pattern of a float read as an integer is an approximate scaled logarithm, and its use for square roots and reciprocals
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.8, Newton-Raphson-Based Square Root with an FMA (the iteration for the reciprocal square root and its quadratic convergence)
---

The fast inverse square root computes an approximation of $1/\sqrt{x}$ for a positive binary32 float $x$ by reading the bit pattern of $x$ as an integer $i$, forming the integer $\texttt{0x5F3759DF} - \lfloor i/2 \rfloor$, reading that pattern back as a float, and improving it with one step of [Newton's method](/newton-raphson-method/). It uses no division and no square root. The result has relative error at most about $0.00175$, which is enough for normalizing vectors in 3D graphics, where it became famous through the source code of Quake III Arena. It works because the bit pattern of a float is, up to scale and shift, a piecewise linear approximation of $\log_2 x$.

## In plain words

A float is stored as an exponent and a fraction. If you read those 32 bits as one whole number, you get roughly the logarithm of the value, scaled and shifted. Taking the inverse square root of a value means multiplying its logarithm by minus one half. So a shift to the right (to halve the number) and a subtraction from a well-chosen constant (to negate it and fix the shift) give a rough guess of the answer, using only integer steps.

The guess is within about three and a half percent of the true answer. One step of Newton's method, which uses only multiplications and one subtraction, then makes the error about twenty times smaller. The famous constant is the number that makes the guess good on average over all inputs.

## The problem

The input is a binary32 float $x$ with $2^{-125} \le x \le (2 - 2^{-23}) 2^{127}$, so that $x$ and $x/2$ are positive normal numbers. The output is a binary32 float $y$ with $y \approx 1/\sqrt{x}$; the goal is a small relative error $|y \sqrt{x} - 1|$, not a correctly rounded result.

**Notation.** $u_{32} = 2^{-24}$ is the unit roundoff of binary32 with round to nearest, and $\mathrm{fl}(\cdot)$ is a binary32 operation, correctly rounded. $\mathrm{BITS}(x)$ is the 32-bit pattern of $x$ as an unsigned integer and $\mathrm{FLOAT}(i)$ is the float with pattern $i$. The general notation of this sub-area is on the page [floating-point arithmetic](/floating-point-arithmetic/).

## The algorithm

```pseudo id=main
FAST-INV-SQRT(x)                      ▷ x a binary32 float in [2^(-125), max]
L1  x2 ← fl(0.5 · x)                   ▷ exact
L2  i ← BITS(x)                        ▷ a 32-bit integer
L3  i ← R − ⌊i / 2⌋                    ▷ R = 0x5F3759DF
L4  y ← FLOAT(i)                       ▷ the initial guess y0
L5  y ← fl(y · fl(1.5 − fl(fl(x2 · y) · y)))   ▷ one Newton step
L6  return y
```

Line L3 does the work. Write a positive normal $x = 2^{E}(1 + m)$ with $0 \le m < 1$. Its pattern is $i = 2^{23}(E + 127 + m)$, so $i/2^{23} - 127 = E + m$, and $E + m$ is a piecewise linear function that touches $\log_2 x = E + \log_2(1 + m)$ at each power of two and stays below it by at most $0.0861$. For $y = x^{-1/2}$, $\log_2 y = -\tfrac12 \log_2 x$, so the pattern of $y$ should be about $2^{23} \cdot 127 - \tfrac12(i - 2^{23} \cdot 127) = \tfrac32 \cdot 2^{23} \cdot 127 - i/2$. The value $\tfrac32 \cdot 2^{23} \cdot 127$ is $\texttt{0x5F400000}$; the constant $R = \texttt{0x5F3759DF}$ is slightly smaller, which shifts the guess to balance the errors of the linear approximation.

Line L5 is one Newton step for $f(y) = y^{-2} - x$, whose root is $x^{-1/2}$. Newton's update $y - f(y)/f'(y)$ is $y(3 - xy^2)/2 = y(1.5 - (x/2) y^2)$, which needs only multiplications. The halving in line L1 is exact for $x \ge 2^{-125}$.

## Example

The table runs the binary32 algorithm on seven inputs. The patterns are in hex; $\varepsilon_0 = y_0\sqrt{x} - 1$ and $\varepsilon_1 = y_1\sqrt{x} - 1$ are the relative errors before and after line L5.

| $x$ | $\mathrm{BITS}(x)$ | $\lfloor i/2 \rfloor$ | $R - \lfloor i/2 \rfloor$ | $y_0$ | $\varepsilon_0$ | $y_1$ | $\varepsilon_1$ |
|---|---|---|---|---|---|---|---|
| 0.15625 | 3E200000 | 1F100000 | 402759DF | 2.6148603 | 0.033614 | 2.5254862 | $-1.714 \times 10^{-3}$ |
| 1 | 3F800000 | 1FC00000 | 3F7759DF | 0.96621507 | $-0.033785$ | 0.99830717 | $-1.693 \times 10^{-3}$ |
| 2 | 40000000 | 20000000 | 3F3759DF | 0.71621507 | 0.012881 | 0.70693004 | $-2.499 \times 10^{-4}$ |
| 3.7297206 | 406EB3BE | 203759DF | 3F000000 | 0.5 | $-0.034376$ | 0.51689243 | $-1.752 \times 10^{-3}$ |
| 4 | 40800000 | 20400000 | 3EF759DF | 0.48310754 | $-0.033785$ | 0.49915358 | $-1.693 \times 10^{-3}$ |
| 100 | 42C80000 | 21640000 | 3DD359DF | 0.10319876 | 0.031988 | 0.099844880 | $-1.551 \times 10^{-3}$ |
| $10^{-30}$ | 0DA24260 | 06D12130 | 586638AF | $1.0125245 \times 10^{15}$ | 0.012525 | $9.9976370 \times 10^{14}$ | $-2.363 \times 10^{-4}$ |

The rows for $1$ and $4$ have the same $\varepsilon_0$: multiplying $x$ by $4$ adds $2^{24}$ to $i$, so the guess is exactly halved. The input $3.7297206$ (exactly $3.7297205924987793$) gives the worst initial error; its guess is exactly $0.5$. After the Newton step every error is negative.

## Correctness

The claim is: for each $x$ in the domain, the result $y$ of FAST-INV-SQRT satisfies

$$-0.0017525 \le y\sqrt{x} - 1 \le 0.0000002.$$

The proof has three steps. (1) Scaling: $\varepsilon_0(4x) = \varepsilon_0(x)$, so it is enough to study $x \in [1, 4)$. (2) On $[1, 4)$ the guess is, up to a term below $2^{-24}$, one of three linear functions of $m$, and calculus gives $-0.0343758 \le \varepsilon_0 \le 0.0339603$. (3) An exact Newton step maps $\varepsilon_0$ to $\varepsilon_1 = -\varepsilon_0^2(3 + \varepsilon_0)/2$, which lies in $[-0.0017523, 0]$, and the four binary32 roundings of line L5 add at most $3.2\,u_{32} < 2 \times 10^{-7}$. The full proof is in `proofs/correctness.md`.

The bound in step (3) is proved; the errors observed on an exhaustive run over all binary32 inputs in $[1, 4)$ are $\varepsilon_0 \in [-0.0343758, 0.0339602]$ and a largest $|\varepsilon_1|$ of $0.0017523$.

## Complexity

The algorithm does one integer shift, one integer subtraction, two reinterpretations (no work on most machines) and, per Newton step, three multiplications and one subtraction, plus one multiplication for $x/2$. So the time is $\Theta(s)$ for $s$ Newton steps, in each case, and the extra space is $\Theta(1)$. The model is the [word RAM](/word-ram/) with unit-cost word and float operations, because the algorithm uses the bit pattern of a float as an integer. Each Newton step squares the relative error, roughly: $|\varepsilon_{k+1}| \le \tfrac32 \varepsilon_k^2 (1 + |\varepsilon_k|/3)$, so two steps give about $4.6 \times 10^{-6}$ in exact arithmetic, and the binary32 rounding then limits the result to a few units of $u_{32}$.

## Properties

- **Not correctly rounded.** One step leaves a relative error up to $0.00175$, between about $15\,000$ and $29\,000$ ulps of binary32. The result is an approximation, not a replacement for `1/sqrtf(x)`.
- **Always below after a step.** In exact arithmetic $\varepsilon_1 = -\varepsilon_0^2(3 + \varepsilon_0)/2 \le 0$ for all $\varepsilon_0 > -3$, so one Newton step from any reasonable guess underestimates $1/\sqrt{x}$.
- **Scale invariance.** $y_0(4x) = y_0(x)/2$ exactly, so the error pattern repeats every two binades.
- **Branch-free.** No table and no test, so it vectorizes.

## Variants and improvements

- **Better constants.** Lomont (2003) found that $\texttt{0x5F37642F}$ minimizes the largest initial error (about $0.03421$) and $\texttt{0x5F375A86}$ minimizes the largest error after one Newton step (about $0.001751$, against $0.0017523$ for $\texttt{0x5F3759DF}$).
- **A tuned Newton step.** Replacing $1.5$ and $0.5$ by other constants, chosen together with $R$, lowers the error after one step further (Moroz et al., 2018).
- **binary64.** The same method works for binary64 with the shift of a 64-bit pattern and a 64-bit constant near $\tfrac32 \cdot 2^{52} \cdot 1023$, chosen by the same analysis (Lomont, 2003).
- **Other powers.** Replacing $-\tfrac12$ by another exponent $a$ gives a guess for $x^{a}$: the pattern of $x^{a}$ is about $(1 - a) \cdot 2^{23} \cdot 127 + a \cdot i$ (Blinn, 1997).
- **Hardware.** SSE has `rsqrtps` (relative error at most $1.5 \times 2^{-12}$) and ARM has `frsqrte`, which are faster and more accurate than the integer trick; compilers use them with a Newton step for `-ffast-math` code.

## When to use it

On current processors, use the hardware reciprocal square root estimate, or `1/sqrt(x)`, which is correctly rounded and fast. The integer trick is still useful on small processors with a fast integer unit but no fast divider or square root, in shader code where an estimate is enough, and as an example of how the format encodes a logarithm. Do not use it where an error of $0.2$ percent matters, for example in a solver whose convergence test depends on the last digits.

## Pitfalls

- **Type punning.** The original C code reads the float through a `long *` pointer, which breaks the strict aliasing rule of C and also assumes that `long` has 32 bits. Use `memcpy` or a union in C, and `struct` in Python, for lines L2 and L4.
- **The domain.** For $x \le 0$, a NaN, an infinity or a subnormal, line L3 gives a meaningless pattern; for example $x = 0$ gives the guess $1.32 \times 10^{19}$ and the result $1.98 \times 10^{19}$ instead of $+\infty$. Test the domain before line L2 if such inputs can occur.
- **The shift.** Line L3 needs a logical shift of the unsigned pattern; on a signed negative pattern an arithmetic shift is wrong, but the domain excludes it.
- **Too few or too many steps.** One step gives about 9 correct bits; the guess of line L4 alone gives fewer than 5. A second step lowers the error to about $5 \times 10^{-6}$, still far from the $6 \times 10^{-8}$ of a correctly rounded result.

## Implementations

## History

The routine appears in the source code of the game Quake III Arena by id Software (1999), published under the GPL in 2005, with the constant $\texttt{0x5F3759DF}$ and one Newton step. Blinn (1997) had already described the use of the bit pattern of a float as an approximate logarithm for square roots and reciprocals. Lomont (2003) published the first analysis of the constant and the search for better ones, and Moroz et al. (2018) gave a full analytic treatment of the initial approximation.

## References
