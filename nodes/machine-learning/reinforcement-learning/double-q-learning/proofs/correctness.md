---
title: The double estimator does not overestimate, and both tables of Double Q-learning converge to the optimal action values
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, rewards are bounded with $|R| \le R_{\max}$, and $0 \le \gamma < 1$. Both tables are 0 at the terminal state. We write $\|Q\| = \max_{s,a} |Q(s, a)|$ and $T^*$ for the Bellman optimality operator on action values.

**Termination.** Each step of the loop of line L4 does one call to the environment, $O(A)$ work for the ε-greedy choice of line L5, one coin flip, and $O(A)$ work for the argmax of line L8. The implementation caps each episode at a given number of steps and runs a given number of episodes, so it stops. Without a cap, an episode ends when the terminal state is reached, which happens with probability 1 when the behavior ends episodes with probability 1. $\square$

**Lemma 1 (the single estimator overestimates).** If $X_1, \dots, X_k$ are random with means $\mu_1, \dots, \mu_k$, then $\mathbb{E}[\max_i X_i] \ge \max_i \mu_i$.

*Proof.* For each $j$, $\max_i X_i \ge X_j$, so $\mathbb{E}[\max_i X_i] \ge \mu_j$. Take the max over $j$. $\square$

**Lemma 2 (the double estimator does not overestimate).** Let $X = (X_1, \dots, X_k)$ and $Y = (Y_1, \dots, Y_k)$ be independent with $\mathbb{E}[Y_i] = \mu_i$, and let $a^*$ be a maximizer of $X$, chosen by any rule that depends only on $X$ and on randomness independent of $Y$. Then $\mathbb{E}[Y_{a^*}] = \mathbb{E}[\mu_{a^*}] \le \max_i \mu_i$, with equality if all $\mu_i$ are equal.

*Proof.* Given $X$ and the tie rule, $a^*$ is fixed and $Y$ keeps its law, so $\mathbb{E}[Y_{a^*} \mid X] = \mu_{a^*} \le \max_i \mu_i$. Take the mean over $X$. If all $\mu_i$ are equal, $\mu_{a^*}$ is that common value. $\square$

**Lemma 3 (bounded tables).** If $\alpha_t \in [0, 1]$, then $\|Q^A_t\|, \|Q^B_t\| \le M = R_{\max} / (1 - \gamma)$ for all $t$, when both start in $[-M, M]$.

*Proof.* By induction on $t$. The target of line L8 satisfies $|y| \le R_{\max} + \gamma M = M$, and line L9 replaces $X(S, A)$ by a convex combination of $X(S, A)$ and $y$, both in $[-M, M]$. The other entries do not change. $\square$

**Lemma 4 (the two tables come together).** Let $\Delta_t = Q^B_t - Q^A_t$. Suppose every pair $(s, a)$ is visited infinitely often, and the step size at a visit depends only on the visit count of the pair, with $\sum_t \alpha_t(s, a) = \infty$ and $\sum_t \alpha_t(s, a)^2 < \infty$. Then $\Delta_t \to 0$ with probability 1.

*Proof.* Fix a step that visits $(s, a)$, with step size $\alpha$, next state $S'$, $a^* \in \arg\max Q^A(S', \cdot)$ and $b^* \in \arg\max Q^B(S', \cdot)$. If the coin picks $Q^A$, then $\Delta(s, a)$ becomes $\Delta(s, a) - \alpha\big(R + \gamma Q^B(S', a^*) - Q^A(s, a)\big)$. If it picks $Q^B$, it becomes $\Delta(s, a) + \alpha\big(R + \gamma Q^A(S', b^*) - Q^B(s, a)\big)$. The mean over the fair coin is

$$\Delta(s, a) + \frac{\alpha}{2}\Big(-\Delta(s, a) + \gamma\big(Q^A(S', b^*) - Q^B(S', a^*)\big)\Big),$$

so the update has the form $\Delta(s, a) \leftarrow (1 - \beta)\Delta(s, a) + \beta\,(F + w)$ with $\beta = \alpha / 2$, $F = \gamma\,\mathbb{E}\big[Q^A(S', b^*) - Q^B(S', a^*) \mid \text{past}\big]$ and $w$ a noise with conditional mean 0 (from $R$, $S'$ and the coin), whose conditional variance is bounded by Lemma 3. We bound $F$. If $Q^A(S', b^*) \ge Q^B(S', a^*)$, then, as $Q^A(S', b^*) \le Q^A(S', a^*)$,

$$0 \le Q^A(S', b^*) - Q^B(S', a^*) \le Q^A(S', a^*) - Q^B(S', a^*) \le \|\Delta\|.$$

If $Q^A(S', b^*) < Q^B(S', a^*)$, then, as $Q^B(S', a^*) \le Q^B(S', b^*)$,

$$0 < Q^B(S', a^*) - Q^A(S', b^*) \le Q^B(S', b^*) - Q^A(S', b^*) \le \|\Delta\|.$$

So $|F| \le \gamma \|\Delta\|$: the mean update of $\Delta$ is a $\gamma$-contraction toward 0 in the max norm. The steps $\beta = \alpha / 2$ satisfy the Robbins-Monro conditions when $\alpha$ does. By the asynchronous stochastic approximation lemma for max-norm contractions with bounded noise (the lemma used for [tabular Q-learning convergence](/tabular-q-learning-convergence/); see the [Robbins-Monro conditions](/robbins-monro-conditions/)), $\Delta_t \to 0$ with probability 1. $\square$

**Theorem (convergence).** Under the conditions of Lemma 4, $Q^A_t \to q_*$ and $Q^B_t \to q_*$ with probability 1.

*Proof.* Every pair is visited infinitely often and each visit flips an independent fair coin, so with probability 1 each table updates each pair infinitely often, and the step sizes on these subsequences still satisfy the Robbins-Monro conditions with probability 1 (each table gets about half of the visits of a pair). On a step that updates $Q^A$ at $(s, a)$ the target is

$$R + \gamma Q^B(S', a^*) = R + \gamma \max_{a'} Q^A(S', a') + \gamma\big(Q^B(S', a^*) - Q^A(S', a^*)\big).$$

The first part is the Q-learning target for $Q^A$, whose conditional mean is $(T^* Q^A)(s, a)$, and $T^*$ is a $\gamma$-contraction. The last part is a bias bounded by $\gamma\|\Delta_t\|$, which goes to 0 by Lemma 4. A stochastic approximation of a max-norm contraction whose bias goes to 0 with probability 1 has the same limit as without the bias (Singh, Jaakkola, Littman and Szepesvari 2000, the lemma they prove for SARSA). Its limit is the fixed point $q_*$ of $T^*$, so $Q^A_t \to q_*$. By symmetry, or because $Q^B_t = Q^A_t + \Delta_t$ and $\Delta_t \to 0$, also $Q^B_t \to q_*$. This is the argument of van Hasselt (2010). $\blacksquare$
