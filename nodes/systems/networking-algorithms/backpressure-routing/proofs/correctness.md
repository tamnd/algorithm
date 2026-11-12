---
title: Backpressure routing keeps all queues stable for every load inside the capacity region
proves: [correctness]
status: full
---

We use the pseudocode of the page and the method of Tassiulas and Ephremides: a quadratic Lyapunov function whose expected drift is negative when the queues are large.

**Model.** Time is slotted. There are nodes $n$, commodities $c$ (destinations) and links $l = (a, b)$ with rates $\mu_l \le \mu_{max}$. A finite list $\mathcal{A}$ holds the feasible link sets. In slot $t$, a policy chooses $S(t) \in \mathcal{A}$ and an *allocation* $\mu_l^c(t) \ge 0$ with $\sum_c \mu_l^c(t) \le \mu_l$ if $l \in S(t)$ and $\mu_l^c(t) = 0$ otherwise. The arrivals $A_n^c(t)$ are independent over slots, with mean $\lambda_n^c$ and $\mathbb{E}[(A_n^c)^2] < \infty$. We set $Q_c^c \equiv 0$, since a packet leaves at its destination (line L7). For $n \ne c$, let $\text{out}_n^c(t) = \sum_{l \text{ leaves } n} \mu_l^c(t)$ and $\text{in}_n^c(t) = \sum_{l \text{ enters } n} \mu_l^c(t)$. A link may be allocated more than its tail holds, so it sends at most the allocation, and only packets that were present at the start of the slot (line L6). Hence

$$Q_n^c(t+1) \le \max\big(Q_n^c(t) - \text{out}_n^c(t),\ 0\big) + \text{in}_n^c(t) + A_n^c(t). \tag{1}$$

Backpressure is the policy that sets $\mu_l^{c_l}(t) = \mu_l$ for $l \in S(t)$ with $W_l > 0$, and 0 for every other pair.

**Capacity region.** A rate vector $\lambda$ is in $\Lambda_\varepsilon$, for $\varepsilon > 0$, if there are a probability distribution $(p_S)_{S \in \mathcal{A}}$ and flows $f_l^c \ge 0$ such that

$$\sum_c f_l^c \le \mu_l \sum_{S \ni l} p_S \quad \text{for every link } l, \qquad \lambda_n^c + \sum_{l \text{ enters } n} f_l^c + \varepsilon \le \sum_{l \text{ leaves } n} f_l^c \quad \text{for every } n \ne c.$$

The interior of the capacity region is the union of the sets $\Lambda_\varepsilon$ over $\varepsilon > 0$.

**Lemma 1 (one-slot drift).** Let $V(t) = \sum_{n \ne c} (Q_n^c(t))^2$. For every policy,

$$V(t+1) - V(t) \le \sum_{n \ne c} \Big(\big(\text{out}_n^c\big)^2 + \big(\text{in}_n^c + A_n^c\big)^2\Big) + 2 \sum_{n \ne c} Q_n^c A_n^c - 2 \sum_l \sum_c \mu_l^c\, \big(Q_a^c - Q_b^c\big),$$

where all terms are at slot $t$ and $l = (a, b)$.

*Proof.* For $q, x, y \ge 0$, let $z = \max(q - x, 0)$. Then $z \le q$ and $z^2 \le (q - x)^2$, so $(z + y)^2 \le (q - x)^2 + 2qy + y^2 = q^2 + x^2 + y^2 + 2q(y - x)$. Apply this to (1) with $q = Q_n^c$, $x = \text{out}_n^c$ and $y = \text{in}_n^c + A_n^c$, and sum over $n \ne c$. The cross terms give $2 \sum_{n \ne c} Q_n^c (\text{in}_n^c - \text{out}_n^c + A_n^c)$. Each allocation $\mu_l^c$ on $l = (a, b)$ appears in $\text{out}_a^c$ with the factor $-Q_a^c$ and in $\text{in}_b^c$ with the factor $Q_b^c$, where $Q_b^c = 0$ if $b = c$. So $\sum_{n \ne c} Q_n^c (\text{in}_n^c - \text{out}_n^c) = -\sum_l \sum_c \mu_l^c (Q_a^c - Q_b^c)$. $\square$

The rates are bounded and the arrivals have finite second moments, so the first sum on the right has a conditional mean at most a constant $B$, for every policy and every $Q(t)$.

**Lemma 2 (backpressure is greedy in the drift).** Given $Q(t)$, the allocation of backpressure maximizes $\Phi(\mu) = \sum_l \sum_c \mu_l^c (Q_a^c - Q_b^c)$ over all feasible allocations.

*Proof.* Fix $S \in \mathcal{A}$. For $l \in S$, the terms of $l$ are at most $\sum_c \mu_l^c \max_c (Q_a^c - Q_b^c)^+ \le \mu_l W_l$, by lines L2 and L3, and putting all of $\mu_l$ on $c_l$ when $W_l > 0$, and nothing otherwise, attains this. So the best allocation with set $S$ has $\Phi = \sum_{l \in S} \mu_l W_l$, and line L4 picks the set that maximizes it. $\square$

**Lemma 3 (a stationary randomized policy).** Let $\lambda \in \Lambda_\varepsilon$ with $p$ and $f$ as above. The policy STAT draws $S$ with probability $p_S$ in each slot, independently of everything else, and gives each $l \in S$ the allocation $\mu_l^c = \mu_l f_l^c / F_l$ with $F_l = \mu_l \sum_{S \ni l} p_S$ (and 0 if $F_l = 0$). It is feasible and, for every $n \ne c$,

$$\mathbb{E}\big[\text{out}_n^c - \text{in}_n^c\big] \ge \lambda_n^c + \varepsilon.$$

*Proof.* $\sum_c \mu_l^c = \mu_l \sum_c f_l^c / F_l \le \mu_l$ by the first constraint. The link $l$ is in the drawn set with probability $\sum_{S \ni l} p_S = F_l / \mu_l$, so $\mathbb{E}[\mu_l^c] = f_l^c$. The second constraint gives the claim. $\square$

**Theorem 4 (throughput optimality).** If $\lambda \in \Lambda_\varepsilon$ for some $\varepsilon > 0$, then under backpressure

$$\mathbb{E}\big[V(t+1) - V(t) \mid Q(t)\big] \le B - 2\varepsilon \sum_{n \ne c} Q_n^c(t),$$

and

$$\limsup_{T \to \infty} \frac{1}{T} \sum_{t=0}^{T-1} \mathbb{E}\Big[\sum_{n \ne c} Q_n^c(t)\Big] \le \frac{B}{2\varepsilon}.$$

*Proof.* The arrivals in slot $t$ are independent of $Q(t)$, so $\mathbb{E}[\sum Q_n^c A_n^c \mid Q(t)] = \sum Q_n^c \lambda_n^c$. By Lemma 2, the value of $\Phi$ for backpressure is at least the value for the allocation that STAT draws in the same slot, for every draw. STAT's draw is independent of $Q(t)$, so by Lemma 3,

$$\mathbb{E}[\Phi(\mu^{\text{STAT}}) \mid Q(t)] = \sum_{n \ne c} Q_n^c\, \mathbb{E}\big[\text{out}_n^c - \text{in}_n^c\big] \ge \sum_{n \ne c} Q_n^c (\lambda_n^c + \varepsilon),$$

where the equality is the regrouping of Lemma 1. Put these into Lemma 1:

$$\mathbb{E}[V(t+1) - V(t) \mid Q(t)] \le B + 2\sum Q_n^c \lambda_n^c - 2\sum Q_n^c(\lambda_n^c + \varepsilon) = B - 2\varepsilon \sum Q_n^c(t).$$

Take the mean and sum over $t = 0, \dots, T-1$. Since $V(T) \ge 0$,

$$2\varepsilon \sum_{t=0}^{T-1} \mathbb{E}\Big[\sum Q_n^c(t)\Big] \le BT + \mathbb{E}[V(0)].$$

Divide by $2\varepsilon T$ and let $T \to \infty$. $\blacksquare$

Backpressure does not use $\lambda$, $\varepsilon$, $p$ or $f$. STAT is used only in the proof.

**Theorem 5 (no policy does better).** If some policy keeps the time-average backlog bounded, then $\lambda$ is in the closure of the capacity region.

*Proof.* Let the policy run for $T$ slots and let $\hat p_S$ be the fraction of slots with set $S$, and $\hat f_l^c$ the number of packets of $c$ sent on $l$ per slot. Then $\sum_c \hat f_l^c \le \mu_l \sum_{S \ni l} \hat p_S$. Packets are conserved at each node, so the packets of $c$ that arrive at $n$ or enter it, minus those that leave it, equal the growth of $Q_n^c$, which is $o(T)$ in mean when the backlog stays bounded on average. So $\lambda_n^c + \sum_{\text{in}} \hat f_l^c - \sum_{\text{out}} \hat f_l^c \to 0$ along a subsequence on which $(\hat p, \hat f)$ converge in mean, which they do since they lie in a compact set. The limit satisfies the constraints of $\Lambda_\varepsilon$ with $\varepsilon = 0$. $\square$
