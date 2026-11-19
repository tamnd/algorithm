---
tag: ZDWMJ1
kind: algorithm
slug: direct-preference-optimization
name: Direct preference optimization
aliases:
- DPO
area: natural-language-and-speech/language-modeling
level: research
summary: "Fit a language model to preference pairs with a logistic loss on the difference of its log-ratios to a frozen reference model. It optimizes the RLHF objective with no reward model and no sampling."
model: real-ram
complexity:
  vars: {m: the number of preference pairs in a batch, n: the length of a response in tokens, c: the cost of one forward and backward pass of the network per token}
  time: {worst: "Θ(m n c)"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2023
  people: [Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn]
  note: Rafailov and colleagues at Stanford showed in 2023 (NeurIPS 2023) that the KL-regularized RLHF objective can be fitted with one classification loss on preference pairs.
prereqs: [reinforcement-learning-from-human-feedback, preference-reward-model, kullback-leibler-divergence, logistic-regression]
see_also: [ppo, instruction-tuning, low-rank-adaptation, logistic-loss, softmax-regression, maximum-entropy-rl, log-sum-exp-trick, generative-pretrained-transformer]
sources:
  - url: https://arxiv.org/abs/2305.18290
    title: "Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning and Chelsea Finn, Direct preference optimization: Your language model is secretly a reward model, NeurIPS 2023"
    locator: "Section 4 (equations 4 to 7: the optimal policy, the reward in terms of the policy, the Bradley-Terry model in terms of the policy, the DPO loss, and the gradient), Appendix A.1 (the optimum of the KL-constrained objective), Appendix A.4 (the gradient), Section 5.1 (Lemmas 1 and 2, Theorem 1), Section 6 (the experiments)"
  - paper: "Ralph Allan Bradley and Milton E. Terry, Rank analysis of incomplete block designs I. The method of paired comparisons, Biometrika 39(3-4), 1952, pages 324 to 345"
    title: Bradley and Terry 1952
    locator: the paired comparison model, with the probability that i beats j proportional to the ratio of their strengths
  - url: https://arxiv.org/abs/2203.02155
    title: "Long Ouyang, Jeff Wu, Xu Jiang and others, Training language models to follow instructions with human feedback, NeurIPS 2022"
    locator: "Section 3.5 (the reward model loss and the KL-penalized objective that DPO targets)"
  - url: https://arxiv.org/abs/2310.12036
    title: "Mohammad Gheshlaghi Azar, Mark Rowland, Bilal Piot, Daniel Guo, Daniele Calandriello, Michal Valko and Remi Munos, A general theoretical paradigm to understand learning from human preferences, AISTATS 2024"
    locator: the analysis of DPO with deterministic preferences and the IPO loss
---

Direct preference optimization (DPO) trains a language model on pairs of responses where people said which one they prefer. It fits the same objective as [reinforcement learning from human feedback](/reinforcement-learning-from-human-feedback/) (RLHF), the expected reward minus $\beta$ times the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from a reference model, but it skips the two stages of that pipeline. It fits no separate [preference reward model](/preference-reward-model/), and it does not sample from the model or run [PPO](/ppo/). The loss of one pair is $-\log \sigma(\beta ((\log \pi_\theta(y_w) - \log \pi_{\text{ref}}(y_w)) - (\log \pi_\theta(y_l) - \log \pi_{\text{ref}}(y_l))))$, a [logistic loss](/logistic-loss/) on the difference of two log-ratios. The derivation is exact under the Bradley-Terry model of preferences. Whether DPO gives a better model than RLHF on a given task is a measured question, with mixed answers. DPO is usually run after [instruction tuning](/instruction-tuning/), which supplies the reference model.

## In plain words

You have a model that already answers questions, and a pile of examples where a person saw two answers to the same question and picked the better one.

DPO keeps a frozen copy of the starting model. For each example it asks two things: how much more likely does the new model make the chosen answer than the frozen copy does, and how much more likely does it make the rejected answer? Training pushes the first amount up and the second down.

The push is strong when the model still prefers the rejected answer, and weak when it already ranks the pair correctly. One setting controls how far the new model may move away from the frozen copy.

## The problem

The data is a set of triples $(x, y_w, y_l)$: a prompt $x$, a preferred response $y_w$ and a dispreferred response $y_l$. There is a reference policy $\pi_{\text{ref}}$, usually the model after supervised fine-tuning, which stays frozen. A policy assigns a sequence log probability $\log \pi(y \mid x) = \sum_{t=1}^{n} \log \pi(y_t \mid x, y_{1:t-1})$ to a response of $n$ tokens, by [causal language modeling](/causal-language-modeling/). The goal is the policy that maximizes the RLHF objective

$$\max_{\pi}\; \mathbb{E}_{x}\Big[ \mathbb{E}_{y \sim \pi(\cdot \mid x)} [r(x, y)] - \beta\, \mathrm{KL}\big(\pi(\cdot \mid x) \,\|\, \pi_{\text{ref}}(\cdot \mid x)\big) \Big]$$

for a reward $r$ that is never observed. What is observed are the preferences, which are assumed to follow the Bradley-Terry model $p(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l))$ with $\sigma(z) = 1 / (1 + e^{-z})$. The page has no Bradley-Terry page to link; see [preference reward model](/preference-reward-model/).

Three steps give the DPO loss, and [proofs/correctness.md](proofs/correctness.md) proves each one.

1. For a fixed reward, the objective has the unique optimum $\pi^*(y \mid x) = \pi_{\text{ref}}(y \mid x)\, e^{r(x, y)/\beta} / Z(x)$, with $Z(x) = \sum_y \pi_{\text{ref}}(y \mid x)\, e^{r(x, y)/\beta}$.
2. Solving for the reward gives $r(x, y) = \beta \log (\pi^*(y \mid x) / \pi_{\text{ref}}(y \mid x)) + \beta \log Z(x)$.
3. In the Bradley-Terry probability only the difference of two rewards for the same $x$ appears, so $\beta \log Z(x)$ cancels, and the preference probability is a function of the policy alone.

Replace $\pi^*$ by the trained policy $\pi_\theta$ and maximize the likelihood of the data. That gives the loss

$$L(\theta) = -\mathbb{E}_{(x, y_w, y_l)} \log \sigma\!\left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right).$$

The quantity $\hat r(x, y) = \beta \log (\pi_\theta(y \mid x) / \pi_{\text{ref}}(y \mid x))$ is the implicit reward of the policy, and $L$ is the Bradley-Terry loss of that reward.

## The algorithm

For each pair the network computes four sequence log probabilities: $a_w = \log \pi_\theta(y_w \mid x)$ and $a_l = \log \pi_\theta(y_l \mid x)$ with gradients, and $b_w$, $b_l$ under $\pi_{\text{ref}}$ with no gradients (they can be computed once before training). The algorithm below takes them as given and returns the mean loss over a batch of $m$ pairs and its gradient with respect to $a_w$ and $a_l$. The training framework multiplies these by $\nabla_\theta a_w$ and $\nabla_\theta a_l$ ([backpropagation](/backpropagation/)) and takes an optimizer step.

```pseudo id=main
DPO-LOSS(β, P)                  ▷ P: m tuples (a_w, b_w, a_l, b_l)
L1  total ← 0
L2  for each (a_w, b_w, a_l, b_l) in P do
L3      z ← β ((a_w - b_w) - (a_l - b_l))      ▷ implicit reward margin
L4      total ← total + log_add(0, -z)          ▷ -log σ(z), no overflow
L5      q ← σ(-z)                               ▷ in [0, 1], computed stably
L6      ∂L/∂a_w ← -β q / m;  ∂L/∂a_l ← β q / m
L7  return total / m and the gradients
```

Here log_add$(a, b) = \max(a, b) + \log(1 + e^{-|a - b|})$, from the [log-sum-exp trick](/log-sum-exp-trick/).

## Example

Take $\beta = 0.1$ and a batch of two pairs.

| pair | $a_w$ | $b_w$ | $a_l$ | $b_l$ | L3 $z$ | L4 $-\log \sigma(z)$ | L5 $q = \sigma(-z)$ | L6 $\partial L / \partial a_w$ |
|---|---|---|---|---|---|---|---|---|
| 1 | -12 | -13 | -15 | -14 | 0.2 | 0.598139 | 0.450166 | -0.0225083 |
| 2 | -20 | -18 | -21 | -22 | -0.3 | 0.854355 | 0.574443 | -0.0287221 |

Line L7 returns the mean loss $(0.598139 + 0.854355) / 2 = 0.726247$. In pair 1 the policy already gives the preferred response a higher log-ratio than the rejected one (implicit rewards $0.1$ and $-0.1$), so $z > 0$ and the weight $q$ is below one half. In pair 2 the order is wrong ($\hat r_w = -0.2$, $\hat r_l = 0.1$), so $z < 0$ and the pair gets the larger weight. Each $\partial L / \partial a_l$ is the negative of $\partial L / \partial a_w$. Pair 2 shows that $a_w$ can be lower than $a_l$ and still count as a win: only the change relative to the reference matters.

The target of the training can be computed by hand for one prompt with three responses. With $\pi_{\text{ref}} = (0.5, 0.3, 0.2)$, rewards $r = (0, 1, 2)$ and $\beta = 1$, step 1 gives $Z = 0.5 + 0.3 e + 0.2 e^2 = 2.793296$ and $\pi^* = (0.17900, 0.29194, 0.52906)$. The expected reward rises from 0.7 under $\pi_{\text{ref}}$ to 1.35006, at a KL cost of 0.32283 nats, and the objective is $\beta \log Z = 1.02722$. A smaller $\beta$ moves further: $\beta = 0.5$ gives $\pi^* = (0.03667, 0.16256, 0.80077)$ and $\beta = 2$ gives $(0.32504, 0.32154, 0.35342)$. The tests run gradient descent on the population DPO loss with Bradley-Terry labels for these rewards, on a softmax policy over the three responses, and reach $\pi^*$ within $10^{-6}$.

## Correctness

[proofs/correctness.md](proofs/correctness.md) has the full proofs. The objective equals $\beta \log Z(x) - \beta\, \mathrm{KL}(\pi \,\|\, \pi^*)$, so Gibbs' inequality makes $\pi^*$ the unique optimum (Theorem 1, the result of Appendix A.1 of Rafailov and colleagues). The reward is $\beta \log(\pi^* / \pi_{\text{ref}})$ plus a term in $x$ that cancels in every Bradley-Terry difference. So the DPO loss is the negative log likelihood of the preferences under the reward that the policy implies. If every pair of responses is compared with positive probability, the labels follow the Bradley-Terry model, and the policy class can express $\pi^*$, the population loss is minimized exactly at $\pi^*$ (Proposition 4). For lines L5 and L6: $\frac{d}{dz}(-\log \sigma(z)) = -\sigma(-z)$, and $z$ has slope $\beta$ in $a_w$ and $-\beta$ in $a_l$.

These are statements about the population optimum. A finite data set, a network that cannot express $\pi^*$, and an optimizer that stops early can all give another policy; what DPO does then is measured, not proved.

## Complexity

The loss and its gradient (lines L1 to L7) cost $\Theta(m)$ in the [real RAM](/real-ram/), which is nothing next to the network. The cost of a training step is dominated by the four sequence log probabilities: two forward passes and one backward pass of $\pi_\theta$ over $y_w$ and $y_l$, and two forward passes of $\pi_{\text{ref}}$ (or none, if the reference log probabilities are cached). For responses of $n$ tokens and a cost $c$ per token of one pass, that is $\Theta(m n c)$. RLHF with PPO needs, per step, sampling from the policy token by token, a reward model pass and a value network, so DPO is cheaper per step; the saving in wall-clock time is a measurement that depends on the system. Memory holds the policy, the reference model (unless its log probabilities are cached) and the optimizer state, against four models for PPO (policy, reference, reward and value).

## Properties

- **No reward model and no sampling (by construction).** The loss uses only the four log probabilities of fixed data, so training is supervised learning.
- **Same optimum as the RLHF objective (theorem).** Under the conditions of Proposition 4, both reach $\pi^*$.
- **Weighting by error.** The weight $\sigma(-z) = \sigma(\hat r_l - \hat r_w)$ is large on pairs the implicit reward ranks wrongly and small on pairs it ranks rightly.
- **Shift invariance.** Adding a function of $x$ to the reward does not change $\pi^*$ or the preferences, so DPO can recover the reward only up to such a term.
- **Relative, not absolute.** The loss depends on $a_w - a_l - (b_w - b_l)$ only. It can lower $\log \pi_\theta(y_w)$ as long as it lowers $\log \pi_\theta(y_l)$ more.
- **Offline.** The pairs are fixed. The policy is not evaluated on its own samples during training.

## Variants and improvements

- **IPO** (Azar and colleagues 2024) replaces the logistic loss by a squared loss on the margin, to keep a finite optimum when the preferences in the data are deterministic.
- **Several responses.** Rafailov and colleagues also give the loss for rankings of more than two responses, under the Plackett-Luce model.
- **Iterative or online DPO.** Sample new pairs from the current policy, label them, and train again. This brings back part of the sampling of RLHF.
- **With LoRA.** DPO is often run with [low-rank adaptation](/low-rank-adaptation/); then the reference is the base model with the adapter turned off, and no second copy of the weights is needed.

## When to use it

Use DPO when you have a fixed set of preference pairs, a reference model after supervised fine-tuning, and you want the KL-regularized objective of RLHF without training a reward model or running PPO. Use RLHF with a reward model when you want to score new samples of the policy during training, to reuse the reward model elsewhere, or to label more data than people can compare. Rafailov and colleagues measured that DPO matched or exceeded PPO-based RLHF on controlled sentiment generation (IMDb with GPT-2-large), summarization (TL;DR with GPT-J) and single-turn dialogue (Anthropic HH with Pythia-2.8B), with GPT-4 as the judge on the last two; these are measurements on their setup.

## Pitfalls

- **Deterministic preferences.** If a pair always has the same winner, the loss has no finite minimizer, and training drives $\pi_\theta(y_l)$ toward 0 for any $\beta$. The KL term of the objective does not prevent it, because the derivation assumed a finite reward.
- **A reference that does not match the data.** The derivation assumes $\pi_{\text{ref}}$ is the model the KL is measured against. If the preferred responses are very unlikely under $\pi_{\text{ref}}$, the log-ratios are large and noisy. Fine-tune the reference on the preferred responses first, as Rafailov and colleagues do when no reference is available.
- **Overflow in the loss.** $\log(1 + e^{-z})$ computed directly overflows for $z$ below about $-709$ in double precision and much earlier in half precision. Use log_add as in line L4, and the two-branch sigmoid in line L5.
- **Per-token means instead of sums.** The derivation uses sequence log probabilities, the sums over tokens. Averaging over tokens changes the objective and favors short or long responses.
- **Reading $\beta$ as a fixed constant.** $\beta$ is a hyperparameter chosen on held out data; Rafailov and colleagues swept values such as 0.05, 0.1, 1 and 5. A smaller $\beta$ lets the policy move further from the reference.
- **Expecting the log probability of the preferred response to rise.** The loss can fall while both $a_w$ and $a_l$ fall. Watch both, not only the margin.

## Implementations

The code takes the four sequence log probabilities of each pair as given and implements the loss and its gradient; it does not train a network and does not load weights. It also has a tabular softmax policy over a few responses of one prompt, used to check the derivation: the tests compare the gradients with central finite differences ($h = 10^{-6}$, tolerance $10^{-5}$), check that no random policy beats $\beta \log Z$, check that gradient descent on the population loss reaches $\pi^*$, and check margins of $\pm 1000$ and sequence log probabilities of $-3000$. It uses log_add from the shared helper nlslog.py.

## History

Christiano and colleagues (2017) fitted a reward model to human comparisons with the Bradley-Terry likelihood and trained a policy on it by reinforcement learning. Stiennon and colleagues (2020) and Ouyang and colleagues (2022) applied the same pipeline to language models with PPO and a KL penalty to a reference model. That the optimum of a KL-regularized reward objective is $\pi_{\text{ref}} e^{r/\beta} / Z$ was known from earlier work on KL-controlled and maximum entropy reinforcement learning. Rafailov, Sharma, Mitchell, Ermon, Manning and Finn (2023) used that closed form to write the reward in terms of the policy, observed that $Z$ cancels in the Bradley-Terry likelihood, and so turned the whole pipeline into one classification loss. Azar and colleagues (2024) analyzed where the derivation breaks with deterministic preferences.

## References
