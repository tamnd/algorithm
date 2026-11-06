---
tag: GQ0CM6
kind: theorem
slug: gcd-lcm-identity
name: GCD and LCM product identity
aliases:
- gcd times lcm identity
area: number-theory/divisibility-and-gcd
level: intro
summary: Gcd(a, b) · lcm(a, b) = |ab| for integers a and b.
prereqs: [greatest-common-divisor, least-common-multiple, bezouts-identity]
see_also: [lcm-of-integers, fundamental-theorem-of-arithmetic, coprime-integers, euclids-lemma, reducing-fractions, euclidean-algorithm]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the identities for gcd and lcm, including gcd(u, v) lcm(u, v) = uv)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 5.1, Highest common divisor and least common multiple
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.2, Primes (gcd and lcm as the minimum and the maximum of the prime exponents)
---

The GCD and LCM identity says that for all integers $a$ and $b$, the [greatest common divisor](/greatest-common-divisor/) times the [least common multiple](/least-common-multiple/) equals $|ab|$. So one gcd computation, by the [Euclidean algorithm](/euclidean-algorithm/), also gives the lcm: $\operatorname{lcm}(a, b) = |a| / \gcd(a, b) \cdot |b|$ for nonzero $a$ and $b$. The identity holds for two numbers only; for three or more numbers the product of the gcd and the lcm is not the product of the numbers.

## Statement

**Theorem.** For all integers $a$ and $b$,

$$\gcd(a, b) \cdot \operatorname{lcm}(a, b) = |ab|.$$

The conventions $\gcd(0, 0) = 0$ and $\operatorname{lcm}(a, 0) = \operatorname{lcm}(0, b) = 0$ make both sides 0 when $a = 0$ or $b = 0$. For nonzero $a$ and $b$, $\gcd(a, b) \ge 1$, and the identity is equivalent to

$$\operatorname{lcm}(a, b) = \frac{|a|}{\gcd(a, b)} \cdot |b|,$$

where the fraction is an integer because $\gcd(a, b) \mid a$.

## In plain words

Take two whole numbers. Their greatest common divisor collects the prime factors that the two numbers share. Their least common multiple collects every prime factor that either number needs, and it takes each shared factor only once. When you multiply the two numbers, each shared factor appears twice. The common divisor holds one copy of each shared factor and the common multiple holds the rest, so together they hold exactly what the product holds.

So you never need to search for the least common multiple. You find the greatest common divisor with a fast method, divide one number by it, and multiply by the other number.

## Proof

If $a = 0$ or $b = 0$, then $\operatorname{lcm}(a, b) = 0$ and $|ab| = 0$, so both sides are 0. From now on let $a \ne 0$ and $b \ne 0$, let $g = \gcd(a, b) \ge 1$, and write $a = g a'$ and $b = g b'$ with integers $a'$ and $b'$.

**Step 1: $\gcd(a', b') = 1$.** By Bézout's identity there are integers $x$ and $y$ with $ax + by = g$. Divide by $g$: $a'x + b'y = 1$. Each common divisor of $a'$ and $b'$ divides 1, so $\gcd(a', b') = 1$.

**Step 2: Gauss's lemma.** If $c \mid de$ and $\gcd(c, d) = 1$, then $c \mid e$. Indeed, $cu + dv = 1$ for some integers $u$ and $v$, so $e = c(eu) + (de)v$, and both terms are multiples of $c$.

**Step 3: $m = |a b'|$ is a common multiple.** We have $m = |a| \cdot |b'|$, a multiple of $a$, and $m = |g a' b'| = |a'| \cdot |b|$, a multiple of $b$. Also $m > 0$.

**Step 4: $m$ divides every common multiple.** Let $M$ be a common multiple of $a$ and $b$. Then $M = ak$ for an integer $k$, and $b \mid ak$ gives $g b' \mid g a' k$, so $b' \mid a' k$. By Step 1 and Step 2, $b' \mid k$. So $k = b' t$ and $M = a b' t$, a multiple of $m$.

**Step 5.** By Steps 3 and 4, $m$ is a positive common multiple that divides every common multiple. In particular $m$ divides $\operatorname{lcm}(a, b)$, so $m \le \operatorname{lcm}(a, b)$; and $m$ is a positive common multiple, so $\operatorname{lcm}(a, b) \le m$. Hence $\operatorname{lcm}(a, b) = m = |a b'| = |ab| / g$, which is the identity. $\blacksquare$

**Second proof, from prime factorizations.** For positive $a$ and $b$, the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) gives $v_p(\gcd(a, b)) = \min(v_p(a), v_p(b))$ and $v_p(\operatorname{lcm}(a, b)) = \max(v_p(a), v_p(b))$ for each prime $p$. For all real $x$ and $y$, $\min(x, y) + \max(x, y) = x + y$. So both sides of the identity have the same exponent of each prime, and they are equal. Signs do not matter, because both $\gcd$ and $\operatorname{lcm}$ depend only on $|a|$ and $|b|$.

## Consequences

- **Computing the lcm.** [LCM of integers](/lcm-of-integers/) uses $\operatorname{lcm}(a, b) = (|a| / \gcd(a, b)) \cdot |b|$. With word-sized integers, dividing first matters: for $a = b = 2^{40}$, the product $ab = 2^{80}$ overflows 64 bits, while $|a| / \gcd(a, b) \cdot |b| = 1 \cdot 2^{40}$ does not.
- **Coprime numbers.** $\operatorname{lcm}(a, b) = |ab|$ if and only if $\gcd(a, b) = 1$ (for nonzero $a$ and $b$). For example, consecutive Fibonacci numbers are [coprime](/coprime-integers/), so $\operatorname{lcm}(89, 144) = 12816 = 89 \cdot 144$.
- **Common denominators.** The least common denominator of $p/a$ and $q/b$ in lowest terms is $\operatorname{lcm}(a, b) = ab/\gcd(a, b)$. Adding fractions this way keeps the numbers small; see [reducing fractions](/reducing-fractions/).
- **Gauss's lemma.** Step 2 of the proof is the general form of [Euclid's lemma](/euclids-lemma/).

Examples:

| $a$ | $b$ | $\gcd(a, b)$ | $\operatorname{lcm}(a, b)$ | $\gcd \cdot \operatorname{lcm} = \lvert ab \rvert$ |
| --- | --- | --- | --- | --- |
| 12 | 18 | 6 | 36 | 216 |
| 21 | 6 | 3 | 42 | 126 |
| $-4$ | 6 | 2 | 12 | 24 |
| 1071 | 462 | 21 | 23562 | 494802 |
| 0 | 7 | 7 | 0 | 0 |

## Tightness

The identity does not extend to three numbers. For $a = b = c = 2$, $\gcd(2, 2, 2) \cdot \operatorname{lcm}(2, 2, 2) = 4$, but $abc = 8$. For $4, 6, 10$: the gcd is 2, the lcm is 60, so the product is 120, while $4 \cdot 6 \cdot 10 = 240$. The prime-exponent proof shows why: $\min(x, y, z) + \max(x, y, z) \ne x + y + z$ in general, because the middle exponent is lost.

The correct identity for three positive integers is

$$\operatorname{lcm}(a, b, c) \cdot \gcd(a, b) \gcd(b, c) \gcd(c, a) = abc \cdot \gcd(a, b, c).$$

Proof: for each prime, with exponents sorted as $x \le y \le z$, the left side has exponent $z + (x + y + x)$ and the right side has $x + y + z + x$, which are equal; the pairwise minima are $x$, $x$ and $y$ in some order. This is the case $k = 3$ of the inclusion and exclusion pattern for maxima and minima.

## References
