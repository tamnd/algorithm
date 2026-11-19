---
title: The LoRA layer equals the merged layer, its update has rank at most r and reaches every update of rank at most r, training starts at the pretrained layer, and the gradients of A and B are the full gradient projected through the factors
proves: [correctness]
status: full
---

We use the notation of the page. $W_0$ is $d \times k$, $B$ is $d \times r$, $A$ is $r \times k$, $x \in \mathbb{R}^k$, $s = \alpha / r$ and $r \ge 1$. The layer computes $h = W_0 x + s B (A x)$. We work in exact real arithmetic (the [real RAM](/real-ram/)); the last section says what changes in floating point.

## Claim 1: the factored layer and the merged layer agree

Let $W = W_0 + s B A$. Matrix multiplication is associative and distributes over addition, so

$$W x = W_0 x + s (B A) x = W_0 x + s B (A x) = h.$$

Lines L3 and L4 compute the right side, and line L9 computes $W$. So the merged layer and the factored layer give the same output for every $x$. Line L10 computes $W - s B A = W_0$, so unmerging returns the pretrained matrix exactly. Because the two forms agree for every input, they agree for every batch of $n$ tokens, and for every network that contains the layer.

## Claim 2: the update has rank at most r

The column space of $B A$ is contained in the column space of $B$, because $(B A) y = B (A y)$ for every $y$. The column space of $B$ is spanned by its $r$ columns, so it has dimension at most $r$. Hence $\operatorname{rank}(s B A) \le \operatorname{rank}(B A) \le \min(r, d, k)$, where the bound by $d$ and $k$ holds for every $d \times k$ matrix.

## Claim 3: every update of rank at most r is reachable

Let $\Delta$ be a $d \times k$ matrix of rank $q \le r$. By the [singular value decomposition](/singular-value-decomposition/), $\Delta = \sum_{i=1}^{q} \sigma_i u_i v_i^\top$. Put $P = [\sigma_1 u_1, \ldots, \sigma_q u_q, 0, \ldots, 0]$ ($d \times r$) and $Q = [v_1, \ldots, v_q, 0, \ldots, 0]^\top$ ($r \times k$), so $\Delta = P Q$. Then $B = P$ and $A = Q / s$ give $s B A = \Delta$. So the set of updates that LoRA of rank $r$ can express is exactly the set of $d \times k$ matrices of rank at most $r$. The factors are not unique: $B G$ and $G^{-1} A$ give the same product for every invertible $r \times r$ matrix $G$.

## Claim 4: training starts at the pretrained layer

Line L2 sets $B = 0$, so $s B A = 0$ and $h = W_0 x$ for every $x$, whatever the random $A$ of line L1. So before the first step the adapted network computes exactly the pretrained network.

## Claim 5: the gradients

Let $\ell$ be a differentiable loss of $h$, and let $g = \partial \ell / \partial h \in \mathbb{R}^d$. Write $u = A x$ and $c = B^\top g$. The output is $h_i = (W_0 x)_i + s \sum_{p} B_{ip} u_p$ with $u_p = \sum_j A_{pj} x_j$.

For $B$: $\partial h_i / \partial B_{ip} = s u_p$, and $h_{i'}$ for $i' \ne i$ does not depend on $B_{ip}$. By the chain rule $\partial \ell / \partial B_{ip} = g_i s u_p$, so $\nabla_B \ell = s\, g u^\top$. This is line L6.

For $A$: $\partial h_i / \partial A_{pj} = s B_{ip} x_j$. So $\partial \ell / \partial A_{pj} = s \sum_i g_i B_{ip} x_j = s\, c_p x_j$, and $\nabla_A \ell = s\, c x^\top = s B^\top g x^\top$. This is line L7.

For $x$: $\partial h_i / \partial x_j = (W_0)_{ij} + s (B A)_{ij}$. So $\nabla_x \ell = W_0^\top g + s A^\top B^\top g = W_0^\top g + s A^\top c$. This is line L8.

The full fine-tuning gradient of the same loss with respect to an update $\Delta$ (with $h = (W_0 + \Delta) x$) is $G = g x^\top$. The two formulas above say $\nabla_B \ell = s\, G A^\top$ and $\nabla_A \ell = s B^\top G$: the LoRA gradients are the full gradient multiplied by the other factor. For a batch of $n$ tokens the loss is a sum over tokens, so each gradient is the sum of the per-token gradients.

## Claim 6: the start is not a stationary point, but A = B = 0 is

At the start $B = 0$, so $c = B^\top g = 0$ and $\nabla_A \ell = 0$, while $\nabla_B \ell = s\, g (A x)^\top$, which is non-zero when $g \ne 0$ and $A x \ne 0$. A random Gaussian $A$ has $A x \ne 0$ for $x \ne 0$ with probability 1. So the first step changes $B$ only, and from the second step on $A$ also moves. If both $A$ and $B$ start at zero, then $u = 0$ and $c = 0$, both gradients are zero for every loss, and gradient descent never leaves the start. This is why one factor must be random.

## Floating point

In floating point the factored form and the merged form round in different places, so they agree only up to rounding. Each entry of $W x$ and of $W_0 x + s B (A x)$ is a sum of $O(k + r)$ products, so the two differ by $O((k + r)\, u)$ times the size of the terms, with $u$ the unit roundoff; the tests use a tolerance of $10^{-12}$ on entries of size about 1. Unmerging after merging returns $W_0$ up to one rounding per entry, and merging in a lower precision than $W_0$ (for example in 16-bit floats) loses more.
