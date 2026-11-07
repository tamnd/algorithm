---
tag: 1G136V
kind: definition
slug: monomial
name: Monomial
aliases:
- power product
- term (in some books)
area: algebra/computer-algebra
level: intro
summary: A product of powers of variables, the basis elements of a polynomial ring.
prereqs: [polynomial, polynomial-ring]
see_also: [monomial-ordering, leading-term, polynomial-ideal, groebner-basis, hilbert-basis-theorem, hilbert-series, sparse-polynomial, dense-polynomial]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 1, Section 1 (monomials, terms and total degree); Chapter 2, Section 4 (monomial ideals and Dickson's lemma)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Section 21.2 (monomials and monomial orders) and Section 21.3 (monomial ideals)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 2 (multivariate polynomial rings) and Chapter 10 (Gröbner bases, terms and term orderings)
---

A monomial in the variables $x_1, \ldots, x_n$ is a product $x_1^{\alpha_1} x_2^{\alpha_2} \cdots x_n^{\alpha_n}$ with exponents $\alpha_i$ that are natural numbers. The monomials are a basis of the [polynomial ring](/polynomial-ring/) $K[x_1, \ldots, x_n]$ as a vector space over the field $K$, so each [polynomial](/polynomial/) is a unique finite sum of coefficients times monomials. Monomials multiply by adding exponent vectors, and one divides another when its exponents are smaller in each place. A [monomial order](/monomial-ordering/), the [leading term](/leading-term/), [Gröbner bases](/groebner-basis/) and the [Hilbert series](/hilbert-series/) are all built on these two facts.

## Definition

**Notation.** $K$ is a field. Where a statement holds over any commutative ring $R$ with $1$, we say so. $\mathbb{N} = \{0, 1, 2, \ldots\}$. For $\alpha = (\alpha_1, \ldots, \alpha_n) \in \mathbb{N}^n$ we write

$$x^\alpha = x_1^{\alpha_1} x_2^{\alpha_2} \cdots x_n^{\alpha_n}.$$

**Definition.** A *monomial* in $x_1, \ldots, x_n$ is an expression $x^\alpha$ with $\alpha \in \mathbb{N}^n$. The vector $\alpha$ is its *exponent vector*, and $|\alpha| = \alpha_1 + \cdots + \alpha_n$ is its *total degree*. The monomial $x^{(0, \ldots, 0)} = 1$ has total degree $0$. A *term* is a product $c\, x^\alpha$ with $c \in K$ and $c \ne 0$. A polynomial is a finite sum of terms with distinct monomials:

$$f = \sum_{\alpha \in S} c_\alpha x^\alpha, \qquad S \subseteq \mathbb{N}^n \text{ finite}, \quad c_\alpha \ne 0 \text{ for } \alpha \in S.$$

The set $S$ is the *support* of $f$. The zero polynomial has empty support. The number of terms is $t = |S|$.

**The operations.** The map $\alpha \mapsto x^\alpha$ is a bijection from $\mathbb{N}^n$ to the set of monomials, and it turns the operations on monomials into operations on vectors:

- *Product.* $x^\alpha x^\beta = x^{\alpha + \beta}$.
- *Divisibility.* $x^\alpha$ divides $x^\beta$ exactly when $\alpha_i \le \beta_i$ for each $i$. Then $x^\beta / x^\alpha = x^{\beta - \alpha}$.
- *Least common multiple and greatest common divisor.* $\operatorname{lcm}(x^\alpha, x^\beta) = x^\gamma$ with $\gamma_i = \max(\alpha_i, \beta_i)$, and $\gcd(x^\alpha, x^\beta) = x^\delta$ with $\delta_i = \min(\alpha_i, \beta_i)$.

So the monomials under multiplication form a commutative monoid isomorphic to $(\mathbb{N}^n, +)$, and divisibility is the componentwise partial order on $\mathbb{N}^n$. Each of the operations costs $O(n)$ operations on the exponents.

**Basis.** The monomials are linearly independent over $K$, and they span $K[x_1, \ldots, x_n]$ by the definition of a polynomial. So they form a basis of $K[x_1, \ldots, x_n]$ as a $K$-vector space, and the coefficients $c_\alpha$ of $f$ are unique. The same holds over a ring $R$: the monomials form a basis of the free $R$-module $R[x_1, \ldots, x_n]$.

**Counting.** The number of monomials of total degree exactly $d$ in $n \ge 1$ variables is $\binom{n + d - 1}{n - 1}$, and the number of total degree at most $d$ is $\binom{n + d}{n}$.

*Proof.* A monomial of total degree $d$ is a vector $\alpha \in \mathbb{N}^n$ with $\alpha_1 + \cdots + \alpha_n = d$. Write $d$ stars in a row and put $n - 1$ bars between them: $\alpha_1$ is the number of stars before the first bar, $\alpha_i$ the number between bar $i - 1$ and bar $i$, and $\alpha_n$ the number after the last bar. This is a bijection between the vectors and the arrangements of $d$ stars and $n - 1$ bars in $d + n - 1$ places, and there are $\binom{n + d - 1}{n - 1}$ such arrangements. A monomial of total degree at most $d$ in $x_1, \ldots, x_n$ is the same as a monomial of total degree exactly $d$ in $x_0, x_1, \ldots, x_n$, by $x^\alpha \mapsto x_0^{d - |\alpha|} x^\alpha$. So there are $\binom{(n + 1) + d - 1}{n} = \binom{n + d}{n}$ of them. $\square$

This count is the dimension of the space of polynomials of total degree at most $d$. A *dense* representation stores all $\binom{n + d}{n}$ coefficients, and a *sparse* one stores only the $t$ terms of the support (see [dense polynomial](/dense-polynomial/) and [sparse polynomial](/sparse-polynomial/)).

**Monomial ideals.** An ideal $I \subseteq K[x_1, \ldots, x_n]$ is a *monomial ideal* if it is generated by monomials. If $I = \langle x^\alpha : \alpha \in A \rangle$ for a set $A \subseteq \mathbb{N}^n$, then a monomial $x^\beta$ lies in $I$ exactly when $x^\alpha$ divides $x^\beta$ for some $\alpha \in A$, and a polynomial lies in $I$ exactly when each of its terms lies in $I$ (Cox, Little and O'Shea, Chapter 2, Section 4). Dickson's lemma says that each monomial ideal is generated by finitely many monomials. Its proof is on the page of the [Hilbert basis theorem](/hilbert-basis-theorem/).

## Examples and non-examples

- $x^2 y z^3$ in $K[x, y, z]$ is a monomial with exponent vector $(2, 1, 3)$ and total degree $6$.
- $1$ is a monomial, with exponent vector $(0, \ldots, 0)$.
- For $x^\alpha = x^2 y z^3$ and $x^\beta = x y^4$: the product is $x^3 y^5 z^3$, the lcm is $x^2 y^4 z^3$ and the gcd is $x y$. Neither divides the other, because $2 > 1$ in the first place and $1 < 4$ in the second.
- In $K[x, y, z]$ there are $\binom{4}{2} = 6$ monomials of total degree $2$: $x^2, y^2, z^2, xy, xz, yz$. There are $\binom{5}{3} = 10$ of total degree at most $2$: these six, the three variables and $1$.
- With $n = 10$ variables and $d = 10$, there are $\binom{20}{10} = 184756$ monomials of total degree at most $10$. A polynomial with $t = 50$ terms uses less than $0.03$ percent of this dense space.

Non-examples:

- $3 x^2 y$ is a term, not a monomial, in the convention of this page: it has the coefficient $3$. Its monomial is $x^2 y$.
- $x + y$ is a polynomial with two terms, not a monomial.
- $x^{-1} y$ is not a monomial: an exponent is negative. It is a *Laurent monomial*, an element of $K[x^{\pm 1}, y^{\pm 1}]$.
- $x^{1/2}$ is not a monomial: the exponent is not an integer.

## Related definitions

- **Term and coefficient.** A term is $c\, x^\alpha$ with $c \ne 0$. Some books, for example Becker and Weispfenning, swap the two words: they call $x^\alpha$ a *term* and $c\, x^\alpha$ a *monomial*. Check the convention of a source before you copy a statement from it.
- **Monomial order.** A total order on monomials that respects multiplication and is a well-order. See [monomial ordering](/monomial-ordering/).
- **Leading term, monomial and coefficient.** $\operatorname{LT}(f)$, $\operatorname{LM}(f)$ and $\operatorname{LC}(f)$ of a nonzero polynomial, for a fixed order. See [leading term](/leading-term/).
- **Homogeneous polynomial.** A polynomial whose terms all have the same total degree.
- **Standard monomials.** For an ideal $I$ and a [Gröbner basis](/groebner-basis/) $G$, the monomials that no $\operatorname{LT}(g)$ with $g \in G$ divides. They form a basis of $K[x_1, \ldots, x_n] / I$, and their count by degree is the [Hilbert function](/hilbert-series/).

## References
