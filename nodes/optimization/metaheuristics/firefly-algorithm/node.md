---
tag: BF1W32
kind: algorithm
slug: firefly-algorithm
name: Firefly algorithm
area: optimization/metaheuristics
level: research
summary: A population method in which each point moves toward every better point by a pull that decays with distance, plus uniform noise. It is a form of particle swarm optimization.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {D: the number of variables, n: the number of fireflies, T: the number of iterations, c: the cost of one evaluation of f}
  time: {worst: O(T n^2 (D + c))}
  space: {extra: O(n D)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 2008
  people: [Xin-She Yang]
  note: Yang described the firefly algorithm in his 2008 book with a metaphor of flashing fireflies. Camacho-Villalón, Dorigo and Stützle showed in 2020 and 2023 that it is a form of particle swarm optimization.
prereqs: [particle-swarm-optimization]
see_also: [bat-algorithm, cuckoo-search, harmony-search, swarm-intelligence, differential-evolution, simulated-annealing, multimodal-optimization, no-free-lunch-theorem]
sources:
  - book: isbn:978-1-905986-10-1
    title: Xin-She Yang, Nature-Inspired Metaheuristic Algorithms, Luniver Press, 2008
    locator: the chapter on the firefly algorithm (the attractiveness β0 exp(-γ r^2) and the move toward brighter fireflies)
  - paper: doi:10.1007/978-3-642-04944-6_14
    title: Xin-She Yang, Firefly algorithms for multimodal optimization, Stochastic Algorithms, Foundations and Applications (SAGA 2009), LNCS 5792, Springer, 2009
    locator: pages 169 to 178 (the update equation, the role of γ and the special cases γ = 0 and γ large)
  - paper: doi:10.1007/978-3-030-60376-2_10
    title: Christian Leonardo Camacho-Villalón, Marco Dorigo and Thomas Stützle, Grey wolf, firefly and bat algorithms, three widespread algorithms that do not contain any novelty, ANTS 2020, LNCS 12421, Springer, 2020
    locator: pages 121 to 133 (the firefly algorithm written as a particle swarm optimization variant)
  - paper: doi:10.1111/itor.13176
    title: Christian Leonardo Camacho-Villalón, Marco Dorigo and Thomas Stützle, Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms, six misleading optimization techniques inspired by bestial metaphors, International Transactions in Operational Research 30(6), 2023
    locator: pages 2945 to 2971 (the firefly section and the comparison of its terms with PSO)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of methods presented through a natural metaphor)
  - paper: doi:10.4018/jamc.2010040104
    title: Dennis Weyland, A rigorous analysis of the harmony search algorithm, how the research community can be misled by a novel methodology, International Journal of Applied Metaheuristic Computing 1(2), 2010
    locator: pages 50 to 60 (the first detailed case of a metaphor-based method that reduces to a known method)
  - paper: doi:10.1109/ICNN.1995.488968
    title: James Kennedy and Russell Eberhart, Particle swarm optimization, Proceedings of ICNN'95, International Conference on Neural Networks, IEEE, 1995
    locator: pages 1942 to 1948 (the velocity and position updates)
---

The firefly algorithm (FA) is a population method for minimizing a function of $D$ real variables. It keeps $n$ points, called fireflies. In each iteration, every point looks at every other point, and for each one that has a better value it moves toward it by a fraction $\beta_0 e^{-\gamma r^2}$ of the distance $r$, plus a small uniform random step. Moves are not greedy: a point takes the new position even when it is worse. Yang presented FA in 2008 with a metaphor of fireflies attracted by brighter ones. It belongs to the family of metaphor-based methods that Sörensen (2015) criticized, and Camacho-Villalón, Dorigo and Stützle (2020, 2023) showed that it is a variant of [particle swarm optimization](/particle-swarm-optimization/). This page describes FA in those terms and makes no claim that it performs better than other methods.

## In plain words

Keep a group of candidate points. In each round, take each point in turn and compare it with every other point. Each time another point is better, move the first point part of the way toward it and add a small random shake. The pull is strong when the two points are close and weak when they are far apart. The best point has nothing better to move toward, so it stays where it is. Make the shakes smaller after each round. Return the best point seen.

## The problem

The input is a function $f : \mathbb{R}^D \to \mathbb{R}$ that can be evaluated at any point, and bounds $\ell_k < u_k$. The goal is a point of the box $B = \prod_k [\ell_k, u_k]$ with a small value of $f$. The brightness of a firefly is a decreasing function of $f$, so "brighter" means "smaller value" here.

## The algorithm

The parameters are the number of fireflies $n \ge 2$, the maximum attractiveness $\beta_0$ (often 1), the absorption coefficient $\gamma \ge 0$, the noise scale $\alpha$, its decay factor $\delta \le 1$ and the number of iterations $T$. The vector $w$ holds the widths $u_k - \ell_k$ of the box, and $\odot$ is the product by coordinates.

```pseudo id=main
FA(f, ℓ, u, n, β0, γ, α, δ, T)
L1  x_i ← a uniform random point of the box, for i = 1..n; g ← the best x_i
L2  for t ← 1 to T do
L3      for i ← 1 to n do
L4          for j ← 1 to n do
L5              if f(x_j) < f(x_i) then                              ▷ the current values
L6                  y ← x_i + β0 e^(−γ‖x_i − x_j‖²) (x_j − x_i) + α (u − ½) ⊙ w, clipped   ▷ u ~ U[0, 1]^D
L7                  x_i ← y; if f(x_i) < f(g) then g ← x_i          ▷ not greedy
L8      α ← δ α
L9  return g
```

**In PSO terms.** Line L6 is the position update $x_i \leftarrow x_i + v$ of particle swarm optimization with the velocity
$$v = \beta (x_j - x_i) + \alpha (u - \tfrac12) \odot w, \qquad \beta = \beta_0 e^{-\gamma \lVert x_i - x_j \rVert^2}.$$

- The inertia weight is 0, so no velocity is kept between moves.
- There is no personal-best term. The attractor is a better point $x_j$ of the current population, and a point is pulled in turn by every better point, as in a fully informed neighborhood that is applied one neighbor at a time.
- The social coefficient is $\beta$, which is the same in all coordinates and depends on the distance. In standard PSO the coefficient is $c_2 r_2$ with a fresh random $r_2$.
- The uniform perturbation $\alpha (u - \frac12) \odot w$ is added to the move. Its size shrinks by the factor $\delta$ per iteration, like the decreasing inertia or step size of many PSO and ES variants.

Two limits make the role of $\gamma$ clear. If $\gamma = 0$, the pull is $\beta_0$ at every distance, and with $\alpha = 0$ and $\beta_0 = 1$ every point jumps onto a better point. Then all points sit on the best start point after one iteration, as the proof below shows. If $\gamma$ is very large compared with $1/r^2$, the pull is almost 0 and every point makes a random walk that is not greedy. The useful range of $\gamma$ therefore depends on the distances between the points, so on the size of the box.

## Example

Let $f(x) = x_1^2 + x_2^2$ on $[-5, 5]^2$, so $w = (10, 10)$. Let $\beta_0 = 1$, $\gamma = 0.1$ and $\alpha = 0.2$. The fireflies are $x_1 = (1, 2)$ with $f = 5$, $x_2 = (-1, 0)$ with $f = 1$, and $x_3 = (3, 1)$ with $f = 10$, so $g = x_2$.

**The turn of firefly 1.** Only $x_2$ is better. The distance is $r^2 = 2^2 + 2^2 = 8$, so $\beta = e^{-0.8} \approx 0.4493$. Suppose $u = (0.5, 0.5)$, so the noise is 0. Then $y = (1, 2) + 0.4493 \cdot (-2, -2) \approx (0.1013, 1.1013)$ with $f(y) \approx 1.2232$.

**The turn of firefly 2.** It has the smallest value, so no firefly is better and it does not move.

**The turn of firefly 3.** Firefly 1 is now at $(0.1013, 1.1013)$ with value $1.2232 < 10$. The distance is $r^2 \approx 8.4125$, so $\beta \approx 0.4312$. Suppose $u = (0.9, 0.1)$, so the noise is $0.2 \cdot (0.4, -0.4) \cdot 10 = (0.8, -0.8)$. Then $x_3 \approx (2.5502, 0.2437)$ with $f \approx 6.5628$. Firefly 2 is also better. The distance is $r^2 \approx 12.6632$, so $\beta \approx 0.2819$. Suppose $u = (0.1, 0.9)$, so the noise is $(-0.8, 0.8)$. Then $x_3 \approx (0.7495, 0.9750)$ with $f \approx 1.5124$.

The iteration made 3 moves and 3 evaluations, and $g$ is still $(-1, 0)$. The test file checks these numbers. Firefly 3 moved twice because it was compared with two better points. The order of the loops matters: firefly 3 used the new position of firefly 1.

## Correctness

FA cannot certify that its result is optimal. The proofs of these invariants are below.

- **Feasibility.** All points lie in the box, since the start points are drawn in the box and every proposal is clipped.
- **Moves go toward better points.** A point moves only toward a point with a strictly smaller current value.
- **The best current value never increases.** A move never changes a point with the smallest current value, so the minimum over the population never rises, although the point that moves can get worse.
- **The best point.** After each move, $f(g)$ is the smallest value among all points evaluated so far.
- **Collapse without noise.** With $\alpha = 0$, $\gamma = 0$ and $\beta_0 = 1$, all points equal the best start point after one iteration.

The page proves no convergence result. The proof file shows that with $\beta_0 \le 1$ and $\delta < 1$ the total noise is bounded, so if this bound is small compared with the box, the points cannot reach a minimizer far from all start points.

## Complexity

Each iteration tests $n(n - 1)$ ordered pairs, and each move costs $O(D)$ work and one evaluation of $f$. So $T$ iterations cost $O(T n^2 (D + c))$ time, and the number of evaluations is $n$ plus the number of moves, at most $n + T n (n - 1)$. The number of moves depends on the values, so a comparison with another method at equal cost must count evaluations, not iterations. The points take $O(n D)$ space.

## Properties

- **Anytime and derivative-free.** $g$ is always available, and only values of $f$ are used, through comparisons.
- **Invariant to monotone changes of $f$.** Lines L5 and L7 only compare values, so replacing $f$ by $h \circ f$ with $h$ strictly increasing gives the same run.
- **Not greedy.** A move is accepted even when it makes the point worse. Only the best point and $g$ are protected.
- **Order dependent.** Line L5 uses the current values, so a point can move toward a point that has already moved in the same iteration.
- **Scale dependent.** The pull depends on $\gamma r^2$, so scaling the box changes the run unless $\gamma$ is scaled by the inverse square of the same factor.

## Variants and improvements

- **The reference code.** A widely copied MATLAB code by Yang compares the values from the start of the iteration, moves toward stored copies of the points, and uses $\beta = (\beta_0 - \beta_{\min}) e^{-\gamma r^2} + \beta_{\min}$ with a floor $\beta_{\min}$. These are different algorithms from the one above, and results with one do not transfer to the other.
- **A random move for the best point.** Some versions let the best firefly make a random move, so that it is not fixed.
- **Other attractiveness laws.** Yang also mentions $\beta_0 / (1 + \gamma r^2)$, which decays more slowly.
- **Lévy-flight FA.** Yang (2010) replaced the uniform noise by heavy-tailed steps, as in [cuckoo search](/cuckoo-search/).
- **Discrete FA.** The pull is replaced by a number of swaps or bit changes toward the better point.

In PSO terms, each of these variants changes the attractor, the coefficient, or the perturbation.

## When to use it

If you need a method of this kind, standard particle swarm optimization, [differential evolution](/differential-evolution/) and [CMA-ES](/cma-es/) have the same or more general operators, a body of theory and well-tested implementations. If you use FA, describe it by its operators as above, state the rule for line L5 and the value of $\gamma$ relative to the size of the box, and compare it with standard methods on your own problems with the same number of evaluations. This page reports no comparison between methods.

## Pitfalls

- **The value of $\gamma$.** We ran the Python code of this page on the 5-dimensional sphere in $[-5.12, 5.12]^5$ with $n = 15$, $\beta_0 = 1$, $\alpha = 0.2$, $\delta = 0.97$ and 300 iterations. Seeds 0, 1 and 2 gave these best values. The test file checks the run with $\gamma = 0.1$ and seed 0.

  | $\gamma$ | seed 0 | seed 1 | seed 2 |
  | --- | --- | --- | --- |
  | 0.1 | $2.3 \cdot 10^{-9}$ | $2.1 \cdot 10^{-9}$ | $2.8 \cdot 10^{-9}$ |
  | 1 | 4.41 | $6.0 \cdot 10^{-9}$ | 5.16 |

  With $\gamma = 1$, the typical squared distance between random points is near 87, so $e^{-\gamma r^2}$ is almost 0, and in two runs the best value did not change from the start. These are six runs of one implementation on one function. They show the sensitivity to $\gamma$, not the general behavior of FA.
- **Cost per iteration.** An iteration can make up to $n(n - 1)$ evaluations, not $n$. Plots against iterations hide this.
- **Description and code differ.** Check whether an implementation uses the current values or the values from the start of the iteration, whether it has $\beta_{\min}$, and whether the noise is scaled by the box.
- **The metaphor.** Light, brightness and absorption name a distance-weighted pull toward better points. Sörensen (2015) asks that methods be described by their operators.

## Implementations

## History

Yang described the firefly algorithm in his book Nature-Inspired Metaheuristic Algorithms (2008) and in a 2009 paper on multimodal optimization, with a metaphor of fireflies that attract each other by flashing light whose intensity falls with distance. Many variants and applications followed. Particle swarm optimization (Kennedy and Eberhart, 1995) already moved points toward better points with random coefficients. Weyland (2010) showed for harmony search that a method named after a metaphor can be a special case of a known method, and Sörensen (2015) criticized the general practice. Camacho-Villalón, Dorigo and Stützle analyzed FA at ANTS 2020 and in a longer 2023 paper, and concluded that it is a PSO variant with no new idea for optimization.

## References
