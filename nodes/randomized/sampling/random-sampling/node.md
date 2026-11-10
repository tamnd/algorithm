---
tag: G9Q1TB
kind: concept
slug: random-sampling
name: Random sampling
aliases:
- sampling
- probability sampling
area: randomized/sampling
level: intro
summary: Drawing elements from a population, a stream or a distribution by a random procedure, so that each candidate has a known inclusion probability.
prereqs: [probability-distribution, expected-value, indicator-random-variable]
see_also: [random-variate-generation, weighted-sampling, uniform-random-subset, reservoir-sampling, bernoulli-sampling, probability-proportional-to-size-sampling, stratified-sampling, importance-sampling]
sources:
  - book: isbn:9780387975283
    title: Carl-Erik Särndal, Bengt Swensson and Jan Wretman, Model Assisted Survey Sampling, Springer, 1992
    locator: Chapter 2 (sampling designs, inclusion probabilities and the pi estimator) and Chapter 3 (Bernoulli, simple random, systematic and pi-ps designs)
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Chapter 1 (the purpose of sampling and the principal steps), Chapter 2 (simple random sampling)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition, Addison-Wesley, 1997
    locator: Section 3.4.2 (random sampling and shuffling)
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter XII (random sampling)
  - paper: doi:10.1080/01621459.1952.10483446
    title: D. G. Horvitz and D. J. Thompson, A generalization of sampling without replacement from a finite universe, Journal of the American Statistical Association 47(260), 1952
    locator: pages 663 to 685
---

Random sampling is the selection of elements from a population by a random procedure whose probabilities are known in advance. The population can be a finite list (pick $n$ of $N$ records), a stream whose length is not known (keep a sample of what has passed), or a probability distribution (produce values with a given law). What makes a sample random in this sense is not that it looks mixed, but that the procedure assigns a known probability to every possible sample, and in particular a known inclusion probability $\pi_i > 0$ to every element. These probabilities are what allow unbiased estimates of population quantities, such as the Horvitz-Thompson estimate $\sum_{i \in S} y_i/\pi_i$ of a total, and what allow error bounds. This page is the map: it names the main settings and sends each one to its own pages. Generating values from a given distribution is the problem of [random variate generation](/random-variate-generation/), and choosing indices by weight is [weighted sampling](/weighted-sampling/).

## In plain words

To learn about a large group, you look at a small part of it. If you choose that part by convenience, for example the first hundred rows or the people who answer, the part can differ from the whole in ways you cannot measure.

Random sampling lets chance choose instead, by a rule that you know. Because you know how likely each item was to be chosen, you can correct for it, and you can say how far off your answer is likely to be.

The same idea appears in many forms: a fair draw of names from a hat, a draw where big items are more likely, a sample kept while data streams past, or random numbers that follow a bell curve.

## The idea

**Designs and inclusion probabilities.** For a finite population $U = \{1, \ldots, N\}$, a sampling design is a probability distribution $p(S)$ over subsets $S \subseteq U$ (or over sequences, when repeats are allowed). The first-order inclusion probability is $\pi_i = \Pr[i \in S]$, and the second-order one is $\pi_{ij} = \Pr[i, j \in S]$. A design is a probability sample when every $\pi_i$ is known and positive. Then for any values $y_i$, the Horvitz-Thompson estimate $\hat Y = \sum_{i \in S} y_i/\pi_i$ has mean $Y = \sum_i y_i$, because $\mathbb{E}[\hat Y] = \sum_i \pi_i\,y_i/\pi_i$ by [linearity of expectation](/linearity-of-expectation/). The proof and the variance are on the [PPS sampling](/probability-proportional-to-size-sampling/) page. The variance depends on the whole design, not only on the $\pi_i$, as the examples below show.

**The main choices.**

- *With or without replacement.* Independent draws are simpler to analyze; distinct elements carry more information for the same size.
- *Equal or unequal probabilities.* Equal $\pi_i$ treat all elements alike; probabilities proportional to a size measure reduce the variance when the measured value grows with the size.
- *Fixed or random size.* Bernoulli and Poisson designs decide for each element independently, so the size is random but the algorithm is trivial and works on a stream.
- *Offline, sequential or streaming.* Whether $N$ is known, whether the data can be read twice, and how much memory is allowed.
- *Exact or approximate.* Most methods below give the stated law exactly with integer arithmetic or in exact real arithmetic. Markov chain methods give it only in the limit.

**The map of methods.**

| setting | methods |
|---|---|
| $n$ of $N$, equal probability, $N$ known | [uniform random subset](/uniform-random-subset/), [Floyd's sampling](/floyd-sampling/), [selection sampling](/selection-sampling/) (Knuth's Algorithm S), a partial [Fisher-Yates shuffle](/fisher-yates-shuffle/) |
| equal probability, random size | [Bernoulli sampling](/bernoulli-sampling/), with geometric skips |
| structured designs | [systematic sampling](/systematic-sampling/), [stratified sampling](/stratified-sampling/), [Latin hypercube sampling](/latin-hypercube-sampling/) |
| a stream of unknown length | [reservoir sampling](/reservoir-sampling/), [Algorithm L](/algorithm-l/), [Vitter's skips](/vitter-reservoir-skip/), [stream sampling](/stream-sampling/) |
| unequal probability, with replacement | [weighted sampling](/weighted-sampling/), the [alias method](/alias-method/), discrete [inversion](/inverse-transform-sampling/), the [Gumbel-max trick](/gumbel-max-trick/) |
| unequal probability, without replacement | [PPS sampling](/probability-proportional-to-size-sampling/), [weighted reservoir sampling](/weighted-reservoir-sampling/), [priority sampling](/priority-sampling/), Gumbel top-k |
| a continuous or discrete distribution | [random variate generation](/random-variate-generation/): [inversion](/inverse-transform-sampling/), [rejection](/rejection-sampling/), [adaptive rejection](/adaptive-rejection-sampling/), [ratio-of-uniforms](/ratio-of-uniforms/), [Box-Muller](/box-muller-transform/), the [polar method](/marsaglia-polar-method/), the [ziggurat](/ziggurat-method/) |
| estimates rather than samples | [importance sampling](/importance-sampling/), [Monte Carlo integration](/monte-carlo-integration/), the [Karp-Luby estimator](/karp-luby-estimator/) |
| hard distributions, approximately | [Metropolis-Hastings](/metropolis-hastings/), [Gibbs sampling](/gibbs-sampling/), [sequential Monte Carlo](/sequential-monte-carlo/) |

**Sampling and counting.** For many combinatorial sets, sampling an element almost uniformly and counting the elements approximately are equally hard; see the [Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/). This is one reason why random sampling is a tool of algorithm design, not only of statistics.

**The random source.** Every method above assumes independent uniform numbers or bits. In practice these come from a [pseudorandom number generator](/pseudorandom-number-generator/), and floating-point arithmetic replaces exact reals. The method pages say where exactness needs exact arithmetic and give integer forms where they exist.

## Examples

**Same inclusion probabilities, different designs.** Take $N = 6$ elements with $y = (1, 2, 3, 4, 5, 6)$ and total $Y = 21$, and three designs with $\pi_i = 1/3$ for every element. The Horvitz-Thompson estimate is $3\sum_{i \in S} y_i$ in each case, and it has mean 21 in each case.

| design | samples | size | variance of the estimate |
|---|---|---|---|
| simple random sampling of 2 | all 15 pairs, each with probability $1/15$ | 2 | 42 |
| systematic, interval 3 | $\{1, 4\}, \{2, 5\}, \{3, 6\}$, each with probability $1/3$ | 2 | 24 |
| Bernoulli with $p = 1/3$ | every subset; one of size $k$ has probability $(1/3)^{k}(2/3)^{6-k}$ | random, 2 on average | 182 |

The systematic estimates are $15, 21, 27$. Here the list is sorted by $y$, so every systematic sample takes one small and one large value, and the variance is lowest. The Bernoulli sample has size exactly 2 with probability only $0.329$, and the random size adds most of its variance: the variance is $\sum_i y_i^2(1 - \pi_i)/\pi_i = 2 \cdot 91 = 182$.

**A convenience sample.** Taking the first two elements of the list always gives the estimate $3(1 + 2) = 9$. It has no variance at all, and it is wrong by 12. No formula can detect this from the sample alone, because the inclusion probabilities of the procedure (1 for the first two elements and 0 for the rest) do not match the ones that the estimate assumes.

**Sampling from a distribution.** To sample the standard exponential law, take $X = -\ln U$ with $U$ uniform on $(0, 1]$; for $U = 0.3$, $X = 1.2040$. This is [inversion](/inverse-transform-sampling/), the simplest method of [random variate generation](/random-variate-generation/).

## Where it is used

- **Surveys and official statistics.** Probability samples of households, firms or farms, with stratified, cluster, systematic and PPS designs.
- **Databases and data systems.** Approximate query answers from Bernoulli or reservoir samples of tables and streams, and sampling for query optimizer statistics.
- **Algorithms.** Random samples as pivots and splitters in [randomized algorithms](/randomized-algorithm/), estimation in [Monte Carlo algorithms](/monte-carlo-algorithm/), and approximate counting.
- **Simulation and numerical integration.** Random variates drive [Monte Carlo integration](/monte-carlo-integration/), [importance sampling](/importance-sampling/) and stochastic simulation.
- **Machine learning.** Minibatches for stochastic gradient descent, bootstrap samples, sampling from a model's predicted distribution, and the resampling steps of [particle filters](/particle-filter/).
- **Auditing and quality control.** Samples of transactions or items with known probabilities, so that error rates can be estimated with stated confidence.

## References
