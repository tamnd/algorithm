---
tag: 2EXWG9
kind: definition
slug: metaheuristic
name: Metaheuristic
aliases:
- meta-heuristic
area: optimization/metaheuristics
level: intro
summary: A general high-level strategy that guides a problem-specific heuristic search.
prereqs: [local-search, local-optimum, neighborhood-structure]
see_also: [stochastic-local-search, intensification-and-diversification, hyper-heuristic, no-free-lunch-theorem, tabu-search, simulated-annealing, genetic-algorithm, black-box-optimization]
sources:
  - paper: doi:10.1016/0305-0548(86)90048-1
    title: Fred Glover, Future paths for integer programming and links to artificial intelligence, Computers and Operations Research 13(5), 1986
    locator: pp. 533 to 549 (the term meta-heuristic, used for tabu search as a strategy that guides another heuristic)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Preface (the working definition of metaheuristics) and Chapters 2 to 7 (tabu search, variable neighborhood search, large neighborhood search, iterated local search, GRASP, multi-start methods)
  - paper: doi:10.1145/937503.937505
    title: Christian Blum and Andrea Roli, Metaheuristics in combinatorial optimization, overview and conceptual comparison, ACM Computing Surveys 35(3), 2003
    locator: pp. 268 to 308 (properties shared by metaheuristics, trajectory and population methods, intensification and diversification)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Chapter 2, SLS Methods, from p. 61 (simple, hybrid and population-based methods)
---

A metaheuristic is a general search strategy that is not tied to one problem and that guides problem-specific parts, such as a [neighborhood](/neighborhood-structure/), a greedy construction or a way to combine solutions, so that the search can get out of [local optima](/local-optimum/) and look at a large part of the solution space. [Tabu search](/tabu-search/), [simulated annealing](/simulated-annealing/), [iterated local search](/iterated-local-search/), [GRASP](/grasp/) and [genetic algorithms](/genetic-algorithm/) are metaheuristics. Glover used the term "meta-heuristic" in 1986 for tabu search, a strategy placed on top of another heuristic. A metaheuristic gives no guarantee of optimality or of a time to reach a good solution, in general; what it gives is a reusable design.

## Definition

There is no single formal definition. The Handbook of Metaheuristics uses this working definition: metaheuristics are "solution methods that orchestrate an interaction between local improvement procedures and higher level strategies to create a process capable of escaping from local optima and performing a robust search of a solution space."

To make this concrete, a metaheuristic is a scheme with two kinds of parts.

- **Problem-specific parts**, given by the user: a set $S$ of candidate solutions with a representation, an objective $f : S \to \mathbb{R}$, and one or more operators that make new solutions, such as a neighborhood $N(x) \subseteq S$, a randomized greedy construction, a perturbation, or a combination of two solutions.
- **Problem-independent rules**, fixed by the metaheuristic: which solutions to generate next, which to accept, what to remember, and when to stop.

The problem-independent rules must allow moves that do not improve $f$, or restarts, or both, so that the search does not stop at the first local optimum. A metaheuristic applied to a problem, with all parts chosen, is a heuristic algorithm for that problem.

Blum and Roli list common traits: metaheuristics are strategies that guide a search, they are approximate and usually non-deterministic, they use problem-specific knowledge only through the parts above, and many use memory of the search so far.

Two common ways to classify them:

- **Trajectory methods** keep one current solution and move it: tabu search, simulated annealing, iterated local search, [variable neighborhood search](/variable-neighborhood-search/), [guided local search](/guided-local-search/).
- **Population methods** keep a set of solutions and combine them: genetic algorithms, [scatter search](/scatter-search/), [ant colony optimization](/ant-colony-optimization/), [particle swarm optimization](/particle-swarm-optimization/).

## Examples and non-examples

**Examples.**

- **Iterated local search on the TSP.** On a 9-city instance of the [iterated local search](/iterated-local-search/) page, best-improvement [2-opt](/two-opt/) from the tour $0, 1, \ldots, 8$ stops at a local minimum of length 72. Iterated local search, which calls the same 2-opt descent after each random double-bridge kick, reaches 69, the optimum by enumeration. The metaheuristic is the kick-and-accept loop; 2-opt is the problem-specific part.
- **Tabu search on knapsack.** The [tabu search](/tabu-search/) page uses bit flips as the neighborhood and a [tabu list](/tabu-list/) as memory. The same tabu rules work with a 2-opt neighborhood on tours.
- **GRASP on set cover.** The [GRASP](/grasp/) page uses the greedy set cover score and a drop and swap descent. With $\alpha = 0$, which is greedy with random tie breaks, it never reaches the optimum of its example; with $\alpha = 1/2$, one iteration reaches it with probability exactly $93/200$.
- **Random restarts.** [Random-restart hill climbing](/random-restart-hill-climbing/) is a simple multi-start metaheuristic: its only rule above the descent is to start again from a random solution.

**Non-examples.**

- **Plain [hill climbing](/hill-climbing/).** A single descent stops at the first local optimum. It is a local search heuristic, and it is the usual problem-specific part inside a metaheuristic.
- **A neighborhood such as 2-opt.** It defines moves but not a strategy for which moves to take.
- **The [nearest neighbor heuristic](/nearest-neighbor-heuristic/).** It is a constructive heuristic for one problem, with no mechanism to leave its result.
- **Exact algorithms**, such as the [Held-Karp algorithm](/held-karp-algorithm/) for the TSP, which always return an optimum.
- **[Greedy set cover](/greedy-set-cover/).** It is an approximation algorithm with a proved bound, $H(d)$ times the optimum, and no search beyond the greedy steps.

## Related definitions

- **Heuristic.** A rule or algorithm that finds good solutions with no guarantee of optimality, usually for one problem. A metaheuristic is a strategy one level above it.
- **[Local search](/local-search/)** and **[local optimum](/local-optimum/).** Most trajectory metaheuristics are built around a local search and are designed to escape its local optima.
- **[Stochastic local search](/stochastic-local-search/).** Hoos and Stützle's term for local search methods with random decisions; most trajectory metaheuristics are SLS methods.
- **[Hyper-heuristic](/hyper-heuristic/).** A method that searches over heuristics, not over solutions.
- **[Intensification and diversification](/intensification-and-diversification/).** The two aims that every metaheuristic must balance.
- **[No free lunch theorem](/no-free-lunch-theorem/).** Over all objective functions on a finite set, all black-box search methods have the same average performance, so a metaheuristic can do well only by matching the structure of a class of problems.
- **[Black-box optimization](/black-box-optimization/).** The setting in which the objective can only be evaluated, which is where problem-independent rules are most useful.

## References
