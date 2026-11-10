---
tag: SZRQN3
kind: technique
slug: speculative-execution
name: Speculative execution
aliases:
- backup tasks
- straggler mitigation
area: parallel/mapreduce-and-bsp
level: core
summary: Near the end of a parallel job, start a second copy of each slow task and keep the result of whichever copy finishes first. It cuts the time that a few slow machines add to the whole job.
prereqs: [mapreduce-model]
see_also: [fault-tolerance-by-recomputation, data-skew, barrier-synchronization, resilient-distributed-datasets, amdahls-law, union-bound]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, OSDI 2004"
    locator: Section 3.6 (backup tasks), Section 5.3 (the sort benchmark) and Section 5.4 (the run with backup tasks disabled)
  - paper: doi:10.1145/1327452.1327492
    title: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, Communications of the ACM 51(1), 2008"
    locator: the journal version, with the same backup task mechanism
  - paper: "Matei Zaharia, Andy Konwinski, Anthony D. Joseph, Randy Katz and Ion Stoica, Improving MapReduce performance in heterogeneous environments, OSDI 2008"
    locator: the Hadoop speculation rule and its assumptions, the LATE scheduler (progress rate, estimated time left, SpeculativeCap and the slow node and slow task thresholds) and its evaluation on Amazon EC2
  - paper: "Jeffrey Dean and Luiz Andre Barroso, The tail at scale, Communications of the ACM 56(2), 2013"
    locator: hedged requests and tied requests for latency in services
---

Speculative execution is a technique for parallel jobs that wait for their slowest task. When a job is close to its end, the scheduler starts a second copy, a backup, of each task that is still running, and it uses the output of whichever copy finishes first. A machine with a bad disk, a busy CPU or a slow network can make one task many times slower than the others, and in a job of thousands of tasks such a straggler is almost certain. Dean and Ghemawat report that the MapReduce sort benchmark took $44\%$ longer with backup tasks turned off.

## In plain words

A teacher waits to collect all exam papers before leaving. Most students finish in an hour, but one student sits at a broken desk and works very slowly. The whole class waits for that student. Speculative execution is the trick of giving the same exam to a second student at a good desk when the room is almost empty, and taking whichever paper comes back first. It costs a little extra work, because two people now do the same task. It works only if the task can be done twice without harm, and only if the slowness comes from the desk, not from the task itself. If the task is just very long, a second copy is just as slow.

## When it applies

- The job is a set of independent tasks, and it ends when the last one ends, as in the map phase or the reduce phase of [MapReduce](/mapreduce-model/), or a [superstep](/superstep/) before a [barrier](/barrier-synchronization/).
- The slowness belongs to the machine, not to the task. Typical causes are a disk with soft errors, other jobs on the same machine, a cache that was turned off by a bad setting, or a slow network link. A copy on another machine then has a good chance to be fast.
- A task can run twice with the same effect as once. In MapReduce this holds because the map and reduce functions are deterministic and write only to private temporary files, and the system commits exactly one output per task.
- There are spare machines near the end of the job. A backup uses resources that other tasks or jobs could use.

## The template

The master tracks the progress of each running task and, when it has a free slot, chooses one task to copy.

```pseudo
procedure SCHEDULE(free slot on machine M)
    if a task has not started then
        run it on M
    else if the job is near its end and fewer than CAP backups are running then
        T ← the running task that is expected to finish last, if M is not slow
        if T has only one copy then
            run a backup copy of T on M

procedure ON-FINISH(copy c of task T)
    if T is not yet done then
        commit the output of c        ▷ for example an atomic file rename
        mark T done
        kill the other copies of T
    else
        discard the output of c
```

Three choices define a variant: when backups start, which task is copied, and how many backups may run at once.

**A model.** A job has $n$ tasks. Each task takes time $1$, but with probability $\pi$ it runs on a slow machine and takes time $s \ge 2$. Without backups, the job takes $s$ if any task is slow, so

$$
\mathbb{E}[T] = 1 + (s - 1)\left(1 - (1 - \pi)^n\right).
$$

At time $1$, every task that has not finished gets one backup on another machine, which is slow with probability $\pi$, independently. A task now takes time $1$ with probability $1 - \pi$, time $2$ with probability $\pi(1 - \pi)$ (its backup is fast), and time $s$ with probability $\pi^2$ (both copies are slow). The job time is the largest task time, so

$$
\mathbb{E}[T] = a + 2(b - a) + s(1 - b), \qquad a = (1 - \pi)^n, \quad b = (1 - \pi^2)^n.
$$

The expected number of backup copies is $n\pi$. For $\pi = 0.01$ and $s = 5$:

| $n$ | $\mathbb{E}[T]$ without backups | $\mathbb{E}[T]$ with backups | backup copies |
|---|---|---|---|
| 1 | 1.0400 | 1.0103 | 0.01 |
| 10 | 1.3825 | 1.0986 | 0.1 |
| 100 | 3.5359 | 1.6638 | 1 |
| 1000 | 4.9998 | 2.2855 | 10 |

With $1000$ tasks the job without backups is slow with probability $1 - 0.99^{1000} \approx 1 - 4.3 \times 10^{-5}$: one bad machine in a hundred is almost sure to hit some task. With backups, a task stays slow only if both copies are slow, with probability $\pi^2 = 10^{-4}$, and the job stays fast up to time $2$ with probability $0.9999^{1000} \approx 0.905$. The price is $1\%$ more task runs. By the [union bound](/union-bound/), the chance that some task is slow is at most $n\pi$ without backups and at most $n\pi^2$ with them. The simulator of this page checks both formulas against 3000 seeded runs for several values of $n$, $\pi$ and $s$.

## Classic examples

**MapReduce backup tasks.** Dean and Ghemawat describe the mechanism in Section 3.6 of the MapReduce paper: when a MapReduce operation is close to completion, the master schedules backup executions of the remaining in-progress tasks, and a task is complete when either copy finishes. In their sort of $10^{10}$ records of 100 bytes, about 1 TB, on about 1800 machines, the normal run took $891$ seconds. With backup tasks disabled, the last 5 reduce tasks dragged the run to $1283$ seconds, $44\%$ longer. They tuned the mechanism so that it adds only a few percent of extra computation.

**Hadoop's rule.** Early Hadoop gave each task a progress score between $0$ and $1$: for a map task, the fraction of its input read; for a reduce task, a third for each of the copy, sort and reduce phases. A task became a candidate for a backup when its score was below the average score of its category minus $0.2$ and it had run for at least one minute.

**LATE.** Zaharia, Konwinski, Joseph, Katz and Stoica showed that this rule breaks down when machines differ in speed, as on virtual machines in a public cloud. Their LATE scheduler (Longest Approximate Time to End) estimates, for each running task,

$$
\text{rate} = \frac{\text{progress score}}{\text{time running}}, \qquad \text{time left} = \frac{1 - \text{progress score}}{\text{rate}},
$$

and copies the task with the longest time left among the tasks whose rate is in the slowest quarter. It does not put backups on machines in the slowest quarter, and it caps the backups at $10\%$ of the slots. On 200 virtual machines of Amazon EC2 it cut the response time of jobs by up to a factor of $2$ compared with the Hadoop rule.

*Example.* At time $100$, six tasks started at time $0$ run at rates from $0.006$ to $0.0085$ per second, a task "slow" started at $0$ has score $0.3$, and a task "late start" started at $40$ has score $0.42$. The average score is $0.634$, so Hadoop flags every task below $0.434$: both "slow" and "late start". LATE computes the rates $0.003$ and $0.007$ and the times left $0.7/0.003 = 233.3$ and $0.58/0.007 = 82.9$. "Late start" runs at a normal speed and only started late; a copy would start from zero and need about $143$ seconds, longer than the original. LATE picks "slow", whose copy at a normal rate would finish well before $233$ seconds.

## Variations

- **When to start.** MapReduce starts backups near the end of a phase; LATE may speculate at any time, but caps the number of copies. Starting early helps more but costs more.
- **Cloning.** For small jobs, run two or more copies of every task from the start, so that no straggler needs to be detected.
- **Hedged requests.** In a service that sends a request to one of several replicas, send a second request to another replica if the first has not answered after a delay, such as the 95th percentile of the latency, and use the first answer. Dean and Barroso describe this, and tied requests, in which the two copies can cancel each other.
- **Restart instead of copy.** If the slow copy is known to be on a bad machine, kill it and restart elsewhere. This saves a slot, but loses the work already done.

## Pitfalls

- **Side effects.** Two copies of a task that write to an external store, send e-mail or increment a counter do it twice. Make the effects of a task atomic and idempotent, or turn speculation off for that job. MapReduce writes to temporary files and commits with an atomic rename, so only one copy's output becomes visible.
- **Skew is not slowness.** If a reduce task is slow because its key has far more values than the others, a backup on another machine has the same amount of data and is just as slow, and it takes a slot. The cure for [data skew](/data-skew/) is to split the work, not to copy it.
- **Bad progress estimates.** A score that grows unevenly, such as a reduce task that finishes its copy phase and jumps from $0.33$ to $0.67$, or a task that started late, makes a rule based on the score copy the wrong tasks. Estimate the time left, not the score.
- **Too many copies.** Backups add load. On a busy cluster, many backups slow down the other tasks and can make the job slower. Cap the number of backups, and do not copy a task more than once.
- **Backups on slow machines.** A backup on a machine that is itself slow does not help. Prefer machines that have finished tasks quickly.
- **Nondeterministic tasks.** If two copies of a task can give different outputs, the job output depends on which copy wins. This is acceptable only if every consumer reads the output of the same winning copy.

## Exercises

1. Show that in the model above, backups can never increase the job time on any run, and that for $s = 2$ they never decrease it. *Hint.* A task time with backup is $\min(t, 1 + b)$ with $b \ge 1$.
2. Compute $\mathbb{E}[T]$ with and without backups for $n = 100$, $\pi = 0.01$ and $s = 5$. *Answer.* $1.6638$ and $3.5359$.
3. Change the model so that the backups start at time $\tau$ with $1 \le \tau < s - 1$. Find the distribution of a task time and the expected job time, and find the $\tau$ that minimizes it.
4. A reduce task has three times as many values as the others because of one popular key. Explain why a backup does not help, and give a change to the job that does.
5. In the LATE example above, raise the score of "slow" to $0.45$ and leave the rest the same. Which tasks does Hadoop flag, and which task does LATE pick?

## References
