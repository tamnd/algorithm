---
tag: PZY31V
kind: definition
slug: canonical-form
name: Canonical form
aliases:
- normal form for expressions
- canonical simplifier
- canonical representation
area: algebra/computer-algebra
level: core
summary: A unique representative of each equivalence class of expressions, so equality can be tested syntactically.
prereqs: [expression]
see_also: [constant-problem, richardson-theorem, expression-tree, expression-dag, reduced-groebner-basis, dense-polynomial, term-rewriting-system, hash-consing]
sources:
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3, Normal forms and algebraic representations (normal and canonical functions, normal forms for polynomials and rational functions)
  - paper: doi:10.1145/362637.362648
    title: Joel Moses, Algebraic simplification, a guide for the perplexed, Communications of the ACM 14(8), 527-537, 1971
    locator: the classes of simplifiers (radical, conservative, liberal) and the canonical and zero-equivalence properties
  - paper: doi:10.2307/2271358
    title: Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4), 514-520, 1968
    locator: the undecidability of the zero-equivalence problem for expressions with exp, sin, abs, pi and log 2
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 6 (the remainder on division by a Gröbner basis as a normal form for the quotient ring)
---

A canonical form for a class of expressions, under a notion of equivalence, is a computable function that maps equivalent expressions to the same expression and each expression to an equivalent one. With it, two expressions are equivalent exactly when their canonical forms are identical, so equality becomes a comparison of data. A weaker *normal form* only guarantees that every expression equivalent to zero maps to the same zero expression. Computer algebra systems are built on canonical forms where they exist, and Richardson's theorem shows that for expressions with exponentials and sines they cannot exist.

## Definition

Let $E$ be a set of [expressions](/expression/), for example the [expression trees](/expression-tree/) over some constants, variables and operations, and let $\sim$ be an equivalence relation on $E$, for example "equal as functions" or "equal in a ring $R$". Write $e \equiv e'$ when $e$ and $e'$ are identical as data. Following Geddes, Czapor and Labahn (Chapter 3), a computable function $f : E \to E$ is

- a **normal function** if $f(e) \sim e$ for each $e \in E$, and $e \sim 0$ implies $f(e) \equiv f(0)$;
- a **canonical function** if $f(e) \sim e$ for each $e \in E$, and $e_1 \sim e_2$ implies $f(e_1) \equiv f(e_2)$.

The image $f(e)$ is the *normal form* or the *canonical form* of $e$. A canonical function picks one representative of each equivalence class.

**Facts.**

1. *A canonical function is normal.* Take $e_2 = 0$.
2. *A canonical function decides $\sim$.* If $f(e_1) \equiv f(e_2)$, then $e_1 \sim f(e_1) \equiv f(e_2) \sim e_2$. The converse is the definition.
3. *A normal function decides $\sim$ when $E$ has subtraction.* Assume that $E$ is closed under a subtraction with $e_1 \sim e_2 \iff e_1 - e_2 \sim 0$, as in a ring. Then $e_1 \sim e_2$ exactly when $f(e_1 - e_2) \equiv f(0)$. If $e_1 - e_2 \sim 0$, normality gives $f(e_1 - e_2) \equiv f(0)$. If $f(e_1 - e_2) \equiv f(0)$, then $e_1 - e_2 \sim f(e_1 - e_2) \equiv f(0) \sim 0$.

So, for ring-like classes, a normal form is enough to decide equality, but it does not give a unique representative to store, hash or display. The question "is $e \sim 0$?" is the zero-equivalence problem; for constant expressions it is the [constant problem](/constant-problem/).

## Examples and non-examples

**Expanded polynomials (canonical).** For $E$ the expressions built from $+$, $-$, $\times$, integers and the variables $x_1, \ldots, x_n$, with $\sim$ equality in $\mathbb{Z}[x_1, \ldots, x_n]$, let $f$ expand all products, collect equal monomials, drop zero coefficients and sort the terms by a fixed [monomial order](/monomial-ordering/). Then $f$ is canonical, because two polynomials are equal exactly when they have the same coefficient for each monomial. For example $(x + 1)^2 - (x - 1)^2$ and $4x$ both map to the list $[(4, x)]$. The [dense](/dense-polynomial/) and sparse representations are both canonical when they keep their invariants.

**Reduced rational functions (canonical).** For quotients of polynomials over a field $K$, map $p/q$ to $(p/g)/(q/g)$ with $g = \gcd(p, q)$, scaled so that the denominator is monic, with both parts expanded. So $(x^2 - 1)/(x - 1)$ and $(2x + 2)/2$ both map to $(x + 1)/1$. This needs a [polynomial gcd](/polynomial-gcd/) at each step, which is the main cost of rational function arithmetic.

**Expanded numerator, no gcd (normal, not canonical).** Keep $p/q$ with $p$ and $q$ expanded but not reduced. A quotient is zero exactly when the expanded numerator is the zero list, so this is a normal form. It is not canonical: $2x/2$ and $x/1$ are equal but have different forms. Systems use this to postpone the cost of gcds.

**Factored form (canonical, sometimes costly).** A nonzero polynomial over $\mathbb{Q}$ written as a constant times a sorted product of monic irreducible factors with exponents is canonical, by unique factorization. Its size can differ greatly from the expanded form in either direction: $(x + 1)^{100}$ has one factor but 101 terms when expanded, while $x^{100} - 1$ has 2 terms but 9 irreducible factors over $\mathbb{Q}$, the cyclotomic polynomials $\Phi_d$ for the divisors $d \in \{1, 2, 4, 5, 10, 20, 25, 50, 100\}$ of 100. Computing it also needs factorization. The choice between expanded and factored forms is a trade-off of size, not of correctness.

**Remainders by a Gröbner basis (canonical).** For the quotient ring $K[x_1, \ldots, x_n]/I$, the remainder of $f$ on division by a [Gröbner basis](/groebner-basis/) of $I$ is the same for all $f$ in a class, and it is in the class. So it is a canonical form. With the [reduced Gröbner basis](/reduced-groebner-basis/), the function depends only on $I$ and the order.

**Non-example: simplification by rules.** A simplifier that applies $\sin^2 x + \cos^2 x \to 1$ and similar rules until none applies is not canonical in general. It can leave $\sin(2x) - 2 \sin x \cos x$ unchanged, which is zero. A rewrite system is canonical only if it is terminating and confluent, which [Knuth-Bendix completion](/knuth-bendix-completion/) tries to reach.

**Non-example: elementary constants.** For expressions built from integers, $\pi$, $\log 2$, $+$, $\times$, $\exp$, $\sin$ and $|\cdot|$ in one real variable, with $\sim$ equality as functions, Richardson (1968) proved that zero-equivalence is undecidable. So no normal function exists, and no canonical one. Systems therefore give canonical forms for polynomials, rational functions and some algebraic and transcendental extensions, and only heuristic simplification beyond.

### Common errors

- Comparing the printed forms of two expressions after "simplify" assumes that the simplifier is canonical. Most general simplifiers are not.
- A canonical form is defined for one equivalence. Expanded polynomials are canonical for equality in $\mathbb{Z}[x]$, but not for equality of functions on a finite field: $x^p - x$ is zero as a function on $\mathbb{Z}/p\mathbb{Z}$.
- A canonical form need not be small. The expanded form of $(x + y)^{50}$ has 51 terms, while the expression has one.

## Related definitions

- [Symbolic expression](/expression/): the objects on which these functions act.
- [Constant problem](/constant-problem/) and [Richardson's theorem](/richardson-theorem/): when zero-equivalence is decidable and when not.
- [Expression DAG](/expression-dag/) and [hash consing](/hash-consing/): with a canonical form, equal subexpressions can be stored once and compared by pointer.
- [Reduced Gröbner basis](/reduced-groebner-basis/): a canonical form for polynomial ideals, and through remainders for elements of quotient rings.
- [Term rewriting system](/term-rewriting-system/): a confluent and terminating system computes a canonical form for its equational theory.
- [Expression swell](/expression-swell/): the price of canonical forms whose size grows fast.

## References
