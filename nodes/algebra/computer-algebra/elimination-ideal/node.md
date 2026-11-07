---
tag: 4EDSP0
kind: concept
slug: elimination-ideal
name: Elimination ideal
aliases:
- k-th elimination ideal
- l-th elimination ideal
area: algebra/computer-algebra
level: core
summary: The ideal of polynomials in a subset of variables obtained by eliminating the others.
prereqs: [polynomial-ideal, groebner-basis]
see_also: [elimination-theorem, resultant, polynomial-system-solving, groebner-basis-computation, triangular-decomposition, quantifier-elimination]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 3, Section 1 (the elimination and extension theorems), Section 2 (the geometry of elimination, the closure theorem) and Section 3 (implicitization)
  - book: isbn:9780387979715
    title: Thomas Becker and Volker Weispfenning (with Heinz Kredel), Gröbner Bases, A Computational Approach to Commutative Algebra, Graduate Texts in Mathematics 141, Springer, 1993
    locator: Chapter 6, first applications of Gröbner bases (elimination of variables and intersections of ideals)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 21.6, geometric applications (elimination and implicitization)
---

The $l$-th elimination ideal of an ideal $I \subseteq K[x_1, \ldots, x_n]$ is $I_l = I \cap K[x_{l+1}, \ldots, x_n]$: the polynomials of $I$ that do not involve the first $l$ variables. It is the algebraic form of eliminating variables from a system of equations. Its zero set is, over an algebraically closed field, the closure of the projection of the zero set of $I$. A [lex Gröbner basis](/groebner-basis/) of $I$ gives a basis of every $I_l$ at once, by the [elimination theorem](/elimination-theorem/).

## In plain words

Take a system of polynomial equations in several unknowns. Some equations follow from it: you get them by multiplying the given equations by polynomials and adding. Among all these consequences, keep only those that do not contain the first few unknowns. They form the elimination ideal. They are the conditions that the remaining unknowns must meet.

For two linear equations in two unknowns, you subtract a multiple of one from the other to remove the first unknown; what is left is one equation in the second unknown. The elimination ideal does this for any polynomial system, and it holds every equation that can arise in this way, not just one.

## The idea

**Definition.** Let $K$ be a field and $I$ an ideal of $K[x_1, \ldots, x_n]$. For $0 \le l \le n$, the $l$-th elimination ideal is

$$I_l = I \cap K[x_{l+1}, \ldots, x_n].$$

So $I_0 = I$, $I_n = I \cap K$ is $\{0\}$ or $K$, and $I_0 \supseteq I_1 \supseteq \cdots \supseteq I_n$ under the inclusions of the rings. Each $I_l$ is an ideal of $K[x_{l+1}, \ldots, x_n]$: a sum of two elements of $I$ without $x_1, \ldots, x_l$ has no such variable, and neither does a product with a polynomial in $x_{l+1}, \ldots, x_n$. More generally, for any subset $Y$ of the variables, $I \cap K[Y]$ is the elimination ideal of the other variables.

**How to compute it.** Choose an *elimination order* for $x_1, \ldots, x_l$: a monomial order in which each monomial that contains one of $x_1, \ldots, x_l$ is larger than each monomial in $x_{l+1}, \ldots, x_n$ alone. Lex with $x_1 > \cdots > x_n$ is one for every $l$; a block order that compares the first block by grevlex and then the second block by grevlex is one for a fixed $l$ and is usually cheaper. If $G$ is a Gröbner basis of $I$ for such an order, then $G \cap K[x_{l+1}, \ldots, x_n]$ is a Gröbner basis of $I_l$. This is the [elimination theorem](/elimination-theorem/).

**Geometry.** Let $V = \mathbf{V}(I) \subseteq \overline{K}^n$ be the common zeros of $I$ over an algebraic closure, and let $\pi_l$ forget the first $l$ coordinates. Each $f \in I_l$ vanishes on $V$ and does not depend on $x_1, \ldots, x_l$, so it vanishes on $\pi_l(V)$. Hence $\pi_l(V) \subseteq \mathbf{V}(I_l)$. The *closure theorem* says more: over an algebraically closed field, $\mathbf{V}(I_l)$ is the smallest variety that contains $\pi_l(V)$ (Cox, Little and O'Shea, Chapter 3, Section 2). The inclusion can be strict, so a zero of $I_l$ need not extend to a zero of $I$.

**Extension.** The *extension theorem* says when a partial solution extends. Let $K$ be algebraically closed and $I = \langle f_1, \ldots, f_s \rangle$. Write each $f_i = c_i(x_2, \ldots, x_n) x_1^{N_i} + (\text{terms of lower degree in } x_1)$ with $c_i \ne 0$. If $(a_2, \ldots, a_n) \in \mathbf{V}(I_1)$ and $(a_2, \ldots, a_n) \notin \mathbf{V}(c_1, \ldots, c_s)$, then some $a_1$ makes $(a_1, a_2, \ldots, a_n) \in \mathbf{V}(I)$ (Cox, Little and O'Shea, Chapter 3, Section 1).

**Resultants.** For two polynomials $f, g$ of positive degree in $x_1$, the [resultant](/resultant/) $\operatorname{Res}_{x_1}(f, g)$ lies in $\langle f, g \rangle \cap K[x_2, \ldots, x_n]$, the first elimination ideal. It is one element of it, often not a generator, and it handles only two polynomials at a time.

## Examples

**A system with five solutions.** In $\mathbb{Q}[x, y, z]$ let $I = \langle x^2 + y + z - 1,\ x + y^2 + z - 1,\ x + y + z^2 - 1 \rangle$ (Cox, Little and O'Shea, Chapter 3, Section 1). The reduced lex basis for $x > y > z$ is

$$g_1 = x + y + z^2 - 1,\quad g_2 = y^2 - y - z^2 + z,\quad g_3 = y z^2 + \tfrac12 z^4 - \tfrac12 z^2,\quad g_4 = z^6 - 4z^4 + 4z^3 - z^2 .$$

So $I_1 = \langle g_2, g_3, g_4 \rangle$ and $I_2 = \langle g_4 \rangle$. Here $g_4 = z^2 (z - 1)^2 (z^2 + 2z - 1)$, so $z \in \{0, 1, -1 \pm \sqrt2\}$. Back substitution gives the five solutions $(1, 0, 0)$, $(0, 1, 0)$, $(0, 0, 1)$ and $(t, t, t)$ with $t = -1 \pm \sqrt 2$: for $z = 0$, $g_2$ gives $y \in \{0, 1\}$ and $g_1$ gives $x = 1 - y$; for $z = 1$, $g_3$ gives $y = 0$ and then $x = 0$; for $z^2 + 2z - 1 = 0$, $g_3$ gives $y = z$, and $g_1$ gives $x = z$.

**Implicitization of the twisted cubic.** The curve $x = t$, $y = t^2$, $z = t^3$ is the projection of $\mathbf{V}(x - t,\ y - t^2,\ z - t^3) \subseteq \mathbb{Q}^4$ to $(x, y, z)$. The reduced lex basis for $t > x > y > z$ is $\{t - x,\ x^2 - y,\ xy - z,\ xz - y^2,\ y^3 - z^2\}$. Its elements without $t$ give

$$I_1 = \langle x^2 - y,\ xy - z,\ xz - y^2,\ y^3 - z^2 \rangle,$$

the implicit equations of the curve. Here the projection is already closed, since each point $(a, a^2, a^3)$ comes from $t = a$.

**A projection that is not closed.** Let $I = \langle xy - 1 \rangle \subseteq \mathbb{C}[x, y]$. Its reduced lex basis is $\{xy - 1\}$, which has no element without $x$, so $I_1 = \{0\}$ and $\mathbf{V}(I_1) = \mathbb{C}$. But the projection of the hyperbola $xy = 1$ to the $y$-axis is $\mathbb{C} \setminus \{0\}$. The partial solution $y = 0$ does not extend, and the extension theorem predicts this: the leading coefficient of $xy - 1$ in $x$ is $y$, which vanishes at $y = 0$.

**A wrong order.** For $I = \langle x^3 - 2xy,\ x^2 y - 2y^2 + x \rangle$ the grlex basis $\{x^2, xy, y^2 - \tfrac12 x\}$ has no element in $\mathbb{Q}[y]$, but $I_1 = \langle y^3 \rangle$, as the lex basis $\{x - 2y^2, y^3\}$ shows. A basis for an order that is not an elimination order does not give the elimination ideal.

## Where it is used

- [Polynomial system solving](/polynomial-system-solving/): a lex basis of a zero-dimensional ideal is triangular, so the solutions follow by solving univariate polynomials and back substitution.
- Implicitization: the equations of the image of a polynomial or rational map, as for the twisted cubic.
- Intersections and quotients of ideals: $I \cap J$ is the elimination ideal of $t$ in $tI + (1 - t)J$, computed with one extra variable (Cox, Little and O'Shea, Chapter 4, Section 3).
- [Triangular decomposition](/triangular-decomposition/) and [characteristic sets](/characteristic-set/) build the same triangular shape by other means.
- [Quantifier elimination](/quantifier-elimination/) over the complex numbers is projection, and so it is elimination plus the closure and extension theorems.

## References
