---
tag: M8QSZ7
kind: algorithm
slug: petkovsek-hyper-algorithm
name: Petkovšek's Hyper algorithm
aliases:
- Hyper
- Petkovšek's algorithm
- algorithm Hyper
area: algebra/computer-algebra
level: research
summary: Finds all hypergeometric solutions of linear recurrences with polynomial coefficients.
solves: [definite-summation]
model: blum-shub-smale-machine
complexity:
  vars: {r: the order of the recurrence, d: the largest degree of a coefficient, d_0: the degree of p_0, d_r: the degree of p_r, D: the largest degree bound met for polynomial solutions}
  time: {worst: O(2^(d_0 + d_r) r (r d + D)^3)}
  space: {extra: O((r d + D)^2)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1992
  people: [Marko Petkovšek]
  note: Petkovšek published Hyper in 1992, building on Gosper's 1978 normal form and on Abramov's algorithms for polynomial and rational solutions; van Hoeij gave a faster method in 1999.
prereqs: [hypergeometric-term, recurrence-relation, gosper-algorithm, polynomial-factorization]
see_also: [holonomic-function, ore-algebra, zeilberger-algorithm, creative-telescoping, indefinite-summation, wz-method, linear-recurrences-with-constant-coefficients, kovacic-algorithm]
sources:
  - paper: "Marko Petkovšek, Hypergeometric solutions of linear recurrences with polynomial coefficients, Journal of Symbolic Computation 14(2-3), 1992"
    locator: the algorithm Hyper, the divisibility conditions on a and b, the equation for Z, and the proof of completeness
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 8, Algorithm Hyper (the statement, worked examples, and the use of Hyper after Zeilberger's algorithm to decide closed forms of definite sums) and Chapter 5 (the Gosper-Petkovšek form of a rational function)
  - paper: "Sergei A. Abramov, Manuel Bronstein and Marko Petkovšek, On polynomial solutions of linear operator equations, ISSAC 1995"
    locator: degree bounds and algorithms for polynomial solutions of linear recurrences
  - paper: "Mark van Hoeij, Finite singularities and hypergeometric solutions of linear recurrence equations, Journal of Pure and Applied Algebra 139, 1999"
    locator: the method that avoids the exponential search over pairs of factors
---

Petkovšek's algorithm Hyper finds every hypergeometric solution of a linear recurrence $\sum_{i=0}^{r} p_i(n)\, t(n + i) = 0$ with polynomial coefficients. A hypergeometric solution is one whose ratio $t(n + 1)/t(n)$ is a rational function of $n$, such as $2^n$, $n!$ or $\binom{2n}{n}$. Hyper writes the unknown ratio in Gosper-Petkovšek form $Z \frac{a(n)}{b(n)} \frac{c(n + 1)}{c(n)}$, and shows that $a$ must divide $p_0(n)$ and $b$ must divide $p_r(n - r + 1)$. It tries each such pair of monic factors. For each pair, $Z$ is a root of a polynomial of degree at most $r$ read off from leading coefficients, and $c$ is a polynomial solution of a derived recurrence. The search is finite and complete, but the number of pairs is exponential in the degrees of $p_0$ and $p_r$. Hyper is the last step that turns a recurrence from [Zeilberger's algorithm](/zeilberger-algorithm/) into a closed form, or proves that none exists.

## In plain words

You have a recurrence, such as one produced by an automatic summation method, and you want to know whether it has a solution as simple as a power, a factorial or a binomial coefficient. All such solutions grow by a rational factor from one term to the next. The algorithm guesses the shape of this factor in three parts. The top and bottom parts must come from factors of the first and last coefficients of the recurrence, so there are only finitely many guesses. For each guess, a constant comes from a small polynomial equation, and a last polynomial part comes from solving linear equations. Every surviving guess is a solution, and every solution is found this way.

## The problem

Notation: $K$ is a field of characteristic $0$, here $\mathbb{Q}$, and $K[n]$ is the polynomial ring in the index $n$. The input is $p_0, \ldots, p_r \in K[n]$ with $r \ge 1$, $p_0 \ne 0$ and $p_r \ne 0$, which define the operator $L = \sum p_i(n) S^i$ in the [Ore algebra](/ore-algebra/) of shift operators, $(S t)(n) = t(n + 1)$. A [hypergeometric term](/hypergeometric-term/) $t$ solves $L$ if $\sum_i p_i(n)\, t(n + i) = 0$ for all large $n$. The output is a finite list of ratios $R_j \in K(n)$ such that each $R_j$ is the ratio of a solution, and every hypergeometric solution with ratio in $K(n)$ is a linear combination of solutions with ratios in the list. Solutions whose ratio needs an algebraic extension, like $\varphi^n$ for the Fibonacci recurrence, are found by running the same algorithm over the extension.

## The algorithm

```pseudo id=main
HYPER(p_0, ..., p_r)
L1  S ← empty list
L2  for each monic factor a of p_0(n) and each monic factor b of p_r(n − r + 1) do
L3      P_i ← p_i(n) · a(n) a(n+1) ··· a(n+i−1) · b(n+i) ··· b(n+r−1)   for i = 0, ..., r
L4      m ← max_i deg P_i;  α_i ← the coefficient of n^m in P_i
L5      for each nonzero root Z of α_0 + α_1 Z + ··· + α_r Z^r do
L6          C ← a basis of the polynomial solutions c of Σ_i Z^i P_i(n) c(n + i) = 0
L7          for each c in C: append Z · a(n)/b(n) · c(n+1)/c(n), in lowest terms, to S
L8  return S
```

Line L3 multiplies the recurrence through by $b(n) \cdots b(n + r - 1)$ after the substitution of the ratio, so it is a polynomial identity. Line L5 is the condition that the leading terms cancel. Line L6 needs a degree bound. Write $\sum_i Q_i(n) E^i = \sum_k R_k(n) \Delta^k$ with $E = 1 + \Delta$, so $R_k = \sum_{i \ge k} \binom{i}{k} Q_i$, and let $b^\ast = \max_k (\deg R_k - k)$. A solution $c$ of degree $\delta$ makes the coefficient of $n^{b^\ast + \delta}$ equal to $\operatorname{lc}(c)\, \varphi(\delta)$ with $\varphi(\delta) = \sum_{\deg R_k - k = b^\ast} \operatorname{lc}(R_k)\, \delta (\delta - 1) \cdots (\delta - k + 1)$. So $\delta$ is a nonnegative integer root of $\varphi$, and the largest such root $D$ bounds the degree. The coefficients of $c$ then solve a linear system with $D + 1$ unknowns.

## Example

Take $(n - 1)\, t(n + 2) - (n^2 + 3n - 2)\, t(n + 1) + 2n(n + 1)\, t(n) = 0$, so $p_0 = 2n(n + 1)$, $p_1 = -(n^2 + 3n - 2)$ and $p_2 = n - 1$. The monic factors of $p_0$ are $1, n, n + 1, n(n + 1)$, and $p_2(n - 1) = n - 2$ has the monic factors $1, n - 2$. The eight pairs give:

| $a$ | $b$ | $\sum \alpha_i Z^i$ | $Z$ | basis of $c$ | ratio |
|---|---|---|---|---|---|
| $1$ | $1$ | $2 - Z$ | $2$ | $1$ | $2$ |
| $1$ | $n - 2$ | $2$ | none | | |
| $n$ | $1$ | $Z^2 - Z$ | $1$ | $n$ | $n + 1$ |
| $n$ | $n - 2$ | $2 - Z$ | $2$ | none | |
| $n + 1$ | $1$ | $Z^2 - Z$ | $1$ | $1$ | $n + 1$ |
| $n + 1$ | $n - 2$ | $2 - Z$ | $2$ | none | |
| $n(n + 1)$ | $1$ | $Z^2$ | none | | |
| $n(n + 1)$ | $n - 2$ | $Z^2 - Z$ | $1$ | none | |

For the first pair, $P_i = p_i$ and the coefficients of $n^2$ are $2, -1, 0$, so $Z = 2$, and $c = 1$ solves $4(n - 1) c(n + 2) - 2(n^2 + 3n - 2) c(n + 1) + 2n(n + 1) c(n) = 0$. The output is the two ratios $2$ and $n + 1$, that is, the solutions $2^n$ and $n!$, and every hypergeometric solution is a combination of them. The ratio $n + 1$ is found twice, by different pairs, and kept once. The implementation reproduces this table.

## Correctness

Each output is a solution: substituting $t(n + i) = t(n)\, Z^i \prod_{j < i} \frac{a(n + j)}{b(n + j)} \frac{c(n + i)}{c(n)}$ into $L t$ and multiplying by $c(n) \prod_{j < r} b(n + j) / t(n)$ gives exactly $\sum_i Z^i P_i(n)\, c(n + i)$, which line L6 makes zero. Conversely, let $t$ be a solution with ratio in Gosper-Petkovšek form. In that same identity, every term with $i \ge 1$ contains the factor $a(n)$, and the coprimality conditions of the form then force $a(n) \mid p_0(n)$. Every term with $i < r$ contains $b(n + r - 1)$, which forces $b(n + r - 1) \mid p_r(n)$. The leading coefficient of the identity is $\operatorname{lc}(c) \sum_i \alpha_i Z^i$, so $Z$ is found at line L5, and $c$ is in the span of the basis of line L6. So $t$ is a combination of output solutions. The proof file gives the details, with the degree bound for line L6.

## Complexity

The cost model counts operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $\mathbb{Q}$. Factoring $p_0$ and $p_r$ and finding the roots $Z$ are separate costs, done once per input and once per pair. These bounds are proved:

- **Pairs.** If $p_0$ and $p_r$ split into $d_0$ and $d_r$ linear factors, there are at most $2^{d_0 + d_r}$ pairs, with equality when the factors are distinct.
- **One pair.** The $P_i$ have degree at most $d + r(d_0 + d_r) \le d + 2rd$. Line L6 builds a matrix with at most $D + 1$ columns and $O(rd + D)$ rows and reduces it in $O((rd + D)^3)$ operations, which dominates. In total, $O(2^{d_0 + d_r}\, r\, (rd + D)^3)$, with the factor $r$ covering up to $r$ roots $Z$.

The bound $D$ is not polynomial in the input size: $n\, c(n + 1) - (n + k)\, c(n) = 0$ has the polynomial solution $c(n) = n(n + 1) \cdots (n + k - 1)$ of degree $k$, from coefficients of size $\log k$. The exponential number of pairs is the real bottleneck in practice, which is an observation from implementations, and most pairs fail. On the random tests of the implementation, the planted solutions are always found, and most pairs have no root $Z$ or no polynomial $c$.

## Properties

- **Complete over the coefficient field.** Every hypergeometric solution with ratio in $K(n)$ is a combination of the returned ones, as long as $p_0$ and $p_r$ are factored completely over $K$ and all roots $Z \in K$ are used.
- **Deterministic and exact.** No randomness, and all arithmetic is in $K$.
- **Output up to similarity.** Several pairs can give the same ratio, and similar solutions such as $1$ and $n$ for $(S - 1)^2$ appear as separate ratios $1$ and $(n + 1)/n$.
- **Decides closed forms.** Applied to the recurrence from [creative telescoping](/creative-telescoping/), Hyper decides whether a definite hypergeometric sum is a linear combination of hypergeometric terms, since the minimal recurrence is found and all its hypergeometric solutions are listed.

## Variants and improvements

- **van Hoeij's algorithm (1999).** It uses the local behaviour at finite singularities to choose $a$ and $b$ together, which avoids the exponential search in most cases, and is the method in current computer algebra systems.
- **Factoring the operator.** Repeating Hyper on the left quotient after dividing out a found right factor $b(n) S - Z a(n) \cdots$ gives all solutions that are sums of products of hypergeometric terms, the d'Alembertian solutions (Abramov and Petkovšek).
- **Rational and polynomial solutions.** Abramov's algorithms find rational solutions, the case $Z = 1$ with $a = b = 1$ after a denominator bound, and the method of line L6 finds polynomial ones.
- **$q$-analogue.** qHyper solves linear $q$-recurrences in the same way, with $q$-shifts in place of shifts.
- **Differential analogue.** For linear differential equations, the analogue finds exponential solutions $\exp(\int R)$, and [Kovacic's algorithm](/kovacic-algorithm/) goes further for order $2$.

## When to use it

Use it to decide whether a linear recurrence with polynomial coefficients has solutions in closed form: after Zeilberger's algorithm, to evaluate a definite sum or prove that it has no hypergeometric closed form; to solve recurrences from the analysis of algorithms; or to find right factors of order $1$ of a recurrence operator. For recurrences with constant coefficients, the [characteristic polynomial](/linear-recurrences-with-constant-coefficients/) is simpler. For coefficients of high degree with many rational roots, prefer van Hoeij's method.

## Pitfalls

- **Shifted leading coefficient.** $b$ ranges over the factors of $p_r(n - r + 1)$, not of $p_r(n)$. Using $p_r(n)$ misses solutions.
- **Incomplete factorization.** Over $\mathbb{Q}$, solutions such as $\varphi^n$ need the roots $Z$ in an extension. Hyper over $\mathbb{Q}$ only finds ratios in $\mathbb{Q}(n)$, and completeness needs the full factorization of $p_0$ and $p_r$.
- **Large degree bounds.** The bound $D$ can be huge, as in the example above, which makes the linear system of line L6 large even for small inputs.
- **Zeros of the solution.** A hypergeometric term may vanish or be undefined at small $n$, where the ratio has roots or poles. Initial values must be chosen beyond the integer roots of $p_r(n - r + 1)$ and of the ratio.
- **Duplicates.** Different pairs often give the same ratio or similar ratios. Reduce each ratio to lowest terms before comparing.

## Implementations

## History

Gosper's 1978 algorithm for indefinite summation introduced the normal form of the ratio that Hyper uses, and Abramov in 1989 gave algorithms for the rational solutions of linear recurrences. Petkovšek published Hyper in 1992, as the first algorithm to find all hypergeometric solutions, and with Wilf and Zeilberger made it a central part of the book A = B (1996), where it completes Zeilberger's method for definite sums. Van Hoeij's 1999 algorithm removed most of the combinatorial search.

## References
