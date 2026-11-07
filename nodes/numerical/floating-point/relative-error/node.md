---
tag: 2C5BN8
kind: concept
slug: relative-error
name: Relative error
aliases:
- relative accuracy
area: numerical/floating-point
level: intro
summary: The error of an approximation divided by the size of the exact value, |x̂ - x|/|x|; the natural error measure for floating point, because rounding has a nearly constant relative error.
prereqs: [floating-point-arithmetic]
see_also: [machine-epsilon, ulp, floating-point-model, catastrophic-cancellation, condition-number, backward-error-analysis, forward-error-analysis, rounding-error-analysis]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.2, Relative Error and Significant Digits; Section 1.7, Cancellation; Section 2.2, Model of Arithmetic (the forms (1 + δ) and 1/(1 + δ)); Section 3.1 and Lemma 3.1 (products of factors 1 + δ)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.3.1, Relative error due to rounding; Section 2.3.3 on the link between errors in ulps and relative errors
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.2, Relative Error and Ulps
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (relative error, and the relations of approximate equality with a relative tolerance)
---

The relative error of an approximation $\hat x$ to a nonzero real $x$ is $|\hat x - x|/|x|$: the error measured as a fraction of the size of the true value. It is the error measure that [floating-point arithmetic](/floating-point-arithmetic/) controls, because rounding to $p$ digits makes a relative error of at most the unit roundoff $u$, whatever the size of the number. Error bounds of numerical algorithms are stated in it, and a relative error of about $10^{-k}$ means about $k$ correct significant digits.

## In plain words

An error of one meter is large for the width of a table and tiny for the distance to the Moon. The relative error compares the error with the size of the thing you measure. It says "off by one part in a thousand" instead of "off by one meter".

A computer stores a real number with a fixed number of digits, like a ruler whose marks get farther apart as the numbers grow. So the error from storing a number is always a small part of the number, never a fixed amount. That is why numerical analysts state their bounds in this form. The measure breaks down for a true value of zero, and it can grow very large when two close numbers are subtracted.

## The idea

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$, with binary64 ($\beta = 2$, $p = 53$) as the default. The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ in binary64, rounding to nearest). $\mathrm{fl}(\cdot)$ is the rounded result.

**Definitions.** For $x \neq 0$ and an approximation $\hat x$,

$$E_{\mathrm{abs}}(\hat x) = |\hat x - x|, \qquad E_{\mathrm{rel}}(\hat x) = \frac{|\hat x - x|}{|x|}.$$

The same fact is often written as $\hat x = x(1 + \delta)$, with $|\delta| = E_{\mathrm{rel}}(\hat x)$. The relative error does not change when $x$ and $\hat x$ are both multiplied by the same nonzero number. That is the reason it fits floating point: scaling by a power of $\beta$ moves a number to another binade without a change of its digits.

**What rounding gives (proved).** For each real $x$ in the normal range, $\mathrm{fl}(x) = x(1 + \delta)$ with $|\delta| \le u$ under rounding to nearest, and $|\delta| < 2u$ under a directed rounding, if there is no underflow and no overflow (Higham, Theorem 2.2; the proof is on the [machine epsilon](/machine-epsilon/) page). The absolute error is not bounded by any constant: it is up to $\tfrac12\mathrm{ulp}(x)$, and the [ulp](/ulp/) grows with $|x|$.

**Relative to which value.** A second form divides by the approximation: $x = \hat x(1 + \eta)$, or $|\hat x - x|/|\hat x|$. The two are close. If $\hat x = x(1 + \delta)$ with $|\delta| < 1$, then $x = \hat x/(1 + \delta) = \hat x(1 + \eta)$ with $\eta = -\delta/(1 + \delta)$, so $|\eta| \le |\delta|/(1 - |\delta|)$. With $|\delta| \le u$ this is $|\eta| \le u/(1-u)$. Higham, Section 2.2, uses both forms of the [standard model](/floating-point-model/), $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$ and $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)/(1 + \delta)$, each with $|\delta| \le u$, because the second form is easier in some proofs.

**Products of relative errors.** If $\hat x = x(1 + \delta_1)$ and then $\hat y = \hat x(1 + \delta_2)$, the total factor is $(1 + \delta_1)(1 + \delta_2) = 1 + \delta_1 + \delta_2 + \delta_1\delta_2$. So relative errors add, to first order, along a chain of products and quotients. The exact form is Higham's Lemma 3.1: if $|\delta_i| \le u$, $\rho_i = \pm 1$ and $nu < 1$, then

$$\prod_{i=1}^{n} (1 + \delta_i)^{\rho_i} = 1 + \theta_n, \qquad |\theta_n| \le \gamma_n = \frac{nu}{1 - nu}.$$

The proof is on the [rounding error analysis](/rounding-error-analysis/) page.

**Sums and differences can lose it.** Let $\hat a = a(1 + \delta_a)$ and $\hat b = b(1 + \delta_b)$ with $|\delta_a|, |\delta_b| \le \delta$. Then the exact difference of the approximations satisfies

$$\frac{|(\hat a - \hat b) - (a - b)|}{|a - b|} = \frac{|a\delta_a - b\delta_b|}{|a - b|} \le \delta \, \frac{|a| + |b|}{|a - b|}.$$

The factor $(|a| + |b|)/|a - b|$ is the relative [condition number](/condition-number/) of subtraction. It is large when $a \approx b$, which is [catastrophic cancellation](/catastrophic-cancellation/). The subtraction itself can be exact (see the [Sterbenz lemma](/sterbenz-lemma/)); the loss comes from the errors that the inputs already have.

**Significant digits.** If $E_{\mathrm{rel}}(\hat x) \le \tfrac12 10^{1-k}$, then $\hat x$ agrees with $x$ to about $k$ significant decimal digits. The link is not exact in either direction: $x = 1$ and $\hat x = 0.9999$ have relative error $10^{-4}$, and no digit of the two strings is the same, but $\hat x$ rounds to $1.000$ at four digits (Higham, Section 1.2, gives similar examples).

**Near zero.** For $x = 0$ the relative error is not defined, and for $x$ near zero it is large even for a tiny absolute error. Codes then use the absolute error, or a mixed test such as $|\hat x - x| \le \tau_{\mathrm{rel}} |x| + \tau_{\mathrm{abs}}$.

**Vectors.** For vectors, the *normwise* relative error is $\|\hat x - x\|/\|x\|$, and the *componentwise* one is $\max_i |\hat x_i - x_i|/|x_i|$. A small normwise error allows the small components to be wrong in all their digits.

## Examples

**Storing 1/3.** In binary64, $\mathrm{fl}(1/3) = 1/3 - 1/54043195528445952$. The relative error is $2^{-54} \approx 5.55 \times 10^{-17} = u/2$. The error divided by the computed value is the same to 16 digits.

**Approximations of $\pi$.** The fraction $22/7$ has relative error $4.02 \times 10^{-4}$ (about 3 correct digits), and $355/113$ has relative error $8.49 \times 10^{-8}$ (about 7 digits). The decimal $3.1416$ has relative error $2.34 \times 10^{-6}$.

**A difference that loses accuracy.** The literal `1.0000001` is stored with relative error $5.84 \times 10^{-17}$. The subtraction `1.0000001 - 1.0` is exact, and it gives $1.0000000005838672 \times 10^{-7}$. Compared with the intended $10^{-7}$, the relative error is $5.84 \times 10^{-10}$: the input error grew by a factor of $10^{7}$, within the bound $(|a| + |b|)/|a - b| \approx 2 \times 10^{7}$ above.

**A sum that loses all of it.** `1e16 + 1 - 1e16` gives `0.0`, a relative error of 1 against the true value 1, because $\mathrm{ulp}(10^{16}) = 2$ and the first sum rounds to $10^{16}$. Each operation had a relative error below $u$.

## Where it is used

- **Error models.** The [standard model](/floating-point-model/) and all bounds of [rounding error analysis](/rounding-error-analysis/) are relative.
- **Backward and forward error.** A [backward error](/backward-error-analysis/) is usually a relative perturbation of the data, and the [forward error](/forward-error-analysis/) is bounded by the condition number times it.
- **Accuracy of libraries.** Math libraries quote errors in [ulps](/ulp/), which convert to relative errors within a factor of $\beta$.
- **Stopping tests.** Iterative methods such as Newton's method stop when the relative change of the iterate falls below a tolerance.
- **Comparisons in tests.** `math.isclose(a, b, rel_tol=1e-9)` tests $|a - b| \le 10^{-9} \max(|a|, |b|)$, a relative difference with respect to the larger value. It needs a nonzero `abs_tol` to compare a value with zero.

## References
