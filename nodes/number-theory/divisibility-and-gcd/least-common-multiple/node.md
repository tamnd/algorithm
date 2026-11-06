---
tag: YNCKGG
kind: definition
slug: least-common-multiple
name: Least common multiple
aliases:
- lcm
- lowest common multiple
area: number-theory/divisibility-and-gcd
level: intro
summary: The smallest positive integer divisible by both a and b.
prereqs: [divisibility, greatest-common-divisor]
see_also: [gcd-lcm-identity, lcm-of-integers, coprime-integers, fundamental-theorem-of-arithmetic, chinese-remainder-theorem, reducing-fractions]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the definition of the least common multiple, the convention for zero, and the identities that relate it to the gcd)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.1, Divisibility (gcd and lcm), and Section 4.2, Primes (lcm as the maximum of the exponents)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 5.1, Highest common divisor and least common multiple
---

The least common multiple of two nonzero integers $a$ and $b$ is the smallest positive integer that both $a$ and $b$ [divide](/divisibility/), written $\operatorname{lcm}(a, b)$. It is the dual of the [greatest common divisor](/greatest-common-divisor/): for nonzero $a$ and $b$, $\operatorname{lcm}(a, b) = |ab| / \gcd(a, b)$, so one gcd computation gives it. Every common multiple of $a$ and $b$ is a multiple of the lcm. It is the period of two events that repeat every $a$ and every $b$ steps, the common denominator of $1/a$ and $1/b$, and the modulus of the combined congruence in the [Chinese remainder theorem](/chinese-remainder-theorem/).

## Definition

Let $a$ and $b$ be integers. A **common multiple** of $a$ and $b$ is an integer $m$ with $a \mid m$ and $b \mid m$.

If $a \ne 0$ and $b \ne 0$, the **least common multiple** of $a$ and $b$ is

$$\operatorname{lcm}(a, b) = \min\{\, m \in \mathbb{Z} : m > 0,\ a \mid m \text{ and } b \mid m \,\}.$$

The minimum exists because $|ab|$ is a positive common multiple, so the set is a nonempty set of positive integers. If $a = 0$ or $b = 0$, then the only common multiple is 0, because $0 \mid m$ forces $m = 0$. The standard convention is

$$\operatorname{lcm}(a, 0) = \operatorname{lcm}(0, b) = 0.$$

With it, $\operatorname{lcm}(a, b) \ge 0$ for all integers, and it is 0 exactly when $a = 0$ or $b = 0$. Python's `math.lcm` and C++'s `std::lcm` follow this convention.

**Equivalent form.** For all integers $a$ and $b$, an integer $m \ge 0$ equals $\operatorname{lcm}(a, b)$ if and only if $a \mid m$, $b \mid m$, and $m$ divides every common multiple of $a$ and $b$.

*Proof.* If $a = 0$ or $b = 0$, the only common multiple is 0, so both sides say $m = 0$. Let $a, b \ne 0$, let $\ell = \operatorname{lcm}(a, b)$, and let $M$ be a common multiple. Write $M = q\ell + r$ with $0 \le r < \ell$. Since $a \mid M$ and $a \mid \ell$, also $a \mid r$, and in the same way $b \mid r$. If $r > 0$, then $r$ is a positive common multiple smaller than $\ell$, which is false. So $r = 0$ and $\ell \mid M$. Conversely, let $m \ge 0$ have the property. Then $m$ is a common multiple, and $m \ne 0$ because $m \mid \ell$ and $\ell > 0$. Also $\ell \mid m$ and $m \mid \ell$ with both positive, so $m = \ell$. $\square$

So the lcm is the least common multiple in the divisibility order too. This form is the definition in other rings, such as polynomials, where the lcm is unique up to a unit factor.

**Several integers.** $\operatorname{lcm}(a_1, \ldots, a_k)$ is the smallest positive common multiple of all of them if none is 0, and 0 otherwise. By the equivalent form, $\operatorname{lcm}(a_1, \ldots, a_k) = \operatorname{lcm}(\operatorname{lcm}(a_1, \ldots, a_{k-1}), a_k)$, so it can be computed by a fold; see [LCM of integers](/lcm-of-integers/).

**From the prime factorizations.** For positive $a = \prod_p p^{\alpha_p}$ and $b = \prod_p p^{\beta_p}$, given by the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/),

$$\operatorname{lcm}(a, b) = \prod_p p^{\max(\alpha_p, \beta_p)}.$$

A positive $m = \prod_p p^{\mu_p}$ is a common multiple if and only if $\mu_p \ge \alpha_p$ and $\mu_p \ge \beta_p$ for each prime $p$, and the smallest such $m$ takes $\mu_p = \max(\alpha_p, \beta_p)$. Since $\min(\alpha, \beta) + \max(\alpha, \beta) = \alpha + \beta$, this gives the [GCD and LCM identity](/gcd-lcm-identity/) $\gcd(a, b) \cdot \operatorname{lcm}(a, b) = ab$.

**Basic identities.** For all integers $a$, $b$ and $m$: $\operatorname{lcm}(a, b) = \operatorname{lcm}(b, a) = \operatorname{lcm}(|a|, |b|)$; $\operatorname{lcm}(a, 1) = |a|$; $\operatorname{lcm}(a, a) = |a|$; $\operatorname{lcm}(ma, mb) = |m| \operatorname{lcm}(a, b)$; and $\operatorname{lcm}(a, b) = |ab|$ if and only if $\gcd(a, b) = 1$ or $ab = 0$.

## Examples and non-examples

- $\operatorname{lcm}(4, 6) = 12$. The positive common multiples are 12, 24, 36 and so on, and each is a multiple of 12.
- $\operatorname{lcm}(-4, 6) = 12$. The lcm ignores signs.
- $\operatorname{lcm}(0, 5) = 0$, by the convention.
- $\operatorname{lcm}(21, 6) = 42 = 21 \cdot 6 / 3$, with $\gcd(21, 6) = 3$.
- $\operatorname{lcm}(360, 84) = 2520$: with $360 = 2^3 \cdot 3^2 \cdot 5$ and $84 = 2^2 \cdot 3 \cdot 7$, the maximum exponents give $2^3 \cdot 3^2 \cdot 5 \cdot 7$.
- $\operatorname{lcm}(1, 2, \ldots, 10) = 2520$ and $\operatorname{lcm}(1, 2, \ldots, 20) = 232792560$.
- $\operatorname{lcm}(6, 10, 15) = 30$, much less than $6 \cdot 10 \cdot 15 = 900$.
- $\operatorname{lcm}(89, 144) = 12816 = 89 \cdot 144$, because consecutive Fibonacci numbers are [coprime](/coprime-integers/).
- **Non-example.** 24 is a common multiple of 4 and 6, but not the least one.
- **Non-example.** The product $ab$ is a common multiple, but it is the lcm only when $\gcd(a, b) = 1$. For 4 and 6, $ab = 24 \ne 12$.
- **Non-example.** 0 is a common multiple of every pair, but it is not the lcm of two nonzero integers, because the definition asks for a positive multiple.
- **On a computer.** For $a = b = 2^{40}$, the product $ab = 2^{80}$ does not fit in 64 bits, but $\operatorname{lcm}(a, b) = 2^{40}$ does. So code computes $(|a| / \gcd(a, b)) \cdot |b|$, and divides before it multiplies.

## Related definitions

- [Greatest common divisor](/greatest-common-divisor/): the largest common divisor; the lcm is its dual.
- [GCD and LCM identity](/gcd-lcm-identity/): $\gcd(a, b) \cdot \operatorname{lcm}(a, b) = |ab|$.
- [LCM of integers](/lcm-of-integers/): the computing task for two or more integers, and the growth of $\operatorname{lcm}(1, \ldots, n)$.
- [Coprime integers](/coprime-integers/): the lcm of coprime integers is their product.
- [Chinese remainder theorem](/chinese-remainder-theorem/): two congruences modulo $a$ and $b$ that agree modulo $\gcd(a, b)$ combine into one congruence modulo $\operatorname{lcm}(a, b)$.
- [Reducing fractions](/reducing-fractions/): the least common denominator of $p/a$ and $q/b$ in lowest terms is $\operatorname{lcm}(a, b)$.

## References
