---
tag: DPM77P
kind: problem
slug: hilberts-tenth-problem
name: Hilbert's tenth problem
aliases:
- Diophantine solvability
- Matiyasevich theorem
area: complexity/computability
level: advanced
summary: Given a polynomial equation with integer coefficients, decide whether it has a solution in integers. The MRDP theorem (1970) shows that no algorithm does this.
prereqs: [halting-problem, recursively-enumerable-language, many-one-reducibility]
see_also: [halting-problem, recursively-enumerable-language, undecidability, linear-diophantine-system, pell-equation, godel-incompleteness-theorem, turing-completeness, tarski-decidability-theorem]
sources:
  - paper: doi:10.1090/S0002-9904-1902-00923-3
    title: David Hilbert, Mathematical problems, Bulletin of the American Mathematical Society 8(10) (1902), translated by Mary Winston Newson
    locator: pp. 437 to 479, problem 10, Determination of the solvability of a Diophantine equation
  - paper: doi:10.2307/1970289
    title: Martin Davis, Hilary Putnam and Julia Robinson, The decision problem for exponential Diophantine equations, Annals of Mathematics 74(3) (1961)
    locator: pp. 425 to 436
  - title: Yuri V. Matiyasevich, Enumerable sets are Diophantine, Doklady Akademii Nauk SSSR 191(2) (1970); English translation in Soviet Mathematics Doklady 11(2) (1970)
    locator: pp. 279 to 282 of the Russian original
  - paper: doi:10.2307/2318339
    title: James P. Jones, Daihachiro Sato, Hideo Wada and Douglas Wiens, Diophantine representation of the set of prime numbers, American Mathematical Monthly 83(6) (1976)
    locator: pp. 449 to 464
  - paper: doi:10.2307/2273588
    title: James P. Jones, Universal Diophantine equation, Journal of Symbolic Logic 47(3) (1982)
    locator: pp. 549 to 571 (the proof that nine unknowns suffice)
  - book: isbn:9780262132954
    title: Yuri V. Matiyasevich, Hilbert's Tenth Problem, MIT Press, 1993
---

Hilbert's tenth problem asks for an algorithm that decides whether a polynomial equation with integer coefficients, in any number of unknowns, has a solution in integers. Such an equation is called *Diophantine*. Hilbert posed the problem in his Paris address of 1900, in the form "devise a process" that decides solvability. The answer is that no such process exists. Davis, Putnam and Robinson proved in 1961 that every computably enumerable (c.e.) set is defined by an exponential Diophantine equation, and Matiyasevich removed the exponential in 1970. The result, now called the MRDP theorem, says that the c.e. sets and the Diophantine sets are the same. Since the [halting problem](/halting-problem/) is c.e. and undecidable, Diophantine solvability is undecidable.

## In plain words

Take an equation built from whole numbers and unknowns with plus, minus and times, such as "x squared minus 61 times y squared equals 1". Does it have a solution in whole numbers?

For some equations a trick gives the answer. Sometimes a short search finds a solution. Sometimes a remainder argument shows there is none. Hilbert asked for one method that works for every equation.

There is no such method. Equations of this kind can describe any computer program: for each program there is an equation that has a solution exactly when the program stops. A method for equations would then tell whether any program stops, and no method can do that.

## Definition

**Instance.** A polynomial $P(x_1, \ldots, x_n)$ with integer coefficients, given as a list of monomials with their coefficients.

**Question.** Are there integers $x_1, \ldots, x_n$ with $P(x_1, \ldots, x_n) = 0$?

Solutions in natural numbers give an equivalent problem. $P$ has a solution in integers if and only if $P(y_1 - z_1, \ldots, y_n - z_n)$ has one in natural numbers. In the other direction, by Lagrange's four-square theorem, $P$ has a solution in natural numbers if and only if $P(a_1^2 + b_1^2 + c_1^2 + d_1^2, \ldots)$ has one in integers. Both maps are many-one reductions.

A set $S \subseteq \mathbb{N}^k$ is *Diophantine* if there is a polynomial $P$ with integer coefficients such that
$$(a_1, \ldots, a_k) \in S \iff \exists x_1, \ldots, x_n \in \mathbb{N}\ \ P(a_1, \ldots, a_k, x_1, \ldots, x_n) = 0.$$

**MRDP theorem (Matiyasevich 1970, completing Davis, Putnam and Robinson 1961).** A set of natural numbers is Diophantine if and only if it is computably enumerable.

**Corollary.** Hilbert's tenth problem is undecidable. Take a Diophantine definition $P(a, x_1, \ldots, x_n)$ of the set $K$ of the [halting problem](/halting-problem/). Then $a \mapsto P(a, x_1, \ldots, x_n)$ is a many-one reduction from $K$ to Diophantine solvability, so a decision procedure for equations would decide $K$.

The easy direction of the theorem is that every Diophantine set is c.e.: list all tuples $x$ and check each. The hard direction has two main steps. Davis, Putnam and Robinson showed that bounded universal quantifiers can be removed if exponentiation is allowed, so every c.e. set is defined by an exponential Diophantine equation. Julia Robinson had shown earlier that exponentiation is Diophantine if some Diophantine relation grows exponentially without growing too fast. Matiyasevich found such a relation: $v = F_{2u}$, where $F_m$ is the $m$-th Fibonacci number.

## Variants

- **One unknown.** Decidable. An integer root of $a_d x^d + \cdots + a_0$ with $a_0 \neq 0$ divides $a_0$, so only finitely many candidates need checking. If $a_0 = 0$, then $x = 0$ is a root.
- **Linear systems.** Decidable in polynomial time, by the Hermite or Smith normal form; see [linear Diophantine systems](/linear-diophantine-system/). One equation $a x + b y = c$ is solvable if and only if $\gcd(a, b)$ divides $c$, which the [Euclidean algorithm](/euclidean-algorithm/) checks.
- **Few unknowns.** Undecidable with $9$ unknowns over the natural numbers (Matiyasevich, with the proof written out by Jones 1982). For two to eight unknowns the question is open; one unknown is decidable, as above.
- **Low degree.** Undecidable for degree $4$. Any system can be cut down by naming each product $u = v w$ with a new unknown, and a system $P_1 = 0, \ldots, P_r = 0$ is solvable if and only if $P_1^2 + \cdots + P_r^2 = 0$ is. The equations $u - v w = 0$ have degree $2$, so the sum of squares has degree $4$.
- **Exponential Diophantine equations.** Allowing terms $x^y$ only makes the problem harder, and it is undecidable by the 1961 theorem.
- **Rational solutions.** Whether a polynomial equation has a solution in rational numbers is open.
- **Real solutions.** Decidable, since the first-order theory of the real numbers is decidable by [Tarski's theorem](/tarski-decidability-theorem/).

## Examples

**Pell's equation.** The equation $x^2 - 61 y^2 = 1$ has the smallest positive solution $x = 1766319049$, $y = 226153980$. For $d = 2$ the smallest positive solution of $x^2 - 2 y^2 = 1$ is $(3, 2)$. For every positive $d$ that is not a square, $x^2 - d y^2 = 1$ has a positive solution, found by the continued fraction of $\sqrt{d}$; see [Pell's equation](/pell-equation/). The example shows how far the smallest solution can be from the size of the equation.

**No solution, by remainders.** The equation $x^2 + y^2 = 3$ has no integer solution. Squares leave remainder $0$ or $1$ when divided by $4$, so a sum of two squares leaves $0$, $1$ or $2$, never $3$. Tests like this one can prove that there is no solution, but there are equations with no integer solution that pass every such test, so they do not give an algorithm.

**Sums of three cubes.** The equation $x^3 + y^3 + z^3 = 29$ has the solutions $(1, 1, 3)$ and $(-3, -2, 4)$. For other right-hand sides the smallest solutions can be very large, and the question for general $k$ is open.

**The primes.** Jones, Sato, Wada and Wiens (1976) wrote down a polynomial of degree $25$ in $26$ unknowns whose positive values, as the unknowns range over the natural numbers, are exactly the prime numbers. The MRDP theorem says such a polynomial exists for every c.e. set.

## Known algorithms

- **Search.** List all tuples in order of size and test each. This is a semi-decision procedure: it halts exactly on the solvable equations.
- **Local tests.** If the equation has no solution modulo some $m$, or no real solution, then it has no integer solution. These tests are decidable, and they settle many equations in practice, but not all.
- **Special classes.** One unknown, linear systems, and Pell's equation and other equations of degree $2$ in two unknowns have their own algorithms.

## Bounds

- **Undecidable** in general, for $9$ unknowns over the natural numbers, and for degree $4$.
- **No computable bound on solutions.** There is no computable function $f$ such that every solvable equation of size $s$ has a solution with entries at most $f(s)$. Otherwise a bounded search would decide the problem.
- **Complete.** Diophantine solvability is complete for the c.e. sets under many-one reductions, so it has the same [Turing degree](/turing-degrees/) as the halting problem.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **From the halting problem.** By the MRDP theorem the set $K$ has a Diophantine definition $P(a, x)$, and $a \mapsto P(a, \cdot)$ is the reduction.
- **To the halting problem.** Map an equation to the machine that searches for a solution and halts when it finds one.
- **Between integers and natural numbers.** The two substitutions in the Definition.

## Applications

- **Incompleteness in number theory.** For every consistent, c.e. theory that proves the basic facts of arithmetic, there is a Diophantine equation with no solution such that the theory cannot prove that it has no solution. This is a concrete form of [Gödel's incompleteness theorem](/godel-incompleteness-theorem/).
- **Open problems as equations.** Each statement of the form "no number has this decidable property" is equivalent to the unsolvability of one Diophantine equation. Goldbach's conjecture is an example: it holds if and only if a certain polynomial equation has no solution.
- **Other undecidable problems.** The MRDP theorem is used to show undecidability in other parts of mathematics, for example for problems about integer programs with polynomial constraints.
- **Universality.** There is a single "universal" polynomial: for every c.e. set $S$ there is an index $e$ such that $a \in S$ exactly when $P_U(e, a, x) = 0$ has a solution, so polynomial equations are a [Turing complete](/turing-completeness/) model of computation.

## References
