---
tag: HDR7FV
kind: problem
slug: ideal-membership-problem
name: Ideal membership problem
aliases:
- polynomial membership in an ideal
- polynomial ideal membership
- radical membership problem
area: algebra/computer-algebra
level: core
summary: Decide whether a given polynomial lies in a given ideal.
model: blum-shub-smale-machine
prereqs: [polynomial-ideal, groebner-basis, multivariate-division-algorithm]
see_also: [buchberger-algorithm, hilbert-nullstellensatz, macaulay-matrix, f4-algorithm, reduced-groebner-basis, polynomial-system-solving]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 6 (ideal membership by the remainder on division by a Gröbner basis) and Section 8 (the worked membership example in k[x, y, z]); Chapter 4, Section 2 (radical membership)
  - paper: doi:10.1016/0001-8708(82)90048-2
    title: Ernst W. Mayr and Albert R. Meyer, The complexity of the word problems for commutative semigroups and polynomial ideals, Advances in Mathematics 46(3), 305-329, 1982
    locator: the exponential space lower bound and the ideals that need cofactors of doubly exponential degree
  - paper: "Grete Hermann, Die Frage der endlich vielen Schritte in der Theorie der Polynomideale, Mathematische Annalen 95, 1926"
    locator: the doubly exponential degree bound for the cofactors of a member of an ideal
  - paper: "Ernst W. Mayr, Membership in polynomial ideals over Q is exponential space complete, STACS 89, Lecture Notes in Computer Science 349, Springer, 1989"
    locator: the exponential space upper bound
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Section 21.7 (the complexity of computing Gröbner bases, with the Mayr and Meyer lower bound)
  - paper: "Daniel Lazard, Gröbner bases, Gaussian elimination and resolution of systems of algebraic equations, EUROCAL 83, Lecture Notes in Computer Science 162, Springer, 1983"
    locator: the degree bound for the grevlex basis of a homogeneous regular sequence and the reduction of Gröbner bases to linear algebra
  - paper: "Y. N. Lakshman, A single exponential bound on the complexity of computing Gröbner bases of zero dimensional ideals, in Effective Methods in Algebraic Geometry (MEGA 90), Progress in Mathematics 94, Birkhäuser, 1991"
    locator: the main theorem
  - paper: "Pascal Koiran, Hilbert's Nullstellensatz is in the polynomial hierarchy, Journal of Complexity 12, 1996"
    locator: the complexity of deciding whether a system has a complex solution
---

The ideal membership problem asks whether a polynomial $f$ lies in the [ideal](/polynomial-ideal/) $\langle f_1, \ldots, f_s \rangle$ of $K[x_1, \ldots, x_n]$, that is, whether $f = h_1 f_1 + \cdots + h_s f_s$ for some polynomials $h_i$. In one variable the [gcd](/polynomial-gcd/) answers it at once. In several variables the standard method computes a [Gröbner basis](/groebner-basis/) and checks that the remainder of [multivariate division](/multivariate-division-algorithm/) is zero. The problem is decidable, but in the worst case it needs exponential space, and the cofactors $h_i$ can need doubly exponential degree (Mayr and Meyer, 1982).

## In plain words

You have a few polynomial equations and one more polynomial. The question is whether the extra polynomial is a consequence of the equations in the strongest algebraic sense: can you build it by multiplying each equation by some polynomial and adding the results? If yes, the extra polynomial is zero at every common solution of the equations. With one variable the answer comes from one greatest common divisor. With several variables you first rewrite the equations into a special form, and then a division answers the question. The rewriting can be very expensive in the worst case.

## Definition

**Input.** A field $K$ in which we can compute exactly (for example $\mathbb{Q}$ or $\mathbb{F}_p$), polynomials $f_1, \ldots, f_s \in K[x_1, \ldots, x_n]$ and $f \in K[x_1, \ldots, x_n]$. Let $d$ be the largest total degree of the $f_i$.

**Output.** "Yes" when $f \in I = \langle f_1, \ldots, f_s \rangle$, that is, when there are $h_1, \ldots, h_s \in K[x_1, \ldots, x_n]$ with

$$f = h_1 f_1 + \cdots + h_s f_s,$$

and "no" otherwise. The answer does not change when $K$ is replaced by an extension field $L$, because the reduced Gröbner basis of $I$ is the same over $K$ and over $L$.

**Search version.** When the answer is yes, output cofactors $h_1, \ldots, h_s$. They are a certificate: anyone can check the identity by expanding it. The cofactors are not unique: one can add any syzygy, a tuple $(g_i)$ with $\sum g_i f_i = 0$.

## Variants

- **Radical membership.** Decide whether $f \in \sqrt{I}$, that is, whether $f$ vanishes on $V(I)$ over the algebraic closure. By the [Nullstellensatz](/hilbert-nullstellensatz/) this holds exactly when $1 \in \langle f_1, \ldots, f_s, 1 - yf \rangle$ in $K[x_1, \ldots, x_n, y]$.
- **The Nullstellensatz problem.** Decide whether $1 \in I$, that is, whether the system $f_1 = \cdots = f_s = 0$ has no solution over $\bar K$. It is the special case $f = 1$.
- **One variable.** $f \in \langle f_1, \ldots, f_s \rangle$ exactly when $g = \gcd(f_1, \ldots, f_s)$ divides $f$. The [Euclidean algorithm](/polynomial-euclidean-algorithm/) decides it with $O(d^2)$ field operations for $s = 2$.
- **Monomial ideals.** If each $f_i$ is a monomial, $f \in I$ exactly when each term of $f$ is divisible by some $f_i$. This costs $O(t s n)$ exponent comparisons for $t$ terms.
- **An ideal given by a Gröbner basis.** Then membership is one division, with the bounds of the [division algorithm](/multivariate-division-algorithm/). The hard part of the general problem is the basis.
- **Bounded-degree membership.** Decide whether cofactors with $\deg(h_i f_i) \le D$ exist. This is a linear system over $K$, the [Macaulay matrix](/macaulay-matrix/) of degree $D$.
- **Binomial ideals.** All $f_i$ are differences of two monomials. This case already contains the word problem for commutative semigroups, and it carries the Mayr and Meyer lower bound.

## Examples

**One variable.** In $\mathbb{Q}[x]$, $\langle x^4 - 1, x^6 - 1 \rangle = \langle x^2 - 1 \rangle$. So $x^3 - x = x(x^2 - 1)$ is a member, and $x - 1$ is not, because it has degree $1 < 2$.

**A yes instance with a Gröbner basis.** Let $I = \langle xz - y^2, x^3 - z^2 \rangle \subseteq \mathbb{Q}[x, y, z]$ with grlex and $x > y > z$. The reduced Gröbner basis is

$$G = \{xz - y^2,\ x^3 - z^2,\ x^2 y^2 - z^3,\ x y^4 - z^4,\ y^6 - z^5\}.$$

The polynomial $f = -4x^2 y^2 z^2 + y^6 + 3z^5$ has remainder $0$ on division by $G$, so $f \in I$. The polynomial $x y^3 - 1$ has remainder $x y^3 - 1$, since no leading term of $G$ divides $x y^3$ or $1$, so it is not in $I$. This is the example of Cox, Little and O'Shea, Chapter 2, Section 8.

**Division without a Gröbner basis can mislead.** Let $I = \langle xy + 1, y^2 - 1 \rangle \subseteq \mathbb{Q}[x, y]$ with lex. The polynomial $f = xy^2 - x = x(y^2 - 1)$ is in $I$, but its remainder on division by $(xy + 1, y^2 - 1)$ in this order is $-x - y \ne 0$. The reduced Gröbner basis is $\{x + y, y^2 - 1\}$, and modulo it $f$ has remainder $0$, while $x$ has remainder $-y$, so $x \notin I$.

**Radical but not ideal membership.** $I = \langle x^2, y^2 \rangle$ and $f = x + y$: $f \notin I$, but $f^3 \in I$, so $f \in \sqrt{I}$. The ideal $\langle x^2, y^2, 1 - t(x + y) \rangle$ has reduced Gröbner basis $\{1\}$.

## Known algorithms

- [Buchberger's algorithm](/buchberger-algorithm/), then [division](/multivariate-division-algorithm/) by the basis. The output also gives cofactors, if the algorithm records how each basis element is a combination of the inputs.
- The [F4 algorithm](/f4-algorithm/) and the [F5 algorithm](/f5-algorithm/), which compute the same Gröbner basis by linear algebra and avoid most useless reductions. See [Gröbner basis computation](/groebner-basis-computation/).
- Linear algebra in bounded degree: solve the [Macaulay matrix](/macaulay-matrix/) system for $D = \deg f + B$, where $B$ is a degree bound for the cofactors. With Hermann's bound this is doubly exponential, and with Kollár's bound for $f = 1$ it is single exponential.
- For one variable, the [polynomial gcd](/polynomial-gcd/), then one division.

## Bounds

The costs are in field operations over $K$ unless stated otherwise. For $K = \mathbb{Q}$ the complexity class results are in the Turing machine model with the input in binary.

- **Upper bound on the cofactors (Hermann, 1926).** If $f \in I$, there are cofactors with a bound of the form $\deg h_i \le \deg f + (sd)^{2^n}$. The original argument had gaps that later authors repaired. With this bound, membership is a linear system of doubly exponential size, so it is decidable.
- **Lower bound (Mayr and Meyer, 1982).** There are ideals generated by binomials of bounded degree in $n$ variables for which some member $f$ of small degree needs cofactors of degree $2^{2^{cn}}$ for a constant $c > 0$. Membership over $\mathbb{Q}$ is hard for exponential space.
- **Upper bound (Mayr, 1989).** Membership over $\mathbb{Q}$ can be decided in exponential space, so the problem is EXPSPACE-complete.
- **Gröbner bases.** The degrees in a Gröbner basis can also be doubly exponential in $n$ in the worst case, so the Gröbner method inherits the doubly exponential worst case. For better cases more is known. For a homogeneous regular sequence of degrees $d_1, \ldots, d_n$ in generic coordinates, the grevlex basis has degree at most $\sum_i (d_i - 1) + 1$, the Macaulay bound (Lazard, 1983). For zero-dimensional ideals, Lakshman (1991) showed that a Gröbner basis can be computed with $d^{O(n)}$ field operations, a single exponential bound.
- **The Nullstellensatz problem.** For $f = 1$ the cofactors need only degree $\max(3, d)^n$ (Kollár, 1988, see the [Nullstellensatz](/hilbert-nullstellensatz/) page), so the problem is single exponential. It is NP-hard (see Reductions), and it lies in PSPACE, by this degree bound and fast parallel linear algebra. Koiran (1996) showed that over $\mathbb{C}$ it lies in the polynomial hierarchy if the generalized Riemann hypothesis holds.

## Reductions

- **Radical membership to the Nullstellensatz problem.** $f \in \sqrt{I}$ exactly when $1 \in \langle I, 1 - yf \rangle$: one extra variable and one extra generator.
- **Satisfiability to the Nullstellensatz problem.** For a formula in conjunctive normal form, take the equations $x_i^2 - x_i = 0$, and for each clause the product of $(1 - x_i)$ over its positive literals and $x_j$ over its negative literals. A common zero is a 0 or 1 vector that satisfies each clause, so the system is consistent exactly when the formula is satisfiable. The degrees are at most the clause length, so 3-SAT gives degree 3. This shows that the Nullstellensatz problem is NP-hard.
- **Membership to linear algebra.** For a degree bound $D$, membership with $\deg(h_i f_i) \le D$ is the question of whether the coefficient vector of $f$ lies in the row space of the Macaulay matrix of degree $D$. Its size is about $s \binom{n + D}{n}$ by $\binom{n + D}{n}$.
- **Commutative semigroup words to binomial membership.** Mayr and Meyer encode the word problem for a finitely presented commutative semigroup as the membership of a binomial in a binomial ideal. Their lower bound for the word problem then transfers to ideal membership.

## Applications

- **Consistency of a system.** Is $1 \in I$? See [polynomial system solving](/polynomial-system-solving/).
- **Arithmetic in quotient rings.** Equality in $K[x_1, \ldots, x_n]/I$ is membership of the difference.
- **Geometric theorem proving.** A hypothesis given by polynomial equations implies a conclusion $g = 0$ on the generic part when $g$ lies in the radical of the hypothesis ideal, after the degenerate cases are removed.
- **Implicitization and elimination.** Testing whether a candidate equation vanishes on a parametrized set is a membership test in an [elimination ideal](/elimination-ideal/).
- **Verification.** A certificate $f = \sum h_i f_i$ is a short proof that a polynomial identity follows from the hypotheses. Proof systems in complexity theory, such as the Nullstellensatz proof system, measure the degree of such certificates.

## References
