---
tag: C8F0NW
kind: theorem
slug: hensel-lemma
name: Hensel's lemma
aliases:
- Hensel lemma
- Hensel lifting lemma
- Hensel's lifting lemma
area: algebra/polynomial-arithmetic
level: advanced
summary: A simple root modulo p lifts uniquely to a root modulo p^k for every k.
prereqs: [polynomial, monic-polynomial, factor-theorem, newton-iteration, extended-euclidean-algorithm]
see_also: [hensel-lifting, zassenhaus-algorithm, polynomial-factorization-over-integers, dixon-p-adic-lifting, newton-power-series-inversion, tonelli-shanks, chinese-remainder-theorem, irreducible-polynomial]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 15.4, Hensel lifting (the Hensel step for a factorization and the uniqueness of the lifted factors); Section 9.4, Solving polynomial equations via Newton iteration
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.5.3, Factorization modulo p^e, Hensel's lemma
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of polynomials (Hensel's lemma in the factorization over the integers)
---

Hensel's lemma says that a solution of a polynomial congruence modulo a prime $p$ can be lifted to a solution modulo $p^2$, $p^4$, $p^8$, and so on, when it is simple: the derivative there is not divisible by $p$. The lifted solution is unique, and each lift is one step of Newton's method done in modular arithmetic, so the exponent doubles at each step. The same holds for a factorization $f \equiv gh \pmod p$ into coprime factors. This is the base of the modular methods that factor polynomials over $\mathbb{Z}$, solve linear systems over $\mathbb{Q}$, and find square roots modulo prime powers.

Notation: $p$ is a prime, $k \ge 1$, and $a \equiv b \pmod{m}$ for polynomials means that every coefficient of $a - b$ is a multiple of $m$. For a commutative ring $R$ and $m \in R$, congruence modulo $m$ means that the difference lies in $m R[x]$. A polynomial is monic if its leading coefficient is $1$.

## Statement

**Theorem 1 (root form).** Let $f \in \mathbb{Z}[x]$ and $a \in \mathbb{Z}$ with $f(a) \equiv 0 \pmod p$ and $f'(a) \not\equiv 0 \pmod p$. Then for every $k \ge 1$ there is exactly one $b$ modulo $p^k$ with $b \equiv a \pmod p$ and $f(b) \equiv 0 \pmod{p^k}$. Moreover, if $f(b) \equiv 0 \pmod{p^j}$ and $b \equiv a \pmod p$, then $f'(b)$ is a unit modulo $p^j$, and with $u \equiv f'(b)^{-1} \pmod{p^j}$,

$$b' = b - f(b)\, u \bmod p^{2j} \quad \text{satisfies} \quad f(b') \equiv 0 \pmod{p^{2j}}, \quad b' \equiv b \pmod{p^j}.$$

**Theorem 2 (factor form, one Hensel step).** Let $R$ be a commutative ring and $m \in R$. Let $f, g, h, s, t \in R[x]$ with $h$ monic, $f \equiv g h \pmod m$ and $s g + t h \equiv 1 \pmod m$. Let $e = f - gh$, divide $s e$ by $h$ with remainder, $s e = q h + r$ with $\deg r < \deg h$, and set

$$g^* = g + t e + q g, \qquad h^* = h + r.$$

Then $f \equiv g^* h^* \pmod{m^2}$, $g^* \equiv g$ and $h^* \equiv h \pmod m$, and $h^*$ is monic of degree $\deg h$. Further, with $b = s g^* + t h^* - 1$ and $s b = c h^* + d$, $\deg d < \deg h^*$, the polynomials $s^* = s - d$ and $t^* = t - t b - c g^*$ satisfy $s^* g^* + t^* h^* \equiv 1 \pmod{m^2}$.

**Theorem 3 (uniqueness).** Let $f, g_1, h_1, g_2, h_2 \in \mathbb{Z}[x]$ with $h_1, h_2$ monic of the same degree, $f \equiv g_1 h_1 \equiv g_2 h_2 \pmod{p^k}$, $g_1 \equiv g_2$ and $h_1 \equiv h_2 \pmod p$, and $g_1 \bmod p$, $h_1 \bmod p$ coprime in $(\mathbb{Z}/p\mathbb{Z})[x]$. Then $g_1 \equiv g_2$ and $h_1 \equiv h_2 \pmod{p^k}$.

## In plain words

Suppose a number solves a polynomial equation if you only look at remainders after division by seven. Hensel's lemma says you can correct it so that it also works for remainders after division by forty-nine, then by seven to the fourth power, and so on, as long as the slope of the polynomial at that number is not a multiple of seven. The correction is the same as one step of Newton's method for finding roots, and each step doubles the number of correct digits in base seven. There is only one correction that works. The same idea lifts a splitting of a polynomial into two parts that share no factor.

## Proof

*Proof of Theorem 1.* **Taylor expansion.** For integers $b$ and $y$, $f(b + y) = f(b) + f'(b)\, y + y^2 W$ for an integer $W$, because $(b + y)^i = b^i + i b^{i-1} y + y^2 \sum_{l \ge 2} \binom{i}{l} b^{i-l} y^{l-2}$ and the binomial coefficients are integers.

**The step.** Since $b \equiv a \pmod p$, $f'(b) \equiv f'(a) \not\equiv 0 \pmod p$, so $f'(b)$ is prime to $p$ and has an inverse $u$ modulo $p^j$. Let $y = -f(b)\, u$. As $p^j$ divides $f(b)$, it divides $y$, so $p^{2j}$ divides $y^2 W$. Hence $f(b + y) \equiv f(b) - f'(b) f(b) u = f(b)(1 - f'(b) u) \pmod{p^{2j}}$. Both $f(b)$ and $1 - f'(b) u$ are multiples of $p^j$, so $f(b + y) \equiv 0 \pmod{p^{2j}}$. Reducing $b + y$ modulo $p^{2j}$ gives $b'$, and $b' \equiv b \pmod{p^j}$ because $p^j$ divides $y$.

**Existence.** Start with $b = a$ and $j = 1$, and apply the step until $2^i \ge k$. The result $b$ has $f(b) \equiv 0 \pmod{p^{2^i}}$, hence modulo $p^k$, and $b \equiv a \pmod p$.

**Uniqueness.** Let $b, c$ both satisfy the conditions modulo $p^k$. We show $b \equiv c \pmod{p^j}$ for $j = 1, \ldots, k$ by induction. For $j = 1$ both are $\equiv a$. If $j < k$ and $c = b + p^j z$, the Taylor expansion gives $0 \equiv f(c) - f(b) = f'(b) p^j z + p^{2j} z^2 W \pmod{p^{j+1}}$. Since $2j \ge j + 1$, this is $p^j f'(b) z \equiv 0 \pmod{p^{j+1}}$, so $p$ divides $f'(b) z$. As $p$ does not divide $f'(b)$, $p$ divides $z$, and $b \equiv c \pmod{p^{j+1}}$. $\square$

*Proof of Theorem 2.* **Division is linear.** Division with remainder by the monic $h$ is defined over any commutative ring, and the map $a \mapsto (q, r)$ is $R$-linear, since the quotient and remainder of $a_1 + c a_2$ are the sums of those of $a_1$ and $c$ times those of $a_2$, by uniqueness of division by a monic polynomial. So if $a \equiv 0 \pmod m$, then $q \equiv 0$ and $r \equiv 0 \pmod m$.

**The factors.** We have $e \equiv 0 \pmod m$, so $s e \equiv 0$, and by linearity $q \equiv r \equiv 0 \pmod m$. Hence $g^* \equiv g$, $h^* \equiv h \pmod m$, and $h^* = h + r$ is monic of degree $\deg h$ since $\deg r < \deg h$. Expanding, and using $g r + g q h = g s e$,

$$f - g^* h^* = e - g r - t e h - q g h - (t e + q g) r = e\,(1 - s g - t h) - (t e + q g)\, r.$$

The first product has two factors that are $\equiv 0 \pmod m$, and so has the second, since $t e + q g \equiv 0$ and $r \equiv 0 \pmod m$. So $f \equiv g^* h^* \pmod{m^2}$.

**The cofactors.** Now $b = s g^* + t h^* - 1 \equiv s g + t h - 1 \equiv 0 \pmod m$. Then

$$s^* g^* + t^* h^* = s g^* + t h^* - d g^* - t b h^* - c g^* h^* = 1 + b - t b h^* - g^* (d + c h^*) = 1 + b - b\,(t h^* + s g^*) = 1 - b^2,$$

using $d + c h^* = s b$. Since $b \equiv 0 \pmod m$, $1 - b^2 \equiv 1 \pmod{m^2}$. $\square$

*Proof of Theorem 3.* Let $s, t \in \mathbb{Z}[x]$ with $s g_1 + t h_1 \equiv 1 \pmod p$; they exist by the extended Euclidean algorithm in $(\mathbb{Z}/p\mathbb{Z})[x]$, as the reductions are coprime. We show $g_1 \equiv g_2$, $h_1 \equiv h_2 \pmod{p^j}$ for $j = 1, \ldots, k$ by induction; $j = 1$ is given. Let $j < k$, $g_2 = g_1 + p^j u$ and $h_2 = h_1 + p^j v$ with $u, v \in \mathbb{Z}[x]$. Since $h_1, h_2$ are monic of the same degree, $\deg v < \deg h_1$. From $g_1 h_1 \equiv g_2 h_2 \pmod{p^k}$, $p^j (u h_1 + g_1 v) + p^{2j} u v \equiv 0 \pmod{p^k}$, and since $2j \ge j + 1$ and $j + 1 \le k$, $p^j(u h_1 + g_1 v) \equiv 0 \pmod{p^{j+1}}$. Dividing by $p^j$, $u h_1 + g_1 v \equiv 0 \pmod p$. Then modulo $p$,

$$v \equiv v (s g_1 + t h_1) = s (g_1 v) + t h_1 v \equiv -s u h_1 + t h_1 v = h_1 (t v - s u).$$

So $h_1$ divides $v$ in $(\mathbb{Z}/p\mathbb{Z})[x]$. As $h_1 \bmod p$ is monic of degree greater than $\deg v$, a nonzero multiple of it has degree at least $\deg h_1$, so $v \equiv 0 \pmod p$. Then $u h_1 \equiv 0 \pmod p$, and a monic polynomial is not a zero divisor, so $u \equiv 0 \pmod p$. Hence $g_1 \equiv g_2$ and $h_1 \equiv h_2 \pmod{p^{j+1}}$. $\blacksquare$

## Consequences

- **Example.** For $f = x^2 - 2$ and $p = 7$, $a = 3$ is a root modulo $7$ with $f'(3) = 6 \not\equiv 0$. The step with $u = 6^{-1} \equiv 6 \pmod 7$ gives $b = 3 - 7 \cdot 6 \equiv 10 \pmod{49}$, and $10^2 = 2 \cdot 49 + 2$. The next step with $u = 20^{-1} \equiv 27 \pmod{49}$ gives $2166 \pmod{7^4}$. Among all residues modulo $7^4$, the roots of $x^2 - 2$ are $235$ and $2166$, and only $2166 \equiv 3 \pmod 7$, as uniqueness says. A script checked these numbers.
- **The Hensel lifting algorithm.** Theorem 2 with $m = p^{2^i}$, applied again and again, lifts a factorization modulo $p$ to one modulo $p^k$ in $\lceil \log_2 k \rceil$ steps. This is [Hensel lifting](/hensel-lifting/), used by the [Zassenhaus algorithm](/zassenhaus-algorithm/) for [factoring over the integers](/polynomial-factorization-over-integers/).
- **$p$-adic roots.** The lifts $b \bmod p^k$ for all $k$ form one $p$-adic integer, a root of $f$ in $\mathbb{Z}_p$. So a simple root modulo $p$ is the shadow of exactly one $p$-adic root.
- **Square roots modulo $p^k$.** For odd $p$ and $c$ prime to $p$, a square root of $c$ modulo $p$, found for example by [Tonelli-Shanks](/tonelli-shanks/), lifts to exactly one square root modulo $p^k$ in each residue class, since $f'(a) = 2a \not\equiv 0$. With the [Chinese remainder theorem](/chinese-remainder-theorem/), this gives square roots modulo any odd number whose factors are known.
- **Inverses and linear systems.** For $f = c x - 1$ the step is Newton's iteration for $1/c$, and the same idea lifts a solution of $A x \equiv v \pmod p$ to $p$-adic precision in [Dixon's method](/dixon-p-adic-lifting/).
- **Power series.** With $m = x$ in $R[x]$, $m^{2j} = x^{2j}$, and Theorem 1 becomes [Newton iteration for power series](/newton-power-series-inversion/): precision doubles at each step.

## Tightness

- **The derivative condition is needed.** For $f = x^2 - 7$, $p = 7$ and $a = 0$, $f(0) \equiv 0$ but $f'(0) = 0$. No $b \equiv 0 \pmod 7$ has $b^2 \equiv 7 \pmod{49}$, since then $49$ divides $b^2$. So existence fails.
- **Uniqueness also fails without it.** For $f = x^2$ and $a = 0$, every $b \in \{0, 7, 14, \ldots, 42\}$ satisfies $b^2 \equiv 0 \pmod{49}$: seven lifts instead of one.
- **A weaker condition can still work.** For $f = x^2 - 17$ and $p = 2$, $f'(a)$ is always even, yet $x^2 \equiv 17 \pmod{2^6}$ has the four roots $9, 23, 41, 55$. The general form of the lemma asks only that $f(a) \equiv 0 \pmod{p^{2v + 1}}$, where $p^v$ is the largest power of $p$ dividing $f'(a)$; here $v = 1$ and $f(1) = -16$.
- **Coprimality in the factor form is needed.** $x^2 - 7 \equiv x \cdot x \pmod 7$ with factors that are not coprime, and no factorization $(x - b)(x - c)$ with $b \equiv c \equiv 0 \pmod 7$ is $\equiv x^2 - 7 \pmod{49}$, since $bc \equiv 0 \pmod{49}$.
- **The doubling is the most one step gives.** In general $f(b') \not\equiv 0 \pmod{p^{2j+1}}$. In the example, $f(10) = 98$ is divisible by $49$ but not by $7^3$.

## History

Kurt Hensel introduced the $p$-adic numbers around 1900, and the lifting lemma appears in his book on algebraic numbers of 1908. Hans Zassenhaus made the quadratic version of the lemma the core of an algorithm in 1969, when he combined [Berlekamp's factorization](/berlekamp-factorization/) modulo $p$ with Hensel lifting to factor polynomials over $\mathbb{Z}$. Since then the lemma has been a standard tool of computer algebra, presented in von zur Gathen and Gerhard, Section 15.4, and in Cohen, Section 3.5.3.

## References
