---
tag: DHVXMW
kind: problem
slug: structured-prediction
name: Structured prediction
aliases:
- structured output prediction
- structured output learning
area: machine-learning/supervised-learning
level: advanced
summary: "Learn to predict outputs with internal structure, such as tag sequences, parse trees or matchings, by scoring whole outputs and decoding the best one, for example with Viterbi."
prereqs: [multiclass-classification, perceptron, viterbi-algorithm]
see_also: [conditional-random-field, hidden-markov-model, map-inference, cyk-algorithm, beam-search, generative-vs-discriminative-models, learning-to-rank, support-vector-machine]
sources:
  - paper: "Michael Collins, Discriminative training methods for hidden Markov models: theory and experiments with perceptron algorithms, Proceedings of the 2002 Conference on Empirical Methods in Natural Language Processing (EMNLP)"
    locator: pp. 1 to 8 (the structured perceptron, the averaged perceptron, and Theorem 1, at most R²/δ² mistakes on separable data)
  - paper: "Ioannis Tsochantaridis, Thorsten Joachims, Thomas Hofmann and Yasemin Altun, Large margin methods for structured and interdependent output variables, Journal of Machine Learning Research 6, 2005"
    locator: pp. 1453 to 1484 (the structured SVM, margin and slack rescaling, and the cutting plane algorithm with loss-augmented inference)
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of the 18th International Conference on Machine Learning (ICML), 2001"
    locator: pp. 282 to 289 (linear-chain CRFs and their training by conditional maximum likelihood)
  - paper: "Ben Taskar, Carlos Guestrin and Daphne Koller, Max-margin Markov networks, Advances in Neural Information Processing Systems 16, MIT Press, 2004"
    locator: pp. 25 to 32 (the max-margin objective with a loss that factors over the graph, and its factored dual)
  - paper: "Hal Daumé III, John Langford and Daniel Marcu, Search-based structured prediction, Machine Learning 75(3), 2009"
    locator: pp. 297 to 325 (SEARN, the reduction of structured prediction to cost-sensitive classification)
  - paper: doi:10.1109/TIT.1967.1054010
    title: Andrew J. Viterbi, Error bounds for convolutional codes and an asymptotically optimum decoding algorithm, IEEE Transactions on Information Theory 13(2), 1967
    locator: pp. 260 to 269 (the dynamic program over the trellis)
  - paper: "Sebastian Nowozin and Christoph H. Lampert, Structured learning and prediction in computer vision, Foundations and Trends in Computer Graphics and Vision 6(3-4), 2011"
    locator: the survey of inference and learning for structured models, with the structured SVM and its training
---

Structured prediction is the supervised learning problem in which each output is a structured object made of many interdependent parts: a sequence of tags for a sentence, a parse tree, an alignment, a matching, or a labeling of all the pixels of an image. The number of possible outputs grows exponentially with the size of the input, so a learner cannot treat each output as a class. The standard approach scores a whole output with a linear function of a joint feature vector, $w^{\top} \phi(x, y)$, chosen so that the score splits into local parts, and predicts with an exact or approximate combinatorial search, such as the [Viterbi algorithm](/viterbi-algorithm/) for chains or [CKY](/cyk-algorithm/) for trees. The main learning methods are the structured perceptron (Collins 2002), [conditional random fields](/conditional-random-field/) (Lafferty, McCallum and Pereira 2001) and structured SVMs (Taskar, Guestrin and Koller 2003; Tsochantaridis et al. 2005).

## In plain words

Some answers are not one label but many labels that depend on each other. For each word of a sentence you may need to say whether it is a noun, a verb or another word type, and the type of one word changes what the next word is likely to be. A sentence of 20 words with 40 word types has more possible answers than there are grains of sand on Earth, so you cannot check them one by one.

The method gives a score to each small piece of an answer, such as "this word is a noun" or "a verb follows a noun", and the score of a full answer is the sum of the scores of its pieces. A clever search finds the best full answer quickly. Learning adjusts the piece scores until the best answer for each training example is the correct one.

## Definition

**Data.** Pairs $(x_1, y_1), \ldots, (x_N, y_N)$ drawn i.i.d. from an unknown distribution, where each $y_i$ lies in a finite set $\mathcal{Y}(x_i)$ of candidate outputs for $x_i$. For sequence labeling with $K$ labels, an input of length $n$ has $|\mathcal{Y}(x)| = K^n$.

**Model.** A joint feature map $\phi(x, y) \in \mathbb{R}^d$ and weights $w$. The prediction is
$$ h_w(x) = \arg\max_{y \in \mathcal{Y}(x)} w^{\top} \phi(x, y). $$
Computing $h_w$ is the inference or decoding problem. It is tractable when $\phi$ is a sum of features over the parts of a graph with low treewidth, such as a chain or a tree. For a first-order chain,
$$ \phi(x, y) = \sum_{t=1}^{n} \big( \phi_{\mathrm{E}}(x, t, y_t) + \phi_{\mathrm{T}}(y_{t-1}, y_t) \big), \qquad y_0 = \text{START}, $$
with emission features of one position and transition features of two neighboring labels.

**Loss and goal.** A task loss $\Delta(y, \hat y) \ge 0$, with $\Delta(y, y) = 0$, for example the Hamming loss $\Delta(y, \hat y) = |\{t : y_t \ne \hat y_t\}|$ for sequences, or one minus the F1 score of the constituents for parses. The goal is weights $w$ with a small expected loss $\mathbb{E}[\Delta(y, h_w(x))]$.

[Multiclass classification](/multiclass-classification/) is the special case $\mathcal{Y} = \{1, \ldots, K\}$ with $\phi(x, y) = e_y \otimes x$, the input copied into the block of class $y$. Structured prediction differs because $|\mathcal{Y}(x)|$ is exponential and the decoder must exploit the structure of $\phi$.

## Variants

- **Output structures.** Sequences (part-of-speech tagging, named entity recognition, gene finding), trees (constituency and dependency parsing), alignments and matchings (word alignment in translation), segmentations and labelings of grid graphs (image segmentation), and sets or rankings ([learning to rank](/learning-to-rank/)).
- **Probabilistic versus margin based.** A CRF defines $p(y \mid x) \propto \exp(w^{\top} \phi(x, y))$ and fits $w$ by conditional maximum likelihood. Perceptrons and structured SVMs need only the argmax, not the normalizer, and can use any loss $\Delta$ in training.
- **Generative models.** A [hidden Markov model](/hidden-markov-model/) or a probabilistic grammar fits $p(x, y)$ and decodes with the same dynamic programs. CRFs and the structured perceptron are their discriminative partners; see [generative versus discriminative models](/generative-vs-discriminative-models/).
- **Exact versus approximate inference.** When the factor graph has cycles or high-order factors, exact decoding is NP-hard in general, and learners use [beam search](/beam-search/), LP relaxations, graph cuts or [MAP inference](/map-inference/) by message passing.
- **Search-based prediction.** SEARN, DAgger and related methods build the output one decision at a time and learn the decision policy, with no global decoder.

## Examples

**A toy tagger.** Labels D (determiner), N (noun) and V (verb). Training data: "the dog runs" tagged D N V, and "a cat sees the dog" tagged D N V D N. Features are the emission $(\mathrm{E}, \text{label}, \text{word})$ and the transition $(\mathrm{T}, \text{previous label}, \text{label})$, so $\phi$ counts these pairs.

*First perceptron step.* With $w = 0$ every tagging scores 0, and the tie rule of Viterbi, which prefers the earlier label, returns D D D for "the dog runs". This is a mistake, so the perceptron adds $\phi(x, \text{D N V}) - \phi(x, \text{D D D})$:

| feature | change |
| --- | --- |
| (E, N, dog), (E, V, runs) | +1 each |
| (E, D, dog), (E, D, runs) | −1 each |
| (T, D, N), (T, N, V) | +1 each |
| (T, D, D) | −2 |

The features shared by both taggings, (E, D, the) and (T, START, D), cancel.

*Second sentence.* For "a cat sees the dog" the weights now give D N V D N the score $1 + 1 + 1 + 1 = 4$: the transitions D→N twice and N→V once, and the emission (N, dog). This is the maximum, so the perceptron makes no update, although it has never seen "a", "cat" or "sees". The transition features carry what it learned to new words.

*Viterbi trellis.* For "the cat sees" under the same weights, all emission weights are 0. Let $V_t(a)$ be the best score of a tagging of the first $t$ words that ends in label $a$, and record the best previous label:

| label | $t = 1$ (the) | $t = 2$ (cat) | $t = 3$ (sees) |
| --- | --- | --- | --- |
| D | 0 | 0 (from N) | 1 (from N) |
| N | 0 | 1 (from D) | 1 (from D) |
| V | 0 | 1 (from N) | 2 (from N) |

The best final cell is V with score 2. Following the pointers back gives V ← N ← D, so the prediction is D N V. Brute force over all $3^3 = 27$ taggings gives the same best score.

*Loss-augmented decoding.* With $w = 0$ and the Hamming loss, the most violating tagging of "the dog runs" gets every word wrong, for a value of 3. The structured hinge loss of the example is $3 + 0 - 0 = 3$.

## Known algorithms

**Inference.** For a first-order chain, Viterbi is a dynamic program over the trellis, in $O(n K^2)$ time and $O(n K)$ space. Below, $e_t(a)$ is the emission weight of label $a$ at position $t$ and $\tau(b, a)$ the transition weight. For loss-augmented decoding with the Hamming loss, $e_t(a)$ gets $+1$ when $a \ne y_t$, since this loss also splits over positions.

```pseudo id=main
VITERBI(w, x)
L1  for each label a do V[1][a] ← τ(START, a) + e_1(a)
L2  for t ← 2 to n do
L3      for each label a do
L4          b* ← the first label b that maximizes V[t−1][b] + τ(b, a)
L5          V[t][a] ← V[t−1][b*] + τ(b*, a) + e_t(a)
L6          B[t][a] ← b*
L7  y_n ← the first label a that maximizes V[n][a]
L8  for t ← n down to 2 do
L9      y_{t−1} ← B[t][y_t]
L10 return (y_1, …, y_n)
```

Line L5 is correct because the best tagging that ends in $a$ at position $t$ extends a best tagging that ends in some $b$ at $t - 1$: the score is a sum of local terms. For trees, CKY and the inside algorithm run in $O(n^3)$ times the grammar size. Maximum weight bipartite matching solves alignment, and minimum cuts solve binary labelings with submodular pairwise terms.

**Structured perceptron** (Collins 2002). Start with $w = 0$. For each example, predict $\hat y = h_w(x_i)$. If $\hat y \ne y_i$, set $w \leftarrow w + \phi(x_i, y_i) - \phi(x_i, \hat y)$. Collins' Theorem 1: if some unit vector $u$ separates the data with margin $\delta > 0$, that is $u^{\top}\phi(x_i, y_i) - u^{\top} \phi(x_i, z) \ge \delta$ for all $i$ and all $z \ne y_i$, and $\lVert \phi(x_i, y_i) - \phi(x_i, z) \rVert \le R$, then the algorithm makes at most $R^2 / \delta^2$ mistakes. The proof is that of the [perceptron convergence theorem](/perceptron-convergence-theorem/): it only uses that $\hat y$ is an argmax, so it holds for any exact decoder, and the bound does not depend on $|\mathcal{Y}|$. The averaged perceptron returns the mean of the weight vectors over all steps, which generalizes much better in practice.

**Conditional random fields.** Maximize $\sum_i \log p_w(y_i \mid x_i)$, a concave function. Its gradient is $\sum_i \big(\phi(x_i, y_i) - \mathbb{E}_{p_w(y \mid x_i)} \phi(x_i, y)\big)$, and the [forward-backward algorithm](/forward-backward-algorithm/) computes the expected features of a chain in $O(n K^2)$.

**Structured SVMs.** Minimize
$$ \frac{1}{2}\lVert w \rVert^2 + \frac{C}{N} \sum_{i=1}^N \Big( \max_{y \in \mathcal{Y}(x_i)} \big[ \Delta(y_i, y) + w^{\top} \phi(x_i, y) \big] - w^{\top} \phi(x_i, y_i) \Big). $$
The bracket is the structured hinge loss, a convex upper bound on $\Delta(y_i, h_w(x_i))$. In constraint form there is one margin constraint for each $y$, exponentially many. Tsochantaridis et al. (2005) solve it by a [cutting plane method](/cutting-plane-method/): find the most violated constraint by loss-augmented inference, $\arg\max_y \Delta(y_i, y) + w^{\top} \phi(x_i, y)$, add it, and re-solve the [quadratic program](/quadratic-programming/). They prove the number of iterations needed for a given precision $\epsilon$ is polynomial and does not depend on $|\mathcal{Y}|$. They also give slack rescaling, which multiplies the slack by $\Delta$ instead of adding $\Delta$ to the margin; it is harder to decode. Max-margin Markov networks (Taskar, Guestrin and Koller 2003) solve the same margin rescaled problem through a factored dual. Subgradient descent, as in the implementation on this page, and block coordinate Frank-Wolfe are simpler alternatives.

**Implementation on this page.** First-order chain features, Viterbi with optional Hamming loss augmentation, brute-force decoding for tests, the structured perceptron with exact averaging, and the structured hinge loss with full subgradient steps. The tests check Viterbi and loss-augmented Viterbi against brute force over all label sequences, the structured hinge loss against the Hamming loss of the prediction, and Collins' mistake bound on data labeled by a random weight vector, with $R$ and $\delta$ computed by brute force.

## Bounds

- **Size of the output space.** $K^n$ taggings, the Catalan number of binary trees on $n$ leaves, $n!$ matchings. Brute force decoding costs $O(K^n n)$ for a chain, which is why decoding must use the structure.
- **Exact chain decoding.** $O(n K^2)$ for first order, $O(n K^{m+1})$ for order $m$ dependencies.
- **Hardness of general decoding.** MAP inference in a general pairwise Markov random field is NP-hard, so learning methods that call an exact decoder are intractable for general structures. With approximate decoders the perceptron and SVM guarantees can fail, and the learning analysis must account for the approximation.
- **Mistakes and margins.** The structured perceptron makes at most $R^2/\delta^2$ mistakes on separable data, and Collins also bounds the mistakes on nonseparable data in terms of how far the data are from a margin $\delta$.
- **Upper bounds on the task loss.** For every $w$, the structured hinge loss is at least $\Delta(y_i, h_w(x_i))$: take $y = h_w(x_i)$ in the max, and use $w^{\top} \phi(x_i, h_w(x_i)) \ge w^{\top} \phi(x_i, y_i)$. So driving the hinge loss to 0 drives the training loss to 0.

## Reductions

- **To multiclass classification.** Each output is one class, with $\phi$ shared across classes. This is exact but useless without a decoder, because the number of classes is exponential.
- **To independent per-part classifiers.** Predicting each tag alone drops the transition features. It is fast but cannot model constraints such as "an I-tag follows a B-tag or an I-tag".
- **Decoding to shortest paths.** Viterbi is a longest path in a directed acyclic graph with $nK + 2$ nodes (a [DP on a DAG](/dp-on-dag/)), and CKY is a dynamic program over spans.
- **Learning to cost-sensitive classification.** SEARN (Daumé, Langford and Marcu 2009) reduces structured prediction to a sequence of cost-sensitive classification problems over search decisions.
- **Reranking.** Generate the top $k$ outputs with a simple model and rerank them with richer features, which reduces the problem to [learning to rank](/learning-to-rank/) over a short list.

## Applications

- **Natural language processing.** Part-of-speech tagging, chunking, named entity recognition, word segmentation, and dependency and constituency parsing. The averaged structured perceptron and CRFs were the standard taggers before neural networks, and neural taggers still often put a CRF layer and Viterbi decoding on top.
- **Speech and handwriting.** Alignment of an input signal to a label sequence.
- **Computational biology.** Gene finding, protein secondary structure, and sequence alignment with learned scores.
- **Computer vision.** Image segmentation and pose estimation with graph-structured outputs, trained as structured SVMs (Nowozin and Lampert 2011).

## References
