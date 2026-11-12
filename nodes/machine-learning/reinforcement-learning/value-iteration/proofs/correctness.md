---
title: Value iteration converges and returns an eps-optimal policy
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, $0 < \gamma < 1$, and $\lVert U \rVert = \max_s |U(s)|$. For a deterministic policy $\pi$ let

$$(T^\pi U)(s) = R(s, \pi(s)) + \gamma \sum_{s'} P(s' \mid s, \pi(s))\, U(s'), \qquad (TU)(s) = \max_a \Big[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, U(s')\Big].$$

We use three facts.

1. $T$ is a $\gamma$-contraction in the max norm and $V^*$ is its unique fixed point. This is proved on the [Bellman contraction](/bellman-contraction/) page.
2. $T^\pi$ is a $\gamma$-contraction. For each $s$, $|(T^\pi U)(s) - (T^\pi W)(s)| = \gamma |\sum_{s'} P(s' \mid s, \pi(s))(U(s') - W(s'))| \le \gamma \sum_{s'} P(s' \mid s, \pi(s)) \lVert U - W \rVert = \gamma \lVert U - W \rVert$, since the probabilities sum to 1. Its unique fixed point is $V^\pi$, by the [Bellman expectation equation](/bellman-expectation-equation/).
3. If $\pi$ is greedy for $U$, then $T^\pi U = TU$. This is the definition of greedy.

**Lemma 1 (geometric convergence).** Let $V_k$ be the vector after $k$ executions of lines L3 to L6. Then $V_k = T^k V_0$ and $\lVert V_k - V^* \rVert \le \gamma^k \lVert V_0 - V^* \rVert$.

*Proof.* Lines L3 and L4 read only $V$ and write only $V'$, so after line L6, $V = TV_{k-1}$. By induction $V_k = T^k V_0$. By fact 1, $\lVert V_k - V^* \rVert = \lVert TV_{k-1} - TV^* \rVert \le \gamma \lVert V_{k-1} - V^* \rVert$, and induction on $k$ gives the claim. $\square$

**Lemma 2 (termination).** If $\varepsilon > 0$, the loop of lines L2 to L7 stops after finitely many sweeps.

*Proof.* The change of sweep $k$ is $\delta_k = \lVert V_k - V_{k-1} \rVert \le \lVert V_k - V^* \rVert + \lVert V_{k-1} - V^* \rVert \le 2\gamma^{k-1} D$ with $D = \lVert V_0 - V^* \rVert$, by Lemma 1. The threshold $\tau = \varepsilon(1-\gamma)/(2\gamma)$ is positive. If $D = 0$ then $\delta_1 = 0 < \tau$. Otherwise $2\gamma^{k-1} D < \tau$ as soon as $k > 1 + \ln(2D/\tau)/\ln(1/\gamma)$, a finite number, because $\gamma^{k-1}$ falls by the fixed factor $\gamma < 1$ at each sweep. $\square$

**Lemma 3 (value error at the stop).** If $\delta_k = \lVert V_k - V_{k-1} \rVert$, then $\lVert V_k - V^* \rVert \le \frac{\gamma}{1-\gamma}\delta_k$.

*Proof.* $\lVert V_k - V^* \rVert = \lVert TV_{k-1} - TV^* \rVert \le \gamma \lVert V_{k-1} - V^* \rVert \le \gamma(\lVert V_{k-1} - V_k \rVert + \lVert V_k - V^* \rVert)$. Move the last term to the left side and divide by $1 - \gamma > 0$. $\square$

**Lemma 4 (policy error at the stop).** If $\pi$ is greedy for $V_k$, then $\lVert V^\pi - V_k \rVert \le \frac{\gamma}{1-\gamma}\delta_k$.

*Proof.* By facts 2 and 3, $V^\pi - V_k = (T^\pi V^\pi - T^\pi V_k) + (T V_k - T V_{k-1})$. The first term has norm at most $\gamma \lVert V^\pi - V_k \rVert$ by fact 2, and the second at most $\gamma \delta_k$ by fact 1. So $\lVert V^\pi - V_k \rVert \le \gamma \lVert V^\pi - V_k \rVert + \gamma\delta_k$, and we solve for $\lVert V^\pi - V_k \rVert$. $\square$

**Theorem.** If $\varepsilon > 0$ and $0 < \gamma < 1$, VALUE-ITERATION stops, and its output satisfies $\lVert V - V^* \rVert < \varepsilon/2$ and $V^\pi(s) > V^*(s) - \varepsilon$ for each state $s$.

*Proof.* By Lemma 2 the loop stops at some sweep $k$ with $\delta_k < \varepsilon(1-\gamma)/(2\gamma)$, and line L10 returns $V = V_k$. Lemma 3 gives $\lVert V_k - V^* \rVert < \frac{\gamma}{1-\gamma} \cdot \frac{\varepsilon(1-\gamma)}{2\gamma} = \varepsilon/2$. Lines L8 and L9 make $\pi$ greedy for $V_k$, so Lemma 4 gives $\lVert V^\pi - V_k \rVert < \varepsilon/2$. By the triangle inequality, $\lVert V^\pi - V^* \rVert < \varepsilon$. $\blacksquare$

**The case $\gamma = 0$.** Then $TV = \max_a R(\cdot, a) = V^*$ for each $V$, so one sweep gives $V^*$ and a greedy policy is optimal. The code skips the test of line L7 in this case.

**Optimal policy after finitely many sweeps.** Let $\Pi$ be the finite set of deterministic policies and $g = \min\{\lVert V^* - V^\pi \rVert : \pi \in \Pi,\ V^\pi \ne V^*\}$, or $g = \infty$ if all policies are optimal. If $\frac{2\gamma}{1-\gamma} \cdot 2\gamma^{k-1}\lVert V_0 - V^* \rVert < g$, then by Lemma 4 and Lemma 3 every greedy policy for $V_k$ has $\lVert V^\pi - V^* \rVert < g$ and is optimal.
