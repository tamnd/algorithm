---
title: Policy iteration terminates with an optimal policy and dominates value iteration
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite and $0 \le \gamma < 1$. Vectors are indexed by states, $U \le W$ means $U(s) \le W(s)$ for every $s$, and $\lVert U \rVert = \max_s |U(s)|$. For a deterministic policy $\pi$ let $(T^\pi U)(s) = R(s, \pi(s)) + \gamma \sum_{s'} P(s' \mid s, \pi(s))\, U(s')$ and $(TU)(s) = \max_a [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, U(s')]$.

We use these facts.

1. $T^\pi$ and $T$ are monotone: if $U \le W$ then $T^\pi U \le T^\pi W$ and $TU \le TW$, because the probabilities are nonnegative and $\gamma \ge 0$.
2. $T^\pi U \le TU$ for every $\pi$ and $U$, and $T^\pi U = TU$ if $\pi$ is greedy for $U$.
3. $V^\pi$ is the unique fixed point of $T^\pi$, and $(T^\pi)^k U \to V^\pi$ for every $U$ ([Bellman expectation equation](/bellman-expectation-equation/); $T^\pi$ is a $\gamma$-contraction).
4. $V^*$ is the unique fixed point of $T$, and $V^\pi \le V^*$ for every $\pi$ ([Bellman contraction](/bellman-contraction/)).

**Lemma 1 (exact evaluation).** Line L3 sets $V = V^\pi$.

*Proof.* The equation $(I - \gamma P_\pi)V = r_\pi$ is $V = T^\pi V$. Each row of $\gamma P_\pi$ has nonnegative entries that sum to $\gamma < 1$, so $I - \gamma P_\pi$ is strictly diagonally dominant by rows and invertible. The unique solution is the unique fixed point of $T^\pi$, which is $V^\pi$ by fact 3. $\square$

**Lemma 2 (improvement).** Let $\pi$ be the policy at line L3 of some iteration and $\pi'$ the policy after line L7. Then $V^{\pi'} \ge T V^\pi \ge V^\pi$. If $\pi' \ne \pi$, then $V^{\pi'} \ne V^\pi$.

*Proof.* Line L6 picks a maximizer in each state, so $\pi'$ is greedy for $V = V^\pi$ and $T^{\pi'}V^\pi = TV^\pi \ge T^\pi V^\pi = V^\pi$ by fact 2. Apply the monotone map $T^{\pi'}$ $k$ times: $(T^{\pi'})^{k+1}V^\pi \ge (T^{\pi'})^k V^\pi$, so the sequence $(T^{\pi'})^k V^\pi$ never decreases. Its limit is $V^{\pi'}$ by fact 3, so $V^{\pi'} \ge T^{\pi'}V^\pi = TV^\pi \ge V^\pi$.

If $\pi' \ne \pi$, there is a state $s$ with $\pi'(s) \ne \pi(s)$. By line L6, $\pi(s)$ is not a maximizer at $s$, so $(TV^\pi)(s) > (T^\pi V^\pi)(s) = V^\pi(s)$, and $V^{\pi'}(s) \ge (TV^\pi)(s) > V^\pi(s)$. $\square$

This is the [policy improvement theorem](/policy-improvement-theorem/) applied to a greedy policy.

**Lemma 3 (termination).** The loop of lines L2 to L8 stops after at most $|A|^{|S|}$ iterations.

*Proof.* Let $\pi_0, \pi_1, \ldots$ be the policies evaluated in successive iterations. While the loop runs, $\pi_{j+1} \ne \pi_j$, so Lemma 2 gives $V^{\pi_{j+1}} \ge V^{\pi_j}$ and $V^{\pi_{j+1}} \ne V^{\pi_j}$. The relation is a strict partial order, so the values $V^{\pi_0}, V^{\pi_1}, \ldots$ are pairwise distinct and so are the policies. There are $|A|^{|S|}$ deterministic policies, and the last iteration evaluates a policy that does not change. $\square$

**Theorem.** POLICY-ITERATION returns an optimal policy $\pi$ and $V = V^\pi = V^*$.

*Proof.* By Lemma 3 the loop stops. In the last iteration no state changed, so the evaluated policy $\pi$ is greedy for $V = V^\pi$ (Lemma 1), and by fact 2, $TV^\pi = T^\pi V^\pi = V^\pi$. So $V^\pi$ is a fixed point of $T$, and by fact 4, $V^\pi = V^*$. Line L9 returns $\pi$ and $V^\pi$. $\blacksquare$

**Proposition (domination of value iteration).** With $\pi_0, \pi_1, \ldots$ as above, $T^j V^{\pi_0} \le V^{\pi_j} \le V^*$ for every $j$ for which $\pi_j$ is defined. So $\lVert V^* - V^{\pi_j} \rVert \le \lVert V^* - T^j V^{\pi_0} \rVert \le \gamma^j \lVert V^* - V^{\pi_0} \rVert$.

*Proof.* The upper bound is fact 4. For the lower bound use induction on $j$. For $j = 0$ it is equality. If $T^j V^{\pi_0} \le V^{\pi_j}$, then Lemma 2 and fact 1 give $V^{\pi_{j+1}} \ge TV^{\pi_j} \ge T(T^j V^{\pi_0}) = T^{j+1}V^{\pi_0}$. The norm bound follows from $0 \le V^* - V^{\pi_j} \le V^* - T^j V^{\pi_0}$ and the contraction of $T$, since $V^* = T^j V^*$. $\square$
