---
tag: 311E1E
kind: problem
slug: floating-point-summation
name: Accurate floating-point summation
aliases:
- summing floating-point numbers
- floating-point summation
area: numerical/floating-point
level: core
summary: Compute the sum of a list of floats with error much smaller than naive left-to-right summation.
prereqs: [floating-point-model, condition-number, two-sum]
see_also: [kahan-summation, neumaier-summation, pairwise-summation, shewchuk-expansion-sum, kulisch-accumulator, reproducible-summation, accurate-dot-product, error-free-transformations]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation (4.1 summation methods, 4.2 error analysis, 4.3 compensated summation with Algorithms 4.2 and 4.3, 4.4 other summation methods, 4.5 statistical estimates of accuracy, 4.6 choice of method)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.3, Computing Sums More Accurately (5.3.1 reordering the operands, 5.3.2 compensated sums, 5.3.3 summation algorithms that somehow imitate a fixed-point arithmetic); Section 5.1.2, classical error bounds
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: the condition number of a sum and the algorithms Sum2 and SumK with their error bounds
  - paper: doi:10.1145/363707.363723
    title: William Kahan, Pracniques, further remarks on reducing truncation errors, Communications of the ACM 8(1) (1965), 40
    locator: the compensated summation algorithm
  - paper: "Jonathan R. Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3) (1997), 305-363"
    title: Jonathan R. Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates (1997)
    locator: nonoverlapping expansions and the exact summation that Python's math.fsum is based on
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (Theorem B and the exercise on the error of compensated summation)
  - paper: "Siegfried M. Rump, Error estimation of floating-point summation and dot product, BIT Numerical Mathematics 52(1) (2012), 201-220"
    title: Siegfried M. Rump, Error estimation of floating-point summation and dot product (2012)
    locator: the bound (n - 1)u times the sum of the absolute values for recursive summation, without a restriction on n
---

The floating-point summation problem asks for $s = \sum_{i=1}^{n} x_i$, for floating-point numbers $x_i$, with a small error. Adding left to right has an error bound that grows like $n u \sum |x_i|$, and with cancellation the relative error can be arbitrarily large. Methods range from reordering ([pairwise summation](/pairwise-summation/)), through compensated summation ([Kahan](/kahan-summation/), [Neumaier](/neumaier-summation/), Sum2), to exact methods that return the correctly rounded sum (Python's `math.fsum`, [expansions](/shewchuk-expansion-sum/), the [long accumulator](/kulisch-accumulator/)). The right choice depends on $n$, on the condition number $\sum|x_i|/|\sum x_i|$, on the speed needed and on whether the result must be reproducible.

## In plain words

Adding many numbers on a computer rounds after every addition. Each rounding is tiny, but there are many, and when a small number is added to a large running total, most of its digits are lost. When the numbers have mixed signs and cancel, the lost digits can be all that is left of the answer.

Better methods add the numbers in a smarter order, or keep track of the lost digits in a second variable and put them back. The best methods return the exact sum, rounded once at the end. They cost more time, from a little more to several times more, and the choice is a trade between speed and accuracy.

## Definition

**Notation.** Binary64 with round to nearest, $u = 2^{-53}$, $\gamma_n = nu/(1 - nu)$, and the [standard model](/floating-point-model/); see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** Floats $x_1, \ldots, x_n$.

**Output.** A float $\hat s$ that approximates $s = \sum_i x_i$ (exactly, in real arithmetic).

**Accuracy goals**, from weakest to strongest:

1. *Recursive-summation accuracy:* $|\hat s - s| \le c_n u \sum_i |x_i|$ with $c_n = O(n)$.
2. *Small constant:* $|\hat s - s| \le c\,u \sum_i |x_i|$ with $c$ independent of $n$ (for $n u \ll 1$).
3. *Doubled precision:* $|\hat s - s| \le u|s| + c_n u^2 \sum_i |x_i|$, as if computed in precision $u^2$ and rounded.
4. *Faithful:* $\hat s$ is one of the two floats around $s$.
5. *Correctly rounded:* $\hat s = \mathrm{fl}(s)$.

**Condition number.** For relative perturbations of the $x_i$, $\mathrm{cond}(s) = \sum_i |x_i| / |s|$ (a [condition number](/condition-number/) of at least $1$). A bound of the form $c\,u\sum|x_i|$ is a relative error bound of $c\,u\,\mathrm{cond}(s)$.

## Variants

- **Data properties.** Sums of nonnegative numbers ($\mathrm{cond} = 1$) are easy; sums with cancellation are the hard case.
- **Streaming.** The terms arrive one at a time and memory is $O(1)$: recursive and compensated summation qualify, sorting does not.
- **Parallel and reproducible.** The order of the terms varies with the number of threads, and the result should not: see [reproducible summation](/reproducible-summation/).
- **Dot products.** $\sum x_i y_i$ reduces to a sum of $2n$ floats by [TwoProduct](/two-product/): see [accurate dot product](/accurate-dot-product/).
- **Sums of other formats.** Low-precision terms (binary16, [bfloat16](/bfloat16/)) accumulated in a wider format, or in the same format with [stochastic rounding](/stochastic-rounding/).

## Examples

All values were computed in Python 3.14 (binary64) and compared with the exact sum, computed with `fractions.Fraction`.

**Two small cases.**

| input | exact | recursive | pairwise | Kahan | Neumaier | `math.fsum` |
|---|---|---|---|---|---|---|
| $0.1$ ten times | $1.0000000000000000555\ldots$ | $0.9999999999999999$ | $1.0$ | $1.0$ | $1.0$ | $1.0$ |
| $1, 10^{100}, 1, -10^{100}$ | $2$ | $0$ | $0$ | $0$ | $2$ | $2$ |

In the second line, the $1$ is lost when $10^{100}$ is added, and Kahan's correction $c = (t - s) - y$ is computed as $0$, because $t - s = 10^{100} - 1$ itself rounds to $10^{100}$: the correction is exact only when the running sum is at least as large as the new term. Neumaier's variant keeps the correction separately and recovers $2$. Python's built-in `sum()` returns $2$ as well: since Python 3.12 it uses Neumaier's compensated summation for floats.

**Random data, $n = 10^{5}$.** The table gives the error in units of $u\sum|x_i|$ (the scale of the classical bounds) and the relative error, for one run with a fixed seed.

| method | uniform $[0, 1)$, cond $= 1$: error / $(u\sum\lvert x_i\rvert)$ | relative error | normal $(0, 1)$, cond $\approx 206$: error / $(u\sum\lvert x_i\rvert)$ | relative error |
|---|---|---|---|---|
| recursive | $30.4$ | $3.4 \times 10^{-15}$ | $0.12$ | $2.8 \times 10^{-15}$ |
| increasing $\lvert x_i\rvert$ | $12.1$ | $1.3 \times 10^{-15}$ | $0.024$ | $5.5 \times 10^{-16}$ |
| pairwise | $0.245$ | $2.7 \times 10^{-17}$ | $0.005$ | $1.1 \times 10^{-16}$ |
| Kahan, Neumaier, `sum()`, `fsum` | $0.245$ | $2.7 \times 10^{-17}$ | $0.0014$ | $3.3 \times 10^{-17}$ |

The worst-case bound for recursive summation is $\gamma_{n-1} \approx 10^{5}$ in these units; the observed $30.4$ is far below it and of the order of $\sqrt{n} \approx 316$ times a small constant, as a probabilistic model predicts. In the last rows the result is the correctly rounded sum.

**Ill-conditioned data.** Sums of $1013$ terms of widely varying magnitude, built to cancel (relative errors, one run each):

| cond | recursive | pairwise | Kahan | Neumaier | `fsum` |
|---|---|---|---|---|---|
| $3.1 \times 10^{7}$ | $2.3 \times 10^{-9}$ | $1.1 \times 10^{-10}$ | $4.3 \times 10^{-10}$ | $2.9 \times 10^{-17}$ | $2.9 \times 10^{-17}$ |
| $7.3 \times 10^{12}$ | $3.8 \times 10^{-4}$ | $4.7 \times 10^{-5}$ | $6.3 \times 10^{-5}$ | $9.6 \times 10^{-18}$ | $9.6 \times 10^{-18}$ |
| $5.1 \times 10^{22}$ | $3.8 \times 10^{6}$ | $7.2 \times 10^{5}$ | $2.4 \times 10^{5}$ | $2.1 \times 10^{-9}$ | $7.6 \times 10^{-17}$ |

Kahan summation follows its bound $2u\,\mathrm{cond}$; Neumaier's variant is much better on these data (an observation, not a bound) but fails when the condition number exceeds $1/u$; `fsum` stays correctly rounded.

## Known algorithms

| algorithm | error bound (proved, round to nearest, no overflow) | cost | notes |
|---|---|---|---|
| recursive (left to right) | $\gamma_{n-1}\sum\lvert x_i\rvert$; also $(n - 1)u\sum\lvert x_i\rvert$ | $n - 1$ additions | Higham, Section 4.2; the second form is Rump's (2012) |
| sorted by increasing $\lvert x_i\rvert$ | same worst case, better in practice for one sign | $O(n \log n)$ | Higham, Section 4.2 |
| [pairwise](/pairwise-summation/) | $\gamma_{\lceil\log_2 n\rceil}\sum\lvert x_i\rvert$ | $n - 1$ additions | NumPy uses a blocked form |
| [Kahan](/kahan-summation/) (compensated) | $(2u + O(nu^2))\sum\lvert x_i\rvert$ | $4n$ flops | Kahan, 1965; Knuth, Section 4.2.2; Higham, Section 4.3 |
| [Neumaier](/neumaier-summation/) | $(2u + O(nu^2))\sum\lvert x_i\rvert$, and exact for more inputs | about $4n$ flops and a comparison | Python's `sum()` |
| Sum2 ([TwoSum](/two-sum/) cascade) | $u\lvert s\rvert + \gamma_{n-1}^2\sum\lvert x_i\rvert$ | $7n$ flops | Ogita, Rump and Oishi, 2005 |
| doubly compensated (Priest) | relative error $2u$ for $n \le 2^{p-3}$ | $O(n \log n)$ with sorting | Higham, Algorithm 4.3 |
| exact: [expansions](/shewchuk-expansion-sum/), `math.fsum` | correctly rounded | $O(n)$ typical, more for wide exponent ranges | Shewchuk, 1997 |
| exact: [long accumulator](/kulisch-accumulator/) | correctly rounded | $O(n)$ with a 2100-bit register for binary64 | Kulisch |

An addition whose result is subnormal is exact, so for summation the standard model holds even with underflow, and the only assumption of these bounds is that no overflow occurs. Kahan's bound has a constant $2$ independent of $n$ while $nu \le 0.1$ or so; it is not a doubled-precision bound, which is why it fails on the ill-conditioned rows above.

## Bounds

- **Lower bound.** Every exact or faithful algorithm must read every input: $\Omega(n)$. Correct rounding is achievable in $O(n)$ time with a long accumulator, so the lower bound is tight.
- **Recursive summation is tight.** The constant of $\gamma_{n-1}$ is attained up to $O(u^2)$: with $x_1 = 1$ and $x_2 = \cdots = x_n = u(1 + 2u)$ (a little more than half an ulp of $1$, for small $n$), every addition rounds up by almost $u$.
- **Order matters.** For nonnegative data, adding in increasing order minimizes a bound of the form $\sum_k |\hat s_k|$ over the partial sums; for data that cancel, decreasing order can be better (Higham, Section 4.2). No ordering gives an error independent of $n$ for all inputs.
- **Statistical behavior.** If the rounding errors are modeled as independent with mean zero, the error of recursive summation grows like $\sqrt{n}\,u$ times the size of the partial sums (Higham, Section 4.5); this is what the uniform-data row above shows.

## Reductions

- **Dot products to sums.** By [TwoProduct](/two-product/), an $n$-term dot product is exactly a $2n$-term sum.
- **Sums to [error-free transformations](/error-free-transformations/).** A cascade of TwoSum operations maps $(x_1, \ldots, x_n)$ to a vector with the same exact sum, whose last entry is the recursive sum; repeating it $K - 1$ times and summing gives SumK, with the accuracy of precision $u^K$.
- **Summation to sorting.** Exact summation algorithms that process the terms in increasing order of magnitude need a sort, $O(n \log n)$; those with a fixed-point accumulator or with bucketing by exponent do not.

## Applications

- **Statistics.** Means, [variances](/variance/) and moments of large data sets; the variance is a sum with cancellation, and accurate summation removes the need for two passes in some formulas.
- **Numerical integration and time stepping.** A long sum of small increments, such as $t \leftarrow t + h$ over $10^{9}$ steps, loses digits in recursive summation; Kahan summation was invented for such sums.
- **Linear algebra.** Every dot product, matrix product and residual is a sum; extended-precision BLAS use compensated or double-double accumulation.
- **Machine learning.** Gradients are summed over large batches in low precision; the accumulation precision and order decide the accuracy and the reproducibility of training.
- **Geometric predicates.** The sign of a sum, exactly, decides orientation and in-circle tests; adaptive exact summation makes these robust.

## References
