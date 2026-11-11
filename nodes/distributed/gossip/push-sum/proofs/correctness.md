---
title: Push-sum conserves mass and reaches relative error epsilon in O(log n + log 1/epsilon + log 1/delta) rounds
proves: [correctness]
status: full
---

**Claim.** Run push-sum on $n$ nodes with inputs $x_1, \ldots, x_n$, with every target uniform over all $n$ nodes and independent. Let $0 < \varepsilon, \delta < 1$. Then (1) $\sum_i s_{t,i} = \sum_j x_j$ and $\sum_i w_{t,i} = n$ for every $t$; and (2) with probability at least $1 - \delta$, for every $t \ge T$ and every node $i$,

$$\Big| \frac{s_{t,i}}{w_{t,i}} - \bar x \Big| \le \varepsilon \cdot \frac1n \sum_j |x_j|, \qquad T = 3\log_2 n + 2 \log_2 \tfrac1\varepsilon + \log_2 \tfrac2\delta + 2\tau,$$

where $\tau$ is any number of rounds such that push rumor spreading from one fixed node, with the same kind of random targets, informs all $n$ nodes within $\tau$ rounds with probability at least $1 - \delta/2$. Kempe, Dobra and Gehrke take $\tau = 4 \log n + \log(2/\delta)$, from Theorem 5.2 of Frieze and Grimmett. So $T = O(\log n + \log(1/\varepsilon) + \log(1/\delta))$.

**Notation.** Let $f_t(k)$ be the target of node $k$ in round $t$. For node $i$ let $S_t(i)$ be the multiset that holds $i$ once and each $k$ with $f_t(k) = i$ once. By lines L4 to L6, $s_{t+1,i} = \sum_{k \in S_t(i)} s_{t,k}/2$ and $w_{t+1,i} = \sum_{k \in S_t(i)} w_{t,k}/2$. Each $k$ lies in exactly two of these multisets, counted with multiplicity: in $S_t(k)$ for the half it keeps and in $S_t(f_t(k))$ for the half it sends. If $f_t(k) = k$, it lies twice in $S_t(k)$.

**Proof of (1), mass conservation.** Summing over $i$, each $s_{t,k}/2$ appears exactly twice, so $\sum_i s_{t+1,i} = \sum_k s_{t,k}$. The same holds for $w$. Induction on $t$ from $s_{0,i} = x_i$ and $w_{0,i} = 1$ gives (1).

**Contribution vectors.** Define $v_{0,i} = e_i \in \mathbb{R}^n$ and $v_{t+1,i} = \sum_{k \in S_t(i)} v_{t,k}/2$. By induction on $t$, $s_{t,i} = \sum_j v_{t,i,j} x_j$ and $w_{t,i} = \sum_j v_{t,i,j}$, because both sides follow the same linear update and agree at $t = 0$. By the argument of (1) applied to each coordinate, $\sum_i v_{t,i,j} = 1$ for every $j$. All entries are nonnegative, and $w_{t,i} \ge 2^{-t} > 0$, because node $i$ keeps half of its own weight in each round.

**Error from contributions.** Let $r_{t,i,j} = v_{t,i,j}/w_{t,i}$. Then $\sum_j r_{t,i,j} = 1$, and

$$\frac{s_{t,i}}{w_{t,i}} - \bar x = \sum_j \Big(r_{t,i,j} - \frac1n\Big) x_j, \qquad \text{so} \qquad \Big| \frac{s_{t,i}}{w_{t,i}} - \bar x \Big| \le \max_j \Big| r_{t,i,j} - \frac1n \Big| \cdot \sum_j |x_j|. \tag{A}$$

So it suffices that $\max_{i,j} |r_{t,i,j} - 1/n| \le \varepsilon / n$.

**Lemma 1 (the potential halves in expectation).** Let $u_{t,i} = v_{t,i} - (w_{t,i}/n) \mathbf 1$ and $\Phi_t = \sum_i \lVert u_{t,i} \rVert^2$. Then $\Phi_0 = n - 1$ and $\mathbb{E}[\Phi_{t+1} \mid \text{state at } t] = (\frac12 - \frac1{4n}) \Phi_t$.

*Proof.* At $t = 0$, $u_{0,i} = e_i - \frac1n \mathbf 1$ has squared norm $(1 - \frac1n)^2 + (n-1)\frac1{n^2} = 1 - \frac1n$, so $\Phi_0 = n - 1$. The map from $(v, w)$ to $u$ is linear, so $u_{t+1,i} = \frac12 \sum_{k \in S_t(i)} u_{t,k}$. By mass conservation of each coordinate, $\sum_k u_{t,k} = \mathbf 1 - \frac{n}{n} \mathbf 1 = 0$. Write $u_k$ for $u_{t,k}$ and $f$ for $f_t$. Then

$$\Phi_{t+1} = \frac14 \sum_i \Big( \lVert u_i \rVert^2 + 2 \sum_{k : f(k) = i} u_i \cdot u_k + \Big\lVert \sum_{k : f(k) = i} u_k \Big\rVert^2 \Big).$$

Take the expectation over the targets, which are independent of the state, with $\Pr[f(k) = i] = \frac1n$ and $\Pr[f(k) = f(k') = i] = \frac1{n^2}$ for $k \ne k'$. The middle term gives $\frac2n \sum_i u_i \cdot \sum_k u_k = 0$. The last term gives $\sum_i \big( \sum_k \frac1n \lVert u_k \rVert^2 + \sum_{k \ne k'} \frac1{n^2} u_k \cdot u_{k'} \big) = \Phi_t + \frac1n \big( \lVert \sum_k u_k \rVert^2 - \Phi_t \big) = (1 - \frac1n)\Phi_t$. So $\mathbb{E}[\Phi_{t+1}] = \frac14 \Phi_t + \frac14 (1 - \frac1n) \Phi_t = (\frac12 - \frac1{4n}) \Phi_t$. $\square$

Taking expectations repeatedly, $\mathbb{E}[\Phi_t] \le (n - 1) 2^{-t}$.

**Lemma 2 (weights).** Fix a round $t_0$ and let $\tau$ be as in the claim. With probability at least $1 - \delta/2$, every node has $w_{t_0 + \tau, i} \ge 2^{-\tau}$.

*Proof.* The weights sum to $n$, so some node $a$ has $w_{t_0, a} \ge 1$. Define $I_{t_0} = \{a\}$ and $I_{t+1} = I_t \cup \{f_t(k) : k \in I_t\}$. This is push rumor spreading from $a$ with the targets of rounds $t_0, t_0 + 1, \ldots$. We show by induction that every $k \in I_t$ has $w_{t,k} \ge 2^{-(t - t_0)}$. It holds at $t_0$. If $k \in I_t$, then $k \in S_t(k)$ and $k \in S_t(f_t(k))$, and all weights are nonnegative, so both $w_{t+1,k}$ and $w_{t+1, f_t(k)}$ are at least $w_{t,k}/2 \ge 2^{-(t + 1 - t_0)}$. The targets of rounds $t_0$ to $t_0 + \tau - 1$ are independent of the state at $t_0$, so of the choice of $a$. So $I_{t_0 + \tau}$ is all nodes with probability at least $1 - \delta/2$, by the choice of $\tau$. $\square$

**Lemma 3 (ratios only improve).** For every $t$, $\max_{i,j} |r_{t+1,i,j} - \frac1n| \le \max_{i,j} |r_{t,i,j} - \frac1n|$.

*Proof.* $r_{t+1,i} = \sum_{k \in S_t(i)} \frac{w_{t,k}}{2 w_{t+1,i}} \, r_{t,k}$. The coefficients are positive and sum to 1, because $w_{t+1,i} = \sum_{k \in S_t(i)} w_{t,k}/2$. So each coordinate of $r_{t+1,i} - \frac1n \mathbf 1$ is a convex combination of the same coordinates of the vectors $r_{t,k} - \frac1n \mathbf 1$. $\square$

**Proof of (2).** Let $t = \lceil T \rceil$ and $t_0 = t - \tau$; we may take $\tau$ to be an integer. Let $a = \varepsilon^2 \, 4^{-\tau} n^{-2}$. By Markov's inequality,

$$\Pr[\Phi_t > a] \le \frac{(n-1) 2^{-t}}{a} \le n^3 \, 4^{\tau} \, \varepsilon^{-2} \, 2^{-t} \le \frac\delta2,$$

because $t \ge 3\log_2 n + 2\tau + 2\log_2 \frac1\varepsilon + \log_2 \frac2\delta$. By Lemma 2, with probability at least $1 - \delta/2$, all weights at time $t$ are at least $2^{-\tau}$. By the union bound, both events hold with probability at least $1 - \delta$. On both events, for all $i, j$,

$$\Big| r_{t,i,j} - \frac1n \Big| = \frac{|u_{t,i,j}|}{w_{t,i}} \le 2^{\tau} \sqrt{\Phi_t} \le 2^{\tau} \sqrt a = \frac{\varepsilon}{n}.$$

By Lemma 3 the same bound holds at every later time, and by (A) every node has error at most $\varepsilon \cdot \frac1n \sum_j |x_j|$ at every time $t' \ge t$. $\square$
