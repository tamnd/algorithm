---
tag: KGFV5X
kind: abstract-type
slug: ore-algebra
name: Ore algebra
aliases:
- skew polynomial ring
- Ore polynomials
- Ore extension
- ring of linear operators
area: algebra/computer-algebra
level: research
summary: Non-commutative polynomial ring of operators with a commutation rule, used for linear differential and recurrence operators.
prereqs: [polynomial-ring, polynomial-division, polynomial-euclidean-algorithm]
see_also: [holonomic-function, creative-telescoping, zeilberger-algorithm, petkovsek-hyper-algorithm, kovacic-algorithm, hypergeometric-term, closed-form-ode-solving, groebner-basis]
sources:
  - paper: "Oystein Ore, Theory of non-commutative polynomials, Annals of Mathematics 34(3), 1933"
    locator: the definition of skew polynomial rings by the rule for a times x, the degree formula, and the left and right Euclidean algorithms with least common multiples
  - paper: doi:10.1006/jsco.1998.0207
    title: Frédéric Chyzak and Bruno Salvy, Non-commutative elimination in Ore algebras proves multivariate identities, Journal of Symbolic Computation 26(2), 187-227, 1998
    locator: the definition of Ore algebras as iterated Ore extensions with commuting operators, the standard examples, and Gröbner bases of left ideals
  - book: isbn:9783709104446
    title: Manuel Kauers and Peter Paule, The Concrete Tetrahedron, Springer, 2011
    locator: Chapter 7, Holonomic sequences and power series (operators for recurrences and differential equations, and their closure properties by least common left multiples)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 3, Differential algebra (differential operators and the noncommutative Euclidean algorithm)
---

An Ore algebra is a ring of polynomials in an operator $\partial$ whose coefficients do not commute with $\partial$: moving $\partial$ past a coefficient $a$ follows a fixed rule $\partial a = \sigma(a)\, \partial + \delta(a)$. With $\delta = d/dx$ it is the ring of linear differential operators, and with $\sigma$ the shift $n \mapsto n + 1$ it is the ring of linear recurrence operators. A linear equation $L f = 0$ is then an element $L$ of the ring, and operations on equations become ring operations: composing equations is multiplication, and finding a common equation for $f + g$ is a least common left multiple. Over a field of coefficients, Ore algebras in one operator have a Euclidean division, so they behave much like $K[x]$, but with the order of factors mattering. They are the setting of [holonomic functions](/holonomic-function/), [creative telescoping](/creative-telescoping/) and the operator view of [Hyper](/petkovsek-hyper-algorithm/) and [Kovacic's algorithm](/kovacic-algorithm/).

## In plain words

A differential equation such as $f'' + x f = 0$ can be written as an operator, "differentiate twice, then add $x$ times the function", applied to $f$. Operators like this can be added and composed, so they form a kind of polynomial arithmetic, with $D$ for "differentiate" in place of a variable. The twist is that $D$ and $x$ do not commute: differentiating $x f$ gives $x f' + f$, so $D x = x D + 1$. Recurrences work the same way with a shift $S$, where $S n = (n + 1) S$. An Ore algebra is this arithmetic, for any such rule. With it, a computer can divide one equation by another, find common factors, and find the smallest equation satisfied by a sum of two solutions.

## Operations

Notation: $A$ is a commutative domain of coefficients, usually $K[x]$ or $K(x)$ for a field $K$ of characteristic $0$; $\sigma \colon A \to A$ is an injective ring endomorphism; and $\delta \colon A \to A$ is a $\sigma$-derivation, that is, additive with $\delta(ab) = \sigma(a)\, \delta(b) + \delta(a)\, b$. The **Ore extension** $A[\partial; \sigma, \delta]$ is the set of finite sums $L = \sum_{i=0}^{r} a_i \partial^i$, with $a_r \ne 0$ the *leading coefficient* and $r = \operatorname{ord} L$ the *order*. An **Ore algebra** in the sense of Chyzak and Salvy is an iterated extension $A[\partial_1; \sigma_1, \delta_1] \cdots [\partial_m; \sigma_m, \delta_m]$ in which the $\partial_j$ commute with each other.

| operation | what it does |
|---|---|
| `add(L, M)` | coefficientwise sum |
| `mul(L, M)` | the product, computed from the rule $\partial a = \sigma(a) \partial + \delta(a)$ |
| `apply(L, f)` | $\sum a_i \partial^i(f)$, for $f$ in a module on which $\partial$ acts, such as functions or sequences |
| `order(L)`, `lc(L)` | the degree in $\partial$ and the leading coefficient |
| `rdiv(L, M)` | for $A$ a field and $\sigma$ an automorphism: $Q, R$ with $L = Q M + R$ and $\operatorname{ord} R < \operatorname{ord} M$ |
| `gcrd(L, M)` | the greatest common right divisor, by the Euclidean algorithm on `rdiv` |
| `lclm(L, M)` | the least common left multiple, by the extended Euclidean algorithm |

Standard instances, each with its commutation rule:

| name | $A$ | $\sigma(a)$ | $\delta(a)$ | rule | acts on |
|---|---|---|---|---|---|
| differential ($D$, Weyl algebra) | $K[x]$ | $a$ | $a'$ | $D x = x D + 1$ | functions, $D f = f'$ |
| Euler ($\theta$) | $K[x]$ | $a$ | $x a'$ | $\theta x = x \theta + x$ | functions, $\theta f = x f'$ |
| shift ($S$) | $K[n]$ | $a(n + 1)$ | $0$ | $S n = (n + 1) S$ | sequences, $(S u)_n = u_{n+1}$ |
| difference ($\Delta$) | $K[n]$ | $a(n + 1)$ | $a(n + 1) - a(n)$ | $\Delta n = (n + 1) \Delta + 1$ | sequences, $\Delta u = S u - u$ |
| $q$-shift ($Q$) | $K(q)[x]$ | $a(qx)$ | $0$ | $Q x = q x Q$ | functions, $(Q f)(x) = f(qx)$ |

**Example.** In the differential case, $D^2 x = x D^2 + 2D$ and $D^3 x^2 = x^2 D^3 + 6x D^2 + 6D$, by the Leibniz rule $D^k a = \sum_j \binom{k}{j} a^{(j)} D^{k-j}$. The two products

$$(D + x)(D - x) = D^2 - x^2 - 1, \qquad (D - x)(D + x) = D^2 - x^2 + 1$$

differ, so the ring is not commutative. Since $(D + x)\, e^{-x^2/2} = 0$, the function $e^{-x^2/2}$ is annihilated by every left multiple of $D + x$, such as $(D - x)(D + x) = D^2 - x^2 + 1$, the operator of the harmonic oscillator.

**A least common left multiple.** $D - 1$ annihilates $e^x$ and $x D - 1$ annihilates $x$. Their least common left multiple is

$$L = (x - 1) D^2 - x D + 1 = \bigl( (x - 1) D - 1 \bigr)(D - 1) = \Bigl( \tfrac{x - 1}{x} D - 1 \Bigr)(x D - 1),$$

so $L$ annihilates $e^x + x$. The second cofactor has a rational coefficient, which is why the Euclidean operations need $A = K(x)$. All products here were checked by a script.

## Laws

Let $L, M$ be nonzero, with $A$ a domain and $\sigma$ injective.

- **Associativity and uniqueness.** For any $(\sigma, \delta)$ as above, there is exactly one associative ring structure on the sums $\sum a_i \partial^i$ that extends the multiplication of $A$ and satisfies $\partial a = \sigma(a) \partial + \delta(a)$ (Ore 1933). The $\sigma$-derivation condition is exactly what associativity of $\partial (ab) = (\partial a) b$ requires.
- **Degree and leading coefficient.** $\operatorname{ord}(LM) = \operatorname{ord} L + \operatorname{ord} M$ and $\operatorname{lc}(LM) = \operatorname{lc}(L)\, \sigma^{\operatorname{ord} L}(\operatorname{lc} M)$. So the ring has no zero divisors.
- **Right division.** If $A$ is a field and $\sigma$ is an automorphism, then for $M \ne 0$ there are unique $Q, R$ with $L = QM + R$ and $\operatorname{ord} R < \operatorname{ord} M$. Each step cancels the leading term with $\frac{\operatorname{lc} L}{\sigma^{s}(\operatorname{lc} M)} \partial^{s} M$ for $s = \operatorname{ord} L - \operatorname{ord} M$. Hence every left ideal is principal, and $\operatorname{gcrd}$ and $\operatorname{lclm}$ exist and are unique up to a left factor in $A$.
- **Order formula.** $\operatorname{ord} \operatorname{lclm}(L, M) + \operatorname{ord} \operatorname{gcrd}(L, M) = \operatorname{ord} L + \operatorname{ord} M$. So a sum of solutions of $L$ and $M$ satisfies an equation of order at most $\operatorname{ord} L + \operatorname{ord} M$.
- **Solutions.** On a module where $\partial$ acts, $\ker(QM) \supseteq \ker M$, and $\ker \operatorname{gcrd}(L, M) = \ker L \cap \ker M$. Right factors of $L$ correspond to subspaces of solutions that are stable under the operator: a hypergeometric solution $t$ of a recurrence $L$ gives the right factor $p(n) S - q(n)$ of order $1$, with $t(n+1)/t(n) = q(n)/p(n)$.
- **Several operators.** In an Ore algebra with $m \ge 2$ operators left ideals need not be principal. Gröbner bases of left ideals, for an order on the monomials $\partial^\alpha$, still exist and are computed by a Buchberger-type algorithm (Chyzak and Salvy 1998).

## Implementations

| implementation | representation | multiplication of order $r$ operators |
|---|---|---|
| dense list of coefficients in $A$ | $(a_0, \ldots, a_r)$ | $O(r^2)$ coefficient products and up to $O(r^2)$ applications of $\sigma$ and $\delta$, naively |
| evaluation and interpolation (differential case) | apply to the basis $x^0, \ldots, x^k$ | near the cost of matrix multiplication of size $r$, for degree comparable to $r$ (van der Hoeven 2002; Bostan, Chyzak and Le Roux 2008) |
| Gröbner bases of left ideals | finite generating sets in several operators | the cost of a noncommutative Buchberger algorithm, with doubly exponential worst case as in the commutative case |

Systems: Maple's OreTools and Mgfun (Chyzak), Koutschan's HolonomicFunctions for Mathematica, and the ore_algebra package for SageMath by Kauers, Jaroschek and Johansson. Coefficient growth is the main practical cost: the Euclidean algorithm over $K(x)$ swells degrees, as in the commutative case, and implementations use fraction-free and modular variants.

## References
