---
tag: FKDFWV
kind: technique
slug: alibi-attention-bias
name: Attention with linear biases
aliases:
- ALiBi
area: natural-language-and-speech/language-modeling
level: research
summary: "Add to each attention score a penalty linear in the distance between query and key, with a fixed slope per head, instead of position vectors."
prereqs: [multi-head-attention]
see_also: [rotary-position-embedding, sinusoidal-positional-encoding, scaled-dot-product-attention, causal-language-modeling, transformer, key-value-cache, flashattention, generative-pretrained-transformer]
sources:
  - paper: "Ofir Press, Noah A. Smith and Mike Lewis, Train short, test long: attention with linear biases enables input length extrapolation, ICLR 2022, arXiv:2108.12409"
    title: Press, Smith and Lewis 2022
    locator: "Abstract and Section 1 (the 1.3B model trained on 1024 tokens, 11% faster and 11% less memory), Figure 1 (extrapolation of sinusoidal, rotary and T5 bias), Section 3 (the biased scores, the slopes, trainable slopes, footnote 10 on the scaling), Section 3 Implementation (the bias in the mask), Section 4 (WikiText-103, books, the 1.3B model)"
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: Section 3.2.1 (scaled dot-product attention), Section 3.5 (the sinusoidal encoding that ALiBi replaces)
---

Attention with linear biases, ALiBi, gives a [transformer](/transformer/) language model word order without any position vectors. In each head, it subtracts from the score of query $i$ and key $j$ a penalty $m \cdot (i - j)$, proportional to how far back the key is. The slope $m$ is fixed before training and is different in each head, so some heads look mostly at the last few tokens and others look far back. Press, Smith and Lewis introduced it in 2021 to make models work on inputs longer than those seen in training: a model trained on short inputs can then be run on longer ones. Their 1.3B-parameter model trained on 1024 tokens matched, on 2048-token inputs, the perplexity of a sinusoidal model trained on 2048 tokens, while training 11% faster and with 11% less memory (a measurement).

## In plain words

In a causal language model, each word looks back at the words before it and decides how much to take from each. ALiBi adds one simple rule: the further back a word is, the more its match score is reduced, by a fixed amount per step.

Each head has its own rate. A head with a high rate sees almost only the last few words. A head with a low rate sees far back. Nothing about position is added to the words themselves.

Because the rule depends only on distance, a word 5 steps back is treated the same at the start of the text and deep into it. And a longer text only adds words that are far back and get little weight, so the model is not surprised by a length it never saw.

## When it applies

- A decoder-only [causal language model](/causal-language-modeling/) that should run on inputs longer than its training inputs, or be trained on short inputs to save time and memory.
- [Multi-head attention](/multi-head-attention/) with a causal mask, where the mask matrix is already added to the scores: the bias goes into the same matrix.
- Tasks with a recency bias, where nearby tokens matter most, such as language modeling of running text.

## The template

Let a head have slope $m > 0$, keys $k_1, \ldots, k_i$ visible to query $q_i$, and head size $d_k$. The biased score is

$$s_{ij} = \frac{q_i \cdot k_j}{\sqrt{d_k}} - m\,(i - j), \qquad j \le i,$$

that is, the row $q_i K^\top / \sqrt{d_k}$ plus $m \cdot [-(i-1), \ldots, -2, -1, 0]$. The bias is not scaled by $1/\sqrt{d_k}$. Softmax and the weighted sum of values are as in [scaled dot-product attention](/scaled-dot-product-attention/).

```pseudo id=main
ALIBI-HEAD(Q, K, V, m)               ▷ causal, slope m of this head
L1  for i ← 1 to n do
L2      for j ← 1 to i do
L3          s_j ← q_i · k_j / sqrt(d_k) - m · (i - j)
L4      p ← softmax(s_1, ..., s_i)
L5      o_i ← Σ_{j ≤ i} p_j v_j
L6  return O = (o_1, ..., o_n)
```

**The slopes.** For $h$ heads, $h$ a power of 2, the slopes are the geometric sequence that starts at $2^{-8/h}$ with ratio $2^{-8/h}$: $m_r = 2^{-8r/h}$ for $r = 1, \ldots, h$. With 8 heads this is $\tfrac12, \tfrac14, \ldots, \tfrac1{256}$. With 16 heads it is $2^{-0.5}, 2^{-1}, \ldots, 2^{-8}$, which puts the geometric mean of each pair of the 8-head slopes between them. For other $h$, the code of the authors takes the $2^a$ slopes of the largest power of 2 below $h$ and fills the rest with every other slope of $2^{a+1}$ heads.

**Row shifts do not matter (theorem).** Softmax does not change when the same number is added to every score of a row. Adding $m\,i$ to row $i$ turns the bias $-m(i - j)$ into $+m\,j$, which depends on the key alone. So the biased head equals a head with the bias $m\,j$ plus the causal mask. In practice the bias is stored in the mask matrix, one $L \times L$ matrix per head, and the cost of attention does not change.

**Distance only (theorem).** The bias of the pair $(i, j)$ is the same as that of $(i + t, j + t)$ for every $t$. If every scaled product satisfies $|q_i \cdot k_j| / \sqrt{d_k} \le B$, the weight on a key at distance $r = i - j$ is at most $e^{2B - m r}$, since its score exceeds the score of the key at distance 0 by at most $2B - m r$. The [full proof](proofs/correctness.md) gives both results and the correctness of the procedure.

**Cost.** As plain causal attention: $\Theta(n^2 (d_k + d_v))$ operations per head, with a bias of $\Theta(1)$ per score. No parameters are added.

## Classic examples

**A worked head.** Take one head with slope $m = \tfrac12$ and all queries and keys equal to zero, so only the bias acts. Values are $v_1, \ldots, v_4 = 0, 1, 2, 3$. For query 4, the scores are $-1.5, -1, -0.5, 0$, and the weights are

| key $j$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| distance $4 - j$ | 3 | 2 | 1 | 0 |
| weight | 0.101536 | 0.167405 | 0.276004 | 0.455054 |

so $o_4 = 2.084576$. Each step back multiplies the weight by $e^{-1/2} = 0.606531$. The outputs for queries 1 to 4 are $0, 0.622459, 1.320157, 2.084576$; with $m = 0$ they would be the plain means $0, 0.5, 1, 1.5$.

**Length extrapolation.** In Figure 1 of Press and colleagues, models trained on WikiText-103 with inputs of 512 or 1024 tokens were tested on longer inputs. The perplexity of the sinusoidal, rotary and T5 bias methods got worse as the inputs grew past the training length, and that of ALiBi did not (a measurement).

**Training short and testing long.** The 1.3B-parameter model of Section 4, trained on 1024 tokens, reached the perplexity of a sinusoidal model trained on 2048 tokens when both were tested on 2048 tokens (a measurement).

**Generation with a cache.** With a [key-value cache](/key-value-cache/), the new query at position $t$ gets the biases $-m(t - j)$ for the cached keys. The bias depends on positions alone, so cached keys need no change, as with [rotary position embedding](/rotary-position-embedding/).

## Variations

- **Trainable slopes.** Press and colleagues tried learned slopes; extrapolation was not strong and training was 3% slower (Section 3, a measurement).
- **Other slope sets.** They report that slopes in $(0, 1)$, denser near 0, work best, and that the method is not very sensitive to the exact set.
- **Bidirectional use.** For an encoder without a causal mask, one choice is the symmetric bias $-m\,|i - j|$. This loses the difference between left and right unless the slopes differ by direction.
- **Learned relative biases.** The T5 bias learns one bias per distance bucket, shared by the layers. ALiBi replaces this table by a fixed line.
- **With fast kernels.** The bias $m\,j$ is computed from the indices, so it fits into a tiled kernel such as [FlashAttention](/flashattention/) without storing an $L \times L$ matrix.

## Pitfalls

- **Scaling the bias.** The bias is added after the scaling by $1/\sqrt{d_k}$ and is not itself scaled (footnote 10 of the paper). Scaling it changes the slopes.
- **Adding position vectors as well.** ALiBi models add no position vectors at any point. Adding a sinusoidal encoding as well changes the model.
- **Wrong sign.** The penalty must decrease the scores of far keys. With the sign flipped, the bias favors the first tokens of the text.
- **Wrong positions with a cache.** The new query must use its absolute position $t$ in the text, not its index in the current chunk.
- **Memory of the bias matrix.** Storing a separate $L \times L$ bias per head costs memory, up to 100 MB in the experiments of the paper. Computing the bias from the indices avoids it.
- **Expecting long-range use.** Extrapolation here means the perplexity does not blow up. Far tokens get small weights in heads with large slopes, so ALiBi does not by itself make a model use very distant context.

## Exercises

1. Show that softmax is unchanged when a constant is added to all its inputs, and conclude that the biases $-m(i - j)$ and $+m\,j$ give the same head.
2. With all scores equal to zero, show that the weights of query $i$ form a truncated geometric distribution with ratio $e^{-m}$, and find their limit as $i \to \infty$.
3. Prove the bound: if $|q_i \cdot k_j| / \sqrt{d_k} \le B$ for all pairs, the weight on a key at distance $r$ is at most $e^{2B - m r}$.
4. Compute the slopes for $h = 4$, $h = 8$ and $h = 12$ with the rule of the authors, and check that the 16-head slopes interleave the 8-head slopes with their geometric means.
5. Explain why ALiBi, like rotary position embedding, puts no position information into the values, and what the output of a layer then knows about position.

## References
