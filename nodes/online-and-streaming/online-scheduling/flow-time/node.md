---
tag: GWQ4VJ
kind: concept
slug: flow-time
name: Flow time
aliases:
- response time
- sojourn time
- turnaround time
area: online-and-streaming/online-scheduling
level: advanced
summary: Time a job spends in the system from its release to its completion.
prereqs: [release-time, scheduling-notation]
see_also: [stretch, srpt, srpt-optimality, online-flow-time-minimization, non-clairvoyant-flow-time-minimization, flow-time-minimization, scheduling-metrics, online-total-completion-time]
sources:
  - book: isbn:9781584883975
    title: Joseph Y-T. Leung (ed.), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004
    locator: Chapter 15, Kirk Pruhs, Jiří Sgall and Eric Torng, Online Scheduling (the flow time objectives and their online results)
  - paper: "Hans Kellerer, Thomas Tautenhahn and Gerhard J. Woeginger, Approximability and nonapproximability results for minimizing total flow time on a single machine, SIAM Journal on Computing 28(4), 1999"
    locator: pages 1155 to 1166 (introduction, on why flow time is harder to approximate than completion time)
  - paper: "Michael A. Bender, Soumen Chakrabarti and S. Muthukrishnan, Flow and stretch metrics for scheduling continuous job streams, SODA 1998"
    locator: pages 270 to 279 (the flow time and stretch metrics, and FIFO for the maximum flow time on parallel machines)
  - paper: "John D. C. Little, A proof for the queuing formula L = lambda W, Operations Research 9(3), 1961"
    locator: pages 383 to 387 (the mean number in the system equals the arrival rate times the mean time in the system)
---

The flow time of a job is the time from its [release](/release-time/) to its completion: $F_j = C_j - r_j$. It measures how long a user waits for an answer, so it is the main quality measure of [online scheduling](/online-flow-time-minimization/) for servers and time-shared systems. A schedule is judged by the total, the weighted total, the maximum or a norm of the flow times. The total flow time has the same optimal schedules as the total completion time, but it is much harder to approximate.

## In plain words

A job arrives at a server at some moment and leaves when the server finishes it. Its flow time is the time between these two moments. It includes the time the job waits in the queue and the time the server works on it. A user who sends a request to a web server sees exactly this time.

If you add the flow times of all jobs, you get the total waiting of all users. The same total also comes from a different count: at each moment, count the jobs that are in the system, and add these counts over time. A scheduler that finishes short jobs first keeps few jobs in the system, so the total stays small. A scheduler that serves jobs in arrival order is fairer to long jobs, but a long job at the front makes many short jobs wait.

## The idea

Fix a schedule of $n$ jobs. Job $j$ has a release time $r_j$, a processing time $p_j > 0$, an optional weight $w_j > 0$ and a completion time $C_j$ in the schedule. Its flow time is

$$F_j = C_j - r_j.$$

On one machine of speed 1, $F_j \ge p_j$, because the job needs $p_j$ units of work after $r_j$. The difference $F_j - p_j$ is the waiting time of the job. The usual objectives are:

| objective | formula | notation |
|---|---|---|
| total flow time | $\sum_j F_j$ | $\sum F_j$ |
| weighted flow time | $\sum_j w_j F_j$ | $\sum w_j F_j$ |
| maximum flow time | $\max_j F_j$ | $F_{\max}$ |
| $\ell_p$ norm of flow time | $(\sum_j F_j^p)^{1/p}$ for $p \ge 1$ | $\ell_p$ |
| total [stretch](/stretch/) | $\sum_j F_j / p_j$ | $\sum S_j$ |

In the online setting, $\sigma$ is the sequence of jobs, each job becomes known at its release time, and ALG$(\sigma)$ and OPT$(\sigma)$ are the objective values of the online schedule and of the best [offline](/offline-optimum/) schedule. An algorithm is $c$-competitive if ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$ (the [competitive ratio](/competitive-ratio/), here with additive constant $b = 0$).

**Flow time and completion time.** Summed over the jobs,

$$\sum_j F_j = \sum_j C_j - \sum_j r_j.$$

The term $\sum_j r_j$ does not depend on the schedule. So a schedule is optimal for the total flow time if and only if it is optimal for the total completion time, and the same holds with weights. The approximation ratios do not carry over. If ALG $\le c \cdot$ OPT for the total completion time, then for the flow time

$$\sum F_j(\text{ALG}) \le c \sum F_j(\text{OPT}) + (c - 1) \sum_j r_j,$$

and the last term can be much larger than OPT. A ratio for $\sum C_j$ therefore gives no ratio for $\sum F_j$. This is why [online total completion time](/online-total-completion-time/) has constant ratios, while total flow time without [preemption](/preemptive-scheduling/) has no constant ratio online, and offline no constant ratio unless P = NP.

**Flow time as an integral.** Let $N(t)$ be the number of jobs that are released but not complete at time $t$, that is, the jobs with $r_j \le t < C_j$. Then

$$\sum_j F_j = \int_0^\infty N(t) \, dt.$$

*Proof.* For each job, $F_j = \int_0^\infty [r_j \le t < C_j] \, dt$. Add over $j$ and change the order of the sum and the integral. The sum of the indicators at time $t$ is $N(t)$. $\square$

With weights, the same proof gives $\sum_j w_j F_j = \int_0^\infty W(t) \, dt$, where $W(t)$ is the total weight of the jobs in the system at time $t$. This form is the base of most online analyses. To show that ALG $\le c \cdot$ OPT, it is enough to show that $N_{\text{ALG}}(t) \le c \cdot N_{\text{OPT}}(t)$ at each $t$, or a weaker statement on average. The proof of [SRPT optimality](/srpt-optimality/) compares the counts $N(t)$ in this way.

**Fractional flow time.** Let $q_j(t)$ be the remaining work of job $j$ at time $t$. The fractional flow time is $\int_0^\infty \sum_j q_j(t)/p_j \, dt$: a job counts in proportion to the part that is not yet done. It is at most the total flow time, and it is easier to bound with a [potential function](/potential-function/). Many analyses with extra machine speed first bound the fractional flow time, then convert it to the total flow time with a small loss in speed or in the ratio.

## Examples

Take three jobs on one machine: job 1 with $r_1 = 0$ and $p_1 = 4$, job 2 with $r_2 = 1$ and $p_2 = 1$, and job 3 with $r_3 = 2$ and $p_3 = 2$.

| schedule | $C_1, C_2, C_3$ | $F_1, F_2, F_3$ | $\sum F_j$ | $F_{\max}$ |
|---|---|---|---|---|
| FIFO, in release order, no preemption | 4, 5, 7 | 4, 4, 5 | 13 | 5 |
| [SRPT](/srpt/), shortest remaining work first | 7, 2, 4 | 7, 1, 2 | 10 | 7 |

SRPT runs job 1 on $[0, 1)$, job 2 on $[1, 2)$, job 3 on $[2, 4)$ and job 1 again on $[4, 7)$. Its count of jobs in the system is $N(t) = 1$ on $[0, 1)$, $2$ on $[1, 4)$ and $1$ on $[4, 7)$. The integral is $1 + 6 + 3 = 10$, the same as the sum of the flow times.

The two objectives disagree here. SRPT has the smaller total flow time, which is optimal by Schrage's theorem. FIFO has the smaller maximum flow time, and on one machine FIFO is optimal for $F_{\max}$ (the proof is on the [flow time minimization](/flow-time-minimization/) page).

Now add 100 to each release time. Each flow time stays the same, so the ratio of FIFO to SRPT for the total flow time stays $13/10 = 1.3$. The total completion times become $316$ and $313$, with ratio about $1.0096$. A small ratio for completion time says almost nothing about flow time.

## Where it is used

- **Servers and operating systems.** The mean response time of a web server or a time-shared processor is the mean flow time. In queueing theory, Little's law $L = \lambda W$ says that the mean number of jobs in the system equals the arrival rate times the mean flow time. The integral identity above is the same statement for one fixed finite input. See also [scheduling metrics](/scheduling-metrics/).
- **Online scheduling theory.** [Online flow time minimization](/online-flow-time-minimization/) and its [non-clairvoyant](/non-clairvoyant-flow-time-minimization/) version study $\sum F_j$, $\sum w_j F_j$ and $F_{\max}$. The [stretch](/stretch/) $F_j / p_j$ and the [max stretch](/online-max-stretch/) normalize the flow time by the job size.
- **Offline approximation.** Without preemption, the total flow time on one machine has an $O(\sqrt{n})$ approximation and no much better one unless P = NP (Kellerer, Tautenhahn and Woeginger 1999). See [flow time minimization](/flow-time-minimization/).
- **Energy and flow time.** In [online speed scaling](/online-speed-scaling/), a common objective is the flow time plus the energy.

## References
