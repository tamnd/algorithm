---
title: Offline TD(lambda) with accumulating traces makes the same total update as the lambda-return algorithm
proves: [correctness, termination]
status: full
---

We use the notation of the page. An episode is $(S_0, R_1), \ldots, (S_{T-1}, R_T)$ with $T \ge 1$, $V(S_T) = 0$ for the terminal state, $0 \le \gamma \le 1$ and $0 \le \lambda \le 1$, with $0^0 = 1$. In the offline mode, $V$ does not change during the episode, so $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ uses one fixed table.

**Termination.** The loop of line L3 runs $T$ times per episode, and lines L5 to L7 touch at most the states with a nonzero trace, a finite set of at most $T$ states. Line L8 touches the same set. So each episode takes $O(T^2)$ operations at most, and the algorithm stops after a finite list of finite episodes. $\square$

**Lemma 1 (the recursion of the λ-return).** For $0 \le t < T$, $G^\lambda_t = R_{t+1} + \gamma\big((1 - \lambda) V(S_{t+1}) + \lambda G^\lambda_{t+1}\big)$, with $G^\lambda_T = 0$ and $V(S_T) = 0$.

*Proof.* For $t = T - 1$ the sum in the definition is empty, so $G^\lambda_{T-1} = \lambda^0 G_{T-1} = R_T$, and the right side is $R_T + \gamma((1-\lambda) \cdot 0 + \lambda \cdot 0) = R_T$. For $t < T - 1$, use $G_{t:t+1} = R_{t+1} + \gamma V(S_{t+1})$, $G_{t:t+n} = R_{t+1} + \gamma G_{t+1:t+n}$ for $n \ge 2$ (both windows bootstrap from $V(S_{t+n})$, since $t + n < T$), and $G_t = R_{t+1} + \gamma G_{t+1}$. Then

$$G^\lambda_t = (1-\lambda) G_{t:t+1} + (1-\lambda)\sum_{n=2}^{T-t-1} \lambda^{n-1} G_{t:t+n} + \lambda^{T-t-1} G_t .$$

The weights $(1-\lambda)\sum_{n=1}^{T-t-1}\lambda^{n-1} + \lambda^{T-t-1}$ sum to 1, so $R_{t+1}$ appears with weight 1. The remaining terms are $\gamma(1-\lambda) V(S_{t+1})$ and $\gamma \lambda \big[(1-\lambda)\sum_{m=1}^{T-t-2} \lambda^{m-1} G_{t+1:t+1+m} + \lambda^{T-t-2} G_{t+1}\big]$ with $m = n - 1$, and the bracket is $G^\lambda_{t+1}$. $\square$

**Lemma 2 (λ-return error as a sum of TD errors).** For $0 \le t < T$, $G^\lambda_t - V(S_t) = \sum_{k=t}^{T-1} (\gamma\lambda)^{k-t} \delta_k$.

*Proof.* By backward induction on $t$. For $t = T - 1$, $G^\lambda_{T-1} - V(S_{T-1}) = R_T - V(S_{T-1}) = \delta_{T-1}$. For $t < T - 1$, Lemma 1 gives

$$G^\lambda_t - V(S_t) = \big(R_{t+1} + \gamma V(S_{t+1}) - V(S_t)\big) + \gamma\lambda\big(G^\lambda_{t+1} - V(S_{t+1})\big) = \delta_t + \gamma\lambda \sum_{k=t+1}^{T-1} (\gamma\lambda)^{k-t-1}\delta_k ,$$

which is the claim. $\square$

**Lemma 3 (the trace).** After line L5 at time $t$, $z_t(s) = \sum_{k=0}^{t} (\gamma\lambda)^{t-k} \mathbf{1}\{S_k = s\}$ for every state $s$.

*Proof.* By induction on $t$. Line L2 sets $z = 0$. If the claim holds at $t - 1$ (or $z = 0$ before $t = 0$), line L5 sets $z_t(s) = \gamma\lambda z_{t-1}(s) + \mathbf{1}\{S_t = s\} = \sum_{k=0}^{t-1} (\gamma\lambda)^{t-k}\mathbf{1}\{S_k = s\} + \mathbf{1}\{S_t = s\}$. $\square$

**Theorem (offline equivalence).** In the offline mode, at line L8 of an episode, $\Delta(s) = \alpha\sum_{k=0}^{T-1} \mathbf{1}\{S_k = s\}\big(G^\lambda_k - V(S_k)\big)$ for every state $s$. So offline TD(λ) and the offline λ-return algorithm leave the same table after each episode.

*Proof.* Lines L6 and L7 add $\alpha\delta_t z_t(s)$ to $\Delta(s)$ for each $s$ with $z_t(s) \ne 0$, and adding the other states would add 0. So, with Lemma 3,

$$\Delta(s) = \alpha\sum_{t=0}^{T-1} \delta_t \sum_{k=0}^{t} (\gamma\lambda)^{t-k}\mathbf{1}\{S_k = s\} = \alpha\sum_{k=0}^{T-1} \mathbf{1}\{S_k = s\}\sum_{t=k}^{T-1} (\gamma\lambda)^{t-k}\delta_t ,$$

by exchanging two finite sums over the pairs $0 \le k \le t \le T - 1$. By Lemma 2 the inner sum is $G^\lambda_k - V(S_k)$. The offline λ-return algorithm adds exactly this amount to $V(s)$ at the end of the episode, with the same table $V$ in the targets. Both start the next episode from the same table, so by induction on the episodes they agree after every episode. $\square$

**Corollary (the end cases).** With $\lambda = 0$, the trace is $z_t(s) = \mathbf{1}\{S_t = s\}$ (with $0^0 = 1$), so line L7 of the online mode is the TD(0) update $V(S_t) \leftarrow V(S_t) + \alpha\delta_t$ with the current table. With $\lambda = 1$ in the offline mode, $G^1_k = G_k$, so the theorem gives the total update $\alpha\sum_k \mathbf{1}\{S_k = s\}(G_k - V(S_k))$ of offline every-visit constant-$\alpha$ Monte Carlo. $\blacksquare$
