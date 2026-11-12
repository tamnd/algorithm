---
title: What is proved about DAgger
proves: [correctness]
status: full
---

DAgger returns a policy with a cost bound, not the expert's policy. We prove the three steps that the page states, in the setting of the page: a finite-horizon problem with $T$ steps, costs $C(s, a) \in [0, 1]$, a fixed start state $s_1$, and a deterministic expert $\pi^*$. For a policy $\pi$, $d^t_\pi$ is the distribution of the state at step $t$, $d_\pi = \frac{1}{T}\sum_{t=1}^{T} d^t_\pi$, and $\ell(s, \pi) = \Pr[\pi(s) \ne \pi^*(s)]$. Let $\varepsilon = \mathbb{E}_{s \sim d_{\pi^*}}[\ell(s, \pi)]$ and $\varepsilon_\pi = \mathbb{E}_{s \sim d_\pi}[\ell(s, \pi)]$.

For $k \ge 0$ steps to go, let $V^*_k(s)$ be the expected cost of the expert over $k$ steps from $s$, with $V^*_0 = 0$, and $Q^*_k(s, a) = C(s, a) + \mathbb{E}_{s' \sim P(\cdot \mid s, a)}[V^*_{k-1}(s')]$. Then $V^*_k(s) = Q^*_k(s, \pi^*(s))$ and $J(\pi^*) = V^*_T(s_1)$.

**Coupling.** Write each transition as $s' = F(s, a, U)$ with $U$ uniform and independent of everything else, and each action of $\pi$ as $a = G(s, W)$ with $W$ uniform and independent. Run $\pi$ and $\pi^*$ with the same $U_1, U_2, \dots$. Then the two runs have the right distributions, and they are in the same state at step $t$ if $\pi$ chose the expert's action at every step before $t$.

## Claim 1 (behavior cloning: $J(\pi) \le J(\pi^*) + T^2 \varepsilon$)

Let $\varepsilon_t = \mathbb{E}_{s \sim d^t_{\pi^*}}[\ell(s, \pi)]$, so $\sum_{t=1}^{T} \varepsilon_t = T\varepsilon$. In the coupling, let $s_t, a_t$ be the run of $\pi$ and $s^*_t, a^*_t$ the run of the expert. Let $B_j$ be the event that $a_i = a^*_i$ for all $i < j$ and $a_j \ne a^*_j$ (the first mistake is at step $j$).

On $B_j$, the runs agree up to step $j$, so $s_j = s^*_j$, and $a_j = G(s^*_j, W_j)$ with $W_j$ independent of $s^*_j$. So

$$\Pr[B_j] \le \Pr\big[G(s^*_j, W_j) \ne \pi^*(s^*_j)\big] = \mathbb{E}\big[\ell(s^*_j, \pi)\big] = \varepsilon_j .$$

If no mistake happens at steps $1, \dots, t$, then $(s_t, a_t) = (s^*_t, a^*_t)$. Otherwise the cost difference at step $t$ is at most 1. So

$$\mathbb{E}[C(s_t, a_t)] \le \mathbb{E}[C(s^*_t, a^*_t)] + \sum_{j \le t} \Pr[B_j] \le \mathbb{E}[C(s^*_t, a^*_t)] + T\varepsilon .$$

Summing over $t = 1, \dots, T$ gives $J(\pi) \le J(\pi^*) + T^2 \varepsilon$. $\square$

## Claim 2 (performance difference and $J(\pi) \le J(\pi^*) + uT\varepsilon_\pi$)

**Identity.** For every policy $\pi$,

$$J(\pi) - J(\pi^*) = \sum_{t=1}^{T} \mathbb{E}_{s \sim d^t_\pi}\Big[\sum_a \pi(a \mid s)\, Q^*_{T-t+1}(s, a) - V^*_{T-t+1}(s)\Big].$$

*Proof.* Let $s_t, a_t$ be a run of $\pi$ and $k_t = T - t + 1$. By the definition of $Q^*$ and the Markov property,

$$\mathbb{E}[Q^*_{k_t}(s_t, a_t)] = \mathbb{E}[C(s_t, a_t)] + \mathbb{E}[V^*_{k_t - 1}(s_{t+1})] = \mathbb{E}[C(s_t, a_t)] + \mathbb{E}[V^*_{k_{t+1}}(s_{t+1})].$$

So the right side of the identity is

$$\sum_{t=1}^{T} \mathbb{E}[C(s_t, a_t)] + \sum_{t=1}^{T} \mathbb{E}[V^*_{k_{t+1}}(s_{t+1})] - \sum_{t=1}^{T} \mathbb{E}[V^*_{k_t}(s_t)] = J(\pi) + \mathbb{E}[V^*_0(s_{T+1})] - V^*_T(s_1),$$

because the two last sums telescope. With $V^*_0 = 0$ and $V^*_T(s_1) = J(\pi^*)$, this is $J(\pi) - J(\pi^*)$. $\square$

**Bound.** Suppose $Q^*_k(s, a) - V^*_k(s) \le u$ for all $k$, $s$ and $a$. For $a = \pi^*(s)$ the difference is 0. So the bracket in the identity is at most $u \sum_{a \ne \pi^*(s)} \pi(a \mid s) = u\, \ell(s, \pi)$, and

$$J(\pi) - J(\pi^*) \le u \sum_{t=1}^{T} \mathbb{E}_{s \sim d^t_\pi}[\ell(s, \pi)] = u T \varepsilon_\pi . \qquad \square$$

The condition is needed only on states that $\pi$ reaches. In the windy lane of the page, $u = 2$.

## Claim 3 (DAgger makes the error on its own states small)

Assume the infinite-sample case, where line L6 minimizes the exact loss over the distributions of the rounds so far. Round $i$ defines the online loss $\ell_i(\pi) = \mathbb{E}_{s \sim d_{\pi_i}}[\ell(s, \pi)]$, and line L6 chooses

$$\hat\pi_{i+1} \in \arg\min_{\pi \in \Pi} \sum_{j \le i} \ell_j(\pi),$$

which is the follow-the-leader rule: $\hat\pi_i$ is chosen before $\ell_i$ is seen. Let $\varepsilon_N = \min_{\pi \in \Pi} \frac{1}{N}\sum_{i=1}^{N} \ell_i(\pi)$, and let $\gamma_N$ be the average regret of this sequence:

$$\frac{1}{N}\sum_{i=1}^{N} \ell_i(\hat\pi_i) \le \varepsilon_N + \gamma_N .$$

Then some $i \in \{1, \dots, N\}$ has $\varepsilon_{\hat\pi_i} \le \varepsilon_N + \gamma_N + \frac{1}{N}\sum_{i=1}^{N} \min(1, T\beta_i)$.

*Proof.* Fix $i$. Run $\pi_i$ by a coin at each step: with probability $\beta_i$ use the expert, else use $\hat\pi_i$. Couple this run with a run of $\hat\pi_i$ that uses the same transition noise and the same action noise of $\hat\pi_i$. The two runs agree up to step $t$ unless the coin chose the expert at some step before $t$, which has probability at most $\min(1, (t-1)\beta_i)$. So the total variation distance between $d^t_{\pi_i}$ and $d^t_{\hat\pi_i}$ is at most $\min(1, T\beta_i)$, and, by convexity, the same holds for the averages $d_{\pi_i}$ and $d_{\hat\pi_i}$. Since $\ell \in [0, 1]$,

$$\varepsilon_{\hat\pi_i} = \mathbb{E}_{d_{\hat\pi_i}}[\ell(s, \hat\pi_i)] \le \mathbb{E}_{d_{\pi_i}}[\ell(s, \hat\pi_i)] + \min(1, T\beta_i) = \ell_i(\hat\pi_i) + \min(1, T\beta_i).$$

Average over $i$ and use the regret bound. The smallest $\varepsilon_{\hat\pi_i}$ is at most the average. $\square$

**Corollary.** With Claim 2, the best of $\hat\pi_1, \dots, \hat\pi_N$ has $J \le J(\pi^*) + uT\big(\varepsilon_N + \gamma_N + \frac{1}{N}\sum_i \min(1, T\beta_i)\big)$. If $\gamma_N \to 0$ and $\frac{1}{N}\sum_i \min(1, T\beta_i) \to 0$ (for example $\beta_1 = 1$ and $\beta_i = 0$ after, or $\beta_i = p^{i-1}$), the extra cost is $uT\varepsilon_N$ plus a term that goes to 0 as $N$ grows. Ross, Gordon and Bagnell (2011, Section 3) state this result with slightly different constants, and add finite-sample versions.

## Loop invariant

After iteration $i$ of lines L2 to L7, $D$ holds the pair $(s, \pi^*(s))$ for every state $s$ visited in the episodes of rounds $1, \dots, i$, and nothing else. This holds for $i = 0$ by line L1, and line L5 adds exactly the pairs of round $i$. So line L6 of round $i$ trains on samples from $d_{\pi_1}, \dots, d_{\pi_i}$, as Claim 3 assumes. In the implementation, the classifier is a table fit by majority vote, which is exactly the minimizer of the empirical 0-1 loss on $D$, that is, follow the leader.

## What is not proved

The regret term $\gamma_N$ is small when the loss is strongly convex in the policy parameters (follow the leader then has regret $O(\log N / N)$), or when line L6 uses another no-regret learner. For the 0-1 loss with a general class $\Pi$, follow the leader need not have small regret, and the bound is only as good as $\gamma_N$. The windy-lane test checks Claims 1 and 2 exactly and shows the improvement of Claim 3 on fixed seeds; it does not prove a regret bound.
