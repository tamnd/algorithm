---
tag: CDP8D2
kind: definition
slug: premature-convergence
name: Premature convergence
aliases:
- stagnation
- loss of diversity
area: optimization/metaheuristics
level: advanced
summary: A search, usually a population, loses its diversity and settles in a region without a global optimum, so that its operators can no longer, or only very rarely, produce better solutions.
prereqs: [genetic-algorithm, population-based-search]
see_also: [multimodal-optimization, intensification-and-diversification, elitism, mutation, local-optimum, exploration-exploitation-tradeoff, cooling-schedule, differential-evolution]
sources:
  - paper: "Kenneth A. De Jong, An analysis of the behavior of a class of genetic adaptive systems, PhD thesis, University of Michigan, 1975"
    title: Kenneth A. De Jong, An analysis of the behavior of a class of genetic adaptive systems
    locator: the measures of convergence (a gene counts as converged when 95 percent of the population share its value) and the crowding factor model
  - paper: doi:10.1109/72.623217
    title: Yee Leung, Yong Gao and Zong-Ben Xu, Degree of population diversity, a perspective on premature convergence in genetic algorithms and its Markov chain analysis, IEEE Transactions on Neural Networks 8(5), 1997
    locator: pages 1165 to 1176 (premature convergence as the loss of alleles, and its probability for a genetic algorithm without mutation)
  - paper: "David E. Goldberg and Kalyanmoy Deb, A comparative analysis of selection schemes used in genetic algorithms, Foundations of Genetic Algorithms 1, Morgan Kaufmann, 1991"
    title: David E. Goldberg and Kalyanmoy Deb, A comparative analysis of selection schemes used in genetic algorithms
    locator: pages 69 to 93 (takeover times of proportional, ranking and tournament selection)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, 2nd edition, Springer, 2015
    locator: Chapter 5 (selection pressure, takeover time, and the methods that preserve diversity)
---

Premature convergence is the state of a search, most often a population-based one such as a [genetic algorithm](/genetic-algorithm/), in which the solutions have become so similar, or the steps so small, that the operators can no longer produce better solutions, or produce them only with a tiny probability, while no global optimum has been found. The usual cause is that selection removes diversity faster than [mutation](/mutation/) and recombination create it. The term has no single formal definition. The common precise versions are the loss of an allele that the optimum needs, which makes the optimum unreachable for a genetic algorithm without mutation, and the collapse of the step size or of the variance of a sampling distribution away from an optimum.

## Definition

Let a search keep a population $P_t$ of points in a space $S$ at generation $t$, and let $S^*$ be the set of global optima.

**Allele loss (bit strings).** For $S = \{0, 1\}^n$, the population has *lost the allele* $b$ at position $i$ if $x_i \ne b$ for every $x \in P_t$. If every optimum has $x_i = b$, and the operators are selection and recombination only (each bit of a child is copied from a parent), then no later population contains $b$ at position $i$. The run is then *prematurely converged* in the strong sense: $P_{t'} \cap S^* = \emptyset$ for all $t' \ge t$, with probability 1. Leung, Gao and Xu use this definition. *Proof of the claim.* Selection copies members of $P_t$, and a child built by recombination takes its bit $i$ from one of its parents. So by induction on $t'$, no member of $P_{t'}$ has $b$ at position $i$, and no optimum can appear. $\square$

**Convergence of a gene (De Jong).** A position is *converged* when at least 95 percent of the population share the same value there. The population is converged when all positions are. Premature convergence then means that the population is converged and the common values do not form an optimum. With mutation this is not an absorbing state, only one that is hard to leave.

**Collapse of a distribution (continuous domains).** For a method that samples from a distribution with center $m_t$ and scale $\sigma_t$, as [evolution strategies](/evolution-strategies/), [CMA-ES](/cma-es/) and the [cross-entropy method](/cross-entropy-method/) do, the run *converges prematurely* if $\sigma_t \to 0$ and $m_t \to \bar x$ where $\bar x$ is not a local optimum, or not a global one, depending on the goal.

**Stagnation.** A run *stagnates* if the population stays diverse but the best value does not improve for many generations. This is different from convergence: the population has not collapsed, but its operators find nothing better. Lampinen and Zelinka observed it in [differential evolution](/differential-evolution/). The alias "stagnation" is often used loosely for both.

## Examples and non-examples

**A genetic algorithm without mutation.** OneMax on $n = 30$ bits (maximize the number of ones), a population of 20, binary tournament selection with ties to the first, uniform crossover, and no mutation. Over 100 runs (seeds 0 to 99) with at most 300 generations, 17 runs found the all-ones string, and in each of the other 83 runs some position had lost the value 1 in every member, so by the claim above the optimum was unreachable. With the same settings and mutation of each bit with probability $1/30$, all 100 runs found the optimum, although 59 of them lost the value 1 at some position for a while, since mutation can restore it.

**Takeover by selection alone.** Start a population of $N = 100$ with one copy of the best solution and apply binary tournament selection with replacement and no variation. Goldberg and Deb estimate the number of generations until the best fills the population, the *takeover time*, as $(\ln N + \ln \ln N)/\ln 2 \approx 8.85$ for binary tournaments. Over 1000 runs (seeds 0 to 999), the best was lost in 201 runs, since nothing protects it, and in the other 799 runs the mean takeover time was 9.62 generations. A short takeover time means that diversity is lost quickly, which is why strong selection pressure is a cause of premature convergence.

**Quenching in simulated annealing.** [Simulated annealing](/simulated-annealing/) with a cooling schedule that is too fast freezes in a local minimum. On the 8-state cycle of that page, the schedule $2 \cdot 0.9^{k-1}$ with 60 steps saw the global minimum in only 8 of 100 runs. This is the single-point analogue of premature convergence, see [cooling schedule](/cooling-schedule/).

**Non-example: convergence to the optimum.** A population that collapses onto a global optimum has converged, but not prematurely. Convergence is the goal of a search for one optimum.

**Non-example: a concentrated population with mutation that can escape.** If every bit can flip with a positive probability, the all-equal population at a local optimum is not absorbing. The search is slow there, and it is a matter of degree whether to call this premature convergence. The time to escape can still be exponential in the distance to a better point.

**Non-example: a local search at a local optimum.** A [hill climbing](/hill-climbing/) run that stops at a [local optimum](/local-optimum/) is usually said to be *trapped*, not prematurely converged, since it never had diversity to lose.

## Related definitions

- **Diversity measures.** The mean pairwise Hamming distance, the entropy of the values at each position, or the spread of the points in a continuous space. Premature convergence is a fall of such a measure to near 0 away from the optimum.
- **Selection pressure and takeover time.** The stronger the selection, the shorter the takeover time and the faster the loss of diversity. [Elitism](/elitism/) protects the best solution, but it increases the pressure.
- **Genetic drift.** In a finite population, random sampling alone fixes values at positions, even without any fitness difference.
- **[Intensification and diversification](/intensification-and-diversification/).** Premature convergence is too much intensification too early. Niching, as in [multimodal optimization](/multimodal-optimization/), restarts, larger populations and higher mutation rates are ways to diversify.
- **[Exploration and exploitation](/exploration-exploitation-tradeoff/).** The same balance in the language of bandit problems.

## References
