---
tag: YGJAGZ
kind: algorithm
slug: gang-scheduling
name: Gang scheduling
aliases:
- coscheduling
area: systems/scheduling
level: advanced
summary: Time-share a parallel machine so that all threads of a parallel job run in the same time slot on different processors. The Ousterhout matrix holds one row per slot and one column per processor.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {P: the number of processors, R: the number of rows of the matrix}
  time: {worst: O(R P)}
  space: {extra: O(R P)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1982
  people: [John K. Ousterhout]
  note: Ousterhout proposed coscheduling of the processes of a parallel job, with a matrix of time slots and processors, at ICDCS in 1982, from his work on the Medusa system for Cm*.
prereqs: [round-robin, cpu-scheduling]
see_also: [cluster-scheduling, backfilling, list-scheduling, makespan, bin-packing, multilevel-queue-scheduling, preemption, utilization]
sources:
  - paper: "John K. Ousterhout, Scheduling Techniques for Concurrent Systems, Proceedings of the 3rd International Conference on Distributed Computing Systems (ICDCS), 1982"
    title: Scheduling Techniques for Concurrent Systems
    locator: pages 22 to 30 (coscheduling, the matrix of time slots and processors, and placement methods)
  - paper: "Dror G. Feitelson and Larry Rudolph, Gang Scheduling Performance Benefits for Fine-Grain Synchronization, Journal of Parallel and Distributed Computing, 16(4), 1992"
    title: Gang Scheduling Performance Benefits for Fine-Grain Synchronization
    locator: the whole paper (gang scheduling, and measurements of fine-grain synchronization with and without gangs)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 8, Section 8.1.4 (multiprocessor scheduling, space sharing and gang scheduling)
---

Gang scheduling, also called coscheduling, is a policy for a parallel machine that time-shares the processors so that all threads of a parallel job (a *gang*) run in the same time slot, each on its own processor. The usual data structure is the *Ousterhout matrix*: one row for each time slot and one column for each processor. Each gang is placed in one row, with one thread in each of some columns. The rows take turns in [round robin](/round-robin/) order, and in each slot every processor runs the thread in its column of the current row. When the threads of a job wait for each other often, gang scheduling lets each wait end in microseconds, while independent scheduling of the threads can make each wait last for a whole time slice.

## In plain words

A parallel program is like a team that must work at the same moment: one member often waits for an answer from another. If the members get the processors at different times, each one waits for the others most of the time and does almost no work.

Gang scheduling gives the whole team its turn together. The scheduler keeps a table with one row for each turn and one column for each processor. A team fills some places in one row. At each turn, the next row runs, and every processor runs the member in its column. Several small teams can share a row, and one row can have empty places that waste processor time.

## The problem

The model is a machine with $P$ identical processors and time in slots. A parallel job $g$ has $\mathit{size}_g \le P$ threads and needs $\mathit{work}_g$ slots in which all its threads run at once. Jobs arrive over time. The goal is to time-share the machine between the jobs, with the rule that the threads of each job always run together: in each slot, either all threads of a job run, or none does. Inside this rule, the scheduler wants few idle processors and a short wait between two turns of each job.

## The algorithm

```pseudo id=main
GANG-SCHEDULE(P, jobs)
L1  M ← an empty matrix with P columns; r ← 0; t ← 0
L2  while some job is not finished do
L3      for each job g that arrives at time t do PLACE(M, g)
L4      if M has no rows then idle for one slot; t ← t + 1; continue
L5      r ← r mod (the number of rows of M)
L6      run every gang of row r, each thread on the processor of its column
L7      [alternate] for each gang h of another row whose columns are all idle in this slot: run h too
L8      for each gang that ran: work ← work − 1; if work = 0 then remove it from M, and drop its row if empty
L9      r ← the index of the first remaining row after the old row r; t ← t + 1
```

PLACE is first fit: it finds the first row with at least $\mathit{size}_g$ free columns, adds an empty row at the end if there is none, and puts the threads of $g$ in the lowest free columns of that row. A gang never changes its row or its columns, so each thread stays on one processor.

Line L7 is optional. Some processors are idle in the current row; if a gang of another row has all its columns idle in this slot, it can run as a whole without breaking the gang rule. Ousterhout's paper lets an idle processor take work from another row; the form here takes only whole gangs, so the rule still holds.

## Example

Four processors and four gangs that arrive at time 0: A with 2 threads and 2 slots of work, B with 3 threads and 1 slot, C with 2 threads and 3 slots, and D with 1 thread and 2 slots. First fit gives this matrix.

| row | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| 0 | A0 | A1 | C0 | C1 |
| 1 | B0 | B1 | B2 | D0 |

The slots run the rows 0, 1, 0, 1, 0. In the slot after B finishes, row 1 holds only D, and three processors idle. When D finishes, row 1 is dropped, and row 0 runs in every slot.

| slot | P0 | P1 | P2 | P3 | finished |
|---|---|---|---|---|---|
| 0 | A0 | A1 | C0 | C1 | |
| 1 | B0 | B1 | B2 | D0 | B at 2 |
| 2 | A0 | A1 | C0 | C1 | A at 3 |
| 3 | idle | idle | idle | D0 | D at 4 |
| 4 | idle | idle | C0 | C1 | C at 5 |

For contrast, deal the 8 threads to the processors in turn and let each processor run its own round robin. Processor 0 holds A0 and B2, and processor 2 holds B0 and C1, so in the first slot B0 and B1 run but B2 does not. If B's threads wait for each other, B0 and B1 spin for the whole slot.

Alternate selection: on 4 processors, A has 3 threads, B has 2 and C has 1, each with 4 slots of work. The rows are `A A A C` and `B B . .`. In the slots of row 1, the column of C is idle, so line L7 runs C too. C finishes at slot 4 instead of 7, and A and B finish at the same times as before.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **The gang rule.** In each slot, for each gang, either all its threads run, each on its own processor, or none does. Line L6 runs whole rows, a gang lies in one row, and line L7 adds only gangs whose columns are all idle.
2. **No processor runs two threads.** Each cell of the matrix holds at most one thread, and line L7 checks that the columns are idle.
3. **Bounded wait.** If no job arrives after time 0, every gang runs at least once in every $R$ consecutive slots, where $R$ is the number of rows after the first placement.
4. **Termination.** Each slot with a non-empty matrix runs at least one gang, so every gang finishes.

## Complexity

PLACE scans at most $R$ rows of $P$ cells, so it takes $O(RP)$ time. Line L6 takes $O(P)$. Line L7 looks at every gang of the other rows, in $O(RP)$ time per slot, so a slot takes $O(P)$ without alternate selection and $O(RP)$ with it. The matrix takes $O(RP)$ space. A machine with a bit mask of the free columns of each row can do the first-fit test with a population count.

## Properties

- **All or nothing.** The threads of a job always make progress together, so a lock or a barrier inside the job is never held by a thread that is not running.
- **Fragmentation.** A row with free columns wastes those processors in its slots, unless line L7 fills them. A gang that needs $P$ processors needs a row of its own.
- **Fair between rows, not between jobs.** Each row gets the same number of slots, so a job in a crowded row gets the same CPU as a job alone in its row.
- **Memory.** All jobs in the matrix stay in memory at once, so the number of rows is limited by memory as well as by the wait that users accept.

## Variants and improvements

- **Placement.** First fit is simple; best fit and buddy schemes (columns split into aligned blocks of powers of two) reduce fragmentation. Moving gangs between rows to fill gaps reduces the number of rows.
- **Space sharing.** The other main way to run parallel jobs gives each job a set of processors until it finishes, with no time sharing. A queue of such jobs is often run with [backfilling](/backfilling/).
- **Implicit coscheduling.** A thread that waits spins for a short time and then blocks, and each node schedules on its own. Threads that talk often end up running at the same time without a global matrix.
- **Hypervisors and clusters.** Virtual machines with several virtual CPUs use relaxed coscheduling, which keeps the virtual CPUs of a machine close in progress. A [cluster scheduler](/cluster-scheduling/) can place all tasks of a job at once, which is gang scheduling in space.

## When to use it

Use gang scheduling when the threads of a parallel job synchronize often, for example at barriers or through spin locks, and the machine is shared by several such jobs: parallel machines with time sharing, and some hypervisors. Do not use it when the threads are independent, because the gang rule then only adds idle slots. For batch jobs that run to completion on their own processors, use space sharing with a queue policy such as backfilling instead.

## Pitfalls

- **Breaking the gang rule while filling gaps.** If an idle processor takes a single thread of a gang from another row, that gang runs only in part and its threads may spin. Fill gaps only with whole gangs, as line L7 does.
- **Moving the turn when a row is dropped.** When a row before the current row is removed, the indices of the later rows fall by one. Track the row itself, not its index, as line L9 does, or one row skips a turn.
- **Slots that are too short.** The switch of all processors at once needs a global clock or a broadcast. If the slot is not much longer than the switch, the machine spends its time in the switch.
- **A gang larger than the machine.** A gang with more threads than processors can never run. Reject it at PLACE.

## Implementations

## History

Ousterhout described coscheduling in 1982, from the Medusa operating system on the Cm* multiprocessor at Carnegie Mellon. He compared the cost of uncoordinated scheduling of cooperating processes to thrashing in paging, and gave methods that place the processes of a task force in a matrix of time slots and processors. Feitelson and Rudolph used the name gang scheduling and measured its benefit for fine-grain synchronization in 1992. Gang scheduling was used on parallel machines such as the Connection Machine CM-5 and in later cluster systems.

## References
