---
title: The hand-written backward pass of GRU4Rec is the gradient of the ranking loss, and the session-parallel batches visit every event once
proves: [correctness]
status: full
---

The notation is that of the page. A sequence has inputs $x_1, \dots, x_T$, targets $y_1, \dots, y_T$, negative lists $N_1, \dots, N_T$ and a fixed start state $h_0$. For $t = 1, \dots, T$,

$$a^z_t = W_z[x_t] + U_z h_{t-1}, \quad a^r_t = W_r[x_t] + U_r h_{t-1}, \quad z_t = \sigma(a^z_t), \quad r_t = \sigma(a^r_t),$$

$$a^h_t = W_h[x_t] + U_h (r_t \odot h_{t-1}), \quad \hat h_t = \tanh(a^h_t), \quad h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \hat h_t,$$

the scores are $\rho_{t,k} = O[k]^\top h_t + c_k$ for $k \in \{y_t\} \cup N_t$, and the loss is $\mathcal L = \sum_t \ell(\rho_t)$ with $\ell$ the BPR or the TOP1 loss of the page. Every function in the chain ($\sigma$, $\tanh$, products, sums, $\ln \sigma$) is smooth, so $\mathcal L$ is a smooth function of all the parameters and the chain rule applies everywhere.

**Lemma 1 (the losses).** With $i$ the target, $N_S = |N_t|$ and $\sigma' = \sigma (1 - \sigma)$:

- BPR, $\ell = -\frac{1}{N_S} \sum_j \ln \sigma(\rho_i - \rho_j)$: $\partial \ell / \partial \rho_i = -\frac{1}{N_S} \sum_j \sigma(\rho_j - \rho_i)$ and $\partial \ell / \partial \rho_j = \frac{1}{N_S} \sigma(\rho_j - \rho_i)$.
- TOP1, $\ell = \frac{1}{N_S} \sum_j \sigma(\rho_j - \rho_i) + \sigma(\rho_j^2)$: $\partial \ell / \partial \rho_i = -\frac{1}{N_S} \sum_j \sigma'(\rho_j - \rho_i)$ and $\partial \ell / \partial \rho_j = \frac{1}{N_S} \bigl(\sigma'(\rho_j - \rho_i) + 2 \rho_j \sigma'(\rho_j^2)\bigr)$.

*Proof.* $\frac{d}{dx} \ln \sigma(x) = 1 - \sigma(x) = \sigma(-x)$, so $\frac{\partial}{\partial \rho_i} \bigl(-\ln \sigma(\rho_i - \rho_j)\bigr) = -\sigma(\rho_j - \rho_i)$ and the derivative in $\rho_j$ is the negative of that. For TOP1, $\sigma(\rho_j - \rho_i)$ has derivative $-\sigma'$ in $\rho_i$ and $\sigma'$ in $\rho_j$, and $\sigma(\rho_j^2)$ has derivative $2 \rho_j \sigma'(\rho_j^2)$ in $\rho_j$. The code computes these. A negative list that contains $j$ twice is a sum, which the code also handles, since it adds. $\square$

**Lemma 2 (the output layer).** Let $\delta_{t,k} = \partial \ell(\rho_t) / \partial \rho_{t,k}$. Then $\partial \ell(\rho_t) / \partial O[k] = \delta_{t,k} h_t$, $\partial \ell(\rho_t) / \partial c_k = \delta_{t,k}$, and $\partial \ell(\rho_t) / \partial h_t = \sum_k \delta_{t,k} O[k]$.

*Proof.* $\rho_{t,k}$ is bilinear in $O[k]$ and $h_t$ and linear in $c_k$. $\square$

**Lemma 3 (one GRU step backward).** Let $g_t = \partial \mathcal L / \partial h_t$, the total derivative through all later steps and the output of step $t$. Then, entry by entry,

$$\bar{\hat h} = g_t \odot z_t, \qquad \bar z = g_t \odot (\hat h_t - h_{t-1}), \qquad \bar a^h = \bar{\hat h} \odot (1 - \hat h_t^2),$$

$$\bar u = U_h^\top \bar a^h, \qquad \bar r = \bar u \odot h_{t-1}, \qquad \bar a^z = \bar z \odot z_t \odot (1 - z_t), \qquad \bar a^r = \bar r \odot r_t \odot (1 - r_t),$$

the gradient contributions of step $t$ are $\bar a^h (r_t \odot h_{t-1})^\top$ to $U_h$, $\bar a^z h_{t-1}^\top$ to $U_z$, $\bar a^r h_{t-1}^\top$ to $U_r$, and $\bar a^h, \bar a^z, \bar a^r$ to the rows $W_h[x_t], W_z[x_t], W_r[x_t]$, and

$$\frac{\partial \mathcal L}{\partial h_{t-1}}\Big|_{\text{through step } t} = g_t \odot (1 - z_t) + \bar u \odot r_t + U_z^\top \bar a^z + U_r^\top \bar a^r.$$

*Proof.* $h_t$ depends on $h_{t-1}$ directly (through $(1 - z_t) \odot h_{t-1}$), and through $z_t$, $r_t$ and $\hat h_t$. The direct path gives $g_t \odot (1 - z_t)$. The product rule on $h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \hat h_t$ gives $\partial h_t / \partial z_t = \mathrm{diag}(\hat h_t - h_{t-1})$ and $\partial h_t / \partial \hat h_t = \mathrm{diag}(z_t)$, so $\bar z$ and $\bar{\hat h}$ are as stated. $\tanh' = 1 - \tanh^2$ and $\sigma' = \sigma(1 - \sigma)$ give $\bar a^h$, $\bar a^z$, $\bar a^r$. The argument $u = r_t \odot h_{t-1}$ enters $a^h_t$ through $U_h$, so $\partial \mathcal L / \partial u = U_h^\top \bar a^h = \bar u$, and $u$ passes $\bar u \odot h_{t-1}$ to $r_t$ and $\bar u \odot r_t$ to $h_{t-1}$. The pre-activations $a^z_t$ and $a^r_t$ pass $U_z^\top \bar a^z$ and $U_r^\top \bar a^r$ to $h_{t-1}$. Each pre-activation $a = W[x_t] + U v$ has $\partial a_k / \partial U_{kq} = v_q$ and $\partial a_k / \partial W[x_t]_k = 1$, and no other row of $W$ appears, because the input is one-hot. $\square$

**Theorem 4 (the backward pass is the gradient).** `sequence_loss_and_grad` returns $\mathcal L$ and its exact gradient in every parameter.

*Proof.* The loop runs $t = T, T - 1, \dots, 1$ and keeps `dh_next`, which on entry to step $t$ holds $\partial \mathcal L / \partial h_t$ through the steps after $t$ (zero for $t = T$, since no later step exists). It adds $\sum_k \delta_{t,k} O[k]$ (Lemma 2, with $\delta$ from Lemma 1), so `dh` is $g_t$, the full derivative: $h_t$ affects $\mathcal L$ only through $\ell(\rho_t)$ and through step $t + 1$. It then adds the contributions of Lemma 3 and sets `dh_next` to $\partial \mathcal L / \partial h_{t-1}$ through step $t$, which is everything after $t - 1$ except the output at $t - 1$; that output is added at the next iteration. By induction from $t = T$ downward the invariant holds at every step. Each parameter is shared across steps, and its gradient is the sum of the contributions of all steps, which is what the code adds. $h_0$ is a constant and gets no gradient. $\square$

The tests compare every entry of this gradient with a central finite difference for both losses on a sequence of four steps with a nonzero $h_0$.

**Proposition 5 (session-parallel batches).** `session_parallel_batches(sessions, X)` returns batches in which (a) each session of length $\ell \ge 2$ contributes exactly the $\ell - 1$ events $(s_t, s_{t+1})$, $t = 1, \dots, \ell - 1$, in order, (b) the reset flag is true exactly at $t = 1$, (c) no batch has more than $X$ events or two events of one session, and (d) sessions shorter than 2 contribute nothing.

*Proof.* Each lane holds at most one session and a position in it. A lane at position $t$ emits $(s_t, s_{t+1})$ with the flag $t = 1$, then moves to $t + 1$ if $s_{t+2}$ exists, and otherwise takes the next session from the queue at position 1 or goes idle. So a lane emits the events of one session in order, from the first to the last, and then moves on, which gives (a) and (b) for each session it takes. The queue holds each session of length at least 2 once and is read in order, so each such session is taken by exactly one lane, and the loop runs until all lanes are idle, so every taken session is finished. Each batch takes at most one event per lane, which gives (c). Sessions shorter than 2 are not in the queue, which gives (d). $\square$

**A training step.** In `train`, a lane carries its hidden state from one batch to the next and resets it to 0 at the start of a session, as in Section 3.1.1 of the paper. The gradient of a batch is the exact gradient of the sum of the one-step losses with each carried state treated as a constant (Theorem 4 with $T = 1$). That is the gradient of the full loss with backpropagation cut at the step boundary, not the full gradient through the session. The page states this choice. This page does not prove that the steps converge, or that the model ranks well; ranking quality is measured. $\blacksquare$
