---
tag: EQDT8V
kind: problem
slug: online-throughput-maximization
name: Online throughput maximization with deadlines
aliases:
- online deadline throughput
area: online-and-streaming/online-scheduling
level: advanced
summary: Maximize the total value of jobs completed by their deadlines when jobs arrive online.
prereqs: [deadline, earliest-deadline-first, competitive-ratio]
see_also: [edf-optimality, online-interval-scheduling, packet-scheduling, real-time-scheduling, minimizing-number-of-late-jobs, job-sequencing-with-deadlines, online-admission-control, preemptive-scheduling]
sources:
  - paper: "Sanjoy Baruah, Gilad Koren, Decao Mao, Bhubaneswar Mishra, Arvind Raghunathan, Louis Rosier, Dennis Shasha and Fuxing Wang, On the competitiveness of on-line real-time task scheduling, Real-Time Systems 4(2), 1992"
    locator: pages 125 to 144 (no deterministic online algorithm is better than 4-competitive when value equals size, and (1 + sqrt k)^2 when value densities differ by a factor k)
  - paper: "Gilad Koren and Dennis Shasha, D^over, an optimal on-line scheduling algorithm for overloaded uniprocessor real-time systems, SIAM Journal on Computing 24(2), 1995"
    locator: pages 318 to 339 (an algorithm with ratio (1 + sqrt k)^2, which matches the lower bound)
  - paper: "Pavel Veselý, Marek Chrobak, Łukasz Jeż and Jiří Sgall, A phi-competitive algorithm for scheduling packets with deadlines, SODA 2019"
    locator: the deterministic ratio phi, about 1.618, for unit jobs with weights and integer deadlines, which matches the known lower bound
  - paper: "Franziska Eberle, Nicole Megow and Kevin Schewior, Optimally handling commitment issues in online throughput maximization, ESA 2020"
    locator: unit values with slack d_j - r_j at least (1 + eps) p_j, and the ratio Theta(1/eps)
  - paper: "Jiří Sgall, On-line scheduling, in Amos Fiat and Gerhard J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: Section 6 (real-time scheduling and the maximization of the value of completed jobs)
---

Online throughput maximization is the problem of scheduling jobs that arrive over time, each with a [deadline](/deadline/) and a value, so that the total value of the jobs that complete by their deadlines is large. On one machine with [preemption](/preemptive-scheduling/), [earliest deadline first](/earliest-deadline-first/) completes every job when this is possible, but it can lose everything when the machine is overloaded. When the value of a job equals its size, the best deterministic [competitive ratio](/competitive-ratio/) is exactly 4 (Baruah et al. 1992, and Koren and Shasha 1995). For unit jobs at integer times, the problem is [packet scheduling](/packet-scheduling/) with deadlines: EDF is optimal for the count, greedy by weight is 2-competitive, and the best deterministic ratio is the golden ratio.

## In plain words

Tasks arrive at a processor. Each task has a size, a deadline and a value, and it earns its value only if it finishes by its deadline. A task can be paused and resumed later. When the processor can finish all tasks, the rule "work on the task with the earliest deadline" finishes all of them. When there is too much work, some tasks must be dropped, and the choice is hard: a large task that is worth a lot may be ruined by a small task that comes later and looks urgent. An online rule does not know what comes later, so it can lose a constant factor of the value, and the theory finds that factor exactly.

## Definition

**Input.** A sequence $\sigma$ of $n$ jobs, revealed online. Job $j$ has a release time $r_j$, a processing time $p_j$, a deadline $d_j \ge r_j + p_j$ and a value $v_j > 0$, all known at time $r_j$.

**Schedule.** One machine of speed 1. Preemption is allowed, and a preempted job may resume later without loss.

**Objective.** Maximize the total value of the jobs $j$ with $C_j \le d_j$. A job that cannot meet its deadline gives nothing, so it may be dropped.

**Notation.** ALG$(\sigma)$ and OPT$(\sigma)$ are the value of the online algorithm and of the best offline schedule. An algorithm is $c$-competitive if OPT$(\sigma) \le c \cdot$ ALG$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. The value density of job $j$ is $v_j / p_j$, and $k$ is the ratio of the largest to the smallest value density.

## Variants

- **Value equal to size.** $v_j = p_j$, so $k = 1$, and the objective is the busy time spent on jobs that complete.
- **Unit values.** $v_j = 1$, so the objective is the number of jobs that complete. The offline version without release times is [minimizing the number of late jobs](/minimizing-number-of-late-jobs/).
- **Unit jobs at integer times.** $p_j = 1$ and integer $r_j$ and $d_j$; job $j$ may use a slot $t$ with $r_j \le t < d_j$. This is the bounded delay buffer model of [packet scheduling](/packet-scheduling/). The offline version is [job sequencing with deadlines](/job-sequencing-with-deadlines/).
- **Slack.** Each job has $d_j - r_j \ge (1 + \varepsilon) p_j$. The case $d_j = r_j + p_j$ without slack is [online interval scheduling](/online-interval-scheduling/) with abort.
- **Commitment.** The algorithm must decide at some point to commit to a job, and then must complete it.

## Examples

**EDF under overload.** Take $J_1 = (r, p, d, v) = (0, 10, 10, 10)$ and $J_2 = (5, 6, 9, 6)$. At time 5, EDF switches to $J_2$, because its deadline is earlier. But $J_2$ can get only 4 units of work by time 9, and then $J_1$ has only 1 unit of time for its 5 units of remaining work. Both jobs miss their deadlines, so EDF gets 0, while running $J_1$ alone gets 10. So plain EDF has no bounded ratio when the machine is overloaded. Dropping jobs that can no longer finish helps here, but the lower bound below shows that no rule avoids a loss of a factor 4.

**Unit jobs.** Take the slots $0, 1, \dots$ and two packets: $a$ with value 1, usable only in slot 0, and $b$ with value $1 + \varepsilon$, usable in slots 0 and 1. Greedy by value sends $b$ in slot 0, and $a$ expires, for a total of $1 + \varepsilon$. The optimum sends $a$ and then $b$, for a total of $2 + \varepsilon$. So the ratio of greedy tends to 2.

## Known algorithms

**EDF for unit jobs and unit values.** In each slot, send a pending packet with the earliest deadline.

*Theorem.* For unit jobs with unit values at integer times, EDF is optimal: ALG$(\sigma) = $ OPT$(\sigma)$.

*Proof.* Take an optimal schedule that agrees with EDF in all slots before $t$, with $t$ as large as possible, and suppose it is not EDF in slot $t$. EDF sends a packet $a$ with the earliest deadline among the pending packets. If the optimal schedule sends $a$ in a later slot $t'$ and sends $b$ (or nothing) in slot $t$, swap $a$ and $b$. The packet $b$ was pending at $t$, so $r_b \le t < t'$, and $d_b \ge d_a > t'$, so $b$ may use slot $t'$. If the optimal schedule never sends $a$, put $a$ in slot $t$ in place of $b$. In each case the count does not decrease and the schedule agrees with EDF in slot $t$, which contradicts the choice of $t$. $\square$

**Greedy by value for unit jobs.** In each slot, send a pending packet with the largest value.

*Theorem.* For unit jobs with values at integer times, greedy is 2-competitive, and the example above shows that the ratio 2 is tight.

*Proof.* Take an optimal schedule and charge each packet $q$ that it sends. If greedy also sends $q$, charge $q$ to itself. Otherwise let $t$ be the slot in which the optimum sends $q$. Then $r_q \le t < d_q$ and greedy has not sent $q$, so $q$ is pending for greedy at $t$, and greedy sends in slot $t$ a packet $g$ with $v_g \ge v_q$. Charge $q$ to $g$. Each greedy packet is charged at most twice: once by itself and once by the slot in which it is sent. Each charge is at most its value, so OPT $\le 2 \cdot$ ALG. $\square$

**The golden ratio for unit jobs (Veselý, Chrobak, Jeż and Sgall 2019).** A deterministic algorithm with ratio $\varphi = (1 + \sqrt 5)/2 \approx 1.618$ exists for unit jobs with values, and no deterministic algorithm is better. This result is cited here and not proved.

**$D^{\text{over}}$ for general jobs (Koren and Shasha 1995).** The algorithm runs EDF while all jobs can meet their deadlines. When a new job makes the set infeasible, it compares the value of the new job with the value of the jobs it would displace, using a factor that depends on $k$, and it keeps track of the latest time at which each job must start to finish. It is $(1 + \sqrt{k})^2$-competitive, so 4-competitive when the value equals the size. This result is cited here, and this description is only a sketch.

**Slack (Eberle, Megow and Schewior 2020).** For unit values and slack $\varepsilon$, with commitment, a deterministic online algorithm is $O(1/\varepsilon)$-competitive, and this is the best possible order. This result is cited here and not proved.

## Bounds

| model | bound | proved here or cited |
|---|---|---|
| all jobs can finish (underloaded) | EDF is optimal | [EDF optimality](/edf-optimality/) |
| general jobs, plain EDF | no bounded ratio | example above |
| deterministic, value equal to size | 4, tight | cited, Baruah et al.; Koren and Shasha |
| deterministic, value densities within a factor $k$ | $(1 + \sqrt k)^2$, tight | cited, Baruah et al.; Koren and Shasha |
| unit jobs, unit values | 1, EDF | proved above |
| unit jobs with values, greedy | 2, tight for greedy | proved above |
| unit jobs with values, deterministic | $\varphi \approx 1.618$, tight | cited, Veselý, Chrobak, Jeż and Sgall |
| unit values, slack $\varepsilon$, commitment | $\Theta(1/\varepsilon)$ | cited, Eberle, Megow and Schewior |

*Idea of the lower bound 4.* The adversary releases jobs with zero slack in a chain, each larger than the one before by a fixed factor, and each one overlapping the previous one. If the algorithm stays with the current job, the adversary stops the chain after the next one, and the optimum takes the larger job. If the algorithm switches, the old job is lost. The growth factor that balances these two cases gives the bound 4. The details are in Baruah et al.

## Reductions

- **From interval scheduling.** Zero slack makes each job an interval $[r_j, d_j)$, and preemption is then the same as abort. So the lower bounds for [online interval scheduling](/online-interval-scheduling/) with abort hold here.
- **To bipartite matching.** Unit jobs at integer times form a bipartite graph between packets and slots, and a schedule is a matching. EDF is the greedy online matching for this special graph, and it is optimal for unit values.
- **Feasibility.** With preemption, a set of jobs can all meet their deadlines if and only if EDF meets them all, so the offline question for a fixed set is easy. The hard part is to choose the set.

## Applications

Real-time operating systems under overload, where tasks have firm deadlines and different importance; network switches that buffer packets with deadlines; and batch systems that sell computing time by the job, where a job finished late earns nothing.

## References
