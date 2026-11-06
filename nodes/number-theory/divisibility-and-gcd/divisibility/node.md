---
tag: 2XV39G
kind: definition
slug: divisibility
name: Divisibility
aliases:
- divides relation
- a divides b
area: number-theory/divisibility-and-gcd
level: intro
summary: An integer a divides b when b = ka for some integer k; the foundation of the area.
prereqs: []
see_also: [divisor, greatest-common-divisor, least-common-multiple, coprime-integers, prime-number, congruence, divisibility-tests, euclids-lemma]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (divisibility and divisors, the division theorem, remainders and equivalence classes)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.1, Divisibility (the definition with m > 0)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 1, Section 1.1, Divisibility of integers
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.2, Divisibility (the basic properties)
---

Divisibility is the relation between two integers that says one of them is an integer multiple of the other: $a$ divides $b$, written $a \mid b$, when $b = ka$ for some integer $k$. It is the starting point of elementary number theory: the [divisors](/divisor/) of a number, the [greatest common divisor](/greatest-common-divisor/), [prime numbers](/prime-number/) and [congruences](/congruence/) are all defined from it. On a computer, $a \mid b$ for $a \ne 0$ is the test "the remainder of $b$ divided by $a$ is zero".

## Definition

Let $a$ and $b$ be integers. Then $a$ **divides** $b$, written $a \mid b$, if there is an integer $k$ such that

$$b = k a.$$

We then say that $a$ is a **divisor** (or factor) of $b$, and that $b$ is a **multiple** of $a$. If no such $k$ exists, we write $a \nmid b$.

The definition puts no condition on the sign of $a$ or $b$, and it allows zero. Three cases follow at once from it:

- $a \mid 0$ for each integer $a$, with $k = 0$.
- $0 \mid b$ if and only if $b = 0$, because $k \cdot 0 = 0$ for each $k$.
- $1 \mid b$ and $-1 \mid b$ for each $b$, with $k = b$ and $k = -b$.

Signs do not matter: $a \mid b$ if and only if $|a| \mid |b|$, because $b = ka$ gives $|b| = |k| \, |a|$, and $|b| = k'|a|$ gives $b = (\pm k') a$ for a suitable sign. So most statements about divisibility can be proved for non-negative integers only.

Some books restrict the definition. *Concrete Mathematics* (Section 4.1) defines $m \mid n$ only when $m > 0$. With that convention $0 \mid n$ is false for every $n$, including $n = 0$. This site uses the definition above, so $0 \mid 0$ is true and $0 \mid b$ is false for $b \ne 0$.

### The division theorem

The link between divisibility and arithmetic is division with remainder.

**Theorem (division theorem).** For each integer $b$ and each integer $a > 0$ there is exactly one pair of integers $q, r$ with $b = qa + r$ and $0 \le r < a$. Then $a \mid b$ if and only if $r = 0$.

*Proof.* Existence: the set $S = \{ b - qa : q \in \mathbb{Z} \}$ has non-negative elements, for example $b + |b| a \ge 0$ (take $q = -|b|$). By the well-ordering of the non-negative integers, $S$ has a least non-negative element $r = b - qa$. If $r \ge a$, then $r - a = b - (q+1)a$ is a smaller non-negative element of $S$, which is false. So $0 \le r < a$. Uniqueness: if $qa + r = q'a + r'$ with both remainders in $[0, a)$, then $(q - q')a = r' - r$ and $|r' - r| < a$. A multiple of $a$ with absolute value less than $a$ is $0$, so $r = r'$ and $q = q'$. Last claim: if $r = 0$ then $b = qa$. Conversely, if $b = ka$, then $(k, 0)$ is a pair with the two conditions, and by uniqueness $r = 0$. $\square$

We write $q = \lfloor b / a \rfloor$ and $r = b \bmod a$. For $a < 0$, the test $a \mid b$ is the test $|a| \mid b$.

### Basic properties

For all integers $a$, $b$, $c$, $x$, $y$:

1. **Reflexive.** $a \mid a$, with $k = 1$.
2. **Transitive.** If $a \mid b$ and $b \mid c$, then $a \mid c$. From $b = ka$ and $c = lb$ we get $c = (lk)a$.
3. **Linear combinations.** If $a \mid b$ and $a \mid c$, then $a \mid bx + cy$. From $b = ka$ and $c = la$ we get $bx + cy = (kx + ly) a$.
4. **Size.** If $a \mid b$ and $b \ne 0$, then $|a| \le |b|$. From $b = ka$ with $k \ne 0$ we get $|k| \ge 1$, so $|b| = |k| \, |a| \ge |a|$.
5. **Antisymmetry up to sign.** If $a \mid b$ and $b \mid a$, then $a = \pm b$. If $b = 0$, then $a = 0$ because $0 \mid a$ forces $a = 0$. Else both are non-zero, and property 4 gives $|a| \le |b| \le |a|$.
6. **Products.** If $a \mid b$, then $ac \mid bc$. If $c \ne 0$ and $ac \mid bc$, then $a \mid b$, because $bc = kac$ and $c \ne 0$ give $b = ka$.

Property 3 is the one that most proofs use. For example, if $d$ divides $a$ and $b$, then $d$ divides $a - qb = a \bmod b$. This is the core of the [Euclidean algorithm](/euclidean-algorithm/).

By properties 1, 2 and 5, divisibility is a partial order on the non-negative integers. In this order $1$ is the least element and $0$ is the greatest element, because each integer divides $0$. Each two elements $a, b$ have a greatest lower bound, $\gcd(a, b)$, and a least upper bound, $\operatorname{lcm}(a, b)$. On all of $\mathbb{Z}$ the relation is only a preorder, because $3 \mid -3$ and $-3 \mid 3$ but $3 \ne -3$.

### Testing divisibility in code

For machine integers and $a \ne 0$, the test is `b % a == 0`. It is correct in each language, whether `%` rounds the quotient toward zero (C, Java, Go) or toward minus infinity (Python), because the remainder is zero in both conventions exactly when $a \mid b$. The case $a = 0$ needs its own branch: the answer is "$b = 0$", and `b % 0` is an error. In C and C++, `INT_MIN % -1` is undefined behaviour, because the quotient overflows, although $-1$ divides every integer. For large numbers, see [divisibility tests](/divisibility-tests/) for digit rules by small divisors.

## Examples and non-examples

| $a$ | $b$ | $a \mid b$? | reason |
|---|---|---|---|
| 3 | 12 | yes | $12 = 4 \cdot 3$ |
| $-3$ | 12 | yes | $12 = (-4)(-3)$ |
| 12 | 3 | no | $3 = 0 \cdot 12 + 3$, remainder 3; also $|12| > |3|$ |
| 4 | 6 | no | $6 = 1 \cdot 4 + 2$ |
| 7 | 0 | yes | $0 = 0 \cdot 7$ |
| 0 | 5 | no | $k \cdot 0 = 0 \ne 5$ for each $k$ |
| 0 | 0 | yes | $0 = 1 \cdot 0$ |
| 1 | $-91$ | yes | $-91 = (-91) \cdot 1$ |
| 7 | 91 | yes | $91 = 13 \cdot 7$ |
| 6 | 91 | no | $91 = 15 \cdot 6 + 1$ |

**Transitivity.** $3 \mid 6$ and $6 \mid 42$, so $3 \mid 42$. Two divisors of the same number need not divide each other: $4 \mid 12$ and $6 \mid 12$, but $4 \nmid 6$ and $6 \nmid 4$.

**Linear combinations.** $7 \mid 91$ and $7 \mid 35$, so $7 \mid 91 \cdot 2 - 35 \cdot 5 = 7$, and also $7 \mid 91 - 2 \cdot 35 = 21$.

**Non-example of a "cancellation" rule.** $6 \mid 4 \cdot 9 = 36$, but $6 \nmid 4$ and $6 \nmid 9$. A divisor of a product need not divide a factor. [Euclid's lemma](/euclids-lemma/) says that this cannot happen when the divisor is prime.

**In other rings.** The same definition works in any commutative ring. In the Gaussian integers $\mathbb{Z}[i]$, $1 + i \mid 2$ because $2 = (1 + i)(1 - i)$, so $2$ is not prime there. The page [Euclidean domain](/euclidean-domain/) covers the rings where a division with remainder exists. For polynomials, $x - 1 \mid x^2 - 1$ because $x^2 - 1 = (x + 1)(x - 1)$.

## Related definitions

- [Divisor](/divisor/): the divisors of $n$, proper divisors, and the number of divisors.
- [Greatest common divisor](/greatest-common-divisor/) and [least common multiple](/least-common-multiple/): the meet and the join in the divisibility order.
- [Coprime integers](/coprime-integers/): pairs with no common divisor other than $\pm 1$.
- [Prime number](/prime-number/): an integer $p > 1$ whose only positive divisors are $1$ and $p$.
- [Congruence](/congruence/): $a \equiv b \pmod m$ means $m \mid a - b$.
- [Divisibility tests](/divisibility-tests/): digit rules that decide $d \mid n$ for small $d$.
- [Euclid's lemma](/euclids-lemma/) and the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/): the structure of divisibility through primes.
- [Integer division](/integer-division/): the computation of the quotient and the remainder.

## References
