---
tag: TDEQSQ
kind: theorem
slug: sterbenz-lemma
name: Sterbenz lemma
aliases:
- Sterbenz's lemma
- Sterbenz theorem
- exact subtraction lemma
area: numerical/floating-point
level: core
summary: If x and y are floats with y/2 ≤ x ≤ 2y, then x - y is a float, so a correctly rounded subtraction computes it exactly.
prereqs: [floating-point-arithmetic, ulp]
see_also: [catastrophic-cancellation, fast-two-sum, two-sum, subnormal-numbers, error-free-transformations, cody-waite-range-reduction, rounding-error-analysis, floating-point-model]
sources:
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.2.1, Exact addition (Sterbenz's lemma, its proof, and the remark on subnormal numbers)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.5, Exact Subtraction (the theorem of Sterbenz, for subtraction done with a guard digit)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.3, Guard Digits, and Section 4, Details (the theorem that x - y is exact when y/2 ≤ x ≤ 2y with a guard digit)
  - paper: "Pat H. Sterbenz, Floating-Point Computation, Prentice-Hall, Englewood Cliffs, 1974"
    title: Pat H. Sterbenz, Floating-Point Computation
    locator: the theorem on the exact subtraction of two close floating-point numbers
---

The Sterbenz lemma says that the difference of two [floating-point](/floating-point-arithmetic/) numbers that are within a factor of 2 of each other is itself a floating-point number. So a correctly rounded subtraction, such as each [IEEE 754](/ieee-754/) subtraction, computes it with no error, in each rounding mode. The lemma explains why [catastrophic cancellation](/catastrophic-cancellation/) is not an error of the subtraction itself, and it is a step of the proofs of [Fast2Sum](/fast-two-sum/), [TwoSum](/two-sum/) and many argument reductions.

## Statement

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta \ge 2$, precision $p \ge 1$ and exponent range $[e_{\min}, e_{\max}]$, and it contains the subnormal numbers. The default is binary64 ($\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$). Each nonzero $x \in \mathbb{F}$ is $x = M_x \beta^{q_x}$ with an integer $M_x$, $|M_x| < \beta^{p}$, and $q_x = \max(e_x, e_{\min}) - p + 1$, where $\beta^{e_x} \le |x| < \beta^{e_x + 1}$. So $\beta^{q_x} = \mathrm{ulp}(x)$, with the [ulp](/ulp/) of Muller et al., Section 2.3.2. A number of the form $D\beta^{q}$ with integers $|D| < \beta^{p}$ and $e_{\min} - p + 1 \le q \le e_{\max} - p + 1$ is in $\mathbb{F}$.

**Theorem (Sterbenz, 1974).** Let $x, y \in \mathbb{F}$ with

$$\frac{y}{2} \le x \le 2y.$$

Then $x - y \in \mathbb{F}$. Hence $\circ(x - y) = x - y$ for each rounding function $\circ$ that returns a representable input unchanged, in particular for the five rounding modes of IEEE 754.

The condition implies that $x$ and $y$ have the same sign or are both zero, and it is symmetric: $y/2 \le x \le 2y$ holds exactly when $x/2 \le y \le 2x$.

## In plain words

When you subtract two numbers that are close, the leading digits cancel, and the answer needs fewer digits than the inputs had. The lemma says how close is close enough: if the larger number is at most twice the smaller, the answer always fits in the digits that the computer has. So the subtraction makes no rounding error at all. If the result is still inaccurate, the error was already in the inputs.

## Proof

Assume first that $x$ and $y$ are not negative. If $y = 0$ the condition gives $x = 0$, and $x - y = 0 \in \mathbb{F}$. So let $y > 0$, and then $x \ge y/2 > 0$.

*Case $y \le x$.* Then $e_y \le e_x$, so $q_y \le q_x$, and $x = M_x\beta^{q_x} = (M_x\beta^{q_x - q_y})\beta^{q_y}$ is an integer multiple of $\beta^{q_y}$. Therefore

$$x - y = D\beta^{q_y}, \qquad D = M_x\beta^{q_x - q_y} - M_y \in \mathbb{Z}.$$

From $y \le x$ we get $D \ge 0$. From $x \le 2y$ we get $x - y \le y$, so $D\beta^{q_y} \le M_y\beta^{q_y}$ and $D \le M_y < \beta^{p}$. The exponent $q_y$ satisfies $e_{\min} - p + 1 \le q_y \le e_{\max} - p + 1$, because $y \in \mathbb{F}$. So $x - y = D\beta^{q_y}$ is in $\mathbb{F}$.

*Case $x < y$.* Then $x/2 \le y \le 2x$ by the symmetry of the condition, and the first case with the roles of $x$ and $y$ exchanged shows $y - x \in \mathbb{F}$. Since $\mathbb{F}$ is symmetric about 0, $x - y = -(y - x) \in \mathbb{F}$.

If $x$ and $y$ are both negative, then $-x, -y$ satisfy the condition, and $x - y = -((-x) - (-y)) \in \mathbb{F}$ by the above. The condition excludes opposite signs. $\square$

The proof uses only that $D\beta^{q}$ is representable when $|D| < \beta^{p}$ and $q$ is an allowed exponent. It uses no property of $\beta$, and no upper bound on the exponents is needed, because $|x - y| \le \max(|x|, |y|)$. It does need the subnormal numbers: the integer $D$ can be small, and then $D\beta^{q_y}$ can be below $\beta^{e_{\min}}$.

## Consequences

- **Cancellation is exact.** If $\hat a$ and $\hat b$ are already rounded and $\hat b/2 \le \hat a \le 2\hat b$, then $\mathrm{fl}(\hat a - \hat b) = \hat a - \hat b$. A large relative error of the difference comes from the errors of $\hat a$ and $\hat b$, which the subtraction makes visible; see [catastrophic cancellation](/catastrophic-cancellation/).
- **Fast2Sum and TwoSum.** In the proof of [Fast2Sum](/fast-two-sum/), the step $z = \mathrm{fl}(s - a)$ is exact by this lemma in the main case. The same holds for some of the steps of [TwoSum](/two-sum/).
- **Exact reductions.** For $x \in [1/2, 2]$, $x - 1$ is exact; codes for $\log(1 + x)$ and for argument reduction (for example [Cody-Waite reduction](/cody-waite-range-reduction/), where $x - k C_1$ is formed with a short constant $C_1$) use this kind of exact step.
- **Error analysis.** In a [rounding error analysis](/rounding-error-analysis/), a subtraction covered by the lemma has $\delta = 0$, which can improve a bound.

## Tightness

The factor 2 cannot be increased, not even by one ulp. In binary64 take $x = 2$ and $y = 1 - 2^{-53}$, the float just below 1. Then $x/y = 2/(1 - 2^{-53})$ is just above 2, and

$$x - y = 1 + 2^{-53} = \frac{9007199254740993}{9007199254740992},$$

which needs 54 significant bits and is not in $\mathbb{F}$. The computed `2.0 - (1 - 2**-53)` is `1.0` (a tie, rounded to even). The same pair with the roles exchanged shows that the lower bound $y/2$ cannot be decreased.

The condition is sufficient, not necessary: $5 - 1 = 4$ is exact although $5 > 2 \cdot 1$. The proof gives a more general rule. Let $m$ be the one of $x, y$ with the smaller magnitude. Then $x - y$ is always an integer multiple of $\mathrm{ulp}(m)$, so $x - y$ is exact whenever $|x - y| < \beta^{p}\,\mathrm{ulp}(m)$. For example, with the stored value $y$ of $0.7$ and $x = 1.5$, the ratio $x/y \approx 2.14$ is above 2, but $\mathrm{ulp}(y) = 2^{-53}$ and $|x - y| \approx 0.8 < 2^{53} \cdot 2^{-53} = 1$, so `1.5 - 0.7` is exact. The rule is also only sufficient: $5 - 1$ is exact because $4$ is a power of 2, not because of it.

**Without subnormals the lemma fails.** If results below $\beta^{e_{\min}}$ are flushed to zero, take $y = \beta^{e_{\min}}$ and $x = y + \mathrm{ulp}(y)$. Then $x - y = \beta^{e_{\min} - p + 1}$ is not zero, but it is below the smallest normal number, so it is flushed to $0$, while $x \neq y$. Gradual underflow was put into IEEE 754 in part to keep such properties.

**Without a guard digit the lemma fails.** On a machine that subtracts with only $p$ digits after aligning the operands (some old machines did), the difference of close numbers can be wrong. Higham and Goldberg state the theorem for subtraction with a guard digit; correct rounding implies it.

## History

The result is in the book *Floating-Point Computation* by Pat H. Sterbenz (Prentice-Hall, 1974), and it carries his name. Goldberg (1991) gives it with a proof for a machine with a guard digit, Higham gives it in his Section 2.5, and Muller et al. give it with the role of subnormal numbers in their Section 4.2.1.

## References
