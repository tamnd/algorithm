---
tag: 8WAC7J
kind: problem
slug: primary-decomposition
name: Primary decomposition
aliases:
- minimal primary decomposition
- Lasker-Noether decomposition
- irredundant primary decomposition
area: algebra/computer-algebra
level: advanced
summary: Write an ideal as an intersection of primary ideals.
model: blum-shub-smale-machine
prereqs: [polynomial-ideal, groebner-basis, polynomial-factorization, hilbert-nullstellensatz]
see_also: [hilbert-basis-theorem, lazard-structure-theorem, triangular-decomposition, polynomial-system-solving, elimination-theorem, hilbert-series, ideal-membership-problem, regular-chain]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 4, Section 3 (sums, products and intersections of ideals), Section 4 (ideal quotients and saturations), Section 6 (decomposition of a variety into irreducibles) and Section 8 (primary decomposition of ideals, the Lasker-Noether theorem)
  - book: isbn:9780201003611
    title: Michael F. Atiyah and Ian G. Macdonald, Introduction to Commutative Algebra, Addison-Wesley, 1969
    locator: Chapter 4, Primary decomposition (the uniqueness theorems for associated primes and isolated components) and Chapter 7 (existence in Noetherian rings)
  - paper: "Patrizia Gianni, Barry Trager and Gail Zacharias, Gröbner bases and primary decomposition of polynomial ideals, Journal of Symbolic Computation 6(2-3), 1988"
    locator: the reduction to the zero-dimensional case and the algorithm by factoring and saturation
  - paper: "David Eisenbud, Craig Huneke and Wolmer Vasconcelos, Direct methods for primary decomposition, Inventiones Mathematicae 110, 1992"
    locator: the equidimensional and homological methods
  - book: isbn:9783540735410
    title: Gert-Martin Greuel and Gerhard Pfister, A Singular Introduction to Commutative Algebra, second edition, Springer, 2008
    locator: Chapter 4, Primary decomposition and related topics (the algorithms of Gianni, Trager and Zacharias and of Shimoyama and Yokoyama, and the radical)
---

Primary decomposition asks to write an ideal $I$ of $K[x_1, \ldots, x_n]$ as an intersection $I = Q_1 \cap \cdots \cap Q_r$ of primary ideals, the analogue for ideals of factoring an integer into prime powers. Geometrically, the radicals $\sqrt{Q_i}$ give the irreducible components of $V(I)$, together with embedded components that record extra multiplicity structure. The Lasker-Noether theorem says a decomposition always exists, and the set of radicals of an irredundant one is unique. The components themselves are unique for the minimal primes and not, in general, for the embedded ones. Algorithms reduce to the zero-dimensional case, where a generic linear form and one [polynomial factorization](/polynomial-factorization/) split the ideal, and they glue the pieces with [Gröbner basis](/groebner-basis/) operations such as intersections and saturations. In one variable the problem is exactly polynomial factorization. In general it is at least as hard, and its Gröbner steps have the doubly exponential worst case of Mayr and Meyer.

## In plain words

An integer splits into prime powers, like $360 = 2^3 \cdot 3^2 \cdot 5$. A system of polynomial equations splits in a similar way. Its solution set is a union of pieces, such as points, curves and surfaces, that cannot be split further. Primary decomposition splits the equations themselves, not just the solution set. It also keeps track of how "thick" each piece is: a double root counts differently from a simple one. Sometimes a piece hides inside another, like a fat point sitting on a line. Those hidden pieces are real but are not unique, while the main pieces are. Computing the decomposition means factoring polynomials and doing many Gröbner basis computations.

## Definition

Notation: $K$ is a field, $S = K[x_1, \ldots, x_n]$, and ideals are given by finite generating sets. $\sqrt{I} = \{ f : f^m \in I \text{ for some } m \}$ is the radical.

An ideal $Q \subsetneq S$ is **primary** if $fg \in Q$ and $f \notin Q$ imply $g^m \in Q$ for some $m \ge 1$. Then $P = \sqrt{Q}$ is prime, and $Q$ is called $P$-primary. A **primary decomposition** of $I$ is an expression $I = Q_1 \cap \cdots \cap Q_r$ with each $Q_i$ primary. It is **irredundant** (minimal) if the primes $P_i = \sqrt{Q_i}$ are distinct and no $Q_i$ contains the intersection of the others.

**Lasker-Noether theorem.** Every proper ideal of the Noetherian ring $S$ has an irredundant primary decomposition (CLO, Chapter 4, Section 8). The set $\operatorname{Ass}(I) = \{P_1, \ldots, P_r\}$ of *associated primes* depends only on $I$. The minimal elements of $\operatorname{Ass}(I)$ are the minimal primes over $I$, and their components $Q_i$, the *isolated* components, are unique. The other primes are *embedded*, and their components need not be unique (Atiyah and Macdonald, Chapter 4).

**Input.** Generators $f_1, \ldots, f_s \in S$ of $I$.

**Output.** Generators of $Q_1, \ldots, Q_r$, and usually of $P_1, \ldots, P_r$, for an irredundant decomposition.

## Variants

- **Minimal primes.** Compute only the minimal associated primes, a prime decomposition $\sqrt{I} = P_1 \cap \cdots \cap P_m$. Geometrically, these are the irreducible components of $V(I)$ (CLO, Chapter 4, Section 6). This is often all that is needed and is cheaper.
- **The radical.** Compute $\sqrt{I}$ without decomposing it.
- **Equidimensional decomposition.** Split $I$ into pieces whose components all have the same dimension, without factoring.
- **Zero-dimensional ideals.** $V(I)$ is finite, every associated prime is maximal, and the decomposition groups the points into Galois orbits over $K$, with their multiplicity structure.
- **Absolute decomposition.** Decompose over $\overline{K}$ instead of $K$. Over $\mathbb{Q}$ this needs algebraic numbers, given by their [minimal polynomials](/minimal-polynomial-algebraic-element/).
- **Triangular decomposition.** Write $V(I)$ as a union of zero sets of triangular sets or [regular chains](/regular-chain/), a weaker but often cheaper description. See [triangular decomposition](/triangular-decomposition/).
- **Numerical irreducible decomposition.** Represent each component by a witness set, a generic linear section, computed by homotopy continuation.

## Examples

**One variable is factorization.** In $K[x]$, $\langle f \rangle = \bigcap_i \langle p_i^{e_i} \rangle$ for the factorization $f = c \prod_i p_i^{e_i}$ into irreducibles. So primary decomposition generalizes [polynomial factorization](/polynomial-factorization/).

**Two lines.** $\langle xy \rangle = \langle x \rangle \cap \langle y \rangle$, the two coordinate axes. Both components are prime and unique.

**An embedded point.** In $K[x, y]$,

$$\langle x^2, xy \rangle = \langle x \rangle \cap \langle x^2, y \rangle.$$

The prime $\langle x \rangle$ is minimal: it is the $y$-axis. The prime $\langle x, y \rangle$ is embedded: it is the origin, a point on the axis. The embedded component is not unique. For every $\lambda \in K$, $\langle x^2, xy \rangle = \langle x \rangle \cap \langle x^2, y + \lambda x \rangle$, since $\langle x^2, y + \lambda x \rangle$ is $\langle x, y \rangle$-primary and contains $x(y + \lambda x) - \lambda x^2 = xy$.

**A zero-dimensional ideal.** For $I = \langle x^3 - x^2, \; y - x^2 \rangle$ in $\mathbb{Q}[x, y]$, the coordinate $x$ separates the points, and its minimal polynomial modulo $I$ is $x^2 (x - 1)$. Each factor gives a component:

$$I = \bigl( I + \langle x^2 \rangle \bigr) \cap \bigl( I + \langle x - 1 \rangle \bigr) = \langle x^2, y \rangle \cap \langle x - 1, y - 1 \rangle,$$

a double point at the origin and a simple point at $(1, 1)$. The intersection can be checked with a Gröbner basis of $t Q_1 + (1 - t) Q_2$ and elimination of $t$.

**Dependence on the field.** $\langle x - y, \; y^2 - \tfrac{1}{2} \rangle$ is prime, in fact maximal, over $\mathbb{Q}$. Over $\mathbb{Q}(\sqrt{2})$ it is the intersection of the maximal ideals of the points $\pm (1/\sqrt{2}, 1/\sqrt{2})$.

## Known algorithms

- **Gianni, Trager and Zacharias (1988).** Choose a maximal independent set of variables $u$ and pass to the zero-dimensional ideal $I K(u)[x \setminus u]$. Put it in general position by a random linear change of coordinates, so that a single variable separates the points. Factor its minimal polynomial over $K(u)$, and get the primary components as $I + \langle p_j^{e_j} \rangle$, contracted back to $S$ by a saturation. Recurse on $I : h^\infty$ for the remaining lower-dimensional part, with $h$ a suitable polynomial.
- **Eisenbud, Huneke and Vasconcelos (1992).** Find the equidimensional parts and the radical by homological methods (Ext modules and Jacobian ideals), avoiding generic coordinate changes.
- **Shimoyama and Yokoyama (1996).** Compute the minimal primes first, then extract the primary components by saturations and separators.
- **Two variables.** Lazard (1985) uses the [structure of lex bases](/lazard-structure-theorem/) and needs only gcds and univariate factorizations.
- **Characteristic $p$.** Steel (2005) and others handle inseparability, where the radical and factorization behave differently.

All of these are implemented in Singular (`primdec.lib`), Macaulay2 and Magma. They are built from Gröbner bases of sums, products, intersections, quotients $I : f$ and saturations $I : f^\infty$ (CLO, Chapter 4, Sections 3 and 4).

## Bounds

- **Gröbner steps.** Every step uses Gröbner bases, so the worst-case cost inherits the doubly exponential lower bound of Mayr and Meyer (1982) for Gröbner bases and ideal membership. Better bounds are known for special tasks: the radical and the minimal primes can be computed within bounds single exponential in $n$, and zero-dimensional ideals have Gröbner bases of degree $d^{O(n)}$.
- **Number and degree of components.** For $I$ generated by polynomials of degree at most $d$, the degrees of the irreducible components of $V(I)$ add up to at most $d^n$ (refined Bézout inequality). So there are at most $d^n$ minimal primes.
- **Factoring is required.** The univariate case is polynomial factorization. Over a computable field without a factoring algorithm, which exists by Fröhlich and Shepherdson (1956), primary decomposition is not computable. Over $\mathbb{Q}$, factoring over number fields and over $\mathbb{Q}(u)$ is needed.
- **Embedded components are invisible in the variety.** Embedded primes do not change $V(I)$, so they cannot be found from the zero set. Finding them needs ideal-theoretic tests on quotients and saturations, which is why full primary decomposition costs more than computing minimal primes.

## Reductions

- **From polynomial factorization.** A univariate primary decomposition is a factorization, and conversely factorization over $K$ is the key step of every algorithm.
- **To the zero-dimensional case.** A maximal independent set $u$ of variables, read off from a Gröbner basis or the [Hilbert series](/hilbert-series/) dimension, turns the top-dimensional part into a zero-dimensional ideal over $K(u)$.
- **To saturation and quotients.** For any $f$, $I = (I : f^\infty) \cap (I + \langle f^m \rangle)$ for large $m$. This splitting lemma is the recursion step of most algorithms.
- **Radical membership.** Deciding $f \in \sqrt{I}$ needs no decomposition: by the Rabinowitsch trick it is the [ideal membership problem](/ideal-membership-problem/) $1 \in I + \langle 1 - tf \rangle$.

## Applications

- **Geometry.** Irreducible components of varieties, their dimensions and degrees, and singular loci.
- **Polynomial system solving.** Separating the components of a positive-dimensional solution set, and the multiplicity structure of isolated solutions in [polynomial system solving](/polynomial-system-solving/).
- **Algebraic statistics.** Conditional independence statements correspond to ideals whose primary decompositions list the statistical models compatible with them.
- **Chemical reaction networks and kinematics.** Steady-state varieties of mass-action systems, and the assembly modes of mechanisms, are found as components.

## References
