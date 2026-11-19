---
tag: GERBMV
kind: model
slug: continuous-bag-of-words
name: Continuous bag-of-words model
aliases:
- CBOW
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: A word2vec model that predicts the center word of a window from the sum or mean of the vectors of the words around it.
history:
  year: 2013
  people: [Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean]
  note: "Mikolov, Chen, Corrado and Dean proposed CBOW together with the skip-gram model in 2013. They describe it as a feedforward language model without the nonlinear hidden layer, with a projection layer that all context words share."
prereqs: [word-embedding, softmax-regression]
see_also: [skip-gram-model, negative-sampling, hierarchical-softmax, neural-probabilistic-language-model, paragraph-vector, glove, word-analogy]
sources:
  - paper: "Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space, ICLR 2013 workshop track, arXiv:1301.3781"
    title: Mikolov, Chen, Corrado and Dean 2013
    locator: "Section 3.1 (the continuous bag-of-words model, the averaged projection, four history and four future words, and the training complexity Q = N x D + D x log2(V) of equation 4), Figure 1, Section 4 (the analogy results)"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: hierarchical softmax, negative sampling and subsampling, which the word2vec tool applies to CBOW as well as to skip-gram
  - paper: "Jeffrey Pennington, Richard Socher and Christopher D. Manning, GloVe: global vectors for word representation, Proceedings of EMNLP 2014, pages 1532 to 1543"
    title: Pennington, Socher and Manning 2014
    locator: Table 2 (analogy accuracy of CBOW and skip-gram vectors trained by the authors with the word2vec tool on 6 billion tokens)
---

## The machine

The continuous bag-of-words model (CBOW) is a conditional model of the center word of a window given the words around it. It has these parts.

- **Vocabulary.** A finite set $V$ of word types, fixed before training.
- **Parameters.** Two tables of real vectors of dimension $d$: an **input vector** $\vec v_w$ and an **output vector** $\vec u_w$ for each $w \in V$, that is $2|V|d$ numbers.
- **Context.** For position $t$ of a corpus $w_1, \ldots, w_N$, the context is the list of words at distance 1 to $C$ on both sides, $\mathrm{ctx}(t) = (w_{t-C}, \ldots, w_{t-1}, w_{t+1}, \ldots, w_{t+C})$, cut at the ends of the sentence. Mikolov et al. use four words on each side.
- **Hidden vector.** The context vectors are averaged (or summed) into one vector, so the order of the context words is lost:

$$\vec h_t = \frac{1}{|\mathrm{ctx}(t)|} \sum_{c \in \mathrm{ctx}(t)} \vec v_c.$$

- **Conditional distribution.** A [softmax](/softmax-regression/) over the vocabulary:

$$P(w \mid \mathrm{ctx}(t)) = \frac{\exp(\vec u_w \cdot \vec h_t)}{\sum_{j \in V} \exp(\vec u_j \cdot \vec h_t)}.$$

- **Objective.** Maximize $\sum_t \log P(w_t \mid \mathrm{ctx}(t))$ by stochastic gradient ascent. After training, the rows of the input table are the [word embedding](/word-embedding/).

The word2vec tool draws the radius of each window uniformly from $\{1, \ldots, C\}$, as for the [skip-gram model](/skip-gram-model/). The code here uses the fixed radius $C$.

```pseudo id=main
CBOW-LOSS(w_1..w_N, C, W_in, W_out)
L1  for each position t, ctx ← the words at distance 1 to C from t
L2      h ← the mean of v_c over c in ctx                ▷ or the sum
L3      s_x ← u_x · h for every x in V                   ▷ |V| dot products
L4      loss ← loss - (s_{w_t} - log Σ_x exp(s_x))       ▷ -log P(w_t | ctx)
```

## What it counts

The loss of position $t$ is $-\log P(w_t \mid \mathrm{ctx}(t))$, a [cross-entropy](/cross-entropy-loss/). With $p_x = P(x \mid \mathrm{ctx}(t))$ and $\vec g = \sum_{x} p_x \vec u_x - \vec u_{w_t}$, the gradient is

$$\frac{\partial\,\text{loss}}{\partial \vec u_x} = \big(p_x - [x = w_t]\big)\,\vec h_t, \qquad \frac{\partial\,\text{loss}}{\partial \vec v_c} = \frac{m_c}{|\mathrm{ctx}(t)|}\,\vec g,$$

where $m_c$ is the number of times $c$ occurs in the context. Every context word gets the same share of the error, and a word that occurs twice in the window gets two shares. With the sum in place of the mean, the factor $1/|\mathrm{ctx}(t)|$ goes away.

**Example.** Take $V = \{\text{the}, \text{cat}, \text{sat}\}$, $d = 2$, the window "the _ sat" with center "cat", $\vec v_{\text{the}} = (1, 0)$ and $\vec v_{\text{sat}} = (0, 1)$. The hidden vector is $\vec h = (0.5, 0.5)$. With $\vec u_{\text{the}} = (0, 0)$, $\vec u_{\text{cat}} = (1, 1)$ and $\vec u_{\text{sat}} = (-1, 0)$, the scores are $(0, 1, -0.5)$ and

$$P(\cdot \mid \text{the}, \text{sat}) = (0.2312, 0.6285, 0.1402).$$

The loss is $-\log 0.6285 = 0.4644$ nats. The vector $\vec g$ is $0.6285(1, 1) + 0.1402(-1, 0) - (1, 1) = (-0.5117, -0.3715)$, and each of the two context vectors gets the gradient $\vec g / 2 = (-0.2559, -0.1857)$. A gradient step moves both toward $\vec u_{\text{cat}}$.

**Cost of one evaluation.** The mean costs $O(|\mathrm{ctx}| d)$, and the full softmax costs $O(|V| d)$. Mikolov et al. give the training complexity per position as $Q = N \times D + D \times \log_2 V$ (their equation 4, with $N$ the number of context words, $D = d$ and a hierarchical softmax over $V$ words). This is one output computation per position, against about $C$ for skip-gram. With [negative sampling](/negative-sampling/) the output term becomes $(k + 1) d$ for $k$ noise words.

## Relation to other models

- **[Skip-gram model](/skip-gram-model/).** Skip-gram predicts each context word from the center word. CBOW predicts the center word from the averaged context. CBOW makes one prediction per position, so it trains faster. Averaging smooths over the window, and each context word gets only a $1/|\mathrm{ctx}|$ share of the error.
- **[Neural probabilistic language model](/neural-probabilistic-language-model/).** Bengio et al. 2003 concatenate the vectors of the previous words, which keeps their order, and pass them through a nonlinear hidden layer. CBOW removes the hidden layer, averages instead of concatenating and uses words on both sides. It is not a language model: it gives no probability to a sentence.
- **[Softmax regression](/softmax-regression/).** For a fixed $\vec h_t$, the output layer is a multinomial logistic regression whose weight rows are the output vectors.
- **[Paragraph vector](/paragraph-vector/).** The distributed memory variant of Le and Mikolov adds a document vector to the CBOW input.
- **Training approximations.** [Hierarchical softmax](/hierarchical-softmax/) and [negative sampling](/negative-sampling/) apply to CBOW unchanged, with $\vec h_t$ in place of the center word vector.

## Known results in the model

**Free-score optimum.** If the scores of each context could be set freely, the objective is maximized when $P(w \mid \mathrm{ctx})$ equals the relative frequency of $w$ among the positions with that context, by Gibbs' inequality. The proof is the one on the [skip-gram model](/skip-gram-model/) page with the context in place of the center word. CBOW cannot reach this optimum, because $\vec h$ depends only on the multiset of context words and lies in a space of dimension $d$.

**Mean and sum.** With the mean, the scale of $\vec h$ does not grow with the size of the window, and windows cut at a sentence end have the same scale as full ones. With a fixed window size $m$, the sum is $m$ times the mean, so the two models can represent the same distributions (scale the output vectors by $1/m$). With windows of different sizes they are different models. The word2vec tool has an option for each.

**Cost.** The cost per position is $O(C d + |V| d)$ with the full softmax, $O(C d + d \log |V|)$ with a balanced hierarchical softmax and $O(C d + (k + 1) d)$ with $k$ negative samples. The memory is $2|V|d$ numbers.

**Measurements.** These are measurements, not guarantees. Pennington, Socher and Manning report, for 300-dimensional vectors trained on 6 billion tokens with the word2vec tool, an analogy accuracy of 63.6 percent (semantic), 67.4 percent (syntactic) and 65.7 percent (total) for CBOW, against 73.0, 66.0 and 69.1 percent for skip-gram (their Table 2). The comparison depends on the corpus, the window, the number of epochs and the settings.

## References
