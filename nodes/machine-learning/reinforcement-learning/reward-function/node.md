---
tag: AMCRZY
kind: definition
slug: reward-function
name: Reward function
aliases:
- reward signal
- MDP reward function
area: machine-learning/reinforcement-learning
level: intro
summary: "The part of an MDP that gives the scalar reward of each step, as R(s, a) or R(s, a, s'). The agent's goal is a large expected sum of these rewards."
prereqs: [markov-decision-process]
see_also: [discounted-return, state-value-function, potential-based-reward-shaping, inverse-reinforcement-learning, multi-armed-bandit]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.1 (the dynamics p(s', r | s, a) and the expected rewards r(s, a) and r(s, a, s')), Section 3.2 (goals and rewards, the reward hypothesis)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 2.1 (rewards that depend on the next state, and their expected values)"
  - paper: "A. Y. Ng, D. Harada and S. Russell, Policy invariance under reward transformations: theory and application to reward shaping, Proceedings of ICML 1999, pages 278-287"
    title: Ng, Harada and Russell 1999
    locator: potential-based shaping keeps the optimal policies, and other shapings can change them
  - paper: "D. Abel, W. Dabney, A. Harutyunyan, M. K. Ho, M. L. Littman, D. Precup and S. Singh, On the expressivity of Markov reward, Advances in Neural Information Processing Systems 34 (NeurIPS 2021)"
    title: Abel et al. 2021
    locator: some tasks given as sets of acceptable policies have no Markov reward function
---

The reward function of a [Markov decision process](/markov-decision-process/) gives the number that the agent receives after each step. It can depend on the state and the action, $R(s, a)$, or also on the next state, $R(s, a, s')$. The agent's goal is a large expected sum of rewards, the expected [discounted return](/discounted-return/), so the reward function is where the designer states the task.

## Definition

Let $(S, A, P, R, \gamma)$ be a finite MDP. The reward at step $t$ is a real random variable $R_{t+1}$ that arrives with the next state $S_{t+1}$. Its law is part of the dynamics

$$p(s', r \mid s, a) = \Pr(S_{t+1} = s', R_{t+1} = r \mid S_t = s, A_t = a).$$

There are three common forms of the reward function, from the most detailed to the least:

- **Next-state reward:** $R(s, a, s') = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a, S_{t+1} = s']$.
- **Expected reward:** $R(s, a) = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a] = \sum_{s'} P(s' \mid s, a)\, R(s, a, s') = \sum_{s', r} r\, p(s', r \mid s, a)$.
- **State reward:** $R(s)$, when the reward does not depend on the action.

A reward function is *bounded* when $|R_{t+1}| \le R_{\max}$ almost surely. The bound makes each discounted sum finite.

**Only the expectation matters.** For a fixed policy $\pi$, the finite horizon, discounted and average reward values depend on the reward only through $R(s, a)$. The reason is linearity: $\mathbb{E}^\pi[\gamma^t R_{t+1}] = \gamma^t\, \mathbb{E}^\pi[\mathbb{E}[R_{t+1} \mid S_t, A_t]] = \gamma^t\, \mathbb{E}^\pi[R(S_t, A_t)]$ by the tower rule and the Markov property, and the sum over $t$ can be taken outside the expectation because $\sum_t \gamma^t R_{\max}$ is finite. So a planner may replace $R(s, a, s')$ by $R(s, a)$ with no change in any value or in the optimal policies. The variance of the return does change, which matters for learning from samples.

**The reward hypothesis.** Sutton and Barto (Section 3.2) state as a hypothesis that all goals and purposes can be well thought of as the maximization of the expected value of the cumulative sum of a received scalar reward. It is a working assumption of the field, not a theorem, and it has known limits: Abel et al. (2021) give tasks, stated as sets of acceptable policies, that no Markov reward function on the given states can express.

**Transformations.** Let $R'(s, a) = c R(s, a) + b$ with $c > 0$. In a continuing discounted MDP every policy then has $V'^\pi = c V^\pi + b/(1-\gamma)$, so the optimal policies stay the same. This fails in an episodic task, where the shift $b$ is paid only until the episode ends. Shaping rewards of the form $\gamma \Phi(s') - \Phi(s)$ keep the optimal policies, in episodic tasks too when $\Phi = 0$ at the terminal states ([potential-based reward shaping](/potential-based-reward-shaping/), Ng, Harada and Russell 1999).

## Examples and non-examples

- **Expected reward of the running example.** In the two-state MDP of the [MDP page](/markov-decision-process/), let *switch* in $s_1$ pay $-2$ when it stays in $s_1$ and $2$ when it reaches $s_2$, each with probability 1/2. Then $R(s_1, \text{switch}) = \frac12(-2) + \frac12(2) = 0$, which is the expected reward in the table there. Every value of every policy is the same under the two descriptions, for example $V^*(s_1) = 360/31$.
- **Cost per step.** A maze task gives $-1$ per step until the exit. The largest return is the shortest expected path, so this reward states "reach the exit fast".
- **Shift in an episodic task.** One state with two actions and $\gamma = 1/2$: *end* gives 0 and ends the episode, *loop* gives $-1$ and stays. The best action is end, with value 0 against $-1/(1 - 1/2) = -2$. Add 3 to both rewards: end gives 3, but loop gives $2/(1-1/2) = 4$, so now the best action is loop. A constant shift changed the task.
- **Positive scaling.** Multiply all rewards of a continuing discounted MDP by 2 and add 5. Each value becomes $2V^\pi + 5/(1-\gamma)$, and the optimal policies do not change.
- **Bandit rewards.** In a [multi-armed bandit](/multi-armed-bandit/) the reward function is the mean $R(a)$ of each arm, and the state plays no part.
- **Non-example: a vector of rewards.** A reward with two parts, such as speed and safety, does not fit the definition until the parts are combined into one number. Without a weighting the best policy is not defined; this is the subject of multi-objective methods.
- **Non-example: a reward of the whole trajectory.** "Reward 1 if the agent ever visited state $s$ and then state $s'$" depends on the history, not on one step. It becomes a reward function only on a larger state that records the visit.
- **Non-example: unbounded rewards.** A reward that can grow without bound, for example $R(s_k) = 2^k$ on a chain $s_1, s_2, \ldots$ that moves right each step with $\gamma = 1/2$, gives an infinite discounted sum. The standard results assume bounded rewards.

## Related definitions

- [Markov decision process](/markov-decision-process/): the model that holds the reward function.
- [Discounted return](/discounted-return/): the sum of rewards that the agent maximizes in expectation.
- [Discount factor](/discount-factor/): the weight of later rewards.
- [State value function](/state-value-function/): the expected return of a policy.
- [Potential-based reward shaping](/potential-based-reward-shaping/): extra rewards that keep the optimal policies.
- [Inverse reinforcement learning](/inverse-reinforcement-learning/): find a reward function that explains the behavior of an expert.

## References
