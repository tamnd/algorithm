---
tag: B62H2R
kind: technique
slug: population-based-search
name: Population-based search
aliases:
- population-based metaheuristic
- population-based method
area: optimization/metaheuristics
level: intro
summary: Keep a set of candidate solutions, make new candidates from the set and the information it holds, and replace members. Genetic algorithms, evolution strategies, PSO and ACO all follow this loop.
prereqs: [metaheuristic, local-search]
see_also: [evolutionary-computation, swarm-intelligence, intensification-and-diversification, estimation-of-distribution-algorithm, premature-convergence, multimodal-optimization, stochastic-local-search, no-free-lunch-theorem]
sources:
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 3, Population-based metaheuristics (the common concepts, the initial population, the stopping criteria, and the evolutionary and swarm algorithms)
  - paper: doi:10.1145/937503.937505
    title: Christian Blum and Andrea Roli, Metaheuristics in combinatorial optimization, overview and conceptual comparison, ACM Computing Surveys 35(3), 2003
    locator: pages 268 to 308, Section 4, Population-based methods
  - paper: Mark Zlochin, Mauro Birattari, Nicolas Meuleau and Marco Dorigo, Model-based search for combinatorial optimization, a critical survey, Annals of Operations Research 131, 2004
    title: Model-based search for combinatorial optimization, a critical survey
    locator: pages 373 to 395 (instance-based and model-based search)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of new methods described only by a metaphor)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Chapter 3, What is an evolutionary algorithm (the general scheme) and Chapter 5, Fitness, selection, and population management
  - paper: Jakub Kudela, A critical problem in benchmarking and analysis of evolutionary computation methods, Nature Machine Intelligence 4, 2022
    title: A critical problem in benchmarking and analysis of evolutionary computation methods
    locator: pages 1238 to 1245 (methods with a bias toward the center of the search space)
---

Population-based search keeps a set of candidate solutions, the population, instead of one current solution. In each iteration it makes new candidates from the members of the population or from a model fitted to them, evaluates them, and decides which candidates form the next population. [Evolutionary algorithms](/evolutionary-computation/), [particle swarm optimization](/particle-swarm-optimization/), [ant colony optimization](/ant-colony-optimization/) and [estimation of distribution algorithms](/estimation-of-distribution-algorithm/) are instances. The population lets the search cover several regions at once and share information between them, but it costs more evaluations per iteration than a single-point [local search](/local-search/).

## In plain words

A [local search](/local-search/) has one current solution and moves it step by step. A population-based search has a group of solutions. In each round, it uses the group to make new solutions: it can mix two members, change one member a little, move members toward the best one, or learn which parts are common in good members and make new solutions with these parts. Then it keeps some of the old and new solutions as the next group.

The group can spread over several good regions at the same time, so one bad start does not decide the result. It also gives information that one solution alone cannot give, for example which parts of good solutions agree. The cost is more evaluations in each round.

## When it applies

- **Black-box problems.** Only evaluations of the objective are available, as in [black-box optimization](/black-box-optimization/), and an evaluation is cheap enough to do many times.
- **Rugged or multimodal landscapes.** The [fitness landscape](/fitness-landscape/) has many [local optima](/local-optimum/), and a set of points spread over the space finds good basins more reliably than one point.
- **Several answers at once.** In [multimodal optimization](/multimodal-optimization/) and in multi-objective optimization, the population can hold several optima or an approximation of the whole Pareto front in one run.
- **Parallel evaluation.** The members of one iteration can be evaluated at the same time, so a population fits parallel hardware well.

It is a weak choice when the problem has structure that an exact or problem-specific method uses well, or when each evaluation is so expensive that only a few hundred are possible. In the second case, model-based methods such as Bayesian optimization use each evaluation better.

## The template

Let $f$ be the objective to minimize, $S$ the search space and $N$ the population size. The four operations are the parts that each method fills in.

```pseudo id=main
POPULATION-BASED-SEARCH(f, S, N)
L1  P ← INITIALIZE(S, N)                    ▷ often uniform at random
L2  evaluate f on each member of P
L3  best ← a member of P with the smallest f
L4  M ← INITIAL-MEMORY(P)                    ▷ pheromone, velocities, a model, or nothing
L5  while the stopping rule is false do
L6      C ← GENERATE(P, M)                  ▷ variation, moves or sampling
L7      evaluate f on each member of C
L8      P ← REPLACE(P, C)                   ▷ survivor selection
L9      M ← UPDATE(M, P, C)
L10     best ← the better of best and the best member of C
L11 return best
```

The methods differ in GENERATE, REPLACE and the memory $M$.

| method | GENERATE | REPLACE | memory $M$ |
|---|---|---|---|
| [genetic algorithm](/genetic-algorithm/) | selection, [crossover](/crossover/), [mutation](/mutation/) | children replace parents, with [elitism](/elitism/) | none |
| [evolution strategy](/evolution-strategies/) | recombination and Gaussian mutation | the best $\mu$ of children, or of parents and children | step sizes |
| [particle swarm optimization](/particle-swarm-optimization/) | move each particle by its velocity | each particle moves; personal bests improve only | velocities, personal and global bests |
| [ant colony optimization](/ant-colony-optimization/) | each ant builds a solution from pheromone and heuristic values | the ants of one iteration | the pheromone matrix |
| [estimation of distribution algorithm](/estimation-of-distribution-algorithm/) | sample a probability model | the selected sample | the model |
| [differential evolution](/differential-evolution/) | difference vectors and crossover | each child against its own parent | none |

Ant colony optimization and estimation of distribution algorithms are model-based: new candidates come from a probability model, and the population only updates the model. Genetic algorithms and differential evolution are instance-based: new candidates come directly from members.

## Classic examples

- **Genetic algorithm.** A generational population of bit strings with roulette or tournament selection, one-point crossover and bit mutation. See [genetic algorithm](/genetic-algorithm/).
- **The $(\mu + \lambda)$ evolution strategy.** $\mu$ parents make $\lambda$ children by Gaussian mutation, and the best $\mu$ of all $\mu + \lambda$ survive. See [evolution strategies](/evolution-strategies/).
- **Particle swarm optimization.** Each member keeps a position, a velocity and its personal best, and all members are drawn toward the best point of the swarm. See [particle swarm optimization](/particle-swarm-optimization/).
- **Ant colony optimization.** Each ant builds a tour of the [traveling salesman problem](/traveling-salesman-problem/) edge by edge, and the edges of good tours get more pheromone. See [ant colony optimization](/ant-colony-optimization/).
- **Multi-start local search.** $N$ independent runs of [hill climbing](/hill-climbing/) form a population with no interaction. It is the baseline that a population-based method must beat to show that the sharing of information helps.

## Variations

- **Generational or steady state.** Replace the whole population at once, or insert one or two children per step.
- **Structured populations.** Island models split the population into groups that exchange members from time to time. Cellular models let each member mate only with its neighbors on a grid. Both slow the spread of good members and keep diversity.
- **Niching.** Fitness sharing divides the fitness of a member by the number of members near it, and crowding lets a child replace a similar member. Both keep members on several peaks, for [multimodal optimization](/multimodal-optimization/).
- **Hybrids.** A [memetic algorithm](/memetic-algorithm/) improves each new member by [local search](/local-search/).
- **Archives.** Keep the best points, or the nondominated points in multi-objective search, in a set outside the population.
- **Population size control.** Restart with a larger population when the search stalls, or change $N$ during the run.

## Pitfalls

- **Loss of diversity.** Strong selection in line L8 can make all members almost equal early in the run. Then GENERATE only makes points close to them, and the search stalls at a [premature convergence](/premature-convergence/). Measure the diversity, and use weaker selection, larger populations, niching or restarts.
- **Counting iterations instead of evaluations.** One iteration of a method with $N = 100$ costs 100 evaluations in line L7, and one iteration of a single-point method costs 1. Compare methods by the number of evaluations, or by time.
- **New names for old methods.** Many recent methods describe the loop above with a new metaphor from nature. Sörensen (2015) showed that the metaphor often hides an operator that an older method already has, so analyse each new method by its operators, not by its story. The pages on [harmony search](/harmony-search/), [cuckoo search](/cuckoo-search/), the [firefly algorithm](/firefly-algorithm/) and the [bat algorithm](/bat-algorithm/) give the details.
- **Claims of general superiority.** No method beats all others on all problems, by the [no free lunch theorem](/no-free-lunch-theorem/). A result on a set of test functions holds for those functions and those budgets.
- **Bias toward the center.** Some update rules move members toward the center of the box or toward the origin. On test functions with the optimum at the origin, such a bias looks like good performance, as Kudela (2022) showed for several recent methods. Test with shifted and rotated functions.

## Exercises

1. Let a fraction $q$ of the search space lie in the basin of the global optimum, and let $N$ members start uniformly at random. Show that at least one starts in the basin with probability $1 - (1 - q)^N$, and find the smallest $N$ that gives probability $0.99$ for $q = 0.01$.
2. In a population of $N$ distinct members, a new population is drawn by $N$ uniform draws with replacement, with no variation. Show that the expected number of distinct members in the new population is $N(1 - (1 - 1/N)^N)$, which is about $0.632 N$ for large $N$. This is the loss of diversity by drift alone.
3. Show that if REPLACE in line L8 keeps the best member of $P \cup C$, then the smallest $f$ in $P$ never increases. Give a REPLACE that does not keep this property.
4. Write multi-start [hill climbing](/hill-climbing/) in the form of the template: say what INITIALIZE, GENERATE, REPLACE and the memory are.

## References
