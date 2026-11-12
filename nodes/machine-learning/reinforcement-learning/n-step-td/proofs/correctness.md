---
title: n-step TD has the error reduction property and matches the online loop, TD(0) and Monte Carlo
proves: [correctness, termination]
status: full
---

We use the notation of the page. Episodes are finite, $V(S_T) = 0$ for the terminal state, $0 \le \gamma \le 1$, and $n \ge 1$.

**Termination.** For an episode of $T$ steps, the loop of line L2 runs $T$ times and the sum of line L3 has at most $n$ terms. So the algorithm stops after $O(nT)$ operations per episode. $\square$

**Lemma 1 (the target of line L3 and L4).** In iteration $\tau$, after line L4, $G = G_{\tau:\tau+n}$ computed with the current table $V$.

*Proof.* If $\tau + n < T$, line L3 gives $\sum_{i=\tau+1}^{\tau+n} \gamma^{i-\tau-1} R_i = R_{\tau+1} + \cdots + \gamma^{n-1} R_{\tau+n}$, and line L4 adds $\gamma^n V(S_{\tau+n})$, which is the definition. If $\tau + n \ge T$, line L3 sums up to $R_T$, which is the full return $G_\tau$, and line L4 adds nothing. $\square$

**Lemma 2 (the online loop).** The online program of Sutton and Barto (Section 7.1) makes the same updates with the same values as the loop of line L2.

*Proof.* The online program, at each time $t = 0, 1, \ldots$, sets $\tau = t - n + 1$ and, if $\tau \ge 0$, updates $V(S_\tau)$ with $G_{\tau:\tau+n}$ computed from the table at that moment; it stops after the update for $\tau = T - 1$. So it updates $\tau = 0, 1, \ldots, T - 1$ in this order, one update per value of $\tau$. The rewards and states of the target are data of the episode and do not depend on when they are read. The only table entry in the target is $V(S_{\tau+n})$, read just before the update of $\tau$ and after the updates of $0, \ldots, \tau - 1$, in both programs. By induction on $\tau$, both programs hold the same table before the update of $\tau$, read the same target and write the same value. $\square$

**Lemma 3 (the end cases).** With $n = 1$, the updates are those of TD(0). With $n \ge T$, the updates are $V(S_\tau) \leftarrow V(S_\tau) + \alpha(G_\tau - V(S_\tau))$ for $\tau = 0, \ldots, T-1$ in order, which is incremental constant-$\alpha$ every-visit Monte Carlo.

*Proof.* For $n = 1$, Lemma 1 gives $G = R_{\tau+1} + \gamma V(S_{\tau+1})$ when $\tau + 1 < T$ and $G = R_T$ when $\tau = T - 1$; these are lines L3 and L4 of TD(0), with the same order of updates. For $n \ge T$, $\tau + n \ge T$ for every $\tau \ge 0$, so by Lemma 1 the target is always the full return. $\square$

**Theorem (error reduction property).** Let $V$ be any table with $V(\text{terminal}) = 0$. Then $\max_s |\mathbb{E}_\pi[G_{t:t+n} \mid S_t = s] - V^\pi(s)| \le \gamma^n \max_s |V(s) - V^\pi(s)|$.

*Proof.* Index the nonterminal states $1, \ldots, m$. Let $P_\pi(s, s') = \Pr(S_{t+1} = s' \mid S_t = s)$ for nonterminal $s, s'$, a matrix with nonnegative entries and row sums at most 1, and $r_\pi(s) = \mathbb{E}[R_{t+1} \mid S_t = s]$. Let $X_k = \mathbf{1}\{t + k < T\}$. After the terminal state the rewards are 0 and the bootstrap value is 0, so $G_{t:t+n} = \sum_{k=0}^{n-1} \gamma^k R_{t+k+1} X_k + \gamma^n V(S_{t+n}) X_n$, where a term with $X_k = 0$ is 0. By the Markov property, $\mathbb{E}[R_{t+k+1} X_k \mid S_t = s] = (P_\pi^k r_\pi)(s)$ and $\mathbb{E}[V(S_{t+n}) X_n \mid S_t = s] = (P_\pi^n V)(s)$. So

$$\mathbb{E}[G_{t:t+n} \mid S_t = \cdot] = \sum_{k=0}^{n-1} \gamma^k P_\pi^k r_\pi + \gamma^n P_\pi^n V.$$

The value vector satisfies $V^\pi = r_\pi + \gamma P_\pi V^\pi$. Substituting this identity into itself $n - 1$ times gives $V^\pi = \sum_{k=0}^{n-1} \gamma^k P_\pi^k r_\pi + \gamma^n P_\pi^n V^\pi$, by induction on $n$. Subtracting the two displays, the difference is $\gamma^n P_\pi^n (V - V^\pi)$. Row $s$ of $P_\pi^n$ has nonnegative entries with sum at most 1 (a product of such matrices has the same property), so $|(\gamma^n P_\pi^n (V - V^\pi))(s)| \le \gamma^n \max_{s'} |V(s') - V^\pi(s')|$. $\blacksquare$
