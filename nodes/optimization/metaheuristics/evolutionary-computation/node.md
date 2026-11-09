---
tag: R0B4J8
kind: concept
slug: evolutionary-computation
name: Evolutionary computation
aliases:
- evolutionary algorithms
- evolutionary algorithm
- EA
area: optimization/metaheuristics
level: intro
summary: Population-based search methods that select, vary and replace candidate solutions in a loop modeled on evolution, such as genetic algorithms, evolution strategies and genetic programming.
prereqs: [population-based-search]
see_also: [genetic-algorithm, evolution-strategies, genetic-programming, differential-evolution, cma-es, swarm-intelligence, fitness-function, no-free-lunch-theorem]
sources:
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Chapter 2, Evolutionary computing, the origins, and Chapter 3, What is an evolutionary algorithm
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992
    locator: Chapters 1 to 7 (adaptive plans, schemata and the genetic plan)
  - paper: doi:10.1023/A:1015059928466
    title: Hans-Georg Beyer and Hans-Paul Schwefel, Evolution strategies, a comprehensive introduction, Natural Computing 1(1), 2002
    locator: pages 3 to 52, Section 2 (the history of evolution strategies from 1964)
  - book: Lawrence J. Fogel, Alvin J. Owens and Michael J. Walsh, Artificial Intelligence through Simulated Evolution, Wiley, 1966
    title: Artificial Intelligence through Simulated Evolution
    locator: the evolution of finite state machines for prediction (evolutionary programming)
  - book: doi:10.1007/978-3-642-17339-4
    title: Thomas Jansen, Analyzing Evolutionary Algorithms, The Computer Science Perspective, Springer, 2013
    locator: Chapters 2 and 5 (evolutionary algorithms as randomized search heuristics, and the methods of runtime analysis)
  - book: doi:10.1007/978-3-030-29414-4
    title: Benjamin Doerr and Frank Neumann (editors), Theory of Evolutionary Computation, Recent Developments in Discrete Optimization, Springer, 2020
    locator: Chapter 1 (probabilistic tools) and Chapter 2 (drift analysis)
---

Evolutionary computation is the family of [population-based](/population-based-search/) search methods that work like a simple model of natural evolution: a population of candidate solutions undergoes selection by fitness, variation by [mutation](/mutation/) and [crossover](/crossover/), and replacement, over many generations. Its main branches are [genetic algorithms](/genetic-algorithm/), [evolution strategies](/evolution-strategies/), evolutionary programming and [genetic programming](/genetic-programming/), which started separately in the 1960s and 1970s. The methods need only evaluations of a [fitness function](/fitness-function/), so they apply to [black-box optimization](/black-box-optimization/). Their theory has moved from the [schema theorem](/schema-theorem/) to proved bounds on the expected number of evaluations for specific algorithms and functions.

## In plain words

Nature does not design a plant or an animal. It makes many slightly different ones, and the ones that do well have more young. Over many generations this process gives good designs without a plan.

An evolutionary algorithm copies this idea to solve a problem. It keeps a group of candidate answers and a score for each. It picks good answers as parents, makes children by small random changes and by mixing parents, and keeps the better answers for the next round. It needs only the score of an answer, not a formula or a slope. The price is that it gives no proof that the best answer is optimal, and it can use many evaluations.

## The idea

An evolutionary algorithm (EA) is the loop of [population-based search](/population-based-search/) with these parts.

- **Representation.** A coding of solutions as genotypes, such as bit strings, real vectors, permutations or trees. The [fitness function](/fitness-function/) maps each genotype to a number.
- **Parent selection.** A random choice that prefers fitter members, such as [roulette wheel selection](/roulette-wheel-selection/) or [tournament selection](/tournament-selection/).
- **Variation.** [Crossover](/crossover/) makes children from two or more parents, and [mutation](/mutation/) changes one child at random.
- **Survivor selection.** The rule that forms the next population, for example all children, the best $\mu$ of parents and children, or the children plus the [elite](/elitism/).
- **Stopping rule.** A budget of evaluations or time, a target value, or a lack of progress.

**The branches.** The four classic branches differ mainly in representation and in the operator that does most of the work.

| branch | started by | representation | main operator | survivor selection |
|---|---|---|---|---|
| [genetic algorithm](/genetic-algorithm/) | Holland, 1960s and 1975 | bit strings | crossover | children replace parents |
| [evolution strategy](/evolution-strategies/) | Rechenberg and Schwefel, 1964 | real vectors | Gaussian mutation with adapted step sizes | best $\mu$ of $\lambda$ or of $\mu + \lambda$ |
| evolutionary programming | L. J. Fogel, 1960s | finite state machines, later real vectors | mutation only | tournaments among parents and children |
| [genetic programming](/genetic-programming/) | Cramer 1985, Koza 1992 | program trees | subtree crossover | children replace parents |

Since the 1990s the branches have merged into one field, and many methods mix their parts. [Differential evolution](/differential-evolution/), [CMA-ES](/cma-es/), [estimation of distribution algorithms](/estimation-of-distribution-algorithm/), [memetic algorithms](/memetic-algorithm/) and multi-objective algorithms such as [NSGA-II](/nsga-ii/) are later members.

**Theory.** Three kinds of results describe what an EA does.

- **One-generation statements.** Holland's [schema theorem](/schema-theorem/) bounds the expected number of strings that match a pattern after one generation. It does not give the behavior over many generations.
- **Convergence.** On a finite space, an EA with [elitism](/elitism/) and a mutation that can reach every point finds an optimum with probability 1 (Rudolph 1994). This says nothing about the time.
- **Runtime analysis.** Since the 1990s, the expected number of evaluations has been bounded for specific algorithms and functions, with tools such as fitness levels and drift analysis. The $(1+1)$ EA needs $\Theta(n \log n)$ expected evaluations on OneMax and on every linear function (Droste, Jansen and Wegener 2002). Jansen (2013) and Doerr and Neumann (2020) give the methods.

The [no free lunch theorem](/no-free-lunch-theorem/) shows that, averaged over all functions on a finite set, every black-box algorithm has the same performance. So a statement that an EA works well must name the class of problems.

## Examples

**One generation of a genetic algorithm.** For $f(x) = x^2$ on 5-bit strings, roulette selection and one-point crossover take the population 01101, 11000, 01000, 10011, with mean fitness 292.5, to 01100, 11001, 11011, 10000, with mean fitness 438.5. The [genetic algorithm](/genetic-algorithm/) page gives the steps.

**The $(1+1)$ EA on OneMax.** Keep one string $x \in \{0,1\}^n$. Flip each bit with probability $1/n$ to get $y$, and keep $y$ if it has at least as many ones as $x$. The expected number of iterations until $x = 1^n$ is at most $e n H_n$, where $H_n$ is the $n$th harmonic number, and at least a constant times $n \ln n$. For $n = 100$ the upper bound is $e \cdot 100 \cdot H_{100} \approx 1410$. The [genetic algorithm](/genetic-algorithm/) page proves both bounds.

**Evolution strategy.** The $(1+1)$-ES on real vectors sets $y = x + \sigma z$ with $z$ standard normal, keeps $y$ if $f(y) \le f(x)$, and changes $\sigma$ by the 1/5 success rule: increase $\sigma$ if more than one fifth of recent mutations succeeded, and decrease it otherwise. See [evolution strategies](/evolution-strategies/).

**Evolving a program.** [Genetic programming](/genetic-programming/) searches for an expression such as $x^2 + x + 1$ that fits given data, with expression trees as genotypes and subtree crossover as the main operator.

## Where it is used

- Engineering design, where a simulation scores each design and no gradient is available, such as the shape of antennas, wings and structures.
- Scheduling, timetabling and routing, usually as [memetic algorithms](/memetic-algorithm/) with a problem-specific [local search](/local-search/).
- Multi-objective optimization, where a population approximates a Pareto front, with algorithms such as [NSGA-II](/nsga-ii/).
- Continuous black-box optimization with [CMA-ES](/cma-es/) and [differential evolution](/differential-evolution/).
- Symbolic regression and the automatic design of programs and circuits with [genetic programming](/genetic-programming/).
- The search for neural network structures, as one of the strategies of [neural architecture search](/neural-architecture-search/).

## References
