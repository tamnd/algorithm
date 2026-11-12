---
tag: AT2YH5
kind: concept
slug: schedulability-analysis
name: Schedulability analysis
aliases:
- schedulability test
area: systems/scheduling
level: advanced
summary: "Decide before a system runs that a set of real-time tasks meets all deadlines under a given policy, with tests that are sufficient, necessary or exact."
prereqs: [periodic-task-model, rate-monotonic-scheduling, earliest-deadline-first]
see_also: [real-time-scheduling, liu-layland-utilization-bound, response-time-analysis, edf-optimality, deadline-monotonic-scheduling, fixed-priority-scheduling, hyperperiod, sporadic-task-model]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the utilization tests for the rate-monotonic and the deadline driven algorithms, and the critical instant
  - paper: doi:10.1007/BF01995675
    title: "Sanjoy K. Baruah, Louis E. Rosier and Rodney R. Howell, Algorithms and complexity concerning the preemptive scheduling of periodic, real-time tasks on one processor, Real-Time Systems 2(4) (1990), 301-324"
    locator: the processor demand test, its pseudo-polynomial bound, and the strong coNP-completeness of feasibility for tasks with offsets
  - paper: "Mathai Joseph and Paritosh Pandya, Finding response times in a real-time system, The Computer Journal 29(5) (1986), 390-395"
    locator: the response time of a task under preemptive fixed priorities as the least solution of a recurrence
  - paper: "Neil C. Audsley, Optimal priority assignment and feasibility of static priority tasks with arbitrary start times, Technical Report YCS 164, Department of Computer Science, University of York, 1991"
    locator: the priority assignment from the lowest level up, and its optimality
  - paper: "John P. Lehoczky, Fixed priority scheduling of periodic task sets with arbitrary deadlines, Proceedings of the 11th IEEE Real-Time Systems Symposium, 1990"
    locator: the analysis of a level-i busy period with several jobs of a task, for deadlines after the periods
  - paper: "Neil C. Audsley, Alan Burns, Mike F. Richardson, Ken Tindell and Andy J. Wellings, Applying new scheduling theory to static priority pre-emptive scheduling, Software Engineering Journal 8(5) (1993), 284-292"
    locator: response-time analysis for deadline-monotonic priorities, with blocking and jitter
  - paper: "Sanjoy Baruah and Alan Burns, Sustainable scheduling analysis, Proceedings of the 27th IEEE Real-Time Systems Symposium, 2006"
    locator: the definition of a sustainable test and the sustainability of the standard uniprocessor tests
  - paper: doi:10.1109/RTSS.2008.25
    title: "Friedrich Eisenbrand and Thomas Rothvoß, Static-priority real-time scheduling: response time computation is NP-hard, Proceedings of the 29th IEEE Real-Time Systems Symposium, 2008"
    locator: the main theorem (NP-hardness of computing the worst-case response time under fixed priorities)
  - paper: doi:10.1137/1.9781611973075.83
    title: "Friedrich Eisenbrand and Thomas Rothvoß, EDF-schedulability of synchronous periodic task systems is coNP-hard, SODA 2010, 1029-1034"
    locator: the main theorem (weak coNP-hardness for constrained deadlines and synchronous release)
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (utilization tests, response time analysis and the processor demand approach)
---

Schedulability analysis is the work of deciding, before a [real-time](/real-time-scheduling/) system runs, whether a set of recurring tasks meets every deadline under a given scheduling policy. A *schedulability test* takes the task parameters, such as the worst-case execution times, the periods and the relative deadlines, and returns yes or no. A test is *exact* if it accepts exactly the task sets that the policy schedules, and *sufficient* if each set it accepts is schedulable but some schedulable sets fail it. Fast sufficient tests, such as the [Liu-Layland bound](/liu-layland-utilization-bound/), and slower exact tests, such as [response-time analysis](/response-time-analysis/), are used side by side.

## In plain words

A machine must do several jobs again and again, and each job has a due time. Before you switch the machine on, you want proof that no job will ever be late. A few test runs are not enough, because the bad case may be one that you did not try. Schedulability analysis gives this proof for every way in which the jobs can arrive.

It works with the worst case of each job: the longest time it can take and the most often it can arrive. Some checks are quick but careful: when they say yes, the answer is yes, but they sometimes say no to a set that would be fine. Other checks take more work, but they are always right. Engineers often run a quick check first, and the exact one only when the quick one says no.

## The idea

**Feasible and schedulable.** Take a set of $n$ tasks $\tau_i = (C_i, T_i, D_i)$ on one processor, [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/), with worst-case execution time $C_i$, period or least gap between releases $T_i$, and relative deadline $D_i$. The set is *feasible* if, for each release pattern that the model allows, some schedule meets all deadlines. It is *schedulable by* a policy $A$ if $A$ meets all deadlines for each allowed release pattern and each run time of at most $C_i$. A test for $A$ is *sufficient* if each set it accepts is schedulable by $A$, *necessary* if each set schedulable by $A$ passes it, and *exact* if it is both. On one processor, [EDF is optimal](/edf-optimality/), so an exact test for EDF is also an exact test for feasibility.

**One worst case.** A sporadic task set has infinitely many release patterns, so a test must find one pattern that is the worst. For preemptive fixed priorities with $D_i \le T_i$, this is the *critical instant*: all tasks release a job at the same time, and then each releases as often as it can ([Liu and Layland 1973](/rate-monotonic-optimality/)). For EDF, the same synchronous release gives the largest demand in each interval, which the processor demand criterion counts with the demand bound function $h(t)$. With $D_i > T_i$, several jobs of a task can be pending at once, and the analysis must follow a whole busy period.

**The main tests.** For $U = \sum_i C_i / T_i$, the [utilization](/utilization/) of the set:

| Test | Policy | Deadlines | Kind | Time |
|---|---|---|---|---|
| $U \le 1$ | EDF | $D_i = T_i$ | exact | $O(n)$ |
| Processor demand criterion: $h(t) \le t$ at the deadlines up to a bound | EDF | $D_i \le T_i$ | exact | pseudo-polynomial if $U \le c < 1$ |
| Density: $\sum_i C_i / \min(D_i, T_i) \le 1$ | EDF | any | sufficient | $O(n)$ |
| Liu-Layland: $U \le n(2^{1/n} - 1)$ | rate-monotonic | $D_i = T_i$ | sufficient | $O(n)$ |
| Hyperbolic: $\prod_i (U_i + 1) \le 2$ | rate-monotonic | $D_i = T_i$ | sufficient | $O(n)$ |
| Response-time analysis: $R_i \le D_i$ for each $i$ | any fixed priorities | $D_i \le T_i$ | exact | pseudo-polynomial |
| Simulation over $[0, H)$ | EDF or fixed priorities, synchronous periodic | $D_i \le T_i$ | exact | linear in the number of jobs in $[0, H)$ |

The hyperbolic test accepts each set that the Liu-Layland test accepts, and some more. For deadlines after the periods, response-time analysis extends to the jobs of a level-$i$ busy period (Lehoczky 1990). For the simulation, $H$ is the [hyperperiod](/hyperperiod/), which can be exponential in $n$; for periodic tasks with offsets up to $s$, a simulation of EDF over $[0, s + 2H)$ is exact.

**How hard it is.** The simple cases are easy: $U \le 1$ decides EDF with implicit deadlines in linear time. The general cases are hard. With constrained deadlines and synchronous release, EDF schedulability is coNP-hard (Eisenbrand and Rothvoß 2010), and the processor demand criterion runs in pseudo-polynomial time only when $U$ is at most a constant below 1 (Baruah, Rosier and Howell 1990). For periodic tasks with given offsets, feasibility is coNP-complete in the [strong sense](/strong-np-hardness/) (Baruah, Rosier and Howell 1990). Under fixed priorities, computing the worst-case response time of a task is NP-hard (Eisenbrand and Rothvoß 2008), although response-time analysis is [pseudo-polynomial](/pseudo-polynomial-time/).

**Priority assignment.** Under fixed priorities, a test checks one order of priorities, and a second question is which order to check. [Rate-monotonic](/rate-monotonic-scheduling/) order is optimal for $D_i = T_i$, and [deadline-monotonic](/deadline-monotonic-scheduling/) order for $D_i \le T_i$. In other models, Audsley's optimal priority assignment (1991) builds the order from the lowest level up: it puts at the lowest free level any task that passes the test there, with all the remaining tasks above it. This works with each test in which the result for a task depends on the set of tasks above it, not on their order.

**What the model leaves out.** A test is only as good as its inputs. The $C_i$ must be safe upper bounds of the execution times, and the analysis must add the costs that the basic model ignores: context switches, the blocking of a task by a lower one that holds a shared resource (bounded by the [priority ceiling protocol](/priority-ceiling-protocol/)), and release jitter. A good test is also *sustainable* (Baruah and Burns 2006): a set that passes still meets its deadlines when a job runs for less than $C_i$, when releases come less often, or when a deadline is later. The exact tests above for preemptive scheduling of sporadic tasks on one processor are sustainable in this sense, but with non-preemptive scheduling a job that ends early can make another job miss.

## Examples

**Sufficient tests fail, the exact test passes.** Take $(C, T) = (1, 4)$, $(2, 6)$ and $(3, 12)$ with $D_i = T_i$. Then $U = 5/6 \approx 0.833$. The Liu-Layland bound for $n = 3$ is $3(2^{1/3} - 1) \approx 0.780$, and the hyperbolic product is $\tfrac54 \cdot \tfrac43 \cdot \tfrac54 = \tfrac{25}{12} > 2$, so both sufficient tests say no. Response-time analysis under rate-monotonic priorities gives $R_1 = 1$ and $R_2 = 3$, and for $\tau_3$ the iteration runs $3, 6, 7, 9, 10, 10$, so $R_3 = 10 \le 12$. The set is schedulable by rate-monotonic priorities. It is schedulable by EDF too, since $U \le 1$.

**Feasible but not rate-monotonic schedulable.** Take $(C, T) = (2, 5)$ and $(4, 7)$ with $D_i = T_i$. Then $U = 34/35 \approx 0.971 \le 1$, so EDF schedules the set. Under rate-monotonic priorities, the iteration for $\tau_2$ runs $4, 6, 8$, and $8 > 7$, so $\tau_2$ misses its deadline at the critical instant. With $n = 2$, the other order of priorities is the only other choice, and then $\tau_1$ misses its deadline: $4 + 2 = 6 > 5$.

**Constrained deadlines.** Take $(C, T, D) = (1, 4, 2)$, $(2, 6, 4)$ and $(3, 12, 9)$. The density is $\tfrac12 + \tfrac24 + \tfrac39 = \tfrac43 > 1$, so the density test says no. Under deadline-monotonic priorities, $R_1 = 1$ and $R_2 = 3$, but the iteration for $\tau_3$ runs $3, 6, 7, 9, 10$, and $10 > 9$. Since deadline-monotonic order is optimal among fixed priorities for $D_i \le T_i$, no order of fixed priorities schedules the set. The processor demand criterion accepts it: $U = 5/6$, the bound is $L_a = 11.5$, and at the deadlines $2, 4, 6, 9, 10$ the demand is $1, 3, 4, 7, 10$, never more than $t$. So EDF meets all deadlines.

**Priority assignment beyond deadline-monotonic.** Take $(C, T, D) = (2, 4, 6)$ and $(4, 8, 7)$, where the first deadline is after its period. Deadline-monotonic order puts $\tau_1$ first, and the iteration for $\tau_2$ runs $4, 6, 8$, so $8 > 7$. Audsley's assignment tries $\tau_1$ at the lowest level: its busy period has length 8 and holds two jobs, with response times 6 and 4, both at most 6. Then $\tau_2$ alone has response time 4. So the order $\tau_2$ above $\tau_1$ is schedulable, though deadline-monotonic order is not.

## Where it is used

- **Admission control.** An online system accepts a new task only if the set with the new task still passes a test. Fast tests, such as $U \le 1$ for EDF or the hyperbolic bound for rate-monotonic priorities, fit here; see [admission control](/admission-control/). Servers such as the [constant bandwidth server](/constant-bandwidth-server/) reserve a share of the processor, so a test of the shares protects the hard tasks from the others.
- **Certification.** In avionics, automotive and industrial control systems, a timing analysis is part of the evidence that a system is safe. Response-time analysis with blocking and jitter terms (Audsley, Burns, Richardson, Tindell and Wellings 1993) is the usual tool for [fixed-priority](/fixed-priority-scheduling/) systems.
- **Design.** A designer searches for periods, priorities or a mapping of tasks to processors, and calls a test for each candidate. Fast sufficient tests prune the search, and an exact test checks the final design.
- **Sensitivity.** With an exact test and a search over a scale factor, a designer finds how much each execution time can grow before a deadline is missed. This shows the margin of the system.
- **Several processors.** In partitioned scheduling, each processor runs its own uniprocessor policy, and placing the tasks is like [bin packing](/bin-packing/): a uniprocessor test, such as $U \le 1$ for EDF, decides whether a task fits on a processor, and heuristics such as [first-fit decreasing](/first-fit-decreasing/) place the tasks.

## References
