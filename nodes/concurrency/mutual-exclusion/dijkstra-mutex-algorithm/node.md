---
tag: EYD54X
kind: algorithm
slug: dijkstra-mutex-algorithm
name: Dijkstra's mutual exclusion algorithm
aliases: [Dijkstra 1965 mutex]
area: concurrency/mutual-exclusion
level: advanced
summary: The first published solution to mutual exclusion for n processes (1965), with read/write registers and a shared turn. It is deadlock free, but a process can starve.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: false, fcfs: false, bounded_bypass: false, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1965
  people: [Edsger W. Dijkstra]
  note: Dijkstra stated the mutual exclusion problem for n processes and gave this solution in a one-page paper in Communications of the ACM in 1965.
prereqs: [mutual-exclusion-problem, dekker-algorithm]
see_also: [knuth-mutex-algorithm, eisenberg-mcguire-algorithm, lamport-bakery-algorithm, burns-lamport-algorithm, deadlock-freedom, starvation-freedom, starvation]
sources:
  - paper: doi:10.1145/365559.365617
    title: E. W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the statement of the problem and the algorithm with the arrays b and c and the variable k
  - url: "https://lamport.azurewebsites.net/pubs/dijkstra.pdf"
    title: Leslie Lamport, Dijkstra Book, Chapter on Concurrent Algorithms, 2021
    locator: Section 2.3, Dijkstra's Algorithm (the proof sketch of deadlock freedom and the starvation run), and Section 2.5 on the requirements
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion with Read/Write Shared Memory (Dijkstra's algorithm)
---

Dijkstra's algorithm is the first published solution to the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes. In the same one-page paper of 1965, Dijkstra stated the problem itself: the processes share only read/write registers, nothing is known about their speeds, a process may stop in its remainder section, and they must never all be blocked. The algorithm extends the idea of a turn from [Dekker's algorithm](/dekker-algorithm/) to $n$ processes. It gives mutual exclusion and deadlock freedom. It is not starvation free: one process can enter again and again while another one waits forever.

## In plain words

There is one shared sign $k$ that names the process whose turn it is. A process that wants to enter first looks at the sign. If the sign names a process that is not trying at all, it writes its own name on the sign.

A process that sees its own name on the sign raises a hand ($c[i] \leftarrow false$) and looks around. If no other hand is up, it enters. If another hand is up, it tries again.

The turn holder wins in the end, because the others lower their hands. But a process can take the turn and keep it: while it goes around again and again, the others always see it as busy, so they never get the sign.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and deadlock freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. Dijkstra also asked that the solution be symmetric: no process may have a fixed priority.

## The algorithm

Each process $i$ has two flags, $b[i]$ and $c[i]$, both true at the start. The flag $b[i]$ is false while $i$ takes part (from the start of its entry section to the end of its exit section). The flag $c[i]$ is false while $i$ claims the critical section. The shared register $k$ holds a process number. Only process $i$ writes $b[i]$ and $c[i]$; every process can write $k$.

```pseudo id=main
LOCK(i)
L1  b[i] ← false
L2  loop
L3      if k ≠ i then
L4          c[i] ← true
L5          if b[k] = true then          ▷ read k, then read b of that process
L6              k ← i
L7      else
L8          c[i] ← false
L9          for each j ≠ i
L10             if c[j] = false then start the next round of the loop at L2
L11         exit the loop
                                       ▷ critical section
UNLOCK(i)
L12 c[i] ← true
L13 b[i] ← true
```

A process takes the turn only from a process that is in its remainder section, since $b[k] = true$ means exactly that. A process that does not have the turn keeps $c[i] = true$, so it does not block the turn holder. A process that has the turn enters only if every other $c[j]$ is true.

## Example

Two processes, $k = 0$ at the start. Process 1 comes first. The test file runs this schedule step by step.

| step | process | action | $k$ |
|---|---|---|---|
| 1 | 1 | $b[1] \leftarrow false$; reads $k = 0$; $c[1] \leftarrow true$; reads $k = 0$ and $b[0] = true$; $k \leftarrow 1$ | 1 |
| 2 | 0 | $b[0] \leftarrow false$; reads $k = 1$; $c[0] \leftarrow true$; reads $k = 1$ and $b[1] = false$ | 1 |
| 3 | 1 | reads $k = 1$; $c[1] \leftarrow false$; reads $c[0] = true$; enters | 1 |
| 4 | 0 | reads $k = 1$; $c[0] \leftarrow true$; reads $k = 1$ and $b[1] = false$ | 1 |
| 5 | 1 | leaves: $c[1] \leftarrow true$, $b[1] \leftarrow true$ | 1 |
| 6 | 0 | reads $k = 1$; $c[0] \leftarrow true$; reads $k = 1$ and $b[1] = true$; $k \leftarrow 0$ | 0 |
| 7 | 0 | reads $k = 0$; $c[0] \leftarrow false$; reads $c[1] = true$; enters | 0 |

In step 2, process 0 does not take the turn, because process 1 is not in its remainder section. In step 6 it is, so process 0 takes the turn.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion.** A process enters only after it wrote $c[i] \leftarrow false$ and then read every other $c[j]$ as true, and it keeps $c[i] = false$ until it leaves. Of two processes in the critical section, the one that wrote $c$ later would have read the $c$ of the other as false.
- **Deadlock freedom.** Suppose that processes loop forever and no one enters. Then the turn $k$ soon names a looping process, because a looping process takes it from an idle one. After that, no process can take it, since every looping process has $b = false$. So $k$ stops changing, the other looping processes keep their $c$ true, and the turn holder enters.
- **No starvation freedom.** Process 0 holds the turn and enters. Process 1 reads $b[0]$ each time while process 0 is in the critical section, so it sees false and never takes the turn. Process 0 leaves and enters again, and the run repeats. The test file builds this run and checks that, after each round, the whole state is the same as before, so the run can go on forever.

The test file checks mutual exclusion and deadlock freedom by exhaustive search of all interleavings for 2 processes (290 states with one passage each, 850 states forever) and for 3 processes with one passage each (33567 states). For 2 processes run forever, the search also finds that each process can starve and that the bypass has no bound. It runs the example above and seeded random schedules for 4 and 6 processes.

## Complexity

| measure | value |
|---|---|
| shared registers | $2n + 1$: the flags $b$ and $c$, and $k$ |
| entry without contention | $3 + (n - 1)$ steps if $k = i$ already; 5 more steps to take the turn |
| exit | 2 writes |
| bypass | unbounded |
| RMRs per passage | unbounded in both the CC and the DSM model |

A waiting process writes $c[i] \leftarrow true$ in every round of its loop, so even in the cache coherent model each round costs a remote reference, and the number of rounds has no bound.

## Properties

- Uses atomic read/write registers only, with small values.
- Mutual exclusion and deadlock freedom; not starvation free, even for $n = 2$.
- Symmetric: all processes run the same code, and no process has a fixed priority.
- The flags have one writer each; $k$ has $n$ writers.
- Not FCFS, and there is no bound on bypass.

## Variants and improvements

- **Knuth (1966).** [Knuth's algorithm](/knuth-mutex-algorithm/) was the first starvation free solution for $n$ processes. A process that leaves passes the turn on, so a waiting process gets it in the end.
- **de Bruijn (1967) and Eisenberg and McGuire (1972).** They lowered the worst wait. The [Eisenberg and McGuire algorithm](/eisenberg-mcguire-algorithm/) has bypass $n - 1$.
- **The bakery.** [Lamport's bakery algorithm](/lamport-bakery-algorithm/) (1974) is FCFS and uses only single-writer registers.
- **One flag per process.** The [Burns and Lamport algorithm](/burns-lamport-algorithm/) also gives deadlock freedom without starvation freedom, with one single-writer flag per process and no shared turn.

## When to use it

Read it to learn where the field began: the statement of the problem in this paper, with no assumptions on speeds and with the demand that every possible run be correct, is still the standard one. Do not use it for a real lock. It is not starvation free, it does not work on hardware with a weaker memory model without fences, and a lock built on an atomic instruction is simpler and faster.

## Pitfalls

**Starvation.** Deadlock freedom does not mean that every process gets in. A busy process can keep the turn forever; see [starvation](/starvation/).

**Two reads at L5.** The test "if $b[k]$" reads $k$ and then $b[k]$. Another process can change $k$ between the two reads. The proof allows this; an implementation must not assume that the two reads are one atomic step.

**Weak memory.** On TSO hardware such as x86, the write $c[i] \leftarrow false$ can wait in a store buffer while the process reads the other flags. The test file finds a run on the TSO model with two processes in the critical section.

**Not the semaphore.** Dijkstra also introduced the [semaphore](/semaphore/), which gives mutual exclusion directly from an atomic operation. The algorithm here uses only reads and writes.

## Implementations

## History

Dijkstra learned of Dekker's two-process solution in the early 1960s and published it in his notes. In 1965 he published this $n$-process solution in Communications of the ACM, with a proof. Lamport (2021) points out that the paper set the terms of the field: atomic shared registers, no assumption on speeds, processes that may stop in the remainder section, and deadlock freedom in every run. The algorithm is not starvation free, even for two processes. Knuth (1966) gave the first starvation free solution for $n$ processes, eight months later.

## References
