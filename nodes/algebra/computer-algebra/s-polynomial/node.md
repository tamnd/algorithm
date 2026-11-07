---
tag: Q8FTP2
kind: definition
slug: s-polynomial
name: S-polynomial
aliases: [S-pair, syzygy polynomial, critical pair]
area: algebra/computer-algebra
level: core
summary: Combination of two polynomials that cancels their leading terms, used in Buchberger's criterion.
prereqs: [leading-term, monomial-ordering, multivariate-division-algorithm]
see_also: [groebner-basis, buchberger-algorithm, buchberger-criteria, syzygy, reduced-groebner-basis, sugar-strategy, gebauer-moller-criteria, f4-algorithm]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 6 (the definition of the S-polynomial, the lemma on cancelling leading terms, and Buchberger's S-pair criterion) and Section 9 (the product criterion and the syzygy view)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 21.4, Gröbner bases and S-polynomials
  - paper: doi:10.1016/j.jsc.2005.09.007
    title: Bruno Buchberger, An algorithm for finding the basis elements of the residue class ring of a zero dimensional polynomial ideal (English translation of the 1965 PhD thesis, University of Innsbruck), Journal of Symbolic Computation 41(3-4), 2006
    locator: the S-polynomial and the criterion that every S-polynomial reduces to zero
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 10, Gröbner Bases for Polynomial Ideals
---

The S-polynomial of two nonzero polynomials $f$ and $g$ is the combination $a f - b g$, with monomial multipliers $a$ and $b$, that makes the [leading terms](/leading-term/) of $f$ and $g$ cancel in the least common multiple of their leading monomials. It is the only new polynomial that a set of generators must handle to become a [Gröbner basis](/groebner-basis/): Buchberger's criterion says that a set $G$ is a Gröbner basis exactly when the S-polynomial of each pair in $G$ has remainder zero on [division](/multivariate-division-algorithm/) by $G$. [Buchberger's algorithm](/buchberger-algorithm/) adds the nonzero remainders until the criterion holds.

## Definition

**Notation.** $K$ is a field and $K[x_1, \ldots, x_n]$ is the polynomial ring over $K$. Fix a [monomial order](/monomial-ordering/) $>$ (lex, grlex or grevlex; the S-polynomial depends on the order). For a nonzero $f$, $\operatorname{LM}(f)$, $\operatorname{LC}(f)$ and $\operatorname{LT}(f) = \operatorname{LC}(f) \operatorname{LM}(f)$ are the leading monomial, coefficient and term. For monomials $x^\alpha$ and $x^\beta$, $\operatorname{lcm}(x^\alpha, x^\beta) = x^\gamma$ with $\gamma_i = \max(\alpha_i, \beta_i)$.

**Definition.** Let $f, g \in K[x_1, \ldots, x_n]$ be nonzero and let $x^\gamma = \operatorname{lcm}(\operatorname{LM}(f), \operatorname{LM}(g))$. The S-polynomial of $f$ and $g$ is

$$S(f, g) = \frac{x^\gamma}{\operatorname{LT}(f)} \, f - \frac{x^\gamma}{\operatorname{LT}(g)} \, g.$$

Both fractions are terms (a coefficient times a monomial) because $\operatorname{LM}(f)$ and $\operatorname{LM}(g)$ divide $x^\gamma$. Each of the two products has leading term exactly $x^\gamma$, so the two leading terms cancel and

$$S(f, g) = 0 \quad \text{or} \quad \operatorname{LM}(S(f, g)) < x^\gamma.$$

Some books scale by $\operatorname{LC}(g) \, x^\gamma / \operatorname{LM}(f)$ and $\operatorname{LC}(f) \, x^\gamma / \operatorname{LM}(g)$ to avoid division in a ring. That changes $S(f, g)$ by the nonzero constant $\operatorname{LC}(f) \operatorname{LC}(g)$ and changes no statement below.

**Basic facts.** $S(g, f) = -S(f, g)$ and $S(f, f) = 0$. For nonzero constants $c, d$, $S(cf, dg) = S(f, g)$. $S(f, g)$ lies in the ideal $\langle f, g \rangle$.

**Cancellation lemma.** Let $f_1, \ldots, f_s$ be nonzero, each with $\operatorname{LM}(f_i) = x^\delta$, and let $c_i \in K$. If $\sum_i c_i f_i = 0$ or $\operatorname{LM}(\sum_i c_i f_i) < x^\delta$, then $\sum_i c_i f_i$ is a $K$-linear combination of the S-polynomials $S(f_j, f_k)$, and each $S(f_j, f_k)$ is $0$ or has leading monomial below $x^\delta$.

*Proof.* Write $d_i = \operatorname{LC}(f_i)$ and $p_i = f_i / d_i$, which is monic with leading monomial $x^\delta$. The coefficient of $x^\delta$ in $\sum c_i f_i$ is $\sum c_i d_i$, and the hypothesis makes it $0$. Here $S(f_j, f_k) = p_j - p_k$, because the lcm is $x^\delta$ itself. Then

$$\sum_{i=1}^{s} c_i f_i = \sum_{i=1}^{s} c_i d_i p_i = \sum_{j=1}^{s-1} \Big( \sum_{i \le j} c_i d_i \Big) (p_j - p_{j+1}) + \Big( \sum_{i=1}^{s} c_i d_i \Big) p_s.$$

The identity follows by summation by parts: the coefficient of $p_j$ on the right is $\sum_{i \le j} c_i d_i - \sum_{i \le j-1} c_i d_i = c_j d_j$. The last term is $0$. Each $p_j - p_{j+1} = S(f_j, f_{j+1})$ has its $x^\delta$ terms cancel. $\square$

**Buchberger's criterion.** Let $G = \{g_1, \ldots, g_t\}$ be a finite set of nonzero polynomials that generates the ideal $I$. Then $G$ is a Gröbner basis of $I$ if and only if, for all $i \ne j$, the remainder of $S(g_i, g_j)$ on division by $G$ (in any fixed order of $G$) is zero. The cancellation lemma is the key step of the proof: in a representation $f = \sum h_i g_i$ whose top terms cancel, the cancelling part is a sum of S-polynomials, and each of them has a standard representation by the hypothesis, so the top degree of the representation can be lowered. The full proof, and the refinements that skip pairs, are on [Buchberger criteria](/buchberger-criteria/).

## Examples and non-examples

- **A worked S-polynomial.** In $\mathbb{Q}[x, y]$ with grlex and $x > y$, let $f = x^3 y^2 - x^2 y^3 + x$ and $g = 3 x^4 y + y^2$. Then $\operatorname{LM}(f) = x^3 y^2$, $\operatorname{LM}(g) = x^4 y$ and $x^\gamma = x^4 y^2$. So $S(f, g) = x f - \tfrac{1}{3} y g = -x^3 y^3 + x^2 - \tfrac{1}{3} y^3$, of degree 6, below $x^4 y^2$ in grlex because the multiplied leading terms cancelled. Division by $(f, g)$ leaves the remainder $-x^2 y^4 + x^2 + x y - \tfrac{1}{3} y^3$, which is not zero. So $\{f, g\}$ is not a Gröbner basis of $\langle f, g \rangle$ for grlex.
- **A failed basis.** In $\mathbb{Q}[x, y]$ with lex and $x > y$, take $f = x^2 - y$ and $g = xy - 1$. The lcm of $x^2$ and $xy$ is $x^2 y$, and $S(f, g) = y f - x g = x - y^2$. Its leading monomial $x$ is divisible by neither $x^2$ nor $xy$, so the remainder is $x - y^2$ itself. Buchberger's algorithm adds it, and the [reduced Gröbner basis](/reduced-groebner-basis/) turns out to be $\{x - y^2, \, y^3 - 1\}$.
- **Coprime leading monomials.** With lex, $f = x^2 + y$ and $g = y^3 + 1$ have leading monomials $x^2$ and $y^3$ with lcm $x^2 y^3$. Here $S(f, g) = y^3 f - x^2 g = y^4 - x^2$, and its remainder on division by $(f, g)$ is $0$. This is the product criterion: when $\operatorname{LM}(f)$ and $\operatorname{LM}(g)$ have no common variable, $S(f, g)$ always reduces to zero, so the pair can be skipped.
- **Non-example: cancelling at a larger monomial.** In the first example, $x^2 f - \tfrac{1}{3} x y \, g$ also kills the leading terms, but at $x^5 y^2$, a proper multiple of the lcm. This combination equals $x \cdot S(f, g)$, so it gives no new information. The S-polynomial uses the least common multiple, the smallest monomial where the two leading terms can meet, and each other cancelling combination of the two is a polynomial multiple of it.
- **Non-example: the zero polynomial.** $S(f, 0)$ is not defined, because $0$ has no leading term. A generating set is first cleaned of zeros.

## Related definitions

- [Gröbner basis](/groebner-basis/): the property that Buchberger's criterion tests through S-polynomials.
- [Syzygy](/syzygy/): the pair of multipliers $(x^\gamma / \operatorname{LT}(f), \, -x^\gamma / \operatorname{LT}(g))$ is a syzygy of the leading terms. These S-syzygies generate the module of all syzygies of the leading terms, which is why it is enough to look at S-polynomials.
- [Buchberger criteria](/buchberger-criteria/) and [Gebauer-Möller criteria](/gebauer-moller-criteria/): rules that prove some S-polynomials reduce to zero without computing them.
- [Sugar strategy](/sugar-strategy/): an order in which to treat the pairs.
- [Subresultant](/subresultant/): in one variable, with $\deg f \ge \deg g$, the S-polynomial $f / \operatorname{LC}(f) - x^{\deg f - \deg g} g / \operatorname{LC}(g)$ is the first step of the division of $f$ by $g$, and a scaled first step of [pseudo-division](/pseudo-division/).
- [F4](/f4-algorithm/): reduces many S-polynomials at once as rows of one matrix.

## References
