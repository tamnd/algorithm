---
tag: KD5CZY
kind: technique
slug: mixed-precision-training
name: Mixed precision training
aliases:
- automatic mixed precision
- fp16 training
area: machine-learning/neural-network-training
level: advanced
summary: "Runs the forward and backward pass in FP16 or BF16, keeps FP32 master weights for the update, and scales the loss so that small FP16 gradients do not underflow."
prereqs: [ieee-754, backpropagation, stochastic-gradient-descent]
see_also: [bfloat16, ulp, subnormal-numbers, kahan-summation, stochastic-rounding, rounding-error-analysis, round-to-nearest-even, gradient-accumulation]
sources:
  - url: https://arxiv.org/abs/1710.03740
    title: Paulius Micikevicius, Sharan Narang, Jonah Alben, Gregory Diamos, Erich Elsen, David Garcia, Boris Ginsburg, Michael Houston, Oleksii Kuchaiev, Ganesh Venkatesh and Hao Wu, Mixed precision training, ICLR 2018
    locator: Section 3.1 (FP32 master copy of weights, updates below 2^-24 and the ratio 2048), Section 3.2 (loss scaling, Figure 3 with the SSD activation gradients, factors from 8 to 32K, skipping the update on overflow), Section 3.3 (FP16 products accumulated in FP32), Section 4 (results), Section 5 (automatic choice of the scale as future work)
  - url: https://docs.pytorch.org/docs/stable/amp.html
    title: PyTorch documentation, Automatic mixed precision package, torch.amp
    locator: GradScaler (init_scale = 65536, growth_factor = 2, backoff_factor = 0.5, growth_interval = 2000) and the autocast op lists
  - url: https://arxiv.org/abs/1905.12322
    title: Dhiraj Kalamkar and others, A study of BFLOAT16 for deep learning training, arXiv 2019
    locator: Section 2 (BF16 avoids loss scaling), Section 3 (BF16 inputs with FP32 accumulation and an FP32 copy of the weights), Section 4 (results without hyperparameter changes)
---

Mixed precision training runs most of the arithmetic of a neural network in a 16 bit floating point format and keeps the parts that need precision in 32 bit. Micikevicius and others (2018) gave the recipe for [IEEE 754](/ieee-754/) half precision (FP16): store weights, activations and gradients in FP16 for the forward and backward pass, sum long products in FP32, keep an FP32 master copy of the weights for the update, and multiply the loss by a scale factor so that small gradients stay above the FP16 underflow limit. This halves the memory of the activations and lets the hardware use its fast 16 bit units, and it trained convolutional, recurrent, speech, translation and GAN models to the accuracy of FP32 training. With [bfloat16](/bfloat16/) (BF16), which has the exponent range of FP32, the loss scale is not needed, but the master copy still is.

## In plain words

Numbers with 16 bits take half the memory and are faster to compute with than numbers with 32 bits, but they are coarse. Near 1 they can only change in steps of about one thousandth, and they cannot hold very small or very large values.

Training makes many tiny changes to the weights. If the weights themselves are 16 bit, a change that is too small to reach the next step is rounded away, every time. So the program keeps a 32 bit copy of the weights, adds the changes there, and makes a 16 bit copy for each pass.

Gradients can also be so small that they become zero. Multiplying the loss by a large number makes every gradient larger by the same factor; the program divides it out again in 32 bit before the update.

## When it applies

- **Hardware with fast 16 bit units**, such as GPUs with tensor cores or TPUs, where 16 bit matrix products run several times faster than 32 bit ones.
- **Memory bound training**, where the activations saved for [backpropagation](/backpropagation/) limit the batch or model size. FP16 activations take half the memory.
- **FP16 with gradients of small magnitude.** Loss scaling is needed when a large share of the gradient values fall below the smallest FP16 number, as in the SSD detector of the paper. Many image classifiers trained without it.
- **BF16 hardware.** BF16 needs no loss scale, so only the master copy and the FP32 sums remain.

It does not apply where the model needs more than about three significant decimal digits inside the forward pass, for example in large reductions, which therefore stay in FP32.

## The template

FP16 has 1 sign bit, 5 exponent bits and 10 fraction bits. Its largest finite value is $65504$, its smallest normal value $2^{-14}$, and its smallest [subnormal](/subnormal-numbers/) value $2^{-24}$. The spacing ([ulp](/ulp/)) at $1$ is $2^{-10}$, so the [machine epsilon](/machine-epsilon/) of [round to nearest even](/round-to-nearest-even/) is $2^{-11}$. BF16 has 8 exponent bits and 7 fraction bits: the range of FP32 and an ulp of $2^{-7}$ at $1$.

```pseudo id=main
MIXED-PRECISION-SGD(w, batches, η, S, N)        ▷ w: FP32 master weights, S: loss scale
L1  for each batch B do
L2      ŵ ← fp16(w)                              ▷ 16 bit copy for this pass
L3      ĝ ← FP16 forward and backward pass of S · L_B(ŵ)   ▷ products summed in FP32
L4      if some ĝᵢ is inf or NaN then
L5          S ← S / 2;  k ← 0                    ▷ back off
L6          skip this step
L7      g ← fp32(ĝ) / S                          ▷ unscale in FP32
L8      w ← w − η g                              ▷ update the FP32 master copy
L9      k ← k + 1
L10     if k = N then S ← 2S;  k ← 0             ▷ grow after N clean steps
L11 return w
```

L5 to L10 are dynamic loss scaling. A static scale keeps $S$ fixed and drops L5, L9 and L10; the paper sets it by hand or so that $S$ times the largest gradient stays below $65504$. Section 3.2 of the paper already skips the update on overflow, and Section 5 proposes adjusting the scale automatically. Libraries use the rule above; the PyTorch GradScaler starts at $S = 2^{16}$, multiplies by $0.5$ on overflow and by $2$ after $N = 2000$ clean steps. With an adaptive optimizer, L8 is the [Adam](/adam/) or [AdamW](/adamw/) step, with its moment estimates also in FP32.

**Why the master copy.** Round to nearest adds $u$ to $w$ correctly only if $u$ is at least half an ulp of $w$. If $w = 2^k$ and $0 < u \le 2^{k-11}$ (a ratio $w/u$ of at least $2048$), then $w + u$ rounds back to $w$ in FP16, and the update is lost. Repeating it does not help: each step rounds back again. In FP32 the ulp at $1$ is $2^{-23}$, so the same updates add up, and the FP16 copy at L2 changes once their sum reaches half an FP16 ulp.

**Why the scale.** A gradient value of magnitude at most $2^{-25}$ rounds to zero in FP16. Multiplying the loss by $S$ multiplies every gradient by $S$, because the backward pass is linear in the output gradient. A power of two as $S$ changes only the exponent, so in the normal range the scaling and the unscaling at L7 add no rounding error.

## Classic examples

**A lost update, by hand.** Start at $w = 1$ and add $u = 2^{-12}$ ten times. In FP16 the neighbours of $1$ above are $1$ and $1 + 2^{-10}$; $1 + 2^{-12}$ is closer to $1$, so $w$ stays $1$ after all ten steps. With an FP32 master copy, $w = 1 + 10 \cdot 2^{-12} = 1.00244140625$ exactly, and its FP16 copy is $1 + 2^{-9} = 1.001953125$, two FP16 ulps above the start.

**An underflowing gradient.** The gradient value $2^{-26}$ rounds to $0$ in FP16. With $S = 2^{10}$ it is $2^{-16}$, a subnormal that FP16 holds exactly, and $2^{-16}/S$ in FP32 gives back $2^{-26}$. In BF16, $2^{-26}$ is a normal number and needs no scale.

**Training that stalls without the master copy.** The implementation fits a linear model whose weights start at $(1, 1, 1)$ and whose target is $(1.01, 0.99, 1.005)$, with SGD, learning rate $0.01$ and 400 batches of 8. Every update is below half an FP16 ulp of $1$. With the weights in FP16 they never move. With FP32 master weights and FP16 passes they reach $(1.0093, 0.9908, 1.0044)$, against $(1.0093, 0.9907, 1.0047)$ for the same SGD run in double precision.

**Dynamic scaling at work.** With residuals of $40$, the FP16 gradient overflows at $S = 2^{16}$. The implementation skips seven steps, halving $S$ each time, until $S = 2^9 = 512$, where the scaled gradient $80 \cdot 512 = 40960$ fits under $65504$. The master weights do not change during the skipped steps.

**The paper's networks.** In the Multibox SSD detector, 67% of the activation gradient values were zero in FP16 (Figure 3); training diverged without scaling and matched FP32 with a scale of 8. The bigLSTM language model needed a scale of 128. In a Mandarin speech model about 5% of the weight gradients were below $2^{-24}$, and training with FP16 weight updates lost accuracy that the FP32 master copy restored.

## Variations

- **BF16 in place of FP16.** Same structure without the loss scale (Kalamkar and others, 2019). The update loss is worse, since the ulp at $1$ is $2^{-7}$, so the FP32 master copy matters even more.
- **FP32 accumulation.** Matrix products take 16 bit inputs and sum the products in FP32 (Section 3.3); large reductions such as the batch normalization statistics and the softmax also run in FP32. Mixed precision libraries keep lists of operations to run in each format.
- **No master copy.** Some systems keep 16 bit weights and add the updates with [stochastic rounding](/stochastic-rounding/), so that small updates are kept on average, or with a [compensated sum](/kahan-summation/) that stores the rounding error of each update.
- **Static or dynamic scale.** A fixed scale needs tuning per model; the dynamic rule finds a scale near the largest that does not overflow, at the cost of a skipped step now and then.
- **8 bit formats.** Later work trains with 8 bit floating point formats in matrix products, with a scale factor per tensor, on the same principle.
- **Memory of the optimizer.** The master weights and the optimizer state stay in FP32, so for an Adam run they dominate the memory of a large model; factored moments as in [Adafactor](/adafactor/) reduce that part.

## Pitfalls

- **Updating FP16 weights.** Without the master copy, updates below half an ulp are lost every step, and training slows or stops. This is a [rounding error](/rounding-error-analysis/) that does not average out, because round to nearest is deterministic.
- **Unscale before you use the gradient.** [Gradient clipping](/gradient-clipping/), gradient norms for logging and [weight decay](/weight-decay/) need the true gradient, so unscale first (L7). Clipping the scaled gradient clips at a threshold $S$ times too small.
- **Skipped steps and counters.** A skipped step is not an optimizer step: the [learning rate schedule](/learning-rate-schedule/) and momentum should not advance on it. A skip on every step means a NaN in the forward pass, not a too large scale.
- **Small constants in FP16.** Adam's $\epsilon = 10^{-8}$ is below $2^{-25}$ and rounds to $0$ in FP16. Keep optimizer arithmetic in FP32.
- **Overflow in the forward pass.** Large activations, a sum of many terms, or an exponential exceed $65504$; the loss scale does not help there, and those operations belong in FP32 (see [floating point exceptions](/floating-point-exceptions/)).
- **Accumulation buffers.** With [gradient accumulation](/gradient-accumulation/), add micro-batch gradients into an FP32 buffer; a 16 bit buffer loses the same small terms as a 16 bit weight. The [summation order](/floating-point-summation/) also changes the result in the last bits.

## Exercises

1. Show that in FP16 with round to nearest even, $1 + u$ rounds to $1$ for $0 \le u \le 2^{-11}$ and to $1 + 2^{-10}$ for $2^{-11} < u < 3 \cdot 2^{-11}$. What changes for $1 - u$?
2. Starting from $w = 1$ and adding $u = 2^{-12}$ at each step in FP32, after how many steps does the FP16 copy of $w$ first change? Compare with stochastic rounding of FP16 weights, where the expected FP16 value after $t$ steps is $1 + tu$.
3. Show that multiplying the loss by $S = 2^j$ and dividing the gradient by $S$ in FP32 gives the same gradient bit for bit when no value overflows and no value becomes subnormal.
4. With the dynamic rule of the template, $N = 2000$, and a true best scale of $2^{20}$ that never changes, how often is a step skipped in the long run?

## References
