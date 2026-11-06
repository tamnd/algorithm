---
tag: 5HBQGH
kind: technique
slug: polynomial-interpretation
name: Polynomial interpretation
aliases:
- Lankford polynomial interpretation
- polynomial ordering
area: automata-and-parsing/term-rewriting
level: advanced
summary: A termination proof method interpreting function symbols as polynomials over the naturals.
prereqs: [well-founded-reduction-ordering, termination]
see_also: [matrix-interpretation, recursive-path-ordering, lexicographic-path-ordering, knuth-bendix-ordering, dependency-pairs, hilberts-tenth-problem, variant-function, termination-proof]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 5.3, The interpretation method (p. 104 onwards; polynomial orders and Lankford's method)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 6, Termination (monotone algebras and polynomial interpretations)
  - paper: doi:10.1007/3-540-51081-8_107
    title: Dieter Hofbauer and Clemens Lautemann, Termination proofs and the length of derivations, Rewriting Techniques and Applications (RTA 1989), Lecture Notes in Computer Science 355
    locator: pp. 167 to 177 (polynomial interpretations bound derivation lengths by a double exponential)
  - paper: doi:10.1007/s10817-005-9022-x
    title: Evelyne Contejean, Claude Marché, Ana Paula Tomás and Xavier Urbain, Mechanically proving termination using polynomial interpretations, Journal of Automated Reasoning 34(4) (2005)
    locator: pp. 325 to 363
  - paper: doi:10.1007/978-3-540-72788-0_33
    title: Carsten Fuhs, Jürgen Giesl, Aart Middeldorp, Peter Schneider-Kamp, René Thiemann and Harald Zankl, SAT solving for termination analysis with polynomial interpretations, Theory and Applications of Satisfiability Testing (SAT 2007), Lecture Notes in Computer Science 4501
    locator: pp. 340 to 354
---

A **polynomial interpretation** proves that a [term rewriting system](/term-rewriting-system/) terminates by giving each function symbol a meaning as a polynomial over the natural numbers, so that every term gets a numeric value for each choice of values for its variables. If each rule makes the value smaller for every choice, then every [rewrite step](/rewrite-step/) makes it smaller, and no infinite reduction exists, because natural numbers cannot decrease forever. The method goes back to Lankford in the 1970s. It is the term analogue of a [variant function](/variant-function/) for loops, and its finite search over coefficients is what automatic termination tools run.

## In plain words

Give every operation a formula that turns the numbers of its arguments into a number, and give every constant a number. Then every expression gets a size that you can compute from its parts. Now look at each rule: if the size of the left side is always larger than the size of the right side, whatever numbers stand for the unknowns, then each rewrite makes the whole expression smaller.

A size that is a whole number and always drops cannot drop forever. So the rewriting must stop. The work is in finding formulas that make every rule drop at the same time. Simple formulas, like "one more than the sum of the arguments", work for simple rules; rules that copy parts need formulas with products or larger factors.

## When it applies

- The system is finite, and the aim is a proof of [termination](/termination/), not a decision procedure: the method proves termination of many systems but cannot refute it.
- The derivation lengths are at most doubly exponential in the size of the start term. A polynomial interpretation bounds them by a double exponential (Hofbauer and Lautemann, 1989), so it cannot prove termination of systems such as the [Ackermann function](/ackermann-function/).
- The rules do not need a non-simplifying step: a strictly monotone polynomial $P$ on natural numbers satisfies $P(\ldots, x, \ldots) \ge x$, so the method can never orient a rule whose left side embeds in its right side, such as $f(f(x)) \to f(g(f(x)))$.

## The template

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

Fix a lower bound $\mu \ge 1$ and the carrier $D = \{d \in \mathbb{N} \mid d \ge \mu\}$. An **interpretation** gives each $f \in \Sigma$ of arity $n$ a polynomial $P_f(x_1, \ldots, x_n)$ with natural coefficients that maps $D^n$ into $D$. The value $[t]_\alpha$ of a term under an assignment $\alpha : V \to D$ is $[x]_\alpha = \alpha(x)$ and $[f(t_1, \ldots, t_n)]_\alpha = P_f([t_1]_\alpha, \ldots, [t_n]_\alpha)$. Write $[t]$ for the polynomial in the variables of $t$ obtained by composing the $P_f$. The two holes are the choice of the polynomials (line L1) and the positivity test (line L3).

```pseudo id=main
POLY-TERMINATION(R)
L1  choose μ and polynomials P_f with natural coefficients, each variable x_i of P_f in a monomial with positive coefficient
L2  for each rule l → r in R do
L3      compute the polynomial d = [l] − [r] by composition
L4      if not POSITIVE(d, μ) then return "unknown"          ▷ test: d(x) > 0 for all x in D^k
L5  return "R terminates"
```

**Why it works.** Define $s > t$ iff $[s]_\alpha > [t]_\alpha$ for all $\alpha : V \to D$. This is a [reduction ordering](/well-founded-reduction-ordering/):

- It is well-founded: a descending chain $t_1 > t_2 > \cdots$ gives a descending chain of natural numbers $[t_1]_\alpha > [t_2]_\alpha > \cdots$ for any fixed $\alpha$.
- It is closed under substitutions: $[t\sigma]_\alpha = [t]_\beta$ with $\beta(x) = [x\sigma]_\alpha$, so a comparison that holds for all assignments holds for $s\sigma$ and $t\sigma$.
- It is closed under contexts: each $P_f$ is strictly increasing in each argument on $D$. A monomial $c\, x_i^k\, m$ with $c, k \ge 1$, where $m$ is a product of the other variables, is strictly increasing in $x_i$ when all variables are at least $\mu \ge 1$, and the other monomials do not decrease.

Line L4 checks $l > r$ for every rule, so $R$ is compatible with a reduction ordering and terminates. For a ground term $t$, each step lowers $[t]$ by at least 1 and $[t] \ge \mu$, so the derivation height of $t$ is at most $[t] - \mu$.

**The positivity test.** Whether a polynomial with integer coefficients is positive on all of $\mathbb{N}^k$ is undecidable: a Diophantine equation $E(x) = 0$ has no solution in natural numbers iff $E(x)^2 > 0$ for all $x$, and that is [Hilbert's tenth problem](/hilberts-tenth-problem/). So POSITIVE is a sound but incomplete test. The standard one is **absolute positiveness**: substitute $x_i = y_i + \mu$, expand, and accept if every coefficient is non-negative and the constant term is positive. Then the value is positive for all $y_i \ge 0$.

**Searching for the interpretation.** Tools fix a shape, for example linear polynomials $a_0 + a_1 x_1 + \cdots + a_n x_n$ or products of degree 2, with unknown coefficients in a small range. Absolute positiveness of $[l] - [r]$ becomes a set of polynomial constraints on the coefficients. These constraints are solved by search, or encoded into SAT (Fuhs and others, 2007); Contejean, Marché, Tomás and Urbain (2005) give a method based on constraint solving over finite domains.

## Classic examples

All comparisons below were computed by a program that composes the polynomials, applies the shift $x_i = y_i + \mu$, and also compares the values on a grid of assignments.

**Addition and multiplication.** Take $\mu = 1$ and $[0] = 1$, $[s](x) = x + 1$, $[+](x, y) = 2x + y$, $[\times](x, y) = 3xy$. The differences $[l] - [r]$ are:

| rule | $[l] - [r]$ |
| --- | --- |
| $0 + y \to y$ | $2$ |
| $s(x) + y \to s(x + y)$ | $1$ |
| $x \times 0 \to 0$ | $3x - 1$ |
| $x \times s(y) \to x + (x \times y)$ | $x$ |
| $(x + y) + z \to x + (y + z)$ | $2x$ |

All are positive for $x, y, z \ge 1$, so the five rules together terminate. The factor 2 in $[+]$ makes the first argument weigh more than the second, which is what the second and fifth rules need.

**The choice of $\mu$ matters.** For distributivity $x \times (y + z) \to (x \times y) + (x \times z)$ with $[+](x, y) = x + y + 1$ and $[\times](x, y) = xy$, the difference is $x(y + z + 1) - (xy + xz + 1) = x - 1$. It is zero at $x = 1$, so the proof fails for $\mu = 1$ and succeeds for $\mu = 2$.

**A size measure.** The interpretation $P_f(x_1, \ldots, x_n) = x_1 + \cdots + x_n + 1$ with $\mu = 1$ gives $[t] = |t|$ for ground terms, the number of symbols. It proves termination of every non-duplicating system whose rules shrink the size, such as $f(x, a) \to x$, and it gives linear derivation height.

**A failure.** For $f(f(x)) \to f(g(f(x)))$, any strictly increasing $P_g$ on $D$ has $P_g(y) \ge y$, so $[f(g(f(x)))] = P_f(P_g(P_f(x))) \ge P_f(P_f(x))$. No polynomial interpretation proves this terminating system. The [dependency pair](/dependency-pairs/) method with a weakly monotone interpretation does.

## Variations

- **Weakly monotone interpretations in reduction pairs.** In the [dependency pair](/dependency-pairs/) framework, the polynomials need only be weakly increasing, coefficients may be zero, and some rules need only $[l] \ge [r]$. This makes the method much stronger.
- **Matrix interpretations.** Interpret symbols as affine maps on vectors of natural numbers, compared in the first coordinate. See [matrix interpretation](/matrix-interpretation/).
- **Rational and real coefficients.** Interpretations into the non-negative rationals or reals, with $s > t$ meaning a decrease by at least a fixed $\delta > 0$, prove some systems that natural coefficients cannot.
- **Max-polynomials.** Allow the maximum function next to sums and products, which models symbols that pass on their largest argument.
- **Complexity analysis.** Restricted shapes bound the derivational complexity: strongly linear interpretations ($x_1 + \cdots + x_n + c$) give linear bounds, and the shape of the polynomials gives polynomial bounds on innermost runtime.

## Pitfalls

- **Forgetting strict monotonicity.** $[\times](x, y) = xy$ is strictly increasing only if the carrier excludes 0. With $\mu = 0$, $0 \cdot y$ does not grow with $y$, and closure under contexts fails.
- **A variable missing from $P_f$.** If $P_f$ does not depend on $x_i$, a step inside argument $i$ does not change the value, and the order is not monotone. Such interpretations are allowed only in reduction pairs.
- **Testing positivity on a few points.** Checking $[l] > [r]$ on a grid does not prove it for all values; use absolute positiveness or another sound test.
- **Duplicating rules with additive interpretations.** For $f(x) \to g(x, x)$, a linear $[g]$ counts $x$ twice; the coefficients of $[f]$ must be large enough to pay for both copies.
- **Treating failure as non-termination.** A failed search only shows that no interpretation of the chosen shape exists.

## Exercises

1. Show that $[f](x) = x^2$, $[g](x) = x + 1$ with $\mu = 2$ proves termination of $f(g(x)) \to g(g(f(x)))$.
2. Prove that a strictly increasing function $P : D \to D$ satisfies $P(y) \ge y$ for all $y \in D$.
3. Find a polynomial interpretation for $x \times s(y) \to (x \times y) + x$ together with $0 + y \to y$ and $s(x) + y \to s(x + y)$, or explain why the shape $[+](x, y) = a x + b y + c$ with $a \ge 2$ cannot work.
4. Show that for ground terms the derivation height under a terminating system proved by $P_f = x_1 + \cdots + x_n + 1$ is less than the size of the term.

## References
