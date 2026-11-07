---
tag: 2J4T9A
kind: problem
slug: constant-problem
name: Constant problem
aliases:
- zero-equivalence problem
- zero testing
- identity problem for elementary functions
area: algebra/computer-algebra
level: advanced
summary: Decide whether an expression built from elementary functions equals zero.
prereqs: [expression, canonical-form]
see_also: [richardson-theorem, hilberts-tenth-problem, polynomial-identity-testing, schwartz-zippel-lemma, risch-algorithm, straight-line-program, expression-swell]
sources:
  - paper: doi:10.2307/2271358
    title: Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4), 514-520, 1968
    locator: the reduction from Hilbert's tenth problem showing that identity to zero is undecidable for expressions in x with rationals, pi, ln 2, sin, exp and the absolute value
  - paper: doi:10.1006/jsco.1997.0157
    title: Daniel Richardson, How to recognize zero, Journal of Symbolic Computation 24(6), 627-645, 1997
    locator: the zero test for constants built with exp and log, correct on every input and terminating on every input if Schanuel's conjecture holds
  - paper: doi:10.1145/321574.321591
    title: B. F. Caviness, On canonical forms and simplification, Journal of the ACM 17(2), 385-396, 1970
    locator: the equivalence of canonical simplification and zero equivalence, and the extension of Richardson's undecidability result
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3 (normal and canonical functions, zero equivalence and Richardson's theorem)
  - paper: doi:10.1137/070697926
    title: Eric Allender, Peter Bürgisser, Johan Kjeldgaard-Pedersen and Peter Bro Miltersen, On the complexity of numerical analysis, SIAM Journal on Computing 38(5), 1987-2006, 2009
    locator: the problems EquSLP and PosSLP for integers given by straight-line programs, and the equivalence of EquSLP with polynomial identity testing
---

The constant problem asks whether a given expression, built from integers by arithmetic operations and functions such as $\exp$, $\log$, $\sin$ and square roots, denotes the number zero. Its functional form, the *zero-equivalence problem*, asks whether an expression in variables is zero for all values of the variables. Every simplifier, every exact linear algebra routine over an expression field and every symbolic integrator needs this test, because they must know whether a pivot, a leading coefficient or a residue vanishes. For rational functions the problem is easy; Richardson (1968) proved it undecidable for expressions in one real variable that use $\pi$, $\sin$, $\exp$ and the absolute value, and for constants built with $\exp$ and $\log$ it is decidable if Schanuel's conjecture holds.

## In plain words

A computer algebra system often has to answer one plain question: is this expression zero? Sometimes the expression looks complicated but is zero in disguise, like a long formula that simplifies to nothing. Sometimes it looks like zero when evaluated with a calculator but is a tiny nonzero number.

Evaluating with more and more digits can prove that a number is not zero, as soon as a nonzero digit appears. It can never prove that a number is zero, because the next digit might be nonzero. For simple kinds of expressions there are exact methods. For rich enough kinds of expressions, no method can always answer, and for some kinds the answer is still unknown.

## Definition

Fix a class $\mathcal{E}$ of expressions, given as trees or DAGs (see [expression](/expression/)): constants from $\mathbb{Q}$ or $\mathbb{Z}$, possibly $\pi$ and $i$, variables $x_1, \ldots, x_n$, the operations $+, -, \times, /$, and a set of functions such as $\exp$, $\log$, $\sin$, $|\cdot|$ and $\sqrt{\cdot}$ with fixed branches.

- **Constant problem.** Input: an expression $E \in \mathcal{E}$ without variables that is defined (no division by zero, logarithms of nonzero arguments). Output: whether the complex number denoted by $E$ is $0$.
- **Zero-equivalence problem.** Input: an expression $E(x_1, \ldots, x_n) \in \mathcal{E}$ and a domain $U$, usually $\mathbb{R}^n$ or an open set where $E$ is defined. Output: whether $E(a) = 0$ for every $a \in U$.

The size of the input is the number of nodes of the expression. In decidable cases the cost is counted in bit operations, since the numbers involved are exact.

## Variants

- **Rational expressions.** $\mathcal{E}$ has only $+, -, \times, /$ over $\mathbb{Q}$. Zero equivalence is decided by reducing to a canonical form, a quotient of expanded coprime polynomials.
- **Algebraic constants.** Expressions with radicals or roots of given polynomials. Decidable by computing a minimal polynomial with resultants, or by numerical evaluation to a precision fixed by a root separation bound.
- **Exp-log constants.** Constants built from $\mathbb{Q}$ with arithmetic, $\exp$ and $\log$, the *elementary numbers*. Richardson's algorithm (1997) is correct whenever it stops, and it stops on every input if Schanuel's conjecture is true.
- **Exp-log functions.** Expressions in $x$ with arithmetic, $\exp$ and $\log$. By the Risch structure theorem, zero equivalence reduces to the constant problem for the constants that occur.
- **Classes with periodic functions and absolute value.** Undecidable by Richardson's theorem; see below.
- **Integers given by straight-line programs.** The problem EquSLP: does an arithmetic circuit with constants $0, 1$ and gates $+, -, \times$ compute $0$? The numbers can have exponentially many digits, so direct evaluation is too slow.
- **Polynomial identity testing.** Zero equivalence for polynomials given by [straight-line programs](/straight-line-program/) or circuits; see [polynomial identity testing](/polynomial-identity-testing/).

## Examples

The values below were computed with Python's `decimal` module at 80 significant digits.

- $\sqrt{2} + \sqrt{3} - \sqrt{5 + 2\sqrt{6}} = 0$, because $(\sqrt{2} + \sqrt{3})^2 = 5 + 2\sqrt{6}$ and both sides are positive. Numerically the difference evaluates to $10^{-79}$ in magnitude, a rounding error. A minimal polynomial computation proves that it is exactly 0.
- $e^{\pi \sqrt{163}} - 640320^3 - 744 \approx -7.4993 \times 10^{-13}$. The number is not zero, but $640320^3 + 744$ has 18 digits and the first 12 digits after the point are zeros, so evaluation with 30 significant digits would report 0. More digits prove it is nonzero.
- $\log 6 - \log 2 - \log 3 = 0$, by the law $\log(ab) = \log a + \log b$ for positive reals.
- $e^{\pi} - \pi = 19.99909997\ldots$ is close to 20 but not equal to it; again numerical evaluation settles the nonzero case.
- $\sin^2 x + \cos^2 x - 1$ is zero equivalent on $\mathbb{R}$. So is $|x|^2 - x^2$. But $\sqrt{x^2} - x$ is not: with the positive branch it equals $-2x$ for $x < 0$.
- Whether $e + \pi$ or $e \pi$ is rational, that is, whether $q(e + \pi) - p = 0$ for some integers $p, q$, is unknown. This shows how far the constant problem for $\exp$ and $\pi$ is from being solved.

## Known algorithms

- **Canonical forms.** For classes with a canonical simplifier, $E \equiv 0$ if and only if the canonical form of $E$ is $0$. Caviness (1970) showed the converse: for classes closed under subtraction, a decidable zero test gives a normal simplifier, and so the two problems are equivalent. See [canonical form](/canonical-form/).
- **Numerical evaluation with a separation bound.** For algebraic constants, a bound computed from the expression (for example from the degree and height of the minimal polynomial, or the bounds of Burnikel, Fleischer, Mehlhorn and Schirra used in exact geometric computation) says how close to $0$ a nonzero value can be. Evaluating to that precision decides the question. This is how exact real number libraries decide signs.
- **Elimination.** For algebraic expressions, introduce a new variable for each radical with its defining equation, then eliminate with [resultants](/resultant/) or Gröbner bases to obtain a polynomial for the value, and test the root.
- **Random evaluation.** For polynomial identities, evaluate at random points, modulo a random prime if numbers grow; the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) bounds the error probability by the degree divided by the size of the sample set. For EquSLP, evaluate the circuit modulo random primes of polynomially many digits.
- **Richardson's algorithm** for exp-log constants: it builds a system of polynomial and exponential equations satisfied by the subexpressions, uses numerical approximation to choose a root, and uses elimination to test candidate dependencies. Its termination relies on Schanuel's conjecture, and it is correct whenever it terminates.
- **Semi-decision by evaluation.** For any class whose values can be approximated to any precision, the set of nonzero inputs is recursively enumerable: evaluate with $1, 2, 4, \ldots$ digits until the interval excludes $0$. The difficulty is entirely on the zero side.

## Bounds

- **Undecidability (Richardson 1968).** Let $\mathcal{E}$ contain the rationals, $\pi$, $\ln 2$, the variable $x$, the operations $+, -, \times$ and the functions $\sin$, $\exp$ and $|\cdot|$, with substitution. Then zero equivalence on $\mathbb{R}$ is undecidable. The proof reduces the many unknowns of a Diophantine equation to one real variable. It started from the undecidability of exponential Diophantine equations, which is why $\exp$ and $\ln 2$ appear; with Matiyasevich's 1970 negative solution of [Hilbert's tenth problem](/hilberts-tenth-problem/) they can be dropped. See [Richardson's theorem](/richardson-theorem/).
- **Decidable but hard.** Rational and algebraic cases are decidable in time polynomial in the size of the minimal polynomials, which can themselves be exponential in the number of radicals.
- **EquSLP** is in coRP, by modular evaluation, and is polynomial-time equivalent to polynomial identity testing for arithmetic circuits (Allender, Bürgisser, Kjeldgaard-Pedersen and Miltersen 2009). No deterministic polynomial-time algorithm is known. The sign problem PosSLP is at least as hard, since EquSLP reduces to it, and it is known to lie in the counting hierarchy.
- **Exp-log constants.** Decidability is open without Schanuel's conjecture.

## Reductions

- **Hilbert's tenth problem to zero equivalence.** Richardson encodes "the polynomial $p$ with integer coefficients has a root in $\mathbb{Z}^n$" as "a certain expression built from $p$ and $\sin^2(\pi x_i)$ takes a value below 1 somewhere", then uses $|\cdot|$ to turn "below 1 somewhere" into "a certain expression is not identically 0". Undecidability of the first gives undecidability of the second.
- **Zero equivalence of exp-log functions to the constant problem.** By the Risch structure theorem, an exp-log function is zero equivalent if and only if certain constants derived from it are zero; see the [Risch algorithm](/risch-algorithm/).
- **Canonical simplification and zero equivalence** are equivalent for classes closed under subtraction (Caviness 1970): a zero test $Z$ gives the simplifier that maps $E$ to the first expression in a fixed enumeration that $Z$ declares equal to $E$, and a canonical simplifier gives the zero test "is the form of $E$ equal to the form of $0$".
- **Polynomial identity testing and EquSLP** reduce to each other in polynomial time.

## Applications

- **Simplification.** A system cannot decide whether to cancel a factor, choose a branch or report a result as zero without a zero test. Practical systems use heuristics with numerical evaluation and accept that they can be wrong.
- **Symbolic integration.** The Risch algorithm is a decision procedure only relative to the constant problem of its constant field; it must decide whether certain constants vanish to know whether an integral is elementary.
- **Linear algebra over expression fields.** Gaussian elimination must choose nonzero pivots. A pivot that is a hidden zero gives a wrong result; see also [expression swell](/expression-swell/).
- **Exact geometric computation.** Geometric predicates are signs of algebraic expressions in the input coordinates. Exact geometry libraries decide them by floating-point filters followed by separation bounds.
- **Limits and series.** Computing a limit of an exp-log function needs to know which terms of a series vanish, which again is a zero test.

## References
