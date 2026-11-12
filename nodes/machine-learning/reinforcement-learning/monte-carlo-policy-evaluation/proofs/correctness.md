---
title: First-visit Monte Carlo is unbiased and consistent, and every-visit Monte Carlo is consistent
proves: [correctness, termination]
status: full
---

We use the notation of the page. The policy $\pi$ is fixed, so the states and rewards form a Markov chain on a finite set of states plus a terminal state. Rewards are bounded, $|R_{t+1}| \le R_{\max}$, and $0 \le \gamma \le 1$. From every state the episode ends with probability 1. The episodes are independent runs of this chain. Fix a state $s$ that an episode visits with probability $q_s > 0$.

**Fact 0 (the episode length has a geometric tail).** Since the chain is finite and ends with probability 1 from each state, there are an integer $m \ge 1$ and $\rho < 1$ such that from any state the episode lasts more than $m$ further steps with probability at most $\rho$. By the Markov property at the times $m, 2m, \ldots$, $\Pr(T > jm) \le \rho^j$. So $\mathbb{E}[T^2] < \infty$. Since $|G_t| \le R_{\max}(T - t) \le R_{\max} T$, all returns have finite mean and variance.

**Lemma 1 (the backward pass).** In one episode, after line L6 of the iteration with index $t$, the variable $G$ equals $G_t$.

*Proof.* By induction on $T - 1 - t$. For $t = T - 1$, line L4 set $G = 0$, and line L6 gives $G = R_T = G_{T-1}$. For $t < T - 1$, the hypothesis gives $G = G_{t+1}$ before line L6, and line L6 gives $R_{t+1} + \gamma G_{t+1} = G_t$ by the definition of the return. $\square$

**Lemma 2 (the running mean).** After $n$ executions of lines L8 and L9 for the state $s$, with the counted values $x_1, \ldots, x_n$, $N(s) = n$ and $V(s) = (x_1 + \cdots + x_n)/n$.

*Proof.* By induction on $n$. For $n = 0$, line L1 sets $N(s) = 0$ and $V(s) = 0$, and the claim on $V$ is empty. If $V(s) = \bar x_{n-1}$ before the $n$-th update, then after it $V(s) = \bar x_{n-1} + (x_n - \bar x_{n-1})/n = ((n-1)\bar x_{n-1} + x_n)/n = \bar x_n$. $\square$

**Lemma 3 (first visit).** Condition on the set of episodes that visit $s$, and let $X_1, X_2, \ldots$ be the returns that the first-visit version counts for $s$, one for each such episode. Then the $X_i$ are independent, and each has mean $V^\pi(s)$.

*Proof.* Let $\tau$ be the first time with $S_\tau = s$ in one episode. The event $\{\tau = t\}$ depends only on $S_0, \ldots, S_t$, so $\tau$ is a stopping time. By the strong Markov property, on $\{\tau < \infty\}$ the process $(S_{\tau + k}, R_{\tau + k + 1})_{k \ge 0}$ is independent of $(S_0, R_1, \ldots, S_\tau)$ and has the law of an episode started in $s$. Line L7 lets exactly the time $\tau$ pass (by line L3, $\mathrm{first}(S_t) = t$ holds only for $t = \tau$ when $S_t = s$), and by Lemma 1 the counted value is $G_\tau$. So $\mathbb{E}[G_\tau \mid \tau < \infty, S_0, \ldots, S_\tau] = \mathbb{E}_\pi[G_0 \mid S_0 = s] = V^\pi(s)$. Whether an episode visits $s$ is a function of the part before $\tau$, so the conditioning on the set of visiting episodes does not change this mean. Different episodes are independent, so the $X_i$ are independent. $\square$

**Theorem 1 (first visit).** After any number of episodes with $N(s) = n \ge 1$, $\mathbb{E}[V(s) \mid N(s) = n] = V^\pi(s)$. As the number of episodes grows, $V(s) \to V^\pi(s)$ with probability 1.

*Proof.* By Lemma 2, $V(s) = (X_1 + \cdots + X_n)/n$, and by Lemma 3 and the linearity of expectation its conditional mean is $V^\pi(s)$. Each episode visits $s$ with probability $q_s > 0$, independently, so by the strong law of large numbers for the indicators, $N(s) \to \infty$ with probability 1. By Lemma 3 and Fact 0 the $X_i$ are independent with the same law and a finite mean, so the strong law of large numbers gives $\bar X_n \to V^\pi(s)$ with probability 1. $\square$

**Theorem 2 (every visit).** For the every-visit version, $V(s) \to V^\pi(s)$ with probability 1 as the number of episodes grows.

*Proof.* In one episode let $K = \sum_{t \ge 0} \mathbf{1}\{t < T, S_t = s\}$ be the number of visits and $Y = \sum_{t \ge 0} \mathbf{1}\{t < T, S_t = s\}\, G_t$ the sum of the returns at the visits. By Lemmas 1 and 2, after $n$ episodes $V(s) = (Y_1 + \cdots + Y_n)/(K_1 + \cdots + K_n)$, once the denominator is positive.

First, $\mathbb{E}[Y] = V^\pi(s)\, \mathbb{E}[K]$. For a fixed time $t$, the event $\{t < T, S_t = s\}$ depends on the past up to $t$, and by the Markov property at the fixed time $t$, $\mathbb{E}[G_t \mid t < T, S_t = s, S_0, \ldots, S_t] = V^\pi(s)$. So $\mathbb{E}[\mathbf{1}\{t < T, S_t = s\} G_t] = V^\pi(s) \Pr(t < T, S_t = s)$. The sum over $t$ of the absolute values is at most $\sum_{t < T} R_{\max} T = R_{\max} T^2$, which has a finite mean by Fact 0, so we may exchange the sum and the expectation (Fubini). Summing over $t$ gives the claim, and $\mathbb{E}[K] \ge q_s > 0$.

The pairs $(Y_i, K_i)$ are independent and have the same law, with finite means. By the strong law of large numbers, $\frac1n \sum Y_i \to \mathbb{E}[Y]$ and $\frac1n \sum K_i \to \mathbb{E}[K] > 0$ with probability 1. So the ratio tends to $\mathbb{E}[Y]/\mathbb{E}[K] = V^\pi(s)$. $\square$

The every-visit estimate is biased in general: the example of the page has $\mathbb{E}[Y_1/K_1] = 3/2 \ne 2 = V^\pi(s)$.

**Termination.** Each episode is finite, so the loops of lines L3 and L5 run $T$ times each, and the loop of line L2 runs once per episode. So the algorithm stops on any finite list of episodes, after $O(T)$ steps in total. $\blacksquare$
