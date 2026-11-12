---
tag: GCJJ20
kind: algorithm
slug: least-laxity-first
name: Least laxity first
aliases:
- LLF
- least slack time first
area: systems/scheduling
level: advanced
summary: "Run the job with the least laxity: the time to its deadline minus its remaining work. Optimal on one processor, like EDF, but it can switch jobs very often."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {k: the number of jobs, s: the number of time slots up to the last deadline}
  time: {worst: O(s k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1983
  people: [Aloysius K. Mok]
  note: Mok studied the least laxity rule in his 1983 MIT thesis on hard real-time systems and proved that it is optimal on one processor.
prereqs: [earliest-deadline-first]
see_also: [earliest-deadline-first, edf-optimality, preemption, real-time-scheduling, exchange-argument, schedulability-analysis, sporadic-task-model]
sources:
  - paper: "Aloysius K. Mok, Fundamental design problems of distributed systems for the hard-real-time environment, PhD thesis, Massachusetts Institute of Technology, 1983"
    locator: the least laxity scheduling rule and its optimality on one processor
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 4 (the least-slack-time-first algorithm and its optimality) and Chapter 6 (dynamic-priority scheduling of periodic tasks)
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapters 3 and 4 (EDF and other dynamic-priority algorithms, and the cost of preemptions)
---

Least laxity first (LLF) is the dynamic-priority scheduling rule that, at each moment, runs the released job with the least *laxity*: the time left until its [deadline](/deadline/) minus the work it still needs. Mok (1983) proved that it is optimal on one preemptive processor: if any schedule meets all deadlines of a set of jobs, LLF does too. Its weak point is the number of [preemptions](/preemption/): the laxity of a waiting job falls while the laxity of the running job stays the same, so two jobs with close laxities take turns again and again, while [earliest deadline first](/earliest-deadline-first/), which is also optimal, would not switch at all.

## In plain words

Each piece of work has a due time and an amount still to do. Its slack is how long it could still wait and finish in time. Always work on the piece with the least slack.

While a piece waits, its slack shrinks; while you work on it, its slack stays the same. So this rule always looks after the most urgent piece, and on one processor it finishes everything on time whenever any plan can. But when two pieces have about the same slack, the rule keeps switching between them, and each switch costs time in a real system. Ranking by due time alone is also on time whenever any plan is, and it switches far less, so it is the usual choice.

## The problem

The input is a set of $k$ jobs on one processor; job $j$ has a release time $r_j$, a work $c_j$ and an absolute deadline $d_j$, all integers. The jobs can come from [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) tasks. Time runs in unit slots, and a job can be preempted only at the start of a slot. The output is a schedule; the question is whether each job ends by its deadline.

At the start of slot $t$, a released job $j$ with remaining work $e_j(t) > 0$ has laxity

$$\ell_j(t) = d_j - t - e_j(t).$$

If $\ell_j(t) < 0$, job $j$ misses its deadline in every schedule. If $\ell_j(t) = 0$, it must run in each slot until it ends.

## The algorithm

```pseudo id=main
LLF(J)                                     ▷ J: jobs (r, c, d) with integer values
L1  t ← 0, last ← none
L2  while some job has work left do
L3      R ← the jobs with r ≤ t and work left
L4      if R is empty then the slot [t, t + 1) is idle; last ← none; t ← t + 1; continue
L5      k ← the job of R with the least laxity d − t − e; ties go to last, then to the earlier deadline, then to the lower number
L6      run k in [t, t + 1); e(k) ← e(k) − 1; t ← t + 1
L7      if e(k) = 0 then finish(k) ← t
        last ← k
```

The tie rule of line L5 is not needed for optimality; any tie rule gives an optimal schedule. Preferring the job that ran last (a *sticky* rule) halves the number of preemptions in the first example below. Without slots, the rule is not well defined at a tie: two jobs with equal laxity would have to share the processor at an infinite rate of switches.

## Example

**Two equal jobs.** Take two jobs with $(r, c, d) = (0, 4, 8)$. Both have laxity 4 at time 0.

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| laxities of A, B under sticky LLF | 4, 4 | 4, 3 | 3, 3 | 2, 3 | 2, 2 | 2, 1 | 1, 1 | 0, done |
| sticky LLF | A | B | B | A | A | B | B | A |
| LLF without the sticky rule | A | B | A | B | A | B | A | B |
| EDF | A | A | A | A | B | B | B | B |

All three meet both deadlines. The sticky rule preempts 3 times, the rule without it 6 times, and EDF never.

**Periodic tasks.** For $\tau_1 = (C, T) = (2, 5)$ and $\tau_2 = (4, 7)$ with implicit deadlines and synchronous release, the hyperperiod $[0, 35)$ holds 12 jobs. Both LLF and EDF meet all deadlines; LLF preempts 4 times, EDF once.

## Correctness

LLF is optimal by an exchange argument in the slot model. Take a feasible schedule $S$ that agrees with LLF before slot $t$, and let LLF run $i$ where $S$ runs $j$. If $d_i \le d_j$, $S$ runs $i$ later but before $d_j$. If $d_i > d_j$, the smaller laxity of $i$ gives $e_i - (d_i - d_j) \ge e_j \ge 1$, so $S$ runs $i$ at least once before $d_j$ too. Swapping that slot with slot $t$ keeps $S$ feasible and makes it agree with LLF up to slot $t$. The full proof is below.

## Complexity

- **Slots.** The loop runs once per slot, up to the last end, and line L5 scans the ready jobs, so the time is $O(s k)$ with $s$ slots. With integer data, $s$ is at most the last deadline of a feasible set.
- **A heap.** While a job waits, its laxity falls by 1 per slot; while it runs, its laxity stays the same. So the order among the waiting jobs never changes, and a heap keyed by $d_j - e_j$ (the laxity plus $t$) gives $O(\log k)$ per slot, plus a check of the running job.
- **Preemptions.** LLF can preempt in almost every slot, as the example shows, where EDF preempts only at releases.

## Properties

- **Optimal on one processor**, for any set of jobs with release times, in the slot model and, as a limit with processor sharing, in continuous time.
- **Dynamic job priority.** The priority of a job changes while it waits. EDF gives each job one priority for its whole life; this is why EDF switches less.
- **Early warning.** A negative laxity shows that a job will miss its deadline, at the first moment when this is certain. EDF finds a miss only at the deadline.
- **Needs the remaining work.** The rule uses the remaining execution time of each job, which a real system knows only as the bound $C_i$ minus the time used. EDF needs only the deadlines.
- **Same tests as EDF.** On one processor, LLF and EDF are both optimal, so a task set is schedulable by LLF exactly when $U \le 1$ for implicit deadlines, or when the processor demand test holds.

## Variants and improvements

- **Sticky ties.** Keep the running job when the laxities tie, as in line L5. It is still optimal.
- **Laxity thresholds.** Switch only when another job's laxity is lower by more than a margin. This reduces preemptions further, but it changes the rule, and the optimality proof no longer applies.
- **Hybrids.** Run EDF while all laxities are large, and switch to LLF when a laxity reaches 0. This keeps the few preemptions of EDF in normal operation.
- **Continuous time.** The fluid version runs all jobs of equal least laxity at equal shares of the processor. It is the limit of LLF with ever smaller slots.

## When to use it

Use LLF in a simulation, in an offline schedule builder, or as a check of urgency in an admission controller, where switches cost nothing and an early warning of a miss helps. On a real processor, prefer [EDF](/earliest-deadline-first/): it has the same optimality on one processor, it needs no estimates of remaining work, and it preempts far less.

## Pitfalls

- **Thrashing.** Two jobs with close laxities switch every slot. With a context switch cost, the extra overhead can cause misses that the model does not show.
- **Slot size.** A smaller slot gives a finer schedule and more switches. The optimality holds for the slots of the model, with integer data in units of a slot.
- **Ties without a rule.** Without a fixed tie rule, the schedule is not deterministic, and two runs of the same input can differ.
- **Remaining work is an estimate.** If a job's real run time is less than its bound $C$, its true laxity is larger than the one the scheduler uses, and the scheduler may switch for no reason.

## Implementations

## History

Mok (1983) studied the least laxity rule in his MIT thesis on the design of hard real-time systems, and proved it optimal on one processor, as Dertouzos (1974) had done for the earliest deadline rule. The thrashing of LLF, with its many context switches, is the main reason why real-time kernels use EDF instead, and why later work proposed variants with thresholds or hybrids with EDF.

## References
