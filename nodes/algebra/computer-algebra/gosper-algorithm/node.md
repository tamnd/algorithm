---
tag: CAVQHD
kind: algorithm
slug: gosper-algorithm
name: Gosper's algorithm
aliases:
- Gosper's indefinite summation
- Gosper's decision procedure
- indefinite hypergeometric summation
area: algebra/computer-algebra
level: advanced
summary: Decides whether a hypergeometric term has a hypergeometric antidifference and finds it when it does.
model: blum-shub-smale-machine
complexity:
  vars: {d: the larger degree of the numerator and denominator of the ratio, H: the bound on integer root differences, D: the degree bound for the polynomial x}
  time: {worst: O(H d^2 + (d + D)^3), best: O(d^2)}
  space: {extra: O((d + D)^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [hypergeometric-term, indefinite-summation, polynomial-gcd]
see_also: [zeilberger-algorithm, creative-telescoping, definite-summation, wz-method, petkovsek-hyper-algorithm, telescoping-sum, hermite-reduction, resultant]
sources:
  - paper: doi:10.1073/pnas.75.1.40
    title: R. William Gosper, Jr., Decision procedure for indefinite hypergeometric summation, Proceedings of the National Academy of Sciences USA 75(1), 40-42, 1978
    locator: the reduction to a polynomial equation, the factorization of the ratio and the degree bound
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 5 (Gosper's algorithm, the Gosper-Petkovšek form, the degree bound and the proof that the method is a decision procedure)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 23.4 (Gosper's algorithm), with the dispersion and the cost analysis in Chapter 23
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 5.7 (partial hypergeometric sums, Gosper's algorithm with worked examples)
---

Gosper's algorithm decides whether a sum $\sum_{k=0}^{n-1} t(k)$ of a hypergeometric term $t$ can be written as $z(n) - z(0)$ for another hypergeometric term $z$, and finds $z$ when it can. A term is hypergeometric when the ratio $t(k+1)/t(k)$ is a rational function of $k$, as for binomial coefficients, factorials and powers. The algorithm turns the question into a linear equation for an unknown polynomial: it factors the ratio into a special form, bounds the degree of the unknown polynomial, and solves a linear system. It is the discrete analogue of the rational part of integration, it was the first complete decision procedure in symbolic summation (Gosper 1978), and it is the inner step of Zeilberger's algorithm for definite sums.

## In plain words

Some sums have a short formula for their running total. Adding up $1 + 2 + \cdots + n$ gives $n(n+1)/2$, and adding up $k \cdot k!$ for $k$ from 0 to $n - 1$ gives $n! - 1$. Other sums, like $1 + 1/2 + 1/3 + \cdots$, have no such formula.

Gosper's method answers the question for a large family of sums, those where each term is a fixed fraction of the previous one. It guesses that the running total is the term itself times an unknown fraction. It then finds out what the bottom of that fraction must be, how large its top can be, and solves for the top with ordinary linear equations. If no top works, the method proves that no short formula of this kind exists.

## The problem

Let $K = \mathbb{Q}$, or any field of characteristic 0, and $K[n]$ the polynomials in one variable; no monomial order is needed in one variable, and $\operatorname{LC}(p)$ is the leading coefficient of $p$. A *hypergeometric term* is a nonzero function $t$ on the integers (from some point on) with

$$\frac{t(n+1)}{t(n)} = r(n) = \frac{\mathrm{num}(n)}{\mathrm{den}(n)}, \qquad \mathrm{num}, \mathrm{den} \in K[n] \setminus \{0\}.$$

**Input:** the polynomials $\mathrm{num}$ and $\mathrm{den}$.

**Output:** a rational function $y \in K(n)$ such that $z = y t$ satisfies $z(n+1) - z(n) = t(n)$, or the answer that no hypergeometric $z$ with this property exists.

Then $\sum_{k=a}^{b-1} t(k) = z(b) - z(a)$ wherever $t$ and $y$ are defined. The cost is counted in operations in $K$ on the [BSS model](/blum-shub-smale-machine/), with $d = \max(\deg \mathrm{num}, \deg \mathrm{den})$; polynomial multiplication of degree $d$ costs $M(d) = O(d^2)$ classically.

## The algorithm

The algorithm rewrites the ratio in the *Gosper form* (also called the Gosper-Petkovšek form)

$$r(n) = \frac{a(n)}{b(n)} \cdot \frac{c(n+1)}{c(n)}, \qquad \gcd(a(n), b(n+h)) = 1 \text{ for all integers } h \ge 0,$$

then solves the polynomial equation $a(n)\,x(n+1) - b(n-1)\,x(n) = c(n)$.

```pseudo id=main
GOSPER(num, den)                        ▷ r(n) = t(n+1)/t(n) = num/den
L1  a ← (LC(num)/LC(den)) · monic(num); b ← monic(den); c ← 1
L2  for h = 0, 1, ..., H do                       ▷ H bounds the integer root differences
L3      while g ← gcd(a(n), b(n+h)) is not constant do
L4          a ← a/g; b ← b/g(n−h); c ← c · g(n−1) g(n−2) ⋯ g(n−h)
L5  B(n) ← b(n−1); D ← degree bound for x from a, B and c
L6  if D < 0 then return NONE
L7  solve a(n) x(n+1) − B(n) x(n) = c(n) for x with deg x ≤ D   ▷ a linear system over K
L8  if there is no solution then return NONE
L9  return y = B(n) x(n) / c(n)                     ▷ z = y · t is an antidifference
```

Lines L2 to L4 move every factor that $a$ shares with a shifted copy of $b$ into $c$: if $g(n)$ divides $a(n)$ and $g(n-h)$ divides $b(n)$, then $g(n)/g(n-h) = C(n+1)/C(n)$ for $C(n) = \prod_{i=1}^{h} g(n-i)$, so the ratio is unchanged. The bound $H$ is the sum of Fujiwara root bounds of $\mathrm{num}$ and $\mathrm{den}$: a common root of $a(n)$ and $b(n+h)$ means $h = \beta - \alpha$ for roots $\alpha$ of $a$ and $\beta$ of $b$. The classical alternative computes the nonnegative integer roots of the resultant $\operatorname{Res}_n(a(n), b(n+h))$ as a polynomial in $h$; see [resultant](/resultant/).

Line L5 computes the degree bound by comparing leading terms in the equation. With $d_1 = \deg a$ and $d_2 = \deg B$: if $d_1 \ne d_2$, then $D = \deg c - \max(d_1, d_2)$; if $d_1 = d_2$ and the leading coefficients differ, $D = \deg c - d_1$; if they are equal to $\lambda$, then $D = \deg c - d_1 + 1$, or the number $(\beta - \alpha)/\lambda$ if that is a larger nonnegative integer, where $\alpha$ and $\beta$ are the coefficients of $n^{d_1 - 1}$ in $a$ and $B$.

## Example

Take $t(k) = k \cdot k!$, so $r(k) = (k+1)^2 / k$. The trace, from the implementation:

| step | $a$ | $b$ | $c$ | note |
|---|---|---|---|---|
| L1 | $(k+1)^2$ | $k$ | $1$ | $H = 4$ |
| L3, $h = 0$ | $(k+1)^2$ | $k$ | $1$ | $\gcd((k+1)^2, k) = 1$ |
| L3 and L4, $h = 1$ | $k + 1$ | $1$ | $k$ | $g = \gcd((k+1)^2, k+1) = k + 1$, $g(k-1) = k$ |
| L3, $h = 2, 3, 4$ | $k + 1$ | $1$ | $k$ | gcds with $b = 1$ are 1 |
| L5 | | $B = 1$ | | $d_1 = 1 \ne d_2 = 0$, so $D = \deg c - 1 = 0$ |
| L7 | | | | $(k+1) x_0 - x_0 = k$ gives $x = 1$ |
| L9 | | | | $y = 1 \cdot 1 / k = 1/k$ |

So $z(k) = y(k)\, t(k) = k!$, and $\sum_{k=0}^{n-1} k \cdot k! = n! - 1$.

Two more runs, each checked by the tests:

- $t(k) = \binom{2k}{k} / 4^k$ has $r(k) = (2k+1)/(2k+2)$. The Gosper form is $a = k + \frac{1}{2}$, $b = k + 1$, $c = 1$, since $\beta - \alpha = -\frac{1}{2}$ is not an integer. The leading coefficients of $a$ and $B = k$ agree, $(\beta - \alpha)/\lambda = -\frac{1}{2}$, so $D = 0$; the equation $(k + \frac12) x_0 - k x_0 = 1$ gives $x = 2$ and $y = 2k$. Hence $\sum_{k=0}^{n-1} \binom{2k}{k} 4^{-k} = 2n \binom{2n}{n} 4^{-n}$.
- $t(k) = k!$ has $r(k) = k + 1$. Here $a = k + 1$, $b = c = 1$, $B = 1$, $D = 0 - 1 < 0$, so the answer is NONE: $\sum k!$ has no hypergeometric closed form. Likewise the harmonic term $1/(k+1)$ gives NONE at line L8.

## Correctness

The proof is in the correctness file; here is the outline. A hypergeometric antidifference $z$ exists exactly when a rational $y$ solves $r(n) y(n+1) - y(n) = 1$, with $z = y t$, because $y = z/t = 1/(\rho - 1)$ for the ratio $\rho$ of $z$. Lines L1 to L4 produce the Gosper form, and terminate because each update lowers $\deg a$. Substituting $y = B x / c$ turns the rational equation into the polynomial equation of line L7. The key lemma, due to Gosper and sharpened by Petkovšek, says that the coprimality condition of the Gosper form forces every solution $x$ to be a polynomial: a pole chain $\gamma, \gamma + 1, \ldots, \gamma + m$ of $x$ would give a common root of $a(n)$ and $b(n + m)$. Comparing leading coefficients gives the degree bound of line L5. So the linear system of line L7 has a solution exactly when an antidifference exists.

## Complexity

The cost model is operations in $K$. Write $d$ for the degree bound of the input, $H$ for the bound on integer root differences, and $D$ for the degree bound of line L5.

- **Gosper form.** Lines L2 to L4 make $H + 1$ iterations, plus at most $d$ successful updates. Each computes a shift and a gcd of polynomials of degree at most $d$, $O(d^2)$ operations classically, so $O(H d^2)$ in total, a proved bound. The resultant method replaces the factor $H$ by the cost of finding integer roots of a polynomial of degree $d^2$ in $h$.
- **Linear system.** Line L7 has $D + 1$ unknowns and at most $d + D + 1$ equations, solved by Gaussian elimination in $O((d + D)^3)$ operations, a proved bound.
- **Pseudo-polynomial.** $H$, $D$ and $\deg c$ are integers read from the input, not sizes. For $r(n) = (n + 1 + m)/(n + 1)$ the Gosper form has $\deg c = m$, and for $r(n) = (n + 1)/(n + 1 + m)$ the degree bound is $D = m - 1$. So the cost is polynomial in $d$ and in these integers, but can be exponential in the bit size of the input. This is inherent: the output $y$ can have degree about $m$.
- **Best case.** When the gcds at $h = 0$ are trivial, $H$ is small and $D < 0$, as for $t = k!$, the cost is $O(d^2)$.
- **Bit cost.** Over $\mathbb{Q}$ the coefficients of $c$ and $x$ grow; no bound on the bit size is used here beyond exact arithmetic.

The space is dominated by the matrix of line L7, $O((d + D)^2)$ field elements.

## Properties

- **Decision procedure.** A negative answer is a proof that no hypergeometric antidifference exists.
- **Unique answer.** If $t$ is not a rational function, the rational $y$ is unique, since two solutions differ by a $w$ with $w t$ constant.
- **Rational certificate.** The output $y$ is a rational function, and the claim $z(n+1) - z(n) = t(n)$ is checked by verifying $r(n) y(n+1) - y(n) = 1$ with rational function arithmetic.
- **Exact.** Over $\mathbb{Q}$ every step is exact; the algorithm needs no factorization, only gcds and linear algebra.

## Variants and improvements

- **Parametrized Gosper.** Allow the term to be $\sum_i a_i\, t_i(n)$ with unknown constants $a_i$ that enter the linear system of line L7 linearly. This is the inner loop of [Zeilberger's algorithm](/zeilberger-algorithm/) and of [creative telescoping](/creative-telescoping/).
- **Dispersion by resultants.** Compute the set of $h$ with $\gcd(a(n), b(n+h)) \ne 1$ as the nonnegative integer roots of $\operatorname{Res}_n(a(n), b(n+h))$, or by factoring $a$ and $b$ and comparing factors of the same degree. Factoring is often faster in practice.
- **Greatest factorial factorization.** Paule's formulation replaces the Gosper form by the greatest factorial factorization of polynomials, the discrete analogue of squarefree factorization, and makes the analogy with [Hermite reduction](/hermite-reduction/) exact.
- **q-Gosper.** The same steps with $q$-shifts $n \mapsto qn$ handle $q$-hypergeometric terms.
- **Faster equation solving.** Von zur Gathen and Gerhard analyze the cost in terms of the dispersion and the degree bound, and discuss methods for the equation of line L7 that are faster than dense linear algebra.

## When to use it

Use Gosper's algorithm to decide whether a sum of hypergeometric terms with variable upper limit has a closed form, and as the core of definite summation. When the sum is definite with natural boundaries, such as $\sum_k \binom{n}{k}^2$, the partial sums usually have no closed form even though the full sum does; then use [Zeilberger's algorithm](/zeilberger-algorithm/). For sums of rational functions, Gosper's algorithm decides the rational part and the remainder needs polygamma functions, as logarithms are needed in integration.

## Pitfalls

- **Partial sums of definite sums.** $\sum_{k=0}^{m} \binom{n}{k}$ with symbolic $n$ and $m$ is not Gosper-summable, although $\sum_{k=0}^{n} \binom{n}{k} = 2^n$. A NONE answer is about the indefinite sum, not about the definite one.
- **Poles and zeros of the term.** The identity $\sum_{k=a}^{b-1} t(k) = z(b) - z(a)$ holds only where $t$ is defined and $y$ has no pole. For $t(k) = k \cdot k!$, $y = 1/k$ has a pole at $k = 0$, where $t(0) = 0$; the formula $z(k) = k!$ is the continuous extension, and the sum starting at 0 is still correct, but this must be checked.
- **The range of $h$.** Missing a value of $h$ at lines L2 to L4 leaves the form non-coprime, and the degree bound or the polynomial lemma can then fail silently. Use a proved bound or the resultant.
- **Unreduced input.** Common factors of $\mathrm{num}$ and $\mathrm{den}$ are removed at $h = 0$; skipping $h = 0$ would be a bug.
- **Degree bound case.** Forgetting the case in which $(\beta - \alpha)/\lambda$ is a nonnegative integer makes the algorithm miss solutions of high degree; the tests include terms where this case decides the answer.

## Implementations

## History

Gosper found the algorithm while working on the Macsyma system at MIT and published it in 1978 as a decision procedure for indefinite hypergeometric summation. Graham, Knuth and Patashnik made it known to a wide audience in *Concrete Mathematics* (1989). Zeilberger (1990, 1991) used a parametrized version of it to sum definite hypergeometric sums, which turned it into the engine of a whole theory. Petkovšek (1992) introduced the normal form now called the Gosper-Petkovšek form and used it in his algorithm Hyper; Paule (1995) gave the formulation with greatest factorial factorization.

## References
