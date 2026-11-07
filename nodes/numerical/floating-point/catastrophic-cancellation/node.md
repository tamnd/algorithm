---
tag: 2A7K3Z
kind: concept
slug: catastrophic-cancellation
name: Catastrophic cancellation
aliases:
- subtractive cancellation
- cancellation
- loss of significance
area: numerical/floating-point
level: intro
summary: Loss of significant digits when subtracting nearly equal floating-point numbers.
prereqs: [floating-point-arithmetic, relative-error]
see_also: [sterbenz-lemma, condition-number, quadratic-formula, variance, numerical-stability, floating-point-summation, log-sum-exp-trick, error-free-transformations]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.7, Cancellation (the bound on the relative error of a difference and the example (1 - cos x)/x^2); Section 1.8, Solving a Quadratic Equation; Section 1.9, Computing the Sample Variance; Section 2.5, Exact Subtraction
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the section Cancellation (catastrophic and benign cancellation, the quadratic formula and the area of a thin triangle)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.2.1, Exact addition (the Sterbenz lemma)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic
---

Catastrophic cancellation is the loss of relative accuracy that happens when two nearly equal numbers that already carry errors are subtracted: the leading digits cancel, and the difference consists mostly of the earlier errors. The subtraction itself is usually exact, by the [Sterbenz lemma](/sterbenz-lemma/); the damage comes from the inputs, and the subtraction only exposes it. The relative error of the difference is the relative error of the inputs times $(|x| + |y|)/|x - y|$, which is the [condition number](/condition-number/) of subtraction. The cure is almost always to rewrite the formula so that the subtraction of close, inexact values does not occur.

## In plain words

Suppose two measurements are 1.23456 and 1.23455, and each one may be wrong in its last digit. Their difference is 0.00001. All the digits that agreed are gone, and the one digit that is left is exactly the digit that may be wrong. So the answer can be off by one hundred percent, though each input was correct to six digits.

A computer has the same problem. The numbers it stores were already rounded, and the results of earlier steps carry small errors. When two such numbers are almost equal and you subtract them, the small errors become the main part of the result. The subtraction is not to blame: it is done without error. The fix is to change the formula so that it never subtracts two close values that are already wrong.

## The idea

**Notation.** Floats are binary64 ($\beta = 2$, $p = 53$), $\mathrm{fl}(\cdot)$ is the computed result, and $u = 2^{-53}$ is the unit roundoff (round to nearest); see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation of this sub-area.

**The bound.** Let $x$ and $y$ be exact reals with $x \ne y$, and let $\hat x = x(1 + a)$ and $\hat y = y(1 + b)$ be their computed values. Even if the subtraction $\hat x - \hat y$ is exact,

$$\frac{\lvert (\hat x - \hat y) - (x - y) \rvert}{\lvert x - y \rvert} = \frac{\lvert x a - y b \rvert}{\lvert x - y \rvert} \le \max(\lvert a \rvert, \lvert b \rvert) \, \frac{\lvert x \rvert + \lvert y \rvert}{\lvert x - y \rvert}.$$

*Proof.* $(\hat x - \hat y) - (x - y) = xa - yb$, and $|xa - yb| \le |x||a| + |y||b| \le \max(|a|, |b|)(|x| + |y|)$. Divide by $|x - y|$. $\square$

The factor $(|x| + |y|)/|x - y|$ is large exactly when $x$ and $y$ are close relative to their size. If $x$ and $y$ agree in their first $k$ significant digits, the factor is about $\beta^{k}$, and about $k$ digits of relative accuracy are lost. The bound is attained when $x$ and $y$ have the same sign and $a = -b$, so the loss is real and not an artifact of the analysis. This is Higham's analysis in Section 1.7.

**The subtraction is exact.** If $\hat x, \hat y \in \mathbb{F}$ and $\hat y/2 \le \hat x \le 2\hat y$, then $\hat x - \hat y \in \mathbb{F}$, so $\mathrm{fl}(\hat x - \hat y) = \hat x - \hat y$ (the [Sterbenz lemma](/sterbenz-lemma/); Higham, Section 2.5; Muller et al., Section 4.2.1). So the rounding of the subtraction adds nothing: all the error of the result comes from $a$ and $b$.

**Catastrophic and benign.** Goldberg (1991) calls cancellation *benign* when the operands are exact, for example two values read from input, and *catastrophic* when they carry rounding errors from earlier operations. A benign cancellation gives the exact difference of the stored values. A catastrophic one gives a result whose relative error can be anywhere up to $1$ or more.

**The cures.**

1. Rewrite the expression algebraically so that the subtraction disappears: $1 - \cos x = 2\sin^2(x/2)$, $\sqrt{x + 1} - \sqrt{x} = 1/(\sqrt{x + 1} + \sqrt{x})$.
2. Use a function that computes the small difference directly: `expm1(x)` for $e^{x} - 1$, `log1p(x)` for $\log(1 + x)$.
3. Subtract early, while the operands are still exact: compute $(x - y)(x + y)$ instead of $x^2 - y^2$ when $x$ and $y$ are inputs.
4. Compute the operands with more precision, for example with [error-free transformations](/error-free-transformations/) or [double-double arithmetic](/double-double-arithmetic/), so that $a$ and $b$ are much smaller than $u$.

## Examples

All values are binary64 results.

**The function (1 - cos x)/x².** The true value at $x = 1.2 \times 10^{-5}$ is $0.49999999999400\ldots$ (the series is $1/2 - x^2/24 + \cdots$). The direct formula computes $\cos x = 0.999999999928$, whose relative error is at most $u$, then $1 - \cos x = 7.199996154838573 \times 10^{-11}$, and the quotient is $0.4999997329749008$: only 6 correct digits. At $x = 10^{-8}$, $\mathrm{fl}(\cos x) = 1$ and the formula returns $0$. The rewritten form $2\sin^2(x/2)/x^2$ gives $0.49999999999399997$ and $0.5$, both correct to about 16 digits. This is Higham's example of Section 1.7, here in binary64.

**The quadratic formula.** For $x^2 - 10^{8} x + 1 = 0$, the small root is $1.0000000000000000 \times 10^{-8}$ to 17 digits. The textbook formula $(b - \sqrt{b^2 - 4c})/2$ with $b = 10^{8}$ gives $7.450580596923828 \times 10^{-9}$, an error of 25 percent: $\sqrt{b^2 - 4c}$ is rounded to a value close to $b$, and the subtraction exposes its rounding error. The form $2c/(b + \sqrt{b^2 - 4c})$ gives $1 \times 10^{-8}$. See the [quadratic formula](/quadratic-formula/) page.

**A difference of square roots.** At $x = 10^{15}$, $\sqrt{x+1} - \sqrt{x}$ gives $1.862645149230957 \times 10^{-8}$, and $1/(\sqrt{x+1} + \sqrt{x})$ gives $1.5811388300841893 \times 10^{-8}$, which is correct to the last digit. The first result is exactly $5 \cdot 2^{-28}$, five ulps of $\sqrt{x}$, and it holds no correct digit.

**exp(x) - 1.** At $x = 10^{-10}$, `exp(x) - 1` gives $1.000000082740371 \times 10^{-10}$ (7 correct digits) and `expm1(x)` gives $1.00000000005 \times 10^{-10}$ (all correct).

**The sample variance.** For the data $10^8 + 4$, $10^8 + 7$, $10^8 + 13$, $10^8 + 16$, the exact sample variance is $90/3 = 30$. The one-pass formula $(\sum x_i^2 - n\bar x^2)/(n-1)$ gives $29.333333333333332$, because $\sum x_i^2 \approx 4 \times 10^{16}$ is rounded with an absolute error of about $4$, and the subtraction of two such values leaves that error. The two-pass formula $\sum (x_i - \bar x)^2/(n-1)$ gives $30.0$: here each $x_i - \bar x$ is a benign cancellation of exact values. See [variance](/variance/) and Higham, Section 1.9.

**A non-example.** $1.0000001 - 1.0$ cancels 7 decimal digits, but both operands are exact floats, so the computed difference $1.0000000005838672 \times 10^{-7}$ is the exact difference of the stored values. The cancellation is benign. (It differs from $10^{-7}$ only because the decimal input $1.0000001$ was rounded when it was read.)

## Where it is used

- The analysis of [numerical stability](/numerical-stability/): an unstable algorithm is often one that cancels inexact intermediate values, and [backward error analysis](/backward-error-analysis/) locates the step.
- Stable formulas for the [quadratic formula](/quadratic-formula/), the [variance](/variance/) (two-pass or Welford updates), the area of a thin triangle (Kahan's formula, in Goldberg 1991), and the [log-sum-exp trick](/log-sum-exp-trick/).
- [Floating-point summation](/floating-point-summation/): the error bound of a sum is relative to $\sum |x_i|$, and cancellation in the sum makes $|\sum x_i|$ much smaller, so the relative error grows by the factor $\sum |x_i| / |\sum x_i|$, the condition number of the sum.
- [Compensated algorithms](/error-free-transformations/) remove cancellation damage by carrying the rounding errors along.
- The cases of [iterative refinement](/iterative-refinement/) and residual computation, where $b - A\hat x$ is a deliberate cancellation and must be computed in higher precision to be useful.

## References
