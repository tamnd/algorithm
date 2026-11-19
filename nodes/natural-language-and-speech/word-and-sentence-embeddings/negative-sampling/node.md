---
tag: 9W46SG
kind: technique
slug: negative-sampling
name: Negative sampling
aliases:
- skip-gram with negative sampling
- SGNS
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Train word vectors by logistic loss that tells observed word-context pairs from k random pairs drawn from a smoothed unigram distribution.
model: real-ram
complexity:
  vars: {d: "the dimension of the vectors", k: "the number of noise words per pair", V: "the vocabulary size, the number of types"}
  time: {worst: "O(k (d + log V))"}
  space: {extra: "O(V)"}
history:
  year: 2013
  people: [Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean]
  note: "Mikolov, Sutskever, Chen, Corrado and Dean introduced negative sampling in 2013 as a simplification of noise-contrastive estimation for the skip-gram model, together with the subsampling of frequent words."
prereqs: [skip-gram-model, logistic-regression]
see_also: [noise-contrastive-estimation, sgns-implicit-factorization-theorem, hierarchical-softmax, continuous-bag-of-words, pointwise-mutual-information, importance-sampling, alias-method, node2vec]
sources:
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: "the negative sampling objective, the noise distribution U(w)^(3/4)/Z, the range of k, the subsampling of frequent words with t = 1e-5, and the empirical comparison with hierarchical softmax and NCE"
  - paper: "Chris Dyer, Notes on noise contrastive estimation and negative sampling, arXiv:1410.8251, 2014 (preprint)"
    title: Dyer 2014
    locator: the difference between NCE, which estimates a normalized model, and negative sampling, which trains a binary classifier
  - paper: "Yoav Goldberg and Omer Levy, word2vec explained: deriving Mikolov et al.'s negative-sampling word-embedding method, arXiv:1402.3722, 2014 (preprint)"
    title: Goldberg and Levy 2014
    locator: the negative sampling objective written over the word and context pairs of a corpus, and the remark that it does not model the conditional distribution of contexts
  - paper: "Omer Levy and Yoav Goldberg, Neural word embedding as implicit matrix factorization, Advances in Neural Information Processing Systems 27 (NIPS 2014), pages 2177 to 2185"
    title: Levy and Goldberg 2014
    locator: "Section 3.1 (the optimum of each cell of the objective, PMI(w, c) - log k)"
---

Negative sampling trains word vectors without the softmax over the vocabulary. For each observed pair of a word $w$ and a context word $c$, it draws $k$ noise words from a fixed distribution, and it trains a [logistic regression](/logistic-regression/) on the dot products to give a high score to the observed pair and a low score to the $k$ noise pairs. One pair costs $k + 1$ dot products instead of $|V|$. Mikolov, Sutskever, Chen, Corrado and Dean (2013) introduced it for the [skip-gram model](/skip-gram-model/). It is a simplification of [noise-contrastive estimation](/noise-contrastive-estimation/), but it is not an estimator of the softmax model: the trained scores are not normalized probabilities.

## In plain words

The full model asks "which word, out of every word in the vocabulary, is the context?" That needs a score for every word, and the vocabulary can have millions of words.

Negative sampling asks an easier question many times. It takes a real pair of words from the text and a few fake pairs, made by putting the same word next to random words. A frequent word is chosen as a fake more often, but less often than its share of the text. The model only has to say "real" or "fake" for each pair.

To do this well, it must pull the vectors of real pairs together and push the vectors of fake pairs apart. Words that occur in the same kinds of places end up with similar vectors. Each step looks at a few words only, so training is fast.

## When it applies

Use it when a model scores a pair by a cheap function, here the dot product $\vec u_c \cdot \vec v_w$, the output space is large, and you need the vectors, not calibrated probabilities. The signals are a softmax over a large vocabulary in the loss, a training set of observed pairs, and an end use (similarity, analogy, features for another model) that does not need $P(c \mid w)$. When you need a normalized distribution, for example for perplexity, use [noise-contrastive estimation](/noise-contrastive-estimation/) or the [hierarchical softmax](/hierarchical-softmax/) instead.

## The template

The holes are the noise distribution $P_n$, the number $k$ of noise words and the score $s(w, c) = \vec u_c \cdot \vec v_w$. The loss of one observed pair $(w, c)$ with noise words $n_1, \ldots, n_k$ is

$$\ell(w, c) = -\log \sigma(\vec u_c \cdot \vec v_w) - \sum_{i=1}^{k} \log \sigma(-\vec u_{n_i} \cdot \vec v_w),$$

where $\sigma(x) = 1/(1 + e^{-x})$. Mikolov et al. take $P_n(u) = \#(u)^{3/4} / Z$, the unigram distribution raised to the power $3/4$ and renormalized, a value they chose from their measurements.

```pseudo id=main
NEGATIVE-SAMPLING-STEP(w, c, k, P_n, η)
L1  draw n_1, ..., n_k from P_n, and skip a draw equal to c
L2  for each (x, y) in (c, 1), (n_1, 0), ..., (n_k, 0) do
L3      e ← σ(u_x · v_w) - y                     ▷ the error of the logistic unit
L4      g_v ← g_v + e u_x                        ▷ the gradient for v_w
L5      g_x ← g_x + e v_w                        ▷ the gradient for u_x
L6  u_x ← u_x - η g_x for each x; v_w ← v_w - η g_v
```

Line L1 draws the noise words. Line L3 is the error of the logistic unit: $\sigma(\cdot) - 1$ for the observed pair and $\sigma(\cdot)$ for a noise pair. Lines L4 and L5 are the two halves of the gradient of $\ell$, since $\frac{d}{dx}\big(-\log\sigma(x)\big) = \sigma(x) - 1$ and $\frac{d}{dx}\big(-\log\sigma(-x)\big) = \sigma(x)$. Line L6 applies the updates after all $k + 1$ terms are computed, so $\vec v_w$ is the same vector in each term. A training pass emits the pairs of the [skip-gram model](/skip-gram-model/) and runs this step on each.

**Example.** Take $\vec v_w = (1, 0)$, the observed context $\vec u_c = (1, 1)$ and two noise words with $\vec u_{n_1} = (0.5, 0)$ and $\vec u_{n_2} = (-1, 0.5)$. The scores are $1$, $0.5$ and $-1$. The loss is

$$-\log\sigma(1) - \log\sigma(-0.5) - \log\sigma(1) = 0.3133 + 0.9741 + 0.3133 = 1.6006.$$

The errors of line L3 are $\sigma(1) - 1 = -0.2689$, $\sigma(0.5) = 0.6225$ and $\sigma(-1) = 0.2689$, and the gradient for $\vec v_w$ is $-0.2689(1, 1) + 0.6225(0.5, 0) + 0.2689(-1, 0.5) = (-0.2267, -0.1345)$. A gradient step moves $\vec v_w$ toward $\vec u_c$ and away from $\vec u_{n_1}$, the noise word with the highest score.

**The noise distribution.** For counts $(8, 4, 2, 1, 1)$, the unigram distribution is $(0.5, 0.25, 0.125, 0.0625, 0.0625)$, and the power $3/4$ gives $(0.4222, 0.2510, 0.1493, 0.0888, 0.0888)$. The power moves mass from frequent words to rare words. A sampler with a cumulative table and binary search draws a word in $O(\log V)$ time; the [alias method](/alias-method/) or the large table of the word2vec tool draws in $O(1)$.

**What the optimum is.** Let $\#(w, c)$ be the number of observed pairs, $\#(w)$ and $\#(c)$ the marginal counts and $|D|$ the number of pairs. In expectation over the noise, the terms of the objective that hold the score $x = \vec u_c \cdot \vec v_w$ are $\#(w, c)\log\sigma(x) + k\,\#(w)\#(c)/|D| \cdot \log\sigma(-x)$. This is concave in $x$, and its maximum is at

$$x^* = \log\frac{\#(w, c)\,|D|}{\#(w)\,\#(c)} - \log k = \mathrm{PMI}(w, c) - \log k,$$

with PMI estimated with unigram context counts (for the smoothed noise, with $\#(c)^{3/4}$ in their place). The [SGNS factorization theorem](/sgns-implicit-factorization-theorem/) turns this into a statement about $W C^\top$.

## Classic examples

- **[Skip-gram model](/skip-gram-model/).** The original use: each (center, context) pair of a window is one observed pair.
- **[Continuous bag-of-words](/continuous-bag-of-words/).** The same step with the mean of the context vectors in place of $\vec v_w$ and the center word as the observed output.
- **[Subword information embeddings](/subword-information-embeddings/).** The same loss, with $\vec v_w$ replaced by the sum of the vectors of the character n-grams of $w$. The gradient of line L4 goes to every n-gram row.
- **[node2vec](/node2vec/).** Skip-gram on random walks over a graph, trained with negative sampling, so the observed pairs are nodes that occur near each other on a walk.

## Variations

- **Subsampling of frequent words.** Mikolov et al. discard each token of a word of relative frequency $f$ with probability $1 - \sqrt{t/f}$, with $t = 10^{-5}$ (a heuristic). A word with $f = 10^{-3}$ is discarded with probability $0.9$, and words with $f \le t$ are always kept. The released word2vec code uses a slightly different formula. Subsampling speeds up training and also widens the effective window.
- **The number of noise words.** Mikolov et al. report that $k$ from 5 to 20 is useful for small data sets and $k$ from 2 to 5 for large ones. Each value of $k$ shifts the optimum by $-\log k$.
- **The power of the noise.** The power $1$ gives the unigram distribution and the power $0$ the uniform one. The power $3/4$ is a choice from measurements, not a derived value.
- **Noise-contrastive estimation.** [NCE](/noise-contrastive-estimation/) uses the logit $s(w, c) - \log(k P_n(c))$ in place of $s(w, c)$. With this correction the optimum is the normalized conditional distribution. Negative sampling is the case where the correction term is dropped, which is the same as NCE only when $k P_n(c) = 1$ for every $c$, that is uniform noise with $k = |V|$.
- **Other uses.** The same pattern trains embeddings of nodes, items and sentences: any model with a dot-product score over a large set of candidates.

## Pitfalls

- **Reading $\sigma(\vec u_c \cdot \vec v_w)$ as $P(c \mid w)$.** The scores of one word do not sum to 1 over the contexts, and their optimum depends on $k$ and on $P_n$. Do not report a perplexity from a model trained with negative sampling.
- **The sign of the noise term.** The noise term is $\log\sigma(-x)$, not $\log(1 - x)$ or $-\log\sigma(x)$. With the wrong sign, line L3 uses $y = 1$ for the noise words and all vectors collapse together.
- **Updating $\vec v_w$ inside the loop.** If line L6 moves $\vec v_w$ after each term, the later terms see a different vector and the step is not a gradient step of $\ell$. Accumulate $g_v$ first, as the word2vec code does.
- **Normalizing before the power.** $P_n$ is $\#(u)^{3/4}$ divided by the sum of $\#(u')^{3/4}$, not the unigram probability raised to $3/4$ without renormalization.
- **The true context as noise.** For a small vocabulary, a noise draw often equals $c$, and the two terms then pull $\vec u_c$ in opposite directions. The word2vec code skips such a draw (line L1), so a step can have fewer than $k$ noise words.

## Exercises

1. Show that the cell objective $a\log\sigma(x) + b\log\sigma(-x)$ with $a, b > 0$ is strictly concave in $x$ and has its maximum at $x = \log(a/b)$. Use it to get $x^* = \mathrm{PMI}(w, c) - \log k$.
2. For counts $(8, 4, 2, 1, 1)$, compute the noise distribution with the power $1/2$ and compare it with the values above.
3. Write the NCE logit $s - \log(k P_n(c))$ and show that its optimum is $s = \log P(c \mid w)$ when the model can represent every distribution. Then show that negative sampling gives the same optimum only when $k P_n(c) = 1$ for all $c$.

## References
