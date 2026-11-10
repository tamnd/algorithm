---
title: Hu's algorithm is optimal for unit jobs with in-forest precedence
proves: [correctness]
status: full
---

We use the notation of the page. The jobs form an in-forest with successor map $s$, each job takes one slot, and there are $m$ machines. The level is $\ell(j) = 1$ for a root and $\ell(j) = 1 + \ell(s(j))$ otherwise. $N(h)$ is the number of jobs of level at least $h$, and $F_h$ is the set of these jobs. Hu's schedule is $\sigma$, with makespan $C = \max_j \sigma(j)$.

**Lemma 1 (feasibility).** In Hu's schedule, at most $m$ jobs share a slot, each job gets exactly one slot, and $\sigma(j) < \sigma(s(j))$.

*Proof.* Line L7 takes at most $m$ jobs. A job enters $A$ once: in line L3 if it has no predecessor, else in line L9 when the last of its predecessors runs. So it runs once. A job $k = s(j)$ enters $A$ only after line L8 gave a slot to each $i$ with $s(i) = k$, in particular to $j$, and line L7 takes $k$ at the earliest in the next pass of the loop. The loop stops only when $A$ is empty. If a job never ran, take one such job of largest level; its predecessors have larger levels, so they all ran, so the job entered $A$ and later ran, a contradiction. $\square$

**Lemma 2 (lower bound).** Each feasible schedule $\tau$ with makespan $C'$ satisfies $C' \ge h - 1 + \lceil N(h)/m \rceil$ for each $h \ge 1$.

*Proof.* A job $j$ of level $\ell$ has the path $j, s(j), s(s(j)), \ldots$ of $\ell$ jobs to its root, and each job of the path runs in a later slot than the one before it. So $\tau(j) \le C' - (\ell - 1)$. For $j \in F_h$ this gives $\tau(j) \le C' - h + 1$. At most $m$ jobs share a slot, so $N(h) \le m (C' - h + 1)$, which is the claim because $C'$ is an integer. $\square$

**Lemma 3 (Hu's rule on $F_h$).** For each $h$, the jobs of $F_h$ that Hu's algorithm runs in slot $t$ are the $\min(m, a)$ jobs of highest level among the $a$ jobs of $F_h$ that are available at slot $t$.

*Proof.* Each predecessor of a job of $F_h$ has a larger level, so it is in $F_h$. So whether a job of $F_h$ is available depends only on jobs of $F_h$. In line L7, every job of $F_h$ has a higher level than every job outside $F_h$, so the rule first takes available jobs of $F_h$, highest level first. $\square$

**Lemma 4 (the tail).** Fix $h$. Let $c$ be the last slot in which Hu's schedule runs a job of $F_h$. Suppose that some slot $t_1 < c$ runs fewer than $m$ jobs of $F_h$, and take the first such slot. Let $H$ be the largest level of a job of $F_h$ that has not run before slot $t_1$. Then $c = t_1 + H - h$, and slot $t_1$ is the last slot that runs a job of $F_H$.

*Proof.* Let $a_t$ be the number of available jobs of $F_h$ at the start of slot $t$, and $r_t$ the number of them that run in slot $t$. A job of $F_h$ becomes available after slot $t$ only if its last predecessor ran in slot $t$, and each job has at most one successor. So at most $r_t$ jobs become available, and $a_{t+1} \le a_t - r_t + r_t = a_t$. By Lemma 3, $r_t = \min(m, a_t)$. At $t_1$ we have $r_{t_1} < m$, so $a_{t_1} = r_{t_1} < m$, and by induction $a_t < m$ and $r_t = a_t$ for all $t \ge t_1$: from slot $t_1$ on, every available job of $F_h$ runs at once.

Let $H_t$ be the largest level of a job of $F_h$ that has not run before slot $t$, as long as one exists. A job that attains $H_t$ has no predecessor left, because its predecessors have larger levels, so it is available and runs in slot $t$ (for $t \ge t_1$). So after slot $t$ no job of level $H_t$ is left. If $H_t > h$, a job of level $H_t$ has its successor of level $H_t - 1 \ge h$, which has not run yet, so $H_{t+1} = H_t - 1$. If $H_t = h$, all jobs left in $F_h$ have level $h$ and all run in slot $t$, so $t = c$. Starting from $H_{t_1} = H$, we get $c = t_1 + (H - h)$.

At slot $t_1$, all jobs of $F_h$ of level above $H$ have run, and the jobs of level $H$ that are left all run in slot $t_1$. So $t_1$ is the last slot with a job of $F_H$. $\square$

**Theorem.** $C = \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$, so Hu's schedule is optimal.

*Proof.* By Lemma 2 it is enough to find an $h$ with $C \le h - 1 + \lceil N(h)/m \rceil$. We build a sequence of pairs $(h, c)$ with these two properties: (i) $c$ is the last slot that runs a job of $F_h$, and (ii) $C = c + h - 1$. The pair $(1, C)$ has both properties, because $F_1$ holds all jobs.

Take a pair $(h, c)$. If each slot $1, \ldots, c - 1$ runs $m$ jobs of $F_h$, then slot $c$ runs at least one more, so $N(h) \ge m(c - 1) + 1$ and $\lceil N(h)/m \rceil \ge c$. Then $h - 1 + \lceil N(h)/m \rceil \ge h - 1 + c = C$, and we stop.

Else let $t_1 < c$ be the first slot with fewer than $m$ jobs of $F_h$, and let $H$ be as in Lemma 4. Lemma 4 gives $c = t_1 + H - h$, so $C = c + h - 1 = t_1 + H - 1$, and $t_1$ is the last slot with a job of $F_H$. So $(H, t_1)$ has properties (i) and (ii). Also $t_1 < c$ gives $H > h$. The level grows in each step and is at most $n$, so the process stops, and it stops only in the first case. $\blacksquare$

**Corollary.** For every in-forest of unit jobs and every $m$, $\mathrm{OPT} = \max_{h \ge 1} \big(h - 1 + \lceil N(h)/m \rceil\big)$.
