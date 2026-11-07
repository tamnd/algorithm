---
tag: C00E29
kind: algorithm
slug: neumaier-summation
name: Neumaier summation
aliases:
- Kahan-Babuska summation
- improved Kahan summation
- Kahan-Babuska-Neumaier summation
area: numerical/floating-point
level: core
summary: Kahan variant that stays accurate when an added term is larger than the running sum.
model: floating-point-model
complexity:
  vars: {n: "the number of terms"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1974
  people: [Arnold Neumaier]
  note: Neumaier published the variant with a comparison in 1974 in ZAMM; Ogita, Rump and Oishi (2005) analysed the same computation as Sum2, and CPython's built-in sum of floats has used it since version 3.12.
prereqs: [kahan-summation, fast-two-sum]
see_also: [two-sum, pairwise-summation, error-free-transformations, shewchuk-expansion-sum, reproducible-summation, kulisch-accumulator, floating-point-summation, numerical-stability]
sources:
  - paper: "A. Neumaier, Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen, Zeitschrift fur Angewandte Mathematik und Mechanik 54 (1974), 39-51"
    title: A. Neumaier, Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen
    locator: the improved compensated summation with a comparison of the operands and its error bound
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: Algorithm 4.4 (Sum2) and Proposition 4.5 (the bound u times the sum plus gamma squared times the sum of absolute values)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 4.3, Compensated Summation (the variants of Kahan's method, including the one that compares the operands)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.3, Computing sums (compensated summation with 2Sum or Fast2Sum, and the result as if computed in twice the working precision)
---

Neumaier summation adds $n$ floating-point numbers and computes the exact rounding error of every addition with [Fast2Sum](/fast-two-sum/), putting the larger operand first; the errors are added in a separate float $c$, and the result is $\mathrm{fl}(s + c)$. Unlike [Kahan summation](/kahan-summation/), it stays accurate when a term is larger than the running sum. Its error is at most $u|s| + \gamma_{n-1}^2\sum|x_i|$, so the result is about as accurate as a plain sum computed in twice the working precision and then rounded.

## In plain words

Every time two numbers are added, a little is rounded off. A short calculation can find exactly what was rounded off, as long as it knows which of the two numbers is bigger. Neumaier's method checks which one is bigger at each step, works out the lost piece, and keeps all the lost pieces in a second running total. At the end it adds the two totals.

Kahan's method always assumes the running total is the bigger one. When a huge number arrives, that guess is wrong and the saved pieces are thrown away. Checking the sizes first removes that weakness.

## The problem

**Notation.** A floating-point system $\mathbb{F}$ with base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ in binary64), $\mathrm{fl}(\cdot)$ is the rounded result, and the [standard model](/floating-point-model/) is $\mathrm{fl}(a \pm b) = (a \pm b)(1 + \delta)$, $|\delta| \le u$, without overflow. $\gamma_k = ku/(1 - ku)$.

**Input.** Floats $x_1, \ldots, x_n$.

**Output.** A float $\hat s$ with $|\hat s - s| \le u|s| + \gamma_{n-1}^2 \sum_i |x_i|$ (for $n^2 u \le 1$; see Correctness), where $s = \sum_i x_i$.

## The algorithm

```pseudo id=main
NEUMAIER-SUM(x[1..n])
L1  s ← 0                              ▷ running sum
L2  c ← 0                              ▷ sum of the exact errors
L3  for i ← 1 to n do
L4      t ← fl(s + x[i])
L5      if |s| ≥ |x[i]| then
L6          c ← fl(c + fl(fl(s − t) + x[i]))   ▷ Fast2Sum error, s first
L7      else c ← fl(c + fl(fl(x[i] − t) + s))  ▷ Fast2Sum error, x[i] first
L8      s ← t
L9  return fl(s + c)
```

Lines L5 to L7 compute $q_i = (s + x_i) - t$, the exact rounding error of line L4, by [Fast2Sum](/fast-two-sum/) with the larger operand first, which is the order under which Fast2Sum is exact. The correction is not fed back into the next term, as in Kahan's method; it is added once, at line L9.

## Example

Take $x = (1, 10^{100}, 1, -10^{100})$, whose sum is $2$.

| $i$ | $x_i$ | $t$ (L4) | branch | $q_i$ | $c$ |
|---|---|---|---|---|---|
| 1 | $1$ | $1$ | L7 | $(1 - 1) + 0 = 0$ | $0$ |
| 2 | $10^{100}$ | $10^{100}$ | L7 | $(10^{100} - 10^{100}) + 1 = 1$ | $1$ |
| 3 | $1$ | $10^{100}$ | L6 | $(10^{100} - 10^{100}) + 1 = 1$ | $2$ |
| 4 | $-10^{100}$ | $0$ | L6 | $(10^{100} - 0) - 10^{100} = 0$ | $2$ |

Line L9 returns $0 + 2 = 2$, the exact sum. A plain loop returns $0$, and so does Kahan summation: at step 2 it computes $c = (10^{100} - 1) - 10^{100} = 0$ and loses the first $1$.

On well-conditioned data the method behaves like Kahan's: $1$ followed by seven copies of $2^{-53}$ sums to `0x1.0000000000004p+0`, and $10^6$ copies of $0.1$ sum to $100000.0$, both correctly rounded.

## Correctness

**Theorem** (Neumaier, 1974; Ogita, Rump and Oishi, Proposition 4.5 for the equivalent algorithm Sum2). In binary arithmetic with round to nearest and no overflow, with $(n - 1)u < 1$, each $q_i$ is exact, $s = t_n + \sum_i q_i$ exactly, and

$$|\hat s - s| \le u|s| + (1 + u)\gamma_{n-2}\gamma_{n-1}\sum_{i=1}^n |x_i|.$$

When $n(n - 2)u \le 1$ (in binary64, $n \le 9 \times 10^7$), $(1 + u)\gamma_{n-2} \le \gamma_{n-1}$, which gives the published form $u|s| + \gamma_{n-1}^2\sum|x_i|$.

*Proof sketch.* The comparison at line L5 puts the larger operand first, so Fast2Sum is exact and $q_i = s_{i-1} + x_i - t_i$. Summing these identities gives $s = t_n + \sum q_i$. Each $|q_i| \le u|t_i|$, and the partial sums of a plain loop satisfy $|t_i| \le (1 + \gamma_{i-1})\sum_{j \le i}|x_j|$, so $\sum|q_i| \le \gamma_{n-1}\sum|x_i|$. Line L6 or L7 sums the $q_i$ by a loop, with error at most $\gamma_{n-2}\sum|q_i|$, and line L9 adds one rounding of size $u|s|$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

What is proved and what is observed:

- **Proved**: the bound above for binary arithmetic with round to nearest (any tie rule), no overflow and $(n - 1)u < 1$. No FMA is involved. Underflow is harmless: an addition whose result is subnormal is exact.
- **Observed**: in the tests, on random data that included sums of large terms cancelling exactly, with condition numbers far above $1/u$, the bound held, and $s_n$ plus the exact sum of the $q_i$ was the exact sum in every case. On $5 \times 10^4$ uniform random numbers in $[0, 1)$ (seed 1) the result was the correctly rounded sum. On recent CPython the result agreed with the built-in `sum` on every finite test case.

The bound says that the result is as accurate as if a plain loop had been run with unit roundoff $u^2$ and the result rounded to working precision: the relative error is at most $u + \gamma_{n-1}^2\kappa$, where $\kappa = \sum|x_i|/|\sum x_i|$ is the condition number. For $\kappa$ up to about $1/(nu)$ the result is accurate to about one ulp; for larger $\kappa$ the accuracy degrades, and only an exact method is safe.

## Complexity

Each term costs one addition (L4), two operations for the error (L6 or L7), one addition to $c$, and a comparison of absolute values: four floating-point operations and a branch, against four operations for Kahan's method and six for the branch-free version with [TwoSum](/two-sum/). The extra space is two floats. The accumulation of $c$ is independent of the next addition to $s$, so the critical path per term is one addition latency, shorter than the four dependent operations of Kahan's loop.

## Properties

- **Exact error terms.** Every $q_i$ is the exact rounding error of the corresponding addition, whatever the relative size of $s$ and $x_i$.
- **Twice the working precision, in effect.** The bound $u|s| + \gamma_{n-1}^2\sum|x_i|$ has the form of a plain loop's bound with $u$ replaced by $u^2$, plus a final rounding.
- **Not always correctly rounded.** For very ill-conditioned sums the second term dominates; for example, the result can be wrong when the $q_i$ themselves cancel heavily.
- **Sequential and deterministic.** For a fixed order the result is fixed; another order can give another result.
- **Same result as Sum2.** Fast2Sum with the larger operand first and TwoSum give the same pair $(t, q)$, so Neumaier's loop and Sum2 of Ogita, Rump and Oishi compute identical results.

## Variants and improvements

- **Branch-free form.** Replacing lines L5 to L7 with [TwoSum](/two-sum/) gives Sum2: six operations per term and no branch, which is faster on processors where the branch is unpredictable or when vectorizing.
- **Cascaded and K-fold summation.** Applying the same transformation again to the vector of errors gives SumK of Ogita, Rump and Oishi, whose result is as if computed with unit roundoff $u^K$ and then rounded.
- **Dot products.** Combining the summation with the exact product of [TwoProduct](/two-product/) gives Dot2, the compensated dot product (see [accurate dot product](/accurate-dot-product/)).
- **Exact and reproducible methods.** [Shewchuk's expansion sum](/shewchuk-expansion-sum/) and `math.fsum` return the correctly rounded sum for any condition number; [reproducible summation](/reproducible-summation/) makes the result independent of the order.

## When to use it

Use Neumaier summation as the default compensated sum when the data can contain terms larger than the running sum, or when the order of the terms is not controlled, as in a general-purpose `sum` function. It costs the same number of floating-point operations as Kahan's method and removes its main failure case. When the sum may be extremely ill conditioned or the result must be correctly rounded, use `math.fsum` or another exact method.

## Pitfalls

- **Infinities.** If $t$ becomes infinite, the error term is $\infty - \infty = \mathrm{NaN}$, and line L9 returns NaN even when the true result is $\pm\infty$: in the plain algorithm $(1, \infty)$ sums to NaN. CPython's `sum` checks whether the correction is finite before adding it.
- **Signed zero.** The sum starts at $+0$, so a list of $-0$ values sums to $+0$.
- **Fast-math compilation.** Algebraic simplification turns $(s - t) + x$ into $0$, which removes the correction.
- **Extended precision.** Keeping $t$ in a wider register than $s$ makes the error term inexact ([double rounding](/double-rounding/)).
- **The comparison.** It must compare absolute values; comparing $s \ge x$ gives a wrong order for negative numbers.

## Implementations

## History

Kahan's compensated summation (1965) assumed that the running sum dominates the next term. Babuška described a related compensated scheme in the late 1960s, and Neumaier published in 1974 the variant that compares the operands, together with a rounding error analysis; the method is therefore also called Kahan-Babuška summation. Ogita, Rump and Oishi (2005) studied the same computation, written with TwoSum, as Sum2, proved that it is as accurate as summation in twice the working precision, and generalized it to SumK. CPython switched its built-in `sum` of floats to this method in version 3.12.

## References
