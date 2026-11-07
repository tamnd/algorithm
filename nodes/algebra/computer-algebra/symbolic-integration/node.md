---
tag: FZWKDA
kind: problem
slug: symbolic-integration
name: Symbolic integration
aliases: [integration in finite terms, indefinite integration, antiderivative in closed form]
area: algebra/computer-algebra
level: core
summary: Find an antiderivative of an elementary function in closed form, or prove none exists.
prereqs: [polynomial-ring, partial-fraction-decomposition, polynomial-gcd]
see_also: [integration-of-rational-functions, hermite-reduction, rothstein-trager, risch-algorithm, risch-norman-heuristic, liouville-theorem, richardson-theorem, indefinite-summation]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2 (integration of rational functions), Chapter 3 (differential fields and elementary extensions), Chapter 5 (integration of transcendental functions and Liouville's theorem), Chapter 6 (the Risch differential equation)
  - paper: doi:10.1090/S0002-9947-1969-0237477-8
    title: Robert H. Risch, The problem of integration in finite terms, Transactions of the American Mathematical Society 139, 1969
    locator: pp. 167 to 189 (the decision procedure for towers of logarithms and exponentials)
  - paper: doi:10.1090/S0002-9904-1970-12454-5
    title: Robert H. Risch, The solution of the problem of integration in finite terms, Bulletin of the American Mathematical Society 76(3), 1970
    locator: pp. 605 to 608 (announcement of the algorithm for the general elementary case, with algebraic functions)
  - paper: doi:10.1080/00029890.1972.11993166
    title: Maxwell Rosenlicht, Integration in finite terms, American Mathematical Monthly 79(9), 1972
    locator: pp. 963 to 972 (the algebraic proof of Liouville's theorem)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of Rational Functions, and Chapter 12, The Risch Integration Algorithm
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 22, Symbolic integration (Hermite's method and the method of Lazard, Rioboo, Rothstein and Trager, with cost bounds)
---

Symbolic integration is the problem of finding, for a function $f$ given by a formula, a formula $g$ in a stated class with $g' = f$, or proving that no such $g$ exists. The classic class is the elementary functions: those built from $x$ and constants by the field operations, exponentials, logarithms and algebraic functions. [Liouville's theorem](/liouville-theorem/) says what shape an elementary antiderivative must have, and the [Risch algorithm](/risch-algorithm/) turns that shape into a decision procedure. For rational functions the answer always exists and is computed by [Hermite reduction](/hermite-reduction/) and the [Rothstein-Trager](/rothstein-trager/) or [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) method.

## In plain words

In a calculus course you learn rules that turn a formula into its derivative, and every formula has one. Going backwards is harder. Some formulas, like the bell curve or the sine of x divided by x, have no antiderivative that you can write with the usual functions. Tables of integrals and clever tricks find answers, but when they fail you do not know if an answer exists.

Symbolic integration asks for a method that always gives one of two results: a formula whose derivative is the input, or a proof that no formula of the allowed kind exists. Such a method exists for a large class of inputs. It does not guess. It works out exactly which logarithms and exponentials an answer can use, and then solves for the unknown parts.

## Definition

**Differential fields.** A *differential field* is a field $K$ with a map $D : K \to K$ (written $f \mapsto f'$) that satisfies $(f + g)' = f' + g'$ and $(fg)' = f' g + f g'$. Its *constants* are $\operatorname{Const}(K) = \{ c \in K : c' = 0 \}$, a subfield. The base case is $K = C(x)$ with $C$ a field of constants of characteristic zero and $x' = 1$.

**Elementary extensions.** An extension $E = K(t_1, \ldots, t_m)$ of differential fields is *elementary* over $K$ when each $t_i$, over $K_{i-1} = K(t_1, \ldots, t_{i-1})$, is

- a *logarithm*: $t_i' = a'/a$ for some $a \in K_{i-1}^{*}$ (we write $t_i = \log a$),
- an *exponential*: $t_i'/t_i = b'$ for some $b \in K_{i-1}$ (we write $t_i = \exp b$), or
- *algebraic*: $t_i$ is algebraic over $K_{i-1}$.

A function is *elementary* when it lies in an elementary extension of $C(x)$. Trigonometric functions and their inverses are elementary over $\mathbb{C}$, since $\tan x = -i \, (e^{2ix} - 1)/(e^{2ix} + 1)$ and $\arctan x = \frac{i}{2} \log \frac{i + x}{i - x}$ up to a constant.

**The problem.** Input: an elementary extension $E$ of $C(x)$, given as a tower in which each $t_i$ is presented by its defining equation, and an element $f \in E$. Output: either an elementary extension $F$ of $E$ with $\operatorname{Const}(F)$ algebraic over $C$ and an element $g \in F$ with $g' = f$, or the answer *no elementary antiderivative exists*.

The condition on the constants excludes trivial answers: without it, one could adjoin a new symbol $g$ with $g' = f$ and call it a constant-free solution. The output $g$ is a formula: a sum of an element of $E$ and constant multiples of logarithms of elements of $E(c_1, \ldots, c_k)$, where the $c_j$ are algebraic constants. This is the content of Liouville's theorem (Rosenlicht 1972; Bronstein, Chapter 5): if $f \in E$ has an elementary antiderivative, then

$$f = v' + \sum_{i=1}^{k} c_i \frac{u_i'}{u_i}$$

with $c_i$ algebraic over $C$ and $v, u_i \in E(c_1, \ldots, c_k)$.

**The cost model.** Algorithms work over an exact constant field: field operations in $C$ count one unit, or, over $\mathbb{Q}$, bit operations with bounds on the coefficient size. They also need a test for zero in $C$ and in each $K_{i}$. For a tower given by formulas, that test is the [constant problem](/constant-problem/), which is undecidable for some natural classes; see Bounds.

## Variants

- **Rational functions.** $E = C(x)$. An antiderivative always exists in an elementary extension: a rational part plus a sum of constant multiples of logarithms. The question is only how to write it with the fewest new constants. See [integration of rational functions](/integration-of-rational-functions/).
- **Transcendental towers.** Each $t_i$ is a logarithm or an exponential that is transcendental over $K_{i-1}$ with no new constants. The Risch algorithm (Risch 1969) decides this case, given the zero test. This is the subject of Bronstein's book.
- **Algebraic and mixed towers.** Some $t_i$ are algebraic. Risch (1970) announced an algorithm. Trager (1984, for purely algebraic functions) and Bronstein (1990, for mixed towers) gave implementable versions. The hard step is to decide whether a divisor on a curve is of finite order.
- **Liouvillian and special-function answers.** Allow the answer to use functions such as the error function, the exponential integral, the logarithmic integral or polylogarithms. Then $\int e^{-x^2} dx$ is $\frac{\sqrt{\pi}}{2} \operatorname{erf}(x)$. Extensions of the Risch method handle some of these classes.
- **Heuristic integration.** Guess the shape of the answer and solve for its coefficients without the full decision procedure. See the [Risch-Norman heuristic](/risch-norman-heuristic/). A failure then proves nothing.
- **Definite integrals.** Compute $\int_a^b f$ without an antiderivative, for example by creative telescoping on [holonomic functions](/holonomic-function/). This is a different problem: $\int_0^\infty e^{-x^2} dx = \sqrt{\pi}/2$ has a closed form even though the indefinite integral is not elementary.
- **The discrete analogue.** [Indefinite summation](/indefinite-summation/) asks for $g$ with $g(k+1) - g(k) = f(k)$. Gosper's algorithm plays the role of the Risch algorithm for hypergeometric terms.

## Examples

- $\int \log x \, dx = x \log x - x$. Here $E = \mathbb{Q}(x, t)$ with $t = \log x$, and the answer lies in $E$.
- $\int x e^{x^2} dx = \tfrac{1}{2} e^{x^2}$. With $t = \exp(x^2)$, the answer is $b t$ where $b \in \mathbb{Q}(x)$ solves $b' + 2x b = x$, so $b = 1/2$.
- $\int x e^{x} dx = (x - 1) e^x$, from $b' + b = x$ with $b = x - 1$.
- $\int e^{-x^2} dx$ is not elementary. An answer would be $b \, e^{-x^2}$ with $b \in \mathbb{Q}(x)$ and $b' - 2x b = 1$. A pole of $b$ of order $m \ge 1$ gives a pole of $b'$ of order $m + 1$ that nothing cancels, so $b$ is a polynomial. If $b \ne 0$, the degree of $b' - 2xb$ is $\deg b + 1 \ge 1$, so it cannot equal $1$. Hence no $b$ exists. The same argument shows that $\int e^x / x \, dx$ is not elementary: $b' + b = 1/x$ forces a simple pole of $b'$, which is impossible.
- $\int \frac{dx}{x^2 - 2} = \frac{1}{2\sqrt{2}} \log \frac{x - \sqrt{2}}{x + \sqrt{2}}$. The answer exists, but it needs the new constant $\sqrt{2}$. The Rothstein-Trager resultant $8z^2 - 1$ shows that no answer with rational constants exists.
- $\int \frac{x + 1}{x^2 + 1} dx = \tfrac{1}{2} \log(x^2 + 1) + \arctan x$. Over $\mathbb{Q}$ the logarithmic part needs the constants $\pm i/2$, and over $\mathbb{R}$ the arctangent is the usual way to write it.
- $\int \frac{dx}{\log x}$ (the logarithmic integral) and $\int \frac{\sin x}{x} dx$ (the sine integral) are not elementary.

## Known algorithms

| algorithm | input class | output | cost |
|---|---|---|---|
| [Hermite reduction](/hermite-reduction/) | rational functions | rational part, and a remainder with squarefree denominator | $O(M(d) \log d)$ field operations for degree $d$ (von zur Gathen and Gerhard, Chapter 22) |
| [Horowitz-Ostrogradsky](/horowitz-ostrogradsky/) | rational functions | rational part by one linear system | a linear system of size $O(d)$ |
| [Rothstein-Trager](/rothstein-trager/) | proper rational function with squarefree denominator | logarithmic part with the fewest constants | a resultant, a factorization over $C$ and gcds over number fields |
| [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) | same | same, without algebraic numbers in the gcd step | subresultants, polynomial in $d$ |
| [Risch algorithm](/risch-algorithm/) | transcendental (and, in its full form, algebraic) elementary towers | an elementary antiderivative or a proof that none exists | no simple bound in the input size |
| [Risch-Norman heuristic](/risch-norman-heuristic/) | towers of logarithms, exponentials and tangents | an antiderivative of a guessed shape, or failure | one linear system per guess |

## Bounds

- **Rational functions.** The rational part and the logarithmic part are computed in time polynomial in the degree, in field operations, and in time polynomial in the degree and the coefficient length for inputs over $\mathbb{Q}$. Von zur Gathen and Gerhard give explicit bounds in Chapter 22. Rothstein and Trager showed that the smallest field of constants over which the logarithmic part can be written is the splitting field of the resultant that their method computes, so no method can avoid these constants.
- **Transcendental towers.** Risch's algorithm decides the problem when the constant field is computable and zero is decidable in each field of the tower. The procedure reduces the problem to polynomial arithmetic, to Risch differential equations $y' + f y = g$, and to linear algebra over the constants. Its cost depends on the height of the tower and on degree bounds for the Risch differential equation, and no bound in terms of the input size alone is standard.
- **Undecidability.** Without a zero test the problem is not decidable. [Richardson's theorem](/richardson-theorem/) (1968) shows that for expressions built from $x$, $\pi$, $\log 2$, the rational numbers, $\sin$, $\exp$ and $|\cdot|$, it is undecidable whether an expression is identically zero, and that it is undecidable whether such an expression has an antiderivative in the same class. So every complete integration algorithm must assume a zero test for its constants and functions.

## Reductions

- **Zero test to integration.** Deciding whether $\int f$ is elementary is at least as hard as deciding whether an expression is zero: For a constant expression $c$, the function $c \, e^{x^2}$ has an elementary antiderivative if and only if $c = 0$, by the argument of the example for $e^{-x^2}$ (here $b' + 2x b = 1$ has no rational solution). So a procedure that decides integrability also decides whether $c = 0$, and Richardson's undecidable zero test for constants transfers to integration.
- **Integration to the Risch differential equation.** In a tower whose top is an exponential $t = \exp(u)$, the coefficient $a_i$ of $t^i$ in a Laurent polynomial integrand contributes $b_i t^i$ to the antiderivative, where $b_i$ solves $b_i' + i u' b_i = a_i$ in the field below. So the exponential case reduces to one differential equation per power. See the [Risch algorithm](/risch-algorithm/).
- **The logarithmic part to a resultant.** For a proper rational function $A/D$ with squarefree $D$, the constants that the logarithmic part needs are the roots of $\operatorname{res}_x(D, A - z D')$, a polynomial in $z$. This is the [Rothstein-Trager](/rothstein-trager/) method.

## Applications

- The integration commands of computer algebra systems (Axiom and its successor FriCAS implement a large part of the Risch algorithm, including algebraic cases; other systems combine parts of it with heuristics and tables).
- Proofs that an integral has no closed form, as in the examples above, which justify the use of special functions and numerical methods.
- Closed forms for physics and engineering integrals, and the reduction of differential equations with integrating factors, see [closed form ODE solving](/closed-form-ode-solving/).
- Rational function integration is the base case of the [creative telescoping](/creative-telescoping/) methods for definite integrals.

## References
