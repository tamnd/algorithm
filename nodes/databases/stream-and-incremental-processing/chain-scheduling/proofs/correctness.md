---
title: The envelope gives convex priorities, and Chain minimizes memory at every instant when every chart is convex
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. This proof covers the model of the code on the page, which is narrower than the model of Babcock, Babu, Datar and Motwani: one processor, operators of unit time, and one operator step per time unit. A query $q$ is a chain of operators $o_1, \dots, o_k$ with sizes $s_0 \ge s_1 \ge \cdots \ge s_k = 0$ and $s_0 > 0$: a tuple of $q$ enters with size $s_0$, has size $s_j$ after $o_j$, and leaves the system after $o_k$. The *drop* of $o_j$ is $d_j = s_{j-1} - s_j \ge 0$. Tuples arrive at given times. The memory $M(\tau)$ after step $\tau$ is the total size of the tuples that have arrived and not yet left.

## Part 1: the envelope

Let $T_0 = 0$ and $T_j = t_1 + \cdots + t_j$ for positive times $t_j$, and let $P_j = (T_j, s_j)$. The lower envelope is the lower convex hull of $P_0, \dots, P_k$, seen as a function $h$ on $[0, T_k]$.

**Lemma 1.** Lines L1 to L5 give each operator $o_j$ the priority $(h(T_{j-1}) - h(T_j)) / t_j$, and the priorities do not increase along the chain.

*Proof.* We use one fact about the hull. If all points lie on or above a line $\ell$, and $\ell$ passes through $P_a$ and $P_b$ with $a < b$, then $h = \ell$ on $[T_a, T_b]$. Indeed, $h(x)$ is the least value at $x$ of a convex combination of the points, every such combination is on or above $\ell$ because $\ell$ is linear, and the combinations of $P_a$ and $P_b$ reach $\ell$.

Let $i_0 = 0, i_1, i_2, \dots$ be the values of $i$ that the loop reaches, and let $\sigma_m$ be the slope that line L3 finds at $i_m$, so $\sigma_m = (s_{i_m} - s_{i_{m+1}}) / (T_{i_{m+1}} - T_{i_m})$ is the largest descent from $P_{i_m}$ to a later point. Let $\ell_m$ be the line through $P_{i_m}$ with slope $-\sigma_m$. We show by induction on $m$ that every point $P_j$ lies on or above $\ell_m$, and that $\sigma_m \le \sigma_{m-1}$ for $m \ge 1$.

Points after $i_m$ are on or above $\ell_m$ by the choice of $\sigma_m$. For $m = 0$ there are no earlier points. For $m \ge 1$, the point $P_{i_{m+1}}$ is on or above $\ell_{m-1}$ by the induction hypothesis, and $\ell_{m-1}$ passes through $P_{i_m}$, so $s_{i_{m+1}} \ge s_{i_m} - \sigma_{m-1}(T_{i_{m+1}} - T_{i_m})$, which gives $\sigma_m \le \sigma_{m-1}$. To the left of $T_{i_m}$, the line $\ell_m$ is then on or below $\ell_{m-1}$, because both pass through $P_{i_m}$ and $\ell_m$ is less steep. The points before $i_m$ are on or above $\ell_{m-1}$, so they are on or above $\ell_m$.

By the fact above, $h = \ell_m$ on $[T_{i_m}, T_{i_{m+1}}]$, so $h$ falls at the rate $\sigma_m$ there. Line L4 gives each operator $o_{i_m + 1}, \dots, o_{i_{m+1}}$ the priority $\sigma_m$, which is $(h(T_{j-1}) - h(T_j)) / t_j$ on this piece, and line L5 moves on to $i_{m+1}$. The order $\sigma_0 \ge \sigma_1 \ge \cdots$ is the second claim. $\square$

The test of the code compares the priorities with a brute-force hull over all pairs of points.

The chart is *convex* when $d_1 / t_1 \ge d_2 / t_2 \ge \cdots \ge d_k / t_k$. Then the chart is its own envelope, and the priority of $o_j$ is $d_j / t_j$; with unit times, it is $d_j$.

## Part 2: optimality for convex charts

Write $A(\tau)$ for the total entry size $s_0$ of the tuples that arrive at or before step $\tau$, and $D(\tau)$ for the total drop of the operator steps run in steps $0, \dots, \tau$. Then
$$M(\tau) = A(\tau) - D(\tau),$$
because a tuple that has run $o_1, \dots, o_j$ has size $s_0 - d_1 - \cdots - d_j$. $A(\tau)$ does not depend on the schedule, so a schedule minimizes $M(\tau)$ if and only if it maximizes $D(\tau)$.

**The relaxation.** Make one *job* $(x, j)$ for each tuple $x$ and each operator $o_j$ of its query, with weight $d_j$ and release time the arrival time of $x$. A relaxed schedule runs at most one released job per step, in any order, without the rule that $(x, j)$ must wait for $(x, j - 1)$. Every real schedule is a relaxed schedule, so the best relaxed value of $D(\tau)$ is an upper bound for every real schedule.

**Lemma 2.** Let $G$ be the relaxed schedule that, at each step, runs a released job of the largest weight that is not done yet. For every $\tau$, $G$ maximizes the total weight of the jobs done in steps $0, \dots, \tau$ over all relaxed schedules.

*Proof.* Fix $\tau$, and among the relaxed schedules with the largest weight by $\tau$ take one, $O$, that agrees with $G$ on the most initial steps, say on steps $0, \dots, u - 1$ with $u \le \tau$ as large as possible. Suppose $u \le \tau$ and let $g$ be the job of $G$ at step $u$; then $g$ is released by step $u$ and not done before it. If $O$ runs $g$ at a later step $u' \le \tau$, exchange the jobs of $O$ at steps $u$ and $u'$. The job $o$ that $O$ ran at step $u$ is released by $u \le u'$, so the result is a valid relaxed schedule with the same weight by $\tau$ that agrees with $G$ on step $u$ too. If $O$ does not run $g$ by $\tau$, replace the job of $O$ at step $u$ (or an idle step) by $g$. The weight by $\tau$ changes by $d(g) - d(o) \ge 0$, because $o$ was also released and not done at step $u$, and $G$ picked the heaviest such job. In both cases we get an optimal schedule that agrees with $G$ on more steps, which is a contradiction. So $O$ agrees with $G$ up to $\tau$, and $G$ is optimal. $\square$

**Lemma 3.** If every chart is convex and times are unit, then $G$ with the tie rule "the largest weight, then the oldest tuple, then the smallest $j$" runs exactly the same steps as Chain (lines L6 to L10) with the tie rule "the highest priority, then the oldest tuple".

*Proof.* By induction on the steps: suppose both have done the same jobs before step $u$, so for each tuple, the done jobs of $G$ are a prefix $(x, 1), \dots, (x, p_x)$ of its chain, as for Chain. Let $w$ be the largest weight of a released job that is not done. Each such job $(x, j)$ has $j > p_x$, and since the chart is convex, the next job $(x, p_x + 1)$ has weight $d_{p_x + 1} \ge d_j$. So $w$ is also the largest weight of a next job, which is the largest Chain priority among the waiting tuples, by Lemma 1. The tuples that own a job of weight $w$ are exactly the tuples whose next job has weight $w$. Both rules take the oldest of these tuples, and $G$ takes its smallest job of weight $w$, which is its next job. So both run the same job, and $G$ keeps the prefix form. $\square$

**Theorem.** If every query has a convex chart and all operators take unit time, then for every step $\tau$, Chain gives the least memory $M(\tau)$ over all schedules.

*Proof.* By Lemma 3, Chain's schedule is $G$, which is a real schedule. By Lemma 2, $G$ has the largest $D(\tau)$ over all relaxed schedules, and so over all real schedules. Since $M(\tau) = A(\tau) - D(\tau)$, it has the least memory. $\blacksquare$

The theorem is false without convexity. With the charts $1, 1, 0$ and $1, 2/5, 0$ and one tuple of each at time 0, Chain gives the priorities $1/2, 1/2$ and $3/5, 2/5$, so it runs the second query first and has memory $7/5$ after two steps, while running both operators of the first query first gives memory 1. The tests check this case, and they check the theorem against a search over all schedules on random small inputs.
