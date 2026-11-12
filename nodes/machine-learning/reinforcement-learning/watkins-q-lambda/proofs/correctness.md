---
title: The cut traces of Watkins's Q(lambda) compute a greedy lambda-return, whose expected update has the optimal action values as a fixed point
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite, rewards are bounded, and either $\gamma\lambda < 1$ or episodes end with probability 1. Steps of one episode are numbered $k = 0, 1, \dots, T-1$, with $(S_k, A_k)$ the pair of step $k$, $\delta_k$ the TD error of line L9 (or line L6 at the last step), and

$$c_{k} = 1 \text{ if } A_{k} = A^*_{k}, \qquad c_k = 0 \text{ otherwise},$$

where $A^*_k$ is the action of line L8 for the state $S_k$. At the end of the episode we set $c_T = 0$, which matches line L14. For $t \le k$ we write $C_{t,k} = \prod_{i=t+1}^{k} c_i$, with $C_{t,t} = 1$.

**Termination.** Each step of the loop of line L4 does one call to the environment, $O(A)$ work for lines L7 and L8, and one update per pair with a nonzero trace, at most $SA$ of them. The implementation caps each episode at a given number of steps and runs a given number of episodes, so it stops. Without a cap, each episode ends when the terminal state is reached, which happens with probability 1 under the assumption. $\square$

**Lemma 1 (the trace).** The trace used by line L12 at step $k$ is

$$z_k(s, a) = \sum_{t \le k,\ (S_t, A_t) = (s, a)} (\gamma\lambda)^{k-t}\, C_{t,k}.$$

*Proof.* By induction on $k$. At $k = 0$, line L3 sets all traces to 0 and line L10 adds 1 to $(S_0, A_0)$, which is the formula. After the update of step $k$, lines L13 and L14 multiply every trace by $\gamma\lambda c_{k+1}$, since $A'$ is $A_{k+1}$ and $A^*$ is $A^*_{k+1}$. Then line L10 of step $k+1$ adds 1 to $(S_{k+1}, A_{k+1})$. Each old term $(\gamma\lambda)^{k-t} C_{t,k}$ becomes $(\gamma\lambda)^{k+1-t} C_{t,k+1}$, and the new term is the one with $t = k+1$. $\square$

**Lemma 2 (the forward view).** Hold $Q$ fixed during an episode (the offline form), and define the greedy λ-return backward from the end by $G_{T-1} = R_T$ and

$$G_t = R_{t+1} + \gamma\Big((1 - \lambda c_{t+1}) \max_b Q(S_{t+1}, b) + \lambda c_{t+1} G_{t+1}\Big).$$

Then the total change of $Q(s, a)$ over the episode is $\alpha \sum_{t:\ (S_t, A_t) = (s, a)} \big(G_t - Q(S_t, A_t)\big)$, and

$$G_t - Q(S_t, A_t) = \sum_{k = t}^{T-1} (\gamma\lambda)^{k-t}\, C_{t,k}\, \delta_k.$$

*Proof.* By Lemma 1 and a swap of the two sums, the total change is $\alpha \sum_k \delta_k z_k(s, a) = \alpha \sum_{t:\ (S_t, A_t) = (s, a)} \sum_{k \ge t} (\gamma\lambda)^{k-t} C_{t,k} \delta_k$. For the second claim, at $t = T-1$ both sides are $R_T - Q(S_{T-1}, A_{T-1}) = \delta_{T-1}$. For $t < T-1$, line L8 gives $Q(S_{t+1}, A^*_{t+1}) = \max_b Q(S_{t+1}, b)$, so $\delta_t = R_{t+1} + \gamma \max_b Q(S_{t+1}, b) - Q(S_t, A_t)$, and

$$G_t - Q(S_t, A_t) = \delta_t + \gamma\lambda c_{t+1}\big(G_{t+1} - \max_b Q(S_{t+1}, b)\big).$$

If $c_{t+1} = 1$, then $A_{t+1}$ is greedy and $\max_b Q(S_{t+1}, b) = Q(S_{t+1}, A_{t+1})$; if $c_{t+1} = 0$ the last term is 0 either way. So $G_t - Q(S_t, A_t) = \delta_t + \gamma\lambda c_{t+1} \big(G_{t+1} - Q(S_{t+1}, A_{t+1})\big)$, and unrolling this recursion gives the sum, since $C_{t,k} = c_{t+1} C_{t+1,k}$. $\square$

**Lemma 3 (only greedy actions after the first).** The return $G_t$ depends on the behavior only through $S_t$, $A_t$ and the steps after $t$ up to the first non-greedy action, and at that point it bootstraps with $\max_b Q$.

*Proof.* In the recursion of Lemma 2, $G_{t+1}$ enters only with the factor $c_{t+1}$. At the first $k > t$ with $c_k = 0$, $G_{k-1} = R_k + \gamma \max_b Q(S_k, b)$ and later rewards do not enter. Every action between $t$ and $k$ is greedy for $Q$. $\square$

So the backup is a mix of $n$-step returns of the greedy policy for $Q$, each closed by $\max_b Q$, which is what Q-learning estimates. This is Tree-Backup(λ) with the greedy target policy, as in Sutton and Barto (Section 12.10).

**Lemma 4 ($q_*$ is a fixed point).** Let $Q = q_*$, and let $\mathcal{F}_k$ be the history up to and including $A_k$. Then $\mathbb{E}[\delta_k \mid \mathcal{F}_k] = 0$ for every $k$, and so $\mathbb{E}[G_t - q_*(S_t, A_t) \mid \mathcal{F}_t] = 0$: in expectation the update does not move $q_*$.

*Proof.* Given $\mathcal{F}_k$, the pair $(S_k, A_k)$ is fixed and $R_{k+1}$, $S_{k+1}$ follow the MDP, so $\mathbb{E}[\delta_k \mid \mathcal{F}_k] = \mathbb{E}[R_{k+1} + \gamma \max_b q_*(S_{k+1}, b) \mid S_k, A_k] - q_*(S_k, A_k) = 0$ by the Bellman optimality equation. The weight $C_{t,k}$ is a function of $A_{t+1}, \dots, A_k$ and of the table, so it is known given $\mathcal{F}_k$. Hence $\mathbb{E}[C_{t,k} \delta_k \mid \mathcal{F}_t] = \mathbb{E}\big[C_{t,k}\, \mathbb{E}[\delta_k \mid \mathcal{F}_k] \mid \mathcal{F}_t\big] = 0$. The sum of Lemma 2 converges absolutely because the $\delta_k$ are bounded and either $\gamma\lambda < 1$ or the episode has finite mean length, so the mean of the sum is the sum of the means, which is 0. $\square$

**Lemma 5 (λ = 0).** With $\lambda = 0$, every update changes only $Q(S_k, A_k)$, by $\alpha\big(R_{k+1} + \gamma \max_b Q(S_{k+1}, b) - Q(S_k, A_k)\big)$, which is the update of one-step Q-learning.

*Proof.* By Lemma 1 with $\lambda = 0$, $z_k$ is 1 at $(S_k, A_k)$ and 0 elsewhere, and line L9 is the Q-learning TD error, as in the proof of Lemma 2. $\square$

**Theorem (correctness).** The updates of Watkins's Q(λ) are, in the offline form, steps of size $\alpha$ toward the greedy λ-returns of Lemma 2, which use only greedy actions after the first step (Lemma 3) and have $q_*$ as a fixed point in expectation (Lemma 4). For $\lambda = 0$ the method is one-step Q-learning (Lemma 5). In the online form, $Q$ changes within the episode, and the difference from the offline form is of order $\alpha^2$ per episode, as for [TD(λ)](/td-lambda/). With Robbins-Monro step sizes and every pair visited infinitely often, the tabular iterates converge to $q_*$ with probability 1; this convergence result is due to Munos, Stepleton, Harutyunyan and Bellemare (2016), as a case of their analysis of Retrace(λ), whose trace coefficient $\lambda \min(1, \pi / b)$ equals $\lambda c_k$ for a greedy target policy $\pi$. $\blacksquare$
