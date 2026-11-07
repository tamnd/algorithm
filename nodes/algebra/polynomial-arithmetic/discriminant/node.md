---
tag: M7Q1KE
kind: definition
slug: discriminant
name: Discriminant
aliases:
- discriminant of a polynomial
- polynomial discriminant
area: algebra/polynomial-arithmetic
level: advanced
summary: Resultant of a polynomial and its derivative; zero exactly when the polynomial has a repeated root.
prereqs: [polynomial, resultant, sylvester-matrix, factor-theorem]
see_also: [square-free-polynomial, square-free-factorization, multiplicity-of-roots, polynomial-gcd, zassenhaus-algorithm, hensel-lifting, eisenstein-criterion, vieta-formulas]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.3, The resultant; Section 14.6, Squarefree factorization; Section 15.2, A factoring algorithm (choice of a prime that keeps the polynomial squarefree)
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.3.2, Resultants and Discriminants
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition, Graduate Texts in Mathematics 211, Springer, 2002
    locator: Chapter IV, Polynomials (symmetric polynomials and the resultant)
---

The discriminant of a polynomial is a single element of the coefficient ring that is zero exactly when the polynomial has a repeated root. For $ax^2 + bx + c$ it is $b^2 - 4ac$. In general it is, up to a sign and a factor of the leading coefficient, the [resultant](/resultant/) of $f$ and its derivative, so it is a polynomial in the coefficients and can be computed without finding any root. Factoring algorithms use it to choose primes modulo which a squarefree integer polynomial stays squarefree.

## Definition

Let $R$ be a commutative ring with $1$ and let $f = \sum_{k=0}^{n} a_k x^k \in R[x]$ with $n \ge 1$ and $a_n \ne 0$. Let $f' = \sum_{k=1}^{n} k a_k x^{k-1}$ be the formal derivative, and let $\operatorname{Res}_{n, n-1}(f, f')$ be the determinant of the $(2n - 1) \times (2n - 1)$ [Sylvester matrix](/sylvester-matrix/) of $f$ and $f'$, where $f'$ is given its formal degree $n - 1$ even if $n a_n = 0$ in $R$.

Every entry of the first column of this matrix is $a_n$, $n a_n$ or $0$, so $a_n$ divides the determinant as a polynomial in the coefficients $a_0, \ldots, a_n$ over $\mathbb{Z}$. The **discriminant** of $f$ is the element

$$\operatorname{disc}(f) = (-1)^{n(n-1)/2}\, \frac{1}{a_n} \operatorname{Res}_{n, n-1}(f, f') \in R,$$

where the division is carried out in the polynomial identity over $\mathbb{Z}$ and then specialized to $R$, so no inverse of $a_n$ is needed.

**Root formula.** If $R$ is a field and $f = a_n \prod_{i=1}^{n} (x - \alpha_i)$ in a splitting field, then

$$\operatorname{disc}(f) = a_n^{2n-2} \prod_{1 \le i < j \le n} (\alpha_i - \alpha_j)^2.$$

*Derivation.* The resultant satisfies $\operatorname{Res}_{n, m}(f, g) = a_n^{m} \prod_i g(\alpha_i)$ for $g$ of formal degree $m$. Differentiating the product gives $f'(\alpha_i) = a_n \prod_{j \ne i} (\alpha_i - \alpha_j)$. So

$$\operatorname{Res}_{n, n-1}(f, f') = a_n^{n-1} \cdot a_n^{n} \prod_i \prod_{j \ne i} (\alpha_i - \alpha_j) = a_n^{2n-1} (-1)^{n(n-1)/2} \prod_{i < j} (\alpha_i - \alpha_j)^2,$$

because each pair $i < j$ appears twice, once as $\alpha_i - \alpha_j$ and once as $\alpha_j - \alpha_i = -(\alpha_i - \alpha_j)$, and there are $n(n-1)/2$ pairs. Multiplying by $(-1)^{n(n-1)/2} / a_n$ gives the formula.

**Main property.** Over a field $F$, $\operatorname{disc}(f) = 0$ exactly when $f$ has a repeated root in an algebraic closure of $F$, exactly when $\gcd(f, f')$ is not constant. The first equivalence is the root formula. For the second, $\alpha$ is a repeated root exactly when $f(\alpha) = f'(\alpha) = 0$, by the [factor theorem](/factor-theorem/) applied twice, and $f, f'$ have a common root exactly when their resultant is zero.

**Properties.** For $f$ as above:

1. **Specialization.** If $\varphi : R \to S$ is a ring homomorphism with $\varphi(a_n) \ne 0$, then $\operatorname{disc}(\varphi f) = \varphi(\operatorname{disc} f)$, because the discriminant is a fixed integer polynomial in the coefficients and $\varphi f$ has the same degree. In particular, for $f \in \mathbb{Z}[x]$ and a prime $p \nmid a_n$, $\operatorname{disc}(f \bmod p) = \operatorname{disc}(f) \bmod p$.
2. **Good primes.** If $f \in \mathbb{Z}[x]$ is squarefree, then $\operatorname{disc}(f) \ne 0$, and for every prime $p$ that divides neither $a_n$ nor $\operatorname{disc}(f)$, $f \bmod p$ is squarefree of the same degree. Only finitely many primes are bad.
3. **Invariance.** $\operatorname{disc}(f(x + c)) = \operatorname{disc}(f)$ for every $c$, and $\operatorname{disc}(c f) = c^{2n-2} \operatorname{disc}(f)$, both from the root formula.
4. **Products.** $\operatorname{disc}(fg) = \operatorname{disc}(f) \operatorname{disc}(g) \operatorname{Res}(f, g)^2$.
5. **Sign over the reals.** If $f \in \mathbb{R}[x]$ has no repeated root and $s$ pairs of nonreal conjugate roots, then $\operatorname{disc}(f)$ has the sign $(-1)^s$. Each conjugate pair gives $(\alpha - \bar\alpha)^2 = (2i \operatorname{Im} \alpha)^2 < 0$, and the other factors pair up into squares of real numbers or products $|z|^2 > 0$.
6. **Cost.** The resultant, and so the discriminant, can be computed over a field with $O(n^2)$ field operations by the Euclidean algorithm, or $O(M(n) \log n)$ by the fast Euclidean algorithm. Over $\mathbb{Z}$ the subresultant algorithm or a modular method avoids fractions.

## Examples and non-examples

All values below were checked with a script that computes the Sylvester determinant exactly.

- **Quadratic.** $\operatorname{disc}(ax^2 + bx + c) = b^2 - 4ac$. For $x^2 + x + 2$ it is $-7$, so the two roots are nonreal and distinct. For $x^2 + 1$ it is $-4$.
- **Cubic.** $\operatorname{disc}(ax^3 + bx^2 + cx + d) = b^2 c^2 - 4ac^3 - 4b^3 d - 27a^2 d^2 + 18abcd$, and for the depressed cubic $\operatorname{disc}(x^3 + px + q) = -4p^3 - 27q^2$.
- $x^3 - x - 1$ has discriminant $-23$. It has one real root and one pair of nonreal roots, which matches the sign $(-1)^1$. It is squarefree modulo every prime except $23$, and modulo $23$ it has a repeated root.
- $x^3 - 3x + 2 = (x - 1)^2 (x + 2)$ has discriminant $-4(-3)^3 - 27 \cdot 4 = 0$, as it must.
- $x^4 + 1$ has discriminant $256 = 2^8$. It is squarefree modulo every odd prime, and modulo $2$ it is $(x + 1)^4$. The four roots form two conjugate pairs and the sign is $(-1)^2 = +1$.
- $f = (x^2 + 1)(x^3 - x - 1)$: $\operatorname{Res}(x^2 + 1, x^3 - x - 1) = 5$ and $\operatorname{disc}(f) = (-4)(-23)(5^2) = 2300$, as property 4 says.
- **Non-example: a leading coefficient divisible by $p$.** $f = 5x^2 + x$ has discriminant $1$, so it is squarefree. Modulo $5$, $f$ becomes $x$, of lower degree, and property 1 does not apply because $\varphi(a_n) = 0$. A factoring algorithm must exclude primes that divide $a_n$ as well as those that divide $\operatorname{disc}(f)$.
- **Non-example: degree 0.** A nonzero constant has no roots, and the definition above needs $n \ge 1$. Some authors set $\operatorname{disc}(f) = 1$ for $n = 1$ by the root formula (the empty product), which agrees with the resultant formula: for $f = a_1 x + a_0$, $\operatorname{Res}_{1,0}(f, a_1) = a_1$ and $\operatorname{disc}(f) = 1$.

## Related definitions

- [Resultant](/resultant/) and [Sylvester matrix](/sylvester-matrix/): the discriminant is a normalized resultant of $f$ and $f'$.
- [Squarefree polynomial](/square-free-polynomial/) and [multiplicity of roots](/multiplicity-of-roots/): over a field of characteristic $0$, and over every finite field, $\operatorname{disc}(f) \ne 0$ exactly when $f$ is squarefree. Over an imperfect field the two notions differ: over $\mathbb{F}_p(t)$ the polynomial $x^p - t$ is irreducible, so squarefree, but its derivative is $0$ and its discriminant is $0$, since it has one root of multiplicity $p$ in an algebraic closure. [Squarefree factorization](/square-free-factorization/) removes repeated factors.
- [Vieta's formulas](/vieta-formulas/): the product $\prod_{i<j} (\alpha_i - \alpha_j)^2$ is a symmetric function of the roots, so it is a polynomial in the elementary symmetric functions, which Vieta's formulas express in the coefficients.
- [Hensel lifting](/hensel-lifting/) and the [Zassenhaus algorithm](/zassenhaus-algorithm/): they need a prime $p$ with $p \nmid a_n \operatorname{disc}(f)$, so that the factorization modulo $p$ is squarefree and can be lifted.
- [Eisenstein's criterion](/eisenstein-criterion/): if $f$ is Eisenstein at $p$ and $n \ge 2$, then $f \equiv a_n x^n \pmod p$ has a repeated root, so $p \mid \operatorname{disc}(f)$.

## References
