---
tag: KWDCKZ
kind: algorithm
slug: multilevel-queue-scheduling
name: Multilevel queue scheduling
aliases:
- multilevel queues
- multilevel queue scheduler
area: systems/scheduling
level: intro
summary: Split the ready jobs into fixed classes, each with its own queue and policy, and choose between the queues by fixed priority or by time slices. Jobs never change queue.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, k: the number of queues, T: the number of ticks simulated}
  time: {worst: O(k T + n log n)}
  space: {extra: O(n + k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [cpu-scheduling, round-robin, priority-scheduling, fcfs-scheduling]
see_also: [multilevel-feedback-queue, aging, preemption, work-conserving-scheduling, scheduling-metrics, lottery-scheduling, completely-fair-scheduler, queue]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.5 (multilevel queue scheduling, the five classes example, fixed priority and time slicing between queues)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.3 (scheduling in interactive systems, priority classes with round robin inside each class)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 7 (scheduling metrics, FIFO, SJF and round robin) and Chapter 8 (the multilevel feedback queue, which lets jobs move)
---

Multilevel queue scheduling is a [CPU scheduling](/cpu-scheduling/) policy that puts each job, for its whole life, into one of $k$ fixed classes. Each class has its own ready queue and its own policy inside the queue, for example [round robin](/round-robin/) for interactive jobs and [first come, first served](/fcfs-scheduling/) for batch jobs. A second rule chooses between the queues: either fixed [priority](/priority-scheduling/) (the highest non-empty queue always runs) or time slicing (each queue gets a fixed part of the CPU). Jobs never move between queues; the [multilevel feedback queue](/multilevel-feedback-queue/) is the variant in which they do.

## In plain words

An office has two lines at the counter: one for urgent short requests and one for long forms. A sign says that the clerk serves the urgent line first, and takes from the long-form line only when the urgent line is empty. Inside each line, people are served in their own way: the urgent line takes turns of a few minutes each, and the long-form line goes in arrival order.

A person never changes line. The class is fixed when the person arrives, for example by the type of request. This makes the rule simple and predictable, but a person in the low line can wait for a very long time if urgent people keep coming. A second version of the sign avoids this: the clerk spends a fixed part of each hour on each line.

## The problem

The model is one CPU and a set of $n$ jobs. Job $j$ has an arrival tick $a_j$, a CPU demand of $b_j \ge 1$ ticks and a class $c_j \in \{0, \ldots, k-1\}$, where class 0 is the most important. Time goes in integer ticks, and the scheduler runs one job in each tick. Queue $i$ has a policy: round robin with a quantum $q_i$, or FCFS. The scheduler is online: at tick $t$ it knows only the jobs with $a_j \le t$. It does not know the demands $b_j$, and it does not optimize a metric. It enforces a fixed policy between classes; the [scheduling metrics](/scheduling-metrics/) (response time, turnaround time, waiting time) are measured afterwards.

## The algorithm

```pseudo id=main
MLQ-SCHEDULE(jobs, Q[0 .. k−1])       ▷ Q[i] has a policy: RR with quantum q_i, or FCFS
L1  t ← 0
L2  while some job is not finished do
L3      append each job j with a_j = t to the tail of Q[c_j]
L4      i ← SELECT-QUEUE(Q, t)            ▷ fixed priority or time slicing
L5      if no queue is selected then t ← t + 1; continue      ▷ the CPU idles
L6      j ← the head of Q[i]
L7      run j for one tick; t ← t + 1; used_j ← used_j + 1
L8      if j has run b_j ticks then remove j from Q[i]; C_j ← t
L9      else if Q[i] is RR and used_j = q_i then move j to the tail of Q[i]; used_j ← 0
```

SELECT-QUEUE has two standard forms.

- **Fixed priority.** Return the smallest $i$ with $Q[i]$ not empty. A job of a lower queue runs only when every higher queue is empty, and an arrival in a higher queue preempts it at the next tick. A preempted round robin job keeps its place at the head of its queue and the part of its quantum that it has used.
- **Time slicing.** The queues take turns in the order $0, 1, \ldots, k-1, 0, \ldots$. Queue $i$ gets up to $s_i$ consecutive ticks in its turn. If the queue of the turn is empty, the turn passes to the next non-empty queue, so the CPU is never idle while a job is ready.

The order of events in one tick is fixed: a job whose quantum ended at tick $t$ goes to the tail first (line L9 of the tick before), and then the arrivals of tick $t$ join (line L3). Other orders are also used; a trace is reproducible only when the order is stated.

## Example

Two queues. Queue 0 is the foreground queue, round robin with $q_0 = 2$. Queue 1 is the background queue, FCFS.

| job | arrival | burst | queue |
|---|---|---|---|
| A | 0 | 3 | 0 |
| B | 0 | 4 | 1 |
| C | 1 | 2 | 0 |
| D | 2 | 3 | 1 |
| E | 7 | 2 | 0 |

**Fixed priority between the queues.** The timeline, one letter per tick from tick 0, is `AACCABBEEBBDDD`.

| ticks | runs | why |
|---|---|---|
| 0 to 1 | A | queue 0 holds A; after 2 ticks A goes to the tail, behind C |
| 2 to 3 | C | C ends at 4 |
| 4 | A | A ends at 5; queue 0 is now empty |
| 5 to 6 | B | queue 1 runs, B is first by arrival |
| 7 to 8 | E | E arrives at 7 and preempts B; E ends at 9 |
| 9 to 10 | B | B ends at 11 |
| 11 to 13 | D | D ends at 14 |

The completion times are C 4, A 5, E 9, B 11 and D 14. B arrives at tick 0 but waits 5 ticks, and it is preempted once by E.

**Time slicing with shares $s_0 = 2$, $s_1 = 1$.** The timeline is `AABCCBAEBEBDDD`, with completion times C 5, A 7, E 10, B 11 and D 14. The background queue now gets a tick in every turn of 3 ticks while both queues are busy, so B starts at tick 2 instead of 5. The foreground jobs end later: A at 7 instead of 5. The last completion is 14 in both cases, because both rules keep the CPU busy whenever a job is ready.

## Correctness

The algorithm enforces a policy rather than computing an optimum, so correctness means these four properties, proved in [proofs/correctness.md](proofs/correctness.md).

1. **No movement.** Each job is in $Q[c_j]$ from its arrival to its completion, and it runs only as the head of that queue.
2. **Work conservation.** In each tick, the CPU idles only if no job is ready. So with finitely many jobs, every job finishes, and the last completion is the same as for any [work-conserving](/work-conserving-scheduling/) policy.
3. **Isolation under fixed priority.** The schedule of the jobs of classes $0, \ldots, c$ is the same as when the jobs of classes $c + 1, \ldots, k - 1$ do not exist. A lower class cannot delay a higher class by even one tick.
4. **Shares under time slicing.** While all queues stay non-empty, each cycle of $\sum_i s_i$ ticks gives exactly $s_i$ ticks to queue $i$.

The key invariant for property 3 is that the state of queues $0, \ldots, c$ (their contents, their order and the used quantum of each job) at each tick depends only on the jobs of those classes. Line L4 reads queues $0, \ldots, c$ first, and it looks at a lower queue only when all of them are empty.

## Complexity

The jobs are first sorted by arrival, in $O(n \log n)$ time. Each tick runs line L4 once. For fixed priority, a scan of the queues takes $O(k)$; for time slicing, the scan from the current turn also takes $O(k)$. Lines L6 to L9 take $O(1)$ with a double-ended queue. Each job is appended once at line L3. So $T$ ticks take $O(kT + n \log n)$ time in the worst case, and the space is $O(n + k)$ for the queues and the counters.

A real kernel does not simulate idle ticks, and it runs the scheduler only at an arrival, a completion, a block or a timer interrupt. With a bit mask of the non-empty queues, the highest non-empty queue is the lowest set bit, which a find-first-set instruction gives in $O(1)$ for $k$ up to the word size. The Linux O(1) scheduler of the 2.6 kernels used this method with 140 priority levels.

## Properties

- **Online and non-clairvoyant.** It needs only the class of each job, not its demand.
- **Deterministic.** The trace depends only on the input and the order of events in a tick.
- **Starvation under fixed priority.** A stream of high-class jobs that keeps a higher queue non-empty stops all lower queues forever. Property 3 is the other side of the same rule.
- **No adaptation.** A job in the wrong class stays there. A CPU-bound job put into the interactive class gets the high priority for its whole run.

## Variants and improvements

- **Multilevel feedback queue.** Jobs move down after they use their allotment, and up at a periodic boost. See [multilevel feedback queue](/multilevel-feedback-queue/).
- **Aging.** Raise a waiting job's class after it waits a long time, to stop starvation. This breaks the "no movement" rule; see [aging](/aging/).
- **Weighted shares.** Time slicing with shares $s_i$ is a deterministic weighted round robin between the queues. [Lottery scheduling](/lottery-scheduling/) and [stride scheduling](/stride-scheduling/) give proportional shares between any number of clients, and they nest: a share can be split again inside a class.
- **Classes by user or group.** Fair-share schedulers put the processes of each user into one class and divide the CPU between users first, then between processes.

## When to use it

Use it when the classes are known in advance and are stable: system tasks, interactive tasks and batch tasks; real-time and best-effort tasks; kernel threads and user threads. Linux, for example, keeps its real-time classes (SCHED_FIFO, SCHED_RR) strictly above its normal class. Do not use pure fixed priority when a high class can saturate the CPU, because the low classes then starve. If the class of a job is not known in advance, use a [multilevel feedback queue](/multilevel-feedback-queue/), which learns it from the job's behavior.

## Pitfalls

- **Losing the quantum on preemption.** If a preempted round robin job is moved to the tail of its queue (line L9 run on a preemption), then a job that is preempted again and again never reaches the end of its quantum and falls behind the jobs of its own queue. Move a job to the tail only when it has used its whole quantum, as line L9 does.
- **Starvation by design.** With fixed priority, a busy foreground stops the background with no bound on the wait. Use time slicing in SELECT-QUEUE (line L4), or add a bound with aging.
- **An unstated tie at one tick.** If a job's quantum ends at the same tick as an arrival, the trace depends on which goes to the tail first. State the order, as in the walk-through after the pseudocode.
- **Idle with a ready job.** A time slicing rule that idles when the queue of the turn is empty is not work-conserving. Pass the turn to the next non-empty queue at line L4.

## Implementations

## History

Silberschatz, Galvin and Gagne present the policy with an example of classes in strict priority order, from real-time and system processes down to interactive and batch processes. They give both fixed priority and time slicing between the queues, with an example that gives 80 percent of the CPU to the foreground queue for round robin and 20 percent to the background queue for FCFS. Tanenbaum and Bos describe priority classes with round robin inside each class as the common design of interactive systems.

## References
