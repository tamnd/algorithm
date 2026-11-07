---
tag: 8BTTVF
kind: algorithm
slug: multivariate-division-algorithm
name: Multivariate division algorithm
aliases:
- normal form reduction
- multivariate polynomial division
- division with remainder in several variables
- reduction modulo a set of polynomials
area: algebra/computer-algebra
level: core
summary: Reduces a polynomial modulo a set of polynomials to a remainder that is unique given a Gröbner basis.
solves: [ideal-membership-problem]
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of variables, s: the number of divisors, D: the total degree of f, T: the largest number of terms of a divisor, N: the number of passes of the main loop}
  time: {worst: O(N (s n + T))}
  space: {extra: O(N n + T n)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1965
  people: [Bruno Buchberger]
  note: Buchberger's 1965 thesis reduces polynomials modulo a set of polynomials, the step that this algorithm performs; the form with an ordered list of divisors and a remainder is the one of Cox, Little and O'Shea.
prereqs: [monomial-ordering, leading-term, polynomial-long-division]
see_also: [groebner-basis, buchberger-algorithm, s-polynomial, ideal-membership-problem, reduced-groebner-basis, pseudo-division]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 3 (the division algorithm in k[x_1, ..., x_n], Theorem 3, with the examples whose remainder depends on the order of the divisors) and Section 6 (unique remainders for a Gröbner basis)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Section 21.2 (multivariate division with remainder)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 10 (reduction of a polynomial modulo a set of polynomials and normal forms)
  - paper: doi:10.1016/j.jsc.2005.09.007
    title: Bruno Buchberger, An algorithm for finding the basis elements of the residue class ring of a zero dimensional polynomial ideal (English translation of the 1965 PhD thesis), Journal of Symbolic Computation 41(3-4), 475-511, 2006
    locator: the reduction of a polynomial modulo a set of polynomials
---

The multivariate division algorithm divides a polynomial $f$ in $K[x_1, \ldots, x_n]$ by an ordered list of polynomials $f_1, \ldots, f_s$, for a fixed [monomial order](/monomial-ordering/). It returns quotients $q_1, \ldots, q_s$ and a remainder $r$ with $f = q_1 f_1 + \cdots + q_s f_s + r$, where no term of $r$ is divisible by any [leading term](/leading-term/) $\operatorname{LT}(f_i)$. It generalizes [polynomial long division](/polynomial-long-division/) to several variables and several divisors. In general the remainder depends on the order of the divisors, but when the divisors form a [Gröbner basis](/groebner-basis/) it is unique, and it is zero exactly when $f$ lies in the ideal.

## In plain words

In one variable you divide by cancelling the highest term again and again. With several variables you first fix a rule that says which term of a polynomial counts as the largest. Then you look at the largest term of what is left. If the largest term of some divisor divides it, you subtract the right multiple of that divisor, which removes the term. If no divisor fits, you move the term to the remainder and go on with the rest. Each step makes the largest remaining term smaller, so the process ends. The remainder you get can depend on the order in which you try the divisors, unless the divisors are a Gröbner basis.

## The problem

**Input.** A field $K$, a [monomial order](/monomial-ordering/) $>$ (lex, grlex or grevlex), a polynomial $f \in K[x_1, \ldots, x_n]$, and an ordered list $F = (f_1, \ldots, f_s)$ of nonzero polynomials.

**Output.** Polynomials $q_1, \ldots, q_s, r$ such that

1. $f = q_1 f_1 + \cdots + q_s f_s + r$;
2. $r = 0$, or no term of $r$ is divisible by any of $\operatorname{LT}(f_1), \ldots, \operatorname{LT}(f_s)$;
3. if $q_i f_i \ne 0$, then $\operatorname{LM}(q_i f_i) \le \operatorname{LM}(f)$.

The output is not unique in general. The algorithm below fixes one output by trying the divisors in the given order. The remainder is written $\overline{f}^F$.

## The algorithm

The working polynomial $p$ starts as $f$. At each pass the leading term of $p$ is cancelled by the first divisor that can, or moved to the remainder.

```pseudo id=main
DIVIDE(f, f_1, ..., f_s)                     ▷ a monomial order > is fixed
L1  q_1, ..., q_s ← 0;  r ← 0;  p ← f
L2  while p ≠ 0 do
L3      i ← 1
L4      while i ≤ s and no division occurred in this pass do
L5          if LT(f_i) divides LT(p) then
L6              q_i ← q_i + LT(p) / LT(f_i)
L7              p ← p − (LT(p) / LT(f_i)) · f_i      ▷ cancels LT(p)
L8              a division occurred in this pass
L9          else i ← i + 1
L10     if no division occurred in this pass then
L11         r ← r + LT(p)
L12         p ← p − LT(p)
L13 return (q_1, ..., q_s), r
```

Line L7 subtracts a term multiple of $f_i$ whose leading term equals $\operatorname{LT}(p)$, so the leading term of $p$ cancels and every new term is smaller than the old $\operatorname{LT}(p)$. Lines L11 and L12 move a term that no $\operatorname{LT}(f_i)$ divides to the remainder. Moving it, and not stopping, is what makes this a full division: the algorithm goes on to reduce the smaller terms of $p$ too.

## Example

Divide $f = x^2 y + x y^2 + y^2$ by $f_1 = xy - 1$ and $f_2 = y^2 - 1$ in $\mathbb{Q}[x, y]$, with lex and $x > y$. This is the example of Cox, Little and O'Shea, Chapter 2, Section 3. Here $\operatorname{LT}(f_1) = xy$ and $\operatorname{LT}(f_2) = y^2$.

| pass | $\operatorname{LT}(p)$ | action | $p$ after the pass | $q_1$ | $q_2$ | $r$ |
|---|---|---|---|---|---|---|
| 1 | $x^2 y$ | $xy$ divides it: subtract $x f_1$ | $x y^2 + x + y^2$ | $x$ | $0$ | $0$ |
| 2 | $x y^2$ | $xy$ divides it: subtract $y f_1$ | $x + y^2 + y$ | $x + y$ | $0$ | $0$ |
| 3 | $x$ | neither divides it: move to $r$ | $y^2 + y$ | $x + y$ | $0$ | $x$ |
| 4 | $y^2$ | $xy$ does not, $y^2$ does: subtract $f_2$ | $y + 1$ | $x + y$ | $1$ | $x$ |
| 5 | $y$ | move to $r$ | $1$ | $x + y$ | $1$ | $x + y$ |
| 6 | $1$ | move to $r$ | $0$ | $x + y$ | $1$ | $x + y + 1$ |

So $x^2 y + x y^2 + y^2 = (x + y)(xy - 1) + 1 \cdot (y^2 - 1) + (x + y + 1)$. The same answer comes out under grlex and grevlex. With the divisors in the other order, $(f_2, f_1)$, the result is $q = (x + 1, x)$ and $r = 2x + 1$: a different remainder.

## Correctness

The algorithm keeps the invariant

$$f = q_1 f_1 + \cdots + q_s f_s + p + r,$$

no term of $r$ is divisible by any $\operatorname{LT}(f_i)$, and each $q_i f_i$ and $p$ has all its monomials at most $\operatorname{LM}(f)$. Each pass of line L2 makes $\operatorname{LM}(p)$ strictly smaller, and a monomial order is a well-order, so the loop stops. At the end $p = 0$, and the invariant is the output specification. The full proof, with the termination argument, is in the proof file below.

## Complexity

The cost model counts field operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $K$, and separately the integer operations on exponent vectors. Over $\mathbb{Q}$ the bit cost also depends on the growth of the coefficients, which this count does not bound. Let $N$ be the number of passes of line L2 and $T$ the largest number of terms of a divisor.

- **One pass.** At most $s$ divisibility tests, each $O(n)$ exponent comparisons (line L5). If a division occurs, line L7 costs one field division and at most $T$ multiplications and $T$ additions. So a pass costs $O(sn + T)$, plus the cost of finding $\operatorname{LT}(p)$, which depends on the data structure (a heap gives $O(\log |p|)$ monomial comparisons).
- **The number of passes.** Each pass adds one term to some $q_i$ or to $r$, so these have at most $N$ terms in total. For a graded order (grlex, grevlex), each monomial of $p$ has total degree at most $D = \deg f$: line L7 adds monomials $x^\gamma m'$ with $m' \le \operatorname{LM}(f_i)$, hence $\deg m' \le \deg \operatorname{LM}(f_i)$ and $\deg(x^\gamma m') \le \deg \operatorname{LM}(p) \le D$. The leading monomials of $p$ in successive passes are distinct monomials of degree at most $D$, so $N \le \binom{n + D}{n}$. This bound is proved.
- **Lex.** For lex there is no bound in terms of $n$ and $D$ alone. Divide $f = x_1$ by $x_1 - x_2^b, x_2 - x_3^b, \ldots, x_{n-1} - x_n^b$: the remainder is $x_n^{b^{n-1}}$, and there are $1 + (b^{n-1} - 1)/(b - 1)$ passes. For $b = 3$ and $n = 4$ that is $14$ passes and the remainder $x_4^{27}$, from inputs of degree at most $3$.

The total is $O(N(sn + T))$ field and exponent operations in the worst case, and the extra space is $O((N + T) n)$ for the terms of the quotients, the remainder and $p$. In practice $N$ is far below the graded bound for sparse inputs. This is an observation, not a theorem.

## Properties

- **Not canonical in general.** The remainder depends on the order of the divisors and on the choice at line L4, as in the example.
- **Canonical for a Gröbner basis.** If $\{f_1, \ldots, f_s\}$ is a Gröbner basis of $I = \langle f_1, \ldots, f_s \rangle$, the remainder is the same for each order of the divisors and each choice of divisor, and $\overline{f}^F = 0$ exactly when $f \in I$ (Cox, Little and O'Shea, Chapter 2, Section 6).
- **One variable, one divisor.** With $n = 1$ and $s = 1$ the algorithm is [polynomial long division](/polynomial-long-division/), and the remainder is the usual one.

## Variants and improvements

- **Top reduction.** Stop as soon as no $\operatorname{LT}(f_i)$ divides $\operatorname{LT}(p)$, and return $p$. This is enough to test whether a remainder is zero, and it is the step used in many [Buchberger](/buchberger-algorithm/) implementations; a full reduction follows only at the end.
- **Choice of divisor.** Any divisor whose leading term divides $\operatorname{LT}(p)$ can be used at line L5. Gröbner basis software often picks the one with the fewest terms or the smallest degree. The output still meets the specification.
- **Fraction-free division.** Over a ring such as $\mathbb{Z}$, multiply $p$ by $\operatorname{LC}(f_i)$ before the subtraction instead of dividing by it, as in [pseudo-division](/pseudo-division/). The result satisfies $c f = \sum q_i f_i + r$ for a product $c$ of leading coefficients.
- **Data structures for $p$.** A heap of the pending terms, or a geobucket, finds $\operatorname{LT}(p)$ quickly and delays the additions. Both are standard in fast sparse division.
- **Linear algebra.** The [F4 algorithm](/f4-algorithm/) performs many reductions at once as Gaussian elimination on a [Macaulay matrix](/macaulay-matrix/).

## When to use it

Use it to compute normal forms modulo a Gröbner basis: membership tests, arithmetic in the quotient ring $K[x_1, \ldots, x_n]/I$, and the reduction of [S-polynomials](/s-polynomial/) in Buchberger's algorithm. Without a Gröbner basis a nonzero remainder does not prove that $f \notin I$, so the algorithm alone does not decide membership. For one variable use long division or [fast division](/fast-polynomial-division/) by Newton iteration, which costs $O(M(d))$ field operations.

## Pitfalls

- **A nonzero remainder does not show non-membership.** Divide $f = xy^2 - x$ by $(xy + 1, y^2 - 1)$ under lex: the remainder is $-x - y$. Yet $f = x (y^2 - 1)$ is in the ideal, and with the divisors in the order $(y^2 - 1, xy + 1)$ the remainder is $0$. Compute a Gröbner basis first.
- **Stopping at the first term that does not divide.** If line L10 returns $p$ instead of moving $\operatorname{LT}(p)$ to $r$ (lines L11 and L12), the smaller terms of $p$ are never reduced, and condition 2 of the output fails.
- **Comparing by total degree under lex.** Line L5 and the choice of $\operatorname{LT}(p)$ must use the same order as the leading terms of the divisors. Mixing the orders breaks the invariant that $\operatorname{LM}(p)$ drops, and the loop may not stop.
- **A zero divisor in the list.** $\operatorname{LT}(0)$ is not defined. Remove zero polynomials before the call.
- **Degree growth under lex.** As in the chain example, the remainder can have degree exponential in $n$ under lex. Use a graded order when you only need a canonical form.

## Implementations

## History

Buchberger's 1965 thesis reduces a polynomial modulo a finite set of polynomials by cancelling leading terms, and uses this reduction to define his algorithm for Gröbner bases. The form with an ordered list of divisors, explicit quotients and a remainder whose terms are not divisible by any leading term is Theorem 3 of Cox, Little and O'Shea, Chapter 2, Section 3.

## References
