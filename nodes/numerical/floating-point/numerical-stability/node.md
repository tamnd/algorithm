---
tag: HBBQX8
kind: concept
slug: numerical-stability
name: Numerical stability
aliases:
- stability
- backward stability
- forward stability
area: numerical/floating-point
level: core
summary: An algorithm is numerically stable when its rounding errors do no more harm than a small change of the data would, so its error is no larger than the conditioning of the problem forces.
prereqs: [floating-point-model, condition-number, backward-error-analysis]
see_also: [rounding-error-analysis, forward-error-analysis, catastrophic-cancellation, relative-error, floating-point-summation, kahan-summation, log-sum-exp-trick, pairwise-summation]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 1, Principles of Finite Precision Computation (Section 1.5 backward and forward errors, Section 1.6 conditioning, Section 1.7 cancellation, Section 1.8 solving a quadratic equation, Section 1.9 computing the sample variance, Section 1.12 on instability without cancellation); Chapter 9 (Gaussian elimination and pivoting)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 14, Stability (the definitions of stable and backward stable algorithms); Lecture 15, More on Stability (accuracy of a backward stable algorithm)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.4, Cancellation (the quadratic formula and the rewriting of formulas to avoid cancellation)
  - paper: "Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance: analysis and recommendations, The American Statistician 37(3) (1983), 242-247"
    title: Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance
    locator: the error bounds of the textbook one-pass formula, the two-pass formula and the updating formulas
---

Numerical stability is the property of an algorithm that its rounding errors in [floating-point arithmetic](/floating-point-arithmetic/) do about as much harm as a small change of the input data would do, and no more. A stable algorithm gives an answer whose error is bounded by the [condition number](/condition-number/) of the problem times a modest multiple of the unit roundoff $u$. An unstable algorithm can give a wrong answer to a well-conditioned problem, often because of a [cancellation](/catastrophic-cancellation/) or of a recurrence that magnifies errors.

## In plain words

Every computer answer has small rounding errors. Some problems are sensitive: a tiny change of the input changes the answer a lot, and no method can do better than the input allows. That is a property of the problem. Stability is a property of the method. A stable method gets an answer that is as good as the problem allows. An unstable method throws accuracy away on the way, even on easy problems.

The usual test is to ask whether the computed answer is the exact answer for an input that is only a little different from the real one. If it is, the method is stable, and the rest of the error is the fault of the problem.

## The idea

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ with round to nearest), and the [standard model](/floating-point-model/) is $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$, $|\delta| \le u$, without underflow or overflow. $\gamma_n = nu/(1 - nu)$.

An algorithm computes $\hat y$ as an approximation of $y = f(x)$. There are three standard definitions, in order of strength (Higham, Section 1.5):

- **Backward stable.** $\hat y = f(x + \Delta x)$ for some $\Delta x$ with $|\Delta x| \le c\,u\,|x|$, where $c$ is a modest constant, possibly a low-degree polynomial in the size $n$ of the problem. The bound can be componentwise (as written) or normwise, $\|\Delta x\| \le c\,u\,\|x\|$.
- **Mixed forward-backward stable** (often just *numerically stable*). $\hat y + \Delta y = f(x + \Delta x)$ with $|\Delta y| \le c_1 u |\hat y|$ and $|\Delta x| \le c_2 u |x|$: the answer is near the exact answer of nearby data. Trefethen and Bau call this *stable* and give it in norms.
- **Forward stable.** The forward error $|\hat y - y|/|y|$ is of the size that a backward stable algorithm would give, that is $c\,u\,\kappa(x)$, where $\kappa$ is the condition number.

**The rule of thumb (proved to first order).** If the algorithm is backward stable with backward error $\eta = c\,u$ and the relative condition number of $f$ at $x$ is $\kappa(x)$, then

$$\frac{|\hat y - y|}{|y|} \lesssim \kappa(x)\,\eta,$$

where $\lesssim$ hides terms of second order in $\eta$. This follows from $f(x + \Delta x) - f(x) = f'(x)\Delta x + O(\Delta x^2)$ and $\kappa(x) = |x f'(x)/f(x)|$ for a scalar $f$. So stability is a property of the algorithm, conditioning is a property of the problem, and the error is about their product.

**How instability enters.** Most unstable algorithms do one of these:

1. They subtract two computed numbers that are close, so that the earlier rounding errors become the leading digits of the difference ([catastrophic cancellation](/catastrophic-cancellation/)).
2. They form an intermediate quantity much larger than the final result, such as $\sum x_i^2$ for a small variance, or an unpivoted elimination step with a tiny pivot.
3. They run a recurrence whose error is multiplied by a factor larger than 1 at each step.
4. They overflow or underflow in an intermediate result while the final result is in range (see the [log-sum-exp trick](/log-sum-exp-trick/)).

A stable algorithm avoids these steps by rewriting the formula, by reordering, by pivoting, or by computing a correction term such as in [Kahan summation](/kahan-summation/).

## Examples

All results are in binary64 and are compared with exact values from `fractions.Fraction`.

**The sample variance.** For the data $10^8 + 4$, $10^8 + 7$, $10^8 + 13$, $10^8 + 16$, the sample variance is exactly 30. The one-pass textbook formula $\bigl(\sum x_i^2 - (\sum x_i)^2/n\bigr)/(n - 1)$ gives $29.333333333333332$: the two sums are about $4 \times 10^{16}$, so their rounding errors are of order 1, and they cancel to leave a result of order 100. With the shift $10^9$ it gives $0.0$. The two-pass formula $\sum (x_i - \bar x)^2/(n - 1)$ and Welford's updating method both give $30.0$. The problem is well conditioned with respect to the data; only the first algorithm is unstable (Chan, Golub and LeVeque, 1983).

**The quadratic formula.** For $x^2 + 10^8 x + 1 = 0$ the roots are about $-10^8$ and $-10^{-8}$ (the small one is $-1.0000000000000000\ldots \times 10^{-8}$ to 16 digits). The textbook $(-b + \sqrt{b^2 - 4ac})/(2a)$ gives $-7.450580596923828 \times 10^{-9}$ for the small root, with a relative error of 25%, because $\sqrt{b^2 - 4ac}$ is close to $b$. The stable form computes $q = -\tfrac12\bigl(b + \operatorname{sign}(b)\sqrt{b^2 - 4ac}\bigr)$, then $x_1 = q/a$ and $x_2 = c/q$; it gives $-10^{-8}$ for the small root, correct to all printed digits (Higham, Section 1.8; Goldberg, Section 1.4).

**A recurrence.** The integrals $I_n = \int_0^1 x^n e^{x-1}\,dx$ satisfy $I_n = 1 - nI_{n-1}$ with $I_0 = 1 - 1/e$, and $0 < I_n < 1/(n + 1)$. Run forward from the rounded $I_0$, the recurrence gives $I_{20} = -30.19\ldots$, which is negative and wrong in all digits: the initial error of about $u$ is multiplied by $20! \approx 2.4 \times 10^{18}$. Run backward, $I_{n-1} = (1 - I_n)/n$, from the crude start $I_{40} = 0$, it gives $I_{20} = 0.045544884075818054$, which is correct to all 17 printed digits, because each step divides the error by $n$. Here the problem is well conditioned and the forward algorithm is unstable without any cancellation of the usual kind (compare Higham, Section 1.12).

**A function near a cancellation.** For $x = 10^{-10}$, `math.log(1 + x)` returns $1.000000082690371 \times 10^{-10}$, with a relative error of $8 \times 10^{-8}$, because $1 + x$ is rounded before the logarithm. `math.log1p(x)` returns $9.999999999500001 \times 10^{-11}$, correct to the last digit. The problem $\log(1 + x)$ is well conditioned for small $x$ ($\kappa \approx 1$); the first algorithm is not stable for it.

**Gaussian elimination.** Elimination without pivoting on $\begin{pmatrix} 10^{-20} & 1 \\ 1 & 1 \end{pmatrix}$ forms the multiplier $10^{20}$ and the entry $1 - 10^{20}$, which rounds to $-10^{20}$; the computed factors are the exact factors of a matrix whose $(2,2)$ entry is 0, not 1, so the method is not backward stable. With partial pivoting the rows are exchanged, and the factorization is backward stable in the sense of Higham, Theorem 9.3, up to the growth factor, which can be $2^{n-1}$ in the worst case and is small in practice.

**Stable but inaccurate.** Recursive summation is backward stable: the computed sum is the exact sum of the $x_i(1 + \theta_{n-1})$, $|\theta_{n-1}| \le \gamma_{n-1}$ (Higham, Section 4.2). For a sum with heavy cancellation, such as $10^{16} + 1 - 10^{16}$, its forward error is still 100%, because the condition number $\sum|x_i|/|\sum x_i|$ is $2 \times 10^{16}$. A more accurate method, such as [Kahan summation](/kahan-summation/) or an exact sum, is then needed; stability alone does not give accuracy on an ill-conditioned problem.

## Where it is used

- **Design of library routines.** LAPACK, BLAS and the math libraries choose backward stable algorithms (Householder QR, LU with partial pivoting, stable recurrences, `log1p`, `expm1`, `hypot`), and document the backward error.
- **Error analysis.** A [backward error analysis](/backward-error-analysis/) proves stability; combined with the [condition number](/condition-number/) it gives the [forward error](/forward-error-analysis/). See [rounding error analysis](/rounding-error-analysis/).
- **Summation and statistics.** [Pairwise summation](/pairwise-summation/), [Kahan summation](/kahan-summation/), Welford's variance and the [log-sum-exp trick](/log-sum-exp-trick/) are stable replacements for formulas that are correct in exact arithmetic but lose accuracy in floating point.
- **Differential equations.** For ODE and PDE solvers the word has a second meaning: a method is stable when the errors from truncation do not grow with the number of time steps. The idea is the same, an error is not amplified, but the source of the error is the discretization, not rounding.

## References
