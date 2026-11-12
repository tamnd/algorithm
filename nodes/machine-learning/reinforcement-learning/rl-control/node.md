---
tag: 688AZ8
kind: problem
slug: rl-control
name: Reinforcement learning control
aliases:
- optimal policy learning
- learning an optimal policy from interaction
area: machine-learning/reinforcement-learning
level: intro
summary: "Find a good policy for an MDP whose transitions and rewards are unknown, using only sampled experience. The main solver families are value based, policy based and model based."
prereqs: [markov-decision-process, policy, action-value-function, mdp-planning]
see_also: [policy-evaluation, q-learning, sarsa, monte-carlo-control, actor-critic, model-based-reinforcement-learning, exploration-exploitation-tradeoff, offline-reinforcement-learning]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapters 5, 6, 8 and 13 (Monte Carlo control, TD control, planning and learning, and policy gradient methods)
  - book: isbn:9781608454921
    title: Csaba Szepesvári, Algorithms for Reinforcement Learning, Morgan and Claypool, 2010
    locator: Chapter 4 (control, including the online and the interactive learning settings)
  - paper: doi:10.1007/BF00992698
    title: "Christopher J. C. H. Watkins and Peter Dayan, Q-learning, Machine Learning 8(3-4), 1992, pages 279 to 292"
    locator: the convergence theorem for tabular Q-learning
  - paper: "Mohammad Gheshlaghi Azar, Rémi Munos and Hilbert J. Kappen, Minimax PAC bounds on the sample complexity of reinforcement learning with a generative model, Machine Learning 91(3), 2013"
    locator: the matching upper and lower bounds for estimating the optimal action values with a generative model
  - paper: "Thomas Jaksch, Ronald Ortner and Peter Auer, Near-optimal regret bounds for reinforcement learning, Journal of Machine Learning Research 11, 2010"
    locator: the regret upper bound of UCRL2 and the matching lower bound up to logarithmic factors
---

Reinforcement learning control is the problem of finding a good [policy](/policy/) for a [Markov decision process](/markov-decision-process/) when the transition probabilities and the rewards are not given. The agent learns only from experience: it acts, observes rewards and next states, and improves its policy. With a known model the same goal is [MDP planning](/mdp-planning/). Its companion, the prediction problem, estimates the values of a fixed policy: [policy evaluation](/policy-evaluation/). The solvers fall into three families: value based methods that learn action values, policy based methods that adjust the policy directly, and model based methods that learn a model and plan with it.

## In plain words

You are put into a world you do not know. You can act and see what happens, and sometimes you get a reward. Nobody tells you the odds or the rules. You want to end up with a way of acting that collects as much reward as possible.

Two things make this hard. First, you must learn from your own tries, which cost time and sometimes cost reward. Second, you must balance trying new actions, which may be better, against using the actions that look best now. A good method learns quickly and does not waste many tries on bad choices.

## Definition

**Environment.** A finite or infinite MDP $(S, A, P, R, \gamma)$. The agent knows $S$, $A$ and $\gamma$, but not $P$ or $R$.

**Access.** One of three settings.

- *Online.* The agent is in state $s_t$, chooses $a_t$, and the environment returns $r_{t+1}$ and $s_{t+1} \sim P(\cdot \mid s_t, a_t)$. Episodes may restart from a start distribution.
- *Generative model.* The agent may ask for a sample next state and reward for any pair $(s, a)$ that it chooses.
- *Offline.* The agent gets a fixed data set of transitions and cannot collect more.

**Goal.** A policy $\pi$ with $V^\pi$ close to $V^*$. Different measures of success are used:

- *Asymptotic*: the learned action values converge to $Q^*$, so the greedy policy is eventually optimal.
- *Sample complexity*: the number of samples, or of steps on which the agent acts more than $\varepsilon$ worse than optimal, is bounded with probability at least $1 - \delta$ (the PAC-MDP criterion).
- *Regret*: the total reward lost, compared with an optimal policy, over $T$ steps of online interaction is small.

## Variants

- **Episodic or continuing.** Tasks may end in terminal states, or go on forever with discounting or with the average reward criterion.
- **Tabular or approximate.** With few states, a table holds one value per state-action pair. With many states, the values or the policy are parametric functions, for example neural networks, as in [DQN](/dqn/).
- **On-policy or off-policy.** The agent learns the values of the policy that it follows, as in [SARSA](/sarsa/), or of another policy, usually the greedy one, as in [Q-learning](/q-learning/).
- **Bandits.** With a single state the problem is the [multi-armed bandit](/multi-armed-bandit/), which isolates the [exploration and exploitation trade-off](/exploration-exploitation-tradeoff/).
- **Offline.** Learning from a fixed data set is [offline reinforcement learning](/offline-reinforcement-learning/).
- **Partial observation and several agents.** See [POMDP](/pomdp/) and [Markov game](/markov-game/).

## Examples

- **Gridworld with unknown slips.** An agent on a grid learns where the walls and the goal are and how often its moves slip, and learns a shortest safe route. See the example of [Dyna-Q](/dyna-q/).
- **Games.** Backgammon, Atari games, Go and chess have been learned by self-play or play against an emulator; [MuZero](/muzero/) learns its own model for planning.
- **Control.** Balancing a pole, robot locomotion and the control of cooling in data centers.

## Known algorithms

| family | methods | idea |
| --- | --- | --- |
| Monte Carlo | [Monte Carlo control](/monte-carlo-control/) | average complete returns, then act greedily |
| temporal difference, value based | [Q-learning](/q-learning/), [SARSA](/sarsa/), [expected SARSA](/expected-sarsa/), [double Q-learning](/double-q-learning/) | bootstrap from the next estimate after each step |
| deep value based | [DQN](/dqn/), [double DQN](/double-dqn/), [dueling network](/dueling-network/) | Q-learning with a neural network and [experience replay](/experience-replay/) |
| policy gradient | [REINFORCE](/reinforce/), [natural policy gradient](/natural-policy-gradient/), [TRPO](/trpo/), [PPO](/ppo/) | follow the gradient of the expected return, by the [policy gradient theorem](/policy-gradient-theorem/) |
| actor-critic | [actor-critic](/actor-critic/), [A2C](/a2c/), [DDPG](/ddpg/), [SAC](/soft-actor-critic/) | a learned critic gives the policy gradient a lower variance |
| model based | [model-based RL](/model-based-reinforcement-learning/), [Dyna-Q](/dyna-q/), [prioritized sweeping](/prioritized-sweeping/), [MuZero](/muzero/) | learn a model, then plan with it |
| offline | [conservative Q-learning](/conservative-q-learning/) | stay close to the actions in the data set |

## Bounds

**Asymptotic convergence.** Tabular Q-learning converges to $Q^*$ with probability 1 if every state-action pair is tried infinitely often and the step sizes satisfy the [Robbins-Monro conditions](/robbins-monro-conditions/) (Watkins and Dayan 1992). See [convergence of tabular Q-learning](/tabular-q-learning-convergence/).

**Sample complexity.** Exploration methods such as R-max and E3 learn an $\varepsilon$-optimal policy after a number of steps that is polynomial in $|S|$, $|A|$, $1/\varepsilon$, $\log(1/\delta)$ and $1/(1-\gamma)$; see [model-based RL](/model-based-reinforcement-learning/). With a generative model, a number of samples of order $|S||A|/((1-\gamma)^3\varepsilon^2)$, up to logarithmic factors, is necessary and sufficient to estimate $Q^*$ to accuracy $\varepsilon$ (Azar, Munos and Kappen 2013).

**Regret.** For communicating MDPs under the average reward criterion, UCRL2 has regret of order $D|S|\sqrt{|A|T}$ up to logarithmic factors after $T$ steps, where $D$ is the diameter, and every algorithm has regret at least of order $\sqrt{D|S||A|T}$ on some MDP (Jaksch, Ortner and Auer 2010).

**Function approximation.** With function approximation, off-policy learning and bootstrapping together, value based methods can diverge. This is the [deadly triad](/deadly-triad/).

## Reductions

- **To planning.** If the model is learned to a good accuracy, planning on the learned model gives a good policy. This is certainty equivalence, the basis of [model-based RL](/model-based-reinforcement-learning/).
- **To prediction.** Generalized policy iteration alternates [policy evaluation](/policy-evaluation/) from samples with greedy improvement, as in Monte Carlo control and SARSA.
- **From bandits.** A bandit is an MDP with one state, so lower bounds for bandits are lower bounds for control.

## Applications

Game playing, robot control, recommendation and advertising with long-term effects, the control of industrial systems, and the fine tuning of large language models from human feedback with [PPO](/ppo/).

## References
