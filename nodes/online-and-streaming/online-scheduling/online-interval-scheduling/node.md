---
tag: Z286P0
kind: problem
slug: online-interval-scheduling
name: Online interval scheduling
aliases:
- online interval selection
area: online-and-streaming/online-scheduling
level: advanced
summary: Intervals arrive online; accept or reject each to maximize the number or weight of accepted, non-overlapping intervals.
prereqs: [activity-selection, online-algorithm, competitive-ratio]
see_also: [earliest-finish-time-first, weighted-interval-scheduling, online-throughput-maximization, online-admission-control, online-independent-set-problem, randomized-online-algorithm, k-machine-interval-scheduling, deadline]
sources:
  - paper: "Richard J. Lipton and Andrew Tomkins, Online interval scheduling, SODA 1994"
    locator: pages 302 to 311 (value equal to length, no abort, randomized algorithms with ratio about log Delta and the matching Omega(log Delta) lower bound)
  - paper: doi:10.1016/0304-3975(94)90150-3
    title: Gerhard J. Woeginger, On-line scheduling of jobs with fixed start and end times, Theoretical Computer Science 130(1), 1994
    locator: pages 5 to 16 (intervals with abort, a 4-competitive deterministic algorithm for weights that are suitable functions of the length, the matching lower bound 4, and no constant ratio for arbitrary weights)
  - paper: "Ulrich Faigle and Willem M. Nawijn, Note on scheduling intervals on-line, Discrete Applied Mathematics 58(1), 1995"
    locator: pages 13 to 17 (with abort, the greedy rule that keeps the interval with the earliest end is optimal for the number of intervals)
  - paper: "Jiří Sgall, On-line scheduling, in Amos Fiat and Gerhard J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: Section 6 (online scheduling with rejection and interval models)
---

Online interval scheduling is the problem in which intervals of time arrive one at a time, in order of their start times, and an online algorithm must accept or reject each interval when it arrives, so that the accepted intervals do not overlap and their number or total weight is large. It is the online form of [activity selection](/activity-selection/) and of [weighted interval scheduling](/weighted-interval-scheduling/). The answer depends strongly on the model. If the algorithm may abort an accepted interval, the greedy rule that keeps the interval with the earliest end is optimal for the number of intervals (Faigle and Nawijn 1995), and a doubling rule is 4-competitive for weights that grow with the length (Woeginger 1994). Without abort, no deterministic algorithm has a bounded ratio for the count, and with weight equal to length the best randomized ratio is $\Theta(\log \Delta)$ (Lipton and Tomkins 1994).

## In plain words

Requests to use one room come in. Each request is for a fixed time slot, from a start time to an end time, and the requests come in the order of their start times. The manager must say yes or no to each request when it comes, and two accepted slots must not overlap.

If the goal is to accept many requests, and the manager may cancel an accepted request that has not finished, a simple rule is best: when two requests conflict, keep the one that ends first. If cancelling is not allowed, the manager can be trapped: after a long request is accepted, many short requests come that all overlap it. If each request is worth its length, the trap goes the other way, and then random choices help.

## Definition

**Input.** A sequence $\sigma$ of $n$ half-open intervals $I_j = [s_j, e_j)$ with $s_j < e_j$, in the order of arrival, which is the order of the start times. Each interval has a weight $w_j > 0$. The interval $I_j$ and its weight become known at time $s_j$.

**Decisions.** When $I_j$ arrives, the algorithm accepts or rejects it, and a rejection is final. The accepted intervals that are still running must be pairwise disjoint.

**Models.**

- *No abort.* An accepted interval must run to its end. So the algorithm can accept $I_j$ only if the machine is free at $s_j$.
- *With abort* (also called preemption). The algorithm may abort the running interval at any time, to accept a new one. An aborted interval gives no value.

**Objective.** Maximize the total weight of the intervals that run to their end. Common weights are $w_j = 1$ (the count), $w_j = e_j - s_j$ (the length), and arbitrary weights.

**Notation.** ALG$(\sigma)$ and OPT$(\sigma)$ are the total weight of the online algorithm and of the best set of disjoint intervals. For this maximization problem, an algorithm is $c$-competitive if OPT$(\sigma) \le c \cdot$ ALG$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. For a [randomized](/randomized-online-algorithm/) algorithm, OPT$(\sigma) \le c \cdot \mathbb{E}[\text{ALG}(\sigma)]$ against an [oblivious adversary](/oblivious-adversary/). Let $\Delta$ be the ratio of the longest to the shortest interval length.

## Variants

- **Arrival order.** In the standard model the intervals arrive in order of start time, so time runs forward. If intervals arrive in arbitrary order, the problem is the [online independent set](/online-independent-set-problem/) problem on interval graphs, and it is also the one-edge case of [online admission control](/online-admission-control/).
- **Several machines.** With $k$ machines, up to $k$ accepted intervals may overlap at each time. The offline version is [$k$-machine interval scheduling](/k-machine-interval-scheduling/).
- **Jobs with slack.** If a job may run anywhere inside a window larger than its length, the problem is [online throughput maximization](/online-throughput-maximization/). Interval scheduling is the case of zero slack, where each job must start at its release time.

## Examples

Take the intervals $[0, 10)$, $[1, 3)$, $[2, 4)$, $[4, 6)$, $[5, 7)$ and $[7, 9)$, in this order of arrival.

| rule | accepted and completed | count | total length |
|---|---|---|---|
| greedy, no abort | $[0, 10)$ | 1 | 10 |
| earliest end, with abort | $[1, 3)$, $[4, 6)$, $[7, 9)$ | 3 | 6 |
| best for the count, offline | $[1, 3)$, $[4, 6)$, $[7, 9)$ | 3 | 6 |
| best for the length, offline | $[0, 10)$ | 1 | 10 |

With abort, the earliest end rule first takes $[0, 10)$, aborts it at time 1 for $[1, 3)$, which ends sooner, and rejects $[2, 4)$, which ends later. At time 4 the interval $[1, 3)$ has completed, so it takes $[4, 6)$, and so on. Greedy without abort is trapped by the long interval when the goal is the count, but it is optimal here when the goal is the length.

## Known algorithms

**Earliest end with abort, unit weights.** When $I_j$ arrives, first record the running interval as complete if it has ended by $s_j$. If the machine is free, accept $I_j$. Otherwise keep whichever of the running interval and $I_j$ ends first, and abort or reject the other.

*Theorem (Faigle and Nawijn 1995).* For $w_j = 1$ and intervals in order of start time, this rule is optimal: ALG$(\sigma) = $ OPT$(\sigma)$.

*Proof.* Let $c$ be the end of the last interval that the rule has completed, with $c = -\infty$ at the start. We claim that the running interval is always one with the smallest end among the intervals that have arrived and start at $c$ or later. When the running interval ends at time $c$ and the next arrival $I_j$ has $s_j \ge c$, no earlier arrival starts at $c$ or later, since its arrival would have recorded the completion. So $I_j$ is the only candidate, and the rule takes it. Otherwise the rule keeps the smaller end of two candidates, so the claim holds by induction. An interval that arrives after the running interval ends has its end after that time, so it cannot have a smaller end. Hence each completed interval has the smallest end among all intervals that start at or after the previous completion. This is exactly the offline [earliest finish time first](/earliest-finish-time-first/) rule, which is optimal for [activity selection](/activity-selection/). $\square$

**Greedy without abort.** Accept $I_j$ if the machine is free at $s_j$.

*Theorem.* For $w_j = e_j - s_j$, greedy without abort is $(1 + \Delta)$-competitive.

*Proof.* Charge each interval $J$ of an optimal set to the greedy interval that runs at time $s_J$. Such an interval exists: either greedy accepted $J$, or greedy rejected it because it was busy at $s_J$. The optimal intervals charged to one greedy interval $I$ are disjoint and start inside $[s_I, e_I)$, so their total length is at most $(e_I - s_I)$ plus the length of the last one, which is at most $\Delta (e_I - s_I)$. Summing over $I$ gives OPT $\le (1 + \Delta)$ ALG. $\square$

**Doubling with abort (Woeginger 1994).** Replace the running interval by a new one only if the new weight is at least twice the current weight. For weights that are suitable functions of the length, including $w_j = e_j - s_j$, this rule is 4-competitive. This result is cited here and not proved.

**Randomized algorithms without abort (Lipton and Tomkins 1994).** For $w_j = e_j - s_j$, pick a random length class $[2^i, 2^{i+1})$ and accept greedily only intervals of that class. This gives ratio $O(\log \Delta)$ against an oblivious adversary when $\Delta$ is known. Lipton and Tomkins refine it to about $O((\log \Delta)^{1 + \varepsilon})$ when $\Delta$ is not known, and prove that no randomized algorithm is better than $\Omega(\log \Delta)$. These results are cited here and not proved.

## Bounds

**Theorem.** Without abort, no deterministic algorithm has a bounded ratio for $w_j = 1$, and no deterministic algorithm is better than $\Delta$-competitive for $w_j = e_j - s_j$.

*Proof.* The adversary releases $[0, L)$. If the algorithm rejects it, no more intervals come, ALG $= 0$ and OPT $> 0$. Otherwise the machine is busy on $[0, L)$. For the count, the adversary then releases $n - 1$ disjoint short intervals inside $(0, L)$; ALG $= 1$ and OPT $= n - 1$. For the length, with $L = 1$, it releases one interval $[\varepsilon, \varepsilon + \Delta)$; ALG $= 1$ and OPT $= \Delta$. $\square$

| model | weights | bound | proved here or cited |
|---|---|---|---|
| with abort, deterministic | count | 1, optimal | proved above |
| no abort, deterministic | count | unbounded | proved above |
| no abort, deterministic | length | between $\Delta$ and $1 + \Delta$ | proved above |
| no abort, randomized, oblivious adversary | length | $\Theta(\log \Delta)$ for known $\Delta$ | cited, Lipton and Tomkins |
| with abort, deterministic | length | 4, tight | cited, Woeginger |
| with abort, deterministic | arbitrary | no constant ratio | cited, Woeginger |

## Reductions

- **Offline.** With all intervals known, the count is solved by [activity selection](/activity-selection/) and arbitrary weights by [weighted interval scheduling](/weighted-interval-scheduling/) in $O(n \log n)$ time.
- **To throughput maximization.** A job with $d_j = r_j + p_j$ must start at its release time, so it is the interval $[r_j, d_j)$. With preemption, an interrupted job with zero slack can never finish, so preemption is abort. Thus interval scheduling with abort is the zero-slack case of [online throughput maximization](/online-throughput-maximization/).
- **To admission control.** An interval is a request for one unit of bandwidth on the edges of a path, and the line of time is a path with capacity 1. See [online admission control](/online-admission-control/).

## Applications

Reservation systems for rooms, vehicles and machines; the acceptance of calls with a fixed start and end; and real-time systems in which a task must run at a fixed time or not at all.

## References
