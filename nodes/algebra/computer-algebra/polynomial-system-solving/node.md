---
tag: 8N933B
kind: problem
slug: polynomial-system-solving
name: Polynomial system solving
aliases:
- solving polynomial equations
- solving systems of polynomial equations
- algebraic system solving
area: algebra/computer-algebra
level: core
summary: Find all solutions of a system of polynomial equations.
model: blum-shub-smale-machine
prereqs: [polynomial-ideal, groebner-basis, hilbert-nullstellensatz]
see_also: [elimination-theorem, fglm-algorithm, f4-algorithm, f5-algorithm, triangular-decomposition, rational-univariate-representation, homotopy-continuation, cylindrical-algebraic-decomposition]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 8 (solving systems with a lex Gröbner basis); Chapter 3, Sections 1 and 2 (the elimination and extension theorems); Chapter 4, Section 1 (consistency by the Nullstellensatz); Chapter 5, Section 3 (the finiteness theorem for zero-dimensional systems)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Gröbner bases (solving and elimination, and Section 21.7 on the complexity, with the Mayr and Meyer lower bound)
  - paper: doi:10.1006/jsco.1993.1051
    title: Jean-Charles Faugère, Patrizia Gianni, Daniel Lazard and Teo Mora, Efficient computation of zero-dimensional Gröbner bases by change of ordering, Journal of Symbolic Computation 16(4), 329-344, 1993
    locator: the FGLM algorithm and its cost in the number of solutions
  - paper: doi:10.1007/s002000050114
    title: Fabrice Rouillier, Solving zero-dimensional systems through the rational univariate representation, Applicable Algebra in Engineering, Communication and Computing 9, 433-461, 1999
    locator: the rational univariate representation
  - paper: doi:10.1016/S0022-4049(99)00005-5
    title: Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases (F4), Journal of Pure and Applied Algebra 139, 61-88, 1999
    locator: the F4 algorithm
  - paper: doi:10.1016/0001-8708(82)90048-2
    title: Ernst W. Mayr and Albert R. Meyer, The complexity of the word problems for commutative semigroups and polynomial ideals, Advances in Mathematics 46(3), 305-329, 1982
    locator: the doubly exponential lower bound for Gröbner bases and ideal membership
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 11 (cylindrical algebraic decomposition) and Chapter 13 (singly exponential sampling of real solutions by critical points)
  - book: isbn:9789812561848
    title: Andrew J. Sommese and Charles W. Wampler, The Numerical Solution of Systems of Polynomials Arising in Engineering and Science, World Scientific, 2005
    locator: Part II, homotopy continuation, and Part III, witness sets for positive-dimensional solution sets
---

Polynomial system solving asks for the common zeros of $f_1, \ldots, f_s \in K[x_1, \ldots, x_n]$, the variety $V(f_1, \ldots, f_s) \subseteq \overline{K}^n$, or its real points. "Solving" covers several outputs, each with its own algorithms and costs: deciding whether a solution exists, computing the dimension, giving a finite solution set in a triangular or univariate form, approximating the solutions numerically, or decomposing a positive-dimensional variety into components. The symbolic route computes a [Gröbner basis](/groebner-basis/) of the ideal, usually under grevlex, converts it to a lex basis or a [rational univariate representation](/rational-univariate-representation/), and finishes with univariate [root isolation](/real-root-isolation/). The numerical route uses [homotopy continuation](/homotopy-continuation/). Over $\mathbb{C}$, deciding whether a solution exists is NP-hard, and a Gröbner basis can have doubly exponential degree in the worst case (Mayr and Meyer 1982). For the systems met in practice, with finitely many solutions, the cost is singly exponential in $n$.

## In plain words

You have several equations in several unknowns, each a polynomial, and you want every combination of values that makes all of them true. With one unknown you would find the roots of one polynomial. With several, the classic trick is to eliminate unknowns until one equation in one unknown is left, solve it, and substitute back, as in Gaussian elimination for linear systems. Gröbner bases do this elimination in a guaranteed way. Sometimes there is no solution, sometimes finitely many, and sometimes a whole curve or surface of them, and a solver must report which case it is in. The number of solutions can be as large as the product of the degrees, so even writing the answer down can be costly.

## Definition

Notation: $K$ is a field, usually $\mathbb{Q}$, and $\overline{K}$ its algebraic closure. The input is $f_1, \ldots, f_s \in K[x_1, \ldots, x_n]$ of degree at most $d$. $I = \langle f_1, \ldots, f_s \rangle$ is their [ideal](/polynomial-ideal/) and $V = V(I) \subseteq \overline{K}^n$ the set of common zeros. Monomial orders are lex with $x_1 > \cdots > x_n$ or grevlex, and $\operatorname{LT}$, $\operatorname{LM}$, $\operatorname{LC}$ are taken for the stated order.

**Input.** $f_1, \ldots, f_s$.

**Output, in increasing order of detail.**

1. **Consistency.** Whether $V \ne \emptyset$. By the weak [Nullstellensatz](/hilbert-nullstellensatz/), $V = \emptyset$ exactly when $1 \in I$, that is, when the reduced Gröbner basis is $\{1\}$.
2. **Finiteness and dimension.** Whether $V$ is finite, and $\dim V$ in general. $V$ is finite exactly when, for each $i$, some $\operatorname{LM}$ of the Gröbner basis is a pure power of $x_i$ (the finiteness theorem). Then $\dim_K K[x]/I$ is the number of solutions counted with multiplicity.
3. **A symbolic description of a finite $V$.** A lex Gröbner basis, a set of triangular sets, or a rational univariate representation: a squarefree polynomial $q(t)$ and polynomials $g_1, \ldots, g_n$ with $V = \{ (g_1(\tau)/q'(\tau), \ldots, g_n(\tau)/q'(\tau)) : q(\tau) = 0 \}$, where $t$ is a linear form in the $x_i$ that separates the points.
4. **Numerical solutions.** Isolating boxes or approximations to a given accuracy for each point, or for each real point.
5. **Components.** For positive-dimensional $V$, a decomposition into irreducible components, each given by a prime ideal, a regular chain or a numerical witness set. See [primary decomposition](/primary-decomposition/).

## Variants

- **Real solving.** Find the points of $V \cap \mathbb{R}^n$, or decide whether a system of polynomial equations and inequalities has a real solution. This is the existential theory of the reals. [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) solves it and also handles quantifiers. Critical point methods find one point in each connected component.
- **Elimination.** Compute $I \cap K[x_{k+1}, \ldots, x_n]$, whose variety is the closure of the projection of $V$. A lex Gröbner basis contains a basis of each such [elimination ideal](/elimination-ideal/) (the [elimination theorem](/elimination-theorem/)).
- **Parametric systems.** The coefficients depend on parameters. Comprehensive Gröbner systems and regular chains split the parameter space into cases.
- **Overdetermined systems over finite fields.** In algebraic cryptanalysis, $s$ is much larger than $n$, the field is $\mathbb{F}_2$ or $\mathbb{F}_q$, and only solutions in the base field matter, so the field equations $x_i^q - x_i$ are added.
- **Sparse systems.** The supports of the $f_i$ are fixed, and the number of solutions in $(\overline{K}^*)^n$ is bounded by the mixed volume of the Newton polytopes (the Bernstein-Kushnirenko-Khovanskii bound) instead of the Bézout number.

## Examples

**A circle and a line.** For $x^2 + y^2 - 1$ and $x - y$ in $\mathbb{Q}[x, y]$ with lex $x > y$, the reduced Gröbner basis is $\{x - y, \; y^2 - \tfrac{1}{2}\}$. It is triangular: solve $y^2 = \tfrac{1}{2}$, then $x = y$. The solutions are $\pm (1/\sqrt{2}, 1/\sqrt{2})$.

**Two parabolas.** For $x^2 + y - 1$ and $x + y^2 - 1$ with lex $x > y$, the reduced Gröbner basis is

$$\{ x + y^2 - 1, \; y^4 - 2y^2 + y \}.$$

The last polynomial is $y (y - 1)(y^2 + y - 1)$, so the solutions are $(1, 0)$, $(0, 1)$, and the two points $x = y = (-1 \pm \sqrt{5})/2$. There are $4 = 2 \cdot 2$ of them, reaching the Bézout bound.

**No solution.** For $xy - 1$ and $x$, the identity $1 = y \cdot x - (xy - 1)$ shows $1 \in I$. The reduced Gröbner basis is $\{1\}$, and $V = \emptyset$.

**Infinitely many solutions.** For the single equation $xy = 0$, $V$ is the union of the two axes, with dimension $1$. No leading monomial of the basis $\{xy\}$ is a pure power of $x$, so the finiteness test reports correctly that $V$ is infinite.

## Known algorithms

| method | output | cost | status |
|---|---|---|---|
| [Buchberger](/buchberger-algorithm/), [F4](/f4-algorithm/), [F5](/f5-algorithm/) | Gröbner basis, hence consistency, dimension, elimination | doubly exponential in $n$ in the worst case; $d^{O(n)}$ for zero-dimensional ideals | proved bounds; F4 and F5 far faster in practice |
| [FGLM](/fglm-algorithm/) | lex basis from a grevlex basis, zero-dimensional | $O(n D^3)$ field operations for $D = \dim_K K[x]/I$ | proved |
| [Rational univariate representation](/rational-univariate-representation/) (Rouillier 1999) | $q(t)$ and $g_1, \ldots, g_n$ | linear algebra in $K[x]/I$, polynomial in $D$ | proved |
| Eigenvalue method (Auzinger and Stetter 1988) | the points, as joint eigenvectors of multiplication matrices on $K[x]/I$ | polynomial in $D$ | proved; numerically sensitive |
| [Triangular decomposition](/triangular-decomposition/), [characteristic sets](/characteristic-set/), [regular chains](/regular-chain/) | a union of triangular sets | exponential in the worst case | proved; good on structured inputs |
| Resultants and [Macaulay matrices](/macaulay-matrix/) | eliminants, the u-resultant | linear algebra on matrices of size $\binom{n + D_M}{n}$ with $D_M = \sum_i (d_i - 1) + 1$ | proved for $n$ generic equations |
| Geometric resolution (Giusti, Lecerf and Salvy 2001) | a rational univariate representation | polynomial in the input size and a geometric degree, randomized | proved |
| [Homotopy continuation](/homotopy-continuation/) | numerical approximations of all isolated solutions; witness sets | one path per start solution, up to the Bézout number or the mixed volume | path tracking is heuristic unless certified |
| [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) (Collins 1975) | real solutions, with quantifiers | doubly exponential in $n$ | proved |
| Critical point methods (Basu, Pollack and Roy) | a point in each real connected component | $(s d)^{O(n)}$ | proved |

## Bounds

- **Number of solutions.** If $s = n$ and $V$ is finite, then $|V| \le d_1 \cdots d_n$, where $d_i = \deg f_i$ (Bézout's theorem). For sparse systems the mixed volume bounds the number of solutions in the torus. So the output has size up to $d^n$, which is exponential in $n$.
- **Gröbner bases are doubly exponential in the worst case.** Mayr and Meyer (1982) gave ideals in $n$ variables, generated by polynomials of bounded degree, whose membership certificates and Gröbner bases need degrees of the form $2^{2^{cn}}$ for a constant $c > 0$, and the ideal membership problem is exponential space complete. The upper bound $2 \left( d^2/2 + d \right)^{2^{n-1}}$ of Dubé (1990) has the same shape. Better cases are known: for zero-dimensional ideals the degrees are $d^{O(n)}$ (Lakshman 1991, Lazard 1983), and for a homogeneous regular sequence in grevlex order they are at most the Macaulay bound $\sum_i (d_i - 1) + 1$ (Lazard 1983).
- **Consistency is NP-hard.** Encode a 3-SAT instance by $x_i^2 - x_i = 0$ for each variable and, for each clause such as $x \lor y \lor \lnot z$, the equation $(1 - x)(1 - y) z = 0$. The system has a solution exactly when the formula is satisfiable, so deciding $V \ne \emptyset$ over $\mathbb{Q}$ or $\mathbb{C}$ is NP-hard. It is in PSPACE, and Koiran (1996) placed it in the polynomial hierarchy under the generalized Riemann hypothesis.
- **Real solving.** Deciding whether a system has a real solution is complete for the existential theory of the reals, which lies in PSPACE (Canny 1988).

## Reductions

- **To ideal membership.** Consistency is the [ideal membership problem](/ideal-membership-problem/) for $f = 1$.
- **To univariate root finding.** In a zero-dimensional ideal, a lex basis in shape position $\{x_1 - g_1(x_n), \ldots, x_{n-1} - g_{n-1}(x_n), p(x_n)\}$ reduces solving to the roots of $p$. After a generic linear change of coordinates, a radical zero-dimensional ideal is in this position (the shape lemma).
- **To linear algebra.** F4, the Macaulay matrix method and the eigenvalue method all reduce solving to linear algebra over $K$ on matrices whose size is governed by a degree bound.
- **From integer and Boolean problems.** SAT, graph coloring and integer feasibility encode as polynomial systems, giving the hardness results above.

## Applications

- **Robotics.** The inverse kinematics of a general 6R manipulator has at most $16$ solutions, found by elimination or homotopy.
- **Computer vision.** The five-point relative pose problem has $10$ solutions in general and is solved by Gröbner basis solvers generated for its fixed structure.
- **Cryptanalysis.** Algebraic attacks set up a system over $\mathbb{F}_2$ for a key. Faugère and Joux (2003) broke the first HFE challenge with F5.
- **Chemistry, biology and economics.** Steady states of mass-action networks, and Nash equilibria of finite games, are the solutions of polynomial systems.
- **Geometry theorem proving.** A geometric claim becomes an implication between polynomial equations, checked by [Wu's method](/wu-characteristic-set-method/) or by Gröbner bases.

## References
