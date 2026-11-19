---
tag: PD9FA6
kind: model
slug: bilstm-crf
name: BiLSTM-CRF
aliases:
- BiLSTM-CRF tagger
- neural CRF tagger
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "A bidirectional LSTM gives each token tag scores, and a linear-chain CRF layer on top adds tag transitions and decodes by Viterbi."
history:
  year: 2015
  people: [Zhiheng Huang, Wei Xu, Kai Yu, Guillaume Lample, Chris Dyer]
  note: "Huang, Xu and Yu applied a bidirectional LSTM with a CRF layer to tagging, chunking and NER in 2015. Lample et al. (2016) added character-level word representations and used no hand-made features."
prereqs: [conditional-random-field, backpropagation-through-time, word-embedding]
see_also: [sequence-labeling, named-entity-recognition, bio-encoding, structured-perceptron, maximum-entropy-markov-model, recurrent-neural-network-language-model, bert, dropout]
sources:
  - paper: "Zhiheng Huang, Wei Xu and Kai Yu, Bidirectional LSTM-CRF models for sequence tagging, arXiv:1508.01991, 2015"
    title: "Huang, Xu and Yu 2015"
    locator: "Section 2 (LSTM, BI-LSTM, CRF, LSTM-CRF and BI-LSTM-CRF; the sentence score as the sum of transition and network scores, Equation 5), Table 2 (POS, CoNLL-2000 and CoNLL-2003 results), Section 4.3.2 and Table 3 (results with word features only)"
  - paper: "Guillaume Lample, Miguel Ballesteros, Sandeep Subramanian, Kazuya Kawakami and Chris Dyer, Neural architectures for named entity recognition, Proceedings of NAACL-HLT 2016, pages 260 to 270"
    title: Lample et al. 2016
    locator: "Section 2.2 (the score s(X, y), the softmax over all tag sequences, Equations 1 and 2), Section 2.4 (IOB and IOBES), Section 4 (character-based word representations, pretrained embeddings, dropout), Section 5.3 and Tables 1 to 4 (CoNLL-2002 and CoNLL-2003 results), Section 5.4 and Table 5 (ablation)"
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pages 282 to 289"
    title: "Lafferty, McCallum and Pereira 2001"
    locator: the linear-chain CRF used as the output layer
---

A BiLSTM-CRF is a neural sequence tagger in two layers. A bidirectional LSTM, a recurrent network read once from left to right and once from right to left, turns each token into a vector that depends on the whole sentence and gives a score for each tag at each position. A linear-chain [conditional random field](/conditional-random-field/) on top adds a learned score for each pair of adjacent tags and normalizes over whole tag sequences. Compared with a plain CRF, the token scores are learned from words and characters instead of hand-made features. Compared with a BiLSTM that picks each tag on its own with a softmax, the CRF layer scores tag pairs, so it can learn constraints such as "I-PER does not follow B-LOC", and it decodes with the [Viterbi algorithm](/viterbi-algorithm/).

## The machine

The input is a sentence $X = (x_1, \ldots, x_n)$ and a tag set of size $k$.

**Word representations.** Each word gets a vector from an embedding table, usually pretrained ([word embedding](/word-embedding/)). Lample et al. (2016, Section 4.1) also run a bidirectional LSTM over the characters of the word and concatenate its two final states, of 25 dimensions each, with the word embedding; this gives information about prefixes, suffixes and capitals and a vector for unknown words. Huang, Xu and Yu (2015) instead add hand-made spelling and context features.

**Bidirectional LSTM.** A forward LSTM reads the word vectors from left to right and gives $\overrightarrow{h_t}$, which summarizes $x_1, \ldots, x_t$. A backward LSTM, with its own parameters, reads from right to left and gives $\overleftarrow{h_t}$, which summarizes $x_t, \ldots, x_n$. The vector $h_t = [\overrightarrow{h_t}; \overleftarrow{h_t}]$ represents word $t$ in its context. A linear layer (Lample et al. add one hidden layer before it) maps $h_t$ to $k$ numbers. These form an $n \times k$ matrix $P$, where $P_{i, j}$ is the score of tag $j$ for word $i$.

**CRF layer.** A $(k + 2) \times (k + 2)$ matrix $A$ holds the score $A_{a, b}$ of tag $b$ right after tag $a$, with extra start and end tags $y_0$ and $y_{n+1}$. The score of a tag sequence $y$ is

$$s(X, y) = \sum_{i=0}^{n} A_{y_i, y_{i+1}} + \sum_{i=1}^{n} P_{i, y_i},$$

and its probability is $p(y \mid X) = \exp(s(X, y)) / \sum_{\tilde y} \exp(s(X, \tilde y))$, a softmax over all $k^n$ tag sequences (Lample et al. 2016, Section 2.2). This is a linear-chain CRF whose token potentials are the outputs of the network.

**Training.** Maximize $\log p(y \mid X) = s(X, y) - \log \sum_{\tilde y} \exp(s(X, \tilde y))$ over the training pairs. The second term is computed by the forward algorithm with the [log-sum-exp trick](/log-sum-exp-trick/) in $O(n k^2)$ time. The gradient flows into $A$, into $P$, and through $P$ into the LSTMs and the embeddings by [backpropagation through time](/backpropagation-through-time/). Lample et al. used [stochastic gradient descent](/stochastic-gradient-descent/) with learning rate 0.01 and gradient clipping at 5.0, and [dropout](/dropout/) with rate 0.5 on the input of the BiLSTM (Sections 4.3 and 5.1).

**Decoding.** $y^* = \arg\max_{\tilde y} s(X, \tilde y)$, by the Viterbi algorithm over the tag lattice with edge scores $A_{a, b} + P_{i, b}$.

## What it counts

- The BiLSTM costs $O(n h^2)$ time for hidden size $h$ (with the input size of the same order), in two passes of $n$ steps each. Each step depends on the one before, so the steps of one direction cannot run in parallel.
- The CRF layer costs $O(n k^2)$ time for the normalizer in training and for Viterbi decoding, and $O(n k)$ space. For the usual tag sets, $k$ is small and this is much less than the cost of the LSTM.
- The parameters are the embeddings, the LSTM weights, the output layer and the $(k + 2)^2$ entries of $A$. The CRF layer adds only $A$.

## Relation to other models

- Linear-chain [CRF](/conditional-random-field/): the same output layer and the same training objective. The difference is only where the token scores come from: learned features of the whole sentence instead of a weighted sum of hand-made features.
- BiLSTM with a softmax per token: drops $A$ and picks each tag on its own. It cannot rule out invalid [BIO](/bio-encoding/) sequences and does worse on entity recognition (see the results below).
- [Maximum entropy Markov model](/maximum-entropy-markov-model/) and greedy neural taggers: they normalize each step and can have the [label bias problem](/label-bias-problem/). The CRF layer normalizes over whole sequences.
- Conv-CRF of Collobert et al. (2011): a convolutional network over word embeddings with the same kind of tag-transition layer, which Huang, Xu and Yu and Lample et al. both describe as the closest earlier model.
- Pretrained encoders: replacing the BiLSTM by a pretrained [transformer](/transformer/) encoder such as [BERT](/bert/), with or without the CRF layer, keeps the same output structure.
- [Structured perceptron](/structured-perceptron/): the same score form and the same Viterbi decoding, but a fixed feature map and perceptron updates in place of a learned encoder and the likelihood.

## Known results in the model

All results here are measurements on standard data sets.

- Huang, Xu and Yu (2015, Table 2), with Senna embeddings: the BI-LSTM-CRF reached 97.55% accuracy on Penn Treebank POS tagging, F1 94.46 on CoNLL-2000 chunking, and F1 88.83 on CoNLL-2003 NER (90.10 with gazetteer features). In the same table, a CRF with the same features got 97.45, 93.83 and 86.13, and a BI-LSTM without the CRF layer got 97.40, 93.92 and 85.17.
- With word features only (Huang, Xu and Yu 2015, Section 4.3.2, Table 3), the CRF lost about 3 to 9 points, while the BI-LSTM-CRF lost little; for example it still got F1 94.40 on chunking.
- Lample et al. (2016, Tables 1 to 4), with character representations and no gazetteers: F1 90.94 on CoNLL-2003 English, 78.76 on German, and 81.74 on CoNLL-2002 Dutch and 85.75 on Spanish.
- Ablation on English (Lample et al. 2016, Section 5.4, Table 5): pretrained embeddings gave the largest gain, +7.31 F1; the CRF layer gave +1.79, dropout +1.17 and character representations +0.74.
- Tagging scheme (Lample et al. 2016, Section 2.4): they used IOBES tags but saw no significant gain over IOB.

## References
