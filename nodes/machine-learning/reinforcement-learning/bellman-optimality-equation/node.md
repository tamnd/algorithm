---
tag: R9MX23
kind: concept
slug: bellman-optimality-equation
name: Bellman optimality equation
aliases:
area: machine-learning/reinforcement-learning
level: intro
summary: "V*(s) = max_a [R(s,a) + gamma sum_s' P(s'|s,a) V*(s')]. Its only solution is the optimal value, and any greedy policy for it is optimal."
prereqs: [bellman-expectation-equation]
see_also: [bellman-contraction, value-iteration, policy-iteration, linear-programming-for-mdps, q-learning, policy-improvement-theorem, bellman-equation, markov-game]
sources:
  - paper: "Richard Bellman, A Markovian Decision Process, Journal of Mathematics and Mechanics 6(5), 1957"
    title: A Markovian Decision Process
    locator: "the functional equation for the discounted problem"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 6.2 (the optimality equations), Theorem 6.2.10"
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.6 (equations 3.19 and 3.20, the Bellman optimality equations)"
---

The Bellman optimality equation says that the optimal value of a state is the best, over the actions, of the expected reward of one step plus the discounted optimal value of the next state. In a finite discounted [MDP](/markov-decision-process/) it has exactly one solution, the optimal [state value function](/state-value-function/) $V^*$, and a policy that is greedy for that solution is optimal. Most planning and control methods in reinforcement learning are ways to solve it.

## In plain words

Suppose you already know the best long term worth of every situation. Then the best worth of the situation you are in now is easy to find: try each choice, add what it gives now to the worth of where it leads, made a little smaller because it comes later, and keep the largest total. The true best worths are the only numbers that pass this test in every situation at once. Once you have them, acting well needs no more look ahead: in each situation, take a choice that gives the largest total. Value iteration applies the test as an update again and again. Policy iteration switches between a fixed way of acting and its best one step change. Q-learning does the same from experience, without a model.

## The idea

Fix a finite MDP $(S, A, P, R, \gamma)$ with $0 \le \gamma < 1$.

**The equations.** For every state $s$ and action $a$,

$$V^*(s) = \max_a \left[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^*(s')\right],$$

$$Q^*(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) \max_{a'} Q^*(s', a').$$

With the operator $(T^* v)(s) = \max_a [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) v(s')]$, the first one reads $V^* = T^* V^*$. It is not linear, because of the max.

**Unique solution.** $T^*$ is a $\gamma$-contraction in the max norm ([Bellman contraction](/bellman-contraction/)). By the Banach fixed point theorem it has exactly one fixed point $v^*$.

**The fixed point is the optimal value, and greedy policies are optimal.** Let $v^* = T^* v^*$, and let $d$ be a deterministic policy with $d(s) \in \arg\max_a [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) v^*(s')]$.

1. *$v^*$ is the value of $d$.* By the choice of $d$, $T^d v^* = T^* v^* = v^*$. The [Bellman expectation equation](/bellman-expectation-equation/) for $d$ has only one solution, so $V^d = v^*$.
2. *No stationary policy does better.* For a stationary policy $\pi$, a mean over actions is at most the max, so $T^\pi v \le T^* v$ for every $v$. Also $T^*$ is monotone: $u \le w$ implies $T^* u \le T^* w$. So $V^\pi = T^\pi V^\pi \le T^* V^\pi$, and by induction $V^\pi \le (T^*)^k V^\pi$ for all $k$. The right side tends to $v^*$, so $V^\pi \le v^*$.
3. *No policy at all does better.* For history-dependent and randomized policies the same bound holds. The proof bounds the expected reward of the first $k$ steps by $(T^*)^k 0$, by induction on the steps, and lets $k \to \infty$. See the [MDP page](/markov-decision-process/) and Puterman, Theorem 6.2.10.

So $v^* = V^* = \sup_\pi V^\pi$, the sup is a max, and a deterministic stationary policy attains it in every state at once. Then $Q^*(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^*(s')$ solves the $Q$ form, with $V^*(s) = \max_a Q^*(s, a)$.

**The converse.** A stationary policy $\pi$ is optimal only if it puts all its mass on actions that are greedy for $V^*$. If $\pi(a \mid s) > 0$ for an action with $Q^*(s, a) < V^*(s)$, then $T^\pi V^* \le V^*$ with $(T^\pi V^*)(s) < V^*(s)$. By monotonicity $V^\pi = \lim_k (T^\pi)^k V^* \le T^\pi V^*$, so $V^\pi(s) < V^*(s)$.

**The finite horizon form.** With $H$ steps left and no discount, $u_H(s) = \max_a [R(s, a) + \sum_{s'} P(s' \mid s, a) u_{H-1}(s')]$ and $u_0 = 0$. This is backward induction, the original [dynamic programming](/dynamic-programming/) recursion. The optimal action now depends on the steps left.

**A linear program.** $V^*$ is the smallest $v$ with $v \ge T^* v$, or with $v(s) \ge R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) v(s')$ for all pairs. Minimizing $\sum_s v(s)$ under these constraints gives [linear programming for MDPs](/linear-programming-for-mdps/).

**Solution methods.** [Value iteration](/value-iteration/) applies $T^*$ until the change is small. [Policy iteration](/policy-iteration/) solves the linear equation of the current policy and then takes the greedy policy, and stops in finitely many steps with the exact answer. [Q-learning](/q-learning/) uses samples of the $Q$ form.

## Examples

Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$: in $s_1$, *stay* gives 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$.

- **The check.** $V^* = (360/31, 440/31)$. In $s_1$: stay gives $1 + \frac{9}{10} \cdot \frac{360}{31} = \frac{355}{31}$ and switch gives $\frac{9}{10}\left(\frac12 \cdot \frac{360}{31} + \frac12 \cdot \frac{440}{31}\right) = \frac{360}{31}$. The max is $360/31$, as required. In $s_2$: stay gives $2 + \frac{9}{10}\left(\frac14 \cdot \frac{360}{31} + \frac34 \cdot \frac{440}{31}\right) = \frac{440}{31}$ and switch gives $3 + \frac{9}{10} \cdot \frac{360}{31} = \frac{417}{31}$. The max is $440/31$.
- **The greedy policy.** It is (switch, stay). Its value is $(360/31, 440/31)$, and it is the best of the four deterministic policies, found by enumeration.
- **Value iteration.** From $v_0 = 0$: $v_1 = (1, 3)$, $v_2 = (19/10, 17/4)$, $v_3 = (1107/400, 4237/800)$. The greedy policy for $v_0$ is (stay, switch), for $v_1$ it is (stay, stay), and from $v_2$ on it is the optimal (switch, stay). With floats the error after 10, 50 and 100 sweeps is about 4.25, 0.063 and 0.00032. The greedy policy settles long before the values do.
- **The discount matters.** For $\gamma = 1/2$ the solution has the greedy policy (stay, switch), and for $\gamma = 7/10$ it is (stay, stay). A short horizon favors the quick reward of *switch* in $s_2$. A long one favors the trip from $s_1$ to the better state $s_2$.
- **Non-example: the mean in place of the max.** Replace the max by the mean of the uniform policy. The result is the Bellman expectation equation of that policy, with the solution $(715/71, 875/71)$, below $V^*$ in both states.

## Where it is used

- **Planning.** [Value iteration](/value-iteration/), [policy iteration](/policy-iteration/), [modified policy iteration](/modified-policy-iteration/) and [linear programming for MDPs](/linear-programming-for-mdps/) solve it with a known model. The planning area states it as the [Bellman equation](/bellman-equation/) and uses it for [stochastic shortest path](/stochastic-shortest-path/) problems.
- **Model-free control.** [Q-learning](/q-learning/), [fitted Q-iteration](/fitted-q-iteration/) and [DQN](/dqn/) use sampled targets $r + \gamma \max_{a'} Q(s', a')$ from the $Q$ form.
- **Games.** In a [Markov game](/markov-game/) the max becomes the value of a matrix game, and the same contraction argument works.
- **Partial observability.** In a [POMDP](/pomdp/) the equation holds on beliefs, with an expectation over observations.

## References
