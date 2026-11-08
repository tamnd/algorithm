---
tag: Y77BXY
kind: algorithm
slug: quasi-monte-carlo-integration
name: Quasi-Monte Carlo integration
aliases:
- QMC integration
- quasi-Monte Carlo method
- low-discrepancy integration
- randomized quasi-Monte Carlo
area: numerical/quadrature
level: research
summary: Uses deterministic low-discrepancy points in place of random samples.
solves: [numerical-integration, multidimensional-integration]
model: real-ram
complexity:
  vars: {N: "the number of points", s: "the dimension", R: "the number of random shifts (0 for the deterministic rule)"}
  time: {worst: "Θ(max(R,1) N s log N)", average: "Θ(max(R,1) N s log N)", best: "Θ(max(R,1) N s log N)"}
  space: {extra: Θ(N + s)}
properties: {deterministic: true, recursive: false}
prereqs: [monte-carlo-integration, koksma-hlawka-inequality]
see_also: [halton-sequence, sobol-sequence, discrepancy, koksma-hlawka-inequality, monte-carlo-integration, sparse-grid-quadrature, latin-hypercube-sampling, multidimensional-integration]
sources:
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, CBMS-NSF Regional Conference Series in Applied Mathematics 63, 1992
    locator: Chapter 2 (the Koksma-Hlawka inequality), Chapter 3, Section 3.1 (van der Corput and Halton sequences, Theorem 3.6), Chapter 4 ((t, m, s)-nets and (t, s)-sequences)
  - book: isbn:9780521191593
    title: Josef Dick and Friedrich Pillichshammer, Digital Nets and Sequences, Cambridge University Press, 2010
    locator: Chapter 2 (QMC error and discrepancy), Chapter 4 (digital nets and sequences, including Sobol and Niederreiter), Chapter 13 (Owen's scrambling)
  - paper: "J. H. Halton, On the efficiency of certain quasi-random sequences of points in evaluating multi-dimensional integrals, Numerische Mathematik 2, 1960, 84-90"
    locator: the Halton sequence and its discrepancy bound O((log N)^s / N)
  - paper: "I. M. Sobol, On the distribution of points in a cube and the approximate evaluation of integrals, USSR Computational Mathematics and Mathematical Physics 7(4), 1967, 86-112"
    locator: the LP_tau sequences (Sobol sequences)
  - paper: "R. Cranley and T. N. L. Patterson, Randomization of number theoretic methods for multiple integration, SIAM Journal on Numerical Analysis 13(6), 1976, 904-914"
    locator: random shifts modulo 1 and error estimation from independent replicates
  - paper: doi:10.1017/S0962492913000044
    title: Josef Dick, Frances Y. Kuo and Ian H. Sloan, High-dimensional integration, the quasi-Monte Carlo way, Acta Numerica 22, 2013, 133-288
    locator: Sections 2 to 6 (worst-case error, weighted spaces, lattice rules, digital nets and randomization)
  - url: https://artowen.su.domains/mc/
    title: Art B. Owen, Monte Carlo theory, methods and examples, 2013
    locator: Chapters 15 to 17, quasi-Monte Carlo and randomized quasi-Monte Carlo (draft chapters on the author's site)
---

Quasi-Monte Carlo (QMC) integration estimates $\int_{[0,1]^s} f$ by the average $\frac1N \sum_{i=1}^N f(x_i)$, exactly as [Monte Carlo](/monte-carlo-integration/) does, but with points $x_i$ chosen deterministically to fill the cube as evenly as possible, measured by their [star discrepancy](/discrepancy/) $D_N^*$. The [Koksma-Hlawka inequality](/koksma-hlawka-inequality/) bounds the error by $V_{HK}(f)\, D_N^*$, and sequences such as [Halton](/halton-sequence/) and [Sobol](/sobol-sequence/) have $D_N^* = O((\log N)^s / N)$, so for integrands of bounded variation the error is close to $N^{-1}$ instead of $N^{-1/2}$. Randomizing the points by a random shift or a scrambling restores an unbiased estimate and a statistical error bar while keeping most of the gain.

## In plain words

Random sample points clump and leave holes, purely by chance, and that unevenness is what makes Monte Carlo slow. Quasi-Monte Carlo uses points that are laid down on purpose so that every region gets close to its fair share: the first point in the middle, the next ones filling the biggest gaps, and so on, in every coordinate at once.

For a function that changes in a reasonable way, the average over such points is much closer to the true average than over random points, and the error drops almost ten times when the number of points grows ten times, instead of about three times. The points are not random, so there is no automatic error bar. To get one, shift the whole set by a random amount, wrapping around the edges, a few times and look at how much the answers differ.

## The problem

Given an oracle for $f$ on a box $[a, b] = \prod_{k=1}^s [a_k, b_k]$ and a budget of $N$ evaluations, approximate $I(f) = \int_{[a,b]} f(x)\,dx$, and when asked, give a standard error. This is [multidimensional integration](/multidimensional-integration/) in the regime where $s$ is too large for [product rules](/product-quadrature/), typically from 5 to several hundred. Other regions and densities are first mapped to the unit cube.

## The algorithm

```pseudo id=main
QMC(f, a, b, N, R, rng)                 ▷ R = 0: deterministic Halton rule; R ≥ 1: R random shifts
L1  V ← Π_k (b_k − a_k)
L2  for r ← 1 to max(R, 1) do
L3      Δ ← (0, ..., 0) if R = 0 else a uniform random point of [0, 1)^s from rng
L4      S ← 0
L5      for i ← 1 to N do
L6          u ← frac(H(i) + Δ)                ▷ H(i) = (φ_2(i), φ_3(i), ..., φ_{p_s}(i)), coordinatewise
L7          S ← S + f(a + u ⊙ (b − a))
L8      Q_r ← V · S / N
L9  return mean of the Q_r, and for R ≥ 2 the standard error sqrt(Σ_r (Q_r − mean)^2 / (R (R − 1)))

φ_b(i)                                   ▷ radical inverse: reflect the base-b digits of i
L10 r ← 0;  f ← 1/b
L11 while i > 0 do  (i, d) ← (⌊i/b⌋, i mod b);  r ← r + d f;  f ← f/b
    return r
```

The radical inverse turns $i = (d_{m-1} \ldots d_1 d_0)_b$ into $0.d_0 d_1 \ldots d_{m-1}$ in base $b$, so consecutive indices alternate between halves, thirds and finer cells of $[0, 1)$; using a different prime in each coordinate makes the coordinates independent in the sense of Lemma 2 of the proof. The index starts at 1, which avoids the corner point $0$ where many transformed integrands are singular. The implementation also provides the exact star discrepancy in one dimension, $D_N^* = \frac{1}{2N} + \max_i |x_{(i)} - \frac{2i-1}{2N}|$, and in two dimensions by checking all $O(N^2)$ candidate corners with prefix sums.

## Example

The first six Halton points in bases 2 and 3 are $(\frac12, \frac13)$, $(\frac14, \frac23)$, $(\frac34, \frac19)$, $(\frac18, \frac49)$, $(\frac58, \frac79)$, $(\frac38, \frac29)$: each new point goes into the largest empty region, and any $2^a 3^b$ consecutive points put exactly one point into each box of size $2^{-a} \times 3^{-b}$.

For $f(x, y) = e^{x + y}$ on $[0, 1]^2$, with $I = (e - 1)^2$ and $\sigma(f) = 1.220$, the exact star discrepancy of the first $N$ Halton points is $0.0502$ for $N = 100$ and $0.0068$ for $N = 1000$, against $0.106$ and $0.0359$ for pseudo-random points (seed 1). Errors:

| $N$ | Monte Carlo RMS $\sigma/\sqrt{N}$ | Halton, deterministic | Halton with one random shift, RMS over 20 shifts |
|---|---|---|---|
| 256 | $7.6 \times 10^{-2}$ | $2.4 \times 10^{-2}$ | $1.1 \times 10^{-2}$ |
| 1024 | $3.8 \times 10^{-2}$ | $6.7 \times 10^{-3}$ | $3.0 \times 10^{-3}$ |
| 4096 | $1.9 \times 10^{-2}$ | $2.0 \times 10^{-3}$ | $7.4 \times 10^{-4}$ |

Quadrupling $N$ divides the Monte Carlo error by 2 and the QMC errors by about 3.5 to 4, close to the $N^{-1}$ rate with its logarithmic factor. The deterministic rule carries a bias of order $(\log N)^2/N$, which the random shift removes in expectation.

In [multidimensional integration](/multidimensional-integration/), on Sobol's test function with kinks, the first $N = 10^5$ Halton points give errors $6.4 \times 10^{-5}$ in $s = 5$ and $4.2 \times 10^{-4}$ in $s = 10$, against Monte Carlo RMS errors of $2.2 \times 10^{-3}$ and $3.5 \times 10^{-3}$.

## Correctness

The full proof is in the correctness file. Lemma 1 shows that lines L10 and L11 compute the radical inverse, and Lemma 2, by the Chinese remainder theorem, that any $\prod_k p_k^{m_k}$ consecutive Halton points meet every elementary box $\prod_k [j_k p_k^{-m_k}, (j_k + 1) p_k^{-m_k})$ exactly once. From this, Theorem 1 proves $N D_N^* \le (b - 1)(\lfloor \log_b N \rfloor + 1)$ for $N$ consecutive van der Corput points. Theorem 2 maps the box to the cube and applies the Koksma-Hlawka inequality: the deterministic error is at most $|V|\, V_{HK}(g)\, D_N^*$, which with Halton's bound (cited) is $O((\log N)^s/N)$ for $g$ of bounded Hardy-Krause variation. Theorem 3 proves that a uniform shift modulo 1 maps every point to a uniform point, so each shifted replicate is an unbiased estimate, and that the standard error of line L9 is an unbiased variance estimate for square-integrable $f$. The deterministic bound is a proved inequality; the error bar from replicates is probabilistic.

## Complexity

The algorithm makes $\max(R, 1)\, N$ evaluations of $f$. Each Halton point costs $O(s \log N)$ digit operations, or $O(s)$ amortized with an incremental digit counter; Sobol points cost $O(s)$ each with Gray code updates. Memory is $O(s)$ beyond the list kept for compensated summation, which could be replaced by a running sum. For $f$ with $V_{HK}(f) < \infty$, reaching error $\tau$ takes $N = O(\tau^{-1} (\log(1/\tau))^s)$ points by the Koksma-Hlawka bound, against $\sigma^2 \tau^{-2}$ for Monte Carlo; the bound is pessimistic in high dimension, and in practice the advantage depends on the effective dimension of $f$.

## Properties

- **Deterministic and extensible.** Without shifts the result is reproducible, and the sequence can be extended: $N$ can grow one point at a time and earlier values are kept.
- **Error decays like $(\log N)^s / N$** for integrands of bounded variation (proved bound), and for randomized nets with smooth integrands, the RMS error can reach $N^{-3/2}$ up to logarithmic factors (Owen's scrambling; cited).
- **No error estimate without randomization.** The Koksma-Hlawka bound is not computable in practice: $V_{HK}$ is unknown and $D_N^*$ is expensive in high dimension.
- **Equal weights.** Every point has weight $V/N$, so the rule is positive and stable.
- **Projections matter.** Halton points with large bases have poorly distributed low-dimensional projections for moderate $N$: in bases 29 and 31 the points with $i < 29$ are $(i/29, i/31)$, all on one line, and the first several hundred points lie on a few parallel lines.

## Variants and improvements

- **Sobol and Niederreiter sequences.** Digital $(t, s)$-sequences in base 2 have better uniformity in high dimension than Halton and are the default in finance; see [Sobol sequence](/sobol-sequence/).
- **Lattice rules.** Points $\{i z / N\}$ for a generating vector $z$, chosen component by component; for periodic smooth $f$ they converge like $N^{-\alpha}$ (Dick, Kuo and Sloan 2013, Section 5).
- **Randomization.** Random shifts (Cranley and Patterson 1976), random digital shifts, and Owen's nested scrambling give unbiased estimators with replicate-based error bars. Scrambled nets have variance $o(1/N)$ for every square-integrable $f$.
- **Leaping, skipping and dropping the first point.** Practical codes skip a prefix of the sequence or use only every $L$-th point; these are heuristics and can harm the uniformity of nets.
- **Effective dimension reduction.** Brownian bridge and principal component constructions of random paths put the important variation into the first coordinates, where QMC points are best.
- **Higher order nets.** Interlaced digital nets attain $O(N^{-\alpha} (\log N)^{s\alpha})$ for integrands with $\alpha$ smooth mixed derivatives (Dick).

## When to use it

- Moderate to high dimension ($s$ from about 5 to a few hundred) with integrands of bounded variation or low effective dimension: option pricing, Bayesian computation with reparametrized integrals, computer graphics.
- When reproducibility matters and a deterministic rule is wanted.
- With randomization, whenever Monte Carlo would be used and the integrand is not wildly irregular; the error bar comes from the replicates.
- Not in one or two dimensions with smooth integrands, where [Gauss rules](/gauss-legendre-quadrature/) or [product rules](/product-quadrature/) are far better, nor for integrands with discontinuities along oblique surfaces in high dimension, where the gain over Monte Carlo can vanish.

## Pitfalls

- **Treating QMC points as random.** The sample variance of $f(x_i)$ over QMC points is not an error estimate; use independent randomized replicates.
- **Large Halton bases.** In 20 or more dimensions, plain Halton points show strong correlations between coordinates with large primes for $N$ in the thousands; use scrambled Halton, Sobol or lattice points.
- **Infinite Hardy-Krause variation.** Indicators of non-rectangular sets and kinks along oblique planes have $V_{HK} = \infty$, so the Koksma-Hlawka bound says nothing; the observed rate then lies between $N^{-1/2}$ and $N^{-1}$ and moves toward the Monte Carlo rate as $s$ grows.
- **Unbounded integrands at the cube's boundary.** Transformations by the inverse normal distribution make $f$ unbounded near the faces; starting the sequence at the corner 0 can then give infinite values, and the variation is infinite.
- **Rounding of radical inverses.** For bases other than 2, points that should lie exactly on box edges may round to the other side; this changes nothing in integration, but exact tests of the box property need a tolerance or rational arithmetic.

## Implementations

## History

Number-theoretic integration began with Hermann Weyl's 1916 theory of uniform distribution and with Koksma's 1942 inequality. Johannes van der Corput constructed his sequence in 1935, John Halton generalized it to several dimensions in 1960, and Ilya Sobol introduced his $LP_\tau$ sequences in 1967. Nikolai Korobov and Edmund Hlawka introduced lattice rules around 1959 to 1962. Harald Niederreiter's theory of $(t, m, s)$-nets and $(t, s)$-sequences from 1987 unified the constructions, and his 1992 monograph is the standard reference. Paskov and Traub's 1995 report of QMC beating Monte Carlo on a 360-dimensional mortgage-backed security started its use in finance, and Sloan and Woźniakowski's weighted spaces (1998) explained why it works in high dimension. Cranley and Patterson (1976) and Owen (1995) introduced the randomizations that give error estimates.

## References
