---
tag: 35N2EC
kind: concept
slug: tournament-selection
name: Tournament selection
aliases:
- k-tournament selection
- binary tournament
area: optimization/metaheuristics
level: intro
summary: Draw k individuals at random and keep the best. With replacement and a strict order, the individual of rank r wins with probability (r^k - (r-1)^k) / N^k.
prereqs: [evolutionary-computation]
see_also: [roulette-wheel-selection, genetic-algorithm, genetic-programming, elitism, premature-convergence, order-statistic]
sources:
  - paper: doi:10.1162/evco.1996.4.4.361
    title: Tobias Blickle and Lothar Thiele, A comparison of selection schemes used in evolutionary algorithms, Evolutionary Computation 4(4), 1996
    locator: pages 361 to 394 (tournament selection, its fitness distribution, selection intensity and loss of diversity)
  - paper: David E. Goldberg and Kalyanmoy Deb, A comparative analysis of selection schemes used in genetic algorithms, in Foundations of Genetic Algorithms 1, Morgan Kaufmann, 1991
    title: A comparative analysis of selection schemes used in genetic algorithms
    locator: pages 69 to 93 (takeover times of proportional, ranking and tournament selection)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Section 5.2.4, Tournament selection
  - book: isbn:9780262111706
    title: John R. Koza, Genetic Programming, MIT Press, 1992
    locator: Chapter 6 (tournament selection as an alternative to fitness-proportionate reproduction)
---

Tournament selection draws $k$ individuals of the population uniformly at random and returns the one with the best fitness. The number $k$ is the tournament size, and it sets the selection pressure: $k = 1$ is a uniform draw, and a larger $k$ favors the best more. It uses only comparisons of fitness values, so it works with negative values and does not change under an increasing transformation of the fitness, unlike [roulette wheel selection](/roulette-wheel-selection/).

## In plain words

To pick one parent, take a few individuals at random from the group, for example two. Compare them and keep the best. Repeat this for each parent that you need.

A weak individual can still win, if all the others in its small contest are weaker. The best individual wins each contest that it enters. With more entrants per contest, the best ones win more often, so the group fills with good individuals faster. The method only asks which of two individuals is better, so it does not care about the size of the scores or their sign. It needs no sum over the whole group, so each contest is cheap and contests can run in parallel.

## The idea

Let the population have $N$ individuals, and sort them in a strict order by fitness, with ties broken by a fixed rule such as the index. Give rank $r = 1$ to the worst and $r = N$ to the best. A tournament of size $k$ with replacement draws $k$ ranks independently and uniformly from $\{1, \ldots, N\}$ and returns the largest.

**The winning probability.** The winner has rank at most $r$ exactly when all $k$ entrants have rank at most $r$, which has probability $(r/N)^k$. So the individual of rank $r$ wins with probability
$$p_r = \frac{r^k - (r-1)^k}{N^k}.$$
This is the law of the largest of $k$ independent uniform ranks, an [order statistic](/order-statistic/). For $k = 2$, $p_r = (2r - 1)/N^2$, which is linear in $r$. So a binary tournament has the same selection probabilities as linear ranking selection with these weights.

Without replacement, the entrants are a uniform $k$-subset, and the individual of rank $r$ wins exactly when the other $k - 1$ entrants come from the $r - 1$ worse ones:
$$p_r = \binom{r - 1}{k - 1} \Big/ \binom{N}{k}.$$

**Ties.** With equal fitness values, the probabilities depend on the tie rule. With a fixed rule, such as the smaller index wins, the order is strict and the formulas hold. With a random tie rule, the tied individuals share their total probability equally.

**Expected copies of the best.** In $N$ tournaments with replacement, the best wins each with probability $1 - (1 - 1/N)^k$. Its expected number of copies is $N(1 - (1 - 1/N)^k)$, which is at most $k$ and tends to $k$ as $N$ grows. Without variation, if a fraction $P$ of the population are copies of the best, the expected fraction after one round is $1 - (1 - P)^k$. So a larger $k$ makes the best take over in fewer generations. Goldberg and Deb (1991) gave takeover times for the common selection schemes.

**Selection intensity.** If the fitness values in the population have a standard normal distribution, the mean fitness of the winners is the expected maximum of $k$ standard normal values. For $k = 2$ this is $\mathrm{E}[\max(Z_1, Z_2)] = \tfrac{1}{2}\mathrm{E}|Z_1 - Z_2| = 1/\sqrt{\pi} \approx 0.564$, and for $k = 3$ it is $3/(2\sqrt{\pi}) \approx 0.846$. Blickle and Thiele (1996) call this the selection intensity and tabulate it for larger $k$.

**Invariance.** Let $g$ be a strictly increasing function. The tournament compares $f$ values only, and $g(f(a)) > g(f(b))$ exactly when $f(a) > f(b)$. So the selection probabilities for $g \circ f$ are the same as for $f$. Roulette wheel selection does not have this property.

## Examples

**Five individuals.** Take the fitness values $5, 1, 4, 2, 3$ for the individuals $0, \ldots, 4$. The ranks are $5, 1, 4, 2, 3$. With $k = 2$ and replacement, $p_r = (2r - 1)/25$:

| individual | fitness | rank $r$ | $p_r$ for $k = 2$ | $p_r$ for $k = 3$ |
|---|---|---|---|---|
| 0 | 5 | 5 | 9/25 = 0.36 | 61/125 = 0.488 |
| 1 | 1 | 1 | 1/25 = 0.04 | 1/125 = 0.008 |
| 2 | 4 | 4 | 7/25 = 0.28 | 37/125 = 0.296 |
| 3 | 2 | 2 | 3/25 = 0.12 | 7/125 = 0.056 |
| 4 | 3 | 3 | 5/25 = 0.20 | 19/125 = 0.152 |

A roulette wheel on the same values gives the best $5/15 = 0.33$ and the worst $1/15 = 0.067$. If we add 100 to each value, the tournament probabilities do not change, but the roulette probabilities become nearly equal.

**Size 1 and size N.** With $k = 1$, $p_r = 1/N$ for each $r$, so selection is uniform and there is no pressure. With $k$ very large, $p_N = 1 - (1 - 1/N)^k$ tends to 1, so selection almost always returns the best.

**A check by counting.** For $N = 3$ and $k = 2$ with replacement there are 9 ordered pairs of entrants. The best wins in the 5 pairs that contain it, the middle one in the 3 pairs from $\{1, 2\}$ that contain rank 2, and the worst only in the pair $(1, 1)$. This gives $5/9$, $3/9$ and $1/9$, which is $(2r - 1)/9$.

## Where it is used

- As the parent selection of most current [genetic algorithms](/genetic-algorithm/), with $k = 2$ the most common choice.
- In [genetic programming](/genetic-programming/), where Koza used it as an alternative to fitness-proportionate selection, and where it is now the usual choice.
- In multi-objective algorithms such as [NSGA-II](/nsga-ii/), where a binary tournament compares individuals by Pareto rank and crowding distance instead of one number.
- In steady state algorithms, where a reverse tournament picks the individual to replace.
- In parallel and distributed evolutionary algorithms, because a tournament needs no global information about the population.

## References
