---
tag: 2ZBR0P
kind: algorithm
slug: actor-critic
name: Actor-critic
aliases:
- actor-critic methods
- one-step actor-critic
area: machine-learning/reinforcement-learning
level: core
summary: "Policy gradient where a learned critic V_w supplies the TD error delta = R + gamma V_w(S') - V_w(S), which replaces the Monte Carlo return in the update of the actor pi_theta."
solves: [rl-control]
model: real-ram
complexity:
  vars: {N: the number of time steps, W: the cost of one evaluation of the actor and the critic with their gradients, d: the number of actor and critic parameters}
  time: {worst: "O(N W)"}
  space: {extra: "O(d)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1983
  people: [Andrew G. Barto, Richard S. Sutton, Charles W. Anderson]
  note: "Barto, Sutton and Anderson balanced a pole on a cart with an associative search element (the actor) trained by the internal reinforcement of an adaptive critic element (the critic)."
prereqs: [reinforce, td-error, policy-gradient-theorem]
see_also: [a2c, a3c, generalized-advantage-estimation, natural-policy-gradient, ddpg, soft-actor-critic, stochastic-approximation, advantage-function]
sources:
  - paper: "Andrew G. Barto, Richard S. Sutton and Charles W. Anderson, Neuronlike adaptive elements that can solve difficult learning control problems, IEEE Transactions on Systems, Man, and Cybernetics SMC-13(5), 1983, pages 834 to 846"
    locator: the associative search element and the adaptive critic element, and the pole balancing experiments
  - paper: "Vijay R. Konda and John N. Tsitsiklis, Actor-critic algorithms, Advances in Neural Information Processing Systems 12, 2000, pages 1008 to 1014"
    locator: the two time scale actor-critic with a linear critic on the compatible features, and its convergence result
  - paper: "Vijay R. Konda and John N. Tsitsiklis, On actor-critic algorithms, SIAM Journal on Control and Optimization 42(4), 2003, pages 1143 to 1166"
    locator: the full convergence analysis (TD(1) and TD(lambda) critics, average reward)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 13.5 (actor-critic methods, the one-step actor-critic box) and Section 13.6 (the continuing case)
  - paper: "Richard S. Sutton, David McAllester, Satinder Singh and Yishay Mansour, Policy gradient methods for reinforcement learning with function approximation, Advances in Neural Information Processing Systems 12, 2000, pages 1057 to 1063"
    locator: Theorem 2 (compatible function approximation) and Theorem 3 (convergence of policy iteration with function approximation)
  - paper: doi:10.1016/j.automatica.2009.07.008
    title: "Shalabh Bhatnagar, Richard S. Sutton, Mohammad Ghavamzadeh and Mark Lee, Natural actor-critic algorithms, Automatica 45(11), 2009, pages 2471 to 2482"
    locator: the TD(0) actor-critic algorithms and their two time scale convergence proofs
---

An actor-critic method learns two things at once: a policy $\pi_\theta$, the *actor*, and a value function $V_w$, the *critic*. After each step $(S, A, R, S')$ the critic computes the [TD error](/td-error/) $\delta = R + \gamma V_w(S') - V_w(S)$. The critic moves $V_w(S)$ toward the target by TD learning, and the actor moves along $\delta\, \nabla_\theta \log \pi_\theta(A \mid S)$: an action that turned out better than the critic expected becomes more likely. Compared with [REINFORCE](/reinforce/), the one-step TD error replaces the return of the whole episode, so the method can learn online, step by step, with much lower variance. The price is bias: the update is the true policy gradient only when the critic equals $V^{\pi}$. The idea goes back to the adaptive critic of Barto, Sutton and Anderson (1983); Konda and Tsitsiklis (2000) proved convergence for critics that learn on a faster time scale than the actor.

## In plain words

The agent has two parts. The actor chooses actions. The critic watches and predicts how much reward will still come from each situation. After every move, the critic compares what happened (the reward plus its prediction for the new situation) with what it predicted before the move. The difference is a surprise. A good surprise tells the actor to make that move more likely; a bad surprise tells it to make that move less likely. The critic also uses the surprise to correct its own prediction. The actor does not wait for the end of the episode, so it can learn during long or never-ending tasks. If the critic is wrong, its advice is slightly wrong too.

## The problem

The setting is [reinforcement learning control](/rl-control/) in a [Markov decision process](/markov-decision-process/) with start distribution $\mu$ and discount $\gamma$. The agent samples transitions and does not know the model. The actor $\pi_\theta(a \mid s)$ is differentiable in $\theta$ and gives every action positive probability. The objective is $J(\theta) = \sum_s \mu(s) V^{\pi_\theta}(s)$, the expected discounted return from the start, as in [REINFORCE](/reinforce/). The critic is a parametric [state-value function](/state-value-function/) $V_w$, for example linear, $V_w(s) = w^\top \phi(s)$, with $V_w = 0$ at the end of an episode.

## The algorithm

This is the one-step actor-critic for episodic tasks, as in Sutton and Barto (Section 13.5). Notation: $\eta_\theta$ and $\eta_w$ are the step sizes of the actor and the critic, and $I$ is the running factor $\gamma^t$.

```pseudo id=main
ACTOR-CRITIC(env, π_θ, V_w, γ, η_θ, η_w)
L1  for each episode do
L2      S ← S_0 ~ μ; I ← 1
L3      while the episode has not ended do
L4          A ~ π_θ(· | S); take A, observe R and S′
L5          δ ← R + γ V_w(S′) − V_w(S)                ▷ V_w(S′) = 0 if the episode ended
L6          w ← w + η_w δ ∇_w V_w(S)
L7          θ ← θ + η_θ I δ ∇_θ log π_θ(A | S)
L8          I ← γ I; S ← S′
```

Line L5 is the TD error. Line L6 is the semi-gradient TD(0) update of the critic: the target $R + \gamma V_w(S')$ is treated as a constant. Line L7 is the actor update. The term $-V_w(S)$ in $\delta$ acts as a baseline, as in [REINFORCE](/reinforce/) with baseline, and the term $R + \gamma V_w(S')$ is a one-step estimate of $Q^{\pi}(S, A)$. The factor $I = \gamma^t$ comes from the [policy gradient theorem](/policy-gradient-theorem/), like the factor $\gamma^t$ in REINFORCE. For continuing tasks under the average reward criterion, $\delta = R - \bar R + V_w(S') - V_w(S)$ with a running estimate $\bar R$ of the average reward, and $I$ is dropped.

For the tabular softmax actor, $\partial \log \pi_\theta(a \mid s) / \partial \theta_{s,b} = \mathbf{1}[a = b] - \pi_\theta(b \mid s)$.

## Example

Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page with $\gamma = \tfrac12$, the uniform softmax actor ($\theta = 0$) and a tabular critic that already holds the true values $V^\pi = (\tfrac{28}{27}, \tfrac{44}{27})$. The actor step size is $\eta_\theta = 1$ and the critic step size is 0, so that the steps show the actor update alone.

| step | transition | $I$ | $\delta$ | actor change |
|---|---|---|---|---|
| 1 | state 0, action 0, reward 1, to state 1 | 1 | $1 + \tfrac12 \cdot \tfrac{44}{27} - \tfrac{28}{27} = \tfrac79$ | $\theta_0 \mathrel{+}= \tfrac79 (\tfrac12, -\tfrac12) = (\tfrac{7}{18}, -\tfrac{7}{18})$ |
| 2 | state 1, action 1, reward 3, end | $\tfrac12$ | $3 - \tfrac{44}{27} = \tfrac{37}{27}$ | $\theta_1 \mathrel{+}= \tfrac12 \cdot \tfrac{37}{27} (-\tfrac12, \tfrac12) = (-\tfrac{37}{108}, \tfrac{37}{108})$ |

REINFORCE with the same baseline changes $\theta_0$ by $(\tfrac{79}{108}, -\tfrac{79}{108})$ on this episode, because it uses the full return $\tfrac52$ in place of $1 + \tfrac12 V^\pi(1)$. In state 0, action 0 has the advantage $Q^\pi(0, 0) - V^\pi(0) = \tfrac{79}{54} - \tfrac{28}{27} = \tfrac{23}{54}$, which is the mean of $\delta$ over the next state. With the exact critic, the mean of the actor change over all episodes is the exact gradient $\nabla J$, for every MDP in which episodes end (proved below).

**Learning.** With both parts learning ($\eta_\theta = 0.5$, $\eta_w = 0.1$, critic starting at 0, start state 0), the actor of the implementation below reaches $\pi(0 \mid 0) > 0.99$ and $\pi(1 \mid 1) > 0.99$ within 300 episodes. This is the optimal policy, with $V^* = (\tfrac{11}{6}, 3)$, and the critic value of state 1 is then close to 3.

## Correctness

The proof is in the correctness proof below. Fix $\theta$ and the critic $w$, and let $e = V_w - V^{\pi_\theta}$ be the error of the critic. If episodes end with probability 1 and either $\gamma < 1$ with bounded rewards, or the MDP has no cycles, the mean of the summed actor updates of line L7 over an episode (with $\eta_\theta = 1$ and $\theta$ frozen) is

$$\mathbb{E}\Big[\sum_t \gamma^t \delta_t \nabla \log \pi_\theta(A_t \mid S_t)\Big] = \nabla J(\theta) + \gamma \sum_s d(s) \sum_a \nabla \pi_\theta(a \mid s) \sum_{s'} P(s' \mid s, a)\, e(s'),$$

where $d(s) = \sum_t \gamma^t \Pr(S_t = s)$. So with an exact critic ($e = 0$) the update is unbiased. An error in $V_w(S)$ does not cause bias, because that term is a baseline; only the error in the bootstrap value $V_w(S')$ does. Sutton et al. (2000) give conditions on the critic, *compatible* features with $\nabla_w Q_w(s, a) = \nabla_\theta \log \pi_\theta(a \mid s)$ and a critic that minimizes the squared error, under which an approximate critic still gives the exact gradient.

For the online algorithm, in which $\theta$ and $w$ change at every step, the standard result is a two time scale argument. If the actor step sizes are much smaller than those of the critic ($\eta_\theta / \eta_w \to 0$, both satisfying the [Robbins-Monro conditions](/robbins-monro-conditions/)), the critic sees an almost fixed policy and tracks its TD fixed point, and the actor follows an approximate gradient. Konda and Tsitsiklis (2000, 2003) proved for the average reward setting that, with a linear critic whose features span the compatible features, $\liminf_k \lVert \nabla J(\theta_k) \rVert = 0$ with probability 1 for a TD(1) critic, and that it is at most a bias term that vanishes as $\lambda \to 1$ for a TD($\lambda$) critic. Bhatnagar et al. (2009) proved convergence to a neighbourhood of the local maxima for TD(0) critics.

## Complexity

Each time step does one forward and backward pass of the actor and of the critic: $O(W)$ work, $O(|A| + F)$ for a tabular softmax actor and a linear critic with $F$ features. So $N$ steps cost $O(N W)$ in the worst case. Memory is $O(d)$ for the parameters; unlike [REINFORCE](/reinforce/), nothing about the episode is stored. The number of steps to reach a good policy has no general bound; it depends on the step sizes, the quality of the critic and the mixing of the MDP.

## Properties

- **Online and incremental.** Each step updates both parts with $O(W)$ work, so it applies to continuing tasks.
- **On-policy.** The TD error must come from the current policy; off-policy actor-critics need importance weights ([V-trace](/v-trace/)) or a Q-critic ([DDPG](/ddpg/), [soft actor-critic](/soft-actor-critic/)).
- **Biased, lower variance.** The one-step target has much less variance than the return, but an inexact critic adds bias.
- **Two time scales.** The analysis needs the critic to learn faster than the actor.
- **Randomized.** Action selection and the environment use random numbers.

## Variants and improvements

- **Multi-step and eligibility traces.** Use the $n$-step or $\lambda$-return in $\delta$, or traces for both the actor and the critic (Sutton and Barto, Section 13.5). [Generalized advantage estimation](/generalized-advantage-estimation/) is the $\lambda$-weighted version used in deep RL.
- **Synchronous batches.** [A2C](/a2c/) collects $n$-step segments from several copies of the environment and updates on the batch.
- **Asynchronous workers.** [A3C](/a3c/) runs many actor-learners that update shared parameters without locks.
- **Natural actor-critic.** Precondition the actor update by the inverse Fisher matrix; with compatible features the natural gradient is the weight vector of the critic ([natural policy gradient](/natural-policy-gradient/)).
- **Trust regions.** [TRPO](/trpo/) and [PPO](/ppo/) restrict how far each actor update can move the policy.
- **Q-critics and continuous actions.** [DDPG](/ddpg/), [TD3](/td3/) and [soft actor-critic](/soft-actor-critic/) learn $Q_w(s, a)$ from replayed data and update a deterministic or reparameterized actor through it.

## When to use it

Use an actor-critic method when you need a stochastic or continuous policy, when episodes are long or never end, or when REINFORCE is too noisy. The one-step tabular form is useful for small problems and teaching; for large problems use one of its descendants, [A2C](/a2c/) or [PPO](/ppo/) with on-policy data, or [soft actor-critic](/soft-actor-critic/) or [TD3](/td3/) when replayed off-policy data is cheaper than new samples. If the action set is small and discrete and a value-based method works, [Q-learning](/q-learning/) or [DQN](/dqn/) is simpler.

## Pitfalls

- **Critic too slow.** If the actor learns as fast as the critic, it follows the errors of the critic and can collapse to a poor deterministic policy. Use a larger critic step size or several critic updates per actor update.
- **The end of an episode.** $V_w(S')$ must be 0 when the episode really ends, and must not be 0 when it is only cut by a time limit.
- **Dropping $I$.** Without $I = \gamma^t$ the episodic update is not the gradient of the discounted objective. Most deep RL code drops it on purpose and optimizes a different, undiscounted state weighting.
- **Gradients into the target.** The critic target $R + \gamma V_w(S')$ must be a constant in line L6; the full gradient of the squared TD error gives the residual gradient method, which has a different fixed point.
- **Shared networks.** When the actor and the critic share layers, the scales of the two losses must be balanced.

## Implementations

## History

Barto, Sutton and Anderson (1983) introduced the actor-critic architecture: an associative search element chose actions, and an adaptive critic element turned the external reward into an internal TD-like reinforcement signal; together they learned to balance a pole on a cart. Sutton's thesis (1984) studied the critic, which led to TD learning. The modern policy gradient view came with Sutton et al. (2000), whose compatible function approximation theorem gave the conditions under which a critic does not bias the actor, and with Konda and Tsitsiklis (2000), who proved convergence of two time scale actor-critics with linear critics. Natural actor-critics (Peters and Schaal; Bhatnagar et al., 2009) and the asynchronous and synchronous deep versions [A3C](/a3c/) and [A2C](/a2c/) followed.

## References
