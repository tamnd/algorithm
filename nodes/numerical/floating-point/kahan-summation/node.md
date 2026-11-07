---
tag: 7H2DE0
kind: algorithm
slug: kahan-summation
name: Kahan summation
aliases:
- compensated summation
- Kahan's summation formula
area: numerical/floating-point
level: core
summary: Compensated summation that keeps a running error term, giving error independent of the number of terms.
model: floating-point-model
complexity:
  vars: {n: "the number of terms"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1965
  people: [William Kahan]
  note: Kahan published the method as a short note in Communications of the ACM in 1965; Knuth and later Goldberg gave proofs of the error bound 2u + O(nu^2) times the sum of absolute values.
prereqs: [floating-point-summation, fast-two-sum]
see_also: [neumaier-summation, pairwise-summation, two-sum, error-free-transformations, shewchuk-expansion-sum, reproducible-summation, numerical-stability, kulisch-accumulator]
sources:
  - paper: doi:10.1145/363707.363723
    title: W. Kahan, Pracniques, further remarks on reducing truncation errors, Communications of the ACM 8(1) (1965), 40
    locator: the compensated summation loop
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 4.3, Compensated Summation (the algorithm, the bound (2u + O(nu^2)) times the sum of absolute values, and the remark that the correction is exact when the running sum dominates)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Theorem 8 (Kahan summation formula) and its proof in the section on the details
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.2, Accuracy of floating point arithmetic (the exercise on Kahan's summation formula and its error bound)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.3, Computing sums (compensated summation algorithms)
---

Kahan summation adds $n$ floating-point numbers while carrying a correction term $c$ that holds the low-order part lost by the last addition; the correction is subtracted from the next term before that term is added. Its error bound is $(2u + O(nu^2))\sum|x_i|$, which is independent of $n$ to first order, against $\gamma_{n-1}\sum|x_i| \approx (n-1)u\sum|x_i|$ for a plain loop. It costs four floating-point operations per term and constant extra space.

## In plain words

When a small number is added to a big running total, its last digits fall off and are lost. Kahan summation catches what fell off. After each addition it works out, with two more subtractions, exactly how much of the new number failed to get into the total. It remembers that leftover and adds it back in with the next number.

The total is still rounded at every step, but the lost pieces are not thrown away; they ride along in the leftover until they are big enough to land in the total. So the final error stays at about one or two roundings of the total, no matter how many numbers there are.

## The problem

**Notation.** A floating-point system $\mathbb{F}$ with base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ in binary64), $\mathrm{fl}(\cdot)$ is the rounded result, and the [standard model](/floating-point-model/) is $\mathrm{fl}(a \pm b) = (a \pm b)(1 + \delta)$, $|\delta| \le u$, without overflow. $\gamma_n = nu/(1 - nu)$. For a float $x$, $e_x$ is its exponent, with $e_x = e_{\min}$ for subnormals.

**Input.** Floats $x_1, \ldots, x_n$.

**Output.** A float $\hat s$ with $|\hat s - s| \le (2u + O(nu^2))\sum_{i=1}^n |x_i|$, where $s = \sum_{i=1}^n x_i$.

## The algorithm

```pseudo id=main
KAHAN-SUM(x[1..n])
L1  s ← 0                              ▷ running sum
L2  c ← 0                              ▷ correction: minus the part last lost
L3  for i ← 1 to n do
L4      y ← fl(x[i] − c)               ▷ the term with the old loss added back
L5      t ← fl(s + y)                  ▷ the new sum, which loses the low part of y
L6      c ← fl(fl(t − s) − y)          ▷ (what got in) − (what was meant to get in)
L7      s ← t
L8  return s
```

Line L5 is an ordinary rounded addition. Line L6 is the second and third step of [Fast2Sum](/fast-two-sum/) applied to $(s, y)$: when $s$ is at least as large as $y$, $\mathrm{fl}(t - s)$ is exactly the part of $y$ that entered $t$, and $c$ is exactly $t - (s + y)$, the negated rounding error of line L5. Line L4 then puts that error back into the next term.

## Example

Take $x = (10^{16}, 1, 1, 1, 1)$. Floats near $10^{16}$ are spaced $2$ apart, the exact sum is $10^{16} + 4$, and a plain loop returns $10^{16}$, because each $10^{16} + 1$ is a tie that rounds to the even $10^{16}$.

| $i$ | $x_i$ | $y$ (L4) | $t$ (L5) | $c$ (L6) |
|---|---|---|---|---|
| 1 | $10^{16}$ | $10^{16}$ | $10^{16}$ | $0$ |
| 2 | $1$ | $1$ | $10^{16}$ | $(10^{16} - 10^{16}) - 1 = -1$ |
| 3 | $1$ | $1 - (-1) = 2$ | $10^{16} + 2$ | $(10^{16} + 2 - 10^{16}) - 2 = 0$ |
| 4 | $1$ | $1$ | $10^{16} + 4$ (tie, to even) | $2 - 1 = 1$ |
| 5 | $1$ | $0$ | $10^{16} + 4$ | $0$ |

In row 4, $t - s = (10^{16} + 4) - (10^{16} + 2) = 2$ and $c = 2 - 1 = 1$: the addition took in one unit too much, so row 5 subtracts it, $y = 1 - 1 = 0$. The result is $10^{16} + 4$, the exact sum.

Two more data sets, run in binary64 and compared with `fractions.Fraction`:

- $1$ followed by seven copies of $2^{-53}$: the loop returns $1$, Kahan summation returns `0x1.0000000000004p+0`, the correctly rounded sum.
- $10^6$ copies of $0.1$: the loop returns $100000.00000133288$, Kahan summation returns $100000.0$, the correctly rounded sum.

## Correctness

**Theorem** (Knuth, Section 4.2.2; Goldberg, Theorem 8; Higham, Section 4.3). With round to nearest in binary and no overflow,

$$\hat s = \sum_{i=1}^n x_i (1 + \mu_i) + \eta, \qquad |\mu_i| \le 2u + O(nu^2),\ |\eta| \le O(nu^2)\textstyle\sum|x_i|,$$

so $|\hat s - s| \le (2u + O(nu^2))\sum_i |x_i|$.

The proof in [proofs/correctness.md](proofs/correctness.md) is complete under one extra hypothesis, and gives an explicit constant:

**Theorem (proved here).** Assume binary arithmetic with precision $p \ge 9$ and round to nearest (any tie rule), no overflow, $nu \le 1/10$, and at every iteration either $s = 0$ or $e_s \ge e_y$ at line L5 (the running sum is not smaller in exponent than the next corrected term). Then each $c$ is exactly $t - (s + y)$, and

$$|\hat s - s| \le \bigl(2u + (n + 4)u^2\bigr)\sum_{i=1}^n |x_i|.$$

*Proof sketch.* Under the hypothesis, lines L5 and L6 are Fast2Sum, so $t - c = s + y$ exactly. The only remaining rounding is in line L4, with error $\epsilon_i(x_i - c)$, $|\epsilon_i| \le u$. Telescoping gives $\hat s - s = c_n + \sum_i \epsilon_i (x_i - c_{i-1})$, and $|c_i| \le u|s_i|$ bounds each piece. The hypothesis often holds for long sums of terms of one sign, and the tests of the implementation check it at run time; when it fails, Knuth's general proof applies.

What is proved and what is observed:

- **Proved here**: the explicit bound above, under round to nearest in binary, no overflow, $nu \le 1/10$ and the exponent hypothesis. An FMA does not change the algorithm (it has no products). Underflow does not matter, because an addition that underflows is exact.
- **Proved in the literature**: the bound $(2u + O(nu^2))\sum|x_i|$ without the exponent hypothesis (Knuth; Goldberg, Theorem 8; Higham, Section 4.3). The constant hidden in $O(nu^2)$ is not reproduced here.
- **Observed**: in the tests, the bound $(2u + (n + 4)u^2)\sum|x_i|$ also held on random data spread over 160 binades, where the exponent hypothesis often fails. For $10^5$ and $10^6$ uniform random numbers in $[0, 1)$ (seed 1), Kahan summation returned the correctly rounded sum, with errors $0.06u$ and $0.39u$ times the sum; a plain loop had errors $120u$ and $117u$.

## Complexity

Four floating-point additions or subtractions per term (lines L4, L5 and the two in L6), so $4n$ operations against $n - 1$ for a loop, and two extra floats of storage. The four operations of one iteration depend on each other and on the previous iteration, so the loop runs at about one term per four addition latencies; it does not vectorize without changing the order of the terms.

## Properties

- **Error independent of $n$ to first order.** The relative error bound is $(2u + O(nu^2))$ times the condition number $\sum|x_i|/|\sum x_i|$; for $n \ll 1/u$ the $nu^2$ term is negligible.
- **Not exact.** The result is not always the correctly rounded sum: under heavy cancellation the bound is still relative to $\sum|x_i|$, not to $|\sum x_i|$.
- **Fails when a term exceeds the sum.** For $x = (1, 10^{100}, 1, -10^{100})$ it returns $0$, while the exact sum is $2$: at the second step $s = 1$ is much smaller than $y = 10^{100}$, line L6 gives $c = 0$, and the first $1$ is lost. [Neumaier summation](/neumaier-summation/) fixes this case.
- **Sequential.** The result depends on the order of the terms; it is deterministic for a fixed order.
- **Fragile under compiler rewriting.** An optimizer that treats addition as associative simplifies $(t - s) - y$ to $0$, which turns the algorithm into a plain loop.

## Variants and improvements

- **[Neumaier summation](/neumaier-summation/)** (Kahan-Babuska). Compares $|s|$ and $|x_i|$ and computes the error of the larger first, accumulating the errors separately; it handles terms larger than the running sum.
- **Final correction.** Returning $\mathrm{fl}(s - c)$ instead of $s$ adds the last loss back; it changes the result only in rare cases.
- **TwoSum version.** Computing the error of each addition with [TwoSum](/two-sum/), which is exact whatever the order of the operands, and adding all the errors in a separate sum at the end, is the algorithm Sum2 of Ogita, Rump and Oishi (2005); its result is as accurate as if it were computed in twice the working precision and then rounded.
- **Doubly compensated summation.** Priest's variant, which also sorts the terms by decreasing magnitude, gives a relative error of about $2u$ for $n \le \beta^{p-3}$ (Higham, Section 4.3).
- **Exact summation.** [Shewchuk's expansion sum](/shewchuk-expansion-sum/), `math.fsum` and the [Kulisch accumulator](/kulisch-accumulator/) return the correctly rounded sum.
- **Inside other loops.** The same correction applies to dot products, running means, numerical integration and the accumulation of time steps in ODE solvers, which was Kahan's original motivation.

## When to use it

Use Kahan summation when a long sequential sum must be accurate to a few ulps and the terms are known to be smaller than the running sum, as in a running total of many small positive values or the accumulation of a time variable. When the terms can be larger than the sum, use Neumaier's variant; when the problem is ill conditioned or the result must be correctly rounded, use an exact method. When speed matters more than the last digits, [pairwise summation](/pairwise-summation/) costs a quarter as much and gives a $\log_2 n$ bound.

## Pitfalls

- **Fast-math compilation.** `-ffast-math`, `-fassociative-math` and similar options, or the `/fp:fast` model, can delete the correction entirely.
- **Extended precision.** If $t$ is kept in an 80-bit register but $s$ is stored to binary64, $\mathrm{fl}(t - s)$ is no longer the part of $y$ that entered $s$, and the correction is wrong ([double rounding](/double-rounding/)).
- **Large terms.** A term much larger than the running sum discards the accumulated correction, as in the example $(1, 10^{100}, 1, -10^{100})$.
- **Infinities.** Once $t = \infty$, line L6 gives $c = \infty - \infty = \mathrm{NaN}$, and the next term turns the sum into NaN: in binary64, $(1, \infty)$ sums to $\infty$ but $(1, \infty, 1)$ sums to NaN.
- **Signed zero.** The sum starts at $+0$, so a list of $-0$ values sums to $+0$, not $-0$.

## Implementations

## History

Kahan published the method in 1965 as a short note in Communications of the ACM, as a way to accumulate a sum without the systematic drift of rounding errors in long computations. Knuth gave it with an error analysis as an exercise in Volume 2 of The Art of Computer Programming, and Goldberg's 1991 survey stated and proved it as Theorem 8. Neumaier's variant of 1974 removed the requirement that the running sum dominates, and Ogita, Rump and Oishi (2005) placed it among the error-free transformations.

## References
