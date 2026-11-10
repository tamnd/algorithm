---
title: Chain sampling returns a uniform item of the window at every step
proves: [correctness]
status: full
---

Fix the window size $W \ge 1$ and any stream $\sigma_1, \sigma_2, \ldots$. Write $S_t$ for the index $C[0].\mathit{index}$ of the sample after step $t$.

**The random choices.** Give each step $u$ a coin $K_u$ uniform on $\{1, \ldots, \min(u, W)\}$ and an offset $D_u$ uniform on $\{1, \ldots, W\}$, all independent. Line L6 of step $u$ uses $K_u$. Lines L3 and L7 of step $u$ set $\mathit{want} \leftarrow u + D_u$; both refer to item $u$, and when both run in one step only the value of line L7 is kept. Drawing a fresh value at each call, as the code does, gives a run with the same distribution, because each value is used at most once and is independent of all earlier values.

**Lemma 1 (chain shape).** After every step $t \ge 1$, the chain is $c_0 < c_1 < \cdots < c_k$ with $c_0 = S_t$, $c_{j+1} = c_j + D_{c_j}$ for $j < k$, $c_k \le t$, and $\mathit{want} = c_k + D_{c_k} > t$. Each element holds the item $\sigma_{c_j}$, and $t - W < c_0$.

*Proof.* By induction on $t$. At $t = 1$ the chain is empty before the step, line L4 does not apply, the coin of line L6 has range $\{1\}$ and wins, and line L7 makes the chain $(1)$ with $\mathit{want} = 1 + D_1 > 1$. Assume the claim after step $t - 1$. If $t = \mathit{want}$, line L3 appends $c_{k+1} = t = c_k + D_{c_k}$ and sets $\mathit{want} = t + D_t > t$; otherwise $\mathit{want} > t$ already, since $\mathit{want} > t - 1$ and $\mathit{want} \ne t$. Either way, the chain now satisfies the shape with $c_k \le t < \mathit{want}$. If $c_0 = t - W$, line L5 removes $c_0$. Then $c_1$ exists: if the chain had only $c_0$, then $\mathit{want} = c_0 + D_{c_0} \le c_0 + W = t$, which contradicts $\mathit{want} > t$. The new first element is $c_1 > t - W$. If $c_0 \ne t - W$, then $c_0 > t - W$ since $c_0 > (t - 1) - W$. If line L7 runs, the chain becomes $(t)$ with $\mathit{want} = t + D_t$. In all cases the claim holds after step $t$. $\square$

**Lemma 2 (transitions).** For $t \ge 2$: if $S_{t-1} = t - W$, then $S_t = S_{t-1} + D_{S_{t-1}}$. Otherwise $S_t = t$ if $K_t = 1$, and $S_t = S_{t-1}$ if $K_t \ne 1$.

*Proof.* Line L4 tests $C[0].\mathit{index} = S_{t-1} = t - W$; line L3 only appends at the end. In the first case line L5 runs, and by Lemma 1 the new first element is $c_1 = S_{t-1} + D_{S_{t-1}}$. In the second case line L6 tests $K_t = 1$, and line L7 makes $t$ the sample, or nothing changes the first element. $\square$

**Lemma 3 (what the past depends on).** For every $t \ge 1$, the sequence $S_1, \ldots, S_t$ is a function of $K_1, \ldots, K_t$ and of $D_u$ for $u \le t - W$ only.

*Proof.* By induction on $t$. $S_1 = 1$. By Lemma 2, $S_t$ is a function of $S_{t-1}$, $K_t$ and, only when $S_{t-1} = t - W$, of $D_{t-W}$. With the claim for $t - 1$, which uses $D_u$ for $u \le t - 1 - W$, the claim for $t$ follows. $\square$

**Theorem.** For every $t \ge 1$ and every index $s$ with $\max(1, t - W + 1) \le s \le t$, $\Pr[S_t = s] = 1/\min(t, W)$. So $\mathrm{SAMPLE}()$ returns $\sigma_{S_t}$, an item of the window at a uniformly random position.

*Proof.* By induction on $t$. For $t = 1$, $S_1 = 1$ with probability $1$.

*Case $2 \le t \le W$.* Then $S_{t-1} \ge 1 > t - W$, so by Lemma 2 $S_t = t$ when $K_t = 1$ and $S_t = S_{t-1}$ otherwise. $K_t$ is independent of $S_{t-1}$ by Lemma 3, and $\Pr[K_t = 1] = 1/t$. So $\Pr[S_t = t] = 1/t$, and for $s < t$, $\Pr[S_t = s] = \Pr[S_{t-1} = s](1 - 1/t) = \frac{1}{t-1} \cdot \frac{t-1}{t} = \frac{1}{t}$.

*Case $t > W$.* Then $\min(t - 1, W) = W$, so by the induction hypothesis $S_{t-1}$ is uniform on $t - W, \ldots, t - 1$. Let $X$ be the event $S_{t-1} = t - W$, with $\Pr[X] = 1/W$. By Lemma 3, $X$ and $S_{t-1}$ are functions of $K_1, \ldots, K_{t-1}$ and $D_u$ for $u \le t - 1 - W$, so both $D_{t-W}$ and $K_t$ are independent of $S_{t-1}$. On $X$, $S_t = t - W + D_{t-W}$ is uniform on $t - W + 1, \ldots, t$. Off $X$, $S_t = t$ when $K_t = 1$, with probability $1/W$, and $S_t = S_{t-1}$ otherwise. For $t - W < u < t$:

$$\Pr[S_t = u] = \Pr[X] \cdot \frac{1}{W} + \Pr[S_{t-1} = u] \cdot \Bigl(1 - \frac{1}{W}\Bigr) = \frac{1}{W^2} + \frac{W - 1}{W^2} = \frac{1}{W}.$$

For $u = t$:

$$\Pr[S_t = t] = \Pr[X] \cdot \frac{1}{W} + \Pr[\text{not } X] \cdot \frac{1}{W} = \frac{1}{W}.$$

The probabilities over the $W$ indices of the window sum to 1, so no other index has positive probability. Finally, no line of the algorithm reads an item to make a choice, so the distribution of $S_t$ is the same for every stream, and by Lemma 1 the sample holds $\sigma_{S_t}$. $\blacksquare$

**The biased order.** If the coin of line L6 were also tossed after line L5, with offsets still on $1, \ldots, W$, then for $W = 2$ at step 3: $S_2$ is uniform on $\{1, 2\}$; if $S_2 = 1$, it expires, the successor is 2 or 3 with probability $1/2$ each, and then item 3 wins with probability $1/2$; if $S_2 = 2$, item 3 wins with probability $1/2$. So $\Pr[S_3 = 3] = \frac12(\frac12 + \frac12 \cdot \frac12) + \frac12 \cdot \frac12 = \frac58$, not $\frac12$.
