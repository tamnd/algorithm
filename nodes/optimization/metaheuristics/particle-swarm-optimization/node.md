---
tag: F6H8KV
kind: algorithm
slug: particle-swarm-optimization
name: Particle swarm optimization
aliases:
- PSO
- particle swarm optimizer
- global-best PSO
area: optimization/metaheuristics
level: advanced
summary: Particles move through the space with a velocity pulled toward their own best point and the swarm's best point. With a stagnant attractor the mean converges iff |w| < 1 and 0 < c1 + c2 < 4(1 + w).
solves: [global-optimization]
model: real-ram
complexity:
  vars: {N: the number of particles, n: the dimension, T: the number of iterations, c: the cost of one evaluation}
  time: {worst: O(T N (n + c))}
  space: {extra: O(N n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 1995
  people: [James Kennedy, Russell C. Eberhart]
  note: Kennedy and Eberhart introduced the particle swarm in 1995 from a model of social behavior. Shi and Eberhart added the inertia weight in 1998, and Clerc and Kennedy gave the constriction analysis in 2002.
prereqs: [swarm-intelligence]
see_also: [differential-evolution, evolution-strategies, cma-es, firefly-algorithm, bat-algorithm, premature-convergence, derivative-free-optimization, gradient-descent]
sources:
  - paper: doi:10.1109/ICNN.1995.488968
    title: James Kennedy and Russell Eberhart, Particle swarm optimization, Proceedings of the IEEE International Conference on Neural Networks, 1995
    locator: pages 1942 to 1948 (the original velocity update with personal and global best)
  - paper: Yuhui Shi and Russell Eberhart, A modified particle swarm optimizer, Proceedings of the IEEE International Conference on Evolutionary Computation, 1998
    title: A modified particle swarm optimizer
    locator: pages 69 to 73 (the inertia weight)
  - paper: doi:10.1109/4235.985692
    title: Maurice Clerc and James Kennedy, The particle swarm, explosion, stability, and convergence in a multidimensional complex space, IEEE Transactions on Evolutionary Computation 6(1), 2002
    locator: pages 58 to 73 (the deterministic one-particle model and the constriction coefficient)
  - paper: doi:10.1109/TEVC.2008.2011744
    title: Riccardo Poli, Mean and variance of the sampling distribution of particle swarm optimizers during stagnation, IEEE Transactions on Evolutionary Computation 13(4), 2009
    locator: pages 712 to 721 (the first and second moments under stagnation and the region of order-2 stability)
  - paper: doi:10.1007/s11721-007-0002-0
    title: Riccardo Poli, James Kennedy and Tim Blackwell, Particle swarm optimization, an overview, Swarm Intelligence 1(1), 2007
    locator: pages 33 to 57 (the main variants, topologies and the theory up to 2007)
  - book: isbn:9781558605954
    title: James Kennedy, Russell C. Eberhart and Yuhui Shi, Swarm Intelligence, Morgan Kaufmann, 2001
    locator: Chapter 7, The particle swarm
  - paper: Frans van den Bergh and Andries P. Engelbrecht, A convergence proof for the particle swarm optimiser, Fundamenta Informaticae 105(4), 2010
    title: A convergence proof for the particle swarm optimiser
    locator: pages 341 to 374 (stagnation of the standard form and the guaranteed convergence variant)
  - paper: James Kennedy, Bare bones particle swarms, Proceedings of the IEEE Swarm Intelligence Symposium, 2003
    title: Bare bones particle swarms
    locator: pages 80 to 87
---

Particle swarm optimization (PSO) minimizes a function $f : \mathbb{R}^n \to \mathbb{R}$ with a set of particles, each with a position, a velocity and the best point it has visited. In each step a particle's velocity keeps a part $w$ of its old value and is pulled at random toward its own best point and toward the best point of the swarm, and the particle moves by its velocity. Kennedy and Eberhart introduced it in 1995 as a model of social behavior, and it is the second main method of [swarm intelligence](/swarm-intelligence/) after [ant colony optimization](/ant-colony-optimization/). Its proved results are about stability, not optimization: when the best points stop changing, the mean position of a particle converges if and only if $|w| < 1$ and $0 < c_1 + c_2 < 4(1 + w)$, and its variance converges in a smaller region given by Poli (2009).

## In plain words

Many points fly through the search space. Each point remembers the best place it has been, and all points know the best place that any of them has found. At each step, a point keeps part of its old speed, turns a little toward its own best place and a little toward the group's best place, with random weights, and moves.

When a point finds a better place, it updates its memory, and if the place is the best of the group, all points start to turn toward it. Over time the points gather around good places and search them more closely. The weights must be in a safe range. If they are too large, the points swing farther and farther out and never settle.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$, given as a black box, and a box $[\ell, u] \subset \mathbb{R}^n$ for the start positions. The goal is a point with a small value of $f$, ideally a global minimum (see [global optimization](/global-optimization/) and [derivative-free optimization](/derivative-free-optimization/)). The parameters are the number of particles $N$, the inertia weight $w$, the acceleration coefficients $c_1$ and $c_2$, and the number of iterations $T$.

## The algorithm

Each particle $i$ has a position $x_i$, a velocity $v_i$ and a personal best $p_i$, the best point it has visited. The swarm has a global best $g$. The product $r \odot y$ is taken coordinate by coordinate.

```pseudo id=main
PSO(f, ℓ, u, N, w, c_1, c_2, T)
L1  for i ← 1 to N: x_i ← uniform point of [ℓ, u], v_i ← 0, p_i ← x_i
L2  g ← the p_i with the smallest f
L3  for t ← 1 to T do
L4      for i ← 1 to N do
L5          draw r_1, r_2 with independent coordinates uniform in [0, 1)
L6          v_i ← w v_i + c_1 r_1 ⊙ (p_i − x_i) + c_2 r_2 ⊙ (g − x_i)
L7          x_i ← x_i + v_i
L8          if f(x_i) < f(p_i) then p_i ← x_i
L9              if f(x_i) < f(g) then g ← x_i
L10 return g
```

Line L6 has three terms: inertia, the pull toward the personal best (the cognitive term) and the pull toward the global best (the social term). Line L9 updates $g$ at once, so later particles of the same iteration use the new $g$. This is the asynchronous form. The synchronous form updates $g$ after all particles have moved. The positions are not clipped to the box.

A common setting is the constriction of Clerc and Kennedy: $w = \chi \approx 0.7298$ and $c_1 = c_2 = 2.05 \chi \approx 1.4962$, with $\chi = 2/|2 - \varphi - \sqrt{\varphi^2 - 4\varphi}|$ for $\varphi = 4.1$.

## Example

Minimize $f(x) = x^2$ in one dimension with two particles, $w = 0.5$ and $c_1 = c_2 = 1.5$. Start at $x_1 = 2$ and $x_2 = -1$ with zero velocities. Then $p_1 = 2$, $p_2 = -1$ and $g = -1$, with $f(g) = 1$.

Particle 1 draws $r_1 = 0.5$ and $r_2 = 0.4$. Its velocity is $0.5 \cdot 0 + 1.5 \cdot 0.5 \cdot (2 - 2) + 1.5 \cdot 0.4 \cdot (-1 - 2) = -1.8$, and it moves to $x_1 = 0.2$ with $f = 0.04$. This is better than $f(p_1) = 4$ and than $f(g) = 1$, so $p_1 = g = 0.2$.

Particle 2 draws $r_1 = 0.3$ and $r_2 = 0.6$. Its personal term is 0, because $x_2 = p_2$. Its velocity is $1.5 \cdot 0.6 \cdot (0.2 - (-1)) = 1.08$, so it moves to $x_2 = 0.08$ with $f = 0.0064$, and $p_2 = g = 0.08$. Particle 2 used the global best that particle 1 had just found.

After one iteration, $f(g)$ fell from 1 to 0.0064. Both particles now carry velocities, $-1.8$ and $1.08$, so in the next iteration the inertia term moves them past the attractors before the pulls turn them back.

## Correctness

PSO gives no certificate of optimality, and the standard form does not even guarantee convergence to a local minimum. Its correctness consists of invariants and a stability theorem. The full proofs are below.

- **Invariants.** After each pass of lines L5 to L9, $p_i$ is a point of smallest $f$ among the points that particle $i$ has visited, and $g$ is a point of smallest $f$ among all evaluated points. So $f(g)$ never increases, and the returned $g$ is the best point found.
- **First-order stability.** Suppose that $p_i$ and $g$ stop changing, which is called stagnation. Then each coordinate of $\mathrm{E}[x_i(t)]$ follows the recurrence $m_{t+1} = (1 + w - \bar c) m_t - w m_{t-1} + \text{const}$ with $\bar c = (c_1 + c_2)/2$. The mean converges for every start, to $(c_1 p_i + c_2 g)/(c_1 + c_2)$, if and only if $|w| < 1$ and $0 < c_1 + c_2 < 4(1 + w)$. With fixed random factors replaced by a fixed total $\varphi$, the deterministic particle of Clerc and Kennedy converges if and only if $|w| < 1$ and $0 < \varphi < 2(1 + w)$.
- **Second-order stability.** Poli (2009) computed the second moments under stagnation. For $c_1 = c_2$ the variance converges if and only if $|w| < 1$ and $0 < c_1 + c_2 < 24(1 - w^2)/(7 - 5w)$, a strict subset of the first-order region. For $w = 0.7298$ this limit is about 3.347, against 6.919 for the first order, and the constriction setting has $c_1 + c_2 \approx 2.992$, inside both.

Stability says that the particles settle. It does not say that they settle at a minimum. If all particles reach $p_i = g = x_i$ with zero velocity, the swarm stops at $g$ even when $g$ is not a local minimum, because line L6 then gives $v_i = 0$. Van den Bergh and Engelbrecht (2010) analysed this stagnation and proposed a variant that keeps a minimum search radius around $g$.

## Complexity

Each iteration moves $N$ particles. A move draws $2n$ random numbers and does $O(n)$ arithmetic in lines L5 to L7, and line L8 evaluates $f$ once. So one iteration costs $O(N(n + c))$ and $T$ iterations cost $O(T N (n + c))$, with $N + N T$ evaluations in all. The positions, velocities and personal bests take $O(N n)$ space.

No bound on the number of iterations to reach a given accuracy holds for general $f$. The stability regions above say when the swarm settles, not how fast it finds a good point.

## Properties

- **Randomized and anytime.** The global best $g$ is a valid answer at any time, and $f(g)$ never increases.
- **Black box and comparison-based.** It uses $f$ only in the comparisons of lines L8 and L9, so it is invariant under any strictly increasing transformation of $f$.
- **Not rotation invariant.** The random factors $r_1$ and $r_2$ in line L6 are drawn per coordinate, so the move depends on the coordinate axes. Rotating the problem changes the behavior.
- **Translation invariant.** Shifting $f$ and the start box by the same vector shifts the whole run.

## Variants and improvements

- **Constriction.** Clerc and Kennedy write $v \leftarrow \chi(v + \varphi_1 r_1 \odot (p - x) + \varphi_2 r_2 \odot (g - x))$. It is the inertia form with $w = \chi$ and $c_j = \chi \varphi_j$.
- **Neighborhood topologies.** In the local-best form, $g$ in line L6 is replaced by the best personal best in a neighborhood of particle $i$, such as its two neighbors on a ring. Information spreads more slowly, and the swarm keeps more diversity.
- **Velocity clamping.** The original 1995 form had no inertia weight and limited each velocity coordinate to $[-v_{\max}, v_{\max}]$ to prevent explosion.
- **Fully informed PSO.** Each particle is pulled toward the personal bests of all its neighbors.
- **Bare bones PSO.** Kennedy (2003) dropped the velocity and drew each coordinate of the new position from a normal distribution with mean $(p_d + g_d)/2$ and standard deviation $|p_d - g_d|$.
- **Binary PSO.** Kennedy and Eberhart (1997) used the velocity as the probability, through a sigmoid, that a bit is 1.
- **Standard PSO 2011.** Clerc's reference version draws the new point in a hypersphere around a center of $x$, $p$ and $l$, which makes the move rotation invariant.

The [firefly algorithm](/firefly-algorithm/) and the [bat algorithm](/bat-algorithm/) are forms of PSO, as their pages show.

## When to use it

PSO is simple to implement and needs no gradient, so it is a common first try for continuous black-box problems with a moderate number of variables. When the function is smooth and gradients are available, [gradient descent](/gradient-descent/) and quasi-Newton methods use far fewer evaluations. For hard continuous black-box problems, [CMA-ES](/cma-es/) and [differential evolution](/differential-evolution/) are the standard methods to compare with. Choose by tests on your own problem, with the same budget of evaluations for each method.

## Pitfalls

- **Explosion.** With $w \ge 1$ or $c_1 + c_2$ above the stability limits, the velocities of line L6 grow without bound. Use parameters inside the second-order region, such as the constriction values, or clamp the velocity.
- **Leaving the box.** Line L7 does not keep $x_i$ in $[\ell, u]$. If $f$ is undefined outside, clip the position and set the velocity coordinate to 0, or give such points the value $+\infty$ so that they never become personal bests.
- **Stagnation.** When all particles sit at $g$ with zero velocity, the swarm stops. Restarts or a minimum search radius around $g$ help.
- **Bias toward the center.** On many test functions the optimum is at the center of the box. A swarm that contracts toward the mean of its start points looks good there for the wrong reason. Test on shifted functions.
- **Synchronous and asynchronous forms.** The two forms of line L9 give different runs. State which one you use.

## Implementations

## History

Kennedy, a social psychologist, and Eberhart, an electrical engineer, introduced the particle swarm in 1995. It grew out of simulations of bird flocks and of the spread of opinions in a group. Shi and Eberhart (1998) added the inertia weight $w$. Clerc and Kennedy (2002) analysed the one-particle deterministic model, and Clerc and Kennedy derived the constriction coefficient from it. Kennedy and Mendes studied the effect of neighborhood topologies. Poli (2009) gave the exact first and second moments of the sampling distribution under stagnation. The survey of Poli, Kennedy and Blackwell (2007) covers the field to that date.

## References
