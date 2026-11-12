---
tag: ARFFDA
kind: algorithm
slug: backfilling
name: Backfilling
aliases:
- EASY backfilling
- conservative backfilling
area: systems/scheduling
level: advanced
summary: A FCFS queue of parallel jobs in which later jobs may start early in idle processors if they do not delay a reservation. EASY gives a reservation to the first job only; conservative to all.
solves: [cluster-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, P: the number of processors}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [David A. Lifka]
  note: Lifka described EASY backfilling for the IBM SP at Argonne National Laboratory at the 1995 workshop on job scheduling strategies for parallel processing. Mu'alem and Feitelson studied conservative backfilling in 2001.
prereqs: [fcfs-scheduling, cpu-scheduling]
see_also: [gang-scheduling, cluster-scheduling, list-scheduling, strip-packing, makespan, utilization, event-driven-simulation, shortest-job-first]
sources:
  - paper: "David A. Lifka, The ANL/IBM SP Scheduling System, Job Scheduling Strategies for Parallel Processing (JSSPP 1995), Lecture Notes in Computer Science 949, Springer, 1995"
    title: The ANL/IBM SP Scheduling System
    locator: pages 295 to 303 (the EASY scheduler, user run time limits, and backfilling that must not delay the first job in the queue)
  - paper: "Ahuva W. Mu'alem and Dror G. Feitelson, Utilization, Predictability, Workloads, and User Runtime Estimates in Scheduling the IBM SP2 with Backfilling, IEEE Transactions on Parallel and Distributed Systems, 12(6), 2001"
    title: "Utilization, Predictability, Workloads, and User Runtime Estimates in Scheduling the IBM SP2 with Backfilling"
    locator: pages 529 to 543 (EASY and conservative backfilling, the profile of free processors, compression after early ends, and the effect of inaccurate estimates)
---

Backfilling is a policy for a queue of rigid parallel jobs on a machine with $P$ processors. Each job needs a fixed number of processors for its whole run, and its user gives an estimate of its run time. Plain [first come, first served](/fcfs-scheduling/) starts the jobs strictly in order, so a large job at the head of the queue leaves processors idle while it waits. Backfilling lets a later job start in those idle processors if it does not delay a *reservation*. **EASY backfilling** (Lifka 1995) gives a reservation only to the first job in the queue. **Conservative backfilling** (Mu'alem and Feitelson 2001) gives a reservation to every job when it arrives, and a backfilled job may delay none of them.

## In plain words

A machine has a number of processors, and each job asks for some of them for some time. Jobs wait in a line. The job at the front needs many processors, so it must wait until enough of them are free. Meanwhile, some processors sit idle.

Backfilling looks further down the line for a small job that fits in the idle processors. The small job may start now if it will not make the front job wait longer. The scheduler knows this because each user says how long the job will run at most, and a job that runs longer is stopped.

The EASY method protects only the front job. The conservative method protects every job in the line: each job gets a promised start time when it arrives, and no other job may break that promise.

## The problem

The model is a machine of $P$ identical processors and jobs that arrive over time. Job $j$ has an arrival time $a_j$, a size $p_j \le P$ (processors), a user estimate $e_j$ and a real run time $r_j$. The system kills a job at its estimate, so job $j$ runs for $\min(r_j, e_j)$. The scheduler knows $a_j$, $p_j$ and $e_j$ when the job arrives, and learns the real end only when it happens. A job that starts at $s_j$ holds $p_j$ processors during $[s_j, s_j + \min(r_j, e_j))$, and at no time can more than $P$ processors be held. There is no preemption. The goals are high [utilization](/utilization/) and short waits, with a guarantee that large jobs do not starve.

## The algorithm

The scheduler runs at each arrival and at each end of a job. This is the EASY pass. Here $t$ is the current time, $\mathit{free}$ the number of idle processors, and the queue is in order of arrival.

```pseudo id=main
EASY-BACKFILL(t, queue, running, free)
L1  while the queue is not empty and size(head) ≤ free do start the head now; free ← free − size(head)
L2  if the queue is empty then return
L3  h ← the head of the queue                       ▷ it does not fit now
L4  sort the running jobs by their estimated end e_k = start_k + estimate_k
L5  shadow ← the first e_k at which free + the sizes of the jobs that end by e_k ≥ size(h)
L6  extra ← free + the sizes of the jobs that end by shadow − size(h)
L7  for each other job j in the queue, in order do
L8      if size(j) ≤ free and (t + estimate(j) ≤ shadow or size(j) ≤ extra) then
L9          start j now; free ← free − size(j); if t + estimate(j) > shadow then extra ← extra − size(j)
```

The *shadow time* of line L5 is the reservation of the head: the time at which, by the estimates, enough processors will be free for it. The *extra* processors of line L6 are the ones that are still free at the shadow time after the head starts. A job may jump the queue at line L8 if it ends by the shadow time, or if it uses only extra processors, so the head can still start at the shadow time.

**Conservative backfilling** keeps a *profile*: the number of free processors as a function of future time, by the estimates of the running jobs and the reservations of the queued jobs.

1. When job $j$ arrives, find the earliest time $s \ge t$ at which $p_j$ processors are free in the profile for $e_j$ time units, and reserve them. The reservation never changes another job's reservation.
2. When a job ends before its estimate, its processors become free early. *Compress* the schedule: in order of reservation time, remove each queued job's reservation and put it back at its earliest fit. A job never moves later, because its old slot is still free.
3. Start each job whose reservation is the current time.

## Example

A machine of 4 processors. All jobs run exactly as long as their estimates.

| job | arrival | size | estimate |
|---|---|---|---|
| J1 | 0 | 2 | 10 |
| J2 | 1 | 3 | 5 |
| J3 | 2 | 4 | 5 |
| J4 | 3 | 1 | 20 |
| J5 | 4 | 2 | 5 |

The start times under the three policies are these.

| job | FCFS | EASY | conservative |
|---|---|---|---|
| J1 | 0 | 0 | 0 |
| J2 | 10 | 10 | 10 |
| J3 | 15 | 23 | 15 |
| J4 | 20 | 3 | 20 |
| J5 | 20 | 15 | 4 |

**EASY.** At time 1, J2 is the head and does not fit. J1 ends at 10 by its estimate, so the shadow time is 10, with 4 free processors, and the extra processors are $4 - 3 = 1$. At time 3, J4 needs 1 processor and ends at 23, after the shadow time, but it fits in the 1 extra processor, so it starts. J2 still starts at 10, as promised. But J3, which needs all 4 processors, now waits for J4 until 23, instead of 15 under FCFS: EASY protects only the head. At time 15, J3 is the head with shadow time 23, and J5 ends by 20, so it is backfilled.

**Conservative.** Each job gets a reservation at its arrival: J2 at 10, J3 at 15, J4 at 20 (at 3 or 10 it would overlap J3), and J5 at 4, because J5 fits next to J1 from 4 to 9 and ends before any reservation needs its processors. No job starts later than under FCFS here, and J5 starts 16 time units earlier.

If J1 really ends at 6 instead of 10, conservative backfilling compresses at time 6: J2 moves from 10 to 9 (it needs J5's processors, free at 9), J3 from 15 to 14 and J4 from 20 to 19.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Capacity.** At no time do the running jobs hold more than $P$ processors. Line L8 starts a job only if it fits in the free processors.
2. **EASY protects the head.** Let job $h$ become the head at time $t_0$, and let $S$ be the shadow time computed then. Then $h$ starts no later than $S$. The key fact is that the shadow time never moves later while $h$ is the head: a backfilled job either ends by the shadow time or uses only extra processors, and a real end is never after the estimated end.
3. **Conservative protects every job.** Each job starts no later than the reservation it gets at its arrival. A new reservation uses only free parts of the profile, and a compression moves each reservation only earlier.
4. **No starvation.** Under both policies, every job starts in finite time: under EASY because each job eventually becomes the head, and under conservative because its reservation is finite.

The tests check these claims on 400 random workloads with inaccurate estimates. For EASY, they recompute the shadow time of each job from the trace alone.

## Complexity

Let $n$ be the number of jobs. There are at most $2n$ events. An EASY pass sorts at most $n$ running jobs and scans the queue once, in $O(n \log n)$ time, so the whole simulation takes $O(n^2 \log n)$ time and $O(n)$ space. Conservative backfilling keeps a profile with $O(n)$ breakpoints. The earliest fit of one job takes $O(n)$ time with a sliding scan over the breakpoints, and a compression re-fits up to $n$ jobs in $O(n^2)$, so it costs $O(n^3)$ in total. The implementation uses a simpler fit that checks every candidate time against every interval, in $O(n^3)$ per fit, which is enough for tests.

## Properties

- **Not optimal.** Scheduling rigid jobs to minimize the makespan or the mean wait is NP-hard, because it contains [bin packing](/bin-packing/) and [strip packing](/strip-packing/). Backfilling is a fast heuristic with a guarantee against starvation.
- **Depends on estimates.** A job with a large estimate is hard to backfill, so users have a reason to give tight estimates. Real estimates are often far too large, and early ends make room that backfilling uses.
- **EASY is more aggressive.** It backfills more jobs than conservative backfilling, because it checks only one reservation. A job that is not the head can be delayed, as J3 is in the example.
- **Conservative is predictable.** Each user gets a start time at submission, and it can only get earlier.

## Variants and improvements

- **Order of the backfill candidates.** Line L7 scans in arrival order. Scanning the shortest estimated jobs first, as in [shortest job first](/shortest-job-first/), lowers the mean wait.
- **More reservations.** Some schedulers give reservations to the first $k$ jobs, between EASY ($k = 1$) and conservative ($k = n$).
- **Predicted run times.** Replace the user estimate with a prediction from the history of the user, and fix a wrong prediction when the job runs past it.
- **Malleable and moldable jobs.** If a job can run on several sizes, the scheduler can shrink it to fit a hole.
- **Clusters.** Batch schedulers such as Slurm, PBS and Maui use backfilling; a [cluster scheduler](/cluster-scheduling/) for many resources faces the same problem with vectors of demands.

## When to use it

Use backfilling for batch queues of rigid parallel jobs, as on supercomputers and HPC clusters, when users give run time limits and jobs do not share processors. Choose EASY when throughput matters most and conservative when users need a promised start time or when the queue holds many large jobs that EASY could delay. If the jobs must share processors in time, for example interactive parallel jobs, use [gang scheduling](/gang-scheduling/) instead.

## Pitfalls

- **Trusting the real run time.** The shadow time must use the estimates of the running jobs, not their real run times, because the scheduler does not know them. A job that is not killed at its estimate breaks every guarantee.
- **Counting extra processors twice.** When a long job is backfilled into the extra processors, line L9 must lower $\mathit{extra}$, or a second long job can take the same processors and delay the head.
- **Moving a reservation later.** In a compression, re-fit the jobs in order of their reservation. Another order can move a job into a slot that a later re-fit needs, and then a job lands after its old reservation.
- **Starting only at arrivals.** The scheduler must run at every end of a job, early or not, because that is when processors become free.

## Implementations

## History

Lifka built the Extensible Argonne Scheduling sYstem (EASY) for the IBM SP at Argonne National Laboratory and described it in 1995. Users gave a run time limit for each job, and the scheduler started later jobs early when this did not delay the first job in the queue. EASY was later combined with IBM LoadLeveler. Mu'alem and Feitelson compared EASY with conservative backfilling in 2001, using workloads from real SP2 installations. They found that the two have similar performance on most workloads, and that inaccurate user estimates hurt backfilling less than one might expect.

## References
