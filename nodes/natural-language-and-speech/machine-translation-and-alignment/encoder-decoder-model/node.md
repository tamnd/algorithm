---
tag: PJCW26
kind: model
slug: encoder-decoder-model
name: Encoder-decoder model
aliases:
- sequence-to-sequence model
- seq2seq
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: One network encodes the source sequence into vectors and another generates the target sequence one token at a time from them.
history:
  year: 2014
  people: [Ilya Sutskever, Oriol Vinyals, Quoc V. Le, Kyunghyun Cho, Yoshua Bengio]
  note: In 2014 Cho et al. scored phrase pairs with an RNN encoder-decoder inside a phrase-based system, and Sutskever, Vinyals and Le translated whole sentences with two LSTMs.
prereqs: [recurrent-neural-network-language-model, machine-translation, cross-entropy-loss]
see_also: [additive-attention, multiplicative-attention, transformer, beam-search, teacher-forcing, exposure-bias, inadequacy-of-the-mode, listen-attend-and-spell]
sources:
  - paper: arxiv:1409.3215
    title: Ilya Sutskever, Oriol Vinyals and Quoc V. Le, Sequence to Sequence Learning with Neural Networks, Advances in Neural Information Processing Systems 27 (NIPS 2014), pages 3104 to 3112
    locator: "abstract (an LSTM encoder and an LSTM decoder; 34.8 BLEU against 33.3 for a phrase-based system on WMT'14 English to French; 36.5 when reranking 1000 hypotheses; reversing the source helps)"
  - paper: arxiv:1406.1078
    title: Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk and Yoshua Bengio, Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation, EMNLP 2014, pages 1724 to 1734
    locator: "the RNN Encoder-Decoder, trained to maximize the conditional probability of the target given the source, and its use as a feature of a log-linear phrase-based system"
  - paper: arxiv:1409.0473
    title: Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio, Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015
    locator: "Section 1 and Section 5 (the fixed-length vector as a bottleneck on long sentences, and attention as the remedy)"
---

An encoder-decoder model is a neural network that maps an input sequence to an output sequence of a different length. The encoder reads the source tokens and produces vectors. The decoder is a conditional [language model](/language-model/): it generates the target one token at a time, each token conditioned on the earlier target tokens and on the encoder output. It is the model behind neural machine translation, and also behind summarization, speech recognition and many other tasks. The first versions (Cho et al. 2014; Sutskever, Vinyals and Le 2014) used recurrent networks and passed one fixed-length vector from the encoder to the decoder. [Attention](/additive-attention/) and then the [transformer](/transformer/) replaced the single vector by access to all the encoder states.

## The machine

The input is a source sequence $x = x_1, \ldots, x_I$ over a source vocabulary of size $V_s$, and the output is a target sequence $y = y_1, \ldots, y_J$ over a target vocabulary of size $V_t$ that contains an end symbol $\langle\mathrm{eos}\rangle$, with $y_J = \langle\mathrm{eos}\rangle$. The model factors the conditional probability by the chain rule:

$$P(y \mid x; \theta) = \prod_{j=1}^{J} p(y_j \mid y_1, \ldots, y_{j-1}, x; \theta).$$

The recurrent version of Sutskever, Vinyals and Le has these layers, with embedding size $e$ and state size $d$:

- **Embeddings.** $E_s \in \mathbb{R}^{e \times V_s}$ and $E_t \in \mathbb{R}^{e \times V_t}$ map each token to a column vector in $\mathbb{R}^e$.
- **Encoder.** $h_i = f_{\mathrm{enc}}(h_{i-1}, E_s x_i) \in \mathbb{R}^d$ for $i = 1, \ldots, I$, with $h_0 = 0$, where $f_{\mathrm{enc}}$ is an LSTM or GRU cell, possibly with several layers.
- **Context.** $c = h_I \in \mathbb{R}^d$, the last encoder state. This is the fixed-length vector.
- **Decoder.** $s_0 = c$ and $s_j = f_{\mathrm{dec}}(s_{j-1}, E_t y_{j-1}) \in \mathbb{R}^d$, with $y_0$ a start symbol. Cho et al. also feed $c$ into every decoder step.
- **Output.** $p(\cdot \mid y_{<j}, x) = \mathrm{softmax}(W_o s_j + b_o)$ with $W_o \in \mathbb{R}^{V_t \times d}$ and $b_o \in \mathbb{R}^{V_t}$.

With attention, the context changes at each step: $c_j = \sum_i \alpha_{j,i} h_i$, where the weights come from a score of the decoder state and each $h_i$ ([additive attention](/additive-attention/), [multiplicative attention](/multiplicative-attention/)). In the [transformer](/transformer/), self-attention layers replace the recurrence in both parts, and cross-attention from the decoder to the encoder output replaces the context vector.

Standing assumptions: fixed vocabularies (usually subword units from [byte-pair encoding](/byte-pair-encoding/)), output from left to right with an end symbol, and parameters trained by maximum likelihood, that is by the [cross-entropy loss](/cross-entropy-loss/) on the reference with [teacher forcing](/teacher-forcing/): the decoder gets the reference prefix $y_{<j}$, not its own outputs.

## What it counts

The model computes the probability $P(y \mid x; \theta)$ of any target sequence, or the log probability $\sum_j \log p(y_j \mid y_{<j}, x)$. This is a proper distribution over the finite sequences that end in $\langle\mathrm{eos}\rangle$ when the probability of never stopping is 0, which holds in practice but is not guaranteed by the factorization.

The cost of one evaluation of $\log P(y \mid x)$ for a given $y$ in the recurrent model with one layer is $\Theta(I (d^2 + d e))$ for the encoder, $\Theta(J (d^2 + d e))$ for the decoder states, and $\Theta(J d V_t)$ for the output softmax. The softmax term often dominates because $V_t$ is in the tens of thousands. Attention adds $\Theta(I J d)$. Training keeps the activations of all steps for [backpropagation through time](/backpropagation-through-time/), which takes $\Theta((I + J) d)$ numbers per layer plus $\Theta(J V_t)$ for the output distributions.

Generation is a search for a good $y$. [Greedy decoding](/greedy-decoding/) takes the most probable token at each step. [Beam search](/beam-search/) with beam $k$ costs $O(n k V_t)$ score evaluations for an output of length $n$, plus the selection of the top $k$. Neither is exact: the decoder state depends on the whole prefix, so the dynamic programming that decodes an HMM does not apply.

## Relation to other models

- **Language model.** A decoder with no encoder is an autoregressive [recurrent neural network language model](/recurrent-neural-network-language-model/). The encoder-decoder is a language model of the target conditioned on the source.
- **Noisy channel.** The [noisy channel translation model](/noisy-channel-translation-model/) of statistical translation scores $P(x \mid y) P(y)$ with separate translation and language models. The encoder-decoder models $P(y \mid x)$ directly, in one network.
- **Attention models.** [Additive attention](/additive-attention/) and [multiplicative attention](/multiplicative-attention/) keep the recurrent encoder and decoder and replace the single context vector by a weighted sum of all encoder states at each step.
- **Transformer.** The [transformer](/transformer/) is an encoder-decoder model with attention only. It computes all encoder states, and all decoder states in training, in parallel.
- **Non-autoregressive models.** [Non-autoregressive translation](/non-autoregressive-translation/) keeps the encoder but drops the dependence of each target token on the earlier ones, so it can emit all tokens at once.
- **Other tasks.** [Listen, attend and spell](/listen-attend-and-spell/) is an encoder-decoder for speech recognition, and the [pointer-generator network](/pointer-generator-network/) is one for summarization that can copy source words.

## Known results in the model

- **Factorization.** By the chain rule, every distribution over finite target sequences that end in $\langle\mathrm{eos}\rangle$ can be written as the product above (a theorem). The model restricts the distribution only through the size of the network and the vocabulary.
- **Bottleneck.** With one fixed-length context vector, translation quality drops on long sentences. Bahdanau, Cho and Bengio (2015) state this as the motivation for attention and show that RNNsearch keeps its quality on long sentences (a measurement on WMT'14 English to French).
- **First results.** On WMT'14 English to French, the deep LSTM model of Sutskever, Vinyals and Le reached 34.8 BLEU against 33.3 for a phrase-based baseline, and 36.5 when it reranked the 1000 best outputs of that baseline. Reversing the order of the source words improved the results (measurements, from the abstract). Cho et al. (2014) improved a phrase-based system by adding the phrase probabilities of the model as a feature (a measurement).
- **Exact decoding.** No polynomial algorithm is known that finds the most probable output of a recurrent decoder, and beam search can miss it. The search problem is the subject of [beam search](/beam-search/) and [length normalization](/length-normalization/).
- **The mode.** For trained translation models the most probable output can be the empty sequence, and a larger beam can make the outputs worse ([inadequacy of the mode](/inadequacy-of-the-mode/), a measurement on trained models, not a theorem).
- **Exposure bias.** Teacher forcing trains the decoder on reference prefixes, but at test time it sees its own outputs. The gap is called [exposure bias](/exposure-bias/); [minimum risk training](/minimum-risk-training/) and [scheduled sampling](/scheduled-sampling/) train on model outputs to reduce it (measured methods).

## References
