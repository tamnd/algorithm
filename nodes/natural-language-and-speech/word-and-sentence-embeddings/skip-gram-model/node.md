---
tag: PV50G4
kind: model
slug: skip-gram-model
name: Skip-gram model
aliases:
- word2vec skip-gram
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: "A log-linear model that predicts each word in a window around a word from that word's vector. Its learned input vectors are word embeddings."
history:
  year: 2013
  people: [Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean]
  note: "Mikolov, Chen, Corrado and Dean proposed the skip-gram and CBOW models in 2013 and released them in the word2vec tool. A later paper of the same year added negative sampling and the subsampling of frequent words."
prereqs: [word-embedding, softmax-regression]
see_also: [continuous-bag-of-words, negative-sampling, hierarchical-softmax, sgns-implicit-factorization-theorem, subword-information-embeddings, glove, neural-probabilistic-language-model, deepwalk]
sources:
  - paper: "Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space, ICLR 2013 workshop track, arXiv:1301.3781"
    title: Mikolov, Chen, Corrado and Dean 2013
    locator: "Section 3.2 (the continuous skip-gram model, the training complexity Q = C x (D + D x log2(V)) of equation 5, and the window radius R drawn from 1 to C, with C = 10 in the experiments), Figure 1, Section 4.1 (the analogy test set)"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: the skip-gram objective as an average log probability over the window, the full softmax and its cost, hierarchical softmax, negative sampling and subsampling
  - paper: "Yoav Goldberg and Omer Levy, word2vec explained: deriving Mikolov et al.'s negative-sampling word-embedding method, arXiv:1402.3722, 2014 (preprint)"
    title: Goldberg and Levy 2014
    locator: the skip-gram objective written as a sum over the word and context pairs of a corpus
  - paper: "Jeffrey Pennington, Richard Socher and Christopher D. Manning, GloVe: global vectors for word representation, Proceedings of EMNLP 2014, pages 1532 to 1543"
    title: Pennington, Socher and Manning 2014
    locator: Table 2 (analogy accuracy of skip-gram and CBOW vectors trained by the authors with the word2vec tool on 6 billion tokens)
---

## The machine

The skip-gram model is a conditional model of a context word given a center word. It has these parts.

- **Vocabulary.** A finite set $V$ of word types, fixed before training. Words outside $V$ are dropped or mapped to one unknown symbol.
- **Parameters.** Two tables of real vectors of dimension $d$: an **input vector** $\vec v_w \in \mathbb{R}^d$ and an **output vector** $\vec u_w \in \mathbb{R}^d$ for each $w \in V$. As matrices they are $W_{\text{in}}$ and $W_{\text{out}}$, each of shape $|V| \times d$, so the model has $2|V|d$ parameters.
- **Conditional distribution.** For a center word $w$ and a context word $c$, the model is a [softmax](/softmax-regression/) over the vocabulary of the dot products:

$$P(c \mid w) = \frac{\exp(\vec u_c \cdot \vec v_w)}{\sum_{j \in V} \exp(\vec u_j \cdot \vec v_w)}.$$

There is no hidden nonlinearity: the score of a pair is bilinear in the two vectors, so the model is log-linear in each table.

- **Training pairs.** A corpus is a sequence of tokens $w_1, \ldots, w_N$ (in practice a list of sentences, and windows do not cross a sentence end). For each position $t$, the training draws a radius $R$ uniformly from $\{1, \ldots, C\}$, where $C$ is the maximum window, and emits the pairs $(w_t, w_{t+j})$ for $1 \le |j| \le R$. A context word at distance $\delta$ is therefore used with probability $(C - \delta + 1)/C$. Mikolov et al. describe this as giving less weight to distant words by sampling them less often.
- **Objective.** Maximize the sum of $\log P(w_{t+j} \mid w_t)$ over the emitted pairs, by stochastic gradient ascent. After training, the rows of $W_{\text{in}}$ are the [word embedding](/word-embedding/); the output table is usually discarded.

The standing assumptions are a closed vocabulary, a bag of context words (the position $j$ inside the window does not enter $P(c \mid w)$), and independence of the pairs in the objective.

The loss of one pair, and the way the pairs are made, as the code computes them:

```pseudo id=main
SKIP-GRAM-LOSS(w_1..w_N, C, W_in, W_out)
L1  for t ← 1 to N do
L2      R ← a uniform draw from {1, ..., C}
L3      for each j with 1 ≤ |j| ≤ R and 1 ≤ t + j ≤ N do emit (w_t, w_{t+j})
L4  for each emitted pair (w, c) do h ← v_w            ▷ the row of W_in
L5      s_x ← u_x · h for every x in V                 ▷ |V| dot products
L6      loss ← loss - (s_c - log Σ_x exp(s_x))         ▷ -log P(c | w)
```

## What it counts

The model assigns the probability $P(c \mid w)$ above to each context word, and the training loss is the [cross-entropy](/cross-entropy-loss/) $-\sum \log P(c \mid w)$ over the emitted pairs. The gradient for one pair $(w, c)$ is

$$\frac{\partial}{\partial \vec v_w}\big(-\log P(c \mid w)\big) = \sum_{x \in V} P(x \mid w)\,\vec u_x - \vec u_c, \qquad \frac{\partial}{\partial \vec u_x}\big(-\log P(c \mid w)\big) = \big(P(x \mid w) - [x = c]\big)\,\vec v_w.$$

**Example.** Take $V = \{\text{the}, \text{cat}, \text{sat}, \text{on}, \text{mat}\}$, $d = 2$, $\vec v_{\text{cat}} = (1, 0)$ and the output vectors $\vec u_{\text{the}} = \vec u_{\text{cat}} = (0, 0)$, $\vec u_{\text{sat}} = (1, 1)$, $\vec u_{\text{on}} = (0.5, 0)$, $\vec u_{\text{mat}} = (-1, 0)$. The scores are $(0, 0, 1, 0.5, -1)$, and the softmax gives

$$P(\cdot \mid \text{cat}) = (0.1485, 0.1485, 0.4036, 0.2448, 0.0546).$$

The loss of the pair (cat, sat) is $-\log 0.4036 = 0.9073$ nats. Its gradient with respect to $\vec v_{\text{cat}}$ is $0.4036 (1, 1) + 0.2448 (0.5, 0) + 0.0546 (-1, 0) - (1, 1) = (-0.5286, -0.5964)$, so a gradient step moves $\vec v_{\text{cat}}$ toward $\vec u_{\text{sat}}$.

**Cost of one evaluation.** With the full softmax, one pair costs $|V|$ dot products of length $d$, that is $O(|V| d)$ time, for the loss and for the gradient. Each position has on average $2 \cdot \frac{1}{C}\sum_{\delta=1}^{C}(C - \delta + 1) = C + 1$ pairs, so a pass over $N$ tokens costs $O(N C |V| d)$. This is too slow for a large vocabulary, and the model is trained with one of two approximations:

- [hierarchical softmax](/hierarchical-softmax/), which replaces the $|V|$ scores by about $\log_2 |V|$ binary decisions, $O(d \log |V|)$ per pair;
- [negative sampling](/negative-sampling/), which replaces the softmax by $k + 1$ logistic terms, $O((k + 1) d)$ per pair, and no longer defines a normalized $P(c \mid w)$.

Mikolov et al. give the training complexity per token as $Q = C \times (D + D \times \log_2 V)$ (their equation 5, with $D = d$ and $V = |V|$), which counts one input vector and a hierarchical softmax for each of about $C$ context words.

## Relation to other models

- **[Continuous bag-of-words](/continuous-bag-of-words/)** reverses the direction. It predicts the center word from the mean of the context vectors. It makes one prediction per position instead of about $C$, so it trains faster.
- **[Neural probabilistic language model](/neural-probabilistic-language-model/).** Bengio et al. 2003 predict the next word from the concatenated vectors of the previous words through a nonlinear hidden layer. The skip-gram model removes the hidden layer and the word order, and predicts in both directions. It is not a language model: it gives no probability to a sentence.
- **[Softmax regression](/softmax-regression/).** For a fixed input vector $\vec v_w$, $P(c \mid w)$ is a multinomial logistic regression whose weight rows are the output vectors. The model trains the input and the weights together.
- **Count methods.** With negative sampling and a large enough dimension, the optimum factorizes a shifted PMI matrix ([SGNS factorization theorem](/sgns-implicit-factorization-theorem/)). [GloVe](/glove/) fits the log counts directly, and a truncated SVD of a [PPMI matrix](/positive-pointwise-mutual-information/) is the classic count analogue.
- **Extensions.** [Subword information embeddings](/subword-information-embeddings/) replace $\vec v_w$ by a sum of character n-gram vectors. [DeepWalk](/deepwalk/) and [node2vec](/node2vec/) apply the skip-gram model to random walks on a graph. The [paragraph vector](/paragraph-vector/) adds a document vector to the input.

## Known results in the model

**The free-score optimum is the conditional frequency.** Let $\#(w, c)$ be the number of emitted pairs and $\#(w) = \sum_c \#(w, c)$. If each row of scores $s_{w, \cdot}$ could be set freely, the objective $\sum_{w, c} \#(w, c) \log P(c \mid w)$ is maximized when $P(c \mid w) = \#(w, c)/\#(w)$ for every word with $\#(w) > 0$.

*Proof.* The objective splits over $w$. For a fixed $w$, any distribution $q$ on $V$ satisfies $\sum_c \#(w, c) \log q(c) = \#(w) \sum_c \hat p(c) \log q(c)$ with $\hat p(c) = \#(w, c)/\#(w)$. By Gibbs' inequality, $\sum_c \hat p(c) \log q(c) \le \sum_c \hat p(c) \log \hat p(c)$, with equality only at $q = \hat p$. Every distribution with full support is a softmax of some scores, and $\hat p$ is approached as the scores of unseen pairs go to $-\infty$. $\blacksquare$

So the scores are determined only up to a constant per row, $s_{wc} = \log \hat p(c) + a_w$. With a finite $d$, the matrix $W_{\text{in}} W_{\text{out}}^\top$ has rank at most $d$, and the trained model is a low-rank compromise, which is what makes similar words share vectors.

**The dynamic window is a weighting.** The expected number of times the pair $(w_t, w_{t+\delta})$ is used is $(C - \delta + 1)/C$: 1 for $\delta = 1$ and $1/C$ for $\delta = C$. With $C = 5$ the weights are $1, 0.8, 0.6, 0.4, 0.2$. [GloVe](/glove/) uses the weight $1/\delta$ for the same purpose.

**Cost.** The three training objectives cost $O(|V| d)$ (full softmax), $O(d \log |V|)$ (balanced hierarchical softmax; for a Huffman tree, the expected path length is within one bit of the entropy of the word distribution) and $O((k + 1) d)$ (negative sampling with $k$ noise words) per pair. The memory is $2|V|d$ numbers for the two tables.

**Measurements.** These are measurements, not guarantees. On the analogy test set of Mikolov et al. (8869 semantic and 10675 syntactic questions), Pennington, Socher and Manning report for 300-dimensional vectors trained on 6 billion tokens with the word2vec tool an accuracy of 73.0 percent (semantic), 66.0 percent (syntactic) and 69.1 percent (total) for skip-gram, against 63.6, 67.4 and 65.7 percent for CBOW (their Table 2). The result depends on the corpus, the window, the number of epochs and the evaluation method of [word analogy](/word-analogy/).

## References
