---
tag: YMRYDZ
kind: algorithm
slug: scaled-dot-product-attention
name: Scaled dot-product attention
aliases:
- softmax attention
- QKV attention
area: natural-language-and-speech/language-modeling
level: core
summary: "Output softmax(Q K^T / sqrt(d_k)) V: each query gets a mix of the value vectors, weighted by how well each key matches it. Costs O(n^2 d) for n tokens."
model: real-ram
complexity:
  vars: {n: the number of queries, m: the number of keys and values, d: the size d_k of a query or key, e: the size d_v of a value}
  time: {worst: "Θ(n m (d + e))"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2017
  people: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin]
  note: Vaswani and colleagues added the factor 1/sqrt(d_k) to the dot-product attention of Luong and colleagues, and made it the only mixing step of the transformer.
prereqs: [softmax-regression, log-sum-exp-trick]
see_also: [multi-head-attention, transformer, flashattention, additive-attention, multiplicative-attention, key-value-cache, causal-language-modeling, sinusoidal-positional-encoding]
sources:
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: Section 3.2.1 (the definition, equation 1, and the footnote on the variance of q . k), Section 3.2.3 (the mask that sets illegal scores to minus infinity), Section 4 and Table 1 (cost per layer)
  - paper: "Minh-Thang Luong, Hieu Pham and Christopher D. Manning, Effective approaches to attention-based neural machine translation, Proceedings of EMNLP 2015"
    title: Luong, Pham and Manning 2015
    locator: the dot score among the score functions of global attention
  - book: isbn:9780262048644
    title: Simon J. D. Prince, Understanding Deep Learning, MIT Press 2023
    locator: Chapter 12 (Transformers), Section 12.2 (dot-product self-attention)
---

Scaled dot-product attention lets each position of a sequence read from all other positions. Each query vector is compared with every key vector by a dot product. The scores are divided by $\sqrt{d_k}$ and turned into weights by a softmax, and the output is the weighted sum of the value vectors. In matrix form the output is $\operatorname{softmax}(Q K^\top / \sqrt{d_k})\, V$, with the softmax taken over each row. It is the only step of a [transformer](/transformer/) where positions exchange information, and [multi-head attention](/multi-head-attention/) runs several copies of it side by side. For $n$ tokens attending to each other it costs $\Theta(n^2 d)$ time.

## In plain words

Each word in a sentence asks a question, holds a label, and carries a piece of content. To update one word, compare its question with the label of every word, including itself. A good match gives a high score.

Turn the scores into shares that add up to one, so that the best matches get most of the share and poor matches get almost nothing. The new value of the word is the content of all the words, mixed in those shares.

The scores are first made smaller by a fixed amount that depends on the length of the vectors. Without this, long vectors give very large scores, one word takes almost the whole share, and learning slows down.

To stop a word from looking at the words after it, give those words a score so low that their share is zero.

## The problem

The input is three matrices: the queries $Q$ of shape $n \times d_k$, the keys $K$ of shape $m \times d_k$ and the values $V$ of shape $m \times d_v$, with row $j$ of $V$ belonging to key $j$. An optional mask $M$ of shape $n \times m$ says which keys each query may see. The output is the $n \times d_v$ matrix

$$O = \operatorname{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}} + B\right) V, \qquad B_{ij} = \begin{cases} 0 & \text{if } M_{ij}, \\ -\infty & \text{otherwise,} \end{cases}$$

where the softmax of a row $s$ is $\operatorname{softmax}(s)_j = e^{s_j} / \sum_{j'} e^{s_{j'}}$ and $e^{-\infty} = 0$. Every query must see at least one key. In self-attention $Q$, $K$ and $V$ are three linear maps of the same $n$ token vectors, so $m = n$. The causal mask lets query $i$ see key $j$ only when $j \le i$; this is what [causal language modeling](/causal-language-modeling/) needs.

Why divide by $\sqrt{d_k}$: Vaswani and colleagues note in a footnote that if the components of $q$ and $k$ are independent with mean 0 and variance 1, then $q \cdot k = \sum_t q_t k_t$ has mean 0 and variance $d_k$. Dividing by $\sqrt{d_k}$ gives the scores variance 1 whatever the size, which keeps the softmax away from the flat regions where its gradient is very small.

## The algorithm

The rows of the output are independent, so the algorithm handles one query at a time. For each query it computes a row of scores, applies the mask, and takes a stable softmax: it subtracts the largest score before taking exponentials, as in the [log-sum-exp trick](/log-sum-exp-trick/).

```pseudo id=main
ATTENTION(Q, K, V, M)                  ▷ Q: n × d_k, K: m × d_k, V: m × d_v
L1  for i ← 1 to n do
L2      for j ← 1 to m do
L3          s_j ← (Q_i · K_j) / √d_k
L4          if not M_ij then s_j ← -∞
L5      μ ← max_j s_j                    ▷ finite, since query i sees a key
L6      p_j ← exp(s_j - μ) for every j;  Z ← Σ_j p_j
L7      p_j ← p_j / Z for every j
L8      O_i ← Σ_j p_j V_j
L9  return O
```

Line L3 is one row of $Q K^\top$, scaled. Line L4 adds the bias $B$. Lines L5 to L7 are the softmax: every exponent at line L6 is at most 0, so no exponential overflows, and the largest one is exactly 1, so $Z \ge 1$. Line L8 multiplies the weight row by $V$. In practice the loops are matrix products: $S = Q K^\top / \sqrt{d_k}$, a row softmax, and $P V$.

## Example

Take $d_k = 4$, so $\sqrt{d_k} = 2$, three queries, three keys and values of size 2:

$$Q = \begin{pmatrix} 1&1&0&0 \\ 0&0&1&1 \\ 1&0&1&0 \end{pmatrix}, \quad K = \begin{pmatrix} 2&2&0&0 \\ 1&1&0&0 \\ 0&0&1&1 \end{pmatrix}, \quad V = \begin{pmatrix} 1&0 \\ 0&1 \\ 1&1 \end{pmatrix}.$$

The state after each line, with no mask:

| query | L3 scores $s$ | L5 $\mu$ | L6 $p$ before division | $Z$ | L7 weights | L8 output |
|---|---|---|---|---|---|---|
| 1 | (2, 1, 0) | 2 | (1, 0.367879, 0.135335) | 1.503215 | (0.66524, 0.24473, 0.09003) | (0.75527, 0.33476) |
| 2 | (0, 0, 1) | 1 | (0.367879, 0.367879, 1) | 1.735759 | (0.21194, 0.21194, 0.57612) | (0.78806, 0.78806) |
| 3 | (1, 0.5, 0.5) | 1 | (1, 0.606531, 0.606531) | 2.213061 | (0.45186, 0.27407, 0.27407) | (0.72593, 0.54814) |

Query 1 matches key 1 best, so its output is close to $V_1 = (1, 0)$. With the causal mask, line L4 sets $s_2 = s_3 = -\infty$ for query 1 and $s_3 = -\infty$ for query 2. Query 1 then has weights (1, 0, 0) and output (1, 0). Query 2 has weights (0.5, 0.5, 0) and output (0.5, 0.5). Query 3 sees all keys, so its row does not change.

## Correctness

Line L6 subtracts the same $\mu$ from every score of the row, and $e^{s_j - \mu} / \sum_{j'} e^{s_{j'} - \mu} = e^{s_j} / \sum_{j'} e^{s_{j'}}$, so lines L5 to L7 give the softmax of the masked row exactly. A masked key gets $e^{-\infty} = 0$, so it has no effect on the output. The weights are non-negative and sum to 1, so each output row is a convex combination of the rows of $V$ that the query sees. The [full proof](proofs/correctness.md) also proves the variance lemma behind the factor $1/\sqrt{d_k}$, and the two symmetry facts below.

## Complexity

Line L3 runs $n m$ times at $\Theta(d_k)$ each, and line L8 runs $n$ times at $\Theta(m d_v)$ each. Lines L4 to L7 are $\Theta(m)$ per query. The total is $\Theta(n m (d_k + d_v))$ arithmetic operations in the [real RAM](/real-ram/), with the same bound in floating point. For self-attention with $m = n$ and $d_k = d_v = d$ this is $\Theta(n^2 d)$. The algorithm keeps one row of $m$ scores at a time, so the extra memory is $\Theta(m)$ beside the $n \times d_v$ output; the front matter counts only this row, not the score matrix. A matrix library usually forms the full $n \times m$ score matrix, which is $\Theta(n m)$ memory; for long sequences this matrix, not the arithmetic, is often the limit. [FlashAttention](/flashattention/) computes the same output without storing it.

## Properties

- **Permutation equivariance (theorem).** Permuting the queries permutes the output rows in the same way. Permuting the key-value pairs together does not change the output. So without a mask, attention does not see word order; a [positional encoding](/sinusoidal-positional-encoding/) adds it.
- **Convex output (theorem).** Each output row lies in the convex hull of the visible value rows.
- **Shift invariance (theorem).** Adding a constant to all scores of a row does not change the weights. Adding a vector $u$ to every key adds $q \cdot u / \sqrt{d_k}$ to the whole row, so it has no effect.
- **No parameters.** The learned weights live in the maps that produce $Q$, $K$ and $V$.
- **Differentiable.** The output is a smooth function of $Q$, $K$ and $V$, so the network is trained by [backpropagation](/backpropagation/).

## Variants and improvements

- **[Additive attention](/additive-attention/)** (Bahdanau, Cho and Bengio) scores with a small network, $v^\top \tanh(W q + U k)$. Vaswani and colleagues report that it does better than unscaled dot products for large $d_k$, which is what the scaling fixes.
- **[Multiplicative attention](/multiplicative-attention/)** (Luong and colleagues) uses $q^\top k$ or $q^\top W k$ without the scaling.
- **[Multi-head attention](/multi-head-attention/)** runs $h$ attentions on learned projections of size $d/h$ and concatenates them.
- **Masks and biases.** The causal mask, a padding mask, and learned or fixed biases such as [ALiBi](/alibi-attention-bias/) all enter as the matrix $B$.
- **[FlashAttention](/flashattention/)** gives the same output with an online softmax over blocks of keys and fewer memory transfers.
- **[Key-value cache](/key-value-cache/).** During generation one new query attends to all stored keys and values, $n = 1$, at $\Theta(m (d_k + d_v))$ per step.

## When to use it

Use it when every position may need information from any other position at distance 1 in the network, and $n$ is small enough that $n^2$ scores fit the time budget. A recurrent layer costs $\Theta(n d^2)$ but needs $n$ sequential steps; attention needs one parallel step. For very long inputs, consider a sparse or local mask, a [selective state space model](/selective-state-space-model/) with cost linear in $n$, or at least the memory-saving schedule of [FlashAttention](/flashattention/).

## Pitfalls

- **Missing scale.** Writing $s_j \leftarrow Q_i \cdot K_j$ at line L3 makes the softmax nearly one-hot for large $d_k$, and its gradients nearly zero. Divide by $\sqrt{d_k}$, not by $d_k$ and not by the model size $d$.
- **Unstable softmax.** Taking $\exp(s_j)$ at line L6 without subtracting $\mu$ overflows for scores above about 709 in double precision, and much earlier in half precision. Subtract the row maximum first.
- **Mask by a large finite number.** Using $-10^9$ instead of $-\infty$ at line L4 is fine in floating point only while real scores are much smaller; in half precision it overflows. With $-\infty$, a row where every key is masked gives $\mu = -\infty$ and $\exp(-\infty - (-\infty))$ is undefined, so check that each query sees a key, as line L5 assumes.
- **Mask after the softmax.** Setting masked weights to 0 after line L7 leaves rows that do not sum to 1. Apply the mask to the scores, before line L5.
- **Wrong axis.** The softmax at lines L6 and L7 is over the keys $j$ for a fixed query $i$, that is over each row of $Q K^\top$, not over each column.

## Implementations

The code takes the matrices $Q$, $K$ and $V$ as given and does not train a network.

## History

Bahdanau, Cho and Bengio (2015) introduced attention for neural machine translation: the decoder scored every encoder state with a small network and read a weighted sum. Luong, Pham and Manning (2015) compared simpler scores, among them the plain dot product. Vaswani and colleagues (2017) divided the dot product by $\sqrt{d_k}$, named the three inputs queries, keys and values, and built the [transformer](/transformer/) from attention alone, with no recurrence.

## References
