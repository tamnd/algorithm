---
title: What is proved about Double DQN
proves: [correctness]
status: full
---

Double DQN, like [DQN](/dqn/), has no convergence theorem with a nonlinear network. We prove the three facts that the page states about its target. Notation is that of the page: $\theta$ and $\theta^-$ are the online and target parameters, $m \ge 2$ is the number of actions, and $a^* = \arg\max_{a'} Q(s', a'; \theta)$ with ties broken by the first index.

**Claim 1 (no upward bias from independent evaluation).** Fix $r$, $s'$ that is not terminal, and $\gamma \ge 0$. Let $q(a) = Q^{\text{true}}(s', a)$ be the true values and write $Q(s', a; \theta^-) = q(a) + e_a$. Suppose that, given $\theta$, each $e_a$ has mean zero: $\mathbb{E}[e_a \mid \theta] = 0$ for every $a$. Then

$$\mathbb{E}[y \mid \theta] = r + \gamma\, q(a^*) \le r + \gamma \max_{a'} q(a').$$

*Proof.* Line L6 computes $a^*$ from $\theta$ only, so given $\theta$ it is a fixed index. Line L7 gives $y = r + \gamma (q(a^*) + e_{a^*})$. Take the expectation given $\theta$: $q(a^*)$ is fixed and $\mathbb{E}[e_{a^*} \mid \theta] = 0$, so $\mathbb{E}[y \mid \theta] = r + \gamma q(a^*)$. Since $q(a^*) \le \max_{a'} q(a')$ and $\gamma \ge 0$, the inequality follows. $\square$

The condition fails for DQN: there the chosen index is $\arg\max_a (q(a) + e_a)$, which depends on the same errors that are then used, and $\mathbb{E}[\max_a (q(a) + e_a)] \ge \max_a q(a)$ by Jensen's inequality for the convex function $\max$. The [double Q-learning](/double-q-learning/) page gives the full maximization bias argument. In Double DQN, $\theta^-$ is an old copy of $\theta$, so the condition holds only in part; Claim 1 shows what the decoupling buys when it holds.

**Claim 2 (van Hasselt, Guez and Silver, Theorem 1).** Let all true values at a state $s$ equal $V^*(s)$, and let the estimates be $Q(s, a) = V^*(s) + e_a$ with $\sum_a e_a = 0$ and $\frac{1}{m} \sum_a e_a^2 = c > 0$. Then

$$\max_a Q(s, a) \ge V^*(s) + \sqrt{\frac{c}{m - 1}},$$

and equality holds for some errors that meet the conditions.

*Proof.* Let $M = \max_a e_a$. Because the $e_a$ sum to zero and are not all zero (since $c > 0$), $M > 0$. Split the actions into the set $P$ with $e_a > 0$ and the rest. Let $S = \sum_{a \in P} e_a$. The negative errors sum to $-S$, so $\sum_{a \notin P} e_a^2 \le S^2$, because for numbers of one sign the sum of squares is at most the square of the sum. On $P$, each $e_a \le M$, so $\sum_{a \in P} e_a^2 \le M S$. There is at least one action outside $P$ (the errors sum to zero and $M > 0$), so $|P| \le m - 1$ and $S \le (m-1) M$. Adding,

$$m c = \sum_a e_a^2 \le M S + S^2 \le (m-1) M^2 + (m-1)^2 M^2 = m (m-1) M^2.$$

Hence $M^2 \ge c / (m-1)$, and $\max_a Q(s, a) = V^*(s) + M \ge V^*(s) + \sqrt{c/(m-1)}$.

For equality, take $e_a = b$ for $m - 1$ actions and $e_a = -(m-1) b$ for the last one, with $b > 0$. The sum is zero, $mc = (m-1) b^2 + (m-1)^2 b^2 = m (m-1) b^2$, so $c = (m-1) b^2$ and $\sqrt{c/(m-1)} = b = M$. $\square$

The same paper notes that, under these conditions, the absolute error of the double estimate has lower bound zero. To see this, let the second set of estimates equal $V^*(s)$ exactly at the action that the first set picks. Then the double estimate equals $V^*(s)$, and the conditions on the first set still hold.

**Claim 3 (reduction to DQN).** If $\theta^- = \theta$, the Double DQN target equals the DQN target.

*Proof.* With $\theta^- = \theta$, line L7 gives $r + \gamma Q(s', a^*; \theta)$ with $a^*$ a maximizer of $Q(s', \cdot; \theta)$, so $Q(s', a^*; \theta) = \max_{a'} Q(s', a'; \theta) = \max_{a'} Q(s', a'; \theta^-)$, which is the DQN target. For a terminal $s'$ both targets are $r$. $\square$

By line L9, $\theta^- = \theta$ right after each sync, so Claim 3 also says that the first minibatch after a sync uses the DQN targets.

**What is not proved.** The step from "the target does not overestimate" to "the learned values do not overestimate" needs that the errors of $\theta^-$ are independent of the choice made by $\theta$, which is false in general because $\theta^-$ is a delayed copy of $\theta$. The convergence of the whole algorithm with a shared-parameter network is not proved, for the reasons on the DQN page. Even in the tabular case the DQN argument does not carry over directly, because the action chosen at line L6 moves with $\theta$ while $\theta$ is fitted, so the fitted table is not simply $\hat T \theta^-$. No such claim is made on the page. $\blacksquare$
