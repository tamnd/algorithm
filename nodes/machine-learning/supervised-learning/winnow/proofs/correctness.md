---
title: The mistake bound of WINNOW1 for monotone disjunctions
proves: [correctness]
status: full
---

We use the pseudocode of the page. The target is $f = x_{i_1} \lor \cdots \lor x_{i_k}$, and $\mathcal{R} = \{i_1, \ldots, i_k\}$ is the set of relevant variables. Assume $\alpha > 1$ and $\theta \ge 1/\alpha$. Call a mistake of line L5 a *promotion step* and a mistake of line L7 an *elimination step*. Let $P$ and $E$ be their numbers.

**Lemma 1.** A relevant weight is never set to 0.

*Proof.* Line L7 runs only when $y = 0$, so $f(x) = 0$, so $x_i = 0$ for each $i \in \mathcal{R}$. Line L7 changes only weights with $x_i = 1$. $\square$

**Lemma 2.** Each relevant weight is promoted at most $\log_\alpha \theta + 1$ times.

*Proof.* Line L5 runs only when $\sum_j w_j x_j \le \theta$. All weights are nonnegative, so each promoted weight $w_i$ satisfies $w_i \le \theta$ just before the promotion. By Lemma 1 a relevant weight is never 0, so it is $\alpha^p$ after $p$ promotions (it starts at 1 and only line L5 changes it). If it is promoted a $p$-th time, then $\alpha^{p-1} \le \theta$, so $p \le \log_\alpha \theta + 1$. The value $\log_\alpha \theta + 1$ is nonnegative because $\theta \ge 1/\alpha$. $\square$

**Lemma 3.** $P \le k(\log_\alpha \theta + 1)$.

*Proof.* At a promotion step $y = 1$, so $f(x) = 1$, so $x_i = 1$ for some $i \in \mathcal{R}$, and line L5 promotes this relevant weight. So each promotion step promotes at least one relevant weight. By Lemma 2 the $k$ relevant weights receive at most $k(\log_\alpha \theta + 1)$ promotions in total. $\square$

**Lemma 4.** $E < n/\theta + (\alpha - 1) P$, when $E \ge 1$.

*Proof.* Let $W = \sum_i w_i$. At the start $W = n$, and $W \ge 0$ at all times.

At a promotion step, $\sum_i w_i x_i \le \theta$, and line L5 adds $(\alpha - 1) w_i$ for each active $i$. So $W$ grows by $(\alpha - 1) \sum_i w_i x_i \le (\alpha - 1)\theta$.

At an elimination step, $\sum_i w_i x_i > \theta$, and line L7 removes exactly this amount. So $W$ drops by more than $\theta$.

Other steps do not change $W$. After all steps, $0 \le W < n + (\alpha - 1)\theta P - \theta E$ when $E \ge 1$. Divide by $\theta > 0$. $\square$

**Theorem.** The number of mistakes is at most $\alpha k(\log_\alpha \theta + 1) + n/\theta$.

*Proof.* If $E = 0$, the number of mistakes is $P \le k(\log_\alpha \theta + 1)$ by Lemma 3, which is at most the bound since $\alpha > 1$. If $E \ge 1$, Lemma 4 gives $P + E < n/\theta + \alpha P$, and Lemma 3 gives $\alpha P \le \alpha k(\log_\alpha \theta + 1)$. $\blacksquare$

**Remark.** With the rule $\hat y = 1$ when $\sum_i w_i x_i \ge \theta$ instead, Lemma 2 uses $w_i < \theta$ and Lemma 4 uses a drop of at least $\theta$; the same bound follows. With $\alpha = 2$ and $\theta = n/2$ the bound is $2k\log_2 n + 2$, since $\log_2(n/2) + 1 = \log_2 n$.
