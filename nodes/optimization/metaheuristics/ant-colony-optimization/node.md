---
tag: H2R48A
kind: algorithm
slug: ant-colony-optimization
name: Ant colony optimization
aliases:
- ACO
- ant system
- MAX-MIN ant system
- MMAS
area: optimization/metaheuristics
level: advanced
summary: Ants build tours part by part, with probabilities set by pheromone and a heuristic, and good tours add pheromone. With pheromone bounds the optimum is found with probability 1.
solves: [traveling-salesman-problem]
model: real-ram
complexity:
  vars: {n: the number of cities, m: the number of ants, T: the number of iterations}
  time: {worst: O(T m n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 1991
  people: [Marco Dorigo, Vittorio Maniezzo, Alberto Colorni]
  note: Dorigo, Maniezzo and Colorni proposed the Ant System in 1991, and Dorigo's 1992 thesis developed it. Stützle and Hoos gave MAX-MIN Ant System in 1997, and Gutjahr gave the first convergence proof in 2000.
prereqs: [swarm-intelligence, traveling-salesman-problem]
see_also: [two-opt, lin-kernighan, nearest-neighbor-heuristic, quadratic-assignment-problem, estimation-of-distribution-algorithm, roulette-wheel-selection, particle-swarm-optimization, stochastic-local-search]
sources:
  - paper: doi:10.1109/3477.484436
    title: Marco Dorigo, Vittorio Maniezzo and Alberto Colorni, Ant system, optimization by a colony of cooperating agents, IEEE Transactions on Systems, Man, and Cybernetics, Part B 26(1), 1996
    locator: pages 29 to 41 (the random proportional rule, evaporation and deposit of Ant System)
  - paper: doi:10.1016/S0167-739X(00)00043-1
    title: Thomas Stützle and Holger H. Hoos, MAX-MIN Ant System, Future Generation Computer Systems 16(8), 2000
    locator: pages 889 to 914 (the pheromone bounds, the best-so-far and iteration-best updates, and the initialization at the upper bound)
  - paper: doi:10.1109/TEVC.2002.802444
    title: Thomas Stützle and Marco Dorigo, A short convergence proof for a class of ant colony optimization algorithms, IEEE Transactions on Evolutionary Computation 6(4), 2002
    locator: pages 358 to 365 (convergence in value with a positive lower bound on the pheromone, and the limit of the pheromone after the optimum is found)
  - paper: Walter J. Gutjahr, A graph-based ant system and its convergence, Future Generation Computer Systems 16(8), 2000
    title: A graph-based ant system and its convergence
    locator: pages 873 to 888 (the first convergence proof for an ant colony algorithm)
  - paper: Walter J. Gutjahr, ACO algorithms with guaranteed convergence to the optimal solution, Information Processing Letters 82(3), 2002
    title: ACO algorithms with guaranteed convergence to the optimal solution
    locator: pages 145 to 153 (convergence in solution with a slowly decreasing lower bound or evaporation rate)
  - book: isbn:9780262042192
    title: Marco Dorigo and Thomas Stützle, Ant Colony Optimization, MIT Press, 2004
    locator: Chapter 3 (ant colony algorithms for the traveling salesman problem) and Chapter 4 (the theory of convergence)
  - paper: Marco Dorigo and Luca Maria Gambardella, Ant colony system, a cooperative learning approach to the traveling salesman problem, IEEE Transactions on Evolutionary Computation 1(1), 1997
    title: Ant colony system, a cooperative learning approach to the traveling salesman problem
    locator: pages 53 to 66 (the pseudo-random proportional rule and the local pheromone update)
---

Ant colony optimization (ACO) is a [swarm intelligence](/swarm-intelligence/) method for combinatorial problems in which artificial ants build solutions part by part. Each ant chooses the next part at random, with probability proportional to a pheromone value learned during the run and a fixed heuristic value, and after each iteration the pheromone evaporates and the parts of good solutions receive more. On the [traveling salesman problem](/traveling-salesman-problem/), a part is an edge between two cities, and the heuristic value is the inverse of its length. With pheromone values kept in an interval $[\tau_{\min}, \tau_{\max}]$ with $\tau_{\min} > 0$, as in MAX-MIN Ant System, the optimal tour is found with probability tending to 1 (Stützle and Dorigo 2002), but the proof gives no useful bound on the time.

## In plain words

Real ants leave a scent on their way, and they prefer paths with more scent. Short paths collect scent fastest, so the colony comes to use them. Here, each artificial ant builds a full tour through all cities. At each city it picks the next one at random, and it prefers cities that are close and edges that have a lot of scent.

After all ants have built their tours, every scent value fades a little. Then the edges of the best tour found so far get more scent. Over many rounds the scent gathers on the edges of good tours, and the ants build tours close to them. A floor and a ceiling on the scent keep every edge possible and stop one tour from taking over too early.

## The problem

The input is a symmetric [traveling salesman problem](/traveling-salesman-problem/): $n \ge 3$ cities and distances $d_{ij} = d_{ji} > 0$ for $i \ne j$. A tour is a cyclic order of all cities, and its length $L$ is the sum of the distances of its $n$ edges. The goal is a tour of minimum length $L^*$. ACO applies to any problem whose solutions can be built step by step from parts, such as the [quadratic assignment problem](/quadratic-assignment-problem/) and scheduling problems, but this page uses the TSP.

The parameters are the number of ants $m$, the weights $\alpha$ and $\beta$ of pheromone and heuristic, the evaporation rate $\rho \in (0, 1]$, the start value $\tau_0$, the bounds $\tau_{\min} \le \tau_0 \le \tau_{\max}$, and the number of iterations $T$.

## The algorithm

The pheromone $\tau_{ij}$ sits on edge $\{i, j\}$, and the heuristic value is $\eta_{ij} = 1/d_{ij}$. The algorithm below is MAX-MIN Ant System with the best-so-far tour as the only tour that deposits pheromone.

```pseudo id=main
MMAS(d, m, α, β, ρ, τ_0, τ_min, τ_max, T)
L1  τ_ij ← τ_0 for all i, j; best ← none, L(best) ← ∞
L2  for t ← 1 to T do
L3      each of the m ants builds a tour: start at a uniform random city, and from city i
        move to an unvisited city j with probability τ_ij^α η_ij^β / Σ_{l unvisited} τ_il^α η_il^β
L4      ib ← the shortest of the m tours
L5      if L(ib) < L(best) then best ← ib
L6      τ_ij ← (1 − ρ) τ_ij for all i, j                       ▷ evaporation
L7      τ_ij ← τ_ij + 1/L(best) for each edge {i, j} of best   ▷ deposit
L8      τ_ij ← min(τ_max, max(τ_min, τ_ij)) for all i, j      ▷ the bounds
L9  return best
```

The rule of line L3 is the random proportional rule of Ant System. It is a [roulette wheel](/roulette-wheel-selection/) over the unvisited cities with weights $\tau_{ij}^\alpha \eta_{ij}^\beta$. With $\alpha = 0$ it is a randomized [nearest neighbor heuristic](/nearest-neighbor-heuristic/). Stützle and Hoos set $\tau_{\max} = 1/(\rho L(best))$, start at $\tau_0 = \tau_{\max}$ and set $\tau_{\min}$ to a fraction of $\tau_{\max}$. With $\tau_{\min} = 0$ and $\tau_{\max} = \infty$, line L8 does nothing.

## Example

Take 4 cities with $d_{12} = 2$, $d_{13} = 4$, $d_{14} = 5$, $d_{23} = 3$, $d_{24} = 5$ and $d_{34} = 2$. The three distinct tours have lengths 12 (1-2-3-4-1), 13 (1-2-4-3-1) and 17 (1-3-2-4-1), so $L^* = 12$. Let $\alpha = 1$, $\beta = 2$, $\rho = 0.1$ and $\tau_0 = \tau_{\max} = 1/(\rho L^*) = 0.8333$.

**The first choice.** All pheromone values are equal, so an ant at city 1 weighs the cities 2, 3 and 4 by $1/d^2 = 0.25, 0.0625, 0.04$. The probabilities are $0.7092$, $0.1773$ and $0.1135$. From city 2, the weights of 3 and 4 are $1/9$ and $1/25$, so city 3 follows with probability $0.7353$, and then city 4 is forced. An ant that starts at city 1 builds the optimal tour, in one of its two directions, with probability $0.7092 \cdot 0.7353 + 0.1135 \cdot 0.8621 = 0.6193$.

**The update.** Suppose that the best tour is 1-2-3-4-1. Line L6 sets every value to $0.9 \cdot 0.8333 = 0.75$. Line L7 adds $1/12 = 0.0833$ to the edges 12, 23, 34 and 41, which return to $0.8333$. Now an ant at city 1 weighs 2, 3 and 4 by $0.8333 \cdot 0.25$, $0.75 \cdot 0.0625$ and $0.8333 \cdot 0.04$, with probabilities $0.7220$, $0.1625$ and $0.1155$.

**The long run.** While the tour stays the best, its edges stay at $\tau_{\max}$, because $0.9 \tau_{\max} + 1/12 = \tau_{\max}$ exactly. The other two edges shrink by the factor 0.9 per iteration until they reach $\tau_{\min}$. With $\tau_{\min} = \tau_{\max}/(2n) = \tau_{\max}/8$, this takes 20 iterations, since $0.9^{19} > 1/8 > 0.9^{20}$.

## Correctness

ACO cannot certify optimality. Its correctness consists of bounds on the pheromone and a convergence statement. The full proofs are below.

- **Bounds.** After line L8, each $\tau_{ij}$ lies in $[\tau_{\min}, \tau_{\max}]$. Without the clamp, each value stays below $\max(\tau_0, 1/(\rho L^*))$, because each step multiplies by $1 - \rho$ and adds at most $1/L(best) \le 1/L^*$.
- **The best tour.** Lines L4 and L5 keep $best$ as a shortest tour among all tours built so far, so $L(best)$ never increases.
- **Convergence in value.** If $\tau_{\min} > 0$, every tour, the optimal one included, is built by one ant with probability at least some $p_{\min} > 0$ in every iteration. So the probability that no optimal tour has been built after $t$ iterations is at most $(1 - p_{\min})^t$, which tends to 0. Stützle and Dorigo (2002) proved this for a class of ACO algorithms that includes MMAS. They also showed that, once the best tour is optimal, its edges converge to $\min(\tau_{\max}, 1/(\rho L^*))$, and all other edges reach $\tau_{\min}$ in finitely many iterations.
- **Convergence in solution.** Gutjahr (2000, 2002) proved the stronger statement that the probability of building an optimal tour in the current iteration tends to 1, for variants in which $\tau_{\min}$ or $\rho$ decreases slowly with time.

The bound $p_{\min}$ is tiny for large $n$, so these results give no useful bound on the time. Runtime analyses for simple ACO algorithms on simple problems exist and are in the book of Dorigo and Stützle and later papers.

## Complexity

In line L3, one ant makes $n - 1$ choices, and each choice computes the weights of up to $n - 1$ unvisited cities, so one tour costs $O(n^2)$ and $m$ tours cost $O(m n^2)$. Lines L6 to L8 touch each of the $n^2$ pheromone values a constant number of times. So one iteration costs $O(m n^2)$ and $T$ iterations cost $O(T m n^2)$. The pheromone matrix takes $O(n^2)$ space. With candidate lists of the $k$ nearest cities, a choice costs $O(k)$ in most steps, and a tour costs $O(n k)$ in practice.

## Properties

- **Randomized and anytime.** $best$ is a valid tour at any time, and its length never increases.
- **Constructive.** Ants build solutions from parts, unlike the methods of [local search](/local-search/), which change complete solutions. The pheromone is a probability model over solutions, which relates ACO to [estimation of distribution algorithms](/estimation-of-distribution-algorithm/).
- **Bounded pheromone.** With $\tau_{\min} > 0$, every edge keeps a positive probability, which prevents the search from locking onto one tour.
- **Problem-specific heuristic.** The heuristic values $\eta_{ij}$ bring knowledge of the problem into every choice.

## Variants and improvements

- **Ant System.** The first form: every ant deposits $Q/L_k$ on the edges of its tour $k$, with no bounds and no elite tour.
- **Elitist and rank-based Ant System.** The best-so-far tour, or the best few tours with weights by rank, deposit extra pheromone.
- **Ant Colony System.** Dorigo and Gambardella (1997) let an ant take the best edge with probability $q_0$ and use the random proportional rule otherwise, decrease the pheromone of an edge as soon as an ant uses it, and let only the best-so-far tour deposit.
- **MAX-MIN Ant System.** This page. The iteration-best tour can deposit instead of the best-so-far tour, which gives a weaker pull toward one tour.
- **ACO with local search.** Each tour is improved by [2-opt](/two-opt/), [3-opt](/three-opt/) or [Lin-Kernighan](/lin-kernighan/) before the update. Most strong ACO results on the TSP use such a local search.
- **Continuous domains.** ACO for real variables replaces the pheromone matrix by a mixture of Gaussian kernels centered at good solutions.

## When to use it

ACO fits combinatorial problems where a solution is built part by part and a good greedy heuristic gives the values $\eta$, such as routing, sequencing and assignment problems with side constraints. For the plain TSP, specialized methods exist: exact branch and cut codes solve large instances to optimality, and [Lin-Kernighan](/lin-kernighan/) style local search gives very good tours fast. Compare ACO with such methods on your own instances and with the same time budget before you choose it.

## Pitfalls

- **Stagnation without bounds.** In Ant System with strong deposits, the pheromone of one tour can grow until every ant builds that tour. Line L8 with $\tau_{\min} > 0$ prevents this, and so does a restart of the pheromone.
- **The scale of $\tau$.** The deposit $1/L$ depends on the unit of length. Set $\tau_0$, $\tau_{\min}$ and $\tau_{\max}$ from the same scale, for example from the length of a [nearest neighbor](/nearest-neighbor-heuristic/) tour.
- **Large exponents.** Large $\beta$ with small distances, or large $\alpha$, can make the weights of line L3 overflow or underflow. Normalize the distances or compute the weights in log space.
- **Zero distances.** $\eta_{ij} = 1/d_{ij}$ is undefined for $d_{ij} = 0$. Merge such cities, or use $1/(d_{ij} + \epsilon)$.
- **Asymmetric problems.** For an asymmetric TSP, keep $\tau_{ij}$ and $\tau_{ji}$ apart, and deposit only in the direction of the tour.

## Implementations

## History

Dorigo, Maniezzo and Colorni introduced the Ant System in 1991, inspired by the experiments of Deneubourg and coworkers on the foraging of Argentine ants, and Dorigo's 1992 doctoral thesis at the Politecnico di Milano developed it. The journal paper appeared in 1996. Dorigo and Gambardella gave Ant Colony System in 1997, and Stützle and Hoos gave MAX-MIN Ant System in 1997, with the journal version in 2000. Dorigo, Di Caro and Gambardella described ACO as a general metaheuristic in 1999. Gutjahr (2000) proved the first convergence result, and Stützle and Dorigo (2002) gave a short proof of convergence in value for MMAS-type algorithms. The book of Dorigo and Stützle (2004) covers the field to that date.

## References
