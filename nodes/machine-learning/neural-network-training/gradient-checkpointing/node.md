---
tag: 6X8J45
kind: technique
slug: gradient-checkpointing
name: Gradient checkpointing
aliases:
- activation checkpointing
- rematerialization
- sublinear memory backpropagation
area: machine-learning/neural-network-training
level: advanced
summary: "Keep only some activations in the forward pass and recompute the rest in the backward pass: O(sqrt n) memory for one extra forward pass on an n-layer chain."
prereqs: [backpropagation, automatic-differentiation]
see_also: [backpropagation-through-time, computational-graph, gradient-accumulation, mixed-precision-training, pebbling-lower-bound, red-blue-pebble-game, binomial-coefficient, reversible-computation]
sources:
  - paper: "Tianqi Chen, Bing Xu, Chiyuan Zhang and Carlos Guestrin, Training deep nets with sublinear memory cost, arXiv:1604.06174, 2016"
    locator: Section 4 (recomputation by segments, the O(sqrt n) memory plan with one extra forward pass, and the recursive O(log n) plan)
  - paper: doi:10.1080/10556789208805505
    title: "Andreas Griewank, Achieving logarithmic growth of temporal and spatial complexity in reverse automatic differentiation, Optimization Methods and Software 1(1), 1992"
    locator: pp. 35 to 54 (binomial reversal schedules; logarithmic growth of memory and of the number of repeated steps)
  - paper: doi:10.1145/347837.347846
    title: "Andreas Griewank and Andrea Walther, Algorithm 799: revolve: an implementation of checkpointing for the reverse or adjoint mode of computational differentiation, ACM Transactions on Mathematical Software 26(1), 2000"
    locator: pp. 19 to 45 (the binomial schedule, its optimality for a given number of checkpoints, and the code)
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, 2nd edition, SIAM, 2008
    locator: Chapter 12 (reversal schedules and checkpointing)
---

Gradient checkpointing reduces the memory of [backpropagation](/backpropagation/) by keeping only some of the forward activations, the checkpoints, and recomputing the others during the backward pass from the nearest checkpoint before them. On a chain of $n$ layers cut into segments of $k = \lceil \sqrt n \rceil$ layers, it keeps about $2\sqrt n$ activations instead of $n$, for $n - \lceil n/k \rceil$ extra layer evaluations, less than one extra forward pass (Chen, Xu, Zhang and Guestrin 2016). Binomial checkpointing (Griewank 1992) goes further and gives memory and recomputation that grow only logarithmically in $n$.

## In plain words

Backpropagation goes through the layers twice: forward to compute the output, then backward to compute the gradient. The backward pass needs the input of every layer, so the usual method keeps all of them in memory. For a deep network or a long sequence, this memory is often larger than the model.

Checkpointing keeps only a few of these inputs, say every tenth one. When the backward pass reaches a block of ten layers, it runs the forward pass again over that block, starting from the saved input at its start, and so gets back the inputs it needs. Then it runs backward through the block and frees them. You pay with some repeated work, and you save most of the memory.

## When it applies

The method applies to any gradient computed in reverse mode, where the backward pass reads values of the forward pass: deep feedforward networks, [backpropagation through time](/backpropagation-through-time/) on long sequences, and the adjoint method for simulations with many time steps. It needs two properties:

- **Recomputation gives the same values.** The forward pass of a segment must be repeatable. Random operations such as dropout must reuse the same random numbers, for example by saving the generator state at each checkpoint.
- **Memory, not time, is the limit.** The method trades compute for memory. It helps when activations do not fit, or when the saved memory allows a larger batch or a larger model.

**Cost of the segment plan.** Take a chain $x_i = F_i(x_{i-1})$ of $n$ layers with segments of $k$ layers, so there are $S = \lceil n/k \rceil$ segments. The forward pass keeps the $S$ segment inputs $x_0, x_k, x_{2k}, \ldots$. In the backward pass, a segment of $\ell$ layers recomputes $\ell - 1$ inputs. So:

- the extra layer evaluations are $\sum_s (\ell_s - 1) = n - S$, fewer than one forward pass;
- the peak number of kept states is $S + \min(k, n) - 1$: the checkpoints of the earlier segments, plus the recomputed inputs of one segment.

The term $n/k + k$ is smallest near $k = \sqrt n$, which gives at most $2\lceil \sqrt n \rceil - 1$ kept states. For a perfect square $n = k^2$ it is exactly $2k - 1$ states and $2n - k$ layer evaluations in total.

## The template

```pseudo id=main
CHECKPOINTED-BACKPROP(F_1..F_n, x_0, k)
L1  for i ← 1 to n do                           ▷ forward pass
L2      x_i ← F_i(x_{i−1})
L3      if k divides i and i < n then keep x_i as a checkpoint; else free x_{i−1} unless it is x_0 or a checkpoint
L4  ḡ ← ∂ℓ/∂x_n
L5  for each segment [a+1, e] of k layers, from the last segment to the first do
L6      recompute x_{a+1}, ..., x_{e−1} from the checkpoint x_a and keep them
L7      for i ← e down to a + 1 do
L8          (∂ℓ/∂θ_i, ḡ) ← the backward rule of F_i at x_{i−1}, applied to ḡ
L9      free x_{a+1}, ..., x_{e−1} and the checkpoint x_e
L10 return all ∂ℓ/∂θ_i and ḡ = ∂ℓ/∂x_0
```

Line L8 is the same vector Jacobian product as in plain backpropagation, on the same values, so the gradient is the same, bit for bit. Only the order in which values are stored and recomputed changes.

## Classic examples

**Memory and work on a chain of 100 layers.** With $n = 100$ and segments of $k$ layers, counting kept layer inputs and layer evaluations:

| $k$ | segments $S$ | peak kept states | layer evaluations |
|---|---|---|---|
| 1 (store all) | 100 | 100 | 100 |
| 5 | 20 | 24 | 180 |
| 10 | 10 | 19 | 190 |
| 20 | 5 | 24 | 195 |
| 50 | 2 | 51 | 198 |
| 100 (store only $x_0$) | 1 | 100 | 199 |

At $k = 10 = \sqrt{100}$ the memory drops from 100 to 19 states, and the work grows from 100 to 190 evaluations. The backward pass costs about two forward passes, so the total time grows from about 300 to 390 layer units, by 30 percent.

**Deep networks.** Chen et al. (2016) applied the segment plan to the computational graph of deep networks, placing checkpoints at the outputs of selected layers. Their recursive variant keeps a checkpoint plan inside each segment and reduces memory to $O(\log n)$ for $O(n \log n)$ extra work. Deep learning frameworks provide the plan as a wrapper around a block of layers, and large transformer models are often trained with one checkpoint per block.

**Binomial checkpointing.** Griewank (1992) asked: with $c$ checkpoint slots and a bound $r$ on how often a step may be repeated, the repetition number, how long a chain can be reversed? The answer is a binomial coefficient: in the counting of Griewank and Walther, the longest chain has $\binom{c + r}{c}$ steps. Conversely, for a chain of $n$ steps and $c$ slots, the repetition number $r$ is the smallest one with $n \le \binom{c+r}{c}$. Taking $c$ and $r$ both of order $\log n$ gives memory and work per step that grow only logarithmically in $n$. The program revolve (Griewank and Walther 2000) computes such a schedule, and it is optimal: no schedule with $c$ slots needs fewer forward steps. For $n = 100$ and $c = 10$ slots, $\binom{12}{10} = 66 < 100 \le \binom{13}{10} = 286$, so the repetition number is 3.

## Variations

- **Uniform segments.** The $\sqrt n$ plan above, simple and nearly optimal when all layers cost the same and have outputs of the same size.
- **Optimal placement on a graph.** For layers of unequal cost and size, choose the checkpoints by dynamic programming or integer programming over the [computational graph](/computational-graph/). The general problem is a [pebble game](/pebbling-lower-bound/) on a graph, a hard combinatorial problem, so practical systems use heuristics or integer programming solvers.
- **Binomial checkpointing.** The schedule of Griewank and revolve, for very long chains such as time steps of a simulation, with a fixed number of slots.
- **Offloading.** Move activations to host memory or disk instead of recomputing them; useful when the transfer is faster than the recomputation.
- **Reversible layers.** If each layer can be inverted, as in reversible residual networks, the backward pass recomputes $x_{i-1}$ from $x_i$, and no activations are stored at all, at the cost of one inverse per layer and some rounding drift.
- **Selective recomputation.** Recompute only the cheap operations with large outputs, such as activation functions and attention scores, and keep the costly matrix products.

## Pitfalls

- **Randomness in the forward pass.** Dropout or noise must produce the same values on recomputation. Save and restore the random generator state, or the gradient belongs to a different network.
- **Side effects.** Batch normalization updates its running statistics in the forward pass; a recomputed forward pass must not update them twice.
- **Checkpoints at the wrong places.** A checkpoint at a small tensor saves much; one at a large tensor saves nothing. On a graph with branches, a checkpoint inside a branch may still leave the other branch's activations alive.
- **No gain from tiny segments.** With $k = 1$ every state is a checkpoint, and with $k = n$ the last segment keeps $n$ recomputed states. The memory is lowest near $k = \sqrt n$, not at either end.
- **Counting only activations.** The parameters, the gradients and the optimizer state also need memory. If they dominate, checkpointing helps little.

## Exercises

1. Show that the segment plan with $S = \lceil n/k \rceil$ segments makes exactly $n - S$ extra layer evaluations.
2. Show that the peak number of kept states is $S + \min(k, n) - 1$, and that it is at most $2 \lceil \sqrt n \rceil - 1$ for $k = \lceil \sqrt n \rceil$.
3. Apply the segment plan recursively inside each segment. Show that with $\log_2 n$ levels of halving the memory is $O(\log n)$ states and the work is $O(n \log n)$ layer evaluations.
4. For $n = 64$, compare the peak memory and the layer evaluations of the plans with $k = 4$, $k = 8$ and $k = 16$.

## References
