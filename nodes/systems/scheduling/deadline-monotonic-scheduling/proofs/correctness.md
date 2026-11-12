---
title: DM is optimal for constrained deadlines, and the busy period analysis and Audsley's algorithm are exact
proves: [correctness]
status: full
---

The tasks are independent, synchronous periodic or sporadic, on one preemptive processor. A *fixed order* runs the pending job of the first task in the order, and jobs of one task in release order. For a task $\tau_i$ and a set $P$ of tasks above it, let $\operatorname{ok}(i, P)$ say that $\tau_i$ meets all its deadlines in each legal release pattern when exactly the tasks of $P$ have higher priority. Tasks below $\tau_i$ never run while a job of $\tau_i$ or of $P$ is pending, so $\operatorname{ok}(i, P)$ depends only on $i$ and the set $P$.

**The loop.** Lines L2 to L6 are the event loop of [rate-monotonic scheduling](/rate-monotonic-scheduling/) with a different rank, so in each run interval the job at the top of $Q$ is the pending job of highest priority. The same proof applies.

**DM optimality.** For $D_i \le T_i$, Theorem 2 on the page on [rate-monotonic optimality](/rate-monotonic-optimality/) shows that if some fixed order meets all deadlines, each deadline-monotonic order does. Line L1 builds one.

**Lemma 1 (busy period analysis).** Fix $\tau_i$ and $P$, and let $\Lambda = P \cup \{i\}$ with $\sum_{j \in \Lambda} C_j / T_j \le 1$ and integer periods. Let $L$ be the least $t > 0$ with $\sum_{j \in \Lambda} \lceil t / T_j \rceil C_j \le t$, and for $q \ge 0$ let $w_q$ be the least $w > 0$ with

$$(q + 1) C_i + \sum_{j \in P} \left\lceil \frac{w}{T_j} \right\rceil C_j \le w .$$

Then the largest response time of a job of $\tau_i$ over all legal release patterns is $\max\{ w_q - q T_i : 0 \le q < \lceil L / T_i \rceil \}$, and the synchronous release reaches it.

*Proof.* $L$ exists: at $t = H = \operatorname{lcm}_{j \in \Lambda} T_j$ the sum is $H \sum_j C_j / T_j \le H$. For $q < \lceil L / T_i \rceil$, $(q + 1) C_i \le \lceil L / T_i \rceil C_i$, so $w = L$ satisfies the inequality, and $w_q \le L$.

*The synchronous release reaches the value.* In the synchronous release, the jobs of $\Lambda$ released in $[0, L)$ have total work $\sum_{j \in \Lambda} \lceil L / T_j \rceil C_j = L$, which is the least such fixed point, so the processor runs jobs of $\Lambda$ without a gap in $[0, L)$. The job $J_q$ of $\tau_i$ released at $q T_i < L$ waits for $J_0, \ldots, J_{q-1}$. The argument of Lemma 1 on the page on [rate-monotonic optimality](/rate-monotonic-optimality/), with $C_k$ replaced by $(q + 1) C_i$ (the work of $J_0, \ldots, J_q$), shows that $J_q$ ends at $w_q$, so its response time is $w_q - q T_i$.

*No pattern does worse.* Take any legal pattern and a job $J$ of $\tau_i$ released at $r$ that ends at $f$. Let $t_0$ be the latest time $s \le r$ such that no job of $\Lambda$ released before $s$ is pending at $s$; it exists, since $s = 0$ qualifies and the schedule has finitely many pieces. By the choice of $t_0$, a job of $\Lambda$ is pending at each time in $(t_0, r]$, and $J$ is pending in $[r, f)$. So in $[t_0, f)$ the processor runs only jobs of $\Lambda$ released at or after $t_0$, without a gap. Let $q$ be the number of jobs of $\tau_i$ released in $[t_0, r)$. Their releases are at least $T_i$ apart, so $r - t_0 \ge q T_i$. Jobs of $\tau_i$ after $J$ do not run before $f$.

Let $w > 0$ satisfy the inequality for this $q$, and assume $f > t_0 + w$. In $[t_0, t_0 + w)$ the processor does $w$ units of work, all of it from jobs of $P$ released in $[t_0, t_0 + w)$, at most $\lceil w / T_j \rceil$ of them for each $\tau_j$, and from at most $q + 1$ jobs of $\tau_i$ up to $J$. Their total work is at most $w$. So all of it is done by $t_0 + w$. If $t_0 + w \ge r$, this includes $J$, so $f \le t_0 + w$, a contradiction. If $t_0 + w < r$, then no job of $\Lambda$ released before $t_0 + w$ is pending at $t_0 + w$, which contradicts the choice of $t_0$. So $f - t_0 \le w_q$, and $f - r \le w_q - q T_i$.

The same argument with $\Lambda$ in place of $P$ and $w = L$ shows that $f \le t_0 + L$, so $q T_i \le r - t_0 < f - t_0 \le L$, and $q < \lceil L / T_i \rceil$. $\square$

`worst_response_time` returns `None` when the utilization of $\Lambda$ is more than 1 (then the work in long windows grows faster than time, and some job misses in the synchronous release). Otherwise it computes $L$ and each $w_q$ by fixed-point iteration from $\sum_{j \in \Lambda} C_j$ and from $(q + 1) C_i$. These starts are at most the least fixed points, and the iterations increase and stay at or below them, as in the proof on the page on [response-time analysis](/response-time-analysis/); they stop at the least fixed points, which are at most $L$. By Lemma 1 the result is the exact worst response time, so `worst_response_time(tasks, i, P)` $\le D_i$ is exactly $\operatorname{ok}(i, P)$.

**Lemma 2 (monotone in the set above).** If $P' \subseteq P$ and $\operatorname{ok}(i, P)$, then $\operatorname{ok}(i, P')$.

*Proof.* The left side of the inequality that defines $w_q$ is pointwise smaller for $P'$, so each $w_q$ is at most its value for $P$; the same holds for $L$. So the maximum in Lemma 1 does not grow. $\square$

**Theorem (Audsley's algorithm).** `audsley_optimal_priority_assignment` returns an order that meets all deadlines if one exists, and `None` otherwise.

*Proof.* If it returns an order, each task $\tau_i$ was placed when the set of unassigned tasks other than $\tau_i$ was exactly the set of tasks that end above it, and $\operatorname{ok}(i, \cdot)$ held for this set. So each task meets its deadlines.

Assume that some order meets all deadlines. We show by induction that after each placement there is an order that meets all deadlines and whose lowest levels are the tasks placed so far, in the same places. At the start, this is the given order. Let $\sigma$ be such an order, and let $X$ be the set of unassigned tasks. The task $u$ of $X$ that is lowest in $\sigma$ has all of $X \setminus \{u\}$ above it, and nothing else, so $\operatorname{ok}(u, X \setminus \{u\})$ holds, and the algorithm finds a task $v$ with $\operatorname{ok}(v, X \setminus \{v\})$. Move $v$ in $\sigma$ to the place of $u$, and move each task of $X$ that was below $v$ one place up. Then $v$ meets its deadlines, by the test. Each task that moved up has lost $v$ from its set above, so it meets its deadlines by Lemma 2. Each other task has the same set above it. The new order meets all deadlines and extends the placement by $v$. So the algorithm never fails to find a task, and it ends with an order. $\blacksquare$
