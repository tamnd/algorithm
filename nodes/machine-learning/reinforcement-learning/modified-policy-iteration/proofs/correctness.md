---
title: Modified policy iteration converges and returns an eps-optimal policy
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, $0 < \gamma < 1$, $\varepsilon > 0$, and $\lVert U \rVert = \max_s |U(s)|$. We write $U \le W$ if $U(s) \le W(s)$ for every $s$, and $\mathbf{1}$ for the vector of ones. We use these facts about the operators $T^\pi$ and $T$ of the page.

1. Both are monotone: $U \le W$ implies $T^\pi U \le T^\pi W$ and $TU \le TW$.
2. Both are $\gamma$-contractions in the max norm. $V^\pi$ is the fixed point of $T^\pi$ and $V^*$ is the fixed point of $T$ ([Bellman contraction](/bellman-contraction/)). Also $V^\pi \le V^*$.
3. $T^\pi U \le TU$, with equality when $\pi$ is greedy for $U$.
4. For a constant $c$, $T^\pi(U + c\mathbf{1}) = T^\pi U + \gamma c \mathbf{1}$ and $T(U + c\mathbf{1}) = TU + \gamma c\mathbf{1}$. A policy is greedy for $U + c\mathbf{1}$ if and only if it is greedy for $U$.

One iteration that does not stop maps $V$ to $\Phi(V) = (T^\pi)^{m+1}V$, where $\pi$ is the greedy policy of line L3. For $m = \infty$, $\Phi(V) = V^\pi$. Lines L4 and L9 to L10 compute exactly this, since $U = T^\pi V$ after line L4.

**Lemma 1 (one step from an improvable vector).** If $TV \ge V$ and $W = \Phi(V)$, then $TV \le W \le V^*$ and $TW \ge W$.

*Proof.* Let $\pi$ be greedy for $V$. Then $T^\pi V = TV \ge V$ by fact 3. Applying the monotone $T^\pi$ $j$ times gives $(T^\pi)^{j+1}V \ge (T^\pi)^j V$, so the sequence $(T^\pi)^j V$ never decreases. It converges to $V^\pi$ by fact 2. So $TV = T^\pi V \le (T^\pi)^{m+1}V \le V^\pi \le V^*$, which covers finite and infinite $m$. Finally $TW \ge T^\pi W = (T^\pi)^{m+2}V \ge (T^\pi)^{m+1}V = W$ for finite $m$, and $TW \ge T^\pi V^\pi = V^\pi = W$ for $m = \infty$. $\square$

**Lemma 2 (sandwich).** If $TV_0 \ge V_0$ and $V_k = \Phi(V_{k-1})$, then $T^k V_0 \le V_k \le V^*$ and $\lVert V_k - V^* \rVert \le \gamma^k \lVert V_0 - V^* \rVert$.

*Proof.* By Lemma 1 every $V_k$ is improvable and $V_k \le V^*$. Induction: $V_k \ge TV_{k-1} \ge T(T^{k-1}V_0)$ by Lemma 1 and fact 1. Then $0 \le V^* - V_k \le V^* - T^k V_0 = T^k V^* - T^k V_0$, whose norm is at most $\gamma^k \lVert V^* - V_0 \rVert$ by fact 2. $\square$

**Lemma 3 (any start).** For any $V_0$, the iterates $V_k = \Phi(V_{k-1})$ converge to $V^*$.

*Proof.* Let $c = \max(0, \max_s (V_0(s) - (TV_0)(s)))/(1 - \gamma)$ and $W_0 = V_0 - c\mathbf{1}$. By fact 4, $TW_0 = TV_0 - \gamma c\mathbf{1} \ge V_0 - (1-\gamma)c\mathbf{1} - \gamma c \mathbf{1} = W_0$, so $W_0$ is improvable. By fact 4 the greedy policies for $V_0$ and $W_0$ are the same, and $\Phi(W_0) = \Phi(V_0) - \gamma^{m+1}c\mathbf{1}$ for finite $m$, while $\Phi(W_0) = \Phi(V_0)$ for $m = \infty$. By induction $W_k = V_k - \gamma^{k(m+1)}c\mathbf{1}$ (or $W_k = V_k$ for $k \ge 1$ when $m = \infty$), where $W_k = \Phi(W_{k-1})$. So $\lVert V_k - V^* \rVert \le \lVert W_k - V^* \rVert + \gamma^{k(m+1)}c \le \gamma^k \lVert W_0 - V^* \rVert + \gamma^k c$ by Lemma 2, and this tends to 0. The tie rule of line L3, which keeps the old action, picks the same action in both runs, because the two runs see the same sets of maximizers. $\square$

**Lemma 4 (termination).** The loop stops after finitely many iterations.

*Proof.* At iteration $k$ line L5 compares $\delta_k = \lVert TV_{k-1} - V_{k-1} \rVert$ with $\tau = \varepsilon(1-\gamma)/(2\gamma) > 0$. Since $TV^* = V^*$, $\delta_k \le \lVert TV_{k-1} - TV^* \rVert + \lVert V^* - V_{k-1} \rVert \le (1 + \gamma)\lVert V_{k-1} - V^* \rVert$, which tends to 0 by Lemma 3. So $\delta_k < \tau$ for some finite $k$. $\square$

**Theorem.** MODIFIED-POLICY-ITERATION stops, and its output $(U, \pi)$ satisfies $\lVert U - V^* \rVert < \varepsilon/2$ and $V^\pi(s) > V^*(s) - \varepsilon$ for each state $s$.

*Proof.* By Lemma 4 the loop stops at line L6 with $V$ and $U = TV$ such that $\delta = \lVert U - V \rVert < \tau$.

Value error: $\lVert U - V^* \rVert = \lVert TV - TV^* \rVert \le \gamma \lVert V - V^* \rVert \le \gamma(\delta + \lVert U - V^* \rVert)$, so $\lVert U - V^* \rVert \le \frac{\gamma}{1-\gamma}\delta < \varepsilon/2$.

Policy error: $\pi$ is greedy for $U$, so $T^\pi U = TU$ and $V^\pi - U = (T^\pi V^\pi - T^\pi U) + (TU - TV)$. The norms of the two terms are at most $\gamma\lVert V^\pi - U \rVert$ and $\gamma\delta$. So $\lVert V^\pi - U \rVert \le \frac{\gamma}{1-\gamma}\delta < \varepsilon/2$.

By the triangle inequality, $\lVert V^\pi - V^* \rVert < \varepsilon$. $\blacksquare$

**The two limits.** For $m = 0$, $\Phi(V) = T^\pi V = TV$, so the iterates are those of value iteration with the same stopping test. For $m = \infty$, $\Phi(V) = V^\pi$ with $\pi$ greedy for $V$ and the old action kept on ties. From the second iteration on, $V = V^{\pi_{\text{old}}}$, so line L3 is the improvement step of policy iteration, and the sequence of evaluated policies is the sequence of policy iteration. When the policy is stable, $TV = V$ and line L5 stops at the next iteration.
