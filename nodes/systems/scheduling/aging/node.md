---
tag: 1CN15A
kind: technique
slug: aging
name: Aging
aliases:
- priority aging
- aging of priorities
area: systems/scheduling
level: intro
summary: "Raise the priority of a process for each period it waits, so that a low-priority process reaches the top after a bounded wait and cannot starve."
prereqs: [priority-scheduling, starvation]
see_also: [multilevel-feedback-queue, shortest-job-first, priority-inversion, lottery-scheduling, completely-fair-scheduler, round-robin, fixed-priority-scheduling]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.4 (starvation of low-priority processes and aging as its solution, with priorities from 127 down to 0)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 8, Section 8.3 (the priority boost, which moves all jobs to the top queue after each period S to avoid starvation)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.2 (shortest process next, where the weighted average of measured bursts is also called aging)
---

Aging is a technique that prevents [starvation](/starvation/) in [priority scheduling](/priority-scheduling/) by raising the priority of a process as it waits. A process of low base priority that waits long enough reaches the highest priority, and from then on only a bounded amount of work can go before it. So its wait no longer depends on how much high-priority work arrives after it. The rule that this page uses is: a process of base priority $\pi$ that has waited $w$ time units has the effective priority $\max(0, \pi - \lfloor w / A \rfloor)$, where 0 is the highest priority and $A$ is the aging period.

## In plain words

Imagine a queue at a help desk where urgent cases go first. A person with a small problem might wait all day if urgent cases keep coming. A fair rule is to move a person one step up for every hour they wait. After a few hours, the person with the small problem is as urgent as anyone, and gets served soon after.

Aging works like this. The scheduler counts how long each program has waited. For every fixed period of waiting, the program's priority goes up by one step. A program that waits long enough reaches the top priority, and then it is served before every program that came after it. So no program waits forever.

## When it applies

- A scheduler picks work by priority, and the priorities can stay unequal for a long time, so some work can starve. This is the case for static [priority scheduling](/priority-scheduling/), for [shortest-job-first](/shortest-job-first/) when short bursts keep arriving, and for lock or queue managers that favor some requests.
- The system needs a bound on the wait of every process, or at least a guarantee that each process eventually runs, but still wants high-priority work to go first in normal load.
- Waiting time can be measured, or at least counted in clock ticks.

Aging does not apply when the priorities are part of a correctness argument that must not change. In a [fixed-priority](/fixed-priority-scheduling/) real-time system, the schedulability test assumes fixed priorities, and aging a low-priority task can make a high-priority task miss its deadline.

## The template

At each decision, the scheduler computes the effective priority of each ready process from its base priority and its waiting time, and takes the least, with ties broken by the time the process became ready.

```pseudo id=main
AGED-CHOICE(R, t, A)                ▷ R: the ready processes, t: now, A: the aging period
1  for each process i in R do
2      w ← t − r[i]                  ▷ r[i]: the time i last became ready
3      e[i] ← max(0, π[i] − ⌊w / A⌋)   ▷ one level higher for each full period of waiting
4  return the i in R with the least (e[i], r[i], i)
```

After the process runs, $r[i]$ is reset to the time it next becomes ready, so its priority starts again from $\pi[i]$. With nonpreemptive scheduling and a single burst per process, $r[i]$ is the arrival time.

**The bound.** Let process $i$ have base priority $\pi_i$ and become ready at $r_i$. At time $r_i + \pi_i A$ its effective priority is 0, the highest. After that moment, a process $j$ can be dispatched before $i$ only if its key $(0, r_j, j)$ is less than $(0, r_i, i)$, so only if it became ready before $i$. Each such process runs at most once before $i$ in the nonpreemptive case, and one more process may be running at the moment $i$ reaches priority 0. So the wait of $i$ is at most

$$W_i \le \pi_i A + b_{\max} + \sum_{j \,:\, (r_j, j) < (r_i, i)} b_j,$$

where $b_j$ are the bursts and $b_{\max}$ is the largest one. The right side depends only on the processes that became ready before $i$, not on the stream of later arrivals. Without aging there is no such bound.

## Classic examples

**A low-priority process and a stream.** A process L of priority 5 and burst 3 arrives at time 1. Processes of priority 0 and burst 2 arrive at times $0, 2, 4, \ldots$ and keep the CPU busy. Scheduling is nonpreemptive and the aging period is $A = 4$.

| dispatch time | 2 | 6 | 10 | 14 | 18 | 22 |
|---|---|---|---|---|---|---|
| wait of L | 1 | 5 | 9 | 13 | 17 | 21 |
| effective priority of L | 5 | 4 | 3 | 2 | 1 | 0 |
| runs | stream | stream | stream | stream | stream | L |

At time 22, L has priority 0 and arrived at time 1, before the stream process that arrived at 22, so L runs on $[22, 25)$. Its wait of 21 is within the bound $5 \cdot 4 + 3 + 2 = 25$. Without aging, L runs only after the last process of the stream: with 1000 stream processes, at time 2000. With aging, L starts at 22 however long the stream is.

**The textbook scale.** Silberschatz, Galvin and Gagne use priorities from 127 (lowest) down to 0 (highest) and raise the priority of a waiting process by 1 at a fixed interval. With an interval of 15 minutes, a process of priority 127 reaches priority 0 after $127 \cdot 15 = 1905$ minutes, a little under 32 hours.

**The priority boost of the multilevel feedback queue.** In the [multilevel feedback queue](/multilevel-feedback-queue/), a job that uses its full quantum moves down a level. To stop the jobs at the bottom from starving, the scheduler moves all jobs to the top queue every $S$ time units (OSTEP, Chapter 8, rule 5). This is aging in one step: the jump is to the top, and it happens for all jobs at once.

**Highest response ratio next.** For [shortest-job-first](/shortest-job-first/), the priority $(w + b)/b$, the response ratio, grows with the waiting time $w$ and falls with the burst $b$. Short bursts still go first, but a long burst gains priority as it waits, so it cannot starve.

**Decay of CPU usage.** Some Unix schedulers compute the priority from the recent CPU usage of a process and decay that usage over time. A process that waits uses no CPU, so its usage decays and its priority rises. The effect is aging, with a geometric rather than a linear rule.

## Variations

- **Linear aging per period**, as in the template: one level per period $A$. It is easy to analyze and gives the bound above.
- **Continuous aging.** Drop the floor and the cut at 0, and use the effective priority $\pi_i - (t - r_i)/A$. At every time $t$ this orders the processes as the fixed value $\pi_i A + r_i$ does, so a heap keyed by $\pi_i A + r_i$ never goes out of date. The value is a virtual deadline, and the rule is an earliest-deadline order. Only processes with $\pi_j A + r_j \le \pi_i A + r_i$ can go before $i$, apart from the one running, so the wait of $i$ depends only on the processes that become ready by time $r_i + \pi_i A$.
- **Periodic sweep.** Every $A$ time units, the scheduler raises the priority of every waiting process by one level, for example by moving it to the next queue of an array of level queues. This avoids a scan at each decision. The steps happen at the ticks of a global clock, not $A$ units after each process arrived, so the wait before each step can be shorter than $A$, but not longer.
- **Boost to the top.** All waiting processes, or all processes, jump to the highest level at fixed times, as in the priority boost of the multilevel feedback queue.
- **Aging with preemption.** If aged priorities can preempt, a process that has aged to the top can preempt the running one. Reset the age of the running process when it runs, or it will be preempted at once by its own former victims, and the system thrashes.
- **Aging of locks and requests.** The same rule prevents starvation in lock managers, disk schedulers and network queues, wherever requests are served by priority.
- **Proportional share instead of priorities.** [Lottery scheduling](/lottery-scheduling/), [stride scheduling](/stride-scheduling/) and the [completely fair scheduler](/completely-fair-scheduler/) give every process a share of the CPU in proportion to its weight. They do not starve any process, so they do not need aging.

## Pitfalls

- **The word "aging" has a second meaning.** Tanenbaum and Bos use "aging" for the weighted average of measured bursts that predicts the next burst in shortest process next. That is the [exponential moving average](/exponential-moving-average/) of [shortest-job-first](/shortest-job-first/), not the priority rule of this page.
- **A period that is too short.** If $A$ is small, every process soon reaches the top priority, the priorities lose their meaning, and the scheduler behaves like FCFS.
- **A period that is too long.** The bound grows with $\pi_i A$. A long period prevents starvation in principle but still allows waits that users see as starvation.
- **Stale heap keys.** The effective priority changes with time, so a [binary heap](/binary-heap/) keyed by the priority at insertion goes out of date. Recompute at each decision, use level queues with a periodic sweep, or use continuous aging, whose order never changes (see Variations).
- **Forgetting to reset.** If the age is not reset when a process runs, its priority stays high, and it can starve the others.
- **Real-time tasks.** Aging changes the priority order, so it breaks the assumptions of [rate-monotonic scheduling](/rate-monotonic-scheduling/) and other fixed-priority analyses.

## Exercises

1. In the stream example, change the aging period to $A = 1$ and to $A = 10$. When does L start in each case? Check the answers against the bound.
2. Show that if all processes have the same base priority, aging with the template rule gives [FCFS](/fcfs-scheduling/).
3. With the periodic sweep at times $A, 2A, 3A, \ldots$, give the exact time at which a process that became ready at time $r$ reaches priority 0.

## References
