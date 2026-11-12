---
title: The Viterbi algorithm returns a most likely state path, chosen by the tie rule
proves: [correctness]
status: full
---

Fix the model $\lambda = (\pi, A, B)$ and $O = o_1 \ldots o_T$ with $T \ge 1$. For a partial path $q_1 \ldots q_t$ define its log weight

$$W_t(q_1, \ldots, q_t) = \log \pi_{q_1} + \log B_{q_1}(o_1) + \sum_{s=2}^{t} \bigl( \log A_{q_{s-1} q_s} + \log B_{q_s}(o_s) \bigr),$$

with $\log 0 = -\infty$ and $-\infty + x = -\infty$. By the product form of the HMM joint, $W_T(Q) = \log P(Q, O)$. The weights satisfy

$$W_t(q_1, \ldots, q_t) = W_{t-1}(q_1, \ldots, q_{t-1}) + \log A_{q_{t-1} q_t} + \log B_{q_t}(o_t). \tag{1}$$

**Lemma 1.** After line L1 and after the pass of line L2 for each $t \ge 2$, $\delta_t(j) = \max \{ W_t(q_1, \ldots, q_t) : q_t = j \}$ for every state $j$.

*Proof.* By induction on $t$. For $t = 1$ the only path with $q_1 = j$ is $(j)$, and line L1 sets $\delta_1(j) = W_1(j)$.

Let $t \ge 2$ and assume the claim for $t - 1$. Every path with $q_t = j$ has some $q_{t-1} = i$. By (1) and because adding a constant keeps the order,

$$\max_{q_t = j} W_t = \max_i \Bigl( \max_{q_{t-1} = i} W_{t-1} + \log A_{ij} \Bigr) + \log B_j(o_t) = \max_i \bigl( \delta_{t-1}(i) + \log A_{ij} \bigr) + \log B_j(o_t),$$

where the last step is the induction hypothesis. Line L4 picks a maximizer $\psi_t(j)$ of the inner term and line L5 adds $\log B_j(o_t)$, so $\delta_t(j)$ equals the right side. $\square$

**Lemma 2.** For each $t \ge 2$ and each state $j$ there is a path with $q_t = j$ and $q_{t-1} = \psi_t(j)$ whose weight $W_t$ is $\delta_t(j)$.

*Proof.* Take $i = \psi_t(j)$ and a path $q_1 \ldots q_{t-1}$ with $q_{t-1} = i$ and $W_{t-1} = \delta_{t-1}(i)$, which exists by Lemma 1 (the maximum is over a finite non-empty set). Append $j$. By (1) its weight is $\delta_{t-1}(i) + \log A_{ij} + \log B_j(o_t) = \delta_t(j)$. $\square$

**Theorem 1 (optimality).** Assume $P(O) > 0$. VITERBI returns a path $Q^*$ with $W_T(Q^*) = \max_Q W_T(Q)$, and the returned score is this maximum.

*Proof.* By Lemma 1, $\max_j \delta_T(j) = \max_Q W_T(Q)$, which is finite because some path has $P(Q, O) > 0$. Line L6 picks $q_T$ with $\delta_T(q_T)$ equal to this maximum. We show by induction on $k = T, T-1, \ldots, 1$ that the traced states satisfy

> **(S)** $\sum_{s=k+1}^{T} \bigl( \log A_{q_{s-1} q_s} + \log B_{q_s}(o_s) \bigr) + \delta_k(q_k) = \delta_T(q_T)$.

For $k = T$ the sum is empty. Assume (S) for $k \ge 2$. Line L7 sets $q_{k-1} = \psi_k(q_k)$, so by line L5, $\delta_k(q_k) = \delta_{k-1}(q_{k-1}) + \log A_{q_{k-1} q_k} + \log B_{q_k}(o_k)$, which gives (S) for $k - 1$. With $k = 1$, (S) and line L1 say $W_T(q_1, \ldots, q_T) = \delta_T(q_T)$. $\square$

**Theorem 2 (the tie rule).** Assume $P(O) > 0$, and that lines L4 and L6 take the smallest maximizer. Let $\mathcal{O}$ be the set of optimal paths. The returned path is the element of $\mathcal{O}$ whose reversed sequence $(q_T, \ldots, q_1)$ is the smallest in lexicographic order.

*Proof.* Let $M = \max_Q W_T(Q)$, which is finite. Let $Q^\circ = (q^\circ_1, \ldots, q^\circ_T)$ be the target path. We show $q_k = q^\circ_k$ by induction on $k$ from $T$ down to 1.

For $k = T$: a state $j$ is the last state of some optimal path if and only if $\delta_T(j) = M$, by Lemma 1. The smallest such $j$ is $q^\circ_T$, by the definition of the order, and line L6 picks the smallest maximizer of $\delta_T$, so $q_T = q^\circ_T$.

For the step, assume $q_s = q^\circ_s$ for all $s \ge k$, with $k \ge 2$, and let $S = (q^\circ_k, \ldots, q^\circ_T)$. The optimal paths with the suffix $S$ are not empty, since $Q^\circ$ is one. For a path with suffix $S$ and $q_{k-1} = i$, equation (1) applied from $k$ to $T$ gives

$$W_T = W_{k-1}(q_1, \ldots, q_{k-2}, i) + \log A_{i q^\circ_k} + C, \qquad C = \log B_{q^\circ_k}(o_k) + \sum_{s=k+1}^{T} \bigl( \log A_{q^\circ_{s-1} q^\circ_s} + \log B_{q^\circ_s}(o_s) \bigr).$$

$C$ does not depend on $i$ or on the prefix, and $C$ is finite because $Q^\circ$ has weight $M > -\infty$. So, by Lemma 1, the largest weight of a path with suffix $S$ and $q_{k-1} = i$ is $\delta_{k-1}(i) + \log A_{i q^\circ_k} + C$. The paths of $\mathcal{O}$ with suffix $S$ are those whose $q_{k-1}$ maximizes $\delta_{k-1}(i) + \log A_{i q^\circ_k}$ and whose prefix is optimal for that $i$. Among them, the reversed order compares $q_{k-1}$ next, so $q^\circ_{k-1}$ is the smallest maximizer of $\delta_{k-1}(i) + \log A_{i q^\circ_k}$. That is $\psi_k(q^\circ_k)$ by line L4, and line L7 sets $q_{k-1} = \psi_k(q_k) = \psi_k(q^\circ_k)$. $\square$

**Termination and the case $P(O) = 0$.** All loops have fixed ranges, so the algorithm stops after $\Theta(T N^2)$ steps. If $P(O) = 0$, every path has weight $-\infty$, so $\max_j \delta_T(j) = -\infty$ by Lemma 1, and the implementation reports that no path has positive probability. $\blacksquare$
