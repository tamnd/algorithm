---
tag: YB0SC1
kind: algorithm
slug: harmony-search
name: Harmony search
aliases:
- HS
area: optimization/metaheuristics
level: research
summary: Build a vector coordinate by coordinate from a memory of good vectors, with small random changes and resets, and let it replace the worst one. It is a special case of a (μ+1) evolution strategy.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {D: the number of variables, H: the size of the harmony memory, T: the number of iterations, c: the cost of one evaluation of f}
  time: {worst: O(T (D + H + c))}
  space: {extra: O(H D)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 2001
  people: [Zong Woo Geem, Joong Hoon Kim, G. V. Loganathan]
  note: Geem, Kim and Loganathan published harmony search in 2001 with a metaphor of musical improvisation. Weyland showed in 2010 that it is a special case of evolution strategies.
prereqs: [population-based-search, evolution-strategies]
see_also: [crossover, mutation, differential-evolution, genetic-algorithm, cuckoo-search, firefly-algorithm, bat-algorithm, no-free-lunch-theorem]
sources:
  - paper: doi:10.1177/003754970107600201
    title: Zong Woo Geem, Joong Hoon Kim and G. V. Loganathan, A new heuristic optimization algorithm, harmony search, Simulation 76(2), 2001
    locator: pages 60 to 68 (the harmony memory, the memory considering rate, the pitch adjusting rate, and the replacement of the worst harmony)
  - paper: doi:10.1016/j.cma.2004.09.007
    title: Kang Seok Lee and Zong Woo Geem, A new meta-heuristic algorithm for continuous engineering optimization, harmony search theory and practice, Computer Methods in Applied Mechanics and Engineering 194(36-38), 2005
    locator: pages 3902 to 3933 (the continuous version with the bandwidth bw)
  - paper: doi:10.1016/j.amc.2006.11.033
    title: M. Mahdavi, M. Fesanghary and E. Damangir, An improved harmony search algorithm for solving optimization problems, Applied Mathematics and Computation 188(2), 2007
    locator: pages 1567 to 1579 (PAR that grows and bw that shrinks during the run)
  - paper: doi:10.4018/jamc.2010040104
    title: Dennis Weyland, A rigorous analysis of the harmony search algorithm, how the research community can be misled by a novel methodology, International Journal of Applied Metaheuristic Computing 1(2), 2010
    locator: pages 50 to 60 (harmony search as a special case of evolution strategies, and the critique of its claims)
  - paper: doi:10.1023/A:1015059928466
    title: Hans-Georg Beyer and Hans-Paul Schwefel, Evolution strategies, a comprehensive introduction, Natural Computing 1(1), 2002
    locator: pages 3 to 52 (the (μ+λ) selection, discrete recombination and mutation, for the comparison)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of methods named after metaphors, with harmony search as a main example)
  - paper: doi:10.1007/s11721-021-00202-9
    title: Claus Aranha, Christian L. Camacho Villalón, Felipe Campelo, Marco Dorigo, Rubén Ruiz, Marc Sevaux, Kenneth Sörensen and Thomas Stützle, Metaphor-based metaheuristics, a call for action, the elephant in the room, Swarm Intelligence 16(1), 2022
    locator: pages 1 to 6 (the case for describing such methods in standard terms)
  - paper: doi:10.1016/j.swevo.2016.01.005
    title: M. P. Saka, O. Hasançebi and Z. W. Geem, Metaheuristics in structural optimization and discussions on harmony search algorithm, Swarm and Evolutionary Computation 28, 2016
    locator: pages 88 to 97 (a reply by authors of harmony search to the critique)
---

Harmony search (HS) is a population method for minimizing a function of $D$ variables. It keeps a memory of $H$ vectors. Each iteration builds one new vector coordinate by coordinate: with probability HMCR it copies the coordinate from a random vector of the memory and, with probability PAR, adds a small random step of width bw, and otherwise it draws the coordinate at random. The new vector replaces the worst vector of the memory if it is better. HS was presented with a metaphor of musicians who improvise. Weyland (2010) showed that it is a special case of a $(\mu + 1)$ [evolution strategy](/evolution-strategies/): the memory is the population, copying coordinates from random members is global discrete recombination, the small step and the random draw are mutations, and replacing the worst is $(\mu + 1)$ selection. This page describes HS in those terms and makes no performance claim.

## In plain words

Keep a short list of good candidate answers. To make a new candidate, fill in its numbers one at a time. For most numbers, copy the number in the same place from a random member of the list, and sometimes move it a little up or down. For the other numbers, pick any allowed value at random.

If the new candidate is better than the worst one on the list, it takes that place. Otherwise throw it away. Repeat many times and return the best candidate on the list.

This is a known kind of evolutionary method: one child per step, made by mixing many parents and by small random changes, which then competes with the worst parent.

## The problem

The input is a function $f : \mathbb{R}^D \to \mathbb{R}$ that can be evaluated at any point, and bounds $\ell_j < u_j$. The goal is a point of the box $B = \prod_j [\ell_j, u_j]$ with a small value of $f$. Discrete versions use a finite set of values for each coordinate, with the pitch step moving to a neighboring value.

## The algorithm

The parameters are the memory size $H$ (HMS), the memory considering rate $\text{HMCR} \in [0, 1]$, the pitch adjusting rate $\text{PAR} \in [0, 1]$, the bandwidth $\text{bw} \ge 0$ and the number of iterations $T$.

```pseudo id=main
HS(f, ℓ, u, H, HMCR, PAR, bw, T)
L1  M ← H uniform random points of the box, with their values
L2  for t ← 1 to T do
L3      build x: for each coordinate j independently,
            with probability HMCR: x_j ← M[r]_j for a uniform random r       ▷ memory
                then with probability PAR: x_j ← x_j + bw · U(−1, 1), clipped   ▷ pitch adjustment
            otherwise: x_j ← U(ℓ_j, u_j)                                       ▷ random selection
L4      w ← a vector of M with the largest value
L5      if f(x) < f(w) then replace w by x
L6  return a vector of M with the smallest value
```

**The same method in ES terms.** Write $\mu = H$. Line L3 makes one offspring from the $\mu$ parents of $M$: in each coordinate, with probability HMCR it takes the value of a uniform random parent, which is **global discrete recombination**, and then a **uniform mutation** of width bw with probability PAR. With probability $1 - \text{HMCR}$ it applies a **uniform reset mutation**. Lines L4 and L5 keep the $\mu$ best of the $\mu + 1$ individuals, which is **$(\mu + 1)$ selection**. So HS is a $(\mu + 1)$-ES with these operators, and the test file checks that the two formulations give the same run, step by step, from the same random numbers.

| harmony search | evolution strategy |
|---|---|
| harmony memory, size HMS | population, size $\mu$ |
| new harmony | one offspring, $\lambda = 1$ |
| memory consideration, rate HMCR | global discrete recombination, per coordinate |
| pitch adjustment, PAR and bw | uniform mutation, rate and width |
| random selection, rate $1 - \text{HMCR}$ | uniform reset mutation |
| replace the worst harmony | $(\mu + 1)$ selection |

## Example

Let $f(x) = x_1^2 + x_2^2$ on $[-5, 5]^2$, $H = 3$, $\text{HMCR} = 0.9$, $\text{PAR} = 0.3$ and $\text{bw} = 0.2$. The memory holds $(1, 2)$ with $f = 5$, $(-1, 0)$ with $f = 1$ and $(3, 1)$ with $f = 10$.

**Building $x$.** For coordinate 1, suppose memory is used and picks the second vector, so $x_1 = -1$, and the pitch is adjusted with $U = 0.5$, so $x_1 = -1 + 0.2 \cdot 0.5 = -0.9$. For coordinate 2, suppose memory is used, picks the second vector again and does not adjust, so $x_2 = 0$. Then $x = (-0.9, 0)$ and $f(x) = 0.81$.

**Replacement.** The worst vector is $(3, 1)$ with $f = 10 > 0.81$, so $x$ replaces it. The memory is now $(1, 2)$, $(-1, 0)$ and $(-0.9, 0)$, and its best value has dropped from 1 to 0.81.

**The probabilities.** A coordinate is the unchanged value of a given memory vector with probability $\text{HMCR}(1 - \text{PAR})/H = 0.9 \cdot 0.7 / 3 = 0.21$, it is a pitch-adjusted memory value with probability $0.9 \cdot 0.3 = 0.27$, and it is a random draw with probability $0.1$. With $D$ coordinates, a new vector has no random-draw coordinate with probability $0.9^D$, about 0.35 for $D = 10$.

## Correctness

HS cannot certify that its result is optimal. The proofs of these statements are below.

- **Feasibility.** All vectors lie in the box: random draws are in the box, memory values are in the box, and pitch steps are clipped.
- **Monotone memory.** For each $r$, the $r$-th smallest value in the memory never increases, since a vector enters only in place of a worst vector with a strictly larger value. So the best value never increases.
- **Equivalence.** With the same random numbers, HS and the $(\mu + 1)$-ES above produce the same memory after every iteration, when ties in line L4 are broken in the same way.
- **Convergence in value.** If $\text{HMCR} < 1$ and $f$ is continuous on $B$, then for every $\varepsilon > 0$ the best value is below $\min_B f + \varepsilon$ after $t$ iterations with probability at least $1 - (1 - q_\varepsilon)^t$, for some $q_\varepsilon > 0$. The proof uses only the random-selection part: every coordinate is a fresh random draw with probability $(1 - \text{HMCR})^D$. It is the same argument as for pure random search, so it says nothing about speed.

## Complexity

Line L3 costs $O(D)$, line L4 costs $O(H)$ in the simple form, and each iteration makes one evaluation of $f$. So $T$ iterations cost $O(T (D + H + c))$ time, and the memory takes $O(H D)$ space. A heap on the values makes line L4 cost $O(\log H)$. HS makes one evaluation per iteration, so a budget of $E$ evaluations allows $T = E - H$ iterations.

## Properties

- **Coordinate-wise variation.** Each coordinate of the new vector is chosen independently, so the method works best on functions that are close to separable, and its behavior changes if the problem is rotated.
- **Steady state.** One new vector per iteration, which competes only with the worst vector.
- **Anytime and derivative-free.** The best vector in memory is always available, and only values of $f$ are used.
- **Few parameters, all from ES.** HMCR, PAR and bw are a recombination rate, a mutation rate and a mutation width.

## Variants and improvements

- **Improved HS.** Mahdavi, Fesanghary and Damangir (2007) let PAR grow and bw shrink during the run. In ES terms, this is a mutation schedule.
- **Global-best HS.** The pitch step copies a coordinate of the best vector, which adds a pull toward the best point.
- **Self-adaptive versions.** The parameters are adapted from the members of the memory, as in self-adaptive evolution strategies.
- **Discrete HS.** For integer or categorical variables, the pitch step moves to a neighboring value in a list.

## When to use it

If you need a method of this kind, you can use a standard evolution strategy, [differential evolution](/differential-evolution/) or [CMA-ES](/cma-es/), which have the same or more general operators, a body of theory and well-tested implementations. Weyland (2010) showed that HS adds no new search mechanism, and Sörensen (2015) used HS as a main example of a method whose metaphor hides its relation to known methods. Saka, Hasançebi and Geem (2016) replied in defense of HS. If you do use HS, report it as a $(\mu + 1)$-ES with the operators above, and compare it with other methods on your own problems with the same number of evaluations. This page reports no such comparison.

## Pitfalls

- **New names for known parts.** Calling recombination memory consideration and mutation pitch adjustment hides the link to the literature on evolution strategies, and with it the known results and advice.
- **Too little random selection.** With HMCR close to 1 and small bw, the memory can lose diversity in a coordinate, and the method can only move by steps of size bw.
- **The scale of bw.** A fixed bw that is large compared with the distances in the memory makes fine search impossible, and a small one makes large moves rare. Set it relative to the box, or shrink it during the run.
- **Ties.** A new vector equal in value to the worst does not enter. With plateaus, this can stop progress. Some versions accept ties.

## Implementations

## History

Geem, Kim and Loganathan introduced harmony search in 2001 with a metaphor of jazz musicians who improvise, and Lee and Geem gave a continuous version in 2005. The method spread fast in engineering applications. Weyland (2010) showed that it is a special case of evolution strategies, which go back to Rechenberg and Schwefel in the 1960s and 1970s, and criticized claims made for it. Sörensen (2015) used it as a main example in his critique of metaphor-based metaheuristics, and later papers, such as Aranha and others (2022), with Camacho Villalón, Dorigo and Stützle among the authors, asked that such methods be described in standard terms.

## References
