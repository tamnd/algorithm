---
tag: C75AVS
kind: definition
slug: floor-division
name: Floor division
aliases:
- floored division
- ceiling division
area: algebra/integer-arithmetic
level: intro
summary: Rounds the quotient toward negative infinity, with the remainder taking the sign of the divisor.
prereqs: [division-with-remainder]
see_also: [division-with-remainder, integer-division, integer-overflow, twos-complement, floor-log2, congruence]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 3.1, Floors and ceilings, and Section 3.4, 'mod', the binary operation (x mod y = x - y floor(x/y), and its laws)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.4, Integer functions and elementary number theory
  - paper: doi:10.1145/128861.128862
    title: Raymond T. Boute, The Euclidean definition of the functions div and mod, ACM Transactions on Programming Languages and Systems 14(2), 1992
    locator: pp. 127 to 144 (the truncated, floored and Euclidean definitions and their laws)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2012
    locator: Chapter 9, Integer division (Section 9-1, preliminaries, the truncated, floored and modulus conventions, and the conversion between them)
---

Floor division is integer division in which the quotient of $a$ by $b \ne 0$ is $\lfloor a/b \rfloor$, the rational quotient rounded toward $-\infty$, and the remainder $a - b\lfloor a/b \rfloor$ has the sign of the divisor. It is the rule of the `//` and `%` operators of Python, of `div` and `mod` in Haskell, and of the binary operation mod in Concrete Mathematics. The related *ceiling division* rounds toward $+\infty$. Both differ from the truncated division of C, C++, Java and most processors, which rounds toward zero, exactly when the signs of $a$ and $b$ differ and $b$ does not divide $a$.

## Definition

Let $a, b \in \mathbb{Z}$ with $b \ne 0$.

**Floor division.** The *floored quotient* and *floored remainder* are

$$a \mathbin{//} b = \left\lfloor \frac{a}{b} \right\rfloor, \qquad a \bmod b = a - b \left\lfloor \frac{a}{b} \right\rfloor .$$

They satisfy $a = b \cdot (a \mathbin{//} b) + (a \bmod b)$, and

$$0 \le a \bmod b < b \ \text{ if } b > 0, \qquad b < a \bmod b \le 0 \ \text{ if } b < 0 .$$

*Proof of the bounds.* Let $q = \lfloor a/b \rfloor$, so $q \le a/b < q + 1$. If $b > 0$, multiply by $b$: $qb \le a < qb + b$, so $0 \le a - qb < b$. If $b < 0$, multiplying by $b$ reverses the inequalities: $qb \ge a > qb + b$, so $0 \ge a - qb > b$. $\blacksquare$

So the pair $(a \mathbin{//} b, a \bmod b)$ is the unique pair $(q, r)$ with $a = qb + r$ and $r$ in the half-open interval between 0 and $b$ that contains 0. For $b > 0$ it is the pair of [division with remainder](/division-with-remainder/).

**Ceiling division.** The ceiling quotient is $\lceil a/b \rceil$, with remainder $a - b\lceil a/b \rceil$, which has the sign opposite to $b$ or is zero. For all integers,

$$\left\lceil \frac{a}{b} \right\rceil = -\left\lfloor \frac{-a}{b} \right\rfloor ,$$

because $\lceil x \rceil = -\lfloor -x \rfloor$ for each real $x$. For $b > 0$ there is also $\lceil a/b \rceil = \lfloor (a + b - 1)/b \rfloor$. *Proof.* Write $a = qb + r$ with $0 \le r < b$. If $r = 0$, both sides are $q$, since $0 \le b - 1 < b$. If $r \ge 1$, then $\lceil a/b \rceil = q + 1$, and $a + b - 1 = (q + 1)b + (r - 1)$ with $0 \le r - 1 < b$, so the right side is $q + 1$ too. $\blacksquare$

**Truncated division, for comparison.** The truncated quotient is $\operatorname{trunc}(a/b)$, which is $\lfloor a/b \rfloor$ when $a/b \ge 0$ and $\lceil a/b \rceil$ when $a/b < 0$. Its remainder has the sign of $a$. If $q_t, r_t$ are the truncated pair, the floored pair is

$$(q_f, r_f) = \begin{cases} (q_t - 1,\ r_t + b) & \text{if } r_t \ne 0 \text{ and } \operatorname{sign}(r_t) \ne \operatorname{sign}(b), \\ (q_t,\ r_t) & \text{otherwise.} \end{cases}$$

This is how a program in C gets floor division from the `/` and `%` operators.

**Laws.** For $b \ne 0$ and each integer $k$:

- $(a + kb) \mathbin{//} b = a \mathbin{//} b + k$ and $(a + kb) \bmod b = a \bmod b$. So $a \bmod b$ depends only on the class of $a$ modulo $b$, which truncated division does not satisfy.
- $(-a) \mathbin{//} b = -(a \mathbin{//} b) - 1$ when $b \nmid a$, and $= -(a \mathbin{//} b)$ when $b \mid a$.
- $a \mathbin{//} 2^k$ equals the arithmetic right shift of $a$ by $k$ in [two's complement](/twos-complement/), for $k \ge 0$. A right shift rounds toward $-\infty$, not toward zero.
- For $c > 0$, $(a \mathbin{//} b) \mathbin{//} c = a \mathbin{//} (bc)$ when $b > 0$. The proof is $\lfloor \lfloor x \rfloor / c \rfloor = \lfloor x / c \rfloor$ for real $x$ and a positive integer $c$ (Concrete Mathematics, Section 3.2).

## Examples and non-examples

The table compares the three rules. Each row satisfies $a = qb + r$.

| $a$ | $b$ | floor $q$, $r$ | ceiling $q$, $r$ | truncated $q$, $r$ |
|---|---|---|---|---|
| 17 | 5 | 3, 2 | 4, $-3$ | 3, 2 |
| $-17$ | 5 | $-4$, 3 | $-3$, $-2$ | $-3$, $-2$ |
| 17 | $-5$ | $-4$, $-3$ | $-3$, 2 | $-3$, 2 |
| $-17$ | $-5$ | 3, $-2$ | 4, 3 | 3, $-2$ |
| $-1$ | 5 | $-1$, 4 | 0, $-1$ | 0, $-1$ |
| 10 | 5 | 2, 0 | 2, 0 | 2, 0 |

**Examples in code.**

- In Python, `-17 // 5` is `-4` and `-17 % 5` is `3`. Also `-7 >> 1` is `-4`, the same as `-7 // 2`.
- In C99 and Java, `-17 / 5` is `-3` and `-17 % 5` is `-2`.
- Splitting $n = 23$ items into pages of $b = 5$ needs $\lceil 23/5 \rceil = \lfloor 27/5 \rfloor = 5$ pages. In Python, `-(-23 // 5)` is also 5.
- The day of the week $k$ days before a Monday (day 0) is $(-k) \bmod 7$ with the floored rule: for $k = 1$ it is 6, a Sunday. The truncated rule gives $-1$, which is not a valid index.

**Non-examples.**

- `(a + b - 1) // b` is not the ceiling for $b < 0$: for $a = 7$ and $b = -2$ it gives $4 // (-2) = -2$, while $\lceil 7/(-2) \rceil = \lceil -3.5 \rceil = -3$.
- In a fixed-width type, `(a + b - 1) / b` can overflow: with 32-bit signed integers and $a = 2^{31} - 1$, $a + b - 1$ does not fit for $b \ge 2$. The form `a / b + (a % b != 0)` for $a \ge 0$, $b > 0$ avoids it ([integer overflow](/integer-overflow/)).
- The floored remainder of $-17$ by $5$ is 3, not $-2$: a program that tests `x % 2 == 1` for odd numbers fails on negative $x$ in C (the result is $-1$), but works in Python.

## Related definitions

- [Division with remainder](/division-with-remainder/): the Euclidean rule $0 \le r < |b|$, equal to floor division when $b > 0$.
- Truncated division: rounds toward zero; the rule of C, C++, Java, Rust and processor division instructions.
- [Integer division](/integer-division/): the algorithms that compute the quotient and remainder of large numbers.
- [Two's complement](/twos-complement/): the arithmetic right shift is floor division by a power of two.
- [Floor of log2](/floor-log2/): $\lfloor \log_2 n \rfloor$, the position of the highest set bit, another floor function on integers.
- [Congruence](/congruence/): $a \equiv a' \pmod b$ exactly when $a \bmod b = a' \bmod b$ under the floored or the Euclidean rule.

## References
