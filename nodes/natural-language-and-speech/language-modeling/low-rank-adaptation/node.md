---
tag: W05XMM
kind: algorithm
slug: low-rank-adaptation
name: Low-rank adaptation
aliases:
- LoRA
area: natural-language-and-speech/language-modeling
level: research
summary: "Fine-tune a large model by freezing a weight matrix W0 and training a rank-r update B A, scaled by alpha / r and zero at the start. The update merges into W0, so inference costs nothing extra."
model: real-ram
complexity:
  vars: {d: the output size of the adapted matrix, k: the input size of the adapted matrix, r: the rank of the update, n: the number of tokens}
  time: {worst: "Θ(n (d k + r (d + k)))"}
  space: {extra: "Θ(r (d + k))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2021
  people: [Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen]
  note: Hu and colleagues at Microsoft proposed LoRA in 2021 (ICLR 2022). They built on measurements that fine-tuning has a low intrinsic dimension, and applied it to the attention matrices of GPT-3 175B.
prereqs: [transformer, rank, gradient-descent]
see_also: [singular-value-decomposition, multi-head-attention, instruction-tuning, adamw, mixed-precision-training, knowledge-distillation, backpropagation, generative-pretrained-transformer]
sources:
  - url: https://arxiv.org/abs/2106.09685
    title: "Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang and Weizhu Chen, LoRA: Low-rank adaptation of large language models, ICLR 2022"
    locator: "Section 4.1 (equation 3, the Gaussian A and zero B, the scale alpha / r, merging with no extra latency), Section 4.2 (W_q and W_v, the VRAM and checkpoint savings on GPT-3 175B), Table 4 (GPT-3 175B results), Section 7.1 and Table 5 (which matrices), Section 7.2 and Table 6 (the rank r)"
  - url: https://arxiv.org/abs/2012.13255
    title: "Armen Aghajanyan, Sonal Gupta and Luke Zettlemoyer, Intrinsic dimensionality explains the effectiveness of language model fine-tuning, ACL-IJCNLP 2021"
    locator: the measurements of the intrinsic dimension of fine-tuning, which motivate the low-rank hypothesis
  - url: https://arxiv.org/abs/1902.00751
    title: "Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe, Andrea Gesmundo, Mona Attariyan and Sylvain Gelly, Parameter-efficient transfer learning for NLP, ICML 2019"
    locator: the adapter layers, the earlier parameter-efficient method that adds inference latency
  - url: https://arxiv.org/abs/2305.14314
    title: "Tim Dettmers, Artidoro Pagnoni, Ari Holtzman and Luke Zettlemoyer, QLoRA: Efficient finetuning of quantized LLMs, NeurIPS 2023"
    locator: LoRA on top of a frozen 4-bit quantized base model
---

Low-rank adaptation (LoRA) fine-tunes a large pretrained network without changing its weights. For a chosen weight matrix $W_0$ of shape $d \times k$, it freezes $W_0$ and trains two small matrices $B$ ($d \times r$) and $A$ ($r \times k$) with a rank $r$ much smaller than $d$ and $k$. The layer computes $h = W_0 x + (\alpha / r) B A x$. $B$ starts at zero, so training starts exactly at the pretrained network. After training, $(\alpha / r) B A$ can be added into $W_0$, so the adapted network runs at the same cost as the original one. LoRA is a way to parametrize fine-tuning: it says which numbers are trained, not what data they are trained on. [Instruction tuning](/instruction-tuning/), the reward model of [RLHF](/reinforcement-learning-from-human-feedback/) and [direct preference optimization](/direct-preference-optimization/) are often run with LoRA, and they are separate pages.

## In plain words

A large model has big tables of numbers. Changing all of them for every new task needs a lot of memory, and each task gets a full copy of the model.

LoRA keeps the big tables fixed. Next to one table it puts two thin tables. Their product has the same shape as the big table, but it can describe only a few independent directions of change. Only the thin tables learn.

At the start one thin table is all zeros, so the model behaves exactly as before. During training the thin tables learn the change that the task needs.

When training ends, you can add the product of the thin tables into the big table once. The model is then as fast as before. You can also keep the thin tables apart and swap them to change the task.

## The problem

The input is a pretrained matrix $W_0 \in \mathbb{R}^{d \times k}$ that maps an input $x \in \mathbb{R}^k$ to $W_0 x \in \mathbb{R}^d$, for example the query projection $W_q$ of an attention layer, with $d = k = d_{\text{model}}$. Full fine-tuning learns an update $\Delta$ of the same shape, so $d k$ new numbers per matrix, plus the optimizer state for each of them. LoRA restricts the update to the form

$$\Delta = s B A, \qquad B \in \mathbb{R}^{d \times r}, \quad A \in \mathbb{R}^{r \times k}, \quad s = \frac{\alpha}{r}, \quad r \ll \min(d, k),$$

so it trains $r (d + k)$ numbers. The hypothesis of Hu and colleagues is that the change that a downstream task needs has a low "intrinsic rank". That is a measured observation on their tasks, not a theorem: Section 7.2 of their paper reports that $r = 1$ already does well on WikiSQL and MultiNLI for GPT-3 175B when both $W_q$ and $W_v$ are adapted, and they say that they do not expect a small $r$ to work for every task. The scale $\alpha$ is a constant; Hu and colleagues set $\alpha$ to the first $r$ they try and do not tune it, so that changing $r$ later needs less retuning of the learning rate.

For a sequence of $n$ tokens, $X$ is $n \times k$ and the output is $H = X W_0^\top + s (X A^\top) B^\top$, of shape $n \times d$.

## The algorithm

The algorithm has an initialization, a forward pass, a backward pass that gives the gradients of $A$ and $B$ (and of the input, for the layers below), and the merge and unmerge steps. $W_0$ is never changed during training. The optimizer (for example [AdamW](/adamw/)) updates $A$ and $B$ with the gradients of lines L6 and L7.

```pseudo id=main
LORA-INIT(d, k, r, σ)
L1  A ← r × k matrix with entries drawn from N(0, σ^2)
L2  B ← d × r zero matrix
LORA-FORWARD(W0, A, B, α, x)                ▷ x: k numbers, s = α / r
L3  u ← A x                                 ▷ r numbers
L4  return h ← W0 x + s B u                 ▷ d numbers, B A is never formed
LORA-BACKWARD(W0, A, B, α, x, g)            ▷ g = ∂ℓ/∂h: d numbers
L5  u ← A x;  c ← B^T g                     ▷ r numbers each
L6  ∇B ← s g u^T                            ▷ d × r
L7  ∇A ← s c x^T                            ▷ r × k
L8  ∇x ← W0^T g + s A^T c                   ▷ k numbers
LORA-MERGE(W0, A, B, α)
L9  return W ← W0 + s B A
LORA-UNMERGE(W, A, B, α)
L10 return W0 ← W - s B A
```

For a batch of $n$ tokens the gradients of $A$ and $B$ are the sums of lines L6 and L7 over the tokens.

## Example

Take $d = 2$, $k = 3$, $r = 1$ and $\alpha = 2$, so $s = 2$, with

$$W_0 = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 1 & -1 \end{pmatrix}, \quad A = \begin{pmatrix} 1 & 2 & 0 \end{pmatrix}, \quad B = \begin{pmatrix} 0.5 \\ -1 \end{pmatrix}, \quad x = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}.$$

| step | value |
|---|---|
| L3 $u = A x$ | 3 |
| $W_0 x$ | (3, 0) |
| $s B u$ | (3, -6) |
| L4 $h$ | (6, -6) |
| L9 $s B A$ | rows (1, 2, 0) and (-2, -4, 0) |
| L9 $W$ | rows (2, 2, 2) and (-2, -3, -1) |
| $W x$ | (6, -6), the same as L4 |

The update $s B A$ has rank 1, as both of its rows are multiples of $A$. With $B = 0$ (line L2) the same input gives $h = W_0 x = (3, 0)$, the pretrained output.

At scale, take GPT-3 175B, which has 96 layers and $d_{\text{model}} = 12288$. One $12288 \times 12288$ matrix has 150,994,944 entries. LoRA with $r = 4$ on that matrix trains $4 \times (12288 + 12288) = 98{,}304$ numbers. Adapting $W_q$ and $W_v$ in all 96 layers trains $96 \times 2 \times r \times 24576$ numbers: 4,718,592 for $r = 1$ and 37,748,736 for $r = 8$. These are the "4.7M" and "37.7M" budgets of Table 4 of Hu and colleagues.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md). Associativity gives $W_0 x + s B (A x) = (W_0 + s B A) x$, so the merged layer of line L9 computes the same function as lines L3 and L4, and line L10 recovers $W_0$. The column space of $B A$ lies in the span of the $r$ columns of $B$, so the update has rank at most $r$; conversely, the [singular value decomposition](/singular-value-decomposition/) of any update of rank at most $r$ gives factors $B$ and $A$ that reach it. Line L2 makes the update zero, so the first forward pass equals the pretrained one. The chain rule gives lines L6 to L8: if $G = g x^\top$ is the gradient of full fine-tuning with respect to $\Delta$, then $\nabla_B = s G A^\top$ and $\nabla_A = s B^\top G$. At the start $B = 0$, so $\nabla_A = 0$ and only $B$ moves in the first step.

## Complexity

The cost is counted in the [real RAM](/real-ram/), per token. Line L3 costs $\Theta(r k)$, line L4 costs $\Theta(d k)$ for $W_0 x$ and $\Theta(d r)$ for $B u$, so the forward pass costs $\Theta(d k + r (d + k))$, against $\Theta(d k)$ for the frozen layer alone. Lines L5 to L8 cost the same order. Over $n$ tokens the time is $\Theta(n (d k + r (d + k)))$. The merged layer costs $\Theta(d k)$, the same as the original. Merging costs $\Theta(d k r)$ once.

The saving is in memory, not in arithmetic. The trained parameters, their gradients and their optimizer state take $\Theta(r (d + k))$ numbers instead of $\Theta(d k)$. The activations of the frozen network must still be stored for the backward pass, so the activation memory is about the same as in full fine-tuning. Hu and colleagues measured on GPT-3 175B a drop of the training VRAM from 1.2 TB to 350 GB, a checkpoint of 35 MB instead of 350 GB for $r = 4$ on $W_q$ and $W_v$, and a 25% higher training throughput (Section 4.2); these are measurements on their hardware.

## Properties

- **No inference cost after merging (theorem).** The merged matrix has the shape of $W_0$, so the merged network has the same cost and the same outputs as the factored one, up to rounding.
- **Starts at the pretrained network (theorem).** With $B = 0$ the output is $W_0 x$ for every input.
- **Rank bound (theorem).** The update has rank at most $r$, and every update of rank at most $r$ is reachable.
- **Not unique.** $(B G, G^{-1} A)$ gives the same update as $(B, A)$ for every invertible $r \times r$ matrix $G$. The loss surface in $(A, B)$ is not convex even when the loss is convex in $\Delta$.
- **Task switching.** Many tasks can share one copy of $W_0$ and keep only their own $A$ and $B$. Unmerge one update and merge another to switch.
- **Full rank recovers full fine-tuning.** With $r = \min(d, k)$, every update is reachable, as in full fine-tuning of that matrix, although the training dynamics differ.

## Variants and improvements

- **Which matrices.** Hu and colleagues adapt only the attention projections and freeze the feed-forward layers. Under a fixed budget of 18M parameters on GPT-3 175B, adapting both $W_q$ and $W_v$ with $r = 4$ did better than one matrix with $r = 8$ (Table 5). Later work, QLoRA among it, adapts every linear layer of the block.
- **QLoRA** (Dettmers and colleagues 2023) stores the frozen $W_0$ in a 4-bit format and trains LoRA factors in higher precision, which lowers the memory further.
- **Adapters** (Houlsby and colleagues 2019) insert small bottleneck layers in series with each block. They also train few parameters, but they add layers that run at inference time, so they add latency that LoRA avoids after merging.
- **The scale.** Hu and colleagues report that with Adam, tuning $\alpha$ is roughly the same as tuning the learning rate if the initialization is scaled to match (Section 4.1). The form $\alpha / r$ is a heuristic choice, not a derived value, and other scales have been proposed.
- **Compression view.** A rank-$r$ approximation of an already trained full update, by the truncated [singular value decomposition](/singular-value-decomposition/), is the best rank-$r$ approximation in the Frobenius norm (Eckart and Young 1936). LoRA does not compute that; it trains the factors directly.

## When to use it

Use LoRA when the full set of weights plus their optimizer state does not fit in memory, or when many fine-tuned versions of one large model must be stored or served. Use full fine-tuning when memory allows and the task is far from the pretraining data, because a low-rank update can underfit there; Hu and colleagues warn that a small $r$ need not work for every task. When the model is small, the saving matters less.

## Pitfalls

- **Both factors at zero.** If line L1 also sets $A = 0$, then $u = 0$ and $c = 0$, both gradients are zero, and training never moves. One factor must be random. If $A$ is zero and $B$ random, the roles swap.
- **Forgetting the scale.** Merging $W_0 + B A$ without $s = \alpha / r$ gives a different network from the one that was trained. Use the same $s$ in lines L4, L9 and L10.
- **Merging in low precision.** Merging into a 16-bit or quantized $W_0$ rounds the update. Small updates can vanish under the rounding of large weights. Merge in a higher precision, or keep the factors apart.
- **Changing $r$ and keeping the learning rate.** The scale $\alpha / r$ is meant to reduce retuning when $r$ changes, but the best learning rate still depends on $r$ and on the optimizer. Tune it on held out data.
- **Expecting less compute per step.** The backward pass still runs through every frozen layer, so the time per step drops much less than the memory.
- **Batching different tasks.** If each input of a batch uses a different adapter, the merged form cannot serve them together. Keep the factored form for such batches.

## Implementations

The code implements one adapted layer: the initialization, the forward pass, the gradients of lines L6 to L8, the merge and the unmerge, and a gradient step on a small squared loss. It takes $W_0$ and the data as given; it does not train a large network and does not load pretrained weights. The tests check the rank-$r$ layer against the full update $W_0 + s B A$ of the same product, the merged layer against the unmerged one, the rank bound with exact rational elimination, the gradients against central finite differences with $h = 10^{-6}$ and a tolerance of $10^{-5}$, and a fit of a planted rank-2 change.

## History

Aghajanyan, Gupta and Zettlemoyer (2021) measured that fine-tuning a pretrained language model in a random subspace of small dimension recovers most of the result of full fine-tuning. Earlier parameter-efficient methods trained adapter layers (Houlsby and colleagues 2019), prompts or prefixes. Hu and colleagues (2021, published at ICLR 2022) proposed to train a low-rank update of the existing weight matrices instead, with $B$ at zero and $A$ random, and showed that it can be merged into the weights. On GPT-3 175B they reported, in Table 4, a WikiSQL accuracy of 73.4 with 4.7M trained parameters and 74.0 with 37.7M, against 73.8 for full fine-tuning, and a MultiNLI-matched accuracy of 91.7 and 91.6 against 89.5. These are measurements on their setup. LoRA then became a common way to fine-tune large open models, often with a quantized base model (QLoRA, 2023).

## References
