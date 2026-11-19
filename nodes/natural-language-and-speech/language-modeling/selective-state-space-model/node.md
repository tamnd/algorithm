---
tag: FBSQEB
kind: model
slug: selective-state-space-model
name: Selective state space model
aliases:
- Mamba
area: natural-language-and-speech/language-modeling
level: research
summary: "A linear recurrent layer whose state matrices depend on the input, computed by a parallel scan in time linear in sequence length."
history:
  year: 2023
  people: [Albert Gu, Tri Dao]
  note: Introduced the selection mechanism (S6) on top of the structured state space layers of Gu and colleagues, with a scan kernel for GPUs and the Mamba block. Published at COLM 2024.
prereqs: [state-space-model, parallel-prefix]
see_also: [transformer, recurrent-neural-network-language-model, hidden-markov-model, kalman-filter, convolution, causal-language-modeling, flashattention, key-value-cache]
sources:
  - paper: "Albert Gu and Tri Dao, Mamba: linear-time sequence modeling with selective state spaces, Conference on Language Modeling (COLM) 2024, arXiv:2312.00752"
    title: Gu and Dao 2024
    locator: "Section 2 (equations 1 to 4, zero-order hold, linear time invariance), Section 3.1 (selection as compression), Section 3.2 (Algorithms 1 and 2, s_B, s_C, s_Delta, softplus), Section 3.3.2 (the hardware-aware scan), Section 3.4 (the block), Section 3.5.1 (Theorem 1), Section 3.6 (real diagonal A), Sections 4.1.1 and 4.1.2 (selective copying, induction heads), Sections 4.2 and 4.5 (language modeling, speed)"
  - paper: "Albert Gu, Karan Goel and Christopher Ré, Efficiently modeling long sequences with structured state spaces, ICLR 2022, arXiv:2111.00396"
    title: Gu, Goel and Ré 2022
    locator: the S4 layer, a linear time-invariant state space model computed as a long convolution
  - paper: "Guy E. Blelloch, Prefix sums and their applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990"
    title: Blelloch 1990
    locator: the work-efficient parallel scan for an associative operator, and its use for first-order linear recurrences
---

A selective state space model is a sequence layer that runs a linear recurrence $h_t = \bar A_t h_{t-1} + \bar B_t x_t$, $y_t = C_t h_t$ over the input, where the matrices $\bar A_t$, $\bar B_t$ and $C_t$ are computed from the current input $x_t$. Earlier structured [state space models](/state-space-model/) such as S4 use the same matrices at every step, which lets them run as one long [convolution](/convolution/) but stops them from choosing what to keep: they cannot ignore a filler token or reset on a boundary. Gu and Dao made the step size $\Delta$ and the maps $B$ and $C$ functions of the input (the S6 layer), gave up the convolution, and computed the recurrence with a [parallel prefix](/parallel-prefix/) scan in a fused GPU kernel. The cost is linear in the sequence length, and generation keeps a state of fixed size instead of a growing [key-value cache](/key-value-cache/). Their Mamba network stacks blocks built around this layer, with no attention.

## The machine

**Continuous system.** For one input channel $x(t)$ with a state $h(t) \in \mathbb{R}^N$,

$$h'(t) = A\, h(t) + B\, x(t), \qquad y(t) = C\, h(t),$$

with $A \in \mathbb{R}^{N \times N}$, $B \in \mathbb{R}^{N \times 1}$ and $C \in \mathbb{R}^{1 \times N}$ (equation 1).

**Discretization.** With a step size $\Delta > 0$, the zero-order hold gives

$$\bar A = \exp(\Delta A), \qquad \bar B = (\Delta A)^{-1}(\exp(\Delta A) - I)\, \Delta B$$

(equation 4), and the discrete recurrence $h_t = \bar A h_{t-1} + \bar B x_t$, $y_t = C h_t$ (equation 2). $A$ is diagonal with real entries $a_1, \ldots, a_N < 0$ by default, so $\bar A = \mathrm{diag}(e^{\Delta a_n})$ and $\bar B_n = (e^{\Delta a_n} - 1)\, b_n / a_n$. The reference code uses the simpler $\bar B = \Delta B$ for the input map.

**Time-invariant case (S4).** If $\Delta$, $A$, $B$ and $C$ are the same at every step, unrolling the recurrence from $h_0 = 0$ gives $y = x * \bar K$ with the kernel $\bar K = (C \bar B,\; C \bar A \bar B,\; C \bar A^2 \bar B, \ldots)$ (equation 3), which can be computed with the [fast Fourier transform](/fast-fourier-transform/).

**Selection (S6).** The input is $x \in \mathbb{R}^{L \times D}$ ($L$ steps, $D$ channels). Each channel $c$ has its own diagonal $A^{(c)}$ with $N$ entries. At each step,

$$B_t = \mathrm{Linear}_N(x_t), \qquad C_t = \mathrm{Linear}_N(x_t), \qquad \Delta_t = \mathrm{softplus}\big(p + \mathrm{Broadcast}_D(\mathrm{Linear}_1(x_t))\big),$$

so $B_t, C_t \in \mathbb{R}^N$ are shared by the channels and $\Delta_t \in \mathbb{R}^D$ has one step per channel ($p$ is a learned vector; the rank-1 map can be widened to rank $R$). Then for each channel $c$ and state entry $n$,

$$h_{t,c,n} = e^{\Delta_{t,c}\, a^{(c)}_n}\, h_{t-1,c,n} + \bar B_{t,c,n}\, x_{t,c}, \qquad y_{t,c} = \sum_{n=1}^{N} C_{t,n}\, h_{t,c,n}.$$

Because the matrices change with $t$, there is no fixed kernel, and the layer is computed as a recurrence only (Algorithm 2).

**The scan.** Each step is the affine map $h \mapsto \alpha_t h + \beta_t$, with $\alpha_t = \bar A_t$ and $\beta_t = \bar B_t x_t$ entrywise. Composing step $s$ and then step $t$ gives $(\alpha_t \alpha_s,\; \alpha_t \beta_s + \beta_t)$, an associative operation, so all states $h_1, \ldots, h_L$ are the prefix results of a [parallel prefix](/parallel-prefix/) scan: $\Theta(L)$ work and $\Theta(\log L)$ depth.

**Hardware-aware kernel.** The expanded state has $B L D N$ numbers for a batch of $B$ sequences. The kernel loads $\Delta$, $A$, $B$, $C$ and $x$ from the GPU main memory into on-chip memory, does the discretization, the scan and the product with $C$ there, and writes back only $y$, of size $B L D$. In the backward pass the states are computed again instead of stored, as [FlashAttention](/flashattention/) does with the attention matrix.

**The block.** The Mamba block widens the channels with a linear map, applies a short causal convolution, a nonlinearity and the selective SSM, multiplies the result by a gated branch of the input, and maps back to $D$ channels. Blocks are stacked with normalization and residual connections, and a language model puts a softmax over the vocabulary on top, trained by [causal language modeling](/causal-language-modeling/).

## What it counts

For a batch of $B$ sequences of length $L$ with $D$ channels and state size $N$ per channel:

- **Training time.** The scan does $\Theta(B L D N)$ work. The projections that make $B_t$, $C_t$ and $\Delta_t$ and the linear maps of the block add $\Theta(B L D^2)$. There is no term in $L^2$.
- **Training memory.** With the fused kernel, the main memory holds $\Theta(B L D)$ numbers per layer, not the $\Theta(B L D N)$ expanded state, which lives only in on-chip memory.
- **Generation.** Each new token costs $\Theta(D N + D^2)$ per layer and needs only the state $h_t$, of $D N$ numbers per layer (plus a few inputs for the short convolution), whatever the number of tokens seen. A [transformer](/transformer/) with a [key-value cache](/key-value-cache/) stores $2 t d$ numbers per layer after $t$ tokens and spends $\Theta(t d)$ per token on attention.
- **Depth.** With a parallel scan the layer has $\Theta(\log L)$ sequential depth; run step by step, it has $L$ steps.
- **The time-invariant case.** An S4 layer with a fixed kernel costs $\Theta(L \log L)$ per channel by FFT; the selective layer cannot use this route.

## Relation to other models

- **[State space models](/state-space-model/) and the [Kalman filter](/kalman-filter/).** The same linear state equation, but here it is deterministic, discretized from continuous time, and learned as a layer of a network, not a model of noisy observations.
- **Structured SSMs (S4 and its diagonal forms).** These are the time-invariant special case: $\Delta$, $B$ and $C$ do not depend on the input. Selection gives up the convolution form for the ability to act on content.
- **Gated recurrent networks.** With one state entry, $A = -1$ and $B = 1$, the selective recurrence is the gate $h_t = (1 - g_t) h_{t-1} + g_t x_t$ of a gated [recurrent network](/recurrent-neural-network-language-model/) with $g_t = \sigma(\mathrm{Linear}(x_t))$ (Theorem 1 below). Unlike an LSTM or GRU, the state update is linear in $h$, which is what allows the scan.
- **[Transformers](/transformer/).** Attention keeps every past key and value and can look any of them up exactly, at $\Theta(L^2)$ cost in training and a cache that grows with $t$. A selective SSM compresses the past into a fixed-size state, at linear cost; Section 3.1 of Gu and Dao frames this as the trade-off between efficiency and the size of the state.
- **[Hidden Markov models](/hidden-markov-model/).** The forward algorithm of an HMM is also a linear recurrence in a state vector whose matrix depends on the current input, $\alpha_t = \mathrm{diag}(b(x_t))\, T^\top \alpha_{t-1}$, and can be computed with the same kind of scan.

## Known results in the model

- **Scan correctness (theorem).** The operation $(\alpha_2, \beta_2) \circ (\alpha_1, \beta_1) = (\alpha_2 \alpha_1,\; \alpha_2 \beta_1 + \beta_2)$ is associative, and the $t$-th prefix result applied to $h_0$ gives $h_t$. So any parallel prefix algorithm computes the same states as the sequential loop, in exact arithmetic.
- **Gating as a special case (theorem).** Theorem 1 of Gu and Dao: with $N = 1$, $A = -1$, $B = 1$, $\Delta_t = \mathrm{softplus}(z_t)$ and $z_t = \mathrm{Linear}(x_t)$, the zero-order hold gives $\bar A_t = e^{-\Delta_t} = 1/(1 + e^{z_t}) = 1 - \sigma(z_t)$ and $\bar B_t = 1 - e^{-\Delta_t} = \sigma(z_t)$, so $h_t = (1 - g_t) h_{t-1} + g_t x_t$ with $g_t = \sigma(z_t)$. A large $\Delta_t$ resets the state to the current input; a small one keeps the state and ignores the input.
- **Stability (theorem).** If every $a_n < 0$ and $\Delta_t > 0$, then $0 < e^{\Delta_t a_n} < 1$, so the state cannot grow without bound when the inputs are bounded.
- **Selective copying (measurement).** On the task of copying tokens placed at random gaps among filler tokens, a time-invariant S4 layer reached 18.3% accuracy and the selective S6 layer 97.0%; the full Mamba network with S6 reached 99.8% (Section 4.1.1).
- **Induction heads (measurement).** Trained on sequences of 256 tokens, the Mamba network solved the induction-head task on test sequences up to $2^{20}$ tokens, about 4000 times longer; the other methods tested did not go beyond about twice the training length (Section 4.1.2).
- **Language modeling (measurement).** Gu and Dao report that their 3B-parameter Mamba model beats transformers of the same size and matches transformers twice its size, in pre-training perplexity and downstream tasks, with 4 to 5 times higher generation throughput than a transformer of similar size (Sections 4.2 and 4.5).

## References
