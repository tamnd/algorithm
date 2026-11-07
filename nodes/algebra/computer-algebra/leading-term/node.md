---
tag: A1BM2F
kind: definition
slug: leading-term
name: Leading term
aliases:
- leading monomial
- initial term
- leading coefficient
- head term
area: algebra/computer-algebra
level: intro
summary: The largest term of a polynomial under a fixed monomial ordering.
prereqs: [monomial, monomial-ordering]
see_also: [multivariate-division-algorithm, groebner-basis, s-polynomial, polynomial-ideal, buchberger-algorithm, polynomial-degree]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 2 (multidegree, leading coefficient, leading monomial and leading term, and their properties) and Section 5 (the ideal of leading terms)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Section 21.2 (leading coefficient, leading monomial and leading term for a monomial order)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 10 (Gröbner bases, the leading term of a polynomial for a term ordering)
---

The leading term of a nonzero polynomial in several variables is its largest term for a fixed [monomial order](/monomial-ordering/). It comes in three parts: the leading [monomial](/monomial/) $\operatorname{LM}(f)$, the leading coefficient $\operatorname{LC}(f)$ and their product, the leading term $\operatorname{LT}(f)$. In one variable it is the term of highest degree, and it plays the same role: [division](/multivariate-division-algorithm/) cancels the leading term at each step, and a [Gröbner basis](/groebner-basis/) is defined by the leading terms of an ideal. The leading term changes when the order changes, so a statement about it must name the order.

## Definition

**Notation.** $K$ is a field, $K[x_1, \ldots, x_n]$ is the polynomial ring and $x^\alpha = x_1^{\alpha_1} \cdots x_n^{\alpha_n}$ for $\alpha \in \mathbb{N}^n$. Fix a [monomial order](/monomial-ordering/) $>$ on $\mathbb{N}^n$, for example lex, grlex or grevlex.

**Definition.** Let $f = \sum_\alpha c_\alpha x^\alpha$ be a nonzero polynomial in $K[x_1, \ldots, x_n]$. Its support $\{\alpha : c_\alpha \ne 0\}$ is finite and not empty, and $>$ is a total order, so the support has a largest element.

- The *multidegree* of $f$ is $\operatorname{multideg}(f) = \max_> \{\alpha : c_\alpha \ne 0\}$.
- The *leading coefficient* is $\operatorname{LC}(f) = c_{\operatorname{multideg}(f)} \in K \setminus \{0\}$.
- The *leading monomial* is $\operatorname{LM}(f) = x^{\operatorname{multideg}(f)}$.
- The *leading term* is $\operatorname{LT}(f) = \operatorname{LC}(f) \cdot \operatorname{LM}(f)$.

The zero polynomial has no support, so these are not defined for it. Some books set $\operatorname{LT}(0) = 0$ as a convention. This page does not.

For an ideal $I$, write $\operatorname{LT}(I) = \{\operatorname{LT}(f) : f \in I, f \ne 0\}$, and $\langle \operatorname{LT}(I) \rangle$ for the ideal that this set generates. It is a monomial ideal, also called the *initial ideal* $\operatorname{in}_>(I)$.

**Properties.** For nonzero $f, g \in K[x_1, \ldots, x_n]$:

1. $\operatorname{LM}(fg) = \operatorname{LM}(f) \operatorname{LM}(g)$ and $\operatorname{LT}(fg) = \operatorname{LT}(f) \operatorname{LT}(g)$.
2. If $f + g \ne 0$, then $\operatorname{multideg}(f + g) \le \max(\operatorname{multideg}(f), \operatorname{multideg}(g))$. If the two multidegrees differ, equality holds.
3. Each monomial $x^\beta$ of $f$ satisfies $x^\beta \le \operatorname{LM}(f)$, and only $\operatorname{LM}(f)$ itself is equal.

*Proof of 1.* Let $\alpha = \operatorname{multideg}(f)$ and $\beta = \operatorname{multideg}(g)$. A monomial of $fg$ is $x^{\alpha' + \beta'}$ with $\alpha'$ in the support of $f$ and $\beta'$ in that of $g$. Always $\alpha' \le \alpha$ and $\beta' \le \beta$. If $(\alpha', \beta') \ne (\alpha, \beta)$, one of the two is strict, say $\alpha' < \alpha$ (the other case swaps the roles of $f$ and $g$). Then by the two rules of a monomial order $\alpha' + \beta' < \alpha + \beta' \le \alpha + \beta$. So the pair $(\alpha, \beta)$ is the only pair that gives the monomial $x^{\alpha + \beta}$, its coefficient in $fg$ is $\operatorname{LC}(f) \operatorname{LC}(g)$, which is not zero because $K$ is a field, and each other monomial of $fg$ is smaller. $\square$

*Proof of 2.* Each monomial of $f + g$ is a monomial of $f$ or of $g$, so it is at most the larger of the two multidegrees. If $\operatorname{multideg}(f) > \operatorname{multideg}(g)$, the leading monomial of $f$ does not appear in $g$, so it does not cancel. $\square$

Property 3 is the definition of a maximum. Property 1 needs a ring without zero divisors: over $\mathbb{Z}/6\mathbb{Z}$, $(2x + 1)(3x + 1) = 5x + 1$, so the leading monomial of the product is $x$, not $x^2$.

## Examples and non-examples

Let $f = 4 x y^2 z + 4 z^2 - 5 x^3 + 7 x^2 z^2 \in \mathbb{Q}[x, y, z]$, with $x > y > z$. This is the example of Cox, Little and O'Shea, Chapter 2, Section 2.

| order | $\operatorname{multideg}(f)$ | $\operatorname{LC}(f)$ | $\operatorname{LM}(f)$ | $\operatorname{LT}(f)$ |
|---|---|---|---|---|
| lex | $(3, 0, 0)$ | $-5$ | $x^3$ | $-5 x^3$ |
| grlex | $(2, 0, 2)$ | $7$ | $x^2 z^2$ | $7 x^2 z^2$ |
| grevlex | $(1, 2, 1)$ | $4$ | $x y^2 z$ | $4 x y^2 z$ |

Under lex the first exponent decides, so $x^3$ wins. Under grlex and grevlex the total degree decides first: $x y^2 z$ and $x^2 z^2$ both have degree $4$, and $x^3$ has degree $3$. Grlex then compares from the left: $x^2 z^2$ has the larger power of $x$. Grevlex compares from the right and the smaller power of the last variable wins: $x y^2 z$ has $z^1$ and $x^2 z^2$ has $z^2$, so $x y^2 z$ is larger.

**The leading terms of the generators are not enough.** Let $I = \langle f_1, f_2 \rangle \subseteq \mathbb{Q}[x, y]$ with $f_1 = x^3 - 2xy$ and $f_2 = x^2 y - 2y^2 + x$, under grlex with $x > y$. Then $\operatorname{LT}(f_1) = x^3$ and $\operatorname{LT}(f_2) = x^2 y$. But

$$x f_2 - y f_1 = x^2 \in I,$$

and $x^2$ is not divisible by $x^3$ or by $x^2 y$. So $\langle \operatorname{LT}(f_1), \operatorname{LT}(f_2) \rangle \subsetneq \langle \operatorname{LT}(I) \rangle$. The reduced Gröbner basis of $I$ for this order is $\{x^2, xy, y^2 - \tfrac{1}{2} x\}$, and $\langle \operatorname{LT}(I) \rangle = \langle x^2, xy, y^2 \rangle$.

**One variable.** In $K[x]$ there is only one monomial order, $1 < x < x^2 < \cdots$. Then $\operatorname{LT}(f)$ is the term of highest degree and $\operatorname{multideg}(f) = \deg f$ (see [polynomial degree](/polynomial-degree/)).

Non-examples:

- "The leading term of $x + y$" has no meaning until an order is fixed: it is $x$ when $x > y$ and $y$ when $y > x$.
- The term of highest total degree is not the leading term under lex. For $f$ above, $7 x^2 z^2$ has the highest total degree, but the lex leading term is $-5 x^3$.
- The zero polynomial has no leading term.

## Related definitions

- **Monomial order.** The order that the definition depends on. See [monomial ordering](/monomial-ordering/).
- **Initial ideal.** $\langle \operatorname{LT}(I) \rangle$. A [Gröbner basis](/groebner-basis/) of $I$ is a finite $G \subseteq I$ with $\langle \operatorname{LT}(g) : g \in G \rangle = \langle \operatorname{LT}(I) \rangle$.
- **S-polynomial.** The combination of two polynomials that cancels their leading terms. See [S-polynomial](/s-polynomial/).
- **Trailing term.** The smallest term of $f$ for the order. Some algorithms for local rings use it in place of the leading term.
- **Leading form.** For a total degree order, the sum of the terms of highest total degree. It is a homogeneous polynomial, and it is not a single term in general.

## References
