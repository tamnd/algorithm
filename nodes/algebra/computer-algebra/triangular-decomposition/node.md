---
tag: KC4W9H
kind: concept
slug: triangular-decomposition
name: Triangular decomposition
aliases: [triangular set decomposition, decomposition into triangular sets, decomposition into regular chains, Wu-Ritt decomposition]
area: algebra/computer-algebra
level: advanced
summary: Writes a polynomial system as a finite union of triangular systems.
prereqs: [polynomial-ideal, pseudo-division, characteristic-set]
see_also: [regular-chain, wu-characteristic-set-method, groebner-basis, lazard-structure-theorem, elimination-ideal, primary-decomposition, rational-univariate-representation, hilbert-nullstellensatz]
sources:
  - paper: doi:10.1007/BF02328447
    title: Wu Wen-Tsun, Basic principles of mechanical theorem proving in elementary geometries, Journal of Automated Reasoning 2(3), 1986
    locator: pp. 221 to 252 (characteristic sets and the zero decomposition)
  - paper: doi:10.1016/0166-218X(91)90113-B
    title: Daniel Lazard, A new method for solving algebraic systems of positive dimension, Discrete Applied Mathematics 33(1-3), 1991
    locator: pp. 147 to 160
  - paper: doi:10.1016/S0747-7171(08)80086-7
    title: Daniel Lazard, Solving zero-dimensional algebraic systems, Journal of Symbolic Computation 13(2), 1992
    locator: pp. 117 to 131 (triangular sets from a lexicographic Gröbner basis)
  - paper: doi:10.1006/jsco.1993.1011
    title: Michael Kalkbrener, A generalized Euclidean algorithm for computing triangular representations of algebraic varieties, Journal of Symbolic Computation 15(2), 1993
    locator: pp. 143 to 167
  - paper: doi:10.1006/jsco.1999.0269
    title: Philippe Aubry, Daniel Lazard and Marc Moreno Maza, On the theories of triangular sets, Journal of Symbolic Computation 28(1-2), 1999
    locator: pp. 105 to 124 (comparison of the definitions of Wu, Lazard, Kalkbrener and others)
  - paper: doi:10.1007/3-540-45084-X_1
    title: Evelyne Hubert, Notes on triangular sets and triangulation-decomposition algorithms I, Polynomial systems, Symbolic and Numerical Scientific Computation, Lecture Notes in Computer Science 2630, 2003
    locator: pp. 1 to 39
  - paper: doi:10.1016/j.jsc.2011.12.023
    title: Changbo Chen and Marc Moreno Maza, Algorithms for computing triangular decomposition of polynomial systems, Journal of Symbolic Computation 47(6), 2012
    locator: pp. 610 to 642
  - paper: doi:10.1145/1005285.1005302
    title: Xavier Dahan and Éric Schost, Sharp estimates for triangular sets, ISSAC 2004
    locator: pp. 103 to 110
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 6, Section 5, Wu's Method
---

## In plain words

A system of polynomial equations in several unknowns is hard to read directly. A triangular system is easy to read: the first equation has only the first unknown, the second adds one more unknown, and so on. To solve it, solve the first equation, put each solution into the second, and continue, as with a triangular linear system.

Most systems are not triangular, and one triangular system is often not enough, because the solutions can fall into pieces of different shapes: a curve here, a few points there. A triangular decomposition writes the set of all solutions as a finite union of solution sets of triangular systems. Each piece is simple, and together they give all solutions and no others. Computing one needs only polynomial division and greatest common divisors, with a split into cases each time a coefficient can be zero or not.

## The idea

**Notation.** $K$ is a field of characteristic $0$ (the theory also works over other fields, with care for separability), $\overline{K}$ an algebraic closure, and $K[x_1, \ldots, x_n]$ the polynomial ring with the variable order $x_1 < x_2 < \cdots < x_n$. For a nonconstant $p$, the *main variable* $\operatorname{mvar}(p)$ is the largest variable in $p$, and the *initial* $\operatorname{init}(p)$ is the leading coefficient of $p$ as a polynomial in its main variable. This is the recursive view of $p$, not a monomial order with $\mathrm{LT}$ and $\mathrm{LC}$.

**Triangular sets.** A *triangular set* is a finite set $T = \{t_1, \ldots, t_m\}$ of nonconstant polynomials with pairwise different main variables. Let $h_T$ be the product of the initials. Two objects are attached to $T$:

- the *quasi-component* $W(T) = V(T) \setminus V(h_T) \subseteq \overline{K}^n$, the common zeros of $T$ where no initial vanishes;
- the *saturated ideal* $\operatorname{sat}(T) = (T) : h_T^{\infty} = \{ f : h_T^k f \in (T) \text{ for some } k \}$.

The variables that are not main variables of $T$ are *free*. On $W(T)$ they can take any value for which the initials do not vanish, and then each main variable is a root of a univariate polynomial whose coefficients are already fixed. This is the triangular reading of the solutions.

**Regular chains.** A triangular set is a *regular chain* if, for each $i$, the initial of $t_i$ is not a zero divisor modulo $\operatorname{sat}(t_1, \ldots, t_{i-1})$ (Kalkbrener 1993; Yang and Zhang). Then $\operatorname{sat}(T)$ is unmixed of dimension $n - m$ (each component has this dimension), and membership in $\operatorname{sat}(T)$ is decided by pseudo-division: $f \in \operatorname{sat}(T)$ exactly when the pseudo-remainder of $f$ by $T$ is $0$. The [regular chain](/regular-chain/) page treats this data structure.

**Two kinds of decomposition.** For a finite $F \subset K[x_1, \ldots, x_n]$ with zero set $V(F) \subseteq \overline{K}^n$, finitely many regular chains $T_1, \ldots, T_e$ form

- a *Lazard decomposition* (or Wu-Ritt type) if $V(F) = W(T_1) \cup \cdots \cup W(T_e)$, an exact union of quasi-components;
- a *Kalkbrener decomposition* if $V(F) = \overline{W(T_1)} \cup \cdots \cup \overline{W(T_e)}$, with Zariski closures, which is the same as $\sqrt{(F)} = \bigcap_i \sqrt{\operatorname{sat}(T_i)}$.

Kalkbrener decompositions are coarser and often shorter. Lazard decompositions describe every point, including points where initials vanish. Wu's characteristic set method gives a decomposition of the first kind with triangular sets that need not be regular chains.

**How they are computed.** All algorithms are built from two operations. *Pseudo-division* by $T$ reduces a polynomial to one that is reduced with respect to each $t_i$. A *GCD modulo a regular chain* computes the GCD of two polynomials in $x_k$ with coefficients in $K[x_1, \ldots, x_{k-1}] / \operatorname{sat}(T)$. This ring is not a field and not a domain, so the Euclidean algorithm can meet a leading coefficient that is a zero divisor. Then the chain *splits* into two chains, one where that coefficient is $0$ and one where it is invertible, and the computation continues on each. This case split is the same idea as dynamic evaluation (the D5 principle of Della Dora, Dicrescenzo and Duval). The incremental algorithm of Moreno Maza and of Chen and Moreno Maza (2012) adds the equations one at a time and splits with these two operations. Wu's method uses repeated pseudo-division instead of GCDs.

**Relation to Gröbner bases.** For a zero-dimensional radical ideal in general position, the reduced [Gröbner basis](/groebner-basis/) for lex with $x_1 < \cdots < x_n$ is a single triangular set $\{q(x_1), x_2 - v_2(x_1), \ldots, x_n - v_n(x_1)\}$ (the shape lemma). In general, a lex Gröbner basis of a zero-dimensional ideal has a triangular structure by [Lazard's structure theorem](/lazard-structure-theorem/), and Lazard (1992) extracts a triangular decomposition from it. A triangular decomposition is weaker than a [primary decomposition](/primary-decomposition/): its components need not be prime, and in the Lazard form they can overlap. But it is computed without factoring polynomials, so it works over $\mathbb{Q}$ with only rational arithmetic.

**Size.** The number of components and their degrees obey Bézout-type bounds: for $n$ equations of degree at most $d$ in $n$ variables, a zero-dimensional decomposition has total degree at most $d^n$. Dahan and Schost (2004) bounded the coefficient size in the triangular sets of a zero-dimensional decomposition and showed that a different representation, with a common denominator taken from derivatives, makes the coefficients much smaller. The running time of the decomposition algorithms in use is not well bounded in the worst case, because the splits can repeat many times; in practice they are often competitive with Gröbner bases on systems with many components.

## Examples

- **A system that splits.** Over $\mathbb{Q}$ with $x < y$, let $F = \{x^2 - x, \; xy - x\}$. This $F$ is already a reduced lex Gröbner basis, but it is not one triangular set: both polynomials are tied to the factor structure of $x^2 - x$. The initial of $xy - x$ is $x$, which is a zero divisor modulo $(x^2 - x)$, since $\gcd(x, x^2 - x) = x$. The split gives two cases. If $x = 0$, then $xy - x$ vanishes and the chain is $T_1 = \{x\}$, with $y$ free. If $x - 1 = 0$, then the initial $x$ is invertible and $xy - x$ becomes $y - 1$, so $T_2 = \{x - 1, \; y - 1\}$. So $V(F) = \{x = 0\} \cup \{(1, 1)\}$, a line and a point, and $\{T_1, T_2\}$ is both a Lazard and a Kalkbrener decomposition.
- **Lazard and Kalkbrener differ.** With $x < y < z$, let $F = \{x z - y\}$. The single chain $T = \{x z - y\}$ has initial $x$, so $W(T)$ is the surface without its points with $x = 0$. Since $x z - y$ is irreducible, $\overline{W(T)} = V(F)$, and $\{T\}$ is a Kalkbrener decomposition. But $V(F)$ also contains the line $x = y = 0$ with $z$ free, which is not in $W(T)$, so a Lazard decomposition is $\{x z - y\}, \{x, y\}$.
- **Shape position.** With $x < y$, $F = \{x^2 + y^2 - 1, \; y - x\}$ has the decomposition $\{2x^2 - 1, \; y - x\}$: one regular chain, which is also the lex Gröbner basis. The two solutions are $x = y = \pm 1/\sqrt 2$, read off from the first polynomial and then the second.
- **A union of two lines.** $F = \{xy\}$ with $x < y$: the chains $\{x\}$ (with $y$ free) and $\{y\}$ (with $x$ free, main variable $y$, initial $1$) give $V(F) = \{x = 0\} \cup \{y = 0\}$.

## Where it is used

- **Solving polynomial systems.** Triangular decompositions are the output format of the `RegularChains` library in Maple and of several solvers, and they feed [real root isolation](/real-root-isolation/) of triangular systems, one variable at a time.
- **Geometry theorem proving.** [Wu's characteristic set method](/wu-characteristic-set-method/) proves theorems of elementary geometry by reducing the conclusion with a triangular set built from the hypotheses, and the initials give the nondegeneracy conditions.
- **Real algebraic geometry.** Triangular decompositions combined with sign conditions describe [semialgebraic sets](/semialgebraic-set/) and give an alternative route to [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/).
- **Computing modulo a triangular set.** Arithmetic in $K[x_1, \ldots, x_n] / (T)$ for a zero-dimensional regular chain (towers of extensions) is used in algebraic number computation, with fast algorithms by Li, Moreno Maza and Schost.
- **Differential algebra.** Ritt's characteristic sets and the Rosenfeld-Gröbner algorithm decompose systems of differential equations in the same triangular way.

## References
