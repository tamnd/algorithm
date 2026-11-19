---
tag: 5X6J97
kind: algorithm
slug: flashattention
name: FlashAttention
aliases:
- IO-aware exact attention
area: natural-language-and-speech/language-modeling
level: research
summary: "Exact attention computed in tiles that fit in fast on-chip memory with an online softmax, so the n by n score matrix is never written out."
model: floating-point-model
complexity:
  vars: {N: the sequence length, d: the head size, M: the size of the fast memory in numbers}
  time: {worst: "Θ(N^2 d)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2022
  people: [Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré]
  note: Dao and colleagues combined tiling with the online softmax of Milakov and Gimelshein, and counted the transfers between GPU high-bandwidth memory and on-chip memory.
prereqs: [scaled-dot-product-attention, log-sum-exp-trick, shared-memory-tiling]
see_also: [multi-head-attention, external-memory-model, red-blue-pebble-game, blocked-matrix-multiplication, roofline-model, loop-tiling, transformer, key-value-cache]
sources:
  - paper: doi:10.52202/068431-1189
    title: "Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra and Christopher Ré, FlashAttention: fast and memory-efficient exact attention with IO-awareness, Advances in Neural Information Processing Systems 35 (NeurIPS 2022), arXiv:2205.14135"
    locator: "Section 3.1 and Algorithm 1 (tiling, the online softmax, the block sizes), Theorem 1 (correctness, O(N^2 d) FLOPs, O(N) extra memory), Theorem 2 (HBM accesses of standard attention and of FlashAttention), Proposition 3 (the lower bound), Section 4 (measured speed-ups)"
  - paper: "Maxim Milakov and Natalia Gimelshein, Online normalizer calculation for softmax, arXiv:1805.02867, 2018"
    title: Milakov and Gimelshein 2018
    locator: the one-pass softmax that keeps a running maximum and a running sum
  - paper: "Markus N. Rabe and Charles Staats, Self-attention does not need O(n^2) memory, arXiv:2112.05682, 2021"
    title: Rabe and Staats 2021
    locator: attention by chunks of keys with a running maximum, in O(log n) or O(sqrt n) memory
  - paper: "Tri Dao, FlashAttention-2: faster attention with better parallelism and work partitioning, arXiv:2307.08691, 2023"
    title: Dao 2023
    locator: the swapped loop order, the deferred division by the running sum, and parallelism over the sequence
---

FlashAttention computes exactly the same output as [scaled dot-product attention](/scaled-dot-product-attention/), $\operatorname{softmax}(Q K^\top / \sqrt{d})\, V$, but never stores the $N \times N$ score matrix. It cuts $Q$, $K$ and $V$ into blocks small enough to fit in the fast on-chip memory of a GPU, and for each query row it keeps only a running maximum, a running sum and a running output. When a new block of keys arrives, it rescales what it has so far to the new maximum. This is the online softmax. The arithmetic stays $\Theta(N^2 d)$, but the number of transfers to and from the slow main memory drops from $\Theta(N d + N^2)$ to $\Theta(N^2 d^2 / M)$, where $M$ is the size of the fast memory, and the extra memory drops from $\Theta(N^2)$ to $\Theta(N)$. Attention on a GPU is usually limited by memory traffic, not by arithmetic, so this makes it faster as well as smaller.

## In plain words

Plain attention first writes a huge table of scores, one for every pair of words, then reads it back to turn the scores into weights, then reads it again to mix the values. For long texts the table is too big to keep close to the processor, so most of the time goes into moving it.

FlashAttention never builds the table. It reads a small group of words, computes their scores in fast memory, uses them at once, and throws them away. To do this it keeps three running numbers per word: the highest score seen so far, a running total, and a running answer. When a higher score turns up, it shrinks the old total and answer so that everything is measured against the new highest score. At the end the answer is exactly what plain attention gives.

## The problem

The input is $Q$ of shape $N \times d$ and $K$, $V$ of shape $N \times d$ (more generally $n \times d_k$, $m \times d_k$ and $m \times d_v$), stored in slow memory, and an optional causal mask. The output is $O = \operatorname{softmax}(Q K^\top / \sqrt{d} + B) V$ in slow memory, with $B$ the mask bias as on the page of [scaled dot-product attention](/scaled-dot-product-attention/).

The cost model has two levels: a slow memory of unbounded size (the GPU high-bandwidth memory, HBM) and a fast memory of $M$ numbers (on-chip SRAM), with $d \le M \le N d$. Arithmetic happens only on data in fast memory. The cost to minimize is the number of numbers moved between the two levels, as in the [external memory model](/external-memory-model/) with block size 1, or the [red-blue pebble game](/red-blue-pebble-game/). Standard attention writes $S = Q K^\top$ to slow memory, reads it to compute $P = \operatorname{softmax}(S)$, writes $P$, and reads it again to compute $P V$: $(n + m) d_k + 4 n m + m d_v + n d_v$ transfers.

## The algorithm

Cut the keys and values into $T_c = \lceil m / B_c \rceil$ blocks of $B_c$ rows and the queries into blocks of $B_r$ rows. Algorithm 1 of the paper uses $B_c = \lceil M / 4d \rceil$ and $B_r = \min(\lceil M / 4d \rceil, d)$, so that a block of $K$, a block of $V$, a block of $Q$, a block of $O$ and a $B_r \times B_c$ score tile fit in fast memory together. For each query row $r$ the slow memory holds the output row $O_r$, the running sum $\ell_r$ and the running maximum $m_r$.

```pseudo id=main
FLASH-ATTENTION(Q, K, V, B_r, B_c)
L1  O ← 0;  ℓ ← 0;  m ← -∞                   ▷ n × d_v, n and n numbers in slow memory
L2  for each block K_J, V_J of B_c keys do      ▷ read into fast memory
L3      for each block Q_I, O_I, ℓ_I, m_I of B_r queries do   ▷ read into fast memory
L4          S ← Q_I K_J^T / √d_k, masked entries set to -∞     ▷ B_r × B_c, in fast memory
L5          for each row r of the block with a finite score in S_r do
L6              m̃ ← max_c S_rc;  p_c ← exp(S_rc - m̃);  ℓ̃ ← Σ_c p_c
L7              m' ← max(m_r, m̃)
L8              ℓ' ← e^(m_r - m') ℓ_r + e^(m̃ - m') ℓ̃
L9              O_r ← (e^(m_r - m') ℓ_r O_r + e^(m̃ - m') Σ_c p_c V_c) / ℓ'
L10             m_r ← m';  ℓ_r ← ℓ'          ▷ O_I, ℓ_I, m_I written back to slow memory
L11 return O
```

Lines L6 to L10 are the online softmax. Line L6 is a local softmax of the tile row, stable because $\tilde m$ is its maximum. Lines L7 and L8 rescale the old sum and the new one to the common maximum $m'$ and add them. Line L9 does the same for the output: $\ell_r O_r$ is the unnormalized output so far, it is rescaled, the new block's unnormalized output is added, and the sum is divided by the new total. A real kernel computes lines L4 to L10 for the whole block at once with matrix products in fast memory. In the backward pass FlashAttention does not store $P$ either: it keeps $\ell$ and $m$ and recomputes the tiles of $S$ and $P$ from $Q$, $K$ and $V$.

## Example

One query, $d = 1$, so the scale is 1: $q = 1$, keys $k = (1, 3, 2, 0)$, so the scores are $(1, 3, 2, 0)$, and values $v = (10, 20, 30, 40)$. Blocks of $B_c = 2$ keys.

| step | block scores | $\tilde m$ | $p$ | $\tilde\ell$ | $m'$ | $\ell'$ | $O$ |
|---|---|---|---|---|---|---|---|
| L1 | | | | | $-\infty$ | 0 | 0 |
| block 1 | (1, 3) | 3 | (0.135335, 1) | 1.135335 | 3 | 1.135335 | 18.807971 |
| block 2 | (2, 0) | 2 | (1, 0.135335) | 1.135335 | 3 | 1.553002 | 22.138557 |

After block 1, $O = (0.135335 \cdot 10 + 1 \cdot 20) / 1.135335$, the attention of the query over the first two keys alone. At block 2 the maximum stays 3, so the old part keeps the factor $e^0 = 1$ and the new part gets $e^{2 - 3} = 0.367879$: $\ell' = 1.135335 + 0.367879 \cdot 1.135335$ and $O = (1.135335 \cdot 18.807971 + 0.367879 \cdot (30 + 0.135335 \cdot 40)) / 1.553002 = 22.138557$. The direct computation, $\sum_j e^{s_j} v_j / \sum_j e^{s_j}$, gives the same value.

## Correctness

The invariant, for each query row $r$: after the key blocks $1, \ldots, J$, $m_r$ is the largest visible score among those keys, $\ell_r = \sum_c e^{s_{rc} - m_r}$ over them, and $O_r$ is the attention output of row $r$ over those keys alone. Lines L7 to L10 keep it, because the old and the new parts are put on the common scale $e^{-m'}$ before they are added. After the last block the invariant is exactly the output of attention over all keys. Every exponent at lines L6, L8 and L9 is at most 0 and one of the two factors at line L8 is 1, so in the [floating-point model](/floating-point-model/) nothing overflows and $\ell' \ge 1$. The [full proof](proofs/correctness.md) gives the induction, the masked case, and the count of transfers.

## Complexity

- **Arithmetic.** Each pair of a query and a key is handled once at lines L4 and L9, at $\Theta(d)$ each, so $\Theta(N^2 d)$, the same as standard attention (Theorem 1 of the paper).
- **Extra memory.** $\ell$ and $m$ take $2N$ numbers beside the output: $\Theta(N)$ (Theorem 1). Standard attention stores $S$ and $P$, $\Theta(N^2)$.
- **Transfers (theorem).** $K$ and $V$ are read once, $N \cdot 2d$ numbers. For each of the $T_c$ key blocks, all of $Q$, $O$, $\ell$ and $m$ are read and $O$, $\ell$ and $m$ written, $N (3d + 4)$ numbers. With $B_c = \lceil M / 4d \rceil$, $T_c \approx 4 N d / M$, so the total is $\Theta(N^2 d^2 / M)$ (Theorem 2). Standard attention needs $\Theta(N d + N^2)$. For $N = 4096$, $d = 64$ and $M = 100000$ the exact counts of the code are about 9.6 million against 68.2 million.
- **Lower bound (theorem).** No exact attention algorithm has $o(N^2 d^2 / M)$ transfers for all $M$ in $[d, N d]$ (Proposition 3 of the paper), so FlashAttention is optimal in this sense up to a constant.

## Properties

- **Exact.** It computes the same function as standard attention; in floating point the results differ only by rounding, since the sums are taken in a different order.
- **No overflow.** All exponents are at most 0, as in the [log-sum-exp trick](/log-sum-exp-trick/).
- **Convex updates.** Line L9 is a convex combination of the old output and the block's values, so $O_r$ always stays inside the range of the values seen.
- **Memory linear in $N$.** This is what allows long sequences on a GPU.
- **Speed (measurement).** Dao and colleagues report 15% faster end-to-end training of BERT-large at sequence length 512 than the MLPerf 1.1 record, 3 times faster training of GPT-2 at length 1K than the HuggingFace and Megatron-LM baselines, and 2.4 times on long-range arena at lengths 1K to 4K. These depend on the GPU and the baseline.

## Variants and improvements

- **FlashAttention-2** (Dao 2023) puts the query blocks in the outer loop, so each output block is written once, divides by $\ell$ only at the end, and splits the work over the sequence as well as over heads.
- **Memory-efficient attention** (Rabe and Staats 2021) processes keys in chunks with the same running maximum, aiming at memory rather than at transfers.
- **Causal block skipping.** With a causal mask, key blocks that lie entirely after a query block can be skipped without reading them, which removes about half of the work.
- **Decoding.** With one query and a long [key-value cache](/key-value-cache/), the key blocks are split over many processors and the partial results $(m, \ell, O)$ are merged at the end with the same rescaling as lines L7 to L9.
- **Block-sparse attention.** Skipping blocks of a fixed sparse mask reduces transfers in proportion to the fraction of non-zero blocks.

## When to use it

Use it whenever exact softmax attention runs on a GPU or another processor with a small fast memory, which today is almost always; many deep learning libraries use it when the shapes and the hardware allow. It helps most for long sequences, where the $N^2$ matrix would dominate memory and traffic. It changes nothing in the arithmetic, so when $N$ is too large for $\Theta(N^2 d)$ work, use a model with linear cost, such as a [selective state space model](/selective-state-space-model/), or an approximate attention.

## Pitfalls

- **Forgetting the old rescaling.** Writing $\ell' \leftarrow \ell_r + \tilde\ell$ at line L8, or adding the new block to $O_r$ without the factor $e^{m_r - m'}$ at line L9, gives wrong weights as soon as a later block has a larger maximum. Both old terms must be multiplied by $e^{m_r - m'}$.
- **Unnormalized $O$.** Line L9 multiplies the stored $O_r$ by $\ell_r$ before adding, because $O_r$ is kept normalized. If the code keeps the unnormalized sum instead, as FlashAttention-2 does, it must not multiply by $\ell_r$ and must divide once at the end.
- **Fully masked tiles.** With a causal mask a tile row can have no visible key. Then $\tilde m = -\infty$ and $e^{\tilde m - \tilde m}$ at line L6 is undefined. Skip such rows, as line L5 does, and start $m$ at $-\infty$ with $\ell = 0$, so that $e^{-\infty} = 0$ removes the empty start at the first real update.
- **Comparing to the wrong reference.** Low-precision results differ from a float32 reference by rounding; compare with a tolerance, not for equality.

## Implementations

The code takes $Q$, $K$ and $V$ as given and does not train a network. It also returns the number of slow-memory transfers under the two-level model of the paper.

## History

Milakov and Gimelshein (2018) showed that the softmax normalizer can be computed in one pass with a running maximum. Rabe and Staats (2021) used this to compute attention in chunks with little memory. Dao, Fu, Ermon, Rudra and Ré (2022) counted the transfers between GPU memory levels, as Hong and Kung had done for other computations with the [red-blue pebble game](/red-blue-pebble-game/), proved matching upper and lower bounds, and wrote a fused GPU kernel for the forward and backward passes. FlashAttention-2 (2023) and later versions improved the use of the hardware.

## References
