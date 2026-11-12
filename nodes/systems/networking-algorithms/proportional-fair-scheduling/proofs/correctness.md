---
title: The proportional fair rule is greedy for the log utility, and its fixed point maximizes the sum of log throughputs
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $\beta = 1/t_c \in (0, 1]$ and let every average $R_i$ be positive. The averages stay positive while $\beta < 1$, since line L5 multiplies by $1 - \beta > 0$ and line L4 adds a value that is not negative. (With $\beta = 1$ an unserved user's average drops to 0, and the rule must not be used.)

**Theorem 1 (one step is greedy).** Let $\beta < 1$. For a choice $k$ of the user to serve, let $R_i^{(k)}$ be the averages after lines L3 to L5. Then the user $i^*$ that line L1 chooses maximizes $\sum_i \log R_i^{(k)}$ over all $k$.

*Proof.* For a choice $k$,

$$\sum_i \log R_i^{(k)} = \sum_i \log\big((1-\beta) R_i\big) + \log\left(1 + \frac{\beta\, r_k}{(1-\beta) R_k}\right),$$

since only the term of user $k$ differs from $(1-\beta)R_i$. The first sum does not depend on $k$. The second term is an increasing function of $r_k / R_k$. So a $k$ with the largest $r_k / R_k$, which line L1 chooses, maximizes the sum. $\blacksquare$

For the long run, let the channel state $H(t) = (r_1(t), \dots, r_N(t))$ be independent and identically distributed over slots, with finite means. A *stationary policy* $\pi$ chooses, in each slot, a user at random with probabilities $\pi(i \mid h)$ that depend only on the current state $h$. Its long-run throughput vector is $T(\pi)$ with $T_i(\pi) = \mathbb{E}[r_i(H)\,\pi(i \mid H)]$. Let $\mathcal{C}$ be the set of these vectors. It is convex, because a mix of two policies with weights $\theta$ and $1 - \theta$ has throughput $\theta T(\pi_1) + (1 - \theta) T(\pi_2)$. A policy that also looks at the past, and whose long-run averages exist, still has throughputs in $\mathcal{C}$: its long-run choice probabilities given the state define a stationary policy with the same throughputs.

**Lemma 2 (the weighted rule maximizes a linear function).** For weights $w_i > 0$, the policy "serve a user with the largest $w_i r_i(h)$" maximizes $\sum_i w_i T_i$ over $\mathcal{C}$.

*Proof.* $\sum_i w_i T_i(\pi) = \mathbb{E}\big[\sum_i w_i r_i(H)\,\pi(i \mid H)\big]$, and for each state $h$, the inner sum is a mean of the values $w_i r_i(h)$ with weights $\pi(i \mid h)$, which is at most $\max_i w_i r_i(h)$. The rule attains this in every state. $\square$

**Theorem 3 (the fixed point is proportionally fair).** Let $T^* \in \mathcal{C}$ have positive entries, and let the rule "serve a user with the largest $r_i / T^*_i$", with some fixed way to break ties, give throughputs $T^*$. Then $T^*$ is the unique maximizer of $U(T) = \sum_i \log T_i$ over the vectors of $\mathcal{C}$ with positive entries.

*Proof.* By Lemma 2 with $w_i = 1/T^*_i$, every $T \in \mathcal{C}$ has $\sum_i T_i / T^*_i \le \sum_i T^*_i / T^*_i = N$. So $\sum_i (T_i - T^*_i)/T^*_i \le 0$. Let $T \in \mathcal{C}$ have positive entries. The function $\log$ is concave, so $\log T_i \le \log T^*_i + (T_i - T^*_i)/T^*_i$, with equality only when $T_i = T^*_i$. Summing,

$$U(T) \le U(T^*) + \sum_i \frac{T_i - T^*_i}{T^*_i} \le U(T^*),$$

and equality forces $T = T^*$. $\blacksquare$

**Remark (the link to the algorithm).** If the averages $R_i$ of PF settle near constants $T^*_i$, then line L1 is the rule of Theorem 3 with $w_i = 1/T^*_i$, and lines L4 and L5 make $R_i$ track the throughput that this rule gives to user $i$. So a limit point of PF must be the proportionally fair point. That the averages do settle, with an error that goes to 0 as $t_c$ grows, is the stochastic approximation theorem of Kushner and Whiting (2004), which we do not prove here.

**Corollary 4 (equal time under scaling).** Let $r_i(t) = c_i h_i(t)$ with constants $c_i > 0$ and with $h_1, \dots, h_N$ independent and identically distributed with a continuous distribution. Then the proportionally fair point gives each user $1/N$ of the slots.

*Proof.* Let $\tau$ be the common throughput of the rule "serve the largest $h_i$" for each $h_i$, which is the same for all $i$ by symmetry. Set $T^*_i = c_i \tau$. Then $r_i / T^*_i = h_i / \tau$, so the rule of Theorem 3 serves the largest $h_i$, which gives user $i$ throughput $c_i \tau = T^*_i$ and, by symmetry, $1/N$ of the slots. By Theorem 3, $T^*$ is the proportionally fair point. $\square$
