---
tag: 3X7CGK
kind: algorithm
slug: additive-attention
name: Additive attention
aliases:
- Bahdanau attention
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: At each decoder step score each encoder state by a small feedforward network of it and the decoder state, and take the softmax-weighted sum.
model: real-ram
complexity:
  vars: {J: the number of encoder states, a: the size of the attention layer, d: the size of the encoder and decoder states}
  time: {worst: "Θ(J a d)"}
  space: {extra: "Θ(J + a)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2014
  people: [Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio]
  note: Bahdanau, Cho and Bengio posted RNNsearch on arXiv in 2014 and published it at ICLR 2015. It removed the fixed-length bottleneck of the recurrent encoder-decoder and started attention in neural translation.
prereqs: [encoder-decoder-model, softmax-regression, log-sum-exp-trick]
see_also: [multiplicative-attention, scaled-dot-product-attention, multi-head-attention, transformer, recurrent-neural-network-language-model, word-alignment, pointer-generator-network, listen-attend-and-spell]
sources:
  - paper: arxiv:1409.0473
    title: Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio, Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015
    locator: "Section 3.1 (equations 5 and 6, the context and the weights), Section 3.2 (the bidirectional encoder), Table 1 (BLEU on newstest2014 English to French), Appendix A.2.2 (the alignment model) and A.2.3 (n = n' = 1000)"
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: "Section 3.2.1 (the comparison of additive and dot-product attention)"
---

Additive attention lets the decoder of a recurrent [encoder-decoder model](/encoder-decoder-model/) look at all the encoder states at each output step, instead of one fixed vector. It scores each encoder state $h_j$ against the previous decoder state $s$ by a small network with one hidden layer, $e_j = v^\top \tanh(W s + U h_j)$, turns the scores into weights by a softmax, and returns the weighted sum of the encoder states as the context. Bahdanau, Cho and Bengio (2015) introduced it in the RNNsearch model. It differs from [scaled dot-product attention](/scaled-dot-product-attention/) in its score: a learned network with a tanh, not a scaled dot product of a query and a key.

## In plain words

A translation model reads the source sentence and keeps one vector for each source word. When it writes the next target word, it should look mostly at the source words that this target word translates.

Additive attention gives each source word a score. It takes the vector of the decoder (what has been written so far) and the vector of the source word, maps both into a common space, adds them, squashes the sum with tanh, and reads off one number with a learned vector.

The scores become weights that are positive and sum to 1. The decoder then gets the weighted average of the source vectors.

The weights act as a soft word alignment. They are learned together with the rest of the network, with no alignment data.

## The problem

The input is a decoder state $s \in \mathbb{R}^{d_s}$, encoder states $h_1, \ldots, h_J \in \mathbb{R}^{d_h}$, and the parameters $W \in \mathbb{R}^{a \times d_s}$, $U \in \mathbb{R}^{a \times d_h}$ and $v \in \mathbb{R}^{a}$, where $a$ is the size of the attention layer. Some positions may be padding and are masked. The output is

$$e_j = v^\top \tanh(W s + U h_j), \qquad \alpha_j = \frac{\exp(e_j)}{\sum_{k} \exp(e_k)}, \qquad c = \sum_{j=1}^{J} \alpha_j h_j,$$

with the sum over the positions that are not masked, and $\alpha_j = 0$ at a masked position. In RNNsearch, at output step $i$ the state is $s = s_{i-1}$, the decoder state before the word $y_i$ is emitted, and each $h_j$ is the concatenation of the forward and the backward state of a bidirectional RNN (Section 3.2). The context $c_i$ then enters the next decoder state $s_i = f(s_{i-1}, y_{i-1}, c_i)$ and the output distribution.

## The algorithm

```pseudo id=main
ADDITIVE-ATTENTION(s, h_1 .. h_J, W, U, v)
L1  q ← W s
L2  for j ← 1 to J do
L3      k_j ← U h_j                         ▷ the same at every decoder step
L4      e_j ← vᵀ tanh(q + k_j)
L5      if position j is masked then e_j ← -∞
L6  α ← SOFTMAX(e_1, ..., e_J)              ▷ subtract max_j e_j before exp
L7  c ← Σ_j α_j h_j
L8  return c, α
```

Line L1 is the query part, computed once per decoder step. Line L3 does not depend on the decoder, so an implementation computes all the keys $k_j = U h_j$ once per source sentence and reuses them at every output step. Line L4 is the network with one hidden layer of $a$ tanh units. Line L6 subtracts the largest score before the exponential, as in the [log-sum-exp trick](/log-sum-exp-trick/), so no exponential overflows. Line L7 is the context.

**How it differs from the other attention pages.** [Scaled dot-product attention](/scaled-dot-product-attention/) scores a query $q$ and a key $k$ by $q^\top k / \sqrt{d_k}$: a product of two vectors, scaled, with no hidden layer. Its scores for many queries are one matrix product $Q K^\top$, which is fast on hardware, and it needs the factor $1/\sqrt{d_k}$ because a dot product grows with the size of the vectors. The additive score passes the sum $q + k_j$ through tanh, so it is bounded by $\|v\|_1$ whatever the size of the vectors, and it needs no scale. It cannot be written as one matrix product, because the tanh comes between the query and the key. [Multiplicative attention](/multiplicative-attention/) of Luong et al. is the dot or bilinear score in recurrent models, and it uses the current decoder state $h_t$ instead of the previous one.

## Example

Take $a = 2$, $d_s = d_h = 2$, $W = U = I$, $v = (1, 1)$, the decoder state $s = (1, 0)$ and three encoder states $h_1 = (1, 0)$, $h_2 = (0, 1)$, $h_3 = (-1, 0)$. Then $q = (1, 0)$ and:

| $j$ | $q + U h_j$ | $e_j$ | $\alpha_j$ |
|---|---|---|---|
| 1 | (2, 0) | tanh 2 = 0.9640 | 0.3194 |
| 2 | (1, 1) | 2 tanh 1 = 1.5232 | 0.5588 |
| 3 | (0, 0) | 0 | 0.1218 |

The context is $c = 0.3194\,(1, 0) + 0.5588\,(0, 1) + 0.1218\,(-1, 0) = (0.1976, 0.5588)$.

The largest weight goes to $h_2$, although $s^\top h_2 = 0$ is smaller than $s^\top h_1 = 1$. A dot-product score would rank $h_1$ first. Here the tanh saturates: the first coordinate of $q + U h_1$ is already 2, and doubling it adds little, while $h_2$ raises both coordinates.

## Correctness

The claim is that the procedure returns the weights and the context of the definition, that the weights are non-negative and sum to 1, and that the masked positions get weight 0. Subtracting the maximum score at line L6 does not change the softmax, because it multiplies the numerator and the denominator by the same factor. So $c$ is a convex combination of the encoder states that are not masked. Each score satisfies $|e_j| \le \|v\|_1$, so every unmasked weight is at least $e^{-2\|v\|_1}/J$. The gradients of a loss $g^\top c$ with respect to $s$, $h_j$, $W$, $U$ and $v$ follow from the chain rule and $\tanh' = 1 - \tanh^2$. These are theorems; the full proof is in the proofs file. That the weights look like a word alignment is an observation on trained models (a measurement), not a property of the formula.

## Complexity

In the [real RAM](/real-ram/) model with $d_s, d_h \le d$, line L1 costs $\Theta(a d)$, line L3 costs $\Theta(a d)$ per position, and lines L4 to L7 cost $\Theta(a + d)$ per position. One decoder step from scratch costs $\Theta(J a d)$. With the keys precomputed once, a step costs $\Theta(a d + J a + J d)$, and a target sentence of $I$ words costs $\Theta(J a d + I (a d + J a + J d))$. The extra space is $\Theta(J + a)$ for the scores and the query, plus $\Theta(J a)$ if the keys are kept. Over a whole sentence pair, attention costs $\Theta(I J)$ score evaluations, which is the cost of letting every output step see every source word.

## Properties

- **Weights are a distribution.** Non-negative, summing to 1, with 0 at masked positions (a theorem).
- **Bounded scores.** $|e_j| \le \|v\|_1$ (a theorem). The weights can become sharp only if $v$ is large.
- **Different sizes.** $s$ and $h_j$ may have different sizes, because $W$ and $U$ map both into the same $a$ dimensions.
- **Differentiable.** All steps are smooth, so the alignment is learned by [backpropagation through time](/backpropagation-through-time/) with the rest of the model.
- **Content based.** The score uses only the vectors, not the positions. Position enters only through what the encoder writes into $h_j$.
- **Previous state.** In RNNsearch the score uses $s_{i-1}$, so the context is ready before the new state $s_i$ is computed.

## Variants and improvements

- **Multiplicative scores.** [Luong et al.](/multiplicative-attention/) replace the network by $s^\top h_j$ or $s^\top W_a h_j$ and use the current decoder state.
- **Scaled dot product.** The [transformer](/transformer/) uses $q^\top k / \sqrt{d_k}$ in [multi-head attention](/multi-head-attention/). Vaswani et al. (2017) state that dot-product attention is much faster and more space-efficient in practice, and that additive attention does better than dot-product attention without the scale for larger $d_k$ (a measurement they cite from other work).
- **Location-aware attention.** In speech recognition, Chorowski et al. (2015) add features of the previous weights to the score, so the attention moves forward along the input. [Listen, attend and spell](/listen-attend-and-spell/) uses content-based attention of this family.
- **Copying.** The [pointer-generator network](/pointer-generator-network/) uses the attention weights as a distribution to copy source words.
- **Coverage.** Later models add a sum of the past weights to the score, so the model does not attend to the same word again and again.

## When to use it

Use additive attention in a recurrent encoder-decoder, especially when the decoder and encoder states have different sizes or when the states are large and unscaled dot products would make the softmax too sharp. In a transformer or any model that runs many queries at once, use scaled dot-product attention, which is one matrix product and much faster on hardware.

## Pitfalls

- **Recomputing the keys.** Computing $U h_j$ again at every decoder step multiplies the cost by $d$ for no gain. Compute the keys once.
- **Masking with a large negative number.** A score of $-10^9$ in place of $-\infty$ can leave a tiny weight on padding, and in low precision it can overflow. Use $-\infty$ and handle a row with every position masked as an error.
- **No max shift.** Without line L6's subtraction, a large $\|v\|$ makes $\exp(e_j)$ overflow.
- **The wrong state.** Using $s_i$ instead of $s_{i-1}$ creates a loop: $s_i$ needs the context, and the context needs $s_i$. Luong et al. avoid this by computing the context after $s_i$ and adding a separate output layer.
- **Reading the weights as alignments.** The weights are trained for translation, not for alignment. They often look like an alignment, but they can be spread out or shifted, so they are not a replacement for a [word alignment](/word-alignment/) model.

## Implementations

The code takes the encoder states, the decoder state and the weight matrices as given and implements the scores, the weights, the context and their gradients; it does not train a network.

## History

Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio posted the paper on arXiv in September 2014 and presented it at ICLR 2015. The earlier recurrent encoder-decoder had to compress the source into one vector, and its quality dropped on long sentences. Their RNNsearch model, with additive attention over the states of a bidirectional encoder, kept its quality on long sentences. On English to French newstest2014, with the Moses tokenizer and a vocabulary of 30,000 words, RNNsearch-50 reached 26.75 BLEU against 17.82 for the encoder-decoder without attention (Table 1, a measurement). Attention then spread to speech recognition, summarization and image captioning, and in 2017 the transformer replaced the recurrence by attention alone.

## References
