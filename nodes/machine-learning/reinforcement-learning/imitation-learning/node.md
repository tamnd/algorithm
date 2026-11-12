---
tag: RZA6XG
kind: problem
slug: imitation-learning
name: Imitation learning
aliases:
- learning from demonstrations
area: machine-learning/reinforcement-learning
level: advanced
summary: "Learn a policy as good as an expert's from its demonstrations or answers, with no reward; the core difficulty is that the learner's mistakes lead to states the expert never showed."
prereqs: [markov-decision-process, classification]
see_also: [dagger, inverse-reinforcement-learning, offline-reinforcement-learning, regression, empirical-risk-minimization, structured-prediction, reward-function, policy]
sources:
  - paper: "Dean A. Pomerleau, ALVINN, an autonomous land vehicle in a neural network, Advances in Neural Information Processing Systems 1 (NIPS 1988), 1989, pages 305 to 313"
    locator: steering a vehicle by a network trained on a human driver's camera images and steering commands
  - paper: "Stephane Ross and J. Andrew Bagnell, Efficient reductions for imitation learning, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (AISTATS), 2010, pages 661 to 668"
    locator: the T squared epsilon bound for behavior cloning, forward training and SMILe
  - paper: "Stephane Ross, Geoffrey J. Gordon and J. Andrew Bagnell, A reduction of imitation learning and structured prediction to no-regret online learning, AISTATS 2011, pages 627 to 635, arXiv:1011.0686"
    locator: Section 2 (problem setting and the two bounds), Section 3 (DAgger)
  - paper: doi:10.1145/1015330.1015430
    title: "Pieter Abbeel and Andrew Y. Ng, Apprenticeship learning via inverse reinforcement learning, Proceedings of the 21st International Conference on Machine Learning (ICML), 2004"
    locator: matching feature expectations, and the bound on the performance of the learned policy for every reward linear in the features
  - paper: "Jonathan Ho and Stefano Ermon, Generative adversarial imitation learning, Advances in Neural Information Processing Systems 29 (NIPS 2016), pages 4565 to 4573, arXiv:1606.03476"
    locator: imitation as matching occupancy measures, and GAIL
  - paper: "Nived Rajaraman, Lin F. Yang, Jiantao Jiao and Kannan Ramchandran, Toward the fundamental limits of imitation learning, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2009.05990"
    locator: the tabular bounds for behavior cloning with N expert trajectories
  - paper: doi:10.1561/2300000053
    title: "Takayuki Osa, Joni Pajarinen, Gerhard Neumann, J. Andrew Bagnell, Pieter Abbeel and Jan Peters, An algorithmic perspective on imitation learning, Foundations and Trends in Robotics 7(1-2), 2018, pages 1 to 179"
    locator: survey of behavior cloning and inverse reinforcement learning
---

Imitation learning is the problem of learning to act from an expert, not from a reward. The learner sees what the expert does (recorded demonstrations, or answers to questions) in a [Markov decision process](/markov-decision-process/) whose [reward](/reward-function/) is not given, and must output a [policy](/policy/) that does about as well as the expert under the unknown reward. It is used when good behavior is easy to show but hard to write as a reward: driving, flying, grasping, and playing games. The simplest method treats it as [classification](/classification/), but the learner's own mistakes take it to states that the data does not cover, and this makes the problem harder than plain supervised learning.

## In plain words

You learn a task by watching someone who is good at it. You write down what they do in each situation and copy it. This works while you stay in situations that they showed you. After your first small mistake you may be in a situation they never were in, and then you have no example to copy, so you make more mistakes.

Methods differ in how they fix this: they ask the expert about your own situations, or they find the goal behind the expert's choices and plan for that goal.

## Definition

**Input.** A Markov decision process without its reward, $(S, A, P, s_1, T)$ with horizon $T$ (or a discount $\gamma$), and access to an expert policy $\pi_E$ in one of two forms:

- *Demonstrations:* a fixed set of $N$ trajectories $(s_1, a_1, s_2, a_2, \dots)$ of $\pi_E$.
- *Interaction:* the learner may run its own policies in the environment and ask for $\pi_E(s)$ in any state it visits.

**Output.** A policy $\pi$.

**Goal.** For the expert's unknown cost $C \in [0, 1]$ (or for every cost in a known class $\mathcal{C}$), make the gap

$$J_C(\pi) - J_C(\pi_E), \qquad J_C(\pi) = \mathbb{E}_\pi\Big[\sum_{t=1}^{T} C(s_t, a_t)\Big],$$

small. A common surrogate is the loss $\ell(s, \pi) = \Pr[\pi(s) \ne \pi_E(s)]$, measured either on the expert's state distribution $d_{\pi_E}$ (error $\varepsilon$) or on the learner's own distribution $d_\pi$ (error $\varepsilon_\pi$).

## Variants

- **Behavior cloning:** demonstrations only, no interaction, no knowledge of $P$.
- **Interactive imitation:** the expert labels states that the learner reaches ([DAgger](/dagger/)); or the expert gives its cost-to-go of each action (AggreVaTe).
- **Inverse reinforcement learning:** recover a reward that explains the demonstrations, then plan for it; see [inverse reinforcement learning](/inverse-reinforcement-learning/). Apprenticeship learning asks only for a policy that is as good as the expert for every reward in a linear class.
- **Distribution matching:** find a policy whose state-action occupancy measure is close to the expert's, for example in Jensen-Shannon divergence (GAIL).
- **Learning from observation:** the demonstrations show states but not actions, as in video.
- **Suboptimal or mixed demonstrations:** the data mixes good and bad behavior. This shades into [offline reinforcement learning](/offline-reinforcement-learning/) when rewards are also logged.

## Examples

- **Steering.** ALVINN (Pomerleau, 1989) mapped camera images to steering angles, trained on a human driver. The network did not learn to recover when the vehicle drifted off center, because the driver never showed such states; Pomerleau added synthetic shifted images with corrected labels.
- **The windy lane** on the [DAgger](/dagger/) page: the expert never leaves the center, so behavior cloning sees only one state. With an error of 0.067 on the expert's states, its cost over 40 steps is 15.97, while two rounds of DAgger reach the best possible cost of 0.695.
- **Structured prediction.** Tagging a sentence word by word, where each tag depends on the earlier predicted tags, is imitation of an expert that knows the correct tags; see [structured prediction](/structured-prediction/).

## Known algorithms

| method | needs | guarantee in terms of |
|---|---|---|
| behavior cloning: [empirical risk minimization](/empirical-risk-minimization/) on the pairs $(s, a)$, by [classification](/classification/) for discrete actions or [regression](/regression/) for continuous ones | demonstrations | $T^2 \varepsilon$ |
| forward training (Ross and Bagnell, 2010): one policy per time step, trained on states of the earlier policies | interaction | $uT\varepsilon$, but $T$ policies |
| SEARN, SMILe: iterative stochastic mixing of policies | interaction | $uT\varepsilon$ up to extra terms |
| [DAgger](/dagger/): aggregate expert labels on the learner's states, retrain | interaction | $uT(\varepsilon_N + \text{regret})$ |
| AggreVaTe: as DAgger, with cost-to-go labels | interaction with cost-to-go | the regret of a cost-sensitive learner |
| apprenticeship learning (Abbeel and Ng, 2004): match feature expectations by repeated [inverse reinforcement learning](/inverse-reinforcement-learning/) and planning | demonstrations and a planner | for every reward linear in the features |
| game-theoretic apprenticeship (Syed and Schapire, 2007): [multiplicative weights](/multiplicative-weights-update/) over reward features | demonstrations and a planner | can beat the expert when the reward signs are known |
| maximum entropy IRL, then planning | demonstrations and a planner | matches feature counts |
| GAIL (Ho and Ermon, 2016): a discriminator gives the reward for a policy-gradient learner | demonstrations and interaction without labels | occupancy measure matching |

## Bounds

- **Behavior cloning compounds.** If $\varepsilon$ is the error on the expert's states, then $J(\pi) \le J(\pi_E) + T^2\varepsilon$ (Ross and Bagnell, 2010), and there are instances where the cost really grows as $T^2\varepsilon$ (Kääriäinen, 2006). Plain supervised learning would suggest $T\varepsilon$.
- **Errors on the learner's own states do not compound.** If one wrong action raises the expert's cost-to-go by at most $u$, then $J(\pi) \le J(\pi_E) + uT\varepsilon_\pi$. Interactive methods such as DAgger make $\varepsilon_\pi$ small, so their bound is linear in $T$. Both bounds are proved on the [DAgger proof page](/dagger/).
- **Sample complexity without interaction.** In the tabular case with a deterministic expert and $N$ expert trajectories, behavior cloning has an expected gap of order $|S| T^2 / N$ up to log factors, and Rajaraman and others (2020) show that no method without interaction can do better in the worst case.
- **Feature matching.** Let the reward be $w^\top \phi(s)$ for features $\phi$ and an unknown $w$ with $\|w\|_2 \le 1$, and let $\mu(\pi) = \mathbb{E}_\pi[\sum_t \gamma^t \phi(s_t)]$ be the discounted feature expectations. Then the return of $\pi$ is $w^\top \mu(\pi)$, so any policy with $\|\mu(\pi) - \mu(\pi_E)\|_2 \le \epsilon$ has a gap at most $\epsilon$ for every such reward, by the Cauchy-Schwarz inequality (Abbeel and Ng, 2004).

## Reductions

- **To classification.** Behavior cloning reduces imitation to supervised learning, with the $T^2$ loss of the first bound.
- **To no-regret online learning.** DAgger reduces imitation to online learning; any learner with average regret $\gamma_N$ gives the linear bound with the extra term $\gamma_N$.
- **To reinforcement learning.** Inverse reinforcement learning and GAIL reduce imitation to a sequence of [control problems](/rl-control/) with learned rewards.
- **From offline reinforcement learning.** When the logged data comes from an expert, offline RL with pessimism behaves like behavior cloning; Rashidinejad and others (2021) study both in one framework of data coverage.

## Applications

Autonomous driving and flight, robot manipulation from teleoperated or kinesthetic demonstrations, character animation from motion capture, game agents trained on human play, distilling slow planners or search into fast policies, and training sequence models for structured prediction.

## References
