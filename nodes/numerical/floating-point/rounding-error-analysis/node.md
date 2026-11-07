---
tag: QZN9W9
kind: technique
slug: rounding-error-analysis
name: Rounding error analysis
aliases:
- floating-point error analysis
- roundoff error analysis
- a priori error analysis
area: numerical/floating-point
level: core
summary: Bounding the total effect of the rounding errors of an algorithm, by writing each operation as exact times (1 + δ) and collecting the factors into bounds such as γ_n = nu/(1 - nu).
prereqs: [floating-point-model, relative-error]
see_also: [backward-error-analysis, forward-error-analysis, numerical-stability, condition-number, floating-point-summation, pairwise-summation, kahan-summation, interval-arithmetic]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 3, Basics (Section 3.1 inner and outer products, Section 3.3 running error analysis, Section 3.4 notation for error analysis with Lemma 3.1 and Lemma 3.3, Section 3.5 matrix multiplication); Section 2.2 (the model with and without underflow); Chapter 4 (summation); Theorem 8.5 and Theorem 9.3 (triangular systems and LU factorization)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.1, Preliminaries (models and notation for error analysis, the refined bounds without the denominator of γ_n); Section 5.2 on computing validated error bounds
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1, Rounding Error; Section 4, Details (the proofs of the theorems on relative error)
  - paper: doi:10.1137/18M1226312
    title: Nicholas J. Higham and Theo Mary, A new approach to probabilistic rounding error analysis, SIAM Journal on Scientific Computing 41(5) (2019), A2815-A2835
    locator: the bound of order √n·u that holds with high probability when the rounding errors are independent and have mean zero
  - paper: "Claude-Pierre Jeannerod and Siegfried M. Rump, Improved error bounds for inner products in floating-point arithmetic, SIAM Journal on Matrix Analysis and Applications 34(2) (2013), 338-344"
    title: Claude-Pierre Jeannerod and Siegfried M. Rump, Improved error bounds for inner products in floating-point arithmetic
    locator: the bound nu instead of γ_n for the inner product under round to nearest
---

Rounding error analysis is the method of bounding how far the result of a [floating-point](/floating-point-arithmetic/) algorithm can be from the exact result. Each operation is written as its exact value times a factor $1 + \delta$ with $|\delta| \le u$, by the [standard model](/floating-point-model/); the analysis follows these factors through the algorithm and collects them into a bound. The bound is read as a [backward error](/backward-error-analysis/) (the computed result is exact for slightly changed data), as a [forward error](/forward-error-analysis/), or both, and with the [condition number](/condition-number/) of the problem it decides whether the algorithm is [numerically stable](/numerical-stability/).

## In plain words

A computer rounds after each step, and each rounding is tiny: a few parts in ten million billion for double precision. But a program does millions of steps, and the small errors can add up or be magnified. Rounding error analysis is the bookkeeping that tells how bad it can get.

You go through the algorithm step by step. At each step you write "the exact value, times one plus a small unknown error". At the end you collect all these small factors and bound their combined effect. The result is a guarantee such as "the computed sum is the exact sum of numbers that each differ from the inputs by at most a thousand roundings". You then decide whether that is good enough for the problem at hand.

## When it applies

- The arithmetic follows a known model. The usual one is the standard model below, which [IEEE 754](/ieee-754/) arithmetic satisfies in round to nearest when no result underflows or overflows.
- The algorithm is a fixed sequence of operations, or a loop whose operations can be counted (sums, dot products, polynomial evaluation, triangular solves, factorizations).
- You want a guarantee for all inputs (an *a priori* bound), or a bound computed with the result (a *running* or *a posteriori* bound).

It does not apply as is to code that a compiler may reorder (the `-ffast-math` options), to arithmetic with extended registers that round twice, or to results in the subnormal range, unless the model is extended for these cases.

## The template

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12\beta^{1-p}$, which is $2^{-53}$ for binary64 with round to nearest. $\mathrm{fl}(\cdot)$ is the computed result. For an integer $n$ with $nu < 1$,

$$\gamma_n = \frac{nu}{1 - nu}.$$

$\theta_k$ denotes any number with $|\theta_k| \le \gamma_k$; two occurrences of $\theta_k$ can be different numbers.

1. **Fix the model and its assumptions.** The standard model: for $x, y \in \mathbb{F}$ and $op \in \{+, -, \times, /\}$,
$$\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta), \qquad |\delta| \le u,$$
if no underflow or overflow occurs. State the rounding mode (round to nearest gives $u = 2^{-53}$; a directed mode gives $2u$ in place of $u$), whether a fused multiply-add is used (it rounds once for $xy + z$), and the order of the operations.
2. **Give each operation its own $\delta$.** Write the computed value of each intermediate quantity as an exact expression in the inputs and the $\delta_i$.
3. **Collect the factors.** A product of $k$ factors $(1 + \delta_i)^{\pm 1}$ is $1 + \theta_k$ (Lemma A below). Combine with the rules of Lemma B.
4. **Read the result.** Push each $1 + \theta_k$ onto an input to get a backward error, or subtract the exact result and bound the difference to get a forward error. Keep the bound in terms of the data, such as $\sum|x_i||y_i|$, not of the result.
5. **Combine with conditioning.** forward error $\lesssim$ condition number $\times$ backward error.
6. **Compare with practice.** The bound is a worst case. Test it on random and on adversarial data, and say which statements are proved and which are observed.

**Lemma A (Higham, Lemma 3.1).** If $|\delta_i| \le u$ and $\rho_i \in \{+1, -1\}$ for $i = 1, \ldots, n$, and $nu < 1$, then $\prod_{i=1}^{n} (1 + \delta_i)^{\rho_i} = 1 + \theta_n$ with $|\theta_n| \le \gamma_n$.

*Proof.* By induction on $n$; for $n = 0$ the product is 1. Let $P = \prod_{i<n}(1+\delta_i)^{\rho_i} = 1 + \theta$ with $|\theta| \le \gamma_{n-1}$, and $Q = P(1 + \delta_n)^{\rho_n}$. If $\rho_n = 1$, then $Q - 1 = \theta + \delta_n(1 + \theta)$, so $|Q - 1| \le \gamma_{n-1} + u(1 + \gamma_{n-1})$. Since $1 + \gamma_{n-1} = 1/(1 - (n-1)u)$, this is $\frac{(n-1)u + u}{1 - (n-1)u} = \frac{nu}{1 - (n-1)u} \le \frac{nu}{1 - nu} = \gamma_n$. If $\rho_n = -1$, then $Q - 1 = (\theta - \delta_n)/(1 + \delta_n)$, so $|Q - 1| \le (\gamma_{n-1} + u)/(1 - u)$. With $\gamma_{n-1} + u = \frac{(n-1)u + u - (n-1)u^2}{1 - (n-1)u} = \frac{nu - (n-1)u^2}{1 - (n-1)u}$ and $(1-u)(1-(n-1)u) = 1 - nu + (n-1)u^2$, the bound is $\frac{nu - (n-1)u^2}{1 - nu + (n-1)u^2} \le \frac{nu}{1 - nu}$, because $a - c \le a$ and $b + c \ge b$ for $a = nu$, $b = 1 - nu > 0$, $c = (n-1)u^2 \ge 0$, and $(a - c)/(b + c) \le a/b$. $\square$

**Lemma B (Higham, Lemma 3.3).** For $ku < 1$ and $ju < 1$ (and $(j+k)u < 1$ where $\gamma_{j+k}$ appears): (i) $(1 + \theta_k)(1 + \theta_j) = 1 + \theta_{k+j}$; (ii) $\gamma_k \le \gamma_{k+1}$ and $c\gamma_k \le \gamma_{ck}$ for an integer $c \ge 1$; (iii) $\gamma_k + u \le \gamma_{k+1}$; (iv) $\gamma_k + \gamma_j + \gamma_k\gamma_j \le \gamma_{k+j}$.

*Proof of (iv), which gives (i).* $1 + \gamma_k = 1/(1 - ku)$, so $(1 + \gamma_k)(1 + \gamma_j) = 1/((1 - ku)(1 - ju)) \le 1/(1 - (k + j)u) = 1 + \gamma_{k+j}$, because $(1 - ku)(1 - ju) = 1 - (k+j)u + kju^2 \ge 1 - (k+j)u$. Then $|(1+\theta_k)(1+\theta_j) - 1| \le \gamma_k + \gamma_j + \gamma_k\gamma_j \le \gamma_{k+j}$. (ii) holds because $\gamma_k$ is increasing in $k$ and $c \cdot ku/(1 - ku) \le cku/(1 - cku)$. (iii) is (iv) with $j = 1$, since $\gamma_1 \ge u$. $\square$

## Classic examples

### The inner product, in full

Compute $s = x^{T}y = \sum_{i=1}^{n} x_i y_i$ in the order $\hat s_1 = \mathrm{fl}(x_1y_1)$, $\hat s_i = \mathrm{fl}(\hat s_{i-1} + \mathrm{fl}(x_iy_i))$, without FMA, in round to nearest, with no underflow or overflow.

Each product has one $\delta$, and each addition one more. The term $x_1y_1$ goes through its product and all $n - 1$ additions; the term $x_iy_i$ for $i \ge 2$ goes through its product and the additions $i$ to $n$. So

$$\hat s_n = x_1y_1(1 + \theta_n) + \sum_{i=2}^{n} x_iy_i(1 + \theta_{n-i+2}).$$

Each $\theta$ has index at most $n$, so by Lemma B(ii) each $|\theta| \le \gamma_n$. This gives the two readings:

- *Backward (proved).* $\hat s_n = \sum_i x_i y_i(1 + \theta^{(i)})$ with $|\theta^{(i)}| \le \gamma_n$: the computed result is the exact inner product of $x$ and a vector $y + \Delta y$ with $|\Delta y_i| \le \gamma_n |y_i|$.
- *Forward (proved).* $|\hat s_n - s| \le \gamma_n \sum_{i=1}^{n} |x_iy_i| = \gamma_n\,|x|^{T}|y|$. The relative error is at most $\gamma_n \cdot |x|^T|y| / |x^Ty|$, where the ratio is the condition number of the inner product.

This is Higham, Section 3.1. Jeannerod and Rump (2013) proved that $\gamma_n$ can be replaced by $nu$ in round to nearest.

**What happens in practice (observed).** For random $x_i, y_i$ uniform in $[0, 1)$ in binary64 (seed 7, 20 trials for each $n$ up to 1000 and 5 for $n = 10000$), the largest relative error, in units of $u$, was 1.5 for $n = 10$, 5.7 for $n = 100$, 15.5 for $n = 1000$ and 65.6 for $n = 10000$, against $\gamma_n/u \approx n$. The growth is close to $\sqrt{n}$, as the probabilistic analysis of Higham and Mary predicts. The worst case can still happen: for the sum $1 + u + u + \cdots + u$ with $n - 1$ terms $u = 2^{-53}$, each addition rounds back to 1 (a tie, broken to even), and for $n = 1000$ the relative error is $999u/(1 + 999u)$, essentially the bound $\gamma_{n-1}$ for summation.

### Other results of the same form

| computation | proved bound (round to nearest, no underflow, no overflow) | where |
|---|---|---|
| recursive sum $\sum x_i$ | $\lvert \hat s - s \rvert \le \gamma_{n-1}\sum\lvert x_i\rvert$ | Higham, Section 4.2 |
| [pairwise summation](/pairwise-summation/) | $\lvert \hat s - s \rvert \le \gamma_{\lceil \log_2 n\rceil}\sum\lvert x_i\rvert$ | Higham, Section 4.2 |
| [Kahan summation](/kahan-summation/) | $\lvert \hat s - s \rvert \le (2u + O(nu^2))\sum\lvert x_i\rvert$ | Higham, Section 4.3 |
| product $x_1 x_2 \cdots x_n$ | $\hat p = p(1 + \theta_{n-1})$ | Lemma A |
| Horner's rule, degree $n$ | $\hat p(x) = \sum a_i(1 + \theta_{2n}) x^i$ | Higham, Section 5.1 |
| matrix product $AB$, inner dimension $n$ | $\lvert \hat C - AB \rvert \le \gamma_n \lvert A\rvert\lvert B\rvert$ | Higham, Section 3.5 |
| triangular solve $Tx = b$ | $(T + \Delta T)\hat x = b$, $\lvert\Delta T\rvert \le \gamma_n\lvert T\rvert$ | Higham, Theorem 8.5 |
| LU factorization | $\hat L\hat U = A + \Delta A$, $\lvert\Delta A\rvert \le \gamma_n\lvert\hat L\rvert\lvert\hat U\rvert$ | Higham, Theorem 9.3 |

### An exact step

Some steps have no error at all, and an analysis should use that. By the [Sterbenz lemma](/sterbenz-lemma/), $x - y$ is exact when $y/2 \le x \le 2y$. A sum whose rounded result is subnormal is exact, because both operands are integer multiples of the smallest subnormal $\beta^{e_{\min}-p+1}$, so their sum is too, and each such multiple below $\beta^{e_{\min}}$ in magnitude is a float. The [error-free transformations](/error-free-transformations/) compute the rounding error of a sum or a product exactly.

## Variations

- **Running error analysis (Higham, Section 3.3).** Compute a bound $\mu$ next to the result. For the sum, $\hat s_i = (\hat s_{i-1} + x_i)(1 + \delta_i)$ gives $|\hat s_n - s| \le u \sum_{i=2}^{n} |\hat s_i| / (1 - u)$, which uses the actual partial sums and is often much smaller than the a priori bound. The cost is one more addition and one absolute value per step.
- **Probabilistic analysis.** If the $\delta_i$ are independent with mean zero, then $|\theta_n| \le \lambda\sqrt{n}\,u + O(u^2)$ with probability at least $1 - 2\exp(-\lambda^2/2)$ (Higham and Mary, 2019). This explains the $\sqrt{n}$ growth seen above. The independence is an assumption, and it fails, for example, for the sum $1 + u + \cdots + u$.
- **Bounds without the denominator.** In round to nearest, many bounds hold with $nu$ in place of $\gamma_n$ and with no condition on $n$ besides a mild one (Jeannerod and Rump; Muller et al., Section 5.1).
- **Underflow.** With underflow, Higham's model adds an absolute term: $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta) + \eta$, with $\delta\eta = 0$ and $|\eta|$ at most half the smallest subnormal, and $\eta = 0$ for addition and subtraction.
- **Automatic analysis.** [Interval arithmetic](/interval-arithmetic/) computes a guaranteed enclosure with the result, with no analysis by hand, but the intervals can be much wider than the true error.
- **Mixed forward-backward analysis.** Show that $\hat y + \Delta y = f(x + \Delta x)$ with both perturbations small. This is the definition of numerical stability used for most algorithms; see [numerical stability](/numerical-stability/).

## Pitfalls

- **Forgetting the assumptions.** The bounds above need no underflow and no overflow, the stated order of the operations, and the stated use of FMA. A compiler that contracts $a \times b + c$ into an FMA, or that reassociates a sum, runs a different algorithm.
- **Bounding by the result instead of the data.** The sum bound is $\gamma_{n-1}\sum|x_i|$, not $\gamma_{n-1}|\sum x_i|$. With cancellation the second is false.
- **Using $\gamma_n$ when $nu \ge 1$.** Lemma A needs $nu < 1$. In binary16, $u = 2^{-11}$, so $\gamma_n$ is not defined for $n \ge 2048$, and the bound is useless long before that. This is one reason for blocked and [pairwise](/pairwise-summation/) summation in low precision.
- **Reading the worst case as typical.** The bound $\gamma_n$ is attained only on special data. It is a guarantee, not a forecast; compare it with experiments and say which is which.
- **A small backward error is not a small forward error.** An ill-conditioned problem turns a backward error of $u$ into a large forward error. The analysis of the algorithm and the conditioning of the problem are separate questions.
- **Directed rounding.** In a directed rounding mode, replace $u$ by $2u$ (that is, by $\varepsilon = \beta^{1-p}$) in each bound.

## Exercises

1. Show that the computed product $\hat p$ of $n$ floats, multiplied left to right, satisfies $\hat p = x_1 \cdots x_n (1 + \theta_{n-1})$. Then show that the relative error of the computed $\prod_{i=1}^{n} x_i / \prod_{i=1}^{n} y_i$, with each product formed left to right and one final division, is bounded by $\gamma_{2n-1}$.
2. Repeat the inner product analysis with an FMA, $\hat s_i = \mathrm{fl}(\hat s_{i-1} + x_iy_i)$ with one rounding. Show that $|\hat s_n - s| \le \gamma_n |x|^T|y|$ still holds, with $\theta$ indices one smaller for $i \ge 2$.
3. For pairwise summation of $n = 2^k$ terms, show that each term goes through exactly $k$ additions, and deduce the bound $\gamma_k \sum|x_i|$.
4. From $\hat s_i = (\hat s_{i-1} + x_i)/(1 + \delta_i)$, the second form of the standard model, prove the running error bound $|\hat s_n - s| \le u\sum_{i=2}^{n}|\hat s_i|$ for recursive summation.
5. Show that a sum of two binary64 floats whose rounded result is subnormal is exact, and give an example where a product whose result is subnormal is not exact.

## References
