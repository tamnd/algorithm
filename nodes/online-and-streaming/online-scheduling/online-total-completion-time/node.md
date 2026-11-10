---
tag: XNQS12
kind: problem
slug: online-total-completion-time
name: Online total completion time
aliases:
- online sum of completion times
- online 1|r_j|sum C_j
area: online-and-streaming/online-scheduling
level: advanced
summary: Online minimization of the sum of job completion times with release dates.
prereqs: [release-time, online-algorithm, competitive-ratio, shortest-processing-time-first]
see_also: [srpt, srpt-optimality, scheduling-with-release-dates, weighted-completion-time-scheduling, online-flow-time-minimization, randomized-online-algorithm, oblivious-adversary, non-clairvoyant-flow-time-minimization]
sources:
  - paper: "J. A. Hoogeveen and A. P. A. Vestjens, Optimal on-line algorithms for single-machine scheduling, IPCO 1996, LNCS 1084, Springer"
    locator: pages 404 to 414 (the delayed SPT rule is 2-competitive for 1|r_j|sum C_j, and no deterministic online algorithm is better)
  - paper: "Chandra Chekuri, Rajeev Motwani, B. Natarajan and Clifford Stein, Approximation techniques for average completion time scheduling, SIAM Journal on Computing 31(1), 2001"
    locator: pages 146 to 166 (the randomized alpha-point conversion with ratio e/(e - 1))
  - paper: "Cynthia A. Phillips, Clifford Stein and Joel Wein, Minimizing average completion time in the presence of release dates, Mathematical Programming 82, 1998"
    locator: pages 199 to 223 (converting a preemptive schedule to a non-preemptive one with C_j at most 2 times the preemptive C_j)
  - paper: "Leen Stougie and Arjen P. A. Vestjens, Randomized algorithms for on-line scheduling problems: how low can't you go?, Operations Research Letters 30(2), 2002"
    locator: the e/(e - 1) lower bound for randomized online algorithms for 1|r_j|sum C_j
  - paper: "Jiří Sgall, On-line scheduling, in Amos Fiat and Gerhard J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: Section 5 (scheduling jobs over time, the total completion time objective)
---

Online total completion time is the problem of scheduling jobs that arrive over time on one machine, without [preemption](/preemptive-scheduling/), so that the sum of the completion times $\sum_j C_j$ is small, when each job becomes known only at its [release time](/release-time/). In [three-field notation](/graham-three-field-notation/) it is $1 \mid r_j \mid \sum C_j$, online. The best deterministic [competitive ratio](/competitive-ratio/) is exactly 2, reached by the delayed SPT rule of Hoogeveen and Vestjens (1996), and the best randomized ratio is $e/(e-1) \approx 1.582$ (Chekuri, Motwani, Natarajan and Stein 2001). With preemption the problem is solved by [SRPT](/srpt/).

## In plain words

Jobs arrive at one machine over time. Each job says how long it takes, but once a job starts, it must run to the end. The goal is that, on average, jobs finish early.

If a long job is waiting and the machine is free, it is tempting to start it. But a short job may arrive a moment later and then wait for the whole long job. The good rule is to wait a little: start a job only when the current time is at least the length of the job. This rule is at most twice as bad as the best schedule made with full knowledge of the future. No rule without random choices can do better. A rule with random choices does better on average.

## Definition

**Input.** A sequence $\sigma$ of $n$ jobs. Job $j$ has a release time $r_j \ge 0$ and a processing time $p_j > 0$, both known at time $r_j$. One machine of speed 1.

**Output.** A non-preemptive schedule, built online: at each time $t$, the decision to start a job, or to wait, uses only the jobs with $r_j \le t$. Job $j$ runs on $[S_j, S_j + p_j)$ with $S_j \ge r_j$, and $C_j = S_j + p_j$.

**Objective.** Minimize $\sum_j C_j$.

**Notation.** ALG$(\sigma)$ and OPT$(\sigma)$ are $\sum_j C_j$ for the online schedule and for the best offline non-preemptive schedule. An algorithm is $c$-competitive if ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. For a [randomized](/randomized-online-algorithm/) algorithm, the ratio is $\mathbb{E}[\text{ALG}(\sigma)] \le c \cdot \text{OPT}(\sigma)$ against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **With preemption.** $1 \mid r_j, \text{pmtn} \mid \sum C_j$ online is solved exactly by SRPT ([SRPT optimality](/srpt-optimality/)).
- **Weighted.** $1 \mid r_j \mid \sum w_j C_j$ online. Delayed versions of Smith's ratio rule also reach ratio 2 for deterministic algorithms; see [weighted completion time scheduling](/weighted-completion-time-scheduling/) for the offline problem.
- **Parallel machines.** The same objective on $m$ [identical machines](/identical-machines/).
- **Total flow time.** The objective $\sum (C_j - r_j)$ has the same optimal schedules but no constant ratio without preemption. See [flow time](/flow-time/).
- **Unknown sizes.** If the sizes are learned only at completion, see [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).

## Examples

**Delayed SPT on four jobs.** Take $A = (0, 5)$, $B = (1, 2)$, $C = (2, 4)$ and $D = (3, 1)$, written as (release, size). At time 0 only $A$ is known and $5 > 0$, so the rule waits until the next release at 1. At time 1 the shortest job is $B$ with $2 > 1$, so it waits until time 2 and starts $B$. At time 4 the shortest waiting job is $D$, then $C$ at 5 and $A$ at 9.

| schedule | $C_A, C_B, C_C, C_D$ | $\sum C_j$ |
|---|---|---|
| delayed SPT, online | 14, 4, 9, 5 | 32 |
| best schedule without preemption, offline | 13, 3, 8, 4 | 28 |
| SRPT with preemption | 8, 3, 12, 4 | 27 |

The ratio here is $32/28 = 8/7$. The offline schedule waits on $[0, 1)$, then runs $B$, $D$, $C$ and $A$.

**The tight example.** One job $(0, 1)$. Delayed SPT waits until time 1 and finishes at 2, while OPT finishes at 1. So the ratio 2 of the theorem below is reached.

## Known algorithms

**Delayed SPT (Hoogeveen and Vestjens 1996).** When the machine is free at time $t$, let $j$ be the released, unstarted job with the smallest $p_j$, with ties broken by the smaller release time. If $p_j \le t$, start $j$. Otherwise wait until time $\min(p_j, r')$, where $r'$ is the next release, and decide again.

**Theorem.** Delayed SPT is 2-competitive for $1 \mid r_j \mid \sum C_j$. More strongly, $\sum_j C_j \le 2 \cdot \text{OPT}_{\text{pmtn}}$, where $\text{OPT}_{\text{pmtn}}$ is the preemptive optimum.

*Proof.* We use three facts about the delayed SPT schedule.

1. Each job starts at $S_j \ge p_j$, by the rule.
2. If the machine is idle at time $\tau$, each released, unstarted job has $p_j > \tau$. Else the rule would start the smallest one.
3. A job that starts at time $S$ has the smallest size among the released, unstarted jobs at $S$.

**Lemma.** Let $t \ge 0$, and let $A$ be a set of $a$ jobs that some preemptive schedule completes by time $t$. Then delayed SPT completes at least $a$ jobs by time $2t$.

Each job $j \in A$ has $r_j + p_j \le t$, and the jobs of $A$ have total size at most $t$. Let $B$ be the set of jobs that start before $t$. By fact 1, a job of $B$ has $p_j \le S_j < t$, so it completes before $2t$. If $|B| \ge a$, we are done. Else let $k = a - |B| \ge 1$, and let $A'' = A \setminus B$, the jobs of $A$ that start at time $t$ or later, so $|A''| \ge k$. Each job of $A''$ is released by $t$ and has $p_j \le t$.

Let $J_1, J_2, \dots$ be the jobs that start at time $t$ or later, in order, and let $q_1 \le q_2 \le \dots$ be the sorted sizes of $A''$. When $J_i$ starts, with $i \le k$, at most $i - 1$ jobs of $A''$ have started, so a job of $A''$ with size at most $q_i$ is released and unstarted. By fact 3, $p_{J_i} \le q_i$. While a job of $A''$ is unstarted, at a time $\tau \ge t$ it has size at most $t \le \tau$, so by fact 2 the machine is not idle. So the machine is busy from $t$ until $J_k$ completes. Let $x$ be the job that runs at time $t$, if any. Then

$$C_{J_k} = \max(t, C_x) + \sum_{i=1}^k p_{J_i} \le \max(t, C_x) + Q, \qquad Q = q_1 + \dots + q_k.$$

We show that this is at most $2t$. Then the jobs of $B$ and $J_1, \dots, J_k$ give $|B| + k = a$ completions by $2t$.

- *No job runs at $t$, or $C_x \le t$.* Then $C_{J_k} \le t + Q \le 2t$, because $Q$ is at most the total size of $A$.
- *$x \in A$.* Then $x \notin A''$, so $p_x + Q \le t$. Also $C_x = S_x + p_x < t + p_x$, so $C_x + Q < 2t$.
- *$x \notin A$, and some job $y \in A''$ has $r_y \le S_x$.* Since $x \in B \setminus A$, we have $|A \cap B| \le |B| - 1$, so $|A''| \ge k + 1$. At time $S_x$ the job $y$ was released and unstarted, so $p_x \le p_y$ by fact 3. The $k$ smallest jobs of $A''$ have total at most the total of any $k$ jobs of $A'' \setminus \{y\}$, so $Q + p_y \le t$. Hence $C_x + Q = S_x + p_x + Q < t + p_y + Q \le 2t$.
- *$x \notin A$, and each job of $A''$ has $r_j > S_x$.* The preemptive schedule does all the work of $A''$ inside $(S_x, t]$, so $Q \le t - S_x$. By fact 1, $C_x = S_x + p_x \le 2 S_x$. Hence $C_x + Q \le t + S_x < 2t$.

This proves the lemma. Now let $C^P_{(1)} \le \dots \le C^P_{(n)}$ be the sorted completion times of an optimal preemptive schedule. For each $i$, the lemma with $t = C^P_{(i)}$ and the first $i$ jobs to complete shows that the $i$-th completion of delayed SPT is at most $2 C^P_{(i)}$. Summing over $i$ gives $\sum_j C_j \le 2 \cdot \text{OPT}_{\text{pmtn}} \le 2 \cdot \text{OPT}$, because each non-preemptive schedule is also a preemptive one. $\blacksquare$

**Conversion of a preemptive schedule (Phillips, Stein and Wein 1998).** Run SRPT in the background, and put each job in a FIFO queue at the moment SRPT completes it. Run the queue without preemption. Each job then completes by twice its SRPT completion time, so this rule is also 2-competitive. This result is cited here.

**Randomized $\alpha$-points (Chekuri, Motwani, Natarajan and Stein 2001).** Run SRPT in the background. Pick one random $\alpha \in (0, 1]$ with density $e^{\alpha}/(e - 1)$, and queue each job at the moment SRPT has done an $\alpha$ fraction of it. The expected total completion time is at most $\frac{e}{e-1}$ times the preemptive optimum, against an oblivious adversary. This result is cited here and not proved.

## Bounds

**Theorem (deterministic lower bound).** No deterministic online algorithm for $1 \mid r_j \mid \sum C_j$ has a ratio below 2.

*Proof.* Release one job of size 1 at time 0. Let $S$ be the time at which the algorithm starts it if no other job arrives; a deterministic algorithm fixes $S$ in advance. If $S \ge 1$, no other job arrives, ALG $= S + 1 \ge 2$ and OPT $= 1$. If $S < 1$, release $n$ jobs of size $\delta$ at time $S + \delta$. The machine is busy until $S + 1$, so each small job completes after $S + 1$, and ALG $\ge (n + 1)(S + 1)$. OPT runs the small jobs at once and the long job after them, so OPT $\le n(S + \delta + n\delta) + S + 1 + (n + 1)\delta \le (n+1)S + 1 + 2(n+1)^2 \delta$. As $\delta \to 0$, the ratio tends to

$$\frac{(n + 1)(S + 1)}{(n + 1) S + 1},$$

which is more than 2 when $(n + 1)(1 - S) > 2$. For $n$ large enough this holds, so the ratio of the algorithm is at least 2. $\square$

The ratio 2 is therefore exactly the deterministic answer. For randomized algorithms against an oblivious adversary, the $\alpha$-point algorithm gives $e/(e-1) \approx 1.582$, and Stougie and Vestjens showed that no randomized online algorithm does better. This lower bound is cited here and not proved.

| model | bound | proved here or cited |
|---|---|---|
| deterministic, upper | 2 (delayed SPT) | proved above |
| deterministic, lower | 2 | proved above |
| randomized, oblivious adversary, upper | $e/(e-1)$ | cited, Chekuri, Motwani, Natarajan and Stein |
| randomized, oblivious adversary, lower | $e/(e-1)$ | cited, Stougie and Vestjens |
| preemptive | 1 (SRPT) | proved on [SRPT optimality](/srpt-optimality/) |

## Reductions

- **From preemptive schedules.** Both upper bounds compare with the preemptive optimum and use SRPT as a lower bound. The non-preemptive offline problem is strongly NP-hard, so this lower bound is the usual tool.
- **To total flow time.** $\sum C_j = \sum F_j + \sum r_j$. A ratio for $\sum C_j$ does not give one for $\sum F_j$; see [flow time](/flow-time/).
- **Offline.** The offline problem with release dates is treated on [scheduling with release dates](/scheduling-with-release-dates/).

## Applications

The problem models a single production resource or a non-preemptive processor that receives jobs over time, where the average completion time is the measure of service. The lesson of delayed SPT, that a scheduler should sometimes leave the machine idle to wait for short jobs, also appears in batch systems and in network schedulers that delay large transfers.

## References
