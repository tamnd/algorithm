---
tag: DVD07D
kind: algorithm
slug: artificial-bee-colony
name: Artificial bee colony algorithm
aliases:
- ABC
- artificial bee colony
area: optimization/metaheuristics
level: research
summary: A population method for continuous minimization. Each solution tries one-coordinate moves toward or away from another solution, good solutions get more tries, and stuck solutions are restarted.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {D: the number of variables, s: the number of food sources SN, T: the number of cycles MCN, c: the cost of one evaluation of f}
  time: {worst: O(T s (D + c + s))}
  space: {extra: O(s D)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 2005
  people: [Derviş Karaboğa]
  note: Karaboğa described the algorithm in a 2005 technical report of Erciyes University. Karaboğa and Baştürk published it in 2007, and Karaboğa and Akay gave a large comparison and a version with constraints in 2009 and 2011.
prereqs: [swarm-intelligence, roulette-wheel-selection]
see_also: [differential-evolution, particle-swarm-optimization, ant-colony-optimization, evolution-strategies, population-based-search, local-search, no-free-lunch-theorem, premature-convergence]
sources:
  - paper: Derviş Karaboğa, An idea based on honey bee swarm for numerical optimization, Technical Report TR06, Erciyes University, Engineering Faculty, Computer Engineering Department, 2005
    title: An idea based on honey bee swarm for numerical optimization
    locator: the whole report (the employed, onlooker and scout phases, the neighbor rule and the fitness transform)
  - paper: doi:10.1007/s10898-007-9149-x
    title: Derviş Karaboğa and Bahriye Baştürk, A powerful and efficient algorithm for numerical function optimization, artificial bee colony (ABC) algorithm, Journal of Global Optimization 39(3), 2007
    locator: pages 459 to 471 (the algorithm, the parameters SN, limit and MCN, and the neighbor rule v_ij = x_ij + φ(x_ij - x_kj))
  - paper: doi:10.1016/j.amc.2009.03.090
    title: Derviş Karaboğa and Bahriye Akay, A comparative study of artificial bee colony algorithm, Applied Mathematics and Computation 214(1), 2009
    locator: pages 108 to 132 (the pseudocode with the fitness 1/(1+f) and 1+|f|, the onlooker probabilities, and the limit SN times D)
  - paper: doi:10.1016/j.amc.2010.08.049
    title: Guopu Zhu and Sam Kwong, Gbest-guided artificial bee colony algorithm for numerical function optimization, Applied Mathematics and Computation 217(7), 2010
    locator: pages 3166 to 3173 (the neighbor rule with an extra term toward the best solution)
  - paper: doi:10.1023/A:1008202821328
    title: Rainer Storn and Kenneth Price, Differential evolution, a simple and efficient heuristic for global optimization over continuous spaces, Journal of Global Optimization 11(4), 1997
    locator: pages 341 to 359 (difference vectors, binomial crossover and greedy one-to-one selection, for the comparison with ABC)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of methods presented through a natural metaphor instead of through their search operators)
---

The artificial bee colony algorithm (ABC) is a population method for minimizing a function $f$ of $D$ real variables on a box. It keeps $SN$ points, called food sources. In each cycle, every point tries a move that changes one coordinate toward or away from another random point, and keeps it only if it is better. Then $SN$ more moves are tried from points chosen by a [roulette wheel](/roulette-wheel-selection/), so better points get more tries. A point that has failed more than $\text{limit}$ times in a row is replaced by a random point. The bee words of the original papers name these three phases: employed bees, onlooker bees and scouts. Read without the metaphor, ABC is a close relative of [differential evolution](/differential-evolution/) with one changed coordinate per move, plus fitness-proportional reuse of good points and restarts. No convergence or runtime result is proved on this page beyond the invariants below.

## In plain words

Keep a fixed number of candidate points. For each point, make a copy and change one of its numbers: move it toward or past the same number of another random point, by a random amount. If the copy is better, it takes the place of the point. If not, count one more failure for the point.

Next, do the same again as many times, but pick each point to work on at random, with better points more likely. At the end of the round, if some point has failed too many times in a row, throw it away and put a new random point in its place. Keep note of the best point ever seen. Repeat for a fixed number of rounds.

## The problem

The input is a function $f : \mathbb{R}^D \to \mathbb{R}$ that can be evaluated at any point, and bounds $\ell_j < u_j$ for each coordinate. The goal is a point of the box $\prod_j [\ell_j, u_j]$ with a small value of $f$. Nothing else is known about $f$: it is a black box, and the cost is counted in evaluations.

## The algorithm

The parameters are the number of sources $SN \ge 2$, the number of failed tries $\text{limit}$ after which a source is dropped, and the number of cycles $MCN$. Karaboğa and Akay set $\text{limit} = SN \cdot D$.

**Fitness.** For minimization, ABC uses
$$\text{fit}(x) = \begin{cases} 1/(1 + f(x)) & \text{if } f(x) \ge 0, \\ 1 + |f(x)| & \text{if } f(x) < 0. \end{cases}$$
This is positive and strictly decreasing in $f(x)$, so a larger fitness means a smaller value of $f$.

**Neighbor rule.** For source $i$, choose a source $k \ne i$ uniformly, a coordinate $j$ uniformly, and $\varphi$ uniform in $[-1, 1]$. The neighbor $v$ equals $x_i$ except in coordinate $j$:
$$v_j = x_{ij} + \varphi \, (x_{ij} - x_{kj}),$$
clipped to $[\ell_j, u_j]$. **Greedy selection** replaces $x_i$ by $v$ and sets $\text{trial}_i \leftarrow 0$ if $\text{fit}(v) > \text{fit}(x_i)$, and otherwise adds 1 to $\text{trial}_i$.

```pseudo id=main
ABC(f, ℓ, u, SN, limit, MCN)
L1  x_i ← a uniform random point of the box, trial_i ← 0, for i = 1..SN
L2  for cycle ← 1 to MCN do
L3      for i ← 1 to SN: try a neighbor of x_i with greedy selection   ▷ employed bees
L4      p_i ← fit(x_i) / Σ_s fit(x_s) for each i
L5      SN times: choose i with probability p_i; try a neighbor of x_i with greedy selection   ▷ onlooker bees
L6      update the best point found so far
L7      if max_i trial_i > limit then replace that x_i by a uniform random point, trial_i ← 0   ▷ scout
L8  return the best point found
```

Line L5 uses fixed probabilities from line L4 for the whole onlooker phase, as in the implementation of Karaboğa and Akay. Some versions recompute them after each move, and the original code chooses onlookers by a different rule. Line L7 makes at most one scout per cycle.

## Example

Let $f(x) = x_1^2 + x_2^2$ and take three sources: $x_1 = (1, 2)$ with $f = 5$, $x_2 = (-1, 0)$ with $f = 1$, and $x_3 = (3, 1)$ with $f = 10$.

**Employed bee of source 1.** Suppose it draws $k = 2$, $j = 1$ and $\varphi = -0.5$. Then $v_1 = 1 + (-0.5)(1 - (-1)) = 0$ and $v = (0, 2)$ with $f(v) = 4 < 5$. So $x_1 \leftarrow (0, 2)$ and $\text{trial}_1 = 0$. With $\varphi = 0.5$ instead, $v = (2, 2)$ with $f = 8$, so $x_1$ would stay and $\text{trial}_1$ would become 1. The sign of $\varphi$ decides whether the move goes toward $x_k$ or away from it, and its size is at most $|x_{ij} - x_{kj}|$.

**Onlooker probabilities.** Suppose that the other employed bees fail. The fitness values are $1/5 = 0.2$, $1/2 = 0.5$ and $1/11 \approx 0.0909$, with sum $0.7909$. So an onlooker chooses the sources with probabilities $0.2529$, $0.6322$ and $0.1149$. Source 2, the best, gets about 63 percent of the onlooker moves.

**Scout.** With $\text{limit} = SN \cdot D = 6$, a source is replaced only after more than 6 failed tries since its last success.

## Correctness

ABC cannot certify that its result is optimal. The proofs of these invariants are below.

- **Feasibility.** Every source and every tried point lies in the box: the start points and the scout points are drawn in the box, and the neighbor rule clips the changed coordinate.
- **Monotone sources.** Between two scout events of source $i$, $f(x_i)$ never increases, and it changes only by a strict decrease.
- **The best point.** After each cycle, the stored best point has the smallest value of $f$ among all points evaluated so far, so its value never increases.
- **Selection.** In line L5, source $i$ is chosen with probability $p_i$, and $p_i > p_s$ exactly when $f(x_i) < f(x_s)$, because fit is positive and strictly decreasing.
- **Trial counters.** $\text{trial}_i$ counts the failed tries of source $i$ since its last success or reset, so a source with $\text{trial}_i \le \text{limit}$ for all $i$ at the end of a cycle had no scout in that cycle.

The page proves no convergence result. The neighbor rule moves only within the range spanned by the current sources in one coordinate, and scouts restart only stuck sources.

## Complexity

Each neighbor costs $O(D)$ to copy plus one evaluation of $f$. A cycle makes $SN$ employed moves, $SN$ onlooker moves and at most one scout, so it makes at most $2 \cdot SN + 1$ evaluations. In the simple form, each roulette choice of line L5 and each choice of $k \ne i$ costs $O(SN)$, so a cycle costs $O(SN (D + c + SN))$ and $MCN$ cycles cost $O(MCN \cdot SN \cdot (D + c + SN))$. With a prefix-sum table and binary search, a roulette choice costs $O(\log SN)$, and $k \ne i$ can be drawn in $O(1)$ by drawing from $SN - 1$ values and skipping $i$. The sources take $O(SN \cdot D)$ space. In practice the evaluations of $f$ dominate.

## Properties

- **Derivative-free and anytime.** ABC uses only values of $f$, and the best point found so far is always available.
- **One coordinate per move.** Each move changes one coordinate. This suits functions that are close to separable, and makes progress slow on functions whose good directions mix many coordinates.
- **Not rotation invariant.** Because moves follow the coordinate axes, the behavior changes if the problem is rotated.
- **Relation to differential evolution.** DE with crossover rate $CR = 0$ changes exactly one coordinate, and greedy one-to-one replacement is the selection of DE. The ABC rule $v_j = x_{ij} + \varphi(x_{ij} - x_{kj})$ is such a move with the target as base vector and a random factor $\varphi \in [-1, 1]$ in place of a fixed $F$. ABC adds the roulette wheel of line L5 and the restarts of line L7.

## Variants and improvements

- **Gbest-guided ABC.** Zhu and Kwong (2010) add a term $\psi (g_j - x_{ij})$ toward the best point $g$, with $\psi$ uniform in $[0, 1.5]$.
- **Modified ABC.** Akay and Karaboğa (2012) change several coordinates per move, controlled by a modification rate, and scale the step.
- **Constrained ABC.** Karaboğa and Akay (2011) use Deb's rules for constraints in the greedy selection.
- **Discrete versions.** Binary and permutation versions replace the neighbor rule by bit flips or swaps.
- **Other selection.** Tournament or rank selection in place of the roulette wheel.

## When to use it

ABC is a simple derivative-free method with few parameters. Before you choose it, compare it with standard methods on your own problems with the same number of evaluations: [differential evolution](/differential-evolution/), [CMA-ES](/cma-es/) and, for smooth problems, quasi-Newton methods with numerical gradients or restarts. Published comparisons depend on the test functions, the budgets and the tuning, and the [no free lunch theorem](/no-free-lunch-theorem/) rules out a method that is best on all problems. This page makes no performance claim.

## Pitfalls

- **Fitness saturation.** In double precision, $1/(1 + f)$ equals 1.0 for $0 \le f < 1.1 \cdot 10^{-16}$, so greedy selection cannot tell such values apart and progress stops at about $10^{-16}$ on problems with optimum 0, as the test file shows. Compare values of $f$ directly in the greedy step, and use fit only for the roulette wheel.
- **Weak selection for large values.** For large $f$, $1/(1 + f)$ is close to $1/f$, so the probabilities depend on ratios of values. Values 1000 and 1001 get almost the same probability, though one is better. Shift $f$, or use rank-based probabilities.
- **The sign of the step.** $\varphi$ is in $[-1, 1]$, so the move can go away from $x_k$. Code that uses $[0, 1]$ only changes the method.
- **The limit.** A small limit restarts sources that are still improving slowly, and a very large limit makes scouts rare. $SN \cdot D$ is the common choice, but it is not a law.
- **The metaphor.** Words such as nectar, dance and scout do not add meaning to the method. Describe and compare ABC through its operators, as Sörensen (2015) asks for metaphor-based methods in general.

## Implementations

## History

Karaboğa proposed ABC in a 2005 technical report of Erciyes University, after earlier bee-inspired methods by several groups in the early 2000s. Karaboğa and Baştürk published it in the Journal of Global Optimization in 2007, and Karaboğa and Akay compared it with other methods on a large set of test functions in 2009 and extended it to constraints in 2011. Many variants followed, such as the gbest-guided ABC of Zhu and Kwong (2010). In 2015 Sörensen criticized the growth of methods named after natural metaphors, and later studies have analyzed several of them in terms of known operators.

## References
