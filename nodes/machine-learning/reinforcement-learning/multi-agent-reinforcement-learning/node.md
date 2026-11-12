---
tag: 9P60Q6
kind: concept
slug: multi-agent-reinforcement-learning
name: Multi-agent reinforcement learning
aliases:
- MARL
- multiagent reinforcement learning
area: machine-learning/reinforcement-learning
level: research
summary: "Reinforcement learning with several agents that act in one environment. Each agent's world contains the others, who also learn, so the single-agent theory breaks and equilibria replace optima."
prereqs: [markov-game, q-learning]
see_also: [minimax-q, nash-equilibrium, zero-sum-game, follow-the-leader, regret, multiplicative-weights-update, counterfactual-regret-minimization, actor-critic]
sources:
  - paper: "Michael L. Littman, Markov games as a framework for multi-agent reinforcement learning, Proceedings of the 11th International Conference on Machine Learning (ICML), 1994, pages 157 to 163"
    locator: Markov games as the model of multi-agent reinforcement learning, and minimax-Q
  - paper: doi:10.1109/TSMCC.2007.913919
    title: "Lucian Busoniu, Robert Babuska and Bart De Schutter, A comprehensive survey of multiagent reinforcement learning, IEEE Transactions on Systems, Man, and Cybernetics, Part C 38(2), 2008, pages 156 to 172"
    locator: the classification into fully cooperative, fully competitive and mixed tasks, the goals of stability and adaptation, and the algorithms of each class
  - paper: "Junling Hu and Michael P. Wellman, Nash Q-learning for general-sum stochastic games, Journal of Machine Learning Research 4, 2003, pages 1039 to 1069"
    locator: Nash-Q and the conditions on the stage games for its convergence
  - paper: "Caroline Claus and Craig Boutilier, The dynamics of reinforcement learning in cooperative multiagent systems, Proceedings of the Fifteenth National Conference on Artificial Intelligence (AAAI), 1998, pages 746 to 752"
    locator: independent learners and joint action learners, and the climbing game
  - paper: "Ming Tan, Multi-agent reinforcement learning, independent vs. cooperative agents, Proceedings of the 10th International Conference on Machine Learning (ICML), 1993, pages 330 to 337"
    locator: independent Q-learners, and the gains from sharing sensations, episodes and policies
  - paper: doi:10.1016/j.artint.2006.02.006
    title: "Yoav Shoham, Rob Powers and Trond Grenager, If multi-agent learning is the answer, what is the question?, Artificial Intelligence 171(7), 2007, pages 365 to 377"
    locator: the different goals of multi-agent learning research
  - paper: doi:10.1287/moor.27.4.819.297
    title: "Daniel S. Bernstein, Robert Givan, Neil Immerman and Shlomo Zilberstein, The complexity of decentralized control of Markov decision processes, Mathematics of Operations Research 27(4), 2002, pages 819 to 840"
    locator: finite-horizon Dec-POMDPs are NEXP-complete
---

## In plain words

Several agents act in the same world at the same time: robots in a warehouse, cars at a crossing, players in a game. Each one learns from its own rewards, as in ordinary reinforcement learning. But the best thing for one agent to do depends on what the others do, and the others are learning and changing too. So the world that one agent sees keeps shifting under it. There may be no single best way to act, only ways that are stable because no agent wants to change alone. Agents may share one goal, have opposite goals, or something in between, and each case needs different methods.

## The idea

**The model.** The standard model is the [Markov game](/markov-game/) (Shapley's stochastic game, made the base model of the field by Littman, 1994): $N$ agents see the state $s$, choose actions $a^1, \dots, a^N$ at the same time, each gets its own reward $R^k(s, a^1, \dots, a^N)$, and the state moves by $P(\cdot \mid s, a^1, \dots, a^N)$. With one agent this is a [Markov decision process](/markov-decision-process/). When the agents see only private observations, the model is a partially observable stochastic game, or a decentralized POMDP (Dec-POMDP) when all share one reward; planning in a finite-horizon Dec-POMDP is NEXP-complete (Bernstein and others, 2002), far above the PSPACE of a single-agent [POMDP](/pomdp/).

**Three kinds of task** (Busoniu, Babuska and De Schutter, 2008):

| task | rewards | solution concept | typical methods |
|---|---|---|---|
| fully cooperative | one shared reward | a jointly optimal policy, and coordination on one of them | joint-action learners, value decomposition, centralized critics |
| fully competitive | two players, $R^2 = -R^1$ | the game value and minimax strategies | [minimax-Q](/minimax-q/), self-play, [counterfactual regret minimization](/counterfactual-regret-minimization/) |
| mixed (general-sum) | arbitrary | [Nash equilibrium](/nash-equilibrium/), correlated equilibrium | Nash-Q, friend-or-foe Q, correlated-Q, no-regret learning, opponent modeling |

**Why it is harder than one agent.**

- *Non-stationarity.* From one agent's view, the other agents are part of the environment. While they learn, its transition and reward laws change, so the Markov property fails and the convergence theorems of [Q-learning](/q-learning/) no longer apply. Old samples in an [experience replay](/experience-replay/) buffer describe opponents that no longer exist.
- *No single optimum.* In a [zero-sum game](/zero-sum-game/) there is a value, and a minimax policy guarantees it. In a general-sum game different equilibria give different payoffs, and agents that learn separately may not reach the same one.
- *Coordination.* Even with one shared reward, there can be several optimal joint actions, and agents that pick their parts separately can mismatch.
- *Credit assignment.* With a shared reward, an agent cannot tell how much of it came from its own action.
- *Scale.* The joint action space has $\prod_k |A^k|$ elements, exponential in $N$.
- *Computation.* Computing a Nash equilibrium of a general-sum game is PPAD-complete even for two players (Chen, Deng and Teng; Daskalakis, Goldberg and Papadimitriou), so an algorithm that converges to Nash equilibria fast in all games is unlikely.

**Families of methods.**

- *Independent learners* (Tan, 1993): each agent runs a single-agent method and ignores the others. Simple and often good in practice, with no general guarantee.
- *Joint-action learners* (Claus and Boutilier, 1998): learn $Q(s, a^1, \dots, a^N)$ and a model of the others' policies.
- *Equilibrium-based value learning:* replace the max of Q-learning by a solution of the stage game: the minimax value (minimax-Q), a Nash equilibrium (Nash-Q, Hu and Wellman, 2003), or a correlated equilibrium (correlated-Q).
- *Best-response and no-regret dynamics:* fictitious play, a form of [follow the leader](/follow-the-leader/), plays a best response to the empirical mix of the others' past actions. No-regret learners such as [multiplicative weights](/multiplicative-weights-update/) make the average joint play approach the set of coarse correlated equilibria, and in two-player zero-sum games the average strategies approach minimax strategies; see [regret](/regret/).
- *Policy gradient with varying step sizes:* WoLF ("win or learn fast", Bowling and Veloso, 2002) learns slowly when winning and fast when losing, to make gradient play converge.
- *Centralized training, decentralized execution:* during training a critic sees all agents' observations and actions (MADDPG, COMA), or the joint value is a sum or a monotone mix of per-agent values (VDN, QMIX); at run time each agent acts on its own observations. These are [actor-critic](/actor-critic/) and value methods with a shared critic.
- *Self-play and population training:* an agent plays against copies or past versions of itself, as in TD-Gammon, AlphaZero and the league training of AlphaStar.

## Examples

**The climbing game** (Claus and Boutilier, 1998). Two agents share the reward of this matrix, row for agent 1 and column for agent 2:

$$\begin{pmatrix} 11 & -30 & 0 \\ -30 & 7 & 6 \\ 0 & 0 & 5 \end{pmatrix}.$$

The best joint action is (1, 1) with 11. An independent learner whose partner explores uniformly at random sees the average rewards $-19/3$, $-17/3$ and $5/3$ for its three actions, so both drift to action 3 and get 5. The high penalties next to the optimum hide it from agents that do not model each other.

**Gradient play in matching pennies.** Let $p$ and $q$ be the probabilities of the first action of the two players, and let the row player get $u(p, q) = (2p - 1)(2q - 1)$, the column player $-u$. If each follows the gradient of its own payoff, $\dot p = 2(2q - 1)$ and $\dot q = -2(2p - 1)$. Then

$$\frac{d}{dt}\big[(2p - 1)^2 + (2q - 1)^2\big] = 8(2p - 1)(2q - 1) - 8(2q - 1)(2p - 1) = 0,$$

so the strategies circle the equilibrium $(1/2, 1/2)$ for ever, and with discrete steps they spiral outward. Each agent's learning is correct for a fixed opponent; together they never settle. Fictitious play in the same game also cycles in its actual play, but the empirical frequencies converge to $(1/2, 1/2)$ (Robinson, 1951).

**Exploitation of a fixed best response.** In the two-state game of the [minimax-Q](/minimax-q/) page, a Q-learner trained against a uniformly random opponent learns a deterministic policy worth $(12.25, 12.75)$ against that opponent. A second learner that adapts to it holds it to about $(2.41, 3.79)$, while minimax-Q's mixed policy guarantees the game value $(7.25, 7.75)$ against any opponent.

## Where it is used

- **Games:** backgammon, Go and chess by self-play; StarCraft II (AlphaStar), Dota 2 (OpenAI Five), and poker, where counterfactual regret minimization computes strategies for imperfect information.
- **Robotics and control:** teams of robots and drones, warehouse fleets, and traffic signal control across many crossings.
- **Autonomous driving:** other road users are agents whose behavior responds to the car's.
- **Economics and networks:** auctions, markets, and resource sharing in communication networks, where the agents' interests conflict.
- **Training by competition:** self-play and population training produce opponents and curricula for single agents.

## References
