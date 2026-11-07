---
tag: 267HQ1
kind: problem
slug: closed-form-ode-solving
name: Closed-form solution of linear ODEs
aliases:
- symbolic ODE solving
- Liouvillian solutions of linear ODEs
- solving linear differential equations in closed form
area: algebra/computer-algebra
level: advanced
summary: Find solutions of linear differential equations in terms of elementary functions.
prereqs: [symbolic-integration]
see_also: [kovacic-algorithm, differential-galois-theory, risch-algorithm, liouville-theorem, holonomic-function, ore-algebra, constant-problem]
sources:
  - book: isbn:9783540442288
    title: Marius van der Put and Michael F. Singer, Galois Theory of Linear Differential Equations, Springer, 2003
    locator: Chapter 4 (algorithmic considerations, rational and exponential solutions, factoring operators and Liouvillian solutions) and Chapter 1 (Picard-Vessiot theory and Liouvillian extensions)
  - paper: doi:10.1016/S0747-7171(86)80010-4
    title: Jerald J. Kovacic, An algorithm for solving second order linear homogeneous differential equations, Journal of Symbolic Computation 2(1), 3-43, 1986
    locator: the four cases of the Galois group of a second-order equation and the algorithm for Liouvillian solutions
  - paper: doi:10.2307/2374045
    title: Michael F. Singer, Liouvillian solutions of n-th order homogeneous linear differential equations, American Journal of Mathematics 103(4), 661-682, 1981
    locator: the decision procedure for Liouvillian solutions of equations of any order with coefficients in an algebraic extension of Q(x)
  - paper: "Sergei A. Abramov, Rational solutions of linear differential and difference equations with polynomial coefficients, USSR Computational Mathematics and Mathematical Physics 29(6), 7-12, 1989"
    locator: the bounds on the denominator of a rational solution from the indicial equations at the singular points
---

Closed-form solution of linear ODEs is the problem of finding all solutions of a linear differential equation with rational function coefficients that can be written in a given class of functions: polynomials, rational functions, exponentials of integrals of rational functions, or the Liouvillian functions built from these by integration, exponentiation and algebraic operations. The problem is decidable for all of these classes. The decision procedures come from differential Galois theory: an equation has Liouvillian solutions exactly when its differential Galois group is small enough, and Kovacic's algorithm (1986) makes this practical for second-order equations.

## In plain words

A differential equation relates an unknown function to its derivatives. Solving it in closed form means writing the answer with familiar pieces: powers, fractions, exponentials, logarithms, roots and integrals.

Some equations have such answers and many do not. The equation behind the Airy function, which appears in optics and quantum mechanics, has no answer built from those pieces. The problem asks a computer to decide which case holds and, when an answer exists, to produce it. For linear equations, mathematicians know how to do this exactly, though the general method is slow; for equations of order two there is a fast method.

## Definition

Let $k$ be a computable field of characteristic 0, for example $\mathbb{Q}$ or a number field, let $\bar{k}$ be its algebraic closure, and let $K = \bar{k}(x)$ with the derivation $' = d/dx$. A linear differential operator of order $n$ is

$$L = a_n \partial^n + a_{n-1} \partial^{n-1} + \cdots + a_0, \qquad a_i \in k[x],\ a_n \ne 0,$$

acting by $L(y) = a_n y^{(n)} + \cdots + a_0 y$. The solutions of $L(y) = 0$ form an $n$-dimensional vector space over the constants in a Picard-Vessiot extension of $K$ (see [differential Galois theory](/differential-galois-theory/)).

**Input:** $L$, given by the polynomials $a_i$, and a class $\mathcal{C}$ of functions.
**Output:** a basis of the solutions of $L(y) = 0$ that lie in $\mathcal{C}$.

The classes, from small to large:

- *polynomial* solutions $y \in \bar{k}[x]$ and *rational* solutions $y \in K$;
- *hyperexponential* (or exponential) solutions, $y \ne 0$ with $y'/y \in K$, that is $y = \exp(\int u)$ with $u \in K$;
- *Liouvillian* solutions, which lie in a tower $K = K_0 \subset K_1 \subset \cdots \subset K_m$ in which each step adjoins an integral ($t' \in K_{i-1}$), an exponential of an integral ($t'/t \in K_{i-1}$), or an algebraic element, all with the same constants.

Costs are counted in operations in $k$ (or in the number field that the algorithm constructs), with the order $n$ and the degree $d$ of the coefficients as parameters. Elementary functions are Liouvillian, so the Liouvillian class contains all closed forms in the usual sense.

## Variants

- **Inhomogeneous equations** $L(y) = f$. With a basis of solutions of $L(y) = 0$, variation of constants reduces the problem to integrals; for order 1 the problem is $y' + p y = q$, solved by $y = e^{-\int p} \int q e^{\int p}$, so it contains [symbolic integration](/symbolic-integration/).
- **Constant coefficients.** If every $a_i \in k$, the solutions are $x^j e^{\lambda x}$ for the roots $\lambda$ of the characteristic polynomial; the problem reduces to factoring a polynomial over $k$.
- **Factoring operators.** Write $L = L_1 L_2$ with operators of lower order. A hyperexponential solution is the same as a right factor of order 1. Beke (1894) gave a method; modern algorithms use local exponents and generalized series (van Hoeij 1997).
- **Special function solutions.** Solutions in terms of Bessel, Whittaker or Gauss hypergeometric functions, found by matching local data against a list of known equations (work of van Hoeij and coauthors).
- **Nonlinear first-order equations.** Find elementary first integrals of $y' = P(x, y)/Q(x, y)$ (Prelle and Singer 1983). The Riccati equation $u' + u^2 = r$ is the special case tied to second-order linear equations.
- **Difference equations.** The discrete analogue: rational, hypergeometric and Liouvillian solutions of linear recurrences (Abramov; Petkovšek's algorithm Hyper).

## Examples

Each solution below was checked by substituting it back into the equation.

- $y'' + y = 0$ has constant coefficients, characteristic polynomial $\lambda^2 + 1$, and solutions $e^{ix}$ and $e^{-ix}$, or $\sin x$ and $\cos x$. They are hyperexponential.
- $x^2 y'' - 2y = 0$ has the singular point $0$, where the indicial equation is $r(r - 1) - 2 = 0$ with roots $2$ and $-1$. The rational solution algorithm bounds the pole order at 0 by 1 and the degree at infinity by 2, and finds the basis $x^2$ and $1/x$.
- $y'' = (x^2 + 1) y$ has the hyperexponential solution $y = e^{x^2/2}$: the Riccati equation $u' + u^2 = x^2 + 1$ for $u = y'/y$ has the rational solution $u = x$. This is case 1 of Kovacic's algorithm. A second solution is $e^{x^2/2} \int e^{-x^2}$, which is Liouvillian but not elementary.
- The Airy equation $y'' = x y$ has no Liouvillian solution. Kovacic's algorithm shows that none of its three cases applies, so the differential Galois group is $\mathrm{SL}_2$.
- $y' - 2xy = 1$ has the solution $y = e^{x^2} \int e^{-x^2}\,dx$, Liouvillian but not elementary; the Risch algorithm proves the last integral is not elementary.

## Known algorithms

- **Polynomial solutions.** The indicial equation at infinity bounds the degree; then the coefficients solve a linear system over $k$. Cost polynomial in $n$, $d$ and the degree bound, which is an integer root of the indicial polynomial and so can be exponential in the bit size of the input.
- **Rational solutions** (Abramov 1989, and earlier methods going back to Liouville). The poles of a rational solution lie among the roots of $a_n$. At each such root $\alpha$, the order of the pole is at most $-r$ for the smallest integer root $r$ of the indicial equation at $\alpha$. Multiplying out the denominator reduces the problem to polynomial solutions.
- **Hyperexponential solutions.** Compute the local exponents at each singular point, including infinity; combine one exponent per point; for each combination, look for a polynomial solution of a transformed equation. The number of combinations can be exponential in the number of singular points, which van Hoeij's methods reduce in practice.
- **Liouvillian solutions of order 2.** [Kovacic's algorithm](/kovacic-algorithm/) normalizes to $y'' = r y$ and tests for a solution $y$ with $y'/y$ rational (case 1), quadratic over $K$ (case 2), or algebraic of degree 4, 6 or 12 (case 3). Each test reduces to finding polynomial solutions.
- **Liouvillian solutions of order $n$.** Singer (1981) proved that if $L$ has a Liouvillian solution, it has one $y$ with $y'/y$ algebraic over $K$ of degree bounded by a function of $n$ alone, from Jordan's theorem on finite linear groups. This gives a decision procedure, made practical for order 3 by Singer and Ulmer and later work.
- **Galois group computation.** Hrushovski (2002) gave an algorithm that computes the differential Galois group of any $L$, which decides every question of this kind in principle.

## Bounds

- **Decidability.** Rational, hyperexponential and Liouvillian solutions are decidable for coefficients in $\bar{\mathbb{Q}}(x)$ (Singer 1981). This is proved.
- **Complexity.** The degree bounds and the case analyses give algorithms whose cost is polynomial in $d$ for fixed $n$ when the integer roots of the indicial equations are small, but the bound in Singer's algorithm grows very fast with $n$ through Jordan's bound, and Hrushovski's algorithm has no practical bound. For order 2, Kovacic's algorithm runs in practice in time polynomial in $d$; the worst case depends on the number of singular points through the exponent combinations.
- **Lower bounds.** No nontrivial lower bounds are known beyond the size of the output, which can be large: a rational solution can have degree equal to a large integer root of the indicial polynomial.

## Reductions

- **Integration** is the order 1 inhomogeneous case $y' = f$, so [symbolic integration](/symbolic-integration/) and the [Risch algorithm](/risch-algorithm/) reduce to this problem, and Liouville's theorem is its counterpart for elementary integrals.
- **Second-order equations to Riccati equations.** $y'' = r y$ has a solution with $y'/y = u$ if and only if $u' + u^2 = r$. Liouvillian solutions correspond to algebraic solutions of the Riccati equation of degree 1, 2, 4, 6 or 12.
- **Solutions to factorization.** A hyperexponential solution is a right factor of order 1; more generally, the solution spaces of right factors are invariant subspaces of the Galois group.
- **Equations to recurrences.** For a power series solution $y = \sum c_m x^m$, the equation $L(y) = 0$ becomes a linear recurrence for $c_m$ with polynomial coefficients, linking this problem to [holonomic functions](/holonomic-function/) and to closed forms of recurrences.

## Applications

- **Computer algebra systems.** The ODE solvers of Maple, Mathematica and other systems combine classification by patterns with these algorithms, often Kovacic's algorithm for order 2.
- **Integrability.** The Morales-Ramis theory deduces nonintegrability of Hamiltonian systems from the Galois group of a variational equation, which is computed with these methods.
- **Physics and combinatorics.** Feynman integrals, generating functions of lattice walks and other D-finite functions are described by linear ODEs whose closed-form solutions, when they exist, give explicit formulas.
- **Special functions.** Deciding whether a function given by an equation is new or reducible to known functions.

## References
