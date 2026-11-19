---
tag: FTCX13
kind: algorithm
slug: minimum-bayes-risk-decoding
name: Minimum Bayes risk decoding
aliases:
- MBR decoding
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: "Choose the candidate output with the least expected loss under the model, for a loss such as 1 - BLEU or the word error rate, often with the expectation estimated from model samples."
solves: [autoregressive-decoding]
model: word-ram
complexity:
  vars: {H: the number of candidates, N: the number of evidence outputs (samples or list entries), L: the cost of one call of the loss}
  time: {worst: "O(H N L)"}
  space: {extra: "O(H + N)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2000
  people: [Vaibhava Goel, William J. Byrne]
  note: Goel and Byrne 2000 formulated MBR decoding for speech recognition over N-best lists and lattices. Kumar and Byrne 2004 applied it to statistical machine translation, and Eikema and Aziz 2020 to neural translation with samples.
prereqs: [autoregressive-decoding, expected-value, loss-function]
see_also: [inadequacy-of-the-mode, confusion-network, word-error-rate, bleu, comet-metric, edit-distance, stochastic-beam-search, self-consistency-decoding]
sources:
  - paper: doi:10.1006/csla.2000.0138
    title: Vaibhava Goel and William J. Byrne, Minimum Bayes-risk automatic speech recognition, Computer Speech and Language 14(2), 2000, pages 115 to 135
    locator: the minimum Bayes risk decision rule under a general loss, and its approximation over N-best lists and lattices
  - url: https://aclanthology.org/N04-1022/
    title: Shankar Kumar and William Byrne, Minimum Bayes-risk decoding for statistical machine translation, HLT-NAACL 2004, pages 169 to 176
    locator: the MBR decoder over N-best lists with loss functions built from BLEU and other translation metrics
  - paper: doi:10.18653/v1/2020.coling-main.398
    title: Bryan Eikema and Wilker Aziz, Is MAP decoding all you need? The inadequacy of the mode in neural machine translation, COLING 2020, pages 4506 to 4520
    locator: sampling based MBR, with unbiased samples of the model as both candidates and pseudo references
---

Minimum Bayes risk (MBR) decoding picks the output that is best on average, not the output that is most probable. Given a model $p(y \mid x)$ and a loss $\ell(h, y)$ that says how bad it is to output $h$ when the right answer is $y$, it returns the candidate $h$ of least expected loss $\sum_y p(y \mid x) \, \ell(h, y)$. With the 0-1 loss this is the most probable output, so MBR generalizes MAP decoding. With a loss that gives partial credit, such as the [word error rate](/word-error-rate/) or $1 - $ [BLEU](/bleu/), it prefers an output that agrees with many probable outputs over a single probable outlier. The sum runs over all outputs, so in practice it is estimated: over an N-best list or a lattice in older systems, and over samples from the model in neural ones. The decision rule is exact for the candidates and the evidence it is given; whether it improves quality is a measurement.

## In plain words

The model gives many possible answers, each with a chance of being right. The most likely single answer can still be a bad bet, for example if the other answers all agree with each other and not with it. MBR decoding asks, for each candidate: if I output this, how wrong will I be on average, counting each possible right answer by its chance? It then outputs the candidate with the smallest average error. If you only count exact matches, this is the most likely answer. If near misses count as partly right, it is often a different, safer answer.

## The problem

The input is a set $\mathcal{H}$ of $H$ candidates, a list $\mathcal{E}$ of evidence pairs $(y_j, w_j)$ with weights $w_j \ge 0$, and a loss $\ell(h, y) \ge 0$. The risk of a candidate is

$$R(h) = \sum_{j=1}^{N} w_j \, \ell(h, y_j),$$

and the task is $h^* = \arg\min_{h \in \mathcal{H}} R(h)$. Three common choices of the evidence:

- **The full distribution.** The evidence is every output with $w = p(y \mid x)$. Then $R(h)$ is the exact Bayes risk, which no system can compute for a neural model, because the outputs are too many.
- **A list.** The evidence is an N-best list or the paths of a [word lattice](/word-lattice/), with the model probabilities renormalized over the list.
- **Samples.** Draw $y_1, \ldots, y_N$ independently from $p(\cdot \mid x)$ and set $w_j = 1/N$. Then $R(h)$ is an unbiased Monte Carlo estimate of the true risk, and the distinct samples are usually also the candidates (Eikema and Aziz 2020).

The loss is often $1 - u(h, y)$ for a utility $u$ in $[0, 1]$ such as BLEU, [chrF](/chrf/) or [COMET](/comet-metric/), or the [edit distance](/edit-distance/) for speech recognition.

## The algorithm

```pseudo id=main
MBR-DECODE(H, E, ℓ)                  ▷ H = candidates, E = list of (y, w), ℓ = loss
    best ← none
L1  r* ← +∞
L2  for each h in H do
L3      r ← Σ over (y, w) in E of w · ℓ(h, y)
L4      if r < r* then (best, r*) ← (h, r)     ▷ ties: the first candidate wins
L5  return (best, r*)
```

The code has two front ends. One takes the evidence as log probabilities and normalizes them in log space with log-sum-exp, so that weights near $e^{-1000}$ do not underflow before the normalization. The other takes $N$ samples, uses the distinct samples as candidates and every sample as evidence with weight $1/N$, and so makes $N$ loss calls per distinct sample.

## Example

A model has four outputs with these probabilities, and the loss is the word [edit distance](/edit-distance/).

| output | words | $p$ |
|---|---|---|
| A | a b c | 7/25 |
| B | a b d | 6/25 |
| C | a e d | 6/25 |
| D | f b d | 6/25 |

The edit distances are $d(A, B) = 1$, $d(A, C) = 2$, $d(A, D) = 2$, $d(B, C) = 1$, $d(B, D) = 1$ and $d(C, D) = 2$. So

- $R(A) = (0 \cdot 7 + 1 \cdot 6 + 2 \cdot 6 + 2 \cdot 6) / 25 = 30/25 = 6/5$,
- $R(B) = (1 \cdot 7 + 0 + 1 \cdot 6 + 1 \cdot 6) / 25 = 19/25$,
- $R(C) = (2 \cdot 7 + 1 \cdot 6 + 0 + 2 \cdot 6) / 25 = 32/25$,
- $R(D) = (2 \cdot 7 + 1 \cdot 6 + 2 \cdot 6 + 0) / 25 = 32/25$.

MBR decoding returns B, with an expected edit distance of $19/25 = 0.76$ words. The most probable output A has an expected edit distance of $1.2$. Under the 0-1 loss the risks are $1 - p$, so A wins with $18/25$, as MAP decoding would. B is the output that shares the most with all the others: it is one edit away from each of them.

With 2000 samples from this model (seed 5 in the test), sampling based MBR also returns B, with an estimated risk within 0.05 of $19/25$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It proves that the algorithm returns a candidate of least risk, the first one on ties, and that scaling all weights by a positive constant does not change the choice, so the weights need not be normalized. It proves that with the 0-1 loss and the full distribution as evidence, MBR over all outputs is MAP decoding. And it proves that with $N$ independent samples as evidence the estimated risk of each fixed candidate is unbiased and converges to the true risk by the [law of large numbers](/law-of-large-numbers/), so for a finite candidate set with a unique minimizer the sampled decision is the exact MBR decision with probability tending to 1.

What is not a theorem: that the MBR output is a better text. That is a measurement on a task with a metric, and it holds best when the loss used in decoding is the metric used in evaluation.

## Complexity

Each candidate needs $N$ loss calls, so the time is $O(H N L)$ in the word RAM, for a loss call of cost $L$. With the samples as candidates, $H \le N$, and the cost is $O(N^2 L)$: 30 samples need up to 900 calls, and the test counts exactly $30 \times (\text{distinct samples})$ calls. For the word edit distance between outputs of $n$ words, $L = O(n^2)$ by the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/); a neural metric such as COMET costs a network call per pair. The space is $O(H + N)$ outputs, plus the work space of the loss.

Drawing the $N$ samples costs $N$ decodes of the model, which is often more than the loss calls for string metrics. Over a lattice, the expected loss under the edit distance has no simple closed form, and systems approximate it, for example with a [confusion network](/confusion-network/).

## Properties

- **Exact for its inputs** (a theorem). The output is a minimizer of the given risk over the given candidates.
- **MAP as a special case** (a theorem). The 0-1 loss with the full distribution gives the most probable output.
- **Consistent with samples** (a theorem). The sample estimate of each risk is unbiased and converges.
- **Not tied to the mode.** A candidate can win without being probable, if it is close to many probable outputs. That avoids the failure of the mode described in [inadequacy of the mode](/inadequacy-of-the-mode/), where the most probable output can be empty.
- **Quadratic cost** in the number of samples.

## Variants and improvements

- **Lattice and N-best MBR.** Goel and Byrne 2000 and Kumar and Byrne 2004 work on N-best lists and lattices from a beam decoder, with the probabilities renormalized over the list.
- **Consensus decoding.** For the word error rate, align the lattice into a [confusion network](/confusion-network/) and take the best word in each slot. This minimizes an approximation to the expected word error at a much lower cost.
- **Separate candidates and evidence.** Draw candidates from beam search, and evidence from unbiased samples; or draw candidates from [nucleus sampling](/nucleus-sampling/) and evidence from the model. The candidate set should hold good outputs, while the evidence should represent the model.
- **Cheaper risk.** Prune candidates with a cheap loss before scoring the survivors with an expensive one, or compare each candidate with the average of the evidence in an embedding space, which makes the cost linear in $N$ for metrics that allow it.
- **Self-consistency.** For answers with a single final value, [self-consistency decoding](/self-consistency-decoding/) is MBR with the 0-1 loss on the final answer over sampled reasoning paths: the majority vote.

## When to use it

Use MBR decoding when you know the metric that will judge the output, the model is not sharp, and you can afford $N$ samples and up to $N^2$ metric calls: translation with a strong metric, speech recognition with word error rate, or summarization. Do not use it for a single short label, where the most probable answer and the MBR answer agree, or under a tight latency budget.

## Pitfalls

- **The loss defines the answer.** MBR optimizes the loss you give it, including its blind spots. A neural metric used both to decode and to evaluate inflates the evaluation score; evaluate with a different metric too.
- **Biased evidence.** Samples from a truncated or low temperature sampler, or a beam N-best list, are not unbiased samples of the model. The risk is then the risk under a different distribution. Say which one you use.
- **Too few samples.** With small $N$ the risk estimates are noisy, and the choice can change from run to run. Report $N$ and the seed.
- **Unnormalized log weights.** Exponentiating raw log probabilities of long outputs underflows to 0 for every candidate. Normalize in log space first.
- **Utilities versus losses.** BLEU is a utility; MBR minimizes $1 - $ BLEU, or maximizes the expected BLEU. Mixing the two signs picks the worst candidate.

## Implementations

The code takes the candidates, the evidence and their model scores as given, and implements the decision rule and the sample based front end; it does not run or train a network.

## History

Bayes decision theory gives the rule directly: the action of least expected loss under the posterior. Goel and Byrne 2000 made it a decoder for speech recognition over N-best lists and lattices, with the word error rate as the loss. Kumar and Byrne 2004 applied it to statistical translation with BLEU and other metrics. Neural translation used beam search for years; Eikema and Aziz 2020 argued that the mode of a neural translation model is often inadequate, and that MBR over unbiased samples is a better use of the model, which renewed interest in the method.

## References
