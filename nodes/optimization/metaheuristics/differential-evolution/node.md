---
tag: R0J5VG
kind: algorithm
slug: differential-evolution
name: Differential evolution
aliases:
- DE
- DE/rand/1/bin
area: optimization/metaheuristics
level: advanced
summary: Population method on real vectors that mutates by adding a scaled difference of two members to a third, crosses over with the target, and keeps the better of the two.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {g: the number of generations, p: the population size, n: the dimension, c: the cost of one value of the objective}
  time: {worst: O(g p (n + c))}
  space: {extra: O(p n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true, comparison-based: true}
history:
  year: 1995
  people: [Rainer Storn, Kenneth Price]
  note: Storn and Price described differential evolution in a 1995 technical report and published it in the Journal of Global Optimization in 1997.
prereqs: [black-box-optimization, mutation, crossover]
see_also: [evolution-strategies, cma-es, genetic-algorithm, particle-swarm-optimization, premature-convergence, multimodal-optimization, derivative-free-optimization, evolutionary-computation]
sources:
  - paper: doi:10.1023/A:1008202821328
    title: Rainer Storn and Kenneth Price, Differential evolution, a simple and efficient heuristic for global optimization over continuous spaces, Journal of Global Optimization 11(4), 1997
    locator: pages 341 to 359 (the scheme DE1, mutation with a scaled difference, crossover and selection)
  - book: doi:10.1007/3-540-31306-0
    title: Kenneth V. Price, Rainer M. Storn and Jouni A. Lampinen, Differential Evolution, a Practical Approach to Global Optimization, Springer, 2005
    locator: Chapter 2 (the classic algorithm, the control parameters and the handling of bounds) and the discussion of rotational invariance
  - paper: doi:10.1109/TEVC.2010.2059031
    title: Swagatam Das and Ponnuthurai N. Suganthan, Differential evolution, a survey of the state-of-the-art, IEEE Transactions on Evolutionary Computation 15(1), 2011
    locator: pages 4 to 31 (the strategies, parameter adaptation and the theory)
  - paper: "Daniela Zaharie, Critical values for the control parameters of differential evolution algorithms, Proceedings of MENDEL 2002, 8th International Conference on Soft Computing, 2002"
    title: Daniela Zaharie, Critical values for the control parameters of differential evolution algorithms
    locator: pages 62 to 67 (the expected population variance after mutation and crossover)
  - paper: "Jouni Lampinen and Ivan Zelinka, On stagnation of the differential evolution algorithm, Proceedings of MENDEL 2000, 6th International Conference on Soft Computing, 2000"
    title: Jouni Lampinen and Ivan Zelinka, On stagnation of the differential evolution algorithm
    locator: pages 76 to 83
---

Differential evolution (DE) is a population method for minimizing a function on $\mathbb{R}^n$, often over a box. To change a member, it takes a third member and adds to it a scaled difference of two other members, mixes the result with the member by crossover, and keeps the better of the two. The differences between members set the size and the direction of the steps, so the steps become smaller as the population contracts, without a step-size rule. Storn and Price proposed it in 1995. It has three parameters, the population size $p$, the scale factor $F$ and the crossover rate $CR$, and it is simple to implement. It has no general guarantee of convergence to the global minimum, or even to a local one: the population can stagnate, and with a small $F$ it can lose its spread before it reaches a minimum.

## In plain words

Keep a group of candidate points. To try to improve one of them, pick three others at random. Take the step that leads from the second to the third, make it a bit shorter, and add it to the first. That gives a new point.

Mix that new point with the one you want to improve: take some coordinates from the new point and keep the others. If the mixed point is at least as good, it takes the place of the old one. Otherwise nothing changes.

While the group is spread out, the steps are long. When the group gathers in a valley, the steps get short. The shape of the group also sets the direction of the steps, so the search follows the shape of the valley.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$ that we can only evaluate, an optional box $[\ell, u] = \prod_j [\ell_j, u_j]$, a start population $x_1, \dots, x_p$ with $p \ge 4$, usually uniform in the box, and a number of generations. The goal is a point with a small value of $f$, the [global optimization](/global-optimization/) problem in the [black-box](/black-box-optimization/) setting.

## The algorithm

The classic strategy DE/rand/1/bin: the base vector is random, one difference is used, and the crossover is binomial.

```pseudo id=main
DIFFERENTIAL-EVOLUTION(f, x₁..x_p, F, CR, G, [ℓ, u])
L1  evaluate f(x_i) for all i
L2  for generation ← 1 to G do
L3      for i ← 1 to p do
L4          pick distinct r₁, r₂, r₃ ∈ {1..p} ∖ {i} at random
L5          v ← x_{r₁} + F · (x_{r₂} − x_{r₃})
L6          for each j with v_j outside [ℓ_j, u_j]: v_j ← (bound + x_{r₁,j}) / 2
L7          j_rand ← random index; t_j ← v_j if j = j_rand or rand() < CR, else x_{i,j}
L8          if f(t) ≤ f(x_i) then x_i' ← t else x_i' ← x_i
L9      x ← x'
L10 return the best x_i
```

Line L5 is the mutation, and the result $v$ is the *mutant*. Line L6 repairs a coordinate that leaves the box by moving it halfway from the base vector to the violated bound. Line L7 is the binomial crossover: each coordinate comes from the mutant with probability $CR$, and the coordinate $j_{\text{rand}}$ always does, so the trial $t$ differs from $x_i$ in at least one coordinate when $v \ne x_i$. Line L8 is the selection, one trial against its own target. The new population replaces the old one after the generation. Common values are $F = 0.5$ and $CR = 0.9$, with $p = 10n$ in the original paper, and $CR = 0.1$ for separable functions.

## Example

**One trial by hand.** Minimize the sphere $f(x) = x_1^2 + x_2^2$ in the box $[-2, 2]^2$, with $F = 0.5$, $CR = 0.5$ and the population $x_1 = (2, 1)$, $x_2 = (-1, 2)$, $x_3 = (0, -2)$, $x_4 = (1, 1)$. For the target $x_1$, with $f(x_1) = 5$, say $r_1 = 3$, $r_2 = 2$, $r_3 = 4$. Then
$$v = (0, -2) + 0.5\,\bigl((-1, 2) - (1, 1)\bigr) = (-1, -1.5),$$
which is in the box. With $j_{\text{rand}} = 1$ and a random number $0.7 > CR$ for coordinate 2, the trial is $t = (-1, 1)$, with $f(t) = 2 \le 5$, so $t$ replaces $x_1$. For the target $x_2$, say $r_1 = 1$, $r_2 = 4$, $r_3 = 3$: then $v = (2, 1) + 0.5\,(1, 3) = (2.5, 2.5)$, which leaves the box in both coordinates. Line L6 gives $v_1 = (2 + 2)/2 = 2$ and $v_2 = (2 + 1)/2 = 1.5$, so $v = (2, 1.5)$.

**Measured runs.** All runs use the box repair above, $F = 0.5$ and a uniform start population in the box. A run counts as a success when the best value is below the target within 600 generations.

| function | $n$ | box | $p$ | $CR$ | target | successes | generations to the target |
|---|---|---|---|---|---|---|---|
| sphere | 10 | $[-5, 5]^n$ | 50 | 0.9 | $10^{-10}$ | 10 of 10 (seeds 0 to 9) | 250 to 270 |
| Rastrigin | 5 | $[-5.12, 5.12]^n$ | 50 | 0.1 | $10^{-8}$ | 20 of 20 (seeds 0 to 19) | 158 to 174 |
| Rastrigin | 5 | $[-5.12, 5.12]^n$ | 50 | 0.9 | $10^{-8}$ | 20 of 20 (seeds 0 to 19) | 329 to 506 |

Rastrigin's function $10n + \sum_i (x_i^2 - 10 \cos 2\pi x_i)$ has $11^5$ local minima in this box. On this separable function, a small $CR$, which changes few coordinates at a time, did better.

**Rotation matters when $CR < 1$.** Take the ellipsoid $\sum_{i=1}^{10} 10^{4(i-1)/9} x_i^2$ with condition number $10^4$, and the same function after a random rotation $Q$ (from seed 99). With $p = 50$, $F = 0.5$, the box $[-5, 5]^{10}$, the target $10^{-8}$ and a budget of 2000 generations, over seeds 0 to 4:

| $CR$ | axis-parallel | rotated |
|---|---|---|
| 0.1 | 275 to 285 generations, 5 of 5 | 0 of 5 |
| 0.9 | 253 to 268 generations, 5 of 5 | 523, 527, 535 and 1097 generations, 4 of 5 |

The crossover works coordinate by coordinate, so it depends on the axes. With $CR = 1$ the trial is the mutant, and the method is invariant under linear maps (Claim 4 below).

## Correctness

The proofs are below.

1. **Bounds.** If the start population is in the box, every mutant after line L6, every trial and every member of every population is in the box.
2. **Elitism per member.** $f(x_i)$ never increases for each $i$, and the returned point is the best point evaluated.
3. **Invariance under increasing transformations of $f$.** With the same random numbers, the run on $g \circ f$, with $g$ strictly increasing, is the same as the run on $f$.
4. **Invariance under maps of the space.** Without bounds and with $CR = 1$, the run on $f(A^{-1}(x - b))$ from the population $A x_i + b$ is the image under $x \mapsto A x + b$ of the run on $f$, for every invertible matrix $A$. For any $CR$ and with bounds, the same holds when $A$ is diagonal with positive entries, with the box mapped too. For $CR < 1$ it fails for rotations in general, as the measurement above shows.
5. **Stagnation.** Given the population, each target has finitely many possible trials. If none of them is accepted, for every target, the population never changes again.

There is no general convergence result. Claim 5 says that a run can stop at a population that contains no minimum, and Lampinen and Zelinka report such stagnation in practice. Zaharie computed how mutation and crossover change the spread: in a model where $r_1, r_2, r_3$ are distinct indices drawn from the whole population and each coordinate is taken from the mutant with probability $CR$, the expected population variance of a coordinate after one generation without selection is $\bigl(2F^2 CR - 2CR/p + CR^2/p + 1\bigr)$ times the variance before. A Monte Carlo check with $p = 10$, $F = 0.5$, $CR = 0.9$ (200000 trials, seed 1) gave the factor $1.3517$, against $1.351$ from the formula. The variance shrinks without selection when $F < \sqrt{(1 - CR/2)/p}$, which is $0.235$ for these $p$ and $CR$. Below that value the population can collapse before it reaches a minimum, a form of [premature convergence](/premature-convergence/).

## Complexity

One trial costs $O(n)$ for the mutation, the repair and the crossover, and one value of $f$. A generation makes $p$ trials, so $g$ generations cost $O(g p (n + c))$, where $c$ is the cost of $f$. The space is $O(p n)$ for two populations. There is no bound on the number of generations that a given accuracy needs.

## Properties

- **Self-scaling steps.** The step sizes come from differences in the population, so they shrink as the population contracts, and they follow its shape.
- **Comparison-based** (Claim 3).
- **Elitist per member** (Claim 2). Each slot keeps its best point.
- **Depends on the axes when $CR < 1$.** Binomial crossover changes some coordinates and not others, which helps on separable functions and hurts on rotated ones.
- **Parallel.** The $p$ trials of a generation are independent and can be evaluated at the same time.
- **Few parameters.** $p$, $F$ and $CR$, with defaults that work on many problems.

## Variants and improvements

- **Other strategies.** DE/best/1 uses the best member as the base vector, which converges faster and loses diversity sooner. DE/rand/2 adds two differences. DE/current-to-best/1 moves the target toward the best member and adds a difference.
- **Exponential crossover.** Copy a run of consecutive coordinates from the mutant, of random length, instead of independent coordinates.
- **Adaptive parameters.** jDE (Brest et al., 2006) gives each member its own $F$ and $CR$ and mutates them. JADE (Zhang and Sanderson, 2009) and SHADE learn the distributions of $F$ and $CR$ from successful trials and use an archive of replaced points.
- **Asynchronous update.** Replace $x_i$ at once in line L8 instead of at the end of the generation. Many implementations do this, so that a good trial can be used as a parent at once.
- **Constraints.** Penalty functions, or the rules of Deb that prefer feasible points.
- **Related methods.** [Particle swarm optimization](/particle-swarm-optimization/) also uses positions of other members to form steps. [CMA-ES](/cma-es/) learns a covariance instead of using the population differences directly.

## When to use it

Use DE for continuous problems of small to moderate dimension where the function is cheap enough for thousands of evaluations, gradients are not available, and there may be many local minima. It is a good first method for box-constrained problems, since it is easy to code and robust to its parameters. On rotated, ill-conditioned problems, use $CR$ close to 1 or a method that learns a covariance, such as [CMA-ES](/cma-es/). On smooth problems with gradients, a gradient method is faster.

## Pitfalls

- **Too small an $F$.** The population collapses, as Zaharie's formula shows. Keep $F$ above $\sqrt{(1 - CR/2)/p}$, and in practice at least about 0.4.
- **Too small a population.** With $p$ much smaller than $n$, the differences span only a subspace of dimension at most $p - 1$, and coordinates outside it change only through the crossover.
- **Clipping at the bounds.** Setting a coordinate that leaves the box equal to the bound piles points on the boundary. Use a repair like the one in line L6, or sample again.
- **$CR$ and separability.** A small $CR$ is good when the variables are independent and bad when they interact, as the rotated ellipsoid shows.
- **Forgetting $j_{\text{rand}}$.** Without it, with a small $CR$, many trials equal their target and waste evaluations.
- **Index rules.** $r_1, r_2, r_3$ must be distinct and differ from $i$. With $p < 4$ this is impossible.

## Implementations

## History

Rainer Storn and Kenneth Price developed differential evolution in 1994 and 1995 while working on the Chebyshev polynomial fitting problem, published a technical report of the International Computer Science Institute in Berkeley in 1995 and the journal paper in 1997. DE took part in the First International Contest on Evolutionary Optimization in 1996. Price, Storn and Lampinen wrote the first book on it in 2005. Zaharie analyzed the population variance in 2002, and many adaptive variants followed, such as jDE, JADE and SHADE.

## References
