---
tag: V5QGYN
kind: definition
slug: square-free-polynomial
name: Square-free polynomial
aliases:
- squarefree polynomial
- square-free part
area: algebra/polynomial-arithmetic
level: core
summary: Polynomial with no repeated irreducible factor; equivalently gcd(f, f') is constant.
prereqs: [polynomial-gcd, irreducible-polynomial]
see_also: [square-free-factorization, yun-square-free-factorization, multiplicity-of-roots, discriminant, polynomial-gcd, distinct-degree-factorization, primitive-polynomial, square-free-word]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 9.3, Formal derivatives (p. 265), and Section 14.6, Squarefree factorization (p. 393; square-free polynomials, gcd(f, f') and the case of finite fields)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (squarefree polynomials and the gcd with the derivative)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 13.5, Separable and inseparable extensions (the derivative criterion for multiple roots and perfect fields)
---

A polynomial over a field is square-free when no irreducible factor appears in it twice, that is, when it is not divisible by the square of any polynomial of positive degree. Over the rationals, the reals and every finite field, this holds exactly when $\gcd(f, f') = 1$, so it can be tested with one [gcd](/polynomial-gcd/) and no factoring. Most factoring and root-isolation algorithms assume a square-free input and get it by [square-free factorization](/square-free-factorization/). Over a field that is not perfect the derivative test can fail, and the definition and the test must be kept apart.

## Definition

Let $F$ be a field and $f \in F[x]$ nonzero.

**Square-free.** $f$ is *square-free* if there is no $g \in F[x]$ with $\deg g \ge 1$ and $g^2 \mid f$. Since $F[x]$ has unique factorization, this means that in $f = c\, p_1^{e_1} \cdots p_k^{e_k}$, with distinct monic [irreducible](/irreducible-polynomial/) $p_i$ and $c \in F^\times$, every $e_i$ is $1$. Constants are square-free.

**Square-free part.** The *square-free part* (or *radical*) of $f$ is $\operatorname{sqf}(f) = p_1 p_2 \cdots p_k$, the product of the distinct monic irreducible factors.

**Perfect field.** $F$ is *perfect* if it has characteristic $0$, or characteristic $p$ and every element of $F$ is a $p$-th power. Finite fields are perfect, since $a \mapsto a^p$ is injective on a finite field and so onto.

**Derivative criterion.** Let $f'$ be the formal derivative.

1. If $\gcd(f, f') = 1$, then $f$ is square-free, over every field.
2. If $F$ is perfect and $f$ is square-free, then $\gcd(f, f') = 1$.
3. If $F$ has characteristic $0$, then $\operatorname{sqf}(f) = f / \gcd(f, f')$ up to a constant factor.

*Proof.* (1) If $f = g^2 h$, then $f' = 2 g g' h + g^2 h' = g\,(2 g' h + g h')$, so $g$ divides $\gcd(f, f')$, and $\deg g \ge 1$.

(2) Let $p$ be an irreducible factor of $\gcd(f, f')$ and write $f = p u$. Then $f' = p' u + p u'$, so $p \mid p' u$. First, $p' \ne 0$: otherwise the characteristic is a prime $\ell$ and $p = \sum_i a_i x^{i\ell}$; since $F$ is perfect, $a_i = b_i^{\ell}$, and $p = (\sum_i b_i x^i)^{\ell}$, which is not irreducible. As $\deg p' < \deg p$, $p \nmid p'$. Since $p$ is irreducible, hence prime in $F[x]$, $p \mid u$, and $p^2 \mid f$. So if $f$ is square-free, no such $p$ exists and $\gcd(f, f') = 1$.

(3) Write $f = c \prod p_i^{e_i}$. In characteristic $0$, $p_i' \ne 0$ and $e_i \ne 0$ in $F$. The product rule gives $f' = c \sum_i e_i p_i^{e_i - 1} p_i' \prod_{j \ne i} p_j^{e_j}$. Each $p_i^{e_i - 1}$ divides every term. $p_i^{e_i}$ divides every term except the $i$-th, and does not divide the $i$-th term, because $p_i \nmid e_i p_i' \prod_{j \ne i} p_j^{e_j}$. So the exact power of $p_i$ in $f'$ is $e_i - 1$, and $\gcd(f, f') = \prod p_i^{e_i - 1}$ up to a constant. Dividing $f$ by it leaves $c \prod p_i$. $\square$

**Over $\mathbb{Z}$.** For $f \in \mathbb{Z}[x]$, one usually asks that $f$ be square-free in $\mathbb{Q}[x]$, or that its [primitive part](/primitive-polynomial/) be square-free in $\mathbb{Z}[x]$. The content can have square factors: $4x + 4 = 2^2 (x + 1)$ is not square-free in $\mathbb{Z}[x]$ but is square-free in $\mathbb{Q}[x]$.

## Examples and non-examples

- $x^2 - 1 = (x - 1)(x + 1)$ is square-free over $\mathbb{Q}$, and $\gcd(x^2 - 1, 2x) = 1$.
- $f = x^3 - x^2 - x + 1 = (x - 1)^2 (x + 1)$ is not square-free. Here $f' = 3x^2 - 2x - 1 = (3x + 1)(x - 1)$, $\gcd(f, f') = x - 1$, and $f / \gcd(f, f') = x^2 - 1$ is the square-free part.
- $x^2 + 1$ is square-free over $\mathbb{R}$; it has no real root, and the definition does not need roots.
- **Over $\mathbb{F}_3$.** $x^3 - x = x(x - 1)(x + 1)$ is square-free, and $f' = 3x^2 - 1 = -1$. But $x^3 + 1 = (x + 1)^3$ is not, and $f' = 3x^2 = 0$, so $\gcd(f, f') = f$: the gcd is $f$ itself, not $(x + 1)^2$, and the formula of fact 3 fails in characteristic $3$.
- **Over $\mathbb{F}_q$.** $x^q - x = \prod_{a \in \mathbb{F}_q} (x - a)$ is square-free, since its derivative is $-1$.
- **An imperfect field.** Over $F = \mathbb{F}_p(t)$, the field of rational functions, $f = x^p - t$ is irreducible, so square-free. But $f' = p x^{p-1} = 0$, so $\gcd(f, f') = f \ne 1$. Fact 2 needs a perfect field. In a splitting field, $f = (x - t^{1/p})^p$ has one root of multiplicity $p$.
- **How many are square-free.** Over $\mathbb{F}_q$, the number of monic square-free polynomials of degree $n \ge 2$ is exactly $q^n - q^{n-1}$, so a fraction $1 - 1/q$ of all monic ones. *Proof.* Every monic $f$ can be written in exactly one way as $f = a^2 b$ with $a, b$ monic and $b$ square-free (put the even part of each exponent into $a^2$). With $s_k$ the number of monic square-free polynomials of degree $k$, counting the monic $f$ of degree $n$ gives $q^n = \sum_{k \ge 0} q^k s_{n - 2k}$. In generating functions, $\frac{1}{1 - qT} = \frac{S(T)}{1 - qT^2}$, so $S(T) = \frac{1 - qT^2}{1 - qT}$ and $s_n = q^n - q \cdot q^{n-2}$ for $n \ge 2$. $\square$ For $q = 2$ and $n = 2, \ldots, 5$ this gives $2, 4, 8, 16$; for $q = 3$, $6, 18, 54, 162$.

## Related definitions

- **Multiple root.** For $f$ over a field $F$, an element $a$ of an extension field is a multiple root when $(x - a)^2 \mid f$, that is when $f(a) = f'(a) = 0$; see [multiplicity of roots](/multiplicity-of-roots/). Over a perfect field, $f$ is square-free exactly when it has no multiple root in an algebraic closure.
- **Separable polynomial.** $f$ is separable when it has no multiple root in an algebraic closure, which is the same as $\gcd(f, f') = 1$. Over a perfect field, separable and square-free are the same; over $\mathbb{F}_p(t)$, $x^p - t$ is square-free but not separable (Dummit and Foote, Section 13.5).
- **Discriminant.** For $\deg f \ge 1$, the [discriminant](/discriminant/) of $f$ is zero exactly when $f$ has a multiple root, so over a perfect field exactly when $f$ is not square-free.
- **Square-free factorization.** $f = c\, a_1 a_2^2 a_3^3 \cdots a_k^k$ with square-free, pairwise coprime $a_i$: see [square-free factorization](/square-free-factorization/) and [Yun's algorithm](/yun-square-free-factorization/).
- **Square-free integer.** An integer with no square prime factor. The polynomial notion is the analogue in $F[x]$, but, unlike for integers, the test needs no factoring, thanks to the derivative.

## References
