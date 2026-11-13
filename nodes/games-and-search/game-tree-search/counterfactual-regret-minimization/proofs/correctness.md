---
title: The average strategy of CFR has exploitability at most 2 Δ |I| sqrt(A) / sqrt(T)
proves: [correctness, convergence-rate]
status: full
---

We use the pseudocode of the page and follow Zinkevich et al. (2007), Theorems 2 to 4. The game is a finite two-player zero-sum extensive game with perfect recall. Write $u$ for the payoff to player 1, so player 2 gets $-u$, and write $u_i$ for the payoff of player $i$. Let $\Delta = \max_z u(z) - \min_z u(z)$, let $|\mathcal I_i|$ be the number of information sets of player $i$, and let $A$ be the largest number of actions at an information set.

**Reach probabilities.** For a profile $\sigma$ and a history $h$, $\pi^\sigma(h) = \pi_1^\sigma(h)\,\pi_2^\sigma(h)\,\pi_c(h)$, where $\pi_i^\sigma(h)$ is the product of the probabilities of player $i$'s own actions on the path to $h$ and $\pi_c$ is the product of the chance probabilities. Write $\pi_{-i}^\sigma(h)$ for the product of the factors of the other player and of chance. By perfect recall, all histories in an information set $I$ of player $i$ have the same sequence of own actions, so $\pi_i^\sigma(h) = \pi_i^\sigma(I)$ for $h \in I$.

**Step 1. The average strategy realizes the average of the realization weights.** Line L12 adds $\pi_i^{\sigma^t}(h)\,\sigma^t(I, a)$ for every $h \in I$. All $h \in I$ have the same own reach, and the number of histories in $I$ does not depend on $t$, so after normalization the average strategy is $\bar\sigma(I, a) = \sum_t \pi_i^{\sigma^t}(I)\,\sigma^t(I, a) / \sum_t \pi_i^{\sigma^t}(I)$, which is Eq. 4 of the paper. By induction along the own actions of player $i$ on the path to $h$: if $\pi_i^{\bar\sigma}(I) = \frac1T \sum_t \pi_i^{\sigma^t}(I)$, then

$$\pi_i^{\bar\sigma}(Ia) = \pi_i^{\bar\sigma}(I)\,\bar\sigma(I, a) = \frac1T \sum_t \pi_i^{\sigma^t}(I)\,\sigma^t(I, a) = \frac1T \sum_t \pi_i^{\sigma^t}(Ia).$$

(If the denominator is 0, both sides are 0.) So $\pi_i^{\bar\sigma}(z) = \frac1T \sum_t \pi_i^{\sigma^t}(z)$ for every leaf $z$. The payoff $u(\sigma) = \sum_z \pi_1^\sigma(z)\,\pi_2^\sigma(z)\,\pi_c(z)\,u(z)$ is linear in the weights of each player when the other player's weights are fixed. Hence, for every strategy $\tau$, $u(\tau, \bar\sigma_2) = \frac1T\sum_t u(\tau, \sigma_2^t)$ and $u(\bar\sigma_1, \tau) = \frac1T\sum_t u(\sigma_1^t, \tau)$.

**Step 2. Exploitability is the sum of the average regrets.** The overall regret of player $i$ is $R_i^T = \max_\tau \sum_t \big(u_i(\tau, \sigma_{-i}^t) - u_i(\sigma^t)\big)$. By Step 1 and $u_2 = -u$,

$$R_1^T + R_2^T = T \max_\tau u(\tau, \bar\sigma_2) - \sum_t u(\sigma^t) - T \min_\tau u(\bar\sigma_1, \tau) + \sum_t u(\sigma^t) = T\,\mathrm{expl}(\bar\sigma),$$

where $\mathrm{expl}(\bar\sigma) = \max_\tau u(\tau, \bar\sigma_2) - \min_\tau u(\bar\sigma_1, \tau)$ is the exploitability of the page. So $\mathrm{expl}(\bar\sigma) = (R_1^T + R_2^T)/T$. This is the zero-sum form of Theorem 2.

**Step 3. Lines L9 to L11 compute the immediate counterfactual regrets.** Line L3 fixes $\sigma^t$ for the whole iteration, so every call of WALK in iteration $t$ uses the same profile. By induction on the height of $h$, WALK returns the expected value of $u$ from $h$ under $\sigma^t$: lines L6 and L7 are the leaf and the chance average, and lines L9 and L10 average the values of the children with the probabilities $\sigma^t(I, \cdot)$. Each call receives the reaches $\pi_1^{\sigma^t}(h)$, $\pi_2^{\sigma^t}(h)$, $\pi_c(h)$, because line L9 multiplies only the reach of the acting player by the probability of the action. Define the counterfactual value of $I$ and of an action $a$ at $I$ as

$$v_i(\sigma, I) = \sum_{h \in I} \pi_{-i}^\sigma(h)\, u_i(\sigma \mid h), \qquad v_i(\sigma, I, a) = \sum_{h \in I} \pi_{-i}^\sigma(h)\, u_i(\sigma \mid ha),$$

where $u_i(\sigma \mid h)$ is the expected payoff of player $i$ from $h$. Line L11 adds $\pi_{-i}^{\sigma^t}(h)\,(u_i(\sigma^t \mid ha) - u_i(\sigma^t \mid h))$ for each $h \in I$ (the sign makes it the payoff of player 2 when $i = 2$). Summed over $h \in I$, after $T$ iterations $R[I][a] = R_{\mathrm{imm}}^T(I, a) = \sum_t \big(v_i(\sigma^t, I, a) - v_i(\sigma^t, I)\big)$.

**Step 4. Regret matching bounds each immediate regret.** Fix $I$, write $R^t(a) = R^t_{\mathrm{imm}}(I, a)$ and $r^{t+1}(a) = v_i(\sigma^{t+1}, I, a) - v_i(\sigma^{t+1}, I)$, so $R^{t+1} = R^t + r^{t+1}$. Some strategy of player $i$ reaches $I$ for sure (perfect recall), so $\sum_{h \in I}\pi_{-i}^\sigma(h)$ is a probability and is at most 1. Hence $|r^{t+1}(a)| \le \Delta$. Line L3 picks $\sigma^{t+1}(I, a) = R^{t,+}(a)/S$ with $S = \sum_b R^{t,+}(b)$ when $S > 0$. Then

$$\sum_a R^{t,+}(a)\, r^{t+1}(a) = \sum_a R^{t,+}(a)\, v_i(\sigma^{t+1}, I, a) - S\, v_i(\sigma^{t+1}, I) = S\sum_a \sigma^{t+1}(I, a)\, v_i(\sigma^{t+1}, I, a) - S\, v_i(\sigma^{t+1}, I) = 0,$$

and the sum is 0 also when $S = 0$. For each $a$, $\big((R^t(a) + r(a))^+\big)^2 \le (R^{t,+}(a) + r(a))^2$: this is an equality if $R^t(a) \ge 0$, and if $R^t(a) < 0$ the left side is at most $(r(a)^+)^2 \le r(a)^2$. Summing over $a$,

$$\lVert R^{t+1,+}\rVert^2 \le \lVert R^{t,+}\rVert^2 + 2\sum_a R^{t,+}(a)\, r^{t+1}(a) + \lVert r^{t+1}\rVert^2 \le \lVert R^{t,+}\rVert^2 + A\,\Delta^2.$$

So $\lVert R^{T,+}\rVert^2 \le T A \Delta^2$, and $R^{T,+}_{\mathrm{imm}}(I) = \max_a R^{T,+}(a) \le \Delta\sqrt{A}\sqrt{T}$. This is Theorem 4 for one information set, with the bound of Hart and Mas-Colell (2000).

**Step 5. The overall regret is at most the sum of the positive immediate regrets.** For an information set $I$ of player $i$ and an action $a$, let $\mathrm{Succ}(I, a)$ be the information sets of player $i$ that are reached after $a$ at $I$ with no other own action in between. By perfect recall, each history of such an $I'$ has exactly one prefix $h \in I$ followed by $a$, and the own reach from $ha$ to it is 1. So for every $\sigma$

$$v_i(\sigma, I, a) = D(\sigma, I, a) + \sum_{I' \in \mathrm{Succ}(I, a)} v_i(\sigma, I'),$$

where $D$ collects the leaves reached from $ha$ with no other own action. Define the full counterfactual regret $R^T_{\mathrm{full}}(I) = \max_{\tau} \sum_t \big(v_i(\sigma^t|_{I \to \tau}, I) - v_i(\sigma^t, I)\big)$, where $\sigma^t|_{I \to \tau}$ plays $\tau$ at $I$ and at the own information sets below $I$. The counterfactual value of $I$ does not depend on the own actions above $I$, so this is well defined. We claim $R^T_{\mathrm{full}}(I) \le \sum_{J} R^{T,+}_{\mathrm{imm}}(J)$, over $J = I$ and the own information sets below $I$. By induction from the bottom, for a deviation $\tau$,

$$\sum_t v_i(\sigma^t|_{I\to\tau}, I) = \sum_a \tau(I, a) \Big(\sum_t D(\sigma^t, I, a) + \sum_{I' \in \mathrm{Succ}(I,a)} \sum_t v_i(\sigma^t|_{I'\to\tau}, I')\Big) \le \sum_a \tau(I, a) \Big(\sum_t v_i(\sigma^t, I, a) + \sum_{I' \in \mathrm{Succ}(I,a)} R^{T,+}_{\mathrm{full}}(I')\Big).$$

A convex combination is at most the largest term, so subtracting $\sum_t v_i(\sigma^t, I)$ gives $R^T_{\mathrm{full}}(I) \le R^T_{\mathrm{imm}}(I) + \max_a \sum_{I' \in \mathrm{Succ}(I,a)} R^{T,+}_{\mathrm{full}}(I')$. The sets $\mathrm{Succ}(I, a)$ for different $a$ are disjoint, so the maximum is at most the sum over all of them, and the induction hypothesis gives the claim. The payoff $u_i(\sigma)$ splits in the same way into the leaves reached with no own action and the counterfactual values of the first own information sets, so $R_i^T \le \sum_{I \in \mathcal I_i} R^{T,+}_{\mathrm{imm}}(I)$. This is Theorem 3.

**Conclusion.** By Steps 4 and 5, $R_i^T \le |\mathcal I_i|\,\Delta\sqrt{A}\sqrt{T}$ for each player, and by Step 2

$$\mathrm{expl}(\bar\sigma^T) = \frac{R_1^T + R_2^T}{T} \le \frac{2\,\Delta\, \max_i |\mathcal I_i|\, \sqrt{A}}{\sqrt{T}} \longrightarrow 0.$$

Every Nash equilibrium of a two-player zero-sum game has exploitability 0 and gives the value $v$, and $\min_\tau u(\bar\sigma_1, \tau) \le v \le \max_\tau u(\tau, \bar\sigma_2)$, so $\bar\sigma^T$ is a $2\varepsilon$-equilibrium with $\varepsilon = \Delta \max_i|\mathcal I_i|\sqrt{A}/\sqrt{T}$, and its guaranteed payoff is within $\mathrm{expl}(\bar\sigma^T)$ of the value. Each iteration walks the finite tree once, so the procedure stops after $T$ iterations. $\blacksquare$
