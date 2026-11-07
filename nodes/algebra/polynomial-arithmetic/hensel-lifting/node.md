---
tag: ZKSCMK
kind: algorithm
slug: hensel-lifting
name: Hensel lifting
aliases:
- Hensel's lemma iteration
- Newton-Hensel lifting
- p-adic lifting
- quadratic Hensel lifting
area: algebra/polynomial-arithmetic
level: advanced
summary: Lifts a factorisation modulo p to one modulo p^k with quadratic convergence in the exponent.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, k: the target exponent in the modulus p^k, p: the prime, M: the cost function M(n) of multiplying two polynomials of degree less than n, I: the cost function I(l) of multiplying two integers of l digits}
  time: {worst: O(M(n) log k + M(n) log n)}
  space: {extra: O(n)}
  lifting_steps: {worst: log2 k + 1}
  word_operations: {worst: O(M(n) I(k log p))}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1969
  people: [Kurt Hensel, Hans Zassenhaus]
  note: Hensel's lemma on lifting factorizations from p to p-adic precision dates from Hensel's work around 1900; Zassenhaus in 1969 used the quadratic form of the lifting, which doubles the exponent at each step, to factor polynomials over the integers.
prereqs: [hensel-lemma, polynomial-extended-euclidean-algorithm, polynomial-division, monic-polynomial]
see_also: [zassenhaus-algorithm, polynomial-factorization-over-integers, newton-iteration, dixon-p-adic-lifting, berlekamp-factorization, cantor-zassenhaus-algorithm, newton-power-series-inversion, fast-polynomial-division]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 15.4, Hensel lifting (the Hensel step and its cost); Section 15.5, Multifactor Hensel lifting; Section 15.6, Factoring using Hensel lifting, Zassenhaus' algorithm
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.5.3, Factorization modulo p^e, Hensel's lemma; Section 3.5.4, Factorization over Z
  - paper: doi:10.1016/0022-314X(69)90047-X
    title: Hans Zassenhaus, On Hensel factorization I, Journal of Number Theory 1, 291-311, 1969
    locator: the quadratic lifting of a factorization modulo p and its use for factoring over the integers
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of polynomials (factoring over the integers by lifting a factorization modulo p)
---

Hensel lifting takes a factorization $f \equiv g h \pmod p$ of an integer polynomial into two coprime factors and turns it into a factorization $f \equiv g^* h^* \pmod{p^k}$ with $g^* \equiv g$ and $h^* \equiv h \pmod p$. Each step goes from modulus $m$ to modulus $m^2$ with a few polynomial products and two divisions, so $\lceil \log_2 k \rceil$ steps reach $p^k$. It is the step of [Hensel's lemma](/hensel-lemma/) done again and again, and it is the bridge from factoring modulo a prime, by [Berlekamp's algorithm](/berlekamp-factorization/) or the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/), to [factoring over the integers](/polynomial-factorization-over-integers/).

Notation: $f \in \mathbb{Z}[x]$ has degree $n$, $p$ is a prime that does not divide the leading coefficient of $f$, and $g, h \in \mathbb{Z}[x]$ have $h$ monic of degree $e$, $f \equiv gh \pmod p$, and $g \bmod p$, $h \bmod p$ coprime. Congruence of polynomials modulo $m$ means congruence of every coefficient. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$, and $I(l)$ is the cost of multiplying two integers of $l$ digits. Costs count operations on residues modulo $p^k$ unless the text says word operations.

## In plain words

Suppose you can split a polynomial into two parts, but only if you look at remainders after dividing every coefficient by a small prime. Hensel lifting fixes the two parts so that the split also holds for remainders after dividing by the square of the prime, then by the fourth power, and so on. Each round doubles the power, the same way Newton's method doubles the number of correct digits. The correction in each round is found by one small division of polynomials. When the power is large enough, the true integer factors, if there are any, can be read off from the lifted parts.

## The problem

**Input:** $f, g, h \in \mathbb{Z}[x]$ and a prime $p$ as in the notation, and an integer $k \ge 1$.

**Output:** $g^*, h^* \in \mathbb{Z}[x]$ with coefficients in $\{0, \ldots, p^k - 1\}$, $h^*$ monic of degree $e$, $f \equiv g^* h^* \pmod{p^k}$, $g^* \equiv g$ and $h^* \equiv h \pmod p$.

By the uniqueness part of [Hensel's lemma](/hensel-lemma/), this output is unique. The leading coefficient of $f$ goes into $g$, so that $h$ can be monic.

## The algorithm

The algorithm keeps cofactors $s, t$ with $s g + t h \equiv 1 \pmod m$ and lifts them together with $g$ and $h$. Lines L4 to L9 are one Hensel step, from modulus $m$ to modulus $m^2$; all arithmetic in them is modulo $m^2$.

```pseudo id=main
HENSEL-LIFT(f, g, h, p, k)
L1  (s, t) ← cofactors with s g + t h ≡ 1 mod p, deg s < deg h, deg t < deg g
L2  m ← p
L3  while m < p^k do
L4      e ← f - g h
L5      (q, r) ← quotient and remainder of s e divided by h
L6      g ← g + t e + q g;   h ← h + r
L7      b ← s g + t h - 1
L8      (c, d) ← quotient and remainder of s b divided by h
L9      s ← s - d;   t ← t - t b - c g
L10     m ← m^2
L11 return (g mod p^k, h mod p^k)
```

Line L1 uses the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) in $(\mathbb{Z}/p\mathbb{Z})[x]$, once. Lines L5 and L8 divide by the monic $h$, which is defined modulo any $m$ because it needs no inverse. The last step can overshoot $p^k$; the result is reduced at line L11. The implementation also lifts a list of pairwise coprime factors by splitting off one factor at a time, and lifts a simple root $a$, which is the case $h = x - a$.

## Example

Take $f = x^4 - 1$ and $p = 5$. Modulo $5$, $f = (x - 1)(x + 1)(x - 2)(x + 2)$, since $2^2 \equiv -1$. Lift $h = x - 2$ against $g = (x - 1)(x + 1)(x + 2) = x^3 + 2x^2 - x - 2$ to $5^4 = 625$. Line L1 gives $s = 3$ and $t = 2x^2 + 3x + 4$; indeed $3g + th = 5x^3 + 15x^2 - 5x - 5 + 1 \equiv 1 \pmod 5$. Coefficients are shown in the symmetric range.

| step | $m \to m^2$ | $e = f - gh$ | $q$, $r$ | new $h$ | new $g$ |
|---|---|---|---|---|---|
| 1 | $5 \to 25$ | $5x^2 - 5$ | $15x + 5$, $-5$ | $x - 7$ | $x^3 + 7x^2 - x - 7$ |
| 2 | $25 \to 625$ | $-25x^3 - 150x^2 + 175x + 300$ | $-200x^2 - 100x + 75$, $-200$ | $x - 182$ | $x^3 + 182x^2 - x - 182$ |

After step 1, $7^2 = 49 \equiv -1 \pmod{25}$; after step 2, $182^2 = 33124 \equiv -1 \pmod{625}$. So $x - 182$ is the factor of $x^4 - 1$ modulo $625$ that lies over $x - 2$, and $182$ is a square root of $-1$ in the $5$-adic integers to four digits. The new $g$ is $(x^2 - 1)(x + 182)$. A script checked every entry.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The loop invariant is that at line L3, with $m = p^{2^i}$, $f \equiv gh$ and $sg + th \equiv 1 \pmod m$, $h$ is monic of degree $e$, $g \equiv g_0$ and $h \equiv h_0 \pmod p$, and $\deg s < e$, $\deg t < n - e$. One step keeps it by the identities

$$f - g^* h^* = e\,(1 - sg - th) - (te + qg)\, r, \qquad s^* g^* + t^* h^* = 1 - b^2,$$

In the first identity each of the two products has two factors that are $\equiv 0 \pmod m$, and in the second $b \equiv 0 \pmod m$. So $f \equiv g^* h^*$ and $s^* g^* + t^* h^* \equiv 1 \pmod{m^2}$. The loop stops when $m \ge p^k$, so $p^k$ divides $m$ and the congruences hold modulo $p^k$.

## Complexity

The bounds are proved. They count operations on residues modulo $m^2$ in each step, and word operations where stated.

- **Steps.** $m = p^{2^i}$ after $i$ steps, so the loop runs $\lceil \log_2 k \rceil$ times.
- **One step.** Nine products and two divisions by a monic polynomial of degree $e$, all of polynomials of degree at most $2n$, so $O(M(n))$ operations. With [fast division](/fast-polynomial-division/) this is $O(M(n))$; with schoolbook arithmetic, as in the implementation, $O(n^2)$.
- **Line L1.** The extended Euclidean algorithm modulo $p$ costs $O(n^2)$ operations, or $O(M(n) \log n)$ with the fast half-gcd method.
- **Total operations.** $O(M(n) \log k + M(n) \log n)$.
- **Word operations.** In step $i$ the residues have about $2^{i+1} \log p$ digits, so one step costs $O(M(n) I(2^{i+1} \log p))$ word operations. These costs grow geometrically, so the last step dominates and the total is $O(M(n) I(k \log p))$. Von zur Gathen and Gerhard analyze the cost of the Hensel step in Section 15.4.
- **Space.** $O(n)$ residues modulo $p^k$.

**In practice (observed).** For factoring over $\mathbb{Z}$, lifting is rarely the bottleneck; the recombination of the lifted factors or the factorization modulo $p$ usually costs more. The constant of one step is about nine products and two divisions, and libraries reduce it by skipping the update of $s, t$ in the last step and by lifting all factors through a balanced tree.

## Properties

- **Quadratic convergence.** The exponent doubles in each step, like the number of correct digits in [Newton iteration](/newton-iteration/). In fact the step for $h = x - a$ is Newton's step $a \leftarrow a - f(a)/f'(a)$.
- **Any modulus.** One step needs only $f \equiv gh$, $sg + th \equiv 1 \pmod m$ and $h$ monic, for any integer $m \ge 2$ or any element $m$ of a commutative ring. The prime $p$ is used only at line L1.
- **Degrees stay fixed.** $\deg h^* = e$ and $\deg g^* = n - e$ in every step, so the work in a step does not grow with the step count, only the size of the residues.
- **Unique result.** For given $g, h$ modulo $p$, the lifted factors modulo $p^k$ are unique.
- **Deterministic and iterative.** No randomness and no recursion.

## Variants and improvements

- **Linear lifting.** Keep $s, t$ fixed modulo $p$ and go from $p^j$ to $p^{j+1}$ in each step. Each step is cheaper, since all corrections are computed modulo $p$, but $k - 1$ steps are needed. This was the original form of the lemma.
- **Multifactor lifting.** For $f \equiv \mathrm{lc}(f)\, f_1 \cdots f_r \pmod p$, split the factors into two halves, lift the two products, and go down a balanced binary tree; von zur Gathen and Gerhard, Section 15.5, give this factor tree method.
- **Root lifting.** For a simple root $a$ of $f$ modulo $p$, lifting $h = x - a$ is Newton's iteration $b \leftarrow b - f(b)\, f'(b)^{-1} \bmod p^{2j}$, which needs only evaluations; see [Hensel's lemma](/hensel-lemma/).
- **Lifting in other rings.** With $m = y - y_0$ in $R[y]$, the same step lifts a factorization of a bivariate polynomial at $y = y_0$ to one modulo $(y - y_0)^k$. This is the basis of multivariate gcd and factoring methods. With $m = x$ it gives [Newton iteration for power series](/newton-power-series-inversion/).
- **Linear systems.** The same idea, with a matrix inverse modulo $p$ in place of $s, t$, is [Dixon's $p$-adic lifting](/dixon-p-adic-lifting/) for rational solutions of linear systems.

## When to use it

Use Hensel lifting when a factorization or a root is easy to find modulo a prime $p$ and is wanted modulo a large power of $p$ or over $\mathbb{Z}$. The main use is the [Zassenhaus algorithm](/zassenhaus-algorithm/): factor modulo a small prime that does not divide the discriminant, lift to $p^k$ larger than twice a bound on the coefficients of the factors, and recombine. Square roots modulo $p^k$ and $p$-adic roots are other uses. For a factorization modulo a product of distinct primes, use the [Chinese remainder theorem](/chinese-remainder-theorem/) instead.

## Pitfalls

- **Non-monic $h$.** The divisions at lines L5 and L8 need a monic divisor. Put the leading coefficient of $f$ into $g$.
- **$p$ divides the leading coefficient of $f$.** Then the degrees drop modulo $p$ and the lifted factors need not have the right degrees. Choose another prime.
- **Factors not coprime modulo $p$.** If $p$ divides the discriminant of $f$, a square-free $f$ can have a repeated factor modulo $p$, and the cofactors do not exist. Choose $p$ with $f$ square-free modulo $p$.
- **Not lifting $s$ and $t$.** With $s, t$ only correct modulo $p$, the error after the step is only $\equiv 0 \pmod{mp}$, so the step is linear, not quadratic.
- **Reading off integer factors.** Coefficients of a true factor can be negative. Map the lifted coefficients to the symmetric range $(-p^k/2, p^k/2]$, and lift far enough that twice the coefficient bound is below $p^k$.

## Implementations

## History

Kurt Hensel developed the $p$-adic numbers around 1900 and gave the lemma that lifts a factorization modulo $p$ to all powers of $p$, in its linear form. Hans Zassenhaus, in his 1969 paper "On Hensel factorization I", used the quadratic form, in which the cofactors $s, t$ are lifted too and the exponent doubles at each step, and combined it with [Berlekamp's factorization](/berlekamp-factorization/) modulo $p$ to give the first practical algorithm for factoring polynomials over the integers. Multifactor lifting by a factor tree and the fast versions with $O(M(n))$ operations per step are presented in von zur Gathen and Gerhard, Sections 15.4 and 15.5.

## References
