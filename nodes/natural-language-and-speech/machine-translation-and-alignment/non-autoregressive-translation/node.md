---
tag: T9EF3B
kind: model
slug: non-autoregressive-translation
name: Non-autoregressive translation
aliases:
- NAT
- mask-predict
area: natural-language-and-speech/machine-translation-and-alignment
level: research
summary: Generate all target tokens in parallel, or refine them over a few rounds, given a predicted length, trading quality for speed.
history:
  year: 2018
  people: [Jiatao Gu, James Bradbury, Caiming Xiong, Victor O. K. Li, Richard Socher]
  note: Gu et al. proposed the non-autoregressive transformer with fertilities at ICLR 2018. Ghazvininejad, Levy, Liu and Zettlemoyer added iterative refinement by mask-predict at EMNLP-IJCNLP 2019.
prereqs: [transformer, encoder-decoder-model, sequence-level-knowledge-distillation]
see_also: [masked-language-modeling, knowledge-distillation, fast-align, connectionist-temporal-classification, autoregressive-model, beam-search, bert, bleu]
sources:
  - paper: arxiv:1711.02281
    title: Jiatao Gu, James Bradbury, Caiming Xiong, Victor O. K. Li and Richard Socher, Non-Autoregressive Neural Machine Translation, ICLR 2018
    locator: "the fertility model, the multimodality problem, knowledge distillation from an autoregressive teacher, and noisy parallel decoding; the abstract gives the cost of as little as 2.0 BLEU, the order of magnitude lower latency, and 29.8 BLEU on WMT 2016 English to Romanian"
  - paper: doi:10.18653/v1/D19-1633
    title: Marjan Ghazvininejad, Omer Levy, Yinhan Liu and Luke Zettlemoyer, Mask-Predict - Parallel Decoding of Conditional Masked Language Models, EMNLP-IJCNLP 2019
    locator: "the conditional masked language model, the length prediction, and mask-predict decoding with a constant number of iterations; the abstract gives over 4 BLEU on average over earlier parallel decoders and about 1 BLEU below a left-to-right transformer"
---

A non-autoregressive translation model generates all the target tokens at once instead of one after another. An autoregressive [encoder-decoder model](/encoder-decoder-model/) conditions each token on all the earlier ones, so it needs as many sequential decoder steps as there are output tokens. A non-autoregressive model first fixes the output length, then predicts every position in parallel, with the tokens independent of each other given the source and the length. Gu et al. (2018) introduced the idea with a [transformer](/transformer/) and a latent fertility for each source token. Mask-predict (Ghazvininejad et al. 2019) runs a few rounds of parallel prediction, each time masking and predicting again the tokens the model is least sure of. These models trade some translation quality for a large cut in latency, and nearly all of them train on the output of an autoregressive teacher by [sequence-level knowledge distillation](/sequence-level-knowledge-distillation/).

## The machine

The input is a source sentence $x = x_1, \ldots, x_I$, and the output is a target sentence $y = y_1, \ldots, y_J$ over a vocabulary of size $V$. Both models below have a transformer encoder with model size $d$ and a decoder with no causal mask, so every decoder position attends to every other.

**Fertility model (Gu et al. 2018).** For each source position $i$, a softmax on the top encoder state predicts a fertility $f_i \in \{0, 1, \ldots, L\}$, the number of target tokens that source token accounts for. The length is $J = \sum_i f_i$. The decoder input is the source embeddings copied by fertility: $x_i$ is repeated $f_i$ times. The decoder outputs a distribution over $V$ at each of the $J$ positions. The model is

$$P(y \mid x) = \sum_{f} \prod_{i=1}^{I} p_F(f_i \mid x) \prod_{j=1}^{J} p(y_j \mid x, f), \qquad J = \sum_i f_i,$$

with the sum over the fertility sequences $f$ consistent with the length of $y$. In training, the fertilities come from an external word aligner such as [fast_align](/fast-align/), and the model is trained on the target sentences of an autoregressive teacher.

**Conditional masked language model (mask-predict).** A special length token in the encoder predicts the length $J$. The decoder gets the target with some positions replaced by a mask symbol, and predicts the masked tokens $Y_{\mathrm{mask}}$ from $x$ and the observed tokens $Y_{\mathrm{obs}}$:

$$p(Y_{\mathrm{mask}} \mid x, Y_{\mathrm{obs}}) = \prod_{j \in \mathrm{mask}} p(y_j \mid x, Y_{\mathrm{obs}}).$$

Training masks a random number of random positions, as in [masked language modeling](/masked-language-modeling/). Decoding with $T$ iterations:

1. Predict the length; start with every position masked, and predict all tokens in parallel.
2. For $t = 1, \ldots, T - 1$: mask again the $n = J (T - t) / T$ tokens with the lowest probability, rounded down, and predict them again from the rest.
3. Return the result. In practice several length candidates are decoded in parallel, and the output with the best average log probability is kept.

Standing assumptions: a fixed vocabulary, a length chosen before the tokens, and conditional independence of the tokens predicted in the same pass.

## What it counts

The fully parallel model assigns $\prod_j p(y_j \mid x, J)$ to a target of length $J$, and decoding takes the most probable token at each position independently, which is exact for this product: the argmax of a product of independent factors is the product of the argmaxes (a theorem). The cost of one pass is that of a transformer encoder and decoder: $\Theta(I^2 d + I d^2)$ and $\Theta(J^2 d + J I d + J d^2)$ per layer, plus $\Theta(J d V)$ for the output layer. All of the decoder work is one parallel pass, so the number of sequential decoder steps is 1, or $T$ for mask-predict, instead of $J$. Gu et al. report an order of magnitude lower latency than their autoregressive teacher (a measurement on their hardware). With noisy parallel decoding, which samples $m$ fertility sequences, decodes them in parallel and lets the teacher rescore them, the work grows by a factor $m$ but the latency stays nearly the same.

## Relation to other models

- **Autoregressive models.** The [encoder-decoder model](/encoder-decoder-model/) factors $P(y \mid x)$ by the chain rule, with no independence assumption, and decodes with [beam search](/beam-search/) in $J$ sequential steps. The non-autoregressive model drops the dependence on earlier tokens to gain parallel decoding.
- **Masked language models.** The conditional masked language model is the training objective of [BERT](/bert/) applied to the decoder, conditioned on a source sentence.
- **CTC.** [Connectionist temporal classification](/connectionist-temporal-classification/) also predicts all output labels in parallel with independent frames, and handles the length with blanks and merging instead of a length predictor. Some later non-autoregressive translation models use a CTC loss.
- **Knowledge distillation.** [Sequence-level knowledge distillation](/sequence-level-knowledge-distillation/) from an autoregressive teacher is part of the training of nearly every model in this family.
- **Iterative refinement.** Mask-predict sits between the two extremes: with $T = 1$ it is fully parallel, and with $T = J$ and one token per round it predicts one token at a time, though not left to right.

## Known results in the model

- **Independence cannot represent correlated outputs.** A product distribution over two positions that gives positive probability to "ab" and to "ba" also gives positive probability to "aa" and to "bb" (a theorem: $p_1(a) p_2(a) > 0$ follows from $p_1(a) p_2(b) > 0$ and $p_1(b) p_2(a) > 0$). This is the multimodality problem of Gu et al.: when a source has two good translations, the parallel model mixes them and can output a word from each, or repeat a word.
- **Distillation reduces the problem.** The outputs of an autoregressive teacher are more consistent than human references, so the target distribution has fewer modes. Gu et al. measured a substantial gain from distillation as one of the three parts of their training, and later non-autoregressive models keep it (measurements).
- **Quality and speed.** Gu et al. report a cost of as little as 2.0 BLEU against their autoregressive teacher and 29.8 BLEU on WMT 2016 English to Romanian with noisy parallel decoding (measurements, from the abstract).
- **Iterative refinement.** Mask-predict with a constant number of iterations improved on earlier non-autoregressive and parallel decoders by over 4 BLEU on average, and reached within about 1 BLEU of a typical left-to-right transformer while decoding faster (measurements, from the abstract).
- **Typical errors.** Repeated tokens and dropped tokens are the common errors of fully parallel models; they follow from the independence assumption and are measured to fall with more refinement iterations and with distillation.
- **Speed depends on the setting.** The gain in latency is largest for one sentence at a time on a parallel device. With large batches an autoregressive model also keeps the device busy, and the advantage is smaller (a measurement that depends on the hardware and the batch size).

## References
