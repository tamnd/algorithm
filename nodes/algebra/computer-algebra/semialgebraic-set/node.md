---
tag: EYCZPM
kind: definition
slug: semialgebraic-set
name: Semialgebraic set
aliases: [semialgebraic, semi-algebraic set, semialgebraic subset, basic semialgebraic set]
area: algebra/computer-algebra
level: advanced
summary: A subset of R^n defined by finitely many polynomial equalities and inequalities.
prereqs: [real-closed-field, polynomial-ring]
see_also: [tarski-seidenberg-theorem, quantifier-elimination, cylindrical-algebraic-decomposition, real-closed-field, hilbert-nullstellensatz, semidefinite-programming, sturm-theorem]
sources:
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 3, Semi-Algebraic Sets, Chapter 5, Decomposition of Semi-Algebraic Sets, and Chapter 7, Quantitative Semi-algebraic Geometry
  - book: isbn:9783540646631
    title: Jacek Bochnak, Michel Coste and Marie-Françoise Roy, Real Algebraic Geometry, Springer, 1998
    locator: Chapter 2, Semi-algebraic Sets
  - book: isbn:9780521598385
    title: Lou van den Dries, Tame Topology and o-minimal Structures, London Mathematical Society Lecture Note Series 248, Cambridge University Press, 1998
    locator: Chapter 1 (o-minimal structures, with the semialgebraic sets as the main example)
  - paper: doi:10.1090/S0002-9939-1964-0161339-9
    title: John Milnor, On the Betti numbers of real varieties, Proceedings of the American Mathematical Society 15(2), 1964
    locator: pp. 275 to 280
  - paper: doi:10.2307/2374240
    title: Robert M. Hardt, Semi-algebraic local-triviality in semi-algebraic mappings, American Journal of Mathematics 102(2), 1980
    locator: p. 291 onward (the local triviality theorem)
---

## Definition

Let $R$ be a [real closed field](/real-closed-field/), for example $\mathbb{R}$, and $R[x_1, \ldots, x_n]$ the [polynomial ring](/polynomial-ring/). A subset $S \subseteq R^n$ is *semialgebraic* if it is a finite Boolean combination (finite unions, finite intersections and complements) of sets of the form

$$\{x \in R^n : P(x) > 0\} \quad \text{or} \quad \{x \in R^n : P(x) = 0\}, \qquad P \in R[x_1, \ldots, x_n].$$

**Normal form.** Every semialgebraic set is a finite union of *basic* semialgebraic sets

$$\{x \in R^n : P(x) = 0, \; Q_1(x) > 0, \; \ldots, \; Q_\ell(x) > 0\},$$

with one equation, because $P_1 = \cdots = P_r = 0$ is the same as $P_1^2 + \cdots + P_r^2 = 0$ over an ordered field. Bring the Boolean combination to disjunctive normal form, write $P \ne 0$ as $P > 0 \vee -P > 0$ and $P \ge 0$ as $P > 0 \vee P = 0$, and merge the equations.

**Equivalent form.** $S$ is semialgebraic exactly when $S = \{x : \Phi(x)\}$ for a first-order formula $\Phi$ in the language of ordered fields with coefficients in $R$, with or without quantifiers. The direction from formulas with quantifiers to sets is the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/), which removes the quantifiers by [quantifier elimination](/quantifier-elimination/).

**Semialgebraic maps.** A map $f : S \to R^m$ on a semialgebraic set $S$ is semialgebraic if its graph is a semialgebraic subset of $R^{n+m}$.

**Closure properties.** The semialgebraic sets are closed under finite Boolean operations (by definition), products, projections $R^{n+1} \to R^n$ (Tarski-Seidenberg), images and preimages under semialgebraic maps, and topological closure and interior (because "$x$ is in the closure of $S$" is the first-order formula $\forall \varepsilon > 0 \; \exists y \in S \; |x - y|^2 < \varepsilon^2$).

## Examples and non-examples

- **Intervals.** $\{x \in \mathbb{R} : x^2 < 2\} = (-\sqrt 2, \sqrt 2)$, and $\{x : x^2 \ge 1\} = \{x^2 - 1 = 0\} \cup \{x^2 - 1 > 0\} = (-\infty, -1] \cup [1, \infty)$.
- **Subsets of the line.** The semialgebraic subsets of $R$ are exactly the finite unions of points and open intervals with ends in $R \cup \{\pm\infty\}$: the sign of each polynomial is constant between its finitely many roots. This property, for every definable subset of the line, is what *o-minimal* means.
- **Algebraic sets.** The zero set of any family of polynomials is semialgebraic: by the Hilbert basis theorem it is cut out by finitely many, and then by one sum of squares.
- **A projection.** The circle $\{x^2 + y^2 = 1\}$ is algebraic, and its projection to the $y$-axis is $[-1, 1] = \{1 - y^2 > 0\} \cup \{1 - y^2 = 0\}$. This is semialgebraic but not algebraic, since a nonzero polynomial in $y$ has only finitely many roots. So projections leave the class of real algebraic sets, but not the class of semialgebraic sets.
- **An image.** $\{x^2 : x \in \mathbb{R}\} = [0, \infty)$, the image of a polynomial map.
- **A parameter set.** The set of $(a, b, c) \in \mathbb{R}^3$ for which $a x^2 + b x + c$ has a real root is semialgebraic: quantifier elimination gives $(a \ne 0 \wedge b^2 - 4ac \ge 0) \vee (a = 0 \wedge b \ne 0) \vee (a = b = c = 0)$.
- **Non-example: the integers.** $\mathbb{Z} \subset \mathbb{R}$ is not semialgebraic, because it has infinitely many connected components (see the finiteness property below), and it is not a finite union of points and intervals.
- **Non-example: the sine curve.** $\{(x, \sin x)\}$ meets the semialgebraic line $y = 0$ in the infinite discrete set $\pi \mathbb{Z}$, so it is not semialgebraic.
- **Non-example: the exponential.** The graph of $e^x$ is not semialgebraic. A semialgebraic function of one variable satisfies a nonzero polynomial equation $P(x, f(x)) = 0$ and so grows at most like a power of $x$, while $e^x$ grows faster than every power.

## Related definitions

- **Real algebraic set.** $\{x \in R^n : P_1 = \cdots = P_r = 0\}$, the semialgebraic sets defined by equations only.
- **Sign condition.** A map $\sigma : \{P_1, \ldots, P_s\} \to \{-1, 0, 1\}$, and its *realization* $\{x : \operatorname{sign} P_i(x) = \sigma(P_i)\}$. The realizable sign conditions of a family split $R^n$ into semialgebraic pieces, and counting them is a basic problem of the quantitative theory.
- **Semialgebraically connected.** $S$ is semialgebraically connected if it is not the disjoint union of two nonempty semialgebraic sets that are closed in $S$. Over $\mathbb{R}$ this is the same as connected. Every semialgebraic set has finitely many semialgebraically connected components, and each is semialgebraic.
- **Cell decomposition.** Every semialgebraic set is a finite disjoint union of cells, each semialgebraically homeomorphic to an open cube $(0, 1)^k$; a [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) computes one. The largest such $k$ is the *dimension* of $S$.
- **Quantitative bounds.** Milnor (1964) proved that the zero set in $\mathbb{R}^n$ of polynomials of degree at most $d$ has total Betti number at most $d (2d - 1)^{n-1}$, so in particular at most that many connected components. Basu, Pollack and Roy give bounds of the same kind for all realizable sign conditions of $s$ polynomials, polynomial in $s$ and singly exponential in $n$.
- **Semialgebraic triviality.** Hardt (1980) proved that a semialgebraic map is trivial, as a projection of a product, over each piece of a finite semialgebraic partition of its target. So a family of semialgebraic sets with parameters has finitely many topological types.
- **Constructible set.** The analogue over an algebraically closed field: a finite Boolean combination of sets $\{P = 0\}$. Chevalley's theorem says projections of constructible sets are constructible.
- **Semialgebraic function, Nash function, o-minimal structure.** A function with semialgebraic graph; a smooth semialgebraic function; and the axiomatic generalization of semialgebraic geometry to larger families of sets, such as those definable with $e^x$.

## References
