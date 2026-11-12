---
title: The Q-learning update is a stochastic approximation step toward the fixed point of a contraction
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, rewards have bounded mean and variance, $0 \le \gamma < 1$, $Q(\text{terminal}, \cdot) = 0$, and $\|Q\| = \max_{s,a}|Q(s, a)|$.

**Termination.** Each step of the loop of line L4 does one call to the environment and $O(A)$ operations. The implementation runs a given number of episodes, each cut after a given number of steps, so it stops. $\square$

**Lemma 1 (the expected target).** Let $\mathcal{F}$ be the past up to the choice of $A$, so that $S = s$, $A = a$ and $Q$ are known given $\mathcal{F}$. Then $\mathbb{E}[y \mid \mathcal{F}] = (T^* Q)(s, a)$, with $(T^* Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\max_{a'} Q(s', a')$.

*Proof.* Given $\mathcal{F}$, the pair $(R, S')$ has the law of the MDP for $(s, a)$, which does not depend on how $A$ was chosen. The target $y = R + \gamma\max_{a'} Q(S', a')$ is a function of $(R, S')$ and of the known table, so its mean is $r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\max_{a'} Q(s', a')$. At a terminal $s'$, $y = R$, which agrees with $Q(s', \cdot) = 0$. $\square$

**Lemma 2 (contraction).** For all tables $Q, Q'$, $\|T^* Q - T^* Q'\| \le \gamma\|Q - Q'\|$. So $T^*$ has exactly one fixed point, which is $q_*$.

*Proof.* For any functions $f, g$ on a finite set, $|\max f - \max g| \le \max|f - g|$: if $\max f = f(x)$, then $\max f - \max g \le f(x) - g(x)$, and the same with $f$ and $g$ swapped. So $|(T^* Q - T^* Q')(s, a)| \le \gamma\sum_{s'} p(s' \mid s, a)\,|\max_{a'} Q(s', a') - \max_{a'} Q'(s', a')| \le \gamma\|Q - Q'\|$. The Banach fixed point theorem gives one fixed point, and the Bellman optimality equation for action values says that $q_*$ is a fixed point. $\square$

**Lemma 3 (the update as stochastic approximation).** Line L8 can be written as

$$Q(s, a) \leftarrow (1 - \alpha)\,Q(s, a) + \alpha\big((T^* Q)(s, a) + w\big), \qquad w = y - (T^* Q)(s, a),$$

where $\mathbb{E}[w \mid \mathcal{F}] = 0$ and $\mathbb{E}[w^2 \mid \mathcal{F}] \le K(1 + \|Q\|^2)$ for a constant $K$.

*Proof.* The form is line L8 with $y = (T^* Q)(s, a) + w$. The mean of $w$ is 0 by Lemma 1. Since $w$ is $y$ minus its conditional mean, $\mathbb{E}[w^2 \mid \mathcal{F}] \le \mathbb{E}[y^2 \mid \mathcal{F}] \le 2\,\mathbb{E}[R^2 \mid \mathcal{F}] + 2\gamma^2\|Q\|^2$, and $\mathbb{E}[R^2 \mid \mathcal{F}]$ is bounded by the assumption on the rewards. $\square$

**Theorem.** If every pair is updated infinitely often and the steps of each pair satisfy $\sum_t \alpha_t(s, a) = \infty$ and $\sum_t \alpha_t(s, a)^2 < \infty$ with probability 1, then $Q \to q_*$ with probability 1.

*Proof.* Lemmas 2 and 3 are the hypotheses of the stochastic approximation theorem for contractions of Jaakkola, Jordan and Singh (1994) and Tsitsiklis (1994): an asynchronous iteration $x_i \leftarrow (1-\alpha)x_i + \alpha((Hx)_i + w)$, where $H$ is a max-norm contraction, the noise has mean 0 and conditional variance at most $K(1 + \|x\|^2)$, and each component has Robbins-Monro steps. The theorem gives $x \to x^*$, the fixed point of $H$, with probability 1. Here the components are the pairs (a pair that is not updated at time $t$ has step 0), $H = T^*$, and $x^* = q_*$. The outline of the proof of that theorem is on the [convergence of tabular Q-learning](/tabular-q-learning-convergence/) page. $\blacksquare$
