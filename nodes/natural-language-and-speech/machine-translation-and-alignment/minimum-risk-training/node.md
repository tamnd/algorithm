---
tag: 1GGJMF
kind: technique
slug: minimum-risk-training
name: Minimum risk training
aliases:
- expected risk minimization for sequences
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Train a sequence model to minimize the expected loss, such as 1 - BLEU, over a sample of its own outputs, renormalized.
history:
  year: 2016
  people: [Shiqi Shen, Yong Cheng, Zhongjun He, Wei He, Hua Wu, Maosong Sun, Yang Liu]
  note: Shen et al. applied minimum risk training to neural machine translation at ACL 2016. The idea of minimizing the expected loss of a translation system is older and comes from statistical machine translation.
prereqs: [encoder-decoder-model, bleu, maximum-likelihood-estimation]
see_also: [minimum-error-rate-training, minimum-bayes-risk-decoding, exposure-bias, cross-entropy-loss, reinforce, scheduled-sampling, sequence-level-knowledge-distillation, stochastic-gradient-descent]
sources:
  - paper: doi:10.18653/v1/P16-1159
    title: Shiqi Shen, Yong Cheng, Zhongjun He, Wei He, Hua Wu, Maosong Sun and Yang Liu, Minimum Risk Training for Neural Machine Translation, ACL 2016, pages 1683 to 1692
    locator: "the risk over a sampled subset of candidates, the sharpness alpha and the gradient alpha Q (Delta - R), with alpha = 5e-3 in the experiments"
---

Minimum risk training trains a sequence model, such as a neural translation model, to minimize the expected loss of its own outputs instead of the negative log likelihood of the reference. The loss is any sentence-level cost, for example 1 - sentence BLEU. The exact expectation is a sum over all output sequences, so the technique samples a small set of candidates from the model and renormalizes the model probabilities over that set, with a sharpness parameter α. Shen et al. (2016) applied it to neural machine translation. The written text sometimes calls it MRT.

## In plain words

Normal training shows the model the reference translation and makes it more likely. The model never sees its own mistakes, and it never learns that some wrong translations are worse than others.

Minimum risk training asks the model to translate. It draws several candidate translations from the model, and a metric such as BLEU gives each candidate a loss. The model then moves probability from the candidates with a high loss to the candidates with a low loss.

The quantity that falls is the average loss of the candidates, weighted by how likely the model finds them. Because the candidates come from the model itself, the training sees the same kind of output that the model will produce at test time.

## When it applies

- The model gives a probability $P(y \mid x; \theta)$ to a whole output sequence, and you can compute $\log P(y \mid x; \theta)$ and its gradient for any $y$. An [encoder-decoder model](/encoder-decoder-model/) does this by the chain rule over the tokens.
- You can sample or list candidate outputs from the model.
- There is a loss $\Delta(y, y^*) $ for a candidate $y$ and the reference $y^*$ that you care about, such as 1 - sentence [BLEU](/bleu/), 1 - [chrF](/chrf/) or [TER](/translation-edit-rate/). The loss need not be differentiable.
- The model already gives sensible outputs. Shen et al. start from a model trained by [maximum likelihood](/maximum-likelihood-estimation/); a random model gives candidates that are all bad, and the risk has almost no signal.

## The template

For one sentence pair $(x, y^*)$ with a subset $S(x)$ of candidates, the renormalized distribution and the risk are

$$Q(y \mid x; \theta, \alpha) = \frac{P(y \mid x; \theta)^{\alpha}}{\sum_{y' \in S(x)} P(y' \mid x; \theta)^{\alpha}}, \qquad R(\theta) = \sum_{y \in S(x)} Q(y \mid x; \theta, \alpha) \, \Delta(y, y^*).$$

The training objective is the sum of $R$ over the training pairs, minimized by [stochastic gradient descent](/stochastic-gradient-descent/). Write $\ell_y = \log P(y \mid x; \theta)$. Then $Q$ is the softmax of $\alpha \ell_y$, and

$$\frac{\partial R}{\partial \ell_y} = \alpha \, Q(y) \bigl(\Delta(y, y^*) - R\bigr), \qquad \frac{\partial R}{\partial \theta} = \sum_{y \in S(x)} \alpha \, Q(y) \bigl(\Delta(y, y^*) - R\bigr) \frac{\partial \ell_y}{\partial \theta}.$$

```pseudo id=main
SENTENCE-RISK(ℓ_y for y in S, Δ_y for y in S, α)
L1  for each y in S do s_y ← α · ℓ_y
L2  Q ← SOFTMAX(s)                                ▷ subtract max_y s_y before exp
L3  R ← Σ_y Q(y) Δ_y
L4  for each y in S do g_y ← α Q(y) (Δ_y - R)     ▷ g_y = ∂R / ∂ℓ_y
L5  return R, Q, g

CORPUS-RISK(batch, α)
L6  for each sentence pair in the batch do R_i, g_i ← SENTENCE-RISK(...)
L7  return Σ_i R_i and the g_i                    ▷ backpropagate Σ_y g_y ∂ℓ_y/∂θ
```

Line L2 works in log space with the [log-sum-exp trick](/log-sum-exp-trick/): a sentence probability is a product of many token probabilities and underflows in double precision, but $\alpha \ell_y$ does not. Line L4 is the derivative by the softmax Jacobian. A candidate with a loss above the current risk gets a positive $g_y$, so a gradient step lowers its log probability; a candidate with a loss below the risk gets a negative $g_y$ and is pushed up. Line L7 hands the $g_y$ to the usual backpropagation through the network, as if $g_y$ were the weight of the log likelihood of $y$.

The code on this page takes the log probabilities $\ell_y$ and the losses as given and implements lines L1 to L7; it does not train a network. The tests check the gradient through a toy model by central finite differences.

These facts about the template are theorems with short proofs:

- **Bounds.** $\min_y \Delta_y \le R \le \max_y \Delta_y$, because $R$ is an average under $Q$.
- **Zero-sum gradient.** $\sum_y \partial R / \partial \ell_y = \alpha (R - R) = 0$. So adding the same constant to every $\ell_y$ does not change $R$, and adding a constant to every loss $\Delta_y$ does not change the gradient. Training with $-\mathrm{BLEU}$ and with $1 - \mathrm{BLEU}$ is the same.
- **Exact expectation.** If $S(x)$ is the set of all outputs and $\alpha = 1$, then $Q = P$ and $R$ is the exact expected loss $\mathbb{E}_{y \sim P}[\Delta(y, y^*)]$.
- **Limits of α.** As $\alpha \to 0$, $Q$ tends to the uniform distribution on $S(x)$. As $\alpha \to \infty$, $Q$ puts all its mass on the most probable candidates in $S(x)$, and $R$ tends to their loss.

With a sampled subset, $R$ is not an unbiased estimate of the expected loss under $P$; it is a different objective that Shen et al. found to work (a heuristic).

## Classic examples

- **Hand example.** Take three candidates with $P = 0.5, 0.3, 0.2$ and losses $\Delta = 0, 0.5, 1$. With $\alpha = 1$, $Q = P$ and $R = 0.5 \cdot 0 + 0.3 \cdot 0.5 + 0.2 \cdot 1 = 0.35$. The gradient in $\ell$ is $g = (0.5 (0 - 0.35), 0.3 (0.5 - 0.35), 0.2 (1 - 0.35)) = (-0.175, 0.045, 0.13)$, which sums to 0. With $\alpha = 0.5$, $Q \propto (\sqrt{0.5}, \sqrt{0.3}, \sqrt{0.2})$ gives $Q = (0.4154, 0.3218, 0.2628)$ and $R = 0.4237$: a smaller $\alpha$ flattens $Q$ and moves the risk toward the plain mean 0.5.
- **Neural translation.** Shen et al. (2016) sampled candidates from an attention-based model trained by maximum likelihood, used a loss based on sentence-level BLEU, and set $\alpha = 5 \times 10^{-3}$. They reported BLEU gains over maximum likelihood training on Chinese to English, English to French and English to German (measurements; see the paper for the test sets and the numbers).
- **Statistical machine translation.** [Minimum error rate training](/minimum-error-rate-training/) tunes the few weights of a log-linear model to minimize the error of the 1-best output directly. Minimum risk training uses a smooth expectation in its place, so it can train millions of parameters by gradient descent.

## Variations

- **The loss.** Any sentence-level cost works: 1 - smoothed sentence BLEU, 1 - chrF, TER, or a learned metric such as [COMET](/comet-metric/). The model learns to please the metric, including its faults.
- **Mixed objective.** Many systems add a fraction of the [cross-entropy loss](/cross-entropy-loss/) on the reference to keep the model close to fluent text.
- **Candidates from beam search.** The subset can come from [beam search](/beam-search/) instead of sampling. Beam candidates are more alike, so $Q$ sees less of the space.
- **Policy gradient.** [REINFORCE](/reinforce/) with the reward $-\Delta$ estimates the gradient of the true expected loss from samples, with a baseline in place of $R$. Minimum risk training renormalizes over the subset instead, which gives a biased but lower variance estimate (a heuristic comparison, not a theorem).
- **Decoding.** [Minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) uses the same expected loss at test time to choose an output, with no training.

## Pitfalls

- **Starting from scratch.** With random parameters every candidate is bad, the losses are all close to 1, and the gradient is near 0. Start from a model trained by maximum likelihood.
- **The wrong α.** A large α makes $Q$ nearly one-hot, so only the top candidate gets a gradient. Shen et al. used the small value $5 \times 10^{-3}$ in their experiments; it is a hyperparameter, so tune it on held-out data (a heuristic).
- **Counting duplicates.** Sampling often draws the same candidate twice. $S(x)$ is a set; if a duplicate stays in the list, its weight in $Q$ doubles.
- **Sentence BLEU without smoothing.** Many short candidates have no matching 4-gram, so their BLEU is 0 and the losses tie. Use a smoothed sentence BLEU or chrF.
- **Cost.** Each update decodes and scores many candidates for each source sentence, which makes an epoch much slower than maximum likelihood training (a measurement of the setup, not a bound).
- **Metric gaming.** The model learns what the metric rewards. Check the gains with a second metric or with human judgments.

## Exercises

1. Prove $\partial R / \partial \ell_y = \alpha Q(y) (\Delta_y - R)$. *Hint:* $\partial Q(y') / \partial \ell_y = \alpha Q(y') ([y = y'] - Q(y))$.
2. Show that if all candidates in $S(x)$ have the same loss, the gradient is 0 whatever the probabilities. *Answer:* then $\Delta_y = R$ for every $y$.
3. In the hand example with $\alpha = 1$, one gradient step with a small rate $\eta$ on the $\ell_y$ directly changes them by $-\eta g$. Which candidate gains probability? *Answer:* the first, the only one with a loss below $R = 0.35$.
4. Show that for $\alpha = 1$ and $S(x)$ equal to all outputs, the gradient is $\mathbb{E}_{P}[(\Delta - R) \nabla \ell]$, the REINFORCE gradient with the baseline $R$.

## References
