---
tag: QVNG1R
kind: algorithm
slug: reinforce
name: REINFORCE
aliases:
- Monte Carlo policy gradient
- REINFORCE with baseline
area: machine-learning/reinforcement-learning
level: core
summary: "Policy gradient ascent that runs whole episodes and steps along the sum of gamma^t (G_t - b(S_t)) grad log pi(A_t|S_t), an unbiased estimate of the gradient of the return."
solves: [rl-control]
model: real-ram
complexity:
  vars: {E: the number of episodes, T: the maximum episode length, W: the cost of one evaluation of the policy and its score, d: the number of policy parameters}
  time: {worst: "O(E T W)"}
  space: {extra: "O(T + d)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 1992
  people: [Ronald J. Williams]
  note: "Williams defined the REINFORCE class of algorithms, showed that their mean update follows the gradient of the expected reinforcement, and gave the episodic version and the reinforcement baseline."
prereqs: [policy-gradient-theorem, discounted-return]
see_also: [actor-critic, generalized-advantage-estimation, natural-policy-gradient, ppo, monte-carlo-policy-evaluation, black-box-variational-inference, importance-sampling-off-policy, advantage-function]
sources:
  - paper: doi:10.1007/BF00992696
    title: "Ronald J. Williams, Simple statistical gradient-following algorithms for connectionist reinforcement learning, Machine Learning 8(3-4), 1992, pages 229 to 256"
    locator: the definition of REINFORCE algorithms and the theorem that their mean update is the gradient direction, the reinforcement baseline, and the section on episodic REINFORCE
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 13.3 (REINFORCE, Monte Carlo policy gradient) and Section 13.4 (REINFORCE with baseline)
  - paper: "Richard S. Sutton, David McAllester, Satinder Singh and Yishay Mansour, Policy gradient methods for reinforcement learning with function approximation, Advances in Neural Information Processing Systems 12, 2000, pages 1057 to 1063"
    locator: Theorem 1 (the policy gradient theorem, the expectation that REINFORCE samples)
  - paper: "Evan Greensmith, Peter L. Bartlett and Jonathan Baxter, Variance reduction techniques for gradient estimates in reinforcement learning, Journal of Machine Learning Research 5, 2004, pages 1471 to 1530"
    locator: the analysis of baselines and the optimal constant baseline
---

REINFORCE (Williams, 1992) is the simplest policy gradient method. It runs the current stochastic policy $\pi_\theta$ for a whole episode, computes the return $G_t$ that follows each step, and moves the parameters by $\eta \sum_t \gamma^t (G_t - b(S_t)) \nabla_\theta \log \pi_\theta(A_t \mid S_t)$. The baseline $b$ can be any function of the state. For every fixed $\theta$ and every baseline, the expected update is $\eta$ times the gradient of the expected discounted return, so REINFORCE is stochastic gradient ascent on the true objective. It needs no model, no value function and no bootstrapping. Its weakness is variance: the return of a whole episode is a noisy signal, and a good baseline, such as an estimate of the state value, is the first remedy. [Actor-critic](/actor-critic/) methods go further and replace the return by a learned critic.

## In plain words

The agent has a policy with adjustable knobs that gives each action a probability. It plays one full episode and then looks back at each choice it made. If the reward collected after a choice was better than usual for that situation, it turns the knobs so that this choice becomes a little more likely. If the reward was worse than usual, it makes the choice less likely. The "usual" level is the baseline; it does not change the direction of learning on average, but it makes each single adjustment much less noisy. Over many episodes, these small adjustments push the policy uphill on its average reward, exactly as if the agent knew the true slope.

## The problem

The setting is [reinforcement learning control](/rl-control/) in an episodic [Markov decision process](/markov-decision-process/) with states $S$, actions $A$, start distribution $\mu$ and discount $0 \le \gamma \le 1$. The agent can sample episodes but does not know the transition probabilities. The policy $\pi_\theta(a \mid s)$ is differentiable in $\theta \in \mathbb{R}^d$ and gives each action positive probability. The objective is the expected [discounted return](/discounted-return/) from the start,

$$J(\theta) = \mathbb{E}_{\pi_\theta}\Big[\sum_{t=0}^{T-1} \gamma^t R_{t+1}\Big],$$

where $T$ is the random time at which the episode ends, possibly cut at a fixed horizon $H$. The task is to find $\theta$ with a high $J(\theta)$ by stochastic gradient ascent.

## The algorithm

Notation: $\eta$ is the policy step size, $\eta_b$ the baseline step size, $G_t = \sum_{k=t}^{T-1} \gamma^{k-t} R_{k+1}$ the return from step $t$, and $b(s)$ the baseline. With $b = 0$ and no line L9 this is plain REINFORCE.

```pseudo id=main
REINFORCE(env, π_θ, γ, η, η_b)
L1  for each episode do
L2      run π_θ from S_0 ~ μ: S_0, A_0, R_1, …, S_{T-1}, A_{T-1}, R_T
L3      g ← 0
L4      G ← 0
L5      for t ← T − 1 down to 0 do
L6          G ← R_{t+1} + γ G                                ▷ now G = G_t
L7          g ← g + γ^t (G − b(S_t)) ∇_θ log π_θ(A_t | S_t)
L8      θ ← θ + η g
L9      for each t: b(S_t) ← b(S_t) + η_b (G_t − b(S_t))      ▷ optional learned baseline
```

Line L2 samples the episode with the current parameters; nothing changes during it. Lines L5 and L6 compute all returns in one backward pass. Line L7 adds the score $\nabla_\theta \log \pi_\theta(A_t \mid S_t)$, weighted by how much better than the baseline the return after step $t$ was. The factor $\gamma^t$ comes from the [policy gradient theorem](/policy-gradient-theorem/): the start-state objective counts a state reached at time $t$ with weight $\gamma^t$. Line L8 is one gradient step. Line L9 moves a tabular baseline toward the observed returns, which makes it an every-visit [Monte Carlo estimate](/monte-carlo-policy-evaluation/) of $V^{\pi}$; with function approximation it is one regression step. The baseline update comes after line L8, so the baseline used in line L7 does not depend on the current episode.

For the tabular softmax policy $\pi_\theta(a \mid s) \propto e^{\theta_{s,a}}$ the score is $\partial \log \pi_\theta(a \mid s) / \partial \theta_{s,b} = \mathbf{1}[a = b] - \pi_\theta(b \mid s)$, and it is zero for the parameters of other states.

## Example

Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page with $\gamma = \tfrac12$, start state 0 and the uniform softmax policy ($\theta = 0$). In state 0, action 0 pays 1 and moves to state 1 with probability $\tfrac14$, to state 0 with probability $\tfrac12$, and ends the episode otherwise; action 1 pays 0 and moves to state 1 with probability $\tfrac34$. In state 1, action 0 pays 0 and moves to state 0 with probability $\tfrac12$; action 1 pays 3 and ends the episode.

**One episode.** Suppose the episode is $S_0 = 0$, $A_0 = 0$, $R_1 = 1$, $S_1 = 1$, $A_1 = 1$, $R_2 = 3$, end. The backward pass gives $G_1 = 3$ and $G_0 = 1 + \tfrac12 \cdot 3 = \tfrac52$. Without a baseline, line L7 adds $\tfrac52 (\tfrac12, -\tfrac12) = (\tfrac54, -\tfrac54)$ to the parameters of state 0 and $\tfrac12 \cdot 3 \cdot (-\tfrac12, \tfrac12) = (-\tfrac34, \tfrac34)$ to those of state 1. With the baseline $b = V^\pi = (\tfrac{28}{27}, \tfrac{44}{27})$, the weights become $G_0 - b(0) = \tfrac{79}{54}$ and $G_1 - b(1) = \tfrac{37}{27}$, and the update is $(\tfrac{79}{108}, -\tfrac{79}{108})$ for state 0 and $(-\tfrac{37}{108}, \tfrac{37}{108})$ for state 1. Both versions raise the probability of the two actions that the episode used.

**The mean update.** Cut episodes at the horizon $H$. For $H = 3$ there are 18 possible episodes. Their probabilities times their updates sum to exactly the gradient of $J_3$, with or without any baseline:

| horizon $H$ | $J_H$ | $\partial J_H / \partial \theta_{0,0}$ | $\partial J_H / \partial \theta_{1,0}$ |
|---|---|---|---|
| 1 | $\tfrac12$ | $\tfrac14$ | $0$ |
| 2 | $\tfrac{15}{16}$ | $\tfrac{7}{32}$ | $-\tfrac{3}{16}$ |
| 3 | $\tfrac{129}{128}$ | $\tfrac{63}{256}$ | $-\tfrac{13}{64}$ |
| $\infty$ | $\tfrac{28}{27}$ | $\tfrac{184}{729}$ | $-\tfrac{148}{729}$ |

The other component in each state is the negative of the one shown. For $H = 3$, the total variance of the update (the trace of its covariance) is $\tfrac{34063}{32768} \approx 1.04$ without a baseline and about $0.27$ with $b = V^\pi$: the same mean, about a quarter of the noise.

## Correctness

Fix $\theta$ and a baseline $b$ that does not depend on the current episode. Let $g$ be the vector that lines L3 to L7 compute. If episodes are cut at a finite horizon $H$, then $\mathbb{E}[g] = \nabla J_H(\theta)$, where $J_H$ is the expected discounted reward of the first $H$ steps. If $\gamma < 1$, rewards are bounded and the score is bounded, the same holds without a cut: $\mathbb{E}[g] = \nabla J(\theta)$. The proof below has three steps. The probability of an episode is a product, so the gradient of its logarithm is $\sum_t \nabla \log \pi_\theta(A_t \mid S_t)$ (the score function or likelihood ratio identity). A score at step $t$ has mean zero given the past, so rewards that came before step $t$ drop out, which turns the total return into $G_t$. For the same reason, the term $b(S_t)$ has mean zero. In particular, the learned baseline of line L9 keeps the update unbiased, because it changes only between episodes.

So REINFORCE with step sizes $\eta_k$ that satisfy $\sum_k \eta_k = \infty$ and $\sum_k \eta_k^2 < \infty$ is a stochastic gradient method, and the general results on [stochastic approximation](/stochastic-approximation/) give convergence to a stationary point of $J$ under smoothness and bounded variance. Like any gradient method on a nonconcave $J$, it can stop at a stationary point that is not optimal.

## Complexity

One episode of length at most $T$ costs $O(T W)$ for sampling and for the backward pass of lines L5 to L7, where $W$ is the cost of one evaluation of $\pi_\theta$ and its score; for the tabular softmax $W = O(|A|)$. The update of line L8 costs $O(d)$, which is at most $T W$ when each score touches all parameters. So $E$ episodes cost $O(E T W)$ in the worst case. The algorithm stores the episode and the gradient: $O(T + d)$ extra space. An online version (below) that accumulates the score with an eligibility vector needs only $O(d)$, but it cannot subtract a baseline that depends on the future.

The number of episodes needed is governed by the variance of $g$, which can grow with the horizon and with the scale of the returns. No bound on $E$ that is polynomial in the size of the MDP holds for plain REINFORCE in general.

## Properties

- **Unbiased.** The expected update is exactly the gradient, for any baseline that depends on the state but not on the action taken.
- **On-policy.** The episode must come from the current $\pi_\theta$. Old episodes need [importance weights](/importance-sampling-off-policy/), whose variance grows with the episode length.
- **Model-free and Monte Carlo.** It uses no transition model and no bootstrapping, so it works in non-Markov settings and with partial observations as well, where value-based methods can fail.
- **High variance.** Each update uses a single sample of each return.
- **Randomized.** The sampling of actions and transitions uses random numbers.

## Variants and improvements

- **Step-by-step updates.** Sutton and Barto apply $\theta \leftarrow \theta + \eta \gamma^t G_t \nabla \log \pi_\theta(A_t \mid S_t)$ at each $t$ of the backward pass. The parameters then change inside the sum; for small $\eta$ the difference is of order $\eta^2$.
- **Batches.** Average $g$ over several episodes before line L8, which divides the variance by the batch size.
- **Better baselines.** The state value $V^\pi$ is the usual choice. The baseline that minimizes the variance weights the returns by the squared norm of the score (Greensmith et al., 2004).
- **Actor-critic.** Replace $G_t$ by a bootstrapped estimate such as $R_{t+1} + \gamma \hat V(S_{t+1})$ ([actor-critic](/actor-critic/)), or by an [advantage estimate](/generalized-advantage-estimation/) that trades bias for variance.
- **Natural gradient.** Precondition $g$ by the inverse Fisher matrix ([natural policy gradient](/natural-policy-gradient/)).
- **Trust regions.** Reuse a batch for several steps with a clipped or constrained objective ([TRPO](/trpo/), [PPO](/ppo/)).
- **Other uses.** The same score function estimator trains discrete latent variables and hard attention in deep learning, and is the basis of [black-box variational inference](/black-box-variational-inference/).

## When to use it

Use REINFORCE as a baseline method, for teaching, for short episodes, or when the reward signal is not Markov and a critic would be misleading. It is also the tool of choice to differentiate an expectation over discrete random choices, such as a sequence model trained on a reward that is not differentiable. For long episodes or sparse rewards it learns slowly; use [actor-critic](/actor-critic/) methods with [generalized advantage estimation](/generalized-advantage-estimation/), or [PPO](/ppo/). For small, known MDPs, [policy iteration](/policy-iteration/) or [value iteration](/value-iteration/) find the optimal policy directly.

## Pitfalls

- **Dropping $\gamma^t$.** Many implementations use $G_t \nabla \log \pi$ without $\gamma^t$. That is not the gradient of the discounted objective; the [policy gradient theorem](/policy-gradient-theorem/) page gives an example where it points the wrong way.
- **A baseline that depends on the action.** A baseline $b(S_t, A_t)$ gives a biased update unless it has a correction term. Use only state-dependent baselines, or the advantage form.
- **A baseline fitted on the same episode.** If $b$ is updated with the current episode before line L7, the baseline is correlated with the return it is subtracted from. The bias is small for large data, but it is not zero. Update after line L8, as here.
- **Deterministic or saturated policies.** When $\pi_\theta(a \mid s)$ is near 0 or 1, the score is near zero and learning stalls; an entropy bonus or a smaller step size helps.
- **Step size and scale.** The size of $g$ scales with the size of the returns. Normalize the returns or the advantages, or use an adaptive optimizer, else one large return can wreck the policy.
- **Time limits.** If episodes are cut at a time limit that the state does not show, the objective is the truncated $J_H$, and the policy cannot see how much time is left.

## Implementations

## History

Williams introduced the REINFORCE class in the late 1980s and gave the full treatment in the journal paper of 1992. The name is an acronym for the form of the update, "reward increment = nonnegative factor times offset reinforcement times characteristic eligibility". He proved that the mean update of any member of the class has a nonnegative inner product with the gradient of the expected reinforcement, and that it equals the gradient up to a factor when all step sizes are equal. The paper also treats episodic tasks and the reinforcement baseline. The same likelihood ratio estimator appeared independently in simulation, as the likelihood ratio method of Glynn and of Rubinstein. Sutton et al. (2000) and Marbach and Tsitsiklis (2001) put it in the general form of the [policy gradient theorem](/policy-gradient-theorem/), and Greensmith, Bartlett and Baxter (2004) analysed the variance of baselines.

## References
