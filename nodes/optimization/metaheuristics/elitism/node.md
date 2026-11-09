---
tag: EV24W3
kind: concept
slug: elitism
name: Elitism
aliases:
- elite preservation
- elitist selection
area: optimization/metaheuristics
level: intro
summary: Copy the best individuals of a generation unchanged into the next one. The best fitness in the population never decreases, and with a mutation that reaches every point it converges with probability 1.
prereqs: [evolutionary-computation]
see_also: [genetic-algorithm, evolution-strategies, nsga-ii, premature-convergence, mutation, tournament-selection, simulated-annealing, markov-chain]
sources:
  - paper: doi:10.1109/72.265964
    title: Günter Rudolph, Convergence analysis of canonical genetic algorithms, IEEE Transactions on Neural Networks 5(1), 1994
    locator: pages 96 to 101 (the canonical genetic algorithm does not converge to the optimum; variants that keep the best solution do)
  - paper: Kenneth A. De Jong, An analysis of the behavior of a class of genetic adaptive systems, PhD thesis, University of Michigan, 1975
    title: An analysis of the behavior of a class of genetic adaptive systems
    locator: the elitist model, one of the variants of the reproductive plan studied in the thesis
  - paper: doi:10.1023/A:1015059928466
    title: Hans-Georg Beyer and Hans-Paul Schwefel, Evolution strategies, a comprehensive introduction, Natural Computing 1(1), 2002
    locator: pages 3 to 52, Section 4 (plus selection and comma selection)
  - paper: doi:10.1109/4235.996017
    title: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal and T. Meyarivan, A fast and elitist multiobjective genetic algorithm, NSGA-II, IEEE Transactions on Evolutionary Computation 6(2), 2002
    locator: pages 182 to 197 (elitism by selection from the union of parents and children)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Section 5.3, Survivor selection (elitism and replace-worst)
---

Elitism is the rule that an [evolutionary algorithm](/evolutionary-computation/) copies its $e \ge 1$ best individuals unchanged into the next generation. With it, the best fitness in the population never decreases. With a [mutation](/mutation/) that can reach every point, an elitist algorithm on a finite space finds an optimum with probability 1 and keeps it, while the canonical [genetic algorithm](/genetic-algorithm/) without elitism does not converge in this sense (Rudolph 1994). The price is a stronger pull toward the current best, which can speed up [premature convergence](/premature-convergence/).

## In plain words

In each round, a population-based method makes a new group of solutions and drops the old one. A good solution can then get lost: its children can all be worse, or it can fail to be chosen as a parent at all. Elitism stops this. Before you fill the new group, copy the best one or the best few of the old group into it, without any change.

So the best solution in the group is never worse than in the round before. The cost is that the copies take places in the group, and the best solutions get even more weight. If the best solution sits on a local peak, the whole group can gather around it and stop looking elsewhere.

## The idea

Let $P_t$ be the population of generation $t$ and $m_t = \max_{x \in P_t} f(x)$, for a fitness $f$ to maximize.

**Monotonicity.** If $P_{t+1}$ contains a best individual of $P_t$, then $m_{t+1} \ge m_t$. This is the only property that elitism gives by itself. It holds for any selection and any variation operators.

**Convergence.** Let the search space be finite, and let each generation make at least one new child whose law gives each point at least a probability $\delta > 0$, whatever the current population is. Standard bit [mutation](/mutation/) with rate $0 < p < 1$ on strings of length $n$ has $\delta = \min(p, 1 - p)^n$. Then an optimal point appears by generation $t$ with probability at least $1 - (1 - \delta)^t$, and by monotonicity, every later population holds an optimal point. So $m_t = f^*$ for all large $t$ with probability 1. The [genetic algorithm](/genetic-algorithm/) page gives the proof.

**Without elitism.** With $0 < p < 1$, the populations of the canonical genetic algorithm form an irreducible [Markov chain](/markov-chain/) on a finite set. Every population, including those with no optimal string, is visited again and again. So $m_t$ does not converge to $f^*$, although the best fitness seen so far does. Rudolph (1994) proved this and showed that keeping the best individual restores convergence. This kind of convergence says nothing about speed: $(1 - \delta)^t$ can be close to 1 for any practical $t$.

**Forms of elitism.**

- **Copy the elite.** A generational algorithm copies the $e$ best of $P_t$ into $P_{t+1}$ and fills the other $N - e$ places with children. This is line L4 of the [genetic algorithm](/genetic-algorithm/) page.
- **Plus selection.** A $(\mu + \lambda)$ [evolution strategy](/evolution-strategies/) chooses the $\mu$ best of the $\mu$ parents and $\lambda$ children together. It is fully elitist. The $(\mu, \lambda)$ strategy chooses among the children only, and it is not elitist.
- **Replace the worst.** A steady state algorithm inserts a child only if it is better than the worst member, so the best member stays.
- **An archive.** Multi-objective algorithms such as [NSGA-II](/nsga-ii/) select from the union of parents and children by Pareto rank, so nondominated points are not lost. Other algorithms keep the best points in a separate archive.

**Elitism is not the same as keeping a record.** Many algorithms, including [simulated annealing](/simulated-annealing/), keep the best point seen so far in a variable and return it at the end, but do not put it back into the search. The returned value is then monotone, but the search itself can move away from the best point. With elitism, the best point keeps taking part in the search.

## Examples

**Losing the best without elitism.** Maximize OneMax on 2 bits, with the population $\{11, 00\}$, [roulette wheel selection](/roulette-wheel-selection/), no crossover and bit mutation with $p = 0.1$. The fitness values are 2 and 0, so both parents are 11. A child stays 11 with probability $0.9^2 = 0.81$. Both children differ from 11 with probability $0.19^2 = 0.0361$. So without elitism, the optimum is lost in this generation with probability 0.0361. With $e = 1$, the optimum is copied and cannot be lost.

**The genetic algorithm example.** In the example of the [genetic algorithm](/genetic-algorithm/) page, the best string of the first population is 11000 with $f = 576$. With $e = 1$, the next population holds 11000 and three children. Without elitism and with the random choices of that example, the next population is 01100, 11001, 11011, 10000, which does not hold 11000 but has a better maximum, 729. Elitism guarantees the bound $m_{t+1} \ge 576$. It does not cause the improvement.

**Plus selection.** A $(1 + 1)$ algorithm keeps the child only if it is at least as good as the parent. It is elitist with $e = 1$ and $N = 1$. Its fitness never decreases, and the proofs of its runtime on OneMax use this fact.

## Where it is used

- In most practical [genetic algorithms](/genetic-algorithm/), with $e = 1$ or a small fraction of the population.
- In the $(\mu + \lambda)$ [evolution strategies](/evolution-strategies/) and in the $(1+1)$ EA.
- In multi-objective algorithms such as [NSGA-II](/nsga-ii/), through selection from parents and children together.
- In the steady state update of [memetic algorithms](/memetic-algorithm/), where a child replaces the worst member only if it is better.
- In [ant colony optimization](/ant-colony-optimization/), where the best-so-far tour of MAX-MIN Ant System deposits pheromone again in each iteration.
- In convergence proofs for evolutionary algorithms on finite spaces.

## References
