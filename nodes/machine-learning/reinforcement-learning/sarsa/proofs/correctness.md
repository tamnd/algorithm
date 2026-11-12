---
title: The SARSA target is an unbiased sample of a contraction, and its gap to the Q-learning target vanishes under GLIE
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, rewards have bounded mean and variance, and $0 \le \gamma < 1$. We write $\|Q\| = \max_{s,a} |Q(s, a)|$, and $Q(\text{terminal}, \cdot) = 0$.

**Termination.** Each step of the loop of line L4 does a constant number of operations plus $O(A)$ for the ε-greedy choice. The implementation caps each episode at a given number of steps, and runs a given number of episodes, so it stops. Without a cap, an episode ends when the terminal state is reached, which happens with probability 1 when every ε-greedy policy ends episodes with probability 1. $\square$

**Lemma 1 (the target for a fixed policy).** Let the action $A'$ be drawn from a policy $\pi(\cdot \mid S')$ that does not depend on $R$ beyond $S'$. Given $S_t = s$, $A_t = a$ and the table $Q$, the expected target of line L6 is

$$(T^\pi Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\sum_{a'} \pi(a' \mid s')\, Q(s', a').$$

*Proof.* By the tower rule, first over $A'$ given $S'$, then over $(R, S')$ given $(s, a)$: $\mathbb{E}[R + \gamma Q(S', A')] = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\, \mathbb{E}[Q(s', A') \mid S' = s']$, and the inner mean is $\sum_{a'} \pi(a' \mid s')\, Q(s', a')$. At a terminal $s'$ the target is $R$ alone, which matches $Q(s', \cdot) = 0$. $\square$

**Lemma 2 (contraction).** $\|T^\pi Q - T^\pi Q'\| \le \gamma\|Q - Q'\|$, so $T^\pi$ has exactly one fixed point, and it is $q_\pi$.

*Proof.* The rewards cancel, and $|(T^\pi Q - T^\pi Q')(s, a)| \le \gamma\sum_{s'} p(s' \mid s, a)\sum_{a'} \pi(a' \mid s')\, |Q(s', a') - Q'(s', a')| \le \gamma\|Q - Q'\|$, since the weights are nonnegative and sum to at most 1. By the Banach fixed point theorem there is exactly one fixed point. The Bellman expectation equation for action values says that $q_\pi$ is a fixed point. $\square$

**Lemma 3 (decomposition).** Let $T^*$ be the Bellman optimality operator, $(T^* Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\max_{a'} Q(s', a')$. Then the SARSA update of line L7 can be written as

$$Q(S, A) \leftarrow Q(S, A) + \alpha\big((T^* Q)(S, A) - Q(S, A) + w + c\big),$$

with $w = R + \gamma\max_{a'} Q(S', a') - (T^* Q)(S, A)$, which has mean 0 given the past, and $c = \gamma\big(Q(S', A') - \max_{a'} Q(S', a')\big) \le 0$.

*Proof.* Add and subtract $(T^* Q)(S, A)$ and $\gamma\max_{a'} Q(S', a')$ in $y - Q(S, A)$, with $y = R + \gamma Q(S', A')$. The mean of $w$ is 0 by the tower rule over $(R, S')$, as in Lemma 1. The sign of $c$ holds because $Q(S', A') \le \max_{a'} Q(S', a')$. $\square$

**Lemma 4 (the extra term vanishes under GLIE).** Suppose that $Q$ stays bounded and the policy is greedy in the limit: the probability of a non-greedy $A'$ given the past tends to 0. Then $\mathbb{E}[c \mid \text{past}] \to 0$.

*Proof.* $c = 0$ when $A'$ is greedy. Otherwise $|c| \le 2\gamma\|Q\|$. So $|\mathbb{E}[c \mid \text{past}]| \le 2\gamma\|Q\| \Pr(A' \text{ not greedy} \mid \text{past}) \to 0$. $\square$

**Theorem (Singh, Jaakkola, Littman and Szepesvari 2000).** If every pair is updated infinitely often, the steps of each pair satisfy $\sum_t \alpha_t(s, a) = \infty$ and $\sum_t \alpha_t(s, a)^2 < \infty$, and the policy is GLIE, then $Q \to q_*$ with probability 1.

*Proof outline.* By Lemma 3, SARSA is the iteration of [tabular Q-learning](/tabular-q-learning-convergence/), a stochastic approximation of the $\gamma$-contraction $T^*$ with noise $w$, plus the extra term $c$. The noise has mean 0 and a conditional variance bounded by a constant times $1 + \|Q\|^2$, by the bounded reward variance. Singh et al. (2000) prove a stochastic approximation lemma like that of Jaakkola, Jordan and Singh (1994), with an added term whose size tends to 0 with probability 1. Boundedness of $Q$ follows from the contraction as in the Q-learning proof, and Lemma 4 shows that the extra term tends to 0. The lemma then gives convergence to the unique fixed point of $T^*$, which is $q_*$ (see the [Bellman contraction](/bellman-contraction/)). $\blacksquare$
