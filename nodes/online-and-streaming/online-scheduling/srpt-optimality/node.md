---
tag: V78HTH
kind: theorem
slug: srpt-optimality
name: Optimality of SRPT for total flow time
aliases:
- Schrage's theorem
- SRPT optimality
area: online-and-streaming/online-scheduling
level: advanced
summary: SRPT minimizes total flow time on a single preemptive machine, and is therefore optimal among online algorithms.
prereqs: [srpt, flow-time, exchange-argument]
see_also: [flow-time-minimization, online-flow-time-minimization, online-total-completion-time, shortest-processing-time-first, smith-rule, preemptive-scheduling, competitive-ratio, identical-machines]
sources:
  - paper: "Linus Schrage, A proof of the optimality of the shortest remaining processing time discipline, Operations Research 16(3), 1968"
    locator: pages 687 to 690 (the theorem and its interchange proof)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Section 4.1 (SRPT is optimal for 1|r_j,pmtn|sum C_j, and its use as a lower bound without preemption)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (the problem without preemption, 1|r_j|sum C_j, is strongly NP-hard)
  - paper: "Stefano Leonardi and Danny Raz, Approximating total flow time on parallel machines, Journal of Computer and System Sciences 73(6), 2007 (STOC 1997)"
    locator: pages 875 to 891 (SRPT on m machines and the online lower bounds)
  - paper: "Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1 to 2), 1956"
    locator: pages 59 to 66 (shortest processing time first and the ratio rule for jobs released at time 0)
---

The optimality of SRPT, proved by Schrage in 1968, says that on one machine with [preemption](/preemptive-scheduling/), the [shortest remaining processing time](/srpt/) rule gives the least total [flow time](/flow-time/) of all schedules. SRPT is an [online algorithm](/online-algorithm/), so the theorem also says that it is 1-competitive, with no extra term. The result is the base case of the theory of online flow time: each other result is about a model where SRPT is not available or not optimal.

## Statement

Consider one machine of speed 1 and $n$ jobs, where job $j$ has release time $r_j \ge 0$ and processing time $p_j > 0$. A schedule runs at most one job at a time, runs no job before its release, and may preempt a job and resume it later with no loss. Let $C_j(S)$ be the completion time of job $j$ in schedule $S$.

**Theorem (Schrage 1968).** Let $S^*$ be the SRPT schedule, which at each time runs a released, unfinished job with the least remaining work. Then for each schedule $S$,

$$\sum_{j=1}^n C_j(S^*) \le \sum_{j=1}^n C_j(S), \qquad \text{and so} \qquad \sum_{j=1}^n (C_j(S^*) - r_j) \le \sum_{j=1}^n (C_j(S) - r_j).$$

The ties in the remaining work may be broken in any way. In three-field notation, SRPT solves $1 \mid r_j, \text{pmtn} \mid \sum C_j$ and $1 \mid r_j, \text{pmtn} \mid \sum F_j$ exactly.

**Online form.** Let $\sigma$ be the sequence of jobs, each one revealed with its size at its release time, and let ALG$(\sigma)$ and OPT$(\sigma)$ be the total flow time of SRPT and of the best offline schedule. Then ALG$(\sigma) = $ OPT$(\sigma)$ for each $\sigma$, so SRPT is 1-competitive with additive constant $b = 0$.

## In plain words

Suppose a schedule works on some job while another released job has less work left. Swap the work of the two jobs from that moment on: give the first part of their shared time to the smaller job, and the rest to the larger one. The smaller job now finishes earlier than either job finished before. The larger job finishes when the later of the two finished before. So the sum of the two finish times does not grow.

Do this swap, moment by moment from the start, until the schedule always works on the job with the least work left. That schedule is SRPT, and it is never worse than the schedule you started with.

## Proof

We give the exchange proof here. A second proof, which compares the sums of the smallest remaining works, is in the [correctness proof of SRPT](/srpt/).

Write the schedule as a finite set of pieces. Let $e_0 < e_1 < \dots < e_K$ be the distinct values among $0$, the release times and the SRPT completion times. On each interval $[e_i, e_{i+1})$, SRPT runs one job $j$ or idles, and no job is released inside the interval. If SRPT runs $j$, the interval is not longer than the remaining work of $j$ at $e_i$, since $j$ does not complete inside it.

The proof is by induction on $i$. Assume that a schedule $S$ with sum at most the sum of the original schedule agrees with SRPT on $[0, e_i)$. Then both have the same remaining work at $e_i$. If SRPT idles on the next interval, all released jobs are done, so $S$ idles too. Else SRPT runs $j$, and each other job $k$ that $S$ runs in the interval was released by $e_i$ and has at least as much remaining work as $j$.

For such a $k$, let $U$ be the set of times from $e_i$ on when $S$ runs $j$ or $k$. Give the first part of $U$, of length equal to the remaining work of $j$, to $j$, and the rest of $U$ to $k$. Then $j$ completes by $\min(C_j, C_k)$ and $k$ completes at $\max(C_j, C_k)$, so the sum does not grow. The part of $U$ inside the interval is no longer than the remaining work of $j$, so all of it goes to $j$, and $k$ leaves the interval. After at most $n - 1$ such exchanges, only $j$ runs in the interval. Finally, move later work of $j$ into the idle part of the interval. Now $S$ agrees with SRPT on $[0, e_{i+1})$.

At $i = K$, the schedule equals SRPT, and the sum never grew. The total flow time is the total completion time minus $\sum_j r_j$, which does not depend on the schedule. The full proof, with each inequality, is in [proofs/exchange.md](proofs/exchange.md). $\blacksquare$

## Consequences

- **SRPT is an optimal online algorithm.** It needs only the jobs released so far and their sizes, and it matches the offline optimum. So the online problem $1 \mid r_j, \text{pmtn} \mid \sum F_j$ is solved, and [online flow time minimization](/online-flow-time-minimization/) studies other models.
- **A lower bound for schedules without preemption.** Each schedule without preemption is also a preemptive schedule, so the SRPT value is a lower bound on the non-preemptive optimum. The analyses of the delayed SPT rule and of other rules for [online total completion time](/online-total-completion-time/) compare with this bound.
- **The order of completions.** The second proof shows more: for each $k$, the $k$-th job to complete under SRPT completes no later than the $k$-th job under any schedule. Equivalently, SRPT has the fewest unfinished jobs at every moment.
- **The batch case.** If all jobs are released at time 0, SRPT never preempts and is [shortest processing time first](/shortest-processing-time-first/), which is optimal for $\sum C_j$ by [Smith's rule](/smith-rule/) with unit weights.
- **The problem without preemption is hard.** In contrast, $1 \mid r_j \mid \sum C_j$ without preemption is strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977). Preemption is what makes the problem easy.

## Tightness

Each hypothesis of the theorem is necessary.

- **More than one machine.** On 2 identical machines, take jobs $(0, 1)$, $(0, 1)$, $(0, 3)$, $(3, 1)$ and $(3, 1)$, written as (release, size). SRPT runs both short jobs at time 0, so the long job runs alone on $[1, 3)$ and one machine idles. At time 3 three jobs with 1 unit of work compete for two machines, and the total flow time is 9. The schedule that starts the long job at time 0 on its own machine and runs the two short jobs one after the other on the other machine gets total 8. On $m$ machines the SRPT ratio is $\Theta(\log \min(n/m, P))$ in the worst case, where $P$ is the ratio of the largest to the smallest size (Leonardi and Raz 1997).
- **Weights.** With weights, $\sum w_j F_j$ is not minimized by SRPT, and the preemptive weighted problem is NP-hard. See [flow time minimization](/flow-time-minimization/) for an example.
- **Other objectives.** SRPT is not optimal for the maximum flow time, where it can starve a long job, while FIFO is optimal on one machine. It is not optimal for the total [stretch](/stretch/) either, where it is 2-competitive. With jobs $(0, 10)$ and $(8, 3)$, SRPT finishes the first job at 10 and the second at 13, for total stretch $1 + 5/3 = 8/3$. Running the second job on $[8, 11)$ gives $1 + 13/10 = 23/10$.
- **Unknown sizes.** If the sizes are revealed only when the jobs complete, SRPT cannot run, and no deterministic online algorithm has a ratio better than $\Omega(n^{1/3})$. See [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).
- **No preemption.** Without preemption, see the last item of Consequences.

## History

Smith showed in 1956 that shortest processing time first minimizes the total completion time when all jobs are released at time 0. Schrage published the proof for the preemptive problem with release times in 1968, by an interchange argument, after an earlier queueing analysis of the rule by Schrage and Miller. The strong NP-hardness of the non-preemptive problem is due to Lenstra, Rinnooy Kan and Brucker in 1977. Leonardi and Raz analyzed SRPT on parallel machines in 1997.

## References
