---
tag: X38093
kind: technique
slug: forward-error-analysis
name: Forward error analysis
aliases:
- forward error
- forward stability
- error propagation
area: numerical/floating-point
level: core
summary: Bounds the difference between the computed result and the exact result.
prereqs: [floating-point-model, relative-error]
see_also: [backward-error-analysis, condition-number, rounding-error-analysis, catastrophic-cancellation, interval-arithmetic, numerical-stability, floating-point-summation, error-free-transformations]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.5, Backward and Forward Errors (the definitions and forward stability); Section 3.2, The Purpose of Rounding Error Analysis; Section 3.3, Running Error Analysis; Section 3.4, Notation for Error Analysis (Lemma 3.1)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.1, Preliminaries (5.1.2 notation for error analysis and classical error estimates, 5.1.3 some refined error estimates); Section 5.2, Computing Validated Running Error Bounds
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (the propagation of relative errors through products and sums)
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the section Cancellation (the formulas x^2 - y^2 and (x - y)(x + y))
---

Forward error analysis is the technique of bounding directly how far a computed result $\hat y$ is from the exact result $y$, by following the rounding errors through each step of the computation. Each intermediate value carries an error bound, and the rules for products, quotients and sums tell how the bounds grow; the bound at the output is the result. The method is the natural one when the question is "how many digits are correct", and it explains [catastrophic cancellation](/catastrophic-cancellation/) step by step. It is often harder than [backward error analysis](/backward-error-analysis/) and its bounds are often pessimistic, so the two are used together.

## In plain words

Each step of a computation with rounding adds a tiny error. Forward error analysis follows those errors from the start to the end. A multiplication adds the relative errors of its two inputs, plus a tiny new one. An addition of two numbers with the same sign keeps the relative error small. A subtraction of two close numbers can make a small relative error large, because the result is small and the errors are not.

At the end you have a guaranteed bound on how far the computed answer can be from the true one. The bound is a worst case: it assumes that every error goes in the worst direction. Real errors often cancel, so the true error is usually much smaller than the bound.

## When it applies

- The output is a scalar or a short vector, and the question is its accuracy, for example the number of correct digits of a library function or of a formula.
- The computation is a fixed sequence of operations, such as a formula, a short loop or a polynomial; each step satisfies the [standard model](/floating-point-model/) $\mathrm{fl}(a \mathbin{op} b) = (a \mathbin{op} b)(1 + \delta)$, $|\delta| \le u$, with no underflow or overflow.
- The data cannot absorb the errors (one scalar input), so a backward result is not available.
- One wants to compare two formulas for the same quantity, as in $x^2 - y^2$ against $(x - y)(x + y)$.

**Notation.** For an exact $y \ne 0$ and a computed $\hat y$, the absolute forward error is $|\hat y - y|$ and the relative forward error is $|\hat y - y|/|y|$. An algorithm is *forward stable* if its forward error is of the size of $\mathrm{cond}(f, x) \cdot u$, the error a backward stable algorithm would have (Higham, Section 1.5). We use binary64 with round to nearest, $u = 2^{-53}$ and $\gamma_n = nu/(1 - nu)$; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**The propagation rules.** Let $\hat a = a(1 + \alpha)$ and $\hat b = b(1 + \beta)$ be computed values, with $|\alpha|, |\beta| \le \epsilon$. Then, exactly,

$$\hat a \hat b = ab(1 + \alpha)(1 + \beta), \qquad \frac{\hat a}{\hat b} = \frac{a}{b} \cdot \frac{1 + \alpha}{1 + \beta}, \qquad (\hat a + \hat b) - (a + b) = a\alpha + b\beta.$$

So a product or quotient has relative error at most $(1 + \epsilon)^2 - 1$ or $(1+\epsilon)/(1-\epsilon) - 1$, both about $2\epsilon$, before its own rounding. A sum has absolute error at most $\epsilon(|a| + |b|)$, so its relative error is at most $\epsilon\,(|a| + |b|)/|a + b|$: this is $\epsilon$ when $a$ and $b$ have the same sign, and unbounded when $a + b$ is near $0$. The rounding of the operation itself then multiplies by $1 + \delta$. With $\epsilon$ a multiple of $u$, Lemma 3.1 of Higham collects these factors into $1 + \theta_n$, $|\theta_n| \le \gamma_n$, as on the page of the [standard model](/floating-point-model/).

## The template

```pseudo id=main
FORWARD-ERROR-ANALYSIS(algorithm A, input x)
L1  for each input x_i: set its relative error bound ε_i (0 for exact data)
L2  for each operation v ← a op b of A, in order:
L3      PROPAGATE(op, bounds of a and b) → bound on |(â op b̂) − (a op b)|   ▷ hole: the rule for op
L4      add the rounding: |fl(â op b̂) − (â op b̂)| ≤ u |â op b̂|
L5      store the bound for v (relative if v is far from 0, else absolute)
L6  return the bound of the output
```

The hole at line L3 is the rule of the operation: the product and quotient rules add relative errors, and the sum rule adds absolute errors. The choice in line L5 matters: a relative bound is right for a value that is far from $0$, and an absolute bound for a value that may be the result of cancellation. A good analysis keeps the bound as a formula in the data (such as $\gamma_{n-1}\sum|x_i|$) rather than a number.

**The template on a product.** Let $\hat p_1 = x_1$ and $\hat p_k = \mathrm{fl}(\hat p_{k-1} x_k)$, with exact data. By line L4, $\hat p_k = \hat p_{k-1} x_k (1 + \delta_k)$, so $\hat p_n = x_1 x_2 \cdots x_n \prod_{k=2}^{n} (1 + \delta_k) = p_n(1 + \theta_{n-1})$ and

$$\frac{|\hat p_n - p_n|}{|p_n|} \le \gamma_{n-1}.$$

In binary64 the product of fifty copies of $\mathrm{fl}(1.1)$ is $117.39085287969573$, with relative error $-4.76u$ against the exact product of the stored values; the bound is $\gamma_{49} \approx 49u$.

## Classic examples

- **Two formulas for x² − y².** In $\mathrm{fl}(\mathrm{fl}(x^2) - \mathrm{fl}(y^2))$, the two squares have relative errors at most $u$, and the subtraction rule multiplies this by $(x^2 + y^2)/|x^2 - y^2|$. In $\mathrm{fl}(\mathrm{fl}(x - y)\,\mathrm{fl}(x + y))$, the product rule gives relative error at most $\gamma_3$ for all $x, y$, because the subtraction acts on exact inputs. For $x = 1 + 2^{-30}$ and $y = 1$, the first formula gives $1.862645149230957 \times 10^{-9}$ (relative error $-2^{-31} \approx -4.7 \times 10^{-10}$) and the second gives the exact $1.8626451500983188 \times 10^{-9}$ (Goldberg, 1991).
- **[Catastrophic cancellation](/catastrophic-cancellation/).** The sum rule, $\epsilon(|a| + |b|)/|a + b|$, is the whole explanation.
- **[Floating-point summation](/floating-point-summation/).** A forward analysis of recursive summation gives $|\hat s - s| \le \gamma_{n-1}\sum|x_i|$; for [Kahan summation](/kahan-summation/) the forward analysis is harder and gives $(2u + O(nu^2))\sum|x_i|$ (Higham, Section 4.3).
- **[Horner's rule](/horner-rule/).** The forward bound $|\hat p(x) - p(x)| \le \gamma_{2n}\sum|a_i||x|^i$ follows from the backward result; the relative error is then bounded by $\gamma_{2n}$ times the condition number $\sum|a_i||x|^i/|p(x)|$.
- **[Error-free transformations](/error-free-transformations/) and compensated algorithms.** Their proofs are forward analyses: the error of each step is computed exactly or bounded, and the final bound has the form $u|y| + \gamma_n^2 \cdot \mathrm{cond} \cdot |y|$.
- **[Interval arithmetic](/interval-arithmetic/).** An automatic, rigorous forward analysis: each value is an interval guaranteed to contain the exact one.

## Variations

- **First-order analysis.** Drop the terms of order $u^2$ and keep $\sum |\partial f/\partial v_k| \cdot |v_k| \cdot u$ over the intermediate values $v_k$. This gives the leading constant of the bound and is the basis of automatic error analysis tools (Higham, Chapter 26).
- **Running error analysis.** Compute a bound together with the result, from the actual intermediate values: for each operation $v = a \mathbin{op} b$, update the bound with $|\hat v|u$ plus the propagated bounds. It costs about one extra operation per step and gives much sharper bounds than an a priori analysis (Higham, Section 3.3; Muller et al., Section 5.2).
- **Refined constants.** With round to nearest, $\gamma_n$ can often be replaced by $nu$ without the denominator, for example for recursive summation and for products (Muller et al., Section 5.1.3; Jeannerod and Rump).
- **Probabilistic analysis.** If the rounding errors are modeled as independent random variables with mean zero, the error of a sum or a dot product grows like $\sqrt{n}\,u$ with high probability, not like $nu$. This explains the observed errors but is not a proved bound for a given input.

## Pitfalls

- **Bounds that are far too large.** The worst-case constant grows like $nu$, the observed error usually like $\sqrt{n}\,u$, and for some algorithms (pairwise summation of positive data) much less. A forward bound that is large does not mean that the result is bad.
- **Mixing relative and absolute errors.** A relative bound on a value that may be $0$ is meaningless. After a subtraction, switch to an absolute bound, as in line L5.
- **Ignoring the data error.** The data are usually rounded already, often from decimal input. A forward bound that starts from $\epsilon_i = 0$ answers a different question from "how accurate is the answer for the measured data".
- **Forgetting the conditions.** The rules assume no underflow and no overflow. Underflow adds an absolute error of up to $\tfrac12 \cdot 2^{-1074}$ per operation in binary64, which a relative bound does not cover.
- **Dependency in interval arithmetic.** An interval evaluation of $x - x$ gives $[-w, w]$, not $0$, because the two copies of $x$ are treated as independent. Automatic forward bounds can grow much faster than the true error.

## Exercises

1. Show that for $a, b \ge 0$ and $c \ge 0$, $\mathrm{fl}(\mathrm{fl}(a + b) + c)$ has relative error at most $\gamma_2$, and give inputs of mixed sign for which the relative error is $1$.
2. Prove that $\mathrm{fl}(\mathrm{fl}(x - y)\,\mathrm{fl}(x + y)) = (x^2 - y^2)(1 + \theta_3)$, $|\theta_3| \le \gamma_3$, and that $\mathrm{fl}(\mathrm{fl}(x^2) - \mathrm{fl}(y^2))$ has no relative error bound that is independent of $x$ and $y$.
3. Write a running error bound for Horner's rule: carry $\hat p_k$ and a bound $\mu_k$ with $|\hat p_k - p_k| \le \mu_k$, and show that $\mu_{k} = |x|\mu_{k-1} + u(|x||\hat p_{k-1}| + |\hat p_k|) + O(u^2)$ terms suffice.

## References
