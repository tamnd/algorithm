---
tag: CDVZ8N
kind: problem
slug: mdp-planning
name: MDP planning
aliases:
- optimal control with known model
- solving a known MDP
area: machine-learning/reinforcement-learning
level: intro
summary: "Given a finite MDP with known transitions and rewards, find an optimal policy and its values. Linear programming solves it in polynomial time, and it is P-complete."
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, L: the number of bits of the input}
  time: {worst: "poly(S, A, L)"}
prereqs: [markov-decision-process, bellman-optimality-equation]
see_also: [rl-control, policy-evaluation, stochastic-shortest-path, pomdp-planning, markov-game, linear-programming-problem, circuit-value-problem, real-time-dynamic-programming]
sources:
  - paper: doi:10.1287/moor.12.3.441
    title: "Christos H. Papadimitriou and John N. Tsitsiklis, The complexity of Markov decision processes, Mathematics of Operations Research 12(3), 1987, pages 441 to 450"
    locator: the P-completeness of the finite horizon, discounted and average cost problems, and the PSPACE-completeness of the partially observed finite horizon problem
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Chapter 4 (finite horizon) and Chapter 6 (discounted models, the existence of optimal deterministic stationary policies, and the solution methods)
  - paper: "Michael L. Littman, Thomas L. Dean and Leslie Pack Kaelbling, On the complexity of solving Markov decision problems, Proceedings of the Eleventh Conference on Uncertainty in Artificial Intelligence (UAI), 1995, pages 394 to 402"
    locator: the survey of the bounds for value iteration, policy iteration and linear programming
  - paper: doi:10.1287/moor.1110.0516
    title: "Yinyu Ye, The simplex and policy-iteration methods are strongly polynomial for the Markov decision problem with a fixed discount rate, Mathematics of Operations Research 36(4), 2011, pages 593 to 603"
    locator: the main theorems (strongly polynomial bounds for a fixed discount)
---

MDP planning is the problem of computing an optimal [policy](/policy/) for a [Markov decision process](/markov-decision-process/) whose transition probabilities and rewards are given in full. It is the problem that dynamic programming solves. Under the discounted criterion with rational data it can be solved in polynomial time by [linear programming](/linear-programming-for-mdps/), and Papadimitriou and Tsitsiklis (1987) proved that it is P-complete. The same problem with an unknown model, where the agent learns from samples, is [reinforcement learning control](/rl-control/).

## In plain words

You have a full map of a world with chance in it. For each place and each action, you know the reward you get and the odds of where you land next. Rewards that come later count a little less. You want a rule that says what to do in each place, so that the total reward you expect is as large as possible from every starting place.

A best rule always exists, and you can choose one that does not use coins and does not depend on the past. The task is to find it. It is a computation on the map, with no trial and error.

## Definition

**Input.** A finite MDP $(S, A, P, R, \gamma)$: a set $S$ of states, a set $A(s)$ of actions in each state, transition probabilities $P(s' \mid s, a)$, expected rewards $R(s, a)$, and a discount factor $0 \le \gamma < 1$. For complexity, all numbers are rationals, and $L$ is the number of bits needed to write them.

**Output.** A deterministic stationary policy $\pi^*$, which picks one action in each state, such that $V^{\pi^*}(s) = V^*(s) = \max_\pi V^\pi(s)$ for every state $s$, where the maximum is over all policies, including randomized and history-dependent ones. Often the output also includes $V^*$, the unique solution of the [Bellman optimality equation](/bellman-optimality-equation/). An optimal deterministic stationary policy always exists for a finite discounted MDP (Puterman, Chapter 6).

**Decision version.** Given the MDP, a state $s_0$ and a rational $t$, decide whether $V^*(s_0) \ge t$. The complexity results below are stated for this version.

**Approximate version.** Given $\varepsilon > 0$, find a policy $\pi$ with $V^\pi(s) \ge V^*(s) - \varepsilon$ for every state.

## Variants

- **Finite horizon.** Maximize the sum of rewards over $H$ steps. The optimal policy depends on the time step. Backward induction solves it in $O(H|S|^2|A|)$ arithmetic operations.
- **Discounted.** The main case of this page.
- **Average reward.** Maximize the long-run average reward per step. Optimal stationary policies still exist, and policy iteration and linear programming solve it with gain and bias vectors.
- **Total reward and shortest paths.** Minimize the expected total cost to reach a goal set: the [stochastic shortest path](/stochastic-shortest-path/) problem. The deterministic case is the shortest path problem.
- **Partial observation.** The agent sees observations, not states: [POMDP planning](/pomdp-planning/). The finite horizon problem is PSPACE-complete (Papadimitriou and Tsitsiklis 1987).
- **Two players.** A [Markov game](/markov-game/) has an opponent in some states. Turn-based stochastic games are in NP and coNP, and no polynomial time algorithm is known for them when the discount is part of the input.
- **Constraints.** Maximize one reward subject to bounds on other expected rewards. Optimal policies may need randomization, and linear programming over occupancy measures is the standard method.

## Examples

- **Two states.** In the example of [value iteration](/value-iteration/), with $\gamma = 0.9$, staying in state L gives 1 per step and moving gives 0 now and reaches, with probability $1/2$, the state H that pays 2 per step (else it stays in L). The optimal policy moves in L and stays in H, with $V^* = (180/11, 20)$. Four deterministic policies exist, and the brute force answer agrees.
- **Gridworld.** A robot on a grid with walls, a goal with a reward, and moves that slip with some probability. The optimal policy is a map of arrows.
- **Inventory control.** The state is the stock level, the action is the order size, demand is random, and the reward is sales income minus order and holding costs.

## Known algorithms

| algorithm | idea | guarantee |
| --- | --- | --- |
| [Value iteration](/value-iteration/) | repeat the Bellman optimality backup | $\varepsilon$-optimal; iterations grow with $1/(1-\gamma)$ |
| [Policy iteration](/policy-iteration/) | exact evaluation, then greedy improvement | exact; strongly polynomial for a fixed $\gamma$ |
| [Modified policy iteration](/modified-policy-iteration/) | greedy step, then $m$ evaluation backups | $\varepsilon$-optimal; contains the two above |
| [Linear programming](/linear-programming-for-mdps/) | primal over values, dual over occupancy measures | exact; polynomial time with an interior point method |
| [Prioritized sweeping](/prioritized-sweeping/) | backups ordered by the Bellman error | $\varepsilon$-optimal; fewer backups in practice |
| [Real-time dynamic programming](/real-time-dynamic-programming/) | backups along simulated trajectories from a start state | optimal on the reachable states, for shortest path problems |
| backward induction | one backward pass over the time steps | exact, for the finite horizon only |

## Bounds

**Polynomial time.** The discounted, average reward and finite horizon problems are linear programs of size polynomial in $|S|$, $|A|$ and $L$ (d'Epenoux 1963; Manne 1960). Since [linear programming is in P](/lp-in-p/), MDP planning is in [P](/p/). The resulting bounds depend on $L$, so they are weakly polynomial.

**P-completeness.** Papadimitriou and Tsitsiklis (1987) proved that the finite horizon, discounted and average cost problems are P-complete, by a reduction from the [circuit value problem](/circuit-value-problem/). So MDP planning has no fast parallel algorithm ([NC](/nc/)) unless every problem in P has one. They also showed that the deterministic versions are much easier in parallel.

**Strongly polynomial for a fixed discount.** Ye (2011) proved that policy iteration and the simplex method with Dantzig's rule stop after $O\big(\frac{|S||A| \cdot |S|}{1-\gamma}\log\frac{|S|}{1-\gamma}\big)$ iterations, and Hansen, Miltersen and Zwick (2013) improved the bound for policy iteration by a factor of $|S|$. The number of arithmetic operations does not depend on $L$. These bounds grow with $1/(1-\gamma)$, so they are not polynomial when $\gamma$ is part of the input.

**Value iteration.** The number of sweeps of value iteration that are needed to find an optimal policy is bounded by a polynomial in $|S|$, $|A|$, $L$ and $1/(1-\gamma)$ (Tseng 1990, as reported by Littman, Dean and Kaelbling 1995), but it is not bounded in terms of $|S|$ and $|A|$ alone, even for a fixed $\gamma$ (Feinberg and Huang 2014).

**Lower bounds for specific methods.** Policy iteration needs exponentially many iterations on some total reward and average reward MDPs (Fearnley 2010). These bounds are for one method, not for the problem.

## Reductions

- **To linear programming.** The values $V^*$ are the optimal solution of the primal LP $\min \sum_s \alpha(s)V(s)$ subject to $V(s) \ge R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)V(s')$ for every pair $(s, a)$, with any positive weights $\alpha$. See [linear programming for MDPs](/linear-programming-for-mdps/).
- **From circuit value.** Any Boolean circuit can be turned in logarithmic space into an MDP whose optimal value at one state tells the output of the circuit. This gives P-hardness.
- **Shortest paths.** A deterministic MDP with costs and a goal state, without discount, is a single-destination shortest path problem, and value iteration on it is the [Bellman-Ford algorithm](/bellman-ford/).
- **Policy evaluation.** Each step of policy iteration reduces to [policy evaluation](/policy-evaluation/), a linear system.

## Applications

MDP planning is used in operations research (inventory, maintenance, queueing control, and the control of reservoirs), in robot navigation with a known map, and in medical treatment planning. Inside reinforcement learning it is the planning step of [model-based methods](/model-based-reinforcement-learning/): the agent learns a model from data and then solves this problem on the learned model, as in [Dyna-Q](/dyna-q/) and certainty equivalence.

## References
