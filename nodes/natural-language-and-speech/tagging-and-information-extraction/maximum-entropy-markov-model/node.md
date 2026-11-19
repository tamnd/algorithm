---
tag: GH9RD1
kind: model
slug: maximum-entropy-markov-model
name: Maximum entropy Markov model
aliases:
- MEMM
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "A tagger with a log-linear distribution of each tag given the previous tag and features of the input, decoded by Viterbi."
history:
  year: 2000
  people: [Andrew McCallum, Dayne Freitag, Fernando Pereira]
  note: "McCallum, Freitag and Pereira named the MEMM at ICML 2000; Ratnaparkhi had built a maximum entropy tagger of the same form in 1996."
prereqs: [hmm-part-of-speech-tagger, softmax-regression, viterbi-algorithm]
see_also: [label-bias-problem, conditional-random-field, structured-perceptron, sequence-labeling, part-of-speech-tagging, generative-vs-discriminative-models, logistic-regression, beam-search]
sources:
  - paper: "Andrew McCallum, Dayne Freitag and Fernando Pereira, Maximum entropy Markov models for information extraction and segmentation, Proceedings of the Seventeenth International Conference on Machine Learning (ICML 2000), pages 591 to 598"
    title: "McCallum, Freitag and Pereira 2000"
    locator: "the MEMM, with one maximum entropy model of the next state per source state, its Viterbi decoding and its training"
  - paper: "Adwait Ratnaparkhi, A maximum entropy model for part-of-speech tagging, Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP 1996), pages 133 to 142"
    title: Ratnaparkhi 1996
    locator: "the maximum entropy tagger with word, affix and previous-tag features, and its search"
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pages 282 to 289"
    title: "Lafferty, McCallum and Pereira 2001"
    locator: "Section 2 (the label bias problem of MEMMs, Figure 1), Section 5.1 (synthetic data), Section 5.3 and Figure 4 (part-of-speech tagging error rates of HMM, MEMM and CRF)"
---

A maximum entropy Markov model (MEMM) tags a sequence with a chain of local classifiers. Each one gives a distribution of the current tag, conditioned on the previous tag and on any features of the input, in the log-linear form of [softmax regression](/softmax-regression/). The probability of a tag sequence is the product of these local probabilities, and Viterbi finds the best sequence. Compared with the [HMM tagger](/hmm-part-of-speech-tagger/), it models $P(y \mid x)$ instead of $P(x, y)$, so its features can overlap and can look at the whole input. Compared with the [conditional random field](/conditional-random-field/), it normalizes each step on its own, which makes training simple but causes the [label bias problem](/label-bias-problem/).

## The machine

A sentence $x = x_1 \ldots x_n$ is given, and the tags come from a set $Y$ of $k$ tags, with $y_0 = \langle s \rangle$. A feature function $f(x, i, y', y) \in \mathbb{R}^d$ describes position $i$ with previous tag $y'$ and current tag $y$. It can test the word $x_i$, its suffixes and capitalization, nearby words, and the pair $(y', y)$. The model has one weight vector $w \in \mathbb{R}^d$ and defines

$$P(y_i = y \mid y_{i-1} = y', x) = \frac{\exp(w \cdot f(x, i, y', y))}{Z(x, i, y')}, \qquad Z(x, i, y') = \sum_{t \in Y} \exp(w \cdot f(x, i, y', t)),$$

$$P(y \mid x) = \prod_{i=1}^{n} P(y_i \mid y_{i-1}, x).$$

McCallum, Freitag and Pereira (2000) write it as one maximum entropy model per source state $y'$, each giving the distribution of the next state given the observation; with features that include the previous tag this is the same model. Ratnaparkhi's tagger (1996) conditions on the two previous tags.

Training maximizes the conditional log likelihood $\sum_{(x,y)} \sum_i \log P(y_i \mid y_{i-1}, x)$, with the gold previous tag in each term. This is a sum of independent multiclass [logistic regression](/logistic-regression/) problems, one per position, so it is concave in $w$ and needs no dynamic programming: the gradient of each term is the observed feature vector minus its expectation under the local distribution. The original papers used generalized iterative scaling; any convex optimizer such as [L-BFGS](/limited-memory-bfgs/) works, usually with a Gaussian prior on $w$.

Decoding finds $\arg\max_y \sum_i \log P(y_i \mid y_{i-1}, x)$ with the [Viterbi algorithm](/viterbi-algorithm/), where the score of the edge from $y'$ at $i - 1$ to $y$ at $i$ is $\log P(y \mid y', x)$. Ratnaparkhi used a beam search instead.

## What it counts

- Decoding time: $O(n k^2)$ evaluations of local scores, plus the cost of the $k$ normalizers $Z(x, i, y')$ at each position, each a sum over $k$ tags, so $O(n k^2)$ in all when the features of a position are computed once. With features of two previous tags, $O(n k^3)$.
- Training time: one gradient of the objective costs $O(N k)$ score evaluations for $N$ training tokens, because each term needs only the normalizer for the gold previous tag. A CRF needs forward-backward over each sentence, which costs $O(N k^2)$ per gradient. The MEMM treats each position as an independent example.
- The model is a probability distribution over tag sequences: the sum of $P(y \mid x)$ over all $k^n$ sequences is 1, since each local distribution sums to 1.

## Relation to other models

- [HMM tagger](/hmm-part-of-speech-tagger/): the HMM is generative and factors as $P(y_i \mid y_{i-1}) P(x_i \mid y_i)$. To add a feature such as a suffix to an HMM, one must model how the tag generates that feature, and overlapping features break the independence assumptions. The MEMM conditions on $x$, so overlapping features cost nothing; see [generative and discriminative models](/generative-vs-discriminative-models/).
- [Conditional random field](/conditional-random-field/): the linear-chain CRF uses the same features but one global normalizer, $P(y \mid x) = \exp(\sum_i w \cdot f(x, i, y_{i-1}, y_i)) / Z(x)$. Lafferty, McCallum and Pereira (2001) introduced it to avoid label bias. Training needs forward-backward.
- [Structured perceptron](/structured-perceptron/): also scores whole sequences with the same features, but trains by Viterbi decoding and additive updates, with no normalization at all.
- Greedy classifiers: tagging left to right with a classifier that sees the previously predicted tags is the MEMM with greedy decoding in place of Viterbi. It suffers from the same mismatch between training on gold previous tags and testing on predicted ones ([exposure bias](/exposure-bias/)).

## Known results in the model

- Label bias (a theorem about the model class, shown by example): because each local distribution sums to 1 whatever the observation is, a state with one successor passes all its mass to it, and the observation at that step cannot change the score of the path. Lafferty et al. (2001, Section 2, Figure 1) give the rib and rob example, where the MEMM cannot learn to read the second letter. See [label bias problem](/label-bias-problem/).
- Synthetic data (a measurement): on data generated by an HMM, designed to show label bias, the MEMM had an error rate of 42% against 4.6% for the CRF (Lafferty et al. 2001, Section 5.1).
- Part-of-speech tagging (a measurement, Penn Treebank, Lafferty et al. 2001, Section 5.3 and Figure 4): with first-order features only, the error rates were 5.69% for the HMM, 6.37% for the MEMM and 5.55% for the CRF; on unknown words 45.99%, 54.61% and 48.05%. With spelling features added, the MEMM got 4.81% (26.99% on unknown words) and the CRF 4.27% (23.76%). The MEMM gains much from the extra features, which the HMM cannot use easily, but stays behind the CRF.
- Training is a convex problem (a theorem): the conditional log likelihood of each local model is concave in $w$, so a global optimum can be found.

## References
