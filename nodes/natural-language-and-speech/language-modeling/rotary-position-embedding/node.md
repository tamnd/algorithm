---
tag: XBK70H
kind: technique
slug: rotary-position-embedding
name: Rotary position embedding
aliases:
- rotary positional encoding
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Rotate pairs of query and key coordinates by angles proportional to position, so that their dot product depends only on the relative offset."
prereqs: [sinusoidal-positional-encoding, multi-head-attention]
see_also: [alibi-attention-bias, scaled-dot-product-attention, key-value-cache, grouped-query-attention, transformer, givens-rotations, generative-pretrained-transformer, rodrigues-rotation-formula]
sources:
  - paper: doi:10.1016/j.neucom.2023.127063
    title: "Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo and Yunfeng Liu, RoFormer: enhanced transformer with rotary position embedding, Neurocomputing 568 (2024) 127063, arXiv:2104.09864"
    locator: "Section 3.2.1 (the 2D case, equation 12), Section 3.2.2 (the general form, equation 15), Section 3.3 (long-term decay, linear attention), Section 3.4.2 (the efficient form), Section 3.4.3 (the decay argument), Section 4.1 (WMT 2014 English to German)"
  - paper: "Ofir Press, Noah A. Smith and Mike Lewis, Train short, test long: attention with linear biases enables input length extrapolation, ICLR 2022, arXiv:2108.12409"
    title: Press, Smith and Lewis 2022
    locator: the extrapolation experiments, where rotary embeddings extrapolate somewhat beyond the training length but less than ALiBi
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: Section 3.5 (the frequencies that RoPE reuses)
---

Rotary position embedding puts word order into [attention](/scaled-dot-product-attention/) by rotating vectors instead of adding to them. The query and the key at position $m$ are cut into pairs of coordinates, and pair $i$ is rotated by the angle $m\theta_i$, with the frequencies $\theta_i = 10000^{-2i/d}$ of the [sinusoidal positional encoding](/sinusoidal-positional-encoding/). Because rotations compose, the dot product of a query rotated by $m$ and a key rotated by $n$ equals the dot product of the original query with the key rotated by $n - m$. So the attention score depends on the two contents and on the offset $n - m$ only, not on where the pair sits in the text. Su and colleagues introduced it in RoFormer, and RoPE is now the position method of many large decoder-only models, including GPT-NeoX, PaLM and LLaMA.

## In plain words

Think of each query and each key as a set of clock hands. Before comparing them, turn the hands of a word at position 10 by ten steps and the hands of a word at position 7 by seven steps. Each hand has its own step size: some turn fast, some slowly.

When two hands are compared, only the angle between them matters. Turning both by the same extra amount changes nothing. So the comparison sees how far apart the two words are, not where they are in the text. A word three places back looks the same to the model at the start of a page as at its end.

Turning a hand does not make it longer or shorter, so the content of the vectors is kept. Nothing is added to the input words.

## When it applies

- A [transformer](/transformer/) where attention scores should depend on the relative position of query and key, for example a decoder-only language model used on texts of very different lengths.
- Generation with a [key-value cache](/key-value-cache/): each key is rotated once by its own position when it is stored, and never needs to change, because the rotation of a new query alone fixes the offset.
- Dot-product attention of any kind, including [grouped-query attention](/grouped-query-attention/), since only $Q$ and $K$ are changed. The values are not rotated.

## The template

Let $d$ be the head size, even, and $\theta_i = 10000^{-2i/d}$ for $i = 0, \ldots, d/2 - 1$. For a vector $x$ at position $m$, rotate pair $(x_{2i}, x_{2i+1})$ by $m\theta_i$:

$$\begin{pmatrix} y_{2i} \\ y_{2i+1} \end{pmatrix} = \begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix} \begin{pmatrix} x_{2i} \\ x_{2i+1} \end{pmatrix}.$$

So $y = R_m x$, where $R_m$ is block diagonal with these 2 by 2 rotations.

```pseudo id=main
ROPE(x, pos, d)                      ▷ x of size d, d even
L1  for i ← 0 to d/2 - 1 do
L2      θ_i ← 10000^(-2i/d)
L3      c ← cos(pos · θ_i);  s ← sin(pos · θ_i)
L4      y[2i] ← c · x[2i] - s · x[2i+1]
L5      y[2i+1] ← s · x[2i] + c · x[2i+1]
L6  return y
```

In each head, after the projections $Q_r = X W^Q_r$ and $K_r = X W^K_r$ of [multi-head attention](/multi-head-attention/), replace row $m$ of $Q_r$ by ROPE$(Q_{r,m}, m, d_k)$ and row $n$ of $K_r$ by ROPE$(K_{r,n}, n, d_k)$, then compute the scores as usual. The cost is $\Theta(d)$ per vector, small next to the score computation.

**The relative property (theorem).** Each block of $R_m$ is a rotation, so $R_m^\top = R_{-m}$ and $R_a R_b = R_{a + b}$. Hence

$$(R_m q)^\top (R_n k) = q^\top R_m^\top R_n k = q^\top R_{n - m} k,$$

which depends on $m$ and $n$ only through $n - m$. Also $\lVert R_m x \rVert = \lVert x \rVert$. With a pair seen as a complex number $z = x_{2i} + \mathrm{i}\, x_{2i+1}$, the rotation is the product $z\, e^{\mathrm{i} m \theta_i}$, and the score of the pair is $\operatorname{Re}\big(q_i \overline{k_i}\, e^{\mathrm{i}(m - n)\theta_i}\big)$. The [full proof](proofs/correctness.md) gives the details.

**Long-term decay (heuristic).** Su and colleagues show, through an upper bound and a plot of it (Section 3.4.3), that the size of the relative part of the score tends to fall as $|n - m|$ grows with these frequencies. It is a bound on a sum, not a guarantee that a trained model attends less to far tokens.

## Classic examples

**Two-dimensional case.** With $d = 2$ the only frequency is $\theta_0 = 1$. Take $q = k = (1, 0)$, the query at position 3 and the key at position 1. Then $R_3 q = (\cos 3, \sin 3)$, $R_1 k = (\cos 1, \sin 1)$, and the score is $\cos 3 \cos 1 + \sin 3 \sin 1 = \cos 2 = -0.416147$. Moving both to positions 103 and 101 gives the same score.

**Decoder-only language models.** GPT-NeoX, PaLM and LLaMA apply RoPE in every head of [causal language models](/causal-language-modeling/) in the style of [GPT](/generative-pretrained-transformer/), with no position vector added to the input.

**Key-value cache.** In a [key-value cache](/key-value-cache/) the stored keys are already rotated by their own positions. When the token at position $t$ is generated, only its query and its new key are rotated by $t$; the scores with all old keys then have the right offsets.

**Translation.** In Section 4.1 of the RoFormer paper, replacing the sinusoidal encoding of a base [transformer](/transformer/) by RoPE on WMT 2014 English to German gave 27.5 BLEU against 27.3 (a measurement, a small gain).

## Variations

- **Layout in halves.** Many code bases pair coordinate $i$ with coordinate $i + d/2$ instead of $i + 1$ and compute $x \cos + \operatorname{rotate\_half}(x) \sin$. This is the same method after a fixed permutation of the coordinates, but weights trained with one layout do not work with the other.
- **Partial rotation.** Rotate only a fraction of the coordinates of each head and leave the rest without position information.
- **Longer contexts.** To run a model beyond its training length, the positions can be scaled down (position interpolation) or the base 10000 raised, usually followed by a short fine-tuning.
- **RoPE with linear attention.** Since RoPE keeps norms and acts on queries and keys separately, it can be applied to the feature maps of linear attention (Section 3.3 of the paper).
- **Other relative methods.** [ALiBi](/alibi-attention-bias/) adds a distance penalty to the scores instead of rotating, and extrapolates better in the experiments of Press and colleagues (a measurement).

## Pitfalls

- **Mixing layouts.** Loading weights trained with the layout in halves into code that uses interleaved pairs (or the reverse) runs without error and gives poor results. Check which pairing the model uses.
- **Rotating the values.** Only $Q$ and $K$ are rotated. Rotating $V$ breaks the output, since the output is a sum of values and not a dot product.
- **Wrong position with a cache.** With a [key-value cache](/key-value-cache/), the new token must be rotated by its absolute position $t$, not by 0 or by its index in the current chunk.
- **Precision of the angles.** For large positions, computing $m\theta_i$ and its sine and cosine in half precision loses accuracy. Compute the angles in float32 or better.
- **Odd head size.** The method needs pairs; an odd $d_k$ leaves one coordinate unrotated.
- **Expecting free extrapolation.** The relative property does not make a model work well beyond the trained length; the high-index pairs have rotated by angles never seen in training.

## Exercises

1. Prove $R_a R_b = R_{a+b}$ and $R_a^\top = R_{-a}$ for the block rotations, and derive $(R_m q)^\top (R_n k) = q^\top R_{n-m} k$.
2. With pairs as complex numbers, show that the score of pair $i$ is $\operatorname{Re}(q_i \overline{k_i} e^{\mathrm{i}(m-n)\theta_i})$.
3. Show that the layout in halves equals $P^\top R_m P$ for a permutation matrix $P$, and that it has the same relative property.
4. Show that $|q^\top R_{n-m} k| \le \lVert q \rVert \lVert k \rVert$ for all offsets, so RoPE cannot make a score larger than the unrotated maximum.
5. Explain why adding the sinusoidal vectors to the input does not give a score that depends only on $n - m$, while RoPE does.

## References
