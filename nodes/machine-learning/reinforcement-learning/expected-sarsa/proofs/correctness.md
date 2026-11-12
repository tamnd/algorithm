---
title: The Expected SARSA target has the mean of the SARSA target and less variance, and with a greedy target policy it is Q-learning
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, rewards have bounded mean and variance, and $0 \le \gamma < 1$ (or $\gamma = 1$ with episodes that end with probability 1). We write $Q(\text{terminal}, \cdot) = 0$, and $T^\pi$ for the Bellman expectation operator on action values,

$$(T^\pi Q)(s, a) = \mathbb{E}\Big[R + \gamma \sum_{a'} \pi(a' \mid S') Q(S', a') \,\Big|\, S = s, A = a\Big].$$

**Termination.** Each step of the loop of line L4 does one call to the environment, $O(A)$ work for the behavior choice of line L5 and $O(A)$ work for the sum of line L7. The implementation caps each episode at a given number of steps and runs a given number of episodes, so it stops. Without a cap, an episode ends when the terminal state is reached, which happens with probability 1 when the behavior policy ends episodes with probability 1. $\square$

**Lemma 1 (the expected target).** Fix the table $Q$ and the pair $S = s$, $A = a$. Let $\bar Y = R + \gamma \sum_{a'} \pi(a' \mid S') Q(S', a')$ be the target of line L7. Then $\mathbb{E}[\bar Y \mid s, a] = (T^\pi Q)(s, a)$.

*Proof.* This is the definition of $T^\pi$. At a terminal $S'$ the sum is $0$ because $Q(\text{terminal}, \cdot) = 0$, and line L7 uses $R$ alone, which is the same value. $\square$

**Lemma 2 (same mean as SARSA, less variance).** With the same $s$, $a$ and $Q$, let $A' \sim \pi(\cdot \mid S')$ be drawn after $R$ and $S'$, and let $Y = R + \gamma Q(S', A')$ be the SARSA target. Then $\mathbb{E}[Y \mid R, S'] = \bar Y$, so $\mathbb{E}[Y] = \mathbb{E}[\bar Y]$, and

$$\operatorname{Var}(Y) = \operatorname{Var}(\bar Y) + \gamma^2\, \mathbb{E}\big[V(S')\big], \qquad V(s') = \sum_{a'} \pi(a' \mid s') \Big(Q(s', a') - \sum_{b} \pi(b \mid s') Q(s', b)\Big)^2 \ge 0.$$

*Proof.* Given $R$ and $S'$, the only randomness in $Y$ is $A'$, so $\mathbb{E}[Y \mid R, S'] = R + \gamma \sum_{a'} \pi(a' \mid S') Q(S', a') = \bar Y$, and the tower rule gives the equal means. Given $R$ and $S'$, $\operatorname{Var}(Y \mid R, S') = \gamma^2 \operatorname{Var}_{A' \sim \pi(\cdot \mid S')}(Q(S', A')) = \gamma^2 V(S')$. The law of total variance, $\operatorname{Var}(Y) = \operatorname{Var}(\mathbb{E}[Y \mid R, S']) + \mathbb{E}[\operatorname{Var}(Y \mid R, S')]$, gives the identity. Each $V(s')$ is a mean of squares, so it is at least $0$, and it is $0$ exactly when every action with $\pi(a' \mid s') > 0$ has the same value $Q(s', a')$. $\square$

**Lemma 3 (contraction).** For any policy $\pi$ and tables $Q_1$, $Q_2$, $\|T^\pi Q_1 - T^\pi Q_2\|_\infty \le \gamma \|Q_1 - Q_2\|_\infty$, and $q_\pi$ is the unique fixed point when $\gamma < 1$.

*Proof.* $|(T^\pi Q_1 - T^\pi Q_2)(s, a)| = \gamma \big|\mathbb{E}\big[\sum_{a'} \pi(a' \mid S')(Q_1 - Q_2)(S', a')\big]\big| \le \gamma \|Q_1 - Q_2\|_\infty$, since the weights $\pi(a' \mid S')$ and the law of $S'$ are probabilities. The fixed point is unique by the [Banach fixed point theorem](/bellman-contraction/), and $q_\pi$ is a fixed point by the Bellman expectation equation. $\square$

**Lemma 4 (a greedy target gives Q-learning).** If $\pi(\cdot \mid s')$ puts weight 1 on an action $a^*$ with $Q(s', a^*) = \max_{a'} Q(s', a')$, then line L7 computes $R + \gamma \max_{a'} Q(S', a')$, the Q-learning target. So with the same behavior policy and the same random draws, Expected SARSA with a greedy target and Q-learning make the same updates in the same order and return the same table.

*Proof.* The sum in line L7 has one nonzero term, $Q(S', a^*) = \max_{a'} Q(S', a')$. All other lines are those of Q-learning, and the behavior choice of line L5 does not depend on the target policy, so by induction on the steps the two tables are equal after every step. $\square$

**Theorem (correctness).**

1. For a fixed target policy $\pi$, Robbins-Monro step sizes for each pair, and every pair updated infinitely often, $Q$ converges to $q_\pi$ with probability 1 when $\gamma < 1$.
2. With a greedy target policy, $Q$ converges to $q_*$ under the conditions of [tabular Q-learning convergence](/tabular-q-learning-convergence/).
3. With an ε-greedy target policy whose $\varepsilon$ goes to 0 (GLIE), $Q$ converges to $q_*$ (van Seijen, van Hasselt, Whiteson and Wiering 2009).

*Proof.* (1) Write the update of line L8 as $Q_{t+1}(s, a) = (1 - \alpha_t) Q_t(s, a) + \alpha_t\big((T^\pi Q_t)(s, a) + w_t\big)$ with $w_t = \bar Y_t - (T^\pi Q_t)(s, a)$. By Lemma 1, $\mathbb{E}[w_t \mid \text{past}] = 0$, and its conditional variance is at most $C(1 + \|Q_t\|_\infty^2)$ for a constant $C$, since rewards have bounded variance and $|\sum_{a'} \pi(a' \mid S') Q_t(S', a')| \le \|Q_t\|_\infty$. By Lemma 3, $T^\pi$ is a $\gamma$-contraction in the max norm. These are the hypotheses of the asynchronous stochastic approximation theorem used for [tabular Q-learning convergence](/tabular-q-learning-convergence/) (see [stochastic approximation](/stochastic-approximation/) and the [Robbins-Monro conditions](/robbins-monro-conditions/)), with $T^\pi$ in place of the optimality operator, so $Q_t \to q_\pi$ with probability 1.

(2) By Lemma 4, the iterates are those of Q-learning, so the Q-learning theorem applies.

(3) The target operator at time $t$ is $T^{\pi_t}$ with $\pi_t$ ε-greedy for $Q_t$. For any table $Q$, $|(T^{\pi_t} Q - T^* Q)(s, a)| \le \gamma\, \varepsilon_t \cdot 2\|Q\|_\infty$, since $\pi_t$ differs from the greedy policy only on a mass $\varepsilon_t$ of the next action. So the update is the Q-learning update plus a bias term bounded by $2\gamma\varepsilon_t \|Q_t\|_\infty$, and $\|Q_t\|$ stays bounded by the same argument as for Q-learning. A bias that goes to 0 does not change the limit of the stochastic approximation (the same lemma that Singh, Jaakkola, Littman and Szepesvari 2000 use for SARSA), so $Q_t \to q_*$. $\blacksquare$
