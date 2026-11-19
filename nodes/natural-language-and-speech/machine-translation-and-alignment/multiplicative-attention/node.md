---
tag: E826M9
kind: algorithm
slug: multiplicative-attention
name: Multiplicative attention
aliases:
- Luong attention
- bilinear attention
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Score each encoder state by its dot product, or bilinear form, with the current decoder state, then take the softmax-weighted sum, over all states or a local window.
model: real-ram
complexity:
  vars: {S: the number of source states, d: the size of the states, D: the half width of the local window}
  time: {worst: "Θ(S d + d²)"}
  space: {extra: "Θ(S + d)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2015
  people: [Minh-Thang Luong, Hieu Pham, Christopher D. Manning]
  note: Luong, Pham and Manning published global and local attention with the dot, general and concat scores at EMNLP 2015, and gained 5.0 BLEU over a non-attentional baseline on WMT'14 English to German.
prereqs: [encoder-decoder-model, softmax-regression, log-sum-exp-trick]
see_also: [additive-attention, scaled-dot-product-attention, multi-head-attention, transformer, word-alignment, recurrent-neural-network-language-model, backpropagation-through-time, beam-search]
sources:
  - paper: arxiv:1508.04025
    title: Minh-Thang Luong, Hieu Pham and Christopher D. Manning, Effective Approaches to Attention-based Neural Machine Translation, EMNLP 2015
    locator: "Section 3 (the attentional state h~ = tanh(W_c [c; h_t])), Section 3.1 (global attention and the dot, general and concat scores), Section 3.2 (local-m and local-p, sigma = D/2), Section 3.3 (input feeding), Section 4.1 (D = 10) and Table 1 (WMT'14 English to German)"
  - paper: arxiv:1409.0473
    title: Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio, Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015
    locator: "Section 3.1 and Appendix A.2.2 (the additive score with the previous decoder state)"
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: "Section 3.2.1 (scaled dot-product attention and the factor 1/sqrt(d_k))"
---

Multiplicative attention lets the decoder of a recurrent [encoder-decoder model](/encoder-decoder-model/) look at the source states at each output step. It scores each source state $\bar h_s$ against the current decoder state $h_t$ by a product: the dot product $h_t^\top \bar h_s$ or the bilinear form $h_t^\top W_a \bar h_s$. A softmax turns the scores into weights, and the weighted sum of the source states is the context. Luong, Pham and Manning (2015) defined it with a global form over all source states and a local form over a window. It differs from [scaled dot-product attention](/scaled-dot-product-attention/) in two ways: it has no factor $1/\sqrt{d}$, and it compares the decoder state with the source states directly, with no separate query, key and value projections.

## In plain words

A translation model keeps one vector for each source word. At each output step, the decoder has a vector for what it is about to write.

Multiplicative attention measures how well each source vector matches the decoder vector by multiplying them coordinate by coordinate and adding the results. The general form first passes the source vector through a learned matrix. A large product means a good match.

The scores become weights that are positive and sum to 1, and the decoder takes the weighted average of the source vectors. It mixes this average with its own state to choose the next word.

The local form looks only at a window of source words around a predicted position. This saves work on long sentences and makes the weights focus on one place.

## The problem

The input is the decoder state $h_t \in \mathbb{R}^d$ at output step $t$, the source states $\bar h_1, \ldots, \bar h_S \in \mathbb{R}^d$, a score function and the parameters it needs. The score is one of

$$\mathrm{dot}: h_t^\top \bar h_s, \qquad \mathrm{general}: h_t^\top W_a \bar h_s, \qquad \mathrm{concat}: v_a^\top \tanh(W_a [h_t; \bar h_s]).$$

Global attention uses all positions $s = 1, \ldots, S$. Local attention uses the window $|s - p_t| \le D$, where $p_t = t$ for local-m (monotonic) and $p_t = S \cdot \mathrm{sigmoid}(v_p^\top \tanh(W_p h_t))$ for local-p (predictive). The output is the weights $a_t(s)$, the context $c_t = \sum_s a_t(s) \bar h_s$, and the attentional state $\tilde h_t = \tanh(W_c [c_t; h_t])$, from which the model computes the output distribution $\mathrm{softmax}(W_s \tilde h_t)$.

The state $h_t$ is the top layer of the decoder after step $t$, so the path is $h_t \to a_t \to c_t \to \tilde h_t$. [Additive attention](/additive-attention/) of Bahdanau et al. uses the previous state $s_{t-1}$ and feeds the context into the next recurrent step instead.

## The algorithm

```pseudo id=main
MULTIPLICATIVE-ATTENTION(h_t, h̄_1 .. h̄_S, score, local, D)
L1  if local is none then K ← {1, ..., S}
L2  else p ← t (local-m) or S · sigmoid(v_pᵀ tanh(W_p h_t)) (local-p); K ← {s : |s - p| ≤ D, 1 ≤ s ≤ S}
L3  for each s in K do
L4      e_s ← h_tᵀ h̄_s (dot), h_tᵀ W_a h̄_s (general) or v_aᵀ tanh(W_a [h_t; h̄_s]) (concat)
L5  a ← SOFTMAX(e_s over s in K)               ▷ subtract the maximum before exp
L6  if local is p then a_s ← a_s · exp(-(s - p)² / (2 σ²)) with σ = D / 2
L7  c ← Σ_{s in K} a_s h̄_s                      ▷ a_s = 0 outside K
L8  h̃ ← tanh(W_c [c; h_t])
L9  return c, a, h̃
```

Lines L1 and L2 choose the positions. For local-p, $p$ is a real number in $[0, S]$, so the window has up to $2D + 1$ positions and is cut at the ends of the sentence. Line L4 is the score. For the general score, an implementation computes $W_a \bar h_s$ once per source sentence and reuses it at every output step. Line L5 is a softmax over the window with the [log-sum-exp trick](/log-sum-exp-trick/). Line L6 multiplies the weights of local-p by a Gaussian centred at $p$. As in the paper, the weights are not normalized again, so they sum to less than 1. Line L8 combines the context with the decoder state.

**How it differs from the other attention pages.** [Scaled dot-product attention](/scaled-dot-product-attention/) computes $\mathrm{softmax}(q^\top k_s / \sqrt{d_k})$ with $q$, $k_s$ and the values $v_s$ produced by separate learned projections, and it runs many queries at once as one matrix product. The general score with $W_a = I / \sqrt{d}$ gives exactly scaled dot-product attention for one query whose keys and values are the source states (a theorem). Without the scale, dot products of large vectors are large, and the softmax becomes very sharp. [Additive attention](/additive-attention/) puts a tanh between the decoder state and the source state, so its scores are bounded but cannot be computed as one matrix product. The concat score here is the additive score with $h_t$ in place of $s_{t-1}$.

## Example

Take the dot score, $h_t = (1, 0)$ and three source states $\bar h_1 = (1, 0)$, $\bar h_2 = (0, 1)$, $\bar h_3 = (-1, 0)$, the same states as on the [additive attention](/additive-attention/) page.

| $s$ | $e_s = h_t^\top \bar h_s$ | $\exp(e_s)$ | $a_t(s)$ |
|---|---|---|---|
| 1 | 1 | 2.7183 | 0.6652 |
| 2 | 0 | 1 | 0.2447 |
| 3 | -1 | 0.3679 | 0.0900 |

The context is $c_t = 0.6652\,(1, 0) + 0.2447\,(0, 1) + 0.0900\,(-1, 0) = (0.5752, 0.2447)$. The largest weight goes to $\bar h_1$, which points in the same direction as $h_t$. With the additive score and $W = U = I$, $v = (1, 1)$, the largest weight went to $\bar h_2$ instead, because the tanh saturates.

With local-m at $t = 2$ and $D = 0$, the window is $\{2\}$, and all the weight goes to $\bar h_2$ whatever the scores.

## Correctness

The claim is that the procedure returns the weights, the context and the attentional state of the definition. For global attention and local-m the weights are non-negative and sum to 1, so $c_t$ is a convex combination of the states in the window. For local-p each weight is at most its softmax value, and the sum is at most 1. Subtracting the maximum at line L5 multiplies the numerator and the denominator by the same factor, so it does not change the softmax. The general score with $W_a = I$ is the dot score, and the concat score is the additive form $v_a^\top \tanh(W_1 h_t + W_2 \bar h_s)$. The gradients of a loss $g^\top \tilde h_t$ for the general score follow from the chain rule and the softmax Jacobian. These are theorems; the full proof is in the proofs file. That the weights look like a word alignment is a measurement on trained models.

## Complexity

In the [real RAM](/real-ram/) model, one global step with the dot score costs $\Theta(S d)$ for the scores and the context, and line L8 costs $\Theta(d^2)$, so a step costs $\Theta(S d + d^2)$. The general score costs $\Theta(S d^2)$ per step if $W_a \bar h_s$ is computed each time, and $\Theta(S d^2)$ once per sentence plus $\Theta(S d)$ per step if it is kept. The concat score with a hidden size $n$ costs $\Theta(S n d)$ per step. Local attention replaces $S$ by $\min(S, 2D + 1)$ and adds $\Theta(d^2)$ for $p_t$ in local-p. The extra space is $\Theta(S + d)$ for the scores, the weights and the context. A target sentence of $T$ words costs $T$ times one step, so global attention makes $\Theta(T S)$ score evaluations, and local attention makes $\Theta(T D)$.

## Properties

- **Weights are a distribution.** For global attention and local-m (a theorem). For local-p the sum is at most 1.
- **Unbounded scores.** The dot and general scores grow with the size of the vectors, so the softmax can become very sharp. The additive score is bounded by $\|v\|_1$.
- **Same sizes.** The dot score needs $h_t$ and $\bar h_s$ of the same size. The general score allows different sizes through $W_a$.
- **Fast.** The dot scores of all source states are one product of a matrix and a vector, and the scores of all output steps in a batch are a product of two matrices.
- **Differentiable.** All lines are smooth except the window edges of local-p, which change only on a set of measure zero.
- **Current state.** The score uses $h_t$, so attention comes after the recurrent step, and the decoder needs input feeding to see the past contexts.

## Variants and improvements

- **Input feeding.** Luong et al. feed $\tilde h_{t-1}$ into the decoder input at step $t$, so the model knows its past attention decisions (Section 3.3). In Table 1 this added 1.3 BLEU to global attention (a measurement).
- **Location-based score.** The paper also tries $a_t = \mathrm{softmax}(W_a h_t)$, which ignores the source states and predicts the weights from the decoder state alone.
- **Scaled dot product.** The [transformer](/transformer/) divides the dot product by $\sqrt{d_k}$ and uses separate projections for queries, keys and values, in [multi-head attention](/multi-head-attention/).
- **Additive score.** [Additive attention](/additive-attention/) uses a network with one hidden layer, and its scores are bounded.
- **Monotonic and sparse attention.** Later work replaces the window of local attention by learned monotonic alignments or sparse weights; these are outside the scope of this page.

## When to use it

Use the dot or general score in a recurrent encoder-decoder when speed matters and the states have a moderate size. Use the general score when the decoder and encoder states have different sizes. Use local attention for long inputs where the alignment is roughly monotonic. In a transformer, use [scaled dot-product attention](/scaled-dot-product-attention/), which adds the scale and the projections.

## Pitfalls

- **No scale with large states.** With large $d$ the dot products can be large, and the softmax puts nearly all weight on one position, which gives small gradients. Divide by $\sqrt{d}$ or use the general score with a well-scaled $W_a$.
- **Renormalizing local-p.** The paper does not normalize the weights again after the Gaussian. An implementation that does gives a different model.
- **Positions from 0 or 1.** The window $|s - p| \le D$ depends on whether positions start at 0 or at 1. Choose one and keep it.
- **An empty window.** For local-m with $t > S + D$ the window is empty. Clip $p_t$ or fall back to global attention.
- **Previous against current state.** Mixing the conventions of Bahdanau et al. ($s_{t-1}$ before the step) and Luong et al. ($h_t$ after the step) gives a model that matches neither paper.

## Implementations

The code takes the decoder state, the source states and the weight matrices as given and implements the scores, the global and local weights, the context, the attentional state and the gradients of the general score; it does not train a network.

## History

Minh-Thang Luong, Hieu Pham and Christopher D. Manning published the paper at EMNLP 2015, a few months after additive attention. They simplified the attention path to $h_t \to a_t \to c_t \to \tilde h_t$, compared the dot, general and concat scores and a location-based score, and proposed local attention as a mix of the soft attention of Bahdanau et al. and the hard attention of image captioning. Their models had 4 LSTM layers with 1000 cells, a vocabulary of 50,000 words, and $D = 10$ (Section 4.1). On WMT'14 English to German newstest2014, with tokenized BLEU, global attention with the location score raised the baseline with reversal and dropout from 14.0 to 16.8 BLEU, input feeding raised it to 18.1, and local-p attention with the general score reached 19.0, a gain of 5.0 over the non-attentional baseline. Unknown word replacement gave 20.9, and an ensemble of 8 models gave 23.0 (Table 1, measurements). The multiplicative form became the common choice in recurrent models, and the transformer of 2017 added the scale and the projections.

## References
