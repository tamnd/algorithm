---
tag: GY4RMM
kind: algorithm
slug: risch-algorithm
name: Risch algorithm
aliases: [Risch's decision procedure, Risch integration algorithm, Risch-Bronstein algorithm, integration in finite terms algorithm]
area: algebra/computer-algebra
level: research
summary: Decision procedure that finds an elementary antiderivative or proves none exists for elementary functions.
solves: [symbolic-integration]
model: blum-shub-smale-machine
complexity:
  vars: {D: "the largest degree in x of a numerator or denominator of the integrand", m: "the degree of the exponent b", K: "the number of powers of t in the integrand"}
  time: {worst: O(K (D + m)^2 + D^3)}
  space: {extra: O(K (D + m))}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [risch-structure-theorem, liouville-theorem, hermite-reduction, rothstein-trager]
see_also: [symbolic-integration, risch-norman-heuristic, risch-structure-theorem, liouville-theorem, hermite-reduction, rothstein-trager, lazard-rioboo-trager, integration-of-rational-functions]
sources:
  - paper: doi:10.1090/S0002-9947-1969-0237477-8
    title: Robert H. Risch, The problem of integration in finite terms, Transactions of the American Mathematical Society 139, 1969
    locator: pp. 167 to 189 (the decision procedure for purely transcendental elementary functions)
  - paper: doi:10.1090/S0002-9904-1970-12454-5
    title: Robert H. Risch, The solution of the problem of integration in finite terms, Bulletin of the American Mathematical Society 76(3), 1970
    locator: pp. 605 to 608 (the announcement of the algebraic case)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2 (Hermite reduction and Rothstein-Trager), Chapter 5 (the transcendental Risch algorithm), Chapter 6 (the Risch differential equation) and Chapter 7 (the parametric problem)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 12, The Risch integration algorithm (Sections 12.4 to 12.7 for the logarithmic and exponential cases)
  - paper: doi:10.1016/S0747-7171(08)80027-2
    title: Manuel Bronstein, Integration of elementary functions, Journal of Symbolic Computation 9(2), 1990
    locator: pp. 117 to 173 (a complete transcendental algorithm and the mixed algebraic case)
  - paper: doi:10.1016/S0747-7171(08)80006-5
    title: Manuel Bronstein, The transcendental Risch differential equation, Journal of Symbolic Computation 9(1), 1990
    locator: pp. 49 to 60 (degree bounds and denominators for y' + f y = g)
  - paper: doi:10.1007/3-540-10290-6
    title: James H. Davenport, On the Integration of Algebraic Functions, Lecture Notes in Computer Science 102, Springer, 1981
    locator: the algebraic case and the torsion problem for divisors
  - paper: "Barry M. Trager, Integration of algebraic functions, PhD thesis, Massachusetts Institute of Technology, 1984"
    title: Integration of algebraic functions
    locator: integral bases and the algorithm for purely algebraic integrands
  - paper: doi:10.1145/362637.362651
    title: Joel Moses, Symbolic integration, the stormy decade, Communications of the ACM 14(8), 1971
    locator: pp. 548 to 560 (the Risch algorithm in the context of SIN and MACSYMA)
---

The Risch algorithm decides whether an elementary function has an elementary antiderivative, and finds one if it does. It writes the integrand in a tower of fields $\mathbb{Q}(x)(t_1, \ldots, t_n)$ where each $t_i$ is a new logarithm, exponential or algebraic function, and then works down the tower: Hermite reduction removes multiple poles, the Rothstein-Trager resultant finds the logarithms, and the polynomial part leads to Risch differential equations $y' + f y = g$ one level lower. Liouville's theorem says what shape an answer must have, and the structure theorem guarantees that the tower can be built. Robert Risch published the transcendental case in 1969. Manuel Bronstein made it complete and practical for transcendental functions around 1990, and the algebraic case is still only partly implemented. This page shows the whole method and gives a tested implementation of the case of one exponential.

## In plain words

Calculus courses teach many tricks for finding antiderivatives, but a trick that fails proves nothing. The Risch algorithm replaces the tricks by a procedure that always gives an answer: either a formula, or a proof that no formula built from the usual functions exists. It first writes the function in terms of a short list of independent building blocks, such as one exponential and one logarithm. It then treats the function like a fraction of polynomials in the last building block. Repeated factors in the bottom are removed by a fixed rule, simple factors become logarithms, and the rest leads to smaller problems one level down. For example, it finds that x times e^x has the antiderivative (x minus 1) times e^x, and it proves that e^(x^2) has no antiderivative of this kind.

## The problem

Notation follows the rest of this sub-area. A *differential field* is a field $K$ with a derivation $u \mapsto u'$. Here $K$ contains $\mathbb{Q}(x)$ with $x' = 1$, and the constants of every field in the tower are the same field $C$ (for the code, $C = \bar{\mathbb{Q}}$, and all input coefficients are in $\mathbb{Q}$). A *monomial* $t$ over $K$ is transcendental over $K$, adds no constants, and is a logarithm ($t' = a'/a$, $a \in K^*$), an exponential ($t' = b' t$, $b \in K$) or, in the general algorithm, algebraic over $K$. An *elementary extension* is a tower of such steps.

**Input.** A tower $\mathbb{Q}(x) = K_0 \subset \cdots \subset K_n = K$ of monomials and an integrand $f \in K$.

**Output.** An element $F$ of an elementary extension of $K$ with $F' = f$, or a proof that no such $F$ exists.

**Cost model.** Operations in the constant field and in the base field $\mathbb{Q}(x)$. For the code: operations in $\mathbb{Q}$, without a bound on the size of the rational numbers. The general algorithm has no published bound on its total cost, because the size of the tower, the degrees of the Risch differential equations and the size of the algebraic numbers in the logarithmic part are not bounded in terms of the input in a simple way.

The code solves the case $K = \mathbb{Q}(x)(t)$ with $t = \exp b$, $b \in \mathbb{Q}[x]$ of degree $m + 1 \ge 1$, and $f = \sum_k f_k t^k$ with $f_k \in \mathbb{Q}(x)$ and $k \in \mathbb{Z}$. This is the polynomial part of the exponential case, and it already contains the decisions that make the algorithm famous.

## The algorithm

The full transcendental algorithm (Bronstein, Symbolic Integration I, Chapter 5) handles $f \in K_{n-1}(t)$ for the top monomial $t$:

1. Split the denominator of $f$ into *normal* factors ($\gcd(p, p') = 1$) and *special* factors (for an exponential, the factor $t$).
2. Hermite reduction in $t$ makes the normal part of the denominator squarefree. See [Hermite reduction](/hermite-reduction/).
3. The squarefree normal part is integrated by the [Rothstein-Trager](/rothstein-trager/) resultant or the [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) variant. It is elementary only if the resultant has constant roots, which can be checked.
4. What is left is a polynomial in $t$ (logarithmic case) or a Laurent polynomial (exponential case). For a logarithm, the coefficients are integrated top-down by recursive calls in $K_{n-1}$ (the *limited integration* problem). For an exponential, each coefficient of $t^k$, $k \ne 0$, gives a *Risch differential equation* $y' + k b' y = f_k$ in $K_{n-1}$, and the coefficient of $t^0$ is integrated in $K_{n-1}$.
5. Recursion stops at $\mathbb{Q}(x)$, where integration is the [integration of rational functions](/integration-of-rational-functions/).

The code implements steps 4 and 5 for one exponential over $\mathbb{Q}(x)$:

```pseudo id=main
RISCH-EXP(b, f)                                  ▷ t = exp(b), f = Σ f_k t^k with f_k ∈ Q(x)
L1  for each k ≠ 0 with f_k ≠ 0
L2    solve the Risch differential equation y_k' + k b' y_k = f_k for y_k ∈ Q(x), by L4 and L5
L3    if it has no solution: return FAIL                  ▷ no elementary integral
L4    write f_k = a / d reduced; h ← gcd(d, d'); if d does not divide a h²: no solution, else y_k = q / h
L5    solve h q' + (k b' h − h') q = a h² / d for q ∈ Q[x] by matching leading terms; no solution if a degree goes below 0
L6  A / D ← f_0
L7  (R, A* / D*) ← HERMITE-REDUCE(A, D)                   ▷ D* squarefree
L8  return Σ y_k t^k + R + ∫ A* / D*                       ▷ the last integral is a sum of logarithms
```

Line L4 is the denominator bound. If $y$ has a pole of order $e$ at a point, $y'$ has a pole of order $e + 1$ and $k b' y$ a pole of order at most $e$, so $f_k$ has a pole of order exactly $e + 1 \ge 2$. So a simple pole of $f_k$ rules out a solution, and the denominator of $y$ is $\gcd(d, d')$. Line L5 is a degree bound and a triangular solve. The operator $q \mapsto h q' + (k b' h - h') q$ raises the degree by exactly $m + \deg h$, because $\deg(k b' h) = m + \deg h$ beats every other term, so $q$ is found from the top coefficient down, like a long division. The Rothstein-Trager step for $\int A^*/D^*$ is not repeated in the code; it is on its own page.

## Example

Take $b = x$, so $t = e^x$, and
$$f = \frac{x - 1}{x^2}\, e^x + 3 e^{-2x} + \frac{x + 1}{x^2}.$$

For $k = 1$: $f_1 = (x - 1)/x^2$, so $a = x - 1$, $d = x^2$ and $h = \gcd(x^2, 2x) = x$. The test $x^2 \mid (x - 1) x^2$ passes. Equation (L5): $x q' + (x - 1) q = x - 1$. The operator raises the degree by $1$, so $q$ has degree $0$, and matching the leading coefficient gives $q = 1$, which leaves remainder $0$. So $y_1 = 1/x$.

For $k = -2$: $f_{-2} = 3$, $h = 1$, and the equation is $q' - 2 q = 3$. The operator keeps the degree, so $q = -3/2$.

For $k = 0$: $f_0 = 1/x + 1/x^2$. Hermite reduction gives $R = -1/x$ and the remainder $1/x$, whose integral is $\log x$.

So
$$\int f\, dx = \frac{e^x}{x} - \frac{3}{2} e^{-2x} - \frac{1}{x} + \log x.$$

Now take $b = x^2$ and $f = e^{x^2}$. For $k = 1$: $a = 1$, $d = 1$, $h = 1$, and the equation is $q' + 2x q = 1$. The operator raises the degree by $1$, but the right side has degree $0$, so no $q$ exists. The algorithm returns FAIL, which proves that $\int e^{x^2} dx$ is not elementary. With $f = (2x^2 + 1) e^{x^2}$ instead, the equation $q' + 2x q = 2x^2 + 1$ has the solution $q = x$, and $\int f\, dx = x e^{x^2}$.

## Correctness

The full proof is in the proof file. When the algorithm returns an answer, differentiation gives $f$: each $y_k$ solves its equation, so $(y_k t^k)' = f_k t^k$, and Hermite reduction gives $f_0 = R' + A^*/D^*$.

When it returns FAIL, there is no elementary integral. By [Liouville's theorem](/liouville-theorem/), an elementary integral would give $f = v' + \sum_i c_i u_i'/u_i$ with $v$ and $u_i$ in $\bar{\mathbb{Q}}(x)(t)$. Every irreducible $p \ne t$ in $\bar{\mathbb{Q}}(x)[t]$ satisfies $p \nmid p'$, so $v'$ has poles of order at least $2$ wherever $v$ has a pole at such a $p$, while the logarithmic terms have only simple poles and $f$ has none. So $v$ is a Laurent polynomial in $t$, the logarithmic terms lie in $\bar{\mathbb{Q}}(x)$, and the coefficient of $t^k$ for $k \ne 0$ gives $v_k' + k b' v_k = f_k$. So a rational solution of each Risch differential equation exists. The equation has at most one solution, because $y' + k b' y = 0$ would make $y'/y$ a nonzero polynomial, and L4 and L5 find it whenever it exists.

## Complexity

Let $D$ bound the degrees of the numerators and denominators of the $f_k$, let $m + 1 = \deg b$, and let $K$ be the number of powers $t^k$. Costs are operations in $\mathbb{Q}$.

- **Each Risch differential equation.** The gcd and the division in L4 cost $O(D^2)$. The solve in L5 runs at most $\deg q + 1 = O(D)$ rounds, each costing $O(D + m)$, so $O(D (D + m))$.
- **Hermite reduction.** At most $D$ rounds of an extended Euclidean algorithm of cost $O(D^2)$, so $O(D^3)$ in this simple form. Fast methods reduce this to $O(M(D) \log D)$.
- **Total.** $O(K (D + m)^2 + D^3)$ operations in $\mathbb{Q}$, proved. The size of the rational numbers is not bounded here. In practice it stays small for the inputs in the tests.

For the general algorithm there is no comparable bound. Each level of the tower can raise the degrees of the Risch differential equations, the Rothstein-Trager resultant can need algebraic extensions of the constants, and the algebraic case needs integral bases and a test whether a divisor is of finite order on a curve. Observed running times in Axiom and Maple are acceptable for inputs that arise by hand, and can grow quickly with the height of the tower.

## Properties

- **Decision procedure.** For a transcendental elementary tower with constants in which one can compute, it is complete: FAIL is a proof.
- **Deterministic.** All steps are exact algebra.
- **Not recursive in the code.** The code handles one level; the general algorithm recurses down the tower, which an implementation can turn into a loop over levels.
- **Unique rational parts.** For an exponential, the coefficient $y_k$ of $t^k$ in the answer is unique. The logarithmic part is unique only up to the choice of the logarithms.

## Variants and improvements

- **Bronstein's algorithm.** Bronstein (1990 and the book) gave a complete version of the transcendental case, with a denominator bound for the Risch differential equation, the *parametric* Risch differential equation needed for logarithms, and a treatment of $\tan$ and other primitive monomials.
- **The algebraic case.** Risch (1970) sketched it, Davenport (1981) gave an algorithm for algebraic functions, and Trager (1984) made it practical with integral bases. Bronstein's work extended it to mixed towers. The hard part is a test whether a divisor has finite order, which is still the slowest step.
- **Lazard-Rioboo-Trager.** Avoids algebraic numbers in the logarithmic part by working with subresultants instead of factoring the resultant.
- **Risch-Norman.** The [parallel heuristic](/risch-norman-heuristic/) guesses the whole answer at once and solves one linear system. It is faster in practice but not a decision procedure.
- **Special functions.** Extensions decide integration in terms of $\mathrm{erf}$, $\mathrm{Ei}$ and other special functions. For example $\int e^{x^2} dx$ is $\frac{\sqrt{\pi}}{2}\, \mathrm{erfi}(x)$.

## When to use it

Use the Risch algorithm when you need a definite answer: an antiderivative, or a proof that none exists in elementary terms. Computer algebra systems run cheap heuristics and table lookups first and use the Risch algorithm when they fail. For rational functions, the [rational function integration](/integration-of-rational-functions/) special case is enough. For definite integrals, numerical quadrature or special function identities are usually more useful than an elementary antiderivative.

## Pitfalls

- **Building the tower.** The integrand must be rewritten so that every $t_i$ is a monomial. For example $e^x$ and $e^{2x}$ cannot both be monomials. The [structure theorem](/risch-structure-theorem/) decides this, but it needs zero tests in the constant field.
- **Constants.** The algorithm needs exact arithmetic and a zero test for constants. With transcendental constants such as $\pi$ and $e$, this is the [constant problem](/constant-problem/).
- **Branch cuts.** The answer is an antiderivative of differential fields. As a function of a real or complex variable it can jump where a logarithm crosses a branch cut, and it may need correction before it is used for definite integrals.
- **Simple poles in the Risch differential equation.** A simple pole of $f_k$ means there is no solution; forgetting this check gives wrong denominators.
- **Expression swell.** Intermediate expressions can be large even when the answer is small. Lazard-Rioboo-Trager and fraction-free methods help.

## Implementations

## History

Liouville (1833 to 1841) proved that elementary integrals have a restricted shape and used it to show that $\int e^{x^2} dx$ is not elementary. Ritt's book Integration in Finite Terms (1948) gave the algebraic form of this theory. Risch (1969) turned it into an algorithm for transcendental towers, and announced the algebraic case in 1970. Joel Moses implemented parts of it in MACSYMA in the early 1970s. Rothstein and Trager (1976 and 1977) found the resultant method for the logarithmic part, and Davenport (1981) and Trager (1984) worked out algebraic functions. Bronstein's thesis (1987), his 1990 papers and his book Symbolic Integration I (1997, second edition 2005) gave the first complete and efficient treatment of the transcendental case. Implementations exist in Axiom and FriCAS, Maple, Mathematica and, in part, SymPy.

## References
