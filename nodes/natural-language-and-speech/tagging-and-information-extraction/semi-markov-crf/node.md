---
tag: N6VK89
kind: model
slug: semi-markov-crf
name: Semi-Markov conditional random field
aliases:
- semi-CRF
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "A CRF over segmentations into labeled spans, with features of whole spans, decoded by a segment Viterbi in O(n L k^2) time."
history:
  year: 2004
  people: [Sunita Sarawagi, William W. Cohen]
  note: "Sarawagi and Cohen introduced semi-Markov CRFs at NIPS 2004 as a conditionally trained version of semi-Markov chains, for named entity recognition."
prereqs: [conditional-random-field, hidden-semi-markov-model]
see_also: [text-chunking, named-entity-recognition, bio-encoding, sequence-labeling, structured-perceptron, forward-backward-algorithm, weighted-interval-scheduling, word-segmentation]
sources:
  - paper: "Sunita Sarawagi and William W. Cohen, Semi-Markov conditional random fields for information extraction, Advances in Neural Information Processing Systems 17 (NIPS 2004), pages 1185 to 1192"
    title: Sarawagi and Cohen 2004
    locator: "Section 2.1 (segmentations and segment features, Equations 2 and 3), Section 2.2 (the semi-Markov Viterbi recursion, Equation 4), Section 2.3 (comparison with order-L CRFs), Section 2.4 (likelihood, gradient and the forward recursion), Section 3.3 (NER results)"
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pages 282 to 289"
    title: "Lafferty, McCallum and Pereira 2001"
    locator: the linear-chain CRF that the semi-CRF generalizes
---

A semi-Markov conditional random field (semi-CRF) is a [conditional random field](/conditional-random-field/) whose output is a segmentation of the input into labeled spans, not one label per token. Its features can look at a whole span: its length, the phrase inside it, and how similar that phrase is to entries of a dictionary. The Markov assumption holds between segments, not between tokens. Compared with a linear-chain CRF over [BIO tags](/bio-encoding/), it can use these span features directly, at a cost that is only a factor $L$ larger, where $L$ is the maximum span length. Compared with a [hidden semi-Markov model](/hidden-semi-markov-model/), it is trained conditionally, so its features can overlap and look at the whole input. Sarawagi and Cohen (2004) introduced it for [named entity recognition](/named-entity-recognition/).

## The machine

The input is a sequence $x = x_1 \ldots x_n$ and a label set $Y$ of $k$ labels. A segmentation $s = (s_1, \ldots, s_p)$ splits $x$ into consecutive non-empty spans that cover it: segment $s_j = (t_j, u_j, y_j)$ covers the tokens $t_j + 1$ to $u_j$ and has the label $y_j$, with $t_1 = 0$, $u_p = n$, $t_{j+1} = u_j$ and $u_j - t_j \le L$. In named entity recognition, tokens outside entities are put into segments of length 1 with the label O.

A segment feature vector $g(y_j, y_{j-1}, x, t_j, u_j) \in \mathbb{R}^d$ may look at the label of the segment, the label of the segment before it, the whole input, and the two ends of the segment. Let $G(x, s) = \sum_j g(y_j, y_{j-1}, x, t_j, u_j)$. The model is

$$P(s \mid x) = \frac{\exp(w \cdot G(x, s))}{Z(x)}, \qquad Z(x) = \sum_{s'} \exp(w \cdot G(x, s')),$$

with the sum over all segmentations $s'$ with segments of length at most $L$ (Sarawagi and Cohen 2004, Section 2.1, Equations 2 and 3).

**Decoding.** Let $V(i, y)$ be the best score $w \cdot G$ of a segmentation of the first $i$ tokens whose last segment ends at $i$ and has the label $y$. Then $V(0, y) = 0$, $V(i, y) = -\infty$ for $i < 0$, and for $i > 0$

$$V(i, y) = \max_{y' \in Y,\ 1 \le d \le L} \bigl( V(i - d, y') + w \cdot g(y, y', x, i - d, i) \bigr).$$

The best segmentation is traced back from $\max_y V(n, y)$ (Section 2.2, Equation 4). For $L = 1$ this is the usual [Viterbi algorithm](/viterbi-algorithm/).

**Training.** The conditional log likelihood $\sum_\ell (w \cdot G(x_\ell, s_\ell) - \log Z(x_\ell))$ is concave, and its gradient is the observed $G$ minus its expectation under the model (Section 2.4). The normalizer comes from the forward recursion

$$\alpha(i, y) = \sum_{d=1}^{L} \sum_{y' \in Y} \alpha(i - d, y') \exp(w \cdot g(y, y', x, i - d, i)), \qquad Z(x) = \sum_y \alpha(n, y),$$

with $\alpha(0, y) = 1$ and $\alpha(i, y) = 0$ for $i < 0$, and the expectations from a similar recursion, the segment form of the [forward-backward algorithm](/forward-backward-algorithm/). Sarawagi and Cohen used a limited-memory quasi-Newton method with a Gaussian prior.

## What it counts

- Decoding and the forward recursion: $O(n L k^2)$ evaluations of the segment score, since each of the $n k$ cells takes a maximum or sum over $L$ lengths and $k$ previous labels. With $L = n$ (no limit), this is $O(n^2 k^2)$, still polynomial.
- Space: $O(n k)$ for the tables $V$ and $\alpha$. Sarawagi and Cohen (2004, Section 2.4, footnote 2) note that the expectations can be computed in $O(n k)$ space instead of $O(n L k)$ by first computing the backward values.
- Feature cost: there are at most $n L$ candidate spans. Span features such as the similarity to a dictionary are computed once per span and label.

## Relation to other models

- Linear-chain [CRF](/conditional-random-field/): the case $L = 1$. A semi-CRF can be written as a first-order CRF exactly when the sum of its segment features can be written as a sum of token features (Section 2.3). A feature $d_j \cdot [y_j = \text{I}]$, the length of an entity, is of this kind, since it equals the number of tokens labeled I. A feature $(d_j - \mu)^2 \cdot [y_j = \text{I}]$, which gives a Gaussian model of entity length, is not.
- Order-$L$ CRF: Sarawagi and Cohen state that for fixed $L$ a semi-CRF is no more expressive than an order-$L$ CRF, but an order-$L$ CRF has $k^L$ label tuples as states, while the semi-CRF only considers runs of one label, so its extra cost is linear in $L$, not exponential (Section 2.3).
- BIO tagging: a CRF over [BIO encoding](/bio-encoding/) tags also outputs labeled spans, and its features see only one token and two adjacent tags at a time. Sarawagi and Cohen compared the semi-CRF with a CRF over I and O tags and with a CRF over four tags that mark the beginning, end, continuation and unit entity.
- [Hidden semi-Markov model](/hidden-semi-markov-model/): the generative model with explicit state durations. The semi-CRF is its conditionally trained form, in the same way as the CRF is the conditional form of the HMM.
- Semi-Markov perceptron: the same segment Viterbi with [structured perceptron](/structured-perceptron/) updates. Sarawagi and Cohen report that their earlier perceptron-based learner was simpler and numerically more stable, since it needs no partition function, but that the semi-CRF did somewhat better on average (in their discussion of related work).
- Without the dependence on the previous label, the best segmentation is a set of disjoint weighted intervals that cover the input, the [weighted interval scheduling](/weighted-interval-scheduling/) structure.

## Known results in the model

- Exact inference and learning take polynomial time (a theorem): the recursions above are exact because each segment score depends only on the segment and the label of the previous segment.
- The likelihood is concave in $w$ (a theorem), so training finds a global optimum, as for the CRF.
- Named entity recognition (a measurement, Sarawagi and Cohen 2004, Section 3.3): on five extraction tasks from three small corpora (addresses, job postings and email), with $L$ between 4 and 6, the semi-CRF had the best F1 on all five tasks without dictionary features. With all available features it beat both CRF variants on eight of ten conditions. Segment-level dictionary features, such as the similarity of a span to the nearest dictionary entry, helped the semi-CRF, while their token-level versions often hurt the CRFs.
- Sarawagi and Cohen (Section 1) name gene finding and NP chunking as other tasks where segments have a clear meaning; see [text chunking](/text-chunking/). [Word segmentation](/word-segmentation/) has the same form, with words as segments.

## References
