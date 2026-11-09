---
tag: TQA8RV
kind: algorithm
slug: cuckoo-search
name: Cuckoo search
aliases:
- CS
area: optimization/metaheuristics
level: research
summary: A population method with two greedy phases per iteration, a heavy-tailed mutation scaled by the distance to the best point and a differential-evolution step. It combines known ES and DE operators.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {D: the number of variables, n: the number of nests, T: the number of iterations, c: the cost of one evaluation of f}
  time: {worst: O(T n (D + c))}
  space: {extra: O(n D)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 2009
  people: [Xin-She Yang, Suash Deb]
  note: Yang and Deb published cuckoo search in 2009 with a metaphor of cuckoos that lay eggs in the nests of other birds. Camacho-Villalón, Dorigo and Stützle showed in 2022 that it combines operators of evolution strategies and differential evolution.
prereqs: [population-based-search, evolution-strategies]
see_also: [differential-evolution, harmony-search, firefly-algorithm, bat-algorithm, particle-swarm-optimization, mutation, no-free-lunch-theorem, cma-es]
sources:
  - paper: doi:10.1109/NABIC.2009.5393690
    title: Xin-She Yang and Suash Deb, Cuckoo search via Lévy flights, World Congress on Nature and Biologically Inspired Computing (NaBIC 2009), IEEE, 2009
    locator: pages 210 to 214 (the three rules, the Lévy flight update and the fraction p_a of abandoned nests)
  - paper: doi:10.1504/IJMMNO.2010.035430
    title: Xin-She Yang and Suash Deb, Engineering optimisation by cuckoo search, International Journal of Mathematical Modelling and Numerical Optimisation 1(4), 2010
    locator: pages 330 to 343 (the step scaled by the difference to the best solution, and Mantegna's method for the steps)
  - paper: doi:10.1103/PhysRevE.49.4677
    title: Rosario Nunzio Mantegna, Fast, accurate algorithm for numerical simulation of Lévy stable stochastic processes, Physical Review E 49(5), 1994
    locator: pages 4677 to 4683 (the ratio u / |v|^(1/β) and the formula for σ_u)
  - paper: doi:10.1016/j.cor.2022.105747
    title: Christian Leonardo Camacho-Villalón, Marco Dorigo and Thomas Stützle, An analysis of why cuckoo search does not bring any novel ideas to optimization, Computers and Operations Research 142, 2022
    locator: article 105747 (cuckoo search described as a combination of evolution strategy and differential evolution operators, and the differences between its description and its reference code)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of methods presented through a natural metaphor)
  - paper: doi:10.1023/A:1008202821328
    title: Rainer Storn and Kenneth Price, Differential evolution, a simple and efficient heuristic for global optimization over continuous spaces, Journal of Global Optimization 11(4), 1997
    locator: pages 341 to 359 (difference vectors, binomial crossover and one-to-one selection)
  - paper: doi:10.4018/jamc.2010040104
    title: Dennis Weyland, A rigorous analysis of the harmony search algorithm, how the research community can be misled by a novel methodology, International Journal of Applied Metaheuristic Computing 1(2), 2010
    locator: pages 50 to 60 (the first detailed case of a metaphor-based method that reduces to evolution strategies)
---

Cuckoo search (CS) is a population method for minimizing a function of $D$ real variables. It keeps $n$ points, called nests, and the best point $g$ found so far. Each iteration has two phases, and in each phase every point makes one proposal and keeps it only if it is better. In the first phase the proposal adds to each coordinate a random step from a heavy-tailed law, called a Lévy flight, times the distance from the point to $g$ in that coordinate. In the second phase the proposal adds $r$ times the difference of two random points in a random subset of coordinates, which is the mutation and crossover of [differential evolution](/differential-evolution/). CS was presented with a metaphor of cuckoos that lay eggs in other birds' nests. It belongs to the family of metaphor-based methods that Sörensen (2015) criticized, and Camacho-Villalón, Dorigo and Stützle (2022) showed that it adds no new idea to [evolution strategies](/evolution-strategies/) and differential evolution. This page describes CS in those terms and makes no performance claim.

## In plain words

Keep a group of candidate points and remember the best point seen. In each round, every point tries a random jump. Most jumps are small, but a few are very large. The size of the jump in each direction grows with the distance to the best point, so the best point itself does not move. A point moves only if its jump lands on a better value.

Then every point tries a second move: in some of its coordinates, add a random fraction of the difference between two other random points. Again the point moves only if this is better. Repeat for a fixed number of rounds and return the best point seen.

## The problem

The input is a function $f : \mathbb{R}^D \to \mathbb{R}$ that can be evaluated at any point, and bounds $\ell_j < u_j$. The goal is a point of the box $B = \prod_j [\ell_j, u_j]$ with a small value of $f$.

## The algorithm

The parameters are the number of nests $n \ge 2$, the probability $p_a$, the step scale $\alpha$ (0.01 in the reference code), the index $\beta \in (0, 2)$ of the steps (1.5 in the reference code) and the number of iterations $T$.

**Lévy steps by Mantegna's method.** Draw $u \sim N(0, \sigma_u^2)$ and $v \sim N(0, 1)$ and return $L = u / |v|^{1/\beta}$, with
$$\sigma_u = \left( \frac{\Gamma(1 + \beta) \sin(\pi \beta / 2)}{\Gamma\!\left(\frac{1 + \beta}{2}\right) \beta \, 2^{(\beta - 1)/2}} \right)^{1/\beta}.$$
For $\beta = 1.5$, $\sigma_u \approx 0.6966$. The probability $P(|L| > s)$ falls like $s^{-\beta}$ for large $s$, so large steps occur far more often than with a normal law. In the test file, about 1.3 percent of 40000 steps with $\beta = 1.5$ have $|L| > 10$, while a normal law with the same median of $|L|$ gives such a step with probability below $10^{-20}$.

```pseudo id=main
CS(f, ℓ, u, n, p_a, α, β, T)
L1  x_i ← a uniform random point of the box, for i = 1..n; g ← the best x_i
L2  for t ← 1 to T do
L3      for each i: y_j ← x_ij + α · L_j · (x_ij − g_j) · N_j for each j, clipped   ▷ L_j Lévy, N_j ~ N(0, 1)
L4          if f(y) < f(x_i) then x_i ← y                                          ▷ greedy
L5      g ← the best of g and all x_i
L6      for each i: random p, q, r ~ U(0, 1); y_j ← x_ij + r (x_pj − x_qj) for each j with probability p_a, else y_j ← x_ij; clip
L7          if f(y) < f(x_i) then x_i ← y                                          ▷ greedy
L8      g ← the best of g and all x_i
L9  return g
```

The form of line L3, with the factor $(x_{ij} - g_j)$ and the extra normal factor, is the form of the reference code of Yang and Deb. The 2009 paper writes the update as $x + \alpha \oplus \text{Lévy}(\lambda)$ and gives no such factor.

**In ES and DE terms.**

- Lines L3 and L4 make, for each point, one mutation with heavy-tailed steps whose scale in coordinate $j$ is $\alpha |x_{ij} - g_j|$, followed by one-to-one $(1 + 1)$ selection. This is mutation and plus selection from [evolution strategies](/evolution-strategies/). The step sizes shrink as the points gather near $g$, which plays the role of step-size control.
- Lines L6 and L7 are a differential evolution step with base vector $x_i$, one difference vector $x_p - x_q$, a random factor $F = r$, a crossover in which each coordinate takes the mutant value with probability $p_a$, and the one-to-one selection of DE. Unlike binomial crossover in DE, no coordinate is forced to change.
- The abandoned nests of the metaphor are the points changed in line L6. Their number is not fixed: a point changes in about $p_a D$ coordinates on average, and it moves only if the proposal is better.

## Example

Let $f(x) = x_1^2 + x_2^2$, $n = 3$, $\alpha = 0.01$ and $p_a = 0.25$. The nests are $x_1 = (1, 2)$ with $f = 5$, $x_2 = (-1, 0)$ with $f = 1$, and $x_3 = (3, 1)$ with $f = 10$, so $g = x_2$.

**Line L3 for $x_3$.** Suppose the Lévy steps are $L = (2.0, -0.5)$ and the normal factors are $N = (1.0, 0.4)$. Then $y_1 = 3 + 0.01 \cdot 2.0 \cdot (3 - (-1)) \cdot 1.0 = 3.08$ and $y_2 = 1 + 0.01 \cdot (-0.5) \cdot (1 - 0) \cdot 0.4 = 0.998$. So $f(y) = 9.4864 + 0.996004 = 10.482404 > 10$, and line L4 rejects $y$.

**Line L3 for $x_2$.** Since $x_2 = g$, every factor $x_{2j} - g_j$ is 0, so $y = x_2$ and the evaluation is wasted. The best point never moves in this phase.

**Line L6 for $x_3$.** Suppose $p = 2$, $q = 1$, $r = 0.5$, and both coordinates are chosen, which has probability $0.25^2 = 0.0625$. Then $y = (3, 1) + 0.5 \cdot ((-1, 0) - (1, 2)) = (2, 0)$ with $f(y) = 4 < 10$, so $x_3 \leftarrow (2, 0)$. With $D = 2$, no coordinate is chosen with probability $0.75^2 = 0.5625$, and then $y = x_3$ and the evaluation is wasted again.

## Correctness

CS cannot certify that its result is optimal. The proofs of these invariants are below.

- **Feasibility.** All nests and proposals lie in the box, since the start points are drawn in the box and every proposal is clipped.
- **Monotone nests.** The value $f(x_i)$ of each nest never increases, and it changes only by a strict decrease, since both phases are greedy.
- **The best point.** After each iteration, $f(g)$ is the smallest value among all points evaluated so far, so it never increases.
- **The best nest is fixed in line L3.** A nest equal to $g$ proposes itself in line L3.

The page proves no convergence result. The steps of line L3 shrink with the distance to $g$, and the steps of line L6 shrink with the spread of the nests, so both can become too small to leave a local minimum once the nests gather.

## Complexity

Each proposal costs $O(D)$ work and one evaluation of $f$. Each iteration makes $2n$ proposals, so $T$ iterations cost $O(T n (D + c))$ time and $2nT$ evaluations, plus $n$ at the start. The nests take $O(n D)$ space. A comparison with another method at equal cost must count evaluations, and CS uses two per nest per iteration.

## Properties

- **Anytime and derivative-free.** $g$ is always available, and only values of $f$ are used.
- **Coordinate-wise steps.** Both phases act coordinate by coordinate, so the behavior changes if the problem is rotated.
- **Elitist.** Each nest keeps its best point, and $g$ is the best point ever evaluated.
- **Wasted evaluations.** As the example shows, some proposals equal their nest and still cost an evaluation, unless the code skips them.

## Variants and improvements

- **Modified CS.** Walton and others (2011) let the step size fall over the run and add an exchange of information among the best nests.
- **Discrete and binary CS.** The Lévy step is turned into a number of swaps or bit flips.
- **Multiobjective CS.** Yang and Deb (2013) gave a version with several objectives.
- **Hybrids.** Many papers join CS with other methods. In ES and DE terms, most of these change the mutation law, the step scale or the selection.

## When to use it

If you need a method of this kind, standard [differential evolution](/differential-evolution/), [CMA-ES](/cma-es/) and other evolution strategies have the same or more general operators, a body of theory and well-tested implementations. If you use CS, describe it by its operators as above, state whether your code follows the paper or the reference code, and compare it with standard methods on your own problems with the same number of evaluations. Published comparisons depend on the test functions, the budgets and the tuning. This page reports no comparison.

## Pitfalls

- **Description and code differ.** The factor $(x_{ij} - g_j)$ in line L3 is in the reference code, not in the 2009 description. Camacho-Villalón, Dorigo and Stützle (2022) discuss the differences between the description and the reference code. Check which rule an implementation uses before you compare results.
- **The meaning of $p_a$.** In this page, $p_a$ is the probability that a coordinate changes in line L6. It is not the fraction of nests that are replaced, and no nest is replaced by a random point.
- **Clipping.** Heavy-tailed steps often leave the box, and clipping puts many points on its border. Reflection or redrawing gives different behavior.
- **The value of $\beta$.** $\sigma_u$ goes to 0 as $\beta \to 2$, since $\sin(\pi) = 0$, so the formula is unsafe near $\beta = 2$. Use $\beta$ well inside $(0, 2)$.
- **The metaphor.** Eggs, nests and host birds name operators that already have names. Sörensen (2015) asks that methods be described by their operators.

## Implementations

## History

Yang and Deb presented cuckoo search at the NaBIC conference in 2009 and gave an engineering version in 2010, with steps from Mantegna's 1994 method for simulating Lévy stable processes. The method was widely used in applications. Weyland (2010) had shown for harmony search that a method named after a metaphor can be a special case of evolution strategies, and Sörensen (2015) criticized the general practice. Camacho-Villalón, Dorigo and Stützle (2022) analyzed CS and its reference code in detail and concluded that it combines elements of evolution strategies and differential evolution and contains no new idea for optimization.

## References
