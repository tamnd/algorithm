---
tag: P06M5D
kind: algorithm
slug: cylindrical-algebraic-decomposition
name: Cylindrical algebraic decomposition
aliases:
- CAD
- Collins' CAD
- Collins' algorithm
area: algebra/computer-algebra
level: research
summary: Decomposes R^n into cells compatible with a polynomial family, enabling quantifier elimination.
model: blum-shub-smale-machine
complexity:
  vars: {m: the number of input polynomials, d: the largest degree of an input polynomial in each variable, n: the number of variables, c: an absolute constant}
  time: {worst: O((m d)^(2^(c n)))}
  space: {extra: O((m d)^(2^(c n)))}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [resultant, discriminant, sturm-sequence, real-root-isolation, semialgebraic-set]
see_also: [quantifier-elimination, tarski-seidenberg-theorem, real-closed-field, subresultant, polynomial-gcd, triangular-decomposition, vincent-collins-akritas, groebner-basis]
sources:
  - paper: doi:10.1007/3-540-07407-4_17
    title: George E. Collins, Quantifier elimination for real closed fields by cylindrical algebraic decomposition, Automata Theory and Formal Languages, 2nd GI Conference, Lecture Notes in Computer Science 33, 134-183, Springer, 1975
    locator: the projection operator, the induction on the number of variables, the lifting through stacks, and the complexity bound doubly exponential in n
  - paper: doi:10.1137/0213054
    title: Dennis S. Arnon, George E. Collins and Scott McCallum, Cylindrical algebraic decomposition I, the basic algorithm, SIAM Journal on Computing 13(4), 865-877, 1984
    locator: the definitions of cells, stacks and delineability, the basic algorithm, and the plane example
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 5 (decomposition of semi-algebraic sets, Section 5.1 on cylindrical decomposition and the proof of delineability) and Chapter 11 (the cylindrical decomposition algorithm and its complexity)
  - paper: doi:10.1016/S0747-7171(88)80004-X
    title: James H. Davenport and Joos Heintz, Real quantifier elimination is doubly exponential, Journal of Symbolic Computation 5(1-2), 29-35, 1988
    locator: a family of formulas whose quantifier-free equivalents need doubly exponential size in the number of variables
  - paper: doi:10.1016/S0747-7171(08)80152-6
    title: George E. Collins and Hoon Hong, Partial cylindrical algebraic decomposition for quantifier elimination, Journal of Symbolic Computation 12(3), 299-328, 1991
    locator: building only the cells needed to decide the formula, with truth values propagated during lifting
  - paper: "Scott McCallum, An improved projection operation for cylindrical algebraic decomposition of three-dimensional space, Journal of Symbolic Computation 5(1-2), 141-161, 1988"
    locator: the smaller projection by leading coefficients, discriminants and resultants, valid for well-oriented inputs
  - book: isbn:9783211827949
    title: Bob F. Caviness and Jeremy R. Johnson (editors), Quantifier Elimination and Cylindrical Algebraic Decomposition, Texts and Monographs in Symbolic Computation, Springer, 1998
    locator: the reprint of Collins 1975 and the surveys of projection operators, partial CAD and applications
---

A cylindrical algebraic decomposition (CAD) of $\mathbb{R}^n$ for a finite set of real polynomials $F$ is a partition of space into finitely many connected pieces, called cells, on each of which every polynomial of $F$ has a constant sign: positive, negative or zero. The cells are arranged in cylinders: their projections to $\mathbb{R}^{n-1}$ form a CAD of $\mathbb{R}^{n-1}$, and over each lower cell the cells above it are stacked one over another. George Collins introduced the decomposition and the algorithm that computes it in 1975. It gave the first practical [quantifier elimination](/quantifier-elimination/) procedure for the real numbers, and it remains the main general-purpose method. Its cost is doubly exponential in the number of variables, and Davenport and Heintz (1988) showed that quantifier elimination cannot avoid this in the worst case.

## In plain words

Take a few polynomial equations in two variables, such as a circle and a line. They cut the plane into regions where each polynomial is positive, negative or zero. The decomposition cuts the plane further into simple pieces arranged in vertical strips. Inside each piece no polynomial changes sign.

The algorithm first finds the special horizontal positions: where a curve turns vertical, where two curves cross, and where a curve escapes to infinity. Vertical lines through these positions, and the strips between them, give the columns. Within one column the curves never cross, so they cut the column into layers. Checking one sample point per piece then tells everything about the signs in the whole plane. Questions such as "is there a point with these signs?" become a search over finitely many samples.

## The problem

**Notation.** Let $R = \mathbb{Q}[x_1, \ldots, x_n]$ with the variables ordered $x_1 < x_2 < \cdots < x_n$, and work over the [real closed field](/real-closed-field/) $\mathbb{R}$; all arithmetic is exact, in $\mathbb{Q}$ and in real algebraic extensions $\mathbb{Q}(\alpha)$. No monomial order is needed: a polynomial is seen as a polynomial in its main variable $x_n$ with coefficients in $\mathbb{Q}[x_1, \ldots, x_{n-1}]$, and $\operatorname{LC}(f)$ is its leading coefficient in $x_n$ (the leading term $\operatorname{LT}$ and monomial $\operatorname{LM}$ are taken in $x_n$ in the same way). The input is $F = \{f_1, \ldots, f_m\} \subset R$ with degree at most $d$ in each variable and at most $t$ terms each; $M(d)$ is the cost of multiplying two univariate polynomials of degree $d$.

**Cells.** A *cell* of $\mathbb{R}^1$ is a point or an open interval. A cell of $\mathbb{R}^k$ is either a *section* $\{(u, \theta(u)) : u \in C\}$ or a *sector* $\{(u, y) : u \in C,\ \theta_1(u) < y < \theta_2(u)\}$, where $C$ is a cell of $\mathbb{R}^{k-1}$, the $\theta$ are continuous semialgebraic functions on $C$ with $\theta_1 < \theta_2$, and $\theta_1 = -\infty$ or $\theta_2 = +\infty$ are allowed. A *cylindrical algebraic decomposition* of $\mathbb{R}^n$ is a partition into cells such that the projections of the cells to $\mathbb{R}^{k}$, for every $k < n$, also form a CAD. It is *$F$-sign-invariant* if each $f \in F$ has a constant sign on each cell.

**Task.** Given $F$, compute an $F$-sign-invariant CAD of $\mathbb{R}^n$. Each cell is described by its position in the cylinder structure, a sample point with real algebraic coordinates, and the sign vector $(\operatorname{sign} f_1, \ldots, \operatorname{sign} f_m)$ at it.

## The algorithm

Collins' algorithm has three phases. *Projection* computes from $F$ a set $\operatorname{proj}(F)$ of polynomials in $x_1, \ldots, x_{n-1}$, then projects again, down to univariate polynomials. *Base* isolates the real roots of the univariate polynomials, giving a decomposition of the line. *Lifting* builds, over each cell of $\mathbb{R}^{k-1}$, the stack of cells in $\mathbb{R}^k$, by isolating the real roots of the level-$k$ polynomials at the sample point. The projection is chosen so that over every cell of the projected decomposition the polynomials of the level above are *delineable*: their real roots are continuous functions that never meet, so the stack computed at the sample point is valid for the whole cell.

For $n = 2$, the case the implementation covers, the projection is one step. Let $S$ be the squarefree part of the product of the primitive parts of the $f_i$, taken as polynomials in $y$ over $\mathbb{Q}[x]$. The projection is the set of the contents of the $f_i$, the leading coefficient $\operatorname{LC}(S)$, and the [discriminant](/discriminant/) in the form of the [resultant](/resultant/) $\operatorname{res}_y(S, \partial S / \partial y)$.

```pseudo id=main
CAD-PLANE(F)
L1  S ← squarefree part of ∏ prim(f); P ← squarefree part of ∏ cont(f) · LC(S) · res_y(S, ∂S/∂y)
L2  isolate the real roots α_1 < ... < α_k of P with rational intervals
L3  x-cells: the sectors (-∞, α_1), (α_1, α_2), ..., (α_k, +∞) with rational samples, and the sections α_i
L4  for each x-cell with sample a
L5      isolate the real roots of S(a, y) over Q(a): sections, with sectors between them and rational samples
L6      for each y-cell with sample b in the stack
L7          record the cell and the sign vector of F at (a, b)
L8  return the cells, P and S
```

Line L5 is where real algebraic numbers appear. When $a = \alpha_i$ is irrational, it is represented by the squarefree polynomial $P$ and an isolating interval. Arithmetic in $\mathbb{Q}(\alpha)$ uses dynamic evaluation: when a gcd with the defining polynomial is nontrivial, the defining polynomial is replaced by the factor that vanishes at $\alpha$, so no factorization is needed. The roots of $S(\alpha, y)$ are found among the roots of the norm $\operatorname{res}_x(p(x), S(x, y))$, which has rational coefficients, and are selected with a [Sturm sequence](/sturm-sequence/) over $\mathbb{Q}(\alpha)$. Signs at sample points are decided exactly: zero by a gcd test, nonzero signs by interval evaluation on intervals that are refined until the sign is clear.

For $n > 2$, Collins' projection of a set $A$ with main variable $x_n$ contains, for every $f \in A$ and every reductum $f^*$ of $f$ (obtained by dropping leading terms), the leading coefficients, the principal [subresultant](/subresultant/) coefficients of $f^*$ and $\partial f^* / \partial x_n$, and those of pairs $f^*$, $g^*$. The reducta handle the points where leading coefficients vanish. Lifting over a cell of $\mathbb{R}^{k-1}$ with a sample point $(\alpha_1, \ldots, \alpha_{k-1})$ works in the tower $\mathbb{Q}(\alpha_1, \ldots, \alpha_{k-1})$, usually through a primitive element.

## Example

Let $F = \{x^2 + y^2 - 1,\ x - y\}$, the unit circle and the diagonal. The squarefree part is $S = (x^2 + y^2 - 1)(y - x)$ up to sign. Its discriminant contributes $x^2 - 1$ (vertical tangents of the circle) and $2x^2 - 1$ (the two intersection points, where the resultant of the two factors vanishes); $\operatorname{LC}(S)$ is constant. So $P = (x^2 - 1)(x^2 - \tfrac12)$, with roots $-1, -\tfrac{1}{\sqrt 2}, \tfrac{1}{\sqrt 2}, 1$, and the line splits into 9 cells. The stacks, from the implementation, listing $(\operatorname{sign} f_1, \operatorname{sign} f_2)$ from bottom to top:

| x-cell | cells | sign vectors from bottom to top |
|---|---|---|
| $x < -1$ | 3 | $(+,+), (+,0), (+,-)$ |
| $x = -1$ | 5 | $(+,+), (+,0), (+,-), (0,-), (+,-)$ |
| $-1 < x < -\frac{1}{\sqrt 2}$ | 7 | $(+,+), (+,0), (+,-), (0,-), (-,-), (0,-), (+,-)$ |
| $x = -\frac{1}{\sqrt 2}$ | 5 | $(+,+), (0,0), (-,-), (0,-), (+,-)$ |
| $-\frac{1}{\sqrt 2} < x < \frac{1}{\sqrt 2}$ | 7 | $(+,+), (0,+), (-,+), (-,0), (-,-), (0,-), (+,-)$ |
| $x = \frac{1}{\sqrt 2}$ | 5 | $(+,+), (0,+), (-,+), (0,0), (+,-)$ |
| $\frac{1}{\sqrt 2} < x < 1$ | 7 | $(+,+), (0,+), (-,+), (0,+), (+,+), (+,0), (+,-)$ |
| $x = 1$ | 5 | $(+,+), (0,+), (+,+), (+,0), (+,-)$ |
| $x > 1$ | 3 | $(+,+), (+,0), (+,-)$ |

There are 47 cells. In the middle column the diagonal lies between the two arcs of the circle; to the left of $-\frac{1}{\sqrt 2}$ it is below both, and to the right of $\frac{1}{\sqrt 2}$ above both. The CAD answers quantified questions by reading the table. For example, $\exists y\ (x^2 + y^2 - 1 < 0 \wedge x - y = 0)$ holds exactly in the x-cells whose stack contains the sign vector $(-, 0)$. That is only the middle cell, so the formula is equivalent to $2x^2 - 1 < 0$.

## Correctness

The key fact is delineability. Over an open interval $I$ of $x$ where $\operatorname{LC}(S)$ and $\operatorname{res}_y(S, \partial S/\partial y)$ have no zero, $S(x, \cdot)$ keeps its degree and its roots stay simple. Its real roots are then continuous functions of $x$ that never meet: a real root cannot appear or disappear without two roots colliding. Every zero of $f \in F$ over $I$ is a zero of $S$, because the contents of the $f_i$ have no zero on $I$ and every irreducible factor of a primitive part divides $S$. By continuity, each $f$ has a constant sign on each sector. On each section, a single irreducible factor of $S$ vanishes along the whole section, so $f$ either vanishes on all of it or on none of it. Over the points $\alpha_i$, the stack is computed directly, and every zero of $f(\alpha_i, \cdot)$ is a root of $S(\alpha_i, \cdot)$ unless $f$ vanishes on the whole vertical line. The [proof](proofs/correctness.md) gives the details, the exactness of the sign computations and termination.

## Complexity

The cost model is the number of operations in $\mathbb{Q}$ and in the real algebraic extensions, with exact rational coefficients; bit costs grow with the coefficient sizes, which are polynomial in the degrees for fixed $n$.

- **Proved bound for general $n$.** Collins' analysis gives a running time polynomial in $m$, $d$ and the coefficient length for fixed $n$, with an exponent that doubles with each variable: the time is $(md)^{2^{O(n)}}$. The reason is that each projection squares the number of polynomials and roughly squares their degrees, through pairwise resultants. The number of cells has the same form.
- **Lower bound.** Davenport and Heintz (1988) gave formulas in $n$ variables whose quantifier-free equivalents need size doubly exponential in $n$. So quantifier elimination, and any CAD from which those equivalents can be read, cannot be singly exponential in the worst case. Brown and Davenport (2007) showed that some polynomial families need a CAD with doubly exponentially many cells.
- **The plane.** For $n = 2$, $S$ has total degree $D \le md$, $P$ has degree $O(D^2)$, and each stack has at most $2D + 1$ cells. So there are $O(D^3)$ cells, computed with a number of field operations polynomial in $D$. No useful best case is stated: the projection, with its resultant, is always computed in full, and only the lifting gets cheaper when $P$ has few real roots.
- **Observed.** The tests check 500 random inputs (220 families of conics, 230 families of lines and 50 cubics) in about 10 seconds. Most of the time goes to real algebraic arithmetic in the section columns, whose defining polynomials are kept small by taking squarefree factors of the projection polynomials.

## Properties

- **Exact and complete.** The output is an exact decomposition with exact sample points, valid for every real point, not only for generic ones.
- **Cylindrical.** The projections of the cells onto the first $k$ coordinates form a CAD of $\mathbb{R}^k$ for every $k$, so quantifiers on the last variables can be eliminated one at a time.
- **Variable order matters.** The decomposition depends on the order of the variables. Different orders can change the number of cells by orders of magnitude.
- **Not minimal.** The cells refine the sign conditions, often by far. In the example 47 cells describe a picture with far fewer distinct regions.
- **Semialgebraic output.** Each cell is a connected [semialgebraic set](/semialgebraic-set/), described by sign conditions on the projection polynomials. This is how quantifier-free formulas are produced.

## Variants and improvements

- **Smaller projections.** McCallum (1988) dropped most reducta and subresultants: for well-oriented inputs, leading coefficients, discriminants and pairwise resultants of squarefree bases are enough. Hong (1990) improved Collins' operator in general. Brown (2001) reduced McCallum's further.
- **Partial CAD.** Collins and Hong (1991) build only the cells needed to decide a formula. Truth values propagate during lifting, and a stack is not built when its value is already known. This is the form used for quantifier elimination in practice.
- **Equational constraints.** When the formula contains an equation $f = 0$, only the cells on its zero set matter, and the projection can be reduced accordingly (Collins 1998; McCallum 1999).
- **CAD by regular chains.** Chen, Moreno Maza, Xia and Yang (2009) first build a complex cylindrical decomposition with [triangular decompositions](/triangular-decomposition/) and then compute the real decomposition. This is implemented in Maple's RegularChains library.
- **Single cells and NLSAT.** Jovanović and de Moura's NLSAT (2012) and cylindrical algebraic coverings (Ábrahám, Davenport, England and Kremer 2021) compute one cell around a point at a time, guided by a satisfiability search. This is how SMT solvers handle nonlinear real arithmetic.
- **Singly exponential algorithms.** Critical point methods (Grigoriev and Vorobjov; Renegar; Basu, Pollack and Roy) decide formulas in time singly exponential in $n$ for a fixed number of quantifier alternations, at the price of large constants. They rarely beat CAD in practice.

## When to use it

Use a CAD for problems about real solutions with inequalities and quantifiers in few variables: quantifier elimination, deciding whether a semialgebraic set is empty, describing the topology of a real curve, and robot motion planning in configuration space. It is the right tool up to about four or five variables with low degrees. For polynomial equations alone, over the complex numbers, a [Gröbner basis](/groebner-basis/) is cheaper. For existence questions only, SMT solvers that compute one cell at a time are usually faster. For many variables, numerical methods or critical point algorithms are the only options.

## Pitfalls

- **Missing projection factors.** Dropping the leading coefficient, or the content, gives cells over which a root goes to infinity or a curve contains a vertical line, and the sign-invariance fails without any error. The implementation keeps both.
- **Squarefree parts.** The discriminant of a non-squarefree polynomial is identically zero, so the projection must use squarefree bases. A repeated input polynomial must not destroy the projection.
- **Floating point.** Sample points over sections are irrational, and signs there must be decided exactly. Rounding can put a sample on the wrong side of a curve or miss a zero on a section.
- **Variable order.** A bad variable order can make the computation infeasible when another order is easy. Heuristics, such as the degree-based heuristic of Brown, help but are not reliable.
- **Well-orientedness.** McCallum's projection is only valid when no projection polynomial vanishes identically on a cell of positive dimension. That must be checked, and the algorithm must fall back to a fuller projection when it fails.

## Implementations

## History

Tarski proved around 1930, and published in 1948 and 1951, that the first-order theory of the real numbers admits quantifier elimination; his procedure was far too slow to use, and its cost is not bounded by any tower of exponentials of fixed height. Collins introduced the cylindrical algebraic decomposition in 1973 and published it in 1975, with the first elementary bound, doubly exponential in the number of variables. Arnon, Collins and McCallum (1984) gave the standard presentation of the basic algorithm, and Arnon's thesis implemented it in the SAC-2 system. Davenport and Heintz (1988) proved that doubly exponential cost is unavoidable for quantifier elimination. McCallum's and Hong's projections, and Collins and Hong's partial CAD (1991) in the QEPCAD system, made it usable. Since 2012 single-cell variants have been central to SMT solving for nonlinear real arithmetic.

## References
