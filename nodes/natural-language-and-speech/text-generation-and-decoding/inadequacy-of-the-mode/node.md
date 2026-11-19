---
tag: MDP6S9
kind: concept
slug: inadequacy-of-the-mode
name: Inadequacy of the mode
aliases:
- beam search curse
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: "A measured fact: the most probable output of a neural translation model is often empty or too short, so wider beams and exact search can lower the quality."
prereqs: [autoregressive-decoding, beam-search]
see_also: [minimum-bayes-risk-decoding, length-normalization, greedy-decoding, stochastic-beam-search, map-inference, depth-first-branch-and-bound, exposure-bias, label-bias-problem]
sources:
  - paper: doi:10.18653/v1/D19-1331
    title: Felix Stahlberg and Bill Byrne, On NMT search errors and model errors, cat got your tongue?, EMNLP-IJCNLP 2019, pages 3356 to 3362
    locator: exact search on a Transformer translation model, where the empty translation is the most probable one for more than half of the test sentences
  - paper: doi:10.18653/v1/W17-3204
    title: Philipp Koehn and Rebecca Knowles, Six challenges for neural machine translation, First Workshop on Neural Machine Translation, 2017, pages 28 to 39
    locator: the challenge of beam search, where the quality drops for wide beams
  - paper: doi:10.18653/v1/2020.coling-main.398
    title: Bryan Eikema and Wilker Aziz, Is MAP decoding all you need? The inadequacy of the mode in neural machine translation, COLING 2020, pages 4506 to 4520
    locator: the argument that the mode is a poor summary of the model, the comparison of beam outputs and unbiased samples with the data, and sampling based MBR
  - paper: doi:10.18653/v1/W18-6322
    title: Kenton Murray and David Chiang, Correcting length bias in neural machine translation, Third Conference on Machine Translation (WMT), 2018, pages 212 to 223
    locator: the length bias of beam search, which makes outputs shorter as the beam grows
  - paper: doi:10.18653/v1/2020.emnlp-main.170
    title: Clara Meister, Ryan Cotterell and Tim Vieira, If beam search is the answer, what was the question?, EMNLP 2020
    locator: beam search as exact search under a regularized objective, which explains why inexact search can give better text than the mode
---

The inadequacy of the mode is the measured observation that, for neural text models, the single most probable output is often a bad output. The standard decoder of translation and speech recognition looks for the mode, $\arg\max_y p(y \mid x)$, with [beam search](/beam-search/). If beam search were only an approximation to a good target, a wider beam, or exact search, should give better outputs. In neural machine translation it does not: Koehn and Knowles 2017 measured that the quality drops for wide beams, and Stahlberg and Byrne 2019 found, with exact search on a Transformer model for English to German, that the empty translation was the most probable one for more than half of the test sentences. So the good results of beam search depend on its search errors, and the problem is in the model's distribution, not only in the search. These are measurements on particular models and data sets, not theorems.

## In plain words

A translation model gives every possible sentence a chance. You might expect the sentence with the largest chance to be the best translation. Experiments show that it often is not. Sometimes the most likely output is an empty sentence. The reason is that the chance is spread over many good translations that differ a little, so each one gets a small share. A single bad output, such as an empty one, can get a larger share than any one good translation, even though all the good ones together get much more.

## The idea

The probability of an output is a product of per-token probabilities, each at most 1. Two effects follow.

**Mass spread over many good outputs.** A source sentence has many good translations that differ in word choice and order. The model spreads its mass over all of them, so each gets a small share. A degenerate output that is not split this way, such as the empty output, can have more mass than any single good one, while the good outputs together have most of the mass. The mode then answers the question "which single output is most probable", which is not the question "what does the model think the translation looks like".

**Shorter is more probable.** Each extra token multiplies the probability by a number at most 1, so the log probability of a prefix never goes up. Among outputs of similar per-token quality, shorter ones score higher. [Length normalization](/length-normalization/) and a word reward (Murray and Chiang 2018) correct the score of the outputs that the beam finds, but they do not change the mode of the model.

Why beam search works at all is then a separate question. A narrow beam cannot find the empty or very short outputs that a wider search would find, because it commits early to probable first tokens. Meister, Cotterell and Vieira 2020 show that beam search is exact search for a different objective, one with a term that rewards an even spread of the surprisal over the tokens, and argue that this bias, not closeness to the mode, is what makes its outputs good. This explanation is an argument supported by measurements.

The practical answer that follows is to stop using the mode as the summary of the model. [Minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) picks the output that agrees most with the model's whole distribution under a loss, and Eikema and Aziz 2020 measured that unbiased samples of the model reproduce statistics of the data that beam outputs do not, and proposed MBR over samples.

## Examples

**A toy model.** Let a model put probability $0.1$ on the empty output and spread $0.9$ evenly over $1024$ sentences of ten words, where each of the ten positions has two equally good word choices. Each sentence has probability $0.9 / 1024 = 0.00087890625$, so the mode is the empty output, with more than 100 times the probability of any single sentence. Now score each output by its expected loss, where the loss between two ten-word sentences is the number of positions at which they differ, and the loss between the empty output and any sentence is 10. The empty output has risk $0.9 \times 10 = 9$. A sentence has risk $0.1 \times 10 + 0.9 \times 5 = 5.5$, since a random sentence differs from it at 5 positions on average. So the MBR choice is a sentence, and the mode is the worst choice under this loss.

**The measurements.** Stahlberg and Byrne 2019 ran exact search by [depth-first branch and bound](/depth-first-branch-and-bound/) on a Transformer base model trained on WMT English to German data, and the empty translation was the most probable output for more than half of the sentences of their test set. Koehn and Knowles 2017 measured that, for several language pairs, the BLEU score first rises and then falls as the beam widens, most strongly without length normalization. Murray and Chiang 2018 relate the drop to outputs that get shorter as the beam widens.

## Where it is used

- **Choosing a decoder.** It is the main argument for [MBR decoding](/minimum-bayes-risk-decoding/) and for sampling based decoders in translation, and for keeping beams narrow when beam search is used.
- **Length corrections.** It explains why systems need [length normalization](/length-normalization/) or a word reward, and why these do not fully fix wide beams.
- **Separating errors.** It splits decoding errors into search errors, where the decoder misses the mode, and model errors, where the mode itself is bad. Exact search measures the second kind.
- **Open text generation.** Practitioners observe that maximizing the probability of long text gives dull and repetitive output, which is one reason why generators sample with [nucleus sampling](/nucleus-sampling/) or [temperature](/temperature-sampling/) instead of searching for the mode.

## References
