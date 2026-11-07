---
tag: 6BJ6TN
kind: problem
slug: quantifier-elimination
name: Quantifier elimination
aliases: [QE, real quantifier elimination, quantifier elimination over the reals]
area: algebra/computer-algebra
level: advanced
summary: Replace a first-order formula over a real or algebraically closed field with an equivalent quantifier-free formula.
prereqs: [semialgebraic-set, real-closed-field, polynomial-ring]
see_also: [tarski-seidenberg-theorem, cylindrical-algebraic-decomposition, fourier-motzkin-elimination, sturm-theorem, groebner-basis, presburger-arithmetic, tarski-decidability-theorem, boolean-quantifier-elimination]
sources:
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 2, Real Closed Fields (the Tarski-Seidenberg principle), Chapter 11, Cylindrical Decomposition Algorithm, Chapter 13, Existential Theory of the Reals, and Chapter 14, Quantifier Elimination
  - paper: "Alfred Tarski, A Decision Method for Elementary Algebra and Geometry, RAND Corporation, 1948; second edition, University of California Press, 1951"
    locator: the elimination procedure for real closed fields
  - paper: doi:10.1007/3-540-07407-4_17
    title: George E. Collins, Quantifier elimination for real closed fields by cylindrical algebraic decomposition, Automata Theory and Formal Languages, Lecture Notes in Computer Science 33, 1975
    locator: pp. 134 to 183
  - paper: doi:10.1016/S0747-7171(88)80004-X
    title: James H. Davenport and Joos Heintz, Real quantifier elimination is doubly exponential, Journal of Symbolic Computation 5(1-2), 1988
    locator: pp. 29 to 35
  - paper: doi:10.1145/235809.235813
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, On the combinatorial and algebraic complexity of quantifier elimination, Journal of the ACM 43(6), 1996
    locator: pp. 1002 to 1045
  - paper: doi:10.1016/S0747-7171(10)80003-3
    title: James Renegar, On the computational complexity and geometry of the first-order theory of the reals, Part I, Journal of Symbolic Computation 13(3), 1992
    locator: pp. 255 to 299 (Parts II and III follow in the same issue)
  - paper: doi:10.1016/S0747-7171(88)80003-8
    title: Volker Weispfenning, The complexity of linear problems in fields, Journal of Symbolic Computation 5(1-2), 1988
    locator: pp. 3 to 27 (virtual substitution for linear formulas and its complexity)
  - paper: doi:10.1145/62212.62257
    title: John Canny, Some algebraic and geometric computations in PSPACE, STOC 1988
    locator: pp. 460 to 469 (the existential theory of the reals is in PSPACE)
  - book: isbn:9783211827949
    title: Bob F. Caviness and Jeremy R. Johnson (editors), Quantifier Elimination and Cylindrical Algebraic Decomposition, Springer, 1998
    locator: the collected papers on Tarski's method, cylindrical algebraic decomposition and its improvements
---

## In plain words

A statement about real numbers can say "there is an x such that" or "for every x". Quantifier elimination removes these phrases. The result says the same thing, but only with equations and inequalities in the other variables. For example, "there is a real x with x squared plus b x plus c equal to zero" becomes "b squared is at least four times c".

Tarski proved that this is always possible over the real numbers, and that the result can be computed. When no free variables are left, the result is true or false, so the method decides every such statement. The known methods are exact but very slow in the worst case, and it is proved that this is not only a weakness of the methods.

## Definition

**Formulas.** Let $K$ be an ordered field, in practice $\mathbb{R}$. An *atom* is $P > 0$ or $P = 0$ with $P \in \mathbb{Z}[y_1, \ldots, y_k, x_1, \ldots, x_n]$; the relations $\ne$, $\ge$, $<$ and $\le$ are Boolean combinations of these. A *first-order formula* is built from atoms by $\wedge$, $\vee$, $\neg$ and the quantifiers $\exists x_i$ and $\forall x_i$ over elements of $K$. Every formula is equivalent to a *prenex* formula

$$\Phi(y) = (Q_1 X^{[1]}) \cdots (Q_\omega X^{[\omega]}) \; \phi(y, X^{[1]}, \ldots, X^{[\omega]}),$$

where $Q_i \in \{\exists, \forall\}$ alternate, $X^{[i]}$ is a block of $k_i$ variables, and $\phi$ is quantifier-free. $\omega$ is the number of *quantifier blocks*. The free variables are $y = (y_1, \ldots, y_k)$.

**The problem.** *Input:* a formula $\Phi(y)$. *Output:* a quantifier-free formula $\Psi(y)$ such that $\Phi(a) \Leftrightarrow \Psi(a)$ for every $a \in \mathbb{R}^k$. By the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/), $\Psi$ exists, and by the transfer principle the equivalence then holds in every [real closed field](/real-closed-field/). The set of $a$ where $\Phi(a)$ holds is a [semialgebraic set](/semialgebraic-set/), and $\Psi$ describes it.

**The decision problem.** For $k = 0$, $\Psi$ is $\mathit{true}$ or $\mathit{false}$, so quantifier elimination decides the first-order theory of the reals. The *existential theory of the reals* is the case $\omega = 1$, $Q_1 = \exists$, $k = 0$: does a system of polynomial equations and inequalities have a real solution?

**Size parameters.** $m$ is the number of distinct polynomials in $\phi$, $d$ bounds their degrees, $n = k_1 + \cdots + k_\omega$ is the number of bound variables, and for integer coefficients $\tau$ bounds their bit length. Costs are counted in arithmetic operations on the coefficients, or in bit operations over $\mathbb{Z}$.

## Variants

- **Algebraically closed fields.** Over $\mathbb{C}$, atoms are only $P = 0$, and elimination is possible by Chevalley's theorem: the projection of a constructible set is constructible. It reduces to ideal computations, for example with [Gröbner bases](/groebner-basis/) and the [elimination theorem](/elimination-theorem/), and the [Nullstellensatz](/hilbert-nullstellensatz/) decides the existential case.
- **Linear formulas.** If all atoms are linear in the bound variables, [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) or the virtual substitution of Weispfenning (1988) eliminates one variable at a time with a finite set of test points. Weispfenning extended virtual substitution to variables that occur with degree at most 2, and in later work 3.
- **Integers.** Over $(\mathbb{Z}, +, <)$, [Presburger arithmetic](/presburger-arithmetic/) admits elimination after divisibility predicates are added. With multiplication over $\mathbb{Z}$ the theory is undecidable, by [Hilbert's tenth problem](/hilberts-tenth-problem/).
- **Boolean variables.** For propositional variables, [Boolean quantifier elimination](/boolean-quantifier-elimination/) is the analogue, done with decision diagrams.
- **Partial and generic elimination.** Many systems return a formula valid only outside a lower-dimensional set of parameters, which is often much smaller.

## Examples

- **A quadratic.** Over $\mathbb{R}$, $\exists x \, (x^2 + b x + c = 0) \Leftrightarrow b^2 - 4c \ge 0$. With a leading coefficient that can vanish, $\exists x \, (a x^2 + b x + c = 0)$ is equivalent to $(a \ne 0 \wedge b^2 - 4ac \ge 0) \vee (a = 0 \wedge b \ne 0) \vee (a = b = c = 0)$. The case split on $a$ is typical: the output must handle every degenerate value of the parameters.
- **A universal statement.** $\forall x \, (x^2 + b x + c > 0) \Leftrightarrow b^2 - 4c < 0$.
- **Order is needed.** $\exists x \, (y = x^2) \Leftrightarrow y \ge 0$, and $\exists x \, (x^2 + y^2 = 1) \Leftrightarrow y^2 \le 1$. The sets $\{y \ge 0\}$ and $[-1, 1]$ are not zero sets of polynomials, so over $\mathbb{R}$ the output needs inequalities even when the input has none.
- **Linear.** $\exists x \, (y < x \wedge x < z) \Leftrightarrow y < z$, the first step of Fourier-Motzkin elimination.
- **Over $\mathbb{C}$.** $\exists x \, (x^2 + b x + c = 0)$ is equivalent to $\mathit{true}$, and $\exists x \, (a x - 1 = 0)$ to $a \ne 0$.
- **A decision.** $\forall x \, \forall y \, (x^2 + y^2 \ge 2xy)$ is $\mathit{true}$, because $x^2 + y^2 - 2xy = (x - y)^2$.

## Known algorithms

- **Tarski (1948, published 1951).** The first procedure, a generalization of [Sturm's theorem](/sturm-theorem/) to parameters. Its cost is not bounded by any tower of exponentials of fixed height.
- **Seidenberg (1954).** A simpler proof and procedure by induction on the number of variables. Also of non-elementary cost.
- **[Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/), Collins (1975).** It decomposes $\mathbb{R}^{k+n}$ into cells on which every polynomial of $\phi$ has a constant sign, cylindrically over $\mathbb{R}^k$, so that each quantifier becomes a finite "or" or "and" over cells. The cost is $(m d)^{2^{O(k + n)}}$ operations, doubly exponential in the number of variables and polynomial in $m$ and $d$ for a fixed number of variables. It is the method of choice in practice for few variables (QEPCAD, Mathematica, Maple).
- **Critical points and block elimination.** Grigoriev and Vorobjov (1988), Renegar (1992), and Basu, Pollack and Roy (1996) eliminate a whole block of variables at once. Basu, Pollack and Roy obtain $m^{(k+1)\prod_i (k_i + 1)} d^{(k+1)\prod_i O(k_i)}$ arithmetic operations. This is singly exponential in the number of variables when $\omega$ is fixed, and doubly exponential only in $\omega$. The existential case costs $m^{n+1} d^{O(n)}$.
- **Virtual substitution (Weispfenning).** For bound variables of low degree it replaces $\exists x$ by a disjunction over finitely many test terms, given by the roots of the atoms. It is implemented in Redlog and is often fast for linear and quadratic problems.
- **Over $\mathbb{C}$.** Gröbner bases, comprehensive Gröbner bases and [triangular decompositions](/triangular-decomposition/) give constructible descriptions of projections.

## Bounds

- **Lower bound for the output.** Davenport and Heintz (1988) gave formulas with $n$ variables and $O(n)$ quantifier alternations whose quantifier-free equivalents must contain polynomials of degree, or a number of atoms, doubly exponential in $n$. So quantifier elimination over $\mathbb{R}$ is doubly exponential in the worst case, in any method. Weispfenning (1988) showed a doubly exponential lower bound already for linear formulas.
- **Lower bound for the decision problem.** Fischer and Rabin (1974) proved that every decision procedure for the first-order theory of $(\mathbb{R}, +, <)$, without multiplication, needs time $2^{c \ell}$ on some formulas of length $\ell$, for a constant $c > 0$, even when it may guess.
- **Upper bounds.** Doubly exponential in the number of variables by cylindrical algebraic decomposition, and doubly exponential only in the number of alternations by block elimination, as above. These are proved bounds. Observed costs of cylindrical algebraic decomposition are often far below them for small inputs, but the doubly exponential growth in the number of variables is also seen in practice.
- **The existential theory.** Deciding it is NP-hard, because $x_i (1 - x_i) = 0$ encodes Boolean variables, and it lies in PSPACE (Canny 1988). Its exact complexity defines the class $\exists\mathbb{R}$.

## Reductions

- **From projection.** Eliminating $\exists x$ from $\phi(y, x)$ is computing the projection of the semialgebraic set $\{(y, x) : \phi\}$ to $y$-space. So quantifier elimination is equivalent to closing semialgebraic sets under projection, which is the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/).
- **Universal to existential.** $\forall x \, \phi \Leftrightarrow \neg \exists x \, \neg \phi$, so an elimination for one $\exists$ block is enough, applied from the innermost block out. The negations make the formula grow, which is one source of the dependence on $\omega$.
- **Polynomial optimization.** $\min_x f(x)$ over a semialgebraic set $S$ is the largest $t$ with $\forall x \, (x \in S \Rightarrow f(x) \ge t)$, a one-parameter elimination problem.
- **Satisfiability.** Every NP problem reduces to the existential theory of the reals, through the encoding of Boolean variables above, and many geometric problems, such as the realizability of order types and the art gallery problem, are complete for $\exists\mathbb{R}$.

## Applications

- **Geometry and theorem proving.** Statements of elementary geometry become real formulas in the coordinates; elimination proves them, or gives the conditions on parameters under which they hold.
- **Control and stability.** Conditions such as "all roots of a polynomial with parameters have negative real part" are eliminated to explicit inequalities on the parameters, generalizing the Routh-Hurwitz criteria.
- **Motion planning.** The piano movers' problem of Schwartz and Sharir asks if two placements of a body are in the same connected component of a semialgebraic set of free placements; cylindrical algebraic decomposition answers it.
- **Verification and SMT.** Solvers for nonlinear real arithmetic, such as the NLSAT procedure of Jovanović and de Moura (2012), combine conflict-driven search with cylindrical algebraic decomposition to decide existential formulas.
- **Optimization and numerical analysis.** Exact certificates of bounds, the existence of real solutions of a system, and the verification of numerical claims.

## References
