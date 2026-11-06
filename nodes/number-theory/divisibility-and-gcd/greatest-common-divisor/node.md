---
tag: ZH68PY
kind: definition
slug: greatest-common-divisor
name: Greatest common divisor
aliases:
- gcd
- highest common factor
- greatest common factor
area: number-theory/divisibility-and-gcd
level: intro
summary: The largest integer dividing both a and b, not both zero.
prereqs: [divisibility, divisor]
see_also: [least-common-multiple, coprime-integers, bezouts-identity, euclidean-algorithm, binary-gcd, gcd-of-two-integers, gcd-lcm-identity, polynomial-gcd]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (common divisors and greatest common divisors, and the theorem that gcd(a, b) is the smallest positive element of the set of linear combinations of a and b)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the definition, the conventions for zero and the basic identities)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.3, Greatest common divisor, and Section 1.8, The greatest common divisor of more than two numbers
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.1, Divisibility (gcd and lcm), and Section 4.2, Primes (gcd and lcm from the exponents of the prime factorization)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 5.1, Highest common divisor and least common multiple
---

The greatest common divisor of two integers $a$ and $b$, not both zero, is the largest integer that [divides](/divisibility/) both of them, written $\gcd(a, b)$. It is always positive, it does not depend on the signs of $a$ and $b$, and the convention $\gcd(0, 0) = 0$ extends it to all pairs. It is also the common divisor that every other common [divisor](/divisor/) divides, and the smallest positive integer of the form $ax + by$ with integers $x$ and $y$. The [Euclidean algorithm](/euclidean-algorithm/) computes it in $O(\log \min(|a|, |b|))$ division steps, without factoring.

## Definition

Let $a$ and $b$ be integers. A **common divisor** of $a$ and $b$ is an integer $d$ with $d \mid a$ and $d \mid b$.

If $a$ and $b$ are not both zero, the **greatest common divisor** of $a$ and $b$ is

$$\gcd(a, b) = \max\{\, d \in \mathbb{Z} : d \mid a \text{ and } d \mid b \,\}.$$

The maximum exists. The number 1 is a common divisor, so the set is not empty. If $a \ne 0$, each divisor $d$ of $a$ has $|d| \le |a|$, so the set is finite (the same holds with $b$ if $b \ne 0$). Since 1 is in the set, $\gcd(a, b) \ge 1$.

For $a = b = 0$, every integer is a common divisor and there is no largest one. The standard convention is

$$\gcd(0, 0) = 0.$$

With this convention, $\gcd(a, b) \ge 0$ for all integers $a$ and $b$, and $\gcd(a, b) = 0$ if and only if $a = b = 0$. Python's `math.gcd`, C++'s `std::gcd` and most computer algebra systems follow it.

**Equivalent forms.** For all integers $a$ and $b$, these three statements about an integer $g \ge 0$ are equivalent.

1. $g = \gcd(a, b)$.
2. $g \mid a$, $g \mid b$, and every common divisor $c$ of $a$ and $b$ divides $g$.
3. $g$ is the smallest positive element of $\{ax + by : x, y \in \mathbb{Z}\}$, or $g = 0$ when $a = b = 0$.

*Proof.* If $a = b = 0$, the only value of $ax + by$ is 0, the only $g \ge 0$ that each integer divides is $g = 0$, and $\gcd(0, 0) = 0$ by the convention, so all three give $g = 0$. Now let $a$ and $b$ be not both zero, and let $s$ be the smallest positive element of $L = \{ax + by\}$; it exists because $|a| + |b| \in L$ is positive. Write $a = qs + r$ with $0 \le r < s$. Then $r = a - q(ax_0 + by_0) \in L$, and $r < s$, so $r = 0$ by the choice of $s$. Thus $s \mid a$, and in the same way $s \mid b$. Each common divisor $c$ divides $ax_0 + by_0 = s$, so $|c| \le s$. Hence $s$ is the largest common divisor: $s = \gcd(a, b)$, which shows that (1) and (3) give the same number, and that this number has property (2). If $g \ge 0$ has property (2), then $g \mid a$ and $g \mid b$ with $a$ or $b$ nonzero, so $g \ne 0$; also $s \mid g$ and $g \mid s$, so $g = s$. $\square$

Form 3 is [Bézout's identity](/bezouts-identity/). Form 2 is the definition used in rings other than $\mathbb{Z}$, for example for polynomials or in a [Euclidean domain](/euclidean-domain/): there "greatest" means "greatest in the divisibility order", and the gcd is unique only up to a unit factor. In $\mathbb{Z}$ the units are $\pm 1$, and the sign condition $g \ge 0$ picks one.

**Several integers.** For integers $a_1, \ldots, a_k$, $\gcd(a_1, \ldots, a_k)$ is the largest common divisor of all of them, or 0 if all are 0. It satisfies $\gcd(a_1, \ldots, a_k) = \gcd(\gcd(a_1, \ldots, a_{k-1}), a_k)$, because both sides have the same set of common divisors. The [GCD of an array](/gcd-of-array/) page computes it.

**Basic identities.** For all integers $a$, $b$, $m$ and $k$:

- $\gcd(a, b) = \gcd(b, a) = \gcd(|a|, |b|)$, because $d \mid a$ if and only if $d \mid -a$.
- $\gcd(a, 0) = |a|$, because each integer divides 0 and the largest divisor of $a \ne 0$ is $|a|$.
- $\gcd(a, b) = \gcd(a, b + ka)$, because $d \mid a$ and $d \mid b$ hold if and only if $d \mid a$ and $d \mid b + ka$. With $k = -\lfloor b/a \rfloor$ this is the step of the Euclidean algorithm; see the [GCD recursion theorem](/gcd-recursion-theorem/).
- $\gcd(ma, mb) = |m| \gcd(a, b)$, because by form 3 the smallest positive value of $max + mby$ is $|m|$ times the smallest positive value of $ax + by$ (for $m \ne 0$; for $m = 0$ both sides are 0).
- If $g = \gcd(a, b) > 0$, then $\gcd(a/g, b/g) = 1$, by the previous line with $m = g$.

**From the prime factorizations.** If $a = \prod_p p^{\alpha_p}$ and $b = \prod_p p^{\beta_p}$ are the factorizations of positive integers given by the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), then

$$\gcd(a, b) = \prod_p p^{\min(\alpha_p, \beta_p)}.$$

A positive $d = \prod_p p^{\delta_p}$ divides both numbers if and only if $\delta_p \le \alpha_p$ and $\delta_p \le \beta_p$ for each prime $p$, and the largest such $d$ takes $\delta_p = \min(\alpha_p, \beta_p)$. This formula is useful in proofs, but it is a poor way to compute, because factoring is much harder than the Euclidean algorithm.

## Examples and non-examples

- $\gcd(12, 18) = 6$. The positive common divisors are 1, 2, 3 and 6.
- $\gcd(-12, 18) = 6$ and $\gcd(-12, -18) = 6$. The gcd ignores signs.
- $\gcd(0, 5) = 5$ and $\gcd(0, 0) = 0$.
- $\gcd(1071, 462) = 21$, and $21 = 1071 \cdot (-3) + 462 \cdot 7$ is the smallest positive combination.
- $\gcd(360, 84) = 12$: with $360 = 2^3 \cdot 3^2 \cdot 5$ and $84 = 2^2 \cdot 3 \cdot 7$, the minimum exponents give $2^2 \cdot 3 = 12$.
- $\gcd(2^{10}, 2^6 \cdot 3) = 2^6 = 64$.
- $\gcd(89, 144) = 1$. Consecutive [Fibonacci numbers](/fibonacci-numbers/) are always [coprime](/coprime-integers/), and they are the inputs on which the Euclidean algorithm takes the most steps ([Lamé's theorem](/lames-theorem/)).
- $\gcd(12, 18, 30) = 6$, and $\gcd(6, 10, 15) = 1$ although no two of 6, 10 and 15 are coprime.
- **Non-example.** 3 is a common divisor of 12 and 18, but it is not the greatest. The greatest common divisor is not the smallest common divisor either: the smallest positive one is always 1.
- **Non-example.** $-6$ divides 12 and 18, but $\gcd(12, 18) = 6$, not $-6$. The sign convention makes the gcd a function with one value.
- **Non-example.** For $a = b = 0$ the set of common divisors is all of $\mathbb{Z}$, so the formula with the maximum does not apply. The value 0 is a convention, chosen so that form 2 still holds.

## Related definitions

- [Least common multiple](/least-common-multiple/): the smallest positive common multiple. For nonzero $a$ and $b$, $\gcd(a, b) \cdot \operatorname{lcm}(a, b) = |ab|$, the [GCD and LCM identity](/gcd-lcm-identity/).
- [Coprime integers](/coprime-integers/): $a$ and $b$ with $\gcd(a, b) = 1$.
- [Bézout's identity](/bezouts-identity/): $\gcd(a, b) = ax + by$ for some integers $x$ and $y$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) finds $x$ and $y$.
- [Euclidean algorithm](/euclidean-algorithm/) and [binary GCD](/binary-gcd/): the standard ways to compute the gcd. The computing task is the [GCD of two integers](/gcd-of-two-integers/) problem.
- [Euclidean domain](/euclidean-domain/) and [polynomial GCD](/polynomial-gcd/): the same notion in other rings, unique up to a unit.
- [Reducing fractions](/reducing-fractions/): $a/b$ is in lowest terms when $\gcd(a, b) = 1$.

## References
