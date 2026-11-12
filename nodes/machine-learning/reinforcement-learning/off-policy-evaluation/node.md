---
tag: 982C79
kind: problem
slug: off-policy-evaluation
name: Off-policy evaluation
aliases:
- OPE
- off-policy policy evaluation
- counterfactual policy evaluation
area: machine-learning/reinforcement-learning
level: advanced
summary: "Estimate the value of a target policy from data logged by a different behavior policy, without running the target policy. Main methods: direct method, importance sampling, doubly robust."
model: real-ram
prereqs: [importance-sampling-off-policy, state-value-function]
see_also: [policy-evaluation, offline-reinforcement-learning, contextual-bandit, retrace, fitted-q-iteration, least-squares-td, effective-sample-size, importance-sampling]
sources:
  - paper: arxiv:1103.4601
    title: Miroslav Dudik, John Langford and Lihong Li, Doubly robust policy evaluation and learning, Proceedings of the 28th International Conference on Machine Learning, 2011
    locator: the direct method, inverse propensity scoring and the doubly robust estimator for contextual bandits, with the bias and variance analysis
  - paper: arxiv:1511.03722
    title: Nan Jiang and Lihong Li, Doubly robust off-policy value evaluation for reinforcement learning, Proceedings of the 33rd International Conference on Machine Learning, 2016
    locator: the sequential doubly robust estimator, its unbiasedness, and the lower bound on the variance
  - paper: arxiv:1604.00923
    title: Philip S. Thomas and Emma Brunskill, Data-efficient off-policy policy evaluation for reinforcement learning, Proceedings of the 33rd International Conference on Machine Learning, 2016
    locator: weighted doubly robust and the MAGIC estimator, which blends model-based and importance sampling estimates
  - paper: "Doina Precup, Richard S. Sutton and Satinder Singh, Eligibility traces for off-policy policy evaluation, Proceedings of the 17th International Conference on Machine Learning, 2000, pages 759 to 766"
    locator: per-decision importance sampling for off-policy evaluation
---

Off-policy evaluation (OPE) is the problem of estimating the expected return $V(\pi)$ of a target policy $\pi$ from data that a different behavior policy $\mu$ collected. The target policy is never run. This is the safe way to test a new policy for medicine, recommendation or advertising, where a bad policy costs real money or harm. The data show the rewards of the actions $\mu$ took and nothing about the other actions, so every method must fill the gap: with a model of the rewards (the direct method), with [importance sampling](/importance-sampling-off-policy/) weights $\pi/\mu$ (inverse propensity scoring), or with both. The doubly robust estimator of Dudik, Langford and Li (2011) uses the model as a baseline and importance weights to correct its error. It is unbiased when either the model or the behavior probabilities are right. Jiang and Li (2016) extend it to sequential decisions.

## In plain words

An old rule made decisions and someone kept a log of what happened. You have a new rule and want to know how well it would do, but you cannot try it. One way is to build a guess of what each choice would give and ask the guess. If the guess is wrong, the answer is wrong. Another way is to look only at logged cases where the old rule made a choice the new rule likes, and count those cases more. That is fair on average but jumps a lot from log to log. The doubly robust way starts from the guess and then uses the reweighted log cases to fix the guess. It stays fair on average if either the guess is right or you know exactly how the old rule chose.

## Definition

**Contextual bandit form.** A context $x$ comes from a distribution $D$, an action $a$ comes from the behavior policy $\mu(\cdot \mid x)$, and a reward $r$ comes from a distribution with mean $q(x, a)$. The input is a log of $n$ independent triples $(x_i, a_i, r_i)$, the target policy $\pi$, and often the logged probabilities $\mu(a_i \mid x_i)$. The output is an estimate of

$$V(\pi) = \mathbb{E}_{x \sim D}\Big[\sum_a \pi(a \mid x)\, q(x, a)\Big].$$

**Sequential form.** The log holds episodes $(S_0, A_0, R_1, \ldots, S_T)$ of a [Markov decision process](/markov-decision-process/) under $\mu$, and the output is an estimate of $v_\pi(s_0)$, the [state value](/state-value-function/) of the start state, or of its mean over a start distribution. A bandit is the case $T = 1$.

**Coverage.** $\pi(a \mid x) > 0$ must imply $\mu(a \mid x) > 0$. Without it the rewards of some actions that $\pi$ takes never appear in the log, and no estimator can be consistent without assumptions on $q$.

The quality of an estimate $\hat{V}$ is its mean squared error, $\mathbb{E}[(\hat{V} - V(\pi))^2] = \text{bias}^2 + \text{variance}$.

## Variants

- **Known or estimated propensities.** In a logged system $\mu(a_i \mid x_i)$ is often recorded. In observational data it must be estimated as $\hat{\mu}$, and its errors bias the importance weights.
- **Deterministic or stochastic target.** A deterministic $\pi$ uses only the logged samples whose action matches $\pi(x)$ in importance sampling.
- **Finite horizon or discounted.** The sequential problem is posed for episodes of length $T$ or with a discount $\gamma$; the importance weights are products over time, so their variance can grow exponentially in $T$.
- **Policy evaluation with the model given.** If the MDP is known, the problem is plain [policy evaluation](/policy-evaluation/), and no data are needed.
- **Confidence bounds.** High-confidence off-policy evaluation asks for a lower bound on $V(\pi)$ that holds with probability $1 - \delta$, for safe deployment.
- **Off-policy learning.** Choosing the best $\pi$ by maximizing an OPE estimate is the core of [offline reinforcement learning](/offline-reinforcement-learning/) and of policy learning in [contextual bandits](/contextual-bandit/).

## Examples

A contextual bandit with two equally likely contexts $x \in \{0, 1\}$, three actions and Bernoulli rewards. The mean rewards are $q(0, \cdot) = (0.2, 0.5, 0.9)$ and $q(1, \cdot) = (0.6, 0.3, 0.1)$. The behavior policy is uniform. The target policy takes action 2 with probability $0.8$ and action 1 with probability $0.2$ in context 0, and takes action 0 in context 1. So $V(\pi) = \frac12(0.1 + 0.72) + \frac12 \cdot 0.6 = 0.71$.

The wrong model is $\hat{q}(0, \cdot) = (0.15, 0.55, 1.05)$ and $\hat{q}(1, \cdot) = (0.55, 0.35, 0.25)$. The wrong propensities are $\hat{\mu}(\cdot \mid 0) = (1/2, 1/4, 1/4)$ and $\hat{\mu}(\cdot \mid 1) = (1/4, 1/4, 1/2)$. The table gives the exact mean and the exact variance of each estimator on one logged sample, computed with fractions over all $18$ outcomes; with $n$ samples the variance divides by $n$.

| case | DM mean | DM var | IPS mean | IPS var | DR mean | DR var |
|---|---|---|---|---|---|---|
| model and propensities right | 0.71 | 0.012 | 0.71 | 1.290 | 0.71 | 0.474 |
| model wrong | 0.75 | 0.040 | 0.71 | 1.290 | 0.71 | 0.489 |
| propensities wrong | 0.71 | 0.012 | 0.947 | 2.293 | 0.71 | 0.832 |
| both wrong | 0.75 | 0.040 | 0.947 | 2.293 | 0.697 | 0.855 |

The direct method has the smallest variance but takes the full bias of the model. Inverse propensity scoring is unbiased only with the right propensities, and its variance is the largest. Doubly robust is unbiased in the three rows where at least one part is right, and in the last row its bias, $-0.013$, is a product of the two errors and is much smaller than the bias of either other method. Self-normalized IPS on two samples has the exact mean $2741/5400 \approx 0.508$, a reminder that the weighted estimators are biased for small $n$.

## Known algorithms

- **Direct method (DM).** Fit $\hat{q}$ by regression on the log and return $\frac1n\sum_i\sum_a \pi(a \mid x_i)\hat{q}(x_i, a)$. In the sequential case, fit a model of the MDP or a $Q$ function with [fitted Q iteration](/fitted-q-iteration/) or [LSTD](/least-squares-td/) and evaluate $\pi$ on it. Low variance, bias equal to the model error under $\pi$.
- **Inverse propensity scoring (IPS).** Return $\frac1n\sum_i w_i r_i$ with $w_i = \pi(a_i \mid x_i)/\mu(a_i \mid x_i)$. Unbiased with the true $\mu$, but the variance grows with the size of the weights. The sequential versions are ordinary and per-decision [importance sampling](/importance-sampling-off-policy/).
- **Self-normalized IPS (SNIPS).** Divide by $\sum_i w_i$ instead of $n$. Biased, consistent, and bounded by the range of the rewards.
- **Doubly robust (DR).** For bandits,

$$\hat{V}_{\text{DR}} = \frac1n\sum_{i=1}^n\Big[\sum_a \pi(a \mid x_i)\hat{q}(x_i, a) + \frac{\pi(a_i \mid x_i)}{\hat{\mu}(a_i \mid x_i)}\big(r_i - \hat{q}(x_i, a_i)\big)\Big].$$

  For episodes, Jiang and Li (2016) apply the same step backward in time: $V_{\text{DR}}^{T} = 0$ and

$$V_{\text{DR}}^{t} = \hat{V}(S_t) + \rho_t\big(R_{t+1} + \gamma V_{\text{DR}}^{t+1} - \hat{Q}(S_t, A_t)\big), \qquad \hat{V}(s) = \sum_a \pi(a \mid s)\hat{Q}(s, a), \quad \rho_t = \frac{\pi(A_t \mid S_t)}{\hat{\mu}(A_t \mid S_t)}.$$

  With $\hat{Q} = 0$ it is per-decision importance sampling. The cost is $O(nA)$ for $n$ logged steps and $A$ actions.
- **Weighted DR and MAGIC.** Thomas and Brunskill (2016) normalize the weights in DR and then blend estimators that switch from importance sampling to the model at different horizons, with weights chosen to minimize an estimate of the mean squared error.
- **Eligibility trace methods.** [Retrace](/retrace/) and Tree Backup learn $Q^\pi$ from off-policy data with truncated or no importance weights, and serve as model-based parts of DR.

**Why DR is unbiased when one part is right.** Fix $x$ and write $\delta(x, a) = \hat{q}(x, a) - q(x, a)$. The expected DR term given $x$ is

$$\sum_a \pi(a \mid x)\hat{q}(x, a) + \sum_a \mu(a \mid x)\frac{\pi(a \mid x)}{\hat{\mu}(a \mid x)}\big(q(x, a) - \hat{q}(x, a)\big) = \sum_a \pi(a \mid x)q(x, a) + \sum_a \pi(a \mid x)\,\delta(x, a)\Big(1 - \frac{\mu(a \mid x)}{\hat{\mu}(a \mid x)}\Big).$$

The last sum is the bias. It is zero if $\delta = 0$ (the model is right) or if $\hat{\mu} = \mu$ (the propensities are right), and otherwise it is a sum of products of the two errors. The sequential estimator has the same form at each step, so by induction backward from $T$ it is unbiased if $\hat{\mu} = \mu$ at every step or if $\hat{Q} = Q^\pi$.

## Bounds

With the true propensities, write $w = \pi(a \mid x)/\mu(a \mid x)$, $\sigma^2(x, a)$ for the reward variance and $V(x) = \sum_a \pi(a \mid x)q(x, a)$. The variance of one DR term splits into three parts:

$$\operatorname{Var}[\hat{V}_{\text{DR}}] = \operatorname{Var}_x[V(x)] + \mathbb{E}_x\big[\operatorname{Var}_{a \sim \mu}[w\,\delta(x, a)]\big] + \mathbb{E}_{x, a \sim \mu}\big[w^2\sigma^2(x, a)\big].$$

The first part is in every estimator; the last part is the reward noise blown up by the weights; the middle part is the model error blown up by the weights. IPS is the case $\hat{q} = 0$, so $\delta = -q$ and the middle part carries the whole reward function. DR lowers the variance exactly when $\hat{q}$ is closer to $q$ than $0$ is in this weighted sense. The direct method has variance $\operatorname{Var}_x[\hat{V}(x)]/n$ but a bias that does not shrink with $n$.

In the sequential case, importance sampling with $T$ steps can have variance exponential in $T$, as in the example of the [importance sampling](/importance-sampling-off-policy/) page. Jiang and Li (2016) prove a Cramér-Rao type lower bound on the variance of any unbiased estimator for tree-structured MDPs, and show that DR with an exact model matches it in some cases.

## Reductions

- The bandit case is the one-step sequential case; the sequential DR applies the bandit DR backward over time with the value of the next step as the reward.
- OPE with a known MDP is [policy evaluation](/policy-evaluation/).
- OPE is a special case of estimating a mean under one distribution from samples of another, which is [importance sampling](/importance-sampling/). DR is the control variate form of importance sampling, with $\hat{q}$ as the control variate.

## Applications

Evaluation of news recommendation, search ranking and advertising policies from logs before a live test; evaluation of treatment policies in medicine from observational records; model selection and hyperparameter tuning in [offline reinforcement learning](/offline-reinforcement-learning/); and safe policy improvement, which deploys a new policy only when a lower confidence bound on its OPE estimate beats the current policy.

## References
