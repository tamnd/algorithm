---
tag: WKJDJS
kind: definition
slug: fitness-function
name: Fitness function
aliases:
- objective function
- cost function
- evaluation function
area: optimization/metaheuristics
level: intro
summary: The function that scores candidate solutions in a metaheuristic, so that they can be compared and selected. It is the objective, often changed by penalties, scaling or ranks.
prereqs: [global-optimization]
see_also: [fitness-landscape, genetic-algorithm, black-box-optimization, local-optimum, premature-convergence, multimodal-optimization, knapsack-problem, pareto-front]
sources:
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, 2nd edition, Springer, 2015
    locator: Chapter 3 (the evaluation function as a component of an evolutionary algorithm) and Chapter 5 (fitness proportional, ranking and tournament selection)
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 3 (fitness scaling and the mapping of objective values to fitness)
  - paper: doi:10.1016/S0045-7825(01)00323-1
    title: Carlos A. Coello Coello, Theoretical and numerical constraint-handling techniques used with evolutionary algorithms, a survey of the state of the art, Computer Methods in Applied Mechanics and Engineering 191(11-12), 2002
    locator: pages 1245 to 1287 (penalty functions and their weights)
  - paper: "Yaochu Jin, A comprehensive survey of fitness approximation in evolutionary computation, Soft Computing 9(1), 2005"
    title: Yaochu Jin, A comprehensive survey of fitness approximation in evolutionary computation
    locator: pages 3 to 12 (surrogate models of an expensive fitness)
---

A fitness function is the function that a [metaheuristic](/metaheuristic/) uses to score candidate solutions, so that it can compare them, keep the better ones and select parents. It is built from the objective of the problem, but it need not be equal to it: constraints are often added as penalties, values are scaled or replaced by ranks, and an expensive objective can be replaced by a cheaper model. In evolutionary computation, larger fitness is better by convention, while an objective is often minimized. Which properties of the fitness matter depends on how the method uses it: a method that only compares values is unchanged by any strictly increasing transformation of the fitness, while fitness proportional selection is not.

## Definition

Let $S$ be the set of candidate solutions, the search space, and let the problem be to maximize an objective $g : S \to \mathbb{R}$ over a feasible set $F \subseteq S$. A *fitness function* is a function $\varphi : S \to \mathbb{R}$ that the algorithm evaluates and uses as its only information about the quality of a solution. It is *faithful* to the problem if every maximizer of $\varphi$ over $S$ is a feasible maximizer of $g$.

Common ways to build $\varphi$ from $g$:

- **Identity or sign change.** $\varphi = g$, or $\varphi = -f$ when an objective $f$ is minimized.
- **Monotone transformation.** $\varphi = h \circ g$ with $h$ strictly increasing. It has the same maximizers and the same order on $S$.
- **Penalty.** $\varphi(x) = g(x) - \mu\, v(x)$, where $v(x) \ge 0$ measures how much $x$ violates the constraints and $v(x) = 0$ exactly when $x \in F$.
- **Rank.** In a population, replace the value of each member by its rank. This depends on the population, so it is a fitness of the population and not of a single solution.

**Invariance.** Call a selection rule *comparison-based* if the probability that it picks a member depends only on the order of the fitness values in the population. Then for any strictly increasing $h$, running the algorithm with $h \circ \varphi$ gives the same distribution of runs as with $\varphi$. *Proof.* Each step uses the fitness only through comparisons $\varphi(x) < \varphi(y)$, and $h(\varphi(x)) < h(\varphi(y))$ holds exactly when $\varphi(x) < \varphi(y)$. So each step has the same conditional distribution, and by induction so does the whole run. $\square$ Tournament selection, truncation selection, rank selection, the (1+1) and $(\mu, \lambda)$ [evolution strategies](/evolution-strategies/) and [CMA-ES](/cma-es/) are comparison-based. Fitness proportional selection, which picks $x_i$ with probability $\varphi(x_i)/\sum_j \varphi(x_j)$ and needs $\varphi > 0$, is not.

## Examples and non-examples

**Proportional selection is not invariant under a shift.** For four members with fitness $1, 2, 3, 4$, proportional selection picks them with probabilities $0.1, 0.2, 0.3, 0.4$. After adding 100 to each fitness, so $101, 102, 103, 104$ with sum 410, the probabilities are $0.2463, 0.2488, 0.2512, 0.2537$, almost uniform, and the selection pressure is nearly gone. Binary tournament selection with replacement picks the member of rank $i$, with rank 1 the worst, with probability $(i^2 - (i - 1)^2)/N^2 = (2i - 1)/N^2$, here $1/16, 3/16, 5/16, 7/16$, before and after the shift. This is why Goldberg recommends fitness scaling for proportional selection.

**A penalty that is too weak.** A [knapsack](/knapsack-problem/) instance has the weights $3, 4, 5$, the values $4, 5, 6$ and the capacity 7. The best feasible set is $\{1, 2\}$ with weight 7 and value 9. Take $\varphi(x) = $ value $- \mu \cdot \max(0, \text{weight} - 7)$. The infeasible sets are $\{1, 3\}$ (value 10, excess 1), $\{2, 3\}$ (value 11, excess 2) and $\{1, 2, 3\}$ (value 15, excess 5). The fitness is faithful if and only if $9 > 10 - \mu$, $9 > 11 - 2\mu$ and $9 > 15 - 5\mu$, that is, $\mu > \max(1, 1, 6/5) = 1.2$. With $\mu = 1$, the fittest set is $\{1, 2, 3\}$ with fitness 10, which is not feasible.

**OneMax and the needle.** On $S = \{0, 1\}^n$, OneMax $\varphi(x) = \sum_i x_i$ gives every non-optimal string a neighbor with higher fitness, so a [hill climbing](/hill-climbing/) finds the optimum. The needle, $\varphi(x) = 1$ if $x$ is one given string and 0 otherwise, has the same optimum, but its fitness gives no guidance at all, see [black-box optimization](/black-box-optimization/). The choice of the fitness, not only of the problem, shapes the [fitness landscape](/fitness-landscape/).

**Non-example: a vector of objectives.** In multi-objective optimization each solution has a vector of values, and two vectors can be incomparable. That is not a fitness function in the sense above. Methods such as [NSGA-II](/nsga-ii/) build a scalar fitness from it, the rank of the front that contains the solution, see [Pareto front](/pareto-front/).

**Non-example: comparisons that are not transitive.** In coevolution, a solution is scored by games against other solutions, and $a$ can beat $b$, $b$ beat $c$ and $c$ beat $a$. No function $\varphi$ gives these comparisons, so there is no fitness function, only a relation.

## Related definitions

- **Objective function and cost function.** The function of the problem. The fitness is what the algorithm uses, which can differ from it.
- **[Fitness landscape](/fitness-landscape/).** The fitness together with a neighborhood on $S$. Its [local optima](/local-optimum/), plateaus and basins decide how hard the search is.
- **Surrogate fitness.** A cheap model of an expensive fitness, such as a [Gaussian process](/gaussian-process/), used to screen candidates before the true evaluation.
- **Noisy fitness.** A fitness that returns a random value whose mean is the true one. Comparisons can then be wrong, and averaging or larger populations are needed.
- **Fitness sharing.** A fitness that is divided by a count of similar members, to keep diversity, see [multimodal optimization](/multimodal-optimization/) and [premature convergence](/premature-convergence/).

## References
