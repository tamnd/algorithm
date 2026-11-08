---
tag: 4BG9SS
kind: algorithm
slug: chebyshev-economization
name: Chebyshev economization
aliases:
- Economization of power series
- Telescoping of power series
- Lanczos economization
area: numerical/interpolation-and-approximation
level: advanced
summary: Rewrite a polynomial in the Chebyshev basis and drop the trailing terms. The degree falls while the added error, at most the sum of the dropped coefficients, stays nearly minimax.
solves: [function-approximation]
model: real-ram
complexity:
  vars: {N: "the degree of the given polynomial", m: "the degree after economization"}
  time: {convert: Θ(N^2), truncate: Θ(N), back_to_monomial: Θ(m^2)}
  space: {extra: Θ(N)}
  flops: {convert: "3N^2/2", back_to_monomial: "2m^2"}
properties: {deterministic: true, recursive: false, error_bound: "sum of the dropped |c_k|", minimax_for_one_term: true}
history:
  year: 1938
  people: [Cornelius Lanczos]
  note: Lanczos introduced the idea in 1938 as the telescoping of power series and popularized it as economization in his Applied Analysis (1956); it was the standard way to build library approximations before the Remez algorithm became routine.
prereqs: [chebyshev-series, chebyshev-polynomials]
see_also: [chebyshev-interpolation, minimax-approximation, remez-algorithm, chebyshev-equioscillation-theorem, horner-rule, polynomial-evaluation, pade-approximation]
sources:
  - book: isbn:9780486656564
    title: Cornelius Lanczos, Applied Analysis, Prentice Hall, 1956; Dover reprint, 1988
    locator: chapter on approximation by Chebyshev polynomials, the economization (telescoping) of power series
  - paper: "Cornelius Lanczos, Trigonometric interpolation of empirical and analytical functions, Journal of Mathematics and Physics 17 (1938) 123-199"
    locator: the reduction of power series by Chebyshev polynomials
  - book: isbn:9780849303555
    title: J. C. Mason and D. C. Handscomb, Chebyshev Polynomials, Chapman and Hall/CRC, 2003
    locator: Chapter 2 (monomials in terms of Chebyshev polynomials) and the section on economization of power series
  - book: isbn:9780471628965
    title: Theodore J. Rivlin, Chebyshev Polynomials, second edition, Wiley, 1990
    locator: Chapter 1 (the minimax property of T_n) and Chapter 3 (Chebyshev expansions)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 3 (Chebyshev coefficients), Chapter 10 (best approximation) and Chapter 16 (Chebyshev projections are near-best)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5 (polynomial evaluation, Horner's rule and the condition of the monomial basis)
---

Chebyshev economization lowers the degree of a polynomial on $[-1, 1]$ with a controlled loss of accuracy. Write $p(x) = \sum_{k=0}^N b_kx^k$, typically a truncated Taylor series, in the Chebyshev basis as $p = \sum_{k=0}^N c_kT_k$, and drop the trailing terms $c_{m+1}T_{m+1}, \ldots, c_NT_N$. Because $|T_k| \le 1$ on the interval, the added error is at most $\sum_{k>m}|c_k|$, and because the Chebyshev coefficients of a smooth function decay fast, this is far smaller than what dropping the same number of monomial terms would cost. Dropping a single term gives exactly the best approximation of $p$ of one lower degree. Conversion costs about $\frac32N^2$ operations.

## In plain words

A Taylor polynomial is very accurate near the center of the interval and poor at the ends, and it uses more terms than the accuracy at the ends would justify. Economization rewrites the same polynomial as a sum of Chebyshev polynomials, which are wavy curves that never leave the band from $-1$ to $1$. In that form, the size of each weight is exactly the most that its term can contribute anywhere on the interval. The last weights are usually tiny, so you throw those terms away and know precisely how much accuracy you gave up. The result is a shorter polynomial whose error is spread evenly over the interval instead of piling up at the ends.

## The problem

The input is a polynomial $p(x) = \sum_{k=0}^N b_kx^k$ on $[-1, 1]$ and a tolerance $\tau \ge 0$ (or a target degree $m$). The output is a polynomial $q$ of the smallest degree $m$ that the method can certify, with $\|p - q\|_\infty \le \tau$, given by its Chebyshev coefficients $c_0, \ldots, c_m$, and the certified bound $e = \sum_{k=m+1}^N|c_k|$. On an interval $[a, b]$, first substitute $x = (2t - a - b)/(b - a)$.

Notation on the interpolation and approximation pages: $T_k$ are the Chebyshev polynomials, $E_m(f)$ is the error of the best (minimax) approximation of degree $m$ in the maximum norm on $[-1, 1]$. Costs are arithmetic operations on the [real RAM](/real-ram/); no function evaluations are needed, since the input is already a polynomial.

## The algorithm

```pseudo id=main
ECONOMIZE(b[0..N], τ)
L1  c ← [b[N]]                                  ▷ Chebyshev coefficients of the Horner partial sum
L2  for k ← N − 1 down to 0: c ← x·c;  c[0] ← c[0] + b[k]
                                                ▷ x·T_0 = T_1,  x·T_j = (T_{j+1} + T_{j−1})/2
L3  m ← N;  e ← 0;  while m > 0 and e + |c[m]| ≤ τ: e ← e + |c[m]|;  m ← m − 1
L4  return c[0..m], e                            ▷ |p − Σ c_k T_k| ≤ e on [−1, 1]
TO-MONOMIAL(c[0..m])                           ▷ optional, and ill-conditioned for large m
L5  for k ← 0 to m: form the monomial coefficients of T_k by T_k = 2x·T_{k−1} − T_{k−2}
L6      add c[k] times them to a
```

Lines L1 and L2 are Horner's rule carried out in the Chebyshev basis: the partial sum $b_N x^{N-k} + \cdots + b_k$ is held as a Chebyshev series, and multiplying a Chebyshev series by $x$ moves each coefficient half a step up and half a step down. Line L3 removes terms from the top while the running sum of their absolute values stays within the tolerance.

The output is best kept in Chebyshev form and evaluated by Clenshaw's recurrence ([Chebyshev interpolation](/chebyshev-interpolation/), lines L5 and L6 there). Lines L5 and L6 here are for when a monomial form is required, for example for a fixed Horner evaluation in hardware or in a math library.

## Example

**$e^x$, Taylor degree 5 to degree 4.** The Taylor polynomial $1 + x + \frac{x^2}2 + \frac{x^3}6 + \frac{x^4}{24} + \frac{x^5}{120}$ has $c_5 = \frac{1}{120} \cdot 2^{-4} = \frac{1}{1920}$, since $x^5 = \frac{1}{16}(10T_1 + 5T_3 + T_5)$. Dropping $c_5T_5$ is the same as replacing $x^5$ by $x^5 - \frac{1}{16}T_5 = \frac54x^3 - \frac5{16}x$, which gives
$$q(x) = 1 + \tfrac{383}{384}x + \tfrac12x^2 + \tfrac{17}{96}x^3 + \tfrac1{24}x^4, \qquad \|p - q\|_\infty = \tfrac{1}{1920} \approx 5.2 \times 10^{-4}.$$
Against $e^x$ the maximum error of $q$ is $2.14 \times 10^{-3}$, while the degree 4 Taylor polynomial has error $e - \frac{65}{24} = 9.95 \times 10^{-3}$, nearly five times larger, with the same number of terms.

**$e^x$, Taylor degree 8 economized.** The Chebyshev coefficients of the degree 8 Taylor polynomial are $1.26607$, $1.13032$, $0.271495$, $0.0443359$, $0.00547418$, $5.42535 \times 10^{-4}$, $4.49529 \times 10^{-5}$, $3.10020 \times 10^{-6}$, $1.93762 \times 10^{-7}$. Keeping degree $m$:

| $m$ | 3 | 4 | 5 |
|---|---|---|---|
| bound $\sum_{k>m}\lvert c_k\rvert$ | 6.06e-3 | 5.91e-4 | 4.82e-5 |
| error against $e^x$ | 6.07e-3 | 5.94e-4 | 5.13e-5 |
| Taylor of degree $m$ | 5.16e-2 | 9.95e-3 | 1.62e-3 |

Here all $c_k$ are positive, so the bound is attained at $x = 1$. Economization gains a factor of 8 to 30 over Taylor truncation of the same degree.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In outline:

1. *Conversion.* Each step of L2 maps the Chebyshev coefficients of a polynomial $r$ to those of $xr + b_k$, by $xT_0 = T_1$ and $xT_j = \frac12(T_{j+1} + T_{j-1})$; so after the loop $\sum c_kT_k$ equals Horner's form of $p$, which is $p$.
2. *Error bound.* $|p(x) - \sum_{k \le m}c_kT_k(x)| = |\sum_{k>m}c_kT_k(x)| \le \sum_{k>m}|c_k| = e$, since $|T_k(x)| = |\cos(k\arccos x)| \le 1$. Line L3 keeps $e \le \tau$, and the bound is attained when the dropped coefficients all have the same sign (at $x = 1$) or alternating signs (at $x = -1$).
3. *One term is optimal.* If only $c_NT_N$ is dropped, the error $c_NT_N$ equioscillates at the $N + 1$ points $\cos(j\pi/N)$, so by the [equioscillation theorem](/chebyshev-equioscillation-theorem/) $q$ is the best approximation of $p$ of degree $N - 1$, and $E_{N-1}(p) = |c_N| = |b_N|2^{1-N}$.
4. *Near-optimality in general.* For $k > m$, $|c_k| \le 2E_m(p)$, because $c_k = \frac2\pi\int_{-1}^1 (p - q^*)T_k(1 - x^2)^{-1/2}dx$ for the best approximation $q^*$ of degree $m$. Hence $E_m(p) \ge \frac12|c_{m+1}|$, and if the dropped coefficients decay at least geometrically, $|c_{k+1}| \le r|c_k|$ with $r < 1$, the economized error is at most $\frac{2}{1 - r}E_m(p)$.

**What economization does not control.** The bounds above compare $q$ with $p$. The error against the original function $f$ is at most $\|f - p\|_\infty + e$. When $p$ is a Taylor polynomial, $\|f - p\|$ is largest at the ends of the interval and can dominate, as in the first example; starting from a higher degree Taylor polynomial, or from the [Chebyshev series](/chebyshev-series/) of $f$ directly, removes this part.

## Complexity

- **Conversion (L1, L2).** At stage $k$ the series has $N - k + 1$ coefficients, and each costs one halving and two additions: about $3\sum_{j=1}^N j \approx \frac32N^2$ operations, plus $N$ additions of the $b_k$. With the closed form $x^k = 2^{1-k}\sum'_j\binom{k}{(k-j)/2}T_j$ (sum over $j \equiv k \pmod 2$, the $j = 0$ term halved) the cost is the same order.
- **Truncation (L3).** At most $N$ comparisons and additions.
- **Back to monomials (L5, L6).** Building $T_0, \ldots, T_m$ costs about $m^2$ operations, and accumulating $c_kT_k$ about $m^2$ more: $2m^2$ in total.
- **Space.** $O(N)$ for the coefficient vector, $O(m)$ for two Chebyshev polynomials in L5.
- **Fast variants.** Basis conversion can be done in $O(N\log N)$ or $O(N\log^2 N)$ operations by fast polynomial algorithms, but $N$ is rarely more than a few dozen here.

**Rounding.** The conversion to the Chebyshev basis is benign: $x^k$ is a combination of $T_0, \ldots, T_k$ with nonnegative weights that sum to 1, so each computed $c_j$ has an absolute error of a few units of $u\sum|b_k|$ times $N$, which is small whenever the monomial form itself was a reasonable representation. The conversion back is not: the monomial coefficients of $T_m$ have absolute values summing to about $(1 + \sqrt2)^m/2$ (3363 for $m = 10$, $2.3 \times 10^7$ for $m = 20$, $1.0 \times 10^{15}$ for $m = 40$), so a monomial evaluation of $q$ can lose about $0.38m$ decimal digits by cancellation, even though $|q|$ is of moderate size on $[-1, 1]$ (Higham, Chapter 5, on [Horner's rule](/horner-rule/)). For small degrees, as in math library kernels, this is harmless; for large ones keep the Chebyshev form.

## Properties

- **Certified.** The bound $e$ is computed exactly from the coefficients, not estimated; in exact arithmetic it holds for every $x \in [-1, 1]$.
- **Near-minimax.** Optimal for one dropped term, within the factor $2/(1 - r)$ of the best for geometrically decaying coefficients.
- **Linear.** For a fixed $m$, the map from $p$ to $q$ is linear: it is the Chebyshev projection onto degree $m$.
- **Even and odd parts are kept.** If $p$ is even or odd, so are the $c_k$ that survive, since $T_k$ has the parity of $k$.
- **No function evaluations.** Only the coefficients of $p$ are used.

## Variants and improvements

- **Economize from the Chebyshev series of $f$.** If $f$ can be sampled, [Chebyshev interpolation](/chebyshev-interpolation/) gives nearly the same truncated series without passing through a Taylor polynomial, and avoids the Taylor error at the ends.
- **Repeated one-term steps.** Dropping the top term, converting back and repeating is the original hand-computation form; it gives the same result as dropping several terms at once in the Chebyshev basis.
- **Remez polish.** The economized polynomial is an excellent starting guess for the [Remez algorithm](/remez-algorithm/), which turns it into the true [minimax approximation](/minimax-approximation/); the improvement is usually less than a factor of 2.
- **Rational economization.** The same idea applied to [Padé approximants](/pade-approximation/) gives rational approximations such as the Maehly (Chebyshev-Padé) approximants, which are often close to the best rational ones.
- **Weighted or relative error.** Economize $p/w$ for a weight $w$ when relative accuracy is wanted; the bound then holds for the weighted error.

## When to use it

Use it when you already have a polynomial, usually a Taylor or asymptotic series, and need a lower-degree one for fast evaluation on an interval, with a guaranteed error. It is quick, exact in rational arithmetic and easy to check by hand. If you can evaluate $f$ itself, Chebyshev interpolation is simpler and slightly better; if the last factor of 2 in the error matters, follow with the Remez algorithm.

## Pitfalls

- **Forgetting the interval.** Economization is relative to $[-1, 1]$. A polynomial in $t \in [a, b]$ must be rewritten in $x = (2t - a - b)/(b - a)$ first; economizing in $t$ directly on a different interval gives meaningless bounds.
- **Ignoring the starting error.** The bound is for $p - q$, not $f - q$. A Taylor polynomial of too low a degree leaves a large error at the ends that no economization can remove.
- **Converting back at high degree.** The monomial form of a degree 30 economized polynomial can lose ten or more digits; evaluate it with Clenshaw's recurrence instead.
- **Stopping at a zero coefficient.** For even or odd $p$, every other $c_k$ is zero; line L3 drops those for free, so a tolerance test must not stop just because one coefficient is tiny.
- **Comparing with $\tau$ in floating point.** The computed $e$ carries rounding error of order $u\sum|b_k|$; when $\tau$ is near that level the certification is not rigorous without interval arithmetic or exact rational coefficients.

## Implementations

## History

The minimax property of $2^{1-n}T_n$, the monic polynomial of least maximum norm on $[-1, 1]$, is due to Chebyshev (1854), and it is exactly the one-term case of economization. Cornelius Lanczos (1938) turned it into a practical method for shortening power series, which he called telescoping, and his Applied Analysis (1956) made "economization" the standard name and a standard technique of the 1950s and 1960s, when library approximations for computers were built by hand. Clenshaw's tables of Chebyshev coefficients (1962) and Fox and Parker's book (1968) carried it further. With the Remez algorithm and later with Chebfun, economization became a step in a pipeline rather than the end result, but it is still the simplest way to get a certified lower-degree polynomial from a series.

## References
