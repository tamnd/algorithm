---
title: Meyerson's algorithm is O(log n)-competitive in adversarial order
proves: [correctness]
status: full
---

**Model.** $(M, d)$ is a metric space, $f > 0$ is the facility cost, and $\sigma = p_1, \ldots, p_n$ is a sequence of demand points, which may repeat. The order is adversarial: the adversary fixes $\sigma$ in advance and does not see the coins of the algorithm. All expectations are over these coins. For step $t$, let $\delta_t$ be the distance from $p_t$ to the nearest facility open before step $t$, with $\delta_1 = \infty$, and let $m_t = \min(\delta_t, f)$. The value $m_t$ depends only on the coins of steps $1, \ldots, t - 1$.

**Feasibility.** Each point is either a new facility (line L5) or assigned to an open facility (line L7), so the output is a feasible solution.

**Lemma 1 (one step).** Given the coins of steps $1, \ldots, t - 1$, step $t$ opens a facility with probability $m_t / f$, and its expected cost is at most $2 m_t$.

*Proof.* If $\delta_t \ge f$, the step opens with probability $1$ and costs $f = m_t$. Otherwise it opens with probability $\delta_t / f = m_t / f$, and its expected cost is $(\delta_t / f) f + (1 - \delta_t / f)\,\delta_t \le 2 \delta_t = 2 m_t$. $\square$

**Clusters and rings.** Fix an optimal solution with facility set $F^*$, and assign each point to its nearest facility of $F^*$. For $c \in F^*$, the cluster $C$ is the multiset of points assigned to $c$, with $r_p = d(p, c)$ and $A_C = \sum_{p \in C} r_p$. Then $\mathrm{OPT} = \sum_C (f + A_C)$. Let $\rho_0 = A_C / \lvert C \rvert$. Ring $0$ of $C$ holds the points with $r_p \le \rho_0$, and ring $i \ge 1$ the points with $2^{i-1} \rho_0 < r_p \le 2^i \rho_0$. Each $r_p$ is at most $A_C = \lvert C \rvert \rho_0$, so a nonempty ring $i \ge 1$ has $2^{i-1} < \lvert C \rvert$, which gives $i \le \lceil \log_2 \lvert C \rvert \rceil$. If $\rho_0 = 0$, all points are in ring $0$. So $C$ has at most $1 + \lceil \log_2 \lvert C \rvert \rceil$ nonempty rings.

**Lemma 2 (before the first opening in a ring).** Fix a ring $R$. Call a step of $R$ *early* if no earlier step of $R$ opened a facility. The expected total cost of the early steps of $R$ is at most $2f$.

*Proof.* Let $E_t$ be the event that $p_t \in R$ and step $t$ is early. $E_t$ depends only on the coins of steps before $t$. The early steps of $R$ are the steps up to and including the first step of $R$ that opens, so at most one early step opens. By Lemma 1,

$$\sum_t \mathbb{E}\big[\mathbf{1}_{E_t} \tfrac{m_t}{f}\big] = \sum_t \Pr[E_t \text{ and step } t \text{ opens}] \le 1.$$

By Lemma 1 again, the expected cost of the early steps is

$$\sum_t \mathbb{E}\big[\mathbf{1}_{E_t} \cdot \text{cost}_t\big] \le \sum_t \mathbb{E}\big[\mathbf{1}_{E_t} \cdot 2 m_t\big] \le 2f. \qquad \square$$

**Lemma 3 (after the first opening).** Let $p \in R$ arrive after a step of $R$ opened a facility at a point $q \in R$. The expected cost of the step of $p$, given the past, is at most $6 r_p$ if $R$ is ring $i \ge 1$, and at most $2 r_p + 2 \rho_0$ if $R$ is ring $0$.

*Proof.* The facility at $q$ is open, so $\delta \le d(p, q) \le r_p + r_q$. In ring $i \ge 1$, $r_q \le 2^i \rho_0 < 2 r_p$, so $\delta < 3 r_p$. In ring $0$, $r_q \le \rho_0$, so $\delta \le r_p + \rho_0$. Lemma 1 bounds the expected cost by $2\delta$. $\square$

**Theorem 4.** For every sequence $\sigma$ of $n \ge 1$ points fixed in advance,

$$\mathbb{E}[\mathrm{ALG}(\sigma)] \le \max\big(2 + 2 \lceil \log_2 n \rceil,\ 8\big) \cdot \mathrm{OPT}(\sigma).$$

*Proof.* Each step belongs to one cluster and one ring, and it is either early or comes after the first opening in its ring. Fix a cluster $C$. By Lemma 2, the early steps of $C$ cost at most $2f (1 + \lceil \log_2 \lvert C \rvert \rceil)$ in expectation. By Lemma 3, the other steps cost at most

$$\sum_{p \in \text{ring } 0} (2 r_p + 2 \rho_0) + \sum_{p \notin \text{ring } 0} 6 r_p \le 6 A_C + 2 \lvert C \rvert \rho_0 = 8 A_C.$$

So the expected cost of the steps of $C$ is at most $2 f (1 + \lceil \log_2 \lvert C \rvert \rceil) + 8 A_C \le \max(2 + 2 \lceil \log_2 n \rceil, 8)(f + A_C)$, because $\lvert C \rvert \le n$. Summing over the clusters gives the theorem by linearity of expectation. $\square$

**Remark (random order).** If the points arrive in a uniformly random order, Meyerson proved that the expected cost is at most $8 \cdot \mathrm{OPT}$. The proof above does not use the order, so it does not give this constant bound. The tests check the adversarial bound by exact enumeration of all coin flips on small instances, and they check the random order bound by averaging the exact expected cost over all orders.
