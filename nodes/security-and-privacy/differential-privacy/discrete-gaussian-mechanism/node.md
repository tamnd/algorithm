---
tag: 70PG4J
kind: algorithm
slug: discrete-gaussian-mechanism
name: Discrete Gaussian mechanism
aliases:
- discrete Gaussian noise
- discrete Gaussian sampler
area: security-and-privacy/differential-privacy
level: research
summary: "Adds integer noise with mass proportional to exp(-y^2/(2 sigma^2)), drawn by an exact sampler with only random integers and rational arithmetic, which avoids the flaws of float noise."
model: word-ram
complexity:
  vars: {b: the number of bits of sigma^2 and of the output}
  time: {expected: O(1)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, exact: true}
history:
  year: 2020
  people: [Clement L. Canonne, Gautam Kamath, Thomas Steinke]
  note: "Canonne, Kamath and Steinke analyzed the discrete Gaussian for differential privacy and gave an exact sampler without floating point arithmetic (NeurIPS 2020). The distribution was used earlier in lattice-based cryptography."
prereqs: [gaussian-mechanism, geometric-mechanism, rejection-sampling, zero-concentrated-differential-privacy]
see_also: [laplace-mechanism, gaussian-sampling-over-lattices, bernoulli-sampling, floating-point-arithmetic, ieee-754, privacy-loss-random-variable, renyi-differential-privacy, geometric-distribution]
sources:
  - url: "https://arxiv.org/abs/2004.00010"
    title: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020, arXiv 2004.00010"
    locator: "Definition 1 (discrete Gaussian), Theorem 4 (zCDP), Proposition 5 and Lemma 6 (Renyi divergence), Theorem 7 (tight (epsilon, delta)), Corollary 17 (variance), Section 5 (Algorithms 1, 2 and 3, Propositions 33 and 34, Theorem 32)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: "the weakness of floating point implementations of noise and the snapping mechanism as a fix"
  - paper: doi:10.1007/978-3-662-53641-4_24
    title: "Mark Bun and Thomas Steinke, Concentrated differential privacy: simplifications, extensions, and lower bounds, TCC 2016-B, LNCS 9985, pages 635 to 658"
    locator: "Definition 1.1 (zCDP) and Proposition 1.3 (conversion to approximate DP)"
---

The discrete Gaussian mechanism answers an integer-valued query $f$ by releasing $f(x) + Y$, where the noise $Y$ is an integer with $\Pr[Y = y]$ proportional to $e^{-y^2/(2\sigma^2)}$. This distribution, written $N_{\mathbb Z}(0, \sigma^2)$, is the discrete Gaussian. It gives the same privacy as the continuous [Gaussian mechanism](/gaussian-mechanism/): for sensitivity $\Delta$ it is $\Delta^2/(2\sigma^2)$-[zCDP](/zero-concentrated-differential-privacy/). Its main value is that it can be sampled *exactly* with only uniform random integers and rational arithmetic, with no floating point numbers, no $\exp$ and no square root. Mironov showed in 2012 that float implementations of continuous noise can leak through the low-order bits of their outputs. An exact integer sampler removes that whole class of problems. Canonne, Kamath and Steinke gave the analysis and the sampler in 2020. The same distribution is central in lattice-based cryptography, where it is sampled for a different purpose (see [Gaussian sampling over lattices](/gaussian-sampling-over-lattices/)).

## In plain words

To hide one person's effect on a count, we add a random whole number to it. Small numbers near zero are likely, and large ones are rare, in the bell shape of the normal curve. This gives the same protection as normal noise with fractions.

The important part is how the random number is drawn. A computer that draws a fraction with limited precision can leave traces in the last digits that point to the true answer. This method draws only whole numbers, by a series of fair choices and exact fractions, so the result has exactly the intended distribution. It needs a few rounds on average.

## The problem

Input: the true answer $v = f(x) \in \mathbb Z$ of a query with integer values and sensitivity $\Delta \in \mathbb Z_{\ge 1}$, and a rational $\sigma^2 > 0$. Output: $v + Y$ with $Y \sim N_{\mathbb Z}(0, \sigma^2)$, where

$$\Pr[Y = y] = \frac{e^{-y^2/(2\sigma^2)}}{\sum_{z \in \mathbb Z} e^{-z^2/(2\sigma^2)}}, \qquad y \in \mathbb Z.$$

The output law must be exact, given a source of uniform random integers, and the computation must use only exact integer and rational arithmetic. The model is the word RAM.

## The algorithm

```pseudo id=main
DISCRETE-GAUSSIAN-MECHANISM(v, sigma2)            ▷ v = f(x) in Z, sigma2 > 0 rational
L1  t <- floor(sqrt(sigma2)) + 1                 ▷ the least integer with t^2 > sigma2
L2  loop
L3      Y <- DISCRETE-LAPLACE(t)                 ▷ Pr[Y = y] proportional to exp(-|y|/t)
L4      gamma <- (|Y| - sigma2/t)^2 / (2 sigma2)
L5      C <- BERNOULLI-EXP(gamma)                ▷ 1 with probability exp(-gamma)
L6      if C = 1 then return v + Y
```

Line L1 picks the scale of a discrete Laplace proposal. It is computed without a square root, as the least integer $t$ with $t^2 > \sigma^2$. Lines L2 to L6 are [rejection sampling](/rejection-sampling/): line L3 proposes $Y$ from the discrete Laplace distribution, and lines L4 and L5 accept it with probability $e^{-\gamma}$. The product of the two weights is $e^{-|y|/t - \gamma} = e^{-y^2/(2\sigma^2)} \cdot e^{-\sigma^2/(2t^2)}$, where the second factor does not depend on $y$. So an accepted $Y$ has exactly the discrete Gaussian law. Each round accepts with probability above $0.29$.

The two subroutines are Algorithms 1 and 2 of Canonne, Kamath and Steinke.

- **BERNOULLI-EXP($\gamma$)** returns 1 with probability $e^{-\gamma}$ for rational $\gamma \ge 0$. For $\gamma \le 1$: set $K = 1$, and while a draw from Bernoulli$(\gamma/K)$ is 1, increase $K$; return 1 if $K$ is odd. The probability that $K$ is odd is $\sum_j (-\gamma)^j/j! = e^{-\gamma}$. For $\gamma > 1$: run the case $\gamma = 1$ up to $\lfloor\gamma\rfloor$ times and return 0 at the first 0; then return BERNOULLI-EXP$(\gamma - \lfloor\gamma\rfloor)$. A Bernoulli$(n/d)$ draw is "a uniform integer in $\{0, \ldots, d-1\}$ is below $n$".
- **DISCRETE-LAPLACE($t$)** draws $U$ uniform in $\{0, \ldots, t-1\}$ and keeps it with probability $e^{-U/t}$; draws $V \ge 0$ by counting 1s from BERNOULLI-EXP$(1)$ until the first 0; sets $X = U + tV$, which is geometric with ratio $e^{-1/t}$; draws a fair sign; starts again if the sign is negative and $X = 0$; and returns the signed $X$.

The tests of the code on this site pass a seeded generator so that each run repeats. A deployment must use a cryptographic source of randomness, such as the operating system generator, and must keep the exact arithmetic (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Example

Let $v = 10$ and $\sigma^2 = 4$. Line L1 gives $t = 3$, since $2^2 = 4$ is not above $\sigma^2$ but $3^2 = 9$ is. Suppose that the proposals are $Y = -5$ and then $Y = 2$, and that the Bernoulli draws are 0 and then 1.

| round | $Y$ (L3) | $\gamma$ (L4) | $e^{-\gamma}$ | $C$ (L5) | action (L6) |
|---|---|---|---|---|---|
| 1 | $-5$ | $(5 - 4/3)^2/8 = 121/72$ | 0.1863 | 0 | reject, go to L3 |
| 2 | 2 | $(2 - 4/3)^2/8 = 1/18$ | 0.9460 | 1 | return $10 + 2 = 12$ |

A proposal of $Y = 0$ would get $\gamma = (4/3)^2/8 = 2/9$. The exact probabilities of the output noise are $\Pr[Y = 0] = 0.199471$, $\Pr[Y = \pm 1] = 0.176033$ and $\Pr[Y = \pm 2] = 0.120985$, and its variance agrees with $\sigma^2 = 4$ to about 15 digits, from below.

For a count with $\Delta = 1$, this release is $1/8$-zCDP. Theorem 7 of Canonne, Kamath and Steinke gives the exact $\delta$ at $\varepsilon = 1$: $\delta = 0.0072488$. The continuous Gaussian with $\sigma = 2$ has $\delta = 0.0068296$ at the same $\varepsilon$, so the discrete version is almost the same.

## Correctness

**Theorem (Canonne, Kamath and Steinke).** Given a perfect source of uniform random integers, DISCRETE-GAUSSIAN-MECHANISM stops with probability 1 and returns $v + Y$ with $Y \sim N_{\mathbb Z}(0, \sigma^2)$ exactly. If $f$ has sensitivity $\Delta$, the mechanism is $\Delta^2/(2\sigma^2)$-zCDP, and its tight $(\varepsilon, \delta)$ curve is
$$\delta(\varepsilon) = \Pr\left[Y > \frac{\varepsilon\sigma^2}{\Delta} - \frac{\Delta}{2}\right] - e^{\varepsilon}\Pr\left[Y > \frac{\varepsilon\sigma^2}{\Delta} + \frac{\Delta}{2}\right].$$

The proof in [proofs/correctness.md](proofs/correctness.md) checks the two subroutines, then the rejection step of lines L4 and L5, and then the privacy claim. For privacy, completing the square gives
$$D_\alpha(N_{\mathbb Z}(\mu, \sigma^2)\|N_{\mathbb Z}(0, \sigma^2)) = \frac{\alpha\mu^2}{2\sigma^2} + \frac{1}{\alpha - 1}\ln\frac{\sum_y e^{-(y - \alpha\mu)^2/(2\sigma^2)}}{\sum_y e^{-y^2/(2\sigma^2)}},$$
and the Poisson summation formula shows that the last ratio is at most 1. It equals 1 when $\alpha\mu$ is an integer.

## Complexity

In the word RAM with rationals of $O(b)$ bits, the expected cost is $O(1)$ arithmetic operations (Canonne, Kamath and Steinke, Theorem 32). Each round of lines L2 to L6 accepts with probability above $0.29$, so the expected number of rounds is below $3.5$. A call of DISCRETE-LAPLACE succeeds in each of its rounds with probability at least $(1 - e^{-1})/2$, and the counting loop for $V$ runs about $0.58$ times on average. BERNOULLI-EXP$(\gamma)$ for $\gamma \le 1$ makes at most $e$ draws on average, and for larger $\gamma$ it stops at the first 0 from Bernoulli$(e^{-1})$. Extra space is $O(1)$ numbers. The run time depends on the noise drawn, so it is not constant.

## Properties

- **Exact.** The output law is exactly $v + N_{\mathbb Z}(0, \sigma^2)$, not an approximation, if the random integers are uniform.
- **Same privacy as the continuous Gaussian.** $\Delta^2/(2\sigma^2)$-zCDP, the same as Proposition 1.6 of Bun and Steinke for continuous noise. The $\delta$ for a given $\varepsilon$ is close to the continuous one, and slightly larger for small $\sigma$.
- **Variance at most $\sigma^2$** (Corollary 17 of Canonne, Kamath and Steinke), and very close to $\sigma^2$ once $\sigma \ge 1$.
- **Integer output.** Counts stay integers; no rounding step is needed.

## Variants and improvements

- **Vectors.** For a query with values in $\mathbb Z^d$, add independent discrete Gaussian noise to each coordinate. The privacy depends on the $\ell_2$ sensitivity, as for the continuous mechanism.
- **Discrete Laplace.** The subroutine DISCRETE-LAPLACE is on its own a pure DP mechanism for integer queries, the two-sided [geometric mechanism](/geometric-mechanism/), with exact sampling.
- **Snapping.** Mironov's snapping mechanism keeps float Laplace noise but rounds and clamps the output, which also defends against the low-bit leak.
- **Other samplers.** Samplers from lattice cryptography (for example table-based and constant-time samplers) also draw discrete Gaussians; they target other trade-offs, such as constant run time.

## When to use it

Use the discrete Gaussian mechanism for integer queries, such as counts and histograms, when the accounting is in zCDP or Renyi DP and the release needs a sampler that is provably exact. It is the natural replacement for float Gaussian noise in production systems. For pure $\varepsilon$-DP use discrete Laplace noise instead.

## Pitfalls

- **Floats at lines L4 and L5.** Computing $e^{-\gamma}$ in floating point and comparing it with a float uniform brings back the rounding errors that the method exists to remove. Keep $\gamma$ a rational and use BERNOULLI-EXP.
- **A seeded generator at line L3.** The exact algorithm is only as good as its random integers. A seeded pseudorandom generator is fine for tests and wrong for a release; use a cryptographic source.
- **Run time at line L2.** The number of rounds, and the work inside BERNOULLI-EXP, depend on the noise value. If an observer can time the release, the time can leak information about the noise. A deployment that exposes timing should hide it, for example by drawing the noise ahead of time, away from the request path.
- **Wrong scale at line L1.** Computing $t$ with a float square root can be off by one for large $\sigma^2$. Any positive integer $t$ keeps the output exact, but a poor $t$ makes the loop slow; use the integer test $t^2 > \sigma^2$.
- **Sensitivity in the wrong norm.** The zCDP bound uses the $\ell_2$ sensitivity, and for a single integer query it must be an integer bound on $|f(x) - f(x')|$.

## Implementations

## History

The discrete Gaussian has long been used in lattice-based cryptography, where it is the noise of many schemes and of trapdoor sampling. In differential privacy, Mironov (2012) showed that float implementations of the Laplace mechanism can leak through the low-order bits of their outputs, and proposed the snapping mechanism. Canonne, Kamath and Steinke (NeurIPS 2020) analyzed the discrete Gaussian as a privacy mechanism, showed that it matches the continuous Gaussian under zCDP, gave its exact $(\varepsilon, \delta)$ curve, and gave the exact sampler of this page. The US Census Bureau used discrete Gaussian noise with zCDP accounting in the disclosure avoidance system of the 2020 Census.

## References
