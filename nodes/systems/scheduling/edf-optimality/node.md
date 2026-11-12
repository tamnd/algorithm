---
tag: GWSMKM
kind: theorem
slug: edf-optimality
name: Optimality of earliest deadline first
aliases:
- EDF optimal on uniprocessors
- Dertouzos's theorem
area: systems/scheduling
level: advanced
summary: "On one preemptive processor, if any schedule meets all deadlines of a set of jobs with release times, EDF does too. Dertouzos proved it in 1974 by an exchange argument."
prereqs: [earliest-deadline-first, exchange-argument]
see_also: [earliest-deadline-first, earliest-due-date-first, least-laxity-first, maximum-lateness-minimization, rate-monotonic-optimality, preemptive-scheduling, scheduling-notation, srpt-optimality]
sources:
  - paper: "Michael L. Dertouzos, Control robotics: the procedural control of physical processes, Proceedings of IFIP Congress 1974, North-Holland, 807-813"
    locator: the optimality of the earliest deadline rule on one preemptive processor for any set of jobs
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the deadline driven scheduling algorithm and its full use of the processor for periodic tasks with implicit deadlines
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1) (1974), 177-185"
    locator: preemptive scheduling with release times on one machine to minimize the maximum lateness
  - paper: "Sudarshan K. Dhall and C. L. Liu, On a real-time scheduling problem, Operations Research 26(1) (1978), 127-140"
    locator: task sets on several processors that global EDF and global rate-monotonic priorities cannot schedule
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 3, Aperiodic Task Scheduling (Horn's algorithm and the proof of the optimality of EDF by exchanges of time slices)
---

The optimality theorem for [earliest deadline first](/earliest-deadline-first/) says that, on one processor with preemption, if any schedule meets all deadlines of a set of jobs with release times, then the schedule that always runs the pending job with the earliest deadline also meets them. Dertouzos proved it in 1974 for any job set, after Liu and Layland (1973) had shown that EDF uses the processor fully for periodic tasks. The proof is an [exchange argument](/exchange-argument/): a feasible schedule can be changed, one step at a time, into the EDF schedule without a missed deadline. The theorem extends [Jackson's rule](/earliest-due-date-first/), which sorts a batch of jobs that are all ready at time 0, to jobs that arrive over time.

## Statement

A *job* $j$ has a release time $r_j \ge 0$, a work $c_j > 0$ and an absolute deadline $d_j$. A *schedule* on one processor assigns to each moment at most one job; it runs job $j$ only at times $t \ge r_j$, for a total time of $c_j$, and it may stop and resume a job at any time with no cost. In each bounded interval it has finitely many pieces. The schedule *meets* the deadline of $j$ if $j$ ends by $d_j$, and it is *feasible* if it meets all deadlines. A job is *pending* at $t$ if it is released by $t$ and not finished.

An *EDF schedule* runs, at each moment when a job is pending, a pending job with the least deadline; ties go by any fixed order of the jobs.

**Theorem (Dertouzos 1974).** Let $J$ be a set of jobs in which each bounded interval of time holds finitely many releases. If $J$ has a feasible schedule on one processor, then each EDF schedule of $J$ is feasible.

**Corollary (maximum lateness).** For each finite job set, EDF minimizes the maximum lateness $\max_j (f_j - d_j)$ over all preemptive schedules on one processor; in the [notation](/scheduling-notation/) of scheduling theory, it solves $1 \mid r_j, \mathrm{pmtn} \mid L_{\max}$ (Horn 1974).

## In plain words

Suppose that some plan finishes every job on time on one machine, where you may pause a job and go back to it later. Then the simple habit "always work on the waiting job that is due first" also finishes every job on time. You do not need to know the future, and you do not need to search for a plan.

The reason is a swap. Take a good plan and find the first moment where it differs from the habit. The habit works on the job that is due first. The plan works on that job later, before its due time. Swap the two pieces of work. The job that is due first now runs earlier, and the other piece moves to a time that is still before the first job's due time, so it is still on time. Repeat until the plan is the habit.

## Proof

Let $J$ be finite first. Let $E$ be an EDF schedule of $J$, and let $0 = e_0 < e_1 < \cdots < e_m$ be the times at which $E$ releases or ends a job, together with 0. Between two such times, $E$ runs one job or idles, since the set of pending jobs and its least deadline change only at these times. Let $S$ be a feasible schedule of $J$.

We show by induction on $k$: there is a feasible schedule $S_k$ that agrees with $E$ on $[0, e_k)$. For $k = 0$ there is nothing to show; take $S_0 = S$. Assume $S_k$ is given. Both schedules have done the same work on each job before $e_k$, so they have the same pending jobs at $e_k$, with the same remaining work.

*If $E$ idles on $[e_k, e_{k+1})$*, no job is pending at $e_k$, and no job is released before $e_{k+1}$, so $S_k$ idles there too. Let $S_{k+1} = S_k$.

*If $E$ runs job $i$ on $[e_k, e_{k+1})$*, let $X$ be the set of times in $[e_k, e_{k+1})$ at which $S_k$ does not run $i$, and let $x$ be its length. If $x = 0$, let $S_{k+1} = S_k$. Otherwise:

- Job $i$ has at least $e_{k+1} - e_k$ units of work left at $e_k$, because $E$ runs it on the whole interval. $S_k$ runs it for only $(e_{k+1} - e_k) - x$ units there, so $S_k$ runs $i$ for at least $x$ units after $e_{k+1}$, and before $d_i$ because $S_k$ is feasible. Let $Y$ be the set of the first $x$ units of time after $e_{k+1}$ at which $S_k$ runs $i$. Then each point of $Y$ is before $d_i$.
- At the times of $X$, $S_k$ idles or runs jobs that are pending at $e_k$: no job is released in $(e_k, e_{k+1})$. Each such job $j$ has $d_j \ge d_i$, because $E$ chose $i$ at $e_k$.
- Build $S_{k+1}$ from $S_k$: run $i$ at the times of $X$, and place the content of $S_k$ on $X$ (the pieces of other jobs and of idle time), in the same order, on the times of $Y$. Nothing else changes.

Job $i$ gets the same total time, at earlier times, so it ends no later. A job $j$ that moves from $X$ to $Y$ runs later than before, but at times after its release and before $d_i \le d_j$. All other jobs keep their times. So $S_{k+1}$ is feasible, and it agrees with $E$ on $[0, e_{k+1})$.

After the last step, $S_m$ agrees with $E$ up to $e_m$, when $E$ has ended all jobs, so $S_m$ has no work left either, and $S_m = E$. So $E$ is feasible.

For an infinite $J$, take a job $j$ of $J$. The jobs released before $d_j$ form a finite set $J'$, which has a feasible schedule: the restriction of a feasible schedule of $J$. Before $d_j$, an EDF schedule of $J$ makes the same choices as an EDF schedule of $J'$ with the same ties, because no other job is released. So by the finite case, $j$ meets its deadline. $\blacksquare$

*Proof of the corollary.* Let $L^*$ be the least maximum lateness of a preemptive schedule of $J$. With deadlines $d_j + L^*$, the job set is feasible. Adding the same $L^*$ to each deadline does not change the order of the deadlines, so EDF makes the same choices. By the theorem, EDF meets the deadlines $d_j + L^*$, so its maximum lateness is at most $L^*$. $\blacksquare$

## Consequences

- **Exact tests for EDF are feasibility tests.** A periodic or sporadic task set is schedulable by EDF on one processor if and only if it is feasible at all. So $U \le 1$ for implicit deadlines (Liu and Layland 1973) and the processor demand criterion for other deadlines decide feasibility; see [EDF](/earliest-deadline-first/).
- **Online is enough.** EDF needs no knowledge of future releases, so on one processor the online and offline problems of meeting all deadlines have the same answer.
- **Other optimal rules.** [Least laxity first](/least-laxity-first/) is optimal on one processor too, by a similar exchange.
- **Maximum lateness.** EDF solves $1 \mid r_j, \mathrm{pmtn} \mid L_{\max}$; see [maximum lateness minimization](/maximum-lateness-minimization/).
- **Fixed priorities lose.** For deadlines at most the periods, the best fixed-priority order is the [deadline-monotonic](/rate-monotonic-optimality/) one, and it can miss deadlines of feasible sets, so fixed priorities waste part of the processor in the worst case.

**How it differs from Jackson's rule.** [Earliest due date first](/earliest-due-date-first/) (Jackson's rule) orders one batch of jobs that are all ready at time 0, with no preemption, to minimize the maximum lateness, $1 \mid\mid L_{\max}$; it is proved by swapping two neighbors in a sequence. The theorem here allows release times and preemption, makes its choices online at each release and completion, and is used for recurring tasks with hard deadlines. With release times and *no* preemption, the earliest deadline rule is not optimal, and $1 \mid r_j \mid L_{\max}$ is [strongly NP-hard](/strong-np-hardness/).

## Tightness

- **Preemption is needed.** Take jobs $(r, c, d) = (0, 4, 10)$ and $(1, 1, 2)$. Non-preemptive EDF starts the first job at time 0, so the second one ends at 5, after 2. Preemptive EDF runs the second job in $[1, 2)$, and so does a non-preemptive schedule that idles in $[0, 1)$.
- **One processor is needed.** Take jobs $(0, 2, 10)$, $(0, 2, 10)$ and $(0, 10, 11)$ on two processors. Global EDF runs the two short jobs first, in $[0, 2)$, and the long job ends at 12, after 11. Running the long job alone on one processor, and the short ones one after the other on the other, meets all deadlines. Dhall and Liu (1978) used task sets of this shape.
- **Only for feasible sets.** The theorem says nothing when no feasible schedule exists. Then EDF can miss many deadlines where another schedule misses one: with jobs $(0, 3, 2)$, $(0, 1, 3)$ and $(0, 1, 4)$, EDF runs the first job in $[0, 3)$ and misses all three deadlines; running the two short jobs first misses only the first one.
- **Cost of a switch.** The model has free preemptions. With a cost per switch the theorem does not apply as stated, although EDF preempts at most once per release.

## History

Jackson (1955) showed that ordering by due date minimizes the maximum lateness when all jobs are ready at the start. Liu and Layland (1973) introduced the deadline driven rule for periodic tasks and showed that it schedules each set with $U \le 1$. Dertouzos (1974) proved the optimality for any set of jobs on one preemptive processor, and Horn (1974) gave the same rule for the maximum lateness with release times. Mok (1983) proved the same for least laxity first. Dhall and Liu (1978) showed that the optimality does not carry over to several processors.

## References
