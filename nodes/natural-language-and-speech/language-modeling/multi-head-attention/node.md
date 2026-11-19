---
tag: YXWRTE
kind: algorithm
slug: multi-head-attention
name: Multi-head attention
aliases:
- multi-headed attention
area: natural-language-and-speech/language-modeling
level: core
summary: "Run h attention heads in parallel on learned low-dimension projections of queries, keys and values, then concatenate and project the outputs."
model: real-ram
complexity:
  vars: {n: the number of tokens, d: the model size, h: the number of heads}
  time: {worst: "Θ(n^2 d + n d^2)"}
  space: {extra: "Θ(n d)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2017
  people: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin]
  note: Introduced in the transformer paper, with h = 8 heads of size 64 in a model of size 512.
prereqs: [scaled-dot-product-attention]
see_also: [transformer, grouped-query-attention, key-value-cache, flashattention, rotary-position-embedding, alibi-attention-bias, bert, generative-pretrained-transformer]
sources:
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: Section 3.2.2 (the definition and the sizes h = 8, d_k = d_v = 64), Section 3.2.3 (the three uses in the model), Section 6.2 and Table 3 rows (A) (the number of heads)
  - paper: "Noam Shazeer, Fast transformer decoding: one write-head is all you need, arXiv:1911.02150, 2019"
    title: Shazeer 2019
    locator: the definition of multi-query attention and its memory traffic during incremental decoding
  - book: isbn:9780262048644
    title: Simon J. D. Prince, Understanding Deep Learning, MIT Press 2023
    locator: Chapter 12 (Transformers)
---

Multi-head attention runs $h$ copies of [scaled dot-product attention](/scaled-dot-product-attention/) side by side. Each copy, called a head, first maps the queries, keys and values to a smaller size $d/h$ with its own learned matrices, so the heads can look for different kinds of match. The $h$ outputs are joined end to end and mapped back to size $d$ by one more matrix. With $h d_k = d$ the cost is about the same as one attention of full size. It is the attention layer of every [transformer](/transformer/), in self-attention and in cross-attention between the encoder and the decoder.

## In plain words

One attention step lets each word take a weighted mix of the other words. But a word often needs several mixes at once: one that follows its grammar, one that finds the thing it refers to, one that looks at the word just before it.

So split the work into several small attention steps, the heads. Each head looks at the words through its own learned lens and makes its own mix. Because each head works with shorter vectors, all heads together cost about as much as one big step.

At the end, put the outputs of the heads next to each other and pass them through one more learned map, which combines what the heads found into a single vector per word.

## The problem

The input is a query-side matrix $X_q$ of shape $n \times d$ and a key-value side $X_{kv}$ of shape $m \times d$; in self-attention $X_{kv} = X_q$ and $m = n$. The weights of head $r$, for $r = 1, \ldots, h$, are $W^Q_r$ and $W^K_r$ of shape $d \times d_k$ and $W^V_r$ of shape $d \times d_v$, and the output map $W^O$ has shape $h d_v \times d$. Usually $d_k = d_v = d/h$. The output is the $n \times d$ matrix

$$\operatorname{MultiHead}(X_q, X_{kv}) = \operatorname{Concat}(H_1, \ldots, H_h)\, W^O, \qquad H_r = \operatorname{Attention}(X_q W^Q_r,\; X_{kv} W^K_r,\; X_{kv} W^V_r),$$

where Attention is the scaled dot-product attention with an optional mask, the same mask for every head. The weights are fixed inputs here; training sets them.

## The algorithm

```pseudo id=main
MULTI-HEAD(X_q, X_kv, W^Q, W^K, W^V, W^O, h, M)
L1  for r ← 1 to h do
L2      Q_r ← X_q W^Q_r                  ▷ n × d_k
L3      K_r ← X_kv W^K_r                 ▷ m × d_k
L4      V_r ← X_kv W^V_r                 ▷ m × d_v
L5      H_r ← ATTENTION(Q_r, K_r, V_r, M)  ▷ n × d_v
L6  H ← [H_1  H_2  ...  H_h]             ▷ n × h d_v, heads side by side
L7  return H W^O                         ▷ n × d
```

Lines L2 to L4 are usually done as three products with $d \times h d_k$ matrices, whose columns are the heads in order, and the result is reshaped into $h$ blocks. The heads at line L5 are independent and run in parallel. Line L7 can also be read as a sum: split $W^O$ into $h$ blocks of $d_v$ rows, $W^O_1, \ldots, W^O_h$, then $H W^O = \sum_r H_r W^O_r$. So each head writes its own contribution into the output, and the concatenation is only a way to do all $h$ products as one.

## Example

Take $d = 4$, $h = 2$ and $d_k = d_v = 2$, so the scale is $\sqrt{2}$. Let every weight matrix be the identity: head 1 then sees the first two coordinates of each token and head 2 the last two. Self-attention on three tokens:

$$X = \begin{pmatrix} 2&0&0&0 \\ 2&0&0&2 \\ 0&2&2&0 \end{pmatrix}.$$

Tokens 1 and 2 are the same for head 1 and differ for head 2. The state after line L5, rounded:

| head | scores of token 1 | weights of token 1 | weights of token 2 | weights of token 3 | $H_r$, rows 1 to 3 |
|---|---|---|---|---|---|
| 1 | (2.82843, 2.82843, 0) | (0.48565, 0.48565, 0.0287) | (0.48565, 0.48565, 0.0287) | (0.05286, 0.05286, 0.89429) | (1.94259, 0.05741), (1.94259, 0.05741), (0.21143, 1.78857) |
| 2 | (0, 0, 0) | (0.33333, 0.33333, 0.33333) | (0.05286, 0.89429, 0.05286) | (0.05286, 0.05286, 0.89429) | (0.66667, 0.66667), (0.10571, 1.78857), (1.78857, 0.10571) |

Head 1 cannot tell tokens 1 and 2 apart and gives them the same output. Head 2 sends token 2 mostly to itself. Lines L6 and L7, with $W^O = I$, give the rows (1.94259, 0.05741, 0.66667, 0.66667), (1.94259, 0.05741, 0.10571, 1.78857) and (0.21143, 1.78857, 1.78857, 0.10571). Tokens 1 and 2 now have different outputs, although head 1 alone gave them the same one.

## Correctness

The loop at line L1 computes each $H_r$ by the definition, using the correctness of [scaled dot-product attention](/scaled-dot-product-attention/) at line L5, and lines L6 and L7 form the product with $W^O$. The [full proof](proofs/correctness.md) shows the identity $\operatorname{Concat}(H_1, \ldots, H_h) W^O = \sum_r H_r W^O_r$, that one head with $d_k = d_v = d$ is plain attention on projected inputs, and that multi-head self-attention without a mask is permutation equivariant.

## Complexity

Count multiply-adds with $m = n$ and $h d_k = h d_v = d$. Lines L2 to L4 cost $3 n d \cdot d$ over all heads. Line L5 costs $n^2 (d_k + d_v)$ per head, $2 n^2 d$ in total. Line L7 costs $n d \cdot d$. The sum is $4 n d^2 + 2 n^2 d = \Theta(n^2 d + n d^2)$ in the [real RAM](/real-ram/): the projections dominate when $n < d$ and the scores when $n > d$. The projections and the heads take $\Theta(n d)$ memory; the front matter counts these and one row of scores at a time. A library that stores all score matrices needs $\Theta(h n^2)$ more, which is the reason for [FlashAttention](/flashattention/). The layer has $4 d^2$ weights, or $4 d^2 + 4 d$ with biases.

## Properties

- **Same cost as one head (theorem).** With $d_k = d/h$ the arithmetic is the same as one head of size $d$, up to the $h$ separate softmaxes.
- **Sum of heads (theorem).** The output is $\sum_r H_r W^O_r$, so heads add their results; this is the form used to study what each head does.
- **Permutation equivariance (theorem).** Without a mask and without positional information, permuting the tokens permutes the output rows.
- **Weights.** $4 d^2$ for the four maps. The number of heads does not change it.
- **Heads matter, but not too many (measurement).** In Table 3 of Vaswani and colleagues, one head was 0.9 BLEU worse than the best setting on English to German, and quality also dropped with too many heads.

## Variants and improvements

- **Multi-query attention** (Shazeer 2019) keeps $h$ query heads but one shared key head and one shared value head, which makes the [key-value cache](/key-value-cache/) $h$ times smaller.
- **[Grouped-query attention](/grouped-query-attention/)** shares each key-value head among $h/g$ query heads, between the two extremes.
- **Positions inside the heads.** [Rotary position embedding](/rotary-position-embedding/) rotates $Q_r$ and $K_r$ after lines L2 and L3; [ALiBi](/alibi-attention-bias/) adds a different distance penalty to the scores of each head.
- **Cross-attention.** With $X_{kv}$ the encoder output and $X_q$ the decoder state, the same algorithm is the encoder-decoder attention of the [transformer](/transformer/).
- **[FlashAttention](/flashattention/)** changes only how line L5 is computed.

## When to use it

Use it wherever a [transformer](/transformer/) uses attention: in self-attention with a padding mask in an encoder such as [BERT](/bert/), with a causal mask in a decoder such as [GPT](/generative-pretrained-transformer/), and in cross-attention. Prefer [grouped-query attention](/grouped-query-attention/) when autoregressive decoding is limited by the memory traffic of the key-value cache. Use a single head only in very small models or for teaching.

## Pitfalls

- **Wrong split.** At lines L2 to L4 each head must use its own block of $d_k$ consecutive columns, and line L6 must place the heads in the same order. Mixing up the reshape (heads as the slow index on one side and the fast index on the other) still runs, with wrong results.
- **Wrong scale.** Line L5 divides by $\sqrt{d_k} = \sqrt{d/h}$, not by $\sqrt{d}$.
- **Forgetting $W^O$.** Returning $H$ at line L7 without the product leaves each head's output in its own coordinates; the next layer then cannot mix them.
- **Different masks per head.** The causal or padding mask at line L5 must be applied to every head.
- **$d$ not divisible by $h$.** Then $d_k = d/h$ is not an integer; choose $h$ to divide $d$ or set $d_k$ on its own.

## Implementations

The code takes the inputs and the weight matrices as given and does not train a network.

## History

Vaswani and colleagues (2017) introduced multi-head attention in the [transformer](/transformer/), with $h = 8$ heads of size $d_k = d_v = 64$ for $d = 512$. They argued that one head averages over different kinds of relation, while several heads can attend to different subspaces at different positions. Shazeer (2019) shared the keys and values across heads to speed up decoding, and Ainslie and colleagues (2023) generalized this to [grouped-query attention](/grouped-query-attention/).

## References
