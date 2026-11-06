---
tag: PBN3R6
kind: concept
slug: knuth-schroeppel-multiplier
name: Knuth-Schroeppel multiplier
aliases:
- Knuth-Schroeppel function
area: number-theory/factorization
level: research
summary: A rule for a small multiplier k such that the sieve or CFRAC factors kN instead of N. It picks the k that maximizes the expected log of the small prime part of the values, minus (1/2) ln k.
prereqs: [quadratic-sieve, legendre-symbol, quadratic-residue, smooth-number]
see_also: [quadratic-sieve, multiple-polynomial-quadratic-sieve, continued-fraction-factorization, factor-base, shanks-squfof, lehman-factorization, smooth-number, integer-factorization]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.5.4, Factoring into primes (the continued fraction method with a multiplier k, and the function of Schroeppel for choosing k)
  - paper: "Robert D. Silverman, The multiple polynomial quadratic sieve, Mathematics of Computation 48(177), 1987"
    locator: pages 329 to 339 (the choice of the multiplier by the Knuth-Schroeppel function in MPQS)
  - paper: "Michael A. Morrison and John Brillhart, A method of factoring and the factorization of F7, Mathematics of Computation 29(129), 1975"
    locator: pages 183 to 205 (expanding the square root of kN for a small multiplier k)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Exercise 6.3, page 307 (the multiplier in QS, with the numbers 1883199855619205203 and 21565941721999797939843713963)
---

The Knuth-Schroeppel multiplier is a small squarefree integer $k$ such that factoring $kN$ instead of $N$ makes the [quadratic sieve](/quadratic-sieve/) or the [continued fraction method](/continued-fraction-factorization/) faster. A multiplier changes which primes are in the [factor base](/factor-base/), since an odd prime $p$ is in it when $kN$ is a [quadratic residue](/quadratic-residue/) modulo $p$, and it changes the power of $2$ in the values. It also makes the values larger by a factor $\sqrt k$. The Knuth-Schroeppel function $f(k, N)$ weighs these effects: it is the expected logarithm of the part of a value that the small primes divide, minus $\frac12 \ln k$. One computes it for all small squarefree $k$ and takes the largest. Donald Knuth published it in his analysis of the continued fraction method, crediting Richard Schroeppel.

## In plain words

The sieve looks for numbers built only from small primes. Which small primes can appear is fixed by the number to factor. For some numbers, many of the smallest primes are excluded, and the sieve then finds fewer good numbers.

The fix is to factor a small multiple of the number instead. A different multiple lets a different set of small primes in. Any factor found for the multiple still gives a factor of the original number.

The price is that the numbers in the sieve get larger, by the square root of the multiplier. So try each small multiplier, add up how much the small primes are expected to divide out, subtract the price, and keep the multiplier with the best score.

## The idea

Let $m = kN$ with $k$ squarefree and $\gcd(k, N) = 1$; a common factor of $k$ and $N$ is already a factor. The quadratic sieve on $m$ looks at $v(x) = x^2 - m$ for $x$ near $\sqrt m$, and any congruence $X^2 \equiv Y^2 \pmod{m}$ that it finds is also one modulo $N$, so $\gcd(X - Y, N)$ is used as before.

**The expected valuation.** For a prime $p$, let $g(p, m)$ be the average of the exponent $v_p(x^2 - m)$ over $x$, in the sense of density: $g(p, m) = \sum_{e \ge 1} P(p^e \mid x^2 - m)$, where $P$ is the fraction of residues $x$ modulo $p^e$. Then

| case | $g(p, m)$ |
|---|---|
| $p$ odd, $p \nmid m$, $(m/p) = 1$ | $2/(p - 1)$ |
| $p$ odd, $p \nmid m$, $(m/p) = -1$ | $0$ |
| $p$ odd, $p \mid k$ | $1/p$ |
| $p = 2$, $m \equiv 1 \pmod 8$ | $2$ |
| $p = 2$, $m \equiv 5 \pmod 8$ | $1$ |
| $p = 2$, $m \equiv 3 \pmod 4$ | $1/2$ |
| $p = 2$, $m \equiv 2 \pmod 4$ | $1/2$ |

*Proof.* For odd $p \nmid m$ with $(m/p) = 1$, the congruence $x^2 \equiv m$ has exactly two roots modulo $p$, and each lifts to exactly one root modulo $p^e$ by [Hensel lifting](/hensel-lifting/), since the derivative $2x$ is a unit. So $P(p^e \mid x^2 - m) = 2/p^e$ and the sum is $2/(p - 1)$. If $(m/p) = -1$ there is no root modulo $p$. If $p \mid k$, then $p \nmid N$ and $p^2 \nmid k$, so $p$ exactly divides $m$; then $p \mid x^2 - m$ if and only if $p \mid x$, and in that case $x^2 \equiv 0 \pmod{p^2}$ while $m \not\equiv 0$, so the exponent is exactly $1$. This gives $1/p$.

For $p = 2$ and $m$ odd, $x^2 - m$ is even exactly when $x$ is odd, with probability $\frac12$, and then $x^2 \equiv 1 \pmod 8$. If $m \equiv 3 \pmod 4$, then $x^2 - m \equiv 2 \pmod 4$, exponent $1$, average $\frac12$. If $m \equiv 5 \pmod 8$, then $x^2 - m \equiv 4 \pmod 8$, exponent $2$, average $1$. If $m \equiv 1 \pmod 8$, then $8 \mid x^2 - m$ for every odd $x$. For $e \ge 3$ the odd squares modulo $2^e$ are exactly the residues $\equiv 1 \pmod 8$, and each is the square of exactly $4$ odd residues, since the squaring map on the $2^{e-1}$ odd residues has kernel $\{\pm 1, \pm 1 + 2^{e-1}\}$ and its image has $2^{e-1}/4 = 2^{e-3}$ elements. So $P(2^e \mid x^2 - m) = 4/2^e$ for $e \ge 3$, and $g = \frac12 + \frac12 + \frac12 + \sum_{e \ge 4} 4/2^e = \frac32 + \frac12 = 2$. If $m \equiv 2 \pmod 4$, odd $x$ give an odd value and even $x$ give $x^2 - m \equiv 2 \pmod 4$, so the average is $\frac12$. $\square$

**The function.** The expected value of $\ln$ of the part of $v(x)$ made of primes $p \le B$ is $\sum_{p \le B} g(p, kN)\ln p$. The values have size about $2M\sqrt{kN}$ on an interval of length $M$, which is $\frac12 \ln k$ larger in the logarithm than for $k = 1$. The Knuth-Schroeppel function is
$$f(k, N) = \sum_{p \le B} g(p, kN)\ln p - \tfrac12 \ln k,$$
and the rule is to take the squarefree $k$ in a small range, such as $k < 100$, that maximizes it. A larger $f$ means a smaller expected leftover $\ln|v(x)| - \sum g \ln p$, hence more [smooth](/smooth-number/) values per sieved interval. The function is a heuristic: it treats the $x$ as random modulo each prime power, and it ignores the change in the size of the factor base.

**Costs.** For each $k$, $f(k, N)$ needs one [Legendre symbol](/legendre-symbol/) per prime up to $B$, so trying all $k < 100$ costs a few thousand symbols, negligible next to the sieve.

## Examples

**The example of Crandall and Pomerance.** For $N = 1883199855619205203 = 924009221 \cdot 2038074743$, $N \equiv 3 \pmod 8$, and with $B = 2000$:

| $k$ | $kN \bmod 8$ | $f(k, N)$ | primes in the base | smooth values among $20000$ |
|---|---|---|---|---|
| 1 | 3 | 6.497 | 151 | 61 |
| 2 | 6 | 5.539 | 129 | 32 |
| 3 | 1 | 7.870 | 156 | 124 |
| 5 | 7 | 6.561 | 165 | 89 |
| 11 | 1 | 4.828 | 154 | 37 |
| 19 | 1 | 6.949 | 159 | 92 |

The last column counts the $x$ in $[\lceil\sqrt{kN}\rceil, \lceil\sqrt{kN}\rceil + 20000)$ for which $x^2 - kN$ is $2000$-smooth. The best squarefree $k < 100$ by $f$ is $k = 3$: then $kN \equiv 1 \pmod 8$, so $2$ contributes $2\ln 2$ instead of $\frac12 \ln 2$, and $3$ divides $k$. It doubles the number of smooth values over $k = 1$, which matches the advice of the exercise to compare $N$ with $3N$. The order by $f$ agrees with the order by the counts, except for $k = 2$ and $k = 11$, which are close together at the bottom. The next best by $f$ are $k = 19$ and $k = 34$.

**The second number.** For $N = 21565941721999797939843713963 = 21565941721999 \cdot 1000000000000037$, again $N \equiv 3 \pmod 8$, and with $B = 2000$ the function gives $f(1, N) = 6.076$ and $f(3, N) = 8.645$, the best value for squarefree $k < 100$, well ahead of $k = 23$ with $6.745$.

**Why $k = 1$ can be poor.** When $N \equiv 3 \pmod 4$, the values $x^2 - N$ have on average only half a factor of $2$, and when also $(N/3) = (N/5) = (N/7) = -1$, the smallest odd primes are all missing from the base. A multiplier $k \equiv N \pmod 8$, such as $k = 3$ when $N \equiv 3 \pmod 8$, gives $kN \equiv N^2 \equiv 1 \pmod 8$ and puts the primes of $k$ into the base.

## Where it is used

- **The quadratic sieve.** Most implementations of the [quadratic sieve](/quadratic-sieve/) and of [MPQS](/multiple-polynomial-quadratic-sieve/) start by choosing $k$ with this function; Silverman describes its use for MPQS.
- **The continued fraction method.** Morrison and Brillhart expanded $\sqrt{kN}$ with a small multiplier; Knuth gave the function to choose $k$ for [CFRAC](/continued-fraction-factorization/), where the values $Q_i$ are bounded by $2\sqrt{kN}$.
- **SQUFOF and Fermat type methods.** [SQUFOF](/shanks-squfof/), [Lehman's method](/lehman-factorization/) and [Hart's one line method](/hart-one-line-factorization/) also work with $kN$, but there the multiplier serves a different purpose: to make $kN$ close to a product of two nearly equal numbers, or to run several expansions in parallel.
- **The number field sieve.** The analogue for the polynomials of the [number field sieve](/general-number-field-sieve/) is Murphy's $\alpha$ value, the same expected valuation of small primes compared with a random integer, used to rank candidate polynomials.

## References
