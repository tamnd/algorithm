---
tag: H1JYJA
kind: theorem
slug: elimination-theorem
name: Elimination theorem
aliases:
- lex elimination property
- elimination property of Gröbner bases
area: algebra/computer-algebra
level: core
summary: A lex Gröbner basis yields a basis of each elimination ideal.
prereqs: [elimination-ideal, groebner-basis, monomial-ordering]
see_also: [polynomial-system-solving, buchberger-algorithm, fglm-algorithm, groebner-basis-conversion, resultant, triangular-decomposition]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 3, Section 1 (the elimination theorem and its proof; elimination orders in the exercises)
  - book: isbn:9780387979715
    title: Thomas Becker and Volker Weispfenning (with Heinz Kredel), Gröbner Bases, A Computational Approach to Commutative Algebra, Graduate Texts in Mathematics 141, Springer, 1993
    locator: Chapter 6, first applications (elimination of variables with block orders)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 21.6, geometric applications (elimination with lex Gröbner bases)
  - paper: "Patrizia Gianni and Teo Mora, Algebraic solution of systems of polynomial equations using Gröbner bases, AAECC-5, Lecture Notes in Computer Science 356, Springer, 1989, pages 247 to 257"
    locator: the shape lemma for zero-dimensional radical ideals
---

The elimination theorem says that a [Gröbner basis](/groebner-basis/) for the lex order with $x_1 > x_2 > \cdots > x_n$ contains a Gröbner basis of every [elimination ideal](/elimination-ideal/) $I \cap K[x_{l+1}, \ldots, x_n]$: take the elements that do not involve $x_1, \ldots, x_l$. The same holds for any elimination order for the first $l$ variables. This makes elimination of variables a by-product of one Gröbner basis computation, and it is the reason that lex bases of zero-dimensional systems are triangular.

## Statement

Let $K$ be a field, $I$ an ideal of $K[x_1, \ldots, x_n]$, and $0 \le l \le n$. A monomial order $>$ is an *$l$-elimination order* if every monomial that involves at least one of $x_1, \ldots, x_l$ is greater than every monomial in $K[x_{l+1}, \ldots, x_n]$. Lex with $x_1 > \cdots > x_n$ is an $l$-elimination order for every $l$.

**Theorem.** Let $>$ be an $l$-elimination order and let $G$ be a Gröbner basis of $I$ for $>$. Then

$$G_l = G \cap K[x_{l+1}, \ldots, x_n]$$

is a Gröbner basis of the elimination ideal $I_l = I \cap K[x_{l+1}, \ldots, x_n]$, for the order that $>$ induces on the monomials of $K[x_{l+1}, \ldots, x_n]$. In particular, $G_l$ generates $I_l$. For lex this holds for every $l$ at once.

If $G$ is the reduced Gröbner basis of $I$, then $G_l$ is the reduced Gröbner basis of $I_l$.

## In plain words

Order the terms so that any term with one of the first few variables counts as larger than any term without them. Compute a Gröbner basis with that order. Then throw away every polynomial of the basis that still contains one of those first variables. What is left describes exactly the consequences of the system that are free of those variables. Nothing is lost: every such consequence can be built from what is left.

With the dictionary order this works for every prefix of the variables at the same time. The basis then looks like a staircase: some polynomials in the last variable only, then some in the last two, and so on.

## Proof

The induced order is a monomial order on $K[x_{l+1}, \ldots, x_n]$, because the conditions of a monomial order (total, compatible with multiplication, a well-order) pass to a subset of monomials that is closed under multiplication.

*Step 1: $G_l \subseteq I_l$.* Each element of $G_l$ is in $G \subseteq I$ and in $K[x_{l+1}, \ldots, x_n]$.

*Step 2: the key property of the order.* Let $g \ne 0$ with $\operatorname{LT}(g) \in K[x_{l+1}, \ldots, x_n]$. Then $g \in K[x_{l+1}, \ldots, x_n]$. Indeed, if some term of $g$ involved one of $x_1, \ldots, x_l$, that term would be greater than $\operatorname{LT}(g)$, which has none of these variables, by the definition of an $l$-elimination order. That contradicts the fact that $\operatorname{LT}(g)$ is the greatest term.

*Step 3: the leading terms.* Let $f \in I_l$ be nonzero. Then $f \in I$, and $G$ is a Gröbner basis of $I$, so $\operatorname{LT}(g)$ divides $\operatorname{LT}(f)$ for some $g \in G$. Since $\operatorname{LT}(f)$ has no $x_1, \ldots, x_l$, neither has its divisor $\operatorname{LT}(g)$. By Step 2, $g \in G_l$. The leading term of $f$ in the induced order is the same as in $>$, because $f$ has only monomials of $K[x_{l+1}, \ldots, x_n]$. So the leading term of each nonzero element of $I_l$ is divisible by the leading term of an element of $G_l$. With Step 1, this is the definition of a Gröbner basis of $I_l$, in the form of condition 2 on the page [Gröbner basis](/groebner-basis/). A Gröbner basis of an ideal generates it.

*Step 4: reduced bases.* If $G$ is reduced, each element of $G_l$ has leading coefficient 1, and no term of an element of $G_l$ is divisible by the leading term of another element of $G$, so in particular not of another element of $G_l$. So $G_l$ is reduced. $\blacksquare$

## Consequences

- **Triangular form.** If $I$ is zero-dimensional and proper, some power of each variable lies in $\langle \operatorname{LT}(I) \rangle$, so for each $l$ the reduced lex basis has an element whose leading monomial is a power of $x_l$. By Step 2 of the proof (applied with $l - 1$), that element lies in $K[x_l, \ldots, x_n]$. So the basis has a polynomial in $x_n$ alone, one in $x_{n-1}, x_n$ with a pure power of $x_{n-1}$ as leading monomial, and so on. [Polynomial system solving](/polynomial-system-solving/) uses this: solve the univariate polynomial, substitute, and repeat. The extension theorem on the [elimination ideal](/elimination-ideal/) page tells when a partial solution extends.
- **Shape lemma.** If $I$ is zero-dimensional and radical, and the $x_n$-coordinates of its solutions over $\overline{K}$ are distinct, then the reduced lex basis has the *shape* $\{x_1 - h_1(x_n), \ldots, x_{n-1} - h_{n-1}(x_n), h(x_n)\}$ with $\deg h_i < \deg h$. This is the shape lemma of Gianni and Mora. It is the form that [FGLM](/fglm-algorithm/) and the [rational univariate representation](/rational-univariate-representation/) aim at.
- **Implicitization, intersections, kernels.** The equations of the image of a polynomial map, the intersection of two ideals and the kernel of a map of polynomial rings are elimination ideals, so each is computed by one basis for an elimination order.
- **Cost.** Lex bases are often much more expensive than grevlex bases. In practice one computes a grevlex basis and converts it ([Gröbner basis conversion](/groebner-basis-conversion/)), or uses a block order with grevlex inside each block, which is an $l$-elimination order for one fixed $l$.

### Example

For $I = \langle x^2 + y + z - 1,\ x + y^2 + z - 1,\ x + y + z^2 - 1 \rangle \subseteq \mathbb{Q}[x, y, z]$, lex with $x > y > z$ gives the reduced basis

$$\{x + y + z^2 - 1,\ y^2 - y - z^2 + z,\ y z^2 + \tfrac12 z^4 - \tfrac12 z^2,\ z^6 - 4z^4 + 4z^3 - z^2\}.$$

By the theorem, the last three form the reduced basis of $I_1 = I \cap \mathbb{Q}[y, z]$, and the last one alone is the reduced basis of $I_2 = I \cap \mathbb{Q}[z]$. The [elimination ideal](/elimination-ideal/) page finds the five solutions from it.

## Tightness

- **The order must be an elimination order.** For $I = \langle x^3 - 2xy,\ x^2 y - 2y^2 + x \rangle$ with grlex and $x > y$, the reduced basis is $\{x^2, xy, y^2 - \tfrac12 x\}$, and no element lies in $\mathbb{Q}[y]$. Yet $I_1 = \langle y^3 \rangle \ne \{0\}$: the lex basis is $\{x - 2y^2, y^3\}$. Grlex fails because $y^2 > x$ in it, so Step 2 breaks: $y^2 - \tfrac12 x$ has a leading term without $x$ but is not in $\mathbb{Q}[y]$.
- **A generating set is not enough.** The theorem needs a Gröbner basis. The generators $\{xy + 1, y^2 - 1\}$ of an ideal of $\mathbb{Q}[x, y]$ contain $y^2 - 1$ in $\mathbb{Q}[y]$, which here happens to generate $I_1$; but the generators $\{x - y, x + y\}$ contain no element of $\mathbb{Q}[y]$, while $I_1 = \langle y \rangle$.
- **Only a prefix of the variables.** Lex with $x_1 > \cdots > x_n$ eliminates $x_1, \ldots, x_l$ for each $l$, but not, for example, $x_2$ alone. To eliminate another set, reorder the variables or use a block order.

## History

Elimination by resultants handles two polynomials at a time and goes back to the nineteenth century. Gröbner bases with lex or block orders give elimination for any number of polynomials. The statement and proof above follow Cox, Little and O'Shea, Chapter 3, Section 1.

## References
