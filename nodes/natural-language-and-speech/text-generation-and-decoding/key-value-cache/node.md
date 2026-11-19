---
tag: JVESYS
kind: data-structure
slug: key-value-cache
name: Key-value cache
aliases:
- KV cache
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: Store the attention keys and values of past tokens during decoding, so each new token costs attention time linear in the length, not quadratic.
model: real-ram
complexity:
  vars: {n: the number of positions so far, L: the number of layers, d: the model width, h: the number of query heads, g: the number of key-value heads}
  time: {step: "O(L (n d + d^2))", generate: "O(L (n^2 d + n d^2))"}
  space: {extra: "O(L n d g / h)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [transformer, scaled-dot-product-attention, multi-head-attention, causal-language-modeling]
see_also: [grouped-query-attention, flashattention, speculative-decoding, greedy-decoding, dynamic-array, free-list, memory-pool, roofline-model]
sources:
  - url: https://arxiv.org/abs/1706.03762
    title: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, NIPS 2017
    locator: the decoder with masked self-attention, which makes the keys and values of past positions independent of later tokens
  - url: https://arxiv.org/abs/1911.02150
    title: Noam Shazeer, Fast transformer decoding, one write-head is all you need, arXiv 1911.02150, 2019
    locator: incremental decoding with stored keys and values, its memory traffic, and multi-query attention
  - paper: doi:10.18653/v1/2023.emnlp-main.298
    title: Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón and Sumit Sanghai, GQA, training generalized multi-query transformer models from multi-head checkpoints, EMNLP 2023, pages 4895 to 4901
    locator: grouped-query attention, with g key-value heads shared by groups of query heads
  - url: https://arxiv.org/abs/2309.06180
    title: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang and Ion Stoica, Efficient memory management for large language model serving with PagedAttention, SOSP 2023
    locator: the block table that maps the logical blocks of a sequence to physical blocks of fixed size
---

A key-value cache stores, for every layer of a decoder-only [transformer](/transformer/) and every position generated so far, the key and value vectors that [attention](/scaled-dot-product-attention/) computed for that position. With a causal mask, these vectors never change once computed, because a position never attends to later ones. So when the decoder appends a token, it computes the query, key and value of the new position only, appends the key and value to the cache, and attends over the cached keys. A step then costs attention time $O(L n d)$ for $n$ cached positions, $L$ layers and width $d$, in place of $O(L n^2 d)$ to recompute all positions, and generating $n$ tokens costs $O(L n^2 d)$ attention in total in place of $O(L n^3 d)$. The price is memory: $2 L n d$ numbers per sequence, or $2 L n d g / h$ with $g$ key-value heads shared by $h$ query heads. For long contexts and large batches, the cache, not the weights, fills the accelerator memory.

## In plain words

To write the next word, the model looks back at every word so far. For each old word it uses two lists of numbers, a key and a value. These lists depend only on that word and the words before it, so they stay the same as the text grows. Without a cache, the model makes them again for every old word at every step, which wastes most of the work. With a cache, it makes them once, keeps them, and at each step only makes the lists for the new word. The cost is the space to keep them all.

## The abstract type

For one sequence, the cache is a list of entries per layer $l = 1 \ldots L$ and per key-value head $j = 1 \ldots g$. Each entry is a pair of vectors (key, value) of size $d_k = d / h$. The operations are:

- **append(l, keys, values):** add the keys and values of the next position to layer $l$, one pair per head;
- **keys(l, j) and values(l, j):** read all stored keys or values of head $j$ in layer $l$, in position order;
- **length:** the number of positions stored;
- **release:** free the storage of a finished sequence.

Entries are never changed after they are appended. A serving system also needs **truncate**, to drop the last entries after a rejected draft in [speculative decoding](/speculative-decoding/), and **fork**, to share a prefix between sequences, as in beam search or parallel sampling.

## Representation

The simple representation keeps, per layer and head, two growable arrays of vectors ([dynamic arrays](/dynamic-array/)), or one preallocated tensor of shape $L \times 2 \times g \times n_{\max} \times d_k$ per sequence. The tensor form is fast to read, but it reserves memory for the longest possible sequence, and most of it stays unused.

PagedAttention (Kwon et al. 2023) splits the cache into blocks of $b$ positions. A pool holds the physical blocks, and a [free list](/free-list/) holds the free ones. Each sequence has a block table that maps its logical block $\lfloor i / b \rfloor$ to a physical block, and position $i$ lives in slot $i \bmod b$ of that block. A sequence takes a new block only when its last block is full, so it wastes at most $b - 1$ slots, and a finished sequence returns its blocks to the pool. Sequences can share blocks of a common prefix, with a reference count and copy on write.

## Operations

One decoding step of a toy transformer with a cache, for a new token at position $pos$:

```pseudo id=main
DECODE-STEP(params, token, pos, cache)
L1  x ← embedding(token) + position(pos)
L2  for l ← 1 to L do
L3      q_1 .. q_h ← split(x W_Q),  k_1 .. k_g ← split(x W_K),  v_1 .. v_g ← split(x W_V)
L4      cache.append(l, k_1 .. k_g, v_1 .. v_g)
L5      for each query head i: a_i ← attention(q_i, cache.keys(l, j), cache.values(l, j)) with j = the group of i
L6      x ← x + concat(a_1 .. a_h) W_O
L7      x ← x + FFN(x)
L8  return the logits x E^T                         ▷ E = the embedding matrix
```

Here $\text{attention}(q, K, V) = \text{softmax}(q K^T / \sqrt{d_k}) V$, and query head $i$ uses key-value head $j = \lfloor i / (h / g) \rfloor$ (numbering from 0). With $g = h$ this is [multi-head attention](/multi-head-attention/), with $g = 1$ multi-query attention, and in between [grouped-query attention](/grouped-query-attention/). The toy network has no layer normalization; adding it changes nothing about the cache. To process a prompt, call DECODE-STEP for each prompt token in order (real systems do the prompt in one parallel pass, which fills the same entries), then generate.

## Example

A model has $L = 2$ layers and $h = 2$ heads. Generate $n = 4$ positions, one after the other.

Without a cache, step $m$ (for $m = 1 \ldots 4$) recomputes all $m$ positions, and position $i$ attends to $i$ keys, so step $m$ computes $1 + 2 + \cdots + m = m(m+1)/2$ attention scores per head and layer. The four steps compute $1 + 3 + 6 + 10 = 20 = n(n+1)(n+2)/6$ scores per head and layer, 80 in all.

With a cache, step $m$ computes the new position only, which attends to $m$ keys: $1 + 2 + 3 + 4 = 10 = n(n+1)/2$ scores per head and layer, 40 in all. The test counts these scores and checks that the logits of both ways agree within $10^{-9}$, for $g = h$, for $g = h/2$ and for $g = 1$.

For memory, take $L = 32$ layers, width $d = 4096$, $h = 32$ heads and a context of $n = 4096$ tokens. The cache holds $2 \times 32 \times 4096 \times 4096 = 1073741824$ numbers per sequence, which is 2 GiB at 2 bytes per number. With $g = 8$ key-value heads it holds a quarter of that, 512 MiB. A batch of 16 such sequences needs 32 GiB with full multi-head attention.

A paged pool with blocks of $b = 4$ positions and 5 blocks serves a sequence of 6 positions (2 blocks) and one of 5 positions (2 blocks), leaving 1 block free. When the first sequence ends, its 2 blocks return to the pool, and a new sequence of 12 positions takes 3 blocks. A thirteenth position finds no free block, and the allocation fails; a real server would then preempt a sequence.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows, by induction over the positions and the layers, that the key and value of position $i$ in layer $l$ depend only on the tokens $1 \ldots i$, because of the causal mask. So the values cached when position $i$ was new are the values that a full recomputation at any later step would produce, and DECODE-STEP returns the same logits as the full forward pass on the whole prefix. The same argument shows that the paged cache returns the same keys and values as the flat one, since the block table is a bijection from positions to slots. In floating point the two ways can round differently, because the sums may run in a different order; the test allows $10^{-9}$, and the code sums with math.fsum.

## Complexity

**Time per step.** The projections of line L3 and the feed-forward block of line L7 cost $O(d^2)$ per layer for the new position (with a feed-forward width of $O(d)$). Attention over $n$ cached positions costs $O(n d_k)$ per query head for the scores and the same for the weighted sum, $O(n d)$ over all heads. So a step costs $O(L (n d + d^2))$ in the real RAM, plus $O(d |V|)$ for the logits. Without the cache, a step costs $O(L (n^2 d + n d^2))$. Over $n$ steps, the attention scores number $L h n (n+1)/2$ with the cache and $L h n (n+1)(n+2)/6$ without it.

**Memory.** $2 L n d g / h$ numbers per sequence: 2 for keys and values, $L$ layers, $n$ positions, and $g$ heads of $d_k = d / h$ numbers. For $g = h$ this is $2 L n d$. A paged cache with blocks of $b$ positions uses at most $b - 1$ extra slots per sequence.

**Memory traffic.** At small batch sizes, a decoding step reads every weight and every cached entry once for a few operations each, so it is limited by memory bandwidth, not arithmetic (see the [roofline model](/roofline-model/)). Shrinking the cache by sharing key-value heads reduces this traffic, which is why multi-query and grouped-query attention speed up decoding in practice, a measurement on the hardware of each paper.

## Variants

- **Multi-query and grouped-query attention.** Share each key-value head among $h / g$ query heads (Shazeer 2019; Ainslie et al. 2023). The cache shrinks by the factor $h / g$; whether quality drops is a measurement.
- **Paged cache.** Fixed blocks with a block table and a free list (Kwon et al. 2023), with prefix sharing between sequences.
- **Quantized cache.** Store keys and values in 8 or fewer bits, with a scale per block or per channel.
- **Sliding window.** Keep only the last $w$ positions, as a ring buffer; the memory is then $2 L w d g / h$, and the model must have been trained to attend within a window.
- **Eviction.** Drop the entries that received little attention so far. This changes the model's output, unlike the exact cache.
- **Prefix cache.** Keep the cache of a common prompt, such as a system prompt, and start each request from a copy of it.

## When to use it

Use a key-value cache in every autoregressive decoder of a transformer; recomputing the past is never cheaper for more than a few tokens. Choose the representation by the workload: a preallocated tensor for one sequence of known length, a paged pool for a server with many requests of unknown length, and grouped-query attention or quantization when the cache does not fit.

## Pitfalls

- **Positions.** The new token must get its true position, the number of tokens before it, not 0. With rotary embeddings the cached keys already carry their rotation; do not rotate them again.
- **Stale entries.** After a rejected draft in speculative decoding, or after a beam is dropped, truncate the cache to the accepted length. Stale entries silently change the output.
- **Beam search copies.** When beams reorder, the cache must follow them. Copying the whole cache at each step is slow; share prefixes with a paged cache.
- **Memory planning.** Size the cache for the longest sequence times the batch. Running out of memory in the middle of a batch means preempting a sequence and recomputing its cache later.
- **Masks with padding.** In a batch of sequences of different lengths, the attention mask must hide the padding slots of the cache.

## Implementations

The code builds a toy transformer with seeded random weights, keeps the cache as plain lists, and tests the cached decoder against recomputation; it takes the weights as given and does not train a network. The paged version keeps a block pool with a free list and a block table per sequence.

## History

Incremental decoding with stored keys and values goes back to the first transformer implementations, since the causal mask of Vaswani et al. 2017 makes the past keys and values fixed. Shazeer 2019 analyzed its memory traffic and proposed multi-query attention to shrink it, and Ainslie et al. 2023 proposed grouped-query attention as a middle ground. Kwon et al. 2023 brought paging from operating systems to the cache with PagedAttention, in the vLLM serving system.

## References
