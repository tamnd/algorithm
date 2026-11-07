---
tag: QGCJX6
kind: algorithm
slug: pairwise-summation
name: Pairwise summation
aliases:
- cascade summation
- recursive summation
- tree summation
area: numerical/floating-point
level: core
summary: Recursively sums halves, giving error growth logarithmic rather than linear in the number of terms.
model: floating-point-model
complexity:
  vars: {n: "the number of terms"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(log n)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1970
  people: [Peter Linz]
  note: Summation along a binary tree was analysed in the numerical literature around 1970, including by Linz; Higham's book gives the error bound with the factor ceil(log2 n).
prereqs: [floating-point-model, floating-point-summation]
see_also: [kahan-summation, neumaier-summation, rounding-error-analysis, numerical-stability, reproducible-summation, kulisch-accumulator, shewchuk-expansion-sum, condition-number]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 4.1, Summation Methods (pairwise summation and the tree of additions); Section 4.2, Error Analysis (the bound with gamma of ceil(log2 n) for pairwise summation and gamma of n - 1 for recursive summation); Lemma 3.1
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.3, Computing sums (the reordering of a summation and its effect on the error bound)
  - paper: "Peter Linz, Accurate floating-point summation, Communications of the ACM 13(6) (1970), 361-362"
    title: Peter Linz, Accurate floating-point summation
    locator: summation by pairs and its error compared with sequential summation
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.2, Accuracy of floating point arithmetic (the failure of the associative law and the error of a sum)
---

Pairwise summation adds $n$ floating-point numbers by splitting them into two halves, summing each half the same way, and adding the two results. Every term then takes part in at most $\lceil \log_2 n \rceil$ additions, so the worst-case error bound is $\gamma_{\lceil \log_2 n \rceil}\sum|x_i|$ instead of the $\gamma_{n-1}\sum|x_i|$ of a left-to-right loop, at the same cost of $n - 1$ additions. It is the default summation method of NumPy and Julia, where the leaves of the tree are blocks of terms summed by an unrolled loop.

## In plain words

When a long list of numbers is added one at a time, the running total grows large while each new number stays small, and a little of every small number is rounded away. Those losses add up along the whole list.

Pairwise summation adds the numbers in pairs, then adds the pair totals in pairs, and so on, like the rounds of a knockout tournament. At each round the two numbers being added are about the same size. Each original number goes through only a few rounds, about the number of times the list can be halved, so far fewer roundings touch it. The work is the same as the plain loop: one addition per number.

## The problem

**Notation.** A floating-point system $\mathbb{F}$ with base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$). The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ in binary64 with round to nearest), $\mathrm{fl}(\cdot)$ is the rounded result, and the [standard model](/floating-point-model/) is $\mathrm{fl}(a + b) = (a + b)(1 + \delta)$, $|\delta| \le u$, when no overflow occurs (underflow in an addition is exact, so it needs no assumption). $\gamma_h = hu/(1 - hu)$ for $hu < 1$.

**Input.** Floats $x_1, \ldots, x_n$, $n \ge 0$, and optionally a block size $b \ge 1$.

**Output.** A float $\hat s$ close to $s = \sum_{i=1}^n x_i$, with $|\hat s - s| \le \gamma_h \sum_{i=1}^n |x_i|$ where $h = \lceil \log_2 n \rceil$ for $b = 1$.

## The algorithm

```pseudo id=main
PAIRWISE-SUM(x, lo, hi, b)               ▷ sums x[lo .. hi−1]; n = hi − lo ≥ 1
L1  n ← hi − lo
L2  if n ≤ b then
L3      s ← x[lo]
L4      for i ← lo + 1 to hi − 1 do s ← fl(s + x[i])
L5      return s
L6  m ← lo + ⌊n/2⌋
L7  s1 ← PAIRWISE-SUM(x, lo, m, b)
L8  s2 ← PAIRWISE-SUM(x, m, hi, b)
L9  return fl(s1 + s2)
```

The call `PAIRWISE-SUM(x, 0, n, b)` returns the sum; an empty input returns $0$. Lines L2 to L5 are the base case, a plain loop over at most $b$ terms; with $b = 1$ they return the single term. Lines L6 to L9 split the range into halves of sizes $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$ and add the two partial sums with one rounding.

A bottom-up variant adds $x_1 + x_2$, $x_3 + x_4$, and so on, carries an odd last term up unchanged, and repeats on the list of partial sums until one value is left. It uses a work array of $\lceil n/2 \rceil$ floats instead of the recursion, and its tree also has depth $\lceil \log_2 n \rceil$.

## Example

Take $x_1 = 1$ and $x_2 = \cdots = x_8 = 2^{-53} = u$. The exact sum is $1 + 7u = 1 + 3.5 \cdot 2^{-52}$, and its correctly rounded value is $1 + 4 \cdot 2^{-52}$ = `0x1.0000000000004p+0` (a tie, broken to even), which `math.fsum` returns.

A left-to-right loop computes $1 + u$, a tie between $1$ and $1 + 2^{-52}$, which rounds to the even $1$; the same happens six more times and the result is $1$, with an error of $3.5$ ulps.

Pairwise summation with $b = 1$ builds this tree:

| level | values |
|---|---|
| 0 | $1,\ u,\ u,\ u,\ u,\ u,\ u,\ u$ |
| 1 | $\mathrm{fl}(1 + u) = 1,\ 2u,\ 2u,\ 2u$ |
| 2 | $\mathrm{fl}(1 + 2u) = 1 + 2^{-52},\ 4u$ |
| 3 | $\mathrm{fl}(1 + 2^{-52} + 2^{-51}) = 1 + 3 \cdot 2^{-52}$ |

The result is `0x1.0000000000003p+0`, with an error of half an ulp. Only the first addition lost anything, because after it every addition combined numbers of similar size.

On a larger scale, summing $10^6$ copies of the float $0.1$ gives $100000.00000133288$ with a loop and $100000.0$ with pairwise summation, which is also the correctly rounded sum.

## Correctness

**Theorem** (Higham, Section 4.2). Let $h$ be the largest number of additions on a path from a leaf to the root of the summation tree, and assume $hu < 1$ and no overflow. Then the computed sum satisfies

$$\hat s = \sum_{i=1}^n x_i (1 + \theta_i), \qquad |\theta_i| \le \gamma_h,$$

so $|\hat s - s| \le \gamma_h \sum_i |x_i|$. For PAIRWISE-SUM with $b = 1$, $h = \lceil \log_2 n \rceil$; with block size $b$, $h \le b - 1 + \lceil \log_2 \lceil n/b \rceil \rceil$.

*Proof sketch.* Each addition multiplies the exact sum of its two inputs by a factor $1 + \delta$, $|\delta| \le u$. Unrolling the tree, $x_i$ is multiplied by the product of the factors on its path to the root, at most $h$ of them, and Higham's Lemma 3.1 bounds such a product by $1 + \theta$ with $|\theta| \le \gamma_h$. The depth of the halving tree satisfies $d(1) = 0$ and $d(n) = 1 + d(\lceil n/2 \rceil)$, whose solution is $\lceil \log_2 n \rceil$. The full proof, including the bound with blocks, is in [proofs/correctness.md](proofs/correctness.md).

What is proved and what is observed:

- **Proved**: the bound above for any rounding mode that satisfies the standard model with unit roundoff $u$ (for round to nearest $u = 2^{-53}$, for directed rounding $u = 2^{-52}$), with or without FMA (no multiplication is involved), when no intermediate sum overflows. The result is the exact sum of slightly perturbed data, so the method is backward stable.
- **Observed**: for $10^5$ and $10^6$ uniform random numbers in $[0, 1)$ (seed 1), the error of pairwise summation was $0.06u$ and $0.39u$ times the sum, against $120u$ and $117u$ for the loop. With random signs of the rounding errors the error grows like $\sqrt{\log_2 n}\,u$ rather than $\log_2 n\,u$, but that is a statistical model, not a bound.

## Complexity

Exactly $n - 1$ floating-point additions for $n \ge 1$, the same as the loop, because every internal node of the tree is one addition and a tree with $n$ leaves has $n - 1$ internal nodes. The recursion is $\lceil \log_2 (n/b) \rceil + 1$ calls deep, so the extra space is $\Theta(\log n)$; the bottom-up variant uses $\Theta(n)$ extra space unless it overwrites its input. The overhead of the recursion is why practical codes use a block size between 8 and 1024.

## Properties

- **Backward stable.** The computed sum is the exact sum of the $x_i(1 + \theta_i)$ with $|\theta_i| \le \gamma_{\lceil \log_2 n \rceil}$.
- **Same cost as the loop.** $n - 1$ additions, no extra operations, unlike [Kahan summation](/kahan-summation/), which needs four operations per term.
- **Order of the result.** The tree depends only on $n$ and $b$, so for a fixed $n$ and $b$ the result is deterministic, but it differs from the loop's result, and it changes when $b$ changes.
- **Exact on exactly representable partial sums.** If every partial sum in the tree is a float, as for integers of moderate size, the result is exact.
- **Not accurate on ill-conditioned sums.** The relative error bound is $\gamma_h$ times the condition number $\sum|x_i|/|\sum x_i|$, which is unbounded under cancellation.

## Variants and improvements

- **Blocked pairwise summation.** Leaves of $b$ terms are summed with a plain or unrolled loop. NumPy uses $b = 128$ for contiguous arrays, Julia uses $b = 1024$; the bound becomes $\gamma_{b - 1 + \lceil \log_2 \lceil n/b \rceil \rceil}$.
- **Bottom-up and streaming forms.** A binary counter of partial sums, one per level, gives a one-pass pairwise sum of a stream with $O(\log n)$ memory.
- **Compensated summation.** [Kahan summation](/kahan-summation/) and [Neumaier summation](/neumaier-summation/) bring the bound down to $2u + O(nu^2)$ times $\sum|x_i|$, independent of $n$ to first order, at about four times the cost.
- **Exact methods.** [Shewchuk's expansion sum](/shewchuk-expansion-sum/), `math.fsum` and the [Kulisch accumulator](/kulisch-accumulator/) return the correctly rounded sum; [reproducible summation](/reproducible-summation/) makes the result independent of the order.
- **Sorting first.** Summing in order of increasing magnitude also helps a loop, but costs $O(n \log n)$ and does not help under cancellation (Higham, Section 4.2).

## When to use it

Use pairwise summation as the default for large sums of floats when speed matters and the data have no heavy cancellation: it costs nothing extra and the error bound grows only logarithmically. It parallelizes naturally, because the two halves are independent. Use compensated summation when the error bound must not depend on $n$, and an exact method when the sum is ill conditioned or the result must be correctly rounded.

## Pitfalls

- **The name "recursive summation".** Some authors use it for this method, but Higham uses it for the plain left-to-right loop, whose bound is $\gamma_{n-1}$; check which is meant.
- **Python's built-in `sum`.** Since Python 3.12, `sum` of floats uses compensated summation, so it is not a plain loop and not a fair baseline for comparisons.
- **Overflow depends on the tree.** For $M$ the largest float, $(M + M) + (-M - M)$ gives $\infty - \infty = \mathrm{NaN}$, while the loop gives $\infty$; the exact sum is $0$. Neither order is safe near the overflow threshold.
- **The result differs from the loop.** Comparing a pairwise result bit for bit with a sequential reference, or with a parallel run that splits differently, fails even though both are accurate.
- **Deep recursion on one side.** Splitting off one term at a time instead of halving gives a tree of depth $n - 1$, which is the loop again; the split must be balanced.

## Implementations

## History

The idea of adding numbers along a balanced tree is old, and the numerical analysis of summation methods around 1970, including Linz's 1970 note on summation by pairs, showed that it reduces the error bound from linear to logarithmic in $n$. Higham's book gives the bound $\gamma_{\lceil \log_2 n \rceil}\sum|x_i|$ and compares pairwise, recursive, insertion and compensated summation. NumPy's `sum` and Julia's `sum` both use blocked pairwise summation today.

## References
