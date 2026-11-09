---
tag: F7GN0A
kind: algorithm
slug: bat-algorithm
name: Bat algorithm
aliases:
- BA
area: optimization/metaheuristics
level: research
summary: A population method with a PSO velocity of inertia 1, a random walk around the best point, and greedy acceptance with a falling probability. It is a form of particle swarm optimization.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {D: the number of variables, n: the number of bats, T: the number of iterations, c: the cost of one evaluation of f}
  time: {worst: O(T n (D + c))}
  space: {extra: O(n D)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 2010
  people: [Xin-She Yang]
  note: Yang published the bat algorithm in 2010 with a metaphor of echolocation. Camacho-Villalón, Dorigo and Stützle showed in 2020 and 2023 that it is a form of particle swarm optimization.
prereqs: [particle-swarm-optimization]
see_also: [firefly-algorithm, cuckoo-search, harmony-search, swarm-intelligence, simulated-annealing, evolution-strategies, differential-evolution, no-free-lunch-theorem]
sources:
  - paper: doi:10.1007/978-3-642-12538-6_6
    title: Xin-She Yang, A new metaheuristic bat-inspired algorithm, Nature Inspired Cooperative Strategies for Optimization (NICSO 2010), Studies in Computational Intelligence 284, Springer, 2010
    locator: pages 65 to 74 (the frequency, velocity and position equations, the local walk with the mean loudness, and the updates of loudness and pulse rate)
  - paper: doi:10.1007/978-3-030-60376-2_10
    title: Christian Leonardo Camacho-Villalón, Marco Dorigo and Thomas Stützle, Grey wolf, firefly and bat algorithms, three widespread algorithms that do not contain any novelty, ANTS 2020, LNCS 12421, Springer, 2020
    locator: pages 121 to 133 (the bat algorithm written as a particle swarm optimization variant)
  - paper: doi:10.1111/itor.13176
    title: Christian Leonardo Camacho-Villalón, Marco Dorigo and Thomas Stützle, Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms, six misleading optimization techniques inspired by bestial metaphors, International Transactions in Operational Research 30(6), 2023
    locator: pages 2945 to 2971 (the bat section and the comparison of its terms with PSO)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18 (the critique of methods presented through a natural metaphor)
  - paper: doi:10.4018/jamc.2010040104
    title: Dennis Weyland, A rigorous analysis of the harmony search algorithm, how the research community can be misled by a novel methodology, International Journal of Applied Metaheuristic Computing 1(2), 2010
    locator: pages 50 to 60 (the first detailed case of a metaphor-based method that reduces to a known method)
  - paper: doi:10.1109/ICNN.1995.488968
    title: James Kennedy and Russell Eberhart, Particle swarm optimization, Proceedings of ICNN'95, International Conference on Neural Networks, IEEE, 1995
    locator: pages 1942 to 1948 (the velocity and position updates without inertia weight, that is with weight 1)
  - paper: doi:10.1109/4235.985692
    title: Maurice Clerc and James Kennedy, The particle swarm, explosion, stability, and convergence in a multidimensional complex space, IEEE Transactions on Evolutionary Computation 6(1), 2002
    locator: pages 58 to 73 (the eigenvalue analysis of the deterministic particle)
  - paper: doi:10.1109/TEVC.2008.2011744
    title: Riccardo Poli, Mean and variance of the sampling distribution of particle swarm optimizers during stagnation, IEEE Transactions on Evolutionary Computation 13(4), 2009
    locator: pages 712 to 721 (the order-1 and order-2 stability region, which needs |w| < 1)
---

The bat algorithm (BA) is a population method for minimizing a function of $D$ real variables. Each of its $n$ points, called bats, has a velocity. In each iteration a bat draws a random number $q$ in $[q_{\min}, q_{\max}]$, called the frequency, adds $q$ times the vector from the best point $x^*$ to the bat to its velocity, and proposes its position plus the velocity. With a probability that falls over the run, this proposal is replaced by a uniform random step around $x^*$. The bat accepts the proposal if it is better and a second random test, whose pass probability falls with each acceptance, succeeds. Yang presented BA in 2010 with a metaphor of bats that use echolocation. It belongs to the family of metaphor-based methods that Sörensen (2015) criticized, and Camacho-Villalón, Dorigo and Stützle (2020, 2023) showed that it is a variant of [particle swarm optimization](/particle-swarm-optimization/). This page describes BA in those terms and makes no claim that it performs better than other methods.

## In plain words

Keep a group of candidate points, each with a speed and direction, and remember the best point seen. In each round, each point changes its speed by a random amount in the direction given by the best point and makes a trial step. Early in the run, the trial step is usually replaced by a small random jump near the best point. The point moves only if the trial is better, and even then only if it passes a coin toss. Each time a point moves, its coin becomes less likely to pass and its jumps near the best point become rarer. Return the best point seen.

## The problem

The input is a function $f : \mathbb{R}^D \to \mathbb{R}$ that can be evaluated at any point, and bounds $\ell_k < u_k$. The goal is a point of the box $B = \prod_k [\ell_k, u_k]$ with a small value of $f$.

## The algorithm

The parameters are the number of bats $n$, the frequency range $[q_{\min}, q_{\max}]$, the initial loudness $A_0$, the maximum pulse rate $r_0$, the factors $\alpha \in (0, 1]$ and $\gamma > 0$, and the number of iterations $T$. Each bat $i$ has a point $x_i$, a velocity $v_i$, a loudness $A_i$ and a pulse rate $r_i$. The paper writes the frequency as $f_i$. This page writes $q$, since $f$ is the objective.

```pseudo id=main
BA(f, ℓ, u, n, q_min, q_max, A0, r0, α, γ, T)
L1  x_i ← a uniform random point of the box, v_i ← 0, A_i ← A0, r_i ← 0 for each i; x* ← the best x_i
L2  for t ← 1 to T do for each bat i:
L3      q ← q_min + (q_max − q_min) β, β ~ U(0, 1); v_i ← v_i + (x_i − x*) q; y ← x_i + v_i   ▷ the sign of the paper
L4      with probability 1 − r_i: y ← x* + ε · mean(A), ε ~ U[−1, 1]^D                    ▷ the local walk
L5      clip y to the box and evaluate f(y)
L6      if f(y) < f(x_i) and a uniform draw is below A_i then x_i ← y; A_i ← α A_i; r_i ← r0 (1 − e^(−γ t))
L7      if f(y) < f(x*) then x* ← y
L8  return x*
```

The paper states the acceptance test of line L6 as $f(x_i) < f(x^*)$ together with the draw below $A_i$. This page compares the proposal with the bat's own point, which makes the bats elitist. Line L7 keeps the best point ever evaluated. Implementations differ on both points.

**In PSO and SA terms.**

- Line L3 is the PSO velocity update $v \leftarrow w v + c_1 \rho_1 (p_i - x) + c_2 \rho_2 (x^* - x)$ with the inertia weight $w = 1$, no personal-best term ($c_1 = 0$), and the random social coefficient $c_2 \rho_2 = -q$. With the sign of the paper and $q_{\min} \ge 0$, this coefficient is not positive, so the velocity term pushes the bat away from $x^*$.
- Line L4 is a mutation of the best point with uniform steps of size $\text{mean}(A)$, the operator of a $(1 + \lambda)$ evolution strategy centered on $x^*$.
- Line L6 is greedy selection, with the extra rule that an improving proposal is rejected with probability $1 - A_i$. The loudness $A_i$ falls by the factor $\alpha$ at each acceptance, like a temperature in [simulated annealing](/simulated-annealing/). It is used the other way round: simulated annealing accepts worse points with a falling probability, while BA rejects better points with a rising probability.
- The pulse rate $r_i$ sets how often the velocity proposal is used instead of the local walk. It starts at 0, so in the first iteration every proposal is a local walk, and it rises toward $r_0$.

## Example

Let $f(x) = x_1^2 + x_2^2$ on $[-5, 5]^2$, with $q_{\min} = 0$, $q_{\max} = 2$, $A_0 = 1$, $r_0 = 0.5$ and $\alpha = \gamma = 0.9$. The bats are $x_1 = (1, 2)$ with $f = 5$, $x_2 = (-1, 0)$ with $f = 1$, and $x_3 = (3, 1)$ with $f = 10$, all with $v = 0$, so $x^* = x_2$.

**Iteration 1, bat 3.** Suppose $\beta = 0.5$, so $q = 1$. Then $v_3 = (3 - (-1), 1 - 0) \cdot 1 = (4, 1)$ and $y = (7, 2)$. This point is farther from $x^*$ than $x_3$. With the opposite sign, $q = -1$, the proposal would be $(-1, 0) = x^*$. Since $r_3 = 0$, line L4 replaces $y$. With $\text{mean}(A) = 1$ and $\varepsilon = (0.3, -0.2)$, $y = (-0.7, -0.2)$ with $f(y) = 0.53 < 10$. The draw is below $A_3 = 1$, so line L6 accepts: $x_3 \leftarrow (-0.7, -0.2)$, $A_3 \leftarrow 0.9$ and $r_3 \leftarrow 0.5 (1 - e^{-0.9}) \approx 0.2967$. Line L7 sets $x^* \leftarrow (-0.7, -0.2)$, since $0.53 < 1$. The velocity $v_3 = (4, 1)$ is kept, although its proposal was not used.

**Iteration 2, bat 3.** Now $x_3 = x^*$, so line L3 adds 0 to the velocity. Suppose that line L4 does not act, which has probability $0.2967$. The proposal is $x_3 + v_3 = (3.3, 0.8)$ with $f = 11.53$, far from the best point the bat is sitting on. Line L6 rejects it.

The test file checks these numbers.

## Correctness

BA cannot certify that its result is optimal. The proofs of these invariants are below.

- **Feasibility.** All points lie in the box, since every proposal is clipped.
- **Monotone bats.** The value of each bat never increases, since line L6 accepts only better points.
- **Loudness and pulse rate.** After $k$ acceptances, $A_i = \alpha^k A_0$, and $r_i = r_0 (1 - e^{-\gamma t})$ for the iteration $t$ of the last acceptance.
- **The best point.** After each proposal, $f(x^*)$ is the smallest value among all points evaluated so far.
- **No damping in the velocity.** While a bat does not move, its velocity grows linearly, so its velocity proposals go to the border of the box. If every proposal were accepted, the error would follow $e_{t+1} = (2 + q) e_t - e_{t-1}$: with the sign of the paper it grows geometrically, and with the opposite sign it stays on a bounded orbit and does not tend to 0. This agrees with the PSO stability results of Clerc and Kennedy (2002) and Poli (2009), which need an inertia weight $|w| < 1$.

The page proves no convergence result.

## Complexity

Each proposal costs $O(D)$ work plus one evaluation of $f$, and the mean loudness can be kept as a running sum in $O(1)$ per change. So $T$ iterations cost $O(T n (D + c))$ time and $n T$ evaluations, plus $n$ at the start. The bats take $O(n D)$ space. The Python code recomputes the mean loudness for each local walk, which adds $O(n)$ per proposal.

## Properties

- **Anytime and derivative-free.** $x^*$ is always available, and only values of $f$ are used.
- **Elitist.** Each bat keeps its best point in this version, and $x^*$ is the best point ever evaluated.
- **Invariant to monotone changes of $f$.** Lines L6 and L7 only compare values.
- **Coordinate dependent.** The local walk uses a uniform box of steps, so the behavior changes if the problem is rotated.

## Variants and improvements

- **The sign of the velocity term.** Some codes use $(x^* - x_i)$, or draw $q$ from a negative range, which turns the push into a pull. By Claim 6 of the proof, even the pull has inertia weight 1 and does not damp.
- **The acceptance test.** Some codes compare the proposal with $x^*$, as the text of the paper does, and some with the bat's own point, as here.
- **Constant loudness and pulse rate.** Some published codes keep $A_i$ and $r_i$ fixed, which removes the schedule of lines L6 and L4.
- **Discrete, binary and multiobjective BA, and hybrids.** These change the move, the representation or the selection. In PSO terms, each changes the attractor, the coefficients or the acceptance.

## When to use it

If you need a method of this kind, standard particle swarm optimization with an inertia weight inside its stability region, [evolution strategies](/evolution-strategies/), [differential evolution](/differential-evolution/) and [CMA-ES](/cma-es/) have well-studied operators and well-tested implementations. If you use BA, describe it by its operators as above, state the sign of the velocity term, the acceptance test and the schedules, and compare it with standard methods on your own problems with the same number of evaluations. This page reports no comparison between methods.

## Pitfalls

- **The sign of $(x_i - x^*)$.** With $q \ge 0$, the velocity of the paper points away from the best point. Read the code before you describe what it does.
- **The velocity may do nothing.** We ran the Python code of this page with $n = 20$, $A_0 = 1$, $r_0 = 0.5$, $\alpha = \gamma = 0.9$ and 500 iterations, on the sphere in $[-5.12, 5.12]^5$ and the Rastrigin function in $[-5.12, 5.12]^2$, with $q \in [0, 2]$ and with $q \in [-2, 0]$, for seeds 0, 1 and 2. In all 12 runs, no velocity proposal set a new best point, at most 9 of about 4900 velocity proposals per run were accepted, and between 86 and 99 percent of them lay on the border of the box. All the progress came from the local walk around $x^*$. The test file checks the counts of the run on the sphere with $q \in [0, 2]$ and seed 0. These runs show the behavior of one implementation on two functions, not the general behavior of BA.
- **Acceptance gets harder as the run goes on.** Each acceptance multiplies $A_i$ by $\alpha$, so a bat that has moved often rejects most improvements. The step size of the local walk is the mean loudness, so it stops falling when acceptances stop.
- **Units.** The local walk adds $\varepsilon \cdot \text{mean}(A)$ in the units of $x$, so $A_0$ must be chosen relative to the size of the box.
- **The metaphor.** Frequency, loudness and pulse rate name a random coefficient, an acceptance probability and a mutation probability. Sörensen (2015) asks that methods be described by their operators.

## Implementations

## History

Yang presented the bat algorithm at the NICSO 2010 workshop, with a metaphor of microbats that find prey by echolocation and change the frequency, loudness and pulse rate of their calls. Many variants and applications followed. Particle swarm optimization (Kennedy and Eberhart, 1995) had the same velocity and position updates, and Clerc and Kennedy (2002) and Poli (2009) showed that their stability needs an inertia weight below 1 in absolute value. Weyland (2010) showed for harmony search that a method named after a metaphor can be a special case of a known method, and Sörensen (2015) criticized the general practice. Camacho-Villalón, Dorigo and Stützle analyzed BA at ANTS 2020 and in a longer 2023 paper, and concluded that it is a PSO variant with no new idea for optimization.

## References
