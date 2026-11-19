---
tag: AP6ENR
kind: technique
slug: length-normalization
name: Length normalization
aliases:
- length penalty
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: Divide the log probability of each finished beam hypothesis by a function of its length, such as |Y|^alpha, so that beam search does not prefer short outputs.
prereqs: [beam-search, language-model, autoregressive-decoding]
see_also: [inadequacy-of-the-mode, greedy-decoding, minimum-bayes-risk-decoding, diverse-beam-search, machine-translation, encoder-decoder-model, perplexity, exposure-bias]
sources:
  - url: https://arxiv.org/abs/1609.08144
    title: Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V. Le, Mohammad Norouzi and others, Google's neural machine translation system, bridging the gap between human and machine translation, arXiv 1609.08144, 2016
    locator: Section 7, the length penalty lp(Y) = ((5 + |Y|) / 6)^alpha and the coverage penalty in Equation 14
  - paper: doi:10.18653/v1/W18-6322
    title: Kenton Murray and David Chiang, Correcting length bias in neural machine translation, Third Conference on Machine Translation (WMT), 2018, pages 212 to 223
    locator: the length bias of beam search, and a per-word reward tuned on held-out data
  - paper: doi:10.18653/v1/W17-3204
    title: Philipp Koehn and Rebecca Knowles, Six challenges for neural machine translation, First Workshop on Neural Machine Translation, 2017, pages 28 to 39
    locator: the challenge of beam search, where wider beams lower the translation quality, also with normalized scores
  - paper: doi:10.18653/v1/2020.emnlp-main.170
    title: Clara Meister, Ryan Cotterell and Tim Vieira, If beam search is the answer, what was the question?, EMNLP 2020
    locator: beam search as the solution of a regularized decoding objective, and the role of the length of the output
---

Length normalization changes the score that [beam search](/beam-search/) uses to compare finished hypotheses. The raw score of an output $Y$ is $\log p(Y \mid X) = \sum_t \log p(y_t \mid y_{<t}, X)$, a sum of terms that are all at most 0. So every extra token lowers the score, and among finished outputs the raw score prefers short ones. Length normalization divides the score by a penalty that grows with the length: $s(Y) = \log p(Y \mid X) / \text{lp}(|Y|)$, with $\text{lp}(|Y|) = |Y|^\alpha$ or the GNMT penalty $\text{lp}(|Y|) = ((5 + |Y|) / 6)^\alpha$ of Wu et al. 2016. With $\alpha = 0$ this is the raw score, and with $\alpha = 1$ and the power form it is the mean log probability per token. The technique is a heuristic: it changes which output the decoder returns, and whether that output is better is a measurement on a task. The value of $\alpha$ is tuned on held-out data.

## In plain words

A model gives each next word a chance. The chance of a whole sentence is the product of these chances, so each extra word makes the total smaller. If the decoder simply picks the sentence with the largest total, it favors short sentences, sometimes far too short. Length normalization corrects this. It compares sentences by their score divided by a number that grows with the length, like an average per word. A single setting controls how strong the correction is; it is chosen by trying values on test data.

## When it applies

Use length normalization when a decoder compares complete outputs of different lengths by their total log probability, and those outputs come from a search, not from sampling. The typical case is beam search in [machine translation](/machine-translation/), speech recognition and summarization with an [encoder-decoder model](/encoder-decoder-model/). It does not apply to [greedy decoding](/greedy-decoding/), which compares tokens at one position only, or to sampling, which does not compare outputs at all.

## The template

The finished hypotheses of a beam search, as pairs (tokens, log probability), are reranked by the normalized score:

```pseudo id=main
RERANK(hyps, lp)                       ▷ hyps = list of (Y, log p(Y)), lp = the penalty
L1  best ← none
L2  for each (Y, s) in hyps do
L3      v ← s / lp(|Y|)
L4      if best = none or v > best.score then best ← (Y, v)    ▷ ties: the first one wins
L5  return best
```

The length $|Y|$ counts every predicted token, the end token "</s>" included. Toolkits differ on this point; whatever rule you use, use the same one everywhere.

Inside the beam search, open hypotheses are still ranked by their raw log probability, because all open hypotheses at one step have the same length. Only finished hypotheses are compared by $s(Y)$. The search can stop early with a bound: if lp is positive and does not decrease with the length, an open hypothesis with raw score $s \le 0$ can reach at most $s / \text{lp}(n_{\max})$ for a length limit $n_{\max}$, because its log probability can only go down and its penalty can grow at most to $\text{lp}(n_{\max})$. When no open hypothesis can beat the best finished one by this bound, the search stops. The proof is in [proofs/correctness.md](proofs/correctness.md), with the facts that RERANK returns a hypothesis of best normalized score and that a beam of unbounded width returns the best normalized output.

## Classic examples

**Two hypotheses.** A beam ends with SHORT, 3 tokens with log probability $-2.0$, and LONG, 8 tokens with log probability $-3.2$.

| penalty | SHORT | LONG | choice |
|---|---|---|---|
| none ($\alpha = 0$) | $-2.0$ | $-3.2$ | SHORT |
| $\vert Y\vert^{1}$ | $-0.6667$ | $-0.4$ | LONG |
| $\vert Y\vert^{0.6}$ | $-1.0346$ | $-0.9190$ | LONG |
| GNMT, $\alpha = 0.6$ | $-1.6829$ | $-2.0122$ | SHORT |
| GNMT, $\alpha = 1$ | $-1.5$ | $-1.4769$ | LONG |

The GNMT penalty grows more slowly with the length than $|Y|^\alpha$ for the same $\alpha$, because of the constant 5: $\text{lp}(1) = 1$, and $\text{lp}(10) = (15/6)^{0.6} = 1.732862$ at $\alpha = 0.6$, where $10^{0.6} = 3.98$. So the same $\alpha$ does not mean the same strength in the two forms.

**GNMT.** Wu et al. 2016 score a finished translation by $\log p(Y \mid X) / \text{lp}(Y) + \text{cp}(X; Y)$, with the coverage penalty $\text{cp}(X; Y) = \beta \sum_i \log \min(\sum_j p_{i,j}, 1)$, where $p_{i,j}$ is the attention weight of target word $j$ on source word $i$. The coverage term penalizes source words that received little attention. For two target words with attention rows $(0.7, 0.3, 0)$ and $(0.6, 0.3, 0.1)$ over three source words, the source words receive $1.3$, $0.6$ and $0.1$, and with $\beta = 0.2$ the coverage penalty is $0.2 (\log 1 + \log 0.6 + \log 0.1) = -0.5627$. The final GNMT system used $\alpha = \beta = 0.2$; a value of $\alpha$ between 0.6 and 0.7 was reported for an earlier form of the penalty, so do not copy one of these values to the other form.

**A word reward.** Murray and Chiang 2018 add a reward $r$ per word, $\log p(Y \mid X) + r |Y|$, and tune $r$ on held-out data. In the example, LONG wins when $-3.2 + 8 r > -2.0 + 3 r$, that is when $r > 0.24$.

## Variations

- **Power penalty** $|Y|^\alpha$, with $\alpha$ from 0 (no correction) to 1 (the mean log probability per token).
- **GNMT penalty** $((5 + |Y|) / 6)^\alpha$, with the coverage term $\text{cp}$ for attention models.
- **Word reward** $+ r |Y|$, an additive form. It can also be applied to open hypotheses during the search, since all of them get the same reward at one step.
- **Length ratio.** Penalize the gap between $|Y|$ and an expected length, for example a fixed ratio times the source length.
- **A length model.** Add $\log p(|Y| \mid X)$ from a separate predictor of the length.
- **Minimum length.** Forbid "</s>" before a minimum number of tokens, a hard constraint in place of a score change.

## Pitfalls

- **The bias comes back with wide beams.** Normalization fixes the comparison of the finished outputs that the beam finds, but a wider beam finds more short outputs to compare. Koehn and Knowles 2017 measured lower quality with very wide beams, most strongly without normalization, and also with it for several language pairs. The deeper cause is described in [inadequacy of the mode](/inadequacy-of-the-mode/).
- **Normalized scores are not monotone.** The raw log probability never increases when a token is added, but the normalized score can: with $\alpha = 1$, a hypothesis at $-1.0$ after one token goes to $(-1.0 + \log 0.9) / 2 \approx -0.553$ after two. So do not prune open hypotheses by their normalized score as if it were a bound.
- **Count the length the same way.** Counting "</s>" or not, and counting subword tokens or words, changes the effective $\alpha$.
- **Do not use underflowing probabilities.** Divide the log probability, not the probability. For 1000 tokens of probability 0.4 each, the probability is 0 in double precision, while the log probability is $-916.29$ and its mean is $\log 0.4$.
- **Tune per task and per model.** The best $\alpha$ depends on the model, the data and the beam width. Report it.

## Exercises

1. Show that the log probability of a prefix never increases when a token is added, and use it to explain why the raw score prefers short outputs.
2. For SHORT and LONG above, find the value of $\alpha$ at which the power penalty changes its choice. (Solve $-2.0 / 3^\alpha = -3.2 / 8^\alpha$.)
3. Prove the stopping bound of the template: if lp is positive and non-decreasing, an open hypothesis with raw score $s \le 0$ cannot reach a normalized score above $s / \text{lp}(n_{\max})$.
4. Show that the word reward and the power penalty with $\alpha = 1$ can choose different outputs from the same two hypotheses.

## References
