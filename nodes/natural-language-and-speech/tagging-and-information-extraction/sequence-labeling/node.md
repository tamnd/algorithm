---
tag: A4KNGY
kind: problem
slug: sequence-labeling
name: Sequence labeling
aliases:
- sequence tagging
area: natural-language-and-speech/tagging-and-information-extraction
level: intro
summary: "Assign one label from a fixed set to each token of a sequence, using the whole sequence, as in tagging, chunking and entity recognition."
prereqs: [structured-prediction, hidden-markov-model]
see_also: [part-of-speech-tagging, text-chunking, named-entity-recognition, bio-encoding, conditional-random-field, structured-perceptron, maximum-entropy-markov-model, bilstm-crf]
sources:
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pages 282 to 289"
    title: "Lafferty, McCallum and Pereira 2001"
    locator: "Section 1 (the labeling problem and the generative and conditional models for it), Section 2 (label bias), Section 5.3 (part-of-speech tagging results of HMM, MEMM and CRF)"
  - paper: "Michael Collins, Discriminative training methods for hidden Markov models: theory and experiments with perceptron algorithms, Proceedings of EMNLP 2002, pages 1 to 8"
    title: Collins 2002
    locator: "Section 2 (tagging as the argmax of a linear score over tag sequences, decoded by Viterbi), Section 4 (tagging and NP chunking experiments)"
  - paper: "Erik F. Tjong Kim Sang and Sabine Buchholz, Introduction to the CoNLL-2000 shared task: chunking, Proceedings of CoNLL-2000 and LLL-2000, pages 127 to 132"
    title: Tjong Kim Sang and Buchholz 2000
    locator: "chunking as tagging with B-X, I-X and O tags, the data and the F score of chunks"
---

Sequence labeling asks for one label per token of an input sequence, chosen from a fixed set of $k$ labels, so that the whole label sequence is right. The labels of nearby tokens depend on each other, so a good method decides them jointly, not one token at a time. It is the most common form of [structured prediction](/structured-prediction/) in language processing: [part-of-speech tagging](/part-of-speech-tagging/), [text chunking](/text-chunking/) and [named entity recognition](/named-entity-recognition/) are all instances. This page is about the problem in general; the pages of the instances describe their label sets, data and scores.

## In plain words

You get a sentence and must write one tag under each word. The tags come from a short list, such as noun, verb and adjective, or "start of a name", "inside a name" and "not a name". You cannot decide each word alone: "can" is a verb after "you" and a noun after "the", and a name that starts must go on until it ends. So a method looks at the whole sentence and at how the tags fit together. When each tag only interacts with the tag before it, a table filled from left to right finds the best tag sequence quickly, even though there are very many sequences.

## Definition

**Input.** A sequence $x = x_1 \ldots x_n$ of tokens, a set $Y$ of $k$ labels, and a model that gives a score $s(x, y)$ to each label sequence $y \in Y^n$. The model is usually learned from training pairs $(x, y)$.

**Output.** A label sequence $\hat y = \arg\max_{y \in Y^n} s(x, y)$. There are $k^n$ candidates.

**First-order models.** Most methods use a score that splits into local parts:

$$s(x, y) = \sum_{i=1}^{n+1} \psi_i(x, y_{i-1}, y_i),$$

with a start label $y_0 = \langle s \rangle$ and an end label $y_{n+1} = \langle /s \rangle$. In a [hidden Markov model](/hidden-markov-model/), $\psi_i = \log P(y_i \mid y_{i-1}) + \log P(x_i \mid y_i)$. In a [conditional random field](/conditional-random-field/) or the [structured perceptron](/structured-perceptron/), $\psi_i = w \cdot f(x, i, y_{i-1}, y_i)$ for a feature vector $f$ that may look at the whole input. Models of order $m$ let $\psi_i$ depend on $y_{i-m}, \ldots, y_i$.

**Measures.** For a per-token task such as tagging, the score is the token accuracy. For a span task such as chunking, it is the F score of the spans: precision and recall of the predicted spans against the gold spans, where a span counts only if both of its ends and its label are right ([precision and recall](/precision-and-recall/)).

## Variants

- Decoding versus learning. Decoding finds $\hat y$ for a fixed model. Learning chooses the model from data, by counting (HMM), by maximizing the conditional likelihood (CRF), or by mistake-driven updates (perceptron).
- Most probable sequence versus best labels one by one. Under a probabilistic model, the most probable sequence (Viterbi) and the sequence of the most probable labels at each position (posterior decoding with the [forward-backward algorithm](/forward-backward-algorithm/)) can differ. The first maximizes the chance that the whole sequence is right, the second the expected number of right tokens.
- Span labeling. Spans can be encoded as token labels with [BIO encoding](/bio-encoding/), or labeled directly by a [semi-Markov CRF](/semi-markov-crf/).
- Constrained labeling. Some label pairs may be forbidden, such as O followed by I-X in BIO. The decoder then gives them a score of $-\infty$.
- Higher order. A second-order model scores label triples, as in the trigram [HMM tagger](/hmm-part-of-speech-tagger/).
- Unsupervised labeling. With no labeled data, the labels are clusters, as in [Bayesian HMM tagging](/bayesian-hmm-tagging/).

## Examples

- Part-of-speech tagging: in "the old man the boats", the first guess old/J man/N leaves no verb. The right tags are the/D old/N man/V the/D boats/N: "old" means old people and "man" is a verb. Only the context decides.
- Chunking with BIO tags: "He/B-NP reckons/B-VP the/B-NP current/I-NP account/I-NP deficit/I-NP".
- Named entities: "Jim/B-PER bought/O shares/O of/O Acme/B-ORG Corp/I-ORG".
- Outside language processing: gene finding labels each base of a DNA sequence as coding or not, and [word segmentation](/word-segmentation/) for languages without spaces can label each character as the start of a word or not.

## Known algorithms

- Exact decoding for first-order models: the [Viterbi algorithm](/viterbi-algorithm/), in $O(n k^2)$ time and $O(n k)$ space. For order $m$, a state is a tuple of $m$ labels and the time is $O(n k^{m+1})$.
- Marginals and the normalizer of a CRF: the forward-backward algorithm, also $O(n k^2)$, with the [log-sum-exp trick](/log-sum-exp-trick/).
- Generative models: the [HMM tagger](/hmm-part-of-speech-tagger/), trained by counting.
- Locally normalized discriminative models: the [maximum entropy Markov model](/maximum-entropy-markov-model/), which has the [label bias problem](/label-bias-problem/).
- Globally normalized and margin-based models: the [conditional random field](/conditional-random-field/) and the [structured perceptron](/structured-perceptron/).
- Rule learning: the [Brill tagger](/brill-tagger/).
- Neural models: the [BiLSTM-CRF](/bilstm-crf/), and token classifiers on top of encoders such as [BERT](/bert/), with or without a CRF layer.
- Approximate decoding: [greedy decoding](/greedy-decoding/) and [beam search](/beam-search/) for models whose scores do not split into local parts.

## Bounds

- Decoding a first-order model takes $O(n k^2)$ time with Viterbi (a theorem; see the [Viterbi algorithm](/viterbi-algorithm/)). The input has $\Theta(n k^2)$ numbers when every local score $\psi_i(y_{i-1}, y_i)$ is given separately, so this is optimal for that input form.
- For order $m$, the state space has $k^m$ states, and the time is $O(n k^{m+1})$.
- Without the local structure, for a general score over $Y^n$, the problem is as hard as maximizing an arbitrary function over $k^n$ points; models with long-range label interactions are decoded approximately.

## Reductions

- Span finding to sequence labeling: [BIO encoding](/bio-encoding/) maps each set of non-overlapping labeled spans to one label sequence and back.
- Sequence labeling to shortest paths: a first-order decoding problem is a longest path in a layered DAG with $n$ layers of $k$ nodes, where the edge from $(i - 1, a)$ to $(i, b)$ has weight $\psi_i(a, b)$. This is the [DAG dynamic programming](/dag-dynamic-programming/) view of Viterbi.
- Order $m$ to order 1: replace each label by the tuple of the last $m$ labels, which gives $k^m$ labels.
- Sequence labeling to classification: label each token alone with a classifier that sees the context. This drops the interaction between labels, and is exact only when the labels are independent given the input.

## Applications

Part-of-speech tagging, chunking, named entity recognition, [semantic role labeling](/semantic-role-labeling/) with BIO tags over argument spans, word segmentation, slot filling in dialogue systems, and the segmentation of speech, handwriting and biological sequences. Labeled spans are also the input of later steps such as [relation extraction](/relation-extraction/) and parsing.

## References
