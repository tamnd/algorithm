---
tag: 1V3GSC
kind: technique
slug: log-sum-exp-trick
name: Log-sum-exp trick
aliases:
- log-sum-exp
- stable softmax
- logsumexp
area: numerical/floating-point
level: core
summary: Computes log of a sum of exponentials by subtracting the maximum to avoid overflow and underflow.
prereqs: [floating-point-model, special-floating-point-values, numerical-stability]
see_also: [condition-number, catastrophic-cancellation, relative-error, pairwise-summation, kahan-summation, subnormal-numbers, rounding-error-analysis]
sources:
  - paper: doi:10.1093/imanum/draa038
    title: Pierre Blanchard, Desmond J. Higham and Nicholas J. Higham, Accurately computing the log-sum-exp and softmax functions, IMA Journal of Numerical Analysis 41(4) (2021), 2311-2330
    locator: the shifted algorithm, the variant with log1p, the condition numbers of log-sum-exp and softmax, and the rounding error bounds
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.6, Conditioning; Chapter 27, Software Issues in Floating Point Arithmetic (avoiding overflow and underflow by scaling, as in the computation of norms)
  - paper: "Maxim Milakov and Natalia Gimelshein, Online normalizer calculation for softmax, arXiv:1805.02867 (2018)"
    title: Maxim Milakov and Natalia Gimelshein, Online normalizer calculation for softmax
    locator: the one-pass softmax normalizer with a running maximum
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Standard for Floating-Point Arithmetic, IEEE Std 754-2019
    locator: Clause 9.2, recommended correctly rounded functions (exp, log, logp1 and their accuracy)
---

The log-sum-exp trick computes $\mathrm{LSE}(x) = \log\sum_{i=1}^n e^{x_i}$ as $m + \log\sum_i e^{x_i - m}$ with $m = \max_i x_i$. In floating point the direct formula overflows as soon as some $x_i$ exceeds about $709.78$ in binary64, and returns $\log 0 = -\infty$ when every $x_i$ is below about $-745$; after the shift every exponential is in $(0, 1]$, the largest is exactly $1$, and the sum lies in $[1, n]$. The same shift gives the stable softmax $e^{x_i - m}/\sum_j e^{x_j - m}$.

## In plain words

Exponentials grow and shrink very fast. The exponential of 1000 is far too large for a computer number, and the exponential of minus 1000 is so small that it becomes zero. A formula that takes the log of a sum of exponentials can therefore fail even when its answer is an ordinary number like 1000.7.

The trick is to pull out the biggest value first. Subtract it from every input, so that the largest exponential becomes exactly 1 and the others are smaller. That sum is a moderate number, its log is safe, and adding the biggest value back gives the answer. The answer is mathematically the same; only the route avoids the numbers that do not fit.

## When it applies

- The quantity is a log of a sum of exponentials or a ratio of exponentials: log-likelihoods of mixtures, log partition functions, normalizing constants, softmax and cross-entropy, log-domain probabilities.
- The inputs can be large in absolute value, so that $e^{x_i}$ overflows ($x_i > \log M \approx 709.78$ for the largest binary64 number $M$) or underflows to zero or to subnormals ($x_i < -708.4$ for the smallest normal, $x_i < -745.13$ for complete underflow).
- More generally, it is one instance of scaling: replace a computation on values of extreme size by one on scaled values and an exact or well-conditioned correction, as in the computation of the 2-norm by scaling or of `hypot`.

## The template

**Notation.** A floating-point system $\mathbb{F}$ with base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64. $u = \tfrac12\beta^{1-p}$ ($2^{-53}$), $\mathrm{fl}(\cdot)$ is the rounded result, the [standard model](/floating-point-model/) $\mathrm{fl}(a \mathbin{op} b) = (a \mathbin{op} b)(1 + \delta)$, $|\delta| \le u$, holds without underflow or overflow, and $\gamma_n = nu/(1 - nu)$.

1. Compute $m = \max_i x_i$ (exact: a comparison does not round).
2. Compute $d_i = \mathrm{fl}(x_i - m) \le 0$ and $e_i = \mathrm{fl}(\exp(d_i)) \in [0, 1]$; the term with $x_k = m$ gives $d_k = 0$ and $e_k = 1$ exactly.
3. Sum: $S = \mathrm{fl}(\sum_i e_i) \in [1, n]$, possibly by [pairwise](/pairwise-summation/) or compensated summation.
4. Return $\mathrm{fl}(m + \mathrm{fl}(\log S))$. For softmax, return $e_i/S$, or $\exp(x_i - \mathrm{LSE})$.

**Why the identity holds.** $\sum_i e^{x_i} = e^m \sum_i e^{x_i - m}$, so $\log\sum_i e^{x_i} = m + \log\sum_i e^{x_i - m}$, and the same factor $e^m$ cancels in the softmax ratio. This is exact in real arithmetic for any choice of $m$; the choice $m = \max x_i$ makes $1 \le \sum e^{x_i - m} \le n$.

**What can no longer go wrong.** $\exp(d_i) \le 1$ cannot overflow. Terms with $d_i < -745$ underflow to $0$, but each contributes less than $2^{-1074}$ relative to the term $1$, far below $u$. $\log S$ is between $0$ and $\log n$. The final addition can overflow only if the result itself is out of range.

**Accuracy (first-order bound, proved below).** Assume the library `exp` and `log` return results with relative error at most $u$ (a correctly rounded or nearly correctly rounded implementation; IEEE 754-2019 Clause 9.2 recommends correct rounding but does not require it) and no underflow other than the harmless one above. To first order in $u$,

$$|\hat y - y| \lesssim u|y| + \bigl(n + n/e + \log n\bigr)u.$$

*Proof to first order.* $d_i = (x_i - m)(1 + \alpha_i)$, so $e_i = e^{x_i - m}e^{\alpha_i(x_i - m)}(1 + \beta_i) = e^{x_i - m}(1 + \zeta_i)$ with $|\zeta_i| \lesssim u(1 + |x_i - m|)$, and the sum of $n$ terms adds $\gamma_{n-1}$. With weights $w_i = e^{x_i - m}/S$, which sum to $1$, the computed sum is $S(1 + \eta)$ with $|\eta| \lesssim (n - 1)u + u + u\sum_i w_i|x_i - m|$. Since $te^{-t} \le 1/e$ for $t \ge 0$ and $S \ge 1$, $\sum_i w_i |x_i - m| \le n/e$. Then $\log(S(1 + \eta)) = \log S + \eta + O(\eta^2)$, the logarithm adds $u\log S \le u\log n$, and the final addition adds $u|y|$. $\square$

The relative error is therefore about $u + (1.4n + \log n)u/|y|$, small unless $|y|$ is small. Blanchard, Higham and Higham (2021) give rigorous bounds and show that the condition number of LSE is $\kappa(x) = \sum_i |x_i| e^{x_i - y}/|y| \le \max_i|x_i|/|y|$ (componentwise relative), so a small $|y|$ is an intrinsically sensitive case.

## Classic examples

**Overflow.** For $x = (1000, 1000)$, `math.log(sum(map(math.exp, x)))` raises `OverflowError` in Python (C returns $\infty$); the shifted form gives $1000 + \log 2 = 1000.6931471805599$.

**Underflow.** For $x = (-1000, -1000)$, the direct formula takes $\log 0$, which is $-\infty$ in C and a `ValueError` in Python; the shifted form gives $-999.3068528194401$.

**One dominant term.** For $x = (-50, -50, -50, 710)$ the direct formula overflows at $e^{710}$; the shifted form gives $710.0$, which is correct to working precision, because the other terms contribute $3e^{-760}$.

**Softmax.** For logits $(1000, 999, 990)$ the stable softmax is $(0.7310343155951328, 0.26893249549828524, 3.318890658198521 \times 10^{-5})$; the direct formula computes $\infty/\infty = \mathrm{NaN}$.

**Log-likelihood of a mixture.** $\log p(x) = \log\sum_k \pi_k p_k(x) = \mathrm{LSE}_k(\log\pi_k + \log p_k(x))$, where each $\log p_k(x)$ may be $-10^4$ for a far-away component. The forward algorithm of hidden Markov models, belief propagation and the EM algorithm all work in log space with this step.

**Cross-entropy.** $-\log\mathrm{softmax}_k(x) = \mathrm{LSE}(x) - x_k$, computed without forming the softmax, which avoids $\log 0$ when the probability underflows.

## Variations

- **`logaddexp`.** For two terms, $\log(e^a + e^b) = \max(a, b) + \mathrm{log1p}(e^{-|a - b|})$, the form used by NumPy's `logaddexp`.
- **With `log1p`.** Writing $\mathrm{LSE}(x) = m + \mathrm{log1p}\bigl(\sum_{i \ne k} e^{x_i - m}\bigr)$, with $k$ an index of the maximum, keeps the small contribution of the other terms when they are below $u$. For $x = (0, -40)$ the true value is $\log(1 + e^{-40}) = 4.248354255291589 \times 10^{-18}$; the plain shifted form returns $0.0$, and the `log1p` form returns the correct value (Blanchard, Higham and Higham).
- **Online (one pass).** Keep a running maximum $m$ and a running sum $S$ of $e^{x_i - m}$; when a new $x_j > m$ arrives, multiply $S$ by $e^{m - x_j}$ and set $m = x_j$ (Milakov and Gimelshein, 2018). This is the normalizer used in streaming softmax and in fused attention kernels.
- **Signed log-sum-exp.** For $\log|\sum_i \sigma_i e^{x_i}|$ with signs $\sigma_i$, the same shift applies, but the sum can cancel, and the result inherits the cancellation.
- **Base 2.** $\log_2\sum 2^{x_i}$ with the same shift; in binary the scaling by $2^m$ is exact when $m$ is an integer, so `ldexp` can replace the addition of $m$.
- **Other shifts.** Any $m$ that keeps the exponentials in range works; the maximum is the standard choice because it makes the largest term exactly $1$.

## Pitfalls

- **All inputs $-\infty$.** Then $m = -\infty$ and $x_i - m = -\infty - (-\infty) = \mathrm{NaN}$. The correct result is $-\infty$ (the log of an empty probability), so the case needs a test; `scipy.special.logsumexp` handles it this way.
- **An input $+\infty$.** Then $m = +\infty$ and $d_k = \mathrm{NaN}$ for that term; the result should be $+\infty$.
- **Small results.** When $|y|$ is near $0$ (all $x_i$ near $-\log n$), the absolute error of order $nu$ is a large relative error, and no shift helps, because the problem is ill conditioned there.
- **Losing small terms.** In the plain shifted form, terms below $u$ relative to the maximum vanish in $\log S$; use the `log1p` variant when $\mathrm{LSE}(x) - m$ itself is wanted.
- **Softmax by division versus by exponentiation.** $e_i/S$ and $\exp(x_i - \mathrm{LSE})$ are both stable but give slightly different results, and the second can turn a probability that should be $1$ into $1 - 2^{-53}$; sums of the output need not be exactly $1$.
- **Low precision.** In binary16 the overflow threshold of $\exp$ is about $11.09$, so the trick is necessary even for modest logits.

## Exercises

1. Show that for any real $c$, $\mathrm{LSE}(x) = c + \mathrm{LSE}(x - c)$, where $x - c$ subtracts $c$ from every entry. Find the set of $c$ for which no $e^{x_i - c}$ overflows and $\sum_i e^{x_i - c} \ge 1$ in binary64, and show that it contains $\max_i x_i$.
2. Prove that $\max_i x_i \le \mathrm{LSE}(x) \le \max_i x_i + \log n$, and that softmax is invariant under adding the same constant to all inputs.
3. Compute the gradient of LSE and show that it is the softmax vector. Use it to derive the condition number $\sum_i |x_i| \mathrm{softmax}_i(x)/|\mathrm{LSE}(x)|$.
4. Derive the online update $S' = S e^{m - m'} + e^{x_j - m'}$ for a new maximum $m'$, and show that it never overflows.
5. For $x = (0, -40)$, explain why $m + \log S$ returns exactly $0$ in binary64 while $m + \mathrm{log1p}\bigl(\sum_{i \ne k} e^{x_i - m}\bigr)$ does not, and why the argument of $\mathrm{log1p}$ must not be computed as $S - 1$.

## References
