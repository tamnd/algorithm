---
tag: QJE5NA
kind: concept
slug: roulette-wheel-selection
name: Roulette wheel selection
aliases:
- fitness-proportionate selection
- fitness proportional selection
- proportional selection
area: optimization/metaheuristics
level: intro
summary: Select individual i with probability f_i divided by the sum of all fitness values. It needs fitness values of at least 0, and it is not invariant when you add a constant to them.
prereqs: [evolutionary-computation]
see_also: [tournament-selection, genetic-algorithm, schema-theorem, weighted-sampling, alias-method, systematic-sampling, premature-convergence]
sources:
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 1 (reproduction with a weighted roulette wheel) and Chapter 4 (fitness scaling)
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992
    locator: Chapter 6 (reproductive plans in which the offspring count is proportional to the observed fitness)
  - paper: James E. Baker, Reducing bias and inefficiency in the selection algorithm, Proceedings of the Second International Conference on Genetic Algorithms, 1987
    title: Reducing bias and inefficiency in the selection algorithm
    locator: pages 14 to 21 (stochastic universal sampling)
  - paper: doi:10.1162/evco.1996.4.4.361
    title: Tobias Blickle and Lothar Thiele, A comparison of selection schemes used in evolutionary algorithms, Evolutionary Computation 4(4), 1996
    locator: pages 361 to 394 (proportional, tournament, truncation and ranking selection compared by fitness distributions)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Section 5.2, Parent selection (fitness proportional selection, ranking selection and sampling algorithms)
---

Roulette wheel selection picks individual $i$ of a population with probability $f_i / \sum_j f_j$, where $f_j \ge 0$ is the fitness of individual $j$. It is the selection step of Holland's [genetic algorithm](/genetic-algorithm/) and the one that the [schema theorem](/schema-theorem/) assumes. In expectation, each individual gets $f_i / \bar f$ copies, where $\bar f$ is the mean fitness, so the result depends on the scale and on the zero point of $f$.

## In plain words

Draw a wheel and cut it into one slice per individual. Make the slice of each individual as wide as its fitness. Spin the wheel and take the individual where it stops. An individual with twice the fitness of another is picked twice as often.

The method needs fitness values that are zero or more. It also reacts to the size of the values, not only to their order. If all values are large and close together, the slices are almost equal, and good individuals get almost no advantage. If one value is much larger than the others, that individual fills the next group fast. Programs often change the values first, by scaling or by ranks, to control this.

## The idea

Let the population have $N$ individuals with fitness $f_1, \ldots, f_N \ge 0$ and $F = \sum_j f_j > 0$. One spin draws $u$ uniformly from $[0, 1)$ and returns the index $i$ with
$$c_{i-1} \le u F < c_i, \qquad c_i = f_1 + \cdots + f_i, \quad c_0 = 0.$$
The interval of $i$ has length $f_i$ out of $F$, so
$$\Pr[\text{pick } i] = p_i = \frac{f_i}{F}.$$
This is [inverse transform sampling](/inverse-transform-sampling/) of a discrete distribution, and a [binary search](/binary-search/) on the prefix sums $c_i$ finds $i$ in $O(\log N)$ time after $O(N)$ preparation. The [alias method](/alias-method/) gives $O(1)$ time per spin after $O(N)$ preparation. A linear scan costs $O(N)$ per spin.

**Expected copies.** With $N$ independent spins, the number of copies of $i$ has the [binomial distribution](/binomial-distribution/) $B(N, p_i)$, with mean
$$N p_i = \frac{f_i}{\bar f}, \qquad \bar f = \frac{F}{N}.$$
So an individual above the mean gets more than one copy in expectation, and one below the mean gets fewer. Summed over the members of a schema $H$, this is the factor $f(H)/\bar f$ of the [schema theorem](/schema-theorem/).

**Stochastic universal sampling.** Baker (1987) spins once: draw $u$ uniformly from $[0, 1/N)$ and take the $N$ points $u, u + 1/N, \ldots, u + (N-1)/N$ on the same wheel. Each point is uniform on $[0, 1)$, so each pick still has the law $p_i$, and individual $i$ gets either $\lfloor N p_i \rfloor$ or $\lceil N p_i \rceil$ copies. The mean is the same, and the spread is as small as possible. This is [systematic sampling](/systematic-sampling/) with selection probability proportional to size.

**Dependence on the scale.** The probabilities do not change when all $f_i$ are multiplied by a constant $a > 0$. They do change when a constant is added. With $f_i + b$,
$$p_i(b) = \frac{f_i + b}{F + N b} \to \frac{1}{N} \quad (b \to \infty),$$
so a large offset turns selection into a uniform draw. Rank-based schemes and [tournament selection](/tournament-selection/) depend only on the order of the values, so they are invariant under every increasing transformation of $f$.

**Growth of the best.** Without crossover and mutation, let a fraction $P$ of the population be copies of the best individual, with fitness $f_{\max}$. After one round of selection, the expected fraction is $P f_{\max} / \bar f$. This ratio is large early in a run, when $\bar f$ is far below $f_{\max}$, and it tends to 1 as the population becomes uniform. So the method selects strongly at first and weakly near the end.

## Examples

**Goldberg's wheel.** The population 01101, 11000, 01000, 10011 with $f(x) = x^2$ has the values 169, 576, 64 and 361, with $F = 1170$. The probabilities are 0.1444, 0.4923, 0.0547 and 0.3085, and the prefix sums cut $[0, 1)$ at 0.1444, 0.6368 and 0.6915. The spins $u = 0.10, 0.40, 0.55, 0.85$ return 01101, 11000, 11000 and 10011. The expected copies are $f_i / \bar f = 0.58, 1.97, 0.22, 1.23$. The [genetic algorithm](/genetic-algorithm/) page continues this example with crossover.

**Stochastic universal sampling on the same wheel.** With $N = 4$, take $u = 0.10$. The points 0.10, 0.35, 0.60, 0.85 return 01101, 11000, 11000 and 10011. Here 11000 must get one or two copies, because $N p_i = 1.97$, and 01000 gets zero or one, because $N p_i = 0.22$. Independent spins could give 11000 no copy at all, with probability $(1 - 0.4923)^4 \approx 0.066$.

**An offset.** Take the values 1, 2, 3, 4. The best has probability $4/10 = 0.4$. Add 100 to each value: the best has probability $104/410 \approx 0.254$, close to the uniform $0.25$. The order of the values is the same in both cases, but the pressure toward the best is much weaker in the second.

**Negative values.** For the values $-1, 2, 3$, the formula gives the "probability" $-1/4$ to the first individual, which is not a probability. The method is not defined here. Common fixes are to subtract the minimum, which sets the worst value to 0 and gives it probability 0, or to use ranks.

## Where it is used

- In Holland's reproductive plans and in the simple [genetic algorithm](/genetic-algorithm/), as the parent selection.
- In the [schema theorem](/schema-theorem/), which is proved for this selection.
- In [artificial bee colony](/artificial-bee-colony/), where onlooker bees pick food sources with probability proportional to a transformed fitness.
- In [ant colony optimization](/ant-colony-optimization/), where an ant picks the next city with probability proportional to a weight. This is the same sampling step with a different weight.
- In the resampling step of particle filters, where stochastic universal sampling is called systematic resampling.

## References
