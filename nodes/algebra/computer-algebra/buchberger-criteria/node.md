---
tag: NSXM93
kind: theorem
slug: buchberger-criteria
name: Buchberger's criteria
aliases:
- Buchberger's first criterion
- Buchberger's second criterion
- Buchberger's criterion
- product criterion
- chain criterion
area: algebra/computer-algebra
level: core
summary: Criteria that let some S-polynomials be skipped and certify a Gröbner basis.
prereqs: [groebner-basis, s-polynomial, multivariate-division-algorithm]
see_also: [buchberger-algorithm, gebauer-moller-criteria, f5-algorithm, syzygy, groebner-basis-computation, reduced-groebner-basis]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 6 (Buchberger's criterion), Section 9 (refinements of the Buchberger criterion, lcm representations and the product criterion) and Section 10 (improvements on Buchberger's algorithm, the chain criterion)
  - book: isbn:9780387979715
    title: Thomas Becker and Volker Weispfenning (with Heinz Kredel), Gröbner Bases, A Computational Approach to Commutative Algebra, Graduate Texts in Mathematics 141, Springer, 1993
    locator: Chapter 5, Gröbner bases (the S-polynomial criterion and the improved algorithm with the two criteria)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 21.5, Buchberger's algorithm (the S-polynomial criterion)
  - paper: doi:10.1016/j.jsc.2005.09.007
    title: Bruno Buchberger, An algorithm for finding the basis elements of the residue class ring of a zero dimensional polynomial ideal (English translation of the 1965 PhD thesis), Journal of Symbolic Computation 41(3-4), 475-511, 2006
    locator: the criterion that all S-polynomials reduce to zero
  - paper: "Bruno Buchberger, A criterion for detecting unnecessary reductions in the construction of Gröbner bases, Proceedings of EUROSAM 79, Lecture Notes in Computer Science 72, Springer, 1979, pages 3 to 21"
    locator: the product criterion and the chain criterion
---

Buchberger's criteria are three results about [S-polynomials](/s-polynomial/). The main criterion says that a finite generating set $G$ of an ideal is a [Gröbner basis](/groebner-basis/) exactly when every S-polynomial of two elements of $G$ reduces to zero by $G$, so the infinite condition of the definition becomes a finite test. The *product criterion* (Buchberger's first criterion) and the *chain criterion* (the second criterion) show that some of these S-polynomials need no reduction at all. [Buchberger's algorithm](/buchberger-algorithm/) is built on the first result, and every practical version uses the other two.

## Statement

$K$ is a field, $>$ is a [monomial order](/monomial-ordering/) on $K[x_1, \ldots, x_n]$, and $\operatorname{LT}$, $\operatorname{LM}$ and $\operatorname{LC}$ are the leading term, monomial and coefficient. Let $G = \{g_1, \ldots, g_t\}$ be nonzero polynomials that generate the ideal $I$. For $i \ne j$ let $x^{\gamma_{ij}} = \operatorname{lcm}(\operatorname{LM}(g_i), \operatorname{LM}(g_j))$, and let

$$S(g_i, g_j) = \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_i)} g_i - \frac{x^{\gamma_{ij}}}{\operatorname{LT}(g_j)} g_j .$$

An *lcm-representation* of $S(g_i, g_j)$ is an equation $S(g_i, g_j) = \sum_{l=1}^t A_l g_l$ with $A_l \in K[x_1, \ldots, x_n]$ and $\operatorname{LM}(A_l g_l) < x^{\gamma_{ij}}$ for each $l$ with $A_l g_l \ne 0$. A remainder of zero on division by $G$ gives one.

**Theorem A (Buchberger's criterion).** $G$ is a Gröbner basis of $I$ if and only if each $S(g_i, g_j)$ with $i < j$ has an lcm-representation. In particular, $G$ is a Gröbner basis if and only if the remainder of each $S(g_i, g_j)$ on division by $G$ is zero.

**Theorem B (product criterion, first criterion).** If $\gcd(\operatorname{LM}(g_i), \operatorname{LM}(g_j)) = 1$, then $S(g_i, g_j)$ has an lcm-representation that uses only $g_i$ and $g_j$.

**Theorem C (chain criterion, second criterion).** If $\operatorname{LM}(g_k)$ divides $x^{\gamma_{ij}}$, and $S(g_i, g_k)$ and $S(g_j, g_k)$ have lcm-representations, then $S(g_i, g_j)$ has one.

## In plain words

A Gröbner basis must catch the top term of every polynomial in the ideal, and there are infinitely many of those. Buchberger showed that you need to test only one polynomial for each pair of basis elements. This polynomial combines the pair so that their top terms cancel. If each such combination divides out to zero, the set is a Gröbner basis. If one does not, its remainder is a new element that you must add.

Two shortcuts save work. If the top terms of the pair share no variable, the test always passes, so you can skip it. If a third element has a top term that divides the common multiple of the pair's top terms, and its tests with both members of the pair pass, the test of the pair passes too.

## Proof

The full proof, with the cancellation lemma, is in the proof file below. Here is its plan.

*Theorem A.* If $G$ is a Gröbner basis, each S-polynomial is in $I$, so its remainder is zero, and the division gives a representation whose terms are at most $\operatorname{LM}(S(g_i, g_j)) < x^{\gamma_{ij}}$. For the converse, take a nonzero $f \in I$ and a representation $f = \sum h_i g_i$ whose largest monomial $x^\delta = \max \operatorname{LM}(h_i g_i)$ is least, which exists because a monomial order is a well-order. If $\operatorname{LM}(f) = x^\delta$, some $\operatorname{LT}(g_i)$ divides $\operatorname{LT}(f)$. If $\operatorname{LM}(f) < x^\delta$, the top parts $\operatorname{LT}(h_i) g_i$ cancel. A summation by parts writes their sum as a combination of terms $x^{\delta - \gamma} S(g_i, g_j)$. Replacing each S-polynomial by its lcm-representation gives a representation of $f$ with all terms below $x^\delta$, which contradicts the choice of $x^\delta$.

*Theorem B.* With $\operatorname{LC}(g_i) = \operatorname{LC}(g_j) = 1$, write $g_i = \operatorname{LM}(g_i) + r_i$ and $g_j = \operatorname{LM}(g_j) + r_j$. Coprime leading monomials give $x^{\gamma_{ij}} = \operatorname{LM}(g_i) \operatorname{LM}(g_j)$ and $S(g_i, g_j) = r_i g_j - r_j g_i$, and both terms are below $x^{\gamma_{ij}}$.

*Theorem C.* Both $x^{\gamma_{ik}}$ and $x^{\gamma_{jk}}$ divide $x^{\gamma_{ij}}$, and

$$S(g_i, g_j) = x^{\gamma_{ij} - \gamma_{ik}} S(g_i, g_k) - x^{\gamma_{ij} - \gamma_{jk}} S(g_j, g_k).$$

Multiplying the two given lcm-representations by these monomials keeps every term below $x^{\gamma_{ij}}$.

*Use in an algorithm.* A pair may be dropped by Theorem C only if the pairs $\{i, k\}$ and $\{j, k\}$ are justified earlier in a fixed order, by a zero remainder, by Theorem B, or by Theorem C. Induction along that order then gives an lcm-representation of every pair, and Theorem A applies.

## Consequences

- **Decidability.** Theorem A turns "is $G$ a Gröbner basis?" into a finite test: $\binom{t}{2}$ divisions. [Buchberger's algorithm](/buchberger-algorithm/) adds the nonzero remainders until the test passes.
- **Fewer reductions.** In [Buchberger's algorithm](/buchberger-algorithm/), the product criterion skips a pair before any work, and the chain criterion skips pairs that are covered by others. The [Gebauer-Möller criteria](/gebauer-moller-criteria/) are an order of applying both criteria that is safe and removes most redundant pairs. Each skipped pair would have reduced to zero, so the criteria save time but never change the result.
- **Signatures.** The chain criterion is a statement about [syzygies](/syzygy/) of the leading terms. The [F5 algorithm](/f5-algorithm/) replaces both criteria by a criterion on signatures that removes all reductions to zero for a regular sequence.

### Examples

All three examples use grlex with $x > y > z$ over $\mathbb{Q}$.

- *Theorem B.* For $g_1 = x^2 + y$ and $g_2 = y^2 + x$, the leading monomials $x^2$ and $y^2$ are coprime. $S(g_1, g_2) = y^2 g_1 - x^2 g_2 = y^3 - x^3$, which equals $r_1 g_2 - r_2 g_1 = y g_2 - x g_1$. Division by $\{g_1, g_2\}$ gives remainder $0$ in two steps. So $\{x^2 + y, y^2 + x\}$ is a Gröbner basis with no reduction needed.
- *Theorem C.* For $g_i = x^2 y - z$, $g_j = x y^2 - z$ and $g_k = xy - z$, the monomial $xy$ divides $x^{\gamma_{ij}} = x^2 y^2$. Here $S(g_i, g_j) = xz - yz$, $S(g_i, g_k) = xz - z$ and $S(g_j, g_k) = yz - z$, and indeed $y(xz - z) - x(yz - z) = xz - yz$.
- *Theorem A fails.* For $\{x^3 - 2xy,\ x^2 y - 2y^2 + x\}$ the only S-polynomial is $-x^2$, and its remainder is $-x^2 \ne 0$. So this set is not a Gröbner basis. The leading monomials $x^3$ and $x^2 y$ are not coprime, so Theorem B does not apply.

## Tightness

- **Theorem B needs coprime leading monomials.** In the last example the leading monomials share $x^2$, and the S-polynomial does not reduce to zero.
- **Theorem C needs an order.** Take $g_1 = xy - z$, $g_2 = yz - x$, $g_3 = xz - y$. All three lcms are $xyz$, and each leading monomial divides $xyz$. So each pair satisfies the divisibility condition of Theorem C with the third element. But $S(g_1, g_2) = x^2 - z^2$, $S(g_1, g_3) = y^2 - z^2$ and $S(g_2, g_3) = y^2 - x^2$, and none of them has remainder zero by $\{g_1, g_2, g_3\}$. A program that dropped all three pairs, each because of the other two, would return a set that is not a Gröbner basis. The reduced Gröbner basis of this ideal has six elements: $xy - z$, $yz - x$, $xz - y$, $x^2 - z^2$, $y^2 - z^2$ and $z^3 - z$.
- **The criteria are not complete.** Many pairs that reduce to zero satisfy neither criterion. Faugère's F5 criterion, based on signatures, detects all of them when the input is a regular sequence ([F5 algorithm](/f5-algorithm/)).

## History

Buchberger proved Theorem A in his 1965 PhD thesis at the University of Innsbruck, where he also gave the algorithm. He published the product criterion and the chain criterion in 1979, at EUROSAM 79. Gebauer and Möller gave in 1988 an order in which to apply the two criteria that removes most redundant pairs without the risk of the circular removal above.

## References
