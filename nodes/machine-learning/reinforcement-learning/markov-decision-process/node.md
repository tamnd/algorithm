---
tag: W1VDJ0
kind: model
slug: markov-decision-process
name: Markov decision process
aliases:
- MDP
- finite MDP
- Markovian decision process
area: machine-learning/reinforcement-learning
level: intro
summary: "A model of sequential decisions: states, actions, transition probabilities, rewards and a discount factor. The next state depends only on the current state and action."
prereqs: [markov-chain]
see_also: [policy, state-value-function, bellman-optimality-equation, value-iteration, policy-iteration, pomdp, markov-game, stochastic-shortest-path]
sources:
  - paper: "R. Bellman, A Markovian decision process, Journal of Mathematics and Mechanics 6(5):679-684, 1957"
    title: Bellman 1957
    locator: the model and its functional equation for the discounted criterion
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Chapter 2 (the model, decision rules and policies), Chapter 4 (finite horizon, backward induction), Section 5.5 (Markov policies), Theorem 6.2.10 (a deterministic stationary optimal policy exists), Chapters 8 and 9 (average reward)"
  - paper: "R. A. Howard, Dynamic Programming and Markov Processes, MIT Press, 1960"
    title: Howard 1960
    locator: the discounted and the average reward models, and policy iteration for both
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Chapter 3, Sections 3.1 to 3.6"
  - paper: doi:10.1214/aoms/1177704593
    title: "D. Blackwell, Discrete dynamic programming, Annals of Mathematical Statistics 33(2):719-726, 1962"
    locator: one deterministic stationary policy is optimal for all discount factors close to 1
  - paper: doi:10.1287/moor.12.3.441
    title: "C. H. Papadimitriou and J. N. Tsitsiklis, The complexity of Markov decision processes, Mathematics of Operations Research 12(3):441-450, 1987"
    locator: finite horizon, discounted and average cost MDPs are P-complete
  - paper: doi:10.1287/moor.1110.0516
    title: "Y. Ye, The simplex and policy-iteration methods are strongly polynomial for the Markov decision problem with a fixed discount rate, Mathematics of Operations Research 36(4):593-603, 2011"
    locator: the strongly polynomial bound for a fixed discount factor
---

A Markov decision process (MDP) is a model of an agent that makes a sequence of decisions under uncertainty. In each step the agent sees the state, picks an action, gets a [reward](/reward-function/) and moves to a random next state, and the distribution of the next state depends only on the current state and action. A [policy](/policy/) says how to pick the actions, and the goal is a policy with the largest expected total reward, usually weighted by a [discount factor](/discount-factor/). The MDP is the standard model for planning under uncertainty and for reinforcement learning.

## The machine

A finite MDP is a tuple $(S, A, P, R, \gamma)$:

- $S$ is a finite set of states.
- $A$ is a finite set of actions. $A(s) \subseteq A$ is the set of actions that are allowed in state $s$. Often $A(s) = A$.
- $P(s' \mid s, a) \ge 0$ is the probability that action $a$ in state $s$ leads to state $s'$, with $\sum_{s'} P(s' \mid s, a) = 1$ for each pair $(s, a)$.
- $R(s, a)$ is the expected reward of action $a$ in state $s$. The rewards are bounded: $|R(s, a)| \le R_{\max}$.
- $\gamma \in [0, 1)$ is the [discount factor](/discount-factor/) of the discounted criterion.

The agent and the environment interact in discrete time. The start state $S_0$ comes from an initial distribution $\mu$. At each step $t = 0, 1, 2, \ldots$ the agent picks an action $A_t \in A(S_t)$. Then the environment draws a reward $R_{t+1}$ and a next state $S_{t+1}$, with $\Pr(S_{t+1} = s' \mid S_t = s, A_t = a) = P(s' \mid s, a)$ and $\mathbb{E}[R_{t+1} \mid S_t = s, A_t = a] = R(s, a)$. The reward has the index $t+1$ because it arrives together with the next state. This is the convention of Sutton and Barto.

**The Markov property.** The next state and the reward depend on the past only through the current state and action:

$$\Pr(S_{t+1} = s', R_{t+1} = r \mid S_0, A_0, R_1, \ldots, S_t, A_t) = \Pr(S_{t+1} = s', R_{t+1} = r \mid S_t, A_t).$$

So the state holds all the information about the past that matters for the future. A [policy](/policy/) can use the full history $(S_0, A_0, \ldots, S_t)$, but the results below show that, for the usual criteria, a policy that looks only at the current state is enough.

**The criteria.** The value of a policy $\pi$ from a start state $s$ is one of these three, with $\mathbb{E}^\pi_s$ the expectation over the trajectories that start in $s$ and follow $\pi$:

- finite horizon $H$: $\; v^\pi_H(s) = \mathbb{E}^\pi_s\left[\sum_{t=0}^{H-1} R_{t+1}\right]$,
- discounted, $0 \le \gamma < 1$: $\; V^\pi(s) = \mathbb{E}^\pi_s\left[\sum_{t=0}^{\infty} \gamma^t R_{t+1}\right]$, which is the expected [discounted return](/discounted-return/), and $|V^\pi(s)| \le R_{\max}/(1-\gamma)$,
- average reward: $\; g^\pi(s) = \liminf_{H \to \infty} \frac{1}{H}\, \mathbb{E}^\pi_s\left[\sum_{t=0}^{H-1} R_{t+1}\right]$.

A policy $\pi^*$ is optimal when $V^{\pi^*}(s) \ge V^\pi(s)$ for every state $s$ and every policy $\pi$ at the same time. The [state value function](/state-value-function/) and the [action value function](/action-value-function/) are the main tools to find it.

**An example.** The MDP below has two states $s_1, s_2$, two actions *stay* and *switch*, and $\gamma = 9/10$.

| state | action | $R(s, a)$ | $P(s_1 \mid s, a)$ | $P(s_2 \mid s, a)$ |
|---|---|---|---|---|
| $s_1$ | stay | 1 | 1 | 0 |
| $s_1$ | switch | 0 | 1/2 | 1/2 |
| $s_2$ | stay | 2 | 1/4 | 3/4 |
| $s_2$ | switch | 3 | 1 | 0 |

There are $2^2 = 4$ deterministic stationary policies. The value of each one is the solution of the linear system $V = R^d + \gamma P^d V$ of the [Bellman expectation equation](/bellman-expectation-equation/):

| action in $s_1$ | action in $s_2$ | $V(s_1)$ | $V(s_2)$ |
|---|---|---|---|
| stay | stay | 10 | 170/13 ≈ 13.08 |
| stay | switch | 10 | 12 |
| switch | stay | 360/31 ≈ 11.61 | 440/31 ≈ 14.19 |
| switch | switch | 270/29 ≈ 9.31 | 330/29 ≈ 11.38 |

The policy (switch, stay) is the best in both states at the same time. It gives up the reward 1 in $s_1$ to reach $s_2$, where it gets 2 in most steps. The policy that picks each action with probability 1/2 in each state has the values $715/71 \approx 10.07$ and $875/71 \approx 12.32$, which are smaller in both states.

### Pitfalls of modelling

- **A state that is not Markov.** If the state leaves out a quantity that drives the future, for example the speed of a robot when the state holds only its position, then the Markov property fails. The process is then a [POMDP](/pomdp/), and a policy of the current observation can be far from optimal.
- **The reward index.** Some books write $R_t$ for the reward of the step from $S_t$, others $R_{t+1}$. The sums differ by one factor of $\gamma$ when the two are mixed.
- **Discount 1 with no end.** With $\gamma = 1$ and no terminal state, the sum $\sum_t R_{t+1}$ can diverge. Use the average reward criterion, or the [stochastic shortest path](/stochastic-shortest-path/) model with a goal that is reached with probability 1.
- **Optimal for one start state only.** A policy can be optimal for one initial distribution and not optimal in states that the distribution does not reach. The definition above asks for every state.

## What it counts

- **Size.** A finite MDP with explicit tables has $|S|^2 |A|$ transition probabilities and $|S| |A|$ rewards. Complexity results count the length of this table in binary.
- **Planning cost.** For a known MDP the unit is one arithmetic operation. One Bellman backup of all states costs $O(|S|^2 |A|)$ operations, or fewer when the transition table is sparse. The exact value of one fixed stationary policy costs $O(|S|^3)$ operations by [Gaussian elimination](/gaussian-elimination/). Algorithms also count iterations: sweeps of [value iteration](/value-iteration/) or improvement steps of [policy iteration](/policy-iteration/).
- **Learning cost.** When $P$ and $R$ are unknown, the agent learns from samples. The units are the number of transitions or episodes, and the regret, the reward lost against an optimal policy.
- **Policy count.** There are $\prod_s |A(s)|$ deterministic stationary policies, that is $|A|^{|S|}$ when all actions are allowed everywhere. Enumeration is exponential, so it serves only as a test oracle for small MDPs.

## Relation to other models

- **[Markov chain](/markov-chain/).** An MDP with one action in each state is a Markov chain with rewards, also called a Markov reward process. A fixed stationary policy $\pi$ turns any MDP into the Markov chain with matrix $P^\pi(s, s') = \sum_a \pi(a \mid s) P(s' \mid s, a)$.
- **[Multi-armed bandit](/multi-armed-bandit/).** A bandit is an MDP with one state. The action has no effect on the future, so the only difficulty is to learn the rewards.
- **[POMDP](/pomdp/).** The agent does not see the state. It sees an observation whose distribution depends on the state.
- **[Markov game](/markov-game/).** Two or more agents choose actions at the same time, and each has its own reward. A Markov game with one agent is an MDP.
- **[Stochastic shortest path](/stochastic-shortest-path/).** Costs in place of rewards, no discount, and an absorbing goal state. A discounted MDP is a special case: add a goal state that each step reaches with probability $1 - \gamma$.
- **[Dynamic programming](/dynamic-programming/).** An MDP in which each $P(\cdot \mid s, a)$ puts all mass on one state is deterministic. Its finite horizon problem is a longest path problem in a layered graph, which [DP on a DAG](/dp-on-dag/) solves. The general [Bellman equation](/bellman-equation/) of planning is the same recursion.
- **[Hidden Markov model](/hidden-markov-model/).** A hidden Markov model has a hidden state and observations but no actions and no rewards.

## Known results in the model

### A deterministic stationary policy is optimal

**Theorem** (Puterman 1994, Theorem 6.2.10). In a finite MDP with $0 \le \gamma < 1$ there is a deterministic stationary policy $d$ with $V^d(s) \ge V^\pi(s)$ for every state $s$ and every policy $\pi$, including the randomized and history dependent policies.

*Proof.* Let $T^*$ be the Bellman optimality operator, $(T^* u)(s) = \max_{a} [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) u(s')]$, and for a deterministic stationary $d$ let $(T^d u)(s) = R(s, d(s)) + \gamma \sum_{s'} P(s' \mid s, d(s)) u(s')$. Both are $\gamma$-contractions in the max norm ([Bellman contraction](/bellman-contraction/)). Let $V^*$ be the unique fixed point of $T^*$, and let $d(s)$ be an action that attains the maximum in $(T^* V^*)(s)$. Then $T^d V^* = T^* V^* = V^*$, so $V^*$ is the fixed point of $T^d$, which is $V^d$ by the [Bellman expectation equation](/bellman-expectation-equation/).

Now fix any policy $\pi$, a start state $s$ and a number of steps $k$. Let $u_0 = 0$ and $u_m = T^* u_{m-1}$. For $j = k, k-1, \ldots, 0$ and a history $h$ that ends in state $s_j$, let $W_j(h) = \mathbb{E}^\pi[\sum_{t=j}^{k-1} \gamma^{t-j} R_{t+1} \mid h]$. We show $W_j(h) \le u_{k-j}(s_j)$ by induction on $k - j$. For $j = k$ both sides are 0. For $j < k$, the Markov property gives

$$W_j(h) = \sum_a \pi(a \mid h)\Big[R(s_j, a) + \gamma \sum_{s'} P(s' \mid s_j, a)\, W_{j+1}(h, a, s')\Big] \le \sum_a \pi(a \mid h)\Big[R(s_j, a) + \gamma \sum_{s'} P(s' \mid s_j, a)\, u_{k-j-1}(s')\Big] \le u_{k-j}(s_j).$$

The first inequality is the induction hypothesis, and the second holds because a weighted mean is at most the maximum. With $j = 0$ the first $k$ rewards add up to at most $u_k(s)$ in expectation, and the rest is at most $\gamma^k R_{\max}/(1-\gamma)$. So $V^\pi(s) \le u_k(s) + \gamma^k R_{\max}/(1-\gamma)$ for every $k$. As $k \to \infty$, $u_k \to V^*$ by the contraction, so $V^\pi(s) \le V^*(s) = V^d(s)$. $\blacksquare$

The proof also shows that the greedy policy of $V^*$ is optimal. In the example, $d = $ (switch, stay) and $V^* = (360/31, 440/31)$.

### Finite horizon: Markov but not stationary

For the finite horizon criterion, backward induction computes $u_m = T^* u_{m-1}$ with $\gamma = 1$ and $u_0 = 0$, for $m = 1, \ldots, H$, in $O(H |S|^2 |A|)$ operations. The same induction as above shows that $u_H$ is the optimal value and that the greedy decision rules form an optimal deterministic Markov policy (Puterman, Chapter 4). This policy depends on the number of steps left, so in general it is not stationary. In the example with $H = 3$ and no discount, the optimal values are $u_3 = (13/4, 47/8)$. The optimal rule in $s_2$ is stay at steps 0 and 1 and switch at step 2: in the last step the future no longer counts, and switch pays 3 against 2.

### Average reward

For finite MDPs, Blackwell (1962) showed that one deterministic stationary policy is optimal for all discount factors in an interval $(\gamma_0, 1)$. Such a *Blackwell optimal* policy is also optimal for the average reward criterion, so a deterministic stationary average-optimal policy exists. Puterman, Chapters 8 and 9, give the theory and the algorithms. Howard (1960) gave policy iteration for both criteria.

### Complexity

A finite MDP with explicit tables can be solved in polynomial time by [linear programming](/linear-programming-for-mdps/). Papadimitriou and Tsitsiklis (1987) proved that the finite horizon, the discounted and the average cost problems are P-complete, so a fast parallel algorithm is unlikely. In the same paper the finite horizon [POMDP](/pomdp/) is PSPACE-complete. For a fixed discount factor, Ye (2011) proved that policy iteration and the simplex method with Dantzig's rule are strongly polynomial.

## References
