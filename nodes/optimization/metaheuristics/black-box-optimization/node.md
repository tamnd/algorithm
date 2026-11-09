---
tag: R16DPF
kind: problem
slug: black-box-optimization
name: Black-box optimization
aliases:
- derivative-free optimization problem
- zero-order optimization
- black-box complexity
area: optimization/metaheuristics
level: advanced
summary: Optimize an objective that is known only through its values at points that the algorithm chooses. The cost is the number of values asked for.
prereqs: [global-optimization, query-model]
see_also: [derivative-free-optimization, no-free-lunch-theorem, fitness-function, lower-bound, hyperparameter-tuning, gaussian-process, cma-es, finite-difference-method]
sources:
  - paper: doi:10.1007/s00224-004-1177-z
    title: Stefan Droste, Thomas Jansen and Ingo Wegener, Upper and lower bounds for randomized search heuristics in black-box optimization, Theory of Computing Systems 39(4), 2006
    locator: pages 525 to 544 (the black-box model, black-box complexity, and the bounds for classes such as needle and generalized OneMax functions)
  - book: doi:10.1007/978-3-319-68913-5
    title: Charles Audet and Warren Hare, Derivative-Free and Blackbox Optimization, Springer, 2017
    locator: Chapter 1 (the blackbox setting and its sources) and Chapter 3 (the first methods, such as exhaustive search, grid search and coordinate search)
  - paper: doi:10.1017/S0962492919000060
    title: Jeffrey Larson, Matt Menickelly and Stefan M. Wild, Derivative-free optimization methods, Acta Numerica 28, 2019
    locator: pages 287 to 404, Section 1 (the oracle model and the measures of cost)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, 2nd edition, Springer, 2018
    locator: Section 1.1.2 (the oracle model and analytical complexity) and Section 1.1.3 (the lower bound for Lipschitz functions)
  - paper: "Stefan Droste, Thomas Jansen and Ingo Wegener, On the analysis of the (1+1) evolutionary algorithm, Theoretical Computer Science 276(1-2), 2002"
    title: Stefan Droste, Thomas Jansen and Ingo Wegener, On the analysis of the (1+1) evolutionary algorithm
    locator: pages 51 to 81 (the expected time on OneMax and on linear functions)
---

Black-box optimization is the problem of minimizing a function $f$ that an algorithm can learn about only by asking for the value $f(x)$ at points $x$ that it chooses. There is no formula, no gradient and no other structure. The cost of an algorithm is the number of values it asks for, not its running time, because in practice each value is a simulation, an experiment or the training of a model. The black-box complexity of a class of functions is the least expected number of values that any algorithm needs to find an optimum of every function in the class. It is the [query model](/query-model/) applied to optimization.

## In plain words

Someone has a machine with a dial and a light. You set the dial, and the light shows a number. You want the setting that gives the smallest number. You cannot open the machine, so all you can do is try settings and read the light.

Each try costs time or money, so the question is how few tries you need. With no idea of how the machine works, you may need to try almost every setting. If you know something about it, for example that close settings give close numbers, you can do much better.

## Definition

An instance is a domain $D$, a class $F$ of functions $f : D \to \mathbb{R}$, and an unknown $f \in F$. An algorithm is given $D$ and $F$, but not $f$. At step $t$, it chooses a point $x_t \in D$, which may depend on $x_1, f(x_1), \dots, x_{t-1}, f(x_{t-1})$ and on random bits, and it receives $f(x_t)$. This is a *zero-order oracle*. The goal is one of these:

- **Find an optimum.** The run ends at the first $t$ with $x_t$ a global minimum of $f$. Let $T_A(f)$ be this $t$, a random variable.
- **Approximate within a budget.** After $B$ values, return a point $x$ and measure $f(x) - f^*$.

The *black-box complexity* of $F$ is $\inf_A \sup_{f \in F} \mathbb{E}[T_A(f)]$, where $A$ ranges over all randomized algorithms. It is a [lower bound](/lower-bound/) for every algorithm, including every [metaheuristic](/metaheuristic/), and it ignores the time that the algorithm spends between two values.

## Variants

- **First-order black box.** The oracle also returns $\nabla f(x)$. This is the model of [gradient descent](/gradient-descent/) and of the lower bounds of [first-order methods](/first-order-lower-bound/).
- **Comparison oracle.** The oracle only says which of two points is better. [Evolution strategies](/evolution-strategies/) and [CMA-ES](/cma-es/) use only this information.
- **Noisy black box.** The oracle returns $f(x)$ plus random noise, as in simulation and in [stochastic approximation](/stochastic-approximation/).
- **Restricted black-box models.** Lehre and Witt, and others after them, restrict the algorithm to unbiased moves or to the ranks of the values, to model what [genetic algorithms](/genetic-algorithm/) and other heuristics can do.
- **Expensive black box.** The budget is a few hundred values or fewer, which is the setting of Bayesian optimization with a [Gaussian process](/gaussian-process/).

## Examples

**Needle in a haystack.** $D = \{0, 1\}^n$ and $F$ is the set of the $2^n$ functions that are 0 at one point and 1 elsewhere. Any algorithm needs $(2^n + 1)/2$ values on average over $F$, and so in the worst case of the expectation. *Proof.* A value tells only whether the needle is at that point, so a deterministic algorithm that has not found it has learned only the set of points it has asked for. So each deterministic algorithm is a fixed order of distinct points, and over the $2^n$ positions of the needle it needs $1, 2, \dots, 2^n$ values once each. A randomized algorithm is a mixture of these, and the average over $F$ of its expected time is again $(2^n + 1)/2$, so the largest expected time is at least that. Random search without repeats reaches this. $\square$

**Generalized OneMax.** $D = \{0, 1\}^n$ and $F = \{f_a : a \in \{0, 1\}^n\}$ with $f_a(x) = $ the number of positions where $x$ and $a$ differ. The optimum of $f_a$ is $a$.

- *Upper bound $n + 1$.* Ask for $f_a(0)$, which is the number of ones in $a$, and for $f_a(e_i)$ for $i = 1, \dots, n - 1$, where $e_i$ has a single one at position $i$. Then $f_a(e_i) = f_a(0) - 1$ if $a_i = 1$ and $f_a(0) + 1$ otherwise, and $a_n$ follows from the number of ones. Then ask for $a$.
- *Lower bound for deterministic algorithms.* Each value is one of $n + 1$ numbers, so a deterministic algorithm is a tree in which each node asks for one point and has at most $n + 1$ children. The $2^n$ functions have distinct optima, and each optimum must be asked for at some node, so the tree has at least $2^n$ nodes. A tree of depth $q$ has at most $((n+1)^q - 1)/n$ nodes, so $q \ge \log_{n+1}(n 2^n + 1)$, which is about $n/\log_2(n+1)$. For $n = 4$ this gives $q \ge 3$, against the upper bound 5. For $n = 20$ it gives $q \ge 6$, against 21.
- *The true order.* Droste, Jansen and Wegener proved that the randomized black-box complexity of this class is $\Omega(n/\log n)$, and a method of Erdős and Rényi on coin weighing gives $O(n/\log n)$. A typical heuristic needs more: the (1+1) evolutionary algorithm, which flips each bit with probability $1/n$, needs $\Theta(n \log n)$ values on average.

**A Lipschitz function on a box.** For $L$-Lipschitz functions on $[0, 1]^n$ in the max norm, every algorithm needs at least $\lfloor L/(2\varepsilon) \rfloor^n$ values to guarantee an error below $\varepsilon$, see [global optimization](/global-optimization/), where the proof is given.

## Known algorithms

- **Random search.** Sample points from a fixed distribution and keep the best. It needs no structure and is the baseline for every other method.
- **Direct search.** Coordinate search, pattern search and the Nelder and Mead method compare values at a pattern of points, see [derivative-free optimization](/derivative-free-optimization/).
- **Model-based methods.** Fit a local model, such as a quadratic interpolant in a trust region, or a global model, such as a [Gaussian process](/gaussian-process/), and optimize the model.
- **Gradients from values.** [Finite differences](/finite-difference-method/) give an approximate gradient from $n + 1$ values, which turns the problem into a first-order one when $f$ is smooth and not noisy.
- **Metaheuristics.** [Simulated annealing](/simulated-annealing/), [genetic algorithms](/genetic-algorithm/), [evolution strategies](/evolution-strategies/), [CMA-ES](/cma-es/), [differential evolution](/differential-evolution/), the [cross-entropy method](/cross-entropy-method/) and [particle swarm optimization](/particle-swarm-optimization/).

## Bounds

- **No free lunch.** If $F$ is the set of all functions from a finite $D$ to a finite set of values, or any set closed under permutations of $D$, all algorithms have the same distribution of observed values, so none beats random search, see the [no free lunch theorem](/no-free-lunch-theorem/).
- **Finite domain with no structure.** A deterministic algorithm must ask for all $|D|$ values to be sure of the minimum, and the needle class needs $(|D| + 1)/2$ values on average.
- **Classes of bit strings.** Droste, Jansen and Wegener gave the black-box complexity of several classes: for the needle class it is $(2^n + 1)/2$, and for generalized OneMax it is between $\Omega(n/\log n)$ and $O(n/\log n)$. They also showed that some classes that are NP-hard in the white-box model have a polynomial black-box complexity, because the model does not count the time between values. So black-box complexity is a bound on information, not on computation.
- **Smooth convex functions.** With a zero-order oracle, methods that estimate gradients from values pay a factor that grows with $n$ over the first-order methods, see Larson, Menickelly and Wild.

## Reductions

- **White box to black box.** Any algorithm for the black-box problem also works when a formula is known, by using the formula only to compute values. So black-box lower bounds hold for every heuristic that uses only values, but not for algorithms that read the formula.
- **Maximization.** Maximize $f$ by minimizing $-f$.
- **Constraints.** A point outside the feasible set can be given the value $+\infty$, an "extreme barrier", or a penalty.
- **Comparisons.** An algorithm that uses only comparisons is also an algorithm for $g \circ f$ for every increasing $g$, so its run does not change when the values are transformed in this way.

## Applications

Black-box optimization is the setting of [hyperparameter tuning](/hyperparameter-tuning/) of learning methods, of engineering design with a simulator in the loop, of the calibration of physical and economic models, of experiments where each value is a measurement, and of policy search in reinforcement learning. It is also the formal model in which the theory of [evolutionary computation](/evolutionary-computation/) proves its runtime bounds.

## References
