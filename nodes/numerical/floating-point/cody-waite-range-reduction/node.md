---
tag: MWGGH6
kind: technique
slug: cody-waite-range-reduction
name: Cody-Waite range reduction
aliases:
- Cody-Waite reduction
- Cody-Waite argument reduction
- additive range reduction with a split constant
area: numerical/floating-point
level: advanced
summary: Reduces an argument modulo π/2 or log 2 using a split constant so the reduction is accurate.
prereqs: [floating-point-model, sterbenz-lemma, catastrophic-cancellation]
see_also: [payne-hanek-argument-reduction, correctly-rounded-functions, fused-multiply-add, double-double-arithmetic, table-maker-dilemma, veltkamp-splitting, error-free-transformations, ulp]
sources:
  - book: "William J. Cody Jr. and William Waite, Software Manual for the Elementary Functions, Prentice-Hall, 1980"
    title: William J. Cody Jr. and William Waite, Software Manual for the Elementary Functions (1980)
    locator: the argument reduction of each function, with the constant split into a short part and a correction
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 10, Evaluating Floating-Point Elementary Functions (range reduction, the Cody and Waite method and its FMA variant)
  - book: "Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition, Birkhauser, 2016"
    title: Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition (2016)
    locator: Chapter 11, Range reduction (the Cody and Waite method, its error, and the worst cases of reduction modulo π/2 in binary64)
  - url: https://www.netlib.org/fdlibm/e_rem_pio2.c
    title: Sun Microsystems, fdlibm, e_rem_pio2.c (reduction modulo π/2)
    locator: the constants pio2_1, pio2_1t, pio2_2, pio2_2t, pio2_3 and the switch to the Payne-Hanek routine for large arguments
  - url: https://www.netlib.org/fdlibm/e_exp.c
    title: Sun Microsystems, fdlibm, e_exp.c (the exponential)
    locator: the reduction x = k ln 2 + r with the constants ln2HI and ln2LO
---

Cody-Waite range reduction computes $r = x - kC$ for a constant $C$ such as $\pi/2$ or $\ln 2$ and an integer $k \approx x/C$, the first step of evaluating $\sin$, $\cos$, $\exp$ and similar functions. The constant is not a float, and $x - k\,\mathrm{fl}(C)$ suffers from [catastrophic cancellation](/catastrophic-cancellation/): the error of $\mathrm{fl}(C)$, multiplied by $k$, becomes a large relative error in the small result. Cody and Waite (1980) split $C$ into a part $C_1$ with few significant bits, so that $kC_1$ and $x - kC_1$ are exact, and one or two correction terms. The method is accurate and cheap for moderate $|x|$; for huge arguments it needs too many parts, and [Payne-Hanek reduction](/payne-hanek-argument-reduction/) takes over.

## In plain words

To compute the sine of a large number, a library first removes whole multiples of a quarter turn, since the sine repeats. What is left is a small number, and the sine of a small number is easy.

The trouble is that the quarter turn, like pi, cannot be stored exactly. Subtracting many copies of a slightly wrong quarter turn multiplies the small mistake, and when the remainder is small the mistake can swamp it. The fix is to store the constant in two or three pieces: a short first piece whose multiples can be subtracted with no error at all, then the small pieces that make up the rest. The leftover then has almost no error.

## When it applies

**Notation.** Binary64 with round to nearest, $p = 53$, $u = 2^{-53}$, $\mathrm{fl}(\cdot)$ for the rounded result, and the [standard model](/floating-point-model/); see [floating-point arithmetic](/floating-point-arithmetic/). $C$ is a positive real constant and $C_1, C_2, C_3$ are floats.

Use the technique when

- a function satisfies $f(x) = g(k, x - kC)$ for an integer $k$, such as $\exp(x) = 2^{k} \exp(x - k\ln 2)$ or $\sin(x) = \pm\sin$ or $\pm\cos$ of $x - k\pi/2$ by $k \bmod 4$;
- $|x|$ is bounded so that $|k|$ is small enough for $kC_1$ to be exact: if $C_1$ has $c$ significant bits, $kC_1$ is a float for $|k| < 2^{p - c}$;
- the reduced argument must be accurate relative to its own size, not only to $|x|$, which is the case for any function evaluated on $r$ in relative error.

**Why $x - kC_1$ is exact.** Assume $k \ne 0$ is the integer nearest to $x/C$, so $|x - kC| \le C/2$, and $C_1$ is $C$ truncated to $c$ bits, so $\tfrac34 C \le C_1 \le C$ (fdlibm's constants are of this kind). Then $kC_1$ is a float by the choice of $c$, and $x$ and $kC_1$ are within a factor of $2$ of each other (for $|k| = 1$ this uses $C_1 \le C$), so $\mathrm{fl}(x - kC_1) = x - kC_1$ by [Sterbenz's lemma](/sterbenz-lemma/).

## The template

```pseudo id=main
CW-REDUCE(x)                       ▷ C ≈ C1 + C2 + C3; requires |k| < 2^(p − c)
L1  k ← NEAREST-INTEGER(fl(x · INVC))   ▷ hole: INVC = fl(1/C), or a floor for one-sided reduction
L2  r ← fl(x − k·C1)                    ▷ exact: k·C1 is a float, then Sterbenz
L3  r ← fl(r − k·C2)                    ▷ hole: with an FMA, fma(−k, C2, r)
L4  r ← fl(r − k·C3)                    ▷ hole: omit when two parts are enough
L5  return (k, r)                       ▷ f(x) is rebuilt from k and g(r)
```

The holes are the constant and its split ($c$, the number of parts), the rounding of $k$, and the use of an FMA. $k$ does not have to be the nearest integer: any integer with $|x - kC|$ small enough to keep Sterbenz's condition works, and an error in $k$ only moves $r$ by a multiple of $C$.

**Error.** Let $\eta = |C - C_1 - C_2|$ for two parts. Lines L2 and L3 give

$$|r_{\mathrm{computed}} - (x - kC)| \le |k|\,\eta + u\,|kC_2| + u\,|x - kC_1 - kC_2|,$$

where the second term is the rounding of $kC_2$ (absent with an FMA) and the third is the final subtraction. If $C_1 = C$ rounded to $c$ bits, $|kC_2| \lesssim |k| \cdot 2^{-c} C$, and $\eta \lesssim 2^{-c-p} C$, so the absolute error is about $u\,|r| + |k|\,2^{-c-p} C$: the reduced argument has a relative error near $u$ as long as $|r|$ is not much smaller than $|k|\, 2^{-c} C$. When $r$ is tiny, because $x$ is close to a multiple of $C$, a third part $C_3$ reduces $\eta$ further. This bound is proved under round to nearest, with no underflow or overflow, for $|k| < 2^{p-c}$.

## Classic examples

Each computation was run in Python with binary64 floats and compared with $x - kC$ computed exactly in `fractions.Fraction` from $1400$-digit values of $\pi$ (Machin's formula) and $\ln 2$.

**The exponential (fdlibm `e_exp.c`).** $C = \ln 2$, $C_1 =$ `ln2HI` $= 0.6931471803691238$ (0x3fe62e42fee00000, $32$ significant bits) and $C_2 =$ `ln2LO` $= 1.9082149292705877 \times 10^{-10}$; $C_1 + C_2$ differs from $\ln 2$ by $1.2 \times 10^{-26}$. Since $|k| \le 1075$ for every finite result, $kC_1$ is always exact.

| $x$ | $k$ | exact $x - k\ln 2$ | Cody-Waite $r$ | its relative error | $\mathrm{fl}(x - k\,\mathrm{fl}(\ln 2))$ relative error |
|---|---|---|---|---|---|
| $700$ | $1010$ | $-0.07865236554476251$ | $-0.07865236554476251$ | $4.2 \times 10^{-17}$ | $-6.3 \times 10^{-13}$ |
| $300.5$ | $434$ | $-0.32587636301626427$ | $-0.32587636301626427$ | $-5.3 \times 10^{-17}$ | $4.1 \times 10^{-14}$ |
| $-745$ | $-1075$ | $0.13321910194120762$ | $0.13321910194120762$ | $-3.9 \times 10^{-17}$ | $1.1 \times 10^{-13}$ |

In each row line L2 was exact, as checked in rational arithmetic. The one-constant reduction loses about $10$ to $13$ bits.

**Sine and cosine near $\pi/2$ (fdlibm `e_rem_pio2.c`).** $C = \pi/2$, $C_1 =$ `pio2_1` $= 1.5707963267341256$ ($31$ significant bits, so $kC_1$ is exact for $|k| < 2^{22}$), $C_2 =$ `pio2_1t` $= 6.077100506506192 \times 10^{-11}$, with $|C - C_1 - C_2| \approx 3.5 \times 10^{-27}$. For $x = \mathrm{fl}(\pi/2) = 1.5707963267948966$, $k = 1$ and $x - \pi/2 = -6.123233995736766 \times 10^{-17}$.

- One constant: $\mathrm{fl}(x - \mathrm{fl}(\pi/2)) = 0$, a relative error of $100\%$. Since $\cos x = -\sin r$, a cosine computed from it would return $0$ instead of $\cos x = 6.123233995736766 \times 10^{-17}$.
- Two parts: $r = -6.12323399538461 \times 10^{-17}$, relative error $5.8 \times 10^{-11}$, because $\eta = 3.5 \times 10^{-27}$ is not small next to $|r|$.
- Three parts (`pio2_1`, `pio2_2`, `pio2_2t`, with $|C - C_1 - C_2 - C_3| \approx 10^{-37}$): $r = -6.123233995736766 \times 10^{-17}$, relative error $2.4 \times 10^{-17}$.

fdlibm uses this: it tries the short reduction and, when the result has lost too many bits to cancellation, repeats it with the next pair of constants.

**A larger argument.** For $x = 10^{6}$, $k = 636620$ and two parts give $r = -0.357564167085735$ with relative error $7 \times 10^{-17}$; the one-constant reduction has relative error $2.3 \times 10^{-10}$.

## Variations

- **With an FMA.** $r = \mathrm{fma}(-k, C_1, x)$ is exact even when $C_1 = \mathrm{fl}(C)$ has the full $p$ bits, because $x - kC_1$ is a float under the same Sterbenz-type condition and the [fused multiply-add](/fused-multiply-add/) rounds only once; then $r = \mathrm{fma}(-k, C_2, r)$. Each part then carries $p$ bits instead of $c$, so fewer parts reach the same accuracy (Muller et al., Chapter 10).
- **Result in double-word form.** Libraries aiming at [correct rounding](/correctly-rounded-functions/) keep $r$ as an unevaluated sum $r_{\mathrm{hi}} + r_{\mathrm{lo}}$ computed with [error-free transformations](/error-free-transformations/), and pass both to the polynomial.
- **Table-based reduction.** For $\exp$, $C = \ln 2 / 2^{t}$ with a table of $2^{j/2^{t}}$ for $0 \le j < 2^{t}$ makes $r$ smaller, so the polynomial is shorter; the reduction is the same.
- **Multiplicative reduction.** For $\log$, $x = 2^{k} m$ is exact, and further reduction uses a table of $1/m_i$; Cody-Waite splitting appears again in $k \ln 2$.
- **Large arguments.** For $|k| \ge 2^{p-c}$, the product $kC_1$ is no longer exact; adding parts keeps it working to about $|x| < 2^{p}$ in practice, beyond which [Payne-Hanek reduction](/payne-hanek-argument-reduction/) multiplies $x$ by the needed bits of $2/\pi$ exactly.

## Pitfalls

- **Too large an argument.** For $x = 10^{15}$, $k = 636619772367581 > 2^{22}$, line L2 is no longer exact, and the two-part result $0.4766$ is wrong in the first digit (the exact reduced argument is $0.5389$). The method must test $|x|$ and switch to another reduction.
- **Arguments very close to a multiple of $C$.** The closest binary64 number to a multiple of $\pi/2$, $x = 6381956970095103 \cdot 2^{797}$, has $x \bmod \pi/2 \approx 4.69 \times 10^{-19} \approx 2^{-60.9}$ (Muller, Elementary Functions, Chapter 11). Any reduction must provide about $61$ bits more than the result needs, which is why reduction is part of the [table maker's dilemma](/table-maker-dilemma/) of trigonometric functions.
- **A constant split with too many bits.** If $C_1$ has more than $p - \lceil \log_2 (k_{\max} + 1) \rceil$ significant bits, $kC_1$ rounds for some $k$, and line L2 silently loses accuracy.
- **Compiler rewriting.** Contracting $r - kC_2$ into an FMA is harmless and even helps, but reassociating $(x - kC_1) - kC_2$ into $x - k(C_1 + C_2)$ destroys the method.
- **The wrong $k$ near ties.** If $\mathrm{fl}(x \cdot \mathrm{fl}(1/C))$ rounds to the other side of a half-integer, $k$ is off by one and $|r|$ is up to about $C/2 + \varepsilon$; the polynomial must cover the slightly wider interval.

## Exercises

1. Show that if $C_1$ has $c$ significant bits and $|k| < 2^{p - c}$, the product $kC_1$ is a binary64 float.
2. Prove that $\mathrm{fl}(x - kC_1) = x - kC_1$ when $k \ge 1$, $|x - kC| \le C/2$ and $\tfrac34 C \le C_1 \le C$, using Sterbenz's lemma.
3. For $C = \ln 2$ in binary32 ($p = 24$), choose $C_1$ so that line L2 is exact for every $x$ whose $\exp$ is finite, and compute $C_2$.
4. Reproduce the three rows of the $\pi/2$ example, then find a binary64 $x$ in $[1, 10^{5}]$ for which two parts lose more than $20$ bits of relative accuracy.

## References
