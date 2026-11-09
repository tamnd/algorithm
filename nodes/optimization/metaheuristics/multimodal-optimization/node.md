---
tag: BATDJ3
kind: problem
slug: multimodal-optimization
name: Multimodal optimization
aliases:
- niching problem
- finding multiple optima
area: optimization/metaheuristics
level: advanced
summary: Find several optima of a function in one run, usually all the global optima or all good local ones, instead of a single best point.
prereqs: [global-optimization, local-optimum]
see_also: [premature-convergence, genetic-algorithm, fitness-landscape, intensification-and-diversification, cma-es, particle-swarm-optimization, pareto-front, coupon-collector-problem]
sources:
  - paper: "David E. Goldberg and Jon Richardson, Genetic algorithms with sharing for multimodal function optimization, Proceedings of the Second International Conference on Genetic Algorithms, Lawrence Erlbaum, 1987"
    title: David E. Goldberg and Jon Richardson, Genetic algorithms with sharing for multimodal function optimization
    locator: pages 41 to 49 (fitness sharing, the sharing function and the test functions with five peaks)
  - paper: "Samir W. Mahfoud, Niching methods for genetic algorithms, PhD thesis, University of Illinois at Urbana-Champaign, 1995"
    title: Samir W. Mahfoud, Niching methods for genetic algorithms
    locator: the chapters on crowding and deterministic crowding, and on the comparison of niching methods
  - paper: doi:10.1016/j.swevo.2011.05.005
    title: Swagatam Das, Sayan Maity, Bo-Yang Qu and Ponnuthurai N. Suganthan, Real-parameter evolutionary multimodal optimization, a survey of the state-of-the-art, Swarm and Evolutionary Computation 1(2), 2011
    locator: pages 71 to 88 (the classes of niching methods and the measures of performance)
  - book: doi:10.1007/978-3-319-07407-8
    title: Mike Preuss, Multimodal Optimization by Means of Evolutionary Algorithms, Springer, 2015
    locator: Chapter 2 (the definitions of the problem and of basins) and Chapter 3 (the measures of performance)
  - paper: "Xiaodong Li, Andries Engelbrecht and Michael G. Epitropakis, Benchmark functions for CEC 2013 special session and competition on niching methods for multimodal function optimization, technical report, RMIT University, 2013"
    title: Xiaodong Li, Andries Engelbrecht and Michael G. Epitropakis, Benchmark functions for CEC 2013 niching competition
    locator: the definitions of the peak ratio and the success rate, with the accuracy levels
---

Multimodal optimization is the problem of finding several optima of a function in one run: usually all the global optima, or all the [local optima](/local-optimum/) whose value is good enough. A user may want a set of different good designs to choose from, or may need all solutions of an inverse problem. Standard [global optimization](/global-optimization/) methods are built to converge to one point, so a population tends to collapse on a single optimum, which is [premature convergence](/premature-convergence/) for this problem. Niching methods, such as fitness sharing and crowding, keep the population spread over several optima. The number of optima can be exponential in the dimension, so finding all of them is impossible in general.

## In plain words

Usually you want the single best answer. Sometimes you want all the good answers. A landscape can have several valleys that are just as deep, or several that are almost as deep, and each valley is a different solution. You may want to see them all, so you can pick one later for other reasons, such as cost or safety.

A search that always follows the best point it has seen ends in one valley. To find many valleys, the search must stop its members from crowding into the same one. That is what niching does: it makes a crowded valley less attractive, so that some members stay in the other valleys.

## Definition

An instance is a function $f : D \to \mathbb{R}$ to minimize, a distance $d$ on $D$, an accuracy $\varepsilon \ge 0$ and a radius $r > 0$. Let $G = \{g_1, \dots, g_K\}$ be the set of global minima, assumed finite and with $d(g_i, g_j) > 2r$ for $i \ne j$. A finite set $P \subseteq D$ of returned points *finds* $g_i$ if some $p \in P$ has $d(p, g_i) \le r$ and $f(p) - f(g_i) \le \varepsilon$.

- **All global optima.** Return $P$ that finds every $g_i$. The *peak ratio* of $P$ is the fraction of the $K$ optima that it finds, and a run is a *success* if the peak ratio is 1. These are the measures of the CEC 2013 niching benchmark of Li, Engelbrecht and Epitropakis.
- **All good local optima.** Replace $G$ by the set of local minima with $f(x) \le f^* + \delta$ for a given $\delta$.
- **The $k$ best diverse solutions.** Return $k$ points, pairwise at distance at least $r$, with the least sum or the least largest value of $f$.

The *basin* of a local minimum $m$, for a given local method, is the set of starts from which that method converges to $m$. The basins describe how hard each optimum is to find.

## Variants

- **Continuous or combinatorial.** On a discrete space, $d$ is the number of moves between solutions or the Hamming distance.
- **Known or unknown number of optima.** Many niching methods need $K$ or the radius $r$ in advance. Methods that estimate them are harder to design.
- **Multi-objective view.** Treat diversity as a second objective and look for a [Pareto front](/pareto-front/) of value against distance to the other points.
- **Robust optima.** Prefer the optima with wide basins, which keep their value when the solution is perturbed.

## Examples

**Five equal peaks.** $f(x) = \sin^6(5\pi x)$ on $[0, 1]$ has five global maxima, at $x = 0.1, 0.3, 0.5, 0.7, 0.9$, all with value 1. Goldberg and Richardson used it and a variant with peaks of falling height to test fitness sharing.

**Himmelblau's function.** $f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2$ has four global minima with value 0, at $(3, 2)$ and near $(-2.8051, 3.1313)$, $(-3.7793, -3.2832)$ and $(3.5844, -1.8481)$. Gradient descent with step $0.002$ and 3000 steps, kept inside $[-6, 6]^2$, was started from the $200 \times 200$ cell centers of that square. Every start converged to one of the four minima, and the fractions of the starts were $0.2497$, $0.2583$, $0.2432$ and $0.2488$. With these basin sizes, the expected number of random starts until all four minima are found is
$$\sum_{\emptyset \ne S \subseteq \{1, 2, 3, 4\}} \frac{(-1)^{|S|+1}}{\sum_{i \in S} p_i} \approx 8.339,$$
close to the [coupon collector](/coupon-collector-problem/) value $4(1 + \tfrac12 + \tfrac13 + \tfrac14) = 8.333$ for equal basins. Over 100 runs of this multistart (seeds 0 to 99), with starts drawn uniformly from the square, the mean number of starts was 8.62 and the largest was 18.

**Exponentially many optima.** The Rastrigin function on $[-5.12, 5.12]^n$ has $11^n$ local minima, see [global optimization](/global-optimization/). Listing all good local optima is then out of reach even for moderate $n$.

## Known algorithms

- **Multistart with clustering.** Start a local method from many points, and group the end points by distance. Simple and strong when the local method is cheap and the basins are not too small.
- **Fitness sharing** (Goldberg and Richardson, 1987). Divide the fitness of each member of a [genetic algorithm](/genetic-algorithm/) population by its niche count $\sum_j \operatorname{sh}(d_{ij})$, where $\operatorname{sh}(d) = 1 - (d/\sigma)^\alpha$ for $d < \sigma$ and 0 otherwise. Members in a crowded region lose fitness, so the population spreads over the peaks.
- **Crowding and deterministic crowding** (De Jong, 1975; Mahfoud, 1992). Each child competes only with the most similar parent or member, so it can replace only a solution in its own region.
- **Clearing** (Pétrowski, 1996). Within each radius, only the best few members keep their fitness, and the others get the worst value.
- **Speciation and restricted tournament selection.** Form species around seeds, or let a child compete with the closest of a random sample of members.
- **Niching in other metaheuristics.** Versions of [particle swarm optimization](/particle-swarm-optimization/) with local neighborhoods, [differential evolution](/differential-evolution/) with crowding, and restarts of [CMA-ES](/cma-es/) with tabu regions around the optima already found.
- **Sequential niching.** Find one optimum, change $f$ to penalize a region around it, and repeat.

## Bounds

- **The number of optima.** A function can have exponentially many global optima, as $f(x) = \prod_i \cos^2(\pi x_i)$ on $[0.5, k + 0.5]^n$ has its $k^n$ global maxima, with value 1, at the integer points. Any method that returns all of them needs time at least $k^n$ to write them down.
- **Multistart.** If each start of a local method reaches optimum $i$ with probability $p_i$, independently, the expected number of starts until all $K$ optima are found is $\sum_{\emptyset \ne S} (-1)^{|S|+1}/\sum_{i \in S} p_i$. With equal basins this is $K H_K \approx K \ln K$. With one basin of probability $p_{\min}$, it is at least $1/p_{\min}$, which can be arbitrarily large.
- **Black box.** A global optimum with a basin of tiny volume is a needle, and no method that sees only values can find it fast, see [black-box optimization](/black-box-optimization/).
- **Niching methods.** For fitness sharing, Goldberg and Richardson argue that at equilibrium the number of members on each peak is proportional to its height, when the peaks are farther apart than $\sigma$. This is an approximate argument for an idealized model, not a theorem about the finite algorithm. For the full methods there are few runtime results.

## Reductions

- **To repeated global optimization.** Sequential niching reduces the problem to a sequence of global problems on modified functions. Each penalty can create false optima at the border of the penalized region.
- **To clustering.** Multistart reduces it to local optimization followed by the clustering of the end points.
- **From multi-objective optimization.** Finding many points of a [Pareto front](/pareto-front/) has the same need for diversity, and methods such as [NSGA-II](/nsga-ii/) use a crowding distance for the same reason as niching.

## Applications

Multimodal optimization is used in engineering design, where several designs that are almost equally good can differ in cost or in ease of manufacture, in inverse problems in physics and medicine, which can have several solutions that fit the data, in the search for several low-energy structures of molecules, and in the analysis of a [fitness landscape](/fitness-landscape/) to see how many good regions it has.

## References
