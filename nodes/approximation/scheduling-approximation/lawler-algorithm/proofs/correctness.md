---
title: Lawler's backward rule is optimal for 1|prec|fmax
proves: [correctness]
status: full
---

**Statement.** Let jobs $1, \ldots, n$ have processing times $p_j \ge 0$ and nondecreasing cost functions $f_j$, and let $G$ be an acyclic precedence graph. Call an order feasible if each arc $(a, b)$ of $G$ has $a$ before $b$, and let $f_{\max}(\sigma) = \max_j f_j(C_j)$ when $\sigma$ runs back to back from time 0. Then LAWLER returns a feasible order $\sigma$ with $f_{\max}(\sigma) \le f_{\max}(\tau)$ for every feasible order $\tau$. Since idle time does not decrease any $C_j$ and the $f_j$ are nondecreasing, $\sigma$ is also optimal among all non-preemptive schedules.

**Setup.** For a set $J$ of jobs, $p(J) = \sum_{j \in J} p_j$, and $G[J]$ is the graph induced on $J$. A job is a *sink* of $J$ if it has no successor in $J$. Every nonempty set has a sink, because $G[J]$ is acyclic. In line L4, $out[j] = 0$ holds exactly for the sinks of the current $J$: line L2 counts all successors, and line L6 lowers the count of $i$ by one each time a successor of $i$ leaves $J$.

We prove by induction on $|J|$ the predicate $Q(J)$: the rounds of lines L3 to L6 that start with the set $J$ and the value $P = p(J)$ fill the last $|J|$ positions with a feasible order of $G[J]$ whose value, with the jobs of $J$ run back to back from time 0, is the least over all feasible orders of $G[J]$. The statement is $Q$ of the set of all jobs.

**Base.** For $|J| = 0$ there is nothing to schedule. For $|J| = 1$ the only order is chosen.

**Step.** Let $|J| \ge 2$ and assume $Q(J')$ for all smaller sets (induction hypothesis). Let $j^*$ be the job of line L4, a sink of $J$ with the least $f_{j^*}(p(J))$ among the sinks.

1. *An optimal order ends with $j^*$.* Let $\tau$ be an optimal feasible order of $G[J]$, and let $\ell$ be its last job. The last job of a feasible order has no successor in $J$, so $\ell$ is a sink and $f_{j^*}(p(J)) \le f_\ell(p(J))$. Let $\tau'$ be $\tau$ with $j^*$ moved to the end and all other jobs kept in their order. $\tau'$ is feasible: the only pairs whose order changes are $(j^*, x)$ for jobs $x$ after $j^*$ in $\tau$, and none of them is an arc, because $j^*$ has no successor in $J$. In $\tau'$, each job $x \ne j^*$ that was after $j^*$ ends $p_{j^*}$ earlier, so $f_x(C_x(\tau')) \le f_x(C_x(\tau))$ by monotonicity. Each job before $j^*$ in $\tau$ keeps its completion time. The job $j^*$ ends at $p(J)$, and $f_{j^*}(p(J)) \le f_\ell(p(J)) = f_\ell(C_\ell(\tau)) \le f_{\max}(\tau)$. So $f_{\max}(\tau') \le f_{\max}(\tau)$, and $\tau'$ is optimal.
2. *The rest is the same problem.* Let $J' = J - \{j^*\}$. A feasible order of $G[J]$ that ends with $j^*$ is a feasible order $\rho$ of $G[J']$ followed by $j^*$, and the jobs of $\rho$ have the same completion times as when $\rho$ is run alone from time 0. So its value is $\max(f_{j^*}(p(J)), f_{\max}(\rho))$.
3. *The algorithm solves the rest.* After line L5 the algorithm holds $J'$ and $P = p(J) - p_{j^*} = p(J')$, and line L6 makes $out$ count successors inside $J'$. By the induction hypothesis $Q(J')$, the next $|J'|$ rounds fill the positions before $j^*$ with a feasible order $\rho^*$ of $G[J']$ of least value.
4. *Conclusion of the step.* The algorithm's order of $J$ is $\rho^*$ followed by $j^*$, with value $\max(f_{j^*}(p(J)), f_{\max}(\rho^*))$. By step 1, some optimal order is $\rho$ followed by $j^*$ for a feasible $\rho$, with value $\max(f_{j^*}(p(J)), f_{\max}(\rho)) \ge \max(f_{j^*}(p(J)), f_{\max}(\rho^*))$ by the choice of $\rho^*$. So the algorithm's order is optimal, which is $Q(J)$.

**End.** $Q$ holds for the set of all jobs, so LAWLER returns an optimal feasible order. ∎

**Cost.** Each of the $n$ rounds of line L4 scans at most $n$ jobs and evaluates at most $n$ cost functions, which is $O(n^2)$ evaluations in total. Line L6 visits each arc once over the whole run, which is $O(e)$. Lines L1 and L2 take $O(n + e)$. With $O(1)$ time for one evaluation, the time is $O(n^2 + e)$. The space is $\Theta(n + e)$ for the predecessor lists and the counters.
