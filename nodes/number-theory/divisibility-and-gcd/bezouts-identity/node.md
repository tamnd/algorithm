---
tag: 0J1WZZ
kind: theorem
slug: bezouts-identity
name: Bézout's identity
aliases:
- Bezout's lemma
area: number-theory/divisibility-and-gcd
level: core
summary: There exist integers x, y with ax + by = gcd(a, b).
prereqs: [greatest-common-divisor, divisibility, well-ordering-principle]
see_also: [extended-euclidean-algorithm, euclids-lemma, coprime-integers, modular-inverse, linear-diophantine-equation, chinese-remainder-theorem, euclidean-domain]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1 (the theorem that gcd(a, b) is the smallest positive element of the set of linear combinations, and its corollaries) and Section 31.2 (EXTENDED-EUCLID)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.3, Greatest common divisor
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition
    locator: Chapter 1, Section 1.1 (unique factorization in Z, the ideal (a, b) = (d)) and Section 1.3 (principal ideal domains)
  - url: "https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity"
    locator: Wikipedia, Bézout's identity (the sections on the structure of solutions and on history, Bachet 1624 and Bézout 1779)
---

Bézout's identity says that the [greatest common divisor](/greatest-common-divisor/) of two integers is an integer combination of them: for integers $a$ and $b$ there are integers $x$ and $y$ with $ax + by = \gcd(a, b)$. Better, $\gcd(a, b)$ is the smallest positive value of $ax + by$, and the values of $ax + by$ are exactly the multiples of $\gcd(a, b)$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) finds $x$ and $y$ in $O(\log \min(|a|, |b|))$ division steps. The identity is the tool behind [Euclid's lemma](/euclids-lemma/), [modular inverses](/modular-inverse/), [linear Diophantine equations](/linear-diophantine-equation/) and the [Chinese remainder theorem](/chinese-remainder-theorem/).

## Statement

**Theorem.** Let $a$ and $b$ be integers, not both zero, and let $L = \{ ax + by : x, y \in \mathbb{Z} \}$ be the set of their integer linear combinations. Then:

1. $\gcd(a, b)$ is the smallest positive element of $L$. In particular there are integers $x, y$ with $ax + by = \gcd(a, b)$.
2. $L = \gcd(a, b) \, \mathbb{Z}$, the set of all multiples of $\gcd(a, b)$.
3. For an integer $c$, the equation $ax + by = c$ has an integer solution if and only if $\gcd(a, b) \mid c$.

If $a = b = 0$, then $L = \{0\}$, $\gcd(0, 0) = 0$, and statements 2 and 3 still hold, with $0 \cdot \mathbb{Z} = \{0\}$. The integers $x, y$ are called **Bézout coefficients**. They are not unique.

The statement holds for all signs of $a$ and $b$, because $ax + by = |a| x' + |b| y'$ with $x' = \pm x$ and $y' = \pm y$.

## In plain words

Take two whole numbers, and add and subtract them as often as you like. For example, with 240 and 46 you can make 46, 240 minus 46, five times 46 minus 240, and so on. The theorem says which numbers you can make: exactly the multiples of the greatest common divisor, and nothing else. So the smallest positive number you can make is the greatest common divisor itself.

One direction is easy: each common divisor of the two numbers divides everything you make from them. The other direction is the real content: the greatest common divisor can always be made. The Euclidean algorithm, run backwards, shows how.

## Proof

**Proof of 1 by the well-ordering principle.** Let $S = L \cap \{1, 2, 3, \ldots\}$, the positive elements of $L$. The set $S$ is not empty: $a \cdot a + b \cdot b = a^2 + b^2 > 0$ is in it, because $a$ and $b$ are not both zero. By the [well-ordering principle](/well-ordering-principle/), $S$ has a least element $d = ax_0 + by_0$.

*$d$ divides $a$.* By the division theorem, $a = qd + r$ with $0 \le r < d$. Then $r = a - qd = a(1 - qx_0) + b(-qy_0)$ is in $L$. If $r > 0$, then $r \in S$ and $r < d$, against the choice of $d$. So $r = 0$ and $d \mid a$. The same argument with $b$ gives $d \mid b$.

*$d$ is the greatest common divisor.* Let $c$ be a common divisor of $a$ and $b$. Then $c$ divides $ax_0 + by_0 = d$, and since $d > 0$, $|c| \le d$. So $d$ is a common divisor and no common divisor is larger: $d = \gcd(a, b)$. Since $d \in S$, the integers $x_0, y_0$ give $ax_0 + by_0 = \gcd(a, b)$. $\square$

**Proof of 2.** Let $g = \gcd(a, b)$. Each element $ax + by$ of $L$ is a multiple of $g$, because $g \mid a$ and $g \mid b$. Conversely, by part 1, $g = ax_0 + by_0$, so $kg = a(kx_0) + b(ky_0) \in L$ for each integer $k$. $\square$

**Proof of 3.** The equation has a solution if and only if $c \in L$. By part 2, this holds if and only if $g \mid c$. $\square$

**A constructive proof of 1.** The proof above shows that $x$ and $y$ exist but does not find them. This second proof is the [extended Euclidean algorithm](/extended-euclidean-algorithm/). We show by strong induction on $b \ge 0$ that for each $a \ge 0$ there are $x, y$ with $ax + by = \gcd(a, b)$. If $b = 0$, take $x = 1$, $y = 0$: $a \cdot 1 = a = \gcd(a, 0)$. If $b > 0$, write $a = qb + r$ with $0 \le r < b$. By the induction hypothesis for the pair $(b, r)$, since $r < b$, there are $x', y'$ with $bx' + ry' = \gcd(b, r)$. By the [GCD recursion theorem](/gcd-recursion-theorem/), $\gcd(b, r) = \gcd(a, b)$. Substituting $r = a - qb$ gives

$$\gcd(a, b) = bx' + (a - qb)y' = a \, y' + b \, (x' - q y').$$

So $x = y'$ and $y = x' - qy'$ work. Negative inputs follow by changing the signs of the coefficients. $\blacksquare$

### Example

For $a = 240$ and $b = 46$, the Euclidean algorithm gives $240 = 5 \cdot 46 + 10$, $46 = 4 \cdot 10 + 6$, $10 = 1 \cdot 6 + 4$, $6 = 1 \cdot 4 + 2$, $4 = 2 \cdot 2$, so $\gcd(240, 46) = 2$. Back-substitution gives

$$2 = 6 - 4 = 6 - (10 - 6) = 2 \cdot 6 - 10 = 2(46 - 4 \cdot 10) - 10 = 2 \cdot 46 - 9 \cdot 10 = 2 \cdot 46 - 9(240 - 5 \cdot 46) = 240 \cdot (-9) + 46 \cdot 47.$$

Other coefficients are $(-9 + 23k, \ 47 - 120k)$ for each integer $k$, for example $(14, -73)$ and $(-32, 167)$. By part 3, $240x + 46y = 7$ has no integer solution, since $2 \nmid 7$, while $240x + 46y = 10$ has the solution $(-45, 235)$.

## Consequences

- **Coprimality.** $\gcd(a, b) = 1$ if and only if $ax + by = 1$ for some integers $x, y$. See [coprime integers](/coprime-integers/).
- **[Euclid's lemma](/euclids-lemma/).** If a prime $p$ divides $ab$ and $p \nmid a$, then $\gcd(p, a) = 1$, so $px + ay = 1$, and $b = pbx + aby$ is a multiple of $p$. This gives the uniqueness part of the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/).
- **Each common divisor divides the gcd.** If $c \mid a$ and $c \mid b$, then $c \mid ax + by = \gcd(a, b)$. So the gcd is the greatest common divisor also in the order of [divisibility](/divisibility/), not only in size.
- **[Modular inverse](/modular-inverse/).** If $\gcd(a, m) = 1$, then $ax + my = 1$ gives $ax \equiv 1 \pmod m$, so $x$ is the inverse of $a$ modulo $m$.
- **[Linear Diophantine equations](/linear-diophantine-equation/).** Part 3 decides solvability. If $(x_0, y_0)$ is one solution of $ax + by = c$ and $g = \gcd(a, b) > 0$, the solutions are exactly $(x_0 + k b/g, \ y_0 - k a/g)$ for $k \in \mathbb{Z}$: if $(x, y)$ is another solution, then $(a/g)(x - x_0) = -(b/g)(y - y_0)$, and since $a/g$ and $b/g$ are coprime, $b/g$ divides $x - x_0$.
- **Small coefficients.** For $a, b > 0$ there is exactly one solution of $ax + by = g$ with $0 \le x < b/g$, by the description of all solutions. For it, $|y| \le a/g$: from $y = (g - ax)/b$ and $0 \le ax \le a(b/g - 1)$ we get $-a/g < y \le g/b \le 1 \le a/g$. So Bézout coefficients fit in the size of the inputs.
- **The [Chinese remainder theorem](/chinese-remainder-theorem/).** For coprime moduli $m, n$ with $mx + ny = 1$, the number $c = a \, ny + b \, mx$ satisfies $c \equiv a \pmod m$ and $c \equiv b \pmod n$.
- **Several integers.** By induction on $k$, using $\gcd(a_1, \ldots, a_k) = \gcd(\gcd(a_1, \ldots, a_{k-1}), a_k)$, there are integers $x_i$ with $\sum a_i x_i = \gcd(a_1, \ldots, a_k)$.
- **Ideals.** In ring language, the ideal $a\mathbb{Z} + b\mathbb{Z}$ equals $\gcd(a, b)\mathbb{Z}$. So $\mathbb{Z}$ is a principal ideal domain. The same proof works in each [Euclidean domain](/euclidean-domain/), with the Euclidean function in place of the absolute value.

## Tightness

**Coefficients of both signs are needed.** With $a, b > 0$, at least one Bézout coefficient is $\le 0$, because $x, y \ge 1$ gives $ax + by \ge a + b > \gcd(a, b)$. A pair with both coefficients $\ge 0$ exists only when one of $a, b$ divides the other. With non-negative coefficients only, $3x + 5y$ takes the values $0, 3, 5, 6, 8, 9, 10, \ldots$ and misses $1, 2, 4, 7$. The largest number that is not a non-negative combination of coprime $a, b > 1$ is $ab - a - b$ (here $7$); this is the Frobenius coin problem for two coins.

**The identity fails in some rings.** In the ring $\mathbb{Z}[x]$ of polynomials with integer coefficients, $2$ and $x$ have no common divisor except $\pm 1$, so their gcd is $1$. But $2 f(x) + x g(x) = 1$ has no solution: the constant term of the left side is $2 f(0)$, which is even. So the identity needs a ring where each ideal generated by two elements is principal, such as $\mathbb{Z}$, polynomials over a field, or any [Euclidean domain](/euclidean-domain/).

**The bound on coefficients is tight up to a constant factor.** Let $a = F_{k+1}$ and $b = F_k$ be consecutive Fibonacci numbers, $k \ge 3$. Cassini's identity $F_{k+1}F_{k-1} - F_k^2 = (-1)^k$ gives the solution $x_0 = (-1)^k F_{k-1}$, $y_0 = (-1)^{k+1} F_k$. Every solution has $x \equiv x_0 \pmod{F_k}$, so $|x| \ge \min(F_{k-1}, F_k - F_{k-1}) = F_{k-2}$, which is about $0.38\,b$. For $(89, 55)$ the smallest $|x|$ is $21$. So the bound $|x| < b/g$ of the consequences cannot be improved by more than a constant factor.

## History

The statement for integers was given by Claude Gaspard Bachet de Méziriac in the second edition (1624) of his *Problèmes plaisans et délectables*, where he solved linear equations in integers by the method of the Euclidean algorithm. Étienne Bézout proved the analogous statement for polynomials in his *Théorie générale des équations algébriques* (1779), and the name of the theorem comes from that work.

## References
