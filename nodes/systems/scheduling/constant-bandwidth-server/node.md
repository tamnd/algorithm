---
tag: P5NM45
kind: algorithm
slug: constant-bandwidth-server
name: Constant bandwidth server
aliases:
- CBS
area: systems/scheduling
level: research
summary: "An EDF server with budget Q and period T that gives its jobs deadlines and moves the deadline when the budget is spent, so an overrun never takes more than Q/T of the processor."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of hard tasks, m: the number of servers, k: the number of soft jobs, h: the number of simulated time units}
  time: {worst: O((n + m + k) h)}
  space: {extra: O(n + m + k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Luca Abeni, Giorgio Buttazzo]
  note: Abeni and Buttazzo defined the constant bandwidth server at the IEEE Real-Time Systems Symposium in 1998, to run multimedia tasks of unknown cost next to hard tasks under EDF.
prereqs: [earliest-deadline-first, utilization]
see_also: [earliest-deadline-first, edf-optimality, sporadic-server, deferrable-server, generalized-processor-sharing, stride-scheduling, real-time-scheduling, schedulability-analysis]
sources:
  - paper: doi:10.1109/REAL.1998.739726
    title: "Luca Abeni and Giorgio Buttazzo, Integrating multimedia applications in hard real-time systems, Proceedings of the 19th IEEE Real-Time Systems Symposium (1998), 4-13"
    locator: Section 3.1 (the rules of the server), Figure 1 (the example), Figure 3 (the algorithm), Lemma 1 and Theorem 1 (isolation)
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 6 (dynamic priority servers), the constant bandwidth server
---

The constant bandwidth server runs soft jobs of unknown cost next to hard tasks under [earliest deadline first](/earliest-deadline-first/) scheduling. Each server has a budget $Q$ and a period $T$, and gives its jobs a deadline $d$. When the budget is spent, it gets a new budget and moves its deadline one period later, so a job that runs too long only loses priority and cannot take more than $Q/T$ of the processor. Abeni and Buttazzo proved in 1998 that if the [utilizations](/utilization/) of the hard tasks and the bandwidths $Q/T$ of the servers add up to at most 1, no hard task misses a deadline, whatever the soft jobs do.

## In plain words

A shared kitchen has a rule: each cook may use the stove for 2 hours in every 7 hours, and the cook whose deadline is first goes next. A slow cook who needs 12 hours does not get them in a row. After each 2 hours the cook's deadline moves 7 hours later, so the others, with earlier deadlines, cook first.

The slow cook still gets a fair share and finishes in the end. The other cooks never lose their own share because of the slow cook. A cook who comes back after a long break gets a fresh deadline, but a cook who just used up the share cannot reset it by stepping out for a moment.

## The problem

One processor runs [periodic](/periodic-task-model/) hard tasks $\tau_i = (C_i, T_i)$ with deadlines equal to periods under EDF, and these must meet all deadlines. Soft tasks also run, such as video or audio decoders, whose jobs arrive at unknown times and whose costs are not known or have a worst case that is far above the usual case. If a soft job runs as a plain EDF job with a guessed cost and it overruns, the hard tasks can miss. The goal is *temporal isolation*: give each soft task a share $U_s$ of the processor so that the hard tasks pass their test with the shares as if the soft tasks were periodic, and an overrun only delays the task that overruns.

## The algorithm

Each server has a budget $Q$, a period $T$, its bandwidth $U = Q/T$, a current budget $c$ and a current deadline $d$, both 0 at the start. It serves its jobs first come, first served. Hard jobs have their own fixed deadlines.

```pseudo id=main
CONSTANT-BANDWIDTH-SERVER(hard tasks, servers)
L1  for t ← 0, 1, 2, ... do
L2      release the hard jobs due at t, each with the deadline t + Ti
L3      for each soft job that arrives at t: if the queue of its server is empty then
L4          if c ≥ (d − t) · Q / T then                     ▷ the old deadline would give too much bandwidth
L5              d ← t + T; c ← Q                            ▷ else keep c and d; then append the job to the queue
L6      run the ready hard job or server with the earliest deadline, a hard job first on a tie
L7      if a server ran then c ← c − 1 and the head of its queue gets one unit
L8          if c = 0 then c ← Q; d ← d + T                  ▷ recharge and postpone
```

Line L8 is the heart of the server: a job that has used the budget is not stopped, but its deadline moves one period later, so EDF lets other work go first. Lines L4 and L5 handle a server that wakes up after an idle time. If the remaining budget at the old deadline would need more than the bandwidth $U$, the server gets a fresh deadline and budget; otherwise it keeps them, so that it cannot gain bandwidth by going idle and coming back.

## Example

This is Figure 1 of Abeni and Buttazzo, and a test of the implementation. A hard task $(2, 3)$ shares the processor with a server $Q = 2$, $T = 7$. Soft jobs arrive at time 2 (3 units), 7 (2 units) and 17 (1 unit). The total utilization is $2/3 + 2/7 < 1$.

| time | event | $c$ | $d$ |
|---|---|---|---|
| 2 | first job arrives, queue empty, $0 \ge (0 - 2) \cdot 2/7$: new | 2 | 9 |
| 2, 5 | server runs in slots 2 and 5; budget spent at 6: recharge | 2 | 16 |
| 7 | second job arrives and waits in the queue | 2 | 16 |
| 8 | server runs; first job ends at 9 | 1 | 16 |
| 11 | server runs; budget spent at 12: recharge | 2 | 23 |
| 14 | server runs; second job ends at 15 | 1 | 23 |
| 17 | third job arrives, queue empty, $1 < (23 - 17) \cdot 2/7$: keep | 1 | 23 |
| 17 | server runs; recharge at 18; third job ends at 18 | 2 | 30 |

The hard task runs in all other slots up to 19 and meets every deadline. At time 17 the server keeps the deadline 23. It has run 5 units since time 2. With a new deadline $17 + 7 = 24$ and a full budget, it could run 2 more by 24, so 7 units in the 22 slots from 2 to 24. That is more than its share $22 \cdot 2/7 \approx 6.3$.

**An overrun.** With the same hard task and server, one soft job of 12 units arrives at 0. Run as a plain EDF job with the deadline $0 + 7$, it takes slot 2 and slots 5 to 15, and the hard jobs released at 6, 9 and 12 miss. Under the server, it runs only in slots 2, 5, 8, 11, ..., two slots for each of the deadlines 7, 14, 21, ..., and the hard task misses nothing.

## Correctness

Fix a server and an arrival at $r$ that finds its queue empty. From then on, the work $W$ of the server since $r$ satisfies $W + c \le (d - r)U$: a new event starts it with equality, running moves one unit from $c$ to $W$, a recharge adds $Q = TU$ to both sides, and the test of line L4 is exactly what keeps it true when a new deadline is set. Deadlines never decrease. Now take a hard job that misses its deadline $t_2$ and the longest interval $[t_1, t_2)$ in which every slot runs work with deadline at most $t_2$. The hard tasks need at most $(t_2 - t_1)\sum_i C_i/T_i$ in it. By the invariant, each server runs at most $(t_2 - t_1)U$ in it. So $t_2 - t_1 < (t_2 - t_1) \cdot (\text{total}) \le t_2 - t_1$, which is false. The test $\sum_i C_i/T_i + \sum_s U_s \le 1$ is the EDF test with each server in the place of a periodic task $(Q, T)$, and the full proof is in the proofs folder.

## Complexity

- **Simulation.** Each time unit scans the $n$ hard jobs, the $m$ servers and the $k$ soft jobs for arrivals, so a run of $h$ units takes $O((n + m + k) h)$ time and $O(n + m + k)$ extra space.
- **In a kernel.** Each rule is $O(1)$ arithmetic on $c$ and $d$, plus one update of the EDF ready queue, which is $O(\log n)$ with a heap. A timer fires when the budget of the running server reaches 0.
- **Admission.** A new server is accepted if the sum of all bandwidths stays at most 1, which is $O(1)$ with a running sum.

## Properties

- **Isolation.** The guarantee holds whatever the soft jobs do, as the proof uses only the server rules. An overrun hurts only the server that overruns.
- **Hard tasks in servers.** Abeni and Buttazzo show that a hard task $(C, T)$ served by its own server with $Q \ge C$ and period $T$ meets all its deadlines. So all tasks can run in servers, and the system needs no separate hard class.
- **Work conserving.** The server never stops a job for lack of budget; it recharges at once and only postpones the deadline. So the processor is never idle while work waits, but a server can get more than its share when others are idle.
- **Soft guarantee.** The same argument shows that, with total bandwidth at most 1, each server spends each budget by its deadline. So a soft job of demand $x$ that arrives at $r$, gets a new deadline and is first in the queue ends by $r + \lceil x / Q \rceil T$.
- **No gain from idling.** The test of line L4 stops a server from getting a fresh budget by going idle and coming back early.

## Variants and improvements

- **Hard reservations.** A server that has spent its budget is suspended until its deadline instead of being recharged at once. It then never runs more than $Q$ in a period, at the cost of idle time.
- **Bandwidth reclaiming.** GRUB and similar algorithms let servers use the bandwidth that idle servers leave, while they keep the isolation of the others.
- **Total bandwidth server.** The total bandwidth server of Spuri and Buttazzo gives each aperiodic job the deadline $\max(r, d_{prev}) + x / U$, which needs the cost $x$ in advance. The constant bandwidth server needs no cost and is safe when the cost is wrong.
- **Multiprocessor and hierarchical forms.** Servers can be placed on several processors, and a server can hold a whole scheduler of its own, as in hierarchical scheduling.

## When to use it

Use it under EDF when some tasks have unknown or highly variable costs and others need hard guarantees, for example multimedia next to control, or several applications that share one processor and must not disturb each other. Give each such task the bandwidth it needs most of the time, and let the server absorb the peaks. With fixed priorities instead of EDF, the [sporadic server](/sporadic-server/) plays the same role.

## Pitfalls

- **Always taking a new deadline.** If line L4 is left out and every wake-up sets $d \leftarrow t + T$ and $c \leftarrow Q$, a server that idles for a moment gets a fresh budget with an early deadline, and it can take more than its bandwidth. In the example, at time 17 the server would get 2 units with the deadline 24 instead of 1 unit with the deadline 23.
- **Recharging without postponing.** If line L8 refills $c$ but keeps $d$, an overrun keeps its early deadline and runs ahead of the hard jobs, which is the plain EDF failure.
- **Admitting too much.** The guarantee needs $\sum_i C_i/T_i + \sum_s U_s \le 1$. Servers whose bandwidths are chosen without this check lose the isolation.
- **Exact arithmetic.** The test of line L4 compares a budget with a product of real numbers. Use the integer form $cT \ge (d - t)Q$ or exact fractions; a rounding error that makes the test true too often is the first pitfall again.

## Implementations

## History

Abeni and Buttazzo presented the constant bandwidth server at the IEEE Real-Time Systems Symposium in 1998, to run multimedia applications with unknown costs next to hard tasks. It builds on the total bandwidth server of Spuri and Buttazzo and on the idea of processor reservations, and many later servers for EDF, such as bandwidth reclaiming and hierarchical servers, extend it. The Linux scheduling class SCHED_DEADLINE uses a constant bandwidth server for each task.

## References
