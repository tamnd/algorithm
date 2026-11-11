---
title: The walk estimator gives all PageRank values within a factor 1 ± δ
proves: [correctness]
status: full
---

The graph $G = (V, E)$ is directed with $n$ nodes, and each node has an out-arc. Let $P$ be the walk matrix, $P[u, w] = 1/\text{outdeg}(u)$ for each arc $u \to w$ and 0 otherwise, and let $Q = (1 - \epsilon) P$. PageRank is the row vector $\pi$ with $\pi = \frac{\epsilon}{n} \mathbf{1}^\top + \pi Q$. The rows of $Q$ sum to $1 - \epsilon$, so $\sum_t Q^t$ converges to $(I - Q)^{-1}$, and $\pi = \frac{\epsilon}{n} \mathbf{1}^\top (I - Q)^{-1}$. Since the term $t = 0$ is $I$ and all terms are nonnegative, $\pi(v) \ge \epsilon / n$.

**The walks.** Lines L1 to L5 move $K$ tokens from each node. Each token is a walk: at each step it stops with probability $\epsilon$ and otherwise moves along a uniform out-arc, with fresh random choices. In this proof, first let the walks run until they stop (no limit $R$). A walk makes at least $t$ steps and is at $w$ after step $t$ with probability $Q^t[u, w]$ if it starts at $u$. Let $X_j$ be the number of visits of walk $j$ to $v$, with the start counted, and let $\zeta(v) = \sum_j X_j$. Line L1 counts the start and line L5 counts each later visit, so $\zeta(v)$ is the value of visits at node $v$ when no limit applies.

**Lemma 1 (unbiased).** $\mu := \mathbb{E}[\zeta(v)] = nK\pi(v)/\epsilon$, and so $\mu \ge K$.

*Proof.* A walk from $u$ visits $v$ at step $t$ with probability $Q^t[u, v]$. Summing over $t$, over the $K$ walks of each start node and over the start nodes, $\mu = K \sum_u \sum_{t \ge 0} Q^t[u, v] = K\, \mathbf{1}^\top (I - Q)^{-1} e_v = K \cdot \frac{n}{\epsilon} \pi(v)$. With $\pi(v) \ge \epsilon/n$, $\mu \ge K$. $\square$

So $\mathbb{E}[\epsilon \zeta(v) / (nK)] = \pi(v)$: the output of line L6 is unbiased when no token is cut off.

**The shape of one walk's visits.** Let $r = r(v)$ be the probability that a walk now at $v$ comes back to $v$ at a later step before it stops. The first step continues with probability $1 - \epsilon$, so $r \le 1 - \epsilon$, and we write $a = 1 - r \ge \epsilon$. Let $p_j$ be the probability that walk $j$ visits $v$ at all. By the Markov property, after each visit to $v$ the rest of the walk is a fresh walk from $v$, so given a first visit, the number of later visits $G$ has $\Pr[G \ge i] = r^i$. So $X_j = B_j (1 + G_j)$ with $B_j \in \{0, 1\}$, $\Pr[B_j = 1] = p_j$, and $\mathbb{E}[X_j] = p_j / a$. With Lemma 1, $\sum_j p_j = a\mu$. The walks use independent random choices, so the $X_j$ are independent.

The generating function of $1 + G$ is $M(\lambda) = \mathbb{E}[e^{\lambda(1 + G)}] = \sum_{i \ge 0} a r^i e^{\lambda(1 + i)} = \frac{a e^\lambda}{1 - r e^\lambda}$ for $r e^\lambda < 1$, and so

$$
M(\lambda) - 1 = \frac{e^\lambda - 1}{1 - r e^\lambda}.
$$

Also $\mathbb{E}[e^{\lambda X_j}] = 1 + p_j (M(\lambda) - 1) \le \exp(p_j (M(\lambda) - 1))$, and by independence

$$
\mathbb{E}[e^{\lambda \zeta(v)}] \le \exp\big(a\mu (M(\lambda) - 1)\big). \tag{1}
$$

**Lemma 2 (upper tail).** For $0 < \delta \le 1$, $\Pr[\zeta(v) \ge (1 + \delta)\mu] \le e^{-a\delta^2\mu/10}$.

*Proof.* Let $x = a\delta/4$ and $\lambda = \ln(1 + x) > 0$. Then $r e^\lambda = (1 - a)(1 + x) < 1$, and $1 - r e^\lambda = a - r x \ge a - x = a(1 - \delta/4)$, so $a(M(\lambda) - 1) \le x / (1 - \delta/4) \le x(1 + \delta/3)$, using $1/(1 - y) \le 1 + 4y/3$ for $0 \le y \le 1/4$. Also $\lambda \ge x - x^2/2$. By (1) and Markov's inequality,

$$
\Pr[\zeta \ge (1 + \delta)\mu] \le \exp\big(\mu x (1 + \delta/3) - \mu x (1 - x/2)(1 + \delta)\big) = \exp\Big(\mu x \Big(-\frac{2\delta}{3} + \frac{x(1 + \delta)}{2}\Big)\Big).
$$

With $\delta \le 1$ and $a \le 1$, $x(1 + \delta)/2 \le x = a\delta/4 \le \delta/4$, so the exponent is at most $-\frac{5}{12}\mu x\delta = -\frac{5}{48} a\delta^2\mu \le -\frac{a\delta^2\mu}{10}$. $\square$

**Lemma 3 (lower tail).** For $0 < \delta \le 1$, $\Pr[\zeta(v) \le (1 - \delta)\mu] \le e^{-a\delta^2\mu/8}$.

*Proof.* Take $\lambda > 0$ and put $y = 1 - e^{-\lambda}$. The same sum as for $M$ gives $\mathbb{E}[e^{-\lambda(1 + G)}] - 1 = \frac{e^{-\lambda} - 1}{1 - r e^{-\lambda}} = \frac{-y}{a + r y} \le \frac{-y}{a + y}$, and as in (1), $\mathbb{E}[e^{-\lambda\zeta}] \le \exp(-a\mu y/(a + y))$. Choose $y = a\delta/4 \le 1/4$. Then $\lambda = -\ln(1 - y) \le y + y^2$, and $\frac{a y}{a + y} = \frac{y}{1 + \delta/4} \ge y(1 - \delta/4)$. By Markov's inequality applied to $e^{-\lambda\zeta}$,

$$
\Pr[\zeta \le (1 - \delta)\mu] \le \exp\big(\mu(y + y^2)(1 - \delta) - \mu y(1 - \delta/4)\big) = \exp\Big(\mu y\Big(y(1 - \delta) - \frac{3\delta}{4}\Big)\Big).
$$

Since $y(1 - \delta) \le y \le \delta/4$, the exponent is at most $-\mu y\delta/2 = -a\delta^2\mu/8$. $\square$

**Lemma 4 (truncation).** With $R = \lceil \ln(n^2 K)/\epsilon \rceil$, the probability that some token is still alive after round $R$ is at most $1/n$.

*Proof.* A token is alive after round $R$ only if it continued $R$ times, which has probability $(1 - \epsilon)^R \le e^{-\epsilon R} \le 1/(n^2 K)$. There are $nK$ tokens, and the union bound gives $1/n$. $\square$

**Theorem.** With $K = \lceil 10\ln(2n^2)/(\epsilon\delta^2) \rceil$ and $0 < \delta \le 1$, with probability at least $1 - 2/n$, every node $v$ outputs $\tilde{\pi}(v)$ with $|\tilde{\pi}(v) - \pi(v)| \le \delta\pi(v)$.

*Proof.* By Lemmas 2 and 3, with $a \ge \epsilon$ and $\mu \ge K$ (Lemma 1), $\Pr[|\zeta(v) - \mu| \ge \delta\mu] \le 2e^{-\epsilon\delta^2 K/10} \le 2e^{-\ln(2n^2)} = 1/n^2$. By the union bound, all $n$ nodes have $|\zeta(v) - \mu| < \delta\mu$ with probability at least $1 - 1/n$. On the event of Lemma 4, which fails with probability at most $1/n$, the visits counted by the run with $R$ rounds equal $\zeta(v)$, since no token is cut off. On both events, line L6 outputs $\tilde{\pi}(v) = \epsilon\zeta(v)/(nK)$, and by Lemma 1, $|\tilde{\pi}(v) - \pi(v)| = \frac{\epsilon}{nK}|\zeta(v) - \mu| < \frac{\epsilon}{nK}\delta\mu = \delta\pi(v)$. $\blacksquare$

**The CONGEST budget.** In each round, line L4 sends at most one number on each arc, and the number is at most the count of tokens, which is at most $nK$. So each message has $O(\log(nK))$ bits, which is $O(\log n)$ when $1/\epsilon$ and $1/\delta$ are polynomial in $n$. The run has $R = O(\log(nK)/\epsilon)$ rounds and at most $mR$ messages.

**A weaker bound with the variance.** From $X_j = B_j(1 + G_j)$, $\mathbb{E}[X_j^2] = p_j\,\mathbb{E}[(1 + G)^2] = \frac{p_j(1 + r)}{a^2}$, so $\text{Var}(\zeta(v)) \le \sum_j \mathbb{E}[X_j^2] = \mu\frac{1 + r}{a} \le \mu\frac{2 - \epsilon}{\epsilon}$. By Chebyshev's inequality, one run fails at $v$ with probability at most $\frac{2 - \epsilon}{\epsilon\delta^2 K}$, which is at most $1/4$ when $K \ge 4(2 - \epsilon)/(\epsilon\delta^2)$. The median of $g$ independent runs then fails with probability at most $e^{-g/8}$ by the [median trick](/median-trick/). The tests check both this variance bound and the tail bounds.
