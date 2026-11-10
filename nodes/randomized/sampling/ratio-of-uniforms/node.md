---
tag: 3SHGH5
kind: algorithm
slug: ratio-of-uniforms
name: Ratio-of-uniforms method
aliases:
- ratio of uniforms
- ROU method
- Kinderman-Monahan method
area: randomized/sampling
level: advanced
summary: Sample a uniform point in a region and return the ratio of its coordinates, yielding the target distribution.
solves: [random-variate-generation]
model: real-ram
complexity:
  vars: {n: the number of variates, p: "the acceptance probability, the area of C_h over the area of the box"}
  time: {expected: Θ(n/p)}
  space: {extra: O(1)}
properties: {deterministic: false, exact: true, online: true, recursive: false}
history:
  year: 1977
  people: [Albert J. Kinderman, John F. Monahan]
  note: Kinderman and Monahan published the method in ACM Transactions on Mathematical Software in 1977.
prereqs: [rejection-sampling, change-of-variables, probability-density-function]
see_also: [rejection-sampling, random-variate-generation, inverse-transform-sampling, box-muller-transform, marsaglia-polar-method, ziggurat-method, adaptive-rejection-sampling]
sources:
  - paper: doi:10.1145/355744.355750
    title: Albert J. Kinderman and John F. Monahan, Computer generation of random variables using the ratio of uniform deviates, ACM Transactions on Mathematical Software 3(3), 1977
    locator: pages 257 to 260
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter IV, Section 7 (the ratio-of-uniforms method)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1, Part C, Algorithm R (the ratio method for normal deviates)
  - paper: "Josef Leydold, Automatic sampling with the ratio-of-uniforms method, ACM Transactions on Mathematical Software 26(1), 2000"
    locator: the whole paper (convexity of the region for T-concave densities)
---

The ratio-of-uniforms method generates a variate with density proportional to $h \ge 0$ from a uniform random point $(U, V)$ in the region $C_h = \{(u, v) : 0 < u \le \sqrt{h(v/u)}\}$: the ratio $X = V/U$ has density $h/\int h$. The uniform point comes from [rejection sampling](/rejection-sampling/) from a box $(0, a] \times [b_-, b_+]$ that holds $C_h$, with $a = \sup \sqrt{h}$ and $b_\pm$ the extremes of $x\sqrt{h(x)}$. The proof is one [change of variables](/change-of-variables/), $du\,dv = u\,du\,dx$. Kinderman and Monahan published it in 1977. It gives short exact generators for the normal, Cauchy, gamma, Student t and other laws, with no need to normalize $h$.

## In plain words

Rejection sampling needs a simple shape that sits above the density. Finding a good one can be hard, mostly because of the tails.

This method moves the problem to another picture. It draws a strange region in a second plane, made from the density. The region has a useful property: if you take a random point in it and divide its second coordinate by its first, the result has exactly the law you want.

For many densities, even those with long tails, this region is small and compact. So a plain rectangle around it is a good enough cover. You throw random points into the rectangle, keep the first one that falls inside the region, and divide.

## The problem

Given an unnormalized density $h \ge 0$ on $\mathbb{R}$ with $0 < \int h < \infty$, generate independent variates with density $h/\int h$. This is the [random variate generation](/random-variate-generation/) problem. The method needs:

- $h$ can be evaluated at any point;
- the three numbers $a = \sup_x \sqrt{h(x)}$, $b_- = \inf_x x\sqrt{h(x)}$ and $b_+ = \sup_x x\sqrt{h(x)}$ are known and finite. This holds when $h$ is bounded and $x^2 h(x)$ is bounded, so tails as heavy as $1/x^2$ are fine.

The model is the [real RAM](/real-ram/) with independent uniform reals.

## The algorithm

```pseudo id=main
RATIO-OF-UNIFORMS(h, a, b₋, b₊)
L1  repeat
L2      U ← a uniform real in (0, a];  V ← a uniform real in [b₋, b₊]
L3      X ← V / U
L4  until U² ≤ h(X)                         ▷ the point (U, V) is in C_h
L5  return X
```

For the standard normal, $h(x) = e^{-x^2/2}$ gives $a = 1$ and $b_\pm = \pm\sqrt{2/e} \approx \pm 0.8578$, and the test in line L4 is $X^2 \le -4 \ln U$. This is the Kinderman-Monahan normal generator.

## Example

The normal generator, with $b = \sqrt{2/e} = 0.8578$. All four points lie in the box $(0, 1] \times [-0.8578, 0.8578]$:

| $U$ | $V$ | $X = V/U$ | $X^2$ | $-4 \ln U$ | result |
|---|---|---|---|---|---|
| 0.2 | 0.8 | 4.0000 | 16.0000 | 6.4378 | reject |
| 0.5 | 0.3 | 0.6000 | 0.3600 | 2.7726 | accept, return 0.6 |
| 0.9 | 0.8 | 0.8889 | 0.7901 | 0.4214 | reject |
| 0.7 | $-0.5$ | $-0.7143$ | 0.5102 | 1.4267 | accept, return $-0.7143$ |

A small $U$ allows a large $|X|$, which is how the method reaches into the tails: $|X| = |V|/U$ is unbounded even though the box is bounded. The acceptance probability is $\operatorname{area}(C_h)/\operatorname{area}(\text{box}) = \frac{1}{2}\sqrt{2\pi} / (2\sqrt{2/e}) = \sqrt{\pi e}/4 \approx 0.7306$, so a variate takes $1.369$ tries in expectation.

For the Cauchy density $h(x) = 1/(1 + x^2)$, the region $C_h$ is the right half of the unit disk, $a = 1$ and $b_\pm = \pm 1$: the method draws a uniform point in a half disk and returns $V/U$, the tangent of a uniform angle.

## Correctness

**Theorem.** If $a$, $b_-$, $b_+$ are as above, RATIO-OF-UNIFORMS returns a variate with density $h/\int h$. The number of tries is geometric with success probability $p = \int h / \bigl(2a(b_+ - b_-)\bigr)$.

Write $v = ux$. The map $(u, x) \mapsto (u, ux)$ has Jacobian determinant $u$, so $du\,dv = u\,du\,dx$, and

$$\operatorname{area}\{(u, v) \in C_h : v/u \in A\} = \int_A \int_0^{\sqrt{h(x)}} u\,du\,dx = \frac{1}{2}\int_A h.$$

So for a uniform point in $C_h$, the ratio falls in $A$ with probability $\int_A h / \int h$. Every point of $C_h$ has $u \le \sqrt{h(x)} \le a$ and $v = xu$ between $b_-$ and $b_+$, so the box holds $C_h$. Rejection from the box gives a uniform point in $C_h$. The full proof is below.

The method is exact for exact uniform reals and exact arithmetic.

## Complexity

- **Per variate.** $1/p$ tries in expectation, each with two uniforms, one division and one evaluation of $h$. The number of tries is [geometric](/geometric-distribution/).
- **Acceptance.** $p = \sqrt{\pi e}/4 \approx 0.731$ for the normal, $\pi/4 \approx 0.785$ for the Cauchy, $e/4 \approx 0.680$ for the exponential.
- **Total.** $n$ variates take $\Theta(n/p)$ expected time. There is no worst-case bound.
- **Setup.** Finding $a$ and $b_\pm$ is one-dimensional optimization. For many standard densities they have closed forms.

## Properties

- **Exact** in the real RAM model.
- **No normalizing constant.** Only $h$ up to a constant factor is needed, as in rejection sampling.
- **Heavy tails.** The box is bounded whenever $h$ and $x^2 h$ are bounded, so the method handles tails like $1/x^2$, where a simple rejection envelope is hard to find.
- **Location.** Replacing $h(x)$ by $h(x + \mu)$ changes $b_\pm$ and so $p$. A good shift, often near the mode, can raise $p$.

## Variants and improvements

- **Squeezes.** Simple bounds on $\ln$ decide most tries without computing it. For the normal test $X^2 \le -4\ln U$, the tangent bound $\ln u \le e^{1/4}u - \frac{5}{4}$ gives a quick accept when $X^2 \le 5 - 4e^{1/4}U$, and the bound $\ln u \ge 1 - c/u + \ln c$ with $c = e^{-1.35}$ gives a quick reject when $X^2 \ge 4e^{-1.35}/U + 1.4$. Knuth's Algorithm R uses these two tests.
- **Better covers than a box.** When $C_h$ is convex, a polygon around it fits better than a box. Leydold (2000) showed that $C_h$ is convex when $-1/\sqrt{h}$ is concave, which holds for all log-concave densities, and built automatic generators on this.
- **Generalized ratio-of-uniforms.** The region $\{0 < u \le h(v/u^r)^{1/(r+1)}\}$ with $X = V/U^r$ works for each $r > 0$, with the same change-of-variables proof. $r = 1$ is the basic method.
- **Comparison with rejection.** The ratio-of-uniforms method is itself a rejection method, in the $(u, v)$ plane. See [rejection sampling](/rejection-sampling/) for the general case and [adaptive rejection sampling](/adaptive-rejection-sampling/) for log-concave densities with an envelope that improves itself.
- **Other normal generators.** The [Box-Muller transform](/box-muller-transform/), the [Marsaglia polar method](/marsaglia-polar-method/) and the [ziggurat method](/ziggurat-method/) solve the normal case by other means.

## When to use it

Use the ratio-of-uniforms method for a fixed density with a simple formula, when the inverse distribution function is not available, and when a good rejection envelope is hard to find, for example for gamma, beta, Student t or Cauchy variates. For the normal density only, the ziggurat method is usually faster.

## Pitfalls

- **The square.** The test is $U^2 \le h(X)$, not $U \le h(X)$. The second test gives density proportional to $h^2$, for the normal a variance of $1/2$.
- **A box that is too small.** If $b_+$ is less than $\sup x\sqrt{h(x)}$, part of $C_h$ is cut off and the tails lose mass. Compute the extremes carefully, by calculus or with a safe upper bound.
- **$U = 0$.** Line L2 draws $U$ from $(0, a]$. With $U = 0$ the ratio is not defined. Use $a(1 - R)$ for a generator $R$ in $[0, 1)$.
- **Densities with heavier tails.** If $x^2 h(x)$ is not bounded, $b_\pm$ is infinite and the box does not exist. Use the generalized form with a larger $r$, or a transformation.
- **Floating point.** $U \ge 2^{-53}a$ with 53-bit uniforms, so $|X| \le 2^{53}\max(|b_-|, b_+)/a$ and the output lies on a finite set. The method is exact only in exact arithmetic.

## Implementations

## History

Kinderman and Monahan published the method in 1977, with generators for the normal and other densities. Knuth presents the normal version as Algorithm R, with the quick tests above. Devroye gives the general theory in Section IV.7 of his 1986 book. Leydold (2000) used the convexity of $C_h$ for automatic generators.

## References
