---
tag: JHRGEV
kind: problem
slug: random-variate-generation
name: Random variate generation
aliases:
- non-uniform random number generation
- non-uniform random variate generation
- sampling from a distribution
area: randomized/sampling
level: intro
summary: Produce samples from a prescribed probability distribution using uniform random numbers or random bits.
prereqs: [probability-distribution, random-variable, uniform-distribution]
see_also: [random-sampling, weighted-sampling, inverse-transform-sampling, rejection-sampling, ratio-of-uniforms, alias-method, ziggurat-method, box-muller-transform]
sources:
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter I, Section 1 (the model of exact uniforms and exact real arithmetic), Chapter II (inversion, rejection, composition), Chapters III to IX (discrete, table and specific methods), Chapter VII, Section 2 (log-concave densities), Chapter XV (the random bit model)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition, Addison-Wesley, 1997
    locator: Section 3.4.1 (numerical distributions)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in J. F. Traub (editor), Algorithms and Complexity: New Directions and Recent Results, Academic Press, 1976"
    locator: pages 357 to 428
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951"
    locator: pages 36 to 38
  - paper: "Wolfgang Hörmann, Josef Leydold and Gerhard Derflinger, Automatic Nonuniform Random Variate Generation, Springer, 2004"
    locator: Chapter 4 (transformed density rejection)
---

Random variate generation is the problem of producing a random variable $X$ with a prescribed distribution $F$ from a source of uniform randomness. The distribution can be given by its cumulative distribution function, its density or mass function (possibly only up to a constant), a list of probabilities, or a description such as "the sum of two independent normals". The standard model, used by Devroye (1986), assumes independent exact uniforms on $[0, 1]$, exact real arithmetic, and unit-cost evaluation of elementary functions; the random bit model counts fair coin flips instead. The answers are general methods (inversion, rejection, composition, transformations, ratio-of-uniforms, tables) and specific algorithms for each family, compared by their expected time, the number of uniforms or bits they use, their setup cost and memory, and how exact they stay in floating-point arithmetic. This page states the problem and maps the methods; [random sampling](/random-sampling/) is the wider map that also covers sampling from finite populations and streams.

## In plain words

A computer can produce random numbers that are spread evenly between 0 and 1, or random bits. Most uses need something else: waiting times that are mostly short but sometimes long, heights that cluster around a mean, or a die with unequal faces.

Random variate generation is the craft of turning even random numbers into numbers with the shape you want. Sometimes a formula does it: stretch the even numbers with the inverse of the distribution function. Sometimes it is easier to propose a value from a simpler shape and keep it only with the right probability. Sometimes a table built once makes each later draw very fast.

The questions are how fast each draw is, how many random numbers it uses, how much setup it needs, and whether the output has exactly the right law.

## Definition

**Input.** A distribution $F$ on $\mathbb{R}$, $\mathbb{R}^d$ or a countable set, given by one or more of: the cumulative distribution function $F$ or its inverse, the density or mass function $f$ (possibly as $\tilde f = c f$ with unknown $c$), a finite list of probabilities, or a construction from other distributions. Parameters of $F$ can change from one call to the next.

**Randomness.** In the real RAM model of Devroye's Chapter I, a source of independent uniforms on $[0, 1]$, exact arithmetic on reals, and elementary functions ($\exp$, $\log$, $\sin$ and others) in constant time. In the random bit model, a source of independent fair bits, with the cost counted in bits. In practice, a [pseudorandom number generator](/pseudorandom-number-generator/) and floating-point arithmetic stand in for both.

**Output.** A random variable $X$ with $\Pr[X \le x] = F(x)$ for all $x$, and independent outputs on independent calls. An approximate method guarantees only that the law of $X$ is close to $F$ in some distance.

**Costs.** The expected time per variate, the expected number of uniforms or bits per variate, the setup time and the memory of tables, the set of distributions the method covers, and the size of the error when real arithmetic is replaced by floating point.

## Variants

- **Discrete with finite support.** This is [weighted sampling](/weighted-sampling/) with replacement.
- **Discrete with infinite support.** Poisson, geometric, binomial with large $n$. Sequential search, inversion by tables, and rejection from continuous envelopes.
- **Continuous univariate.** The exponential, normal, gamma and beta families, and densities given by a formula.
- **Universal or automatic methods.** The method receives only $f$ and some properties, such as log-concavity or the mode, and builds its own envelope: [adaptive rejection sampling](/adaptive-rejection-sampling/), transformed density rejection, and Devroye's black-box methods for log-concave densities.
- **Multivariate.** Multivariate normals by a Cholesky factor, distributions by conditional densities (a chain of univariate draws), uniform points in a set by rejection.
- **Random objects.** [Random permutations](/random-permutation/), random subsets and random samples from finite populations. See [random sampling](/random-sampling/).
- **Approximate generation.** When no exact method is practical, [Markov chain Monte Carlo](/metropolis-hastings/) produces a sequence whose law converges to $F$.
- **Random bit model.** Exact generation from fair bits with the fewest bits, after Knuth and Yao (1976). See [unbiased bits from a biased coin](/unbiased-bits-from-biased-coin/) for the inverse problem.

## Examples

**Exponential by inversion.** $F(x) = 1 - e^{-x}$, so $X = -\ln(1 - U)$. For $U = 0.3$, $X = 0.3567$. Since $1 - U$ is also uniform, $X = -\ln U$ works too, and gives $1.2040$ for the same $U$.

**Poisson by sequential inversion.** For mean $\lambda = 3$, add up $\Pr[X = 0], \Pr[X = 1], \ldots$ until the sum exceeds $U$. For $U = 0.6$, the sums are $0.0498, 0.1991, 0.4232, 0.6472$, so $X = 3$. The search stops after $X + 1$ steps, so it takes $\lambda + 1$ steps on average.

**Four ways to a standard normal.**

| method | page | uniforms per normal | note |
|---|---|---|---|
| Box-Muller | [Box-Muller transform](/box-muller-transform/) | 1 | two normals from two uniforms, with $\log$, $\sqrt{\ }$, $\cos$ and $\sin$ |
| polar method | [Marsaglia polar method](/marsaglia-polar-method/) | $4/\pi \approx 1.273$ | two normals per accepted pair; no trigonometric functions |
| ratio-of-uniforms | [ratio-of-uniforms](/ratio-of-uniforms/) | $2 \cdot 1.369 = 2.74$ | acceptance $\sqrt{\pi e}/4 \approx 0.7306$ |
| ziggurat | [ziggurat method](/ziggurat-method/) | about 1 random word | $1.012$ tries per normal with 128 layers; a table of 128 entries |

Rejection from the two-sided exponential density (the Laplace density) also works, with an envelope constant $\sqrt{2e/\pi} \approx 1.3155$; see [rejection sampling](/rejection-sampling/).

## Known algorithms

The general methods, in the order of Devroye's Chapter II and later chapters:

- **[Inversion](/inverse-transform-sampling/).** $X = F^{-1}(U)$ with the generalized inverse. One uniform per variate, monotone in $U$, which suits common random numbers and [quasi-Monte Carlo](/quasi-monte-carlo-integration/). Needs $F^{-1}$ in closed form, or a numerical root finder.
- **[Rejection](/rejection-sampling/).** Propose from $g$ with $f \le M g$ and accept with probability $f/(Mg)$; $M$ tries on average. A squeeze, a cheap lower bound on $f$, avoids most evaluations of $f$. Works with unnormalized $f$.
- **Composition.** If $f = \sum_j p_j f_j$, pick $j$ by [weighted sampling](/weighted-sampling/), then draw from $f_j$.
- **Transformations.** Use a known relation: [Box-Muller](/box-muller-transform/) and the [polar method](/marsaglia-polar-method/) for normals, sums of exponentials for the gamma with integer shape, ratios of gammas for the beta.
- **[Ratio-of-uniforms](/ratio-of-uniforms/).** A uniform point in a bounded region gives $X = V/U$ with density proportional to $h$.
- **Table methods.** The [alias method](/alias-method/) and guide tables for discrete laws; the [ziggurat method](/ziggurat-method/) for monotone and symmetric densities.
- **Methods for log-concave densities.** [Adaptive rejection sampling](/adaptive-rejection-sampling/) and transformed density rejection build piecewise exponential envelopes from tangents. Devroye's Chapter VII, Section 2 gives rejection algorithms with a uniformly bounded expected number of tries for all log-concave densities with a known mode.
- **The Gumbel-max trick.** Discrete laws given by log-weights; see the [Gumbel-max trick](/gumbel-max-trick/).
- **The Knuth-Yao DDG tree.** Optimal in the random bit model for discrete laws.

## Bounds

**One uniform is enough in the real RAM.** Every univariate law can be generated from one uniform by inversion, if $F^{-1}$ can be evaluated. With exact reals, one uniform even carries infinitely many independent uniforms in its digits, so the number of uniforms is a useful cost only together with the set of allowed operations.

**Random bits.** Knuth and Yao (1976) proved that every exact generator of a discrete law $p$ from fair bits uses at least the [entropy](/shannon-entropy/) $H(p)$ bits on average, and that an optimal generator uses fewer than $H(p) + 2$. A law with a continuous part cannot be output exactly with finitely many bits; the random bit model then asks for the first $k$ bits of $X$, or for $X$ rounded to a grid.

**Rejection.** A rejection method with constant $M$ uses a geometric number of tries with mean $M$, and $M \ge 1$, with equality only when $f = g$. The expected time is bounded uniformly over a family only if $M$ is.

**Universal methods.** Devroye's Chapter VII, Section 2 shows that a bounded expected time is possible for the whole class of log-concave densities with a known mode. Some such condition is needed. For a general density known only through evaluations of $f$, no exact method exists at all: a narrow spike that holds half of the mass can sit where the method evaluates $f$ with tiny probability, and then the method cannot put half of its output there.

## Reductions

- **[Weighted sampling](/weighted-sampling/)** is the discrete finite case.
- **Uniforms from bits.** A uniform on $[0, 1]$ to $b$ bits is $b$ fair bits; a uniform integer in $\{0, \ldots, m - 1\}$ is made from bits by rejection.
- **To [Monte Carlo integration](/monte-carlo-integration/).** Estimating $\mathbb{E}[g(X)]$ by averaging $g$ over generated variates. [Importance sampling](/importance-sampling/) changes the law that is generated and weights the result.
- **From Markov chains.** When exact generation is too hard, [Metropolis-Hastings](/metropolis-hastings/) and [Gibbs sampling](/gibbs-sampling/) generate approximately, at the cost of correlated outputs and a burn-in.
- **From the pseudorandom source.** All the methods assume independent uniforms. The quality of the [pseudorandom number generator](/pseudorandom-number-generator/) limits the quality of the variates; some methods, such as the ziggurat with shared bits, are more sensitive to it than others.

## Applications

- Stochastic simulation in physics, finance, queueing and reliability.
- [Monte Carlo integration](/monte-carlo-integration/), [importance sampling](/importance-sampling/) and [sequential Monte Carlo](/sequential-monte-carlo/).
- Randomized algorithms that need non-uniform choices, such as [randomized rounding](/randomized-rounding/) with biased coins.
- Machine learning: noise for training and data augmentation, and the reparameterization $X = \mu + \sigma Z$ used to train a [variational autoencoder](/variational-autoencoder/).
- Statistics: bootstrap resampling, permutation tests and Bayesian computation.

## References
