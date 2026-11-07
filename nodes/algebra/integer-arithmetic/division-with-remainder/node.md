---
tag: CEHANR
kind: definition
slug: division-with-remainder
name: Division with remainder
aliases:
- Euclidean division
- division algorithm theorem
area: algebra/integer-arithmetic
level: intro
summary: Every integer a and positive b give unique q and r with a = qb + r and 0 <= r < b.
prereqs: [divisibility]
see_also: [floor-division, integer-division, long-division, euclidean-algorithm, congruence, euclidean-domain, divisibility]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (the division theorem, and the definitions of quotient, remainder and mod)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.4, Integer functions and elementary number theory (the definition of x mod y by the floor function)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 3.4, 'mod', the binary operation
  - paper: doi:10.1145/128861.128862
    title: Raymond T. Boute, The Euclidean definition of the functions div and mod, ACM Transactions on Programming Languages and Systems 14(2), 1992
    locator: pp. 127 to 144 (the Euclidean, floored and truncated conventions compared)
---

Division with remainder is the statement that for each integer $a$ and each positive integer $b$ there are unique integers $q$ and $r$ with $a = qb + r$ and $0 \le r < b$. The number $q = \lfloor a/b \rfloor$ is the *quotient* and $r = a \bmod b$ is the *remainder*. The statement is often called the division algorithm, although it is a theorem; the algorithms that compute $q$ and $r$ are on the page [integer division](/integer-division/). It is the base of [divisibility](/divisibility/), [congruences](/congruence/) and the [Euclidean algorithm](/euclidean-algorithm/).

## Definition

**Theorem (division with remainder).** Let $a \in \mathbb{Z}$ and $b \in \mathbb{Z}$ with $b > 0$. There is exactly one pair $(q, r) \in \mathbb{Z}^2$ with

$$a = qb + r \quad \text{and} \quad 0 \le r < b .$$

It is $q = \lfloor a/b \rfloor$ and $r = a - b\lfloor a/b \rfloor$.

*Proof of existence.* Let $q = \lfloor a/b \rfloor$, the largest integer with $q \le a/b$, and $r = a - qb$. From $q \le a/b < q + 1$ and $b > 0$ we get $qb \le a < qb + b$, so $0 \le r < b$.

*Proof of uniqueness.* Let $a = qb + r = q'b + r'$ with $0 \le r, r' < b$. Then $(q - q')b = r' - r$, and $-b < r' - r < b$. So $|q - q'| \cdot b < b$, hence $|q - q'| < 1$, and $q = q'$ because both are integers. Then $r = r'$. $\blacksquare$

**The general divisor.** For $b < 0$ the same proof, with $|b|$ in place of $b$, gives a unique pair with $a = qb + r$ and $0 \le r < |b|$. This is *Euclidean division*: the remainder is never negative. For $b = 0$ there is no quotient.

**Notation.** We write $a \operatorname{div} b = q$ and $a \bmod b = r$. Knuth (Section 1.2.4) defines $x \bmod y = x - y \lfloor x/y \rfloor$ for all real $x$ and $y \ne 0$, and $x \bmod 0 = x$. For $y > 0$ this agrees with the theorem. For $y < 0$ it gives a remainder in $(y, 0]$, which is the [floored division](/floor-division/) rule and differs from the Euclidean rule.

**Divisibility.** $b$ divides $a$, written $b \mid a$, exactly when $a \bmod b = 0$. Two integers are congruent modulo $b$ exactly when they have the same remainder: $a \equiv a' \pmod b \iff a \bmod b = a' \bmod b$.

**In a positional system.** In the base $\beta$, the remainder $a \bmod \beta$ is the last digit of $a \ge 0$ and $\lfloor a/\beta \rfloor$ is $a$ with that digit removed. Repeating this gives the digits of $a$, which proves that each nonnegative integer has a [positional representation](/positional-number-system/).

## Examples and non-examples

**Examples.** The table gives the Euclidean pair for a few inputs. Each row satisfies $a = qb + r$ and $0 \le r < |b|$.

| $a$ | $b$ | $q$ | $r$ | check |
|---|---|---|---|---|
| 17 | 5 | 3 | 2 | $3 \cdot 5 + 2 = 17$ |
| $-17$ | 5 | $-4$ | 3 | $-4 \cdot 5 + 3 = -17$ |
| 17 | $-5$ | $-3$ | 2 | $(-3)(-5) + 2 = 17$ |
| $-17$ | $-5$ | 4 | 3 | $4 \cdot (-5) + 3 = -17$ |
| 0 | 5 | 0 | 0 | $0 \cdot 5 + 0 = 0$ |
| $-1$ | 5 | $-1$ | 4 | $-1 \cdot 5 + 4 = -1$ |

The second row is the common trap: the quotient of $-17$ by $5$ is $-4$, not $-3$, because $-3 \cdot 5 = -15 > -17$ would need the remainder $-2$.

**Non-examples.**

- $17 = 2 \cdot 5 + 7$ is a true equation, but $(2, 7)$ is not the pair of the theorem, because $7 \ge 5$. Uniqueness holds only together with the bound on $r$.
- $-17 = -3 \cdot 5 + (-2)$ is the result of truncated division, as in C and Java. Its remainder $-2$ is outside $[0, 5)$, so it is not the Euclidean pair.
- For $b = 0$ there is no pair: $a = q \cdot 0 + r$ forces $r = a$, and no bound $0 \le r < 0$ can hold.
- Over the rationals, $17/5 = 3.4$ is a quotient with no remainder. Division with remainder is a statement about $\mathbb{Z}$, and about rings with a similar size function, the [Euclidean domains](/euclidean-domain/).

**In a program.** Python's `divmod(-17, 5)` is `(-4, 3)`, the Euclidean pair, because for $b > 0$ the floored rule of Python and the Euclidean rule agree. `divmod(17, -5)` is `(-4, -3)` in Python, the floored pair, while the Euclidean pair is $(-3, 2)$.

## Related definitions

- [Floor division](/floor-division/): the quotient rounds toward $-\infty$ and the remainder has the sign of the divisor. It agrees with this page when $b > 0$.
- Truncated division: the quotient rounds toward zero, and the remainder has the sign of the dividend. It is the rule of C (since C99), C++, Java and the division instructions of most processors.
- [Integer division](/integer-division/): the computational problem of finding $q$ and $r$ for large numbers, with [long division](/long-division/) and faster methods.
- [Divisibility](/divisibility/) and [congruence](/congruence/): defined by a zero remainder and by equal remainders.
- [Euclidean domain](/euclidean-domain/): a ring with a size function for which a division with a smaller remainder always exists, such as the polynomials over a field ([polynomial division](/polynomial-division/)).
- [Euclidean algorithm](/euclidean-algorithm/): the [greatest common divisor](/greatest-common-divisor/) by repeated division with remainder, based on $\gcd(a, b) = \gcd(b, a \bmod b)$.

## References
