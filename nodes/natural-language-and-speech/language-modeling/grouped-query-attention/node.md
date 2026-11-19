---
tag: VQPZ6C
kind: technique
slug: grouped-query-attention
name: Grouped-query attention
aliases:
- GQA
- multi-query attention
area: natural-language-and-speech/language-modeling
level: research
summary: "Let groups of query heads share one key head and one value head, which shrinks the key-value cache with little loss in quality."
prereqs: [multi-head-attention, key-value-cache]
see_also: [scaled-dot-product-attention, transformer, flashattention, rotary-position-embedding, alibi-attention-bias, causal-language-modeling, speculative-decoding, generative-pretrained-transformer]
sources:
  - paper: doi:10.18653/v1/2023.emnlp-main.298
    title: "Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón and Sumit Sanghai, GQA: training generalized multi-query transformer models from multi-head checkpoints, EMNLP 2023, pages 4895-4901, arXiv:2305.13245"
    locator: "Section 2.1 (uptraining, mean pooling), Section 2.2 (GQA-G, GQA-1 and GQA-H, not applied to the encoder, the cache against model size), Section 3.1 (T5.1.1 Large and XXL, alpha = 0.05), Table 1 in Section 3.2, Section 3.3 (Figure 4 checkpoint conversion, Figure 6 number of groups)"
  - paper: "Noam Shazeer, Fast transformer decoding: one write-head is all you need, arXiv:1911.02150, 2019"
    title: Shazeer 2019
    locator: the multi-query attention layer, with one key head and one value head for all query heads
---

Grouped-query attention, GQA, is [multi-head attention](/multi-head-attention/) in which the $h$ query heads are split into $g$ groups, and all query heads of a group use the same key head and the same value head. So the layer computes $h$ query projections but only $g$ key and $g$ value projections. With $g = h$ it is multi-head attention, and with $g = 1$ it is the multi-query attention of Shazeer, with one key head and one value head for all queries. The point is generation: a decoder keeps the keys and values of all past tokens in a [key-value cache](/key-value-cache/), and reading that cache at each step limits the speed. GQA makes the cache $h/g$ times smaller. Ainslie and colleagues introduced it in 2023 and showed that a multi-head model can be converted to GQA with a short extra training.

## In plain words

In multi-head attention, each head asks its own question and also keeps its own copy of what every past word offers. When a model writes text one word at a time, it must keep all those copies in memory and read them again for each new word. That reading is slow.

GQA lets several heads share one copy. The heads still ask different questions, but a group of them looks things up in the same notes. With 8 heads in groups of 4, the model keeps 2 copies instead of 8, so it reads a quarter as much at each step.

One copy for all heads is fastest but can lose quality. A few groups keep nearly all the quality of separate copies and most of the speed.

## When it applies

- Decoder-only and encoder-decoder models that generate text with a [key-value cache](/key-value-cache/), where memory traffic per step, and not arithmetic, limits the speed.
- Long contexts or large batches, where the cache is a large part of the memory.
- Converting an existing multi-head checkpoint to faster decoding, by mean pooling and a short uptraining.
- It is not needed where all tokens are processed at once with no cache; Ainslie and colleagues do not apply it to the encoder self-attention layers (Section 2.2).

## The template

Let $h$ query heads, $g$ groups with $g$ dividing $h$, head sizes $d_k$ and $d_v$, and weights $W^Q \in \mathbb{R}^{d \times h d_k}$, $W^K \in \mathbb{R}^{d \times g d_k}$, $W^V \in \mathbb{R}^{d \times g d_v}$ and $W^O \in \mathbb{R}^{h d_v \times d}$. Query head $r$ (from 0) uses group $s(r) = \lfloor r / (h/g) \rfloor$:

$$\mathrm{head}_r = \mathrm{Attention}(X W^Q_r,\; X W^K_{s(r)},\; X W^V_{s(r)}), \qquad \mathrm{GQA}(X) = \mathrm{Concat}(\mathrm{head}_0, \ldots, \mathrm{head}_{h-1})\, W^O.$$

```pseudo id=main
GQA(X_q, X_kv, W^Q, W^K, W^V, W^O, h, g)      ▷ g divides h
L1  for s ← 0 to g - 1 do
L2      K_s ← X_kv W^K_s;  V_s ← X_kv W^V_s
L3  for r ← 0 to h - 1 do
L4      s ← floor(r / (h/g))
L5      Q_r ← X_q W^Q_r
L6      head_r ← ATTENTION(Q_r, K_s, V_s)
L7  return Concat(head_0, ..., head_{h-1}) W^O
```

ATTENTION is [scaled dot-product attention](/scaled-dot-product-attention/), with a causal mask in a decoder.

**Equal to multi-head attention with copied weights (theorem).** Build $\tilde W^K$ from $W^K$ by giving each query head $r$ a copy of the column block $W^K_{s(r)}$, and $\tilde W^V$ in the same way. Then GQA with $W^K, W^V$ equals multi-head attention with $\tilde W^K, \tilde W^V$, since each head sees the same three matrices. So GQA is multi-head attention with a constraint on the weights: the heads of a group must have equal key and value maps. The [full proof](proofs/correctness.md) gives the details.

**Cache size.** Per layer and token, the cache holds $g (d_k + d_v)$ numbers instead of $h (d_k + d_v)$, a factor $g/h$. The parameters of the key and value maps shrink by the same factor; the query and output maps are unchanged.

**Uptraining.** To convert a multi-head checkpoint, replace the key and value maps of each group by the mean of the maps of its heads (mean pooling), then continue pre-training for a fraction $\alpha$ of the original steps; Ainslie and colleagues used $\alpha = 0.05$. If the heads of a group already have equal maps, mean pooling changes nothing.

## Classic examples

**A worked layer.** Let $d = 1$, $h = 4$ heads, $g = 2$ groups and head sizes 1, so heads 0 and 1 use group 0 and heads 2 and 3 use group 1. Take $W^Q = (1, 0, 1, 0)$, $W^K = (1, 0.5)$, $W^V = (1, -1)$, $W^O = (1, 1, 1, 1)^\top$ and the tokens $x_0 = 1$, $x_1 = 2$, with a causal mask. Token 0 sees only itself, and the heads give $1, 1, -1, -1$, so the output is 0. For token 1, head 0 has the scores 2 and 4 on the values 1 and 2 and gives $1 + \sigma(2)$, head 2 has the scores 1 and 2 on $-1$ and $-2$ and gives $-(1 + \sigma(1))$, and heads 1 and 3 have query 0 and give the means $1.5$ and $-1.5$. The output is $\sigma(2) - \sigma(1) = 0.149738$, where $\sigma$ is the logistic function.

**Cache sizes.** For a model with 32 layers, 32 query heads of size 128, and 4096 cached tokens in 16-bit numbers:

| layout | key-value heads $g$ | cache |
|---|---|---|
| multi-head | 32 | 2 GiB |
| GQA | 8 | 512 MiB |
| multi-query | 1 | 64 MiB |

**T5 XXL.** In Table 1 of Ainslie and colleagues, uptrained T5 XXL models on summarization, translation and question answering scored on average 47.2 with multi-head attention at 1.51 s per sample, 47.1 with GQA with 8 groups at 0.28 s, and 46.6 with one key-value head at 0.24 s (a measurement). Multi-head T5 Large scored 46.0 at 0.37 s.

**Decoder-only models.** Many recent decoder-only [GPT](/generative-pretrained-transformer/)-style models use GQA in every layer, often with [rotary position embedding](/rotary-position-embedding/) applied to the queries and the shared keys.

## Variations

- **One group.** $g = 1$ gives the smallest cache, at some loss in quality: 46.6 against 47.2 in Table 1 (a measurement).
- **Number of groups.** Figure 6 of the GQA paper shows that the time per sample grows slowly from $g = 1$ and faster near $g = h$; they chose 8 groups.
- **Conversion choices.** Mean pooling worked better than keeping the first head of each group, which worked better than a random start (Figure 4, a measurement).
- **Training from scratch.** A model can be trained with GQA from the start, with no conversion.
- **Larger models.** Section 2.2 notes that the cache grows with the model dimension while the parameters and the arithmetic grow with its square, so large models suffer relatively less from the memory traffic of attention. The authors argue that GQA is a good trade-off for them.

## Pitfalls

- **Wrong head-to-group map.** The heads of a group must be the ones whose weights were pooled. Code that groups heads $r$ with $r \bmod g$ while the checkpoint uses $\lfloor r / (h/g) \rfloor$, or the reverse, runs without error and gives wrong outputs.
- **Copying the cache.** Repeating the key-value heads $h/g$ times before attention gives the right output but loses the memory saving if the copies are stored. Index the shared heads instead.
- **$g$ not dividing $h$.** The groups must have equal sizes in the usual layout.
- **Expecting a speedup without a cache.** In training or in the first pass over a prompt, the cost is dominated by the score computation, which is the same for all $g$. The gain is in the decoding steps.
- **Counting parameters.** Only the key and value maps shrink. The query and output maps keep $d \cdot h d_k$ and $h d_v \cdot d$ weights.

## Exercises

1. Prove that GQA equals multi-head attention with copied key and value maps, and conclude that the set of functions of GQA-$g$ is contained in that of GQA-$g'$ when $g$ divides $g'$.
2. Show that if the heads of each group have equal key and value maps, mean pooling returns those maps, so the converted model computes the same function.
3. For $d = 4096$, $h = 32$, $d_k = d_v = 128$, compute the parameters of one attention layer for $g = 32, 8, 1$.
4. Compute the cache in bytes for 80 layers, 64 query heads of size 128, $g = 8$, 8192 tokens and 16-bit numbers, and compare with $g = 64$.
5. Explain why the time per decoding step depends on $g$ mostly through the bytes of cache read, and not through the arithmetic.

## References
