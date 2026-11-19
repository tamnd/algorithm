---
tag: 3JXDQW
kind: model
slug: pointer-generator-network
name: Pointer-generator network
aliases:
- copy mechanism
- CopyNet
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: An encoder-decoder that at each step mixes generating a word from the vocabulary with copying a source word through its attention weights.
history:
  year: 2017
  people: [Abigail See, Peter J. Liu, Christopher D. Manning]
  note: See, Liu and Manning at Stanford and Google Brain published the pointer-generator network with a coverage loss at ACL 2017, for abstractive summarization of the CNN and Daily Mail news stories.
prereqs: [encoder-decoder-model, additive-attention, cross-entropy-loss]
see_also: [automatic-summarization, rouge, beam-search, teacher-forcing, exposure-bias, transformer, textrank, lexrank]
sources:
  - paper: doi:10.18653/v1/P17-1099
    title: Abigail See, Peter J. Liu and Christopher D. Manning, Get To The Point, Summarization with Pointer-Generator Networks, ACL 2017, pages 1073 to 1083
    locator: "Section 2.1 (the attention baseline), Section 2.2 (equations 8 and 9, the generation probability and the final distribution), Section 2.3 (equations 10 to 13, coverage and the coverage loss), Table 1 (ROUGE on CNN and Daily Mail)"
  - paper: "Oriol Vinyals, Meire Fortunato and Navdeep Jaitly, Pointer Networks, Advances in Neural Information Processing Systems 28 (NIPS 2015)"
    title: Vinyals, Fortunato and Jaitly 2015
    locator: the attention distribution used as the output distribution over input positions
  - paper: "Jiatao Gu, Zhengdong Lu, Hang Li and Victor O.K. Li, Incorporating Copying Mechanism in Sequence-to-Sequence Learning, ACL 2016, pages 1631 to 1640"
    title: Gu, Lu, Li and Li 2016 (CopyNet)
    locator: the copy mode and the generate mode with a shared normalization
---

A pointer-generator network is an [encoder-decoder model](/encoder-decoder-model/) with [attention](/additive-attention/) that can either generate a word from a fixed vocabulary or copy a word from the source text. At each output step it computes a number $p_{\mathrm{gen}}$ between 0 and 1, and its output distribution is $p_{\mathrm{gen}}$ times the vocabulary distribution plus $1 - p_{\mathrm{gen}}$ times the attention distribution over the source positions. So it can write rare names and numbers that are not in the vocabulary, by pointing at them. Abigail See, Peter Liu and Christopher Manning introduced it in 2017 for abstractive [summarization](/automatic-summarization/), together with a coverage mechanism that discourages the model from attending to the same source words again, which reduces repetition. The aliases name the general idea: "copy mechanism" is the family of methods, and CopyNet (Gu, Lu, Li and Li 2016) is a different model of the same family, with its own copy and generate scores.

## The machine

The source is a sequence of tokens $w_1, \ldots, w_n$. A bidirectional LSTM encoder gives hidden states $h_1, \ldots, h_n$. At output step $t$, the decoder LSTM has state $s_t$ and reads the embedding $x_t$ of the previous output word. The parts of the model, in the notation of the paper:

- **Attention (Section 2.1).** $e_i^t = v^{\mathsf T} \tanh(W_h h_i + W_s s_t + b_{\mathrm{attn}})$ and $a^t = \mathrm{softmax}(e^t)$, a distribution over the $n$ source positions. The context vector is $h_t^* = \sum_i a_i^t h_i$.
- **Vocabulary distribution.** $P_{\mathrm{vocab}} = \mathrm{softmax}(V'(V[s_t; h_t^*] + b) + b')$, over a fixed vocabulary.
- **Generation probability (equation 8).** $p_{\mathrm{gen}} = \sigma(w_{h^*}^{\mathsf T} h_t^* + w_s^{\mathsf T} s_t + w_x^{\mathsf T} x_t + b_{\mathrm{ptr}})$, where $\sigma$ is the logistic function.
- **Final distribution (equation 9).** Over the extended vocabulary, the fixed vocabulary together with the words of this source,
$$P(w) = p_{\mathrm{gen}}\, P_{\mathrm{vocab}}(w) + (1 - p_{\mathrm{gen}}) \sum_{i : w_i = w} a_i^t,$$
with $P_{\mathrm{vocab}}(w) = 0$ for a word outside the vocabulary and an empty sum for a word not in the source.
- **Coverage (equations 10 and 11).** The coverage vector $c^t = \sum_{t' < t} a^{t'}$ is the sum of the earlier attention distributions, and the attention score gets an extra term: $e_i^t = v^{\mathsf T}\tanh(W_h h_i + W_s s_t + w_c c_i^t + b_{\mathrm{attn}})$.
- **Loss (equations 12 and 13).** With the reference word $w_t^*$, the loss at step $t$ is
$$\mathrm{loss}_t = -\log P(w_t^*) + \lambda \sum_i \min(a_i^t, c_i^t),$$
and the loss of a sequence is the mean over its steps. The paper uses $\lambda = 1$.

Training uses [teacher forcing](/teacher-forcing/) on pairs of articles and summaries. At test time the summary is decoded with [beam search](/beam-search/) on $P(w)$. A word copied from the source and outside the vocabulary is fed back to the decoder as the unknown word token.

## What it counts

One decoding step costs the LSTM update, $O(nh)$ for the attention over $n$ source positions with hidden size $h$, $O(Vh)$ for the vocabulary softmax with $V$ words, and $O(n)$ more to add the copy probabilities into the extended vocabulary. The copy part adds only $O(n + h)$ to a step of the attention model, and its parameters are the vectors $w_{h^*}$, $w_s$, $w_x$, the scalar $b_{\mathrm{ptr}}$, and $w_c$ for coverage.

Two small facts follow from the definitions; they are theorems.

- **The output is a distribution.** $P_{\mathrm{vocab}}$ and $a^t$ are distributions, so $\sum_w P(w) = p_{\mathrm{gen}} \cdot 1 + (1 - p_{\mathrm{gen}}) \sum_i a_i^t = 1$. A word that is both in the vocabulary and in the source gets probability from both parts, and a word that occurs several times in the source gets the attention of all its positions.
- **The coverage loss is bounded.** At each step $0 \le \sum_i \min(a_i^t, c_i^t) \le \sum_i a_i^t = 1$. It is 0 exactly when step $t$ puts no attention on a position that earlier steps attended to. So the sum of the coverage loss over a summary is 0 exactly when the attention distributions of all steps have disjoint supports, and it is at most the number of steps.

## Relation to other models

- **Encoder-decoder with attention.** With $p_{\mathrm{gen}} = 1$ the model is the attention baseline of Section 2.1.
- **Pointer networks.** Vinyals, Fortunato and Jaitly (2015) used the attention distribution itself as the output distribution over input positions, for problems such as convex hulls and the traveling salesman problem, where the output is a sequence of input positions. With $p_{\mathrm{gen}} = 0$ the pointer-generator network is a pointer network.
- **CopyNet.** Gu, Lu, Li and Li (2016) give scores to a generate mode and a copy mode and normalize them together in one softmax, so there is no explicit switch. It is a different model, listed here as an alias because the two are often named together.
- **Other switches.** Gulcehre and colleagues (2016) and Nallapati and colleagues (2016) used a hard switch between pointing and generating, trained with labels that say when the word was copied. The pointer-generator network uses a soft switch, learned end to end, and needs no such labels.
- **Coverage.** Tu and colleagues (2016) introduced coverage for machine translation. The pointer-generator network adds the coverage loss, which penalizes attention that overlaps with the coverage vector.
- **Extractive methods.** [TextRank](/textrank/) and [LexRank](/lexrank/) select whole sentences. The pointer-generator network writes new text, but in practice it copies much of it.

## Known results in the model

These are measurements on the non-anonymized CNN and Daily Mail data set, scored with [ROUGE](/rouge/) F1 (Table 1 of the paper).

| model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---|---|---|
| pointer-generator | 36.44 | 15.66 | 33.42 |
| pointer-generator with coverage | 39.53 | 17.28 | 36.38 |
| lead-3 baseline (the first three sentences) | 40.34 | 17.70 | 36.57 |

- **Coverage helps.** Adding coverage raised all three scores by about 3 points, and the paper reports that it removed most of the repetition of the models without it.
- **Lead-3 is hard to beat.** The simple baseline of the first three sentences scores higher than the model on ROUGE. The paper attributes this to the structure of news articles, where the main facts come first.
- **Training schedule.** The model was trained for about 230,000 iterations, and coverage was added for a further 3,000 iterations at the end. The paper reports that training with coverage from the start did not work as well.
- **The model copies a lot.** On the test set the mean of $p_{\mathrm{gen}}$ was 0.17, so most of the probability goes to copying. The summaries contain fewer new n-grams than the reference summaries.
- **Later work.** Transformer based pretrained models such as BART and PEGASUS score higher on the same data. Copy mechanisms remain in use for data-to-text generation, dialogue and code, where exact names must be reproduced.

## References
