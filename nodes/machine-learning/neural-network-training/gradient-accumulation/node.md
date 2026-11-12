---
tag: H2P10E
kind: technique
slug: gradient-accumulation
name: Gradient accumulation
area: machine-learning/neural-network-training
level: advanced
summary: "Adds the gradients of m micro-batches, each weighted by its share of the batch, then takes one step. Exact for a mean loss; not exact with batch normalization."
prereqs: [stochastic-gradient-descent, backpropagation]
see_also: [batch-normalization, data-parallelism, gradient-checkpointing, mixed-precision-training, learning-rate-schedule, gradient-clipping, layer-wise-adaptive-rate-scaling, lamb]
sources:
  - url: https://arxiv.org/abs/1806.00187
    title: Myle Ott, Sergey Edunov, David Grangier and Michael Auli, Scaling neural machine translation, WMT 2018
    locator: Section 4.2 (training with larger batches by accumulating the gradients of several batches before an update) and Table 1 (cumul = 16)
  - url: https://arxiv.org/abs/1706.02677
    title: Priya Goyal and others, Accurate, large minibatch SGD, training ImageNet in 1 hour, arXiv 2017
    locator: Section 2.3 (batch normalization breaks the independence of the per example losses; the per worker batch size n is kept fixed) and Section 3 (normalize the per worker loss by the total batch size kn, not by n)
  - url: https://arxiv.org/abs/1705.08741
    title: Elad Hoffer, Itay Hubara and Daniel Soudry, Train longer, generalize better, closing the generalization gap in large batch training of neural networks, NeurIPS 2017
    locator: Section 4 and Algorithm 1 (Ghost Batch Normalization, statistics computed on small virtual batches)
---

Gradient accumulation trains with a batch that does not fit in memory. It splits the batch $B$ into $m$ micro-batches $B_1, \dots, B_m$, runs the forward and backward pass on one micro-batch at a time, adds the gradients into one buffer with the weight $|B_j|/|B|$, and takes one optimizer step with the sum. When the loss is a mean of per example terms, the sum is exactly the gradient of the whole batch, so the run is the same as training with batch $B$, with the activation memory of one micro-batch. When the loss couples the examples of a batch, as [batch normalization](/batch-normalization/) does, the two are not equal. Ott and others (2018) used it to train translation models with the gradients of 16 batches per update on one machine.

## In plain words

A large batch gives a better estimate of the gradient, but the memory of the GPU limits how many examples one pass can hold. Gradient accumulation cuts the batch into small parts. It computes the gradient of each part, adds it to a running total, and only changes the weights when all parts are done. Each part counts in proportion to its number of examples.

If the loss of each example depends only on that example, the total is the same number that one large pass would give. If the network mixes examples, for example by normalizing with the mean of the batch, then each small part sees different statistics and the total is a different number.

## When it applies

- **Memory bound.** The batch size that the method needs, for example the batch of a [learning rate schedule](/learning-rate-schedule/) tuned at a large scale, is larger than the batch whose activations fit in memory.
- **Few devices.** A run designed for $k$ devices with [data parallelism](/data-parallelism/) is reproduced on fewer devices: each device accumulates $m$ micro-batches so that $k$ devices times $m$ micro-batches times the micro-batch size equals the original batch.
- **Less communication.** With data parallelism the workers exchange gradients once per optimizer step instead of once per micro-batch, so the cost of the exchange is shared by $m$ passes.
- **A loss that is a mean of per example terms**, or a loss whose coupling between examples you accept to change, as with batch normalization below.

It does not make training faster per example: the $m$ passes run one after the other, and the network computes the same number of forward and backward passes as with one large batch.

## The template

Let the batch loss be the mean $L_B(w) = \frac{1}{|B|}\sum_{i \in B}\ell_i(w)$. For a partition of $B$ into $B_1, \dots, B_m$,
$$L_B(w) = \sum_{j=1}^m \frac{|B_j|}{|B|}\,L_{B_j}(w), \qquad \nabla L_B(w) = \sum_{j=1}^m \frac{|B_j|}{|B|}\,\nabla L_{B_j}(w),$$
because a sum over $B$ is the sum of the sums over the parts, and the gradient is linear. With equal sizes the weight is $1/m$.

```pseudo id=main
GRADIENT-ACCUMULATION(w, batches, sizes)       ▷ sizes = (|B₁|, …, |Bₘ|)
L1  for each batch B do
L2      a ← 0                                  ▷ one buffer, the size of w
L3      for each micro-batch Bⱼ of B do
L4          gⱼ ← ∇ L_Bⱼ(w)                      ▷ forward and backward pass on Bⱼ only
L5          a ← a + (|Bⱼ| / |B|) gⱼ
L6      w ← optimizer step(w, a)               ▷ SGD, momentum, Adam, …
L7  return w
```

The weights do not change inside the inner loop, so every $g_j$ is taken at the same $w$, and after L5 runs $m$ times $a = \nabla L_B(w)$. The optimizer at L6 sees the same gradient as with one pass over $B$, so its state (momentum, second moments) and its step count are the same too. The implementation uses SGD at L6.

Memory: the activations of one micro-batch, about $1/m$ of those of $B$, plus one buffer of the size of the parameters. Time: the same number of example passes as one large batch, with one optimizer step per $m$ passes.

## Classic examples

**Unequal micro-batches by hand.** Take the model $\hat y = wx$ with squared error, $w = 0$, and the batch $(x, y) = (1, 1), (1, 3), (2, 2)$. The per example gradients $2(wx - y)x$ are $-2$, $-6$ and $-8$, so $\nabla L_B = -16/3$. Split the batch into $B_1 = \{(1, 1), (1, 3)\}$ and $B_2 = \{(2, 2)\}$, with mean gradients $-4$ and $-8$. With the weights $2/3$ and $1/3$ the sum is $-8/3 - 8/3 = -16/3$, exact. With the weight $1/m = 1/2$ for each part it is $-6$, which gives the single example of $B_2$ the weight of two. Summing without any weight gives $-12$.

**Batch normalization, a counterexample.** Let the model be $z_i = w^\top x_i$, normalized with the statistics of its batch, $\hat z_i = (z_i - \mu_B)/\sigma_B$, with the loss $\frac{1}{|B|}\sum_i(\hat z_i - y_i)^2$. Take $w = (1, 0)$, so $z_i$ is the first input. The micro-batches have first inputs $\{-7, -1, 1, 7\}$ and $\{17, 23, 25, 31\}$; each has standard deviation $5$, and the whole batch has mean $12$ and standard deviation $13$. With second inputs $1, 0, 2, 1, 0, 1, 1, 2$ and targets $-1, 0, 1, 0, 1, -1, 1, 0$, the exact gradients are

| | gradient |
|---|---|
| whole batch of 8 | $(0,\ 15/4394) \approx (0,\ 0.0034)$ |
| accumulated over two micro-batches of 4 | $(0,\ -27/1000) = (0,\ -0.027)$ |

The second component even has the opposite sign. The accumulated gradient is the exact gradient of a different loss: the mean of the two micro-batch losses, each normalized with its own statistics. That is ghost batch normalization (Hoffer and others, 2017), which normalizes small virtual batches inside a large batch on purpose. Without the normalization, the same split gives the exact gradient of the whole batch.

**Translation with 16 batches per update.** Ott and others (2018) accumulate the gradients of 16 batches before each update on one machine with 8 GPUs, which gives an effective batch of about 400K tokens. In their Table 1, this setting together with 16 bit training runs about 3.2 times as fast as their baseline.

## Variations

- **Per token weighting.** For sequence models whose loss is a mean over tokens, the weight of a micro-batch is its number of target tokens over the number in the batch, not its number of sequences. With padding and varied lengths the two differ.
- **Sum the losses, divide once.** An equivalent form adds the unnormalized sums $\sum_{i \in B_j}\nabla\ell_i$ and divides by $|B|$ at the end. Goyal and others (2017) state the data parallel version of this rule: normalize the loss of each worker by the total batch size, not the worker's own.
- **Data parallel accumulation.** With $k$ workers, each accumulates its $m$ micro-batches locally and the workers average once per step. Libraries offer a mode that skips the exchange on the first $m - 1$ backward passes.
- **Ghost batch normalization.** Splitting a batch into small groups for the normalization statistics on purpose, while the gradient covers the whole batch.
- **Alternatives for normalization.** [Layer normalization](/layer-normalization/) and other per example normalizations do not couple the examples, so accumulation is exact with them.
- **With activation recomputation.** [Gradient checkpointing](/gradient-checkpointing/) reduces the memory of one pass; the two combine when one micro-batch still does not fit.

## Pitfalls

- **Wrong scale.** Adding the micro-batch mean gradients without a weight gives $m$ times the gradient of the batch, which acts like an $m$ times larger learning rate for SGD. Adam and other normalized methods hide much of the error, but weight decay and gradient clipping thresholds then act at the wrong scale.
- **Unequal sizes.** Dividing each micro-batch loss by $m$ is right only when all parts have the same size. The last micro-batch of an epoch and micro-batches with different token counts need the weight $|B_j|/|B|$.
- **Losses that couple examples.** Batch normalization, contrastive losses with in-batch negatives and any loss that uses statistics of the batch give a different value on each micro-batch. Accumulation then optimizes a different objective, and its gradient is not the large batch gradient. The running statistics of batch normalization are also updated $m$ times per step with micro-batch statistics.
- **Forgotten reset.** Frameworks that add each backward pass into the gradient buffer need the buffer set to zero after each optimizer step (L2); otherwise gradients of earlier steps stay in it.
- **Step counts.** The [learning rate schedule](/learning-rate-schedule/), warmup and logging count optimizer steps (L6), not micro-batches. A schedule set in micro-batches runs $m$ times too fast.
- **Clip after the sum.** [Gradient clipping](/gradient-clipping/) applies to the accumulated gradient $a$, once per step. Clipping each $g_j$ gives a different update.
- **Rounding.** In floating point the sum in another order can round differently, so the result agrees with the large batch only up to rounding. With [mixed precision training](/mixed-precision-training/) keep the buffer in 32 bit.
- **Not more updates.** Compared with training at the micro-batch size, accumulation makes $m$ times fewer updates per epoch. It reproduces the large batch, not the small one.

## Exercises

1. Show that $\nabla L_B(w) = \sum_j(|B_j|/|B|)\nabla L_{B_j}(w)$ for any partition of $B$, and that the weights $1/m$ give the same result for every loss only when all $|B_j|$ are equal.
2. A batch of 10 examples is split into micro-batches of 7 and 3, and each micro-batch loss is divided by $m = 2$. Which weight does each example get, compared with $1/10$?
3. Show that for a batch of two examples with $z_1 \ne z_2$, batch normalization without the affine part outputs $\pm 1$ whatever $w$ is, so the loss gradient in $w$ is zero. What does accumulation with micro-batches of size 2 then compute?
4. With $k$ workers, a micro-batch size $b$ and $m$ accumulation steps, what is the effective batch size, and how many gradient exchanges per epoch of $N$ examples does each choice of $m$ need?

## References
